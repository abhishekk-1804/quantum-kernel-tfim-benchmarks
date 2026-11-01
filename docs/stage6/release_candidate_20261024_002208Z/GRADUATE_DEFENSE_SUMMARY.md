# Graduate Research Fellowship Defense Briefs
**Candidate:** Abhishek K. Doddagoudar  
**Project:** Benchmarking Quantum Kernels and Classical Correlator Baselines on Disordered TFIM Chains  
**Target Fellowship Programs:** DAAD (Germany), OIST (Japan), TEEP (Taiwan)  
**Package:** docs/stage6/release_candidate_20261024_002208Z

---

## 1. Executive Research Summary
This research provides a rigorous, controlled empirical and algebraic investigation into the generalization capabilities and resource scaling of quantum kernel algorithms relative to physically matched classical correlator baselines. Utilizing exact numerical diagonalization on open-boundary 1D transverse-field Ising models (TFIM) and frustrated 2D -J_2$ lattices ( \le 14$), the study decouples intrinsic representation geometry from NISQ hardware gate errors.

### Principal Scientific Insights:
1. **Algebraic Equivalence to Classical RBF:** We proved mathematically that single-body (PQK-1) and two-body nearest-neighbor (PQK-2nn) projected quantum kernels on $\mathbb{Z}_2$-symmetric ground states are algebraically identical to classical RBF kernels on local and nearest-neighbor Pauli expectation features, scaled by exact constant factors (/2$ and /4$). Pairwise Gram distance matrices match to numerical machine precision ($|D^2_{\mathrm{RDM}} - D^2_{\mathrm{Pauli}}| \le 1.33 \times 10^{-15}$).
2. **Measurement Shot Budget Inversion:** Under equal total measurement shot budgets ({\mathrm{tot}} \in [10^5, 10^7]$), projected feature kernels achieve substantially superior sample efficiency compared to fidelity quantum kernels (FQ). At {\mathrm{tot}}=10^6$, PQK-2nn achieves test ^2 = 0.9575 \pm 0.0026$ while FQ attains only .8288 \pm 0.0067$ ($\Delta R^2 = -0.1287 \pm 0.0067$). At {\mathrm{tot}} \le 30{,}000$, FQ circuits are excluded under minimum-shot constraints ({\mathrm{swap}} < 10$).
3. **Controlled Phase-Shift Out-of-Distribution Generalization:** Under a severe out-of-distribution distribution shift across the TFIM quantum phase transition ( \in [0.8, 1.5]$ paramagnetic $\to [0.2, 0.7]$ ferromagnetic), fidelity kernels on ideal noiseless statevectors achieve significantly lower Mean Absolute Error than projected feature models (.0602 \pm 0.0085$ vs .1850 \pm 0.0294$, paired $\Delta\mathrm{MAE} = -0.1248 \pm 0.0334$, Wilcoxon =21.0$,  = 8.51 \times 10^{-4}$).
4. **Finite-Shot Non-Positive Semidefiniteness:** Under simulated destructive swap tests with finite shots, 100% of unmitigated fidelity Gram matrices (20/20 seeds) become indefinite ($\lambda_{\min} < 0$), causing catastrophic SVR breakdown unless stabilized by spectral PSD eigenvalue clipping.

---

## 2. Fellowship-Specific Technical Defense Briefs

### Brief A: DAAD Research Fellowship (Germany)
*Targeting:* Quantum Information & Condensed Matter Theory Groups (e.g., MPQ Garching, LMU Munich, TU Munich, FZ Jülich).

- **Theoretical & Methodological Grounding:**
  Emphasizes algebraic transparency and mathematical rigor. The project directly addresses fundamental questions in quantum machine learning: what represents genuine quantum feature encoding versus classical observable regression? By establishing the exact Frobenius identity connecting 2-qubit reduced density matrix distances to Pauli expectation differences, the work demonstrates that PQK models do not operate in an abstract, inaccessible Hilbert space, but rather in a low-dimensional manifold spanned by local physical correlators.
- **Protocol Pre-Declaration & Open Science:**
  In alignment with German standards of scientific integrity, all primary confirmatory hypotheses were evaluated under a pre-declared statistical protocol with two-sided Wilcoxon signed-rank tests and Holm family-wise error rate control ({\mathrm{Holm}}$). Stage 2 and Stage 3 retrospective investigations are transparently classified as exploratory, preventing post-hoc confirmation bias.
