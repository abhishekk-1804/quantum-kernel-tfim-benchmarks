# Gate-0 Reproduction Card: Contributor C1 (Lead)

## 1. Specifications
- **Baseline Commit:** `739a724919f52164193a200b6e07d827fe273c62`
- **Environment Spec:** Python 3.12.10, NumPy 2.5.4, SciPy 1.18.1, scikit-learn 1.9.1 in active virtual environment `D:\qml_env`
- **Config File:** `scripts/common.py`
- **Arm:** Numerical Sparse Diagonalization & Parity-Sector Eigenpair Engine (`src/hamiltonians.py`)
- **Seeds:** Fixed benchmark evaluation seeds 0–19

---

## 2. Verification Commands
Execute the following verification commands:
```powershell
# 1. Sparse vs dense parity sector test
D:\qml_env\Scripts\python.exe -m pytest -k sparse_vs_dense -v

# 2. Eigenpair residual verification across n in {4, 6, 8, 10, 12, 14}
D:\qml_env\Scripts\python.exe -c "import sys; sys.path.insert(0, 'src'); from hamiltonians import build_tfim, ground_state; import numpy as np; [print(f'n={n}: E0={E0:.8f}, residual={float(np.linalg.norm(H.dot(psi) - E0*psi)):.3e}') for n in [4,6,8,10,12,14] for H in [build_tfim(n, g=1.0, J=1.0, boundary='open')] for E0, psi, _ in [ground_state(H, n, sector='even')]]"
```

---

## 3. Expected Artifacts and Metrics
- **Expected Output Artifact:** Parity-projected ground statevectors $|\psi_0\rangle$ and energy eigenvalues $E_0$.
- **Expected Benchmark Metric:**
  - **Source File:** `results/t1_entropy_gridv3.csv`
  - **Filter Criteria:** `task == "t1"`, `N_train == 40`, `seed == 0`, `model == "PQK-2nn"`, `metric == "r2"`
  - **Exact Value:** `0.9802670332`
- **Tolerances:**
  - Sparse vs. dense matrix overlap error: $< 1.0 \times 10^{-10}$
  - Eigenpair residual $\|H \psi_0 - E_0 \psi_0\|_2$: $< 1.0 \times 10^{-9}$ for all $n \in \{4, 6, 8, 10, 12, 14\}$
  - Test $R^2$ re-evaluation: $|R^2_{\text{observed}} - 0.9802670332| < 1.0 \times 10^{-10}$

---

## 4. Metrics to Record
- **Execution Runtime:** [Record seconds]
- **Peak Memory Footprint:** [Record MB]

---

## 5. Known Limitations
- Exact numerical diagonalization scales exponentially as $2^n$ in statevector memory.
- Restricted to $n \le 14$ spins ($2^{14} = 16{,}384$ amplitudes; density matrices up to $256 \times 256$ in partial traces).

---

## 6. Results
*(Left empty for Gate-0 execution recording)*

```text

```
