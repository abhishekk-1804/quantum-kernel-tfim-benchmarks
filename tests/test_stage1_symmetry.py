"""
tests/test_stage1_symmetry.py
-----------------------------
Theory checks as formal tests (S1.6):
Verifies parity symmetry, state reality, and operator vanishing identities
on disordered 1D open TFIM (n=6) and 2D frustrated lattice (2x4, n=8).
"""

import os
import sys
import pytest
import numpy as np
import scipy.sparse as sp

# Add src to path
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC = os.path.join(_PROJECT_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from hamiltonians import (
    build_tfim,
    build_frustrated_2d,
    ground_state,
    _single_site_op,
    _two_site_op,
    _build_parity_op,
    _X, _Y, _Z
)


def exp_val(psi: np.ndarray, Op: sp.spmatrix) -> complex:
    """Compute <psi| Op |psi>."""
    return complex(np.vdot(psi, Op.dot(psi)))


def test_symmetry_disordered_tfim_n6():
    """
    Test 5 disordered open-TFIM ground states at n=6 (even sector).
    Asserts vanishing observables (<Z_i>, <Y_i>, <X_i Z_j> (i!=j), <Y_i Z_j> (i!=j), <Z_i Y_j> (i!=j) == 0),
    parity == +1, and reality (max |Im psi| == 0).
    """
    n = 6
    rng = np.random.default_rng(20261023)

    max_z_all = 0.0
    max_y_all = 0.0
    max_xz_all = 0.0
    max_yz_all = 0.0
    max_zy_all = 0.0

    print("\n--- Testing 5 Disordered Open-TFIM Instances at n=6 ---")
    for inst in range(5):
        # Disordered couplings J_i in [0.8, 1.2], fields g_i in [0.5, 1.5]
        couplings = rng.uniform(0.8, 1.2, size=n - 1)
        fields = rng.uniform(0.5, 1.5, size=n)
        H = build_tfim(n, g=1.0, J=1.0, boundary="open", couplings=couplings, fields=fields)
        E0, psi, gap = ground_state(H, n, sector="even")

        # 1. State Reality: ground state is strictly real
        max_im = float(np.max(np.abs(np.imag(psi))))
        assert max_im == 0.0, f"Instance {inst}: Ground state has non-zero imaginary component {max_im}"

        # 2. Parity: <psi| prod X |psi> == +1
        P = _build_parity_op(n)
        p_val = exp_val(psi, P).real
        np.testing.assert_allclose(p_val, 1.0, rtol=0, atol=1e-10, err_msg=f"Instance {inst}: Parity != +1")

        # 3. Vanishing 1-body observables: <Z_i> and <Y_i>
        for i in range(n):
            Zi = _single_site_op(_Z, i, n)
            Yi = _single_site_op(_Y, i, n)
            val_z = abs(exp_val(psi, Zi))
            val_y = abs(exp_val(psi, Yi))
            max_z_all = max(max_z_all, val_z)
            max_y_all = max(max_y_all, val_y)
            np.testing.assert_allclose(val_z, 0.0, rtol=0, atol=1e-10, err_msg=f"Instance {inst}: <Z_{i}> != 0")
            np.testing.assert_allclose(val_y, 0.0, rtol=0, atol=1e-10, err_msg=f"Instance {inst}: <Y_{i}> != 0")

        # 4. Vanishing 2-body cross observables for i != j: <X_i Z_j>, <Y_i Z_j>, <Z_i Y_j>
        for i in range(n):
            for j in range(n):
                if i != j:
                    XZ = _two_site_op(_X, i, _Z, j, n)
                    YZ = _two_site_op(_Y, i, _Z, j, n)
                    ZY = _two_site_op(_Z, i, _Y, j, n)

                    val_xz = abs(exp_val(psi, XZ))
                    val_yz = abs(exp_val(psi, YZ))
                    val_zy = abs(exp_val(psi, ZY))

                    max_xz_all = max(max_xz_all, val_xz)
                    max_yz_all = max(max_yz_all, val_yz)
                    max_zy_all = max(max_zy_all, val_zy)

                    np.testing.assert_allclose(val_xz, 0.0, rtol=0, atol=1e-10, err_msg=f"Instance {inst}: <X_{i} Z_{j}> != 0")
                    np.testing.assert_allclose(val_yz, 0.0, rtol=0, atol=1e-10, err_msg=f"Instance {inst}: <Y_{i} Z_{j}> != 0")
                    np.testing.assert_allclose(val_zy, 0.0, rtol=0, atol=1e-10, err_msg=f"Instance {inst}: <Z_{i} Y_{j}> != 0")

    print(f"Max observed magnitudes across 5 instances (n=6):")
    print(f"  <Z_i>:             {max_z_all:.2e}")
    print(f"  <Y_i>:             {max_y_all:.2e}")
    print(f"  <X_i Z_j> (i!=j):  {max_xz_all:.2e}")
    print(f"  <Y_i Z_j> (i!=j):  {max_yz_all:.2e}")
    print(f"  <Z_i Y_j> (i!=j):  {max_zy_all:.2e}")


def test_symmetry_frustrated_2x4():
    """
    Test 2D frustrated lattice state (2x4, n=8, even sector).
    """
    rows, cols = 2, 4
    n = rows * cols
    H, _, _ = build_frustrated_2d(rows=rows, cols=cols, g=1.0, J1=-1.0, J2=-0.5)
    E0, psi, gap = ground_state(H, n, sector="even")

    # 1. State Reality
    max_im = float(np.max(np.abs(np.imag(psi))))
    assert max_im == 0.0, f"Frustrated 2x4: Ground state has non-zero imaginary component {max_im}"

    # 2. Parity
    P = _build_parity_op(n)
    p_val = exp_val(psi, P).real
    np.testing.assert_allclose(p_val, 1.0, rtol=0, atol=1e-10, err_msg="Frustrated 2x4: Parity != +1")

    # 3. Vanishing observables
    max_z = 0.0
    max_y = 0.0
    for i in range(n):
        Zi = _single_site_op(_Z, i, n)
        Yi = _single_site_op(_Y, i, n)
        val_z = abs(exp_val(psi, Zi))
        val_y = abs(exp_val(psi, Yi))
        max_z = max(max_z, val_z)
        max_y = max(max_y, val_y)
        np.testing.assert_allclose(val_z, 0.0, rtol=0, atol=1e-10)
        np.testing.assert_allclose(val_y, 0.0, rtol=0, atol=1e-10)

    max_xz = 0.0
    max_yz = 0.0
    max_zy = 0.0
    for i in range(n):
        for j in range(n):
            if i != j:
                XZ = _two_site_op(_X, i, _Z, j, n)
                YZ = _two_site_op(_Y, i, _Z, j, n)
                ZY = _two_site_op(_Z, i, _Y, j, n)

                val_xz = abs(exp_val(psi, XZ))
                val_yz = abs(exp_val(psi, YZ))
                val_zy = abs(exp_val(psi, ZY))

                max_xz = max(max_xz, val_xz)
                max_yz = max(max_yz, val_yz)
                max_zy = max(max_zy, val_zy)

                np.testing.assert_allclose(val_xz, 0.0, rtol=0, atol=1e-10)
                np.testing.assert_allclose(val_yz, 0.0, rtol=0, atol=1e-10)
                np.testing.assert_allclose(val_zy, 0.0, rtol=0, atol=1e-10)

    print(f"\nFrustrated 2x4 lattice (n=8) maximum observed magnitudes:")
    print(f"  <Z_i>:             {max_z:.2e}")
    print(f"  <Y_i>:             {max_y:.2e}")
    print(f"  <X_i Z_j> (i!=j):  {max_xz:.2e}")
    print(f"  <Y_i Z_j> (i!=j):  {max_yz:.2e}")
    print(f"  <Z_i Y_j> (i!=j):  {max_zy:.2e}")


def test_operator_hermiticity_n4():
    """
    Explicit dense check that Y_i Z_j (i != j) is Hermitian and traceless at n=4.
    """
    n = 4
    for i in range(n):
        for j in range(n):
            if i != j:
                YZ = _two_site_op(_Y, i, _Z, j, n).toarray()
                # Hermiticity: (Y_i Z_j)^\dagger = Y_i Z_j
                np.testing.assert_allclose(YZ, YZ.conj().T, atol=1e-12, err_msg=f"Y_{i} Z_{j} is not Hermitian!")
                # Traceless
                np.testing.assert_allclose(np.trace(YZ), 0.0, atol=1e-12, err_msg=f"Y_{i} Z_{j} is not traceless!")


def test_negative_control_longitudinal_field():
    """
    Negative control: Add a small longitudinal pinning field h sum_i Z_i (symmetry_break path)
    in the full space, and verify <Z_i> != 0.
    """
    n = 6
    H = build_tfim(n, g=1.0, J=1.0, boundary="open")
    h_field = 0.05
    E0_sb, psi_sb, _ = ground_state(H, n, sector="full", symmetry_break=h_field)

    z_vals = [abs(exp_val(psi_sb, _single_site_op(_Z, i, n)).real) for i in range(n)]
    max_z_sb = max(z_vals)
    print(f"\nNegative Control (longitudinal field h={h_field}): Max <Z_i> = {max_z_sb:.4f}")
    assert max_z_sb > 1e-3, f"Expected non-zero <Z_i> with longitudinal field, got {max_z_sb}"


def test_negative_control_reality_and_rotation():
    """
    Negative control for reality:
    1. Multiply real state by global phase e^{i theta}: <Y_i Z_j> is still 0 (global phase invariance).
    2. Apply non-trivial complex rotation exp(-i t X_0) on the state: show <Y_i Z_j> can become non-zero.
       Comment why that does not apply to real ground states.
    """
    n = 4
    H = build_tfim(n, g=1.0, J=1.0, boundary="open")
    E0, psi, _ = ground_state(H, n, sector="even")

    YZ_01 = _two_site_op(_Y, 0, _Z, 1, n)

    # 1. Global phase rotation
    theta = 0.785398  # pi/4
    psi_global = np.exp(1j * theta) * psi
    val_yz_global = abs(exp_val(psi_global, YZ_01))
    print(f"\nGlobal phase exp(i*theta) state: <Y_0 Z_1> = {val_yz_global:.2e}")
    np.testing.assert_allclose(val_yz_global, 0.0, atol=1e-10, err_msg="Global phase broke zero expectation!")

    # 2. Local complex rotation exp(-i t X_0)
    t = 0.5
    I_n = sp.eye(2 ** n, dtype=complex, format="csr")
    X0 = _single_site_op(_X, 0, n)
    U_rot = np.cos(t) * I_n - 1j * np.sin(t) * X0
    psi_rotated = U_rot.dot(psi)
    psi_rotated = psi_rotated / np.linalg.norm(psi_rotated)

    val_yz_rot = abs(exp_val(psi_rotated, YZ_01))
    print(f"Local rotation exp(-i*t*X_0) state: <Y_0 Z_1> = {val_yz_rot:.4f}")
    assert val_yz_rot > 1e-3, f"Expected non-zero <Y_0 Z_1> after complex rotation, got {val_yz_rot}"
