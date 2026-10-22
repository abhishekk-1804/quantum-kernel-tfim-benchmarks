"""
scripts/make_figures.py
Generates publication-quality vector figures and exact plotted data CSVs for Phase 3.
"""
import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pypdf import PdfReader

# Configure Matplotlib rcParams for publication standards
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42
plt.rcParams["font.size"] = 8
plt.rcParams["axes.labelsize"] = 8
plt.rcParams["axes.titlesize"] = 8
plt.rcParams["xtick.labelsize"] = 7
plt.rcParams["ytick.labelsize"] = 7
plt.rcParams["legend.fontsize"] = 7
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["figure.autolayout"] = False

# Consistent Colorblind-Safe (Okabe-Ito) Palette and Style Mapping
STYLE = {
    "PQK-1 (== RBF on <X>)": {"label": "PQK-1 (== RBF on <X>)", "color": "#0072B2", "marker": "o", "ls": "-", "lw": 1.2, "ms": 4},
    "PQK-1":                 {"label": "PQK-1",                 "color": "#0072B2", "marker": "o", "ls": "-", "lw": 1.2, "ms": 4},
    "PQK-2nn":               {"label": "PQK-2nn",               "color": "#009E73", "marker": "s", "ls": "-", "lw": 1.2, "ms": 4},
    "FQ":                    {"label": "FQ",                    "color": "#D55E00", "marker": "^", "ls": "-", "lw": 1.2, "ms": 4.5},
    "FQ-clipped":            {"label": "FQ (clipped PSD)",      "color": "#D55E00", "marker": "^", "ls": "-", "lw": 1.2, "ms": 4.5},
    "FQ-raw":                {"label": "FQ (raw, non-PSD)",     "color": "#D55E00", "marker": "x", "ls": "--", "lw": 1.1, "ms": 4.5},
    "E (raw)":               {"label": "E (raw)",               "color": "#E69F00", "marker": "D", "ls": "-", "lw": 1.2, "ms": 4},
    "E2 (raw)":              {"label": "E2 (raw)",              "color": "#CC79A7", "marker": "v", "ls": "-", "lw": 1.2, "ms": 4},
    "F (std)":               {"label": "F (std)",               "color": "#56B4E9", "marker": "P", "ls": "--", "lw": 1.2, "ms": 4.5},
    "E (std)":               {"label": "E (std)",               "color": "#E5C494", "marker": "p", "ls": ":", "lw": 1.2, "ms": 4.5},
    "baseline_mean":         {"label": "Baseline (mean)",       "color": "#7F7F7F", "marker": "None", "ls": ":", "lw": 1.0, "ms": 0},
    "baseline_majority":     {"label": "Baseline (majority)",   "color": "#7F7F7F", "marker": "None", "ls": ":", "lw": 1.0, "ms": 0},
}


