# CS182 · Function Approximation — narration

Generated from the episode subtitles (.srt).


## 01-samples

- `00:06` Somewhere there is a function f that turns inputs x into outputs y. We are never given its formula.
- `00:12` All we get are sample pairs: a handful of inputs with their noisy outputs.
- `00:17` We want a parameterized function N of theta that fits these pairs, and behaves sensibly in between and beyond them.
- `00:24` Between the samples we interpolate. Beyond them we extrapolate, and that is where the real test lies.
- `00:31` From calculus we know one way to approximate a function: chop the input into intervals and hold a constant value on each.
- `00:39` With three intervals the fit is crude. The error can be large anywhere inside a step.
- `00:44` Refine to six intervals and the steps hug the curve much better.
- `00:49` Twelve intervals shrink the worst-case error again. Refining the intervals keeps improving the fit.
- `00:56` Now the catch. Slide a step of fixed height along x: how does the loss change with its location tau?
- `01:03` For a hard step the loss is a staircase: perfectly flat between neighboring samples, with sudden jumps.
- `01:10` Its derivative is zero almost everywhere, so backpropagation gives no signal about which way to move the step.
- `01:17` A final linear layer over fixed steps can still learn their heights, but it cannot learn the locations at the same time.
- `01:24` Now swap the step for a ramp: one ReLU unit, ReLU of x minus tau. The same loss becomes a curve with a slope.
- `01:33` Slide tau across the gap between two samples. The step's loss does not move at all, while the ramp's loss keeps changing.
- `01:40` At tau = 2.4 the step's slope is exactly zero. The ramp's slope is -1.39: a direction to follow.
- `01:50` A ramp is a step with a slope. That makes the locations learnable, and it seeds piecewise-linear models.
- `01:58` There is a second catch: many different curves pass through exactly the same samples.
- `02:03` Here is a plain piecewise-linear curve that simply connects the dots.
- `02:07` And here is a very different piecewise-linear curve that detours between the dots but still hits every one.
- `02:14` Both have zero error on the training set, so the samples alone cannot tell us which one is right.
- `02:21` The hidden f, drawn dashed, was smooth. Preferring smoothness is an inductive bias: a bet, which we must test on fresh data.

## 02-relu-ramps

- `00:06` The rectified linear unit is the simplest bend there is: zero for negative inputs, and the input itself for positive ones.
- `00:14` Put an affine function inside: multiply x by a weight w and add a bias b. That is one ramp, a single ReLU unit.
- `00:23` The bend, called the knot, sits where the inside is zero: x equals minus b over w.
- `00:29` A bigger weight makes the ramp steeper and, with the same bias, pulls the knot closer to zero.
- `00:36` A negative weight flips the ramp: it now switches on to the left of its knot.
- `00:41` Why ReLU, and not the sigmoid or tanh of older networks? Those flatten out for large inputs, so their gradients shrink.
- `00:49` Stack many of them and the gradient vanishes. ReLU has slope one wherever it is active, so gradients pass through intact.
- `00:58` The upgrade: a piecewise-linear function is an intercept, a starting slope, and a slope change at each knot.
- `01:05` Equation 1.6: a straight line plus one shifted ReLU per knot, each scaled by its slope change.
- `01:13` Start with the straight line c plus s zero times x. Here c is 0.5 and the first slope is 0.2.
- `01:21` At knot 1, x = 1, the slope goes from 0.2 to 1.4: a change of 1.2. Add 1.2 times ReLU(x − 1).
- `01:33` At knot 2, x = 2.5, the slope goes from 1.4 to -0.8: a change of −2.2. Add minus 2.2 times ReLU(x − 2.5).
- `01:47` At knot 3, x = 4, the slope goes from -0.8 to 0.6: a change of 1.4. Add 1.4 times ReLU(x − 4).
- `01:59` Before its knot a ramp is zero, so earlier pieces stay put. After it, the slope bends exactly as needed.
- `02:07` One loose end: that straight-line term s zero times x is not a ReLU. Or is it?
- `02:14` It is: x equals ReLU of x, minus ReLU of negative x. Positive x survives the first ramp, negative x survives the second.
- `02:24` Every term is a scaled ReLU of a weight times x plus a bias. That is Equation 1.7, a one-hidden-layer network.
- `02:32` 5 hidden units suffice: two for the straight line, one per knot, all read off the slopes and knot locations.
- `02:40` Add up these five units and we recover the spline exactly: same curve, now written as a network.
- `02:48` Real targets are smooth. On a closed interval, a piecewise-linear curve with many knots can approximate one.
- `02:55` With 3 knots and 5 hidden units the fit is rough.
- `02:59` With 6 knots the curve already hugs the target much better.
- `03:03` With 12 knots the worst-case error is down to 0.03. More ramps, better fit.
- `03:09` A caution: this is a statement about existence. A wide enough network can represent the curve.
- `03:15` It does not say a given finite network fits every function equally well, or that gradient descent will find these weights.

