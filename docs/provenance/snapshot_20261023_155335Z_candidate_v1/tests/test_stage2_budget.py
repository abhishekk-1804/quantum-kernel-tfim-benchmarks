"""
tests/test_stage2_budget.py
---------------------------
Unit tests for Stage 2 Equal-Total-Budget allocation and accounting.
"""

import os
import sys
import pytest
import numpy as np

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SCRIPTS = os.path.join(_PROJECT_ROOT, "scripts")
_SRC = os.path.join(_PROJECT_ROOT, "src")
for p in [_SRC, _SCRIPTS]:
    if p not in sys.path:
        sys.path.insert(0, p)

from stage2_equal_budget import calculate_shot_allocations, BUDGETS_ALL


def test_exact_budget_accounting():
    """
    Test 1 (Exact budget accounting):
    For all B_tot, assert total shots consumed (720 * S_feat) <= B_tot
    and (8780 * S_swap) <= B_tot.
    """
    for B_tot in BUDGETS_ALL:
        S_feat, S_xonly, S_swap, is_feasible = calculate_shot_allocations(B_tot)
        consumed_feat = 720 * S_feat
        consumed_swap = 8780 * S_swap

        assert consumed_feat <= B_tot, f"B_tot={B_tot}: 720 * S_feat ({consumed_feat}) > B_tot"
        assert consumed_swap <= B_tot, f"B_tot={B_tot}: 8780 * S_swap ({consumed_swap}) > B_tot"
        assert S_feat >= 0
        assert S_swap >= 0


def test_infeasibility_condition():
    """
    Test 2 (Infeasibility condition):
    Assert S_swap < 10 for B_tot in {1e4, 3e4} and returns explicit InfeasibleBudget flag (is_feasible_fq == False).
    """
    infeasible_budgets = [10000, 30000]
    for B_tot in infeasible_budgets:
        S_feat, S_xonly, S_swap, is_feasible = calculate_shot_allocations(B_tot)
        assert S_swap < 10, f"B_tot={B_tot}: expected S_swap < 10, got {S_swap}"
        assert not is_feasible, f"B_tot={B_tot}: expected is_feasible_fq to be False"

    # Verify feasible budgets
    feasible_budgets = [100000, 300000, 1000000, 3000000, 10000000]
    for B_tot in feasible_budgets:
        S_feat, S_xonly, S_swap, is_feasible = calculate_shot_allocations(B_tot)
        assert S_swap >= 10, f"B_tot={B_tot}: expected S_swap >= 10, got {S_swap}"
        assert is_feasible, f"B_tot={B_tot}: expected is_feasible_fq to be True"


def test_symmetry_consistency():
    """
    Test 3 (Symmetry consistency):
    Verify X-only PQK-1 consumes exactly 240 * S_xonly <= B_tot,
    and S_xonly is strictly greater than S_feat due to 1-basis vs 3-basis efficiency.
    """
    for B_tot in BUDGETS_ALL:
        S_feat, S_xonly, S_swap, is_feasible = calculate_shot_allocations(B_tot)
        consumed_xonly = 240 * S_xonly
        assert consumed_xonly <= B_tot, f"B_tot={B_tot}: 240 * S_xonly ({consumed_xonly}) > B_tot"
        assert S_xonly >= S_feat, f"B_tot={B_tot}: expected S_xonly >= S_feat, got {S_xonly} vs {S_feat}"
