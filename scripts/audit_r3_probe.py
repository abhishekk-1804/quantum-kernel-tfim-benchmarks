"""
scripts/audit_r3_probe.py
-------------------------
Audit R3: Source code inspection of PSD clipping paths and numerical probe
comparing:
  (a) Current production method: clip train Gram only (in CV folds and refit)
  (b) Alternative exploratory method: clip joint (N_tr + N_te) Gram first, then slice

Outputs:
  - docs/stage1/r3_clipping_paths.md
"""

import os
import sys
import time
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_absolute_error

# Add paths
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SCRIPTS = os.path.join(_PROJECT_ROOT, "scripts")
_SRC = os.path.join(_PROJECT_ROOT, "src")
for p in [_SRC, _SCRIPTS]:
    if p not in sys.path:
        sys.path.insert(0, p)

from common import (
    C_GRID_V2,
    EPSILON_GRID_V3,
    make_split,
)
from noise import (
    destructive_swap_test_fidelity,
    fidelity_clip_psd,
)

DOC_PATH = os.path.join(_PROJECT_ROOT, "docs", "stage1", "r3_clipping_paths.md")


def evaluate_svr_precomputed(
    K_tr: np.ndarray,
    y_tr_z: np.ndarray,
    y_tr_orig: np.ndarray,
    K_te: np.ndarray,
    y_te: np.ndarray,
    y_mean: float,
    y_std: float,
    kf: KFold,
    clip_psd: bool = False,
):
    folds_data = []
    for tr_idx, val_idx in kf.split(K_tr):
        f_y_tr = y_tr_orig[tr_idx]
        f_m, f_s = float(np.mean(f_y_tr)), float(np.std(f_y_tr))
        if f_s < 1e-12:
            f_s = 1.0
        f_y_tr_z = (f_y_tr - f_m) / f_s
        f_y_val = y_tr_orig[val_idx]
        K_fold_tr = K_tr[np.ix_(tr_idx, tr_idx)]
        K_fold_val = K_tr[np.ix_(val_idx, tr_idx)]
        if clip_psd:
            K_fold_tr = fidelity_clip_psd(K_fold_tr)
        folds_data.append((K_fold_tr, K_fold_val, f_y_tr_z, f_y_val, f_m, f_s))

    best_cv = -np.inf
    best_C, best_eps = C_GRID_V2[0], EPSILON_GRID_V3[0]

    for C_val in C_GRID_V2:
        for eps_val in EPSILON_GRID_V3:
            scores = []
            for K_fold_tr, K_fold_val, f_y_tr_z, f_y_val, f_m, f_s in folds_data:
                svr = SVR(kernel="precomputed", C=C_val, epsilon=eps_val)
                svr.fit(K_fold_tr, f_y_tr_z)
                pred_z = svr.predict(K_fold_val)
                pred_orig = pred_z * f_s + f_m
                scores.append(r2_score(f_y_val, pred_orig))
            mean_cv = float(np.mean(scores))
            if mean_cv > best_cv:
                best_cv = mean_cv
                best_C, best_eps = C_val, eps_val

    K_fit_tr = fidelity_clip_psd(K_tr) if clip_psd else K_tr
    svr_final = SVR(kernel="precomputed", C=best_C, epsilon=best_eps)
    svr_final.fit(K_fit_tr, y_tr_z)
    pred_te_z = svr_final.predict(K_te)
    pred_te = pred_te_z * y_std + y_mean

    test_r2 = float(r2_score(y_te, pred_te))
    test_mae = float(mean_absolute_error(y_te, pred_te))
    params_str = json.dumps({"C": float(best_C), "epsilon": float(best_eps)})
    return test_r2, test_mae, params_str, best_cv


