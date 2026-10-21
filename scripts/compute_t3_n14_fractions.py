"""
scripts/compute_t3_n14_fractions.py
Compute fraction of off-diagonal kernel entries < 1e-3 at n=14 in the disorder ensemble.
"""
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SRC = os.path.join(_ROOT, "src")
for p in [_ROOT, _SRC]:
    if p not in sys.path:
        sys.path.insert(0, p)

import numpy as np
from hamiltonians import build_tfim, ground_state
from kernels import fidelity_gram, pqk_gram, pqk_gram_2local, one_rdm

def main():
    n = 14
    n_states = 30
    seeds = range(20)

    kernel_keys = [
        ("FQ", "none"),
        ("PQK-1", "1.0"),
        ("PQK-1", "0.1/n"),
        ("PQK-1", "0.3/n"),
        ("PQK-1", "1.0/n"),
        ("PQK-1", "3.0/n"),
        ("PQK-1", "10.0/n"),
        ("PQK-2nn", "1.0"),
        ("PQK-2nn", "0.1/n"),
        ("PQK-2nn", "0.3/n"),
        ("PQK-2nn", "1.0/n"),
        ("PQK-2nn", "3.0/n"),
        ("PQK-2nn", "10.0/n"),
    ]

    total_off_diag = 0
    small_counts = {k: 0 for k in kernel_keys}
    min_vals = {k: float("inf") for k in kernel_keys}

    triu_idx = np.triu_indices(n_states, k=1)

    print(f"Starting n={n} computation over {len(seeds)} seeds...")
    for seed in seeds:
        rng = np.random.default_rng(seed)
        states = []
        for _ in range(n_states):
            couplings = rng.uniform(0.5, 1.5, size=n - 1)
            fields = rng.uniform(0.3, 2.0, size=n)
            H = build_tfim(n, g=1.0, J=1.0, boundary="open", couplings=couplings, fields=fields)
            _, psi, _ = ground_state(H, n, sector="even")
            states.append(psi)

        states_arr = np.array(states, dtype=np.float64)
        rdm1_list = [[one_rdm(psi, n, q) for q in range(n)] for psi in states_arr]

        # FQ
        K_fq = fidelity_gram(states_arr)
        vals_fq = K_fq[triu_idx]
        small_counts[("FQ", "none")] += int(np.sum(vals_fq < 1e-3))
        min_vals[("FQ", "none")] = min(min_vals[("FQ", "none")], float(np.min(vals_fq)))

        # PQK-1
        for rule in ["1.0", "0.1/n", "0.3/n", "1.0/n", "3.0/n", "10.0/n"]:
            gamma = 1.0 if rule == "1.0" else float(rule.split("/")[0]) / n
            K = pqk_gram(rdm1_list, gamma=gamma)
            vals = K[triu_idx]
            small_counts[("PQK-1", rule)] += int(np.sum(vals < 1e-3))
            min_vals[("PQK-1", rule)] = min(min_vals[("PQK-1", rule)], float(np.min(vals)))

        # PQK-2nn
        for rule in ["1.0", "0.1/n", "0.3/n", "1.0/n", "3.0/n", "10.0/n"]:
            gamma = 1.0 if rule == "1.0" else float(rule.split("/")[0]) / n
            K = pqk_gram_2local(states_arr, n=n, pairs="nn", gamma=gamma)
            vals = K[triu_idx]
            small_counts[("PQK-2nn", rule)] += int(np.sum(vals < 1e-3))
            min_vals[("PQK-2nn", rule)] = min(min_vals[("PQK-2nn", rule)], float(np.min(vals)))

        total_off_diag += len(triu_idx[0])
        print(f"  Seed {seed:2d} done.")

    print("\nFraction of off-diagonal entries < 1e-3 at n=14 (Disordered TFIM, 20 seeds):")
    print(f"{'Kernel':<12} {'Gamma Rule':<12} {'Small Pairs':<12} {'Total Pairs':<12} {'Fraction < 1e-3':<16} {'Min Entry':<12}")
    print("-" * 80)
    for k in kernel_keys:
        cnt = small_counts[k]
        frac = cnt / total_off_diag
        m_val = min_vals[k]
        print(f"{k[0]:<12} {k[1]:<12} {cnt:<12} {total_off_diag:<12} {frac:<16.6f} {m_val:<12.6f}")

if __name__ == "__main__":
    main()
