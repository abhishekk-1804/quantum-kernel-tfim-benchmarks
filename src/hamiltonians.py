"""
Sparse-matrix Hamiltonians and observables for 1D/2D transverse-field Ising models.

Qubit convention (little-endian / standard Kronecker ordering):
    |q_0 q_1 ... q_{n-1}⟩  =  |q_0⟩ ⊗ |q_1⟩ ⊗ ... ⊗ |q_{n-1}⟩

This means qubit 0 is the *most significant* tensor factor.  The computational
basis state with integer index  k  corresponds to the bit-string obtained by
writing k in binary with n bits, where the leftmost (most significant) bit is
qubit 0.

All Hamiltonians are returned as SciPy CSR sparse matrices.
"""

import functools
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import scipy.linalg


# ── Pauli matrices (dense, used as building-blocks) ────────────────────────────
_I2 = sp.eye(2, format="csr", dtype=complex)
_X = sp.csr_matrix(np.array([[0, 1], [1, 0]], dtype=complex))
_Y = sp.csr_matrix(np.array([[0, -1j], [1j, 0]], dtype=complex))
_Z = sp.csr_matrix(np.array([[1, 0], [0, -1]], dtype=complex))

# Real-valued Paulis (needed for the purely-real sparse sector path)
_I2r = sp.eye(2, format="csr", dtype=np.float64)
_Xr  = sp.csr_matrix(np.array([[0, 1], [1, 0]], dtype=np.float64))
_Zr  = sp.csr_matrix(np.array([[1, 0], [0, -1]], dtype=np.float64))


# ── Low-level helpers ──────────────────────────────────────────────────────────

def _single_site_op(op, site, n):
    """
    Embed a single-qubit operator `op` at `site` in an n-qubit Hilbert space.
    Returns a 2^n × 2^n sparse matrix in CSR format.
    """
    factors = [_I2] * n
    factors[site] = op
    result = factors[0]
    for f in factors[1:]:
        result = sp.kron(result, f, format="csr")
    return result


def _two_site_op(op_a, site_a, op_b, site_b, n):
    """
    Embed op_a (at site_a) ⊗ op_b (at site_b) in an n-qubit Hilbert space.

    When site_a == site_b the operators are composed at that site:
        factors[site_a] = op_a @ op_b
    This correctly handles Z_i² = I and other same-site products.
    """
    factors = [_I2] * n
    if site_a == site_b:
        factors[site_a] = op_a @ op_b
    else:
        factors[site_a] = op_a
        factors[site_b] = op_b
    result = factors[0]
    for f in factors[1:]:
        result = sp.kron(result, f, format="csr")
    return result


# ── 1D TFIM ────────────────────────────────────────────────────────────────────

def build_tfim(n, g, J=1.0, boundary="open", couplings=None, fields=None):
    """
    Build the 1D transverse-field Ising model (TFIM) Hamiltonian:

        H = -∑_i J_i Z_i Z_{i+1}  -  ∑_i g_i X_i

    Parameters
    ----------
    n : int
        Number of qubits.
    g : float
        Uniform transverse field strength (used when `fields` is None).
    J : float
        Uniform coupling strength (used when `couplings` is None).
    boundary : {"open", "periodic"}
        Boundary conditions.
    couplings : array-like or None
        Site-resolved couplings J_i.  Length must be n-1 (open) or n (periodic).
    fields : array-like or None
        Site-resolved fields g_i.  Length must be n.

    Returns
    -------
    H : scipy.sparse.csr_matrix, shape (2^n, 2^n)
    """
    dim = 2 ** n

    # --- validate / set couplings ---
    if couplings is None:
        if boundary == "open":
            couplings = np.full(n - 1, J, dtype=float)
        else:
            couplings = np.full(n, J, dtype=float)
    else:
        couplings = np.asarray(couplings, dtype=float)
        if boundary == "open":
            assert len(couplings) == n - 1, (
                f"For open boundary, len(couplings) must be {n - 1}, got {len(couplings)}"
            )
        else:
            assert len(couplings) == n, (
                f"For periodic boundary, len(couplings) must be {n}, got {len(couplings)}"
            )

    # --- validate / set fields ---
    if fields is None:
        fields = np.full(n, g, dtype=float)
    else:
        fields = np.asarray(fields, dtype=float)
        assert len(fields) == n, (
            f"len(fields) must be {n}, got {len(fields)}"
        )

    H = sp.csr_matrix((dim, dim), dtype=complex)

    # ZZ coupling terms
    if boundary == "open":
        bond_range = range(n - 1)
    else:
        bond_range = range(n)

    for idx, i in enumerate(bond_range):
        j = (i + 1) % n
        ZZ = _two_site_op(_Z, i, _Z, j, n)
        H = H - couplings[idx] * ZZ

    # Transverse-field X terms
    for i in range(n):
        Xi = _single_site_op(_X, i, n)
        H = H - fields[i] * Xi

    return H.tocsr()


