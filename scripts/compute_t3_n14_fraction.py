"""
scripts/compute_t3_n14_fraction.py
Computes results/t3_n14_fraction.csv:
Evaluates n=14 disordered TFIM ensemble across 20 seeds (30 states per seed),
using the exact seed/generator protocol as T3 (v2).
Records fraction of off-diagonal entries < 1e-3 and minimum entry.
Schema: kernel, gamma_rule, n, n_pairs, n_below, fraction, min_entry
"""
import os
import sys
import time
from multiprocessing import Pool, cpu_count
import numpy as np
import pandas as pd

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC = os.path.join(_PROJECT_ROOT, "src")
for p in [_PROJECT_ROOT, _SRC]:
    if p not in sys.path:
        sys.path.insert(0, p)

from hamiltonians import build_tfim, ground_state
from kernels import one_rdm, two_rdm


def process_seed(seed):
    n = 14
    n_states = 30
    rng = np.random.default_rng(seed * 1000 + n * 10 + 2)

    # 1. Generate 30 disordered TFIM ground states
    states = []
    for _ in range(n_states):
        couplings = rng.uniform(0.5, 1.5, size=n - 1)
        fields = rng.uniform(0.3, 2.0, size=n)
        H = build_tfim(n, g=1.0, J=1.0, boundary="open", couplings=couplings, fields=fields)
        _, psi, _ = ground_state(H, n, sector="even")
        states.append(psi)
    states = np.array(states, dtype=np.float64)

    triu_idx = np.triu_indices(n_states, k=1)
    n_pairs = len(triu_idx[0])

    # 2. FQ Gram
    K_fq = (states @ states.T) ** 2
    fq_off = K_fq[triu_idx]

    # 3. PQK-1: 1-local Frobenius distance matrix
    rdms_1local = [[one_rdm(psi, n, k) for k in range(n)] for psi in states]
    D1 = np.zeros((n_states, n_states), dtype=float)
    for i in range(n_states):
        for j in range(i + 1, n_states):
            d1_val = sum(np.sum((rdms_1local[i][k] - rdms_1local[j][k]) ** 2) for k in range(n))
            D1[i, j] = d1_val
            D1[j, i] = d1_val

    pqk1_1_off = np.exp(-1.0 * D1)[triu_idx]
    pqk1_invn_off = np.exp(-(1.0 / n) * D1)[triu_idx]

    # 4. PQK-2nn: 2-local NN Frobenius distance matrix
    pairs_nn = [(i, i + 1) for i in range(n - 1)]
    rdms_2local = [[two_rdm(psi, n, p[0], p[1]) for p in pairs_nn] for psi in states]
    D2 = np.zeros((n_states, n_states), dtype=float)
    for i in range(n_states):
        for j in range(i + 1, n_states):
            d2_val = sum(np.sum((rdms_2local[i][k] - rdms_2local[j][k]) ** 2) for k in range(len(pairs_nn)))
            D2[i, j] = d2_val
            D2[j, i] = d2_val

    pqk2_1_off = np.exp(-1.0 * D2)[triu_idx]
    pqk2_invn_off = np.exp(-(1.0 / n) * D2)[triu_idx]

    return {
        "n_pairs": n_pairs,
        "FQ_none": fq_off,
        "PQK-1_1.0": pqk1_1_off,
        "PQK-1_1.0/n": pqk1_invn_off,
        "PQK-2nn_1.0": pqk2_1_off,
        "PQK-2nn_1.0/n": pqk2_invn_off,
    }


def main():
    print("=" * 80)
    print("TASK 0a: Evaluate n=14 Disordered TFIM Kernel Entries Across 20 Seeds")
    print("=" * 80)

    n_workers = min(10, cpu_count())
    print(f"Spawning {n_workers} worker processes...")
    t0 = time.time()

    with Pool(processes=n_workers) as pool:
        seed_results = pool.map(process_seed, range(20))

    print(f"Computed all 20 seeds in {time.time() - t0:.2f}s.")

    kernels_to_report = [
        ("FQ", "none", "FQ_none"),
        ("PQK-1", "1.0", "PQK-1_1.0"),
        ("PQK-1", "1.0/n", "PQK-1_1.0/n"),
        ("PQK-2nn", "1.0", "PQK-2nn_1.0"),
        ("PQK-2nn", "1.0/n", "PQK-2nn_1.0/n"),
    ]

    records = []
    for k_name, g_rule, key in kernels_to_report:
        all_vals = np.concatenate([res[key] for res in seed_results])
        n_pairs = len(all_vals)
        n_below = int(np.sum(all_vals < 1e-3))
        fraction = float(n_below / n_pairs)
        min_entry = float(np.min(all_vals))

        records.append({
            "kernel": k_name,
            "gamma_rule": g_rule,
            "n": 14,
            "n_pairs": n_pairs,
            "n_below": n_below,
            "fraction": fraction,
            "min_entry": min_entry,
        })
        print(f"  {k_name:<10} (gamma={g_rule:<6}): n_pairs={n_pairs}, n_below={n_below}, fraction={fraction:.6f}, min_entry={min_entry:.6f}")

    df_out = pd.DataFrame(records)
    out_csv = os.path.join("results", "t3_n14_fraction.csv")
    df_out.to_csv(out_csv, index=False)
    print(f"\nWrote {len(df_out)} rows to {out_csv}.")


if __name__ == "__main__":
    main()
