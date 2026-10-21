"""
scripts/run_t4_v2.py
--------------------
Task 4 (v2): Frustrated 2D Ising Lattice with randomized parameters per state.
- Lattices: 2x4 (n=8) and 3x4 (n=12), OPEN boundary conditions.
- Ensemble: J1 = -1.0, J2 ~ U[-1.0, -0.1], g ~ U[0.2, 3.0] sampled per state.
- T4a: classification, label = sign(S(pi,pi) - S(pi,0)) (Neel=1 vs stripe=0).
       Drop states with |diff| < 1e-3 and log the dropped fraction.
       tag: "contained".
- T4b: regression, target = half-cut entropy across row cut (half_chain_entropy).
       tag: "not_contained".
- N_train in {10, 20, 40, 80}, 200 fixed test states per (lattice, seed).
- Arms:
  * Baseline: baseline_majority (T4a), baseline_mean (T4b)
  * PQK-1 (== RBF on <X>): gamma = c/n (gamma_E = c / (2n))
  * PQK-2nn: gamma = c/n (gamma_E = c / (4n)), lattice NN bonds
  * FQ: precomputed fidelity Gram matrix, tune C
  * E (raw, std): RBF on [<X_i>, all <Z_i Z_j> i<j], gamma = c / d
  * F (std): Ridge / RidgeClassifier on standardized E features
  * E2 (raw): RBF on 2pt_pauli_nn features, gamma = c / d_e2
  * E_X (raw): RBF on <X> features, gamma = c / (2n)
"""

import os
import sys
import csv
import time
import json
from collections import Counter
from typing import Dict, Any, List, Tuple
import numpy as np

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
_SRC_DIR = os.path.abspath(os.path.join(_SCRIPTS_DIR, "..", "src"))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from common import (
    get_parser,
    parse_seeds,
    write_run_meta,
    C_GRID,
    C_FACTORS,
    ALPHA_GRID,
)
from hamiltonians import build_frustrated_2d, ground_state, structure_factor, half_chain_entropy, expect_x
from kernels import classical_features

from sklearn.model_selection import StratifiedKFold, KFold
from sklearn.svm import SVC, SVR
from sklearn.linear_model import Ridge, RidgeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, balanced_accuracy_score, r2_score, mean_absolute_error


def generate_t4_states(rows: int, cols: int, seed: int, n_needed: int = 280) -> Tuple[np.ndarray, np.ndarray, np.ndarray, list, int, int]:
    """
    Generate ground states for frustrated 2D lattice.
    Rejects states with |S(pi, pi) - S(pi, 0)| < 1e-3.
    Returns:
        states: (n_needed, 2^n) array
        labels: (n_needed,) integer array (1 for Neel, 0 for Stripe)
        entropies: (n_needed,) float array (half-cut entropy)
        nn_bonds: list of (i, j) tuples
        dropped_count: int
        total_sampled: int
    """
    n = rows * cols
    rng = np.random.default_rng(seed * 10000 + n)
    
    states = []
    labels = []
    entropies = []
    dropped_count = 0
    total_sampled = 0
    nn_bonds_ret = None

    while len(states) < n_needed:
        total_sampled += 1
        g = float(rng.uniform(0.2, 3.0))
        J2 = float(rng.uniform(-1.0, -0.1))
        H, nn_bonds, _ = build_frustrated_2d(rows=rows, cols=cols, g=g, J1=-1.0, J2=J2)
        if nn_bonds_ret is None:
            nn_bonds_ret = nn_bonds

        _, psi, _ = ground_state(H, n, sector="even")
        sq = structure_factor(psi, rows, cols)
        s_pipi = sq.get((np.pi, np.pi), 0.0)
        s_pi0 = sq.get((np.pi, 0.0), 0.0)
        diff = s_pipi - s_pi0

        if abs(diff) < 1e-3:
            dropped_count += 1
            continue

        label = 1 if diff > 0 else 0
        ent = half_chain_entropy(psi, n)

        states.append(psi)
        labels.append(label)
        entropies.append(ent)

    return (
        np.array(states, dtype=np.float64),
        np.array(labels, dtype=int),
        np.array(entropies, dtype=float),
        nn_bonds_ret,
        dropped_count,
        total_sampled
    )


