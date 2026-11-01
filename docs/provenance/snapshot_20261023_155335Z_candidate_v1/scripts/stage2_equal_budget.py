"""
scripts/stage2_equal_budget.py
------------------------------
Stage 2: Equal-Total-Budget Experiment Execution & Crossover Analysis.
Statistical classification: CONFIRMATORY (Stage 2 Frozen Protocol).

Setup:
  Task 1: Disordered 1D TFIM (n=8, N_train=40, N_test=200, 20 seeds: 0..19).
  Total measurement budgets:
    B_tot in {1e4, 3e4, 1e5, 3e5, 1e6, 3e6, 1e7}

Budget Accounting:
  - Feature Arms (Linear scaling, m = 240 states):
    * 3-basis arms (PQK-1 3basis, PQK-2nn, E2 raw_4n_grid):
      3 * m = 720 settings -> S_feat = floor(B_tot / 720).
    * 1-basis arm (PQK-1 x_only):
      1 * m = 240 settings -> S_xonly = floor(B_tot / 240).
  - Fidelity Quantum Kernel (FQ, Quadratic scaling):
    * Pairwise swap-test pairs:
      N_pairs = binom(40, 2) + 40 * 200 = 780 + 8,000 = 8,780 pairs.
      S_swap = floor(B_tot / 8,780).
    * Feasibility threshold: S_swap >= 10. If S_swap < 10 (at B_tot in {1e4, 3e4}),
      FQ is marked infeasible with S_swap = 0, R2 = NaN, MAE = NaN.

Models and Variants:
  1. PQK-1 (variant: 3basis)
  2. PQK-1 (variant: x_only)
  3. PQK-2nn (variant: none)
  4. E2 (variant: raw_4n_grid)
  5. FQ (variant: train_only) [Primary deployable FQ]
  6. FQ (variant: none) [Raw baseline]
  7. FQ (variant: inductive) [Exploratory out-of-sample repair]

Output:
  results/stage2/t1_equal_budget.csv
"""

import os
import sys
import time
import json
import argparse
from typing import Dict, List, Any, Tuple, Optional, Union

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.model_selection import KFold
from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_absolute_error

# Add src and scripts to sys.path
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SCRIPTS = os.path.join(_PROJECT_ROOT, "scripts")
_SRC = os.path.join(_PROJECT_ROOT, "src")
for p in [_SRC, _SCRIPTS]:
    if p not in sys.path:
        sys.path.insert(0, p)

from common import (
    C_GRID_V2,
    C_FACTORS_V2,
    EPSILON_GRID_V3,
    make_split,
)
from noise import (
    get_basis_rotation_matrix,
    destructive_swap_test_fidelity,
    fidelity_clip_psd,
)
from ablation_r3_repairs import (
    repair_none,
    repair_train_only,
    repair_inductive,
)

DEFAULT_OUT_CSV = os.path.join(_PROJECT_ROOT, "results", "stage2", "t1_equal_budget.csv")
BUDGETS_ALL = [10000, 30000, 100000, 300000, 1000000, 3000000, 10000000]

# Precomputed rotation unitaries at n=8
_UX_8 = get_basis_rotation_matrix("X", 8)
_UY_8 = get_basis_rotation_matrix("Y", 8)

# Precomputed bitstring indices and signs for n=8
_DIM = 256
_K_INDICES = np.arange(_DIM)
_BITSTRINGS = ((_K_INDICES[:, None] >> np.arange(8 - 1, -1, -1)) & 1)
_SIGNS = 1.0 - 2.0 * _BITSTRINGS  # (256, 8)
_SIGNS_NN = np.column_stack([_SIGNS[:, i] * _SIGNS[:, i + 1] for i in range(7)])  # (256, 7)


