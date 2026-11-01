# Stage 2A Change Log

**Execution Timestamp (UTC):** `20261101_090455Z`  
**Output Directory:** `docs/finalization/20261101_082313Z/stage2a_20261101_090455Z/`  
**Stage 2A Diff:** [`02A_PATCH.diff`](file:///d:/quantum-kernel-tfim-benchmarks/docs/finalization/20261101_082313Z/stage2a_20261101_090455Z/02A_PATCH.diff)  
**Cumulative Diff:** [`02_CUMULATIVE_PATCH.diff`](file:///d:/quantum-kernel-tfim-benchmarks/docs/finalization/20261101_082313Z/stage2a_20261101_090455Z/02_CUMULATIVE_PATCH.diff)  

---

## 1. Targeted Manuscript Corrections Applied

### A. Math Delimiter Repair
- **File:** `paper/main.tex:86`
- **Fix:** Repaired missing closing math delimiter in `$\rho_i = \frac{1}{2}(I + \langle X_i \rangle X_i)$` to eliminate LaTeX runaway math syntax error.

### B. Table IV FQ Label & Measurement Accounting
- **File:** `paper/tables/tab_equal_budget.tex` and `paper/main.tex:185`
- **Fix:** Replaced remaining `FQ (train_only)` in Table IV header with a wrapped `\shortstack{\textbf{FQ} \\ \scriptsize (training-Gram PSD clipping)}`. In table notes and main text, clarified that measurement acquisition accounts for all 8,780 deployed pairs (780 training + 8,000 query pairs), eigenvalue thresholding is applied to the training Gram matrix, and cross-blocks remain unclipped.

### C. OOD Physical Scope Qualification
- **File:** `paper/main.tex:189, 191` and `paper/tables/tab_ood.tex`
- **Fix:** Removed unsupported phrases 'across the phase boundary', 'exclusively paramagnetic', and 'ferromagnetic'. Consistently described the setting as a transverse-field distribution shift from a higher-field regime ($h_i \in [0.8, 1.5]$) to a lower-field regime ($h_i \in [0.2, 0.7]$) with coupling $J=1.0$. Removed speculative causal claims attributing model differences to entanglement changes.

### D. Constant-Control Objective Wording
- **File:** `paper/main.tex:195`
- **Fix:** Removed 'To confirm ... genuine inductive physical signal', 'confirms that active kernel features reduce...', and 'zero-parameter training-mean'. Adopted exact terminology: 'training-mean constant predictor' and 'post-fit intercept-only ablation', stating improvement over these simple controls without asserting a unique physical mechanism.

### E. Representation Paragraph Refinement
- **File:** `paper/main.tex:86, 98`
- **Fix:** Removed the unverified number `0.5614`. Changed 'non-vanishing' to 'potentially nonzero' in both Section II-B paragraphs. Unified open-chain interior vs endpoint multiplicity descriptions to eliminate indexing discrepancy. Preserved the exact squared-distance identity $D^2_{\mathrm{RDM}} = 0.25 \|f_{E_2}(\psi) - f_{E_2}(\phi)\|_2^2$ and the verified reference residuals.

### F & G. Uncertainty Labels & Negative OOD R^2 Clarification
- **File:** `paper/main.tex:193` and `paper/tables/tab_ood.tex`
- **Fix:** Removed the assertion that negative $R^2$ is uninformative. Clarified that $R^2$ is retained in Table V for completeness while MAE serves as the primary evaluation metric. Explicitly documented that '$\pm$' values represent sample standard error ($\mathrm{SE} = s/\sqrt{20}$), distinct from bootstrap confidence intervals.

### H. Abstract Precision
- **File:** `paper/main.tex:33-38`
- **Fix:** Replaced 'requiring eigenvalue clipping' with a descriptive statement that both raw and training-Gram-corrected matrices were evaluated. Bounded the budget claim to the evaluated budget points where fidelity estimation was executed. Removed 'severe phase-shift' wording.

### I. Budget Claim Scope & Exploratory Status
- **File:** `paper/main.tex:185` and `paper/tables/tab_equal_budget.tex`
- **Fix:** Replaced continuous-range and blanket superiority phrasing with 'at the evaluated budget points where fidelity estimation was executed ($B_{\mathrm{tot}} \in [10^5, 10^7]$)'. Removed reference to an unverified preregistration manifest, stating explicitly: 'This evaluation is exploratory; prospective protocol timing was not established from available records.'

### J. Statistical Family & Status Separation
- **File:** `paper/main.tex:147, 193` and `paper/tables/tab_ood.tex`
- **Fix:** For Task 2b (Claim C3), explicitly cited `results/stats.csv` rows 112--114. Clarified that while labeled confirmatory in analysis records, prospective protocol timing was not independently certified, preserving a bounded finite-sample interpretation. Kept retrospective OOD families distinct without cross-family adjusted p-value transfer.

### K. Bibliography Diff Reconciliation
- **File:** `paper/references.bib`
- **Reconciliation:**
  - Pre-Stage-2 workspace had duplicate `@article{Shaydulin2022importance, ...}` (lines 59-70) and `@article{Canatar2023bandwidth, ...}` (lines 72-82).
  - Stage 2 removed `Shaydulin2022importance`, yielding a net -11 lines (-302 bytes) against pre-Stage-2 snapshot.
  - Baseline Git HEAD (`292d689d`) ended at line 57 without either entry. Thus, `git diff HEAD paper/references.bib` displays +11 lines (+395 bytes) corresponding solely to the addition of `Canatar2023bandwidth`.
  - Reconciled: No file corruption; the apparent discrepancy is entirely due to `Canatar2023bandwidth` being added to the working copy prior to Stage 2 snapshot creation while `Shaydulin2022importance` was removed during Stage 2.

---

## 2. Unresolved Evidence & Checks Deferred to Stage 3

- **Checks Deferred to Stage 3:**
  1. Visual verification that the Table IV header wrapping and `\tabcolsep = 3.0pt` eliminate the Overfull `\hbox` without aesthetic degradation in compiled PDF output.
  2. Full LaTeX document compilation (`pdflatex`, `bibtex`, `latexmk`) to verify zero undefined citations and clean font/math rendering.
