"""
scripts/run_t5_depol_fixedhp.py
Executes Step 0b: Task 1 half-chain entropy, n=8, N=40, 20 seeds,
per-qubit local depolarizing p in {0.00, 0.02, 0.04, 0.06, 0.08} with FIXED hyperparameters
(C, c, epsilon) set to the p=0.00 optimum recorded in results/t5_noise.csv.
Evaluated arms: PQK-1, PQK-2nn, FQ (variant: mixed_state_overlap), E (raw), E2 (raw).
Asserts that at p=0.00, fixed-hp R^2 reproduces the tuned p=0 baseline to < 1e-10.
Output schema: seed, p, model, variant, r2, mae, hp_source
Includes incremental CSV writing and resumption.
"""
import os
import sys
import json
import time
from multiprocessing import Pool, cpu_count
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_absolute_error

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC = os.path.join(_PROJECT_ROOT, "src")
_SCRIPTS = os.path.join(_PROJECT_ROOT, "scripts")
for p in [_PROJECT_ROOT, _SRC, _SCRIPTS]:
    if p not in sys.path:
        sys.path.insert(0, p)

from common import SEEDS, make_split
from kernels import classical_features

# Precomputed bit tables for n=8
_DIM = 256
_N = 8
_DEPOL_TABLES = []
_IDX = np.arange(_DIM)
for _k in range(_N):
    _flip = 1 << (_N - 1 - _k)
    _bits = (_IDX >> (_N - 1 - _k)) & 1
    _same_bit = (_bits[:, None] == _bits[None, :])
    _idx_flipped = _IDX ^ _flip
    _DEPOL_TABLES.append((_same_bit, _idx_flipped))


def fast_local_depolarizing_channel(rho: np.ndarray, p: float) -> np.ndarray:
    if p == 0.0:
        return rho.copy()
    curr = rho.copy()
    for same_bit, idx_flipped in _DEPOL_TABLES:
        rho_flipped = curr[np.ix_(idx_flipped, idx_flipped)]
        out = np.empty_like(curr)
        out[~same_bit] = (1.0 - p) * curr[~same_bit]
        out[same_bit] = (1.0 - 0.5 * p) * curr[same_bit] + 0.5 * p * rho_flipped[same_bit]
        curr = out
    return curr


def fast_local_depolarizing_fidelity_gram(states: np.ndarray, p: float) -> np.ndarray:
    if p == 0.0:
        K = (states @ states.T) ** 2
        np.fill_diagonal(K, 1.0)
        return K
    rhos = [fast_local_depolarizing_channel(np.outer(s, s), p) for s in states]
    R = np.array([r.reshape(-1) for r in rhos])
    overlap = np.real(R @ R.conj().T)
    diag = np.sqrt(np.diag(overlap))
    K = overlap / np.outer(diag, diag)
    np.fill_diagonal(K, 1.0)
    return K


# Global p0_df loaded once for workers
_P0_DICT = {}

def init_worker(p0_dict):
    global _P0_DICT
    _P0_DICT = p0_dict


