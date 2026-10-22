# Phase 3 Summary: Paired Statistics and Benchmark Metrics

## 1. Paired Statistics Evaluation Summary Counts

| Metric / Item | Value |
| :--- | :--- |
| Total Paired Statistical Tests | 248 |
| Confirmatory Tests | 36 |
| Exploratory Tests | 212 |
| Excluded T4a Degenerate/Skipped Seeds | 0 |
| Max Absolute Difference Custom Holm vs statsmodels | 0.00e+00 |
| Holm Assertion Threshold | < 1e-12 |

### Family Sizes for p_holm_family

| Family (Task, Target, Lattice, Metric) | Total Tests | Valid Tests (p_raw not NaN) | Identical Excluded |
| :--- | :--- | :--- | :--- |
| (T1, half_chain_entropy, chain, r2) | 40 | 40 | 0 |
| (T2a, z0_zn, chain, r2) | 40 | 40 | 0 |
| (T2b, z0_z1_zn2_zn1, chain, r2) | 40 | 40 | 0 |
| (T4a, sq_diff_sign, 2x4, accuracy) | 32 | 32 | 0 |
| (T4a, sq_diff_sign, 3x4, accuracy) | 32 | 32 | 0 |
| (T4b, half_cut_entropy, 2x4, r2) | 32 | 32 | 0 |
| (T4b, half_cut_entropy, 3x4, r2) | 32 | 32 | 0 |
| **Sum of Family Sizes** | **248** | | |

## 2. Paired Comparisons with p_holm_perN < 0.05

Grouped by Task, then Tier (Confirmatory first, then Exploratory).

