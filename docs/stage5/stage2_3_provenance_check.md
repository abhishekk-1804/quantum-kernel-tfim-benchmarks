# Stage 2 & 3 Protocol Provenance and Timing Verification Report
**Workspace:** `D:\quantum-kernel-tfim-benchmarks`  
**Audit Date:** 2026-10-23 18:51:50Z  
**Auditor:** Automated forensic timing audit  

---

## 1. Executive Summary & Provenance Classifications

Per project governance rules, an experiment can be classified as **'Confirmatory (prospectively frozen protocol)'** ONLY IF timing establishes that the protocol was formally committed/frozen *prior* to data generation.
If a protocol was committed atomically with the results or generated after the benchmark execution, the protocol must be formally classified as **'Exploratory (documented protocol, timing not established)'**.

### Formal Classifications:
- **Stage 2 (Equal-Total-Budget Experiment):**
  * **Classification:** **`Exploratory (documented protocol, timing not established)`**
  * **Rationale:** In Git, all 6 Stage 2 artifacts (scripts, tests, results, and summary) were committed **atomically** in a single commit (`dff0171183c99c43f9555964ba0a88731ddc98cf`). Furthermore, file-system timestamps show that the summary report (`equal_budget_summary.md`, mtime 14:56:39 UTC) was created *after* the results CSV (`t1_equal_budget.csv`, mtime 14:53:44 UTC). No prior Git commit froze the protocol prospectively.
- **Stage 3 (Controlled OOD Phase-Shift Generalization):**
  * **Classification:** **`Exploratory (documented protocol, timing not established)`**
  * **Rationale:** In Git, all 6 Stage 3 artifacts (`ood_protocol.md`, `ood_findings.md`, `t6_ood_shift.csv`, scripts, tests) were committed **atomically** in a single commit (`292d689dd845f6228fae6265cffe83b81d5f0f66`). While file-system metadata shows `ood_protocol.md` was created locally at 15:21:02 UTC prior to CSV completion (15:33:35 UTC), Git history does not record an external or prior cryptographic commit freezing the protocol. Therefore, timing is not verifiably established in version control.

---

## 2. Stage 2 Detailed Forensic Timestamps

| File Path | File System Created (UTC) | File System Modified (UTC) | Git Commit Hash | Commit Timestamp | Commit Message |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `docs/stage2/equal_budget_summary.md` | 2026-10-23 14:55:18Z | 2026-10-23 14:56:39Z | `dff0171` | 2026-10-23T20:32:50+05:30 | feat(stage2): complete equal-total-budget benchmark and crossover analysis |
| `docs/stage2/fig_equal_budget_curve.csv` | 2026-10-23 14:55:16Z | 2026-10-23 14:56:38Z | `dff0171` | 2026-10-23T20:32:50+05:30 | feat(stage2): complete equal-total-budget benchmark and crossover analysis |
| `results/stage2/t1_equal_budget.csv` | 2026-10-23 14:23:32Z | 2026-10-23 14:53:44Z | `dff0171` | 2026-10-23T20:32:50+05:30 | feat(stage2): complete equal-total-budget benchmark and crossover analysis |
| `scripts/stage2_equal_budget.py` | 2026-10-23 14:22:39Z | 2026-10-23 14:22:39Z | `dff0171` | 2026-10-23T20:32:50+05:30 | feat(stage2): complete equal-total-budget benchmark and crossover analysis |
| `scripts/stage2_analysis.py` | 2026-10-23 14:25:03Z | 2026-10-23 14:55:55Z | `dff0171` | 2026-10-23T20:32:50+05:30 | feat(stage2): complete equal-total-budget benchmark and crossover analysis |
| `tests/test_stage2_budget.py` | 2026-10-23 14:22:53Z | 2026-10-23 14:22:53Z | `dff0171` | 2026-10-23T20:32:50+05:30 | feat(stage2): complete equal-total-budget benchmark and crossover analysis |

---

## 3. Stage 3 Detailed Forensic Timestamps

| File Path | File System Created (UTC) | File System Modified (UTC) | Git Commit Hash | Commit Timestamp | Commit Message |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `docs/stage3/ood_protocol.md` | 2026-10-23 15:21:02Z | 2026-10-23 15:21:02Z | `292d689` | 2026-10-23T21:11:11+05:30 | feat(stage3): complete controlled OOD phase-shift generalization benchmark |
| `docs/stage3/ood_findings.md` | 2026-10-23 15:33:58Z | 2026-10-23 15:34:55Z | `292d689` | 2026-10-23T21:11:11+05:30 | feat(stage3): complete controlled OOD phase-shift generalization benchmark |
| `results/stage3/t6_ood_shift.csv` | 2026-10-23 15:30:07Z | 2026-10-23 15:33:35Z | `292d689` | 2026-10-23T21:11:11+05:30 | feat(stage3): complete controlled OOD phase-shift generalization benchmark |
| `scripts/stage3_ood_shift.py` | 2026-10-23 15:27:06Z | 2026-10-23 15:27:06Z | `292d689` | 2026-10-23T21:11:11+05:30 | feat(stage3): complete controlled OOD phase-shift generalization benchmark |
| `scripts/stage3_analysis.py` | 2026-10-23 15:31:27Z | 2026-10-23 15:34:43Z | `292d689` | 2026-10-23T21:11:11+05:30 | feat(stage3): complete controlled OOD phase-shift generalization benchmark |
| `tests/test_stage3_ood.py` | 2026-10-23 15:27:46Z | 2026-10-23 15:27:46Z | `292d689` | 2026-10-23T21:11:11+05:30 | feat(stage3): complete controlled OOD phase-shift generalization benchmark |

---

## 4. Policy Impact on Manuscript Tables

Because neither stage satisfies the strict prospective pre-registration standard in version control, all compiled tables incorporating Stage 2 or Stage 3 data (`tab_equal_budget.tex` and `tab_ood.tex`) MUST explicitly display the tag **'Exploratory'** in their captions and documentation headers.

