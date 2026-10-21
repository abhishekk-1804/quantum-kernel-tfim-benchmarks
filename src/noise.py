"""
Noise models for quantum kernel benchmarking.

Provides analytic depolarisation of reduced density matrices and Monte-Carlo
finite-shot noise simulation for PQK and fidelity kernels.
"""

import numpy as np

from kernels import pqk_gram, one_rdm


# ── Analytic depolarisation ────────────────────────────────────────────────────

def depolarize_rdm(rho, p):
    """
    Apply the single-qubit depolarising channel analytically:

        ε(ρ) = (1 − p) ρ  +  p (I₂/2)

    Parameters
    ----------
    rho : np.ndarray, shape (2, 2)
    p : float in [0, 1]

    Returns
    -------
    rho_out : np.ndarray, shape (2, 2)
    """
    I2_half = np.eye(2, dtype=complex) / 2.0
    return (1.0 - p) * rho + p * I2_half


# ── Shot-noise simulation ──────────────────────────────────────────────────────

def shot_noise_pqk(rdms_list, shots, rng):
    """
    Simulate finite-shot measurement noise on the PQK Gram matrix.

    For each state i and each qubit site k, independently simulate the
    measurement of the Bloch vector (X and Z components only; Y ≡ 0 for real
    states).

    For component X:
        n_X+ ~ Binomial(shots, (1 + ⟨X⟩)/2)
        estimated ⟨X⟩ = (n_X+ − n_X−) / shots  = (2 n_X+ / shots) − 1

    Analogously for Z.

    The noisy 2×2 density matrix is reconstructed as:
        ρ̂_k = (I + x̂ X + ẑ Z) / 2

    Then the noisy PQK Gram matrix is computed with the default γ=1.

    Parameters
    ----------
    rdms_list : list of lists of np.ndarray (2×2)
        rdms_list[i] is a list of n density matrices for state i.
    shots : int
        Number of measurement shots per observable per qubit.
    rng : np.random.Generator

    Returns
    -------
    K_noisy : np.ndarray, shape (m, m)
    """
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)

    noisy_rdms = []
    for rdms_i in rdms_list:
        noisy_rdms_i = []
        for rho in rdms_i:
            # Bloch-vector components
            x_exact = float(np.real(np.trace(sx @ rho)))
            z_exact = float(np.real(np.trace(sz @ rho)))

            # Clamp to valid probabilities (floating-point safety)
            p_xp = np.clip((1.0 + x_exact) / 2.0, 0.0, 1.0)
            p_zp = np.clip((1.0 + z_exact) / 2.0, 0.0, 1.0)

            n_xp = rng.binomial(shots, p_xp)
            n_zp = rng.binomial(shots, p_zp)

            x_hat = (2.0 * n_xp / shots) - 1.0
            z_hat = (2.0 * n_zp / shots) - 1.0

            rho_hat = (I2 + x_hat * sx + z_hat * sz) / 2.0
            noisy_rdms_i.append(rho_hat)
        noisy_rdms.append(noisy_rdms_i)

    return pqk_gram(noisy_rdms)


def shot_noise_fidelity(K, shots, rng):
    """
    Simulate finite-shot noise on a fidelity kernel Gram matrix.

    For each off-diagonal pair (i < j):
        K̂_{ij} ~ Binomial(shots, K_{ij}) / shots

    The matrix is then symmetrised and the diagonal is set to 1.0.

    Note: positive semi-definiteness is NOT enforced.

    Parameters
    ----------
    K : np.ndarray, shape (m, m)
    shots : int
    rng : np.random.Generator

    Returns
    -------
    K_noisy : np.ndarray, shape (m, m)
    lam_min : float
        Minimum eigenvalue of K_noisy (may be negative).
    """
    m = K.shape[0]
    K_noisy = np.zeros((m, m), dtype=float)

    for i in range(m):
        for j in range(i + 1, m):
            p = float(np.clip(K[i, j], 0.0, 1.0))
            k_hat = rng.binomial(shots, p) / shots
            K_noisy[i, j] = k_hat
            K_noisy[j, i] = k_hat

    np.fill_diagonal(K_noisy, 1.0)

    lam_min = float(np.linalg.eigvalsh(K_noisy)[0])
    return K_noisy, lam_min
