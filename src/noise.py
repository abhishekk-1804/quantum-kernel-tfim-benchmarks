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


# ── Shared-basis measurement engine (Phase 2b) ────────────────────────────────

_H1 = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex) / np.sqrt(2.0)
_S_dag = np.array([[1.0, 0.0], [0.0, -1j]], dtype=complex)
_Uy1 = _H1 @ _S_dag  # Maps Y eigenstates to computational basis: Uy Y Uy† = Z

_sx_dense = np.array([[0, 1], [1, 0]], dtype=complex)
_sy_dense = np.array([[0, -1j], [1j, 0]], dtype=complex)
_sz_dense = np.array([[1, 0], [0, -1]], dtype=complex)
_i2_dense = np.eye(2, dtype=complex)

_XI_dense = np.kron(_sx_dense, _i2_dense)
_IX_dense = np.kron(_i2_dense, _sx_dense)
_XX_dense = np.kron(_sx_dense, _sx_dense)
_YY_dense = np.kron(_sy_dense, _sy_dense)
_ZZ_dense = np.kron(_sz_dense, _sz_dense)
_II_dense = np.eye(4, dtype=complex)


def get_basis_rotation_matrix(basis: str, n: int) -> np.ndarray:
    r"""
    Construct the 2^n × 2^n unitary rotation matrix for the chosen basis:
    - Basis 'X': H^{\otimes n}
    - Basis 'Y': (H S^\dagger)^{\otimes n}
    - Basis 'Z': I_{2^n}
    """
    b = basis.upper()
    if b == "Z":
        return np.eye(2**n, dtype=complex)
    elif b == "X":
        u1 = _H1
    elif b == "Y":
        u1 = _Uy1
    else:
        raise ValueError(f"Unknown basis: {basis!r}. Use 'X', 'Y', or 'Z'.")

    un = u1
    for _ in range(n - 1):
        un = np.kron(un, u1)
    return un


def sample_bitstrings_basis(
    psi: np.ndarray,
    n: int,
    basis: str,
    shots: int,
    rng: np.random.Generator,
    u_rot: np.ndarray = None,
) -> np.ndarray:
    """
    Sample `shots` bitstrings from the state |ψ⟩ measured in the specified basis.
    Returns array of shape (shots, n) with values in {0, 1}.
    Qubit 0 is the most significant tensor factor (big-endian).
    """
    if u_rot is None:
        u_rot = get_basis_rotation_matrix(basis, n)

    if basis.upper() == "Z":
        psi_rot = psi
    else:
        psi_rot = u_rot @ psi

    probs = np.abs(psi_rot) ** 2
    probs = np.maximum(probs, 0.0)
    p_sum = np.sum(probs)
    if p_sum > 0:
        probs /= p_sum
    else:
        probs = np.ones(2**n) / (2**n)

    indices = rng.choice(2**n, size=shots, p=probs)
    bitstrings = ((indices[:, None] >> np.arange(n - 1, -1, -1)) & 1).astype(np.int8)
    return bitstrings


def extract_basis_expectations(
    bitstrings_x: np.ndarray,
    bitstrings_y: np.ndarray,
    bitstrings_z: np.ndarray,
    n: int,
) -> dict:
    """
    Extract single-body and two-body expectation values from shared-basis bitstrings:
    - Basis X: <X_i> and nearest-neighbour <X_i X_{i+1}>
    - Basis Y: nearest-neighbour <Y_i Y_{i+1}> (<Y_i> projection noise also available)
    - Basis Z: <Z_i>, nearest-neighbour <Z_i Z_{i+1}>, and all pairs <Z_i Z_j> (i < j).
    """
    signs_x = 1.0 - 2.0 * bitstrings_x.astype(float)
    signs_y = 1.0 - 2.0 * bitstrings_y.astype(float)
    signs_z = 1.0 - 2.0 * bitstrings_z.astype(float)

    # Basis X
    exp_x = np.mean(signs_x, axis=0)  # (n,)
    exp_xx_nn = [float(np.mean(signs_x[:, i] * signs_x[:, i + 1])) for i in range(n - 1)]

    # Basis Y
    exp_y = np.mean(signs_y, axis=0)  # (n,)
    exp_yy_nn = [float(np.mean(signs_y[:, i] * signs_y[:, i + 1])) for i in range(n - 1)]

    # Basis Z
    exp_z = np.mean(signs_z, axis=0)  # (n,)
    exp_zz_nn = [float(np.mean(signs_z[:, i] * signs_z[:, i + 1])) for i in range(n - 1)]
    exp_zz_all = []
    for i in range(n):
        for j in range(i + 1, n):
            exp_zz_all.append(float(np.mean(signs_z[:, i] * signs_z[:, j])))

    return {
        "x": exp_x,
        "y": exp_y,
        "z": exp_z,
        "xx_nn": exp_xx_nn,
        "yy_nn": exp_yy_nn,
        "zz_nn": exp_zz_nn,
        "zz_all": exp_zz_all,
    }


