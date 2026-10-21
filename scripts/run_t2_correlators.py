"""
scripts/run_t2_correlators.py
-----------------------------
Task 2: Disordered 1D TFIM correlators, n=8.
- Target T2a: <Z_0 Z_{n-1}> (tag: "contained")
- Target T2b: <Z_0 Z_1 Z_{n-2} Z_{n-1}> (tag: "not_contained")
N_train in {10, 20, 40, 80, 160}.
"""

import os
import sys
import time

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from common import (
    get_parser,
    parse_seeds,
    write_run_meta,
    make_split,
    evaluate_regression_models,
    write_csv_rows,
)


def run_t2(seeds, quick=False, out_csv=None, grid_version="grid_v2"):
    if out_csv is None:
        out_csv = os.path.join("results", "t2_correlators_gridv2.csv" if grid_version == "grid_v2" else "t2_correlators.csv")

    write_run_meta()

    n = 8
    if quick:
        n_train_list = [10, 20, 40]
    else:
        n_train_list = [10, 20, 40, 80, 160]

    print(f"=== Starting T2 Correlators Benchmark ({grid_version}, Seeds: {seeds}, N_train: {n_train_list}) ===")
    total_rows = 0
    t_start = time.time()

    for seed in seeds:
        t_seed = time.time()
        for N in n_train_list:
            # --- T2a: 2-point end-to-end correlator (contained) ---
            tr_states_a, tr_targets_a, te_states_a, te_targets_a, _ = make_split(
                task="t2", n=n, N=N, seed=seed, target_name="z0zn"
            )
            rows_a = evaluate_regression_models(
                task="T2a",
                target="z0_zn",
                tag="contained",
                n=n,
                N_train=N,
                seed=seed,
                train_states=tr_states_a,
                train_targets=tr_targets_a,
                test_states=te_states_a,
                test_targets=te_targets_a,
                grid_version=grid_version,
            )
            write_csv_rows(out_csv, rows_a)
            total_rows += len(rows_a)

            # --- T2b: 4-point correlator (not_contained) ---
            tr_states_b, tr_targets_b, te_states_b, te_targets_b, _ = make_split(
                task="t2", n=n, N=N, seed=seed, target_name="zzzz"
            )
            rows_b = evaluate_regression_models(
                task="T2b",
                target="z0_z1_zn2_zn1",
                tag="not_contained",
                n=n,
                N_train=N,
                seed=seed,
                train_states=tr_states_b,
                train_targets=tr_targets_b,
                test_states=te_states_b,
                test_targets=te_targets_b,
                grid_version=grid_version,
            )
            write_csv_rows(out_csv, rows_b)
            total_rows += len(rows_b)

        print(f"  [T2] Seed {seed:2d} completed in {time.time() - t_seed:.2f}s (logged {total_rows} rows so far)")

    total_time = time.time() - t_start
    print(f"=== T2 Benchmark complete: {total_rows} rows in {total_time:.2f}s -> {out_csv} ===")
    return total_time


if __name__ == "__main__":
    parser = get_parser(description="Run Task 2 (Correlator Prediction) Benchmark")
    args = parser.parse_args()
    seeds = parse_seeds(args)
    run_t2(seeds, quick=args.quick, out_csv=args.out)
