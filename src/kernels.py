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
    Compute the 2×2 reduced density matrix ρ_k for qubit ``target_q`` via
    partial trace over all other qubits.

    Qubit convention: qubit 0 is the most significant tensor factor.

        ρ_k = Tr_{all j ≠ k}(|ψ⟩⟨ψ|)

    Algorithm
    ---------
    Reshape |ψ⟩ into a tensor of shape (2, 2, ..., 2) with one axis per
    qubit.  Move axis ``target_q`` to position 0, then flatten the remaining
    n-1 axes to get a (2, 2^{n-1}) matrix M.  The 1-RDM is ρ = M M†.

    Parameters
    ----------
    psi : np.ndarray, shape (2^n,)
    n : int
    target_q : int

    Returns
    -------
    rho : np.ndarray, shape (2, 2), dtype complex
    """
    psi_t = psi.reshape([2] * n)
    psi_t = np.moveaxis(psi_t, target_q, 0)
    psi_mat = psi_t.reshape(2, -1)          # (2, 2^{n-1})
    rho = psi_mat @ psi_mat.conj().T        # (2, 2)
    return rho


def two_rdm(psi, n, i, j):
    """
    Compute the 4×4 two-site reduced density matrix ρ_{ij} by partial trace
    over all sites except i and j.

    Qubit convention:
    Qubit 0 is the most significant tensor factor (big-endian bit ordering):
        |q_0 q_1 ... q_{n-1}⟩ = |q_0⟩ ⊗ |q_1⟩ ⊗ ... ⊗ |q_{n-1}⟩

    The returned 4×4 matrix maintains this ordering where site i occupies
    qubit 0 (most significant factor) and site j occupies qubit 1:
        ρ_{ij}[α·2 + β, α'·2 + β'] = ⟨α_i β_j | ρ_{ij} | α'_i β'_j⟩

    Algorithm
    ---------
    1. Reshape |ψ⟩ to shape (2,)*n.
    2. Move axes i and j to positions 0 and 1 respectively.
    3. Flatten remaining n-2 axes to get shape (2, 2, 2^{n-2}).
    4. Reshape to (4, 2^{n-2}) and compute ρ = M M†.

    Parameters
    ----------
    psi : np.ndarray, shape (2^n,)
    n : int
    i, j : int
        Site indices (i ≠ j). Site i becomes the first (most significant) tensor index.

    Returns
    -------
    rho_ij : np.ndarray, shape (4, 4), dtype complex
    """
    assert i != j, "two_rdm requires distinct sites i ≠ j"
    psi_t = psi.reshape([2] * n)

    # Move sites i and j to axes 0 and 1 (in that order)
    psi_t = np.moveaxis(psi_t, [i, j], [0, 1])
    # Shape is now (2, 2, 2, ..., 2) with n axes, sites i and j first.
    # Reshape: merge (axis 0, axis 1) → 4, merge remaining → 2^{n-2}
    psi_mat = psi_t.reshape(4, -1)          # (4, 2^{n-2})
    rho_ij = psi_mat @ psi_mat.conj().T     # (4, 4)
    return rho_ij


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
    Projected quantum kernel (PQK) Gram matrix using 1-RDMs:

        K^{PQ}_{ij} = exp(-γ ∑_k ‖ρ_k(i) - ρ_k(j)‖_F²)

    Mathematical identity
    ---------------------
    For single-qubit states parametrised by Bloch vectors b_k = (bx, by, bz):

        ρ_k = (I + b_k · σ) / 2
        ‖ρ_k^i - ρ_k^j‖_F² = ½ ‖b_k^i - b_k^j‖²

    Hence K^{PQ}(γ) is identical to the RBF kernel

        exp(-(γ/2) · ‖concat(b^i) − concat(b^j)‖²)

    i.e. ``sklearn.metrics.pairwise.rbf_kernel(X, gamma=gamma/2)`` where X
    contains the concatenated Bloch vectors.

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


def pqk_gram_2local(psi_list, n, pairs="nn", gamma=1.0):
    """
    2-local Projected Quantum Kernel (PQK2) Gram matrix using 2-RDMs:

        K^{PQ2}_{ab} = exp(-γ ∑_{(i,j) ∈ pairs} ‖ρ_{ij}^{(a)} - ρ_{ij}^{(b)}‖_F²)

    Parameters
    ----------
    psi_list : list of np.ndarray, each of shape (2^n,)
    n : int
        Number of qubits.
    pairs : {"nn", "all"}
        Which pairs (i, j) to include:
        - ``"nn"``:  nearest-neighbour open-boundary pairs (i, i+1) for
                     i ∈ {0, ..., n-2}.
        - ``"all"``: all unique pairs i < j.
    gamma : float

    Returns
    -------
    K : np.ndarray, shape (m, m)
    """
    if pairs == "nn":
        pair_list = [(i, i + 1) for i in range(n - 1)]
    elif pairs == "all":
        pair_list = [(i, j) for i in range(n) for j in range(i + 1, n)]
    else:
        raise ValueError(f"Unknown pairs mode: {pairs!r}. Use 'nn' or 'all'.")

    m = len(psi_list)

    # Pre-compute 2-RDMs for all states and all pairs
    rdms_2local = []
    for psi in psi_list:
        rdms_2local.append(
            {(i, j): two_rdm(psi, n, i, j) for (i, j) in pair_list}
        )

    K = np.zeros((m, m), dtype=float)
    for a in range(m):
        for b in range(a, m):
            dist2 = 0.0
            for (i, j) in pair_list:
                diff = rdms_2local[a][(i, j)] - rdms_2local[b][(i, j)]
                dist2 += float(np.real(np.trace(diff.conj().T @ diff)))
            k_val = float(np.exp(-gamma * dist2))
            K[a, b] = k_val
            K[b, a] = k_val
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
        - ``"1pt_X"``        : [⟨X_0⟩, ..., ⟨X_{n-1}⟩]              (n features)
        - ``"1pt_xyz"``      : concatenated Bloch vectors [bx,by,bz]  (3n features)
        - ``"2pt_all_pairs"``: all unique ⟨Z_i Z_j⟩ for i < j        (n(n-1)/2 features)
        - ``"2pt_pauli_nn"`` : ⟨X_i⟩ plus nearest-neighbour ⟨XX⟩, ⟨YY⟩, ⟨ZZ⟩
                               (5*(n-1) features from 2-RDM Pauli expansion)
        - ``"full_corr"``    : "1pt_xyz" ∥ "2pt_all_pairs"            (strongest baseline)

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

    elif mode == "2pt_pauli_nn":
        # Extract the 5 non-zero Pauli expectation values for each nearest-neighbour pair (i, i+1):
        # <X_i>, <X_{i+1}>, <X_i X_{i+1}>, <Y_i Y_{i+1}>, <Z_i Z_{i+1}>
        # In the Z_2-even sector, these are the only non-zero Pauli expansion coefficients of rho_{i, i+1}.
        _XI = np.kron(_X.toarray(), np.eye(2, dtype=complex))
        _IX = np.kron(np.eye(2, dtype=complex), _X.toarray())
        _XX = np.kron(_X.toarray(), _X.toarray())
        _YY = np.kron(_Y.toarray(), _Y.toarray())
        _ZZ = np.kron(_Z.toarray(), _Z.toarray())
        feats = []
        for i in range(n - 1):
            rho_ij = two_rdm(psi, n, i, i + 1)
            feats.extend([
                float(np.real(np.trace(rho_ij @ _XI))),
                float(np.real(np.trace(rho_ij @ _IX))),
                float(np.real(np.trace(rho_ij @ _XX))),
                float(np.real(np.trace(rho_ij @ _YY))),
                float(np.real(np.trace(rho_ij @ _ZZ))),
            ])
        return np.array(feats, dtype=float)

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
