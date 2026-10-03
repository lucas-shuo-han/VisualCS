"""Episode 3 — The RMS Norm (Lectures 7-8: Xavier recap, RMS norm, induced RMS->RMS norm)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers

# (a) Xavier: RMS of a layer's output vs fan-in
DINS = [16, 64, 256, 1024, 4096]
DOUT, NB = 64, 100
rng = np.random.RandomState(3)
X = rng.randn(NB, 4096)
RMS_STD, RMS_XAV = [], []
for d in DINS:
    W = rng.randn(DOUT, d)
    h1 = X[:, :d] @ W.T                         # weights with variance 1
    h2 = X[:, :d] @ (W / np.sqrt(d)).T           # weights with variance 1 / d_in
    RMS_STD.append(float(np.sqrt(np.mean(h1 ** 2))))
    RMS_XAV.append(float(np.sqrt(np.mean(h2 ** 2))))
assert all(0.9 < r / np.sqrt(d) < 1.1 for r, d in zip(RMS_STD, DINS)), RMS_STD
assert all(0.9 < r < 1.1 for r in RMS_XAV), RMS_XAV
assert DINS[-1] == 4096 and f"{RMS_STD[-1]:.0f}" == "64"            # spoken in xavier()

# (b) RMS norm vs the ordinary length
V4, V16 = np.array([1, -1, 1, 1.0]), np.array([1, -1] * 8, float)
assert np.linalg.norm(V4) == 2 and np.linalg.norm(V16) == 4
rms = lambda v: float(np.linalg.norm(v) / np.sqrt(len(v)))
assert rms(V4) == 1 and rms(V16) == 1

# (c) induced RMS -> RMS norm
D_OUT, D_IN = 64, 256
rng = np.random.RandomState(5)
A = rng.randn(D_OUT, D_IN) / np.sqrt(D_IN)
UA, SA, VAt = np.linalg.svd(A, full_matrices=False)
x_star = np.sqrt(D_IN) * VAt[0]
assert abs(rms(x_star) - 1) < 1e-12
NORM_RMS = rms(A @ x_star)
assert abs(NORM_RMS - np.sqrt(D_IN / D_OUT) * SA[0]) < 1e-9
trials = []
for _ in range(2000):
    x = rng.randn(D_IN)
    x /= rms(x)
    trials.append(rms(A @ x))
assert max(trials) < NORM_RMS
FACTOR = float(np.sqrt(D_IN / D_OUT))
assert FACTOR == 2.0
# the numbers as they are spoken in induced()
assert (f"{SA[0]:.2f}", f"{NORM_RMS:.2f}", f"{max(trials):.2f}", len(trials)) == ("1.49", "2.98", "1.29", 2000)

# (d) steps of RMS->RMS size eta in layers of different shapes
ETA = 0.1
SHAPES = [(64, 256), (256, 256), (256, 64)]      # (d_out, d_in)
ROWS = []
for do, di in SHAPES:
    G = np.random.RandomState(do + di).randn(do, di)
    U, S, Vt = np.linalg.svd(G, full_matrices=False)
    dW = -ETA * np.sqrt(do / di) * U @ Vt
    x = np.sqrt(di) * Vt[0]                        # a unit-RMS input the step can grab
    dh = dW @ x
    spec = float(np.linalg.norm(dW, 2))
    assert abs(spec - ETA * np.sqrt(do / di)) < 1e-9 and abs(rms(dh) - ETA) < 1e-9
    ROWS.append((do, di, spec, rms(dh)))


def neuron(cx, cy, n=4):
    """Inputs -> weights -> sum -> h; returns group and the h dot."""
    ins = VGroup(*[Dot([cx - 2.2, cy + (1.5 - i) * 0.75 - 0.0, 0], color=C_TRAIN, radius=0.1) for i in range(n)])
    labs = VGroup(*[txt(f"x{i + 1}", 22, C_TRAIN).next_to(d, LEFT, buff=0.12) for i, d in enumerate(ins)])
    sm = Circle(radius=0.28, color=WHITE, stroke_width=3).move_to([cx + 0.4, cy + 0.375, 0])
    sm.add(txt("+", 28, WHITE).move_to(sm))
    edges = VGroup(*[Line(d.get_center(), sm.get_left(), color=C_MODEL, stroke_width=3) for d in ins])
    wl = VGroup(*[txt(f"w{i + 1}", 20, C_MODEL).move_to(0.5 * (d.get_center() + sm.get_left()) + UP * 0.2) for i, d in enumerate(ins)])
    hd = Dot([cx + 1.9, cy + 0.375, 0], color=C_RAMP, radius=0.11)
    out = Arrow(sm.get_right(), hd.get_center(), buff=0.05, color=GREY_B, stroke_width=3)
    hl = txt("h", 26, C_RAMP).next_to(hd, RIGHT, buff=0.12)
    return VGroup(ins, labs, edges, wl, sm, out, hd, hl)


class Ep03Rms(NarratedScene):
    series = SERIES
    SCENES = ["xavier", "rms_norm", "induced", "shapes"]

    def construct(self):
        self.title_card()
        self.xavier()
        self.rms_norm()
        self.induced()
        self.shapes()
        self.end_card(
            ["Xavier keeps the RMS size of activations steady, layer after layer",
             "RMS norm: length over root d, so a typical entry is about size one",
             "RMS to RMS norm: the spectral norm times root d_in over d_out",
             "Measure steps in that norm, and one eta changes every layer's output by eta"],
        )

    # ---------------------------------------------------------------- 1
    def xavier(self):
        head = self.heading("Recap: Xavier initialization")
        nn = neuron(-3.3, 0.6)
        want = txt("inputs ≈ N(0, 1)   →   want h ≈ N(0, 1)", 26, GREY_A).move_to([-2.0, -1.5, 0])
        eqs = VGroup(
            mts([r"h=\vec w^{\top}\vec x=\sum_i w_i x_i"], 0.75),
            mts([r"\mathbb E[h^2]=", r"\sigma_w^2", r"\sum_i x_i^2"], 0.75, {1: C_LAM}),
            mts([r"x_i^2\approx1\ \Rightarrow\ \sigma_w^2\approx\dfrac{1}{d_{\rm in}}"], 0.75),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.3, 0.6, 0])
        assert eqs.get_right()[0] < 7.0 and eqs.get_left()[0] > 0.2, eqs.get_center()
        self.say("Let's flash back to Xavier initialization. We feed a neuron standard normal inputs, as many as its "
                 "fan-in, and we'd like the output to be standard normal too. With independent weights, the "
                 "squared output averages to the weight variance times the sum of the squared inputs.")
        self.play(Write(head), FadeIn(nn), FadeIn(want))
        self.cue("With independent weights", Write(eqs[0]), Write(eqs[1]))
        self.say("Each squared input is about one, so that sum is about the fan-in, which we write as d_in. "
                 "And that means the weight variance has to be one over the fan-in.")
        self.play(Write(eqs[2]))
        self.hold(0.3)
        self.clear_stage()
        head = self.heading("Does it work? Simulate")
        ax = make_axes([4, 12, 1], [-1, 7, 1], 7.4, 3.6).move_to([-1.6, 0.3, 0])
        xt = VGroup(*[txt(str(d), 20, GREY_B).next_to(ax.c2p(np.log2(d), -1), DOWN, buff=0.15) for d in DINS])
        yt = VGroup(*[txt(str(2 ** k), 20, GREY_B).next_to(ax.c2p(4, k), LEFT, buff=0.15) for k in (0, 2, 4, 6)])
        xl = txt("fan-in d_in", 22, GREY_B).next_to(ax, DOWN, buff=0.55)
        yl = txt("RMS of h", 22, GREY_B).next_to(ax.y_axis.get_top(), UP, buff=0.1).shift(RIGHT * 0.5)
        ps = polyline(ax, [np.log2(d) for d in DINS], [np.log2(r) for r in RMS_STD], C_STD, 4)
        px = polyline(ax, [np.log2(d) for d in DINS], [np.log2(r) for r in RMS_XAV], C_MUP, 4)
        ds = VGroup(*[Dot(ax.c2p(np.log2(d), np.log2(r)), color=C_STD, radius=0.08) for d, r in zip(DINS, RMS_STD)])
        dx = VGroup(*[Dot(ax.c2p(np.log2(d), np.log2(r)), color=C_MUP, radius=0.08) for d, r in zip(DINS, RMS_XAV)])
        lb1 = txt("weights ~ N(0, 1)", 24, C_STD).move_to([4.8, 1.4, 0])
        lb2 = txt("weights ~ N(0, 1/d_in)", 24, C_MUP).move_to([4.8, -0.3, 0])
        assert lb1.get_right()[0] < 7.0 and lb2.get_right()[0] < 7.0
        self.say("Does that actually work? With unit-variance weights, the output grows like the square root of the "
                 "fan-in. At a fan-in of four thousand and ninety-six, it's sixty-four times too big. "
                 "With a variance of one over the fan-in, it sits right near one at every width.")
        self.play(Write(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), Create(ps), FadeIn(ds), FadeIn(lb1))
        self.cue("At a fan-in of", Indicate(ds[-1], color=C_STD, scale_factor=1.8))
        self.cue("With a variance of", Create(px), FadeIn(dx), FadeIn(lb2))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 2
    def rms_norm(self):
        head = self.heading("Which norm is being preserved?")
        eq = mts([r"\|\vec x\|_{\rm RMS}=\dfrac{1}{\sqrt{d}}\|\vec x\|_2=\sqrt{\dfrac1d\sum_i x_i^2}"], 0.9).move_to([0, 2.5, 0])

        def barvec(v, cx):
            g = VGroup()
            w = min(0.32, 5.2 / len(v))
            for i, e in enumerate(v):
                h = 0.5 * abs(e)
                r = Rectangle(width=w * 0.85, height=h, stroke_width=1, stroke_color=C_WIDTH, fill_color=C_WIDTH, fill_opacity=0.5)
                r.move_to([cx + (i - (len(v) - 1) / 2) * w, 0.3 + (h / 2) * np.sign(e), 0])
                g.add(r)
            return g

        b4, b16 = barvec(V4, -3.4), barvec(V16, 3.0)
        z1 = Line([-5.6, 0.3, 0], [-1.2, 0.3, 0], color=GREY_D, stroke_width=2)
        z2 = Line([0.5, 0.3, 0], [5.6, 0.3, 0], color=GREY_D, stroke_width=2)
        n4 = VGroup(txt("4 entries of ±1", 24, GREY_A), txt("length 2,  RMS 1", 26, C_WIDTH)).arrange(DOWN, buff=0.12).move_to([-3.4, -1.3, 0])
        n16 = VGroup(txt("16 entries of ±1", 24, GREY_A), txt("length 4,  RMS 1", 26, C_WIDTH)).arrange(DOWN, buff=0.12).move_to([3.0, -1.3, 0])
        pt = txt("RMS ≈ 1  ⇒  typical entry about 1, at any width", 28, C_STEP).move_to([0, -2.2, 0])
        self.say("So what is Xavier really keeping steady? It's the length divided by root d, which is called the "
                 "root-mean-square norm, or RMS norm for short. Four entries of plus or minus one have length two, "
                 "and sixteen of them have length four. But the RMS norm is one for both. So an RMS norm of one "
                 "just means a typical entry is about size one, however wide the vector gets.")
        self.play(Write(head), Write(eq))
        self.cue("Four entries", Create(z1), FadeIn(b4), FadeIn(n4))
        self.cue("and sixteen of them", Create(z2), FadeIn(b16), FadeIn(n16))
        self.cue("So an RMS norm of one", FadeIn(pt))
        self.hold(0.4)
        self.clear_stage()
        head = self.heading("Xavier preserves RMS size")
        chain = mts([r"\|\vec x\|_{\rm RMS}\approx1", r"\ \xrightarrow{\ W\ }\ ", r"\|\vec h\|_{\rm RMS}\approx1"], 1.0, {0: C_TRAIN, 2: C_RAMP}).move_to([0, 1.0, 0])
        self.say("And that's what the plot showed. With Xavier scaling, the RMS size going in equals the RMS size "
                 "coming out. So can we turn that into a norm for matrices, one that measures how much a weight "
                 "matrix grows RMS size?")
        self.play(Write(head), Write(chain))
        self.cue("So can we turn", Indicate(chain[1], color=C_STEP))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 3
    def induced(self):
        head = self.heading("The induced RMS to RMS norm")
        ind = mts([r"\|A\|_{\alpha\to\beta}=\max_{\|\vec x\|_\alpha=1}\|A\vec x\|_\beta"], 0.9).move_to([-2.5, 2.4, 0])
        rr = mts([r"\|A\|_{\rm RMS\to RMS}=\max_{\|\vec x\|_{\rm RMS}=1}\|A\vec x\|_{\rm RMS}"], 0.85).move_to([-2.5, 1.2, 0])
        self.say("There's a standard way to do that, and it's called the induced norm. Feed in every input of size "
                 "one, and take the biggest output. If we measure both sides in RMS, it tells us how much the "
                 "matrix can grow an input of RMS size one.")
        self.play(Write(head), Write(ind))
        self.cue("If we measure both", Write(rr))
        d1 = mts([r"\|\vec x\|_{\rm RMS}=1\iff\|\vec x\|_2=\sqrt{d_{\rm in}}"], 0.8).move_to([-2.5, 0.2, 0])
        d2 = mts([r"\|A\vec x\|_{\rm RMS}=\dfrac{1}{\sqrt{d_{\rm out}}}\|A\vec x\|_2"], 0.8).move_to([-2.5, -0.8, 0])
        d3 = mts([r"\Rightarrow\ \|A\|_{\rm RMS\to RMS}=", r"\sqrt{\dfrac{d_{\rm in}}{d_{\rm out}}}", r"\,\|A\|_2"], 0.85, {1: C_WIDTH}).move_to([-2.5, -1.85, 0])
        assert max(x.get_right()[0] for x in (ind, rr, d1, d2, d3)) < 1.6, [x.get_right()[0] for x in (ind, rr, d1, d2, d3)]
        self.say("An input with RMS norm one has length root d_in, and an output's RMS norm is its length over "
                 "root d_out. Put those together, and the RMS to RMS norm is just the spectral norm, times the "
                 "square root of d_in over d_out.")
        self.play(Write(d1))
        self.cue("and an output's", Write(d2))
        self.cue("Put those together", Write(d3))
        # numeric check panel
        pan = VGroup(txt(f"A: {D_OUT} × {D_IN}, random", 24, C_TEXT),
                     txt(f"σ_max = {SA[0]:.3f}", 26, C_SV),
                     txt(f"2 · σ_max = {NORM_RMS:.3f}", 26, C_WIDTH),
                     txt(f"random inputs: at most {max(trials):.2f}", 22, GREY_A),
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.4, 0.3, 0])
        assert pan.get_right()[0] < 7.0 and pan.get_left()[0] > 1.7, (pan.get_left()[0], pan.get_right()[0])
        self.say("Let's check it on a random matrix that's sixty-four by two hundred fifty-six. Its spectral norm "
                 "is one point four nine, so its RMS to RMS norm should be twice that, or two point nine eight. "
                 "And sure enough, two thousand random inputs never grow by more than one point two nine.")
        self.play(FadeIn(pan[0], shift=LEFT * 0.2))
        self.cue("Its spectral norm", FadeIn(pan[1], shift=LEFT * 0.2))
        self.cue("so its RMS to RMS norm", FadeIn(pan[2], shift=LEFT * 0.2))
        self.cue("And sure enough", FadeIn(pan[3], shift=LEFT * 0.2))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 4
    def shapes(self):
        head = self.heading("Using it in the recipe")
        rec = mts([r"\arg\min_{\|\Delta W\|_{\rm RMS\to RMS}\le\eta}\langle\nabla_W\mathcal L,\Delta W\rangle"], 0.8).move_to([0, 2.4, 0])
        eq = mts([r"\Rightarrow\ \|\Delta W\|_2\le", r"\sqrt{\dfrac{d_{\rm out}}{d_{\rm in}}}", r"\,\eta", r"\ \Rightarrow\ \Delta W^{*}=-\eta", r"\sqrt{\dfrac{d_{\rm out}}{d_{\rm in}}}", r"U_rV_r^{\top}"],
                 0.8, {1: C_WIDTH, 4: C_WIDTH}).move_to([0, 1.2, 0])
        assert eq.width < 13.0 and rec.width < 13.0
        self.say("Now drop this norm into our recipe from episode one, and allow steps whose RMS to RMS norm is at "
                 "most eta. In spectral terms, that's eta times the square root of d_out over d_in. So the best "
                 "step is that amount times U V transpose.")
        self.play(Write(head), Write(rec))
        self.cue("In spectral terms", Write(eq))
        # table for three shapes
        hdr = ["layer  (d_out × d_in)", "spectral size of step", "change in output, RMS"]
        colx = [-4.2, 0.4, 4.3]
        cells = VGroup(*[txt(h, 22, GREY_B).move_to([colx[j], -0.1, 0]) for j, h in enumerate(hdr)])
        rows = VGroup()
        for i, (do, di, spec, dh) in enumerate(ROWS):
            y = -0.75 - 0.55 * i
            rows.add(VGroup(txt(f"{do} × {di}", 28, C_TEXT).move_to([colx[0], y, 0]),
                            txt(f"η · {np.sqrt(do / di):g} = {spec:g}", 28, C_WIDTH).move_to([colx[1], y, 0]),
                            txt(f"{dh:.2f}  =  η", 28, C_STEP).move_to([colx[2], y, 0])))
        assert rows.get_bottom()[1] > -2.5 and rows.get_right()[0] < 7.0 and cells.get_right()[0] < 7.0
        assert ETA == 0.1
        self.say("Try an eta of zero point one on three layer shapes. A layer that narrows gets a smaller spectral "
                 "step, and a layer that widens gets a bigger one. But look at the last column, where every "
                 "layer's output changes by exactly eta.")
        self.play(FadeIn(cells), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3))
        self.cue("But look at the last column", *[Indicate(r[2], color=C_STEP) for r in rows])
        self.say("So one eta gives each layer its own right rate, and the fan-in and fan-out do the adjusting. "
                 "Push that idea to growing widths and you get maximal update parametrization, which is where "
                 "this unit ends up.")
        self.play(Indicate(eq[1], color=C_WIDTH), Indicate(eq[4], color=C_WIDTH))
        self.hold(0.5)
