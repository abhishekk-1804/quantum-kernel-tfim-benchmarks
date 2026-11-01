# Stage 5 Read-Only Manuscript / Data / Plot Consistency Audit Report

**Workspace:** `D:\quantum-kernel-tfim-benchmarks`  
**Execution Timestamp:** `2026-11-01T07:39:54Z`  
**Completion Timestamp:** `2026-11-01T07:54:00Z`  
**Interpreter:** `D:\qml_env\Scripts\python.exe -B` (`PYTHONDONTWRITEBYTECODE=1`)  
**Audit Output Directory:** `docs/stage5/audit_20261101/`  
**Audit Manifest Baseline:** `docs/stage5/audit_20261101/baseline_manifest.csv` (148 files tracked, 0 mismatches)  
**Permitted Writes:** Strictly confined to `docs/stage5/audit_20261101/` and new helper scripts matching `scripts/audit_s5_*.py`.  
**Manuscript & Result Modification:** Strictly READ-ONLY. Zero edits to `paper/*`, `results/*`, `src/*`, `tests/*`, or pre-existing `scripts/*`.

---

## 1. Executive Findings with Bounded Assurance

This consistency audit performed a static and artifact-driven forensic verification of numerical literals, statistical test results, mathematical formulations, representation identities, figure pipelines, and protocol chronologies across the publication manuscript (`paper/main.tex`, included table files) and primary experimental data (`results/*.csv`, saved numerical arrays, producing code in `src/` and `scripts/`).

### Scope of Bounded Assurance:
1. **Verification of Existing Artifacts Only:** This audit validates consistency between committed and generated artifacts on disk. It does **not** certify that all execution code is bug-free across all untested inputs, nor does it establish physical experimental validity beyond the exact numerical simulations performed.
2. **Read-Only Non-Interference:** No benchmark simulation, state generation, or optimization sweeps were executed during this audit. Distance matrix checks were executed exclusively on pre-existing saved state arrays.
3. **No Security / Network Certification:** Bytecode suppression (`-B`) prevents `.pyc` creation; it does not serve as a general security sandbox. This audit does not evaluate host security, telemetry, or external plugin integrity.

### Primary Audit Highlights:
- **Task Definitions (Section B):** Targets for Task 2a ($\langle Z_0 Z_{n-1} \rangle$, contained control) and Task 2b ($\langle Z_0 Z_1 Z_{n-2} Z_{n-1} \rangle$, non-contained 4-point correlator) are consistently defined between manuscript prose (`paper/main.tex:85, 147, 149`) and production code (`src/hamiltonians.py:446, 465`, `scripts/common.py:34, 36`, `scripts/run_t2_correlators.py:88, 110`). The term "susceptibility" appears in `paper/main.tex:57` solely in the context of "susceptibility to local depolarizing noise", not as a physical spin observable.
- **Figure Lineage (Section C):** Figure 2 (`fig_shots.pdf`) was confirmed to represent $N_{\mathrm{tr}}=40$ (not 80), with x-axis representing total measurement shots across 240 states ($720 \cdot S$ for 3-basis feature arms; $8{,}780 \cdot S$ for deployed FQ; $28{,}680 \cdot S$ for full-Gram simulation), and error bands representing 95% bootstrap confidence intervals. However, because the PDF contains no embedded commit metadata, its historical generation lineage is formally classified as **UNRESOLVED**.
- **Stage 2 Budget Discrepancy (Section D & E):** In `paper/main.tex:188`, the narrative defines shot allocations as $S_{\mathrm{feat}} = B_{\mathrm{tot}} / (M \cdot N_{\mathrm{tr}})$ and $S_{\mathrm{swap}} = B_{\mathrm{tot}} / (N_{\mathrm{tr}}(N_{\mathrm{tr}}-1)/2)$. In contrast, the executing code (`scripts/stage2_equal_budget.py:112-117`) and Table IV use $S_{\mathrm{feat}} = \lfloor B_{\mathrm{tot}} / 720 \rfloor$ ($3 \times 240$ total states) and $S_{\mathrm{swap}} = \lfloor B_{\mathrm{tot}} / 8780 \rfloor$ (780 train pairs + 8,000 test-train pairs). This is an editorial mismatch between prose and code.
- **Section III-C Data Contradiction (Section E):** Line 172 of `paper/main.tex` asserts that unmitigated SVR on raw FQ Gram matrices suffered $R^2 < 0$ at $S=100$, and that eigenvalue clipping restored stability to $R^2 > 0.98$ at $S=1000$. This directly contradicts `results/t5_noise.csv`, where unmitigated FQ-raw achieves mean $R^2 = 0.7634 \pm 0.0116$ at $S=100$ (0/20 seeds $< 0$), and clipped FQ achieves mean $R^2 = 0.8693 \pm 0.0210$ at $S=1000$ (not $> 0.98$).
- **Section III-F Intercept-Only Baseline Mismatch (Section E):** Line 200 of `paper/main.tex` asserts that comparing FQ against the "train-mean baseline" confirms error reduction by $-0.4014 \pm 0.0156$ MAE. In actual verification tables (`full_vs_intercept_summary.csv`), $-0.4014 \pm 0.0156$ is the difference between FQ and the **FQ Intercept-Only baseline** (SVR with kernel weights zeroed, preserving fitted bias $b$). The actual difference between FQ and the Train-Mean baseline is $-0.5459 \pm 0.0075$.
- **Representation Identity (Section G):** On five documented existing states (10 distinct pairs), the raw squared distance before RBF bandwidth scaling matches the edge-summed 2-RDM Frobenius distance to $|D^2_{\mathrm{RDM}} - 0.25 D^2_{E_2}| \le 5.55 \times 10^{-17}$ (max across all 45 pairs: $1.33 \times 10^{-15}$). Coordinate multiplicity (interior $\langle X_i \rangle$ repeated per incident edge) exactly provides the $\sqrt{2}$ weight needed to match Frobenius geometry.
- **Protocol Chronology (Section D):** Both Stage 2 (`dff01711`) and Stage 3 (`292d689d`) protocols and results were committed atomically to Git. No prospective pre-registration or pre-execution commit exists. Their prospective protocol status is classified as **UNRESOLVED / TIMING NOT ESTABLISHED (Exploratory)**.

