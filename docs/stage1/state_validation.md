# S1.7 Ground-State Solver Validation Report

Status: COMPLETED (Verification across system sizes $n \in \{4, 6, 8, 10, 12, 14\}$)

## 1. Summary of Validation Assertions

| System Size $n$ | Instances Tested | Max Residual $\|H \psi - E \psi\|_2$ | Max $|\Delta E|$ (Sparse vs Dense) | Parity Range | Norm Range | Max $|\text{Im} \psi|$ | Gate Result |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 4 | 10 | 1.55e-14 | 1.33e-14 | [1.00000000, 1.00000000] | [1.00000000, 1.00000000] | 0.00e+00 | **PASS** |
| 6 | 10 | 2.85e-14 | 3.11e-14 | [1.00000000, 1.00000000] | [1.00000000, 1.00000000] | 0.00e+00 | **PASS** |
| 8 | 10 | 2.65e-14 | 3.20e-14 | [1.00000000, 1.00000000] | [1.00000000, 1.00000000] | 0.00e+00 | **PASS** |
| 10 | 10 | 2.20e-14 | 3.20e-14 | [1.00000000, 1.00000000] | [1.00000000, 1.00000000] | 0.00e+00 | **PASS** |
| 12 | 10 | 7.79e-14 | 1.35e-13 | [1.00000000, 1.00000000] | [1.00000000, 1.00000000] | 0.00e+00 | **PASS** |
| 14 | 10 | 4.82e-14 | N/A | [1.00000000, 1.00000000] | [1.00000000, 1.00000000] | 0.00e+00 | **PASS** |

## 2. Near-Degenerate Instances (In-Sector Gap $< 10^{-3}$)

Total near-degenerate instances observed: **0** / 60

No instances with in-sector gap $< 10^{-3}$ were observed across the evaluated ensemble.

## 3. Symmetry-Break Cross-Check

Cross-checking the even-sector projected solution against the full-space solver with a tiny longitudinal pinning field ($h = 10^{-6}$):
- Minimum ground state overlap |<psi_sector | psi_sb>|: **1.000000**
- Maximum ground state overlap |<psi_sector | psi_sb>|: **1.000000**
