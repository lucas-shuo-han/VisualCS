# Coverage: CS182 Optimization notes -> episodes

Caption numbers are the `captions.py` numbers of each episode (`E<ep>.<n>`; `end.N` are the end-card bullets, in order). Sources: Note 2 (`02a_LeastSquares_Ridge.pdf`), Note 3 (`02b_gd_sgd.pdf`), Note 4 (`03_momentum_adam.pdf`), iPad Lecture 2 (`02_fa26.pdf`) and Lecture 3 (`03_fa26.pdf`).

## Note 2: least squares, ridge, implicit regularization
| Item | Where |
|---|---|
| Least squares loss, gradient 2X^T(Xw-y), gradient step | E1.1-E1.3 |
| Step as a linear map plus a constant; error map; linear dynamical system | E1.4-E1.6 |
| Eigenbasis of X^T X decouples into scalar problems; factor r = 1 - 2 eta lambda | E1.7-E1.11 |
| Two-direction ravine, eta below 1/lambda_max, optimal eta = 1/(lambda_max + lambda_min) | E1.12-E1.16, end.1-end.3 |
| Condition number kappa, rate (kappa-1)/(kappa+1), iterations grow with kappa | E1.17-E1.21, end.4 |
| Overparameterized least squares: row space, null space, fundamental theorem | E2.1-E2.4 |
| Updates stay in the row space, null part of the start is frozen | E2.5-E2.6, end.2 |
| Minimum-norm solution X^T(XX^T)^{-1}y, Pythagoras 25 = 5 + 20 | E2.7-E2.9, end.3 |
| Non-zero start lands at w_min + P_null w_0 (initialization matters) | E2.10-E2.13, end.4 |
| SVD-basis view, per-coordinate rates, null coordinate never moves | E2.14-E2.15 |
| Ridge objective and closed form, d x d versus n x n inverse | E3.1-E3.3, end.1 |
| Ridge per singular direction: sigma/(sigma^2+lambda), filter sigma^2/(sigma^2+lambda) | E3.4-E3.7, end.2 |
| Multiplier cap 1/(2 sqrt(lambda)), no blow-up (own addition, follows from the formula) | E3.8-E3.9, end.3 |
| Ridge improves conditioning (eigenvalues sigma^2 + lambda) | E3.10-E3.12 |
| Noise amplification in weak directions, overfitting as trusting weak directions | E3.13-E3.17 |
| Ridge in gradient descent equals weight decay (1 - 2 eta lambda) | E3.18-E3.19, end.4 |
| Probabilistic (MAP, Gaussian prior) view of ridge | E3.20 |
| Lambda cannot be learned by minimizing the training objective | E3.21 |
| Lambda is a hyperparameter chosen on held-out data | E3.22, E4.15-E4.17 |
| Early stopping as a filter q_t = 1 - (1 - 2 eta sigma^2)^t | E4.1-E4.5 |
| Early stopping versus ridge; "same lesson, not the same estimator" | E4.6-E4.7 |
| Caveat: ordering guaranteed only for eta <= 1/(2 sigma_max^2) | E4.8-E4.9 |
| When to stop, U-shaped error, validation-based checkpoint | E4.10-E4.14 |
| Hyperparameters, log scales, train/validation/test roles | E4.15-E4.17 |
| Grid versus random/adaptive search, cost 5^m | E4.18-E4.19 |
| "Superstition" (borrow settings), meta-learning | E4.20-E4.21 |
| Broken "Figure ??" references (two) | Omitted: no content behind them; see notes errors in the report |

