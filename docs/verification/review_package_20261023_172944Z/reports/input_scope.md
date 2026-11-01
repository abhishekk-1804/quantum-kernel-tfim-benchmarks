# Discovery and Input Scope Report

- **Execution Timestamp (UTC):** `2026-10-23T17:39:27.232228+00:00`
- **Package Directory:** `docs/verification/review_package_20261023_172944Z`
- **Total Input Artifacts Mapped:** 38

## 1. Categorical Distribution of Inspected Evidence

- **saved replay output:** 20 files
- **derived audit output:** 12 files
- **historical narrative:** 2 files
- **audit report:** 1 files
- **original results:** 1 files
- **audit script:** 1 files
- **historical script:** 1 files

## 2. Input Integrity and Ambiguity Resolution

- **Primary Result CSV:** `results/stage3/t6_ood_shift.csv` is the immutable primary record containing all 100 benchmark rows across 5 models and 20 seeds.
- **Model Selection Predicates:** Unambiguously identified as `model in ['FQ', 'PQK-2nn']` and `variant == 'none'`. There are no competing or ambiguous variant assignments for these models in Stage 3.
- **Target & Prediction Mapping:** `y_ood` in `seed_XX_arrays.npz` represents the 100 test states in the deep ferromagnetic regime ($h_i \in [0.2, 0.7]$). Predictions `fq_pred_ood` and `pqk2_pred_ood` have identical shape `(100,)` float64 and evaluate the exact same test instances in identical order.
- **Safety Verification:** All NPZ loading is performed strictly with `allow_pickle=False` as a context manager. No untrusted objects or unverified code was imported.
