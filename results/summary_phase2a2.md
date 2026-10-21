# Phase 2a.2 Summary Statistics (10,000 Bootstrap Resamples over Seeds, grid_v2)

## Task 1: Disordered TFIM Half-Chain Entropy (n=8, grid_v2)

| task | target | tag | n | N_train | model | variant | metric | num_seeds | mean | ci_95_lower | ci_95_upper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | half_chain_entropy | not_contained | 8 | 10 | baseline_mean | none | r2 | 20 | -0.178472 | -0.351753 | -0.0687144 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | baseline_mean | none | mae | 20 | 0.200516 | 0.193047 | 0.211704 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.755266 | 0.717104 | 0.791821 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0839562 | 0.0780761 | 0.0900824 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | PQK-2nn | none | r2 | 20 | 0.855332 | 0.807229 | 0.893724 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | PQK-2nn | none | mae | 20 | 0.0641782 | 0.0554604 | 0.0747502 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | FQ | none | r2 | 20 | 0.830324 | 0.738947 | 0.891489 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | FQ | none | mae | 20 | 0.0686184 | 0.0569414 | 0.0837628 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | E | raw | r2 | 20 | 0.833154 | 0.769578 | 0.883225 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | E | raw | mae | 20 | 0.0684026 | 0.0574422 | 0.081236 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | E | std | r2 | 20 | 0.790012 | 0.728031 | 0.832805 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | E | std | mae | 20 | 0.0799084 | 0.0721053 | 0.0899318 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | F | std | r2 | 20 | 0.819151 | 0.785271 | 0.849253 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | F | std | mae | 20 | 0.0750427 | 0.0683073 | 0.0821986 |
| T1 | half_chain_entropy | sanity | 8 | 10 | E2 | raw | r2 | 20 | 0.852039 | 0.80582 | 0.890315 |
| T1 | half_chain_entropy | sanity | 8 | 10 | E2 | raw | mae | 20 | 0.0649116 | 0.0561935 | 0.075239 |
| T1 | half_chain_entropy | sanity | 8 | 10 | E_X | raw | r2 | 20 | 0.755266 | 0.717104 | 0.791821 |
| T1 | half_chain_entropy | sanity | 8 | 10 | E_X | raw | mae | 20 | 0.0839562 | 0.0780761 | 0.0900824 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | PQK-2nn-eps001 | none | r2 | 20 | 0.865352 | 0.832057 | 0.896531 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | PQK-2nn-eps001 | none | mae | 20 | 0.0619051 | 0.0541688 | 0.0703332 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | E-raw-eps001 | raw | r2 | 20 | 0.831041 | 0.772709 | 0.881072 |
| T1 | half_chain_entropy | not_contained | 8 | 10 | E-raw-eps001 | raw | mae | 20 | 0.0680133 | 0.0572089 | 0.0801215 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | baseline_mean | none | r2 | 20 | -0.0440045 | -0.0856722 | -0.0180433 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | baseline_mean | none | mae | 20 | 0.191759 | 0.187991 | 0.195699 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.860534 | 0.841591 | 0.878006 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0639086 | 0.0602814 | 0.0678282 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | PQK-2nn | none | r2 | 20 | 0.95046 | 0.9444 | 0.956048 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | PQK-2nn | none | mae | 20 | 0.0367919 | 0.0348126 | 0.0388925 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | FQ | none | r2 | 20 | 0.961708 | 0.956229 | 0.966634 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | FQ | none | mae | 20 | 0.0336746 | 0.0314141 | 0.0360851 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | E | raw | r2 | 20 | 0.95904 | 0.950996 | 0.966776 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | E | raw | mae | 20 | 0.034042 | 0.0305194 | 0.0375659 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | E | std | r2 | 20 | 0.920531 | 0.903435 | 0.935436 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | E | std | mae | 20 | 0.0486503 | 0.0441348 | 0.0534306 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | F | std | r2 | 20 | 0.92839 | 0.915545 | 0.9393 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | F | std | mae | 20 | 0.0454078 | 0.0415311 | 0.0495962 |
| T1 | half_chain_entropy | sanity | 8 | 20 | E2 | raw | r2 | 20 | 0.952824 | 0.948003 | 0.957404 |
| T1 | half_chain_entropy | sanity | 8 | 20 | E2 | raw | mae | 20 | 0.0359205 | 0.0342144 | 0.0376279 |
| T1 | half_chain_entropy | sanity | 8 | 20 | E_X | raw | r2 | 20 | 0.860534 | 0.841591 | 0.878006 |
| T1 | half_chain_entropy | sanity | 8 | 20 | E_X | raw | mae | 20 | 0.0639086 | 0.0602814 | 0.0678282 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | PQK-2nn-eps001 | none | r2 | 20 | 0.957227 | 0.949645 | 0.964344 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | PQK-2nn-eps001 | none | mae | 20 | 0.0327933 | 0.0301493 | 0.0355078 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | E-raw-eps001 | raw | r2 | 20 | 0.975276 | 0.970886 | 0.979199 |
| T1 | half_chain_entropy | not_contained | 8 | 20 | E-raw-eps001 | raw | mae | 20 | 0.0250349 | 0.0227124 | 0.0275536 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | baseline_mean | none | r2 | 20 | -0.0243195 | -0.0428134 | -0.0095254 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | baseline_mean | none | mae | 20 | 0.190591 | 0.187425 | 0.193533 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.904568 | 0.895461 | 0.913741 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0531663 | 0.0506011 | 0.0557936 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | PQK-2nn | none | r2 | 20 | 0.97169 | 0.968825 | 0.974599 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | PQK-2nn | none | mae | 20 | 0.0271523 | 0.0258052 | 0.0284448 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | FQ | none | r2 | 20 | 0.982621 | 0.981089 | 0.984097 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | FQ | none | mae | 20 | 0.0220876 | 0.0211799 | 0.0230251 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | E | raw | r2 | 20 | 0.980723 | 0.978551 | 0.982593 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | E | raw | mae | 20 | 0.0231116 | 0.0220626 | 0.0242143 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | E | std | r2 | 20 | 0.972087 | 0.968389 | 0.975304 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | E | std | mae | 20 | 0.0286387 | 0.026987 | 0.0303638 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | F | std | r2 | 20 | 0.972755 | 0.966364 | 0.977571 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | F | std | mae | 20 | 0.0261083 | 0.0239032 | 0.0287176 |
| T1 | half_chain_entropy | sanity | 8 | 40 | E2 | raw | r2 | 20 | 0.971483 | 0.968641 | 0.974407 |
| T1 | half_chain_entropy | sanity | 8 | 40 | E2 | raw | mae | 20 | 0.0272527 | 0.0258617 | 0.0285788 |
| T1 | half_chain_entropy | sanity | 8 | 40 | E_X | raw | r2 | 20 | 0.904568 | 0.895461 | 0.913741 |
| T1 | half_chain_entropy | sanity | 8 | 40 | E_X | raw | mae | 20 | 0.0531663 | 0.0506011 | 0.0557936 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | PQK-2nn-eps001 | none | r2 | 20 | 0.978245 | 0.97153 | 0.983318 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | PQK-2nn-eps001 | none | mae | 20 | 0.0222672 | 0.020249 | 0.0245462 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | E-raw-eps001 | raw | r2 | 20 | 0.987017 | 0.984012 | 0.989745 |
| T1 | half_chain_entropy | not_contained | 8 | 40 | E-raw-eps001 | raw | mae | 20 | 0.0167591 | 0.0154265 | 0.0180808 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | baseline_mean | none | r2 | 20 | -0.0108176 | -0.0189806 | -0.00461302 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | baseline_mean | none | mae | 20 | 0.189851 | 0.186654 | 0.192935 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.930728 | 0.922219 | 0.938408 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0443617 | 0.042264 | 0.0467112 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | PQK-2nn | none | r2 | 20 | 0.985253 | 0.983548 | 0.987043 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | PQK-2nn | none | mae | 20 | 0.0197418 | 0.0186342 | 0.0208406 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | FQ | none | r2 | 20 | 0.988385 | 0.98724 | 0.989495 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | FQ | none | mae | 20 | 0.0181936 | 0.0174158 | 0.0189829 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | E | raw | r2 | 20 | 0.98953 | 0.988348 | 0.990585 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | E | raw | mae | 20 | 0.0172405 | 0.0164732 | 0.0180718 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | E | std | r2 | 20 | 0.986231 | 0.984833 | 0.987542 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | E | std | mae | 20 | 0.0197904 | 0.0189934 | 0.0206029 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | F | std | r2 | 20 | 0.984649 | 0.983331 | 0.985948 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | F | std | mae | 20 | 0.0192275 | 0.0183292 | 0.0201516 |
| T1 | half_chain_entropy | sanity | 8 | 80 | E2 | raw | r2 | 20 | 0.985232 | 0.983468 | 0.987061 |
| T1 | half_chain_entropy | sanity | 8 | 80 | E2 | raw | mae | 20 | 0.0196991 | 0.018555 | 0.0208325 |
| T1 | half_chain_entropy | sanity | 8 | 80 | E_X | raw | r2 | 20 | 0.930728 | 0.922219 | 0.938408 |
| T1 | half_chain_entropy | sanity | 8 | 80 | E_X | raw | mae | 20 | 0.0443617 | 0.042264 | 0.0467112 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | PQK-2nn-eps001 | none | r2 | 20 | 0.989964 | 0.988778 | 0.990988 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | PQK-2nn-eps001 | none | mae | 20 | 0.0151837 | 0.0144392 | 0.0159606 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | E-raw-eps001 | raw | r2 | 20 | 0.996101 | 0.995566 | 0.996572 |
| T1 | half_chain_entropy | not_contained | 8 | 80 | E-raw-eps001 | raw | mae | 20 | 0.00954957 | 0.00905615 | 0.0100538 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | baseline_mean | none | r2 | 20 | -0.00819864 | -0.0150711 | -0.00302696 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | baseline_mean | none | mae | 20 | 0.190353 | 0.186922 | 0.193719 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.953732 | 0.951037 | 0.956446 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.037038 | 0.0361023 | 0.0379652 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | PQK-2nn | none | r2 | 20 | 0.99052 | 0.989685 | 0.991354 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | PQK-2nn | none | mae | 20 | 0.0160256 | 0.0153903 | 0.0166571 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | FQ | none | r2 | 20 | 0.992397 | 0.991965 | 0.992851 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | FQ | none | mae | 20 | 0.0148547 | 0.0145206 | 0.0152021 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | E | raw | r2 | 20 | 0.993472 | 0.993098 | 0.993829 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | E | raw | mae | 20 | 0.0140076 | 0.0136579 | 0.0143698 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | E | std | r2 | 20 | 0.991893 | 0.99138 | 0.99238 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | E | std | mae | 20 | 0.0155073 | 0.0151258 | 0.0159075 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | F | std | r2 | 20 | 0.98869 | 0.987807 | 0.989459 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | F | std | mae | 20 | 0.0167566 | 0.0161536 | 0.0174733 |
| T1 | half_chain_entropy | sanity | 8 | 160 | E2 | raw | r2 | 20 | 0.990584 | 0.989672 | 0.991498 |
| T1 | half_chain_entropy | sanity | 8 | 160 | E2 | raw | mae | 20 | 0.0159416 | 0.0152787 | 0.0166104 |
| T1 | half_chain_entropy | sanity | 8 | 160 | E_X | raw | r2 | 20 | 0.953732 | 0.951037 | 0.956446 |
| T1 | half_chain_entropy | sanity | 8 | 160 | E_X | raw | mae | 20 | 0.037038 | 0.0361023 | 0.0379652 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | PQK-2nn-eps001 | none | r2 | 20 | 0.994346 | 0.993557 | 0.995029 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | PQK-2nn-eps001 | none | mae | 20 | 0.0112983 | 0.0106479 | 0.0120445 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | E-raw-eps001 | raw | r2 | 20 | 0.998648 | 0.998499 | 0.99879 |
| T1 | half_chain_entropy | not_contained | 8 | 160 | E-raw-eps001 | raw | mae | 20 | 0.00566351 | 0.00537465 | 0.00595298 |

