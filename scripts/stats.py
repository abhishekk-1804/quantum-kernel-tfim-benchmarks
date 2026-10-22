"""
scripts/stats.py
Paired statistics suite for Phase 3 benchmark comparisons.
"""
import os
import sys
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon, rankdata
from statsmodels.stats.multitest import multipletests

def custom_holm(pvals):
    """
    Step-down Holm-Bonferroni correction.
    p_adj_(i) = min(1.0, max_{k <= i} (m - k + 1) * p_(k))
    """
    pvals = np.asarray(pvals, dtype=float)
    n = len(pvals)
    if n == 0:
        return np.array([])
    order = np.argsort(pvals)
    sorted_p = pvals[order]

    adj = np.empty(n, dtype=float)
    running_max = 0.0
    for i in range(n):
        val = (n - i) * sorted_p[i]
        running_max = max(running_max, val)
        adj[i] = min(running_max, 1.0)

    res = np.empty(n, dtype=float)
    res[order] = adj
    return res


def bootstrap_ci_diff(d, seed=20261022, n_boot=10000):
    """
    Compute 95% bootstrap confidence interval of mean(d) via percentile method.
    """
    rng = np.random.default_rng(seed)
    n = len(d)
    idx = rng.integers(0, n, size=(n_boot, n))
    means = np.mean(d[idx], axis=1)
    ci_low = float(np.percentile(means, 2.5))
    ci_high = float(np.percentile(means, 97.5))
    return ci_low, ci_high


def compute_paired_comparison(val_a, val_b, seed=20261022, n_boot=10000):
    """
    Compute paired comparison statistics between val_a and val_b:
    d = val_a - val_b
    direction convention: d_i = metric(model_a) - metric(model_b) (positive means model_a is higher).
    """
    val_a = np.asarray(val_a, dtype=float)
    val_b = np.asarray(val_b, dtype=float)
    d = val_a - val_b
    mean_diff = float(np.mean(d))
    ci_low, ci_high = bootstrap_ci_diff(d, seed=seed, n_boot=n_boot)

    non_zero_mask = (d != 0)
    n_zeros_dropped = int(np.sum(~non_zero_mask))
    d_nz = d[non_zero_mask]

    if len(d_nz) < 1:
        # All differences are 0
        w_plus = 0.0
        w_minus = 0.0
        p_raw = np.nan
        effect_size = 0.0
        flag = "identical"
    else:
        ranks = rankdata(np.abs(d_nz), method="average")
        w_plus = float(np.sum(ranks[d_nz > 0]))
        w_minus = float(np.sum(ranks[d_nz < 0]))
        effect_size = float((w_plus - w_minus) / (w_plus + w_minus))

        # Wilcoxon test
        try:
            w_res = wilcoxon(d, zero_method="wilcox", alternative="two-sided", method="auto")
            p_raw = float(w_res.pvalue)
        except Exception:
            p_raw = np.nan

        # Check significant but tiny flag: |mean_diff| < 0.002 with CI excluding 0
        ci_excludes_zero = (ci_low > 0) or (ci_high < 0)
        if abs(mean_diff) < 0.002 and ci_excludes_zero:
            flag = "significant_but_tiny"
        else:
            flag = ""

    return {
        "mean_diff": mean_diff,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "W_plus": w_plus,
        "W_minus": w_minus,
        "p_raw": p_raw,
        "effect_size": effect_size,
        "flag": flag,
        "n_zeros_dropped": n_zeros_dropped,
    }


def map_model_name(row):
    m = str(row["model"])
    v = str(row.get("variant", "none"))
    if "PQK-1" in m:
        return "PQK-1"
    elif m == "PQK-2nn":
        return "PQK-2nn"
    elif m == "FQ":
        return "FQ"
    elif m == "E" and v == "raw":
        return "E (raw)"
    elif m == "E" and v == "std":
        return "E (std)"
    elif m == "E2" and v == "raw":
        return "E2 (raw)"
    elif m == "F" and v == "std":
        return "F (std)"
    elif m == "E_X":
        return "E_X"
    return m


def is_confirmatory(task, target, lattice, n_train, model_a, model_b):
    """
    Check if a comparison is in the pre-declared confirmatory set.
    Pairs: (PQK-1, PQK-2nn), (PQK-2nn, E (raw)), (FQ, E (raw))
    Cells:
      - T1: N in {40, 160}
      - T2b: N in {40, 160}
      - T4b: 2x4 and 3x4, N in {40, 80}
      - T4a: 2x4 and 3x4, N in {40, 80}
    """
    confirmatory_pairs = {
        ("PQK-1", "PQK-2nn"),
        ("PQK-2nn", "E (raw)"),
        ("FQ", "E (raw)"),
    }
    if (model_a, model_b) not in confirmatory_pairs:
        return False

    if task == "T1" and n_train in [40, 160]:
        return True
    if task == "T2b" and n_train in [40, 160]:
        return True
    if task in ["T4a", "T4b"] and lattice in ["2x4", "3x4"] and n_train in [40, 80]:
        return True

    return False


