# Forensic Read-Only Technical Audit Report: Reviewer-Flagged Issues
**Workspace:** `D:\quantum-kernel-tfim-benchmarks`  
**Execution Timestamp:** `20261025_055950Z`  
**Interpreter:** `D:\qml_env\Scripts\python.exe -B` (Bytecode generation suppressed)  
**Execution Safety Mode:** Strict Read-Only Static Inspection & Pre-computed Artifact Audit  
**Target File Allowlist:** Confined strictly to `docs/stage5/reviewer_flaw_audit_20261025_055950Z/`  

---

## A. Executive Findings

This forensic audit evaluated six technical domains flagged in reviewer and internal methodological critiques across `paper/main.tex`, `paper/tables/*.tex`, `src/*.py`, `scripts/*.py`, and `results/*.csv`. Every finding has been classified under the required four-tier evidence scheme (**VERIFIED IMPLEMENTATION FACT**, **VERIFIED MANUSCRIPT FACT**, **INFERENCE**, or **UNRESOLVED**).

### High-Level Summary of Findings:
1. **Measurement Budget Formula Discrepancy (Audit 1):**
   - In `paper/main.tex` (Line 188), the stated measurement formulas are:
     $$S_{\mathrm{feat}} = B_{\mathrm{tot}} / (M \cdot N_{\mathrm{tr}}), \quad S_{\mathrm{swap}} = B_{\mathrm{tot}} / (N_{\mathrm{tr}}(N_{\mathrm{tr}}-1)/2)$$
   - In the actual execution code (`scripts/stage2_equal_budget.py`, Lines 112–117), the denominators are fundamentally different:
     $$S_{\mathrm{feat}} = \lfloor B_{\mathrm{tot}} / 720 \rfloor, \quad S_{\mathrm{swap}} = \lfloor B_{\mathrm{tot}} / 8780 \rfloor$$
     where $720 = 3 \cdot (N_{\mathrm{tr}} + N_{\mathrm{te}}) = 3 \cdot 240$ measurement settings, and $8{,}780 = \binom{40}{2} + 40 \times 200 = 780 + 8{,}000$ pairwise swap tests (accounting for all training and deployment pairs).
   - The manuscript text in Line 188 conflated measurement settings with observable counts, and omitted test-set measurement costs from the formula, creating an apparent contradiction with Table IV.
   - Three global basis rotations ($X, Y, Z$) simultaneously measure all 35 local and nearest-neighbor observables via bitstring post-processing; single-setting outcomes are reused across sites and pairs, preserving empirical covariance.
   - For $B_{\mathrm{tot}} \le 30{,}000$, $S_{\mathrm{swap}} = 0$ is recorded because under the pre-declared minimum-shot policy ($S \ge 10$), circuits with $S < 10$ ($1$ at $10\text{k}$, $3$ at $30\text{k}$) were deliberately unexecuted (0 shots expended).

2. **Representation Identity, Symmetry & Multiplicity (Audit 2):**
   - The algebraic identity between `PQK-2nn` and `E2(raw)` is confirmed to machine precision ($|D^2_{\mathrm{RDM}} - D^2_{\mathrm{Pauli}}| \le 1.33 \times 10^{-15}$).
   - In production code (`src/kernels.py`, Lines 310–337), the 35-dimensional `E2` feature vector extracts five Pauli observables per open-chain edge. Interior single-site $\langle X_i \rangle$ terms ($i=1..6$) are repeated across both incident edges, which exactly provides the $\sqrt{\text{deg}_i} = \sqrt{2}$ multiplicity weighting required to match the edge-summed 2-RDM Frobenius distance.
   - An analytical symmetry flaw was identified in the narrative: $X$-Parity ($P = \prod X_k$) enforces $\langle Z_i \rangle = \langle Y_i \rangle = \langle X_i Z_j \rangle = \langle Z_i X_j \rangle = \langle X_i Y_j \rangle = \langle Y_i X_j \rangle = 0$ (6 terms), but does **not** vanish $\langle Y_i Z_j \rangle$ or $\langle Z_i Y_j \rangle$, because $P(Y_i Z_j)P = (-Y_i)(-Z_j) = + Y_i Z_j$ is parity-even.
   - $\langle Y_i Z_j \rangle$ and $\langle Z_i Y_j \rangle$ vanish strictly due to **Reality / Complex Conjugation symmetry** ($K H K^{-1} = H^* = H$ in the computational $Z$-basis). Physical spin time reversal $\Theta = \prod (-i Y_k) K$ is explicitly broken by the magnetic field $-h_i X_i$.

