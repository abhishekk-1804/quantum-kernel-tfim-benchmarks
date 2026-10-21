# Phase 2a / Phase 2a.1 Technical Notes & Audit Findings

## 1. Rationale for Task 4 (Frustrated 2D Lattice) Redesign

### Limitations of Phase 2a Formulation (v1)
In the initial Task 4 formulation (`results/archive_v1/t4_frustrated.csv`):
- $J_2 \in \{-0.25, -0.5, -0.75\}$ was held fixed while only the transverse field $g \sim U[0.2, 3.0]$ varied on a $2 \times 4$ open lattice.
- **T4a (Classification):** The target was defined as $\operatorname{argmax}_{q} S(q)$ over the 2D Brillouin zone. Across all seeds and samples, $S(q)$ maximized strictly at the Neel wavevector $(\pi, \pi)$ in 100.0% of generated states. Because only a single class existed, binary classifiers (SVC, RidgeClassifier) could not be trained, and the task degenerated into a trivial majority-class prediction.
- **T4b (Regression):** The target was half-chain entropy across the row cut. For fixed $J_2$, varying $g$ in $[0.2, 3.0]$ yielded saturated entanglement entropy with negligible dynamic range.

### Redesigned Formulation (v2)
- **Ensemble:** $J_1 = -1.0$, with both $J_2 \sim U[-1.0, -0.1]$ and $g \sim U[0.2, 3.0]$ sampled randomly per state.
- **Lattices:** Evaluated on both $2 \times 4$ ($n=8$) and $3 \times 4$ ($n=12$) open lattices.
- **T4a (Classification - "contained"):** Predicts the physical phase competition between Neel antiferromagnetic order and collinear stripe order:
  $$\text{label} = \operatorname{sign}(S(\pi, \pi) - S(\pi, 0))$$
  States falling within $|S(\pi, \pi) - S(\pi, 0)| < 10^{-3}$ are dropped to avoid boundary ambiguity.
  - *Pilot Gate (1000 states):*
    - $2 \times 4$ ($n=8$): 0 dropped (0.00%), Neel 594 (59.40%), Stripe 406 (40.60%).
    - $3 \times 4$ ($n=12$): 0 dropped (0.00%), Neel 591 (59.10%), Stripe 409 (40.90%).
    Both lattices demonstrated a balanced binary distribution well above the 15% threshold.
- **T4b (Regression - "not_contained"):** Predicts half-cut entropy across the row bipartition ($n_A = n // 2$). With randomized $J_2$ and $g$, entropy spans a wide physical range across frustrated ground states.
- **Training partition & test set:** $N_{\text{train}} \in \{10, 20, 40, 80\}$, evaluated on 200 fixed test states per (lattice, seed), across 20 independent seeds.

---

## 2. Hyperparameter Grid Boundary Findings (`results/grid_boundary.csv`)

Hyperparameter grids used during 3-fold inner cross-validation:
- SVM regularization: $C \in \{0.1, 1.0, 10.0, 100.0\}$
- RBF bandwidth factor: $c \in \{0.1, 0.3, 1.0, 3.0, 10.0\}$
- Ridge regularization: $\alpha \in \{10^{-4}, 10^{-2}, 1.0, 100.0\}$

### Key Boundary Hit Patterns
1. **Upper Bound Selection for Regularization $C$:**
   - In Task 1 (Entropy) and Task 2 (Correlators), SVM models (PQK-1, PQK-2nn, FQ, and E) selected $C=100.0$ in 70% to 100% of seeds as training size $N_{\text{train}}$ increased to 80 and 160.
   - This indicates high target signal-to-noise ratio in the feature space, where strong fitting with minimal margin slack improves validation performance.
2. **Lower Bound Selection for Bandwidth Factor $c$ in Standardized Features:**
   - In E (std) across T1 and T2, the chosen bandwidth factor $c$ consistently clustered at $c=0.1$ (the lower grid edge) in 80% to 100% of seeds.
   - Standardization of high-dimensional correlators ($d=36$ for $n=8$) reduces the variance of pairwise Euclidean distances, which effectively increases the distance metric; consequently, smaller $\gamma = c/d$ (i.e. $c=0.1$) is selected by CV to maintain Gaussian kernel resolution.
3. **Ridge Regularization $\alpha$:**
   - Ridge baseline F selected the upper boundary $\alpha=100.0$ predominantly at small $N_{\text{train}} = 10$ to prevent severe overfitting on 36 features, but settled on internal grid values ($\alpha \in \{1.0, 10^{-2}\}$) at larger sample sizes.
4. **Audit Compliance:**
   - All edge selection fractions are quantified per (task, target, model, variant, $N_{\text{train}}$) in `results/grid_boundary.csv`.
   - Per Phase 2a.1 instructions, no automatic reruns of T1/T2 were conducted. Future grid extensions may expand $C$ up to $1000$ and $c$ down to $0.01$.
