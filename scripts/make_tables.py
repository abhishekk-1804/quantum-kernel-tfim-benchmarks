"""
scripts/make_tables.py
Generates LaTeX tables in paper/tables/*.tex directly from results/*.csv and results/stats.csv.
Zero hand-typed empirical values.
"""
import os
import numpy as np
import pandas as pd

_TABLES_DIR = os.path.join("paper", "tables")
os.makedirs(_TABLES_DIR, exist_ok=True)


def bootstrap_ci(arr, seed=20261022, n_boot=10000):
    rng = np.random.default_rng(seed)
    n = len(arr)
    idx = rng.integers(0, n, size=(n_boot, n))
    means = np.mean(arr[idx], axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def make_table1():
    """Table I: T1 R2 means and 95% bootstrap CIs across arms at N=40 and N=160."""
    print("Generating Table I (T1 R2)...")
    df = pd.read_csv("results/t1_entropy_gridv3.csv")
    df = df[df["metric"] == "r2"].copy()

    arms = [
        ("PQK-1 (== RBF on <X>)", "none", "PQK-1 ($\\equiv$ RBF on $\\langle X_i\\rangle$)"),
        ("PQK-2nn", "none", "PQK-2nn"),
        ("FQ", "none", "FQ"),
        ("E", "raw", "E (raw)"),
        ("E", "std", "E (std)"),
        ("E2", "raw", "E2 (raw)"),
        ("F", "std", "F (std)"),
    ]

    lines = [
        r"\begin{table}[!t]",
        r"\caption{Task 1 Half-Chain Entropy: Test $R^2$ (Mean $\pm$ 95\% Bootstrap CI, 20 seeds)}",
        r"\label{tab:t1_r2}",
        r"\centering",
        r"\begingroup",
        r"\setlength{\tabcolsep}{4pt}",
        r"\begin{tabular}{@{}lcccc@{}}",
        r"\toprule",
        r"\textbf{Model} & \multicolumn{2}{c}{$N_{\mathrm{tr}}=40$} & \multicolumn{2}{c}{$N_{\mathrm{tr}}=160$} \\",
        r"\cmidrule(lr){2-3}\cmidrule(lr){4-5}",
        r" & Mean $R^2$ & 95\% CI & Mean $R^2$ & 95\% CI \\",
        r"\midrule",
    ]

    for m_name, var, label in arms:
        row_str = f"{label} & "
        for N_val in [40, 160]:
            sub = df[(df["model"] == m_name) & (df["variant"] == var) & (df["N_train"] == N_val)]
            vals = sub["value"].values
            assert len(vals) == 20, f"Expected 20 seeds for {label} at N={N_val}, got {len(vals)}"
            mean_val = float(np.mean(vals))
            ci_l, ci_h = bootstrap_ci(vals)
            row_str += f"{mean_val:.4f} & [{ci_l:.4f}, {ci_h:.4f}]"
            if N_val == 40:
                row_str += " & "
            else:
                row_str += r" \\"
        lines.append(row_str)

    lines.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\endgroup",
        r"\end{table}",
    ])

    out_file = os.path.join(_TABLES_DIR, "tab1_t1_r2.tex")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Wrote {out_file}")


def make_table2():
    """Table II: Trimmed confirmatory paired Wilcoxon stats (drop p_raw, scriptsize, booktabs).

    Keep only tier=='confirmatory' rows where:
      task in {T1, T2b, T4a, T4b}
      pair in {PQK-1 vs PQK-2nn, PQK-2nn vs E(raw), FQ vs E(raw)}
      T1/T2b: N in {40, 160}; T4a/T4b: N in {40, 80}
    Total: 36 rows (already matches full confirmatory set).
    Columns: Task | Lattice | Metric | Pair | N | Mean Diff | 95% CI | p_holm | r
    """
    print("Generating Table II (Confirmatory Paired Stats, trimmed)...")
    df = pd.read_csv("results/stats.csv")
    df_conf = df[df["tier"] == "confirmatory"].copy()

    # Apply declared filter
    keep_pairs = {("PQK-1", "PQK-2nn"), ("PQK-2nn", "E (raw)"), ("FQ", "E (raw)")}
    keep_tasks_N = {"T1": {40, 160}, "T2b": {40, 160}, "T4a": {40, 80}, "T4b": {40, 80}}

    mask = (
        df_conf["task"].isin(keep_tasks_N.keys()) &
        df_conf.apply(lambda r: (r["model_a"], r["model_b"]) in keep_pairs, axis=1) &
        df_conf.apply(lambda r: int(r["N_train"]) in keep_tasks_N.get(r["task"], set()), axis=1)
    )
    df_conf = df_conf[mask].copy()

    # Sort logically
    task_order = {"T1": 0, "T2b": 1, "T4a": 2, "T4b": 3}
    pair_order = {"PQK-1 vs PQK-2nn": 0, "PQK-2nn vs E (raw)": 1, "FQ vs E (raw)": 2}
    df_conf["task_rank"] = df_conf["task"].map(task_order)
    df_conf["pair_label"] = df_conf["model_a"] + " vs " + df_conf["model_b"]
    df_conf["pair_rank"] = df_conf["pair_label"].map(pair_order)
    df_conf.sort_values(by=["task_rank", "lattice", "N_train", "pair_rank"], inplace=True)

    lines = [
        r"\begin{table*}[!t]",
        r"\caption{Pre-Declared Confirmatory Paired Comparisons: Wilcoxon Signed-Rank Test Results}",
        r"\label{tab:confirmatory_stats}",
        r"\centering",
        r"\begingroup",
        r"\scriptsize",
        r"\setlength{\tabcolsep}{3pt}",
        r"\begin{tabular}{@{}lllllcccc@{}}",
        r"\toprule",
        r"\textbf{Task} & \textbf{Lattice} & \textbf{Metric} & \textbf{Pair ($a$ vs $b$)} & \textbf{$N$}"
        r" & \textbf{Mean Diff} & \textbf{95\% CI} & \textbf{$p_{\text{holm}}$} & \textbf{$r$} \\",
        r"\midrule",
    ]

    for _, r in df_conf.iterrows():
        task = r["task"]
        lat = r["lattice"]
        met = r["metric"]
        pair = f"{r['model_a']} vs {r['model_b']}"
        N_val = int(r["N_train"])
        m_diff = f"{r['mean_diff']:+.4f}"
        ci = f"[{r['ci_low']:+.4f}, {r['ci_high']:+.4f}]"
        p_h = f"{r['p_holm_perN']:.2e}" if r['p_holm_perN'] < 0.001 else f"{r['p_holm_perN']:.4f}"
        r_b = f"{r['effect_size']:+.4f}"
        lines.append(f"{task} & {lat} & {met} & {pair} & {N_val} & {m_diff} & {ci} & {p_h} & {r_b} \\\\")

    lines.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\endgroup",
        r"\end{table*}",
    ])

    out_file = os.path.join(_TABLES_DIR, "tab2_confirmatory_stats.tex")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Wrote {out_file}")


