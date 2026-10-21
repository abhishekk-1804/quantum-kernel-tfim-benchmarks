"""
scripts/run_t1_entropy.py
-------------------------
Task 1: Open-boundary disordered TFIM, n=8.
Target: half-chain entanglement entropy (tag: "not_contained").
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


def run_t1(seeds, quick=False, out_csv=None, grid_version="grid_v3"):
    if out_csv is None:
        if grid_version == "grid_v3":
            out_csv = os.path.join("results", "t1_entropy_gridv3.csv")
        elif grid_version == "grid_v2":
            out_csv = os.path.join("results", "t1_entropy_gridv2.csv")
        else:
            out_csv = os.path.join("results", "t1_entropy.csv")

    write_run_meta()

    n = 8
    if quick:
        n_train_list = [10, 20, 40]
    else:
        n_train_list = [10, 20, 40, 80, 160]

    print(f"=== Starting T1 Entropy Benchmark ({grid_version}, Seeds: {seeds}, N_train: {n_train_list}) ===")
    total_rows = 0
    t_start = time.time()

    for seed in seeds:
        t_seed = time.time()
        for N in n_train_list:
            train_states, train_targets, test_states, test_targets, meta = make_split(
                task="t1", n=n, N=N, seed=seed, target_name="entropy"
            )
            rows = evaluate_regression_models(
                task="T1",
                target="half_chain_entropy",
                tag="not_contained",
                n=n,
                N_train=N,
                seed=seed,
                train_states=train_states,
                train_targets=train_targets,
                test_states=test_states,
                test_targets=test_targets,
                grid_version=grid_version,
            )
            write_csv_rows(out_csv, rows)
            total_rows += len(rows)

        print(f"  [T1] Seed {seed:2d} completed in {time.time() - t_seed:.2f}s (logged {total_rows} rows so far)")

    total_time = time.time() - t_start
    print(f"=== T1 Benchmark complete: {total_rows} rows in {total_time:.2f}s -> {out_csv} ===")
    return total_time


if __name__ == "__main__":
    parser = get_parser(description="Run Task 1 (Entropy Prediction) Benchmark")
    args = parser.parse_args()
    seeds = parse_seeds(args)
    grid_ver = args.grid if hasattr(args, "grid") and args.grid else "grid_v3"
    run_t1(seeds, quick=args.quick, out_csv=args.out, grid_version=grid_ver)
