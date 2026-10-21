"""
scripts/diagnostics_t3_disorder.py
----------------------------------
Extract and tabulate Task 3 disordered diagnostic metrics for n in {4, 8, 14}:
- Off-diagonal variance: FQ, PQK-1 (gamma=1.0 and gamma=1.0/n), PQK-2nn (gamma=1.0 and gamma=1.0/n).
- Off-diagonal median: FQ, PQK-1, PQK-2nn (gamma=1.0 and gamma=1.0/n).
- Fraction of off-diagonal FQ entries with K_ij < 10^-3.
"""

import os
import sys
import pandas as pd
import numpy as np

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
_SRC_DIR = os.path.abspath(os.path.join(_SCRIPTS_DIR, "..", "src"))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from hamiltonians import build_tfim, ground_state

def compute_t3_disordered_diagnostics():
    t3_path = os.path.join("results", "t3_concentration_v2.csv")
    if not os.path.exists(t3_path):
        print(f"Error: {t3_path} does not exist.")
        return

    df = pd.read_csv(t3_path)
    df_disorder = df[df["tag"] == "disorder"]

    n_target_list = [4, 8, 14]
    
    print("=== Task 3 Disordered Diagnostic Metrics (Mean over 20 Seeds) ===")
    
    # 1. Off-diagonal Variance
    print("\n--- Off-Diagonal Variance ---")
    var_rows = []
    models_rules = [
        ("FQ", "none"),
        ("PQK-1", "1.0"),
        ("PQK-1", "1.0/n"),
        ("PQK-2nn", "1.0"),
        ("PQK-2nn", "1.0/n"),
    ]
    for kernel, grule in models_rules:
        row = {"kernel": kernel, "gamma_rule": grule}
        for n in n_target_list:
            sub = df_disorder[(df_disorder["kernel"] == kernel) & (df_disorder["gamma_rule"] == grule) & (df_disorder["n"] == n)]
            if not sub.empty:
                vals = sub["off_diag_var"].astype(float).values
                row[f"n={n}"] = f"{np.mean(vals):.6e}"
            else:
                row[f"n={n}"] = "N/A"
        var_rows.append(row)
    df_var = pd.DataFrame(var_rows)
    print(df_var.to_string(index=False))

    # 2. Off-diagonal Median
    print("\n--- Off-Diagonal Median ---")
    med_rows = []
    med_models_rules = [
        ("FQ", "none"),
        ("PQK-1", "1.0"),
        ("PQK-1", "1.0/n"),
        ("PQK-2nn", "1.0"),
        ("PQK-2nn", "1.0/n"),
    ]
    for kernel, grule in med_models_rules:
        row = {"kernel": kernel, "gamma_rule": grule}
        for n in n_target_list:
            sub = df_disorder[(df_disorder["kernel"] == kernel) & (df_disorder["gamma_rule"] == grule) & (df_disorder["n"] == n)]
            if not sub.empty:
                vals = sub["off_diag_median"].astype(float).values
                row[f"n={n}"] = f"{np.mean(vals):.6f}"
            else:
                row[f"n={n}"] = "N/A"
        med_rows.append(row)
    df_med = pd.DataFrame(med_rows)
    print(df_med.to_string(index=False))

    # 3. Fraction of off-diagonal FQ entries with K_ij < 10^-3
    print("\n--- Fraction of Off-Diagonal FQ Entries with K_ij < 10^-3 ---")
    frac_rows = []
    for n in n_target_list:
        fracs_per_seed = []
        for seed in range(20):
            rng = np.random.default_rng(seed * 1000 + n * 10 + 2)
            states = []
            for _ in range(30):
                couplings = rng.uniform(0.5, 1.5, size=n - 1)
                fields = rng.uniform(0.3, 2.0, size=n)
                H = build_tfim(n, g=1.0, J=1.0, boundary="open", couplings=couplings, fields=fields)
                _, psi, _ = ground_state(H, n, sector="even")
                states.append(psi)
            states = np.array(states, dtype=np.float64)
            K_fq = (states @ states.T) ** 2
            mask = ~np.eye(30, dtype=bool)
            off_diag = K_fq[mask]
            frac_lt_1e3 = np.mean(off_diag < 1e-3)
            fracs_per_seed.append(frac_lt_1e3)
        mean_frac = np.mean(fracs_per_seed)
        max_frac = np.max(fracs_per_seed)
        min_frac = np.min(fracs_per_seed)
        frac_rows.append({
            "n": n,
            "mean_frac_lt_1e3": f"{mean_frac:.6f}",
            "min_frac_lt_1e3": f"{min_frac:.6f}",
            "max_frac_lt_1e3": f"{max_frac:.6f}",
        })
    df_frac = pd.DataFrame(frac_rows)
    print(df_frac.to_string(index=False))

if __name__ == "__main__":
    compute_t3_disordered_diagnostics()
