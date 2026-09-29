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

    def construct(self):
        self.title_card(2, "ReLU Ramps Are a Spline Basis", "how a sum of bent lines draws any piecewise-linear curve")
        self.one_ramp()
        self.build_spline()
        self.as_network()
        self.refine()
        self.end_card(
            ["ReLU(z) = max(0, z): flat, then a ramp",
             "An affine map inside ReLU puts the elbow at −b/w",
             "Each ramp adds exactly one slope change",
             "The whole spline is a one-hidden-layer ReLU network"],
            next_title="From ramps to a layer",
        )

    # ---------------------------------------------------------------- 1. one ramp
    def one_ramp(self):
        head = self.heading("One ramp")
        ax = make_axes([-3, 3, 1], [-1, 4, 1], 6.0, 3.4).move_to([-3.0, -0.1, 0])
        xl = txt("z", 24, GREY_B).next_to(ax.x_axis.get_end(), RIGHT, buff=0.15)
        eq = mt(r"\mathrm{ReLU}(z)=\max(0,z)=\begin{cases} z & z\ge 0\\ 0 & z<0\end{cases}", 0.8, C_RAMP)
        eq.scale(0.85).to_edge(RIGHT, buff=0.4).shift(UP * 1.9)
        c = plot(ax, relu, C_RAMP, [-3, 3])
        self.say("The rectified linear unit is the simplest bend there is: zero for negative inputs, and the input itself for positive ones.",
                 Write(head), Create(ax), FadeIn(xl), Create(c), Write(eq))
        self.hold(0.3)
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
        self.say("Put an affine function inside: multiply x by a weight w, add a bias b. Now the bend happens at x = −b / w, the elbow.",
                 ReplacementTransform(c, ramp), FadeIn(elbow), FadeIn(lab))
        w, b = STAGES[1]
        self.say("A bigger weight makes the ramp steeper and, with the same bias, pulls the elbow closer to zero.",
                 Transform(ramp, ramp_curve(ax, w, b)),
                 elbow.animate.move_to(ax.c2p(ELBOWS[1], 0)), Transform(lab, label(w, b, ELBOWS[1])))
        w, b = STAGES[2]
        self.say("A negative weight flips the ramp: it now switches on to the left of its elbow.",
                 Transform(ramp, ramp_curve(ax, w, b)),
                 elbow.animate.move_to(ax.c2p(ELBOWS[2], 0)), Transform(lab, label(w, b, ELBOWS[2])))
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
        self.say("A continuous piecewise-linear function: an intercept, a starting slope, and a slope change at every kink.",
                 Write(head), Create(ax), FadeIn(xl), Create(target), FadeIn(knots), FadeIn(ticks))
        eq = mt(r"g(x)=c+s_0x+\sum_{i=1}^{K}(s_i-s_{i-1})\,\mathrm{ReLU}(x-\tau_i)", 0.75)
        eq.move_to([0, 2.95, 0])
        eq.shift(RIGHT * 0.9)
        self.say("Equation 1.6: a straight line plus one shifted ReLU per kink, each scaled by its slope change.",
                 Write(eq))
        cur = clip_poly(ax, XG, partial(0)(XG), 3.5)
        seg_lab = VGroup(mt(rf"c={fmt(C0)},\ s_0={fmt(SLOPES[0])}", 0.7, C_MODEL)).move_to(ax.c2p(2.0, 3.25))
        self.say(f"Start with the straight line c plus s zero times x. Here c is {fmt(C0)} and the first slope is {fmt(SLOPES[0])}.",
                 Create(cur), FadeIn(seg_lab))
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
        for i in range(3):
            d, t = DELTAS[i], TAUS[i]
            lab = mt(rf"{signed(d)}\cdot\mathrm{{ReLU}}(x-{fmt(t)})", 0.6, C_RAMP).next_to(minis[i], UP, buff=0.08)
            new = clip_poly(ax, XG, partial(i + 1)(XG), 3.5)
            s_from, s_to = SLOPES[i], SLOPES[i + 1]
            cap = (f"At τ{i + 1} = {fmt(t)} the slope must go from {fmt(s_from)} to {fmt(s_to)}: a change of {signed(d)[1:] if d > 0 else '−' + fmt(abs(d))}. "
                   f"Add {signed(d)} times ReLU(x − {fmt(t)}).")
            self.say(cap, Create(minis[i]), Create(term_curves[i]), FadeIn(lab),
                     Transform(cur, new), Flash(ax.c2p(t, float(partial(i + 1)(t))), color=YELLOW_D, flash_radius=0.3))
            self.hold(0.3)
        assert np.allclose(partial(3)(XG), T["g"](XG))
        self.say("Before its elbow a ramp is zero, so earlier pieces stay put. After it, the slope bends exactly as needed.",
                 Circumscribe(cur, color=YELLOW_D, time_width=1.2))
        self.hold(0.6)
        self.clear_stage()

    # ---------------------------------------------------------------- 3. as a network
    def as_network(self):
        head = self.heading("It is already a neural network")
        eq1 = mt(r"g(x)=c+s_0\,x+\sum_i \Delta_i\,\mathrm{ReLU}(x-\tau_i)", 0.9).move_to([0, 2.3, 0])
        self.say("One loose end: that straight-line term s zero times x is not a ReLU. Or is it?", Write(head), Write(eq1))
        eq2 = mt(r"x=\mathrm{ReLU}(x)-\mathrm{ReLU}(-x)", 1.0, C_RAMP).move_to([0, 1.1, 0])
        self.say("It is: x equals ReLU of x minus ReLU of minus x. Positive x survives the first ramp, negative x survives the second.",
                 Write(eq2))
        self.hold(0.3)
        eq3 = mt(r"N_\theta(x)=b^{(2)}+\sum_{i=1}^{d} w^{(2)}_i\,\mathrm{ReLU}\!\left(w^{(1)}_i x+b^{(1)}_i\right)", 0.9).move_to([0, 2.3, 0])
        self.say("So every unit takes the same form: ReLU of a weight times x plus a bias, then a weight on the output. That is Equation 1.7, a one-hidden-layer network.",
                 ReplacementTransform(eq1, eq3), FadeOut(eq2))
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
        self.say(f"{len(UNITS)} hidden units suffice: two for the straight line, one per kink, all read off the slopes and elbows.",
                 FadeIn(table), FadeIn(b2))
        ax = make_axes([0, 6, 1], [0, 3.5, 1], 5.6, 2.9).move_to([3.4, -0.35, 0])
        tgt = DashedVMobject(polyline(ax, XG, T["g"](XG), C_TARGET, 3), num_dashes=70)
        out = polyline(ax, XG, net(XG), C_MODEL, 4)
        self.say("Add up these five units and we recover the spline exactly: same curve, now written as a network.",
                 Create(ax), Create(tgt), Create(out, run_time=2.2))
        self.hold(0.6)
        self.clear_stage()

    # ---------------------------------------------------------------- 4. refine
    def refine(self):
        head = self.heading("Any continuous curve, given enough ramps")
        ax = make_axes([0, 6, 1], [-0.5, 3, 1], 7.6, 3.4).move_to([-1.6, -0.1, 0])
        tgt = plot(ax, f, C_TARGET, [0, 6], width=3)
        self.say("Real targets are smooth, not piecewise linear. But on a closed interval we can approximate one by a piecewise-linear curve with many kinks.",
                 Write(head), Create(ax), Create(DashedVMobject(tgt, num_dashes=60)))
        cur = None
        info = None
        for K in (3, 6, 12):
            sp, e = REFINE[K]
            new = polyline(ax, XG, sp["g"](XG), C_MODEL, 4)
            new_info = VGroup(txt(f"kinks K = {K}", 26, C_TEXT), txt(f"hidden units d = {K + 2}", 26, C_RAMP),
                              txt(f"max error = {e:.2f}", 26, C_LOSS)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.6).shift(UP * 1.4)
            cap = {3: f"With {K} kinks and {K + 2} hidden units the fit is rough.",
                   6: f"With {K} kinks the curve already hugs the target much better.",
                   12: f"With {K} kinks the worst-case error is down to {e:.2f}. More ramps, better fit."}[K]
            if cur is None:
                cur, info = new, new_info
                self.say(cap, Create(cur, run_time=1.6), FadeIn(info))
            else:
                self.say(cap, Transform(cur, new), Transform(info, new_info))
            self.hold(0.3)
        info.generate_target()
        remark = VGroup(*[txt(t, 24, YELLOW_D if k == 0 else C_TEXT) for k, t in enumerate(
            ["Existence, not training:", "a wide enough network can", "represent the curve, but", "gradient descent need not", "find these weights."])]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(RIGHT, buff=0.5)
        remark.move_to([info.get_center()[0], -1.05, 0])
        assert remark.get_bottom()[1] > -2.85 and remark.get_right()[0] < 7.0
        self.say("A caution: this says a wide enough network can represent the curve. It does not say gradient descent will find those weights.",
                 FadeIn(remark))
        self.hold(0.6)
        self.clear_stage()