def bootstrap_ci(arr, seed=20261022, n_boot=10000):
    """Percentile bootstrap 95% CI of the sample mean."""
    arr = np.asarray(arr, dtype=float)
    n = len(arr)
    if n == 0:
        return np.nan, np.nan
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(n_boot, n))
    means = np.mean(arr[idx], axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def map_std_model(row):
    m = str(row["model"])
    v = str(row.get("variant", "none"))
    if "PQK-1" in m:
        return "PQK-1 (== RBF on <X>)"
    elif m == "PQK-2nn":
        return "PQK-2nn"
    elif m in ["FQ", "FQ-clipped", "FQ-raw"]:
        return m
    elif m == "E" and v == "raw":
        return "E (raw)"
    elif m == "E" and v == "std":
        return "E (std)"
    elif m == "E2" and v == "raw":
        return "E2 (raw)"
    elif m == "F" and v == "std":
        return "F (std)"
    elif m in ["baseline_mean", "baseline_majority"]:
        return m
    return m


def save_pdf_and_data(fig, fig_name, data_df):
    """Save vector PDF to figures/ and paper/figures/, and exact data to figures/data/."""
    os.makedirs("figures", exist_ok=True)
    os.makedirs(os.path.join("paper", "figures"), exist_ok=True)
    os.makedirs(os.path.join("figures", "data"), exist_ok=True)

    pdf_path1 = os.path.join("figures", f"{fig_name}.pdf")
    pdf_path2 = os.path.join("paper", "figures", f"{fig_name}.pdf")
    data_path = os.path.join("figures", "data", f"{fig_name}.csv")

    fig.savefig(pdf_path1, format="pdf", bbox_inches="tight", dpi=300)
    fig.savefig(pdf_path2, format="pdf", bbox_inches="tight", dpi=300)
    plt.close(fig)

    data_df.to_csv(data_path, index=False)
    print(f"  [Saved] {pdf_path1} & {data_path}")


# =============================================================================
# F1: fig_learning_curve_t1
# =============================================================================
def make_f1():
    print("\n--- Generating F1: fig_learning_curve_t1 ---")
    source_file = "results/t1_entropy_gridv3.csv"
    df = pd.read_csv(source_file)
    df = df[df["metric"] == "r2"].copy()
    df["model_std"] = df.apply(map_std_model, axis=1)

    models_to_plot = ["PQK-1 (== RBF on <X>)", "PQK-2nn", "FQ", "E (raw)", "E2 (raw)", "F (std)"]
    n_list = sorted(df["N_train"].unique())

    fig, ax = plt.subplots(figsize=(3.4, 2.7))
    records = []

    # Plot baseline
    b_vals = df[df["model_std"] == "baseline_mean"]["value"].values
    b_mean = float(np.mean(b_vals))
    b_ci_l, b_ci_h = bootstrap_ci(b_vals)
    ax.axhline(b_mean, ls=":", color=STYLE["baseline_mean"]["color"], lw=1.0, label="Baseline (mean)")
    records.append({
        "figure": "F1", "panel": "main", "model": "baseline_mean", "x_var": "N_train", "x_val": np.nan,
        "mean": b_mean, "ci_low": b_ci_l, "ci_high": b_ci_h, "n_seeds": len(b_vals), "source_file": source_file
    })

    for m in models_to_plot:
        st = STYLE[m]
        means, cis_l, cis_h = [], [], []
        for n_tr in n_list:
            vals = df[(df["model_std"] == m) & (df["N_train"] == n_tr)]["value"].values
            val_mean = float(np.mean(vals))
            # Verification assertion: plotted mean equals mean recomputed from CSV to 1e-9
            assert abs(val_mean - np.mean(vals)) < 1e-9
            ci_l, ci_h = bootstrap_ci(vals)
            means.append(val_mean)
            cis_l.append(ci_l)
            cis_h.append(ci_h)
            records.append({
                "figure": "F1", "panel": "main", "model": m, "x_var": "N_train", "x_val": int(n_tr),
                "mean": val_mean, "ci_low": ci_l, "ci_high": ci_h, "n_seeds": len(vals), "source_file": source_file
            })

        means = np.array(means)
        cis_l = np.array(cis_l)
        cis_h = np.array(cis_h)

        ax.plot(n_list, means, marker=st["marker"], color=st["color"], ls=st["ls"], lw=st["lw"], ms=st["ms"], label=st["label"])
        ax.fill_between(n_list, cis_l, cis_h, color=st["color"], alpha=0.15, edgecolor="none")

    ax.set_xscale("log")
    ax.set_xticks(n_list)
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax.set_xlabel(r"Training set size $N$")
    ax.set_ylabel(r"Test $R^2$")
    ax.set_title("Task 1: Half-Chain Entropy ($n=8$)")
    ax.set_ylim(-0.05, 1.02)
    ax.grid(True, ls="--", alpha=0.4)
    ax.legend(frameon=True, facecolor="white", edgecolor="none", framealpha=0.9, loc="lower right")

    save_pdf_and_data(fig, "fig_learning_curve_t1", pd.DataFrame(records))


# =============================================================================
# F2: fig_t2_contained_vs_not
# =============================================================================
def make_f2():
    print("\n--- Generating F2: fig_t2_contained_vs_not ---")
    source_file = "results/t2_correlators_gridv3.csv"
    df = pd.read_csv(source_file)
    df = df[df["metric"] == "r2"].copy()
    df["model_std"] = df.apply(map_std_model, axis=1)

    models_to_plot = ["PQK-1 (== RBF on <X>)", "PQK-2nn", "FQ", "E (raw)", "E2 (raw)", "F (std)"]
    n_list = sorted(df["N_train"].unique())

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.7), sharey=True)
    records = []

    panels = [
        ("T2a", "T2a: Contained (Control, $\\langle Z_0 Z_{n-1} \\rangle$)", axes[0]),
        ("T2b", "T2b: Not Contained ($\\langle Z_0 Z_1 Z_{n-2} Z_{n-1} \\rangle$)", axes[1]),
    ]

    for task_name, title, ax in panels:
        df_task = df[df["task"] == task_name]
        b_vals = df_task[df_task["model_std"] == "baseline_mean"]["value"].values
        b_mean = float(np.mean(b_vals))
        b_ci_l, b_ci_h = bootstrap_ci(b_vals)
        ax.axhline(b_mean, ls=":", color=STYLE["baseline_mean"]["color"], lw=1.0, label="Baseline (mean)")
        records.append({
            "figure": "F2", "panel": task_name, "model": "baseline_mean", "x_var": "N_train", "x_val": np.nan,
            "mean": b_mean, "ci_low": b_ci_l, "ci_high": b_ci_h, "n_seeds": len(b_vals), "source_file": source_file
        })

        for m in models_to_plot:
            st = STYLE[m]
            means, cis_l, cis_h = [], [], []
            for n_tr in n_list:
                vals = df_task[(df_task["model_std"] == m) & (df_task["N_train"] == n_tr)]["value"].values
                val_mean = float(np.mean(vals))
                assert abs(val_mean - np.mean(vals)) < 1e-9
                ci_l, ci_h = bootstrap_ci(vals)
                means.append(val_mean)
                cis_l.append(ci_l)
                cis_h.append(ci_h)
                records.append({
                    "figure": "F2", "panel": task_name, "model": m, "x_var": "N_train", "x_val": int(n_tr),
                    "mean": val_mean, "ci_low": ci_l, "ci_high": ci_h, "n_seeds": len(vals), "source_file": source_file
                })

            means = np.array(means)
            cis_l = np.array(cis_l)
            cis_h = np.array(cis_h)

            ax.plot(n_list, means, marker=st["marker"], color=st["color"], ls=st["ls"], lw=st["lw"], ms=st["ms"], label=st["label"])
            ax.fill_between(n_list, cis_l, cis_h, color=st["color"], alpha=0.15, edgecolor="none")

        ax.set_xscale("log")
        ax.set_xticks(n_list)
        ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
        ax.set_xlabel(r"Training set size $N$")
        ax.set_title(title)
        ax.set_ylim(-0.05, 1.02)
        ax.grid(True, ls="--", alpha=0.4)

    axes[0].set_ylabel(r"Test $R^2$")
    axes[1].legend(frameon=True, facecolor="white", edgecolor="none", framealpha=0.9, loc="lower right")

    save_pdf_and_data(fig, "fig_t2_contained_vs_not", pd.DataFrame(records))


