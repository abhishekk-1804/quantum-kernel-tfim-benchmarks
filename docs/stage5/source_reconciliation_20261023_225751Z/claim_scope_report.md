# Task 1 Claim Scope & Statistical Invariant Analysis Report
**Target Package:** `docs/stage5/source_reconciliation_20261023_225751Z/`  
**Evaluation Date:** 2026-10-24 (UTC)  
**Primary Sources:** `results/t1_entropy_gridv3.csv` (SHA256: `619151b90777046a...`), `results/stats.csv` (SHA256: `62fca5f51e298380...`)

---

## 1. Executive Summary: Scope of the $\le 0.011$ Difference Bound (Item M1)

In the historical manuscript drafts (`paper/main.tex` lines 36, 64, 139), a performance bound was stated as:
$$\Delta R^2 \le 0.011$$
suggesting that the performance advantage of full quantum fidelity kernels (FQ) over classical correlator representations is universally bounded by $0.011$ across all evaluation regimes.

A systematic audit of all machine-readable records in `results/stats.csv` and `results/t1_entropy_gridv3.csv` shows that **this claim holds strictly and exclusively for Task 1 at $N_{\mathrm{tr}} = 160$** (where FQ vs. E(raw) paired mean difference is $-0.0012$, and FQ vs. PQK-2nn is $+0.0032$). It **does not hold universally**:

1. **Exceeded Across Other Training Sizes in Task 1:**
   - At $N_{\mathrm{tr}} = 40$: FQ vs. PQK-2nn mean difference is $+0.01135$ (slightly exceeds $0.011$).
   - At $N_{\mathrm{tr}} = 20$: FQ vs. PQK-2nn mean difference is $+0.02700$.
   - At $N_{\mathrm{tr}} = 10$: FQ vs. PQK-2nn mean difference is $+0.03961$, and FQ vs. E(raw) is $+0.06113$ (substantially exceeds $0.011$).
   - At $N_{\mathrm{tr}} = 10$: PQK-1 vs. PQK-2nn difference is $-0.1044$ ($p_{\mathrm{holm}} = 0.0186$).

2. **Exceeded Across Confirmatory Benchmarks ($N \ge 80$):**
   In `results/stats.csv`, out of the 36 pre-declared confirmatory tests, **7 confirmatory tests exceed $|\text{mean\_diff}| > 0.011$**:
   - `T1 chain r2`: PQK-1 vs. PQK-2nn ($N=40$, $\Delta R^2 = -0.0803$; $N=160$, $\Delta R^2 = -0.0414$).
   - `T2b chain r2`: PQK-1 vs. PQK-2nn ($N=40$, $\Delta R^2 = -0.0544$; $N=160$, $\Delta R^2 = -0.0385$).
   - `T2b chain r2`: FQ vs. E (raw) ($N=40$, $\Delta R^2 = +0.0242$).
   - `T4a 2x4 accuracy`: PQK-1 vs. PQK-2nn ($N=40$, $\Delta\text{acc} = -0.2218$; $N=80$, $\Delta\text{acc} = -0.1907$).
   - `T4a 2x4 accuracy`: PQK-2nn vs. E (raw) ($N=40$, $\Delta\text{acc} = -0.0192$; $N=80$, $\Delta\text{acc} = -0.0127$).
   - `T4a 3x4 accuracy`: PQK-1 vs. PQK-2nn ($N=40$, $\Delta\text{acc} = -0.1470$; $N=80$, $\Delta\text{acc} = -0.0725$).
   - `T4b 2x4 r2`: PQK-1 vs. PQK-2nn ($N=40$, $\Delta R^2 = -0.0775$; $N=80$, $\Delta R^2 = -0.0461$).
   - `T4b 2x4 r2`: FQ vs. E (raw) ($N=40$, $\Delta R^2 = -0.0320$; $N=80$, $\Delta R^2 = -0.0119$).
   - `T4b 3x4 r2`: PQK-1 vs. PQK-2nn ($N=40$, $\Delta R^2 = -0.0233$).

**Action Required for Manuscript:** The scope of $\le 0.011$ must be explicitly qualified as applying only to Task 1 at $N_{\mathrm{tr}} = 160$ ($|\Delta R^2| = 0.0012 \le 0.011$). It must not be presented as a universal ceiling.

---

## 2. Invariant Analysis: PQK-2nn vs. E2 (raw) Representation Equivalence (Item M2)

In the original manuscript drafts, $E_2(\text{raw})$ and $\text{PQK-2nn}$ were tabulated as if they represented distinct physical models with independent empirical performance ($R^2 = 0.9786$ vs. $0.9789$ at $N=40$, and $0.9942$ vs. $0.9943$ at $N=160$).

However, the dedicated ablation (`results/ablations/t1_e2_pqkgrid.csv`) and algebraic analysis established that:
1. Both models construct an RBF kernel over identical 2-body connected correlator features (the $B == C$ invariant).
2. The minute observed numerical discrepancy in `t1_entropy_gridv3.csv` ($+0.000259$ at $N=40$, $+0.000079$ at $N=160$) was solely caused by an arbitrary difference in normalizer grid sizing:
   - PQK-2nn used a feature dimension scaling of $4n = 32$.
   - E2 used a feature dimension scaling of $5(n-1) = 35$.
