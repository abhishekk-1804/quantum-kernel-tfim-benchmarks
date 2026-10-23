# Gate-0 Reproduction Card: Contributor C4 (Measurement & Noise)

## 1. Specifications
- **Baseline Commit:** `739a724919f52164193a200b6e07d827fe273c62`
- **Environment Spec:** Python 3.12.10, NumPy 2.5.4, SciPy 1.18.1, scikit-learn 1.9.1 in active virtual environment `D:\qml_env`
- **Config File:** `scripts/run_t5_noise.py`
- **Arm:** Measurement Noise Engine & Open-System Depolarizing Simulator (`src/noise.py`)
- **Seeds:** Fixed benchmark evaluation seeds 0–19

---

## 2. Verification Commands
Execute the following verification command:
```powershell
D:\qml_env\Scripts\python.exe -m pytest tests/test_noise_engine.py -v
```

---

## 3. Expected Artifacts and Metrics
- **Expected Output Artifact:** Passing test suite verifying multinomial sampling convergence, basis rotation unitary consistency, swap test unbiasedness, and depolarizing density matrix channel attenuation.
- **Expected Benchmark Metrics:**
  - **Source File:** `results/t5_noise.csv`
  - **Finite Shots ($S=1000$, Seed 0, Metric $R^2$):**
    - Row 2009 (`FQ-clipped`): `0.9105805334`
    - Row 2011 (`FQ-raw`): `0.8980248751`
    - Row 2013 (`PQK-1`): `0.8873289150`
    - Row 2015 (`PQK-2nn`): `0.9529091232`
    - Row 2001 (`E (raw)`): `0.9652256323`
    - Row 2005 (`E2 (raw)`): `0.9534911352`
  - **Depolarizing Noise ($p=0.08$, Seed 0, Metric $R^2$):**
    - Row 1409 (`FQ`, `mixed_state_overlap`): `0.9932191409`
    - Row 1413 (`PQK-2nn`, `none`): `0.9808078086`
    - Row 1401 (`E (raw)`, `raw`): `0.9916279444`
    - Row 1405 (`E2 (raw)`, `raw`): `0.9810277401`
- **Tolerances:**
  - Metric reproduction: $|R^2_{\text{reproduced}} - R^2_{\text{expected}}| < 1.0 \times 10^{-10}$
  - Swap test sample mean convergence: within $3\sigma$ binomial confidence bounds
  - Minimum eigenvalue $\lambda_{\min}$ of raw finite-shot Gram: $< 0$ across 20/20 seeds

---

## 4. Measurement Pauli Basis Consumption Manifest
In `scripts/run_t5_noise.py` (lines 440–475), measurements across $m=240$ states are grouped into commuting Pauli bases:
1. **PQK-1 Arm:**
   - Consumes **2 bases**: Basis X (for $\langle X_i \rangle$) and Basis Z (for $\langle Z_i \rangle$).
   - Total shot cost: $2 \times m \times S = 480 \cdot S$ shots.
2. **PQK-2nn Arm:**
   - Consumes **3 bases**: Basis X (for $\langle X_i \rangle, \langle X_i X_{i+1} \rangle$), Basis Y (for $\langle Y_i Y_{i+1} \rangle$), and Basis Z (for $\langle Z_i Z_{i+1} \rangle$).
   - Total shot cost: $3 \times m \times S = 720 \cdot S$ shots.
3. **E2 (raw) Arm:**
   - Consumes **3 bases**: Basis X, Basis Y, and Basis Z (identical to PQK-2nn, 35 features).
   - Total shot cost: $3 \times m \times S = 720 \cdot S$ shots.
4. **E (raw) & E (std) Arms:**
   - Consumes **2 active bases**: Basis X (for $\langle X_i \rangle$) and Basis Z (for $\langle Z_i \rangle$ and all 28 $\langle Z_i Z_j \rangle$ pairs). 1-body $Y$ features are set to zero.
   - Total shot cost recorded: $3 \times m \times S = 720 \cdot S$ shots (standard 3-basis budget).
5. **F (std) Arm:**
   - Linear ridge regressor on full 2-body correlators, consuming the same 2 active bases (recorded as $3 \times m \times S$).
6. **FQ-raw & FQ-clipped Arms:**
   - Consumes destructive swap tests on distinct state pairs ($K_{ij} = |\langle \psi_i | \psi_j \rangle|^2$).
   - Deployed shot cost: $\binom{40}{2} S + 40 \times 200 S = 780 S + 8000 S = 8{,}780 \cdot S$ shots ($12.2\times$ overhead).
   - Full Gram shot cost: $\binom{240}{2} S = 28{,}680 \cdot S$ shots ($39.8\times$ overhead).

---

## 5. Spectral Clipping Observation: Test-Train Kernel Block
- **Observation:** In `scripts/run_t5_noise.py` (lines 190–217), when `clip_psd=True`:
  - Eigenvalue thresholding (`fidelity_clip_psd`) is applied exclusively to square training Gram matrices: the inner CV training fold blocks `K_fold_tr` (line 193) and the final training Gram matrix `K_fit_tr` (line 214).
  - The rectangular $N_{\text{te}} \times N_{\text{tr}}$ test-train kernel block `K_te` (and the validation fold block `K_fold_val`) is passed to `SVR.predict()` completely unrepaired and unclipped.

---

## 6. Metrics to Record
- **Execution Runtime:** [Record seconds]
- **Peak Memory Footprint:** [Record MB]

---

## 7. Known Limitations
- The simulated destructive swap test assumes independent binomial outcomes per Gram entry, which neglects multi-entry covariance present when estimating state overlaps with a shared state preparation.
- Idealized per-qubit local depolarizing channel does not model cross-talk or two-qubit entangling gate noise.

---

## 8. Results
*(Left empty for Gate-0 execution recording)*

```text

```
