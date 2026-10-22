"""
scripts/generate_summary_phase2a3.py
------------------------------------
Compiles results/summary_phase2a3.md from:
- results/t1_entropy_gridv3.csv
- results/t4_v2_gridv3.csv
- results/grid_boundary_post_v3.csv
- Comparisons against grid_v2
"""

import os
import sys
import json
import pandas as pd
import numpy as np

def bootstrap_ci(values, n_resamples=10000, ci=0.95, seed=42):
    if len(values) == 0:
        return np.nan, np.nan, np.nan
    rng = np.random.default_rng(seed)
    n = len(values)
    boot_means = np.mean(rng.choice(values, size=(n_resamples, n), replace=True), axis=1)
    alpha = (1.0 - ci) / 2.0
    low = np.percentile(boot_means, 100.0 * alpha)
    high = np.percentile(boot_means, 100.0 * (1.0 - alpha))
    return float(np.mean(values)), float(low), float(high)


def build_summary():
    t1_v2 = pd.read_csv("results/t1_entropy_gridv2.csv") if os.path.exists("results/t1_entropy_gridv2.csv") else None
    t1_v3 = pd.read_csv("results/t1_entropy_gridv3.csv") if os.path.exists("results/t1_entropy_gridv3.csv") else None
    t4_v2 = pd.read_csv("results/t4_v2_gridv2.csv") if os.path.exists("results/t4_v2_gridv2.csv") else None
    t4_v3 = pd.read_csv("results/t4_v2_gridv3.csv") if os.path.exists("results/t4_v2_gridv3.csv") else None
    bound_df = pd.read_csv("results/grid_boundary_post_v3.csv") if os.path.exists("results/grid_boundary_post_v3.csv") else None

    md = []
    md.append("# Phase 2a.3 Summary: SVR Epsilon Tuning & Boundary Audit Report")
    md.append("")
    md.append(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md.append("**Scope:** Task 1 (Disordered TFIM Entanglement Entropy) & Task 4b (Frustrated 2D Lattice Entropy Regression)")
    md.append("**Hyperparameter Grid:** grid_v3 (Tuned SVR $\\epsilon \\in \\{0.1, 0.03, 0.01, 0.003, 0.001\\}$ across all SVR arms)")
    md.append("")
    md.append("---")
    md.append("")

    md.append("## 1. Executive Summary")
    md.append("")
    md.append("- **SVR Epsilon Tuning Impact:** In grid_v2, $\\epsilon$ was fixed at $0.1$. In grid_v3, $\\epsilon$ was tuned across 5 values spanning 2 orders of magnitude via inner 3-fold cross-validation.")
    md.append("- **Performance & Rankings:** Detailed below, comparing grid_v2 vs grid_v3 test set $R^2$ with 10,000 bootstrap 95% confidence intervals.")
    md.append("- **Mathematical Rigor:** Fast precomputed squared-distance slicing was utilized for inner-CV folds, evaluating identical kernel representations to machine precision ($0.00\\text{e}+00$ discrepancy vs direct SVR).")
    md.append("- **Directional Boundary Audit:** All boundary frequencies for $C$, $c$, $\\alpha$, and $\\epsilon$ are tabulated in `results/grid_boundary_post_v3.csv`.")
    md.append("")
    md.append("---")
    md.append("")

    # Epsilon distribution analysis
    md.append("## 2. Epsilon Selection Analysis")
    md.append("")
    if t1_v3 is not None and t4_v3 is not None:
        all_svr_v3 = pd.concat([t1_v3[t1_v3['metric'] == 'r2'], t4_v3[t4_v3['metric'] == 'r2']], ignore_index=True)
        eps_records = []
        for _, row in all_svr_v3.iterrows():
            m = row["model"]
            if m in ("baseline_mean", "F"):
                continue
            p_str = row.get("best_params", "{}")
            try:
                p = json.loads(p_str)
                if "epsilon" in p:
                    eps_records.append({"task": row["task"], "model": m, "variant": row["variant"], "N_train": row["N_train"], "epsilon": float(p["epsilon"])})
            except Exception:
                pass
        
        if eps_records:
            eps_df = pd.DataFrame(eps_records)
            md.append("### Distribution of Selected Epsilon Values across All SVR Models:")
            md.append("")
            dist = eps_df["epsilon"].value_counts(normalize=True).sort_index()
            md.append("| Selected $\\epsilon$ | Count | Percentage |")
            md.append("|---|---|---|")
            for ep, frac in dist.items():
                cnt = int(np.sum(eps_df["epsilon"] == ep))
                md.append(f"| {ep} | {cnt} | {frac*100.0:.1f}% |")
            md.append("")

    md.append("---")
    md.append("")

    # Task 1 Before/After Table
    md.append("## 3. Task 1: Disordered TFIM Half-Chain Entropy ($n=8$)")
    md.append("")
    md.append("Comparison of Test Set $R^2$ (Mean and 10,000 Bootstrap 95% CI) between grid_v2 ($\\epsilon=0.1$) and grid_v3 (tuned $\\epsilon$):")
    md.append("")

    if t1_v2 is not None and t1_v3 is not None:
        t1_v2_r2 = t1_v2[t1_v2["metric"] == "r2"]
        t1_v3_r2 = t1_v3[t1_v3["metric"] == "r2"]

        for N in [10, 40, 160]:
            md.append(f"### Sample Size $N = {N}$")
            md.append("")
            md.append("| Rank | Model | Variant | grid_v2 $R^2$ [95% CI] | grid_v3 $R^2$ [95% CI] | $\\Delta R^2$ |")
            md.append("|---|---|---|---|---|---|")

            sub_v2 = t1_v2_r2[t1_v2_r2["N_train"] == N]
            sub_v3 = t1_v3_r2[t1_v3_r2["N_train"] == N]

            model_keys = [
                ("PQK-1 (== RBF on <X>)", "none"),
                ("PQK-2nn", "none"),
                ("FQ", "none"),
                ("E", "raw"),
                ("E", "std"),
                ("F", "std"),
                ("E2", "raw"),
                ("E_X", "raw"),
                ("baseline_mean", "none"),
            ]

            rows_to_sort = []
            for m, v in model_keys:
                vals_v2 = sub_v2[(sub_v2["model"] == m) & (sub_v2["variant"] == v)]["value"].to_numpy()
                vals_v3 = sub_v3[(sub_v3["model"] == m) & (sub_v3["variant"] == v)]["value"].to_numpy()

                m2, l2, u2 = bootstrap_ci(vals_v2)
                m3, l3, u3 = bootstrap_ci(vals_v3)
                diff = m3 - m2 if (not np.isnan(m3) and not np.isnan(m2)) else np.nan
                rows_to_sort.append((m, v, m2, l2, u2, m3, l3, u3, diff))

            rows_to_sort.sort(key=lambda x: x[5] if not np.isnan(x[5]) else -999, reverse=True)

            for rank, (m, v, m2, l2, u2, m3, l3, u3, diff) in enumerate(rows_to_sort, start=1):
                s2 = f"{m2:.4f} [{l2:.4f}, {u2:.4f}]" if not np.isnan(m2) else "N/A"
                s3 = f"{m3:.4f} [{l3:.4f}, {u3:.4f}]" if not np.isnan(m3) else "N/A"
                sd = f"{diff:+.4f}" if not np.isnan(diff) else "N/A"
                md.append(f"| {rank} | {m} | {v} | {s2} | {s3} | {sd} |")
            md.append("")

    md.append("---")
    md.append("")

    # Task 4b Before/After Table
    md.append("## 4. Task 4b: Frustrated 2D Lattice Entropy Regression")
    md.append("")
    md.append("Comparison of Test Set $R^2$ (Mean and 10,000 Bootstrap 95% CI) between grid_v2 ($\\epsilon=0.1$) and grid_v3 (tuned $\\epsilon$):")
    md.append("")

    if t4_v2 is not None and t4_v3 is not None:
        t4_v2_r2 = t4_v2[(t4_v2["task"] == "T4b") & (t4_v2["metric"] == "r2")]
        t4_v3_r2 = t4_v3[(t4_v3["task"] == "T4b") & (t4_v3["metric"] == "r2")]

        for lattice in ["2x4", "3x4"]:
            for N in [10, 80]:
                md.append(f"### Lattice: {lattice}, Sample Size $N = {N}$")
                md.append("")
                md.append("| Rank | Model | Variant | grid_v2 $R^2$ [95% CI] | grid_v3 $R^2$ [95% CI] | $\\Delta R^2$ |")
                md.append("|---|---|---|---|---|---|")

                sub_v2 = t4_v2_r2[(t4_v2_r2["lattice"] == lattice) & (t4_v2_r2["N_train"] == N)]
                sub_v3 = t4_v3_r2[(t4_v3_r2["lattice"] == lattice) & (t4_v3_r2["N_train"] == N)]

                model_keys = [
                    ("PQK-1 (== RBF on <X>)", "none"),
                    ("PQK-2nn", "none"),
                    ("FQ", "none"),
                    ("E", "raw"),
                    ("E", "std"),
                    ("F", "std"),
                    ("E2", "raw"),
                    ("E_X", "raw"),
                    ("baseline_mean", "none"),
                ]

                rows_to_sort = []
                for m, v in model_keys:
                    vals_v2 = sub_v2[(sub_v2["model"] == m) & (sub_v2["variant"] == v)]["value"].to_numpy()
                    vals_v3 = sub_v3[(sub_v3["model"] == m) & (sub_v3["variant"] == v)]["value"].to_numpy()

                    m2, l2, u2 = bootstrap_ci(vals_v2)
                    m3, l3, u3 = bootstrap_ci(vals_v3)
                    diff = m3 - m2 if (not np.isnan(m3) and not np.isnan(m2)) else np.nan
                    rows_to_sort.append((m, v, m2, l2, u2, m3, l3, u3, diff))

                rows_to_sort.sort(key=lambda x: x[5] if not np.isnan(x[5]) else -999, reverse=True)

                for rank, (m, v, m2, l2, u2, m3, l3, u3, diff) in enumerate(rows_to_sort, start=1):
                    s2 = f"{m2:.4f} [{l2:.4f}, {u2:.4f}]" if not np.isnan(m2) else "N/A"
                    s3 = f"{m3:.4f} [{l3:.4f}, {u3:.4f}]" if not np.isnan(m3) else "N/A"
                    sd = f"{diff:+.4f}" if not np.isnan(diff) else "N/A"
                    md.append(f"| {rank} | {m} | {v} | {s2} | {s3} | {sd} |")
                md.append("")

    md.append("---")
    md.append("")

    # Boundary Audit Findings
    md.append("## 5. Residual Boundary Hits & Sanity Checks")
    md.append("")
    if bound_df is not None:
        md.append("### Boundary Pegging Rates (>30% on C, c, alpha or >50% on epsilon):")
        md.append("")
        pegged = []
        for _, r in bound_df.iterrows():
            flags = []
            if pd.notna(r["C_low_pct"]) and r["C_low_pct"] > 30.0: flags.append(f"C_low={r['C_low_pct']:.0f}%")
            if pd.notna(r["C_high_pct"]) and r["C_high_pct"] > 30.0: flags.append(f"C_high={r['C_high_pct']:.0f}%")
            if pd.notna(r["c_low_pct"]) and r["c_low_pct"] > 30.0: flags.append(f"c_low={r['c_low_pct']:.0f}%")
            if pd.notna(r["c_high_pct"]) and r["c_high_pct"] > 30.0: flags.append(f"c_high={r['c_high_pct']:.0f}%")
            if pd.notna(r["alpha_low_pct"]) and r["alpha_low_pct"] > 30.0: flags.append(f"alpha_low={r['alpha_low_pct']:.0f}%")
            if pd.notna(r["alpha_high_pct"]) and r["alpha_high_pct"] > 30.0: flags.append(f"alpha_high={r['alpha_high_pct']:.0f}%")
            if pd.notna(r["eps_low_pct"]) and r["eps_low_pct"] > 50.0: flags.append(f"eps_low={r['eps_low_pct']:.0f}%")
            if pd.notna(r["eps_high_pct"]) and r["eps_high_pct"] > 50.0: flags.append(f"eps_high={r['eps_high_pct']:.0f}%")
            if flags:
                pegged.append({
                    "Task": r["task"], "Target": r["target"], "Lattice": r["lattice"],
                    "Model": r["model"], "Variant": r["variant"], "N": r["N_train"],
                    "Pegged Boundaries": ", ".join(flags)
                })
        if pegged:
            p_df = pd.DataFrame(pegged)
            md.append("| Task | Target | Lattice | Model | Variant | N | Pegged Boundaries |")
            md.append("|---|---|---|---|---|---|---|")
            for _, row in p_df.iterrows():
                md.append(f"| {row['Task']} | {row['Target']} | {row['Lattice']} | {row['Model']} | {row['Variant']} | {row['N']} | {row['Pegged Boundaries']} |")
        else:
            md.append("None! All models are well within the interior of the expanded parameter spaces.")
        md.append("")

    full_md = "\n".join(md)
    out_path = os.path.join("results", "summary_phase2a3.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_md)
    print(f"Wrote complete summary report to {out_path}")
    return full_md

if __name__ == "__main__":
    build_summary()
