# S1.5 Statistics and Manuscript Reconciliation

Status: COMPLETED (Automated Extraction & Bidirectional Numerical Audit)

## 1. Confirmatory Hypotheses Audit (results/stats.csv)

The 36 pre-registered confirmatory rows from `results/stats.csv`:

| Task | Target | Lattice | $N_{\text{tr}}$ | Metric | Pair ($a$ vs $b$) | Mean Diff | 95% Bootstrap CI | $p_{\text{holm}}$ | Flag |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| T1 | half_chain_entropy | chain | 40 | r2 | PQK-2nn vs E (raw) | -0.0083 | [-0.0132, -0.0041] | 1.1845e-03 | - |
| T1 | half_chain_entropy | chain | 40 | r2 | FQ vs E (raw) | +0.0031 | [0.0015, 0.0050] | 1.1845e-03 | - |
| T1 | half_chain_entropy | chain | 40 | r2 | PQK-1 vs PQK-2nn | -0.0803 | [-0.0950, -0.0662] | 1.5259e-05 | - |
| T1 | half_chain_entropy | chain | 160 | r2 | PQK-2nn vs E (raw) | -0.0044 | [-0.0051, -0.0038] | 1.5259e-05 | - |
| T1 | half_chain_entropy | chain | 160 | r2 | FQ vs E (raw) | -0.0012 | [-0.0015, -0.0009] | 1.5259e-05 | significant_but_tiny |
| T1 | half_chain_entropy | chain | 160 | r2 | PQK-1 vs PQK-2nn | -0.0414 | [-0.0437, -0.0391] | 1.5259e-05 | - |
| T2b | z0_z1_zn2_zn1 | chain | 40 | r2 | PQK-2nn vs E (raw) | -0.0019 | [-0.0142, 0.0097] | 1.0000e+00 | - |
| T2b | z0_z1_zn2_zn1 | chain | 40 | r2 | FQ vs E (raw) | +0.0242 | [0.0172, 0.0308] | 8.0109e-05 | - |
| T2b | z0_z1_zn2_zn1 | chain | 40 | r2 | PQK-1 vs PQK-2nn | -0.0544 | [-0.0719, -0.0376] | 9.5367e-05 | - |
| T2b | z0_z1_zn2_zn1 | chain | 160 | r2 | PQK-2nn vs E (raw) | -0.0001 | [-0.0004, 0.0001] | 1.0000e+00 | - |
| T2b | z0_z1_zn2_zn1 | chain | 160 | r2 | FQ vs E (raw) | +0.0000 | [-0.0002, 0.0003] | 1.0000e+00 | - |
| T2b | z0_z1_zn2_zn1 | chain | 160 | r2 | PQK-1 vs PQK-2nn | -0.0385 | [-0.0420, -0.0349] | 1.5259e-05 | - |
| T4a | sq_diff_sign | 2x4 | 40 | accuracy | PQK-2nn vs E (raw) | -0.0192 | [-0.0325, -0.0070] | 5.2460e-02 | - |
| T4a | sq_diff_sign | 2x4 | 40 | accuracy | FQ vs E (raw) | +0.0053 | [-0.0045, 0.0158] | 4.8554e-01 | - |
| T4a | sq_diff_sign | 2x4 | 40 | accuracy | PQK-1 vs PQK-2nn | -0.2218 | [-0.2450, -0.1975] | 7.0359e-04 | - |
| T4a | sq_diff_sign | 2x4 | 80 | accuracy | PQK-2nn vs E (raw) | -0.0127 | [-0.0210, -0.0055] | 1.8583e-02 | - |
| T4a | sq_diff_sign | 2x4 | 80 | accuracy | FQ vs E (raw) | +0.0008 | [-0.0037, 0.0053] | 6.6222e-01 | - |
| T4a | sq_diff_sign | 2x4 | 80 | accuracy | PQK-1 vs PQK-2nn | -0.1907 | [-0.2130, -0.1695] | 7.0160e-04 | - |
| T4a | sq_diff_sign | 3x4 | 40 | accuracy | PQK-2nn vs E (raw) | -0.0070 | [-0.0278, 0.0187] | 4.4114e-01 | - |
| T4a | sq_diff_sign | 3x4 | 40 | accuracy | FQ vs E (raw) | +0.0080 | [-0.0035, 0.0215] | 5.8517e-01 | - |
| T4a | sq_diff_sign | 3x4 | 40 | accuracy | PQK-1 vs PQK-2nn | -0.1470 | [-0.1740, -0.1245] | 6.9564e-04 | - |
| T4a | sq_diff_sign | 3x4 | 80 | accuracy | PQK-2nn vs E (raw) | -0.0067 | [-0.0147, 0.0013] | 3.3501e-01 | - |
| T4a | sq_diff_sign | 3x4 | 80 | accuracy | FQ vs E (raw) | +0.0005 | [-0.0055, 0.0067] | 9.2979e-01 | - |
| T4a | sq_diff_sign | 3x4 | 80 | accuracy | PQK-1 vs PQK-2nn | -0.0725 | [-0.0962, -0.0527] | 6.9762e-04 | - |
| T4b | half_cut_entropy | 2x4 | 40 | r2 | PQK-2nn vs E (raw) | -0.0076 | [-0.0205, 0.0079] | 5.9151e-02 | - |
| T4b | half_cut_entropy | 2x4 | 40 | r2 | FQ vs E (raw) | -0.0320 | [-0.0622, -0.0053] | 1.2611e-02 | - |
| T4b | half_cut_entropy | 2x4 | 40 | r2 | PQK-1 vs PQK-2nn | -0.0775 | [-0.1634, -0.0274] | 2.1744e-04 | - |
| T4b | half_cut_entropy | 2x4 | 80 | r2 | PQK-2nn vs E (raw) | -0.0017 | [-0.0030, -0.0005] | 9.6882e-02 | significant_but_tiny |
| T4b | half_cut_entropy | 2x4 | 80 | r2 | FQ vs E (raw) | -0.0119 | [-0.0161, -0.0082] | 1.5259e-05 | - |
| T4b | half_cut_entropy | 2x4 | 80 | r2 | PQK-1 vs PQK-2nn | -0.0461 | [-0.0543, -0.0377] | 1.5259e-05 | - |
| T4b | half_cut_entropy | 3x4 | 40 | r2 | PQK-2nn vs E (raw) | -0.0054 | [-0.0172, 0.0013] | 1.0000e+00 | - |
| T4b | half_cut_entropy | 3x4 | 40 | r2 | FQ vs E (raw) | -0.0002 | [-0.0018, 0.0014] | 1.0000e+00 | - |
| T4b | half_cut_entropy | 3x4 | 40 | r2 | PQK-1 vs PQK-2nn | -0.0233 | [-0.0409, -0.0089] | 4.8256e-03 | - |
| T4b | half_cut_entropy | 3x4 | 80 | r2 | PQK-2nn vs E (raw) | +0.0001 | [-0.0004, 0.0005] | 1.0000e+00 | - |
| T4b | half_cut_entropy | 3x4 | 80 | r2 | FQ vs E (raw) | +0.0003 | [-0.0000, 0.0007] | 1.0000e+00 | - |
| T4b | half_cut_entropy | 3x4 | 80 | r2 | PQK-1 vs PQK-2nn | -0.0107 | [-0.0148, -0.0072] | 3.0518e-05 | - |

