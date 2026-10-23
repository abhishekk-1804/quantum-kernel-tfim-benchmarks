"""
scripts/ablation_r3_experiment.py
---------------------------------
R3 Decision Experiment: Evaluation of Gram Repair Strategies for Finite-Shot FQ.
Setup:
  Task 1: Disordered open-chain TFIM (n=8, N_train=40, N_test=200, 20 seeds).
  Shot budgets: S in {100, 300, 1000, 3000, 10000}.
  Arms:
    1. none: Unrepaired noisy Gram (FQ-raw baseline).
    2. train_only: Train-only PSD clipping (FQ-clipped production baseline).
    3. inductive: Inductive eigenvalue clipping & projection of test block.
    4. joint: Transductive joint clipping of (N_tr + N_te) Gram then slicing.

Asserts:
  - 'train_only' reproduces results/t5_noise.csv FQ-clipped rows to 1e-10.
  - 'none' reproduces results/t5_noise.csv FQ-raw rows to 1e-10.

Outputs:
  - results/ablations/t5_fq_repairs.csv
  - Statistical summary table (mean R2, paired bootstrap CIs, count of R2 < 0.7).
  - All results labeled "exploratory".
"""

import os
import sys
import time
import json
import argparse
from typing import Dict, List, Any, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_absolute_error

# Add src and scripts to path
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SCRIPTS = os.path.join(_PROJECT_ROOT, "scripts")
_SRC = os.path.join(_PROJECT_ROOT, "src")
for p in [_SRC, _SCRIPTS]:
    if p not in sys.path:
        sys.path.insert(0, p)

from common import (
    C_GRID_V2,
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
    repair_joint,
)

OUT_CSV = os.path.join(_PROJECT_ROOT, "results", "ablations", "t5_fq_repairs.csv")
REF_CSV = os.path.join(_PROJECT_ROOT, "results", "t5_noise.csv")

SHOTS_ALL = [100, 300, 1000, 3000, 10000]

# Precomputed rotation unitaries at n=8
_UX_8 = get_basis_rotation_matrix("X", 8)
_UY_8 = get_basis_rotation_matrix("Y", 8)


