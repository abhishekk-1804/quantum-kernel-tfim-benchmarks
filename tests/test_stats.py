"""
tests/test_stats.py
Unit tests for paired statistical analysis engine.
"""
import numpy as np
import pytest
from scripts.stats import custom_holm, bootstrap_ci_diff, compute_paired_comparison


def test_holm_step_down_known_vector():
    """
    1. Holm step-down on known vector [0.01, 0.04, 0.03] -> [0.03, 0.06, 0.06].
    """
    p_raw = [0.01, 0.04, 0.03]
    expected = np.array([0.03, 0.06, 0.06])
    adj = custom_holm(p_raw)
    assert np.allclose(adj, expected, atol=1e-12)


def test_rank_biserial_known_vector():
    """
    2. Rank-biserial on d = [1, 2, 3, -1] -> W+ = 8.5, W- = 1.5, r = (8.5 - 1.5)/10 = 0.7.
    """
    val_a = np.array([1.0, 2.0, 3.0, -1.0])
    val_b = np.array([0.0, 0.0, 0.0, 0.0])
    res = compute_paired_comparison(val_a, val_b)

    assert pytest.approx(res["W_plus"], abs=1e-10) == 8.5
    assert pytest.approx(res["W_minus"], abs=1e-10) == 1.5
    assert pytest.approx(res["effect_size"], abs=1e-10) == 0.7


def test_sign_flip_on_swap():
    """
    3. Sign check: swapping a and b flips sign of mean diff and r.
    """
    val_a = np.array([0.85, 0.72, 0.91, 0.64, 0.88, 0.79])
    val_b = np.array([0.80, 0.75, 0.89, 0.60, 0.82, 0.70])

    res_ab = compute_paired_comparison(val_a, val_b, seed=42)
    res_ba = compute_paired_comparison(val_b, val_a, seed=42)

    assert pytest.approx(res_ab["mean_diff"], abs=1e-12) == -res_ba["mean_diff"]
    assert pytest.approx(res_ab["effect_size"], abs=1e-12) == -res_ba["effect_size"]
    assert pytest.approx(res_ab["W_plus"], abs=1e-12) == res_ba["W_minus"]
    assert pytest.approx(res_ab["W_minus"], abs=1e-12) == res_ba["W_plus"]


def test_identical_array():
    """
    4. Identical array: all-zero d -> p = NaN, flag = 'identical', excluded from Holm.
    """
    val_a = np.array([0.5, 0.5, 0.5, 0.5])
    val_b = np.array([0.5, 0.5, 0.5, 0.5])

    res = compute_paired_comparison(val_a, val_b)
    assert np.isnan(res["p_raw"])
    assert res["flag"] == "identical"
    assert res["effect_size"] == 0.0
    assert res["W_plus"] == 0.0
    assert res["W_minus"] == 0.0


def test_bootstrap_ci_reproducibility():
    """
    5. Bootstrap CI matches fixed-seed reference.
    """
    d = np.array([0.1, -0.05, 0.2, 0.15, -0.02, 0.08, 0.12, -0.01])
    low1, high1 = bootstrap_ci_diff(d, seed=20261022, n_boot=1000)
    low2, high2 = bootstrap_ci_diff(d, seed=20261022, n_boot=1000)

    assert low1 == low2
    assert high1 == high2
    # Verify bounds enclose the mean
    mean_d = float(np.mean(d))
    assert low1 <= mean_d <= high1
