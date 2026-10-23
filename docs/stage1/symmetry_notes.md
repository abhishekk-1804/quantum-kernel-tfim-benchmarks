# S1.6 Vanishing Operator Families & Symmetry Checklist

This document is a formal mathematical checklist recording the mechanisms by which operator families vanish in the ground states of the Transverse-Field Ising Model (TFIM) and frustrated lattice Hamiltonians.

## Symmetry Mechanisms
- **Parity Symmetry ($P = \bigotimes_{i=0}^{n-1} X_i$):**
  $P$ commutes with $H$. The ground state satisfies $P |\psi\rangle = +|\psi\rangle$ (even sector).
  An operator $O$ with odd parity under conjugation $\{O, P\} = 0$ satisfies:
  $$\langle \psi | O | \psi \rangle = \langle \psi | P^\dagger O P | \psi \rangle = -\langle \psi | O | \psi \rangle = 0.$$
- **Hamiltonian & Wavefunction Reality ($\psi \in \mathbb{R}^{2^n}$):**
  In the computational $Z$-basis, $X_i$ and $Z_i$ matrices are purely real symmetric, making $H$ real symmetric, so $|\psi\rangle$ is strictly real.
  $Y_i$ is purely imaginary skew-Hermitian. For any operator $O = i A$ where $A$ is real skew-symmetric ($A^T = -A$), its expectation on any real state satisfies:
  $$\langle \psi | O | \psi \rangle = i \psi^T A \psi = 0.$$

---

## Operator Family Checklist

| Operator Family | Algebraic Form | Parity Under $P = \bigotimes X$ | Matrix Elements in $Z$-basis | Vanishing Mechanism | Observed Max Magnitude (Disordered TFIM n=6) | Observed Max Magnitude (Frustrated 2x4 n=8) | Status |
| :--- | :--- | :---: | :---: | :--- | :---: | :---: | :---: |
| $\langle Z_i \rangle$ | Single-site $Z$ | Odd ($X Z X = -Z$) | Real diagonal | Parity $P$ | $2.22 \times 10^{-16}$ | $2.22 \times 10^{-16}$ | VERIFIED |
| $\langle Y_i \rangle$ | Single-site $Y$ | Odd ($X Y X = -Y$) | Purely imaginary skew-symmetric | Parity $P$ & State Reality | $1.41 \times 10^{-17}$ | $1.53 \times 10^{-17}$ | VERIFIED |
| $\langle X_i Z_j \rangle$ ($i \neq j$) | 2-body cross $X Z$ | Odd ($P (X_i Z_j) P = - X_i Z_j$) | Real off-diagonal | Parity $P$ | $1.39 \times 10^{-16}$ | $1.94 \times 10^{-16}$ | VERIFIED |
| $\langle Y_i Z_j \rangle$ ($i \neq j$) | 2-body cross $Y Z$ | Even ($P (Y_i Z_j) P = + Y_i Z_j$) | Purely imaginary skew-symmetric | State Reality ($\psi \in \mathbb{R}^{2^n}$) | $4.30 \times 10^{-17}$ | $4.03 \times 10^{-17}$ | VERIFIED |
| $\langle Z_i Y_j \rangle$ ($i \neq j$) | 2-body cross $Z Y$ | Even ($P (Z_i Y_j) P = + Z_i Y_j$) | Purely imaginary skew-symmetric | State Reality ($\psi \in \mathbb{R}^{2^n}$) | $4.30 \times 10^{-17}$ | $4.03 \times 10^{-17}$ | VERIFIED |
| $\langle X_i \rangle$ | Single-site $X$ | Even ($X X X = +X$) | Real off-diagonal | Non-vanishing (Field response) | Non-zero | Non-zero | NON-VANISHING |
| $\langle Z_i Z_j \rangle$ | 2-body $Z Z$ | Even ($P (Z_i Z_j) P = + Z_i Z_j$) | Real diagonal | Non-vanishing (Two-point correlation) | Non-zero | Non-zero | NON-VANISHING |
| $\langle X_i X_j \rangle$ | 2-body $X X$ | Even ($P (X_i X_j) P = + X_i X_j$) | Real off-diagonal | Non-vanishing (Two-point correlation) | Non-zero | Non-zero | NON-VANISHING |
| $\langle Y_i Y_j \rangle$ | 2-body $Y Y$ | Even ($P (Y_i Y_j) P = + Y_i Y_j$) | Real symmetric | Non-vanishing (Two-point correlation) | Non-zero | Non-zero | NON-VANISHING |

---

## Negative Controls Checklist

| Control Test | State Modification | Expected Effect | Measured Observable Value | Status |
| :--- | :--- | :--- | :---: | :---: |
| **Parity Breaking** | Longitudinal field $h \sum_i Z_i$ ($h = 0.05$) in full space | Breaks parity symmetry $\to \langle Z_i \rangle \neq 0$ | $\max |\langle Z_i \rangle| = 0.5252$ | VERIFIED |
| **Global Complex Phase** | $|\psi'\rangle = e^{i\theta} |\psi\rangle$ ($\theta = \pi/4$) | Global phase invariance $\to \langle Y_0 Z_1 \rangle = 0$ | $|\langle Y_0 Z_1 \rangle| = 9.69 \times 10^{-18}$ | VERIFIED |
| **Local Complex Rotation** | $|\psi'\rangle = \frac{e^{-i t X_0} |\psi\rangle}{\|e^{-i t X_0} |\psi\rangle\|}$ ($t = 0.5$) | Generates relative complex phase $\to \langle Y_0 Z_1 \rangle \neq 0$ | $|\langle Y_0 Z_1 \rangle| = 0.4164$ | VERIFIED |
