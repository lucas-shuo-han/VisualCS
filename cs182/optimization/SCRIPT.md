# CS182 · Optimization — narration

Generated from the episode subtitles (.srt).


## 01-gd-least-squares

- `00:06` Least squares is a lamppost: the geometry is explicit, so we can watch exactly what optimization does.
- `00:13` The loss is the squared length of the residual, and its gradient is two X transpose times the residual.
- `00:19` A gradient step with learning rate eta subtracts eta times that gradient.
- `00:25` Expand it and the step is a fixed linear map applied to the weights, plus a constant.
- `00:32` Subtract the minimizer and the constant vanishes: the error is multiplied by the same matrix at every step.
- `00:39` Optimizing a quadratic is therefore a linear dynamical system, and its eigenvalues decide everything.
- `00:47` In the eigenbasis of X transpose X, a problem splits into scalar ones. Start with one, sigma times w equals y.
- `00:55` Each gradient step multiplies the error by the same number, r equals one minus two eta sigma squared.
- `01:02` A small learning rate gives r between zero and one: the error shrinks smoothly, but slowly.
- `01:09` At eta equal to one over two sigma squared, r is zero, and a single step lands exactly on the answer.
- `01:16` Push eta higher and r turns negative: the iterate overshoots, bounces across the answer, and still settles.
- `01:25` Past eta equal to one over sigma squared, r falls below minus one, and every bounce is bigger than the last.
- `01:33` So the scalar rule is simple: the iteration is stable exactly when the absolute value of r is below one.
- `01:41` Now two directions: a ravine, steep where sigma is 2 and shallow where sigma is one half.
- `01:48` Take eta equal to 0.2. Each step multiplies the steep coordinate by minus 0.6 and the shallow one by 0.9.
- `01:57` The path bounces across the ravine while creeping along it: the shallow direction sets the pace.
- `02:03` The steepest direction forbids a bigger step: eta must stay below one over lambda max, not lambda min.
- `02:11` The best constant rate balances the two extremes, equal and opposite. Now both modes shrink by 0.88 per step.
- `02:19` Even the best constant learning rate is still slow. The ravine itself is the problem.
- `02:26` The ratio of the largest to the smallest eigenvalue is the condition number, kappa. Here it is 16.
- `02:33` At the best rate the error shrinks by kappa minus one over kappa plus one per step: 15 over 17 here.
- `02:40` Iterations grow with kappa: one for a round bowl, over two hundred at kappa 100, over two thousand at 1000.
- `02:48` Large condition number means slow convergence even when stable. Momentum and Adam will attack exactly this.

## 02-null-space

- `00:06` Usually more data than parameters gives one answer. Not here: one equation, two unknowns.
- `00:12` Every point on this line fits perfectly, with loss zero. Which one will gradient descent pick?
- `00:18` The row of X is (1, 2). Moving along the null direction, (2, minus 1), changes no prediction.
- `00:26` The two are perpendicular and span the whole space: the fundamental theorem of linear algebra.
- `00:33` The gradient step is X transpose times the residual, so every update lies in the row space.
- `00:40` So the null-space part of the starting point is preserved forever; only the row space changes.
- `00:45` Start at zero: the iterates walk along (1, 2) and stop where they meet the solution line.
- `00:52` That is the minimum-norm solution, X transpose (X X transpose) inverse y. Here it is (1, 2).
- `01:00` Why closest? Any other solution is w min plus a perpendicular null vector: at (5, 0), 25 = 5 + 20.
- `01:13` Start elsewhere, at (3, minus 2). The path is still parallel to (1, 2) but lands on another solution.
- `01:22` The null part of the start, (3.2, minus 1.6), stayed frozen. The limit is w min plus that part.
- `01:30` So gradient descent finds the solution closest to where it began. Only a zero start gives minimum norm.
- `01:37` Here initialization matters: the loss cannot tell the solutions apart, so the start decides.
- `01:44` In higher dimensions it is the same. In the SVD basis, each weight coordinate evolves on its own.
- `01:51` Two coordinates converge to their targets, at rates 0.4 and 0.8. The null coordinate never moves.
- `01:59` Real networks have far more parameters than data: the optimizer and its start pick the solution.

