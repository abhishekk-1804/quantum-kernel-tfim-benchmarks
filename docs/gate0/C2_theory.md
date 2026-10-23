# Gate-0 Reproduction Card: Contributor C2 (Theory)

## 1. Specifications
- **Baseline Commit:** `739a724919f52164193a200b6e07d827fe273c62`
- **Environment Spec:** Python 3.12.10, NumPy 2.5.4, SciPy 1.18.1, scikit-learn 1.9.1 in active virtual environment `D:\qml_env`
- **Config File:** `tests/test_identities_integration.py`
- **Arm:** Quantum Kernel Representation Theory & Algebraic Identities (`src/kernels.py`)
- **Seeds:** Fixed seeds (e.g., seed `20261023` for 1D TFIM, seed `20261024` for 2D frustrated lattice)

---

## 2. Verification Commands
Execute the following verification command:
```powershell
D:\qml_env\Scripts\python.exe -m pytest tests/test_identities_integration.py -v
```

---

## 3. Expected Artifacts and Metrics
- **Expected Output Artifact:** Full test report confirming exact equivalence across pre-exponential squared distances and Gram matrices.
- **Expected Benchmark Metrics:**
  - **Source File:** `results/t3_n14_fraction.csv`
  - **Row 0:** `kernel == "FQ"`, `gamma_rule == "none"`, `n == 14`, `n_pairs == 8700`, `fraction == 0.0`, `min_entry == 0.161635`
  - **Row 3:** `kernel == "PQK-2nn"`, `gamma_rule == "1.0"`, `n == 14`, `n_pairs == 8700`, `fraction == 0.0`, `min_entry == 0.019492`
- **Tolerances:**
  - Pre-exponential squared distance equality: `atol = 1e-12`, `rtol = 0.0`
  - Gram matrix equality: `atol = 1e-12`, `rtol = 0.0`
  - Negative control distance gaps: `gap > 1e-6`
  - Off-diagonal entries $< 1e-3$ count: `0` (exact fraction `0.0`)

---

## 4. Draft Checklist: Parity vs. Reality Derivation
*(Checklist only; no prose claims)*

- [ ] Global $\mathbb{Z}_2$ spin-flip parity generator: $P = \bigotimes_{i=0}^{n-1} X_i$.
- [ ] Hamiltonian commutation: $[H, P] = 0$ for Eq.~(1).
- [ ] Even-parity sector ground state: $P |\psi\rangle = +1 |\psi\rangle$.
- [ ] Single-qubit Pauli transformations under parity: $P X_i P = X_i$, $P Y_i P = -Y_i$, $P Z_i P = -Z_i$.
- [ ] Vanishing 1-body odd expectations: $\langle Y_i \rangle = \langle \psi | P Y_i P | \psi \rangle = -\langle Y_i \rangle = 0$; $\langle Z_i \rangle = 0$.
- [ ] 1-qubit reduced density matrix structure: $\rho_i = \frac{1}{2}(I + \langle X_i \rangle X_i)$.
- [ ] Frobenius distance identity for PQK-1: $\|\rho_i(a) - \rho_i(b)\|_F^2 = \frac{1}{2}(\langle X_i \rangle_a - \langle X_i \rangle_b)^2$.
- [ ] Two-qubit Pauli transformations under parity: $\sigma_i \otimes \sigma_j$ transforms as $(-1)^{\mathbb{I}(\sigma_i \in \{Y,Z\}) + \mathbb{I}(\sigma_j \in \{Y,Z\})}$.
- [ ] Non-zero 2-body Pauli expansion components: $\{I \otimes I, X_i \otimes I, I \otimes X_j, X_i \otimes X_j, Y_i \otimes Y_j, Z_i \otimes Z_j\}$.
- [ ] Frobenius distance identity for 2-qubit pair: $\|\rho_{ij}(a) - \rho_{ij}(b)\|_F^2 = \frac{1}{4} \left[ (\Delta X_i)^2 + (\Delta X_j)^2 + (\Delta X_i X_j)^2 + (\Delta Y_i Y_j)^2 + (\Delta Z_i Z_j)^2 \right]$.
- [ ] Multi-edge summation on general graph $G=(V, E)$: $\sum_{(i,j) \in E} [(\Delta X_i)^2 + (\Delta X_j)^2] = \sum_{i \in V} \text{deg}(i) (\Delta X_i)^2$.
- [ ] Deduplicated feature vector definition: $\tilde{f} = [x_i \sqrt{\text{deg}(i)}]_{i \in V} \cup [\langle X_i X_j \rangle, \langle Y_i Y_j \rangle, \langle Z_i Z_j \rangle]_{(i,j) \in E}$.
- [ ] Norm equivalence proof: $\|\tilde{f}(a) - \tilde{f}(b)\|^2 = 4 \sum_{e \in E} \|\rho_e(a) - \rho_e(b)\|_F^2$.
- [ ] Physical reality check: open boundary conditions induce non-uniform degrees (e.g., $\text{deg}=1$ vs. $2$ in 1D chain; $\text{deg}=2$ vs. $3$ in $2 \times 4$ ladder).
- [ ] Perturbation vulnerability: transverse field tilt or longitudinal fields ($h_z Z_i$) break parity symmetry, generating non-zero $\langle Z_i \rangle$ and $\langle Y_i \rangle$.

---

## 5. Metrics to Record
- **Execution Runtime:** [Record seconds]
- **Peak Memory Footprint:** [Record MB]

---

## 6. Known Limitations
- Parity identities strictly hold only for reflection-symmetric Hamiltonians without longitudinal magnetic fields.
- 2-RDM Frobenius equality applies specifically to nearest-neighbour graph edges, not all $\binom{n}{2}$ pairs.

---

## 7. Results
*(Left empty for Gate-0 execution recording)*

```text

```
