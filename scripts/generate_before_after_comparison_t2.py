"""
scripts/generate_before_after_comparison_t2.py
----------------------------------------------
Generates side-by-side Before/After performance comparisons for Task 2:
grid_v2 (fixed epsilon=0.1) vs grid_v3 (tuned epsilon in {0.1, 0.03, 0.01, 0.003, 0.001})
Uses 10,000 bootstrap resamples for 95% confidence intervals and evaluates model rank shifts.
"""

import os
import sys
import pandas as pd
import numpy as np

def bootstrap_ci(values, n_resamples=10000, ci=0.95, seed=42):
    """Compute bootstrap mean and percentile confidence interval."""
    if len(values) == 0:
        return np.nan, np.nan, np.nan
    rng = np.random.default_rng(seed)
    n = len(values)
    boot_means = np.mean(rng.choice(values, size=(n_resamples, n), replace=True), axis=1)
    alpha = (1.0 - ci) / 2.0
    low = np.percentile(boot_means, 100.0 * alpha)
    high = np.percentile(boot_means, 100.0 * (1.0 - alpha))
    return float(np.mean(values)), float(low), float(high)


def generate_t2_comparison():
    t2_v2_path = os.path.join("results", "t2_correlators_gridv2.csv")
    t2_v3_path = os.path.join("results", "t2_correlators_gridv3.csv")

    if not os.path.exists(t2_v2_path) or not os.path.exists(t2_v3_path):
        print(f"Error: {t2_v2_path} or {t2_v3_path} not found.")
        return

    df_v2 = pd.read_csv(t2_v2_path)
    df_v3 = pd.read_csv(t2_v3_path)

    df_v2_r2 = df_v2[df_v2["metric"] == "r2"]
    df_v3_r2 = df_v3[df_v3["metric"] == "r2"]

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

    target_configs = [
        ("T2a", "z0_zn", "<Z_0 Z_{n-1}> (contained)"),
        ("T2b", "z0_z1_zn2_zn1", "<Z_0 Z_1 Z_{n-2} Z_{n-1}> (not_contained)"),
    ]

    lines = []
    lines.append("=" * 110)
    lines.append("TASK 2 BEFORE/AFTER COMPARISON: grid_v2 (eps=0.1) vs. grid_v3 (tuned eps)")
    lines.append("=" * 110)

    for task_name, target_name, desc in target_configs:
        lines.append(f"\nTarget: {task_name} - {desc}")
        lines.append("=" * 110)

        for N in [10, 40, 160]:
            lines.append(f"\n--- Training Set Size N = {N} ---")
            header = f"{'Rank':<5} {'Model':<25} {'Variant':<8} {'grid_v2 R2 [95% CI]':<32} {'grid_v3 R2 [95% CI]':<32} {'Delta':<10}"
            lines.append(header)
            lines.append("-" * 110)

            sub_v2 = df_v2_r2[(df_v2_r2["task"] == task_name) & (df_v2_r2["N_train"] == N)]
            sub_v3 = df_v3_r2[(df_v3_r2["task"] == task_name) & (df_v3_r2["N_train"] == N)]

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
                str_v2 = f"{m2:7.4f} [{l2:7.4f}, {u2:7.4f}]" if not np.isnan(m2) else "N/A"
                str_v3 = f"{m3:7.4f} [{l3:7.4f}, {u3:7.4f}]" if not np.isnan(m3) else "N/A"
                str_diff = f"{diff:+7.4f}" if not np.isnan(diff) else "N/A"
                lines.append(f"{rank:<5} {m:<25} {v:<8} {str_v2:<32} {str_v3:<32} {str_diff:<10}")

    report_text = "\n".join(lines)
    print(report_text)
    return report_text

if __name__ == "__main__":
    generate_t2_comparison()