3. **Gram Matrix PSD Repair & Test Independence (Audit 3):**
   - In `"train_only"` mode, $K_{\mathrm{tr}}$ is projected onto the PSD cone via `fidelity_clip_psd` (symmetrized, eigenvalues clipped at 0, diagonal congruence normalized to 1.0), while $K_{\mathrm{te}}$ is passed unclipped.
   - Zero test states influence the training eigendecomposition in either `"train_only"` or `"inductive"` modes.
   - Libsvm's precomputed SVR solver processes indefinite Gram matrices without throwing an exception, but converges to non-convex saddle points resulting in degraded predictions.

4. **Prose vs Data Contradiction in Section III-C (Audit 4):**
   - In `paper/main.tex` (Line 172), the narrative asserts:
     * "Unmitigated SVR on indefinite Gram matrices suffered catastrophic degradation ($R^2 < 0$ at $S=100$)."
     * "Eigenvalue thresholding ... successfully restored stability ($R^2 > 0.98$ at $S=1000$)."
   - This assertion directly contradicts the primary data in `results/t5_noise.csv`, `results/ablations/t5_fq_repairs.csv`, and Figure 2 (`fig_shots.pdf`):
     * In `t5_noise.csv`, unmitigated `FQ-raw` at $S=100$ achieves mean $R^2 = 0.7634$ (min 0.6719, max 0.8623) across all 20 seeds (zero seeds have $R^2 < 0$).
     * At $S=1000$, `FQ-clipped` achieves mean $R^2 = 0.8693$ (min 0.5557, max 0.9427), NOT $R^2 > 0.98$.
     * Figure 2's y-axis is bounded in $[0.70, 1.01]$; negative $R^2$ values are physically absent.

5. **Statistical Claims, Estimands & Seed Hierarchy (Audit 5):**
   - The 20 benchmark seeds regenerate independent sets of 360 disordered Hamiltonian ground states ($160$ train pool $+ 200$ test states per seed). They do not recycle a single fixed state pool.
   - The manuscript contains overstatements: claiming models are "statistically indistinguishable" (Lines 149, 227) and that Claim C3 "proves identical asymptotic accuracy" (Line 155). These conflate finite-sample nonsignificance with proof of equivalence.
   - At $N_{\mathrm{tr}}=160$ in Task 1, while absolute $R^2$ differences appear small ($-0.0012$ for FQ vs E(raw), $+0.0032$ for FQ vs PQK-2nn), the unexplained residual variance $(1 - R^2)$ for FQ ($0.002468$) is nearly double ($1.97\times$) that of E(raw) ($0.001252$), and PQK-2nn ($0.005679$) is $4.53\times$ higher.

6. **Stage 3 OOD Benchmarks & Layout (Audit 6):**
   - The strongest classical non-linear baseline, all-pairs $E(\text{raw})$ RBF, was omitted from Stage 3; only nearest-neighbor $E_2(4n)$ and Linear Ridge were evaluated.
   - Phase labels ("Paramagnetic" vs "Ferromagnetic") were assigned based on parameter ranges without computing order parameters, correlation lengths, or spectral gaps.
   - LaTeX build logs confirm an Overfull `\hbox` of **101.68 pt** on Table IV (`tab_equal_budget.tex`) and **37.22 pt** on Table I (`tab1_t1_r2.tex`).

---

## B. Evidence Table

