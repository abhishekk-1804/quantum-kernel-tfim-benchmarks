"""
scripts/ablation_r3_repairs.py
------------------------------
Gram matrix repair functions for finite-shot noisy quantum kernel benchmarks (Issue R3).

Implements four post-processing strategies:
1. repair_none: Identity map (unrepaired raw noisy Gram).
2. repair_train_only: Projects training Gram onto the PSD cone via fidelity_clip_psd;
   leaves test-train evaluation block completely unclipped (current production baseline).
3. repair_inductive: Eigendecomposes training Gram K_tr = U L U^T, clips negative
   eigenvalues, and filters test evaluations via K_te' = K_te U diag(f) U^T where
   f_i = L_clip_i / L_i if L_i > tol else 0. Rescales both blocks consistently to
   maintain unit diagonal on K_tr'.
   - Tolerance & Handling: For L_i <= tol (where tol=1e-10 by default), f_i is set
     strictly to 0.0. This handles both negative eigenvalues (whose clipped value
     is 0.0) and near-zero singular eigenvalues (preventing numerical division by
     tiny numbers).
   - Inductive Property: Test points are transformed strictly through the training
     eigenbasis and diagonal normalizer, preserving strict row-wise test independence.
4. repair_joint: Projects the full (N_tr + N_te) joint Gram matrix onto the PSD cone,
   then slices into train and test-train blocks.
   - TRANSDUCTIVE PROPERTY: Modifying a test state alters the resulting training Gram
     block K_tr'. It requires simultaneous access to all test states and is not
     strictly inductive.
"""

import os
import sys
from typing import Tuple

import numpy as np

# Add src to path
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC = os.path.join(_PROJECT_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from noise import fidelity_clip_psd


def repair_none(K_tr: np.ndarray, K_te: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Unrepaired noisy Gram matrices (Raw).
    """
    return K_tr.copy(), K_te.copy()


def repair_train_only(K_tr: np.ndarray, K_te: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Train-only clipping (Current production method in run_t5_noise.py).
    Projects K_tr onto PSD cone; leaves K_te unclipped.
    """
    K_tr_clipped = fidelity_clip_psd(K_tr)
    return K_tr_clipped, K_te.copy()


def repair_inductive(
    K_tr: np.ndarray, K_te: np.ndarray, tol: float = 1e-10
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Inductive Gram repair.
    
    Eigendecomposes symmetrized K_tr = U diag(L) U^T.
    Clips eigenvalues L_clip = max(L, 0).
    Filters test predictions via K_te' = K_te U diag(f) U^T with:
        f_i = L_clip_i / L_i  if L_i > tol else 0.0.
    
    Tolerance and Handling:
    - If L_i <= tol (negative or near-zero eigenvalues), f_i is set to 0.0,
      projecting the test evaluation onto the positive eigenspace of K_tr.
    
    Rescaling:
    - Normalizes K_tr' and K_te' using diagonal congruence factor D^{-1/2} from K_tr',
      ensuring diag(K_tr'') == 1.0 and keeping K_te'' scaled consistently.
    """
    K_sym = 0.5 * (K_tr + K_tr.T)
    evals, U = np.linalg.eigh(K_sym)
    evals_clip = np.maximum(evals, 0.0)

    # Filter factors: for evals > tol, evals_clip / evals == 1.0; for evals <= tol, 0.0
    f = np.where(evals > tol, evals_clip / np.maximum(evals, 1e-14), 0.0)

    K_tr_prime = U @ np.diag(evals_clip) @ U.T
    K_te_prime = K_te @ U @ np.diag(f) @ U.T

    # Rescale consistently to maintain unit diagonal on K_tr_prime
    diag_tr = np.maximum(np.diag(K_tr_prime), 1e-14)
    D_inv_sqrt = 1.0 / np.sqrt(diag_tr)

    K_tr_out = D_inv_sqrt[:, None] * K_tr_prime * D_inv_sqrt[None, :]
    np.fill_diagonal(K_tr_out, 1.0)
    K_tr_out = 0.5 * (K_tr_out + K_tr_out.T)

    K_te_out = K_te_prime * D_inv_sqrt[None, :]
    return K_tr_out, K_te_out


def repair_joint(K_full: np.ndarray, N_tr: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Joint Gram repair (TRANSDUCTIVE).
    
    Projects full (N_tr + N_te) joint Gram matrix onto PSD cone via fidelity_clip_psd,
    then slices into train and test blocks.
    
    Warning: This method is transductive because test states affect K_tr'.
    """
    K_full_clipped = fidelity_clip_psd(K_full)
    K_tr_out = K_full_clipped[:N_tr, :N_tr]
    K_te_out = K_full_clipped[N_tr:, :N_tr]
    return K_tr_out, K_te_out