| Task | Tier | Lattice | N | Metric | Model A | Model B | Mean Diff | 95% Bootstrap CI | W+ | W- | p_raw | p_holm_perN | p_holm_family | Rank-Biserial r | Flag |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | confirmatory | chain | 40 | r2 | FQ | E (raw) | +0.0031 | [+0.0015, +0.0050] | 192.0 | 18.0 | 4.8256e-04 | 0.0012 | 0.0053 | +0.8286 |  |
| T1 | confirmatory | chain | 40 | r2 | PQK-1 | PQK-2nn | -0.0803 | [-0.0950, -0.0662] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T1 | confirmatory | chain | 40 | r2 | PQK-2nn | E (raw) | -0.0083 | [-0.0132, -0.0041] | 17.0 | 193.0 | 3.9482e-04 | 0.0012 | 0.0047 | -0.8381 |  |
| T1 | confirmatory | chain | 160 | r2 | FQ | E (raw) | -0.0012 | [-0.0015, -0.0009] | 2.0 | 208.0 | 5.7220e-06 | 1.5259e-05 | 1.0300e-04 | -0.9810 | significant_but_tiny |
| T1 | confirmatory | chain | 160 | r2 | PQK-1 | PQK-2nn | -0.0414 | [-0.0437, -0.0391] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T1 | confirmatory | chain | 160 | r2 | PQK-2nn | E (raw) | -0.0044 | [-0.0051, -0.0038] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T1 | exploratory | chain | 10 | r2 | PQK-1 | E (raw) | -0.0828 | [-0.1431, -0.0127] | 28.0 | 182.0 | 0.0027 | 0.0190 | 0.0217 | -0.7333 |  |
| T1 | exploratory | chain | 10 | r2 | PQK-1 | PQK-2nn | -0.1044 | [-0.1564, -0.0520] | 27.0 | 183.0 | 0.0023 | 0.0186 | 0.0209 | -0.7429 |  |
| T1 | exploratory | chain | 20 | r2 | E (raw) | E (std) | +0.0481 | [+0.0329, +0.0665] | 209.0 | 1.0 | 3.8147e-06 | 1.9073e-05 | 7.6294e-05 | +0.9905 |  |
| T1 | exploratory | chain | 20 | r2 | E (raw) | E2 (raw) | +0.0194 | [+0.0108, +0.0301] | 202.0 | 8.0 | 4.7684e-05 | 1.0872e-04 | 6.6757e-04 | +0.9238 |  |
| T1 | exploratory | chain | 20 | r2 | E (raw) | F (std) | +0.0470 | [+0.0354, +0.0593] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | +1.0000 |  |
| T1 | exploratory | chain | 20 | r2 | FQ | E (raw) | +0.0042 | [+0.0012, +0.0071] | 174.0 | 36.0 | 0.0083 | 0.0083 | 0.0582 | +0.6571 |  |
| T1 | exploratory | chain | 20 | r2 | PQK-1 | E (raw) | -0.1189 | [-0.1392, -0.1001] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T1 | exploratory | chain | 20 | r2 | PQK-1 | PQK-2nn | -0.0990 | [-0.1198, -0.0804] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T1 | exploratory | chain | 20 | r2 | PQK-2nn | E (raw) | -0.0199 | [-0.0315, -0.0109] | 7.0 | 203.0 | 3.6240e-05 | 1.0872e-04 | 5.4359e-04 | -0.9333 |  |
| T1 | exploratory | chain | 20 | r2 | PQK-2nn | FQ | -0.0240 | [-0.0358, -0.0150] | 1.0 | 209.0 | 3.8147e-06 | 1.9073e-05 | 7.6294e-05 | -0.9905 |  |
| T1 | exploratory | chain | 40 | r2 | E (raw) | E (std) | +0.0071 | [+0.0047, +0.0096] | 205.0 | 5.0 | 1.9073e-05 | 7.6294e-05 | 3.0518e-04 | +0.9524 |  |
| T1 | exploratory | chain | 40 | r2 | E (raw) | E2 (raw) | +0.0085 | [+0.0042, +0.0136] | 187.0 | 23.0 | 0.0012 | 0.0012 | 0.0121 | +0.7810 |  |
| T1 | exploratory | chain | 40 | r2 | E (raw) | F (std) | +0.0144 | [+0.0088, +0.0214] | 206.0 | 4.0 | 1.3351e-05 | 6.6757e-05 | 2.2697e-04 | +0.9619 |  |
| T1 | exploratory | chain | 40 | r2 | PQK-1 | E (raw) | -0.0886 | [-0.1021, -0.0763] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T1 | exploratory | chain | 40 | r2 | PQK-2nn | FQ | -0.0114 | [-0.0162, -0.0075] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T1 | exploratory | chain | 80 | r2 | E (raw) | E (std) | +0.0035 | [+0.0027, +0.0044] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | +1.0000 |  |
| T1 | exploratory | chain | 80 | r2 | E (raw) | E2 (raw) | +0.0066 | [+0.0056, +0.0077] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | +1.0000 |  |
| T1 | exploratory | chain | 80 | r2 | E (raw) | F (std) | +0.0114 | [+0.0100, +0.0128] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | +1.0000 |  |
| T1 | exploratory | chain | 80 | r2 | FQ | E (raw) | -0.0019 | [-0.0027, -0.0012] | 10.0 | 200.0 | 8.2016e-05 | 8.2016e-05 | 0.0011 | -0.9048 | significant_but_tiny |
| T1 | exploratory | chain | 80 | r2 | PQK-1 | E (raw) | -0.0655 | [-0.0734, -0.0585] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T1 | exploratory | chain | 80 | r2 | PQK-1 | PQK-2nn | -0.0589 | [-0.0669, -0.0518] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T1 | exploratory | chain | 80 | r2 | PQK-2nn | E (raw) | -0.0066 | [-0.0075, -0.0058] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T1 | exploratory | chain | 80 | r2 | PQK-2nn | FQ | -0.0047 | [-0.0059, -0.0035] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T1 | exploratory | chain | 160 | r2 | E (raw) | E (std) | +0.0022 | [+0.0019, +0.0026] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | +1.0000 |  |
| T1 | exploratory | chain | 160 | r2 | E (raw) | E2 (raw) | +0.0045 | [+0.0038, +0.0053] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | +1.0000 |  |
| T1 | exploratory | chain | 160 | r2 | E (raw) | F (std) | +0.0101 | [+0.0093, +0.0109] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | +1.0000 |  |
| T1 | exploratory | chain | 160 | r2 | PQK-1 | E (raw) | -0.0458 | [-0.0482, -0.0435] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T1 | exploratory | chain | 160 | r2 | PQK-2nn | FQ | -0.0032 | [-0.0039, -0.0025] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T2a | exploratory | chain | 10 | r2 | E (raw) | E2 (raw) | +0.2786 | [+0.1988, +0.3744] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | +1.0000 |  |
| T2a | exploratory | chain | 10 | r2 | FQ | E (raw) | -0.1453 | [-0.2384, -0.0518] | 31.0 | 179.0 | 0.0042 | 0.0211 | 0.0549 | -0.7048 |  |
| T2a | exploratory | chain | 10 | r2 | PQK-1 | E (raw) | -0.2612 | [-0.3540, -0.1807] | 2.0 | 208.0 | 5.7220e-06 | 4.0054e-05 | 1.0872e-04 | -0.9810 |  |
| T2a | exploratory | chain | 10 | r2 | PQK-2nn | E (raw) | -0.2668 | [-0.3674, -0.1802] | 3.0 | 207.0 | 9.5367e-06 | 5.7220e-05 | 1.7166e-04 | -0.9714 |  |
| T2a | exploratory | chain | 20 | r2 | E (raw) | E2 (raw) | +0.2533 | [+0.1874, +0.3299] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | +1.0000 |  |
| T2a | exploratory | chain | 20 | r2 | FQ | E (raw) | -0.1076 | [-0.1781, -0.0451] | 20.0 | 190.0 | 7.0763e-04 | 0.0028 | 0.0099 | -0.8095 |  |
| T2a | exploratory | chain | 20 | r2 | PQK-1 | E (raw) | -0.2166 | [-0.2961, -0.1451] | 3.0 | 207.0 | 9.5367e-06 | 5.7220e-05 | 1.7166e-04 | -0.9714 |  |
| T2a | exploratory | chain | 20 | r2 | PQK-2nn | E (raw) | -0.2583 | [-0.3345, -0.1929] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T2a | exploratory | chain | 20 | r2 | PQK-2nn | FQ | -0.1507 | [-0.2044, -0.0995] | 6.0 | 204.0 | 2.6703e-05 | 1.3351e-04 | 4.2725e-04 | -0.9429 |  |
| T2a | exploratory | chain | 40 | r2 | E (raw) | E2 (raw) | +0.1228 | [+0.1015, +0.1467] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | +1.0000 |  |
| T2a | exploratory | chain | 40 | r2 | FQ | E (raw) | -0.0290 | [-0.0361, -0.0228] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T2a | exploratory | chain | 40 | r2 | PQK-1 | E (raw) | -0.1159 | [-0.1354, -0.0987] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T2a | exploratory | chain | 40 | r2 | PQK-2nn | E (raw) | -0.1250 | [-0.1490, -0.1040] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T2a | exploratory | chain | 40 | r2 | PQK-2nn | FQ | -0.0960 | [-0.1164, -0.0781] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T2a | exploratory | chain | 80 | r2 | E (raw) | E2 (raw) | +0.0747 | [+0.0614, +0.0900] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | +1.0000 |  |
| T2a | exploratory | chain | 80 | r2 | E (raw) | F (std) | -0.0003 | [-0.0004, -0.0002] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 | significant_but_tiny |
| T2a | exploratory | chain | 80 | r2 | FQ | E (raw) | -0.0076 | [-0.0098, -0.0059] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T2a | exploratory | chain | 80 | r2 | PQK-1 | E (raw) | -0.0903 | [-0.1089, -0.0741] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T2a | exploratory | chain | 80 | r2 | PQK-2nn | E (raw) | -0.0754 | [-0.0920, -0.0611] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T2a | exploratory | chain | 80 | r2 | PQK-2nn | FQ | -0.0679 | [-0.0842, -0.0537] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T2a | exploratory | chain | 160 | r2 | E (raw) | E (std) | -0.0000 | [-0.0000, -0.0000] | 16.0 | 194.0 | 3.2234e-04 | 3.2234e-04 | 0.0048 | -0.8476 | significant_but_tiny |
| T2a | exploratory | chain | 160 | r2 | E (raw) | E2 (raw) | +0.0354 | [+0.0307, +0.0400] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | +1.0000 |  |
| T2a | exploratory | chain | 160 | r2 | E (raw) | F (std) | -0.0000 | [-0.0000, -0.0000] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 | significant_but_tiny |
| T2a | exploratory | chain | 160 | r2 | FQ | E (raw) | -0.0014 | [-0.0016, -0.0012] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 | significant_but_tiny |
| T2a | exploratory | chain | 160 | r2 | PQK-1 | E (raw) | -0.0583 | [-0.0661, -0.0507] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T2a | exploratory | chain | 160 | r2 | PQK-1 | PQK-2nn | -0.0229 | [-0.0279, -0.0178] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T2a | exploratory | chain | 160 | r2 | PQK-2nn | E (raw) | -0.0354 | [-0.0401, -0.0307] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T2a | exploratory | chain | 160 | r2 | PQK-2nn | FQ | -0.0340 | [-0.0387, -0.0293] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T2b | confirmatory | chain | 40 | r2 | FQ | E (raw) | +0.0242 | [+0.0172, +0.0308] | 206.0 | 4.0 | 1.3351e-05 | 8.0109e-05 | 3.7384e-04 | +0.9619 |  |
| T2b | confirmatory | chain | 40 | r2 | PQK-1 | PQK-2nn | -0.0544 | [-0.0719, -0.0376] | 5.0 | 205.0 | 1.9073e-05 | 9.5367e-05 | 4.9591e-04 | -0.9524 |  |
| T2b | confirmatory | chain | 160 | r2 | PQK-1 | PQK-2nn | -0.0385 | [-0.0420, -0.0349] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T2b | exploratory | chain | 10 | r2 | PQK-1 | E (raw) | -0.1319 | [-0.1964, -0.0740] | 6.0 | 204.0 | 2.6703e-05 | 2.1362e-04 | 6.6757e-04 | -0.9429 |  |
| T2b | exploratory | chain | 10 | r2 | PQK-2nn | FQ | -0.1930 | [-0.3140, -0.0873] | 22.0 | 188.0 | 0.0010 | 0.0071 | 0.0213 | -0.7905 |  |
| T2b | exploratory | chain | 20 | r2 | E (raw) | E (std) | +0.0543 | [+0.0273, +0.0798] | 187.0 | 23.0 | 0.0012 | 0.0060 | 0.0242 | +0.7810 |  |
| T2b | exploratory | chain | 20 | r2 | E (raw) | F (std) | +0.0523 | [+0.0227, +0.0806] | 182.0 | 28.0 | 0.0027 | 0.0108 | 0.0515 | +0.7333 |  |
| T2b | exploratory | chain | 20 | r2 | PQK-1 | E (raw) | -0.1197 | [-0.1537, -0.0864] | 4.0 | 206.0 | 1.3351e-05 | 9.3460e-05 | 3.7384e-04 | -0.9619 |  |
| T2b | exploratory | chain | 20 | r2 | PQK-1 | PQK-2nn | -0.1089 | [-0.1423, -0.0803] | 1.0 | 209.0 | 3.8147e-06 | 3.0518e-05 | 1.1826e-04 | -0.9905 |  |
| T2b | exploratory | chain | 20 | r2 | PQK-2nn | FQ | -0.0335 | [-0.0518, -0.0177] | 21.0 | 189.0 | 8.5068e-04 | 0.0051 | 0.0187 | -0.8000 |  |
| T2b | exploratory | chain | 40 | r2 | E (raw) | E (std) | +0.0322 | [+0.0206, +0.0441] | 203.0 | 7.0 | 3.6240e-05 | 1.4496e-04 | 8.6975e-04 | +0.9333 |  |
| T2b | exploratory | chain | 40 | r2 | E (raw) | F (std) | +0.0600 | [+0.0205, +0.1229] | 195.0 | 15.0 | 2.6131e-04 | 7.8392e-04 | 0.0060 | +0.8571 |  |
| T2b | exploratory | chain | 40 | r2 | PQK-1 | E (raw) | -0.0562 | [-0.0737, -0.0419] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T2b | exploratory | chain | 40 | r2 | PQK-2nn | FQ | -0.0261 | [-0.0392, -0.0155] | 1.0 | 209.0 | 3.8147e-06 | 2.6703e-05 | 1.1826e-04 | -0.9905 |  |
| T2b | exploratory | chain | 80 | r2 | E (raw) | E (std) | +0.0226 | [+0.0177, +0.0286] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | +1.0000 |  |
| T2b | exploratory | chain | 80 | r2 | E (raw) | E2 (raw) | -0.0021 | [-0.0039, -0.0004] | 44.0 | 166.0 | 0.0215 | 0.0321 | 0.3438 | -0.5810 |  |
| T2b | exploratory | chain | 80 | r2 | E (raw) | F (std) | +0.0269 | [+0.0219, +0.0337] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | +1.0000 |  |
| T2b | exploratory | chain | 80 | r2 | FQ | E (raw) | +0.0044 | [+0.0028, +0.0062] | 209.0 | 1.0 | 3.8147e-06 | 1.5259e-05 | 1.1826e-04 | +0.9905 |  |
| T2b | exploratory | chain | 80 | r2 | PQK-1 | E (raw) | -0.0616 | [-0.0732, -0.0511] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T2b | exploratory | chain | 80 | r2 | PQK-1 | PQK-2nn | -0.0641 | [-0.0762, -0.0530] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T2b | exploratory | chain | 80 | r2 | PQK-2nn | E (raw) | +0.0025 | [+0.0008, +0.0043] | 171.0 | 39.0 | 0.0121 | 0.0321 | 0.2053 | +0.6286 |  |
| T2b | exploratory | chain | 80 | r2 | PQK-2nn | FQ | -0.0019 | [-0.0033, -0.0007] | 38.0 | 172.0 | 0.0107 | 0.0321 | 0.1924 | -0.6381 | significant_but_tiny |
| T2b | exploratory | chain | 160 | r2 | E (raw) | E (std) | +0.0057 | [+0.0052, +0.0063] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | +1.0000 |  |
| T2b | exploratory | chain | 160 | r2 | E (raw) | F (std) | +0.0232 | [+0.0214, +0.0251] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | +1.0000 |  |
| T2b | exploratory | chain | 160 | r2 | PQK-1 | E (raw) | -0.0386 | [-0.0421, -0.0350] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 |  |
| T4a | confirmatory | 2x4 | 40 | accuracy | PQK-1 | PQK-2nn | -0.2218 | [-0.2450, -0.1975] | 0.0 | 210.0 | 8.8449e-05 | 7.0359e-04 | 0.0027 | -1.0000 |  |
| T4a | confirmatory | 2x4 | 80 | accuracy | PQK-1 | PQK-2nn | -0.1907 | [-0.2130, -0.1695] | 0.0 | 210.0 | 8.8324e-05 | 7.0160e-04 | 0.0027 | -1.0000 |  |
| T4a | confirmatory | 2x4 | 80 | accuracy | PQK-2nn | E (raw) | -0.0127 | [-0.0210, -0.0055] | 19.0 | 134.0 | 0.0062 | 0.0186 | 0.0805 | -0.7516 |  |
| T4a | confirmatory | 3x4 | 40 | accuracy | PQK-1 | PQK-2nn | -0.1470 | [-0.1740, -0.1245] | 0.0 | 210.0 | 8.6955e-05 | 6.9564e-04 | 0.0027 | -1.0000 |  |
| T4a | confirmatory | 3x4 | 80 | accuracy | PQK-1 | PQK-2nn | -0.0725 | [-0.0962, -0.0527] | 0.0 | 210.0 | 8.7699e-05 | 6.9762e-04 | 0.0027 | -1.0000 |  |
| T4a | exploratory | 2x4 | 10 | accuracy | E (raw) | E2 (raw) | +0.0472 | [+0.0182, +0.0797] | 108.0 | 12.0 | 0.0064 | 0.0256 | 0.0805 | +0.8000 |  |
| T4a | exploratory | 2x4 | 10 | accuracy | FQ | E (raw) | +0.0450 | [+0.0198, +0.0720] | 110.0 | 10.0 | 0.0045 | 0.0224 | 0.0672 | +0.8333 |  |
| T4a | exploratory | 2x4 | 10 | accuracy | PQK-1 | E (raw) | -0.1392 | [-0.2027, -0.0800] | 4.0 | 132.0 | 9.3509e-04 | 0.0065 | 0.0178 | -0.9412 |  |
| T4a | exploratory | 2x4 | 10 | accuracy | PQK-1 | PQK-2nn | -0.0950 | [-0.1527, -0.0442] | 11.0 | 125.0 | 0.0032 | 0.0192 | 0.0513 | -0.8382 |  |
| T4a | exploratory | 2x4 | 10 | accuracy | PQK-2nn | E (raw) | -0.0442 | [-0.0762, -0.0165] | 18.0 | 118.0 | 0.0097 | 0.0291 | 0.1067 | -0.7353 |  |
| T4a | exploratory | 2x4 | 10 | accuracy | PQK-2nn | FQ | -0.0892 | [-0.1260, -0.0557] | 0.0 | 120.0 | 6.5331e-04 | 0.0052 | 0.0131 | -1.0000 |  |
| T4a | exploratory | 2x4 | 20 | accuracy | E (raw) | E (std) | +0.1660 | [+0.1242, +0.2105] | 210.0 | 0.0 | 8.8324e-05 | 6.1390e-04 | 0.0027 | +1.0000 |  |
| T4a | exploratory | 2x4 | 20 | accuracy | E (raw) | F (std) | +0.1645 | [+0.1255, +0.2025] | 209.0 | 1.0 | 1.0306e-04 | 6.1390e-04 | 0.0027 | +0.9905 |  |
| T4a | exploratory | 2x4 | 20 | accuracy | PQK-1 | E (raw) | -0.2812 | [-0.3302, -0.2325] | 0.0 | 210.0 | 8.7699e-05 | 6.1390e-04 | 0.0027 | -1.0000 |  |
| T4a | exploratory | 2x4 | 20 | accuracy | PQK-1 | PQK-2nn | -0.2370 | [-0.2960, -0.1805] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 6.1035e-05 | -1.0000 |  |
| T4a | exploratory | 2x4 | 20 | accuracy | PQK-2nn | FQ | -0.0658 | [-0.0995, -0.0340] | 16.5 | 193.5 | 9.4847e-04 | 0.0038 | 0.0178 | -0.8429 |  |
| T4a | exploratory | 2x4 | 40 | accuracy | E (raw) | E (std) | +0.0810 | [+0.0652, +0.0987] | 210.0 | 0.0 | 8.7949e-05 | 7.0359e-04 | 0.0027 | +1.0000 |  |
| T4a | exploratory | 2x4 | 40 | accuracy | E (raw) | F (std) | +0.0460 | [+0.0310, +0.0628] | 206.0 | 4.0 | 1.6136e-04 | 8.0680e-04 | 0.0035 | +0.9619 |  |
| T4a | exploratory | 2x4 | 40 | accuracy | PQK-1 | E (raw) | -0.2410 | [-0.2612, -0.2190] | 0.0 | 210.0 | 8.8324e-05 | 7.0359e-04 | 0.0027 | -1.0000 |  |
| T4a | exploratory | 2x4 | 40 | accuracy | PQK-2nn | FQ | -0.0245 | [-0.0380, -0.0110] | 29.0 | 181.0 | 0.0045 | 0.0181 | 0.0672 | -0.7238 |  |
| T4a | exploratory | 2x4 | 80 | accuracy | E (raw) | E (std) | +0.0502 | [+0.0367, +0.0660] | 210.0 | 0.0 | 8.7699e-05 | 7.0160e-04 | 0.0027 | +1.0000 |  |
| T4a | exploratory | 2x4 | 80 | accuracy | E (raw) | E2 (raw) | +0.0127 | [+0.0065, +0.0198] | 128.5 | 7.5 | 0.0016 | 0.0065 | 0.0276 | +0.8897 |  |
| T4a | exploratory | 2x4 | 80 | accuracy | E (raw) | F (std) | +0.0182 | [+0.0107, +0.0272] | 200.0 | 10.0 | 3.7356e-04 | 0.0019 | 0.0078 | +0.9048 |  |
| T4a | exploratory | 2x4 | 80 | accuracy | PQK-1 | E (raw) | -0.2035 | [-0.2240, -0.1837] | 0.0 | 210.0 | 8.8199e-05 | 7.0160e-04 | 0.0027 | -1.0000 |  |
| T4a | exploratory | 2x4 | 80 | accuracy | PQK-2nn | FQ | -0.0135 | [-0.0225, -0.0045] | 34.0 | 156.0 | 0.0139 | 0.0278 | 0.1392 | -0.6421 |  |
| T4a | exploratory | 3x4 | 10 | accuracy | E (raw) | E (std) | +0.0925 | [+0.0407, +0.1515] | 140.5 | 12.5 | 0.0024 | 0.0147 | 0.0440 | +0.8366 |  |
| T4a | exploratory | 3x4 | 10 | accuracy | PQK-1 | E (raw) | -0.2280 | [-0.2908, -0.1672] | 0.0 | 171.0 | 1.9609e-04 | 0.0016 | 0.0045 | -1.0000 |  |
| T4a | exploratory | 3x4 | 10 | accuracy | PQK-1 | PQK-2nn | -0.1837 | [-0.2448, -0.1270] | 0.0 | 171.0 | 1.9644e-04 | 0.0016 | 0.0045 | -1.0000 |  |
| T4a | exploratory | 3x4 | 10 | accuracy | PQK-2nn | FQ | -0.0780 | [-0.1340, -0.0272] | 24.0 | 147.0 | 0.0074 | 0.0369 | 0.1255 | -0.7193 |  |
| T4a | exploratory | 3x4 | 20 | accuracy | E (raw) | E (std) | +0.1255 | [+0.0702, +0.1850] | 201.5 | 8.5 | 3.1429e-04 | 0.0016 | 0.0066 | +0.9190 |  |
| T4a | exploratory | 3x4 | 20 | accuracy | E (raw) | F (std) | +0.1380 | [+0.0842, +0.1920] | 197.0 | 13.0 | 1.6785e-04 | 0.0010 | 0.0042 | +0.8762 |  |
| T4a | exploratory | 3x4 | 20 | accuracy | PQK-1 | E (raw) | -0.2460 | [-0.2990, -0.1947] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 6.1035e-05 | -1.0000 |  |
| T4a | exploratory | 3x4 | 20 | accuracy | PQK-1 | PQK-2nn | -0.2277 | [-0.2727, -0.1815] | 0.0 | 210.0 | 8.8449e-05 | 6.1914e-04 | 0.0027 | -1.0000 |  |
| T4a | exploratory | 3x4 | 40 | accuracy | E (raw) | E (std) | +0.0818 | [+0.0650, +0.0985] | 210.0 | 0.0 | 8.8324e-05 | 6.9564e-04 | 0.0027 | +1.0000 |  |
| T4a | exploratory | 3x4 | 40 | accuracy | E (raw) | F (std) | +0.0700 | [+0.0422, +0.0977] | 195.5 | 14.5 | 7.2310e-04 | 0.0036 | 0.0145 | +0.8619 |  |
| T4a | exploratory | 3x4 | 40 | accuracy | PQK-1 | E (raw) | -0.1540 | [-0.1898, -0.1135] | 5.0 | 205.0 | 1.8804e-04 | 0.0011 | 0.0045 | -0.9524 |  |
| T4a | exploratory | 3x4 | 80 | accuracy | E (raw) | E (std) | +0.0487 | [+0.0375, +0.0605] | 190.0 | 0.0 | 1.3121e-04 | 7.8728e-04 | 0.0034 | +1.0000 |  |
| T4a | exploratory | 3x4 | 80 | accuracy | E (raw) | F (std) | +0.0265 | [+0.0167, +0.0365] | 194.5 | 15.5 | 8.1831e-04 | 0.0041 | 0.0155 | +0.8524 |  |
| T4a | exploratory | 3x4 | 80 | accuracy | PQK-1 | E (raw) | -0.0792 | [-0.1040, -0.0600] | 0.0 | 210.0 | 8.7202e-05 | 6.9762e-04 | 0.0027 | -1.0000 |  |
| T4b | confirmatory | 2x4 | 40 | r2 | FQ | E (raw) | -0.0320 | [-0.0622, -0.0053] | 29.0 | 181.0 | 0.0032 | 0.0126 | 0.0599 | -0.7238 |  |
| T4b | confirmatory | 2x4 | 40 | r2 | PQK-1 | PQK-2nn | -0.0775 | [-0.1634, -0.0274] | 7.0 | 203.0 | 3.6240e-05 | 2.1744e-04 | 7.9727e-04 | -0.9333 |  |
| T4b | confirmatory | 2x4 | 80 | r2 | FQ | E (raw) | -0.0119 | [-0.0161, -0.0082] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 6.1035e-05 | -1.0000 |  |
| T4b | confirmatory | 2x4 | 80 | r2 | PQK-1 | PQK-2nn | -0.0461 | [-0.0543, -0.0377] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 6.1035e-05 | -1.0000 |  |
| T4b | confirmatory | 3x4 | 40 | r2 | PQK-1 | PQK-2nn | -0.0233 | [-0.0409, -0.0089] | 18.0 | 172.0 | 9.6512e-04 | 0.0048 | 0.0222 | -0.8105 |  |
| T4b | confirmatory | 3x4 | 80 | r2 | PQK-1 | PQK-2nn | -0.0107 | [-0.0148, -0.0072] | 0.0 | 190.0 | 3.8147e-06 | 3.0518e-05 | 1.2207e-04 | -1.0000 |  |
| T4b | exploratory | 2x4 | 10 | r2 | E (raw) | E (std) | +0.1999 | [+0.0707, +0.3312] | 176.0 | 34.0 | 0.0064 | 0.0447 | 0.1150 | +0.6762 |  |
| T4b | exploratory | 2x4 | 10 | r2 | E (raw) | F (std) | +0.4801 | [+0.3312, +0.6476] | 209.0 | 1.0 | 3.8147e-06 | 3.0518e-05 | 9.1553e-05 | +0.9905 |  |
| T4b | exploratory | 2x4 | 20 | r2 | E (raw) | E (std) | +0.0906 | [+0.0528, +0.1344] | 202.0 | 8.0 | 4.7684e-05 | 3.3379e-04 | 0.0010 | +0.9238 |  |
| T4b | exploratory | 2x4 | 20 | r2 | E (raw) | F (std) | +0.2358 | [+0.1647, +0.3442] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 6.1035e-05 | +1.0000 |  |
| T4b | exploratory | 2x4 | 40 | r2 | E (raw) | E (std) | +0.0717 | [+0.0544, +0.0902] | 209.0 | 1.0 | 3.8147e-06 | 2.6703e-05 | 9.1553e-05 | +0.9905 |  |
| T4b | exploratory | 2x4 | 40 | r2 | E (raw) | F (std) | +0.0614 | [+0.0325, +0.1046] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 6.1035e-05 | +1.0000 |  |
| T4b | exploratory | 2x4 | 40 | r2 | PQK-1 | E (raw) | -0.0851 | [-0.1777, -0.0292] | 15.0 | 195.0 | 2.6131e-04 | 0.0013 | 0.0052 | -0.8571 |  |
| T4b | exploratory | 2x4 | 80 | r2 | E (raw) | E (std) | +0.0387 | [+0.0270, +0.0516] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 6.1035e-05 | +1.0000 |  |
| T4b | exploratory | 2x4 | 80 | r2 | E (raw) | F (std) | +0.0325 | [+0.0200, +0.0488] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 6.1035e-05 | +1.0000 |  |
| T4b | exploratory | 2x4 | 80 | r2 | PQK-1 | E (raw) | -0.0478 | [-0.0567, -0.0389] | 0.0 | 210.0 | 1.9073e-06 | 1.5259e-05 | 6.1035e-05 | -1.0000 |  |
| T4b | exploratory | 2x4 | 80 | r2 | PQK-2nn | FQ | +0.0102 | [+0.0069, +0.0139] | 210.0 | 0.0 | 1.9073e-06 | 1.5259e-05 | 6.1035e-05 | +1.0000 |  |
| T4b | exploratory | 3x4 | 10 | r2 | E (raw) | E (std) | +0.1273 | [-0.0472, +0.2640] | 179.0 | 31.0 | 0.0042 | 0.0256 | 0.0802 | +0.7048 |  |
| T4b | exploratory | 3x4 | 10 | r2 | E (raw) | F (std) | +1.1277 | [+0.3833, +2.3157] | 194.0 | 16.0 | 3.2234e-04 | 0.0026 | 0.0077 | +0.8476 |  |
| T4b | exploratory | 3x4 | 10 | r2 | PQK-2nn | FQ | -0.0822 | [-0.1703, +0.0012] | 30.0 | 180.0 | 0.0037 | 0.0256 | 0.0731 | -0.7143 |  |
| T4b | exploratory | 3x4 | 20 | r2 | E (raw) | E (std) | +0.0680 | [-0.0389, +0.1800] | 172.0 | 18.0 | 9.6512e-04 | 0.0068 | 0.0222 | +0.8105 |  |
| T4b | exploratory | 3x4 | 20 | r2 | E (raw) | F (std) | +0.4961 | [+0.4063, +0.6112] | 190.0 | 0.0 | 3.8147e-06 | 3.0518e-05 | 1.2207e-04 | +1.0000 |  |
| T4b | exploratory | 3x4 | 20 | r2 | PQK-1 | PQK-2nn | -0.2264 | [-0.6304, -0.0165] | 23.0 | 167.0 | 0.0024 | 0.0144 | 0.0504 | -0.7579 |  |
| T4b | exploratory | 3x4 | 40 | r2 | E (raw) | E (std) | +0.0239 | [+0.0186, +0.0304] | 190.0 | 0.0 | 3.8147e-06 | 3.0518e-05 | 1.2207e-04 | +1.0000 |  |
| T4b | exploratory | 3x4 | 40 | r2 | E (raw) | F (std) | +0.0609 | [+0.0138, +0.1260] | 190.0 | 0.0 | 3.8147e-06 | 3.0518e-05 | 1.2207e-04 | +1.0000 |  |
| T4b | exploratory | 3x4 | 40 | r2 | PQK-1 | E (raw) | -0.0288 | [-0.0445, -0.0181] | 0.0 | 190.0 | 3.8147e-06 | 3.0518e-05 | 1.2207e-04 | -1.0000 |  |
| T4b | exploratory | 3x4 | 80 | r2 | E (raw) | E (std) | +0.0060 | [+0.0045, +0.0078] | 190.0 | 0.0 | 3.8147e-06 | 3.0518e-05 | 1.2207e-04 | +1.0000 |  |
| T4b | exploratory | 3x4 | 80 | r2 | E (raw) | F (std) | +0.0324 | [+0.0039, +0.0716] | 190.0 | 0.0 | 3.8147e-06 | 3.0518e-05 | 1.2207e-04 | +1.0000 |  |
| T4b | exploratory | 3x4 | 80 | r2 | PQK-1 | E (raw) | -0.0106 | [-0.0149, -0.0069] | 0.0 | 190.0 | 3.8147e-06 | 3.0518e-05 | 1.2207e-04 | -1.0000 |  |

