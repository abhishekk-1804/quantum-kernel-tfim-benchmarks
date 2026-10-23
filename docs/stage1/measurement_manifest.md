# S1.8 Measurement and Shot Budget Manifest

Status: VERIFIED (All theoretical formulas match production code and `results/t5_noise.csv`)

## 1. Measurement Settings and Shot Accounting Manifest

Protocol: Open-chain disordered TFIM ($n=8$, $N_{\text{train}}=40$, $N_{\text{test}}=200$, total states $m=240$).

| Model Arm | Features Consumed | Feature Dim | Pauli Bases Sampled | Shots / State | Deployed Cost ($N_{\text{te}}=200$) | Full-Gram Cost ($m=240$) | Notes |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **PQK-1 (X+Z, t5 production)** | 1-RDM: <X_i>, <Z_i> | 16 | X, Z (2 bases) | 2 S | 2 * 200 * S = 400 S | 2 * 240 * S = 480 S | Includes Basis Z (absent from noiseless arm). Issue R2. |
| **PQK-1 (X-only, ablation)** | 1-RDM: <X_i> | 8 | X (1 basis) | 1 S | 1 * 200 * S = 200 S | 1 * 240 * S = 240 S | Matches exact feature family used in noiseless Task 1. |
| **PQK-2nn** | 2-RDM: X_i, X_j, XX_ij, YY_ij, ZZ_ij (NN) | 35 | X, Y, Z (3 bases) | 3 S | 3 * 200 * S = 600 S | 3 * 240 * S = 720 S | Shared basis reconstructs all 1-body and NN 2-body correlators. |
| **FQ (raw & clipped)** | Swap-test fidelity |<psi_i|psi_j>|^2 | N/A (Gram directly) | Bell/Swap basis on state pairs | N/A (Pairwise) | 40 * 200 * S = 8000 S | m(m-1)/2 * S = 28680 S | Requires quadratic pairwise measurement pairs (O(m^2)). |
| **E (raw & std)** | Full correlators: 3n 1-body + all ZZ 2-body | 52 | X, Y, Z (3 bases) | 3 S | 3 * 200 * S = 600 S | 3 * 240 * S = 720 S | Reconstructed from the exact same 3 basis shots as PQK-2nn. |
| **E2 (raw)** | 2-pt Pauli nearest-neighbor (identical to PQK-2nn) | 35 | X, Y, Z (3 bases) | 3 S | 3 * 200 * S = 600 S | 3 * 240 * S = 720 S | Exact same feature vector as PQK-2nn. Issue R1. |
| **F (std)** | Ridge regression on standardized full correlators | 52 | X, Y, Z (3 bases) | 3 S | 3 * 200 * S = 600 S | 3 * 240 * S = 720 S | Linear Ridge baseline on 3-basis measurements. |

## 2. Fidelity (FQ) Block Decomposition

The destructive swap test measures state pairs directly. The total shot count is partitioned into distinct blocks:

- **Train-Train Block:** $N_{\text{tr}}(N_{\text{tr}} - 1)/2 = 40 \times 39 / 2 =$ **780** settings ($780 S$ total shots)
- **Train-Test Block:** $N_{\text{tr}} \times N_{\text{te}} = 40 \times 200 =$ **8000** settings ($8,000 S$ total shots)
- **Test-Test Block:** $N_{\text{te}}(N_{\text{te}} - 1)/2 = 200 \times 199 / 2 =$ **19900** settings ($19,900 S$ total shots)
- **Total Gram Matrix:** $780 + 8,000 + 19,900 =$ **28680** settings (**28680 S** total shots)

> [!NOTE]
> In a real deployed prediction scenario, only the **Train-Test** block ($8,000 S$) must be evaluated to predict on new test states. The test-test block ($19,900 S$) is required only for full out-of-sample Gram evaluation.

## 3. Discrepancy Analysis (Issue R2)

In Task 1 noiseless benchmarks (`results/t1_entropy_gridv3.csv`), `PQK-1` uses solely the transverse magnetization $\langle X_i \rangle$ ($n=8$ features) because $\langle Z_i \rangle = 0$ by parity symmetry.

In finite-shot benchmarks (`results/t5_noise.csv`), the production implementation of `PQK-1` reconstructs both $\langle X_i \rangle$ and $\langle Z_i \rangle$ ($16$ features) by sampling both basis $X$ and basis $Z$ ($2 S$ shots per state). Consequently:
1. `PQK-1` in `t5_noise.csv` incurs double the shot cost ($2 m S$ vs $1 m S$) compared to an $X$-only protocol.
2. The finite-shot arm includes shot noise from measuring the vanishing $Z$-basis expectations $\langle Z_i \rangle$.
3. The S1.2 ablation (`results/ablations/t5_pqk1_basis.csv`) quantifies the exact performance delta between $X$-only and $X+Z$ protocols.