## 03-layer

- `00:06` Last time, every ramp was ReLU of a weight times x plus a bias. As a computation graph: multiply, add, then take the max with zero.
- `00:16` Feed in x = 1.5: 2 × 1.5 = 3, then 3 − 1 = 2, and the max with zero keeps it: h = 2.
- `00:28` Feed in x = 0.2: 2 × 0.2 = 0.4, then 0.4 − 1 = −0.6, and the max with zero clips it: h = 0.
- `00:42` Three cheap operations; only the last is nonlinear. Multiply-accumulate hardware runs many units at once.
- `00:51` Run d units side by side, each one a ramp; here d = 4. Each has its own weight and bias, and all see the same x.
- `01:00` A linear readout adds the units up with output weights plus one more bias: exactly the sum in Equation 1.7.
- `01:09` Feed in x = 1.5. Each unit forms its pre-activation z: weight times x, plus bias.
- `01:17` ReLU keeps 3 of the four and clips the second to zero, so the activations are 1.5, 0, 2, 0.25.
- `01:27` The readout multiplies each activation by its output weight, adds them, and adds the bias.
- `01:34` Stack the weights into a matrix and the biases into a vector: one matrix multiply gives all d pre-activations.
- `01:42` Here W one has d rows and one column, because the input is a single number.
- `01:48` ReLU acts entrywise. Then W two, a row vector with d columns, reads the activations out into one number.
- `01:57` Every step is a multiply-accumulate, and this layer needs only 8. Vector inputs and outputs work the same way.
- `02:06` Here is the whole layer as a function of x. Its bends sit at the units' elbows: x = 0, 0.5, 1.
- `02:14` Now delete every ReLU. Two affine maps in a row multiply out into one: a single matrix times x, plus a single vector.
- `02:23` With our numbers the weights multiply to 4 and the biases combine to −2: just the line 4x − 2.
- `02:31` Four units, two layers, and all we can draw is a line. Without the nonlinearity, extra depth adds nothing.
- `02:39` Deeper networks repeat affine, ReLU, affine, ReLU; the ReLUs keep the layers from merging.

## 04-risk

