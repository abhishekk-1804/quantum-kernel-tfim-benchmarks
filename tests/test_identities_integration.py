"""
tests/test_identities_integration.py
------------------------------------
Integration tests verifying exact algebraic identities between projected quantum
kernels (PQK-1, PQK-2nn) and classical Pauli correlator representations,
including degree weighting and physical parity constraints on 1D TFIM and 2D
frustrated lattices.
"""

import sys
import os
import numpy as np
import pytest
from numpy.testing import assert_allclose

# Ensure src is in sys.path
_SRC = os.path.join(os.path.dirname(__file__), "..", "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from hamiltonians import (
    build_tfim,
    build_frustrated_2d,
    ground_state,
    _build_parity_op,
)
from kernels import (
    one_rdm,
    two_rdm,
    pqk_gram,
    pqk_gram_2local,
    classical_features,
)


def _build_deduplicated_features(psi, n, pairs, degrees, weight_mode="sqrt_deg"):
    """
    Build deduplicated feature vector:
      [x_i * w_i for i in range(n)] + [XX, YY, ZZ for each edge in pairs]
    where w_i depends on weight_mode.
    """
    feats = []
    x = classical_features(psi, n, mode="1pt_X")
    for i in range(n):
        if weight_mode == "sqrt_deg":
            w = np.sqrt(degrees[i])
        elif weight_mode == "one":
            w = 1.0
        elif weight_mode == "deg":
            w = float(degrees[i])
        else:
            raise ValueError(f"Unknown weight_mode: {weight_mode}")
        feats.append(x[i] * w)

    # 2-body correlators per edge: XX, YY, ZZ
    _XX = np.kron(np.array([[0, 1], [1, 0]], dtype=complex), np.array([[0, 1], [1, 0]], dtype=complex))
    _YY = np.kron(np.array([[0, -1j], [1j, 0]], dtype=complex), np.array([[0, -1j], [1j, 0]], dtype=complex))
    _ZZ = np.kron(np.array([[1, 0], [0, -1]], dtype=complex), np.array([[1, 0], [0, -1]], dtype=complex))
    for i, j in pairs:
        rho_ij = two_rdm(psi, n, i, j)
        feats.append(float(np.real(np.trace(rho_ij @ _XX))))
        feats.append(float(np.real(np.trace(rho_ij @ _YY))))
        feats.append(float(np.real(np.trace(rho_ij @ _ZZ))))
    return np.array(feats, dtype=float)


@pytest.fixture(scope="module")
def tfim_1d_states():
    """Generate 5 disordered 1D TFIM states at n=6 with fixed seed."""
    n = 6
    rng = np.random.default_rng(20261023)
    sample_states = []
    hamiltonians = []
    energies = []
    for _ in range(5):
        fields = rng.uniform(0.5, 1.5, size=n)
        couplings = rng.uniform(0.8, 1.2, size=n - 1)
        H = build_tfim(n, g=1.0, J=1.0, boundary="open", fields=fields, couplings=couplings)
        E0, psi, _ = ground_state(H, n, sector="even")
        sample_states.append(psi)
        hamiltonians.append(H)
        energies.append(E0)
    return {
        "n": n,
        "states": sample_states,
        "hamiltonians": hamiltonians,
        "energies": energies,
    }


@pytest.fixture(scope="module")
def lattice_2d_states():
    """Generate 5 frustrated 2D lattice states (2x4) with fixed seed."""
    rows, cols = 2, 4
    n = rows * cols
    rng = np.random.default_rng(20261024)
    sample_states = []
    hamiltonians = []
    energies = []

    # Obtain the real nearest-neighbour bond list as used in scripts/run_t4_v2.py
    _, nn_bonds, _ = build_frustrated_2d(rows=rows, cols=cols, g=1.0, J1=-1.0, J2=0.5)

    for _ in range(5):
        g = rng.uniform(0.5, 1.5)
        J2 = rng.uniform(0.1, 0.9)
        H, bonds, _ = build_frustrated_2d(rows=rows, cols=cols, g=g, J1=-1.0, J2=J2)
        E0, psi, _ = ground_state(H, n, sector="even")
        sample_states.append(psi)
        hamiltonians.append(H)
        energies.append(E0)

    degrees = np.zeros(n, dtype=float)
    for i, j in nn_bonds:
        degrees[i] += 1
        degrees[j] += 1

    return {
        "rows": rows,
        "cols": cols,
        "n": n,
        "nn_bonds": nn_bonds,
        "degrees": degrees,
        "states": sample_states,
        "hamiltonians": hamiltonians,
        "energies": energies,
    }


