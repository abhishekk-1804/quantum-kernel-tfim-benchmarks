"""
scripts/run_t5_noise.py
-----------------------
Phase 2b: Shared-Basis Measurement Noise & Depolarizing Channel Benchmark.
Evaluates Task 1 Half-chain entropy regression (n=8, N_train=40, N_test=200, 20 seeds):
1. Finite-shots sweep (S in {100, 1000, 10000} and S=inf):
   - Shared-basis bitstring sampling (Basis X, Y, Z) with budget S per state
   - Reconstructed Noisy 1-RDMs (PQK-1), Noisy 2-RDMs (PQK-2nn), Noisy E (raw/std),
     Noisy E2 (raw), Noisy F (std, Ridge)
   - Destructive swap-test for FQ (raw and PSD-clipped)
2. Depolarizing channel sweep (p in {0.00, 0.01, 0.02, 0.04, 0.06, 0.08}):
   - Subsystem depolarizing: (1-p)^k rho_k + (1-(1-p)^k)(I/d_k)
   - Classical scaling: 1-body Paulis by (1-p), 2-body Paulis by (1-p)^2
   - FQ mixed-state normalized overlap Tr(rho_i rho_j)/sqrt(Tr(rho_i^2)Tr(rho_j^2))
"""

import os
import sys
import time
import json
import argparse
import subprocess
from typing import Dict, List, Any, Tuple

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.model_selection import KFold
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error

# Set up paths
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC = os.path.join(_PROJECT_ROOT, "src")
_SCRIPTS = os.path.join(_PROJECT_ROOT, "scripts")
for p in [_SRC, _SCRIPTS]:
    if p not in sys.path:
        sys.path.insert(0, p)

from common import (
    SEEDS,
    C_GRID_V2,
    C_FACTORS_V2,
    C_FACTORS_STD_V2,
    ALPHA_GRID_V2,
    EPSILON_GRID_V3,
    make_split,
    write_run_meta,
)
from noise import (
    get_basis_rotation_matrix,
    sample_bitstrings_basis,
    extract_basis_expectations,
    reconstruct_noisy_features_from_basis,
    destructive_swap_test_fidelity,
    fidelity_clip_psd,
    mixed_state_fidelity_gram,
)
from kernels import classical_features

# Precomputed rotation unitaries at n=8
_UX_8 = get_basis_rotation_matrix("X", 8)
_UY_8 = get_basis_rotation_matrix("Y", 8)

# Shot sweeps
SHOTS_FULL = [100, 1000, 10000]
SHOTS_QUICK = [100, 1000]

# Depolarizing sweeps
DEPOL_FULL = [0.00, 0.01, 0.02, 0.04, 0.06, 0.08]
DEPOL_QUICK = [0.00, 0.04]


def get_completed_keys(csv_path: str) -> set:
    """Read existing CSV and return completed (experiment, noise_level, seed, model, variant)."""
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        return set()
    try:
        df = pd.read_csv(csv_path)
        if len(df) == 0:
            return set()
        keys = set()
        for _, row in df.iterrows():
            keys.add((
                str(row["experiment"]),
                str(row["noise_level"]),
                int(row["seed"]),
                str(row["model"]),
                str(row["variant"]),
                str(row["metric"]),
            ))
        return keys
    except Exception as e:
        print(f"Warning: could not parse {csv_path} for resumption ({e})", flush=True)
        return set()


def evaluate_svr_rbf_fast(
    X_tr: np.ndarray,
    y_tr_z: np.ndarray,
    y_tr_orig: np.ndarray,
    X_te: np.ndarray,
    y_te: np.ndarray,
    gamma_denom: float,
    c_factors: list,
    y_mean: float,
    y_std: float,
    kf: KFold,
) -> Tuple[float, float, str, float]:
    """Fast inner 3-fold CV tuning for SVR with precomputed distance matrices."""
    D2_tr = cdist(X_tr, X_tr, metric="sqeuclidean")
    D2_te = cdist(X_te, X_tr, metric="sqeuclidean")

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
    best_C, best_c, best_eps = C_GRID_V2[0], c_factors[0], EPSILON_GRID_V3[0]

    for c_val in c_factors:
        gamma = float(c_val / gamma_denom)
        fold_kernels = []
        for D2_fold_tr, D2_fold_val, f_y_tr_z, f_y_val, f_m, f_s in folds_data:
            K_tr_fold = np.exp(-gamma * D2_fold_tr)
            K_val_fold = np.exp(-gamma * D2_fold_val)
            fold_kernels.append((K_tr_fold, K_val_fold, f_y_tr_z, f_y_val, f_m, f_s))

        for C_val in C_GRID_V2:
            for eps_val in EPSILON_GRID_V3:
                scores = []
                for K_tr_fold, K_val_fold, f_y_tr_z, f_y_val, f_m, f_s in fold_kernels:
                    svr = SVR(kernel="precomputed", C=C_val, epsilon=eps_val)
                    svr.fit(K_tr_fold, f_y_tr_z)
                    pred_z = svr.predict(K_val_fold)
                    pred_orig = pred_z * f_s + f_m
                    scores.append(r2_score(f_y_val, pred_orig))
                mean_cv = float(np.mean(scores))
                if mean_cv > best_cv:
                    best_cv = mean_cv
                    best_C, best_c, best_eps = C_val, c_val, eps_val

    # Refit on full train set
    best_gamma = float(best_c / gamma_denom)
    K_full_tr = np.exp(-best_gamma * D2_tr)
    K_full_te = np.exp(-best_gamma * D2_te)

    svr_final = SVR(kernel="precomputed", C=best_C, epsilon=best_eps)
    svr_final.fit(K_full_tr, y_tr_z)
    pred_te_z = svr_final.predict(K_full_te)
    pred_te = pred_te_z * y_std + y_mean

    test_r2 = float(r2_score(y_te, pred_te))
    test_mae = float(mean_absolute_error(y_te, pred_te))
    params_str = json.dumps({"C": float(best_C), "c": float(best_c), "epsilon": float(best_eps)})
    return test_r2, test_mae, params_str, best_cv


