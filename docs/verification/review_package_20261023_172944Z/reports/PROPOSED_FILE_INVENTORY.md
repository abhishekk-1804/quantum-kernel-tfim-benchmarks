# Proposed File Inventory and Release Assessment

**Package Directory:** `docs/verification/review_package_20261023_172944Z`  
**Total Additions:** 19 files  

| Relative Path | Purpose | Public Release Suitable | Sensitive / Machine-Specific Content | Action |
|---|---|---|---|---|
| `tables/input_map.csv` | Comprehensive map of all 38 inspected inputs with hashes, selectors, and categories | Yes | None | Commit with review package |
| `tables/descriptive_statistics.csv` | Full descriptive statistics (mean, SD, SE, min, max) for all 5 key vectors | Yes | None | Commit with review package |
| `tables/uncertainty_claim_reconciliation.csv` | Reconciliation table evaluating historical SE claims against empirical values | Yes | None | Commit with review package |
| `tables/statistical_results.csv` | Complete 3-comparison retrospective family testing results | Yes | None | Commit with review package |
| `tables/holm_verification.csv` | Step-by-step Holm-Bonferroni independent calculation and verification | Yes | None | Commit with review package |
| `tables/seed_direction_checks.csv` | Seed-by-seed verification of Claim A (16/4) and Claim B (20/0) | Yes | None | Commit with review package |
| `reports/input_scope.md` | Report detailing input boundaries, schemas, and allow_pickle safety | Yes | None | Commit with review package |
| `reports/uncertainty_verification.md` | Report documenting sample SD/SE derivations and rejecting proposed SE claims | Yes | None | Commit with review package |
| `reports/statistical_family.md` | Report documenting the 3-comparison family, Wilcoxon call, and Holm adjustment | Yes | None | Commit with review package |
| `reports/claim_separation.md` | Report separating Claim A (FQ vs PQK2) from Claim B (Full vs Intercept) | Yes | None | Commit with review package |
| `reports/CORRECTION_RECORD_T6.md` | Superseding correction record establishing official audit corrections | Yes | None | Commit with review package |
| `reports/CONTRIBUTOR_REVIEW.md` | Instructions and sign-off template for independent human contributor | Yes | None | Commit with review package |
| `reports/manuscript_claim_map.csv` | Mapping linking draft LaTeX sentences directly to verified data rows | Yes | None | Commit with review package |
| `reports/PROPOSED_FILE_INVENTORY.md` | Inventory of all newly generated files and release readiness | Yes | None | Commit with review package |
| `reports/REVIEW_PACKAGE_STATUS.md` | Executive summary of completed checks, blockers, and next human actions | Yes | None | Commit with review package |
| `scripts/reviewer_checks.py` | Standalone, read-only executable reviewer helper executing all 7 checks | Yes | Local filesystem paths in root | Commit with review package |
| `scripts/build_review_package.py` | Master builder script driving the entire review package generation | Yes | Local path references | Commit with review package |
| `proposed_paper/t6_results.tex` | Draft LaTeX prose adhering to negative wording constraints (DO NOT APPLY) | Yes | None | Do NOT commit to paper/ until signed |
| `proposed_paper/t6_statistics_table.tex` | Draft LaTeX table reflecting reconciled numbers (DO NOT APPLY) | Yes | None | Do NOT commit to paper/ until signed |

> **IMPORTANT:** None of these files have been staged or committed. Paper files in `paper/` remain 100% unaltered.
