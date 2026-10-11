"""Shared drawing for the State and Timing episodes: waveforms and circuit symbols.

A `Timeline` maps time (ns or ps) to x, so every trace, band, edge line and window
of one diagram agrees. Colours follow PLAN.md (one colour per concept).

    tl = Timeline(0, 32, x_left=-5, width=10)
    clk = clock_wave(tl, period=8, y=1.5)                 # rising edges at 0, 8, 16, ...
    d = bit_trace(tl, [(0, 0), (3, 1), (11, 0)], y=0.5)   # (time, level) changes
    s = bus_band(tl, [(0, 2, "0"), (2, 4, "3")], y=-0.5)  # one cell per value, s[i] to animate
"""
from manim import *

from manim_kit import BG, num
from manim_kit import txt as _kit_txt

FRAME_W = 14.2222     # the whole frame, in scene units


def txt(s, size=40, color=WHITE, **kw):
    """A label on the picture. Larger than the kit's default: these frames hold few
    objects, and a 28 pt label next to a circuit reads as a footnote."""
    return _kit_txt(s, size, color, **kw)

C_CLK = YELLOW_D      # the clock
C_LOGIC = BLUE_C      # adder, shifter, gates, CL block
C_REG = TEAL_C        # registers and flip-flops
C_DATA = WHITE        # the next number (X)
C_SUM = GREEN_C       # the stored total (S)
C_WINDOW = ORANGE     # setup + hold window
C_CQ = PURPLE_B       # clock-to-q
C_BAD = RED_C         # a wrong value that gets captured; the critical path
C_UNKNOWN = GREY_B    # garbage / unknown


class Timeline:
    """Time to x. `x(t)` is the frame coordinate of time t."""

    def __init__(self, t0, t1, x_left=-5.0, width=10.0):
        self.t0, self.t1, self.x_left, self.width = t0, t1, x_left, width

    def x(self, t):
        return self.x_left + (t - self.t0) / (self.t1 - self.t0) * self.width

    def dx(self, dt):
        return dt / (self.t1 - self.t0) * self.width

    def ruler(self, y, step, unit="", size=28, color=GREY_B):
        """A time axis with a tick and a number every `step`."""
        g = VGroup(Line([self.x(self.t0), y, 0], [self.x(self.t1), y, 0], color=color, stroke_width=2))
        t = self.t0
        while t <= self.t1 + 1e-9:
            g.add(Line([self.x(t), y - 0.07, 0], [self.x(t), y + 0.07, 0], color=color, stroke_width=2))
            g.add(num(f"{t:g}", size=size, color=color).next_to([self.x(t), y, 0], DOWN, buff=0.14))
            t += step
        if unit:
            g.add(txt(unit, color=color).scale(size / 40).next_to(g[0], RIGHT, buff=0.2))
        return g

    def vline(self, t, y_top, y_bot, color=C_CLK, dashed=True, width=2):
        a, b = [self.x(t), y_top, 0], [self.x(t), y_bot, 0]
        return (DashedLine(a, b, color=color, stroke_width=width, dash_length=0.08) if dashed
                else Line(a, b, color=color, stroke_width=width))

    def window(self, t_a, t_b, y_top, y_bot, color=C_WINDOW, opacity=0.25):
        """A shaded stretch of time, e.g. from setup before an edge to hold after it."""
        r = Rectangle(width=self.dx(t_b - t_a), height=y_top - y_bot, stroke_width=0,
                      fill_color=color, fill_opacity=opacity)
        return r.move_to([(self.x(t_a) + self.x(t_b)) / 2, (y_top + y_bot) / 2, 0])


def _corners(points, color, width=4):
    return VMobject(color=color, stroke_width=width).set_points_as_corners([[x, y, 0] for x, y in points])


def bit_trace(tl, changes, y, h=0.5, color=C_DATA, rise=0.0, t_end=None):
    """One wire over time. `changes` is [(time, 0 or 1), ...], the first entry at the start.
    `rise` is how long a transition takes, in time units (0 draws it vertical)."""
    t_end = tl.t1 if t_end is None else t_end
    lvl = lambda v: y + (h if v else 0)
    pts = [(tl.x(changes[0][0]), lvl(changes[0][1]))]
    for (t, v), (_, prev) in zip(changes[1:], changes):
        if v == prev:
            continue
        pts += [(tl.x(t - rise / 2), lvl(prev)), (tl.x(t + rise / 2), lvl(v))]
    last = [v for _, v in changes][-1]
    pts.append((tl.x(t_end), lvl(last)))
    return _corners(pts, color)