| Issue ID | File Path & Exact Lines | Classification Tag | Observed Evidence | Scientific Consequence | Minimal Corrective Action | Rerun Status |
|---|---|---|---|---|---|:---:|
| **E1** | `paper/main.tex` Line 188 | **VERIFIED MANUSCRIPT FACT** | Manuscript defines $S_{\mathrm{feat}} = B_{\mathrm{tot}} / (M \cdot N_{\mathrm{tr}})$ and $S_{\mathrm{swap}} = B_{\mathrm{tot}} / (N_{\mathrm{tr}}(N_{\mathrm{tr}}-1)/2)$. | Text formula does not match the actual code denominators ($720$ and $8{,}780$). | Update Line 188 to state $S_{\mathrm{feat}} = \lfloor B_{\mathrm{tot}} / (3 \cdot N_{\mathrm{tot}}) \rfloor$ ($N_{\mathrm{tot}}=240$) and $S_{\mathrm{swap}} = \lfloor B_{\mathrm{tot}} / (\binom{N_{\mathrm{tr}}}{2} + N_{\mathrm{tr}} N_{\mathrm{te}}) \rfloor$. | Unnecessary |
| **E2** | `scripts/stage2_equal_budget.py` Lines 112–117 | **VERIFIED IMPLEMENTATION FACT** | Code uses `B_tot // 720` for 3-basis feature arms and `B_tot // 8780` for FQ swap tests. | Produces the exact integers displayed in Table IV columns 2 and 3. | Harmonize manuscript narrative with the verified code implementation. | Unnecessary |
| **E3** | `paper/tables/tab_equal_budget.tex` Lines 14–15 | **VERIFIED MANUSCRIPT FACT** | At $B_{\mathrm{tot}} \in \{10\text{k}, 30\text{k}\}$, FQ is marked "Excluded under minimum-shot policy ($S_{\mathrm{swap}} < 10$)". | Pre-policy shot values ($S=1, 3$) are clamped to 0 to indicate zero executed shots. | Text is accurate; ensure caption explicitly notes $S_{\mathrm{swap}}=0$ indicates unexecuted circuits. | Unnecessary |
| **E4** | `paper/main.tex` Lines 88, 100 | **VERIFIED MANUSCRIPT FACT** | Section II-B asserts $Z_2$ parity symmetry alone zeroes all 1-point and non-diagonal 2-point terms. | Incomplete physics: $Y_i Z_j$ and $Z_i Y_j$ are parity-even; they vanish due to wavefunction reality ($K$). | Clarify that parity zeroes 6 Pauli terms, while reality ($K H K^{-1}=H$) zeroes the remaining 2 terms. | Unnecessary |
| **E5** | `src/kernels.py` Lines 310–336 | **VERIFIED IMPLEMENTATION FACT** | `mode="2pt_pauli_nn"` extracts 35 features per state; interior $\langle X_i \rangle$ terms are repeated per incident edge. | Edge repetition provides exact $\sqrt{\text{deg}_i}$ weight, making squared Euclidean distance equal to edge 2-RDM Frobenius distance. | Document the exact algebraic identity and multiplicity correspondence in Section II-B. | Unnecessary |
| **E6** | `docs/verification/audit_20261023_155335Z/representation_reference_arrays.npz` | **VERIFIED IMPLEMENTATION FACT** | `max |D_RDM - D_prod_pqk2| == 1.33e-15` and `max |D_prod_pqk2 - D_prod_e2_div4| == 0.0`. | Proves `PQK-2nn` and `E2(raw)` are algebraically identical under identical normalizer grids. | Reconcile historical performance divergence as a 9.4% grid normalizer difference ($c/32$ vs $c/35$). | Unnecessary |
| **E7** | `paper/main.tex` Line 172 | **VERIFIED MANUSCRIPT FACT** | Asserts FQ-raw suffered $R^2 < 0$ at $S=100$ and FQ-clipped restored $R^2 > 0.98$ at $S=1000$. | Directly contradicted by `t5_noise.csv` (FQ-raw is $0.7634$ at $S=100$; FQ-clipped is $0.8693$ at $S=1000$). | Correct Line 172 to reflect actual CSV metrics ($R^2 = 0.7634$ unmitigated, $0.8693$ clipped). | Unnecessary |
| **E8** | `scripts/make_figures.py` Lines 440–543 | **VERIFIED IMPLEMENTATION FACT** | Figure 2 (`fig_shots.pdf`) plots `t5_noise.csv` with y-axis $[0.70, 1.01]$; matches CSV numbers exactly. | Figure is correct; prose in Section III-C was hand-typed/erroneous. | Update prose to match Figure 2 and `t5_noise.csv`. | Unnecessary |
| **E9** | `paper/main.tex` Lines 149, 155, 227 | **VERIFIED MANUSCRIPT FACT** | Uses "statistically indistinguishable" and "proves identical asymptotic accuracy". | Overstated statistical language; non-significant $p$-value ($p > 0.05$) does not prove equivalence. | Replace with "statistically indistinguishable within observed resolution" and "demonstrates empirical sample-efficiency parity". | Unnecessary |
| **E10** | `scripts/common.py` Lines 17–48 | **VERIFIED IMPLEMENTATION FACT** | `_get_disordered_tfim_ensemble` uses `rng = np.random.default_rng(seed)` to generate 360 unique Hamiltonians per seed. | Confirms 20 seeds constitute 20 independent physical disorder realizations. | Reaffirm independent disorder realizations in Section II-A. | Unnecessary |
| **E11** | `results/stage3/t6_ood_shift.csv` | **VERIFIED IMPLEMENTATION FACT** | Stage 3 evaluates `FQ`, `PQK-1`, `PQK-2nn`, `E2 (4n)`, and `Linear_Ridge`. | All-pairs $E(\text{raw})$ RBF was omitted from Stage 3. | Document omission of all-pairs $E(\text{raw})$ in Section III-F. | Unnecessary |
| **E12** | `scripts/stage3_ood_shift.py` Lines 103–129 | **VERIFIED IMPLEMENTATION FACT** | Disordered ground states are sampled without evaluating order parameter $q$, gap $\Delta$, or correlation length $\xi$. | Phase labels are heuristic based on $h_i$ ranges rather than calculated physical order parameters. | Qualify phase labels as nominal parameter regimes in Section III-F. | Unnecessary |
| **E13** | `docs/stage5/integration_20261024_002208Z/build/main.log` | **VERIFIED IMPLEMENTATION FACT** | Build log reports Overfull `\hbox` of 101.68 pt on `tab_equal_budget.tex` and 37.22 pt on `tab1_t1_r2.tex`. | Table IV intrudes into outer page margin by 1.41 inches. | Adjust column widths or column separation in `tab_equal_budget.tex`. | Unnecessary |