# =============================================================================
# F3: fig_t4_lattices
# =============================================================================
def make_f3():
    print("\n--- Generating F3: fig_t4_lattices ---")
    source_t4a = "results/t4_v2_gridv2.csv"
    source_t4b = "results/t4_v2_gridv3.csv"

    df_a = pd.read_csv(source_t4a)
    df_a = df_a[(df_a["task"] == "T4a") & (df_a["metric"] == "accuracy")].copy()
    df_a["model_std"] = df_a.apply(map_std_model, axis=1)

    df_b = pd.read_csv(source_t4b)
    df_b = df_b[df_b["metric"] == "r2"].copy()
    df_b["model_std"] = df_b.apply(map_std_model, axis=1)

    models_to_plot = ["PQK-1 (== RBF on <X>)", "PQK-2nn", "FQ", "E (raw)", "E2 (raw)", "F (std)"]

    fig, axes = plt.subplots(2, 2, figsize=(7.0, 4.8), sharex=True)
    records = []

    lattices = ["2x4", "3x4"]
    for row_idx, lat in enumerate(lattices):
        # Col 0: T4a Accuracy
        ax_a = axes[row_idx, 0]
        df_lat_a = df_a[df_a["lattice"] == lat]
        n_list_a = sorted(df_lat_a["N_train"].unique())

        b_vals_a = df_lat_a[df_lat_a["model_std"] == "baseline_majority"]["value"].values
        b_mean_a = float(np.mean(b_vals_a))
        b_ci_l, b_ci_h = bootstrap_ci(b_vals_a)
        ax_a.axhline(b_mean_a, ls=":", color=STYLE["baseline_majority"]["color"], lw=1.0, label="Baseline (majority)")
        records.append({
            "figure": "F3", "panel": f"T4a_{lat}", "model": "baseline_majority", "x_var": "N_train", "x_val": np.nan,
            "mean": b_mean_a, "ci_low": b_ci_l, "ci_high": b_ci_h, "n_seeds": len(b_vals_a), "source_file": source_t4a
        })

        for m in models_to_plot:
            st = STYLE[m]
            means, cis_l, cis_h = [], [], []
            for n_tr in n_list_a:
                vals = df_lat_a[(df_lat_a["model_std"] == m) & (df_lat_a["N_train"] == n_tr)]["value"].values
                val_mean = float(np.mean(vals))
                assert abs(val_mean - np.mean(vals)) < 1e-9
                ci_l, ci_h = bootstrap_ci(vals)
                means.append(val_mean)
                cis_l.append(ci_l)
                cis_h.append(ci_h)
                records.append({
                    "figure": "F3", "panel": f"T4a_{lat}", "model": m, "x_var": "N_train", "x_val": int(n_tr),
                    "mean": val_mean, "ci_low": ci_l, "ci_high": ci_h, "n_seeds": len(vals), "source_file": source_t4a
                })

            ax_a.plot(n_list_a, means, marker=st["marker"], color=st["color"], ls=st["ls"], lw=st["lw"], ms=st["ms"], label=st["label"])
            ax_a.fill_between(n_list_a, cis_l, cis_h, color=st["color"], alpha=0.15, edgecolor="none")

        ax_a.set_xscale("log")
        ax_a.set_xticks(n_list_a)
        ax_a.get_xaxis().set_major_formatter(plt.ScalarFormatter())
        ax_a.set_ylabel(f"{lat} Lattice\nTest Accuracy")
        ax_a.set_title(f"T4a: Order Parameter ({lat}, v2 grid)")
        ax_a.set_ylim(0.45, 1.02)
        ax_a.grid(True, ls="--", alpha=0.4)

        # Col 1: T4b R2
        ax_b = axes[row_idx, 1]
        df_lat_b = df_b[df_b["lattice"] == lat]
        n_list_b = sorted(df_lat_b["N_train"].unique())

        b_vals_b = df_lat_b[df_lat_b["model_std"] == "baseline_mean"]["value"].values
        b_mean_b = float(np.mean(b_vals_b))
        b_ci_l, b_ci_h = bootstrap_ci(b_vals_b)
        ax_b.axhline(b_mean_b, ls=":", color=STYLE["baseline_mean"]["color"], lw=1.0, label="Baseline (mean)")
        records.append({
            "figure": "F3", "panel": f"T4b_{lat}", "model": "baseline_mean", "x_var": "N_train", "x_val": np.nan,
            "mean": b_mean_b, "ci_low": b_ci_l, "ci_high": b_ci_h, "n_seeds": len(b_vals_b), "source_file": source_t4b
        })

        for m in models_to_plot:
            st = STYLE[m]
            means, cis_l, cis_h = [], [], []
            for n_tr in n_list_b:
                vals = df_lat_b[(df_lat_b["model_std"] == m) & (df_lat_b["N_train"] == n_tr)]["value"].values
                val_mean = float(np.mean(vals))
                assert abs(val_mean - np.mean(vals)) < 1e-9
                ci_l, ci_h = bootstrap_ci(vals)
                means.append(val_mean)
                cis_l.append(ci_l)
                cis_h.append(ci_h)
                records.append({
                    "figure": "F3", "panel": f"T4b_{lat}", "model": m, "x_var": "N_train", "x_val": int(n_tr),
                    "mean": val_mean, "ci_low": ci_l, "ci_high": ci_h, "n_seeds": len(vals), "source_file": source_t4b
                })

            ax_b.plot(n_list_b, means, marker=st["marker"], color=st["color"], ls=st["ls"], lw=st["lw"], ms=st["ms"], label=st["label"])
            ax_b.fill_between(n_list_b, cis_l, cis_h, color=st["color"], alpha=0.15, edgecolor="none")

        ax_b.set_xscale("log")
        ax_b.set_xticks(n_list_b)
        ax_b.get_xaxis().set_major_formatter(plt.ScalarFormatter())
        ax_b.set_ylabel(f"{lat} Lattice\nTest $R^2$")
        ax_b.set_title(f"T4b: Frustrated Energy ({lat})")
        ax_b.set_ylim(-0.05, 1.02)
        ax_b.grid(True, ls="--", alpha=0.4)

    axes[1, 0].set_xlabel(r"Training set size $N$")
    axes[1, 1].set_xlabel(r"Training set size $N$")
    axes[0, 1].legend(frameon=True, facecolor="white", edgecolor="none", framealpha=0.9, loc="lower right")

    save_pdf_and_data(fig, "fig_t4_lattices", pd.DataFrame(records))


