# Stage 5 Integration Blueprint: Manuscript Architecture and Revision Plan
**Workspace:** `D:\quantum-kernel-tfim-benchmarks`  
**Package:** `docs/stage4/readiness_20261023_180339Z/`  
**Classification:** Pre-integration specification; zero modifications to `paper/` applied.

---

## 1. Current Manuscript State vs Proposed Section Structure

The current manuscript (`paper/main.tex`) comprises a polished 4-page IEEEtran conference format (commit `ea42c3a`). It incorporates Tasks 1, 2, 3, and 5, but completely lacks Stage 2 (Equal-Total-Budget) and Stage 3 (Task 6 OOD Generalization). Furthermore, items M1–M7 and open issues R1–R3 remain unresolved in the tracked text.

### Proposed Section Restructuring for Stage 5:
```
Current Structure (paper/main.tex)              Proposed Structure (Stage 5 Target)
-------------------------------------          -------------------------------------
I. Introduction                                I. Introduction (resolve M3 keywords)
II. Problem Formulation & Architectures        II. Problem Formulation & Architectures
                                                  - Clarify M2: E2(raw) == PQK-2nn rep
                                                  - Clarify M5: Exact Z_2 parity logic
III. Empirical Results                         III. Empirical Results
    A. Task 1: Half-Chain Entropy Regression      A. Task 1 (qualify M1: <= 0.011 bound)
    B. Task 2: Contained vs Non-Contained         B. Task 2: Contained vs Non-Contained
    C. Task 3: Absence of Concentration           C. Task 3: Absence of Concentration
    D. Noise and Measurement Shot Budgets         D. Measurement Shot Overhead & Depolarizing
                                                     (verify M6 numbers; note R3 PSD clip)
                                                  E. Equal-Total-Budget Crossover Analysis
                                                     (NEW: Incorporate Stage 2 Claim C8)
                                                  F. Controlled Out-of-Distribution Phase
                                                     Shift Generalization (NEW: Claim C9)
IV. Limitations & Threats to Validity          IV. Limitations & Threats to Validity
V. What This Study Does NOT Show               V. What This Study Does NOT Show (Negative rules)
VI. Conclusion & Reproducibility Statement     VI. Conclusion & Reproducibility Statement
```

---

## 2. Separation of Scientific Claims and Evidence Types

To ensure methodological clarity, Stage 5 text must strictly separate five categories of findings:
1. **Equal-Budget In-Distribution Experiment (Stage 2):** Evaluates finite-shot tradeoffs between state evaluations ($m=240$) and Gram evaluations ($N(N-1)/2$). Finding: No crossover up to $B_{\text{tot}} = 10^5$.
2. **Noiseless OOD Generalization Experiment (Stage 3):** Evaluates extrapolation across a quantum phase transition ($g \in [0.2, 0.8] \to [1.2, 1.8]$). Finding: FQ outperforms PQK-2nn in 16/20 seeds ($W=21.0, p=8.51 \times 10^{-4}$).
3. **Mathematical Derivations:** Analytical proof that in the $Z_2$-even ground-state sector, single-site $\langle Z_i \rangle \equiv 0$, rendering Basis $Z$ shots in PQK-1 redundant (Issue R2).
4. **Numerical Identity Validation:** Empirical proof that $E_2(\text{raw})$ and $PQK\text{-2nn}$ consume identical feature representations ($B == C$, max diff $0.00 \times 10^0$; Issue R1 / Item M2).
5. **Retrospective Diagnostic Analyses:** Labeling all post-hoc audits and reconciliations explicitly as *exploratory retrospective checks*; never stating "pre-declared" or "pre-registered".

---

## 3. Human Approval Gates Required Before Editing `paper/main.tex`

Under no circumstances should `paper/main.tex` be modified until the following three gates are satisfied:

| Gate | Requirement | Status | Blocking? |
| :---: | :--- | :---: | :---: |
| **Gate 1** | Signed independent review block in `reports/CONTRIBUTOR_REVIEW.md` | PENDING | **YES** |
| **Gate 2** | Formal author approval of empirical SEs ($0.0602 \pm 0.0085$, $-0.1248 \pm 0.0334$) | PENDING | **YES** |
| **Gate 3** | Venue selection and page budget expansion decision (4 pages vs journal) | PENDING | **YES** |

---

## 4. Build and Visual-Inspection Verification Plan

Once Stage 5 modifications are authorized:
1. **Compilation Check:**
   ```powershell
   cd paper
   pdflatex -interaction=nonstopmode main.tex
   bibtex main
   pdflatex -interaction=nonstopmode main.tex
   pdflatex -interaction=nonstopmode main.tex
   ```
   *Requirement:* Exit code 0; zero undefined references (`LaTeX Warning: Reference ... undefined`); zero missing citations.
2. **Visual Layout Checks:**
   - Float placement: ensure Table I, Table II, and figures do not push text past section headers.
   - Column balance: verify column height parity on the final page.
   - Caption precision: all figure and table captions must report exact metric names, sample sizes ($N$), and statistical confidence types (bootstrap CI vs empirical SE).
