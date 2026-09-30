"""Episode 9 — Standardize Inputs, Initialize Weights (Lecture 3: "Stepping back", initialization)."""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers

# (a) conditioning of a raw feature in [100, 200] with an intercept column
XR = np.linspace(100, 200, 50)
XS = (XR - XR.mean()) / XR.std()
KAP_RAW = float(np.linalg.cond(np.c_[XR, np.ones(50)]) ** 2)             # kappa of X^T X
KAP_STD = float(np.linalg.cond(np.c_[XS, np.ones(50)]) ** 2)
assert 5e5 < KAP_RAW < 7e5 and abs(KAP_STD - 1) < 1e-9
STEPS = lambda k: float(np.log(0.01) / np.log((k - 1) / (k + 1)))
N_RAW, N_STD = STEPS(KAP_RAW), STEPS(1.0000001)
assert 1.2e6 < N_RAW < 1.6e6
assert abs(XS.mean()) < 1e-12 and abs(XS.std() - 1) < 1e-12

# (b) corners of ReLU(w x + b) with w, b ~ N(0, 1): the kink sits at -b/w, a standard Cauchy variable
CAUCHY = lambda a: 2 / math.pi * math.atan(a)                            # P(|corner| < a)
assert abs(CAUCHY(1) - 0.5) < 1e-12 and abs(CAUCHY(2) - 0.7048) < 1e-3
assert abs(CAUCHY(3) - 0.7952) < 1e-3 and abs(CAUCHY(7) - 0.9097) < 1e-3
P_IN = (math.atan(200) - math.atan(100)) / math.pi
assert abs(P_IN - 0.00159) < 1e-5                                         # about 0.16% per unit
assert abs(1000 * P_IN - 1.59) < 0.01
_r = np.random.RandomState(0)
D_H = 1000
WH = _r.randn(D_H)
BH = _r.randn(D_H)
_c = -BH / WH
_feat = lambda x: np.maximum(0, np.outer(x, WH) + BH)


def numrank(H):
    s = np.linalg.svd(H, compute_uv=False)
    return int((s > 1e-8 * s[0]).sum()), s


RANK_RAW, SV_RAW = numrank(_feat(XR))
RANK_STD, SV_STD = numrank(_feat(XS))
assert RANK_RAW == 3 and RANK_STD == 50
CORN_RAW = int(((_c > XR.min()) & (_c < XR.max())).sum())
CORN_STD = int(((_c > XS.min()) & (_c < XS.max())).sum())
assert CORN_RAW == 1 and CORN_STD > 500

# (c) forward signal through a deep ReLU net for three initialisations
DW, LAYERS = 256, 10
_r2 = np.random.RandomState(1)
INITS = [("N(0, 1)", 1.0, C_LOSS), ("Xavier: N(0, 1/d)", 1.0 / DW, C_MODEL), ("He: N(0, 2/d)", 2.0 / DW, C_TRAIN)]
LOGMS = {}
for _n, _v, _c2 in INITS:
    _h = _r2.randn(2000, DW)
    _ms = []
    for _l in range(LAYERS):
        _h = np.maximum(0, _h @ (_r2.randn(DW, DW) * np.sqrt(_v)))
        _ms.append(np.log10((_h ** 2).mean()))
    LOGMS[_n] = np.array(_ms)
assert LOGMS["N(0, 1)"][-1] > 15                                       # explodes by ~2.1 decades per layer
assert LOGMS["Xavier: N(0, 1/d)"][-1] < -2.5                           # halves each layer: 10 log10(1/2) = -3.0
assert abs(LOGMS["He: N(0, 2/d)"]).max() < 0.4
assert abs(LOGMS["Xavier: N(0, 1/d)"][-1] - LAYERS * math.log10(0.5)) < 0.6
assert abs(LOGMS["N(0, 1)"][0] - math.log10(DW / 2)) < 0.1
# a linear layer with Xavier keeps variance one
_h = _r2.randn(4000, DW)
_w = _r2.randn(DW, DW) / np.sqrt(DW)
assert abs((_h @ _w).var() - 1) < 0.05
# Var(sum w_i h_i) = d * E[w^2] E[h^2] = 1 for w ~ N(0, 1/d), zero-mean independent
assert abs(DW * (1 / DW) * 1.0 - 1) < 1e-12
# Glorot with d_in = d_out = d equals Xavier
assert abs(2 / (DW + DW) - 1 / DW) < 1e-15


