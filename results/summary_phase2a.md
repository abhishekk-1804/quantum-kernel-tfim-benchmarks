# Phase 2a Summary Statistics (10,000 Bootstrap Resamples over Seeds)

## Task 1: Disordered TFIM Half-Chain Entropy (n=8)

| task | target | tag | n | N_train | model | variant | metric | num_seeds | mean | ci_95_lower | ci_95_upper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | half_chain_entropy | not_contained | 8 | 10 | baseline_mean | none | r2 | 20 | -0.178472 | -0.351753 | -0.0687144 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | baseline_mean | none | mae | 20 | 0.200516 | 0.193047 | 0.211704 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.784707 | 0.743563 | 0.820397 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0799256 | 0.0738768 | 0.0866178 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | PQK-2nn | none | r2 | 20 | 0.863361 | 0.826108 | 0.894258 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | PQK-2nn | none | mae | 20 | 0.0634969 | 0.0556862 | 0.0728684 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | FQ | none | r2 | 20 | 0.830324 | 0.738947 | 0.891489 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | FQ | none | mae | 20 | 0.0686184 | 0.0569414 | 0.0837628 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | E | raw | r2 | 20 | 0.835995 | 0.77331 | 0.884564 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | E | raw | mae | 20 | 0.0680462 | 0.0574142 | 0.0805911 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | E | std | r2 | 20 | 0.694955 | 0.588198 | 0.777101 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | E | std | mae | 20 | 0.0937116 | 0.080919 | 0.109582 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | F | std | r2 | 20 | 0.819151 | 0.785273 | 0.849254 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | F | std | mae | 20 | 0.0750426 | 0.0683072 | 0.0821985 |
| T1 | half_chain_entropy | sanity | 8 | 10 | E2 | raw | r2 | 20 | 0.874331 | 0.847225 | 0.897803 |
| T1 | half_chain_entropy | sanity | 8 | 10 | E2 | raw | mae | 20 | 0.0610828 | 0.0550789 | 0.067931 |
| T1 | half_chain_entropy | sanity | 8 | 10 | E_X | raw | r2 | 20 | 0.782449 | 0.745722 | 0.816134 |
| T1 | half_chain_entropy | sanity | 8 | 10 | E_X | raw | mae | 20 | 0.0809558 | 0.0743554 | 0.0881679 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | baseline_mean | none | r2 | 20 | -0.0440045 | -0.0856722 | -0.0180433 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | baseline_mean | none | mae | 20 | 0.191759 | 0.187991 | 0.195699 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.867869 | 0.849507 | 0.884061 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0627387 | 0.0590277 | 0.0668045 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | PQK-2nn | none | r2 | 20 | 0.954419 | 0.948456 | 0.959513 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | PQK-2nn | none | mae | 20 | 0.0358971 | 0.0337561 | 0.0383577 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | FQ | none | r2 | 20 | 0.961708 | 0.956229 | 0.966634 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | FQ | none | mae | 20 | 0.0336746 | 0.0314141 | 0.0360851 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | E | raw | r2 | 20 | 0.957814 | 0.949543 | 0.965563 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | E | raw | mae | 20 | 0.0348837 | 0.0314213 | 0.0384446 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | E | std | r2 | 20 | 0.908252 | 0.894132 | 0.920919 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | E | std | mae | 20 | 0.0519301 | 0.0484216 | 0.0556568 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | F | std | r2 | 20 | 0.928391 | 0.915548 | 0.939301 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | F | std | mae | 20 | 0.0454073 | 0.0415306 | 0.0495958 |
| T1 | half_chain_entropy | sanity | 8 | 20 | E2 | raw | r2 | 20 | 0.956565 | 0.951331 | 0.961308 |
| T1 | half_chain_entropy | sanity | 8 | 20 | E2 | raw | mae | 20 | 0.0350521 | 0.0330171 | 0.0372786 |
| T1 | half_chain_entropy | sanity | 8 | 20 | E_X | raw | r2 | 20 | 0.851893 | 0.833392 | 0.868849 |
| T1 | half_chain_entropy | sanity | 8 | 20 | E_X | raw | mae | 20 | 0.0659479 | 0.0628692 | 0.0691495 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | baseline_mean | none | r2 | 20 | -0.0243195 | -0.0428134 | -0.0095254 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | baseline_mean | none | mae | 20 | 0.190591 | 0.187425 | 0.193533 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.904805 | 0.894665 | 0.914502 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0529755 | 0.0503862 | 0.0556028 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | PQK-2nn | none | r2 | 20 | 0.972627 | 0.970252 | 0.975008 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | PQK-2nn | none | mae | 20 | 0.027035 | 0.0257868 | 0.0282469 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | FQ | none | r2 | 20 | 0.982621 | 0.981089 | 0.984097 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | FQ | none | mae | 20 | 0.0220876 | 0.0211799 | 0.0230251 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | E | raw | r2 | 20 | 0.981061 | 0.979101 | 0.982912 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | E | raw | mae | 20 | 0.0233035 | 0.02215 | 0.0244542 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | E | std | r2 | 20 | 0.963239 | 0.95637 | 0.96902 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | E | std | mae | 20 | 0.0327884 | 0.0305717 | 0.0351469 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | F | std | r2 | 20 | 0.972801 | 0.966496 | 0.977571 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | F | std | mae | 20 | 0.0260938 | 0.0239003 | 0.0286854 |
| T1 | half_chain_entropy | sanity | 8 | 40 | E2 | raw | r2 | 20 | 0.972194 | 0.969825 | 0.974593 |
| T1 | half_chain_entropy | sanity | 8 | 40 | E2 | raw | mae | 20 | 0.0272367 | 0.025981 | 0.0284723 |
| T1 | half_chain_entropy | sanity | 8 | 40 | E_X | raw | r2 | 20 | 0.902166 | 0.892377 | 0.910991 |
| T1 | half_chain_entropy | sanity | 8 | 40 | E_X | raw | mae | 20 | 0.0539332 | 0.0516616 | 0.0562278 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | baseline_mean | none | r2 | 20 | -0.0108176 | -0.0189806 | -0.00461302 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | baseline_mean | none | mae | 20 | 0.189851 | 0.186654 | 0.192935 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.934986 | 0.927654 | 0.941428 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0437169 | 0.0416819 | 0.0459929 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | PQK-2nn | none | r2 | 20 | 0.984356 | 0.982681 | 0.985984 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | PQK-2nn | none | mae | 20 | 0.020318 | 0.0194049 | 0.0211631 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | FQ | none | r2 | 20 | 0.988385 | 0.98724 | 0.989495 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | FQ | none | mae | 20 | 0.0181936 | 0.0174158 | 0.0189829 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | E | raw | r2 | 20 | 0.989649 | 0.988395 | 0.990772 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | E | raw | mae | 20 | 0.0173409 | 0.0165028 | 0.0182045 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | E | std | r2 | 20 | 0.982098 | 0.979788 | 0.984306 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | E | std | mae | 20 | 0.022895 | 0.0215344 | 0.0242805 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | F | std | r2 | 20 | 0.984649 | 0.983331 | 0.985948 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | F | std | mae | 20 | 0.0192275 | 0.0183292 | 0.0201516 |
| T1 | half_chain_entropy | sanity | 8 | 80 | E2 | raw | r2 | 20 | 0.984573 | 0.982877 | 0.986178 |
| T1 | half_chain_entropy | sanity | 8 | 80 | E2 | raw | mae | 20 | 0.0202179 | 0.0193301 | 0.0210471 |
| T1 | half_chain_entropy | sanity | 8 | 80 | E_X | raw | r2 | 20 | 0.936005 | 0.929369 | 0.941436 |
| T1 | half_chain_entropy | sanity | 8 | 80 | E_X | raw | mae | 20 | 0.0434159 | 0.0415107 | 0.0454141 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | baseline_mean | none | r2 | 20 | -0.00819864 | -0.0150711 | -0.00302696 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | baseline_mean | none | mae | 20 | 0.190353 | 0.186922 | 0.193719 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.955411 | 0.953438 | 0.957371 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0369671 | 0.0360345 | 0.0379038 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | PQK-2nn | none | r2 | 20 | 0.990391 | 0.989626 | 0.991122 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | PQK-2nn | none | mae | 20 | 0.0160429 | 0.015435 | 0.0166826 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | FQ | none | r2 | 20 | 0.992397 | 0.991965 | 0.992851 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | FQ | none | mae | 20 | 0.0148547 | 0.0145206 | 0.0152021 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | E | raw | r2 | 20 | 0.993258 | 0.992796 | 0.99367 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | E | raw | mae | 20 | 0.0141783 | 0.0137095 | 0.0146529 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | E | std | r2 | 20 | 0.990085 | 0.989229 | 0.990915 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | E | std | mae | 20 | 0.0170568 | 0.0162664 | 0.0178095 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | F | std | r2 | 20 | 0.98869 | 0.987807 | 0.989459 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | F | std | mae | 20 | 0.0167566 | 0.0161536 | 0.0174733 |
| T1 | half_chain_entropy | sanity | 8 | 160 | E2 | raw | r2 | 20 | 0.990285 | 0.989486 | 0.991036 |
| T1 | half_chain_entropy | sanity | 8 | 160 | E2 | raw | mae | 20 | 0.01613 | 0.0155129 | 0.0167847 |
| T1 | half_chain_entropy | sanity | 8 | 160 | E_X | raw | r2 | 20 | 0.956467 | 0.954009 | 0.958819 |
| T1 | half_chain_entropy | sanity | 8 | 160 | E_X | raw | mae | 20 | 0.0363149 | 0.0350759 | 0.0375593 |

## Task 2: Disordered TFIM Correlators (T2a Contained, T2b Not Contained, n=8)

