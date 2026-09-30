"""Episode 1 — Steepest Descent Under a Norm (Lecture 7, first half: linearization, sign SGD, GD)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers

# (a) the local linear picture
def L(t):
    return 0.12 * t ** 4 - 0.6 * t ** 2 + 0.25 * t + 2.2


def dL(t):
    return 0.48 * t ** 3 - 1.2 * t + 0.25


T0 = 2.0
STEP_SMALL, STEP_BIG = -0.15, -1.6
lin = lambda d: L(T0) + dL(T0) * d
GAP_SMALL, GAP_BIG = abs(L(T0 + STEP_SMALL) - lin(STEP_SMALL)), abs(L(T0 + STEP_BIG) - lin(STEP_BIG))
assert GAP_SMALL < 0.15 and GAP_BIG > 10 * GAP_SMALL, (GAP_SMALL, GAP_BIG)

# (b) one SGD step on a least-squares sample
XS, YS, TH = np.array([1.0, 2.0]), 3.0, np.array([0.0, 0.0])
ETA_LS = 0.1
RES = float(XS @ TH - YS)
TH1 = TH - ETA_LS * RES * XS
assert RES == -3.0 and np.allclose(TH1, [0.3, 0.6])
assert np.allclose(np.array([RES * XS[0], RES * XS[1]]), [-3.0, -6.0])   # gradient of 1/2 (x.theta - y)^2

# (c) steepest descent in two parameters
G = np.array([2.0, -0.5])
G1, G2 = float(np.abs(G).sum()), float(np.linalg.norm(G))
D_INF = -np.sign(G)                      # eta = 1
D_TWO = -G / G2
assert np.allclose(D_INF, [-1, 1]) and abs(G @ D_INF + G1) < 1e-12 and abs(G @ D_TWO + G2) < 1e-12
grid = np.linspace(-1, 1, 401)
sq = np.array([[a, b] for a in grid for b in grid if max(abs(a), abs(b)) > 0.999])            # boundary of the square
ang = np.linspace(0, 2 * np.pi, 40001)
ci = np.stack([np.cos(ang), np.sin(ang)], 1)
assert abs((sq @ G).min() + G1) < 1e-9 and abs((ci @ G).min() + G2) < 1e-6      # brute-force check of both solutions
assert abs(G1 - 2.5) < 1e-12 and abs(G2 - np.sqrt(4.25)) < 1e-12
LEN_SIGN = float(np.linalg.norm(D_INF))
assert abs(LEN_SIGN - np.sqrt(2)) < 1e-12
# lagrange view: minimize <g, d> + lam |d|^2  ->  d* = -g / (2 lam)
LAM = 2.0
D_LAM = -G / (2 * LAM)
assert np.allclose(G + 2 * LAM * D_LAM, 0) and np.allclose(D_LAM, [-0.5, 0.125])

# ------------------------------------------------------------------ helpers

SC = 1.35          # screen units per unit of eta in the plane pictures
ORG = np.array([-3.7, 0.3, 0.0])


def P(v):
    """Plane coordinates (in units of eta) -> screen point."""
    return ORG + SC * np.array([v[0], v[1], 0.0])


class Ep01Steepest(NarratedScene):
    series = SERIES

    def construct(self):
        self.title_card()
        self.why()
        self.linearize()
        self.ball()
        self.recipe()
        self.end_card(
            ["Near a point the loss is a line: L plus the gradient times the step",
             "Steepest descent: minimize that line over all steps inside a ball",
             "The infinity-norm ball gives sign SGD; the two-norm ball gives gradient descent",
             "The recipe: choose a norm, choose a step size, get an optimizer"],
        )

    # ---------------------------------------------------------------- 1. why
    def why(self):
        head = self.heading("Why care about optimizers?")
        cards = VGroup(
            box_label("Training time is money", C_LOSS, w=8.6, h=0.75, font_size=28),
            box_label("Default: AdamW with tuned hyperparameters", C_MODEL, w=8.6, h=0.75, font_size=28),
            box_label("A new optimizer needs a new, hard search", C_LAM, w=8.6, h=0.75, font_size=28),
            box_label("Under Adam: lazy training", C_RAMP, w=8.6, h=0.75, font_size=28),
        ).arrange(DOWN, buff=0.3).move_to([0, 0.5, 0])
        assert cards.get_bottom()[1] > -2.5
        self.say("Training a large model costs real money, so we want to train fast.",
                 Write(head), FadeIn(cards[0], shift=UP * 0.2))
        self.say("Today the default is AdamW with carefully tuned hyperparameters.", FadeIn(cards[1], shift=UP * 0.2))
        self.say("A new optimizer needs its own hyperparameter search, and that search is difficult.",
                 FadeIn(cards[2], shift=UP * 0.2))
        # lazy training picture: parameters barely move
        far = Line(LEFT * 2.0, RIGHT * 2.0, color=GREY_B, stroke_width=3)
        far.move_to([0, -2.1, 0])
        self.say("Worse, under Adam we often see lazy training: the model barely moves from its random initialization.",
                 FadeIn(cards[3], shift=UP * 0.2))
        self.hold(0.3)
        self.clear_stage()
        self.say("Initialization rules were a relief. Before them everything was standard normal. Can updates be as principled?")
        self.hold(0.6)

    # ---------------------------------------------------------------- 2. linearize
    def linearize(self):
        head = self.heading("The local linear picture")
        ax = make_axes([-2.5, 2.5, 1], [0, 4, 1], 6.6, 3.5).move_to([-2.6, 0.25, 0])
        curve = plot(ax, L, C_LOSS, width=5)
        lab = txt("loss L(θ)", 26, C_LOSS).next_to(ax.c2p(-2.5, L(-2.5)), UP, buff=0.2).shift(RIGHT * 0.6)
        xl = txt("θ", 26, GREY_B).next_to(ax.x_axis.get_end(), DOWN, buff=0.15)
        dot0 = Dot(ax.c2p(T0, L(T0)), color=WHITE, radius=0.09)
        eq0 = mts([r"\mathcal L(\vec\theta+\Delta\vec\theta)", r"\approx", r"\mathcal L(\vec\theta)",
                   r"+", r"\Big\langle\nabla_{\theta}\mathcal L,\ \Delta\vec\theta\Big\rangle"], 0.72,
                  {4: C_GRAD})
        eq0.move_to([3.2, 1.9, 0])
        assert eq0.get_right()[0] < 7.0 and eq0.get_left()[0] > -0.6, eq0.get_center()
        self.say("Write theta for all the parameters and L for the average loss over the data.",
                 Write(head), Create(ax), Create(curve), FadeIn(lab), FadeIn(xl), FadeIn(dot0))
        tan = ax.plot(lambda t: lin(t - T0), x_range=[0.6, 2.5], color=C_STEP, stroke_width=4, use_smoothing=False)
        self.say("Near the current point, the loss looks like a line: its value plus the gradient times the step.",
                 Create(tan), Write(eq0))

        def gap_group(step):
            x1 = T0 + step
            a = Dot(ax.c2p(x1, L(x1)), color=C_LOSS, radius=0.08)
            b = Dot(ax.c2p(x1, lin(step)), color=C_STEP, radius=0.08)
            seg = Line(a.get_center(), b.get_center(), color=WHITE, stroke_width=3)
            return VGroup(seg, a, b)

        g1 = gap_group(STEP_SMALL)
        info1 = VGroup(txt(f"step {STEP_SMALL}", 26, C_STEP),
                       txt(f"line says {lin(STEP_SMALL):.2f}", 24, C_STEP),
                       txt(f"loss is {L(T0 + STEP_SMALL):.2f}", 24, C_LOSS)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.2, 0.0, 0])
        self.say("For a small step, the line is accurate.", FadeIn(g1), FadeIn(info1))
        g2 = gap_group(STEP_BIG)
        info2 = VGroup(txt(f"step {STEP_BIG}", 26, C_STEP),
                       txt(f"line says {lin(STEP_BIG):.2f}", 24, C_STEP),
                       txt(f"loss is {L(T0 + STEP_BIG):.2f}", 24, C_LOSS)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(info1)
        self.say("For a big step, the line lies to us: it promises a much lower loss than we get.",
                 Transform(g1, g2), Transform(info1, info2))
        self.say("So a step must be small enough for the approximation to hold, yet large enough to converge fast.")
        self.hold(0.4)
        self.clear_stage()
        # least squares SGD
        head = self.heading("The step we already know")
        ls = mts([r"\ell=\tfrac12(\vec x^{\top}\vec\theta-y)^2", r"\quad\Rightarrow\quad",
                  r"\nabla_\theta\ell=(\vec x^{\top}\vec\theta-y)\,\vec x"], 0.78, {2: C_GRAD})
        ls.move_to([0, 2.3, 0])
        upd = mts([r"\vec\theta_{t+1}=\vec\theta_t-", r"\eta", r"(\vec x^{\top}\vec\theta_t-y)\,\vec x"], 0.85, {1: C_LAM})
        upd.move_to([0, 1.2, 0])
        self.say("For least squares on one sample, the gradient is the residual times the input.",
                 Write(head), Write(ls))
        self.say("SGD steps against it, scaled by the learning rate eta.", Write(upd))
        num = VGroup(txt("x = (1, 2),  y = 3,  θ = (0, 0),  η = 0.1", 28, C_TEXT),
                     txt(f"residual = 0 − 3 = {RES:g}", 28, C_LOSS),
                     txt(f"θ becomes (0, 0) − 0.1 · ({RES:g}) · (1, 2) = ({TH1[0]:g}, {TH1[1]:g})", 28, C_STEP)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, -0.7, 0])
        assert num.width < 13 and num.get_bottom()[1] > -2.5
        self.say("With these numbers the residual is minus three, and one step moves theta to zero point three, zero point six.",
                 LaggedStart(*[FadeIn(n, shift=UP * 0.15) for n in num], lag_ratio=0.4))
        self.say("But why this direction and this length? Let's derive a step instead of guessing one.")
        self.hold(0.3)
        self.clear_stage()

    # ---------------------------------------------------------------- 3. the ball
    def ball(self):
        head = self.heading("Steepest descent inside a ball")
        obj = mts([r"\arg\min_{\|\Delta\vec\theta\|\le\eta}\Big(\mathcal L(\vec\theta)+\big\langle\nabla_\theta\mathcal L,\Delta\vec\theta\big\rangle\Big)"], 0.7)
        obj.move_to([2.6, 2.75, 0])
        assert obj.get_right()[0] < 7.0
        obj2 = mts([r"=\ \arg\min_{\|\Delta\vec\theta\|\le\eta}", r"\big\langle\nabla_\theta\mathcal L,\Delta\vec\theta\big\rangle"], 0.7, {1: C_GRAD})
        obj2.next_to(obj, DOWN, buff=0.15).align_to(obj, LEFT)
        self.say("Ask directly: among all steps of size at most eta, which lowers the linearized loss the most?",
                 Write(head), Write(obj))
        self.say("The loss value itself is a constant, so only the inner product with the gradient matters.",
                 Write(obj2))
        # plane
        axx = Line(P([-1.9, 0]), P([1.9, 0]), color=GREY_D, stroke_width=2)
        axy = Line(P([0, -1.7]), P([0, 1.9]), color=GREY_D, stroke_width=2)
        assert P([-1.9, 0])[0] > -6.6 and P([0, -1.7])[1] > -2.5
        gvec = Arrow(P([0, 0]), P(0.55 * G), buff=0, color=C_GRAD, stroke_width=6, max_tip_length_to_length_ratio=0.3)
        glab = txt("g", 28, C_GRAD).next_to(gvec.get_end(), DOWN, buff=0.08)
        square = Square(2 * SC, stroke_color=C_STEP, stroke_width=4, fill_color=C_STEP, fill_opacity=0.12).move_to(P([0, 0]))
        sqlab = txt("‖Δθ‖∞ ≤ η", 26, C_STEP).next_to(square, DOWN, buff=0.15)
        self.say("Take two parameters, gradient g = (2, −0.5). Choice one: change each by at most eta: a square.",
                 Create(axx), Create(axy), GrowArrow(gvec), FadeIn(glab), FadeIn(square), FadeIn(sqlab))
        # sweeping line of constant inner product
        gh = G / G2
        perp = np.array([-gh[1], gh[0]])
        cval = ValueTracker(3.0)

        def sweep_line():
            c = cval.get_value()
            pt = c * G / (G @ G)
            a, b = P(pt + 1.55 * perp), P(pt - 1.55 * perp)
            return Line(a, b, color=WHITE, stroke_width=3)

        sw = always_redraw(sweep_line)
        readout = always_redraw(lambda: txt(f"⟨g, Δ⟩ = {cval.get_value():+.2f} η", 30, WHITE).move_to([3.4, -1.4, 0]))
        self.say("Slide a line of constant inner product against the gradient, and stop when it is about to leave the square.",
                 FadeIn(sw), FadeIn(readout))
        self.play(cval.animate.set_value(-G1), run_time=3.2, rate_func=smooth)
        corner = Dot(P(D_INF), color=C_STEP, radius=0.11)
        self.remove(glab)
        self.say("It leaves through a corner: every coordinate moves by eta, against the sign of its gradient.",
                 FadeIn(corner), Flash(P(D_INF), color=C_STEP, flash_radius=0.4))
        sign_eq = mts([r"\Delta\vec\theta^{*}=-\eta\,\mathrm{sgn}\big(\nabla_\theta\mathcal L\big)"], 0.8, )
        sign_eq.move_to([3.4, 1.0, 0])
        sgn = txt("sign SGD", 34, C_STEP).next_to(sign_eq, DOWN, buff=0.25)
        assert sign_eq.get_right()[0] < 7.0
        self.say("That step is minus eta times the sign of the gradient. It is called sign SGD.", Write(sign_eq), FadeIn(sgn))
        self.say(f"Predicted change: minus two plus minus a half, that is minus {G1:g} eta.",
                 Indicate(readout, color=C_STEP))
        self.hold(0.3)
        # circle
        circle = Circle(radius=SC, stroke_color=C_STEP, stroke_width=4, fill_color=C_STEP, fill_opacity=0.12).move_to(P([0, 0]))
        circlab = txt("‖Δθ‖₂ ≤ η", 26, C_STEP).move_to(sqlab)
        sign_group = VGroup(sign_eq, sgn)
        self.say("Choice two: bound the ordinary length instead. Now the allowed set is a circle.",
                 Transform(square, circle), Transform(sqlab, circlab), FadeOut(corner), FadeOut(sign_group),
                 cval.animate.set_value(3.0), run_time=1.0)
        tip = Dot(P(D_TWO), color=C_STEP, radius=0.11)
        self.say("The line now last touches the circle where the step points straight against the gradient.",
                 cval.animate.set_value(-G2))
        self.play(FadeIn(tip), Flash(P(D_TWO), color=C_STEP, flash_radius=0.4))
        cs = mts([r"\vec x^{\top}\vec y=\|\vec x\|_2\|\vec y\|_2\cos\phi"], 0.75).move_to([3.4, 0.95, 0])
        cs.set_x(min(cs.get_x(), 7.0 - cs.width / 2 - 0.1))
        d2 = mts([r"\Delta\vec\theta^{*}=-\eta\,\dfrac{\nabla_\theta\mathcal L}{\|\nabla_\theta\mathcal L\|_2}"], 0.8).move_to([3.4, -0.15, 0])
        assert d2.get_right()[0] < 7.0 and cs.get_right()[0] < 7.0
        self.say("Cauchy-Schwarz: an inner product is largest in size when the vectors are aligned. So the step is minus eta times the unit-length gradient.",
                 Write(cs), Write(d2))
        self.say(f"That is gradient descent with a normalized step. Predicted change: minus {G2:.2f} eta, a bit less than the sign step.",
                 FadeOut(cs))
        self.hold(0.3)
        self.clear_stage()
        # lagrange
        head = self.heading("The penalty view")
        gd = mts([r"g(\Delta\vec\theta)=\big\langle\nabla_\theta\mathcal L,\Delta\vec\theta\big\rangle+", r"\lambda", r"\|\Delta\vec\theta\|_2^2"], 0.8, {1: C_LAM})
        gd.move_to([0, 2.1, 0])
        cvx = txt("convex, and unconstrained", 28, GREY_B).next_to(gd, DOWN, buff=0.3)
        self.say("A cousin of this idea: instead of a hard bound, penalize the step with lambda times its squared length.",
                 Write(head), Write(gd), FadeIn(cvx))
        st = mts([r"\nabla g=\nabla_\theta\mathcal L+2", r"\lambda", r"\Delta\vec\theta=0"], 0.8, {1: C_LAM})
        st.move_to([0, 0.6, 0])
        ans = mts([r"\Delta\vec\theta^{*}=-", r"\dfrac{1}{2\lambda}", r"\nabla_\theta\mathcal L"], 0.9, {1: C_LAM, 2: C_GRAD})
        ans.move_to([0, -0.7, 0])
        self.say("Set its gradient to zero and solve.", Write(st))
        self.say("The minimizer is minus one over two lambda times the gradient. That is plain gradient descent.",
                 Write(ans))
        ex = txt(f"λ = {LAM:g}: step = −g / 4 = ({D_LAM[0]:g}, {D_LAM[1]:g})", 28, C_TEXT).move_to([0, -1.8, 0])
        self.say("Its learning rate is one over two lambda, so sweeping lambda sweeps out the same solutions as eta.", FadeIn(ex))
        self.hold(0.4)
        self.clear_stage()
        # aha: lengths
        head = self.heading("Same eta, different meaning")
        ax0 = Line(P([-1.6, 0]), P([1.9, 0]), color=GREY_D, stroke_width=2).shift(RIGHT * 4.6)
        ay0 = Line(P([0, -1.7]), P([0, 1.9]), color=GREY_D, stroke_width=2).shift(RIGHT * 4.6)
        org2 = P([0, 0]) + RIGHT * 4.6
        circ = Circle(radius=SC, stroke_color=C_STEP, stroke_width=3, fill_color=C_STEP, fill_opacity=0.1).move_to(org2)
        sqr = Square(2 * SC, stroke_color=C_STEP, stroke_width=3).move_to(org2)
        a_sign = Arrow(org2, org2 + SC * np.array([D_INF[0], D_INF[1], 0]), buff=0, color=C_STEP, stroke_width=5, max_tip_length_to_length_ratio=0.2)
        a_gd = Arrow(org2, org2 + SC * np.array([D_TWO[0], D_TWO[1], 0]), buff=0, color=C_GRAD, stroke_width=5, max_tip_length_to_length_ratio=0.25)
        txts = VGroup(txt("sign step: length √2 η", 30, C_STEP),
                      txt("gradient step: length η", 30, C_GRAD),
                      txt("in d dimensions: √d η", 30, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.6, 0.5, 0])
        assert txts.get_left()[0] > -6.8 and txts.get_right()[0] < org2[0] - 1.6, (txts.get_left(), txts.get_right())
        self.say(f"Notice the sign step is longer: its corner sits at root two, about {LEN_SIGN:.2f}, times eta.",
                 Write(head), Create(ax0), Create(ay0), FadeIn(circ), Create(sqr), GrowArrow(a_gd), GrowArrow(a_sign),
                 FadeIn(txts[:2]))
        self.say("With d parameters it is root d times eta. Same eta, different norm, different meaning of small.",
                 FadeIn(txts[2]))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 4. recipe
    def recipe(self):
        head = self.heading("A recipe for optimizers")
        b1 = box_label("choose a norm", C_STEP, w=3.4, h=0.9, font_size=28)
        b2 = box_label("choose a step size η", C_LAM, w=3.9, h=0.9, font_size=28)
        b3 = box_label("optimizer", C_MODEL, w=3.0, h=0.9, font_size=28)
        row = VGroup(b1, b2, b3).arrange(RIGHT, buff=1.0).move_to([0, 1.7, 0])
        a1 = Arrow(b1.get_right(), b2.get_left(), buff=0.05, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        a2 = Arrow(b2.get_right(), b3.get_left(), buff=0.05, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        assert row.width < 13.2
        self.say("This is the recipe of Bernstein and Newhouse, 2024: choose a norm, choose a step size, and an optimizer falls out.",
                 Write(head), FadeIn(b1, shift=UP * 0.2), FadeIn(b2, shift=UP * 0.2), Create(a1), Create(a2), FadeIn(b3, shift=UP * 0.2))
        tab = VGroup(
            VGroup(txt("infinity norm", 28, C_STEP), txt("→", 28, GREY_B), txt("sign SGD", 28, WHITE)),
            VGroup(txt("two norm", 28, C_STEP), txt("→", 28, GREY_B), txt("gradient descent", 28, WHITE)),
            VGroup(txt("spectral norm", 28, C_STEP), txt("→", 28, GREY_B), txt("next episode", 28, C_SV)),
        )
        for r in tab:
            r.arrange(RIGHT, buff=0.35)
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -0.4, 0])
        assert tab.get_bottom()[1] > -2.5
        self.say("The infinity norm gives sign SGD, the two norm gives gradient descent, and the spectral norm is coming up.",
                 LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in tab], lag_ratio=0.5))
        self.say("The right norm may depend on the geometry and architecture of the network. That is where we go next.",
                 Indicate(b1, color=C_STEP))
        self.hold(0.5)