class Ep09StandardizeInit(NarratedScene):
    series = SERIES

    def construct(self):
        self.title_card()
        self.conditioning()
        self.corners()
        self.rank()
        self.init_intro()
        self.deep()
        self.end_card(
            ["Standardize features to zero mean and unit variance: better conditioning and fewer numerical problems",
             "A ReLU kink at minus b over w is Cauchy distributed: it rarely lands in data far from zero, and expressive power is lost",
             "Inspect the rank or singular values of the feature matrix when a model seems unexpectedly weak",
             "Initialize so each layer's inputs look standardized: Xavier one over d, He two over d for ReLU, Glorot two over d in plus d out"],
        )

    # ---------------------------------------------------------------- 1. conditioning
    def conditioning(self):
        head = self.heading("Why standardize?")
        b1 = box_label("features on similar scales: better conditioning", C_TRAIN, w=8.6, h=0.9, font_size=26).move_to([0, 2.3, 0])
        b2 = box_label("otherwise large features dominate the prediction", C_LOSS, w=8.6, h=0.9, font_size=26).move_to([0, 1.1, 0])
        b3 = box_label("and numbers of very different sizes lose precision", C_SOFT, w=8.6, h=0.9, font_size=26).move_to([0, -0.1, 0])
        assert_on_screen(b1, b2, b3)
        self.say("Why standardize? First, features should have similar sizes; else one in the thousands dominates one near one.",
                 Write(head), FadeIn(b1, shift=UP * 0.2), FadeIn(b2, shift=UP * 0.2))
        self.say("Second, there are numerical issues: mixing huge and tiny values wastes floating-point precision.",
                 FadeIn(b3, shift=UP * 0.2))
        self.play(FadeOut(b1), FadeOut(b2), FadeOut(b3))
        setup = mts([r"X=[\,x\ \ 1\,],\quad x\in[100,200]"], 0.8, {}).move_to([-3.4, 2.4, 0])
        raw = VGroup(txt("raw", 26, C_LOSS), mt(rf"\kappa(X^\top X)\approx{KAP_RAW / 1e5:.1f}\times10^5", 0.85, C_LOSS),
                     txt(f"about {N_RAW / 1e6:.1f} million steps to shrink the error 100×", 22, C_LOSS)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([-3.2, 0.9, 0])
        std = VGroup(txt("standardized", 26, C_TRAIN), mt(r"\kappa(X^\top X)=1", 0.85, C_TRAIN),
                     txt("one step lands on the answer", 22, C_TRAIN)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([-3.2, -1.2, 0])
        ax = Axes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], x_length=3.0, y_length=3.0,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([4.2, 0.4, 0])
        ax2 = Axes(x_range=[100, 200, 50], y_range=[0, 1, 1], x_length=3.0, y_length=0.3,
                   axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([4.2, -1.8, 0])
        assert_on_screen(setup, raw, std, ax, ax2)
        self.say("Take a feature that runs from 100 to 200, plus an intercept column. The two columns nearly point the same way.",
                 Write(setup), FadeIn(raw))
        self.say("The condition number is about six hundred thousand. Subtract the mean, divide by the deviation: exactly one.",
                 FadeIn(std))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 2. corners
    def corners(self):
        head = self.heading("Why the kink must land in the data")
        net = mts([r"h=\max(0,\ wx+b)"], 0.9, {}).move_to([-4.2, 2.3, 0])
        init = mts([r"w,\,b\sim\mathcal N(0,1)"], 0.8, {}).move_to([-4.2, 1.4, 0])
        cor = mts([r"\text{kink at }x=-\frac bw\ \sim\ \text{Cauchy}"], 0.85, {}).move_to([-2.9, 0.2, 0])
        pdf = mts([r"\text{pdf}=\frac1\pi\,\frac1{x^2+1}"], 0.75, {}).move_to([-3.7, -0.9, 0])
        ax = Axes(x_range=[-8, 8, 4], y_range=[0, 0.35, 0.1], x_length=6.0, y_length=2.6,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([3.0, 1.0, 0])
        cauchy = plot(ax, lambda x: 1 / (math.pi * (x ** 2 + 1)), C_RAMP, [-8, 8], 4)
        xt = VGroup(*[txt(f"{v}", 20, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.12) for v in (-8, -4, 0, 4, 8)])
        assert_on_screen(net, init, cor, pdf, VGroup(ax, xt))
        self.say("A ReLU unit bends at x equal to minus b over w. With standard normal w and b, that kink is a Cauchy variable.",
                 Write(head), Write(net), Write(init), Write(cor), Write(pdf), Create(ax), FadeIn(xt), Create(cauchy))
        rows = VGroup(*[VGroup(txt(f"|kink| < {a}", 22, WHITE), txt(f"{CAUCHY(a) * 100:.0f}%", 22, C_RAMP)).arrange(RIGHT, buff=0.3) for a in (1, 2, 3, 7)]).arrange_in_grid(2, 2, buff=(0.6, 0.15)).move_to([2.2, -1.95, 0])
        hv = txt("mean zero, infinite variance, yet mostly near zero", 22, GREY_B).move_to([3.0, -1.0, 0])
        assert_on_screen(rows, hv)
        self.say("Its variance is infinite, yet half its mass lies within one of zero, and ninety percent within seven.",
                 FadeIn(rows), FadeIn(hv))
        self.play(FadeOut(net), FadeOut(init), FadeOut(cor), FadeOut(pdf), FadeOut(ax), FadeOut(xt), FadeOut(cauchy), FadeOut(rows), FadeOut(hv))
        ln = NumberLine(x_range=[-100, 300, 100], length=10.0, color=GREY_B, include_numbers=False, tick_size=0.1).move_to([0, 1.2, 0])
        lab = VGroup(*[txt(f"{v}", 20, GREY_B).next_to(ln.n2p(v), DOWN, buff=0.12) for v in (-100, 0, 100, 200, 300)])
        band = Rectangle(width=ln.n2p(200)[0] - ln.n2p(100)[0], height=0.7, color=C_DATA, fill_opacity=0.35, stroke_width=1).move_to(ln.n2p(150) + UP * 0.35)
        bl = txt("data: 100 to 200", 22, C_DATA).next_to(band, UP, buff=0.1)
        res = mts([rf"P(\text{{kink in }}[100,200])\approx{P_IN * 100:.2f}\%", rf"\ \Rightarrow\ \approx{D_H * P_IN:.1f}\text{{ of }}1000\text{{ units}}"], 0.75, {}).move_to([0, -0.4, 0])
        assert_on_screen(VGroup(ln, lab, band, bl), res)
        self.say("Now suppose the data live between 100 and 200. A kink lands there with chance about 0.16 percent per unit.",
                 FadeIn(ln), FadeIn(lab), FadeIn(band), FadeIn(bl), Write(res[0]))
        self.say("Among a thousand hidden units, only one or two bend inside the data. The rest are zero or straight lines.",
                 Write(res[1]))
        cn = txt("We want the data to sit where the nonlinearity is interesting: true for tanh and sigmoid too.", 24, YELLOW_D).move_to([0, -1.7, 0])
        assert_on_screen(cn)
        self.say("Non-standardized data thus wastes the nonlinearity's expressive power. The same holds for tanh and sigmoid.",
                 FadeIn(cn))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 3. rank
    def rank(self):
        head = self.heading("Debugging tip: inspect the rank")
        form = mts([r"h_i(x)=\begin{cases}0\\ \alpha_i x+\beta_i\end{cases}\ \text{ for all }x\text{ in the data, if no kink there}"], 0.7, {}).move_to([0, 2.4, 0])
        sm = mts([r"H=\sum\ \text{(rank-one matrices)}\ \Rightarrow\ \text{rank}\ \approx 3"], 0.75, {}).move_to([0, 1.5, 0])
        assert_on_screen(form, sm)
        self.say("A unit with no kink in the data is zero or a straight line there. All thousand stack into a few rank-one pieces.",
                 Write(head), Write(form), Write(sm))
        ax1 = Axes(x_range=[0, 6, 1], y_range=[-8, 5, 4], x_length=5.0, y_length=2.0,
                   axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([-3.5, -0.2, 0])
        ax2 = ax1.copy().move_to([3.2, -0.2, 0])
        k = 6
        b1 = VGroup(*[Rectangle(width=0.4, height=max(ax1.c2p(0, np.log10(max(s, 1e-14)))[1] - ax1.c2p(0, -8)[1], 0.03), color=C_LOSS, fill_opacity=0.85, stroke_width=1)
                      .move_to(ax1.c2p(i + 0.5, -8), aligned_edge=DOWN) for i, s in enumerate(SV_RAW[:k])])
        b2 = VGroup(*[Rectangle(width=0.4, height=max(ax2.c2p(0, np.log10(s))[1] - ax2.c2p(0, -8)[1], 0.03), color=C_TRAIN, fill_opacity=0.85, stroke_width=1)
                      .move_to(ax2.c2p(i + 0.5, -8), aligned_edge=DOWN) for i, s in enumerate(SV_STD[:k])])
        t1 = txt(f"raw: numerical rank {RANK_RAW} of 50", 22, C_LOSS).next_to(ax1, UP, buff=0.15)
        t2 = txt(f"standardized: rank {RANK_STD}", 22, C_TRAIN).next_to(ax2, UP, buff=0.15)
        sv = txt("first six singular values (log scale)", 20, GREY_B).next_to(VGroup(ax1, ax2), DOWN, buff=0.3).set_x(-0.2)
        assert_on_screen(VGroup(ax1, t1), VGroup(ax2, t2), sv)
        self.say("Take 50 data points. The raw feature matrix has only three singular values above zero; standardized, all fifty.",
                 Create(ax1), Create(ax2), FadeIn(b1), FadeIn(b2), FadeIn(t1), FadeIn(t2), FadeIn(sv))
        tip = txt("Oddly weak network? Check the rank of its features.", 24, YELLOW_D).move_to([0, -2.15, 0])
        assert_on_screen(tip)
        self.say("That gives a cheap debugging check: when a model seems weak, look at the rank of its features.",
                 FadeIn(tip))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 4. init intro
    def init_intro(self):
        head = self.heading("Initialization: start every layer standardized")
        rows = VGroup(box_label("all zeros?", C_LOSS, w=2.6, h=0.8, font_size=26),
                      txt("gradients vanish and the weights never move", 24, C_LOSS)).arrange(RIGHT, buff=0.4).move_to([0, 2.3, 0])
        key = txt("Key observation: the outputs of one layer are the inputs of the next.", 24, YELLOW_D).move_to([0, 1.1, 0])
        goal = txt("Goal: every layer's inputs start out roughly zero-mean, unit-variance.", 24, C_TRAIN).move_to([0, 0.2, 0])
        assert_on_screen(rows, key, goal)
        self.say("How to initialize? All zeros fails: everything is multiplied by zero, gradients vanish, nothing moves.",
                 Write(head), FadeIn(rows))
        self.say("Key observation: one layer's outputs feed the next, so every layer's inputs should look standardized.",
                 FadeIn(key), FadeIn(goal))
        self.play(FadeOut(rows), FadeOut(key), FadeOut(goal))
        xa = mts([r"\mathrm{Var}\Big(\sum_{i=1}^{d}w_ih_i\Big)=\sum_{i=1}^d\mathbb E[w_i^2]\,\mathbb E[h_i^2]=d\,\mathbb E[w^2]"], 0.8, {}).move_to([0, 2.3, 0])
        xb = mts([r"\text{unit-variance inputs}\ \Rightarrow\ ", r"w_i\sim\mathcal N\!\Big(0,\frac1d\Big)", r"\quad d=\text{fan-in}"], 0.85, {1: C_MODEL}).move_to([0, 1.1, 0])
        xc = txt("Xavier initialization", 28, C_MODEL).move_to([0, 0.1, 0])
        assert_on_screen(xa, xb, xc)
        self.say("For d independent, zero-mean, unit-variance inputs, the output variance is d times the weight variance.",
                 Write(xa))
        self.say("Choose weight variance one over d, the fan-in, and the output is unit-variance too: Xavier initialization.",
                 Write(xb), FadeIn(xc))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 5. deep net
    def deep(self):
        head = self.heading("Does it keep the signal alive?")
        ax = Axes(x_range=[1, LAYERS, 1], y_range=[-4, 22, 5], x_length=7.6, y_length=3.4,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([-1.9, 0.2, 0])
        xt = VGroup(*[txt(f"{v}", 20, GREY_B).next_to(ax.c2p(v, -4), DOWN, buff=0.12) for v in (1, 4, 7, 10)])
        yt = VGroup(*[txt(lb, 20, GREY_B).next_to(ax.c2p(1, v), LEFT, buff=0.12) for v, lb in ((0, "1"), (10, "10¹⁰"), (20, "10²⁰"))])
        xl = txt("layer", 22, GREY_B).next_to(ax.x_axis, DOWN, buff=0.45)
        yl = txt("mean square of the activations", 22, GREY_B).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        one = DashedLine(ax.c2p(1, 0), ax.c2p(LAYERS, 0), color=GREY_A, stroke_width=2)
        curves = {n: polyline(ax, np.arange(1, LAYERS + 1), LOGMS[n], c, 4) for n, _, c in INITS}
        labs = VGroup(*[txt(n, 22, c) for n, _, c in INITS]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.9, 1.2, 0])
        setup = txt(f"ReLU network, width {DW}, {LAYERS} layers", 22, GREY_B).move_to([4.6, 2.35, 0])
        assert_on_screen(VGroup(ax, xt, yt, xl, yl), labs, setup)
        self.say("Push standardized inputs through ten ReLU layers of width 256, with three weight choices, tracking size.",
                 Write(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), Create(one), FadeIn(setup))
        self.say("Standard normal weights make the signal explode by two orders of magnitude every layer.",
                 Create(curves["N(0, 1)"], run_time=2), FadeIn(labs[0]))
        self.say("Xavier suits a linear layer, but a ReLU zeroes half its outputs, so the signal halves each layer and fades.",
                 Create(curves["Xavier: N(0, 1/d)"], run_time=2), FadeIn(labs[1]))
        he = mts([r"\text{He: }\mathcal N\!\Big(0,\frac{1}{d/2}\Big)=\mathcal N\!\Big(0,\frac2d\Big)"], 0.75, {}).move_to([4.7, -0.5, 0])
        glo = mts([r"\text{Glorot: }\mathcal N\!\Big(0,\frac{2}{d_{\rm in}+d_{\rm out}}\Big)"], 0.75, {}).move_to([4.7, -1.5, 0])
        assert_on_screen(he, glo)
        self.say("He initialization compensates: half the inputs are alive, so use variance two over d. The signal stays level.",
                 Create(curves["He: N(0, 2/d)"], run_time=2), FadeIn(labs[2]), Write(he))
        self.say("Glorot uses two over fan-in plus fan-out, balancing forward and backward passes. For equal widths it is Xavier.",
                 Write(glo))
        bias = txt("Biases: start at 0, or at a small number like 0.01.", 22, YELLOW_D).move_to([0, -2.35, 0])
        assert_on_screen(bias)
        self.say("Biases are simple: start at zero, use a small constant such as 0.01, or treat the bias as one more weight.",
                 FadeIn(bias))
        self.hold(0.6)
        self.clear_stage()
