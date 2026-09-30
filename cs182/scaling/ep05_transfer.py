"""Episode 5 — The Right Scaling Transfers (Lecture 8: why parameterization matters, the 1/sqrt(n) example)."""

import os
import sys
from math import lgamma, log

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403
import width_demo  # noqa: E402

# ------------------------------------------------------------------ numbers

# (a) sums of n iid zero-mean, unit-variance variables (Rademacher: exact binomial sampling)
NS_SUM = [10, 100, 1000, 10000]
rng = np.random.RandomState(0)
STD_ROOT, STD_MEAN, STD_SUM = [], [], []
for n in NS_SUM:
    s = rng.binomial(n, 0.5, 200000) * 2 - n
    STD_ROOT.append(float(np.std(s / np.sqrt(n))))
    STD_MEAN.append(float(np.std(s / n)))
    STD_SUM.append(float(np.std(s)))
assert all(abs(v - 1) < 0.02 for v in STD_ROOT)
assert all(abs(a - 1 / np.sqrt(n)) < 0.01 * 10 / np.sqrt(n) + 0.005 for a, n in zip(STD_MEAN, NS_SUM))
assert all(abs(a - np.sqrt(n)) / np.sqrt(n) < 0.02 for a, n in zip(STD_SUM, NS_SUM))


# (b) F_n(c) = E f(c (x_1 + ... + x_n)), computed exactly for Rademacher x_i
def pmf(n):
    k = np.arange(n + 1)
    lg = np.array([lgamma(n + 1) - lgamma(i + 1) - lgamma(n - i + 1) for i in k])
    return np.exp(lg - n * log(2)), 2 * k - n


f = lambda z: -z ** 2 * np.exp(-z ** 2 / 2)


def F(n, c):
    p, s = pmf(n)
    return float(np.sum(p * f(c * s)))


NS_F = [4, 16, 64, 256]
AL = np.linspace(0.2, 3.0, 561)
CS = np.linspace(0.02, 1.2, 300)
FC = {n: np.array([F(n, c) for c in CS]) for n in NS_F}
GA = {n: np.array([F(n, a / np.sqrt(n)) for a in AL]) for n in NS_F}
C_STAR = {n: float(CS[np.argmin(FC[n])]) for n in NS_F}
A_STAR = {n: float(AL[np.argmin(GA[n])]) for n in NS_F}
LIMIT = np.array([-a ** 2 / (1 + a ** 2) ** 1.5 for a in AL])          # E f(N(0, a^2)) in closed form
assert abs(A_STAR[256] - np.sqrt(2)) < 0.02 and abs(AL[np.argmin(LIMIT)] - np.sqrt(2)) < 0.01
assert max(abs(GA[256] - LIMIT)) < 0.01
assert C_STAR[4] / C_STAR[256] > 6                       # the best c drifts by ~8x ...
assert max(A_STAR.values()) - min(A_STAR.values()) < 0.2     # ... the best alpha barely moves

# (c) real training runs, standard rule
R = width_demo.results()
W, E = width_demo.WIDTHS, width_demo.LOG2_LRS
BEST_STD = [E[int(np.argmin(row))] for row in R["standard"]]
assert BEST_STD[0] - BEST_STD[-1] >= 2, BEST_STD                 # the best learning rate falls as width grows


