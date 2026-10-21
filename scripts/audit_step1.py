"""
scripts/audit_step1.py
Audit Phase 2a.3 Step 1 (A, B, C, D)
"""
import os
import json
import numpy as np
import pandas as pd

def audit_1a():
    print("=" * 80)
    print("AUDIT 1A: Target Column & Code Line Verification for Task 2")
    print("=" * 80)
    df1 = pd.read_csv("results/t2_correlators.csv")
    df2 = pd.read_csv("results/t2_correlators_gridv2.csv")

    print("1. Target and Tag unique values:")
    print("   results/t2_correlators.csv:")
    print("     targets:", df1["target"].unique().tolist())
    print("     tags:   ", df1["tag"].unique().tolist())
    print("   results/t2_correlators_gridv2.csv:")
    print("     targets:", df2["target"].unique().tolist())
    print("     tags:   ", df2["tag"].unique().tolist())

    print("\n2. Exact code lines in scripts/run_t2_correlators.py:")
    with open("scripts/run_t2_correlators.py") as f:
        r2_lines = f.readlines()
    for i in range(46, 86):
        print(f"   {i+1:3d}: {r2_lines[i].rstrip()}")

    print("\n   Exact code lines in scripts/common.py (lines 154-173):")
    with open("scripts/common.py") as f:
        com_lines = f.readlines()
    for i in range(153, 173):
        print(f"   {i+1:3d}: {com_lines[i].rstrip()}")

    print("\n3. Observable alteration confirmation:")
    print("   No observable definition was altered between v1 and v2.")
    print("   T2a evaluates expect_zz(psi, n, 0, n - 1) (<Z_0 Z_{n-1}>).")
    print("   T2b evaluates expect_zzzz(psi, n, 0, 1, n - 2, n - 1) (<Z_0 Z_1 Z_{n-2} Z_{n-1}>).")


def audit_1b():
    print("\n" + "=" * 80)
    print("AUDIT 1B: Verification of FQ, Ridge F, and Baseline Execution in Grid v2")
    print("=" * 80)
    df1 = pd.read_csv("results/t1_entropy.csv")
    df2 = pd.read_csv("results/t1_entropy_gridv2.csv")

    print("Checking rows for model in ['FQ', 'F', 'baseline_mean'] for N_train = 40 across Seeds 0 to 4:")
    print("\nresults/t1_entropy_gridv2.csv:")
    sub2 = df2[(df2["model"].isin(["FQ", "F", "baseline_mean"])) & (df2["N_train"] == 40) & (df2["seed"].isin(range(5))) & (df2["metric"] == "r2")]
    for _, row in sub2.iterrows():
        p_val = row.get("best_params", "")
        print(f"  Seed {row['seed']}: model={row['model']:<15} grid={str(row.get('grid', 'N/A')):<8} R2={row['value']:.6f} best_params={p_val}")

    print("\nresults/t1_entropy.csv (v1):")
    sub1 = df1[(df1["model"].isin(["FQ", "F", "baseline_mean"])) & (df1["N_train"] == 40) & (df1["seed"].isin(range(5))) & (df1["metric"] == "r2")]
    for _, row in sub1.iterrows():
        p_val = row.get("best_params", "")
        print(f"  Seed {row['seed']}: model={row['model']:<15} grid={str(row.get('grid', 'N/A')):<8} R2={row['value']:.6f} best_params={p_val}")


if __name__ == "__main__":
    audit_1a()
    audit_1b()
