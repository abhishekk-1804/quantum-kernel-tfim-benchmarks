# Open Questions and Issues Register

This register documents methodological edge cases, technical discrepancies, open questions, and audit findings across the benchmark suite.

---

### R1: Discrepancy between PQK-2nn and E2 (raw) in Task 1 at $N=40$
- **ID:** R1
- **Statement:** PQK-2nn and E2 (raw) exhibit non-identical test $R^2$ performance in Task 1 at $N_{\text{tr}}=40$ ($R^2 = 0.9803$ vs $0.9799$ on seed 0; mean $R^2 = 0.9789$ vs $0.9786$), even though both models consume identical two-body Pauli correlator features (`classical_features(mode="2pt_pauli_nn")`). Working hypothesis: the difference originates from the bandwidth grid formulation, where PQK-2nn searches over $\gamma = c / (4n)$ while E2 (raw) searches over $\gamma = c / d_{\text{E2}}$ where $d_{\text{E2}} = 5(n-1) = 35 \neq 4n = 32$.
- **Source:** `results/t1_entropy_gridv3.csv` and `scripts/common.py` (lines 373, 405-415).
- **Status:** reported
- **Owner:** WP-3 (Statistics & Baselines) / WP-2 (Theory)
- **How to check:** Run an ablation executing E2 with PQK-2nn's exact gamma grid ($\gamma = c / (4n)$) on Task 1 ($N_{\text{tr}}=40$, 20 seeds) into a NEW versioned file (e.g., `results/ablations/t1_e2_pqkgrid.csv`); do NOT modify or overwrite existing CSV records.
- **Stage 1 observations:**
  - Evaluated in `scripts/ablation_r1_e2_grid.py` -> `results/ablations/t1_e2_pqkgrid.csv`.
  - Max |Arm A - Reference E2|: 1.11e-16 (tolerance: 1e-10) -> PASS.
  - Max |Arm C - Reference PQK-2nn|: 1.11e-16 (tolerance: 1e-10) -> PASS.
  - Max |B - C| R2 across evaluated seeds: 0.00e+00.
  - Max |B - C| MAE across evaluated seeds: 0.00e+00.
  - Number of evaluated seeds with identical best_params: 20 / 20.
  - Observation: When evaluated on identical gamma grid c/(4n), E2 (raw) and PQK-2nn produce bit-for-bit identical test performance and hyperparameter selections across all 20 seeds.
- **Stage 1b observations:**
  - Resolved by ablation: `results/ablations/t1_e2_pqkgrid.csv` confirms $B == C$ ($|\Delta R^2| = 0.00 \times 10^0$). The discrepancy reported in R1 between PQK-2nn and E2 (raw) is solely an artifact of the normalizer grid parameterization ($4n=32$ vs $5(n-1)=35$), not of the underlying physical representations. Status field unchanged per protocol.

---

### R2: Extra Basis Measurement in Noisy PQK-1 Arm
- **ID:** R2
- **Statement:** The noisy finite-shot implementation of PQK-1 in `scripts/run_t5_noise.py` allocates shots to both Basis X and Basis Z ($2 \times m \times S$ total shots), measuring $\langle X_i \rangle$ and $\langle Z_i \rangle$, whereas the noiseless PQK-1 identity proves that $k_{\text{PQK-1}}$ depends purely on single-site magnetization $\langle X_i \rangle$ because $\langle Z_i \rangle \equiv 0$ in the $Z_2$-even parity ground-state sector.
- **Source:** `scripts/run_t5_noise.py` (lines 454-455, 498-500) and `src/kernels.py` (lines 60-70).
- **Status:** reported
- **Owner:** WP-4 (Measurement) / WP-1 (Lead)
- **How to check:** Compare test $R^2$ of noisy PQK-1 using $[X_i, Z_i] / \sqrt{2}$ versus $[X_i]$ alone under finite shots $S$; verify whether shot noise in the null observable $\langle Z_i \rangle$ degrades SVR performance relative to an exact single-basis $X$ measurement allocation ($m \times S$ shots).
- **Stage 1 observations:**
  - Evaluated in `scripts/ablation_r2_pqk1_basis.py` -> `results/ablations/t5_pqk1_basis.csv`.
  - Max |PQK-1(X+Z) - Reference t5_noise.csv|: 1.11e-16 (tolerance: 1e-10) -> PASS.
  - Paired bootstrap analysis: [PQK-1 (X-only)] - [PQK-1 (X+Z)] (R2) across 20 seeds (10,000 resamples, seed 20261023, exploratory):
    - S = 100: Mean R2 (X+Z) = 0.7374, Mean R2 (X-only) = 0.7582, Mean Diff = +0.0208, 95% CI [-0.0003, +0.0436]
    - S = 300: Mean R2 (X+Z) = 0.8300, Mean R2 (X-only) = 0.8301, Mean Diff = +0.0001, 95% CI [-0.0365, +0.0256]
    - S = 1000: Mean R2 (X+Z) = 0.8717, Mean R2 (X-only) = 0.8764, Mean Diff = +0.0048, 95% CI [-0.0048, +0.0147]
    - S = 3000: Mean R2 (X+Z) = 0.8933, Mean R2 (X-only) = 0.8919, Mean Diff = -0.0014, 95% CI [-0.0135, +0.0093]
    - S = 10000: Mean R2 (X+Z) = 0.9036, Mean R2 (X-only) = 0.9027, Mean Diff = -0.0009, 95% CI [-0.0078, +0.0056]
  - Observation: At low shot budgets ($S=100$), dedicating all shots to basis $X$ yields $+0.0208$ higher mean $R^2$ than splitting shots across $X$ and null observable $Z$. At high shot budgets ($S \ge 1000$), the performance difference between $X$-only and $X+Z$ protocols is negligible ($|\Delta R^2| \le 0.005$). Status remains 'reported'.