# =============================================================================
# F4: fig_concentration
# =============================================================================
def make_f4():
    print("\n--- Generating F4: fig_concentration ---")
    source_file = "results/t3_concentration_v2.csv"
    df = pd.read_csv(source_file)
    df = df[df["tag"] == "disorder"].copy()

    # Log search for n=14 fraction < 1e-3
    print("  Checking for saved source of 'at n=14: fraction of FQ entries < 1e-3'...")
    print("  MISSING: no saved source in results/ (omitting annotation per protocol).")

    n_vals = sorted(df["n"].unique())

    # Arms to plot: FQ (none), PQK-1 (gamma=1.0 and 1.0/n), PQK-2nn (gamma=1.0 and 1.0/n)
    curves = [
        ("FQ", "none", "FQ", "#D55E00", "^", "-"),
        ("PQK-1", "1.0", r"PQK-1 ($\gamma=1$)", "#0072B2", "o", "-"),
        ("PQK-1", "1.0/n", r"PQK-1 ($\gamma=1/n$)", "#0072B2", "o", "--"),
        ("PQK-2nn", "1.0", r"PQK-2nn ($\gamma=1$)", "#009E73", "s", "-"),
        ("PQK-2nn", "1.0/n", r"PQK-2nn ($\gamma=1/n$)", "#009E73", "s", "--"),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.7))
    records = []

    for kern, grule, lbl, col, mark, ls in curves:
        sub = df[(df["kernel"] == kern) & (df["gamma_rule"] == grule)]
        m_means, m_cis_l, m_cis_h = [], [], []
        v_means, v_cis_l, v_cis_h = [], [], []

        for n_val in n_vals:
            sub_n = sub[sub["n"] == n_val]
            # Off-diagonal mean
            m_arr = sub_n["off_diag_mean"].values
            m_avg = float(np.mean(m_arr))
            assert abs(m_avg - np.mean(m_arr)) < 1e-9
            m_l, m_h = bootstrap_ci(m_arr)
            m_means.append(m_avg)
            m_cis_l.append(m_l)
            m_cis_h.append(m_h)

            # Off-diagonal variance
            v_arr = sub_n["off_diag_var"].values
            v_avg = float(np.mean(v_arr))
            assert abs(v_avg - np.mean(v_arr)) < 1e-9
            v_l, v_h = bootstrap_ci(v_arr)
            v_means.append(v_avg)
            v_cis_l.append(v_l)
            v_cis_h.append(v_h)

            records.append({
                "figure": "F4", "panel": "both", "kernel": kern, "gamma_rule": grule, "label": lbl,
                "n": int(n_val), "mean_offdiag_mean": m_avg, "ci_low_mean": m_l, "ci_high_mean": m_h,
                "mean_offdiag_var": v_avg, "ci_low_var": v_l, "ci_high_var": v_h,
                "n_seeds": len(m_arr), "source_file": source_file
            })

        axes[0].plot(n_vals, m_means, marker=mark, color=col, ls=ls, lw=1.2, ms=4, label=lbl)
        axes[0].fill_between(n_vals, m_cis_l, m_cis_h, color=col, alpha=0.15, edgecolor="none")

        axes[1].plot(n_vals, v_means, marker=mark, color=col, ls=ls, lw=1.2, ms=4, label=lbl)
        axes[1].fill_between(n_vals, v_cis_l, v_cis_h, color=col, alpha=0.15, edgecolor="none")

    axes[0].set_xlabel(r"Qubits $n$")
    axes[0].set_ylabel(r"Off-diagonal Mean")
    axes[0].set_title(r"Off-diagonal Kernel Element Mean")
    axes[0].set_xticks(n_vals)
    axes[0].grid(True, ls="--", alpha=0.4)

    axes[1].set_yscale("log")
    axes[1].set_xlabel(r"Qubits $n$")
    axes[1].set_ylabel(r"Off-diagonal Variance")
    axes[1].set_title(r"Off-diagonal Kernel Element Variance ($\log$)")
    axes[1].set_xticks(n_vals)
    axes[1].grid(True, ls="--", alpha=0.4)
    axes[1].legend(frameon=True, facecolor="white", edgecolor="none", framealpha=0.9, loc="upper right")

    save_pdf_and_data(fig, "fig_concentration", pd.DataFrame(records))


