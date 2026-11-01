# Forensic Audit of Gram Repairs, Cross-Validation, and Information Flow

**Audit Identifier:** `audit_20261023_155335Z`  
**Execution Timestamp:** 2026-10-23T15:53:35Z  

## 1. Gram Repair Modes & Mathematical Implementations

The candidate benchmark in `scripts/stage2_equal_budget.py` and `scripts/ablation_r3_repairs.py` evaluates three FQ variants:

### 1.1 `train_only` (Primary Deployable FQ)
- **Implementation (`repair_train_only`):**
  ```python
  def repair_train_only(K_tr, K_te):
      K_tr_clipped = fidelity_clip_psd(K_tr)
      return K_tr_clipped, K_te.copy()
  ```
- **Mathematical Mechanism:** Symmetrizes $K_{\text{tr}}$ and clips negative eigenvalues to zero ($L_{\text{clip}} = \max(L, 0)$), then scales by diagonal factor $D^{-1/2} K D^{-1/2}$ to enforce unit diagonal. The test block $K_{\text{te}}$ is left completely unaltered.
- **Information Flow Assessment:** **ZERO LEAKAGE**. $K_{\text{te}}$ is neither consulted nor modified. Training-set eigenvalues are derived strictly from $K_{\text{tr}}$.

### 1.2 `none` (Raw Baseline)
- **Implementation:** Uses raw empirical swap-test estimates $\hat{K}$ directly without spectral clipping or PSD projection.
- **Information Flow Assessment:** **ZERO LEAKAGE**.

### 1.3 `inductive` (Out-of-Sample Spectral Filtering)
- **Implementation (`repair_inductive`):**
  Computes eigendecomposition $K_{\text{tr}} = U \Lambda U^T$. Projects test evaluations onto training eigenspace:
  $$K_{\text{te}}' = K_{\text{te}} U \operatorname{diag}(f) U^T$$
  where $f_i = \max(\lambda_i, 0) / \lambda_i$ if $\lambda_i > 10^{-10}$ else $0.0$.
- **Inductivity Verification:** The transformation basis $U$ and filter factors $f$ are computed **strictly from $K_{\text{tr}}$**. Test covariates $K_{\text{te}}$ are transformed linearly via an operator fixed by training data. Test labels $y_{\text{test}}$ are never used.
- **Classification:** Unsupervised inductive feature mapping. Label leakage is **ABSENT**.

## 2. Inner Cross-Validation and Preprocessing Audit

1. **Fold Splitting:**
   `kf = KFold(n_splits=3, shuffle=True, random_state=42)` operates strictly on $N_{\text{train}} = 40$ training instances.
2. **Standardization & Scaling:**
   - Target standardization parameters ($y_{\text{mean}}, y_{\text{std}}$) are computed strictly on training targets `tr_targets`.
   - Within inner CV folds, fold-specific means ($f_m$) and standard deviations ($f_s$) are fitted solely on training folds.
3. **Hyperparameter Selection:**
   - Grid search over $(C, c, \epsilon)$ is scored exclusively on validation folds (`val_idx`).
   - Test data ($N_{\text{test}} = 200$) is never consulted during model selection.
4. **Refitting:**
   - Final SVR model is refitted on the complete $40 \times 40$ training matrix before a single evaluation on test data.

## 3. Findings & Integrity Verdict

- **Status:** `SUPPORTED WITHIN TESTED SCOPE`.
- **Summary:** The candidate implementation of Gram repairs and inner-CV follows rigorous supervised learning isolation standards without covariate or label leakage from the test domain.
