"""Episode 2: Inside the Register.

A register is a row of flip-flops; "at the rising edge" is really a window
(setup, hold), and the output answers a moment later (clock-to-q).
Notes: The Register §3; Summary (register example, exercises 1-2).
"""
import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403
from sds_common import *  # noqa: E402,F403
from ep01_runaway_sum import circuit, flash_along  # noqa: E402

# ---- scene `sample`: an input that changes whenever it likes, sampled at four rising edges
S_PERIOD, S_EDGES = 8, [4, 12, 20, 28]
S_D = [(0, 0), (2, 1), (6.5, 0), (8.5, 1), (10.8, 0), (14, 1), (16.5, 0), (24, 1)]


def level(changes, t):
    """The level of a trace at time t."""
    return [v for at, v in changes if at <= t][-1]


S_Q = [level(S_D, e) for e in S_EDGES]
assert S_Q == [1, 0, 0, 1]                      # high, low, low again (nothing visible), high

# ---- scene `edge`: one edge, in made-up units, with clock-to-q longer than hold
E_SETUP, E_HOLD, E_CQ = 2.0, 1.5, 2.5
assert E_HOLD <= E_CQ

# ---- scene `numbers`: the notes' example (summary page, figure 2), in picoseconds
N_SETUP, N_HOLD, N_CQ, N_PERIOD = 2.5, 1.5, 1.5, 13
N_EDGES = [5, 5 + N_PERIOD]
N_IN = [(-4, 0), (-2.5, 1), (-0.5, 0), (0.8, 1), (8, 0), (10.5, 1), (12.5, 0), (13.6, 1), (14.8, 0), (21.5, 1),
        (23, 0)]
N_WIN = [(e - N_SETUP, e + N_HOLD) for e in N_EDGES]
assert all(not (a <= t <= b) for t, _ in N_IN[1:] for a, b in N_WIN)   # every change is outside a window
N_OUT = [level(N_IN, e) for e in N_EDGES]
assert N_OUT == [1, 0]


def lab(text, y, tl, h, color=C_DATA):
    return txt(text, color=color).move_to([tl.x(tl.t0) - 0.85, y + h / 2, 0])


def span(tl, t_a, t_b, y, text, color, above=True, side=None):
    """A double arrow from t_a to t_b with its name."""
    a = DoubleArrow([tl.x(t_a), y, 0], [tl.x(t_b), y, 0], color=color, buff=0, stroke_width=4, tip_length=0.16,
                    max_tip_length_to_length_ratio=0.3)
    t = txt(text, color=color)
    if side is not None:
        t.next_to(a, side, buff=0.2)
    else:
        t.next_to(a, UP if above else DOWN, buff=0.1)
    return VGroup(a, t)


def edge_diagram():
    """One rising edge, close enough to see the clock's slope, with all three times marked."""
    g = SimpleNamespace()
    tl = g.tl = Timeline(-6, 8, x_left=-4.6, width=10.4)
    g.yc, g.yd, g.yq, g.h = 1.5, -0.2, -1.9, 0.9
    g.clk = bit_trace(tl, [(-6, 0), (0, 1)], g.yc, g.h, C_CLK, rise=1.4)
    g.labs = VGroup(lab("clock", g.yc, tl, g.h, C_CLK), lab("d", g.yd, tl, g.h), lab("q", g.yq, tl, g.h, C_REG))
    g.edge = tl.vline(0, g.yc + g.h + 0.35, g.yq - 0.2, color=C_CLK)
    g.d_ok = bit_trace(tl, [(-6, 0), (-3.4, 1), (3.6, 0)], g.yd, g.h, rise=0.5)
    g.win = tl.window(-E_SETUP, E_HOLD, g.yd + g.h + 0.15, g.yd - 0.15)
    g.l_set = tl.vline(-E_SETUP, g.yd + g.h + 0.15, g.yd - 0.15, color=C_WINDOW)
    g.l_hold = tl.vline(E_HOLD, g.yd + g.h + 0.15, g.yd - 0.15, color=C_WINDOW)
    g.setup = span(tl, -E_SETUP, 0, g.yd - 0.4, "setup", C_WINDOW, side=LEFT)
    g.hold = span(tl, 0, E_HOLD, g.yd - 0.4, "hold", C_WINDOW, side=RIGHT)
    g.q = bit_trace(tl, [(-6, 0), (E_CQ, 1)], g.yq, g.h, C_REG, rise=0.5)
    g.l_cq = tl.vline(E_CQ, g.yq + g.h + 0.15, g.yq - 0.2, color=C_CQ)
    g.cq = span(tl, 0, E_CQ, g.yq - 0.4, "clock-to-q", C_CQ, side=RIGHT)
    g.all = VGroup(g.clk, g.labs, g.edge, g.win, g.l_set, g.l_hold, g.d_ok, g.setup, g.hold, g.q, g.l_cq, g.cq)
    return g


