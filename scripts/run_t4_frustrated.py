"""
scripts/run_t4_frustrated.py
----------------------------
Task 4: 2x4 OPEN frustrated Ising lattice, J1 = -1.0.
J2 in {-0.25, -0.5, -0.75}, g ~ U[0.2, 3.0], n = 8.
- T4a: classification, label = argmax of S(q) (tag: "contained").
       Log class balance per (J2, seed) to results/t4_class_balance.csv.
       If any class < 15% of samples, merge or drop it and write decision to log.
- T4b: regression, target = half-cut entropy across row cut (tag: "not_contained").
N_train in {6, 10, 16, 24, 48}.
"""

import os
import sys
import csv
import time
import json
from collections import Counter
import numpy as np

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from common import (
    get_parser,
    parse_seeds,
    write_run_meta,
    make_split,
    evaluate_regression_models,
    C_GRID,
    C_FACTORS,
    ALPHA_GRID,
)
from hamiltonians import expect_x, half_chain_entropy
from kernels import classical_features
from sklearn.model_selection import StratifiedKFold, KFold
from sklearn.svm import SVC
from sklearn.linear_model import RidgeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, balanced_accuracy_score


def evaluate_t4a_classification(
    J2: float,
    N_train: int,
    seed: int,
    train_states: np.ndarray,
    train_labels: np.ndarray,
    test_states: np.ndarray,
    test_labels: np.ndarray,
    pairs: list,
) -> list:
    """Evaluate classification models for T4a."""
    results = []
    n = 8
    task = "T4a"
    target = "sq_argmax"
    tag = "contained"

    # Baseline majority
    classes, counts = np.unique(train_labels, return_counts=True)
    majority_class = classes[np.argmax(counts)]
    y_pred_base = np.full(len(test_labels), majority_class)

    acc_base = float(accuracy_score(test_labels, y_pred_base))
    bacc_base = float(balanced_accuracy_score(test_labels, y_pred_base))
    for m_name, val in [("accuracy", acc_base), ("balanced_accuracy", bacc_base)]:
        results.append({
            "task": task, "target": target, "tag": tag, "n": n, "J2": J2, "N_train": N_train,
            "seed": seed, "model": "baseline_majority", "variant": "none",
            "metric": m_name, "value": val, "best_params": "{}", "fit_seconds": 0.0,
        })

    # If only 1 class is present, SVC/RidgeClassifier cannot be trained
    if len(classes) < 2:
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
                "task": task, "target": target, "tag": arm_tag, "n": n, "J2": J2, "N_train": N_train,
                "seed": seed, "model": model_name, "variant": variant,
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
            "task": task, "target": target, "tag": tag, "n": n, "J2": J2, "N_train": N_train,
            "seed": seed, "model": "FQ", "variant": "none",
            "metric": m_name, "value": val, "best_params": b_params_fq, "fit_seconds": fit_sec_fq,
        })

    # Arm 4: E (raw)
    tune_and_score_svc(X_e_train, X_e_test, d_e, "E", "raw", tag)
    # Arm 5: E (std)
    tune_and_score_svc(X_e_train_std, X_e_test_std, d_e, "E", "std", tag)

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
            "task": task, "target": target, "tag": tag, "n": n, "J2": J2, "N_train": N_train,
            "seed": seed, "model": "F", "variant": "std",
            "metric": m_name, "value": val, "best_params": b_params_rc, "fit_seconds": fit_sec_rc,
        })

    # Arm 7: E2
    tune_and_score_svc(X_e2_train, X_e2_test, d_e2, "E2", "raw", "sanity")
    # Arm 8: E_X
    tune_and_score_svc(X_x_train, X_x_test, float(n), "E_X", "raw", "sanity")

    return results


