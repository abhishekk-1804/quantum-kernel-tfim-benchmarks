# Stage 4 Literature Synthesis: Quantum Kernels, Inductive Bias, and Generalization
**Workspace:** `D:\quantum-kernel-tfim-benchmarks`  
**Package:** `docs/stage4/readiness_20261023_180339Z/`  
**Classification:** Research synthesis and contextual grounding.

---

## 1. Synthesis of Theoretical and Empirical Foundations

The benchmark suite investigates quantum kernel methods for learning physical ground-state properties of the 1D Transverse-Field Ising Model (TFIM). Grounding our findings in established literature reveals several direct alignments and distinctions:

### 1.1 The Role of Kernel Bandwidth (Shaydulin & Wild 2022; Canatar et al. 2023)
A central theme in recent quantum kernel literature is the critical sensitivity of quantum models to bandwidth parameterization. Shaydulin & Wild (PRA 2022) and Canatar et al. (TMLR 2023) proved that unscaled quantum kernels often suffer from flat geometry (exponential concentration or trivial identity Gram matrices) unless the effective bandwidth is carefully tuned to match the data distribution.
- **In our study:** We confirm this sensitivity in Task 1 (Claim C7), showing that SVR performance varies by up to $+0.06$ $R^2$ across $\epsilon$ and bandwidth grids. Furthermore, our audit of Issue R1 demonstrated that the apparent performance discrepancy between classical $E_2(\text{raw})$ and $PQK\text{-2nn}$ was entirely an artifact of normalizer grid formulation ($4n=32$ vs $5(n-1)=35$), reinforcing Canatar et al.'s finding that bandwidth choices dictate observed performance.

### 1.2 Classical Surrogates and Inductive Bias (Kübler et al. 2021; Huang et al. 2021)
Kübler et al. (NeurIPS 2021) established that when classical kernels are engineered with the same inductive bias as quantum kernels, classical methods frequently match or surpass quantum models without quantum measurement overhead.
- **In our study:** This principle is directly observed in Task 2 and Item M2. Classical RBF kernels on 2-body Pauli expectations ($E_2$) possess the exact same feature representation as $PQK\text{-2nn}$ ($B == C$, max $|B-C| = 0.00 \times 10^0$). For local 1D TFIM observables, quantum data representation does not offer a structural advantage over classical 2-body correlators.

### 1.3 Measurement Resources and Sample Efficiency (Huang et al. 2021)
Huang et al. (Nature Comm 2021) argued that projected quantum kernels provide substantial measurement advantages over fidelity kernels because $PQK$ evaluates single- or two-qubit marginals ($O(N \cdot n^k)$ measurements) rather than quadratic pairs of quantum states ($O(N^2)$ swap tests).
- **In our study:** We rigorously quantified this measurement trade-off in Stage 2 (Equal-Total-Budget) and Task 5 (Finite Shots). Feature-based models allocate $3.25\times$ higher shot precision per evaluation under identical total budgets ($B_{\text{tot}} = 10^5$). However, our confirmatory Stage 2 experiment revealed that under total shot budgets up to $B_{\text{tot}} = 10^5$, **no finite-shot crossover occurs**: FQ remains sample-inefficient and fails to surpass $PQK\text{-2nn}$ in the low-to-medium budget regime.

### 1.4 Out-of-Distribution Phase-Shift Generalization (Task 6)
While most prior studies (Havlicek 2019, Shaydulin 2022, Canatar 2023) evaluated in-distribution test splits, our Task 6 benchmark evaluated out-of-distribution (OOD) extrapolation across a severe quantum phase shift (training in ordered ferromagnetic phase $g \in [0.2, 0.8]$, testing in disordered paramagnetic phase $g \in [1.2, 1.8]$).
- **In our study:** Under this severe distribution shift, full fidelity quantum kernels (FQ) significantly outperform $PQK\text{-2nn}$ ($W = 21.0, p = 8.51 \times 10^{-4}$), achieving $3.07\times$ lower mean MAE ($0.0602$ vs $0.1850$). This indicates that global fidelity geometry retains non-local phase information that local 2-body marginals lose under distribution shift.