def process_seed(seed):
    t_seed = time.time()
    n = 8
    N_train = 40
    N_test = 200
    p_sweep = [0.00, 0.02, 0.04, 0.06, 0.08]

    # Arms configuration: (model, variant, gamma_denom)
    eval_arms = [
        ("PQK-1", "none", 16),
        ("PQK-2nn", "none", 32),
        ("FQ", "mixed_state_overlap", None),
        ("E", "raw", 52),
        ("E2", "raw", 35),
    ]

    tr_states, tr_targets, te_states, te_targets, _ = make_split("t1", n=n, N=N_train, seed=seed)
    all_states = np.vstack([tr_states, te_states])

    y_mean = float(np.mean(tr_targets))
    y_std = float(np.std(tr_targets))
    if y_std < 1e-12:
        y_std = 1.0
    y_tr_z = (tr_targets - y_mean) / y_std

    pure_x_all = np.array([classical_features(psi, n, mode="1pt_X") for psi in all_states])
    pure_e2_all = np.array([classical_features(psi, n, mode="2pt_pauli_nn") for psi in all_states])
    pure_e_all = np.array([classical_features(psi, n, mode="full_corr") for psi in all_states])

    seed_results = []
    max_diff_seed = 0.0

    for p_val in p_sweep:
        scale_1 = 1.0 - p_val
        scale_2 = (1.0 - p_val) ** 2

        X_pqk1 = scale_1 * pure_x_all
        scale_e2 = np.tile([scale_1, scale_1, scale_2, scale_2, scale_2], n - 1)
        X_e2 = pure_e2_all * scale_e2
        scale_e = np.concatenate([np.full(3 * n, scale_1), np.full(n * (n - 1) // 2, scale_2)])
        X_e = pure_e_all * scale_e

        if p_val == 0.0:
            K_depol_tr = (tr_states @ tr_states.T) ** 2
            K_depol_te = (te_states @ tr_states.T) ** 2
        else:
            K_depol_full = fast_local_depolarizing_fidelity_gram(all_states, p=p_val)
            K_depol_tr = K_depol_full[:N_train, :N_train]
            K_depol_te = K_depol_full[N_train:, :N_train]

        for mod, var, gamma_denom in eval_arms:
            params, r2_ref = _P0_DICT[(seed, mod, var)]
            C = params["C"]
            eps = params["epsilon"]

            if mod == "FQ":
                svr = SVR(kernel="precomputed", C=C, epsilon=eps)
                svr.fit(K_depol_tr, y_tr_z)
                pred_z = svr.predict(K_depol_te)
            else:
                if mod == "PQK-1":
                    X_curr = X_pqk1
                elif mod in ("PQK-2nn", "E2"):
                    X_curr = X_e2
                elif mod == "E":
                    X_curr = X_e
                else:
                    raise ValueError(f"Unknown model {mod}")

                gamma = params.get("gamma", params["c"] / gamma_denom)
                D2_tr = cdist(X_curr[:N_train], X_curr[:N_train], metric="sqeuclidean")
                D2_te = cdist(X_curr[N_train:], X_curr[:N_train], metric="sqeuclidean")
                K_tr = np.exp(-gamma * D2_tr)
                K_te = np.exp(-gamma * D2_te)

                svr = SVR(kernel="precomputed", C=C, epsilon=eps)
                svr.fit(K_tr, y_tr_z)
                pred_z = svr.predict(K_te)

            pred = pred_z * y_std + y_mean
            test_r2 = float(r2_score(te_targets, pred))
            test_mae = float(mean_absolute_error(te_targets, pred))

            if p_val == 0.00:
                diff = abs(test_r2 - r2_ref)
                if diff > max_diff_seed:
                    max_diff_seed = diff
                assert diff < 1e-10, f"Seed {seed} {mod} {var}: fixed-hp at p=0 differs by {diff:.2e} from reference ({test_r2} vs {r2_ref})!"

            seed_results.append({
                "seed": seed,
                "p": p_val,
                "model": mod,
                "variant": var,
                "r2": test_r2,
                "mae": test_mae,
                "hp_source": "p0_optimum",
            })

    elapsed = time.time() - t_seed
    return seed, seed_results, max_diff_seed, elapsed


def main():
    print("=" * 80, flush=True)
    print("STEP 0b: Task 1 Fixed-Hyperparameter Depolarizing Sweep", flush=True)
    print("=" * 80, flush=True)

    out_csv = os.path.join("results", "t5_depol_fixedhp.csv")
    completed_seeds = set()
    if os.path.exists(out_csv) and os.path.getsize(out_csv) > 0:
        try:
            df_prev = pd.read_csv(out_csv)
            if len(df_prev) > 0:
                completed_seeds = set(df_prev["seed"].unique())
                print(f"Resumption: found {len(completed_seeds)} already completed seeds in {out_csv}.", flush=True)
        except Exception:
            pass

    # 1. Load p=0.00 optimum parameters from results/t5_noise.csv
    noise_csv = os.path.join("results", "t5_noise.csv")
    df_noise = pd.read_csv(noise_csv)
    p0_df = df_noise[
        (df_noise["experiment"] == "depolarizing")
        & (df_noise["noise_level"] == 0.0)
        & (df_noise["metric"] == "r2")
    ].copy()

    p0_dict = {}
    for _, row in p0_df.iterrows():
        s = int(row["seed"])
        m = str(row["model"])
        v = str(row["variant"])
        params = json.loads(row["best_params"])
        val = float(row["value"])
        p0_dict[(s, m, v)] = (params, val)

    remaining_seeds = [s for s in SEEDS if s not in completed_seeds]
    if not remaining_seeds:
        print("All 20 seeds already completed!", flush=True)
        return

    n_workers = min(4, cpu_count())
    print(f"Executing {len(remaining_seeds)} seeds using {n_workers} workers...", flush=True)
    t0 = time.time()

    # Write header if file does not exist
    if not os.path.exists(out_csv) or os.path.getsize(out_csv) == 0:
        schema = ["seed", "p", "model", "variant", "r2", "mae", "hp_source"]
        with open(out_csv, "w", encoding="utf-8") as f:
            f.write(",".join(schema) + "\n")

    overall_max_diff = 0.0
    done_count = len(completed_seeds)

    with Pool(processes=n_workers, initializer=init_worker, initargs=(p0_dict,)) as pool:
        for seed, seed_records, diff, elapsed in pool.imap_unordered(process_seed, remaining_seeds):
            done_count += 1
            overall_max_diff = max(overall_max_diff, diff)
            print(f"  [Progress {done_count:2d}/20] Seed {seed:2d} finished in {elapsed:.1f}s (p=0 diff: {diff:.2e})", flush=True)

            # Append to CSV
            df_batch = pd.DataFrame(seed_records)
            df_batch.to_csv(out_csv, mode="a", header=False, index=False)

    print(f"\nAll 20 seeds complete in {time.time() - t0:.2f}s.", flush=True)
    print(f"Max absolute difference from p=0.00 baseline: {overall_max_diff:.2e}", flush=True)
    assert overall_max_diff < 1e-10, f"Fixed-hp p=0 baseline diff failed: {overall_max_diff:.2e}"
    print("--> Assertion PASSED: at p=0.00, fixed-hp R^2 reproduces tuned baseline to < 1e-10!", flush=True)

    df_final = pd.read_csv(out_csv)
    print(f"Verified {len(df_final)} rows in {out_csv}.", flush=True)


if __name__ == "__main__":
    main()