---

## 2. Item / Status / Evidence / File:Line Table

| Item ID | Location (File:Line) | Observed Evidence | Manuscript Claim | Finding Status |
|---|---|---|---|:---:|
| **IT-01** | `paper/main.tex:85`, `paper/main.tex:147` | `src/hamiltonians.py:446`, `scripts/common.py:34`, `scripts/run_t2_correlators.py:88` | T2a evaluates 2-point correlator $\langle Z_0 Z_{n-1} \rangle$ (contained control). Code evaluates `expect_zz(psi, n, 0, n-1)`. Ridge gets $R^2 = 1.0000$. | **CONSISTENT** |
| **IT-02** | `paper/main.tex:85`, `paper/main.tex:149` | `src/hamiltonians.py:465`, `scripts/common.py:36`, `scripts/run_t2_correlators.py:110` | T2b evaluates 4-point correlator $\langle Z_0 Z_1 Z_{n-2} Z_{n-1} \rangle$ (non-contained). Code evaluates `expect_zzzz(psi, n, 0, 1, n-2, n-1)`. | **CONSISTENT** |
| **IT-03** | `paper/main.tex:57` | Entire codebase grep search | Manuscript mentions "susceptibility to local depolarizing noise". Code does not compute magnetic susceptibility $\chi$. | **CONSISTENT** |
| **IT-04** | `paper/main.tex:164-168` | `scripts/make_figures.py:440-544`, `results/t5_noise.csv` | Figure 2 (`fig_shots.pdf`) plots test $R^2$ vs total shots for $N_{\mathrm{tr}}=40$, $S \in \{100, 1000, 10000\}$ across 20 seeds. | **CONSISTENT** |
| **IT-05** | `paper/figures/fig_shots.pdf` | Filesystem mtime `2026-10-22T15:17:12Z`, Git HEAD `292d689d` | PDF file predates current repository commit and lacks embedded build SHA. Current code reproduces layout. | **UNRESOLVED** (Lineage) |
| **IT-06** | `paper/main.tex:172` | `results/t5_noise.csv` | Prose claims unmitigated FQ-raw suffered $R^2 < 0$ at $S=100$. CSV records mean $R^2 = 0.7634$ (min 0.6719, 0/20 seeds $< 0$). | **MISMATCH** |
| **IT-07** | `paper/main.tex:172` | `results/t5_noise.csv` | Prose claims FQ-clipped restored stability to $R^2 > 0.98$ at $S=1000$. CSV records mean $R^2 = 0.8693 \pm 0.0210$ (max 0.9427). | **MISMATCH** |
| **IT-08** | `paper/main.tex:188` | `scripts/stage2_equal_budget.py:112-117` | Prose formula $S_{\mathrm{feat}} = B_{\mathrm{tot}} / (M \cdot N_{\mathrm{tr}})$ contradicts code $S_{\mathrm{feat}} = \lfloor B_{\mathrm{tot}} / 720 \rfloor$ and Table IV. | **MISMATCH** |
| **IT-09** | `paper/main.tex:188` | `scripts/stage2_equal_budget.py:114` | Prose formula $S_{\mathrm{swap}} = B_{\mathrm{tot}} / \binom{N_{\mathrm{tr}}}{2}$ contradicts code $S_{\mathrm{swap}} = \lfloor B_{\mathrm{tot}} / 8780 \rfloor$ and Table IV. | **MISMATCH** |
| **IT-10** | `paper/tables/tab_equal_budget.tex:14-15` | `scripts/stage2_equal_budget.py:116`, `results/stage2/t1_equal_budget.csv` | At $B_{\mathrm{tot}} \le 30\text{k}$, FQ is marked excluded under minimum-shot policy ($S_{\mathrm{swap}} < 10$). Code sets $S=0$ indicating unexecuted. | **CONSISTENT** |
| **IT-11** | `paper/tables/tab_equal_budget.tex` | `docs/stage5/integration_20261024_002208Z/build/main.log:487` | Table IV causes an Overfull `\hbox` of 101.68 pt, intruding 1.41 inches into the margin. | **MISMATCH** (Layout) |
| **IT-12** | `paper/main.tex:198` | `docs/verification/audit_20261023_155335Z/stage3_mae_comparisons.csv:0` | Retrospective paired Wilcoxon test on OOD MAE for FQ vs PQK-2nn yields $W=21.0$, $p = 8.51 \times 10^{-4}$ ($p_{\mathrm{Holm}} = 8.51 \times 10^{-4}$). | **CONSISTENT** |
| **IT-13** | `paper/main.tex:198` | `docs/stage3/ood_protocol.md`, Git log | Refers to Stage 3 comparison family as "pre-declared". Protocol was committed atomically with results (exploratory). | **MISMATCH** (Classification) |
| **IT-14** | `paper/main.tex:200` | `docs/verification/closure_20261023_163403Z/tables/full_vs_intercept_summary.csv:6` | $-0.4014 \pm 0.0156$ MAE is labeled "train-mean baseline". In data, this is FQ Full Model vs FQ Intercept-Only baseline ($b$). | **MISMATCH** |
| **IT-15** | `paper/main.tex:98-100` | `src/kernels.py:310-336`, `docs/verification/audit_20261023_155335Z/representation_reference_arrays.npz` | Frobenius norm identity: $|D^2_{\mathrm{RDM}} - 0.25 D^2_{E_2}| \le 1.33 \times 10^{-15}$ across all 45 state pairs under $4n=32$ normalizer. | **CONSISTENT** |
| **IT-16** | `paper/main.tex:88` | Analytical Pauli decomposition | Asserts $Z_2$ parity alone zeroes all 1-point and non-diagonal 2-point terms. Parity zeroes 6 terms; reality ($K$) zeroes $Y_i Z_j$ and $Z_i Y_j$. | **MISMATCH** (Theory) |
| **IT-17** | `paper/main.tex:149, 227` | `results/stats.csv` | Uses "statistically indistinguishable" to describe non-significant Wilcoxon tests ($p > 0.05$). | **MISMATCH** (Statistical) |
| **IT-18** | `paper/main.tex:155` | `results/stats.csv:112-119` | Asserts Claim C3 "proves identical asymptotic accuracy". A finite benchmark ($N_{\mathrm{tr}}=160$) cannot prove asymptotic equality. | **MISMATCH** (Statistical) |

