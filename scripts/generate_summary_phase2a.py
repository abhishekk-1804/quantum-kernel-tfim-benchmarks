"""
scripts/generate_summary_phase2a.py
-----------------------------------
Compute Mean +/- 95% Bootstrap CI (10,000 resamples over seeds)
for Phase 2a noiseless benchmark results.

Output: results/summary_phase2a.md (Strictly numbers and tables only. No prose, no interpretation).
"""

import os
import glob
import numpy as np
import pandas as pd


def bootstrap_ci(values: np.ndarray, n_boot: int = 10000, ci: float = 0.95, seed: int = 42) -> tuple:
    """Compute mean and 95% bootstrap confidence interval over seeds."""
    if len(values) == 0:
        return np.nan, np.nan, np.nan
    rng = np.random.default_rng(seed)
    mean_val = float(np.mean(values))
    if len(values) == 1:
        return mean_val, mean_val, mean_val
    # Resample with replacement
    boot_indices = rng.integers(0, len(values), size=(n_boot, len(values)))
    boot_means = np.mean(values[boot_indices], axis=1)
    alpha = (1.0 - ci) / 2.0
    ci_lower = float(np.percentile(boot_means, 100.0 * alpha))
    ci_upper = float(np.percentile(boot_means, 100.0 * (1.0 - alpha)))
    return mean_val, ci_lower, ci_upper


def summarize_regression_and_classification(csv_path: str, extra_group_cols: list = None) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    group_cols = ["task", "target", "tag"]
    if extra_group_cols:
        group_cols.extend([c for c in extra_group_cols if c in df.columns])
    group_cols.extend(["n", "N_train", "model", "variant", "metric"])

    records = []
    for keys, sub_df in df.groupby(group_cols, sort=False):
        vals = sub_df["value"].to_numpy(dtype=float)
        mean_val, ci_l, ci_u = bootstrap_ci(vals)
        d = dict(zip(group_cols, keys))
        d["num_seeds"] = len(vals)
        d["mean"] = mean_val
        d["ci_95_lower"] = ci_l
        d["ci_95_upper"] = ci_u
        records.append(d)
    return pd.DataFrame(records)


def summarize_concentration(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    group_cols = ["task", "tag", "n", "hilbert_dim", "kernel", "gamma_rule"]
    records = []
    for keys, sub_df in df.groupby(group_cols, sort=False):
        for metric_col in ["off_diag_mean", "off_diag_var"]:
            vals = sub_df[metric_col].to_numpy(dtype=float)
            mean_val, ci_l, ci_u = bootstrap_ci(vals)
            d = dict(zip(group_cols, keys))
            d["metric"] = metric_col
            d["num_seeds"] = len(vals)
            d["mean"] = mean_val
            d["ci_95_lower"] = ci_l
            d["ci_95_upper"] = ci_u
            records.append(d)
    return pd.DataFrame(records)


def df_to_markdown_simple(df: pd.DataFrame) -> str:
    headers = [str(c) for c in df.columns]
    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    rows = []
    for _, row in df.iterrows():
        formatted_vals = []
        for v in row:
            if isinstance(v, float):
                formatted_vals.append(f"{v:.6g}")
            else:
                formatted_vals.append(str(v))
        rows.append("| " + " | ".join(formatted_vals) + " |")
    return "\n".join([header_line, separator_line] + rows)


def main():
    results_dir = "results"
    out_md = os.path.join(results_dir, "summary_phase2a.md")

    lines = []
    lines.append("# Phase 2a Summary Statistics (10,000 Bootstrap Resamples over Seeds)\n\n")

    # 1. T1 Entropy
    t1_csv = os.path.join(results_dir, "t1_entropy.csv")
    if os.path.exists(t1_csv):
        lines.append("## Task 1: Disordered TFIM Half-Chain Entropy (n=8)\n\n")
        df_t1 = summarize_regression_and_classification(t1_csv)
        lines.append(df_to_markdown_simple(df_t1))
        lines.append("\n\n")

    # 2. T2 Correlators
    t2_csv = os.path.join(results_dir, "t2_correlators.csv")
    if os.path.exists(t2_csv):
        lines.append("## Task 2: Disordered TFIM Correlators (T2a Contained, T2b Not Contained, n=8)\n\n")
        df_t2 = summarize_regression_and_classification(t2_csv)
        lines.append(df_to_markdown_simple(df_t2))
        lines.append("\n\n")

    # 3. T3 Concentration
    t3_csv = os.path.join(results_dir, "t3_concentration.csv")
    if os.path.exists(t3_csv):
        lines.append("## Task 3: Kernel Concentration Diagnostics\n\n")
        df_t3 = summarize_concentration(t3_csv)
        lines.append(df_to_markdown_simple(df_t3))
        lines.append("\n\n")

    # 4. T4 Frustrated Lattice
    t4_csv = os.path.join(results_dir, "t4_frustrated.csv")
    if os.path.exists(t4_csv):
        lines.append("## Task 4: Frustrated 2D Lattice (2x4, J1=-1.0)\n\n")
        df_t4_raw = pd.read_csv(t4_csv)
        extra = ["J2"] if "J2" in df_t4_raw.columns else []
        df_t4 = summarize_regression_and_classification(t4_csv, extra_group_cols=extra)
        lines.append(df_to_markdown_simple(df_t4))
        lines.append("\n\n")

    # 5. T4 Class Balance
    t4_cb_csv = os.path.join(results_dir, "t4_class_balance.csv")
    if os.path.exists(t4_cb_csv):
        lines.append("## Task 4: Class Balance Records\n\n")
        df_cb = pd.read_csv(t4_cb_csv)
        lines.append(df_to_markdown_simple(df_cb))
        lines.append("\n")

    with open(out_md, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Summary markdown written to {out_md} ({os.path.getsize(out_md)} bytes).")


if __name__ == "__main__":
    main()
