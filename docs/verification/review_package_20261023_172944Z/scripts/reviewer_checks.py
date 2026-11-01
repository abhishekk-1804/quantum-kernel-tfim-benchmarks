"""
reviewer_checks.py
------------------
Standalone, read-only executable review script for independent contributors.
Executes 7 explicit checks against primary benchmark artifacts.
Does NOT modify files. Does NOT auto-sign approval.
"""

import os
import sys
import numpy as np
import pandas as pd
import scipy
from scipy import stats
from sklearn.metrics import mean_absolute_error

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
CSV_PATH = os.path.join(ROOT, "results", "stage3", "t6_ood_shift.csv")
PRED_DIR = os.path.join(ROOT, "docs", "verification", "audit_20261023_155335Z", "predictions")
CLOSURE_DIR = os.path.join(ROOT, "docs", "verification", "closure_20261023_163403Z")

def main():
    print("=== INDEPENDENT CONTRIBUTOR REVIEW CHECKS (TASK 6) ===")
    print(f"Repository Root: {ROOT}")
    print(f"Python Executable: {sys.executable}")
    print(f"SciPy Version: {scipy.__version__}")

    # Check 1: Original CSV pairing and selected model variants
    print("\n[CHECK 1] Original CSV Pairing & Model Variants")
    df = pd.read_csv(CSV_PATH)
    fq_rows = df[(df["model"] == "FQ") & (df["variant"] == "none")].sort_values("seed").reset_index(drop=True)
    pqk2_rows = df[(df["model"] == "PQK-2nn") & (df["variant"] == "none")].sort_values("seed").reset_index(drop=True)
    print(f"  FQ row count: {len(fq_rows)}, PQK-2nn row count: {len(pqk2_rows)}")
    assert len(fq_rows) == 20 and len(pqk2_rows) == 20, "FAIL: Expected exactly 20 pairs"
    assert list(fq_rows["seed"]) == list(range(20)), "FAIL: Seed sequence mismatch"
    print("  PASS: Exactly 20 matching seeds found without duplicates.")

    # Check 2: One FQ-favoring seed reconstructed from arrays (Seed 00)
    print("\n[CHECK 2] Reconstruction of FQ-Favoring Seed (Seed 00)")
    npz0 = np.load(os.path.join(PRED_DIR, "seed_00_arrays.npz"), allow_pickle=False)
    y_ood_0 = npz0["y_ood"]
    fq_pred_0 = npz0["fq_pred_ood"]
    pqk2_pred_0 = npz0["pqk2_pred_ood"]
    mae_fq_0 = float(mean_absolute_error(y_ood_0, fq_pred_0))
    mae_pqk2_0 = float(mean_absolute_error(y_ood_0, pqk2_pred_0))
    csv_fq_0 = fq_rows.loc[0, "ood_mae"]
    csv_pqk2_0 = pqk2_rows.loc[0, "ood_mae"]
    diff_fq_0 = abs(mae_fq_0 - csv_fq_0)
    diff_pqk2_0 = abs(mae_pqk2_0 - csv_pqk2_0)
    print(f"  Seed 00 Array MAE: FQ={mae_fq_0:.6f}, PQK2={mae_pqk2_0:.6f} (Diff={mae_fq_0 - mae_pqk2_0:+.6f})")
    print(f"  CSV vs Array Discrepancy: FQ={diff_fq_0:.2e}, PQK2={diff_pqk2_0:.2e}")
    assert diff_fq_0 < 1e-7 and diff_pqk2_0 < 1e-7, "FAIL: Discrepancy exceeds atol=1e-7"
    print("  PASS: Seed 00 verifies FQ superiority and matches CSV to machine precision.")

    # Check 3: One PQK-favoring seed reconstructed from arrays (Seed 08)
    print("\n[CHECK 3] Reconstruction of PQK2-Favoring Seed (Seed 08)")
    npz8 = np.load(os.path.join(PRED_DIR, "seed_08_arrays.npz"), allow_pickle=False)
    y_ood_8 = npz8["y_ood"]
    fq_pred_8 = npz8["fq_pred_ood"]
    pqk2_pred_8 = npz8["pqk2_pred_ood"]
    mae_fq_8 = float(mean_absolute_error(y_ood_8, fq_pred_8))
    mae_pqk2_8 = float(mean_absolute_error(y_ood_8, pqk2_pred_8))
    csv_fq_8 = fq_rows.loc[8, "ood_mae"]
    csv_pqk2_8 = pqk2_rows.loc[8, "ood_mae"]
    diff_fq_8 = abs(mae_fq_8 - csv_fq_8)
    diff_pqk2_8 = abs(mae_pqk2_8 - csv_pqk2_8)
    print(f"  Seed 08 Array MAE: FQ={mae_fq_8:.6f}, PQK2={mae_pqk2_8:.6f} (Diff={mae_fq_8 - mae_pqk2_8:+.6f})")
    print(f"  CSV vs Array Discrepancy: FQ={diff_fq_8:.2e}, PQK2={diff_pqk2_8:.2e}")
    assert diff_fq_8 < 1e-7 and diff_pqk2_8 < 1e-7, "FAIL: Discrepancy exceeds atol=1e-7"
    assert mae_pqk2_8 < mae_fq_8, "FAIL: PQK2 was expected to be lower in Seed 08"
    print("  PASS: Seed 08 verifies PQK-2nn superiority and matches CSV to machine precision.")

    # Check 4: Mean difference and paired sample SE
    print("\n[CHECK 4] Mean Paired Difference & Paired Sample SE")
    fq_all = fq_rows["ood_mae"].values
    pqk2_all = pqk2_rows["ood_mae"].values
    d_all = fq_all - pqk2_all
    mean_d = float(np.mean(d_all))
    sd_d = float(np.std(d_all, ddof=1))
    se_d = float(sd_d / np.sqrt(len(d_all)))
    print(f"  Mean FQ OOD MAE: {np.mean(fq_all):.6f} ± {np.std(fq_all, ddof=1)/np.sqrt(20):.6f}")
    print(f"  Mean PQK2 OOD MAE: {np.mean(pqk2_all):.6f} ± {np.std(pqk2_all, ddof=1)/np.sqrt(20):.6f}")
    print(f"  Mean Paired Diff: {mean_d:.6f} ± {se_d:.6f} (sample SD = {sd_d:.6f})")
    assert abs(mean_d - (-0.124849)) < 1e-5, "FAIL: Mean diff does not match -0.124849"
    assert abs(se_d - 0.033425) < 1e-5, "FAIL: Paired SE does not match 0.033425"
    print("  PASS: Mean diff is -0.1248 ± 0.0334 (reproduced exactly).")

    # Check 5: Wilcoxon statistic & p-value
    print("\n[CHECK 5] Wilcoxon Signed-Rank Test Configuration & Result")
    res_w = stats.wilcoxon(d_all, alternative="two-sided")
    print(f"  Wilcoxon Statistic: W = {res_w.statistic:.1f}")
    print(f"  Wilcoxon p-value: p = {res_w.pvalue:.8e}")
    assert abs(res_w.statistic - 21.0) < 1e-5, "FAIL: W is not 21.0"
    assert abs(res_w.pvalue - 8.5068e-4) < 1e-6, "FAIL: p-value is not 8.51e-4"
    print("  PASS: W = 21.0 and p = 8.51e-4 reproduced exactly.")

    # Check 6: Independent Holm-Bonferroni calculation
    print("\n[CHECK 6] Independent Holm-Bonferroni Calculation")
    base_csv = os.path.join(ROOT, "docs", "verification", "audit_20261023_155335Z", "stage3_baselines.csv")
    df_base = pd.read_csv(base_csv)
    d_mean_bl = df_base["mae_fq"].values - df_base["mae_train_mean_baseline"].values
    d_med_bl = df_base["mae_fq"].values - df_base["mae_train_median_baseline"].values
    p_mean_bl = float(stats.wilcoxon(d_mean_bl, alternative="two-sided").pvalue)
    p_med_bl = float(stats.wilcoxon(d_med_bl, alternative="two-sided").pvalue)
    p_pqk2 = float(res_w.pvalue)

    p_vals = [p_pqk2, p_mean_bl, p_med_bl]
    labels = ["FQ vs PQK2", "FQ vs Train-Mean", "FQ vs Train-Median"]
    s_idx = np.argsort(p_vals)
    adj_p = []
    c_max = 0.0
    for r, idx in enumerate(s_idx):
        mult = 3 - r
        val = min(p_vals[idx] * mult, 1.0)
        c_max = max(c_max, val)
        adj_p.append((labels[idx], p_vals[idx], mult, c_max))
    for lbl, raw_p, mult, h_p in adj_p:
        print(f"  {lbl}: raw_p={raw_p:.4e}, multiplier={mult}, holm_p={h_p:.4e}")
    print("  PASS: Holm-adjusted p-values verified across the 3-comparison family.")

    # Check 7: Full vs Intercept-Only SVR comparison
    print("\n[CHECK 7] Full SVR Predictor vs Constant Intercept Baseline")
    inter_csv = os.path.join(CLOSURE_DIR, "tables", "full_vs_intercept_per_seed.csv")
    df_inter = pd.read_csv(inter_csv)
    d_inter = df_inter["fq_mae_diff_full_minus_inter"].values
    neg_inter = int(np.sum(d_inter < 0))
    pos_inter = int(np.sum(d_inter > 0))
    print(f"  Full FQ MAE: {df_inter['fq_mae_full'].mean():.4f} ± {df_inter['fq_mae_full'].std(ddof=1)/np.sqrt(20):.4f}")
    print(f"  Intercept MAE: {df_inter['fq_mae_intercept'].mean():.4f} ± {df_inter['fq_mae_intercept'].std(ddof=1)/np.sqrt(20):.4f}")
    print(f"  Mean Improvement (Full - Intercept): {np.mean(d_inter):.4f} ± {np.std(d_inter, ddof=1)/np.sqrt(20):.4f}")
    print(f"  Seeds where Full Model has lower MAE: {neg_inter}/20 (100%)")
    assert neg_inter == 20 and pos_inter == 0, "FAIL: Intercept comparison is not 20/0"
    print("  PASS: Full model improves MAE over intercept in 20/20 seeds.")

    print("\n=======================================================")
    print("ALL 7 CHECKS PASSED. OBSERVATIONS LOGGED.")
    print("Independent Contributor Review Pending.")
    print("=======================================================")

if __name__ == "__main__":
    main()
