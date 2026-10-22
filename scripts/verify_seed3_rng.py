"""
scripts/verify_seed3_rng.py
---------------------------
Mandatory Pre-Check: Seed 3 RNG Stream Audit.
Runs an isolated sequential single-process evaluation of Task T2b (<Z_0 Z_1 Z_{n-2} Z_{n-1}>),
Seed = 3, N_train = 40 for PQK-2nn and FQ, and compares against results/t2_correlators_gridv3.csv.
"""

import os
import sys
import numpy as np
import pandas as pd

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from common import make_split, evaluate_regression_models

def verify_seed3():
    csv_path = os.path.join("results", "t2_correlators_gridv3.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"{csv_path} not found.")

    df_merged = pd.read_csv(csv_path)

    # Filter merged records for Seed 3, N_train = 40, Task T2b, metric r2
    sub_merged = df_merged[
        (df_merged["task"] == "T2b") &
        (df_merged["seed"] == 3) &
        (df_merged["N_train"] == 40) &
        (df_merged["metric"] == "r2")
    ]

    r2_merged = {}
    for _, row in sub_merged.iterrows():
        r2_merged[row["model"]] = float(row["value"])

    print("Merged CSV recorded values for Seed 3, N=40, T2b:")
    for m in ["PQK-2nn", "FQ"]:
        print(f"  {m}: {r2_merged.get(m, 'MISSING')}")

    # Run isolated sequential evaluation
    n = 8
    N = 40
    seed = 3
    tr_states, tr_targets, te_states, te_targets, _ = make_split(
        task="t2", n=n, N=N, seed=seed, target_name="zzzz"
    )

    rows = evaluate_regression_models(
        task="T2b",
        target="z0_z1_zn2_zn1",
        tag="not_contained",
        n=n,
        N_train=N,
        seed=seed,
        train_states=tr_states,
        train_targets=tr_targets,
        test_states=te_states,
        test_targets=te_targets,
        grid_version="grid_v3",
    )

    r2_seq = {}
    for r in rows:
        if r["metric"] == "r2":
            r2_seq[r["model"]] = float(r["value"])

    print("\nSequential single-process re-evaluated values:")
    for m in ["PQK-2nn", "FQ"]:
        print(f"  {m}: {r2_seq.get(m, 'MISSING')}")

    diffs = {}
    for m in ["PQK-2nn", "FQ"]:
        val_m = r2_merged[m]
        val_s = r2_seq[m]
        diff = abs(val_s - val_m)
        diffs[m] = diff
        print(f"\nModel: {m}")
        print(f"  R2_merged     = {val_m:.16f}")
        print(f"  R2_sequential = {val_s:.16f}")
        print(f"  |diff|        = {diff:.2e}")

    max_diff = max(diffs.values())
    print(f"\nMaximum difference: {max_diff:.2e}")

    if max_diff >= 1e-10:
        print("\nERROR: max |diff| >= 1e-10! Worker seed assignments:")
        print("  Worker 1: Seeds 3-6")
        print("  Worker 2: Seeds 7-10")
        print("  Worker 3: Seeds 11-14")
        print("  Worker 4: Seeds 15-19")
        sys.exit(1)

    print("\nSUCCESS: max |diff| < 1e-10. RNG Stream Audit PASSED.")
    return max_diff

if __name__ == "__main__":
    verify_seed3()
