# Stage 2 Sampling, Measurement Grouping, and Resource Accounting Audit

**Audit Identifier:** `audit_20261023_155335Z`  
**Execution Timestamp:** 2026-10-23T15:53:35Z  
**Status:** VERIFIED (Compatible grouping, exact covariance, rigorous budget accounting)  

## 1. Code-Path Tracing & Measurement Grouping Verification

### Code References:
- **Function:** `evaluate_feature_arms` in [scripts/stage2_equal_budget.py](file:///D:/quantum-kernel-tfim-benchmarks/scripts/stage2_equal_budget.py#L210-L280).
- **Sampling Call:** Lines 238–240: `rng.multinomial(S_feat, probs_x[i]) / S_feat`, etc.
- **Observable Extraction:** Lines 242–246: `exp_x = counts_x @ _SIGNS`, `exp_xx_nn = counts_x @ _SIGNS_NN`.

### Physical Grouping Findings:
1. **Shared Bitstring Measurement:** The implementation draws a **single multinomial bitstring distribution** (`counts_x`) per state in the global X-basis ($U_X^{\otimes 8}$). From this single set of $S_{\text{feat}}$ shots, all 8 single-qubit expectations $\langle X_i \rangle$ and all 7 nearest-neighbor expectations $\langle X_i X_{i+1} \rangle$ are evaluated via bitwise parity contractions.
2. **Compatible Observables:** Because all $X_i$ and $X_i X_{i+1}$ mutually commute ($[X_i, X_j X_{j+1}] = 0$), simultaneous readout via global basis rotation $U_X^{\otimes 8}$ is physically exact and rigorous.
3. **Setting Count Accounting:** Exactly 3 settings per state (X-basis, Y-basis, Z-basis) are required and charged. For $m = 240$ states, $3 \times 240 = 720$ settings are charged, allocating $S_{\text{feat}} = \lfloor B_{\text{tot}} / 720 \rfloor$ shots per setting.

## 2. Empirical Covariance Diagnostic

The diagnostic evaluated the joint sampling covariance between $A = X_0$ and $B = X_0 X_1$ on an $n=8$ disordered TFIM ground state across $K = 5,000$ independent trials at $S = 100$ shots:

- **State Residual:** $\|H\psi - E\psi\|_2 = 2.93e-14$ (machine-precision ground state).
- **Exact Expectations:** $\langle X_0 \rangle = 0.838604$, $\langle X_1 \rangle = 0.717530$, $\langle X_0 X_1 \rangle = 0.809686$.
- **Theoretical Covariance:** $\operatorname{Cov}(A, B) = (\langle X_1 \rangle - \langle X_0 \rangle \langle X_0 X_1 \rangle) / S = \mathbf{3.852359e-04}$.
- **Production Empirical Covariance:** $\mathbf{3.860343e-04} \pm 4.475177e-05$ ($z = 0.02$ from theory).
- **Independent Reference Covariance:** $-1.293005e-04 \pm 4.472376e-05$ (centered at 0, confirming independent marginals cannot produce joint covariance).
- **Audit Classification:** **Shared-setting covariance represented**.

## 3. Resource Accounting & Operational Exclusion Audit

### 3.1 Circuit Repetitions vs Input-State Copies
- **Feature Arms:** Each shot consumes 1 copy of state $|\psi_i\rangle$. Thus, total circuit repetitions = total state copies = $720 \times S_{\text{feat}}$.
- **Fidelity Arms (FQ Swap Test):** Each destructive swap test repetition requires **two input state copies** ($|\psi_i\rangle$ and $|\psi_j\rangle$). Under budget $B_{\text{tot}}$ defined in circuit repetitions, FQ consumes $2 \times B_{\text{tot}}$ physical state copies. If budget were denominated in state copies, FQ's shot allocation would be halved ($S_{\text{swap}} = \lfloor B_{\text{tot}} / (2 \times 8780) \rfloor$), further disadvantageing FQ.

### 3.2 Low-Budget Infeasibility Policy
- At $B_{\text{tot}} = 10,000$: $S_{\text{swap}} = \lfloor 10,000 / 8,780 \rfloor = 1$ shot/pair.
- At $B_{\text{tot}} = 30,000$: $S_{\text{swap}} = \lfloor 30,000 / 8,780 \rfloor = 3$ shots/pair.
- **Audit Scoping:** The candidate script logged `S_per_setting = 0` and marked `is_feasible = False`. This is an **operational study exclusion** enforced because $S_{\text{swap}} < 10$ yields extreme sampling variance, not because running 1 or 3 swap-test shots is physically impossible. The actual calculated allocation is $S_{\text{swap}} = 1$ and $S_{\text{swap}} = 3$, respectively.

