"""
scripts/reproduce_quick.py
Fast smoke test for quick reproduction: runs 3 seeds of Task 1 on small N.
Finishes in < 1 minute.
"""
import sys
import os
import time
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.svm import SVR
from sklearn.metrics import r2_score

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC = os.path.join(_PROJECT_ROOT, "src")
_SCRIPTS = os.path.join(_PROJECT_ROOT, "scripts")
for p in [_PROJECT_ROOT, _SRC, _SCRIPTS]:
    if p not in sys.path:
        sys.path.insert(0, p)

from common import make_split, SEEDS
from kernels import classical_features

print("=" * 60)
print("QUICK REPRODUCTION SMOKE TEST (3 seeds, Task 1, N=40)")
print("=" * 60)

t0 = time.time()
test_seeds = SEEDS[:3]
results = []

for s in test_seeds:
    t_start = time.time()
    tr_states, tr_targets, te_states, te_targets, _ = make_split("t1", n=8, N=40, seed=s)
    all_states = np.vstack([tr_states, te_states])

    # Z-score targets
    y_mean = float(np.mean(tr_targets))
    y_std = float(np.std(tr_targets))
    y_tr_z = (tr_targets - y_mean) / y_std

    # Features
    X_pqk1 = np.array([classical_features(psi, 8, mode="1pt_X") for psi in all_states])
    gamma = 1.0 / 16.0
    K = np.exp(-gamma * cdist(X_pqk1, X_pqk1, "sqeuclidean"))
    K_tr = K[:40, :40]
    K_te = K[40:, :40]

    svr = SVR(kernel="precomputed", C=10.0, epsilon=0.01)
    svr.fit(K_tr, y_tr_z)
    pred_z = svr.predict(K_te)
    pred = pred_z * y_std + y_mean
    r2 = r2_score(te_targets, pred)
    print(f"  Seed {s} PQK-1 test R^2: {r2:.4f} ({time.time()-t_start:.2f}s)")
    results.append({"seed": s, "model": "PQK-1", "r2": r2})

print("-" * 60)
print(f"Quick smoke test completed in {time.time()-t0:.2f}s.")
print("Average PQK-1 R^2 over 3 seeds:", np.mean([r["r2"] for r in results]))
print("=" * 60)
