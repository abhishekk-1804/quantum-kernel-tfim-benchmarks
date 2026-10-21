"""
scripts/run_t3_concentration_v2.py
----------------------------------
Task 3 (v2): Concentration scaling of quantum kernels.
Includes:
- Samplings: "logunif", "narrow", and new "disorder" (open TFIM with random J_i ~ U[0.5, 1.5], g_i ~ U[0.3, 2.0])
- Kernels:
  * FQ: gamma_rule="none", with off_diag_mean, off_diag_var, off_diag_median, off_diag_log10_mean
  * PQK-1: gamma_rule="1.0" (fixed) and c/n (c in {0.1, 0.3, 1.0, 3.0, 10.0})
  * PQK-2nn: gamma_rule="1.0" (fixed) and c/n (c in {0.1, 0.3, 1.0, 3.0, 10.0})
- Uniform samplings also record frac_cross_pairs (fraction of pairs with g on opposite sides of 1.0).
- n in {4, 6, 8, 10, 12, 14}, 30 states per seed, 20 seeds.
- Precomputes 1-local and 2-local Frobenius distances for optimal execution speed.
"""

import os
import sys
import time
import numpy as np

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
_SRC_DIR = os.path.abspath(os.path.join(_SCRIPTS_DIR, "..", "src"))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from common import get_parser, parse_seeds, write_run_meta, C_FACTORS
from hamiltonians import build_tfim, ground_state
from kernels import one_rdm, two_rdm