# ── 2D frustrated lattice ──────────────────────────────────────────────────────

def build_frustrated_2d(rows=2, cols=4, g=1.0, J1=-1.0, J2=-0.5):
    """
    Build a 2D frustrated Ising Hamiltonian on a `rows × cols` lattice with
    OPEN boundary conditions.

    Sign convention:
        H = -J1 ∑_{⟨i,j⟩} Z_i Z_j  -  J2 ∑_{⟪i,k⟫} Z_i Z_k  -  g ∑_i X_i

    Couplings:
    - J1 couples nearest-neighbour (NN) pairs (horizontal and vertical).
    - J2 couples next-nearest-neighbour (NNN) diagonal pairs within each
      elementary plaquette.

    Note: negative J1/J2 values penalise ferromagnetic alignment (i.e. the
    sign in the Hamiltonian is  -J1 ZZ, so with J1 < 0 the interaction becomes
    |J1| ZZ, which *penalises* parallel spins and favours antiferromagnetic
    order).

    For a 2×4 open lattice, the bond counts are:
    - NN horizontal: (cols-1)*rows = 3*2 = 6... wait — for 2 rows, 4 cols:
        row 0: cols-1 = 3 horizontal bonds
        row 1: cols-1 = 3 horizontal bonds  → total 6 horizontal
        vertical: rows-1 per column = 1 * cols = 4 vertical bonds
        NN total = 10
    - NNN diagonal: (rows-1)*(cols-1) = 1*3 = 3 plaquettes, each with 2
        diagonals → 6 diagonal bonds.

    Parameters
    ----------
    rows, cols : int
        Lattice dimensions.
    g : float
        Transverse field.
    J1 : float
        Nearest-neighbour coupling (negative → antiferromagnetic in context
        of the -J1 sign convention).
    J2 : float
        Next-nearest-neighbour diagonal coupling.

    Returns
    -------
    H : scipy.sparse.csr_matrix
    nn_bonds : list of (i, j) tuples
    nnn_bonds : list of (i, k) tuples
    """
    n = rows * cols
    dim = 2 ** n

    def site(r, c):
        return r * cols + c

    H = sp.csr_matrix((dim, dim), dtype=complex)

    nn_bonds = []
    nnn_bonds = []

    # NN horizontal bonds
    for r in range(rows):
        for c in range(cols - 1):
            i, j = site(r, c), site(r, c + 1)
            nn_bonds.append((i, j))
            ZZ = _two_site_op(_Z, i, _Z, j, n)
            H = H - J1 * ZZ

    # NN vertical bonds
    for r in range(rows - 1):
        for c in range(cols):
            i, j = site(r, c), site(r + 1, c)
            nn_bonds.append((i, j))
            ZZ = _two_site_op(_Z, i, _Z, j, n)
            H = H - J1 * ZZ

    # NNN diagonal bonds (within each plaquette)
    for r in range(rows - 1):
        for c in range(cols - 1):
            # diagonal 1: (r,c) — (r+1,c+1)
            i, k = site(r, c), site(r + 1, c + 1)
            nnn_bonds.append((i, k))
            ZZ = _two_site_op(_Z, i, _Z, k, n)
            H = H - J2 * ZZ
            # diagonal 2: (r,c+1) — (r+1,c)
            i, k = site(r, c + 1), site(r + 1, c)
            nnn_bonds.append((i, k))
            ZZ = _two_site_op(_Z, i, _Z, k, n)
            H = H - J2 * ZZ

    # Transverse-field terms
    for i in range(n):
        Xi = _single_site_op(_X, i, n)
        H = H - g * Xi

    return H.tocsr(), nn_bonds, nnn_bonds


