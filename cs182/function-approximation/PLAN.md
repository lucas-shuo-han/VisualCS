# CS182 · Function Approximation — series plan

Source: **CS 182 / EECS 282A Fall 2026 Course Notes, Note 1: Function Approximation** (`Note01.pdf`, 8 pages).
Five episodes, ~3–4 min each, English captions. One core idea per episode, one worked example whose
numbers are computed in Python (with `assert`s), one "aha" beat.

Color convention (fixed for the whole series, see `dl.py`): data = white, true target f = light grey dashed,
model N_θ = blue, ReLU ramps / hidden units = teal, loss/error/risk = red, regularization λ = orange,
train = green, validation = gold, test = purple.

| Ep | Title | Question | Worked example (numbers from Python) | "Aha" beat | Notes § |
|---|---|---|---|---|---|
| 1 | Learning a Function from Samples | What are we even trying to learn, and why not just use steps? | 7 noisy samples of a hidden f; piecewise-constant fits with 3→6→12 intervals (max error computed); best-fit-height loss vs. step/ramp location τ | A hard step gives a loss that is flat almost everywhere (zero gradient); a ramp gives a slope you can follow. Also: two very different curves interpolate the same points — smoothness is a bet. | 1.1 |
| 2 | ReLU Ramps Are a Spline Basis | How can a sum of ReLUs draw any piecewise-linear curve? | knots τ = 1, 2.5, 4 with slopes 0.2 → 1.4 → −0.8 → 0.6; each ramp adds exactly the slope change (Eq. 1.6); rewrite as a 5-unit one-hidden-layer net (Eq. 1.7) and check it equals g; refine with 3/6/12 knots to approximate a smooth target | The linear part x = ReLU(x) − ReLU(−x): the whole spline *is* a one-hidden-layer network | 1.2 |
| 3 | From Ramps to a Layer | How does a pile of scalar ramps become "affine → ReLU → affine"? | one unit on x = 1.5 and x = 0.2; d = 4 units as W⁽¹⁾x + b⁽¹⁾ → ReLU → W⁽²⁾h + b⁽²⁾ with real matrices | Delete the ReLUs and two affine layers collapse into one line; depth adds nothing without the nonlinearity | 1.3 |
| 4 | Looking Where the Light Is | Why isn't training loss the goal? | accuracy vs. cross-entropy surrogate on a prediction moving 0.51 → 0.55 → 0.90; degree-9 polynomial fit on 10 points with λ = 0 vs. ridge λ; validation sweep of λ over orders of magnitude, test touched once | Training error keeps falling while population error turns around; the proxy is only useful while its mismatch with the goal stays explicit | 1.4 |
| 5 | Hold Out What Will Be New | How do you evaluate honestly when the data has hidden structure? | random row split vs. split at the patient: 1-NN "memorizer" on random labels (~100 % vs ~50 %); hospital-only shortcut AUC on a two-hospital toy (exact computation); Zech et al. numbers (0.93 → 0.82, 34 % vs 1 %, 0.86) | A model that never looks at the lungs can score 0.86 — the split must be at the unit that will be new in deployment | 1.4–1.5 |

Ep. 5 also closes with the four "is this problem coherent?" questions (pattern exists / matters / observable / extractable)
and the one-slide vocabulary map (supervised, unsupervised, foundation models).

## Provenance
- All structure and claims follow Note 1. Figures are redrawn, not copied.
- Own additions (not in the note): the specific numeric examples, the loss-vs-τ comparison in Ep 1, the 5-unit
  parameter table in Ep 2, the collapse-of-two-affine-maps numbers in Ep 3, the polynomial/ridge experiment in Ep 4
  and the memorizer + two-hospital AUC toys in Ep 5. Those toy numbers are computed live and are illustrations, not
  the paper's data; the Zech et al. figures are quoted from the note.
