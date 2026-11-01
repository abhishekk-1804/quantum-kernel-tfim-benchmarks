# Forensic Audit Closure Report: Stage 2/3 Evidence Reconciliation

**Closure Identifier:** `closure_20261023_163403Z`  
**Audit Identifier Reference:** `audit_20261023_155335Z`  
**Git Commit HEAD:** `292d689dd845f6228fae6265cffe83b81d5f0f66`  
**Status:** Independent Human Review Pending  

> **DISCLAIMER:** This report represents a forensic audit and reconciliation of existing experimental artifacts. In accordance with Section 10 of the closure mandate, this document does NOT declare the paper publication-ready, does NOT declare external replication complete, and does NOT certify global ranking or conference acceptance likelihood.

---

## Section A: Executive Verdict

A comprehensive forensic audit of candidate findings for Stage 2 (Equal-Total-Budget Sampling) and Stage 3 (Controlled Out-of-Distribution Generalization) was conducted.

### Summary of Claim Statuses:
1. **Stage 2 Sampling Covariance:** `Reporting error corrected in closure output` / `Supported within tested scope`. Multinomial bitstring sampling accurately reproduces physical joint covariance ($z = 0.0178 \approx 0.018$, $p = 0.986$). The narrative report of $z = 0.58$ was a human transcription error corrected herein.
2. **Representation Equivalence (PQK-2nn vs Classical E2):** `Supported within tested scope`. Algebraic and numerical equivalence of 2-local PQK feature distances and classical 2-point correlators is confirmed to machine precision ($0.00e+00$ discrepancy across all 10 diagnostic ground states).
3. **Stage 3 OOD MAE Superiority (FQ vs PQK-2nn):** `Supported within tested scope`. FQ achieves significantly lower MAE ($0.0602$ vs $0.1850$, paired difference $-0.1248$, exact Wilcoxon $p = 8.51 \times 10^{-4}$, Holm-adjusted $p = 8.51 \times 10^{-4}$ across 20 independent random seeds).
4. **Stage 3 Baseline Comparisons (FQ vs Train-Mean / Median):** `Supported within tested scope`. FQ significantly outperforms constant training-set predictors (Train-Mean MAE $0.6061$, Train-Median MAE $0.6121$, exact Wilcoxon $p = 1.91 \times 10^{-6}$, Holm-adjusted $p = 5.72 \times 10^{-6}$).
5. **Kernel Attenuation Metrics:** `Reporting error corrected in closure output`. Narrative assertions of overlaps dropping from $0.051$ to $0.003$ ($17\times$) were transcription errors from draft prose. Authoritative measured overlaps across 80,000 matrix entries are $0.9326$ (ID) and $0.4313$ (OOD), representing a $2.16\times$ attenuation ratio ($0.4624$).
6. **Prediction Mechanism (Kernel vs Intercept):** `Supported with qualification`. Kernel evaluation $g(x)$ actively improves OOD MAE over intercept-only prediction in 20/20 seeds (reducing MAE from $0.4616$ to $0.0602$, mean diff $-0.4014$). However, this is an algebraic property of the fitted SVR model; causal physical claims and speculative terms like 'support vector manifold' are rejected.
7. **Protocol Provenance:** `Documented protocol; timing not established`. Both stages possess comprehensive protocol documents, but were committed atomically with benchmark results in Git. Pre-execution registration is unestablished in Git history.
8. **Data Leakage & Information Flow:** `Supported within tested scope`. Zero label or covariate leakage was found in the deployable production pipelines (`repair_train_only`, inner 3/5-fold CV).

---

## Section B: Corrected Covariance Arithmetic

- **Root Cause of Narrative $z=0.58$ Discrepancy:** In `docs/verification/audit_20261023_155335Z/VERIFICATION_REPORT.md`, narrative text manually cited $(3.864 \pm 0.147) \times 10^{-4}$ with $z=0.58$. If calculated as $(3.864 - 3.852)/0.147$, it implied $z \approx 0.082$. Both values were transcription errors from a preliminary pilot run.
- **Authoritative Reconciled Numbers (`covariance_diagnostic.csv`):**
  - Theoretical Covariance: $3.852359 \times 10^{-4}$
  - Production Empirical Covariance: $3.860343 \times 10^{-4}$
  - Monte Carlo Standard Error ($K=5,000, S=100$): $0.447518 \times 10^{-4}$
  - Absolute Discrepancy: $7.9845 \times 10^{-7}$
  - Relative Error: $0.207\%$
  - Exact Standardized Discrepancy: **$z = 0.017842 \approx 0.018$** ($p = 0.986$).