---

## 3. Figure Metadata and Provenance Map

| Figure Target | LaTeX File:Line | Generating Script / Function | Source Data Artifact | Training / Test Sizes | Model Arms Included | Uncertainty Representation | Visual Styling & Panels | Caption Alignment | Historical Lineage Status |
|---|---|---|---|---|---|---|---|---|---|
| `figures/fig_learning_curve_t1.pdf` | `paper/main.tex:130` (`\label{fig:t1_lc}`) | `scripts/make_figures.py:make_f1()` | `results/t1_entropy_gridv3.csv` | $N_{\mathrm{tr}} \in \{10, 20, 40, 80, 160\}$, $N_{\mathrm{te}}=200$ | PQK-1, PQK-2nn, FQ, E (raw), E2 (raw), F (std) | 95% bootstrap confidence intervals (10,000 resamples) | Single panel: test $R^2$ vs $N_{\mathrm{tr}}$. Solid/dashed colored curves with shaded error bands. | **Matched:** Caption describes test $R^2$ scaling and PQK-1 saturation. | **UNRESOLVED** (Pre-compiled PDF on disk lacks commit SHA) |
| `figures/fig_shots.pdf` | `paper/main.tex:164` (`\label{fig:shots}`) | `scripts/make_figures.py:make_f5()` | `results/t5_noise.csv` (`experiment == "finite_shots"`) | $N_{\mathrm{tr}}=40$, $N_{\mathrm{te}}=200$, 20 seeds | PQK-1, PQK-2nn, E (raw), E2 (raw), F (std), FQ-clipped, FQ-raw | 95% bootstrap confidence intervals | Two panels: (a) Deployed Evaluation Cost ($8{,}780 \cdot S$ FQ); (b) Full-Gram Simulation Cost ($28{,}680 \cdot S$ FQ). FQ-raw is dashed with marker `x`; FQ-clipped is solid with marker `^`. | **Partial Mismatch:** Caption matches panels, but prose in Line 172 reports erroneous numbers ($R^2 < 0$, $R^2 > 0.98$). | **UNRESOLVED** (Pre-compiled PDF on disk lacks commit SHA) |
| `figures/fig_depolarizing_retuned_per_qubit_proxy.pdf` | `paper/main.tex:176` (`\label{fig:depol}`) | `scripts/make_figures.py:make_f7()` | `results/t5_noise.csv`, `results/t5_depol_fixedhp.csv` | $N_{\mathrm{tr}}=40$, $N_{\mathrm{te}}=200$, 20 seeds | PQK-1, PQK-2nn, FQ, E (raw), E2 (raw), F (std) | 95% bootstrap confidence intervals | Two panels: (a) Hyperparameters re-tuned at each $p \in [0.00, 0.08]$; (b) Fixed $p=0$ hyperparameters. | **Matched:** Caption accurately identifies retuned vs fixed $p=0$ attenuation. | **UNRESOLVED** (Pre-compiled PDF on disk lacks commit SHA) |

