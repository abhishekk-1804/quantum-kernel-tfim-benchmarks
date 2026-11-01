# Verification Report: Portable Saved-Artifact Bundle

**Status:** PASSED  
**Execution Runtime:** 0.2108 seconds  
**Python Version:** 3.12.10  
**NumPy Version:** 2.5.4  
**SciPy Version:** 1.18.1  

---

## Checks Summary

| Check ID | Description | Status | Key Findings |
| :--- | :--- | :---: | :--- |
| **CHECK_A** | Payload Manifest Integrity | PASSED | 32 files verified via SHA-256 |
| **CHECK_B** | CSV Key Integrity | PASSED | Exactly 20 unique seeds per model/cell; zero duplicates |
| **CHECK_C** | Array Metrics Reproduction | PASSED | Max MAE diff = 0.00e+00 (tol 1e-7); Max R² diff = 0.00e+00 |
| **CHECK_D** | Paired Summary Verification | PASSED | 16 FQ lower, 4 PQK lower (Seeds 8, 9, 11, 16); Mean diff = -0.1248, SE = 0.0334 |
| **CHECK_E** | Wilcoxon Signed-Rank Test | PASSED | $W=21.0$, $p=8.5068 \times 10^{-4}$ reproduced to machine precision |
| **CHECK_F** | Stage 2 Aggregation | PASSED | 49 experimental cells independently aggregated without discrepancies |

---
*Report generated programmatically by `verify_bundle.py`.*
