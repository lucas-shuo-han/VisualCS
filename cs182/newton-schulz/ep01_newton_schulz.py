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

    def construct(self):
        self.title_card()
        self.ellipse()
        self.why_p()
        self.try_numbers()
        self.cobweb()
        self.slopes()
        self.how_big()
        self.too_big()
        self.the_gap()
        self.first_boundary()
        self.basins()
        self.boundary_points()
        self.summary()
        self.back_to_matrix()
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

    def web(self, x0, n, color, width=3.0):
        ax = self.ax
        pts = [ax.c2p(x0, 0)]
        x = x0
        for _ in range(n):
            y = p(x)
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
        lab = mt(label or num(x0, 1), 26, color).next_to(d, DOWN, buff=0.42)
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

        s1, s2 = ValueTracker(1.0), ValueTracker(1.0)

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
        self.play(circ.animate.set_stroke(opacity=0.35), FadeIn(ell), run_time=0.6)
        self.say("It stretches one direction by σ1 and another by σ2: those are its singular values.",
                 s1.animate.set_value(1.3), s2.animate.set_value(0.5), run_time=1.8)

        def readout(tr, name):
            d = DecimalNumber(tr.get_value(), num_decimal_places=3, font_size=36, color=C_SIG)
            d.add_updater(lambda m: m.set_value(tr.get_value()))
            return VGroup(mt(name + "=", 36, C_SIG), d).arrange(RIGHT, buff=0.15)

        r1, r2 = readout(s1, r"\sigma_1"), readout(s2, r"\sigma_2")
        rd = VGroup(r1, r2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([PANEL_X, 0.1, 0])
        self.play(FadeIn(rd))
        ortho = txt("all σ = 1  ⇔  W is orthogonal", 28, C_PLUS).move_to([PANEL_X, -1.3, 0])
        self.say("If every stretch were exactly 1, the circle would stay a circle, and W would be orthogonal.",
                 FadeIn(ortho))
        self.hold()
        muon = txt("Muon: orthogonalize each update", 26, GREY_A).move_to([PANEL_X, -2.1, 0])
        self.say("Optimizers like Muon want this for every weight update: same directions, every stretch 1.", FadeIn(muon))
        self.hold()
        it = MathTex(r"W_{k+1}=\tfrac12\left(3I-W_kW_k^{\top}\right)W_k", font_size=38)
        it.move_to([PANEL_X, 2.3, 0])
        tag = txt("Newton–Schulz", 26, GREY_A).next_to(it, DOWN, buff=0.2)
        self.say("An SVD could do it, but it is slow on a GPU. The Newton–Schulz iteration uses only "
                 "matrix products.", FadeOut(VGroup(ortho, muon)), Write(it), FadeIn(tag))
        self.hold()

        k_lab = mt(r"k=0", 34).move_to([PANEL_X, -1.3, 0])
        self.say("Let's apply it a few times and watch the ellipse.", FadeIn(k_lab))
        a, b = 1.3, 0.5
        for k in range(1, 6):
            a, b = p(a), p(b)
            self.play(s1.animate.set_value(a), s2.animate.set_value(b),
                      Transform(k_lab, mt(f"k={k}", 34).move_to(k_lab)), run_time=1.0)
            self.wait(0.2)
        assert abs(a - 1) < 1e-3 and abs(b - 1) < 1e-3
        self.say("After a handful of steps, the ellipse is a circle. Why does this work? And can it fail?",
                 Flash(ell[0].get_center() + R * u1, color=C_PLUS))
        self.hold(0.5)
        ell.clear_updaters()
        for d in (r1[1], r2[1]):
            d.clear_updaters()
        self.clear_stage()

    # ------------------------------------------------------------ 2. one matrix step = p on each σ
    def why_p(self):
        it = MathTex(r"W_{k+1}", r"=", r"\tfrac12\left(3I-W_kW_k^{\top}\right)W_k", font_size=44)
        it.to_edge(UP, buff=0.7)
        svd = MathTex(r"W", r"=", r"U", r"\;\;\Sigma\;\;", r"V^{\top}", font_size=52)
        svd[3].set_color(C_SIG)
        svd.move_to(UP * 0.7)
        rot_u = txt("rotate", 22, GREY_B).next_to(svd[2], DOWN, buff=0.25)
        rot_v = txt("rotate", 22, GREY_B).next_to(svd[4], DOWN, buff=0.25)
        stretch = txt("stretch", 22, C_SIG).next_to(svd[3], DOWN, buff=0.7)
        self.say("To see why, write W with its SVD. U and V only rotate; all the stretching sits in Σ.",
                 FadeIn(it), Write(svd), FadeIn(VGroup(rot_u, rot_v, stretch), shift=UP * 0.1))

        d1 = MathTex(r"WW^{\top}", r"=U\Sigma V^{\top}V\Sigma U^{\top}", r"=U\Sigma^2U^{\top}", font_size=38)
        d2 = MathTex(r"W_{k+1}", r"=U\,\tfrac12\left(3I-\Sigma^2\right)\Sigma\,V^{\top}",
                     r"=U\,p(\Sigma)\,V^{\top}", font_size=38)
        VGroup(d1, d2).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 1.2)
        self.say("Plug it into the iteration. U and V pass through untouched; only the middle Σ changes.",
                 VGroup(rot_u, rot_v, stretch).animate.set_opacity(0), Write(d1), run_time=1.6)
        self.play(Write(d2), run_time=1.6)
        self.play(Circumscribe(d2[2], color=C_SIG))
        self.hold()
        self.remove(rot_u, rot_v, stretch)

        sig = Matrix([[r"\sigma_1", "0", "0"], ["0", r"\sigma_2", "0"], ["0", "0", r"\sigma_3"]],
                     h_buff=1.5).scale(0.8)
        psig = Matrix([[r"p(\sigma_1)", "0", "0"], ["0", r"p(\sigma_2)", "0"], ["0", "0", r"p(\sigma_3)"]],
                      h_buff=1.5).scale(0.8)
        for m in (sig, psig):
            for k in (0, 4, 8):
                m.get_entries()[k].set_color(C_SIG)
        lhs = mt(r"\Sigma=", 44, C_SIG)
        grp = VGroup(lhs, sig).arrange(RIGHT, buff=0.25).move_to(DOWN * 0.4)
        self.play(FadeOut(VGroup(d1, d2)), FadeOut(svd), FadeIn(grp))
        self.say("Σ is diagonal, so each singular value is updated on its own: σ becomes p(σ).")
        lhs2 = mt(r"p(\Sigma)=", 44, C_SIG).move_to(lhs, aligned_edge=RIGHT)
        psig.move_to(sig, aligned_edge=LEFT)
        self.play(ReplacementTransform(sig, psig), ReplacementTransform(lhs, lhs2), run_time=1.4)
        self.hold()

        self.play(FadeOut(VGroup(it, lhs2, psig)))

        # could you have invented p? only odd powers are available, then two wishes
        odd = VGroup(*[MathTex(a, r"\;\leadsto\;", b, font_size=40) for a, b in
                       ((r"W", r"\sigma"), (r"WW^{\top}W", r"\sigma^3"),
                        (r"WW^{\top}WW^{\top}W", r"\sigma^5"))])
        for m in odd:
            m[2].set_color(C_SIG)
        odd.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(UP * 1.2)
        self.say("But why this cubic? Imagine inventing it yourself, with only matrix products to work with.")
        self.say("Multiplying W by W transpose and W again turns each σ into σ cubed; one more round gives "
                 "σ to the fifth.", LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in odd], lag_ratio=0.4))
        self.hold()
        guess = mt(r"p(\sigma)=a\,\sigma+b\,\sigma^3", 44).move_to(DOWN * 0.6)
        self.say("So the cheapest recipe is a mix of the first two: a times σ plus b times σ cubed.",
                 odd.animate.scale(0.75).to_edge(LEFT, buff=0.6).set_opacity(0.5), FadeIn(guess))
        w1 = mt(r"p(1)=1:\quad a+b=1", 38, C_PLUS)
        w2 = mt(r"p'(1)=0:\quad a+3b=0", 38, C_PLUS)
        wishes = VGroup(w1, w2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(guess, DOWN, buff=0.5)
        self.say("Wish one: a σ that is already 1 should stay 1. That means a + b = 1.", FadeIn(w1))
        self.say("Wish two: a σ near 1 should snap to 1 fast, so the curve should be flat there. "
                 "That means a + 3b = 0.", FadeIn(w2))
        self.hold()
        px = MathTex(r"p(x)", r"=", r"\tfrac32\,x-\tfrac12\,x^3", font_size=60)
        px[2].set_color(C_P)
        px.move_to(DOWN * 0.2)
        box = SurroundingRectangle(px, color=C_P, buff=0.25, corner_radius=0.1)
        self.say("Solve: a = 3/2 and b = −1/2. That is exactly the Newton–Schulz polynomial.",
                 FadeOut(VGroup(odd, wishes)), ReplacementTransform(guess, px), Create(box),
                 speak="Solve, and a is three halves, b is minus one half. That is exactly the Newton Schulz polynomial.")
        self.hold(1.0)
        q = mt(r"\sigma\;\to\;p(\sigma)\;\to\;p(p(\sigma))\;\to\;\cdots\;\to\;?", 40, GREY_A)
        q.next_to(box, DOWN, buff=0.7)
        self.say("Start at some positive σ, apply p over and over. Where does it end up? That is part (e).",
                 FadeIn(q, shift=UP * 0.2))
        self.hold()
        corner = MathTex(r"p(x)=\tfrac32x-\tfrac12x^3", font_size=34).to_corner(UR, buff=0.35)
        corner[0][5:].set_color(C_P)
        self.play(FadeOut(q), FadeOut(box), ReplacementTransform(px, corner))
        self.corner = corner

    # ------------------------------------------------------------ 3. just try some numbers
    def try_numbers(self):
        lines = VGroup()
        for x0, n, c in ((0.5, 5, C_PLUS), (1.3, 4, C_PLUS), (0.1, 9, C_PLUS)):
            o = orbit(x0, n)
            assert abs(o[-1] - 1) < 0.04
            s = r"\to ".join(num(v, 1 if i == 0 else 2) for i, v in enumerate(o)) + r"\to\cdots"
            lines.add(mt(s, 34))
        lines.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(UP * 1.0).to_edge(LEFT, buff=0.8)
        if lines.width > 12.4:
            lines.scale_to_fit_width(12.4)
        self.say("No theory yet. Let's just try numbers. Start at 0.5: 0.69, 0.87, 0.98, then 1.",
                 Write(lines[0]), run_time=2.0)
        self.say("1.3 drops to 0.85, then climbs back up to 1.", Write(lines[1]))
        self.say("Even a tiny 0.1 creeps up, slowly at first, and also reaches 1.", Write(lines[2]))
        self.hold()
        p1 = mt(r"p(1)=\tfrac32-\tfrac12=1", 38, C_PLUS).move_to(DOWN * 1.0)
        self.say("Everything lands on 1, just as designed: p(1) = 1, so once a value reaches 1, it stays.",
                 FadeIn(p1))
        eqs = mt(r"p(x)=x\iff \tfrac12x-\tfrac12x^3=0\iff x^3=x\iff x\in\{-1,\,0,\,1\}", 36)
        eqs.move_to(DOWN * 2.0)
        self.say("A point with p(x) = x is called a fixed point. But 1 is not the only one: −1 and 0 "
                 "stay put too.", Write(eqs))
        self.hold()
        self.say("So why does 0.1 walk away from 0 and toward 1? A picture makes it clear.")
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 4. the graph and the cobweb
    def cobweb(self):
        g = self.make_graph()
        ax, curve, diag = self.ax, self.curve, self.diag
        self.say("Draw the curve y = p(x), and the diagonal y = x.",
                 Create(ax), FadeIn(g[1]), Create(curve), Create(diag), FadeIn(g[4]), FadeIn(g[5]),
                 run_time=2.0)
        rule = VGroup(
            txt("1. up or down to the curve: p(x)", 24),
            txt("2. across to the diagonal: new x", 24),
            txt("3. repeat", 24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rule.move_to([PANEL_X, 1.2, 0])
        if rule.width > 6.2:
            rule.scale_to_fit_width(6.2)
        w = self.web(0.3, 8, WHITE)
        m = self.start_mark(0.3, WHITE)
        self.say("To iterate on the picture, go from x up to the curve: that height is p(x).",
                 FadeIn(m), FadeIn(rule[0]), Create(w[0]))
        self.say("Then go across to the diagonal. That moves p(x) back onto the x axis as the new x.",
                 FadeIn(rule[1]), Create(w[1]))
        self.say("Repeat. Starting at 0.3, the path climbs a staircase up to 1.",
                 FadeIn(rule[2]), self.draw(w[2:], 0.3))
        self.hold()
        w2 = self.web(1.2, 5, WHITE)
        m2 = self.start_mark(1.2, WHITE)
        self.say("From 1.2, it drops just below 1, then settles on 1 as well.",
                 FadeOut(VGroup(w, m)), FadeIn(m2), self.draw(w2, 0.4))
        self.hold()
        fps = VGroup(*[Dot(ax.c2p(v, v), radius=0.09, color=c)
                       for v, c in ((-1, C_MINUS), (0, C_ZERO), (1, C_PLUS))])
        self.say("The fixed points −1, 0 and 1 are exactly where the curve meets the diagonal.",
                 FadeOut(VGroup(w2, m2, rule)), LaggedStart(*[GrowFromCenter(d) for d in fps], lag_ratio=0.25))
        self.fps = fps

    # ------------------------------------------------------------ 5. why 1 attracts and 0 repels
    def slopes(self):
        ax, fps = self.ax, self.fps
        der = mt(r"p'(x)=\tfrac32-\tfrac32x^2", 38).move_to([PANEL_X, 2.2, 0])
        self.say("Why is 1 a magnet while 0 pushes things away? Look at the slope of p at each one.",
                 Write(der))
        tan0 = ax.plot(lambda x: 1.5 * x, x_range=[-0.9, 0.9], color=C_ZERO, stroke_width=3)
        near0 = orbit(0.05, 4)
        s0 = mt(r"p'(0)=\tfrac32>1", 36, C_ZERO)
        seq0 = mt(r"\to ".join(num(v, 3) for v in near0) + r"\to\cdots", 30)
        g0 = VGroup(s0, seq0).arrange(DOWN, buff=0.25).next_to(der, DOWN, buff=0.45)
        if g0.width > 6.2:
            g0.scale_to_fit_width(6.2)
        w0 = self.web(0.05, 10, C_ZERO, width=2.5)
        self.say("At 0 the slope is 1.5, so a small offset grows by half each step. From 0.05 it drifts away.",
                 Create(tan0), FadeIn(s0))
        self.play(FadeIn(seq0), self.draw(w0, 0.22))
        self.hold()

        near1 = orbit(1.2, 3)
        errs = [abs(v - 1) for v in near1]
        assert errs[1] < errs[0] ** 2 * 1.7 and errs[2] < errs[1] ** 2 * 1.7
        s1 = mt(r"p'(\pm1)=0", 36, C_PLUS)
        seq1 = mt(r"|x-1|:\ " + r"\to ".join(f"{e:.2g}" for e in errs[:3]) + r"\to\cdots", 30)
        g1 = VGroup(s1, seq1).arrange(DOWN, buff=0.25).next_to(der, DOWN, buff=0.45)
        tan1 = VGroup(ax.plot(lambda x: 1, x_range=[0.5, 1.5], color=C_PLUS, stroke_width=3),
                      ax.plot(lambda x: -1, x_range=[-1.5, -0.5], color=C_MINUS, stroke_width=3))
        self.say(f"At ±1 the slope is 0, as we wished, so the error roughly squares: from 1.2 it is "
                 f"{errs[0]:.1f}, {errs[1]:.3f}, {errs[2]:.3f}.",
                 FadeOut(VGroup(g0, w0, tan0)), Create(tan1), FadeIn(g1))
        self.hold()
        lab0 = txt("unstable", 22, C_ZERO).next_to(fps[1], RIGHT, buff=0.3).shift(DOWN * 0.45)
        lab1 = txt("stable", 22, C_PLUS).next_to(fps[2], DOWN, buff=0.25).shift(RIGHT * 0.25)
        lab_1 = txt("stable", 22, C_MINUS).next_to(fps[0], UP, buff=0.25).shift(LEFT * 0.25)
        self.say("So 0 is unstable, like a hilltop, and ±1 are stable, like the bottoms of two valleys.",
                 FadeIn(VGroup(lab0, lab1, lab_1)))
        self.hold()
        self.play(FadeOut(VGroup(der, g1, tan1, lab0, lab1, lab_1)))

    # ------------------------------------------------------------ 6. how big can σ be? (√3)
    def how_big(self):
        ax = self.ax
        self.say("So far every start went to 1. But we don't get to choose σ. How large can it be?")
        w = self.web(1.5, 8, C_PLUS)
        m = self.start_mark(1.5, C_PLUS)
        t15 = mt(r"p(1.5)=" + num(p(1.5)), 36, C_PLUS).move_to([PANEL_X, 2.2, 0])
        self.say(f"Try 1.5. It drops to {p(1.5):.2f}, then climbs back to 1. Still fine.",
                 FadeIn(m), FadeIn(t15), self.draw(w, 0.3))
        self.hold()
        m2 = self.start_mark(1.8, C_MINUS)
        self.say("Now 1.8, a little bigger. Before we look: where do you think it ends up?",
                 FadeOut(VGroup(w, m)), FadeIn(m2))
        self.hold(1.5)
        w2 = self.web(1.8, 9, C_MINUS)
        t18 = mt(r"p(1.8)=" + num(p(1.8), 3), 36, C_MINUS).next_to(t15, DOWN, buff=0.35)
        self.say("It lands below the axis, at −0.216, and then slides all the way down to −1!",
                 FadeIn(t18), self.draw(w2, 0.3))
        self.hold(1.0)

        # √3 is where the hump comes back down to the axis
        hump = ax.plot(p, x_range=[0, S3], color=C_PLUS, stroke_width=7)
        past = ax.plot(p, x_range=[S3, 2.05], color=C_MINUS, stroke_width=7)
        cross = Dot(ax.c2p(S3, 0), radius=0.09, color=C_ZERO)
        self.say("After its hump, the curve comes back down and crosses the axis. Past that point, p(x) is negative.",
                 FadeOut(VGroup(t15, t18)), FadeOut(w2), Create(hump), Create(past), GrowFromCenter(cross))
        fac = MathTex(r"p(x)", r"=", r"\frac{x}{2}", r"\,(3-x^2)", font_size=42)
        fac.move_to([PANEL_X, 2.2, 0])
        tick = Line(ax.c2p(S3, -0.08), ax.c2p(S3, 0.08), color=C_ZERO, stroke_width=4)
        lab = mt(r"\sqrt3", 30, C_ZERO).move_to(ax.c2p(S3 - 0.3, 0.25))
        self.say(f"Factoring p shows where: the crossing is at x = √3, about {S3:.2f}. And 1.8 is just past it.",
                 Write(fac), FadeIn(lab), Flash(cross, color=C_ZERO))
        self.hold()
        top = DashedLine(ax.c2p(0, 1), ax.c2p(S3, 1), color=GREY_B, dash_length=0.08)
        self.say("Below √3, the hump stays above the axis but never above 1. So one step lands between 0 and 1.",
                 FadeOut(past), Create(top), Indicate(self.fps[2], color=C_PLUS), FadeOut(m2))
        seg01 = ax.plot(p, x_range=[0, 1], color=C_PLUS)
        area = ax.get_area(seg01, x_range=[0, 1], bounded_graph=self.diag, color=C_PLUS, opacity=0.35)
        w3 = self.web(0.3, 8, WHITE, width=2.5)
        self.say("And between 0 and 1 the curve sits above the diagonal, so every step climbs, never past 1.",
                 FadeIn(area), self.draw(w3, 0.25))
        self.say("So every σ between 0 and √3 ends at +1.", FadeOut(w3))
        self.hold()
        arrow = CurvedArrow(ax.c2p(S3, 0) + UP * 0.12, ax.c2p(0, 0) + UP * 0.12, angle=PI / 3,
                            color=C_ZERO, stroke_width=4)
        s3 = mt(r"p(\sqrt3)=0", 36, C_ZERO).next_to(fac, DOWN, buff=0.45)
        self.say("And exactly at √3? p(√3) = 0. It lands on the unstable fixed point 0, and stays there forever.",
                 Create(arrow), FadeIn(s3), Flash(self.fps[1], color=C_ZERO))
        self.hold()
        self.play(FadeOut(VGroup(s3, arrow, top, hump, area, cross)), FadeIn(tick))
        self.s3_mark = VGroup(tick, lab)
        self.fac = fac

    # ------------------------------------------------------------ 7. much bigger σ (√5)
    def too_big(self):
        ax = self.ax
        o3 = orbit(3.0, 2)
        assert o3 == [3.0, -9.0, 351.0]
        blow = mt(r"3\to -9\to 351\to\cdots", 38, C_S5).next_to(self.fac, DOWN, buff=0.45)
        self.say("Past √3 the sign flips every step. That alone might be fine. But try a big start, like 3.",
                 FadeIn(blow[0][0]))
        self.say("p(3) = −9, and then 351. Flipping and growing: it explodes.", FadeIn(blow))
        self.hold()
        anti = DashedLine(ax.c2p(-2.5, 2.5), ax.c2p(2.5, -2.5), color=C_S5, stroke_width=2.5,
                          dash_length=0.1)
        anti_l = mt(r"y=-x", 30, C_S5).move_to(ax.c2p(1.0, -1.5))
        xc = _root(-2.5, 1.0, 2.5)
        shrink = ax.plot(p, x_range=[S3, S5], color=C_ZERO, stroke_width=7)
        grow = ax.plot(p, x_range=[S5, xc], color=C_S5, stroke_width=7)
        self.say("When does it shrink? Draw y = −x: a flipped value has shrunk if the curve lies above that line.", FadeOut(blow), Create(anti), FadeIn(anti_l))
        self.say("Just past √3, the curve is above that line: flip and shrink. Further out it dives below: "
                 "flip and grow.", Create(shrink), Create(grow))
        meet = Dot(ax.c2p(S5, -S5), radius=0.09, color=C_S5)
        eqm = mt(r"p(x)=-x\iff x^2=5", 36, C_S5).next_to(self.fac, DOWN, buff=0.45)
        s5 = Line(ax.c2p(S5, -0.08), ax.c2p(S5, 0.08), color=C_S5, stroke_width=4)
        s5l = mt(r"\sqrt5", 30, C_S5).next_to(s5, UP, buff=0.1)
        self.say(f"They meet where p(x) = −x, that is x squared = 5. The second key number is √5, about {S5:.2f}.", GrowFromCenter(meet), FadeIn(eqm), Create(s5), FadeIn(s5l))
        self.hold(1.0)

        pts = [ax.c2p(S5, 0)]
        x = S5
        for _ in range(4):
            y = p(x)
            pts += [ax.c2p(x, y), ax.c2p(y, y)]
            x = y
        sq = VGroup(*[Line(a, b, color=C_S5, stroke_width=3.5) for a, b in zip(pts, pts[1:])])
        self.say("Start exactly at √5: it lands on −√5, then back on √5. The cobweb becomes a square.",
                 FadeOut(VGroup(shrink, grow)), self.draw(sq[:5], 0.5))
        self.play(self.draw(sq[5:], 0.35))
        per = txt("period-2 orbit", 26, C_S5).next_to(eqm, DOWN, buff=0.35)
        self.say("So √5 neither settles nor explodes. It bounces between ±√5 forever: a period-2 orbit.",
                 FadeIn(per))
        self.hold(1.0)
        o = orbit(2.3, 3)
        seq = mt(r"\to ".join(num(v, 2 if abs(v) < 10 else 1) for v in o) + r"\to\cdots", 34, C_S5)
        seq.next_to(per, DOWN, buff=0.45)
        if seq.width > 6.2:
            seq.scale_to_fit_width(6.2)
        self.say(f"Just past it, at 2.3, every step flips and grows: {neg(num(o[1]))}, {num(o[2])}, "
                 f"{neg(num(o[3], 1))}. It diverges.", FadeIn(seq))
        self.hold(0.5)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 8. the gap between √3 and √5
    def the_gap(self):
        L = NumberLine(x_range=[0, 2.4, 0.5], length=9.0, include_tip=False).move_to([-0.2, 0, 0])
        ov = NumberLine(x_range=[0, 2.4, 0.5], length=9.0, color=GREY_B, stroke_width=2,
                        include_tip=False, tick_size=0.04).move_to([-0.2, 0.4, 0])
        gap = Rectangle(width=L.n2p(S5)[0] - L.n2p(S3)[0], height=0.5, stroke_width=0,
                        fill_color=C_ZERO, fill_opacity=0.35)
        gap.move_to([(L.n2p(S3)[0] + L.n2p(S5)[0]) / 2, 0.4, 0])
        ovl = VGroup(mt(r"\sqrt3", 28, C_ZERO).next_to(ov.n2p(S3), DOWN, buff=0.35),
                     mt(r"\sqrt5", 28, C_S5).next_to(ov.n2p(S5), DOWN, buff=0.35),
                     mt(r"1", 28, C_PLUS).next_to(ov.n2p(1), DOWN, buff=0.35),
                     mt(r"0", 28, GREY_B).next_to(ov.n2p(0), DOWN, buff=0.35))
        self.say("That leaves the gap between √3 and √5: flip and shrink. Shrinking, it must fall below √3 "
                 "at some point.", Create(ov), FadeIn(ovl), FadeIn(gap))
        self.say("From there, no more flips: it settles at +1 or −1. 1.8 went to −1. Does the whole gap?")
        self.hold()

        # color every start by its fate
        def fcol(v):
            f = fate(v)[0]
            return C_S5 if f == "diverges" else (C_PLUS if f > 0 else (C_MINUS if f < 0 else C_ZERO))

        N, hi = 2400, 2.4
        xs = [(i + 0.5) * hi / N for i in range(N)]
        cols = [fcol(v) for v in xs]
        strip = VGroup()
        i = 0
        while i < N:
            j = i
            while j + 1 < N and cols[j + 1] == cols[i]:
                j += 1
            a_, b_ = ov.n2p(i * hi / N)[0], ov.n2p((j + 1) * hi / N)[0]
            r = Rectangle(width=b_ - a_, height=0.5, stroke_width=0, fill_color=cols[i], fill_opacity=0.9)
            r.move_to([(a_ + b_) / 2, 0.4, 0])
            strip.add(r)
            i = j + 1
        assert len(strip) >= 5, len(strip)
        legend = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.9),
                                 txt(t, 22, c)).arrange(RIGHT, buff=0.12)
                          for c, t in ((C_PLUS, "ends at +1"), (C_MINUS, "ends at −1"),
                                       (C_S5, "blows up"))]).arrange(RIGHT, buff=0.6).move_to([-0.2, 1.6, 0])
        self.say("Let's not guess. Color every start from 0 to 2.4 by where it ends up.",
                 FadeOut(gap), FadeIn(legend))
        self.play(LaggedStart(*[FadeIn(r) for r in strip], lag_ratio=0.02), run_time=2.5)
        self.hold(1.0)
        a0, b0 = ov.n2p(2.1)[0], ov.n2p(S5)[0]
        focus = Rectangle(width=b0 - a0, height=0.8, color=YELLOW_D, stroke_width=3).move_to([(a0 + b0) / 2, 0.4, 0])
        self.say("Below √3, all teal, as we proved. But the gap is not all gold. Near √5 there are stripes.",
                 Create(focus))
        mag = VGroup()
        lo_z, hi_z = 2.1, S5
        Lz = NumberLine(x_range=[lo_z, hi_z, 0.05], length=9.0, include_tip=False).move_to([-0.2, -1.2, 0])
        Nz = 1500
        zc = [fcol(lo_z + (k + 0.5) * (hi_z - lo_z) / Nz) for k in range(Nz)]
        k = 0
        while k < Nz:
            m_ = k
            while m_ + 1 < Nz and zc[m_ + 1] == zc[k]:
                m_ += 1
            a_ = Lz.n2p(lo_z + k * (hi_z - lo_z) / Nz)[0]
            b_ = Lz.n2p(lo_z + (m_ + 1) * (hi_z - lo_z) / Nz)[0]
            mag.add(Rectangle(width=b_ - a_, height=0.5, stroke_width=0, fill_color=zc[k],
                              fill_opacity=0.9).move_to([(a_ + b_) / 2, -1.2, 0]))
            k = m_ + 1
        zl = VGroup(mt(num(lo_z, 1), 24, GREY_B).next_to(mag, DOWN, buff=0.15).align_to(mag, LEFT),
                    mt(r"\sqrt5", 24, C_S5).next_to(mag, DOWN, buff=0.15).align_to(mag, RIGHT))
        links = VGroup(Line(focus.get_corner(DL), mag.get_corner(UL), color=YELLOW_D, stroke_width=1.5),
                       Line(focus.get_corner(DR), mag.get_corner(UR), color=YELLOW_D, stroke_width=1.5))
        self.say("Zoom in: gold, teal, gold, teal, each stripe thinner than the last, squeezed against √5.",
                 Create(links), FadeIn(mag), FadeIn(zl))
        self.hold(1.5)
        self.say("Where do these stripes come from? Let's follow one start from each: 2.0, 2.2 and 2.23.")
        self.play(FadeOut(VGroup(ov, ovl, strip, legend, focus, mag, zl, links)))

        starts = [2.0, 2.2, 2.23]
        rows, dots, names, counters = VGroup(), VGroup(), VGroup(), VGroup()
        for i, x0 in enumerate(starts):
            nl = NumberLine(x_range=[0, 2.4, 0.5], length=9.0, color=GREY_B, stroke_width=2,
                            include_tip=False, tick_size=0.04).move_to([-0.2, 1.3 - 1.4 * i, 0])
            rows.add(nl)
            names.add(mt(r"x_0=" + num(x0), 30).next_to(nl, LEFT, buff=0.3))
            dots.add(Dot(nl.n2p(x0), radius=0.1, color=sign_color(x0)))
            counters.add(txt("0 flips", 24, GREY_A).next_to(nl, RIGHT, buff=0.35))
        top, bot = 2.05, -1.55
        band = Rectangle(width=L.n2p(S5)[0] - L.n2p(S3)[0], height=top - bot, stroke_width=0,
                         fill_color=C_ZERO, fill_opacity=0.14)
        band.move_to([(L.n2p(S3)[0] + L.n2p(S5)[0]) / 2, (top + bot) / 2, 0])
        guides = VGroup()
        for v, c, s in ((1, C_PLUS, r"1"), (S3, C_ZERO, r"\sqrt3"), (S5, C_S5, r"\sqrt5")):
            xx = L.n2p(v)[0]
            guides.add(DashedLine([xx, bot, 0], [xx, top, 0], color=c, stroke_width=2, dash_length=0.08))
            guides.add(mt(s, 28, c).move_to([xx, top + 0.25, 0]))
        zero = mt(r"|x|=0", 24, GREY_B).next_to(rows[-1].n2p(0), DOWN, buff=0.2)
        legend = VGroup(
            VGroup(Dot(radius=0.08, color=C_PLUS), txt("positive", 22, C_PLUS)).arrange(RIGHT, buff=0.12),
            VGroup(Dot(radius=0.08, color=C_MINUS), txt("negative", 22, C_MINUS)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.4).next_to(rows[-1], DOWN, buff=0.3).align_to(rows[-1], RIGHT)
        self.say("We plot only the size of each value, show its sign by color, and count the flips.",
                 FadeIn(band), FadeIn(guides), FadeIn(rows), FadeIn(names), FadeIn(zero),
                 FadeIn(legend), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.2),
                 FadeIn(counters))

        orbs = [orbit(x0, 5) for x0 in starts]
        flips = [0, 0, 0]

        def step(k):
            anims = []
            for i in range(3):
                a, b = orbs[i][k - 1], orbs[i][k]
                if a * b < 0:
                    flips[i] += 1
                    word = "flip" if flips[i] == 1 else "flips"
                    new = txt(f"{flips[i]} {word}", 24, sign_color(b)).move_to(counters[i], aligned_edge=LEFT)
                    anims.append(Transform(counters[i], new))
                anims.append(dots[i].animate.move_to(rows[i].n2p(abs(b))).set_color(sign_color(b)))
            return anims

        self.say("Step by step: the sizes move left, and the colors alternate.", *step(1), run_time=1.2)
        for k in range(2, 6):
            self.play(*step(k), run_time=1.0)
        assert flips == [1, 2, 3], flips
        self.say("2.0 flips once before dropping below √3. 2.2 flips twice, and 2.23 three times.",
                 LaggedStart(*[Indicate(c) for c in counters], lag_ratio=0.3))
        self.hold()
        fates = VGroup()
        for i, x0 in enumerate(starts):
            lim = fate(x0)[0]
            fates.add(mt(("+" if lim > 0 else "") + str(int(lim)), 34, sign_color(lim))
                      .next_to(counters[i], RIGHT, buff=0.3))
        self.say("So 2.0 ends at −1, 2.2 at +1, and 2.23 at −1: one for each stripe.",
                 LaggedStart(*[FadeIn(f_, shift=LEFT * 0.2) for f_ in fates], lag_ratio=0.3))
        rule = VGroup(txt("odd flips → −1", 30, C_MINUS), txt("even flips → +1", 30, C_PLUS))
        rule.arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.9)
        self.say("From a positive start, an odd number of flips ends at −1, and an even number at +1.",
                 FadeIn(rule))
        self.say("So the stripes are flip counts. Where exactly does the count change from one to two?")
        self.hold(0.5)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 9. the first boundary b1
    def first_boundary(self):
        g = self.make_graph()
        ax = self.ax
        s3 = VGroup(Line(ax.c2p(S3, -0.08), ax.c2p(S3, 0.08), color=C_ZERO, stroke_width=4),
                    mt(r"\sqrt3", 28, C_ZERO).move_to(ax.c2p(S3 - 0.3, 0.25)))
        self.play(FadeIn(g), FadeIn(s3))
        b1 = B[1]
        h = DashedLine(ax.c2p(-0.3, -S3), ax.c2p(2.4, -S3), color=C_ZERO, dash_length=0.08)
        hl = mt(r"y=-\sqrt3", 28, C_ZERO).next_to(ax.c2p(-0.3, -S3), LEFT, buff=0.1)
        dot = Dot(ax.c2p(b1, -S3), radius=0.08, color=C_ZERO)
        drop = DashedLine(ax.c2p(b1, -S3), ax.c2p(b1, 0), color=C_ZERO, dash_length=0.06)
        bl = mt(r"b_1", 28, C_ZERO).next_to(ax.c2p(b1, 0), UP, buff=0.2)
        defn = mt(r"p(b_1)=-\sqrt3", 38, C_ZERO).move_to([PANEL_X, 2.2, 0])
        val = mt(r"b_1\approx" + num(b1, 4), 36, C_ZERO).next_to(defn, DOWN, buff=0.3)
        self.say("One flip or two? One step must land inside √3. The cutoff is where p(x) is exactly −√3. "
                 "Call it b1.", Create(h), FadeIn(hl), GrowFromCenter(dot), Create(drop), FadeIn(bl),
                 FadeIn(defn), FadeIn(val))
        self.hold()
        xin = Line(ax.c2p(S3, 0), ax.c2p(b1, 0), color=C_MINUS, stroke_width=9)
        yin = Line(ax.c2p(0, 0), ax.c2p(0, -S3), color=C_MINUS, stroke_width=9)
        piece = ax.plot(p, x_range=[S3, b1], color=C_MINUS, stroke_width=7)
        mapto = mt(r"p\big((\sqrt3,\,b_1)\big)=(-\sqrt3,\,0)", 36, C_MINUS).next_to(val, DOWN, buff=0.45)
        self.say("p is decreasing here, so every x between √3 and b1 lands between −√3 and 0: one flip, then −1.",
                 Create(xin), Create(piece), FadeIn(mapto))
        self.play(TransformFromCopy(xin, yin), run_time=1.2)
        self.hold()
        two = Dot(ax.c2p(2, -1), radius=0.08, color=C_MINUS)
        twol = mt(r"p(2)=-1", 36, C_MINUS).next_to(mapto, DOWN, buff=0.4)
        self.say("Both 1.8 and 2 are in this piece. In fact p(2) is exactly −1.", GrowFromCenter(two),
                 FadeIn(twol), Flash(two, color=C_MINUS))
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
        defn = mt(r"b_0=\sqrt3,\qquad p(b_n)=-b_{n-1}\ \iff\ b_n^3-3b_n=2b_{n-1}", 36)
        defn.to_edge(UP, buff=0.4).to_edge(LEFT, buff=0.5)
        self.say("Same idea one level up: b2 is the start that lands exactly on −b1, b3 lands exactly on −b2, "
                 "and so on.",
                 Write(defn))
        vals = mt(r",\ ".join(f"b_{{{k}}}\\approx{B[k]:.4f}" for k in (1, 2, 3)) + r",\ \ldots\ \nearrow\sqrt5", 34)
        vals.move_to([0, -0.9, 0])
        self.say(f"b1 is about {B[1]:.3f}, b2 about {B[2]:.3f}, b3 about {B[3]:.3f}: the stripe edges, "
                 f"creeping up toward √5.",
                 FadeIn(vals))

        bar = self.basin_bar(S3, colored=False)
        X = bar.X
        s3l = mt(r"\sqrt3", 30, C_ZERO).next_to([X(S3), 0.45 - 0.31, 0], DOWN, buff=0.18)
        core = Rectangle(width=1.55, height=0.62, stroke_width=0, fill_color=GREY_D, fill_opacity=0.9)
        core.move_to([-5.85, 0.45, 0])
        core_l = mt(r"|x|<\sqrt3", 26).move_to(core)
        self.say("Cut the gap at these points, and watch where one step of p sends each piece.",
                 FadeIn(bar), FadeIn(s3l), FadeIn(core), FadeIn(core_l))
        centers = [X((B[k - 1] + B[k]) / 2) for k in (1, 2, 3)]
        arrows = VGroup()
        for k in (3, 2, 1):
            a = [centers[k - 1], 0.8, 0]
            b = [centers[k - 2] if k > 1 else -5.85, 0.8, 0]
            arrows.add(CurvedArrow(a, b, angle=PI / 2.4 if k > 1 else PI / 3, color=GREY_A,
                                   stroke_width=3, tip_length=0.18))
        arrows.submobjects.reverse()   # arrows[0]: I1 -> core, arrows[1]: I2 -> I1, arrows[2]: I3 -> I2
        plab = mt(r"p", 30, GREY_A).next_to(arrows[0], UP, buff=0.05)
        maps = mt(r"p\big((b_{n-1},\,b_n)\big)=(-b_{n-1},\,-b_{n-2})", 34).move_to([0, -1.75, 0])
        self.play(Create(arrows[2]), Create(arrows[1]), Create(arrows[0]), FadeIn(plab), FadeIn(maps),
                  run_time=1.6)
        self.hold()

        colors = [C_MINUS, C_PLUS, C_MINUS]
        self.say("The first piece lands inside √3, on the negative side. From there it slides to −1.",
                 bar.rects[0].animate.set_fill(colors[0], 0.75), Indicate(arrows[0], color=C_MINUS))
        f1 = mt("-1", 30, BLACK).move_to(bar.rects[0])
        self.play(FadeIn(f1))
        ghost = bar.rects[1].copy().set_fill(WHITE, 0.5)
        self.say("The second piece lands exactly on the first piece, flipped to the negative side.",
                 Indicate(arrows[1], color=WHITE))
        self.play(ghost.animate(path_arc=PI / 2.4).become(bar.rects[0].copy().set_fill(WHITE, 0.5)),
                  run_time=1.6)
        self.say("p is odd, so a flipped start has a flipped fate. The first piece's −1 becomes +1.",
                 FadeOut(ghost), bar.rects[1].animate.set_fill(colors[1], 0.75))
        self.hold(0.8)
        f2 = mt("+1", 30, BLACK).move_to(bar.rects[1])
        self.play(FadeIn(f2))
        self.say("The third maps onto the mirror of the second: −1 again. And so on, alternating.",
                 bar.rects[2].animate.set_fill(colors[2], 0.75), Indicate(arrows[2], color=C_MINUS),
                 *[bar.rects[k].animate.set_fill(C_MINUS if k % 2 == 0 else C_PLUS, 0.75)
                   for k in range(3, 12)])
        rule = MathTex(r"b_{n-1}<\sigma<b_n", r"\ \Longrightarrow\ ", r"x_k\to(-1)^n", font_size=38)
        rule[2].set_color(YELLOW_D)
        rule.move_to([0, -1.75, 0])
        self.say("So the n-th piece flips n times: odd n ends at −1, even n at +1. That is the striped picture.",
                 FadeOut(maps), FadeIn(rule))
        self.hold()

        # zoom towards √5: the picture repeats
        live = self.basin_bar(S3)
        self.remove(bar, f1, f2)
        self.add(live)
        t = ValueTracker(0.0)
        zoomed = always_redraw(lambda: self.basin_bar(S5 - (S5 - S3) * 6 ** (-t.get_value())))
        self.remove(live)
        self.add(zoomed)
        self.say("The pieces pile up against √5. Zoom in, and the same pattern repeats again and again.",
                 FadeOut(VGroup(arrows, plab, core, core_l, s3l, vals)))
        self.play(t.animate.set_value(2.0), run_time=6.0, rate_func=smooth)
        zoomed.clear_updaters()
        self.hold()
        slope = mt(r"p'(\sqrt5)=\tfrac32-\tfrac32\cdot5=-6", 36, C_S5)
        ratios = mt(r"\frac{\sqrt5-b_{n-1}}{\sqrt5-b_n}\ \to\ 6", 36)
        sr = VGroup(slope, ratios).arrange(RIGHT, buff=1.0).move_to([0, -0.85, 0])
        r_now = (S5 - B[5]) / (S5 - B[6])
        assert abs(r_now - 6) < 0.05
        self.say("Each piece is about a sixth of the one before, because the slope of p at √5 is −6.",
                 FadeIn(sr))
        self.hold()
        self.say("So between √3 and √5 there are infinitely many basins, alternating −1, +1, −1, +1, and so on.",
                 Indicate(rule[2]))
        self.hold(0.5)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 11. the boundary points themselves
    def boundary_points(self):
        rows, dots, names, chains = VGroup(), VGroup(), VGroup(), VGroup()
        paths = []
        for i, n in enumerate((1, 2, 3)):
            row = self.number_row(1.7 - 1.55 * i, lo=-2.4, hi=2.4, length=10.0, x=0.6, marks=(0,))
            nl = row[0]
            for v in (S3, -S3):
                row.add(Line(nl.n2p(v) + DOWN * 0.1, nl.n2p(v) + UP * 0.1, color=C_ZERO, stroke_width=4))
                row.add(mt(r"\sqrt3" if v > 0 else r"-\sqrt3", 22, C_ZERO).next_to(nl.n2p(v), DOWN, buff=0.14))
            rows.add(row)
            names.add(mt(f"b_{{{n}}}", 34, C_ZERO).next_to(nl, LEFT, buff=0.35))
            # b_n -> -b_{n-1} -> ... -> ±√3 -> 0, exactly
            path = [(+1, n)]
            s = 1
            for k in range(n - 1, -1, -1):
                s = -s
                path.append((s, k))
            vals = [sg * B[k] for sg, k in path] + [0.0]
            assert all(abs(p(a) - b) < 1e-9 for a, b in zip(vals, vals[1:]))
            paths.append(vals)
            terms = [("-" if sg < 0 else "") + (r"\sqrt3" if k == 0 else f"b_{{{k}}}") for sg, k in path] + ["0"]
            chains.add(mt(r"\to ".join(terms), 30, C_ZERO).next_to(nl, UP, buff=0.18).align_to(nl, RIGHT))
            dots.add(Dot(nl.n2p(vals[0]), radius=0.09, color=C_ZERO))
        self.say("And the stripe edges themselves? b1 goes to −√3 in one step, and then to 0.",
                 FadeIn(rows[0]), FadeIn(names[0]), GrowFromCenter(dots[0]))
        nl = rows[0][0]
        for a, b in zip(paths[0], paths[0][1:]):
            self.play(self.hop(dots[0], nl, a, b, C_ZERO), run_time=0.9)
        self.play(FadeIn(chains[0]))
        self.say("b2 takes two steps to reach √3, b3 takes three. Then both drop to 0.",
                 FadeIn(rows[1:]), FadeIn(names[1:]), *[GrowFromCenter(d) for d in dots[1:]])
        for j in range(max(len(q) for q in paths[1:]) - 1):
            anims = []
            for i in (1, 2):
                if j + 1 < len(paths[i]):
                    anims.append(self.hop(dots[i], rows[i][0], paths[i][j], paths[i][j + 1], C_ZERO))
            self.play(*anims, run_time=0.9)
        self.play(FadeIn(chains[1:]))
        self.say("Every stripe edge hits ±√3 exactly after a few steps, then sits on 0, the unstable fixed point.",
                 LaggedStart(*[Flash(d, color=C_ZERO) for d in dots], lag_ratio=0.2))
        self.hold()
        self.say("But they are single points: nudge one slightly, and it falls into a basin on either side.")
        self.hold(0.5)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 12. the answer to (e)
    def summary(self):
        head = [txt("start σ", 26, GREY_B), txt("what happens", 26, GREY_B), txt("ends at", 26, GREY_B)]
        rows = [
            (mt(r"0<\sigma<\sqrt3", 34), txt("no flips, climbs to 1", 26), mt(r"+1", 34, C_PLUS)),
            (mt(r"\sigma=\sqrt3", 34), txt("lands on 0 in one step", 26), mt(r"0", 34, C_ZERO)),
            (mt(r"b_{n-1}<\sigma<b_n", 34), txt("n flips while shrinking", 26), mt(r"(-1)^n", 34, YELLOW_D)),
            (mt(r"\sigma=b_n", 34), txt("hits ±√3, then 0", 26), mt(r"0", 34, C_ZERO)),
            (mt(r"\sigma=\sqrt5", 34), txt("bounces between ±√5", 26), txt("period 2", 26, C_S5)),
            (mt(r"\sigma>\sqrt5", 34), txt("flips while growing", 26), txt("diverges", 26, C_S5)),
        ]
        xs = (-3.9, 0.7, 4.6)
        table = VGroup()
        for r, cells in enumerate([head] + rows):
            y = 2.55 - 0.72 * r
            line = VGroup(*[c.move_to([x, y, 0]) for c, x in zip(cells, xs)])
            table.add(line)
        rule = Line([-6.2, 2.2, 0], [6.2, 2.2, 0], color=GREY_C, stroke_width=1.5)
        self.say("Here is the full answer to part (e).", FadeIn(table[0]), Create(rule))
        self.say("Below √3, σ goes to +1. Exactly at √3, it lands on 0.",
                 FadeIn(table[1], shift=UP * 0.1), FadeIn(table[2], shift=UP * 0.1))
        self.say("Between √3 and √5, the stripes alternate −1 and +1 by flip count; their edges go to 0.",
                 FadeIn(table[3], shift=UP * 0.1), FadeIn(table[4], shift=UP * 0.1))
        self.say("At √5 it bounces forever, and beyond √5 it diverges.",
                 FadeIn(table[5], shift=UP * 0.1), FadeIn(table[6], shift=UP * 0.1))
        self.hold(0.8)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 13. back to the matrix
    def back_to_matrix(self):
        sig0 = [2.9, 1.6, 0.9, 0.35]
        nl = NumberLine(x_range=[0, 3.2, 0.5], length=11.0, color=GREY_B, stroke_width=2,
                        include_tip=False, tick_size=0.04).move_to([0.3, -0.2, 0])
        marks = VGroup()
        for v, c, s in ((0, GREY_B, "0"), (1, C_PLUS, "1"), (S3, C_ZERO, r"\sqrt3"), (S5, C_S5, r"\sqrt5")):
            marks.add(Line(nl.n2p(v) + DOWN * 0.12, nl.n2p(v) + UP * 0.12, color=c, stroke_width=4))
            marks.add(mt(s, 28, c).next_to(nl.n2p(v), DOWN, buff=0.2))
        lab = mt(r"\sigma_i", 32, C_SIG).next_to(nl, LEFT, buff=0.3)
        dots = VGroup(*[Dot(nl.n2p(s), radius=0.1, color=C_SIG) for s in sig0])
        self.say("Back to the matrix. A real W can have singular values anywhere, some far above √5.",
                 Create(nl), FadeIn(marks), FadeIn(lab), LaggedStart(*[GrowFromCenter(d) for d in dots]))
        bad = SurroundingRectangle(dots[0], color=C_S5, buff=0.12)
        blow = mt(r"p(2.9)=" + num(p(2.9)), 32, C_S5).next_to(dots[0], UP, buff=0.35)
        self.say("This one at 2.9 would blow up. So before iterating, W must be scaled down.",
                 Create(bad), FadeIn(blow))
        self.hold()

        fro = math.sqrt(sum(s * s for s in sig0))
        sig1 = [s / fro for s in sig0]
        assert max(sig1) < 1 < S3
        norm = MathTex(r"W\ \leftarrow\ \frac{W}{\|W\|_F}", r",\qquad",
                       r"\sigma_{\max}\le\|W\|_F=\sqrt{\textstyle\sum_i\sigma_i^2}",
                       font_size=38).to_edge(UP, buff=0.8)
        self.say("A common choice: divide by the Frobenius norm. It is never smaller than the largest singular value.",
                 FadeOut(VGroup(bad, blow)), Write(norm))
        self.say("After scaling, every singular value sits between 0 and 1, safely below √3.",
                 *[d.animate.move_to(nl.n2p(s)) for d, s in zip(dots, sig1)], run_time=1.6)
        steps = 8
        orbs = [orbit(s, steps) for s in sig1]
        assert all(abs(o[-1] - 1) < 0.01 for o in orbs)
        k_lab = mt(r"k=0", 34).next_to(nl, UP, buff=1.1).align_to(nl, LEFT)
        self.say("Now each one walks to +1. Small ones take longer, but all arrive, and W becomes U V transpose.",
                 FadeIn(k_lab))
        for k in range(1, steps + 1):
            new_k = mt(f"k={k}", 34).move_to(k_lab, aligned_edge=LEFT)
            self.play(*[d.animate.move_to(nl.n2p(o[k])).set_color(C_PLUS if abs(o[k] - 1) < 0.02 else C_SIG)
                        for d, o in zip(dots, orbs)], Transform(k_lab, new_k), run_time=0.55)
        res = mt(r"W_k\ \to\ UV^{\top}", 40, C_PLUS).next_to(nl, UP, buff=1.1).align_to(nl, RIGHT)
        self.play(FadeIn(res))
        self.say("The ellipse became a circle. All it took was a cubic built from two simple wishes.")
        self.hold(0.8)
