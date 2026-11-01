# Stage 5 & 6 Full Compilation & Build Audit Report

**Timestamp:** 20261024_002208Z
**Workspace:** D:\quantum-kernel-tfim-benchmarks
**Compiler Suite:** MiKTeX 25.12 (pdflatex Version 3.141592653-2.6-1.40.28, ibtex Version 0.99e)
**Output PDF:** main_compiled.pdf (397,973 bytes, 6 pages)

---

## 1. Build Pipeline & Exit Statuses

| Stage | Command | Working Directory | Exit Code | Status |
|---|---|---|---|---|
| Pass 1 | pdflatex -interaction=nonstopmode -output-directory=... main.tex | paper/ | 0 | PASSED |
| Pass 2 | ibtex main | docs/stage5/integration_20261024_002208Z/build/ | 0 | PASSED |
| Pass 3 | pdflatex -interaction=nonstopmode -output-directory=... main.tex | paper/ | 0 | PASSED |
| Pass 4 | pdflatex -interaction=nonstopmode -output-directory=... main.tex | paper/ | 0 | PASSED |

---

## 2. Compilation Log Diagnostics

- **Errors Encountered:** 0
- **Warnings Encountered:** 0
- **Undefined References:** 0
- **Undefined Citations:** 0
- **Overfull / Underfull Fatalities:** 0

All citations (havlicek2019, schuld2019, huang2021, 	hanasilp2024, shaydulin2022, Canatar2023bandwidth) resolved cleanly from paper/references.bib via IEEEtran.bst.
All labels and cross-references (	ab:equal_budget, 	ab:ood, 	ab:confirmatory_stats, 	ab:t1_r2, 	ab4_grid_boundaries, ig:shots, ig:depol, ig:t1_lc, eq:tfim) resolved cleanly.

---

## 3. Integrated Manuscript Modifications

1. **Abstract:** Updated to qualify Task 1 half-chain entropy regression ({\mathrm{tr}}=160$, $-0.0012$ to $+0.0032$ mean ^2$), state variable ordering across tasks, note exploratory status of equal-budget and OOD benchmarks, and emphasize zero claims of quantum advantage.
2. **Section I (Contributions):** Replaced universal $\le 0.011$ bound with task-scoped Task 1 formulation.
3. **Section II-B (Representations):** Added exact Frobenius identity and algebraic equivalence for PQK-2nn, proving identity to RBF on nearest-neighbor Paulis ($|D^2_{\mathrm{RDM}} - D^2_{\mathrm{Pauli}}| \le 1.33 \times 10^{-15}$), and cited Canatar et al. (2023) regarding grid normalizer artifacts.
4. **Section III-A (Claim C2):** Qualified Task 1 =160$ scope ($-0.0012$ vs $+0.0032$).
5. **Section III-E (Equal-Total-Budget Measurement Scaling):** Integrated Table~\ref{tab:equal_budget} with  \in [10^4, 10^7]$ scaling narrative, low-budget exclusion policy ( < 10$), and exploratory classification.
6. **Section III-F (Controlled Out-of-Distribution Phase-Shift Generalization):** Integrated Table~\ref{tab:ood} with negative ^2$ context, MAE evaluation (.0602 \pm 0.0085$ vs .1850 \pm 0.0294$), paired Wilcoxon test (=21.0, p=8.51\times 10^{-4}$), baseline ablation ($-0.4014$ MAE), and noiseless statevector constraint.
7. **Sections IV & V (Limitations & Non-Claims):** Explicitly added negative scope items and exploratory classification.
