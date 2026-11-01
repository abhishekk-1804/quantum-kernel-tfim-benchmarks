# Closure Input Inventory and Baseline Discovery

- **Execution Timestamp (UTC):** 2026-10-23T16:39:03.026760+00:00
- **Python:** `D:\qml_env\Scripts\python.exe` (`3.12.10`)
- **Repository Root:** `D:\quantum-kernel-tfim-benchmarks`
- **Git HEAD:** `292d689dd845f6228fae6265cffe83b81d5f0f66`
- **Total Input Files Tracked:** 48

## 1. Inventory Summary

All inputs originate from verified read-only audit directories and frozen benchmark results.
No existing files were modified or deleted.

### Tracked Input Categories
1. **Audit 20261023_155335Z Core Artifacts:** 22 files (tables, reports, manifests, arrays)
2. **Audit 20261023_155335Z Prediction Archives:** 20 files (`seed_00_arrays.npz` to `seed_19_arrays.npz`)
3. **Candidate Production Benchmarks & Scripts:** 8 files (Stage 2/3 CSVs, experiment scripts, audit scripts, snapshot manifest)

## 2. CSV Schemas and Record Counts

### `docs/provenance/snapshot_20261023_155335Z_candidate_v1/manifest_sha256.csv`
- **Row count:** 18
- **Columns (7):** `source_path, snapshot_relative_path, file_size_bytes, sha256_before, sha256_snapshot, sha256_after, match_status`

### `docs/verification/audit_20261023_155335Z/covariance_diagnostic.csv`
- **Row count:** 1
- **Columns (14):** `trials_K, shots_S, rng_seed, eigenpair_residual, exact_exp_X0, exact_exp_X1, exact_exp_X0X1, theoretical_covariance, production_empirical_cov, production_cov_se, production_z_score, independent_empirical_cov, independent_cov_se, classification`

### `docs/verification/audit_20261023_155335Z/input_integrity.csv`
- **Row count:** 2
- **Columns (12):** `dataset, csv_path, row_count, expected_row_count, composite_key, duplicate_keys, seeds_count, seeds_range, budgets_count, structural_nans, unexpected_nans, status`

### `docs/verification/audit_20261023_155335Z/kernel_summary.csv`
- **Row count:** 20
- **Columns (9):** `seed, model, K_id_mean, K_id_median, K_id_max, K_ood_mean, K_ood_median, K_ood_max, K_attenuation_ratio`

### `docs/verification/audit_20261023_155335Z/measurement_manifest.csv`
- **Row count:** 46
- **Columns (8):** `model_arm, observable_symbol, observable_type, pauli_basis, measurement_setting, shared_source, exact_symmetry_assumption, shots_charged_per_state`

### `docs/verification/audit_20261023_155335Z/replay_metric_comparison.csv`
- **Row count:** 500
- **Columns (8):** `seed, model, metric, original_value, recomputed_value, abs_diff, tolerance, status`

### `docs/verification/audit_20261023_155335Z/representation_distance_checks.csv`
- **Row count:** 4
- **Columns (6):** `comparison, max_abs_error, max_rel_error, target_tolerance, status, interpretation`

### `docs/verification/audit_20261023_155335Z/resource_accounting.csv`
- **Row count:** 21
- **Columns (9):** `B_tot, architecture, settings, allocated_shots_per_setting, circuit_repetitions_consumed, input_state_copies_consumed, unused_budget_shots, efficiency_percent, feasibility_status`

### `docs/verification/audit_20261023_155335Z/stage3_baselines.csv`
- **Row count:** 20
- **Columns (9):** `seed, c_train_mean, c_train_median, mae_train_mean_baseline, mae_train_median_baseline, r2_train_mean_baseline, r2_train_median_baseline, mae_fq, mae_pqk2`

### `docs/verification/audit_20261023_155335Z/stage3_mae_comparisons.csv`
- **Row count:** 3
- **Columns (10):** `comparison, n_pairs, mean_paired_diff, median_paired_diff, se_diff, ci_95_low, ci_95_high, wilcoxon_stat, raw_pval, holm_pval`

### `docs/verification/audit_20261023_155335Z/stage3_svr_decomposition.csv`
- **Row count:** 20
- **Columns (17):** `seed, model, support_vectors_count, support_fraction, dual_coef_l1_norm, intercept_model_z, intercept_physical, mae_full_model, mae_intercept_only, mae_diff_full_minus_intercept, mean_g_ood, median_abs_g_ood, q90_abs_g_ood, rms_g_ood, pred_min_ood, pred_max_ood, reconstruction_error`

### `docs/verification/audit_20261023_155335Z/stage3_target_diagnostics.csv`
- **Row count:** 20
- **Columns (12):** `seed, y_train_mean, y_train_std, y_train_min, y_train_max, y_id_mean, y_id_std, sst_id, y_ood_mean, y_ood_std, sst_ood, variance_ratio_ood_to_train`

### `results/stage2/t1_equal_budget.csv`
- **Row count:** 980
- **Columns (10):** `seed, B_tot, model, variant, S_per_setting, test_r2, test_mae, best_params, inner_cv_score, is_feasible`

### `results/stage3/t6_ood_shift.csv`
- **Row count:** 100
- **Columns (10):** `seed, model, variant, id_r2, id_mae, ood_r2, ood_mae, delta_r2, best_params, inner_cv_score`

## 3. Snapshot Integrity Verification

The candidate snapshot manifest at `docs/provenance/snapshot_20261023_155335Z_candidate_v1/manifest_sha256.csv` was previously verified to have 100% byte-for-byte SHA256 integrity.
All 18 candidate files remain unperturbed in the workspace.
