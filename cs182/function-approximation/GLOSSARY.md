# Series glossary (preferred forms)

| Preferred term | Meaning / note | Avoid |
|---|---|---|
| target function f | the unknown function that generates the data | "true function", "ground truth" |
| sample, sample pair (x, y) | one noisy observation of f | "example", "data point" in narration |
| training set | samples used to fit | "train data" |
| model N_theta ("N of theta") | the parameterized function | |
| parameters | learned by the optimizer: weights and biases | "params", "coefficients" |
| hyperparameters | chosen by the engineer with validation data (lambda, learning rate, number of hidden units) | "settings" |
| interpolate / extrapolate | between / beyond the samples | |
| step (hard step) | unit step, zero derivative almost everywhere | "threshold" |
| ramp | one ReLU of an affine function, ReLU(w x + b) | |
| ReLU | max(0, z) | "rectifier" after Ep 2 |
| knot | where a ramp bends, x = -b/w (the note's word, Eq 1.6) | "elbow", "kink" |
| slope change | s_i - s_(i-1), the coefficient on each ramp | |
| continuous piecewise-linear function (spline) | | "polyline" |
| hidden unit | one ramp inside the layer (Ep 3+) | "neuron" |
| pre-activation z / activation h | before / after ReLU | |
| affine map | W x + b | "linear layer" |
| one-hidden-layer network | Eq 1.7 | "shallow net" |
| loss | per-example penalty | |
| empirical risk | average loss on training set | |
| population risk | expected loss under P(x, y); the real target | "true risk" |
| training surrogate | differentiable stand-in for the metric | "proxy" only in the "looking where the light is" line |
| evaluation metric | what we measure (accuracy, AUC) | |
| update estimator | how an update is computed | |
| validation set / test set | choices / one-time final check | "dev set" |
| fresh data | data the model has not been trained on | "unseen data", "new data" |
| overfitting | good on training data, poor on new data | |
| regularization, ridge regression, lambda | | |
| distribution shift | | "dataset shift" |
| leakage | same entity on both sides of a split | |
| split at the unit that will be new in deployment | | "group split" |
| AUC | spell out once as area under the ROC curve (Ep 5) | |
| supervised / unsupervised / foundation model | Fig 1.7 vocabulary | |
| density estimation | one route to generation, not its definition | |

## Terms used inconsistently in captions

1. elbow / kink / knot: E2.2 and E2.9 "elbow", E2.5-E2.6 "kink"; the note's Eq 1.6 says "knots". Resolved: use "knot".
2. new data: E1.18 "unseen data", E4.10-11 "fresh data", E4.13 "new data". Resolved: use "fresh data".
3. ramp / unit / hidden unit: E2.12-13 "unit(s)/hidden units", E3.4-8 "ramps" and "unit", E3.16 "units". E3.4 should say once "each ramp is a hidden unit".
4. error / loss / risk: E1.6 "error", E1.8 "loss", E4.6 "empirical risk", E4.11-13 "training error", "error on new data". Tie error (plots) to risk (definition) once in Ep 4.
5. weights vs parameters: E4.18 "Weights are learned"; the note says parameters (such as the weights). Use "parameters (weights and biases)".
6. Spelling: "neighbouring" (E1.9), "nearest-neighbour" (E5.3) vs American "memorizes", "minimizes". Use American.
7. held-out: E4.18 "held-out validation data", E5.8 "held-out scans" (test-like). Reserve for anything not trained on; name the specific set.
8. Ep 5 alternates detector / model / CNN; say "a CNN" once.
9. Computed captions (E1.7, E2.8, E2.16-17, E3.2, E4.16) print as placeholders ("cap", "notes", "caps[lam]") in captions.py; their rendered text was not checked.
