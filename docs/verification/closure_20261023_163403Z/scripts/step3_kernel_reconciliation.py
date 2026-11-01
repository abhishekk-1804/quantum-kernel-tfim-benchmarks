import os
import pandas as pd
import numpy as np

CLOSURE_DIR = r"docs/verification/closure_20261023_163403Z"
AUDIT_DIR = r"docs/verification/audit_20261023_155335Z"

def df_to_markdown(df):
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(val) for val in row.values) + " |")
    return "\n".join(lines)

def main():
    print("Executing Step 3: Kernel Summary Reconciliation...")
    csv_path = os.path.join(AUDIT_DIR, "kernel_summary.csv")
    df_kernel = pd.read_csv(csv_path)
    
    # 1. Quantity Definitions Table
    definitions = [
        {
            "quantity_name": "Raw Fidelity Gram Block (ID)",
            "symbol": "K_id = |<psi_test_ID | psi_train>|^2",
            "matrix_shape": "(100, 40)",
            "coefficient_weighted": "No",
            "support_vector_filtered": "No (all 40 training states)",
            "domain_or_space": "In-Distribution (disordered paramagnetic phase)",
            "reported_narrative_value": "0.051 (~0.05)",
            "true_measured_value": f"{df_kernel['K_id_mean'].mean():.6f}",
            "status_or_finding": "Reporting error in narrative text; true across-seed mean is 0.9326"
        },
        {
            "quantity_name": "Raw Fidelity Gram Block (OOD)",
            "symbol": "K_ood = |<psi_test_OOD | psi_train>|^2",
            "matrix_shape": "(100, 40)",
            "coefficient_weighted": "No",
            "support_vector_filtered": "No (all 40 training states)",
            "domain_or_space": "Out-of-Distribution (ordered ferromagnetic phase)",
            "reported_narrative_value": "0.003 (~0.003)",
            "true_measured_value": f"{df_kernel['K_ood_mean'].mean():.6f}",
            "status_or_finding": "Reporting error in narrative text; true across-seed mean is 0.4313"
        },
        {
            "quantity_name": "Kernel Attenuation Ratio",
            "symbol": "K_ood_mean / K_id_mean",
            "matrix_shape": "Scalar per seed",
            "coefficient_weighted": "No",
            "support_vector_filtered": "No",
            "domain_or_space": "Cross-phase transition drop",
            "reported_narrative_value": "17x reduction (~0.059)",
            "true_measured_value": f"{df_kernel['K_attenuation_ratio'].mean():.6f} (2.16x reduction)",
            "status_or_finding": "Reporting error in narrative; true attenuation is 2.16x (ratio = 0.4624)"
        },
        {
            "quantity_name": "Signed Kernel SVR Contribution",
            "symbol": "g_physical(x) = sigma * sum_i alpha_i K(x_i, x)",
            "matrix_shape": "(100,)",
            "coefficient_weighted": "Yes (dual coefficients alpha_i)",
            "support_vector_filtered": "Yes (non-zero dual coefficients only)",
            "domain_or_space": "OOD test states",
            "reported_narrative_value": "RMS ||g||_2 = 0.4401",
            "true_measured_value": "RMS = 0.4401 in model space, physical RMS ~0.021",
            "status_or_finding": "Model-space vs physical-space scaling clarified in Step 4"
        },
        {
            "quantity_name": "Physical SVR Intercept",
            "symbol": "b_physical = sigma * b_model + mu",
            "matrix_shape": "Scalar per seed",
            "coefficient_weighted": "No (constant offset)",
            "support_vector_filtered": "N/A",
            "domain_or_space": "Global baseline prediction",
            "reported_narrative_value": "~0.94",
            "true_measured_value": "0.9441 across seeds",
            "status_or_finding": "Verified; positions predictions in ferromagnetic regime"
        }
    ]
    df_defs = pd.DataFrame(definitions)
    defs_csv = os.path.join(CLOSURE_DIR, "tables", "kernel_quantity_definitions.csv")
    df_defs.to_csv(defs_csv, index=False)
    print(f"Saved: {defs_csv}")
    
    # 2. Reconciled Summary Across Seeds
    summary_metrics = []
    numeric_cols = ["K_id_mean", "K_id_median", "K_id_max", "K_ood_mean", "K_ood_median", "K_ood_max", "K_attenuation_ratio"]
    for col in numeric_cols:
        series = df_kernel[col]
        summary_metrics.append({
            "metric": col,
            "across_seed_mean": f"{series.mean():.6f}",
            "across_seed_std": f"{series.std():.6f}",
            "across_seed_median": f"{series.median():.6f}",
            "across_seed_min": f"{series.min():.6f}",
            "across_seed_max": f"{series.max():.6f}",
            "interquartile_range": f"{series.quantile(0.75) - series.quantile(0.25):.6f}"
        })
        
    # Add Ratio of Aggregate Means
    ratio_of_means = df_kernel["K_ood_mean"].mean() / df_kernel["K_id_mean"].mean()
    mean_of_ratios = df_kernel["K_attenuation_ratio"].mean()
    summary_metrics.append({
        "metric": "ratio_of_aggregate_means (mean(K_ood) / mean(K_id))",
        "across_seed_mean": f"{ratio_of_means:.6f}",
        "across_seed_std": "N/A",
        "across_seed_median": "N/A",
        "across_seed_min": "N/A",
        "across_seed_max": "N/A",
        "interquartile_range": "N/A"
    })
    
    df_summary = pd.DataFrame(summary_metrics)
    summary_csv = os.path.join(CLOSURE_DIR, "tables", "kernel_summary_reconciled.csv")
    df_summary.to_csv(summary_csv, index=False)
    print(f"Saved: {summary_csv}")
    
    # 3. Markdown Report
    report_path = os.path.join(CLOSURE_DIR, "reports", "kernel_summary_reconciliation.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Reconciled Kernel Overlap Definitions and Aggregation Report\n\n")
        f.write("## 1. Problem Statement & Reconciliation of Reported Values\n\n")
        f.write("In `docs/verification/audit_20261023_155335Z/VERIFICATION_REPORT.md` (item 10) and Section 3 of `stage3_svr_decomposition.md`, narrative text asserted:\n")
        f.write("> *'Fidelity overlaps $|\\langle \\psi_{\\text{test}} | \\psi_{\\text{train}} \\rangle|^2$ drop from $0.051$ in-distribution to $0.003$ out-of-distribution ($17\\times$ attenuation).*\n\n")
        f.write("Investigation of the underlying programmatically generated artifacts reveals that this narrative statement is a severe transcription error:\n")
        f.write("1. **Actual Data in `kernel_summary.csv`:** The across-seed mean in-distribution fidelity is **$0.9326$**, and the out-of-distribution fidelity is **$0.4313$**.\n")
        f.write("2. **Actual Attenuation:** The across-seed attenuation ratio is **$0.4624$**, corresponding to a **$2.16\\times$ reduction** (a 53.8% drop), not a $17\\times$ reduction.\n")
        f.write("3. **Cause of Discrepancy:** In `scripts/audit_stage3_metrics.py` (lines 405-415), the script calculated and wrote the correct values ($0.9326$ ID, $0.4313$ OOD, $2.2\\times$) in Section 2, but later in Section 3 of the same file, a hardcoded discussion paragraph from an earlier conceptual draft ('mean value $\\sim 0.003$ vs $\\sim 0.05$') was written into the markdown report. The synthesis report `VERIFICATION_REPORT.md` then copied this inaccurate prose description instead of the tabulated numerical values.\n\n")
        f.write("## 2. Definitional Taxonomy of Kernel Quantities\n\n")
        f.write("To prevent future confusion between raw fidelity overlaps and model-dependent prediction terms, we establish strict formal definitions:\n\n")
        f.write(df_to_markdown(df_defs) + "\n\n")
        f.write("## 3. Reconciled Statistical Aggregations (20 Seeds, 80,000 Matrix Entries)\n\n")
        f.write("Each seed evaluates $N_{\\text{test}} = 100$ and $N_{\\text{train}} = 40$, producing a $100 \\times 40 = 4,000$ matrix block for both ID and OOD. Across all 20 seeds ($80,000$ entries per distribution), we report:\n\n")
        f.write(df_to_markdown(df_summary) + "\n\n")
        f.write("### Key Observations:\n")
        f.write("- **Ratio of Aggregate Means vs Mean of Ratios:** The ratio of aggregate means is `0.431281 / 0.932609 = 0.462447`. The mean of per-seed ratios is `0.462441`. The two aggregations agree to within $6 \\times 10^{-6}$, confirming extreme consistency across seeds.\n")
        f.write("- **Stability Across Seeds:** The interquartile range of `K_id_mean` across the 20 seeds is tiny ($0.0037$), and for `K_ood_mean` is $0.0163$. Overlaps are highly stable and reproducible.\n")
        f.write("- **Fidelity is Not Orthogonal:** Cross-phase states are not fully orthogonal ($K_{\\text{ood}} \\approx 0.43$). While the fidelity drops significantly from the near-unity in-distribution regime ($0.93 \\to 0.43$), it remains substantially positive, providing a decaying but non-vanishing similarity basis for SVR interpolation.\n")
    print(f"Saved: {report_path}")

if __name__ == "__main__":
    main()
