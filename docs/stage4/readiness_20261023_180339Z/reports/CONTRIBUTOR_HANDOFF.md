# Stage 4 Contributor Review Handoff: Task 6 Verification
**Workspace:** `D:\quantum-kernel-tfim-benchmarks`  
**Package:** `docs/stage4/readiness_20261023_180339Z/`  
**Review Status:** **Independent contributor review pending**  
**Classification:** Handoff specification and review instructions; not independent human approval.

---

## 1. Objective and Review Protocol
This document provides an independent human contributor with exact, executable instructions to verify Task 6 (Controlled Out-of-Distribution Phase-Shift Generalization) without performing benchmark sweeps or modifying repository files.

All automated verification checks executed locally are classified as **readiness checks**. Independent human review requires verifying the evidence trail, executing the read-only check script, and recording findings in the sign-off block below.

---

## 2. Discovered Artifact Paths and Schemas

- **Primary Results CSV:**  
  [`results/stage3/t6_ood_shift.csv`](file:///d:/quantum-kernel-tfim-benchmarks/results/stage3/t6_ood_shift.csv)  
  *Schema:* `seed, model, variant, id_r2, id_mae, ood_r2, ood_mae, delta_r2, best_params, inner_cv_score` (100 rows: 20 seeds across 5 models).
- **Saved Raw Prediction Arrays:**  
  [`docs/verification/audit_20261023_155335Z/predictions/`](file:///d:/quantum-kernel-tfim-benchmarks/docs/verification/audit_20261023_155335Z/predictions/)  
  *Files:* `seed_00_arrays.npz` through `seed_19_arrays.npz` (20 files, `allow_pickle=False`).  
  *Keys:* `y_train`, `y_id`, `y_ood`, `fq_pred_id`, `fq_pred_ood`, `pqk1_pred_id`, `pqk1_pred_ood`, `pqk2_pred_id`, `pqk2_pred_ood`, `e2_pred_id`, `e2_pred_ood`, `ridge_pred_id`, `ridge_pred_ood`, `fq_dual_coef`, `fq_support`, `fq_intercept`, `fq_K_tr`, `fq_K_id`, `fq_K_ood`, `pqk2_dual_coef`, `pqk2_support`, `pqk2_intercept`, `pqk2_K_tr`, `pqk2_K_id`, `pqk2_K_ood`.
- **Reviewer Checks Helper:**  
  [`docs/verification/review_package_20261023_172944Z/scripts/reviewer_checks.py`](file:///d:/quantum-kernel-tfim-benchmarks/docs/verification/review_package_20261023_172944Z/scripts/reviewer_checks.py)

---

## 3. Core Verification Points

### 3.1 Original CSV Pairing & Sample Integrity
- Filter: `model in ['FQ', 'PQK-2nn']` in `results/stage3/t6_ood_shift.csv`.
- Exactly 20 matching seeds (0 through 19) without duplicates or missing values.

### 3.2 Machine-Precision Spot Checks on Saved Arrays (atol=1e-7, rtol=0)
Calculated from raw target vector `y_ood` and model prediction vectors:
- **Seed 00 (FQ-Favoring Seed):**
  * FQ Array OOD MAE: `0.030009` | CSV `ood_mae`: `0.030009` (Discrepancy: $6.25 \times 10^{-17}$)
  * PQK-2nn Array OOD MAE: `0.199973` | CSV `ood_mae`: `0.199973` (Discrepancy: $8.33 \times 10^{-17}$)
  * Paired Difference: $-0.169964$ (FQ achieves $6.66\times$ lower error).
- **Seed 08 (PQK-Favoring Seed):**
  * FQ Array OOD MAE: `0.070931` | CSV `ood_mae`: `0.070931` (Discrepancy: $2.78 \times 10^{-17}$)
  * PQK-2nn Array OOD MAE: `0.054557` | CSV `ood_mae`: `0.054557` (Discrepancy: $4.16 \times 10^{-17}$)
  * Paired Difference: $+0.016374$ (PQK-2nn achieves $1.30\times$ lower error).

### 3.3 Paired Mean Difference & Empirical Sample Standard Errors
Computed with sample standard deviation degree of freedom `ddof=1` across $N=20$ seeds:
- **Mean FQ OOD MAE:** $0.060181 \approx \mathbf{0.0602}$, Sample SD $= 0.038100$, Sample SE $= \mathbf{0.008519} \approx \mathbf{0.0085}$.
- **Mean PQK-2nn OOD MAE:** $0.185030 \approx \mathbf{0.1850}$, Sample SD $= 0.131658$, Sample SE $= \mathbf{0.029440} \approx \mathbf{0.0294}$.
- **Mean Paired Difference ($d = \text{FQ} - \text{PQK}$):** $-0.124849 \approx \mathbf{-0.1248}$, Sample SD $= 0.149481$, Sample SE $= \mathbf{0.033425} \approx \mathbf{0.0334}$.

### 3.4 Wilcoxon Signed-Rank Test Configuration and Output
Using exact parameters: `scipy.stats.wilcoxon(fq_mae, pqk_mae, alternative='two-sided', zero_method='wilcox', correction=False)`:
- Sum of positive ranks ($d > 0$, where PQK beats FQ: seeds 8, 9, 11, 16): $W = 4 + 7 + 8 + 2 = \mathbf{21.0}$.
- Exact two-sided p-value: $p = \mathbf{8.5068 \times 10^{-4}}$.

### 3.5 Complete Retrospective Holm-Bonferroni Family ($m=3$)
All comparisons evaluated against FQ OOD MAE across the 20 seeds:
1. **FQ vs Train-Mean Baseline:** Baseline MAE $= 0.6061 \pm 0.0075$, $W = 0.0$, Raw $p = 1.9073 \times 10^{-6}$, Multiplier $= 3$, Holm $p = \mathbf{5.7220 \times 10^{-6}}$.
2. **FQ vs Train-Median Baseline:** Baseline MAE $= 0.6121 \pm 0.0086$, $W = 0.0$, Raw $p = 1.9073 \times 10^{-6}$, Multiplier $= 2$, Holm $p = \mathbf{5.7220 \times 10^{-6}}$.
3. **FQ vs PQK-2nn:** PQK MAE $= 0.1850 \pm 0.0294$, $W = 21.0$, Raw $p = 8.5068 \times 10^{-4}$, Multiplier $= 1$, Holm $p = \mathbf{8.5068 \times 10^{-4}}$.

### 3.6 Full SVR Predictor vs Constant Intercept-Only Baseline
- Full FQ SVR MAE: $0.0602 \pm 0.0085$.
- Intercept-Only MAE: $0.4616 \pm 0.0162$.
- Mean Improvement (Full - Intercept): $-0.4014 \pm 0.0156$ ($W = 0.0, p = 1.9073 \times 10^{-6}$).
- Seeds where Full Model has lower MAE: **20 / 20 seeds (100%)**.

---

## 4. Contradicted Historical Values Recorded and Superseded

| Historical Claim | Verified Empirical Value | Resolution & Cause |
| :--- | :--- | :--- |
| FQ OOD MAE SE: `0.0039` | **`0.0085`** | **Contradicted.** Historical SE does not reproduce from data. |
| PQK-2nn OOD MAE SE: `0.0154` | **`0.0294`** | **Contradicted.** Historical SE does not reproduce from data. |
| Paired Diff SE: `0.0166` | **`0.0334`** | **Contradicted.** True paired sample SE is approximately $2\times$ larger. |
| Intercept OOD MAE SE: `0.0042` | **`0.0162`** | **Contradicted.** Historical value was In-Distribution MAE SE. |
| Wilcoxon $W = 1.0$ for OOD MAE | **`W = 21.0`** | **Contradicted.** $W=1.0$ was the In-Distribution (ID) comparison. |
| Wilcoxon $p = 7.08 \times 10^{-4}$ | **`p = 8.51e-4`** | **Contradicted.** $7.08 \times 10^{-4}$ was the OOD $R^2$ test ($W=20.0$). |
| "FQ lower in all 20 seeds" | **16 / 20 seeds** | **Contradicted.** PQK-2nn is superior in 4 seeds (Seeds 8, 9, 11, 16). |

---

## 5. Independent Human Contributor Review & Approval Block

> [!IMPORTANT]
> This block must be completed by an independent human contributor. All automated execution remains classified as local readiness checks until this block is signed.

- **Reviewer Name:** `________________________________________`
- **Affiliation / Role:** `________________________________________`
- **Date of Review:** `____________________`
- **Independent Calculations Performed:**  
  `[ ]` Verified raw CSV pairing in `results/stage3/t6_ood_shift.csv`  
  `[ ]` Executed `reviewer_checks.py` independently  
  `[ ]` Verified Seed 00 and Seed 08 array reconstruction  
  `[ ]` Computed paired difference sample mean and standard error ($ddof=1$)  
  `[ ]` Executed Wilcoxon signed-rank test and Holm adjustments  
  `[ ]` Verified Full SVR vs Intercept baseline superiority (20/20 seeds)  
- **Reviewer Findings & Remarks:**  
  `__________________________________________________________________________`  
  `__________________________________________________________________________`  
- **Scope of Approval:**  
  `[ ]` Approved for manuscript text and table integration in Stage 5  
  `[ ]` Approved with reservations / qualifications noted above  
  `[ ]` Rejected / Additional clarification required  
- **Reviewer Signature / Formal Sign-Off:** `________________________________________`
