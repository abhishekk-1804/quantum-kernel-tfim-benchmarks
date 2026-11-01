# Uncertainty Values and Descriptive Statistics Verification

## 1. Verified Descriptive Statistics (N = 20 Seeds)

All statistics are computed directly from the unrounded float64 vectors with Bessel's correction (sample variance with `ddof=1`):

| Vector | Count | Mean | Sample SD | Sample SE (SD/√N) | Min | Max |
|---|---|---|---|---|---|---|
| FQ OOD MAE | 20 | 0.060181 | 0.038100 | **0.008519** | 0.026945 | 0.186101 |
| PQK-2nn OOD MAE | 20 | 0.185030 | 0.131658 | **0.029440** | 0.032773 | 0.502865 |
| Paired difference (FQ minus PQK-2nn) | 20 | -0.124849 | 0.149481 | **0.033425** | -0.444919 | 0.153329 |
| FQ Intercept-only OOD MAE | 20 | 0.461597 | 0.072487 | **0.016209** | 0.283620 | 0.585750 |
| Full minus Intercept OOD MAE | 20 | -0.401417 | 0.069824 | **0.015613** | -0.549732 | -0.215245 |

### Numerical Identity Check:
- mean(FQ - PQK2) = -0.12484924959269612
- mean(FQ) - mean(PQK2) = -0.12484924959269617
- Discrepancy: `4.16e-17` (identity holds exactly to machine precision).

## 2. Historical Uncertainty Claims Reconciliation

A critical objective of this audit was verifying whether previously proposed standard error values (`FQ: 0.0039`, `PQK-2nn: 0.0154`, `Paired diff: 0.0166`, `Intercept: 0.0042`) reproduce from the data.

| Quantity | Historical Claimed SE | Actual Calculated SE | Actual Sample SD | Verdict |
|---|---|---|---|---|
| FQ OOD MAE Standard Error | `0.0039` | **`0.008519`** | `0.038100` | **Does not reproduce** |
| PQK-2nn OOD MAE Standard Error | `0.0154` | **`0.029440`** | `0.131658` | **Does not reproduce** |
| Paired Difference Standard Error (FQ - PQK2) | `0.0166` | **`0.033425`** | `0.149481` | **Does not reproduce** |
| FQ Intercept-Only OOD MAE Standard Error | `0.0042` | **`0.016209`** | `0.072487` | **Does not reproduce** |

### Root Cause Analysis:
1. **None of the proposed historical SE values reproduce.** In all cases, the true standard error computed as $s / \sqrt{20}$ is substantially larger than the claimed numbers (e.g. true paired SE is $0.0334$, not $0.0166$; true FQ SE is $0.0085$, not $0.0039$).
2. **Origins of Claimed Numbers:**
   - `0.0042` and `0.0039` are present in `t6_ood_shift.csv` as *in-distribution* MAEs (Seed 0 FQ `id_mae` = 0.004204) and hyperparameter values (`gamma=0.00395285`), respectively.
   - `0.0166` is approximately half the true paired SE ($0.033425 / 2 = 0.01671$), suggesting an accidental division by 2 or division by $\sqrt{80}$ rather than $\sqrt{20}$.
3. **Authoritative Mandate:** For all future manuscript drafting and reporting, only the actual verified sample standard errors ($s / \sqrt{20}$) must be used:
   - FQ OOD MAE: **$0.0602 \pm 0.0085$**
   - PQK-2nn OOD MAE: **$0.1850 \pm 0.0294$**
   - Paired Difference (FQ - PQK-2nn): **$-0.1248 \pm 0.0334$**
   - Intercept-Only OOD MAE: **$0.4616 \pm 0.0162$**
