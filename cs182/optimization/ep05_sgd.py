"""Episode 5 — Stochastic Gradient Descent (Note 3, sections 3.1-3.2)."""

import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers

# (a) unbiased mini-batches: six per-example gradients at one fixed point, batch size two
GI = np.array([-3.0, -1.0, 0.5, 1.0, 2.0, 4.5])
G_FULL = float(GI.mean())
BATCH = [float(np.mean(c)) for c in itertools.combinations(GI, 2)]
assert len(BATCH) == 15 and abs(G_FULL - 2 / 3) < 1e-12
assert abs(np.mean(BATCH) - G_FULL) < 1e-12                       # E_B g_B = grad f
N_WRONG = sum(b < 0 for b in BATCH)
assert N_WRONG == 5 and sum(b > 0 for b in BATCH) == 9 and min(BATCH) == -2.0 and max(BATCH) == 3.25

# (b) a nonconvex landscape: shallow and deep valley
LAND = lambda x: 0.1 * x ** 4 - 0.5 * x ** 2 + 0.3 * x
_xs = np.linspace(-3.2, 3.2, 6401)
_ys = LAND(_xs)
XD = float(_xs[_ys.argmin()])
_r = _xs > 0
XS = float(_xs[_r][_ys[_r].argmin()])
assert XD < -1.5 and XS > 1.2 and LAND(XD) < LAND(XS) - 0.5

# (c) interpolating linear model, d = 3 > n = 2
X = np.array([[1.0, 0.5, 0.0], [0.0, 1.0, 0.5]])
Y = np.array([1.0, 2.0])
WSTAR = X.T @ np.linalg.inv(X @ X.T) @ Y
assert np.allclose(X @ WSTAR, Y) and abs(WSTAR @ WSTAR - 3.2381) < 1e-3
RHO2 = float(max((X ** 2).sum(1)))
SMIN2 = float(np.linalg.eigvalsh(X @ X.T).min())
assert abs(RHO2 - 1.25) < 1e-12 and abs(SMIN2 - 0.75) < 1e-9
ETA = 1 / (2 * RHO2)                                             # the best step for the bound
assert ETA < 1 / RHO2
ALPHA = 1 - 4 * ETA * (1 - ETA * RHO2) * SMIN2 / len(Y)
assert abs(ALPHA - 0.7) < 1e-9 and 0 <= ALPHA < 1
assert SMIN2 <= RHO2 + 1e-12                                     # so alpha >= 0

TMAX = 40


def run(seed, T=TMAX):
    rs = np.random.RandomState(seed)
    w = np.zeros(3)
    out = []
    for _ in range(T + 1):
        out.append(float(((w - WSTAR) ** 2).sum()))
        i = rs.randint(0, 2)
        w = w - 2 * ETA * (X[i] @ w - Y[i]) * X[i]
    return np.array(out)


RUNS = [run(s) for s in (0, 1, 2)]
BOUND = np.array([ALPHA ** t * float(WSTAR @ WSTAR) for t in range(TMAX + 1)])
# average over many runs sits below the bound
_rs = np.random.RandomState(5)
_w = np.zeros((20000, 3))
MEAN = []
for _t in range(TMAX + 1):
    MEAN.append(float(((_w - WSTAR) ** 2).sum(1).mean()))
    _i = _rs.randint(0, 2, 20000)
    _xi = X[_i]
    _w = _w - 2 * ETA * ((_xi * _w).sum(1) - Y[_i])[:, None] * _xi
MEAN = np.array(MEAN)
assert all(MEAN[t] <= BOUND[t] * 1.02 for t in range(0, 31)), (MEAN[:5], BOUND[:5])
assert MEAN[TMAX] < 1e-6 and BOUND[TMAX] < 1e-5
# one exact step check: the identity |q'|^2 = |q|^2 - 4 eta (1 - eta |x|^2) (x.q)^2
_q = WSTAR * -1.0
_x = X[0]
_q2 = _q - 2 * ETA * (_x @ _q) * _x
assert abs(_q2 @ _q2 - (_q @ _q - 4 * ETA * (1 - ETA * (_x @ _x)) * (_x @ _q) ** 2)) < 1e-12


