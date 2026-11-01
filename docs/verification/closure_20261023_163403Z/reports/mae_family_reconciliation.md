# MAE Comparison Family and Statistical Inference Reconciliation

## 1. Context and Problem Statement

During audit synthesis, multiple discrepancies emerged in how the MAE comparisons were specified, adjusted, and reported:
1. **Original Candidate Specification:** In `docs/stage3/ood_findings.md`, the benchmark tested only `FQ vs PQK-2nn` on OOD $R^2$ and MAE. It included zero constant baseline comparisons.
2. **Audit Metric Expansion:** The auditor recognized that negative $R^2$ across all models warranted evaluating against constant predictors fitted to the training set (`Train-Mean` and `Train-Median`).
3. **Narrative Discrepancies:** In `VERIFICATION_REPORT.md` (Section 3.1):
   - `Train-Median` was completely omitted from the text, despite being present in `stage3_mae_comparisons.csv`.
   - The Wilcoxon $p$-value for `FQ vs PQK-2nn` was reported as $7.08 \times 10^{-4}$ (the $R^2$ test $p$-value) rather than $8.51 \times 10^{-4}$ (the true MAE test $p$-value).
   - Holm adjustment for `FQ vs PQK-2nn` was reported as $1.42 \times 10^{-3}$ ($2 \times 7.08 \times 10^{-4}$), whereas in a 3-comparison family, the largest $p$-value receives a multiplier of 1, yielding $p_{\text{holm}} = 8.51 \times 10^{-4}$.
   - Mean difference for `FQ vs Train-Mean` was cited as $-0.4746$ (based on an incorrect baseline MAE of $0.5348$), whereas the true mean difference is **$-0.5459$** (baseline MAE = $0.6061$).

## 2. Baseline Model Performance Across 20 Seeds

To ensure complete transparency, we first report the un-differenced, absolute OOD MAE for all models and baselines:

| model_or_baseline | mean_ood_mae | std_ood_mae | median_ood_mae | min_ood_mae | max_ood_mae | iqr_ood_mae |
| --- | --- | --- | --- | --- | --- | --- |
| FQ (Fidelity Quantum Kernel) | 0.060181 | 0.038100 | 0.050817 | 0.026945 | 0.186101 | 0.035038 |
| PQK-2nn (Projected Quantum Kernel 2-local) | 0.185030 | 0.131658 | 0.173700 | 0.032773 | 0.502865 | 0.142365 |
| Train-Mean Constant Baseline | 0.606095 | 0.025523 | 0.601508 | 0.562067 | 0.672046 | 0.030176 |
| Train-Median Constant Baseline | 0.612131 | 0.035959 | 0.606392 | 0.564887 | 0.690508 | 0.050208 |

## 3. Authoritative Rechecked 3-Comparison Family

All 20 random seeds evaluate matched pairs on identical training/testing splits ($N=20$). Negative paired differences favor FQ:

| comparison_id | pair_count | mean_paired_diff | median_paired_diff | se_diff | ci_95_bootstrap_pointwise | wilcoxon_stat | raw_pval | zero_tie_handling | inference_library | holm_pval_3_comp_family |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FQ vs PQK-2nn | 20 | -0.124849 | -0.120608 | 0.033425 | [-0.191997, -0.062419] | 21.0 | 8.50677490e-04 | Wilcoxon method 'wilcox' (exact distribution for N=20) | scipy 1.18.1 | 8.50677490e-04 |
| FQ vs Train-Mean Baseline | 20 | -0.545914 | -0.552580 | 0.007495 | [-0.559466, -0.531140] | 0.0 | 1.90734863e-06 | Wilcoxon method 'wilcox' (exact distribution for N=20) | scipy 1.18.1 | 5.72204590e-06 |
| FQ vs Train-Median Baseline | 20 | -0.551950 | -0.553779 | 0.008570 | [-0.568018, -0.535501] | 0.0 | 1.90734863e-06 | Wilcoxon method 'wilcox' (exact distribution for N=20) | scipy 1.18.1 | 5.72204590e-06 |

## 4. Reconciliation of Family Scopes

| family_scope | comparisons_included | raw_p_fq_vs_pqk | holm_p_fq_vs_pqk | raw_p_train_mean | holm_p_train_mean | raw_p_train_median | holm_p_train_median | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Original Stage 3 Candidate (docs/stage3/ood_findings.md) | 1: FQ vs PQK-2nn (tested on R^2 and reported MAE) | 7.0763e-04 (R^2) / 8.5068e-04 (MAE) | 7.0763e-04 (no multiple testing) | Not performed in candidate | N/A | Not performed in candidate | N/A | Candidate report did not include constant baselines |
| Audit Synthesis Narrative (VERIFICATION_REPORT.md Sec 3.1) | 2: FQ vs PQK-2nn, FQ vs Train-Mean (Train-Median omitted) | 7.08e-04 (conflated with R^2) | 1.42e-03 (manual Bonferroni x2) | 1.91e-06 | 5.72e-06 (multiplier 3 applied but 3rd test omitted from prose) | Omitted in narrative text | Omitted | Narrative text had transcription discrepancies and omitted Train-Median |
| Audit Reconciled 3-Comparison Family (closure authoritative) | 3: FQ vs PQK-2nn, FQ vs Train-Mean, FQ vs Train-Median | 8.5068e-04 | 8.5068e-04 (multiplier 1) | 1.9073e-06 | 5.7220e-06 (multiplier 3) | 1.9073e-06 | 5.7220e-06 (monotonicity enforced) | Exact pairwise Wilcoxon on N=20 seeds, rigorous Holm adjustment |

## 5. Methodological Notes and Scoping

- **Pointwise Bootstrap Intervals:** The 95% bootstrap confidence intervals are pointwise percentiles derived from 10,000 resamples of the paired difference vector. They describe uncertainty in the mean paired difference, whereas the Wilcoxon signed-rank test evaluates the distribution of symmetric ranks.
- **Independent Datasets vs Resamples:** The 20 seeds represent independently generated random instances of disordered TFIM transverse couplings and independent target states. They are not bootstrap subsamples of a single dataset.
- **Zero/Tie Handling:** There were zero tied pairs and zero zero-differences across all 20 seeds in all three comparisons. Scipy executed the exact permutation distribution for $N=20$.
