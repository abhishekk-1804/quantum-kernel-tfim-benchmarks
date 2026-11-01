# STAGE 3 PROTOCOL: Controlled Out-of-Distribution (OOD) Phase-Shift Generalization

**Statistical Classification:** CONFIRMATORY (Stage 3 Frozen Protocol)  
**Task Designation:** Task 6: Out-of-Distribution Phase-Shift Generalization  
**Physical System:** Disordered 1D Transverse-Field Ising Model ($n = 8$ spins, open boundary conditions)  
**Target Observable:** Half-chain bipartite entanglement entropy $S_{n/2}(\psi)$ across cut at $n/2 = 4$  

---

## 1. Physical Formulation & Phase Diagram

The transverse-field Ising model (TFIM) on an open 1D chain of $n$ qubits is governed by the Hamiltonian:
$$H = -\sum_{i=0}^{n-2} J_{i, i+1} Z_i Z_{i+1} - \sum_{i=0}^{n-1} h_i X_i$$
with disordered ferromagnetic exchange couplings $J_{i, i+1} \sim \mathcal{U}(0.5, 1.5)$ and disordered transverse fields $h_i > 0$.

In the clean limit ($J_{i, i+1} = J = 1.0$, $h_i = h$), the model exhibits a continuous quantum phase transition at critical field $h_c = 1.0$:
- **Paramagnetic / Disordered Phase ($h > 1.0$):** Transverse alignment dominates along the $X$-axis ($\langle X_i \rangle \to 1$), while longitudinal two-point correlations decay exponentially ($\langle Z_i Z_j \rangle \to 0$ for $|i - j| \gg 1$). The ground state is non-degenerate and symmetric.
- **Ferromagnetic / Ordered Phase ($h < 1.0$):** Longitudinal exchange dominates along the $Z$-axis, generating spontaneous $\mathbb{Z}_2$ symmetry breaking in the thermodynamic limit. In finite systems with open boundaries, ground states in the even-parity sector exhibit macroscopic longitudinal correlations ($\langle Z_i Z_j \rangle \approx 1$) and suppressed transverse polarization.
- **Critical Point ($h = 1.0$):** Entanglement entropy diverges logarithmically with subsystem size ($S_{L} \sim \frac{c}{6} \log_2 L$).

In the disordered model, the transition broadens into an infinite-randomness critical regime.

---

## 2. Controlled Domain Partitions

To test out-of-distribution generalization across the macroscopic phase boundary, the data distribution is partitioned into three non-overlapping domains:

1. **Training Domain ($D_{\text{train}}$ — Paramagnetic & Critical Regime):**
   - Transverse fields: $h_i \sim \mathcal{U}(0.8, 1.5)$ for $i \in \{0, \dots, n-1\}$.
   - Sample size: $N_{\text{train}} = 40$ ground states per seed.
   - Purpose: Train models strictly in the paramagnetic and critical crossover regime.

2. **In-Distribution Test Domain ($D_{\text{test,ID}}$):**
   - Transverse fields: $h_i \sim \mathcal{U}(0.8, 1.5)$ for $i \in \{0, \dots, n-1\}$ (sampled independently from $D_{\text{train}}$).
   - Sample size: $N_{\text{test,ID}} = 100$ ground states per seed.
   - Purpose: Quantify standard in-distribution generalization performance.

3. **Out-of-Distribution Test Domain ($D_{\text{test,OOD}}$ — Deep Ferromagnetic Regime):**
   - Transverse fields: $h_i \sim \mathcal{U}(0.2, 0.7)$ for $i \in \{0, \dots, n-1\}$.
   - Sample size: $N_{\text{test,OOD}} = 100$ ground states per seed.
   - Domain shift: Shifted entirely across the critical threshold into the strongly ordered phase ($h_i < 0.7 \ll 1.0$).
   - Purpose: Stress-test whether full-state quantum fidelity or low-order local correlator kernels generalize across macroscopic ground-state structural reorganization.

All states satisfy:
- Parity projection: Even parity sector $\langle \psi | P | \psi \rangle = +1$ where $P = \bigotimes_{i=0}^{n-1} X_i$.
- Ground-state convergence: Eigenpair residual $\|H|\psi\rangle - E|\psi\rangle\|_2 < 10^{-10}$.

---

## 3. Target Observable & Representation Spaces

### 3.1 Target Observable
Half-chain bipartite entanglement entropy $S_{n/2}(\psi)$ computed via exact partial trace over spins $A = \{0, 1, 2, 3\}$ ($n/2 = 4$):
$$\rho_A = \operatorname{Tr}_B(|\psi\rangle \langle\psi|), \quad S_{n/2}(\psi) = -\sum_k \lambda_k \log_2 \lambda_k$$
where $\lambda_k$ are the eigenvalues of $\rho_A$.

