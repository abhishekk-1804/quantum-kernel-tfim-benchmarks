# Stage 2A Post-Edit Integrity Report

**Execution Timestamp (UTC):** `20261101_090455Z`  
**Baseline Git HEAD:** `292d689dd845f6228fae6265cffe83b81d5f0f66`  
**Target Manifest Checked:** `docs/finalization/20261101_082313Z/00_FILE_MANIFEST.csv`  
**Total Manifest Entries Checked:** 28  
**Expected Changed Files:** 4 (paper/main.tex, paper/references.bib, paper/tables/tab_equal_budget.tex, paper/tables/tab_ood.tex)  
**Unexpected Changed Files:** 0  
**Missing Manifest Entries:** 0  
**Git-Tracked Files Outside Manifest Scope:** 540 (all remain completely untouched)  
**Integrity Verdict:** PASS - 100% Invariant Preservation  

---

## Detailed Status of Allowlisted Files

| File Path | Stage 0 SHA-256 | Post-Stage-2A SHA-256 | Size Diff (Bytes) | Verdict |
|---|---|---|:---:|:---:|
| `paper/main.tex` | `4b76e3a45f44bdfc...` | `81daddf0906777b7...` | +4448 | **APPLIED & VERIFIED** |
| `paper/references.bib` | `3541c7ff3b45a822...` | `d35a7e4c42585d82...` | -302 | **APPLIED & VERIFIED** |
| `paper/tables/tab_equal_budget.tex` | `28a759698e7e5b19...` | `2573b93cc21f458f...` | +295 | **APPLIED & VERIFIED** |
| `paper/tables/tab_ood.tex` | `43987ffb7555dcd0...` | `39d60c321b53c7ca...` | +1 | **APPLIED & VERIFIED** |

---

## Scientific Inputs and Code Invariance
All protected scientific files (`results/*`, `src/*`, `tests/*`, saved arrays) remained completely untouched and bit-preserved.