## 2. Maximum Discrepancy Across Sample Budgets

| Task | Target | Lattice | Model Pair | Max $|\text{Mean Diff}|$ ($N \le 40$) | Max $|\text{Mean Diff}|$ ($N \ge 80$) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| T1 | half_chain_entropy | chain | FQ vs E (raw) | 0.0611 | 0.0019 |
| T1 | half_chain_entropy | chain | PQK-2nn vs E (raw) | 0.0215 | 0.0066 |
| T1 | half_chain_entropy | chain | FQ vs PQK-2nn | 0.0396 | 0.0047 |
| T2a | z0_zn | chain | FQ vs E (raw) | 0.1453 | 0.0076 |
| T2a | z0_zn | chain | PQK-2nn vs E (raw) | 0.2668 | 0.0754 |
| T2a | z0_zn | chain | FQ vs PQK-2nn | 0.1507 | 0.0679 |
| T2b | z0_z1_zn2_zn1 | chain | FQ vs E (raw) | 0.0897 | 0.0044 |
| T2b | z0_z1_zn2_zn1 | chain | PQK-2nn vs E (raw) | 0.1034 | 0.0025 |
| T2b | z0_z1_zn2_zn1 | chain | FQ vs PQK-2nn | 0.1930 | 0.0019 |
| T4a | sq_diff_sign | 2x4 | FQ vs E (raw) | 0.0450 | 0.0008 |
| T4a | sq_diff_sign | 2x4 | PQK-2nn vs E (raw) | 0.0442 | 0.0127 |
| T4a | sq_diff_sign | 2x4 | FQ vs PQK-2nn | 0.0892 | 0.0135 |
| T4a | sq_diff_sign | 3x4 | FQ vs E (raw) | 0.0337 | 0.0005 |
| T4a | sq_diff_sign | 3x4 | PQK-2nn vs E (raw) | 0.0442 | 0.0067 |
| T4a | sq_diff_sign | 3x4 | FQ vs PQK-2nn | 0.0780 | 0.0073 |
| T4b | half_cut_entropy | 2x4 | FQ vs E (raw) | 0.2004 | 0.0119 |
| T4b | half_cut_entropy | 2x4 | PQK-2nn vs E (raw) | 0.2204 | 0.0017 |
| T4b | half_cut_entropy | 2x4 | FQ vs PQK-2nn | 0.0380 | 0.0102 |
| T4b | half_cut_entropy | 3x4 | FQ vs E (raw) | 0.1032 | 0.0003 |
| T4b | half_cut_entropy | 3x4 | PQK-2nn vs E (raw) | 0.0671 | 0.0001 |
| T4b | half_cut_entropy | 3x4 | FQ vs PQK-2nn | 0.0822 | 0.0002 |

