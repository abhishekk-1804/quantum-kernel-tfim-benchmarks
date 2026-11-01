# Stage 5 Integration Git Diff Report
Timestamp: 20261024_002208Z

`diff
diff --git a/paper/main.tex b/paper/main.tex
index 236e105..2cd68f1 100644
--- a/paper/main.tex
+++ b/paper/main.tex
@@ -30,17 +30,18 @@ and matched classical correlator baselines for predicting ground-state
 properties of quantum spin chains. On 1D TFIM and 2D $J_1$--$J_2$ lattices
 up to $n\le 14$ spins, ground states are obtained via exact numerical
 diagonalization, isolating representation geometry from circuit hardware
-noise. In a pre-declared statistical protocol across 20 fixed seeds,
-nearest-neighbor projected kernels (PQK-2nn) and classical two-body
-correlator features (E-raw) match full fidelity kernels to
-$\Delta R^2\le 0.011$ while requiring $12.2\times$ to $39.8\times$ fewer
-measurement shots. Under simulated destructive swap tests, raw FQ Gram
-matrices become non-positive semidefinite across 100\% of seeds, requiring
-eigenvalue clipping. Hyperparameter-retuned models show resilience to local
-depolarizing channels, while unmitigated models exhibit predictable
-$(1-p)^2$ attenuation. Physical correlator baselines match quantum kernel
-sample efficiency in equilibrium spin ground states, with zero claims of
-quantum advantage.
+noise. In a pre-declared statistical protocol across 20 fixed seeds for Task~1
+half-chain entropy regression ($N_{\mathrm{tr}}=160$), nearest-neighbor projected
+kernels (PQK-2nn) and classical two-body correlator features (E-raw) track
+full fidelity kernels within $-0.0012$ to $+0.0032$ mean $R^2$, while requiring
+$12.2\times$ to $39.8\times$ fewer measurement shots. Rankings vary across tasks
+and sample sizes. Under simulated destructive swap tests, raw FQ Gram matrices
+become non-positive semidefinite across 100\% of seeds, requiring eigenvalue
+clipping. In exploratory equal-total-budget evaluations, feature models maintain
+higher observed sample efficiency, while under severe out-of-distribution
+phase-shift tests on noiseless statevectors, fidelity kernels achieve lower mean
+absolute error. Physical correlator baselines match quantum kernel sample efficiency
+in equilibrium spin ground states, with zero claims of quantum advantage.
 \end{abstract}
 
 \begin{IEEEkeywords}
@@ -60,9 +61,11 @@ $k_{\mathrm{PQK\text{-}1}}(\psi,\phi)=\exp(-\tfrac{\gamma}{2}\sum_i
 (\langle X_i\rangle_\psi-\langle X_i\rangle_\phi)^2)$ proving that PQK-1
 is identically an RBF kernel on single-site magnetization (Sec.~II-B);
 (ii) a pre-declared, 20-seed Wilcoxon protocol on exact TFIM and
-$J_1$--$J_2$ ground states ($n\le 14$) showing that PQK-2nn and classical
-two-body correlators match FQ to $\Delta R^2\le 0.011$
-(Table~\ref{tab:confirmatory_stats}); and (iii) a $12.2\times$--$39.8\times$ FQ
+$J_1$--$J_2$ ground states ($n\le 14$) demonstrating that for Task~1
+half-chain block entropy regression at $N_{\mathrm{tr}}=160$, PQK-2nn
+and classical two-body correlators match FQ within $-0.0012$ to $+0.0032$
+mean $R^2$ (Table~\ref{tab:confirmatory_stats}), with relative rankings
+varying across tasks and sample sizes; and (iii) a $12.2\times$--$39.8\times$ FQ
 shot-budget overhead with non-PSD Gram matrices in 20/20 finite-shot
 seeds requiring spectral clipping (Fig.~\ref{fig:shots}).
 
@@ -97,7 +100,7 @@ k_{\text{PQK-1}}(\psi, \phi) = \exp\left( -\frac{\gamma}{2} \sum_{i=1}^n (\langl
 \end{equation}
 proving that PQK-1 is identically an RBF kernel on single-site magnetization $\langle X_i \rangle$ with effective bandwidth $\gamma' = \gamma/2$.
 
-Similarly, the 2-body nearest-neighbor projected kernel PQK-2nn evaluates 2-qubit reduced density matrices over graph edges $\mathcal{E}$. Due to parity constraints, the 2-body reduced states decompose into identity, local $X_i$, and two-body components $X_i X_j$, $Y_i Y_j$, and $Z_i Z_j$. The resulting kernel is identically an RBF kernel on nearest-neighbor Pauli expectations with $\gamma' = \gamma/4$.
+Similarly, the 2-body nearest-neighbor projected kernel PQK-2nn evaluates 2-qubit reduced density matrices over graph edges $\mathcal{E}$. Due to $\mathbb{Z}_2$ parity symmetry, the 2-body reduced states decompose into identity, local $X_i$, and two-body components $X_i X_j$, $Y_i Y_j$, and $Z_i Z_j$. The squared Frobenius distance between reduced density matrices algebraically satisfies $\|\rho_{ij}(\psi) - \rho_{ij}(\phi)\|_F^2 = \frac{1}{4}\sum_{O \in \{X_i, X_j, X_i X_j, Y_i Y_j, Z_i Z_j\}} (\langle O \rangle_\psi - \langle O \rangle_\phi)^2$. Consequently, PQK-2nn is algebraically identical to a classical RBF kernel on nearest-neighbor Pauli expectations with bandwidth scaled by $1/4$. When identical normalizers are used (e.g., $4n=32$ for $n=8$), the pairwise squared distance matrices match to machine precision ($|D^2_{\mathrm{RDM}} - D^2_{\mathrm{Pauli}}| \le 1.33 \times 10^{-15}$). Any minor divergence observed in historical heuristic hyperparameter sweeps between PQK-2nn and E2 (raw) is entirely an artifact of differing grid normalizers ($c/32$ for $4n$ vs $c/35$ for $5(n-1)=35$) rather than distinct physical representation geometry~\cite{Canatar2023bandwidth}.
 
 We compare these quantum kernels against classical linear and non-linear correlator baselines:
 \begin{itemize}
@@ -136,7 +139,7 @@ Table~\ref{tab:confirmatory_stats} reports confirmatory paired comparisons, whil
 Four primary empirical findings emerge:
 \begin{enumerate}
     \item \textbf{PQK Spatial Dimension Hierarchy (Claim C1):} PQK-2nn consistently outperforms PQK-1 across all sample sizes $N_{\text{tr}} \in [10, 160]$. At $N_{\text{tr}}=10$, PQK-2nn exceeds PQK-1 by $\Delta R^2 = 0.1044$ ($p_{\text{holm}} = 0.0186$), narrowing to $\Delta R^2 = 0.0414$ at $N_{\text{tr}}=160$ ($p_{\text{holm}} = 1.53 \times 10^{-5}$). The performance gap ranges from $0.0414$ to $0.1044$ in mean $R^2$, demonstrating that 2-body spatial entanglement information is essential for predicting block entropy.
-    \item \textbf{FQ vs Classical Correlator Ordering (Claim C2):} At $N_{\text{tr}}=40$, the performance hierarchy is $\text{FQ} > \text{E (raw)} > \text{PQK-2nn}$, with FQ achieving mean $R^2 = 0.9902$ versus $0.9872$ for E (raw) and $0.9789$ for PQK-2nn. At $N_{\text{tr}}=160$, the hierarchy reverses to $\text{E (raw)} > \text{FQ} > \text{PQK-2nn}$, with E (raw) reaching $0.9987$ versus $0.9975$ for FQ. All differences between top performers remain small ($\le 0.011$ $R^2$), and the relative ordering is unstable across sample sizes.
+    \item \textbf{FQ vs Classical Correlator Ordering (Claim C2):} At $N_{\text{tr}}=40$, the performance hierarchy is $\text{FQ} > \text{E (raw)} > \text{PQK-2nn}$, with FQ achieving mean $R^2 = 0.9902$ versus $0.9872$ for E (raw) and $0.9789$ for PQK-2nn. At $N_{\text{tr}}=160$, the hierarchy reverses to $\text{E (raw)} > \text{FQ} > \text{PQK-2nn}$, with E (raw) reaching $0.9987$ versus $0.9975$ for FQ. For half-chain entropy at $N_{\mathrm{tr}}=160$, observed mean $R^2$ differences were $-0.0012$ for FQ $-$ E(raw) and $+0.0032$ for FQ $-$ PQK-2nn (Table~\ref{tab:t1_r2}), demonstrating near-parity among top performers, while relative ranking varies across tasks and sample sizes.
     \item \textbf{Hyperparameter Sensitivity (Claim C7):} SVR insensitive band tuning ($\epsilon \in \{0.001, \dots, 0.1\}$) altered test $R^2$ by up to $+0.06$ relative to fixed defaults. At small training sizes ($N_{\text{tr}}=10$), 3-fold inner cross-validation exhibited small-sample overfitting, frequently pegging hyperparameters to search grid boundaries (Table~\ref{tab:grid_boundaries}).
 \end{enumerate}
 
@@ -180,6 +183,24 @@ Under an idealized per-qubit local depolarizing proxy $\mathcal{E}_k(\rho) = (1-
 
 \input{tables/tab4_grid_boundaries.tex}
 
+\subsection{Equal-Total-Budget Measurement Scaling}
+\label{sec:equal_budget}
+To assess realistic resource trade-offs on quantum hardware, we evaluate model sample efficiency under equal total measurement shot budgets $B_{\mathrm{tot}} \in [10^4, 10^7]$ ($N_{\mathrm{tr}}=40$, $N_{\mathrm{te}}=200$, 20 seeds) on 1D TFIM ground states. Because fidelity kernels and projected kernels require fundamentally distinct measurement routines, direct comparison at fixed shots per circuit can obscure experimental cost. Feature models (PQK-2nn) measure $M$ local Pauli expectations per state, allocating $S_{\mathrm{feat}} = B_{\mathrm{tot}} / (M \cdot N_{\mathrm{tr}})$ shots per observable. In contrast, fidelity kernels require pairwise swap tests on $N_{\mathrm{tr}}(N_{\mathrm{tr}}-1)/2$ training pairs, allocating $S_{\mathrm{swap}} = B_{\mathrm{tot}} / (N_{\mathrm{tr}}(N_{\mathrm{tr}}-1)/2)$ shots per kernel entry (train-only mode).
+
+Table~\ref{tab:equal_budget} presents the empirical scaling results. At low budgets $B_{\mathrm{tot}} \le 30{,}000$, FQ circuits are excluded under the study's minimum-shot protocol policy ($S_{\mathrm{swap}} < 10$), where swap-test sampling yields fewer than 10 shots per entry. Across the operational scaling regime $B_{\mathrm{tot}} \in [10^5, 10^7]$, PQK-2nn consistently achieves higher observed sample efficiency than FQ. At $B_{\mathrm{tot}}=10^6$, PQK-2nn obtains mean $R^2 = 0.9575 \pm 0.0026$ compared to $0.8288 \pm 0.0067$ for FQ (paired $\Delta R^2 = -0.1287 \pm 0.0067$). At $B_{\mathrm{tot}}=10^7$, PQK-2nn attains $0.9753 \pm 0.0024$ versus $0.8828 \pm 0.0130$ for FQ ($\Delta R^2 = -0.0924 \pm 0.0126$). These results demonstrate that when total measurement expenditure is constrained, feature-based quantum representations provide substantially higher prediction accuracy per shot than full-state swap tests. Because prospective protocol timing was not recorded in the initial pre-registration manifest, this evaluation is explicitly classified as exploratory.
+
+\input{tables/tab_equal_budget.tex}
+
+\subsection{Controlled Out-of-Distribution Phase-Shift Generalization}
+\label{sec:ood}
+We further evaluate model generalization under an out-of-distribution (OOD) physical distribution shift across the transverse-field Ising phase boundary ($n=8$, $N_{\mathrm{tr}}=40$, $N_{\mathrm{te}}=100$, 20 seeds). Training ensembles are drawn exclusively from the paramagnetic regime ($h_i \in [0.8, 1.5]$), while test ensembles are drawn from the ferromagnetic regime ($h_i \in [0.2, 0.7]$).
+
+Due to the fundamental qualitative shift in ground-state entanglement structure and the accompanying shift in mean target values between phases, all evaluated models yield negative test coefficient of determination values ($R^2 < 0$), rendering $R^2$ uninformative for discriminating model performance. We therefore assess generalization using Mean Absolute Error (MAE), summarized in Table~\ref{tab:ood}. Full fidelity kernels (FQ) achieve a mean OOD MAE of $0.0602 \pm 0.0085$, compared to $0.1850 \pm 0.0294$ for PQK-2nn, resulting in a mean paired difference of $\Delta\mathrm{MAE} = -0.1248 \pm 0.0334$. A retrospective paired Wilcoxon signed-rank test on the OOD MAE difference yields $W=21.0$, raw $p=8.51\times 10^{-4}$ (Holm-adjusted $p_{\mathrm{Holm}}=8.51\times 10^{-4}$ across the pre-declared three-comparison family including Train-Mean and Train-Median baselines), with FQ achieving lower MAE in 16 of 20 seeds.
+
+To confirm that models extract genuine inductive physical signal rather than trivial constant predictions, we conducted an intercept-only baseline ablation. Comparing full FQ against the train-mean baseline confirms that FQ reduces prediction error by $-0.4014 \pm 0.0156$ MAE across 20/20 seeds ($W=0.0, p=1.91\times 10^{-6}$). Linear Ridge regression on two-body observables is reported for descriptive calibration ($0.1345 \pm 0.0136$), without confirmatory hypothesis testing. Crucially, this OOD evaluation was performed on exact, noiseless statevectors; whether the observed fidelity-kernel extrapolation advantage survives finite measurement shot sampling or physical open-system decoherence channels remains an open question for future experimental work. This benchmark is classified as exploratory.
+
+\input{tables/tab_ood.tex}
+
 \section{Limitations \& Threats to Validity}
 Several boundaries constrain our conclusions:
 \begin{enumerate}
@@ -188,6 +209,8 @@ Several boundaries constrain our conclusions:
     \item \textbf{Noise Proxies:} Depolarizing noise was modeled via per-qubit local quantum channels rather than noisy pulse-level hardware simulations.
     \item \textbf{Sample Size Constraints:} At $N_{\text{tr}}=10$, inner 3-fold cross-validation suffers from high variance, occasionally selecting boundary hyperparameters.
     \item \textbf{Ensemble Scope:} Benchmark evaluation is based on 20 shared random train/test splits.
+    \item \textbf{Exploratory Protocol Status:} The equal-total-budget (Stage~2) and out-of-distribution phase-shift (Stage~3) evaluations were conducted retrospectively; their prospective protocol timings were not established in the initial pre-registration manifest, and they are classified as exploratory.
+    \item \textbf{Idealized Statevectors in OOD Shift:} The OOD phase-shift benchmark evaluated exact noiseless statevectors. It does not establish whether FQ's MAE advantage persists under finite measurement shot sampling or open-system noise.
 \end{enumerate}
 
 \section{What This Study Does NOT Show}
@@ -196,6 +219,8 @@ To prevent over-generalization, we explicitly delineate the negative scope of th
     \item This study does \textit{not} show that classical correlators match quantum kernels on non-equilibrium quantum dynamics or chaotic time evolution.
     \item It does \textit{not} rule out quantum advantages for high-dimensional 2D frustrated spin liquids or topological states with long-range non-local order.
     \item It does \textit{not} evaluate synthetic or cryptographically hard quantum circuit data specifically engineered to defeat classical polynomial-time estimators.
+    \item It does \textit{not} show that fidelity quantum kernels outperform feature models under realistic finite measurement budgets; rather, under equal total shot budgets $B_{\mathrm{tot}} \le 10^7$, feature models achieve superior sample efficiency.
+    \item It does \textit{not} demonstrate quantum advantage in any tested regime.
 \end{itemize}
 
 \section{Conclusion \& Reproducibility Statement}
diff --git a/paper/references.bib b/paper/references.bib
index d79e0f2..164e331 100644
--- a/paper/references.bib
+++ b/paper/references.bib
@@ -55,3 +55,25 @@
   publisher = {American Physical Society},
   doi       = {10.1103/PhysRevA.106.042407}
 }
+
+@article{Shaydulin2022importance,
+  author    = {Shaydulin, Ruslan and Wild, Stefan M.},
+  title     = {Importance of kernel bandwidth in quantum machine learning},
+  journal   = {Phys. Rev. A},
+  volume    = {106},
+  issue     = {4},
+  pages     = {042407},
+  year      = {2022},
+  publisher = {American Physical Society},
+  doi       = {10.1103/PhysRevA.106.042407}
+}
+
+@article{Canatar2023bandwidth,
+  author    = {Canatar, Abdulkadir and Peters, Evan and Pehlevan, Cengiz and Wild, Stefan M. and Shaydulin, Ruslan},
+  title     = {Bandwidth Enables Generalization in Quantum Kernel Models},
+  journal   = {Transactions on Machine Learning Research},
+  year      = {2023},
+  issn      = {2835-8856},
+  url       = {https://openreview.net/forum?id=sfgJuq7x8K}
+}
+

`
