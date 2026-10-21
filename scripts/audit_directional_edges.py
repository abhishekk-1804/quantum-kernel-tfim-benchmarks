"""
scripts/audit_directional_edges.py
----------------------------------
Dynamic directional edge audit for hyperparameter selections in Phase 2a / 2a.1.
Dynamically reads active grid definitions from scripts/common.py (do not hardcode numeric bounds).
Outputs results/grid_boundary_v2.csv.
Checks Gate Stop Rule: If > 50% of the main arms sit pegged at the LOW edge for C or c,
warns and stops.
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

MAIN_ARMS = [
    "PQK-1 (== RBF on <X>)",
    "PQK-2nn",
    "FQ",
    "E",
    "F",
]

def run_directional_edge_audit(
    csv_paths: Optional[List[str]] = None,
    out_csv: Optional[str] = None
) -> pd.DataFrame:
    if csv_paths is None:
        csv_paths = [
            os.path.join("results", "t1_entropy.csv"),
            os.path.join("results", "t2_correlators.csv"),
            os.path.join("results", "t4_v2.csv"),
        ]
    if out_csv is None:
        out_csv = os.path.join("results", "grid_boundary_v2.csv")

    # Dynamically extract bounds from common.py
    C_min = float(np.min(common.C_GRID))
    C_max = float(np.max(common.C_GRID))
    c_min = float(np.min(common.C_FACTORS))
    c_max = float(np.max(common.C_FACTORS))
    alpha_min = float(np.min(common.ALPHA_GRID))
    alpha_max = float(np.max(common.ALPHA_GRID))

    print(f"Active Grid Bounds from common.py:")
    print(f"  C: [{C_min}, {C_max}] (values: {list(common.C_GRID)})")
    print(f"  c: [{c_min}, {c_max}] (values: {list(common.C_FACTORS)})")
    print(f"  alpha: [{alpha_min}, {alpha_max}] (min: {alpha_min:.1e}, max: {alpha_max:.1e})")
    print("-" * 80)

    records = []
    main_arm_low_pegged = []
    total_main_arm_groups = 0

    for path in csv_paths:
        if not os.path.exists(path):
            print(f"Warning: File not found, skipping: {path}")
            continue

        df = pd.read_csv(path)
        # Select representative metric to avoid duplicate counts per seed
        # For regression, metric 'r2'; for classification, metric 'accuracy'
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
                    if np.isclose(val_c, c_min, rtol=1e-5, atol=1e-8):
                        factor_low_cnt += 1
                    if np.isclose(val_c, c_max, rtol=1e-5, atol=1e-8):
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

            # Check Gate Stop Rule on main arms
            if model in MAIN_ARMS:
                total_main_arm_groups += 1
                pegged_low = False
                if has_C and (c_low_cnt / n_seeds) > 0.50:
                    pegged_low = True
                if has_c and (factor_low_cnt / n_seeds) > 0.50:
                    pegged_low = True
                if pegged_low:
                    main_arm_low_pegged.append((task, target, lattice, model, variant, N, c_low_pct, factor_low_pct))

    # Write CSV
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

    print(f"Directional edge audit written to {out_csv} ({len(records)} row groups).\n")

    # Print summary table
    df_rec = pd.DataFrame(records)
    print(df_rec.to_string(index=False))

    # Check Gate Stop Rule
    low_pegged_frac = len(main_arm_low_pegged) / float(total_main_arm_groups) if total_main_arm_groups > 0 else 0.0
    print("\n" + "=" * 80)
    print(f"GATE STOP AUDIT: {len(main_arm_low_pegged)} / {total_main_arm_groups} main arm groups ({low_pegged_frac:.1%}) pegged at LOW edge for C or c.")
    print("=" * 80)

    if low_pegged_frac > 0.50:
        print("\n[GATE STOP WARNING] > 50% of main arms sit pegged at the LOW edge for C or c!")
        print("List of low-pegged groups:")
        for item in main_arm_low_pegged:
            print(f"  {item[0]} | {item[1]} | {item[2]} | {item[3]} ({item[4]}) N={item[5]}: C_low={item[6]}%, c_low={item[7]}%")
        print("\nHALTING FOR HUMAN REVIEW.")
        sys.exit(1)
    else:
        print("[GATE PASS] <= 50% of main arms pegged at LOW edge. Proceeding permitted.")

    return df_rec

if __name__ == "__main__":
    run_directional_edge_audit()