## 3. Special Case Flags: significant_but_tiny and identical

### 3.1 Rows with flag == 'significant_but_tiny' (Count = 9)

| Task | Tier | Lattice | N | Metric | Model A | Model B | Mean Diff | 95% Bootstrap CI | p_raw | p_holm_perN | p_holm_family | Rank-Biserial r | Flag |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | exploratory | chain | 80 | r2 | FQ | E (raw) | -0.0019 | [-0.0027, -0.0012] | 8.2016e-05 | 8.2016e-05 | 1.0662e-03 | -0.9048 | significant_but_tiny |
| T1 | confirmatory | chain | 160 | r2 | FQ | E (raw) | -0.0012 | [-0.0015, -0.0009] | 5.7220e-06 | 1.5259e-05 | 1.0300e-04 | -0.9810 | significant_but_tiny |
| T2a | exploratory | chain | 80 | r2 | E (raw) | F (std) | -0.0003 | [-0.0004, -0.0002] | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 | significant_but_tiny |
| T2a | exploratory | chain | 80 | r2 | E (raw) | E (std) | -0.0001 | [-0.0002, -0.0000] | 2.6642e-02 | 5.3284e-02 | 2.6346e-01 | -0.5619 | significant_but_tiny |
| T2a | exploratory | chain | 160 | r2 | FQ | E (raw) | -0.0014 | [-0.0016, -0.0012] | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 | significant_but_tiny |
| T2a | exploratory | chain | 160 | r2 | E (raw) | F (std) | -0.0000 | [-0.0000, -0.0000] | 1.9073e-06 | 1.5259e-05 | 7.6294e-05 | -1.0000 | significant_but_tiny |
| T2a | exploratory | chain | 160 | r2 | E (raw) | E (std) | -0.0000 | [-0.0000, -0.0000] | 3.2234e-04 | 3.2234e-04 | 4.8351e-03 | -0.8476 | significant_but_tiny |
| T2b | exploratory | chain | 80 | r2 | PQK-2nn | FQ | -0.0019 | [-0.0033, -0.0007] | 1.0689e-02 | 3.2066e-02 | 1.9240e-01 | -0.6381 | significant_but_tiny |
| T4b | confirmatory | 2x4 | 80 | r2 | PQK-2nn | E (raw) | -0.0017 | [-0.0030, -0.0005] | 4.8441e-02 | 9.6882e-02 | 5.8129e-01 | -0.5048 | significant_but_tiny |

### 3.2 Rows with flag == 'identical' (Count = 0)

No rows were identical across all seeds (0 rows excluded from Holm testing).

## 4. Hyperparameter Grid Boundary Audit: Arms with >50% Seeds at Edge

Audited from `results/grid_boundary_post_v3.csv` and `results/grid_boundary_post_v3_t2.csv`.

