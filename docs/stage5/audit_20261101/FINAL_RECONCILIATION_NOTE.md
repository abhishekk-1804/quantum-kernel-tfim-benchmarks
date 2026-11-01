# Final Reconciliation Note: Figure 2, OOD Baselines, and Artifact Regeneration Status

**Workspace:** `D:\quantum-kernel-tfim-benchmarks`  
**Date:** `2026-11-01`  
**Permitted Audit Directory:** `docs/stage5/audit_20261101/`  
**Machine-Readable Table:** [final_reconciliation.csv](file:///d:/quantum-kernel-tfim-benchmarks/docs/stage5/audit_20261101/final_reconciliation.csv)  
**Safety & Guardrails:** Strictly read-only on `paper/*`, `results/*`, `src/*`, `tests/*`, and pre-existing `scripts/*`. No git writes, no manuscript modifications, and no forged review sign-offs.

---

## 1. Figure 2 Reconciliation

### A. Exact Filters, Model Arms, and Sample Sizes
From `results/t5_noise.csv`:
- **Primary Filter:** `experiment == "finite_shots"` and `metric == "r2"`
- **Model Arms & Variants:**
  * `model == "FQ-raw"`, `variant == "none"` (unmitigated raw SVR, dashed line with marker `x`)
  * `model == "FQ-clipped"`, `variant == "none"` (training Gram matrix PSD-clipped via eigenvalue thresholding at $0$, solid line with marker `^`)
  * `model == "PQK-2nn"`, `variant == "none"`
  * `model == "PQK-1"`, `variant == "none"`
  * `model == "E"`, `variant == "raw"`
  * `model == "E2"`, `variant == "raw"`
  * `model == "F"`, `variant == "std"`
- **Training Set Size:** $N_{\mathrm{tr}} = 40$ (evaluated on test set $N_{\mathrm{te}} = 200$)
- **Seed Count:** 20 fixed random seeds ($0..19$)
- **Shot Budgets Evaluated:** $S \in \{100.0, 1000.0, 10000.0\}$ per measurement setting/pair, plus $S = \infty$ (statevector limit)
- **Plotted X-Axis Metrics (in `scripts/make_figures.py:make_f5()`):**
  * Panel (a) Deployed Evaluation Cost: $(780 + 8000) \cdot S = 8{,}780 \cdot S$ shots for FQ; $720 \cdot S$ for 3-basis models ($3 \times 240$ states); $480 \cdot S$ for PQK-1 ($2 \times 240$ states).
  * Panel (b) Full-Gram Simulation Cost: $28{,}680 \cdot S$ shots for FQ ($\binom{240}{2} = 28{,}680$ pairs); $720 \cdot S$ for 3-basis models.

### B. Empirical Performance Metrics for Raw and Clipped FQ
All metrics computed across the 20 seeds with 95% percentile bootstrap confidence intervals ($10{,}000$ resamples, seed `20261022` per plotting script):

| Shot Level | Model Arm | Mean Test $R^2$ | Sample SD | Sample SE | 95% Bootstrap CI | Median | Min | Max |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **$S = 100$** | `FQ-raw` | **$0.763351$** | $0.047635$ | $0.010652$ | $[0.7433, 0.7841]$ | $0.757764$ | $0.671853$ | $0.862281$ |
| **$S = 100$** | `FQ-clipped` | **$0.810063$** | $0.042880$ | $0.009588$ | $[0.7920, 0.8279]$ | $0.812675$ | $0.732449$ | $0.875949$ |
| **$S = 1000$** | `FQ-raw` | **$0.889398$** | $0.034130$ | $0.007632$ | $[0.8747, 0.9038]$ | $0.897745$ | $0.822569$ | $0.932442$ |
| **$S = 1000$** | `FQ-clipped` | **$0.869345$** | $0.096087$ | $0.021486$ | $[0.8247, 0.9045]$ | $0.910263$ | $0.555674$ | $0.942682$ |
| **$S = 10000$** | `FQ-raw` | **$0.861270$** | $0.049074$ | $0.010973$ | $[0.8394, 0.8812]$ | $0.876660$ | $0.748977$ | $0.922139$ |
| **$S = 10000$** | `FQ-clipped` | **$0.963022$** | $0.015544$ | $0.003476$ | $[0.9553, 0.9686]$ | $0.968757$ | $0.906797$ | $0.975705$ |

### C. Resolution of 0.7686 versus 0.8101 at $S = 100$
1. **Ground Truth Evidence:**
   - At $S=100$, the sample mean test $R^2$ of unmitigated `FQ-raw` is **$0.7634$** (exact: $0.763351$, 95% CI $[0.7433, 0.7841]$).
   - The sample mean test $R^2$ of `FQ-clipped` is **$0.8101$** (exact: $0.810063$, 95% CI $[0.7920, 0.8279]$).
2. **Provenance Trace of 0.7686:**
   - A literal value of `0.768676` exists in `results/t5_noise.csv` (lines 1792-1793) as the 5-fold cross-validation `inner_cv_score` for model `PQK-2nn`, seed 6, at $S=100$.
   - A literal value of `0.768603` exists in `results/t1_entropy_gridv2.csv` (line 776) as the test $R^2$ of `PQK-2nn` at $N_{\mathrm{tr}}=10$, seed 7.
   - In `results/ablations/t5_fq_repairs.csv`, the inductive repair arm has mean $R^2 = 0.7621$, `none` (raw) has mean $0.7634$, and `train_only` (clipped) has mean $0.8101$.
3. **Conclusion:**
   - The figure of $0.7686$ cited in review inquiries is a **numerical misattribution / typographical corruption** for the verified FQ-raw sample mean of **$0.7634$** ($0.763351$). The performance gain from PSD clipping at $S=100$ is $\Delta R^2 = 0.8101 - 0.7634 = +0.0467$.

---

## 2. Stage 3 OOD Baseline Reconciliation

### A. Independent Baseline Definitions
1. **Train-Mean Baseline (Zero-Parameter Empirical Baseline):**
   - **Mathematical Definition:** A trivial predictor that predicts the constant empirical mean of the training labels for all test queries:
     $$\hat{y}_{\mathrm{OOD}}(x) = \bar{y}_{\mathrm{train}} = \frac{1}{N_{\mathrm{tr}}} \sum_{i=1}^{N_{\mathrm{tr}}} y_i^{\mathrm{train}}$$
   - **Code Implementation:** `pred_mean = np.full_like(y_ood, np.mean(y_tr))` in `scripts/audit_stage3_metrics.py:682`.
   - **Nature:** Completely featureless and model-free. Measures target distribution shift from in-distribution ($h_i \in [0.8, 1.5]$) to out-of-distribution ($h_i \in [0.2, 0.7]$).
2. **FQ Intercept-Only Baseline (Model Regularization Floor):**
   - **Mathematical Definition:** The prediction of the fitted FQ dual SVR model when all dual kernel weights are zeroed ($\boldsymbol{\alpha} = \mathbf{0}$):
     $$f(x) = \sum_{i \in \mathrm{SV}} \alpha_i K(x_i, x) + b \quad \xrightarrow{\boldsymbol{\alpha} \to \mathbf{0}} \quad f_{\mathrm{intercept}}(x) = b$$
     Transformed back from standardized target units ($z = (y - \mu_y)/\sigma_y$) to physical entanglement entropy units:
     $$\hat{y}_{\mathrm{OOD}}(x) = b_{\mathrm{physical}} = b_z \cdot \sigma_y^{\mathrm{train}} + \mu_y^{\mathrm{train}}$$
   - **Code Implementation:** `pred_intercept_only = np.full_like(y_ood, intercept_phys)` in `scripts/audit_stage3_metrics.py:874`.
   - **Nature:** Evaluates whether FQ's OOD accuracy derives solely from regularized bias shrinkage ($b$) versus active kernel-driven pattern matching ($g(x) = \sum_i \alpha_i K(x_i, x)$).

### B. Direct Empirical Verification from Raw Saved Prediction Arrays
Evaluated directly on the 20 raw prediction files `docs/verification/audit_20261023_155335Z/predictions/seed_*_arrays.npz` ($N_{\mathrm{tr}}=40$, $N_{\mathrm{ood}}=100$, 20 seeds):

#### 1. Baseline Performance Summary:
- **FQ Full Model:** Mean OOD MAE = **$0.060181 \pm 0.008519$** (SD = $0.038100$)
- **PQK-2nn Full Model:** Mean OOD MAE = **$0.185030 \pm 0.029440$** (SD = $0.131658$)
- **FQ Intercept-Only Baseline:** Mean OOD MAE = **$0.461597 \pm 0.016209$** (SD = $0.072487$)
- **Train-Mean Baseline:** Mean OOD MAE = **$0.606095 \pm 0.005707$** (SD = $0.025523$)

#### 2. Paired Statistical Tests ($\Delta\mathrm{MAE} = \mathrm{MAE}_{\mathrm{FQ}} - \mathrm{MAE}_{\mathrm{Baseline}}$):

| Comparison | Mean Difference ($\Delta\mathrm{MAE}$) | Sample SD | Sample SE | 95% Bootstrap CI | Wilcoxon $W$ | Raw $p$-value | Holm $p$-value | Seed-Win Count |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **FQ vs PQK-2nn** | **$-0.124849$** | $0.149481$ | $0.033425$ | $[-0.1899, -0.0630]$ | $21.0$ | $8.51 \times 10^{-4}$ | $8.51 \times 10^{-4}$ | **16 / 20** |
| **FQ vs FQ Intercept-Only** | **$-0.401417$** | $0.069824$ | $0.015613$ | $[-0.4310, -0.3707]$ | $0.0$ | $1.91 \times 10^{-6}$ | $3.81 \times 10^{-6}$ | **20 / 20** |
| **FQ vs Train-Mean Baseline** | **$-0.545914$** | $0.033520$ | $0.007495$ | $[-0.5596, -0.5310]$ | $0.0$ | $1.91 \times 10^{-6}$ | $5.72 \times 10^{-6}$ | **20 / 20** |

### C. Resolution of Manuscript Line 200 Contradiction
- In `paper/main.tex:200`, the text states:
  > *"Evaluating FQ against the train-mean baseline further confirms that error is reduced by $-0.4014 \pm 0.0156$ MAE ($W=0.0$, $p=1.9 \times 10^{-6}$)..."*
- **Audit Finding:** The reported numeric reduction of **$-0.4014 \pm 0.0156$** is the difference between FQ and the **FQ Intercept-Only baseline**, **not** the Train-Mean baseline.
- The actual difference between FQ and the Train-Mean baseline is **$-0.5459 \pm 0.0075$** MAE.
- Both baselines yield $W=0.0$, $p=1.91 \times 10^{-6}$, and $20/20$ seed wins. The error is purely editorial mislabeling in the manuscript narrative.

---

## 3. Artifact Status & Reproducibility Boundaries

### A. Distinction of Status Categories

```mermaid
flowchart TD
    subgraph Data Layer ["Data & Simulation Layer (100% Intact)"]
        D1["results/t1_entropy_gridv3.csv"]
        D2["results/t5_noise.csv"]
        D3["results/stage2/t1_equal_budget.csv"]
        D4["results/stage3/t6_ood_shift.csv"]
        D5["Saved Prediction Arrays (seed_*.npz)"]
    end

    subgraph NoRerun ["Status: NO SIMULATION RERUN NEEDED"]
        R1["Bit preservation 100% verified"]
        R2["Zero missing seed observations"]
        R3["Dual coefficients & Gram matrices intact"]
    end

    subgraph Regen ["Status: REGENERATION / EDITORIAL NEEDED"]
        E1["Figure 2 PDF: Re-export with build SHA metadata"]
        E2["Table IV TeX: Adjust tabcolsep to eliminate 101.68 pt overfull hbox"]
        E3["Manuscript Lines 88, 149, 155, 172, 188, 198, 200, 227: Narrative errata"]
    end

    Data Layer --> NoRerun
    NoRerun -.->|"Plotting / Compiling"| Regen
```

1. **Category 1: NO SIMULATION RERUN NEEDED**
   - Primary benchmark data across all experimental stages (`results/*.csv` and `docs/verification/*/predictions/*.npz`) are complete, self-consistent, and bit-preserved against the pre-audit hash manifest (148/148 files matched).
   - No new quantum state eigensolves, Trotterizations, or shot-noise Monte Carlo draws are required.
2. **Category 2: REGENERATION / EDITORIAL UPDATES NEEDED**
   - **Figure 2 PDF (`paper/figures/fig_shots.pdf`):** While reproducible from `scripts/make_figures.py:make_f5()`, the existing PDF lacks embedded Git commit SHA metadata. Re-exporting via the build pipeline will tie the visual artifact directly to repository HEAD.
   - **Table IV LaTeX (`paper/tables/tab_equal_budget.tex`):** Needs column padding adjustment (`\tabcolsep = 3.0pt`) and header wrapping to fix the 101.68 pt margin violation.
   - **Manuscript Text (`paper/main.tex`):** Editorial corrections required for finite-shot numbers (Line 172), budget formulas (Line 188), and baseline labeling (Line 200).

### B. Evidentiary Boundary: Bit Preservation vs Reproducibility
- **Important Distinction:** Demonstrating 100% bit preservation of saved CSV files and arrays on the author workspace confirms data custody, absence of silent corruption, and internal consistency.
- Bit preservation **does not** by itself prove:
  * Platform-independent computational reproducibility across external architectures, compilers, or BLAS implementations.
  * Prospective validity of protocol design (both Stages 2 and 3 were committed atomically with output data in commits `dff01711` and `292d689d`).
- Therefore, in accordance with open-science standards, Stages 2 and 3 remain formally classified as:
  **`Exploratory (documented protocol, timing not established)`**.

### C. Explicitly Unresolved Items
1. **Historical PDF Build Lineage:** The exact timestamp and compiler environment of `paper/figures/fig_shots.pdf` cannot be reconstructed beyond filesystem modification time because no PDF metadata dictionary contains the Git commit hash.
2. **Prospective Protocol Timing:** Prospective registration of Stage 3 hypotheses prior to simulation execution is historically unresolvable from Git history alone.