class Ep02FlipFlop(NarratedScene):
    SCENES = ["recap", "inside", "sample", "edge", "numbers", "check", "close"]

    def construct(self):
        if self.preview_only([]):
            return
        self.title_card()
        for s in self.SCENES:
            getattr(self, s)()
        self.end_card([
            "A register for n bits is n flip-flops on one clock.",
            "A flip-flop copies d to q at each rising edge, and ignores d otherwise.",
            "Setup time is how long before the edge d must be steady. Hold time is how long after.",
            "The clock to q delay is how long after the edge q shows the new value.",
        ])

    # ------------------------------------------------------------------ 01 recap
    def recap(self):
        self.camera.frame.set(width=11.6).move_to(ORIGIN)
        c = circuit([0, 1.0, 0], 1.0, reg=True, value=4)
        c.load_wire.set_color(C_CLK)
        c.val.set_color(C_REG)
        clk = txt("clock", color=C_CLK).next_to(c.load_wire, DOWN, buff=0.12)
        self.say("Last time a register saved our running sum. It took in a new value at each rising edge of the "
                 "clock and held it still for the rest of the period.\nToday we open the box.",
                 FadeIn(c.all), FadeIn(clk))
        self.cue("took in a new value", flash_along(c.load_wire, run_time=0.8),
                 Transform(c.val, num(8, 44, C_REG).move_to(c.val)))
        self.cue("held it still", Indicate(c.box, color=C_REG, scale_factor=1.15))
        self.zoom_to(c.box, width=5.0)
        self.hold(0.4)
        self.clear_stage()
        self.camera.frame.set(width=FRAME_W).move_to(ORIGIN)

    # ------------------------------------------------------------------ 02 inside
    def inside(self):
        y0 = 0.2
        xs = [-3.0, -1.0, 1.0, 3.0]
        outer = Rectangle(width=8.6, height=2.6, color=C_REG, stroke_width=4).move_to([0, y0, 0])
        outer.set_fill(C_REG, opacity=0.12)
        title = txt("register", color=C_REG).move_to(outer).shift(UP * 0.75)
        d_bus = Arrow([0, y0 + 2.9, 0], [0, y0 + 1.3, 0], color=GREY_A, buff=0, stroke_width=8, tip_length=0.25)
        q_bus = Arrow([0, y0 - 1.3, 0], [0, y0 - 2.9, 0], color=GREY_A, buff=0, stroke_width=8, tip_length=0.25)
        D = txt("D", color=C_REG).next_to(d_bus, RIGHT, buff=0.25)
        Q = txt("Q", color=C_REG).next_to(q_bus, RIGHT, buff=0.25)
        clk_line = Line([-6.2, y0, 0], [xs[-1], y0, 0], color=C_CLK, stroke_width=4)
        clk_lab = txt("clock", color=C_CLK).next_to(clk_line, UP, buff=0.12).set_x(-5.5)
        ffs, d_w, q_w = VGroup(), VGroup(), VGroup()
        for x in xs:
            b = Square(1.2, color=C_REG, stroke_width=4).set_fill("#12262a", opacity=1).move_to([x, y0, 0])
            tri = VMobject(color=C_CLK, stroke_width=3).set_points_as_corners(
                [b.get_left() + UP * 0.13, b.get_left() + RIGHT * 0.18, b.get_left() + DOWN * 0.13])
            ffs.add(VGroup(b, tri))
            d_w.add(Arrow([x, y0 + 2.9, 0], [x, y0 + 0.6, 0], color=GREY_A, buff=0, stroke_width=3, tip_length=0.16))
            q_w.add(Arrow([x, y0 - 0.6, 0], [x, y0 - 2.9, 0], color=GREY_A, buff=0, stroke_width=3, tip_length=0.16))
        self.say("Our register stored a whole number, so it has several wires going in and several coming out.\n"
                 "Inside there is no clever machinery. There is one small circuit for each bit, side by side, and "
                 "all of them listen to the same clock.",
                 FadeIn(outer), FadeIn(title))
        self.cue("several wires going in", GrowArrow(d_bus), GrowArrow(q_bus), Create(clk_line), FadeIn(clk_lab))
        self.cue("Inside there is no clever", FadeOut(title), outer.animate.set_fill(opacity=0).set_stroke(opacity=0.35))
        self.cue("one small circuit for each bit",
                 LaggedStart(*[FadeIn(f, scale=0.8) for f in ffs], lag_ratio=0.25, run_time=1.6),
                 ReplacementTransform(d_bus, d_w), ReplacementTransform(q_bus, q_w))
        self.cue("the same clock", flash_along(clk_line, run_time=1.4))
        self.hold()

        bits = [0, 1, 1, 0]
        vals = VGroup(*[num(b, 48, C_REG).move_to(f[0]) for b, f in zip(bits, ffs)])
        name = txt("flip-flop", color=YELLOW).next_to(ffs[3], RIGHT, buff=0.35)
        ten = txt("about 10 transistors", color=GREY_A).scale(0.8).next_to(name, DOWN, buff=0.2, aligned_edge=LEFT)
        d_small = MathTex("d", font_size=48, color=C_REG).next_to(d_w[0], LEFT, buff=0.15)
        q_small = MathTex("q", font_size=48, color=C_REG).next_to(q_w[0], LEFT, buff=0.15)
        D.next_to(d_w[3], RIGHT, buff=0.3).shift(UP * 0.5)
        Q.next_to(q_w[3], RIGHT, buff=0.3).shift(DOWN * 0.5)
        self.say("Each of these small circuits is a register for a single bit. It is called a flip-flop, because "
                 "all it ever does is flip to one or flop back to zero, and it takes about ten transistors to "
                 "build.\nBy convention the input of a register is capital D and its output is capital Q. For a "
                 "single flip-flop we use the small letters.",
                 FadeIn(vals))
        self.cue("called a flip-flop", FadeIn(name, shift=LEFT * 0.2))
        self.cue("flip to one", Transform(vals[0], num(1, 48, C_REG).move_to(vals[0])), run_time=0.5)
        self.cue("flop back to zero", Transform(vals[0], num(0, 48, C_REG).move_to(vals[0])), run_time=0.5)
        self.cue("about ten transistors", FadeIn(ten, shift=UP * 0.15))
        self.cue("capital D", FadeOut(name), FadeIn(D))
        self.cue("capital Q", FadeIn(Q))
        self.cue("the small letters", FadeIn(d_small), FadeIn(q_small), Indicate(ffs[0], color=YELLOW))
        self.hold()

        self.say("So to understand a register of any width, we only have to understand one flip-flop. Let's put a "
                 "probe on its three wires and watch.",
                 *[FadeOut(m) for m in (ffs[1:], d_w[1:], q_w[1:], vals, outer, D, Q, ten)],
                 clk_line.animate.put_start_and_end_on(clk_line.get_start(), [xs[0] - 0.6, y0, 0]))
        self.cue("three wires", Indicate(d_w[0], color=YELLOW), Indicate(q_w[0], color=YELLOW),
                 flash_along(clk_line, run_time=1.2))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 03 sample
    def sample(self):
        tl = Timeline(0, 34, x_left=-4.4, width=10.8)
        yc, yd, yq, h = 1.7, 0.0, -1.8, 0.9
        clk = clock_wave(tl, S_PERIOD, yc, h, first_rise=S_EDGES[0], rise=0.5)
        d = bit_trace(tl, S_D, yd, h, rise=0.4)
        labs = VGroup(lab("clock", yc, tl, h, C_CLK), lab("d", yd, tl, h), lab("q", yq, tl, h, C_REG))
        lines = [tl.vline(e, yc + h + 0.2, yq - 0.15) for e in S_EDGES]
        dots = [Dot([tl.x(e), yd + (h if v else 0), 0], radius=0.11, color=YELLOW) for e, v in zip(S_EDGES, S_Q)]
        unknown = bus_cell(tl, 0, S_EDGES[0], None, yq, h, unknown=True)
        # q, one piece per period: each starts at its edge and changes a moment after it
        q_parts, prev = [], None
        ends = S_EDGES[1:] + [34]
        for e, end, v in zip(S_EDGES, ends, S_Q):
            start = v if prev is None else prev
            q_parts.append(bit_trace(tl, [(e, start), (e + 0.45, v)], yq, h, C_REG, rise=0.4, t_end=end))
            prev = v

        self.say("Here is the clock, and here is an input that changes whenever it likes. Before the output "
                 "appears, try to predict it.\n"
                 "All you need to know is that the flip-flop only looks at its input at each rising edge.",
                 FadeIn(labs[0]), Create(clk, run_time=2.0, rate_func=linear))
        self.cue("here is an input", FadeIn(labs[1]), Create(d, run_time=2.4, rate_func=linear))
        self.cue("try to predict", FadeIn(labs[2]), FadeIn(unknown))
        self.cue("at each rising edge", LaggedStart(*[Create(l) for l in lines], lag_ratio=0.4, run_time=2.0))
        self.hold(1.0)

        self.say("At the first edge the input is high, so the output goes high. During this period the input "
                 "drops and comes back up, and the output takes no notice at all.\n"
                 "At the second edge the input is low, so the output goes low.",
                 FadeIn(dots[0], scale=2), Indicate(lines[0], color=YELLOW, scale_factor=1.0))
        self.cue("the output goes high", Create(q_parts[0], run_time=1.6, rate_func=linear))
        dip = SurroundingRectangle(VGroup(Dot([tl.x(6), yd, 0]), Dot([tl.x(9), yd + h, 0])), color=GREY_B, buff=0.15)
        self.cue("drops and comes back up", Create(dip))
        self.cue("takes no notice", Indicate(q_parts[0], color=C_REG, scale_factor=1.0), FadeOut(dip))
        self.cue("At the second edge", FadeIn(dots[1], scale=2), Indicate(lines[1], color=YELLOW, scale_factor=1.0))
        self.cue("the output goes low", Create(q_parts[1], run_time=1.6, rate_func=linear))
        self.hold()

        self.say("At the third edge the input is low again. The flip-flop does take that value in, but it is the "
                 "value the output already has, so nothing visible happens.\n"
                 "At the fourth the input is high, and the output goes high again.",
                 FadeIn(dots[2], scale=2), Indicate(lines[2], color=YELLOW, scale_factor=1.0))
        self.cue("nothing visible happens", Create(q_parts[2], run_time=1.6, rate_func=linear))
        self.cue("At the fourth", FadeIn(dots[3], scale=2), Indicate(lines[3], color=YELLOW, scale_factor=1.0))
        self.cue("goes high again", Create(q_parts[3], run_time=1.2, rate_func=linear))
        self.hold()

        name = txt("positive edge-triggered D flip-flop", color=YELLOW).move_to([0.6, 3.35, 0])
        self.say("So the rule is short. At every rising edge q becomes whatever d is at that moment, and between "
                 "edges q does not move.\n"
                 "This kind is called a positive edge triggered D flip-flop. There is also a kind that acts on "
                 "the falling edge, but we will only use this one.")
        self.cue("q becomes whatever d is", LaggedStart(*[Flash(dt, color=YELLOW, flash_radius=0.35) for dt in dots],
                                                        lag_ratio=0.35, run_time=2.2))
        self.cue("called a positive edge", FadeIn(name, shift=DOWN * 0.15))
        falls = VGroup(*[tl.vline(e + S_PERIOD / 2, yc + h + 0.1, yc - 0.1, color=GREY_B) for e in S_EDGES[:-1]])
        self.cue("the falling edge", FadeIn(falls))
        self.cue("only use this one", FadeOut(falls))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 04 edge
    def edge(self):
        g = edge_diagram()
        tl = g.tl
        small_tl = Timeline(0, 34, x_left=-2.0, width=4.6)
        small = clock_wave(small_tl, S_PERIOD, 3.25, 0.4, first_rise=S_EDGES[0], rise=0.5)
        small.set_stroke(width=3)
        box = Rectangle(width=0.6, height=0.7, color=YELLOW, stroke_width=3).move_to([small_tl.x(12), 3.45, 0])
        guides = VGroup(
            DashedLine(box.get_corner(DL), [tl.x(-6), g.yc + g.h + 0.1, 0], color=GREY_C, stroke_width=2),
            DashedLine(box.get_corner(DR), [tl.x(8), g.yc + g.h + 0.1, 0], color=GREY_C, stroke_width=2))
        self.say("That rule has a soft spot, and it is the phrase at that moment. Let's zoom in on one rising "
                 "edge, far enough to see that the clock itself takes a little while to rise.",
                 Create(small, run_time=1.5))
        self.cue("zoom in on one rising edge", Create(box))
        self.cue("far enough to see", Create(guides), FadeIn(g.labs[0]), Create(g.clk, run_time=2.0))
        self.hold()

        d_bad = bit_trace(tl, [(-6, 0), (0, 1)], g.yd, g.h, rise=0.5)
        q_unknown = bus_cell(tl, 0.8, 8, None, g.yq, g.h, unknown=True)
        q_before = bit_trace(tl, [(-6, 0)], g.yq, g.h, C_REG, t_end=0.8)
        q_mark = txt("?", size=56, color=YELLOW).move_to(q_unknown)
        self.say("Suppose the input changes right here, in the middle of the rise. Is the value at the edge a zero "
                 "or a one?\n"
                 "The transistors inside are partway through taking the old value in, and now they are handed a "
                 "different one. What the output ends up as is anyone's guess.",
                 FadeOut(small), FadeOut(box), FadeOut(guides), FadeIn(g.labs[1]), Create(d_bad, run_time=2.0),
                 Create(g.edge))
        self.cue("a zero or a one", Flash([tl.x(0), g.yd + g.h / 2, 0], color=C_BAD, flash_radius=0.6))
        self.cue("What the output ends up as", FadeIn(g.labs[2]), Create(q_before), FadeIn(q_unknown))
        self.cue("anyone's guess", FadeIn(q_mark, scale=1.5))
        self.hold()

        d_early = bit_trace(tl, [(-6, 0), (-3.4, 1)], g.yd, g.h, rise=0.5)
        self.say("So the flip-flop comes with a condition. Its input has to be steady already a short time before "
                 "the edge, so that the value has time to get in.\nThat time is called the setup time.",
                 FadeOut(q_mark), FadeOut(q_unknown), FadeOut(q_before))
        self.cue("steady already", Transform(d_bad, d_early, run_time=1.4))
        self.cue("a short time before the edge", Create(g.l_set), GrowFromCenter(g.setup[0]))
        self.cue("called the setup time", FadeIn(g.setup[1], shift=RIGHT * 0.15))
        self.hold()

        outside = VGroup(txt("free", color=GREY_B).scale(0.85).move_to([tl.x(-4.9), g.yd - 0.55, 0]),
                         txt("free", color=GREY_B).scale(0.85).move_to([tl.x(6.6), g.yd - 0.55, 0]))
        self.say("And the input has to stay steady for a short time after the edge, until the flip-flop has safely "
                 "let go of it. That time is called the hold time.\n"
                 "Together they make a window around every rising edge. Inside the window the input must not "
                 "change. Outside it, the input can do whatever it wants.",
                 ReplacementTransform(d_bad, g.d_ok, run_time=1.4))
        self.cue("a short time after the edge", Create(g.l_hold), GrowFromCenter(g.hold[0]))
        self.cue("called the hold time", FadeIn(g.hold[1], shift=LEFT * 0.15))
        self.cue("a window around", FadeIn(g.win))
        self.cue("must not change", Indicate(g.win, color=C_WINDOW, scale_factor=1.08))
        self.cue("Outside it", FadeIn(outside))
        self.hold()

        self.say("There is one more delay, on the output side. Even when the input behaves, the new value does not "
                 "show up at the output on the edge itself.\n"
                 "It appears a little later, and that delay is called the clock to q delay.",
                 FadeOut(outside), FadeIn(g.labs[2]), Create(g.q, run_time=2.4, rate_func=linear))
        self.cue("It appears a little later", Create(g.l_cq), GrowFromCenter(g.cq[0]))
        self.cue("called the clock to q delay", FadeIn(g.cq[1], shift=LEFT * 0.15))
        self.hold()

        self.say("Three numbers, then, describe a flip-flop. Setup and hold are demands it makes on its input, and "
                 "clock to q is how long it makes its output wait.")
        self.cue("Setup and hold", Indicate(g.setup[1], color=C_WINDOW), Indicate(g.hold[1], color=C_WINDOW))
        self.cue("clock to q is how long", Indicate(g.cq[1], color=C_CQ))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 05 numbers
    def numbers(self):
        tl = Timeline(-4, 27, x_left=-4.4, width=10.8)
        yc, yd, yq, h = 1.3, -0.4, -2.1, 0.8
        clk = bit_trace(tl, [(-4, 0), (N_EDGES[0], 1), (N_EDGES[0] + 6.5, 0), (N_EDGES[1], 1), (N_EDGES[1] + 6.5, 0)],
                        yc, h, C_CLK, rise=0.5)
        labs = VGroup(lab("clock", yc, tl, h, C_CLK), lab("input", yd, tl, h), lab("output", yq, tl, h, C_REG))
        labs.shift(LEFT * 0.25)
        facts = VGroup(
            VGroup(txt("setup", color=C_WINDOW), num("2.5", 44, C_WINDOW), txt("ps", color=C_WINDOW)),
            VGroup(txt("hold", color=C_WINDOW), num("1.5", 44, C_WINDOW), txt("ps", color=C_WINDOW)),
            VGroup(txt("clock-to-q", color=C_CQ), num("1.5", 44, C_CQ), txt("ps", color=C_CQ)))
        for f in facts:
            f.arrange(RIGHT, buff=0.15)
        facts.arrange(RIGHT, buff=0.8).move_to([0.3, 3.4, 0])
        per = span(tl, N_EDGES[0], N_EDGES[1], yc + h + 0.3, "13 ps", C_CLK, side=None)
        self.say("Let's put numbers on them. Take a flip-flop with a setup time of two and a half picoseconds, a "
                 "hold time of one and a half, and a clock to q delay of one and a half.\n"
                 "The clock period is thirteen picoseconds.",
                 FadeIn(labs[0]), Create(clk, run_time=2.0, rate_func=linear))
        self.cue("a setup time", FadeIn(facts[0], shift=DOWN * 0.15))
        self.cue("a hold time", FadeIn(facts[1], shift=DOWN * 0.15))
        self.cue("a clock to q delay", FadeIn(facts[2], shift=DOWN * 0.15))
        self.cue("thirteen picoseconds", GrowFromCenter(per[0]), FadeIn(per[1]))
        self.hold()

        wins = VGroup(*[tl.window(a, b, yc + h + 0.1, yd - 0.15) for a, b in N_WIN])
        edges = VGroup(*[tl.vline(e, yc + h + 0.1, yq - 0.15) for e in N_EDGES])
        w_lab = VGroup(num("2.5", 30, C_WINDOW).move_to([tl.x(N_EDGES[0] - N_SETUP / 2), yd - 0.4, 0]),
                       num("1.5", 30, C_WINDOW).move_to([tl.x(N_EDGES[0] + N_HOLD / 2) + 0.12, yd - 0.4, 0]))
        d = bit_trace(tl, N_IN, yd, h, rise=0.3)
        ticks = VGroup(*[Dot([tl.x(t), yd + h / 2, 0], radius=0.07, color=GREY_A) for t, _ in N_IN[1:]])
        self.say("Draw the window at each edge. It opens two and a half picoseconds before and closes one and a "
                 "half after.\n"
                 "This input changes many times, but every change falls outside a window, so each edge samples a "
                 "clean value.",
                 FadeOut(per), Create(edges), FadeIn(wins))
        self.cue("two and a half picoseconds before", FadeIn(w_lab[0]))
        self.cue("one and a half after", FadeIn(w_lab[1]))
        self.cue("This input changes", FadeIn(labs[1]), Create(d, run_time=2.6, rate_func=linear))
        self.cue("every change falls outside", LaggedStart(*[FadeIn(t, scale=2) for t in ticks], lag_ratio=0.15,
                                                           run_time=1.8))
        self.cue("samples a clean value", FadeOut(ticks), Indicate(wins, color=C_WINDOW, scale_factor=1.03))
        self.hold()

        t1, t2 = N_EDGES[0] + N_CQ, N_EDGES[1] + N_CQ
        unknown = bus_cell(tl, -4, t1, None, yq, h, unknown=True, pinch=0.0)
        q1 = bit_trace(tl, [(t1, 1)], yq, h, C_REG, t_end=t2)
        q2 = bit_trace(tl, [(t2 - 0.01, 1), (t2 + 0.15, 0)], yq, h, C_REG, rise=0.3)
        cq = span(tl, N_EDGES[0], t1, yq + h + 0.25, "1.5", C_CQ, side=RIGHT)
        self.say("Now the output. Before the first edge we have no idea what the flip-flop holds, so we shade it as "
                 "unknown.\n"
                 "One and a half picoseconds after that edge, the output shows the value the input had, which was "
                 "a one. After the next edge it shows a zero.",
                 FadeIn(labs[2]), FadeOut(w_lab))
        self.cue("shade it as unknown", FadeIn(unknown))
        self.cue("One and a half picoseconds after", GrowFromCenter(cq[0]), FadeIn(cq[1]))
        self.cue("the output shows the value", Create(q1, run_time=1.6, rate_func=linear))
        self.cue("After the next edge", FadeOut(cq), Create(q2, run_time=1.2, rate_func=linear))
        self.hold()

        self.say("Here the hold time and the clock to q delay happen to be equal. Nothing forces that, because "
                 "one describes the input and the other describes the output.\n"
                 "In practice, though, flip-flops are built so that the hold time is the smaller of the two, or "
                 "at most equal.",
                 Indicate(facts[1], color=C_WINDOW), Indicate(facts[2], color=C_CQ))
        self.cue("one describes the input", Indicate(labs[1], color=C_WINDOW))
        self.cue("the other describes the output", Indicate(labs[2], color=C_CQ))
        rel = MathTex(r"\text{hold} \le \text{clock-to-q}", font_size=44, color=YELLOW)
        rel.move_to([tl.x(22.5), yd + h / 2 + 1.75, 0]).set_y(yc + h + 0.55)
        self.cue("the hold time is the smaller", FadeIn(rel, shift=UP * 0.15))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 06 check
    def check(self):
        g = edge_diagram()
        g.all.shift(DOWN * 0.45)
        s1 = txt("``clock-to-q is the time from the rising edge to the hold time''", color=WHITE)
        s2 = txt("``q only updates at a rising edge, even if d changes in between''", color=WHITE)
        for s in (s1, s2):
            if s.width > 12.4:
                s.scale_to_fit_width(12.4)
            s.move_to([0, 3.35, 0])
        no = txt("false", color=C_BAD).next_to(s1, DOWN, buff=0.18)
        yes = txt("true", color=C_SUM).next_to(s2, DOWN, buff=0.18)
        self.say("Here are two statements to test yourself on. The first says that the clock to q delay is the "
                 "time from the rising edge to the hold time.\n"
                 "That is false. Clock to q runs from the rising edge to the moment the output shows the new "
                 "value, and the hold time is about the input.",
                 FadeIn(g.all))
        self.cue("The first says", FadeIn(s1, shift=DOWN * 0.15))
        self.cue("That is false", FadeIn(no, scale=1.3))
        self.cue("Clock to q runs", Indicate(g.cq, color=C_CQ), Indicate(g.l_cq, color=C_CQ, scale_factor=1.0))
        self.cue("the hold time is about the input", Indicate(g.hold, color=C_WINDOW))
        self.hold()

        self.say("The second says that a flip-flop only updates its output at a rising edge, even if its input "
                 "changes in between.\nThat one is true, and it is the whole point of the device.",
                 FadeOut(s1), FadeOut(no), FadeIn(s2, shift=DOWN * 0.15))
        self.cue("even if its input changes", Indicate(g.d_ok, color=YELLOW, scale_factor=1.0))
        self.cue("That one is true", FadeIn(yes, scale=1.3), Indicate(g.q, color=C_REG, scale_factor=1.0))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 07 close
    def close(self):
        self.camera.frame.set(width=11.6).move_to(ORIGIN)
        c = circuit([0, 1.0, 0], 1.0, reg=True, value="")
        c.load_wire.set_color(C_CLK)
        clk = txt("clock", color=C_CLK).next_to(c.load_wire, DOWN, buff=0.12)
        d_pin = c.fb_d[1].get_center()
        win = Rectangle(width=0.5, height=0.8, stroke_width=0, fill_color=C_WINDOW, fill_opacity=0.45)
        win.move_to(d_pin + RIGHT * 0.3)
        ask = txt("how short can the period be?", color=YELLOW).move_to([0, 2.6, 0])
        self.say("So a register is a row of flip-flops. Each one samples its input in a small window around the "
                 "rising edge and answers a moment later.\n"
                 "Now put it back in our circuit, where the adder's result has to arrive before that window "
                 "opens. How short can we make the clock period before the sum stops being right?",
                 FadeIn(c.box, scale=0.9))
        self.cue("Now put it back", FadeIn(VGroup(*[m for m in c.all if m is not c.box])), FadeIn(clk))
        self.cue("the adder's result", flash_along(VGroup(c.out_wire[0], c.fb_d[0]), color=C_SUM, run_time=1.6))
        self.cue("before that window opens", FadeIn(win, scale=1.4))
        self.cue("How short", FadeIn(ask, shift=DOWN * 0.15), flash_along(c.load_wire, run_time=0.8))
        self.hold(0.8)
        self.clear_stage()
        self.camera.frame.set(width=FRAME_W).move_to(ORIGIN)
