"""Episode 6 — Maximal Update Parametrization (Lecture 8: feature-learning conditions, sign SGD / Adam rule, muP)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403
import width_demo  # noqa: E402

# ------------------------------------------------------------------ numbers

rms = lambda v: float(np.linalg.norm(v) / np.sqrt(len(v)))
DS = [64, 128, 256, 512, 1024]

# (a) RMS -> RMS norm of a d x d weight matrix at initialization
rng = np.random.RandomState(1)
XAV, STD = [], []
for d in DS:
    XAV.append(float(np.linalg.norm(rng.randn(d, d) / np.sqrt(d), 2)))      # square: RMS->RMS norm = spectral norm
    STD.append(float(np.linalg.norm(rng.randn(d, d), 2)))
assert all(1.8 < v < 2.2 for v in XAV)
assert all(1.8 * np.sqrt(d) < s < 2.2 * np.sqrt(d) for s, d in zip(STD, DS))

# (b) rank-one sign gradient (batch size 1) and the step size rule
GAMMA = 0.05
rng = np.random.RandomState(2)
ROWS = []
for d in DS:
    delta, x = rng.randn(d), rng.randn(d)
    S = np.outer(np.sign(delta), np.sign(x))                # sign of the rank-one gradient delta x^T
    spec = float(np.linalg.norm(S, 2))
    assert abs(spec - np.linalg.norm(S)) < 1e-6 * d and abs(spec - d) < 1e-6 * d         # rank one: spectral = Frobenius = sqrt(d_in d_out)
    if d <= 256:
        assert np.linalg.matrix_rank(S) == 1
    eta_fixed, eta_mup = 1e-3, GAMMA / d
    rr_fixed = eta_fixed * np.sqrt(d / d) * spec           # ||eta S||_RMS->RMS
    rr_mup = eta_mup * spec
    dh_fixed = rms(-eta_fixed * S @ (x / rms(x)))           # change in the layer output on a unit-RMS input
    dh_mup = rms(-eta_mup * S @ (x / rms(x)))
    ROWS.append((d, rr_fixed, rr_mup, dh_fixed, dh_mup))
assert abs(ROWS[-1][1] / ROWS[0][1] - DS[-1] / DS[0]) < 1e-6                 # fixed eta: grows in proportion to d
assert all(abs(r[2] - GAMMA) < 1e-9 for r in ROWS)                            # eta = gamma / d: constant
assert ROWS[-1][3] / ROWS[0][3] > 10 and max(r[4] for r in ROWS) / min(r[4] for r in ROWS) < 1.2
# larger batches: Frobenius norm only upper-bounds the spectral norm
rng = np.random.RandomState(4)
RATIO = {}
for B in (1, 16):
    g = sum(np.outer(rng.randn(256), rng.randn(256)) for _ in range(B))
    Sg = np.sign(g)
    RATIO[B] = float(np.linalg.norm(Sg, 2) / np.linalg.norm(Sg))
assert abs(RATIO[1] - 1) < 1e-9 and RATIO[16] < 0.4

# (c) width-transfer experiment
R = width_demo.results()
W, E = width_demo.WIDTHS, width_demo.LOG2_LRS
BEST_STD = [E[int(np.argmin(r))] for r in R["standard"]]
BEST_SC = [E[int(np.argmin(r))] for r in R["scaled"]]
assert BEST_STD[0] - BEST_STD[-1] >= 2 and max(BEST_SC) - min(BEST_SC) == 0, (BEST_STD, BEST_SC)
MIN_SC = [float(r.min()) for r in R["scaled"]]
assert MIN_SC[-1] < 1.3 * MIN_SC[0]

# the numbers the narration says out loud
assert (DS[0], DS[-1], f"{STD[-1]:.0f}") == (64, 1024, "64"), STD
assert (W[0], W[-1], BEST_SC[0]) == (32, 512, -6), (W, BEST_SC)
assert RATIO[16] < 1


class Ep06Mup(NarratedScene):
    series = SERIES
    SCENES = ["desiderata", "condition_one", "condition_two", "sign_rule", "payoff"]

    def construct(self):
        self.title_card()
        self.desiderata()
        self.condition_one()
        self.condition_two()
        self.sign_rule()
        self.payoff()
        self.end_card(
            ["Ask activations, and their changes, to stay order one in RMS size at every width",
             "That means weights and updates with RMS to RMS norm of order one",
             "For Adam, a rank-one step has RMS to RMS size eta times d_in. So eta goes like one over d_in",
             "Then the best learning rate transfers across widths, so tune narrow and reuse wide"],
        )

    # ---------------------------------------------------------------- 1
    def desiderata(self):
        head = self.heading("Conditions for feature learning")
        blk = VGroup(txt("h(ℓ−1)", 26, C_RAMP), box_label("W", C_MODEL, w=1.0, h=0.7, font_size=28), txt("+ b", 26, GREY_B),
                     box_label("nonlinearity", C_RAMP, w=2.4, h=0.7, font_size=24), txt("h(ℓ)", 26, C_RAMP)).arrange(RIGHT, buff=0.35).move_to([0, 2.3, 0])
        dims = txt("h(ℓ−1) has d_in entries, h(ℓ) has d_out, and W is d_out × d_in", 24, GREY_A).next_to(blk, DOWN, buff=0.25)
        assert blk.width < 12
        d1 = mts([r"\|\vec h_\ell\|_{\rm RMS}=\Theta(1)"], 1.0, ).move_to([0, 0.6, 0])
        b1 = SurroundingRectangle(d1, color=C_RAMP, buff=0.2)
        t1 = txt("(1) activations stay a sensible size", 26, C_RAMP).next_to(b1, DOWN, buff=0.15)
        self.say("Here's one hidden layer, with its weights, its bias and its nonlinearity. What should stay fixed as "
                 "we make it wider? Condition one comes straight from Xavier, and it says the activations should keep "
                 "an RMS size of about one.")
        self.play(Write(head), FadeIn(blk), FadeIn(dims))
        self.cue("Condition one comes", Write(d1), Create(b1), FadeIn(t1))
        d2 = mts([r"\|\Delta\vec h_\ell\|_{\rm RMS}=\Theta(1)"], 1.0).move_to([0, -1.1, 0])
        b2 = SurroundingRectangle(d2, color=C_STEP, buff=0.2)
        t2 = txt("(2) updates are not negligible", 26, C_STEP).next_to(b2, DOWN, buff=0.15)
        assert t2.get_bottom()[1] > -2.5
        note = txt("Θ(1): bounded above and below\nby constants, at any width", 20, GREY_A).move_to([5.0, -0.25, 0])
        assert note.get_right()[0] < 7.0 and note.get_left()[0] > 3.0, (note.get_left(), note.get_right())
        self.say("Condition two is about learning. Each update should change those activations by an amount that "
                 "doesn't vanish as the layer widens. And theta of one just means pinned between two constants, "
                 "however wide the layer gets.")
        self.play(Write(d2), Create(b2), FadeIn(t2))
        self.cue("And theta of one", FadeIn(note))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 2
    def condition_one(self):
        head = self.heading("Achieving (1)")
        ig = txt("for now ignore the bias and the nonlinearity:", 26, GREY_A).move_to([-3.0, 2.5, 0])
        e0 = mts([r"\vec h_\ell=W_\ell\,\vec h_{\ell-1}"], 0.95).move_to([-4.0, 1.6, 0])
        e1 = mts([r"\|\vec h_\ell\|_2=\|W_\ell\|_2\,\|\vec h_{\ell-1}\|_2"], 0.85).move_to([-3.4, 0.5, 0])
        e2 = mts([r"\Theta(\sqrt{d_{\rm out}})=\|W_\ell\|_2\,\Theta(\sqrt{d_{\rm in}})"], 0.85).move_to([-3.4, -0.55, 0])
        e3 = mts([r"\Rightarrow\ \|W_\ell\|_2=\Theta\Big(\sqrt{d_{\rm out}/d_{\rm in}}\Big)\ \iff\ \|W_\ell\|_{\rm RMS\to RMS}=\Theta(1)"], 0.85).move_to([0, -1.75, 0])
        assert e3.width < 13.0 and e2.get_right()[0] < 0.5, (e3.width, e2.get_right())
        self.say("To get condition one, let's ignore the bias and the nonlinearity for now. Then the output's length "
                 "is at most the spectral norm times the input's length.")
        self.play(Write(head), FadeIn(ig), Write(e0))
        self.cue("Then the output's", Write(e1))
        self.say("We want the output to have length around root d_out, and the input has length around root d_in. That "
                 "forces the spectral norm to be about the square root of d_out over d_in. And that's the same as an "
                 "RMS to RMS norm of order one.")
        self.play(Write(e2))
        self.cue("That forces the spectral norm", Write(e3))
        # numeric table on the right
        hdr = VGroup(txt("width d", 22, GREY_B), txt("N(0,1)", 22, C_STD), txt("N(0,1/d)", 22, C_MUP))
        colx = [2.6, 4.3, 6.0]
        for h, x in zip(hdr, colx):
            h.move_to([x, 2.5, 0])
        rows = VGroup()
        for i, d in enumerate(DS):
            y = 2.0 - 0.45 * i
            rows.add(VGroup(txt(f"{d}", 24, C_TEXT).move_to([colx[0], y, 0]),
                            txt(f"{STD[i]:.0f}", 24, C_STD).move_to([colx[1], y, 0]),
                            txt(f"{XAV[i]:.2f}", 24, C_MUP).move_to([colx[2], y, 0])))
        cap = txt("RMS→RMS norm of a d × d matrix", 22, GREY_A).move_to([4.3, -0.4, 0])
        assert rows.get_right()[0] < 7.0 and cap.get_right()[0] < 7.05 and cap.get_left()[0] > 0.6, (cap.get_left(), cap.get_right())
        self.say("Random matrices agree. With unit-variance weights, that norm climbs to sixty-four by width one "
                 "thousand twenty-four. Xavier scaling holds it near two at every width.")
        self.play(FadeIn(hdr), FadeIn(cap), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2))
        self.cue("Xavier scaling holds", *[Indicate(r[2], color=C_MUP) for r in rows])
        self.say("So condition one holds when the weights have an RMS to RMS norm of order one. That's the very norm "
                 "we built our optimizer around.")
        self.play(Indicate(e3, color=C_MUP))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 3
    def condition_two(self):
        head = self.heading("Achieving (2)")
        r0 = mts([r"\vec h_\ell=W_\ell\vec h_{\ell-1}\ \Rightarrow\ \Delta\vec h_\ell=", r"\Delta W_\ell\,\vec h_{\ell-1}", r"+\ ", r"W_\ell\,\Delta\vec h_{\ell-1}"],
                 0.85, {1: C_STEP, 3: C_STEP}).move_to([0, 2.4, 0])
        r1 = mts([r"\|\Delta\vec h_\ell\|_2\le\|\Delta W_\ell\|_2\|\vec h_{\ell-1}\|_2+\|W_\ell\|_2\|\Delta\vec h_{\ell-1}\|_2"], 0.85).move_to([0, 1.3, 0])
        assert r0.width < 13 and r1.width < 13
        self.say("Now for the update. The layer's output changes for two reasons, because the weights changed and "
                 "because its input changed. Take lengths and use the triangle inequality, and each piece is at most a "
                 "spectral norm times the length it acts on.")
        self.play(Write(head), Write(r0))
        self.cue("Take lengths", Write(r1))
        r2 = mts([r"=\ \boxed{\ \Theta\big(\sqrt{d_{\rm out}/d_{\rm in}}\big)\ }\,\Theta(\sqrt{d_{\rm in}})\ +\ \Theta\big(\sqrt{d_{\rm out}/d_{\rm in}}\big)\,\Theta(\sqrt{d_{\rm in}})"], 0.85).move_to([0, 0.2, 0])
        r3 = mts([r"\Rightarrow\ \|\Delta\vec h_\ell\|_2=\Theta(\sqrt{d_{\rm out}})\ \Rightarrow\ \|\Delta\vec h_\ell\|_{\rm RMS}=\Theta(1)"], 0.85).move_to([0, -0.9, 0])
        assert r2.width < 13.4 and r3.width < 13
        self.say("Condition one already takes care of the second piece. The first piece needs an update whose spectral "
                 "size is about root d_out over d_in. Then both pieces come out around root d_out, so the output's RMS "
                 "change is order one. That's just what we wanted.")
        self.play(Write(r2))
        self.cue("Then both pieces", Write(r3))
        cond = VGroup(mts([r"(1)\ \|W\|_{\rm RMS\to RMS}=\Theta(1)"], 0.9), mts([r"(2)\ \|\Delta W\|_{\rm RMS\to RMS}=\Theta(1)"], 0.9)).arrange(RIGHT, buff=0.8).move_to([0, -2.0, 0])
        assert cond.width < 13.2 and cond.get_bottom()[1] > -2.5
        box = SurroundingRectangle(cond, color=YELLOW_D, buff=0.15)
        self.say("So here's the whole story in two lines. The weights and the updates both need an RMS to RMS norm of "
                 "order one.")
        self.play(FadeIn(cond), Create(box))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 4
    def sign_rule(self):
        head = self.heading("What does Adam need?")
        e0 = mts([r"W_{t+1}=W_t-\eta\cdot\mathrm{sign}\big(\nabla_W\mathcal L\big)"], 0.95).move_to([-2.2, 2.5, 0])
        e1 = mts([r"\text{batch size 1:}\ \nabla_W\mathcal L=\sigma\,\vec u\vec v^{\top}\ \Rightarrow\ S=\mathrm{sgn}(\vec u)\,\mathrm{sgn}(\vec v)^{\top}"], 0.8).move_to([0, 1.5, 0])
        assert e1.width < 13.2
        self.say("So what does that mean for Adam? We'll use sign SGD as a stand-in, and ask how its eta should depend "
                 "on the layer. With a batch of one, the gradient has rank one. So does its sign, which is an outer "
                 "product of two sign vectors.")
        self.play(Write(head), Write(e0))
        self.cue("With a batch of one", Write(e1))
        e2 = mts([r"\|S\|_F^2=d_{\rm in}d_{\rm out}\ \Rightarrow\ \|S\|_2=\sqrt{d_{\rm in}d_{\rm out}}"], 0.85).move_to([0, 0.45, 0])
        e3 = mts([r"\eta\,\sqrt{\dfrac{d_{\rm in}}{d_{\rm out}}}\,\sqrt{d_{\rm in}d_{\rm out}}\le\gamma\ \Rightarrow\ ", r"\eta\le\dfrac{\gamma}{d_{\rm in}}"], 0.9, {1: C_WIDTH}).move_to([0, -0.8, 0])
        assert e3.width < 13.2
        self.say("At rank one, the spectral and Frobenius norms agree. Every entry is plus or minus one, so that norm "
                 "is the square root of d_in times d_out. Now cap the step's RMS to RMS size at gamma. The square "
                 "roots cancel, and what's left is an eta of gamma over d_in, the layer's fan-in.")
        self.play(Write(e2))
        self.cue("Now cap the step", Write(e3))
        tag = txt("learning rate scales with the layer's fan-in", 30, C_WIDTH).move_to([0, -1.9, 0])
        self.say("So Adam's rate should shrink like one over the fan-in. And that's the heart of muP.")
        self.play(FadeIn(tag), Indicate(e3[1], color=C_WIDTH))
        self.hold(0.3)
        self.clear_stage()
        head = self.heading("Checking the rule")
        hdr = ["width d", "η fixed = 0.001", f"η = γ / d,  γ = {GAMMA:g}"]
        colx = [-4.6, -0.5, 4.0]
        cells = VGroup(*[txt(h, 24, c).move_to([colx[j], 2.4, 0]) for j, (h, c) in enumerate(zip(hdr, [GREY_B, C_STD, C_MUP]))])
        sub = txt("RMS→RMS size of the step  ·  change in output RMS", 22, GREY_A).move_to([0, 1.85, 0])
        rows = VGroup()
        for i, (d, a, b, c, e) in enumerate(ROWS):
            y = 1.25 - 0.55 * i
            rows.add(VGroup(txt(f"{d}", 28, C_TEXT).move_to([colx[0], y, 0]),
                            txt(f"{a:.3f}  ·  {c:.3f}", 28, C_STD).move_to([colx[1], y, 0]),
                            txt(f"{b:.3f}  ·  {e:.3f}", 28, C_MUP).move_to([colx[2], y, 0])))
        assert rows.get_right()[0] < 7.0 and rows.get_bottom()[1] > -2.0, (rows.get_right(), rows.get_bottom())
        self.say("Let's test it at widths from sixty-four up to one thousand twenty-four. With a fixed learning rate, "
                 "the size of the update grows right along with the width. Switch to gamma over d, and it holds still, "
                 "and so does the change in the layer's output.")
        self.play(Write(head), FadeIn(cells), FadeIn(sub), LaggedStart(*[FadeIn(r[:2]) for r in rows], lag_ratio=0.25))
        self.cue("Switch to gamma", LaggedStart(*[FadeIn(r[2]) for r in rows], lag_ratio=0.25))
        bs = txt(f"batch 16: spectral / Frobenius = {RATIO[16]:.2f}, so the bound is loose", 24, GREY_A).move_to([0, -1.75, 0])
        assert bs.width < 13
        self.say("There's one caveat. With bigger batches, the gradient isn't rank one anymore, and the spectral norm "
                 "falls below the Frobenius norm. So this rule plays it safe.")
        self.play(FadeIn(bs))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 5
    def payoff(self):
        head = self.heading("Does the best learning rate transfer?")
        ax1 = make_axes([E[0], E[-1] + 0.4, 1], [0, 2.0, 0.5], 5.6, 2.7).move_to([-3.6, 0.5, 0])
        ax2 = make_axes([E[0], E[-1] + 0.4, 1], [0, 2.0, 0.5], 5.6, 2.7).move_to([3.0, 0.5, 0])
        cols = [interpolate_color(PURPLE_D, YELLOW_B, i / (len(W) - 1)) for i in range(len(W))]
        t1 = txt("standard: one η everywhere", 24, C_STD).next_to(ax1, UP, buff=0.15)
        t2 = txt("η × 32 / width in layers with fan-in = width", 24, C_MUP).next_to(ax2, UP, buff=0.15)
        t2.scale_to_fit_width(min(t2.width, 6.0))

        def panel(ax, M):
            cur, mk = VGroup(), VGroup()
            for row, col in zip(M, cols):
                y = np.log10(np.clip(row, 10 ** -1.6, 10 ** 0.4)) + 1.6
                cur.add(polyline(ax, E, y, col, 3))
                mk.add(Dot(ax.c2p(E[int(np.argmin(row))], np.log10(np.clip(row.min(), 10 ** -1.6, 10 ** 0.4)) + 1.6), color=col, radius=0.08))
            return cur, mk

        c1, m1 = panel(ax1, R["standard"])
        c2, m2 = panel(ax2, R["scaled"])
        yl1 = Line(ax1.c2p(E[0], 0), ax1.c2p(E[0], 2.0), color=GREY_B, stroke_width=2)
        yl2 = Line(ax2.c2p(E[0], 0), ax2.c2p(E[0], 2.0), color=GREY_B, stroke_width=2)
        xl1 = txt("log₂ learning rate", 20, GREY_B).next_to(ax1, DOWN, buff=0.15)
        xl2 = txt("log₂ base learning rate", 20, GREY_B).next_to(ax2, DOWN, buff=0.15)
        leg = VGroup(*[txt(f"{w}", 20, c) for w, c in zip(W, cols)]).arrange(RIGHT, buff=0.3).move_to([0, 2.65, 0])
        wl = txt("width:", 20, GREY_B).next_to(leg, LEFT, buff=0.2)
        assert xl1.get_bottom()[1] > -2.5 and ax2.get_right()[0] < 6.9 and t2.get_right()[0] < 7.0 and t1.get_left()[0] > -7.0, (t2.get_right(), t1.get_left())
        self.say("Now back to our experiment, with widths from thirty-two to five hundred twelve. On the left is "
                 "standard scaling, and the best learning rate keeps sliding as the network widens.")
        self.play(Write(head), Create(ax1.x_axis), Create(yl1), FadeIn(t1), FadeIn(xl1), FadeIn(leg), FadeIn(wl))
        self.cue("On the left", LaggedStart(*[Create(c) for c in c1], lag_ratio=0.15, run_time=2.0))
        self.cue("and the best learning rate", FadeIn(m1))
        self.say("On the right, each layer whose fan-in is the width gets its rate multiplied by thirty-two over the "
                 "width. The first layer keeps its rate. And now every width agrees, because the best rate is two to "
                 "the minus six for all of them.")
        self.play(Create(ax2.x_axis), Create(yl2), FadeIn(t2), FadeIn(xl2))
        self.cue("gets its rate", LaggedStart(*[Create(c) for c in c2], lag_ratio=0.15, run_time=2.0))
        self.cue("And now every width agrees", FadeIn(m2))
        self.cue("two to the minus six", Indicate(m2, color=WHITE))
        self.say("So you tune the narrow network, and the wide one inherits the answer. Yang and coauthors saw this in "
                 "Transformers in twenty twenty-two. The optimum holds still, and wider networks do better.")
        fin = txt("muP: hyperparameters that survive changes in width", 28, C_STEP).move_to([0, -1.95, 0])
        assert fin.width < 13
        self.say("And that's muP, short for maximal update parametrization. It takes the biggest updates that still "
                 "keep activations, and their changes, at order one for any width.")
        self.play(FadeIn(fin))
        self.hold(0.6)