- `00:06` Keep four things apart: the outcome we want, the metric, the training surrogate, and the update estimator.
- `00:12` For a classifier: good decisions, measured by accuracy, trained with cross-entropy and mini-batch gradients.
- `00:21` The true class gets probability 0.45, 0.49, 0.51, then 0.90. Accuracy only sees which side of 0.5 we are on.
- `00:33` 0.45 to 0.49: accuracy is stuck, but cross-entropy falls from 0.80 to 0.71. That is a usable signal.
- `00:45` A useful surrogate expresses what we care about, gives local information, is stable, and is cheap to optimize.
- `00:53` With a loss chosen, training minimizes the empirical risk: the average loss over the training pairs.
- `00:59` Take squared error and four points. This line, y = x, misses them by these red gaps.
- `01:06` Square each gap, average them, and this line scores an empirical risk of 0.045.
- `01:13` Another line, y = 0.5x + 1, scores 0.270. Empirical risk minimization prefers the first line.
- `01:24` The real target is population risk: expected loss on fresh data. Ten noisy samples; dashed is the unseen truth.
- `01:32` A degree-nine polynomial can hit all ten points: training error is essentially zero, but on fresh data it is 3.2.
- `01:41` Training error only ever falls as models get more flexible: a richer family can always fit the samples at least as well.
- `01:49` Error on new data bottoms out near degree 3, then climbs. That turnaround is overfitting.
- `01:55` Empirical risk can be optimized; population performance cannot be seen. We are looking where the light is.
- `02:03` One remedy is a second pressure: ridge regression balances fit against weight size, with strength lambda.
- `02:10` A small lambda already tames the wild swings between the points.
- `02:15` At lambda = 0.1 the curve follows the trend, misses some points on purpose, and generalizes far better.
- `02:23` Too much lambda squeezes the weights until the model underfits. Regularization is a dial, not a cure.
- `02:30` So fit the data, but not too tightly. Even then, generalization is never guaranteed.
- `02:37` Training data sets the weights; validation data sets hyperparameters like lambda, learning rate, and hidden units.
- `02:44` Sweep the hyperparameter over orders of magnitude. Each point is a full training run scored on validation.
- `02:51` Validation picks lambda = 0.1. Careful: every look at the validation set spends a little of its honesty.
- `02:59` Only now do we open the test set, once, after every choice is made. It assumes test data resemble deployment.
- `03:07` A cats-and-dogs model shown dinosaurs: test scores mislead when deployment differs. Detecting shift is only partial.

## 05-holdout

- `00:06` Forty patients, five scans each. Every scan is its patient's fingerprint plus noise; the labels are coin flips.
- `00:13` Left: shuffle rows, half become test. Right: shuffle patients, half of the patients become test.
- `00:21` A 1-nearest-neighbor model just memorizes. Each test scan copies the label of its closest training scan.
- `00:28` With random rows the closest scan is the same patient: about 100 percent, on labels that are pure noise.
- `00:35` Split by patient and the trick collapses to chance. The honest number is the one on the right.
- `00:42` Two hospitals, a hundred chest scans each. In one hospital 34 percent are sick, in the other 1 percent.
- `00:49` Predict from the hospital name alone and the AUC, the area under the ROC curve, is 0.79.
- `00:58` A published pneumonia CNN scored AUC 0.93 on test scans from the hospitals it trained on.
- `01:05` On scans from a new hospital it fell to 0.82. The same model, the same disease, a different building.
- `01:12` Prevalence differed by site, so the hospital name alone scores 0.86 on the pooled test set.
- `01:18` The CNN read scanner signatures, patient positioning and text overlays, without needing the lungs at all.
- `01:25` Random splits could never catch this: the shortcut lives on both sides. Hold out the hospital.
- `01:33` Hold out whole units: a patient, a document, a time period, a molecule scaffold or a cluster of near-duplicates.
- `01:41` Mimic deployment and nothing more. A test set that differs in unrelated ways teaches you nothing either.
- `01:47` Leakage is common: surveys across many fields keep finding the same mistake, and it inflates reported results.
- `01:56` Before any model, ask four questions. Does a pattern exist? Does it matter? Can we observe it? Can we extract it?
- `02:04` A model can pass the last three and still miss the point, as the hospital shortcut did.
- `02:10` Function approximation covers a family: supervised learning with labels, such as regression and classification.
- `02:17` Unsupervised learning finds structure without labels: embeddings like PCA, or density estimation, one route to generation.
- `02:26` Foundation models pretrain on broad data first, then are prompted or adapted. Same ideas, bigger scale.
- `02:35` Samples do not determine a function. Ramps make a flexible basis, and layers stack them.
- `02:40` The training surrogate is not the goal, and honest evaluation holds out exactly what will be new.