def test_a_pqk1_identity_1d(tfim_1d_states):
    """
    a. PQK-1 algebraic identity:
       sum_k ||rho_k(a) - rho_k(b)||_F^2 == 0.5 * ||x(a) - x(b)||^2
       where x = classical_features(mode='1pt_X'),
       and pqk_gram(gamma) == exp(-(gamma/2) * sqeuclid).
    """
    n = tfim_1d_states["n"]
    states = tfim_1d_states["states"]
    m = len(states)

    rdms_list = [[one_rdm(psi, n, k) for k in range(n)] for psi in states]
    x_feats = np.array([classical_features(psi, n, mode="1pt_X") for psi in states])

    # Step 1: Compare pre-exponential squared distances first
    dist2_rdm = np.zeros((m, m), dtype=float)
    dist2_class = np.zeros((m, m), dtype=float)
    for a in range(m):
        for b in range(m):
            sum_fro = 0.0
            for k in range(n):
                diff = rdms_list[a][k] - rdms_list[b][k]
                sum_fro += float(np.real(np.trace(diff.conj().T @ diff)))
            dist2_rdm[a, b] = sum_fro
            dist2_class[a, b] = 0.5 * float(np.sum((x_feats[a] - x_feats[b]) ** 2))

    assert_allclose(dist2_rdm, dist2_class, rtol=0.0, atol=1e-12)

    # Step 2: Compare Gram matrices
    gamma = 1.25
    K_pqk = pqk_gram(rdms_list, gamma=gamma)
    K_expected = np.exp(-(gamma / 2.0) * (np.sum((x_feats[:, None, :] - x_feats[None, :, :]) ** 2, axis=-1)))
    assert_allclose(K_pqk, K_expected, rtol=0.0, atol=1e-12)


def test_b_pqk2nn_chain_identity(tfim_1d_states):
    """
    b. PQK-2nn on a chain:
       sum_{(i,j) in nn} ||rho_ij(a) - rho_ij(b)||_F^2 == 0.25 * ||f(a) - f(b)||^2
       where f = classical_features(mode='2pt_pauli_nn', pairs=pairs),
       and pqk_gram_2local(gamma) == exp(-(gamma/4) * sqeuclid).
    """
    n = tfim_1d_states["n"]
    states = tfim_1d_states["states"]
    m = len(states)
    pairs = [(i, i + 1) for i in range(n - 1)]

    f_2nn = np.array([classical_features(psi, n, mode="2pt_pauli_nn", pairs=pairs) for psi in states])

    # Step 1: Compare pre-exponential squared distances first
    dist2_rdm = np.zeros((m, m), dtype=float)
    dist2_class = np.zeros((m, m), dtype=float)
    for a in range(m):
        for b in range(m):
            sum_fro = 0.0
            for i, j in pairs:
                diff = two_rdm(states[a], n, i, j) - two_rdm(states[b], n, i, j)
                sum_fro += float(np.real(np.trace(diff.conj().T @ diff)))
            dist2_rdm[a, b] = sum_fro
            dist2_class[a, b] = 0.25 * float(np.sum((f_2nn[a] - f_2nn[b]) ** 2))

    assert_allclose(dist2_rdm, dist2_class, rtol=0.0, atol=1e-12)

    # Step 2: Compare Gram matrices
    gamma = 0.75
    K_pqk2 = pqk_gram_2local(states, n, pairs=pairs, gamma=gamma)
    sqeuclid = np.sum((f_2nn[:, None, :] - f_2nn[None, :, :]) ** 2, axis=-1)
    K_expected = np.exp(-(gamma / 4.0) * sqeuclid)
    assert_allclose(K_pqk2, K_expected, rtol=0.0, atol=1e-12)