class Ep05Transfer(NarratedScene):
    series = SERIES

    def construct(self):
        self.title_card()
        self.problem()
        self.toy()
        self.transfer()
        self.bridge()
        self.end_card(
            ["Hyperparameter search is expensive for large networks: tune small, transfer to big",
             "That only works if the hyperparameter is scaled the right way with size",
             "One over root n is the right scaling for a sum of n terms",
             "In the reparametrized variable the optimum stays put as n grows"],
        )

    # ---------------------------------------------------------------- 1
    def problem(self):
        head = self.heading("What is a parameterization?")
        units = txt("choosing the right “units”", 32, C_STEP).move_to([0, 2.3, 0])
        self.say("A parameterization is about choosing the right units. Why? Hyperparameter search is a key challenge.",
                 Write(head), FadeIn(units))
        small = box_label("small network", C_MODEL, w=3.0, h=0.9, font_size=26)
        tune = box_label("tune η here: cheap", C_LAM, w=3.5, h=0.9, font_size=26)
        big = box_label("large network", C_LOSS, w=3.0, h=0.9, font_size=26)
        row = VGroup(small, tune, big).arrange(RIGHT, buff=0.9).move_to([0, 1.0, 0])
        a1 = Arrow(small.get_right(), tune.get_left(), buff=0.05, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        a2 = Arrow(tune.get_right(), big.get_left(), buff=0.05, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        q = txt("copy?", 26, C_STEP).move_to(a2.get_center() + DOWN * 0.8)
        assert row.width < 13.2
        self.say("It is worst when the network is large, because every experiment is very expensive.",
                 FadeIn(big, shift=UP * 0.2))
        self.say("Can we optimize hyperparameters on a smaller network, then transfer them to a larger one? What is the right scaling?",
                 FadeIn(small), FadeIn(tune), Create(a1), Create(a2), FadeIn(q))
        self.hold(0.3)
        self.clear_stage()
        # real experiment, standard rule
        head = self.heading("With standard scaling, the optimum moves")
        ax = make_axes([E[0], E[-1] + 0.4, 1], [0, 2.0, 0.5], 7.2, 3.3).move_to([-2.0, 0.2, 0])
        cols = [interpolate_color(BLUE_E, WHITE, i / (len(W) - 1)) for i in range(len(W))]
        cols = [interpolate_color(PURPLE_D, YELLOW_B, i / (len(W) - 1)) for i in range(len(W))]
        curves, marks = VGroup(), VGroup()
        for w, row, col, best in zip(W, R["standard"], cols, BEST_STD):
            y = np.log10(np.clip(row, 10 ** -1.6, 10 ** 0.4)) + 1.6
            curves.add(polyline(ax, E, y, col, 3))
            marks.add(Dot(ax.c2p(best, np.log10(np.clip(row.min(), 10 ** -1.6, 10 ** 0.4)) + 1.6), color=col, radius=0.09))
        xt = VGroup(*[txt(f"{e}", 20, GREY_B).next_to(ax.c2p(e, 0), DOWN, buff=0.12) for e in E[::2]])
        yline = Line(ax.c2p(E[0], 0), ax.c2p(E[0], 2.0), color=GREY_B, stroke_width=2)
        xax = ax.x_axis
        xl = txt("log₂ learning rate", 22, GREY_B).next_to(ax, DOWN, buff=0.55)
        yl = txt("final loss (log scale)", 22, GREY_B).next_to(yline, UP, buff=0.12).shift(RIGHT * 0.9)
        leg = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, color=c, stroke_width=4), txt(f"width {w}", 22, c)).arrange(RIGHT, buff=0.15)
                       for w, c in zip(W, cols)]).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([5.0, 0.6, 0])
        assert leg.get_right()[0] < 7.0 and xl.get_bottom()[1] > -2.5, (leg.get_right(), xl.get_bottom())
        self.say("Here is a small experiment: a three-layer network trained with Adam, one learning rate for every layer, at five widths.",
                 Write(head), Create(xax), Create(yline), FadeIn(xt), FadeIn(xl), FadeIn(yl), FadeIn(leg),
                 LaggedStart(*[Create(c) for c in curves], lag_ratio=0.2, run_time=2.5))
        self.say(f"The best learning rate is not shared. It drops from 2 to the {BEST_STD[0]} at width {W[0]} to 2 to the {BEST_STD[-1]} at width {W[-1]}.",
                 LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.2))
        self.say("Yang and coauthors, 2022, saw the same in Transformers: widths do not share the best setting.")
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 2
    def toy(self):
        head = self.heading("A warm-up: sums of n random numbers")
        setup = mts([r"x_1,\dots,x_n\ \text{iid, mean }0,\ \text{variance }1"], 0.85).move_to([0, 2.5, 0])
        self.say("Add up n independent numbers with mean zero and variance one. How should we scale the sum?",
                 Write(head), Write(setup))
        # table
        hdr = ["n", "sum / √n", "sum / n", "sum"]
        colx = [-4.5, -1.6, 1.4, 4.4]
        cols = [GREY_B, C_MUP, C_LOSS, C_STD]
        hd = VGroup(*[txt(h, 26, c).move_to([colx[j], 1.4, 0]) for j, (h, c) in enumerate(zip(hdr, cols))])
        rows = VGroup()
        for i, n in enumerate(NS_SUM):
            y = 0.75 - 0.55 * i
            rows.add(VGroup(txt(f"{n:,}", 28, C_TEXT).move_to([colx[0], y, 0]),
                            txt(f"{STD_ROOT[i]:.2f}", 28, C_MUP).move_to([colx[1], y, 0]),
                            txt(f"{STD_MEAN[i]:.3f}", 28, C_LOSS).move_to([colx[2], y, 0]),
                            txt(f"{STD_SUM[i]:.0f}", 28, C_STD).move_to([colx[3], y, 0])))
        cap = txt("spread (standard deviation) of each rescaled sum", 24, GREY_A).move_to([0, -1.75, 0])
        assert rows.get_bottom()[1] > -1.5
        self.say("Watch the spread. Divided by root n it stays at one for every n, approaching a standard normal.",
                 FadeIn(hd), FadeIn(cap), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3))
        self.say("Divide by n and it shrinks to zero. Do not divide at all and it grows without bound.",
                 *[Indicate(r[2], color=C_LOSS) for r in rows], *[Indicate(r[3], color=C_STD) for r in rows])
        self.say("One over root n is the right order of scaling factor: the only choice that converges to something non-trivial.",
                 *[Indicate(r[1], color=C_MUP) for r in rows])
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 3
    def transfer(self):
        head = self.heading("Why the scaling matters for tuning")
        eq = mts([r"F_n(c)=\mathbb E\,f\big(c\,(x_1+\cdots+x_n)\big)"], 0.9).move_to([-2.4, 2.5, 0])
        sub = txt("f bounded and continuous; c is a tunable scale", 24, GREY_A).next_to(eq, DOWN, buff=0.15)
        self.say("Let a scale c multiply the sum, and tune c to minimize the expected value of a bounded f. Call it F sub n of c.",
                 Write(head), Write(eq), FadeIn(sub))
        cols = [interpolate_color(BLUE_E, YELLOW_B, i / (len(NS_F) - 1)) for i in range(len(NS_F))]
        ax1 = make_axes([0, 1.2, 0.4], [-0.45, 0.05, 0.2], 5.6, 2.3).move_to([-3.6, -0.45, 0])
        ax2 = make_axes([0, 3, 1], [-0.45, 0.05, 0.2], 5.6, 2.3).move_to([3.0, -0.45, 0])
        t1 = txt("F_n(c) against c", 24, GREY_B).next_to(ax1, UP, buff=0.15)
        t2 = txt("G_n(α) = F_n(α/√n) against α", 24, GREY_B).next_to(ax2, UP, buff=0.15)
        assert ax2.get_right()[0] < 6.9 and ax1.get_left()[0] > -6.9 and ax1.get_bottom()[1] > -2.4, (ax1.get_bottom(), ax2.get_right())
        cur1 = VGroup(*[polyline(ax1, CS, FC[n], c, 3) for n, c in zip(NS_F, cols)])
        cur2 = VGroup(*[polyline(ax2, AL, GA[n], c, 3) for n, c in zip(NS_F, cols)])
        dots1 = VGroup(*[Dot(ax1.c2p(C_STAR[n], FC[n].min()), color=c, radius=0.08) for n, c in zip(NS_F, cols)])
        dots2 = VGroup(*[Dot(ax2.c2p(A_STAR[n], GA[n].min()), color=c, radius=0.08) for n, c in zip(NS_F, cols)])
        leg = VGroup(*[txt(f"n = {n}", 22, c) for n, c in zip(NS_F, cols)]).arrange(RIGHT, buff=0.4).move_to([0.4, 2.55, 0])
        leg.set_x(3.4)
        assert leg.get_right()[0] < 7.0 and leg.get_left()[0] > -0.2, (leg.get_left(), leg.get_right())
        self.say(f"Plot it for n of 4, 16, 64, 256. The best c drifts left, from {C_STAR[4]:.2f} to {C_STAR[256]:.2f}, so small-n tuning does not carry over.",
                 Create(ax1), FadeIn(t1), FadeIn(leg), Create(cur1), FadeIn(dots1))
        self.say("Now reparametrize: write c as alpha over root n. The optimum in alpha barely moves.",
                 Create(ax2), FadeIn(t2), Create(cur2), FadeIn(dots2))
        lim = mts([r"G_n(\alpha)\to\mathbb E\,f\big(N(0,\alpha^2)\big)"], 0.8).move_to([2.6, -1.95, 0])
        lim.shift(UP * 0.0)
        assert lim.get_bottom()[1] > -2.6
        self.say(f"No accident: G_n converges to a fixed function of alpha. Best alpha is about {A_STAR[256]:.2f} at n of 256, limit root two.",
                 Write(lim))
        self.say("So we can copy alpha star from a smaller n to a larger one. Copying c star cannot work the same way.",
                 Indicate(dots2, color=WHITE), Indicate(dots1, color=WHITE))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 4
    def bridge(self):
        head = self.heading("Can we do this for a network?")
        q = txt("Can we find such a scaling for neural-network hyperparameters?", 30, C_TEXT).move_to([0, 2.2, 0])
        self.say("Can we do something similar for neural-network hyperparameters?", Write(head), FadeIn(q))
        rule = mts([r"\eta\ \le\ ", r"\dfrac{1}{d_{\rm in}}", r"\cdot", r"\gamma"], 1.2, {1: C_WIDTH, 3: C_LAM}).move_to([0, 0.5, 0])
        lb1 = txt("the right scaling with width", 26, C_WIDTH).next_to(rule[1], DOWN, buff=0.6).shift(LEFT * 0.4)
        lb2 = txt("still a hyperparameter: tune this", 26, C_LAM).next_to(rule[3], UP, buff=0.6).shift(RIGHT * 0.3)
        assert lb2.get_right()[0] < 7.0 and lb1.get_bottom()[1] > -2.5
        self.say("A preview of the answer: for Adam-like updates, a learning rate of one over the fan-in d_in, times a constant gamma.",
                 Write(rule), FadeIn(lb1), FadeIn(lb2))
        self.say("One over d_in is the right scaling with width. Tune gamma small and reuse it. Next: where this comes from.",
                 Indicate(lb2, color=C_LAM))
        self.hold(0.6)
