# Project Charter: Classical Correlator Baselines vs. Quantum Kernels on Spin-Chain Ground States

## 1. Research Question
"When do low-order correlator representations retain the predictive information of fidelity kernels, and how does their performance change under a matched measurement budget and a controlled distribution shift?"

---

## 2. Scope
The project investigates the empirical and theoretical boundary between quantum kernel architectures—specifically single-body projected quantum kernels (PQK-1), nearest-neighbour two-body projected quantum kernels (PQK-2nn), and global fidelity quantum kernels (FQ)—and matched classical correlator baselines (e.g., Ridge regression on 2-body observables, RBF kernels on raw and standardized Pauli expectations).

The physical models comprise:
1. 1D Transverse-Field Ising Models (TFIM) with open and periodic boundary conditions, uniform and disordered transverse fields ($n \le 14$).
2. 2D Frustrated $J_1$-$J_2$ lattices ($2 \times 4$ and $3 \times 4$ geometries).

Evaluation targets include:
- Half-chain entanglement entropy ($S_{n/2}$).
- Contained 2-point correlators ($\langle Z_0 Z_{n-1} \rangle$) and non-contained 4-point correlators ($\langle Z_0 Z_1 Z_{n-2} Z_{n-1} \rangle$).
- Frustrated lattice ground-state phase classification and ground-state energy regression.
- Kernel concentration scaling ($n \in \{4, 6, 8, 10, 12, 14\}$).
- Finite measurement shot scaling (destructive swap test vs. commuting Pauli basis pooling).
- Local per-qubit depolarizing noise channels with retuned and fixed hyperparameters.

---

## 3. Work Packages
- **WP-1 Lead:** Protocol governance, state and Hamiltonian validation, claim ledger maintenance, repository integration, manuscript synthesis.
- **WP-2 Theory:** Parity symmetry constraints vs. reality, formal algebraic identities for PQK-1 and PQK-2nn, graph vertex degree weighting derivations.
- **WP-3 Statistics and Baselines:** Pre-declared protocol enforcement, data leakage audit, comparison registry, family-wise error rate control (Holm step-down), bootstrap confidence intervals.
- **WP-4 Measurement:** Observable-to-setting grouping manifest, equal-shot-budget benchmarking, swap-test eigenvalue thresholding (PSD spectral clipping).
- **WP-5 Optional Independent Validation:** Independent replication and clean-room verification (activated only with substantive independent work).

---

## 4. Cross-Review Pairs
To maintain methodological rigor and eliminate blind spots, work packages are paired for mutual cross-review:
- **WP-1 $\longleftrightarrow$ WP-2** (Lead $\longleftrightarrow$ Theory)
- **WP-3 $\longleftrightarrow$ WP-4** (Statistics $\longleftrightarrow$ Measurement)

---

## 5. Quality Gates
Quality gates enforce strict sequential gating. No dependent main experiment starts before its preceding gate passes; documentation, exploratory pilots, and test scaffolding may proceed in parallel:
- **G0 (Foundations & Baseline):** Baseline runs cleanly and is fully reproduced; integration tests pass with zero errors.
- **G1 (Methodological Parity & Integrity):** No unresolved issues or discrepancies that could alter the central empirical comparisons.
- **G2 (Equal-Budget Reproducibility):** Equal-budget measurement results regenerate deterministically from versioned exports.
- **G3 (Distribution Shift Protocol):** Distribution shift experiment run exactly once per its frozen, committed protocol.
- **G4 (Independent Reproduction):** Clean reproduction of core pipelines on an isolated environment.
- **G5 (Skeptical Read):** Adversarial peer review probing limitations, edge cases, and threats to validity.
- **G6 (Submission-Ready):** Manuscript, tables, figures, code, and replication artifacts verified as submission-ready.

---

## 6. Authorship Rule
Authorship is governed strictly by substantive intellectual contribution, active drafting or critical revision of the manuscript, and final approval and accountability for the submitted work.
- Decided at manuscript freeze based on verified contribution, never by advance promise.
- Rigorous negative/null results and the discovery of central methodological flaws count fully as substantive intellectual contributions.

---

## 7. Effort and Availability
- "Estimated 560-750 focused person-hours across four contributors; weekly availability recorded separately; revised after Gate 0."
- Target start date: 26 Oct 2026. Dates represent internal targets only and are rescheduled whenever a gate fails. External program deadlines are strictly omitted.

---

## 8. Scope Rules
1. **Exploratory vs. Confirmatory Separation:** Pilot work is explicitly exploratory. Main-evaluation protocols must be committed (with the git commit hash recorded in the protocol registry) after pilot exploration and prior to executing main evaluation runs.
2. **Immutable Empirical Records:** Historical results in `results/*.csv` are immutable archives. Correction reruns or ablations must output to versioned files (`results/v2/...`).
3. **Fail-Closed Gate Enforcement:** If a gate condition is unmet, execution halts immediately; no downstream experimental data is accepted without passing the gate.

---

## 9. Out-of-Scope List
The following domains are explicitly out of scope for this investigation:
- Variational quantum circuits (VQC) and parameterized ansatz optimization (ground states are obtained via exact numerical diagonalization to isolate kernel geometry).
- Non-equilibrium quantum dynamics, chaotic time evolution, and Floquet systems.
- Topological spin liquids or long-range ordered topological phases with non-local string order parameters.
- Synthetic quantum data or cryptographically engineered datasets constructed intentionally to foil classical polynomial-time estimators.
- Pulse-level quantum hardware synthesis and physical device calibration drift.
