# Series glossary (preferred forms), CS182 · Optimization

Captions are spoken, so Greek letters are written as words in captions and end-card bullets (eta, lambda, kappa, sigma, rho, alpha, beta); symbols stay on screen.

| Preferred term | Meaning / note | Avoid |
|---|---|---|
| gradient descent | full-gradient update w_{t+1} = w_t - eta grad | "steepest descent", "batch GD" |
| learning rate eta ("eta") | the step size | "step length", "alpha" (only in the unnormalized momentum form) |
| least squares, residual | squared length of X w - y, and X w - y | "error vector" |
| eigenvalue lambda of X^T X | curvature of a direction (Ep 1-2, 7) | mixing with the ridge lambda: say "ridge lambda" when both appear |
| singular value sigma | of X; curvature is sigma squared (Ep 1-4) | "eigenvalue of X" |
| condition number kappa | largest over smallest eigenvalue | "ill-conditioning ratio" |
| contraction factor / rate r, rho | per-step multiplier on the error | "decay constant" |
| row space / null space | Row(X), Null(X) | "span of the data" |
| minimum-norm solution | w_min = X^T (X X^T)^{-1} y | "smallest solution", "sparse solution" |
| interpolate / interpolating solution | fits every example exactly | "overfit" for this meaning |
| SVD basis | coordinates along right singular vectors | "diagonalizing basis" |
| ridge regression, ridge lambda | penalty lambda times the squared weight norm | "L2 regularization" only as the alias in Ep 8 |
| filter (ridge filter, early-stopping filter q_t) | per-singular-direction multiplier | "shrinkage factor" |
| early stopping | stop gradient descent before convergence | "premature stopping" |
| hyperparameter | lambda, eta, beta, stopping time; chosen on validation data | "setting", "knob" only in the episode title |
| validation set / test set / training set | as in Unit 1 | "dev set" |
| mini-batch, batch size b | a random subset of examples | "minibatch" |
| unbiased (gradient estimate) | expectation equals the full gradient | "correct", "accurate" |
| SGD | stochastic gradient descent, spoken "S G D" | |
| mean-square convergence | E of squared distance to the solution goes to 0 | "convergence in probability" |
| momentum, first moment m (Adam), average z | exponential moving average of gradients | "velocity" only for the unnormalized v |
| low-pass filter | keeps slow changes, damps fast ones | "smoothing" alone |
| normalized / unnormalized convention | z with a (1 - beta) prefactor, versus v without it | "Polyak vs Nesterov form" |
| damping regimes: overdamped, critical, underdamped | by the discriminant a^2 - 4 beta | |
| s = eta (1 - beta) lambda | the single number that decides a momentum mode | "effective learning rate" |
| Schur stability test | p(1) > 0, p(-1) > 0, abs(beta) < 1 | "Jury test" |
| Nesterov momentum | gradient at the look-ahead point | |
| SignSGD | update by the sign of each gradient coordinate | "sign descent" |
| Adam, second moment v, bias correction | m and v both averaged, then divided by 1 - beta^t | "RMSProp" |
| AdamW, decoupled weight decay | shrink weights separately; lambda_wd inside 1 - eta lambda_wd | "L2 in Adam" |
| standardize | zero mean, unit variance per feature | "normalize" (kept for RMS/layer norm in the scaling unit) |
| kink (ReLU corner), Cauchy distribution | the point -b/w; heavy-tailed | "knot" here (Unit 1 word for spline knots; notes use "corner") |
| Xavier / He / Glorot initialization | N(0, 1/d), N(0, 2/d), N(0, 2/(d_in + d_out)) | "LeCun" |
| fan-in | number of inputs d of a unit | "input width" |

## Terms used inconsistently in the notes (resolved here)
- Note 2 uses lambda for ridge strength; Note 4 uses lambda both for the Hessian eigenvalue and, as lambda_wd, for decay. Episodes say "ridge lambda", "eigenvalue lambda" and "lambda w d".
- The notes call the momentum average z (normalized) and v (unnormalized), while Adam calls its averages m and v. Ep 6 to 7 use z and v; Ep 8 uses m and v (v = second moment).
- "Corner" (Lecture 3) and "knot" or "elbow" (Note 1) name the same bend; Ep 9 says kink.
