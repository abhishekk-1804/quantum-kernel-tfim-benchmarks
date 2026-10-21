"""
scripts/compute_grid_boundary.py
--------------------------------
Audit check for Phase 2a.1:
Compute for each (task, target, model, variant, N_train) the fraction of seeds
whose best C or best c sits at the lowest or highest grid value.
Write to results/grid_boundary.csv.
Report any main arm with >30% at an edge.
Do NOT rerun anything.
"""

import os
import json
import csv
import pandas as pd
import numpy as np

C_MIN, C_MAX = 0.1, 100.0
c_MIN, c_MAX = 0.1, 10.0
ALPHA_MIN, ALPHA_MAX = 0.0001, 100.0

MAIN_ARMS = [
    "PQK-1 (== RBF on <X>)",
    "PQK-2nn",
    "FQ",
    "E",
    "F",
]

def analyze_grid_boundaries():
    csv_paths = [
        os.path.join("results", "t1_entropy.csv"),
        os.path.join("results", "t2_correlators.csv"),
    ]

    records = []
    high_edge_reports = []

    for path in csv_paths:
        if not os.path.exists(path):
            continue
        df = pd.read_csv(path)
        # Use r2 metric rows to examine parameters (each seed has 1 best_param per model/N)
        df_r2 = df[df["metric"] == "r2"]

        group_cols = ["task", "target", "model", "variant", "N_train"]
        for keys, group in df_r2.groupby(group_cols, sort=False):
            task, target, model, variant, N = keys
            n_seeds = len(group)
            
            c_edge_count = 0
            factor_c_edge_count = 0
            alpha_edge_count = 0
            any_edge_count = 0

            for _, row in group.iterrows():
                p_str = row["best_params"]
                if not p_str or p_str == "{}":
                    continue
                try:
                    params = json.loads(p_str)
                except Exception:
                    continue

                is_edge = False

                # C check
                if "C" in params:
                    val_C = float(params["C"])
                    if np.isclose(val_C, C_MIN) or np.isclose(val_C, C_MAX):
                        c_edge_count += 1
                        is_edge = True

                # c factor check
                if "c" in params:
                    val_c = float(params["c"])
                    if np.isclose(val_c, c_MIN) or np.isclose(val_c, c_MAX):
                        factor_c_edge_count += 1
                        is_edge = True

                # alpha check (for Ridge F)
                if "alpha" in params:
                    val_a = float(params["alpha"])
                    if np.isclose(val_a, ALPHA_MIN) or np.isclose(val_a, ALPHA_MAX):
                        alpha_edge_count += 1
                        is_edge = True

                if is_edge:
                    any_edge_count += 1

            frac_any = any_edge_count / n_seeds if n_seeds > 0 else 0.0
            frac_C = c_edge_count / n_seeds if n_seeds > 0 else 0.0
            frac_c = factor_c_edge_count / n_seeds if n_seeds > 0 else 0.0
            frac_alpha = alpha_edge_count / n_seeds if n_seeds > 0 else 0.0

            rec = {
                "task": task,
                "target": target,
                "model": model,
                "variant": variant,
                "N_train": N,
                "num_seeds": n_seeds,
                "frac_any_edge": frac_any,
                "frac_C_edge": frac_C,
                "frac_c_factor_edge": frac_c,
                "frac_alpha_edge": frac_alpha,
            }
            records.append(rec)

            if model in MAIN_ARMS and frac_any > 0.30:
                high_edge_reports.append((task, target, model, variant, N, frac_any, frac_C, frac_c, frac_alpha))

    out_csv = os.path.join("results", "grid_boundary.csv")
    fieldnames = [
        "task", "target", "model", "variant", "N_train", "num_seeds",
        "frac_any_edge", "frac_C_edge", "frac_c_factor_edge", "frac_alpha_edge"
    ]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            writer.writerow(r)

    print(f"Wrote {len(records)} records to {out_csv}.")
    print(f"\n=== Main arms with >30% seeds at grid boundary ===")
    if not high_edge_reports:
        print("None! All main arms have <=30% at grid edges.")
    else:
        print(f"{'Task':5s} | {'Target':18s} | {'Model':22s} | {'Var':5s} | {'N':4s} | {'AnyEdge':7s} | {'C_Edge':7s} | {'c_Edge':7s} | {'Alpha_Edge':10s}")
        print("-" * 95)
        for r in high_edge_reports:
            print(f"{r[0]:5s} | {r[1]:18s} | {r[2]:22s} | {r[3]:5s} | {r[4]:4d} | {r[5]:6.1%} | {r[6]:6.1%} | {r[7]:6.1%} | {r[8]:6.1%}")

if __name__ == "__main__":
    analyze_grid_boundaries()
