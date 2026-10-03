"""Newton–Schulz iteration, EECS 182 Fall 2026 Discussion 5, part (e): what the three
episodes share. The math of p (every number on screen is computed here, the key ones are
asserted), the colors, and NSScene with the graph of p, cobwebs and the cards.
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
    """A formula, in one of three sizes: small labels (28), formulas (36), display (44)."""
    return MathTex(s, font_size=28 if size < 30 else (36 if size < 40 else 44), color=color)


def fit(m, width=6.2):
    """Shrink a panel item that is wider than the panel."""
    if m.width > width:
        m.scale_to_fit_width(width)
    return m


def neg(s):
    return s.replace("-", "−")


class NSScene(NarratedScene):
    """What the three episodes share: the graph of p, cobwebs, number lines, the cards."""

    # Latin captions: Pango wraps a single over-long line on its own (and the
    # wrapped lines overlap), so keep each caption line short
    caption_units = 30

    SCENES: list = []
    CARDS = ["opening", "closing"]      # not story scenes: no number, no entry in the scene list
    CHAIN: list = []                    # scenes that keep drawing on the stage the one before left
    CORNER_FROM = None                  # the scene that leaves p(x) in the corner
    ASK = ""                            # the question on the title card (LaTeX text)
    ASK_SAY = ""                        # ... and how the voice says it

    def construct(self):
        # KIT_ONLY=the_gap,basins renders just those scenes (see preview.py); what earlier
        # scenes leave on the stage is put up directly
        only = [x for x in os.environ.get("KIT_ONLY", "").split(",") if x]
        if not only:
            self.opening()
            for name in self.SCENES:
                getattr(self, name)()
            self.closing()
            return
        assert all(x in self.SCENES + self.CARDS for x in only), only
        first = only[0]
        after = self.CORNER_FROM in self.SCENES and (first == "closing" or first in self.SCENES
                                                     and self.SCENES.index(first) > self.SCENES.index(self.CORNER_FROM))
        if after:
            self.restore(first)
        if first in self.CHAIN[1:]:
            self.fast_forward(*[getattr(self, x) for x in self.CHAIN[:self.CHAIN.index(first)]])
        for name in only:
            getattr(self, name)()
        self.uncaption()

    def restore(self, first):
        """Put up what the scenes before `first` leave on the stage (single-scene previews)."""
        self.add(self.make_corner())

    def make_corner(self):
        """p(x) in the top right corner; it keeps its place on the screen when the camera moves."""
        corner = MathTex(r"p(x)=\tfrac32x-\tfrac12x^3", font_size=34).to_corner(UR, buff=0.35)
        corner[0][5:].set_color(C_P)
        self.corner = self.pin(corner)
        return corner

    # ------------------------------------------------------------ the cards
    def opening(self):
        """The name and this episode's question, under a circle being pulled into an ellipse.
        No episode number and no list of contents: the story is not given away before it starts."""
        C0, R = np.array([0, 1.55, 0]), 1.05
        ref = Circle(radius=R, color=GREY_B, stroke_width=3).move_to(C0)
        shape = Circle(radius=R, color=C_SIG, stroke_width=5).move_to(C0)
        ell = Ellipse(width=2 * R * 1.5, height=2 * R * 0.55, color=C_SIG, stroke_width=5)
        ell.rotate(30 * DEGREES).move_to(C0)
        name = tex_text("Newton–Schulz", 84, WHITE, bold=True).move_to([0, -0.7, 0])
        ask = fit(tex_text(self.ASK, 44, C_SIG), 12.0).next_to(name, DOWN, buff=0.45)
        tag = txt(series_name(), 24, GREY_B).to_edge(DOWN, buff=0.5)
        self.play(Create(ref), run_time=1.0)
        self.add(shape)
        t0 = self.time
        talk = self.voice("Newton–Schulz. " + self.ASK_SAY)
        self.play(Transform(shape, ell), ref.animate.set_stroke(opacity=0.35), Write(name), run_time=1.8)
        self.play(FadeIn(ask, shift=UP * 0.2), FadeIn(tag))
        self.wait(max(1.2, talk + 1.0 - (self.time - t0)))
        self.play(FadeOut(VGroup(ref, shape, name, ask, tag)), run_time=0.8)
        self.wait(0.4)

    def sign_off(self):
        """The last seconds of an episode: the series tag, then everything fades."""
        self.hold(1.2)
        self.uncaption()
        tag = txt(series_name(), 24, GREY_B).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(tag), run_time=0.6)
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.5)

    def expand(self, box, new, keep=(), run_time=1.8):
        """A zoom that keeps the viewer oriented: `box` marks a region of the picture on
        stage; it grows into the frame of the picture `new` (a VGroup whose first item is
        its axes) while everything else except `keep` fades, and `new` appears inside it."""
        keep_ids = {id(m) for k in keep for m in k.get_family()}
        gone = [m for m in self.mobjects if m is not box and id(m) not in keep_ids]
        target = SurroundingRectangle(new[0], color=box.get_color(), buff=0.12, stroke_width=3)
        self.play(Transform(box, target), *[FadeOut(m) for m in gone], run_time=run_time)
        self.play(FadeIn(new), run_time=0.8)
        self.play(FadeOut(box), run_time=0.5)

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

    # ------------------------------------------------------------ 8. the gap between √3 and √5
    def gap_marks(self, ax):
        m = VGroup()
        for v, c in ((S3, C_ZERO), (S5, C_S5)):
            m.add(Line(ax.c2p(v, -0.08), ax.c2p(v, 0.08), color=c, stroke_width=4))
        m.add(mt(r"\sqrt3", 30, C_ZERO).move_to(ax.c2p(S3 - 0.3, 0.25)))
        m.add(mt(r"\sqrt5", 30, C_S5).next_to(m[1], UP, buff=0.1))
        return m
