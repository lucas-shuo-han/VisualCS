# CS182 · Scaling and muP — series plan

Sources: handwritten iPad notes **Lecture 7** (`iPad_notes/07_fa26.pdf`, 20 pp: linearization, sign SGD, GD, spectral norm / Shampoo, RMS norm, start of Muon)
and **Lecture 8** (`08_fa26.pdf`, 28 pp: RMS->RMS induced norm, Muon and Newton-Schulz, sign-SGD step-size rule, muP, feature-learning conditions).
Lecture 8 repeats pp. 11-19 of Lecture 7 (Xavier recap ... Newton-Schulz); the episodes follow the union once.
Six episodes, English captions, colours from `dl.py` (new here: gradient maroon, step yellow, singular values pink, width teal, standard = red, muP = green).

| Ep | Title | Question | Worked numbers (Python, asserted) | Aha | Notes |
|---|---|---|---|---|---|
| 1 | Steepest Descent Under a Norm | Where does a step come from? | tangent-line error at small/large step; one SGD least-squares step; g=(2,-0.5): sign step vs GD step, brute-force check; lambda view | Same eta in a different norm means a different size of step (sign step is sqrt(2) longer) | L7 pp1-5 |
| 2 | Matrices Want the Spectral Norm | What is the best step for a weight matrix? | Frobenius inner product = trace; 2x2 ellipse, sigma; 5x3 gradient: sum of sigma 6.46 vs 4.80 (20,000 random) vs 4.21 (GD step) | U V^T flattens all singular values to 1 (= Shampoo) | L7 pp6-10 |
| 3 | The RMS Norm | Which norm did Xavier preserve? | RMS of h vs fan-in (5 widths, simulated); induced RMS->RMS = sqrt(din/dout) sigma_max, checked; three layer shapes all change output by exactly eta | One eta acts as a layer-specific learning rate through fan-in / fan-out | L7 pp11-16, L8 pp2-3 |
| 4 | Muon: Orthogonalize Cheaply | How to get U V^T without an SVD? | odd polynomial = U p(Sigma) V^T; cobweb of 3/2x-1/2x^3 from 0.3 and divergence from 2.5; 5x3 singular values over 6 iterations; 0.01 needs 14 iterations; tuned quintic f(1)=0.70, 5 iterations in [0.70, 1.2]; ms/step bars read off the slide | Muon is not converged Newton-Schulz: a few noisy iterations are enough | L7 pp16-20, L8 pp4-14 |
| 5 | The Right Scaling Transfers | Can a hyperparameter tuned small be reused big? | real Adam runs at 5 widths (optimum moves 2^-6 -> 2^-9); sums of n variables: sd of sum/sqrt(n), /n, none; exact F_n(c) vs G_n(alpha), alpha* stays 1.41 while c* drifts 8x | In the reparametrized variable the optimum stays put | L8 pp22-24 |
| 6 | Maximal Update Parametrization | What scaling of eta makes activations AND updates Theta(1) in width? | RMS->RMS norm of d x d Gaussian init (2 vs 2 sqrt d); rank-1 sign matrix, ||S||_2 = d; step size vs width table; width-transfer experiment (best eta constant at 2^-6) | Adam's learning rate should scale as 1/d_in | L8 pp16-21, 25-28 |

Order note: the notes derive eta <= gamma/d_in (sign SGD) before the transfer toy example; here the toy (Ep 5) comes first as motivation and Ep 6 derives the rule, then verifies it.

## Provenance
- Structure and claims follow the two lectures. Own additions (not in the notes): all numeric examples, the width-transfer training experiment (`width_demo.py`), the exact binomial computation of F_n, the unaccumulated-Shampoo identity (GG^T)^(-1/4) G (G^T G)^(-1/4) = U V^T, and the Rademacher toy f(z) = -z^2 exp(-z^2/2).
- Speed numbers in Ep 4 (ms/step, speedrun minutes) are read off the lecture slides (approximate).