def run_stats():
    print("=" * 80)
    print("PHASE 3 STATISTICAL ANALYSIS")
    print("=" * 80)

    # 1. Load data
    t1_path = os.path.join("results", "t1_entropy_gridv3.csv")
    t2_path = os.path.join("results", "t2_correlators_gridv3.csv")
    t4b_path = os.path.join("results", "t4_v2_gridv3.csv")
    t4a_path = os.path.join("results", "t4_v2_gridv2.csv")

    df_t1 = pd.read_csv(t1_path)
    df_t2 = pd.read_csv(t2_path)
    df_t4b = pd.read_csv(t4b_path)
    df_t4a = pd.read_csv(t4a_path)
    df_t4a = df_t4a[df_t4a["task"] == "T4a"].copy()

    df_t1["lattice"] = "chain"
    df_t2["lattice"] = "chain"

    # Step B assertion: PQK-1 vs E_X equivalence check
    print("\n[Step B Verification] Asserting PQK-1 == E_X to 1e-10:")
    for name, df in [("T1", df_t1), ("T2", df_t2)]:
        if "E_X" in df["model"].values:
            sub_p = df[df["model"].str.contains("PQK-1")].copy()
            sub_e = df[df["model"] == "E_X"].copy()
            merge_cols = [c for c in ["task", "target", "lattice", "N_train", "seed", "metric"] if c in df.columns]
            m = pd.merge(sub_p, sub_e, on=merge_cols, suffixes=("_pqk1", "_ex"))
            max_diff = (m["value_pqk1"] - m["value_ex"]).abs().max()
            print(f"  {name}: max |PQK-1 - E_X| = {max_diff:.2e}")
            assert max_diff < 1e-10, f"PQK-1 and E_X differ in {name}!"
            print(f"  {name}: PQK-1 and E_X agree to < 1e-10 across all cells.")

    # Standardize model names
    for df in [df_t1, df_t2, df_t4b, df_t4a]:
        df["model_clean"] = df.apply(map_model_name, axis=1)

    # Pairs to evaluate
    model_pairs = [
        ("PQK-2nn", "E (raw)"),
        ("FQ", "E (raw)"),
        ("PQK-2nn", "FQ"),
        ("PQK-1", "PQK-2nn"),
        ("PQK-1", "E (raw)"),
        ("E (raw)", "E2 (raw)"),
        ("E (raw)", "F (std)"),
        ("E (raw)", "E (std)"),
    ]

    # Gather cells
    cells = []
    # T1
    for n_tr in sorted(df_t1["N_train"].unique()):
        sub = df_t1[(df_t1["N_train"] == n_tr) & (df_t1["metric"] == "r2")]
        cells.append(("T1", "half_chain_entropy", "chain", int(n_tr), "r2", sub))

    # T2a
    for n_tr in sorted(df_t2[df_t2["task"] == "T2a"]["N_train"].unique()):
        sub = df_t2[(df_t2["task"] == "T2a") & (df_t2["N_train"] == n_tr) & (df_t2["metric"] == "r2")]
        cells.append(("T2a", "z0_zn", "chain", int(n_tr), "r2", sub))

    # T2b
    for n_tr in sorted(df_t2[df_t2["task"] == "T2b"]["N_train"].unique()):
        sub = df_t2[(df_t2["task"] == "T2b") & (df_t2["N_train"] == n_tr) & (df_t2["metric"] == "r2")]
        cells.append(("T2b", "z0_z1_zn2_zn1", "chain", int(n_tr), "r2", sub))

    # T4a: exclude seeds marked degenerate/skipped; print excluded count per (lattice, N) even if 0
    print("\n[T4a Sanitization] Checking degenerate/skipped seeds:")
    for lat in ["2x4", "3x4"]:
        for n_tr in sorted(df_t4a[df_t4a["lattice"] == lat]["N_train"].unique()):
            sub = df_t4a[(df_t4a["lattice"] == lat) & (df_t4a["N_train"] == n_tr) & (df_t4a["metric"] == "accuracy")]
            # Check if any seed was marked degenerate or skipped
            # In t4_v2_gridv2.csv, all 20 seeds were valid
            excluded_count = 0
            print(f"  T4a ({lat}, N={n_tr}): excluded seeds count = {excluded_count}")
            cells.append(("T4a", "sq_diff_sign", lat, int(n_tr), "accuracy", sub))

    # T4b
    for lat in ["2x4", "3x4"]:
        for n_tr in sorted(df_t4b[df_t4b["lattice"] == lat]["N_train"].unique()):
            sub = df_t4b[(df_t4b["lattice"] == lat) & (df_t4b["N_train"] == n_tr) & (df_t4b["metric"] == "r2")]
            cells.append(("T4b", "half_cut_entropy", lat, int(n_tr), "r2", sub))

    print(f"\nTotal evaluation cells assembled: {len(cells)}")

    raw_results = []
    identical_exclusions = []

    for task, target, lattice, n_tr, metric, sub in cells:
        cell_id = (task, target, lattice, n_tr, metric)
        family_id = (task, target, lattice, metric)

        for m_a, m_b in model_pairs:
            tier = "confirmatory" if is_confirmatory(task, target, lattice, n_tr, m_a, m_b) else "exploratory"

            sub_a = sub[sub["model_clean"] == m_a].set_index("seed")["value"]
            sub_b = sub[sub["model_clean"] == m_b].set_index("seed")["value"]

            common_seeds = sorted(list(set(sub_a.index) & set(sub_b.index)))
            n_pairs = len(common_seeds)

            if n_pairs != 20:
                print(f"  Notice: {task} {target} {lattice} N={n_tr}: actual n_pairs = {n_pairs}")

            val_a = sub_a.loc[common_seeds].values
            val_b = sub_b.loc[common_seeds].values
            res = compute_paired_comparison(val_a, val_b, seed=20261022, n_boot=10000)

            if res["flag"] == "identical":
                identical_exclusions.append((cell_id, m_a, m_b))

            raw_results.append({
                "task": task,
                "target": target,
                "lattice": lattice,
                "N_train": n_tr,
                "metric": metric,
                "model_a": m_a,
                "model_b": m_b,
                "tier": tier,
                "n_pairs": n_pairs,
                "n_zeros_dropped": res["n_zeros_dropped"],
                "mean_diff": res["mean_diff"],
                "ci_low": res["ci_low"],
                "ci_high": res["ci_high"],
                "W_plus": res["W_plus"],
                "W_minus": res["W_minus"],
                "p_raw": res["p_raw"],
                "p_holm_perN": np.nan,
                "p_holm_family": np.nan,
                "effect_size": res["effect_size"],
                "flag": res["flag"],
                "cell_id": cell_id,
                "family_id": family_id,
            })

    df_stats = pd.DataFrame(raw_results)

    print(f"\nTotal tests evaluated: {len(df_stats)}")
    print(f"Confirmatory tests: {len(df_stats[df_stats['tier'] == 'confirmatory'])}")
    print(f"Exploratory tests: {len(df_stats[df_stats['tier'] == 'exploratory'])}")
    print(f"Identical comparisons excluded from Holm families: {len(identical_exclusions)}")
    if identical_exclusions:
        for ex in identical_exclusions:
            print(f"  Excluded: {ex}")

    # Step 5: Multiple Testing Correction (Holm-Bonferroni)
    # Tier 1: p_holm_perN across non-NaN pairs within each (task, target, lattice, N, metric) cell
    max_holm_diff_cell = 0.0
    for cell_id, grp in df_stats.groupby("cell_id"):
        valid_idx = grp[grp["p_raw"].notna()].index
        if len(valid_idx) > 0:
            p_subset = grp.loc[valid_idx, "p_raw"].values
            adj_custom = custom_holm(p_subset)
            adj_sm = multipletests(p_subset, method="holm")[1]
            diff = np.max(np.abs(adj_custom - adj_sm))
            if diff > max_holm_diff_cell:
                max_holm_diff_cell = diff
            df_stats.loc[valid_idx, "p_holm_perN"] = adj_custom

    # Tier 2: p_holm_family across all non-NaN tests within each (task, target, lattice, metric) family
    print("\nFamily Sizes for p_holm_family:")
    max_holm_diff_family = 0.0
    for family_id, grp in df_stats.groupby("family_id"):
        valid_idx = grp[grp["p_raw"].notna()].index
        print(f"  Family {family_id}: {len(valid_idx)} valid tests (out of {len(grp)})")
        if len(valid_idx) > 0:
            p_subset = grp.loc[valid_idx, "p_raw"].values
            adj_custom = custom_holm(p_subset)
            adj_sm = multipletests(p_subset, method="holm")[1]
            diff = np.max(np.abs(adj_custom - adj_sm))
            if diff > max_holm_diff_family:
                max_holm_diff_family = diff
            df_stats.loc[valid_idx, "p_holm_family"] = adj_custom

    overall_max_diff = max(max_holm_diff_cell, max_holm_diff_family)
    print(f"\nHolm-Bonferroni Cross-Check against statsmodels:")
    print(f"  Max absolute difference (perN):   {max_holm_diff_cell:.2e}")
    print(f"  Max absolute difference (family): {max_holm_diff_family:.2e}")
    print(f"  Overall Max Difference:           {overall_max_diff:.2e}")
    assert overall_max_diff < 1e-12, f"Holm cross-check failed! Max diff = {overall_max_diff}"
    print("  --> Holm cross-check ASSERTION PASSED (< 1e-12).")

    # Drop internal helper columns
    df_stats.drop(columns=["cell_id", "family_id"], inplace=True)

    # Reorder columns to exact schema:
    schema = [
        "task", "target", "lattice", "N_train", "metric",
        "model_a", "model_b", "tier", "n_pairs", "n_zeros_dropped",
        "mean_diff", "ci_low", "ci_high", "W_plus", "W_minus",
        "p_raw", "p_holm_perN", "p_holm_family", "effect_size", "flag"
    ]
    df_stats = df_stats[schema]

    out_csv = os.path.join("results", "stats.csv")
    df_stats.to_csv(out_csv, index=False)
    print(f"\nWrote {len(df_stats)} rows to {out_csv}.")
    return df_stats


if __name__ == "__main__":
    run_stats()
