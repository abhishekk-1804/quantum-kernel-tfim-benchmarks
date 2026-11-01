# Forensic Audit Code Development and Debugging History

## 1. Scope and Evidentiary Sources

In accordance with Section 8 of the closure mandate, this document records all known audit-code corrections, debugging steps, and operational changes that occurred during the execution of the forensic audit suite.
All entries are grounded directly in recorded transcript logs (`transcript.jsonl` and `transcript_full.jsonl`) and script diffs. No deleted code or historical timestamps are fabricated.

## 2. Reconstructed Incident Ledger

### Incident 1: Loop Variable Definition in Representation Identity Audit
- **Audit Script Affected:** `scripts/audit_representation_identity.py` (lines 85-115)
- **Observed Failure:** Execution failed with `NameError: name 's_idx' is not defined` during feature extraction.
- **Root Cause:** In the initial version written in Step 5616, the loop was written as `for psi in psis:`, but the dictionary of reduced density matrices was indexed by state index: `rdms_by_state[s_idx][(i, i + 1)]`.
- **Correction Applied (Step 5636):** Modified the loop header to `for s_idx, psi in enumerate(psis):` in both the reference deduplicated feature loop and the negative control loop.
- **Impact on Experimental Logic:** Zero. The fix was confined entirely to the audit verification diagnostic. Original production scripts (`src/kernels.py`, `scripts/stage3_ood_shift.py`) were not touched.
- **Post-Correction Validation:** Re-execution in Step 5638 passed in 3.12 seconds, producing `representation_distance_checks.csv` and validating that the maximum discrepancy between 2-RDM distance and classical 2-point correlators is identically $0.00e+00$ across all 10 diagnostic ground states.
- **Remaining Uncertainty:** None.

### Incident 2: Scipy Module Version Attribute in Metrics Audit
- **Audit Script Affected:** `scripts/audit_stage3_metrics.py` (lines 28, 335)
- **Observed Failure:** `AttributeError: module 'scipy.stats' has no attribute '__version__'`.
- **Root Cause:** The script imported `from scipy import stats` and attempted to log `stats.__version__`.
- **Correction Applied (Steps 5818, 5820):** Added top-level `import scipy` and updated the log string to `scipy.__version__`.
- **Impact on Experimental Logic:** Zero. Affected only log metadata formatting.
- **Post-Correction Validation:** Resolved attribute error cleanly.
- **Remaining Uncertainty:** None.

### Incident 3: Replay Cache Optimization and Prediction Loader
- **Audit Script Affected:** `scripts/audit_stage3_metrics.py` (lines 450-510)
- **Observed Behavior:** Replaying the entire Stage 3 benchmark from scratch across all 20 seeds took several minutes on every diagnostic invocation.
- **Root Cause:** SVR fitting with 5-fold cross-validation across 20 seeds requires solving quadratic programs repeatedly.
- **Correction Applied (Step 5828):** Implemented `load_or_run_stage3_replay()`. The function checks if all 20 seed prediction files (`docs/verification/audit_20261023_155335Z/predictions/seed_00_arrays.npz` through `seed_19_arrays.npz`) exist on disk. If verified, it loads the saved arrays directly into memory in 1.4 seconds rather than re-executing.
- **Impact on Experimental Logic:** Zero. The arrays loaded from disk are the identical, uncompressed numpy predictions and Gram matrices produced by the first verified replay.
- **Post-Correction Validation:** Output comparison confirmed identical metrics to machine precision ($0.00e+00$).
- **Remaining Uncertainty:** None.

### Incident 4: Markdown Formatting & Latex Delimiter Fixes
- **Audit Script Affected:** `scripts/audit_stage3_metrics.py` (line 425)
- **Observed Failure:** Markdown parsers encountered double-backslash escaping anomalies when rendering LaTeX norm symbols (`$\|g(x)\|_2$`).
- **Correction Applied (Step 5822):** Simplified formatting to `||g(x)||_2`.
- **Impact on Experimental Logic:** Zero.

## 3. Summary Assessment

All audit development debugging was strictly operational (correcting indexing variables, handling optional library attributes, adding caching loaders, and fixing markdown escapes). At no point was any underlying benchmark result modified, tuned, or regenerated to force a desired outcome.