---

## C. Budget Ledger (Table IV Audit)

### 1. Row-by-Row Budget Verification

| Requested Budget $B_{\mathrm{tot}}$ | Manuscript Line 188 Denominators | Code Implementation Denominators | $S_{\mathrm{feat}}$ (Code) | $S_{\mathrm{swap}}$ (Code) | Actual Circuit Shots Spent | State Preps (Feature) | State Preps (FQ Swap Test) | Feasibility Status |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **$10{,}000$** | $35 \times 40 = 1{,}400$ / $780$ | $720$ / $8{,}780$ | 13 | 0 (raw: 1) | 9,360 | 9,360 | 0 (unexecuted) | Excluded ($S < 10$) |
| **$30{,}000$** | $1{,}400$ / $780$ | $720$ / $8{,}780$ | 41 | 0 (raw: 3) | 29,520 | 29,520 | 0 (unexecuted) | Excluded ($S < 10$) |
| **$100{,}000$** | $1{,}400$ / $780$ | $720$ / $8{,}780$ | 138 | 11 | 99,360 (feat) / 96,580 (FQ) | 99,360 | 193,160 ($2 \times 96{,}580$) | Feasible |
| **$300{,}000$** | $1{,}400$ / $780$ | $720$ / $8{,}780$ | 416 | 34 | 299,520 (feat) / 298,520 (FQ) | 299,520 | 597,040 ($2 \times 298{,}520$) | Feasible |
| **$1{,}000{,}000$** | $1{,}400$ / $780$ | $720$ / $8{,}780$ | 1,388 | 113 | 999,360 (feat) / 992,140 (FQ) | 999,360 | 1,984,280 ($2 \times 992{,}140$) | Feasible |
| **$3{,}000{,}000$** | $1{,}400$ / $780$ | $720$ / $8{,}780$ | 4,166 | 341 | 2,999,520 (feat) / 2,993,980 (FQ) | 2,999,520 | 5,987,960 ($2 \times 2{,}993{,}980$) | Feasible |
| **$10{,}000{,}000$** | $1{,}400$ / $780$ | $720$ / $8{,}780$ | 13,888 | 1,138 | 9,999,360 (feat) / 9,991,640 (FQ) | 9,999,360 | 19,983,280 ($2 \times 9{,}991{,}640$) | Feasible |

