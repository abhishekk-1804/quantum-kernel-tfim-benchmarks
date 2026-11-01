# Stage 4 Artifact Availability & Portability Assessment
**Workspace:** `D:\quantum-kernel-tfim-benchmarks`  
**Package:** `docs/stage4/readiness_20261023_180339Z/`  
**Classification:** Artifact audit and review-bundle specification.

---

## 1. Portability Audit Across Git Commits

To assess whether a fresh clone can reproduce the benchmark findings, we evaluated asset availability across Git history:

| Asset | Tracked at `dff0171` | Tracked at `HEAD` (`292d689`) | Current Working Tree | Fresh-Clone Impact |
| :--- | :---: | :---: | :---: | :--- |
| `src/hamiltonians.py` | YES | YES | Tracked | Physics core available |
| `src/kernels.py` | YES | YES | Tracked | Kernel engine available |
| `scripts/stage2_equal_budget.py` | YES | YES | Tracked | Stage 2 executable available |
| `results/stage2/t1_equal_budget.csv` | YES | YES | Tracked | Stage 2 results available |
| `scripts/stage3_ood_shift.py` | **NO** | YES | Tracked | Stage 3 code available at `HEAD` |
| `results/stage3/t6_ood_shift.csv` | **NO** | YES | Tracked | Stage 3 results available at `HEAD` |
| `docs/.../predictions/seed_*.npz` | **NO** | **NO** | **UNTRACKED** | **UNAVAILABLE in fresh clone** |
| `docs/verification/*` | **NO** | **NO** | **UNTRACKED** | **UNAVAILABLE in fresh clone** |

### Key Portability Findings:
1. **Target Commit `dff0171` Incompleteness:** Commit `dff0171` captures Stage 2 but completely predates Stage 3. A fresh clone checked out at `dff0171` lacks `scripts/stage3_ood_shift.py` and `results/stage3/t6_ood_shift.csv`.
2. **Current `HEAD` (`292d689`) Completeness for Level A & C:** `HEAD` contains all source code and primary result CSVs for Stages 0, 1, 2, and 3. Level A (table regeneration) and Level C (fresh rerun) can execute from a fresh clone of `HEAD`.
3. **Critical Portability Gap for Level B:** The 20 raw prediction array archives (`seed_00_arrays.npz` through `seed_19_arrays.npz`, total size 2.94 MB) are **untracked**. A fresh clone cannot perform Level B bit-level array checks without an explicit review bundle.

---

## 2. Portable Review-Bundle Specification

To enable an external reviewer to execute Level B spot-checks without access to this specific local workspace, the following files must be bundled or committed:

### 2.1 Required Bundle Manifest
- **Source Scripts:**
  * `src/hamiltonians.py` (SHA-256: `3b3ebf2a...`)
  * `src/kernels.py` (SHA-256: `bca96fb8...`)
  * `scripts/stage3_ood_shift.py` (SHA-256: `41bb8ee9...`)
- **Primary Results Data:**
  * `results/stage3/t6_ood_shift.csv` (SHA-256: `81908f5a14f0c7c2...`)
- **Raw Prediction Array Archives (20 files, 2.94 MB):**
  * `docs/verification/audit_20261023_155335Z/predictions/seed_00_arrays.npz` (SHA-256: `ebc8bf61...`)
  * ... through `seed_19_arrays.npz` (SHA-256: `78bb1a49...`)
- **Review Helper & Driver:**
  * `docs/verification/review_package_20261023_172944Z/scripts/reviewer_checks.py`
  * `docs/stage4/readiness_20261023_180339Z/scripts/reproduction_driver.py`

### 2.2 Expected Bundle Execution
```powershell
pip install -r requirements.txt
python docs/stage4/readiness_20261023_180339Z/scripts/reproduction_driver.py
```
- **Runtime:** $< 5$ seconds.
- **Tolerances:** Numerical discrepancies $< 10^{-16}$ (within `atol=1e-7, rtol=0`).

### 2.3 Policy Statement on External Archives
> [!NOTE]
> Per project safety rules, **no external archive (e.g. Zenodo, OSF, or tarball) has been generated or published automatically**. This specification establishes the exact manifest for when human contributors decide to release a public artifact bundle.
