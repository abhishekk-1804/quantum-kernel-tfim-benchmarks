# Gate-0 Reproduction Card: Contributor C3 (Statistics & Baselines)

## 1. Specifications
- **Baseline Commit:** `739a724919f52164193a200b6e07d827fe273c62`
- **Environment Spec:** Python 3.12.10, NumPy 2.5.4, SciPy 1.18.1, scikit-learn 1.9.1 in active virtual environment `D:\qml_env`
- **Config File:** `scripts/common.py` and `scripts/stats.py`
- **Arm:** Statistical Testing Engine, RNG Streams, & Classical Regressor Baselines
- **Seeds:** Seed 3 RNG stream audit; full benchmark across seeds 0–19

---

## 2. Verification Commands
Execute the following verification commands:
```powershell
# 1. Seed 3 RNG Stream Audit (Task T2b sequential re-evaluation)
D:\qml_env\Scripts\python.exe scripts/verify_seed3_rng.py

# 2. Statistical unit test suite
D:\qml_env\Scripts\python.exe -m pytest tests/test_stats.py -v
```

---

## 3. Expected Artifacts and Metrics
- **Expected Output Artifact:**
  - `verify_seed3_rng.py` console output reporting `SUCCESS: max |diff| < 1e-10`.
  - Passing pytest suite covering Holm step-down correction, rank-biserial effect sizes, and bootstrap CI reproducibility.
- **Expected Benchmark Metrics:**
  - **Source File 1:** `results/t2_correlators_gridv3.csv`
    - **Filter:** `task == "T2b"`, `seed == 3`, `N_train == 40`, `metric == "r2"`
    - **Row 2121 (PQK-2nn):** `0.9511316620674743`
    - **Row 2117 (FQ):** `0.9853037854710071`
  - **Source File 2:** `results/stats.csv`
    - **Filter:** `task == "T1"`, `N_train == 40`, `model_a == "PQK-1"`, `model_b == "PQK-2nn"`
    - **Row 19:** `mean_diff = -0.080290`, `ci_low = -0.095012`, `ci_high = -0.066189`, `p_holm_perN = 0.000015`
- **Tolerances:**
  - RNG sequential vs. merged CSV difference: $< 1.0 \times 10^{-10}$ (observed: $1.11 \times 10^{-16}$)
  - Holm step-down adjustment: exact monotonic ranking with $p_{\text{holm}} \ge p_{\text{raw}}$
  - Bootstrap 95% confidence intervals: bounded within $[-0.095012, -0.066189]$

---

## 4. Data-Access Points: StandardScaler and Inner Cross-Validation
An audit of data access and scaling points reveals:
1. **Outer Split Integrity:**
   - In `scripts/common.py` (lines 140–200), `make_split(...)` partitions states into disjoint training ($N_{\text{tr}}$) and test sets ($N_{\text{te}} = 200$). Test indices are frozen per seed.
2. **StandardScaler Fitting Point:**
   - In `scripts/common.py` (lines 360–362):
     ```python
     scaler = StandardScaler()
     X_e_train_std = scaler.fit_transform(X_e_train)
     X_e_test_std = scaler.transform(X_e_test)
     ```
     `StandardScaler` is fitted exclusively on `X_e_train` and transforms `X_e_test`.
   - *Observation:* Inside `tune_and_score_rbf` (inner CV), `X_e_train_std` is sliced into fold subsets (`D2_tr[np.ix_(tr_idx, tr_idx)]`) rather than refitting the feature scaler inside each inner fold.
3. **Inner Cross-Validation Data Access:**
   - In `scripts/common.py` (lines 341, 392–400):
     `kf = KFold(n_splits=3, shuffle=True, random_state=42)`
     Fold target normalization `(f_y_tr - f_m) / f_s` is strictly computed per training fold `tr_idx`, avoiding target leakage to validation fold `val_idx`.

---

## 5. Metrics to Record
- **Execution Runtime:** [Record seconds]
- **Peak Memory Footprint:** [Record MB]

---

## 6. Known Limitations
- At $N_{\text{tr}} = 10$, 3-fold inner cross-validation has only $\approx 6$–$7$ training samples per fold, causing high variance and edge boundary pegging.
- Pre-standardizing `X_e_train` prior to inner CV is computationally standard but strictly shares feature moment estimates across inner folds.

---

## 7. Results
*(Left empty for Gate-0 execution recording)*

```text

```
