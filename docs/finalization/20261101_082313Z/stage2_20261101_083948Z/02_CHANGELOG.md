# Stage 2 Change Log

**Execution Timestamp (UTC):** `20261101_083948Z`  
**Target Output Directory:** `docs/finalization/20261101_082313Z/stage2_20261101_083948Z/`  
**Patch Diff:** [`02_PATCH.diff`](file:///d:/quantum-kernel-tfim-benchmarks/docs/finalization/20261101_082313Z/stage2_20261101_083948Z/02_PATCH.diff)  
**Patch Status Matrix:** [`02_PATCH_STATUS.csv`](file:///d:/quantum-kernel-tfim-benchmarks/docs/finalization/20261101_082313Z/stage2_20261101_083948Z/02_PATCH_STATUS.csv)  

---

## Applied Corrections Summary

### Patch P01: Abstract Scope & Quantitative Differences
- **File:** `paper/main.tex:33-44`
- **What Changed:** Replaced blanket parity assertions with exact descriptive Task 1 differences (-0.0012 for FQ minus E(raw) and +0.0032 for FQ minus PQK-2nn), stated that model ordering varies across tasks and training sizes, and replaced general equivalence wording with experimental constraint wording.
- **Evidence Source:** `results/stats.csv:34,36`; `results/t1_entropy_gridv3.csv`. Descriptive & confirmatory where tested.

### Patch P02: TFIM Symmetry Derivation
- **File:** `paper/main.tex:90-92`
- **What Changed:** Conditioned reduction on states being both real in the computational Z-basis and parity-definite under global spin-flip parity P = prod_k X_k. Classified 15 two-qubit operators into 8 eliminated by parity (Y_i, Z_i, Y_j, Z_j, X_iY_j, X_iZ_j, Y_iX_j, Z_iX_j), 2 eliminated additionally by reality (Y_iZ_j, Z_iY_j), leaving only 5 non-zero expectations (X_i, X_j, X_iX_j, Y_iY_j, Z_iZ_j). Explicitly clarified K is basis-dependent complex conjugation, not physical spin time reversal.
- **Evidence Source:** Analytical Pauli matrix algebra; `docs/stage5/audit_20261101/REPORT.md` Section 7 & Item IT-16.

### Patch P03: Representation Identity & Interior Multiplicities
- **File:** `paper/main.tex:103`
- **What Changed:** Defined edge-stacked feature map f_E2(psi) in R^35 on 1D open chain (n=8, 7 edges). Stated exact raw squared distance identity D^2_RDM = 0.25 ||f_E2(psi) - f_E2(phi)||_2^2. Explained that repeating interior magnetizations algebraically provides sqrt(deg_i) = sqrt(2) weighting to match Frobenius edge summation. Kept bandwidth normalization (1/32) distinct from coordinate weights. Attached exact verified residuals (5.55e-17 on 10 pairs; 1.33e-15 on 45 pairs).
- **Evidence Source:** `src/kernels.py:310-336`; `docs/stage5/audit_20261101/representation_distance_check.json`.

### Patch P04 & P05: Task 2b & Claim C3 Interpretation
- **File:** `paper/main.tex:149, 155`
- **What Changed:** Clarified Task 2b is the non-contained four-point correlator <Z_0 Z_1 Z_{n-2} Z_{n-1}>. Replaced 'statistically indistinguishable' with approved wording: 'observed differences among the compared models were small, and the reported paired tests did not detect statistically significant differences for these comparisons. This finite-sample result does not establish practical equivalence or identical asymptotic accuracy.' Qualified Claim C3 to state that paired tests did not detect statistically significant differences at N_tr=160, without establishing asymptotic equivalence.
- **Evidence Source:** `results/stats.csv:112-119`; `REPORT.md` Item IT-17, IT-18.

### Patch P06: Figure 2 Caption Styling & Cost Axes
- **File:** `paper/main.tex:164-167`
- **What Changed:** Corrected inverted line style descriptions to match `scripts/make_figures.py:make_f5()`: FQ-raw is dashed with marker x, eigenvalue-clipped FQ is solid with marker blacktriangle. Specified 95% bootstrap CIs and deployed (8,780 * S) vs full-Gram (28,680 * S) total-shot axes.
- **Evidence Source:** `scripts/make_figures.py:472-544`; `figures/data/fig_shots.csv`.

### Patch P07: Finite-Shot Data & PSD Scope
- **File:** `paper/main.tex:172`
- **What Changed:** Replaced narrative errors with verified empirical metrics from `results/t5_noise.csv`: raw FQ achieves 0.7634 (S=100), 0.8894 (S=1000), 0.8613 (S=10000); clipped FQ achieves 0.8101 (S=100), 0.8693 (S=1000), 0.9630 (S=10000). Stated that training-Gram clipping varies across budgets, raw performance is nonmonotonic, and test-train cross-blocks are unclipped.
- **Evidence Source:** `results/t5_noise.csv`; `figures/data/fig_shots.csv`; `final_reconciliation.csv`.

### Patch P08: Deployed Budget Accounting
- **File:** `paper/main.tex:188`
- **What Changed:** Stated general counts before numerical substitution: N_settings = 3(N_tr + N_te), N_pairs = choose(N_tr, 2) + N_tr * N_te. For audited design (40/200), N_settings = 720 and N_pairs = 8780. Harmonized formulas to S_feat = floor(B_tot / 720) and S_swap = floor(B_tot / 8780). Described shared-bitstring extraction for compatible observables. Detailed state preparations at B_tot=10^6 (999,360 feature preparations vs 1,984,280 swap preparations).
- **Evidence Source:** `scripts/stage2_equal_budget.py:112-117`; `paper/tables/tab_equal_budget.tex`.

### Patch P09 & P10: OOD Generalization & Baseline Mislabeling Fix
- **File:** `paper/main.tex:198-200`
- **What Changed:** Clarified retrospective status of Stage 3 three-comparison family. Corrected baseline mislabeling: -0.4014 +- 0.0156 MAE is FQ vs post-fit intercept-only ablation (f(x)=b). True reduction vs training-mean constant predictor is -0.5459 +- 0.0075 MAE. Disclosed omission of full all-pairs E(raw) RBF baseline and finite-shot sampling.
- **Evidence Source:** Saved prediction arrays in `predictions/seed_*_arrays.npz`; `scripts/audit_stage3_metrics.py:680-730, 840-895`.

### Patch P11: Conclusion
- **File:** `paper/main.tex:227`
- **What Changed:** Replaced blanket indistinguishability wording with approved bounded summary stating task-dependent ordering, in-distribution statistical detectability, deployed budget advantages, and OOD extrapolation scope limits.
- **Evidence Source:** Section 12 approved text; `results/stats.csv`.

### Patch P12: Bibliography Deduplication
- **File:** `paper/references.bib:59-70`
- **What Changed:** Removed duplicate entry Shaydulin2022importance. Retained existing shaydulin2022.
- **Evidence Source:** `paper/references.bib:47-70`.

### Patch P13: Table IV Layout Formatting
- **File:** `paper/tables/tab_equal_budget.tex`
- **What Changed:** Reduced tabcolsep from 4.5pt to 3.0pt and streamlined repeated strings in the 9th column (Below minimum-shot threshold and PQK-2nn higher observed R^2) to resolve the 101.68 pt Overfull hbox.
- **Evidence Source:** `main.log:487`; `REPORT.md` Item IT-11.

### Patch P14: Table V Footnote
- **File:** `paper/tables/tab_ood.tex`
- **What Changed:** Updated table footnote to classify comparison family as retrospective.
- **Evidence Source:** `docs/stage3/ood_protocol.md`; Git commit `292d689d`.