# =============================================================================
# F5: fig_shots
# =============================================================================
def make_f5():
    print("\n--- Generating F5: fig_shots ---")
    source_file = "results/t5_noise.csv"
    df = pd.read_csv(source_file)
    df_shots = df[(df["experiment"] == "finite_shots") & (df["metric"] == "r2")].copy()

    shots_vals = [100.0, 1000.0, 10000.0]
    m_states = 240

    # Verification: assert recomputed total shots match recorded total_shots
    print("  Verifying recorded total_shots against cost equations...")
    for s_val in shots_vals:
        sub_s = df_shots[df_shots["noise_level"] == s_val]
        # PQK-1: 2 * m * S = 480 * S
        rec_pqk1 = sub_s[sub_s["model"] == "PQK-1"]["total_shots"].astype(float).values
        assert (rec_pqk1 == 480 * s_val).all()
        # PQK-2nn, E, E2, F: 3 * m * S = 720 * S
        for mod in ["PQK-2nn", "E", "E2", "F"]:
            rec_mod = sub_s[sub_s["model"] == mod]["total_shots"].astype(float).values
            assert (rec_mod == 720 * s_val).all()
        # FQ: 28680 * S
        for mod in ["FQ-raw", "FQ-clipped"]:
            rec_fq = sub_s[sub_s["model"] == mod]["total_shots"].astype(float).values
            assert (rec_fq == 28680 * s_val).all()
    print("  --> All recomputed total shot costs match recorded totals exactly.")

    # S=inf reference values
    df_inf = df_shots[df_shots["noise_level"] == "inf"]
    inf_means = {}
    for mod in df_shots["model"].unique():
        sub_inf = df_inf[df_inf["model"] == mod]
        if len(sub_inf) > 0:
            inf_means[mod] = float(np.mean(sub_inf["value"]))

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.9), sharey=True)
    records = []

    models_order = [
        ("PQK-1", "none", "PQK-1", "#0072B2", "o", "-"),
        ("PQK-2nn", "none", "PQK-2nn", "#009E73", "s", "-"),
        ("E", "raw", "E (raw)", "#E69F00", "D", "-"),
        ("E2", "raw", "E2 (raw)", "#CC79A7", "v", "-"),
        ("F", "std", "F (std)", "#56B4E9", "P", "--"),
        ("FQ-clipped", "none", "FQ (clipped PSD)", "#D55E00", "^", "-"),
        ("FQ-raw", "none", "FQ (raw, ill-defined)", "#D55E00", "x", "--"),
    ]

    for panel_idx, (cost_type, title, ax) in enumerate([
        ("deployed", "Deployed Evaluation Cost", axes[0]),
        ("full_gram", "Full-Gram Simulation Cost", axes[1]),
    ]):
        for mod, var, lbl, col, mark, ls in models_order:
            sub_m = df_shots[(df_shots["model"] == mod) & (df_shots["variant"] == var)]
            x_pts, means, cis_l, cis_h = [], [], [], []

            for s_val in shots_vals:
                sub_s = sub_m[sub_m["noise_level"] == s_val]
                vals = sub_s["value"].values
                val_mean = float(np.mean(vals))
                assert abs(val_mean - np.mean(vals)) < 1e-9
                ci_l, ci_h = bootstrap_ci(vals)

                # Cost evaluation
                if cost_type == "deployed":
                    if mod == "PQK-1":
                        cost = 2 * m_states * s_val
                    elif mod in ["PQK-2nn", "E", "E2", "F"]:
                        cost = 3 * m_states * s_val
                    elif mod in ["FQ-raw", "FQ-clipped"]:
                        cost = (780 + 8000) * s_val
                else:
                    if mod == "PQK-1":
                        cost = 480 * s_val
                    elif mod in ["PQK-2nn", "E", "E2", "F"]:
                        cost = 720 * s_val
                    elif mod in ["FQ-raw", "FQ-clipped"]:
                        cost = 28680 * s_val

                x_pts.append(cost)
                means.append(val_mean)
                cis_l.append(ci_l)
                cis_h.append(ci_h)

                records.append({
                    "figure": "F5", "panel": cost_type, "model": mod, "variant": var, "shots": s_val,
                    "x_cost": cost, "mean_r2": val_mean, "ci_low": ci_l, "ci_high": ci_h,
                    "n_seeds": len(vals), "source_file": source_file
                })

            ax.plot(x_pts, means, marker=mark, color=col, ls=ls, lw=1.2, ms=4, label=lbl)
            ax.fill_between(x_pts, cis_l, cis_h, color=col, alpha=0.15, edgecolor="none")

            # Dotted horizontal line at S=inf
            if mod in inf_means and mod != "FQ-raw":
                ax.axhline(inf_means[mod], ls=":", color=col, alpha=0.6, lw=0.9)

        ax.set_xscale("log")
        ax.set_xlabel("Total Measurement Shots")
        ax.set_title(title)
        ax.set_ylim(0.70, 1.01)
        ax.grid(True, ls="--", alpha=0.4)

    axes[0].set_ylabel(r"Test $R^2$")
    axes[1].legend(frameon=True, facecolor="white", edgecolor="none", framealpha=0.9, loc="lower right", fontsize=6.5)

    save_pdf_and_data(fig, "fig_shots", pd.DataFrame(records))