def test_c_degree_weighting_1d(tfim_1d_states):
    """
    c. Degree weighting on 1D chain:
       Deduplicated features [x_i * sqrt(deg_i), (xx,yy,zz) per edge];
       its 0.25 * sqeuclid equals sum over nn pairs of ||rho_ij(a) - rho_ij(b)||_F^2.
       Negative controls with weights 1 and deg_i must differ (gap > 1e-6).
    """
    n = tfim_1d_states["n"]
    states = tfim_1d_states["states"]
    m = len(states)
    pairs = [(i, i + 1) for i in range(n - 1)]

    degrees = np.zeros(n, dtype=float)
    for i, j in pairs:
        degrees[i] += 1
        degrees[j] += 1

    f_dedup = np.array([_build_deduplicated_features(psi, n, pairs, degrees, "sqrt_deg") for psi in states])
    f_nc1 = np.array([_build_deduplicated_features(psi, n, pairs, degrees, "one") for psi in states])
    f_nc2 = np.array([_build_deduplicated_features(psi, n, pairs, degrees, "deg") for psi in states])

    dist2_rdm = np.zeros((m, m), dtype=float)
    dist2_dedup = np.zeros((m, m), dtype=float)
    dist2_nc1 = np.zeros((m, m), dtype=float)
    dist2_nc2 = np.zeros((m, m), dtype=float)

    for a in range(m):
        for b in range(m):
            sum_fro = sum(
                float(np.real(np.trace((two_rdm(states[a], n, i, j) - two_rdm(states[b], n, i, j)).conj().T @ (
                    two_rdm(states[a], n, i, j) - two_rdm(states[b], n, i, j)
                ))))
                for i, j in pairs
            )
            dist2_rdm[a, b] = sum_fro
            dist2_dedup[a, b] = 0.25 * float(np.sum((f_dedup[a] - f_dedup[b]) ** 2))
            dist2_nc1[a, b] = 0.25 * float(np.sum((f_nc1[a] - f_nc1[b]) ** 2))
            dist2_nc2[a, b] = 0.25 * float(np.sum((f_nc2[a] - f_nc2[b]) ** 2))

    # Deduplicated features with sqrt(deg_i) must match exactly
    assert_allclose(dist2_rdm, dist2_dedup, rtol=0.0, atol=1e-12)

    # Negative controls:
    # In an open chain, end spins have degree 1 while bulk spins have degree 2.
    # In the sum over edges, each site i appears deg(i) times in the 1-body terms.
    # Therefore, the squared Euclidean distance requires weighting x_i by sqrt(deg_i)
    # so that (x_i * sqrt(deg_i))^2 contributes deg_i * x_i^2.
    # Weighting by 1.0 underestimates bulk sites (weight 1 != 2), while weighting
    # by deg_i produces deg_i^2 * x_i^2 (weight 4 != 2 for bulk sites).
    gap_nc1 = float(np.max(np.abs(dist2_rdm - dist2_nc1)))
    gap_nc2 = float(np.max(np.abs(dist2_rdm - dist2_nc2)))

    print(f"\n[1D Chain] Max gap for negative control (weight=1.0): {gap_nc1:.6e}")
    print(f"[1D Chain] Max gap for negative control (weight=deg_i): {gap_nc2:.6e}")

    assert gap_nc1 > 1e-6, f"Expected gap_nc1 > 1e-6, got {gap_nc1}"
    assert gap_nc2 > 1e-6, f"Expected gap_nc2 > 1e-6, got {gap_nc2}"