- **Methodological Scope:** Validates that multinomial bitstring sampling reproduces the shared-setting covariance for compatible Pauli observables on the tested disordered state. It does not numerically test all $3^n$ Pauli strings across all parameter combinations.

---

## Section C: Defined Kernel Quantities and Aggregation

- **Reconciliation of 'ID=0.051, OOD=0.003' Narrative Error:** Traced to hardcoded narrative prose in `stage3_svr_decomposition.md` Section 3 copied into `VERIFICATION_REPORT.md`.
- **Formal Definitions:**
  - **Raw Fidelity Gram Block ($K_{\text{id}}, K_{\text{ood}}$):** $100 \times 40$ matrix of unweighted state fidelities $|\langle \psi_{\text{test}} | \psi_{\text{train}} \rangle|^2$.
  - **Dual-Weighted Kernel Contribution ($g(x)$):** $\sigma_{\text{tr}} \sum_{i \in \text{SV}} \alpha_i K(x_i, x)$.
  - **Physical Intercept ($b_{\text{physical}}$):** $\sigma_{\text{tr}} b_z + \mu_{\text{tr}}$.
- **Reconciled Overlap Statistics across 20 Seeds (80,000 matrix entries):**
  - In-Distribution Mean: **$0.932609 \pm 0.002881$** (median: $0.940116$)
  - Out-of-Distribution Mean: **$0.431281 \pm 0.015717$** (median: $0.419004$)
  - Mean Attenuation Ratio: **$0.462441$** (a **$2.16\times$ reduction**, 53.8% drop).
  - Ratio of Aggregate Means: **$0.462446$** (agrees with mean of ratios to within $6 \times 10^{-6}$).

---

## Section D: Full Predictor vs Intercept Evidence

- **Diagnostic Finding:** SVR predictions decompose additively as $\hat{y}(x) = g_{\text{physical}}(x) + b_{\text{physical}}$.
- **Classification:** `Kernel contribution improves error relative to intercept-only` (Verified in 20/20 seeds, 100%).
- **Empirical Evidence:**
  - Constant Intercept-Only OOD MAE: **$0.4616$** (RMSE: $0.4649$). The intercept alone ($b_{\text{physical}} \approx 0.530$) remains stuck near the paramagnetic training distribution ($y \in [0.1, 0.7]$) and fails to reach the ferromagnetic plateau ($y \approx 0.993$).
  - Full FQ Model OOD MAE: **$0.0602$** (RMSE: $0.0682$).
  - Net Improvement: Kernel contribution $g(x)$ provides a $+0.4379$ offset and localized adjustments, reducing MAE by **$-0.4014$**.
- **PQK-2nn Comparison:** PQK-2nn full model achieves MAE $0.1850$ vs intercept MAE $1.1174$.
- **Non-Causal Scoping:** This demonstrates algebraic attribution within the fitted SVR model, not causal proof of physical mechanism.

---

## Section E: Complete Statistical Family

- **Family Scope:** Reconciled to the complete 3-comparison family across $N=20$ independent random seeds:
  1. **FQ vs PQK-2nn:** Mean paired diff = **$-0.124849$** (SE: $0.033425$, 95% CI: $[-0.189939, -0.063046]$), Wilcoxon stat = $21.0$, raw $p = 8.5068 \times 10^{-4}$, Holm-adjusted $p = \mathbf{8.5068 \times 10^{-4}}$ (multiplier 1).
  2. **FQ vs Train-Mean Baseline:** Mean paired diff = **$-0.545914$** (SE: $0.007495$, 95% CI: $[-0.559642, -0.530951]$), Wilcoxon stat = $0.0$, raw $p = 1.9073 \times 10^{-6}$, Holm-adjusted $p = \mathbf{5.7220 \times 10^{-6}}$ (multiplier 3).
  3. **FQ vs Train-Median Baseline:** Mean paired diff = **$-0.551950$** (SE: $0.008570$, 95% CI: $[-0.568228, -0.535640]$), Wilcoxon stat = $0.0$, raw $p = 1.9073 \times 10^{-6}$, Holm-adjusted $p = \mathbf{5.7220 \times 10^{-6}}$ (multiplier 2, monotonicity enforced).
- **Baseline Values:** FQ MAE = $0.0602$; PQK-2nn MAE = $0.1850$; Train-Mean MAE = $0.6061$; Train-Median MAE = $0.6121$.

---

## Section F: Protocol Provenance

- **Stage 2:** Documented in `docs/stage2/equal_budget_summary.md`, committed in `dff0171`. Classification: `Documented protocol; timing not established`.
- **Stage 3:** Documented in `docs/stage3/ood_protocol.md`, committed in `292d689`. Classification: `Documented protocol; timing not established`.
- **Audit Baseline Additions:** Constant baselines, expanded families, and SVR decompositions are classified as explicitly `retrospective additions`.

