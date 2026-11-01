# Superseding Correction Record: Task 6 (OOD Phase-Shift Generalization)

**Document Creation UTC:** `2026-10-23T17:39:27.232228+00:00`  
**Status:** Prepared for independent review  
**Review Approval:** Independent human review pending (no approval signature)  
**Evidence Package References:**
- Primary Reconciliation: `docs/verification/paired_mae_check_20261023_171155Z`
- Audit Reference: `docs/verification/audit_20261023_155335Z`
- Closure Package: `docs/verification/closure_20261023_163403Z`

---

## Mandatory Evidentiary Corrections

### Correction 1: Wilcoxon Test Statistic W=1 Belongs to ID MAE, Not OOD MAE
- **Historical Discrepancy:** Multiple narrative summaries and review queries asserted a Wilcoxon statistic of $W = 1.0$ for the primary out-of-distribution MAE comparison.
- **Authoritative Finding:** Two-sided Wilcoxon testing on the 20-seed paired OOD MAE vector yields **$W = 21.0$** (sum of 4 positive ranks: $2 + 4 + 3 + 12 = 21.0$).
- **Etiology:** $W = 1.0$ is the exact Wilcoxon statistic for the **In-Distribution (ID) MAE** comparison (`id_mae` in `results/stage3/t6_ood_shift.csv`), where FQ is lower than PQK-2nn in 19 seeds and higher in 1 seed of rank 1 ($W = 1.0, p = 3.81 \times 10^{-6}$). Early drafts conflated ID and OOD statistics.

### Correction 2: Misattribution of OOD R² P-Value (7.08e-4) to MAE
- **Historical Discrepancy:** Early candidate summaries (`docs/stage3/ood_findings.md` line 211) and synthesis reports (`VERIFICATION_REPORT.md` Table 1) cited $p = 7.08 \times 10^{-4}$ alongside MAE values.
- **Authoritative Finding:** Two-sided Wilcoxon testing on OOD MAE yields $p = 8.5068 \times 10^{-4}$ (**`8.51e-4`**).
- **Etiology:** In `scripts/stage3_analysis.py` (line 139), the script computed Wilcoxon testing on **`ood_r2`**, yielding $W = 20.0, p = 7.0763 \times 10^{-4}$. Narrative prose in line 211 inadvertently quoted this $R^2$ p-value in a sentence discussing MAE.

### Correction 3: Authoritative OOD MAE Wilcoxon Statistic and P-Value
- **Authoritative Values:** For FQ vs PQK-2nn OOD MAE across $N=20$ seeds:
  - Wilcoxon test statistic: **$W = 21.0$**
  - Raw two-sided p-value: **$p = 8.5068 \times 10^{-4}$** (`8.51e-4`)
  - Holm-adjusted p-value (in 3-comparison family): **$p_{\text{holm}} = 8.5068 \times 10^{-4}$** (`8.51e-4`)

### Correction 4: FQ vs PQK-2nn Direction is 16/4, Not 20/0
- **Historical Discrepancy:** Certain narrative draft claims stated or implied that FQ outperformed PQK-2nn across all evaluated seeds.
- **Authoritative Finding:** In `results/stage3/t6_ood_shift.csv`, FQ achieves lower MAE in **16 seeds**, while PQK-2nn achieves lower MAE in **4 seeds** (Seeds 8, 9, 11, 16). The 20/0 claim applies strictly to Full FQ vs its own Intercept-only baseline, NOT FQ vs PQK-2nn.

### Correction 5: Exclusion of Manual Seed Table from Evidentiary Record
- **Historical Discrepancy:** A hand-composed seed summary table in early discussions presented approximate or rounded values that did not match machine-readable CSVs.
- **Authoritative Action:** In accordance with Section 0 Rule 6, all manual seed tables are explicitly excluded from the evidentiary baseline. Only `results/stage3/t6_ood_shift.csv` and `predictions/seed_XX_arrays.npz` are admitted as evidence.

### Correction 6: Saved-Array/CSV Agreement vs Fresh Experiment Replay
- **Clarification:** The verification that saved `.npz` arrays agree with CSV values to machine precision ($< 10^{-16}$) validates archival integrity. It is distinct from a fresh from-scratch simulation replay of the quantum circuit and training pipelines.

### Correction 7: Protocol Timing Remains Unestablished
- **Clarification:** While `docs/stage3/ood_protocol.md` contains a formal frozen protocol header, it was committed atomically with results in Git commit `292d689`. Prospective pre-registration prior to data generation cannot be established from repository Git history alone. Status: **`Documented protocol; timing not established`**.

### Correction 8: Retrospective Status of Decomposition and Baseline Additions
- **Clarification:** Constant training-set baselines (`Train-Mean`, `Train-Median`), Holm family expansion, and SVR intercept/kernel decompositions were formulated post-hoc during the forensic audit to understand the negative $R^2$ values. They are classified as **`retrospective additions`**.
