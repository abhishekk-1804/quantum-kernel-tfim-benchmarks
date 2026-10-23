"""
scripts/ablation_r1_e2_grid.py
------------------------------
Ablation R1: Evaluate E2(raw) and PQK-2nn on Task 1 (disordered open TFIM, n=8, N_train=40).
Arms:
  A: E2(raw) with its original gamma grid (c/d_E2, d_E2=35), re-evaluated from scratch.
  B: E2(raw) with PQK-2nn's exact gamma grid (c/(4n), 4n=32).
  C: PQK-2nn as in grid_v3 (c/(4n), 4n=32).

Asserts:
  - Arm A reproduces results/t1_entropy_gridv3.csv E2 rows to 1e-10.
  - Arm C reproduces results/t1_entropy_gridv3.csv PQK-2nn rows to 1e-10.

Outputs:
  - results/ablations/t1_e2_pqkgrid.csv
  - Observations: max |B - C| per seed, matching best_params count.
"""

import os
import sys
import time
import json
import argparse
from typing import Dict, List, Any

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
from kernels import classical_features

OUT_CSV = os.path.join(_PROJECT_ROOT, "results", "ablations", "t1_e2_pqkgrid.csv")
REF_CSV = os.path.join(_PROJECT_ROOT, "results", "t1_entropy_gridv3.csv")


def evaluate_arm(
    X_tr: np.ndarray,
    X_te: np.ndarray,
    train_targets: np.ndarray,
    test_targets: np.ndarray,
    gamma_denom: float,
    kf: KFold,
) -> Dict[str, Any]:
    C_search = C_GRID_V2
    c_search = C_FACTORS_V2
    eps_list = EPSILON_GRID_V3

    D2_tr = cdist(X_tr, X_tr, metric="sqeuclidean")
    D2_te = cdist(X_te, X_tr, metric="sqeuclidean")

    folds_data = []
    for tr_idx, val_idx in kf.split(X_tr):
        f_y_tr = train_targets[tr_idx]
        f_m, f_s = float(np.mean(f_y_tr)), float(np.std(f_y_tr))
        if f_s < 1e-12:
            f_s = 1.0
        f_y_tr_z = (f_y_tr - f_m) / f_s
        f_y_val = train_targets[val_idx]
        D2_fold_tr = D2_tr[np.ix_(tr_idx, tr_idx)]
        D2_fold_val = D2_tr[np.ix_(val_idx, tr_idx)]
        folds_data.append((D2_fold_tr, D2_fold_val, f_y_tr_z, f_y_val, f_m, f_s))

    best_cv = -np.inf
    best_C, best_c, best_eps = C_search[0], c_search[0], eps_list[0]

    for c_val in c_search:
        gamma = float(c_val / gamma_denom)
        fold_kernels = []
        for D2_fold_tr, D2_fold_val, f_y_tr_z, f_y_val, f_m, f_s in folds_data:
            K_tr = np.exp(-gamma * D2_fold_tr)
            K_val = np.exp(-gamma * D2_fold_val)
            fold_kernels.append((K_tr, K_val, f_y_tr_z, f_y_val, f_m, f_s))

        for C in C_search:
            for eps in eps_list:
                fold_scores = []
                for K_tr, K_val, f_y_tr_z, f_y_val, f_m, f_s in fold_kernels:
                    clf = SVR(kernel="precomputed", C=float(C), epsilon=float(eps))
                    clf.fit(K_tr, f_y_tr_z)
                    pred_z = clf.predict(K_val)
                    pred = pred_z * f_s + f_m
                    fold_scores.append(r2_score(f_y_val, pred))
                mean_r2 = float(np.mean(fold_scores))
                if mean_r2 > best_cv:
                    best_cv = mean_r2
                    best_C, best_c, best_eps = C, c_val, eps

    best_gamma = float(best_c / gamma_denom)
    K_final_tr = np.exp(-best_gamma * D2_tr)
    K_final_te = np.exp(-best_gamma * D2_te)

    y_mean = float(np.mean(train_targets))
    y_std = float(np.std(train_targets))
    y_train_z = (train_targets - y_mean) / y_std

    clf_final = SVR(kernel="precomputed", C=float(best_C), epsilon=float(best_eps))
    clf_final.fit(K_final_tr, y_train_z)
    pred_z = clf_final.predict(K_final_te)
    pred = pred_z * y_std + y_mean

    r2 = float(r2_score(test_targets, pred))
    mae = float(mean_absolute_error(test_targets, pred))
    b_params = json.dumps({
        "C": float(best_C),
        "c": float(best_c),
        "gamma": float(best_gamma),
        "epsilon": float(best_eps),
    })

    return {
        "r2": r2,
        "mae": mae,
        "best_params": b_params,
        "inner_cv_score": float(best_cv),
    }


