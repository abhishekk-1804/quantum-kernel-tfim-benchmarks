"""
scripts/generate_before_after_comparison.py
-------------------------------------------
Compare Phase 2a/2a.1 (grid_v1) vs Phase 2a.2 (grid_v2) performance
with 10,000 bootstrap confidence intervals:
- T1 (N_train in {10, 40, 160}, metric: r2)
- T2b (N_train = 40, metric: r2)
- T4a v2 (N_train in {10, 80}, on 2x4 and 3x4 lattices, metric: accuracy)
Pure numbers and tables only. No interpretive prose.
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


def load_and_group(csv_path: str, group_cols: list) -> dict:
    if not os.path.exists(csv_path):
        return {}
    df = pd.read_csv(csv_path)
    res = {}
    for keys, sub in df.groupby(group_cols, sort=False):
        vals = sub["value"].to_numpy(dtype=float)
        m, l, u = bootstrap_ci(vals)
        res[keys] = (m, l, u, len(vals))
    return res


def print_comparison():
    # ── Task 1 ────────────────────────────────────────────────────────────────
    t1_v1 = os.path.join("results", "t1_entropy.csv")
    t1_v2 = os.path.join("results", "t1_entropy_gridv2.csv")

    cols_t1 = ["task", "target", "model", "variant", "N_train", "metric"]
    v1_t1 = load_and_group(t1_v1, cols_t1)
    v2_t1 = load_and_group(t1_v2, cols_t1)

    print("\n" + "=" * 95)
    print("TASK 1: Disordered TFIM Half-Chain Entropy (n=8, metric: R2)")
    print("=" * 95)
    print(f"{'Model':<25} {'Variant':<8} {'N':<6} {'grid_v1 Mean [95% CI]':<30} {'grid_v2 Mean [95% CI]':<30} {'Diff':<10}")
    print("-" * 95)

    all_keys_t1 = sorted(set(list(v1_t1.keys()) + list(v2_t1.keys())), key=lambda x: (x[4], x[2], x[3]))
    for k in all_keys_t1:
        task, target, model, variant, N, metric = k
        if metric != "r2" or N not in (10, 40, 160):
            continue
        v1_stat = v1_t1.get(k)
        v2_stat = v2_t1.get(k)

        v1_str = f"{v1_stat[0]:.4f} [{v1_stat[1]:.4f}, {v1_stat[2]:.4f}]" if v1_stat else "N/A"
        v2_str = f"{v2_stat[0]:.4f} [{v2_stat[1]:.4f}, {v2_stat[2]:.4f}]" if v2_stat else "N/A"
        diff_str = f"{v2_stat[0] - v1_stat[0]:+.4f}" if (v1_stat and v2_stat) else "N/A"

        print(f"{model:<25} {variant:<8} {N:<6} {v1_str:<30} {v2_str:<30} {diff_str:<10}")

    # ── Task 2b ───────────────────────────────────────────────────────────────
    t2_v1 = os.path.join("results", "t2_correlators.csv")
    t2_v2 = os.path.join("results", "t2_correlators_gridv2.csv")

    cols_t2 = ["task", "target", "model", "variant", "N_train", "metric"]
    v1_t2 = load_and_group(t2_v1, cols_t2)
    v2_t2 = load_and_group(t2_v2, cols_t2)

    print("\n" + "=" * 95)
    print("TASK 2b: Connected ZZ Correlator (n=8, N_train=40, metric: R2)")
    print("=" * 95)
    print(f"{'Model':<25} {'Variant':<8} {'N':<6} {'grid_v1 Mean [95% CI]':<30} {'grid_v2 Mean [95% CI]':<30} {'Diff':<10}")
    print("-" * 95)

    all_keys_t2 = sorted(set(list(v1_t2.keys()) + list(v2_t2.keys())), key=lambda x: (x[2], x[3]))
    for k in all_keys_t2:
        task, target, model, variant, N, metric = k
        if task != "T2b" or metric != "r2" or N != 40:
            continue
        v1_stat = v1_t2.get(k)
        v2_stat = v2_t2.get(k)

        v1_str = f"{v1_stat[0]:.4f} [{v1_stat[1]:.4f}, {v1_stat[2]:.4f}]" if v1_stat else "N/A"
        v2_str = f"{v2_stat[0]:.4f} [{v2_stat[1]:.4f}, {v2_stat[2]:.4f}]" if v2_stat else "N/A"
        diff_str = f"{v2_stat[0] - v1_stat[0]:+.4f}" if (v1_stat and v2_stat) else "N/A"

        print(f"{model:<25} {variant:<8} {N:<6} {v1_str:<30} {v2_str:<30} {diff_str:<10}")

    # ── Task 4a v2 ────────────────────────────────────────────────────────────
    t4_v1 = os.path.join("results", "t4_v2.csv")
    t4_v2 = os.path.join("results", "t4_v2_gridv2.csv")

    cols_t4 = ["task", "target", "lattice", "model", "variant", "N_train", "metric"]
    v1_t4 = load_and_group(t4_v1, cols_t4)
    v2_t4 = load_and_group(t4_v2, cols_t4)

    print("\n" + "=" * 105)
    print("TASK 4a (v2): Frustrated 2D Classification (metric: Accuracy, N_train in {10, 80})")
    print("=" * 105)
    print(f"{'Lattice':<10} {'Model':<25} {'Variant':<8} {'N':<6} {'grid_v1 Mean [95% CI]':<30} {'grid_v2 Mean [95% CI]':<30} {'Diff':<10}")
    print("-" * 105)

    all_keys_t4 = sorted(set(list(v1_t4.keys()) + list(v2_t4.keys())), key=lambda x: (x[2], x[5], x[3], x[4]))
    for k in all_keys_t4:
        task, target, lattice, model, variant, N, metric = k
        if task != "T4a" or metric != "accuracy" or N not in (10, 80):
            continue
        v1_stat = v1_t4.get(k)
        v2_stat = v2_t4.get(k)

        v1_str = f"{v1_stat[0]:.4f} [{v1_stat[1]:.4f}, {v1_stat[2]:.4f}]" if v1_stat else "N/A"
        v2_str = f"{v2_stat[0]:.4f} [{v2_stat[1]:.4f}, {v2_stat[2]:.4f}]" if v2_stat else "N/A"
        diff_str = f"{v2_stat[0] - v1_stat[0]:+.4f}" if (v1_stat and v2_stat) else "N/A"

        print(f"{lattice:<10} {model:<25} {variant:<8} {N:<6} {v1_str:<30} {v2_str:<30} {diff_str:<10}")


if __name__ == "__main__":
    print_comparison()