## 03-ridge

- `00:06` Ridge adds a penalty on the size of the weights, with strength lambda. Positive lambda makes it well posed.
- `00:13` Setting the gradient to zero gives a closed form. It inverts X transpose X plus lambda times the identity.
- `00:20` A second form inverts an n by n matrix instead. Same estimator: use whichever matrix is smaller.
- `00:28` Take the SVD. Then ridge weights each direction by sigma over sigma squared plus lambda.
- `00:35` The pseudoinverse uses one over sigma. Ridge keeps the fraction sigma squared over sigma squared plus lambda.
- `00:43` Plot it. Large singular values are nearly untouched; small ones are strongly attenuated.
- `00:49` At sigma equal to root lambda, exactly half is kept. A bigger lambda pushes that line right.
- `00:56` Now the actual multiplier. Without ridge it is one over sigma, which explodes for weak directions.
- `01:03` With ridge it rises, peaks at one over two root lambda where sigma is root lambda, then falls.
- `01:11` Adding lambda times the identity shifts every eigenvalue up by lambda. The smallest gain the most, relatively.
- `01:18` The ravine from episode one has kappa 16. Ridge of 0.25 cuts it to 8.5, and ridge of 1 to 4.
- `01:27` The price is a different problem and a different answer. Conditioning and overfitting improve together.
- `01:34` Data has strong energy along strong directions. Suppose the truth is small, and each direction carries noise.
- `01:42` Without ridge we divide by sigma, so noise grows by one over sigma: thirty times more in the weakest direction.
- `01:49` Ridge shrinks each direction by its own factor. Weak directions collapse toward zero; strong ones barely move.
- `01:57` Averaged over noise, the error drops about twelvefold: calibrated distrust of directions that are mostly noise.
- `02:04` Weak directions can hold signal, so suppressing them is a judgment. Overfitting trusts the data too much.
- `02:12` Gradient descent on the ridge objective shrinks the weights by a fixed factor, then takes the usual data step.
- `02:19` That decay alone shrinks a weight by 0.9 each step. For plain gradient descent, ridge equals weight decay.
- `02:27` A Gaussian prior on the weights plus Gaussian noise makes the MAP estimate a ridge solution.
- `02:33` One trap: minimizing the objective cannot pick lambda. It only grows with lambda, so lambda collapses to zero.
- `02:41` Lambda is a hyperparameter, chosen with held-out data. That is next, along with two other knobs.

## 04-early-stopping

- `00:06` Rotate gradient descent into the SVD basis, with the weights and the targets rotated the same way.
- `00:13` Each singular direction obeys its own scalar recurrence, with factor one minus two eta sigma squared.
- `00:20` Start at zero and solve it. Direction i reaches the fraction q t of the converged answer, y tilde over sigma.
- `00:29` Plot q t against sigma. After a few steps only large singular values are fit; small ones have barely started.
- `00:37` Keep stepping and the curve rises from the right: large singular values converge first, small ones far later.
- `00:44` Compare with ridge. Both hold back weak directions, so stopping early regularizes without a penalty.
- `00:51` The curves need not coincide. What they share is the ordering: weak singular directions enter last.
- `00:59` This ordering is guaranteed only for eta up to one over two sigma max squared: here sigma is 1.5, eta 0.1.
- `01:08` Up to one over sigma max squared, the largest directions overshoot: q t goes above one, then settles.
- `01:17` Now watch four directions, with singular values 3, 1, 0.3 and 0.1, noisy data, and a fixed step size.
- `01:27` Training loss only ever falls: given enough steps, gradient descent fits every direction, noise included.
- `01:35` The distance falls, then climbs as noisy weak directions are fit. Best stopping is near 36 steps.
- `01:42` Run to convergence and the error is many times larger. Stopping early trades a little bias for much less noise.
- `01:49` In practice, save checkpoints and keep the one with the best validation score, not an arbitrary step count.
- `01:57` Regularization strength, learning rate and stopping time are hyperparameters spanning orders of magnitude.
- `02:04` So sweep on a log scale. Evenly spaced values bunch into one decade; one value per power of ten spans it all.
- `02:13` Each candidate is trained, then scored on validation data. The test set is kept for the final procedure.
- `02:19` A grid grows exponentially: five values per knob is 5, 25, 125 runs, and over fifteen thousand for six knobs.
- `02:29` Random search tries new values of every knob on every run, usually a better use of the same budget.
- `02:36` With no budget for broad search, borrow settings from a closely related paper: an engineering prior, not proof.
- `02:43` Could another learner tune the knobs? Meta-learning can, but it is an outer loop with its own data and cost.

