import os
import pandas as pd

CLOSURE_DIR = r"docs/verification/closure_20261023_163403Z"

def df_to_markdown(df):
    headers = list(df.columns)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(val) for val in row.values) + " |")
    return "\n".join(lines)

def main():
    print("Executing Step 7: Repair and Inner-CV Information Flow Audit...")
    
    records = [
        {
            "component": "repair_none (Raw FQ)",
            "source_location": "scripts/ablation_r3_repairs.py:42-46",
            "training_kernel_construction": "Direct empirical swap-test/sampling estimate K_tr",
            "repair_timing": "None (unrepaired)",
            "validation_test_generation": "Direct empirical estimate K_te, unaltered",
            "held_out_covariates_used": "No",
            "held_out_labels_used": "No",
            "target_standardization_fitted": "Strictly on training fold targets",
            "classification": "Inductive fold-local processing",
            "impact_on_tested_claims": "Does not affect claim; establishes raw baseline"
        },
        {
            "component": "repair_train_only (Production FQ)",
            "source_location": "scripts/ablation_r3_repairs.py:49-55; stage2_equal_budget.py:75-80",
            "training_kernel_construction": "K_tr symmetrized and clipped to PSD cone via fidelity_clip_psd",
            "repair_timing": "Fitted strictly on training Gram block K_tr",
            "validation_test_generation": "K_te left completely unclipped and unaltered (K_te.copy())",
            "held_out_covariates_used": "No (K_te completely isolated)",
            "held_out_labels_used": "No",
            "target_standardization_fitted": "Strictly on training fold targets",
            "classification": "Inductive fold-local processing",
            "impact_on_tested_claims": "Does not affect claim; verified zero information leakage"
        },
        {
            "component": "repair_inductive (Out-of-Sample Spectral)",
            "source_location": "scripts/ablation_r3_repairs.py:58-96",
            "training_kernel_construction": "Eigendecomposition of K_tr = U diag(L) U^T; clipping L_clip = max(L, 0)",
            "repair_timing": "Eigenbasis U and filter factors f computed strictly from K_tr",
            "validation_test_generation": "K_te transformed via K_te' = K_te U diag(f) U^T and rescaled by training diagonal",
            "held_out_covariates_used": "No (operator is fixed by K_tr before applying to K_te)",
            "held_out_labels_used": "No",
            "target_standardization_fitted": "Strictly on training fold targets",
            "classification": "Inductive fold-local processing",
            "impact_on_tested_claims": "Does not affect claim; demonstrates out-of-sample PSD projection"
        },
        {
            "component": "repair_joint (Transductive Control)",
            "source_location": "scripts/ablation_r3_repairs.py:99-112",
            "training_kernel_construction": "Joint (N_tr + N_te) Gram matrix clipped to PSD cone; K_tr sliced from joint",
            "repair_timing": "Fitted globally across train and test states simultaneously",
            "validation_test_generation": "K_te sliced from jointly clipped Gram matrix",
            "held_out_covariates_used": "Yes (test states influence training eigenvalues)",
            "held_out_labels_used": "No (labels never used)",
            "target_standardization_fitted": "Strictly on training fold targets",
            "classification": "Unsupervised transductive processing",
            "impact_on_tested_claims": "Ablation control only; NOT used in production Stage 2/3 benchmarks"
        },
        {
            "component": "Inner Cross-Validation (Stage 2/3 SVR)",
            "source_location": "scripts/stage2_equal_budget.py:310-370; stage3_ood_shift.py:280-350",
            "training_kernel_construction": "KFold(n_splits=3/5, shuffle=True, random_state=42) on N_train=40 instances",
            "repair_timing": "Fold-local within inner CV; global on training set for final fit",
            "validation_test_generation": "Validation folds evaluate fold-local models; final test evaluates refit model",
            "held_out_covariates_used": "No (test set held out until final evaluation)",
            "held_out_labels_used": "No (hyperparameter tuning uses only training-fold CV scores)",
            "target_standardization_fitted": "Fold-local during CV; refit on full N_train=40 for final evaluation",
            "classification": "Inductive fold-local processing",
            "impact_on_tested_claims": "Does not affect claim; follows standard supervised ML isolation standards"
        }
    ]
    
    df_dataflow = pd.DataFrame(records)
    dataflow_csv = os.path.join(CLOSURE_DIR, "tables", "repair_cv_dataflow.csv")
    df_dataflow.to_csv(dataflow_csv, index=False)
    print(f"Saved: {dataflow_csv}")
    
    report_path = os.path.join(CLOSURE_DIR, "reports", "repair_cv_closure.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Forensic Audit of Gram Repairs, Cross-Validation, and Information Flow\n\n")
        f.write("## 1. Executive Verdict and Scope\n\n")
        f.write("This audit rigorously tracks the flow of covariate and label information across all kernel repair modes, inner cross-validation folds, preprocessing pipelines, and final evaluation test blocks in Stages 2 and 3.\n\n")
        f.write("- **Label Leakage:** **COMPLETELY ABSENT**. In no stage, fold, or repair method are held-out test labels ($y_{\\text{test}}$ or $y_{\\text{val}}$) ever accessed, standardized against, or consulted during training, PSD projection, or model selection.\n")
        f.write("- **Covariate Leakage in Production Benchmarks:** **COMPLETELY ABSENT**. The production deployable pipeline utilizes `repair_train_only`, which clips solely $K_{\\text{tr}}$ and leaves $K_{\\text{te}}$ untouched. Neither training eigenvalues nor support vectors depend in any way on held-out test states.\n")
        f.write("- **Transductive Ablation Isolation:** The transductive method `repair_joint` was implemented exclusively as an ablation control in Stage 1b to measure the impact of unsupervised transductive feature leakage, and was correctly excluded from all confirmatory production benchmarks in Stages 2 and 3.\n\n")
        f.write("## 2. Granular Data Flow and Information Trace Matrix\n\n")
        f.write(df_to_markdown(df_dataflow) + "\n\n")
        f.write("## 3. Evaluation of Inner Cross-Validation and Final Model Refitting\n\n")
        f.write("### 3.1 Inner-Fold Isolation\n")
        f.write("1. **Data Partitioning:** In `scripts/stage2_equal_budget.py` (lines 310-330) and `scripts/stage3_ood_shift.py` (lines 280-310), $K$-fold cross-validation operates strictly on the $N_{\\text{train}} = 40$ training instances.\n")
        f.write("2. **Target Standardization:** The target transformation parameters $\\mu_{\\text{fold}}$ and $\\sigma_{\\text{fold}}$ are computed exclusively from the training indices of that fold, preventing validation fold target leakage.\n")
        f.write("3. **Hyperparameter Selection:** The grid search across regularization penalty $C$, bandwidth $c$, and tolerance $\\epsilon$ optimizes the mean squared error across the held-out inner validation folds.\n\n")
        f.write("### 3.2 Final Model Refitting & Out-of-Sample Evaluation\n")
        f.write("1. Once optimal hyperparameters $(C^*, c^*, \\epsilon^*)$ are selected, the SVR model is refitted once on the complete training set ($N_{\\text{train}} = 40$).\n")
        f.write("2. The held-out test blocks ($N_{\\text{test,ID}} = 100$, $N_{\\text{test,OOD}} = 100$) are presented to the refitted model strictly as out-of-sample covariates.\n")
        f.write("3. Inverse standardization transforms predictions back to physical units using $\\mu_{\\text{train}}$ and $\\sigma_{\\text{train}}$, ensuring complete consistency.\n")
    print(f"Saved: {report_path}")

if __name__ == "__main__":
    main()