def clock_wave(tl, period, y, h=0.5, first_rise=0.0, color=C_CLK, rise=0.0):
    """A square wave, high for the first half of each period, rising at first_rise + k * period."""
    changes, t, v = [(tl.t0, 0)], first_rise, 1
    if first_rise <= tl.t0:
        changes = [(tl.t0, 1)]
        t, v = first_rise + period / 2, 0
        while t <= tl.t0:
            changes = [(tl.t0, v)]
            t, v = t + period / 2, 1 - v
    while t < tl.t1:
        changes.append((t, v))
        t, v = t + period / 2, 1 - v
    return bit_trace(tl, changes, y, h, color, rise)


def rising_edges(tl, period, first_rise=0.0):
    out, t = [], first_rise
    while t < tl.t1 - 1e-9:
        if t >= tl.t0:
            out.append(t)
        t += period
    return out


def bus_cell(tl, t_a, t_b, label, y, h=0.5, color=C_SUM, size=24, pinch=None, unknown=False):
    """One value on a bus: a flat hexagon from t_a to t_b with the value inside."""
    xa, xb = tl.x(t_a), tl.x(t_b)
    p = min(0.12, (xb - xa) / 4) if pinch is None else pinch
    mid = y + h / 2
    shape = Polygon([xa, mid, 0], [xa + p, y + h, 0], [xb - p, y + h, 0], [xb, mid, 0],
                    [xb - p, y, 0], [xa + p, y, 0], color=C_UNKNOWN if unknown else color, stroke_width=3)
    if unknown:
        shape.set_fill(C_UNKNOWN, opacity=0.45)
    cell = VGroup(shape)
    if label not in (None, ""):
        t = num(str(label), size=size, color=color)
        if t.width > (xb - xa) - 2 * p - 0.06:
            t.scale_to_fit_width(max(0.1, (xb - xa) - 2 * p - 0.06))
        cell.add(t.move_to([(xa + xb) / 2, mid, 0]))
    return cell


def bus_band(tl, segs, y, h=0.5, color=C_SUM, size=24):
    """A bus over time. `segs` is [(t_start, t_end, label), ...]; a label of None draws an
    unknown (hatched grey) stretch. Returns a VGroup with one cell per segment."""
    return VGroup(*[bus_cell(tl, a, b, lab, y, h, color, size, unknown=lab is None) for a, b, lab in segs])


def trace_label(text, trace_y, tl, h=0.5, size=40, color=C_DATA):
    """The name of a trace, left of where the timeline starts."""
    return txt(text, size=size, color=color).move_to([tl.x(tl.t0) - 0.7, trace_y + h / 2, 0])


# ------------------------------------------------------------------ circuit symbols
def block(label, w=1.5, h=1.3, color=C_LOGIC, size=44):
    """A box of combinational logic with its name inside."""
    box = RoundedRectangle(width=w, height=h, corner_radius=0.12, color=color, stroke_width=4)
    box.set_fill(color, opacity=0.12)
    return VGroup(box, txt(label, size=size, color=color).move_to(box))


def register_box(label="", w=1.0, h=1.5, color=C_REG, size=40, clocked=True):
    """A register: a box, with the clock input drawn as a small triangle on the bottom edge."""
    box = Rectangle(width=w, height=h, color=color, stroke_width=4).set_fill(color, opacity=0.12)
    g = VGroup(box)
    if clocked:
        b = box.get_bottom()
        g.add(_corners([(b[0] - 0.14, b[1]), (b[0], b[1] + 0.2), (b[0] + 0.14, b[1])], color, width=3))
    if label:
        g.add(txt(label, size=size, color=color).move_to(box.get_center() + UP * 0.12))
    return g


def and_gate(h=0.9, color=C_LOGIC):
    """An AND gate pointing right: a flat back and a round front. `gate.out` and
    `gate.ins(n)` give the pin positions after the gate has been placed."""
    r = h / 2
    body = VMobject(color=color, stroke_width=4)
    body.set_points_as_corners([[0, r, 0], [-r, r, 0], [-r, -r, 0], [0, -r, 0]])
    arc = Arc(radius=r, start_angle=-PI / 2, angle=PI, color=color, stroke_width=4)
    g = VGroup(body, arc)
    g.set_fill(color, opacity=0.12)
    g.h = h
    g.out = lambda: g.get_right()
    g.ins = lambda n=2: [g.get_left() + UP * (g.height * (0.5 - (i + 1) / (n + 1))) for i in range(n)]
    return g


def wire(*points, color=GREY_A, width=3):
    """A wire through the given points (right-angle corners are up to the caller)."""
    return VMobject(color=color, stroke_width=width).set_points_as_corners([np.array(p, dtype=float) for p in points])


def state_circle(name, r=0.55, color=C_REG, size=40):
    c = Circle(radius=r, color=color, stroke_width=4).set_fill(color, opacity=0.12)
    return VGroup(c, txt(name, size=size, color=color).move_to(c))
