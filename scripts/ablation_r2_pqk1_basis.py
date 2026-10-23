"""
scripts/ablation_r2_pqk1_basis.py
---------------------------------
Ablation R2: Evaluate PQK-1 basis comparison on Task 1 (open TFIM, n=8, N_train=40, N_test=200).
Shots: S in {100, 300, 1000, 3000, 10000}, 20 seeds (0 to 19).
Arms:
  - PQK-1 (X-only): Expectation of X only from basis X. Shot accounting: 1 * m * S.
  - PQK-1 (X+Z): Expectations of X and Z from bases X and Z. Shot accounting: 2 * m * S.

Asserts:
  - PQK-1 (X+Z) reproduces existing results/t5_noise.csv rows for S in {100, 1000, 10000} to 1e-10.

Outputs:
  - results/ablations/t5_pqk1_basis.csv
  - Paired bootstrap CI (10,000 resamples, RNG seed 20261023) of R2 difference per S.
  - Labeled "exploratory".
"""

import os
import sys
import time
import json
import argparse
from typing import Dict, List, Any, Tuple

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.model_selection import KFold
from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_absolute_error

# Add paths
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
from noise import get_basis_rotation_matrix

OUT_CSV = os.path.join(_PROJECT_ROOT, "results", "ablations", "t5_pqk1_basis.csv")
REF_CSV = os.path.join(_PROJECT_ROOT, "results", "t5_noise.csv")

# Precomputed rotation unitaries at n=8
_UX_8 = get_basis_rotation_matrix("X", 8)
_UY_8 = get_basis_rotation_matrix("Y", 8)

SHOTS_ALL = [100, 300, 1000, 3000, 10000]


