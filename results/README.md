# Results Data Directory Documentation

This directory contains empirical benchmark data, pre-registered statistical analyses, and summary metrics for the quantum kernel and classical correlator evaluation suite on transverse-field Ising model (TFIM) ground states.

---

## Benchmark Data Files

### 1. `t1_entropy_gridv3.csv`
- **Task:** Task 1 half-chain entanglement entropy regression ($S_{n/2}$).
- **System:** Open-boundary 1D TFIM, $n=8$ qubits, critical regime ($h_c = 1.0$).
- **Hyperparameter Grid:** `grid_v3` (SVR $\epsilon$-tuning: $\epsilon \in \{0.1, 0.03, 0.01, 0.003, 0.001\}$, $C \in \text{logspace}(-2, 4, 7)$, $c \in \text{logspace}(-2, 2, 9)$ or scaled).
- **Training Sizes:** $N_{\text{tr}} \in \{10, 20, 40, 80, 160\}$ across 20 fixed seeds ($N_{\text{te}} = 200$).
- **Columns:**
  - `seed`: Integer RNG seed (0–19).
  - `N_train`: Training partition size.
  - `model`: Evaluated arm (`PQK-1 (== RBF on <X>)`, `PQK-2nn`, `FQ`, `E`, `E2`, `F`, `E_X`).
  - `variant`: Preprocessing variant (`none`, `raw`, `std`).
  - `metric`: Evaluated metric (`r2`, `mae`).
  - `value`: Test partition metric value.
  - `best_params`: JSON-serialized dictionary of optimal inner-CV hyperparameters.

### 2. `t2_correlators_gridv3.csv`
- **Task:** Task 2 spin correlator regression.
  - T2a: 2-point end-to-end correlator $\langle Z_0 Z_{n-1} \rangle$ (contained control).
  - T2b: 4-point correlator $\langle Z_0 Z_1 Z_{n-2} Z_{n-1} \rangle$ (non-contained target).
- **System:** Open-boundary 1D TFIM, $n=8$, $N_{\text{tr}} \in \{10, 20, 40, 80, 160\}$, 20 seeds.
- **Hyperparameter Grid:** `grid_v3`.
- **Columns:** Same schema as `t1_entropy_gridv3.csv` with additional `target` column (`z0_zn_minus_1` vs `z0_z1_zn2_zn1`).

### 3. `t3_concentration_v2.csv` & `t3_n14_fraction.csv`
- **Task:** Task 3 kernel concentration and off-diagonal scaling across qubit counts $n \in \{4, 6, 8, 10, 12, 14\}$.
- **Ensemble:** Disordered 1D TFIM ($h_i \sim \text{Uniform}(0.5, 1.5)$, 30 states per seed, 20 seeds).
- **Kernels:** FQ, PQK-1 ($\gamma=1.0, 1.0/n$), PQK-2nn ($\gamma=1.0, 1.0/n$).
- **Columns in `t3_concentration_v2.csv`:**
  - `seed`, `n`, `kernel`, `gamma_rule`, `off_diag_mean`, `off_diag_var`.
- **Columns in `t3_n14_fraction.csv`:**
  - `kernel`, `gamma_rule`, `n`, `n_pairs`, `n_below`, `fraction`, `min_entry`.

### 4. `t4_v2_gridv3.csv` & `t4_frustrated.csv`
- **Task:** Task 4 2D frustrated $J_1$-$J_2$ lattice ground states ($2 \times 4$ and $3 \times 4$).
  - T4a: Frustrated phase classification across $J_2/J_1$ boundaries (evaluated on `grid_v2`).
  - T4b: Frustrated ground-state energy regression (evaluated on `grid_v3`).
- **Columns:** `seed`, `lattice`, `target`, `N_train`, `model`, `variant`, `metric`, `value`, `best_params`.

### 5. `t5_noise.csv`
- **Task:** Task 5 measurement shot noise and physical local depolarizing channel sweeps on Task 1 ($n=8$, $N_{\text{tr}}=40$, $N_{\text{te}}=200$, 20 seeds).
- **Experiments:**
  - `finite_shots`: Destructive swap-test sampling ($S \in \{100, 1000, 10000, \infty\}$) with PSD eigenvalue thresholding (`FQ-raw` vs `FQ-clipped`).
  - `depolarizing`: Local per-qubit depolarizing channel $\mathcal{E}(\rho) = (1-p)\rho + p(I/2)$ for $p \in \{0.00, 0.01, 0.02, 0.04, 0.06, 0.08\}$ with hyperparameters retuned by inner-CV at each $p$.
- **Columns:** `experiment`, `seed`, `noise_level`, `model`, `variant`, `metric`, `value`, `best_params`, `total_shots`, `lam_min`.

### 6. `t5_depol_fixedhp.csv`
- **Task:** Unmitigated physical depolarizing control where hyperparameters $(C, c, \epsilon)$ are fixed to the noiseless ($p=0.00$) optimum.
- **Columns:** `seed`, `p`, `model`, `variant`, `r2`, `mae`, `hp_source`.

### 7. `stats.csv`
- **Task:** Pre-registered confirmatory and exploratory paired statistical tests across all benchmark cells.
- **Correction:** Two-tiered Holm correction (`p_holm_perN` as primary tier, `p_holm_family` as sensitivity tier).
- **Columns:**
  - `task`, `target`, `lattice`, `N_train`, `metric`, `model_a`, `model_b`, `tier`, `n_pairs`, `n_zeros_dropped`, `mean_diff`, `ci_low`, `ci_high`, `W_plus`, `W_minus`, `p_raw`, `p_holm_perN`, `p_holm_family`, `effect_size` (rank-biserial $r$), `flag`.

### 8. `grid_boundary_post_v3.csv`
- **Task:** Search grid boundary audit identifying configurations where $> 50\%$ of seeds selected hyperparameter values at lower or upper search limits.
- **Columns:** `task`, `target`, `model`, `variant`, `N_train`, `boundary_type`, `hit_pct`.
