# S1.4 Data Leakage and Preprocessing Audit

Status: COMPLETED (Static Grep + Dynamic Execution Audit)

## 1. Executive Summary: Check Status

| Check ID | Description | Result | Evidence / Details |
| :--- | :--- | :---: | :--- |
| **CHK-LEAK-1** | `StandardScaler` fitted strictly on training data | **PASS** | All `fit` and `fit_transform` operations have input row count $\le N_{\text{train}}$. Zero test state vectors passed. |
| **CHK-LEAK-2** | `SVR` estimator fitted strictly on training folds and full train set | **PASS** | SVR Gram inputs to `.fit()` are exactly fold-size ($26$ or $27$) or full-train ($40$). No test samples in fit. |
| **CHK-LEAK-3** | `KFold` validation folds are proper subsets of training indices | **PASS** | KFold split called strictly on $X_{\text{tr}}$, max index $< N_{\text{train}}$, zero overlap with test indices. |
| **CHK-LEAK-4** | Target $y$ z-scoring uses training statistics only | **PASS** | Training $y$ normalized using $\mu_{\text{tr}}, \sigma_{\text{tr}}$; CV folds use fold-specific $\mu_{\text{fold\_tr}}, \sigma_{\text{fold\_tr}}$. Predictions unscaled by train stats. |
| **CHK-LEAK-5** | SVR epsilon parameter scaling units matched across arms | **PASS** | All regression models (FQ, PQK-1, PQK-2nn, E, E2) operate on standardized targets y_tr_z = (y - mu)/sigma, so epsilon in [0.1, 0.03, 0.01, 0.003, 0.001] applies to standard-deviation units uniformly. |

## 2. Static Grep Audit Table

The table below documents every identified occurrence of `StandardScaler`, `.fit()`, `.fit_transform()`, `cdist()`, and `KFold()` across the benchmark scripts:

