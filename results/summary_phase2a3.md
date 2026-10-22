# Phase 2a.3 Summary: SVR Epsilon Tuning & Boundary Audit Report

**Date:** 2026-10-22 05:45:06
**Scope:** Task 1 (Disordered TFIM Entanglement Entropy) & Task 4b (Frustrated 2D Lattice Entropy Regression)
**Hyperparameter Grid:** grid_v3 (Tuned SVR $\epsilon \in \{0.1, 0.03, 0.01, 0.003, 0.001\}$ across all SVR arms)

---

## 1. Executive Summary

- **SVR Epsilon Tuning Impact:** In grid_v2, $\epsilon$ was fixed at $0.1$. In grid_v3, $\epsilon$ was tuned across 5 values spanning 2 orders of magnitude via inner 3-fold cross-validation.
- **Performance & Rankings:** Detailed below, comparing grid_v2 vs grid_v3 test set $R^2$ with 10,000 bootstrap 95% confidence intervals.
- **Mathematical Rigor:** Fast precomputed squared-distance slicing was utilized for inner-CV folds, evaluating identical kernel representations to machine precision ($0.00\text{e}+00$ discrepancy vs direct SVR).
- **Directional Boundary Audit:** All boundary frequencies for $C$, $c$, $\alpha$, and $\epsilon$ are tabulated in `results/grid_boundary_post_v3.csv`.

---

## 2. Epsilon Selection Analysis

### Distribution of Selected Epsilon Values across All SVR Models:

| Selected $\epsilon$ | Count | Percentage |
|---|---|---|
| 0.001 | 618 | 34.4% |
| 0.003 | 228 | 12.7% |
| 0.01 | 315 | 17.5% |
| 0.03 | 353 | 19.6% |
| 0.1 | 285 | 15.8% |

---

## 3. Task 1: Disordered TFIM Half-Chain Entropy ($n=8$)

Comparison of Test Set $R^2$ (Mean and 10,000 Bootstrap 95% CI) between grid_v2 ($\epsilon=0.1$) and grid_v3 (tuned $\epsilon$):

### Sample Size $N = 10$

| Rank | Model | Variant | grid_v2 $R^2$ [95% CI] | grid_v3 $R^2$ [95% CI] | $\Delta R^2$ |
|---|---|---|---|---|---|
| 1 | FQ | none | 0.8303 [0.7389, 0.8915] | 0.8916 [0.8586, 0.9206] | +0.0613 |
| 2 | E2 | raw | 0.8520 [0.8058, 0.8903] | 0.8661 [0.8318, 0.8977] | +0.0140 |
| 3 | PQK-2nn | none | 0.8553 [0.8072, 0.8937] | 0.8520 [0.8020, 0.8948] | -0.0033 |
| 4 | E | raw | 0.8332 [0.7696, 0.8832] | 0.8305 [0.7660, 0.8835] | -0.0027 |
| 5 | F | std | 0.8192 [0.7853, 0.8493] | 0.8192 [0.7853, 0.8493] | +0.0000 |
| 6 | E | std | 0.7900 [0.7280, 0.8328] | 0.8161 [0.7872, 0.8434] | +0.0261 |
| 7 | PQK-1 (== RBF on <X>) | none | 0.7553 [0.7171, 0.7918] | 0.7477 [0.7114, 0.7827] | -0.0076 |
| 8 | E_X | raw | 0.7553 [0.7171, 0.7918] | 0.7477 [0.7114, 0.7827] | -0.0076 |
| 9 | baseline_mean | none | -0.1785 [-0.3518, -0.0687] | -0.1785 [-0.3518, -0.0687] | +0.0000 |

### Sample Size $N = 40$