# ── Sparse parity-sector basis ─────────────────────────────────────────────────

def _build_parity_op(n):
    """
    Parity operator P = ⊗_{i=0}^{n-1} X_i  (2^n × 2^n sparse matrix).
    """
    result = _X.copy()
    for _ in range(n - 1):
        result = sp.kron(result, _X, format="csr")
    return result


@functools.lru_cache(maxsize=16)
def _build_sector_basis(n, sector="even"):
    """
    Build a sparse orthonormal basis for the Z_2 parity sector.

    The Z_2 parity operator is P = ⊗_{i=0}^{n-1} X_i, with eigenvalues ±1.
    The ±1 eigenvectors are the symmetric / antisymmetric superpositions of
    computational-basis pairs:

        |+⟩_{s,s̄} = (|s⟩ + |s̄⟩) / √2    (even sector, eigenvalue +1)
        |−⟩_{s,s̄} = (|s⟩ − |s̄⟩) / √2    (odd  sector, eigenvalue −1)

    where s̄ = (2^n − 1) XOR s is the bitwise complement of s (flips all
    qubits, equivalent to P |s⟩ = |s̄⟩).

    We keep only the representative s < s̄ to avoid double-counting, giving
    exactly 2^(n−1) basis columns.

    Note
    ----
    The basis handles the fixed-point s == s̄ only when n = 0; for n ≥ 1
    there are no self-symmetric states (s ≠ s̄ always).

    Parameters
    ----------
    n : int
    sector : {"even", "odd"}

    Returns
    -------
    V : scipy.sparse.csc_matrix, shape (2^n, 2^(n-1)), dtype float64
        Columns are orthonormal basis vectors for the chosen sector.
    """
    dim = 2 ** n
    flip_mask = dim - 1  # XOR with this to flip all bits

    sign = +1.0 if sector == "even" else -1.0
    val = 1.0 / np.sqrt(2.0)

    rows_idx = []
    cols_idx = []
    data = []

    col = 0
    for s in range(dim):
        s_flip = flip_mask ^ s
        if s < s_flip:
            rows_idx.append(s)
            cols_idx.append(col)
            data.append(val)

            rows_idx.append(s_flip)
            cols_idx.append(col)
            data.append(sign * val)

            col += 1

    sector_dim = col  # should be 2^(n-1)
    V = sp.csc_matrix(
        (data, (rows_idx, cols_idx)),
        shape=(dim, sector_dim),
        dtype=np.float64,
    )
    return V


