"""Episode 2 — Engineering or Alchemy? (Lecture 0: history timeline, the stir-the-pile comic, what the course is for)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers

# (a) timeline (dates from the lecture slide)
Y0, Y1 = 1950, 2015
TOP, BOT = 2.55, -2.1


def year_y(yr):
    return TOP + (yr - Y0) * (BOT - TOP) / (Y1 - Y0)


GAP_PA = 2012 - 1957
GAP_BL = 1986 - 1969
assert GAP_PA == 55 and GAP_BL == 17

# (b) XOR: one linear element cannot get all four right, two ramps plus a readout can
XOR_PTS = [(0, 0), (1, 1), (0, 1), (1, 0)]
XOR_Y = [-1, -1, 1, 1]


def n_wrong_line(w, b):
    return sum(1 for (x1, x2), y in zip(XOR_PTS, XOR_Y) if np.sign(w[0] * x1 + w[1] * x2 + b + 1e-9) != y)


_best = {}
for th in np.linspace(0, 2 * np.pi, 360, endpoint=False):
    for b in np.linspace(-2.2, 2.2, 89):
        w = (np.cos(th), np.sin(th))
        m = n_wrong_line(w, b)
        _best[m] = _best.get(m, 0) + 1
        if m == 1 and "line" not in _best:
            pass
assert 0 not in _best and 1 in _best            # no line gets all four right; some get three


def one_wrong_line(idx):
    """A line that gets XOR point `idx` wrong and the other three right (search over angles and offsets)."""
    for th in np.linspace(0, 2 * np.pi, 720, endpoint=False):
        for b in np.linspace(-2.2, 2.2, 177):
            w = (np.cos(th), np.sin(th))
            wrong = [i for i, ((x1, x2), y) in enumerate(zip(XOR_PTS, XOR_Y)) if np.sign(w[0] * x1 + w[1] * x2 + b + 1e-9) != y]
            if wrong == [idx]:
                return np.array(w), float(b)
    raise AssertionError(idx)


LINES = [one_wrong_line(i) for i in range(4)]


def xor_net(x1, x2):
    h1, h2 = relu(x1 + x2), relu(x1 + x2 - 1)
    return h1, h2, h1 - 2 * h2


TABLE = [(x1, x2, *xor_net(x1, x2)) for x1, x2 in XOR_PTS]
assert [t[4] for t in TABLE] == [0, 0, 1, 1] and [t[2] for t in TABLE] == [0, 2, 1, 1] and [t[3] for t in TABLE] == [0, 1, 0, 0]
assert all((t[4] > 0.5) == (y > 0) for t, y in zip(TABLE, XOR_Y))

# (c) gradient descent on L(w) = 2 w^2 (curvature 4): w <- (1 - 4 eta) w
ETAS = [0.1, 0.4, 0.5, 0.6]
FACT = [1 - 4 * e for e in ETAS]
assert np.allclose(FACT, [0.6, -0.6, -1.0, -1.4])
TRAJ = {e: [1.0 * (1 - 4 * e) ** k for k in range(11)] for e in ETAS}
# check the closed form against real gradient steps
for e in ETAS:
    w = 1.0
    for k in range(10):
        w = w - e * 4 * w                       # L'(w) = 4 w
    assert abs(w - TRAJ[e][10]) < 1e-9
assert abs(TRAJ[0.1][10]) < 0.01 and abs(TRAJ[0.4][10]) < 0.01
assert abs(abs(TRAJ[0.5][10]) - 1.0) < 1e-12 and 28 < TRAJ[0.6][10] < 29.5
ETA_MAX = 2 / 4
assert ETA_MAX == 0.5

C_ETA = {0.1: GREEN_B, 0.4: TEAL_B, 0.5: YELLOW_D, 0.6: RED_C}


def fmt(v):
    return f"{v:.1f}".replace("-", "−")


def pline(ax, xs, ys, color, width=4):
    return polyline(ax, xs, ys, color, width)


def box_line(w, b, lo, hi):
    """Endpoints of w.x + b = 0 clipped to the square [lo, hi]^2."""
    c = []
    for xv in (lo, hi):
        if abs(w[1]) > 1e-9:
            yv = -(w[0] * xv + b) / w[1]
            if lo - 1e-9 <= yv <= hi + 1e-9:
                c.append((xv, yv))
    for yv in (lo, hi):
        if abs(w[0]) > 1e-9:
            xv = -(w[1] * yv + b) / w[0]
            if lo - 1e-9 <= xv <= hi + 1e-9 and all(abs(xv - p[0]) + abs(yv - p[1]) > 1e-6 for p in c):
                c.append((xv, yv))
    assert len(c) >= 2
    return c[0], c[1]


def marker(ax, p, y, color=C_DATA, s=0.15):
    c = ax.c2p(p[0], p[1])
    if y > 0:
        return Circle(radius=s, stroke_color=color, stroke_width=3, fill_opacity=0).move_to(c)
    return VGroup(Line(c + np.array([-s, -s, 0]), c + np.array([s, s, 0]), color=color, stroke_width=3),
                  Line(c + np.array([-s, s, 0]), c + np.array([s, -s, 0]), color=color, stroke_width=3))


class Ep02Alchemy(NarratedScene):
    series = SERIES

    def construct(self):
        self.title_card()
        self.timeline()
        self.limit()
        self.pile()
        self.learning_rate()
        self.course()
        self.reading()
        self.end_card(
            ["Learned circuits are an old idea: 55 years from perceptron to AlexNet",
             "One element draws one line; stacked elements do more",
             "Alchemy stirs the pile; engineering explains the knob",
             "This course: design, visualize and understand deep networks"],
        )

    # ---------------------------------------------------------------- 1. timeline
    def timeline(self):
        head = self.heading("A short history")
        ax_x = -5.7
        axis = Arrow([ax_x, year_y(1946), 0], [ax_x, year_y(2018), 0], buff=0, color=GREY_B, stroke_width=3,
                     max_tip_length_to_length_ratio=0.05)
        ticks = VGroup()
        for yr in range(1950, 2011, 10):
            ticks.add(txt(str(yr), 20, GREY_B).move_to([ax_x - 0.6, year_y(yr), 0]),
                      Line([ax_x - 0.1, year_y(yr), 0], [ax_x + 0.1, year_y(yr), 0], color=GREY_B))
        events = [
            ("1950", 1950, "Turing: learning as a path to machine intelligence", WHITE),
            ("1957", 1957, "Rosenblatt's perceptron; LMS in adaptive signal processing", WHITE),
            ("1969", 1969, "Minsky and Papert: fundamental limits of neural networks", WHITE),
            ("1986", 1986, "Backpropagation: a practical way to train deep nets", WHITE),
            ("1989", 1989, "LeNet: a neural network reads handwriting", WHITE),
            ("1990s", 1998, "probabilistic and convex methods, mostly shallow models", GREY_A),
            ("~2006", 2006, "Deep neural networks start gaining attention", WHITE),
            ("2012", 2012, "AlexNet beats all other methods on ImageNet", WHITE),
        ]
        # dodge labels so that they never touch
        ys, prev = [], 9.0
        for _, yr, _, _ in events:
            y = min(year_y(yr), prev - 0.5)
            ys.append(y)
            prev = y
        assert ys[-1] > -2.2
        items = []
        for (lab, yr, desc, col), y in zip(events, ys):
            d = Dot([ax_x, year_y(yr), 0], radius=0.07, color=YELLOW_D)
            yl = txt(lab, 24, YELLOW_D)
            ds = txt(desc, 23, col)
            row = VGroup(yl, ds).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
            row.move_to([0, y, 0]).align_to([-4.85, 0, 0], LEFT)
            assert row.get_right()[0] < 5.2, (lab, row.get_right()[0])
            lead = Line(d.get_center() + RIGHT * 0.08, [row.get_left()[0] - 0.1, y, 0], color=GREY_D, stroke_width=2)
            items.append(VGroup(d, lead, row))
        span = Rectangle(width=0.14, height=year_y(1990) - year_y(2006), fill_color=GREY_C, fill_opacity=0.5, stroke_width=0
                         ).move_to([ax_x + 0.12, (year_y(1990) + year_y(2006)) / 2, 0])

        def show(*ix, cap, extra=()):
            self.say(cap, *[FadeIn(items[i], shift=RIGHT * 0.2) for i in ix], *extra)

        self.say("The idea is old. In 1950, Turing describes learning as a path to machine intelligence.",
                 Write(head), Create(axis), FadeIn(ticks), FadeIn(items[0], shift=RIGHT * 0.2))
        show(1, cap="In 1957 Rosenblatt proposes the perceptron. In the same years, L M S appears in adaptive signal processing.")
        show(2, cap="In 1969, Minsky and Papert publish a book on the fundamental limitations of neural networks.")
        show(3, 4, cap="In 1986, backpropagation becomes a practical way to train deep networks, and in 1989 LeNet reads handwriting.")
        show(5, cap="Then attention shifted to probabilistic methods and convex optimization, mostly on shallow models.",
             extra=(FadeIn(span),))
        show(6, 7, cap="Around 2006 deep networks regain attention; in 2012 Krizhevsky's AlexNet beats all methods on ImageNet.")
        x_arrow = 6.0
        y57, y12 = year_y(1957), year_y(2012)
        dbl = DoubleArrow([x_arrow, y57, 0], [x_arrow, y12, 0], buff=0, color=YELLOW_D, stroke_width=3, tip_length=0.2)
        lab = txt(f"{GAP_PA} years", 26, YELLOW_D).rotate(PI / 2).move_to([x_arrow + 0.45, (y57 + y12) / 2, 0])
        assert lab.get_right()[0] < 7.0
        self.say(f"From the perceptron to AlexNet is {GAP_PA} years. The idea of a learned circuit is old; the breakthrough is recent.",
                 Create(dbl), FadeIn(lab))
        self.hold(0.6)
        self.clear_stage()

    # ---------------------------------------------------------------- 2. the limit of 1969
    def limit(self):
        head = self.heading("What one element cannot do")
        ax = Axes(x_range=[-0.5, 1.5, 1], y_range=[-0.5, 1.5, 1], x_length=4.2, y_length=4.2,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2, "include_numbers": False}
                  ).move_to([-3.6, 0.35, 0])
        pts = VGroup(*[marker(ax, p, y) for p, y in zip(XOR_PTS, XOR_Y)])
        tags = VGroup(*[txt(f"({p[0]}, {p[1]})", 20, GREY_B).next_to(ax.c2p(*p), DL if k < 2 else (UL if p == (0, 1) else DR), buff=0.12)
                        for k, p in enumerate(XOR_PTS)])
        rule = txt("+1 exactly when one input is on", 24, GREY_A).next_to(ax, RIGHT, buff=0.5).align_to(ax, UP).shift(DOWN * 0.3)
        assert rule.get_right()[0] < 7.0
        self.say("What limit was 1969 about? Take four points labeled exclusive or: plus one when exactly one input is on.",
                 Write(head), Create(ax), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.15), FadeIn(tags), FadeIn(rule))

        def ln(i):
            w, b = LINES[i]
            p, q = box_line(w, b, -0.5, 1.5)
            return Line(ax.c2p(*p), ax.c2p(*q), color=C_MODEL, stroke_width=5)

        def ring(i):
            return Circle(0.3, color=C_LOSS, stroke_width=4).move_to(ax.c2p(*XOR_PTS[i]))

        cur, rg = ln(0), ring(0)
        verdict = VGroup(txt("best any single line can do:", 24, GREY_B), txt("3 of 4 correct", 34, C_LOSS)
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(rule, DOWN, buff=0.6).align_to(rule, LEFT)
        assert verdict.get_right()[0] < 7.0
        self.say("One element draws one line. Try every line: some get three points right, none gets all four.",
                 Create(cur), FadeIn(rg), FadeIn(verdict))
        for i in range(1, 4):
            self.play(Transform(cur, ln(i)), Transform(rg, ring(i)), run_time=0.9)
        self.hold(0.3)
        self.clear_stage()
        # two ramps and a readout
        head = self.heading("Stack two elements")
        hdrs = ["x₁", "x₂", "h₁", "h₂", "y"]
        colx = [-6.0, -5.0, -3.7, -2.6, -1.4]
        cols = [GREY_B, GREY_B, C_RAMP, C_RAMP, C_MODEL]
        hd = VGroup(*[txt(h, 26, c).move_to([x, 1.95, 0]) for h, x, c in zip(hdrs, colx, cols)])
        rows = []
        for r, t in enumerate(TABLE):
            y = 1.35 - 0.55 * r
            rows.append(VGroup(*[txt(str(int(v)), 28, c).move_to([x, y, 0]) for v, x, c in zip(t, colx, [WHITE, WHITE, C_RAMP, C_RAMP, C_MODEL])]))
        pos = {"x1": [1.6, 1.85], "x2": [1.6, 0.35], "h1": [3.8, 1.85], "h2": [3.8, 0.35], "y": [6.0, 1.1]}
        nodes = {k: Circle(0.32, color=(GREY_B if k[0] == "x" else C_RAMP if k[0] == "h" else C_MODEL), stroke_width=3).move_to(v + [0])
                 for k, v in pos.items()}
        nlab = {k: mt({"x1": "x_1", "x2": "x_2", "h1": "h_1", "h2": "h_2", "y": "y"}[k], 0.7, WHITE).move_to(nodes[k]) for k in nodes}
        edges = VGroup(*[Line(nodes[a].get_right(), nodes[b].get_left(), color=GREY_B, stroke_width=2)
                         for a, b in [("x1", "h1"), ("x1", "h2"), ("x2", "h1"), ("x2", "h2"), ("h1", "y"), ("h2", "y")]])
        net = VGroup(edges, *nodes.values(), *nlab.values())
        eqs = VGroup(mts([r"h_1=\mathrm{ReLU}(x_1+x_2)"], 0.7, {0: C_RAMP}),
                     mts([r"h_2=\mathrm{ReLU}(x_1+x_2-1)"], 0.7, {0: C_RAMP}),
                     mts([r"y=h_1-2\,h_2"], 0.7, {0: C_MODEL})).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.7, -1.0, 0])
        assert eqs.get_right()[0] < 6.9 and eqs.get_bottom()[1] > -2.4 and net.get_right()[0] < 6.9
        self.say("Stack two ramps on x1 plus x2, the second bending at 1, and read out first minus twice the second.",
                 Write(head), FadeIn(net), Write(eqs))
        self.say("Compute the four rows: y comes out 0, 0, 1, 1. That is exclusive or, exactly, with no line in sight.",
                 FadeIn(hd), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.4))
        self.say("One element cannot, a stack can. Making stacks trainable is what backpropagation did in 1986.",
                 *[Indicate(r[4], color=GREEN_C) for r in rows])
        self.hold(0.6)
        self.clear_stage()

    # ---------------------------------------------------------------- 3. the pile
    def pile(self):
        head = self.heading("Engineering or alchemy?")
        xs = np.linspace(-2.4, 2.4, 60)
        top = [[x, 1.15 * np.exp(-x * x / 1.3), 0] for x in xs]
        body = VMobject(stroke_color=GREY_B, stroke_width=3, fill_color=GREY_D, fill_opacity=0.5)
        body.set_points_as_corners(top + [[2.4, 0, 0], [-2.4, 0, 0], top[0]])
        rng = np.random.RandomState(2)
        specks = VGroup()
        for (x, y, v) in [(-1.3, 0.12, "0.3"), (-0.6, 0.45, "7"), (0.1, 0.8, "4"), (0.7, 0.4, "−1"), (1.4, 0.12, "2.5"), (-0.1, 0.15, "0.8"), (0.55, 0.85, "−0.2")]:
            specks.add(txt(v, 18, GREY_A).move_to([x, y, 0]))
        pile = VGroup(body, specks).scale(1.5).move_to([0, -0.9, 0])
        funnel = Polygon([-0.5, 0.35, 0], [0.5, 0.35, 0], [0.12, -0.15, 0], [-0.12, -0.15, 0], color=C_DATA, stroke_width=3).move_to([-4.2, 0.85, 0])
        dlab = txt("data", 26, C_DATA).next_to(funnel, UP, buff=0.15)
        a_in = Arrow([-3.6, 0.35, 0], pile.get_left() + [0.9, 0.35, 0], buff=0.1, color=GREY_B, stroke_width=3)
        crate = box_label("answers", GREY_A, w=1.9, h=0.6, font_size=24).move_to([5.5, -1.1, 0])
        a_out = Arrow(pile.get_right() + [-0.4, 0.1, 0], crate.get_left(), buff=0.1, color=GREY_B, stroke_width=3)
        paddle = VGroup(Line([1.0, 1.5, 0], [2.4, -0.1, 0], color=GREY_A, stroke_width=6),
                        Rectangle(width=0.32, height=0.6, color=GREY_A, fill_opacity=0.4, stroke_width=2).move_to([2.5, -0.25, 0]).rotate(-0.9))
        stir = CurvedArrow([-0.9, 0.75, 0], [0.5, 0.75, 0], angle=-PI * 0.8, color=YELLOW_D, stroke_width=4)
        stirt = txt("stir until the answers look right", 26, YELLOW_D).move_to([0, 2.3, 0])
        assert stirt.get_right()[0] < 6.9 and pile.get_bottom()[1] > -2.4 and dlab.get_left()[0] > -6.9
        self.say("Is deep learning engineering, or alchemy? The lecture puts that question next to a famous xkcd comic.",
                 Write(head), speak="Is deep learning engineering, or alchemy? The lecture puts that question next to a famous X K C D comic.")
        self.say("The comic's machine learning system: pour the data into a big pile of linear algebra, collect the answers on the other side.",
                 FadeIn(funnel), FadeIn(dlab), Create(a_in), FadeIn(pile, shift=UP * 0.2), Create(a_out), FadeIn(crate))
        self.say("What if the answers are wrong? Just stir the pile until they start looking right. That is the alchemist's method.",
                 FadeIn(paddle), Create(stir), Write(stirt))
        self.play(Wiggle(paddle, run_time=1.6))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 4. learning rate
    def learning_rate(self):
        head = self.heading("Stirring, with a reason")
        ax = make_axes([0, 10, 1], [-3, 3, 1], 6.4, 3.5).move_to([-3.4, 0.35, 0])
        ticks = tick_labels(ax, [0, 5, 10], 20)
        xl = txt("step k", 22, GREY_B).move_to(ax.c2p(7.5, -3) + DOWN * 0.5)
        yl = txt("w", 24, GREY_B).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        curves = {}
        for e in ETAS:
            ks = [k for k in range(11) if abs(TRAJ[e][k]) <= 3.0]
            curves[e] = pline(ax, ks, [TRAJ[e][k] for k in ks], C_ETA[e])
        dots_ = VGroup(*[Dot(ax.c2p(0, 1), radius=0.08, color=WHITE)])
        eq = mts([r"L(w)=2w^2,\quad w\leftarrow w-", r"\eta", r"L'(w)=(1-4", r"\eta", r")\,w"], 0.62, {1: C_LR, 3: C_LR}).move_to([3.5, 2.55, 0])
        assert eq.get_right()[0] < 6.95 and eq.get_left()[0] > 0.0, (eq.get_left()[0], eq.get_right()[0])
        self.say("The learning rate decides whether training works. Try a bowl, starting from w equals 1.",
                 Write(head), Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl), Write(eq), FadeIn(dots_))
        panel = VGroup()
        for i, e in enumerate(ETAS):
            row = VGroup(txt(f"η = {e}", 26, C_ETA[e]), txt(f"×({fmt(FACT[i])}) per step", 22, GREY_A),
                         txt(f"|w₁₀| = {abs(TRAJ[e][10]):.3g}", 24, WHITE)).arrange(RIGHT, buff=0.3)
            panel.add(row)
        panel.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 0.35, 0]).shift(DOWN * 0.15)
        assert panel.get_right()[0] < 6.95 and panel.get_left()[0] > 0.2, (panel.get_left()[0], panel.get_right()[0])
        self.say("Try four learning rates. 0.1 and 0.4 settle to zero, 0.5 bounces forever, and 0.6 blows up.",
                 LaggedStart(*[Create(curves[e]) for e in ETAS], lag_ratio=0.35, run_time=3.0), FadeIn(panel, lag_ratio=0.3))
        up = Arrow(ax.c2p(3.0, -2.2), ax.c2p(3.4, -2.95), buff=0, color=C_LOSS, stroke_width=4)
        blow = txt(f"w = {TRAJ[0.6][10]:.0f} at step 10", 22, C_LOSS).next_to(up, RIGHT, buff=0.1)
        assert blow.get_right()[0] < 0.5 and blow.get_bottom()[1] > -2.5
        self.play(FadeIn(up), FadeIn(blow))
        rule = mts([r"\text{settles iff }", r"\eta", r"<\tfrac{2}{4}=0.5"], 0.8, {1: C_LR}
                   ).move_to([3.4, -1.85, 0]).align_to(panel, LEFT)
        assert rule.get_right()[0] < 6.95 and rule.get_bottom()[1] > -2.45
        self.say("No magic: each step multiplies w by one minus four eta. It shrinks only while eta stays below two over four, which is 0.5.",
                 Write(rule), Indicate(curves[0.5], color=YELLOW_D))
        self.hold(0.5)
        self.say("That is engineering: a knob with a reason, which predicts where it works and where it fails.",
                 Indicate(rule, color=YELLOW_D))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 5. the course
    def course(self):
        head = self.heading("What the course is for")
        top_c = [C_DATA, C_MODEL, C_NEW]
        top_t = ["a pattern in the data", "circuits set by optimization", "answers on new data"]
        bot_t = ["machine learning\nCS 189", "linear algebra, optimization\nEECS 127", "probability\nEECS 126"]
        xs = [-4.5, 0.0, 4.5]
        tops = VGroup(*[box_label(t, c, w=4.1, h=0.9, font_size=24).move_to([x, 1.6, 0]) for t, c, x in zip(top_t, top_c, xs)])
        bots = VGroup(*[box_label(t, GREY_B, w=4.1, h=1.2, font_size=22).move_to([x, -0.9, 0]) for t, x in zip(bot_t, xs)])
        arrows = VGroup(*[Arrow(b.get_top(), t.get_bottom(), buff=0.12, color=GREY_B, stroke_width=3) for b, t in zip(bots, tops)])
        assert tops.get_right()[0] < 6.9 and bots.get_left()[0] > -6.9
        self.say("Three earlier courses feed this one, and they line up with the definition.",
                 Write(head), LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in tops], lag_ratio=0.25), FadeIn(bots, lag_ratio=0.25), Create(arrows))
        self.say("Machine learning brings the patterns, optimization the circuits and knobs, probability the new data.",
                 *[Indicate(a, color=YELLOW_D) for a in arrows])
        self.hold(0.4)
        self.clear_stage()
        goals = VGroup(*[box_label(t, c, w=3.8, h=1.0, font_size=32) for t, c in
                         [("designing", C_MODEL), ("visualizing", C_RAMP), ("understanding", C_NEW)]]).arrange(RIGHT, buff=0.5).move_to([0, 1.2, 0])
        sub = txt("deep neural networks", 34, WHITE).move_to([0, -0.35, 0])
        assert goals.get_right()[0] < 6.9
        self.say("So the course is about designing, visualizing and understanding deep networks, and knowing why they work.",
                 FadeIn(goals, lag_ratio=0.3), FadeIn(sub))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 6. reading
    def reading(self):
        head = self.heading("One more reading")
        card = Rectangle(width=4.0, height=3.5, stroke_color=GREY_B, stroke_width=2, fill_color=GREY_E, fill_opacity=0.6).move_to([-4.6, 0.5, 0])
        lines = VGroup(txt("MATHEMATICS IN\nTHE AGE OF AI", 24, WHITE, line_spacing=0.9), txt("Terence Tao", 22, GREY_A),
                       txt("arXiv 2608.16753", 22, C_NEW)).arrange(DOWN, buff=0.3).move_to(card)
        for k in range(4):
            lines.add(Line([-6.2, -0.6 - 0.25 * k, 0], [-3.4 - 0.3 * (k % 2), -0.6 - 0.25 * k, 0], color=GREY_D, stroke_width=3))
        assert lines.get_left()[0] > card.get_left()[0] and lines[0].get_right()[0] < card.get_right()[0]
        q1 = txt("How might mathematicians respond to AI tools\nthat can do research-level work?", 26, WHITE, line_spacing=0.9)
        q2 = txt("Set the tools' capabilities aside: what are the goals\nand values of the research itself?", 26, GREY_A, line_spacing=0.9)
        qs = VGroup(q1, q2).arrange(DOWN, aligned_edge=LEFT, buff=0.7).next_to(card, RIGHT, buff=0.5)
        assert qs.get_right()[0] < 7.0, qs.get_right()[0]
        self.say("A companion reading: Terence Tao's essay, Mathematics in the Age of AI.",
                 Write(head), FadeIn(card), FadeIn(lines), FadeIn(q1))
        self.say("It sets aside what AI tools can do and asks what the goals and values of a field are. We can ask the same of deep learning.",
                 FadeIn(q2))
        self.hold(0.6)