| task | target | tag | n | N_train | model | variant | metric | num_seeds | mean | ci_95_lower | ci_95_upper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T2a | z0_zn | contained | 8 | 10 | baseline_mean | none | r2 | 20 | -0.176866 | -0.334108 | -0.0635969 |
| T2a | z0_zn | contained | 8 | 10 | baseline_mean | none | mae | 20 | 0.0742066 | 0.0681191 | 0.0813893 |
| T2a | z0_zn | contained | 8 | 10 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.407228 | 0.278863 | 0.516902 |
| T2a | z0_zn | contained | 8 | 10 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.044697 | 0.041152 | 0.0486229 |
| T2a | z0_zn | contained | 8 | 10 | PQK-2nn | none | r2 | 20 | 0.375787 | 0.251065 | 0.480355 |
| T2a | z0_zn | contained | 8 | 10 | PQK-2nn | none | mae | 20 | 0.0448767 | 0.0419328 | 0.0483206 |
| T2a | z0_zn | contained | 8 | 10 | FQ | none | r2 | 20 | 0.456537 | 0.308529 | 0.582358 |
| T2a | z0_zn | contained | 8 | 10 | FQ | none | mae | 20 | 0.0417248 | 0.0376201 | 0.0462636 |
| T2a | z0_zn | contained | 8 | 10 | E | raw | r2 | 20 | 0.577852 | 0.426106 | 0.698682 |
| T2a | z0_zn | contained | 8 | 10 | E | raw | mae | 20 | 0.0353185 | 0.0311285 | 0.0403922 |
| T2a | z0_zn | contained | 8 | 10 | E | std | r2 | 20 | 0.528747 | 0.385416 | 0.648867 |
| T2a | z0_zn | contained | 8 | 10 | E | std | mae | 20 | 0.0372801 | 0.0327622 | 0.0422619 |
| T2a | z0_zn | contained | 8 | 10 | F | std | r2 | 20 | 0.7607 | 0.70907 | 0.806769 |
| T2a | z0_zn | contained | 8 | 10 | F | std | mae | 20 | 0.0303831 | 0.0274306 | 0.0334404 |
| T2a | z0_zn | sanity | 8 | 10 | E2 | raw | r2 | 20 | 0.388075 | 0.256069 | 0.500435 |
| T2a | z0_zn | sanity | 8 | 10 | E2 | raw | mae | 20 | 0.0445032 | 0.0411458 | 0.0482161 |
| T2a | z0_zn | sanity | 8 | 10 | E_X | raw | r2 | 20 | 0.401603 | 0.269006 | 0.511885 |
| T2a | z0_zn | sanity | 8 | 10 | E_X | raw | mae | 20 | 0.0441405 | 0.0408959 | 0.0478985 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | baseline_mean | none | r2 | 20 | -0.116675 | -0.170914 | -0.068975 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | baseline_mean | none | mae | 20 | 0.090472 | 0.0866829 | 0.0948573 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.418927 | 0.219003 | 0.601778 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0595498 | 0.0498315 | 0.0696717 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | PQK-2nn | none | r2 | 20 | 0.413541 | 0.236857 | 0.578919 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | PQK-2nn | none | mae | 20 | 0.0587929 | 0.0495753 | 0.0681724 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | FQ | none | r2 | 20 | 0.587201 | 0.421845 | 0.730504 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | FQ | none | mae | 20 | 0.0485953 | 0.0400039 | 0.0584762 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | E | raw | r2 | 20 | 0.563609 | 0.392062 | 0.709548 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | E | raw | mae | 20 | 0.0502768 | 0.0417231 | 0.059923 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | E | std | r2 | 20 | 0.433441 | 0.321497 | 0.542847 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | E | std | mae | 20 | 0.0607057 | 0.05412 | 0.0674401 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | F | std | r2 | 20 | 0.596708 | 0.498474 | 0.690565 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | F | std | mae | 20 | 0.0522808 | 0.0457006 | 0.0590431 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 10 | E2 | raw | r2 | 20 | 0.408867 | 0.232315 | 0.573146 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 10 | E2 | raw | mae | 20 | 0.059157 | 0.0500436 | 0.0684906 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 10 | E_X | raw | r2 | 20 | 0.458295 | 0.269653 | 0.626488 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 10 | E_X | raw | mae | 20 | 0.056915 | 0.0477589 | 0.066592 |
| T2a | z0_zn | contained | 8 | 20 | baseline_mean | none | r2 | 20 | -0.0528071 | -0.0844546 | -0.0272839 |
| T2a | z0_zn | contained | 8 | 20 | baseline_mean | none | mae | 20 | 0.0700486 | 0.0664852 | 0.0739292 |
| T2a | z0_zn | contained | 8 | 20 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.682748 | 0.627188 | 0.733012 |
| T2a | z0_zn | contained | 8 | 20 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0326119 | 0.0300289 | 0.0353906 |
| T2a | z0_zn | contained | 8 | 20 | PQK-2nn | none | r2 | 20 | 0.630999 | 0.577004 | 0.681581 |
| T2a | z0_zn | contained | 8 | 20 | PQK-2nn | none | mae | 20 | 0.0338057 | 0.0318136 | 0.0360011 |
| T2a | z0_zn | contained | 8 | 20 | FQ | none | r2 | 20 | 0.756616 | 0.705531 | 0.798851 |
| T2a | z0_zn | contained | 8 | 20 | FQ | none | mae | 20 | 0.0276119 | 0.0255173 | 0.03007 |
| T2a | z0_zn | contained | 8 | 20 | E | raw | r2 | 20 | 0.826297 | 0.772406 | 0.870271 |
| T2a | z0_zn | contained | 8 | 20 | E | raw | mae | 20 | 0.0223252 | 0.019954 | 0.0252317 |
| T2a | z0_zn | contained | 8 | 20 | E | std | r2 | 20 | 0.813424 | 0.76708 | 0.849558 |
| T2a | z0_zn | contained | 8 | 20 | E | std | mae | 20 | 0.0233282 | 0.0210986 | 0.0261054 |
| T2a | z0_zn | contained | 8 | 20 | F | std | r2 | 20 | 0.905592 | 0.886176 | 0.924443 |
| T2a | z0_zn | contained | 8 | 20 | F | std | mae | 20 | 0.0194621 | 0.0174854 | 0.0216686 |
| T2a | z0_zn | sanity | 8 | 20 | E2 | raw | r2 | 20 | 0.642969 | 0.583369 | 0.698057 |
| T2a | z0_zn | sanity | 8 | 20 | E2 | raw | mae | 20 | 0.0335427 | 0.0313868 | 0.0358981 |
| T2a | z0_zn | sanity | 8 | 20 | E_X | raw | r2 | 20 | 0.637293 | 0.575886 | 0.694381 |
| T2a | z0_zn | sanity | 8 | 20 | E_X | raw | mae | 20 | 0.033937 | 0.0317096 | 0.0363677 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | baseline_mean | none | r2 | 20 | -0.0456779 | -0.0757247 | -0.0239571 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | baseline_mean | none | mae | 20 | 0.0875912 | 0.08475 | 0.0908486 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.79582 | 0.765441 | 0.820735 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0353556 | 0.032438 | 0.0386712 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | PQK-2nn | none | r2 | 20 | 0.835929 | 0.775442 | 0.876711 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | PQK-2nn | none | mae | 20 | 0.0299887 | 0.0264816 | 0.0347493 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | FQ | none | r2 | 20 | 0.861068 | 0.79546 | 0.898899 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | FQ | none | mae | 20 | 0.0277029 | 0.0242701 | 0.0329449 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | E | raw | r2 | 20 | 0.86596 | 0.842763 | 0.885472 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | E | raw | mae | 20 | 0.0283489 | 0.0263886 | 0.0306349 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | E | std | r2 | 20 | 0.80227 | 0.781136 | 0.822793 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | E | std | mae | 20 | 0.0350491 | 0.0327819 | 0.0373867 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | F | std | r2 | 20 | 0.826094 | 0.797371 | 0.854361 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | F | std | mae | 20 | 0.0339239 | 0.0308436 | 0.0370602 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 20 | E2 | raw | r2 | 20 | 0.835661 | 0.774686 | 0.876287 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 20 | E2 | raw | mae | 20 | 0.030222 | 0.0266181 | 0.0350647 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 20 | E_X | raw | r2 | 20 | 0.781884 | 0.757319 | 0.807354 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 20 | E_X | raw | mae | 20 | 0.0361045 | 0.0333845 | 0.038996 |
| T2a | z0_zn | contained | 8 | 40 | baseline_mean | none | r2 | 20 | -0.0278493 | -0.041996 | -0.0154354 |
| T2a | z0_zn | contained | 8 | 40 | baseline_mean | none | mae | 20 | 0.0709879 | 0.0682339 | 0.0738624 |
| T2a | z0_zn | contained | 8 | 40 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.871134 | 0.846817 | 0.892591 |
| T2a | z0_zn | contained | 8 | 40 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0215239 | 0.0201555 | 0.0230354 |
| T2a | z0_zn | contained | 8 | 40 | PQK-2nn | none | r2 | 20 | 0.831893 | 0.791326 | 0.867541 |
| T2a | z0_zn | contained | 8 | 40 | PQK-2nn | none | mae | 20 | 0.0230945 | 0.0215149 | 0.0246786 |
| T2a | z0_zn | contained | 8 | 40 | FQ | none | r2 | 20 | 0.924827 | 0.908539 | 0.937833 |
| T2a | z0_zn | contained | 8 | 40 | FQ | none | mae | 20 | 0.0161316 | 0.0149745 | 0.0172644 |
| T2a | z0_zn | contained | 8 | 40 | E | raw | r2 | 20 | 0.940204 | 0.927806 | 0.951207 |
| T2a | z0_zn | contained | 8 | 40 | E | raw | mae | 20 | 0.0140659 | 0.0130879 | 0.0151201 |
| T2a | z0_zn | contained | 8 | 40 | E | std | r2 | 20 | 0.923137 | 0.910748 | 0.933538 |
| T2a | z0_zn | contained | 8 | 40 | E | std | mae | 20 | 0.0156777 | 0.0145479 | 0.0168436 |
| T2a | z0_zn | contained | 8 | 40 | F | std | r2 | 20 | 0.994456 | 0.990303 | 0.997244 |
| T2a | z0_zn | contained | 8 | 40 | F | std | mae | 20 | 0.00418345 | 0.00327765 | 0.00526011 |
| T2a | z0_zn | sanity | 8 | 40 | E2 | raw | r2 | 20 | 0.832968 | 0.792728 | 0.868303 |
| T2a | z0_zn | sanity | 8 | 40 | E2 | raw | mae | 20 | 0.0230546 | 0.0214617 | 0.0246608 |
| T2a | z0_zn | sanity | 8 | 40 | E_X | raw | r2 | 20 | 0.86912 | 0.838933 | 0.89549 |
| T2a | z0_zn | sanity | 8 | 40 | E_X | raw | mae | 20 | 0.0214493 | 0.0199111 | 0.0232038 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | baseline_mean | none | r2 | 20 | -0.0348022 | -0.0563957 | -0.0160471 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | baseline_mean | none | mae | 20 | 0.0882927 | 0.0858402 | 0.0910763 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.883962 | 0.868993 | 0.897746 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0256154 | 0.0243433 | 0.0269754 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | PQK-2nn | none | r2 | 20 | 0.92743 | 0.91945 | 0.935555 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | PQK-2nn | none | mae | 20 | 0.0196835 | 0.0184645 | 0.0208779 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | FQ | none | r2 | 20 | 0.944832 | 0.936869 | 0.952237 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | FQ | none | mae | 20 | 0.0176903 | 0.0165924 | 0.0188813 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | E | raw | r2 | 20 | 0.92702 | 0.917927 | 0.935411 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | E | raw | mae | 20 | 0.0202495 | 0.019138 | 0.0213379 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | E | std | r2 | 20 | 0.899576 | 0.888119 | 0.910384 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | E | std | mae | 20 | 0.0246467 | 0.0233032 | 0.0260081 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | F | std | r2 | 20 | 0.890168 | 0.833811 | 0.925063 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | F | std | mae | 20 | 0.0249703 | 0.0218968 | 0.0292693 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 40 | E2 | raw | r2 | 20 | 0.924716 | 0.915209 | 0.934289 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 40 | E2 | raw | mae | 20 | 0.0198457 | 0.0185626 | 0.0210556 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 40 | E_X | raw | r2 | 20 | 0.884648 | 0.864355 | 0.901772 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 40 | E_X | raw | mae | 20 | 0.0252882 | 0.0237014 | 0.0270301 |
| T2a | z0_zn | contained | 8 | 80 | baseline_mean | none | r2 | 20 | -0.0132264 | -0.0215426 | -0.00658716 |
| T2a | z0_zn | contained | 8 | 80 | baseline_mean | none | mae | 20 | 0.0699301 | 0.0674094 | 0.0725787 |
| T2a | z0_zn | contained | 8 | 80 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.919542 | 0.905342 | 0.93212 |
| T2a | z0_zn | contained | 8 | 80 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0174854 | 0.0165737 | 0.0185163 |
| T2a | z0_zn | contained | 8 | 80 | PQK-2nn | none | r2 | 20 | 0.911806 | 0.896324 | 0.925201 |
| T2a | z0_zn | contained | 8 | 80 | PQK-2nn | none | mae | 20 | 0.017546 | 0.0167304 | 0.0183645 |
| T2a | z0_zn | contained | 8 | 80 | FQ | none | r2 | 20 | 0.968866 | 0.964072 | 0.972906 |
| T2a | z0_zn | contained | 8 | 80 | FQ | none | mae | 20 | 0.0108036 | 0.0102739 | 0.0113603 |
| T2a | z0_zn | contained | 8 | 80 | E | raw | r2 | 20 | 0.976321 | 0.972799 | 0.979439 |
| T2a | z0_zn | contained | 8 | 80 | E | raw | mae | 20 | 0.00927047 | 0.00873926 | 0.00980682 |
| T2a | z0_zn | contained | 8 | 80 | E | std | r2 | 20 | 0.968108 | 0.962618 | 0.972914 |
| T2a | z0_zn | contained | 8 | 80 | E | std | mae | 20 | 0.0106312 | 0.0101498 | 0.011172 |
| T2a | z0_zn | contained | 8 | 80 | F | std | r2 | 20 | 1 | 1 | 1 |
| T2a | z0_zn | contained | 8 | 80 | F | std | mae | 20 | 5.47026e-06 | 4.52286e-06 | 6.47232e-06 |
| T2a | z0_zn | sanity | 8 | 80 | E2 | raw | r2 | 20 | 0.91387 | 0.898606 | 0.927452 |
| T2a | z0_zn | sanity | 8 | 80 | E2 | raw | mae | 20 | 0.0174084 | 0.0165714 | 0.0182686 |
| T2a | z0_zn | sanity | 8 | 80 | E_X | raw | r2 | 20 | 0.914298 | 0.897276 | 0.928911 |
| T2a | z0_zn | sanity | 8 | 80 | E_X | raw | mae | 20 | 0.017573 | 0.0166712 | 0.0184927 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | baseline_mean | none | r2 | 20 | -0.0152682 | -0.0233126 | -0.00814739 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | baseline_mean | none | mae | 20 | 0.0867999 | 0.0849925 | 0.0887704 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.927158 | 0.914083 | 0.938571 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.020121 | 0.0186848 | 0.0216641 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | PQK-2nn | none | r2 | 20 | 0.963213 | 0.954886 | 0.970385 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | PQK-2nn | none | mae | 20 | 0.0138703 | 0.0128009 | 0.0151757 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | FQ | none | r2 | 20 | 0.972527 | 0.966712 | 0.977523 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | FQ | none | mae | 20 | 0.0125108 | 0.0115617 | 0.0135779 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | E | raw | r2 | 20 | 0.962619 | 0.956439 | 0.968443 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | E | raw | mae | 20 | 0.0143308 | 0.0134081 | 0.0153377 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | E | std | r2 | 20 | 0.951196 | 0.944208 | 0.957335 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | E | std | mae | 20 | 0.0169932 | 0.0161577 | 0.0178943 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | F | std | r2 | 20 | 0.963779 | 0.957038 | 0.969277 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | F | std | mae | 20 | 0.0149047 | 0.0138923 | 0.0161471 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 80 | E2 | raw | r2 | 20 | 0.96443 | 0.955794 | 0.971374 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 80 | E2 | raw | mae | 20 | 0.0136988 | 0.0126682 | 0.0150358 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 80 | E_X | raw | r2 | 20 | 0.933704 | 0.922446 | 0.943801 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 80 | E_X | raw | mae | 20 | 0.0190827 | 0.0179204 | 0.0203145 |
| T2a | z0_zn | contained | 8 | 160 | baseline_mean | none | r2 | 20 | -0.0113966 | -0.0187393 | -0.0055127 |
| T2a | z0_zn | contained | 8 | 160 | baseline_mean | none | mae | 20 | 0.0697378 | 0.0670641 | 0.072707 |
| T2a | z0_zn | contained | 8 | 160 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.943857 | 0.937206 | 0.950103 |
| T2a | z0_zn | contained | 8 | 160 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0148177 | 0.0141775 | 0.0154601 |
| T2a | z0_zn | contained | 8 | 160 | PQK-2nn | none | r2 | 20 | 0.953102 | 0.947903 | 0.958429 |
| T2a | z0_zn | contained | 8 | 160 | PQK-2nn | none | mae | 20 | 0.0136585 | 0.0131423 | 0.0141356 |
| T2a | z0_zn | contained | 8 | 160 | FQ | none | r2 | 20 | 0.985502 | 0.983546 | 0.987218 |
| T2a | z0_zn | contained | 8 | 160 | FQ | none | mae | 20 | 0.00789432 | 0.00746213 | 0.00833353 |
| T2a | z0_zn | contained | 8 | 160 | E | raw | r2 | 20 | 0.989561 | 0.98828 | 0.990645 |
| T2a | z0_zn | contained | 8 | 160 | E | raw | mae | 20 | 0.00666987 | 0.00634586 | 0.00701396 |
| T2a | z0_zn | contained | 8 | 160 | E | std | r2 | 20 | 0.98609 | 0.983992 | 0.987967 |
| T2a | z0_zn | contained | 8 | 160 | E | std | mae | 20 | 0.00743592 | 0.00706321 | 0.00784307 |
| T2a | z0_zn | contained | 8 | 160 | F | std | r2 | 20 | 1 | 1 | 1 |
| T2a | z0_zn | contained | 8 | 160 | F | std | mae | 20 | 9.54541e-07 | 8.40394e-07 | 1.06937e-06 |
| T2a | z0_zn | sanity | 8 | 160 | E2 | raw | r2 | 20 | 0.953943 | 0.948999 | 0.959082 |
| T2a | z0_zn | sanity | 8 | 160 | E2 | raw | mae | 20 | 0.0135938 | 0.0130974 | 0.014058 |
| T2a | z0_zn | sanity | 8 | 160 | E_X | raw | r2 | 20 | 0.947843 | 0.942487 | 0.95351 |
| T2a | z0_zn | sanity | 8 | 160 | E_X | raw | mae | 20 | 0.0144555 | 0.0138493 | 0.0150951 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | baseline_mean | none | r2 | 20 | -0.0112725 | -0.0158214 | -0.00690624 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | baseline_mean | none | mae | 20 | 0.0860142 | 0.084314 | 0.0877908 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.964272 | 0.961402 | 0.967091 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0145046 | 0.0141208 | 0.0148734 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | PQK-2nn | none | r2 | 20 | 0.984998 | 0.982969 | 0.986737 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | PQK-2nn | none | mae | 20 | 0.00933755 | 0.00886693 | 0.00987644 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | FQ | none | r2 | 20 | 0.987974 | 0.98672 | 0.989159 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | FQ | none | mae | 20 | 0.008567 | 0.00819242 | 0.008965 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | E | raw | r2 | 20 | 0.9843 | 0.982705 | 0.985821 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | E | raw | mae | 20 | 0.009741 | 0.00940848 | 0.010072 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | E | std | r2 | 20 | 0.977707 | 0.974823 | 0.980039 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | E | std | mae | 20 | 0.0117364 | 0.0113187 | 0.0121863 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | F | std | r2 | 20 | 0.975678 | 0.973877 | 0.977557 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | F | std | mae | 20 | 0.0122392 | 0.0118228 | 0.0126474 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 160 | E2 | raw | r2 | 20 | 0.985226 | 0.983251 | 0.986922 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 160 | E2 | raw | mae | 20 | 0.0093042 | 0.00883878 | 0.00983798 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 160 | E_X | raw | r2 | 20 | 0.960934 | 0.957855 | 0.96407 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 160 | E_X | raw | mae | 20 | 0.015273 | 0.0148615 | 0.0156525 |