def run_t3_v2(seeds, quick=False, out_csv=None):
    if out_csv is None:
        out_csv = os.path.join("results", "t3_concentration_v2.csv")

    write_run_meta()

    if quick:
        n_list = [4, 6, 8, 10]
        n_states = 15
    else:
        n_list = [4, 6, 8, 10, 12, 14]
        n_states = 30

    samplings = ["logunif", "narrow", "disorder"]

    os.makedirs(os.path.dirname(os.path.abspath(out_csv)), exist_ok=True)
    write_header = not os.path.exists(out_csv) or os.path.getsize(out_csv) == 0
    fieldnames = [
        "task", "tag", "n", "hilbert_dim", "seed",
        "kernel", "gamma_rule",
        "off_diag_mean", "off_diag_var", "off_diag_median", "off_diag_log10_mean",
        "frac_cross_pairs", "gs_seconds"
    ]

    print(f"=== Starting T3 (v2) Concentration Benchmark (n: {n_list}, Seeds: {seeds}, States: {n_states}) ===")
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
                    
                    if sampling_tag == "logunif":
                        rng = np.random.default_rng(seed * 1000 + n * 10 + 0)
                        g_vals = 10.0 ** rng.uniform(-1.0, 1.0, size=n_states)
                        n_pairs = n_states * (n_states - 1) // 2
                        cross_count = sum(
                            1 for i in range(n_states) for j in range(i + 1, n_states)
                            if (g_vals[i] - 1.0) * (g_vals[j] - 1.0) < 0
                        )
                        frac_cross_str = f"{cross_count / float(n_pairs):.6f}"
                    elif sampling_tag == "narrow":
                        rng = np.random.default_rng(seed * 1000 + n * 10 + 1)
                        g_vals = rng.uniform(0.7, 1.4, size=n_states)
                        n_pairs = n_states * (n_states - 1) // 2
                        cross_count = sum(
                            1 for i in range(n_states) for j in range(i + 1, n_states)
                            if (g_vals[i] - 1.0) * (g_vals[j] - 1.0) < 0
                        )
                        frac_cross_str = f"{cross_count / float(n_pairs):.6f}"
                    else:  # disorder
                        rng = np.random.default_rng(seed * 1000 + n * 10 + 2)
                        g_vals = None
                        frac_cross_str = ""

                    # Solve ground states
                    states = []
                    t_gs_start = time.time()
                    for idx in range(n_states):
                        if sampling_tag in ("logunif", "narrow"):
                            g = g_vals[idx]
                            H = build_tfim(n, g=g, J=1.0, boundary="open")
                        else:
                            couplings = rng.uniform(0.5, 1.5, size=n - 1)
                            fields = rng.uniform(0.3, 2.0, size=n)
                            H = build_tfim(n, g=1.0, J=1.0, boundary="open", couplings=couplings, fields=fields)
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
                        od_median = float(np.median(off_diag))
                        if k_name == "FQ":
                            # Safe log10 with 1e-300 clamp
                            od_log10 = float(np.mean(np.log10(np.maximum(off_diag, 1e-300))))
                            od_log10_str = f"{od_log10:.6f}"
                        else:
                            od_log10_str = ""

                        row_dict = {
                            "task": "T3",
                            "tag": sampling_tag,
                            "n": str(n),
                            "hilbert_dim": str(hilbert_dim),
                            "seed": str(seed),
                            "kernel": k_name,
                            "gamma_rule": g_rule,
                            "off_diag_mean": f"{od_mean:.6f}",
                            "off_diag_var": f"{od_var:.6e}",
                            "off_diag_median": f"{od_median:.6f}",
                            "off_diag_log10_mean": od_log10_str,
                            "frac_cross_pairs": frac_cross_str,
                            "gs_seconds": f"{gs_seconds_per_state:.6f}",
                        }
                        line = [str(row_dict[col]) for col in fieldnames]
                        f.write(",".join(line) + "\n")
                        total_rows += 1

                    # 1. Fidelity Gram matrix: K_ij = (psi_i @ psi_j)^2
                    K_fq = (states @ states.T) ** 2
                    log_kernel_record("FQ", "none", K_fq)

                    # 2. PQK-1: Precompute 1-local Frobenius distance matrix
                    rdms_1local = [[one_rdm(psi, n, k) for k in range(n)] for psi in states]
                    D1 = np.zeros((n_states, n_states), dtype=float)
                    for i in range(n_states):
                        for j in range(i + 1, n_states):
                            d1_val = sum(np.sum((rdms_1local[i][k] - rdms_1local[j][k]) ** 2) for k in range(n))
                            D1[i, j] = d1_val
                            D1[j, i] = d1_val

                    # PQK-1 gamma = 1.0 (fixed)
                    log_kernel_record("PQK-1", "1.0", np.exp(-1.0 * D1))
                    # PQK-1 gamma = c / n
                    for c_val in C_FACTORS:
                        gamma = c_val / float(n)
                        log_kernel_record("PQK-1", f"{c_val}/n", np.exp(-gamma * D1))

                    # 3. PQK-2nn: Precompute 2-local NN Frobenius distance matrix
                    pairs_nn = [(i, i + 1) for i in range(n - 1)]
                    rdms_2local = [[two_rdm(psi, n, p[0], p[1]) for p in pairs_nn] for psi in states]
                    D2 = np.zeros((n_states, n_states), dtype=float)
                    for i in range(n_states):
                        for j in range(i + 1, n_states):
                            d2_val = sum(np.sum((rdms_2local[i][k] - rdms_2local[j][k]) ** 2) for k in range(len(pairs_nn)))
                            D2[i, j] = d2_val
                            D2[j, i] = d2_val

                    # PQK-2nn gamma = 1.0 (fixed)
                    log_kernel_record("PQK-2nn", "1.0", np.exp(-1.0 * D2))
                    # PQK-2nn gamma = c / n
                    for c_val in C_FACTORS:
                        gamma = c_val / float(n)
                        log_kernel_record("PQK-2nn", f"{c_val}/n", np.exp(-gamma * D2))

            f.flush()
            print(f"  [T3 v2] Seed {seed:2d} completed in {time.time() - t_seed:.2f}s (logged {total_rows} rows so far)")

    total_time = time.time() - t_start
    print(f"=== T3 v2 Benchmark complete: {total_rows} rows in {total_time:.2f}s -> {out_csv} ===")
    return total_time


if __name__ == "__main__":
    parser = get_parser(description="Run Task 3 v2 (Concentration Scaling) Benchmark")
    args = parser.parse_args()
    seeds = parse_seeds(args)
    run_t3_v2(seeds, quick=args.quick, out_csv=args.out)