---

### R3: Asymmetric Spectral Clipping of Test-Train Kernel Block in FQ-Clipped
- **ID:** R3
- **Statement:** In `scripts/run_t5_noise.py`, `evaluate_svr_precomputed(..., clip_psd=True)` performs eigenvalue clipping ($\lambda_i \leftarrow \max(\lambda_i, 0)$) exclusively on the square $N_{\text{tr}} \times N_{\text{tr}}$ training Gram matrix ($K_{\text{fit\_tr}}$ and $K_{\text{fold\_tr}}$). The rectangular $N_{\text{te}} \times N_{\text{tr}}$ test-train kernel block ($K_{\text{te}}$) and the validation-fold blocks ($K_{\text{fold\_val}}$) are passed to `SVR.predict()` completely unrepaired and unclipped.
- **Source:** `scripts/run_t5_noise.py` (lines 190-217).
- **Status:** reported
- **Owner:** WP-4 (Measurement)
- **How to check:** Inspect SVR dual decision function $f(x) = \sum_i \alpha_i K(x, x_i) + b$. Since the test prediction uses $K_{\text{te}} \alpha$, determine whether projecting the full $(N_{\text{tr}} + N_{\text{te}}) \times (N_{\text{tr}} + N_{\text{te}})$ joint Gram matrix onto the positive semidefinite cone alters out-of-sample $R^2$ stability.
- **Stage 1 observations:**
  - Evaluated in `scripts/audit_r3_probe.py` -> `docs/stage1/r3_clipping_paths.md`.
  - Static grep confirms `fidelity_clip_psd` is applied exclusively to the square training Gram blocks (`K_fit_tr` and `K_fold_tr`) in `scripts/run_t5_noise.py` (lines 193, 214). Test-train block `K_te` is passed unclipped.
  - Numerical sensitivity probe (5 seeds, S=1000):
    - Seed 0: R2(a)=0.9115, R2(b)=0.9637, Delta=+0.0522
    - Seed 1: R2(a)=0.9284, R2(b)=0.9653, Delta=+0.0370
    - Seed 2: R2(a)=0.9243, R2(b)=0.9575, Delta=+0.0333
    - Seed 3: R2(a)=0.4839, R2(b)=0.9590, Delta=+0.4752
    - Seed 4: R2(a)=0.8316, R2(b)=0.9591, Delta=+0.1275
    - Mean: R2(a)=0.8160, R2(b)=0.9609, Mean Delta=+0.1450.
  - Observation: Joint clipping eliminates catastrophic out-of-sample degradation observed in seed 3 under train-only clipping. Sliced train submatrix from PSD joint Gram is guaranteed PSD by Cauchy interlacing.
