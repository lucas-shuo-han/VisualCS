# CS182 · Scaling and muP — narration

Generated from the episode subtitles (.srt).


## 01-steepest

- `00:06` Training a large model costs real money, so we want to train fast.
- `00:10` Today the default is AdamW with carefully tuned hyperparameters.
- `00:15` A new optimizer needs its own hyperparameter search, and that search is difficult.
- `00:20` Worse, under Adam we often see lazy training: the model barely moves from its random initialization.
- `00:28` Initialization rules were a relief. Before them everything was standard normal. Can updates be as principled?
- `00:36` Write theta for all the parameters and L for the average loss over the data.
- `00:41` Near the current point, the loss looks like a line: its value plus the gradient times the step.
- `00:47` For a small step, the line is accurate.
- `00:49` For a big step, the line lies to us: it promises a much lower loss than we get.
- `00:55` So a step must be small enough for the approximation to hold, yet large enough to converge fast.
- `01:03` For least squares on one sample, the gradient is the residual times the input.
- `01:08` SGD steps against it, scaled by the learning rate eta.
- `01:12` With these numbers the residual is minus three, and one step moves theta to zero point three, zero point six.
- `01:19` But why this direction and this length? Let's derive a step instead of guessing one.
- `01:26` Ask directly: among all steps of size at most eta, which lowers the linearized loss the most?
- `01:32` The loss value itself is a constant, so only the inner product with the gradient matters.
- `01:38` Take two parameters, gradient g = (2, −0.5). Choice one: change each by at most eta: a square.
- `01:48` Slide a line of constant inner product against the gradient, and stop when it is about to leave the square.
- `01:54` It leaves through a corner: every coordinate moves by eta, against the sign of its gradient.
- `02:01` That step is minus eta times the sign of the gradient. It is called sign SGD.
- `02:06` Predicted change: minus two plus minus a half, that is minus 2.5 eta.
- `02:13` Choice two: bound the ordinary length instead. Now the allowed set is a circle.
- `02:19` The line now last touches the circle where the step points straight against the gradient.
- `02:24` Cauchy-Schwarz: an inner product is largest in size when the vectors are aligned. So the step is minus eta times the unit-length gradient.
- `02:33` That is gradient descent with a normalized step. Predicted change: minus 2.06 eta, a bit less than the sign step.
- `02:43` A cousin of this idea: instead of a hard bound, penalize the step with lambda times its squared length.
- `02:49` Set its gradient to zero and solve.
- `02:52` The minimizer is minus one over two lambda times the gradient. That is plain gradient descent.
- `02:58` Its learning rate is one over two lambda, so sweeping lambda sweeps out the same solutions as eta.
- `03:06` Notice the sign step is longer: its corner sits at root two, about 1.41, times eta.
- `03:13` With d parameters it is root d times eta. Same eta, different norm, different meaning of small.
- `03:22` This is the recipe of Bernstein and Newhouse, 2024: choose a norm, choose a step size, and an optimizer falls out.
- `03:30` The infinity norm gives sign SGD, the two norm gives gradient descent, and the spectral norm is coming up.
- `03:37` The right norm may depend on the geometry and architecture of the network. That is where we go next.

## 02-spectral

- `00:06` Until now we treated the parameters theta as one long vector. But network parameters live in matrices, one per layer.
- `00:14` Recall from Xavier initialization: scaling problems come from the weight matrices.
- `00:19` So let's measure the change ΔW in weight-matrix space instead.
- `00:23` The matching inner product multiplies entries in the same position and adds them up.
- `00:28` That number is the trace of G transpose times ΔW. Here both ways give five.
- `00:36` Here is a 2 by 2 matrix A. Feed it every input of length one, the unit circle.
- `00:42` It maps the circle to an ellipse.
- `00:44` The longest stretch is the largest singular value, 2.14. The shortest is 0.69.
- `00:52` The spectral norm of a matrix is exactly this: the largest amount it can stretch a unit vector.
- `00:58` So a spectral-norm ball of radius eta contains every matrix that stretches no input by more than eta.
- `01:06` Now the same question as before, for a matrix: the step of spectral size eta that lowers the linearized loss most.
- `01:14` Write the gradient's singular value decomposition: left vectors U, singular values sigma, right vectors V.
- `01:22` Trace is linear, so the inner product becomes a sum: each singular value times one small scalar.
- `01:29` Each scalar is at most one, because B cannot stretch anything past one. So the total is at most the sum of singular values.
- `01:37` And B equals U V transpose reaches that bound. So the best step is minus eta times U V transpose.
- `01:45` Take a random 5 by 3 gradient. Its singular values are 3.54, 2.15, 0.77, which sum to 6.46.
- `01:56` Normalized G gains only 4.21. Twenty thousand random steps never beat 4.80.
- `02:04` Only U V transpose reaches the full sum. The larger ball of allowed steps buys a larger predicted decrease.
- `02:12` Look at what this step does to the gradient. The gradient has three very different singular values.
- `02:18` U V transpose keeps the singular vectors, the directions, and replaces every singular value by one.
- `02:25` Such a matrix is semi-orthogonal. Its condition number is one, versus 4.6 for the gradient.
- `02:32` Uniform step in all directions, and no domination by the largest singular values.
- `02:39` This is the Shampoo optimizer of Gupta and coauthors, 2017 and 2018.
- `02:46` Shampoo scales the gradient on both sides by inverse fourth roots. That also gives U V transpose.
- `02:53` A variant of Shampoo, by Dahl and coauthors in 2023, won AlgoPerf, a competition for training algorithms.
- `03:01` Two questions remain: how to avoid computing the SVD every step, and how to set the step size for layers of different shapes.