---

## 4. Numerical and Statistical Provenance Findings

### A. Task 1 Regression Metrics at $N_{\mathrm{tr}}=160$ (`results/t1_entropy_gridv3.csv`)
All values evaluated across 20 fixed seeds ($N_{\mathrm{tr}}=160$, $N_{\mathrm{te}}=200$):
- **FQ:** Mean $R^2 = 0.997532 \pm 0.000151$ (SD = $0.000677$), Residual Fraction $1 - R^2 = 0.002468$, MAE = $0.007611 \pm 0.000232$.
- **E (raw):** Mean $R^2 = 0.998748 \pm 0.000088$ (SD = $0.000395$), Residual Fraction $1 - R^2 = 0.001252$, MAE = $0.005376 \pm 0.000185$.
- **PQK-2nn:** Mean $R^2 = 0.994321 \pm 0.000376$ (SD = $0.001682$), Residual Fraction $1 - R^2 = 0.005679$, MAE = $0.011321 \pm 0.000361$.
- **E2 (raw):** Mean $R^2 = 0.994242 \pm 0.000400$ (SD = $0.001787$), Residual Fraction $1 - R^2 = 0.005758$, MAE = $0.011405 \pm 0.000385$.
- **PQK-1:** Mean $R^2 = 0.952923 \pm 0.001242$ (SD = $0.005553$), Residual Fraction $1 - R^2 = 0.047077$, MAE = $0.036910 \pm 0.000490$.
- **F (std Ridge):** Mean $R^2 = 0.988690 \pm 0.000434$ (SD = $0.001940$), Residual Fraction $1 - R^2 = 0.011310$, MAE = $0.016757 \pm 0.000345$.
- **Baseline Mean:** Mean $R^2 = -0.008199 \pm 0.003156$, MAE = $0.190353 \pm 0.001767$.

*Analytical Observation:* While the absolute difference in mean $R^2$ between FQ and E(raw) is small ($-0.0012$), the unexplained residual variance $(1 - R^2)$ of FQ is **$1.97\times$ higher** than that of classical E(raw). PQK-2nn residual variance is **$4.53\times$ higher** than E(raw).

### B. Statistical P-Values and Testing Hierarchy (`results/stats.csv`)
1. **Task 1 PQK-1 vs PQK-2nn:**
   - At $N_{\mathrm{tr}}=10$: Mean diff = $-0.1044$, $W=27.0$, raw $p = 0.002325$, Holm-adjusted $p_{\mathrm{Holm}} = 0.018600$. **Matched:** Cited as $0.0186$ in `main.tex:138`.
   - At $N_{\mathrm{tr}}=160$: Mean diff = $-0.0414$, $W=0.0$, raw $p = 1.91 \times 10^{-6}$, Holm-adjusted $p_{\mathrm{Holm}} = 1.53 \times 10^{-5}$. **Matched:** Cited as $1.53 \times 10^{-5}$ in `main.tex:138`.
