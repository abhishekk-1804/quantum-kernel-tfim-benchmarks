# Final T6 Contributor-Review Package Status

**Status:** Prepared for independent review  
**Execution Timestamp (UTC):** `2026-10-23T17:39:27.232228+00:00`  
**Package Location:** `docs/verification/review_package_20261023_172944Z`  

## 1. Summary of Completed Checks

1. **Discovery & Input Mapping:** All 38 inputs (CSVs, NPZs, audit tables, scripts) mapped with SHA-256 and verified safe.
2. **Descriptive Statistics:** Verified exact sample means, SDs (`ddof=1`), and sample SEs ($s / \sqrt{20}$) for all 5 key vectors.
3. **Uncertainty Claims Reconciliation:** Proved that historical proposed SE claims (`0.0039`, `0.0154`, `0.0166`, `0.0042`) do not reproduce. Authoritative empirical SEs established.
4. **Statistical Family Reconciliation:** Reconciled 3-comparison family with exact Wilcoxon statistics ($W=21.0$ for PQK2, $W=0.0$ for Baselines) and verified Holm adjustment to machine precision (`0.00e+00` discrepancy).
5. **Claim Separation:** Strictly verified and documented that FQ vs PQK-2nn is a 16/4 directional split (Seeds 8, 9, 11, 16 favor PQK2), whereas Full FQ vs Intercept is a 20/0 directional split.
6. **Executable Contributor Review Tool:** Created `scripts/reviewer_checks.py` and `reports/CONTRIBUTOR_REVIEW.md`.
7. **Draft Manuscript Scoped Artifacts:** Drafted `proposed_paper/t6_results.tex` and `proposed_paper/t6_statistics_table.tex` under strict negative constraints without touching `paper/`.

## 2. Contradicted Historical Values

- **Wilcoxon Statistic W=1.0 for OOD MAE:** Contradicted. True statistic is $W=21.0$. ($W=1.0$ belongs to ID MAE).
- **P-value 7.08e-4 for OOD MAE:** Contradicted. True p-value is $8.51e-4$. ($7.08e-4$ belongs to OOD $R^2$).
- **Claim that FQ is lower in all 20 seeds:** Contradicted. FQ is lower in 16 seeds, higher in 4 seeds.
- **Proposed SE values (0.0039, 0.0154, 0.0166, 0.0042):** Contradicted. True SEs are $0.0085, 0.0294, 0.0334, 0.0162$.

## 3. Outstanding Blockers

1. **Independent Human Review Sign-Off:** An independent contributor who did not author the original code must execute `scripts/reviewer_checks.py` and sign `reports/CONTRIBUTOR_REVIEW.md`.
2. **Manuscript Integration Remains Blocked:** Until human sign-off is completed, no paper files (`paper/main.tex`, etc.) may be modified.

## 4. Exact Next Human-Review Action

Execute from repository root:
```bash
D:\qml_env\Scripts\python.exe -B docs/verification/review_package_20261023_172944Z/scripts/reviewer_checks.py
```
Then review observations and complete sign-off form in `reports/CONTRIBUTOR_REVIEW.md`.