def run_probe():
    n = 8
    N_train = 40
    N_test = 200
    S = 1000
    seeds = [0, 1, 2, 3, 4]
    kf = KFold(n_splits=3, shuffle=True, random_state=42)

    probe_results = []
    print(f"=== S1.3 R3 Numerical Probe (seeds={seeds}, S={S}) ===")

    for seed in seeds:
        train_states, tr_targets, test_states, te_targets, _ = make_split(
            task="t1", n=n, N=N_train, seed=seed, target_name="entropy"
        )
        all_states = np.vstack([train_states, test_states])
        K_pure_full = (all_states @ all_states.T) ** 2

        y_mean = float(np.mean(tr_targets))
        y_std = float(np.std(tr_targets))
        if y_std < 1e-12:
            y_std = 1.0
        y_tr_z = (tr_targets - y_mean) / y_std

        rng_seed = int(100000 * seed + S)
        rng = np.random.default_rng(rng_seed)

        # Destructive swap-test Gram matrix
        K_hat, lam_min_full_raw = destructive_swap_test_fidelity(K_pure_full, S, rng)

        # --- Method (a): Current production - clip train Gram only ---
        K_hat_tr = K_hat[:N_train, :N_train]
        K_hat_te = K_hat[N_train:, :N_train]
        lam_min_tr_raw = float(np.min(np.linalg.eigvalsh(K_hat_tr)))
        
        K_tr_clipped = fidelity_clip_psd(K_hat_tr)
        lam_min_tr_clipped = float(np.min(np.linalg.eigvalsh(K_tr_clipped)))

        r2_a, mae_a, params_a, cv_a = evaluate_svr_precomputed(
            K_hat_tr, y_tr_z, tr_targets, K_hat_te, te_targets,
            y_mean, y_std, kf, clip_psd=True
        )

        # --- Method (b): Joint clipping of (N_tr + N_te) Gram then slice ---
        K_joint_psd = fidelity_clip_psd(K_hat)
        lam_min_full_psd = float(np.min(np.linalg.eigvalsh(K_joint_psd)))

        K_joint_tr = K_joint_psd[:N_train, :N_train]
        K_joint_te = K_joint_psd[N_train:, :N_train]
        lam_min_joint_tr_sliced = float(np.min(np.linalg.eigvalsh(K_joint_tr)))

        r2_b, mae_b, params_b, cv_b = evaluate_svr_precomputed(
            K_joint_tr, y_tr_z, tr_targets, K_joint_te, te_targets,
            y_mean, y_std, kf, clip_psd=False
        )

        row = {
            "seed": seed,
            "r2_a": r2_a,
            "r2_b": r2_b,
            "delta_r2": r2_b - r2_a,
            "mae_a": mae_a,
            "mae_b": mae_b,
            "lam_min_tr_raw": lam_min_tr_raw,
            "lam_min_tr_clipped": lam_min_tr_clipped,
            "lam_min_full_raw": lam_min_full_raw,
            "lam_min_full_psd": lam_min_full_psd,
            "lam_min_joint_tr_sliced": lam_min_joint_tr_sliced,
            "params_a": params_a,
            "params_b": params_b,
        }
        probe_results.append(row)
        print(f"  Seed {seed:2d}: R2(a)={r2_a:.4f}, R2(b)={r2_b:.4f}, Delta={r2_b - r2_a:+.4f} | lam_min_tr_raw={lam_min_tr_raw:.3e}, lam_min_full_raw={lam_min_full_raw:.3e}")

    # Write documentation markdown file
    os.makedirs(os.path.dirname(os.path.abspath(DOC_PATH)), exist_ok=True)
    with open(DOC_PATH, "w", encoding="utf-8") as f:
        f.write("# R3 Audit: Fidelity Gram Matrix PSD Clipping Paths\n\n")
        f.write("Status: EXPLORATORY (Audit & Sensitivity Probe)\n\n")
        f.write("## 1. Source Code Inspection of Clipping Call Sites\n\n")
        f.write("Every call site of `fidelity_clip_psd` and `clip_psd` across the repository was statically identified:\n\n")
        f.write("| File | Line | Symbol / Context | Matrix Input | Matrix Clipped | Fit Matrix to SVR | Predict Matrix to SVR |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        f.write("| `scripts/run_t5_noise.py` | 179 | `def evaluate_svr_precomputed(..., clip_psd=False)` | Parameter declaration | N/A | N/A | N/A |\n")
        f.write("| `scripts/run_t5_noise.py` | 192-194 | `if clip_psd: K_fold_tr = fidelity_clip_psd(K_fold_tr)` | Inner CV fold train block | Fold train-train (`K_fold_tr`) | `K_fold_tr` (clipped) | `K_fold_val` (unclipped) |\n")
        f.write("| `scripts/run_t5_noise.py` | 214-217 | `K_fit_tr = fidelity_clip_psd(K_tr) if clip_psd else K_tr` | Full training Gram | Train-train (`K_tr`) | `K_fit_tr` (clipped) | `K_te` (unclipped) |\n")
        f.write("| `scripts/run_t5_noise.py` | 520-522 | Call for `Arm 3: FQ-raw` | Raw noisy Gram blocks | None (`clip_psd=False`) | `K_hat_tr` (raw) | `K_hat_te` (raw) |\n")
        f.write("| `scripts/run_t5_noise.py` | 535-537 | Call for `Arm 4: FQ-clipped` | Raw noisy Gram blocks | Train-train only (`clip_psd=True`) | `K_fit_tr` (clipped) | `K_hat_te` (unclipped) |\n")
        f.write("| `scripts/run_t5_noise.py` | 696-698 | Call for `Arm 3: FQ (mixed_state_overlap)` | Analytic depolarizing Gram | None (`clip_psd=False`) | `K_depol_tr` (analytic) | `K_depol_te` (analytic) |\n")
        f.write("| `src/noise.py` | 197-223 | `def fidelity_clip_psd(K)` | Implementation | Symmetric $m \\times m$ matrix | N/A (algorithm definition) | N/A |\n")
        f.write("| `tests/test_physics_core.py` | 1274-1275 | Test suite verification | Synthetic noisy matrix | Entire synthetic matrix | Verified PSD $\\lambda_{\\min} \\ge 0$ | N/A |\n\n")

        f.write("### Key Observations from Source Code Inspection\n")
        f.write("1. **Train-Only Clipping:** In the current production pipeline (`scripts/run_t5_noise.py`), `clip_psd=True` clips ONLY the square training Gram matrix $K_{\\text{tr}} \\in \\mathbb{R}^{N_{\\text{tr}} \\times N_{\\text{tr}}}$ (and inner CV fold training blocks $K_{\\text{fold\\_tr}}$). It does NOT clip the rectangular test-train block $K_{\\text{te}} \\in \\mathbb{R}^{N_{\\text{te}} \\times N_{\\text{tr}}}$.\n")
        f.write("2. **Joint Gram Matrix:** The joint $(N_{\\text{tr}} + N_{\\text{te}}) \\times (N_{\\text{tr}} + N_{\\text{te}})$ matrix is never projected onto the PSD cone in the production pipeline.\n\n")

        f.write("## 2. Numerical Sensitivity Probe (5 Seeds, S=1000)\n\n")
        f.write("Comparison between:\n")
        f.write("- **Method (a) [Current production]:** Clip train Gram matrix $K_{\\text{tr}}$ only.\n")
        f.write("- **Method (b) [Exploratory alternative]:** Clip joint $(N_{\\text{tr}} + N_{\\text{te}}) \\times (N_{\\text{tr}} + N_{\\text{te}})$ Gram matrix first, then slice into train and test blocks.\n\n")

        f.write("| Seed | $R^2$ (a: train-only) | $R^2$ (b: joint-clipped) | $\\Delta R^2$ (b - a) | MAE (a) | MAE (b) | $\\lambda_{\\min}(K_{\\text{tr}})$ raw | $\\lambda_{\\min}(K_{\\text{tr}})$ clipped | $\\lambda_{\\min}(K_{\\text{joint}})$ raw | $\\lambda_{\\min}(K_{\\text{joint}})$ clipped | $\\lambda_{\\min}(K_{\\text{joint\\_tr}})$ sliced |\n")
        f.write("| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")
        for r in probe_results:
            f.write(f"| {r['seed']} | {r['r2_a']:.4f} | {r['r2_b']:.4f} | {r['delta_r2']:+.4f} | {r['mae_a']:.4f} | {r['mae_b']:.4f} | {r['lam_min_tr_raw']:.3e} | {r['lam_min_tr_clipped']:.3e} | {r['lam_min_full_raw']:.3e} | {r['lam_min_full_psd']:.3e} | {r['lam_min_joint_tr_sliced']:.3e} |\n")

        mean_r2_a = np.mean([r["r2_a"] for r in probe_results])
        mean_r2_b = np.mean([r["r2_b"] for r in probe_results])
        mean_delta = np.mean([r["delta_r2"] for r in probe_results])
        f.write(f"| **Mean** | **{mean_r2_a:.4f}** | **{mean_r2_b:.4f}** | **{mean_delta:+.4f}** | - | - | - | - | - | - | - |\n\n")

        f.write("### Numerical Observations\n")
        f.write(f"- Across 5 seeds at S=1000, the mean R2 for train-only clipping (Method a) is {mean_r2_a:.4f}, while joint clipping (Method b) yields {mean_r2_b:.4f} (mean difference Delta R2 = {mean_delta:+.4f}).\n")
        f.write("- Slicing a principal submatrix from a PSD joint Gram matrix guarantees that the resulting training submatrix remains PSD (Cauchy interlacing theorem: lambda_i(K_joint_tr) >= lambda_min(K_joint) = 0).\n")

    print(f"\nWritten R3 documentation and probe report to {DOC_PATH}")


if __name__ == "__main__":
    run_probe()
