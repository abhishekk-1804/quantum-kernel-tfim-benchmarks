# Stage 2 Source-to-Table Synchronization Report
**Directory:** `docs/stage5/stage2_sync_20261023_231851Z/`  
**Execution Timestamp:** 2026-10-24 04:52:00 UTC  
**Workspace:** `D:\\quantum-kernel-tfim-benchmarks`  
**Interpreter:** `D:\\qml_env\\Scripts\\python.exe`

---

## 1. Executive Summary

This report performs an independent mathematical and provenance audit tracing Stage 2 equal-total-budget metrics from primary machine-readable records to downstream tables.

### Key Audit Conclusions:
1. **Mathematical Invariance (Original CSV -> Exported Cells):**
   - The primary record `results/stage2/t1_equal_budget.csv` contains exactly **980 rows** (7 budgets $\\times$ 7 model arms $\\times$ 20 seeds).
   - Exactly one valid observation exists per seed for each cell. There are **zero duplicate seeds**, **zero missing seeds**, and **zero unhandled folds**.
   - Independent re-aggregation demonstrates **100% numerical agreement** (difference $< 10^{-12}$) with the exported cell table `docs/stage5/source_reconciliation_20261023_225751Z/stage2_verified_cells.csv` across all 49 cells.
2. **LaTeX Generation Invariance (Exported Cells -> Proposed LaTeX):**
   - The proposed table `proposed_tab_equal_budget.tex` matches the independently aggregated metrics identically to 4 decimal places.
3. **Disputed Narrative Numbers (0.9575 vs 0.9582, 0.8288 vs 0.7241, -0.0984 vs 0.0811, 0.4723 vs 0.1045):**
   - In all primary repository artifacts (`results/stage2/t1_equal_budget.csv`, `docs/stage2/equal_budget_summary.md`, `paper/tables/tab_equal_budget.tex`), the true sample means are:
     * $B=1\\text{M}$, PQK-2nn: **0.9575** ($0.957497 \\pm 0.002629$)
     * $B=1\\text{M}$, FQ (train_only): **0.8288** ($0.828752 \\pm 0.006686$)
     * $B=100\\text{k}$, FQ (none, raw unclipped): **-0.0984** ($-0.098386 \\pm 0.084581$)
     * $B=100\\text{k}$, FQ (inductive repair): **0.4723** ($0.472292 \\pm 0.032065$)
   - The alternative numbers (`0.9582`, `0.7241`, `0.0811`, `0.1045`) **do not exist as Stage 2 cell aggregates** in any repository artifact. Per strict audit protocol, they are formally classified as **"Origin not established"** (they may reflect single-seed values or external typographical errors).

---

## 2. Input Cryptographic Verification

| Input File | Pre-Analysis SHA-256 | Post-Analysis SHA-256 | Status |
| :--- | :--- | :--- | :---: |
| `results/stage2/t1_equal_budget.csv` | `22d66cd6e27372a53936b7d7aa4d9317878367aefebc0560a8be0a6bbbf955bd` | `22d66cd6e27372a53936b7d7aa4d9317878367aefebc0560a8be0a6bbbf955bd` | Preserved (Read-Only) |
| `docs/stage5/source_reconciliation_20261023_225751Z/stage2_verified_cells.csv` | `d0b5bc21b6a33374ff3740075b19f4fdcf97eb1051f2dab82ed692a68e79d63a` | `d0b5bc21b6a33374ff3740075b19f4fdcf97eb1051f2dab82ed692a68e79d63a` | Preserved (Read-Only) |
| `docs/stage5/source_reconciliation_20261023_225751Z/proposed_tab_equal_budget.tex` | `00db65e63150dab1105f6f82122019223ff5cd640ba2885e0f2e60ed8e044a7d` | `00db65e63150dab1105f6f82122019223ff5cd640ba2885e0f2e60ed8e044a7d` | Preserved (Read-Only) |

---

## 3. Disputed Cell Comparison & Root Cause Classifications

