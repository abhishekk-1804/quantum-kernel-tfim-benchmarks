# Independent Contributor Review Instructions and Evaluation Form

**Status:** Independent Contributor Review Pending  
**Review Package:** `docs/verification/review_package_20261023_172944Z`  
**Target Task:** Task 6 (Controlled OOD Phase-Shift Generalization)  

> **NOTICE TO REVIEWER:** This evaluation form must be completed by an independent subject-matter expert who did NOT author the original Stage 3 implementation. Completion of these checks is required before any modified results may be integrated into the publication manuscript.

---

## 1. Fast Automated Verification Execution

To execute the full suite of 7 automated verification checks using the active project Python environment, execute from the repository root:

```bash
D:\qml_env\Scripts\python.exe -B docs/verification/review_package_20261023_172944Z/scripts/reviewer_checks.py
```

---

## 2. Reviewer Verification Checklist

### Check 1: Original CSV Pairing
- **Description:** Verify results/stage3/t6_ood_shift.csv contains exactly 20 matching seeds for FQ and PQK-2nn without missing or duplicated rows.
- **Reviewer Finding:** [ ] Passed  [ ] Discrepancy Observed
- **Comments / Notes:** ___________________________________________________

### Check 2: Array Reconstruction (Seed 00)
- **Description:** Verify that Seed 00 prediction arrays yield FQ MAE = 0.030009 and match CSV to machine precision (< 1e-16).
- **Reviewer Finding:** [ ] Passed  [ ] Discrepancy Observed
- **Comments / Notes:** ___________________________________________________

### Check 3: Array Reconstruction (Seed 08)
- **Description:** Verify that Seed 08 prediction arrays yield PQK-2nn MAE = 0.054557 (superior to FQ = 0.070931) and match CSV to machine precision.
- **Reviewer Finding:** [ ] Passed  [ ] Discrepancy Observed
- **Comments / Notes:** ___________________________________________________

### Check 4: Mean Difference & Paired SE
- **Description:** Verify mean paired diff = -0.1248 ± 0.0334, rejecting historical proposed SE 0.0166.
- **Reviewer Finding:** [ ] Passed  [ ] Discrepancy Observed
- **Comments / Notes:** ___________________________________________________

### Check 5: Wilcoxon Test Configuration
- **Description:** Verify two-sided Wilcoxon yields W = 21.0 and raw p = 8.51e-4, rejecting historical W = 1.0.
- **Reviewer Finding:** [ ] Passed  [ ] Discrepancy Observed
- **Comments / Notes:** ___________________________________________________

### Check 6: Independent Holm Calculation
- **Description:** Verify Holm adjustment across 3-comparison family yields p_holm = 8.51e-4 for FQ vs PQK2.
- **Reviewer Finding:** [ ] Passed  [ ] Discrepancy Observed
- **Comments / Notes:** ___________________________________________________

### Check 7: Full vs Intercept Comparison
- **Description:** Verify Full FQ improves MAE over constant intercept in 20/20 seeds (0.0602 vs 0.4616).
- **Reviewer Finding:** [ ] Passed  [ ] Discrepancy Observed
- **Comments / Notes:** ___________________________________________________

---

## 3. Reviewer Sign-Off and Identification Form

- **Reviewer Name:** __________________________________________________
- **Affiliation / Organization:** __________________________________________________
- **Professional Role:** __________________________________________________
- **Confirmation of Independence:** I confirm that I did not author the original Stage 3 implementation (`scripts/stage3_ood_shift.py` or `scripts/stage3_analysis.py`).  
  *Signature:* _____________________________________________  *Date:* _______________
- **Commands Executed:**
  ```
  ___________________________________________________________________
  ```
- **Observed Discrepancies or Irregularities:**
  ___________________________________________________________________
  ___________________________________________________________________

- **Scope of Approval:**
  - [ ] **APPROVED FOR MANUSCRIPT INTEGRATION:** All 7 mathematical checks verified; proposed manuscript text in `proposed_paper/` accurately reflects findings without overstatement.
  - [ ] **PROVISIONALLY APPROVED:** Requires minor textual adjustments noted above.
  - [ ] **REJECTED:** Material mathematical or procedural defects remain unresolved.

- **Reviewer Final Signature:** _________________________________________  **Date:** _______________