## 05-sgd

- `00:06` A training loss averages over n examples, so its gradient is a sum of n terms. Costly for huge n.
- `00:13` Instead draw a random batch of b examples and average those gradients. On average, this is the full gradient.
- `00:21` Six examples have these gradients at one point. Their average, the full gradient, is two thirds.
- `00:27` Now list every batch of two. Their averages scatter widely, from minus two to three and a quarter.
- `00:34` Their average over all 15 batches is exactly two thirds. Unbiased, yet five batches would step the wrong way.
- `00:43` On a bumpy loss surface, the noise may shake the iterate out of a shallow valley.
- `00:48` That is a possibility, not a guarantee: the same noise can just as well push it toward a worse region.
- `00:54` Far from a solution, a rough direction already helps. Near it, the variance of the estimate is the limit.
- `01:02` Take the overparameterized case again: more parameters than examples, and every example can be fit exactly.
- `01:10` Use one random example per step, starting from zero. Its update is the gradient of that example's squared loss.
- `01:17` Measure the distance to the minimum-norm solution. Since the fit is exact, the error updates alike.
- `01:24` Expand the squared norm of the next error. This identity is exact: a good step subtracts a positive amount.
- `01:32` Replace the per-example factor by its worst case, with a step below one over rho squared: an upper bound.
- `01:39` Average over the random example: each has probability one over n, so the sum becomes the norm of X q.
- `01:46` The error stays in the row space, where X q is at least sigma min times q: a contraction factor alpha below one.
- `01:55` Try two equations, three unknowns: rho squared is 1.25, sigma min squared is 0.75, so alpha is 0.7.
- `02:06` Single runs jitter but all fall. The average of many runs sits just under the bound: a line on a log scale.
- `02:15` The reason: at the interpolating solution every example has zero gradient, so the noise vanishes there.
- `02:21` A special case: it needs exact fit, full row rank and a small step. With noisy labels a constant step stalls.
- `02:29` Strict decrease alone is not enough: a decreasing sequence can stall above zero. The factor alpha does the work.

## 06-momentum

- `00:06` Poor conditioning forces a trade-off. A step small enough for the stiff direction crawls along the soft one.
- `00:12` A larger step makes the stiff direction overshoot and bounce. Averaging recent gradients could calm it.
- `00:19` Keep a running average: shrink the old average by beta, and add a small dose of the newest gradient.
- `00:25` Unrolled, that is a weighted sum of all past gradients, weights falling by a factor beta each step back.
- `00:32` For beta of 0.9, the newest gradient gets weight 0.1, the one before 0.09, and so on. One vector holds it all.
- `00:42` Why not average everything equally? A stale, huge gradient would linger for ages; exponential weights forget.
- `00:50` An electrical low-pass filter, a resistor and a capacitor, stores one state. A sudden step charges it smoothly.
- `00:58` Momentum is the discrete version. If the gradient jumps to one, the average becomes one minus beta to the t.
- `01:05` With beta of 0.9 the memory is about 9 steps: the average needs around ten steps to catch up.
- `01:13` Feed in a gradient with a steady part, one, plus a bounce that flips sign each step, like a stiff direction.
- `01:20` The average rises to the steady value and the bounce nearly disappears. That is a low-pass filter at work.
- `01:27` A persistent gradient passes with gain one. An alternating one is cut to one minus beta over one plus beta.
- `01:34` For beta of 0.9, that is five percent. The trial form A times minus one to the t confirms the ratio.
- `01:43` Many libraries omit the one minus beta factor and accumulate an unnormalized velocity instead.
- `01:50` That velocity is bigger by exactly one over one minus beta, so its learning rate must shrink by the same factor.
- `01:58` With beta of 0.9, a rate of 0.1 in one form matches 0.01 in the other. Match before comparing rates.
- `02:08` Here is a ravine: steep across, shallow along. Plain gradient descent with a stable step zigzags across.
- `02:15` With the averaged gradient, the bounces across the ravine cancel while the steady push along it accumulates.
- `02:22` Caution: this shows filtering. A square-root-of-kappa guarantee needs tuning and a smooth, strongly convex loss.

