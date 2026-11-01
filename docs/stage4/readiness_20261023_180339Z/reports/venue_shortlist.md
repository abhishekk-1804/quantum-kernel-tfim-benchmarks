# Stage 4 Venue Shortlist & Strategic Assessment
**Workspace:** `D:\quantum-kernel-tfim-benchmarks`  
**Package:** `docs/stage4/readiness_20261023_180339Z/`  
**Classification:** Strategic venue evaluation based on verified publisher policies.

---

## 1. Comparative Venue Profile Matrix

| Feature | IEEE TQE | IOP QST | Phys. Rev. A | Phys. Rev. Research |
| :--- | :---: | :---: | :---: | :---: |
| **Publisher** | IEEE | IOP Publishing | APS | APS |
| **Model** | Gold Open Access | Hybrid | Hybrid | Gold Open Access |
| **Standard APC** | **$1,995 USD** | $4,295 USD (or $0) | $2,910 USD (or $0) | **$2,910 USD** |
| **Free Route?** | No ($1,995 APC) | **YES ($0 subscription)** | **YES ($0 subscription)** | No ($2,910 APC) |
| **LaTeX Style** | `IEEEtran.cls` | `iopart.cls` | `revtex4-2.cls` | `revtex4-2.cls` |
| **Current Manuscript Fit** | **Direct (`IEEEtran`)** | Needs porting | Needs porting | Needs porting |
| **Page Limit** | No rigid limit | No rigid limit | No rigid limit | No rigid limit |
| **Turnaround** | Moderate (~6-8 wks) | Fast-Moderate | Moderate (~8-12 wks) | Moderate (~8-12 wks) |
| **Focus** | Software/Benchmarks | High-Impact Tech | Foundational Physics | Interdisciplinary |

---

## 2. In-Depth Strategic Analysis

### 2.1 Option 1 (Primary Engineering Track): IEEE Transactions on Quantum Engineering (TQE)
- **Strengths:** 
  * The current manuscript (`paper/main.tex`) is already formatted in `IEEEtran.cls` (IEEE transactions format). Minimal formatting friction.
  * TQE specifically emphasizes quantum software, reproducible empirical benchmarks, error mitigation protocols, and measurement resource trade-offs.
  * Lowest Gold Open Access APC among dedicated quantum venues ($1,995 USD, with IEEE member discounts bringing it to ~$1,596 - $1,895 USD).
  * No strict page limit allows thorough reporting of both Stage 2 equal-budget analyses and Stage 3 OOD generalization tables.
- **Trade-offs:** 
  * Mandatory APC (no traditional subscription $0 route). Requires open-access funding allocation.

### 2.2 Option 2 (Foundational Physics Track, Zero-Cost Route): Physical Review A (PRA)
- **Strengths:**
  * PRA is the historical home of rigorous quantum information theory and TFIM many-body Hamiltonian benchmarking (e.g., Shaydulin & Wild 2022).
  * **Free Subscription Option ($0 USD):** If open-access grant funding is unavailable, PRA allows traditional subscription publishing with zero author fees.
  * Highly respected among quantum physicists for foundational soundness.
- **Trade-offs:**
  * Requires porting the manuscript from `IEEEtran.cls` to `revtex4-2.cls`.
  * Reviewers may place higher emphasis on analytical proofs rather than empirical software benchmarking suites.

### 2.3 Option 3 (Broad Applied Physics Track): Physical Review Research (PRResearch)
- **Strengths:**
  * Multidisciplinary scope bridges quantum physics and machine learning engineering.
  * Uses `revtex4-2.cls`. High visibility across both physics and computer science communities.
- **Trade-offs:**
  * Mandatory Gold OA APC ($2,910 USD). Requires active institutional transformative agreement or grant budget.

### 2.4 Option 4 (High-Selectivity Applied Track): Quantum Science and Technology (QST)
- **Strengths:**
  * Very high impact factor and visibility in the quantum technology sector.
  * Offers a $0 subscription publishing route.
- **Trade-offs:**
  * Editorial board performs aggressive initial desk-screening for broad technological impact.
  * Gold OA APC is the highest in the field ($4,295 USD). Requires reformatting to `iopart.cls`.

---

## 3. Recommended Action Plan for Human Authors

1. **If Funding is Allocated for Open Access (~$2,000 USD):**  
   **Target IEEE Transactions on Quantum Engineering (TQE).** The paper is already structured and formatted for `IEEEtran`, perfectly aligns with TQE's software benchmarking scope, and incurs the lowest open-access cost ($1,995 USD).
2. **If Zero Open-Access Funding is Available ($0 USD Budget):**  
   **Target Physical Review A (PRA).** Reformat to `revtex4-2` and publish via the traditional subscription route with $0 author fees.