def evaluate_t4a_classification(
    lattice_str: str,
    n: int,
    N_train: int,
    seed: int,
    train_states: np.ndarray,
    train_labels: np.ndarray,
    test_states: np.ndarray,
    test_labels: np.ndarray,
    pairs: list,
) -> List[Dict[str, Any]]:
    """Fit and evaluate classification models for T4a."""
    results = []
    task = "T4a"
    target = "sq_diff_sign"
    tag = "contained"

    # Baseline majority
    classes, counts = np.unique(train_labels, return_counts=True)
    majority_class = classes[np.argmax(counts)]
    y_pred_base = np.full(len(test_labels), majority_class)

    acc_base = float(accuracy_score(test_labels, y_pred_base))
    bacc_base = float(balanced_accuracy_score(test_labels, y_pred_base))
    for m_name, val in [("accuracy", acc_base), ("balanced_accuracy", bacc_base)]:
        results.append({
            "task": task, "target": target, "tag": tag, "n": n, "lattice": lattice_str, "boundary": "open",
            "N_train": N_train, "seed": seed, "model": "baseline_majority", "variant": "none",
            "metric": m_name, "value": val, "best_params": "{}", "fit_seconds": 0.0,
        })

    # Abort check: single class in train or test
    if len(classes) < 2 or len(np.unique(test_labels)) < 2:
        print(f"  [ABORT WARNING] T4a single-class encountered for {lattice_str} seed={seed} N={N_train}")
        return results

    # Choose cross-validation scheme
    min_count = min(counts)
    if min_count >= 3:
        cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    else:
        cv = KFold(n_splits=3, shuffle=True, random_state=42)

    # Features
    X_x_train = np.array([expect_x(psi, n) for psi in train_states])
    X_x_test = np.array([expect_x(psi, n) for psi in test_states])

    X_e_train = np.array([classical_features(psi, n, mode="full_corr") for psi in train_states])
    X_e_test = np.array([classical_features(psi, n, mode="full_corr") for psi in test_states])
    d_e = X_e_train.shape[1]

    scaler = StandardScaler()
    X_e_train_std = scaler.fit_transform(X_e_train)
    X_e_test_std = scaler.transform(X_e_test)

    X_e2_train = np.array([classical_features(psi, n, mode="2pt_pauli_nn", pairs=pairs) for psi in train_states])
    X_e2_test = np.array([classical_features(psi, n, mode="2pt_pauli_nn", pairs=pairs) for psi in test_states])
    d_e2 = X_e2_train.shape[1]

    K_fq_train = (train_states @ train_states.T) ** 2
    K_fq_test = (test_states @ train_states.T) ** 2

    def tune_and_score_svc(X_tr, X_te, gamma_grid, model_name, variant, arm_tag):
        t0 = time.time()
        best_cv = -np.inf
        best_C, best_c = C_GRID[0], C_FACTORS[0]

        for C in C_GRID:
            for c_val in C_FACTORS:
                gamma = c_val / gamma_grid
                fold_scores = []
                for tr_idx, val_idx in cv.split(X_tr, train_labels):
                    if len(np.unique(train_labels[tr_idx])) < 2:
                        continue
                    clf = SVC(kernel="rbf", C=C, gamma=gamma)
                    clf.fit(X_tr[tr_idx], train_labels[tr_idx])
                    pred = clf.predict(X_tr[val_idx])
                    fold_scores.append(accuracy_score(train_labels[val_idx], pred))
                mean_acc = float(np.mean(fold_scores)) if fold_scores else 0.0
                if mean_acc > best_cv:
                    best_cv = mean_acc
                    best_C, best_c = C, c_val

        best_gamma = best_c / gamma_grid
        clf_final = SVC(kernel="rbf", C=best_C, gamma=best_gamma)
        clf_final.fit(X_tr, train_labels)
        pred = clf_final.predict(X_te)
        fit_sec = time.time() - t0

        acc = float(accuracy_score(test_labels, pred))
        bacc = float(balanced_accuracy_score(test_labels, pred))
        b_params = json.dumps({"C": best_C, "c": best_c, "gamma": float(best_gamma)})

        for m_name, val in [("accuracy", acc), ("balanced_accuracy", bacc)]:
            results.append({
                "task": task, "target": target, "tag": arm_tag, "n": n, "lattice": lattice_str, "boundary": "open",
                "N_train": N_train, "seed": seed, "model": model_name, "variant": variant,
                "metric": m_name, "value": val, "best_params": b_params, "fit_seconds": fit_sec,
            })

    # Arm 1: PQK-1
    tune_and_score_svc(X_x_train, X_x_test, 2.0 * n, "PQK-1 (== RBF on <X>)", "none", tag)
    # Arm 2: PQK-2nn
    tune_and_score_svc(X_e2_train, X_e2_test, 4.0 * n, "PQK-2nn", "none", tag)

    # Arm 3: FQ
    t0 = time.time()
    best_cv_fq = -np.inf
    best_C_fq = C_GRID[0]
    for C in C_GRID:
        fold_scores = []
        for tr_idx, val_idx in cv.split(train_states, train_labels):
            if len(np.unique(train_labels[tr_idx])) < 2:
                continue
            clf = SVC(kernel="precomputed", C=C)
            clf.fit(K_fq_train[np.ix_(tr_idx, tr_idx)], train_labels[tr_idx])
            pred = clf.predict(K_fq_train[np.ix_(val_idx, tr_idx)])
            fold_scores.append(accuracy_score(train_labels[val_idx], pred))
        mean_acc = float(np.mean(fold_scores)) if fold_scores else 0.0
        if mean_acc > best_cv_fq:
            best_cv_fq = mean_acc
            best_C_fq = C

    clf_fq = SVC(kernel="precomputed", C=best_C_fq)
    clf_fq.fit(K_fq_train, train_labels)
    pred_fq = clf_fq.predict(K_fq_test)
    fit_sec_fq = time.time() - t0
    acc_fq = float(accuracy_score(test_labels, pred_fq))
    bacc_fq = float(balanced_accuracy_score(test_labels, pred_fq))
    b_params_fq = json.dumps({"C": best_C_fq})
    for m_name, val in [("accuracy", acc_fq), ("balanced_accuracy", bacc_fq)]:
        results.append({
            "task": task, "target": target, "tag": tag, "n": n, "lattice": lattice_str, "boundary": "open",
            "N_train": N_train, "seed": seed, "model": "FQ", "variant": "none",
            "metric": m_name, "value": val, "best_params": b_params_fq, "fit_seconds": fit_sec_fq,
        })

    # Arm 4: E (raw)
    tune_and_score_svc(X_e_train, X_e_test, float(d_e), "E", "raw", tag)
    # Arm 5: E (std)
    tune_and_score_svc(X_e_train_std, X_e_test_std, float(d_e), "E", "std", tag)

    # Arm 6: F (RidgeClassifier)
    t0 = time.time()
    best_cv_rc = -np.inf
    best_alpha = ALPHA_GRID[0]
    for alpha in ALPHA_GRID:
        fold_scores = []
        for tr_idx, val_idx in cv.split(X_e_train_std, train_labels):
            if len(np.unique(train_labels[tr_idx])) < 2:
                continue
            clf = RidgeClassifier(alpha=alpha)
            clf.fit(X_e_train_std[tr_idx], train_labels[tr_idx])
            pred = clf.predict(X_e_train_std[val_idx])
            fold_scores.append(accuracy_score(train_labels[val_idx], pred))
        mean_acc = float(np.mean(fold_scores)) if fold_scores else 0.0
        if mean_acc > best_cv_rc:
            best_cv_rc = mean_acc
            best_alpha = alpha

    clf_rc = RidgeClassifier(alpha=best_alpha)
    clf_rc.fit(X_e_train_std, train_labels)
    pred_rc = clf_rc.predict(X_e_test_std)
    fit_sec_rc = time.time() - t0
    acc_rc = float(accuracy_score(test_labels, pred_rc))
    bacc_rc = float(balanced_accuracy_score(test_labels, pred_rc))
    b_params_rc = json.dumps({"alpha": float(best_alpha)})
    for m_name, val in [("accuracy", acc_rc), ("balanced_accuracy", bacc_rc)]:
        results.append({
            "task": task, "target": target, "tag": tag, "n": n, "lattice": lattice_str, "boundary": "open",
            "N_train": N_train, "seed": seed, "model": "F", "variant": "std",
            "metric": m_name, "value": val, "best_params": b_params_rc, "fit_seconds": fit_sec_rc,
        })

    # Arm 7: E2
    tune_and_score_svc(X_e2_train, X_e2_test, float(d_e2), "E2", "raw", "sanity")
    # Arm 8: E_X with c/(2n) grid
    tune_and_score_svc(X_x_train, X_x_test, 2.0 * n, "E_X", "raw", "sanity")

    return results