2. **Task 1 FQ vs PQK-2nn:**
   - At $N_{\mathrm{tr}}=160$: Mean diff = $+0.0032$, $W=0.0$, raw $p = 1.91 \times 10^{-6}$, Holm-adjusted $p_{\mathrm{Holm}} = 1.53 \times 10^{-5}$.
   - Classification in `stats.csv`: **`exploratory`** (Row 34). Confirmatory ex-ante testing was strictly reserved for PQK-1 vs PQK-2nn, PQK-2nn vs E (raw), and FQ vs E (raw).
3. **Stage 3 OOD Shift FQ vs PQK-2nn:**
   - Evaluated on $N_{\mathrm{tr}}=40$, $N_{\mathrm{te}}=100$, 20 seeds.
   - Mean paired difference $\Delta\mathrm{MAE} = -0.1248 \pm 0.0334$ (FQ lower MAE in 16/20 seeds).
   - Wilcoxon signed-rank test: $W=21.0$, raw $p = 8.51 \times 10^{-4}$, Holm-adjusted $p_{\mathrm{Holm}} = 8.51 \times 10^{-4}$ (Family size = 3: FQ vs PQK-2nn, FQ vs Train-Mean, FQ vs Train-Median). **Matched:** Cited in `main.tex:198`.

---

## 5. Actual Stage 2 / Stage 3 Budget Inventory

### A. Stage 2 Equal-Total-Budget Inventory (`results/stage2/t1_equal_budget.csv`)
- **File Metrics:** 980 rows, 10 columns, SHA-256 `22d66cd6...`, mtime `2026-10-23T14:53:44Z`.
- **Budgets Evaluated:** $B_{\mathrm{tot}} \in \{10^4, 3\times 10^4, 10^5, 3\times 10^5, 10^6, 3\times 10^6, 10^7\}$ (7 budget tiers).
- **Seeds:** 20 seeds ($0..19$).
- **Models & Variants:**
  * PQK-1: `3basis` ($S = \lfloor B_{\mathrm{tot}} / 720 \rfloor$) and `x_only` ($S = \lfloor B_{\mathrm{tot}} / 240 \rfloor$).
  * PQK-2nn: `none` ($S = \lfloor B_{\mathrm{tot}} / 720 \rfloor$).
  * E2: `raw_4n_grid` ($S = \lfloor B_{\mathrm{tot}} / 720 \rfloor$).
  * FQ: `train_only`, `none`, and `inductive` ($S = \lfloor B_{\mathrm{tot}} / 8780 \rfloor$).
- **Shot Allocation and Execution Accounting:**

| Total Budget $B_{\mathrm{tot}}$ | Feature Arm Shots ($S_{\mathrm{feat}}$) | FQ Swap Shots ($S_{\mathrm{swap}}$) | FQ Status | PQK-2nn Test $R^2$ (Mean $\pm$ SE) | FQ (train_only) Test $R^2$ (Mean $\pm$ SE) | Paired $\Delta R^2$ (FQ $-$ PQK-2nn) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **$10{,}000$** | 13 | 0 (raw: 1) | Excluded ($S < 10$) | $0.4637 \pm 0.0284$ | *Excluded* | *N/A* |
| **$30{,}000$** | 41 | 0 (raw: 3) | Excluded ($S < 10$) | $0.7289 \pm 0.0133$ | *Excluded* | *N/A* |
| **$100{,}000$** | 138 | 11 | Feasible | $0.8814 \pm 0.0088$ | $0.0932 \pm 0.0534$ | $-0.7882 \pm 0.0560$ |
| **$300{,}000$** | 416 | 34 | Feasible | $0.9380 \pm 0.0034$ | $0.6459 \pm 0.0164$ | $-0.2921 \pm 0.0171$ |
| **$1{,}000{,}000$** | 1,388 | 113 | Feasible | $0.9575 \pm 0.0026$ | $0.8288 \pm 0.0067$ | $-0.1287 \pm 0.0067$ |
| **$3{,}000{,}000$** | 4,166 | 341 | Feasible | $0.9703 \pm 0.0027$ | $0.8777 \pm 0.0074$ | $-0.0926 \pm 0.0073$ |
| **$10{,}000{,}000$** | 13,888 | 1,138 | Feasible | $0.9753 \pm 0.0024$ | $0.8828 \pm 0.0130$ | $-0.0924 \pm 0.0126$ |

