# Forensic Audit of Stage 3 Out-of-Distribution Metrics & Baselines

**Audit Identifier:** `audit_20261023_155335Z`  
**Execution Timestamp:** 2026-10-23T15:53:35Z  
**Statistical Convention:** Retrospective, 10,000 bootstrap resamples (seed `20261023`), SciPy 1.18.1.

## 1. Physical Target Variance & The Negative-$R^2$ Mechanism

- **Training Domain Variance:** $\operatorname{Var}(S_{\text{train}}) \approx 0.0216$. In the paramagnetic and critical regimes, entanglement entropy varies broadly ($S \in [0.10, 0.75]$).
- **OOD Domain Variance:** $\operatorname{Var}(S_{\text{OOD}}) \approx 0.000331$ ($S \in [0.90, 1.02]$).
- **Variance Compression:** The target variance in deep ferromagnetism compresses by a factor of **65.2×**! Because $R^2 = 1 - \operatorname{MSE} / \operatorname{Var}(y_{\mathrm{OOD}})$, a tiny denominator (~ 0.0004) causes any model with a modest mean offset to produce large negative $R^2$ values.
- **Methodological Warning:** Ratios of negative $R^2$ scores **must never be interpreted as error ratios**. MAE and RMSE are the only physically meaningful metrics under severe target variance compression.

## 2. Retrospective Paired MAE Comparison Family

| Comparison ($a$ vs $b$) | Mean Diff | Median Diff | SE Diff | 95% Bootstrap CI | Wilcoxon $W$ | Raw $p$ | Holm $p$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `FQ vs PQK-2nn` | **-0.1248** | -0.1206 | 0.0334 | [-0.1899, -0.0630] | 21.0 | 8.5068e-04 | **8.5068e-04** |
| `FQ vs Train-Mean Baseline` | **-0.5459** | -0.5526 | 0.0075 | [-0.5596, -0.5310] | 0.0 | 1.9073e-06 | **5.7220e-06** |
| `FQ vs Train-Median Baseline` | **-0.5520** | -0.5538 | 0.0086 | [-0.5682, -0.5356] | 0.0 | 1.9073e-06 | **5.7220e-06** |

## 3. Comparison with Constant Baselines

- **Training-Target Mean Baseline:** An uninformed model predicting the constant mean of D_train (mean_y ~ 0.42) achieves MAE = 0.6061.
- **Fidelity Quantum Kernel (`FQ`):** Achieves MAE = 0.0602, outperforming the constant training-mean baseline by 0.5459 MAE (p = 5.7220e-06).
- **Interpretation:** Even under complete phase transition, `FQ` predictions do not simply revert to the training mean; the kernel structure actively places predictions closer to the true physical range.