## Note 3: gradient descent and SGD
| Item | Where |
|---|---|
| Finite-sum objective, cost of the full gradient | E5.1 |
| Mini-batch gradient is an unbiased estimate; six-gradient enumeration (own numbers) | E5.2-E5.5, end.1-end.2 |
| Intuition figure (noise escaping or falling into valleys) | E5.6-E5.8 (as a sketch, not the notes' figure) |
| Interpolating least squares setting (d > n, rank X = n, zero start) | E5.9-E5.10 |
| One-step identity for ||q_{t+1}||^2 and bound with rho = max ||x_i|| | E5.11-E5.13 |
| Expectation over the sampled example, sigma_min, contraction alpha, eta < 1/rho^2 | E5.14-E5.15, end.4 |
| Numeric check of alpha and Monte Carlo of the bound | E5.16-E5.17 |
| Why a constant step works: zero gradient at every example at the solution | E5.18, end.3 |
| Limits: noisy labels leave a neighborhood; strict decrease alone is not enough | E5.19-E5.20 |
| Recap paragraph (momentum bullets belong to Note 4) | Omitted: repeats content and mis-attributes Note 4 |
| Bottou and Ma et al. references, reading list | Omitted: bibliography only |
| Non-quadratic and general convex SGD rates | Omitted: the notes give no derivation; out of scope for a 5-minute episode |

## Note 4: momentum, Adam, AdamW
| Item | Where |
|---|---|
| Motivation: conditioning trade-off of a single step size | E6.1-E6.2 |
| Momentum as exponential moving average, unrolled weights | E6.3-E6.6, end.1 |
| RC-circuit / low-pass analogy | E6.7-E6.9 |
| Persistent versus alternating gradient, gain (1-beta)/(1+beta) | E6.10-E6.13, end.2-end.3 |
| Two conventions (z normalized, v unnormalized), rate matching | E6.14-E6.16, end.4 |
| Ravine with and without momentum; caution that filtering is not a speed-up proof | E6.17-E6.19, end.5 |
| Scalar quadratic mode as a 2x2 linear system; recurrence with a, s | E7.1-E7.3 |
| Schur stability test, 0 < s < 2(1+beta), range 19x wider at beta 0.9 | E7.4-E7.7, end.2 |
| Root motion: overdamped, critical, underdamped (size sqrt(beta)), negative roots | E7.8-E7.12, end.3 |
| Three regimes over time, envelope sqrt(beta)^t | E7.13-E7.15 |
| One eta, many curvatures; minimax tuning; rate (sqrt(kappa)-1)/(sqrt(kappa)+1) | E7.16-E7.21, end.4 |
| Note's claim "overdamped: both roots real and positive" | E7.9 says it for small s; the real-negative regime near the edge is shown in E7.12 (the notes' Fig 4.2 shows it too, the text omits it) |
| Nesterov momentum | E7.22-E7.24, end.5 |
| Why normalize per coordinate (SVD fix is too costly) | E8.1-E8.3 |
| SignSGD, first-moment / second-moment reading of Adam | E8.4-E8.7, end.2 |
| Adam: two averages, bias correction | E8.8-E8.12, end.3 |
| Adam versus SignSGD in the ravine; "not fully understood" | E8.13-E8.15, end.2 |
| AdamW versus L2 in Adam, lambda_wd convention | E8.16-E8.20, end.4 |
| Optimizer comparison, ledger, extra state | E8.21-E8.23, end.5 |
| Memory savings by quantized optimizer state | Mentioned only as "optimizer-state counts, not a full memory budget" (E8.22); no derivation in the notes |
| Fig 4.4 (garbled caption in the PDF) | Omitted: the redraw in E7 replaces it |
| Reading list, historical arc (Polyak, Nesterov, Kingma) | Omitted: bibliographic |

## Lectures 2 and 3 (iPad)
| Item | Where |
|---|---|
| L2: GD on least squares, eta bounds, rate | E1 (all); the pink margin note "eta < 1/lambda_min" is a typo for lambda_max, corrected in E1.15 |
| L2: overparameterized, min-norm | E2 (all) |
| L2/L3: ridge, weight decay | E3.18-E3.19 (convention with factor 2, unlike the L3 half-loss) |
| L3: early stopping, hyperparameter selection | E4 |
| L3: standardize inputs, conditioning example [100, 200] | E9.1-E9.4, end.1 |
| L3: numerical issues of unscaled data | E9.2 |
| L3: ReLU kink at -b/w is Cauchy, 0.16% inside [100, 200] | E9.5-E9.9, end.2 |
| L3: rank of the feature matrix as a debugging check | E9.10-E9.12, end.3 |
| L3: initialization, all zeros, unit-variance layer input, Xavier | E9.13-E9.16, end.4 |
| L3: He and Glorot, depth experiment (own addition), biases | E9.17-E9.22 |
| L3: half-loss convention (stable for eta < 2/sigma^2) | Omitted: the series uses the notes' factor-2 convention throughout |
| L3: normalization layers (batch/layer norm) | Omitted: belongs to a later unit (scaling); glossary keeps "normalize" for that unit |
