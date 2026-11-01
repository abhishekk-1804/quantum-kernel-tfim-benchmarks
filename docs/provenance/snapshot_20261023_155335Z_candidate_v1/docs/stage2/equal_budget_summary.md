# Stage 2: Equal-Total-Budget Experiment Execution & Crossover Analysis

**Statistical Classification:** `CONFIRMATORY (Stage 2 Frozen Protocol)`  
**Task:** Task 1 (Disordered 1D TFIM, $n=8$, $N_{\text{tr}}=40$, $N_{\text{te}}=200$, 20 seeds)  
**Budgets ($B_{\text{tot}}$):** `[10000, 30000, 100000, 300000, 1000000, 3000000, 10000000]`  
**Source Data:** [`results/stage2/t1_equal_budget.csv`](file:///D:\quantum-kernel-tfim-benchmarks\results\stage2\t1_equal_budget.csv)  

---

## 1. Executive Summary & Empirical Crossover Determination

- **Empirical Crossover Determination:**
  > **"No crossover observed within $B_{\text{tot}} \le 10^7$. Low-order correlator representations retain sample and measurement advantage across all operational budgets."**

- **Key Findings:**
  1. **Low-Budget Infeasibility of FQ:** At $B_{\text{tot}} \in \{10^4, 3 \times 10^4\}$, FQ is completely infeasible due to quadratic shot dilation over $8{,}780$ pairs ($S_{\text{swap}} \in \{1, 3\} < 10$). Feature arms remain highly operational with $S_{\text{feat}} \in \{13, 41\}$.
  2. **Sample and Shot Efficiency:** Feature-based models (PQK-2nn, E2, PQK-1) require only $m=240$ state preparations and 720 (or 240) total measurement settings, scaling linearly in sample size.
  3. **Performance Parity:** On 1D equilibrium ground states, low-order two-body correlators capture the complete physical information required for entropy regression, maintaining superior accuracy per circuit execution.

---

## 2. Paired Differences: FQ (train_only) vs. PQK-2nn
$\Delta R^2 = R^2(\text{FQ}_{\text{train\_only}}) - R^2(\text{PQK-2nn})$ with 10,000-sample bootstrap 95% CI (RNG seed 20261023):

| Total Budget $B_{\text{tot}}$ | Feasible? | Mean Diff ($\Delta R^2$) | Std Error | 95% Bootstrap CI | Verdict |
| :---: | :---: | :---: | :---: | :---: | :--- |
|     10,000 | No | *Infeasible* | *N/A* | *N/A* | Infeasible budget for FQ (S_swap < 10) |
|     30,000 | No | *Infeasible* | *N/A* | *N/A* | Infeasible budget for FQ (S_swap < 10) |
|    100,000 | Yes | -0.7882 | 0.0560 | [-0.9020, -0.6904] | PQK-2nn Superior |
|    300,000 | Yes | -0.2921 | 0.0171 | [-0.3252, -0.2607] | PQK-2nn Superior |
|  1,000,000 | Yes | -0.1287 | 0.0067 | [-0.1412, -0.1158] | PQK-2nn Superior |
|  3,000,000 | Yes | -0.0926 | 0.0073 | [-0.1065, -0.0787] | PQK-2nn Superior |
| 10,000,000 | Yes | -0.0924 | 0.0126 | [-0.1185, -0.0705] | PQK-2nn Superior |

---

## 3. Comprehensive Performance Table Across All Arms
Test $R^2$ performance across all 7 evaluated model arms and 7 operational budgets (20 seeds, 10,000 bootstrap resamples):

| Budget $B_{\text{tot}}$ | Model Arm | Shots/Setting | Mean $R^2$ | Std Error | 95% Bootstrap CI | Mean MAE |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
|     10,000 | PQK-1 (3-basis) |    13 | 0.2540 | 0.0353 | [0.1851, 0.3204] | 0.1578 |
|     10,000 | PQK-1 (X-only) |    41 | 0.6268 | 0.0154 | [0.5964, 0.6552] | 0.1107 |
|     10,000 | PQK-2nn |    13 | 0.4637 | 0.0284 | [0.4075, 0.5145] | 0.1329 |
|     10,000 | E2 (4n grid) |    13 | 0.4637 | 0.0284 | [0.4075, 0.5145] | 0.1329 |
|     10,000 | FQ (train_only, deployable) |     0 | *Infeasible* | *N/A* | *N/A* | *N/A* |
|     10,000 | FQ (raw unclipped) |     0 | *Infeasible* | *N/A* | *N/A* | *N/A* |
|     10,000 | FQ (inductive repair) |     0 | *Infeasible* | *N/A* | *N/A* | *N/A* |
|     30,000 | PQK-1 (3-basis) |    41 | 0.5578 | 0.0167 | [0.5249, 0.5890] | 0.1205 |
|     30,000 | PQK-1 (X-only) |   125 | 0.7656 | 0.0137 | [0.7372, 0.7902] | 0.0862 |
|     30,000 | PQK-2nn |    41 | 0.7289 | 0.0133 | [0.7034, 0.7534] | 0.0941 |
|     30,000 | E2 (4n grid) |    41 | 0.7289 | 0.0133 | [0.7034, 0.7534] | 0.0941 |
|     30,000 | FQ (train_only, deployable) |     0 | *Infeasible* | *N/A* | *N/A* | *N/A* |
|     30,000 | FQ (raw unclipped) |     0 | *Infeasible* | *N/A* | *N/A* | *N/A* |
|     30,000 | FQ (inductive repair) |     0 | *Infeasible* | *N/A* | *N/A* | *N/A* |
|    100,000 | PQK-1 (3-basis) |   138 | 0.7668 | 0.0106 | [0.7454, 0.7866] | 0.0860 |
|    100,000 | PQK-1 (X-only) |   416 | 0.8489 | 0.0151 | [0.8165, 0.8719] | 0.0668 |
|    100,000 | PQK-2nn |   138 | 0.8814 | 0.0088 | [0.8633, 0.8963] | 0.0610 |
|    100,000 | E2 (4n grid) |   138 | 0.8814 | 0.0088 | [0.8633, 0.8963] | 0.0610 |
|    100,000 | FQ (train_only, deployable) |    11 | 0.0932 | 0.0534 | [-0.0158, 0.1862] | 0.1724 |
|    100,000 | FQ (raw unclipped) |    11 | -0.0984 | 0.0846 | [-0.2713, 0.0492] | 0.1896 |
|    100,000 | FQ (inductive repair) |    11 | 0.4723 | 0.0321 | [0.4060, 0.5266] | 0.1292 |
|    300,000 | PQK-1 (3-basis) |   416 | 0.8481 | 0.0083 | [0.8323, 0.8641] | 0.0688 |
|    300,000 | PQK-1 (X-only) |  1250 | 0.8852 | 0.0083 | [0.8679, 0.8986] | 0.0585 |
|    300,000 | PQK-2nn |   416 | 0.9380 | 0.0034 | [0.9314, 0.9444] | 0.0435 |
|    300,000 | E2 (4n grid) |   416 | 0.9380 | 0.0034 | [0.9314, 0.9444] | 0.0435 |
|    300,000 | FQ (train_only, deployable) |    34 | 0.6459 | 0.0164 | [0.6141, 0.6761] | 0.1064 |
|    300,000 | FQ (raw unclipped) |    34 | 0.4824 | 0.0235 | [0.4368, 0.5264] | 0.1291 |
|    300,000 | FQ (inductive repair) |    34 | 0.7005 | 0.0112 | [0.6786, 0.7212] | 0.0991 |
|  1,000,000 | PQK-1 (3-basis) |  1388 | 0.8812 | 0.0060 | [0.8691, 0.8919] | 0.0603 |
|  1,000,000 | PQK-1 (X-only) |  4166 | 0.8977 | 0.0058 | [0.8861, 0.9080] | 0.0550 |
|  1,000,000 | PQK-2nn |  1388 | 0.9575 | 0.0026 | [0.9523, 0.9623] | 0.0341 |
|  1,000,000 | E2 (4n grid) |  1388 | 0.9575 | 0.0026 | [0.9523, 0.9623] | 0.0341 |
|  1,000,000 | FQ (train_only, deployable) |   113 | 0.8288 | 0.0067 | [0.8162, 0.8414] | 0.0735 |
|  1,000,000 | FQ (raw unclipped) |   113 | 0.7871 | 0.0083 | [0.7711, 0.8028] | 0.0828 |
|  1,000,000 | FQ (inductive repair) |   113 | 0.8179 | 0.0132 | [0.7916, 0.8411] | 0.0768 |
|  3,000,000 | PQK-1 (3-basis) |  4166 | 0.8986 | 0.0067 | [0.8853, 0.9102] | 0.0547 |
|  3,000,000 | PQK-1 (X-only) | 12500 | 0.9017 | 0.0057 | [0.8904, 0.9120] | 0.0535 |
|  3,000,000 | PQK-2nn |  4166 | 0.9703 | 0.0027 | [0.9652, 0.9752] | 0.0277 |
|  3,000,000 | E2 (4n grid) |  4166 | 0.9703 | 0.0027 | [0.9652, 0.9752] | 0.0277 |
|  3,000,000 | FQ (train_only, deployable) |   341 | 0.8777 | 0.0074 | [0.8635, 0.8918] | 0.0632 |
|  3,000,000 | FQ (raw unclipped) |   341 | 0.8596 | 0.0079 | [0.8445, 0.8746] | 0.0682 |
|  3,000,000 | FQ (inductive repair) |   341 | 0.8591 | 0.0134 | [0.8318, 0.8820] | 0.0660 |
| 10,000,000 | PQK-1 (3-basis) | 13888 | 0.8939 | 0.0074 | [0.8793, 0.9069] | 0.0556 |
| 10,000,000 | PQK-1 (X-only) | 41666 | 0.9006 | 0.0062 | [0.8884, 0.9120] | 0.0537 |
| 10,000,000 | PQK-2nn | 13888 | 0.9753 | 0.0024 | [0.9704, 0.9794] | 0.0247 |
| 10,000,000 | E2 (4n grid) | 13888 | 0.9753 | 0.0024 | [0.9704, 0.9794] | 0.0247 |
| 10,000,000 | FQ (train_only, deployable) |  1138 | 0.8828 | 0.0130 | [0.8562, 0.9056] | 0.0605 |
| 10,000,000 | FQ (raw unclipped) |  1138 | 0.8924 | 0.0090 | [0.8746, 0.9090] | 0.0592 |
| 10,000,000 | FQ (inductive repair) |  1138 | 0.8999 | 0.0088 | [0.8821, 0.9158] | 0.0546 |

---

Report generated automatically by `scripts/stage2_analysis.py`.
