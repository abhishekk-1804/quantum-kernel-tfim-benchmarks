# Ground-Truth Stage 3 Paired-MAE Reconciliation Report

**Execution Timestamp (UTC):** `2026-10-23T17:18:05.068663+00:00`  
**Execution Directory:** `docs/verification/paired_mae_check_20261023_171155Z`  
**Primary Evidence Source:** `results/stage3/t6_ood_shift.csv`  
**Prediction Array Source:** `docs/verification/audit_20261023_155335Z/predictions`  

> **EVIDENTIARY STATUS:** Retrospective forensic verification. This report does NOT certify confirmatory status, global quantum advantage, publication readiness, or independent human review.

---

## Section A: Evidence Inspected

1. **Primary Benchmark CSV:** `results/stage3/t6_ood_shift.csv` (100 rows, 5 models, 20 seeds). SHA-256: `81908f5a14f0c7c262b1647964b02fbd7570ba737a2dd4f3420659be8da139cb`
2. **Saved Prediction NPZ Archives:** 20 seed files (`seed_00_arrays.npz` to `seed_19_arrays.npz`) in `docs/verification/audit_20261023_155335Z/predictions`.
3. **Historical Analysis & Audit Reports:**
   - `scripts/stage3_analysis.py` (original candidate analysis script)
   - `docs/stage3/ood_findings.md` (original candidate summary)
   - `scripts/audit_stage3_metrics.py` (audit metrics script)
   - `docs/verification/audit_20261023_155335Z/stage3_mae_comparisons.csv`
   - `docs/verification/audit_20261023_155335Z/VERIFICATION_REPORT.md`
   - `docs/verification/closure_20261023_163403Z/tables/mae_family_original_rechecked.csv`
   - `docs/verification/closure_20261023_163403Z/reports/mae_family_reconciliation.md`

## Section B: Actual Model/Variant and Metric Mapping

- **Selection Predicates:** `model in ['FQ', 'PQK-2nn']` and `variant == 'none'`.
- **Target Metric:** `ood_mae` (Mean Absolute Error on the out-of-distribution ferromagnetic test split $h_i \in [0.2, 0.7]$).
- **Ground Truth Physical Target:** Half-chain bipartite entanglement entropy $S_{n/2}(\psi)$ ($n=8$ disordered TFIM, open boundary conditions).
- **Pairing Integrity:** Exactly 1 row per model per seed across all 20 seeds ($s \in \{0, \dots, 19\}$). 100% matched, zero missing rows, zero duplicates.

## Section C: Recovered Pair Count and Descriptive Results

- **Total Seeds / Pairs:** $N = 20$
- **Mean FQ OOD MAE:** `0.060181` (rounds to `0.0602`)
- **Mean PQK-2nn OOD MAE:** `0.185030` (rounds to `0.1850`)
- **Mean Paired Difference (d = MAE_FQ - MAE_PQK2):** `-0.124849` (rounds to `-0.1248`)
- **Median Paired Difference:** `-0.120608`
- **Range of Paired Differences:** `[-0.444919, 0.153329]`
- **Sign Breakdown:** Negative: **16** (FQ superior), Positive: **4** (PQK-2nn superior: Seeds 8, 9, 11, 16), Zero: **0**.
- **Absolute Tie Structure:** Exactly **0** ties across all 20 seeds. All $|d_s|$ values are distinct.
- **Signed Rank Sums:** Positive rank sum $W^+ = 21.0$, Negative rank sum $W^- = 189.0$ (Total = $210.0 = 20 \times 21 / 2$).
- **Numerical Identity Check:** $\operatorname{mean}(d) - [\operatorname{mean}(\text{FQ}) - \operatorname{mean}(\text{PQK2})] = 0.00e+00$ (exact).

### Complete Recovered 20-Seed Paired Vector:

| Seed | FQ OOD MAE | PQK-2nn OOD MAE | Difference ($d$) | Absolute Diff ($|d|$) | Rank | Sign |
|---|---|---|---|---|---|---|
| 00 | 0.030009 | 0.199973 | -0.169964 | 0.169964 | 16.0 | - |
| 01 | 0.026945 | 0.191343 | -0.164399 | 0.164399 | 14.0 | - |
| 02 | 0.065406 | 0.234294 | -0.168889 | 0.168889 | 15.0 | - |
| 03 | 0.036628 | 0.165139 | -0.128512 | 0.128512 | 10.0 | - |
| 04 | 0.027052 | 0.127993 | -0.100941 | 0.100941 | 8.0 | - |
| 05 | 0.036018 | 0.178722 | -0.142704 | 0.142704 | 11.0 | - |
| 06 | 0.068300 | 0.223191 | -0.154891 | 0.154891 | 13.0 | - |
| 07 | 0.033019 | 0.043413 | -0.010394 | 0.010394 | 1.0 | - |
| 08 | 0.070931 | 0.054557 | +0.016374 | 0.016374 | 2.0 | + |
| 09 | 0.091870 | 0.034900 | +0.056971 | 0.056971 | 4.0 | + |
| 10 | 0.034062 | 0.092629 | -0.058567 | 0.058567 | 5.0 | - |
| 11 | 0.099897 | 0.056520 | +0.043378 | 0.043378 | 3.0 | + |
| 12 | 0.100929 | 0.168677 | -0.067748 | 0.067748 | 6.0 | - |
| 13 | 0.033715 | 0.259862 | -0.226148 | 0.226148 | 17.0 | - |
| 14 | 0.034779 | 0.465294 | -0.430515 | 0.430515 | 19.0 | - |
| 15 | 0.068375 | 0.181079 | -0.112704 | 0.112704 | 9.0 | - |
| 16 | 0.186101 | 0.032773 | +0.153329 | 0.153329 | 12.0 | + |
| 17 | 0.052976 | 0.140436 | -0.087460 | 0.087460 | 7.0 | - |
| 18 | 0.057946 | 0.502865 | -0.444919 | 0.444919 | 20.0 | - |
| 19 | 0.048658 | 0.346940 | -0.298282 | 0.298282 | 18.0 | - |

## Section D: Original CSV versus Saved-Array Agreement

For all 20 seeds, the out-of-distribution true target array `y_ood` (shape `(100,)`) and model predictions `fq_pred_ood` (shape `(100,)`) and `pqk2_pred_ood` (shape `(100,)`) were extracted from `predictions/seed_XX_arrays.npz` using `allow_pickle=False`.
- **Maximum Absolute Discrepancy (FQ):** `0.00e+00`
- **Maximum Absolute Discrepancy (PQK-2nn):** `0.00e+00`
- **Tolerance Evaluation:** Both maximum discrepancies are $< 10^{-16}$, passing the strict tolerance `atol=1e-7, rtol=0` at floating-point machine precision.
- **Conclusion:** The CSV values in `results/stage3/t6_ood_shift.csv` and the serialized prediction arrays in `audit_20261023_155335Z/predictions/` are identical bit-for-bit.

## Section E: Wilcoxon Call, Version, Warnings, Statistic, and P-Value

- **SciPy Version:** `1.18.1`
- **Exact Call Tested:** `scipy.stats.wilcoxon(diffs_arr, alternative='two-sided')`
- **Resulting Test Statistic:** **$W = 21.0$** (equal to $\min(W^+, W^-) = \min(21.0, 189.0)$)
- **Resulting P-Value:** **$p = 8.50677490e-04$** (formatted: **`8.51e-4`**)
- **Runtime Warnings:** None encountered.
- **Methodology:** Because $N=20 \le 50$ and there are zero ties and zero zero-differences, SciPy's default `method='auto'` executes the exact permutation distribution.

## Section F: Sensitivity Analyses

1. **Explicit Exact Method (`method='exact'`):** $W = 21.0, p = 8.50677490e-04$ (Identical to default call).
2. **Asymptotic Approximation (`method='approx'`):** $W = 21.0, p = 1.71301764e-03$ ($p \approx 1.71 \times 10^-3$ without continuity correction).

## Section G: Historical Claim Reconciliation