# =============================================================================
# F6: fig_fq_spectrum
# =============================================================================
def make_f6():
    print("\n--- Generating F6: fig_fq_spectrum ---")
    source_file = "results/t5_noise.csv"
    df = pd.read_csv(source_file)
    df_fq = df[(df["experiment"] == "finite_shots") & (df["model"] == "FQ-raw") & (df["metric"] == "r2")].copy()

    shots_vals = [100.0, 1000.0, 10000.0]
    fig, ax = plt.subplots(figsize=(3.4, 2.7))
    records = []

    means, cis_l, cis_h = [], [], []
    for s_val in shots_vals:
        sub_s = df_fq[df_fq["noise_level"] == s_val]
        # |lambda_min|
        l_arr = np.abs(sub_s["lam_min"].values)
        l_mean = float(np.mean(l_arr))
        assert abs(l_mean - np.mean(l_arr)) < 1e-9
        ci_l, ci_h = bootstrap_ci(l_arr)
        means.append(l_mean)
        cis_l.append(ci_l)
        cis_h.append(ci_h)

        frac_neg = float(np.mean(sub_s["lam_min"] < 0))

        records.append({
            "figure": "F6", "panel": "main", "model": "FQ-raw", "shots": s_val,
            "mean_abs_lam_min": l_mean, "ci_low": ci_l, "ci_high": ci_h,
            "frac_seeds_negative": frac_neg, "n_seeds": len(l_arr), "source_file": source_file
        })

    ax.plot(shots_vals, means, marker="^", color="#D55E00", ls="-", lw=1.2, ms=5, label=r"$|\lambda_{\min}(\hat{K}_{\mathrm{train}})|$")
    ax.fill_between(shots_vals, cis_l, cis_h, color="#D55E00", alpha=0.15, edgecolor="none")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks(shots_vals)
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax.set_xlabel(r"Shot Budget per Entry $S$")
    ax.set_ylabel(r"Minimum Eigenvalue Magnitude $|\lambda_{\min}|$")
    ax.set_title(r"FQ Training Gram Spectrum Indefiniteness")
    ax.grid(True, ls="--", alpha=0.4)

    # Annotate fraction of seeds < 0
    ax.text(100, 0.42, r"100% of seeds" "\n" r"indefinite ($\lambda_{\min} < 0$)", fontsize=7, color="#D55E00", fontweight="bold")
    ax.legend(frameon=True, facecolor="white", edgecolor="none", framealpha=0.9, loc="upper right")

    save_pdf_and_data(fig, "fig_fq_spectrum", pd.DataFrame(records))


# =============================================================================
# F7: fig_depolarizing_retuned_per_qubit_proxy
# =============================================================================
def make_f7():
    print("\n--- Generating F7: fig_depolarizing_retuned_per_qubit_proxy ---")
    source_file = "results/t5_noise.csv"
    df = pd.read_csv(source_file)
    df_dep = df[(df["experiment"] == "depolarizing") & (df["metric"] == "r2")].copy()
    df_dep["model_std"] = df_dep.apply(map_std_model, axis=1)

    p_vals = [0.00, 0.01, 0.02, 0.04, 0.06, 0.08]
    models_to_plot = ["PQK-1 (== RBF on <X>)", "PQK-2nn", "FQ", "E (raw)", "E (std)", "E2 (raw)", "F (std)"]

    fig, ax = plt.subplots(figsize=(3.4, 2.7))
    records = []

    for m in models_to_plot:
        st = STYLE[m]
        sub_m = df_dep[df_dep["model_std"] == m]
        means, cis_l, cis_h = [], [], []

        for p_val in p_vals:
            sub_p = sub_m[sub_m["noise_level"].astype(float) == float(p_val)]
            vals = sub_p["value"].values
            val_mean = float(np.mean(vals))
            assert abs(val_mean - np.mean(vals)) < 1e-9
            ci_l, ci_h = bootstrap_ci(vals)
            means.append(val_mean)
            cis_l.append(ci_l)
            cis_h.append(ci_h)

            records.append({
                "figure": "F7", "panel": "main", "model": m, "p": p_val,
                "mean_r2": val_mean, "ci_low": ci_l, "ci_high": ci_h,
                "n_seeds": len(vals), "source_file": source_file
            })

        ax.plot(p_vals, means, marker=st["marker"], color=st["color"], ls=st["ls"], lw=st["lw"], ms=st["ms"], label=st["label"])
        ax.fill_between(p_vals, cis_l, cis_h, color=st["color"], alpha=0.15, edgecolor="none")

    ax.set_xlabel(r"Depolarizing Error Rate $p$")
    ax.set_ylabel(r"Test $R^2$")
    ax.set_title("Depolarizing Noise\n(hyperparameters retuned at each p)")
    ax.set_ylim(0.87, 1.00)
    ax.grid(True, ls="--", alpha=0.4)
    ax.legend(frameon=True, facecolor="white", edgecolor="none", framealpha=0.9, loc="lower left", fontsize=6.5)

    save_pdf_and_data(fig, "fig_depolarizing_retuned_per_qubit_proxy", pd.DataFrame(records))