def reconstruct_noisy_features_from_basis(exp_dict: dict, n: int) -> dict:
    """
    Reconstruct 1-RDMs, 2-RDMs, and classical features from the exact same
    sampled basis expectation values:
    - Noisy 1-RDMs: ρ_i = (I + <X_i> X + <Z_i> Z) / 2
    - Noisy 2-RDMs: nearest-neighbour Pauli reconstruction
    - Noisy E: [<X_i>, all <Z_i Z_j>] padded with 0 for Y and <Z_i> for consistency with full_corr
    - Noisy E2: 2pt_pauli_nn features (<X_i>, <X_j>, <XX>, <YY>, <ZZ>)
    """
    exp_x = exp_dict["x"]
    exp_z = exp_dict["z"]
    exp_xx_nn = exp_dict["xx_nn"]
    exp_yy_nn = exp_dict["yy_nn"]
    exp_zz_nn = exp_dict["zz_nn"]
    exp_zz_all = exp_dict["zz_all"]

    # 1-RDMs: (I + <X_i> X + <Z_i> Z) / 2
    rdms_1local = []
    for i in range(n):
        rho_1 = 0.5 * (_i2_dense + exp_x[i] * _sx_dense + exp_z[i] * _sz_dense)
        rdms_1local.append(rho_1)

    # 2-RDMs for nearest-neighbour pairs (i, i+1)
    # rho_{i, i+1} = (1/4) [ I + <X_i> (X (x) I) + <X_{i+1}> (I (x) X)
    #                         + <XX> (X (x) X) + <YY> (Y (x) Y) + <ZZ> (Z (x) Z) ]
    rdms_2local = {}
    feats_e2 = []
    for i in range(n - 1):
        j = i + 1
        xi = float(exp_x[i])
        xj = float(exp_x[j])
        xx = float(exp_xx_nn[i])
        yy = float(exp_yy_nn[i])
        zz = float(exp_zz_nn[i])

        rho_2 = 0.25 * (
            _II_dense
            + xi * _XI_dense
            + xj * _IX_dense
            + xx * _XX_dense
            + yy * _YY_dense
            + zz * _ZZ_dense
        )
        rdms_2local[(i, j)] = rho_2
        feats_e2.extend([xi, xj, xx, yy, zz])

    # E features: 52-dim format matching full_corr: [bx_k, by_k=0, bz_k] + [all ZZ]
    feats_e = []
    for i in range(n):
        feats_e.extend([float(exp_x[i]), 0.0, float(exp_z[i])])
    feats_e.extend(exp_zz_all)

    return {
        "rdms_1local": rdms_1local,
        "rdms_2local": rdms_2local,
        "e_features": np.array(feats_e, dtype=float),
        "e2_features": np.array(feats_e2, dtype=float),
        "bloch_x": np.array(exp_x, dtype=float),
        "bloch_z": np.array(exp_z, dtype=float),
    }


def destructive_swap_test_fidelity(K: np.ndarray, shots: int, rng: np.random.Generator):
    """
    Destructive swap-test simulation for an m × m fidelity matrix K:
    For each off-diagonal pair i < j:
        P_0 = (1 + K_{ij}) / 2
        N_0 ~ Binomial(shots, P_0)
        K̂_{ij} = 2 * (N_0 / shots) - 1
    Symmetrize: K̂_{ji} = K̂_{ij}, K̂_{ii} = 1.0.
    Returns (K_hat, lam_min).
    """
    m = K.shape[0]
    K_hat = np.eye(m, dtype=float)

    for i in range(m):
        for j in range(i + 1, m):
            p0 = float(np.clip((1.0 + K[i, j]) / 2.0, 0.0, 1.0))
            n0 = rng.binomial(shots, p0)
            k_val = 2.0 * (n0 / shots) - 1.0
            K_hat[i, j] = k_val
            K_hat[j, i] = k_val

    lam_min = float(np.min(np.linalg.eigvalsh(K_hat)))
    return K_hat, lam_min


def depolarize_state(psi: np.ndarray, p: float, n: int = None) -> np.ndarray:
    """
    Apply depolarizing channel to an n-qubit pure state |ψ⟩⟨ψ|:
        ρ(p) = (1 - p)^n |ψ⟩⟨ψ| + (1 - (1 - p)^n) (I / 2^n)
    """
    dim = len(psi)
    if n is None:
        n = int(round(np.log2(dim)))
    rho_pure = np.outer(psi, psi.conj())
    coeff = (1.0 - p) ** n
    return coeff * rho_pure + (1.0 - coeff) * (np.eye(dim, dtype=complex) / dim)


def mixed_state_fidelity_gram(states: list, p: float, n: int = 8) -> np.ndarray:
    """
    Compute the normalized mixed-state overlap matrix:
        K_{ij}(p) = Tr(ρ_i(p) ρ_j(p)) / sqrt(Tr(ρ_i(p)^2) Tr(ρ_j(p)^2))
    where ρ_i(p) = (1-p)^n |ψ_i⟩⟨ψ_i| + (1 - (1-p)^n) (I / 2^n).
    """
    dim = 2**n
    m = len(states)
    states_arr = np.asarray(states)
    K_pure = np.abs(states_arr @ states_arr.conj().T) ** 2

    if p == 0.0:
        return K_pure

    lam = 1.0 - (1.0 - p) ** n
    w_pure = (1.0 - lam) ** 2
    w_mix = (1.0 - w_pure) / dim
    denom = w_pure + w_mix

    K_mixed = (w_pure * K_pure + w_mix) / denom
    np.fill_diagonal(K_mixed, 1.0)
    return K_mixed

