"""
scripts/run_t3_concentration.py
-------------------------------
Task 3: Concentration scaling of quantum kernels.
UNIFORM open-boundary TFIM, J = 1.
n in {4, 6, 8, 10, 12, 14}, 30 states per seed, 20 seeds.
Two g-samplings:
- "logunif": g = 10**U[-1, 1]
- "narrow":  g ~ U[0.7, 1.4]
Columns: task, tag, n, hilbert_dim, seed, kernel, gamma_rule, off_diag_mean, off_diag_var, gs_seconds
"""

import os
import sys
import time
import numpy as np

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from common import get_parser, parse_seeds, write_run_meta, C_FACTORS
from hamiltonians import build_tfim, ground_state
from kernels import one_rdm, pqk_gram, pqk_gram_2local, off_diagonal_variance


def run_t3(seeds, quick=False, out_csv=None):
    if out_csv is None:
        out_csv = os.path.join("results", "t3_concentration.csv")

    write_run_meta()

    if quick:
        n_list = [4, 6, 8, 10]
        n_states = 15
    else:
        n_list = [4, 6, 8, 10, 12, 14]
        n_states = 30

    samplings = ["logunif", "narrow"]

    os.makedirs(os.path.dirname(os.path.abspath(out_csv)), exist_ok=True)
    write_header = not os.path.exists(out_csv) or os.path.getsize(out_csv) == 0
    fieldnames = [
        "task", "tag", "n", "hilbert_dim", "seed",
        "kernel", "gamma_rule", "off_diag_mean", "off_diag_var", "gs_seconds"
    ]

    print(f"=== Starting T3 Concentration Benchmark (n: {n_list}, Seeds: {seeds}, States: {n_states}) ===")
    total_rows = 0
    t_start = time.time()

    with open(out_csv, "a", encoding="utf-8") as f:
        if write_header:
            f.write(",".join(fieldnames) + "\n")
            f.flush()

        for seed in seeds:
            t_seed = time.time()
            for sampling_tag in samplings:
                for n in n_list:
                    hilbert_dim = 2 ** n
                    rng = np.random.default_rng(seed * 1000 + n * 10 + (0 if sampling_tag == "logunif" else 1))

                    if sampling_tag == "logunif":
                        # g = 10**U[-1, 1] -> log-uniform in [0.1, 10.0]
                        g_vals = 10.0 ** rng.uniform(-1.0, 1.0, size=n_states)
                    else:
                        # narrow: g ~ U[0.7, 1.4]
                        g_vals = rng.uniform(0.7, 1.4, size=n_states)

                    # Solve ground states and record wall-clock time
                    states = []
                    t_gs_start = time.time()
                    for g in g_vals:
                        H = build_tfim(n, g=g, J=1.0, boundary="open")
                        _, psi, _ = ground_state(H, n, sector="even")
                        states.append(psi)
                    gs_time_total = time.time() - t_gs_start
                    gs_seconds_per_state = gs_time_total / n_states
                    states = np.array(states, dtype=np.float64)

                    # Helper to log a row
                    def log_kernel_record(k_name, g_rule, K):
                        nonlocal total_rows
                        mask = ~np.eye(n_states, dtype=bool)
                        off_diag = K[mask]
                        od_mean = float(np.mean(off_diag))
                        od_var = float(np.var(off_diag, ddof=1)) if len(off_diag) > 1 else 0.0

                        row_dict = {
                            "task": "T3",
                            "tag": sampling_tag,
                            "n": n,
                            "hilbert_dim": hilbert_dim,
                            "seed": seed,
                            "kernel": k_name,
                            "gamma_rule": g_rule,
                            "off_diag_mean": od_mean,
                            "off_diag_var": od_var,
                            "gs_seconds": gs_seconds_per_state,
                        }
                        line = [str(row_dict[col]) for col in fieldnames]
                        f.write(",".join(line) + "\n")
                        total_rows += 1

                    # 1. Fidelity Gram matrix: K_ij = (psi_i @ psi_j)^2
                    K_fq = (states @ states.T) ** 2
                    log_kernel_record("FQ", "none", K_fq)

                    # 2. PQK-1: extract 1-RDMs
                    rdms_1local = [[one_rdm(psi, n, k) for k in range(n)] for psi in states]
                    # Fixed gamma = 1.0
                    K_pqk1_g1 = pqk_gram(rdms_1local, gamma=1.0)
                    log_kernel_record("PQK-1", "1.0", K_pqk1_g1)
                    # Grid gamma = c / n
                    for c_val in C_FACTORS:
                        gamma = c_val / float(n)
                        K_pqk1_c = pqk_gram(rdms_1local, gamma=gamma)
                        log_kernel_record("PQK-1", f"{c_val}/n", K_pqk1_c)

                    # 3. PQK-2nn: nearest-neighbour 2-local PQK
                    for c_val in C_FACTORS:
                        gamma = c_val / float(n)
                        K_pqk2_c = pqk_gram_2local(states, n, pairs="nn", gamma=gamma)
                        log_kernel_record("PQK-2nn", f"{c_val}/n", K_pqk2_c)

            f.flush()
            print(f"  [T3] Seed {seed:2d} complete in {time.time() - t_seed:.2f}s (logged {total_rows} rows)")

    total_time = time.time() - t_start
    print(f"=== T3 Benchmark complete: {total_rows} rows in {total_time:.2f}s -> {out_csv} ===")
    return total_time


if __name__ == "__main__":
    parser = get_parser(description="Run Task 3 (Concentration Scaling) Benchmark")
    args = parser.parse_args()
    seeds = parse_seeds(args)
    run_t3(seeds, quick=args.quick, out_csv=args.out)