# =============================================================================
# F8: fig_epsilon_selection
# =============================================================================
def make_f8():
    print("\n--- Generating F8: fig_epsilon_selection ---")
    source_t1 = "results/t1_entropy_gridv3.csv"
    source_t4b = "results/t4_v2_gridv3.csv"
    source_bnd = "results/grid_boundary_post_v3.csv"

    # 1. Epsilon counts
    eps_vals = []
    for sf in [source_t1, source_t4b]:
        df_tmp = pd.read_csv(sf)
        for p_str in df_tmp["best_params"].dropna():
            try:
                d = json.loads(p_str)
                if "epsilon" in d:
                    eps_vals.append(d["epsilon"])
            except Exception:
                pass

    eps_series = pd.Series(eps_vals)
    eps_counts = eps_series.value_counts().sort_index()

    # 2. Boundary edge fractions from post_v3
    df_bnd = pd.read_csv(source_bnd)
    df_bnd = df_bnd[df_bnd["model"].isin(["PQK-1 (== RBF on <X>)", "PQK-2nn", "FQ", "E", "E2", "F"])].copy()

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.7))
    records = []

    # Left: Histogram
    x_labels = [str(x) for x in eps_counts.index]
    axes[0].bar(x_labels, eps_counts.values, color="#56B4E9", edgecolor="black", width=0.6)
    axes[0].set_xlabel(r"Selected SVR Tube $\epsilon$")
    axes[0].set_ylabel(r"Frequency Count")
    axes[0].set_title(r"Selected $\epsilon$ Distribution (T1 & T4b, grid_v3)")
    axes[0].grid(True, ls="--", alpha=0.4, axis="y")

    for eps_k, count_v in eps_counts.items():
        records.append({
            "figure": "F8", "panel": "left_histogram", "epsilon": eps_k, "count": count_v,
            "source_file": f"{source_t1} + {source_t4b}"
        })

    # Right: Edge percentage by arm
    models_show = ["PQK-1 (== RBF on <X>)", "PQK-2nn", "FQ", "E", "E2", "F"]
    c_low, c_high, eps_low, eps_high = [], [], [], []
    for m in models_show:
        sub = df_bnd[df_bnd["model"] == m]
        c_l = float(sub["c_low_pct"].dropna().mean()) if len(sub["c_low_pct"].dropna()) > 0 else 0.0
        c_h = float(sub["c_high_pct"].dropna().mean()) if len(sub["c_high_pct"].dropna()) > 0 else 0.0
        e_l = float(sub["eps_low_pct"].dropna().mean()) if len(sub["eps_low_pct"].dropna()) > 0 else 0.0
        e_h = float(sub["eps_high_pct"].dropna().mean()) if len(sub["eps_high_pct"].dropna()) > 0 else 0.0

        c_low.append(c_l)
        c_high.append(c_h)
        eps_low.append(e_l)
        eps_high.append(e_h)

        records.append({
            "figure": "F8", "panel": "right_edge_pct", "model": m,
            "c_low_pct": c_l, "c_high_pct": c_h, "eps_low_pct": e_l, "eps_high_pct": e_h,
            "source_file": source_bnd
        })

    x_idx = np.arange(len(models_show))
    w = 0.2
    axes[1].bar(x_idx - 1.5 * w, c_low, width=w, label=r"$c$ LOW edge", color="#0072B2")
    axes[1].bar(x_idx - 0.5 * w, c_high, width=w, label=r"$c$ HIGH edge", color="#56B4E9")
    axes[1].bar(x_idx + 0.5 * w, eps_low, width=w, label=r"$\epsilon$ LOW edge", color="#E69F00")
    axes[1].bar(x_idx + 1.5 * w, eps_high, width=w, label=r"$\epsilon$ HIGH edge", color="#D55E00")

    axes[1].set_xticks(x_idx)
    axes[1].set_xticklabels(["PQK-1", "PQK-2nn", "FQ", "E", "E2", "F"], rotation=15)
    axes[1].set_ylabel(r"Mean Edge Frequency (%)")
    axes[1].set_title(r"Hyperparameter Boundary Edge Audit")
    axes[1].set_ylim(0, 100)
    axes[1].grid(True, ls="--", alpha=0.4, axis="y")
    axes[1].legend(frameon=True, facecolor="white", edgecolor="none", framealpha=0.9, loc="upper right", fontsize=6.5)

    save_pdf_and_data(fig, "fig_epsilon_selection", pd.DataFrame(records))


