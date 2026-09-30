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

    def construct(self):
        self.title_card()
        self.xavier()
        self.rms_norm()
        self.induced()
        self.shapes()
        self.end_card(
            ["Xavier initialization keeps the RMS size of activations steady",
             "RMS norm: the ordinary length divided by root d, so an entry is about size one",
             "Induced RMS to RMS norm: root d_in over d_out times the spectral norm",
             "A step of RMS size eta moves every layer's output by eta, whatever its shape"],
        )

    # ---------------------------------------------------------------- 1
    def xavier(self):
        head = self.heading("Recap: Xavier initialization")
        nn = neuron(-3.3, 0.6)
        want = txt("inputs ≈ N(0, 1)   →   want h ≈ N(0, 1)", 26, GREY_A).move_to([-2.0, -1.5, 0])
        self.say("Recall Xavier initialization. A neuron with d_in standard normal inputs should output a standard normal too.",
                 Write(head), FadeIn(nn), FadeIn(want))
        eqs = VGroup(
            mts([r"h=\vec w^{\top}\vec x=\sum_i w_i x_i"], 0.75),
            mts([r"\mathbb E[h^2]=", r"\sigma_w^2", r"\sum_i x_i^2"], 0.75, {1: C_LAM}),
            mts([r"x_i^2\approx1\ \Rightarrow\ \sigma_w^2\approx\dfrac{1}{d_{\rm in}}"], 0.75),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.3, 0.6, 0])
        assert eqs.get_right()[0] < 7.0 and eqs.get_left()[0] > 0.2, eqs.get_center()
        self.say("With independent zero-mean weights, the expected square of h is the weight variance times the sum of squared inputs.",
                 Write(eqs[0]), Write(eqs[1]))
        self.say("If each squared input is about one, the sum is d_in, so the weight variance should be one over d_in.", Write(eqs[2]))
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
        self.say("Feed random inputs through a layer. With unit-variance weights, outputs grow like the root of the fan-in.",
                 Write(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), Create(ps), FadeIn(ds), FadeIn(lb1))
        self.say(f"At d_in of 4096 that is about {RMS_STD[-1]:.0f} times too large. With variance one over d_in, the size stays near one.",
                 Create(px), FadeIn(dx), FadeIn(lb2))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 2
    def rms_norm(self):
        head = self.heading("Which norm is being preserved?")
        eq = mts([r"\|\vec x\|_{\rm RMS}=\dfrac{1}{\sqrt{d}}\|\vec x\|_2=\sqrt{\dfrac1d\sum_i x_i^2}"], 0.9).move_to([0, 2.5, 0])
        self.say("Xavier quietly preserves a norm: the length divided by root d, the root-mean-square or RMS norm.",
                 Write(head), Write(eq))

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
        self.say("Four entries of plus or minus one have length 2, sixteen have length 4. The RMS is one for both.",
                 Create(z1), Create(z2), FadeIn(b4), FadeIn(b16), FadeIn(n4), FadeIn(n16))
        pt = txt("RMS ≈ 1  ⇒  typical entry about 1, at any width", 28, C_STEP).move_to([0, -2.2, 0])
        self.say("RMS one means every entry is about size one.", FadeIn(pt))
        self.hold(0.4)
        self.clear_stage()
        head = self.heading("Xavier preserves RMS size")
        chain = mts([r"\|\vec x\|_{\rm RMS}\approx1", r"\ \xrightarrow{\ W\ }\ ", r"\|\vec h\|_{\rm RMS}\approx1"], 1.0, {0: C_TRAIN, 2: C_RAMP}).move_to([0, 1.0, 0])
        self.say("That is what the plot showed: with Xavier scaling, output RMS size matches input RMS size.",
                 Write(head), Write(chain))
        self.say("Is there a matrix version of the RMS norm, measuring how much a weight matrix changes RMS size?",
                 Indicate(chain[1], color=C_STEP))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 3
    def induced(self):
        head = self.heading("The induced RMS to RMS norm")
        ind = mts([r"\|A\|_{\alpha\to\beta}=\max_{\|\vec x\|_\alpha=1}\|A\vec x\|_\beta"], 0.9).move_to([-2.5, 2.4, 0])
        rr = mts([r"\|A\|_{\rm RMS\to RMS}=\max_{\|\vec x\|_{\rm RMS}=1}\|A\vec x\|_{\rm RMS}"], 0.85).move_to([-2.5, 1.2, 0])
        self.say("Recall the induced matrix norm: the largest output size, measured in one norm, over inputs of size one in another.",
                 Write(head), Write(ind))
        self.say("Use RMS on both sides: how much can A grow an input of RMS size one?",
                 Write(rr))
        d1 = mts([r"\|\vec x\|_{\rm RMS}=1\iff\|\vec x\|_2=\sqrt{d_{\rm in}}"], 0.8).move_to([-2.5, 0.2, 0])
        d2 = mts([r"\|A\vec x\|_{\rm RMS}=\dfrac{1}{\sqrt{d_{\rm out}}}\|A\vec x\|_2"], 0.8).move_to([-2.5, -0.8, 0])
        d3 = mts([r"\Rightarrow\ \|A\|_{\rm RMS\to RMS}=", r"\sqrt{\dfrac{d_{\rm in}}{d_{\rm out}}}", r"\,\|A\|_2"], 0.85, {1: C_WIDTH}).move_to([-2.5, -1.85, 0])
        assert max(x.get_right()[0] for x in (ind, rr, d1, d2, d3)) < 1.6, [x.get_right()[0] for x in (ind, rr, d1, d2, d3)]
        self.say("An input of RMS one has length root d_in. An output's RMS is its length over root d_out.", Write(d1), Write(d2))
        self.say("So the RMS to RMS norm is the spectral norm times root of d_in over d_out.", Write(d3))
        # numeric check panel
        pan = VGroup(txt(f"A: {D_OUT} × {D_IN}, random", 24, C_TEXT),
                     txt(f"σ_max = {SA[0]:.3f}", 26, C_SV),
                     txt(f"2 · σ_max = {NORM_RMS:.3f}", 26, C_WIDTH),
                     txt(f"random inputs: at most {max(trials):.2f}", 22, GREY_A),
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.4, 0.3, 0])
        assert pan.get_right()[0] < 7.0 and pan.get_left()[0] > 1.7, (pan.get_left()[0], pan.get_right()[0])
        self.say(f"Check: a 64 by 256 matrix has spectral norm {SA[0]:.2f}, so its RMS norm is twice that, {NORM_RMS:.2f}.",
                 LaggedStart(*[FadeIn(p, shift=LEFT * 0.2) for p in pan], lag_ratio=0.3))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 4
    def shapes(self):
        head = self.heading("Using it in the recipe")
        rec = mts([r"\arg\min_{\|\Delta W\|_{\rm RMS\to RMS}\le\eta}\langle\nabla_W\mathcal L,\Delta W\rangle"], 0.8).move_to([0, 2.4, 0])
        eq = mts([r"\Rightarrow\ \|\Delta W\|_2\le", r"\sqrt{\dfrac{d_{\rm out}}{d_{\rm in}}}", r"\,\eta", r"\ \Rightarrow\ \Delta W^{*}=-\eta", r"\sqrt{\dfrac{d_{\rm out}}{d_{\rm in}}}", r"U_rV_r^{\top}"],
                 0.8, {1: C_WIDTH, 4: C_WIDTH}).move_to([0, 1.2, 0])
        assert eq.width < 13.0 and rec.width < 13.0
        self.say("Now put this norm into the optimizer recipe from episode one: steps of RMS to RMS size at most eta.",
                 Write(head), Write(rec))
        self.say("The spectral size allowed is eta times root of d_out over d_in, so the best step is that factor times U V transpose.",
                 Write(eq))
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
        self.say(f"Try eta equal to {ETA:g} on three shapes. Wide-to-narrow layers get a smaller spectral step, narrow-to-wide a larger one.",
                 FadeIn(cells), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3))
        self.say("Yet each layer's output changes by exactly eta in RMS size. One number eta behaves like a layer-specific learning rate.",
                 *[Indicate(r[2], color=C_STEP) for r in rows])
        self.say("Fan-in and fan-out do the adjusting. Making this precise for growing width is the idea behind maximal update parametrization.",
                 Indicate(eq[1], color=C_WIDTH), Indicate(eq[4], color=C_WIDTH))
        self.hold(0.5)
