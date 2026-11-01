r"""
build_portable_bundle.py — Assemble and Verify Portable Saved-Artifact Verification Bundle
Workspace: D:\quantum-kernel-tfim-benchmarks
Interpreter: D:\qml_env\Scripts\python.exe
"""

import os
import sys
import csv
import json
import shutil
import zipfile
import hashlib
import subprocess
import time
import numpy as np
import scipy
from scipy import stats as sp_stats

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))

def compute_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def check_git_tracked(rel_path: str) -> bool:
    try:
        res = subprocess.run(["git", "ls-files", "--error-unmatch", rel_path],
                             cwd=REPO_ROOT, capture_output=True, text=True)
        return (res.returncode == 0)
    except Exception:
        return False

def main():
    print("======================================================================")
    print("BUILDING PORTABLE SAVED-ARTIFACT VERIFICATION BUNDLE")
    print(f"Bundle Directory: {SCRIPT_DIR}")
    print(f"Repo Root:       {REPO_ROOT}")
    print("======================================================================\n")

    # -------------------------------------------------------------------------
    # 1. INPUT DISCOVERY
    # -------------------------------------------------------------------------
    print("[Step 1] Discovering and inventorying inputs...")

    input_specs = [
        {
            "rel_path": "results/stage3/t6_ood_shift.csv",
            "role": "Primary Stage 3 experimental metrics (100 rows, 5 models x 20 seeds)",
            "nature": "Original primary benchmark output",
        },
        {
            "rel_path": "results/stage2/t1_equal_budget.csv",
            "role": "Primary Stage 2 experimental metrics (980 rows, 7 budgets x 7 models x 20 seeds)",
            "nature": "Original primary benchmark output",
        },
        {
            "rel_path": "docs/verification/paired_mae_check_20261023_171155Z/paired_mae_original.csv",
            "role": "Reconciled Stage 3 FQ vs PQK-2nn paired OOD MAE vector (20 seeds)",
            "nature": "Derived verification artifact",
        },
        {
            "rel_path": "docs/verification/paired_mae_check_20261023_171155Z/test_configuration.json",
            "role": "Exact historical Wilcoxon call specification and SciPy signature",
            "nature": "Derived verification artifact",
        },
        {
            "rel_path": "docs/verification/paired_mae_check_20261023_171155Z/input_mapping.json",
            "role": "Field and target array key mappings for Stage 3 transfer",
            "nature": "Derived verification artifact",
        },
        {
            "rel_path": "docs/stage5/stage2_sync_20261023_231851Z/independent_stage2_cells.csv",
            "role": "Independently aggregated Stage 2 cell reference table (49 cells)",
            "nature": "Derived verification artifact",
        },
        {
            "rel_path": "docs/verification/review_package_20261023_172944Z/tables/descriptive_statistics.csv",
            "role": "Full-precision descriptive statistics for Stage 3 MAE comparison vectors",
            "nature": "Derived verification artifact",
        },
        {
            "rel_path": "docs/verification/review_package_20261023_172944Z/tables/holm_verification.csv",
            "role": "Full-precision Holm-Bonferroni step-down multiplier and p-value reference",
            "nature": "Derived verification artifact",
        },
        {
            "rel_path": "docs/verification/closure_20261023_163403Z/tables/full_vs_intercept_per_seed.csv",
            "role": "Full FQ vs Intercept-only OOD MAE ablation per seed (20 seeds)",
            "nature": "Derived verification artifact",
        },
    ]

    # Add the 20 NPZ prediction files
    pred_dir = os.path.join(REPO_ROOT, "docs", "verification", "audit_20261023_155335Z", "predictions")
    for seed in range(20):
        npz_name = f"seed_{seed:02d}_arrays.npz"
        npz_rel = f"docs/verification/audit_20261023_155335Z/predictions/{npz_name}"
        input_specs.append({
            "rel_path": npz_rel,
            "role": f"Raw ground truth targets, predictions, and Gram matrices for Seed {seed:02d}",
            "nature": "Saved numerical prediction arrays",
        })

    inventory_rows = []
    pre_hashes = {}

    for spec in input_specs:
        rel = spec["rel_path"]
        abs_p = os.path.join(REPO_ROOT, rel)
        if not os.path.exists(abs_p):
            raise FileNotFoundError(f"Input file not found: {abs_p}")

        size = os.path.getsize(abs_p)
        sha = compute_sha256(abs_p)
        pre_hashes[rel] = sha
        tracked = check_git_tracked(rel)

        inventory_rows.append({
            "relative_path": rel,
            "size_bytes": size,
            "sha256": sha,
            "git_tracked": tracked,
            "evidence_role": spec["role"],
            "artifact_nature": spec["nature"],
        })

    inv_csv_path = os.path.join(SCRIPT_DIR, "input_inventory.csv")
    with open(inv_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["relative_path", "size_bytes", "sha256", "git_tracked", "evidence_role", "artifact_nature"])
        writer.writeheader()
        writer.writerows(inventory_rows)
    print(f"  Wrote input_inventory.csv ({len(inventory_rows)} records)")

    # -------------------------------------------------------------------------
    # 2. NPZ ARRAY SCHEMA INSPECTION (allow_pickle=False)
    # -------------------------------------------------------------------------
    print("\n[Step 2] Inspecting NPZ array schemas (allow_pickle=False)...")
    array_schema_info = {
        "inspection_protocol": "allow_pickle=False enforced on all numpy loads",
        "total_array_files": 20,
        "seed_range": [0, 19],
        "common_keys": [
            "e2_pred_id", "e2_pred_ood",
            "fq_K_id", "fq_K_ood", "fq_K_tr", "fq_dual_coef", "fq_intercept", "fq_pred_id", "fq_pred_ood", "fq_support",
            "pqk1_pred_id", "pqk1_pred_ood",
            "pqk2_K_id", "pqk2_K_ood", "pqk2_K_tr", "pqk2_dual_coef", "pqk2_intercept", "pqk2_pred_id", "pqk2_pred_ood", "pqk2_support",
            "ridge_pred_id", "ridge_pred_ood",
            "y_id", "y_ood", "y_train"
        ],
        "key_descriptions": {
            "y_train": {"shape": [40], "dtype": "float64", "description": "Training ground-state half-chain entanglement entropies S_{n/2}"},
            "y_id": {"shape": [100], "dtype": "float64", "description": "In-distribution test ground-state entanglement entropies (h in [0.8, 1.5])"},
            "y_ood": {"shape": [100], "dtype": "float64", "description": "Out-of-distribution test ground-state entanglement entropies (h in [0.2, 0.7])"},
            "fq_pred_id": {"shape": [100], "dtype": "float64", "description": "Full Quantum Fidelity Kernel SVR predictions on ID test set"},
            "fq_pred_ood": {"shape": [100], "dtype": "float64", "description": "Full Quantum Fidelity Kernel SVR predictions on OOD test set"},
            "pqk1_pred_id": {"shape": [100], "dtype": "float64", "description": "PQK-1 (RBF on <X_i>) SVR predictions on ID test set"},
            "pqk1_pred_ood": {"shape": [100], "dtype": "float64", "description": "PQK-1 (RBF on <X_i>) SVR predictions on OOD test set"},
            "pqk2_pred_id": {"shape": [100], "dtype": "float64", "description": "PQK-2nn (2-local Correlator) SVR predictions on ID test set"},
            "pqk2_pred_ood": {"shape": [100], "dtype": "float64", "description": "PQK-2nn (2-local Correlator) SVR predictions on OOD test set"},
            "e2_pred_id": {"shape": [100], "dtype": "float64", "description": "E2 (4n grid raw correlator) SVR predictions on ID test set"},
            "e2_pred_ood": {"shape": [100], "dtype": "float64", "description": "E2 (4n grid raw correlator) SVR predictions on OOD test set"},
            "ridge_pred_id": {"shape": [100], "dtype": "float64", "description": "Linear Ridge regression predictions on ID test set"},
            "ridge_pred_ood": {"shape": [100], "dtype": "float64", "description": "Linear Ridge regression predictions on OOD test set"},
            "fq_K_tr": {"shape": [40, 40], "dtype": "float64", "description": "FQ Training Gram matrix (Fidelity overlaps)"},
            "fq_K_id": {"shape": [100, 40], "dtype": "float64", "description": "FQ Test-ID to Train Kernel matrix"},
            "fq_K_ood": {"shape": [100, 40], "dtype": "float64", "description": "FQ Test-OOD to Train Kernel matrix"},
            "pqk2_K_tr": {"shape": [40, 40], "dtype": "float64", "description": "PQK-2nn Training Gram matrix"},
            "pqk2_K_id": {"shape": [100, 40], "dtype": "float64", "description": "PQK-2nn Test-ID to Train Kernel matrix"},
            "pqk2_K_ood": {"shape": [100, 40], "dtype": "float64", "description": "PQK-2nn Test-OOD to Train Kernel matrix"},
        },
        "per_seed_summary": []
    }

    for seed in range(20):
        npz_name = f"seed_{seed:02d}_arrays.npz"
        npz_p = os.path.join(pred_dir, npz_name)
        data = np.load(npz_p, allow_pickle=False)
        array_schema_info["per_seed_summary"].append({
            "seed": seed,
            "filename": npz_name,
            "keys_count": len(data.files),
            "fq_support_vectors_count": int(len(data["fq_support"])),
            "pqk2_support_vectors_count": int(len(data["pqk2_support"])),
            "all_finite": bool(np.all(np.isfinite(data["y_ood"])) and np.all(np.isfinite(data["fq_pred_ood"]))),
        })

    arr_schema_path = os.path.join(SCRIPT_DIR, "array_schema.json")
    with open(arr_schema_path, "w", encoding="utf-8") as f:
        json.dump(array_schema_info, f, indent=2)
    print(f"  Wrote array_schema.json ({len(array_schema_info['per_seed_summary'])} seeds verified)")

    # Write input_mapping.json in bundle dir
    input_mapping_data = {
        "seed_mapping_rule": "seed_XX_arrays.npz corresponds to CSV row where seed == int(XX)",
        "ood_target_key": "y_ood",
        "id_target_key": "y_id",
        "model_key_mapping": {
            "FQ": {"pred_id": "fq_pred_id", "pred_ood": "fq_pred_ood", "variant": "none"},
            "PQK-1": {"pred_id": "pqk1_pred_id", "pred_ood": "pqk1_pred_ood", "variant": "none"},
            "PQK-2nn": {"pred_id": "pqk2_pred_id", "pred_ood": "pqk2_pred_ood", "variant": "none"},
            "E2 (4n)": {"pred_id": "e2_pred_id", "pred_ood": "e2_pred_ood", "variant": "raw_4n_grid"},
            "Linear_Ridge": {"pred_id": "ridge_pred_id", "pred_ood": "ridge_pred_ood", "variant": "none"},
        },
        "tolerances": {
            "mae_atol": 1e-7,
            "mae_rtol": 0.0,
            "r2_atol": 1e-6,
            "r2_rtol": 0.0,
        },
        "statistical_protocol": {
            "paired_difference": "diff = FQ_mae - PQK2_mae",
            "wilcoxon_test": "scipy.stats.wilcoxon(diff, alternative='two-sided')",
            "historical_W": 21.0,
            "historical_p": 0.000850677490234375,
        }
    }
    inp_map_path = os.path.join(SCRIPT_DIR, "input_mapping.json")
    with open(inp_map_path, "w", encoding="utf-8") as f:
        json.dump(input_mapping_data, f, indent=2)
    print("  Wrote input_mapping.json")

    # -------------------------------------------------------------------------
    # 3. CONSTRUCT PAYLOAD
    # -------------------------------------------------------------------------
    print("\n[Step 3] Constructing payload directory structure...")
    payload_dir = os.path.join(SCRIPT_DIR, "payload")
    if os.path.exists(payload_dir):
        shutil.rmtree(payload_dir)

    os.makedirs(os.path.join(payload_dir, "data", "results", "stage3"), exist_ok=True)
    os.makedirs(os.path.join(payload_dir, "data", "results", "stage2"), exist_ok=True)
    os.makedirs(os.path.join(payload_dir, "arrays"), exist_ok=True)
    os.makedirs(os.path.join(payload_dir, "references"), exist_ok=True)
    os.makedirs(os.path.join(payload_dir, "scripts"), exist_ok=True)

    # Copy files into payload
    copy_manifest = [
        # Data
        (os.path.join(REPO_ROOT, "results", "stage3", "t6_ood_shift.csv"),
         os.path.join(payload_dir, "data", "results", "stage3", "t6_ood_shift.csv"),
         "Primary Stage 3 experimental metrics"),
        (os.path.join(REPO_ROOT, "results", "stage2", "t1_equal_budget.csv"),
         os.path.join(payload_dir, "data", "results", "stage2", "t1_equal_budget.csv"),
         "Primary Stage 2 experimental metrics"),
        # References
        (os.path.join(REPO_ROOT, "docs", "verification", "paired_mae_check_20261023_171155Z", "paired_mae_original.csv"),
         os.path.join(payload_dir, "references", "paired_mae_original.csv"),
         "Reconciled Stage 3 paired MAE reference vector"),
        (os.path.join(REPO_ROOT, "docs", "verification", "paired_mae_check_20261023_171155Z", "test_configuration.json"),
         os.path.join(payload_dir, "references", "test_configuration.json"),
         "Exact Wilcoxon test configuration and signature"),
        (os.path.join(SCRIPT_DIR, "input_mapping.json"),
         os.path.join(payload_dir, "references", "input_mapping.json"),
         "Target and prediction key mapping rules"),
        (os.path.join(REPO_ROOT, "docs", "stage5", "stage2_sync_20261023_231851Z", "independent_stage2_cells.csv"),
         os.path.join(payload_dir, "references", "independent_stage2_cells.csv"),
         "Independently aggregated Stage 2 cell reference table"),
        (os.path.join(REPO_ROOT, "docs", "verification", "review_package_20261023_172944Z", "tables", "descriptive_statistics.csv"),
         os.path.join(payload_dir, "references", "descriptive_statistics.csv"),
         "Full-precision descriptive statistics for Stage 3 vectors"),
        (os.path.join(REPO_ROOT, "docs", "verification", "review_package_20261023_172944Z", "tables", "holm_verification.csv"),
         os.path.join(payload_dir, "references", "holm_verification.csv"),
         "Full-precision Holm-Bonferroni verification table"),
        (os.path.join(REPO_ROOT, "docs", "verification", "closure_20261023_163403Z", "tables", "full_vs_intercept_per_seed.csv"),
         os.path.join(payload_dir, "references", "full_vs_intercept_per_seed.csv"),
         "Full FQ vs Intercept-only OOD MAE per seed table"),
        # Script
        (os.path.join(SCRIPT_DIR, "verify_bundle_template.py"),
         os.path.join(payload_dir, "scripts", "verify_bundle.py"),
         "Standalone bundle verification runner"),
    ]

    # Add 20 NPZ files to copy
    for seed in range(20):
        npz_name = f"seed_{seed:02d}_arrays.npz"
        src_p = os.path.join(pred_dir, npz_name)
        dst_p = os.path.join(payload_dir, "arrays", npz_name)
        copy_manifest.append((src_p, dst_p, f"Raw ground truth and predictions array for Seed {seed:02d}"))

    # Copy and verify hashes
    print(f"  Copying {len(copy_manifest)} files to payload...")
    for src, dst, desc in copy_manifest:
        shutil.copy2(src, dst)
        src_h = compute_sha256(src)
        dst_h = compute_sha256(dst)
        assert src_h == dst_h, f"Hash mismatch during copy: {src} -> {dst}"

    # Write environment_reference.txt
    env_ref_path = os.path.join(payload_dir, "environment_reference.txt")
    env_txt = f"""# Environment Reference for Portable Saved-Artifact Verification Bundle
# Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}

OS: Windows (Platform-portable Python runner; compatible with Linux/macOS)
Python Version: {sys.version}
NumPy Version: {np.__version__}
SciPy Version: {sp_stats.__name__} (scipy {getattr(sp_stats, '__version__', 'unknown')})

Minimum Requirements:
- Python 3.8+
- NumPy >= 1.20
- SciPy >= 1.7.0

No other packages are required (standard library used for CSV, JSON, hashing, and argument parsing).
"""
    with open(env_ref_path, "w", encoding="utf-8") as f:
        f.write(env_txt)

    # Write README.md in payload
    readme_path = os.path.join(payload_dir, "README.md")
    readme_txt = """# Portable Saved-Artifact Verification Bundle

This bundle contains saved numerical arrays, primary result CSVs, reference summaries, and a standalone runner for verifying the empirical results of the TFIM quantum kernel benchmark study.

## Quick Start

```bash
# 1. Inspect contents and run verification
python scripts/verify_bundle.py --bundle-root . --output-dir ./verification_output
```

The runner performs:
- **CHECK_A**: Payload manifest integrity (verifies all files against manifest.csv using SHA-256)
- **CHECK_B**: CSV key integrity (asserts exactly 20 seeds per cell; no duplicates)
- **CHECK_C**: Array metrics reproduction (recomputes MAE and R² from raw NPZ prediction arrays)
- **CHECK_D**: Paired summary reproduction (verifies paired difference mean, SE, and seed sign distribution)
- **CHECK_E**: Wilcoxon signed-rank test (recomputes exact test statistic W=21.0 and p=8.5068e-4)
- **CHECK_F**: Stage 2 independent aggregation (aggregates all 49 equal-budget cells)

Results will be written to `verification_output/`:
- `verification_results.json`
- `verification_results.csv`
- `VERIFICATION_REPORT.md`
- `execution_log.txt`
"""
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_txt)

    # -------------------------------------------------------------------------
    # 4. GENERATE MANIFEST.CSV
    # -------------------------------------------------------------------------
    print("\n[Step 4] Generating manifest.csv for payload...")
    manifest_rows = []
    
    for root, dirs, files in os.walk(payload_dir):
        for f in files:
            if f == "manifest.csv":
                continue  # manifest.csv is explicitly excluded from self-hashing
            abs_f = os.path.join(root, f)
            rel_f = os.path.relpath(abs_f, payload_dir).replace("\\", "/")
            size_b = os.path.getsize(abs_f)
            sha = compute_sha256(abs_f)
            
            # Determine role
            if rel_f.startswith("data/"):
                role = "Primary experimental metric CSV"
            elif rel_f.startswith("arrays/"):
                role = "Ground truth targets, predictions, and Gram matrix NPZ"
            elif rel_f.startswith("references/"):
                role = "Full-precision reference table or test configuration"
            elif rel_f.startswith("scripts/"):
                role = "Standalone verification script"
            else:
                role = "Documentation or environment reference"

            manifest_rows.append({
                "relative_path": rel_f,
                "size_bytes": size_b,
                "sha256": sha,
                "role": role,
            })

    # Sort manifest for deterministic output
    manifest_rows.sort(key=lambda x: x["relative_path"])

    manifest_csv_path = os.path.join(payload_dir, "manifest.csv")
    with open(manifest_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["relative_path", "size_bytes", "sha256", "role"])
        writer.writeheader()
        writer.writerows(manifest_rows)
    print(f"  Wrote manifest.csv ({len(manifest_rows)} files hashed, manifest.csv itself excluded)")

    # -------------------------------------------------------------------------
    # 5. CREATE ZIP ARCHIVE
    # -------------------------------------------------------------------------
    print("\n[Step 5] Packaging payload into portable_verification_bundle.zip...")
    zip_path = os.path.join(SCRIPT_DIR, "portable_verification_bundle.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(payload_dir):
            for f in files:
                abs_f = os.path.join(root, f)
                rel_f = os.path.relpath(abs_f, payload_dir).replace("\\", "/")
                # Store in zip under payload/<rel_f>
                arc_name = f"payload/{rel_f}"
                zf.write(abs_f, arcname=arc_name)

    zip_size = os.path.getsize(zip_path)
    zip_sha = compute_sha256(zip_path)

    sha_file_path = os.path.join(SCRIPT_DIR, "bundle_sha256.txt")
    with open(sha_file_path, "w", encoding="utf-8") as f:
        f.write(f"{zip_sha}  portable_verification_bundle.zip\n")

    print(f"  Created portable_verification_bundle.zip:")
    print(f"    Size: {zip_size:,} bytes ({zip_size / 1024 / 1024:.2f} MB)")
    print(f"    Files: {len(manifest_rows) + 1} (including manifest.csv)")
    print(f"    SHA-256: {zip_sha}")

    # -------------------------------------------------------------------------
    # 6. LOCAL EXTRACTION SMOKE CHECK
    # -------------------------------------------------------------------------
    print("\n[Step 6] Running local extraction smoke check...")
    smoke_extract_dir = os.path.join(SCRIPT_DIR, "extracted_smoke_check")
    if os.path.exists(smoke_extract_dir):
        shutil.rmtree(smoke_extract_dir)
    os.makedirs(smoke_extract_dir, exist_ok=True)

    # Extract zip
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(smoke_extract_dir)

    smoke_payload = os.path.join(smoke_extract_dir, "payload")
    smoke_script = os.path.join(smoke_payload, "scripts", "verify_bundle.py")
    smoke_output_dir = os.path.join(smoke_extract_dir, "results")

    smoke_cmd = [
        sys.executable,
        smoke_script,
        "--bundle-root", smoke_payload,
        "--output-dir", smoke_output_dir,
    ]

    t0 = time.time()
    smoke_res = subprocess.run(smoke_cmd, capture_output=True, text=True)
    smoke_elapsed = time.time() - t0

    print(f"  Command: {' '.join(smoke_cmd)}")
    print(f"  Exit Code: {smoke_res.returncode}")
    print(f"  Runtime:   {smoke_elapsed:.3f}s")
    if smoke_res.returncode == 0:
        print("  SMOKE CHECK STATUS: PASSED (All 6 checks verified)")
    else:
        print("  SMOKE CHECK STATUS: FAILED")
        print("  STDERR:\n", smoke_res.stderr)
        print("  STDOUT:\n", smoke_res.stdout)

    assert smoke_res.returncode == 0, "Smoke check failed!"

    # -------------------------------------------------------------------------
    # 7. WRITE C5_VERIFICATION_GUIDE.MD
    # -------------------------------------------------------------------------
    print("\n[Step 7] Writing C5_VERIFICATION_GUIDE.md...")
    guide_md = f"""# C5 Verification Guide: Independent Contributor Verification

**Bundle Name:** `portable_verification_bundle.zip`  
**Bundle SHA-256:** `{zip_sha}`  
**Bundle Size:** `{zip_size:,} bytes` ({zip_size / 1024 / 1024:.2f} MB)  
**Creation Date:** {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}  

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
`{zip_sha}`

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
source venv/bin/activate  # Or venv\\Scripts\\activate on Windows
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
"""
    guide_path = os.path.join(SCRIPT_DIR, "C5_VERIFICATION_GUIDE.md")
    with open(guide_path, "w", encoding="utf-8") as f:
        f.write(guide_md)
    print("  Wrote C5_VERIFICATION_GUIDE.md")

    # -------------------------------------------------------------------------
    # 8. POST-EXECUTION HASH VERIFICATION
    # -------------------------------------------------------------------------
    print("\n[Step 8] Re-verifying SHA-256 hashes of all pre-existing original inputs...")
    for rel, pre_h in pre_hashes.items():
        abs_p = os.path.join(REPO_ROOT, rel)
        post_h = compute_sha256(abs_p)
        assert post_h == pre_h, f"CRITICAL: Original file was modified: {rel}"
        print(f"  [VERIFIED UNCHANGED] {rel}")

    print("\n======================================================================")
    print("PORTABLE VERIFICATION BUNDLE COMPLETED SUCCESSFULLY.")
    print("======================================================================")

if __name__ == "__main__":
    main()
