"""
tests/test_stage1b_repairs.py
-----------------------------
Unit tests for Gram repair functions (S1b.1):
- repair_none
- repair_train_only
- repair_inductive
- repair_joint (transductive)
"""

import os
import sys
import pytest
import numpy as np

# Add src and scripts to path
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SCRIPTS = os.path.join(_PROJECT_ROOT, "scripts")
_SRC = os.path.join(_PROJECT_ROOT, "src")
for p in [_SRC, _SCRIPTS]:
    if p not in sys.path:
        sys.path.insert(0, p)

from ablation_r3_repairs import (
    repair_none,
    repair_train_only,
    repair_inductive,
    repair_joint,
)


@pytest.fixture
def exact_psd_gram():
    """Exact PSD fidelity Gram on n=6, 8 train + 5 test pure states."""
    n = 6
    dim = 2 ** n
    rng = np.random.default_rng(20261023)
    states = rng.normal(size=(13, dim)) + 1j * rng.normal(size=(13, dim))
    states = states / np.linalg.norm(states, axis=1, keepdims=True)
    K_full = np.abs(states @ states.conj().T) ** 2
    N_tr = 8
    N_te = 5
    K_tr = K_full[:N_tr, :N_tr].copy()
    K_te = K_full[N_tr:, :N_tr].copy()
    return K_full, K_tr, K_te, N_tr, N_te


def test_repairs_on_exact_psd_gram(exact_psd_gram):
    """
    On an exact PSD Gram (noiseless fidelity Gram, n=6, 8 train + 5 test),
    all four repairs return the input (to 1e-10).
    """
    K_full, K_tr, K_te, N_tr, N_te = exact_psd_gram

    k_tr_none, k_te_none = repair_none(K_tr, K_te)
    np.testing.assert_allclose(k_tr_none, K_tr, rtol=0, atol=1e-10)
    np.testing.assert_allclose(k_te_none, K_te, rtol=0, atol=1e-10)

    k_tr_to, k_te_to = repair_train_only(K_tr, K_te)
    np.testing.assert_allclose(k_tr_to, K_tr, rtol=0, atol=1e-10)
    np.testing.assert_allclose(k_te_to, K_te, rtol=0, atol=1e-10)

    k_tr_ind, k_te_ind = repair_inductive(K_tr, K_te)
    np.testing.assert_allclose(k_tr_ind, K_tr, rtol=0, atol=1e-10)
    np.testing.assert_allclose(k_te_ind, K_te, rtol=0, atol=1e-10)

    k_tr_joint, k_te_joint = repair_joint(K_full, N_tr)
    np.testing.assert_allclose(k_tr_joint, K_tr, rtol=0, atol=1e-10)
    np.testing.assert_allclose(k_te_joint, K_te, rtol=0, atol=1e-10)


def test_inductive_repair_properties(exact_psd_gram):
    """
    K_tr' from repair_inductive is symmetric, PSD (min eig >= -1e-10), unit diagonal.
    """
    _, K_tr, K_te, _, _ = exact_psd_gram

    # Create deliberately indefinite training matrix with -0.2 eigenvalue
    K_tr_indef = K_tr.copy()
    K_tr_indef[0, 1] = 1.2
    K_tr_indef[1, 0] = 1.2

    K_tr_repaired, K_te_repaired = repair_inductive(K_tr_indef, K_te)

    # 1. Symmetry
    np.testing.assert_allclose(K_tr_repaired, K_tr_repaired.T, rtol=0, atol=1e-10)

    # 2. PSD (min eig >= -1e-10)
    min_eig = float(np.min(np.linalg.eigvalsh(K_tr_repaired)))
    assert min_eig >= -1e-10, f"Expected min eigenvalue >= -1e-10, got {min_eig}"

    # 3. Unit diagonal
    np.testing.assert_allclose(np.diag(K_tr_repaired), 1.0, rtol=0, atol=1e-10)


def test_inductive_row_independence(exact_psd_gram):
    """
    Inductive repair of the test block depends only on K_tr and K_te (assert by changing
    K_te rows of OTHER test points and checking row-wise independence: each row of K_te' is unchanged).
    """
    _, K_tr, K_te, _, _ = exact_psd_gram

    # Indefinite K_tr
    K_tr_indef = K_tr.copy()
    K_tr_indef[0, 1] = 1.2
    K_tr_indef[1, 0] = 1.2

    _, K_te_rep1 = repair_inductive(K_tr_indef, K_te)

    # Perturb row 2 of K_te
    K_te_pert = K_te.copy()
    K_te_pert[2, :] += 0.4
    _, K_te_rep2 = repair_inductive(K_tr_indef, K_te_pert)

    # Assert row 0, 1, 3, 4 are completely unchanged (to 1e-10)
    np.testing.assert_allclose(K_te_rep1[0], K_te_rep2[0], rtol=0, atol=1e-10)
    np.testing.assert_allclose(K_te_rep1[1], K_te_rep2[1], rtol=0, atol=1e-10)
    np.testing.assert_allclose(K_te_rep1[3], K_te_rep2[3], rtol=0, atol=1e-10)
    np.testing.assert_allclose(K_te_rep1[4], K_te_rep2[4], rtol=0, atol=1e-10)


def test_joint_repair_transductive_property(exact_psd_gram):
    """
    Joint repair: changing one test state's entries changes train-block output (print the magnitude)
    -> this is the transductive property.
    """
    K_full, _, _, N_tr, _ = exact_psd_gram

    # Indefinite full Gram with coupling to test state
    K_full_indef = K_full.copy()
    K_full_indef[0, 1] = K_full_indef[1, 0] = 0.95
    K_full_indef[N_tr, 0] = K_full_indef[0, N_tr] = 0.95
    K_full_indef[N_tr, 1] = K_full_indef[1, N_tr] = 0.95

    K_tr_j1, _ = repair_joint(K_full_indef, N_tr)

    # Perturb test state (row N_tr)
    K_full_mod = K_full_indef.copy()
    K_full_mod[N_tr, 2] = K_full_mod[2, N_tr] = 0.95

    K_tr_j2, _ = repair_joint(K_full_mod, N_tr)

    max_train_diff = float(np.max(np.abs(K_tr_j1 - K_tr_j2)))
    print(f"\nTransductive shift in K_tr when altering one test state: {max_train_diff:.4e}")
    assert max_train_diff > 1e-4, f"Expected non-zero transductive effect on K_tr, got {max_train_diff}"


def test_negative_control_indefinite_repair(exact_psd_gram):
    """
    Negative control: with a deliberately indefinite K_tr (inject -0.2 eigenvalue),
    repair_train_only leaves K_te unchanged, inductive does not.
    """
    _, K_tr, K_te, _, _ = exact_psd_gram

    # Inject -0.2 eigenvalue via off-diagonal coupling
    K_tr_indef = K_tr.copy()
    K_tr_indef[0, 1] = 1.2
    K_tr_indef[1, 0] = 1.2

    # repair_train_only leaves K_te identical
    _, K_te_to = repair_train_only(K_tr_indef, K_te)
    np.testing.assert_allclose(K_te_to, K_te, rtol=0, atol=1e-10)

    # repair_inductive modifies K_te
    _, K_te_ind = repair_inductive(K_tr_indef, K_te)
    te_diff = float(np.max(np.abs(K_te_ind - K_te)))
    print(f"\nNegative control difference in K_te under inductive repair: {te_diff:.4e}")
    assert te_diff > 1e-4, f"Expected inductive repair to alter K_te for indefinite K_tr, got diff {te_diff}"