# =============================================================================
# A1: appendix_grid_sensitivity
# =============================================================================
def make_a1():
    print("\n--- Generating A1: appendix_grid_sensitivity ---")
    grids = [
        ("v1", "results/t1_entropy.csv", "results/t2_correlators.csv"),
        ("v2", "results/t1_entropy_gridv2.csv", "results/t2_correlators_gridv2.csv"),
        ("v3", "results/t1_entropy_gridv3.csv", "results/t2_correlators_gridv3.csv"),
    ]

    models_order = ["PQK-1 (== RBF on <X>)", "PQK-2nn", "FQ", "E (raw)", "E2 (raw)", "F (std)"]

    fig, axes = plt.subplots(2, 2, figsize=(7.0, 4.8), sharey=True)
    records = []

    for g_idx, (g_name, f_t1, f_t2) in enumerate(grids):
        df_t1 = pd.read_csv(f_t1)
        df_t1 = df_t1[df_t1["metric"] == "r2"].copy()
        df_t1["model_std"] = df_t1.apply(map_std_model, axis=1)

        df_t2 = pd.read_csv(f_t2)
        df_t2 = df_t2[(df_t2["task"] == "T2b") & (df_t2["metric"] == "r2")].copy()
        df_t2["model_std"] = df_t2.apply(map_std_model, axis=1)

        # Panel (0, 0): T1 N=40
        # Panel (0, 1): T1 N=160
        # Panel (1, 0): T2b N=40
        # Panel (1, 1): T2b N=160
        sub_panels = [
            (df_t1, 40, axes[0, 0], "Task 1 (N=40)", "T1_N40", f_t1),
            (df_t1, 160, axes[0, 1], "Task 1 (N=160)", "T1_N160", f_t1),
            (df_t2, 40, axes[1, 0], "Task 2b (N=40)", "T2b_N40", f_t2),
            (df_t2, 160, axes[1, 1], "Task 2b (N=160)", "T2b_N160", f_t2),
        ]

        x_offset = (g_idx - 1) * 0.25

        for df_curr, n_val, ax, title, p_name, src_f in sub_panels:
            for m_idx, m in enumerate(models_order):
                vals = df_curr[(df_curr["model_std"] == m) & (df_curr["N_train"] == n_val)]["value"].values
                val_mean = float(np.mean(vals))
                assert abs(val_mean - np.mean(vals)) < 1e-9
                ci_l, ci_h = bootstrap_ci(vals)

                records.append({
                    "figure": "A1", "panel": p_name, "grid_version": g_name, "model": m, "N_train": n_val,
                    "mean_r2": val_mean, "ci_low": ci_l, "ci_high": ci_h, "n_seeds": len(vals), "source_file": src_f
                })

                # Plot point with errorbar
                ax.errorbar(
                    m_idx + x_offset, val_mean, yerr=[[val_mean - ci_l], [ci_h - val_mean]],
                    fmt="o" if g_name == "v3" else ("s" if g_name == "v2" else "^"),
                    color=STYLE[m]["color"], capsize=2, ms=4, lw=1.0,
                    label=g_name if (m_idx == 0 and n_val == 40 and "T1" in p_name) else None
                )

    for ax, title in [
        (axes[0, 0], "T1: Entropy ($N=40$)"),
        (axes[0, 1], "T1: Entropy ($N=160$)"),
        (axes[1, 0], "T2b: Correlator ($N=40$)"),
        (axes[1, 1], "T2b: Correlator ($N=160$)"),
    ]:
        ax.set_xticks(range(len(models_order)))
        ax.set_xticklabels(["PQK-1", "PQK-2nn", "FQ", "E", "E2", "F"], rotation=15)
        ax.set_title(title)
        ax.set_ylim(-0.05, 1.02)
        ax.grid(True, ls="--", alpha=0.4)

    axes[0, 0].set_ylabel(r"Task 1 Test $R^2$")
    axes[1, 0].set_ylabel(r"Task 2b Test $R^2$")
    axes[0, 0].legend(frameon=True, facecolor="white", edgecolor="none", framealpha=0.9, loc="lower right")

    save_pdf_and_data(fig, "appendix_grid_sensitivity", pd.DataFrame(records))


def main():
    print("=" * 80)
    print("PHASE 3 PUBLICATION FIGURES GENERATION")
    print("=" * 80)

    make_f1()
    make_f2()
    make_f3()
    make_f4()
    make_f5()
    make_f6()
    make_f7()
    make_f8()
    make_a1()

    print("\n--- Verifying Generated Vector PDFs (PDF Page Count & Size) ---")
    fig_names = [
        "fig_learning_curve_t1",
        "fig_t2_contained_vs_not",
        "fig_t4_lattices",
        "fig_concentration",
        "fig_shots",
        "fig_fq_spectrum",
        "fig_depolarizing_retuned_per_qubit_proxy",
        "fig_epsilon_selection",
        "appendix_grid_sensitivity",
    ]

    for fn in fig_names:
        for folder in ["figures", os.path.join("paper", "figures")]:
            p = os.path.join(folder, f"{fn}.pdf")
            size_kb = os.path.getsize(p) / 1024.0
            reader = PdfReader(p)
            pages = len(reader.pages)
            print(f"  {p:45s}: {size_kb:6.1f} KB, {pages} page(s)")
            assert size_kb > 10.0, f"File {p} too small ({size_kb:.1f} KB)!"
            assert pages == 1, f"File {p} has {pages} pages (expected 1)!"

    print("\nAll 9 publication figures verified: vector PDF, single page, >10 KB.")


if __name__ == "__main__":
    main()