def evaluate_svr_precomputed(
    K_tr: np.ndarray,
    y_tr_z: np.ndarray,
    y_tr_orig: np.ndarray,
    K_te: np.ndarray,
    y_te: np.ndarray,
    y_mean: float,
    y_std: float,
    kf: KFold,
    clip_psd: bool = False,
) -> Tuple[float, float, str, float]:
    """Inner 3-fold CV tuning for SVR with a precomputed Gram matrix (FQ)."""
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
        if clip_psd:
            K_fold_tr = fidelity_clip_psd(K_fold_tr)
        folds_data.append((K_fold_tr, K_fold_val, f_y_tr_z, f_y_val, f_m, f_s))

    best_cv = -np.inf
    best_C, best_eps = C_GRID_V2[0], EPSILON_GRID_V3[0]

    for C_val in C_GRID_V2:
        for eps_val in EPSILON_GRID_V3:
            scores = []
            for K_fold_tr, K_fold_val, f_y_tr_z, f_y_val, f_m, f_s in folds_data:
                svr = SVR(kernel="precomputed", C=C_val, epsilon=eps_val)
                svr.fit(K_fold_tr, f_y_tr_z)
                pred_z = svr.predict(K_fold_val)
                pred_orig = pred_z * f_s + f_m
                scores.append(r2_score(f_y_val, pred_orig))
            mean_cv = float(np.mean(scores))
            if mean_cv > best_cv:
                best_cv = mean_cv
                best_C, best_eps = C_val, eps_val

    # Refit
    K_fit_tr = fidelity_clip_psd(K_tr) if clip_psd else K_tr
    svr_final = SVR(kernel="precomputed", C=best_C, epsilon=best_eps)
    svr_final.fit(K_fit_tr, y_tr_z)
    pred_te_z = svr_final.predict(K_te)
    pred_te = pred_te_z * y_std + y_mean

    test_r2 = float(r2_score(y_te, pred_te))
    test_mae = float(mean_absolute_error(y_te, pred_te))
    params_str = json.dumps({"C": float(best_C), "epsilon": float(best_eps)})
    return test_r2, test_mae, params_str, best_cv


def evaluate_ridge(
    X_tr_std: np.ndarray,
    y_tr_z: np.ndarray,
    y_tr_orig: np.ndarray,
    X_te_std: np.ndarray,
    y_te: np.ndarray,
    y_mean: float,
    y_std: float,
    kf: KFold,
) -> Tuple[float, float, str, float]:
    """Inner 3-fold CV tuning for Ridge regression."""
    folds_data = []
    for tr_idx, val_idx in kf.split(X_tr_std):
        f_y_tr = y_tr_orig[tr_idx]
        f_m, f_s = float(np.mean(f_y_tr)), float(np.std(f_y_tr))
        if f_s < 1e-12:
            f_s = 1.0
        f_y_tr_z = (f_y_tr - f_m) / f_s
        f_y_val = y_tr_orig[val_idx]
        folds_data.append((X_tr_std[tr_idx], X_tr_std[val_idx], f_y_tr_z, f_y_val, f_m, f_s))

    best_cv = -np.inf
    best_alpha = ALPHA_GRID_V2[0]

    for alpha in ALPHA_GRID_V2:
        scores = []
        for X_fold_tr, X_fold_val, f_y_tr_z, f_y_val, f_m, f_s in folds_data:
            ridge = Ridge(alpha=alpha)
            ridge.fit(X_fold_tr, f_y_tr_z)
            pred_z = ridge.predict(X_fold_val)
            pred_orig = pred_z * f_s + f_m
            scores.append(r2_score(f_y_val, pred_orig))
        mean_cv = float(np.mean(scores))
        if mean_cv > best_cv:
            best_cv = mean_cv
            best_alpha = alpha

    ridge_final = Ridge(alpha=best_alpha)
    ridge_final.fit(X_tr_std, y_tr_z)
    pred_te_z = ridge_final.predict(X_te_std)
    pred_te = pred_te_z * y_std + y_mean

    test_r2 = float(r2_score(y_te, pred_te))
    test_mae = float(mean_absolute_error(y_te, pred_te))
    params_str = json.dumps({"alpha": float(best_alpha)})
    return test_r2, test_mae, params_str, best_cv