def get_completed_keys(csv_path: str) -> set:
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        return set()
    try:
        df = pd.read_csv(csv_path)
        return set(zip(df["seed"], df["N_train"], df["arm"], df["metric"]))
    except Exception:
        return set()


def write_rows(csv_path: str, rows: List[Dict[str, Any]]):
    os.makedirs(os.path.dirname(os.path.abspath(csv_path)), exist_ok=True)
    write_header = not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0
    df = pd.DataFrame(rows)
    df.to_csv(csv_path, mode="a", header=write_header, index=False)


def run_ablation(seeds: List[int], quick: bool = False):
    n = 8
    N_train = 40
    d_e2 = 35.0
    denom_4n = 4.0 * n  # 32.0

    print(f"=== S1.1 R1 Ablation (seeds={seeds}, quick={quick}) ===")

    # Load reference data
    if os.path.exists(REF_CSV):
        df_ref = pd.read_csv(REF_CSV)
        ref_e2 = df_ref[(df_ref["model"] == "E2") & (df_ref["N_train"] == N_train)]
        ref_pqk2 = df_ref[(df_ref["model"] == "PQK-2nn") & (df_ref["N_train"] == N_train)]
    else:
        df_ref = None
        ref_e2 = None
        ref_pqk2 = None
        print(f"WARNING: Reference CSV {REF_CSV} not found!")

    completed = get_completed_keys(OUT_CSV)
    kf = KFold(n_splits=3, shuffle=True, random_state=42)

    all_seed_results = []
    max_diff_a = 0.0
    max_diff_c = 0.0
    times = []

    for seed in seeds:
        t0 = time.time()
        # Check if all arms completed for this seed
        needed_arms = [a for a in ["A", "B", "C"] if (seed, N_train, a, "r2") not in completed]
        
        # We need the split
        train_states, train_targets, test_states, test_targets, _ = make_split(
            task="t1", n=n, N=N_train, seed=seed, target_name="entropy"
        )

        # Extract E2 features
        X_e2_tr = np.array([classical_features(psi, n, mode="2pt_pauli_nn") for psi in train_states])
        X_e2_te = np.array([classical_features(psi, n, mode="2pt_pauli_nn") for psi in test_states])

        rows_seed = []

        # Arm A: E2(raw) with c/d_E2 (d_e2 = 35.0)
        res_a = evaluate_arm(X_e2_tr, X_e2_te, train_targets, test_targets, d_e2, kf)
        for m in ["r2", "mae"]:
            rows_seed.append({
                "seed": seed, "N_train": N_train, "arm": "A",
                "metric": m, "value": res_a[m],
                "best_params": res_a["best_params"],
                "inner_cv_score": res_a["inner_cv_score"],
                "source": "recomputed",
            })

        # Arm B: E2(raw) with c/(4n) (denom = 32.0)
        res_b = evaluate_arm(X_e2_tr, X_e2_te, train_targets, test_targets, denom_4n, kf)
        for m in ["r2", "mae"]:
            rows_seed.append({
                "seed": seed, "N_train": N_train, "arm": "B",
                "metric": m, "value": res_b[m],
                "best_params": res_b["best_params"],
                "inner_cv_score": res_b["inner_cv_score"],
                "source": "ablation",
            })

        # Arm C: PQK-2nn (c/(4n))
        res_c = evaluate_arm(X_e2_tr, X_e2_te, train_targets, test_targets, denom_4n, kf)
        for m in ["r2", "mae"]:
            rows_seed.append({
                "seed": seed, "N_train": N_train, "arm": "C",
                "metric": m, "value": res_c[m],
                "best_params": res_c["best_params"],
                "inner_cv_score": res_c["inner_cv_score"],
                "source": "grid_v3_recomputed",
            })

        # Assert reproduction if ref data exists
        if ref_e2 is not None and len(ref_e2) > 0:
            for m in ["r2", "mae"]:
                sub_ref_a = ref_e2[(ref_e2["seed"] == seed) & (ref_e2["metric"] == m)]
                if len(sub_ref_a) > 0:
                    val_ref_a = float(sub_ref_a["value"].values[0])
                    diff_a = abs(res_a[m] - val_ref_a)
                    max_diff_a = max(max_diff_a, diff_a)
                    assert diff_a < 1e-10, f"Arm A seed {seed} {m} mismatch: recomputed={res_a[m]} vs ref={val_ref_a} (diff={diff_a})"

                sub_ref_c = ref_pqk2[(ref_pqk2["seed"] == seed) & (ref_pqk2["metric"] == m)]
                if len(sub_ref_c) > 0:
                    val_ref_c = float(sub_ref_c["value"].values[0])
                    diff_c = abs(res_c[m] - val_ref_c)
                    max_diff_c = max(max_diff_c, diff_c)
                    assert diff_c < 1e-10, f"Arm C seed {seed} {m} mismatch: recomputed={res_c[m]} vs ref={val_ref_c} (diff={diff_c})"

        # Write rows for uncompleted keys
        to_write = [r for r in rows_seed if (r["seed"], r["N_train"], r["arm"], r["metric"]) not in completed]
        if to_write:
            write_rows(OUT_CSV, to_write)
            for r in to_write:
                completed.add((r["seed"], r["N_train"], r["arm"], r["metric"]))

        elapsed = time.time() - t0
        times.append(elapsed)
        all_seed_results.append({
            "seed": seed,
            "res_a": res_a,
            "res_b": res_b,
            "res_c": res_c,
            "elapsed": elapsed,
        })
        print(f"  Seed {seed:2d}: computed in {elapsed:.2f}s | diff_A_ref={max_diff_a:.2e}, diff_C_ref={max_diff_c:.2e}")

    # Summary statistics & observations
    avg_time = float(np.mean(times))
    total_time = float(np.sum(times))
    projected_20 = avg_time * 20.0
    print(f"\n--- Runtime Report ---")
    print(f"Seeds evaluated: {len(seeds)}")
    print(f"Average time per seed: {avg_time:.2f}s")
    print(f"Total time for {len(seeds)} seeds: {total_time:.2f}s ({total_time/60.0:.2f} min)")
    print(f"Projected total time for 20 seeds: {projected_20:.2f}s ({projected_20/60.0:.2f} min, {projected_20/3600.0:.2f} h)")

    print(f"\n--- Reproduction Assertions ---")
    print(f"Max |Arm A - Reference E2|: {max_diff_a:.2e} (tolerance: 1e-10) -> {'PASS' if max_diff_a < 1e-10 else 'FAIL'}")
    print(f"Max |Arm C - Reference PQK-2nn|: {max_diff_c:.2e} (tolerance: 1e-10) -> {'PASS' if max_diff_c < 1e-10 else 'FAIL'}")

    # Comparison of B and C
    diffs_bc_r2 = []
    diffs_bc_mae = []
    matching_params = 0
    for s_res in all_seed_results:
        d_r2 = abs(s_res["res_b"]["r2"] - s_res["res_c"]["r2"])
        d_mae = abs(s_res["res_b"]["mae"] - s_res["res_c"]["mae"])
        diffs_bc_r2.append(d_r2)
        diffs_bc_mae.append(d_mae)
        if s_res["res_b"]["best_params"] == s_res["res_c"]["best_params"]:
            matching_params += 1

    max_diff_bc_r2 = max(diffs_bc_r2) if diffs_bc_r2 else 0.0
    max_diff_bc_mae = max(diffs_bc_mae) if diffs_bc_mae else 0.0

    print(f"\n--- Arm B vs Arm C Observations ---")
    print(f"Max |B - C| R2 across evaluated seeds: {max_diff_bc_r2:.2e}")
    print(f"Max |B - C| MAE across evaluated seeds: {max_diff_bc_mae:.2e}")
    print(f"Number of evaluated seeds with identical best_params: {matching_params} / {len(all_seed_results)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ablation R1: E2 vs PQK-2nn grid")
    parser.add_argument("--quick", action="store_true", help="Run 3 seeds for runtime preflight")
    parser.add_argument("--seeds", type=int, nargs="+", default=None, help="Explicit list of seeds")
    args = parser.parse_args()

    if args.seeds is not None:
        target_seeds = args.seeds
    elif args.quick:
        target_seeds = [0, 1, 2]
    else:
        target_seeds = list(range(20))

    run_ablation(target_seeds, quick=args.quick)
