r"""
test_reproduction_driver.py — Pytest suite for Stage 4 reproduction driver.
Workspace: D:\quantum-kernel-tfim-benchmarks
Interpreter: D:\qml_env\Scripts\python.exe

Tests the 5 core checks in reproduction_driver.py without modifying any repository files.
"""

import os
import sys
import pytest

# Add reproduction_driver directory to sys.path
DRIVER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if DRIVER_DIR not in sys.path:
    sys.path.insert(0, DRIVER_DIR)

import reproduction_driver as rd

def test_check_1_input_availability():
    """Verify check 1 succeeds without assertion errors."""
    assert rd.check_1_input_availability() is True

def test_check_2_physics_rdm_and_features():
    """Verify check 2 computes RDM and features correctly."""
    assert rd.check_2_physics_rdm_and_features() is True

def test_check_3_symmetry_properties():
    """Verify check 3 enforces Z_2 parity symmetry."""
    assert rd.check_3_symmetry_properties() is True

def test_check_4_stage2_budget_arithmetic():
    """Verify check 4 confirms budget formulas."""
    assert rd.check_4_stage2_budget_arithmetic() is True

def test_check_5_t6_array_csv_agreement():
    """Verify check 5 confirms array-to-CSV agreement within atol=1e-7."""
    assert rd.check_5_t6_array_csv_agreement() is True
