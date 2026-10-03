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
assert [f"{v:.2f}" for v in SA] == ["2.14", "0.69"]            # spoken in spectral_norm()

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
# the numbers as they are spoken in solve() and flatten()
assert [f"{v:.2f}" for v in S] == ["3.54", "2.15", "0.77"]
assert (f"{NUC:.2f}", f"{FRO:.2f}", f"{BEST:.2f}", f"{COND:.1f}") == ("6.46", "4.21", "4.80", "4.6")
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
    SCENES = ["matrices", "spectral_norm", "solve", "flatten"]

    def construct(self):
        self.title_card()
        self.matrices()
        self.spectral_norm()
        self.solve()
        self.flatten()
        self.end_card(
            ["Weights are matrices, so measure a step as a matrix too",
             "Spectral norm: the most a matrix can stretch a unit vector",
             "Steepest descent in the spectral ball: minus eta times U V transpose",
             "U V transpose keeps the gradient's directions and sets every singular value to one (Shampoo)"],
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
        self.say("So far we've treated theta as one long vector. But a network's weights come as matrices, one for "
                 "each layer. And every scaling problem we met in Xavier initialization came from those weight "
                 "matrices. So let's measure a step as what it really is, which is a matrix.")
        self.play(Write(head), LaggedStart(*[Write(e) for e in eqs], lag_ratio=0.4))
        self.cue("And every scaling problem", Create(box))
        self.hold(0.2)
        # inner product of matrices
        self.play(FadeOut(eqs), FadeOut(box))
        gm = mt(r"G=" + mat_tex(GM), 0.9)
        dm = mt(r"\Delta W=" + mat_tex(DM), 0.9)
        mats = VGroup(gm, dm).arrange(RIGHT, buff=1.0).move_to([0, 1.5, 0])
        assert mats.width < 12
        prods = mt(r"\langle G,\Delta W\rangle_F=2\cdot1+(-1)\cdot0+0\cdot2+1\cdot3=5", 0.85).move_to([0, 0.0, 0])
        tr = mt(r"=\mathrm{trace}(G^{\top}\Delta W)=\mathrm{trace}" + mat_tex(GM.T @ DM) + r"=5", 0.85).move_to([0, -1.2, 0])
        assert tr.width < 13
        self.say("First we need an inner product for matrices. Multiply the entries in matching spots and add "
                 "everything up, which here gives five. That's the same number you get from the trace of G transpose "
                 "times the step.")
        self.play(FadeIn(mats))
        self.cue("Multiply the entries", Write(prods))
        self.cue("That's the same number", Write(tr))
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
        pts = [ctr + np.array([*(AM @ np.array([np.cos(t), np.sin(t)])), 0.0]) for t in th[::100]]
        ell = VMobject(stroke_color=C_MODEL, stroke_width=4).set_points_as_corners(pts + [pts[0]])
        self.say("How big is a matrix? Take this two by two matrix, and feed it every input of length one, which is "
                 "the whole unit circle. What comes out the other side is an ellipse.")
        self.play(Write(head), Create(ax), Create(circ), Write(eqA))
        self.cue("What comes out", ReplacementTransform(circ.copy(), ell), run_time=2.0)
        s1 = Arrow(ctr, ctr + np.array([*(SA[0] * UA[:, 0]), 0.0]), buff=0, color=C_SV, stroke_width=6, max_tip_length_to_length_ratio=0.15)
        s2 = Arrow(ctr, ctr + np.array([*(SA[1] * UA[:, 1]), 0.0]), buff=0, color=C_SV, stroke_width=6, max_tip_length_to_length_ratio=0.25)
        assert (ctr + np.array([*(SA[0] * UA[:, 0]), 0.0]))[1] < 2.6
        l1 = txt(f"σ₁ = {SA[0]:.2f}", 26, C_SV).next_to(s1.get_end(), UR if UA[1, 0] > 0 else DL, buff=0.03)
        l2 = txt(f"σ₂ = {SA[1]:.2f}", 26, C_SV).next_to(s2.get_end(), UP, buff=0.25).shift(LEFT*0.5)
        defn = VGroup(mt(r"\|A\|_2=\sigma_{\max}=\max_{\|\vec x\|_2=1}\|A\vec x\|_2", 0.8)).move_to([3.0, 0.9, 0])
        assert defn.get_right()[0] < 7.0 and defn.get_left()[0] > -0.4
        bound = mt(r"\|\Delta W\|_2\le\eta", 0.9, ).move_to([3.0, -0.4, 0])
        self.say("Its longest stretch is two point one four, and that's the largest singular value. The shortest is "
                 "zero point six nine. The biggest stretch is what we call the spectral norm, so it's the most the "
                 "matrix can stretch a unit vector. That makes the spectral ball of radius eta the set of steps that "
                 "stretch no input by more than eta.")
        self.play(GrowArrow(s1), FadeIn(l1))
        self.cue("The shortest is", GrowArrow(s2), FadeIn(l2))
        self.cue("The biggest stretch", Write(defn))
        self.cue("That makes the spectral ball", Write(bound))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 3
    def solve(self):
        head = self.heading("Steepest descent in the spectral ball")
        goal = mts([r"\arg\min_{\|\Delta W\|_2\le\eta}", r"\big\langle\nabla_W\mathcal L,\Delta W\big\rangle"], 0.85, {1: C_GRAD})
        goal.move_to([0, 2.3, 0])
        svd = mts([r"\nabla_W\mathcal L=U\Sigma V^{\top}=\sum_i", r"\sigma_i", r"\vec u_i\vec v_i^{\top}"], 0.85, {1: C_SV})
        svd.move_to([0, 1.3, 0])
        self.say("Now ask our question for a matrix. Which step of spectral size eta lowers the linearized loss the "
                 "most? To answer it, break the gradient into its singular value decomposition. That gives us output "
                 "directions U, input directions V, and a stretch sigma for each pair.")
        self.play(Write(head), Write(goal))
        self.cue("To answer it", Write(svd))
        a = mts([r"\max_{\|B\|_2\le1}\mathrm{trace}(A^{\top}B)=\max_{\|B\|_2\le1}\sum_i", r"\sigma_i", r"\,\vec u_i^{\top}B\,\vec v_i"], 0.8, {1: C_SV})
        a.move_to([0, 0.15, 0])
        b = mts([r"\big|\vec u_i^{\top}B\,\vec v_i\big|\le\|B\|_2\le1", r"\ \Rightarrow\ \le\sum_i", r"\sigma_i"], 0.8, {2: C_SV})
        b.move_to([0, -0.85, 0])
        c = mts([r"\text{equality at }B=UV^{\top}", r"\ \Rightarrow\ ", r"\Delta W^{*}=-\eta\,UV^{\top}"], 0.85, {2: C_STEP})
        c.move_to([0, -1.85, 0])
        assert max(x.width for x in (a, b, c)) < 13.0 and c.get_bottom()[1] > -2.4
        self.say("The trace is linear, so the inner product splits into a sum, with each singular value times one "
                 "number. Each of those numbers is at most one, because B can't stretch anything past one. So the sum "
                 "of the sigmas is a ceiling, and choosing B to be U V transpose hits it exactly. That makes the best "
                 "step minus eta times U V transpose.")
        self.play(Write(a))
        self.cue("Each of those numbers", Write(b))
        self.cue("and choosing B", Write(c))
        self.cue("That makes the best step", Indicate(c[2], color=C_STEP))
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
        self.say("Let's check that with numbers. Take a random five by three gradient. Its singular values are three "
                 "point five four, two point one five and zero point seven seven. Together they add up to six point "
                 "four six.")
        self.play(Write(head), FadeIn(sub))
        self.cue("Together they add up", FadeIn(bars[2]))
        self.say("The gradient step collects only four point two one. And twenty thousand random tries never get past "
                 "four point eight. Only U V transpose collects the full sum. So a bigger ball of allowed steps buys "
                 "us a bigger predicted drop.")
        self.play(FadeIn(bars[0]))
        self.cue("And twenty thousand", FadeIn(bars[1]))
        self.cue("Only U V transpose", Indicate(bars[2][0], color=C_STEP))
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
        new = VGroup()
        for x in xs:
            r = Rectangle(width=0.8, height=1.0 * sc, stroke_color=C_STEP, fill_color=C_STEP, fill_opacity=0.3, stroke_width=3)
            r.move_to([x + 6.6, base_y + sc / 2, 0])
            new.add(r)
        nlabs = VGroup(*[txt("1", 24, C_STEP).next_to(new[i], DOWN, buff=0.12) for i in range(3)])
        title2 = txt("spectral step  U Vᵀ", 26, C_STEP).move_to([3.0, 2.2, 0])
        arr = Arrow([-1.2, 0.0, 0], [0.6, 0.0, 0], buff=0, color=GREY_B, stroke_width=4)
        assert new[-1].get_right()[0] < 7.0
        self.say("Now look at what this step does. The gradient has three very different singular values. But U V "
                 "transpose keeps the directions and throws the stretches away, so every singular value becomes one.")
        self.play(Write(head), FadeIn(title), FadeIn(old), FadeIn(labs))
        self.cue("keeps the directions", Create(arr), FadeIn(title2), *[TransformFromCopy(o, n) for o, n in zip(old, new)], FadeIn(nlabs))
        info = VGroup(txt(f"condition number  σ₁ / σ₃ = {COND:.1f}  →  1", 26, C_TEXT),
                      txt("every direction gets the same size of step", 26, GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -1.85, 0])
        assert info.width < 12 and info.get_bottom()[1] > -2.5
        self.say("A matrix like that is called semi-orthogonal. Its condition number drops from four point six all the "
                 "way down to one. That means every direction gets the same size of step, and the big singular values "
                 "don't get to hog it.")
        self.play(FadeIn(info[0]))
        self.cue("That means every direction", FadeIn(info[1]))
        self.hold(0.3)
        self.clear_stage()
        # shampoo
        head = self.heading("This is Shampoo")
        eq = mts([r"(GG^{\top})^{-1/4}\;G\;(G^{\top}G)^{-1/4}", r"=UV^{\top}"], 0.95, {1: C_STEP}).move_to([0, 1.5, 0])
        self.say("And this isn't new. It's the Shampoo optimizer, from Gupta and coauthors in twenty seventeen and "
                 "twenty eighteen. Shampoo squeezes the gradient from both sides with inverse fourth roots, and out "
                 "comes U V transpose again.")
        self.play(Write(head))
        self.cue("Shampoo squeezes", Write(eq))
        award = VGroup(txt("A variant of Shampoo (Dahl et al., 2023)", 28, C_TEXT),
                       txt("won the AlgoPerf training-algorithm competition", 28, C_TEXT)
                       ).arrange(DOWN, buff=0.15).move_to([0, -0.3, 0])
        nxt = txt("But an SVD every step is expensive, and what should the step size be?", 28, GREY_A).move_to([0, -1.7, 0])
        self.say("A variant of it, from Dahl and coauthors, won the AlgoPerf contest in twenty twenty-three. There are "
                 "two catches, though. An SVD at every step is expensive, and we still don't know what step size fits "
                 "layers of different shapes.")
        self.play(FadeIn(award))
        self.cue("There are two catches", FadeIn(nxt))
        self.hold(0.6)