def test_d_lattice_case_2d(lattice_2d_states):
    """
    d. Lattice case: repeat (b) and (c) for build_frustrated_2d(rows=2, cols=4)
       using the real nearest-neighbour bond list taken from run_t4_v2.py.
    """
    n = lattice_2d_states["n"]
    nn_bonds = lattice_2d_states["nn_bonds"]
    degrees = lattice_2d_states["degrees"]
    states = lattice_2d_states["states"]
    m = len(states)

    print(f"\n[2D Frustrated Lattice 2x4] Bond list ({len(nn_bonds)} bonds): {nn_bonds}")
    print(f"[2D Frustrated Lattice 2x4] Vertex degrees: {degrees.tolist()}")

    # Repeat (b): PQK-2nn identity on 2D lattice
    f_2nn = np.array([classical_features(psi, n, mode="2pt_pauli_nn", pairs=nn_bonds) for psi in states])

    dist2_rdm = np.zeros((m, m), dtype=float)
    dist2_class = np.zeros((m, m), dtype=float)
    for a in range(m):
        for b in range(m):
            sum_fro = sum(
                float(np.real(np.trace((two_rdm(states[a], n, i, j) - two_rdm(states[b], n, i, j)).conj().T @ (
                    two_rdm(states[a], n, i, j) - two_rdm(states[b], n, i, j)
                ))))
                for i, j in nn_bonds
            )
            dist2_rdm[a, b] = sum_fro
            dist2_class[a, b] = 0.25 * float(np.sum((f_2nn[a] - f_2nn[b]) ** 2))

    assert_allclose(dist2_rdm, dist2_class, rtol=0.0, atol=1e-12)

    gamma = 1.1
    K_pqk2 = pqk_gram_2local(states, n, pairs=nn_bonds, gamma=gamma)
    sqeuclid = np.sum((f_2nn[:, None, :] - f_2nn[None, :, :]) ** 2, axis=-1)
    K_expected = np.exp(-(gamma / 4.0) * sqeuclid)
    assert_allclose(K_pqk2, K_expected, rtol=0.0, atol=1e-12)

    # Repeat (c): Degree weighting on 2D lattice
    f_dedup = np.array([_build_deduplicated_features(psi, n, nn_bonds, degrees, "sqrt_deg") for psi in states])
    f_nc1 = np.array([_build_deduplicated_features(psi, n, nn_bonds, degrees, "one") for psi in states])
    f_nc2 = np.array([_build_deduplicated_features(psi, n, nn_bonds, degrees, "deg") for psi in states])

    dist2_dedup = np.zeros((m, m), dtype=float)
    dist2_nc1 = np.zeros((m, m), dtype=float)
    dist2_nc2 = np.zeros((m, m), dtype=float)

    for a in range(m):
        for b in range(m):
            dist2_dedup[a, b] = 0.25 * float(np.sum((f_dedup[a] - f_dedup[b]) ** 2))
            dist2_nc1[a, b] = 0.25 * float(np.sum((f_nc1[a] - f_nc1[b]) ** 2))
            dist2_nc2[a, b] = 0.25 * float(np.sum((f_nc2[a] - f_nc2[b]) ** 2))

    assert_allclose(dist2_rdm, dist2_dedup, rtol=0.0, atol=1e-12)

    # On the 2x4 lattice, corner sites have degree 2 while bulk/edge sites have degree 3.
    # Non-uniform degrees ensure that unweighted (w=1) and degree-squared (w=deg) features
    # fail to reproduce the multi-edge appearance count of 1-body observables.
    gap_nc1 = float(np.max(np.abs(dist2_rdm - dist2_nc1)))
    gap_nc2 = float(np.max(np.abs(dist2_rdm - dist2_nc2)))

    print(f"[2D Lattice] Max gap for negative control (weight=1.0): {gap_nc1:.6e}")
    print(f"[2D Lattice] Max gap for negative control (weight=deg_i): {gap_nc2:.6e}")

    assert gap_nc1 > 1e-6, f"Expected 2D gap_nc1 > 1e-6, got {gap_nc1}"
    assert gap_nc2 > 1e-6, f"Expected 2D gap_nc2 > 1e-6, got {gap_nc2}"


