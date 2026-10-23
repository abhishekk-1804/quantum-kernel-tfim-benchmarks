# R3 Audit: Fidelity Gram Matrix PSD Clipping Paths

Status: EXPLORATORY (Audit & Sensitivity Probe)

## 1. Source Code Inspection of Clipping Call Sites

Every call site of `fidelity_clip_psd` and `clip_psd` across the repository was statically identified:

| File | Line | Symbol / Context | Matrix Input | Matrix Clipped | Fit Matrix to SVR | Predict Matrix to SVR |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `scripts/run_t5_noise.py` | 179 | `def evaluate_svr_precomputed(..., clip_psd=False)` | Parameter declaration | N/A | N/A | N/A |
| `scripts/run_t5_noise.py` | 192-194 | `if clip_psd: K_fold_tr = fidelity_clip_psd(K_fold_tr)` | Inner CV fold train block | Fold train-train (`K_fold_tr`) | `K_fold_tr` (clipped) | `K_fold_val` (unclipped) |
| `scripts/run_t5_noise.py` | 214-217 | `K_fit_tr = fidelity_clip_psd(K_tr) if clip_psd else K_tr` | Full training Gram | Train-train (`K_tr`) | `K_fit_tr` (clipped) | `K_te` (unclipped) |
| `scripts/run_t5_noise.py` | 520-522 | Call for `Arm 3: FQ-raw` | Raw noisy Gram blocks | None (`clip_psd=False`) | `K_hat_tr` (raw) | `K_hat_te` (raw) |
| `scripts/run_t5_noise.py` | 535-537 | Call for `Arm 4: FQ-clipped` | Raw noisy Gram blocks | Train-train only (`clip_psd=True`) | `K_fit_tr` (clipped) | `K_hat_te` (unclipped) |
| `scripts/run_t5_noise.py` | 696-698 | Call for `Arm 3: FQ (mixed_state_overlap)` | Analytic depolarizing Gram | None (`clip_psd=False`) | `K_depol_tr` (analytic) | `K_depol_te` (analytic) |
| `src/noise.py` | 197-223 | `def fidelity_clip_psd(K)` | Implementation | Symmetric $m \times m$ matrix | N/A (algorithm definition) | N/A |
| `tests/test_physics_core.py` | 1274-1275 | Test suite verification | Synthetic noisy matrix | Entire synthetic matrix | Verified PSD $\lambda_{\min} \ge 0$ | N/A |

### Key Observations from Source Code Inspection
1. **Train-Only Clipping:** In the current production pipeline (`scripts/run_t5_noise.py`), `clip_psd=True` clips ONLY the square training Gram matrix $K_{\text{tr}} \in \mathbb{R}^{N_{\text{tr}} \times N_{\text{tr}}}$ (and inner CV fold training blocks $K_{\text{fold\_tr}}$). It does NOT clip the rectangular test-train block $K_{\text{te}} \in \mathbb{R}^{N_{\text{te}} \times N_{\text{tr}}}$.
2. **Joint Gram Matrix:** The joint $(N_{\text{tr}} + N_{\text{te}}) \times (N_{\text{tr}} + N_{\text{te}})$ matrix is never projected onto the PSD cone in the production pipeline.

## 2. Numerical Sensitivity Probe (5 Seeds, S=1000)

Comparison between:
- **Method (a) [Current production]:** Clip train Gram matrix $K_{\text{tr}}$ only.
- **Method (b) [Exploratory alternative]:** Clip joint $(N_{\text{tr}} + N_{\text{te}}) \times (N_{\text{tr}} + N_{\text{te}})$ Gram matrix first, then slice into train and test blocks.

| Seed | $R^2$ (a: train-only) | $R^2$ (b: joint-clipped) | $\Delta R^2$ (b - a) | MAE (a) | MAE (b) | $\lambda_{\min}(K_{\text{tr}})$ raw | $\lambda_{\min}(K_{\text{tr}})$ clipped | $\lambda_{\min}(K_{\text{joint}})$ raw | $\lambda_{\min}(K_{\text{joint}})$ clipped | $\lambda_{\min}(K_{\text{joint\_tr}})$ sliced |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | 0.9115 | 0.9637 | +0.0522 | 0.0523 | 0.0340 | -1.567e-01 | -4.742e-15 | -5.127e-01 | -9.488e-15 | 2.701e-02 |
| 1 | 0.9284 | 0.9653 | +0.0370 | 0.0476 | 0.0318 | -1.408e-01 | -5.652e-15 | -5.002e-01 | -1.171e-14 | 3.069e-02 |
| 2 | 0.9243 | 0.9575 | +0.0333 | 0.0497 | 0.0369 | -1.969e-01 | -6.339e-15 | -5.135e-01 | -1.932e-14 | 3.053e-02 |
| 3 | 0.4839 | 0.9590 | +0.4752 | 0.1371 | 0.0373 | -1.485e-01 | -1.954e-15 | -5.144e-01 | -2.385e-14 | 2.719e-02 |
| 4 | 0.8316 | 0.9591 | +0.1275 | 0.0787 | 0.0365 | -1.470e-01 | -3.393e-15 | -5.257e-01 | -3.454e-14 | 2.856e-02 |
| **Mean** | **0.8159** | **0.9609** | **+0.1450** | - | - | - | - | - | - | - |

### Numerical Observations
- Across 5 seeds at S=1000, the mean R2 for train-only clipping (Method a) is 0.8159, while joint clipping (Method b) yields 0.9609 (mean difference Delta R2 = +0.1450).
- Slicing a principal submatrix from a PSD joint Gram matrix guarantees that the resulting training submatrix remains PSD (Cauchy interlacing theorem: lambda_i(K_joint_tr) >= lambda_min(K_joint) = 0).
