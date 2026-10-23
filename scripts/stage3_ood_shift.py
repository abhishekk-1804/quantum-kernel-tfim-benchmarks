"""
scripts/stage3_ood_shift.py
---------------------------
Stage 3: Controlled Out-of-Distribution (OOD) Phase-Shift Generalization (Task 6).
Statistical classification: CONFIRMATORY (Stage 3 Frozen Protocol).

Physical Formulation:
  - System: 1D Transverse-Field Ising Model on open chain (n=8).
  - Couplings: J_{i, i+1} ~ U[0.5, 1.5] for i in {0, ..., n-2}.
  - Training Domain (D_train): h_i ~ U[0.8, 1.5] (Paramagnetic & Critical), N_train = 40.
  - In-Distribution Test (D_test,ID): h_i ~ U[0.8, 1.5], N_test,ID = 100.
  - Out-of-Distribution Test (D_test,OOD): h_i ~ U[0.2, 0.7] (Deep Ferromagnetic), N_test,OOD = 100.
  - Target: Half-chain bipartite entanglement entropy S_{n/2}(\\psi) at n/2 = 4.

Model Arms Evaluated:
  1. FQ: Exact Gram blocks K_{ij} = |\\langle \\psi_i | \\psi_j \\rangle|^2, SVR precomputed, inner 3-fold CV tuning of C and eps.
  2. PQK-1: RBF on single-site \\langle X_i \\rangle (d=8), bandwidth gamma = c / n, inner 3-fold CV tuning of (C, c, eps).
  3. PQK-2nn: Frobenius RBF on edge 2-RDMs (X_e2 / 2.0, d=35), bandwidth gamma = c / n, inner 3-fold CV tuning of (C, c, eps).
  4. E2 (4n): RBF on 35-dim 2-point correlators (X_e2, d=35), bandwidth gamma = c / (4n), matching PQK-2nn identity (B == C).
  5. Linear_Ridge: Ridge regression on standardized 35-dim E2 features, tuning alpha in {1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100}.

Output:
  results/stage3/t6_ood_shift.csv
  Columns: seed, model, variant, id_r2, id_mae, ood_r2, ood_mae, delta_r2, best_params, inner_cv_score
"""

import os
import sys
import time
import json
import argparse
from typing import Dict, List, Any, Tuple, Optional, Sequence

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.model_selection import KFold
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error

# Add src and scripts to sys.path
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SCRIPTS = os.path.join(_PROJECT_ROOT, "scripts")
_SRC = os.path.join(_PROJECT_ROOT, "src")
for p in [_SRC, _SCRIPTS]:
    if p not in sys.path:
        sys.path.insert(0, p)

from hamiltonians import build_tfim, ground_state, half_chain_entropy, expect_x
from kernels import classical_features
from common import (
    C_GRID_V2,
    C_FACTORS_V2,
    EPSILON_GRID_V3,
)

DEFAULT_OUT_CSV = os.path.join(_PROJECT_ROOT, "results", "stage3", "t6_ood_shift.csv")
C_GRID_FQ = [0.1, 1.0, 10.0, 100.0, 1000.0]
ALPHA_GRID_RIDGE = [1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0]


def sample_domain_states(
    n: int,
    num_states: int,
    h_min: float,
    h_max: float,
    rng: np.random.Generator,
) -> Dict[str, Any]:
    """
    Generate valid disordered TFIM ground states in the even parity sector
    within a specified transverse field domain [h_min, h_max].

    Parameters
    ----------
    n : int
        Number of spins (n=8).
    num_states : int
        Number of states to sample.
    h_min : float
        Lower bound of transverse field uniform distribution.
    h_max : float
        Upper bound of transverse field uniform distribution.
    rng : np.random.Generator
        Deterministic random number generator.

    Returns
    -------
    dict with keys:
      'states': np.ndarray, shape (num_states, 2^n)
      'entropies': np.ndarray, shape (num_states,)
      'fields': np.ndarray, shape (num_states, n)
      'couplings': np.ndarray, shape (num_states, n-1)
      'residuals': np.ndarray, shape (num_states,)
    """
    states = []
    entropies = []
    fields_list = []
    couplings_list = []
    residuals = []

    for _ in range(num_states):
        J = rng.uniform(0.5, 1.5, size=n - 1)
        h = rng.uniform(h_min, h_max, size=n)
        H = build_tfim(n, g=1.0, J=1.0, boundary="open", couplings=J, fields=h)
        E0, psi, _ = ground_state(H, n, sector="even")

        # Verify eigenpair residual
        res = float(np.linalg.norm(H.dot(psi) - E0 * psi))
        if res >= 1e-10:
            raise RuntimeError(f"Ground state convergence failed: residual = {res} >= 1e-10")

        # Target: half-chain entanglement entropy at n/2 = 4
        S = half_chain_entropy(psi, n)

        states.append(psi)
        entropies.append(S)
        fields_list.append(h)
        couplings_list.append(J)
        residuals.append(res)

    return {
        "states": np.array(states, dtype=np.float64),
        "entropies": np.array(entropies, dtype=np.float64),
        "fields": np.array(fields_list, dtype=np.float64),
        "couplings": np.array(couplings_list, dtype=np.float64),
        "residuals": np.array(residuals, dtype=np.float64),
    }