## Task 3: Kernel Concentration Diagnostics

| task | tag | n | hilbert_dim | kernel | gamma_rule | metric | num_seeds | mean | ci_95_lower | ci_95_upper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T3 | logunif | 4 | 16 | FQ | none | off_diag_mean | 20 | 0.728361 | 0.718822 | 0.737282 |
| T3 | logunif | 4 | 16 | FQ | none | off_diag_var | 20 | 0.0717929 | 0.0675114 | 0.0768612 |
| T3 | logunif | 4 | 16 | PQK-1 | 1.0 | off_diag_mean | 20 | 0.689181 | 0.6809 | 0.697626 |
| T3 | logunif | 4 | 16 | PQK-1 | 1.0 | off_diag_var | 20 | 0.0900825 | 0.0856087 | 0.095234 |
| T3 | logunif | 4 | 16 | PQK-1 | 0.1/n | off_diag_mean | 20 | 0.987621 | 0.987144 | 0.988076 |
| T3 | logunif | 4 | 16 | PQK-1 | 0.1/n | off_diag_var | 20 | 0.000182651 | 0.000171382 | 0.000195327 |
| T3 | logunif | 4 | 16 | PQK-1 | 0.3/n | off_diag_mean | 20 | 0.963862 | 0.962496 | 0.965169 |
| T3 | logunif | 4 | 16 | PQK-1 | 0.3/n | off_diag_var | 20 | 0.00153427 | 0.00144136 | 0.00163982 |
| T3 | logunif | 4 | 16 | PQK-1 | 1.0/n | off_diag_mean | 20 | 0.890177 | 0.886325 | 0.8939 |
| T3 | logunif | 4 | 16 | PQK-1 | 1.0/n | off_diag_var | 20 | 0.0134945 | 0.0127113 | 0.0143899 |
| T3 | logunif | 4 | 16 | PQK-1 | 3.0/n | off_diag_mean | 20 | 0.740597 | 0.73313 | 0.748153 |
| T3 | logunif | 4 | 16 | PQK-1 | 3.0/n | off_diag_var | 20 | 0.0663566 | 0.0629161 | 0.0703052 |
| T3 | logunif | 4 | 16 | PQK-1 | 10.0/n | off_diag_mean | 20 | 0.530044 | 0.51948 | 0.540998 |
| T3 | logunif | 4 | 16 | PQK-1 | 10.0/n | off_diag_var | 20 | 0.159628 | 0.15263 | 0.16738 |
| T3 | logunif | 4 | 16 | PQK-2nn | 0.1/n | off_diag_mean | 20 | 0.979676 | 0.978917 | 0.980385 |
| T3 | logunif | 4 | 16 | PQK-2nn | 0.1/n | off_diag_var | 20 | 0.000447178 | 0.000419511 | 0.000478854 |
| T3 | logunif | 4 | 16 | PQK-2nn | 0.3/n | off_diag_mean | 20 | 0.941575 | 0.939474 | 0.943551 |
| T3 | logunif | 4 | 16 | PQK-2nn | 0.3/n | off_diag_var | 20 | 0.00360695 | 0.00338949 | 0.00385817 |
| T3 | logunif | 4 | 16 | PQK-2nn | 1.0/n | off_diag_mean | 20 | 0.830962 | 0.8256 | 0.836053 |
| T3 | logunif | 4 | 16 | PQK-2nn | 1.0/n | off_diag_var | 20 | 0.027837 | 0.0263051 | 0.02965 |
| T3 | logunif | 4 | 16 | PQK-2nn | 3.0/n | off_diag_mean | 20 | 0.641016 | 0.632917 | 0.649279 |
| T3 | logunif | 4 | 16 | PQK-2nn | 3.0/n | off_diag_var | 20 | 0.102748 | 0.0980463 | 0.108331 |
| T3 | logunif | 4 | 16 | PQK-2nn | 10.0/n | off_diag_mean | 20 | 0.438163 | 0.427733 | 0.448905 |
| T3 | logunif | 4 | 16 | PQK-2nn | 10.0/n | off_diag_var | 20 | 0.163595 | 0.157759 | 0.170172 |
| T3 | logunif | 6 | 64 | FQ | none | off_diag_mean | 20 | 0.620591 | 0.611214 | 0.630133 |
| T3 | logunif | 6 | 64 | FQ | none | off_diag_var | 20 | 0.118306 | 0.112322 | 0.12433 |
| T3 | logunif | 6 | 64 | PQK-1 | 1.0 | off_diag_mean | 20 | 0.601089 | 0.592401 | 0.610071 |
| T3 | logunif | 6 | 64 | PQK-1 | 1.0 | off_diag_var | 20 | 0.126243 | 0.120752 | 0.131941 |
| T3 | logunif | 6 | 64 | PQK-1 | 0.1/n | off_diag_mean | 20 | 0.98701 | 0.986463 | 0.987542 |
| T3 | logunif | 6 | 64 | PQK-1 | 0.1/n | off_diag_var | 20 | 0.000192346 | 0.000179055 | 0.000206338 |
| T3 | logunif | 6 | 64 | PQK-1 | 0.3/n | off_diag_mean | 20 | 0.962105 | 0.960546 | 0.963625 |
| T3 | logunif | 6 | 64 | PQK-1 | 0.3/n | off_diag_var | 20 | 0.00161197 | 0.00150284 | 0.00172717 |
| T3 | logunif | 6 | 64 | PQK-1 | 1.0/n | off_diag_mean | 20 | 0.885094 | 0.880726 | 0.889353 |
| T3 | logunif | 6 | 64 | PQK-1 | 1.0/n | off_diag_var | 20 | 0.0140712 | 0.0131783 | 0.0150112 |
| T3 | logunif | 6 | 64 | PQK-1 | 3.0/n | off_diag_mean | 20 | 0.729943 | 0.721823 | 0.738042 |
| T3 | logunif | 6 | 64 | PQK-1 | 3.0/n | off_diag_var | 20 | 0.0680088 | 0.0643634 | 0.0718297 |
| T3 | logunif | 6 | 64 | PQK-1 | 10.0/n | off_diag_mean | 20 | 0.514508 | 0.506556 | 0.522816 |
| T3 | logunif | 6 | 64 | PQK-1 | 10.0/n | off_diag_var | 20 | 0.159492 | 0.153769 | 0.165405 |
| T3 | logunif | 6 | 64 | PQK-2nn | 0.1/n | off_diag_mean | 20 | 0.976066 | 0.975223 | 0.976891 |
| T3 | logunif | 6 | 64 | PQK-2nn | 0.1/n | off_diag_var | 20 | 0.000600472 | 0.000564689 | 0.000638353 |
| T3 | logunif | 6 | 64 | PQK-2nn | 0.3/n | off_diag_mean | 20 | 0.931662 | 0.929358 | 0.93392 |
| T3 | logunif | 6 | 64 | PQK-2nn | 0.3/n | off_diag_var | 20 | 0.00476809 | 0.00449027 | 0.00506248 |
| T3 | logunif | 6 | 64 | PQK-2nn | 1.0/n | off_diag_mean | 20 | 0.806465 | 0.800881 | 0.811986 |
| T3 | logunif | 6 | 64 | PQK-2nn | 1.0/n | off_diag_var | 20 | 0.0350357 | 0.0331338 | 0.0370072 |
| T3 | logunif | 6 | 64 | PQK-2nn | 3.0/n | off_diag_mean | 20 | 0.606679 | 0.599429 | 0.614331 |
| T3 | logunif | 6 | 64 | PQK-2nn | 3.0/n | off_diag_var | 20 | 0.117331 | 0.111983 | 0.122743 |
| T3 | logunif | 6 | 64 | PQK-2nn | 10.0/n | off_diag_mean | 20 | 0.417294 | 0.409883 | 0.426906 |
| T3 | logunif | 6 | 64 | PQK-2nn | 10.0/n | off_diag_var | 20 | 0.169547 | 0.162994 | 0.176156 |
| T3 | logunif | 8 | 256 | FQ | none | off_diag_mean | 20 | 0.553501 | 0.543143 | 0.564817 |
| T3 | logunif | 8 | 256 | FQ | none | off_diag_var | 20 | 0.150796 | 0.14481 | 0.15667 |
| T3 | logunif | 8 | 256 | PQK-1 | 1.0 | off_diag_mean | 20 | 0.547011 | 0.535421 | 0.560362 |
| T3 | logunif | 8 | 256 | PQK-1 | 1.0 | off_diag_var | 20 | 0.15302 | 0.146681 | 0.159277 |
| T3 | logunif | 8 | 256 | PQK-1 | 0.1/n | off_diag_mean | 20 | 0.986652 | 0.986077 | 0.987295 |
| T3 | logunif | 8 | 256 | PQK-1 | 0.1/n | off_diag_var | 20 | 0.000199563 | 0.000185915 | 0.000211714 |
| T3 | logunif | 8 | 256 | PQK-1 | 0.3/n | off_diag_mean | 20 | 0.961082 | 0.95943 | 0.962931 |
| T3 | logunif | 8 | 256 | PQK-1 | 0.3/n | off_diag_var | 20 | 0.00167288 | 0.0015608 | 0.00177218 |
| T3 | logunif | 8 | 256 | PQK-1 | 1.0/n | off_diag_mean | 20 | 0.882212 | 0.877467 | 0.887491 |
| T3 | logunif | 8 | 256 | PQK-1 | 1.0/n | off_diag_var | 20 | 0.0146151 | 0.0137025 | 0.015419 |
| T3 | logunif | 8 | 256 | PQK-1 | 3.0/n | off_diag_mean | 20 | 0.724657 | 0.715136 | 0.735325 |
| T3 | logunif | 8 | 256 | PQK-1 | 3.0/n | off_diag_var | 20 | 0.0707611 | 0.0670495 | 0.0740714 |
| T3 | logunif | 8 | 256 | PQK-1 | 10.0/n | off_diag_mean | 20 | 0.512757 | 0.501133 | 0.5261 |
| T3 | logunif | 8 | 256 | PQK-1 | 10.0/n | off_diag_var | 20 | 0.165649 | 0.159182 | 0.172201 |
| T3 | logunif | 8 | 256 | PQK-2nn | 0.1/n | off_diag_mean | 20 | 0.974106 | 0.97318 | 0.975098 |
| T3 | logunif | 8 | 256 | PQK-2nn | 0.1/n | off_diag_var | 20 | 0.000699217 | 0.000661667 | 0.00073288 |
| T3 | logunif | 8 | 256 | PQK-2nn | 0.3/n | off_diag_mean | 20 | 0.926359 | 0.923801 | 0.9291 |
| T3 | logunif | 8 | 256 | PQK-2nn | 0.3/n | off_diag_var | 20 | 0.00551961 | 0.00523354 | 0.00577825 |
| T3 | logunif | 8 | 256 | PQK-2nn | 1.0/n | off_diag_mean | 20 | 0.794101 | 0.787641 | 0.801014 |
| T3 | logunif | 8 | 256 | PQK-2nn | 1.0/n | off_diag_var | 20 | 0.0398071 | 0.0379082 | 0.0415394 |
| T3 | logunif | 8 | 256 | PQK-2nn | 3.0/n | off_diag_mean | 20 | 0.593077 | 0.583519 | 0.603704 |
| T3 | logunif | 8 | 256 | PQK-2nn | 3.0/n | off_diag_var | 20 | 0.128239 | 0.122949 | 0.133374 |
| T3 | logunif | 8 | 256 | PQK-2nn | 10.0/n | off_diag_mean | 20 | 0.419992 | 0.409063 | 0.431576 |
| T3 | logunif | 8 | 256 | PQK-2nn | 10.0/n | off_diag_var | 20 | 0.177784 | 0.171892 | 0.18355 |
| T3 | logunif | 10 | 1024 | FQ | none | off_diag_mean | 20 | 0.516826 | 0.507668 | 0.526665 |
| T3 | logunif | 10 | 1024 | FQ | none | off_diag_var | 20 | 0.16631 | 0.159249 | 0.173653 |
| T3 | logunif | 10 | 1024 | PQK-1 | 1.0 | off_diag_mean | 20 | 0.517232 | 0.504948 | 0.530488 |
| T3 | logunif | 10 | 1024 | PQK-1 | 1.0 | off_diag_var | 20 | 0.16891 | 0.161474 | 0.176584 |
| T3 | logunif | 10 | 1024 | PQK-1 | 0.1/n | off_diag_mean | 20 | 0.986636 | 0.985957 | 0.987292 |
| T3 | logunif | 10 | 1024 | PQK-1 | 0.1/n | off_diag_var | 20 | 0.000202955 | 0.000187082 | 0.000220197 |
| T3 | logunif | 10 | 1024 | PQK-1 | 0.3/n | off_diag_mean | 20 | 0.961047 | 0.959109 | 0.962926 |
| T3 | logunif | 10 | 1024 | PQK-1 | 0.3/n | off_diag_var | 20 | 0.00170155 | 0.00157051 | 0.00184338 |
| T3 | logunif | 10 | 1024 | PQK-1 | 1.0/n | off_diag_mean | 20 | 0.88222 | 0.876758 | 0.887509 |
| T3 | logunif | 10 | 1024 | PQK-1 | 1.0/n | off_diag_var | 20 | 0.014872 | 0.0137954 | 0.0160371 |
| T3 | logunif | 10 | 1024 | PQK-1 | 3.0/n | off_diag_mean | 20 | 0.725382 | 0.715091 | 0.735717 |
| T3 | logunif | 10 | 1024 | PQK-1 | 3.0/n | off_diag_var | 20 | 0.0720765 | 0.06763 | 0.0768566 |
| T3 | logunif | 10 | 1024 | PQK-1 | 10.0/n | off_diag_mean | 20 | 0.517232 | 0.504948 | 0.530488 |
| T3 | logunif | 10 | 1024 | PQK-1 | 10.0/n | off_diag_var | 20 | 0.16891 | 0.161474 | 0.176584 |
| T3 | logunif | 10 | 1024 | PQK-2nn | 0.1/n | off_diag_mean | 20 | 0.97338 | 0.972285 | 0.974414 |
| T3 | logunif | 10 | 1024 | PQK-2nn | 0.1/n | off_diag_var | 20 | 0.000748621 | 0.00070157 | 0.00079938 |
| T3 | logunif | 10 | 1024 | PQK-2nn | 0.3/n | off_diag_mean | 20 | 0.924438 | 0.921468 | 0.927261 |
| T3 | logunif | 10 | 1024 | PQK-2nn | 0.3/n | off_diag_var | 20 | 0.00588901 | 0.00552807 | 0.00627879 |
| T3 | logunif | 10 | 1024 | PQK-2nn | 1.0/n | off_diag_mean | 20 | 0.789988 | 0.782949 | 0.796853 |
| T3 | logunif | 10 | 1024 | PQK-2nn | 1.0/n | off_diag_var | 20 | 0.0420166 | 0.0396325 | 0.0445767 |
| T3 | logunif | 10 | 1024 | PQK-2nn | 3.0/n | off_diag_mean | 20 | 0.589891 | 0.58069 | 0.599457 |
| T3 | logunif | 10 | 1024 | PQK-2nn | 3.0/n | off_diag_var | 20 | 0.132576 | 0.126405 | 0.139071 |
| T3 | logunif | 10 | 1024 | PQK-2nn | 10.0/n | off_diag_mean | 20 | 0.4229 | 0.411334 | 0.434944 |
| T3 | logunif | 10 | 1024 | PQK-2nn | 10.0/n | off_diag_var | 20 | 0.179085 | 0.172969 | 0.185254 |
| T3 | logunif | 12 | 4096 | FQ | none | off_diag_mean | 20 | 0.479994 | 0.472012 | 0.488938 |
| T3 | logunif | 12 | 4096 | FQ | none | off_diag_var | 20 | 0.172907 | 0.167282 | 0.179163 |
| T3 | logunif | 12 | 4096 | PQK-1 | 1.0 | off_diag_mean | 20 | 0.479377 | 0.468667 | 0.49145 |
| T3 | logunif | 12 | 4096 | PQK-1 | 1.0 | off_diag_var | 20 | 0.174238 | 0.168309 | 0.180496 |
| T3 | logunif | 12 | 4096 | PQK-1 | 0.1/n | off_diag_mean | 20 | 0.985956 | 0.985329 | 0.986608 |
| T3 | logunif | 12 | 4096 | PQK-1 | 0.1/n | off_diag_var | 20 | 0.000219061 | 0.000203811 | 0.000234026 |
| T3 | logunif | 12 | 4096 | PQK-1 | 0.3/n | off_diag_mean | 20 | 0.959109 | 0.957324 | 0.960969 |
| T3 | logunif | 12 | 4096 | PQK-1 | 0.3/n | off_diag_var | 20 | 0.00183047 | 0.00170539 | 0.00195307 |
| T3 | logunif | 12 | 4096 | PQK-1 | 1.0/n | off_diag_mean | 20 | 0.876793 | 0.871766 | 0.882059 |
| T3 | logunif | 12 | 4096 | PQK-1 | 1.0/n | off_diag_var | 20 | 0.0158224 | 0.0148151 | 0.01682 |
| T3 | logunif | 12 | 4096 | PQK-1 | 3.0/n | off_diag_mean | 20 | 0.714947 | 0.70533 | 0.725396 |
| T3 | logunif | 12 | 4096 | PQK-1 | 3.0/n | off_diag_var | 20 | 0.074665 | 0.0706858 | 0.0786852 |
| T3 | logunif | 12 | 4096 | PQK-1 | 10.0/n | off_diag_mean | 20 | 0.503979 | 0.493326 | 0.516055 |
| T3 | logunif | 12 | 4096 | PQK-1 | 10.0/n | off_diag_var | 20 | 0.167486 | 0.161515 | 0.173861 |
| T3 | logunif | 12 | 4096 | PQK-2nn | 0.1/n | off_diag_mean | 20 | 0.971908 | 0.970841 | 0.973016 |
| T3 | logunif | 12 | 4096 | PQK-2nn | 0.1/n | off_diag_var | 20 | 0.000817653 | 0.000769137 | 0.000865808 |
| T3 | logunif | 12 | 4096 | PQK-2nn | 0.3/n | off_diag_mean | 20 | 0.920458 | 0.917556 | 0.923471 |
| T3 | logunif | 12 | 4096 | PQK-2nn | 0.3/n | off_diag_var | 20 | 0.00638829 | 0.00602205 | 0.0067536 |
| T3 | logunif | 12 | 4096 | PQK-2nn | 1.0/n | off_diag_mean | 20 | 0.780592 | 0.773713 | 0.787804 |
| T3 | logunif | 12 | 4096 | PQK-2nn | 1.0/n | off_diag_var | 20 | 0.0446237 | 0.0423381 | 0.0469607 |
| T3 | logunif | 12 | 4096 | PQK-2nn | 3.0/n | off_diag_mean | 20 | 0.577302 | 0.568473 | 0.58706 |
| T3 | logunif | 12 | 4096 | PQK-2nn | 3.0/n | off_diag_var | 20 | 0.135375 | 0.130039 | 0.141116 |
| T3 | logunif | 12 | 4096 | PQK-2nn | 10.0/n | off_diag_mean | 20 | 0.411412 | 0.40332 | 0.420192 |
| T3 | logunif | 12 | 4096 | PQK-2nn | 10.0/n | off_diag_var | 20 | 0.178887 | 0.173697 | 0.184553 |
| T3 | logunif | 14 | 16384 | FQ | none | off_diag_mean | 20 | 0.45753 | 0.450621 | 0.465708 |
| T3 | logunif | 14 | 16384 | FQ | none | off_diag_var | 20 | 0.176227 | 0.168594 | 0.184082 |
| T3 | logunif | 14 | 16384 | PQK-1 | 1.0 | off_diag_mean | 20 | 0.452858 | 0.445506 | 0.461275 |
| T3 | logunif | 14 | 16384 | PQK-1 | 1.0 | off_diag_var | 20 | 0.176528 | 0.168884 | 0.184433 |
| T3 | logunif | 14 | 16384 | PQK-1 | 0.1/n | off_diag_mean | 20 | 0.985873 | 0.985286 | 0.986469 |
| T3 | logunif | 14 | 16384 | PQK-1 | 0.1/n | off_diag_var | 20 | 0.000215296 | 0.000200857 | 0.000229178 |
| T3 | logunif | 14 | 16384 | PQK-1 | 0.3/n | off_diag_mean | 20 | 0.958853 | 0.957184 | 0.960548 |
| T3 | logunif | 14 | 16384 | PQK-1 | 0.3/n | off_diag_var | 20 | 0.00179972 | 0.00168083 | 0.00191452 |
| T3 | logunif | 14 | 16384 | PQK-1 | 1.0/n | off_diag_mean | 20 | 0.875901 | 0.871218 | 0.880651 |
| T3 | logunif | 14 | 16384 | PQK-1 | 1.0/n | off_diag_var | 20 | 0.0155775 | 0.0146064 | 0.0165293 |
| T3 | logunif | 14 | 16384 | PQK-1 | 3.0/n | off_diag_mean | 20 | 0.712216 | 0.7036 | 0.721007 |
| T3 | logunif | 14 | 16384 | PQK-1 | 3.0/n | off_diag_var | 20 | 0.0737642 | 0.0696856 | 0.0777916 |
| T3 | logunif | 14 | 16384 | PQK-1 | 10.0/n | off_diag_mean | 20 | 0.497314 | 0.490147 | 0.505637 |
| T3 | logunif | 14 | 16384 | PQK-1 | 10.0/n | off_diag_var | 20 | 0.166228 | 0.158574 | 0.174011 |
| T3 | logunif | 14 | 16384 | PQK-2nn | 0.1/n | off_diag_mean | 20 | 0.971538 | 0.970517 | 0.972535 |
| T3 | logunif | 14 | 16384 | PQK-2nn | 0.1/n | off_diag_var | 20 | 0.000827328 | 0.000779446 | 0.000873749 |
| T3 | logunif | 14 | 16384 | PQK-2nn | 0.3/n | off_diag_mean | 20 | 0.919435 | 0.916668 | 0.922127 |
| T3 | logunif | 14 | 16384 | PQK-2nn | 0.3/n | off_diag_var | 20 | 0.00646038 | 0.00609402 | 0.00681533 |
| T3 | logunif | 14 | 16384 | PQK-2nn | 1.0/n | off_diag_mean | 20 | 0.777989 | 0.771491 | 0.784325 |
| T3 | logunif | 14 | 16384 | PQK-2nn | 1.0/n | off_diag_var | 20 | 0.0450583 | 0.0426636 | 0.0474176 |
| T3 | logunif | 14 | 16384 | PQK-2nn | 3.0/n | off_diag_mean | 20 | 0.573259 | 0.565586 | 0.581312 |
| T3 | logunif | 14 | 16384 | PQK-2nn | 3.0/n | off_diag_var | 20 | 0.136315 | 0.129779 | 0.142917 |
| T3 | logunif | 14 | 16384 | PQK-2nn | 10.0/n | off_diag_mean | 20 | 0.408117 | 0.397935 | 0.419077 |
| T3 | logunif | 14 | 16384 | PQK-2nn | 10.0/n | off_diag_var | 20 | 0.17838 | 0.171213 | 0.185671 |
| T3 | narrow | 4 | 16 | FQ | none | off_diag_mean | 20 | 0.983466 | 0.982655 | 0.984331 |
| T3 | narrow | 4 | 16 | FQ | none | off_diag_var | 20 | 0.000401034 | 0.00036708 | 0.000434498 |
| T3 | narrow | 4 | 16 | PQK-1 | 1.0 | off_diag_mean | 20 | 0.979696 | 0.978576 | 0.980869 |
| T3 | narrow | 4 | 16 | PQK-1 | 1.0 | off_diag_var | 20 | 0.000632527 | 0.000573316 | 0.00069175 |
| T3 | narrow | 4 | 16 | PQK-1 | 0.1/n | off_diag_mean | 20 | 0.999479 | 0.99945 | 0.99951 |
| T3 | narrow | 4 | 16 | PQK-1 | 0.1/n | off_diag_var | 20 | 4.28572e-07 | 3.87078e-07 | 4.69875e-07 |
| T3 | narrow | 4 | 16 | PQK-1 | 0.3/n | off_diag_mean | 20 | 0.998439 | 0.998351 | 0.998531 |
| T3 | narrow | 4 | 16 | PQK-1 | 0.3/n | off_diag_var | 20 | 3.84104e-06 | 3.47004e-06 | 4.21081e-06 |
| T3 | narrow | 4 | 16 | PQK-1 | 1.0/n | off_diag_mean | 20 | 0.994821 | 0.994531 | 0.995124 |
| T3 | narrow | 4 | 16 | PQK-1 | 1.0/n | off_diag_var | 20 | 4.20593e-05 | 3.80307e-05 | 4.60888e-05 |
| T3 | narrow | 4 | 16 | PQK-1 | 3.0/n | off_diag_mean | 20 | 0.98467 | 0.983821 | 0.98556 |
| T3 | narrow | 4 | 16 | PQK-1 | 3.0/n | off_diag_var | 20 | 0.000363176 | 0.000328911 | 0.00039745 |
| T3 | narrow | 4 | 16 | PQK-1 | 10.0/n | off_diag_mean | 20 | 0.951186 | 0.948584 | 0.953943 |
| T3 | narrow | 4 | 16 | PQK-1 | 10.0/n | off_diag_var | 20 | 0.00350366 | 0.00319051 | 0.00381906 |
| T3 | narrow | 4 | 16 | PQK-2nn | 0.1/n | off_diag_mean | 20 | 0.998995 | 0.998942 | 0.99905 |
| T3 | narrow | 4 | 16 | PQK-2nn | 0.1/n | off_diag_var | 20 | 1.53057e-06 | 1.39172e-06 | 1.66837e-06 |
| T3 | narrow | 4 | 16 | PQK-2nn | 0.3/n | off_diag_mean | 20 | 0.996992 | 0.996835 | 0.997157 |
| T3 | narrow | 4 | 16 | PQK-2nn | 0.3/n | off_diag_var | 20 | 1.36665e-05 | 1.24308e-05 | 1.48924e-05 |
| T3 | narrow | 4 | 16 | PQK-2nn | 1.0/n | off_diag_mean | 20 | 0.990061 | 0.989545 | 0.990605 |
| T3 | narrow | 4 | 16 | PQK-2nn | 1.0/n | off_diag_var | 20 | 0.00014772 | 0.000134521 | 0.000160826 |
| T3 | narrow | 4 | 16 | PQK-2nn | 3.0/n | off_diag_mean | 20 | 0.970919 | 0.969435 | 0.972486 |
| T3 | narrow | 4 | 16 | PQK-2nn | 3.0/n | off_diag_var | 20 | 0.00123018 | 0.00112385 | 0.00133551 |
| T3 | narrow | 4 | 16 | PQK-2nn | 10.0/n | off_diag_mean | 20 | 0.91084 | 0.906549 | 0.915433 |
| T3 | narrow | 4 | 16 | PQK-2nn | 10.0/n | off_diag_var | 20 | 0.0105509 | 0.00973055 | 0.0113637 |
| T3 | narrow | 6 | 64 | FQ | none | off_diag_mean | 20 | 0.958791 | 0.956016 | 0.961516 |
| T3 | narrow | 6 | 64 | FQ | none | off_diag_var | 20 | 0.00241999 | 0.00215378 | 0.00272271 |
| T3 | narrow | 6 | 64 | PQK-1 | 1.0 | off_diag_mean | 20 | 0.947953 | 0.944365 | 0.951594 |
| T3 | narrow | 6 | 64 | PQK-1 | 1.0 | off_diag_var | 20 | 0.00390755 | 0.00347243 | 0.0044015 |
| T3 | narrow | 6 | 64 | PQK-1 | 0.1/n | off_diag_mean | 20 | 0.999071 | 0.999003 | 0.999139 |
| T3 | narrow | 6 | 64 | PQK-1 | 0.1/n | off_diag_var | 20 | 1.3401e-06 | 1.18217e-06 | 1.51995e-06 |
| T3 | narrow | 6 | 64 | PQK-1 | 0.3/n | off_diag_mean | 20 | 0.997219 | 0.997017 | 0.997422 |
| T3 | narrow | 6 | 64 | PQK-1 | 0.3/n | off_diag_var | 20 | 1.19727e-05 | 1.05634e-05 | 1.35766e-05 |
| T3 | narrow | 6 | 64 | PQK-1 | 1.0/n | off_diag_mean | 20 | 0.990807 | 0.990143 | 0.991473 |
| T3 | narrow | 6 | 64 | PQK-1 | 1.0/n | off_diag_var | 20 | 0.000129669 | 0.000114513 | 0.000146931 |
| T3 | narrow | 6 | 64 | PQK-1 | 3.0/n | off_diag_mean | 20 | 0.973062 | 0.971155 | 0.974987 |
| T3 | narrow | 6 | 64 | PQK-1 | 3.0/n | off_diag_var | 20 | 0.00108578 | 0.000961383 | 0.00122745 |
| T3 | narrow | 6 | 64 | PQK-1 | 10.0/n | off_diag_mean | 20 | 0.917039 | 0.911521 | 0.922645 |
| T3 | narrow | 6 | 64 | PQK-1 | 10.0/n | off_diag_var | 20 | 0.00947174 | 0.00845268 | 0.0106233 |
| T3 | narrow | 6 | 64 | PQK-2nn | 0.1/n | off_diag_mean | 20 | 0.998008 | 0.997865 | 0.99815 |
| T3 | narrow | 6 | 64 | PQK-2nn | 0.1/n | off_diag_var | 20 | 6.01374e-06 | 5.31684e-06 | 6.80637e-06 |
| T3 | narrow | 6 | 64 | PQK-2nn | 0.3/n | off_diag_mean | 20 | 0.994054 | 0.99363 | 0.994476 |
| T3 | narrow | 6 | 64 | PQK-2nn | 0.3/n | off_diag_var | 20 | 5.32878e-05 | 4.71378e-05 | 6.02805e-05 |
| T3 | narrow | 6 | 64 | PQK-2nn | 1.0/n | off_diag_mean | 20 | 0.980524 | 0.979159 | 0.981894 |
| T3 | narrow | 6 | 64 | PQK-2nn | 1.0/n | off_diag_var | 20 | 0.000560974 | 0.000497127 | 0.00063354 |
| T3 | narrow | 6 | 64 | PQK-2nn | 3.0/n | off_diag_mean | 20 | 0.944359 | 0.94061 | 0.948142 |
| T3 | narrow | 6 | 64 | PQK-2nn | 3.0/n | off_diag_var | 20 | 0.00434529 | 0.00386961 | 0.00488427 |
| T3 | narrow | 6 | 64 | PQK-2nn | 10.0/n | off_diag_mean | 20 | 0.841488 | 0.832195 | 0.851214 |
| T3 | narrow | 6 | 64 | PQK-2nn | 10.0/n | off_diag_var | 20 | 0.0298835 | 0.0270499 | 0.0330792 |
| T3 | narrow | 8 | 256 | FQ | none | off_diag_mean | 20 | 0.933725 | 0.927379 | 0.93982 |
| T3 | narrow | 8 | 256 | FQ | none | off_diag_var | 20 | 0.00637009 | 0.00553735 | 0.00727297 |
| T3 | narrow | 8 | 256 | PQK-1 | 1.0 | off_diag_mean | 20 | 0.919879 | 0.912187 | 0.927319 |
| T3 | narrow | 8 | 256 | PQK-1 | 1.0 | off_diag_var | 20 | 0.00932552 | 0.00813562 | 0.0106174 |
| T3 | narrow | 8 | 256 | PQK-1 | 0.1/n | off_diag_mean | 20 | 0.998878 | 0.998762 | 0.99899 |
| T3 | narrow | 8 | 256 | PQK-1 | 0.1/n | off_diag_var | 20 | 2.05515e-06 | 1.76121e-06 | 2.37688e-06 |
| T3 | narrow | 8 | 256 | PQK-1 | 0.3/n | off_diag_mean | 20 | 0.996643 | 0.996298 | 0.996978 |
| T3 | narrow | 8 | 256 | PQK-1 | 0.3/n | off_diag_var | 20 | 1.83283e-05 | 1.57136e-05 | 2.11863e-05 |
| T3 | narrow | 8 | 256 | PQK-1 | 1.0/n | off_diag_mean | 20 | 0.988928 | 0.987796 | 0.990025 |
| T3 | narrow | 8 | 256 | PQK-1 | 1.0/n | off_diag_var | 20 | 0.000197282 | 0.0001694 | 0.00022763 |
| T3 | narrow | 8 | 256 | PQK-1 | 3.0/n | off_diag_mean | 20 | 0.967748 | 0.964505 | 0.970882 |
| T3 | narrow | 8 | 256 | PQK-1 | 3.0/n | off_diag_var | 20 | 0.00162393 | 0.00140139 | 0.00186649 |
| T3 | narrow | 8 | 256 | PQK-1 | 10.0/n | off_diag_mean | 20 | 0.90254 | 0.893344 | 0.911459 |
| T3 | narrow | 8 | 256 | PQK-1 | 10.0/n | off_diag_var | 20 | 0.0134253 | 0.0117649 | 0.0152227 |
| T3 | narrow | 8 | 256 | PQK-2nn | 0.1/n | off_diag_mean | 20 | 0.997443 | 0.997183 | 0.997695 |
| T3 | narrow | 8 | 256 | PQK-2nn | 0.1/n | off_diag_var | 20 | 1.04535e-05 | 8.9781e-06 | 1.20645e-05 |
| T3 | narrow | 8 | 256 | PQK-2nn | 0.3/n | off_diag_mean | 20 | 0.992382 | 0.991609 | 0.993128 |
| T3 | narrow | 8 | 256 | PQK-2nn | 0.3/n | off_diag_var | 20 | 9.21701e-05 | 7.92482e-05 | 0.000106284 |
| T3 | narrow | 8 | 256 | PQK-2nn | 1.0/n | off_diag_mean | 20 | 0.975195 | 0.972716 | 0.977583 |
| T3 | narrow | 8 | 256 | PQK-2nn | 1.0/n | off_diag_var | 20 | 0.000953963 | 0.000823495 | 0.00109637 |
| T3 | narrow | 8 | 256 | PQK-2nn | 3.0/n | off_diag_mean | 20 | 0.930248 | 0.923573 | 0.9367 |
| T3 | narrow | 8 | 256 | PQK-2nn | 3.0/n | off_diag_var | 20 | 0.00706219 | 0.00615586 | 0.00804551 |
| T3 | narrow | 8 | 256 | PQK-2nn | 10.0/n | off_diag_mean | 20 | 0.810108 | 0.79421 | 0.825876 |
| T3 | narrow | 8 | 256 | PQK-2nn | 10.0/n | off_diag_var | 20 | 0.0428231 | 0.0384389 | 0.0475857 |
| T3 | narrow | 10 | 1024 | FQ | none | off_diag_mean | 20 | 0.897012 | 0.888836 | 0.905805 |
| T3 | narrow | 10 | 1024 | FQ | none | off_diag_var | 20 | 0.0144548 | 0.0126592 | 0.0161952 |
| T3 | narrow | 10 | 1024 | PQK-1 | 1.0 | off_diag_mean | 20 | 0.881313 | 0.871744 | 0.891691 |
| T3 | narrow | 10 | 1024 | PQK-1 | 1.0 | off_diag_var | 20 | 0.0188585 | 0.0165332 | 0.0210765 |
| T3 | narrow | 10 | 1024 | PQK-1 | 0.1/n | off_diag_mean | 20 | 0.998591 | 0.998464 | 0.998725 |
| T3 | narrow | 10 | 1024 | PQK-1 | 0.1/n | off_diag_var | 20 | 3.15432e-06 | 2.70765e-06 | 3.59099e-06 |
| T3 | narrow | 10 | 1024 | PQK-1 | 0.3/n | off_diag_mean | 20 | 0.995788 | 0.995411 | 0.99619 |
| T3 | narrow | 10 | 1024 | PQK-1 | 0.3/n | off_diag_var | 20 | 2.80741e-05 | 2.41098e-05 | 3.1949e-05 |
| T3 | narrow | 10 | 1024 | PQK-1 | 1.0/n | off_diag_mean | 20 | 0.986139 | 0.984912 | 0.987454 |
| T3 | narrow | 10 | 1024 | PQK-1 | 1.0/n | off_diag_var | 20 | 0.000300076 | 0.000258102 | 0.000341079 |
| T3 | narrow | 10 | 1024 | PQK-1 | 3.0/n | off_diag_mean | 20 | 0.959893 | 0.956426 | 0.963627 |
| T3 | narrow | 10 | 1024 | PQK-1 | 3.0/n | off_diag_var | 20 | 0.00242281 | 0.00209371 | 0.00274123 |
| T3 | narrow | 10 | 1024 | PQK-1 | 10.0/n | off_diag_mean | 20 | 0.881313 | 0.871744 | 0.891691 |
| T3 | narrow | 10 | 1024 | PQK-1 | 10.0/n | off_diag_var | 20 | 0.0188585 | 0.0165332 | 0.0210765 |
| T3 | narrow | 10 | 1024 | PQK-2nn | 0.1/n | off_diag_mean | 20 | 0.996683 | 0.996391 | 0.996996 |
| T3 | narrow | 10 | 1024 | PQK-2nn | 0.1/n | off_diag_var | 20 | 1.7145e-05 | 1.47619e-05 | 1.94666e-05 |
| T3 | narrow | 10 | 1024 | PQK-2nn | 0.3/n | off_diag_mean | 20 | 0.990134 | 0.98927 | 0.99106 |
| T3 | narrow | 10 | 1024 | PQK-2nn | 0.3/n | off_diag_var | 20 | 0.000150362 | 0.0001296 | 0.000170595 |
| T3 | narrow | 10 | 1024 | PQK-2nn | 1.0/n | off_diag_mean | 20 | 0.968078 | 0.96533 | 0.971025 |
| T3 | narrow | 10 | 1024 | PQK-2nn | 1.0/n | off_diag_var | 20 | 0.00152805 | 0.00132131 | 0.00172829 |
| T3 | narrow | 10 | 1024 | PQK-2nn | 3.0/n | off_diag_mean | 20 | 0.911723 | 0.904506 | 0.919555 |
| T3 | narrow | 10 | 1024 | PQK-2nn | 3.0/n | off_diag_var | 20 | 0.0107792 | 0.00941229 | 0.0120853 |
| T3 | narrow | 10 | 1024 | PQK-2nn | 10.0/n | off_diag_mean | 20 | 0.770436 | 0.754309 | 0.788023 |
| T3 | narrow | 10 | 1024 | PQK-2nn | 10.0/n | off_diag_var | 20 | 0.0574443 | 0.0515906 | 0.0629651 |
| T3 | narrow | 12 | 4096 | FQ | none | off_diag_mean | 20 | 0.871365 | 0.860177 | 0.882833 |
| T3 | narrow | 12 | 4096 | FQ | none | off_diag_var | 20 | 0.0223932 | 0.0194906 | 0.0252379 |
| T3 | narrow | 12 | 4096 | PQK-1 | 1.0 | off_diag_mean | 20 | 0.857994 | 0.845732 | 0.870655 |
| T3 | narrow | 12 | 4096 | PQK-1 | 1.0 | off_diag_var | 20 | 0.0265321 | 0.0231903 | 0.0297986 |
| T3 | narrow | 12 | 4096 | PQK-1 | 0.1/n | off_diag_mean | 20 | 0.998534 | 0.998394 | 0.998679 |
| T3 | narrow | 12 | 4096 | PQK-1 | 0.1/n | off_diag_var | 20 | 3.48638e-06 | 2.97383e-06 | 3.98938e-06 |
| T3 | narrow | 12 | 4096 | PQK-1 | 0.3/n | off_diag_mean | 20 | 0.995619 | 0.995201 | 0.996051 |
| T3 | narrow | 12 | 4096 | PQK-1 | 0.3/n | off_diag_var | 20 | 3.10123e-05 | 2.6465e-05 | 3.54752e-05 |
| T3 | narrow | 12 | 4096 | PQK-1 | 1.0/n | off_diag_mean | 20 | 0.985593 | 0.98423 | 0.987005 |
| T3 | narrow | 12 | 4096 | PQK-1 | 1.0/n | off_diag_var | 20 | 0.000330842 | 0.000282732 | 0.000378031 |
| T3 | narrow | 12 | 4096 | PQK-1 | 3.0/n | off_diag_mean | 20 | 0.958395 | 0.954527 | 0.962387 |
| T3 | narrow | 12 | 4096 | PQK-1 | 3.0/n | off_diag_var | 20 | 0.00265711 | 0.00228112 | 0.00302666 |
| T3 | narrow | 12 | 4096 | PQK-1 | 10.0/n | off_diag_mean | 20 | 0.877628 | 0.866876 | 0.888707 |
| T3 | narrow | 12 | 4096 | PQK-1 | 10.0/n | off_diag_var | 20 | 0.0203481 | 0.0177194 | 0.0229212 |
| T3 | narrow | 12 | 4096 | PQK-2nn | 0.1/n | off_diag_mean | 20 | 0.996472 | 0.996138 | 0.996817 |
| T3 | narrow | 12 | 4096 | PQK-2nn | 0.1/n | off_diag_var | 20 | 1.98176e-05 | 1.69494e-05 | 2.26365e-05 |
| T3 | narrow | 12 | 4096 | PQK-2nn | 0.3/n | off_diag_mean | 20 | 0.989514 | 0.988526 | 0.990534 |
| T3 | narrow | 12 | 4096 | PQK-2nn | 0.3/n | off_diag_var | 20 | 0.000173477 | 0.000148524 | 0.00019801 |
| T3 | narrow | 12 | 4096 | PQK-2nn | 1.0/n | off_diag_mean | 20 | 0.96615 | 0.963003 | 0.969391 |
| T3 | narrow | 12 | 4096 | PQK-2nn | 1.0/n | off_diag_var | 20 | 0.00175185 | 0.00150569 | 0.00199444 |
| T3 | narrow | 12 | 4096 | PQK-2nn | 3.0/n | off_diag_mean | 20 | 0.906964 | 0.898661 | 0.915507 |
| T3 | narrow | 12 | 4096 | PQK-2nn | 3.0/n | off_diag_var | 20 | 0.0121557 | 0.0105497 | 0.0137354 |
| T3 | narrow | 12 | 4096 | PQK-2nn | 10.0/n | off_diag_mean | 20 | 0.761933 | 0.74349 | 0.781056 |
| T3 | narrow | 12 | 4096 | PQK-2nn | 10.0/n | off_diag_var | 20 | 0.0620521 | 0.05545 | 0.0684919 |
| T3 | narrow | 14 | 16384 | FQ | none | off_diag_mean | 20 | 0.838171 | 0.825139 | 0.851902 |
| T3 | narrow | 14 | 16384 | FQ | none | off_diag_var | 20 | 0.0310476 | 0.0281619 | 0.0339202 |
| T3 | narrow | 14 | 16384 | PQK-1 | 1.0 | off_diag_mean | 20 | 0.82773 | 0.813891 | 0.842399 |
| T3 | narrow | 14 | 16384 | PQK-1 | 1.0 | off_diag_var | 20 | 0.0339394 | 0.0308761 | 0.0369575 |
| T3 | narrow | 14 | 16384 | PQK-1 | 0.1/n | off_diag_mean | 20 | 0.998417 | 0.998276 | 0.998564 |
| T3 | narrow | 14 | 16384 | PQK-1 | 0.1/n | off_diag_var | 20 | 3.73045e-06 | 3.30985e-06 | 4.15214e-06 |
| T3 | narrow | 14 | 16384 | PQK-1 | 0.3/n | off_diag_mean | 20 | 0.995271 | 0.994848 | 0.99571 |
| T3 | narrow | 14 | 16384 | PQK-1 | 0.3/n | off_diag_var | 20 | 3.31631e-05 | 2.94365e-05 | 3.69029e-05 |
| T3 | narrow | 14 | 16384 | PQK-1 | 1.0/n | off_diag_mean | 20 | 0.984454 | 0.98307 | 0.985887 |
| T3 | narrow | 14 | 16384 | PQK-1 | 1.0/n | off_diag_var | 20 | 0.000353042 | 0.000313971 | 0.000392366 |
| T3 | narrow | 14 | 16384 | PQK-1 | 3.0/n | off_diag_mean | 20 | 0.955145 | 0.951216 | 0.959229 |
| T3 | narrow | 14 | 16384 | PQK-1 | 3.0/n | off_diag_var | 20 | 0.0028192 | 0.00251627 | 0.00312128 |
| T3 | narrow | 14 | 16384 | PQK-1 | 10.0/n | off_diag_mean | 20 | 0.868394 | 0.857479 | 0.879877 |
| T3 | narrow | 14 | 16384 | PQK-1 | 10.0/n | off_diag_var | 20 | 0.0212247 | 0.0192019 | 0.0232294 |
| T3 | narrow | 14 | 16384 | PQK-2nn | 0.1/n | off_diag_mean | 20 | 0.996135 | 0.995792 | 0.996488 |
| T3 | narrow | 14 | 16384 | PQK-2nn | 0.1/n | off_diag_var | 20 | 2.18267e-05 | 1.94255e-05 | 2.42392e-05 |
| T3 | narrow | 14 | 16384 | PQK-2nn | 0.3/n | off_diag_mean | 20 | 0.988515 | 0.987502 | 0.989564 |
| T3 | narrow | 14 | 16384 | PQK-2nn | 0.3/n | off_diag_var | 20 | 0.000190716 | 0.000169896 | 0.000211593 |
| T3 | narrow | 14 | 16384 | PQK-2nn | 1.0/n | off_diag_mean | 20 | 0.962973 | 0.959751 | 0.966321 |
| T3 | narrow | 14 | 16384 | PQK-2nn | 1.0/n | off_diag_var | 20 | 0.00191415 | 0.00171119 | 0.00211681 |
| T3 | narrow | 14 | 16384 | PQK-2nn | 3.0/n | off_diag_mean | 20 | 0.898546 | 0.890043 | 0.907449 |
| T3 | narrow | 14 | 16384 | PQK-2nn | 3.0/n | off_diag_var | 20 | 0.0130747 | 0.0117935 | 0.0143377 |
| T3 | narrow | 14 | 16384 | PQK-2nn | 10.0/n | off_diag_mean | 20 | 0.742329 | 0.723094 | 0.762951 |
| T3 | narrow | 14 | 16384 | PQK-2nn | 10.0/n | off_diag_var | 20 | 0.0642307 | 0.0590692 | 0.0693568 |

