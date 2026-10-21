"""
scripts/audit_post_rerun_edges.py
---------------------------------
Post-rerun directional edge audit for Phase 2a.2 (grid_v2).
Evaluates boundary selection on widened grids:
- C: [0.01, 10000.0]
- c: [0.01, 100.0] (for E std: [0.001, 100.0])
- alpha: [1e-8, 100.0]
Outputs results/grid_boundary_post_v2.csv.
"""

import os
import sys
import json
import csv
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import common

def run_post_rerun_audit():
    csv_paths = [
        os.path.join("results", "t1_entropy_gridv2.csv"),
        os.path.join("results", "t2_correlators_gridv2.csv"),
        os.path.join("results", "t4_v2_gridv2.csv"),
    ]
    out_csv = os.path.join("results", "grid_boundary_post_v2.csv")

    C_min = float(np.min(common.C_GRID_V2))
    C_max = float(np.max(common.C_GRID_V2))
    c_raw_min = float(np.min(common.C_FACTORS_V2))
    c_raw_max = float(np.max(common.C_FACTORS_V2))
    c_std_min = float(np.min(common.C_FACTORS_STD_V2))
    c_std_max = float(np.max(common.C_FACTORS_STD_V2))
    alpha_min = float(np.min(common.ALPHA_GRID_V2))
    alpha_max = float(np.max(common.ALPHA_GRID_V2))

    print("Post-Rerun Widened Grid Bounds:")
    print(f"  C: [{C_min}, {C_max}]")
    print(f"  c (raw / PQK): [{c_raw_min}, {c_raw_max}]")
    print(f"  c (E std): [{c_std_min}, {c_std_max}]")
    print(f"  alpha: [{alpha_min:.1e}, {alpha_max:.1e}]")
    print("-" * 80)

    records = []

    for path in csv_paths:
        if not os.path.exists(path):
            print(f"Warning: File not found: {path}")
            continue

        df = pd.read_csv(path)
        if "metric" in df.columns:
            df_unique = df[df["metric"].isin(["r2", "accuracy"])]
        else:
            df_unique = df

        group_cols = ["task", "target", "model", "variant", "N_train"]
        if "lattice" in df_unique.columns:
            group_cols.insert(2, "lattice")

        for keys, group in df_unique.groupby(group_cols, sort=False):
            if "lattice" in group_cols:
                task, target, lattice, model, variant, N = keys
            else:
                task, target, model, variant, N = keys
                lattice = "none"

            n_seeds = len(group)
            if n_seeds == 0:
                continue

            c_min_val = c_std_min if variant == "std" and model in ("E", "E (std)") else c_raw_min
            c_max_val = c_std_max if variant == "std" and model in ("E", "E (std)") else c_raw_max

            c_low_cnt = 0
            c_high_cnt = 0
            factor_low_cnt = 0
            factor_high_cnt = 0
            alpha_low_cnt = 0
            alpha_high_cnt = 0

            has_C = False
            has_c = False
            has_alpha = False

            for _, row in group.iterrows():
                p_str = row.get("best_params", "")
                if not p_str or pd.isna(p_str) or p_str == "{}":
                    continue
                try:
                    params = json.loads(p_str)
                except Exception:
                    continue

                if "C" in params:
                    has_C = True
                    val_C = float(params["C"])
                    if np.isclose(val_C, C_min, rtol=1e-5, atol=1e-8):
                        c_low_cnt += 1
                    if np.isclose(val_C, C_max, rtol=1e-5, atol=1e-8):
                        c_high_cnt += 1

                if "c" in params:
                    has_c = True
                    val_c = float(params["c"])
                    if np.isclose(val_c, c_min_val, rtol=1e-5, atol=1e-8):
                        factor_low_cnt += 1
                    if np.isclose(val_c, c_max_val, rtol=1e-5, atol=1e-8):
                        factor_high_cnt += 1

                if "alpha" in params:
                    has_alpha = True
                    val_a = float(params["alpha"])
                    if np.isclose(val_a, alpha_min, rtol=1e-5, atol=1e-8):
                        alpha_low_cnt += 1
                    if np.isclose(val_a, alpha_max, rtol=1e-5, atol=1e-8):
                        alpha_high_cnt += 1

            c_low_pct = (c_low_cnt / n_seeds * 100.0) if has_C else np.nan
            c_high_pct = (c_high_cnt / n_seeds * 100.0) if has_C else np.nan
            factor_low_pct = (factor_low_cnt / n_seeds * 100.0) if has_c else np.nan
            factor_high_pct = (factor_high_cnt / n_seeds * 100.0) if has_c else np.nan
            alpha_low_pct = (alpha_low_cnt / n_seeds * 100.0) if has_alpha else np.nan
            alpha_high_pct = (alpha_high_cnt / n_seeds * 100.0) if has_alpha else np.nan

            rec = {
                "task": task,
                "target": target,
                "lattice": lattice,
                "model": model,
                "variant": variant,
                "N_train": N,
                "num_seeds": n_seeds,
                "C_low_pct": f"{c_low_pct:.1f}" if not np.isnan(c_low_pct) else "",
                "C_high_pct": f"{c_high_pct:.1f}" if not np.isnan(c_high_pct) else "",
                "c_low_pct": f"{factor_low_pct:.1f}" if not np.isnan(factor_low_pct) else "",
                "c_high_pct": f"{factor_high_pct:.1f}" if not np.isnan(factor_high_pct) else "",
                "alpha_low_pct": f"{alpha_low_pct:.1f}" if not np.isnan(alpha_low_pct) else "",
                "alpha_high_pct": f"{alpha_high_pct:.1f}" if not np.isnan(alpha_high_pct) else "",
            }
            records.append(rec)

    os.makedirs(os.path.dirname(os.path.abspath(out_csv)), exist_ok=True)
    fieldnames = [
        "task", "target", "lattice", "model", "variant", "N_train", "num_seeds",
        "C_low_pct", "C_high_pct", "c_low_pct", "c_high_pct", "alpha_low_pct", "alpha_high_pct"
    ]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            writer.writerow(r)

    print(f"Post-rerun boundary statistics written to {out_csv} ({len(records)} row groups).")
    return pd.DataFrame(records)

if __name__ == "__main__":
    run_post_rerun_audit()
