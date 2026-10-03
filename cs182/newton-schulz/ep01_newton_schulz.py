"""Newton–Schulz iteration, EECS 182 Fall 2026 Discussion 5, focused on part (e):
why the iteration turns an ellipse into a circle, and where a singular value that
starts at +σ ends up. The story builds from easy starts to √3, √5 and the basins.

Every number on screen is computed below; the key ones are asserted.
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---------------------------------------------------------------- the math


def p(x):
    return 1.5 * x - 0.5 * x ** 3


def dp(x):
    return 1.5 - 1.5 * x ** 2


S3, S5 = math.sqrt(3), math.sqrt(5)


def _next_b(prev):
    """The unique b in (√3, √5) with p(b) = −prev, i.e. b³ − 3b = 2·prev."""
    lo, hi = S3, S5
    for _ in range(200):
        m = (lo + hi) / 2
        if m ** 3 - 3 * m < 2 * prev:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


B = [S3]
for _ in range(14):
    B.append(_next_b(B[-1]))


def orbit(x, n):
    out = [x]
    for _ in range(n):
        x = p(x)
        out.append(x)
    return out


def fate(x, n=400):
    """(limit, number of sign flips) of the orbit of x."""
    flips = 0
    for _ in range(n):
        y = p(x)
        if abs(y) > 1e6:
            return "diverges", flips
        flips += y * x < 0
        x = y
    return round(x, 9), flips


def _root(c, lo, hi):
    """x in [lo, hi] with p(x) = c, p decreasing there."""
    for _ in range(200):
        m = (lo + hi) / 2
        if p(m) > c:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


# fixed points and their slopes
assert p(0) == 0 and p(1) == 1 and p(-1) == -1
assert dp(0) == 1.5 and dp(1) == 0 and dp(-1) == 0
# the two thresholds
assert abs(p(S3)) < 1e-12 and abs(p(-S3)) < 1e-12
assert abs(p(S5) + S5) < 1e-12 and abs(p(-S5) - S5) < 1e-12
assert abs(dp(S5) + 6) < 1e-12
# the boundary points (values from the brief)
for b, want in zip(B[1:4], (2.14776346, 2.22122772, 2.23359117)):
    assert abs(b - want) < 1e-8, (b, want)
for k in range(1, 12):
    assert abs(p(B[k]) + B[k - 1]) < 1e-12 and B[k - 1] < B[k] < S5
# √5 − b_n shrinks by ~6 each time
assert abs((S5 - B[6]) / (S5 - B[7]) - 6) < 0.01
# the three neighbours of the opening
assert fate(2.0) == (-1.0, 1) and fate(2.2) == (1.0, 2) and fate(2.23) == (-1.0, 3)
assert p(2.0) == -1.0
# every point of (b_{n-1}, b_n) flips exactly n times and ends at (−1)^n
for n in range(1, 7):
    for s in (0.1, 0.5, 0.9):
        x = B[n - 1] + s * (B[n] - B[n - 1])
        assert fate(x) == ((-1.0) ** n, n), (n, s, fate(x))
assert fate(1.6) == (1.0, 0) and fate(0.3) == (1.0, 0) and fate(0.05) == (1.0, 0)
assert fate(2.3)[0] == "diverges"
# the easy starts, and the first ones that go wrong
assert fate(0.5)[0] == 1.0 and fate(1.3)[0] == 1.0 and fate(0.1)[0] == 1.0 and fate(1.5) == (1.0, 0)
assert fate(1.8) == (-1.0, 1) and fate(3.0)[0] == "diverges"

# ---------------------------------------------------------------- colors (one per concept)

C_P = BLUE_C        # the curve y = p(x)
C_DIAG = GREY_B     # y = x
C_PLUS = TEAL_C     # positive values, fate +1
C_MINUS = GOLD_C    # negative values, fate −1
C_ZERO = PURPLE_B   # √3, 0 and the boundary points that fall into it
C_S5 = RED_C        # √5 and divergence
C_SIG = YELLOW_D    # Σ, singular values

PANEL_X = 3.65      # centre of the right-hand panel next to the graph


def sign_color(x):
    return C_PLUS if x > 0 else C_MINUS


def num(v, d=2):
    """A number for MathTex, with a real minus sign."""
    return f"{v:.{d}f}"


def mt(s, size=36, color=C_TEXT):
    return MathTex(s, font_size=size, color=color)


def neg(s):
    return s.replace("-", "−")


class Ep01NewtonSchulz(NarratedScene):
    # Latin captions: Pango wraps a single over-long line on its own (and the
    # wrapped lines overlap), so keep each caption line short
    caption_units = 30

    SCENES = ["ellipse", "why_orthogonal", "why_p", "try_numbers", "cobweb", "slopes", "how_big",
              "too_big", "the_gap", "first_boundary", "basins", "boundary_points", "summary",
              "back_to_matrix"]

    def construct(self):
        # KIT_ONLY=the_gap,basins renders just those scenes (see preview.py): no title or end
        # card, and the corner formula that why_p normally leaves behind is put up directly
        only = [s for s in os.environ.get("KIT_ONLY", "").split(",") if s]
        if only:
            assert all(s in self.SCENES for s in only), only
            if self.SCENES.index(only[0]) > self.SCENES.index("why_p"):
                self.corner = MathTex(r"p(x)=\tfrac32x-\tfrac12x^3", font_size=34).to_corner(UR, buff=0.35)
                self.corner[0][5:].set_color(C_P)
                self.add(self.corner)
            # slopes, how_big and too_big keep drawing on the graph that cobweb put up
            chain = self.SCENES[self.SCENES.index("cobweb"):self.SCENES.index("too_big") + 1]
            if only[0] in chain[1:]:
                self.fast_forward(*[getattr(self, s) for s in chain[:chain.index(only[0])]])
            for s in only:
                getattr(self, s)()
            self.uncaption()
            return
        self.title_card()
        for s in self.SCENES:
            getattr(self, s)()
        self.end_card([
            "Newton–Schulz only changes the singular values: each σ follows p on its own",
            "Fixed points −1, 0, 1: ±1 attract (slope 0), 0 repels (slope 1.5)",
            "Below √3 the sign never flips, so σ goes to +1",
            "√5 decides shrink or grow: √5 bounces, anything bigger diverges",
            "Between √3 and √5 the number of flips picks −1 or +1, in alternating basins",
            "So scale W first, so every singular value is below √3",
        ])

    # ------------------------------------------------------------ helpers
    def number_row(self, y, lo=-2.5, hi=2.5, length=10.2, x=0.7, marks=(-2, -1, 0, 1, 2)):
        nl = NumberLine(x_range=[lo, hi, 0.5], length=length, color=GREY_B, stroke_width=2,
                        tick_size=0.05, include_tip=False)
        nl.move_to([x, y, 0])
        labels = VGroup(*[
            mono(neg(str(v)), 18, GREY_B).next_to(nl.n2p(v), DOWN, buff=0.14) for v in marks
        ])
        return VGroup(nl, labels)

    def hop(self, dot, line, x_old, x_new, color=None):
        a = 0.55 * PI if x_new < x_old else -0.55 * PI
        anim = dot.animate(path_arc=a).move_to(line.n2p(x_new))
        return anim.set_color(color or sign_color(x_new))

    def make_graph(self):
        ax = Axes(x_range=[-2.5, 2.5, 0.5], y_range=[-2.5, 2.5, 0.5], x_length=5.4, y_length=5.4,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2,
                               "tick_size": 0.04})
        ax.move_to([-3.45, 0.3, 0])
        nums = VGroup()
        for v in (-2, -1, 1, 2):
            nums.add(mono(neg(str(v)), 18, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.12))
            nums.add(mono(neg(str(v)), 18, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12))
        xc = _root(-2.5, 1.0, 2.5)
        curve = ax.plot(p, x_range=[-xc, xc], color=C_P, stroke_width=4)
        diag = ax.plot(lambda x: x, x_range=[-2.5, 2.5], color=C_DIAG, stroke_width=2.5)
        lab_p = mt("y=p(x)", 32, C_P).move_to(ax.c2p(-1.1, 1.55))
        lab_d = mt("y=x", 32, C_DIAG).move_to(ax.c2p(2.15, 1.45))
        self.ax, self.curve, self.diag = ax, curve, diag
        self.graph_group = VGroup(ax, nums, curve, diag, lab_p, lab_d)
        return self.graph_group

    def web(self, x0, n, color, width=3.0, f=p):
        ax = self.ax
        pts = [ax.c2p(x0, 0)]
        x = x0
        for _ in range(n):
            y = f(x)
            if abs(y) > 2.45:
                break
            pts += [ax.c2p(x, y), ax.c2p(y, y)]
            x = y
        segs = VGroup()
        for a, b in zip(pts, pts[1:]):
            if np.linalg.norm(b - a) > 0.012:
                segs.add(Line(a, b, color=color, stroke_width=width))
        return segs

    def draw(self, segs, per=0.35):
        return Succession(*[Create(s, rate_func=linear) for s in segs], run_time=per * len(segs))

    def start_mark(self, x0, color, label=None):
        d = Dot(self.ax.c2p(x0, 0), radius=0.06, color=color)
        side = UP if p(x0) < 0 else DOWN   # keep clear of a curve that dips below the axis
        lab = mt(label or num(x0, 1), 26, color).next_to(d, side, buff=0.7)
        return VGroup(d, lab)

    def panel(self, *mobs, y=2.4, buff=0.35):
        g = VGroup(*mobs).arrange(DOWN, buff=buff)
        g.move_to([PANEL_X, 0, 0]).set_y(y - g.height / 2)
        return g

    # ------------------------------------------------------------ 1. why anyone iterates this
    def ellipse(self):
        R, th = 1.45, 30 * DEGREES
        C0 = np.array([-3.3, 0.15, 0])
        u1 = np.array([np.cos(th), np.sin(th), 0])
        u2 = np.array([-np.sin(th), np.cos(th), 0])
        circ = Circle(radius=R, color=GREY_B, stroke_width=3).move_to(C0)
        wlab = mt(r"W", 40).next_to(circ, UP, buff=0.25)
        self.say("Take a matrix W. It turns the unit circle into an ellipse.", Create(circ), FadeIn(wlab))

        # the SVD as three moves: rotate, stretch along the axes, rotate
        def arm(v, c):
            return Line(C0, C0 + R * v, color=c, stroke_width=5)

        phi = 75 * DEGREES
        v1 = np.array([np.cos(phi), np.sin(phi), 0])
        v2 = np.array([-np.sin(phi), np.cos(phi), 0])
        demo = VGroup(Circle(radius=R, color=C_SIG, stroke_width=4).move_to(C0),
                      arm(v1, C_PLUS), arm(v2, C_MINUS))
        svd = MathTex(r"W", r"=", r"U", r"\,\Sigma\,", r"V^{\top}", font_size=48).move_to([PANEL_X, 1.4, 0])
        steps = VGroup(txt("1. rotate", 26, GREY_A), txt("2. stretch the axes", 26, C_SIG),
                       txt("3. rotate again", 26, GREY_A)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        steps.next_to(svd, DOWN, buff=0.5)
        self.say("How? Every matrix does it in three moves. Follow two perpendicular arms on the circle.",
                 FadeIn(demo), Write(svd))
        self.say("First, a rotation turns the arms onto the axes. That is V transpose.",
                 Rotate(demo, -phi, about_point=C0), FadeIn(steps[0]), Indicate(svd[4]), run_time=2.0)
        self.say("Next, Σ stretches each axis by its own amount, here 1.3 and 0.5. The circle becomes an ellipse.",
                 demo.animate.apply_matrix(np.diag([1.3, 0.5, 1]), about_point=C0), FadeIn(steps[1]),
                 Indicate(svd[3], color=C_SIG), run_time=2.0)
        self.say("Finally U rotates the ellipse into place. Rotations never change lengths, "
                 "so all the stretching lives in Σ.",
                 Rotate(demo, th, about_point=C0), FadeIn(steps[2]), Indicate(svd[2]), run_time=2.0)
        self.hold()

        s1, s2 = ValueTracker(1.3), ValueTracker(0.5)

        def shape():
            a, b = s1.get_value(), s2.get_value()
            e = Ellipse(width=2 * R * a, height=2 * R * b, color=C_SIG, stroke_width=4)
            e.rotate(th).move_to(C0)
            l1 = Line(C0, C0 + R * a * u1, color=C_SIG, stroke_width=4)
            l2 = Line(C0, C0 + R * b * u2, color=C_SIG, stroke_width=4)
            t1 = mt(r"\sigma_1", 30, C_SIG).move_to(C0 + R * a * u1 * 0.55 - 0.3 * u2)
            t2 = mt(r"\sigma_2", 30, C_SIG).move_to(C0 + R * b * u2 * 0.55 + 0.3 * u1)
            return VGroup(e, l1, l2, t1, t2)

        ell = always_redraw(shape)
        self.play(circ.animate.set_stroke(opacity=0.35), FadeOut(demo), FadeIn(ell), FadeOut(steps),
                  FadeOut(svd), run_time=0.8)
        self.say("The two stretch factors, σ1 and σ2, are the half-axes of the ellipse: W's singular values.",
                 Indicate(ell[3], color=C_SIG), Indicate(ell[4], color=C_SIG))

        def readout(tr, name):
            d = DecimalNumber(tr.get_value(), num_decimal_places=3, font_size=36, color=C_SIG)
            d.add_updater(lambda m: m.set_value(tr.get_value()))
            return VGroup(mt(name + "=", 36, C_SIG), d).arrange(RIGHT, buff=0.15)

        r1, r2 = readout(s1, r"\sigma_1"), readout(s2, r"\sigma_2")
        rd = VGroup(r1, r2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([PANEL_X, 0.1, 0])
        self.play(FadeIn(rd))
        ortho = txt("all σ = 1  ⇔  W is orthogonal", 28, C_PLUS).move_to([PANEL_X, -1.3, 0])
        self.say("If every stretch were exactly 1, only the rotations would remain: W would be orthogonal.",
                 FadeIn(ortho))
        self.hold()
        self.hold(1.0)
        ell.clear_updaters()
        for d in (r1[1], r2[1]):
            d.clear_updaters()
        self.clear_stage()

    # ------------------------------------------------------------ 2. why each direction should not blow up
    def why_orthogonal(self):
        R, th = 1.45, 30 * DEGREES
        C0 = np.array([-3.35, 0.15, 0])
        u1 = np.array([np.cos(th), np.sin(th), 0])
        u2 = np.array([-np.sin(th), np.cos(th), 0])

        circ = Circle(radius=R, color=GREY_B, stroke_width=3).move_to(C0)
        axes = VGroup(Line(C0 - 1.1 * R * u1, C0 + 1.1 * R * u1, color=C_SIG, stroke_width=3),
                      Line(C0 - 1.1 * R * u2, C0 + 1.1 * R * u2, color=C_SIG, stroke_width=3))
        self.say("The singular value decomposition lets us watch the stretching along each "
                 "natural direction of the matrix, one direction at a time.",
                 FadeIn(circ), FadeIn(axes))

        arm1 = Line(C0, C0 + R * u1, color=C_PLUS, stroke_width=5)
        arm2 = Line(C0, C0 + R * u2, color=C_MINUS, stroke_width=5)
        avg = txt("one average number", 26, GREY_A).move_to([PANEL_X, 0.9, 0])
        self.say("In class we worried about one thing, that the overall scale of the "
                 "gradients does not explode. That is the idea behind Xavier initialization.",
                 FadeIn(arm1), FadeIn(arm2), FadeIn(avg))

        self.say("But that is a single number, a rough average over the whole matrix. "
                 "It says little about any one direction.",
                 Indicate(avg, color=C_MINUS, scale_factor=1.15))

        big = Line(C0, C0 + 1.65 * R * u1, color=C_PLUS, stroke_width=6)
        small = Line(C0, C0 + 0.35 * R * u2, color=C_MINUS, stroke_width=6)
        lab_big = txt("too far", 26, C_PLUS).move_to(C0 + 1.9 * R * u1)
        lab_small = txt("to nothing", 26, C_MINUS).move_to(C0 + 0.15 * R * u2)
        self.say("Xavier does not solve every problem. The average can be fine while one "
                 "direction still stretches too far and another gets squeezed to nothing.",
                 Transform(arm1, big), Transform(arm2, small), FadeIn(lab_big), FadeIn(lab_small))

        back1 = Line(C0, C0 + R * u1, color=C_PLUS, stroke_width=5)
        back2 = Line(C0, C0 + R * u2, color=C_MINUS, stroke_width=5)
        self.say("We want every direction to keep its size, so none gets stretched too far "
                 "and none gets squeezed away.",
                 Transform(big, back1), Transform(small, back2), FadeOut(lab_big), FadeOut(lab_small))

        ortho = txt("every stretch one", 28, C_PLUS).move_to([PANEL_X, 0.9, 0])
        self.say("That is why Muon asks for an orthogonal update, one where every singular "
                 "value is exactly one. Nothing grows, nothing vanishes.",
                 ReplacementTransform(avg, ortho), FadeIn(Circle(radius=R, color=C_PLUS,
                                                                 stroke_width=3).move_to(C0)))

        self.say("Every direction moves together, and the matrix stays healthy step after step.",
                 Indicate(ortho, color=C_PLUS, scale_factor=1.15))
        self.hold(0.5)
        self.clear_stage()

    # ------------------------------------------------------------ 3. one matrix step = p on each σ
    def why_p(self):
        # 01-02: the target U Vᵀ, and the one cheap tool
        svd = MathTex(r"W", r"=", r"U", r"\,\Sigma\,", r"V^{\top}", font_size=56).move_to([0, 1.7, 0])
        svd[3].set_color(C_SIG)
        tgt = MathTex(r"U", r"\,I\,", r"V^{\top}", r"=", r"U", r"V^{\top}", font_size=56).move_to([0, 0.3, 0])
        tgt[1].set_color(C_SIG)
        tgt[4:].set_color(C_PLUS)
        slow = txt("but computing the SVD is slow on a GPU", 28, C_S5).move_to([0, -1.2, 0])
        self.say("We want every singular value to be one. The SVD hands us exactly that. Write W as U, sigma, "
                 "V transpose, keep the two rotations, and replace every stretch in sigma with one. What "
                 "remains is just U times V transpose. But computing an SVD is a long procedure, and it runs "
                 "slowly on a GPU.", Write(svd))
        self.cue("replace every stretch in sigma with one", TransformFromCopy(svd[2:], tgt[:3]))
        self.cue("What remains is", FadeIn(tgt[3:]))
        self.cue("But computing an SVD", FadeIn(slow))
        self.hold()
        goal = VGroup(txt("goal:", 26, GREY_A), MathTex(r"UV^{\top}", font_size=40, color=C_PLUS))
        goal.arrange(RIGHT, buff=0.2).to_corner(UL, buff=0.45)
        cheap = txt("cheap: matrix products", 30, C_PLUS).move_to([0, 0.3, 0])
        self.say("So we want that same result, U times V transpose, without ever computing the SVD. What can a"
                 " GPU do cheaply? It can multiply matrices. That is the one thing it is built for.", FadeOut(svd), FadeOut(tgt), FadeOut(slow), FadeIn(goal))
        self.cue("It can multiply matrices", FadeIn(cheap))
        self.hold()

        # 03: W·W does not fit, Wᵀ W does
        a1 = MathTex(r"W", r"\,W", font_size=56).move_to([-2.6, 1.2, 0])
        sh1 = mt(r"(3\times2)\ (3\times2)", 32, GREY_A).next_to(a1, DOWN, buff=0.35)
        x1 = Cross(VGroup(a1, sh1), stroke_color=C_S5, stroke_width=5)
        a2 = MathTex(r"W^{\top}", r"W", font_size=56).move_to([2.6, 1.2, 0])
        sh2 = mt(r"(2\times3)\ (3\times2)", 32, C_PLUS).next_to(a2, DOWN, buff=0.35)
        self.say("So let's start multiplying. The only matrix we have is W, so the first thing to try is W "
                 "times W. But two matrices can only be multiplied when the number of columns of the first "
                 "matches the number of rows of the second. If W has three rows and two columns, W times W "
                 "does not fit. The transpose swaps rows and columns. So W transpose times W always fits. "
                 "Let's see what that product gives.", cheap.animate.scale(0.8).next_to(goal, DOWN, buff=0.2, aligned_edge=LEFT))
        self.cue("the first thing to try", FadeIn(a1))
        self.cue("If W has three rows", FadeIn(sh1))
        self.cue("W times W does not fit", Create(x1))
        self.cue("The transpose swaps", FadeIn(a2), FadeIn(sh2))
        self.hold()

        # 04: Wᵀ W = V Σ² Vᵀ: U is lost
        def cancel(piece):
            br = Brace(piece, DOWN, color=GREY_B, buff=0.08)
            return VGroup(br, mt("I", 32, GREY_B).next_to(br, DOWN, buff=0.08))

        e1 = mt(r"W=U\,\Sigma\,V^{\top}", 44).move_to([-3.0, 2.0, 0])
        e2 = mt(r"W^{\top}=V\,\Sigma\,U^{\top}", 44).move_to([3.0, 2.0, 0])
        prod = MathTex(r"W^{\top}W", r"=", r"V\,\Sigma\,", r"U^{\top}U", r"\,\Sigma\,V^{\top}", font_size=52)
        prod.move_to([0, 0.6, 0])
        c4 = cancel(prod[3])
        res = MathTex(r"=", r"V\,\Sigma^2\,V^{\top}", font_size=52)
        res.shift(prod[1].get_center() + DOWN * 1.9 - res[0].get_center())
        bad = txt("U has disappeared", 28, C_S5).next_to(res, RIGHT, buff=0.6)
        self.say("To see it, write W with its SVD, as U, sigma, V transpose. Transposing a product reverses "
                 "the order, so W transpose is V, sigma, U transpose. Now put them side by side. In the "
                 "middle, U transpose meets U. The transpose of a rotation is the same rotation done "
                 "backwards, and a rotation followed by its reverse does nothing. So the pair cancels. What is"
                 " left is V, sigma times sigma, V transpose. That is not what we want. Our target has U on "
                 "the left, and here U has disappeared.", FadeOut(VGroup(a1, sh1, x1, a2, sh2)), FadeIn(e1))
        self.cue("Transposing a product", FadeIn(e2))
        self.cue("Now put them side by side", Write(prod))
        self.cue("U transpose meets U", Indicate(prod[3], color=WHITE))
        self.cue("So the pair cancels", FadeIn(c4), prod[3].animate.set_opacity(0.4))
        self.cue("What is left is", FadeIn(res))
        self.cue("That is not what we want", FadeIn(bad), Indicate(goal[1], color=C_PLUS))
        self.hold()

        # 05: one more W on the left: U Σ³ Vᵀ
        prod2 = MathTex(r"W\,W^{\top}W", r"=", r"U\,\Sigma\,", r"V^{\top}V", r"\,\Sigma^2\,V^{\top}", font_size=52)
        prod2.move_to([0, 0.6, 0])
        c5 = cancel(prod2[3])
        res2 = MathTex(r"=", r"U\,\Sigma^3\,V^{\top}", font_size=52)
        res2.shift(prod2[1].get_center() + DOWN * 1.9 - res2[0].get_center())
        res2[1].set_color(C_PLUS)
        ok = txt("both rotations are back", 28, C_PLUS).next_to(res2, RIGHT, buff=0.6)
        self.say("So bring U back. Multiply by W one more time, on the left. Now the V transpose at the end of"
                 " W meets the V at the start of our product, and that pair cancels too. What survives is U on"
                 " the left, V transpose on the right, and sigma three times in between. This time both "
                 "rotations are back where they belong.", FadeOut(VGroup(e2, prod, c4, res, bad)))
        self.cue("Multiply by W one more time", Write(prod2))
        self.cue("Now the V transpose", Indicate(prod2[3], color=WHITE))
        self.cue("and that pair cancels too", FadeIn(c5), prod2[3].animate.set_opacity(0.4))
        self.cue("What survives", FadeIn(res2))
        self.cue("This time both rotations", FadeIn(ok))
        self.hold()

        # 06: Σ is diagonal, so Σ³ cubes each σ on its own
        assert abs(1.3 ** 3 - 2.2) < 0.005 and 0.5 ** 3 == 0.125
        top3 = mt(r"W\,W^{\top}W=U\,\Sigma^3\,V^{\top}", 46).move_to([0, 2.3, 0])
        dg = mt(r"\Sigma=\begin{pmatrix}1.3&0\\0&0.5\end{pmatrix}", 42, C_SIG).move_to([0, 0.7, 0])
        dg3 = MathTex(r"\Sigma^3=\begin{pmatrix}1.3^3&0\\0&0.5^3\end{pmatrix}",
                      r"\approx\begin{pmatrix}2.2&0\\0&0.125\end{pmatrix}", font_size=42, color=C_SIG)
        dg3.move_to([0, -1.1, 0])
        self.say("And the middle is easy to read. Sigma is diagonal, which means it only holds the singular "
                 "values, one for each direction. Multiplying diagonal matrices just multiplies the matching "
                 "entries. So sigma three times in a row cubes each singular value on its own. In our example,"
                 " one point three becomes about two point two, and zero point five becomes zero point one two"
                 " five. No direction disturbs another.", FadeOut(VGroup(e1, prod2, c5, res2, ok)), FadeIn(top3))
        self.cue("Sigma is diagonal", FadeIn(dg))
        self.cue("So sigma three times", FadeIn(dg3[0]))
        self.cue("In our example", FadeIn(dg3[1]))
        self.hold()

        # 07: the two attempts, and one more Wᵀ W
        rows = VGroup(MathTex(r"W^{\top}W", r"=", r"V\,\Sigma^2\,V^{\top}", font_size=46),
                      MathTex(r"W\,W^{\top}W", r"=", r"U\,\Sigma^3\,V^{\top}", font_size=46),
                      MathTex(r"W\,W^{\top}W\,W^{\top}W", r"=", r"U\,\Sigma^5\,V^{\top}", font_size=46))
        for r_, y in zip(rows, (1.6, 0.4, -0.8)):
            r_.shift(np.array([0.6, y, 0]) - r_[1].get_center())
        notes = VGroup(txt("lost a rotation", 26, C_S5).next_to(rows[0], RIGHT, buff=0.5),
                       txt("kept both", 26, C_PLUS).next_to(rows[1], RIGHT, buff=0.5),
                       txt("kept both", 26, C_PLUS).next_to(rows[2], RIGHT, buff=0.5))
        self.say("Look back at the two attempts. Two copies of W lost a rotation. Three copies kept both, and "
                 "only the singular values changed. And we can keep going. Attach another W transpose times W,"
                 " and the same cancelling happens again. U and V transpose stay where they are, and the "
                 "middle gains two more sigmas.", FadeOut(VGroup(top3, dg, dg3)))
        self.cue("Two copies of W", FadeIn(rows[0]), FadeIn(notes[0]))
        self.cue("Three copies kept both", FadeIn(rows[1]), FadeIn(notes[1]))
        self.cue("Attach another", FadeIn(rows[2]))
        self.cue("U and V transpose stay", FadeIn(notes[2]))
        self.hold()

        # 08: the odd products
        odd = VGroup(*[MathTex(a, r"\;\leadsto\;", b, font_size=44) for a, b in
                       ((r"W", r"\sigma"), (r"W\,W^{\top}W", r"\sigma^3"),
                        (r"W\,W^{\top}W\,W^{\top}W", r"\sigma^5"))])
        for m, y in zip(odd, (1.5, 0.5, -0.5)):
            m[2].set_color(C_SIG)
            m.shift(np.array([1.2, y, 0]) - m[1].get_center())
        self.say("So the products with an odd number of copies are the ones we can use. W itself carries "
                 "sigma. Three copies carry sigma cubed. Five copies carry sigma to the fifth, and so on.", FadeOut(rows), FadeOut(notes))
        self.cue("W itself carries", FadeIn(odd[0], shift=RIGHT * 0.2))
        self.cue("Three copies carry", FadeIn(odd[1], shift=RIGHT * 0.2))
        self.cue("Five copies carry", FadeIn(odd[2], shift=RIGHT * 0.2))
        self.hold()

        # 09: a mix is a polynomial p; one step cannot do it; two terms
        mix = MathTex(r"a\,W+b\,W\,W^{\top}W+\cdots", r"=", r"U\,(a\,\Sigma+b\,\Sigma^3+\cdots)\,V^{\top}", font_size=40)
        mix.move_to([0, 2.1, 0])
        pdef = MathTex(r"\sigma\ \longmapsto\ ", r"a\,\sigma+b\,\sigma^3+\cdots", r"\ =\ p(\sigma)", font_size=40)
        pdef.move_to([0, 1.3, 0])
        pdef[1:].set_color(C_SIG)
        want = mt(r"\text{want: }\ p(\sigma)=1\ \text{ for every }\sigma", 36).move_to([0, 0.6, 0])
        wx = Line(want.get_left(), want.get_right(), color=C_S5, stroke_width=4)
        tiny = mt(r"\text{a tiny }\sigma\text{ gives a tiny }p(\sigma)", 34, C_S5).move_to([0, 0.0, 0])
        rep = mt(r"\sigma\ \to\ p(\sigma)\ \to\ p(p(\sigma))\ \to\ \cdots\ \to\ 1", 40, C_PLUS).move_to([0, -0.9, 0])
        one = mt(r"p(\sigma)=a\,\sigma\qquad\text{only rescales}", 36, GREY_B).move_to([0, -1.9, 0])
        guess = mt(r"p(\sigma)=a\,\sigma+b\,\sigma^3", 46).move_to([0, -1.9, 0])
        self.say("Every one of these products has the same U on the left and the same V transpose on the "
                 "right. So if we multiply each product by a number and add them up, U and V transpose factor "
                 "out, and only the middle is a sum. In that middle, each singular value becomes a number "
                 "times sigma, plus a number times sigma cubed, and so on. A sum of powers like this is a "
                 "polynomial. Call it p. So turning W into U times V transpose now means one thing. We need a "
                 "p that sends every sigma to one. Can p do that in a single step? Then it would have to give "
                 "one for every input. But p is made of powers of sigma, so a tiny sigma always gives a tiny "
                 "output. One step is not enough. So we ask for less. One step only has to bring sigma closer "
                 "to one, and then we apply p again and again. Which p? Every extra term costs more matrix "
                 "products, so we want as few as possible. One term alone, a times sigma, only rescales every "
                 "singular value by the same number, so the ellipse stays an ellipse. So take two terms, a "
                 "times sigma plus b times sigma cubed.", *[Indicate(m[0], color=WHITE, scale_factor=1.05) for m in odd])
        self.cue("So if we multiply each product", FadeOut(odd), FadeIn(mix))
        self.cue("each singular value becomes", FadeIn(pdef[:2]))
        self.cue("Call it p", FadeIn(pdef[2]))
        self.cue("We need a p that sends", FadeIn(want))
        self.cue("But p is made of powers", FadeIn(tiny))
        self.cue("One step is not enough", Create(wx))
        self.cue("So we ask for less", FadeIn(rep))
        self.cue("One term alone", FadeIn(one))
        self.cue("So take two terms", FadeOut(one), FadeIn(guess))
        self.hold()

        # 10: wish one, p(1) = 1
        p1 = MathTex(r"p(1)", r"=a\cdot1+b\cdot1^3", r"=a+b", font_size=42).move_to([0, 1.3, 0])
        w1 = mt(r"\text{wish 1:}\quad a+b=1", 42, C_PLUS).move_to([0, 0.2, 0])
        self.say("What should a and b be? We want the repeated steps to settle at one. So a sigma that has "
                 "reached one must stay there, or the steps would never settle. Put sigma equals one into p. "
                 "One cubed is still one, so p gives a plus b. For one to stay at one, a plus b must equal "
                 "one. Call this our first wish.", FadeOut(VGroup(mix, pdef, want, wx, tiny)), guess.animate.move_to([0, 2.6, 0]),
                 rep.animate.move_to([0, -2.4, 0]).set_opacity(0.6))
        self.cue("Put sigma equals one", FadeIn(p1[:2]))
        self.cue("so p gives", FadeIn(p1[2]))
        self.cue("must equal one", FadeIn(w1))
        self.hold()

        # 11: wish two, the error near 1 is multiplied by a + 3b
        l1 = MathTex(r"p(1+e)", r"=a\,(1+e)+b\,(1+e)^3", font_size=42).move_to([-0.6, 1.5, 0])
        cube = mt(r"(1+e)^3=1+3e+3e^2+e^3\approx1+3e", 36, GREY_A).move_to([0, 0.7, 0])
        exm = mt(r"1.1^3=1.331\approx1.3", 32, GREY_B).next_to(cube, DOWN, buff=0.22)
        assert abs(1.1 ** 3 - 1.331) < 1e-12
        ls = VGroup(mt(r"\approx a\,(1+e)+b\,(1+3e)", 42), mt(r"=(a+b)+(a+3b)\,e", 42), mt(r"=1+(a+3b)\,e", 42))
        for m, y in zip(ls, (-0.6, -1.3, -2.0)):
            m.move_to([0, y, 0]).align_to(l1[1], LEFT)
        err = mt(r"\text{error: }\quad e\ \ \longrightarrow\ \ (a+3b)\,e", 38, C_SIG).move_to([0, 0.5, 0])
        w2 = mt(r"\text{wish 2:}\quad a+3b=0", 42, C_PLUS).scale(0.8).move_to([4.7, 2.0, 0])
        self.say("Staying at one is not enough. A sigma that is only close to one has to move closer. So take "
                 "a sigma that misses one by a small error e, and put one plus e into p. We need the cube of "
                 "one plus e. Multiplied out, it is one, plus three e, plus terms with e squared and e cubed. "
                 "When e is small, those last terms are far smaller still, so we drop them. For example, one "
                 "point one cubed is one point three three, very close to one point three. So p gives a times "
                 "one plus e, plus b times one plus three e. Collect the pieces, and that is a plus b, plus a "
                 "plus three b times e. The first piece, a plus b, is one, by our first wish. So p gives one, "
                 "plus a plus three b times e. We went in with an error of e, and we came out with an error of"
                 " a plus three b times e. One step multiplies the error by a plus three b. We want the error "
                 "to shrink, and the most it can shrink is all the way to nothing. So our second wish is that "
                 "a plus three b equals zero.", FadeOut(p1), FadeOut(rep), w1.animate.scale(0.8).move_to([4.7, 2.6, 0]))
        self.cue("put one plus e into p", FadeIn(l1))
        self.cue("Multiplied out", FadeIn(cube))
        self.cue("For example", FadeIn(exm))
        self.cue("So p gives", FadeIn(ls[0]))
        self.cue("Collect the pieces", FadeIn(ls[1]))
        self.cue("The first piece", Indicate(w1, color=C_PLUS), FadeIn(ls[2]))
        self.cue("We went in with", FadeOut(VGroup(cube, exm)), FadeIn(err))
        self.cue("So our second wish", FadeIn(w2), Indicate(ls[2][0][3:8], color=C_PLUS))
        self.hold()

        # 12: solve; the polynomial and the matrix step
        both = VGroup(mt(r"a+b=1", 44, C_PLUS), mt(r"a+3b=0", 44, C_PLUS)).arrange(RIGHT, buff=1.2)
        both.move_to([0, 1.5, 0])
        sol = VGroup(mt(r"a=-3b", 42), mt(r"-3b+b=1\ \ \Longrightarrow\ \ b=-\tfrac12", 42), mt(r"a=\tfrac32", 42))
        sol.arrange(DOWN, buff=0.35).move_to([0, -0.4, 0])
        px = MathTex(r"p(\sigma)", r"=", r"\tfrac32\,\sigma-\tfrac12\,\sigma^3", font_size=60)
        px[2].set_color(C_P)
        px.move_to([0, 0.8, 0])
        box = SurroundingRectangle(px, color=C_P, buff=0.25, corner_radius=0.1)
        step = mt(r"W\ \leftarrow\ \tfrac32\,W-\tfrac12\,W\,W^{\top}W", 46).move_to([0, -1.2, 0])
        self.say("Two wishes and two unknowns, which is exactly enough. The second wish says a equals minus "
                 "three b. Put that into the first, and minus three b plus b equals one, so b is minus one "
                 "half. Then a is three halves. So p of sigma is three halves sigma, minus one half sigma "
                 "cubed. For the matrix, one step is three halves W, minus one half W times W transpose times "
                 "W. That is the Newton–Schulz step, and you could have invented it yourself.", FadeOut(VGroup(l1, ls, err)), ReplacementTransform(w1, both[0]),
                 ReplacementTransform(w2, both[1]))
        self.cue("The second wish says", FadeIn(sol[0]))
        self.cue("Put that into the first", FadeIn(sol[1]))
        self.cue("is three halves", FadeIn(sol[2]))
        self.cue("So p of sigma is", FadeOut(VGroup(both, sol)), ReplacementTransform(guess, px), Create(box))
        self.cue("For the matrix", FadeIn(step))
        self.hold(1.0)

        # 13: the question for the rest of the video
        q = mt(r"\sigma\;\to\;p(\sigma)\;\to\;p(p(\sigma))\;\to\;\cdots\;\to\;?", 42, GREY_A).move_to([0, -1.2, 0])
        self.say("We built p from what happens close to one. But a real sigma can start anywhere. So take any "
                 "positive sigma and apply p over and over. Where does it end up? That is the question in part"
                 " (e) of the worksheet, and the rest of this video answers it.", FadeOut(step), FadeIn(q, shift=UP * 0.2))
        self.hold()
        corner = MathTex(r"p(x)=\tfrac32x-\tfrac12x^3", font_size=34).to_corner(UR, buff=0.35)
        corner[0][5:].set_color(C_P)
        self.play(FadeOut(VGroup(q, box, goal, cheap)), ReplacementTransform(px, corner))
        self.corner = corner

    # ------------------------------------------------------------ 3. just try some numbers
    def try_numbers(self):
        def chain(x0, n):
            """x0 → p(x0) → …, one mobject per term, so each can appear when it is said."""
            o = orbit(x0, n)
            assert abs(o[-1] - 1) < 0.003
            terms = [num(x0, 1)] + [r"\to " + num(v, 3 if 0.995 <= v < 0.9995 else 2) for v in o[1:]]
            return VGroup(*[mt(s, 34) for s in terms], mt(r"\to\cdots\to 1", 34, C_PLUS)).arrange(RIGHT, buff=0.14)

        lines = VGroup(chain(0.5, 4), chain(1.3, 3), chain(0.1, 8))
        lines.arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(UP * 1.2).to_edge(LEFT, buff=0.8)
        if lines.width > 12.4:
            lines.scale_to_fit_width(12.4).to_edge(LEFT, buff=0.8)
        assert abs(1.5 * 0.5 - 0.75) < 1e-12 and 0.5 ** 3 == 0.125 and p(0.5) == 0.6875
        calc = VGroup(mt(r"\tfrac32\cdot0.5=0.75", 38), mt(r"0.5^3=0.125", 38),
                      mt(r"\tfrac12\cdot0.125=0.0625", 38)).arrange(RIGHT, buff=0.9).move_to(DOWN * 0.6)
        res = mt(r"p(0.5)=0.75-0.0625=0.6875", 40, C_P).move_to(DOWN * 1.7)
        self.say("Where does a sigma end up? No theory yet. Let's just pick a number and try it, say zero "
                 "point five.")
        self.cue("say zero point five", FadeIn(lines[0][0]))
        self.say("One step of p takes three halves of the number, and subtracts one half of its cube. Three "
                 "halves of zero point five is zero point seven five. Zero point five cubed is zero point one "
                 "two five, and half of that is zero point zero six two five. Subtract, and we get zero point "
                 "six eight seven five.")
        self.cue("Three halves of zero point five", FadeIn(calc[0]))
        self.cue("Zero point five cubed", FadeIn(calc[1]))
        self.cue("and half of that", FadeIn(calc[2]))
        self.cue("Subtract", FadeIn(res))
        self.hold()
        self.say("Now feed that result back in, and keep going. Zero point six nine becomes zero point eight "
                 "seven, then zero point nine eight, then zero point nine nine nine. It is closing in on one.", FadeOut(calc), FadeOut(res), FadeIn(lines[0][1]))
        self.cue("becomes zero point eight seven", FadeIn(lines[0][2]))
        self.cue("then zero point nine eight", FadeIn(lines[0][3]))
        self.cue("then zero point nine nine nine", FadeIn(lines[0][4]))
        self.cue("It is closing in on one", FadeIn(lines[0][5]))
        self.say("That start was below one. Now try one above it. One point three drops to zero point eight "
                 "five, which is below one, and then it climbs, to zero point nine seven, and then zero point "
                 "nine nine eight. It also closes in on one.")
        self.cue("One point three drops", FadeIn(lines[1][0]), FadeIn(lines[1][1]))
        self.cue("to zero point nine seven", FadeIn(lines[1][2]))
        self.cue("and then zero point nine nine eight", FadeIn(lines[1][3]))
        self.cue("It also closes in", FadeIn(lines[1][4]))
        self.say("Both of those were fairly close to one. So try a start that is far away, down near zero. "
                 "Zero point one becomes zero point one five, then zero point two two, then zero point three "
                 "three. It is slow at first, but it keeps climbing, and after eight steps it also reaches "
                 "one.")
        self.cue("Zero point one becomes", FadeIn(lines[2][0]), FadeIn(lines[2][1]))
        self.cue("then zero point two two", FadeIn(lines[2][2]))
        self.cue("then zero point three three", FadeIn(lines[2][3]))
        self.cue("but it keeps climbing", LaggedStart(*[FadeIn(m) for m in lines[2][4:9]], lag_ratio=0.5),
                 run_time=2.5)
        self.cue("it also reaches one", FadeIn(lines[2][9]))
        self.hold()
        p1 = mt(r"p(1)=\tfrac32-\tfrac12=1", 40, C_PLUS).move_to([-2.6, -1.6, 0])
        self.say("All three starts end at one. And once a value is at one, it stays there. Three halves minus "
                 "one half is one, so p of one equals one. That is our first wish at work.", *[Indicate(l[-1], color=C_PLUS) for l in lines])
        self.cue("Three halves minus one half", FadeIn(p1))
        self.hold()
        p0 = mt(r"p(0)=\tfrac32\cdot0-\tfrac12\cdot0^3=0", 40, C_ZERO).move_to([2.8, -1.6, 0])
        fp = VGroup(txt("fixed point:", 30), mt(r"p(x)=x", 42)).arrange(RIGHT, buff=0.3).move_to(UP * 1.6)
        self.say("But if some other number also stayed put, a sigma could get stuck there and never reach one."
                 " Is there such a number? Try zero. Three halves of zero is zero, and zero cubed is zero, so "
                 "p of zero is zero. Zero stays put as well. From here on, call the input x. A value where p "
                 "of x equals x is called a fixed point. We have found two of them. Are there any more?")
        self.cue("Try zero", FadeIn(p0))
        self.cue("From here on, call the input x", FadeOut(lines), FadeIn(fp))
        self.cue("We have found two of them", Indicate(p1, color=C_PLUS), Indicate(p0, color=C_ZERO))
        self.hold()

        der = VGroup(mt(r"p(x)=x", 40),
                     mt(r"\tfrac32x-\tfrac12x^3=x", 40),
                     mt(r"\tfrac12x-\tfrac12x^3=0", 40),
                     mt(r"\tfrac12\,x\,(1-x^2)=0", 40),
                     mt(r"\tfrac12\,x\,(1-x)(1+x)=0", 40),
                     mt(r"x=0,\ \ x=1,\ \ x=-1", 42, C_PLUS)).arrange(DOWN, buff=0.33).move_to(UP * 0.5)
        self.say("To find them all at once, write down p of x equals x. That is three halves x, minus one half"
                 " x cubed, equals x. Subtract x from both sides, and we get one half x, minus one half x "
                 "cubed, equals zero.", FadeOut(VGroup(p1, p0, fp)))
        self.cue("write down p of x equals x", FadeIn(der[0]))
        self.cue("That is three halves x", FadeIn(der[1]))
        self.cue("Subtract x from both sides", FadeIn(der[2]))
        self.say("Both terms contain one half x, so pull it out. What is left inside is one minus x squared. "
                 "And one minus x squared splits into one minus x, times one plus x. So the equation says one "
                 "half x, times one minus x, times one plus x, equals zero.")
        self.cue("so pull it out", FadeIn(der[3]))
        self.cue("splits into", FadeIn(der[4]))
        self.hold()
        chk = mt(r"p(-1)=-\tfrac32+\tfrac12=-1", 36, C_MINUS).next_to(der, DOWN, buff=0.4)
        self.say("A product is zero only if one of its factors is zero. So x is zero, or x is one, or x is "
                 "minus one. Those are all the fixed points there are, the two we found and a new one. And "
                 "minus one does check out. Minus three halves, plus one half, is minus one. A singular value "
                 "is never negative, so for now minus one is just a point on the list.")
        self.cue("So x is zero", FadeIn(der[5]))
        self.cue("And minus one does check out", FadeIn(chk))
        self.hold()
        again = chain(0.1, 8)
        again.move_to(DOWN * 0.2)
        if again.width > 12.4:
            again.scale_to_fit_width(12.4)
        stuck = mt(r"0\to 0\to 0\to\cdots", 36, C_ZERO).next_to(again, UP, buff=0.6)
        self.say("But zero matters right away. A sigma at exactly zero is stuck. And yet zero point one, right"
                 " next to zero, walked away from it, all the way to one. Why would one fixed point pull "
                 "values in and another push them away? To see what happens around each of them, we need a "
                 "picture of the iteration.", FadeOut(VGroup(der, chk)))
        self.cue("A sigma at exactly zero", FadeIn(stuck))
        self.cue("And yet zero point one", FadeIn(again))
        self.hold()
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 4. the graph and the cobweb
    def cobweb(self):
        g = self.make_graph()
        ax, curve, diag = self.ax, self.curve, self.diag
        known = VGroup(Dot(ax.c2p(0, 0), radius=0.07, color=WHITE), Dot(ax.c2p(1, 1), radius=0.07, color=WHITE))
        guide = VGroup(DashedLine(ax.c2p(1, 0), ax.c2p(1, 1), color=GREY_B, dash_length=0.05),
                       DashedLine(ax.c2p(0, 1), ax.c2p(1, 1), color=GREY_B, dash_length=0.05))
        io = VGroup(txt("along the bottom: the input x", 24), txt("height of the curve: the output p(x)", 24, C_P))
        io.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([PANEL_X, 1.8, 0])
        self.say("Start with the graph of p. Along the bottom is the input x, and the height of the curve "
                 "above it is the output, p of x. We know a few points already. At zero the height is zero, "
                 "and at one the height is one. The curve rises from zero, reaches a hump at one, and comes "
                 "back down after it.", Create(ax), FadeIn(g[1]), Create(curve), FadeIn(g[4]), run_time=2.0)
        self.cue("Along the bottom", FadeIn(io[0]))
        self.cue("and the height of the curve", FadeIn(io[1]))
        self.cue("At zero the height is zero", GrowFromCenter(known[0]))
        self.cue("and at one the height is one", Create(guide), GrowFromCenter(known[1]))
        self.hold()

        w = self.web(0.3, 8, WHITE)
        m = self.start_mark(0.3, WHITE)
        y1 = p(0.3)
        assert abs(y1 - 0.44) < 0.005 and abs(p(y1) - 0.61) < 0.005
        pt1 = Dot(ax.c2p(0.3, y1), radius=0.06, color=WHITE)
        pl1 = mt(r"p(0.3)\approx" + num(y1), 36).move_to([PANEL_X, 1.9, 0])
        self.say("On this picture, one step of the iteration looks like this. Start at x equals zero point "
                 "three on the bottom axis, and go straight up to the curve. The height you reach is p of zero"
                 " point three, about zero point four four.", FadeOut(VGroup(known, guide, io)))
        self.cue("Start at x equals zero point three", FadeIn(m))
        self.cue("and go straight up to the curve", Create(w[0]))
        self.cue("The height you reach", GrowFromCenter(pt1), FadeIn(pl1))
        self.hold()
        hgt = DashedLine(ax.c2p(0.3, y1), ax.c2p(0, y1), color=YELLOW_D, dash_length=0.05)
        hl = mt(num(y1), 24, YELLOW_D).next_to(ax.c2p(0, y1), LEFT, buff=0.1)
        ask = VGroup(txt("a height", 26, YELLOW_D), mt(r"\longrightarrow", 34), txt("a position ?", 26))
        ask.arrange(RIGHT, buff=0.3).next_to(pl1, DOWN, buff=0.6)
        self.say("For the next step, zero point four four has to become the new input. But right now it is a "
                 "height, and inputs are measured along the bottom. We need a way to turn a height into a "
                 "position.")
        self.cue("But right now it is a height", Create(hgt), FadeIn(hl))
        self.cue("We need a way", FadeIn(ask))
        self.hold()
        pt2 = Dot(ax.c2p(y1, y1), radius=0.06, color=WHITE)
        drop = DashedLine(ax.c2p(y1, y1), ax.c2p(y1, 0), color=YELLOW_D, dash_length=0.05)
        dl = mt(num(y1), 24, YELLOW_D).next_to(ax.c2p(y1, 0), DOWN, buff=0.1)
        on_d = mt(r"\text{on the diagonal: }(" + num(y1) + r",\ " + num(y1) + ")", 32).move_to(ask)
        self.say("Here is a line that does exactly that, the diagonal y equals x. Every point on it is as far "
                 "to the right as it is high. So go sideways from the curve until you hit the diagonal. You "
                 "are still at height zero point four four, and now you are also above x equals zero point "
                 "four four.", FadeOut(ask))
        self.cue("the diagonal y equals x", Create(diag), FadeIn(g[5]))
        self.cue("So go sideways from the curve", Create(w[1]), GrowFromCenter(pt2))
        self.cue("You are still at height", FadeIn(on_d))
        self.cue("and now you are also above", Create(drop), FadeIn(dl))
        self.hold()
        seq = mt(r"0.3\to " + r"\to ".join(num(v) for v in orbit(0.3, 4)[1:]) + r"\to\cdots\to 1", 32)
        seq.move_to([PANEL_X, 1.9, 0])
        if seq.width > 6.2:
            seq.scale_to_fit_width(6.2)
        self.say("From there, the second step is the same move. Go straight up to the curve, which gives zero "
                 "point six one, and sideways to the diagonal again. Keep repeating, and the path climbs like "
                 "a staircase, zero point eight, zero point nine five, and into one.", FadeOut(VGroup(pt1, pl1, pt2, on_d, drop, dl, hgt, hl)), FadeIn(seq))
        self.cue("Go straight up to the curve", Create(w[2]))
        self.cue("and sideways to the diagonal again", Create(w[3]))
        self.cue("Keep repeating", self.draw(w[4:], 0.3))
        self.hold()
        w2 = self.web(1.2, 5, WHITE)
        m2 = self.start_mark(1.2, WHITE)
        assert abs(p(1.2) - 0.94) < 0.005
        seq2 = mt(r"1.2\to " + num(p(1.2)) + r"\to\cdots\to 1", 32).move_to(seq)
        self.say("Now a start above one. From one point two, the curve is below the diagonal, so the first "
                 "move goes down, to zero point nine four. After that the path climbs the last little bit and "
                 "settles on one as well.", FadeOut(VGroup(w, m, seq)), FadeIn(m2))
        self.cue("so the first move goes down", Create(w2[0]), FadeIn(seq2))
        self.cue("After that the path climbs", self.draw(w2[1:], 0.4))
        self.hold()
        fps = VGroup(*[Dot(ax.c2p(v, v), radius=0.09, color=c)
                       for v, c in ((-1, C_MINUS), (0, C_ZERO), (1, C_PLUS))])
        cross = VGroup(mt(r"\text{diagonal: height}=x", 32, C_DIAG), mt(r"\text{curve: height}=p(x)", 32, C_P),
                       mt(r"\text{crossing: }p(x)=x", 34)).arrange(DOWN, buff=0.3).move_to([PANEL_X, 1.5, 0])
        away = self.web(0.05, 6, C_ZERO, width=2.5)
        self.say("Now look at where the curve meets the diagonal. On the diagonal the height equals x, and on "
                 "the curve the height is p of x. So at a crossing, p of x equals x. The three crossings are "
                 "our three fixed points, minus one, zero, and one. And the staircases show which way things "
                 "move around them. Near zero the path walks away, and near one it walks in.", FadeOut(VGroup(w2, m2, seq2)))
        self.cue("On the diagonal the height equals x", FadeIn(cross[0]))
        self.cue("and on the curve", FadeIn(cross[1]))
        self.cue("So at a crossing", FadeIn(cross[2]))
        self.cue("The three crossings", LaggedStart(*[GrowFromCenter(d) for d in fps], lag_ratio=0.25))
        self.cue("Near zero the path walks away", self.draw(away, 0.2))
        self.hold()
        self.play(FadeOut(VGroup(cross, away)))
        self.fps = fps

    # ------------------------------------------------------------ 5. why 1 attracts and 0 repels
    def slopes(self):
        ax, fps = self.ax, self.fps
        TOP = [PANEL_X, 2.2, 0]
        at1 = VGroup(mt(r"p(1+e)\approx1+(a+3b)\,e", 36), mt(r"a+3b=0", 36, C_PLUS),
                     mt(r"\text{at }1:\ \text{error}\times0", 36, C_PLUS)).arrange(DOWN, buff=0.3).move_to(TOP, UP)
        self.say("Why does one pull values in, while zero pushes them away? For one, we already know. When we "
                 "built p, we put in one plus a small error e, and we chose p so that one step multiplies that"
                 " error by zero.", Indicate(fps[2], color=C_PLUS), Indicate(fps[1], color=C_ZERO))
        self.cue("we put in one plus a small error e", FadeIn(at1[0]))
        self.cue("and we chose p", FadeIn(at1[1]))
        self.cue("multiplies that error by zero", FadeIn(at1[2]))
        self.hold()
        at0 = VGroup(mt(r"p(e)=1.5\,e-0.5\,e^3", 36), mt(r"e=0.1:\quad e^3=0.001", 32, GREY_A),
                     mt(r"p(e)\approx1.5\,e", 36), mt(r"\text{at }0:\ \text{error}\times1.5", 36, C_ZERO))
        at0.arrange(DOWN, buff=0.3).move_to(TOP, UP)
        self.say("So do the same thing at zero. A value near zero is just a small error e. Put it into p, and "
                 "we get one point five e, minus one half e cubed. For a small e, the cube is tiny. If e is "
                 "zero point one, e cubed is only zero point zero zero one. So p gives about one point five e."
                 " This time, one step multiplies the error by one point five, and the error grows.", FadeOut(at1[:2]), at1[2].animate.move_to([PANEL_X, -2.3, 0]))
        self.cue("Put it into p", FadeIn(at0[0]))
        self.cue("If e is zero point one", FadeIn(at0[1]))
        self.cue("So p gives about", FadeIn(at0[2]))
        self.cue("This time, one step multiplies", FadeIn(at0[3]))
        self.hold()
        o = orbit(0.1, 3)
        assert all(abs(b_ / a_ - 1.5) < 0.03 for a_, b_ in zip(o, o[1:]))
        grow = mt(r"0.1\to " + r"\to ".join(num(v) for v in o[1:]), 34)
        times = mt(r"\times1.5\quad\times1.5\quad\times1.5", 26, C_ZERO)
        gg = VGroup(grow, times).arrange(DOWN, buff=0.15).move_to(TOP, UP)
        tan0 = ax.plot(lambda x: 1.5 * x, x_range=[-0.9, 0.9], color=C_ZERO, stroke_width=3)
        E = 0.6
        tri = VGroup(Line(ax.c2p(0, 0), ax.c2p(E, 0), color=YELLOW_D, stroke_width=4),
                     Line(ax.c2p(E, 0), ax.c2p(E, 1.5 * E), color=YELLOW_D, stroke_width=4))
        tri_l = VGroup(mt("e", 26, YELLOW_D).next_to(tri[0], DOWN, buff=0.08),
                       mt("1.5e", 26, YELLOW_D).next_to(tri[1], RIGHT, buff=0.08))
        slope0 = mt(r"\text{slope at }0:\ \frac{1.5\,e}{e}=1.5", 36, C_ZERO).next_to(gg, DOWN, buff=0.5)
        self.say("We have seen this growth already. Zero point one went to zero point one five, then zero "
                 "point two two, then zero point three three. Each value is about one and a half times the one"
                 " before. That is why zero pushes values away. On the graph, this multiplier is the slope of "
                 "the curve. Zoom in at zero, and the curve looks like a straight line. Move e to the right, "
                 "and it rises by one point five e. Rise over run is one point five.", FadeOut(at0[:3]), at0[3].animate.move_to([PANEL_X, -1.7, 0]), FadeIn(grow))
        self.cue("Each value is about", FadeIn(times))
        self.cue("Zoom in at zero", Create(tan0))
        self.cue("Move e to the right", Create(tri[0]), FadeIn(tri_l[0]))
        self.cue("and it rises by", Create(tri[1]), FadeIn(tri_l[1]))
        self.cue("Rise over run", FadeIn(slope0))
        self.hold()
        rule = VGroup(txt("each step: error × slope", 26),
                      mt(r"|\text{slope}|>1:\ \text{pushed away}", 34, C_ZERO),
                      mt(r"|\text{slope}|<1:\ \text{pulled in}", 34, C_PLUS)).arrange(DOWN, buff=0.3).move_to(TOP, UP)
        near0 = orbit(0.05, 3)
        assert abs(near0[1] - 0.075) < 0.0005 and abs(near0[2] - 0.11) < 0.005
        seq0 = mt(r"0.05\to0.075\to0.11\to\cdots", 32, C_ZERO).next_to(rule, DOWN, buff=0.45)
        w0 = self.web(0.05, 10, C_ZERO, width=2.5)
        self.say("So here is the rule. Near a fixed point, each step multiplies the error by the slope of the "
                 "curve there. If the slope is bigger than one in size, the error grows and values are pushed "
                 "away. If it is smaller than one, the error shrinks and values are pulled in. At zero the "
                 "slope is one point five, and zero point zero five drifts to zero point zero seven five, then"
                 " zero point one one, and on.", FadeOut(VGroup(gg, slope0, tri, tri_l)), FadeIn(rule[0]))
        self.cue("If the slope is bigger than one", FadeIn(rule[1]))
        self.cue("If it is smaller than one", FadeIn(rule[2]))
        self.cue("and zero point zero five drifts", FadeIn(seq0), self.draw(w0, 0.22))
        self.hold()
        near1 = orbit(1.2, 2)
        errs = [abs(v - 1) for v in near1]
        assert abs(errs[1] - 0.06) < 0.005 and abs(errs[2] - 0.006) < 0.0005
        tan1 = VGroup(ax.plot(lambda x: 1, x_range=[0.5, 1.5], color=C_PLUS, stroke_width=3),
                      ax.plot(lambda x: -1, x_range=[-1.5, -0.5], color=C_MINUS, stroke_width=3))
        flat = VGroup(mt(r"\text{slope at }\pm1:\ 0", 36, C_PLUS), mt(r"\text{new error}\approx1.5\,e^2", 36),
                      mt(r"\text{error: }\ 0.2\to0.06\to0.006", 34, C_PLUS)).arrange(DOWN, buff=0.3).move_to(TOP, UP)
        w1 = self.web(1.2, 5, C_PLUS, width=2.5)
        self.say("At one, the multiplier is zero, so the slope is zero. The curve is flat at the top of its "
                 "hump. That is our second wish, seen as a picture. But an error cannot vanish completely in "
                 "one step. When we built p, we dropped the terms with e squared, because they were small. Now"
                 " they are all that is left. Worked out, the new error is about one and a half times e "
                 "squared. Start at one point two. The error goes from zero point two, to zero point zero six,"
                 " to zero point zero zero six. Each step roughly squares it, which is far faster than "
                 "shrinking by a fixed factor. The same calculation at minus one gives the same result.", FadeOut(VGroup(rule, seq0, w0, tan0)))
        self.cue("The curve is flat", Create(tan1[0]), FadeIn(flat[0]))
        self.cue("Worked out, the new error", FadeIn(flat[1]))
        self.cue("Start at one point two", self.draw(w1, 0.3), FadeIn(flat[2]))
        self.cue("The same calculation at minus one", Create(tan1[1]))
        self.hold()
        lab0 = txt("unstable", 22, C_ZERO).next_to(fps[1], RIGHT, buff=0.3).shift(DOWN * 0.45)
        lab1 = txt("stable", 22, C_PLUS).next_to(fps[2], UP, buff=0.3).shift(LEFT * 0.35)
        lab_1 = txt("stable", 22, C_MINUS).next_to(fps[0], DOWN, buff=0.3).shift(RIGHT * 0.45)
        self.say("So zero is unstable, like the top of a hill, where the smallest push sends you rolling away."
                 " One and minus one are stable, like the bottoms of two valleys, where everything nearby "
                 "rolls in.", FadeOut(w1), FadeIn(lab0))
        self.cue("One and minus one are stable", FadeIn(lab1), FadeIn(lab_1))
        self.hold()
        self.play(FadeOut(VGroup(flat, tan1, lab0, lab1, lab_1, at1[2], at0[3])))

    # ------------------------------------------------------------ 6. how big can σ be? (√3)
    def how_big(self):
        ax = self.ax
        TOP = [PANEL_X, 2.3, 0]
        m13 = Dot(ax.c2p(1.3, 0), radius=0.06, color=C_PLUS)
        l13 = mt("1.3", 24, C_PLUS).next_to(m13, DOWN, buff=0.35)
        self.say("So far every start rolled into the valley at one. But the largest start we tried was one "
                 "point three, and we don't get to choose sigma. How large can it be before something goes "
                 "wrong?", Indicate(self.fps[2], color=C_PLUS))
        self.cue("the largest start we tried", GrowFromCenter(m13), FadeIn(l13))
        self.hold()
        o = orbit(1.5, 3)
        assert [num(v) for v in o[1:]] == ["0.56", "0.75", "0.92"]
        w = self.web(1.5, 8, C_PLUS)
        m = Dot(ax.c2p(1.5, 0), radius=0.07, color=C_PLUS)
        t15 = mt(r"1.5\to " + r"\to ".join(num(v) for v in o[1:]) + r"\to\cdots\to 1", 34, C_PLUS).move_to(TOP)
        self.say("Go a little bigger, to one point five. That is past the hump, where the curve is already "
                 "coming down, so the first step drops all the way to zero point five six. But from there it "
                 "climbs as before, zero point seven five, zero point nine two, and into one. Still fine.", FadeOut(VGroup(m13, l13)), FadeIn(m), FadeIn(t15[0][:3]))
        self.cue("so the first step drops", Create(w[0]), FadeIn(t15[0][3:8]))
        self.cue("But from there it climbs", self.draw(w[1:], 0.3), FadeIn(t15[0][8:]))
        self.hold()
        m2 = Dot(ax.c2p(1.8, 0), radius=0.07, color=WHITE)
        q18 = mt(r"1.8\to\ ?", 38).move_to(TOP)
        self.say("A little bigger again, one point eight. Before we look, where do you think it ends up?", FadeOut(VGroup(w, m, t15)), FadeIn(m2), FadeIn(q18))
        self.hold(1.5)

        assert abs(1.5 * 1.8 - 2.7) < 1e-9 and abs(0.5 * 1.8 ** 3 - 2.916) < 1e-9 and abs(p(1.8) + 0.216) < 1e-9
        assert abs(p(0.216) - 0.32) < 0.005
        calc = VGroup(mt(r"\tfrac32\cdot1.8=2.7", 34), mt(r"\tfrac12\cdot1.8^3=2.92", 34),
                      mt(r"p(1.8)=2.7-2.92=-0.216", 34, C_MINUS)).arrange(DOWN, buff=0.22).move_to(TOP, UP)
        mirror = VGroup(mt(r"p(-x)=-p(x)", 36), txt("the mirror rule", 24, YELLOW_D)).arrange(RIGHT, buff=0.35)
        mirror.next_to(calc, DOWN, buff=0.45)
        pair = VGroup(mt(r"+0.216\to+0.32", 34, C_PLUS), mt(r"-0.216\to-0.32", 34, C_MINUS))
        pair.arrange(DOWN, buff=0.2).next_to(mirror, DOWN, buff=0.4)
        end = mt(r"1.8\to-0.216\to-0.32\to\cdots\to-1", 32, C_MINUS).next_to(pair, DOWN, buff=0.4)
        w2 = self.web(1.8, 9, C_MINUS)
        self.say("Do the step. Three halves of one point eight is two point seven. But half of its cube is two"
                 " point nine two, which is bigger. Subtract, and the result is negative, minus zero point two"
                 " one six. What does p do with a negative number? p has only odd powers, so flipping the sign"
                 " of the input just flips the sign of the output. Plus zero point two one six goes to plus "
                 "zero point three two, so minus zero point two one six goes to minus zero point three two. "
                 "The negative side is a mirror image of the positive side. Call this the mirror rule. So this"
                 " value does what its mirror image would do, with the sign flipped. It moves away from zero "
                 "and settles at minus one. For a singular value, that has the right size but the wrong sign. "
                 "This direction ends up reversed.", FadeOut(q18))
        self.cue("Three halves of one point eight", FadeIn(calc[0]))
        self.cue("But half of its cube", FadeIn(calc[1]))
        self.cue("Subtract, and the result is negative", FadeIn(calc[2]), Create(w2[0]))
        self.cue("p has only odd powers", FadeIn(mirror[0]))
        self.cue("Plus zero point two one six goes to", FadeIn(pair[0]))
        self.cue("so minus zero point two one six", FadeIn(pair[1]))
        self.cue("Call this the mirror rule", FadeIn(mirror[1]))
        self.cue("It moves away from zero", self.draw(w2[1:], 0.3), FadeIn(end))
        self.cue("that has the right size but the wrong sign", Flash(self.fps[0], color=C_MINUS))
        self.hold(1.0)

        # √3 is where the hump comes back down to the axis
        hump = ax.plot(p, x_range=[0, S3], color=C_PLUS, stroke_width=7)
        past = ax.plot(p, x_range=[S3, 2.05], color=C_MINUS, stroke_width=7)
        cross = Dot(ax.c2p(S3, 0), radius=0.09, color=C_ZERO)
        self.say("So what went wrong was the very first step, which landed below the axis. On the graph, that "
                 "is where the curve, after its hump, comes down and crosses the axis. Past that crossing, p "
                 "of x is negative.", FadeOut(VGroup(calc, mirror, pair, end)), FadeOut(w2[1:]), Indicate(w2[0], color=C_MINUS))
        self.cue("comes down and crosses the axis", Create(hump), GrowFromCenter(cross))
        self.cue("Past that crossing", Create(past))
        self.hold()
        fac = MathTex(r"p(x)", r"=", r"\frac{x}{2}", r"\,(3-x^2)", font_size=42)
        fac.move_to([PANEL_X, 2.2, 0])
        split = VGroup(mt(r"\tfrac32\,x=\tfrac{x}{2}\cdot3", 36), mt(r"\tfrac12\,x^3=\tfrac{x}{2}\cdot x^2", 36))
        split.arrange(DOWN, buff=0.3).next_to(fac, DOWN, buff=0.6)
        tick = Line(ax.c2p(S3, -0.08), ax.c2p(S3, 0.08), color=C_ZERO, stroke_width=4)
        lab = mt(r"\sqrt3", 30, C_ZERO).move_to(ax.c2p(S3 - 0.3, 0.25))
        sgn = VGroup(mt(r"x>0:\quad\frac{x}{2}>0", 36), mt(r"3-x^2<0\iff x>\sqrt3\approx1.73", 36, C_ZERO))
        sgn.arrange(DOWN, buff=0.3).next_to(fac, DOWN, buff=0.45)
        self.say("Where is the crossing? Both terms of p contain x over two. Three halves x is x over two "
                 "times three, and one half x cubed is x over two times x squared. So p of x is x over two, "
                 "times three minus x squared.", FadeOut(w2[0]))
        self.cue("Three halves x is x over two times three", FadeIn(split[0]))
        self.cue("and one half x cubed", FadeIn(split[1]))
        self.cue("So p of x is x over two", Write(fac))
        self.hold()
        self.say("For a positive x, the first factor, x over two, is positive. So the sign of p comes from the"
                 " second factor, three minus x squared.", FadeOut(split), FadeIn(sgn[0]), Indicate(fac[2]))
        self.cue("So the sign of p comes from", Indicate(fac[3]))
        self.say("Three minus x squared is positive while x squared is below three, and negative once x "
                 "squared passes three. The change happens at x equals square root of three, about one point "
                 "seven three.")
        self.cue("and negative once x squared passes three", FadeIn(sgn[1]), Indicate(fac[3], color=C_ZERO))
        self.cue("The change happens at", FadeIn(lab), Flash(cross, color=C_ZERO))
        self.hold()
        m15 = Dot(ax.c2p(1.5, 0), radius=0.07, color=C_PLUS)
        cmp_ = mt(r"1.5<\sqrt3<1.8", 38).next_to(sgn, DOWN, buff=0.5)
        self.say("One point five is below square root of three, and it was fine. One point eight is just above"
                 " it, and it flipped. That matches.", GrowFromCenter(m15), FadeIn(cmp_[0][:3]))
        self.cue("One point eight is just above", Indicate(m2, scale_factor=1.6), FadeIn(cmp_[0][3:]))
        self.hold()
        top = DashedLine(ax.c2p(0, 1), ax.c2p(S3, 1), color=GREY_B, dash_length=0.08)
        land = Line(ax.c2p(0, 0), ax.c2p(0, 1), color=C_PLUS, stroke_width=8)
        first = mt(r"0<x<\sqrt3:\quad 0<p(x)\le1", 36, C_PLUS).next_to(fac, DOWN, buff=0.5)
        self.say("Then is every start below square root of three safe? Look at the curve between zero and "
                 "square root of three. It stays above the axis, and its highest point, the top of the hump, "
                 "is at height one. So wherever we start in this range, the first step lands somewhere between"
                 " zero and one.", FadeOut(VGroup(sgn, cmp_, m15, m2)), FadeOut(past))
        self.cue("It stays above the axis", Indicate(hump, color=C_PLUS, scale_factor=1.0))
        self.cue("the top of the hump", Create(top), Indicate(self.fps[2], color=C_PLUS))
        self.cue("the first step lands somewhere between zero and one", Create(land), FadeIn(first))
        self.hold()
        seg01 = ax.plot(p, x_range=[0, 1], color=C_PLUS)
        area = ax.get_area(seg01, x_range=[0, 1], bounded_graph=self.diag, color=C_PLUS, opacity=0.35)
        w3 = self.web(0.3, 8, WHITE, width=2.5)
        climb = mt(r"0<x<1:\quad p(x)>x", 36, C_PLUS).next_to(first, DOWN, buff=0.35)
        self.say("And between zero and one, the curve sits above the diagonal. That means the output is bigger"
                 " than the input, so every step climbs. It cannot climb past one, because the curve never "
                 "goes higher than one. And the only place where it stops moving is a fixed point, so it ends "
                 "at one.")
        self.cue("the curve sits above the diagonal", FadeIn(area), FadeIn(climb))
        self.cue("so every step climbs", self.draw(w3, 0.3))
        self.cue("so it ends at one", Flash(self.fps[2], color=C_PLUS))
        self.hold()
        safe = Line(ax.c2p(0, 0), ax.c2p(S3, 0), color=C_PLUS, stroke_width=8)
        verdict = mt(r"0<\sigma<\sqrt3\ \ \Longrightarrow\ \ \sigma\to+1", 38, C_PLUS).next_to(climb, DOWN, buff=0.5)
        self.say("So yes. Every sigma between zero and square root of three ends at one.", FadeOut(w3), Create(safe), FadeIn(verdict))
        self.hold()
        arrow = CurvedArrow(ax.c2p(S3, 0) + UP * 0.12, ax.c2p(0, 0) + UP * 0.12, angle=PI / 3,
                            color=C_ZERO, stroke_width=4)
        s3 = mt(r"p(\sqrt3)=\tfrac{\sqrt3}{2}\,(3-3)=0", 36, C_ZERO).next_to(verdict, DOWN, buff=0.4)
        self.say("And exactly at square root of three, the second factor is zero, so p gives zero. The value "
                 "lands on the fixed point at zero, and it stays there forever.", Indicate(fac[3], color=C_ZERO))
        self.cue("so p gives zero", Create(arrow), FadeIn(s3))
        self.cue("and it stays there forever", Flash(self.fps[1], color=C_ZERO))
        self.hold()
        self.play(FadeOut(VGroup(s3, arrow, top, hump, area, cross, land, first, climb, safe, verdict)), FadeIn(tick))
        self.s3_mark = VGroup(tick, lab)
        self.fac = fac

    # ------------------------------------------------------------ 7. much bigger σ (√5)
    def too_big(self):
        ax = self.ax
        o3 = orbit(3.0, 2)
        assert o3 == [3.0, -9.0, 351.0] and 1.5 * 9 == 13.5 and 0.5 * 9 ** 3 == 364.5
        under = self.fac.get_bottom() + DOWN * 0.4
        start3 = mt(r"\text{start: }3", 38, C_S5).move_to(under, UP)
        self.say("So past square root of three, the first step flips the sign. One point eight flipped and "
                 "still settled, at minus one. Maybe a flip is all that ever happens. Test that with a much "
                 "bigger start, three.")
        self.cue("Test that with a much bigger start", FadeIn(start3))
        self.hold()
        steps = VGroup(mt(r"p(3)=4.5-13.5=-9", 34), mt(r"p(-9)=-p(9)", 34),
                       mt(r"p(9)=13.5-364.5=-351", 34)).arrange(DOWN, buff=0.25).move_to(under, UP)
        blow = mt(r"3\to -9\to +351\to\cdots", 38, C_S5).next_to(steps, DOWN, buff=0.4)
        self.say("Three halves of three is four point five, and half of three cubed is thirteen point five. "
                 "Subtract, and we get minus nine. It flipped, as expected. Now the next step. By the mirror "
                 "rule, minus nine does what nine does, with the sign flipped. Nine goes to thirteen point "
                 "five minus three hundred sixty four point five, which is minus three hundred fifty one. So "
                 "minus nine goes to plus three hundred fifty one. It flips every time, and it gets bigger "
                 "every time. This one explodes.", FadeOut(start3))
        self.cue("Three halves of three is four point five", FadeIn(steps[0]))
        self.cue("By the mirror rule", FadeIn(steps[1]))
        self.cue("Nine goes to", FadeIn(steps[2]))
        self.cue("So minus nine goes to plus", FadeIn(blow))
        self.hold()
        sizes = VGroup(mt(r"1.8:\ \ \text{size }0.216<1.8", 34, C_ZERO), mt(r"3:\ \ \text{size }9>3", 34, C_S5),
                       mt(r"2.0:\ \ \text{size }" + num(abs(p(2.0))) + r"<2.0", 34, C_ZERO),
                       mt(r"2.3:\ \ \text{size }" + num(abs(p(2.3))) + r">2.3", 34, C_S5))
        sizes.arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(under, UP)
        self.say("Both one point eight and three flip, so the difference must be in the size, meaning the "
                 "number without its sign. One point eight came out at size zero point two, smaller than it "
                 "went in. Three came out at size nine, bigger than it went in. So somewhere between them, "
                 "shrinking turns into growing. Narrow it down. Two point zero goes to minus one, so its size "
                 "is one. That is still smaller.", FadeOut(VGroup(steps, blow)))
        self.cue("One point eight came out at size", FadeIn(sizes[0]))
        self.cue("Three came out at size nine", FadeIn(sizes[1]))
        self.cue("Two point zero goes to minus one", FadeIn(sizes[2]))
        self.say("But two point three goes to minus two point six three. Its size is bigger than where it "
                 "started. So the turning point is somewhere between two point zero and two point three.", FadeIn(sizes[3]))
        self.hold()
        self.play(FadeOut(sizes))
        xc = _root(-2.5, 1.0, 2.5)
        shrink = ax.plot(p, x_range=[S3, S5], color=C_ZERO, stroke_width=7)
        grow = ax.plot(p, x_range=[S5, xc], color=C_S5, stroke_width=7)
        size = MathTex(r"|p(x)|", r"=", r"|x|", r"\cdot", r"\frac{x^2-3}{2}", font_size=40)
        size.next_to(self.fac, DOWN, buff=0.4)
        box = SurroundingRectangle(size[4], color=YELLOW_D, buff=0.1, stroke_width=2.5)
        box_l = txt("size factor", 22, YELLOW_D).next_to(box, RIGHT, buff=0.15)
        self.say("Where exactly is the turning point? Compare the size after a step with the size before. Use "
                 "the factored form. p of x is x over two, times three minus x squared. So the size of p of x "
                 "is the size of x, times the size of three minus x squared, over two. Past square root of "
                 "three, that second part is x squared minus three, over two. Call it the size factor. Each "
                 "step multiplies the size by this factor.")
        self.cue("p of x is x over two", Indicate(self.fac))
        self.cue("So the size of p of x", FadeIn(size[:4]))
        self.cue("Past square root of three", FadeIn(size[4]))
        self.cue("Call it the size factor", Create(box), FadeIn(box_l))
        self.hold()
        f20, f23 = (2.0 ** 2 - 3) / 2, (2.3 ** 2 - 3) / 2
        assert f20 == 0.5 and abs(2.0 * f20 - abs(p(2.0))) < 1e-12 and abs(2.3 * f23 - abs(p(2.3))) < 1e-12
        assert num(f23) == "1.14"
        rows = VGroup(mt(r"x=2.0:\quad\frac{4-3}{2}=0.5<1\quad\text{shrinks}", 32, C_ZERO),
                      mt(r"x=2.3:\quad\frac{5.29-3}{2}\approx" + num(f23) + r">1\quad\text{grows}", 32, C_S5))
        rows.arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(size, DOWN, buff=0.5)
        self.say("Check it with the starts we tried. At two point zero, the factor is four minus three, over "
                 "two, which is one half. And two did go to size one. At two point three, the factor is about "
                 "one point one four, and two point three did come out bigger. So a factor below one means "
                 "flip and shrink. A factor above one means flip and grow.", FadeIn(rows[0][0][:15]))
        self.cue("And two did go", FadeIn(rows[0][0][15:]))
        self.cue("At two point three", FadeIn(rows[1][0][:19]))
        self.cue("and two point three did come out", FadeIn(rows[1][0][19:]))
        self.hold()
        eqm = mt(r"\frac{x^2-3}{2}=1\iff x^2=5", 36, C_S5).next_to(size, DOWN, buff=0.5)
        s5 = Line(ax.c2p(S5, -0.08), ax.c2p(S5, 0.08), color=C_S5, stroke_width=4)
        s5l = mt(r"\sqrt5", 30, C_S5).next_to(s5, UP, buff=0.1)
        self.say("The turning point is where the factor is exactly one. That means x squared minus three "
                 "equals two, so x squared equals five. The turning point is square root of five, about two "
                 "point two four, and it does sit between two point zero and two point three. On the curve, "
                 "between square root of three and square root of five a step shrinks the size, and beyond "
                 "square root of five it grows.", FadeOut(rows), FadeIn(eqm))
        self.cue("The turning point is square root of five", Create(s5), FadeIn(s5l))
        self.cue("On the curve", Create(shrink))
        self.cue("and beyond square root of five", Create(grow))
        self.hold(1.0)

        pts = [ax.c2p(S5, 0)]
        x = S5
        for _ in range(4):
            y = p(x)
            pts += [ax.c2p(x, y), ax.c2p(y, y)]
            x = y
        sq = VGroup(*[Line(a, b, color=C_S5, stroke_width=3.5) for a, b in zip(pts, pts[1:])])
        at5 = mt(r"p(\sqrt5)=\tfrac{\sqrt5}{2}\,(3-5)=-\sqrt5", 34, C_S5).next_to(eqm, DOWN, buff=0.4)
        self.say("What happens exactly at square root of five? Use the factored form. x over two, times three "
                 "minus five, is minus x. So square root of five goes to minus square root of five. By the "
                 "mirror rule, that goes straight back to plus square root of five. On the picture, the path "
                 "becomes a square.", FadeOut(VGroup(shrink, grow)))
        self.cue("x over two, times three minus five", FadeIn(at5))
        self.cue("So square root of five goes to", self.draw(sq[:2], 0.5))
        self.cue("that goes straight back", self.draw(sq[2:5], 0.5))
        self.hold()
        per = txt("period-2 orbit", 26, C_S5).next_to(at5, DOWN, buff=0.35)
        self.say("So square root of five neither settles nor explodes. It jumps back and forth between plus "
                 "and minus square root of five forever. This is called a period two orbit, because it repeats"
                 " every two steps.", self.draw(sq[5:], 0.4))
        self.cue("This is called a period two orbit", FadeIn(per))
        self.hold(1.0)
        o = orbit(2.3, 3)
        assert [num(o[1]), num(o[2]), num(o[3], 1)] == ["-2.63", "5.18", "-61.8"]
        seq = mt(r"\to ".join(num(v, 2 if abs(v) < 10 else 1) for v in o) + r"\to\cdots", 34, C_S5)
        seq.next_to(per, DOWN, buff=0.45)
        if seq.width > 6.2:
            seq.scale_to_fit_width(6.2)
        self.say("And past square root of five, every step flips and grows. Two point three goes to minus two "
                 "point six three, then five point one eight, then minus sixty one point eight. Like three, it"
                 " explodes.", FadeOut(sq))
        self.cue("Two point three goes to", FadeIn(seq))
        self.hold(0.5)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 8. the gap between √3 and √5
    def gap_marks(self, ax):
        m = VGroup()
        for v, c in ((S3, C_ZERO), (S5, C_S5)):
            m.add(Line(ax.c2p(v, -0.08), ax.c2p(v, 0.08), color=c, stroke_width=4))
        m.add(mt(r"\sqrt3", 30, C_ZERO).move_to(ax.c2p(S3 - 0.3, 0.25)))
        m.add(mt(r"\sqrt5", 30, C_S5).next_to(m[1], UP, buff=0.1))
        return m

    def the_gap(self):
        g = self.make_graph()
        ax = self.ax
        marks = self.gap_marks(ax)
        gapseg = Line(ax.c2p(S3, 0), ax.c2p(S5, 0), color=C_ZERO, stroke_width=9)
        self.play(FadeIn(g), FadeIn(marks))
        factor = mt(r"|p(x)|=|x|\cdot\frac{x^2-3}{2}", 36).move_to([PANEL_X, 2.4, 0])
        small = mt(r"\sqrt3<x<\sqrt5:\quad\frac{x^2-3}{2}<1", 32, C_ZERO).next_to(factor, DOWN, buff=0.35)
        self.say("So below square root of three, everything goes to one, and beyond square root of five, "
                 "everything explodes. That leaves the gap between them. In the gap, every step flips the sign. "
                 "And the size factor is below one, so every step also makes the size smaller.",
                 Create(gapseg))
        self.cue("And the size factor", FadeIn(factor), FadeIn(small))
        self.hold()

        # the hope: shrink until it is inside √3, where everything is known
        pos_in = Line(ax.c2p(0, 0), ax.c2p(S3, 0), color=C_PLUS, stroke_width=9)
        neg_in = Line(ax.c2p(-S3, 0), ax.c2p(0, 0), color=C_MINUS, stroke_width=9)
        known = VGroup(mt(r"\text{inside: }|x|<\sqrt3", 32), mt(r"x>0\ \ \to\ \ +1", 32, C_PLUS),
                       mt(r"x<0\ \ \to\ \ -1", 32, C_MINUS)).arrange(DOWN, buff=0.22)
        known.next_to(small, DOWN, buff=0.6)
        self.say("That suggests a plan. If the size keeps getting smaller, then sooner or later it drops below "
                 "square root of three. And inside square root of three we already know everything. A positive "
                 "value goes to plus one. By the mirror rule, a negative value goes to minus one. So we only "
                 "have to follow a start until it gets inside, and see on which side it arrives.")
        self.cue("And inside square root of three", FadeIn(known[0]))
        self.cue("A positive value", Create(pos_in), FadeIn(known[1]))
        self.cue("By the mirror rule", Create(neg_in), FadeIn(known[2]))
        self.hold()
        self.play(FadeOut(VGroup(factor, small, known)))

        # three starts on the cobweb picture
        def trial(x0, d, y, terms, verdict, color):
            parts = VGroup(*[mt(t, 32) for t in terms]).arrange(RIGHT, buff=0.18)
            parts.move_to([PANEL_X, y, 0])
            v = txt(verdict, 24, color).next_to(parts, DOWN, buff=0.16)
            return Dot(self.ax.c2p(x0, 0), radius=0.07, color=WHITE), parts, v

        o = orbit(2.0, 1)
        assert o[1] == -1.0
        w1 = self.web(2.0, 3, C_MINUS)
        m1, c1, v1 = trial(2.0, 1, 2.5, ["2.0", r"\to\ -1"], "1 flip, ends at −1", C_MINUS)
        self.say("Try it on the cobweb picture. Start at two point zero. Go down to the curve, which gives "
                 "minus one. Then across to the diagonal. Minus one is inside, on the negative side, and it "
                 "is already a fixed point. So two point zero ends at minus one, after one flip.",
                 FadeIn(m1), FadeIn(c1[0]))
        self.cue("Go down to the curve", Create(w1[0]), FadeIn(c1[1]))
        self.cue("Then across to the diagonal", Create(w1[1]))
        self.cue("So two point zero ends", FadeIn(v1))
        self.hold()

        o = orbit(2.2, 3)
        assert o[1] < -S3 and 0 < o[2] < S3
        w2 = self.web(2.2, 8, WHITE)
        m2, c2, v2 = trial(2.2, 1, 1.35, ["2.2", r"\to\ " + num(o[1]), r"\to\ +" + num(o[2]),
                                          r"\to\cdots\to\ +1"], "2 flips, ends at +1", C_PLUS)
        self.say("Now two point two. Down to the curve, at minus two point zero two. That is smaller in size "
                 "than two point two, but it is still outside. So go across to the diagonal and step again. "
                 "This time the curve sends it up, to plus one point one one. Now it is inside, on the positive "
                 "side, and from there it settles at plus one. Two flips, and a different ending.",
                 FadeOut(w1), FadeOut(m1), FadeIn(m2), FadeIn(c2[0]))
        self.cue("Down to the curve", Create(w2[0]), FadeIn(c2[1]))
        self.cue("So go across to the diagonal", Create(w2[1]))
        self.cue("This time the curve sends it up", Create(w2[2]), FadeIn(c2[2]))
        self.cue("Now it is inside", self.draw(w2[3:], 0.3), FadeIn(c2[3]))
        self.cue("Two flips", FadeIn(v2))
        self.hold()

        o = orbit(2.23, 3)
        assert o[1] < -S3 and o[2] > S3 and -S3 < o[3] < 0
        w3 = self.web(2.23, 10, C_MINUS)
        m3, c3, v3 = trial(2.23, 2, 0.2, ["2.23", r"\to\ " + num(o[1]), r"\to\ +" + num(o[2]),
                                          r"\to\ " + num(o[3]), r"\to\cdots\to\ -1"],
                           "3 flips, ends at −1", C_MINUS)
        if c3.width > 6.0:
            c3.scale_to_fit_width(6.0)
        self.say("And two point two three, just a little further out. Minus two point two zero. Then plus two "
                 "point zero two. Then minus one point one zero. It takes three flips to get inside, it arrives "
                 "on the negative side, and it ends at minus one.",
                 FadeOut(w2), FadeOut(m2), FadeIn(m3), FadeIn(c3[0]))
        self.cue("Minus two point two zero", self.draw(w3[:2], 0.4), FadeIn(c3[1]))
        self.cue("Then plus two", self.draw(w3[2:4], 0.4), FadeIn(c3[2]))
        self.cue("Then minus one point one zero", self.draw(w3[4:6], 0.4), FadeIn(c3[3]))
        self.cue("It takes three flips", self.draw(w3[6:], 0.3), FadeIn(c3[4]), FadeIn(v3))
        self.hold()

        rule = VGroup(txt("odd number of flips: arrives negative, ends at −1", 24, C_MINUS),
                      txt("even number of flips: arrives positive, ends at +1", 24, C_PLUS))
        rule.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([PANEL_X, -1.6, 0])
        if rule.width > 6.2:
            rule.scale_to_fit_width(6.2)
        self.say("So the starts in the gap do not all end the same way. What matters is how many flips it "
                 "takes to get inside. Every start here is positive, and each flip changes the sign. After an "
                 "odd number of flips the value arrives negative, and ends at minus one. After an even number "
                 "it arrives positive, and ends at plus one.", FadeOut(w3), FadeOut(m3))
        self.cue("After an odd number", FadeIn(rule[0]))
        self.cue("After an even number", FadeIn(rule[1]))
        self.hold()
        self.clear_stage(self.corner)

        # the whole picture: color every start by its fate
        ov = NumberLine(x_range=[0, 2.4, 0.5], length=9.0, color=GREY_B, stroke_width=2,
                        include_tip=False, tick_size=0.04).move_to([-0.2, 0.4, 0])
        ovl = VGroup(mt(r"\sqrt3", 28, C_ZERO).next_to(ov.n2p(S3), DOWN, buff=0.35),
                     mt(r"\sqrt5", 28, C_S5).next_to(ov.n2p(S5), DOWN, buff=0.35),
                     mt(r"1", 28, C_PLUS).next_to(ov.n2p(1), DOWN, buff=0.35),
                     mt(r"0", 28, GREY_B).next_to(ov.n2p(0), DOWN, buff=0.35))

        def fcol(v):
            f = fate(v)[0]
            return C_S5 if f == "diverges" else (C_PLUS if f > 0 else (C_MINUS if f < 0 else C_ZERO))

        def colored(line, lo, hi, n, y):
            out, cols, i = VGroup(), [fcol(lo + (k + 0.5) * (hi - lo) / n) for k in range(n)], 0
            while i < n:
                j = i
                while j + 1 < n and cols[j + 1] == cols[i]:
                    j += 1
                a_ = line.n2p(lo + i * (hi - lo) / n)[0]
                b_ = line.n2p(lo + (j + 1) * (hi - lo) / n)[0]
                out.add(Rectangle(width=b_ - a_, height=0.5, stroke_width=0, fill_color=cols[i],
                                  fill_opacity=0.9).move_to([(a_ + b_) / 2, y, 0]))
                i = j + 1
            return out

        strip = colored(ov, 0, 2.4, 2400, 0.4)
        assert len(strip) >= 5, len(strip)
        legend = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.9),
                                 txt(t, 22, c)).arrange(RIGHT, buff=0.12)
                          for c, t in ((C_PLUS, "ends at +1"), (C_MINUS, "ends at −1"),
                                       (C_S5, "explodes"))]).arrange(RIGHT, buff=0.6).move_to([-0.2, 1.6, 0])
        self.say("Three starts are not the whole story, so here is every start at once. Take each start "
                 "from zero to two point four, run the iteration, and color it by where it ends. Teal means "
                 "plus one, gold means minus one, and red means it explodes.",
                 FadeIn(ov), FadeIn(ovl))
        self.cue("Teal means", FadeIn(legend))
        self.play(LaggedStart(*[FadeIn(r) for r in strip], lag_ratio=0.02), run_time=2.5)
        self.hold(1.0)
        lo_z, hi_z = 2.1, S5
        a0, b0 = ov.n2p(lo_z)[0], ov.n2p(hi_z)[0]
        focus = Rectangle(width=b0 - a0, height=0.8, color=YELLOW_D, stroke_width=3).move_to([(a0 + b0) / 2, 0.4, 0])
        Lz = NumberLine(x_range=[lo_z, hi_z, 0.05], length=9.0, include_tip=False).move_to([-0.2, -1.6, 0])
        mag = colored(Lz, lo_z, hi_z, 1500, -1.6)
        zl = VGroup(mt(num(lo_z, 1), 24, GREY_B).next_to(mag, DOWN, buff=0.15).align_to(mag, LEFT),
                    mt(r"\sqrt5", 24, C_S5).next_to(mag, DOWN, buff=0.15).align_to(mag, RIGHT))
        links = VGroup(Line(focus.get_corner(DL), mag.get_corner(UL), color=YELLOW_D, stroke_width=1.5),
                       Line(focus.get_corner(DR), mag.get_corner(UR), color=YELLOW_D, stroke_width=1.5))
        self.say("Below square root of three it is all teal, as we showed. The gap begins gold. That is where "
                 "two point zero sits, with its one flip. Then comes a thin teal stripe, which holds two point "
                 "two. And then more stripes, each thinner than the last, squeezed up against square root "
                 "of five.")
        self.cue("Then comes a thin teal stripe", Create(focus))
        self.cue("And then more stripes", Create(links), FadeIn(mag), FadeIn(zl))
        self.hold(1.5)
        self.say("So each stripe is a flip count. One flip, two flips, three flips, and so on. Two things are "
                 "still open. Where exactly does one flip turn into two, and two into three? And do these "
                 "stripes really fill the whole gap, all the way up to square root of five?")
        self.hold(0.5)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 9. sizes only: the folded curve, and b1
    def gap_picture(self, close=False):
        """Sizes in the gap: y = |p(x)| and y = x (not to scale: x is stretched).
        close=True is the corner next to √5, where the edges pile up."""
        lo, hi, ylo, top = (2.05, 2.26, 1.6, 2.3) if close else (1.65, 2.3, 0.0, 2.5)
        ax = Axes(x_range=[lo, hi, 0.05], y_range=[ylo, top, 0.1 if close else 0.5], x_length=5.8, y_length=5.0,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2, "tick_size": 0.04})
        ax.move_to([-3.3, 0.25, 0])
        xs, ys = ((2.1, 2.2), (1.8, 2.0, 2.2)) if close else ((1.8, 2.0), (1, 2))
        nums = VGroup(*[mono(str(v), 18, GREY_B).next_to(ax.c2p(v, ylo), DOWN, buff=0.14) for v in xs],
                      *[mono(str(v), 18, GREY_B).next_to(ax.c2p(lo, v), LEFT, buff=0.12) for v in ys])
        x0 = max(S3, _root(-(ylo + 0.001), S3, 2.5))
        x1 = min(_root(-(top - 0.02), S3, 2.5), hi)
        curve = ax.plot(lambda x: abs(p(x)), x_range=[x0, x1], color=C_P, stroke_width=4)
        d0, d1 = max(lo, ylo), min(hi, top)
        diag = Line(ax.c2p(d0, d0), ax.c2p(d1, d1), color=C_DIAG, stroke_width=2.5)
        lab_c = mt(r"\text{size after one step}", 26, C_P).move_to(ax.c2p(*((2.2, 1.68) if close else (1.82, 1.0))))
        lab_d = mt(r"\text{same size}", 26, C_DIAG).move_to(ax.c2p(*((2.09, 2.2) if close else (1.9, 2.42))))
        s3 = VGroup() if close else VGroup(
            Line(ax.c2p(S3, -0.05), ax.c2p(S3, 0.05), color=C_ZERO, stroke_width=4),
            mt(r"\sqrt3", 26, C_ZERO).next_to(ax.c2p(S3, 0), DOWN, buff=0.14))
        xlab = txt("size of the start", 20, GREY_B).next_to(ax.c2p((lo + hi) / 2 - 0.02 * (hi - lo), ylo), DOWN,
                                                              buff=0.55)
        self.gx, self.gbox = ax, (lo, hi, ylo)
        return VGroup(ax, nums, curve, diag, lab_c, lab_d, s3, xlab)

    def level(self, v, color, label):
        ax, (lo, hi, _) = self.gx, self.gbox
        line = DashedLine(ax.c2p(lo, v), ax.c2p(hi, v), color=color, dash_length=0.08, stroke_width=2.5)
        return VGroup(line, mt(label, 26, color).next_to(line, RIGHT, buff=0.1))

    def edge(self, k, shift=ORIGIN):
        """b_k: where the folded curve reaches the height b_{k-1}."""
        ax, (_, _, ylo) = self.gx, self.gbox
        d = Dot(ax.c2p(B[k], B[k - 1]), radius=0.07, color=C_ZERO)
        drop = DashedLine(ax.c2p(B[k], B[k - 1]), ax.c2p(B[k], ylo), color=C_ZERO, dash_length=0.06)
        lab = mt(f"b_{{{k}}}", 26, C_ZERO).next_to(ax.c2p(B[k], ylo), DOWN, buff=0.14).shift(shift)
        return VGroup(d, drop, lab)

    def stripe(self, k):
        ax, (lo, _, ylo) = self.gx, self.gbox
        return Line(ax.c2p(max(B[k - 1], lo), ylo), ax.c2p(max(B[k], lo), ylo),
                    color=C_MINUS if k % 2 else C_PLUS, stroke_width=10)

    def first_boundary(self):
        g = self.make_graph()
        ax = self.ax
        marks = self.gap_marks(ax)
        self.play(FadeIn(g), FadeIn(marks))
        twin = VGroup(mt(r"p(-x)=-p(x)", 36), mt(r"\text{size: }\ |x|\ \to\ |p(x)|", 34, C_P),
                      txt("sign: one flip for each step from outside √3", 22, C_ZERO))
        twin.arrange(DOWN, buff=0.35).move_to([PANEL_X, 1.8, 0])
        self.say("Following the sign and the size together on this picture gets messy. But the mirror rule "
                 "lets us take them apart. A negative value moves exactly like its positive twin, with the sign "
                 "flipped. So the size follows a rule of its own. The next size is the size of p of x. And the "
                 "sign we can simply count. Every step that starts outside square root of three is one flip.",
                 FadeIn(twin[0]))
        self.cue("So the size follows", FadeIn(twin[1]))
        self.cue("And the sign we can simply count", FadeIn(twin[2]))
        self.hold()

        # fold the part below the axis up: y = |p(x)|
        xq = _root(-2.45, S5, 2.5)
        fold = ax.plot(p, x_range=[S3, xq], color=C_P, stroke_width=4)
        up = ax.plot(lambda x: abs(p(x)), x_range=[S3, xq], color=C_P, stroke_width=4)
        keep = ax.plot(p, x_range=[0, S3], color=C_P, stroke_width=4)
        self.say("So fold the picture. We only need positive sizes, so look at the right half. Wherever the "
                 "curve dips below the axis, flip that part up. This folded curve answers one question. "
                 "If the size is x now, what is the size after one step?",
                 FadeOut(twin), self.curve.animate.set_stroke(opacity=0.2), FadeIn(keep), FadeIn(fold))
        self.cue("flip that part up", Transform(fold, up), run_time=2.0)
        self.hold()

        shrink = ax.plot(lambda x: abs(p(x)), x_range=[S3, S5], color=C_ZERO, stroke_width=7)
        grow = ax.plot(lambda x: abs(p(x)), x_range=[S5, xq], color=C_S5, stroke_width=7)
        meet = Dot(ax.c2p(S5, S5), radius=0.08, color=C_S5)
        cmp_ = VGroup(mt(r"\text{below the diagonal: }|p(x)|<|x|", 30, C_ZERO),
                      mt(r"\text{above the diagonal: }|p(x)|>|x|", 30, C_S5))
        cmp_.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([PANEL_X, 2.2, 0])
        self.say("Now compare it with the diagonal, where the size would stay the same. Between square root "
                 "of three and square root of five, the folded curve is below the diagonal. The size after "
                 "the step is smaller than the size before. Beyond square root of five it is above the "
                 "diagonal, and the size grows. They meet exactly at square root of five.")
        self.cue("Between square root of three", Create(shrink), FadeIn(cmp_[0]))
        self.cue("Beyond square root of five", Create(grow), FadeIn(cmp_[1]))
        self.cue("They meet exactly", GrowFromCenter(meet), Flash(meet, color=C_S5))
        self.hold()

        o = orbit(2.2, 3)
        wf = self.web(2.2, 6, WHITE, f=lambda x: abs(p(x)))
        mf = Dot(ax.c2p(2.2, 0), radius=0.07, color=WHITE)
        sizes = mt(r"2.2\ \to\ " + num(-o[1]) + r"\ \to\ " + num(o[2]) + r"\ \to\ \cdots\ \to\ 1", 34)
        sizes.next_to(cmp_, DOWN, buff=0.6)
        count = txt("two steps start outside √3: two flips", 24, C_PLUS).next_to(sizes, DOWN, buff=0.25)
        self.say("And the cobweb works on the folded picture too. Start at two point two. Up to the folded "
                 "curve, at two point zero two. Across to the diagonal, and then to the curve again, at one "
                 "point one one. Now we are inside, and the size climbs to one. Two of these steps started "
                 "outside square root of three. So two flips, and the sign ends up positive.",
                 FadeOut(grow), FadeIn(mf), FadeIn(sizes[0][:3]))
        self.cue("Up to the folded curve", Create(wf[0]), FadeIn(sizes[0][3:8]))
        self.cue("Across to the diagonal", self.draw(wf[1:3], 0.5), FadeIn(sizes[0][8:13]))
        self.cue("Now we are inside", self.draw(wf[3:], 0.3), FadeIn(sizes[0][13:]))
        self.cue("Two of these steps", FadeIn(count))
        self.hold()
        self.clear_stage(self.corner)

        # zoom in on the gap: where does one flip become two?
        pic = self.gap_picture()
        gx = self.gx
        lvl = self.level(S3, C_ZERO, r"\sqrt3")
        lvl_l = lvl[1]
        e1 = self.edge(1)
        st1 = self.stripe(1)
        land = Line(gx.c2p(1.65, 0), gx.c2p(1.65, S3), color=C_MINUS, stroke_width=10)
        defn = mt(r"|p(b_1)|=\sqrt3", 38, C_ZERO).move_to([PANEL_X, 2.5, 0])
        first = txt("first stripe: one flip, ends at −1", 24, C_MINUS).next_to(defn, DOWN, buff=0.3)
        self.say("Now zoom in on the gap, and stretch it sideways so we can see. When does a start need "
                 "exactly one flip? When its first step already lands inside, at a size below square root of "
                 "three. So draw that level as a horizontal line. The folded curve climbs through it at one "
                 "point. Call that start b one, b for boundary. A start to the left of b one lands below the "
                 "line. One flip, and it is inside, on the negative side, so it ends at minus one. This is the "
                 "first stripe.", FadeIn(pic))
        self.cue("So draw that level", Create(lvl[0]), FadeIn(lvl_l))
        self.cue("The folded curve climbs through it", GrowFromCenter(e1[0]), Create(e1[1]), FadeIn(e1[2]),
                 FadeIn(defn))
        self.cue("A start to the left of b one", Create(st1))
        self.play(TransformFromCopy(st1, land), run_time=1.2)
        self.cue("This is the first stripe", FadeIn(first))
        self.hold()

        target = 2 * S3
        tries = [(v, v ** 3 - 3 * v) for v in (2.1, 2.2)]
        assert tries[0][1] < target < tries[1][1]
        eq0 = mt(r"b\cdot\frac{b^2-3}{2}=\sqrt3", 34, C_ZERO).next_to(defn, DOWN, buff=0.4)
        eq = mt(r"b^3-3b=2\sqrt3\approx" + num(target), 34, C_ZERO).next_to(eq0, DOWN, buff=0.3)
        t1 = mt(r"b=2.1:\quad " + num(tries[0][1]) + r"\ \ \text{too small}", 30).next_to(eq, DOWN, buff=0.35)
        t2 = mt(r"b=2.2:\quad " + num(tries[1][1]) + r"\ \ \text{too big}", 30).next_to(t1, DOWN, buff=0.22)
        val = mt(r"b_1\approx" + num(B[1], 3), 38, C_ZERO).next_to(t2, DOWN, buff=0.4)
        self.say("Where is b one exactly? Its size after one step must be square root of three. With the size "
                 "factor, that is b, times b squared minus three, over two, equals square root of three. "
                 "Multiply by two, and we get b cubed, minus three b, equals two times square root of three, "
                 "which is about three point four six. This has no tidy answer, so try values. Two point one "
                 "gives two point nine six, which is too small. Two point two gives four point zero five, "
                 "which is too big. Closing in between them gives about two point one four eight.",
                 FadeOut(first))
        self.cue("With the size factor", FadeIn(eq0))
        self.cue("Multiply by two", FadeIn(eq))
        self.cue("Two point one gives", FadeIn(t1))
        self.cue("Two point two gives", FadeIn(t2))
        self.cue("Closing in", FadeIn(val), Flash(e1[0], color=C_ZERO))
        self.hold()

        chk = VGroup(*[Dot(gx.c2p(v, 0), radius=0.07, color=c)
                       for v, c in ((1.8, C_MINUS), (2.0, C_MINUS), (2.2, C_PLUS))])
        chk_l = mt("2.2", 24, C_PLUS).next_to(chk[2], UP, buff=0.12)
        order = mt(r"1.8,\ \ 2.0\ <\ b_1\ <\ 2.2", 36).move_to(eq)
        self.say("That fits what we saw. One point eight and two point zero are both below b one, in the first "
                 "stripe, and both ended at minus one. Two point two is above b one. Its first step did not "
                 "get inside, and it needed a second flip.",
                 FadeOut(VGroup(eq0, eq, t1, t2)), GrowFromCenter(chk[0]), GrowFromCenter(chk[1]),
                 FadeIn(order[0][:10]))
        self.cue("Two point two is above", GrowFromCenter(chk[2]), FadeIn(chk_l), FadeIn(order[0][10:]))
        self.hold(0.5)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 10. the alternating basins
    def basin_bar(self, lo, colored=True, n=12):
        X0, W, Y = -4.7, 11.3, 0.45
        span = S5 - lo

        def X(v):
            return X0 + (v - lo) / span * W

        bar = VGroup()
        rects, ticks, labels, fates = VGroup(), VGroup(), VGroup(), VGroup()
        for k in range(1, n + 1):
            a, b = max(B[k - 1], lo), max(B[k], lo)
            w = max(X(b) - X(a), 1e-4)
            c = (C_MINUS if k % 2 else C_PLUS) if colored else GREY_D
            r = Rectangle(width=w, height=0.62, stroke_width=0, fill_color=c, fill_opacity=0.75)
            r.move_to([(X(a) + X(b)) / 2, Y, 0])
            rects.add(r)
            f = mt("-1" if k % 2 else "+1", 30, BLACK).move_to(r)
            f.set_opacity(1 if (colored and w > 0.75) else 0)
            fates.add(f)
        for k in range(1, n + 1):
            x = X(B[k])
            gap = X(B[k + 1]) - x if k + 1 < len(B) else 0
            t = Line([x, Y - 0.36, 0], [x, Y + 0.36, 0], color=WHITE, stroke_width=2)
            t.set_opacity(1 if B[k] >= lo else 0)
            ticks.add(t)
            lab = mt(f"b_{{{k}}}", 28).next_to(t, DOWN, buff=0.12)
            lab.set_opacity(1 if (B[k] >= lo - 1e-12 and gap > 0.42) else 0)
            labels.add(lab)
        edge = Line([X(S5), Y - 0.5, 0], [X(S5), Y + 0.5, 0], color=C_S5, stroke_width=4)
        edge_l = mt(r"\sqrt5", 30, C_S5).next_to(edge, DOWN, buff=0.12)
        bar.add(rects, fates, ticks, labels, edge, edge_l)
        bar.rects, bar.fates, bar.X = rects, fates, X
        return bar

    def basins(self):
        pic = self.gap_picture()
        gx = self.gx
        lvl = self.level(S3, C_ZERO, r"\sqrt3")
        e1, st1 = self.edge(1), self.stripe(1)
        self.play(FadeIn(pic), FadeIn(lvl), FadeIn(e1), FadeIn(st1))

        def band(k):
            c = C_MINUS if k % 2 else C_PLUS
            r = Rectangle(width=gx.c2p(2.3, 0)[0] - gx.c2p(1.65, 0)[0],
                          height=gx.c2p(0, B[k])[1] - gx.c2p(0, B[k - 1])[1],
                          stroke_width=0, fill_color=c, fill_opacity=0.22)
            r.move_to([(gx.c2p(1.65, 0)[0] + gx.c2p(2.3, 0)[0]) / 2,
                       (gx.c2p(0, B[k])[1] + gx.c2p(0, B[k - 1])[1]) / 2, 0])
            side = Line(gx.c2p(1.65, B[k - 1]), gx.c2p(1.65, B[k]), color=c, stroke_width=10)
            return VGroup(r, side)

        band1 = band(1)
        idea = VGroup(txt("lands in stripe 1", 24, C_MINUS), txt("= one more flip to go", 24, C_MINUS))
        idea.arrange(DOWN, buff=0.15).move_to([PANEL_X, 2.5, 0])
        self.say("Now the starts above b one. Their first step does not get inside. But we do not have to "
                 "follow them all the way. Suppose the first step lands, in size, somewhere in the first stripe. "
                 "We already know the first stripe. From there it takes one more flip to get inside. So such a "
                 "start flips exactly twice.")
        self.cue("Suppose the first step lands", TransformFromCopy(st1, band1[1]), FadeIn(band1[0]),
                 FadeIn(idea[0]), run_time=1.5)
        self.cue("From there it takes one more flip", FadeIn(idea[1]))
        self.hold()

        e2, st2 = self.edge(2), self.stripe(2)
        lvl2 = self.level(B[1], C_ZERO, "b_1")
        d2 = mt(r"|p(b_2)|=b_1", 36, C_ZERO).next_to(idea, DOWN, buff=0.45)
        second = txt("second stripe: two flips, ends at +1", 24, C_PLUS).next_to(d2, DOWN, buff=0.3)
        self.say("Which starts are those? Read it off the picture. On the vertical axis, the first stripe is "
                 "the band of sizes from square root of three up to b one. The folded curve passes through "
                 "that band. It enters at b one, and it leaves at a new point, where its height is exactly "
                 "b one. Call that point b two. So every start between b one and b two lands in the first "
                 "stripe. Two flips, an even number, so it ends at plus one. This is the second stripe.")
        self.cue("and it leaves at a new point", FadeIn(lvl2), GrowFromCenter(e2[0]))
        self.cue("Call that point b two", Create(e2[1]), FadeIn(e2[2]), FadeIn(d2))
        self.cue("So every start between", Create(st2))
        self.cue("This is the second stripe", FadeIn(second))
        self.hold()

        y22 = abs(p(2.2))
        assert S3 < y22 < B[1] and B[1] < 2.2 < B[2]
        dot22 = Dot(gx.c2p(2.2, y22), radius=0.07, color=WHITE)
        path22 = VGroup(DashedLine(gx.c2p(2.2, 0), gx.c2p(2.2, y22), color=WHITE, dash_length=0.06),
                        DashedLine(gx.c2p(2.2, y22), gx.c2p(1.65, y22), color=WHITE, dash_length=0.06))
        ex = mt(r"2.2\ \to\ \text{size }" + num(y22) + r"\qquad\sqrt3<" + num(y22) + r"<b_1", 30)
        ex.next_to(second, DOWN, buff=0.45)
        self.say("Check it with two point two. It sits between b one and b two. Its first step has size two "
                 "point zero two. And two point zero two lies between square root of three and b one, in the "
                 "first stripe. So one more flip, and it is inside. That is the two flips we counted, and it "
                 "ended at plus one.")
        self.cue("Its first step has size", Create(path22[0]), GrowFromCenter(dot22))
        self.cue("And two point zero two lies", Create(path22[1]), FadeIn(ex))
        self.hold()

        band2 = band(2)
        e3, st3 = self.edge(3, shift=DOWN * 0.38 + RIGHT * 0.1), self.stripe(3)
        d3 = mt(r"|p(b_3)|=b_2", 36, C_ZERO).move_to(d2)
        third = txt("third stripe: three flips, ends at −1", 24, C_MINUS).move_to(second)
        self.say("And the same step works again. Starts that land in the second stripe need one flip more "
                 "than the second stripe does, so three flips. The curve leaves that band where its height is "
                 "b two. Call that point b three. The starts between b two and b three are the third stripe, "
                 "and they end at minus one. Each new stripe is carried onto the stripe before it, so it "
                 "needs exactly one more flip.",
                 FadeOut(VGroup(dot22, path22, ex, idea)), FadeOut(band1[0]))
        self.cue("Starts that land in the second stripe", TransformFromCopy(st2, band2[1]), FadeIn(band2[0]),
                 run_time=1.5)
        self.cue("Call that point b three", GrowFromCenter(e3[0]), Create(e3[1]), FadeIn(e3[2]),
                 Transform(d2, d3))
        self.cue("The starts between b two and b three", Create(st3), Transform(second, third))
        self.hold()

        vals = VGroup(*[mt(f"b_{{{k}}}\\approx{B[k]:.3f}", 34, C_ZERO) for k in (1, 2, 3)],
                      mt(r"\sqrt5\approx" + num(S5, 3), 34, C_S5)).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        vals.move_to([PANEL_X, 0.2, 0])
        self.say("Each edge is found like b one, by trying values. b one is about two point one four eight. "
                 "b two is about two point two two one. b three is about two point two three four. They creep "
                 "up toward square root of five, which is two point two three six.",
                 FadeOut(d2), FadeOut(second), FadeIn(vals[0]))
        self.cue("b two is about", FadeIn(vals[1]))
        self.cue("b three is about", FadeIn(vals[2]))
        self.cue("They creep up", FadeIn(vals[3]))
        self.hold()
        self.clear_stage(self.corner)

        # all the stripes on one bar, then zoom towards √5
        live = self.basin_bar(S3)
        s3l = mt(r"\sqrt3", 30, C_ZERO).next_to([live.X(S3), 0.45 - 0.31, 0], DOWN, buff=0.18)
        rule = VGroup(txt("stripe n:  n flips", 28), txt("odd n: ends at −1", 28, C_MINUS),
                      txt("even n: ends at +1", 28, C_PLUS)).arrange(RIGHT, buff=0.7).move_to([0, -1.2, 0])
        if rule.width > 11.5:
            rule.scale_to_fit_width(11.5)
        self.say("So here are all the stripes on one line. Stripe number n flips n times. An odd n ends at "
                 "minus one, and an even n ends at plus one. That is the striped picture we saw.",
                 FadeIn(live), FadeIn(s3l))
        self.cue("Stripe number n", FadeIn(rule[0]))
        self.cue("An odd n", FadeIn(rule[1]), FadeIn(rule[2]))
        self.hold()
        t = ValueTracker(0.0)
        zoomed = always_redraw(lambda: self.basin_bar(S5 - (S5 - S3) * 6 ** (-t.get_value())))
        self.remove(live)
        self.add(zoomed)
        self.say("The stripes pile up against square root of five. Zoom in, and the same pattern shows up "
                 "again and again.", FadeOut(s3l), FadeOut(rule))
        self.play(t.animate.set_value(2.0), run_time=6.0, rate_func=smooth)
        zoomed.clear_updaters()
        self.hold()
        ya, yb = p(2.2), p(2.23)
        assert 5.5 < (ya - yb) / 0.03 < 6.5
        pair = mt(r"2.20\ \to\ \text{size }" + num(-ya) + r",\qquad 2.23\ \to\ \text{size }" + num(-yb), 34)
        moved = mt(r"\text{in: }0.03\qquad\text{out: }" + num(ya - yb) + r"\ \approx\ 6\times0.03", 34, C_S5)
        sixth = mt(r"\text{each stripe}\ \approx\ \tfrac16\ \text{of the one before}", 34)
        sr = VGroup(pair, moved, sixth).arrange(DOWN, buff=0.3).move_to([0, -1.9, 0])
        assert abs((S5 - B[5]) / (S5 - B[6]) - 6) < 0.05
        self.say("Why do the stripes get thin so quickly? Near square root of five the folded curve is steep. "
                 "From two point two to two point two three, the start moves by zero point zero three. But "
                 "the size after the step moves from two point zero two to two point two zero, which is zero "
                 "point one eight. That is six times as far. So one step stretches a stripe to six times its "
                 "width. And the stretched stripe has to fit exactly onto the stripe before it. So each stripe "
                 "is only about a sixth as wide as the one before.")
        self.cue("From two point two to", FadeIn(pair))
        self.cue("That is six times as far", FadeIn(moved))
        self.cue("So each stripe is only", FadeIn(sixth))
        self.hold(0.5)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 11. do the stripes cover the gap? and the edges
    def boundary_points(self):
        pic = self.gap_picture(close=True)
        gx = self.gx
        sts = VGroup(*[self.stripe(k) for k in range(1, 8)])
        self.play(FadeIn(pic), FadeIn(sts))
        # the edges as a staircase between the folded curve and the diagonal
        pts = [gx.c2p(self.gbox[0], S3)]
        for k in range(1, 9):
            pts += [gx.c2p(B[k], B[k - 1]), gx.c2p(B[k], B[k])]
        stair = VGroup(*[Line(a, b, color=C_ZERO, stroke_width=3) for a, b in zip(pts, pts[1:])])
        labs = VGroup(mt(r"b_1", 26, C_ZERO).next_to(gx.c2p(B[1], S3), DOWN, buff=0.1),
                      mt(r"b_2", 26, C_ZERO).next_to(gx.c2p(B[2], B[1]), RIGHT, buff=0.1))
        q = txt("is there a piece next to √5 that no stripe reaches?", 24).move_to([PANEL_X, 2.5, 0])
        if q.width > 6.2:
            q.scale_to_fit_width(6.2)
        self.say("One question is still open. Do the stripes really fill the whole gap? Or is there a last "
                 "piece, right next to square root of five, that no stripe ever reaches? Look at how we found "
                 "the edges. Here is the corner of the picture next to square root of five. Start at the "
                 "height square root of three, and go across to the folded curve. That is b one. Go up to the "
                 "diagonal, and across to the curve again. That is b two. The edges are a staircase, squeezed "
                 "between the curve and the diagonal.", FadeIn(q))
        self.cue("and go across to the folded curve", Create(stair[0]), FadeIn(labs[0]))
        self.cue("Go up to the diagonal", Create(stair[1]), Create(stair[2]), FadeIn(labs[1]))
        self.cue("The edges are a staircase", self.draw(stair[3:], 0.3))
        self.hold()

        top = Dot(gx.c2p(S5, S5), radius=0.08, color=C_S5)
        top_l = mt(r"\sqrt5", 28, C_S5).next_to(top, RIGHT, buff=0.12)
        why = VGroup(txt("the edges increase, and stay below √5", 24),
                     txt("so they close in on one point", 24),
                     txt("there the curve meets the diagonal: only at √5", 24, C_S5))
        why.arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(q, DOWN, buff=0.5)
        if why.width > 6.2:
            why.scale_to_fit_width(6.2)
        self.say("Every step of the staircase moves to the right, and it can never get past square root of "
                 "five. So the edges close in on some point. At that point the staircase has no room left, "
                 "which means the curve touches the diagonal there. And in the gap, the only place where the "
                 "curve touches the diagonal is square root of five itself. So the edges come as close to "
                 "square root of five as we like. Every start below square root of five is passed by some "
                 "edge, so it lies in some stripe. The stripes fill the whole gap.", FadeIn(why[0]))
        self.cue("So the edges close in", FadeIn(why[1]))
        self.cue("And in the gap, the only place", FadeIn(why[2]), GrowFromCenter(top), FadeIn(top_l))
        self.cue("The stripes fill the whole gap", Indicate(sts, color=WHITE, scale_factor=1.0))
        self.hold()
        self.clear_stage(self.corner)

        # the edges themselves: ±√3 after a few steps, then 0
        rows, dots, names, chains = VGroup(), VGroup(), VGroup(), VGroup()
        paths = []
        for i, n in enumerate((1, 2, 3)):
            row = self.number_row(1.7 - 1.55 * i, lo=-2.4, hi=2.4, length=7.4, x=-1.3, marks=(0,))
            nl = row[0]
            for v in (S3, -S3):
                row.add(Line(nl.n2p(v) + DOWN * 0.1, nl.n2p(v) + UP * 0.1, color=C_ZERO, stroke_width=4))
                row.add(mt(r"\sqrt3" if v > 0 else r"-\sqrt3", 22, C_ZERO).next_to(nl.n2p(v), DOWN, buff=0.14))
            rows.add(row)
            names.add(mt(f"b_{{{n}}}", 34, C_ZERO).next_to(nl, LEFT, buff=0.35))
            path = [(+1, n)]
            s = 1
            for k in range(n - 1, -1, -1):
                s = -s
                path.append((s, k))
            vals = [sg * B[k] for sg, k in path] + [0.0]
            assert all(abs(p(a) - b) < 1e-9 for a, b in zip(vals, vals[1:]))
            paths.append(vals)
            terms = [("-" if sg < 0 else "") + (r"\sqrt3" if k == 0 else f"b_{{{k}}}") for sg, k in path] + ["0"]
            chains.add(mt(r"\to ".join(terms), 24, C_ZERO).next_to(nl, RIGHT, buff=0.3))
            dots.add(Dot(nl.n2p(vals[0]), radius=0.09, color=C_ZERO))
        self.say("And what about the edges themselves? Take b one. Its first step lands exactly on minus "
                 "square root of three. And we know what happens at square root of three. The next step gives "
                 "exactly zero, and by the mirror rule the same holds for minus square root of three. So b one "
                 "ends on zero, and stays there.",
                 FadeIn(rows[0]), FadeIn(names[0]), GrowFromCenter(dots[0]))
        nl = rows[0][0]
        self.cue("Its first step lands", self.hop(dots[0], nl, paths[0][0], paths[0][1], C_ZERO), run_time=1.2)
        self.cue("The next step gives", self.hop(dots[0], nl, paths[0][1], paths[0][2], C_ZERO), run_time=1.2)
        self.cue("So b one ends on zero", FadeIn(chains[0]))
        self.hold()
        self.say("b two lands on minus b one, and from there it follows the path of b one with the sign "
                 "flipped. So it takes one step more. And b three takes one step more again. Every edge reaches "
                 "plus or minus square root of three after a few steps, and then it sits on zero forever. "
                 "An edge never reaches one or minus one.",
                 FadeIn(rows[1:]), FadeIn(names[1:]), *[GrowFromCenter(d) for d in dots[1:]])
        for j in range(max(len(q_) for q_ in paths[1:]) - 1):
            anims = []
            for i in (1, 2):
                if j + 1 < len(paths[i]):
                    anims.append(self.hop(dots[i], rows[i][0], paths[i][j], paths[i][j + 1], C_ZERO))
            self.play(*anims, run_time=1.2)
            self.wait(0.6)
        self.play(FadeIn(chains[1:]))
        self.hold()
        ends = [fate(B[1] - 0.01)[0], fate(B[1] + 0.01)[0]]
        assert sorted(ends) == [-1.0, 1.0]
        nudged = VGroup(*[Dot(nl.n2p(B[1] + dx), radius=0.07, color=sign_color(e))
                          for dx, e in zip((-0.01, 0.01), ends)])
        self.say("Should that worry us? Not much. Each edge is a single point, and zero is the top of the "
                 "hill. Move the start by the tiniest amount, and it is inside a stripe on one side or the "
                 "other, and it rolls down to plus one or minus one.")
        self.cue("Move the start by", FadeOut(dots[0]), *[GrowFromCenter(d) for d in nudged])
        self.play(*[d.animate(path_arc=0.5 * PI).move_to(nl.n2p(e)) for d, e in zip(nudged, ends)],
                  run_time=2.0)
        self.hold(0.5)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 12. the answer to (e)
    def summary(self):
        head = [txt("start σ", 26, GREY_B), txt("what happens", 26, GREY_B), txt("ends at", 26, GREY_B)]
        rows = [
            (mt(r"0<\sigma<\sqrt3", 34), txt("first step lands in (0, 1], then climbs", 26), mt(r"+1", 34, C_PLUS)),
            (mt(r"\sigma=\sqrt3", 34), txt("lands on 0 in one step", 26), mt(r"0", 34, C_ZERO)),
            (mt(r"b_{n-1}<\sigma<b_n", 34), txt("n flips while shrinking", 26), mt(r"(-1)^n", 34, YELLOW_D)),
            (mt(r"\sigma=b_n", 34), txt("hits ±√3, then 0", 26), mt(r"0", 34, C_ZERO)),
            (mt(r"\sigma=\sqrt5", 34), txt("jumps between ±√5", 26), txt("period 2", 26, C_S5)),
            (mt(r"\sigma>\sqrt5", 34), txt("flips while growing", 26), txt("explodes", 26, C_S5)),
        ]
        xs = (-3.9, 0.7, 4.6)
        table = VGroup()
        for r, cells in enumerate([head] + rows):
            y = 2.75 - 0.66 * r
            table.add(VGroup(*[c.move_to([x, y, 0]) for c, x in zip(cells, xs)]))
        rule = Line([-6.2, 2.42, 0], [6.2, 2.42, 0], color=GREY_C, stroke_width=1.5)
        bar = self.basin_bar(2.0, n=8).shift(DOWN * 2.75)
        self.say("Now we can answer the question we started with. Where does a positive sigma end up when we "
                 "apply p again and again? Here is the full answer to part (e), from left to right along the "
                 "number line.")
        self.cue("Here is the full answer", FadeIn(table[0]), Create(rule))
        self.hold()
        self.say("Below square root of three, the first step lands between zero and one, and from there sigma "
                 "climbs to plus one. Exactly at square root of three, it lands on zero and stays there.", FadeIn(table[1], shift=UP * 0.1))
        self.cue("Exactly at square root of three", FadeIn(table[2], shift=UP * 0.1))
        self.hold()
        self.say("Between square root of three and square root of five, each step flips the sign and shrinks "
                 "the size, until the value is inside square root of three. An odd number of flips ends at "
                 "minus one, and an even number ends at plus one. That gives the stripes. Their edges are "
                 "single points that end on zero.", FadeIn(table[3][:2], shift=UP * 0.1))
        self.cue("An odd number of flips", FadeIn(table[3][2]))
        self.cue("That gives the stripes", FadeIn(bar))
        self.cue("Their edges are single points", FadeIn(table[4], shift=UP * 0.1))
        self.hold()
        want = SurroundingRectangle(table[1], color=C_PLUS, buff=0.14, stroke_width=3)
        self.say("Exactly at square root of five, sigma jumps between plus and minus square root of five "
                 "forever. And beyond square root of five, each step flips and grows, so it explodes. Out of "
                 "all these cases, only the first one is what we wanted.", FadeIn(table[5], shift=UP * 0.1))
        self.cue("And beyond square root of five", FadeIn(table[6], shift=UP * 0.1))
        self.cue("only the first one is what we wanted", Create(want))
        self.hold(0.8)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 13. back to the matrix
    def back_to_matrix(self):
        sig0 = [2.9, 1.6, 0.9, 0.35]
        nl = NumberLine(x_range=[0, 3.2, 0.5], length=11.0, color=GREY_B, stroke_width=2,
                        include_tip=False, tick_size=0.04).move_to([0.3, -0.6, 0])
        marks = VGroup()
        for v, c, s in ((0, GREY_B, "0"), (1, C_PLUS, "1"), (S3, C_ZERO, r"\sqrt3"), (S5, C_S5, r"\sqrt5")):
            marks.add(Line(nl.n2p(v) + DOWN * 0.12, nl.n2p(v) + UP * 0.12, color=c, stroke_width=4))
            marks.add(mt(s, 28, c).next_to(nl.n2p(v), DOWN, buff=0.2))
        lab = mt(r"\sigma_i", 32, C_SIG).next_to(nl, LEFT, buff=0.3)
        dots = VGroup(*[Dot(nl.n2p(s), radius=0.1, color=C_SIG) for s in sig0])
        safe = Line(nl.n2p(0), nl.n2p(S3), color=C_PLUS, stroke_width=8).set_opacity(0.45)
        self.say("We wanted every singular value to end at one, and that only happens for starts below square "
                 "root of three. But a real W can have singular values anywhere, some of them far above square"
                 " root of five.", Create(nl), FadeIn(marks), FadeIn(lab))
        self.cue("that only happens for starts below", Create(safe))
        self.cue("But a real W can have", LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.3))
        self.hold()
        bad = SurroundingRectangle(dots[0], color=C_S5, buff=0.12)
        blow = mt(r"2.9\to" + num(p(2.9)) + r"\to\cdots", 32, C_S5).next_to(dots[0], UP, buff=0.35)
        sc = mt(r"\frac{W}{c}=U\,\frac{\Sigma}{c}\,V^{\top}", 44).move_to([0, 2.4, 0])
        same = txt("U and Vᵀ unchanged, every σ divided by c", 26, C_PLUS).next_to(sc, DOWN, buff=0.35)
        self.say("This one, at two point nine, would explode. And one that sits in a gold stripe would end at "
                 "minus one, with its direction reversed. So before we iterate, we have to bring every "
                 "singular value down. That is easy to do. Divide W by a number, and every singular value is "
                 "divided by that number, while U and V transpose stay exactly the same. Our target, U times V"
                 " transpose, does not change at all.", Create(bad), FadeIn(blow))
        self.cue("we have to bring every singular value down", FadeOut(VGroup(bad, blow)))
        self.cue("Divide W by a number", FadeIn(sc))
        self.cue("while U and V transpose stay", FadeIn(same))
        self.hold()

        fro = math.sqrt(sum(s * s for s in sig0))
        sig1 = [s / fro for s in sig0]
        assert max(sig1) < 1 < S3 and num(fro) == "3.45" and num(sig1[0]) == "0.84"
        ideal = mt(r"c=\sigma_{\max}\ ?\qquad\text{needs the SVD}", 36, C_S5).move_to([1.5, 2.5, 0])
        fdef = mt(r"\|W\|_F=\sqrt{\textstyle\sum_{i,j}w_{ij}^2}", 38).move_to([1.5, 2.5, 0])
        fsum = mt(r"\textstyle\sum_{i,j}w_{ij}^2=\sum_i\sigma_i^2\ \ge\ \sigma_{\max}^2", 36).move_to([1.5, 1.7, 0])
        fge = mt(r"\|W\|_F\ \ge\ \sigma_{\max}", 40, C_PLUS).move_to([1.5, 0.9, 0])
        self.say("Which number? Dividing by the largest singular value would be ideal, because then everything"
                 " is at one or below. But finding the largest singular value takes the very SVD we are trying"
                 " to avoid. There is a cheap stand-in, called the Frobenius norm. Square every entry of W, "
                 "add them all up, and take the square root. That only needs the entries, so it costs almost "
                 "nothing. And it is big enough. The sum of the squared entries always equals the sum of the "
                 "squared singular values. That sum already contains the largest one squared, plus more. So "
                 "its square root, the Frobenius norm, is never smaller than the largest singular value.", FadeOut(same), sc.animate.scale(0.8).move_to([-4.3, 2.6, 0]))
        self.cue("Dividing by the largest singular value", FadeIn(ideal[0][:7]))
        self.cue("But finding the largest singular value", FadeIn(ideal[0][7:]))
        self.cue("There is a cheap stand-in", FadeOut(ideal), FadeIn(fdef))
        self.cue("The sum of the squared entries always equals", FadeIn(fsum[0][:15]))
        self.cue("That sum already contains", FadeIn(fsum[0][15:]))
        self.cue("So its square root", FadeIn(fge))
        self.hold()
        fro_eq = mt(r"\|W\|_F=\sqrt{2.9^2+1.6^2+0.9^2+0.35^2}\approx" + num(fro), 36).move_to([1.5, 2.5, 0])
        self.say("Here the Frobenius norm comes out to about three point four five, a bit more than our "
                 "largest singular value, two point nine. Divide every sigma by it.", FadeOut(VGroup(fdef, fsum)), fge.animate.move_to([1.5, 1.6, 0]), FadeIn(fro_eq))
        self.hold()
        div = mt(r"2.9\,/\,3.45=0.84", 36, C_SIG).move_to([1.5, 0.8, 0])
        self.say("Two point nine becomes zero point eight four, and the others are smaller still. Now every "
                 "singular value sits between zero and one, safely below square root of three.", *[d.animate.move_to(nl.n2p(s)) for d, s in zip(dots, sig1)], FadeIn(div), run_time=2.0)
        self.hold()
        steps = 8
        orbs = [orbit(s, steps) for s in sig1]
        assert all(abs(o[-1] - 1) < 0.01 for o in orbs)
        step = mt(r"W\ \leftarrow\ \tfrac32\,W-\tfrac12\,W\,W^{\top}W", 44).move_to([0, 2.6, 0])
        each = mt(r"\sigma_i\ \leftarrow\ p(\sigma_i)", 38, C_SIG).next_to(step, DOWN, buff=0.35)
        k_lab = mt(r"k=0", 34).move_to([-4.6, 0.6, 0])
        res = mt(r"\Sigma\to I,\qquad W\to UV^{\top}", 42, C_PLUS).move_to([0, 0.9, 0])
        self.say("Now apply our matrix step, three halves W, minus one half W, W transpose, W, again and "
                 "again. It needs nothing but matrix products. And each time, every singular value goes "
                 "through p once. So each singular value climbs to plus one. The small ones start slowly, "
                 "growing by about one and a half times per step as zero point one did, but they all arrive. "
                 "And all along, U and V transpose never changed. So the middle is now all ones, and W has "
                 "become U times V transpose.", FadeOut(VGroup(sc, fro_eq, fge, div)), FadeIn(step))
        self.cue("And each time, every singular value", FadeIn(each), FadeIn(k_lab))
        self.cue("So each singular value climbs")
        for k in range(1, steps + 1):
            new_k = mt(f"k={k}", 34).move_to(k_lab, aligned_edge=LEFT)
            self.play(*[d.animate.move_to(nl.n2p(o[k])).set_color(C_PLUS if abs(o[k] - 1) < 0.02 else C_SIG)
                        for d, o in zip(dots, orbs)], Transform(k_lab, new_k), run_time=1.0)
        self.cue("So the middle is now all ones", FadeIn(res))
        self.hold()
        ell = Ellipse(width=3.4, height=1.3, color=C_SIG, stroke_width=4).rotate(30 * DEGREES).move_to([0, 1.6, 0])
        circ = Circle(radius=1.0, color=C_PLUS, stroke_width=4).move_to([0, 1.6, 0])
        self.say("The ellipse has become a circle. All it took was matrix products, and a cubic built from two"
                 " simple wishes.", FadeOut(VGroup(step, each, res, k_lab)), FadeIn(ell))
        self.play(Transform(ell, circ), run_time=2.0)
        self.hold(0.8)
# --- end of episode