| Rank | Model | Variant | grid_v2 $R^2$ [95% CI] | grid_v3 $R^2$ [95% CI] | $\Delta R^2$ |
|---|---|---|---|---|---|
| 1 | FQ | none | 0.9826 [0.9811, 0.9841] | 0.9902 [0.9888, 0.9916] | +0.0076 |
| 2 | E | raw | 0.9807 [0.9786, 0.9826] | 0.9872 [0.9847, 0.9894] | +0.0064 |
| 3 | E | std | 0.9721 [0.9684, 0.9753] | 0.9801 [0.9769, 0.9834] | +0.0080 |
| 4 | PQK-2nn | none | 0.9717 [0.9688, 0.9746] | 0.9789 [0.9731, 0.9834] | +0.0072 |
| 5 | E2 | raw | 0.9715 [0.9686, 0.9744] | 0.9786 [0.9728, 0.9833] | +0.0071 |
| 6 | F | std | 0.9728 [0.9664, 0.9776] | 0.9728 [0.9664, 0.9776] | +0.0000 |
| 7 | PQK-1 (== RBF on <X>) | none | 0.9046 [0.8955, 0.9137] | 0.8986 [0.8845, 0.9113] | -0.0060 |
| 8 | E_X | raw | 0.9046 [0.8955, 0.9137] | 0.8986 [0.8845, 0.9113] | -0.0060 |
| 9 | baseline_mean | none | -0.0243 [-0.0428, -0.0095] | -0.0243 [-0.0428, -0.0095] | +0.0000 |

### Sample Size $N = 160$

| Rank | Model | Variant | grid_v2 $R^2$ [95% CI] | grid_v3 $R^2$ [95% CI] | $\Delta R^2$ |
|---|---|---|---|---|---|
| 1 | E | raw | 0.9935 [0.9931, 0.9938] | 0.9987 [0.9986, 0.9989] | +0.0053 |
| 2 | FQ | none | 0.9924 [0.9920, 0.9929] | 0.9975 [0.9972, 0.9978] | +0.0051 |
| 3 | E | std | 0.9919 [0.9914, 0.9924] | 0.9965 [0.9961, 0.9969] | +0.0046 |
| 4 | PQK-2nn | none | 0.9905 [0.9897, 0.9914] | 0.9943 [0.9936, 0.9950] | +0.0038 |
| 5 | E2 | raw | 0.9906 [0.9897, 0.9915] | 0.9942 [0.9934, 0.9950] | +0.0037 |
| 6 | F | std | 0.9887 [0.9878, 0.9895] | 0.9887 [0.9878, 0.9895] | +0.0000 |
| 7 | PQK-1 (== RBF on <X>) | none | 0.9537 [0.9510, 0.9564] | 0.9529 [0.9506, 0.9553] | -0.0008 |
| 8 | E_X | raw | 0.9537 [0.9510, 0.9564] | 0.9529 [0.9506, 0.9553] | -0.0008 |
| 9 | baseline_mean | none | -0.0082 [-0.0151, -0.0030] | -0.0082 [-0.0151, -0.0030] | +0.0000 |

---

## 4. Task 4b: Frustrated 2D Lattice Entropy Regression

Comparison of Test Set $R^2$ (Mean and 10,000 Bootstrap 95% CI) between grid_v2 ($\epsilon=0.1$) and grid_v3 (tuned $\epsilon$):

### Lattice: 2x4, Sample Size $N = 10$

| Rank | Model | Variant | grid_v2 $R^2$ [95% CI] | grid_v3 $R^2$ [95% CI] | $\Delta R^2$ |
|---|---|---|---|---|---|
| 1 | E | raw | 0.7533 [0.6372, 0.8550] | 0.8249 [0.7431, 0.8910] | +0.0716 |
| 2 | E2 | raw | 0.8250 [0.7400, 0.8892] | 0.7233 [0.5416, 0.8682] | -0.1017 |
| 3 | E | std | 0.6600 [0.5805, 0.7282] | 0.6250 [0.5092, 0.7198] | -0.0350 |
| 4 | FQ | none | 0.7260 [0.5628, 0.8466] | 0.6245 [0.3864, 0.8054] | -0.1015 |
| 5 | PQK-2nn | none | 0.7751 [0.6544, 0.8658] | 0.6045 [0.3524, 0.8110] | -0.1706 |
| 6 | PQK-1 (== RBF on <X>) | none | 0.5886 [0.1771, 0.8237] | 0.5559 [0.1234, 0.8277] | -0.0327 |
| 7 | E_X | raw | 0.5886 [0.1771, 0.8237] | 0.5559 [0.1234, 0.8277] | -0.0327 |
| 8 | F | std | 0.3448 [0.1613, 0.5007] | 0.3448 [0.1613, 0.5007] | +0.0000 |
| 9 | baseline_mean | none | -0.0755 [-0.1151, -0.0415] | -0.0755 [-0.1151, -0.0415] | +0.0000 |

