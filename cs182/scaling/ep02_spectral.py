"""Episode 2 — Matrices Want the Spectral Norm (Lecture 7: matrix parameters, spectral norm, Shampoo)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers

# (a) Frobenius inner product = trace(G^T D)
GM = np.array([[2.0, -1.0], [0.0, 1.0]])
DM = np.array([[1.0, 0.0], [2.0, 3.0]])
IP = float(np.sum(GM * DM))
assert IP == float(np.trace(GM.T @ DM)) == 5.0

# (b) spectral norm of a 2x2 matrix: unit circle -> ellipse
AM = np.array([[1.8, 0.8], [0.4, 1.0]])
UA, SA, VAt = np.linalg.svd(AM)
th = np.linspace(0, 2 * np.pi, 20001)
lens = np.linalg.norm(AM @ np.stack([np.cos(th), np.sin(th)]), axis=0)
assert abs(lens.max() - SA[0]) < 1e-6 and abs(lens.min() - SA[1]) < 1e-6

# (c) steepest descent in the spectral-norm ball
rng = np.random.RandomState(0)
GG = rng.randn(5, 3)
U, S, Vt = np.linalg.svd(GG, full_matrices=False)
NUC = float(S.sum())                       # max of <G, B> over ||B||_2 <= 1
FRO = float(np.linalg.norm(GG))            # value attained by the gradient-descent step G / ||G||_F
B_STAR = U @ Vt
assert abs(np.sum(GG * B_STAR) - NUC) < 1e-12 and abs(np.linalg.norm(B_STAR, 2) - 1) < 1e-12
BEST = -1.0
for _ in range(20000):
    M = rng.randn(5, 3)
    M /= np.linalg.norm(M, 2)
    BEST = max(BEST, float(np.sum(GG * M)))
assert BEST < NUC and FRO < BEST < NUC          # random feasible matrices never beat U V^T
assert np.linalg.norm(GG / FRO, 2) < 1            # the Frobenius step is feasible in the spectral ball, but inside it
COND = float(S[0] / S[-1])
assert abs(S[0] - 3.5379) < 1e-3 and abs(NUC - 6.4557) < 1e-3 and abs(FRO - 4.2102) < 1e-3
# Shampoo-style preconditioning (no accumulation) gives the same U V^T


def mpow(M, p):
    w, Q = np.linalg.eigh(M)
    return (Q * w ** p) @ Q.T


SH = mpow(GG.T @ GG, -0.25)
SHL = U @ np.diag(S ** -0.5) @ U.T          # (G G^T)^(-1/4) restricted to the range of G
assert np.allclose(SHL @ GG @ SH, B_STAR)
assert np.allclose(GG @ Vt.T @ np.diag(np.ones(3)), U @ np.diag(S))       # G v_i = sigma_i u_i


def mat_tex(M, fmt="{:g}"):
    rows = " \\\\ ".join(" & ".join(fmt.format(v) for v in r) for r in M)
    return r"\begin{bmatrix}" + rows + r"\end{bmatrix}"


class Ep02Spectral(NarratedScene):
    series = SERIES

    def construct(self):
        self.title_card()
        self.matrices()
        self.spectral_norm()
        self.solve()
        self.flatten()
        self.end_card(
            ["Weights live in matrices, so measure a step ΔW as a matrix",
             "The spectral norm is the largest singular value",
             "Steepest descent in the spectral ball: minus eta times U Vᵀ",
             "That flattens every singular value of the gradient to one (Shampoo)"],
        )

    # ---------------------------------------------------------------- 1
    def matrices(self):
        head = self.heading("Parameters are matrices")
        eqs = VGroup(
            mts([r"\vec h_1=\mathrm{ReLU}\big[\vec b_0+W_0\,\vec x\big]"], 0.8),
            mts([r"\vec h_j=\mathrm{ReLU}\big[\vec b_j+W_{j-1}\,\vec h_{j-1}\big]"], 0.8),
            mts([r"\vec y=\mathrm{ReLU}\big[\vec b_k+W_k\,\vec h_k\big]"], 0.8),
        ).arrange(DOWN, buff=0.3).move_to([-2.6, 1.3, 0])
        box = SurroundingRectangle(eqs, color=C_MODEL, buff=0.25, stroke_width=2)
        self.say("Until now we treated the parameters theta as one long vector. But network parameters live in matrices, one per layer.",
                 Write(head), LaggedStart(*[Write(e) for e in eqs], lag_ratio=0.4))
        self.say("Recall from Xavier initialization: scaling problems come from the weight matrices.", Create(box))
        self.say("So let's measure the change ΔW in weight-matrix space instead.")
        # inner product of matrices
        self.play(FadeOut(eqs), FadeOut(box))
        gm = mt(r"G=" + mat_tex(GM), 0.9)
        dm = mt(r"\Delta W=" + mat_tex(DM), 0.9)
        mats = VGroup(gm, dm).arrange(RIGHT, buff=1.0).move_to([0, 1.5, 0])
        assert mats.width < 12
        self.say("The matching inner product multiplies entries in the same position and adds them up.", FadeIn(mats))
        prods = mt(r"\langle G,\Delta W\rangle_F=2\cdot1+(-1)\cdot0+0\cdot2+1\cdot3=5", 0.85).move_to([0, 0.0, 0])
        tr = mt(r"=\mathrm{trace}(G^{\top}\Delta W)=\mathrm{trace}" + mat_tex(GM.T @ DM) + r"=5", 0.85).move_to([0, -1.2, 0])
        assert tr.width < 13
        self.say("That number is the trace of G transpose times ΔW. Here both ways give five.", Write(prods), Write(tr))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 2
    def spectral_norm(self):
        head = self.heading("The spectral norm")
        ctr = np.array([-3.4, 0.3, 0.0])
        ax = VGroup(Line(ctr + LEFT * 2.6, ctr + RIGHT * 2.6, color=GREY_D, stroke_width=2),
                    Line(ctr + DOWN * 2.3, ctr + UP * 2.4, color=GREY_D, stroke_width=2))
        circ = Circle(radius=1.0, color=GREY_A, stroke_width=4).move_to(ctr)
        clab = txt("unit circle ‖x‖₂ = 1", 24, GREY_A).next_to(circ, DOWN, buff=1.35).shift(LEFT * 0.0)
        eqA = mt(r"A=" + mat_tex(AM), 0.85).move_to([2.8, 2.3, 0])
        self.say("Here is a 2 by 2 matrix A. Feed it every input of length one, the unit circle.",
                 Write(head), Create(ax), Create(circ), Write(eqA))
        pts = [ctr + np.array([*(AM @ np.array([np.cos(t), np.sin(t)])), 0.0]) for t in th[::100]]
        ell = VMobject(stroke_color=C_MODEL, stroke_width=4).set_points_as_corners(pts + [pts[0]])
        self.say("It maps the circle to an ellipse.", ReplacementTransform(circ.copy(), ell), run_time=2.0)
        s1 = Arrow(ctr, ctr + np.array([*(SA[0] * UA[:, 0]), 0.0]), buff=0, color=C_SV, stroke_width=6, max_tip_length_to_length_ratio=0.15)
        s2 = Arrow(ctr, ctr + np.array([*(SA[1] * UA[:, 1]), 0.0]), buff=0, color=C_SV, stroke_width=6, max_tip_length_to_length_ratio=0.25)
        assert (ctr + np.array([*(SA[0] * UA[:, 0]), 0.0]))[1] < 2.6
        l1 = txt(f"σ₁ = {SA[0]:.2f}", 26, C_SV).next_to(s1.get_end(), UR if UA[1, 0] > 0 else DL, buff=0.03)
        l2 = txt(f"σ₂ = {SA[1]:.2f}", 26, C_SV).next_to(s2.get_end(), UP, buff=0.25).shift(LEFT*0.5)
        self.say(f"The longest stretch is the largest singular value, {SA[0]:.2f}. The shortest is {SA[1]:.2f}.",
                 GrowArrow(s1), GrowArrow(s2), FadeIn(l1), FadeIn(l2))
        defn = VGroup(mt(r"\|A\|_2=\sigma_{\max}=\max_{\|\vec x\|_2=1}\|A\vec x\|_2", 0.8)).move_to([3.0, 0.9, 0])
        assert defn.get_right()[0] < 7.0 and defn.get_left()[0] > -0.4
        self.say("The spectral norm of a matrix is exactly this: the largest amount it can stretch a unit vector.", Write(defn))
        bound = mt(r"\|\Delta W\|_2\le\eta", 0.9, ).move_to([3.0, -0.4, 0])
        self.say("So a spectral-norm ball of radius eta contains every matrix that stretches no input by more than eta.", Write(bound))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 3
    def solve(self):
        head = self.heading("Steepest descent in the spectral ball")
        goal = mts([r"\arg\min_{\|\Delta W\|_2\le\eta}", r"\big\langle\nabla_W\mathcal L,\Delta W\big\rangle"], 0.85, {1: C_GRAD})
        goal.move_to([0, 2.3, 0])
        svd = mts([r"\nabla_W\mathcal L=U\Sigma V^{\top}=\sum_i", r"\sigma_i", r"\vec u_i\vec v_i^{\top}"], 0.85, {1: C_SV})
        svd.move_to([0, 1.3, 0])
        self.say("Now the same question as before, for a matrix: the step of spectral size eta that lowers the linearized loss most.",
                 Write(head), Write(goal))
        self.say("Write the gradient's singular value decomposition: left vectors U, singular values sigma, right vectors V.", Write(svd))
        a = mts([r"\max_{\|B\|_2\le1}\mathrm{trace}(A^{\top}B)=\max_{\|B\|_2\le1}\sum_i", r"\sigma_i", r"\,\vec u_i^{\top}B\,\vec v_i"], 0.8, {1: C_SV})
        a.move_to([0, 0.15, 0])
        b = mts([r"\big|\vec u_i^{\top}B\,\vec v_i\big|\le\|B\|_2\le1", r"\ \Rightarrow\ \le\sum_i", r"\sigma_i"], 0.8, {2: C_SV})
        b.move_to([0, -0.85, 0])
        c = mts([r"\text{equality at }B=UV^{\top}", r"\ \Rightarrow\ ", r"\Delta W^{*}=-\eta\,UV^{\top}"], 0.85, {2: C_STEP})
        c.move_to([0, -1.85, 0])
        assert max(x.width for x in (a, b, c)) < 13.0 and c.get_bottom()[1] > -2.4
        self.say("Trace is linear, so the inner product becomes a sum: each singular value times one small scalar.", Write(a))
        self.say("Each scalar is at most one, because B cannot stretch anything past one. So the total is at most the sum of singular values.", Write(b))
        self.say("And B equals U V transpose reaches that bound. So the best step is minus eta times U V transpose.", Write(c),
                 Indicate(c[2], color=C_STEP))
        self.hold(0.4)
        self.clear_stage()
        # numbers
        head = self.heading("Checking with numbers")
        base_y, sc = -1.4, 0.4
        vals = [FRO, BEST, NUC]
        names = ["gradient step\nG / ‖G‖_F", "best of 20,000\nrandom matrices", "spectral step\nU Vᵀ"]
        cols = [C_GRAD, GREY_B, C_STEP]
        bars = VGroup()
        for i, (v, n, col) in enumerate(zip(vals, names, cols)):
            x = -3.6 + 3.6 * i
            r = Rectangle(width=1.7, height=v * sc, stroke_color=col, fill_color=col, fill_opacity=0.3, stroke_width=3)
            r.move_to([x, base_y + v * sc / 2, 0])
            val = txt(f"{v:.2f}", 30, col).next_to(r, UP, buff=0.1)
            nm = txt(n, 22, GREY_A, line_spacing=0.9).next_to(r, DOWN, buff=0.15)
            bars.add(VGroup(r, val, nm))
        assert max(b[0].get_top()[1] for b in bars) < 3.0 and min(b[2].get_bottom()[1] for b in bars) > -2.5
        sub = mt(r"\text{decrease }\ -\langle G,\Delta W\rangle/\eta\ \text{ for a }5\times3\text{ gradient}", 0.65).move_to([0, 2.7, 0])
        self.say(f"Take a random 5 by 3 gradient. Its singular values are {S[0]:.2f}, {S[1]:.2f}, {S[2]:.2f}, which sum to {NUC:.2f}.",
                 Write(head), FadeIn(sub), FadeIn(bars[2]))
        self.say(f"Normalized G gains only {FRO:.2f}. Twenty thousand random steps never beat {BEST:.2f}.",
                 FadeIn(bars[0]), FadeIn(bars[1]))
        self.say("Only U V transpose reaches the full sum. The larger ball of allowed steps buys a larger predicted decrease.",
                 Indicate(bars[2][0], color=C_STEP))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 4
    def flatten(self):
        head = self.heading("Every singular value becomes one")
        base_y, sc = -0.6, 0.62
        xs = [-4.8, -3.6, -2.4]
        old = VGroup()
        for x, s in zip(xs, S):
            r = Rectangle(width=0.8, height=s * sc, stroke_color=C_SV, fill_color=C_SV, fill_opacity=0.3, stroke_width=3)
            r.move_to([x, base_y + s * sc / 2, 0])
            old.add(r)
        labs = VGroup(*[txt(f"σ{i + 1} = {s:.2f}", 22, C_SV).next_to(old[i], DOWN, buff=0.12) for i, s in enumerate(S)])
        labs[0].shift(LEFT * 0.0)
        for lb in labs:
            lb.scale(0.85)
        title = txt("gradient  G = U Σ Vᵀ", 26, C_GRAD).move_to([-3.6, 2.2, 0])
        self.say("Look at what this step does to the gradient. The gradient has three very different singular values.",
                 Write(head), FadeIn(title), FadeIn(old), FadeIn(labs))
        new = VGroup()
        for x in xs:
            r = Rectangle(width=0.8, height=1.0 * sc, stroke_color=C_STEP, fill_color=C_STEP, fill_opacity=0.3, stroke_width=3)
            r.move_to([x + 6.6, base_y + sc / 2, 0])
            new.add(r)
        nlabs = VGroup(*[txt("1", 24, C_STEP).next_to(new[i], DOWN, buff=0.12) for i in range(3)])
        title2 = txt("spectral step  U Vᵀ", 26, C_STEP).move_to([3.0, 2.2, 0])
        arr = Arrow([-1.2, 0.0, 0], [0.6, 0.0, 0], buff=0, color=GREY_B, stroke_width=4)
        assert new[-1].get_right()[0] < 7.0
        self.say("U V transpose keeps the singular vectors, the directions, and replaces every singular value by one.",
                 Create(arr), FadeIn(title2), *[TransformFromCopy(o, n) for o, n in zip(old, new)], FadeIn(nlabs))
        info = VGroup(txt(f"condition number  σ₁ / σ₃ = {COND:.1f}  →  1", 26, C_TEXT),
                      txt("every direction gets the same size of step", 26, GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -1.85, 0])
        assert info.width < 12 and info.get_bottom()[1] > -2.5
        self.say(f"Such a matrix is semi-orthogonal. Its condition number is one, versus {COND:.1f} for the gradient.", FadeIn(info[0]))
        self.say("Uniform step in all directions, and no domination by the largest singular values.", FadeIn(info[1]))
        self.hold(0.3)
        self.clear_stage()
        # shampoo
        head = self.heading("This is Shampoo")
        eq = mts([r"(GG^{\top})^{-1/4}\;G\;(G^{\top}G)^{-1/4}", r"=UV^{\top}"], 0.95, {1: C_STEP}).move_to([0, 1.5, 0])
        self.say("This is the Shampoo optimizer of Gupta and coauthors, 2017 and 2018.", Write(head))
        self.say("Shampoo scales the gradient on both sides by inverse fourth roots. That also gives U V transpose.",
                 Write(eq))
        award = VGroup(txt("A variant of Shampoo (Dahl et al., 2023)", 28, C_TEXT),
                       txt("won the AlgoPerf training-algorithm competition", 28, C_TEXT)
                       ).arrange(DOWN, buff=0.15).move_to([0, -0.3, 0])
        self.say("A variant of Shampoo, by Dahl and coauthors in 2023, won AlgoPerf, a competition for training algorithms.", FadeIn(award))
        nxt = txt("But an SVD every step is expensive, and what should the step size be?", 28, GREY_A).move_to([0, -1.7, 0])
        self.say("Two questions remain: how to avoid computing the SVD every step, and how to set the step size for layers of different shapes.",
                 FadeIn(nxt))
        self.hold(0.6)