### 2. Analysis of the Feature Measurement Model
- **Measurement Settings vs Observables:** In `scripts/stage2_equal_budget.py` (Lines 314–329), the feature arms execute exactly **3 global measurement settings** per state:
  1. Setting 1: Global rotation $U_X^{\otimes n}$ followed by computational-basis readout.
  2. Setting 2: Global rotation $U_Y^{\otimes n}$ followed by computational-basis readout.
  3. Setting 3: Direct computational-basis readout (Z basis).
- **Observable Extraction & Covariance:** From the single sample of $S_{\mathrm{feat}}$ bitstrings in Setting 1, the code extracts both local magnetizations $\langle X_i \rangle$ and all nearest-neighbor correlators $\langle X_i X_{i+1} \rangle$. Because they are computed from the identical sampled bitstring distribution, single-setting outcomes are reused across sites and pairs, preserving empirical covariance.
- **Cross-Axis Observables:** The 35 observables in $E_2$ are strictly collinear ($X_i, X_{i+1}, X_i X_{i+1}, Y_i Y_{i+1}, Z_i Z_{i+1}$). Zero cross-axis observables (e.g. $X_i Y_j$) are included; hence, exactly 3 settings are physically and mathematically sufficient.
- **State Copy Discrepancy:** Each swap-test shot requires **2 state copies** ($|\psi\rangle$ and $|\phi\rangle$), whereas each feature measurement shot consumes **1 state copy**. Consequently, at $B_{\mathrm{tot}}=10^6$, FQ consumes $1{,}984{,}280$ state preparations compared to $999{,}360$ for feature models. This further magnifies the practical hardware overhead of fidelity kernels.

---

## D. Representation and Symmetry Findings

### 1. Code Locations
- Density matrix routines: `src/kernels.py` Lines 18–48 (`one_rdm`), Lines 50–90 (`two_rdm`), Lines 209–238 (`pqk_gram_2local`).
- Classical feature maps: `src/kernels.py` Lines 310–337 (`classical_features` mode `"2pt_pauli_nn"`).
- Representation identity audit: `scripts/audit_representation_identity.py` Lines 72–170.

### 2. Analytical Symmetry Decomposition
Let $|\psi\rangle$ be a ground state of the 1D TFIM Hamiltonian $H = -J \sum Z_i Z_{i+1} - \sum h_i X_i$.

1. **Global Spin-Flip Parity $P = \prod_{k=1}^n X_k$:**
   - $P X_i P = X_i$, $P Y_i P = -Y_i$, $P Z_i P = -Z_i$.
   - Any operator odd under $P$ must vanish on parity eigenstates ($P|\psi\rangle = +|\psi\rangle$):
     * Single-site: $\langle Y_i \rangle = 0$, $\langle Z_i \rangle = 0$.
     * Two-site: $\langle X_i Y_j \rangle = 0$, $\langle Y_i X_j \rangle = 0$, $\langle X_i Z_j \rangle = 0$, $\langle Z_i X_j \rangle = 0$.
   - However, $P(Y_i Z_j)P = (-Y_i)(-Z_j) = + Y_i Z_j$ is **parity-even**. Parity does NOT enforce $\langle Y_i Z_j \rangle = 0$.

2. **Reality / Complex Conjugation $K$:**
   - In the standard computational $Z$-basis, $Z_i$ and $X_i$ are purely real matrices ($Z^* = Z, X^* = X$).
   - Since $J$ and $h_i$ are real, $H^* = H$, and the ground state wavefunction $|\psi\rangle$ is strictly real ($|\psi^*\rangle = |\psi\rangle$).
   - The Pauli operator $Y_i$ is purely imaginary ($Y^* = -Y$).
   - Therefore, $(Y_i Z_j)^* = (-Y_i) Z_j = - Y_i Z_j$.
   - For any real state $|\psi\rangle$, the expectation value of an anti-Hermitian or purely imaginary observable must vanish:
     $$\langle \psi | Y_i Z_j | \psi \rangle = \langle \psi^* | (Y_i Z_j)^* | \psi^* \rangle = -\langle \psi | Y_i Z_j | \psi \rangle \implies \langle Y_i Z_j \rangle = 0.$$
   - Likewise, $\langle Z_i Y_j \rangle = 0$.

3. **Physical Spin Time Reversal $\Theta$:**
   - Physical spin-1/2 time reversal is $\Theta = \left(\prod_k -i Y_k\right) K$.
   - Under $\Theta$, $\Theta X_i \Theta^{-1} = -X_i$, so the magnetic field term $-h_i X_i$ is odd.
   - Physical spin time reversal is **broken** by the transverse magnetic field. The vanishing of $\langle Y_i Z_j \rangle$ stems from Hamiltonian reality $K$, not physical time-reversal invariance $\Theta$.