## 07-damping

- `00:06` In the Hessian's eigenbasis a quadratic decouples, so study one scalar mode with curvature lambda.
- `00:12` Plugging in its gradient couples the weight and the average into a two-by-two linear system.
- `00:18` Eliminating the average gives a second-order recurrence with one number: s, eta times one minus beta times lambda.
- `00:26` Its polynomial has two roots. The mode mixes their powers, so both must lie inside the unit circle.
- `00:34` The Schur test needs three checks: no root at plus one, none at minus one, and a root product below one.
- `00:41` So it is stable exactly for s between zero and two times one plus beta. At beta zero, eta lambda is below two.
- `00:50` With beta of 0.9, the stable learning-rate range is nineteen times wider. The real gain is speed, not range.
- `01:00` Fix beta at one half and slide s up from zero. The larger root's size sets the convergence rate.
- `01:06` Small s: both roots are real and positive, and the slow one sits near one. Smooth, but slow.
- `01:13` The roots meet and merge at s equal to one minus root beta, squared: the fastest non-oscillating decay.
- `01:21` Beyond that the roots split into a complex pair, both of size root beta. The rate stays flat: a plateau.
- `01:28` Near the far end both roots turn real and negative. At s equal to three one reaches minus one: unstable.
- `01:37` Start the mode at one and watch. Overdamped creeps toward zero; critical gets there quickly without crossing.
- `01:44` Underdamped overshoots and rings, but inside an envelope shrinking like root beta to the t. Still fast.
- `01:51` So oscillation is not the enemy; only the size of the roots counts. With beta zero, the regimes coincide.
- `02:00` A single eta must serve every eigenvalue. Each mode lands at its own s, the same curve scaled by its curvature.
- `02:08` A soft mode wants a big step to leave the overdamped zone; a stiff one nears the edge. Their s differ by kappa.
- `02:16` Tuning is a minimax problem: make the worst rate over all modes as small as possible, using the plateau.
- `02:23` This works below a kappa bound set by beta. At the limit, the rate is root kappa minus one over root kappa plus one.
- `02:31` Plain gradient descent pays kappa minus one over kappa plus one. This is the standard tuned heavy-ball result.
- `02:38` To shrink the error a hundredfold: kappa 20 takes 46 steps against 10; kappa 100, 230 against 23.
- `02:48` Nesterov evaluates the gradient where the momentum is about to carry the iterate, then steps from here.
- `02:55` Look ahead, then measure the slope there. Tuned Nesterov provably needs about root kappa steps.
- `03:01` Conventions differ between books and libraries. Never mix one line from one convention with another's update.

## 08-adam