### Lattice: 2x4, Sample Size $N = 80$

| Rank | Model | Variant | grid_v2 $R^2$ [95% CI] | grid_v3 $R^2$ [95% CI] | $\Delta R^2$ |
|---|---|---|---|---|---|
| 1 | E | raw | 0.9890 [0.9834, 0.9936] | 0.9951 [0.9911, 0.9979] | +0.0061 |
| 2 | PQK-2nn | none | 0.9867 [0.9815, 0.9910] | 0.9934 [0.9888, 0.9969] | +0.0067 |
| 3 | E2 | raw | 0.9867 [0.9813, 0.9912] | 0.9917 [0.9851, 0.9965] | +0.0049 |
| 4 | FQ | none | 0.9838 [0.9774, 0.9888] | 0.9832 [0.9756, 0.9890] | -0.0007 |
| 5 | F | std | 0.9626 [0.9425, 0.9769] | 0.9626 [0.9425, 0.9769] | +0.0000 |
| 6 | E | std | 0.9524 [0.9402, 0.9632] | 0.9564 [0.9415, 0.9697] | +0.0039 |
| 7 | PQK-1 (== RBF on <X>) | none | 0.9491 [0.9387, 0.9585] | 0.9472 [0.9362, 0.9575] | -0.0018 |
| 8 | E_X | raw | 0.9491 [0.9387, 0.9585] | 0.9472 [0.9362, 0.9575] | -0.0018 |
| 9 | baseline_mean | none | -0.0172 [-0.0333, -0.0050] | -0.0172 [-0.0333, -0.0050] | +0.0000 |

### Lattice: 3x4, Sample Size $N = 10$

| Rank | Model | Variant | grid_v2 $R^2$ [95% CI] | grid_v3 $R^2$ [95% CI] | $\Delta R^2$ |
|---|---|---|---|---|---|
| 1 | FQ | none | 0.9321 [0.8854, 0.9643] | 0.9455 [0.9013, 0.9735] | +0.0135 |
| 2 | E2 | raw | 0.6371 [0.0279, 0.9498] | 0.9054 [0.8498, 0.9470] | +0.2683 |
| 3 | PQK-2nn | none | 0.6724 [0.1071, 0.9647] | 0.8633 [0.7831, 0.9330] | +0.1910 |
| 4 | E | raw | 0.8743 [0.7760, 0.9382] | 0.8423 [0.6823, 0.9373] | -0.0320 |
| 5 | E | std | 0.3416 [-0.5228, 0.7986] | 0.7150 [0.6358, 0.7852] | +0.3734 |
| 6 | PQK-1 (== RBF on <X>) | none | 0.5768 [0.1657, 0.8771] | 0.6166 [0.2073, 0.8701] | +0.0398 |
| 7 | E_X | raw | 0.5768 [0.1657, 0.8771] | 0.6166 [0.2073, 0.8701] | +0.0398 |
| 8 | baseline_mean | none | -0.0601 [-0.0930, -0.0343] | -0.0601 [-0.0930, -0.0343] | +0.0000 |
| 9 | F | std | -0.1934 [-1.3214, 0.4810] | -0.2854 [-1.4458, 0.4398] | -0.0920 |

### Lattice: 3x4, Sample Size $N = 80$

