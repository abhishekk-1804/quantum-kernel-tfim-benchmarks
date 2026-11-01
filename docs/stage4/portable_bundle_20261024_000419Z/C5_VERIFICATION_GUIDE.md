# C5 Verification Guide: Independent Contributor Verification

**Bundle Name:** `portable_verification_bundle.zip`  
**Bundle SHA-256:** `2e4e265be73be675cafe55545546886717ce61dca755d5d15428539598e37b95`  
**Bundle Size:** `2,893,362 bytes` (2.76 MB)  
**Creation Date:** 2026-10-24 00:08:49 UTC  

---

## 1. Overview and Scope

This guide enables an independent contributor to verify the numerical results, paired summaries, prediction arrays, and statistical tests of the TFIM quantum kernel study without requiring access to the original Windows environment or running simulation sweeps.

> [!NOTE]
> **Saved-Artifact Verification Only:** This verification evaluates the numerical fidelity, schema consistency, and mathematical reproducibility of the saved numerical arrays and CSV records. It does not reproduce model fitting, state generation, or quantum circuit execution from scratch.

---

## 2. Step-by-Step Verification Instructions

### Step 1: Obtain Archive and Expected SHA-256
Obtain `portable_verification_bundle.zip` and the accompanying `bundle_sha256.txt` through the project's authorized repository or transfer channel.

### Step 2: Verify ZIP Hash Before Extraction
Before unzipping, verify the cryptographic hash of the archive:

```bash
# On Linux / macOS:
sha256sum portable_verification_bundle.zip

# On Windows (PowerShell):
Get-FileHash -Algorithm SHA256 portable_verification_bundle.zip
```
Confirm the output matches exactly:
`2e4e265be73be675cafe55545546886717ce61dca755d5d15428539598e37b95`

### Step 3: Inspect Archive File List and Extract Safely
Inspect the archive contents to ensure paths are relative and clean:
```bash
unzip -l portable_verification_bundle.zip
unzip portable_verification_bundle.zip -d verification_bundle/
cd verification_bundle/payload
```

### Step 4: Verify Payload Hashes
Verify that every extracted payload file matches `manifest.csv`:
```bash
# Automated via the included runner (Check A), or manually:
python3 -c "
import csv, hashlib, os
with open('manifest.csv') as f:
    for r in csv.DictReader(f):
        h = hashlib.sha256(open(r['relative_path'], 'rb').read()).hexdigest()
        assert h == r['sha256'], f'Mismatch in ' + r['relative_path']
print('All payload files match manifest.csv!')
"
```

### Step 5: Inspect the Verification Runner
Inspect `scripts/verify_bundle.py`. It uses only standard library modules, NumPy, and SciPy. It contains zero network access, zero code generation, and zero file modification logic.

### Step 6: Prepare Python Environment
Create and activate an isolated Python environment (Python 3.8+):
```bash
python3 -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install numpy scipy
```

### Step 7: Run the Verification Suite
Execute the runner specifying an isolated output directory:
```bash
python scripts/verify_bundle.py --bundle-root . --output-dir ./my_verification_results
```

### Step 8: Inspect Verification Results
The runner will produce:
- `my_verification_results/VERIFICATION_REPORT.md`: Markdown summary of all 6 checks.
- `my_verification_results/verification_results.json`: Machine-readable results and discrepancy values.
- `my_verification_results/verification_results.csv`: Table of check statuses.
- `my_verification_results/execution_log.txt`: Complete execution trace.

### Step 9: Report Discrepancies
If any check produces a non-zero exit code or discrepancy exceeding declared tolerances (`atol=1e-7` for MAE, `atol=1e-6` for $R^2$), record the exact output, operating system, and package versions. Do not modify bundled inputs.

### Step 10: Sign Only Checks Actually Performed
Reviewers must sign only those checks they personally and independently verified.

---

## 3. Reference Values for Independent Checks

| Metric / Check | Primary Source | Expected Verified Value | Tolerance |
| :--- | :--- | :---: | :---: |
| **FQ vs PQK-2nn Paired Diff Mean** | `references/paired_mae_original.csv` | **-0.124849** | `1e-6` |
| **FQ vs PQK-2nn Paired Diff SE** | `references/paired_mae_original.csv` | **0.033425** | `1e-6` |
| **Wilcoxon Statistic $W$** | `references/test_configuration.json` | **21.0** | Exact |
| **Wilcoxon Raw $p$-value** | `references/test_configuration.json` | **8.5068e-4** | `1e-7` |
| **Stage 2 PQK-2nn ($B=10^6$) $R^2$ Mean** | `references/independent_stage2_cells.csv` | **0.9575** | `1e-4` |
| **Stage 2 FQ train_only ($B=10^6$) $R^2$ Mean** | `references/independent_stage2_cells.csv` | **0.8288** | `1e-4` |

---

## 4. Contributor Verification Sign-Off Block
*(To be completed by the independent reviewer)*

- **Reviewer Name / ID:** _________________________________________________________________
- **Reviewer Affiliation / Email:** _______________________________________________________
- **Operating System & Environment:** ____________________________________________________
- **Python / NumPy / SciPy Versions:** ____________________________________________________
- **Date of Independent Verification:** ___________________________________________________
- **Checks Personally Executed:** [ ] Check A  [ ] Check B  [ ] Check C  [ ] Check D  [ ] Check E  [ ] Check F
- **Discrepancies / Qualifications Noted:** _______________________________________________
- **Reviewer Signature:** ________________________________________________________________
