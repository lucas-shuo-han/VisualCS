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

    def construct(self):
        self.title_card()
        self.equations()
        self.scalar_case()
        self.two_directions()
        self.condition_number()
        self.end_card(
            ["On a quadratic, gradient descent is a linear system: every error mode is multiplied by its own factor",
             "That factor is one minus two eta lambda, so stability needs eta below one over lambda max",
             "The steepest direction sets the speed limit; the flattest sets the pace",
             "Condition number kappa is lambda max over lambda min: large kappa means slow, even at the best eta"],
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
        self.say("Least squares is a lamppost: the geometry is explicit, so we can watch exactly what optimization does.",
                 Write(head), Write(loss))
        self.say("The loss is the squared length of the residual, and its gradient is two X transpose times the residual.",
                 Write(grad))
        self.say("A gradient step with learning rate eta subtracts eta times that gradient.", Write(step))
        self.say("Expand it and the step is a fixed linear map applied to the weights, plus a constant.",
                 ReplacementTransform(step, upd))
        self.hold(0.3)
        self.play(FadeOut(loss), FadeOut(grad), upd.animate.move_to([0, 1.6, 0]))
        err.move_to([0, 0.2, 0])
        dfn.move_to([0, -0.9, 0])
        box = SurroundingRectangle(VGroup(err[1], err[2], err[3]), color=YELLOW_D, buff=0.1)
        self.say("Subtract the minimizer and the constant vanishes: the error is multiplied by the same matrix at every step.",
                 Write(err), FadeIn(dfn))
        self.say("Optimizing a quadratic is therefore a linear dynamical system, and its eigenvalues decide everything.",
                 Create(box))
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
        self.say("In the eigenbasis of X transpose X, a problem splits into scalar ones. Start with one, sigma times w equals y.",
                 Write(head), Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yt), Create(star), FadeIn(sl), Write(prob))
        self.say("Each gradient step multiplies the error by the same number, r equals one minus two eta sigma squared.",
                 Write(rec))

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

        caps = [
            "A small learning rate gives r between zero and one: the error shrinks smoothly, but slowly.",
            "At eta equal to one over two sigma squared, r is zero, and a single step lands exactly on the answer.",
            "Push eta higher and r turns negative: the iterate overshoots, bounces across the answer, and still settles.",
            "Past eta equal to one over sigma squared, r falls below minus one, and every bounce is bigger than the last.",
        ]
        pan = panel(0)
        cur = curve(0)
        self.say(caps[0], FadeIn(pan), Create(cur[0], run_time=1.5), LaggedStart(*[FadeIn(d) for d in cur[1]], lag_ratio=0.1, run_time=1.5))
        for k in range(1, 4):
            new_pan, new_cur = panel(k), curve(k)
            self.say(caps[k], Transform(pan, new_pan), Transform(cur, new_cur))
            self.hold(0.3)
        cond = mts([r"|1-2\eta\sigma^2|<1\iff 0<\eta<\frac{1}{\sigma^2}"], 0.8, {})
        cond.move_to([4.0, 2.4, 0])
        assert_on_screen(cond)
        self.say("So the scalar rule is simple: the iteration is stable exactly when the absolute value of r is below one.",
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
        self.say("Now two directions: a ravine, steep where sigma is 2 and shallow where sigma is one half.",
                 Write(head), Create(ax), LaggedStart(*[Create(c) for c in cont], lag_ratio=0.15), FadeIn(xl), FadeIn(yl))

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
        self.say("Take eta equal to 0.2. Each step multiplies the steep coordinate by minus 0.6 and the shallow one by 0.9.",
                 FadeIn(start), FadeIn(pan))
        self.say("The path bounces across the ravine while creeping along it: the shallow direction sets the pace.",
                 Create(pa, run_time=3.5, rate_func=linear), LaggedStart(*[FadeIn(d) for d in da], lag_ratio=0.05, run_time=3.5))
        n_it = txt(f"{IT_A} steps for a 100× smaller error", 22, C_SOFT).next_to(pan, DOWN, buff=0.4).align_to(pan, LEFT)
        assert_on_screen(n_it)
        self.say("The steepest direction forbids a bigger step: eta must stay below one over lambda max, not lambda min.",
                 FadeIn(n_it))
        lim = mts([r"\eta<\frac{1}{\lambda_{\max}}", r"=\frac{1}{4}"], 0.75, {0: C_ETA}).next_to(n_it, DOWN, buff=0.35).align_to(pan, LEFT)
        assert_on_screen(lim)
        self.play(Write(lim))
        self.hold(0.3)
        # eta star
        pan2 = factors(1 - 2 * ETA_STAR * LAM_STEEP, 1 - 2 * ETA_STAR * LAM_SOFT, ETA_STAR)
        n_it2 = txt(f"{IT_STAR} steps for a 100× smaller error", 22, GREEN_C).next_to(pan2, DOWN, buff=0.4).align_to(pan2, LEFT)
        pb = path_pts(ax, P_STAR, color=GREEN_C)
        db = path_dots(ax, P_STAR, color=GREEN_C)
        assert_on_screen(pan2, n_it2)
        best = mts([r"\eta^*=\frac{1}{\lambda_{\max}+\lambda_{\min}}=0.235"], 0.7, {0: C_ETA}).next_to(n_it2, DOWN, buff=0.35).align_to(pan2, LEFT)
        assert_on_screen(best)
        self.say("The best constant rate balances the two extremes, equal and opposite. Now both modes shrink by 0.88 per step.",
                 FadeOut(pa), FadeOut(da), Transform(pan, pan2), Transform(n_it, n_it2), FadeOut(lim))
        self.play(Create(pb, run_time=3.5, rate_func=linear), LaggedStart(*[FadeIn(d) for d in db], lag_ratio=0.05, run_time=3.5), Write(best))
        self.say("Even the best constant learning rate is still slow. The ravine itself is the problem.",
                 Indicate(pb, color=YELLOW_D))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 4. condition number
    def condition_number(self):
        head = self.heading("The condition number")
        kap = mts([r"\kappa=\frac{\lambda_{\max}}{\lambda_{\min}}", r"=\frac{4}{1/4}=16"], 0.85).move_to([-3.2, 1.6, 0])
        rho = mts([r"\rho(\eta^*)=\frac{\kappa-1}{\kappa+1}", r"=\frac{15}{17}\approx0.88"], 0.85).move_to([-3.2, 0.3, 0])
        assert_on_screen(kap, rho)
        self.say("The ratio of the largest to the smallest eigenvalue is the condition number, kappa. Here it is 16.",
                 Write(head), Write(kap))
        self.say("At the best rate the error shrinks by kappa minus one over kappa plus one per step: 15 over 17 here.",
                 Write(rho))
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
        self.say("Iterations grow with kappa: one for a round bowl, over two hundred at kappa 100, over two thousand at 1000.",
                 FadeIn(hdr), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.25))
        self.say("Large condition number means slow convergence even when stable. Momentum and Adam will attack exactly this.",
                 Indicate(rows[4], color=C_LOSS), Indicate(rows[5], color=C_LOSS))
        self.hold(0.6)
        self.clear_stage()
