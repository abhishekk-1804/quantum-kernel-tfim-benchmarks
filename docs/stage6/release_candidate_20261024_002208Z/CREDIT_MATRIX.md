# CRediT (Contributor Roles Taxonomy) Authorship Matrix

**Project:** Benchmarking Quantum Kernels and Classical Correlator Baselines on Disordered TFIM Chains  
**Release Candidate:** 
elease_candidate_20261024_002208Z  
**Standard:** [ANSI/NISO Z39.104-2022 CRediT](https://credit.niso.org/)

---

## Contributor Roles Overview

| Contributor | Affiliation / Role | Status |
|---|---|---|
| **Abhishek K. Doddagoudar** | Presidency University, Bengaluru | Primary Investigator & Lead Developer |
| **Contributor C2** | Independent Verification / Peer | Theory & Protocol Reviewer |
| **Contributor C3** | Independent Verification / Peer | Numerical & Experimental Architecture Reviewer |
| **Contributor C4** | Independent Verification / Peer | Verification Tooling & Environment Reviewer |
| **Contributor C5** | Independent Verification / Peer | Independent Artifact & Table Replication Auditor |

---

## Detailed CRediT Activity Matrix

| CRediT Category | Abhishek K. Doddagoudar | Contributor C2 | Contributor C3 | Contributor C4 | Contributor C5 |
|---|:---:|:---:|:---:|:---:|:---:|
| **Conceptualization** | Lead | Supporting | Supporting | — | — |
| **Methodology** | Lead | Supporting | Supporting | — | — |
| **Software** | Lead | — | — | Supporting | — |
| **Validation** | Supporting | Supporting | Supporting | Supporting | Lead |
| **Formal Analysis** | Lead | Supporting | — | — | Supporting |
| **Investigation** | Lead | — | Supporting | — | — |
| **Resources** | Lead | — | — | — | — |
| **Data Curation** | Lead | — | — | — | Supporting |
| **Writing - Original Draft** | Lead | — | — | — | — |
| **Writing - Review & Editing** | Lead | Supporting | Supporting | Supporting | Supporting |
| **Visualization** | Lead | — | Supporting | — | — |
| **Supervision** | Lead | — | — | — | — |
| **Project Administration** | Lead | — | — | — | — |

---

## Specific Contribution Statements

- **Abhishek K. Doddagoudar (Lead Author):** Formulated research hypothesis, implemented sparse Hamiltonian diagonalization routines for 1D TFIM and 2D -J_2$ lattices, developed the end-to-end kernel evaluation pipeline (FQ, PQK-1, PQK-2nn, classical correlators), proved the exact Frobenius norm algebraic equivalence of PQK-1 and PQK-2nn with Pauli expectation RBF kernels, implemented local depolarizing noise channels and swap-test finite measurement shot simulations, conducted all primary empirical sweeps (Tasks 1--6), generated publication figures and tables, and drafted the manuscript.
- **Contributor C2 (Theory & Protocol Review):** Reviewed theoretical derivation of the $\mathbb{Z}_2$ symmetry constraints on reduced density matrices; validated pre-declared statistical testing protocol (two-sided Wilcoxon signed-rank tests with Holm family-wise error rate control).
- **Contributor C3 (Experimental Architecture Review):** Reviewed out-of-distribution (OOD) phase-shift experimental design ( \in [0.8, 1.5] 	o [0.2, 0.7]$); audited hyperparameter search grids and cross-validation splitting protocols.
- **Contributor C4 (Tooling & Verification Infrastructure):** Designed portable artifact bundle specification and automated checksum validation scripts for cross-platform replication.
- **Contributor C5 (Independent Replication Audit):** Executed independent cell-level and table-level verification across all 49 Stage 2 budget cells and 20 Stage 3 paired MAE vectors, confirming zero discrepancy between raw CSV results and manuscript tables.
