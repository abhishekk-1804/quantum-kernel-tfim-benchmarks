# Claim Separation: Verification of the Two Distinct Directional Findings

## 1. Problem Statement & Conceptual Boundary

A frequent source of confusion in previous narrative summaries was conflating two entirely distinct directional comparisons:
- **Claim A (Across Models):** FQ vs PQK-2nn out-of-distribution MAE.
- **Claim B (Within FQ Model):** Full FQ predictor vs its own constant intercept-only predictor.

These two claims examine fundamentally different questions and exhibit different sign distributions. Neither implies the other, and they must never be combined into a single claim.

## 2. Granular Verification of Claim A (Across Models: FQ vs PQK-2nn)

- **Directional Finding:** FQ achieves lower MAE than PQK-2nn in **16 out of 20 seeds** (80%). In **4 seeds**, PQK-2nn achieves lower MAE.
- **Exact Positive Seeds (PQK-2nn Superior):**
  - **Seed 08:** FQ MAE = `0.070931`, PQK-2nn MAE = `0.054557` (Diff = `+0.016374`)
  - **Seed 09:** FQ MAE = `0.091870`, PQK-2nn MAE = `0.034900` (Diff = `+0.056971`)
  - **Seed 11:** FQ MAE = `0.099897`, PQK-2nn MAE = `0.056520` (Diff = `+0.043378`)
  - **Seed 16:** FQ MAE = `0.186101`, PQK-2nn MAE = `0.032773` (Diff = `+0.153329`)
- **Verdict:** Statements claiming 'FQ achieves lower error in every seed' are **FALSE** and prohibited.

## 3. Granular Verification of Claim B (Within Model: Full FQ vs Intercept-Only)

- **Directional Finding:** Full FQ achieves lower MAE than its own constant intercept in **20 out of 20 seeds** (100%).
- **Aggregate MAE:** Full FQ mean MAE is **`0.0602 ± 0.0085`** vs Intercept-only mean MAE **`0.4616 ± 0.0162`**.
- **Mean Paired Improvement:** **`-0.4014 ± 0.0156`** (improvement ranges from `-0.2152` to `-0.5497` across seeds).
- **Physical Interpretation:** The training distribution lies in the paramagnetic regime where ground-state entanglement entropy is low ($y \in [0.1, 0.7]$, mean $\approx 0.392$). The constant intercept alone ($b_{\text{physical}} \approx 0.530$) cannot reach the ferromagnetic plateau ($y \approx 0.993$). The dual-weighted kernel sum $g(x) = \sigma \sum_i \alpha_i K(x_i, x)$ provides the required positive offset ($+0.4379$), shifting predictions into the physical target domain.

## 4. Summary Matrix

| Feature | Claim A (Across Models) | Claim B (Within Model) |
|---|---|---|
| Compared Entities | FQ vs PQK-2nn | Full FQ vs Intercept FQ |
| Evaluation Split | OOD (ferromagnetic) | OOD (ferromagnetic) |
| Seed Direction Breakdown | **16 / 4** (FQ lower in 16, PQK2 lower in 4) | **20 / 0** (Full model lower in 20/20) |
| Exceptional Seeds | Seeds 8, 9, 11, 16 | None |
| Mean Paired Difference | **-0.1248 ± 0.0334** | **-0.4014 ± 0.0156** |
| Inferential Target | Relative architecture expressiveness | SVR functional attribution |
