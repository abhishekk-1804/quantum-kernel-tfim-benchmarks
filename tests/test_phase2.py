"""
tests/test_phase2.py
--------------------
Unit tests for Phase 2a:
- expect_zzzz: product state |0000...> gives 1.0, and matches dense matrix at n=6 to 1e-10.
- Shared-test-set property: test set is fixed per (task, seed) and training sets are nested.
- Equivalence: PQK-1 vs E_X predictions match within 1e-6 with gamma_E = gamma_PQK / 2.
- Custom pairs in pqk_gram_2local and classical_features for 2D frustrated lattice.
"""

import sys
import os
import hashlib
import numpy as np
import scipy.linalg
import pytest

_SRC = os.path.join(os.path.dirname(__file__), "..", "src")
_SCRIPTS = os.path.join(os.path.dirname(__file__), "..", "scripts")
for path in [_SRC, _SCRIPTS]:
    if path not in sys.path:
        sys.path.insert(0, path)

from hamiltonians import (
    build_tfim,
    build_frustrated_2d,
    ground_state,
    expect_x,
    expect_zz,
    expect_zzzz,
    _single_site_op,
    _Z,
)
from kernels import (
    one_rdm,
    two_rdm,
    pqk_gram,
    pqk_gram_2local,
    classical_features,
)
from common import make_split
from sklearn.svm import SVR
from sklearn.metrics.pairwise import rbf_kernel


class TestExpectZZZZ:
    """Tests for expect_zzzz observable."""

    def test_product_state_gives_one(self):
        """Product state |0000...0> must give exactly 1.0 for any 4 sites."""
        n = 6
        psi = np.zeros(2 ** n)
        psi[0] = 1.0  # all spins up (eigenvalue +1 under Z)

        val = expect_zzzz(psi, n, 0, 1, 2, 3)
        assert abs(val - 1.0) < 1e-14, f"Expected 1.0, got {val}"

        val2 = expect_zzzz(psi, n, 0, 2, 4, 5)
        assert abs(val2 - 1.0) < 1e-14

    def test_matches_dense_matrix_n6(self):
        """At n=6, expect_zzzz must match dense operator expectation to 1e-10."""
        n = 6
        H = build_tfim(n, g=1.0, J=1.0, boundary="open")
        _, psi, _ = ground_state(H, n, sector="even")

        # Dense operator Z_0 Z_1 Z_4 Z_5
        Z0 = _single_site_op(_Z, 0, n)
        Z1 = _single_site_op(_Z, 1, n)
        Z4 = _single_site_op(_Z, 4, n)
        Z5 = _single_site_op(_Z, 5, n)
        ZZZZ_dense = (Z0 @ Z1 @ Z4 @ Z5).toarray()

        dense_val = float(np.real(psi.conj() @ ZZZZ_dense @ psi))
        fast_val = expect_zzzz(psi, n, 0, 1, 4, 5)

        diff = abs(dense_val - fast_val)
        assert diff < 1e-10, f"Dense/fast mismatch: {dense_val} vs {fast_val}, diff={diff:.3e}"


class TestSharedTestSetAndNesting:
    """Tests verifying make_split guarantees."""

    def test_shared_test_set_across_N(self):
        """Test set must be identical for different N on the same (task, seed)."""
        seed = 42
        n = 8
        _, _, te_states_10, te_targets_10, meta_10 = make_split("t1", n=n, N=10, seed=seed)
        _, _, te_states_40, te_targets_40, meta_40 = make_split("t1", n=n, N=40, seed=seed)
        _, _, te_states_160, te_targets_160, meta_160 = make_split("t1", n=n, N=160, seed=seed)

        assert len(te_states_10) == 200
        assert np.array_equal(te_states_10, te_states_40)
        assert np.array_equal(te_states_10, te_states_160)
        assert np.array_equal(te_targets_10, te_targets_40)
        assert meta_10["test_indices"] == meta_40["test_indices"]

    def test_nested_training_sets(self):
        """Training sets must be nested: first N of fixed per-seed ordering."""
        seed = 7
        n = 8
        tr_10, _, _, _, _ = make_split("t1", n=n, N=10, seed=seed)
        tr_20, _, _, _, _ = make_split("t1", n=n, N=20, seed=seed)
        tr_40, _, _, _, _ = make_split("t1", n=n, N=40, seed=seed)

        assert np.array_equal(tr_20[:10], tr_10)
        assert np.array_equal(tr_40[:20], tr_20)

    def test_test_set_hash_consistency(self):
        """Hash of test set states is deterministic and constant."""
        n = 8
        hashes = []
        for _ in range(2):
            _, _, te_states, _, _ = make_split("t1", n=n, N=20, seed=3)
            h = hashlib.sha256(te_states.tobytes()).hexdigest()
            hashes.append(h)
        assert hashes[0] == hashes[1]


