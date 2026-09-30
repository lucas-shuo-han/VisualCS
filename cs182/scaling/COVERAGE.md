# Coverage: Lectures 7 and 8 -> episodes

Lecture 8 pp. 11-19 repeat Lecture 7 pp. 11-19 (Xavier recap ... Newton-Schulz); covered once.

| Notes item | Where |
|---|---|
| L7 p1-2 motivation, linearization of the loss, tangent-line picture | Ep1 (why, linearize) |
| SGD as steepest descent, sign SGD (l-infinity ball), normalized GD (l2 ball, Cauchy-Schwarz) | Ep1 (ball) |
| Penalty / Lagrange view, step = -(1/2 lambda) grad | Ep1 (ball) |
| Recipe: pick a norm, get an optimizer | Ep1 (recipe, end card) |
| L7 p6 parameters are matrices, Frobenius inner product = trace | Ep2 (matrices) |
| Spectral norm, largest singular value, ellipse picture | Ep2 (spectral_norm) |
| Trace / SVD derivation of Delta W = -eta U V^T | Ep2 (solve) |
| Flattening singular values, semi-orthogonal, condition number, Shampoo, AlgoPerf win (Dahl 2023) | Ep2 (flatten) |
| Xavier recap, RMS norm, why fan-in matters | Ep3 (xavier, rms_norm) |
| Induced RMS->RMS norm = sqrt(d_in/d_out) sigma_max; step -eta sqrt(d_out/d_in) U V^T | Ep3 (induced, shapes) |
| Newton-Schulz: odd polynomials commute with SVD, 1.5x - 0.5x^3, normalize by Frobenius | Ep4 (commute, iterate, demo) |
| Tuned quintic (3.444, -4.7750, 2.0315), f(1) = 0.70, no need to converge | Ep4 (tuned) |
| Muon = momentum + Newton-Schulz + step; code listing; speed/speedrun/Kimi remarks | Ep4 (muon) |
| Hyperparameter transfer, 1/sqrt(n) toy F_n, G_n | Ep5 (toy, transfer) |
| Feature-learning desiderata ||h|| = Theta(1), ||Delta h|| = Theta(1) | Ep6 (desiderata, condition_one, condition_two) |
| Sign SGD / Adam rank-1 sign matrix, ||S||_2 = sqrt(d_in d_out), eta <= gamma / d_in (muP essence, Yang et al. 2022) | Ep6 (sign_rule) |
| Width-transfer payoff | Ep5 (problem) and Ep6 (payoff) |

## Omitted or shortened
- Remark that biases and nonlinearities are ignored: stated only implicitly (the model is drawn with ReLU, but the analysis is about weights).
- The claim that the gradient's singular directions align with the update ("can show this is the case"): not proved in the notes either; skipped.
- Modula dualization / watermark figure: decorative reference, skipped.
- Nano GPT details beyond the plotted numbers: only the ms/step and speedrun bars, read off the slides (approximate).
- Quiz-1 reminder and logistics: not content.

## Notes errors / oddities (shown correctly in the videos)
- L7 p14 / L8 p16: bound written ||Delta W||_2 <= eta sqrt(d1/d2); should be sqrt(d_out/d_in) (episodes use the corrected form).
- Zoomed-out plots of the iteration are labelled x^2 where the polynomial is x^3.
- Output layer is written with a ReLU.
- L7 uses unlabeled d1, d2; the episodes name them d_in, d_out.
- The Lecture 7 brief described L7 as something else; actual content is optimizers under a norm, with Muon and muP in L8.

## Own additions
All numeric examples, the real width-transfer experiment (`width_demo.py`), the Shampoo identity (GG^T)^(-1/4) G (G^T G)^(-1/4) = U V^T, and the exact binomial computation of F_n.