## 3. Specifically Tested Bound: $|\Delta R^2| \le 0.011$ at $N \ge 80$

**CONTRADICTED:** The assertion in the manuscript that all differences between top performers remain $\le 0.011$ at large sample sizes is exceeded by **7** data row(s):

| Task | Target | Lattice | $N_{\text{tr}}$ | Pair | Mean Diff | Absolute Diff | Stated Bound |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| T2a | z0_zn | chain | 80 | PQK-2nn vs E (raw) | -0.075433 | 0.075433 | 0.011000 |
| T2a | z0_zn | chain | 80 | PQK-2nn vs FQ | -0.067878 | 0.067878 | 0.011000 |
| T2a | z0_zn | chain | 160 | PQK-2nn vs E (raw) | -0.035404 | 0.035404 | 0.011000 |
| T2a | z0_zn | chain | 160 | PQK-2nn vs FQ | -0.034005 | 0.034005 | 0.011000 |
| T4a | sq_diff_sign | 2x4 | 80 | PQK-2nn vs E (raw) | -0.012750 | 0.012750 | 0.011000 |
| T4a | sq_diff_sign | 2x4 | 80 | PQK-2nn vs FQ | -0.013500 | 0.013500 | 0.011000 |
| T4b | half_cut_entropy | 2x4 | 80 | FQ vs E (raw) | -0.011928 | 0.011928 | 0.011000 |

> [!WARNING]
> **Claim C2 Inconsistency:** Task 4b (2x4 lattice) at $N_{\text{tr}}=80$ exhibits a mean difference of $-0.011928$ between FQ and E (raw). The absolute difference $|\Delta R^2| = 0.011928$ strictly exceeds the stated upper bound $0.011$.

## 4. Manuscript Numerical Claims Audit

- Total numeric claims extracted: **251**
- Verified against underlying data (tolerance $\le 5 \times 10^-5$): **245**
- Contradicted by data: **1**
- Unmatched (e.g. narrative constants, section numbers, degrees): **5**

### Contradicted Claims

| Claim ID | Location | Number | Stated Claim | Discrepancy Notes |
| :---: | :---: | :---: | :--- | :--- |
| CLM-018 | `paper/main.tex:139` | 0.011 | \item \textbf{FQ vs Classical Correlator Ordering (Claim C2):} At $N_{\text{tr}}=40$, the performance hierarchy is $\text{FQ} > \text{E (raw | Bound <= 0.011 R2 contradicted by T4b 2x4 N=80 FQ vs E (raw) mean_diff = -0.011928 (|diff|=0.0119 > 0.011) |
