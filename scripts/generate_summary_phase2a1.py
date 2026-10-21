"""
scripts/generate_summary_phase2a1.py
------------------------------------
Generate results/summary_phase2a1.md with 10,000 bootstrap resamples over seeds.
Pure tables, numbers only, no interpretive prose.
"""

import os
import sys
import pandas as pd
import numpy as np

def bootstrap_ci(values, n_resamples=10000, ci=0.95, rng=None):
    if rng is None:
        rng = np.random.default_rng(42)
    vals = np.asarray(values, dtype=float)
    vals = vals[~np.isnan(vals)]
    if len(vals) == 0:
        return np.nan, np.nan, np.nan
    if len(vals) == 1:
        return float(vals[0]), float(vals[0]), float(vals[0])
    
    boot_means = np.mean(rng.choice(vals, size=(n_resamples, len(vals)), replace=True), axis=1)
    lower = float(np.percentile(boot_means, (1.0 - ci) / 2.0 * 100))
    upper = float(np.percentile(boot_means, (1.0 + ci) / 2.0 * 100))
    return float(np.mean(vals)), lower, upper


def generate_summary():
    t3_path = os.path.join("results", "t3_concentration_v2.csv")
    t4_path = os.path.join("results", "t4_v2.csv")
    out_md = os.path.join("results", "summary_phase2a1.md")

    rng = np.random.default_rng(42)
    lines = ["# Phase 2a.1 Summary Statistics (10,000 Bootstrap Resamples over Seeds)\n"]

    # ── Task 3 v2 ─────────────────────────────────────────────────────────────
    if os.path.exists(t3_path):
        lines.append("## Task 3 (v2): Concentration Scaling of Quantum Kernels\n")
        lines.append("### Off-Diagonal Mean by Ensemble, Kernel, Bandwidth Rule, and System Size n\n")
        df3 = pd.read_csv(t3_path)
        
        headers3 = ["tag", "kernel", "gamma_rule", "n", "num_seeds", "mean", "ci_95_lower", "ci_95_upper"]
        lines.append("| " + " | ".join(headers3) + " |")
        lines.append("| " + " | ".join(["---"] * len(headers3)) + " |")

        group_cols3 = ["tag", "kernel", "gamma_rule", "n"]
        for keys, group in df3.groupby(group_cols3, sort=False):
            tag, kernel, grule, n = keys
            n_seeds = len(group["seed"].unique())
            m, lo, hi = bootstrap_ci(group["off_diag_mean"].values, rng=rng)
            lines.append(f"| {tag} | {kernel} | {grule} | {n} | {n_seeds} | {m:.6f} | {lo:.6f} | {hi:.6f} |")
        lines.append("\n")

        # FQ log10 off-diagonal mean
        df3_fq = df3[(df3["kernel"] == "FQ") & (df3["off_diag_log10_mean"].notna()) & (df3["off_diag_log10_mean"] != "")]
        if not df3_fq.empty:
            lines.append("### FQ Mean Log10 Off-Diagonal Entries\n")
            headers3_log = ["tag", "n", "num_seeds", "mean_log10", "ci_95_lower", "ci_95_upper"]
            lines.append("| " + " | ".join(headers3_log) + " |")
            lines.append("| " + " | ".join(["---"] * len(headers3_log)) + " |")
            for (tag, n), group in df3_fq.groupby(["tag", "n"], sort=False):
                n_seeds = len(group["seed"].unique())
                m, lo, hi = bootstrap_ci(group["off_diag_log10_mean"].astype(float).values, rng=rng)
                lines.append(f"| {tag} | {n} | {n_seeds} | {m:.6f} | {lo:.6f} | {hi:.6f} |")
            lines.append("\n")

    # ── Task 4 v2 ─────────────────────────────────────────────────────────────
    if os.path.exists(t4_path):
        lines.append("## Task 4 (v2): Frustrated 2D Lattice Benchmark\n")
        df4 = pd.read_csv(t4_path)

        for task_name in ["T4a", "T4b"]:
            sub = df4[df4["task"] == task_name]
            if sub.empty:
                continue
            sub_title = "T4a: Classification (sign(S(pi,pi) - S(pi,0)))" if task_name == "T4a" else "T4b: Regression (Half-Cut Entropy)"
            lines.append(f"### {sub_title}\n")

            headers4 = [
                "task", "target", "tag", "lattice", "boundary", "n",
                "N_train", "model", "variant", "metric", "num_seeds", "mean", "ci_95_lower", "ci_95_upper"
            ]
            lines.append("| " + " | ".join(headers4) + " |")
            lines.append("| " + " | ".join(["---"] * len(headers4)) + " |")

            group_cols4 = ["task", "target", "tag", "lattice", "boundary", "n", "N_train", "model", "variant", "metric"]
            for keys, group in sub.groupby(group_cols4, sort=False):
                t_name, target, tag, lattice, bdry, n, N_tr, model, variant, metric = keys
                n_seeds = len(group["seed"].unique())
                m, lo, hi = bootstrap_ci(group["value"].values, rng=rng)
                lines.append(
                    f"| {t_name} | {target} | {tag} | {lattice} | {bdry} | {n} | {N_tr} | {model} | {variant} | {metric} | {n_seeds} | {m:.6f} | {lo:.6f} | {hi:.6f} |"
                )
            lines.append("\n")

    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Summary written to {out_md}")

if __name__ == "__main__":
    generate_summary()