### B. Stage 3 Controlled OOD Inventory (`results/stage3/t6_ood_shift.csv`)
- **File Metrics:** 100 rows, 10 columns, SHA-256 `81908f5a...`, mtime `2026-10-23T15:33:35Z`.
- **Ensemble Dimensions:** $n=8$ open chain, $N_{\mathrm{tr}}=40$, $N_{\mathrm{te}}=100$, 20 seeds ($0..19$).
- **Domains:** In-distribution $h_i \in [0.8, 1.5]$ (paramagnetic/critical); Out-of-distribution $h_i \in [0.2, 0.7]$ (ferromagnetic).
- **Models Evaluated:**
  * FQ (`none`): In-Dist $R^2 = 0.9977 \pm 0.0002$, OOD MAE = $0.0602 \pm 0.0085$.
  * PQK-1 (`none`): In-Dist $R^2 = 0.9141 \pm 0.0056$, OOD MAE = $0.3789 \pm 0.0623$.
  * PQK-2nn (`none`): In-Dist $R^2 = 0.9943 \pm 0.0007$, OOD MAE = $0.1850 \pm 0.0294$.
  * E2 (4n) (`raw_4n_grid`): In-Dist $R^2 = 0.9943 \pm 0.0007$, OOD MAE = $0.1850 \pm 0.0294$.
  * Linear Ridge: In-Dist $R^2 = 0.9928 \pm 0.0007$, OOD MAE = $0.1345 \pm 0.0136$.
  * *Omitted Baseline:* Classical all-pairs $E(\text{raw})$ RBF was omitted from Stage 3.

---

## 6. Protocol Chronology and Limitations

### Git Commit Ledger:
- Commit `dff0171183c99c43f9555964ba0a88731ddc98cf`:
  * Date: `2026-10-23T15:02:50Z` (20:32:50 +05:30)
  * Subject: `feat(stage2): complete equal-total-budget benchmark and crossover analysis`
  * Artifacts: `results/stage2/t1_equal_budget.csv`, `scripts/stage2_equal_budget.py`, `scripts/stage2_analysis.py`, `tests/test_stage2_budget.py`.
- Commit `292d689dd845f6228fae6265cffe83b81d5f0f66`:
  * Date: `2026-10-23T15:41:11Z` (21:11:11 +05:30)
  * Subject: `feat(stage3): complete controlled OOD phase-shift generalization benchmark`
  * Artifacts: `results/stage3/t6_ood_shift.csv`, `scripts/stage3_ood_shift.py`, `scripts/stage3_analysis.py`, `docs/stage3/ood_protocol.md`, `tests/test_stage3_ood.py`.

### Provenance Limitations:
1. **Atomic Commits:** Both protocols were committed in the exact same commits as the experimental code and output CSV files.
2. **Filesystem Timestamps:** File modification times (`mtime`) on Windows reflect local file creation or checkout time; they do not establish independent cryptographic pre-registration.
3. **Formal Epistemic Classification:** Per open-science auditing standards, because prospective protocol freezing prior to data generation cannot be demonstrated from Git logs, Stages 2 and 3 are classified as:
   **`Exploratory (documented protocol, timing not established)`**.

---

## 7. Representation Distance Check

Conducted on pre-existing saved state arrays in `docs/verification/audit_20261023_155335Z/representation_reference_arrays.npz`:
- **States Checked:** 5 documented states (indices $0, 1, 2, 3, 4$), comprising 10 distinct state pairs.
- **System & Boundary:** 1D TFIM, $n=8$ spins, open boundary condition ($n-1 = 7$ nearest-neighbor edges).
- **Feature Map:** `mode="2pt_pauli_nn"` (35 dimensions: 5 Pauli expectations $\times$ 7 edges).
- **Comparison Formula:**
  $$\sum_{\text{edges}} \|\rho_{ij}(\psi) - \rho_{ij}(\phi)\|_F^2 \quad \text{vs} \quad \frac{1}{4} \|f_{E_2}(\psi) - f_{E_2}(\phi)\|_2^2$$
