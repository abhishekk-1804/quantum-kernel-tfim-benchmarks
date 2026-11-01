# STAGE 4 STATUS: Evidence, Provenance, and Readiness Inventory
**Workspace:** `D:\quantum-kernel-tfim-benchmarks`  
**Package:** `docs/stage4/readiness_20261023_180339Z/`  
**Generated:** 2026-10-23 18:20:37Z  
**Classification:** Status and readiness inventory; not an assertion of project completion.

---

## 1. Executive Summary & Governance Stance
This readiness package consolidates the experimental evidence, audit trail, and verification artifacts accumulated across Stages 0, 1, 1b, 2, and 3. In strict compliance with project governance rules:
- **No manuscript modifications** have been applied to `paper/` or `paper/main.tex`.
- **No automated checks constitute human review:** All findings remain classified as *Awaiting Independent Human Review*.
- **No arbitrary completion percentage** is assigned: Progress is measured by the concrete verification status of specific artifacts, items, and tests.
- **Pre-existing files remain strictly read-only:** All new artifacts reside exclusively in `docs/stage4/readiness_20261023_180339Z/`.

---

## 2. Git Baseline and Tracking Discrepancies

A critical discovery of this audit is the discrepancy between the historical target commit `dff0171` and the current `HEAD` commit `292d689`:

| Asset Group | Tracked at `dff0171` | Tracked at `HEAD` (`292d689`) | Current On-Disk Status | Portability Implication |
| :--- | :---: | :---: | :---: | :--- |
| **Stage 0/1 Baselines** (`results/t1_*.csv`, `results/stats.csv`) | YES | YES | Tracked | Portable across fresh clones |
| **Stage 2 Equal-Budget** (`results/stage2/t1_equal_budget.csv`) | YES | YES | Tracked | Committed in `dff0171` |
| **Stage 3 OOD Generalization** (`results/stage3/t6_ood_shift.csv`) | **NO** | YES | Tracked | Missing at `dff0171`; present at `HEAD` |
| **Saved Raw Prediction Arrays** (`docs/.../predictions/seed_*.npz`) | **NO** | **NO** | **UNTRACKED** | **Not available in fresh clone without bundle** |
| **Audit Verification Packages** (`docs/verification/*`) | **NO** | **NO** | **UNTRACKED** | Local forensic artifacts |

> [!WARNING]
> **Critical Portability Limitation:** Because the 20 raw prediction array files (`seed_00_arrays.npz` through `seed_19_arrays.npz`, total ~2.9 MB) are untracked, a fresh clone of the repository at either `dff0171` or `292d689` cannot execute bit-level array spot-checks without an external review bundle.

---

## 3. Evidence Inventory Breakdown
The evidence inventory ([`evidence_inventory.csv`](file:///d:/quantum-kernel-tfim-benchmarks/docs/stage4/readiness_20261023_180339Z/tables/evidence_inventory.csv)) contains **46 cataloged artifacts**:
- **Original Experiment Outputs (10 items):** Pinned CSV records from Stage 0 through Stage 3.
- **Saved Replay Artifacts (20 items):** Per-seed `.npz` archives containing ground-truth targets, SVR dual coefficients, intercepts, and prediction vectors.
- **Derived Audit Tables (6 items):** Cross-reconciliation tables, descriptive statistics, Wilcoxon tests, and Holm calculations.
- **Narrative Reports & Governance (10 items):** Charters, protocols, issue registers, and manuscript audit reports.

---

## 4. Human-Reviewed Findings vs Findings Awaiting Review

### 4.1 Human-Reviewed Findings: NONE (0)
No human contributor or external reviewer has signed off on the experimental results or audit conclusions. All automated tests executed to date constitute **local readiness checks**, not independent approvals.

### 4.2 Findings Awaiting Independent Human Review:
1. **Task 6 OOD Generalization Advantage:** Superiority of Full Quantum (FQ) over Projected Quantum Kernel (PQK-2nn) under severe Hamiltonian parameter shift ($W = 21.0$, $p = 8.51 \times 10^{-4}$, Holm-adjusted $p = 8.51 \times 10^{-4}$).
2. **Directional Separation of Claims A & B:** 
   - Across models: FQ achieves lower MAE in 16 seeds, while PQK-2nn achieves lower MAE in 4 seeds (Seeds 8, 9, 11, 16). The claim "FQ lower in all 20 seeds" is contradicted.
   - Within FQ model: Full SVR achieves lower MAE than the constant intercept baseline in 20 out of 20 seeds (100%).
3. **Empirical Standard Errors:** Correction of historical sample SE claims ($\pm 0.0039 \to 0.0085$ for FQ; $\pm 0.0154 \to 0.0294$ for PQK-2nn; $\pm 0.0166 \to 0.0334$ for paired difference).
4. **Stage 2 Equal-Budget Crossover Absence:** Lack of sample efficiency crossover between FQ and PQK-2nn under total measurement shot budgets up to $B_{\text{tot}} = 10^5$.
5. **Manuscript Items M1–M7:** Formal definitions and required manuscript qualifications documented in `docs/stage1b/manuscript_items.md`.
6. **Open Questions Register R1–R3:** Methodological resolutions for bandwidth grid parameterization (R1), null observable basis allocation (R2), and asymmetric PSD clipping (R3).

---

## 5. Formal Definitions of Manuscript Items M1–M7
As verified from `docs/stage1b/manuscript_items.md` and `scripts/audit_manuscript_items.py`:
- **M1:** Bound `\le 0.011` (Claim C2) vs All Confirmatory Rows ($N \ge 80$). Seven confirmatory rows exceed this bound; the manuscript must clarify that the bound applies strictly to Task 1 at $N=160$ or specific top-performer comparisons.
- **M2:** Treatment of E2(raw) and PQK-2nn as Separate Arms. Proven identical in representation up to normalizer scaling ($B == C$); 17 manuscript locations require qualification.
- **M3:** Epistemic Keywords Occurrences. Removal of overclaiming terms (e.g., "proves", "guarantees") in favor of empirical descriptions.
- **M4:** Statements on FQ-clipped / PSD Clipping Recovery. Accurate reporting that PSD clipping stabilizes training Gram matrices but leaves rectangular test blocks unclipped.
- **M5:** Parity/Reality Statements in Section II. Exact physical formulation of $Z_2$ ground-state symmetry.
- **M6:** Shot-Cost Numbers Audit. Verification of shot scaling factors (480, 720, 8780, 28680, 12.2x, 39.8x).
- **M7:** Table I and Table II Numbers vs Results CSV Values. Verification of all printed LaTeX numbers against results CSV data.
