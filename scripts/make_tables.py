"""
scripts/make_tables.py
Generates LaTeX tables in paper/tables/*.tex directly from results/*.csv and results/stats.csv.
Zero hand-typed empirical values.
"""
import os
import json
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
        ("PQK-1 (== RBF on <X>)", "none", "PQK-1"),
        ("PQK-2nn", "none", "PQK-2nn"),
        ("FQ", "none", "FQ"),
        ("E", "raw", "E (raw)"),
        ("E", "std", "E (std)"),
        ("E2", "raw", "E2 (raw)"),
        ("F", "std", "F (std)"),
    ]

    lines = [
        r"\begin{table}[htbp]",
        r"\caption{Task 1 Half-Chain Entropy Prediction Test $R^2$ (Mean and 95\% Bootstrap CI across 20 Seeds)}",
        r"\label{tab:t1_r2}",
        r"\centering",
        r"\begingroup",
        r"\begin{tabular}{lcccc}",
        r"\hline",
        r"\textbf{Model / Arm} & \multicolumn{2}{c}{\textbf{$N=40$}} & \multicolumn{2}{c}{\textbf{$N=160$}} \\",
        r" & Mean $R^2$ & 95\% CI & Mean $R^2$ & 95\% CI \\",
        r"\hline",
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
        r"\hline",
        r"\end{tabular}",
        r"\endgroup",
        r"\end{table}",
    ])

    out_file = os.path.join(_TABLES_DIR, "tab1_t1_r2.tex")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Wrote {out_file}")


def make_table2():
    """Table II: Confirmatory paired Wilcoxon stats (mean diff, 95% CI, p_holm_perN, rank-biserial r)."""
    print("Generating Table II (Confirmatory Paired Stats)...")
    df = pd.read_csv("results/stats.csv")
    df_conf = df[df["tier"] == "confirmatory"].copy()

    # Sort logically
    task_order = {"T1": 0, "T2b": 1, "T4a": 2, "T4b": 3}
    df_conf["task_rank"] = df_conf["task"].map(task_order)
    df_conf.sort_values(by=["task_rank", "lattice", "N_train", "model_a"], inplace=True)

    lines = [
        r"\begin{table*}[t]",
        r"\caption{Pre-declared Confirmatory Paired Comparisons: Wilcoxon Signed-Rank Test and Bootstrap Differences}",
        r"\label{tab:confirmatory_stats}",
        r"\centering",
        r"\begingroup",
        r"\setlength{\tabcolsep}{4.5pt}",
        r"\begin{tabular}{llllcccccc}",
        r"\hline",
        r"\textbf{Task} & \textbf{Lattice} & \textbf{Metric} & \textbf{Pair ($a$ vs $b$)} & \textbf{$N$} & \textbf{Mean Diff} & \textbf{95\% Bootstrap CI} & \textbf{$p_{\text{raw}}$} & \textbf{$p_{\text{holm}}$} & \textbf{Rank-Biserial $r$} \\",
        r"\hline",
    ]

    for _, r in df_conf.iterrows():
        task = r["task"]
        lat = r["lattice"]
        met = r["metric"]
        pair = f"{r['model_a']} vs {r['model_b']}"
        N_val = int(r["N_train"])
        m_diff = f"{r['mean_diff']:+.4f}"
        ci = f"[{r['ci_low']:+.4f}, {r['ci_high']:+.4f}]"
        p_raw = f"{r['p_raw']:.2e}" if r['p_raw'] < 0.001 else f"{r['p_raw']:.4f}"
        p_h = f"{r['p_holm_perN']:.2e}" if r['p_holm_perN'] < 0.001 else f"{r['p_holm_perN']:.4f}"
        r_b = f"{r['effect_size']:+.4f}"
        lines.append(f"{task} & {lat} & {met} & {pair} & {N_val} & {m_diff} & {ci} & {p_raw} & {p_h} & {r_b} \\\\")

    lines.extend([
        r"\hline",
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
        r"\begin{table}[htbp]",
        r"\caption{Measurement Shot Budget Scaling for $n=8$ TFIM System across Benchmark Arms}",
        r"\label{tab:shot_costs}",
        r"\centering",
        r"\begingroup",
        r"\begin{tabular}{lcccc}",
        r"\hline",
        r"\textbf{Model / Arm} & \textbf{Observable} & \textbf{Distinct} & \textbf{Deployed Cost} & \textbf{Full Gram Cost} \\",
        r" & \textbf{Families} & \textbf{Bases} & \textbf{($N_{\text{tr}}=40, N_{\text{te}}=200$)} & \textbf{($m=240$ states)} \\",
        r"\hline",
        r"PQK-1 & $\langle X_i \rangle, \langle Z_i \rangle$ & 2 & $480 \cdot S$ & $480 \cdot S$ \\",
        r"PQK-2nn & 1-body + NN 2-body & 3 & $720 \cdot S$ & $720 \cdot S$ \\",
        r"E (raw) & 1-body + all ZZ & 3 & $720 \cdot S$ & $720 \cdot S$ \\",
        r"E2 (raw) & 1-body + NN 2-body & 3 & $720 \cdot S$ & $720 \cdot S$ \\",
        r"F (std) & 1-body + all ZZ & 3 & $720 \cdot S$ & $720 \cdot S$ \\",
        r"FQ & Swap test & 1 & $8{,}780 \cdot S$ & $28{,}680 \cdot S$ \\",
        r"\hline",
        r"\end{tabular}",
        r"\endgroup",
        r"\end{table}",
    ]

    out_file = os.path.join(_TABLES_DIR, "tab3_shot_costs.tex")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Wrote {out_file}")


def make_table4():
    """Table IV: Grid boundary pegging summary."""
    print("Generating Table IV (Grid Boundaries)...")
    dfs = []
    if os.path.exists("results/grid_boundary_post_v3.csv"):
        dfs.append(pd.read_csv("results/grid_boundary_post_v3.csv"))
    if os.path.exists("results/grid_boundary_post_v3_t2.csv"):
        dfs.append(pd.read_csv("results/grid_boundary_post_v3_t2.csv"))

    df = pd.concat(dfs, ignore_index=True)
    pct_cols = [c for c in df.columns if c.endswith("_pct")]

    rows = []
    for _, r in df.iterrows():
        for c in pct_cols:
            val = r[c]
            if pd.notna(val) and float(val) > 50.0:
                rows.append((r["task"], r["model"], r.get("variant", "none"), int(r["N_train"]), c, float(val)))

    lines = [
        r"\begin{table}[htbp]",
        r"\caption{Hyperparameter Search Grid Boundary Pegging ($> 50\%$ of Seeds at Lower or Upper Edge)}",
        r"\label{tab:grid_boundaries}",
        r"\centering",
        r"\begingroup",
        r"\setlength{\tabcolsep}{4pt}",
        r"\begin{tabular}{llcccc}",
        r"\hline",
        r"\textbf{Task} & \textbf{Model} & \textbf{Variant} & \textbf{$N$} & \textbf{Boundary Parameter} & \textbf{\% at Edge} \\",
        r"\hline",
    ]

    for task, mod, var, N_val, col, pct in sorted(rows, key=lambda x: (x[0], x[3], x[1])):
        param_clean = col.replace("_pct", "").replace("_", " ").upper()
        mod_clean = mod.replace("_", r"\_").replace("<", r"$<$").replace(">", r"$>$")
        lines.append(f"{task} & {mod_clean} & {var} & {N_val} & {param_clean} & {pct:.1f}\\% \\\\")

    lines.extend([
        r"\hline",
        r"\end{tabular}",
        r"\endgroup",
        r"\end{table}",
    ])

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
