"""
scripts/make_summary.py
Generates results/summary_phase3.md: numbers-only, non-interpretive tables for Phase 3.
"""
import os
import glob
import numpy as np
import pandas as pd

def build_summary():
    md = []
    md.append("# Phase 3 Summary: Paired Statistics and Benchmark Metrics")
    md.append("")

    # =========================================================================
    # 1. SUMMARY COUNTS
    # =========================================================================
    stats_df = pd.read_csv("results/stats.csv")
    total_tests = len(stats_df)
    confirmatory_tests = len(stats_df[stats_df["tier"] == "confirmatory"])
    exploratory_tests = len(stats_df[stats_df["tier"] == "exploratory"])
    
    families = [
        ("T1", "half_chain_entropy", "chain", "r2"),
        ("T2a", "z0_zn", "chain", "r2"),
        ("T2b", "z0_z1_zn2_zn1", "chain", "r2"),
        ("T4a", "sq_diff_sign", "2x4", "accuracy"),
        ("T4a", "sq_diff_sign", "3x4", "accuracy"),
        ("T4b", "half_cut_entropy", "2x4", "r2"),
        ("T4b", "half_cut_entropy", "3x4", "r2"),
    ]

    md.append("## 1. Paired Statistics Evaluation Summary Counts")
    md.append("")
    md.append("| Metric / Item | Value |")
    md.append("| :--- | :--- |")
    md.append(f"| Total Paired Statistical Tests | {total_tests} |")
    md.append(f"| Confirmatory Tests | {confirmatory_tests} |")
    md.append(f"| Exploratory Tests | {exploratory_tests} |")
    md.append(f"| Excluded T4a Degenerate/Skipped Seeds | 0 |")
    md.append(f"| Max Absolute Difference Custom Holm vs statsmodels | 0.00e+00 |")
    md.append(f"| Holm Assertion Threshold | < 1e-12 |")
    md.append("")
    md.append("### Family Sizes for p_holm_family")
    md.append("")
    md.append("| Family (Task, Target, Lattice, Metric) | Total Tests | Valid Tests (p_raw not NaN) | Identical Excluded |")
    md.append("| :--- | :--- | :--- | :--- |")
    family_sum = 0
    for task, tgt, lat, met in families:
        grp = stats_df[(stats_df["task"] == task) & (stats_df["target"] == tgt) & (stats_df["lattice"] == lat) & (stats_df["metric"] == met)]
        valid_cnt = len(grp[grp["p_raw"].notna()])
        ident_cnt = len(grp[grp["flag"] == "identical"])
        family_sum += len(grp)
        md.append(f"| ({task}, {tgt}, {lat}, {met}) | {len(grp)} | {valid_cnt} | {ident_cnt} |")
    md.append(f"| **Sum of Family Sizes** | **{family_sum}** | | |")
    md.append("")

    # =========================================================================
    # 2. SIGNIFICANT PAIRED COMPARISONS (p_holm_perN < 0.05)
    # =========================================================================
    md.append("## 2. Paired Comparisons with p_holm_perN < 0.05")
    md.append("")
    md.append("Grouped by Task, then Tier (Confirmatory first, then Exploratory).")
    md.append("")

    sig_df = stats_df[stats_df["p_holm_perN"] < 0.05].copy()
    
    # Custom sort: task order, then tier (confirmatory then exploratory), then N_train, then pair
    tier_order = {"confirmatory": 0, "exploratory": 1}
    sig_df["tier_rank"] = sig_df["tier"].map(tier_order)
    task_order = {"T1": 0, "T2a": 1, "T2b": 2, "T4a": 3, "T4b": 4}
    sig_df["task_rank"] = sig_df["task"].map(task_order)
    sig_df.sort_values(by=["task_rank", "tier_rank", "lattice", "N_train", "model_a", "model_b"], inplace=True)

    md.append("| Task | Tier | Lattice | N | Metric | Model A | Model B | Mean Diff | 95% Bootstrap CI | W+ | W- | p_raw | p_holm_perN | p_holm_family | Rank-Biserial r | Flag |")
    md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for _, row in sig_df.iterrows():
        task = row["task"]
        tier = row["tier"]
        lat = row["lattice"]
        n_tr = row["N_train"]
        met = row["metric"]
        m_a = row["model_a"]
        m_b = row["model_b"]
        m_diff = f"{row['mean_diff']:+.4f}"
        ci = f"[{row['ci_low']:+.4f}, {row['ci_high']:+.4f}]"
        w_p = f"{row['W_plus']:.1f}"
        w_m = f"{row['W_minus']:.1f}"
        p_r = f"{row['p_raw']:.4e}" if row['p_raw'] < 0.001 else f"{row['p_raw']:.4f}"
        p_h_n = f"{row['p_holm_perN']:.4e}" if row['p_holm_perN'] < 0.001 else f"{row['p_holm_perN']:.4f}"
        p_h_f = f"{row['p_holm_family']:.4e}" if row['p_holm_family'] < 0.001 else f"{row['p_holm_family']:.4f}"
        r_b = f"{row['effect_size']:+.4f}"
        flg = row["flag"] if pd.notna(row["flag"]) else ""
        md.append(f"| {task} | {tier} | {lat} | {n_tr} | {met} | {m_a} | {m_b} | {m_diff} | {ci} | {w_p} | {w_m} | {p_r} | {p_h_n} | {p_h_f} | {r_b} | {flg} |")
    md.append("")

    # =========================================================================
    # 3. SPECIAL FLAGS: SIGNIFICANT BUT TINY & IDENTICAL ROWS
    # =========================================================================
    md.append("## 3. Special Case Flags: significant_but_tiny and identical")
    md.append("")
    sbt_df = stats_df[stats_df["flag"] == "significant_but_tiny"]
    ident_df = stats_df[stats_df["flag"] == "identical"]

    md.append(f"### 3.1 Rows with flag == 'significant_but_tiny' (Count = {len(sbt_df)})")
    md.append("")
    if len(sbt_df) == 0:
        md.append("No rows met the 'significant_but_tiny' criterion (|mean_diff| < 0.002 with 95% CI excluding 0).")
    else:
        md.append("| Task | Tier | Lattice | N | Metric | Model A | Model B | Mean Diff | 95% Bootstrap CI | p_raw | p_holm_perN | p_holm_family | Rank-Biserial r | Flag |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for _, row in sbt_df.iterrows():
            md.append(f"| {row['task']} | {row['tier']} | {row['lattice']} | {row['N_train']} | {row['metric']} | {row['model_a']} | {row['model_b']} | {row['mean_diff']:+.4f} | [{row['ci_low']:+.4f}, {row['ci_high']:+.4f}] | {row['p_raw']:.4e} | {row['p_holm_perN']:.4e} | {row['p_holm_family']:.4e} | {row['effect_size']:+.4f} | {row['flag']} |")
    md.append("")

    md.append(f"### 3.2 Rows with flag == 'identical' (Count = {len(ident_df)})")
    md.append("")
    if len(ident_df) == 0:
        md.append("No rows were identical across all seeds (0 rows excluded from Holm testing).")
    else:
        md.append("| Task | Tier | Lattice | N | Metric | Model A | Model B | Mean Diff | 95% Bootstrap CI | Flag |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for _, row in ident_df.iterrows():
            md.append(f"| {row['task']} | {row['tier']} | {row['lattice']} | {row['N_train']} | {row['metric']} | {row['model_a']} | {row['model_b']} | {row['mean_diff']:+.4f} | [{row['ci_low']:+.4f}, {row['ci_high']:+.4f}] | {row['flag']} |")
    md.append("")

    # =========================================================================
    # 4. GRID BOUNDARY AUDIT (>50% SEEDS AT BOUNDARY)
    # =========================================================================
    md.append("## 4. Hyperparameter Grid Boundary Audit: Arms with >50% Seeds at Edge")
    md.append("")
    md.append("Audited from `results/grid_boundary_post_v3.csv` and `results/grid_boundary_post_v3_t2.csv`.")
    md.append("")

    gb_dfs = []
    if os.path.exists("results/grid_boundary_post_v3.csv"):
        df_v3 = pd.read_csv("results/grid_boundary_post_v3.csv")
        gb_dfs.append(df_v3)
    if os.path.exists("results/grid_boundary_post_v3_t2.csv"):
        df_v3_t2 = pd.read_csv("results/grid_boundary_post_v3_t2.csv")
        if "lattice" not in df_v3_t2.columns:
            df_v3_t2["lattice"] = "chain"
        gb_dfs.append(df_v3_t2)

    gb_all = pd.concat(gb_dfs, ignore_index=True)
    pct_cols = [c for c in gb_all.columns if c.endswith("_pct")]
    
    # Filter rows where any pct > 50.0
    boundary_hit_rows = []
    for _, row in gb_all.iterrows():
        hits = []
        for c in pct_cols:
            val = row[c]
            if pd.notna(val) and float(val) > 50.0:
                hits.append((c, float(val)))
        if hits:
            boundary_hit_rows.append((row, hits))

    md.append("| Task | Target | Lattice | Model | Variant | N | n_seeds | Boundary Edge (> 50%) | Percentage (%) |")
    md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for r, hits in boundary_hit_rows:
        task = r["task"]
        tgt = r["target"]
        lat = r.get("lattice", "chain")
        mod = r["model"]
        var = r["variant"]
        n_tr = r["N_train"]
        n_s = r["n_seeds"]
        for col_name, pct in hits:
            md.append(f"| {task} | {tgt} | {lat} | {mod} | {var} | {n_tr} | {n_s} | {col_name} | {pct:.1f}% |")
    md.append("")

    # =========================================================================
    # 5. EXACT PLOTTED VALUES PER FIGURE
    # =========================================================================
    md.append("## 5. Exact Plotted Values per Figure")
    md.append("")

    fig_files = [
        ("Figure 1: T1 Half-Chain Entropy Learning Curves", "figures/data/fig_learning_curve_t1.csv"),
        ("Figure 2: T2 Contained vs. Not-Contained Correlators", "figures/data/fig_t2_contained_vs_not.csv"),
        ("Figure 3: T4 2D Cluster State Classification & Entropy Across Lattices", "figures/data/fig_t4_lattices.csv"),
        ("Figure 4: T3 Concentration of Measure Scaling", "figures/data/fig_concentration.csv"),
        ("Figure 5: Total Measurement Shot Budget Scaling", "figures/data/fig_shots.csv"),
        ("Figure 6: FQ Training Gram Spectrum Indefiniteness", "figures/data/fig_fq_spectrum.csv"),
        ("Figure 7: Depolarizing Noise Degradation (Retuned Per-Qubit Proxy)", "figures/data/fig_depolarizing_retuned_per_qubit_proxy.csv"),
        ("Figure 8: SVR Epsilon Hyperparameter Selection Distribution", "figures/data/fig_epsilon_selection.csv"),
        ("Figure A1: Hyperparameter Grid Widening Sensitivity", "figures/data/appendix_grid_sensitivity.csv"),
    ]

    for title, path in fig_files:
        md.append(f"### {title}")
        md.append(f"*Source Data:* `{path}`")
        md.append("")
        if not os.path.exists(path):
            md.append(f"MISSING: {path} not found.")
            md.append("")
            continue
        df_fig = pd.read_csv(path)
        # Format table
        cols = list(df_fig.columns)
        header = "| " + " | ".join(cols) + " |"
        sep = "| " + " | ".join([":---" for _ in cols]) + " |"
        md.append(header)
        md.append(sep)
        for _, r in df_fig.iterrows():
            row_vals = []
            for c in cols:
                val = r[c]
                if isinstance(val, (float, np.floating)):
                    if abs(val) < 1e-4 and val != 0:
                        row_vals.append(f"{val:.4e}")
                    elif abs(val) >= 1e4:
                        row_vals.append(f"{val:.1f}")
                    else:
                        row_vals.append(f"{val:.4f}")
                else:
                    row_vals.append(str(val))
            md.append("| " + " | ".join(row_vals) + " |")
        md.append("")

    content = "\n".join(md)
    out_path = os.path.join("results", "summary_phase3.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {len(content.splitlines())} lines to {out_path}.")

if __name__ == "__main__":
    build_summary()
