"""
tests/test_stage3_ood.py
------------------------
Unit tests for Stage 3: Controlled OOD Phase-Shift Generalization (Task 6).
"""

import os
import sys
import pytest
import numpy as np

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SCRIPTS = os.path.join(_PROJECT_ROOT, "scripts")
_SRC = os.path.join(_PROJECT_ROOT, "src")
for p in [_SRC, _SCRIPTS]:
    if p not in sys.path:
        sys.path.insert(0, p)

from stage3_ood_shift import sample_domain_states, extract_features, build_gram_matrices


def test_domain_bounds():
    """
    Test 1 (Domain bounds):
    Assert min(h_train) >= 0.8, max(h_train) <= 1.5;
    assert min(h_ood) >= 0.2, max(h_ood) <= 0.7.
    """
    rng = np.random.default_rng(20261023)
    n = 8

    # Train domain: 40 states
    train_data = sample_domain_states(n, 40, 0.8, 1.5, rng)
    fields_train = train_data["fields"]
    assert np.min(fields_train) >= 0.8 - 1e-12, f"Train field min out of bounds: {np.min(fields_train)}"
    assert np.max(fields_train) <= 1.5 + 1e-12, f"Train field max out of bounds: {np.max(fields_train)}"

    # ID test domain: 100 states
    id_data = sample_domain_states(n, 100, 0.8, 1.5, rng)
    fields_id = id_data["fields"]
    assert np.min(fields_id) >= 0.8 - 1e-12, f"ID field min out of bounds: {np.min(fields_id)}"
    assert np.max(fields_id) <= 1.5 + 1e-12, f"ID field max out of bounds: {np.max(fields_id)}"

    # OOD test domain: 100 states
    ood_data = sample_domain_states(n, 100, 0.2, 0.7, rng)
    fields_ood = ood_data["fields"]
    assert np.min(fields_ood) >= 0.2 - 1e-12, f"OOD field min out of bounds: {np.min(fields_ood)}"
    assert np.max(fields_ood) <= 0.7 + 1e-12, f"OOD field max out of bounds: {np.max(fields_ood)}"

    # Strictly disjoint threshold check: max(OOD) < min(Train)
    assert np.max(fields_ood) < np.min(fields_train), "OOD and Train field distributions must not overlap"


def test_shape_and_leakage_consistency():
    """
    Test 2 (Shape & leakage consistency):
    Assert X_train is (40, 35), X_test,ID is (100, 35), and X_test,OOD is (100, 35).
    Verify FQ Gram matrices shapes: (40, 40), (100, 40), (100, 40).
    """
    rng = np.random.default_rng(999)
    n = 8

    train_data = sample_domain_states(n, 40, 0.8, 1.5, rng)
    id_data = sample_domain_states(n, 100, 0.8, 1.5, rng)
    ood_data = sample_domain_states(n, 100, 0.2, 0.7, rng)

    X_x_tr, X_e2_tr, X_pqk2_tr = extract_features(train_data["states"], n)
    X_x_id, X_e2_id, X_pqk2_id = extract_features(id_data["states"], n)
    X_x_ood, X_e2_ood, X_pqk2_ood = extract_features(ood_data["states"], n)

    # Correlator shapes
    assert X_e2_tr.shape == (40, 35), f"Expected X_e2_tr shape (40, 35), got {X_e2_tr.shape}"
    assert X_e2_id.shape == (100, 35), f"Expected X_e2_id shape (100, 35), got {X_e2_id.shape}"
    assert X_e2_ood.shape == (100, 35), f"Expected X_e2_ood shape (100, 35), got {X_e2_ood.shape}"

    # PQK-1 shapes
    assert X_x_tr.shape == (40, 8), f"Expected X_x_tr shape (40, 8), got {X_x_tr.shape}"
    assert X_x_id.shape == (100, 8), f"Expected X_x_id shape (100, 8), got {X_x_id.shape}"
    assert X_x_ood.shape == (100, 8), f"Expected X_x_ood shape (100, 8), got {X_x_ood.shape}"

    # Gram matrix shapes
    K_tr, K_id, K_ood = build_gram_matrices(train_data["states"], id_data["states"], ood_data["states"])
    assert K_tr.shape == (40, 40), f"Expected K_tr shape (40, 40), got {K_tr.shape}"
    assert K_id.shape == (100, 40), f"Expected K_id shape (100, 40), got {K_id.shape}"
    assert K_ood.shape == (100, 40), f"Expected K_ood shape (100, 40), got {K_ood.shape}"

    # Diagonal fidelity of train Gram matrix is 1.0
    np.testing.assert_allclose(np.diag(K_tr), 1.0, atol=1e-12)


def test_residual_integrity():
    """
    Test 3 (Residual integrity):
    Assert eigenpair residual ||H|psi> - E|psi>||_2 < 1e-10 across both
    paramagnetic and ferromagnetic generated states.
    """
    rng = np.random.default_rng(12345)
    n = 8

    # Paramagnetic sample
    para_data = sample_domain_states(n, 10, 0.8, 1.5, rng)
    for res in para_data["residuals"]:
        assert res < 1e-10, f"Paramagnetic ground state residual {res} >= 1e-10"

    # Ferromagnetic sample
    ferro_data = sample_domain_states(n, 10, 0.2, 0.7, rng)
    for res in ferro_data["residuals"]:
        assert res < 1e-10, f"Ferromagnetic ground state residual {res} >= 1e-10"
