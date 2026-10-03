"""Episode 2 — ReLU Ramps Are a Spline Basis (Note 1, section 1.2)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers


def spline(nx, ny):
    """Continuous piecewise-linear function through nodes -> parameters of Eq. (1.6)."""
    nx, ny = np.asarray(nx, float), np.asarray(ny, float)
    slopes = np.diff(ny) / np.diff(nx)
    c, s0, taus = ny[0] - slopes[0] * nx[0], slopes[0], nx[1:-1]
    deltas = np.diff(slopes)

    def g(x):
        x = np.asarray(x, float)
        out = c + s0 * x
        for t, d in zip(taus, deltas):
            out = out + d * relu(x - t)
        return out

    return dict(c=c, s0=s0, taus=taus, slopes=slopes, deltas=deltas, g=g, nx=nx, ny=ny)


TAUS = [1.0, 2.5, 4.0]
SLOPES = [0.2, 1.4, -0.8, 0.6]
C0 = 0.5
NODES_X = [0.0] + TAUS + [6.0]
NODES_Y = [C0]
for k in range(4):
    NODES_Y.append(NODES_Y[-1] + SLOPES[k] * (NODES_X[k + 1] - NODES_X[k]))
T = spline(NODES_X, NODES_Y)
assert np.allclose(T["slopes"], SLOPES) and np.isclose(T["c"], C0)
XG = np.linspace(0, 6, 601)
assert np.allclose(T["g"](XG), np.interp(XG, NODES_X, NODES_Y))          # Eq. (1.6) == the piecewise-linear curve
DELTAS = T["deltas"]                                                      # 1.2, -2.2, 1.4
assert np.allclose(DELTAS, [1.2, -2.2, 1.4])


def partial(k):
    """Running sum after adding the first k ramps."""
    return lambda x: T["c"] + T["s0"] * np.asarray(x, float) + sum(
        DELTAS[i] * relu(np.asarray(x, float) - TAUS[i]) for i in range(k))


# one-hidden-layer form, Eq. (1.7): units are (w1, b1, w2), plus output bias b2
UNITS = [(1.0, 0.0, T["s0"]), (-1.0, 0.0, -T["s0"])] + [(1.0, -t, d) for t, d in zip(TAUS, DELTAS)]
B2 = T["c"]


def net(x):
    x = np.asarray(x, float)
    return B2 + sum(w2 * relu(w1 * x + b1) for w1, b1, w2 in UNITS)


assert np.allclose(net(XG), T["g"](XG))                                   # 5 hidden units reproduce g exactly
assert len(UNITS) == len(TAUS) + 2

# a ramp: elbow at -b/w
STAGES = [(1.0, -2.0), (2.0, -2.0), (-1.5, 3.0)]
ELBOWS = [-b / w for w, b in STAGES]
assert ELBOWS == [2.0, 1.0, 2.0]

# refining a smooth target
f = lambda x: np.sin(x) + 0.35 * x
REFINE = {}
for K in (3, 6, 12):
    nx = np.linspace(0, 6, K + 2)
    sp = spline(nx, f(nx))
    assert np.allclose(sp["g"](XG), np.interp(XG, nx, f(nx)))
    REFINE[K] = (sp, float(np.max(np.abs(f(XG) - sp["g"](XG)))))
assert REFINE[3][1] > REFINE[6][1] > REFINE[12][1]


def fmt(v):
    return f"{v:g}"


def clip_poly(ax, xs, ys, ymax, color=C_MODEL, width=4):
    """Polyline of the part of (xs, ys) that stays at or below ymax (the curve leaves through the top edge)."""
    xs, ys = np.asarray(xs), np.asarray(ys)
    keep = ys <= ymax
    return polyline(ax, xs[keep], ys[keep], color, width)


def ramp_curve(ax, w, b, ymax=3.9):
    xs = np.linspace(-3, 3, 601)
    return clip_poly(ax, xs, relu(w * xs + b), ymax, C_RAMP, 4)


def wx(w):
    return {1.0: "x", -1.0: "-x"}.get(w, f"{fmt(w)}\,x")


def signed(v):
    return ("+" if v >= 0 else "-") + f"{abs(v):g}"


class Ep02ReluRamps(NarratedScene):
    series = SERIES
    SCENES = ["one_ramp", "build_spline", "as_network", "refine"]

    def construct(self):
        self.title_card()
        self.one_ramp()
        self.build_spline()
        self.as_network()
        self.refine()
        self.end_card(
            ["A ramp is one ReLU unit: flat, then a slope",
             "ReLU(w x + b) bends at x = minus b over w",
             "Each ramp adds one slope change and leaves everything left of its knot alone",
             "Any spline is already a one-hidden-layer ReLU net. Existence, not training"],
        )

    # ---------------------------------------------------------------- 1. one ramp
    def one_ramp(self):
        head = self.heading("One ramp")
        ax = make_axes([-3, 3, 1], [-1, 4, 1], 6.0, 3.4).move_to([-3.0, -0.1, 0])
        xl = txt("z", 24, GREY_B).next_to(ax.x_axis.get_end(), RIGHT, buff=0.15)
        eq = mt(r"\mathrm{ReLU}(z)=\max(0,z)=\begin{cases} z & z\ge 0\\ 0 & z<0\end{cases}", 0.8, C_RAMP)
        eq.scale(0.85).to_edge(RIGHT, buff=0.4).shift(UP * 1.9)
        c = plot(ax, relu, C_RAMP, [-3, 3])
        w, b = STAGES[0]
        ramp = ramp_curve(ax, w, b)
        elbow = Dot(ax.c2p(ELBOWS[0], 0), color=YELLOW_D, radius=0.11)

        def label(w, b, el):
            side = "x > τ" if w > 0 else "x < τ"
            return VGroup(
                mt(rf"g(x)=\mathrm{{ReLU}}({wx(w)}{signed(b)})", 0.8, C_RAMP),
                mt(rf"\tau=-b/w={fmt(el)}", 0.8, YELLOW_D),
                txt(f"active where {side}", 26, GREY_A),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.7)

        lab = label(w, b, ELBOWS[0])
        self.say("What's the simplest bend you can put in a straight line? It's this one, called ReLU, which "
                 "stays at zero on the left and then just copies its input. Now feed it w times x plus b "
                 "instead of the plain input, and we get one ramp, which is a single ReLU unit.",
                 Write(head), Create(ax), FadeIn(xl), Create(c), Write(eq))
        self.cue("Now feed it", ReplacementTransform(c, ramp), FadeIn(elbow), FadeIn(lab))
        self.say("So where does the ramp bend? It bends right where the inside hits zero, and that happens at x "
                 "equals minus b over w. We'll call that point the knot.",
                 Indicate(elbow, color=RED_C, scale_factor=2.0))
        self.hold(0.3)
        w, b = STAGES[1]
        w2, b2 = STAGES[2]
        self.say("If we turn up the weight, the ramp gets steeper, and with the same bias the knot slides in "
                 "toward zero. If we make the weight negative, the ramp flips over, so now it switches on to "
                 "the left of its knot.",
                 Transform(ramp, ramp_curve(ax, w, b)),
                 elbow.animate.move_to(ax.c2p(ELBOWS[1], 0)), Transform(lab, label(w, b, ELBOWS[1])))
        self.cue("If we make the weight negative", Transform(ramp, ramp_curve(ax, w2, b2)),
                 elbow.animate.move_to(ax.c2p(ELBOWS[2], 0)), Transform(lab, label(w2, b2, ELBOWS[2])))
        self.say("You might wonder why we use ReLU and not the older sigmoid or hyperbolic tangent. Those curves flatten out "
                 "for big inputs, so their gradients shrink, and after enough layers the gradient fades away. "
                 "ReLU's slope is exactly one wherever the unit is on, so gradients pass straight through.",
                 Indicate(ramp, color=YELLOW_D, scale_factor=1.0))
        self.cue("ReLU's slope is exactly one", Indicate(ramp, color=YELLOW_D, scale_factor=1.0))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 2. build the spline
    def build_spline(self):
        head = self.heading("Bend by bend")
        ax = make_axes([0, 6, 1], [0, 3.5, 1], 6.6, 3.3).move_to([-2.6, -0.15, 0])
        xl = txt("x", 24, GREY_B).next_to(ax.x_axis.get_end(), RIGHT, buff=0.15)
        target = DashedVMobject(polyline(ax, NODES_X, NODES_Y, C_TARGET, 3), num_dashes=70)
        knots = VGroup(*[Dot(ax.c2p(x, y), radius=0.07, color=C_TARGET) for x, y in zip(NODES_X[1:-1], NODES_Y[1:-1])])
        ticks = VGroup(*[txt(f"τ{i + 1}={fmt(t)}", 20, GREY_B).next_to(ax.c2p(t, 0), DOWN, buff=0.15) for i, t in enumerate(TAUS)])
        eq = mt(r"g(x)=c+s_0x+\sum_{i=1}^{K}(s_i-s_{i-1})\,\mathrm{ReLU}(x-\tau_i)", 0.75)
        eq.move_to([0, 2.95, 0])
        eq.shift(RIGHT * 0.9)
        self.say("The idea is that any curve made of straight pieces is just a starting height, a starting slope, "
                 "and a slope change at each knot. The notes write this as equation one point six. It's a "
                 "straight line plus one ramp per knot, and each ramp is scaled by how much the slope changes "
                 "there.",
                 Write(head), Create(ax), FadeIn(xl), Create(target), FadeIn(knots), FadeIn(ticks))
        self.cue("The notes write this", Write(eq))
        cur = clip_poly(ax, XG, partial(0)(XG), 3.5)
        seg_lab = VGroup(mt(rf"c={fmt(C0)},\ s_0={fmt(SLOPES[0])}", 0.7, C_MODEL)).move_to(ax.c2p(4.7, 3.2))
        # mini axes for each ramp term
        minis, term_curves = [], []
        for i in range(3):
            vals = DELTAS[i] * relu(XG - TAUS[i])
            lo, hi = min(0.0, vals.min()), max(0.0, vals.max())
            pad = (hi - lo) * 0.1
            mx = make_axes([0, 6, 6], [lo - pad, hi + pad, hi - lo + 2 * pad], 3.0, 0.85, stroke_width=1.5)
            mx.move_to([4.9, 1.05 - i * 1.4, 0])
            minis.append(mx)
            term_curves.append(polyline(mx, XG, vals, C_RAMP, 3))

        def add_ramp(i):
            d, t = DELTAS[i], TAUS[i]
            lab = mt(rf"{signed(d)}\cdot\mathrm{{ReLU}}(x-{fmt(t)})", 0.6, C_RAMP).next_to(minis[i], UP, buff=0.08)
            new = clip_poly(ax, XG, partial(i + 1)(XG), 3.5)
            return (Create(minis[i]), Create(term_curves[i]), FadeIn(lab), Transform(cur, new),
                    Flash(ax.c2p(t, float(partial(i + 1)(t))), color=YELLOW_D, flash_radius=0.3))

        # spoken numbers below
        assert (C0, SLOPES[0], SLOPES[1], TAUS[0]) == (0.5, 0.2, 1.4, 1.0) and np.isclose(DELTAS[0], 1.2)
        self.say("Let's build this curve one bend at a time, starting with just the straight line. It begins at "
                 "one half and climbs with a gentle slope of zero point two. At x equals one, the slope jumps "
                 "from zero point two to one point four, so we add a ramp that starts right there, scaled "
                 "by one point two.",
                 Create(cur), FadeIn(seg_lab))
        self.cue("At x equals one", *add_ramp(0))
        self.hold(0.3)
        assert (TAUS[1], SLOPES[2], TAUS[2], SLOPES[3]) == (2.5, -0.8, 4.0, 0.6) and np.allclose(DELTAS[1:], [-2.2, 1.4])
        self.say("At two point five, the slope drops from one point four to minus zero point eight, so the next "
                 "ramp gets a negative weight, minus two point two. And at four the slope climbs back up to "
                 "zero point six, which takes one last ramp with weight one point four.",
                 *add_ramp(1))
        self.cue("And at four", *add_ramp(2))
        self.hold(0.3)
        assert np.allclose(partial(3)(XG), T["g"](XG))
        self.say("And the reason this works is that a ramp is exactly zero before its knot. So adding a new ramp "
                 "can never disturb the part of the curve we've already built.",
                 Circumscribe(cur, color=YELLOW_D, time_width=1.2))
        self.hold(0.6)
        self.clear_stage()

    # ---------------------------------------------------------------- 3. as a network
    def as_network(self):
        head = self.heading("It is already a neural network")
        eq1 = mt(r"g(x)=c+s_0\,x+\sum_i \Delta_i\,\mathrm{ReLU}(x-\tau_i)", 0.9).move_to([0, 2.3, 0])
        eq2 = mt(r"x=\mathrm{ReLU}(x)-\mathrm{ReLU}(-x)", 1.0, C_RAMP).move_to([0, 1.1, 0])
        self.say("There's one loose end, because the straight-line piece doesn't look like a ReLU at all. But "
                 "it can be written as two of them. Any number x equals ReLU of x, minus ReLU of minus x. So "
                 "one ramp covers the right side and the other covers the left.",
                 Write(head), Write(eq1))
        self.cue("Any number x equals", Write(eq2))
        self.hold(0.3)
        eq3 = mt(r"N_\theta(x)=b^{(2)}+\sum_{i=1}^{d} w^{(2)}_i\,\mathrm{ReLU}\!\left(w^{(1)}_i x+b^{(1)}_i\right)", 0.9).move_to([0, 2.3, 0])
        cols_x = [0.0, 1.5, 3.0, 4.5]
        table = VGroup()
        for j, h in enumerate(["unit", "w1", "b1", "w2"]):
            table.add(mono(h, 26, GREY_B).move_to([cols_x[j], 0, 0]))
        for i, (w1, b1, w2) in enumerate(UNITS):
            col = BLUE_B if i < 2 else C_RAMP
            for j, v in enumerate([str(i + 1), f"{w1:.1f}", f"{b1:.1f}", f"{w2:.1f}"]):
                table.add(mono(v, 26, col).move_to([cols_x[j], -0.46 * (i + 1), 0]))
        table.move_to([-4.0, -0.15, 0])
        b2 = mono(f"b2 = {B2:.1f}", 26, GREY_A).next_to(table, DOWN, buff=0.25).align_to(table, LEFT)
        assert b2.get_bottom()[1] > -2.85
        assert len(UNITS) == 5                               # spoken: "five hidden units"
        self.say("Now every term is a scaled ReLU of w times x plus b, and that shape has a name. It's called a "
                 "one-hidden-layer network. Ours needs five hidden units, two for the line and one for each "
                 "knot, and every weight is read straight off the picture.",
                 ReplacementTransform(eq1, eq3), FadeOut(eq2))
        self.cue("Ours needs five hidden units", FadeIn(table), FadeIn(b2))
        ax = make_axes([0, 6, 1], [0, 3.5, 1], 5.6, 2.9).move_to([3.4, -0.35, 0])
        tgt = DashedVMobject(polyline(ax, XG, T["g"](XG), C_TARGET, 3), num_dashes=70)
        out = polyline(ax, XG, net(XG), C_MODEL, 4)
        self.say("Add the five units up, and out comes exactly the same curve. Nothing was learned here. We "
                 "just took the spline and wrote it down as a network.",
                 Create(ax), Create(tgt), Create(out, run_time=2.2))
        self.hold(0.6)
        self.clear_stage()

    # ---------------------------------------------------------------- 4. refine
    def refine(self):
        head = self.heading("Any continuous curve, given enough ramps")
        ax = make_axes([0, 6, 1], [-0.5, 3, 1], 7.6, 3.4).move_to([-1.6, -0.1, 0])
        tgt = plot(ax, f, C_TARGET, [0, 6], width=3)
        self.say("But real targets curve smoothly, so can straight pieces keep up? On a closed interval they "
                 "can, as long as we keep adding knots.",
                 Write(head), Create(ax), Create(DashedVMobject(tgt, num_dashes=60)))

        def stage(K):
            sp, e = REFINE[K]
            new = polyline(ax, XG, sp["g"](XG), C_MODEL, 4)
            new_info = VGroup(txt(f"knots K = {K}", 26, C_TEXT), txt(f"hidden units d = {K + 2}", 26, C_RAMP),
                              txt(f"max error = {e:.2f}", 26, C_LOSS)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.6).shift(UP * 1.4)
            return new, new_info

        cur, info = stage(3)
        assert f"{REFINE[12][1]:.2f}" == "0.03"               # spoken: "zero point zero three"
        self.say("With three knots, which means five hidden units, the fit is pretty rough. With six knots it's "
                 "already hugging the curve. And with twelve, the worst miss is down to zero point zero three, "
                 "so more ramps really do mean a better fit.",
                 Create(cur, run_time=1.6), FadeIn(info))
        new, new_info = stage(6)
        self.cue("With six knots", Transform(cur, new), Transform(info, new_info))
        new, new_info = stage(12)
        self.cue("And with twelve", Transform(cur, new), Transform(info, new_info))
        self.hold(0.3)
        info.generate_target()
        remark = VGroup(*[txt(t, 24, YELLOW_D if k == 0 else C_TEXT) for k, t in enumerate(
            ["Existence, not training:", "a wide enough network can", "represent the curve, but", "a finite net may fall short,", "and descent may miss it."])]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(RIGHT, buff=0.5)
        remark.to_edge(RIGHT, buff=0.6).set_y(-1.05)
        assert remark.get_bottom()[1] > -2.85 and remark.get_right()[0] <= 6.7 and info.get_right()[0] <= 6.7
        self.say("But be careful about what this says. It's a statement about existence, which means some wide "
                 "enough network can draw the curve. It doesn't say your network is wide enough, and it doesn't "
                 "say gradient descent will ever find those weights.",
                 FadeIn(remark))
        self.cue("It doesn't say your network", Indicate(remark, color=YELLOW_D, scale_factor=1.0))
        self.hold(0.6)
        self.clear_stage()