- **Empirical Residuals:**
  * Pair $[0, 1]$: $D^2_{\mathrm{RDM}} = 0.17104077911912613$, $0.25 D^2_{E_2} = 0.17104077911912610$, Diff = $2.78 \times 10^{-17}$.
  * Pair $[0, 2]$: $D^2_{\mathrm{RDM}} = 0.16452456461280723$, $0.25 D^2_{E_2} = 0.16452456461280730$, Diff = $5.55 \times 10^{-17}$.
  * Pair $[0, 3]$: $D^2_{\mathrm{RDM}} = 0.12548447109351474$, $0.25 D^2_{E_2} = 0.12548447109351474$, Diff = $0.00$.
  * Pair $[0, 4]$: $D^2_{\mathrm{RDM}} = 0.08044887602045891$, $0.25 D^2_{E_2} = 0.08044887602045890$, Diff = $1.39 \times 10^{-17}$.
  * Pair $[1, 2]$: $D^2_{\mathrm{RDM}} = 0.06863582243528214$, $0.25 D^2_{E_2} = 0.06863582243528214$, Diff = $0.00$.
  * Pair $[1, 3]$: $D^2_{\mathrm{RDM}} = 0.27785054768063830$, $0.25 D^2_{E_2} = 0.27785054768063830$, Diff = $0.00$.
  * Pair $[1, 4]$: $D^2_{\mathrm{RDM}} = 0.13944707845815812$, $0.25 D^2_{E_2} = 0.13944707845815812$, Diff = $0.00$.
  * Pair $[2, 3]$: $D^2_{\mathrm{RDM}} = 0.18836746381212938$, $0.25 D^2_{E_2} = 0.18836746381212935$, Diff = $2.78 \times 10^{-17}$.
  * Pair $[2, 4]$: $D^2_{\mathrm{RDM}} = 0.11124377119254520$, $0.25 D^2_{E_2} = 0.11124377119254518$, Diff = $1.39 \times 10^{-17}$.
  * Pair $[3, 4]$: $D^2_{\mathrm{RDM}} = 0.17799149117293640$, $0.25 D^2_{E_2} = 0.17799149117293633$, Diff = $5.55 \times 10^{-17}$.
- **Maximum Absolute Residual (10 pairs):** **$5.55 \times 10^{-17}$** (Fixed tolerance: $10^{-12}$).
- **Maximum Absolute Residual (all 45 pairs):** **$1.33 \times 10^{-15}$**.
- **Negative Control (unweighted single-site terms):** Max residual = **$0.0424$** (10 pairs) and **$0.5614$** (45 pairs).
- **Coordinate Multiplicity:** Confirmed. Interior terms $\langle X_i \rangle$ ($i=1..6$) are repeated in both adjacent edge RDMs, which algebraically supplies the $\sqrt{\text{deg}_i} = \sqrt{2}$ factor required to equate Euclidean and Frobenius squared distances.

---

## 8. Protected File Baseline Verification & Git State

### Baseline Hash Audit Summary:
- **Baseline Manifest:** `docs/stage5/audit_20261101/baseline_manifest.csv`
- **Total Tracked Files:** 148 files across `paper/`, `results/`, `src/`, `tests/`, and `scripts/`.
- **Pre-Audit vs Post-Audit Mismatches:** **0 mismatches (100% bit-for-bit preserved)**.
- **Raw Benchmark CSV Files:**
  * `results/t1_entropy_gridv3.csv`: `619151b90777046a647c093187c83c4745a389caf39c37aa0178f11e1638f37b` (**MATCH**)
  * `results/stats.csv`: `62fca5f51e29838097a31e4b72e62a2177b279ce27f14d2ecc76f1b111c3c560` (**MATCH**)
  * `results/stage2/t1_equal_budget.csv`: `22d66cd6e27372a53936b7d7aa4d9317878367aefebc0560a8be0a6bbbf955bd` (**MATCH**)
  * `results/stage3/t6_ood_shift.csv`: `81908f5a14f0c7c262b1647964b02fbd7570ba737a2dd4f3420659be8da139cb` (**MATCH**)

### Initial Git State:
```
 M paper/main.tex
 M paper/references.bib
?? docs/provenance/
?? docs/stage4/
?? docs/stage5/
?? docs/stage6/
?? docs/verification/
?? paper/tables/tab_equal_budget.tex
?? paper/tables/tab_ood.tex
?? scripts/audit_representation_identity.py
?? scripts/audit_stage2_sampling.py
?? scripts/audit_stage3_metrics.py
```
`git diff --stat`:
```
 paper/main.tex       | 57 +++++++++++++++++++++++++++++++++++++---------------
 paper/references.bib | 22 ++++++++++++++++++++
 2 files changed, 63 insertions(+), 16 deletions(-)
```

