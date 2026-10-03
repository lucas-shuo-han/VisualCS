# Glossary (preferred forms)

| Term | Meaning | Avoid |
|---|---|---|
| linearized loss | L(theta) + <grad, step> | "first-order model" |
| step, update | Delta theta / Delta W | "move" |
| learning rate eta | radius of the ball in steepest descent (episodes 1-4); the step-size hyperparameter | "step size" only where the norm ball is meant (say "ball radius") |
| norm ball | set of steps with norm at most eta | |
| infinity norm, two norm, spectral norm | the three norms used | "max norm", "L2" in narration |
| sign SGD | step = -eta sgn(gradient) | "signSGD" |
| gradient descent | the two-norm case | |
| singular value decomposition (SVD) | G = U Sigma V^T | |
| spectral norm | largest singular value | "operator norm" |
| Frobenius norm / inner product | | |
| semi-orthogonal | U V^T, all singular values one | |
| Shampoo, Muon | optimizers | |
| Newton-Schulz iteration | the odd-polynomial iteration in Muon | |
| RMS norm | length / sqrt(d) | "root mean square" only on first use |
| RMS to RMS norm | induced norm, sqrt(d_in/d_out) times the spectral norm | |
| fan-in d_in, fan-out d_out | input / output width of a layer | |
| Xavier initialization | weight variance 1/d_in | |
| activation h, change Delta h | | |
| Theta(1) | does not grow or shrink with width ("theta of one" spoken) | "O(1)" |
| feature learning | updates change the activations by an order-one amount | |
| muP, maximal update parametrization | spoken "mu P" | "mup" |
| hyperparameter transfer | tune small, reuse on large | |
| width | number of hidden units | |
