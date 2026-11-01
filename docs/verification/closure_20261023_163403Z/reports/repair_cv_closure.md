# Forensic Audit of Gram Repairs, Cross-Validation, and Information Flow

## 1. Executive Verdict and Scope

This audit rigorously tracks the flow of covariate and label information across all kernel repair modes, inner cross-validation folds, preprocessing pipelines, and final evaluation test blocks in Stages 2 and 3.

- **Label Leakage:** **COMPLETELY ABSENT**. In no stage, fold, or repair method are held-out test labels ($y_{\text{test}}$ or $y_{\text{val}}$) ever accessed, standardized against, or consulted during training, PSD projection, or model selection.
- **Covariate Leakage in Production Benchmarks:** **COMPLETELY ABSENT**. The production deployable pipeline utilizes `repair_train_only`, which clips solely $K_{\text{tr}}$ and leaves $K_{\text{te}}$ untouched. Neither training eigenvalues nor support vectors depend in any way on held-out test states.
- **Transductive Ablation Isolation:** The transductive method `repair_joint` was implemented exclusively as an ablation control in Stage 1b to measure the impact of unsupervised transductive feature leakage, and was correctly excluded from all confirmatory production benchmarks in Stages 2 and 3.

## 2. Granular Data Flow and Information Trace Matrix

| component | source_location | training_kernel_construction | repair_timing | validation_test_generation | held_out_covariates_used | held_out_labels_used | target_standardization_fitted | classification | impact_on_tested_claims |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| repair_none (Raw FQ) | scripts/ablation_r3_repairs.py:42-46 | Direct empirical swap-test/sampling estimate K_tr | None (unrepaired) | Direct empirical estimate K_te, unaltered | No | No | Strictly on training fold targets | Inductive fold-local processing | Does not affect claim; establishes raw baseline |
| repair_train_only (Production FQ) | scripts/ablation_r3_repairs.py:49-55; stage2_equal_budget.py:75-80 | K_tr symmetrized and clipped to PSD cone via fidelity_clip_psd | Fitted strictly on training Gram block K_tr | K_te left completely unclipped and unaltered (K_te.copy()) | No (K_te completely isolated) | No | Strictly on training fold targets | Inductive fold-local processing | Does not affect claim; verified zero information leakage |
| repair_inductive (Out-of-Sample Spectral) | scripts/ablation_r3_repairs.py:58-96 | Eigendecomposition of K_tr = U diag(L) U^T; clipping L_clip = max(L, 0) | Eigenbasis U and filter factors f computed strictly from K_tr | K_te transformed via K_te' = K_te U diag(f) U^T and rescaled by training diagonal | No (operator is fixed by K_tr before applying to K_te) | No | Strictly on training fold targets | Inductive fold-local processing | Does not affect claim; demonstrates out-of-sample PSD projection |
| repair_joint (Transductive Control) | scripts/ablation_r3_repairs.py:99-112 | Joint (N_tr + N_te) Gram matrix clipped to PSD cone; K_tr sliced from joint | Fitted globally across train and test states simultaneously | K_te sliced from jointly clipped Gram matrix | Yes (test states influence training eigenvalues) | No (labels never used) | Strictly on training fold targets | Unsupervised transductive processing | Ablation control only; NOT used in production Stage 2/3 benchmarks |
| Inner Cross-Validation (Stage 2/3 SVR) | scripts/stage2_equal_budget.py:310-370; stage3_ood_shift.py:280-350 | KFold(n_splits=3/5, shuffle=True, random_state=42) on N_train=40 instances | Fold-local within inner CV; global on training set for final fit | Validation folds evaluate fold-local models; final test evaluates refit model | No (test set held out until final evaluation) | No (hyperparameter tuning uses only training-fold CV scores) | Fold-local during CV; refit on full N_train=40 for final evaluation | Inductive fold-local processing | Does not affect claim; follows standard supervised ML isolation standards |

## 3. Evaluation of Inner Cross-Validation and Final Model Refitting

### 3.1 Inner-Fold Isolation
1. **Data Partitioning:** In `scripts/stage2_equal_budget.py` (lines 310-330) and `scripts/stage3_ood_shift.py` (lines 280-310), $K$-fold cross-validation operates strictly on the $N_{\text{train}} = 40$ training instances.
2. **Target Standardization:** The target transformation parameters $\mu_{\text{fold}}$ and $\sigma_{\text{fold}}$ are computed exclusively from the training indices of that fold, preventing validation fold target leakage.
3. **Hyperparameter Selection:** The grid search across regularization penalty $C$, bandwidth $c$, and tolerance $\epsilon$ optimizes the mean squared error across the held-out inner validation folds.

### 3.2 Final Model Refitting & Out-of-Sample Evaluation
1. Once optimal hyperparameters $(C^*, c^*, \epsilon^*)$ are selected, the SVR model is refitted once on the complete training set ($N_{\text{train}} = 40$).
2. The held-out test blocks ($N_{\text{test,ID}} = 100$, $N_{\text{test,OOD}} = 100$) are presented to the refitted model strictly as out-of-sample covariates.
3. Inverse standardization transforms predictions back to physical units using $\mu_{\text{train}}$ and $\sigma_{\text{train}}$, ensuring complete consistency.