def evaluate_svr_arm(
    K_raw_tr: np.ndarray,
    K_raw_te: np.ndarray,
    tr_targets: np.ndarray,
    te_targets: np.ndarray,
    y_mean: float,
    y_std: float,
    kf: KFold,
    repair_mode: str,
) -> Tuple[float, float, str, float, float]:
    """
    Inner 3-fold CV tuning and final scoring for precomputed Gram matrix.
    Applies the identical repair mode to inner-fold training blocks from the raw Gram.
    Returns: (test_r2, test_mae, best_params_json, best_cv_score, lam_min_train_after)
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
            K_fit_fold, K_pred_fold = repair_inductive(K_f_tr, K_f_val)
        elif repair_mode == "joint":
            # For joint repair, K_raw_tr passed in is already K_tr_joint sliced from the full PSD Gram
            K_fit_fold, K_pred_fold = K_f_tr, K_f_val
        else:
            raise ValueError(f"Unknown repair mode: {repair_mode}")

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
        K_fit_final, K_pred_final = repair_inductive(K_raw_tr, K_raw_te)
    elif repair_mode == "joint":
        K_fit_final, K_pred_final = K_raw_tr, K_raw_te
    else:
        raise ValueError(f"Unknown repair mode: {repair_mode}")

    lam_min_after = float(np.min(np.linalg.eigvalsh(0.5 * (K_fit_final + K_fit_final.T))))

    svr_final = SVR(kernel="precomputed", C=float(best_C), epsilon=float(best_eps))
    svr_final.fit(K_fit_final, y_tr_z)
    pred_te_z = svr_final.predict(K_pred_final)
    pred_te = pred_te_z * y_std + y_mean

    r2 = float(r2_score(te_targets, pred_te))
    mae = float(mean_absolute_error(te_targets, pred_te))
    params_str = json.dumps({"C": float(best_C), "epsilon": float(best_eps)})
    return r2, mae, params_str, float(best_cv), lam_min_after


def get_completed_keys(csv_path: str) -> set:
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        return set()
    try:
        df = pd.read_csv(csv_path)
        return set(zip(df["seed"], df["S"], df["arm"], df["metric"]))
    except Exception:
        return set()


def write_rows(csv_path: str, rows: List[Dict[str, Any]]):
    os.makedirs(os.path.dirname(os.path.abspath(csv_path)), exist_ok=True)
    write_header = not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0
    df = pd.DataFrame(rows)
    df.to_csv(csv_path, mode="a", header=write_header, index=False)


def run_experiment(seeds: List[int], shots_list: List[int], quick: bool = False):
    n = 8
    N_train = 40
    N_test = 200
    m = N_train + N_test  # 240

    print(f"=== S1b.2 R3 Decision Experiment (seeds={seeds}, shots={shots_list}) ===")

    # Reference data for reproduction assertions
    df_ref = None
    if os.path.exists(REF_CSV):
        df_ref = pd.read_csv(REF_CSV)
        df_ref = df_ref[df_ref["experiment"] == "finite_shots"].copy()
        df_ref["shots_int"] = pd.to_numeric(df_ref["noise_level"], errors="coerce")
    else:
        print(f"WARNING: Reference CSV {REF_CSV} not found!")

    completed = get_completed_keys(OUT_CSV)
    kf = KFold(n_splits=3, shuffle=True, random_state=42)

    times = []
    max_diff_clipped_ref = 0.0
    max_diff_raw_ref = 0.0

    for seed in seeds:
        t_seed = time.time()
        train_states, tr_targets, test_states, te_targets, _ = make_split(
            task="t1", n=n, N=N_train, seed=seed, target_name="entropy"
        )
        all_states = np.vstack([train_states, test_states])
        K_pure_full = (all_states @ all_states.T) ** 2

        y_mean = float(np.mean(tr_targets))
        y_std = float(np.std(tr_targets))
        if y_std < 1e-12:
            y_std = 1.0

        all_psi_x = all_states @ _UX_8.T
        all_psi_y = all_states @ _UY_8.T
        probs_x = np.abs(all_psi_x) ** 2
        probs_y = np.abs(all_psi_y) ** 2
        probs_z = np.abs(all_states) ** 2

        for S in shots_list:
            # Check if all 4 arms for this (seed, S) are completed
            arms_to_run = [a for a in ["none", "train_only", "inductive", "joint"] if (seed, S, a, "r2") not in completed]
            if not arms_to_run:
                continue

            # Deterministic RNG advancing sequence matching run_t5_noise.py exactly
            rng_seed = int(100000 * seed + S)
            rng = np.random.default_rng(rng_seed)
            _counts_x = np.array([rng.multinomial(S, probs_x[i]) for i in range(m)], dtype=float) / S
            _counts_y = np.array([rng.multinomial(S, probs_y[i]) for i in range(m)], dtype=float) / S
            _counts_z = np.array([rng.multinomial(S, probs_z[i]) for i in range(m)], dtype=float) / S

            # Noisy destructive swap-test Gram matrix
            K_hat, _ = destructive_swap_test_fidelity(K_pure_full, S, rng)
            K_hat_tr = K_hat[:N_train, :N_train]
            K_hat_te = K_hat[N_train:, :N_train]

            # Spectral diagnostics of raw training block
            evals_tr_raw = np.linalg.eigvalsh(0.5 * (K_hat_tr + K_hat_tr.T))
            lam_min_raw = float(np.min(evals_tr_raw))
            frac_neg = float(np.sum(evals_tr_raw < 0.0) / len(evals_tr_raw))

            seed_s_rows = []

            # 1. Arm: none
            r2_none, mae_none, params_none, cv_none, lam_after_none = evaluate_svr_arm(
                K_hat_tr, K_hat_te, tr_targets, te_targets, y_mean, y_std, kf, repair_mode="none"
            )
            for m_name, val in [("r2", r2_none), ("mae", mae_none)]:
                seed_s_rows.append({
                    "seed": seed, "S": S, "arm": "none", "metric": m_name, "value": val,
                    "lam_min_train_before": lam_min_raw,
                    "lam_min_train_after": lam_after_none,
                    "frac_negative_eig_train": frac_neg,
                    "best_params": params_none, "inner_cv_score": cv_none,
                    "total_shots_deployed": 8000 * S, "total_shots_full": 28680 * S,
                    "transductive": False,
                })

            # 2. Arm: train_only
            r2_to, mae_to, params_to, cv_to, lam_after_to = evaluate_svr_arm(
                K_hat_tr, K_hat_te, tr_targets, te_targets, y_mean, y_std, kf, repair_mode="train_only"
            )
            for m_name, val in [("r2", r2_to), ("mae", mae_to)]:
                seed_s_rows.append({
                    "seed": seed, "S": S, "arm": "train_only", "metric": m_name, "value": val,
                    "lam_min_train_before": lam_min_raw,
                    "lam_min_train_after": lam_after_to,
                    "frac_negative_eig_train": frac_neg,
                    "best_params": params_to, "inner_cv_score": cv_to,
                    "total_shots_deployed": 8000 * S, "total_shots_full": 28680 * S,
                    "transductive": False,
                })

            # 3. Arm: inductive
            r2_ind, mae_ind, params_ind, cv_ind, lam_after_ind = evaluate_svr_arm(
                K_hat_tr, K_hat_te, tr_targets, te_targets, y_mean, y_std, kf, repair_mode="inductive"
            )
            for m_name, val in [("r2", r2_ind), ("mae", mae_ind)]:
                seed_s_rows.append({
                    "seed": seed, "S": S, "arm": "inductive", "metric": m_name, "value": val,
                    "lam_min_train_before": lam_min_raw,
                    "lam_min_train_after": lam_after_ind,
                    "frac_negative_eig_train": frac_neg,
                    "best_params": params_ind, "inner_cv_score": cv_ind,
                    "total_shots_deployed": 8000 * S, "total_shots_full": 28680 * S,
                    "transductive": False,
                })

            # 4. Arm: joint (transductive)
            K_tr_joint, K_te_joint = repair_joint(K_hat, N_train)
            r2_joint, mae_joint, params_joint, cv_joint, lam_after_joint = evaluate_svr_arm(
                K_tr_joint, K_te_joint, tr_targets, te_targets, y_mean, y_std, kf, repair_mode="joint"
            )
            for m_name, val in [("r2", r2_joint), ("mae", mae_joint)]:
                seed_s_rows.append({
                    "seed": seed, "S": S, "arm": "joint", "metric": m_name, "value": val,
                    "lam_min_train_before": lam_min_raw,
                    "lam_min_train_after": lam_after_joint,
                    "frac_negative_eig_train": frac_neg,
                    "best_params": params_joint, "inner_cv_score": cv_joint,
                    "total_shots_deployed": 28680 * S, "total_shots_full": 28680 * S,
                    "transductive": True,
                })

            # Verify reproduction assertions against results/t5_noise.csv
            if df_ref is not None:
                sub_ref_s = df_ref[(df_ref["seed"] == seed) & (df_ref["shots_int"] == S)]
                if len(sub_ref_s) > 0:
                    row_c = sub_ref_s[(sub_ref_s["model"] == "FQ-clipped") & (sub_ref_s["metric"] == "r2")]
                    if len(row_c) > 0:
                        ref_val_c = float(row_c["value"].values[0])
                        diff_c = abs(r2_to - ref_val_c)
                        max_diff_clipped_ref = max(max_diff_clipped_ref, diff_c)
                        assert diff_c < 1e-10, f"Seed {seed} S={S} FQ-clipped mismatch: {r2_to} vs {ref_val_c}"

                    row_r = sub_ref_s[(sub_ref_s["model"] == "FQ-raw") & (sub_ref_s["metric"] == "r2")]
                    if len(row_r) > 0:
                        ref_val_r = float(row_r["value"].values[0])
                        diff_r = abs(r2_none - ref_val_r)
                        max_diff_raw_ref = max(max_diff_raw_ref, diff_r)
                        assert diff_r < 1e-10, f"Seed {seed} S={S} FQ-raw mismatch: {r2_none} vs {ref_val_r}"

            # Flush rows per (seed, S)
            write_rows(OUT_CSV, seed_s_rows)
            for r in seed_s_rows:
                completed.add((r["seed"], r["S"], r["arm"], r["metric"]))

        elapsed = time.time() - t_seed
        times.append(elapsed)
        print(f"  Seed {seed:2d}: evaluated in {elapsed:.2f}s | max_diff_clipped={max_diff_clipped_ref:.2e}, max_diff_raw={max_diff_raw_ref:.2e}")

    avg_time = float(np.mean(times)) if times else 0.0
    total_time = float(np.sum(times)) if times else 0.0
    projected_20 = avg_time * 20.0
    print(f"\n--- Runtime Report ---")
    print(f"Seeds evaluated: {len(seeds)}")
    print(f"Average time per seed: {avg_time:.2f}s")
    print(f"Total time for {len(seeds)} seeds: {total_time:.2f}s ({total_time/60.0:.2f} min)")
    print(f"Projected total time for 20 seeds: {projected_20:.2f}s ({projected_20/60.0:.2f} min, {projected_20/3600.0:.2f} h)")

    print(f"\n--- Reference Reproduction Assertions ---")
    print(f"Max |train_only - Reference FQ-clipped|: {max_diff_clipped_ref:.2e} -> {'PASS' if max_diff_clipped_ref < 1e-10 else 'FAIL'}")
    print(f"Max |none - Reference FQ-raw|:         {max_diff_raw_ref:.2e} -> {'PASS' if max_diff_raw_ref < 1e-10 else 'FAIL'}")

    # Statistical Report from CSV
    print_summary_tables(OUT_CSV, shots_list)


def print_summary_tables(csv_path: str, shots_list: List[int]):
    if not os.path.exists(csv_path):
        return

    df = pd.read_csv(csv_path)
    df_r2 = df[df["metric"] == "r2"]

    print("\n=========================================================================================")
    print("TABLE 1: Mean R2 and Failure Count (R2 < 0.7) by Repair Arm and Shot Budget")
    print("Label: EXPLORATORY (Task 1 Disordered TFIM, N_train=40, N_test=200)")
    print("=========================================================================================")
    print(f"{'S':>6} | {'none':>14} | {'train_only':>14} | {'inductive':>14} | {'joint (transd)':>16}")
    print("-" * 75)

    for S in shots_list:
        sub_s = df_r2[df_r2["S"] == S]
        if len(sub_s) == 0:
            continue
        vals_str = []
        for arm in ["none", "train_only", "inductive", "joint"]:
            sub_arm = sub_s[sub_s["arm"] == arm]["value"]
            m_r2 = float(np.mean(sub_arm)) if len(sub_arm) > 0 else np.nan
            n_fail = int(np.sum(sub_arm < 0.7)) if len(sub_arm) > 0 else 0
            vals_str.append(f"{m_r2:.4f} (fail:{n_fail:2d})")
        print(f"{S:6d} | {vals_str[0]:>14} | {vals_str[1]:>14} | {vals_str[2]:>14} | {vals_str[3]:>16}")

    print("\n=========================================================================================")
    print("TABLE 2: Paired Differences with 10,000-Sample Bootstrap 95% CI (RNG Seed 20261023)")
    print("Label: EXPLORATORY")
    print("=========================================================================================")
    print(f"{'S':>6} | {'Comparison Pair':>24} | {'Mean Diff':>10} | {'95% Bootstrap CI':>24}")
    print("-" * 75)

    rng_boot = np.random.default_rng(20261023)

    for S in shots_list:
        sub_s = df_r2[df_r2["S"] == S]
        if len(sub_s) == 0:
            continue
        seeds = sorted(sub_s["seed"].unique())
        n_seeds = len(seeds)

        def get_series(arm_name):
            return np.array([sub_s[(sub_s["seed"] == s) & (sub_s["arm"] == arm_name)]["value"].values[0] for s in seeds])

        try:
            r2_none = get_series("none")
            r2_to = get_series("train_only")
            r2_ind = get_series("inductive")
            r2_joint = get_series("joint")

            comparisons = [
                ("inductive - train_only", r2_ind - r2_to),
                ("inductive - none", r2_ind - r2_none),
                ("joint - inductive", r2_joint - r2_ind),
            ]

            for comp_name, diffs in comparisons:
                m_diff = float(np.mean(diffs))
                boot_diffs = []
                for _ in range(10000):
                    idx = rng_boot.integers(0, n_seeds, size=n_seeds)
                    boot_diffs.append(float(np.mean(diffs[idx])))
                ci_low = float(np.percentile(boot_diffs, 2.5))
                ci_high = float(np.percentile(boot_diffs, 97.5))
                print(f"{S:6d} | {comp_name:>24} | {m_diff:+10.4f} | [{ci_low:+.4f}, {ci_high:+.4f}]")
        except Exception as e:
            print(f"Error computing comparisons for S={S}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ablation R3: FQ Gram Repairs Experiment")
    parser.add_argument("--quick", action="store_true", help="Run 3 seeds for runtime preflight")
    parser.add_argument("--seeds", type=int, nargs="+", default=None, help="Explicit list of seeds")
    parser.add_argument("--shots", type=int, nargs="+", default=None, help="Explicit list of shots")
    args = parser.parse_args()

    if args.seeds is not None:
        target_seeds = args.seeds
    elif args.quick:
        target_seeds = [0, 1, 2]
    else:
        target_seeds = list(range(20))

    if args.shots is not None:
        target_shots = args.shots
    else:
        target_shots = SHOTS_ALL

    run_experiment(target_seeds, target_shots, quick=args.quick)
