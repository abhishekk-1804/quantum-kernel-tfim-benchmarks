# Pre-Declared Statistical Analysis Plan

This document establishes the pre-registered statistical analysis protocol for Phase 3 benchmark comparisons across quantum and classical kernel methods on the transverse-field Ising model (TFIM).

## 1. Multiple Testing Correction Tiers

- **PRIMARY Tier (`p_holm_perN`):**
  Holm-Bonferroni correction applied across the non-identical model pairs within each individual `(task, target, lattice, N_train, metric)` evaluation cell.
- **SENSITIVITY Tier (`p_holm_family`):**
  Holm-Bonferroni correction applied across all non-identical comparisons across all sample sizes $N_{\text{train}}$ within each `(task, target, lattice, metric)` family.

## 2. Confirmatory vs. Exploratory Designation

### Confirmatory Comparisons
The following three model pairs are declared *a priori* as confirmatory:
1. `PQK-1` vs. `PQK-2nn`
2. `PQK-2nn` vs. `E (raw)`
3. `FQ` vs. `E (raw)`

Evaluated strictly at the following benchmark cells:
- **Task 1 (Half-chain Entanglement Entropy):** $N_{\text{train}} \in \{40, 160\}$
- **Task 2b (4-Point Correlator $\langle Z_0 Z_1 Z_{n-2} Z_{n-1} \rangle$):** $N_{\text{train}} \in \{40, 160\}$
- **Task 4b (Frustrated Ground-State Energy):** Lattices $2 \times 4$ and $3 \times 4$, $N_{\text{train}} \in \{40, 80\}$
- **Task 4a (Phase Classification / Order Parameter):** Lattices $2 \times 4$ and $3 \times 4$, $N_{\text{train}} \in \{40, 80\}$

### Exploratory Comparisons
All other evaluations are designated exploratory:
- Every other model pair:
  - `PQK-2nn` vs. `FQ`
  - `PQK-1` vs. `E (raw)`
  - `E (raw)` vs. `E2 (raw)`
  - `E (raw)` vs. `F (std)`
  - `E (raw)` vs. `E (std)`
- Every other sample size $N_{\text{train}}$ (e.g., $N_{\text{train}} \in \{10, 20\}$ where finite-sample inner-CV overfitting is documented, and $N_{\text{train}} = 80$ for T1/T2).
- All Task 2a rows ($\langle Z_0 Z_{n-1} \rangle$ is a "contained" 2-body control observable where linear/Ridge models succeed by construction).
- All Task 5 noise evaluations (measurement shot budgets and depolarizing sweeps).

## 3. Mathematical & Direction Conventions

- **Pair Difference:**
  $$d_i = \text{metric}_i(\text{model}_a) - \text{metric}_i(\text{model}_b)$$
  A positive difference ($d_i > 0$) strictly indicates that $\text{model}_a$ achieved a higher test score than $\text{model}_b$ on seed $i$.
- **Primary Metrics:**
  - Regression (T1, T2, T4b, T5): Test $R^2$.
  - Classification (T4a): Test Accuracy.
- **Statistical Significance & Rank-Biserial Correlation:**
  - Two-sided Wilcoxon signed-rank test (`zero_method="wilcox"`, `alternative="two-sided"`).
  - Explicit rank computation: $W_+$ (sum of positive ranks), $W_-$ (sum of negative ranks).
  - Rank-biserial effect size: $r = \frac{W_+ - W_-}{W_+ + W_-}$.
- **Bootstrap Confidence Intervals:**
  - 10,000 empirical bootstrap resamples over seeds using the percentile method with fixed RNG seed `20261022`.
- **Effect Thresholds & Flags:**
  - If $|\text{mean}(d)| < 0.002$ and the 95% bootstrap CI excludes $0$: flag `"significant_but_tiny"`.
  - If all $d_i = 0$ (or fewer than 1 non-zero pair): $p_{\text{raw}} = \text{NaN}$, $\text{effect\_size} = 0.0$, flag = `"identical"`, and the comparison is excluded from Holm-Bonferroni correction families.
