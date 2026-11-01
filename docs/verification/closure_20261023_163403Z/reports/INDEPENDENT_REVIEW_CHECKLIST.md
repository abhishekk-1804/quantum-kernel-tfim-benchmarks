# Independent Technical Review Checklist

**Status:** Independent Human Review Pending  
**Closure Package:** `docs/verification/closure_20261023_163403Z/`  

This checklist allows an independent human reviewer to independently verify all primary mathematical and statistical claims of the benchmark audit without relying on complex internal pipeline orchestration.

All commands should be executed from the repository root (`D:\quantum-kernel-tfim-benchmarks`) using Python with NumPy, SciPy, and Pandas.

---

## Check 1: Recalculate Covariance Standardized Discrepancy
- **Input Path:** `docs/verification/audit_20261023_155335Z/covariance_diagnostic.csv`
- **Mathematical Formula:** $z = \frac{|\operatorname{Cov}_{\text{emp}} - \operatorname{Cov}_{\text{theo}}|}{\operatorname{SE}_{\text{MC}}}$
- **Expected Result:** $z = 0.017842 \approx 0.018$ ($p = 0.986$). Note: Resolves transcription error in narrative report ($z=0.58$).
- **Acceptance Tolerance:** $|z - 0.017842| < 10^{-5}$
- **Standalone Python Command:**
```python
import pandas as pd
df = pd.read_csv('docs/verification/audit_20261023_155335Z/covariance_diagnostic.csv')
emp, theo, se = df['production_empirical_cov'].iloc[0], df['theoretical_covariance'].iloc[0], df['production_cov_se'].iloc[0]
z = abs(emp - theo) / se
print(f'Empirical: {emp:.6e}, Theo: {theo:.6e}, SE: {se:.6e}')
print(f'Computed z-score: {z:.6f}')
```
- **Reviewer Findings:** [ ] Passed  [ ] Discrepancy Observed  
  *Notes:* ___________________________________________________

---

## Check 2: Verify Exact 2-RDM to Classical Correlator Distance Identity
- **Input Path:** `docs/verification/audit_20261023_155335Z/representation_distance_checks.csv`
- **Mathematical Identity:** $D_{\text{RDM}}(\psi_a, \psi_b) = \frac{1}{4} \| \mathbf{f}_{E2}(\psi_a) - \mathbf{f}_{E2}(\psi_b) \|_2^2$
- **Row Identifier:** `state_a = 0, state_b = 1`
- **Expected Result:** Absolute discrepancy $= 0.00e+00$ (identical to machine precision)
- **Acceptance Tolerance:** Discrepancy $< 10^{-12}$
- **Standalone Python Command:**
```python
import pandas as pd
df = pd.read_csv('docs/verification/audit_20261023_155335Z/representation_distance_checks.csv')
row = df[(df['state_a'] == 0) & (df['state_b'] == 1)].iloc[0]
diff = abs(row['d_rdm_frobenius'] - row['d_prod_e2_div4'])
print(f"D_RDM: {row['d_rdm_frobenius']:.8f}, D_E2/4: {row['d_prod_e2_div4']:.8f}, Discrepancy: {diff:.2e}")
```
- **Reviewer Findings:** [ ] Passed  [ ] Discrepancy Observed  
  *Notes:* ___________________________________________________

---

## Check 3: Recalculate Seed 00 OOD MAE and R² from Saved Prediction Arrays
- **Input Path:** `docs/verification/audit_20261023_155335Z/predictions/seed_00_arrays.npz`
- **Identifiers:** Seed `00`, Model `FQ`, Test Split `OOD`
- **Expected Result:** $\text{MAE} = 0.030009$, $R^2 = -1.979849$
- **Acceptance Tolerance:** $|\Delta \text{MAE}| < 10^{-5}, |\Delta R^2| < 10^{-5}$
- **Standalone Python Command:**
```python
import numpy as np
from sklearn.metrics import mean_absolute_error, r2_score
npz = np.load('docs/verification/audit_20261023_155335Z/predictions/seed_00_arrays.npz')
mae = mean_absolute_error(npz['y_ood'], npz['fq_pred_ood'])
r2 = r2_score(npz['y_ood'], npz['fq_pred_ood'])
print(f'Seed 00 FQ OOD MAE: {mae:.6f}, R2: {r2:.6f}')
```
- **Reviewer Findings:** [ ] Passed  [ ] Discrepancy Observed  
  *Notes:* ___________________________________________________