## Task 2: Ground-State Correlator Prediction (n=8, grid_v2)

| task | target | tag | n | N_train | model | variant | metric | num_seeds | mean | ci_95_lower | ci_95_upper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T2a | z0_zn | contained | 8 | 10 | baseline_mean | none | r2 | 20 | -0.176866 | -0.334108 | -0.0635969 |
| T2a | z0_zn | contained | 8 | 10 | baseline_mean | none | mae | 20 | 0.0742066 | 0.0681191 | 0.0813893 |
| T2a | z0_zn | contained | 8 | 10 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.357478 | 0.225217 | 0.467379 |
| T2a | z0_zn | contained | 8 | 10 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0467792 | 0.0431115 | 0.0507784 |
| T2a | z0_zn | contained | 8 | 10 | PQK-2nn | none | r2 | 20 | 0.348378 | 0.217945 | 0.460281 |
| T2a | z0_zn | contained | 8 | 10 | PQK-2nn | none | mae | 20 | 0.0462096 | 0.0425318 | 0.050254 |
| T2a | z0_zn | contained | 8 | 10 | FQ | none | r2 | 20 | 0.45576 | 0.306601 | 0.5822 |
| T2a | z0_zn | contained | 8 | 10 | FQ | none | mae | 20 | 0.0417529 | 0.0376201 | 0.0463331 |
| T2a | z0_zn | contained | 8 | 10 | E | raw | r2 | 20 | 0.541646 | 0.372399 | 0.682662 |
| T2a | z0_zn | contained | 8 | 10 | E | raw | mae | 20 | 0.0365951 | 0.0318016 | 0.042212 |
| T2a | z0_zn | contained | 8 | 10 | E | std | r2 | 20 | 0.62157 | 0.467522 | 0.74396 |
| T2a | z0_zn | contained | 8 | 10 | E | std | mae | 20 | 0.0341974 | 0.0296853 | 0.039374 |
| T2a | z0_zn | contained | 8 | 10 | F | std | r2 | 20 | 0.7607 | 0.709069 | 0.806769 |
| T2a | z0_zn | contained | 8 | 10 | F | std | mae | 20 | 0.0303831 | 0.0274306 | 0.0334404 |
| T2a | z0_zn | sanity | 8 | 10 | E2 | raw | r2 | 20 | 0.351118 | 0.218046 | 0.466439 |
| T2a | z0_zn | sanity | 8 | 10 | E2 | raw | mae | 20 | 0.046135 | 0.0424187 | 0.0501575 |
| T2a | z0_zn | sanity | 8 | 10 | E_X | raw | r2 | 20 | 0.357478 | 0.225217 | 0.467379 |
| T2a | z0_zn | sanity | 8 | 10 | E_X | raw | mae | 20 | 0.0467792 | 0.0431115 | 0.0507784 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | baseline_mean | none | r2 | 20 | -0.116675 | -0.170914 | -0.068975 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | baseline_mean | none | mae | 20 | 0.090472 | 0.0866829 | 0.0948573 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.419479 | 0.249082 | 0.58027 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0590199 | 0.0500013 | 0.0683111 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | PQK-2nn | none | r2 | 20 | 0.411516 | 0.243545 | 0.570164 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | PQK-2nn | none | mae | 20 | 0.0588622 | 0.0496224 | 0.0683351 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | FQ | none | r2 | 20 | 0.587201 | 0.421845 | 0.730504 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | FQ | none | mae | 20 | 0.0485953 | 0.0400039 | 0.0584762 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | E | raw | r2 | 20 | 0.540448 | 0.357253 | 0.700558 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | E | raw | mae | 20 | 0.051138 | 0.041987 | 0.0613059 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | E | std | r2 | 20 | 0.520078 | 0.387287 | 0.64279 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | E | std | mae | 20 | 0.055966 | 0.0484025 | 0.0639114 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | F | std | r2 | 20 | 0.596708 | 0.498474 | 0.690565 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 10 | F | std | mae | 20 | 0.0522808 | 0.0457006 | 0.0590431 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 10 | E2 | raw | r2 | 20 | 0.381166 | 0.209733 | 0.543025 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 10 | E2 | raw | mae | 20 | 0.0604562 | 0.0513928 | 0.0696806 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 10 | E_X | raw | r2 | 20 | 0.419479 | 0.249082 | 0.58027 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 10 | E_X | raw | mae | 20 | 0.0590199 | 0.0500013 | 0.0683111 |
| T2a | z0_zn | contained | 8 | 20 | baseline_mean | none | r2 | 20 | -0.0528071 | -0.0844546 | -0.0272839 |
| T2a | z0_zn | contained | 8 | 20 | baseline_mean | none | mae | 20 | 0.0700486 | 0.0664852 | 0.0739292 |
| T2a | z0_zn | contained | 8 | 20 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.640822 | 0.56694 | 0.706322 |
| T2a | z0_zn | contained | 8 | 20 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0340565 | 0.0313304 | 0.0368847 |
| T2a | z0_zn | contained | 8 | 20 | PQK-2nn | none | r2 | 20 | 0.615879 | 0.554804 | 0.67079 |
| T2a | z0_zn | contained | 8 | 20 | PQK-2nn | none | mae | 20 | 0.03461 | 0.0324761 | 0.0369077 |
| T2a | z0_zn | contained | 8 | 20 | FQ | none | r2 | 20 | 0.756616 | 0.705531 | 0.798851 |
| T2a | z0_zn | contained | 8 | 20 | FQ | none | mae | 20 | 0.0276119 | 0.0255173 | 0.03007 |
| T2a | z0_zn | contained | 8 | 20 | E | raw | r2 | 20 | 0.849271 | 0.808722 | 0.885497 |
| T2a | z0_zn | contained | 8 | 20 | E | raw | mae | 20 | 0.0212498 | 0.0191805 | 0.0236603 |
| T2a | z0_zn | contained | 8 | 20 | E | std | r2 | 20 | 0.839627 | 0.795803 | 0.874975 |
| T2a | z0_zn | contained | 8 | 20 | E | std | mae | 20 | 0.0225716 | 0.0201862 | 0.0253678 |
| T2a | z0_zn | contained | 8 | 20 | F | std | r2 | 20 | 0.905593 | 0.886177 | 0.924443 |
| T2a | z0_zn | contained | 8 | 20 | F | std | mae | 20 | 0.0194621 | 0.0174853 | 0.0216686 |
| T2a | z0_zn | sanity | 8 | 20 | E2 | raw | r2 | 20 | 0.617929 | 0.553929 | 0.675907 |
| T2a | z0_zn | sanity | 8 | 20 | E2 | raw | mae | 20 | 0.0345033 | 0.0323007 | 0.0368732 |
| T2a | z0_zn | sanity | 8 | 20 | E_X | raw | r2 | 20 | 0.640822 | 0.56694 | 0.706322 |
| T2a | z0_zn | sanity | 8 | 20 | E_X | raw | mae | 20 | 0.0340565 | 0.0313304 | 0.0368847 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | baseline_mean | none | r2 | 20 | -0.0456779 | -0.0757247 | -0.0239571 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | baseline_mean | none | mae | 20 | 0.0875912 | 0.08475 | 0.0908486 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.781777 | 0.755048 | 0.807163 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0362315 | 0.0332036 | 0.0394391 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | PQK-2nn | none | r2 | 20 | 0.866858 | 0.847092 | 0.885561 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | PQK-2nn | none | mae | 20 | 0.0278877 | 0.0258771 | 0.0300934 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | FQ | none | r2 | 20 | 0.861068 | 0.79546 | 0.898899 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | FQ | none | mae | 20 | 0.0277029 | 0.0242701 | 0.0329449 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | E | raw | r2 | 20 | 0.878405 | 0.854532 | 0.897826 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | E | raw | mae | 20 | 0.0273581 | 0.0251427 | 0.0298681 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | E | std | r2 | 20 | 0.824157 | 0.795523 | 0.851767 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | E | std | mae | 20 | 0.0335408 | 0.0308898 | 0.0360786 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | F | std | r2 | 20 | 0.826092 | 0.797368 | 0.85436 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 20 | F | std | mae | 20 | 0.0339241 | 0.0308436 | 0.0370607 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 20 | E2 | raw | r2 | 20 | 0.865603 | 0.844662 | 0.88498 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 20 | E2 | raw | mae | 20 | 0.0280078 | 0.025906 | 0.0303468 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 20 | E_X | raw | r2 | 20 | 0.781777 | 0.755048 | 0.807163 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 20 | E_X | raw | mae | 20 | 0.0362315 | 0.0332036 | 0.0394391 |
| T2a | z0_zn | contained | 8 | 40 | baseline_mean | none | r2 | 20 | -0.0278493 | -0.041996 | -0.0154354 |
| T2a | z0_zn | contained | 8 | 40 | baseline_mean | none | mae | 20 | 0.0709879 | 0.0682339 | 0.0738624 |
| T2a | z0_zn | contained | 8 | 40 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.874274 | 0.850246 | 0.895365 |
| T2a | z0_zn | contained | 8 | 40 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0213644 | 0.0199986 | 0.0227999 |
| T2a | z0_zn | contained | 8 | 40 | PQK-2nn | none | r2 | 20 | 0.839195 | 0.790667 | 0.875581 |
| T2a | z0_zn | contained | 8 | 40 | PQK-2nn | none | mae | 20 | 0.023348 | 0.0216956 | 0.0251392 |
| T2a | z0_zn | contained | 8 | 40 | FQ | none | r2 | 20 | 0.924827 | 0.908539 | 0.937833 |
| T2a | z0_zn | contained | 8 | 40 | FQ | none | mae | 20 | 0.0161316 | 0.0149745 | 0.0172644 |
| T2a | z0_zn | contained | 8 | 40 | E | raw | r2 | 20 | 0.955593 | 0.946106 | 0.963665 |
| T2a | z0_zn | contained | 8 | 40 | E | raw | mae | 20 | 0.0129205 | 0.0119405 | 0.0139289 |
| T2a | z0_zn | contained | 8 | 40 | E | std | r2 | 20 | 0.951244 | 0.939733 | 0.961114 |
| T2a | z0_zn | contained | 8 | 40 | E | std | mae | 20 | 0.0137264 | 0.0124188 | 0.0151118 |
| T2a | z0_zn | contained | 8 | 40 | F | std | r2 | 20 | 0.994461 | 0.990314 | 0.997249 |
| T2a | z0_zn | contained | 8 | 40 | F | std | mae | 20 | 0.00417841 | 0.0032713 | 0.00525739 |
| T2a | z0_zn | sanity | 8 | 40 | E2 | raw | r2 | 20 | 0.843191 | 0.806519 | 0.873024 |
| T2a | z0_zn | sanity | 8 | 40 | E2 | raw | mae | 20 | 0.0232255 | 0.0218019 | 0.02468 |
| T2a | z0_zn | sanity | 8 | 40 | E_X | raw | r2 | 20 | 0.874274 | 0.850246 | 0.895365 |
| T2a | z0_zn | sanity | 8 | 40 | E_X | raw | mae | 20 | 0.0213644 | 0.0199986 | 0.0227999 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | baseline_mean | none | r2 | 20 | -0.0348022 | -0.0563957 | -0.0160471 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | baseline_mean | none | mae | 20 | 0.0882927 | 0.0858402 | 0.0910763 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.880962 | 0.860751 | 0.899387 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0253848 | 0.0236866 | 0.0271603 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | PQK-2nn | none | r2 | 20 | 0.92326 | 0.913887 | 0.933116 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | PQK-2nn | none | mae | 20 | 0.0202777 | 0.0186995 | 0.0217727 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | FQ | none | r2 | 20 | 0.944832 | 0.936869 | 0.952237 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | FQ | none | mae | 20 | 0.0176903 | 0.0165924 | 0.0188813 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | E | raw | r2 | 20 | 0.938024 | 0.931972 | 0.943742 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | E | raw | mae | 20 | 0.019411 | 0.0185122 | 0.0203569 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | E | std | r2 | 20 | 0.90705 | 0.896255 | 0.918402 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | E | std | mae | 20 | 0.0240927 | 0.0226173 | 0.0255792 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | F | std | r2 | 20 | 0.886227 | 0.821988 | 0.925063 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 40 | F | std | mae | 20 | 0.0251257 | 0.0218968 | 0.0297451 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 40 | E2 | raw | r2 | 20 | 0.924816 | 0.91533 | 0.934574 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 40 | E2 | raw | mae | 20 | 0.0200733 | 0.0185873 | 0.0215307 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 40 | E_X | raw | r2 | 20 | 0.880962 | 0.860751 | 0.899387 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 40 | E_X | raw | mae | 20 | 0.0253848 | 0.0236866 | 0.0271603 |
| T2a | z0_zn | contained | 8 | 80 | baseline_mean | none | r2 | 20 | -0.0132264 | -0.0215426 | -0.00658716 |
| T2a | z0_zn | contained | 8 | 80 | baseline_mean | none | mae | 20 | 0.0699301 | 0.0674094 | 0.0725787 |
| T2a | z0_zn | contained | 8 | 80 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.906312 | 0.885271 | 0.92388 |
| T2a | z0_zn | contained | 8 | 80 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0184783 | 0.0174289 | 0.0196808 |
| T2a | z0_zn | contained | 8 | 80 | PQK-2nn | none | r2 | 20 | 0.912844 | 0.898529 | 0.925357 |
| T2a | z0_zn | contained | 8 | 80 | PQK-2nn | none | mae | 20 | 0.0176698 | 0.0169808 | 0.0183185 |
| T2a | z0_zn | contained | 8 | 80 | FQ | none | r2 | 20 | 0.968866 | 0.964072 | 0.972906 |
| T2a | z0_zn | contained | 8 | 80 | FQ | none | mae | 20 | 0.0108036 | 0.0102739 | 0.0113603 |
| T2a | z0_zn | contained | 8 | 80 | E | raw | r2 | 20 | 0.983257 | 0.980509 | 0.985625 |
| T2a | z0_zn | contained | 8 | 80 | E | raw | mae | 20 | 0.00830913 | 0.00790836 | 0.00869314 |
| T2a | z0_zn | contained | 8 | 80 | E | std | r2 | 20 | 0.98289 | 0.980277 | 0.985266 |
| T2a | z0_zn | contained | 8 | 80 | E | std | mae | 20 | 0.00875284 | 0.00821657 | 0.00932611 |
| T2a | z0_zn | contained | 8 | 80 | F | std | r2 | 20 | 1 | 1 | 1 |
| T2a | z0_zn | contained | 8 | 80 | F | std | mae | 20 | 5.49871e-10 | 4.54255e-10 | 6.51033e-10 |
| T2a | z0_zn | sanity | 8 | 80 | E2 | raw | r2 | 20 | 0.914816 | 0.900829 | 0.926988 |
| T2a | z0_zn | sanity | 8 | 80 | E2 | raw | mae | 20 | 0.0175528 | 0.0169158 | 0.0181767 |
| T2a | z0_zn | sanity | 8 | 80 | E_X | raw | r2 | 20 | 0.906312 | 0.885271 | 0.92388 |
| T2a | z0_zn | sanity | 8 | 80 | E_X | raw | mae | 20 | 0.0184783 | 0.0174289 | 0.0196808 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | baseline_mean | none | r2 | 20 | -0.0152682 | -0.0233126 | -0.00814739 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | baseline_mean | none | mae | 20 | 0.0867999 | 0.0849925 | 0.0887704 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.933203 | 0.923085 | 0.942294 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0189001 | 0.0178042 | 0.0199821 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | PQK-2nn | none | r2 | 20 | 0.966059 | 0.957351 | 0.973323 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | PQK-2nn | none | mae | 20 | 0.0134886 | 0.0124321 | 0.0148037 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | FQ | none | r2 | 20 | 0.972527 | 0.966712 | 0.977523 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | FQ | none | mae | 20 | 0.0125108 | 0.0115617 | 0.0135779 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | E | raw | r2 | 20 | 0.967623 | 0.961978 | 0.972675 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | E | raw | mae | 20 | 0.0138562 | 0.0130458 | 0.0147652 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | E | std | r2 | 20 | 0.957019 | 0.950779 | 0.962452 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | E | std | mae | 20 | 0.0161875 | 0.015338 | 0.017194 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | F | std | r2 | 20 | 0.963779 | 0.957038 | 0.969277 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 80 | F | std | mae | 20 | 0.0149047 | 0.0138923 | 0.0161471 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 80 | E2 | raw | r2 | 20 | 0.965853 | 0.957056 | 0.973079 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 80 | E2 | raw | mae | 20 | 0.0135908 | 0.012525 | 0.0149185 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 80 | E_X | raw | r2 | 20 | 0.933203 | 0.923085 | 0.942294 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 80 | E_X | raw | mae | 20 | 0.0189001 | 0.0178042 | 0.0199821 |
| T2a | z0_zn | contained | 8 | 160 | baseline_mean | none | r2 | 20 | -0.0113966 | -0.0187393 | -0.0055127 |
| T2a | z0_zn | contained | 8 | 160 | baseline_mean | none | mae | 20 | 0.0697378 | 0.0670641 | 0.072707 |
| T2a | z0_zn | contained | 8 | 160 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.942096 | 0.93485 | 0.949166 |
| T2a | z0_zn | contained | 8 | 160 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0151184 | 0.0145007 | 0.0157406 |
| T2a | z0_zn | contained | 8 | 160 | PQK-2nn | none | r2 | 20 | 0.955937 | 0.951786 | 0.960266 |
| T2a | z0_zn | contained | 8 | 160 | PQK-2nn | none | mae | 20 | 0.0135963 | 0.0130781 | 0.0141009 |
| T2a | z0_zn | contained | 8 | 160 | FQ | none | r2 | 20 | 0.985502 | 0.983546 | 0.987218 |
| T2a | z0_zn | contained | 8 | 160 | FQ | none | mae | 20 | 0.00789432 | 0.00746213 | 0.00833353 |
| T2a | z0_zn | contained | 8 | 160 | E | raw | r2 | 20 | 0.992624 | 0.991766 | 0.993478 |
| T2a | z0_zn | contained | 8 | 160 | E | raw | mae | 20 | 0.00594773 | 0.00558798 | 0.00632786 |
| T2a | z0_zn | contained | 8 | 160 | E | std | r2 | 20 | 0.992145 | 0.991195 | 0.99305 |
| T2a | z0_zn | contained | 8 | 160 | E | std | mae | 20 | 0.00619515 | 0.00586756 | 0.00653125 |
| T2a | z0_zn | contained | 8 | 160 | F | std | r2 | 20 | 1 | 1 | 1 |
| T2a | z0_zn | contained | 8 | 160 | F | std | mae | 20 | 9.55134e-11 | 8.40902e-11 | 1.07009e-10 |
| T2a | z0_zn | sanity | 8 | 160 | E2 | raw | r2 | 20 | 0.955706 | 0.951441 | 0.960221 |
| T2a | z0_zn | sanity | 8 | 160 | E2 | raw | mae | 20 | 0.0136215 | 0.0130809 | 0.0141617 |
| T2a | z0_zn | sanity | 8 | 160 | E_X | raw | r2 | 20 | 0.942096 | 0.93485 | 0.949166 |
| T2a | z0_zn | sanity | 8 | 160 | E_X | raw | mae | 20 | 0.0151184 | 0.0145007 | 0.0157406 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | baseline_mean | none | r2 | 20 | -0.0112725 | -0.0158214 | -0.00690624 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | baseline_mean | none | mae | 20 | 0.0860142 | 0.084314 | 0.0877908 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.961821 | 0.958062 | 0.965435 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.014616 | 0.0140959 | 0.0151535 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | PQK-2nn | none | r2 | 20 | 0.987203 | 0.985774 | 0.98846 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | PQK-2nn | none | mae | 20 | 0.00881384 | 0.00840258 | 0.00929672 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | FQ | none | r2 | 20 | 0.987974 | 0.98672 | 0.989159 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | FQ | none | mae | 20 | 0.008567 | 0.00819242 | 0.008965 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | E | raw | r2 | 20 | 0.986996 | 0.985768 | 0.988219 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | E | raw | mae | 20 | 0.00907167 | 0.00877538 | 0.00936279 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | E | std | r2 | 20 | 0.97911 | 0.977363 | 0.980788 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | E | std | mae | 20 | 0.0114515 | 0.011095 | 0.0118447 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | F | std | r2 | 20 | 0.975678 | 0.973877 | 0.977557 |
| T2b | z0_z1_zn2_zn1 | not_contained | 8 | 160 | F | std | mae | 20 | 0.0122392 | 0.0118228 | 0.0126474 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 160 | E2 | raw | r2 | 20 | 0.987215 | 0.9858 | 0.988454 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 160 | E2 | raw | mae | 20 | 0.00882032 | 0.00841429 | 0.00929856 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 160 | E_X | raw | r2 | 20 | 0.961821 | 0.958062 | 0.965435 |
| T2b | z0_z1_zn2_zn1 | sanity | 8 | 160 | E_X | raw | mae | 20 | 0.014616 | 0.0140959 | 0.0151535 |

