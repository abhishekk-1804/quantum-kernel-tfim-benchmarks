# Projected and Fidelity Quantum Kernels versus Classical Correlator Baselines on Exact Spin-Chain Ground States

[![Tests](https://github.com/abhishek/quantum-kernel-tfim-benchmarks/actions/workflows/tests.yml/badge.svg)](https://github.com/abhishek/quantum-kernel-tfim-benchmarks/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview & Objective Abstract
This repository provides a rigorous, pre-declared empirical benchmark comparing **Projected Quantum Kernels (PQK)**, **Fidelity Quantum Kernels (FQ)**, and **matched classical correlator baselines** for predicting physical properties of quantum spin-chain ground states.

Across 1D transverse-field Ising models (TFIM) and frustrated 2D $J_1$-$J_2$ lattices up to $n \le 14$ spins, quantum states are generated via exact numerical diagonalization, isolating kernel representation geometry from circuit synthesis and variational optimization noise. Evaluated across 20 fixed RNG seeds with two-tiered family-wise error rate control (Holm step-down procedure), the empirical results show:
- Nearest-neighbor projected quantum kernels (`PQK-2nn`) and classical two-body correlator features (`E-raw`) achieve learning accuracy comparable to full fidelity kernels (`FQ`).
- Classical correlator and projected feature models require $12.2\times$ to $39.8\times$ fewer measurement shots than fidelity kernels.
- Under simulated finite-shot swap tests, raw FQ Gram matrices become indefinite ($\lambda_{\min} < 0$) in 100% of seeds, requiring eigenvalue clipping to prevent catastrophic regression failure.
- Under local per-qubit depolarizing noise, models with cross-validation retuning maintain baseline performance, while unmitigated models exhibit predictable signal attenuation.
- **Zero claims of quantum advantage** are made; on equilibrium spin-chain ground states, classical correlator baselines match quantum kernel sample efficiency.

---

## Primary Empirical Results

### Task 1: Half-Chain Entropy Prediction ($n=8$, Test $R^2$, Mean and 95% Bootstrap CI)
Evaluated across 20 fixed seeds on open-chain TFIM ground states:

| Model / Arm | Description | $N_{\text{tr}} = 40$ Mean $R^2$ [95% CI] | $N_{\text{tr}} = 160$ Mean $R^2$ [95% CI] |
| :--- | :--- | :---: | :---: |
| **PQK-1** | Single-body projected kernel ($\equiv$ RBF on $\langle X_i \rangle$) | 0.8986 [0.8847, 0.9111] | 0.9529 [0.9505, 0.9553] |
| **PQK-2nn** | 2-body nearest-neighbor projected kernel | 0.9789 [0.9731, 0.9833] | 0.9943 [0.9936, 0.9950] |
| **FQ** | Pure state fidelity overlap $|\langle \psi \vert \phi \rangle|^2$ | 0.9902 [0.9889, 0.9915] | 0.9975 [0.9972, 0.9978] |
| **E (raw)** | Classical RBF kernel on full 1-body + 2-body correlators | 0.9872 [0.9847, 0.9893] | 0.9987 [0.9986, 0.9989] |
| **E (std)** | Standardized classical RBF kernel | 0.9801 [0.9767, 0.9833] | 0.9965 [0.9961, 0.9969] |
| **E2 (raw)** | Classical RBF on 1-body + NN 2-body correlators | 0.9786 [0.9727, 0.9833] | 0.9942 [0.9935, 0.9950] |
| **F (std)** | Classical Ridge regression ($\ell_2$-linear) | 0.9728 [0.9663, 0.9776] | 0.9887 [0.9878, 0.9894] |

### Confirmatory Paired Hypothesis Tests (Wilcoxon Signed-Rank with Holm Step-Down)
| Task | Target | Pair ($a$ vs $b$) | $N_{\text{tr}}$ | Mean Diff ($a - b$) | 95% Bootstrap CI | $p_{\text{holm}}$ | Interpretation |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **T1** | Half-chain entropy | PQK-1 vs PQK-2nn | 40 | -0.0803 | [-0.0950, -0.0662] | $1.53 \times 10^{-5}$ | PQK-2nn significantly beats PQK-1 |
| **T1** | Half-chain entropy | FQ vs E (raw) | 40 | +0.0031 | [+0.0015, +0.0050] | 0.0012 | FQ leads marginally at $N=40$ |
| **T1** | Half-chain entropy | FQ vs E (raw) | 160 | -0.0012 | [-0.0015, -0.0009] | $1.53 \times 10^{-5}$ | E (raw) leads marginally at $N=160$ |
| **T2b** | 4-point correlator | FQ vs E (raw) | 160 | +0.0000 | [-0.0002, +0.0003] | 1.0000 | Statistically indistinguishable |
| **T2b** | 4-point correlator | PQK-2nn vs E (raw) | 160 | -0.0001 | [-0.0004, +0.0001] | 1.0000 | Statistically indistinguishable |

### Measurement Shot Complexity Comparison ($n=8$, $m=240$ states)
| Model / Arm | Observable Families | Distinct Bases | Deployed Shots ($N_{\text{tr}}=40, N_{\text{te}}=200$) | Full Gram Simulation ($m=240$) |
| :--- | :--- | :---: | :---: | :---: |
| **PQK-1** | $\langle X_i \rangle, \langle Z_i \rangle$ | 2 | $480 \cdot S$ | $480 \cdot S$ |
| **PQK-2nn** | 1-body + NN 2-body | 3 | $720 \cdot S$ | $720 \cdot S$ |
| **E (raw)** | 1-body + all ZZ | 3 | $720 \cdot S$ | $720 \cdot S$ |
| **FQ** | Swap test | 1 | $8{,}780 \cdot S$ | $28{,}680 \cdot S$ |

---

## Publication Figures
All figures are vector PDFs compiled from committed raw data in `results/`:
- **Figure 1:** [Task 1 Learning Curves](figures/fig_learning_curve_t1.pdf)
- **Figure 2:** [Task 2 Contained vs Non-Contained Correlators](figures/fig_t2_contained_vs_not.pdf)
- **Figure 3:** [Task 4 2D Frustrated Lattices ($2 \times 4$ and $3 \times 4$)](figures/fig_t4_lattices.pdf)
- **Figure 4:** [Task 3 Kernel Concentration Scaling ($n=4$ to $14$)](figures/fig_concentration.pdf)
- **Figure 5:** [Task 5 Finite Measurement Shot Costs](figures/fig_shots.pdf)
- **Figure 6:** [Task 5 FQ Gram Spectrum Indefiniteness](figures/fig_fq_spectrum.pdf)
- **Figure 7:** [Task 5 Depolarizing Noise: Retuned vs Fixed Hyperparameters](figures/fig_depolarizing_retuned_per_qubit_proxy.pdf)
- **Figure 8:** [Hyperparameter Search Grid Epsilon Selection](figures/fig_epsilon_selection.pdf)

---

## Explicit Boundaries & Limitations
1. **Exact Ground States:** States are obtained via exact diagonalization rather than shallow parameterized quantum circuits. This isolates representation expressivity from barren plateaus in circuit optimization, but does not capture gate synthesis errors.
2. **System Size Range ($n \le 14$):** Due to exponential statevector scaling ($2^{14} = 16{,}384$), classical ground state computation was bounded at $n \le 14$.
3. **Equilibrium Physical Manifolds:** The benchmark evaluates equilibrium Hamiltonian ground states. It does not generalize to non-equilibrium Floquet states, thermal states, or synthetic data engineered to defeat classical polynomial-time algorithms.
4. **Noise Model Scope:** Measurement noise is modeled via independent binomial swap-test sampling; decoherence is modeled via local per-qubit depolarizing channels rather than full hardware pulse-level cross-talk.

---

## Reproduction Commands

### Prerequisites
- Python 3.10+
- Virtual environment setup:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
pip install -r requirements.txt
```

### 1. Run Unit Tests (< 10 seconds)
```bash
make test
# or: pytest tests/ -v
```

### 2. Fast Smoke Test (< 1 minute)
Runs 3 seeds on Task 1 at $N=40$:
```bash
make reproduce-quick
# or: python scripts/reproduce_quick.py
```

### 3. Generate Publication Figures & LaTeX Tables
```bash
make figures
# or: python scripts/make_figures.py && python scripts/make_tables.py
```

### 4. Full Benchmark Execution
```bash
make reproduce-full
```

---

## License & Citation
This project is licensed under the [MIT License](LICENSE).

```bibtex
@article{doddagoudar2026quantumkernels,
  title={Projected and Fidelity Quantum Kernels versus Classical Correlator Baselines on Exact Spin-Chain Ground States},
  author={Doddagoudar, Abhishek K.},
  year={2026},
  publisher={Presidency University}
}
```