### 3. Empirical Verification on Existing Saved States
- Data source: `results/validation/ground_state_validation.csv` (60 instances across $n \in \{4, 6, 8, 10, 12, 14\}$).
- State normalization residual: $|\|\psi\| - 1.0| \le 2.0 \times 10^{-16}$.
- Imaginary-amplitude residual: $\max |\text{Im}(\psi)| = 0.0$ (wavefunctions are exactly real).
- Parity residual: $|\langle P \rangle - 1.0| \le 4.44 \times 10^{-16}$.
- Hamiltonian eigenstate residual: $\|H\psi - E_0\psi\|_2 \le 7.79 \times 10^{-14}$.
- Vanishing expectation residuals: In `representation_reference_arrays.npz`, all 8 predicted vanishing expectations have absolute values $< 10^{-15}$.

### 4. Edge Sums and Multiplicity Weights
- In `src/kernels.py` (Line 327), `mode="2pt_pauli_nn"` iterates over the $n-1 = 7$ nearest-neighbor edges of the open chain.
- For an open chain, boundary sites $0$ and $n-1$ have degree 1 (appear in 1 edge), while interior sites $1..n-2$ have degree 2 (appear in 2 edges).
- The 35D vector in code stacks $[\langle X_i \rangle, \langle X_{i+1} \rangle, \langle X_i X_{i+1} \rangle, \langle Y_i Y_{i+1} \rangle, \langle Z_i Z_{i+1} \rangle]$.
- This repeats interior single-site terms twice, which is mathematically identical to a deduplicated 29D feature vector where single-site terms are weighted by $\sqrt{\text{deg}_i} = \sqrt{2}$.
- When scaled by $1/2$, the squared Euclidean distance matrix `D_prod_pqk2` matches the true 2-RDM Frobenius distance matrix `D_RDM` with maximum absolute error:
  $$\max |D_{\mathrm{RDM}} - D_{\mathrm{prod\_pqk2}}| = 1.332 \times 10^{-15}.$$
- Omitting the degree weighting (negative control `D_flawed`) produces a massive discrepancy of $0.5614$.
- Therefore, historical performance differences between `PQK-2nn` and `E2(raw)` in Task 1 were entirely an artifact of evaluating different heuristic bandwidth grids ($c/32$ for PQK vs $c/35$ for E2), rather than distinct physical representation geometry.

---

## E. Figure and Table Provenance

### 1. Figure 2 (`fig_shots.pdf`)
- **Generating Script:** `scripts/make_figures.py`, function `make_f5()` (Lines 438–544).
- **Source Data:** `results/t5_noise.csv`.
- **Filters:** `experiment == "finite_shots"` and `metric == "r2"`.
- **Evaluated Shot Tiers:** $S \in \{100, 1000, 10000\}$, plus $S = \infty$ reference.
- **Plot Structure:** Two panels:
  * Left: "Deployed Evaluation Cost" ($x = 720 \cdot S$ for features, $x = 8780 \cdot S$ for FQ).
  * Right: "Full-Gram Simulation Cost" ($x = 720 \cdot S$ for features, $x = 28680 \cdot S$ for FQ).
- **Line Styles & Markers:**
  * `FQ (clipped PSD)`: Solid `#D55E00`, marker `^`.
  * `FQ (raw, ill-defined)`: Dashed `#D55E00`, marker `x`.
  * `PQK-2nn`: Solid `#009E73`, marker `s`.
  * `PQK-1`: Solid `#0072B2`, marker `o`.
  * `E (raw)`: Solid `#E69F00`, marker `D`.
  * `E2 (raw)`: Solid `#CC79A7`, marker `v`.
  * `F (std)`: Dashed `#56B4E9`, marker `P`.
- **Y-Axis Limits:** Explicitly set to `[0.70, 1.01]` (Line 537).
- **Underlying Data Values vs Prose Claims:**
  * At $S=100$: `FQ-raw` achieved mean $R^2 = 0.7634$ (min 0.6719, max 0.8623). **Prose claim ($R^2 < 0$) is FALSE.**
  * At $S=1000$: `FQ-clipped` achieved mean $R^2 = 0.8693$ (min 0.5557, max 0.9427). **Prose claim ($R^2 > 0.98$) is FALSE.**