- `00:06` Implicit regularization is a feature and a bug: it resists noise but is slow on weak directions.
- `00:13` Dividing by each singular value would fix that, but an SVD of a large model is prohibitive.
- `00:19` So do the next best thing: make steps in ordinary coordinates about the same size in every coordinate.
- `00:27` Set the average to the gradient and the second moment to its square. Dividing gives just the sign.
- `00:33` Gradients of 100, 0.01 and minus 3 all become steps of plus or minus eta. Coordinate scale no longer matters.
- `00:42` Try it in the ravine. It races to the valley floor, since every coordinate moves at full speed.
- `00:48` Then it cannot settle: a fixed-size step overshoots, bouncing between two points near the minimum.
- `00:56` Adam keeps two exponential averages: of the gradient, the first moment, and of its square, the second moment.
- `01:03` Both start at zero, so early on they are too small: with beta 0.9, the first average is a tenth of the gradient.
- `01:11` Bias correction divides by one minus beta to the power of the step count. That scales the early moments back up.
- `01:18` The update divides the corrected first moment by the root of the corrected second moment, per coordinate.
- `01:24` Without the second correction, the first step would be over three times too large; with both, exactly one.
- `01:32` Same ravine, same step size. SignSGD is drawn thin: its cycle around the minimum.
- `01:39` Adam's moments bend and smooth the path, so the iterate settles instead of cycling.
- `01:45` Why discarding magnitude helps is not fully understood. The original analysis had gaps; Adam is robust anyway.
- `01:54` In plain gradient descent, a ridge penalty is exactly the same as shrinking the weights by a fixed factor.
- `02:01` Put the penalty gradient inside Adam and it is averaged and divided by the second moment like everything else.
- `02:07` With weights of one and gradient sizes 10 and 0.05, the penalty shrinks the two coordinates very differently.
- `02:15` AdamW shrinks the weights separately and forms the moments from the data gradient only. All decay alike.
- `02:22` Mind the convention: decay sits inside one minus eta times lambda wd, so it is not the ridge lambda.
- `02:31` Compare optimizers on three axes: how fast training falls, which solution they favor, and what they cost.
- `02:38` Extra state costs memory: momentum stores one more vector, Adam two. Gradients and activations add more.
- `02:45` Neither Adam nor momentum SGD always wins. Optimizers seek low loss; deep learning also needs generalization.

## 09-standardize-init

- `00:06` Why standardize? First, features should have similar sizes; else one in the thousands dominates one near one.
- `00:14` Second, there are numerical issues: mixing huge and tiny values wastes floating-point precision.
- `00:20` Take a feature that runs from 100 to 200, plus an intercept column. The two columns nearly point the same way.
- `00:27` The condition number is about six hundred thousand. Subtract the mean, divide by the deviation: exactly one.
- `00:36` A ReLU unit bends at x equal to minus b over w. With standard normal w and b, that kink is a Cauchy variable.
- `00:45` Its variance is infinite, yet half its mass lies within one of zero, and ninety percent within seven.
- `00:52` Now suppose the data live between 100 and 200. A kink lands there with chance about 0.16 percent per unit.
- `01:00` Among a thousand hidden units, only one or two bend inside the data. The rest are zero or straight lines.
- `01:07` Non-standardized data thus wastes the nonlinearity's expressive power. The same holds for tanh and sigmoid.
- `01:16` A unit with no kink in the data is zero or a straight line there. All thousand stack into a few rank-one pieces.
- `01:23` Take 50 data points. The raw feature matrix has only three singular values above zero; standardized, all fifty.
- `01:31` That gives a cheap debugging check: when a model seems weak, look at the rank of its features.
- `01:38` How to initialize? All zeros fails: everything is multiplied by zero, gradients vanish, nothing moves.
- `01:46` Key observation: one layer's outputs feed the next, so every layer's inputs should look standardized.
- `01:52` For d independent, zero-mean, unit-variance inputs, the output variance is d times the weight variance.
- `02:00` Choose weight variance one over d, the fan-in, and the output is unit-variance too: Xavier initialization.
- `02:09` Push standardized inputs through ten ReLU layers of width 256, with three weight choices, tracking size.
- `02:17` Standard normal weights make the signal explode by two orders of magnitude every layer.
- `02:22` Xavier suits a linear layer, but a ReLU zeroes half its outputs, so the signal halves each layer and fades.
- `02:30` He initialization compensates: half the inputs are alive, so use variance two over d. The signal stays level.
- `02:38` Glorot uses two over fan-in plus fan-out, balancing forward and backward passes. For equal widths it is Xavier.
- `02:46` Biases are simple: start at zero, use a small constant such as 0.01, or treat the bias as one more weight.