def test_e_assumption_checks(tfim_1d_states, lattice_2d_states):
    """
    e. Assumption checks on the sample states:
       - norm 1
       - eigenpair residual < 1e-9: ||H psi - E0 psi||_2 < 1e-9
       - parity <psi|P|psi> = +1 within 1e-8
       - <Y_i> = 0 within 1e-12, <Z_i> = 0 within 1e-12
       - 1-RDM and 2-RDM Hermitian with trace 1 within 1e-12
    """
    # Test 1D TFIM states
    n_1d = tfim_1d_states["n"]
    P_1d = _build_parity_op(n_1d)
    for psi, H, E0 in zip(tfim_1d_states["states"], tfim_1d_states["hamiltonians"], tfim_1d_states["energies"]):
        # Norm 1
        assert abs(float(np.linalg.norm(psi)) - 1.0) < 1e-12

        # Eigenpair residual
        residual = float(np.linalg.norm(H.dot(psi) - E0 * psi))
        assert residual < 1e-9, f"1D eigenpair residual {residual:.3e} >= 1e-9"

        # Parity <psi|P|psi> = +1
        parity = float(np.real(psi.conj() @ (P_1d @ psi)))
        assert abs(parity - 1.0) < 1e-8, f"1D parity expectation {parity} not +1 within 1e-8"

        # 1-RDM checks
        _Y2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
        _Z2 = np.array([[1, 0], [0, -1]], dtype=complex)
        for k in range(n_1d):
            rho_k = one_rdm(psi, n_1d, k)
            assert_allclose(rho_k, rho_k.conj().T, rtol=0.0, atol=1e-12)
            assert_allclose(float(np.real(np.trace(rho_k))), 1.0, rtol=0.0, atol=1e-12)
            exp_y = float(np.real(np.trace(rho_k @ _Y2)))
            exp_z = float(np.real(np.trace(rho_k @ _Z2)))
            assert abs(exp_y) < 1e-12, f"Expected <Y_{k}> == 0, got {exp_y}"
            assert abs(exp_z) < 1e-12, f"Expected <Z_{k}> == 0, got {exp_z}"

        # 2-RDM checks on nearest neighbours
        for i in range(n_1d - 1):
            rho_ij = two_rdm(psi, n_1d, i, i + 1)
            assert_allclose(rho_ij, rho_ij.conj().T, rtol=0.0, atol=1e-12)
            assert_allclose(float(np.real(np.trace(rho_ij))), 1.0, rtol=0.0, atol=1e-12)

    # Test 2D frustrated lattice states
    n_2d = lattice_2d_states["n"]
    P_2d = _build_parity_op(n_2d)
    nn_bonds = lattice_2d_states["nn_bonds"]
    for psi, H, E0 in zip(lattice_2d_states["states"], lattice_2d_states["hamiltonians"], lattice_2d_states["energies"]):
        # Norm 1
        assert abs(float(np.linalg.norm(psi)) - 1.0) < 1e-12

        # Eigenpair residual
        residual = float(np.linalg.norm(H.dot(psi) - E0 * psi))
        assert residual < 1e-9, f"2D eigenpair residual {residual:.3e} >= 1e-9"

        # Parity <psi|P|psi> = +1
        parity = float(np.real(psi.conj() @ (P_2d @ psi)))
        assert abs(parity - 1.0) < 1e-8, f"2D parity expectation {parity} not +1 within 1e-8"

        # 1-RDM checks
        _Y2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
        _Z2 = np.array([[1, 0], [0, -1]], dtype=complex)
        for k in range(n_2d):
            rho_k = one_rdm(psi, n_2d, k)
            assert_allclose(rho_k, rho_k.conj().T, rtol=0.0, atol=1e-12)
            assert_allclose(float(np.real(np.trace(rho_k))), 1.0, rtol=0.0, atol=1e-12)
            exp_y = float(np.real(np.trace(rho_k @ _Y2)))
            exp_z = float(np.real(np.trace(rho_k @ _Z2)))
            assert abs(exp_y) < 1e-12, f"Expected 2D <Y_{k}> == 0, got {exp_y}"
            assert abs(exp_z) < 1e-12, f"Expected 2D <Z_{k}> == 0, got {exp_z}"

        # 2-RDM checks on bonds
        for i, j in nn_bonds:
            rho_ij = two_rdm(psi, n_2d, i, j)
            assert_allclose(rho_ij, rho_ij.conj().T, rtol=0.0, atol=1e-12)
            assert_allclose(float(np.real(np.trace(rho_ij))), 1.0, rtol=0.0, atol=1e-12)
