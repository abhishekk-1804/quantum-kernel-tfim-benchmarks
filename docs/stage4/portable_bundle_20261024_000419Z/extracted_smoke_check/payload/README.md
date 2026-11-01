# Portable Saved-Artifact Verification Bundle

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
