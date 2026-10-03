# Coverage map: Note 1 (Function Approximation) -> episodes

Captions cited as `E<episode>.<caption#>` (from `captions.py`; `end.N` = end-card lines). "Omitted" rows state a reason.
The note has no worked numeric examples except the Zech et al. figures; the episodes' numbers are the series' own additions (see PLAN.md).

| Item | Note section | Episode / caption |
|---|---|---|
| Prerequisites list (vectors, affine, calculus, distributions) | front | omitted: administrative |
| Prince / JRS reading correspondence | front | omitted: reading list, not content |
| Target function f: R->R (1.1); f not available in closed form | 1.1 | E1.1 |
| Training set of noisy sample pairs (1.2) | 1.1 | E1.2 |
| Parameterized model N_theta (1.3): fit pairs, behave sensibly between and beyond | 1.1 | E1.3, E1.4 |
| Remark: two piecewise-linear interpolants; smoothness is an inductive bias | 1.1 | E1.14-18, end.4 |
| Calculus-style piecewise-constant approximation; refining improves it (Fig 1.1) | 1.1 | E1.5, E1.6, end.2 |
| Hard unit-step has zero derivative; backprop gives no useful gradient for locations / earlier layers | 1.1 | E1.8-12 (loss vs tau) |
| A final linear layer over fixed steps can learn heights but not locations | 1.1 | GAP: never stated (E1.8 fixes the height but does not say heights are learnable) |
| Continuous piecewise-linear is the natural upgrade; universal on compact intervals | 1.1/1.2 | E1.13 (ramp = step with slope); E2.15 (closed interval) |
| PWL function fixed by intercept, initial slope, slope change at each elbow | 1.1 | E2.5 |
| ReLU definition (1.4) | 1.2 | E2.1, end.1 |
| Ramp g_i = ReLU(w x + b) (1.5); elbow at -b/w; sign and size of w set active side and slope | 1.2 | E2.2-E2.4, end.2 |
| Remark: why ReLU over sigmoid/tanh; saturation; vanishing gradient; ReLU derivative is 1 | 1.2 | GAP: no caption |
| Spline construction (1.6): knots, s_0, s_i, c; each ramp adds its slope change | 1.2 | E2.6, E2.7, E2.9, end.3 |
| x = ReLU(x) - ReLU(-x) | 1.2 | E2.10, E2.11 |
| One-hidden-layer form (1.7) | 1.2 | E2.12-14, end.4 |
| Any continuous univariate PWL function is exactly representable by a wide enough 1-hidden-layer ReLU net | 1.2 | E2.12-14 (shown for the example; general claim implicit) |
| Continuous targets on compact intervals approximated by refining (Fig 1.3) | 1.2 | E2.15-17 |
| Remark: statement is for compact domain and wide network; GD need not find the construction | 1.2 | E2.18 (GD caveat yes; "not every function equally well by a given finite net" not said) |
| Fig 1.2 computation graph (multiply, add, max) | 1.2/1.3 | E3.1, E3.3 |
| Hardware motivation: parallel multiply-accumulate | 1.3 | E3.3, E3.12 |
| Vector of d ramps h = ReLU(W1 x + b1), W1 in R^{d x 1} (1.8) | 1.3 | E3.4, E3.9-11, end.2 |
| Linear readout N = W2 h + b2, W2 in R^{1 x d} (1.9); Fig 1.4 | 1.3 | E3.5, E3.8, E3.11, end.3 |
| Vector inputs/outputs: same pattern; deeper nets repeat it | 1.3 | E3.12, E3.17 |
| Without nonlinearity stacked affine maps collapse; depth adds nothing | 1.3 | E3.14-16, end.4 |
| Empirical risk minimization (1.10) | 1.4 | E4.6-9 |
| Loss must express quality and permit progress; squared error, cross-entropy; differentiable surrogate for non-differentiable metric | 1.4 | E4.2-4 (cross-entropy), E4.7-9 (squared error) |
| Four ideas: outcome, metric, surrogate, update estimator (Fig 1.5) | 1.4 | E4.1, E4.2, end.1 |
| Good surrogate: relevant preference, local information, numerically well-behaved, affordable | 1.4 | E4.5 |
| Other update routes when no differentiable surrogate (randomized estimators, relaxations, structured optimization) | 1.4 | GAP: "update estimator" named (E4.1), alternatives never listed |
| Population risk / theta* (1.11); joint P(x,y) | 1.4 | E4.10, end.2 |
| Validation set guides choices; test set used once after choices | 1.4 | E4.19-21 |
| Evaluation data must represent the population; distribution shift is failure of that | 1.4 | E4.21 (partial), E5.9 |
| Pitfall: looking where the light is; proxy useful only while mismatch explicit | 1.4 | E4.14, end.4, episode title |
| Remark: unease, craft precedes theory, "alchemy" licenses careful experiments | 1.4 | omitted: motivational aside (a possible closing line for Ep 5) |
| Remark: detecting shift; cats/dogs vs dinosaurs; density estimation / synthetic samples / labeling help, no guarantee | 1.4 | GAP: not covered |
| Zech et al.: CNN, three hospitals, AUC 0.93 internal | 1.4 | E5.8 ("three hospitals" not stated) |
| New hospital: AUC 0.82 | 1.4 | E5.9 |
| CNN identified hospital with >99.9% accuracy via scanner signatures, positioning, text overlays | 1.4 | GAP: Ep 5 never says what the shortcut cues were or the >99.9% figure |
| Prevalence 34% vs 1%; hospital-only model AUC 0.86 | 1.4 | E5.6, E5.7 (toy), E5.10 |
| CNN learned a shortcut that works internally, useless at a new site | 1.4 | E5.11 |
| Hold-out unit depends on deployment: person, patient, document, time period, molecule scaffold, near-duplicate cluster | 1.4 | E5.11, end.1 (list not narrated; only if on screen) |
| Random row split leaks the entity (Fig 1.6b, entities A/B/C) | 1.4 | E5.1-5, end.2 |
| Do not make the test set maximally different; split must not add unrelated shift | 1.4 | GAP: not covered |
| Kapoor and Narayanan 2023 (leakage) | 1.4/refs | GAP: not cited in captions (add on-screen credit) |
| Overfitting definition | 1.4 | E4.11, E4.13 |
| Regularization; ridge regression (1.12) | 1.4 | E4.15, E4.16 |
| "Love the training data, but not that much"; regularization gives no guarantee | 1.4 | E4.17 |
| Remark: parameters vs hyperparameters (lambda, learning rate, hidden units); chosen by validation; search orders of magnitude | 1.4 | E4.18-20 (learning rate, number of hidden units not named) |
| Four coherence questions: pattern exists / matters / observable / extractable (Fig 1.6 top) | 1.4, 1.5 | E5.12, E5.13, end.4 |
| Vocabulary map (Fig 1.7): supervised = regression, classification, localized annotation (semantic segmentation) | 1.5 | E5.14 (localized annotation / segmentation not mentioned) |
| Unsupervised: learned embeddings (PCA), generative models | 1.5 | E5.15 |
| Density estimation is one route to generation, not its definition | 1.5 | GAP: not covered (E5.15 lists "generative models of the data" only) |
| Foundation models: broad pretraining then prompting or adaptation | 1.5 | E5.16 |
| Coherence questions do not replace the function/data/loss/generalization checklist | 1.5 | E5.17-18 (partial); otherwise omitted: meta-comment |
| Recap bullets 1-4 | 1.5 | E5.17-18 plus per-episode end cards |
| References | end | omitted: bibliography (put Zech 2018 and Kapoor 2023 on screen in Ep 5) |