- **Stage 1b observations:**
  - Evaluated in `scripts/ablation_r3_experiment.py` -> `results/ablations/t5_fq_repairs.csv` (20 seeds, 5 shot budgets, 4 arms, labeled exploratory).
  - Bit-for-bit reproduction of `results/t5_noise.csv`: `train_only` vs `FQ-clipped` max diff $= 1.11 \times 10^{-16}$; `none` vs `FQ-raw` max diff $= 1.11 \times 10^{-16}$.
  - Mean $R^2$ (failures $R^2 < 0.7$):
    - $S=100$: none $= 0.7634$ (fail: 2), train_only $= 0.8101$ (fail: 0), inductive $= 0.7621$ (fail: 3), joint $= 0.8814$ (fail: 0)
    - $S=300$: none $= 0.8622$ (fail: 0), train_only $= 0.8783$ (fail: 0), inductive $= 0.8437$ (fail: 2), joint $= 0.9330$ (fail: 0)
    - $S=1000$: none $= 0.8894$ (fail: 0), train_only $= 0.8693$ (fail: 2), inductive $= 0.8916$ (fail: 1), joint $= 0.9569$ (fail: 0)
    - $S=3000$: none $= 0.8704$ (fail: 1), train_only $= 0.9044$ (fail: 0), inductive $= 0.9537$ (fail: 0), joint $= 0.9740$ (fail: 0)
    - $S=10000$: none $= 0.8613$ (fail: 0), train_only $= 0.9630$ (fail: 0), inductive $= 0.9723$ (fail: 0), joint $= 0.9807$ (fail: 0)
  - Paired bootstrap 95% CIs (10,000 resamples, seed 20261023, exploratory):
    - Inductive vs Train-Only: $S=100$: $-0.0480$ $[-0.1464, +0.0132]$; $S=300$: $-0.0346$ $[-0.0670, -0.0067]$; $S=1000$: $+0.0223$ $[-0.0262, +0.0755]$; $S=3000$: $+0.0493$ $[+0.0366, +0.0623]$; $S=10000$: $+0.0093$ $[+0.0039, +0.0171]$.
    - Inductive vs None: $S=100$: $-0.0013$ $[-0.1029, +0.0615]$; $S=300$: $-0.0185$ $[-0.0540, +0.0114]$; $S=1000$: $+0.0022$ $[-0.0311, +0.0327]$; $S=3000$: $+0.0833$ $[+0.0452, +0.1336]$; $S=10000$: $+0.1110$ $[+0.0916, +0.1322]$.
    - Joint vs Inductive: $S=100$: $+0.1193$ $[+0.0576, +0.2193]$; $S=300$: $+0.0892$ $[+0.0576, +0.1261]$; $S=1000$: $+0.0653$ $[+0.0425, +0.0948]$; $S=3000$: $+0.0203$ $[+0.0145, +0.0269]$; $S=10000$: $+0.0084$ $[+0.0064, +0.0105]$.
  - Observation: At moderate-to-high shot counts ($S \ge 1000$), inductive repair significantly outpaces unclipped baseline ($+0.08$ to $+0.11$) and surpasses train-only clipping ($+0.01$ to $+0.05$) without transductive test-point leakage. Joint transductive clipping yields the highest overall accuracy across all budgets ($R^2 \ge 0.8814$). Status field unchanged ('reported').

---

### R4: Agent-Modified Files Outside the Workspace from Earlier Session
- **ID:** R4
- **Statement:** In an earlier execution session, IDE/agent configuration files outside the repository (`hooks.json` and `telemetry_hook.js`) were inspected/edited. These modifications are external to `D:\quantum-kernel-tfim-benchmarks`.
- **Source:** Previous agent session logs and telemetry audit notes.
- **Status:** unresolved
- **Owner:** WP-1 (Lead)
- **How to check:** Request explicit user review of external environment configuration; inspect external diffs and confirm that no external telemetry hooks or unauthorized IDE-level settings remain in an inconsistent state.

---

### R5: Verification of Manuscript Numerical Performance Bounds Against stats.csv
- **ID:** R5
- **Statement:** Draft manuscript text and summaries quote bounds such as $|\Delta R^2| \le 0.011$ at $N_{\text{tr}} \ge 80$ and $\approx 0.032$ at $N_{\text{tr}} = 40$ for confirmatory top-performing comparisons. These ranges need formal auditing against all 36 confirmatory rows in `results/stats.csv`.
- **Source:** `paper/main.tex` and `results/stats.csv`.
- **Status:** reported
- **Owner:** WP-3 (Statistics & Baselines)
- **How to check:** Audit verified against `results/stats.csv`:
  - At $N_{\text{tr}}=40$, the largest mean difference between FQ and E (raw) is $-0.0320$ (T4b $2 \times 4$ lattice).
  - At $N_{\text{tr}} \ge 80$, the maximum mean difference between FQ and E (raw) is $-0.0119$ (T4b $2 \times 4$ lattice at $N=80$) and $-0.0012$ (T1 chain at $N=160$); between PQK-2nn and E (raw) it is $-0.0044$ (T1 at $N=160$) and $-0.0017$ (T4b $2 \times 4$ at $N=80$).
  Confirm whether table entries and text narratives strictly align with rounded decimals.