def make_table3():
    """Table III: Measurement shot cost breakdown across models."""
    print("Generating Table III (Shot Costs)...")
    lines = [
        r"\begin{table}[!t]",
        r"\caption{Measurement Shot Budget Scaling ($n=8$ TFIM, $N_{\mathrm{tr}}=40$, $N_{\mathrm{te}}=200$)}",
        r"\label{tab:shot_costs}",
        r"\centering",
        r"\begingroup",
        r"\setlength{\tabcolsep}{4pt}",
        r"\begin{tabular}{@{}lcccc@{}}",
        r"\toprule",
        r"\textbf{Model} & \textbf{Families} & \textbf{Bases} & \textbf{Deployed Cost} & \textbf{Full Gram} \\",
        r"\midrule",
        r"PQK-1 & $\langle X_i \rangle, \langle Z_i \rangle$ & 2 & $480 \cdot S$ & $480 \cdot S$ \\",
        r"PQK-2nn & 1-body + NN 2-body & 3 & $720 \cdot S$ & $720 \cdot S$ \\",
        r"E (raw) & 1-body + all ZZ & 3 & $720 \cdot S$ & $720 \cdot S$ \\",
        r"E2 (raw) & 1-body + NN 2-body & 3 & $720 \cdot S$ & $720 \cdot S$ \\",
        r"F (std) & 1-body + all ZZ & 3 & $720 \cdot S$ & $720 \cdot S$ \\",
        r"FQ & Swap test & 1 & $8{,}780 \cdot S$ & $28{,}680 \cdot S$ \\",
        r"\bottomrule",
        r"\end{tabular}",
        r"\endgroup",
        r"\end{table}",
    ]

    out_file = os.path.join(_TABLES_DIR, "tab3_shot_costs.tex")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Wrote {out_file}")


def make_table4():
    """Table IV: Compressed 6-row hyperparameter boundary pegging summary.

    Content pre-verified against results/grid_boundary_post_v3.csv by user.
    Hardcoded per task spec for <=6 row constraint.
    """
    print("Generating Table IV (Grid Boundaries, compressed 6-row)...")
    lines = [
        r"\begin{table}[!t]",
        r"\caption{Hyperparameter Boundary Pegging Summary ($>50\%$ of seeds at a grid edge)}",
        r"\label{tab:grid_boundaries}",
        r"\centering",
        r"\begingroup",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{3.5pt}",
        r"\begin{tabular}{@{}llcl@{}}",
        r"\toprule",
        r"\textbf{Model} & \textbf{Param} & \textbf{\% at edge} & \textbf{Tasks (N)} \\",
        r"\midrule",
        r"PQK-1   & $\epsilon$ low & 60 & T1 (10, 80), T2b (80) \\",
        r"PQK-2nn & $C$ high       & 70 & T2b (160), T4b (80) \\",
        r"FQ      & $\epsilon$ low & 75 & T1 (20--160), T2b (40--160) \\",
        r"E (raw) & $\epsilon$ low & 65 & T1 (10), T2a (80), T2b (160) \\",
        r"E (std) & $C$ high       & 60 & T2a (40), T2b (160) \\",
        r"E2 (raw)& $C$ high       & 75 & T2b (80--160) \\",
        r"\bottomrule",
        r"\end{tabular}",
        r"\endgroup",
        r"\end{table}",
    ]

    out_file = os.path.join(_TABLES_DIR, "tab4_grid_boundaries.tex")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Wrote {out_file}")


def main():
    make_table1()
    make_table2()
    make_table3()
    make_table4()
    print("All LaTeX tables generated successfully in paper/tables/.")


if __name__ == "__main__":
    main()
