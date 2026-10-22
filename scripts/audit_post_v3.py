"""
scripts/audit_post_v3.py
------------------------
Post-run directional edge and sensitivity audit for Phase 2a.3 (grid_v3).
Evaluates boundary selection across all tuned hyperparameter axes:
- C: [0.01, 10000.0]
- c: [0.01, 100.0] (for E std: [0.001, 100.0])
- alpha: [1e-8, 100.0]
- epsilon: [0.001, 0.1]
Outputs results/grid_boundary_post_v3.csv and prints summary tables.
"""

import os
import sys
import json
import pandas as pd
import numpy as np

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import common

def run_post_v3_audit():
    csv_paths = [
        os.path.join("results", "t1_entropy_gridv3.csv"),
        os.path.join("results", "t4_v2_gridv3.csv"),
    ]
    out_csv = os.path.join("results", "grid_boundary_post_v3.csv")

    C_min = float(np.min(common.C_GRID_V2))
    C_max = float(np.max(common.C_GRID_V2))
    c_raw_min = float(np.min(common.C_FACTORS_V2))
    c_raw_max = float(np.max(common.C_FACTORS_V2))
    c_std_min = float(np.min(common.C_FACTORS_STD_V2))
    c_std_max = float(np.max(common.C_FACTORS_STD_V2))
    alpha_min = float(np.min(common.ALPHA_GRID_V2))
    alpha_max = float(np.max(common.ALPHA_GRID_V2))
    eps_min = float(np.min(common.EPSILON_GRID_V3))
    eps_max = float(np.max(common.EPSILON_GRID_V3))

    print("=" * 80)
    print("PHASE 2a.3 HYPERPARAMETER BOUNDARY AUDIT (grid_v3)")
    print("=" * 80)
    print(f"  C: [{C_min}, {C_max}]")
    print(f"  c (raw / PQK): [{c_raw_min}, {c_raw_max}]")
    print(f"  c (E std): [{c_std_min}, {c_std_max}]")
    print(f"  alpha: [{alpha_min:.1e}, {alpha_max:.1e}]")
    print(f"  epsilon: [{eps_min}, {eps_max}]")
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
            eps_low_cnt = 0
            eps_high_cnt = 0

            has_C = False
            has_c = False
            has_alpha = False
            has_eps = False

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
                    if np.isclose(val_C, C_min, rtol=1e-5):
                        c_low_cnt += 1
                    if np.isclose(val_C, C_max, rtol=1e-5):
                        c_high_cnt += 1

                if "c" in params:
                    has_c = True
                    val_c = float(params["c"])
                    if np.isclose(val_c, c_min_val, rtol=1e-5):
                        factor_low_cnt += 1
                    if np.isclose(val_c, c_max_val, rtol=1e-5):
                        factor_high_cnt += 1

                if "alpha" in params:
                    has_alpha = True
                    val_a = float(params["alpha"])
                    if np.isclose(val_a, alpha_min, rtol=1e-5):
                        alpha_low_cnt += 1
                    if np.isclose(val_a, alpha_max, rtol=1e-5):
                        alpha_high_cnt += 1

                if "epsilon" in params:
                    has_eps = True
                    val_eps = float(params["epsilon"])
                    if np.isclose(val_eps, eps_min, rtol=1e-5):
                        eps_low_cnt += 1
                    if np.isclose(val_eps, eps_max, rtol=1e-5):
                        eps_high_cnt += 1

            records.append({
                "task": task,
                "target": target,
                "lattice": lattice,
                "model": model,
                "variant": variant,
                "N_train": N,
                "n_seeds": n_seeds,
                "C_low_pct": (c_low_cnt / n_seeds * 100.0) if has_C else np.nan,
                "C_high_pct": (c_high_cnt / n_seeds * 100.0) if has_C else np.nan,
                "c_low_pct": (factor_low_cnt / n_seeds * 100.0) if has_c else np.nan,
                "c_high_pct": (factor_high_cnt / n_seeds * 100.0) if has_c else np.nan,
                "alpha_low_pct": (alpha_low_cnt / n_seeds * 100.0) if has_alpha else np.nan,
                "alpha_high_pct": (alpha_high_cnt / n_seeds * 100.0) if has_alpha else np.nan,
                "eps_low_pct": (eps_low_cnt / n_seeds * 100.0) if has_eps else np.nan,
                "eps_high_pct": (eps_high_cnt / n_seeds * 100.0) if has_eps else np.nan,
            })

    out_df = pd.DataFrame(records)
    out_df.to_csv(out_csv, index=False)
    print(f"Wrote audit results to {out_csv} ({len(out_df)} rows).")

    # Filter and display high boundary hits
    print("\n" + "=" * 95)
    print("RESIDUAL BOUNDARY HITS (>30% on C, c, alpha, or >50% on epsilon):")
    print("=" * 95)
    pegged = []
    for _, r in out_df.iterrows():
        reasons = []
        if pd.notna(r["C_low_pct"]) and r["C_low_pct"] > 30.0:
            reasons.append(f"C_low={r['C_low_pct']:.0f}%")
        if pd.notna(r["C_high_pct"]) and r["C_high_pct"] > 30.0:
            reasons.append(f"C_high={r['C_high_pct']:.0f}%")
        if pd.notna(r["c_low_pct"]) and r["c_low_pct"] > 30.0:
            reasons.append(f"c_low={r['c_low_pct']:.0f}%")
        if pd.notna(r["c_high_pct"]) and r["c_high_pct"] > 30.0:
            reasons.append(f"c_high={r['c_high_pct']:.0f}%")
        if pd.notna(r["alpha_low_pct"]) and r["alpha_low_pct"] > 30.0:
            reasons.append(f"alpha_low={r['alpha_low_pct']:.0f}%")
        if pd.notna(r["alpha_high_pct"]) and r["alpha_high_pct"] > 30.0:
            reasons.append(f"alpha_high={r['alpha_high_pct']:.0f}%")
        if pd.notna(r["eps_low_pct"]) and r["eps_low_pct"] > 50.0:
            reasons.append(f"eps_low={r['eps_low_pct']:.0f}%")
        if pd.notna(r["eps_high_pct"]) and r["eps_high_pct"] > 50.0:
            reasons.append(f"eps_high={r['eps_high_pct']:.0f}%")

        if reasons:
            pegged.append({
                "task": r["task"],
                "target": r["target"],
                "lattice": r["lattice"],
                "model": r["model"],
                "variant": r["variant"],
                "N_train": r["N_train"],
                "flags": ", ".join(reasons),
            })

    if pegged:
        pegged_df = pd.DataFrame(pegged)
        print(pegged_df.to_string(index=False))
    else:
        print("None! All models well within hyperparameter interior.")

    return out_df

if __name__ == "__main__":
    run_post_v3_audit()
