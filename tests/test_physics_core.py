"""
tests/test_physics_core.py
--------------------------
Pytest suite for Phase 1 physics core: hamiltonians, kernels, noise.

All tests use the D:/quantum-kernel-tfim-benchmarks/src package, which is
added to sys.path by conftest.py (or inserted explicitly here for portability).
"""

import sys
import os
import numpy as np
import scipy.linalg
import pytest

# Ensure src/ is importable regardless of how pytest is invoked
_SRC = os.path.join(os.path.dirname(__file__), "..", "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from hamiltonians import (
    build_tfim,
    build_frustrated_2d,
    ground_state,
    expect_x,
    expect_zz,
    correlation_matrix,
    half_chain_entropy,
    structure_factor,
)
from kernels import (
    one_rdm,
    bloch_vector,
    fidelity_gram,
    pqk_gram,
    kta,
    classical_features,
    off_diagonal_variance,
)
from noise import depolarize_rdm, shot_noise_pqk, shot_noise_fidelity


# ═══════════════════════════════════════════════════════════════════════════════
# 1. Analytic Energy Verification
# ═══════════════════════════════════════════════════════════════════════════════

class TestAnalyticEnergy:
    """Compare ground_state against free-fermion exact results."""

    def test_n4_periodic_energy_against_closed_form(self):
        """
        1D Periodic TFIM, n=4, J=1, g=1.
        Free-fermion result: E0 = -2 / sin(π/8) ≈ -5.2262518595.
        """
        H = build_tfim(4, g=1.0, J=1.0, boundary="periodic")
        E0, psi, gap = ground_state(H, 4, sector="even", symmetry_break=0.0)

        expected_E0 = -2.0 / np.sin(np.pi / 8.0)
        assert abs(E0 - expected_E0) < 1e-8, (
            f"n=4 periodic E0={E0:.12f}, expected {expected_E0:.12f}, "
            f"diff={abs(E0-expected_E0):.3e}"
        )

    def test_n4_periodic_energy_against_dense_diag(self):
        """
        n=4 periodic: ground_state result must agree with dense eigh to 1e-10.
        """
        H = build_tfim(4, g=1.0, J=1.0, boundary="periodic")
        E0_gs, _, _ = ground_state(H, 4, sector="even")

        H_dense = H.toarray()
        evals_dense = scipy.linalg.eigh(H_dense, eigvals_only=True)
        E0_dense = float(evals_dense[0])

        assert abs(E0_gs - E0_dense) < 1e-10, (
            f"Sparse/dense mismatch: {E0_gs:.14f} vs {E0_dense:.14f}"
        )

    def test_n6_periodic_energy_against_free_fermion(self):
        """
        1D Periodic TFIM, n=6, J=1, g=1.
        Free-fermion ground energy:
            E0 = -∑_{k ∈ {±π/6, ±π/2, ±5π/6}} 2|sin(k/2)|
        """
        H = build_tfim(6, g=1.0, J=1.0, boundary="periodic")
        E0, psi, gap = ground_state(H, 6, sector="even", symmetry_break=0.0)

        k_modes = [np.pi / 6, np.pi / 2, 5 * np.pi / 6,
                   -np.pi / 6, -np.pi / 2, -5 * np.pi / 6]
        expected_E0 = -sum(2.0 * abs(np.sin(k / 2.0)) for k in k_modes)

        assert abs(E0 - expected_E0) < 1e-8, (
            f"n=6 periodic E0={E0:.12f}, expected {expected_E0:.12f}"
        )

    def test_n4_wavevector_normalised(self):
        """Ground state returned by ground_state must be normalised."""
        H = build_tfim(4, g=1.0, J=1.0, boundary="periodic")
        _, psi, _ = ground_state(H, 4, sector="even")
        assert abs(np.dot(psi, psi) - 1.0) < 1e-7


# ═══════════════════════════════════════════════════════════════════════════════
# 2. 2D Frustrated Lattice — Bond Count Validation
# ═══════════════════════════════════════════════════════════════════════════════

class TestFrustratedLattice2D:
    """Structural tests for build_frustrated_2d."""

    def test_bond_counts_2x4(self):
        """
        For a 2×4 open lattice:
        - NN bonds: 3 horizontal (row 0) + 3 horizontal (row 1) + 4 vertical = 10
        - NNN diagonal bonds: 1 × 3 plaquettes × 2 diagonals = 6
        """
        _, nn_bonds, nnn_bonds = build_frustrated_2d(rows=2, cols=4)
        assert len(nn_bonds) == 10, (
            f"Expected 10 NN bonds, got {len(nn_bonds)}"
        )
        assert len(nnn_bonds) == 6, (
            f"Expected 6 NNN diagonal bonds, got {len(nnn_bonds)}"
        )

    def test_no_duplicate_bonds(self):
        """Each bond pair should appear exactly once."""
        _, nn_bonds, nnn_bonds = build_frustrated_2d(rows=2, cols=4)
        nn_set = set(tuple(sorted(b)) for b in nn_bonds)
        nnn_set = set(tuple(sorted(b)) for b in nnn_bonds)
        assert len(nn_set) == 10, "Duplicate NN bonds detected"
        assert len(nnn_set) == 6, "Duplicate NNN bonds detected"

    def test_hamiltonian_shape(self):
        """Hamiltonian shape must be 2^(rows*cols) × 2^(rows*cols)."""
        H, _, _ = build_frustrated_2d(rows=2, cols=4)
        n = 2 * 4
        assert H.shape == (2 ** n, 2 ** n), f"Unexpected shape {H.shape}"

    def test_hamiltonian_hermitian(self):
        """2D Hamiltonian must be Hermitian (sparse)."""
        H, _, _ = build_frustrated_2d(rows=2, cols=4, g=0.5)
        diff = H - H.conj().T
        assert diff.max() < 1e-12, "Hamiltonian is not Hermitian"


# ═══════════════════════════════════════════════════════════════════════════════
# 3. Structure Factor Sanity
# ═══════════════════════════════════════════════════════════════════════════════