| Task | Target | Lattice | Model | Variant | N | n_seeds | Boundary Edge (> 50%) | Percentage (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | half_chain_entropy | none | PQK-2nn | none | 10 | 20 | eps_low_pct | 60.0% |
| T1 | half_chain_entropy | none | FQ | none | 10 | 20 | eps_low_pct | 60.0% |
| T1 | half_chain_entropy | none | E | raw | 10 | 20 | eps_low_pct | 65.0% |
| T1 | half_chain_entropy | none | E | std | 10 | 20 | c_low_pct | 60.0% |
| T1 | half_chain_entropy | none | E | std | 10 | 20 | eps_low_pct | 65.0% |
| T1 | half_chain_entropy | none | E2 | raw | 10 | 20 | eps_low_pct | 65.0% |
| T1 | half_chain_entropy | none | FQ | none | 20 | 20 | eps_low_pct | 75.0% |
| T1 | half_chain_entropy | none | E | raw | 20 | 20 | C_high_pct | 60.0% |
| T1 | half_chain_entropy | none | E | raw | 20 | 20 | eps_low_pct | 60.0% |
| T1 | half_chain_entropy | none | E | std | 20 | 20 | eps_low_pct | 55.0% |
| T1 | half_chain_entropy | none | FQ | none | 40 | 20 | eps_low_pct | 60.0% |
| T1 | half_chain_entropy | none | PQK-1 (== RBF on <X>) | none | 80 | 20 | eps_high_pct | 60.0% |
| T1 | half_chain_entropy | none | E_X | raw | 80 | 20 | eps_high_pct | 60.0% |
| T4b | half_cut_entropy | 2x4 | PQK-1 (== RBF on <X>) | none | 10 | 20 | C_high_pct | 55.0% |
| T4b | half_cut_entropy | 2x4 | E | std | 10 | 20 | eps_low_pct | 60.0% |
| T4b | half_cut_entropy | 2x4 | E_X | raw | 10 | 20 | C_high_pct | 55.0% |
| T4b | half_cut_entropy | 2x4 | PQK-2nn | none | 20 | 20 | C_high_pct | 65.0% |
| T4b | half_cut_entropy | 2x4 | E | std | 20 | 20 | eps_low_pct | 65.0% |
| T4b | half_cut_entropy | 2x4 | E2 | raw | 20 | 20 | C_high_pct | 60.0% |
| T4b | half_cut_entropy | 2x4 | FQ | none | 80 | 20 | C_high_pct | 65.0% |
| T4b | half_cut_entropy | 2x4 | E | raw | 80 | 20 | C_high_pct | 60.0% |
| T4b | half_cut_entropy | 3x4 | E | std | 10 | 20 | eps_low_pct | 55.0% |
| T4b | half_cut_entropy | 3x4 | F | std | 10 | 20 | alpha_high_pct | 65.0% |
| T4b | half_cut_entropy | 3x4 | PQK-2nn | none | 20 | 20 | C_high_pct | 55.0% |
| T4b | half_cut_entropy | 3x4 | E | raw | 20 | 20 | C_high_pct | 55.0% |
| T4b | half_cut_entropy | 3x4 | F | std | 20 | 20 | alpha_high_pct | 60.0% |
| T4b | half_cut_entropy | 3x4 | PQK-2nn | none | 40 | 20 | C_high_pct | 65.0% |
| T4b | half_cut_entropy | 3x4 | PQK-2nn | none | 40 | 20 | eps_low_pct | 55.0% |
| T4b | half_cut_entropy | 3x4 | E | raw | 40 | 20 | C_high_pct | 85.0% |
| T4b | half_cut_entropy | 3x4 | E2 | raw | 40 | 20 | C_high_pct | 65.0% |
| T4b | half_cut_entropy | 3x4 | E2 | raw | 40 | 20 | eps_low_pct | 65.0% |
| T4b | half_cut_entropy | 3x4 | PQK-2nn | none | 80 | 20 | C_high_pct | 95.0% |
| T4b | half_cut_entropy | 3x4 | PQK-2nn | none | 80 | 20 | eps_low_pct | 60.0% |
| T4b | half_cut_entropy | 3x4 | E | raw | 80 | 20 | C_high_pct | 60.0% |
| T4b | half_cut_entropy | 3x4 | E | raw | 80 | 20 | eps_low_pct | 65.0% |
| T4b | half_cut_entropy | 3x4 | E | std | 80 | 20 | C_high_pct | 75.0% |
| T4b | half_cut_entropy | 3x4 | E | std | 80 | 20 | eps_low_pct | 65.0% |
| T4b | half_cut_entropy | 3x4 | E2 | raw | 80 | 20 | C_high_pct | 75.0% |
| T4b | half_cut_entropy | 3x4 | E2 | raw | 80 | 20 | eps_low_pct | 60.0% |
| T2a | z0_zn | chain | E | raw | 10 | 20 | eps_low_pct | 70.0% |
| T2a | z0_zn | chain | E | std | 10 | 20 | eps_low_pct | 80.0% |
| T2a | z0_zn | chain | E2 | raw | 10 | 20 | eps_low_pct | 55.0% |
| T2a | z0_zn | chain | PQK-2nn | none | 10 | 20 | eps_low_pct | 55.0% |
| T2a | z0_zn | chain | E | std | 20 | 20 | eps_low_pct | 55.0% |
| T2a | z0_zn | chain | FQ | none | 20 | 20 | eps_low_pct | 75.0% |
| T2a | z0_zn | chain | E | raw | 40 | 20 | C_high_pct | 100.0% |
| T2a | z0_zn | chain | E | raw | 40 | 20 | eps_low_pct | 70.0% |
| T2a | z0_zn | chain | E | std | 40 | 20 | C_high_pct | 90.0% |
| T2a | z0_zn | chain | E | std | 40 | 20 | eps_low_pct | 70.0% |
| T2a | z0_zn | chain | FQ | none | 40 | 20 | eps_low_pct | 90.0% |
| T2a | z0_zn | chain | E | raw | 80 | 20 | C_high_pct | 100.0% |
| T2a | z0_zn | chain | E | raw | 80 | 20 | eps_low_pct | 100.0% |
| T2a | z0_zn | chain | E | std | 80 | 20 | C_high_pct | 100.0% |
| T2a | z0_zn | chain | E | std | 80 | 20 | c_low_pct | 65.0% |
| T2a | z0_zn | chain | E | std | 80 | 20 | eps_low_pct | 95.0% |
| T2a | z0_zn | chain | F | std | 80 | 20 | alpha_low_pct | 100.0% |
| T2a | z0_zn | chain | FQ | none | 80 | 20 | eps_low_pct | 90.0% |
| T2a | z0_zn | chain | E | raw | 160 | 20 | C_high_pct | 100.0% |
| T2a | z0_zn | chain | E | raw | 160 | 20 | eps_low_pct | 100.0% |
| T2a | z0_zn | chain | E | std | 160 | 20 | C_high_pct | 100.0% |
| T2a | z0_zn | chain | E | std | 160 | 20 | c_low_pct | 100.0% |
| T2a | z0_zn | chain | E | std | 160 | 20 | eps_low_pct | 100.0% |
| T2a | z0_zn | chain | E2 | raw | 160 | 20 | C_high_pct | 60.0% |
| T2a | z0_zn | chain | F | std | 160 | 20 | alpha_low_pct | 100.0% |
| T2a | z0_zn | chain | FQ | none | 160 | 20 | eps_low_pct | 95.0% |
| T2a | z0_zn | chain | PQK-2nn | none | 160 | 20 | C_high_pct | 55.0% |
| T2b | z0_z1_zn2_zn1 | chain | E | std | 10 | 20 | eps_low_pct | 60.0% |
| T2b | z0_z1_zn2_zn1 | chain | E2 | raw | 10 | 20 | eps_low_pct | 55.0% |
| T2b | z0_z1_zn2_zn1 | chain | FQ | none | 10 | 20 | eps_low_pct | 55.0% |
| T2b | z0_z1_zn2_zn1 | chain | E | std | 20 | 20 | c_low_pct | 55.0% |
| T2b | z0_z1_zn2_zn1 | chain | E | raw | 40 | 20 | C_high_pct | 55.0% |
| T2b | z0_z1_zn2_zn1 | chain | E2 | raw | 40 | 20 | eps_low_pct | 55.0% |
| T2b | z0_z1_zn2_zn1 | chain | E_X | raw | 40 | 20 | eps_high_pct | 55.0% |
| T2b | z0_z1_zn2_zn1 | chain | FQ | none | 40 | 20 | eps_low_pct | 70.0% |
| T2b | z0_z1_zn2_zn1 | chain | PQK-1 (== RBF on <X>) | none | 40 | 20 | eps_high_pct | 55.0% |
| T2b | z0_z1_zn2_zn1 | chain | PQK-2nn | none | 40 | 20 | eps_low_pct | 65.0% |
| T2b | z0_z1_zn2_zn1 | chain | E | raw | 80 | 20 | C_high_pct | 60.0% |
| T2b | z0_z1_zn2_zn1 | chain | E | raw | 80 | 20 | eps_low_pct | 55.0% |
| T2b | z0_z1_zn2_zn1 | chain | E | std | 80 | 20 | C_high_pct | 65.0% |
| T2b | z0_z1_zn2_zn1 | chain | E2 | raw | 80 | 20 | C_high_pct | 75.0% |
| T2b | z0_z1_zn2_zn1 | chain | E2 | raw | 80 | 20 | eps_low_pct | 75.0% |
| T2b | z0_z1_zn2_zn1 | chain | E_X | raw | 80 | 20 | C_high_pct | 70.0% |
| T2b | z0_z1_zn2_zn1 | chain | FQ | none | 80 | 20 | eps_low_pct | 95.0% |
| T2b | z0_z1_zn2_zn1 | chain | PQK-1 (== RBF on <X>) | none | 80 | 20 | C_high_pct | 70.0% |
| T2b | z0_z1_zn2_zn1 | chain | PQK-2nn | none | 80 | 20 | C_high_pct | 70.0% |
| T2b | z0_z1_zn2_zn1 | chain | PQK-2nn | none | 80 | 20 | eps_low_pct | 75.0% |
| T2b | z0_z1_zn2_zn1 | chain | E | raw | 160 | 20 | C_high_pct | 95.0% |
| T2b | z0_z1_zn2_zn1 | chain | E | raw | 160 | 20 | eps_low_pct | 95.0% |
| T2b | z0_z1_zn2_zn1 | chain | E | std | 160 | 20 | C_high_pct | 55.0% |
| T2b | z0_z1_zn2_zn1 | chain | E | std | 160 | 20 | eps_low_pct | 75.0% |
| T2b | z0_z1_zn2_zn1 | chain | E2 | raw | 160 | 20 | C_high_pct | 95.0% |
| T2b | z0_z1_zn2_zn1 | chain | E2 | raw | 160 | 20 | eps_low_pct | 80.0% |
| T2b | z0_z1_zn2_zn1 | chain | FQ | none | 160 | 20 | eps_low_pct | 85.0% |
| T2b | z0_z1_zn2_zn1 | chain | PQK-2nn | none | 160 | 20 | C_high_pct | 95.0% |
| T2b | z0_z1_zn2_zn1 | chain | PQK-2nn | none | 160 | 20 | eps_low_pct | 85.0% |

## 5. Exact Plotted Values per Figure

### Figure 1: T1 Half-Chain Entropy Learning Curves
*Source Data:* `figures/data/fig_learning_curve_t1.csv`

| figure | panel | model | x_var | x_val | mean | ci_low | ci_high | n_seeds | source_file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F1 | main | baseline_mean | N_train | nan | -0.0532 | -0.0911 | -0.0269 | 100 | results/t1_entropy_gridv3.csv |
| F1 | main | PQK-1 (== RBF on <X>) | N_train | 10.0000 | 0.7477 | 0.7106 | 0.7819 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | PQK-1 (== RBF on <X>) | N_train | 20.0000 | 0.8565 | 0.8364 | 0.8755 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | PQK-1 (== RBF on <X>) | N_train | 40.0000 | 0.8986 | 0.8847 | 0.9111 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | PQK-1 (== RBF on <X>) | N_train | 80.0000 | 0.9306 | 0.9227 | 0.9376 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | PQK-1 (== RBF on <X>) | N_train | 160.0000 | 0.9529 | 0.9505 | 0.9553 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | PQK-2nn | N_train | 10.0000 | 0.8520 | 0.8013 | 0.8950 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | PQK-2nn | N_train | 20.0000 | 0.9555 | 0.9447 | 0.9640 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | PQK-2nn | N_train | 40.0000 | 0.9789 | 0.9731 | 0.9833 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | PQK-2nn | N_train | 80.0000 | 0.9895 | 0.9883 | 0.9905 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | PQK-2nn | N_train | 160.0000 | 0.9943 | 0.9936 | 0.9950 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | FQ | N_train | 10.0000 | 0.8916 | 0.8584 | 0.9207 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | FQ | N_train | 20.0000 | 0.9795 | 0.9757 | 0.9826 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | FQ | N_train | 40.0000 | 0.9902 | 0.9889 | 0.9915 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | FQ | N_train | 80.0000 | 0.9941 | 0.9933 | 0.9949 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | FQ | N_train | 160.0000 | 0.9975 | 0.9972 | 0.9978 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | E (raw) | N_train | 10.0000 | 0.8305 | 0.7653 | 0.8837 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | E (raw) | N_train | 20.0000 | 0.9754 | 0.9722 | 0.9785 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | E (raw) | N_train | 40.0000 | 0.9872 | 0.9847 | 0.9893 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | E (raw) | N_train | 80.0000 | 0.9961 | 0.9955 | 0.9966 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | E (raw) | N_train | 160.0000 | 0.9987 | 0.9986 | 0.9989 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | E2 (raw) | N_train | 10.0000 | 0.8661 | 0.8313 | 0.8981 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | E2 (raw) | N_train | 20.0000 | 0.9560 | 0.9460 | 0.9641 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | E2 (raw) | N_train | 40.0000 | 0.9786 | 0.9727 | 0.9833 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | E2 (raw) | N_train | 80.0000 | 0.9895 | 0.9881 | 0.9906 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | E2 (raw) | N_train | 160.0000 | 0.9942 | 0.9935 | 0.9950 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | F (std) | N_train | 10.0000 | 0.8192 | 0.7862 | 0.8498 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | F (std) | N_train | 20.0000 | 0.9284 | 0.9156 | 0.9395 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | F (std) | N_train | 40.0000 | 0.9728 | 0.9663 | 0.9776 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | F (std) | N_train | 80.0000 | 0.9846 | 0.9833 | 0.9860 | 20 | results/t1_entropy_gridv3.csv |
| F1 | main | F (std) | N_train | 160.0000 | 0.9887 | 0.9878 | 0.9894 | 20 | results/t1_entropy_gridv3.csv |

### Figure 2: T2 Contained vs. Not-Contained Correlators
*Source Data:* `figures/data/fig_t2_contained_vs_not.csv`

| figure | panel | model | x_var | x_val | mean | ci_low | ci_high | n_seeds | source_file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F2 | T2a | baseline_mean | N_train | nan | -0.0564 | -0.0903 | -0.0312 | 100 | results/t2_correlators_gridv3.csv |
| F2 | T2a | PQK-1 (== RBF on <X>) | N_train | 10.0000 | 0.3466 | 0.2184 | 0.4493 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | PQK-1 (== RBF on <X>) | N_train | 20.0000 | 0.6809 | 0.6128 | 0.7414 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | PQK-1 (== RBF on <X>) | N_train | 40.0000 | 0.8757 | 0.8552 | 0.8940 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | PQK-1 (== RBF on <X>) | N_train | 80.0000 | 0.9094 | 0.8908 | 0.9256 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | PQK-1 (== RBF on <X>) | N_train | 160.0000 | 0.9417 | 0.9339 | 0.9493 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | PQK-2nn | N_train | 10.0000 | 0.3411 | 0.2101 | 0.4499 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | PQK-2nn | N_train | 20.0000 | 0.6392 | 0.5695 | 0.7037 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | PQK-2nn | N_train | 40.0000 | 0.8666 | 0.8402 | 0.8889 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | PQK-2nn | N_train | 80.0000 | 0.9243 | 0.9077 | 0.9386 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | PQK-2nn | N_train | 160.0000 | 0.9646 | 0.9599 | 0.9693 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | FQ | N_train | 10.0000 | 0.4626 | 0.3088 | 0.5944 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | FQ | N_train | 20.0000 | 0.7899 | 0.7313 | 0.8394 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | FQ | N_train | 40.0000 | 0.9626 | 0.9523 | 0.9708 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | FQ | N_train | 80.0000 | 0.9921 | 0.9898 | 0.9939 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | FQ | N_train | 160.0000 | 0.9986 | 0.9984 | 0.9988 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | E (raw) | N_train | 10.0000 | 0.6078 | 0.4423 | 0.7344 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | E (raw) | N_train | 20.0000 | 0.8975 | 0.8656 | 0.9258 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | E (raw) | N_train | 40.0000 | 0.9916 | 0.9877 | 0.9945 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | E (raw) | N_train | 80.0000 | 0.9997 | 0.9996 | 0.9998 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | E (raw) | N_train | 160.0000 | 1.0000 | 1.0000 | 1.0000 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | E2 (raw) | N_train | 10.0000 | 0.3293 | 0.1989 | 0.4403 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | E2 (raw) | N_train | 20.0000 | 0.6442 | 0.5778 | 0.7016 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | E2 (raw) | N_train | 40.0000 | 0.8688 | 0.8426 | 0.8913 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | E2 (raw) | N_train | 80.0000 | 0.9250 | 0.9097 | 0.9383 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | E2 (raw) | N_train | 160.0000 | 0.9646 | 0.9600 | 0.9693 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | F (std) | N_train | 10.0000 | 0.7607 | 0.7085 | 0.8067 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | F (std) | N_train | 20.0000 | 0.9056 | 0.8861 | 0.9238 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | F (std) | N_train | 40.0000 | 0.9945 | 0.9905 | 0.9972 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | F (std) | N_train | 80.0000 | 1.0000 | 1.0000 | 1.0000 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2a | F (std) | N_train | 160.0000 | 1.0000 | 1.0000 | 1.0000 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | baseline_mean | N_train | nan | -0.0447 | -0.0606 | -0.0314 | 100 | results/t2_correlators_gridv3.csv |
| F2 | T2b | PQK-1 (== RBF on <X>) | N_train | 10.0000 | 0.3876 | 0.2252 | 0.5381 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | PQK-1 (== RBF on <X>) | N_train | 20.0000 | 0.7587 | 0.7270 | 0.7873 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | PQK-1 (== RBF on <X>) | N_train | 40.0000 | 0.8900 | 0.8698 | 0.9065 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | PQK-1 (== RBF on <X>) | N_train | 80.0000 | 0.9291 | 0.9169 | 0.9402 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | PQK-1 (== RBF on <X>) | N_train | 160.0000 | 0.9603 | 0.9568 | 0.9640 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | PQK-2nn | N_train | 10.0000 | 0.4161 | 0.2402 | 0.5780 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | PQK-2nn | N_train | 20.0000 | 0.8675 | 0.8502 | 0.8835 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | PQK-2nn | N_train | 40.0000 | 0.9443 | 0.9297 | 0.9570 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | PQK-2nn | N_train | 80.0000 | 0.9932 | 0.9917 | 0.9945 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | PQK-2nn | N_train | 160.0000 | 0.9988 | 0.9986 | 0.9990 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | FQ | N_train | 10.0000 | 0.6092 | 0.4364 | 0.7502 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | FQ | N_train | 20.0000 | 0.9010 | 0.8893 | 0.9115 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | FQ | N_train | 40.0000 | 0.9705 | 0.9636 | 0.9763 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | FQ | N_train | 80.0000 | 0.9951 | 0.9943 | 0.9958 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | FQ | N_train | 160.0000 | 0.9989 | 0.9987 | 0.9991 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | E (raw) | N_train | 10.0000 | 0.5195 | 0.3321 | 0.6842 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | E (raw) | N_train | 20.0000 | 0.8784 | 0.8560 | 0.8974 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | E (raw) | N_train | 40.0000 | 0.9462 | 0.9406 | 0.9517 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | E (raw) | N_train | 80.0000 | 0.9907 | 0.9887 | 0.9925 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | E (raw) | N_train | 160.0000 | 0.9989 | 0.9987 | 0.9991 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | E2 (raw) | N_train | 10.0000 | 0.4041 | 0.2254 | 0.5679 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | E2 (raw) | N_train | 20.0000 | 0.8708 | 0.8515 | 0.8877 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | E2 (raw) | N_train | 40.0000 | 0.9432 | 0.9289 | 0.9558 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | E2 (raw) | N_train | 80.0000 | 0.9928 | 0.9912 | 0.9943 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | E2 (raw) | N_train | 160.0000 | 0.9988 | 0.9985 | 0.9990 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | F (std) | N_train | 10.0000 | 0.5967 | 0.4978 | 0.6879 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | F (std) | N_train | 20.0000 | 0.8261 | 0.7977 | 0.8534 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | F (std) | N_train | 40.0000 | 0.8862 | 0.8237 | 0.9249 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | F (std) | N_train | 80.0000 | 0.9638 | 0.9570 | 0.9692 | 20 | results/t2_correlators_gridv3.csv |
| F2 | T2b | F (std) | N_train | 160.0000 | 0.9757 | 0.9738 | 0.9776 | 20 | results/t2_correlators_gridv3.csv |

### Figure 3: T4 2D Cluster State Classification & Entropy Across Lattices
*Source Data:* `figures/data/fig_t4_lattices.csv`

| figure | panel | model | x_var | x_val | mean | ci_low | ci_high | n_seeds | source_file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F3 | T4a_2x4 | baseline_majority | N_train | nan | 0.5288 | 0.5112 | 0.5458 | 80 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | PQK-1 (== RBF on <X>) | N_train | 10.0000 | 0.5840 | 0.5468 | 0.6222 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | PQK-1 (== RBF on <X>) | N_train | 20.0000 | 0.6285 | 0.5847 | 0.6697 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | PQK-1 (== RBF on <X>) | N_train | 40.0000 | 0.7268 | 0.7060 | 0.7492 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | PQK-1 (== RBF on <X>) | N_train | 80.0000 | 0.7782 | 0.7570 | 0.7993 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | PQK-2nn | N_train | 10.0000 | 0.6790 | 0.6290 | 0.7332 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | PQK-2nn | N_train | 20.0000 | 0.8655 | 0.8255 | 0.9027 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | PQK-2nn | N_train | 40.0000 | 0.9485 | 0.9340 | 0.9625 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | PQK-2nn | N_train | 80.0000 | 0.9690 | 0.9603 | 0.9770 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | FQ | N_train | 10.0000 | 0.7683 | 0.7027 | 0.8325 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | FQ | N_train | 20.0000 | 0.9313 | 0.9022 | 0.9537 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | FQ | N_train | 40.0000 | 0.9730 | 0.9652 | 0.9805 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | FQ | N_train | 80.0000 | 0.9825 | 0.9760 | 0.9888 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | E (raw) | N_train | 10.0000 | 0.7232 | 0.6660 | 0.7822 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | E (raw) | N_train | 20.0000 | 0.9097 | 0.8698 | 0.9450 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | E (raw) | N_train | 40.0000 | 0.9677 | 0.9593 | 0.9760 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | E (raw) | N_train | 80.0000 | 0.9818 | 0.9758 | 0.9875 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | E2 (raw) | N_train | 10.0000 | 0.6760 | 0.6285 | 0.7253 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | E2 (raw) | N_train | 20.0000 | 0.8847 | 0.8485 | 0.9180 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | E2 (raw) | N_train | 40.0000 | 0.9547 | 0.9410 | 0.9680 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | E2 (raw) | N_train | 80.0000 | 0.9690 | 0.9615 | 0.9762 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | F (std) | N_train | 10.0000 | 0.6940 | 0.6550 | 0.7345 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | F (std) | N_train | 20.0000 | 0.7453 | 0.6998 | 0.7865 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | F (std) | N_train | 40.0000 | 0.9217 | 0.9048 | 0.9370 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_2x4 | F (std) | N_train | 80.0000 | 0.9635 | 0.9553 | 0.9705 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4b_2x4 | baseline_mean | N_train | nan | -0.0444 | -0.0614 | -0.0304 | 80 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | PQK-1 (== RBF on <X>) | N_train | 10.0000 | 0.5559 | 0.1195 | 0.8285 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | PQK-1 (== RBF on <X>) | N_train | 20.0000 | 0.8122 | 0.6990 | 0.8985 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | PQK-1 (== RBF on <X>) | N_train | 40.0000 | 0.8961 | 0.8067 | 0.9482 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | PQK-1 (== RBF on <X>) | N_train | 80.0000 | 0.9472 | 0.9364 | 0.9578 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | PQK-2nn | N_train | 10.0000 | 0.6045 | 0.3484 | 0.8062 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | PQK-2nn | N_train | 20.0000 | 0.9194 | 0.8854 | 0.9464 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | PQK-2nn | N_train | 40.0000 | 0.9736 | 0.9635 | 0.9829 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | PQK-2nn | N_train | 80.0000 | 0.9934 | 0.9887 | 0.9969 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | FQ | N_train | 10.0000 | 0.6245 | 0.3857 | 0.8063 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | FQ | N_train | 20.0000 | 0.8814 | 0.8046 | 0.9397 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | FQ | N_train | 40.0000 | 0.9492 | 0.9213 | 0.9713 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | FQ | N_train | 80.0000 | 0.9832 | 0.9757 | 0.9889 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | E (raw) | N_train | 10.0000 | 0.8249 | 0.7428 | 0.8904 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | E (raw) | N_train | 20.0000 | 0.9403 | 0.9215 | 0.9578 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | E (raw) | N_train | 40.0000 | 0.9812 | 0.9657 | 0.9919 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | E (raw) | N_train | 80.0000 | 0.9951 | 0.9911 | 0.9979 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | E2 (raw) | N_train | 10.0000 | 0.7233 | 0.5368 | 0.8663 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | E2 (raw) | N_train | 20.0000 | 0.8933 | 0.8335 | 0.9401 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | E2 (raw) | N_train | 40.0000 | 0.9724 | 0.9552 | 0.9865 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | E2 (raw) | N_train | 80.0000 | 0.9917 | 0.9850 | 0.9965 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | F (std) | N_train | 10.0000 | 0.3448 | 0.1613 | 0.5015 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | F (std) | N_train | 20.0000 | 0.7044 | 0.5942 | 0.7764 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | F (std) | N_train | 40.0000 | 0.9198 | 0.8626 | 0.9556 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_2x4 | F (std) | N_train | 80.0000 | 0.9626 | 0.9429 | 0.9770 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4a_3x4 | baseline_majority | N_train | nan | 0.5309 | 0.5058 | 0.5551 | 80 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | PQK-1 (== RBF on <X>) | N_train | 10.0000 | 0.5520 | 0.4980 | 0.6020 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | PQK-1 (== RBF on <X>) | N_train | 20.0000 | 0.6587 | 0.6178 | 0.7025 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | PQK-1 (== RBF on <X>) | N_train | 40.0000 | 0.8043 | 0.7747 | 0.8313 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | PQK-1 (== RBF on <X>) | N_train | 80.0000 | 0.8970 | 0.8740 | 0.9160 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | PQK-2nn | N_train | 10.0000 | 0.7357 | 0.6665 | 0.8030 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | PQK-2nn | N_train | 20.0000 | 0.8865 | 0.8467 | 0.9230 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | PQK-2nn | N_train | 40.0000 | 0.9512 | 0.9322 | 0.9675 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | PQK-2nn | N_train | 80.0000 | 0.9695 | 0.9615 | 0.9770 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | FQ | N_train | 10.0000 | 0.8137 | 0.7312 | 0.8868 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | FQ | N_train | 20.0000 | 0.9127 | 0.8780 | 0.9437 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | FQ | N_train | 40.0000 | 0.9663 | 0.9510 | 0.9798 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | FQ | N_train | 80.0000 | 0.9767 | 0.9702 | 0.9828 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | E (raw) | N_train | 10.0000 | 0.7800 | 0.7052 | 0.8470 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | E (raw) | N_train | 20.0000 | 0.9048 | 0.8565 | 0.9462 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | E (raw) | N_train | 40.0000 | 0.9583 | 0.9340 | 0.9780 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | E (raw) | N_train | 80.0000 | 0.9762 | 0.9705 | 0.9820 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | E2 (raw) | N_train | 10.0000 | 0.7800 | 0.7173 | 0.8398 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | E2 (raw) | N_train | 20.0000 | 0.8967 | 0.8580 | 0.9302 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | E2 (raw) | N_train | 40.0000 | 0.9480 | 0.9247 | 0.9670 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | E2 (raw) | N_train | 80.0000 | 0.9700 | 0.9608 | 0.9780 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | F (std) | N_train | 10.0000 | 0.7488 | 0.7153 | 0.7840 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | F (std) | N_train | 20.0000 | 0.7668 | 0.7318 | 0.8015 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | F (std) | N_train | 40.0000 | 0.8882 | 0.8668 | 0.9083 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4a_3x4 | F (std) | N_train | 80.0000 | 0.9497 | 0.9423 | 0.9573 | 20 | results/t4_v2_gridv2.csv |
| F3 | T4b_3x4 | baseline_mean | N_train | nan | -0.0357 | -0.0487 | -0.0244 | 77 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | PQK-1 (== RBF on <X>) | N_train | 10.0000 | 0.6166 | 0.2106 | 0.8710 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | PQK-1 (== RBF on <X>) | N_train | 20.0000 | 0.7518 | 0.3476 | 0.9605 | 19 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | PQK-1 (== RBF on <X>) | N_train | 40.0000 | 0.9689 | 0.9535 | 0.9792 | 19 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | PQK-1 (== RBF on <X>) | N_train | 80.0000 | 0.9887 | 0.9844 | 0.9924 | 19 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | PQK-2nn | N_train | 10.0000 | 0.8633 | 0.7808 | 0.9319 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | PQK-2nn | N_train | 20.0000 | 0.9782 | 0.9664 | 0.9884 | 19 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | PQK-2nn | N_train | 40.0000 | 0.9922 | 0.9808 | 0.9985 | 19 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | PQK-2nn | N_train | 80.0000 | 0.9994 | 0.9988 | 0.9998 | 19 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | FQ | N_train | 10.0000 | 0.9455 | 0.9012 | 0.9736 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | FQ | N_train | 20.0000 | 0.9897 | 0.9840 | 0.9944 | 19 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | FQ | N_train | 40.0000 | 0.9975 | 0.9959 | 0.9988 | 19 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | FQ | N_train | 80.0000 | 0.9996 | 0.9995 | 0.9997 | 19 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | E (raw) | N_train | 10.0000 | 0.8423 | 0.6881 | 0.9378 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | E (raw) | N_train | 20.0000 | 0.9111 | 0.8064 | 0.9785 | 19 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | E (raw) | N_train | 40.0000 | 0.9976 | 0.9963 | 0.9987 | 19 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | E (raw) | N_train | 80.0000 | 0.9993 | 0.9989 | 0.9997 | 19 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | E2 (raw) | N_train | 10.0000 | 0.9054 | 0.8497 | 0.9467 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | E2 (raw) | N_train | 20.0000 | 0.9705 | 0.9534 | 0.9837 | 19 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | E2 (raw) | N_train | 40.0000 | 0.9961 | 0.9928 | 0.9984 | 19 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | E2 (raw) | N_train | 80.0000 | 0.9994 | 0.9987 | 0.9998 | 19 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | F (std) | N_train | 10.0000 | -0.2854 | -1.4600 | 0.4294 | 20 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | F (std) | N_train | 20.0000 | 0.4150 | 0.2592 | 0.5391 | 19 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | F (std) | N_train | 40.0000 | 0.9367 | 0.8713 | 0.9842 | 19 | results/t4_v2_gridv3.csv |
| F3 | T4b_3x4 | F (std) | N_train | 80.0000 | 0.9669 | 0.9275 | 0.9956 | 19 | results/t4_v2_gridv3.csv |

### Figure 4: T3 Concentration of Measure Scaling
*Source Data:* `figures/data/fig_concentration.csv`

| figure | panel | kernel | gamma_rule | label | n | mean_offdiag_mean | ci_low_mean | ci_high_mean | mean_offdiag_var | ci_low_var | ci_high_var | n_seeds | source_file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F4 | both | FQ | none | FQ | 4 | 0.9398 | 0.9344 | 0.9452 | 0.0032 | 0.0025 | 0.0040 | 20 | results/t3_concentration_v2.csv |
| F4 | both | FQ | none | FQ | 6 | 0.8922 | 0.8846 | 0.9001 | 0.0063 | 0.0051 | 0.0075 | 20 | results/t3_concentration_v2.csv |
| F4 | both | FQ | none | FQ | 8 | 0.8419 | 0.8348 | 0.8489 | 0.0086 | 0.0076 | 0.0096 | 20 | results/t3_concentration_v2.csv |
| F4 | both | FQ | none | FQ | 10 | 0.7931 | 0.7833 | 0.8031 | 0.0124 | 0.0107 | 0.0142 | 20 | results/t3_concentration_v2.csv |
| F4 | both | FQ | none | FQ | 12 | 0.7423 | 0.7303 | 0.7545 | 0.0152 | 0.0135 | 0.0170 | 20 | results/t3_concentration_v2.csv |
| F4 | both | FQ | none | FQ | 14 | 0.6969 | 0.6879 | 0.7065 | 0.0166 | 0.0150 | 0.0186 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-1 | 1.0 | PQK-1 ($\gamma=1$) | 4 | 0.9388 | 0.9319 | 0.9459 | 0.0054 | 0.0040 | 0.0069 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-1 | 1.0 | PQK-1 ($\gamma=1$) | 6 | 0.8925 | 0.8824 | 0.9030 | 0.0097 | 0.0078 | 0.0118 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-1 | 1.0 | PQK-1 ($\gamma=1$) | 8 | 0.8454 | 0.8374 | 0.8535 | 0.0122 | 0.0108 | 0.0135 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-1 | 1.0 | PQK-1 ($\gamma=1$) | 10 | 0.7982 | 0.7868 | 0.8094 | 0.0165 | 0.0142 | 0.0188 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-1 | 1.0 | PQK-1 ($\gamma=1$) | 12 | 0.7506 | 0.7366 | 0.7649 | 0.0191 | 0.0171 | 0.0211 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-1 | 1.0 | PQK-1 ($\gamma=1$) | 14 | 0.7093 | 0.6987 | 0.7205 | 0.0200 | 0.0181 | 0.0223 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-1 | 1.0/n | PQK-1 ($\gamma=1/n$) | 4 | 0.9837 | 0.9817 | 0.9857 | 0.0004 | 0.0003 | 0.0006 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-1 | 1.0/n | PQK-1 ($\gamma=1/n$) | 6 | 0.9802 | 0.9781 | 0.9823 | 0.0004 | 0.0003 | 0.0005 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-1 | 1.0/n | PQK-1 ($\gamma=1/n$) | 8 | 0.9782 | 0.9769 | 0.9794 | 0.0003 | 0.0003 | 0.0003 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-1 | 1.0/n | PQK-1 ($\gamma=1/n$) | 10 | 0.9764 | 0.9748 | 0.9779 | 0.0003 | 0.0003 | 0.0004 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-1 | 1.0/n | PQK-1 ($\gamma=1/n$) | 12 | 0.9749 | 0.9732 | 0.9765 | 0.0003 | 0.0002 | 0.0003 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-1 | 1.0/n | PQK-1 ($\gamma=1/n$) | 14 | 0.9742 | 0.9730 | 0.9755 | 0.0002 | 0.0002 | 0.0003 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-2nn | 1.0 | PQK-2nn ($\gamma=1$) | 4 | 0.8790 | 0.8686 | 0.8895 | 0.0129 | 0.0103 | 0.0157 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-2nn | 1.0 | PQK-2nn ($\gamma=1$) | 6 | 0.7876 | 0.7734 | 0.8028 | 0.0232 | 0.0197 | 0.0268 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-2nn | 1.0 | PQK-2nn ($\gamma=1$) | 8 | 0.7003 | 0.6880 | 0.7127 | 0.0287 | 0.0260 | 0.0314 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-2nn | 1.0 | PQK-2nn ($\gamma=1$) | 10 | 0.6214 | 0.6057 | 0.6374 | 0.0346 | 0.0307 | 0.0386 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-2nn | 1.0 | PQK-2nn ($\gamma=1$) | 12 | 0.5443 | 0.5265 | 0.5626 | 0.0368 | 0.0342 | 0.0396 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-2nn | 1.0 | PQK-2nn ($\gamma=1$) | 14 | 0.4816 | 0.4686 | 0.4952 | 0.0343 | 0.0319 | 0.0370 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-2nn | 1.0/n | PQK-2nn ($\gamma=1/n$) | 4 | 0.9664 | 0.9630 | 0.9696 | 0.0012 | 0.0009 | 0.0016 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-2nn | 1.0/n | PQK-2nn ($\gamma=1/n$) | 6 | 0.9576 | 0.9540 | 0.9612 | 0.0014 | 0.0011 | 0.0018 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-2nn | 1.0/n | PQK-2nn ($\gamma=1/n$) | 8 | 0.9525 | 0.9499 | 0.9550 | 0.0012 | 0.0010 | 0.0013 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-2nn | 1.0/n | PQK-2nn ($\gamma=1/n$) | 10 | 0.9484 | 0.9451 | 0.9515 | 0.0012 | 0.0010 | 0.0014 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-2nn | 1.0/n | PQK-2nn ($\gamma=1/n$) | 12 | 0.9444 | 0.9413 | 0.9476 | 0.0012 | 0.0010 | 0.0014 | 20 | results/t3_concentration_v2.csv |
| F4 | both | PQK-2nn | 1.0/n | PQK-2nn ($\gamma=1/n$) | 14 | 0.9429 | 0.9404 | 0.9453 | 0.0010 | 0.0009 | 0.0012 | 20 | results/t3_concentration_v2.csv |

### Figure 5: Total Measurement Shot Budget Scaling
*Source Data:* `figures/data/fig_shots.csv`

| figure | panel | model | variant | shots | x_cost | mean_r2 | ci_low | ci_high | n_seeds | source_file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F5 | deployed | PQK-1 | none | 100.0000 | 48000.0 | 0.7374 | 0.7205 | 0.7536 | 20 | results/t5_noise.csv |
| F5 | deployed | PQK-1 | none | 1000.0000 | 480000.0 | 0.8717 | 0.8606 | 0.8819 | 20 | results/t5_noise.csv |
| F5 | deployed | PQK-1 | none | 10000.0 | 4800000.0 | 0.9036 | 0.8939 | 0.9131 | 20 | results/t5_noise.csv |
| F5 | deployed | PQK-2nn | none | 100.0000 | 72000.0 | 0.8576 | 0.8460 | 0.8671 | 20 | results/t5_noise.csv |
| F5 | deployed | PQK-2nn | none | 1000.0000 | 720000.0 | 0.9574 | 0.9519 | 0.9627 | 20 | results/t5_noise.csv |
| F5 | deployed | PQK-2nn | none | 10000.0 | 7200000.0 | 0.9725 | 0.9659 | 0.9777 | 20 | results/t5_noise.csv |
| F5 | deployed | E | raw | 100.0000 | 72000.0 | 0.8237 | 0.8074 | 0.8390 | 20 | results/t5_noise.csv |
| F5 | deployed | E | raw | 1000.0000 | 720000.0 | 0.9571 | 0.9522 | 0.9616 | 20 | results/t5_noise.csv |
| F5 | deployed | E | raw | 10000.0 | 7200000.0 | 0.9815 | 0.9750 | 0.9861 | 20 | results/t5_noise.csv |
| F5 | deployed | E2 | raw | 100.0000 | 72000.0 | 0.8583 | 0.8470 | 0.8674 | 20 | results/t5_noise.csv |
| F5 | deployed | E2 | raw | 1000.0000 | 720000.0 | 0.9571 | 0.9521 | 0.9620 | 20 | results/t5_noise.csv |
| F5 | deployed | E2 | raw | 10000.0 | 7200000.0 | 0.9721 | 0.9652 | 0.9774 | 20 | results/t5_noise.csv |
| F5 | deployed | F | std | 100.0000 | 72000.0 | 0.8338 | 0.8218 | 0.8459 | 20 | results/t5_noise.csv |
| F5 | deployed | F | std | 1000.0000 | 720000.0 | 0.9405 | 0.9332 | 0.9474 | 20 | results/t5_noise.csv |
| F5 | deployed | F | std | 10000.0 | 7200000.0 | 0.9653 | 0.9556 | 0.9728 | 20 | results/t5_noise.csv |
| F5 | deployed | FQ-clipped | none | 100.0000 | 878000.0 | 0.8101 | 0.7920 | 0.8279 | 20 | results/t5_noise.csv |
| F5 | deployed | FQ-clipped | none | 1000.0000 | 8780000.0 | 0.8693 | 0.8247 | 0.9045 | 20 | results/t5_noise.csv |
| F5 | deployed | FQ-clipped | none | 10000.0 | 87800000.0 | 0.9630 | 0.9553 | 0.9686 | 20 | results/t5_noise.csv |
| F5 | deployed | FQ-raw | none | 100.0000 | 878000.0 | 0.7634 | 0.7433 | 0.7841 | 20 | results/t5_noise.csv |
| F5 | deployed | FQ-raw | none | 1000.0000 | 8780000.0 | 0.8894 | 0.8747 | 0.9038 | 20 | results/t5_noise.csv |
| F5 | deployed | FQ-raw | none | 10000.0 | 87800000.0 | 0.8613 | 0.8394 | 0.8812 | 20 | results/t5_noise.csv |
| F5 | full_gram | PQK-1 | none | 100.0000 | 48000.0 | 0.7374 | 0.7205 | 0.7536 | 20 | results/t5_noise.csv |
| F5 | full_gram | PQK-1 | none | 1000.0000 | 480000.0 | 0.8717 | 0.8606 | 0.8819 | 20 | results/t5_noise.csv |
| F5 | full_gram | PQK-1 | none | 10000.0 | 4800000.0 | 0.9036 | 0.8939 | 0.9131 | 20 | results/t5_noise.csv |
| F5 | full_gram | PQK-2nn | none | 100.0000 | 72000.0 | 0.8576 | 0.8460 | 0.8671 | 20 | results/t5_noise.csv |
| F5 | full_gram | PQK-2nn | none | 1000.0000 | 720000.0 | 0.9574 | 0.9519 | 0.9627 | 20 | results/t5_noise.csv |
| F5 | full_gram | PQK-2nn | none | 10000.0 | 7200000.0 | 0.9725 | 0.9659 | 0.9777 | 20 | results/t5_noise.csv |
| F5 | full_gram | E | raw | 100.0000 | 72000.0 | 0.8237 | 0.8074 | 0.8390 | 20 | results/t5_noise.csv |
| F5 | full_gram | E | raw | 1000.0000 | 720000.0 | 0.9571 | 0.9522 | 0.9616 | 20 | results/t5_noise.csv |
| F5 | full_gram | E | raw | 10000.0 | 7200000.0 | 0.9815 | 0.9750 | 0.9861 | 20 | results/t5_noise.csv |
| F5 | full_gram | E2 | raw | 100.0000 | 72000.0 | 0.8583 | 0.8470 | 0.8674 | 20 | results/t5_noise.csv |
| F5 | full_gram | E2 | raw | 1000.0000 | 720000.0 | 0.9571 | 0.9521 | 0.9620 | 20 | results/t5_noise.csv |
| F5 | full_gram | E2 | raw | 10000.0 | 7200000.0 | 0.9721 | 0.9652 | 0.9774 | 20 | results/t5_noise.csv |
| F5 | full_gram | F | std | 100.0000 | 72000.0 | 0.8338 | 0.8218 | 0.8459 | 20 | results/t5_noise.csv |
| F5 | full_gram | F | std | 1000.0000 | 720000.0 | 0.9405 | 0.9332 | 0.9474 | 20 | results/t5_noise.csv |
| F5 | full_gram | F | std | 10000.0 | 7200000.0 | 0.9653 | 0.9556 | 0.9728 | 20 | results/t5_noise.csv |
| F5 | full_gram | FQ-clipped | none | 100.0000 | 2868000.0 | 0.8101 | 0.7920 | 0.8279 | 20 | results/t5_noise.csv |
| F5 | full_gram | FQ-clipped | none | 1000.0000 | 28680000.0 | 0.8693 | 0.8247 | 0.9045 | 20 | results/t5_noise.csv |
| F5 | full_gram | FQ-clipped | none | 10000.0 | 286800000.0 | 0.9630 | 0.9553 | 0.9686 | 20 | results/t5_noise.csv |
| F5 | full_gram | FQ-raw | none | 100.0000 | 2868000.0 | 0.7634 | 0.7433 | 0.7841 | 20 | results/t5_noise.csv |
| F5 | full_gram | FQ-raw | none | 1000.0000 | 28680000.0 | 0.8894 | 0.8747 | 0.9038 | 20 | results/t5_noise.csv |
| F5 | full_gram | FQ-raw | none | 10000.0 | 286800000.0 | 0.8613 | 0.8394 | 0.8812 | 20 | results/t5_noise.csv |

### Figure 6: FQ Training Gram Spectrum Indefiniteness
*Source Data:* `figures/data/fig_fq_spectrum.csv`

| figure | panel | model | shots | mean_abs_lam_min | ci_low | ci_high | frac_seeds_negative | n_seeds | source_file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F6 | main | FQ-raw | 100.0000 | 0.5598 | 0.5380 | 0.5841 | 1.0000 | 20 | results/t5_noise.csv |
| F6 | main | FQ-raw | 1000.0000 | 0.1584 | 0.1513 | 0.1650 | 1.0000 | 20 | results/t5_noise.csv |
| F6 | main | FQ-raw | 10000.0 | 0.0423 | 0.0407 | 0.0440 | 1.0000 | 20 | results/t5_noise.csv |

### Figure 7: Depolarizing Noise Degradation (Retuned Per-Qubit Proxy)
*Source Data:* `figures/data/fig_depolarizing_retuned_per_qubit_proxy.csv`

| figure | panel | model | p | mean_r2 | ci_low | ci_high | n_seeds | source_file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F7 | main | PQK-1 (== RBF on <X>) | 0.0000 | 0.8986 | 0.8847 | 0.9111 | 20 | results/t5_noise.csv |
| F7 | main | PQK-1 (== RBF on <X>) | 0.0100 | 0.8991 | 0.8856 | 0.9113 | 20 | results/t5_noise.csv |
| F7 | main | PQK-1 (== RBF on <X>) | 0.0200 | 0.8998 | 0.8872 | 0.9113 | 20 | results/t5_noise.csv |
| F7 | main | PQK-1 (== RBF on <X>) | 0.0400 | 0.9004 | 0.8890 | 0.9112 | 20 | results/t5_noise.csv |
| F7 | main | PQK-1 (== RBF on <X>) | 0.0600 | 0.9006 | 0.8897 | 0.9110 | 20 | results/t5_noise.csv |
| F7 | main | PQK-1 (== RBF on <X>) | 0.0800 | 0.9024 | 0.8915 | 0.9123 | 20 | results/t5_noise.csv |
| F7 | main | PQK-2nn | 0.0000 | 0.9789 | 0.9731 | 0.9833 | 20 | results/t5_noise.csv |
| F7 | main | PQK-2nn | 0.0100 | 0.9786 | 0.9729 | 0.9831 | 20 | results/t5_noise.csv |
| F7 | main | PQK-2nn | 0.0200 | 0.9784 | 0.9726 | 0.9828 | 20 | results/t5_noise.csv |
| F7 | main | PQK-2nn | 0.0400 | 0.9776 | 0.9692 | 0.9836 | 20 | results/t5_noise.csv |
| F7 | main | PQK-2nn | 0.0600 | 0.9772 | 0.9687 | 0.9833 | 20 | results/t5_noise.csv |
| F7 | main | PQK-2nn | 0.0800 | 0.9770 | 0.9686 | 0.9831 | 20 | results/t5_noise.csv |
| F7 | main | FQ | 0.0000 | 0.9902 | 0.9889 | 0.9915 | 20 | results/t5_noise.csv |
| F7 | main | FQ | 0.0100 | 0.9903 | 0.9889 | 0.9916 | 20 | results/t5_noise.csv |
| F7 | main | FQ | 0.0200 | 0.9901 | 0.9886 | 0.9915 | 20 | results/t5_noise.csv |
| F7 | main | FQ | 0.0400 | 0.9900 | 0.9886 | 0.9914 | 20 | results/t5_noise.csv |
| F7 | main | FQ | 0.0600 | 0.9900 | 0.9884 | 0.9915 | 20 | results/t5_noise.csv |
| F7 | main | FQ | 0.0800 | 0.9900 | 0.9883 | 0.9915 | 20 | results/t5_noise.csv |
| F7 | main | E (raw) | 0.0000 | 0.9872 | 0.9847 | 0.9893 | 20 | results/t5_noise.csv |
| F7 | main | E (raw) | 0.0100 | 0.9872 | 0.9848 | 0.9894 | 20 | results/t5_noise.csv |
| F7 | main | E (raw) | 0.0200 | 0.9872 | 0.9849 | 0.9894 | 20 | results/t5_noise.csv |
| F7 | main | E (raw) | 0.0400 | 0.9875 | 0.9854 | 0.9894 | 20 | results/t5_noise.csv |
| F7 | main | E (raw) | 0.0600 | 0.9875 | 0.9855 | 0.9894 | 20 | results/t5_noise.csv |
| F7 | main | E (raw) | 0.0800 | 0.9874 | 0.9855 | 0.9891 | 20 | results/t5_noise.csv |
| F7 | main | E (std) | 0.0000 | 0.9801 | 0.9767 | 0.9833 | 20 | results/t5_noise.csv |
| F7 | main | E (std) | 0.0100 | 0.9801 | 0.9767 | 0.9833 | 20 | results/t5_noise.csv |
| F7 | main | E (std) | 0.0200 | 0.9801 | 0.9767 | 0.9833 | 20 | results/t5_noise.csv |
| F7 | main | E (std) | 0.0400 | 0.9801 | 0.9767 | 0.9833 | 20 | results/t5_noise.csv |
| F7 | main | E (std) | 0.0600 | 0.9801 | 0.9767 | 0.9833 | 20 | results/t5_noise.csv |
| F7 | main | E (std) | 0.0800 | 0.9801 | 0.9767 | 0.9833 | 20 | results/t5_noise.csv |
| F7 | main | E2 (raw) | 0.0000 | 0.9786 | 0.9727 | 0.9833 | 20 | results/t5_noise.csv |
| F7 | main | E2 (raw) | 0.0100 | 0.9784 | 0.9725 | 0.9831 | 20 | results/t5_noise.csv |
| F7 | main | E2 (raw) | 0.0200 | 0.9775 | 0.9690 | 0.9834 | 20 | results/t5_noise.csv |
| F7 | main | E2 (raw) | 0.0400 | 0.9769 | 0.9685 | 0.9829 | 20 | results/t5_noise.csv |
| F7 | main | E2 (raw) | 0.0600 | 0.9769 | 0.9686 | 0.9829 | 20 | results/t5_noise.csv |
| F7 | main | E2 (raw) | 0.0800 | 0.9775 | 0.9693 | 0.9834 | 20 | results/t5_noise.csv |
| F7 | main | F (std) | 0.0000 | 0.9728 | 0.9663 | 0.9776 | 20 | results/t5_noise.csv |
| F7 | main | F (std) | 0.0100 | 0.9728 | 0.9663 | 0.9776 | 20 | results/t5_noise.csv |
| F7 | main | F (std) | 0.0200 | 0.9728 | 0.9663 | 0.9776 | 20 | results/t5_noise.csv |
| F7 | main | F (std) | 0.0400 | 0.9728 | 0.9663 | 0.9776 | 20 | results/t5_noise.csv |
| F7 | main | F (std) | 0.0600 | 0.9728 | 0.9663 | 0.9776 | 20 | results/t5_noise.csv |
| F7 | main | F (std) | 0.0800 | 0.9728 | 0.9663 | 0.9776 | 20 | results/t5_noise.csv |

### Figure 8: SVR Epsilon Hyperparameter Selection Distribution
*Source Data:* `figures/data/fig_epsilon_selection.csv`

| figure | panel | epsilon | count | source_file | model | c_low_pct | c_high_pct | eps_low_pct | eps_high_pct |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F8 | left_histogram | 0.0010 | 1236.0000 | results/t1_entropy_gridv3.csv + results/t4_v2_gridv3.csv | nan | nan | nan | nan | nan |
| F8 | left_histogram | 0.0030 | 456.0000 | results/t1_entropy_gridv3.csv + results/t4_v2_gridv3.csv | nan | nan | nan | nan | nan |
| F8 | left_histogram | 0.0100 | 630.0000 | results/t1_entropy_gridv3.csv + results/t4_v2_gridv3.csv | nan | nan | nan | nan | nan |
| F8 | left_histogram | 0.0300 | 706.0000 | results/t1_entropy_gridv3.csv + results/t4_v2_gridv3.csv | nan | nan | nan | nan | nan |
| F8 | left_histogram | 0.1000 | 570.0000 | results/t1_entropy_gridv3.csv + results/t4_v2_gridv3.csv | nan | nan | nan | nan | nan |
| F8 | right_edge_pct | nan | nan | results/grid_boundary_post_v3.csv | PQK-1 (== RBF on <X>) | 1.5385 | 9.6154 | 23.8462 | 29.2308 |
| F8 | right_edge_pct | nan | nan | results/grid_boundary_post_v3.csv | PQK-2nn | 2.6923 | 0.3846 | 36.1538 | 10.0000 |
| F8 | right_edge_pct | nan | nan | results/grid_boundary_post_v3.csv | FQ | 0.0000 | 0.0000 | 35.3846 | 13.8462 |
| F8 | right_edge_pct | nan | nan | results/grid_boundary_post_v3.csv | E | 7.5000 | 0.5769 | 42.8846 | 8.0769 |
| F8 | right_edge_pct | nan | nan | results/grid_boundary_post_v3.csv | E2 | 3.0769 | 0.3846 | 36.5385 | 11.5385 |
| F8 | right_edge_pct | nan | nan | results/grid_boundary_post_v3.csv | F | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

### Figure A1: Hyperparameter Grid Widening Sensitivity
*Source Data:* `figures/data/appendix_grid_sensitivity.csv`

| figure | panel | grid_version | model | N_train | mean_r2 | ci_low | ci_high | n_seeds | source_file |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | T1_N40 | v1 | PQK-1 (== RBF on <X>) | 40 | 0.9048 | 0.8948 | 0.9142 | 20 | results/t1_entropy.csv |
| A1 | T1_N40 | v1 | PQK-2nn | 40 | 0.9726 | 0.9703 | 0.9750 | 20 | results/t1_entropy.csv |
| A1 | T1_N40 | v1 | FQ | 40 | 0.9826 | 0.9811 | 0.9841 | 20 | results/t1_entropy.csv |
| A1 | T1_N40 | v1 | E (raw) | 40 | 0.9811 | 0.9791 | 0.9829 | 20 | results/t1_entropy.csv |
| A1 | T1_N40 | v1 | E2 (raw) | 40 | 0.9722 | 0.9698 | 0.9746 | 20 | results/t1_entropy.csv |
| A1 | T1_N40 | v1 | F (std) | 40 | 0.9728 | 0.9664 | 0.9776 | 20 | results/t1_entropy.csv |
| A1 | T1_N160 | v1 | PQK-1 (== RBF on <X>) | 160 | 0.9554 | 0.9535 | 0.9573 | 20 | results/t1_entropy.csv |
| A1 | T1_N160 | v1 | PQK-2nn | 160 | 0.9904 | 0.9896 | 0.9911 | 20 | results/t1_entropy.csv |
| A1 | T1_N160 | v1 | FQ | 160 | 0.9924 | 0.9920 | 0.9929 | 20 | results/t1_entropy.csv |
| A1 | T1_N160 | v1 | E (raw) | 160 | 0.9933 | 0.9928 | 0.9937 | 20 | results/t1_entropy.csv |
| A1 | T1_N160 | v1 | E2 (raw) | 160 | 0.9903 | 0.9895 | 0.9911 | 20 | results/t1_entropy.csv |
| A1 | T1_N160 | v1 | F (std) | 160 | 0.9887 | 0.9878 | 0.9894 | 20 | results/t1_entropy.csv |
| A1 | T2b_N40 | v1 | PQK-1 (== RBF on <X>) | 40 | 0.8840 | 0.8685 | 0.8975 | 20 | results/t2_correlators.csv |
| A1 | T2b_N40 | v1 | PQK-2nn | 40 | 0.9274 | 0.9195 | 0.9354 | 20 | results/t2_correlators.csv |
| A1 | T2b_N40 | v1 | FQ | 40 | 0.9448 | 0.9368 | 0.9521 | 20 | results/t2_correlators.csv |
| A1 | T2b_N40 | v1 | E (raw) | 40 | 0.9270 | 0.9181 | 0.9352 | 20 | results/t2_correlators.csv |
| A1 | T2b_N40 | v1 | E2 (raw) | 40 | 0.9247 | 0.9153 | 0.9342 | 20 | results/t2_correlators.csv |
| A1 | T2b_N40 | v1 | F (std) | 40 | 0.8902 | 0.8355 | 0.9249 | 20 | results/t2_correlators.csv |
| A1 | T2b_N160 | v1 | PQK-1 (== RBF on <X>) | 160 | 0.9643 | 0.9614 | 0.9671 | 20 | results/t2_correlators.csv |
| A1 | T2b_N160 | v1 | PQK-2nn | 160 | 0.9850 | 0.9830 | 0.9868 | 20 | results/t2_correlators.csv |
| A1 | T2b_N160 | v1 | FQ | 160 | 0.9880 | 0.9867 | 0.9892 | 20 | results/t2_correlators.csv |
| A1 | T2b_N160 | v1 | E (raw) | 160 | 0.9843 | 0.9827 | 0.9858 | 20 | results/t2_correlators.csv |
| A1 | T2b_N160 | v1 | E2 (raw) | 160 | 0.9852 | 0.9833 | 0.9869 | 20 | results/t2_correlators.csv |
| A1 | T2b_N160 | v1 | F (std) | 160 | 0.9757 | 0.9738 | 0.9776 | 20 | results/t2_correlators.csv |
| A1 | T1_N40 | v2 | PQK-1 (== RBF on <X>) | 40 | 0.9046 | 0.8953 | 0.9135 | 20 | results/t1_entropy_gridv2.csv |
| A1 | T1_N40 | v2 | PQK-2nn | 40 | 0.9717 | 0.9689 | 0.9746 | 20 | results/t1_entropy_gridv2.csv |
| A1 | T1_N40 | v2 | FQ | 40 | 0.9826 | 0.9811 | 0.9841 | 20 | results/t1_entropy_gridv2.csv |
| A1 | T1_N40 | v2 | E (raw) | 40 | 0.9807 | 0.9785 | 0.9826 | 20 | results/t1_entropy_gridv2.csv |
| A1 | T1_N40 | v2 | E2 (raw) | 40 | 0.9715 | 0.9687 | 0.9744 | 20 | results/t1_entropy_gridv2.csv |
| A1 | T1_N40 | v2 | F (std) | 40 | 0.9728 | 0.9663 | 0.9776 | 20 | results/t1_entropy_gridv2.csv |
| A1 | T1_N160 | v2 | PQK-1 (== RBF on <X>) | 160 | 0.9537 | 0.9511 | 0.9564 | 20 | results/t1_entropy_gridv2.csv |
| A1 | T1_N160 | v2 | PQK-2nn | 160 | 0.9905 | 0.9897 | 0.9913 | 20 | results/t1_entropy_gridv2.csv |
| A1 | T1_N160 | v2 | FQ | 160 | 0.9924 | 0.9920 | 0.9929 | 20 | results/t1_entropy_gridv2.csv |
| A1 | T1_N160 | v2 | E (raw) | 160 | 0.9935 | 0.9931 | 0.9938 | 20 | results/t1_entropy_gridv2.csv |
| A1 | T1_N160 | v2 | E2 (raw) | 160 | 0.9906 | 0.9897 | 0.9915 | 20 | results/t1_entropy_gridv2.csv |
| A1 | T1_N160 | v2 | F (std) | 160 | 0.9887 | 0.9878 | 0.9894 | 20 | results/t1_entropy_gridv2.csv |
| A1 | T2b_N40 | v2 | PQK-1 (== RBF on <X>) | 40 | 0.8810 | 0.8599 | 0.8990 | 20 | results/t2_correlators_gridv2.csv |
| A1 | T2b_N40 | v2 | PQK-2nn | 40 | 0.9233 | 0.9139 | 0.9332 | 20 | results/t2_correlators_gridv2.csv |
| A1 | T2b_N40 | v2 | FQ | 40 | 0.9448 | 0.9368 | 0.9521 | 20 | results/t2_correlators_gridv2.csv |
| A1 | T2b_N40 | v2 | E (raw) | 40 | 0.9380 | 0.9318 | 0.9438 | 20 | results/t2_correlators_gridv2.csv |
| A1 | T2b_N40 | v2 | E2 (raw) | 40 | 0.9248 | 0.9153 | 0.9344 | 20 | results/t2_correlators_gridv2.csv |
| A1 | T2b_N40 | v2 | F (std) | 40 | 0.8862 | 0.8237 | 0.9249 | 20 | results/t2_correlators_gridv2.csv |
| A1 | T2b_N160 | v2 | PQK-1 (== RBF on <X>) | 160 | 0.9618 | 0.9581 | 0.9654 | 20 | results/t2_correlators_gridv2.csv |
| A1 | T2b_N160 | v2 | PQK-2nn | 160 | 0.9872 | 0.9858 | 0.9885 | 20 | results/t2_correlators_gridv2.csv |
| A1 | T2b_N160 | v2 | FQ | 160 | 0.9880 | 0.9867 | 0.9892 | 20 | results/t2_correlators_gridv2.csv |
| A1 | T2b_N160 | v2 | E (raw) | 160 | 0.9870 | 0.9857 | 0.9882 | 20 | results/t2_correlators_gridv2.csv |
| A1 | T2b_N160 | v2 | E2 (raw) | 160 | 0.9872 | 0.9858 | 0.9885 | 20 | results/t2_correlators_gridv2.csv |
| A1 | T2b_N160 | v2 | F (std) | 160 | 0.9757 | 0.9738 | 0.9776 | 20 | results/t2_correlators_gridv2.csv |
| A1 | T1_N40 | v3 | PQK-1 (== RBF on <X>) | 40 | 0.8986 | 0.8847 | 0.9111 | 20 | results/t1_entropy_gridv3.csv |
| A1 | T1_N40 | v3 | PQK-2nn | 40 | 0.9789 | 0.9731 | 0.9833 | 20 | results/t1_entropy_gridv3.csv |
| A1 | T1_N40 | v3 | FQ | 40 | 0.9902 | 0.9889 | 0.9915 | 20 | results/t1_entropy_gridv3.csv |
| A1 | T1_N40 | v3 | E (raw) | 40 | 0.9872 | 0.9847 | 0.9893 | 20 | results/t1_entropy_gridv3.csv |
| A1 | T1_N40 | v3 | E2 (raw) | 40 | 0.9786 | 0.9727 | 0.9833 | 20 | results/t1_entropy_gridv3.csv |
| A1 | T1_N40 | v3 | F (std) | 40 | 0.9728 | 0.9663 | 0.9776 | 20 | results/t1_entropy_gridv3.csv |
| A1 | T1_N160 | v3 | PQK-1 (== RBF on <X>) | 160 | 0.9529 | 0.9505 | 0.9553 | 20 | results/t1_entropy_gridv3.csv |
| A1 | T1_N160 | v3 | PQK-2nn | 160 | 0.9943 | 0.9936 | 0.9950 | 20 | results/t1_entropy_gridv3.csv |
| A1 | T1_N160 | v3 | FQ | 160 | 0.9975 | 0.9972 | 0.9978 | 20 | results/t1_entropy_gridv3.csv |
| A1 | T1_N160 | v3 | E (raw) | 160 | 0.9987 | 0.9986 | 0.9989 | 20 | results/t1_entropy_gridv3.csv |
| A1 | T1_N160 | v3 | E2 (raw) | 160 | 0.9942 | 0.9935 | 0.9950 | 20 | results/t1_entropy_gridv3.csv |
| A1 | T1_N160 | v3 | F (std) | 160 | 0.9887 | 0.9878 | 0.9894 | 20 | results/t1_entropy_gridv3.csv |
| A1 | T2b_N40 | v3 | PQK-1 (== RBF on <X>) | 40 | 0.8900 | 0.8698 | 0.9065 | 20 | results/t2_correlators_gridv3.csv |
| A1 | T2b_N40 | v3 | PQK-2nn | 40 | 0.9443 | 0.9297 | 0.9570 | 20 | results/t2_correlators_gridv3.csv |
| A1 | T2b_N40 | v3 | FQ | 40 | 0.9705 | 0.9636 | 0.9763 | 20 | results/t2_correlators_gridv3.csv |
| A1 | T2b_N40 | v3 | E (raw) | 40 | 0.9462 | 0.9406 | 0.9517 | 20 | results/t2_correlators_gridv3.csv |
| A1 | T2b_N40 | v3 | E2 (raw) | 40 | 0.9432 | 0.9289 | 0.9558 | 20 | results/t2_correlators_gridv3.csv |
| A1 | T2b_N40 | v3 | F (std) | 40 | 0.8862 | 0.8237 | 0.9249 | 20 | results/t2_correlators_gridv3.csv |
| A1 | T2b_N160 | v3 | PQK-1 (== RBF on <X>) | 160 | 0.9603 | 0.9568 | 0.9640 | 20 | results/t2_correlators_gridv3.csv |
| A1 | T2b_N160 | v3 | PQK-2nn | 160 | 0.9988 | 0.9986 | 0.9990 | 20 | results/t2_correlators_gridv3.csv |
| A1 | T2b_N160 | v3 | FQ | 160 | 0.9989 | 0.9987 | 0.9991 | 20 | results/t2_correlators_gridv3.csv |
| A1 | T2b_N160 | v3 | E (raw) | 160 | 0.9989 | 0.9987 | 0.9991 | 20 | results/t2_correlators_gridv3.csv |
| A1 | T2b_N160 | v3 | E2 (raw) | 160 | 0.9988 | 0.9985 | 0.9990 | 20 | results/t2_correlators_gridv3.csv |
| A1 | T2b_N160 | v3 | F (std) | 160 | 0.9757 | 0.9738 | 0.9776 | 20 | results/t2_correlators_gridv3.csv |
