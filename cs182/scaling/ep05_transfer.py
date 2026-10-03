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

# the numbers the narration says out loud
assert (len(W), W[0], W[-1], BEST_STD[0], BEST_STD[-1]) == (5, 32, 512, -6, -9), (W, BEST_STD)
assert (NS_F[0], NS_F[-1], f"{C_STAR[4]:.2f}", f"{C_STAR[256]:.2f}") == (4, 256, "0.63", "0.09"), C_STAR


class Ep05Transfer(NarratedScene):
    series = SERIES
    SCENES = ["problem", "toy", "transfer", "bridge"]

    def construct(self):
        self.title_card()
        self.problem()
        self.toy()
        self.transfer()
        self.bridge()
        self.end_card(
            ["Tuning a big network is expensive. So tune a small one and copy the answer",
             "That copy only works if the hyperparameter is scaled right with size",
             "For a sum of n terms, the right scale is one over root n",
             "In the right units, the best setting stays put as n grows"],
        )

    # ---------------------------------------------------------------- 1
    def problem(self):
        head = self.heading("What is a parameterization?")
        units = txt("choosing the right “units”", 32, C_STEP).move_to([0, 2.3, 0])
        small = box_label("small network", C_MODEL, w=3.0, h=0.9, font_size=26)
        tune = box_label("tune η here: cheap", C_LAM, w=3.5, h=0.9, font_size=26)
        big = box_label("large network", C_LOSS, w=3.0, h=0.9, font_size=26)
        row = VGroup(small, tune, big).arrange(RIGHT, buff=0.9).move_to([0, 1.0, 0])
        a1 = Arrow(small.get_right(), tune.get_left(), buff=0.05, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        a2 = Arrow(tune.get_right(), big.get_left(), buff=0.05, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        q = txt("copy?", 26, C_STEP).move_to(a2.get_center() + DOWN * 0.8)
        assert row.width < 13.2
        self.say("What's a parameterization? It's really a choice of units, and the reason it matters is "
                 "hyperparameter search. Search hurts most on a big network, where every single experiment costs a "
                 "fortune.")
        self.play(Write(head), FadeIn(units))
        self.cue("Search hurts most", FadeIn(big, shift=UP * 0.2))
        self.say("So here's a tempting idea. Why not tune on a small network, where it's cheap, and then copy the "
                 "answer over to the big one? Whether that works depends entirely on the scaling.")
        self.cue("Why not tune", FadeIn(small), FadeIn(tune), Create(a1))
        self.cue("and then copy", Create(a2), FadeIn(q))
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
        self.say("Let's try it for real. We'll train a three-layer network with Adam, using one learning rate for "
                 "every layer, at five different widths. And the best learning rate doesn't stay put.")
        self.play(Write(head), Create(xax), Create(yline), FadeIn(xt), FadeIn(xl), FadeIn(yl), FadeIn(leg))
        self.cue("at five different widths", LaggedStart(*[Create(c) for c in curves], lag_ratio=0.2, run_time=2.5))
        self.cue("And the best learning rate", LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.2))
        self.say("At width thirty-two, the best rate is two to the minus six. At width five hundred twelve, it's down "
                 "to two to the minus nine. Yang and coauthors saw the same drift in Transformers in twenty "
                 "twenty-two. With this scaling, each width wants its own setting.")
        self.play(Indicate(marks[0], color=WHITE, scale_factor=1.8))
        self.cue("At width five hundred twelve", Indicate(marks[-1], color=WHITE, scale_factor=1.8))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 2
    def toy(self):
        head = self.heading("A warm-up: sums of n random numbers")
        setup = mts([r"x_1,\dots,x_n\ \text{iid, mean }0,\ \text{variance }1"], 0.85).move_to([0, 2.5, 0])
        self.say("Let's warm up with something simpler. Add up n random numbers with mean zero and variance one. How "
                 "should we scale that sum?")
        self.play(Write(head), Write(setup))
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
        self.say("Watch the spread of each version. If we divide by root n, it stays at one whatever n is, and the sum "
                 "settles into a standard normal. If we divide by n, it shrinks to nothing, and if we don't divide at "
                 "all, it blows up.")
        self.play(FadeIn(hd), FadeIn(cap), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3))
        self.cue("it stays at one", *[Indicate(r[1], color=C_MUP) for r in rows])
        self.cue("it shrinks to nothing", *[Indicate(r[2], color=C_LOSS) for r in rows])
        self.cue("it blows up", *[Indicate(r[3], color=C_STD) for r in rows])
        self.say("So one over root n is the right scaling. It's the only choice that lands on something interesting, "
                 "neither zero nor infinity.")
        self.play(*[Indicate(r[1], color=C_MUP) for r in rows])
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 3
    def transfer(self):
        head = self.heading("Why the scaling matters for tuning")
        eq = mts([r"F_n(c)=\mathbb E\,f\big(c\,(x_1+\cdots+x_n)\big)"], 0.9).move_to([-2.4, 2.5, 0])
        sub = txt("f bounded and continuous; c is a tunable scale", 24, GREY_A).next_to(eq, DOWN, buff=0.15)
        self.say("Now turn that scale into a knob, and call it c. We tune c to minimize the average of some bounded "
                 "function f, and we'll call that average F sub n of c.")
        self.play(Write(head), Write(eq), FadeIn(sub))
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
        self.say("Here's that average for n from four up to two hundred fifty-six. The best c slides from zero point "
                 "six three all the way down to zero point zero nine. So if you tune at a small n, you miss badly at a "
                 "large one.")
        self.play(Create(ax1), FadeIn(t1), FadeIn(leg), Create(cur1))
        self.cue("The best c slides", FadeIn(dots1))
        lim = mts([r"G_n(\alpha)\to\mathbb E\,f\big(N(0,\alpha^2)\big)"], 0.8).move_to([2.6, -1.95, 0])
        lim.shift(UP * 0.0)
        assert lim.get_bottom()[1] > -2.6
        self.say("Now let's change units. Write c as alpha over root n, and suddenly the best alpha barely moves. "
                 "That's no accident. The curves settle onto a single limit curve, whose best alpha is the square root "
                 "of two.")
        self.play(Create(ax2), FadeIn(t2), Create(cur2))
        self.cue("and suddenly", FadeIn(dots2))
        self.cue("The curves settle", Write(lim))
        self.say("So you can copy the best alpha from a small n to a large one, and it just works. Copying the best c "
                 "never could.")
        self.play(Indicate(dots2, color=WHITE))
        self.cue("Copying the best c", Indicate(dots1, color=WHITE))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 4
    def bridge(self):
        head = self.heading("Can we do this for a network?")
        q = txt("Can we find such a scaling for neural-network hyperparameters?", 30, C_TEXT).move_to([0, 2.2, 0])
        rule = mts([r"\eta\ \le\ ", r"\dfrac{1}{d_{\rm in}}", r"\cdot", r"\gamma"], 1.2, {1: C_WIDTH, 3: C_LAM}).move_to([0, 0.5, 0])
        lb1 = txt("the right scaling with width", 26, C_WIDTH).next_to(rule[1], DOWN, buff=0.6).shift(LEFT * 0.4)
        lb2 = txt("still a hyperparameter: tune this", 26, C_LAM).next_to(rule[3], UP, buff=0.6).shift(RIGHT * 0.3)
        assert lb2.get_right()[0] < 7.0 and lb1.get_bottom()[1] > -2.5
        self.say("Can we pull the same trick with a real network's hyperparameters? Here's a sneak peek. For Adam-like "
                 "updates, we set the learning rate to gamma divided by the fan-in.")
        self.play(Write(head), FadeIn(q))
        self.cue("For Adam-like", Write(rule))
        self.say("The one over fan-in part handles the width. Gamma is still a hyperparameter, but you tune it just "
                 "once, on a small network. Next time, we'll see why that works.")
        self.play(FadeIn(lb1))
        self.cue("Gamma is still", FadeIn(lb2))
        self.hold(0.6)