class TestStructureFactor:
    """Structure factor tests on known states."""

    @staticmethod
    def _neel_state_2x4():
        """Build Néel product state |↑↓↑↓↓↑↓↑⟩ on a 2×4 lattice (row-major).

        Site (r, c): spin-up if (r+c) is even, spin-down if (r+c) is odd.
        Basis: |0⟩ = spin-up (Z=+1), |1⟩ = spin-down (Z=-1).
        Qubit 0 is the most significant bit of the state index.
        """
        n, cols = 8, 4
        neel_index = 0
        for site in range(n):
            r, c = divmod(site, cols)
            if (r + c) % 2 == 1:  # spin-down → bit = 1
                neel_index |= 1 << (n - 1 - site)
        psi = np.zeros(2 ** n)
        psi[neel_index] = 1.0
        return psi

    def test_neel_structure_factor_max_at_pi_pi(self):
        """
        Perfect Néel state: structure factor S(q) must peak at q=(π, π).
        """
        psi = self._neel_state_2x4()
        Sq = structure_factor(psi, rows=2, cols=4)

        max_q = max(Sq, key=Sq.get)
        assert max_q == (np.pi, np.pi), (
            f"S(q) max at {max_q}, expected (π, π). Values:\n"
            + "\n".join(f"  {k}: {v:.4f}" for k, v in sorted(Sq.items()))
        )

    def test_structure_factor_returns_all_wavevectors(self):
        """structure_factor must return exactly 8 wavevectors."""
        psi = np.zeros(2 ** 8)
        psi[0] = 1.0
        Sq = structure_factor(psi, rows=2, cols=4)
        assert len(Sq) == 8, f"Expected 8 wavevectors, got {len(Sq)}"

    def test_structure_factor_ferromagnetic_state_max_at_00(self):
        """Ferromagnetic state |↑↑↑↑↑↑↑↑⟩: S(q) must peak at q=(0, 0)."""
        n = 8
        psi = np.zeros(2 ** n)
        psi[0] = 1.0  # all spin-up
        Sq = structure_factor(psi, rows=2, cols=4)
        max_q = max(Sq, key=Sq.get)
        assert max_q == (0.0, 0.0), (
            f"Ferromagnet should peak at (0,0), got {max_q}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# 4. State & Subsystem Entanglement Sanity
# ═══════════════════════════════════════════════════════════════════════════════

class TestStateAndEntanglement:
    """Tests on state normalisation, entropy, 1-RDMs, and Bloch vectors."""

    def test_ground_state_normalisation(self):
        """Ground state vector must satisfy ‖ψ‖² = 1 ± 1e-7."""
        for n, g in [(4, 1.0), (6, 0.5), (4, 5.0)]:
            H = build_tfim(n, g=g, J=1.0)
            _, psi, _ = ground_state(H, n, sector="even")
            norm2 = float(np.dot(psi, psi))
            assert abs(norm2 - 1.0) < 1e-7, (
                f"n={n}, g={g}: ‖ψ‖² = {norm2:.10f}"
            )

    def test_product_state_entropy_zero(self):
        """All-up product state |00...0⟩: half_chain_entropy must be 0."""
        for n in [2, 4, 6]:
            psi = np.zeros(2 ** n)
            psi[0] = 1.0
            S = half_chain_entropy(psi, n)
            assert abs(S) < 1e-10, f"n={n}: S={S:.3e}, expected 0"

    def test_bell_state_entropy_one(self):
        """Bell state (|00⟩+|11⟩)/√2 on n=2: entropy must equal 1.0."""
        psi = np.zeros(4)
        psi[0] = 1.0 / np.sqrt(2)   # |00⟩
        psi[3] = 1.0 / np.sqrt(2)   # |11⟩
        S = half_chain_entropy(psi, 2)
        assert abs(S - 1.0) < 1e-10, f"Bell entropy = {S:.12f}, expected 1.0"

    def test_rdm_trace_hermitian_psd(self):
        """Every 1-RDM must satisfy Tr=1, ρ=ρ†, λ_min ≥ -1e-10."""
        H = build_tfim(4, g=1.0)
        _, psi, _ = ground_state(H, 4, sector="even")
        for i in range(4):
            rho = one_rdm(psi, 4, i)
            # Trace
            tr = float(np.real(np.trace(rho)))
            assert abs(tr - 1.0) < 1e-10, f"qubit {i}: Tr(ρ)={tr:.12f}"
            # Hermiticity
            herm_err = float(np.max(np.abs(rho - rho.conj().T)))
            assert herm_err < 1e-12, f"qubit {i}: non-Hermitian error={herm_err:.3e}"
            # PSD
            lmin = float(np.linalg.eigvalsh(rho)[0])
            assert lmin >= -1e-10, f"qubit {i}: λ_min={lmin:.3e}"

    def test_bloch_y_zero_for_real_ground_states(self):
        """For real ground states, ⟨Y_i⟩ = Tr(Y ρ_i) must be 0 ± 1e-12."""
        for n, g in [(4, 0.5), (4, 1.0), (4, 2.0)]:
            H = build_tfim(n, g=g)
            _, psi, _ = ground_state(H, n, sector="even")
            for i in range(n):
                rho = one_rdm(psi, n, i)
                bv = bloch_vector(rho)
                assert abs(bv[1]) < 1e-12, (
                    f"n={n}, g={g}, qubit {i}: ⟨Y⟩={bv[1]:.3e}, expected 0"
                )

    def test_entropy_increases_toward_critical_point(self):
        """Entanglement entropy should be larger near the critical point (g≈1)."""
        H_para = build_tfim(6, g=5.0)
        H_crit = build_tfim(6, g=1.0)
        _, psi_para, _ = ground_state(H_para, 6, sector="even")
        _, psi_crit, _ = ground_state(H_crit, 6, sector="even")
        S_para = half_chain_entropy(psi_para, 6)
        S_crit = half_chain_entropy(psi_crit, 6)
        assert S_crit > S_para, (
            f"Entropy at critical point ({S_crit:.4f}) should exceed "
            f"deep paramagnetic ({S_para:.4f})"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# 5. Kernel Mathematical Integrity
# ═══════════════════════════════════════════════════════════════════════════════

class TestKernelIntegrity:
    """Verify mathematical properties of fidelity and PQK Gram matrices."""

    @pytest.fixture(scope="class")
    @classmethod
    def states_and_rdms(cls):
        """Pre-compute states for n=4, g in {0.5, 1.0, 2.0, 4.0}."""
        g_vals = [0.5, 1.0, 2.0, 4.0]
        n = 4
        states = []
        rdms_list = []
        for g in g_vals:
            H = build_tfim(n, g=g)
            _, psi, _ = ground_state(H, n, sector="even")
            states.append(psi)
            rdms_list.append([one_rdm(psi, n, k) for k in range(n)])
        return states, rdms_list

    def test_fq_symmetry(self, states_and_rdms):
        """K^FQ must be symmetric."""
        states, _ = states_and_rdms
        K = fidelity_gram(states)
        assert np.allclose(K, K.T, atol=1e-12), "K^FQ is not symmetric"

    def test_fq_diagonal_ones(self, states_and_rdms):
        """K^FQ diagonal must equal 1.0 (normalised states)."""
        states, _ = states_and_rdms
        K = fidelity_gram(states)
        assert np.allclose(np.diag(K), 1.0, atol=1e-12), (
            f"K^FQ diagonal: {np.diag(K)}"
        )

    def test_fq_psd(self, states_and_rdms):
        """K^FQ must be positive semi-definite (λ_min ≥ -1e-9)."""
        states, _ = states_and_rdms
        K = fidelity_gram(states)
        lmin = float(np.linalg.eigvalsh(K)[0])
        assert lmin >= -1e-9, f"K^FQ λ_min = {lmin:.3e}"

    def test_pqk_symmetry(self, states_and_rdms):
        """K^PQ must be symmetric."""
        _, rdms_list = states_and_rdms
        K = pqk_gram(rdms_list)
        assert np.allclose(K, K.T, atol=1e-12), "K^PQ is not symmetric"

    def test_pqk_diagonal_ones(self, states_and_rdms):
        """K^PQ diagonal must equal 1.0."""
        _, rdms_list = states_and_rdms
        K = pqk_gram(rdms_list)
        assert np.allclose(np.diag(K), 1.0, atol=1e-12), (
            f"K^PQ diagonal: {np.diag(K)}"
        )

    def test_pqk_psd(self, states_and_rdms):
        """K^PQ must be positive semi-definite (λ_min ≥ -1e-9)."""
        _, rdms_list = states_and_rdms
        K = pqk_gram(rdms_list)
        lmin = float(np.linalg.eigvalsh(K)[0])
        assert lmin >= -1e-9, f"K^PQ λ_min = {lmin:.3e}"

    def test_kta_range(self, states_and_rdms):
        """KTA score must be finite and bounded."""
        states, _ = states_and_rdms
        K = fidelity_gram(states)
        y = np.array([1.0, 1.0, -1.0, -1.0])
        score = kta(K, y)
        assert np.isfinite(score), f"KTA is not finite: {score}"

    def test_off_diagonal_variance_nonneg(self, states_and_rdms):
        """Off-diagonal variance must be non-negative."""
        states, _ = states_and_rdms
        K = fidelity_gram(states)
        v = off_diagonal_variance(K)
        assert v >= 0.0, f"Variance={v} < 0"

    def test_classical_features_shapes(self, states_and_rdms):
        """classical_features must return the correct number of features."""
        states, _ = states_and_rdms
        psi, n = states[0], 4
        assert classical_features(psi, n, mode="1pt_X").shape == (n,)
        assert classical_features(psi, n, mode="1pt_xyz").shape == (3 * n,)
        assert classical_features(psi, n, mode="2pt_all_pairs").shape == (n * (n - 1) // 2,)
        full = classical_features(psi, n, mode="full_corr")
        expected = 3 * n + n * (n - 1) // 2
        assert full.shape == (expected,), f"full_corr shape {full.shape}, expected ({expected},)"


# ═══════════════════════════════════════════════════════════════════════════════
# 6. Physical Asymptotics
# ═══════════════════════════════════════════════════════════════════════════════

class TestPhysicalAsymptotics:
    """
    Verify qualitative correctness in the deep paramagnetic and ferromagnetic
    phases.

    Tolerances: atol = 1e-2 (except where noted).

    Note on |⟨ZZ⟩| < 0.1 at g=10:
        For n=4 finite systems, first-order perturbation theory gives
        |⟨ZZ⟩| ~ J/(2g) ≈ 0.05.  The test asserts |ZZ| < 0.1 (1 order of
        magnitude smaller than J=1), confirming the paramagnetic regime.
    """

    def test_large_g_paramagnetic_x_close_to_1(self):
        """
        At g=10.0 (J=1), all ⟨X_i⟩ should be close to 1.0 within 1e-2.
        """
        n = 4
        H = build_tfim(n, g=10.0, J=1.0, boundary="open")
        _, psi, _ = ground_state(H, n, sector="even")
        x_vals = expect_x(psi, n)
        for i, xi in enumerate(x_vals):
            assert abs(xi - 1.0) < 1e-2, (
                f"g=10: ⟨X_{i}⟩ = {xi:.6f}, expected ≈ 1.0 (within 1e-2)"
            )

    def test_large_g_paramagnetic_zz_small(self):
        """
        At g=10.0 (J=1), |⟨Z_i Z_{i+1}⟩| should be much smaller than 1.
        In the thermodynamic limit J/g → 0; for n=4, |ZZ| ~ J/(2g) ≈ 0.05.
        Threshold: < 0.1 (demonstrating paramagnetic regime).
        """
        n = 4
        H = build_tfim(n, g=10.0, J=1.0, boundary="open")
        _, psi, _ = ground_state(H, n, sector="even")
        for i in range(n - 1):
            zz = abs(expect_zz(psi, n, i, i + 1))
            assert zz < 0.1, (
                f"g=10: |⟨Z_{i}Z_{i+1}⟩| = {zz:.6f}, expected < 0.1"
            )

    def test_small_g_ferromagnetic_zz_close_to_1(self):
        """
        At g=0.05, J=1 with symmetry_break=1e-4: |⟨Z_i Z_{i+1}⟩| ≈ 1.0
        (within 1e-2), confirming the ferromagnetic ordered phase.
        """
        n = 4
        H = build_tfim(n, g=0.05, J=1.0, boundary="open")
        _, psi, _ = ground_state(H, n, sector="even", symmetry_break=1e-4)
        for i in range(n - 1):
            zz = abs(expect_zz(psi, n, i, i + 1))
            assert abs(zz - 1.0) < 1e-2, (
                f"g=0.05: |⟨Z_{i}Z_{i+1}⟩| = {zz:.6f}, expected ≈ 1.0"
            )

    def test_gap_is_positive(self):
        """ground_state must return a positive spectral gap in even sector."""
        for g in [0.5, 1.0, 2.0]:
            H = build_tfim(4, g=g)
            _, _, gap = ground_state(H, 4, sector="even")
            assert gap > 1e-9, f"g={g}: gap={gap:.3e} ≤ 1e-9"

    def test_energy_ordering(self):
        """
        E0(g=10) < E0(g=1) < E0(g=0.1) for n=4 open TFIM.
        Larger transverse field lowers the ground-state energy (more negative).
        """
        n = 4
        energies = {}
        for g in [0.1, 1.0, 10.0]:
            H = build_tfim(n, g=g)
            E0, _, _ = ground_state(H, n, sector="even")
            energies[g] = E0
        assert energies[10.0] < energies[1.0] < energies[0.1], (
            f"Energy ordering unexpected: {energies}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# 7. Noise Channel Limits
# ═══════════════════════════════════════════════════════════════════════════════

class TestNoise:
    """Tests for depolarisation and shot-noise simulation."""

    @pytest.fixture
    def sample_rho(self):
        """A generic mixed-state 2×2 density matrix."""
        rho = np.array([[0.75, 0.25 + 0.05j],
                        [0.25 - 0.05j, 0.25]], dtype=complex)
        return rho

    def test_depolarize_p0_identity(self, sample_rho):
        """depolarize_rdm(ρ, p=0) must return ρ unchanged."""
        rho_out = depolarize_rdm(sample_rho, p=0.0)
        assert np.allclose(rho_out, sample_rho, atol=1e-14), (
            "depolarize(p=0) changed ρ"
        )

    def test_depolarize_p1_maximally_mixed(self, sample_rho):
        """depolarize_rdm(ρ, p=1) must return I₂/2."""
        rho_out = depolarize_rdm(sample_rho, p=1.0)
        expected = np.eye(2, dtype=complex) / 2.0
        assert np.allclose(rho_out, expected, atol=1e-14), (
            f"depolarize(p=1) = {rho_out}, expected I/2"
        )

    def test_depolarize_interpolation(self, sample_rho):
        """Intermediate p interpolates correctly."""
        p = 0.5
        rho_out = depolarize_rdm(sample_rho, p=p)
        expected = 0.5 * sample_rho + 0.5 * np.eye(2, dtype=complex) / 2.0
        assert np.allclose(rho_out, expected, atol=1e-14)

    def test_depolarize_preserves_trace(self, sample_rho):
        """Trace must be preserved by depolarisation."""
        for p in [0.0, 0.3, 0.7, 1.0]:
            rho_out = depolarize_rdm(sample_rho, p=p)
            tr = float(np.real(np.trace(rho_out)))
            assert abs(tr - 1.0) < 1e-14, f"p={p}: Tr(ε(ρ))={tr}"

    def test_shot_noise_pqk_shape(self):
        """shot_noise_pqk must return a square matrix of correct size."""
        n, m = 4, 3
        H_list = [build_tfim(n, g=g) for g in [0.5, 1.0, 2.0]]
        psis = [ground_state(H, n, sector="even")[1] for H in H_list]
        rdms_list = [[one_rdm(psi, n, k) for k in range(n)] for psi in psis]
        rng = np.random.default_rng(42)
        K_noisy = shot_noise_pqk(rdms_list, shots=100, rng=rng)
        assert K_noisy.shape == (m, m), f"Shape {K_noisy.shape}, expected ({m},{m})"

    def test_shot_noise_pqk_diagonal_near_one(self):
        """Diagonal of shot-noisy PQK must be ≈ 1.0 (exp(-0) = 1 exactly)."""
        n = 4
        H_list = [build_tfim(n, g=g) for g in [0.5, 1.0, 2.0]]
        psis = [ground_state(H, n, sector="even")[1] for H in H_list]
        rdms_list = [[one_rdm(psi, n, k) for k in range(n)] for psi in psis]
        rng = np.random.default_rng(7)
        K_noisy = shot_noise_pqk(rdms_list, shots=1000, rng=rng)
        # Diagonal: identical states give dist²=0, so exp(-0)=1 exactly
        assert np.allclose(np.diag(K_noisy), 1.0, atol=1e-12)

    def test_shot_noise_fidelity_shape_and_diagonal(self):
        """shot_noise_fidelity returns correct shape and diagonal=1."""
        n, m = 4, 3
        H_list = [build_tfim(n, g=g) for g in [0.5, 1.0, 2.0]]
        psis = [ground_state(H, n, sector="even")[1] for H in H_list]
        from kernels import fidelity_gram
        K = fidelity_gram(psis)
        rng = np.random.default_rng(99)
        K_noisy, lam_min = shot_noise_fidelity(K, shots=500, rng=rng)
        assert K_noisy.shape == (m, m)
        assert np.allclose(np.diag(K_noisy), 1.0, atol=1e-12)
        assert isinstance(lam_min, float)

    def test_shot_noise_fidelity_symmetry(self):
        """shot_noise_fidelity must return a symmetric matrix."""
        n = 4
        H_list = [build_tfim(n, g=g) for g in [0.5, 1.0, 2.0]]
        psis = [ground_state(H, n, sector="even")[1] for H in H_list]
        from kernels import fidelity_gram
        K = fidelity_gram(psis)
        rng = np.random.default_rng(0)
        K_noisy, _ = shot_noise_fidelity(K, shots=200, rng=rng)
        assert np.allclose(K_noisy, K_noisy.T, atol=1e-14)

    def test_shot_noise_convergence_with_shots(self):
        """
        As shots → ∞, noisy PQK should converge to the noiseless PQK.
        Compare 100 vs 10000 shots: 10000-shot version should be closer.
        """
        n = 4
        H_list = [build_tfim(n, g=g) for g in [0.5, 1.0, 2.0]]
        psis = [ground_state(H, n, sector="even")[1] for H in H_list]
        rdms_list = [[one_rdm(psi, n, k) for k in range(n)] for psi in psis]
        K_exact = pqk_gram(rdms_list)

        rng = np.random.default_rng(2024)
        K_low = shot_noise_pqk(rdms_list, shots=100, rng=rng)
        rng2 = np.random.default_rng(2025)
        K_high = shot_noise_pqk(rdms_list, shots=10000, rng=rng2)

        err_low = np.linalg.norm(K_low - K_exact, "fro")
        err_high = np.linalg.norm(K_high - K_exact, "fro")
        assert err_high < err_low, (
            f"High-shot error ({err_high:.4f}) ≥ low-shot error ({err_low:.4f})"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Additional edge-case tests
# ═══════════════════════════════════════════════════════════════════════════════

class TestEdgeCases:
    """Edge cases and boundary conditions."""

    def test_n2_open_energy(self):
        """n=2 open TFIM: verify ground energy by direct 4×4 diagonalisation."""
        g = 1.0
        H = build_tfim(2, g=g, J=1.0, boundary="open")
        E0_gs, _, _ = ground_state(H, 2, sector="even")
        H_dense = H.toarray()
        evals = scipy.linalg.eigh(H_dense, eigvals_only=True)
        assert abs(E0_gs - float(evals[0])) < 1e-10

    def test_custom_couplings_open(self):
        """Custom coupling list must be accepted without error."""
        couplings = [0.5, 1.0, 1.5]
        H = build_tfim(4, g=1.0, J=1.0, boundary="open", couplings=couplings)
        assert H.shape == (16, 16)

    def test_custom_couplings_periodic(self):
        """Custom periodic coupling list length n."""
        couplings = [0.5, 1.0, 1.5, 0.8]
        H = build_tfim(4, g=1.0, J=1.0, boundary="periodic", couplings=couplings)
        assert H.shape == (16, 16)

    def test_custom_fields(self):
        """Custom field list must be accepted."""
        fields = [0.5, 1.0, 1.5, 2.0]
        H = build_tfim(4, g=1.0, J=1.0, boundary="open", fields=fields)
        assert H.shape == (16, 16)

    def test_wrong_coupling_length_raises(self):
        """Wrong coupling length must raise AssertionError."""
        with pytest.raises(AssertionError):
            build_tfim(4, g=1.0, J=1.0, boundary="open", couplings=[1.0, 2.0])

    def test_wrong_field_length_raises(self):
        """Wrong field length must raise AssertionError."""
        with pytest.raises(AssertionError):
            build_tfim(4, g=1.0, J=1.0, boundary="open", fields=[1.0, 2.0])

    def test_correlation_matrix_diagonal_is_one(self):
        """C_{ii} = ⟨Z_i²⟩ = 1 for any normalised state."""
        H = build_tfim(4, g=1.0)
        _, psi, _ = ground_state(H, 4, sector="even")
        C = correlation_matrix(psi, 4)
        assert np.allclose(np.diag(C), 1.0, atol=1e-10), (
            f"Diagonal of correlation matrix: {np.diag(C)}"
        )

    def test_correlation_matrix_symmetric(self):
        """Correlation matrix must be symmetric: C_{ij} = C_{ji}."""
        H = build_tfim(4, g=1.0)
        _, psi, _ = ground_state(H, 4, sector="even")
        C = correlation_matrix(psi, 4)
        assert np.allclose(C, C.T, atol=1e-10)

    def test_symmetry_break_lifts_degeneracy(self):
        """With symmetry_break > 0, ground state should have definite Z orientation."""
        n = 4
        H = build_tfim(n, g=0.1, J=1.0, boundary="open")
        _, psi_sym, _ = ground_state(H, n, sector="even", symmetry_break=0.0)
        _, psi_broken, _ = ground_state(H, n, sector="even", symmetry_break=0.01)
        # Broken state should have non-zero total magnetisation ∑<Z_i>
        zz_broken = [expect_zz(psi_broken, n, i, i) for i in range(n)]  # <Z_i^2>=1, meaningless
        # Better: check <Z_i> for first site via Bloch vector
        rho0_broken = one_rdm(psi_broken, n, 0)
        bv_broken = bloch_vector(rho0_broken)
        rho0_sym = one_rdm(psi_sym, n, 0)
        bv_sym = bloch_vector(rho0_sym)
        # In even sector, <Z_0> = 0 by symmetry; with breaking, |bv_z| > 0
        assert abs(bv_broken[2]) > abs(bv_sym[2]), (
            f"|Z| broken={abs(bv_broken[2]):.4f}, symmetric={abs(bv_sym[2]):.4f}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Phase 1.5 — Sparse Parity Sector, 2-Local PQK, Mathematical Identity Tests
# ═══════════════════════════════════════════════════════════════════════════════

import time
import tracemalloc
from kernels import two_rdm, pqk_gram_2local


class TestMathematicalIdentities:
    """
    Mathematical identity and structural proofs for Z_2-even sector states.
    """

    def test_z2_sector_bloch_z_zero(self):
        """
        In the Z_2-even parity sector, ⟨Z_k⟩ = Tr(Z ρ_k) = 0 for all sites k.

        Proof sketch: P = ⊗X_i commutes with H and has eigenvalue +1 on the
        ground state. Since P Z_k P^{-1} = -Z_k, we have
        ⟨ψ|Z_k|ψ⟩ = ⟨ψ|P^{-1}P Z_k P^{-1}P|ψ⟩ = -⟨ψ|Z_k|ψ⟩ = 0.
        """
        for n, g in [(4, 0.5), (4, 1.0), (6, 1.0)]:
            H = build_tfim(n, g=g)
            _, psi, _ = ground_state(H, n, sector="even")
            for k in range(n):
                rho = one_rdm(psi, n, k)
                bv = bloch_vector(rho)
                assert abs(bv[2]) < 1e-10, (
                    f"n={n}, g={g}, site {k}: ⟨Z⟩ = {bv[2]:.3e} ≠ 0"
                )

    def test_z2_sector_bloch_y_zero(self):
        """
        For real ground states in the even sector, Tr(Y ρ_k) = 0.
        """
        for n, g in [(4, 1.0), (6, 2.0)]:
            H = build_tfim(n, g=g)
            _, psi, _ = ground_state(H, n, sector="even")
            for k in range(n):
                rho = one_rdm(psi, n, k)
                bv = bloch_vector(rho)
                assert abs(bv[1]) < 1e-10, (
                    f"n={n}, g={g}, site {k}: ⟨Y⟩ = {bv[1]:.3e} ≠ 0"
                )

    def test_rdm_form_in_even_sector(self):
        """
        In the Z_2-even sector, ρ_k = (I + x_k X) / 2.
        Verify: off-diagonal elements of ρ_k are purely real, diagonal is 1/2,
        and ρ_k[0,1] = ρ_k[1,0] = x_k/2.
        """
        n, g = 4, 1.0
        H = build_tfim(n, g=g)
        _, psi, _ = ground_state(H, n, sector="even")
        for k in range(n):
            rho = one_rdm(psi, n, k)
            # Diagonal must equal 1/2
            assert abs(np.real(rho[0, 0]) - 0.5) < 1e-10
            assert abs(np.real(rho[1, 1]) - 0.5) < 1e-10
            # Imaginary parts vanish (real state, no Y component)
            assert abs(np.imag(rho[0, 1])) < 1e-10
            assert abs(np.imag(rho[1, 0])) < 1e-10
            # Off-diagonals equal x_k/2
            bv = bloch_vector(rho)
            assert abs(np.real(rho[0, 1]) - bv[0] / 2) < 1e-10

    def test_pqk_equals_rbf_kernel(self):
        """
        Verify: pqk_gram(rdms_list, gamma) ≡ rbf_kernel(X_bloch, gamma=gamma/2)
        within 1e-10.

        Derivation:
            ‖ρ_k^i - ρ_k^j‖_F² = ½ ‖b_k^i - b_k^j‖²
        therefore
            K^PQ(γ) = exp(-γ ∑_k ‖ρ_k^i-ρ_k^j‖_F²)
                     = exp(-γ/2 · ‖concat(b^i)-concat(b^j)‖²)
                     = RBF(X, gamma=γ/2).
        """
        from sklearn.metrics.pairwise import rbf_kernel as sklearn_rbf

        n = 4
        g_vals = [0.5, 1.0, 2.0, 4.0]
        gamma = 3.0

        rdms_list = []
        bloch_features = []
        for gv in g_vals:
            H = build_tfim(n, g=gv)
            _, psi, _ = ground_state(H, n, sector="even")
            rdms = [one_rdm(psi, n, k) for k in range(n)]
            rdms_list.append(rdms)
            bvs = np.concatenate([bloch_vector(r) for r in rdms])
            bloch_features.append(bvs)

        K_pqk = pqk_gram(rdms_list, gamma=gamma)
        X_feat = np.array(bloch_features)
        K_rbf = sklearn_rbf(X_feat, gamma=gamma / 2.0)

        max_diff = float(np.max(np.abs(K_pqk - K_rbf)))
        assert max_diff < 1e-10, (
            f"PQK ≠ RBF: max diff = {max_diff:.3e}"
        )


class TestSparseParitySector:
    """
    Verify sparse parity-sector solver against dense reference diagonalisation.
    """

    def _dense_ground_energy(self, H, n):
        """Return the exact ground energy via dense diagonalisation."""
        evals = scipy.linalg.eigh(H.toarray(), eigvals_only=True)
        return float(evals[0])

    def test_sparse_vs_dense_n6(self):
        """
        n=6 periodic TFIM: sparse sector solver energy and state overlap match
        dense eigh to within 1e-10.
        """
        n = 6
        H = build_tfim(n, g=1.0, J=1.0, boundary="periodic")

        # Sparse sector result
        E0_sparse, psi_sparse, _ = ground_state(H, n, sector="even")

        # Dense reference
        H_arr = H.toarray().real
        evals, evecs = scipy.linalg.eigh(H_arr)
        E0_dense = float(evals[0])
        psi_dense = evecs[:, 0].astype(float)

        assert abs(E0_sparse - E0_dense) < 1e-10, (
            f"n=6 energy: sparse={E0_sparse:.14f}, dense={E0_dense:.14f}"
        )
        overlap = abs(float(np.dot(psi_sparse, psi_dense)))
        assert overlap > 1 - 1e-10, (
            f"n=6 state overlap={overlap:.12f}, expected > 1-1e-10"
        )

    def test_sparse_vs_dense_n8(self):
        """
        n=8 open TFIM: sparse sector solver energy and state overlap match
        dense eigh to within 1e-10.
        """
        n = 8
        H = build_tfim(n, g=1.0, J=1.0, boundary="open")

        E0_sparse, psi_sparse, _ = ground_state(H, n, sector="even")

        H_arr = H.toarray().real
        evals, evecs = scipy.linalg.eigh(H_arr)
        E0_dense = float(evals[0])
        psi_dense = evecs[:, 0].astype(float)

        assert abs(E0_sparse - E0_dense) < 1e-10, (
            f"n=8 energy: sparse={E0_sparse:.14f}, dense={E0_dense:.14f}"
        )
        overlap = abs(float(np.dot(psi_sparse, psi_dense)))
        assert overlap > 1 - 1e-10, (
            f"n=8 state overlap={overlap:.12f}"
        )

    def test_sector_basis_is_orthonormal(self):
        """V^T V = I (sparse sector basis is orthonormal)."""
        from hamiltonians import _build_sector_basis
        for n in [4, 6, 8]:
            V = _build_sector_basis(n, sector="even")
            VtV = (V.T @ V).toarray()
            id_ref = np.eye(V.shape[1])
            assert np.allclose(VtV, id_ref, atol=1e-12), (
                f"n={n}: V^T V is not identity (max err = "
                f"{np.max(np.abs(VtV - id_ref)):.3e})"
            )

    def test_sector_basis_spans_parity_sector(self):
        """V V^T projects onto the +1 eigenspace of P = ⊗ X_i."""
        import scipy.sparse as _sp
        from hamiltonians import _build_sector_basis, _build_parity_op
        for n in [4, 6]:
            V = _build_sector_basis(n, sector="even")
            P = _build_parity_op(n)
            # For any column v of V, P v = +v
            V_dense = V.toarray()
            P_dense = P.toarray().real
            PV = P_dense @ V_dense
            diff = np.max(np.abs(PV - V_dense))
            assert diff < 1e-10, (
                f"n={n}: P V ≠ V (max diff = {diff:.3e})"
            )

    def test_two_site_op_same_site_identity(self):
        """
        _two_site_op(Z, k, Z, k, n) must equal the identity (Z² = I).
        After the Phase 1.5 fix this should hold for all sites.
        """
        from hamiltonians import _two_site_op, _Z
        import scipy.sparse as _sp
        n = 4
        I_full = _sp.eye(2 ** n, format="csr", dtype=complex)
        for k in range(n):
            ZZ_kk = _two_site_op(_Z, k, _Z, k, n)
            diff = (ZZ_kk - I_full).data
            max_err = float(np.max(np.abs(diff))) if len(diff) > 0 else 0.0
            assert max_err < 1e-14, (
                f"Site {k}: Z_k Z_k ≠ I (max err = {max_err:.3e})"
            )


class TestLargeScalePerformance:
    """
    Memory and timing benchmark for n=14 ground-state computation.
    Asserts completion within 60 s and RAM usage < 4 GB.
    """

    def test_n14_ground_state_memory_and_time(self):
        """
        n=14 open TFIM: sparse sector solver must finish in < 60 s and use
        < 4 GB of RAM (peak tracemalloc allocation).
        """
        n = 14

        tracemalloc.start()
        t_start = time.time()

        H = build_tfim(n, g=1.0, J=1.0, boundary="open")
        E0, psi, gap = ground_state(H, n, sector="even")

        elapsed = time.time() - t_start
        _, peak_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        peak_gb = peak_bytes / 1e9

        assert elapsed < 60.0, (
            f"n=14 took {elapsed:.2f}s, expected < 60s"
        )
        assert peak_gb < 4.0, (
            f"n=14 used {peak_gb:.2f} GB peak RAM, expected < 4 GB"
        )
        # Sanity: energy should be negative and roughly -n
        assert E0 < 0.0, f"E0={E0:.4f} should be negative"
        assert abs(psi @ psi - 1.0) < 1e-7, "psi not normalised"
        assert gap > 1e-9, f"gap={gap:.3e} too small"


class TestFirstOrderPerturbationAsymptotics:
    """
    First-order perturbation theory: at g >> J,
    ⟨Z_i Z_{i+1}⟩ ≈ J/(2g) to leading order.
    """

    def test_nn_zz_first_order_at_large_g(self):
        """
        n=8, J=1, g=20 (open boundary):
        ⟨Z_i Z_{i+1}⟩ ≈ J/(2g) = 0.025 within 10% relative error for
        all nearest-neighbour bonds.

        First-order perturbation theory:
            ⟨0|Z_i Z_{i+1}|0⟩^{(1)} = J/(2g) + O(J/g)^2
        """
        n = 8
        g = 20.0
        J = 1.0
        expected = J / (2.0 * g)   # = 0.025

        H = build_tfim(n, g=g, J=J, boundary="open")
        _, psi, _ = ground_state(H, n, sector="even")

        for i in range(n - 1):
            zz = expect_zz(psi, n, i, i + 1)
            rel_err = abs(zz - expected) / expected
            assert rel_err < 0.10, (
                f"Bond ({i},{i+1}): ⟨ZZ⟩={zz:.6f}, expected≈{expected:.6f}, "
                f"rel_err={rel_err*100:.2f}% > 10%"
            )

    def test_large_g_x_expectation_perturbative(self):
        """
        At g=20 (J=1), ⟨X_i⟩ = 1 - J²/(8g²) + O(J/g)^4.
        For n=8, verify the correction is small: ⟨X_i⟩ > 0.99.
        """
        n = 8
        H = build_tfim(n, g=20.0, J=1.0, boundary="open")
        _, psi, _ = ground_state(H, n, sector="even")
        x_vals = expect_x(psi, n)
        for i, xi in enumerate(x_vals):
            assert xi > 0.99, (
                f"g=20: ⟨X_{i}⟩={xi:.6f} < 0.99"
            )


class TestTwoLocalPQK:
    """
    Verify the 2-local PQK kernel properties: symmetry, PSD, unit diagonal.
    """

    @pytest.fixture(scope="class")
    @classmethod
    def psi_list_and_n(cls):
        n = 4
        g_vals = [0.5, 1.0, 2.0, 4.0]
        psis = []
        for gv in g_vals:
            H = build_tfim(n, g=gv)
            _, psi, _ = ground_state(H, n, sector="even")
            psis.append(psi)
        return psis, n

    def test_pqk2_nn_symmetry(self, psi_list_and_n):
        """K^{PQ2} (nearest-neighbour) must be symmetric."""
        psi_list, n = psi_list_and_n
        K = pqk_gram_2local(psi_list, n, pairs="nn")
        assert np.allclose(K, K.T, atol=1e-12), "K^PQ2 (nn) is not symmetric"

    def test_pqk2_nn_diagonal_ones(self, psi_list_and_n):
        """K^{PQ2} diagonal must equal 1.0 (exp(-γ·0) = 1)."""
        psi_list, n = psi_list_and_n
        K = pqk_gram_2local(psi_list, n, pairs="nn")
        assert np.allclose(np.diag(K), 1.0, atol=1e-12), (
            f"K^PQ2 diagonal: {np.diag(K)}"
        )

    def test_pqk2_nn_psd(self, psi_list_and_n):
        """K^{PQ2} (nearest-neighbour) must be positive semi-definite."""
        psi_list, n = psi_list_and_n
        K = pqk_gram_2local(psi_list, n, pairs="nn")
        lmin = float(np.linalg.eigvalsh(K)[0])
        assert lmin >= -1e-9, f"K^PQ2 (nn) λ_min = {lmin:.3e}"

    def test_pqk2_all_symmetry(self, psi_list_and_n):
        """K^{PQ2} (all pairs) must be symmetric."""
        psi_list, n = psi_list_and_n
        K = pqk_gram_2local(psi_list, n, pairs="all")
        assert np.allclose(K, K.T, atol=1e-12), "K^PQ2 (all) is not symmetric"

    def test_pqk2_all_diagonal_ones(self, psi_list_and_n):
        """K^{PQ2} (all pairs) diagonal must equal 1.0."""
        psi_list, n = psi_list_and_n
        K = pqk_gram_2local(psi_list, n, pairs="all")
        assert np.allclose(np.diag(K), 1.0, atol=1e-12)

    def test_pqk2_all_psd(self, psi_list_and_n):
        """K^{PQ2} (all pairs) must be positive semi-definite."""
        psi_list, n = psi_list_and_n
        K = pqk_gram_2local(psi_list, n, pairs="all")
        lmin = float(np.linalg.eigvalsh(K)[0])
        assert lmin >= -1e-9, f"K^PQ2 (all) λ_min = {lmin:.3e}"

    def test_two_rdm_trace_one(self, psi_list_and_n):
        """Tr(ρ_{ij}) = 1 for all 2-site RDMs."""
        psi_list, n = psi_list_and_n
        for psi in psi_list:
            for i in range(n):
                for j in range(i + 1, n):
                    rho = two_rdm(psi, n, i, j)
                    tr = float(np.real(np.trace(rho)))
                    assert abs(tr - 1.0) < 1e-10, (
                        f"Tr(ρ_{{{i},{j}}}) = {tr:.12f}"
                    )

    def test_two_rdm_hermitian(self, psi_list_and_n):
        """ρ_{ij} must be Hermitian."""
        psi_list, n = psi_list_and_n
        for psi in psi_list:
            for i, j in [(0, 1), (1, 3), (0, 3)]:
                rho = two_rdm(psi, n, i, j)
                herm_err = float(np.max(np.abs(rho - rho.conj().T)))
                assert herm_err < 1e-12, (
                    f"ρ_{{{i},{j}}} non-Hermitian err = {herm_err:.3e}"
                )

    def test_two_rdm_psd(self, psi_list_and_n):
        """ρ_{ij} must be positive semi-definite (λ_min ≥ -1e-10)."""
        psi_list, n = psi_list_and_n
        for psi in psi_list:
            for i in range(n):
                for j in range(i + 1, n):
                    rho = two_rdm(psi, n, i, j)
                    lmin = float(np.linalg.eigvalsh(rho)[0])
                    assert lmin >= -1e-10, (
                        f"ρ_{{{i},{j}}} λ_min = {lmin:.3e}"
                    )

    def test_two_rdm_marginals_consistent_with_one_rdm(self, psi_list_and_n):
        """
        Partial trace of ρ_{ij} over site j must equal ρ_i (1-RDM).
        """
        psi_list, n = psi_list_and_n
        for psi in psi_list:
            for i in range(n):
                for j in range(i + 1, n):
                    rho_2 = two_rdm(psi, n, i, j)
                    # Partial trace over second subsystem (j):
                    # Reshape ρ_{ij} as (2,2,2,2) with axes (a_i, b_j, a'_i, b'_j)
                    # Sum over b_j == b'_j (axes 1 and 3)
                    rho_2_t = rho_2.reshape(2, 2, 2, 2)
                    rho_i_from_2 = np.einsum("abcb->ac", rho_2_t)
                    rho_i_direct = one_rdm(psi, n, i)
                    diff = np.max(np.abs(rho_i_from_2 - rho_i_direct))
                    assert diff < 1e-10, (
                        f"ρ_i from Tr_j(ρ_{{ij}}) mismatch: sites ({i},{j}), "
                        f"max diff = {diff:.3e}"
                    )

    def test_pqk2_nn_coarser_than_all(self, psi_list_and_n):
        """
        NN-pairs PQK uses fewer features than all-pairs PQK, so its entries
        should differ (unless states are identical up to NN correlations).
        """
        psi_list, n = psi_list_and_n
        K_nn = pqk_gram_2local(psi_list, n, pairs="nn")
        K_all = pqk_gram_2local(psi_list, n, pairs="all")
        # They should NOT be identical in general
        assert not np.allclose(K_nn, K_all), (
            "K^PQ2(nn) should differ from K^PQ2(all)"
        )

    def test_pqk2_invalid_pairs_raises(self, psi_list_and_n):
        """Invalid pairs argument must raise ValueError."""
        psi_list, n = psi_list_and_n
        with pytest.raises(ValueError, match="Unknown pairs mode"):
            pqk_gram_2local(psi_list, n, pairs="diagonal")
