"""
Quantum kernel functions and classical feature maps for TFIM ground states.

All kernels operate on pre-computed quantum states (wavefunctions) and their
derived observables.  No circuit simulation is performed here.
"""

import numpy as np
import scipy.linalg

from hamiltonians import (
    _single_site_op, _X, _Y, _Z, expect_x, expect_zz
)


# ── Single-qubit density matrices ──────────────────────────────────────────────

def one_rdm(psi, n, target_q):
    """
    Compute the 2×2 reduced density matrix ρ_k for qubit `target_q` via
    partial trace over all other qubits.

    Qubit convention: qubit 0 is the most significant tensor factor.

        ρ_k = Tr_{all j ≠ k}(|ψ⟩⟨ψ|)

    Parameters
    ----------
    psi : np.ndarray, shape (2^n,)
    n : int
    target_q : int

    Returns
    -------
    rho : np.ndarray, shape (2, 2), dtype complex
    """
    # Reshape to tensor with one axis per qubit
    psi_t = psi.reshape([2] * n)

    # Move target qubit to axis 0, merge remaining axes
    # After moveaxis: shape (2, 2^(n-1))
    psi_t = np.moveaxis(psi_t, target_q, 0)
    psi_mat = psi_t.reshape(2, -1)  # (2, 2^(n-1))

    rho = psi_mat @ psi_mat.conj().T  # (2, 2)
    return rho


def bloch_vector(rho):
    """
    Compute the Bloch vector of a 2×2 density matrix.

        b = [Tr(X ρ), Tr(Y ρ), Tr(Z ρ)]

    Note: for real wavefunctions |ψ⟩, Tr(Y ρ) ≡ 0.

    Parameters
    ----------
    rho : np.ndarray, shape (2, 2)

    Returns
    -------
    b : np.ndarray, shape (3,), dtype float
    """
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    bx = float(np.real(np.trace(sx @ rho)))
    by = float(np.real(np.trace(sy @ rho)))
    bz = float(np.real(np.trace(sz @ rho)))
    return np.array([bx, by, bz])


# ── Kernel matrices ─────────────────────────────────────────────────────────────

def fidelity_gram(states):
    """
    Fidelity (quantum) kernel Gram matrix:

        K^{FQ}_{ij} = |⟨ψ_i | ψ_j⟩|²

    Parameters
    ----------
    states : list of np.ndarray, each of shape (2^n,)

    Returns
    -------
    K : np.ndarray, shape (m, m)
    """
    m = len(states)
    K = np.zeros((m, m), dtype=float)
    for i in range(m):
        for j in range(i, m):
            ip = float(np.abs(np.dot(states[i].conj(), states[j])) ** 2)
            K[i, j] = ip
            K[j, i] = ip
    return K


def pqk_gram(rdms_list, gamma=1.0):
    """
    Projected quantum kernel (PQK) Gram matrix:

        K^{PQ}_{ij} = exp(-γ ∑_k ‖ρ_k(i) - ρ_k(j)‖_F²)

    Parameters
    ----------
    rdms_list : list of lists
        rdms_list[i] is a list of n density matrices (2×2 arrays) for state i.
    gamma : float

    Returns
    -------
    K : np.ndarray, shape (m, m)
    """
    m = len(rdms_list)
    K = np.zeros((m, m), dtype=float)
    for i in range(m):
        for j in range(i, m):
            dist2 = 0.0
            for rho_i, rho_j in zip(rdms_list[i], rdms_list[j]):
                diff = rho_i - rho_j
                dist2 += float(np.real(np.trace(diff.conj().T @ diff)))
            k_val = float(np.exp(-gamma * dist2))
            K[i, j] = k_val
            K[j, i] = k_val
    return K


# ── Kernel-Target Alignment ────────────────────────────────────────────────────

def kta(K, y):
    """
    Kernel-Target Alignment:

        KTA = (y^T K y) / (N √Tr(K²))

    Parameters
    ----------
    K : np.ndarray, shape (m, m)
    y : np.ndarray, shape (m,)  — class labels (±1 convention)

    Returns
    -------
    score : float
    """
    y = np.asarray(y, dtype=float)
    N = len(y)
    numerator = float(y @ K @ y)
    denominator = N * float(np.sqrt(np.trace(K @ K)))
    if denominator == 0.0:
        return 0.0
    return numerator / denominator


# ── Classical feature maps ─────────────────────────────────────────────────────

def classical_features(psi, n, mode="full_corr"):
    """
    Compute a classical feature vector derived from the quantum state |ψ⟩.

    Parameters
    ----------
    psi : np.ndarray, shape (2^n,)
    n : int
    mode : str
        One of:
        - "1pt_X"        : [⟨X_0⟩, ..., ⟨X_{n-1}⟩]              (n features)
        - "1pt_xyz"      : concatenated Bloch vectors [bx,by,bz]  (3n features)
        - "2pt_all_pairs": all unique ⟨Z_i Z_j⟩ for i < j        (n(n-1)/2 features)
        - "full_corr"    : "1pt_xyz" || "2pt_all_pairs"           (strongest baseline)

    Returns
    -------
    features : np.ndarray, shape (d,)
    """
    if mode == "1pt_X":
        return expect_x(psi, n)

    elif mode == "1pt_xyz":
        feats = []
        for k in range(n):
            rho_k = one_rdm(psi, n, k)
            bv = bloch_vector(rho_k)
            feats.append(bv)
        return np.concatenate(feats)

    elif mode == "2pt_all_pairs":
        feats = []
        for i in range(n):
            for j in range(i + 1, n):
                feats.append(expect_zz(psi, n, i, j))
        return np.array(feats)

    elif mode == "full_corr":
        xyz = classical_features(psi, n, mode="1pt_xyz")
        pairs = classical_features(psi, n, mode="2pt_all_pairs")
        return np.concatenate([xyz, pairs])

    else:
        raise ValueError(f"Unknown mode: {mode!r}")


# ── Diagnostics ─────────────────────────────────────────────────────────────────

def off_diagonal_variance(K):
    """
    Sample variance of off-diagonal kernel entries {K_{ij} : i ≠ j}.

    Parameters
    ----------
    K : np.ndarray, shape (m, m)

    Returns
    -------
    var : float
    """
    m = K.shape[0]
    mask = ~np.eye(m, dtype=bool)
    off_diag = K[mask]
    return float(np.var(off_diag, ddof=1)) if len(off_diag) > 1 else 0.0