3. When evaluated on the same grid (as verified in Stage 2 and Stage 3 with `raw_4n_grid`), the outputs of PQK-2nn and E2 are identically zero to machine precision ($\max |\Delta| = 0.00\times 10^{0}$).

**Conclusion:** The two models are mathematically identical physical representations. The narrative distinction in earlier drafts was an artifact of hyperparameter grid discretization, not physical separation.

---

## 3. Detailed Task 1 Model Means Across Training Sizes ($N_{\mathrm{tr}} \in [10, 20, 40, 80, 160]$)

| $N_{\mathrm{tr}}$ | Model | Mean $R^2$ | Sample SE | 95% Bootstrap CI | Mean MAE | Sample SE |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 10 | PQK-1 | 0.7477 | 0.0188 | [0.7106, 0.7819] | 0.0856 | 0.0030 |
| 10 | PQK-2nn | 0.8520 | 0.0245 | [0.8013, 0.8950] | 0.0639 | 0.0055 |
| 10 | FQ | 0.8916 | 0.0164 | [0.8584, 0.9207] | 0.0555 | 0.0046 |
| 10 | E (raw) | 0.8305 | 0.0312 | [0.7653, 0.8837] | 0.0678 | 0.0062 |
| 10 | E (std) | 0.8161 | 0.0146 | [0.7874, 0.8433] | 0.0754 | 0.0030 |
| 10 | E2 (raw) | 0.8661 | 0.0174 | [0.8313, 0.8981] | 0.0617 | 0.0044 |
| 10 | F (std) | 0.8192 | 0.0167 | [0.7862, 0.8498] | 0.0750 | 0.0036 |
| 20 | PQK-1 | 0.8565 | 0.0102 | [0.8364, 0.8755] | 0.0650 | 0.0021 |
| 20 | PQK-2nn | 0.9555 | 0.0051 | [0.9447, 0.9640] | 0.0331 | 0.0012 |
| 20 | FQ | 0.9795 | 0.0019 | [0.9757, 0.9826] | 0.0228 | 0.0011 |
| 20 | E (raw) | 0.9754 | 0.0017 | [0.9722, 0.9785] | 0.0249 | 0.0010 |
| 20 | E (std) | 0.9273 | 0.0084 | [0.9099, 0.9420] | 0.0455 | 0.0026 |
| 20 | E2 (raw) | 0.9560 | 0.0048 | [0.9460, 0.9641] | 0.0329 | 0.0012 |
| 20 | F (std) | 0.9284 | 0.0063 | [0.9156, 0.9395] | 0.0454 | 0.0021 |
| 40 | PQK-1 | 0.8986 | 0.0070 | [0.8847, 0.9111] | 0.0538 | 0.0015 |
| 40 | PQK-2nn | 0.9789 | 0.0027 | [0.9731, 0.9833] | 0.0221 | 0.0010 |
| 40 | FQ | 0.9902 | 0.0007 | [0.9889, 0.9915] | 0.0152 | 0.0004 |
| 40 | E (raw) | 0.9872 | 0.0012 | [0.9847, 0.9893] | 0.0169 | 0.0006 |
| 40 | E (std) | 0.9801 | 0.0017 | [0.9767, 0.9833] | 0.0220 | 0.0007 |
| 40 | E2 (raw) | 0.9786 | 0.0028 | [0.9727, 0.9833] | 0.0221 | 0.0011 |
| 40 | F (std) | 0.9728 | 0.0030 | [0.9663, 0.9776] | 0.0261 | 0.0013 |
| 80 | PQK-1 | 0.9306 | 0.0039 | [0.9227, 0.9376] | 0.0445 | 0.0011 |
| 80 | PQK-2nn | 0.9895 | 0.0006 | [0.9883, 0.9905] | 0.0154 | 0.0004 |
| 80 | FQ | 0.9941 | 0.0004 | [0.9933, 0.9949] | 0.0117 | 0.0003 |
| 80 | E (raw) | 0.9961 | 0.0003 | [0.9955, 0.9966] | 0.0096 | 0.0003 |
| 80 | E (std) | 0.9925 | 0.0005 | [0.9915, 0.9935] | 0.0141 | 0.0005 |
| 80 | E2 (raw) | 0.9895 | 0.0007 | [0.9881, 0.9906] | 0.0155 | 0.0004 |
| 80 | F (std) | 0.9846 | 0.0007 | [0.9833, 0.9860] | 0.0192 | 0.0005 |
| 160 | PQK-1 | 0.9529 | 0.0012 | [0.9505, 0.9553] | 0.0369 | 0.0005 |
| 160 | PQK-2nn | 0.9943 | 0.0004 | [0.9936, 0.9950] | 0.0113 | 0.0004 |
| 160 | FQ | 0.9975 | 0.0002 | [0.9972, 0.9978] | 0.0076 | 0.0002 |
| 160 | E (raw) | 0.9987 | 0.0001 | [0.9986, 0.9989] | 0.0054 | 0.0002 |
| 160 | E (std) | 0.9965 | 0.0002 | [0.9961, 0.9969] | 0.0097 | 0.0003 |
| 160 | E2 (raw) | 0.9942 | 0.0004 | [0.9935, 0.9950] | 0.0114 | 0.0004 |
| 160 | F (std) | 0.9887 | 0.0004 | [0.9878, 0.9894] | 0.0168 | 0.0003 |

---
*Report generated programmatically by `docs/stage5/source_reconciliation_20261023_225751Z/run_source_reconciliation.py`.*