def extract_features(
    states: np.ndarray,
    n: int = 8,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Extract representation spaces from quantum ground states:
    1. Single-site expectations <X_i> (shape: m, 8)
    2. Nearest-neighbor 2-point correlators (shape: m, 35)
    3. Scaled 2-RDM features X_pqk2 = X_e2 / 2.0 (shape: m, 35)

    Parameters
    ----------
    states : np.ndarray, shape (m, 2^n)
    n : int, default 8

    Returns
    -------
    X_x : np.ndarray, shape (m, n)
    X_e2 : np.ndarray, shape (m, 35)
    X_pqk2 : np.ndarray, shape (m, 35)
    """
    X_x = np.array([expect_x(psi, n) for psi in states], dtype=np.float64)
    X_e2 = np.array([classical_features(psi, n, mode="2pt_pauli_nn") for psi in states], dtype=np.float64)
    X_pqk2 = X_e2 / 2.0
    return X_x, X_e2, X_pqk2


def build_gram_matrices(
    train_states: np.ndarray,
    id_states: np.ndarray,
    ood_states: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Construct exact fidelity Gram blocks:
    K_ij = |<psi_i | psi_j>|^2

    Parameters
    ----------
    train_states : np.ndarray, shape (N_train, 2^n)
    id_states : np.ndarray, shape (N_id, 2^n)
    ood_states : np.ndarray, shape (N_ood, 2^n)

    Returns
    -------
    K_fq_train : np.ndarray, shape (N_train, N_train)
    K_fq_id : np.ndarray, shape (N_id, N_train)
    K_fq_ood : np.ndarray, shape (N_ood, N_train)
    """
    K_fq_train = (train_states @ train_states.T) ** 2
    K_fq_id = (id_states @ train_states.T) ** 2
    K_fq_ood = (ood_states @ train_states.T) ** 2
    return K_fq_train, K_fq_id, K_fq_ood


def evaluate_svr_rbf_dual(
    X_tr: np.ndarray,
    y_tr_z: np.ndarray,
    y_tr_orig: np.ndarray,
    X_te_id: np.ndarray,
    y_te_id: np.ndarray,
    X_te_ood: np.ndarray,
    y_te_ood: np.ndarray,
    gamma_denom: float,
    y_mean: float,
    y_std: float,
    kf: KFold,
    c_factors: Sequence[float] = C_FACTORS_V2,
    c_grid: Sequence[float] = C_GRID_V2,
    eps_grid: Sequence[float] = EPSILON_GRID_V3,
) -> Dict[str, Any]:
    """
    Tune SVR RBF kernel strictly on D_train via 3-fold CV using precomputed squared distance matrices,
    then evaluate on both D_test,ID and D_test,OOD.
    """
    D2_tr = cdist(X_tr, X_tr, metric="sqeuclidean")
    D2_id = cdist(X_te_id, X_tr, metric="sqeuclidean")
    D2_ood = cdist(X_te_ood, X_tr, metric="sqeuclidean")

    folds_data = []
    for tr_idx, val_idx in kf.split(X_tr):
        f_y_tr = y_tr_orig[tr_idx]
        f_m, f_s = float(np.mean(f_y_tr)), float(np.std(f_y_tr))
        if f_s < 1e-12:
            f_s = 1.0
        f_y_tr_z = (f_y_tr - f_m) / f_s
        f_y_val = y_tr_orig[val_idx]
        D2_fold_tr = D2_tr[np.ix_(tr_idx, tr_idx)]
        D2_fold_val = D2_tr[np.ix_(val_idx, tr_idx)]
        folds_data.append((D2_fold_tr, D2_fold_val, f_y_tr_z, f_y_val, f_m, f_s))

    best_cv = -np.inf
    best_C = c_grid[0]
    best_c = c_factors[0]
    best_eps = eps_grid[0]

    for c_val in c_factors:
        gamma = float(c_val / gamma_denom)
        fold_kernels = []
        for D2_fold_tr, D2_fold_val, f_y_tr_z, f_y_val, f_m, f_s in folds_data:
            K_tr_fold = np.exp(-gamma * D2_fold_tr)
            K_val_fold = np.exp(-gamma * D2_fold_val)
            fold_kernels.append((K_tr_fold, K_val_fold, f_y_tr_z, f_y_val, f_m, f_s))

        for C_val in c_grid:
            for eps_val in eps_grid:
                scores = []
                for K_tr_fold, K_val_fold, f_y_tr_z, f_y_val, f_m, f_s in fold_kernels:
                    svr = SVR(kernel="precomputed", C=float(C_val), epsilon=float(eps_val))
                    svr.fit(K_tr_fold, f_y_tr_z)
                    pred_z = svr.predict(K_val_fold)
                    pred_orig = pred_z * f_s + f_m
                    scores.append(r2_score(f_y_val, pred_orig))
                mean_cv = float(np.mean(scores))
                if mean_cv > best_cv:
                    best_cv = mean_cv
                    best_C, best_c, best_eps = C_val, c_val, eps_val

    # Refit final model on full D_train
    best_gamma = float(best_c / gamma_denom)
    K_full_tr = np.exp(-best_gamma * D2_tr)
    K_full_id = np.exp(-best_gamma * D2_id)
    K_full_ood = np.exp(-best_gamma * D2_ood)

    svr_final = SVR(kernel="precomputed", C=float(best_C), epsilon=float(best_eps))
    svr_final.fit(K_full_tr, y_tr_z)

    pred_id = svr_final.predict(K_full_id) * y_std + y_mean
    pred_ood = svr_final.predict(K_full_ood) * y_std + y_mean

    id_r2 = float(r2_score(y_te_id, pred_id))
    id_mae = float(mean_absolute_error(y_te_id, pred_id))
    ood_r2 = float(r2_score(y_te_ood, pred_ood))
    ood_mae = float(mean_absolute_error(y_te_ood, pred_ood))
    delta_r2 = id_r2 - ood_r2
    best_params = f"C={best_C}_gamma={best_gamma:.6g}_eps={best_eps}"

    return {
        "id_r2": id_r2,
        "id_mae": id_mae,
        "ood_r2": ood_r2,
        "ood_mae": ood_mae,
        "delta_r2": delta_r2,
        "best_params": best_params,
        "inner_cv_score": best_cv,
    }


def evaluate_svr_fq_dual(
    K_tr: np.ndarray,
    y_tr_z: np.ndarray,
    y_tr_orig: np.ndarray,
    K_id: np.ndarray,
    y_te_id: np.ndarray,
    K_ood: np.ndarray,
    y_te_ood: np.ndarray,
    y_mean: float,
    y_std: float,
    kf: KFold,
    c_grid: Sequence[float] = C_GRID_FQ,
    eps_grid: Sequence[float] = EPSILON_GRID_V3,
) -> Dict[str, Any]:
    """
    Tune SVR on precomputed exact fidelity Gram blocks strictly on D_train via 3-fold CV,
    then evaluate on both D_test,ID and D_test,OOD.
    """
    folds_data = []
    for tr_idx, val_idx in kf.split(K_tr):
        f_y_tr = y_tr_orig[tr_idx]
        f_m, f_s = float(np.mean(f_y_tr)), float(np.std(f_y_tr))
        if f_s < 1e-12:
            f_s = 1.0
        f_y_tr_z = (f_y_tr - f_m) / f_s
        f_y_val = y_tr_orig[val_idx]
        K_fold_tr = K_tr[np.ix_(tr_idx, tr_idx)]
        K_fold_val = K_tr[np.ix_(val_idx, tr_idx)]
        folds_data.append((K_fold_tr, K_fold_val, f_y_tr_z, f_y_val, f_m, f_s))

    best_cv = -np.inf
    best_C = c_grid[0]
    best_eps = eps_grid[0]

    for C_val in c_grid:
        for eps_val in eps_grid:
            scores = []
            for K_fold_tr, K_fold_val, f_y_tr_z, f_y_val, f_m, f_s in folds_data:
                svr = SVR(kernel="precomputed", C=float(C_val), epsilon=float(eps_val))
                svr.fit(K_fold_tr, f_y_tr_z)
                pred_z = svr.predict(K_fold_val)
                pred_orig = pred_z * f_s + f_m
                scores.append(r2_score(f_y_val, pred_orig))
            mean_cv = float(np.mean(scores))
            if mean_cv > best_cv:
                best_cv = mean_cv
                best_C, best_eps = C_val, eps_val

    # Refit final model on full D_train
    svr_final = SVR(kernel="precomputed", C=float(best_C), epsilon=float(best_eps))
    svr_final.fit(K_tr, y_tr_z)

    pred_id = svr_final.predict(K_id) * y_std + y_mean
    pred_ood = svr_final.predict(K_ood) * y_std + y_mean

    id_r2 = float(r2_score(y_te_id, pred_id))
    id_mae = float(mean_absolute_error(y_te_id, pred_id))
    ood_r2 = float(r2_score(y_te_ood, pred_ood))
    ood_mae = float(mean_absolute_error(y_te_ood, pred_ood))
    delta_r2 = id_r2 - ood_r2
    best_params = f"C={best_C}_eps={best_eps}"

    return {
        "id_r2": id_r2,
        "id_mae": id_mae,
        "ood_r2": ood_r2,
        "ood_mae": ood_mae,
        "delta_r2": delta_r2,
        "best_params": best_params,
        "inner_cv_score": best_cv,
    }


def evaluate_linear_ridge_dual(
    X_tr: np.ndarray,
    y_tr_z: np.ndarray,
    y_tr_orig: np.ndarray,
    X_te_id: np.ndarray,
    y_te_id: np.ndarray,
    X_te_ood: np.ndarray,
    y_te_ood: np.ndarray,
    y_mean: float,
    y_std: float,
    kf: KFold,
    alpha_grid: Sequence[float] = ALPHA_GRID_RIDGE,
) -> Dict[str, Any]:
    """
    Tune Linear Ridge regression strictly on D_train via 3-fold CV with inner fold standardization,
    then evaluate on both D_test,ID and D_test,OOD.
    """
    best_cv = -np.inf
    best_alpha = alpha_grid[0]

    for alpha_val in alpha_grid:
        scores = []
        for tr_idx, val_idx in kf.split(X_tr):
            sc = StandardScaler()
            f_X_tr_std = sc.fit_transform(X_tr[tr_idx])
            f_X_val_std = sc.transform(X_tr[val_idx])

            f_y_tr = y_tr_orig[tr_idx]
            f_m, f_s = float(np.mean(f_y_tr)), float(np.std(f_y_tr))
            if f_s < 1e-12:
                f_s = 1.0
            f_y_tr_z = (f_y_tr - f_m) / f_s
            f_y_val = y_tr_orig[val_idx]

            clf = Ridge(alpha=float(alpha_val))
            clf.fit(f_X_tr_std, f_y_tr_z)
            pred_z = clf.predict(f_X_val_std)
            pred_orig = pred_z * f_s + f_m
            scores.append(r2_score(f_y_val, pred_orig))
        mean_cv = float(np.mean(scores))
        if mean_cv > best_cv:
            best_cv = mean_cv
            best_alpha = alpha_val

    # Refit on full D_train with full scaler
    sc_full = StandardScaler()
    X_tr_std = sc_full.fit_transform(X_tr)
    X_id_std = sc_full.transform(X_te_id)
    X_ood_std = sc_full.transform(X_te_ood)

    clf_final = Ridge(alpha=float(best_alpha))
    clf_final.fit(X_tr_std, y_tr_z)

    pred_id = clf_final.predict(X_id_std) * y_std + y_mean
    pred_ood = clf_final.predict(X_ood_std) * y_std + y_mean

    id_r2 = float(r2_score(y_te_id, pred_id))
    id_mae = float(mean_absolute_error(y_te_id, pred_id))
    ood_r2 = float(r2_score(y_te_ood, pred_ood))
    ood_mae = float(mean_absolute_error(y_te_ood, pred_ood))
    delta_r2 = id_r2 - ood_r2
    best_params = f"alpha={best_alpha}"

    return {
        "id_r2": id_r2,
        "id_mae": id_mae,
        "ood_r2": ood_r2,
        "ood_mae": ood_mae,
        "delta_r2": delta_r2,
        "best_params": best_params,
        "inner_cv_score": best_cv,
    }


def run_seed_evaluation(
    seed: int,
    n: int = 8,
    N_train: int = 40,
    N_test_id: int = 100,
    N_test_ood: int = 100,
) -> List[Dict[str, Any]]:
    """
    Execute full Stage 3 OOD evaluation for a single seed across all 5 model arms:
      1. FQ (variant: none)
      2. PQK-1 (variant: none)
      3. PQK-2nn (variant: none)
      4. E2 (4n) (variant: raw_4n_grid)
      5. Linear_Ridge (variant: none)
    """
    rng = np.random.default_rng(seed)

    # 1. Sample states from domains
    train_data = sample_domain_states(n, N_train, 0.8, 1.5, rng)
    id_data = sample_domain_states(n, N_test_id, 0.8, 1.5, rng)
    ood_data = sample_domain_states(n, N_test_ood, 0.2, 0.7, rng)

    tr_states, y_tr = train_data["states"], train_data["entropies"]
    id_states, y_id = id_data["states"], id_data["entropies"]
    ood_states, y_ood = ood_data["states"], ood_data["entropies"]

    # Target normalization parameters from D_train strictly
    y_mean = float(np.mean(y_tr))
    y_std = float(np.std(y_tr))
    if y_std < 1e-12:
        y_std = 1.0
    y_tr_z = (y_tr - y_mean) / y_std

    kf = KFold(n_splits=3, shuffle=True, random_state=42)

    # 2. Extract feature representations
    X_x_tr, X_e2_tr, X_pqk2_tr = extract_features(tr_states, n)
    X_x_id, X_e2_id, X_pqk2_id = extract_features(id_states, n)
    X_x_ood, X_e2_ood, X_pqk2_ood = extract_features(ood_states, n)

    # 3. Build Gram matrices for FQ
    K_fq_tr, K_fq_id, K_fq_ood = build_gram_matrices(tr_states, id_states, ood_states)

    results = []

    # Arm 1: FQ
    res_fq = evaluate_svr_fq_dual(
        K_fq_tr, y_tr_z, y_tr, K_fq_id, y_id, K_fq_ood, y_ood, y_mean, y_std, kf
    )
    results.append({
        "seed": seed, "model": "FQ", "variant": "none", **res_fq
    })

    # Arm 2: PQK-1
    res_pqk1 = evaluate_svr_rbf_dual(
        X_x_tr, y_tr_z, y_tr, X_x_id, y_id, X_x_ood, y_ood,
        float(n), y_mean, y_std, kf
    )
    results.append({
        "seed": seed, "model": "PQK-1", "variant": "none", **res_pqk1
    })

    # Arm 3: PQK-2nn
    res_pqk2 = evaluate_svr_rbf_dual(
        X_pqk2_tr, y_tr_z, y_tr, X_pqk2_id, y_id, X_pqk2_ood, y_ood,
        float(n), y_mean, y_std, kf
    )
    results.append({
        "seed": seed, "model": "PQK-2nn", "variant": "none", **res_pqk2
    })

    # Arm 4: E2 (4n)
    res_e2 = evaluate_svr_rbf_dual(
        X_e2_tr, y_tr_z, y_tr, X_e2_id, y_id, X_e2_ood, y_ood,
        float(4 * n), y_mean, y_std, kf
    )
    results.append({
        "seed": seed, "model": "E2 (4n)", "variant": "raw_4n_grid", **res_e2
    })

    # Arm 5: Linear_Ridge
    res_ridge = evaluate_linear_ridge_dual(
        X_e2_tr, y_tr_z, y_tr, X_e2_id, y_id, X_e2_ood, y_ood,
        y_mean, y_std, kf
    )
    results.append({
        "seed": seed, "model": "Linear_Ridge", "variant": "none", **res_ridge
    })

    return results


def main():
    parser = argparse.ArgumentParser(description="Stage 3: Controlled OOD Phase-Shift Generalization")
    parser.add_argument("--preflight", action="store_true", help="Run 3-seed preflight runtime check")
    parser.add_argument("--run", action="store_true", help="Execute full experiment sweep")
    parser.add_argument("--seeds", nargs="+", type=int, default=list(range(20)), help="Seeds to evaluate")
    parser.add_argument("--out", type=str, default=DEFAULT_OUT_CSV, help="Output CSV path")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    if args.preflight:
        print("=== STAGE 3 PREFLIGHT RUNTIME GATE ===")
        preflight_seeds = [0, 1, 2] if not args.seeds or len(args.seeds) > 3 else args.seeds
        times = []
        for s in preflight_seeds:
            t0 = time.time()
            rows = run_seed_evaluation(s)
            elapsed = time.time() - t0
            times.append(elapsed)
            print(f"Seed {s}: {elapsed:.2f} s ({len(rows)} model evaluations)")

        avg_seed_time = float(np.mean(times))
        total_projected_sec = avg_seed_time * 20.0
        total_projected_min = total_projected_sec / 60.0
        print(f"\nAverage time per seed: {avg_seed_time:.2f} s")
        print(f"Total projected wall time for 20 seeds: {total_projected_sec:.2f} s ({total_projected_min:.2f} min)")

        GATE_LIMIT_SEC = 5400.0  # 1.5 hours
        if total_projected_sec > GATE_LIMIT_SEC:
            print(f"PREFLIGHT GATE: FAILED (Projected {total_projected_sec:.2f} s > {GATE_LIMIT_SEC} s)")
            sys.exit(1)
        else:
            print(f"PREFLIGHT GATE: PASS (Projected {total_projected_sec:.2f} s <= {GATE_LIMIT_SEC} s)")
        return

    if not args.run:
        print("Please specify --run or --preflight")
        return

    # Load existing rows for resumption
    completed_keys = set()
    if os.path.exists(args.out):
        try:
            df_existing = pd.read_csv(args.out)
            for _, r in df_existing.iterrows():
                completed_keys.add((int(r["seed"]), str(r["model"])))
            print(f"Loaded existing CSV with {len(df_existing)} rows ({len(completed_keys)} seed-model pairs).")
        except Exception as e:
            print(f"Warning: could not read existing CSV: {e}")

    fieldnames = [
        "seed", "model", "variant",
        "id_r2", "id_mae", "ood_r2", "ood_mae", "delta_r2",
        "best_params", "inner_cv_score"
    ]

    # Write header if file does not exist
    if not os.path.exists(args.out):
        df_empty = pd.DataFrame(columns=fieldnames)
        df_empty.to_csv(args.out, index=False)

    print(f"Starting Stage 3 OOD sweep across {len(args.seeds)} seeds...")
    sweep_t0 = time.time()

    for s in args.seeds:
        seed_needed = any((s, m) not in completed_keys for m in ["FQ", "PQK-1", "PQK-2nn", "E2 (4n)", "Linear_Ridge"])
        if not seed_needed:
            print(f"Seed {s}: all models already completed, skipping.")
            continue

        seed_t0 = time.time()
        seed_results = run_seed_evaluation(s)
        new_rows = []
        for row in seed_results:
            key = (row["seed"], row["model"])
            if key not in completed_keys:
                new_rows.append(row)
                completed_keys.add(key)

        if new_rows:
            df_new = pd.DataFrame(new_rows)
            df_new.to_csv(args.out, mode="a", header=False, index=False)
            elapsed_seed = time.time() - seed_t0
            print(f"Seed {s}: appended {len(new_rows)} rows in {elapsed_seed:.2f} s.")

    total_time = time.time() - sweep_t0
    print(f"\nStage 3 OOD sweep completed in {total_time:.2f} s ({total_time / 60.0:.2f} min).")


if __name__ == "__main__":
    main()
