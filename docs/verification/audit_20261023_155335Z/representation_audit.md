# Forensic Representation Identity Audit: PQK-2nn vs Classical Correlators (E2)

**Audit Identifier:** `audit_20261023_155335Z`  
**Execution Timestamp:** 2026-10-23T15:53:35Z  
**Verdict:** `SUPPORTED WITHIN TESTED SCOPE` (Exact mathematical identity B == C proven and empirically verified)  

## 1. Production-Path Code Inspection

### Code Tracing in Stage 2 and Stage 3:
- **Feature Generation:** In both `scripts/stage2_equal_budget.py` and `scripts/stage3_ood_shift.py`, the 35-dimensional array `X_e2` is constructed from 5 Pauli expectation values per nearest-neighbor bond:
  `[<X_i>, <X_{i+1}>, <X_i X_{i+1}>, <Y_i Y_{i+1}>, <Z_i Z_{i+1}>]` for $i \in \{0, \dots, 6\}$.
- **Array Scaling:** `X_pqk2 = X_e2 / 2.0`.
- **Estimator Fitting:**
  * `PQK-2nn`: Fits SVR with `X_tr = X_pqk2`, `gamma_denom = float(n)` ($n = 8$).
  * `E2 (4n)`: Fits SVR with `X_tr = X_e2`, `gamma_denom = float(4 * n)` ($4n = 32$).
- **Independence Assessment:**
  * Do they share fitted estimator objects? **No**. Two separate SVR instances are instantiated and fitted.
  * Do they copy score values? **No**. Scores are evaluated independently on the two fitted models.
  * Do they use identical mathematical kernels? **Yes**. Because:
    $$\exp\left(-\frac{c}{n} \|X_{\text{pqk2}}^{(a)} - X_{\text{pqk2}}^{(b)}\|^2\right) = \exp\left(-\frac{c}{n} \frac{\|X_{e2}^{(a)} - X_{e2}^{(b)}\|^2}{4}\right) = \exp\left(-\frac{c}{4n} \|X_{e2}^{(a)} - X_{e2}^{(b)}\|^2\right)$$
    the Gram matrices fed into SVR optimization are **bit-for-bit identical**.

## 2. Independent Mathematical Reference & Verification

To test whether the 35-dimensional classical representation truly equals the quantum 2-RDM Frobenius kernel, an independent reference was constructed:
1. 10 diagnostic ground states were diagonalized covering both paramagnetic ($h \in [0.8, 1.5]$) and ferromagnetic ($h \in [0.2, 0.7]$) domains (all residual < 1e-10).
2. Edge 2-RDMs $\rho_{i, i+1}$ were computed directly via partial trace and verified for Hermiticity and unit trace.
3. The exact Frobenius distance matrix $D_{\mathrm{RDM}}[a, b] = \sum_e \|\rho_e^{(a)} - \rho_e^{(b)}\|_F^2$ was computed directly on the density matrices.
4. A deduplicated Pauli feature map with $\sqrt{\mathrm{degree}}$ single-site weighting was constructed independently.

### Distance Matrix Comparison Results:

| Comparison | Max Absolute Error | Max Relative Error | Tolerance | Status |
| :--- | :---: | :---: | :---: | :---: |
| D_RDM vs D_reference (Deduplicated Pauli with sqrt(deg)) | `1.33e-15` | `7.96e-16` | `1e-12` | **PASS (Exact algebraic equivalence confirmed)** |
| D_RDM vs D_prod_pqk2 (Production X_e2 / 2.0) | `1.33e-15` | `5.74e-16` | `1e-12` | **PASS (Exact match to production PQK-2nn)** |
| D_prod_pqk2 vs D_prod_e2 / 4.0 (Production Identity B == C) | `0.00e+00` | `0.00e+00` | `1e-12` | **PASS (Exact B == C identity confirmed)** |
| NEGATIVE CONTROL: D_RDM vs D_flawed (Missing sqrt(deg) weights) | `5.61e-01` | `3.80e-01` | `1e-12` | **CONFIRMED SENSITIVE (Discrepancy strongly detected)** |

## 3. Negative Control Validation

When the single-site features in the deduplicated map are left unweighted (missing the $\sqrt{\mathrm{degree}}$ correction for shared vertices), the discrepancy between $D_{\mathrm{RDM}}$ and $D_{\mathrm{flawed}}$ immediately spikes to `0.5614` (> 1e-3). This confirms that the verification suite is strictly sensitive to improper vertex-weighting and boundary conventions.

## 4. Methodological Scope & Limitations

### What the Independent Identity Establishes:
1. For any set of quantum states where odd-parity Pauli terms vanish (such as TFIM ground states in the even parity sector), the 2-local RDM Frobenius distance is **strictly isomorphic** to a Euclidean distance over classical 2-point correlators.
2. A quantum computer measuring 2-RDMs and a classical learner using 2-point correlators evaluate **the exact same reproducing kernel Hilbert space (RKHS)**.

### What Production Score Equality Establishes:
1. The numerical pipelines for `PQK-2nn` and `E2 (4n)` are algebraically consistent and produce identical predictions to machine precision ($0.00\text{e+}00$).

### What Neither Establishes:
1. Score equality does **not** prove that PQK-2nn is unlearnable; rather, it proves that PQK-2nn **is classically simulable** using 2-point correlators.
2. The equivalence depends on the parity symmetry of the state manifold (vanishing odd-order correlators); systems with non-zero single-qubit $Y$ or $Z$ expectations require additional terms in the Pauli basis expansion to maintain identity.
