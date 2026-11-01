# Stage 4 Reproduction Plan: Multi-Level Verification Protocols
**Workspace:** `D:\quantum-kernel-tfim-benchmarks`  
**Package:** `docs/stage4/readiness_20261023_180339Z/`  
**Classification:** Reproduction specification; distinguishing execution tiers.

---

## 1. Definition of Reproduction Levels

To prevent overstating reproducibility or confusing inspection with independent execution, this protocol establishes four distinct operational tiers:

```
+-------------------------------------------------------------------------+
| Level A: Table Regeneration from Existing Outputs                       |
|   Inputs: Existing results/*.csv and stats.csv                          |
|   Runtime: ~10 seconds | Dependencies: pandas, numpy                   |
|   Scope: Reconstructs tables and summary metrics from stored CSV rows.   |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| Level B: Numerical Spot-Checks on Saved Raw Arrays                      |
|   Inputs: docs/.../predictions/seed_*.npz (20 files, allow_pickle=False)|
|   Runtime: ~3 seconds | Dependencies: numpy, scipy                      |
|   Scope: Verifies exact prediction array targets, SVR dual variables,   |
|          intercepts, and Wilcoxon signed-rank tests to machine prec.   |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| Level C: Fresh Experiment Rerun from Scratch                            |
|   Inputs: Pure source scripts (scripts/stage2_*.py, stage3_*.py)        |
|   Runtime: ~1.5 - 2.0 hours | Hardware: Multi-core CPU                  |
|   Scope: Re-diagonalizes TFIM Hamiltonians, regenerates state vectors,  |
|          recomputes Gram matrices, and re-runs nested-CV SVR grids.     |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| Level D: Independent Clean-Room Implementation                          |
|   Inputs: Mathematical specification in docs/PROJECT_CHARTER.md        |
|   Runtime: Variable | Tools: Julia, Qiskit, QuTiP, PennyLane            |
|   Scope: Clean-room implementation verifying theory independent of code.|
+-------------------------------------------------------------------------+
```

---

## 2. Operational Scope of Proposed Commands

The commands provided in this readiness package (`scripts/reproduction_driver.py` and `tests/test_reproduction_driver.py`) explicitly test **Level A (Table/Budget Integrity)** and **Level B (Numerical Spot-Checks on Precomputed Arrays)**.

They do **NOT** constitute a Level C fresh experiment rerun. Calling precomputed array inspection an "experiment rerun" is strictly prohibited by project governance rules.

---

## 3. Step-by-Step Execution Protocols

### 3.1 Level A Execution: Table Regeneration
```powershell
# Recompute all summary statistics and confirmatory tables from CSV data
D:\qml_env\Scripts\python.exe scripts/stats.py
D:\qml_env\Scripts\python.exe scripts/make_tables.py
```
- **Expected Outcome:** Table values in `paper/tables/` regenerated bit-for-bit.
- **Pass/Fail Criteria:** Zero discrepancy against pinned numbers in `results/stats.csv`.

### 3.2 Level B Execution: Saved Array Spot-Checks
```powershell
# Run the local reproduction driver (5 core checks)
D:\qml_env\Scripts\python.exe docs/stage4/readiness_20261023_180339Z/scripts/reproduction_driver.py

# Run the pytest verification suite
D:\qml_env\Scripts\python.exe -m pytest docs/stage4/readiness_20261023_180339Z/tests/test_reproduction_driver.py -v
```
- **Expected Outcome:** All 5 checks and 5 pytest test cases pass.
- **Pass/Fail Tolerance:** `atol=1e-7, rtol=0` (observed max discrepancy: $< 10^{-16}$).

### 3.3 Level C Execution: Full Experiment Reruns (Compute Intensive)
```powershell
# Stage 2 Equal-Total-Budget Rerun (~1.5 hours)
D:\qml_env\Scripts\python.exe scripts/stage2_equal_budget.py --n-seeds 20

# Stage 3 OOD Phase-Shift Rerun (~1.2 hours)
D:\qml_env\Scripts\python.exe scripts/stage3_ood_shift.py --seeds 20
```
- **Required Resources:** 4+ physical CPU cores, ~8 GB RAM, ~2 hours wall time.
- **Resumability:** Scripts flush per seed block; interrupted runs skip completed rows.