class TestPqk1EqualsExEquivalence:
    """Verify PQK-1 vs E_X predictions match within 1e-6 with gamma_E = gamma_PQK / 2."""

    def test_pqk1_vs_ex_predictions(self):
        n = 4
        g_vals = [0.4, 0.8, 1.2, 1.6, 2.0, 2.4]
        psis = [ground_state(build_tfim(n, g=g), n, sector="even")[1] for g in g_vals]
        y = np.array([0.1, 0.5, 0.9, 1.3, 1.7, 2.1])

        train_psis, test_psis = psis[:4], psis[4:]
        y_train = y[:4]

        gamma_pqk = 1.0
        rdms_train = [[one_rdm(p, n, k) for k in range(n)] for p in train_psis]
        rdms_test = [[one_rdm(p, n, k) for k in range(n)] for p in test_psis]

        K_train_pqk = pqk_gram(rdms_train, gamma=gamma_pqk)
        K_test_pqk = np.zeros((len(test_psis), len(train_psis)))
        for i in range(len(test_psis)):
            for j in range(len(train_psis)):
                d2 = 0.0
                for k in range(n):
                    diff = rdms_test[i][k] - rdms_train[j][k]
                    d2 += float(np.real(np.trace(diff.conj().T @ diff)))
                K_test_pqk[i, j] = np.exp(-gamma_pqk * d2)

        svr_pqk = SVR(kernel="precomputed", C=10.0, epsilon=0.1)
        svr_pqk.fit(K_train_pqk, y_train)
        pred_pqk = svr_pqk.predict(K_test_pqk)

        # E_X with gamma_E = gamma_pqk / 2
        X_train = np.array([expect_x(p, n) for p in train_psis])
        X_test = np.array([expect_x(p, n) for p in test_psis])
        gamma_E = gamma_pqk / 2.0

        svr_ex = SVR(kernel="rbf", C=10.0, gamma=gamma_E, epsilon=0.1)
        svr_ex.fit(X_train, y_train)
        pred_ex = svr_ex.predict(X_test)

        diff = float(np.max(np.abs(pred_pqk - pred_ex)))
        assert diff < 1e-6, f"PQK-1 != E_X: diff = {diff:.3e}"

    def test_prediction_level_identity_make_split(self):
        """Verify on T1 split that SVR(precomputed, PQK-1(gamma)) == SVR(rbf, E_X(gamma/2))."""
        n = 8
        tr_states, tr_y, te_states, te_y, _ = make_split("t1", n=n, N=20, seed=0)
        gamma = 1.0
        gamma_rbf = gamma / 2.0
        C = 10.0

        # Precomputed PQK-1
        rdms_train = [[one_rdm(p, n, k) for k in range(n)] for p in tr_states]
        rdms_test = [[one_rdm(p, n, k) for k in range(n)] for p in te_states]
        K_tr = pqk_gram(rdms_train, gamma=gamma)
        
        K_te = np.zeros((len(te_states), len(tr_states)))
        for i in range(len(te_states)):
            for j in range(len(tr_states)):
                d2 = sum(float(np.real(np.trace((rdms_test[i][k] - rdms_train[j][k]).conj().T @ (rdms_test[i][k] - rdms_train[j][k])))) for k in range(n))
                K_te[i, j] = np.exp(-gamma * d2)

        svr_pqk = SVR(kernel="precomputed", C=C, epsilon=0.1)
        svr_pqk.fit(K_tr, tr_y)
        pred_pqk = svr_pqk.predict(K_te)

        # RBF on <X> features
        X_tr = np.array([expect_x(p, n) for p in tr_states])
        X_te = np.array([expect_x(p, n) for p in te_states])
        svr_ex = SVR(kernel="rbf", C=C, gamma=gamma_rbf, epsilon=0.1)
        svr_ex.fit(X_tr, tr_y)
        pred_ex = svr_ex.predict(X_te)

        max_diff = float(np.max(np.abs(pred_pqk - pred_ex)))
        assert max_diff < 1e-6, f"Mismatch: {max_diff:.4e}"


class TestCustomPairsSupport:
    """Verify custom pairs support for 2D lattices."""

    def test_custom_pairs_pqk2_and_features(self):
        H, nn_bonds, _ = build_frustrated_2d(rows=2, cols=4, g=1.0)
        _, psi, _ = ground_state(H, 8, sector="even")

        # Custom pairs in classical_features
        f = classical_features(psi, 8, mode="2pt_pauli_nn", pairs=nn_bonds)
        assert len(f) == 5 * len(nn_bonds) == 50

        # Custom pairs in pqk_gram_2local
        K = pqk_gram_2local([psi, psi], 8, pairs=nn_bonds, gamma=1.0)
        assert K.shape == (2, 2)
        assert np.allclose(K, 1.0)
