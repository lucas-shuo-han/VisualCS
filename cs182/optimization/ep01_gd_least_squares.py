"""Episode 1 — Gradient Descent on Least Squares (Note 2, section 2.1; Lecture 2; HW1 problem 1)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers

# (a) scalar problem  sigma * w = y,  L(w) = (y - sigma w)^2,  w0 = 0
SIG, YV = 2.0, 4.0
WSTAR = YV / SIG
ETAS = [0.02, 0.125, 0.2, 0.26]
RS = [1 - 2 * e * SIG ** 2 for e in ETAS]
assert np.allclose(RS, [0.84, 0.0, -0.6, -1.08])
assert abs(1 / (2 * SIG ** 2) - 0.125) < 1e-12 and abs(1 / SIG ** 2 - 0.25) < 1e-12
TS = np.arange(0, 10)


def scalar_run(eta, T=10):
    w, out = 0.0, [0.0]
    for _ in range(T - 1):
        w = w + 2 * eta * SIG * (YV - SIG * w)          # w <- w - eta * dL/dw
        out.append(w)
    return np.array(out)


WS = [scalar_run(e) for e in ETAS]
for r, w in zip(RS, WS):
    assert np.allclose(w, WSTAR * (1 - r ** TS))          # closed form: error is multiplied by r each step

# (b) two directions: X = diag(2, 0.5), lambdas = sigma^2 = (4, 0.25), error coordinates
S_STEEP, S_SOFT = 2.0, 0.5
LAM_STEEP, LAM_SOFT = S_STEEP ** 2, S_SOFT ** 2
KAPPA = LAM_STEEP / LAM_SOFT
assert KAPPA == 16.0
ETA_LIM = 1 / LAM_STEEP                          # 0.25
ETA_STAR = 1 / (LAM_STEEP + LAM_SOFT)            # 0.2353
RHO_STAR = (KAPPA - 1) / (KAPPA + 1)             # 15/17
assert abs(1 - 2 * ETA_STAR * LAM_STEEP + (1 - 2 * ETA_STAR * LAM_SOFT)) < 1e-12      # equal and opposite
assert abs(abs(1 - 2 * ETA_STAR * LAM_STEEP) - RHO_STAR) < 1e-12
ETA_A = 0.2
F_STEEP_A, F_SOFT_A = 1 - 2 * ETA_A * LAM_STEEP, 1 - 2 * ETA_A * LAM_SOFT
assert abs(F_STEEP_A + 0.6) < 1e-12 and abs(F_SOFT_A - 0.9) < 1e-12
START = (2.4, 0.8)                                # (soft coordinate, steep coordinate)
assert abs(LAM_SOFT * START[0] ** 2 + LAM_STEEP * START[1] ** 2 - 4.0) < 1e-12


def gd_path(eta, steps):
    e = np.array(START, float)
    pts = [tuple(e)]
    for _ in range(steps):
        e = e - eta * 2 * np.array([LAM_SOFT * e[0], LAM_STEEP * e[1]])      # gradient of L = l e^2
        pts.append(tuple(e))
    return pts


P_A = gd_path(ETA_A, 20)
P_STAR = gd_path(ETA_STAR, 20)
assert abs(P_A[3][1] - 0.8 * (-0.6) ** 3) < 1e-12 and abs(P_A[3][0] - 2.4 * 0.9 ** 3) < 1e-12
assert abs(P_STAR[5][0] - 2.4 * RHO_STAR ** 5) < 1e-12


def iters_to(rho, factor=0.01):
    """Steps until the error has shrunk to `factor` of its start: rho^t <= factor."""
    return 1 if rho == 0 else int(np.ceil(np.log(factor) / np.log(rho)))


IT_A, IT_STAR = iters_to(0.9), iters_to(RHO_STAR)
assert (IT_A, IT_STAR) == (44, 37)
KAPS = [1, 2, 4, 16, 100, 1000]
RHOS = [(k - 1) / (k + 1) for k in KAPS]
ITS = [iters_to(r) for r in RHOS]
assert ITS[:4] == [1, 5, 10, 37] and ITS[4] > 200 and ITS[5] > 2000, ITS


def mode_marker(r, w=4.6):
    """Number line for the per-step factor r with the stable band (-1, 1) shaded."""
    lo, hi = -1.6, 1.3
    s = w / (hi - lo)
    x = lambda v: (v - lo) * s - w / 2
    line = Line([x(lo), 0, 0], [x(hi), 0, 0], color=GREY_B, stroke_width=2)
    band = Rectangle(width=x(1) - x(-1), height=0.3, stroke_width=0, fill_color=GREEN_D, fill_opacity=0.35).move_to([(x(1) + x(-1)) / 2, 0, 0])
    ticks = VGroup(*[txt(t, 20, GREY_B).move_to([x(v), -0.32, 0]) for v, t in [(-1, "−1"), (0, "0"), (1, "1")]])
    col = C_LOSS if abs(r) >= 1 else GREEN_C
    dot = Dot([x(r), 0, 0], radius=0.12, color=col)
    return VGroup(band, line, ticks, dot), dot, x


class Ep01GdLeastSquares(NarratedScene):
    series = SERIES
    SCENES = ["equations", "scalar_case", "two_directions", "condition_number"]

    def construct(self):
        self.title_card()
        self.equations()
        self.scalar_case()
        self.two_directions()
        self.condition_number()
        self.end_card(
            ["On a quadratic, each error direction just gets multiplied by its own factor, every step",
             "Keep that factor between minus one and one, or the run blows up",
             "The steepest direction caps the learning rate; the flattest one sets the pace",
             "Condition number: steepest over flattest. Big kappa means slow, however you tune eta"],
        )

    # ---------------------------------------------------------------- 1. equations
    def equations(self):
        head = self.heading("Least squares as a dynamical system")
        loss = mts([r"L(\vec w)=", r"\|X\vec w-\vec y\|_2^2"], 0.85)
        grad = mts([r"\nabla L(\vec w)=", r"2X^\top(X\vec w-\vec y)"], 0.85, {1: C_GRAD})
        step = mts([r"\vec w_{t+1}", r"=\vec w_t-", r"\eta", r"\nabla L(\vec w_t)"], 0.85, {2: C_ETA, 3: C_GRAD})
        upd = mts([r"\vec w_{t+1}", r"=\big(I-2", r"\eta", r"X^\top X\big)", r"\vec w_t+2", r"\eta", r"X^\top\vec y"], 0.85, {2: C_ETA, 5: C_ETA})
        err = mts([r"\vec\Delta_{t+1}", r"=\big(I-2", r"\eta", r"X^\top X\big)", r"\vec\Delta_t"], 0.85, {2: C_ETA})
        dfn = mts([r"\vec\Delta_t=\vec w_t-\vec w_{\min}"], 0.7, {0: C_LOSS})
        loss.move_to([0, 2.2, 0]); grad.move_to([0, 1.2, 0]); step.move_to([0, 0.1, 0]); upd.move_to([0, 0.1, 0])
        assert_on_screen(loss, grad, step, upd)
        self.say("How does gradient descent actually move? On most problems that's hard to say, but least squares "
                 "is the one place where we can follow every step exactly. Here's the loss, and here's its "
                 "gradient, which is two X transpose times the residual.",
                 Write(head), Write(loss))
        self.cue("and here's its gradient", Write(grad))
        self.say("Each step walks downhill, so we take the gradient, scale it by the learning rate eta, and "
                 "subtract it. Now multiply that out, and something nice appears. Every step is just one fixed "
                 "matrix times w, plus some constant.",
                 Write(step))
        self.cue("Now multiply that out", ReplacementTransform(step, upd))
        self.hold(0.3)
        self.play(FadeOut(loss), FadeOut(grad), upd.animate.move_to([0, 1.6, 0]))
        err.move_to([0, 0.2, 0])
        dfn.move_to([0, -0.9, 0])
        box = SurroundingRectangle(VGroup(err[1], err[2], err[3]), color=YELLOW_D, buff=0.1)
        self.say("If we measure from the answer instead, the constant disappears, and the error simply gets "
                 "multiplied by that matrix again and again. It's the same matrix at every single step, so the "
                 "whole story is hiding in its eigenvalues.",
                 Write(err), FadeIn(dfn))
        self.cue("It's the same matrix", Create(box))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 2. scalar case
    def scalar_case(self):
        head = self.heading("One direction: sigma times w equals y")
        ax = make_axes([0, 9, 1], [-2, 6, 2], 7.4, 3.6).move_to([-2.2, -0.3, 0])
        ticks = tick_labels(ax, [0, 3, 6, 9], 20)
        xl = txt("step t", 22, GREY_B).next_to(ax.x_axis.get_end(), DOWN, buff=0.15).shift(LEFT * 0.4)
        yt = VGroup(*[txt(f"{v}", 20, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.14) for v in (-2, 0, 2, 4, 6)])
        star = DashedLine(ax.c2p(0, WSTAR), ax.c2p(9, WSTAR), color=C_TARGET, stroke_width=2)
        sl = txt("w* = 2", 22, C_TARGET).next_to(ax.c2p(9, WSTAR), RIGHT, buff=0.12)
        prob = mts([r"\sigma w=y,\ \ \sigma=2,\ y=4"], 0.7).to_edge(UP, buff=1.0).set_x(4.0)
        rec = mts([r"w_{t+1}-w^*=", r"(1-2\eta\sigma^2)", r"\,(w_t-w^*)"], 0.72, {1: C_ITER})
        rec.next_to(prob, DOWN, buff=0.3)
        assert_on_screen(prob, rec)
        self.say("Each eigen-direction behaves on its own, so let's shrink the problem down to a single number. "
                 "We want two times w to equal four, and we start from zero. Every step multiplies the error by "
                 "one number, which we'll call r, so let's see what the learning rate does to it.",
                 Write(head), Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yt), Create(star), FadeIn(sl), Write(prob))
        self.cue("Every step multiplies", Write(rec))

        def panel(k):
            eta, r = ETAS[k], RS[k]
            nl, dot, _ = mode_marker(r)
            nl.move_to([4.2, -0.5, 0])
            lab = VGroup(txt(f"η = {eta:g}", 30, C_ETA), txt(f"r = {r:.2f}", 30, C_LOSS if abs(r) >= 1 else GREEN_C)).arrange(RIGHT, buff=0.6).move_to([4.2, 0.6, 0])
            cap = txt("r must stay inside the band", 20, GREY_B).next_to(nl, DOWN, buff=0.25)
            g = VGroup(lab, nl, cap)
            assert_on_screen(g)
            return g

        def curve(k):
            return VGroup(clipped(ax, TS, WS[k], -2, 6, C_ITER, 4),
                          VGroup(*[Dot(ax.c2p(t, w), radius=0.07, color=C_ITER) for t, w in zip(TS, WS[k]) if -2 <= w <= 6]))

        pan = panel(0)
        cur = curve(0)
        self.say("Start with a timid step. Then r is zero point eight four, so we creep toward the answer a little "
                 "at a time. Raise eta to one eighth and r is exactly zero, so a single step lands on the answer.",
                 FadeIn(pan), Create(cur[0], run_time=1.5), LaggedStart(*[FadeIn(d) for d in cur[1]], lag_ratio=0.1, run_time=1.5))
        self.cue("Raise eta", Transform(pan, panel(1)), Transform(cur, curve(1)))
        self.say("Go bigger and r turns negative. Now we overshoot and bounce back and forth, but each bounce is "
                 "smaller, so we still settle down. Push a little further and r drops below minus one, and then "
                 "every bounce is bigger than the last, and the run blows up.",
                 Transform(pan, panel(2)), Transform(cur, curve(2)))
        self.cue("Push a little further", Transform(pan, panel(3)), Transform(cur, curve(3)))
        self.hold(0.3)
        cond = mts([r"|1-2\eta\sigma^2|<1\iff 0<\eta<\frac{1}{\sigma^2}"], 0.8, {})
        cond.move_to([4.0, 2.4, 0])
        assert_on_screen(cond)
        self.say("So the whole rule fits on one line. Keep r strictly between minus one and one, which means the "
                 "learning rate has to stay below one over sigma squared.",
                 FadeOut(prob), FadeOut(rec), Write(cond))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 3. two directions
    def two_directions(self):
        head = self.heading("Two directions, one learning rate")
        ax = Axes(x_range=[-4.5, 4.5, 1], y_range=[-1.5, 1.5, 1], x_length=8.1, y_length=2.7,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([-2.3, -0.1, 0])
        cont = contour_family(ax, (LAM_SOFT, LAM_STEEP), [4.0, 2.25, 1.0, 0.25, 0.04])
        xl = txt("shallow direction, σ = 0.5", 21, C_SOFT).next_to(ax, DOWN, buff=0.15).align_to(ax, LEFT).shift(RIGHT * 0.3)
        yl = txt("steep, σ = 2", 21, C_STIFF).next_to(ax.c2p(0, 1.5), RIGHT, buff=0.15).shift(DOWN * 0.15)
        assert_on_screen(VGroup(ax, cont, xl))
        self.say("Real problems have many directions at once, so here are two of them. One is a steep wall and "
                 "the other is a shallow floor, and together they make a ravine.",
                 Write(head), Create(ax), LaggedStart(*[Create(c) for c in cont], lag_ratio=0.15))
        self.cue("One is a steep wall", FadeIn(yl), FadeIn(xl))

        def factors(f_steep, f_soft, eta):
            return VGroup(txt(f"η = {eta:.3g}", 30, C_ETA),
                          txt(f"steep mode × {f_steep:+.2f}", 24, C_STIFF),
                          txt(f"shallow mode × {f_soft:+.2f}", 24, C_SOFT)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.7, 1.0, 0]).align_to([2.6, 0, 0], LEFT)

        pan = factors(F_STEEP_A, F_SOFT_A, ETA_A)
        assert_on_screen(pan)
        start = Dot(ax.c2p(*START), radius=0.1, color=C_ITER)
        pa = path_pts(ax, P_A)
        da = path_dots(ax, P_A)
        self.say("A single learning rate has to serve both directions. At zero point two, the steep error flips "
                 "sign and keeps sixty percent of its size, while the shallow one keeps ninety percent. So we "
                 "zigzag across the ravine while barely creeping along it, and the shallow direction is the one "
                 "that makes us slow.",
                 FadeIn(start), FadeIn(pan))
        self.cue("So we zigzag", Create(pa, run_time=3.5, rate_func=linear),
                 LaggedStart(*[FadeIn(d) for d in da], lag_ratio=0.05, run_time=3.5))
        n_it = txt(f"{IT_A} steps for a 100× smaller error", 22, C_SOFT).next_to(pan, DOWN, buff=0.4).align_to(pan, LEFT)
        assert_on_screen(n_it)
        self.say("That takes forty-four steps to make the error a hundred times smaller. So why not just take "
                 "bigger steps? Because the steep wall won't let us. Once eta passes one quarter, that direction "
                 "blows up.",
                 FadeIn(n_it))
        lim = mts([r"\eta<\frac{1}{\lambda_{\max}}", r"=\frac{1}{4}"], 0.75, {0: C_ETA}).next_to(n_it, DOWN, buff=0.35).align_to(pan, LEFT)
        assert_on_screen(lim)
        self.cue("Once eta passes", Write(lim))
        self.hold(0.3)
        # eta star
        pan2 = factors(1 - 2 * ETA_STAR * LAM_STEEP, 1 - 2 * ETA_STAR * LAM_SOFT, ETA_STAR)
        n_it2 = txt(f"{IT_STAR} steps for a 100× smaller error", 22, GREEN_C).next_to(pan2, DOWN, buff=0.4).align_to(pan2, LEFT)
        pb = path_pts(ax, P_STAR, color=GREEN_C)
        db = path_dots(ax, P_STAR, color=GREEN_C)
        assert_on_screen(pan2, n_it2)
        best = mts([r"\eta^*=\frac{1}{\lambda_{\max}+\lambda_{\min}}=0.235"], 0.7, {0: C_ETA}).next_to(n_it2, DOWN, buff=0.35).align_to(pan2, LEFT)
        assert_on_screen(best)
        self.say("The best we can do is choose eta so both directions shrink equally fast, and then each of them "
                 "keeps eighty-eight percent per step. But look how little that buys us. It's thirty-seven steps "
                 "instead of forty-four. So the learning rate isn't the real problem here, the ravine is.",
                 FadeOut(pa), FadeOut(da), Transform(pan, pan2), Transform(n_it, n_it2), FadeOut(lim))
        self.cue("and then each of them", Create(pb, run_time=3.5, rate_func=linear),
                 LaggedStart(*[FadeIn(d) for d in db], lag_ratio=0.05, run_time=3.5), Write(best))
        self.cue("So the learning rate", Indicate(pb, color=YELLOW_D))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 4. condition number
    def condition_number(self):
        head = self.heading("The condition number")
        kap = mts([r"\kappa=\frac{\lambda_{\max}}{\lambda_{\min}}", r"=\frac{4}{1/4}=16"], 0.85).move_to([-3.2, 1.6, 0])
        rho = mts([r"\rho(\eta^*)=\frac{\kappa-1}{\kappa+1}", r"=\frac{15}{17}\approx0.88"], 0.85).move_to([-3.2, 0.3, 0])
        assert_on_screen(kap, rho)
        self.say("How stretched the ravine is has a name. It's called the condition number, kappa, and it's the "
                 "steepest curvature divided by the flattest, which here is sixteen. Even at the best learning "
                 "rate, kappa sets the speed. In our ravine each step keeps fifteen seventeenths of the error.",
                 Write(head), Write(kap))
        self.cue("Even at the best", Write(rho))
        # table
        colx = [1.6, 3.6, 5.6]
        hdr = VGroup(txt("κ", 26, GREY_B).move_to([colx[0], 2.3, 0]), txt("rate ρ", 26, GREY_B).move_to([colx[1], 2.3, 0]),
                     txt("steps for 100×", 26, GREY_B).move_to([colx[2] + 0.1, 2.3, 0]))
        rows = VGroup()
        for i, (k, r, n) in enumerate(zip(KAPS, RHOS, ITS)):
            y = 1.65 - 0.55 * i
            col = C_LOSS if k >= 100 else (YELLOW_D if k == 16 else WHITE)
            rows.add(VGroup(txt(f"{k}", 28, col).move_to([colx[0], y, 0]), txt(f"{r:.3f}", 28, col).move_to([colx[1], y, 0]),
                            txt(f"{n}", 28, col).move_to([colx[2], y, 0])))
        assert_on_screen(hdr, rows)
        self.say("Here's what that costs. A perfectly round bowl takes one step, but at kappa one hundred we need "
                 "over two hundred steps, and at kappa one thousand, over two thousand. Stretched bowls are slow "
                 "however you tune eta, and fixing that is exactly what momentum and Adam are for.",
                 FadeIn(hdr), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.25))
        self.cue("Stretched bowls", Indicate(rows[4], color=C_LOSS), Indicate(rows[5], color=C_LOSS))
        self.hold(0.6)
        self.clear_stage()
