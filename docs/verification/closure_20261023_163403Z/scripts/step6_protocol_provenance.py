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
    print("Executing Step 6: Protocol Provenance Ledger...")
    
    records = [
        {
            "stage_id": "Stage 2: Equal-Total-Budget Benchmark",
            "git_commit_sha": "dff0171183c99c43f9555964ba0a88731ddc98cf",
            "git_commit_timestamp_utc": "2026-10-23T15:02:50Z",
            "protocol_document": "docs/stage2/equal_budget_summary.md (in-repo)",
            "classification": "Documented protocol; timing not established",
            "experiment_definition": "Fixed budget B_tot = M * S trade-off at B_tot in {1e3..1e6} on T1 disordered TFIM ground state energy",
            "primary_outcome": "R^2 metric vs total budget B_tot and shot count S",
            "comparisons": "PQK-1 vs PQK-2nn vs FQ across measurement budgets",
            "thresholds_cutoffs": "Crossover point where shot noise dominates representation capacity",
            "subsequent_additions": "Retrospective covariance diagnostic (K=5000) and resource accounting audit",
            "provenance_assessment": "The protocol was specified in user prompt directives and documented in equal_budget_summary.md, but committed atomically with results in git commit dff0171. Pre-execution git commit absent."
        },
        {
            "stage_id": "Stage 3: Controlled OOD Phase-Shift Generalization",
            "git_commit_sha": "292d689dd845f6228fae6265cffe83b81d5f0f66",
            "git_commit_timestamp_utc": "2026-10-23T15:41:11Z",
            "protocol_document": "docs/stage3/ood_protocol.md",
            "classification": "Documented protocol; timing not established",
            "experiment_definition": "Controlled OOD phase shift from paramagnetic (h in [0.8, 1.5]) to ferromagnetic (h in [0.2, 0.7]) predicting entanglement entropy",
            "primary_outcome": "In-distribution and out-of-distribution R^2 and MAE across 20 random seeds",
            "comparisons": "FQ vs PQK-2nn vs Classical Ridge on 2-point correlators",
            "thresholds_cutoffs": "R^2 sign (positive vs negative) and paired MAE difference",
            "subsequent_additions": "Addition of Train-Mean/Train-Median constant baselines, Holm adjustment across expanded family, and SVR intercept/kernel decompositions (Audit 20261023_155335Z)",
            "provenance_assessment": "The formal protocol was written in ood_protocol.md labeled 'CONFIRMATORY', but committed atomically with benchmark results in git commit 292d689. Pre-execution git commit absent."
        },
        {
            "stage_id": "Audit & Evidence Reconciliation (Audit 20261023_155335Z & Closure)",
            "git_commit_sha": "Uncommitted working tree additions",
            "git_commit_timestamp_utc": "N/A (working tree)",
            "protocol_document": "docs/verification/closure_20261023_163403Z/task_specification.txt",
            "classification": "Explicitly retrospective / post-hoc audit",
            "experiment_definition": "Forensic audit of sampling covariance, RDM representations, metrics, constant baselines, SVR decompositions, and protocol provenance",
            "primary_outcome": "Identification of supported vs qualified claims, correction of narrative reporting errors, and reconciliation of mathematical quantities",
            "comparisons": "Authoritative CSV values vs narrative reports; full models vs intercept-only predictors; full 3-comparison family",
            "thresholds_cutoffs": "z < 3.0 for sampling covariance, p_holm < 0.05 for pairwise differences",
            "subsequent_additions": "Closure package (closure_20261023_163403Z)",
            "provenance_assessment": "Fully post-hoc forensic audit executed after benchmark completion to establish rigor and boundaries."
        }
    ]
    
    df_ledger = pd.DataFrame(records)
    ledger_csv = os.path.join(CLOSURE_DIR, "tables", "protocol_provenance_ledger.csv")
    df_ledger.to_csv(ledger_csv, index=False)
    print(f"Saved: {ledger_csv}")
    
    report_path = os.path.join(CLOSURE_DIR, "reports", "protocol_provenance.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Protocol Provenance and Preregistration Analysis Report\n\n")
        f.write("## 1. Methodological Principles of Provenance Evaluation\n\n")
        f.write("To adhere to the highest scientific standards of reproducibility and evidentiary rigor, we evaluate the prospective vs retrospective status of all benchmark stages using strict evidentiary criteria:\n")
        f.write("1. **Weak Evidence:** Local file timestamps (`mtime`) and post-run snapshot directories do NOT establish prospective protocol freezing.\n")
        f.write("2. **Git Commit Timing:** A Git commit created *after* experimental execution does NOT prove that the protocol was pre-registered prior to data collection.\n")
        f.write("3. **Epistemic Classification Standard:** In the absence of an independent, cryptographically timestamped pre-commitment (e.g. OSF, public pre-run commit SHA, or external registry), a documented protocol must be classified as **`Documented protocol; timing not established`**, rather than falsely claiming external pre-registration or dismissively labeling it purely ad-hoc.\n\n")
        f.write("## 2. Protocol Provenance Ledger\n\n")
        f.write(df_to_markdown(df_ledger) + "\n\n")
        f.write("## 3. Detailed Stage-by-Stage Provenance Assessment\n\n")
        f.write("### 3.1 Stage 2: Equal-Total-Budget Benchmark\n")
        f.write("- **Git Provenance:** All Stage 2 files (`docs/stage2/equal_budget_summary.md`, `results/stage2/t1_equal_budget.csv`, `scripts/stage2_equal_budget.py`) were committed atomically in commit `dff0171` (2026-10-23 20:32:50 +0530 / 15:02:50Z).\n")
        f.write("- **Protocol Status:** The experimental parameters ($B_{\\text{tot}} = M \\cdot S$, shot grids, observable cliques) were defined in user prompt specifications prior to execution, and the summary document states frozen rules. However, because no pre-execution Git tag or commit exists in the repo history, its provenance is formally classified as **Documented protocol; timing not established**.\n\n")
        f.write("### 3.2 Stage 3: Controlled OOD Phase-Shift Generalization\n")
        f.write("- **Git Provenance:** All Stage 3 files (`docs/stage3/ood_protocol.md`, `results/stage3/t6_ood_shift.csv`, `scripts/stage3_ood_shift.py`, `tests/test_stage3_ood.py`) were committed atomically in commit `292d689` (2026-10-23 21:11:11 +0530 / 15:41:11Z).\n")
        f.write("- **Protocol Status:** The file `docs/stage3/ood_protocol.md` contains an extensive, mathematically rigorous protocol header declaring `CONFIRMATORY (Stage 3 Frozen Protocol)`. The core hypotheses (FQ vs PQK-2nn, domain partitions $h \\in [0.8, 1.5]$ vs $[0.2, 0.7]$) were followed as written. However, because it was committed simultaneously with the results, the timing cannot be externally proven from git history alone. It is classified as **Documented protocol; timing not established**.\n")
        f.write("- **Retrospective Additions:** The inclusion of training-set constant baselines (`Train-Mean` and `Train-Median`), Holm family expansion, and SVR intercept/kernel decompositions performed during the audit are explicitly retrospective additions.\n")
    print(f"Saved: {report_path}")

if __name__ == "__main__":
    main()
