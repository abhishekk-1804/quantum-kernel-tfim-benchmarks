# Stage 4 Local Smoke Check Report
**Workspace:** `D:\quantum-kernel-tfim-benchmarks`  
**Package:** `docs/stage4/readiness_20261023_180339Z/`  
**Executed:** 2026-10-23 18:20:40Z  
**Classification:** **Local smoke check; not an independent experiment rerun.**

---

## 1. Execution Environment & Invariants
- **Operating System:** Windows (win32)
- **Python Executable:** `D:\qml_env\Scripts\python.exe`
- **Python Version:** 3.12.10
- **NumPy Version:** 2.5.4
- **SciPy Version:** 1.18.1
- **Pandas Version:** 3.0.6
- **Pytest Version:** 9.1.1
- **Working Tree Integrity:** Read-only preservation maintained; zero modifications to pre-existing files.

---

## 2. Summary of Executed Commands

| Step | Command | Exit Code | Wall Time | Warnings | Status |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **Driver** | `python docs/stage4/.../scripts/reproduction_driver.py` | `0` | `1.580 s` | 0 | **PASS** |
| **Pytest** | `pytest docs/stage4/.../tests/test_reproduction_driver.py -v` | `0` | `2.002 s` | 0 | **PASS** |

**Observed Test Count:** Exactly **5 passed out of 5 collected** (100% pass rate in local environment).

---

## 3. Detailed Check Breakdown

### Check 1: Input Availability & Cryptographic Integrity
- Verified existence and SHA-256 checksums of `t1_equal_budget.csv`, `t6_ood_shift.csv`, `seed_00_arrays.npz`, and `seed_08_arrays.npz`.
- Result: **PASS**.

### Check 2: First-Principles Physics & RDM Verification
- Recomputed 1D TFIM Hamiltonian ($n=4, g=1.0$), ground state vector $\psi$, energy $E_0 = -4.758770$, gap $= 2.694593$.
- Verified 1-RDM trace ($1.000000$) and positivity (eigenvalues $\ge -10^-12$).
- Verified 2-RDM trace ($1.000000$) and positivity (eigenvalues $\ge -10^-12$).
- Verified 2-body nearest-neighbor Pauli feature extraction ($15$ dimensions).
- Result: **PASS**.

### Check 3: $Z_2$ Parity Symmetry Constraints
- Ground state in even sector has $\langle Z_0 \rangle = 1.11 \times 10^-16 \approx 0.0$ (vanishing single-site magnetization).
- Transverse magnetization $\langle X_0 \rangle = 0.862086 > 0$ (non-trivial order).
- Result: **PASS**.

### Check 4: Stage 2 Budget Arithmetic
- Verified budget allocation formula $B_{\text{tot}} = S \times \text{evaluations}$.
- At $B_{\text{tot}} = 10^5$, $N=40$: FQ requires $780$ pairs $\to S = 128$ shots/pair; Feature arm requires $240$ states $\to S = 416$ shots/state.
- Shot cost ratio: Feature models allocate $3.25\times$ higher shots per evaluation under identical total measurement budgets.
- Result: **PASS**.

### Check 5: Saved Array vs CSV T6 Metric Agreement
- Recomputed OOD MAE on raw prediction arrays for Seed 00 and Seed 08.
- Observed discrepancies against `results/stage3/t6_ood_shift.csv`:
  * Seed 00 FQ: $6.25 \times 10^-17$
  * Seed 00 PQK-2nn: $8.33 \times 10^-17$
  * Seed 08 FQ: $2.78 \times 10^-17$
  * Seed 08 PQK-2nn: $4.16 \times 10^-17$
- Result: **PASS** (strictly within `atol=1e-7, rtol=0`).

---

## 4. Raw Command Logs

### 4.1 Reproduction Driver Log
```
======================================================================
STAGE 4 LOCAL REPRODUCTION DRIVER (SMOKE CHECK)
Timestamp: 2026-10-23 18:20:38Z
Repository Root: D:\quantum-kernel-tfim-benchmarks
Python: D:\qml_env\Scripts\python.exe
======================================================================
[CHECK 1] Input Availability & Cryptographic Integrity
  Verified results\stage2\t1_equal_budget.csv (SHA-256: 22d66cd6e27372a5...)
  Verified results\stage3\t6_ood_shift.csv (SHA-256: 81908f5a14f0c7c2...)
  Verified docs\verification\audit_20261023_155335Z\predictions\seed_00_arrays.npz (SHA-256: ebc8bf61a7917260...)
  Verified docs\verification\audit_20261023_155335Z\predictions\seed_08_arrays.npz (SHA-256: ff4f63600aabf68b...)
  PASS: All required spot-check inputs present and readable.
[CHECK 2] First-Principles Physics & RDM Verification
  Ground energy: -4.758770, Gap: 2.694593
  1-RDM trace: 1.000000, 2-RDM trace: 1.000000
  Classical 2pt_pauli_nn feature dim: 15 (verified)
  PASS: Physics core and RDM calculations verified.
[CHECK 3] Z_2 Parity Symmetry Verification
  Single-site <Z_0>: 1.11e-16 (identically zero within numerical precision)
  Single-site <X_0>: 0.862086 (positive finite polarization)
  PASS: Z_2 symmetry constraints verified.
[CHECK 4] Stage 2 Budget Allocation Arithmetic
  Budget B_tot=100000: FQ pairs=780, S_fq=128 shots/pair
  Budget B_tot=100000: Feature states=240, S_feat=416 shots/state
  Shot cost ratio (Feature / FQ): 3.25x higher precision per evaluation
  PASS: Equal-budget arithmetic verified.
[CHECK 5] Saved Array vs CSV T6 Metric Agreement
  Seed 00: FQ Array=0.030009, CSV=0.030009 (disc=6.25e-17)
  Seed 00: PQK Array=0.199973, CSV=0.199973 (disc=8.33e-17)
  Seed 08: FQ Array=0.070931, CSV=0.070931 (disc=2.78e-17)
  Seed 08: PQK Array=0.054557, CSV=0.054557 (disc=4.16e-17)
  PASS: Saved prediction arrays match CSV to machine precision (< 1e-16).
======================================================================
STATUS: ALL 5 SMOKE CHECKS PASSED (0.034 s)
Classification: Local smoke check; not an independent experiment rerun.
======================================================================
```

### 4.2 Pytest Execution Log
```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.7.0 -- D:\qml_env\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\quantum-kernel-tfim-benchmarks
collecting ... collected 5 items

docs/stage4/readiness_20261023_180339Z/tests/test_reproduction_driver.py::test_check_1_input_availability PASSED [ 20%]
docs/stage4/readiness_20261023_180339Z/tests/test_reproduction_driver.py::test_check_2_physics_rdm_and_features PASSED [ 40%]
docs/stage4/readiness_20261023_180339Z/tests/test_reproduction_driver.py::test_check_3_symmetry_properties PASSED [ 60%]
docs/stage4/readiness_20261023_180339Z/tests/test_reproduction_driver.py::test_check_4_stage2_budget_arithmetic PASSED [ 80%]
docs/stage4/readiness_20261023_180339Z/tests/test_reproduction_driver.py::test_check_5_t6_array_csv_agreement PASSED [100%]

============================== 5 passed in 1.16s ==============================
```