def evaluate_svr_fast(
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

    best_gamma = float(best_c / gamma_denom)
    K_final_tr = np.exp(-best_gamma * D2_tr)
    K_final_te = np.exp(-best_gamma * D2_te)
    svr_final = SVR(kernel="precomputed", C=float(best_C), epsilon=float(best_eps))
    svr_final.fit(K_final_tr, y_tr_z)
    pred_z = svr_final.predict(K_final_te)
    pred_orig = pred_z * y_std + y_mean

    r2 = float(r2_score(y_te, pred_orig))
    mae = float(mean_absolute_error(y_te, pred_orig))
    b_params = json.dumps({
        "C": float(best_C),
        "c": float(best_c),
        "gamma": float(best_gamma),
        "epsilon": float(best_eps),
    })
    return r2, mae, b_params, float(best_cv)


def get_completed_keys(csv_path: str) -> set:
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        return set()
    try:
        df = pd.read_csv(csv_path)
        return set(zip(df["seed"], df["N_train"], df["S"], df["arm"], df["metric"]))
    except Exception:
        return set()


def write_rows(csv_path: str, rows: List[Dict[str, Any]]):
    os.makedirs(os.path.dirname(os.path.abspath(csv_path)), exist_ok=True)
    write_header = not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0
    df = pd.DataFrame(rows)
    df.to_csv(csv_path, mode="a", header=write_header, index=False)


def run_ablation(seeds: List[int], shots_list: List[int], quick: bool = False):
    n = 8
    N_train = 40
    N_test = 200
    m = N_train + N_test  # 240

    print(f"=== S1.2 R2 Ablation: PQK-1 Basis Comparison (seeds={seeds}, shots={shots_list}) ===")

    # Load reference data
    df_ref = None
    if os.path.exists(REF_CSV):
        df_ref = pd.read_csv(REF_CSV)
        # Filter for finite_shots PQK-1
        df_ref = df_ref[(df_ref["experiment"] == "finite_shots") & (df_ref["model"] == "PQK-1")]
        # Cast noise_level to int
        df_ref["shots_int"] = pd.to_numeric(df_ref["noise_level"], errors="coerce")
    else:
        print(f"WARNING: Reference CSV {REF_CSV} not found!")

    completed = get_completed_keys(OUT_CSV)
    kf = KFold(n_splits=3, shuffle=True, random_state=42)

    # Bitstring signs
    dim = 256
    k_indices = np.arange(dim)
    bitstrings = ((k_indices[:, None] >> np.arange(n - 1, -1, -1)) & 1)
    signs = 1.0 - 2.0 * bitstrings  # (256, 8)

    times = []
    max_diff_xz_ref = 0.0
    all_rows = []

    for seed in seeds:
        t0 = time.time()
        train_states, tr_targets, test_states, te_targets, _ = make_split(
            task="t1", n=n, N=N_train, seed=seed, target_name="entropy"
        )
        all_states = np.vstack([train_states, test_states])

        y_mean = float(np.mean(tr_targets))
        y_std = float(np.std(tr_targets))
        if y_std < 1e-12:
            y_std = 1.0
        y_tr_z = (tr_targets - y_mean) / y_std

        # State rotations for all 240 states
        all_psi_x = all_states @ _UX_8.T
        all_psi_y = all_states @ _UY_8.T
        probs_x = np.abs(all_psi_x) ** 2
        probs_y = np.abs(all_psi_y) ** 2
        probs_z = np.abs(all_states) ** 2

        seed_rows = []
        for S in shots_list:
            # Check if both arms completed
            needed = [a for a in ["PQK-1 (X+Z)", "PQK-1 (X-only)"] if (seed, N_train, S, a, "r2") not in completed]
            if not needed:
                continue

            # Deterministic RNG exactly as in run_t5_noise.py
            rng_seed = int(100000 * seed + S)
            rng = np.random.default_rng(rng_seed)

            # Sample basis measurements for all 240 states in order: X, Y, Z
            counts_x = np.array([rng.multinomial(S, probs_x[i]) for i in range(m)], dtype=float) / S
            counts_y = np.array([rng.multinomial(S, probs_y[i]) for i in range(m)], dtype=float) / S
            counts_z = np.array([rng.multinomial(S, probs_z[i]) for i in range(m)], dtype=float) / S

            exp_x = counts_x @ signs  # (240, 8)
            exp_z = counts_z @ signs  # (240, 8)

            # Arm 1: PQK-1 (X+Z)
            X_pqk1_xz = np.hstack([exp_x, exp_z]) / np.sqrt(2.0)
            r2_xz, mae_xz, params_xz, cv_xz = evaluate_svr_fast(
                X_pqk1_xz[:N_train], y_tr_z, tr_targets, X_pqk1_xz[N_train:], te_targets,
                float(n), y_mean, y_std, kf
            )

            # Arm 2: PQK-1 (X-only)
            # Feature is exp_x, gamma_denom is 2.0 * n (matches noiseless PQK-1 normalization)
            X_pqk1_x = exp_x
            r2_x, mae_x, params_x, cv_x = evaluate_svr_fast(
                X_pqk1_x[:N_train], y_tr_z, tr_targets, X_pqk1_x[N_train:], te_targets,
                2.0 * n, y_mean, y_std, kf
            )

            # Verification against reference t5_noise.csv for X+Z arm
            if df_ref is not None:
                sub_ref = df_ref[(df_ref["seed"] == seed) & (df_ref["shots_int"] == S)]
                if len(sub_ref) > 0:
                    ref_r2_row = sub_ref[sub_ref["metric"] == "r2"]
                    if len(ref_r2_row) > 0:
                        ref_r2 = float(ref_r2_row["value"].values[0])
                        diff = abs(r2_xz - ref_r2)
                        max_diff_xz_ref = max(max_diff_xz_ref, diff)
                        assert diff < 1e-10, f"Seed {seed} S={S} X+Z mismatch: got {r2_xz}, ref={ref_r2}, diff={diff}"

            # Log rows
            for met, val in [("r2", r2_xz), ("mae", mae_xz)]:
                seed_rows.append({
                    "seed": seed, "N_train": N_train, "S": S,
                    "arm": "PQK-1 (X+Z)", "metric": met, "value": val,
                    "best_params": params_xz, "inner_cv_score": cv_xz,
                    "total_shots": 2 * m * S, "source": "t5_recomputed",
                })
            for met, val in [("r2", r2_x), ("mae", mae_x)]:
                seed_rows.append({
                    "seed": seed, "N_train": N_train, "S": S,
                    "arm": "PQK-1 (X-only)", "metric": met, "value": val,
                    "best_params": params_x, "inner_cv_score": cv_x,
                    "total_shots": 1 * m * S, "source": "ablation",
                })

        if seed_rows:
            write_rows(OUT_CSV, seed_rows)
            for r in seed_rows:
                completed.add((r["seed"], r["N_train"], r["S"], r["arm"], r["metric"]))
            all_rows.extend(seed_rows)

        elapsed = time.time() - t0
        times.append(elapsed)
        print(f"  Seed {seed:2d}: evaluated in {elapsed:.2f}s | max_diff_ref(X+Z)={max_diff_xz_ref:.2e}")

    # Summary & Bootstrap analysis
    avg_time = float(np.mean(times)) if times else 0.0
    total_time = float(np.sum(times)) if times else 0.0
    projected_20 = avg_time * 20.0
    print(f"\n--- Runtime Report ---")
    print(f"Seeds evaluated: {len(seeds)}")
    print(f"Average time per seed: {avg_time:.2f}s")
    print(f"Total time for {len(seeds)} seeds: {total_time:.2f}s ({total_time/60.0:.2f} min)")
    print(f"Projected total time for 20 seeds: {projected_20:.2f}s ({projected_20/60.0:.2f} min, {projected_20/3600.0:.2f} h)")

    print(f"\n--- Reference Reproduction (X+Z Arm vs t5_noise.csv) ---")
    print(f"Max |PQK-1(X+Z) - Reference t5_noise.csv|: {max_diff_xz_ref:.2e} -> {'PASS' if max_diff_xz_ref < 1e-10 else 'FAIL'}")

    # Paired Bootstrap CI (10,000 resamples, rng seed 20261023)
    # Read full CSV to compute bootstrap across all available seeds
    if os.path.exists(OUT_CSV):
        df_all = pd.read_csv(OUT_CSV)
        df_r2 = df_all[df_all["metric"] == "r2"]

        print(f"\n--- Paired Bootstrap Analysis: [PQK-1 (X-only)] - [PQK-1 (X+Z)] (R2) ---")
        print(f"Label: EXPLORATORY (10,000 bootstrap resamples, RNG seed 20261023)")
        print(f"{'S':>6} | {'N_seeds':>7} | {'Mean R2 (X+Z)':>14} | {'Mean R2 (X-only)':>16} | {'Mean Diff':>10} | {'95% Bootstrap CI':>22}")
        print("-" * 85)

        rng_boot = np.random.default_rng(20261023)

        for S in shots_list:
            sub_s = df_r2[df_r2["S"] == S]
            seeds_available = sorted(sub_s["seed"].unique())
            if not seeds_available:
                continue

            r2_xz_list = []
            r2_x_list = []
            for s in seeds_available:
                v_xz = sub_s[(sub_s["seed"] == s) & (sub_s["arm"] == "PQK-1 (X+Z)")]["value"].values
                v_x = sub_s[(sub_s["seed"] == s) & (sub_s["arm"] == "PQK-1 (X-only)")]["value"].values
                if len(v_xz) > 0 and len(v_x) > 0:
                    r2_xz_list.append(v_xz[0])
                    r2_x_list.append(v_x[0])

            r2_xz_arr = np.array(r2_xz_list)
            r2_x_arr = np.array(r2_x_list)
            diffs = r2_x_arr - r2_xz_arr
            n_eval = len(diffs)

            if n_eval == 0:
                continue

            mean_diff = float(np.mean(diffs))
            mean_xz = float(np.mean(r2_xz_arr))
            mean_x = float(np.mean(r2_x_arr))

            # Bootstrap
            boot_diffs = []
            for _ in range(10000):
                boot_idx = rng_boot.integers(0, n_eval, size=n_eval)
                boot_diffs.append(float(np.mean(diffs[boot_idx])))
            ci_low = float(np.percentile(boot_diffs, 2.5))
            ci_high = float(np.percentile(boot_diffs, 97.5))

            print(f"{S:6d} | {n_eval:7d} | {mean_xz:14.4f} | {mean_x:16.4f} | {mean_diff:+10.4f} | [{ci_low:+.4f}, {ci_high:+.4f}]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ablation R2: PQK-1 basis comparison")
    parser.add_argument("--quick", action="store_true", help="Run 3 seeds for runtime preflight")
    parser.add_argument("--seeds", type=int, nargs="+", default=None, help="Explicit list of seeds")
    parser.add_argument("--shots", type=int, nargs="+", default=None, help="Explicit list of shot budgets")
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

    run_ablation(target_seeds, target_shots, quick=args.quick)
