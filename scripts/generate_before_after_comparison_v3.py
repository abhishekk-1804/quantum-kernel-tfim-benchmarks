"""
scripts/generate_before_after_comparison_v3.py
----------------------------------------------
Generates side-by-side Before/After performance comparisons:
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


def generate_comparison_report():
    t1_v2_path = os.path.join("results", "t1_entropy_gridv2.csv")
    t1_v3_path = os.path.join("results", "t1_entropy_gridv3.csv")
    t4_v2_path = os.path.join("results", "t4_v2_gridv2.csv")
    t4_v3_path = os.path.join("results", "t4_v2_gridv3.csv")

    output_lines = []

    # ─────────────────────────────────────────────────────────────────────────
    # Task 1: Disordered TFIM Half-Chain Entropy
    # ─────────────────────────────────────────────────────────────────────────
    output_lines.append("=" * 105)
    output_lines.append("TASK 1: Disordered TFIM Half-Chain Entropy (n=8, Metric: R2)")
    output_lines.append("=" * 105)

    if os.path.exists(t1_v2_path) and os.path.exists(t1_v3_path):
        df1_v2 = pd.read_csv(t1_v2_path)
        df1_v3 = pd.read_csv(t1_v3_path)

        df1_v2_r2 = df1_v2[df1_v2["metric"] == "r2"]
        df1_v3_r2 = df1_v3[df1_v3["metric"] == "r2"]

        target_N_t1 = [10, 40, 160]

        for N in target_N_t1:
            output_lines.append(f"\n--- Training Set Size N = {N} ---")
            header = f"{'Model':<25} {'Variant':<8} {'grid_v2 R2 [95% CI]':<32} {'grid_v3 R2 [95% CI]':<32} {'Delta':<10}"
            output_lines.append(header)
            output_lines.append("-" * 105)

            sub_v2 = df1_v2_r2[df1_v2_r2["N_train"] == N]
            sub_v3 = df1_v3_r2[df1_v3_r2["N_train"] == N]

            # Models to evaluate
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

            # Sort by grid_v3 mean descending
            rows_to_sort.sort(key=lambda x: x[5] if not np.isnan(x[5]) else -999, reverse=True)

            for rank, (m, v, m2, l2, u2, m3, l3, u3, diff) in enumerate(rows_to_sort, start=1):
                str_v2 = f"{m2:7.4f} [{l2:7.4f}, {u2:7.4f}]" if not np.isnan(m2) else "N/A"
                str_v3 = f"{m3:7.4f} [{l3:7.4f}, {u3:7.4f}]" if not np.isnan(m3) else "N/A"
                str_diff = f"{diff:+7.4f}" if not np.isnan(diff) else "N/A"
                output_lines.append(f"{m:<25} {v:<8} {str_v2:<32} {str_v3:<32} {str_diff:<10}")

    # ─────────────────────────────────────────────────────────────────────────
    # Task 4b: Frustrated 2D Lattice Entropy Regression
    # ─────────────────────────────────────────────────────────────────────────
    output_lines.append("\n" + "=" * 105)
    output_lines.append("TASK 4b: Frustrated 2D Lattice Entropy Regression (Metric: R2)")
    output_lines.append("=" * 105)

    if os.path.exists(t4_v2_path) and os.path.exists(t4_v3_path):
        df4_v2 = pd.read_csv(t4_v2_path)
        df4_v3 = pd.read_csv(t4_v3_path)

        df4_v2_r2 = df4_v2[(df4_v2["task"] == "T4b") & (df4_v2["metric"] == "r2")]
        df4_v3_r2 = df4_v3[(df4_v3["task"] == "T4b") & (df4_v3["metric"] == "r2")]

        for lattice in ["2x4", "3x4"]:
            for N in [10, 80]:
                output_lines.append(f"\n--- Lattice: {lattice}, Training Set Size N = {N} ---")
                header = f"{'Model':<25} {'Variant':<8} {'grid_v2 R2 [95% CI]':<32} {'grid_v3 R2 [95% CI]':<32} {'Delta':<10}"
                output_lines.append(header)
                output_lines.append("-" * 105)

                sub_v2 = df4_v2_r2[(df4_v2_r2["lattice"] == lattice) & (df4_v2_r2["N_train"] == N)]
                sub_v3 = df4_v3_r2[(df4_v3_r2["lattice"] == lattice) & (df4_v3_r2["N_train"] == N)]

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
                    str_v2 = f"{m2:7.4f} [{l2:7.4f}, {u2:7.4f}]" if not np.isnan(m2) else "N/A"
                    str_v3 = f"{m3:7.4f} [{l3:7.4f}, {u3:7.4f}]" if not np.isnan(m3) else "N/A"
                    str_diff = f"{diff:+7.4f}" if not np.isnan(diff) else "N/A"
                    output_lines.append(f"{m:<25} {v:<8} {str_v2:<32} {str_v3:<32} {str_diff:<10}")

    report_text = "\n".join(output_lines)
    print(report_text)
    return report_text

if __name__ == "__main__":
    generate_comparison_report()