## 03-rms

- `00:06` Recall Xavier initialization. A neuron with d_in standard normal inputs should output a standard normal too.
- `00:13` With independent zero-mean weights, the expected square of h is the weight variance times the sum of squared inputs.
- `00:20` If each squared input is about one, the sum is d_in, so the weight variance should be one over d_in.
- `00:28` Feed random inputs through a layer. With unit-variance weights, outputs grow like the root of the fan-in.
- `00:35` At d_in of 4096 that is about 64 times too large. With variance one over d_in, the size stays near one.
- `00:45` Xavier quietly preserves a norm: the length divided by root d, the root-mean-square or RMS norm.
- `00:52` Four entries of plus or minus one have length 2, sixteen have length 4. The RMS is one for both.
- `01:00` RMS one means every entry is about size one.
- `01:05` That is what the plot showed: with Xavier scaling, output RMS size matches input RMS size.
- `01:11` Is there a matrix version of the RMS norm, measuring how much a weight matrix changes RMS size?
- `01:18` Recall the induced matrix norm: the largest output size, measured in one norm, over inputs of size one in another.
- `01:27` Use RMS on both sides: how much can A grow an input of RMS size one?
- `01:32` An input of RMS one has length root d_in. An output's RMS is its length over root d_out.
- `01:39` So the RMS to RMS norm is the spectral norm times root of d_in over d_out.
- `01:45` Check: a 64 by 256 matrix has spectral norm 1.49, so its RMS norm is twice that, 2.98.
- `01:55` Now put this norm into the optimizer recipe from episode one: steps of RMS to RMS size at most eta.
- `02:03` The spectral size allowed is eta times root of d_out over d_in, so the best step is that factor times U V transpose.
- `02:11` Try eta equal to 0.1 on three shapes. Wide-to-narrow layers get a smaller spectral step, narrow-to-wide a larger one.
- `02:20` Yet each layer's output changes by exactly eta in RMS size. One number eta behaves like a layer-specific learning rate.
- `02:29` Fan-in and fan-out do the adjusting. Making this precise for growing width is the idea behind maximal update parametrization.

## 04-muon

- `00:06` Last time the RMS ball gave the step minus eta, root d_out over d_in, times U V transpose. Muon's first key idea.
- `00:15` The catch: computing U V transpose needs an SVD of the gradient at every step, and that is expensive.
- `00:22` Two observations: an approximate direction is good enough, and Newton-Schulz can produce it cheaply.
- `00:29` We want a cheap function f that turns U sigma V transpose into U V transpose: every singular value replaced by one.
- `00:38` Take odd matrix polynomials: X, X X transpose X, and so on. Example: three halves X minus a half X X transpose X.
- `00:49` Plug in the SVD. The V transposes and U's in the middle cancel, because U and V have orthonormal columns.
- `00:56` What is left is U times p applied to the singular values, times V transpose. The singular vectors are untouched.
- `01:04` So p can be applied to a whole matrix while changing only its singular values, with no SVD needed.
- `01:12` Can we find p so that repeatedly applying it sends every positive singular value to one? Try this cubic.
- `01:19` Start at 0.3 and bounce between the curve and the diagonal: 0.44, 0.61, 0.80, and on toward one.
- `01:29` The point one is a fixed point that attracts everything nearby. Iterating p, singular values in the interval zero to one climb to one.
- `01:39` Zoom out. Start at 2.5 and the iteration jumps to minus four, then twenty-seven, and diverges.
- `01:46` So singular values must start inside zero to one. Dividing by the Frobenius norm guarantees it.
- `01:54` Take a random 5 by 3 gradient, normalized. Its singular values are 0.84, 0.51 and 0.18.
- `02:03` One iteration of p lifts the small ones the most.
- `02:07` Another one, and the spread between them is shrinking.
- `02:10` After three iterations, all three are within about one tenth of one.
- `02:15` By iteration six the smallest is 0.990. Almost the same as replacing the singular values by exactly one.
- `02:24` A tiny singular value grows only about one and a half times per step, so from 0.01 it takes 14 iterations.
- `02:33` We may choose the coefficients. Higher orders may converge faster, but each step costs more.
- `02:39` The NanoGPT speedrun uses these three coefficients. Notice f of one is 0.70, not one. So it does not converge to one.
- `02:49` Five iterations send every input from 0.01 up to between 0.68 and 1.13. Noisy, but far from tiny.
- `02:59` Must it converge? No. Singular values roughly one are good enough, and much faster than the plain cubic.
- `03:07` Put it together: Muon stands for momentum orthogonalized by Newton-Schulz.
- `03:12` Keep a momentum buffer, orthogonalize it with a few Newton-Schulz steps, and step the weights against it.
- `03:19` On the NanoGPT speedrun, Muon costs about the same time per step as Adam, and far less than Shampoo or SOAP.
- `03:27` Per step it also gets the validation loss down faster, so it reaches a given loss in less wall-clock time.
- `03:35` The task took about 45 minutes at the May 2024 baseline. Muon was a big step down, and by December the record was a few minutes.
- `03:44` In February 2025, Moonshot AI and UCLA showed that Muon scales to large language model training.