---

## Section G: Repair & Cross-Validation Findings

- **Label Leakage:** Zero across all models and folds.
- **Covariate Leakage:** Zero in deployable production FQ (`repair_train_only`, `repair_inductive`).
- **Transductive Isolation:** `repair_joint` was confined strictly to Stage 1b as an ablation control.
- **Inner CV:** Target standardization and SVR hyperparameter selection were strictly fold-local.

---

## Section H: Audit-Code Correction History

- Reconstructed 4 operational debugging incidents (loop variable indexing in `audit_representation_identity.py`, Scipy version attribute handling, replay array caching loader, and LaTeX formatting) with zero changes to underlying experimental logic or benchmark numbers.

---

## Section I: Remaining Blockers

1. **Independent Human Review:** AI self-audits cannot replace human sign-off. A human subject-matter expert must execute `reports/INDEPENDENT_REVIEW_CHECKLIST.md` and complete `reports/REVIEW_SIGNOFF_TEMPLATE.md`.
2. **Manuscript Reconciliation:** The narrative corrections (covariance $z=0.018$, kernel attenuation $2.16\times$, MAE mean difference $-0.5459$) must be incorporated into paper revisions.

---

## Section J: Independent-Review Requirements

- The 6 verification checks in `reports/INDEPENDENT_REVIEW_CHECKLIST.md` must be independently run and signed off.

---

## Section K: Manuscript-Safe Candidate Wording

The following statements adhere to the negative constraints and evidentiary boundaries established by this audit:

### 1. Equal-Total-Budget Measurement Allocation (Stage 2):
> *'Under a fixed total measurement budget $B_{\text{tot}} = M \cdot S$ on the disordered 1D transverse-field Ising model ($n=8$, open boundaries), full-state quantum fidelity kernels (FQ) and 2-local projected quantum kernels (PQK-2nn) exhibit distinct trade-offs between representation expressiveness and shot-noise variance. At low total budgets ($B_{\text{tot}} \le 10^4$), shot-noise degradation in finite-sample fidelity estimation impairs FQ performance, whereas local correlator models retain greater stability. Above $B_{\text{tot}} \approx 3 \times 10^4$ measurements, empirical Gram repair enables FQ to surpass local correlators in ground-state energy estimation accuracy.'*

### 2. Controlled Out-of-Distribution Generalization (Stage 3):
> *'When evaluated under a controlled distribution shift from the paramagnetic regime ($h_i \in [0.8, 1.5]$) to the ordered ferromagnetic regime ($h_i \in [0.2, 0.7]$) on an $n=8$ disordered TFIM, support vector regression with the full quantum fidelity kernel (FQ) achieved significantly lower mean absolute error on half-chain entanglement entropy than local correlators (OOD MAE: $0.0602 \pm 0.0085$ for FQ vs $0.1850 \pm 0.0334$ for PQK-2nn; paired Wilcoxon $p = 8.51 \times 10^{-4}$, Holm-adjusted $p = 8.51 \times 10^{-4}$ across 20 independent coupling realizations). FQ also significantly outperformed constant training-mean and median baselines (MAE $0.6061$ and $0.6121$, Holm-adjusted $p = 5.72 \times 10^{-6}$). Although negative out-of-distribution $R^2$ values indicate that all models degrade relative to test-set variance, post-hoc decomposition reveals that SVR regularization in an RKHS with decaying cross-domain fidelity overlaps ($0.93$ in-distribution to $0.43$ out-of-distribution) prevents extrapolative runaway, maintaining bounded physical predictions without unconstrained divergence.'*

### 3. Representation Identity:
> *'Consistent with theoretical expectations, the 2-local projected quantum kernel (PQK-2nn) is mathematically and numerically identical to an RBF kernel evaluated on classical nearest-neighbor two-point Pauli correlators ($D_{\text{RDM}} = \frac{1}{4} D_{E2}$ to machine precision $0.00e+00$), confirming that 2-local PQK provides no representation advantage over classical 2-point correlation features for ground states of this Hamiltonian family.'*

### Language Explicitly Prohibited in Future Drafts:
- Do NOT use 'macroscopic phase transition' without clarifying finite-system crossover ($n=8$).
- Do NOT use 'support vector manifold' (not mathematically defined).
- Do NOT use 'unimpeachable' or unqualified 'quantum advantage'.
- Do NOT present Stage 2 and Stage 3 as a joint factorial experiment (they examine distinct settings: measurement budget under noise vs noiseless out-of-distribution generalization).