- **Stage 1 observations:**
  - Evaluated in `scripts/audit_stats_claims.py` -> `analysis/stats_claims_check.csv` and `docs/stage1/stats_vs_manuscript.md`.
  - Confirmatory rows audited: all 36 rows in `results/stats.csv` printed.
  - Specifically tested bound "|Delta R^2| <= 0.011 at N >= 80":
    - Exceeded by T4b (2x4 lattice, N=80) FQ vs E (raw): mean_diff = -0.011928 (|diff| = 0.011928 > 0.011).
    - Exceeded in exploratory comparisons: T2a (chain, N=80) PQK-2nn vs E (raw) (mean_diff = -0.075433), T4a (2x4, N=80) PQK-2nn vs E (raw) (mean_diff = -0.012750).
  - Observation: Claim C2 in `paper/main.tex` stating "All differences between top performers remain small (<= 0.011 R^2)" is contradicted by the exact value in `results/stats.csv` (-0.011928). Status remains 'reported'.

---

### R6: Systematic Literature Matrix and Related Work Positioning
- **ID:** R6
- **Statement:** A formal structured literature matrix positioning this work relative to recent quantum kernel literature (e.g., Huang et al. 2021, Thanasilp et al. 2024, Shaydulin & Wild 2022, Kübler et al. 2021, Bowles et al. 2024) has not yet been authored in `docs/`.
- **Source:** Project roadmap and manuscript related-work audit.
- **Status:** unresolved
- **Owner:** WP-2 (Theory) / WP-1 (Lead)
- **How to check:** Author `docs/literature_matrix.md` compiling 10-15 key papers, contrasting their input data distribution (synthetic vs. Hamiltonian ground states), baseline choices (matched vs. unmatched), noise models (gate vs. measurement), and concentration analyses.

---

### R7: FQ-Clipped Numbers in t5_noise.csv Correspond to Train-Only Clipping
- **ID:** R7
- **Statement:** The `FQ-clipped` numbers in `results/t5_noise.csv` correspond to `train_only` clipping (where `fidelity_clip_psd` is applied exclusively to the training Gram block, leaving test kernel evaluations unprojected).
- **Source:** `scripts/run_t5_noise.py` (lines 190-220) and `scripts/ablation_r3_experiment.py`.
- **Status:** reported
- **Owner:** TBD
- **How to check:** S1b.2 experiment reproduces `FQ-clipped` to machine precision ($|\Delta R^2| \le 1.11 \times 10^{-16}$) using `repair_train_only`.
- **Stage 1b observations:**
  - Verified by exact reproduction in S1b.2 across evaluated seeds and shot levels.

---

### R8: Joint Clipping is Transductive
- **ID:** R8
- **Statement:** Joint clipping projects the full $(N_{\text{tr}} + N_{\text{te}}) \times (N_{\text{tr}} + N_{\text{te}})$ Gram matrix onto the PSD cone, which uses test-state information during training/repair. Deployability in practical production streaming inference remains unresolved.
- **Source:** `scripts/ablation_r3_repairs.py` and `tests/test_stage1b_repairs.py`.
- **Status:** reported
- **Owner:** TBD
- **How to check:** Unit test `test_joint_repair_transductive_property` in `tests/test_stage1b_repairs.py` proves altering an arbitrary test state changes the training Gram matrix by $\approx 6.22 \times 10^{-2}$.
- **Stage 1b observations:**
  - Evaluated in S1b.1 and S1b.2. Joint repair guarantees PSD Gram matrices by Cauchy interlacing, but creates a transductive information flow from unlabeled test points into the training block.

---

### R9: E2(raw) Duplicates PQK-2nn Feature Map
- **ID:** R9
- **Statement:** E2(raw) duplicates the PQK-2nn feature map (`classical_features(mode="2pt_pauli_nn")`); the benchmark grids differ only in the normalizer divisor ($4n=32$ vs $5(n-1)=35$).
- **Source:** `src/kernels.py`, `scripts/common.py`, and `results/ablations/t1_e2_pqkgrid.csv`.
- **Status:** reported
- **Owner:** TBD
- **How to check:** See R1 ablation `scripts/ablation_r1_e2_grid.py` -> `results/ablations/t1_e2_pqkgrid.csv` ($B == C$ bit-for-bit across all 20 seeds).
- **Stage 1b observations:**
  - Evaluated in Stage 1 and confirmed in Stage 1b. When given identical bandwidth grids, E2(raw) and PQK-2nn achieve identical CV scores, identical chosen hyperparameters, and identical test predictions ($|\Delta R^2| = 0.00 \times 10^0$).
