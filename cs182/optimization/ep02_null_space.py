"""Episode 2 — Where Gradient Descent Cannot Go (Note 2, section 2.1.1; Lecture 2; HW1 problem 2)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers

# (a) one equation, two unknowns: w1 + 2 w2 = 5
X1 = np.array([[1.0, 2.0]])
Y1 = np.array([5.0])
ROW = np.array([1.0, 2.0])
NULL = np.array([2.0, -1.0])
assert X1 @ NULL == 0 and ROW @ NULL == 0
WMIN = (X1.T @ np.linalg.inv(X1 @ X1.T) @ Y1)
assert np.allclose(WMIN, [1, 2]) and np.isclose((X1 @ X1.T)[0, 0], 5.0)
ETA = 0.05
assert ETA < 1 / 5.0


def gd(w0, steps, eta=ETA):
    w, out = np.array(w0, float), [np.array(w0, float)]
    for _ in range(steps):
        w = w - eta * 2 * X1.T @ (X1 @ w - Y1)
        out.append(w.copy())
    return out


P0 = gd([0, 0], 12)
assert np.allclose(P0[3], WMIN * (1 - 0.5 ** 3))                        # factor 1 - 2*eta*5 = 0.5 per step
W0 = np.array([3.0, -2.0])
P1 = gd(W0, 12)
PN0 = (W0 @ NULL) / (NULL @ NULL) * NULL                                 # null component of the start
assert np.allclose(PN0, [3.2, -1.6])
WINF = WMIN + PN0
assert np.allclose(WINF, [4.2, 0.4]) and abs(X1 @ WINF - 5) < 1e-12
assert np.allclose(gd(W0, 60)[-1], WINF, atol=1e-6)
for w in P1:                                                            # null component never changes
    assert np.allclose((w @ NULL) / (NULL @ NULL) * NULL, PN0)
# closest solution to the start
zs = [WMIN + s * NULL for s in np.linspace(-3, 3, 601)]
assert np.allclose(min(zs, key=lambda z: np.linalg.norm(z - W0)), WINF, atol=0.01)
# Pythagoras at the point (5, 0)
Z5 = np.array([5.0, 0.0])
assert np.isclose(Z5 @ Z5, WMIN @ WMIN + (Z5 - WMIN) @ (Z5 - WMIN)) and (WMIN @ WMIN, (Z5 - WMIN) @ (Z5 - WMIN), Z5 @ Z5) == (5.0, 20.0, 25.0)

# (b) two equations, three unknowns, in the SVD basis
X2 = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])
Y2 = np.array([1.0, 2.0])
U2, S2, VT2 = np.linalg.svd(X2)
assert np.allclose(S2, [np.sqrt(3), 1.0])
ETA2 = 0.1
Wb0 = np.array([1.0, -1.0, 2.0])
Wb = [Wb0.copy()]
for _ in range(60):
    Wb.append(Wb[-1] - ETA2 * 2 * X2.T @ (X2 @ Wb[-1] - Y2))
COORD = [VT2 @ w for w in Wb]                                            # coordinates v_i . w_t
WMIN2 = np.linalg.pinv(X2) @ Y2
assert abs(COORD[0][2] - COORD[-1][2]) < 1e-12                          # null coordinate frozen
assert np.allclose(COORD[-1][:2], (VT2 @ WMIN2)[:2], atol=1e-4)
assert np.allclose(Wb[-1], WMIN2 + (VT2[2] @ Wb0) * VT2[2], atol=1e-4)
assert np.allclose(np.abs(VT2[2]), 1 / np.sqrt(3))
FACT2 = [1 - 2 * ETA2 * s ** 2 for s in S2]
assert np.allclose(FACT2, [0.4, 0.8])
STAGES = [0, 1, 2, 4, 8, 20]


class Ep02NullSpace(NarratedScene):
    series = SERIES

    def construct(self):
        self.title_card()
        self.solution_set()
        self.row_space_update()
        self.other_start()
        self.svd_bars()
        self.end_card(
            ["With more parameters than data, infinitely many weight vectors fit perfectly",
             "Every gradient step lies in the row space, so the null-space component never changes",
             "Starting at zero, gradient descent finds the minimum-norm solution, X transpose times X X transpose inverse times y",
             "From any other start it finds the interpolating solution closest to where it began"],
        )

    # ---------------------------------------------------------------- 1. solution set
    def make_axes(self):
        ax = Axes(x_range=[-2, 6, 1], y_range=[-2, 4, 1], x_length=7.0, y_length=4.4,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([-2.7, 0.6, 0])
        return ax

    def solution_set(self):
        head = self.heading("More unknowns than equations")
        ax = self.make_axes()
        c2p = ax.c2p
        line = Line(c2p(-1, 3), c2p(6, -0.5), color=C_LOSS, stroke_width=4)
        eq = mts([r"X=\begin{bmatrix}1&2\end{bmatrix},\ \ y=5", r"\ \Rightarrow\ w_1+2w_2=5"], 0.6, {1: C_LOSS})
        eq.move_to([4.1, 2.2, 0])
        zero = txt("loss = 0 everywhere on the line", 24, C_LOSS).move_to([4.1, 1.3, 0])
        assert_on_screen(eq, zero, ax)
        self.say("Usually more data than parameters gives one answer. Not here: one equation, two unknowns.",
                 Write(head), Create(ax), Write(eq))
        self.say("Every point on this line fits perfectly, with loss zero. Which one will gradient descent pick?",
                 Create(line), FadeIn(zero))
        rowa = Arrow(c2p(0, 0), c2p(1, 2), buff=0, color=C_STIFF, stroke_width=5, max_tip_length_to_length_ratio=0.2)
        rowt = txt("row of X: (1, 2)", 22, C_STIFF).next_to(c2p(0.5, 1), LEFT, buff=0.15).shift(UP * 0.1)
        nulla = Arrow(c2p(1, 2), c2p(1 + 1.6, 2 - 0.8), buff=0, color=C_SOFT, stroke_width=5, max_tip_length_to_length_ratio=0.2)
        nullt = txt("null direction: (2, −1)", 22, C_SOFT).next_to(c2p(3.2, 1.2), UP, buff=0.35).shift(RIGHT * 0.4)
        ra = RightAngle(Line(c2p(1, 2), c2p(0, 0)), Line(c2p(1, 2), c2p(2, 1.5)), length=0.22, color=WHITE)
        assert_on_screen(rowt, nullt)
        self.say("The row of X is (1, 2). Moving along the null direction, (2, minus 1), changes no prediction.",
                 GrowArrow(rowa), FadeIn(rowt), GrowArrow(nulla), FadeIn(nullt))
        fund = mts([r"\mathbb R^d=", r"\mathrm{Row}(X)", r"\oplus", r"\mathrm{Null}(X)"], 0.75, {1: C_STIFF, 3: C_SOFT}).move_to([4.0, 0.3, 0])
        assert_on_screen(fund)
        self.say("The two are perpendicular and span the whole space: the fundamental theorem of linear algebra.",
                 Create(ra), Write(fund))
        self.hold(0.3)
        self.ax, self.line, self.fund = ax, line, fund
        self.keep = [head, ax, line, rowa, rowt, nulla, nullt, ra, fund]
        self.play(FadeOut(eq), FadeOut(zero))

    # ---------------------------------------------------------------- 2. update stays in the row space
    def row_space_update(self):
        ax = self.ax
        c2p = ax.c2p
        upd = mts([r"w_{t+1}=w_t-2\eta", r"X^\top(Xw_t-y)"], 0.75, {1: C_STIFF}).move_to([3.5, 2.4, 0])
        brace = Brace(upd[1], DOWN, buff=0.1, color=C_STIFF)
        btxt = txt("X transpose times something", 21, C_STIFF).next_to(brace, DOWN, buff=0.1).shift(LEFT * 0.4)
        assert_on_screen(upd, btxt)
        self.say("The gradient step is X transpose times the residual, so every update lies in the row space.",
                 Write(upd), GrowFromCenter(brace), FadeIn(btxt))
        keep_null = mts([r"P_{\mathrm{Null}}\,w_t=P_{\mathrm{Null}}\,w_0\ \ \forall t"], 0.75, {}).move_to([4.0, -0.9, 0])
        assert_on_screen(keep_null)
        self.say("So the null-space part of the starting point is preserved forever; only the row space changes.",
                 Write(keep_null))
        origin = Dot(c2p(0, 0), radius=0.1, color=C_ITER)
        path = path_pts(ax, [tuple(p) for p in P0])
        dots = path_dots(ax, [tuple(p) for p in P0[1:9]])
        self.say("Start at zero: the iterates walk along (1, 2) and stop where they meet the solution line.",
                 FadeIn(origin), Create(path, run_time=2.5, rate_func=linear), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.1, run_time=2.5))
        wm = Dot(c2p(*WMIN), radius=0.13, color=C_TRAIN)
        wmt = mts([r"w_{\min}=X^\top(XX^\top)^{-1}y=\tfrac15(1,2)\cdot5"], 0.6, {}).move_to([4.0, -1.7, 0])
        assert_on_screen(wmt)
        self.say("That is the minimum-norm solution, X transpose (X X transpose) inverse y. Here it is (1, 2).",
                 FadeIn(wm), Write(wmt))
        # Pythagoras
        z5 = Dot(c2p(5, 0), radius=0.1, color=WHITE)
        s1 = Line(c2p(0, 0), c2p(1, 2), color=C_TRAIN, stroke_width=3)
        s2 = Line(c2p(1, 2), c2p(5, 0), color=C_SOFT, stroke_width=3)
        s3 = Line(c2p(0, 0), c2p(5, 0), color=WHITE, stroke_width=3)
        pyth = mts([r"\|w\|^2=", r"\|w_{\min}\|^2", r"+", r"\|z\|^2", r"\ \ \Rightarrow\ 25=5+20"], 0.68, {1: C_TRAIN, 3: C_SOFT}).move_to([3.4, -2.05, 0])
        assert_on_screen(pyth)
        self.say("Why closest? Any other solution is w min plus a perpendicular null vector: at (5, 0), 25 = 5 + 20.",
                 FadeIn(z5), Create(s1), Create(s2), Create(s3), FadeOut(wmt), Write(pyth))
        self.hold(0.4)
        self.play(FadeOut(z5), FadeOut(s1), FadeOut(s2), FadeOut(s3), FadeOut(pyth), FadeOut(upd), FadeOut(brace), FadeOut(btxt))
        self.play(FadeOut(path), FadeOut(dots), FadeOut(origin))
        self.wm = wm
        self.keep_null = keep_null

    # ---------------------------------------------------------------- 3. another start
    def other_start(self):
        ax = self.ax
        c2p = ax.c2p
        st = Dot(c2p(*W0), radius=0.1, color=C_ITER)
        stt = txt("start (3, −2)", 22, C_ITER).next_to(st, LEFT, buff=0.15)
        path = path_pts(ax, [tuple(p) for p in P1])
        dots = path_dots(ax, [tuple(p) for p in P1[1:10]])
        self.say("Start elsewhere, at (3, minus 2). The path is still parallel to (1, 2) but lands on another solution.",
                 FadeIn(st), FadeIn(stt), Create(path, run_time=2.5, rate_func=linear), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.1, run_time=2.5))
        end = Dot(c2p(*WINF), radius=0.13, color=C_ITER)
        endt = txt("lands at (4.2, 0.4)", 22, C_ITER).next_to(end, DOWN, buff=0.2).shift(RIGHT * 0.5)
        frozen = mts([r"P_{\mathrm{Null}}\,w_0=(3.2,\,-1.6)\ \text{stays}"], 0.68, {}).move_to([4.0, -0.9, 0])
        assert_on_screen(endt, frozen)
        self.say("The null part of the start, (3.2, minus 1.6), stayed frozen. The limit is w min plus that part.",
                 FadeIn(end), FadeIn(endt), FadeOut(self.keep_null), Write(frozen))
        gen = mts([r"w_\infty=w_{\min}+P_{\mathrm{Null}}\,w_0"], 0.8, {}).move_to([4.0, -1.8, 0])
        assert_on_screen(gen)
        self.say("So gradient descent finds the solution closest to where it began. Only a zero start gives minimum norm.",
                 Write(gen))
        self.say("Here initialization matters: the loss cannot tell the solutions apart, so the start decides.",
                 Indicate(st, color=C_ITER))
        self.hold(0.6)
        self.clear_stage()

    # ---------------------------------------------------------------- 4. SVD bars
    def svd_bars(self):
        head = self.heading("The same story in the SVD basis")
        eqn = mts([r"X=\begin{bmatrix}1&0&1\\0&1&1\end{bmatrix},\ \ y=(1,2),\ \ w_0=(1,-1,2)"], 0.7, {}).move_to([0, 2.5, 0])
        assert_on_screen(eqn)
        base_y = -0.2
        sc = 0.75
        xs = [-3.6, 0.0, 3.6]
        names = [("v₁·w   σ = 1.73", C_STIFF), ("v₂·w   σ = 1", C_SOFT), ("v₃·w   null direction", GREY_A)]

        def bars(k):
            g = VGroup()
            for i, v in enumerate(COORD[k]):
                h = max(abs(v) * sc, 0.03)
                r = Rectangle(width=1.4, height=h, stroke_width=0, fill_color=names[i][1], fill_opacity=0.85)
                if v >= 0:
                    r.move_to([xs[i], base_y + h / 2, 0])
                else:
                    r.move_to([xs[i], base_y - h / 2, 0])
                lab = txt(f"{v:+.2f}", 24, WHITE)
                lab.next_to(r, UP if v >= 0 else DOWN, buff=0.12)
                g.add(VGroup(r, lab))
            return g

        axis = Line([-6, base_y, 0], [6, base_y, 0], color=GREY_B, stroke_width=2)
        labs = VGroup(*[txt(n, 22, c).move_to([xs[i], -2.2, 0]) for i, (n, c) in enumerate(names)])
        cur = bars(0)
        assert_on_screen(cur, labs)
        self.say("In higher dimensions it is the same. In the SVD basis, each weight coordinate evolves on its own.",
                 Write(head), Write(eqn), Create(axis), FadeIn(labs), FadeIn(cur))
        for k in STAGES[1:]:
            new = bars(k)
            assert_on_screen(new)
            self.play(Transform(cur, new), run_time=0.9)
        self.say("Two coordinates converge to their targets, at rates 0.4 and 0.8. The null coordinate never moves.",
                 Indicate(cur[2][0], color=WHITE))
        self.say("Real networks have far more parameters than data: the optimizer and its start pick the solution.",
                 Indicate(cur[2][1], color=WHITE))
        self.hold(0.6)
        self.clear_stage()