## Task 4 (v2): Frustrated 2D Lattice Benchmark (grid_v2)

| task | target | tag | lattice | boundary | n | N_train | model | variant | metric | num_seeds | mean | ci_95_lower | ci_95_upper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 10 | baseline_majority | none | accuracy | 20 | 0.51775 | 0.481 | 0.55225 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 10 | baseline_majority | none | balanced_accuracy | 20 | 0.5 | 0.5 | 0.5 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 10 | PQK-1 (== RBF on <X>) | none | accuracy | 20 | 0.584 | 0.547494 | 0.62175 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 10 | PQK-1 (== RBF on <X>) | none | balanced_accuracy | 20 | 0.562547 | 0.530993 | 0.597172 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 10 | PQK-2nn | none | accuracy | 20 | 0.679 | 0.629 | 0.732 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 10 | PQK-2nn | none | balanced_accuracy | 20 | 0.657149 | 0.604382 | 0.713684 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 10 | FQ | none | accuracy | 20 | 0.76825 | 0.704 | 0.8325 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 10 | FQ | none | balanced_accuracy | 20 | 0.752083 | 0.680523 | 0.821365 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 10 | E | raw | accuracy | 20 | 0.72325 | 0.66725 | 0.781256 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 10 | E | raw | balanced_accuracy | 20 | 0.707886 | 0.64422 | 0.772934 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 10 | E | std | accuracy | 20 | 0.674 | 0.637244 | 0.71225 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 10 | E | std | balanced_accuracy | 20 | 0.664534 | 0.620316 | 0.707462 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 10 | F | std | accuracy | 20 | 0.694 | 0.6555 | 0.733756 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 10 | F | std | balanced_accuracy | 20 | 0.684993 | 0.641107 | 0.730226 |
| T4a | sq_diff_sign | sanity | 2x4 | open | 8 | 10 | E2 | raw | accuracy | 20 | 0.676 | 0.628744 | 0.725756 |
| T4a | sq_diff_sign | sanity | 2x4 | open | 8 | 10 | E2 | raw | balanced_accuracy | 20 | 0.655692 | 0.604409 | 0.709771 |
| T4a | sq_diff_sign | sanity | 2x4 | open | 8 | 10 | E_X | raw | accuracy | 20 | 0.584 | 0.547494 | 0.62175 |
| T4a | sq_diff_sign | sanity | 2x4 | open | 8 | 10 | E_X | raw | balanced_accuracy | 20 | 0.562547 | 0.530993 | 0.597172 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 10 | baseline_mean | none | r2 | 20 | -0.0755168 | -0.115089 | -0.041451 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 10 | baseline_mean | none | mae | 20 | 0.299635 | 0.291224 | 0.307909 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 10 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.588599 | 0.177094 | 0.823652 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 10 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.102735 | 0.0855769 | 0.126189 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 10 | PQK-2nn | none | r2 | 20 | 0.775095 | 0.654423 | 0.865762 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 10 | PQK-2nn | none | mae | 20 | 0.0887388 | 0.0746976 | 0.103936 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 10 | FQ | none | r2 | 20 | 0.726039 | 0.562783 | 0.846635 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 10 | FQ | none | mae | 20 | 0.101144 | 0.0790451 | 0.130487 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 10 | E | raw | r2 | 20 | 0.753266 | 0.637165 | 0.854984 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 10 | E | raw | mae | 20 | 0.0904584 | 0.0733757 | 0.109359 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 10 | E | std | r2 | 20 | 0.660002 | 0.580491 | 0.728168 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 10 | E | std | mae | 20 | 0.141372 | 0.124927 | 0.161224 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 10 | F | std | r2 | 20 | 0.344767 | 0.161345 | 0.500664 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 10 | F | std | mae | 20 | 0.180587 | 0.170304 | 0.191784 |
| T4b | half_cut_entropy | sanity | 2x4 | open | 8 | 10 | E2 | raw | r2 | 20 | 0.825009 | 0.740002 | 0.889152 |
| T4b | half_cut_entropy | sanity | 2x4 | open | 8 | 10 | E2 | raw | mae | 20 | 0.0790213 | 0.067391 | 0.0927908 |
| T4b | half_cut_entropy | sanity | 2x4 | open | 8 | 10 | E_X | raw | r2 | 20 | 0.588599 | 0.177094 | 0.823652 |
| T4b | half_cut_entropy | sanity | 2x4 | open | 8 | 10 | E_X | raw | mae | 20 | 0.102735 | 0.0855769 | 0.126189 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 20 | baseline_majority | none | accuracy | 20 | 0.52525 | 0.48775 | 0.55825 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 20 | baseline_majority | none | balanced_accuracy | 20 | 0.5 | 0.5 | 0.5 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 20 | PQK-1 (== RBF on <X>) | none | accuracy | 20 | 0.6285 | 0.58375 | 0.67 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 20 | PQK-1 (== RBF on <X>) | none | balanced_accuracy | 20 | 0.61732 | 0.583912 | 0.650091 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 20 | PQK-2nn | none | accuracy | 20 | 0.8655 | 0.826494 | 0.9015 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 20 | PQK-2nn | none | balanced_accuracy | 20 | 0.851738 | 0.805552 | 0.894395 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 20 | FQ | none | accuracy | 20 | 0.93125 | 0.902 | 0.9545 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 20 | FQ | none | balanced_accuracy | 20 | 0.929422 | 0.896259 | 0.954938 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 20 | E | raw | accuracy | 20 | 0.90975 | 0.869744 | 0.944506 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 20 | E | raw | balanced_accuracy | 20 | 0.909874 | 0.86915 | 0.945367 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 20 | E | std | accuracy | 20 | 0.74375 | 0.6995 | 0.785 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 20 | E | std | balanced_accuracy | 20 | 0.740422 | 0.699054 | 0.779168 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 20 | F | std | accuracy | 20 | 0.74525 | 0.699 | 0.78825 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 20 | F | std | balanced_accuracy | 20 | 0.741524 | 0.70057 | 0.780606 |
| T4a | sq_diff_sign | sanity | 2x4 | open | 8 | 20 | E2 | raw | accuracy | 20 | 0.88475 | 0.849 | 0.91825 |
| T4a | sq_diff_sign | sanity | 2x4 | open | 8 | 20 | E2 | raw | balanced_accuracy | 20 | 0.875042 | 0.834881 | 0.912301 |
| T4a | sq_diff_sign | sanity | 2x4 | open | 8 | 20 | E_X | raw | accuracy | 20 | 0.6285 | 0.58375 | 0.67 |
| T4a | sq_diff_sign | sanity | 2x4 | open | 8 | 20 | E_X | raw | balanced_accuracy | 20 | 0.61732 | 0.583912 | 0.650091 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 20 | baseline_mean | none | r2 | 20 | -0.0608747 | -0.108222 | -0.0291649 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 20 | baseline_mean | none | mae | 20 | 0.294971 | 0.287899 | 0.302487 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 20 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.878903 | 0.820967 | 0.919856 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 20 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.062407 | 0.0554754 | 0.0710605 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 20 | PQK-2nn | none | r2 | 20 | 0.921299 | 0.891114 | 0.94611 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 20 | PQK-2nn | none | mae | 20 | 0.0517512 | 0.0440773 | 0.0602007 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 20 | FQ | none | r2 | 20 | 0.919133 | 0.891938 | 0.942677 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 20 | FQ | none | mae | 20 | 0.0550686 | 0.0467873 | 0.0645245 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 20 | E | raw | r2 | 20 | 0.950191 | 0.933611 | 0.96508 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 20 | E | raw | mae | 20 | 0.0412749 | 0.0368116 | 0.0458777 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 20 | E | std | r2 | 20 | 0.849822 | 0.812634 | 0.880919 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 20 | E | std | mae | 20 | 0.0898755 | 0.0791671 | 0.10228 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 20 | F | std | r2 | 20 | 0.704421 | 0.598154 | 0.776926 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 20 | F | std | mae | 20 | 0.12366 | 0.111824 | 0.133703 |
| T4b | half_cut_entropy | sanity | 2x4 | open | 8 | 20 | E2 | raw | r2 | 20 | 0.938983 | 0.923172 | 0.953896 |
| T4b | half_cut_entropy | sanity | 2x4 | open | 8 | 20 | E2 | raw | mae | 20 | 0.046831 | 0.0411345 | 0.0522022 |
| T4b | half_cut_entropy | sanity | 2x4 | open | 8 | 20 | E_X | raw | r2 | 20 | 0.878903 | 0.820967 | 0.919856 |
| T4b | half_cut_entropy | sanity | 2x4 | open | 8 | 20 | E_X | raw | mae | 20 | 0.062407 | 0.0554754 | 0.0710605 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 40 | baseline_majority | none | accuracy | 20 | 0.52525 | 0.48875 | 0.55825 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 40 | baseline_majority | none | balanced_accuracy | 20 | 0.5 | 0.5 | 0.5 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 40 | PQK-1 (== RBF on <X>) | none | accuracy | 20 | 0.72675 | 0.706 | 0.74875 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 40 | PQK-1 (== RBF on <X>) | none | balanced_accuracy | 20 | 0.7049 | 0.679695 | 0.730405 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 40 | PQK-2nn | none | accuracy | 20 | 0.9485 | 0.93425 | 0.9625 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 40 | PQK-2nn | none | balanced_accuracy | 20 | 0.947437 | 0.931932 | 0.962114 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 40 | FQ | none | accuracy | 20 | 0.973 | 0.965 | 0.98075 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 40 | FQ | none | balanced_accuracy | 20 | 0.9729 | 0.964757 | 0.980909 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 40 | E | raw | accuracy | 20 | 0.96775 | 0.9595 | 0.97625 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 40 | E | raw | balanced_accuracy | 20 | 0.966334 | 0.95795 | 0.975073 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 40 | E | std | accuracy | 20 | 0.88675 | 0.869 | 0.90325 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 40 | E | std | balanced_accuracy | 20 | 0.883771 | 0.868006 | 0.899398 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 40 | F | std | accuracy | 20 | 0.92175 | 0.90475 | 0.9365 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 40 | F | std | balanced_accuracy | 20 | 0.917197 | 0.898228 | 0.933471 |
| T4a | sq_diff_sign | sanity | 2x4 | open | 8 | 40 | E2 | raw | accuracy | 20 | 0.95475 | 0.941244 | 0.9675 |
| T4a | sq_diff_sign | sanity | 2x4 | open | 8 | 40 | E2 | raw | balanced_accuracy | 20 | 0.954816 | 0.940458 | 0.968185 |
| T4a | sq_diff_sign | sanity | 2x4 | open | 8 | 40 | E_X | raw | accuracy | 20 | 0.72675 | 0.706 | 0.74875 |
| T4a | sq_diff_sign | sanity | 2x4 | open | 8 | 40 | E_X | raw | balanced_accuracy | 20 | 0.7049 | 0.679695 | 0.730405 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 40 | baseline_mean | none | r2 | 20 | -0.0239724 | -0.0360937 | -0.0139055 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 40 | baseline_mean | none | mae | 20 | 0.293103 | 0.287223 | 0.300235 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 40 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.894521 | 0.804406 | 0.946842 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 40 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0495856 | 0.0432949 | 0.0587477 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 40 | PQK-2nn | none | r2 | 20 | 0.969739 | 0.958831 | 0.979145 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 40 | PQK-2nn | none | mae | 20 | 0.0311277 | 0.0277587 | 0.0347906 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 40 | FQ | none | r2 | 20 | 0.962009 | 0.949668 | 0.972515 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 40 | FQ | none | mae | 20 | 0.0361902 | 0.0321913 | 0.0402162 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 40 | E | raw | r2 | 20 | 0.975376 | 0.96278 | 0.984994 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 40 | E | raw | mae | 20 | 0.029216 | 0.025641 | 0.0332088 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 40 | E | std | r2 | 20 | 0.909607 | 0.893737 | 0.923943 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 40 | E | std | mae | 20 | 0.0669664 | 0.0625164 | 0.0714289 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 40 | F | std | r2 | 20 | 0.919818 | 0.86339 | 0.95592 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 40 | F | std | mae | 20 | 0.0478367 | 0.0400626 | 0.0563752 |
| T4b | half_cut_entropy | sanity | 2x4 | open | 8 | 40 | E2 | raw | r2 | 20 | 0.96852 | 0.956432 | 0.978859 |
| T4b | half_cut_entropy | sanity | 2x4 | open | 8 | 40 | E2 | raw | mae | 20 | 0.0313768 | 0.0276617 | 0.0354125 |
| T4b | half_cut_entropy | sanity | 2x4 | open | 8 | 40 | E_X | raw | r2 | 20 | 0.894521 | 0.804406 | 0.946842 |
| T4b | half_cut_entropy | sanity | 2x4 | open | 8 | 40 | E_X | raw | mae | 20 | 0.0495856 | 0.0432949 | 0.0587477 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 80 | baseline_majority | none | accuracy | 20 | 0.54675 | 0.51325 | 0.575 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 80 | baseline_majority | none | balanced_accuracy | 20 | 0.5 | 0.5 | 0.5 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 80 | PQK-1 (== RBF on <X>) | none | accuracy | 20 | 0.77825 | 0.757 | 0.79925 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 80 | PQK-1 (== RBF on <X>) | none | balanced_accuracy | 20 | 0.761453 | 0.737257 | 0.784711 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 80 | PQK-2nn | none | accuracy | 20 | 0.969 | 0.96025 | 0.977 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 80 | PQK-2nn | none | balanced_accuracy | 20 | 0.967834 | 0.958804 | 0.976278 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 80 | FQ | none | accuracy | 20 | 0.9825 | 0.97575 | 0.98875 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 80 | FQ | none | balanced_accuracy | 20 | 0.981962 | 0.974899 | 0.988424 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 80 | E | raw | accuracy | 20 | 0.98175 | 0.97575 | 0.98725 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 80 | E | raw | balanced_accuracy | 20 | 0.981348 | 0.975381 | 0.986885 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 80 | E | std | accuracy | 20 | 0.9315 | 0.917 | 0.9445 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 80 | E | std | balanced_accuracy | 20 | 0.930098 | 0.914606 | 0.944023 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 80 | F | std | accuracy | 20 | 0.9635 | 0.95525 | 0.9705 |
| T4a | sq_diff_sign | contained | 2x4 | open | 8 | 80 | F | std | balanced_accuracy | 20 | 0.960884 | 0.952288 | 0.968307 |
| T4a | sq_diff_sign | sanity | 2x4 | open | 8 | 80 | E2 | raw | accuracy | 20 | 0.969 | 0.9615 | 0.976 |
| T4a | sq_diff_sign | sanity | 2x4 | open | 8 | 80 | E2 | raw | balanced_accuracy | 20 | 0.967725 | 0.95975 | 0.975371 |
| T4a | sq_diff_sign | sanity | 2x4 | open | 8 | 80 | E_X | raw | accuracy | 20 | 0.77825 | 0.757 | 0.79925 |
| T4a | sq_diff_sign | sanity | 2x4 | open | 8 | 80 | E_X | raw | balanced_accuracy | 20 | 0.761453 | 0.737257 | 0.784711 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 80 | baseline_mean | none | r2 | 20 | -0.0172359 | -0.0333491 | -0.00504779 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 80 | baseline_mean | none | mae | 20 | 0.291834 | 0.286388 | 0.297869 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 80 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.94905 | 0.938728 | 0.958491 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 80 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0391405 | 0.036916 | 0.0413166 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 80 | PQK-2nn | none | r2 | 20 | 0.986727 | 0.98154 | 0.991046 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 80 | PQK-2nn | none | mae | 20 | 0.0218002 | 0.0201129 | 0.0237752 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 80 | FQ | none | r2 | 20 | 0.983828 | 0.977443 | 0.988765 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 80 | FQ | none | mae | 20 | 0.024998 | 0.0230711 | 0.0272398 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 80 | E | raw | r2 | 20 | 0.988969 | 0.983358 | 0.993593 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 80 | E | raw | mae | 20 | 0.0218031 | 0.019632 | 0.0243958 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 80 | E | std | r2 | 20 | 0.952438 | 0.94017 | 0.963212 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 80 | E | std | mae | 20 | 0.0461561 | 0.0425824 | 0.0499865 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 80 | F | std | r2 | 20 | 0.96257 | 0.942514 | 0.976898 |
| T4b | half_cut_entropy | not_contained | 2x4 | open | 8 | 80 | F | std | mae | 20 | 0.0326359 | 0.027754 | 0.039057 |
| T4b | half_cut_entropy | sanity | 2x4 | open | 8 | 80 | E2 | raw | r2 | 20 | 0.986745 | 0.981271 | 0.991202 |
| T4b | half_cut_entropy | sanity | 2x4 | open | 8 | 80 | E2 | raw | mae | 20 | 0.0217625 | 0.0200462 | 0.0236617 |
| T4b | half_cut_entropy | sanity | 2x4 | open | 8 | 80 | E_X | raw | r2 | 20 | 0.94905 | 0.938728 | 0.958491 |
| T4b | half_cut_entropy | sanity | 2x4 | open | 8 | 80 | E_X | raw | mae | 20 | 0.0391405 | 0.036916 | 0.0413166 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 10 | baseline_majority | none | accuracy | 20 | 0.47375 | 0.425 | 0.5225 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 10 | baseline_majority | none | balanced_accuracy | 20 | 0.5 | 0.5 | 0.5 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 10 | PQK-1 (== RBF on <X>) | none | accuracy | 20 | 0.552 | 0.49775 | 0.602 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 10 | PQK-1 (== RBF on <X>) | none | balanced_accuracy | 20 | 0.556106 | 0.531716 | 0.582114 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 10 | PQK-2nn | none | accuracy | 20 | 0.73575 | 0.66625 | 0.803 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 10 | PQK-2nn | none | balanced_accuracy | 20 | 0.749727 | 0.690327 | 0.807693 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 10 | FQ | none | accuracy | 20 | 0.81375 | 0.73075 | 0.88675 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 10 | FQ | none | balanced_accuracy | 20 | 0.828595 | 0.753794 | 0.895734 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 10 | E | raw | accuracy | 20 | 0.78 | 0.7045 | 0.84825 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 10 | E | raw | balanced_accuracy | 20 | 0.796528 | 0.731915 | 0.855798 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 10 | E | std | accuracy | 20 | 0.6875 | 0.62825 | 0.74225 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 10 | E | std | balanced_accuracy | 20 | 0.69588 | 0.64793 | 0.742096 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 10 | F | std | accuracy | 20 | 0.74875 | 0.71475 | 0.78425 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 10 | F | std | balanced_accuracy | 20 | 0.755606 | 0.729592 | 0.785663 |
| T4a | sq_diff_sign | sanity | 3x4 | open | 12 | 10 | E2 | raw | accuracy | 20 | 0.78 | 0.717994 | 0.84125 |
| T4a | sq_diff_sign | sanity | 3x4 | open | 12 | 10 | E2 | raw | balanced_accuracy | 20 | 0.785459 | 0.726973 | 0.842817 |
| T4a | sq_diff_sign | sanity | 3x4 | open | 12 | 10 | E_X | raw | accuracy | 20 | 0.552 | 0.49775 | 0.602 |
| T4a | sq_diff_sign | sanity | 3x4 | open | 12 | 10 | E_X | raw | balanced_accuracy | 20 | 0.556106 | 0.531716 | 0.582114 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 10 | baseline_mean | none | r2 | 20 | -0.0601319 | -0.0929703 | -0.034343 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 10 | baseline_mean | none | mae | 20 | 0.30253 | 0.296038 | 0.309493 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 10 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.576776 | 0.16567 | 0.877101 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 10 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.094236 | 0.071423 | 0.122913 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 10 | PQK-2nn | none | r2 | 20 | 0.672379 | 0.107143 | 0.964682 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 10 | PQK-2nn | none | mae | 20 | 0.0647913 | 0.0431154 | 0.102829 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 10 | FQ | none | r2 | 20 | 0.932057 | 0.885363 | 0.964289 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 10 | FQ | none | mae | 20 | 0.0559607 | 0.0438687 | 0.0728228 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 10 | E | raw | r2 | 20 | 0.874291 | 0.776005 | 0.938201 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 10 | E | raw | mae | 20 | 0.0644869 | 0.0528156 | 0.0769212 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 10 | E | std | r2 | 20 | 0.34161 | -0.52279 | 0.798554 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 10 | E | std | mae | 20 | 0.142493 | 0.114564 | 0.185656 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 10 | F | std | r2 | 20 | -0.193432 | -1.32143 | 0.48101 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 10 | F | std | mae | 20 | 0.216742 | 0.18794 | 0.258733 |
| T4b | half_cut_entropy | sanity | 3x4 | open | 12 | 10 | E2 | raw | r2 | 20 | 0.637058 | 0.0279169 | 0.949795 |
| T4b | half_cut_entropy | sanity | 3x4 | open | 12 | 10 | E2 | raw | mae | 20 | 0.0713928 | 0.0484396 | 0.110931 |
| T4b | half_cut_entropy | sanity | 3x4 | open | 12 | 10 | E_X | raw | r2 | 20 | 0.576776 | 0.16567 | 0.877101 |
| T4b | half_cut_entropy | sanity | 3x4 | open | 12 | 10 | E_X | raw | mae | 20 | 0.094236 | 0.071423 | 0.122913 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 20 | baseline_majority | none | accuracy | 20 | 0.52075 | 0.46775 | 0.569 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 20 | baseline_majority | none | balanced_accuracy | 20 | 0.5 | 0.5 | 0.5 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 20 | PQK-1 (== RBF on <X>) | none | accuracy | 20 | 0.65875 | 0.617494 | 0.70175 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 20 | PQK-1 (== RBF on <X>) | none | balanced_accuracy | 20 | 0.647643 | 0.606607 | 0.689055 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 20 | PQK-2nn | none | accuracy | 20 | 0.8865 | 0.84625 | 0.923256 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 20 | PQK-2nn | none | balanced_accuracy | 20 | 0.888708 | 0.849096 | 0.924864 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 20 | FQ | none | accuracy | 20 | 0.91275 | 0.878 | 0.944 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 20 | FQ | none | balanced_accuracy | 20 | 0.914509 | 0.881768 | 0.944062 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 20 | E | raw | accuracy | 20 | 0.90475 | 0.85625 | 0.94675 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 20 | E | raw | balanced_accuracy | 20 | 0.905794 | 0.858818 | 0.946597 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 20 | E | std | accuracy | 20 | 0.77925 | 0.7285 | 0.82775 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 20 | E | std | balanced_accuracy | 20 | 0.782418 | 0.737982 | 0.827141 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 20 | F | std | accuracy | 20 | 0.76675 | 0.7305 | 0.80225 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 20 | F | std | balanced_accuracy | 20 | 0.76605 | 0.730768 | 0.800898 |
| T4a | sq_diff_sign | sanity | 3x4 | open | 12 | 20 | E2 | raw | accuracy | 20 | 0.89675 | 0.85825 | 0.9305 |
| T4a | sq_diff_sign | sanity | 3x4 | open | 12 | 20 | E2 | raw | balanced_accuracy | 20 | 0.894178 | 0.857628 | 0.926827 |
| T4a | sq_diff_sign | sanity | 3x4 | open | 12 | 20 | E_X | raw | accuracy | 20 | 0.65875 | 0.617494 | 0.70175 |
| T4a | sq_diff_sign | sanity | 3x4 | open | 12 | 20 | E_X | raw | balanced_accuracy | 20 | 0.647643 | 0.606607 | 0.689055 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 20 | baseline_mean | none | r2 | 20 | -0.0426164 | -0.0726867 | -0.017921 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 20 | baseline_mean | none | mae | 20 | 0.299815 | 0.293797 | 0.306255 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 20 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.948597 | 0.936449 | 0.960249 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 20 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0517185 | 0.0466527 | 0.0569775 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 20 | PQK-2nn | none | r2 | 20 | 0.958006 | 0.945028 | 0.969777 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 20 | PQK-2nn | none | mae | 20 | 0.041955 | 0.0374064 | 0.0467122 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 20 | FQ | none | r2 | 20 | 0.976571 | 0.971418 | 0.9809 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 20 | FQ | none | mae | 20 | 0.0359997 | 0.0334726 | 0.0386467 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 20 | E | raw | r2 | 20 | 0.863031 | 0.704184 | 0.971661 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 20 | E | raw | mae | 20 | 0.0464249 | 0.0365712 | 0.0597423 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 20 | E | std | r2 | 20 | 0.89086 | 0.842816 | 0.926494 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 20 | E | std | mae | 20 | 0.0793191 | 0.0689576 | 0.0919087 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 20 | F | std | r2 | 20 | 0.47317 | 0.343211 | 0.568805 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 20 | F | std | mae | 20 | 0.181256 | 0.170489 | 0.193639 |
| T4b | half_cut_entropy | sanity | 3x4 | open | 12 | 20 | E2 | raw | r2 | 20 | 0.95545 | 0.931383 | 0.973274 |
| T4b | half_cut_entropy | sanity | 3x4 | open | 12 | 20 | E2 | raw | mae | 20 | 0.0396891 | 0.0345394 | 0.0452267 |
| T4b | half_cut_entropy | sanity | 3x4 | open | 12 | 20 | E_X | raw | r2 | 20 | 0.948597 | 0.936449 | 0.960249 |
| T4b | half_cut_entropy | sanity | 3x4 | open | 12 | 20 | E_X | raw | mae | 20 | 0.0517185 | 0.0466527 | 0.0569775 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 40 | baseline_majority | none | accuracy | 20 | 0.54425 | 0.49375 | 0.58825 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 40 | baseline_majority | none | balanced_accuracy | 20 | 0.5 | 0.5 | 0.5 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 40 | PQK-1 (== RBF on <X>) | none | accuracy | 20 | 0.80425 | 0.7745 | 0.832 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 40 | PQK-1 (== RBF on <X>) | none | balanced_accuracy | 20 | 0.786612 | 0.753417 | 0.817465 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 40 | PQK-2nn | none | accuracy | 20 | 0.95125 | 0.9325 | 0.96775 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 40 | PQK-2nn | none | balanced_accuracy | 20 | 0.948762 | 0.925394 | 0.968615 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 40 | FQ | none | accuracy | 20 | 0.96625 | 0.9515 | 0.97975 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 40 | FQ | none | balanced_accuracy | 20 | 0.967044 | 0.952421 | 0.980467 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 40 | E | raw | accuracy | 20 | 0.95825 | 0.93425 | 0.97825 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 40 | E | raw | balanced_accuracy | 20 | 0.960621 | 0.939047 | 0.979117 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 40 | E | std | accuracy | 20 | 0.8765 | 0.85375 | 0.89925 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 40 | E | std | balanced_accuracy | 20 | 0.872348 | 0.84943 | 0.89611 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 40 | F | std | accuracy | 20 | 0.88825 | 0.86775 | 0.90875 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 40 | F | std | balanced_accuracy | 20 | 0.884408 | 0.858646 | 0.907179 |
| T4a | sq_diff_sign | sanity | 3x4 | open | 12 | 40 | E2 | raw | accuracy | 20 | 0.948 | 0.925 | 0.96725 |
| T4a | sq_diff_sign | sanity | 3x4 | open | 12 | 40 | E2 | raw | balanced_accuracy | 20 | 0.945869 | 0.921298 | 0.966995 |
| T4a | sq_diff_sign | sanity | 3x4 | open | 12 | 40 | E_X | raw | accuracy | 20 | 0.80425 | 0.7745 | 0.832 |
| T4a | sq_diff_sign | sanity | 3x4 | open | 12 | 40 | E_X | raw | balanced_accuracy | 20 | 0.786612 | 0.753417 | 0.817465 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 40 | baseline_mean | none | r2 | 20 | -0.0215091 | -0.0358247 | -0.00990287 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 40 | baseline_mean | none | mae | 20 | 0.299035 | 0.293559 | 0.304596 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 40 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.975788 | 0.971539 | 0.979633 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 40 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0364232 | 0.034326 | 0.038669 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 40 | PQK-2nn | none | r2 | 20 | 0.987904 | 0.985662 | 0.989864 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 40 | PQK-2nn | none | mae | 20 | 0.0252587 | 0.0241005 | 0.0263948 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 40 | FQ | none | r2 | 20 | 0.987069 | 0.9834 | 0.989995 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 40 | FQ | none | mae | 20 | 0.0267796 | 0.0250104 | 0.0289954 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 40 | E | raw | r2 | 20 | 0.986635 | 0.982894 | 0.98988 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 40 | E | raw | mae | 20 | 0.0262448 | 0.0241117 | 0.0286231 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 40 | E | std | r2 | 20 | 0.958765 | 0.952105 | 0.964579 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 40 | E | std | mae | 20 | 0.0496511 | 0.0470762 | 0.0525631 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 40 | F | std | r2 | 20 | 0.886068 | 0.712358 | 0.983562 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 40 | F | std | mae | 20 | 0.0264483 | 0.0174144 | 0.0408286 |
| T4b | half_cut_entropy | sanity | 3x4 | open | 12 | 40 | E2 | raw | r2 | 20 | 0.97814 | 0.958486 | 0.989122 |
| T4b | half_cut_entropy | sanity | 3x4 | open | 12 | 40 | E2 | raw | mae | 20 | 0.0285708 | 0.0247786 | 0.0344773 |
| T4b | half_cut_entropy | sanity | 3x4 | open | 12 | 40 | E_X | raw | r2 | 20 | 0.975788 | 0.971539 | 0.979633 |
| T4b | half_cut_entropy | sanity | 3x4 | open | 12 | 40 | E_X | raw | mae | 20 | 0.0364232 | 0.034326 | 0.038669 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 80 | baseline_majority | none | accuracy | 20 | 0.58475 | 0.54775 | 0.6155 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 80 | baseline_majority | none | balanced_accuracy | 20 | 0.5 | 0.5 | 0.5 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 80 | PQK-1 (== RBF on <X>) | none | accuracy | 20 | 0.897 | 0.874244 | 0.91575 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 80 | PQK-1 (== RBF on <X>) | none | balanced_accuracy | 20 | 0.88338 | 0.850843 | 0.908451 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 80 | PQK-2nn | none | accuracy | 20 | 0.9695 | 0.9615 | 0.97725 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 80 | PQK-2nn | none | balanced_accuracy | 20 | 0.969853 | 0.96045 | 0.978289 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 80 | FQ | none | accuracy | 20 | 0.97675 | 0.9705 | 0.98275 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 80 | FQ | none | balanced_accuracy | 20 | 0.978087 | 0.971265 | 0.984204 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 80 | E | raw | accuracy | 20 | 0.97625 | 0.9705 | 0.982 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 80 | E | raw | balanced_accuracy | 20 | 0.976044 | 0.969555 | 0.982183 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 80 | E | std | accuracy | 20 | 0.9275 | 0.91425 | 0.9395 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 80 | E | std | balanced_accuracy | 20 | 0.927033 | 0.911291 | 0.940967 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 80 | F | std | accuracy | 20 | 0.94975 | 0.9425 | 0.95725 |
| T4a | sq_diff_sign | contained | 3x4 | open | 12 | 80 | F | std | balanced_accuracy | 20 | 0.948102 | 0.938405 | 0.958132 |
| T4a | sq_diff_sign | sanity | 3x4 | open | 12 | 80 | E2 | raw | accuracy | 20 | 0.97 | 0.96075 | 0.978 |
| T4a | sq_diff_sign | sanity | 3x4 | open | 12 | 80 | E2 | raw | balanced_accuracy | 20 | 0.970067 | 0.960152 | 0.978827 |
| T4a | sq_diff_sign | sanity | 3x4 | open | 12 | 80 | E_X | raw | accuracy | 20 | 0.897 | 0.874244 | 0.91575 |
| T4a | sq_diff_sign | sanity | 3x4 | open | 12 | 80 | E_X | raw | balanced_accuracy | 20 | 0.88338 | 0.850843 | 0.908451 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 80 | baseline_mean | none | r2 | 20 | -0.0138951 | -0.0315457 | -0.00333354 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 80 | baseline_mean | none | mae | 20 | 0.29958 | 0.294088 | 0.305364 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 80 | PQK-1 (== RBF on <X>) | none | r2 | 20 | 0.985826 | 0.981547 | 0.989181 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 80 | PQK-1 (== RBF on <X>) | none | mae | 20 | 0.0266852 | 0.0250805 | 0.02821 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 80 | PQK-2nn | none | r2 | 20 | 0.992655 | 0.990478 | 0.994341 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 80 | PQK-2nn | none | mae | 20 | 0.0199923 | 0.0190756 | 0.0210202 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 80 | FQ | none | r2 | 20 | 0.993474 | 0.992278 | 0.994309 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 80 | FQ | none | mae | 20 | 0.0216706 | 0.0210725 | 0.0223258 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 80 | E | raw | r2 | 20 | 0.992744 | 0.991093 | 0.994041 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 80 | E | raw | mae | 20 | 0.0209421 | 0.0200155 | 0.021853 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 80 | E | std | r2 | 20 | 0.981405 | 0.979357 | 0.983408 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 80 | E | std | mae | 20 | 0.0334667 | 0.0315262 | 0.035414 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 80 | F | std | r2 | 20 | 0.978708 | 0.953684 | 0.996021 |
| T4b | half_cut_entropy | not_contained | 3x4 | open | 12 | 80 | F | std | mae | 20 | 0.0116294 | 0.00875428 | 0.0155378 |
| T4b | half_cut_entropy | sanity | 3x4 | open | 12 | 80 | E2 | raw | r2 | 20 | 0.9932 | 0.991744 | 0.9944 |
| T4b | half_cut_entropy | sanity | 3x4 | open | 12 | 80 | E2 | raw | mae | 20 | 0.0199396 | 0.018988 | 0.0209204 |
| T4b | half_cut_entropy | sanity | 3x4 | open | 12 | 80 | E_X | raw | r2 | 20 | 0.985826 | 0.981547 | 0.989181 |
| T4b | half_cut_entropy | sanity | 3x4 | open | 12 | 80 | E_X | raw | mae | 20 | 0.0266852 | 0.0250805 | 0.02821 |