def ground_state(H, n, sector="even", symmetry_break=0.0):
    """
    Solve for the ground state of Hamiltonian H using sparse parity-sector
    projection.

    Strategy
    --------
    1. If ``symmetry_break > 0``: add a longitudinal pinning field
       h ∑_i Z_i, bypass parity-sector projection, and diagonalise the full
       2^n × 2^n sparse Hamiltonian with ``eigsh(k=2)``.

    2. Otherwise: project into the Z_2-parity sector by transforming to the
       sparse orthonormal sector basis V (shape 2^n × 2^(n-1)) constructed in
       :func:`_build_sector_basis`.  Compute H_sec = V^T H V sparsely.

       * Sector dimension ≤ 1024 (n ≤ 11): use ``scipy.linalg.eigh`` on the
         dense sector matrix (exact).
       * Sector dimension > 1024 (n ≥ 12): use ``scipy.sparse.linalg.eigsh``
         with k=2 (Lanczos / ARPACK).

    The returned ``gap`` is the **in-sector** gap (energy difference between
    the two lowest levels within the chosen parity sector).  For the TFIM this
    equals the true spectral gap (the complementary sector starts higher), but
    for general Hamiltonians the macroscopic gap to the opposite sector may be
    exponentially small and is NOT captured here.

    Parameters
    ----------
    H : scipy.sparse.csr_matrix, shape (2^n, 2^n)
    n : int
    sector : {"even", "odd", "full"}
        Parity sector to solve in.  ``"full"`` bypasses projection.
    symmetry_break : float
        Strength of longitudinal pinning field h ∑_i Z_i added before
        diagonalisation.  When > 0, overrides ``sector``.

    Returns
    -------
    E0 : float
    psi : np.ndarray, shape (2^n,), dtype float64
        Normalised ground-state vector.
    gap : float
        In-sector energy gap (first excited level minus ground level within the
        chosen sector).
    """
    dim = 2 ** n
    H_real = H.real.astype(np.float64)  # TFIM is purely real

    # ── Case 1: symmetry breaking — full-space eigsh ──────────────────────────
    if symmetry_break > 0.0:
        H_full = H_real.copy()
        for i in range(n):
            Zi = _single_site_op(_Zr, i, n)
            H_full = H_full + symmetry_break * Zi
        vals, vecs = spla.eigsh(H_full, k=2, which="SA")
        idx = np.argsort(vals)
        E0, E1 = vals[idx[0]], vals[idx[1]]
        psi = np.real(vecs[:, idx[0]]).astype(np.float64)
        psi /= np.linalg.norm(psi)
        return float(E0), psi, float(E1 - E0)

    # ── Case 2: full-space solve (sector="full") ──────────────────────────────
    if sector == "full":
        vals, vecs = spla.eigsh(H_real, k=2, which="SA")
        idx = np.argsort(vals)
        E0, E1 = vals[idx[0]], vals[idx[1]]
        psi = vecs[:, idx[0]].astype(np.float64)
        psi /= np.linalg.norm(psi)
        return float(E0), psi, float(E1 - E0)

    # ── Case 3: sparse parity-sector projection ───────────────────────────────
    V = _build_sector_basis(n, sector=sector)   # shape (dim, dim//2), float64
    sector_dim = V.shape[1]

    # Project: H_sec = V^T H V  (sparse × sparse, stays sparse)
    HV = H_real @ V                              # shape (dim, sector_dim)
    H_sec = (V.T @ HV).tocsr()                  # shape (sector_dim, sector_dim)

    # Symmetrise to eliminate any floating-point asymmetry
    H_sec = (H_sec + H_sec.T) * 0.5

    if sector_dim <= 1024:
        # Dense exact diagonalisation in sector
        evals, evecs = scipy.linalg.eigh(H_sec.toarray())
        E0 = float(evals[0])
        gap = float(evals[1] - evals[0]) if len(evals) > 1 else float("inf")
        phi = evecs[:, 0]
    else:
        # Sparse iterative diagonalisation
        vals, vecs = spla.eigsh(H_sec, k=2, which="SA")
        idx = np.argsort(vals)
        E0, E1 = float(vals[idx[0]]), float(vals[idx[1]])
        gap = E1 - E0
        phi = vecs[:, idx[0]]

    assert gap > 1e-9, f"Degenerate ground state in sector (gap={gap:.3e})"

    # Lift sector solution back to full Hilbert space
    psi = (V @ phi).astype(np.float64)
    psi /= np.linalg.norm(psi)

    return E0, psi, float(gap)


# ── Observables ────────────────────────────────────────────────────────────────

def expect_x(psi, n):
    """
    Compute ⟨X_i⟩ for each site i.

    Evaluated via bit-flip action in the computational basis:
        ⟨ψ| X_i |ψ⟩ = ∑_s ψ_s ψ_{s ⊕ 2^{n - 1 - i}}
    respecting qubit 0 as the most significant tensor factor (big-endian).

    Returns
    -------
    x_vals : np.ndarray, shape (n,)
    """
    dim = 2 ** n
    s = np.arange(dim)
    x_vals = np.zeros(n, dtype=float)
    for i in range(n):
        s_flip = s ^ (1 << (n - 1 - i))
        x_vals[i] = float(np.real(np.sum(psi.conj() * psi[s_flip])))
    return x_vals


def expect_zz(psi, n, i, j):
    """
    Compute ⟨ψ| Z_i Z_j |ψ⟩.

    When i == j, Z_i² = I analytically, returning ‖ψ‖² = 1 for any
    normalised state without constructing the full operator.
    Evaluated via the diagonal representation in the computational basis:
        ⟨ψ| Z_i Z_j |ψ⟩ = ∑_s |ψ_s|² (-1)^{b_i(s) ⊕ b_j(s)}
    """
    if i == j:
        return float(np.real(np.dot(psi.conj(), psi)))
    dim = 2 ** n
    s = np.arange(dim)
    bi = (s >> (n - 1 - i)) & 1
    bj = (s >> (n - 1 - j)) & 1
    signs = 1.0 - 2.0 * ((bi ^ bj) & 1)
    return float(np.sum(np.abs(psi) ** 2 * signs))