### 2. Table IV (`paper/tables/tab_equal_budget.tex`)
- Generated from `results/stage2/t1_equal_budget.csv`.
- Captures all 49 cells across 7 budget tiers and 7 model arms ($n=20$ seeds per cell).
- Formatting issue: Generates an **Overfull `\hbox` of 101.68 pt** in the LaTeX build log due to long multicolumn text and 9 table columns in a two-column float.

### 3. Table I (`paper/tables/tab1_t1_r2.tex`)
- Captures Task 1 test $R^2$ at $N_{\mathrm{tr}}=40$ and $N_{\mathrm{tr}}=160$.
- Formatting issue: Generates an **Overfull `\hbox` of 37.22 pt** in single-column format.

---

## F. Claims Requiring Qualification

The following specific statements in `paper/main.tex` require qualification or revision:

1. **Line 172 (Finite-Shot FQ Performance):**
   - *Current Text:* "Unmitigated SVR on indefinite Gram matrices suffered catastrophic degradation ($R^2 < 0$ at $S=100$). Eigenvalue thresholding (PSD clipping: $\lambda_i \leftarrow \max(\lambda_i, 0)$) successfully restored stability ($R^2 > 0.98$ at $S=1000$)."
   - *Issue:* Erroneous numbers contradicting `results/t5_noise.csv`.
   - *Recommended Revision:* "Unmitigated SVR on indefinite Gram matrices exhibited substantial performance degradation ($R^2 = 0.7634 \pm 0.0116$ at $S=100$). Eigenvalue thresholding (PSD clipping: $\lambda_i \leftarrow \max(\lambda_i, 0)$) improved stability ($R^2 = 0.8101 \pm 0.0093$ at $S=100$ and $0.8693 \pm 0.0210$ at $S=1000$), reaching $0.9630 \pm 0.0041$ at $S=10{,}000$."

2. **Line 188 (Equal-Budget Measurement Formulas):**
   - *Current Text:* "allocating $S_{\mathrm{feat}} = B_{\mathrm{tot}} / (M \cdot N_{\mathrm{tr}})$ shots per observable. In contrast, fidelity kernels require pairwise swap tests on $N_{\mathrm{tr}}(N_{\mathrm{tr}}-1)/2$ training pairs, allocating $S_{\mathrm{swap}} = B_{\mathrm{tot}} / (N_{\mathrm{tr}}(N_{\mathrm{tr}}-1)/2)$ shots per kernel entry (train-only mode)."
   - *Issue:* Formula denominators omit test states and confuse settings with observables.
   - *Recommended Revision:* "allocating $S_{\mathrm{feat}} = \lfloor B_{\mathrm{tot}} / (3 \cdot (N_{\mathrm{tr}} + N_{\mathrm{te}})) \rfloor$ shots per measurement setting across 3 global bases ($X, Y, Z$). In contrast, fidelity kernels require pairwise swap tests on all deployed pairs (training and test evaluation), allocating $S_{\mathrm{swap}} = \lfloor B_{\mathrm{tot}} / (\binom{N_{\mathrm{tr}}}{2} + N_{\mathrm{tr}} N_{\mathrm{te}}) \rfloor$ shots per pair."

3. **Lines 149 & 227 (Equivalence and Statistical Claims):**
   - *Current Text:* "FQ, E (raw), and PQK-2nn become statistically indistinguishable" and "achieve learning performance statistically indistinguishable from full fidelity quantum kernels".
   - *Issue:* Confuses failure to reject null ($p > 0.05$) with proof of equivalence.
   - *Recommended Revision:* "FQ, E (raw), and PQK-2nn exhibit sample-efficiency parity with no statistically significant difference detected under our pre-declared test protocol ($p_{\mathrm{Holm}} > 0.05$)."

4. **Line 155 (Claim C3 Asymptotic Claim):**
   - *Current Text:* "This confirmatory test (Claim C3) proves that for non-trivial 4-body correlators, classical RBF kernels on 2-body expectations attain identical asymptotic accuracy to full fidelity quantum kernels."
   - *Issue:* Finite-sample empirical evaluations at $N_{\mathrm{tr}}=160$ cannot "prove" "identical asymptotic accuracy".
   - *Recommended Revision:* "This confirmatory test (Claim C3) demonstrates that for non-trivial 4-body correlators, classical RBF kernels on 2-body expectations attain empirical accuracy comparable to full fidelity quantum kernels at $N_{\mathrm{tr}}=160$."

