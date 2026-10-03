"""Episode 6 — Momentum as a Low-Pass Filter (Note 4, section 4.1, first part)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers

# (a) the exponential moving average as weights on past gradients
BETA = 0.9
KW = np.arange(0, 11)
WEIGHTS = (1 - BETA) * BETA ** KW
assert abs(WEIGHTS[0] - 0.1) < 1e-12 and abs(WEIGHTS[1] - 0.09) < 1e-12
assert abs(sum((1 - BETA) * BETA ** np.arange(0, 400)) - 1) < 1e-12
assert abs(BETA ** 10 - 0.3487) < 1e-4                           # weight has fallen to 35% after ten steps


def ema(g, beta):
    z, out = 0.0, []
    for x in g:
        z = beta * z + (1 - beta) * x
        out.append(z)
    return np.array(out)


# unrolled form z_{t+1} = (1-beta) sum_k beta^(t-k) g_k
_g = np.random.RandomState(0).randn(30)
_z = ema(_g, BETA)
assert abs(_z[-1] - (1 - BETA) * sum(BETA ** (len(_g) - 1 - k) * _g[k] for k in range(len(_g)))) < 1e-12

# (b) step response = 1 - beta^t  (RC circuit: 1 - exp(-t/RC), with beta = exp(-1/RC))
T_STEP = np.arange(0, 41)
ZSTEP = np.concatenate([[0.0], ema(np.ones(40), BETA)])
assert np.allclose(ZSTEP, 1 - BETA ** T_STEP)
RC = -1 / np.log(BETA)
assert abs(RC - 9.49) < 0.01
assert abs(1 - np.exp(-RC / RC) - 0.6321) < 1e-3 and abs(1 - BETA ** RC - 0.6321) < 1e-3

# (c) persistent + alternating gradient
C_PERS, C_ALT = 1.0, 3.0
TS = np.arange(0, 60)
GIN = C_PERS + C_ALT * (-1.0) ** TS
ZOUT = ema(GIN, BETA)
GAIN_ALT = (1 - BETA) / (1 + BETA)
assert abs(GAIN_ALT - 0.05263) < 1e-4
_alt = ZOUT[55:] - C_PERS
assert abs(np.abs(_alt).max() - C_ALT * GAIN_ALT) < 0.01, (np.abs(_alt).max(), C_ALT * GAIN_ALT)
assert abs(ZOUT[54:].mean() - C_PERS) < 0.02

# (d) two conventions give identical iterates when alpha_v = eta_z (1 - beta)
ETAZ = 0.1
ALPHAV = ETAZ * (1 - BETA)
assert abs(ALPHAV - 0.01) < 1e-12


def run_norm(gradf, w0, eta, beta, T):
    w, z, P = np.array(w0, float), 0.0 * np.array(w0, float), [np.array(w0, float)]
    for _ in range(T):
        z = beta * z + (1 - beta) * gradf(w)
        w = w - eta * z
        P.append(w.copy())
    return np.array(P)


def run_unnorm(gradf, w0, alpha, beta, T):
    w, v, P = np.array(w0, float), 0.0 * np.array(w0, float), [np.array(w0, float)]
    for _ in range(T):
        v = beta * v + gradf(w)
        w = w - alpha * v
        P.append(w.copy())
    return np.array(P)


LAM = np.array([1.0, 20.0])
GRAD = lambda w: LAM * w
_a = run_norm(GRAD, [-4, 1], ETAZ, BETA, 50)
_b = run_unnorm(GRAD, [-4, 1], ALPHAV, BETA, 50)
assert np.allclose(_a, _b)

# (e) ravine: gradient descent vs momentum on f = (w1^2 + 20 w2^2)/2
W0 = np.array([-4.0, 1.0])
ETA_GD = 0.09
ETA_M, BETA_M = 0.2, 0.5
assert ETA_GD < 2 / LAM.max()
P_GD = run_norm(GRAD, W0, ETA_GD, 0.0, 120)
P_M = run_norm(GRAD, W0, ETA_M, BETA_M, 120)


def first_below(P, tol=0.01):
    n = np.linalg.norm(P, axis=1)
    return int(np.argmax(n < tol * n[0]))


N_GD, N_M = first_below(P_GD), first_below(P_M)
assert (N_GD, N_M) == (49, 15), (N_GD, N_M)
assert abs(P_GD[1][1] + 0.8) < 1e-12 and abs(P_GD[2][1] - 0.64) < 1e-12        # y flips sign each step


class Ep06Momentum(NarratedScene):
    series = SERIES
    SCENES = ["averaging", "rc", "signals", "conventions", "ravine"]

    def construct(self):
        self.title_card()
        self.averaging()
        self.rc()
        self.signals()
        self.conventions()
        self.ravine()
        self.end_card(
            ["Momentum is one running average of past gradients, with fading weights",
             "It's a low-pass filter. Steady gradients pass, bouncing ones get squashed",
             "At beta zero point nine, an alternating gradient shrinks to about five percent",
             "Libraries disagree about the factor of one minus beta. Convert before comparing learning rates",
             "It calms the zigzag in a ravine. A guaranteed speed-up needs more"],
        )

    # ---------------------------------------------------------------- 1. averaging
    def averaging(self):
        head = self.heading("Averaging recent gradients")
        prob = txt("A learning rate safe for the stiff direction crawls along the soft one.", 26, GREY_B).move_to([0, 2.5, 0])
        prob2 = txt("A larger one makes the stiff direction overshoot and bounce.", 26, C_LOSS).move_to([0, 1.8, 0])
        assert_on_screen(prob, prob2)
        self.say("Remember the ravine? A step that's small enough for the stiff direction just crawls along the soft "
                 "one, and a bigger step makes the stiff direction overshoot and bounce. So what if we averaged "
                 "the recent gradients, instead of trusting only the newest one?",
                 Write(head), FadeIn(prob), run_time=0.8)
        self.cue("and a bigger step", FadeIn(prob2))
        rec =mts([r"z_{t+1}=", r"\beta z_t", r"+", r"(1-\beta)\nabla f(w_t)", r",\quad w_{t+1}=w_t-\eta z_{t+1}"], 0.8,
                  {1: C_MOM, 3: C_GRAD}).move_to([0, 0.5, 0])
        unroll = mts([r"z_{t+1}=(1-\beta)\sum_{k=0}^{t}\beta^{\,t-k}\,\nabla f(w_k)"], 0.8, {}).move_to([0, -0.7, 0])
        assert_on_screen(rec, unroll)
        self.say("So we keep a running average. At each step we shrink the old average by beta, and then mix in a "
                 "little of the newest gradient. Unroll that and it's a weighted sum of every past gradient, where "
                 "each step back in time shrinks the weight by another factor of beta.",
                 FadeOut(prob), FadeOut(prob2), Write(rec), run_time=1.2)
        self.cue("Unroll that", Write(unroll))
        self.hold(0.3)
        self.play(FadeOut(rec), FadeOut(unroll))
        ax = Axes(x_range=[0, 10.5, 1], y_range=[0, 0.12, 0.05], x_length=8.0, y_length=2.6,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([-1.5, 0.3, 0])
        bars = VGroup(*[Rectangle(width=0.5, height=max(ax.c2p(0, w)[1] - ax.c2p(0, 0)[1], 0.01), color=C_MOM, fill_opacity=0.85, stroke_width=1)
                        .move_to(ax.c2p(k, 0), aligned_edge=DOWN) for k, w in zip(KW, WEIGHTS)])
        xt = VGroup(*[txt(f"{k}", 20, GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.12) for k in (0, 2, 4, 6, 8, 10)])
        xl = txt("how many steps ago", 22, GREY_B).next_to(ax.x_axis, DOWN, buff=0.5)
        yt = VGroup(*[txt(f"{v:g}", 20, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.4) for v in (0, 0.05, 0.1)])
        yl = txt("weight on that gradient, β = 0.9", 22, GREY_B).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        note = txt("after ten steps the weight is\nstill 35% of the newest", 22, C_MOM).move_to([4.6, 0.6, 0])
        assert_on_screen(VGroup(ax, xt, xl, yt, yl), note)
        rm = txt("Equal weights would fade old gradients only like 1/t.", 24, YELLOW_D).move_to([0, -2.25, 0])
        assert_on_screen(rm)
        self.say("With beta at zero point nine, the newest gradient gets a weight of zero point one. The one before "
                 "it gets zero point zero nine, and so on down, yet a single stored vector holds it all. Why not "
                 "weigh them all equally? Because then a huge, stale gradient would hang around for ages, while "
                 "exponential weights forget it.",
                 Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(yt), FadeIn(yl), LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars], lag_ratio=0.1, run_time=2.5))
        self.cue("Why not", FadeIn(rm))
        self.cue("while exponential", FadeIn(note))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 2. RC circuit
    def rc(self):
        head = self.heading("The RC circuit analogy")
        ax = Axes(x_range=[0, 40, 10], y_range=[0, 1.1, 0.5], x_length=7.0, y_length=3.0,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([-2.6, -0.1, 0])
        xt = VGroup(*[txt(f"{v}", 20, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.12) for v in (0, 10, 20, 30, 40)])
        yt = VGroup(*[txt(f"{v:g}", 20, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12) for v in (0, 0.5, 1)])
        xl = txt("steps t", 22, GREY_B).next_to(ax.x_axis, DOWN, buff=0.45)
        yl = txt("average after the gradient jumps to 1", 22, GREY_B).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        one = DashedLine(ax.c2p(0, 1), ax.c2p(40, 1), color=GREY_A, stroke_width=2)
        curve = polyline(ax, T_STEP, ZSTEP, C_MOM, 4)
        lab = mts([r"1-\beta^{t}", r"\ \leftrightarrow\ ", r"V\,(1-e^{-t/RC})"], 0.75, {0: C_MOM}).move_to([4.1, 0.9, 0])
        sub = txt("charging a capacitor: one stored state", 22, GREY_B).move_to([4.1, 0.1, 0])
        tau = txt(f"time constant ≈ {RC:.1f} steps", 22, C_MOM).move_to([4.1, -0.6, 0])
        assert_on_screen(VGroup(ax, xt, yt, xl, yl), lab, sub, tau)
        self.say("An electric circuit does the same thing. A resistor and a capacitor hold one stored state, and "
                 "that state charges up smoothly. Momentum is the step-by-step version, so if the gradient "
                 "suddenly jumps to one, the average creeps up toward it like this.",
                 Write(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), Create(one), FadeIn(sub), run_time=1.5)
        self.cue("Momentum is the", Create(curve, run_time=2.5), Write(lab))
        self.say("With beta at zero point nine, the memory is about nine and a half steps. That's roughly how long "
                 "the average takes to catch up with a change.",
                 FadeIn(tau))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 3. signals
    def signals(self):
        head = self.heading("Keeping the trend, dropping the bounce")
        ax = Axes(x_range=[0, 40, 10], y_range=[-3, 5, 2], x_length=8.4, y_length=3.3,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([-1.3, 0.3, 0])
        xt = VGroup(*[txt(f"{v}", 20, GREY_B).next_to(ax.c2p(v, -3), DOWN, buff=0.12) for v in (0, 10, 20, 30, 40)])
        yt = VGroup(*[txt(f"{v}", 20, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12) for v in (-2, 0, 2, 4)])
        xl = txt("steps t", 22, GREY_B).next_to(ax.c2p(20, -3), DOWN, buff=0.5)
        pers = DashedLine(ax.c2p(0, C_PERS), ax.c2p(40, C_PERS), color=GREY_A, stroke_width=2)
        gin = polyline(ax, TS[:41], GIN[:41], C_NOISE, 2)
        gdot = dots(ax, TS[:41], GIN[:41], C_NOISE, 0.05)
        zl = polyline(ax, TS[:41], ZOUT[:41], C_MOM, 4)
        l1 = txt("gradient: 1 plus a bounce of ±3", 22, C_NOISE).move_to([4.5, 2.0, 0])
        l2 = txt("momentum average", 22, C_MOM).move_to([4.5, 1.3, 0])
        assert_on_screen(VGroup(ax, xt, yt, xl), l1, l2)
        self.say("Now feed in a steady gradient of one, with a bounce on top that flips sign at every step, the way "
                 "a stiff direction does. The average settles on the steady value, and the bounce nearly vanishes, "
                 "which is exactly what a low-pass filter does.",
                 Write(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), Create(pers), Create(gin), FadeIn(gdot), FadeIn(l1))
        self.cue("The average settles", Create(zl, run_time=3), FadeIn(l2))
        g1 = mts([r"g_t=c"], 0.75, {}).move_to([5.0, 0.3, 0])
        g2 = mts([r"z_\infty=c"], 0.75, {}).move_to([5.0, -0.3, 0])
        g3 = mts([r"g_t=(-1)^t c"], 0.75, {}).move_to([5.0, -0.85, 0])
        g4 = mts([r"\frac{|z|}{|c|}=\frac{1-\beta}{1+\beta}\approx0.05"], 0.75, {0: C_MOM}).move_to([5.0, -1.9, 0])
        assert_on_screen(g1, g2, g3, g4)
        self.say("We can put numbers on that. A steady gradient passes straight through, while an alternating one "
                 "gets cut down by this ratio. For beta at zero point nine that's about five percent, so the "
                 "trend survives and the bounce is basically gone.",
                 Write(g1), Write(g2), run_time=1.2)
        self.cue("while an alternating", Write(g3), Write(g4))
        self.cue("For beta at", Indicate(g4, color=YELLOW_D))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 4. conventions
    def conventions(self):
        head = self.heading("Two conventions in the wild")
        n = mts([r"z_{t+1}=\beta z_t+(1-\beta)\nabla f(w_t)", r",\quad w_{t+1}=w_t-\eta z_{t+1}"], 0.75, {0: C_MOM}).move_to([0, 2.4, 0])
        u = mts([r"v_{t+1}=\beta v_t+\nabla f(w_t)", r",\quad w_{t+1}=w_t-\alpha v_{t+1}"], 0.75, {0: C_V2}).move_to([0, 1.3, 0])
        rel = mts([r"v_t=\frac{z_t}{1-\beta}", r",\qquad \alpha=\eta\,(1-\beta)"], 0.8, {}).move_to([0, 0.0, 0])
        ex = mts([r"\beta=0.9:\ \ \eta=0.1\ \Longleftrightarrow\ \alpha=0.01"], 0.8, {}).move_to([0, -1.1, 0])
        st = mts([r"\text{constant gradient }c:\ \ z_\infty=c,\ \ v_\infty=\frac{c}{1-\beta}=10\,c"], 0.7, {}).move_to([0, -2.1, 0])
        assert_on_screen(n, u, rel, ex, st, ymin=-2.5)
        assert abs(1 / (1 - BETA) - 10) < 1e-9
        self.say("Here's a trap to watch for. Many libraries drop the factor of one minus beta and just add up the "
                 "raw gradients, which is the unnormalized convention. With beta at zero point nine that running "
                 "sum is ten times bigger, so its learning rate has to be ten times smaller to match.",
                 Write(head), Write(n), run_time=1.2)
        self.cue("Many libraries", Write(u))
        self.cue("With beta at", Write(rel))
        self.say("So a learning rate of zero point one in the first form is zero point zero one in the second. "
                 "Always convert before you compare learning rates across libraries.",
                 Write(ex), Write(st))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 5. ravine
    def ravine(self):
        head = self.heading("A ravine, with and without momentum")
        ax = Axes(x_range=[-4.5, 4.5, 1], y_range=[-1.5, 1.5, 1], x_length=8.4, y_length=3.4,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([-1.6, -0.15, 0])
        cont = contour_family(ax, (1.0, 20.0), [16.0, 9.0, 4.0, 1.0, 0.16])
        gd = path_pts(ax, [tuple(p) for p in P_GD[:N_GD + 1]], C_LOSS, 3)
        gdd = path_dots(ax, [tuple(p) for p in P_GD[:N_GD + 1]], C_LOSS, 0.045)
        mm = path_pts(ax, [tuple(p) for p in P_M[:N_M + 1]], C_MOM, 4)
        mmd = path_dots(ax, [tuple(p) for p in P_M[:N_M + 1]], C_MOM, 0.06)
        l1 = VGroup(txt(f"gradient descent, η = {ETA_GD}", 22, C_LOSS), txt(f"{N_GD} steps to shrink the distance 100×", 20, C_LOSS)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        l2 = VGroup(txt(f"momentum, β = {BETA_M}, η = {ETA_M}", 22, C_MOM), txt(f"{N_M} steps to shrink the distance 100×", 20, C_MOM)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        lg = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.6, 1.0, 0])
        assert_on_screen(VGroup(ax, cont), lg)
        self.say("Let's go back to a ravine, steep across and shallow along. Plain gradient descent zigzags its way "
                 "down. Now average the gradients, and the bounces across cancel while the push along adds up, so "
                 "it takes fifteen steps instead of forty-nine.",
                 Write(head), Create(ax), Create(cont))
        self.cue("Plain gradient descent", Create(gd, run_time=3), FadeIn(gdd), FadeIn(l1))
        self.cue("Now average", Create(mm, run_time=2), FadeIn(mmd), FadeIn(l2))
        cav = txt("Filtering is not acceleration: speed-up guarantees need tuned parameters.", 22, YELLOW_D).move_to([0, -2.15, 0])
        assert_on_screen(cav)
        self.say("A word of caution before we move on. What we've shown is filtering, and the famous square root "
                 "of kappa speed-up needs tuned parameters and a strongly convex loss.",
                 FadeIn(cav))
        self.hold(0.6)
        self.clear_stage()