## 05-transfer

- `00:06` A parameterization is about choosing the right units. Why? Hyperparameter search is a key challenge.
- `00:13` It is worst when the network is large, because every experiment is very expensive.
- `00:18` Can we optimize hyperparameters on a smaller network, then transfer them to a larger one? What is the right scaling?
- `00:26` Here is a small experiment: a three-layer network trained with Adam, one learning rate for every layer, at five widths.
- `00:34` The best learning rate is not shared. It drops from 2 to the -6 at width 32 to 2 to the -9 at width 512.
- `00:43` Yang and coauthors, 2022, saw the same in Transformers: widths do not share the best setting.
- `00:51` Add up n independent numbers with mean zero and variance one. How should we scale the sum?
- `00:57` Watch the spread. Divided by root n it stays at one for every n, approaching a standard normal.
- `01:03` Divide by n and it shrinks to zero. Do not divide at all and it grows without bound.
- `01:09` One over root n is the right order of scaling factor: the only choice that converges to something non-trivial.
- `01:17` Let a scale c multiply the sum, and tune c to minimize the expected value of a bounded f. Call it F sub n of c.
- `01:26` Plot it for n of 4, 16, 64, 256. The best c drifts left, from 0.63 to 0.09, so small-n tuning does not carry over.
- `01:39` Now reparametrize: write c as alpha over root n. The optimum in alpha barely moves.
- `01:46` No accident: G_n converges to a fixed function of alpha. Best alpha is about 1.42 at n of 256, limit root two.
- `01:56` So we can copy alpha star from a smaller n to a larger one. Copying c star cannot work the same way.
- `02:04` Can we do something similar for neural-network hyperparameters?
- `02:08` A preview of the answer: for Adam-like updates, a learning rate of one over the fan-in d_in, times a constant gamma.
- `02:15` One over d_in is the right scaling with width. Tune gamma small and reuse it. Next: where this comes from.

## 06-mup

- `00:06` Consider one hidden layer: a weight matrix, a bias and a nonlinearity. What happens as the width grows?
- `00:13` Xavier thinking: we want the RMS size of the activations to be about one, so the typical entry is.
- `00:20` Second, each update should change the activations by a size that does not vanish with width.
- `00:26` Theta of one means bounded above and below by constants, whatever the width.
- `00:32` Ignoring bias and nonlinearity, the output length is at most the spectral norm times the input length.
- `00:39` So lengths root d_out and root d_in force a spectral norm of order root d_out over d_in.
- `00:45` Random matrices: unit variance grows the norm to 64 by width 1024. Xavier variance keeps it near 2.
- `00:53` So condition one holds when the weights have RMS to RMS norm of order one: the norm behind the optimizer.
- `01:01` Now the update. The output change has two parts: new weights on the old input, and old weights on the input change.
- `01:09` Take lengths and use the triangle inequality: each part is a spectral norm times a length.
- `01:15` The second term is fine by condition one. For the first, the update needs spectral norm of order root d_out over d_in.
- `01:22` Then both terms are of order root d_out, and the output's RMS change is order one, as desired.
- `01:29` Two conditions, then: the weights and the updates should both have RMS to RMS norm of order one.
- `01:37` Take sign SGD, a stand-in for Adam: eta times the sign of the gradient. How should eta depend on the layer?
- `01:45` With one sample the gradient has rank one, and so does its sign matrix: an outer product of sign vectors.
- `01:52` For rank one the spectral and Frobenius norms agree, so the norm is root of d_in times d_out.
- `01:58` Bound the RMS to RMS size of the step by gamma. The roots cancel, so eta scales as gamma over d_in.
- `02:06` So Adam's learning rate should scale as one over d_in. This captures an essence of muP.
- `02:13` Test the sign step in layers of width 64 to 1024. With a fixed learning rate, the update grows in proportion to width.
- `02:22` With gamma over d it stays constant, and so does the change in the layer's output.
- `02:27` A caveat: with a larger batch the gradient is no longer rank one, so the rule is conservative.
- `02:35` Rerun the earlier experiment at widths 32 to 512. On the left, standard scaling: the best rate keeps moving.
- `02:44` On the right, layers whose fan-in is the width get their rate times 32 over width. The first layer is untouched.
- `02:51` Now every width is best at 2 to the -6. Tune on the narrow network and the wide one inherits it.
- `02:58` Yang and coauthors, 2022, report this for Transformers too: a stable optimum, and wider networks do better.
- `03:06` That is muP: the largest updates that keep activations and their changes order one at every width.