## Task 4: Frustrated 2D Lattice (2x4, J1=-1.0)

| task | target | tag | J2 | n | N_train | model | variant | metric | num_seeds | mean | ci_95_lower | ci_95_upper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T4a | sq_argmax | contained | -0.25 | 8 | 6 | baseline_majority | none | accuracy | 20 | 1 | 1 | 1 |
| T4a | sq_argmax | contained | -0.25 | 8 | 6 | baseline_majority | none | balanced_accuracy | 20 | 1 | 1 | 1 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 6 | baseline_mean | none | r2 | 20 | -0.162712 | -0.264865 | -0.0743252 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 6 | baseline_mean | none | mae | 20 | 0.314108 | 0.307787 | 0.320841 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 6 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.741393 | 0.536249 | 0.878299 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 6 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.102378 | 0.0754698 | 0.136922 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 6 | PQK-2nn | none | r2 | 20 | 0.805636 | 0.597481 | 0.944314 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 6 | PQK-2nn | none | mae | 20 | 0.0826478 | 0.0526649 | 0.120635 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 6 | FQ | none | r2 | 20 | 0.900797 | 0.765624 | 0.979981 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 6 | FQ | none | mae | 20 | 0.0555931 | 0.0356657 | 0.0843371 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 6 | E | raw | r2 | 20 | 0.811728 | 0.662113 | 0.93201 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 6 | E | raw | mae | 20 | 0.0815945 | 0.0528837 | 0.113748 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 6 | E | std | r2 | 20 | 0.701621 | 0.544106 | 0.830793 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 6 | E | std | mae | 20 | 0.127514 | 0.103156 | 0.15418 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 6 | F | std | r2 | 20 | 0.213328 | -0.367848 | 0.59527 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 6 | F | std | mae | 20 | 0.194167 | 0.167727 | 0.227623 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 6 | E2 | raw | r2 | 20 | 0.845433 | 0.704061 | 0.948583 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 6 | E2 | raw | mae | 20 | 0.0759086 | 0.0488056 | 0.108053 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 6 | E_X | raw | r2 | 20 | 0.76477 | 0.549841 | 0.920512 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 6 | E_X | raw | mae | 20 | 0.0899764 | 0.0628261 | 0.124402 |
| T4a | sq_argmax | contained | -0.25 | 8 | 10 | baseline_majority | none | accuracy | 20 | 1 | 1 | 1 |
| T4a | sq_argmax | contained | -0.25 | 8 | 10 | baseline_majority | none | balanced_accuracy | 20 | 1 | 1 | 1 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 10 | baseline_mean | none | r2 | 20 | -0.0816438 | -0.119316 | -0.0470907 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 10 | baseline_mean | none | mae | 20 | 0.310256 | 0.305505 | 0.314986 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 10 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.94488 | 0.914593 | 0.96915 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 10 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0477143 | 0.0393245 | 0.0571199 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 10 | PQK-2nn | none | r2 | 20 | 0.968736 | 0.931782 | 0.989729 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 10 | PQK-2nn | none | mae | 20 | 0.0346006 | 0.0262539 | 0.047802 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 10 | FQ | none | r2 | 20 | 0.985296 | 0.982874 | 0.987596 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 10 | FQ | none | mae | 20 | 0.0306849 | 0.0286628 | 0.0327315 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 10 | E | raw | r2 | 20 | 0.974594 | 0.941705 | 0.992041 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 10 | E | raw | mae | 20 | 0.0314298 | 0.0239544 | 0.0443216 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 10 | E | std | r2 | 20 | 0.887141 | 0.829105 | 0.933241 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 10 | E | std | mae | 20 | 0.0798043 | 0.0646033 | 0.0974601 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 10 | F | std | r2 | 20 | 0.708983 | 0.654037 | 0.753983 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 10 | F | std | mae | 20 | 0.143353 | 0.133177 | 0.155163 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 10 | E2 | raw | r2 | 20 | 0.970511 | 0.935818 | 0.989077 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 10 | E2 | raw | mae | 20 | 0.0348417 | 0.0270003 | 0.0479775 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 10 | E_X | raw | r2 | 20 | 0.941722 | 0.898233 | 0.974634 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 10 | E_X | raw | mae | 20 | 0.0455339 | 0.0344944 | 0.0595399 |
| T4a | sq_argmax | contained | -0.25 | 8 | 16 | baseline_majority | none | accuracy | 20 | 1 | 1 | 1 |
| T4a | sq_argmax | contained | -0.25 | 8 | 16 | baseline_majority | none | balanced_accuracy | 20 | 1 | 1 | 1 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 16 | baseline_mean | none | r2 | 20 | -0.0604541 | -0.105121 | -0.0273175 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 16 | baseline_mean | none | mae | 20 | 0.311202 | 0.306229 | 0.316531 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 16 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.990028 | 0.983734 | 0.993564 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 16 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0249283 | 0.0224751 | 0.0287611 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 16 | PQK-2nn | none | r2 | 20 | 0.993056 | 0.992164 | 0.993908 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 16 | PQK-2nn | none | mae | 20 | 0.0235825 | 0.0221711 | 0.0250294 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 16 | FQ | none | r2 | 20 | 0.991913 | 0.990684 | 0.993036 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 16 | FQ | none | mae | 20 | 0.0250574 | 0.0238494 | 0.0262671 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 16 | E | raw | r2 | 20 | 0.994314 | 0.993813 | 0.994758 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 16 | E | raw | mae | 20 | 0.0217622 | 0.0209549 | 0.0227004 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 16 | E | std | r2 | 20 | 0.955779 | 0.938285 | 0.968793 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 16 | E | std | mae | 20 | 0.0522501 | 0.045603 | 0.0601339 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 16 | F | std | r2 | 20 | 0.866522 | 0.821961 | 0.911431 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 16 | F | std | mae | 20 | 0.0867106 | 0.0636624 | 0.108128 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 16 | E2 | raw | r2 | 20 | 0.993214 | 0.992433 | 0.993956 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 16 | E2 | raw | mae | 20 | 0.0237343 | 0.0224952 | 0.0249936 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 16 | E_X | raw | r2 | 20 | 0.992078 | 0.990555 | 0.993338 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 16 | E_X | raw | mae | 20 | 0.0247668 | 0.0230559 | 0.0267417 |
| T4a | sq_argmax | contained | -0.25 | 8 | 24 | baseline_majority | none | accuracy | 20 | 1 | 1 | 1 |
| T4a | sq_argmax | contained | -0.25 | 8 | 24 | baseline_majority | none | balanced_accuracy | 20 | 1 | 1 | 1 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 24 | baseline_mean | none | r2 | 20 | -0.0442571 | -0.0712549 | -0.0222358 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 24 | baseline_mean | none | mae | 20 | 0.310285 | 0.305757 | 0.31493 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 24 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.99372 | 0.992651 | 0.994611 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 24 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0218963 | 0.0207836 | 0.0231216 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 24 | PQK-2nn | none | r2 | 20 | 0.9939 | 0.993283 | 0.994466 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 24 | PQK-2nn | none | mae | 20 | 0.022095 | 0.0213114 | 0.0229569 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 24 | FQ | none | r2 | 20 | 0.992341 | 0.990932 | 0.993488 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 24 | FQ | none | mae | 20 | 0.024361 | 0.0233336 | 0.025477 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 24 | E | raw | r2 | 20 | 0.994122 | 0.993634 | 0.994557 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 24 | E | raw | mae | 20 | 0.0218196 | 0.0211769 | 0.0225164 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 24 | E | std | r2 | 20 | 0.979336 | 0.975441 | 0.982951 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 24 | E | std | mae | 20 | 0.0381529 | 0.0351962 | 0.0411637 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 24 | F | std | r2 | 20 | 0.999695 | 0.999564 | 0.999796 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 24 | F | std | mae | 20 | 0.00340575 | 0.00310453 | 0.00371469 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 24 | E2 | raw | r2 | 20 | 0.993353 | 0.992411 | 0.994089 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 24 | E2 | raw | mae | 20 | 0.0232261 | 0.0222076 | 0.0243395 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 24 | E_X | raw | r2 | 20 | 0.993246 | 0.992107 | 0.9942 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 24 | E_X | raw | mae | 20 | 0.0227197 | 0.0215697 | 0.0240238 |
| T4a | sq_argmax | contained | -0.25 | 8 | 48 | baseline_majority | none | accuracy | 20 | 1 | 1 | 1 |
| T4a | sq_argmax | contained | -0.25 | 8 | 48 | baseline_majority | none | balanced_accuracy | 20 | 1 | 1 | 1 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 48 | baseline_mean | none | r2 | 20 | -0.0191938 | -0.0330572 | -0.00910685 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 48 | baseline_mean | none | mae | 20 | 0.308337 | 0.304028 | 0.312794 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 48 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.995209 | 0.994668 | 0.995605 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 48 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0198954 | 0.0193912 | 0.0204914 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 48 | PQK-2nn | none | r2 | 20 | 0.994705 | 0.994106 | 0.995205 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 48 | PQK-2nn | none | mae | 20 | 0.0210779 | 0.0203178 | 0.0219341 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 48 | FQ | none | r2 | 20 | 0.993907 | 0.992769 | 0.994633 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 48 | FQ | none | mae | 20 | 0.0226863 | 0.0219148 | 0.0236611 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 48 | E | raw | r2 | 20 | 0.995369 | 0.995103 | 0.995611 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 48 | E | raw | mae | 20 | 0.0198382 | 0.0193434 | 0.0203625 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 48 | E | std | r2 | 20 | 0.991091 | 0.990093 | 0.992022 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 48 | E | std | mae | 20 | 0.0261647 | 0.0249543 | 0.0273667 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 48 | F | std | r2 | 20 | 0.999791 | 0.999514 | 0.999942 |
| T4b | half_cut_entropy | not_contained | -0.25 | 8 | 48 | F | std | mae | 20 | 0.00217219 | 0.00180522 | 0.00266793 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 48 | E2 | raw | r2 | 20 | 0.994664 | 0.993833 | 0.995315 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 48 | E2 | raw | mae | 20 | 0.020992 | 0.020056 | 0.0220863 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 48 | E_X | raw | r2 | 20 | 0.994927 | 0.994223 | 0.995459 |
| T4b | half_cut_entropy | sanity | -0.25 | 8 | 48 | E_X | raw | mae | 20 | 0.0203699 | 0.019586 | 0.021235 |
| T4a | sq_argmax | contained | -0.5 | 8 | 6 | baseline_majority | none | accuracy | 20 | 1 | 1 | 1 |
| T4a | sq_argmax | contained | -0.5 | 8 | 6 | baseline_majority | none | balanced_accuracy | 20 | 1 | 1 | 1 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 6 | baseline_mean | none | r2 | 20 | -0.17766 | -0.282227 | -0.0901214 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 6 | baseline_mean | none | mae | 20 | 0.302522 | 0.287122 | 0.320416 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 6 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.89024 | 0.825244 | 0.945332 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 6 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0540701 | 0.041706 | 0.0674984 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 6 | PQK-2nn | none | r2 | 20 | 0.807661 | 0.652047 | 0.931684 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 6 | PQK-2nn | none | mae | 20 | 0.064466 | 0.0445511 | 0.0874359 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 6 | FQ | none | r2 | 20 | 0.881717 | 0.740838 | 0.971944 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 6 | FQ | none | mae | 20 | 0.0521889 | 0.0336518 | 0.0787472 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 6 | E | raw | r2 | 20 | 0.831398 | 0.685405 | 0.946926 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 6 | E | raw | mae | 20 | 0.0586467 | 0.0399645 | 0.0804332 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 6 | E | std | r2 | 20 | 0.554117 | 0.320138 | 0.757125 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 6 | E | std | mae | 20 | 0.134462 | 0.106949 | 0.16391 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 6 | F | std | r2 | 20 | -0.100459 | -1.22457 | 0.598066 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 6 | F | std | mae | 20 | 0.170547 | 0.137924 | 0.216584 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 6 | E2 | raw | r2 | 20 | 0.817206 | 0.682323 | 0.92624 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 6 | E2 | raw | mae | 20 | 0.063376 | 0.0445088 | 0.0845504 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 6 | E_X | raw | r2 | 20 | 0.819574 | 0.691446 | 0.927189 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 6 | E_X | raw | mae | 20 | 0.0647383 | 0.0456762 | 0.0854856 |
| T4a | sq_argmax | contained | -0.5 | 8 | 10 | baseline_majority | none | accuracy | 20 | 1 | 1 | 1 |
| T4a | sq_argmax | contained | -0.5 | 8 | 10 | baseline_majority | none | balanced_accuracy | 20 | 1 | 1 | 1 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 10 | baseline_mean | none | r2 | 20 | -0.101903 | -0.142228 | -0.0681992 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 10 | baseline_mean | none | mae | 20 | 0.297682 | 0.28456 | 0.311534 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 10 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.940084 | 0.885278 | 0.981724 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 10 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0381671 | 0.0285854 | 0.0498379 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 10 | PQK-2nn | none | r2 | 20 | 0.967401 | 0.931807 | 0.988781 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 10 | PQK-2nn | none | mae | 20 | 0.0312406 | 0.0257574 | 0.0383501 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 10 | FQ | none | r2 | 20 | 0.988185 | 0.981769 | 0.992671 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 10 | FQ | none | mae | 20 | 0.0247768 | 0.0216459 | 0.0282985 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 10 | E | raw | r2 | 20 | 0.96815 | 0.936548 | 0.991974 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 10 | E | raw | mae | 20 | 0.0312317 | 0.0241864 | 0.0401795 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 10 | E | std | r2 | 20 | 0.837199 | 0.728633 | 0.922106 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 10 | E | std | mae | 20 | 0.081723 | 0.0682877 | 0.0974951 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 10 | F | std | r2 | 20 | 0.578903 | 0.401677 | 0.726631 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 10 | F | std | mae | 20 | 0.139255 | 0.127024 | 0.151973 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 10 | E2 | raw | r2 | 20 | 0.968427 | 0.942976 | 0.990269 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 10 | E2 | raw | mae | 20 | 0.0307256 | 0.024803 | 0.0377979 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 10 | E_X | raw | r2 | 20 | 0.927224 | 0.834525 | 0.988414 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 10 | E_X | raw | mae | 20 | 0.0375064 | 0.0261647 | 0.0532294 |
| T4a | sq_argmax | contained | -0.5 | 8 | 16 | baseline_majority | none | accuracy | 20 | 1 | 1 | 1 |
| T4a | sq_argmax | contained | -0.5 | 8 | 16 | baseline_majority | none | balanced_accuracy | 20 | 1 | 1 | 1 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 16 | baseline_mean | none | r2 | 20 | -0.0700441 | -0.104599 | -0.0393177 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 16 | baseline_mean | none | mae | 20 | 0.296196 | 0.285511 | 0.307134 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 16 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.973319 | 0.943577 | 0.991332 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 16 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0289829 | 0.0236594 | 0.0361697 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 16 | PQK-2nn | none | r2 | 20 | 0.973725 | 0.938819 | 0.993605 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 16 | PQK-2nn | none | mae | 20 | 0.0273318 | 0.0222261 | 0.0348813 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 16 | FQ | none | r2 | 20 | 0.993471 | 0.991767 | 0.994916 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 16 | FQ | none | mae | 20 | 0.0202945 | 0.0184833 | 0.0221393 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 16 | E | raw | r2 | 20 | 0.984849 | 0.970823 | 0.994661 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 16 | E | raw | mae | 20 | 0.0252909 | 0.0211473 | 0.030507 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 16 | E | std | r2 | 20 | 0.918615 | 0.835081 | 0.977843 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 16 | E | std | mae | 20 | 0.0502296 | 0.0389995 | 0.0643078 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 16 | F | std | r2 | 20 | 0.911725 | 0.879936 | 0.943965 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 16 | F | std | mae | 20 | 0.0637057 | 0.0445611 | 0.0826646 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 16 | E2 | raw | r2 | 20 | 0.977432 | 0.953095 | 0.993932 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 16 | E2 | raw | mae | 20 | 0.026163 | 0.0212741 | 0.0324534 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 16 | E_X | raw | r2 | 20 | 0.987187 | 0.980815 | 0.991991 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 16 | E_X | raw | mae | 20 | 0.0250826 | 0.0232304 | 0.0272167 |
| T4a | sq_argmax | contained | -0.5 | 8 | 24 | baseline_majority | none | accuracy | 20 | 1 | 1 | 1 |
| T4a | sq_argmax | contained | -0.5 | 8 | 24 | baseline_majority | none | balanced_accuracy | 20 | 1 | 1 | 1 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 24 | baseline_mean | none | r2 | 20 | -0.0547397 | -0.0913529 | -0.0247134 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 24 | baseline_mean | none | mae | 20 | 0.293802 | 0.285568 | 0.30181 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 24 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.993222 | 0.991624 | 0.994662 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 24 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0209181 | 0.0193264 | 0.0224928 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 24 | PQK-2nn | none | r2 | 20 | 0.994521 | 0.993218 | 0.995513 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 24 | PQK-2nn | none | mae | 20 | 0.0201347 | 0.0188499 | 0.0213733 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 24 | FQ | none | r2 | 20 | 0.995584 | 0.9949 | 0.996152 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 24 | FQ | none | mae | 20 | 0.0177075 | 0.0164767 | 0.0189496 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 24 | E | raw | r2 | 20 | 0.995101 | 0.994328 | 0.995798 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 24 | E | raw | mae | 20 | 0.0200296 | 0.018719 | 0.021179 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 24 | E | std | r2 | 20 | 0.986265 | 0.983707 | 0.988795 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 24 | E | std | mae | 20 | 0.0313119 | 0.0282345 | 0.0342064 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 24 | F | std | r2 | 20 | 0.993809 | 0.986117 | 0.999318 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 24 | F | std | mae | 20 | 0.0063613 | 0.0033854 | 0.00977561 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 24 | E2 | raw | r2 | 20 | 0.993735 | 0.99084 | 0.995646 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 24 | E2 | raw | mae | 20 | 0.0201392 | 0.0182682 | 0.0221706 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 24 | E_X | raw | r2 | 20 | 0.989277 | 0.984575 | 0.993167 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 24 | E_X | raw | mae | 20 | 0.0233275 | 0.0212814 | 0.0255189 |
| T4a | sq_argmax | contained | -0.5 | 8 | 48 | baseline_majority | none | accuracy | 20 | 1 | 1 | 1 |
| T4a | sq_argmax | contained | -0.5 | 8 | 48 | baseline_majority | none | balanced_accuracy | 20 | 1 | 1 | 1 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 48 | baseline_mean | none | r2 | 20 | -0.0323439 | -0.0572276 | -0.0145205 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 48 | baseline_mean | none | mae | 20 | 0.291986 | 0.285216 | 0.299048 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 48 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.99572 | 0.995001 | 0.996268 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 48 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0178909 | 0.016932 | 0.0190142 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 48 | PQK-2nn | none | r2 | 20 | 0.995858 | 0.995341 | 0.996316 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 48 | PQK-2nn | none | mae | 20 | 0.0184177 | 0.0173485 | 0.0194311 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 48 | FQ | none | r2 | 20 | 0.996531 | 0.9962 | 0.996867 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 48 | FQ | none | mae | 20 | 0.016067 | 0.0151035 | 0.0170145 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 48 | E | raw | r2 | 20 | 0.995796 | 0.995438 | 0.996167 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 48 | E | raw | mae | 20 | 0.0189563 | 0.0180714 | 0.0198265 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 48 | E | std | r2 | 20 | 0.993316 | 0.992493 | 0.994099 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 48 | E | std | mae | 20 | 0.0232579 | 0.0218408 | 0.0246195 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 48 | F | std | r2 | 20 | 0.999543 | 0.998825 | 0.999974 |
| T4b | half_cut_entropy | not_contained | -0.5 | 8 | 48 | F | std | mae | 20 | 0.00229877 | 0.00122951 | 0.00377531 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 48 | E2 | raw | r2 | 20 | 0.996342 | 0.996016 | 0.99668 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 48 | E2 | raw | mae | 20 | 0.0169404 | 0.0160419 | 0.017773 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 48 | E_X | raw | r2 | 20 | 0.995003 | 0.993604 | 0.995857 |
| T4b | half_cut_entropy | sanity | -0.5 | 8 | 48 | E_X | raw | mae | 20 | 0.0193955 | 0.0182138 | 0.020938 |
| T4a | sq_argmax | contained | -0.75 | 8 | 6 | baseline_majority | none | accuracy | 20 | 1 | 1 | 1 |
| T4a | sq_argmax | contained | -0.75 | 8 | 6 | baseline_majority | none | balanced_accuracy | 20 | 1 | 1 | 1 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 6 | baseline_mean | none | r2 | 20 | -0.149715 | -0.253213 | -0.0662123 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 6 | baseline_mean | none | mae | 20 | 0.264072 | 0.253891 | 0.275215 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 6 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.856518 | 0.783678 | 0.920155 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 6 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.06092 | 0.0468735 | 0.0773986 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 6 | PQK-2nn | none | r2 | 20 | 0.916791 | 0.843655 | 0.96925 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 6 | PQK-2nn | none | mae | 20 | 0.0437059 | 0.031024 | 0.0588516 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 6 | FQ | none | r2 | 20 | 0.963017 | 0.927539 | 0.984801 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 6 | FQ | none | mae | 20 | 0.0334579 | 0.0269212 | 0.0428757 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 6 | E | raw | r2 | 20 | 0.847368 | 0.69864 | 0.957278 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 6 | E | raw | mae | 20 | 0.0525347 | 0.0367391 | 0.0726722 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 6 | E | std | r2 | 20 | 0.647722 | 0.456108 | 0.79898 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 6 | E | std | mae | 20 | 0.113217 | 0.0924931 | 0.13821 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 6 | F | std | r2 | 20 | 0.340985 | -0.150531 | 0.654686 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 6 | F | std | mae | 20 | 0.137095 | 0.117259 | 0.168136 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 6 | E2 | raw | r2 | 20 | 0.881297 | 0.745065 | 0.967916 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 6 | E2 | raw | mae | 20 | 0.0520572 | 0.0340822 | 0.0756447 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 6 | E_X | raw | r2 | 20 | 0.866363 | 0.751958 | 0.945066 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 6 | E_X | raw | mae | 20 | 0.0536719 | 0.0408311 | 0.0699235 |
| T4a | sq_argmax | contained | -0.75 | 8 | 10 | baseline_majority | none | accuracy | 20 | 1 | 1 | 1 |
| T4a | sq_argmax | contained | -0.75 | 8 | 10 | baseline_majority | none | balanced_accuracy | 20 | 1 | 1 | 1 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 10 | baseline_mean | none | r2 | 20 | -0.147447 | -0.250169 | -0.0710108 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 10 | baseline_mean | none | mae | 20 | 0.262659 | 0.252926 | 0.27337 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 10 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.919718 | 0.844397 | 0.97799 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 10 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0393867 | 0.0303941 | 0.0505557 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 10 | PQK-2nn | none | r2 | 20 | 0.985101 | 0.9748 | 0.993257 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 10 | PQK-2nn | none | mae | 20 | 0.0232554 | 0.0192171 | 0.0278516 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 10 | FQ | none | r2 | 20 | 0.988013 | 0.981553 | 0.992402 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 10 | FQ | none | mae | 20 | 0.0230911 | 0.0206536 | 0.0257933 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 10 | E | raw | r2 | 20 | 0.964801 | 0.936601 | 0.986003 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 10 | E | raw | mae | 20 | 0.030758 | 0.0251279 | 0.0373465 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 10 | E | std | r2 | 20 | 0.832819 | 0.724306 | 0.921009 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 10 | E | std | mae | 20 | 0.0744887 | 0.0577485 | 0.094938 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 10 | F | std | r2 | 20 | 0.774034 | 0.703891 | 0.829717 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 10 | F | std | mae | 20 | 0.0982308 | 0.0888897 | 0.107177 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 10 | E2 | raw | r2 | 20 | 0.981471 | 0.966358 | 0.992531 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 10 | E2 | raw | mae | 20 | 0.0244877 | 0.0202336 | 0.0296358 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 10 | E_X | raw | r2 | 20 | 0.929649 | 0.867319 | 0.976385 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 10 | E_X | raw | mae | 20 | 0.0394916 | 0.0317511 | 0.0489662 |
| T4a | sq_argmax | contained | -0.75 | 8 | 16 | baseline_majority | none | accuracy | 20 | 1 | 1 | 1 |
| T4a | sq_argmax | contained | -0.75 | 8 | 16 | baseline_majority | none | balanced_accuracy | 20 | 1 | 1 | 1 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 16 | baseline_mean | none | r2 | 20 | -0.0988651 | -0.203872 | -0.0312147 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 16 | baseline_mean | none | mae | 20 | 0.261335 | 0.252408 | 0.271523 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 16 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.987921 | 0.984689 | 0.990855 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 16 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.023927 | 0.0220496 | 0.0259082 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 16 | PQK-2nn | none | r2 | 20 | 0.994135 | 0.992304 | 0.99549 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 16 | PQK-2nn | none | mae | 20 | 0.0187649 | 0.0171966 | 0.020477 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 16 | FQ | none | r2 | 20 | 0.992684 | 0.990934 | 0.994067 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 16 | FQ | none | mae | 20 | 0.0207442 | 0.0192328 | 0.022355 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 16 | E | raw | r2 | 20 | 0.993111 | 0.991208 | 0.994553 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 16 | E | raw | mae | 20 | 0.0204412 | 0.0190885 | 0.02202 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 16 | E | std | r2 | 20 | 0.970739 | 0.960434 | 0.979534 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 16 | E | std | mae | 20 | 0.038102 | 0.0333745 | 0.0434639 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 16 | F | std | r2 | 20 | 0.975328 | 0.950518 | 0.995491 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 16 | F | std | mae | 20 | 0.0205532 | 0.00901086 | 0.034512 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 16 | E2 | raw | r2 | 20 | 0.993793 | 0.992108 | 0.99508 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 16 | E2 | raw | mae | 20 | 0.0190969 | 0.0176747 | 0.020657 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 16 | E_X | raw | r2 | 20 | 0.989019 | 0.98658 | 0.991216 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 16 | E_X | raw | mae | 20 | 0.0237296 | 0.0220243 | 0.0255745 |
| T4a | sq_argmax | contained | -0.75 | 8 | 24 | baseline_majority | none | accuracy | 20 | 1 | 1 | 1 |
| T4a | sq_argmax | contained | -0.75 | 8 | 24 | baseline_majority | none | balanced_accuracy | 20 | 1 | 1 | 1 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 24 | baseline_mean | none | r2 | 20 | -0.045997 | -0.0831959 | -0.02196 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 24 | baseline_mean | none | mae | 20 | 0.258254 | 0.252032 | 0.264434 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 24 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.992254 | 0.989641 | 0.994145 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 24 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0206416 | 0.0193552 | 0.0220829 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 24 | PQK-2nn | none | r2 | 20 | 0.994495 | 0.993803 | 0.995125 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 24 | PQK-2nn | none | mae | 20 | 0.0190436 | 0.0180823 | 0.0200385 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 24 | FQ | none | r2 | 20 | 0.994043 | 0.99327 | 0.994781 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 24 | FQ | none | mae | 20 | 0.0193274 | 0.0182538 | 0.0204197 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 24 | E | raw | r2 | 20 | 0.994699 | 0.994179 | 0.995189 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 24 | E | raw | mae | 20 | 0.0187526 | 0.0179121 | 0.0195433 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 24 | E | std | r2 | 20 | 0.983212 | 0.979369 | 0.986731 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 24 | E | std | mae | 20 | 0.0301223 | 0.0273411 | 0.0330684 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 24 | F | std | r2 | 20 | 0.998867 | 0.997671 | 0.999674 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 24 | F | std | mae | 20 | 0.00349125 | 0.00255006 | 0.00448351 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 24 | E2 | raw | r2 | 20 | 0.994748 | 0.994064 | 0.995424 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 24 | E2 | raw | mae | 20 | 0.0183661 | 0.0172142 | 0.0194996 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 24 | E_X | raw | r2 | 20 | 0.992873 | 0.991162 | 0.994233 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 24 | E_X | raw | mae | 20 | 0.0200016 | 0.0188976 | 0.0211676 |
| T4a | sq_argmax | contained | -0.75 | 8 | 48 | baseline_majority | none | accuracy | 20 | 1 | 1 | 1 |
| T4a | sq_argmax | contained | -0.75 | 8 | 48 | baseline_majority | none | balanced_accuracy | 20 | 1 | 1 | 1 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 48 | baseline_mean | none | r2 | 20 | -0.0332825 | -0.0732156 | -0.0099481 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 48 | baseline_mean | none | mae | 20 | 0.256246 | 0.250824 | 0.261842 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 48 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.995104 | 0.99468 | 0.995505 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 48 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0180193 | 0.017395 | 0.0186332 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 48 | PQK-2nn | none | r2 | 20 | 0.995423 | 0.995024 | 0.99579 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 48 | PQK-2nn | none | mae | 20 | 0.0174656 | 0.0167822 | 0.0181774 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 48 | FQ | none | r2 | 20 | 0.995056 | 0.994604 | 0.995476 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 48 | FQ | none | mae | 20 | 0.0179291 | 0.0172438 | 0.0186279 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 48 | E | raw | r2 | 20 | 0.995289 | 0.994889 | 0.99564 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 48 | E | raw | mae | 20 | 0.0178469 | 0.0173722 | 0.0183402 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 48 | E | std | r2 | 20 | 0.992923 | 0.991949 | 0.993766 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 48 | E | std | mae | 20 | 0.0206794 | 0.0196411 | 0.0219031 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 48 | F | std | r2 | 20 | 0.999954 | 0.999908 | 0.99998 |
| T4b | half_cut_entropy | not_contained | -0.75 | 8 | 48 | F | std | mae | 20 | 0.00111688 | 0.000872369 | 0.00150038 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 48 | E2 | raw | r2 | 20 | 0.995857 | 0.995452 | 0.996218 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 48 | E2 | raw | mae | 20 | 0.0164354 | 0.0157844 | 0.0171279 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 48 | E_X | raw | r2 | 20 | 0.995372 | 0.994845 | 0.995808 |
| T4b | half_cut_entropy | sanity | -0.75 | 8 | 48 | E_X | raw | mae | 20 | 0.0173858 | 0.0168261 | 0.0180819 |

## Task 4: Class Balance Records

| J2 | seed | total_samples | class_counts | decision |
| --- | --- | --- | --- | --- |
| -0.25 | 0 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 0 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 0 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 1 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 1 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 1 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 2 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 2 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 2 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 3 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 3 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 3 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 4 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 4 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 4 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 5 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 5 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 5 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 6 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 6 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 6 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 7 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 7 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 7 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 8 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 8 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 8 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 9 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 9 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 9 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 10 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 10 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 10 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 11 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 11 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 11 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 12 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 12 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 12 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 13 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 13 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 13 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 14 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 14 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 14 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 15 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 15 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 15 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 16 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 16 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 16 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 17 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 17 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 17 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 18 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 18 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 18 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.25 | 19 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.5 | 19 | 248 | {3.14_3.14": 248}" | Single class present ({np.str_('3.14_3.14'): 248}); baseline_majority evaluated, SVC arms skipped |
| -0.75 | 19 | 248 | {3.14_0.00": 248}" | Single class present ({np.str_('3.14_0.00'): 248}); baseline_majority evaluated, SVC arms skipped |