| Historical Claim | Claimed Value | Observed Location | Identified Metric Origin | Reconciled Value | Classification |
|---|---|---|---|---|---|
| Mean FQ OOD MAE | 0.0602 | `docs/stage3/ood_findings.md line 211; stage3_...` | OOD MAE of FQ in results/stage3/t6_ood_shift.... | `0.060181` | **Reproduces from original paired MAE vector** |
| Mean PQK-2nn OOD MAE | 0.1850 | `docs/stage3/ood_findings.md line 211; stage3_...` | OOD MAE of PQK-2nn in results/stage3/t6_ood_s... | `0.185030` | **Reproduces from original paired MAE vector** |
| Mean paired difference (FQ - PQK-2nn) | -0.1248 | `stage3_mae_comparisons.csv; VERIFICATION_REPO...` | Difference of OOD MAE in results/stage3/t6_oo... | `-0.124849` | **Reproduces from original paired MAE vector** |
| Wilcoxon statistic = 1.0 | 1.0 | `Historical prompt query / narrative draft not...` | In-Distribution (ID) MAE difference: stats.wi... | `OOD MAE W=21.0; ID MAE W=1.0` | **Reproduces from another identified metric/comparison** |
| Raw p-value = 8.51e-4 | 8.51e-4 (0.000851) | `docs/verification/audit_20261023_155335Z/stag...` | Two-sided Wilcoxon signed-rank test on OOD MA... | `8.50677490e-04` | **Reproduces from original paired MAE vector** |
| Earlier raw p-value = 7.08e-4 | 7.08e-4 (7.0763e-04) | `docs/stage3/ood_findings.md line 34; VERIFICA...` | Two-sided Wilcoxon signed-rank test on OOD R^... | `OOD R^2 p=7.07626343e-04` | **Reproduces from another identified metric/comparison** |

### Detailed Historical Findings:
1. **Mean MAE & Paired Difference:** The values `0.0602`, `0.1850`, and `-0.1248` faithfully reproduce the across-seed sample means of `ood_mae` in `t6_ood_shift.csv` after standard 4-decimal rounding.
2. **Raw P-Value `8.51e-4`:** Faithfully reproduces the two-sided Wilcoxon signed-rank test on the 20-seed paired OOD MAE vector ($W=21.0, p = 8.5068 \times 10^{-4}$).
3. **Earlier Raw P-Value `7.08e-4`:** Does NOT belong to MAE. It is the exact Wilcoxon p-value of the **OOD $R^2$** comparison ($W=20.0, p = 7.0763 \times 10^{-4}$), which was originally computed in `scripts/stage3_analysis.py` (line 139) and reported in `docs/stage3/ood_findings.md` (lines 34, 211). Earlier narrative synthesis texts inadvertently cited the $R^2$ test $p$-value alongside the MAE means.
4. **Wilcoxon Statistic `1.0`:** Does NOT belong to OOD MAE (which has $W=21.0$). It belongs to **In-Distribution (ID) MAE** (`id_mae`), where FQ is lower in 19 seeds and higher in 1 seed of rank 1 ($W=1.0, p = 3.81 \times 10^{-6}$).

## Section H: Input and Provenance Limitations

- **Timing of Specification:** The primary data file `results/stage3/t6_ood_shift.csv` and protocol `docs/stage3/ood_protocol.md` were committed atomically in commit `292d689`. Pre-execution registration is not provable from Git history alone.
- **Independent Datasets vs Resamples:** The 20 pairs represent independent disorder realizations of the TFIM chain. They are not bootstrap resamples.

## Section I: Determination on Further Computation

- **No further computation is necessary.** The mathematical, tabular, and serialized array representations of the Stage 3 paired MAE vector are in 100% mutual agreement ($< 10^{-16}$ discrepancy). All historical statistics have been definitively mapped to their exact computational origins.

## Section J: Statements Excluded from Manuscript Prose

1. Do NOT state that 'FQ achieves lower MAE in every seed' (FQ is lower in 16 seeds, but higher in 4 seeds: Seeds 8, 9, 11, 16).
2. Do NOT report $W = 1.0$ for out-of-distribution MAE (the statistic is $W = 21.0$).
3. Do NOT cite $p = 7.08 \times 10^{-4}$ as the MAE Wilcoxon test p-value (it is the $R^2$ p-value; the MAE p-value is $8.51 \times 10^{-4}$).
4. Do NOT assert 'support vector manifold' or unrestricted causal claims.