def expect_zzzz(psi, n, i, j, k, l):
    """
    Compute ⟨ψ| Z_i Z_j Z_k Z_l |ψ⟩.

    Evaluated via the diagonal representation in the computational basis:
        ⟨ψ| Z_i Z_j Z_k Z_l |ψ⟩ = ∑_s |ψ_s|² (-1)^{b_i(s) ⊕ b_j(s) ⊕ b_k(s) ⊕ b_l(s)}
    respecting qubit 0 as the most significant tensor factor (big-endian).
    """
    s = np.arange(2 ** n)
    bi = (s >> (n - 1 - i)) & 1
    bj = (s >> (n - 1 - j)) & 1
    bk = (s >> (n - 1 - k)) & 1
    bl = (s >> (n - 1 - l)) & 1
    signs = 1.0 - 2.0 * ((bi ^ bj ^ bk ^ bl) & 1)
    return float(np.sum(np.abs(psi) ** 2 * signs))


def correlation_matrix(psi, n):
    """
    Compute the n×n matrix  C_{ij} = ⟨ψ| Z_i Z_j |ψ⟩.
    """
    C = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            C[i, j] = expect_zz(psi, n, i, j)
    return C


def half_chain_entropy(psi, n):
    """
    Von Neumann entanglement entropy across the half-chain bipartition
    A = {0, ..., ⌊n/2⌋-1}.

        S = -Tr(ρ_A log₂ ρ_A)

    Parameters
    ----------
    psi : np.ndarray, shape (2^n,)
    n : int

    Returns
    -------
    S : float
    """
    n_A = n // 2
    n_B = n - n_A
    dim_A = 2 ** n_A
    dim_B = 2 ** n_B

    # Reshape: axes 0..n_A-1 belong to A, axes n_A..n-1 belong to B
    psi_tensor = psi.reshape([2] * n)
    # Merge A-indices and B-indices
    psi_mat = psi_tensor.reshape(dim_A, dim_B)

    # Eigenvalues of reduced density matrix ρ_A = Tr_B(|ψ⟩⟨ψ|)
    # Using SVD: singular values σ_k → eigenvalues λ_k = σ_k²
    _, sv, _ = np.linalg.svd(psi_mat, full_matrices=False)
    lambdas = sv ** 2

    # Filter tiny eigenvalues
    lambdas = lambdas[lambdas > 1e-14]
    S = float(-np.sum(lambdas * np.log2(lambdas)))
    return S


def structure_factor(psi, rows, cols):
    """
    Static spin structure factor on a `rows × cols` lattice:

        S(q) = (1/N) ∑_{j,k} exp(i q·(r_j - r_k)) ⟨Z_j Z_k⟩

    Evaluated on the grid:
        q_x ∈ {0, π}
        q_y ∈ {0, π/2, π, 3π/2}

    Parameters
    ----------
    psi : np.ndarray, shape (2^(rows*cols),)
    rows, cols : int

    Returns
    -------
    Sq : dict mapping (q_x, q_y) → float
    """
    n = rows * cols

    def site_pos(s):
        r, c = divmod(s, cols)
        return np.array([c, r], dtype=float)  # (x, y)

    # Pre-compute ⟨Z_j Z_k⟩ for all pairs
    Czz = correlation_matrix(psi, n)

    qx_vals = [0.0, np.pi]
    qy_vals = [0.0, np.pi / 2, np.pi, 3 * np.pi / 2]

    Sq = {}
    for qx in qx_vals:
        for qy in qy_vals:
            q = np.array([qx, qy])
            total = 0.0 + 0.0j
            for j in range(n):
                for k in range(n):
                    rjk = site_pos(j) - site_pos(k)
                    phase = np.exp(1j * np.dot(q, rjk))
                    total += phase * Czz[j, k]
            Sq[(qx, qy)] = float(np.real(total)) / n
    return Sq
