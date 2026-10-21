"""
Noise models for quantum kernel benchmarking.

Provides analytic depolarisation of reduced density matrices, finite-shot
sampling of Bloch and Pauli observables, and finite-shot noise simulation
for quantum kernels.
"""

import numpy as np

from kernels import pqk_gram, one_rdm, classical_features


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


# ── Shot-noise simulation for features ─────────────────────────────────────────

def noisy_bloch_features(psi_list, n, shots, rng, components=("x", "z")):
    """
    Simulate finite-shot measurement of single-qubit Bloch vector components.

    For each state i, site k, and component c in components:
        n_+ ~ Binomial(shots, (1 + ⟨c⟩)/2)
        c_hat = (2 * n_+ / shots) - 1

    Parameters
    ----------
    psi_list : list of np.ndarray, each of shape (2^n,)
        List of m quantum statevectors.
    n : int
        Number of qubits.
    shots : int
        Measurement shots per observable per site.
    rng : np.random.Generator
        NumPy random number generator.
    components : tuple or list of str
        Subset of ('x', 'y', 'z'). Default: ('x', 'z').

    Returns
    -------
    features : np.ndarray, shape (m, n, len(components))
        Noisy Bloch vector estimates.
    """
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    pauli_map = {"x": sx, "y": sy, "z": sz}

    m = len(psi_list)
    n_comp = len(components)
    features = np.zeros((m, n, n_comp), dtype=float)

    for i, psi in enumerate(psi_list):
        for k in range(n):
            rho_k = one_rdm(psi, n, k)
            for c_idx, comp in enumerate(components):
                op = pauli_map[comp.lower()]
                val = float(np.real(np.trace(op @ rho_k)))
                p_plus = np.clip((1.0 + val) / 2.0, 0.0, 1.0)
                n_plus = rng.binomial(shots, p_plus)
                features[i, k, c_idx] = (2.0 * n_plus / shots) - 1.0

    return features


def noisy_classical_features(psi_list, n, shots, rng, mode="2pt_pauli_nn"):
    """
    Estimate classical observables by binomial finite-shot sampling.

    For each state and each observable in the chosen mode (e.g. ⟨X_i⟩, ⟨Z_i Z_j⟩,
    ⟨XX⟩, ⟨YY⟩), the expectation value is converted to a Bernoulli parameter
    p = (1 + ⟨O⟩)/2, and simulated with shots measurements.

    Parameters
    ----------
    psi_list : list of np.ndarray, each of shape (2^n,)
        List of m quantum statevectors.
    n : int
        Number of qubits.
    shots : int
        Measurement shots per observable.
    rng : np.random.Generator
    mode : str
        Feature mode matching `kernels.classical_features`.
        Options include: "1pt_X", "2pt_pauli_nn", "2pt_all_pairs", "full_corr".

    Returns
    -------
    noisy_features : np.ndarray, shape (m, d)
        Noisy feature matrix.
    """
    m = len(psi_list)
    exact_feats = [classical_features(psi, n, mode=mode) for psi in psi_list]
    d = len(exact_feats[0])

    noisy_feats = np.zeros((m, d), dtype=float)
    for i in range(m):
        for j in range(d):
            val = exact_feats[i][j]
            p_plus = np.clip((1.0 + val) / 2.0, 0.0, 1.0)
            n_plus = rng.binomial(shots, p_plus)
            noisy_feats[i, j] = (2.0 * n_plus / shots) - 1.0

    return noisy_feats


def shot_noise_pqk(rdms_list, shots, rng):
    """
    Legacy wrapper: simulate finite-shot noise on a PQK Gram matrix.
    """
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)

    noisy_rdms = []
    for rdms_i in rdms_list:
        noisy_rdms_i = []
        for rho in rdms_i:
            x_exact = float(np.real(np.trace(sx @ rho)))
            z_exact = float(np.real(np.trace(sz @ rho)))

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

    Note: positive semi-definiteness is NOT enforced implicitly.
    Use `fidelity_clip_psd` to explicitly project onto the PSD cone.

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


def fidelity_clip_psd(K):
    """
    Project a symmetric noisy kernel matrix onto the positive semi-definite (PSD)
    cone by setting negative eigenvalues to zero, then restoring unit diagonal
    via congruence scaling D^{-1/2} K D^{-1/2}.

    Parameters
    ----------
    K : np.ndarray, shape (m, m)
        Symmetric kernel matrix (e.g. from shot_noise_fidelity).

    Returns
    -------
    K_psd : np.ndarray, shape (m, m)
        Projected positive semi-definite kernel matrix with unit diagonal.
    """
    K_sym = 0.5 * (K + K.T)
    evals, evecs = np.linalg.eigh(K_sym)
    evals_clipped = np.maximum(evals, 0.0)
    K_clipped = evecs @ np.diag(evals_clipped) @ evecs.T

    # Congruence normalization D^{-1/2} K_clipped D^{-1/2} preserves PSD property
    diag = np.sqrt(np.maximum(np.diag(K_clipped), 1e-14))
    K_psd = K_clipped / np.outer(diag, diag)
    np.fill_diagonal(K_psd, 1.0)
    K_psd = 0.5 * (K_psd + K_psd.T)
    return K_psd


def total_shots(model, m, n, S):
    """
    Compute the total measurement shot cost to construct an m × m kernel Gram matrix.

    Scaling properties:
    - PQK (1-local and 2-local nearest-neighbour): O(m * S), linear in m.
      Each of the m states is measured in a fixed set of Pauli bases.
    - Fidelity (FQ): O(m^2 * S), quadratic in m.
      Requires measuring m(m-1)/2 distinct state pairs.

    Parameters
    ----------
    model : str
        One of {"fidelity", "fq", "pqk", "pqk_1local", "pqk2_nn", "pqk_2local_nn"}.
    m : int
        Number of dataset samples (states).
    n : int
        Number of qubits.
    S : int
        Number of shots allocated per measurement setting.

    Returns
    -------
    shots : int
        Total shot count across the full experiment.
    """
    mod = model.lower()
    if mod in ("fidelity", "fq"):
        # m*(m-1)/2 off-diagonal pairs, each measured with S shots
        return (m * (m - 1) // 2) * S
    elif mod in ("pqk", "pqk_1local"):
        # 2 bases (X, Z) per site for each of the m states
        return 2 * n * m * S
    elif mod in ("pqk2_nn", "pqk_2local_nn"):
        # 3 bases (XX, YY, ZZ) per nearest-neighbour bond for each of the m states
        return 3 * (n - 1) * m * S
    elif mod in ("classical", "classical_full"):
        return 2 * n * m * S
    else:
        raise ValueError(f"Unknown model: {model!r}")