- **Future Integration:**
  Provides a solid foundation for research into tensor network methods (MPS/PEPS) and non-equilibrium quantum dynamics in German collaborative research centers (SFBs).

---

### Brief B: OIST Research Internship / Graduate Defense (Japan)
*Targeting:* Strongly Correlated Systems, Quantum Dynamics, and Statistical Physics Units.

- **Condensed Matter & Quantum Phase Transitions:**
  Addresses quantum critical phenomena in the 1D transverse-field Ising chain and frustrated 2D antiferromagnets (-J_2$). The out-of-distribution benchmark evaluates inductive transfer across quantum critical points, where divergent correlation lengths and symmetry breaking fundamentally restructure ground-state entanglement.
- **Handling Non-Standard Evaluation Regimes:**
  When standard regression metrics fail under severe distribution shifts (^2 < 0$), our work rigorously diagnoses the breakdown, replaces ^2$ with Mean Absolute Error (MAE), and demonstrates genuine inductive physical signal via intercept-only baseline ablation ($-0.4014 \pm 0.0156$ MAE improvement,  = 1.91 \times 10^{-6}$).
- **Clarity on Limitations:**
  Frankly delineates the boundary between noiseless statevector simulations and experimental reality, noting that FQ's OOD extrapolation advantage has only been confirmed on ideal statevectors and remains to be demonstrated under finite measurement sampling.

---

### Brief C: TEEP Fellowship / Practical Quantum Systems (Taiwan)
*Targeting:* Quantum Computing Initiatives (e.g., Academia Sinica, National Taiwan University, ITRI).

- **Hardware-Aware Quantum Computing & NISQ Realism:**
  Focuses on the direct physical and financial cost of quantum circuit execution. The project demonstrates that global state overlap estimation via destructive swap tests incurs a prohibitive .2\times$ to .8\times$ measurement shot overhead relative to local Pauli observable estimation.
- **Mitigation of Physical Noise Channels:**
  Investigates local depolarizing noise channels ($\mathcal{E}(\rho) = (1-p)\rho + p(I/2)\text{Tr}(\rho)$) and demonstrates that adaptive bandwidth retuning via inner cross-validation successfully absorbs uniform feature shrinkage, maintaining model fidelity up to =0.08$.
- **Software Engineering & Benchmarking Architecture:**
  Demonstrates mastery of scalable Python/NumPy/SciPy quantum simulation pipelines, automated statistical auditing, and reproducible research workflows ready for deployment on hybrid quantum-classical hardware.

---

## 3. Defense Audit & Technical Rigor Matrix

| Technical Criterion | Project Implementation & Verification Evidence |
|---|---|
| **Data Integrity** | Cryptographic SHA-256 verification on all raw results; 100% bit-level immutability across all benchmark CSVs. |
| **Statistical Power** | 20 independent fixed seeds; two-sided Wilcoxon signed-rank tests; Holm step-down multiple-testing correction. |
| **Cell Synchronization** | 49 out of 49 Stage 2 budget cells and 20 out of 20 Stage 3 paired MAE vectors independently reproduced from raw observations. |
| **Ablation Testing** | Full model vs train-mean and train-median intercept baselines; classical Linear Ridge descriptive baselines. |
| **Negative Scope Control** | Explicitly precluding claims of quantum advantage, non-equilibrium dynamics, or noisy OOD superiority. |

---

## 4. Personal Contributions of Abhishek K. Doddagoudar
1. **Core Simulation Engine:** Developed the exact sparse Hamiltonian generation and Lanczos diagonalization algorithms for 1D TFIM and 2D -J_2$ spin models.
2. **Mathematical Proofs:** Formulated and verified the Frobenius distance identities mapping PQK-1 and PQK-2nn directly to RBF kernels on local and nearest-neighbor Pauli observables.
3. **Hardware Noise & Measurement Models:** Implemented the finite-shot binomial swap-test simulator, PSD eigenvalue clipping routines, and local depolarizing quantum channels.
4. **Reproducible Research Infrastructure:** Architected the end-to-end audit and release framework, ensuring programmatic synchronization between raw data CSVs and publication LaTeX tables with zero manual transcription.