---

## Check 4: Recalculate Seed 00 Constant Training-Mean Baseline MAE
- **Input Path:** `docs/verification/audit_20261023_155335Z/predictions/seed_00_arrays.npz`
- **Formulas:** $\bar{y}_{\text{train}} = \frac{1}{N_{\text{tr}}} \sum_i y_{\text{train}, i}$; $\text{MAE} = \frac{1}{N_{\text{ood}}} \sum_j |y_{\text{ood}, j} - \bar{y}_{\text{train}}|$
- **Expected Result:** $\bar{y}_{\text{train}} = 0.392399$, $\text{MAE} = 0.600949$
- **Acceptance Tolerance:** $|\Delta \text{MAE}| < 10^{-5}$
- **Standalone Python Command:**
```python
import numpy as np
from sklearn.metrics import mean_absolute_error
npz = np.load('docs/verification/audit_20261023_155335Z/predictions/seed_00_arrays.npz')
c_mean = np.mean(npz['y_train'])
mae_bl = mean_absolute_error(npz['y_ood'], np.full_like(npz['y_ood'], c_mean))
print(f'Train Mean: {c_mean:.6f}, Baseline MAE: {mae_bl:.6f}')
```
- **Reviewer Findings:** [ ] Passed  [ ] Discrepancy Observed  
  *Notes:* ___________________________________________________

---

## Check 5: Reconstruct SVR Predictions from Dual Parameters
- **Input Path:** `docs/verification/audit_20261023_155335Z/predictions/seed_00_arrays.npz`
- **Mathematical Formula:** $\hat{y}(x) = \sigma_{\text{tr}} [K_{\text{ood}}(x, \text{supp}) \cdot \boldsymbol{\alpha} + b_z] + \mu_{\text{tr}}$
- **Expected Result:** $\max |\hat{y}_{\text{reconstructed}} - \hat{y}_{\text{saved}}| < 10^{-14}$
- **Acceptance Tolerance:** Maximum discrepancy $< 10^{-11}$
- **Standalone Python Command:**
```python
import numpy as np
npz = np.load('docs/verification/audit_20261023_155335Z/predictions/seed_00_arrays.npz')
y_tr = npz['y_train']
mu, sig = np.mean(y_tr), np.std(y_tr, ddof=0)
g_z = npz['fq_K_ood'][:, npz['fq_support']] @ npz['fq_dual_coef']
p_recon = (g_z + float(npz['fq_intercept'])) * sig + mu
err = np.max(np.abs(p_recon - npz['fq_pred_ood']))
print(f'Max SVR reconstruction error: {err:.2e}')
```
- **Reviewer Findings:** [ ] Passed  [ ] Discrepancy Observed  
  *Notes:* ___________________________________________________

---

## Check 6: Recalculate Holm-Bonferroni Correction from Exported Raw P-Values
- **Input Path:** `docs/verification/closure_20261023_163403Z/tables/mae_family_original_rechecked.csv`
- **Formula:** For $m=3$ tests sorted in ascending order of raw $p$: $p_{(1)} \to 3 p_{(1)}$, $p_{(2)} \to \max(2 p_{(2)}, p_{\text{adj},(1)})$, $p_{(3)} \to \max(1 p_{(3)}, p_{\text{adj},(2)})$
- **Expected Result:**
  - `FQ vs Train-Mean`: $p_{\text{raw}} = 1.9073 \times 10^{-6} \implies p_{\text{holm}} = 5.7220 \times 10^{-6}$
  - `FQ vs Train-Median`: $p_{\text{raw}} = 1.9073 \times 10^{-6} \implies p_{\text{holm}} = 5.7220 \times 10^{-6}$
  - `FQ vs PQK-2nn`: $p_{\text{raw}} = 8.5068 \times 10^{-4} \implies p_{\text{holm}} = 8.5068 \times 10^{-4}$
- **Acceptance Tolerance:** Exact agreement to 6 significant digits
- **Standalone Python Command:**
```python
import pandas as pd
df = pd.read_csv('docs/verification/closure_20261023_163403Z/tables/mae_family_original_rechecked.csv')
print(df[['comparison_id', 'raw_pval', 'holm_pval_3_comp_family']])
```
- **Reviewer Findings:** [ ] Passed  [ ] Discrepancy Observed  
  *Notes:* ___________________________________________________