| File | Line | Object / Method Call | Data Object Fit On / Computed On |
| :--- | :--- | :--- | :--- |
| `scripts/common.py` | 25 | `from sklearn.model_selection import KFold, StratifiedKFold` | Unknown |
| `scripts/common.py` | 28 | `from sklearn.preprocessing import StandardScaler` | Scaler instantiation |
| `scripts/common.py` | 341 | `kf = KFold(n_splits=3, shuffle=True, random_state=42)` | KFold CV splitter instantiation |
| `scripts/common.py` | 360 | `scaler = StandardScaler()` | Scaler instantiation |
| `scripts/common.py` | 361 | `X_e_train_std = scaler.fit_transform(X_e_train)` | fit_transform on: X_e_train |
| `scripts/common.py` | 388 | `D2_tr = cdist(X_tr, X_tr, metric="sqeuclidean")` | cdist on: X_tr, X_tr, metric="sqeuclidean" |
| `scripts/common.py` | 389 | `D2_te = cdist(X_te, X_tr, metric="sqeuclidean")` | cdist on: X_te, X_tr, metric="sqeuclidean" |
| `scripts/common.py` | 415 | `clf.fit(K_tr, f_y_tr_z)` | fit on: K_tr, f_y_tr_z |
| `scripts/common.py` | 428 | `clf_final.fit(K_final_tr, y_train_z)` | fit on: K_final_tr, y_train_z |
| `scripts/common.py` | 480 | `clf.fit(K_fold_tr, f_y_tr_z)` | fit on: K_fold_tr, f_y_tr_z |
| `scripts/common.py` | 491 | `clf_fq.fit(K_fq_train, y_train_z)` | fit on: K_fq_train, y_train_z |
| `scripts/common.py` | 533 | `clf.fit(X_e_train_std[tr_idx], f_y_tr_z)` | fit on: X_e_train_std[tr_idx], f_y_tr_z |
| `scripts/common.py` | 543 | `clf_ridge.fit(X_e_train_std, y_train_z)` | fit on: X_e_train_std, y_train_z |
| `scripts/run_t4_v2.py` | 57 | `from sklearn.model_selection import StratifiedKFold, KFold` | Unknown |
| `scripts/run_t4_v2.py` | 60 | `from sklearn.preprocessing import StandardScaler` | Scaler instantiation |
| `scripts/run_t4_v2.py` | 179 | `cv = KFold(n_splits=3, shuffle=True, random_state=42)` | KFold CV splitter instantiation |
| `scripts/run_t4_v2.py` | 189 | `scaler = StandardScaler()` | Scaler instantiation |
| `scripts/run_t4_v2.py` | 190 | `X_e_train_std = scaler.fit_transform(X_e_train)` | fit_transform on: X_e_train |
| `scripts/run_t4_v2.py` | 215 | `clf.fit(X_tr[tr_idx], train_labels[tr_idx])` | fit on: X_tr[tr_idx], train_labels[tr_idx] |
| `scripts/run_t4_v2.py` | 225 | `clf_final.fit(X_tr, train_labels)` | fit on: X_tr, train_labels |
| `scripts/run_t4_v2.py` | 255 | `clf.fit(K_fq_train[np.ix_(tr_idx, tr_idx)], train_labels[tr_idx])` | fit on: K_fq_train[np.ix_(tr_idx, tr_idx |
| `scripts/run_t4_v2.py` | 264 | `clf_fq.fit(K_fq_train, train_labels)` | fit on: K_fq_train, train_labels |
| `scripts/run_t4_v2.py` | 292 | `clf.fit(X_e_train_std[tr_idx], train_labels[tr_idx])` | fit on: X_e_train_std[tr_idx], train_labels[tr_idx] |
| `scripts/run_t4_v2.py` | 301 | `clf_rc.fit(X_e_train_std, train_labels)` | fit on: X_e_train_std, train_labels |
| `scripts/run_t4_v2.py` | 378 | `kf = KFold(n_splits=3, shuffle=True, random_state=42)` | KFold CV splitter instantiation |
| `scripts/run_t4_v2.py` | 388 | `scaler = StandardScaler()` | Scaler instantiation |
| `scripts/run_t4_v2.py` | 389 | `X_e_train_std = scaler.fit_transform(X_e_train)` | fit_transform on: X_e_train |
| `scripts/run_t4_v2.py` | 406 | `D2_tr = cdist(X_tr, X_tr, metric="sqeuclidean")` | cdist on: X_tr, X_tr, metric="sqeuclidean" |
| `scripts/run_t4_v2.py` | 407 | `D2_te = cdist(X_te, X_tr, metric="sqeuclidean")` | cdist on: X_te, X_tr, metric="sqeuclidean" |
| `scripts/run_t4_v2.py` | 433 | `svr.fit(K_tr, f_y_tr_z)` | fit on: K_tr, f_y_tr_z |
| `scripts/run_t4_v2.py` | 446 | `svr_final.fit(K_final_tr, y_train_z)` | fit on: K_final_tr, y_train_z |
| `scripts/run_t4_v2.py` | 489 | `svr.fit(K_fold_tr, f_y_tr_z)` | fit on: K_fold_tr, f_y_tr_z |
| `scripts/run_t4_v2.py` | 500 | `svr_fq.fit(K_fq_train, y_train_z)` | fit on: K_fq_train, y_train_z |
| `scripts/run_t4_v2.py` | 532 | `ridge.fit(X_e_train_std[tr_idx], f_y_tr_z)` | fit on: X_e_train_std[tr_idx], f_y_tr_z |
| `scripts/run_t4_v2.py` | 542 | `ridge_final.fit(X_e_train_std, y_train_z)` | fit on: X_e_train_std, y_train_z |
| `scripts/run_t5_noise.py` | 28 | `from sklearn.model_selection import KFold` | Unknown |
| `scripts/run_t5_noise.py` | 31 | `from sklearn.preprocessing import StandardScaler` | Scaler instantiation |
| `scripts/run_t5_noise.py` | 111 | `kf: KFold,` | Unknown |
| `scripts/run_t5_noise.py` | 114 | `D2_tr = cdist(X_tr, X_tr, metric="sqeuclidean")` | cdist on: X_tr, X_tr, metric="sqeuclidean" |
| `scripts/run_t5_noise.py` | 115 | `D2_te = cdist(X_te, X_tr, metric="sqeuclidean")` | cdist on: X_te, X_tr, metric="sqeuclidean" |
| `scripts/run_t5_noise.py` | 145 | `svr.fit(K_tr_fold, f_y_tr_z)` | fit on: K_tr_fold, f_y_tr_z |
| `scripts/run_t5_noise.py` | 160 | `svr_final.fit(K_full_tr, y_tr_z)` | fit on: K_full_tr, y_tr_z |
| `scripts/run_t5_noise.py` | 178 | `kf: KFold,` | Unknown |
| `scripts/run_t5_noise.py` | 204 | `svr.fit(K_fold_tr, f_y_tr_z)` | fit on: K_fold_tr, f_y_tr_z |
| `scripts/run_t5_noise.py` | 216 | `svr_final.fit(K_fit_tr, y_tr_z)` | fit on: K_fit_tr, y_tr_z |
| `scripts/run_t5_noise.py` | 234 | `kf: KFold,` | Unknown |
| `scripts/run_t5_noise.py` | 254 | `ridge.fit(X_fold_tr, f_y_tr_z)` | fit on: X_fold_tr, f_y_tr_z |
| `scripts/run_t5_noise.py` | 264 | `ridge_final.fit(X_tr_std, y_tr_z)` | fit on: X_tr_std, y_tr_z |
| `scripts/run_t5_noise.py` | 308 | `kf = KFold(n_splits=3, shuffle=True, random_state=42)` | KFold CV splitter instantiation |
| `scripts/run_t5_noise.py` | 476 | `scaler_e = StandardScaler()` | Scaler instantiation |
| `scripts/run_t5_noise.py` | 477 | `X_e_tr_std = scaler_e.fit_transform(X_e[:N_train])` | fit_transform on: X_e[:N_train] |
| `scripts/run_t5_noise.py` | 652 | `scaler_e_depol = StandardScaler()` | Scaler instantiation |
| `scripts/run_t5_noise.py` | 653 | `X_e_tr_depol_std = scaler_e_depol.fit_transform(X_e_depol[:N_train])` | fit_transform on: X_e_depol[:N_train] |

## 3. Dynamic Verification Details (Task 1, Seeds 0, 1, 2, N=40)

- **Test Set Isolation:** Intercepted all `StandardScaler.fit`, `StandardScaler.fit_transform`, and `SVR.fit` calls during full execution of `evaluate_regression_models`. In 100% of calls, the first dimension of the feature/kernel input was $\le N_{\text{train}} = 40$.
- **Cross-Validation Integrity:** Intercepted all `KFold.split()` invocations. All indices in `tr_idx` and `val_idx` satisfy $0 \le i < 40$. In CV folds, fold target statistics $(f_m, f_s)$ were computed strictly on `f_y_tr = train_targets[tr_idx]`.
- **Unit Consistency:** Because all models fit SVR on normalized targets $y_{\text{tr\_z}}$, the SVR loss parameter $\epsilon$ represents an absolute error tolerance in units of target standard deviations $\sigma_y$ across all kernel arms, ensuring a strictly fair parameter grid.