### 3.2 Model Architectures & Feature Spaces
1. **Fidelity Quantum Kernel (`FQ`):**
   - Gram matrix elements: $K_{ij} = |\langle \psi_i | \psi_j \rangle|^2$.
   - SVR with precomputed kernel.
   - Hyperparameter grid: $C \in \{0.1, 1, 10, 100, 1000\}$, $\epsilon \in \{0.01, 0.05, 0.1, 0.2\}$.

2. **1-local Projected Quantum Kernel (`PQK-1`):**
   - Single-site expectation vector: $x_i = \langle X_i \rangle$ ($d = 8$).
   - Bandwidth: $\gamma = c / n$ with $n = 8$.
   - Hyperparameter grid: $C \in \{0.1, 1, 10, 100, 1000\}$, $c \in \{0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0\}$, $\epsilon \in \{0.01, 0.05, 0.1, 0.2\}$.

3. **2-local Nearest-Neighbor Projected Quantum Kernel (`PQK-2nn`):**
   - Two-site reduced density matrices $\rho_{i, i+1}$ for nearest-neighbor bonds $i \in \{0, \dots, n-2\}$.
   - Feature representation: $X_{\text{pqk2}} = X_{e2} / 2.0$ ($d = 35$).
   - Bandwidth: $\gamma = c / n$ with $n = 8$.
   - Metric: Frobenius distance over 2-RDMs.

4. **Classical 2-Point Correlators (`E2 (4n)`):**
   - 35-dimensional feature representation with 5 non-zero Pauli coefficients per bond:
     $$[\langle X_i \rangle, \langle X_{i+1} \rangle, \langle X_i X_{i+1} \rangle, \langle Y_i Y_{i+1} \rangle, \langle Z_i Z_{i+1} \rangle]$$
   - Bandwidth: $\gamma = c / (4n) = c / 32.0$.
   - Theoretical equivalence: By construction, $\|X_{e2} / 2.0 - X'_{e2} / 2.0\|^2 / n = \|X_{e2} - X'_{e2}\|^2 / (4n)$, identically proving $B == C$.

5. **Linear Ridge Regression (`Linear_Ridge`):**
   - Standardized 35-dimensional E2 features (standard scaler fitted strictly on $D_{\text{train}}$).
   - Regularization grid: $\alpha \in \{10^{-4}, 10^{-3}, 10^{-2}, 10^{-1}, 1, 10, 100\}$.
   - Serves as the pure linear baseline to determine whether non-linear kernel warping is necessary for OOD transfer.

---

## 4. Hyperparameter Selection & Validation Protocol

- **Strict Leakage Prevention:**
  - Standard scaling parameters ($\mu, \sigma$) and target standardization parameters ($y_{\text{mean}}, y_{\text{std}}$) are computed exclusively on $D_{\text{train}}$.
  - Model hyperparameters ($C, c, \epsilon, \alpha$) are selected via inner 3-fold cross validation strictly within $D_{\text{train}}$ ($N_{\text{train}} = 40$).
  - Neither $D_{\text{test,ID}}$ nor $D_{\text{test,OOD}}$ is ever exposed during training or hyperparameter selection.
- **Evaluation Metrics:**
  - $R^2_{\text{ID}}$ and $\text{MAE}_{\text{ID}}$ on $D_{\text{test,ID}}$ ($N_{\text{test,ID}} = 100$).
  - $R^2_{\text{OOD}}$ and $\text{MAE}_{\text{OOD}}$ on $D_{\text{test,OOD}}$ ($N_{\text{test,OOD}} = 100$).
  - Generalization Drop: $\Delta_{\text{OOD}} R^2 = R^2_{\text{ID}} - R^2_{\text{OOD}}$.

---

## 5. Statistical Hypotheses & Pre-Declared Comparisons

1. **Full-State vs Local Quantum Advantage:**
   - Null: $\mathbb{E}[R^2_{\text{OOD}}(\text{FQ})] \le \mathbb{E}[R^2_{\text{OOD}}(\text{PQK-2nn})]$.
   - Alternative: Fidelity quantum kernel retains global state information that enhances transfer across the phase transition.
2. **PQK-2nn vs Classical Correlators (Equivalence under Shift):**
   - Verification that $R^2_{\text{OOD}}(\text{PQK-2nn}) = R^2_{\text{OOD}}(\text{E2 (4n)})$ holds up to floating-point precision on out-of-distribution states.
3. **Non-linear Kernel Warping vs Linear Correlator Baseline:**
   - Null: $\mathbb{E}[R^2_{\text{OOD}}(\text{PQK-2nn})] \le \mathbb{E}[R^2_{\text{OOD}}(\text{Linear\_Ridge})]$.
   - Assesses whether non-linear RBF kernel warping on 2-RDMs maintains predictive utility under distribution shift over a linear correlator model.

---

## 6. Execution Parameters
- Seeds: 20 seeds ($0, 1, \dots, 19$).
- Resumability: Append-and-flush per seed block into `results/stage3/t6_ood_shift.csv`.
- Pre-flight runtime budget: $\le 1.5$ hours (5,400 seconds) across all 20 seeds.