def evaluate_t4b_regression(
    lattice_str: str,
    n: int,
    N_train: int,
    seed: int,
    train_states: np.ndarray,
    train_targets: np.ndarray,
    test_states: np.ndarray,
    test_targets: np.ndarray,
    pairs: list,
) -> List[Dict[str, Any]]:
    """Fit and evaluate regression models for T4b."""
    results = []
    task = "T4b"
    target = "half_cut_entropy"
    tag = "not_contained"

    # Target statistics from TRAIN only
    y_mean = float(np.mean(train_targets))
    y_std = float(np.std(train_targets))
    if y_std < 1e-12:
        y_std = 1.0
    y_train_z = (train_targets - y_mean) / y_std

    # Baseline: predict train mean
    y_pred_base = np.full(len(test_targets), y_mean)
    r2_base = float(r2_score(test_targets, y_pred_base))
    mae_base = float(mean_absolute_error(test_targets, y_pred_base))
    for metric, val in [("r2", r2_base), ("mae", mae_base)]:
        results.append({
            "task": task, "target": target, "tag": tag, "n": n, "lattice": lattice_str, "boundary": "open",
            "N_train": N_train, "seed": seed, "model": "baseline_mean", "variant": "none",
            "metric": metric, "value": val, "best_params": "{}", "fit_seconds": 0.0,
        })

    kf = KFold(n_splits=3, shuffle=True, random_state=42)

    # Features
    X_x_train = np.array([expect_x(psi, n) for psi in train_states])
    X_x_test = np.array([expect_x(psi, n) for psi in test_states])

    X_e_train = np.array([classical_features(psi, n, mode="full_corr") for psi in train_states])
    X_e_test = np.array([classical_features(psi, n, mode="full_corr") for psi in test_states])
    d_e = X_e_train.shape[1]

    scaler = StandardScaler()
    X_e_train_std = scaler.fit_transform(X_e_train)
    X_e_test_std = scaler.transform(X_e_test)

    X_e2_train = np.array([classical_features(psi, n, mode="2pt_pauli_nn", pairs=pairs) for psi in train_states])
    X_e2_test = np.array([classical_features(psi, n, mode="2pt_pauli_nn", pairs=pairs) for psi in test_states])
    d_e2 = X_e2_train.shape[1]

    K_fq_train = (train_states @ train_states.T) ** 2
    K_fq_test = (test_states @ train_states.T) ** 2

    def tune_and_score_svr(X_tr, X_te, gamma_grid, model_name, variant, arm_tag):
        t0 = time.time()
        best_cv = -np.inf
        best_C, best_c = C_GRID[0], C_FACTORS[0]

        for C in C_GRID:
            for c_val in C_FACTORS:
                gamma = c_val / gamma_grid
                fold_scores = []
                for tr_idx, val_idx in kf.split(X_tr):
                    svr = SVR(kernel="rbf", C=C, epsilon=0.1, gamma=gamma)
                    svr.fit(X_tr[tr_idx], y_train_z[tr_idx])
                    pred_z = svr.predict(X_tr[val_idx])
                    pred_phys = pred_z * y_std + y_mean
                    fold_scores.append(r2_score(train_targets[val_idx], pred_phys))
                mean_r2 = float(np.mean(fold_scores))
                if mean_r2 > best_cv:
                    best_cv = mean_r2
                    best_C, best_c = C, c_val

        best_gamma = best_c / gamma_grid
        svr_final = SVR(kernel="rbf", C=best_C, epsilon=0.1, gamma=best_gamma)
        svr_final.fit(X_tr, y_train_z)
        pred_z = svr_final.predict(X_te)
        pred_phys = pred_z * y_std + y_mean
        fit_sec = time.time() - t0

        r2 = float(r2_score(test_targets, pred_phys))
        mae = float(mean_absolute_error(test_targets, pred_phys))
        b_params = json.dumps({"C": best_C, "c": best_c, "gamma": float(best_gamma)})

        for m_name, val in [("r2", r2), ("mae", mae)]:
            results.append({
                "task": task, "target": target, "tag": arm_tag, "n": n, "lattice": lattice_str, "boundary": "open",
                "N_train": N_train, "seed": seed, "model": model_name, "variant": variant,
                "metric": m_name, "value": val, "best_params": b_params, "fit_seconds": fit_sec,
            })

    # Arm 1: PQK-1
    tune_and_score_svr(X_x_train, X_x_test, 2.0 * n, "PQK-1 (== RBF on <X>)", "none", tag)
    # Arm 2: PQK-2nn
    tune_and_score_svr(X_e2_train, X_e2_test, 4.0 * n, "PQK-2nn", "none", tag)

    # Arm 3: FQ
    t0 = time.time()
    best_cv_fq = -np.inf
    best_C_fq = C_GRID[0]
    for C in C_GRID:
        fold_scores = []
        for tr_idx, val_idx in kf.split(train_states):
            svr = SVR(kernel="precomputed", C=C, epsilon=0.1)
            svr.fit(K_fq_train[np.ix_(tr_idx, tr_idx)], y_train_z[tr_idx])
            pred_z = svr.predict(K_fq_train[np.ix_(val_idx, tr_idx)])
            pred_phys = pred_z * y_std + y_mean
            fold_scores.append(r2_score(train_targets[val_idx], pred_phys))
        mean_r2 = float(np.mean(fold_scores))
        if mean_r2 > best_cv_fq:
            best_cv_fq = mean_r2
            best_C_fq = C

    svr_fq = SVR(kernel="precomputed", C=best_C_fq, epsilon=0.1)
    svr_fq.fit(K_fq_train, y_train_z)
    pred_z = svr_fq.predict(K_fq_test)
    pred_phys = pred_z * y_std + y_mean
    fit_sec_fq = time.time() - t0
    r2_fq = float(r2_score(test_targets, pred_phys))
    mae_fq = float(mean_absolute_error(test_targets, pred_phys))
    b_params_fq = json.dumps({"C": best_C_fq})
    for m_name, val in [("r2", r2_fq), ("mae", mae_fq)]:
        results.append({
            "task": task, "target": target, "tag": tag, "n": n, "lattice": lattice_str, "boundary": "open",
            "N_train": N_train, "seed": seed, "model": "FQ", "variant": "none",
            "metric": m_name, "value": val, "best_params": b_params_fq, "fit_seconds": fit_sec_fq,
        })

    # Arm 4: E (raw)
    tune_and_score_svr(X_e_train, X_e_test, float(d_e), "E", "raw", tag)
    # Arm 5: E (std)
    tune_and_score_svr(X_e_train_std, X_e_test_std, float(d_e), "E", "std", tag)

    # Arm 6: F (Ridge)
    t0 = time.time()
    best_cv_ridge = -np.inf
    best_alpha = ALPHA_GRID[0]
    for alpha in ALPHA_GRID:
        fold_scores = []
        for tr_idx, val_idx in kf.split(X_e_train_std):
            ridge = Ridge(alpha=alpha)
            ridge.fit(X_e_train_std[tr_idx], y_train_z[tr_idx])
            pred_z = ridge.predict(X_e_train_std[val_idx])
            pred_phys = pred_z * y_std + y_mean
            fold_scores.append(r2_score(train_targets[val_idx], pred_phys))
        mean_r2 = float(np.mean(fold_scores))
        if mean_r2 > best_cv_ridge:
            best_cv_ridge = mean_r2
            best_alpha = alpha

    ridge_final = Ridge(alpha=best_alpha)
    ridge_final.fit(X_e_train_std, y_train_z)
    pred_z = ridge_final.predict(X_e_test_std)
    pred_phys = pred_z * y_std + y_mean
    fit_sec_ridge = time.time() - t0
    r2_ridge = float(r2_score(test_targets, pred_phys))
    mae_ridge = float(mean_absolute_error(test_targets, pred_phys))
    b_params_ridge = json.dumps({"alpha": float(best_alpha)})
    for m_name, val in [("r2", r2_ridge), ("mae", mae_ridge)]:
        results.append({
            "task": task, "target": target, "tag": tag, "n": n, "lattice": lattice_str, "boundary": "open",
            "N_train": N_train, "seed": seed, "model": "F", "variant": "std",
            "metric": m_name, "value": val, "best_params": b_params_ridge, "fit_seconds": fit_sec_ridge,
        })

    # Arm 7: E2
    tune_and_score_svr(X_e2_train, X_e2_test, float(d_e2), "E2", "raw", "sanity")
    # Arm 8: E_X with c/(2n) grid
    tune_and_score_svr(X_x_train, X_x_test, 2.0 * n, "E_X", "raw", "sanity")

    return results


