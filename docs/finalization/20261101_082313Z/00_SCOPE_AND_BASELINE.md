# Stage 0: Scope and Baseline Specification

**Timestamp (UTC):** `2026-11-01T08:23:13Z`  
**Execution Environment:** Windows PowerShell, `D:\qml_env\Scripts\python.exe -B` (`PYTHONDONTWRITEBYTECODE=1`)  
**Git HEAD:** `292d689dd845f6228fae6265cffe83b81d5f0f66`  
**Audit Output Directory:** `docs/finalization/20261101_082313Z/`  
**File Manifest:** [`00_FILE_MANIFEST.csv`](file:///d:/quantum-kernel-tfim-benchmarks/docs/finalization/20261101_082313Z/00_FILE_MANIFEST.csv)  

---

## 1. Baseline Git State

### `git status --short`:
```
M paper/main.tex
 M paper/references.bib
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

### Uncommitted Modification Summary:
- `paper/main.tex`: 57 insertions, 16 deletions from earlier integration sessions.
- `paper/references.bib`: 22 insertions adding Shaydulin2022 and Canatar2023.
- All untracked directories (`docs/stage4/`, `docs/stage5/`, `docs/stage6/`, `docs/verification/`) are protected audit/reconciliation evidence and will remain untouched.

---

## 2. Invariant Rules & Protected Scientific Inputs

1. **Strictly Read-Only Files:**
   - Raw benchmark results: `results/*.csv` (including `results/stage2/` and `results/stage3/`).
   - Saved numerical state/prediction arrays: `docs/verification/*/predictions/*.npz`, `representation_reference_arrays.npz`.
   - Core computational physics code: `src/*.py`, `tests/*.py`.
   - Prior audit and reconciliation evidence: `docs/stage5/audit_20261101/*`, `docs/stage4/*`, `docs/verification/*`.
2. **Prohibited Actions:**
   - Zero git staging (`git add`), commits, pushes, checkouts, stashes, resets, or cleans.
   - Zero new physical quantum simulations, exact eigensolves, Trotterizations, or shot draws.
   - Zero author approvals, contributor sign-offs, or venue submissions on behalf of humans.
3. **Proposed Editable Files:**
   - `paper/main.tex`: Update narrative, equations, data corrections, and statistical phrasing.
   - `paper/references.bib`: Remove duplicate `Shaydulin2022importance` entry.
   - `paper/tables/tab_equal_budget.tex`: Fix 101.68 pt Overfull `\hbox` by adjusting padding and header wrapping.
   - `paper/tables/tab_ood.tex`: Harmonize notes to designate Stage 3 as retrospective/exploratory.

---

## 3. Project Configuration & Inspection

- **Manuscript Entry Point:** `paper/main.tex` (IEEEtran document class, pdflatex + bibtex backend).
- **Included Table Targets:**
  * `paper/tables/tab1_t1_r2.tex` (Task 1 sample efficiency)
  * `paper/tables/tab2_confirmatory_stats.tex` (Task 1 confirmatory Wilcoxon tests)
  * `paper/tables/tab4_grid_boundaries.tex` (Hyperparameter tuning bounds)
  * `paper/tables/tab_equal_budget.tex` (Stage 2 budget scaling - requires overfull hbox fix)
  * `paper/tables/tab_ood.tex` (Stage 3 OOD phase-shift generalization)
- **Included Graphics:**
  * `paper/figures/fig_learning_curve_t1.pdf` (from `results/t1_entropy_gridv3.csv`)
  * `paper/figures/fig_shots.pdf` (from `results/t5_noise.csv`)
  * `paper/figures/fig_depolarizing_retuned_per_qubit_proxy.pdf` (from `results/t5_noise.csv`, `results/t5_depol_fixedhp.csv`)
- **Build Backend:** `pdflatex` + `bibtex`.
