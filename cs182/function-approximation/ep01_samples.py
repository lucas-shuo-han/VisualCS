"""Episode 1 — Learning a Function from Samples (Note 1, section 1.1)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ data (all numbers come from here)

f = lambda x: np.sin(x) + 0.35 * x          # the hidden target
rng = np.random.RandomState(7)
XS = np.array([0.3, 1.1, 2.0, 2.8, 3.9, 4.8, 5.7])
YS = f(XS) + rng.uniform(-0.15, 0.15, size=XS.size)
GRID = np.linspace(0, 6, 1201)


def step_approx(n):
    """Piecewise-constant approximation of f on [0, 6] with n equal intervals (height = f at the midpoint)."""
    edges = np.linspace(0, 6, n + 1)
    hs = f((edges[:-1] + edges[1:]) / 2)
    px, py = [], []
    for a, b, h in zip(edges[:-1], edges[1:], hs):
        px += [a, b]
        py += [h, h]
    vals = hs[np.minimum((GRID / 6 * n).astype(int), n - 1)]
    return px, py, float(np.max(np.abs(f(GRID) - vals)))


ERR = {n: step_approx(n)[2] for n in (3, 6, 12)}
assert ERR[3] > ERR[6] > ERR[12], ERR

# a smooth model fitted to the samples: a + b x + c sin x + d cos x (least squares), sane on [0, 7]
_FEAT = lambda x: np.stack([np.ones_like(x), x, np.sin(x), np.cos(x)], axis=-1)
COEF, *_ = np.linalg.lstsq(_FEAT(XS), YS, rcond=None)
model = lambda x: _FEAT(np.asarray(x, dtype=float)) @ COEF
_m = model(np.linspace(0, 7, 200))
assert -0.5 < _m.min() and _m.max() < 3.5, (_m.min(), _m.max())


A_H, C_H = 1.0, 0.4          # fixed height and baseline: only the location tau is learned


def best_loss(phi, tau):
    """Mean squared error of the one-unit model c + a * phi(x - tau) on the samples (a, c fixed)."""
    return float(np.mean((C_H + A_H * phi(XS - tau) - YS) ** 2))


hard_step = lambda z: (z > 0).astype(float)
TAUS = np.linspace(0.05, 5.95, 400)
L_STEP = np.array([best_loss(hard_step, t) for t in TAUS])
L_RAMP = np.array([best_loss(relu, t) for t in TAUS])
GAP = np.linspace(2.05, 2.75, 15)                     # tau strictly between samples x=2.0 and x=2.8
gap_step = np.array([best_loss(hard_step, t) for t in GAP])
gap_ramp = np.array([best_loss(relu, t) for t in GAP])
assert np.ptp(gap_step) < 1e-12                        # step: loss is exactly flat between samples
assert np.ptp(gap_ramp) > 1e-3                         # ramp: loss changes as tau moves
T0 = 2.4
slope_ramp = (best_loss(relu, T0 + 1e-4) - best_loss(relu, T0 - 1e-4)) / 2e-4
slope_step = (best_loss(hard_step, T0 + 1e-4) - best_loss(hard_step, T0 - 1e-4)) / 2e-4
assert abs(slope_step) < 1e-9 and abs(slope_ramp) > 0.05

# two interpolants of the same samples
ZIG = []
for k, (x, y) in enumerate(zip(XS, YS)):
    ZIG.append((x, y))
    if k < len(XS) - 1:
        xm = (x + XS[k + 1]) / 2
        ZIG.append((xm, (y + YS[k + 1]) / 2 + (1.1 if k % 2 == 0 else -1.1)))
ZX, ZY = zip(*ZIG)
assert np.allclose(np.interp(XS, ZX, ZY), YS) and np.allclose(np.interp(XS, XS, YS), YS)
G2 = np.linspace(XS[0], XS[-1], 800)
ERR_SMOOTH = float(np.mean(np.abs(np.interp(G2, XS, YS) - f(G2))))
ERR_ZIG = float(np.mean(np.abs(np.interp(G2, ZX, ZY) - f(G2))))
assert ERR_SMOOTH < ERR_ZIG


class Ep01Samples(NarratedScene):
    series = SERIES
    SCENES = ["samples", "steps", "gradients", "interpolants"]

    def construct(self):
        self.title_card()
        self.samples()
        self.steps()
        self.gradients()
        self.interpolants()
        self.end_card(
            ["We never see f itself, just a few samples (x, y)",
             "Finer steps fit better, but a step's loss is flat: zero gradient",
             "A ramp is a step that tilts, so gradients can move it",
             "Many curves hit every sample. Picking smooth is a bet, so test it"],
        )

    # ---------------------------------------------------------------- helpers
    def base_axes(self, y=0.1, w=8.0, h=3.6):
        ax = make_axes([0, 7, 1], [-0.5, 3.5, 1], w, h).move_to([0, y, 0])
        xl = txt("input x", 24, GREY_B).next_to(ax.x_axis.get_end(), RIGHT, buff=0.15)
        yl = txt("output y", 24, GREY_B).next_to(ax.y_axis.get_end(), UP, buff=0.15)
        return ax, VGroup(xl, yl)

    # ---------------------------------------------------------------- 1. samples
    def samples(self):
        head = self.heading("The setup")
        ax, labels = self.base_axes()
        d = dots(ax, XS, YS)
        eq = mt(r"\mathcal{D}_{\text{train}}=\{(x_1,y_1),\dots,(x_n,y_n)\},\quad y_i\approx f(x_i)", 0.7)
        eq.to_corner(UR, buff=0.45).shift(DOWN * 0.1)
        self.say("How do you learn a function that nobody will show you? Somewhere there's a target function f "
                 "that turns each input x into an output y, and we never get to see it. All we ever get is a "
                 "handful of samples, where each one is an input paired with a slightly noisy output.",
                 Write(head), Create(ax), FadeIn(labels))
        self.cue("All we ever get", LaggedStart(*[GrowFromCenter(p) for p in d], lag_ratio=0.15), Write(eq))
        self.hold()
        curve = plot(ax, model, C_MODEL, [0, 7])
        nlabel = mt(r"\hat y = N_\theta(x)", 0.8, C_MODEL).move_to(ax.c2p(1.3, 2.9))
        between = Line(ax.c2p(XS[0], -0.5), ax.c2p(XS[-1], -0.5), color=YELLOW_D, stroke_width=4).shift(DOWN * 0.3)
        beyond = Line(ax.c2p(XS[-1], -0.5), ax.c2p(7, -0.5), color=RED_C, stroke_width=4).shift(DOWN * 0.3)
        lb = txt("between samples", 22, YELLOW_D).next_to(between, DOWN, buff=0.1)
        le = txt("beyond", 22, RED_C).next_to(beyond, DOWN, buff=0.1)
        self.say("So we build a function of our own, called N of theta, with parameters we can adjust. We want it "
                 "to pass close to these samples and still behave sensibly everywhere else. Between the samples "
                 "it has to interpolate, and past the last one it has to extrapolate, which is where the real "
                 "test is.",
                 Create(curve, run_time=2.5), FadeIn(nlabel))
        self.cue("Between the samples", Create(between), FadeIn(lb))
        self.cue("past the last one", Create(beyond), FadeIn(le))
        self.hold()
        self.clear_stage()

    # ---------------------------------------------------------------- 2. piecewise constant
    def steps(self):
        head = self.heading("The calculus answer: steps")
        ax, labels = self.base_axes()
        target = plot(ax, f, C_TARGET, [0, 6], width=3).set_stroke(opacity=0.9)
        target = DashedVMobject(target, num_dashes=60)
        d = dots(ax, XS, YS)
        px, py, _ = step_approx(3)
        cur = polyline(ax, px, py, C_MODEL, 4)
        err = txt(f"3 intervals   max error = {ERR[3]:.2f}", 26, C_LOSS).to_corner(UR, buff=0.5).shift(DOWN * 0.1)
        assert f"{ERR[3]:.1f}" == "1.2"                       # spoken: "about one point two"
        self.say("Calculus already has one trick for this. We chop the input into intervals and hold a flat value "
                 "on each one. With three intervals the fit is crude, and somewhere inside a step we miss the "
                 "curve by about one point two.",
                 Write(head), Create(ax), FadeIn(labels), Create(target), FadeIn(d))
        self.cue("With three intervals", Create(cur, run_time=1.8), FadeIn(err))
        self.hold(0.4)
        assert 0.45 < ERR[12] / ERR[6] < 0.55                 # spoken: "roughly halves again"

        def refine(n):
            px, py, e = step_approx(n)
            new_err = txt(f"{n} intervals   max error = {e:.2f}", 26, C_LOSS).move_to(err, aligned_edge=RIGHT)
            return Transform(cur, polyline(ax, px, py, C_MODEL, 4)), Transform(err, new_err)

        self.say("Double that to six intervals, and the steps start to hug the curve. Go up to twelve, and the "
                 "worst miss roughly halves again. So the finer we chop, the better the fit gets.",
                 *refine(6))
        self.cue("Go up to twelve", *refine(12))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 3. why steps can't be learned
    def gradients(self):
        head = self.heading("Why steps are hard to learn")
        ymL, ymR = (float(np.ceil(L.max() * 10) / 10) for L in (L_STEP, L_RAMP))
        axL = make_axes([0, 6, 1], [0, ymL, ymL / 2], 5.6, 2.9).move_to([-3.5, 0.15, 0])
        axR = make_axes([0, 6, 1], [0, ymR, ymR / 2], 5.6, 2.9).move_to([3.5, 0.15, 0])
        tl = txt("hard step:  1[x > τ]", 26, WHITE).next_to(axL, UP, buff=0.35)
        tr = txt("ramp:  ReLU(x − τ)", 26, C_RAMP).next_to(axR, UP, buff=0.35)
        xl = VGroup(*[txt("location τ", 22, GREY_B).next_to(a.get_bottom(), DOWN, buff=0.3) for a in (axL, axR)])
        yl = VGroup(*[txt("loss", 22, C_LOSS).next_to(a.y_axis.get_end(), UP, buff=0.12) for a in (axL, axR)])
        for lab in yl:
            lab.shift(RIGHT * 0.5)
        cL = polyline(axL, TAUS, L_STEP, C_LOSS, 4)
        cR = polyline(axR, TAUS, L_RAMP, C_LOSS, 4)
        self.say("But there's a catch, and we can see it if we take a single step, slide it along x, and ask how "
                 "the loss changes as its location, tau, moves. For a hard step the loss is a staircase, which is dead flat between "
                 "samples and then makes a sudden jump.",
                 Write(head), Create(axL), Create(axR), FadeIn(tl), FadeIn(tr), FadeIn(xl), FadeIn(yl))
        self.cue("For a hard step", Create(cL, run_time=2.0))
        self.say("Flat means the derivative is zero almost everywhere, so backpropagation has no idea which way "
                 "to push the step. A layer on top could still learn how tall each step is, but it can't learn "
                 "where the steps should sit.",
                 Indicate(cL, color=YELLOW_D, scale_factor=1.0))
        self.cue("A layer on top", Indicate(tl, color=YELLOW_D))
        tau = ValueTracker(2.1)
        dotL = always_redraw(lambda: Dot(axL.c2p(tau.get_value(), best_loss(hard_step, tau.get_value())), color=YELLOW_D, radius=0.1))
        dotR = always_redraw(lambda: Dot(axR.c2p(tau.get_value(), best_loss(relu, tau.get_value())), color=YELLOW_D, radius=0.1))
        self.say("Now swap the step for a ramp, which is ReLU of x minus tau. It's the same loss, but now it's a "
                 "curve with a real slope. Watch what happens as tau slides across the gap between two samples. "
                 "The step's loss doesn't budge, while the ramp's loss keeps moving.",
                 Create(cR, run_time=2.0))
        self.cue("Watch what happens", FadeIn(dotL), FadeIn(dotR))
        self.cue("slides across the gap", tau.animate.set_value(2.7), run_time=2.5)
        gl = txt(f"slope = {slope_step:.2f}", 26, WHITE).next_to(axL, DOWN, buff=0.7)
        gr = txt(f"slope = {slope_ramp:.2f}", 26, C_RAMP).next_to(axR, DOWN, buff=0.7)
        assert T0 == 2.4 and f"{slope_ramp:.2f}" == "-1.39"    # spoken below
        self.say("At tau equals two point four, the step's slope is exactly zero. The ramp's slope there is minus "
                 "one point three nine, and that gives us a direction to walk. So a ramp is just a step that "
                 "tilts, and that tilt is what makes its location learnable.",
                 FadeIn(gl), FadeIn(gr))
        self.cue("So a ramp is just", Indicate(tr, color=C_RAMP), Indicate(gr, color=C_RAMP))
        self.hold(0.6)
        self.clear_stage()

    # ---------------------------------------------------------------- 4. interpolants
    def interpolants(self):
        head = self.heading("Many curves fit the same samples")
        ax, labels = self.base_axes()
        d = dots(ax, XS, YS)
        smooth = polyline(ax, XS, YS, C_MODEL, 4)
        zig = polyline(ax, ZX, ZY, C_RAMP, 4)
        self.say("And there's a second catch, which is that lots of different curves pass through exactly the "
                 "same samples. Here's the obvious one, where we just connect them with straight lines. And "
                 "here's a strange one, which wanders off in between but still hits every single sample.",
                 Write(head), Create(ax), FadeIn(labels), FadeIn(d))
        self.cue("Here's the obvious one", Create(smooth, run_time=1.8))
        self.cue("here's a strange one", Create(zig, run_time=2.2))
        self.hold(0.4)
        target = DashedVMobject(plot(ax, f, C_TARGET, [XS[0], XS[-1]], width=3), num_dashes=50)
        e1 = txt(f"plain: mean error {ERR_SMOOTH:.2f}", 24, C_MODEL)
        e2 = txt(f"detour: mean error {ERR_ZIG:.2f}", 24, C_RAMP)
        VGroup(e1, e2).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.5).shift(DOWN * 0.1)
        self.say("Both of them get zero error on the training set, so the samples alone can't tell us which one "
                 "to trust. The hidden target function, drawn dashed, turns out to be smooth. But betting on "
                 "smooth curves is an inductive bias, and only fresh data can check that bet.",
                 Indicate(smooth, color=YELLOW_D, scale_factor=1.0), Indicate(zig, color=YELLOW_D, scale_factor=1.0))
        self.cue("The hidden target function", Create(target, run_time=1.6), FadeIn(e1), FadeIn(e2))
        self.hold(0.6)
        self.clear_stage()