def run_t4_v2(seeds, quick=False, out_csv=None):
    if out_csv is None:
        out_csv = os.path.join("results", "t4_v2.csv")

    cb_csv = os.path.join("results", "t4_v2_class_balance.csv")
    write_run_meta()

    if quick:
        lattices = [("2x4", 2, 4)]
        n_train_list = [10, 20]
    else:
        lattices = [("2x4", 2, 4), ("3x4", 3, 4)]
        n_train_list = [10, 20, 40, 80]

    os.makedirs(os.path.dirname(os.path.abspath(cb_csv)), exist_ok=True)
    with open(cb_csv, "w", encoding="utf-8") as f_cb:
        f_cb.write("lattice,seed,total_sampled,dropped_count,dropped_fraction,n_neel,n_stripe,frac_neel,frac_stripe,decision\n")

    os.makedirs(os.path.dirname(os.path.abspath(out_csv)), exist_ok=True)
    fieldnames = [
        "task", "target", "tag", "n", "lattice", "boundary",
        "N_train", "seed", "model", "variant", "metric", "value",
        "best_params", "fit_seconds"
    ]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

    print(f"=== Starting T4 (v2) Benchmark (Lattices: {[l[0] for l in lattices]}, Seeds: {seeds}, N_train: {n_train_list}) ===")
    total_rows = 0
    t_start = time.time()

    for seed in seeds:
        t_seed = time.time()
        for lattice_str, rows, cols in lattices:
            n = rows * cols
            
            # Generate 80 train states + 200 test states = 280 states
            states, labels, ents, pairs, dropped_cnt, total_samp = generate_t4_states(
                rows=rows, cols=cols, seed=seed, n_needed=280
            )

            # Class balance logging over all 280 states
            n_neel = int(np.sum(labels == 1))
            n_stripe = int(np.sum(labels == 0))
            frac_neel = n_neel / 280.0
            frac_stripe = n_stripe / 280.0
            drop_frac = dropped_cnt / float(total_samp) if total_samp > 0 else 0.0

            if min(frac_neel, frac_stripe) < 0.15:
                decision = f"WARNING: minority class < 15% (neel={frac_neel:.1%}, stripe={frac_stripe:.1%})"
            else:
                decision = "Balanced classes >= 15%"

            with open(cb_csv, "a", encoding="utf-8") as f_cb:
                f_cb.write(f"{lattice_str},{seed},{total_samp},{dropped_cnt},{drop_frac:.6f},{n_neel},{n_stripe},{frac_neel:.4f},{frac_stripe:.4f},\"{decision}\"\n")

            # Training pool: first 80 states
            # Test pool: states 80 to 280 (200 states)
            test_states = states[80:280]
            test_labels = labels[80:280]
            test_ents = ents[80:280]

            for N in n_train_list:
                train_states = states[:N]
                train_labels = labels[:N]
                train_ents = ents[:N]

                # Evaluate T4a (Classification)
                rows_a = evaluate_t4a_classification(
                    lattice_str=lattice_str, n=n, N_train=N, seed=seed,
                    train_states=train_states, train_labels=train_labels,
                    test_states=test_states, test_labels=test_labels,
                    pairs=pairs
                )
                with open(out_csv, "a", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    for r in rows_a:
                        writer.writerow({k: r.get(k, "") for k in fieldnames})
                    f.flush()
                total_rows += len(rows_a)

                # Evaluate T4b (Regression)
                rows_b = evaluate_t4b_regression(
                    lattice_str=lattice_str, n=n, N_train=N, seed=seed,
                    train_states=train_states, train_targets=train_ents,
                    test_states=test_states, test_targets=test_ents,
                    pairs=pairs
                )
                with open(out_csv, "a", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    for r in rows_b:
                        writer.writerow({k: r.get(k, "") for k in fieldnames})
                    f.flush()
                total_rows += len(rows_b)

        print(f"  [T4 v2] Seed {seed:2d} completed in {time.time() - t_seed:.2f}s (logged {total_rows} rows so far)")

    total_time = time.time() - t_start
    print(f"=== T4 v2 Benchmark complete: {total_rows} rows in {total_time:.2f}s -> {out_csv} ===")
    return total_time


if __name__ == "__main__":
    parser = get_parser(description="Run Task 4 v2 (Frustrated Lattice Redesign) Benchmark")
    args = parser.parse_args()
    seeds = parse_seeds(args)
    run_t4_v2(seeds, quick=args.quick, out_csv=args.out)