class Ep05Sgd(NarratedScene):
    series = SERIES
    SCENES = ["minibatch", "landscape", "proof"]

    def construct(self):
        self.title_card()
        self.minibatch()
        self.landscape()
        self.proof()
        self.end_card(
            ["A random mini-batch gradient is right on average. Unbiased, but noisy",
             "Unbiased doesn't mean every step goes downhill. Noise can help or hurt",
             "If the model fits every example, the noise vanishes at the answer and a fixed step converges",
             "The proof needs exact fit, full row rank, zero start and eta below one over rho squared"],
        )

    # ---------------------------------------------------------------- 1. mini-batches
    def minibatch(self):
        head = self.heading("From full gradients to mini-batches")
        f = mts([r"f(\theta)=\frac1n\sum_{i=1}^n f_i(\theta)", r",\qquad ", r"\nabla f=\frac1n\sum_{i=1}^n\nabla f_i"], 0.8, {}).move_to([0, 2.3, 0])
        gb = mts([r"g_B(\theta)=\frac1b\sum_{i\in B}\nabla f_i(\theta)", r",\qquad ", r"\mathbb E_B[g_B]=\nabla f(\theta)"], 0.8, {2: C_NOISE}).move_to([0, 1.2, 0])
        assert_on_screen(f, gb)
        self.say("What if we have a billion examples? The full gradient sums over every one of them, which is a lot "
                 "of work for a single step. So instead we grab a random mini-batch and average its "
                 "gradients, and on average we get the full gradient back.",
                 Write(head), Write(f), run_time=1.2)
        self.cue("So instead we grab", Write(gb))
        self.hold(0.3)
        self.play(FadeOut(f), FadeOut(gb))
        # numbers
        ln = NumberLine(x_range=[-3, 5, 1], length=10.4, color=GREY_B, include_numbers=False, tick_size=0.1).move_to([0, 1.5, 0])
        lab = VGroup(*[txt(f"{v}", 20, GREY_B).next_to(ln.n2p(v), DOWN, buff=0.15) for v in range(-3, 6)])
        d1 = VGroup(*[Dot(ln.n2p(g), radius=0.1, color=C_NOISE) for g in GI])
        t1 = txt("six per-example gradients at one point", 22, C_NOISE).next_to(ln, UP, buff=0.5).shift(LEFT * 2.8)
        full = VGroup(Line(ln.n2p(G_FULL) + UP * 0.5, ln.n2p(G_FULL) + DOWN * 0.3, color=C_LOSS, stroke_width=4),
                      txt(f"full gradient = {G_FULL:.2f}", 22, C_LOSS).next_to(ln.n2p(G_FULL) + UP * 0.5, UP, buff=0.1).shift(RIGHT * 2.0))
        assert_on_screen(VGroup(ln, lab), t1, full)
        # batches on a second line
        ln2 = NumberLine(x_range=[-3, 5, 1], length=10.4, color=GREY_B, include_numbers=False, tick_size=0.1).move_to([0, -0.9, 0])
        lab2 = VGroup(*[txt(f"{v}", 20, GREY_B).next_to(ln2.n2p(v), DOWN, buff=0.15) for v in range(-3, 6)])
        d2 = VGroup(*[Dot(ln2.n2p(b), radius=0.1, color=C_NOISE) for b in BATCH])
        bad = VGroup(*[Dot(ln2.n2p(b), radius=0.1, color=C_LOSS) for b in BATCH if b < 0])
        mean_mark = Line(ln2.n2p(G_FULL) + UP * 0.5, ln2.n2p(G_FULL) + DOWN * 0.3, color=C_LOSS, stroke_width=4)
        t2 = txt("all 15 batches of size 2: their averages", 22, C_NOISE).next_to(ln2, UP, buff=0.5).align_to(ln2, LEFT)
        wr = txt(f"{N_WRONG} of 15 point the wrong way", 22, C_LOSS).next_to(ln2, DOWN, buff=0.6)
        assert_on_screen(VGroup(ln2, lab2), t2, wr, ymin=-2.6)
        self.say("Here are six per-example gradients at one point, and their average, the full gradient, is two "
                 "thirds. Now try every possible batch of two. Those batch averages land all over the place, from "
                 "minus two up to three and a quarter.",
                 FadeIn(ln), FadeIn(lab), FadeIn(d1), FadeIn(t1))
        self.cue("and their average", FadeIn(full))
        self.cue("Now try every", FadeIn(ln2), FadeIn(lab2), LaggedStart(*[FadeIn(d) for d in d2], lag_ratio=0.1, run_time=2), FadeIn(t2))
        self.say("Average all fifteen of them and you get exactly two thirds, which is what unbiased means. And "
                 "yet five of the fifteen point the wrong way.",
                 Create(mean_mark))
        self.cue("yet five", FadeIn(bad), FadeIn(wr))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 2. landscape
    def landscape(self):
        head = self.heading("What the noise can do")
        ax = make_axes([-2.4, 2.4, 1], [-1.6, 1.6, 1], 7.6, 3.4).move_to([-2.4, -0.1, 0])
        curve = plot(ax, LAND, C_LOSS, [-2.4, 2.4], 4)
        ball = Dot(ax.c2p(XS, LAND(XS)), radius=0.12, color=C_ITER)
        jump = CurvedArrow(ax.c2p(XS - 0.1, LAND(XS) + 0.25), ax.c2p(-0.05, LAND(0) + 0.35), angle=TAU / 6, color=C_NOISE, stroke_width=4)
        sh = txt("shallow valley", 22, GREY_B).next_to(ax.c2p(XS, LAND(XS)), DOWN, buff=0.35)
        dp = txt("deep valley", 22, GREY_B).next_to(ax.c2p(XD, LAND(XD)), DOWN, buff=0.35)
        assert_on_screen(VGroup(ax, curve, sh, dp))
        b1 = box_label("noise can shake it out of a shallow valley", C_NOISE, w=5.3, h=0.9, font_size=19).move_to([4.2, 1.5, 0])
        b2 = box_label("or send it somewhere worse", C_LOSS, w=5.3, h=0.9, font_size=19).move_to([4.2, 0.1, 0])
        b3 = box_label("early on, rough directions are enough", C_TRAIN, w=5.3, h=0.9, font_size=19).move_to([4.2, -1.3, 0])
        assert_on_screen(b1, b2, b3)
        self.say("So is the noise a bad thing? On a bumpy surface like this one, it might shake us out of a shallow "
                 "valley. But the same noise can just as easily kick us somewhere worse, so it's a possibility "
                 "and not a promise. Far from the answer a rough direction is plenty, but close to it the noise "
                 "is what holds us back.",
                 Write(head), Create(ax), Create(curve), FadeIn(ball), FadeIn(sh), FadeIn(dp), run_time=1.2)
        self.cue("it might shake", Create(jump), FadeIn(b1))
        self.cue("But the same noise", FadeIn(b2))
        self.cue("Far from the answer", FadeIn(b3))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 3. proof
    def proof(self):
        head = self.heading("When does SGD converge with a constant step?")
        setup = mts([r"Xw=y,\ \ X\in\mathbb R^{n\times d},\ d>n,\ \mathrm{rank}\,X=n"], 0.75, {}).move_to([0, 2.4, 0])
        upd = mts([r"w_{t+1}=w_t-2\eta\,(x_{I_t}^\top w_t-y_{I_t})\,x_{I_t}"], 0.8, {}).move_to([0, 1.3, 0])
        err = mts([r"q_t=w_t-w^*", r"\ \Rightarrow\ ", r"q_{t+1}=(I-2\eta\,x_{I_t}x_{I_t}^\top)\,q_t"], 0.8, {2: C_NOISE}).move_to([0, 0.1, 0])
        why = txt("the error obeys the same random update, because y = Xw* exactly", 24, GREY_B).move_to([0, -1.0, 0])
        assert_on_screen(setup, upd, err, why)
        self.say("So when does SGD converge with a constant step? Let's take the case where every example can be "
                 "fit exactly. We start from zero, and each step picks one random example and follows just that "
                 "example's gradient.",
                 Write(head), Write(setup))
        self.cue("We start from zero", Write(upd))
        self.say("Now track the error from the minimum-norm solution. Because the fit is exact, that "
                 "error follows the very same random update.",
                 Write(err))
        self.cue("Because the fit", FadeIn(why))
        self.hold(0.3)
        self.clear_stage()
        # proof steps
        head = self.heading("One step, in expectation")
        s1 = mts([r"\|q_{t+1}\|^2=\|q_t\|^2-4\eta\,(1-\eta\|x_I\|^2)\,(x_I^\top q_t)^2"], 0.75, {}).move_to([0, 2.5, 0])
        s2 = mts([r"\le\|q_t\|^2-4\eta(1-\eta\rho^2)\,(x_I^\top q_t)^2", r",\quad \rho=\max_i\|x_i\|"], 0.75, {}).move_to([0, 1.4, 0])
        s3 = mts([r"\mathbb E\big[\|q_{t+1}\|^2\,\big|\,q_t\big]\le\|q_t\|^2-4\eta(1-\eta\rho^2)\,\frac1n\|Xq_t\|^2"], 0.75, {}).move_to([0, 0.2, 0])
        s4 = mts([r"\|Xq_t\|^2\ge\sigma_{\min}^2\|q_t\|^2", r"\ \Rightarrow\ ", r"\mathbb E\big[\|q_{t+1}\|^2\,\big|\,q_t\big]\le\alpha\,\|q_t\|^2"], 0.75, {2: C_LOSS}).move_to([0, -1.05, 0])
        s5 = mts([r"\alpha=1-\frac{4\eta(1-\eta\rho^2)\,\sigma_{\min}^2}{n}", r",\quad 0<\eta<\frac1{\rho^2}"], 0.75, {0: C_LOSS}).move_to([0, -2.1, 0])
        assert_on_screen(s1, s2, s3, s4, ymin=-1.8)
        assert_on_screen(s5, ymin=-2.6)
        self.say("Zoom in on one step and expand the squared error. This first line is exact, and it says a good "
                 "step subtracts something positive. Swap that factor for its worst case, and as long as eta is "
                 "below one over rho squared we get an upper bound.",
                 Write(head), Write(s1))
        self.cue("Swap that factor", Write(s2))
        self.say("Now average over which example we drew. Every example is equally likely, so the sum turns into "
                 "the squared length of X times the error. The error lives in the row space, so that length "
                 "can't be tiny. On average, then, each step keeps at most a fraction alpha of the squared error.",
                 Write(s3), run_time=1.5)
        self.cue("The error lives", Write(s4))
        self.cue("On average, then", Write(s5))
        self.hold(0.3)
        self.clear_stage()
        # numeric demonstration
        head = self.heading("The bound in numbers")
        setup = mts([r"X=\begin{bmatrix}1&0.5&0\\0&1&0.5\end{bmatrix}", r",\ \ y=(1,2),\ \ \eta=0.4"], 0.7, {}).move_to([-2.6, 2.5, 0])
        vals = mts([r"\rho^2=1.25,\ \ \sigma_{\min}^2=0.75,\ \ ", r"\alpha=0.7"], 0.7, {1: C_LOSS}).move_to([-2.6, 1.7, 0])
        ax = Axes(x_range=[0, TMAX, 10], y_range=[-10, 1, 5], x_length=7.6, y_length=2.4,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([-2.4, -0.4, 0])
        xt = VGroup(*[txt(f"{v}", 20, GREY_B).next_to(ax.c2p(v, -10), DOWN, buff=0.12) for v in (0, 10, 20, 30, 40)])
        yt = VGroup(*[txt(lb, 20, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12) for v, lb in ((-10, "10⁻¹⁰"), (-5, "10⁻⁵"), (0, "1"))])
        xl = txt("steps t", 22, GREY_B).next_to(ax.c2p(20, -10), DOWN, buff=0.5)
        yl = txt("squared distance to w*", 22, GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        ts = np.arange(TMAX + 1)
        curves = VGroup(*[polyline(ax, ts, np.log10(np.maximum(r, 1e-10)), C_NOISE, 2) for r in RUNS])
        mean = polyline(ax, ts, np.log10(MEAN), C_TRAIN, 4)
        bnd = polyline(ax, ts, np.log10(BOUND), C_LOSS, 4)
        l1 = txt("three single SGD runs", 22, C_NOISE).move_to([4.2, 0.9, 0])
        l2 = txt("average of 20,000 runs", 22, C_TRAIN).move_to([4.2, 0.3, 0])
        l3 = txt("bound α^t ‖w*‖²", 22, C_LOSS).move_to([4.2, -0.3, 0])
        assert_on_screen(VGroup(setup, vals), VGroup(ax, xt, yt, xl, yl), l1, l2, l3)
        self.say("Let's try it with two equations and three unknowns. With these numbers alpha comes out as "
                 "zero point seven, so on average at most seventy percent of the squared error survives a step. "
                 "Single runs jitter, but they all fall. Their average sits just under the bound, which is a "
                 "straight line on this log scale.",
                 Write(head), Write(setup), Write(vals))
        self.cue("Single runs jitter", Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(l1),
                 *[Create(c) for c in curves])
        self.cue("Their average", Create(bnd), FadeIn(l3), Create(mean), FadeIn(l2))
        self.hold(0.4)
        self.clear_stage()
        # aha and pitfalls
        head = self.heading("Why constant steps work here")
        b1 = box_label("at the solution every example's gradient is zero", C_TRAIN, w=8.6, h=0.9, font_size=26)
        b2 = box_label("so the noise vanishes exactly where we want to stop", C_NOISE, w=8.6, h=0.9, font_size=26)
        p1 = txt("Needs: exact fit, full row rank, uniform sampling, zero start, squared loss, η below 1/ρ²", 22, YELLOW_D)
        p2 = txt("With noisy labels the gradients do not vanish, and a constant step leaves a neighborhood of error", 22, YELLOW_D)
        grp = VGroup(b1, b2, p1, p2).arrange(DOWN, buff=0.4).move_to([0, 0.3, 0])
        assert_on_screen(grp)
        self.say("Why does a fixed step work here? At the solution every example's gradient is zero, so the noise "
                 "vanishes exactly where we want to stop. But this is a special case. It needs an exact fit, "
                 "full row rank and a small enough step, and with noisy labels a constant step stalls some "
                 "distance from the answer.",
                 Write(head), FadeIn(b1, shift=UP * 0.2), run_time=1.2)
        self.cue("so the noise", FadeIn(b2, shift=UP * 0.2))
        self.cue("But this is a special", FadeIn(p1))
        self.cue("and with noisy labels", FadeIn(p2))
        self.say("There's one last subtlety in the proof. Shrinking at every step isn't enough on its own, because "
                 "the error could still stall above zero. The fixed factor alpha, strictly below one, is what "
                 "rules that out.",
                 Indicate(b2, color=YELLOW_D))
        self.hold(0.6)
        self.clear_stage()