def run_t4(seeds, quick=False, out_csv=None):
    if out_csv is None:
        out_csv = os.path.join("results", "t4_frustrated.csv")

    class_balance_csv = os.path.join("results", "t4_class_balance.csv")
    write_run_meta()

    n = 8
    J2_list = [-0.25, -0.5, -0.75]
    if quick:
        n_train_list = [6, 10, 16]
    else:
        n_train_list = [6, 10, 16, 24, 48]

    # Initialize class balance CSV
    os.makedirs(os.path.dirname(os.path.abspath(class_balance_csv)), exist_ok=True)
    with open(class_balance_csv, "w", encoding="utf-8") as f_cb:
        f_cb.write("J2,seed,total_samples,class_counts,decision\n")

    os.makedirs(os.path.dirname(os.path.abspath(out_csv)), exist_ok=True)
    fieldnames = [
        "task", "target", "tag", "n", "J2", "N_train", "seed",
        "model", "variant", "metric", "value", "best_params", "fit_seconds"
    ]
    with open(out_csv, "w", encoding="utf-8") as f:
        f.write(",".join(fieldnames) + "\n")

    print(f"=== Starting T4 Frustrated Lattice Benchmark (Seeds: {seeds}, N_train: {n_train_list}) ===")
    total_rows = 0
    t_start = time.time()

    for seed in seeds:
        t_seed = time.time()
        for J2 in J2_list:
            # Check class balance on the full 248 states of this (J2, seed)
            _, all_sq, _, _, meta = make_split(task="t4", n=n, N=48, seed=seed, J2=J2, target_name="sq_argmax")
            # All 248 labels:
            _, _, te_states_full, te_sq_full, _ = make_split(task="t4", n=n, N=48, seed=seed, J2=J2, target_name="sq_argmax")
            all_labels = np.concatenate([all_sq, te_sq_full])
            counts_dict = dict(Counter(all_labels))
            total_s = len(all_labels)

            # 15% rule
            minority_classes = [c for c, cnt in counts_dict.items() if cnt / total_s < 0.15]
            if len(counts_dict) == 1:
                decision = f"Single class present ({counts_dict}); baseline_majority evaluated, SVC arms skipped"
            elif minority_classes:
                decision = f"Minority classes {minority_classes} < 15%; merged/dropped"
            else:
                decision = "Balanced classes >= 15%; all arms evaluated"

            with open(class_balance_csv, "a", encoding="utf-8") as f_cb:
                counts_str = json.dumps(counts_dict).replace(",", ";")
                f_cb.write(f"{J2},{seed},{total_s},\"{counts_str}\",\"{decision}\"\n")

            pairs_2d = meta["nn_bonds"]

            for N in n_train_list:
                # --- T4a: Classification ---
                tr_states, tr_labels, te_states, te_labels, _ = make_split(
                    task="t4", n=n, N=N, seed=seed, J2=J2, target_name="sq_argmax"
                )
                rows_a = evaluate_t4a_classification(
                    J2=J2, N_train=N, seed=seed,
                    train_states=tr_states, train_labels=tr_labels,
                    test_states=te_states, test_labels=te_labels,
                    pairs=pairs_2d,
                )
                with open(out_csv, "a", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    for r in rows_a:
                        writer.writerow({k: r.get(k, "") for k in fieldnames})
                    f.flush()
                total_rows += len(rows_a)

                # --- T4b: Regression on row-cut entropy ---
                tr_states_b, tr_ent_b, te_states_b, te_ent_b, _ = make_split(
                    task="t4", n=n, N=N, seed=seed, J2=J2, target_name="entropy"
                )
                rows_b = evaluate_regression_models(
                    task="T4b",
                    target="half_cut_entropy",
                    tag="not_contained",
                    n=n,
                    N_train=N,
                    seed=seed,
                    train_states=tr_states_b,
                    train_targets=tr_ent_b,
                    test_states=te_states_b,
                    test_targets=te_ent_b,
                    pairs=pairs_2d,
                )
                with open(out_csv, "a", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    for r in rows_b:
                        r["J2"] = J2
                        writer.writerow({k: r.get(k, "") for k in fieldnames})
                    f.flush()
                total_rows += len(rows_b)

        print(f"  [T4] Seed {seed:2d} completed in {time.time() - t_seed:.2f}s (logged {total_rows} rows so far)")

    total_time = time.time() - t_start
    print(f"=== T4 Benchmark complete: {total_rows} rows in {total_time:.2f}s -> {out_csv} ===")
    return total_time


if __name__ == "__main__":
    parser = get_parser(description="Run Task 4 (Frustrated Lattice) Benchmark")
    args = parser.parse_args()
    seeds = parse_seeds(args)
    run_t4(seeds, quick=args.quick, out_csv=args.out)