| Rank | Model | Variant | grid_v2 $R^2$ [95% CI] | grid_v3 $R^2$ [95% CI] | $\Delta R^2$ |
|---|---|---|---|---|---|
| 1 | FQ | none | 0.9935 [0.9923, 0.9943] | 0.9996 [0.9995, 0.9997] | +0.0061 |
| 2 | PQK-2nn | none | 0.9927 [0.9905, 0.9943] | 0.9994 [0.9988, 0.9998] | +0.0067 |
| 3 | E2 | raw | 0.9932 [0.9917, 0.9944] | 0.9994 [0.9987, 0.9998] | +0.0062 |
| 4 | E | raw | 0.9927 [0.9911, 0.9940] | 0.9993 [0.9989, 0.9997] | +0.0066 |
| 5 | E | std | 0.9814 [0.9794, 0.9834] | 0.9933 [0.9916, 0.9949] | +0.0119 |
| 6 | PQK-1 (== RBF on <X>) | none | 0.9858 [0.9815, 0.9892] | 0.9887 [0.9844, 0.9924] | +0.0029 |
| 7 | E_X | raw | 0.9858 [0.9815, 0.9892] | 0.9887 [0.9844, 0.9924] | +0.0029 |
| 8 | F | std | 0.9787 [0.9537, 0.9960] | 0.9669 [0.9284, 0.9955] | -0.0118 |
| 9 | baseline_mean | none | -0.0139 [-0.0315, -0.0033] | -0.0146 [-0.0334, -0.0035] | -0.0007 |

---

## 5. Residual Boundary Hits & Sanity Checks

### Boundary Pegging Rates (>30% on C, c, alpha or >50% on epsilon):

