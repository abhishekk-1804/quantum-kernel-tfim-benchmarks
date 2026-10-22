"""
scripts/generate_summary_phase2b.py
-----------------------------------
Generates results/summary_phase2b.md from results/t5_noise.csv.
Computes 10,000 bootstrap 95% confidence intervals over seeds for all models
across all noise levels in both finite-shots and depolarizing experiments.
Logs FQ negative eigenvalue fraction across shot levels.
"""

import os
import sys
from typing import Tuple, List, Dict, Any
import numpy as np
import pandas as pd

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def bootstrap_ci(values: np.ndarray, n_boot: int = 10000, rng_seed: int = 42) -> Tuple[float, float, float]:
    """Compute mean and 95% bootstrap percentile CI."""
    vals = np.asarray(values, dtype=float)
    if len(vals) == 0:
        return np.nan, np.nan, np.nan
    mean_val = float(np.mean(vals))
    if len(vals) == 1:
        return mean_val, mean_val, mean_val
    rng = np.random.default_rng(rng_seed)
    boot_means = np.mean(rng.choice(vals, size=(n_boot, len(vals)), replace=True), axis=1)
    ci_low = float(np.percentile(boot_means, 2.5))
    ci_high = float(np.percentile(boot_means, 97.5))
    return mean_val, ci_low, ci_high


def normalize_level(val: Any) -> str:
    """Normalize noise level string across int, float, and inf representations."""
    try:
        f = float(val)
        if np.isinf(f):
            return "inf"
        if f == int(f) and f >= 1:
            return str(int(f))
        return f"{f:.2f}"
    except Exception:
        return str(val)


def generate_summary(csv_path: str = "results/t5_noise.csv", out_md: str = "results/summary_phase2b.md"):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"{csv_path} not found.")

    df = pd.read_csv(csv_path)
    df["noise_level"] = df["noise_level"].apply(normalize_level)

    lines = []
    lines.append("# Phase 2b: Shared-Basis Measurement Noise & Depolarizing Benchmark Summary\n")
    lines.append(f"Source data: `{csv_path}` (Total rows: {len(df)})\n")

    # 1. Finite-Shots Experiment Summary
    df_shots = df[(df["experiment"] == "finite_shots") & (df["metric"] == "r2")]
    if len(df_shots) > 0:
        lines.append("## 1. Finite-Shots Noise Sweep (Target: Half-Chain Entropy, n=8, N_train=40)\n")
        lines.append("Evaluation across measurement shot budgets $S \\in \\{100, 1000, 10000, \\infty\\}$ (20 seeds).\n")

        # Table header
        models_shots = [
            ("PQK-1", "none"),
            ("PQK-2nn", "none"),
            ("FQ-raw", "none"),
            ("FQ-clipped", "none"),
            ("E", "raw"),
            ("E", "std"),
            ("E2", "raw"),
            ("F", "std"),
        ]

        # FQ negative eigenvalue fractions
        lines.append("### FQ Gram Matrix Spectrum Analysis (Training Gram $\\hat{K}_{\\text{train}}$)\n")
        lines.append("| Shot Budget $S$ | Seeds Evaluated | Fraction with $\\lambda_{\\min} < 0$ | Mean $\\lambda_{\\min}$ | Min $\\lambda_{\\min}$ |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")

        for s_level in ["100", "1000", "10000", "inf"]:
            sub_fq = df_shots[(df_shots["noise_level"] == s_level) & (df_shots["model"] == "FQ-raw")]
            if len(sub_fq) > 0:
                n_seeds = len(sub_fq)
                lam_vals = sub_fq["lam_min"].values
                neg_frac = float(np.mean(lam_vals < 0))
                mean_lam = float(np.mean(lam_vals))
                min_lam = float(np.min(lam_vals))
                lines.append(f"| {s_level} | {n_seeds} | {neg_frac:.2%} | {mean_lam:.4f} | {min_lam:.4f} |")
        lines.append("\n")

        lines.append("### Test $R^2$ Performance vs. Shot Budget $S$ (Mean [95% CI])\n")
        shot_levels = ["100", "1000", "10000", "inf"]

        table_header = "| Model | Variant | " + " | ".join([f"S={s}" for s in shot_levels]) + " |"
        table_sep = "| :--- | :--- | " + " | ".join([":---:" for _ in shot_levels]) + " |"
        lines.append(table_header)
        lines.append(table_sep)

        for m_name, v_name in models_shots:
            row_cells = [m_name, v_name]
            for s_level in shot_levels:
                sub = df_shots[
                    (df_shots["noise_level"] == s_level) &
                    (df_shots["model"] == m_name) &
                    (df_shots["variant"] == v_name)
                ]
                if len(sub) > 0:
                    mean_val, ci_l, ci_h = bootstrap_ci(sub["value"].values)
                    row_cells.append(f"{mean_val:.4f} [{ci_l:.4f}, {ci_h:.4f}]")
                else:
                    row_cells.append("N/A")
            lines.append("| " + " | ".join(row_cells) + " |")
        lines.append("\n")

    # 2. Depolarizing Channel Sweep Summary
    df_depol = df[(df["experiment"] == "depolarizing") & (df["metric"] == "r2")]
    if len(df_depol) > 0:
        lines.append("## 2. Depolarizing Channel Noise Sweep (p in [0.00, 0.08])\n")
        lines.append("Subsystem and mixed-state overlap evaluation across depolarizing rates $p$ (20 seeds).\n")

        models_depol = [
            ("PQK-1", "none"),
            ("PQK-2nn", "none"),
            ("FQ", "mixed_state_overlap"),
            ("E", "raw"),
            ("E", "std"),
            ("E2", "raw"),
            ("F", "std"),
        ]

        depol_levels = ["0.00", "0.01", "0.02", "0.04", "0.06", "0.08"]
        # Filter existing levels
        existing_p = [p for p in depol_levels if p in df_depol["noise_level"].astype(str).unique()]

        table_header = "| Model | Variant | " + " | ".join([f"p={p}" for p in existing_p]) + " |"
        table_sep = "| :--- | :--- | " + " | ".join([":---:" for _ in existing_p]) + " |"
        lines.append(table_header)
        lines.append(table_sep)

        for m_name, v_name in models_depol:
            row_cells = [m_name, v_name]
            for p_lvl in existing_p:
                sub = df_depol[
                    (df_depol["noise_level"].astype(str) == p_lvl) &
                    (df_depol["model"] == m_name) &
                    (df_depol["variant"] == v_name)
                ]
                if len(sub) > 0:
                    mean_val, ci_l, ci_h = bootstrap_ci(sub["value"].values)
                    row_cells.append(f"{mean_val:.4f} [{ci_l:.4f}, {ci_h:.4f}]")
                else:
                    row_cells.append("N/A")
            lines.append("| " + " | ".join(row_cells) + " |")
        lines.append("\n")

    # Write summary
    os.makedirs(os.path.dirname(os.path.abspath(out_md)), exist_ok=True)
    summary_text = "\n".join(lines)
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(summary_text)

    print(f"Summary written to {out_md}.")
    return summary_text


if __name__ == "__main__":
    src_csv = sys.argv[1] if len(sys.argv) > 1 else "results/t5_noise.csv"
    dst_md = sys.argv[2] if len(sys.argv) > 2 else "results/summary_phase2b.md"
    generate_summary(src_csv, dst_md)
