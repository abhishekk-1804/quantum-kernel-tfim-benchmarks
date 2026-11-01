# Pre-Stage-2 Snapshot and State Specification

**Execution Timestamp (UTC):** `20261101_083948Z`  
**Git HEAD:** `292d689dd845f6228fae6265cffe83b81d5f0f66`  
**Workspace:** `D:\quantum-kernel-tfim-benchmarks`  
**Diagnostic Output Directory:** `docs/finalization/20261101_082313Z/stage2_20261101_083948Z/`  
**Pre-Edit Manifest:** [`00_PRE_STAGE2_MANIFEST.csv`](file:///d:/quantum-kernel-tfim-benchmarks/docs/finalization/20261101_082313Z/stage2_20261101_083948Z/00_PRE_STAGE2_MANIFEST.csv)  

---

## 1. Git State Prior to Stage 2 Edits

### `git status --short`:
```
M paper/main.tex
 M paper/references.bib
?? docs/finalization/
?? docs/provenance/
?? docs/stage4/
?? docs/stage5/
?? docs/stage6/
?? docs/verification/
?? paper/tables/tab_equal_budget.tex
?? paper/tables/tab_ood.tex
?? scripts/audit_representation_identity.py
?? scripts/audit_s5_anchors.py
?? scripts/audit_s5_baseline.py
?? scripts/audit_s5_claims_audit.py
?? scripts/audit_s5_distance_check.py
?? scripts/audit_s5_fig_details.py
?? scripts/audit_s5_figures.py
?? scripts/audit_s5_generate_patch_plan.py
?? scripts/audit_s5_generate_reconciliation.py
?? scripts/audit_s5_numerical_claims.py
?? scripts/audit_s5_p1_fig2.py
?? scripts/audit_s5_p2_ood.py
?? scripts/audit_s5_reconciliation.py
?? scripts/audit_s5_reconciliation_p1.py
?? scripts/audit_s5_stage0_stage1.py
?? scripts/audit_s5_stage2_3_chronology.py
?? scripts/audit_s5_statistical_provenance.py
?? scripts/audit_s5_tasks.py
?? scripts/audit_s5_trace_figs.py
?? scripts/audit_stage2_sampling.py
?? scripts/audit_stage3_metrics.py
```

### `git diff --stat`:
```
paper/main.tex       | 57 +++++++++++++++++++++++++++++++++++++---------------
 paper/references.bib | 22 ++++++++++++++++++++
 2 files changed, 63 insertions(+), 16 deletions(-)
```

---

## 2. Allowlisted Files Status (Pre-Edit)

| File Path | Git Status | Size (Bytes) | SHA-256 Hash |
|---|:---:|:---:|---|
| `paper/main.tex` | Tracked (Modified) | 25956 | `4b76e3a45f44bdfc14768362475652374b46a2d5218c8a83dc145d2953853233` |
| `paper/references.bib` | Tracked (Modified) | 2717 | `3541c7ff3b45a822dbd72db6b967cca660d37e760c35201e860062018ddb1ddb` |
| `paper/tables/tab_equal_budget.tex` | Untracked | 2612 | `28a759698e7e5b19c2e0165c7855bd17c55774478b8ed915eae61cd299f00dfb` |
| `paper/tables/tab_ood.tex` | Untracked | 2099 | `43987ffb7555dcd01aec3f4ae527e5ddc2b99e7ea8ff7f02a44e58fdefe15d99` |

Byte-for-byte exact copies of all four allowlisted files have been preserved under:
`docs/finalization/20261101_082313Z/stage2_20261101_083948Z/before/`
