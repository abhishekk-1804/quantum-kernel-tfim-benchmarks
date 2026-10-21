"""
scripts/generate_summary_phase2a2.py
------------------------------------
Generate results/summary_phase2a2.md with 10,000 bootstrap resamples over seeds
for Phase 2a.2 (grid_v2) results.
Pure tables, numbers only, no interpretive prose.
"""

import os
import sys
import numpy as np
import pandas as pd


def bootstrap_ci(values: np.ndarray, n_boot: int = 10000, ci: float = 0.95, seed: int = 42) -> tuple:
    vals = np.asarray(values, dtype=float)
    vals = vals[~np.isnan(vals)]
    if len(vals) == 0:
        return np.nan, np.nan, np.nan
    if len(vals) == 1:
        return float(vals[0]), float(vals[0]), float(vals[0])
    rng = np.random.default_rng(seed)
    boot_indices = rng.integers(0, len(vals), size=(n_boot, len(vals)))
    boot_means = np.mean(vals[boot_indices], axis=1)
    alpha = (1.0 - ci) / 2.0
    ci_lower = float(np.percentile(boot_means, 100.0 * alpha))
    ci_upper = float(np.percentile(boot_means, 100.0 * (1.0 - alpha)))
    return float(np.mean(vals)), ci_lower, ci_upper


def summarize_df(df: pd.DataFrame, group_cols: list) -> pd.DataFrame:
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
    out_md = os.path.join(results_dir, "summary_phase2a2.md")

    lines = []
    lines.append("# Phase 2a.2 Summary Statistics (10,000 Bootstrap Resamples over Seeds, grid_v2)\n\n")

    # 1. T1 Entropy
    t1_csv = os.path.join(results_dir, "t1_entropy_gridv2.csv")
    if os.path.exists(t1_csv):
        lines.append("## Task 1: Disordered TFIM Half-Chain Entropy (n=8, grid_v2)\n\n")
        df_t1 = pd.read_csv(t1_csv)
        group_cols_t1 = ["task", "target", "tag", "n", "N_train", "model", "variant", "metric"]
        summary_t1 = summarize_df(df_t1, group_cols_t1)
        lines.append(df_to_markdown_simple(summary_t1))
        lines.append("\n\n")

    # 2. T2 Correlators
    t2_csv = os.path.join(results_dir, "t2_correlators_gridv2.csv")
    if os.path.exists(t2_csv):
        lines.append("## Task 2: Ground-State Correlator Prediction (n=8, grid_v2)\n\n")
        df_t2 = pd.read_csv(t2_csv)
        group_cols_t2 = ["task", "target", "tag", "n", "N_train", "model", "variant", "metric"]
        summary_t2 = summarize_df(df_t2, group_cols_t2)
        lines.append(df_to_markdown_simple(summary_t2))
        lines.append("\n\n")

    # 3. T4 Frustrated 2D
    t4_csv = os.path.join(results_dir, "t4_v2_gridv2.csv")
    if os.path.exists(t4_csv):
        lines.append("## Task 4 (v2): Frustrated 2D Lattice Benchmark (grid_v2)\n\n")
        df_t4 = pd.read_csv(t4_csv)
        group_cols_t4 = ["task", "target", "tag", "lattice", "boundary", "n", "N_train", "model", "variant", "metric"]
        summary_t4 = summarize_df(df_t4, group_cols_t4)
        lines.append(df_to_markdown_simple(summary_t4))
        lines.append("\n\n")

    with open(out_md, "w", encoding="utf-8") as f:
        f.write("".join(lines))
    print(f"Summary written to {out_md}")


if __name__ == "__main__":
    main()
