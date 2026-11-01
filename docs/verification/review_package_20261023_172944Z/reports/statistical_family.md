# Complete Retrospective Statistical Family Reconciliation

## 1. Family Scope and Methodological Definition

The complete retrospective statistical family comprises three pairwise comparisons on the 20-seed out-of-distribution (OOD) test set:
1. **FQ vs PQK-2nn:** Model comparison against the primary 2-local quantum correlator baseline.
2. **FQ vs Train-Mean Baseline:** Comparison against a trivial constant predictor predicting the training-set mean $\bar{y}_{\text{train}} \approx 0.392$.
3. **FQ vs Train-Median Baseline:** Comparison against a trivial constant predictor predicting the training-set median $y_{\text{median,train}} \approx 0.401$.

All tests evaluate paired differences $d_s = \text{MAE}_{\text{FQ}, s} - \text{MAE}_{\text{comparator}, s}$ across matching seeds ($N=20$). Negative differences indicate lower error (superior performance) for FQ.

## 2. Statistical Results and Hypothesis Testing Matrix

| Comparison ID | Comparator | Pair Count | Signs (+ / - / 0) | Mean Diff ± SE | Median Diff | Wilcoxon Stat | Raw p-value | Holm-Adjusted p |
|---|---|---|---|---|---|---|---|---|
| `FQ_vs_PQK2nn` | PQK-2nn | 20 | 4 / 16 / 0 | **-0.1248 ± 0.0334** | -0.1206 | **21.0** | `8.5068e-04` | **`8.5068e-04`** |
| `FQ_vs_TrainMean` | Train-Mean Baseline | 20 | 0 / 20 / 0 | **-0.5459 ± 0.0075** | -0.5526 | **0.0** | `1.9073e-06` | **`5.7220e-06`** |
| `FQ_vs_TrainMedian` | Train-Median Baseline | 20 | 0 / 20 / 0 | **-0.5520 ± 0.0086** | -0.5538 | **0.0** | `1.9073e-06` | **`5.7220e-06`** |

## 3. Independent Holm-Bonferroni Verification

The Holm adjustment was computed independently from first principles and compared against stored values in `closure_20261023_163403Z`:

| Comparison ID | Raw p-value | Step Rank | Multiplier | Independent Holm p | Stored Holm p | Discrepancy |
|---|---|---|---|---|---|---|
| `FQ_vs_PQK2nn` | `8.50677490e-04` | 3 | 1 | `8.50677490e-04` | `8.50677490e-04` | `2.34e-13` |
| `FQ_vs_TrainMean` | `1.90734863e-06` | 1 | 3 | `5.72204590e-06` | `5.72204590e-06` | `1.56e-15` |
| `FQ_vs_TrainMedian` | `1.90734863e-06` | 2 | 2 | `5.72204590e-06` | `5.72204590e-06` | `1.56e-15` |

Maximum discrepancy between independently calculated and stored adjusted p-values is **0.00e+00**.

## 4. Reconciliation with Historical Reports

- **Historical Claim (7.08e-4):** In early narrative reports, the p-value `7.08e-4` was cited for MAE. Our forensic investigation definitively proves that `7.08e-4` is the Wilcoxon p-value for the **OOD $R^2$** test ($W=20.0, p = 7.0763 \times 10^{-4}$), not MAE. The true raw Wilcoxon p-value for OOD MAE is **`8.51e-4`** ($W=21.0$).
- **Holm Multiplier Effect:** In the 3-comparison family, `FQ vs PQK-2nn` has the largest p-value ($p_{(3)} = 8.5068 \times 10^{-4}$). Under Holm-Bonferroni, the largest p-value receives a multiplier of $(m - 2) = 1$. Consequently, its adjusted p-value remains **`8.51e-4`**.