5. **Line 198 (Pre-Declaration Status of Stage 3):**
   - *Current Text:* "within the pre-declared three-comparison family including Train-Mean and Train-Median baselines"
   - *Issue:* Stage 3 was conducted retrospectively; prospective timing was not established in the initial pre-registration.
   - *Recommended Revision:* "within the retrospective three-comparison family declared prior to multi-test correction"

6. **Lines 196 & 198 (Phase Transition Nomenclature):**
   - *Current Text:* "paramagnetic regime ($h_i \in [0.8, 1.5]$)" and "ferromagnetic regime ($h_i \in [0.2, 0.7]$)"
   - *Issue:* No physical order parameter or correlation length was calculated to certify phase identity.
   - *Recommended Revision:* "higher-field regime ($h_i \in [0.8, 1.5]$, nominally paramagnetic)" and "lower-field regime ($h_i \in [0.2, 0.7]$, nominally ferromagnetic)"

---

## G. Rerun Decision Matrix

| Audit Topic | Computational Artifact Status | Discrepancy Location | Is Code/Experiment Rerun Required? | Justification & Safe Action |
|---|---|---|:---:|---|
| **Audit 1: Budget Accounting** | Correct & Validated | Manuscript Line 188 text only | **NO** | Raw CSV (`results/stage2/t1_equal_budget.csv`) and Table IV are 100% synchronized. Only the prose formula in `paper/main.tex` needs alignment. |
| **Audit 2: Representation Identity** | Correct & Validated | Section II-B text only | **NO** | Reference arrays prove $|D^2_{\mathrm{RDM}} - D^2_{\mathrm{Pauli}}| \le 1.33 \times 10^{-15}$. Physics clarification on $K$ vs $P$ is purely narrative. |
| **Audit 3: PSD Repair & Solvers** | Correct & Validated | None | **NO** | Implementation in `ablation_r3_repairs.py` and `noise.py` is sound and preserves test independence. |
| **Audit 4: Figure 2 Reconciliation** | Correct & Validated | Manuscript Line 172 text only | **NO** | `results/t5_noise.csv` and `fig_shots.pdf` are correct. Only the prose claim in Line 172 was erroneous. |
| **Audit 5: Statistical Claims** | Correct & Validated | Narrative wording | **NO** | Raw seed data in `t1_entropy_gridv3.csv` is intact. Revisions require only tempering prose from "proves"/"indistinguishable" to precise empirical statements. |
| **Audit 6: Stage 3 OOD Benchmarks** | Correct & Validated | Scope documentation | **NO** | Evaluating all-pairs $E(\text{raw})$ on OOD is outside the frozen Stage 3 protocol. Transparently documenting the omission in Section III-F is fully sufficient. |
| **Table Layout Overfull `\hbox`** | Layout Flaw | Table LaTeX macros | **NO** | Resolving overfull `\hbox` requires adjusting `\tabcolsep` and table font sizes, not rerunning simulations. |

---

## H. Git Status Before and After

### Initial State (Before Audit):
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
**Diff Stat:**
```
paper/main.tex       | 57 +++++++++++++++++++++++++++++++++++++---------------
paper/references.bib | 22 ++++++++++++++++++++
2 files changed, 63 insertions(+), 16 deletions(-)
```

### Final State (After Audit):
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
**Diff Stat:**
```
paper/main.tex       | 57 +++++++++++++++++++++++++++++++++++++---------------
paper/references.bib | 22 ++++++++++++++++++++
2 files changed, 63 insertions(+), 16 deletions(-)
```

### Invariance Verification:
- **Modified Tracked Files:** Exactly 0 additional files were modified.
- **Raw Data Files:** `results/*.csv` verified 100% bit-for-bit unchanged.
- **Source Files:** `src/*.py`, `scripts/*.py`, and `paper/main.tex` were strictly untouched during this read-only audit.
- **Generated Diagnostic Artifacts:** All output strictly confined to `docs/stage5/reviewer_flaw_audit_20261025_055950Z/`.
