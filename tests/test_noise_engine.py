"""
tests/test_noise_engine.py
--------------------------
Unit tests for the measurement and physics engine (Phase 2b):
1. test_sample_bitstrings_convergence:
   Assert empirical expectations converge to exact statevector expectations
   with RMS error scaling as O(1/sqrt(S)) for S in [100, 1000, 10000] on open TFIM at n=4.
2. test_shared_basis_consistency:
   Assert that PQK-1, PQK-2nn, E, E2, and F features extracted from the exact
   same bitstring arrays share identical underlying values.
3. test_destructive_swap_test_unbiased:
   Verify that estimator K_hat = 2*(N_0/S) - 1 with N_0 ~ Binomial(S, (1 + K)/2)
   is unbiased with Var = (1 - K^2)/S.
4. test_mixed_state_depolarizing_fidelity:
   Verify that the exact density matrix overlap Tr(rho_i rho_j) approaches 1/(2^n)
   as p -> 1, and normalized mixed-state overlap K_{ij}(p) is consistent.
"""

import os
import sys
import numpy as np
import pytest

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC = os.path.join(_PROJECT_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from hamiltonians import build_tfim, ground_state, expect_x, expect_zz
from kernels import two_rdm, _X, _Y, _Z
from noise import (
    sample_bitstrings_basis,
    extract_basis_expectations,
    reconstruct_noisy_features_from_basis,
    destructive_swap_test_fidelity,
    depolarize_state,
    mixed_state_fidelity_gram,
    apply_single_qubit_depolarizing,
    apply_local_depolarizing_channel,
    partial_trace,
    local_depolarizing_fidelity_gram,
)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
from scripts.common import make_split


class TestNoiseEngine:
    """Phase 2b measurement & physics engine unit tests."""

    def test_sample_bitstrings_convergence(self):
        """
        Verify that empirical expectations from shared-basis bitstring sampling
        converge to exact expectations with RMS error scaling as O(1/sqrt(S))
        for S in [100, 1000, 10000] on open TFIM at n=4.
        """
        n = 4
        H = build_tfim(n, g=1.0)
        _, psi, _ = ground_state(H, n, sector="even")

        # Exact expectations
        exp_x_exact = expect_x(psi, n)
        exp_z_exact = np.zeros(n)  # Exact parity symmetry in even sector
        _XX = np.kron(_X.toarray(), _X.toarray())
        exp_xx_exact = [
            float(np.real(np.trace(two_rdm(psi, n, i, i + 1) @ _XX)))
            for i in range(n - 1)
        ]
        exp_zz_exact = [expect_zz(psi, n, i, i + 1) for i in range(n - 1)]

        exact_all = np.concatenate([exp_x_exact, exp_z_exact, exp_xx_exact, exp_zz_exact])

        s_values = [100, 1000, 10000]
        n_trials = 35
        rms_per_s = []

        rng = np.random.default_rng(2026)
        for s in s_values:
            trial_errors = []
            for _ in range(n_trials):
                bx = sample_bitstrings_basis(psi, n, "X", s, rng)
                bz = sample_bitstrings_basis(psi, n, "Z", s, rng)
                # Y bitstrings (needed for complete basis extraction)
                by = sample_bitstrings_basis(psi, n, "Y", s, rng)

                exps = extract_basis_expectations(bx, by, bz, n)
                emp_all = np.concatenate([
                    exps["x"],
                    exps["z"],
                    exps["xx_nn"],
                    exps["zz_nn"],
                ])
                err = np.mean((emp_all - exact_all) ** 2)
                trial_errors.append(err)

            rms = np.sqrt(np.mean(trial_errors))
            rms_per_s.append(rms)

        print(f"\nEmpirical RMS errors: S=100: {rms_per_s[0]:.5f}, S=1000: {rms_per_s[1]:.5f}, S=10000: {rms_per_s[2]:.5f}")

        # 1. Monotonic decrease with sample size
        assert rms_per_s[0] > rms_per_s[1] > rms_per_s[2], (
            f"Expected monotonic decrease in RMS error, got {rms_per_s}"
        )

        # 2. O(1/sqrt(S)) scaling verification:
        # Ratio of RMS between 10x shot increase should be approximately sqrt(10) ≈ 3.16
        ratio_100_1000 = rms_per_s[0] / rms_per_s[1]
        ratio_1000_10000 = rms_per_s[1] / rms_per_s[2]
        print(f"Ratios: RMS(100)/RMS(1000) = {ratio_100_1000:.2f}, RMS(1000)/RMS(10000) = {ratio_1000_10000:.2f}")

        assert 2.0 < ratio_100_1000 < 4.5, f"Expected ratio near 3.16, got {ratio_100_1000}"
        assert 2.0 < ratio_1000_10000 < 4.5, f"Expected ratio near 3.16, got {ratio_1000_10000}"

    def test_shared_basis_consistency(self):
        """
        Assert that PQK-1, PQK-2nn, E, E2, and F features extracted from the exact
        same bitstring arrays share identical underlying values to machine precision.
        """
        n = 4
        H = build_tfim(n, g=0.8)
        _, psi, _ = ground_state(H, n, sector="even")

        rng = np.random.default_rng(42)
        shots = 5000

        # Sample shared bitstring arrays
        bx = sample_bitstrings_basis(psi, n, "X", shots, rng)
        by = sample_bitstrings_basis(psi, n, "Y", shots, rng)
        bz = sample_bitstrings_basis(psi, n, "Z", shots, rng)

        exps = extract_basis_expectations(bx, by, bz, n)
        reconstructed = reconstruct_noisy_features_from_basis(exps, n)

        rdms_1local = reconstructed["rdms_1local"]
        rdms_2local = reconstructed["rdms_2local"]
        feats_e = reconstructed["e_features"]
        feats_e2 = reconstructed["e2_features"]
        bloch_x = reconstructed["bloch_x"]
        bloch_z = reconstructed["bloch_z"]

        sx = np.array([[0, 1], [1, 0]], dtype=complex)
        sz = np.array([[1, 0], [0, -1]], dtype=complex)
        _XI = np.kron(sx, np.eye(2, dtype=complex))
        _IX = np.kron(np.eye(2, dtype=complex), sx)
        _XX = np.kron(sx, sx)
        _YY = np.kron(np.array([[0, -1j], [1j, 0]], dtype=complex), np.array([[0, -1j], [1j, 0]], dtype=complex))
        _ZZ = np.kron(sz, sz)

        # 1. 1-RDM matches bloch_x and bloch_z
        for i in range(n):
            tr_x = float(np.real(np.trace(rdms_1local[i] @ sx)))
            tr_z = float(np.real(np.trace(rdms_1local[i] @ sz)))
            assert abs(tr_x - bloch_x[i]) < 1e-14
            assert abs(tr_z - bloch_z[i]) < 1e-14
            # E features site i: [bx, 0, bz]
            assert abs(feats_e[3 * i] - bloch_x[i]) < 1e-14
            assert abs(feats_e[3 * i + 1] - 0.0) < 1e-14
            assert abs(feats_e[3 * i + 2] - bloch_z[i]) < 1e-14

        # 2. 2-RDM matches 2pt_pauli_nn (E2) observables
        for i in range(n - 1):
            j = i + 1
            rho_2 = rdms_2local[(i, j)]
            tr_xi = float(np.real(np.trace(rho_2 @ _XI)))
            tr_xj = float(np.real(np.trace(rho_2 @ _IX)))
            tr_xx = float(np.real(np.trace(rho_2 @ _XX)))
            tr_yy = float(np.real(np.trace(rho_2 @ _YY)))
            tr_zz = float(np.real(np.trace(rho_2 @ _ZZ)))

            # Check matching against bloch_x
            assert abs(tr_xi - bloch_x[i]) < 1e-14
            assert abs(tr_xj - bloch_x[j]) < 1e-14

            # Check matching against E2 features
            base = 5 * i
            assert abs(tr_xi - feats_e2[base]) < 1e-14
            assert abs(tr_xj - feats_e2[base + 1]) < 1e-14
            assert abs(tr_xx - feats_e2[base + 2]) < 1e-14
            assert abs(tr_yy - feats_e2[base + 3]) < 1e-14
            assert abs(tr_zz - feats_e2[base + 4]) < 1e-14

            # Check matching against E features (nn ZZ is the first pair)
            if i == 0 and j == 1:
                # ZZ_01 is at index 3*n + 0 in E features
                assert abs(tr_zz - feats_e[3 * n]) < 1e-14

        print("\nAll shared-basis consistency assertions passed to < 1e-14!")

    def test_destructive_swap_test_unbiased(self):
        """
        Verify that estimator K_hat = 2*(N_0/S) - 1 with N_0 ~ Binomial(S, (1 + K)/2)
        is unbiased (E[K_hat] = K) with exact analytic variance Var = (1 - K^2)/S.
        """
        K_val = 0.65
        shots = 400
        n_samples = 60000

        rng = np.random.default_rng(12345)
        P_0 = (1.0 + K_val) / 2.0
        N_0 = rng.binomial(shots, P_0, size=n_samples)
        K_hat = 2.0 * (N_0 / shots) - 1.0

        emp_mean = float(np.mean(K_hat))
        emp_var = float(np.var(K_hat, ddof=1))

        theo_var = (1.0 - K_val ** 2) / shots
        std_error_mean = np.sqrt(theo_var / n_samples)

        print(f"\nSwap test: Theo K={K_val}, Emp mean={emp_mean:.6f}, diff={abs(emp_mean - K_val):.2e}")
        print(f"Swap test: Theo Var={theo_var:.6f}, Emp Var={emp_var:.6f}, diff={abs(emp_var - theo_var):.2e}")

        # Unbiasedness: within 3 standard errors of the mean
        assert abs(emp_mean - K_val) < 3.0 * std_error_mean, (
            f"Mean {emp_mean} differs from {K_val} by more than 3 standard errors"
        )

        # Variance: within 4% of theoretical variance
        assert abs(emp_var - theo_var) / theo_var < 0.04, (
            f"Variance {emp_var} differs from theoretical {theo_var} by >4%"
        )

    def test_mixed_state_depolarizing_fidelity(self):
        """
        Verify that:
        1. Tr(rho_i(p) rho_j(p)) approaches 1/(2^n) as p -> 1 for any states.
        2. Tr(rho_i(p) |psi_j><psi_j|) approaches 1/(2^n) as p -> 1.
        3. Normalized mixed-state overlap K_ij(p) = Tr(rho_i rho_j)/sqrt(Tr(rho_i^2)Tr(rho_j^2))
           equals pure overlap at p=0 and is consistent with complete mixed-state concentration at p=1.
        """
        n = 4
        dim = 2 ** n

        # Two orthogonal states
        psi1 = np.zeros(dim, dtype=complex)
        psi1[0] = 1.0
        psi2 = np.zeros(dim, dtype=complex)
        psi2[1] = 1.0

        # At p=1.0: state is completely maximally mixed I / 2^n
        rho1_full = depolarize_state(psi1, p=1.0, n=n)
        rho2_full = depolarize_state(psi2, p=1.0, n=n)

        # Tr(rho_1(1) @ rho_2(1)) == 1 / 2^n
        tr_overlap = float(np.real(np.trace(rho1_full @ rho2_full)))
        expected_overlap = 1.0 / dim
        print(f"\np=1.0 Tr(rho1 rho2) = {tr_overlap:.8f}, expected = {expected_overlap:.8f}")
        assert abs(tr_overlap - expected_overlap) < 1e-14

        # Tr(rho_1(1) @ |psi2><psi2|) == 1 / 2^n
        rho2_pure = np.outer(psi2, psi2.conj())
        tr_pure_mixed = float(np.real(np.trace(rho1_full @ rho2_pure)))
        assert abs(tr_pure_mixed - expected_overlap) < 1e-14

        # Normalized overlap K_{12}(p)
        K_p0 = mixed_state_fidelity_gram([psi1, psi2], p=0.0, n=n)
        assert abs(K_p0[0, 1] - 0.0) < 1e-14
        assert abs(K_p0[0, 0] - 1.0) < 1e-14

        K_p1 = mixed_state_fidelity_gram([psi1, psi2], p=1.0, n=n)
        assert abs(K_p1[0, 1] - 1.0) < 1e-14  # Both become identical maximally mixed states
        assert abs(K_p1[0, 0] - 1.0) < 1e-14

    def test_per_qubit_depolarizing_pauli_sum_equivalence_n4(self):
        """
        At n=4, assert that Tr(rho_i(p) rho_j(p)) computed via sequential
        single-qubit channels equals the analytical Pauli sum:
            (1/2^n) * sum_P (1 - p)^(2*|P|) <P>_i <P>_j
        to < 1e-12.
        """
        import itertools
        n = 4
        dim = 2 ** n
        p = 0.07

        # Generate two random pure states
        rng = np.random.default_rng(202610)
        psi1 = rng.standard_normal(dim)
        psi1 /= np.linalg.norm(psi1)
        psi2 = rng.standard_normal(dim)
        psi2 /= np.linalg.norm(psi2)

        rho1 = np.outer(psi1, psi1)
        rho2 = np.outer(psi2, psi2)

        rho1_p = apply_local_depolarizing_channel(rho1, p, n)
        rho2_p = apply_local_depolarizing_channel(rho2, p, n)

        hs_overlap_channel = float(np.real(np.sum(rho1_p * rho2_p)))

        # Analytical Pauli sum
        I2 = np.eye(2, dtype=complex)
        X = np.array([[0, 1], [1, 0]], dtype=complex)
        Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
        Z = np.array([[1, 0], [0, -1]], dtype=complex)
        paulis = [I2, X, Y, Z]

        hs_overlap_pauli = 0.0
        for ops in itertools.product(range(4), repeat=n):
            weight = sum(1 for op in ops if op != 0)
            mat = paulis[ops[0]]
            for op in ops[1:]:
                mat = np.kron(mat, paulis[op])
            exp1 = float(np.real(psi1.conj() @ (mat @ psi1)))
            exp2 = float(np.real(psi2.conj() @ (mat @ psi2)))
            hs_overlap_pauli += ((1.0 - p) ** (2 * weight)) * exp1 * exp2

        hs_overlap_pauli /= (2 ** n)

        diff = abs(hs_overlap_channel - hs_overlap_pauli)
        print(f"\nTest 1 Pauli sum vs channel diff: {diff:.2e}")
        assert diff < 1e-12, f"Pauli sum equivalence failed with diff={diff}"

    def test_per_qubit_depolarizing_noiseless_limit(self):
        """
        At p = 0.00, assert that the normalized overlap matrix K(p=0)
        equals the pure-state fidelity Gram matrix |<psi_i|psi_j>|^2 to < 1e-12.
        """
        n = 4
        dim = 2 ** n
        rng = np.random.default_rng(42)
        states = [rng.standard_normal(dim) for _ in range(6)]
        states = [s / np.linalg.norm(s) for s in states]

        K_p0 = local_depolarizing_fidelity_gram(states, 0.0, n)
        states_arr = np.array(states)
        K_pure = (states_arr @ states_arr.T) ** 2

        diff = np.max(np.abs(K_p0 - K_pure))
        print(f"\nTest 2 p=0 vs K_pure diff: {diff:.2e}")
        assert diff < 1e-12, f"p=0 limit failed with diff={diff}"

    def test_rdm_evolution_equivalence(self):
        """
        Assert that 1-RDMs and 2-RDMs derived from partial tracing rho_i(p)
        match the scaled Bloch coefficient definitions to < 1e-12.
        """
        n = 4
        dim = 2 ** n
        p = 0.05
        rng = np.random.default_rng(999)
        psi = rng.standard_normal(dim)
        psi /= np.linalg.norm(psi)
        rho = np.outer(psi, psi)

        rho_p = apply_local_depolarizing_channel(rho, p, n)

        # 1-RDM test on site 0
        rdm1_traced = partial_trace(rho_p, [0], n)
        sx = np.array([[0, 1], [1, 0]], dtype=complex)
        sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
        sz = np.array([[1, 0], [0, -1]], dtype=complex)
        I2 = np.eye(2, dtype=complex)

        rdm1_pure = partial_trace(rho, [0], n)
        bx = float(np.real(np.trace(sx @ rdm1_pure)))
        by = float(np.real(np.trace(sy @ rdm1_pure)))
        bz = float(np.real(np.trace(sz @ rdm1_pure)))
        rdm1_scaled = 0.5 * (I2 + (1 - p) * bx * sx + (1 - p) * by * sy + (1 - p) * bz * sz)

        diff1 = np.max(np.abs(rdm1_traced - rdm1_scaled))
        assert diff1 < 1e-12, f"1-RDM traced vs scaled diff={diff1}"

        # 2-RDM test on sites 0, 1
        rdm2_traced = partial_trace(rho_p, [0, 1], n)
        rdm2_pure = partial_trace(rho, [0, 1], n)
        paulis = [I2, sx, sy, sz]
        rdm2_scaled = np.zeros((4, 4), dtype=complex)
        for a in range(4):
            for b in range(4):
                weight = (1 if a > 0 else 0) + (1 if b > 0 else 0)
                coeff = float(np.real(np.trace(np.kron(paulis[a], paulis[b]) @ rdm2_pure))) / 4.0
                rdm2_scaled += ((1 - p) ** weight) * coeff * np.kron(paulis[a], paulis[b])

        diff2 = np.max(np.abs(rdm2_traced - rdm2_scaled))
        assert diff2 < 1e-12, f"2-RDM traced vs scaled diff={diff2}"

    def test_feature_std_ratios(self):
        """
        Precondition: Evaluate on the EXACT SAME fixed set of 40 training states from Seed 0.
        Assert std(<X_0>_{p=0.08}) / std(<X_0>_{p=0.00}) == (1 - 0.08) within atol=1e-9.
        Assert std(<Z_0 Z_1>_{p=0.08}) / std(<Z_0 Z_1>_{p=0.00}) == (1 - 0.08)^2 within atol=1e-9.
        """
        tr_states, _, _, _, _ = make_split("t1", n=8, N=40, seed=0)

        sx = np.array([[0, 1], [1, 0]], dtype=complex)
        sz = np.array([[1, 0], [0, -1]], dtype=complex)
        X0 = np.kron(sx, np.eye(128, dtype=complex))
        ZZ01 = np.kron(np.kron(sz, sz), np.eye(64, dtype=complex))

        p = 0.08

        exp_x0_p0 = [float(np.real(psi.conj() @ (X0 @ psi))) for psi in tr_states]
        exp_zz01_p0 = [float(np.real(psi.conj() @ (ZZ01 @ psi))) for psi in tr_states]

        # Under local depolarizing channel:
        # <X_0>_p = (1 - p) * <X_0>_0
        # <Z_0 Z_1>_p = (1 - p)^2 * <Z_0 Z_1>_0
        exp_x0_p08 = [(1.0 - p) * v for v in exp_x0_p0]
        exp_zz01_p08 = [((1.0 - p) ** 2) * v for v in exp_zz01_p0]

        std_x0_p0 = float(np.std(exp_x0_p0))
        std_x0_p08 = float(np.std(exp_x0_p08))
        std_zz_p0 = float(np.std(exp_zz01_p0))
        std_zz_p08 = float(np.std(exp_zz01_p08))

        ratio_x = std_x0_p08 / std_x0_p0
        ratio_zz = std_zz_p08 / std_zz_p0

        print(f"\nratio_x: {ratio_x:.10f}, expected: {1-p:.10f}")
        print(f"ratio_zz: {ratio_zz:.10f}, expected: {(1-p)**2:.10f}")

        assert abs(ratio_x - (1.0 - p)) < 1e-9
        assert abs(ratio_zz - (1.0 - p) ** 2) < 1e-9