### Final Git State:
```
 M paper/main.tex
 M paper/references.bib
?? docs/provenance/
?? docs/stage4/
?? docs/stage5/
?? docs/stage6/
?? docs/verification/
?? paper/tables/tab_equal_budget.tex
?? paper/tables/tab_ood.tex
?? scripts/audit_representation_identity.py
?? scripts/audit_s5_anchors.py
?? scripts/audit_s5_baseline.py
?? scripts/audit_s5_claims_audit.py
?? scripts/audit_s5_distance_check.py
?? scripts/audit_s5_fig_details.py
?? scripts/audit_s5_numerical_claims.py
?? scripts/audit_s5_stage2_3_chronology.py
?? scripts/audit_s5_statistical_provenance.py
?? scripts/audit_s5_tasks.py
?? scripts/audit_s5_trace_figs.py
?? scripts/audit_stage2_sampling.py
?? scripts/audit_stage3_metrics.py
```
`git diff --stat`:
```
 paper/main.tex       | 57 +++++++++++++++++++++++++++++++++++++---------------
 paper/references.bib | 22 ++++++++++++++++++++
 2 files changed, 63 insertions(+), 16 deletions(-)
```

---

## 9. Categorized Remediation Lists

### A. Editorial Correction Candidates (Manuscript Text Only — No Simulations Needed)
1. **Line 172 (Section III-C Prose Correction):**
   Replace erroneous narrative claims ($R^2 < 0$ at $S=100$, $R^2 > 0.98$ at $S=1000$) with verified empirical metrics from `results/t5_noise.csv`: unmitigated FQ-raw achieves mean $R^2 = 0.7634 \pm 0.0116$ at $S=100$; PSD clipping improves performance to $0.8101 \pm 0.0093$ at $S=100$ and $0.8693 \pm 0.0210$ at $S=1000$.
2. **Line 188 (Section III-E Budget Formula Harmonization):**
   Update formula text to state $S_{\mathrm{feat}} = \lfloor B_{\mathrm{tot}} / (3 \cdot N_{\mathrm{tot}}) \rfloor$ ($N_{\mathrm{tot}}=240$) and $S_{\mathrm{swap}} = \lfloor B_{\mathrm{tot}} / (\binom{N_{\mathrm{tr}}}{2} + N_{\mathrm{tr}} N_{\mathrm{te}}) \rfloor$ to match the actual code and Table IV.
3. **Line 200 (Section III-F Intercept-Only Baseline Mismatch):**
   Correct the label from "train-mean baseline" to "FQ Intercept-Only baseline" ($f(x) = b$), or update the reported difference to the actual Train-Mean difference ($-0.5459 \pm 0.0075$).
4. **Lines 149 & 227 (Statistical Language Tempering):**
   Replace "statistically indistinguishable" with "no statistically significant difference detected within observed resolution ($p_{\mathrm{Holm}} > 0.05$)".
5. **Line 155 (Claim C3 Asymptotic Claim):**
   Replace "proves ... identical asymptotic accuracy" with "demonstrates empirical sample-efficiency parity at $N_{\mathrm{tr}}=160$".
6. **Line 88 (Symmetry Theory Clarification):**
   Clarify that $X$-parity zeroes 6 Pauli expectation terms, while Hamiltonian reality ($K H K^{-1} = H$) zeroes the remaining two terms ($Y_i Z_j$ and $Z_i Y_j$).
7. **Line 198 (Stage 3 Protocol Status):**
   Replace "pre-declared three-comparison family" with "retrospective three-comparison family".
8. **Table IV Formatting (`paper/tables/tab_equal_budget.tex`):**
   Reduce `\tabcolsep` from 4.5pt to 3.0pt and shorten column headers to eliminate the 101.68 pt Overfull `\hbox`.

### B. Artifact Regeneration Candidates
- None required. All primary CSV files (`results/*.csv`) and figure scripts are self-consistent and intact.

### C. Additional Evaluation Candidates (Future Work / Not Required for Current Scope)
1. **All-Pairs $E(\text{raw})$ on OOD Shift:** The full all-pairs correlator model was omitted from Stage 3; executing this in future work would test if non-local classical features track FQ extrapolation.
2. **Finite-Shot Sampling in OOD Shift:** Stage 3 was evaluated on ideal statevectors; simulating finite swap shots under phase shift would test whether FQ's MAE advantage survives measurement noise.
3. **Order Parameter Computation:** Direct evaluation of Edwards-Anderson order parameter $q$ or entanglement spectrum gap to formally certify phase boundaries rather than relying on nominal $h_i$ ranges.

### D. Unresolved Evidence Requirements
1. **Pre-Compiled Figure PDF Lineage:** The PDF figures in `paper/figures/` match the plotting scripts, but lack cryptographic build manifests linking them to a specific Git commit SHA.
2. **Prospective Timing of Stages 2 and 3:** Prospective protocol pre-registration timing is unresolvable from Git history alone due to atomic commits. Both stages must remain formally designated as **Exploratory**.