| Task | Target | Lattice | Model | Variant | N | Pegged Boundaries |
|---|---|---|---|---|---|---|
| T1 | half_chain_entropy | none | PQK-1 (== RBF on <X>) | none | 10 | C_high=40% |
| T1 | half_chain_entropy | none | PQK-2nn | none | 10 | C_high=35%, eps_low=60% |
| T1 | half_chain_entropy | none | FQ | none | 10 | eps_low=60% |
| T1 | half_chain_entropy | none | E | raw | 10 | C_high=45%, eps_low=65% |
| T1 | half_chain_entropy | none | E | std | 10 | C_high=40%, c_low=60%, eps_low=65% |
| T1 | half_chain_entropy | none | F | std | 10 | alpha_low=45% |
| T1 | half_chain_entropy | none | E2 | raw | 10 | C_high=40%, eps_low=65% |
| T1 | half_chain_entropy | none | E_X | raw | 10 | C_high=40% |
| T1 | half_chain_entropy | none | PQK-2nn | none | 20 | C_high=35% |
| T1 | half_chain_entropy | none | FQ | none | 20 | eps_low=75% |
| T1 | half_chain_entropy | none | E | raw | 20 | C_high=60%, eps_low=60% |
| T1 | half_chain_entropy | none | E | std | 20 | C_high=35%, c_low=50%, eps_low=55% |
| T1 | half_chain_entropy | none | F | std | 20 | alpha_low=40% |
| T1 | half_chain_entropy | none | E2 | raw | 20 | C_high=35% |
| T1 | half_chain_entropy | none | FQ | none | 40 | eps_low=60% |
| T1 | half_chain_entropy | none | E | raw | 40 | C_high=35% |
| T1 | half_chain_entropy | none | E | std | 40 | C_high=50% |
| T1 | half_chain_entropy | none | PQK-1 (== RBF on <X>) | none | 80 | eps_high=60% |
| T1 | half_chain_entropy | none | PQK-2nn | none | 80 | C_high=40% |
| T1 | half_chain_entropy | none | E2 | raw | 80 | C_high=35% |
| T1 | half_chain_entropy | none | E_X | raw | 80 | eps_high=60% |
| T1 | half_chain_entropy | none | E | raw | 160 | C_high=45% |
| T4b | half_cut_entropy | 2x4 | PQK-1 (== RBF on <X>) | none | 10 | C_high=55% |
| T4b | half_cut_entropy | 2x4 | E | std | 10 | eps_low=60% |
| T4b | half_cut_entropy | 2x4 | E_X | raw | 10 | C_high=55% |
| T4b | half_cut_entropy | 2x4 | PQK-1 (== RBF on <X>) | none | 20 | C_high=35% |
| T4b | half_cut_entropy | 2x4 | PQK-2nn | none | 20 | C_high=65% |
| T4b | half_cut_entropy | 2x4 | FQ | none | 20 | C_high=35% |
| T4b | half_cut_entropy | 2x4 | E | raw | 20 | C_high=45% |
| T4b | half_cut_entropy | 2x4 | E | std | 20 | eps_low=65% |
| T4b | half_cut_entropy | 2x4 | F | std | 20 | alpha_high=35% |
| T4b | half_cut_entropy | 2x4 | E2 | raw | 20 | C_high=60% |
| T4b | half_cut_entropy | 2x4 | E_X | raw | 20 | C_high=35% |
| T4b | half_cut_entropy | 2x4 | PQK-2nn | none | 40 | C_high=40% |
| T4b | half_cut_entropy | 2x4 | E | raw | 40 | C_high=35% |
| T4b | half_cut_entropy | 2x4 | E2 | raw | 40 | C_high=45% |
| T4b | half_cut_entropy | 2x4 | PQK-1 (== RBF on <X>) | none | 80 | C_high=50% |
| T4b | half_cut_entropy | 2x4 | PQK-2nn | none | 80 | C_high=45% |
| T4b | half_cut_entropy | 2x4 | FQ | none | 80 | C_high=65% |
| T4b | half_cut_entropy | 2x4 | E | raw | 80 | C_high=60% |
| T4b | half_cut_entropy | 2x4 | E | std | 80 | C_high=35% |
| T4b | half_cut_entropy | 2x4 | E2 | raw | 80 | C_high=45% |
| T4b | half_cut_entropy | 2x4 | E_X | raw | 80 | C_high=50% |
| T4b | half_cut_entropy | 3x4 | E | std | 10 | eps_low=55% |
| T4b | half_cut_entropy | 3x4 | F | std | 10 | alpha_high=65% |
| T4b | half_cut_entropy | 3x4 | PQK-1 (== RBF on <X>) | none | 20 | C_high=40% |
| T4b | half_cut_entropy | 3x4 | PQK-2nn | none | 20 | C_high=55% |
| T4b | half_cut_entropy | 3x4 | E | raw | 20 | C_high=55% |
| T4b | half_cut_entropy | 3x4 | F | std | 20 | alpha_high=60% |
| T4b | half_cut_entropy | 3x4 | E2 | raw | 20 | C_high=45% |
| T4b | half_cut_entropy | 3x4 | E_X | raw | 20 | C_high=40% |
| T4b | half_cut_entropy | 3x4 | PQK-2nn | none | 40 | C_high=65%, eps_low=55% |
| T4b | half_cut_entropy | 3x4 | E | raw | 40 | C_high=85% |
| T4b | half_cut_entropy | 3x4 | E | std | 40 | C_high=40% |
| T4b | half_cut_entropy | 3x4 | E2 | raw | 40 | C_high=65%, eps_low=65% |
| T4b | half_cut_entropy | 3x4 | PQK-1 (== RBF on <X>) | none | 80 | C_high=45% |
| T4b | half_cut_entropy | 3x4 | PQK-2nn | none | 80 | C_high=95%, eps_low=60% |
| T4b | half_cut_entropy | 3x4 | E | raw | 80 | C_high=60%, eps_low=65% |
| T4b | half_cut_entropy | 3x4 | E | std | 80 | C_high=75%, eps_low=65% |
| T4b | half_cut_entropy | 3x4 | E2 | raw | 80 | C_high=75%, eps_low=60% |
| T4b | half_cut_entropy | 3x4 | E_X | raw | 80 | C_high=45% |