def run_noise_benchmark(
    seeds: list,
    quick: bool = False,
    out_csv: str = None,
    worker_id: int = None,
):
    """Run Phase 2b benchmarks across assigned seeds."""
    if out_csv is None:
        if worker_id is not None:
            out_csv = os.path.join("results", f"t5_noise_worker{worker_id}.csv")
        else:
            out_csv = os.path.join("results", "t5_noise.csv")

    os.makedirs(os.path.dirname(os.path.abspath(out_csv)), exist_ok=True)
    write_run_meta()

    shots_list = SHOTS_QUICK if quick else SHOTS_FULL
    depol_list = DEPOL_QUICK if quick else DEPOL_FULL

    fieldnames = [
        "experiment", "noise_param", "noise_level", "seed", "n", "N_train",
        "model", "variant", "metric", "value", "best_params", "inner_cv_score",
        "lam_min", "train_shots", "predict_shots", "total_shots", "fit_seconds",
    ]

    completed_keys = get_completed_keys(out_csv)
    if completed_keys:
        print(f"Resumption: found {len(completed_keys)} completed rows in {out_csv}.", flush=True)

    # Load noiseless baseline from results/t1_entropy_gridv3.csv for S=inf / p=0 reference
    t1_v3_path = os.path.join("results", "t1_entropy_gridv3.csv")
    df_noiseless = pd.read_csv(t1_v3_path) if os.path.exists(t1_v3_path) else None

    kf = KFold(n_splits=3, shuffle=True, random_state=42)
    n = 8
    N_train = 40
    N_test = 200
    m = N_train + N_test

    print(f"=== Starting T5 Noise Benchmark (Seeds: {seeds}, Quick: {quick}) ===", flush=True)

    for seed in seeds:
        t_seed_start = time.time()
        print(f"\n--- [Seed {seed:2d}] Generating ground states (n=8, N_train=40, N_test=200) ---", flush=True)
        tr_states, tr_targets, te_states, te_targets, _ = make_split("t1", n=n, N=N_train, seed=seed)
        all_states = np.vstack([tr_states, te_states])  # shape (240, 256)

        # Target statistics
        y_mean = float(np.mean(tr_targets))
        y_std = float(np.std(tr_targets))
        if y_std < 1e-12:
            y_std = 1.0
        y_tr_z = (tr_targets - y_mean) / y_std

        # Precompute state rotations for all 240 states
        all_psi_x = (all_states @ _UX_8.T)
        all_psi_y = (all_states @ _UY_8.T)
        probs_x = np.abs(all_psi_x) ** 2
        probs_y = np.abs(all_psi_y) ** 2
        probs_z = np.abs(all_states) ** 2

        # Bitstring basis indices and signs
        dim = 256
        k_indices = np.arange(dim)
        bitstrings = ((k_indices[:, None] >> np.arange(n - 1, -1, -1)) & 1)
        signs = 1.0 - 2.0 * bitstrings  # (256, 8)
        signs_nn = np.column_stack([signs[:, i] * signs[:, i + 1] for i in range(n - 1)])  # (256, 7)
        signs_zz_all = np.column_stack([signs[:, i] * signs[:, j] for i in range(n) for j in range(i + 1, n)])  # (256, 28)

        # Pure fidelity matrix for swap test
        K_pure_full = (all_states @ all_states.T) ** 2

        new_rows = []

        # =====================================================================
        # 1. REFERENCE BASELINE: S = inf / p = 0.00
        # =====================================================================
        # Pure features
        pure_x_all = np.array([classical_features(psi, n, mode="1pt_X") for psi in all_states])
        pure_e2_all = np.array([classical_features(psi, n, mode="2pt_pauli_nn") for psi in all_states])
        pure_e_all = np.array([classical_features(psi, n, mode="full_corr") for psi in all_states])

        # Evaluate Seed 0 noiseless consistency check against t1_entropy_gridv3.csv
        if seed == 0 and df_noiseless is not None:
            sub_s0 = df_noiseless[(df_noiseless["seed"] == 0) & (df_noiseless["N_train"] == 40) & (df_noiseless["metric"] == "r2")]
            # Check PQK-1
            r2_pqk1, _, _, _ = evaluate_svr_rbf_fast(
                pure_x_all[:N_train], y_tr_z, tr_targets, pure_x_all[N_train:], te_targets,
                2.0 * n, C_FACTORS_V2, y_mean, y_std, kf
            )
            val_pqk1_csv = sub_s0[sub_s0["model"] == "PQK-1 (== RBF on <X>)"]["value"].values[0]
            assert abs(r2_pqk1 - val_pqk1_csv) < 1e-10, f"Seed 0 pure PQK-1 mismatch: {r2_pqk1} vs {val_pqk1_csv}"
            print(f"  [Sanity check] Seed 0 fresh pure PQK-1 matches gridv3 baseline: diff = {abs(r2_pqk1 - val_pqk1_csv):.2e}", flush=True)

        # Add S=inf rows to results
        for exp_type, noise_param, lvl_str, s_val, p_val in [
            ("finite_shots", "shots", "inf", np.inf, 0.0),
            ("depolarizing", "p", "0.00", np.inf, 0.0),
        ]:
            if df_noiseless is not None:
                sub_ref = df_noiseless[(df_noiseless["seed"] == seed) & (df_noiseless["N_train"] == 40)]
                for _, r_ref in sub_ref.iterrows():
                    m_name = str(r_ref["model"])
                    v_name = str(r_ref["variant"])
                    metric = str(r_ref["metric"])
                    val = float(r_ref["value"])
                    b_params = str(r_ref["best_params"])
                    cv_sc = r_ref.get("inner_cv_score", "")

                    # Map model names to suite
                    target_models = []
                    if m_name == "PQK-1 (== RBF on <X>)":
                        target_models.append(("PQK-1", "none", 2 * N_train, 2 * N_test, 2 * m))
                    elif m_name == "PQK-2nn":
                        target_models.append(("PQK-2nn", "none", 3 * N_train, 3 * N_test, 3 * m))
                    elif m_name == "E" and v_name == "raw":
                        target_models.append(("E", "raw", 3 * N_train, 3 * N_test, 3 * m))
                    elif m_name == "E" and v_name == "std":
                        target_models.append(("E", "std", 3 * N_train, 3 * N_test, 3 * m))
                    elif m_name == "E2" and v_name == "raw":
                        target_models.append(("E2", "raw", 3 * N_train, 3 * N_test, 3 * m))
                    elif m_name == "F" and v_name == "std":
                        target_models.append(("F", "std", 3 * N_train, 3 * N_test, 3 * m))
                    elif m_name == "FQ":
                        if exp_type == "finite_shots":
                            target_models.append(("FQ-raw", "none", 780, 8000, 28680))
                            target_models.append(("FQ-clipped", "none", 780, 8000, 28680))
                        else:
                            target_models.append(("FQ", "mixed_state_overlap", 780, 8000, 28680))

                    for mod_n, var_n, tr_sh, te_sh, tot_sh in target_models:
                        key = (exp_type, lvl_str, seed, mod_n, var_n, metric)
                        if key not in completed_keys:
                            new_rows.append({
                                "experiment": exp_type, "noise_param": noise_param, "noise_level": lvl_str,
                                "seed": seed, "n": n, "N_train": N_train, "model": mod_n, "variant": var_n,
                                "metric": metric, "value": val, "best_params": b_params,
                                "inner_cv_score": cv_sc, "lam_min": 0.0,
                                "train_shots": "inf" if np.isinf(s_val) else tr_sh * s_val,
                                "predict_shots": "inf" if np.isinf(s_val) else te_sh * s_val,
                                "total_shots": "inf" if np.isinf(s_val) else tot_sh * s_val,
                                "fit_seconds": 0.0,
                            })

        # =====================================================================
        # 2. EXPERIMENT A: FINITE SHOTS SWEEP
        # =====================================================================
        for S in shots_list:
            lvl_str = str(S)
            needed_models = [
                m for m in ["PQK-1", "PQK-2nn", "FQ-raw", "FQ-clipped", "E", "E2", "F"]
                if ("finite_shots", lvl_str, seed, m, "none", "r2") not in completed_keys
                and ("finite_shots", lvl_str, seed, m, "raw", "r2") not in completed_keys
                and ("finite_shots", lvl_str, seed, m, "std", "r2") not in completed_keys
            ]
            if not needed_models:
                continue

            t0_level = time.time()
            # Deterministic RNG per (seed, level)
            rng_seed = int(100000 * seed + S)
            rng = np.random.default_rng(rng_seed)

            # Sample basis measurements for all 240 states
            # Counts via multinomial for all 240 states
            counts_x = np.array([rng.multinomial(S, probs_x[i]) for i in range(m)], dtype=float) / S
            counts_y = np.array([rng.multinomial(S, probs_y[i]) for i in range(m)], dtype=float) / S
            counts_z = np.array([rng.multinomial(S, probs_z[i]) for i in range(m)], dtype=float) / S

            # Extract observables
            exp_x = counts_x @ signs          # (240, 8)
            exp_xx_nn = counts_x @ signs_nn   # (240, 7)
            exp_yy_nn = counts_y @ signs_nn   # (240, 7)
            exp_z = counts_z @ signs          # (240, 8)
            exp_zz_nn = counts_z @ signs_nn   # (240, 7)
            exp_zz_all = counts_z @ signs_zz_all  # (240, 28)

            # Reconstruct feature sets
            # 1. PQK-1 features: [exp_x, exp_z] / sqrt(2)
            X_pqk1 = np.hstack([exp_x, exp_z]) / np.sqrt(2.0)  # (240, 16)

            # 2. PQK-2nn / E2 features: 35 dims
            # For each nn pair: [X_i, X_j, XX_ij, YY_ij, ZZ_ij]
            feats_2pt_list = []
            for i in range(n - 1):
                j = i + 1
                feats_2pt_list.extend([
                    exp_x[:, i], exp_x[:, j], exp_xx_nn[:, i], exp_yy_nn[:, i], exp_zz_nn[:, i]
                ])
            X_e2 = np.column_stack(feats_2pt_list)  # (240, 35)
            X_pqk2 = X_e2 / 2.0                     # (240, 35), dist2 / 4 matches 2-RDM Frobenius

            # 3. E features: 52 dims matching full_corr [bx, 0, bz] + [all ZZ]
            feats_e_list = []
            for i in range(n):
                feats_e_list.extend([exp_x[:, i], np.zeros(m), exp_z[:, i]])
            feats_e_list.extend([exp_zz_all[:, k] for k in range(exp_zz_all.shape[1])])
            X_e = np.column_stack(feats_e_list)    # (240, 52)

            # Standardized E
            scaler_e = StandardScaler()
            X_e_tr_std = scaler_e.fit_transform(X_e[:N_train])
            X_e_te_std = scaler_e.transform(X_e[N_train:])

            # Destructive swap-test Gram matrix
            K_hat, lam_min_full = destructive_swap_test_fidelity(K_pure_full, S, rng)
            K_hat_tr = K_hat[:N_train, :N_train]
            K_hat_te = K_hat[N_train:, :N_train]
            lam_min_tr = float(np.min(np.linalg.eigvalsh(K_hat_tr)))

            # Evaluate arms
            # Arm 1: PQK-1
            t_arm = time.time()
            r2_val, mae_val, params, cv_sc = evaluate_svr_rbf_fast(
                X_pqk1[:N_train], y_tr_z, tr_targets, X_pqk1[N_train:], te_targets,
                n, C_FACTORS_V2, y_mean, y_std, kf
            )
            for met, val in [("r2", r2_val), ("mae", mae_val)]:
                new_rows.append({
                    "experiment": "finite_shots", "noise_param": "shots", "noise_level": lvl_str,
                    "seed": seed, "n": n, "N_train": N_train, "model": "PQK-1", "variant": "none",
                    "metric": met, "value": val, "best_params": params, "inner_cv_score": cv_sc,
                    "lam_min": 0.0, "train_shots": 2 * N_train * S, "predict_shots": 2 * N_test * S,
                    "total_shots": 2 * m * S, "fit_seconds": time.time() - t_arm,
                })

            # Arm 2: PQK-2nn
            t_arm = time.time()
            r2_val, mae_val, params, cv_sc = evaluate_svr_rbf_fast(
                X_pqk2[:N_train], y_tr_z, tr_targets, X_pqk2[N_train:], te_targets,
                n, C_FACTORS_V2, y_mean, y_std, kf
            )
            for met, val in [("r2", r2_val), ("mae", mae_val)]:
                new_rows.append({
                    "experiment": "finite_shots", "noise_param": "shots", "noise_level": lvl_str,
                    "seed": seed, "n": n, "N_train": N_train, "model": "PQK-2nn", "variant": "none",
                    "metric": met, "value": val, "best_params": params, "inner_cv_score": cv_sc,
                    "lam_min": 0.0, "train_shots": 3 * N_train * S, "predict_shots": 3 * N_test * S,
                    "total_shots": 3 * m * S, "fit_seconds": time.time() - t_arm,
                })

            # Arm 3: FQ-raw
            t_arm = time.time()
            r2_val, mae_val, params, cv_sc = evaluate_svr_precomputed(
                K_hat_tr, y_tr_z, tr_targets, K_hat_te, te_targets,
                y_mean, y_std, kf, clip_psd=False
            )
            for met, val in [("r2", r2_val), ("mae", mae_val)]:
                new_rows.append({
                    "experiment": "finite_shots", "noise_param": "shots", "noise_level": lvl_str,
                    "seed": seed, "n": n, "N_train": N_train, "model": "FQ-raw", "variant": "none",
                    "metric": met, "value": val, "best_params": params, "inner_cv_score": cv_sc,
                    "lam_min": lam_min_tr, "train_shots": 780 * S, "predict_shots": 8000 * S,
                    "total_shots": 28680 * S, "fit_seconds": time.time() - t_arm,
                })

            # Arm 4: FQ-clipped
            t_arm = time.time()
            r2_val, mae_val, params, cv_sc = evaluate_svr_precomputed(
                K_hat_tr, y_tr_z, tr_targets, K_hat_te, te_targets,
                y_mean, y_std, kf, clip_psd=True
            )
            for met, val in [("r2", r2_val), ("mae", mae_val)]:
                new_rows.append({
                    "experiment": "finite_shots", "noise_param": "shots", "noise_level": lvl_str,
                    "seed": seed, "n": n, "N_train": N_train, "model": "FQ-clipped", "variant": "none",
                    "metric": met, "value": val, "best_params": params, "inner_cv_score": cv_sc,
                    "lam_min": lam_min_tr, "train_shots": 780 * S, "predict_shots": 8000 * S,
                    "total_shots": 28680 * S, "fit_seconds": time.time() - t_arm,
                })

            # Arm 5: E (raw)
            t_arm = time.time()
            r2_val, mae_val, params, cv_sc = evaluate_svr_rbf_fast(
                X_e[:N_train], y_tr_z, tr_targets, X_e[N_train:], te_targets,
                52, C_FACTORS_V2, y_mean, y_std, kf
            )
            for met, val in [("r2", r2_val), ("mae", mae_val)]:
                new_rows.append({
                    "experiment": "finite_shots", "noise_param": "shots", "noise_level": lvl_str,
                    "seed": seed, "n": n, "N_train": N_train, "model": "E", "variant": "raw",
                    "metric": met, "value": val, "best_params": params, "inner_cv_score": cv_sc,
                    "lam_min": 0.0, "train_shots": 3 * N_train * S, "predict_shots": 3 * N_test * S,
                    "total_shots": 3 * m * S, "fit_seconds": time.time() - t_arm,
                })

            # Arm 6: E (std)
            t_arm = time.time()
            r2_val, mae_val, params, cv_sc = evaluate_svr_rbf_fast(
                X_e_tr_std, y_tr_z, tr_targets, X_e_te_std, te_targets,
                52, C_FACTORS_STD_V2, y_mean, y_std, kf
            )
            for met, val in [("r2", r2_val), ("mae", mae_val)]:
                new_rows.append({
                    "experiment": "finite_shots", "noise_param": "shots", "noise_level": lvl_str,
                    "seed": seed, "n": n, "N_train": N_train, "model": "E", "variant": "std",
                    "metric": met, "value": val, "best_params": params, "inner_cv_score": cv_sc,
                    "lam_min": 0.0, "train_shots": 3 * N_train * S, "predict_shots": 3 * N_test * S,
                    "total_shots": 3 * m * S, "fit_seconds": time.time() - t_arm,
                })

            # Arm 7: E2 (raw)
            t_arm = time.time()
            r2_val, mae_val, params, cv_sc = evaluate_svr_rbf_fast(
                X_e2[:N_train], y_tr_z, tr_targets, X_e2[N_train:], te_targets,
                35, C_FACTORS_V2, y_mean, y_std, kf
            )
            for met, val in [("r2", r2_val), ("mae", mae_val)]:
                new_rows.append({
                    "experiment": "finite_shots", "noise_param": "shots", "noise_level": lvl_str,
                    "seed": seed, "n": n, "N_train": N_train, "model": "E2", "variant": "raw",
                    "metric": met, "value": val, "best_params": params, "inner_cv_score": cv_sc,
                    "lam_min": 0.0, "train_shots": 3 * N_train * S, "predict_shots": 3 * N_test * S,
                    "total_shots": 3 * m * S, "fit_seconds": time.time() - t_arm,
                })

            # Arm 8: F (std)
            t_arm = time.time()
            r2_val, mae_val, params, cv_sc = evaluate_ridge(
                X_e_tr_std, y_tr_z, tr_targets, X_e_te_std, te_targets,
                y_mean, y_std, kf
            )
            for met, val in [("r2", r2_val), ("mae", mae_val)]:
                new_rows.append({
                    "experiment": "finite_shots", "noise_param": "shots", "noise_level": lvl_str,
                    "seed": seed, "n": n, "N_train": N_train, "model": "F", "variant": "std",
                    "metric": met, "value": val, "best_params": params, "inner_cv_score": cv_sc,
                    "lam_min": 0.0, "train_shots": 3 * N_train * S, "predict_shots": 3 * N_test * S,
                    "total_shots": 3 * m * S, "fit_seconds": time.time() - t_arm,
                })

            print(f"  [Seed {seed:2d}] Finite shots S={S:5d} done in {time.time() - t0_level:.2f}s (lam_min={lam_min_tr:.4f})", flush=True)

        # =====================================================================
        # 3. EXPERIMENT B: DEPOLARIZING CHANNEL SWEEP
        # =====================================================================
        for p in depol_list:
            if p == 0.0:
                continue  # p=0.00 already added from reference baseline above

            lvl_str = f"{p:.2f}"
            needed_models = [
                m for m in ["PQK-1", "PQK-2nn", "FQ", "E", "E2", "F"]
                if ("depolarizing", lvl_str, seed, m, "none", "r2") not in completed_keys
                and ("depolarizing", lvl_str, seed, m, "raw", "r2") not in completed_keys
                and ("depolarizing", lvl_str, seed, m, "std", "r2") not in completed_keys
                and ("depolarizing", lvl_str, seed, m, "mixed_state_overlap", "r2") not in completed_keys
            ]
            if not needed_models:
                continue

            t0_level = time.time()

            # 1. Scale classical observables
            # 1-body Paulis scale by (1-p)
            scale_1 = 1.0 - p
            # 2-body Paulis scale by (1-p)^2
            scale_2 = (1.0 - p) ** 2

            # PQK-1 features: <X> scaled by (1-p)
            X_pqk1_depol = scale_1 * pure_x_all

            # PQK-2nn / E2 features:
            # 5 features per pair: [X_i, X_j, XX_ij, YY_ij, ZZ_ij]
            # scale: [scale_1, scale_1, scale_2, scale_2, scale_2]
            scale_e2 = np.tile([scale_1, scale_1, scale_2, scale_2, scale_2], n - 1)
            X_e2_depol = pure_e2_all * scale_e2
            X_pqk2_depol = X_e2_depol / 2.0

            # E features: full_corr format (52 dims)
            # 3 dims per site: [bx, by, bz] -> all 1-body, scale by scale_1
            # 28 dims for all ZZ -> all 2-body, scale by scale_2
            scale_e = np.concatenate([np.full(3 * n, scale_1), np.full(n * (n - 1) // 2, scale_2)])
            X_e_depol = pure_e_all * scale_e

            # Standardized E
            scaler_e_depol = StandardScaler()
            X_e_tr_depol_std = scaler_e_depol.fit_transform(X_e_depol[:N_train])
            X_e_te_depol_std = scaler_e_depol.transform(X_e_depol[N_train:])

            # FQ mixed-state normalized overlap
            K_depol_full = mixed_state_fidelity_gram(all_states, p=p, n=n)
            K_depol_tr = K_depol_full[:N_train, :N_train]
            K_depol_te = K_depol_full[N_train:, :N_train]
            lam_min_depol = float(np.min(np.linalg.eigvalsh(K_depol_tr)))

            # Evaluate arms
            # Arm 1: PQK-1
            t_arm = time.time()
            r2_val, mae_val, params, cv_sc = evaluate_svr_rbf_fast(
                X_pqk1_depol[:N_train], y_tr_z, tr_targets, X_pqk1_depol[N_train:], te_targets,
                2.0 * n, C_FACTORS_V2, y_mean, y_std, kf
            )
            for met, val in [("r2", r2_val), ("mae", mae_val)]:
                new_rows.append({
                    "experiment": "depolarizing", "noise_param": "p", "noise_level": lvl_str,
                    "seed": seed, "n": n, "N_train": N_train, "model": "PQK-1", "variant": "none",
                    "metric": met, "value": val, "best_params": params, "inner_cv_score": cv_sc,
                    "lam_min": 0.0, "train_shots": "inf", "predict_shots": "inf", "total_shots": "inf",
                    "fit_seconds": time.time() - t_arm,
                })

            # Arm 2: PQK-2nn
            t_arm = time.time()
            r2_val, mae_val, params, cv_sc = evaluate_svr_rbf_fast(
                X_pqk2_depol[:N_train], y_tr_z, tr_targets, X_pqk2_depol[N_train:], te_targets,
                n, C_FACTORS_V2, y_mean, y_std, kf
            )
            for met, val in [("r2", r2_val), ("mae", mae_val)]:
                new_rows.append({
                    "experiment": "depolarizing", "noise_param": "p", "noise_level": lvl_str,
                    "seed": seed, "n": n, "N_train": N_train, "model": "PQK-2nn", "variant": "none",
                    "metric": met, "value": val, "best_params": params, "inner_cv_score": cv_sc,
                    "lam_min": 0.0, "train_shots": "inf", "predict_shots": "inf", "total_shots": "inf",
                    "fit_seconds": time.time() - t_arm,
                })

            # Arm 3: FQ (mixed_state_overlap)
            t_arm = time.time()
            r2_val, mae_val, params, cv_sc = evaluate_svr_precomputed(
                K_depol_tr, y_tr_z, tr_targets, K_depol_te, te_targets,
                y_mean, y_std, kf, clip_psd=False
            )
            for met, val in [("r2", r2_val), ("mae", mae_val)]:
                new_rows.append({
                    "experiment": "depolarizing", "noise_param": "p", "noise_level": lvl_str,
                    "seed": seed, "n": n, "N_train": N_train, "model": "FQ", "variant": "mixed_state_overlap",
                    "metric": met, "value": val, "best_params": params, "inner_cv_score": cv_sc,
                    "lam_min": lam_min_depol, "train_shots": "inf", "predict_shots": "inf", "total_shots": "inf",
                    "fit_seconds": time.time() - t_arm,
                })

            # Arm 4: E (raw)
            t_arm = time.time()
            r2_val, mae_val, params, cv_sc = evaluate_svr_rbf_fast(
                X_e_depol[:N_train], y_tr_z, tr_targets, X_e_depol[N_train:], te_targets,
                52, C_FACTORS_V2, y_mean, y_std, kf
            )
            for met, val in [("r2", r2_val), ("mae", mae_val)]:
                new_rows.append({
                    "experiment": "depolarizing", "noise_param": "p", "noise_level": lvl_str,
                    "seed": seed, "n": n, "N_train": N_train, "model": "E", "variant": "raw",
                    "metric": met, "value": val, "best_params": params, "inner_cv_score": cv_sc,
                    "lam_min": 0.0, "train_shots": "inf", "predict_shots": "inf", "total_shots": "inf",
                    "fit_seconds": time.time() - t_arm,
                })

            # Arm 5: E (std)
            t_arm = time.time()
            r2_val, mae_val, params, cv_sc = evaluate_svr_rbf_fast(
                X_e_tr_depol_std, y_tr_z, tr_targets, X_e_te_depol_std, te_targets,
                52, C_FACTORS_STD_V2, y_mean, y_std, kf
            )
            for met, val in [("r2", r2_val), ("mae", mae_val)]:
                new_rows.append({
                    "experiment": "depolarizing", "noise_param": "p", "noise_level": lvl_str,
                    "seed": seed, "n": n, "N_train": N_train, "model": "E", "variant": "std",
                    "metric": met, "value": val, "best_params": params, "inner_cv_score": cv_sc,
                    "lam_min": 0.0, "train_shots": "inf", "predict_shots": "inf", "total_shots": "inf",
                    "fit_seconds": time.time() - t_arm,
                })

            # Arm 6: E2 (raw)
            t_arm = time.time()
            r2_val, mae_val, params, cv_sc = evaluate_svr_rbf_fast(
                X_e2_depol[:N_train], y_tr_z, tr_targets, X_e2_depol[N_train:], te_targets,
                35, C_FACTORS_V2, y_mean, y_std, kf
            )
            for met, val in [("r2", r2_val), ("mae", mae_val)]:
                new_rows.append({
                    "experiment": "depolarizing", "noise_param": "p", "noise_level": lvl_str,
                    "seed": seed, "n": n, "N_train": N_train, "model": "E2", "variant": "raw",
                    "metric": met, "value": val, "best_params": params, "inner_cv_score": cv_sc,
                    "lam_min": 0.0, "train_shots": "inf", "predict_shots": "inf", "total_shots": "inf",
                    "fit_seconds": time.time() - t_arm,
                })

            # Arm 7: F (std)
            t_arm = time.time()
            r2_val, mae_val, params, cv_sc = evaluate_ridge(
                X_e_tr_depol_std, y_tr_z, tr_targets, X_e_te_depol_std, te_targets,
                y_mean, y_std, kf
            )
            for met, val in [("r2", r2_val), ("mae", mae_val)]:
                new_rows.append({
                    "experiment": "depolarizing", "noise_param": "p", "noise_level": lvl_str,
                    "seed": seed, "n": n, "N_train": N_train, "model": "F", "variant": "std",
                    "metric": met, "value": val, "best_params": params, "inner_cv_score": cv_sc,
                    "lam_min": 0.0, "train_shots": "inf", "predict_shots": "inf", "total_shots": "inf",
                    "fit_seconds": time.time() - t_arm,
                })

            print(f"  [Seed {seed:2d}] Depolarizing p={p:.2f} done in {time.time() - t0_level:.2f}s", flush=True)

        # Flush rows for this seed to disk
        if new_rows:
            write_header = not os.path.exists(out_csv) or os.path.getsize(out_csv) == 0
            df_new = pd.DataFrame(new_rows, columns=fieldnames)
            df_new.to_csv(out_csv, mode="a", header=write_header, index=False)
            print(f"  [Seed {seed:2d}] Flushed {len(new_rows)} rows to {out_csv} (seed time: {time.time() - t_seed_start:.1f}s)", flush=True)
            new_rows = []


def launch_parallel_workers(seeds: list, quick: bool, out_csv: str, n_workers: int = 4):
    """Launch n_workers parallel subprocesses, wait, and merge results."""
    t_start = time.time()
    worker_csvs = [os.path.join("results", f"t5_noise_worker{w}.csv") for w in range(n_workers)]

    # Clean existing worker files
    for w_csv in worker_csvs:
        if os.path.exists(w_csv):
            try:
                os.remove(w_csv)
            except Exception:
                pass

    # Split seeds
    worker_seeds = [[] for _ in range(n_workers)]
    for idx, s in enumerate(seeds):
        worker_seeds[idx % n_workers].append(s)

    processes = []
    python_exe = sys.executable

    print(f"=== Spawning {n_workers} Parallel Workers for {len(seeds)} Seeds ===", flush=True)
    for w in range(n_workers):
        w_s_list = worker_seeds[w]
        if not w_s_list:
            continue
        seeds_str = ",".join(map(str, w_s_list))
        cmd = [
            python_exe, os.path.abspath(__file__),
            "--worker", str(w),
            "--seeds", seeds_str,
            "--out", worker_csvs[w],
        ]
        if quick:
            cmd.append("--quick")

        env = os.environ.copy()
        env["OMP_NUM_THREADS"] = "1"
        env["MKL_NUM_THREADS"] = "1"
        env["OPENBLAS_NUM_THREADS"] = "1"

        print(f"  Worker {w}: seeds {w_s_list}", flush=True)
        p = subprocess.Popen(cmd, env=env)
        processes.append((w, p, worker_csvs[w]))

    # Wait for completion
    for w, p, w_csv in processes:
        ret = p.wait()
        if ret != 0:
            raise RuntimeError(f"Worker {w} failed with exit code {ret}")

    print("\nAll workers finished successfully! Merging results...", flush=True)

    # Merge
    merged_dfs = []
    for w_csv in worker_csvs:
        if os.path.exists(w_csv) and os.path.getsize(w_csv) > 0:
            merged_dfs.append(pd.read_csv(w_csv))

    if merged_dfs:
        final_df = pd.concat(merged_dfs, ignore_index=True)
        # Sort for clarity
        final_df.sort_values(
            by=["experiment", "noise_level", "seed", "model", "variant", "metric"],
            inplace=True,
        )
        final_df.to_csv(out_csv, index=False)
        print(f"Merged {len(final_df)} rows into {out_csv} in {time.time() - t_start:.2f}s.", flush=True)

    # Remove worker CSVs after successful merge
    for w_csv in worker_csvs:
        if os.path.exists(w_csv):
            try:
                os.remove(w_csv)
            except Exception:
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phase 2b Noise Benchmark")
    parser.add_argument("--seeds", type=str, default=None, help="Seeds to evaluate.")
    parser.add_argument("--quick", action="store_true", help="Quick mode (3 seeds, subsets).")
    parser.add_argument("--worker", type=int, default=None, help="Worker ID if running in worker mode.")
    parser.add_argument("--workers", type=int, default=4, help="Number of parallel workers.")
    parser.add_argument("--out", type=str, default=None, help="Output CSV path.")
    parser.add_argument("--single-process", action="store_true", help="Run sequentially without subprocesses.")
    args = parser.parse_args()

    # Parse seeds: explicit --seeds takes priority over --quick
    if args.seeds is not None:
        if "-" in args.seeds:
            s_start, s_end = map(int, args.seeds.split("-"))
            seed_list = list(range(s_start, s_end + 1))
        else:
            seed_list = [int(s.strip()) for s in args.seeds.split(",") if s.strip()]
    elif args.quick:
        seed_list = [0, 1, 2]
    else:
        seed_list = list(SEEDS)

    target_out = args.out if args.out else os.path.join("results", "t5_noise.csv")

    if args.worker is not None or args.single_process:
        run_noise_benchmark(
            seeds=seed_list,
            quick=args.quick,
            out_csv=target_out,
            worker_id=args.worker,
        )
    else:
        launch_parallel_workers(
            seeds=seed_list,
            quick=args.quick,
            out_csv=target_out,
            n_workers=args.workers,
        )
