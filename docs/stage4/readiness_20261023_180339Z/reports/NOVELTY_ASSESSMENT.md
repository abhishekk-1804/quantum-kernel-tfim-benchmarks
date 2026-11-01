# Stage 4 Novelty Assessment: Contributions and Scope Boundaries
**Workspace:** `D:\quantum-kernel-tfim-benchmarks`  
**Package:** `docs/stage4/readiness_20261023_180339Z/`  
**Classification:** Epistemic contribution audit; strictly enforcing negative constraints.

---

## 1. Categorization of Proposed Contributions

To maintain strict scientific integrity and prevent overclaiming, all claims and findings are separated into 5 formal epistemic tiers:

```
+-------------------------------------------------------------------------+
| 1. Established Background (Prior Literature)                            |
|    - RKHS kernel formulations (Schuld & Killoran 2019)                  |
|    - Projected Quantum Kernels (Huang et al. 2021)                      |
|    - Bandwidth sensitivity in quantum kernels (Shaydulin & Wild 2022)   |
|    - Exponential concentration bounds (Thanasilp et al. 2024)           |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| 2. Implementation & Correctness Clarifications                          |
|    - R1: Bandwidth normalizer grid parameterization resolves E2 vs PQK  |
|    - R2: Shot-noise impact of null observable Z in noisy PQK-1          |
|    - R3: Asymmetric PSD clipping behavior on rectangular test blocks    |
|    - M1: Scope qualification of <= 0.011 bound across sample sizes      |
|    - M2: Representation identity B == C between E2(raw) and PQK-2nn     |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| 3. Confirmatory Empirical Findings                                      |
|    - Task 1: PQK spatial hierarchy (PQK-2nn > PQK-1 across N_tr)        |
|    - Task 2: Asymptotic equivalence for 4-point correlator (Claim C3)   |
|    - Task 3: Absence of exponential concentration for 1D TFIM up to n=14|
|    - Stage 2: Lack of finite-shot crossover up to B_tot = 10^5          |
|    - Stage 3: Superior OOD phase extrapolation of FQ over PQK-2nn       |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| 4. Potentially Novel Scientific Contributions                           |
|    - First rigorous equal-total-budget evaluation revealing the sample  |
|      efficiency threshold for fidelity vs projected quantum kernels.    |
|    - Controlled demonstration that full fidelity geometry provides      |
|      superior out-of-distribution phase extrapolation over 2-body RDMs. |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| 5. Novelty Unresolved (Requires Future Theoretical Investigation)       |
|    - Exact analytical mechanism explaining why global fidelity vectors  |
|      extrapolate across quantum phase boundaries better than marginals. |
+-------------------------------------------------------------------------+
```

---

## 2. Enforcement of Mandatory Negative Constraints

Per project governance rules, the following assertions are **STRICTLY PROHIBITED** and excluded from the manuscript:

1. **NO Claim of New Theorems for Standard Expansions:**  
   The mathematical expansion of reduced density matrices into Pauli expectation bases is standard quantum mechanics; it is **NOT** claimed as a novel theorem.
2. **NO Assertion that Absence of Crossover Proves Universal Absence:**  
   The observation that no finite-shot crossover occurs between FQ and PQK-2nn up to $B_{\text{tot}} = 10^5$ is an empirical finding within the tested domain; it does **NOT** prove that a crossover cannot exist at asymptotically higher budgets ($B_{\text{tot}} > 10^6$) or larger system sizes ($n > 14$).
3. **NO Claim that Small Target Variance Alone Causes Negative $R^2$:**  
   While low target variance in test splits inflates negative $R^2$ values, it is **NOT** claimed as the sole cause of model failure. Out-of-distribution degradation is driven by structural shift in feature representations.
4. **NO Claim that Kernel Contribution Ablations Establish Causal Physical Mechanisms:**  
   Ablation studies isolating 1-body and 2-body kernel terms demonstrate statistical associations; they do **NOT** prove a causal physical mechanism.