def calculate_shot_allocations(B_tot: int) -> Tuple[int, int, int, bool]:
    """
    Compute shot allocations across architectures under total budget B_tot.

    Parameters
    ----------
    B_tot : int
        Total measurement budget.

    Returns
    -------
    S_feat : int
        Shots per setting for 3-basis feature arms (720 settings).
    S_xonly : int
        Shots per setting for 1-basis feature arm (240 settings).
    S_swap : int
        Shots per pair for FQ (8,780 pairs). If infeasible (< 10), returns 0.
    is_feasible_fq : bool
        True if S_swap >= 10, False otherwise.
    """
    S_feat = int(B_tot // 720)
    S_xonly = int(B_tot // 240)
    raw_swap = int(B_tot // 8780)
    is_feasible_fq = bool(raw_swap >= 10)
    S_swap = raw_swap if is_feasible_fq else 0
    return S_feat, S_xonly, S_swap, is_feasible_fq


def evaluate_svr_rbf_fast(
    X_tr: np.ndarray,
    y_tr_z: np.ndarray,
    y_tr_orig: np.ndarray,
    X_te: np.ndarray,
    y_te: np.ndarray,
    gamma_denom: float,
    y_mean: float,
    y_std: float,
    kf: KFold,
) -> Tuple[float, float, str, float]:
    """
    Fast inner 3-fold CV tuning for SVR with precomputed distance matrices.
    """
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
    best_C, best_c, best_eps = C_GRID_V2[0], C_FACTORS_V2[0], EPSILON_GRID_V3[0]

    for c_val in C_FACTORS_V2:
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
                    svr = SVR(kernel="precomputed", C=float(C_val), epsilon=float(eps_val))
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

    svr_final = SVR(kernel="precomputed", C=float(best_C), epsilon=float(best_eps))
    svr_final.fit(K_full_tr, y_tr_z)
    pred_te_z = svr_final.predict(K_full_te)
    pred_te = pred_te_z * y_std + y_mean

    test_r2 = float(r2_score(y_te, pred_te))
    test_mae = float(mean_absolute_error(y_te, pred_te))
    params_str = json.dumps({"C": float(best_C), "c": float(best_c), "epsilon": float(best_eps)})
    return test_r2, test_mae, params_str, float(best_cv)


def evaluate_svr_fq_arm(
    K_raw_tr: np.ndarray,
    K_raw_te: np.ndarray,
    tr_targets: np.ndarray,
    te_targets: np.ndarray,
    y_mean: float,
    y_std: float,
    kf: KFold,
    repair_mode: str,
) -> Tuple[float, float, str, float]:
    """
    Inner 3-fold CV tuning and final evaluation for FQ Gram matrices.
    Applies the specified repair mode to inner-fold training blocks.
    """
    y_tr_z = (tr_targets - y_mean) / y_std

    folds_data = []
    for tr_idx, val_idx in kf.split(K_raw_tr):
        f_y_tr = tr_targets[tr_idx]
        f_m, f_s = float(np.mean(f_y_tr)), float(np.std(f_y_tr))
        if f_s < 1e-12:
            f_s = 1.0
        f_y_tr_z = (f_y_tr - f_m) / f_s
        f_y_val = tr_targets[val_idx]

        K_f_tr = K_raw_tr[np.ix_(tr_idx, tr_idx)]
        K_f_val = K_raw_tr[np.ix_(val_idx, tr_idx)]

        if repair_mode == "none":
            K_fit_fold, K_pred_fold = repair_none(K_f_tr, K_f_val)
        elif repair_mode == "train_only":
            K_fit_fold, K_pred_fold = repair_train_only(K_f_tr, K_f_val)
        elif repair_mode == "inductive":
            K_fit_fold, K_pred_fold = repair_inductive(K_f_tr, K_f_val, tol=1e-10)
        else:
            raise ValueError(f"Unknown FQ repair mode: {repair_mode}")

        folds_data.append((K_fit_fold, K_pred_fold, f_y_tr_z, f_y_val, f_m, f_s))

    best_cv = -np.inf
    best_C, best_eps = C_GRID_V2[0], EPSILON_GRID_V3[0]

    for C_val in C_GRID_V2:
        for eps_val in EPSILON_GRID_V3:
            scores = []
            for K_fit_fold, K_pred_fold, f_y_tr_z, f_y_val, f_m, f_s in folds_data:
                svr = SVR(kernel="precomputed", C=float(C_val), epsilon=float(eps_val))
                svr.fit(K_fit_fold, f_y_tr_z)
                pred_z = svr.predict(K_pred_fold)
                pred_orig = pred_z * f_s + f_m
                scores.append(r2_score(f_y_val, pred_orig))
            mean_cv = float(np.mean(scores))
            if mean_cv > best_cv:
                best_cv = mean_cv
                best_C, best_eps = C_val, eps_val

    # Final fit on full training block and prediction on test block
    if repair_mode == "none":
        K_fit_final, K_pred_final = repair_none(K_raw_tr, K_raw_te)
    elif repair_mode == "train_only":
        K_fit_final, K_pred_final = repair_train_only(K_raw_tr, K_raw_te)
    elif repair_mode == "inductive":
        K_fit_final, K_pred_final = repair_inductive(K_raw_tr, K_raw_te, tol=1e-10)
    else:
        raise ValueError(f"Unknown FQ repair mode: {repair_mode}")

    svr_final = SVR(kernel="precomputed", C=float(best_C), epsilon=float(best_eps))
    svr_final.fit(K_fit_final, y_tr_z)
    pred_te_z = svr_final.predict(K_pred_final)
    pred_te = pred_te_z * y_std + y_mean

    test_r2 = float(r2_score(te_targets, pred_te))
    test_mae = float(mean_absolute_error(te_targets, pred_te))
    params_str = json.dumps({"C": float(best_C), "epsilon": float(best_eps)})
    return test_r2, test_mae, params_str, float(best_cv)


def _unpack_states_and_targets(
    states: Union[np.ndarray, Tuple[np.ndarray, np.ndarray]],
    y: Union[np.ndarray, Tuple[np.ndarray, np.ndarray]],
    N_train: int = 40,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Helper to flexibly handle either split pairs or combined arrays."""
    if isinstance(states, tuple):
        train_states, test_states = states
        tr_targets, te_targets = y
    else:
        train_states = states[:N_train]
        test_states = states[N_train:]
        tr_targets = y[:N_train]
        te_targets = y[N_train:]
    return train_states, tr_targets, test_states, te_targets


def evaluate_feature_arms(
    states: Union[np.ndarray, Tuple[np.ndarray, np.ndarray]],
    y: Union[np.ndarray, Tuple[np.ndarray, np.ndarray]],
    B_tot: int,
    seed: int,
    rng: np.random.Generator,
    N_train: int = 40,
) -> List[Dict[str, Any]]:
    """
    Evaluates all feature-based arms under total budget B_tot:
      1. PQK-1 (variant: 3basis)
      2. PQK-1 (variant: x_only)
      3. PQK-2nn (variant: none)
      4. E2 (variant: raw_4n_grid)
    """
    train_states, tr_targets, test_states, te_targets = _unpack_states_and_targets(states, y, N_train)
    all_states = np.vstack([train_states, test_states])
    m = all_states.shape[0]  # 240
    n = 8

    y_mean = float(np.mean(tr_targets))
    y_std = float(np.std(tr_targets))
    if y_std < 1e-12:
        y_std = 1.0
    y_tr_z = (tr_targets - y_mean) / y_std

    kf = KFold(n_splits=3, shuffle=True, random_state=42)
    S_feat, S_xonly, _, _ = calculate_shot_allocations(B_tot)

    # State basis probabilities
    all_psi_x = all_states @ _UX_8.T
    all_psi_y = all_states @ _UY_8.T
    probs_x = np.abs(all_psi_x) ** 2
    probs_y = np.abs(all_psi_y) ** 2
    probs_z = np.abs(all_states) ** 2

    # 1. 3-basis measurements at S_feat shots per setting
    counts_x = np.array([rng.multinomial(S_feat, probs_x[i]) for i in range(m)], dtype=float) / S_feat
    counts_y = np.array([rng.multinomial(S_feat, probs_y[i]) for i in range(m)], dtype=float) / S_feat
    counts_z = np.array([rng.multinomial(S_feat, probs_z[i]) for i in range(m)], dtype=float) / S_feat

    exp_x = counts_x @ _SIGNS          # (240, 8)
    exp_xx_nn = counts_x @ _SIGNS_NN   # (240, 7)
    exp_yy_nn = counts_y @ _SIGNS_NN   # (240, 7)
    exp_z = counts_z @ _SIGNS          # (240, 8)
    exp_zz_nn = counts_z @ _SIGNS_NN   # (240, 7)

    # 1a. PQK-1 (3basis): [exp_x, exp_z] / sqrt(2.0), gamma_denom = n = 8
    X_pqk1_3b = np.hstack([exp_x, exp_z]) / np.sqrt(2.0)
    r2_p1_3b, mae_p1_3b, params_p1_3b, cv_p1_3b = evaluate_svr_rbf_fast(
        X_pqk1_3b[:N_train], y_tr_z, tr_targets, X_pqk1_3b[N_train:], te_targets,
        float(n), y_mean, y_std, kf
    )

    # 1b. Two-body features: 35 dims
    feats_2pt_list = []
    for i in range(n - 1):
        j = i + 1
        feats_2pt_list.extend([
            exp_x[:, i], exp_x[:, j], exp_xx_nn[:, i], exp_yy_nn[:, i], exp_zz_nn[:, i]
        ])
    X_e2 = np.column_stack(feats_2pt_list)  # (240, 35)

    # PQK-2nn: X_e2 / 2.0, gamma_denom = n = 8
    X_pqk2 = X_e2 / 2.0
    r2_p2, mae_p2, params_p2, cv_p2 = evaluate_svr_rbf_fast(
        X_pqk2[:N_train], y_tr_z, tr_targets, X_pqk2[N_train:], te_targets,
        float(n), y_mean, y_std, kf
    )

    # E2 (raw_4n_grid): X_e2, gamma_denom = 4 * n = 32
    r2_e2, mae_e2, params_e2, cv_e2 = evaluate_svr_rbf_fast(
        X_e2[:N_train], y_tr_z, tr_targets, X_e2[N_train:], te_targets,
        float(4 * n), y_mean, y_std, kf
    )

    # 2. 1-basis measurement (X-only) at S_xonly shots per setting
    counts_x_only = np.array([rng.multinomial(S_xonly, probs_x[i]) for i in range(m)], dtype=float) / S_xonly
    exp_x_only = counts_x_only @ _SIGNS  # (240, 8)
    # PQK-1 (x_only): exp_x_only, gamma_denom = 2 * n = 16
    r2_p1_x, mae_p1_x, params_p1_x, cv_p1_x = evaluate_svr_rbf_fast(
        exp_x_only[:N_train], y_tr_z, tr_targets, exp_x_only[N_train:], te_targets,
        float(2 * n), y_mean, y_std, kf
    )

    return [
        {
            "seed": seed, "B_tot": B_tot, "model": "PQK-1", "variant": "3basis",
            "S_per_setting": S_feat, "test_r2": r2_p1_3b, "test_mae": mae_p1_3b,
            "best_params": params_p1_3b, "inner_cv_score": cv_p1_3b, "is_feasible": True,
        },
        {
            "seed": seed, "B_tot": B_tot, "model": "PQK-1", "variant": "x_only",
            "S_per_setting": S_xonly, "test_r2": r2_p1_x, "test_mae": mae_p1_x,
            "best_params": params_p1_x, "inner_cv_score": cv_p1_x, "is_feasible": True,
        },
        {
            "seed": seed, "B_tot": B_tot, "model": "PQK-2nn", "variant": "none",
            "S_per_setting": S_feat, "test_r2": r2_p2, "test_mae": mae_p2,
            "best_params": params_p2, "inner_cv_score": cv_p2, "is_feasible": True,
        },
        {
            "seed": seed, "B_tot": B_tot, "model": "E2", "variant": "raw_4n_grid",
            "S_per_setting": S_feat, "test_r2": r2_e2, "test_mae": mae_e2,
            "best_params": params_e2, "inner_cv_score": cv_e2, "is_feasible": True,
        },
    ]


def evaluate_fq_arms(
    states: Union[np.ndarray, Tuple[np.ndarray, np.ndarray]],
    y: Union[np.ndarray, Tuple[np.ndarray, np.ndarray]],
    B_tot: int,
    seed: int,
    rng: np.random.Generator,
    N_train: int = 40,
) -> List[Dict[str, Any]]:
    """
    Evaluates all FQ arms under total budget B_tot:
      1. FQ (variant: train_only) [Primary deployable FQ]
      2. FQ (variant: none) [Raw baseline]
      3. FQ (variant: inductive) [Exploratory out-of-sample repair]
    If S_swap < 10 (B_tot in {1e4, 3e4}), logs is_feasible=False and R2=NaN.
    """
    train_states, tr_targets, test_states, te_targets = _unpack_states_and_targets(states, y, N_train)
    all_states = np.vstack([train_states, test_states])

    _, _, S_swap, is_feasible_fq = calculate_shot_allocations(B_tot)

    if not is_feasible_fq:
        # FQ is infeasible at this budget tier
        rows = []
        for var in ["train_only", "none", "inductive"]:
            rows.append({
                "seed": seed, "B_tot": B_tot, "model": "FQ", "variant": var,
                "S_per_setting": 0, "test_r2": np.nan, "test_mae": np.nan,
                "best_params": json.dumps({"status": "infeasible"}),
                "inner_cv_score": np.nan, "is_feasible": False,
            })
        return rows

    # Feasible FQ: compute noisy destructive swap-test Gram matrix
    K_pure_full = (all_states @ all_states.T) ** 2
    K_hat, _ = destructive_swap_test_fidelity(K_pure_full, S_swap, rng)
    K_hat_tr = K_hat[:N_train, :N_train]
    K_hat_te = K_hat[N_train:, :N_train]

    y_mean = float(np.mean(tr_targets))
    y_std = float(np.std(tr_targets))
    if y_std < 1e-12:
        y_std = 1.0
    kf = KFold(n_splits=3, shuffle=True, random_state=42)

    # 1. train_only (primary deployable)
    r2_to, mae_to, params_to, cv_to = evaluate_svr_fq_arm(
        K_hat_tr, K_hat_te, tr_targets, te_targets, y_mean, y_std, kf, repair_mode="train_only"
    )

    # 2. none (raw baseline)
    r2_no, mae_no, params_no, cv_no = evaluate_svr_fq_arm(
        K_hat_tr, K_hat_te, tr_targets, te_targets, y_mean, y_std, kf, repair_mode="none"
    )

    # 3. inductive (exploratory out-of-sample repair)
    r2_ind, mae_ind, params_ind, cv_ind = evaluate_svr_fq_arm(
        K_hat_tr, K_hat_te, tr_targets, te_targets, y_mean, y_std, kf, repair_mode="inductive"
    )

    return [
        {
            "seed": seed, "B_tot": B_tot, "model": "FQ", "variant": "train_only",
            "S_per_setting": S_swap, "test_r2": r2_to, "test_mae": mae_to,
            "best_params": params_to, "inner_cv_score": cv_to, "is_feasible": True,
        },
        {
            "seed": seed, "B_tot": B_tot, "model": "FQ", "variant": "none",
            "S_per_setting": S_swap, "test_r2": r2_no, "test_mae": mae_no,
            "best_params": params_no, "inner_cv_score": cv_no, "is_feasible": True,
        },
        {
            "seed": seed, "B_tot": B_tot, "model": "FQ", "variant": "inductive",
            "S_per_setting": S_swap, "test_r2": r2_ind, "test_mae": mae_ind,
            "best_params": params_ind, "inner_cv_score": cv_ind, "is_feasible": True,
        },
    ]


def get_completed_keys(csv_path: str) -> set:
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        return set()
    try:
        df = pd.read_csv(csv_path)
        return set(zip(df["seed"], df["B_tot"], df["model"], df["variant"]))
    except Exception:
        return set()


def write_rows(csv_path: str, rows: List[Dict[str, Any]]):
    os.makedirs(os.path.dirname(os.path.abspath(csv_path)), exist_ok=True)
    write_header = not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0
    df = pd.DataFrame(rows)
    df.to_csv(csv_path, mode="a", header=write_header, index=False)


def run_experiment(
    seeds: List[int],
    budgets: List[int],
    out_csv: str = DEFAULT_OUT_CSV,
    preflight: bool = False,
):
    n = 8
    N_train = 40
    N_test = 200

    print("================================================================================")
    print("STAGE 2: Equal-Total-Budget Experiment Execution")
    print(f"Classification: CONFIRMATORY (Stage 2 Frozen Protocol)")
    print(f"Seeds ({len(seeds)}): {seeds}")
    print(f"Budgets ({len(budgets)}): {budgets}")
    print(f"Output CSV: {out_csv}")
    print("================================================================================\n")

    completed = get_completed_keys(out_csv)
    times_per_seed = []
    budget_times: Dict[int, List[float]] = {b: [] for b in budgets}

    for seed in seeds:
        t_seed = time.time()
        train_states, tr_targets, test_states, te_targets, _ = make_split(
            task="t1", n=n, N=N_train, seed=seed, target_name="entropy"
        )
        states = (train_states, test_states)
        y = (tr_targets, te_targets)

        for b_idx, B_tot in enumerate(budgets):
            # Check if all 7 arms for (seed, B_tot) are completed
            expected_arms = [
                ("PQK-1", "3basis"), ("PQK-1", "x_only"),
                ("PQK-2nn", "none"), ("E2", "raw_4n_grid"),
                ("FQ", "train_only"), ("FQ", "none"), ("FQ", "inductive"),
            ]
            needed = [pair for pair in expected_arms if (seed, B_tot, pair[0], pair[1]) not in completed]
            if not needed:
                continue

            t_b = time.time()
            # Deterministic RNG seed per (seed, B_tot)
            rng_seed = int(100000 * seed + (b_idx + 1) * 1000)
            rng = np.random.default_rng(rng_seed)

            # Evaluate feature arms
            feat_rows = evaluate_feature_arms(states, y, B_tot, seed, rng, N_train)
            # Evaluate FQ arms
            fq_rows = evaluate_fq_arms(states, y, B_tot, seed, rng, N_train)

            block_rows = feat_rows + fq_rows
            write_rows(out_csv, block_rows)
            for r in block_rows:
                completed.add((r["seed"], r["B_tot"], r["model"], r["variant"]))

            b_elapsed = time.time() - t_b
            budget_times[B_tot].append(b_elapsed)

        seed_elapsed = time.time() - t_seed
        times_per_seed.append(seed_elapsed)
        print(f"Seed {seed:2d} finished in {seed_elapsed:.2f}s")

    # Runtime report
    avg_seed = float(np.mean(times_per_seed)) if times_per_seed else 0.0
    total_run = float(np.sum(times_per_seed)) if times_per_seed else 0.0
    projected_20 = avg_seed * 20.0

    print("\n--------------------------------------------------------------------------------")
    print("STAGE 2 RUNTIME REPORT")
    print("--------------------------------------------------------------------------------")
    print(f"Seeds evaluated: {len(seeds)}")
    print(f"Total time elapsed: {total_run:.2f}s ({total_run/60.0:.2f} min)")
    print(f"Average time per seed: {avg_seed:.2f}s")
    print(f"Projected 20-seed runtime: {projected_20:.2f}s ({projected_20/60.0:.2f} min, {projected_20/3600.0:.3f} h)")

    print("\nPer-Budget Average Runtime:")
    for b in budgets:
        b_avg = float(np.mean(budget_times[b])) if budget_times[b] else 0.0
        print(f"  B_tot = {b:8d}: {b_avg:.3f}s per seed")

    if preflight:
        print("\n--------------------------------------------------------------------------------")
        if projected_20 > 7200.0:
            print(f"PREFLIGHT GATE: FAIL (Projected {projected_20/3600.0:.2f} h > 2.0 h). STOPPING.")
            sys.exit(1)
        else:
            print(f"PREFLIGHT GATE: PASS (Projected {projected_20/3600.0:.2f} h <= 2.0 h). Safe to proceed.")
        print("--------------------------------------------------------------------------------\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stage 2 Equal-Total-Budget Experiment")
    parser.add_argument("--preflight", action="store_true", help="Run 3-seed preflight runtime gate")
    parser.add_argument("--quick", action="store_true", help="Quick mode (seeds 0, 1, 2)")
    parser.add_argument("--run", action="store_true", help="Execute sweep")
    parser.add_argument("--seeds", type=int, nargs="+", default=None, help="List of seeds")
    parser.add_argument("--budgets", type=int, nargs="+", default=None, help="List of budgets")
    parser.add_argument("--out", type=str, default=DEFAULT_OUT_CSV, help="Output CSV path")
    args = parser.parse_args()

    if args.seeds is not None:
        target_seeds = args.seeds
    elif args.preflight or args.quick:
        target_seeds = [0, 1, 2]
    else:
        target_seeds = list(range(20))

    if args.budgets is not None:
        target_budgets = args.budgets
    else:
        target_budgets = BUDGETS_ALL

    run_experiment(
        seeds=target_seeds,
        budgets=target_budgets,
        out_csv=args.out,
        preflight=args.preflight or args.quick,
    )