| Cell Selector | Independent Mean | Independent SE | Previous Export | LaTeX String | Disputed Value | Link Where Disagreement Occurs | Forensic Classification & Evidence |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `B=1M, PQK-2nn, none` | 0.9575 | 0.0026 | 0.9575 | `0.9575 \\pm 0.0026` | 0.9582 | Link D | **Origin not established.** Source CSV mean across all 20 seeds is 0.957497 (SE 0.0026). Single seed 5 has $R^2=0.958230$, but no aggregate table reports 0.9582. |
| `B=1M, FQ, train_only` | 0.8288 | 0.0067 | 0.8288 | `0.8288 \\pm 0.0067` | 0.7241 | Link D | **Origin not established.** Source CSV mean across all 20 seeds is 0.828752 (SE 0.0067). No Stage 2 artifact reports 0.7241. |
| `B=100k, FQ, none` | -0.0984 | 0.0846 | -0.0984 | Supporting arm | 0.0811 | Link D | **Origin not established.** Source CSV mean is -0.098386 (SE 0.0846). 0.0811 appears only as an RMS metric in Stage 3 closure reports, never as an $R^2$ aggregate. |
| `B=100k, FQ, inductive` | 0.4723 | 0.0321 | 0.4723 | Supporting arm | 0.1045 | Link D | **Origin not established.** Source CSV mean is 0.472292 (SE 0.0321). 0.1045 appears only in Task 4 frustration archives, never in Stage 2. |

---

## 4. Pipeline Trace Across the Four Links

### Link A: Original CSV $\\rightarrow$ Newly Aggregated Cells
- **Evaluation:** For each of the 49 experimental cells, the subset was filtered on `(B_tot, model, variant)`.
- **Row Key Integrity:** Exactly 20 unique seeds (`seed \in [0..19]`) were verified for each cell.
- **Exclusion Policy:** For $B_{\\mathrm{tot}} \\in \\{10000, 30000\\}$ and all 3 FQ variants, `is_feasible == False`, $S_{\\mathrm{swap}} = 0$, and status is recorded as *"Excluded under minimum-shot policy"*.
- **Verdict:** **Identical** (Zero discrepancies).

### Link B: Newly Aggregated Cells $\\rightarrow$ `stage2_verified_cells.csv`
- **Evaluation:** Cell-by-cell numerical difference $|\\mu_{\\mathrm{new}} - \\mu_{\\mathrm{prev}}|$ and $|\\text{SE}_{\\mathrm{new}} - \\text{SE}_{\\mathrm{prev}}|$.
- **Verdict:** **Identical** (Max absolute difference $< 10^{-15}$ across all 49 cells).

### Link C: `stage2_verified_cells.csv` $\\rightarrow$ `proposed_tab_equal_budget.tex`
- **Evaluation:** Verification that LaTeX cells match `f"{val:.4f} \\pm {se:.4f}"`.
- **Verdict:** **Identical** / **Formatting-only difference** (standard rounding to 4 decimal places).

### Link D: `proposed_tab_equal_budget.tex` $\\rightarrow$ Earlier Narrative Text
- **Evaluation:** Checking whether repository drafts or narrative texts disagree with the verified tables.
- **Finding:** Existing repository summary `docs/stage2/equal_budget_summary.md` and LaTeX table `paper/tables/tab_equal_budget.tex` display **0.9575**, **0.8288**, **-0.0984**, and **0.4723**, which are in 100% agreement with the primary CSV.
- **Verdict on Disputed Values:** **Origin not established** for the external numbers (`0.9582`, `0.7241`, `0.0811`, `0.1045`).

---

## 5. Deliverables in Package

1. [`independent_stage2_cells.csv`](file:///D:/quantum-kernel-tfim-benchmarks/docs/stage5/stage2_sync_20261023_231851Z/independent_stage2_cells.csv): Complete independent re-aggregation across all 49 cells.
2. [`cell_comparison.csv`](file:///D:/quantum-kernel-tfim-benchmarks/docs/stage5/stage2_sync_20261023_231851Z/cell_comparison.csv): Four-link audit trace and agreement classification for every cell.
3. [`proposed_tab_equal_budget.tex`](file:///D:/quantum-kernel-tfim-benchmarks/docs/stage5/stage2_sync_20261023_231851Z/proposed_tab_equal_budget.tex): Programmatically generated table from independent cells.
4. [`SYNC_REPORT.md`](file:///D:/quantum-kernel-tfim-benchmarks/docs/stage5/stage2_sync_20261023_231851Z/SYNC_REPORT.md): This comprehensive verification report.

---
*Generated programmatically with zero manual number editing.*
