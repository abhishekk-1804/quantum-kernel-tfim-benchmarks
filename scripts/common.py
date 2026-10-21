"""
scripts/common.py
-----------------
Shared utilities for Phase 2a benchmarks:
- SEEDS and CLI argument parsing (--seeds, --quick, --out).
- Metadata writing (run_meta.json).
- Ensemble generation and nested train/test splitting (make_split).
- Model evaluation protocol (inner 3-fold CV tuning on train only, scoring on test).
"""

import os
import sys
import csv
import json
import time
import datetime
import subprocess
import argparse
from typing import Dict, List, Tuple, Any

import numpy as np
import scipy
import sklearn
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.svm import SVR, SVC
from sklearn.linear_model import Ridge, RidgeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, accuracy_score, balanced_accuracy_score
from sklearn.metrics.pairwise import rbf_kernel

# Ensure src/ is on sys.path
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC = os.path.join(_PROJECT_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from hamiltonians import (
    build_tfim,
    build_frustrated_2d,
    ground_state,
    expect_x,
    expect_zz,
    expect_zzzz,
    half_chain_entropy,
    structure_factor,
)
from kernels import (
    one_rdm,
    two_rdm,
    bloch_vector,
    fidelity_gram,
    pqk_gram,
    pqk_gram_2local,
    classical_features,
)

# 20 seeds standard
SEEDS = list(range(20))

# Hyperparameter search grids
C_GRID = [0.1, 1.0, 10.0, 100.0]
C_FACTORS = [0.1, 0.3, 1.0, 3.0, 10.0]
ALPHA_GRID = np.logspace(-4, 2, 7)


def get_parser(description: str = "") -> argparse.ArgumentParser:
    """Standard CLI argument parser for all benchmark scripts."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--seeds",
        type=str,
        default=None,
        help="Comma-separated seed list or range like '0-19'. Default: all 20 seeds.",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick smoke test mode: 3 seeds (0, 1, 2), smaller N / n.",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Custom output CSV path.",
    )
    return parser


def parse_seeds(args: argparse.Namespace) -> List[int]:
    """Parse seed list according to --quick or --seeds flag."""
    if args.quick:
        return [0, 1, 2]
    if args.seeds is not None:
        if "-" in args.seeds:
            start, end = map(int, args.seeds.split("-"))
            return list(range(start, end + 1))
        return [int(s.strip()) for s in args.seeds.split(",") if s.strip()]
    return list(SEEDS)


def write_run_meta(results_dir: str = "results") -> str:
    """Write environment and git metadata to results/run_meta.json."""
    os.makedirs(results_dir, exist_ok=True)
    git_hash = "unknown"
    try:
        git_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=_PROJECT_ROOT,
            stderr=subprocess.DEVNULL,
        ).decode("utf-8").strip()
    except Exception:
        pass

    meta = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_commit": git_hash,
        "python_version": sys.version,
        "packages": {
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "sklearn": sklearn.__version__,
        },
    }
    meta_path = os.path.join(results_dir, "run_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    return meta_path


# ── In-memory caches for generated ensembles ──────────────────────────────────
_DISORDERED_TFIM_CACHE: Dict[Tuple[int, int], Dict[str, Any]] = {}
_FRUSTRATED_2D_CACHE: Dict[Tuple[int, float], Dict[str, Any]] = {}


def _get_disordered_tfim_ensemble(n: int, seed: int) -> Dict[str, Any]:
    """
    Generate or retrieve 360 disordered TFIM states for (n, seed).
    160 training pool + 200 fixed test states.
    J_i ~ U[0.5, 1.5] (n-1 bonds), g_i ~ U[0.3, 2.0] (n sites).
    """
    key = (seed, n)
    if key in _DISORDERED_TFIM_CACHE:
        return _DISORDERED_TFIM_CACHE[key]

    rng = np.random.default_rng(seed)
    total_states = 360  # 160 max train + 200 test
    states = []
    entropies = []
    z0zn = []
    zzzz = []

    for _ in range(total_states):
        couplings = rng.uniform(0.5, 1.5, size=n - 1)
        fields = rng.uniform(0.3, 2.0, size=n)
        H = build_tfim(n, g=1.0, J=1.0, boundary="open", couplings=couplings, fields=fields)
        _, psi, _ = ground_state(H, n, sector="even")
        states.append(psi)
        entropies.append(half_chain_entropy(psi, n))
        z0zn.append(expect_zz(psi, n, 0, n - 1))
        zzzz.append(expect_zzzz(psi, n, 0, 1, n - 2, n - 1))

    ensemble = {
        "states": np.array(states, dtype=np.float64),
        "entropy": np.array(entropies, dtype=float),
        "z0zn": np.array(z0zn, dtype=float),
        "zzzz": np.array(zzzz, dtype=float),
    }
    _DISORDERED_TFIM_CACHE[key] = ensemble
    return ensemble


def _get_frustrated_2d_ensemble(seed: int, J2: float) -> Dict[str, Any]:
    """
    Generate or retrieve 248 frustrated 2D states for (seed, J2).
    48 training pool + 200 fixed test states.
    J1 = -1.0, J2 in {-0.25, -0.5, -0.75}, g ~ U[0.2, 3.0], rows=2, cols=4.
    """
    key = (seed, round(J2, 4))
    if key in _FRUSTRATED_2D_CACHE:
        return _FRUSTRATED_2D_CACHE[key]

    # Deterministic distinct stream per (seed, J2)
    j2_int = int(round(abs(J2) * 1000))
    rng = np.random.default_rng(seed * 10000 + j2_int)
    total_states = 248  # 48 max train + 200 test
    states = []
    entropies = []
    sq_argmaxes = []

    for _ in range(total_states):
        g = rng.uniform(0.2, 3.0)
        H, nn_bonds, _ = build_frustrated_2d(rows=2, cols=4, g=g, J1=-1.0, J2=J2)
        _, psi, _ = ground_state(H, 8, sector="even")
        states.append(psi)
        entropies.append(half_chain_entropy(psi, 8))
        Sq = structure_factor(psi, 2, 4)
        max_q = max(Sq, key=Sq.get)
        sq_argmaxes.append(f"{max_q[0]:.2f}_{max_q[1]:.2f}")

    ensemble = {
        "states": np.array(states, dtype=np.float64),
        "entropy": np.array(entropies, dtype=float),
        "sq_argmax": np.array(sq_argmaxes),
        "nn_bonds": nn_bonds,
    }
    _FRUSTRATED_2D_CACHE[key] = ensemble
    return ensemble


def make_split(task: str, n: int, N: int, seed: int, **kwargs) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, Dict[str, Any]]:
    """
    Returns (train_states, train_targets, test_states, test_targets, meta).
    - test_states is fixed per (task, seed) and contains exactly 200 states.
    - train_states contains the first N states from the fixed per-seed training pool.
    """
    t_lower = task.lower()
    if t_lower in ("t1", "t1_entropy", "t2", "t2_correlators", "t2a", "t2b"):
        ensemble = _get_disordered_tfim_ensemble(n=n, seed=seed)
        target_name = kwargs.get("target_name", "entropy")
        if target_name in ("entropy", "half_chain_entropy"):
            targets = ensemble["entropy"]
        elif target_name in ("z0zn", "z0_zn"):
            targets = ensemble["z0zn"]
        elif target_name in ("zzzz", "z0_z1_zn2_zn1"):
            targets = ensemble["zzzz"]
        else:
            raise ValueError(f"Unknown target: {target_name}")

        train_pool_size = 160
        assert N <= train_pool_size, f"N={N} exceeds training pool {train_pool_size}"
        train_states = ensemble["states"][:N]
        train_targets = targets[:N]
        test_states = ensemble["states"][train_pool_size : train_pool_size + 200]
        test_targets = targets[train_pool_size : train_pool_size + 200]
        meta = {"train_indices": list(range(N)), "test_indices": list(range(train_pool_size, train_pool_size + 200))}
        return train_states, train_targets, test_states, test_targets, meta

    elif t_lower in ("t4", "t4_frustrated", "t4a", "t4b"):
        J2 = kwargs.get("J2", -0.5)
        ensemble = _get_frustrated_2d_ensemble(seed=seed, J2=J2)
        target_name = kwargs.get("target_name", "entropy")
        if target_name in ("sq_argmax", "classification"):
            targets = ensemble["sq_argmax"]
        elif target_name in ("entropy", "half_cut_entropy", "regression"):
            targets = ensemble["entropy"]
        else:
            raise ValueError(f"Unknown T4 target: {target_name}")

        train_pool_size = 48
        assert N <= train_pool_size, f"N={N} exceeds training pool {train_pool_size}"
        train_states = ensemble["states"][:N]
        train_targets = targets[:N]
        test_states = ensemble["states"][train_pool_size : train_pool_size + 200]
        test_targets = targets[train_pool_size : train_pool_size + 200]
        meta = {
            "train_indices": list(range(N)),
            "test_indices": list(range(train_pool_size, train_pool_size + 200)),
            "nn_bonds": ensemble["nn_bonds"],
        }
        return train_states, train_targets, test_states, test_targets, meta

    else:
        raise ValueError(f"Unknown task: {task}")


# ── Model Evaluation Suite ────────────────────────────────────────────────────

def evaluate_regression_models(
    task: str,
    target: str,
    tag: str,
    n: int,
    N_train: int,
    seed: int,
    train_states: np.ndarray,
    train_targets: np.ndarray,
    test_states: np.ndarray,
    test_targets: np.ndarray,
    pairs: Any = None,
) -> List[Dict[str, Any]]:
    """
    Fit and evaluate all regression model arms per protocol:
    - Inner 3-fold CV on train set only (z-scoring targets within fold).
    - Refit on all N training states, score on 200 test states.
    - Record R2 and MAE in original physical units.
    """
    results = []

    # Target statistics from TRAIN only
    y_mean = float(np.mean(train_targets))
    y_std = float(np.std(train_targets))
    if y_std < 1e-12:
        y_std = 1.0
    y_train_z = (train_targets - y_mean) / y_std

    # Baseline: predict train mean
    y_pred_base = np.full(len(test_targets), y_mean)
    r2_base = float(r2_score(test_targets, y_pred_base))
    mae_base = float(mean_absolute_error(test_targets, y_pred_base))
    for metric, val in [("r2", r2_base), ("mae", mae_base)]:
        results.append({
            "task": task, "target": target, "tag": tag, "n": n, "N_train": N_train,
            "seed": seed, "model": "baseline_mean", "variant": "none",
            "metric": metric, "value": val, "best_params": "{}", "fit_seconds": 0.0,
        })

    kf = KFold(n_splits=3, shuffle=True, random_state=42)

    # Pre-extract features for all train + test states
    # 1. <X> features (dim n)
    X_x_train = np.array([expect_x(psi, n) for psi in train_states])
    X_x_test = np.array([expect_x(psi, n) for psi in test_states])

    # 2. E features [<X_i>, all <Z_i Z_j> i<j] (dim n + n*(n-1)/2)
    def extract_e_features(psis):
        feats = []
        for psi in psis:
            feats.append(classical_features(psi, n, mode="full_corr"))
        return np.array(feats)

    X_e_train = extract_e_features(train_states)
    X_e_test = extract_e_features(test_states)
    d_e = X_e_train.shape[1]

    # Standardized E features
    scaler = StandardScaler()
    X_e_train_std = scaler.fit_transform(X_e_train)
    X_e_test_std = scaler.transform(X_e_test)

    # 3. E2 features (2pt_pauli_nn)
    def extract_e2_features(psis):
        feats = []
        for psi in psis:
            feats.append(classical_features(psi, n, mode="2pt_pauli_nn", pairs=pairs))
        return np.array(feats)

    X_e2_train = extract_e2_features(train_states)
    X_e2_test = extract_e2_features(test_states)
    d_e2 = X_e2_train.shape[1]

    # 4. FQ Gram matrix
    # K_fq = (Psi @ Psi.T)^2
    K_fq_train = (train_states @ train_states.T) ** 2
    K_fq_test = (test_states @ train_states.T) ** 2

    # Helper: tune SVR with precomputed kernel or RBF
    def tune_and_score_rbf(X_tr, X_te, gamma_grid, model_name, variant, arm_tag):
        t0 = time.time()
        best_cv = -np.inf
        best_C, best_c = C_GRID[0], C_FACTORS[0]

        for C in C_GRID:
            for c_val in C_FACTORS:
                gamma = c_val / gamma_grid
                fold_scores = []
                for tr_idx, val_idx in kf.split(X_tr):
                    # Fold z-score
                    f_y_tr = train_targets[tr_idx]
                    f_m, f_s = np.mean(f_y_tr), np.std(f_y_tr)
                    if f_s < 1e-12: f_s = 1.0
                    f_y_tr_z = (f_y_tr - f_m) / f_s

                    clf = SVR(kernel="rbf", C=C, gamma=gamma, epsilon=0.1)
                    clf.fit(X_tr[tr_idx], f_y_tr_z)
                    pred_z = clf.predict(X_tr[val_idx])
                    pred = pred_z * f_s + f_m
                    fold_scores.append(r2_score(train_targets[val_idx], pred))
                mean_r2 = float(np.mean(fold_scores))
                if mean_r2 > best_cv:
                    best_cv = mean_r2
                    best_C, best_c = C, c_val

        best_gamma = best_c / gamma_grid
        clf_final = SVR(kernel="rbf", C=best_C, gamma=best_gamma, epsilon=0.1)
        clf_final.fit(X_tr, y_train_z)
        pred_z = clf_final.predict(X_te)
        pred = pred_z * y_std + y_mean
        fit_sec = time.time() - t0

        r2 = float(r2_score(test_targets, pred))
        mae = float(mean_absolute_error(test_targets, pred))
        b_params = json.dumps({"C": best_C, "c": best_c, "gamma": float(best_gamma)})

        for m_name, val in [("r2", r2), ("mae", mae)]:
            results.append({
                "task": task, "target": target, "tag": arm_tag, "n": n, "N_train": N_train,
                "seed": seed, "model": model_name, "variant": variant,
                "metric": m_name, "value": val, "best_params": b_params, "fit_seconds": fit_sec,
            })

    # Arm 1: PQK-1 (== RBF on <X>)
    # By proven identity: K^PQ1(gamma=c/n) == RBF(X, gamma'=c/(2n))
    # We tune and run ONCE as requested
    tune_and_score_rbf(
        X_x_train, X_x_test, gamma_grid=2.0 * n,
        model_name="PQK-1 (== RBF on <X>)", variant="none", arm_tag=tag
    )

    # Arm 2: PQK-2nn
    # By proven identity: K^PQ2(gamma=c/n) == RBF(2pt_pauli_nn, gamma'=c/(4n))
    tune_and_score_rbf(
        X_e2_train, X_e2_test, gamma_grid=4.0 * n,
        model_name="PQK-2nn", variant="none", arm_tag=tag
    )

    # Arm 3: FQ (tune C only)
    t0 = time.time()
    best_cv_fq = -np.inf
    best_C_fq = C_GRID[0]
    for C in C_GRID:
        fold_scores = []
        for tr_idx, val_idx in kf.split(train_states):
            f_y_tr = train_targets[tr_idx]
            f_m, f_s = np.mean(f_y_tr), np.std(f_y_tr)
            if f_s < 1e-12: f_s = 1.0
            f_y_tr_z = (f_y_tr - f_m) / f_s

            K_fold_tr = K_fq_train[np.ix_(tr_idx, tr_idx)]
            K_fold_val = K_fq_train[np.ix_(val_idx, tr_idx)]

            clf = SVR(kernel="precomputed", C=C, epsilon=0.1)
            clf.fit(K_fold_tr, f_y_tr_z)
            pred_z = clf.predict(K_fold_val)
            pred = pred_z * f_s + f_m
            fold_scores.append(r2_score(train_targets[val_idx], pred))
        mean_r2 = float(np.mean(fold_scores))
        if mean_r2 > best_cv_fq:
            best_cv_fq = mean_r2
            best_C_fq = C

    clf_fq = SVR(kernel="precomputed", C=best_C_fq, epsilon=0.1)
    clf_fq.fit(K_fq_train, y_train_z)
    pred_z = clf_fq.predict(K_fq_test)
    pred = pred_z * y_std + y_mean
    fit_sec_fq = time.time() - t0

    r2_fq = float(r2_score(test_targets, pred))
    mae_fq = float(mean_absolute_error(test_targets, pred))
    b_params_fq = json.dumps({"C": best_C_fq})
    for m_name, val in [("r2", r2_fq), ("mae", mae_fq)]:
        results.append({
            "task": task, "target": target, "tag": tag, "n": n, "N_train": N_train,
            "seed": seed, "model": "FQ", "variant": "none",
            "metric": m_name, "value": val, "best_params": b_params_fq, "fit_seconds": fit_sec_fq,
        })

    # Arm 4: E (raw) - gamma = c / d_e
    tune_and_score_rbf(
        X_e_train, X_e_test, gamma_grid=d_e,
        model_name="E", variant="raw", arm_tag=tag
    )

    # Arm 5: E (std) - gamma = c / d_e
    tune_and_score_rbf(
        X_e_train_std, X_e_test_std, gamma_grid=d_e,
        model_name="E", variant="std", arm_tag=tag
    )

    # Arm 6: F (Ridge on standardized E features)
    t0 = time.time()
    best_cv_ridge = -np.inf
    best_alpha = ALPHA_GRID[0]
    for alpha in ALPHA_GRID:
        fold_scores = []
        for tr_idx, val_idx in kf.split(X_e_train_std):
            f_y_tr = train_targets[tr_idx]
            f_m, f_s = np.mean(f_y_tr), np.std(f_y_tr)
            if f_s < 1e-12: f_s = 1.0
            f_y_tr_z = (f_y_tr - f_m) / f_s

            clf = Ridge(alpha=alpha)
            clf.fit(X_e_train_std[tr_idx], f_y_tr_z)
            pred_z = clf.predict(X_e_train_std[val_idx])
            pred = pred_z * f_s + f_m
            fold_scores.append(r2_score(train_targets[val_idx], pred))
        mean_r2 = float(np.mean(fold_scores))
        if mean_r2 > best_cv_ridge:
            best_cv_ridge = mean_r2
            best_alpha = alpha

    clf_ridge = Ridge(alpha=best_alpha)
    clf_ridge.fit(X_e_train_std, y_train_z)
    pred_z = clf_ridge.predict(X_e_test_std)
    pred = pred_z * y_std + y_mean
    fit_sec_ridge = time.time() - t0

    r2_ridge = float(r2_score(test_targets, pred))
    mae_ridge = float(mean_absolute_error(test_targets, pred))
    b_params_ridge = json.dumps({"alpha": float(best_alpha)})
    for m_name, val in [("r2", r2_ridge), ("mae", mae_ridge)]:
        results.append({
            "task": task, "target": target, "tag": tag, "n": n, "N_train": N_train,
            "seed": seed, "model": "F", "variant": "std",
            "metric": m_name, "value": val, "best_params": b_params_ridge, "fit_seconds": fit_sec_ridge,
        })

    # Arm 7: E2 (RBF on 2pt_pauli_nn, gamma = c/d_e2, tag "sanity")
    tune_and_score_rbf(
        X_e2_train, X_e2_test, gamma_grid=d_e2,
        model_name="E2", variant="raw", arm_tag="sanity"
    )

    # Arm 8: E_X (RBF on <X_i> only, raw, gamma = c/n, tag "sanity")
    tune_and_score_rbf(
        X_x_train, X_x_test, gamma_grid=float(n),
        model_name="E_X", variant="raw", arm_tag="sanity"
    )

    return results


def write_csv_rows(csv_path: str, rows: List[Dict[str, Any]]):
    """Append rows to CSV file in a thread/crash-safe manner, writing header if new."""
    os.makedirs(os.path.dirname(os.path.abspath(csv_path)), exist_ok=True)
    write_header = not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0

    fieldnames = [
        "task", "target", "tag", "n", "N_train", "seed",
        "model", "variant", "metric", "value", "best_params", "fit_seconds"
    ]
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        for row in rows:
            clean_row = {k: row.get(k, "") for k in fieldnames}
            writer.writerow(clean_row)
        f.flush()
