"""Episode 1: The Sum That Ran Away.

An adder with a feedback wire is asked to add up a list, and the sum runs away.
What is missing is a register (something that holds) and a clock (something
that says when). Notes: Signals/Waveforms/Clock §2-4, Register §1-2, Timing §2.1-2.3.
"""
import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403
from sds_common import *  # noqa: E402,F403

XS = [3, 1, 4, 2]       # the list
DELAY = 2               # adder propagation delay, ns
PERIOD = 8              # one number every 8 ns


def runaway(n_steps):
    """Adder output with the feedback wire alone: out(t) = out(t - DELAY) + X(t - DELAY).
    Returns [(t_start, t_end, value)]."""
    x_at = lambda t: XS[min(int(t // PERIOD), len(XS) - 1)]
    out, vals = [(0, DELAY, 0)], {0: 0}
    for k in range(1, n_steps + 1):
        t = k * DELAY
        vals[t] = vals[t - DELAY] + x_at(t - DELAY)
        out.append((t, t + DELAY, vals[t]))
    return out


RUN = runaway(7)
assert [v for _, _, v in RUN] == [0, 3, 6, 9, 12, 13, 14, 15]
assert RUN[4][0] == PERIOD and RUN[4][2] == 12          # twelve when the second number arrives

TOTALS = [sum(XS[:k]) for k in range(len(XS) + 1)]       # what the register holds: 0, 3, 4, 8, 10
assert TOTALS == [0, 3, 4, 8, 10] and sum(XS) == 10


def tip(at, direction, color=GREY_A, size=0.16):
    """A small arrowhead on a wire, pointing along `direction`."""
    t = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=0).scale(size / 2)
    t.rotate(angle_of_vector(direction) - PI / 2)
    return t.move_to(np.array(at, dtype=float) - np.array(direction, dtype=float) * size / 3)


def circuit(center=ORIGIN, s=1.0, reg=False, value=None):
    """The accumulator. Without `reg`: adder and a bare feedback wire. With it: a
    register on the bottom run of the feedback (D on its right, Q on its left)."""
    c = SimpleNamespace()
    c.adder = block("+", w=1.5, h=1.6)
    c.x_wire = VGroup(wire([-3.2, 0.4, 0], [-0.75, 0.4, 0]), tip([-0.75, 0.4, 0], RIGHT))
    c.out_wire = VGroup(wire([0.75, 0, 0], [3.2, 0, 0]), tip([3.2, 0, 0], RIGHT))
    c.x_lab = txt("X", color=C_DATA).move_to([-3.5, 0.4, 0])
    c.s_lab = txt("S", color=C_SUM).move_to([3.5, 0, 0])
    c.tap = Dot([2, 0, 0], radius=0.07, color=GREY_A)
    parts = [c.adder, c.x_wire, c.out_wire, c.x_lab, c.s_lab, c.tap]
    if not reg:
        c.fb = VGroup(wire([2, 0, 0], [2, -2.0, 0], [-2, -2.0, 0], [-2, -0.4, 0], [-0.75, -0.4, 0]),
                      tip([-0.75, -0.4, 0], RIGHT))
        parts.append(c.fb)
    else:
        c.fb_d = VGroup(wire([2, 0, 0], [2, -2.0, 0], [0.55, -2.0, 0]), tip([0.55, -2.0, 0], LEFT))
        c.fb_q = VGroup(wire([-0.55, -2.0, 0], [-2, -2.0, 0], [-2, -0.4, 0], [-0.75, -0.4, 0]),
                        tip([-0.75, -0.4, 0], RIGHT))
        c.box = register_box("", w=1.1, h=1.0, clocked=False)
        c.box.move_to([0, -2.0, 0])
        c.val = (blank(44) if value in (None, "") else num(value, size=44, color=C_SUM)).move_to(c.box)
        c.load_wire = wire([0, -2.5, 0], [0, -3.1, 0])
        parts += [c.fb_d, c.fb_q, c.box, c.val, c.load_wire]
    c.all = VGroup(*parts)
    c.all.scale(s, about_point=ORIGIN).shift(center)
    c.s = s
    return c


def set_num(old, value, size=44, color=C_SUM):
    """Animation: the number `old` becomes `value`, in place."""
    return Transform(old, num(value, size=size, color=color).move_to(old))


def blank(size=34):
    """An invisible number, to be given a value later with set_num()."""
    return num(0, size=size).set_opacity(0)


def flash_along(mob, color=YELLOW, run_time=1.0):
    return ShowPassingFlash(mob.copy().set_color(color).set_stroke(width=7), time_width=0.6, run_time=run_time)


class Ep01RunawaySum(NarratedScene):
    SCENES = ["hook", "waveform", "delay", "runaway", "hold_it", "clock", "works", "close"]

    def construct(self):
        if self.preview_only(["hold_it", "clock"]):
            return
        self.title_card()
        for s in self.SCENES:
            getattr(self, s)()
        self.end_card([
            "A waveform plots a wire's voltage over time. Low is zero, high is one.",
            "Every circuit takes time to answer. That is its propagation delay.",
            "An adder wired back to itself keeps adding, because nothing tells it to wait.",
            "A register holds a value, and takes a new one only at a rising edge of the clock.",
        ])

    # ------------------------------------------------------------------ 01 hook
    def hook(self):
        self.camera.frame.set(width=10.6).move_to([0, -0.35, 0])
        c = circuit(ORIGIN, 1.0)
        a_in = wire([-3.2, -0.4, 0], [-0.75, -0.4, 0])
        a_tip = tip([-0.75, -0.4, 0], RIGHT)
        ex = VGroup(num(2, 48).next_to(c.x_wire, UP, buff=0.12).set_x(-2.4),
                    num(5, 48).next_to(a_in, DOWN, buff=0.12).set_x(-2.4),
                    num(7, 48, C_SUM).next_to(c.out_wire, UP, buff=0.12).set_x(2.6))
        self.say("Here is an adder. Put two numbers on its inputs, and their sum comes out on the other side.\n"
                 "It has no memory at all, so its output depends only on what the inputs are right now.",
                 FadeIn(c.adder, scale=0.9), Create(c.x_wire), Create(a_in), FadeIn(a_tip), Create(c.out_wire))
        self.cue("Put two numbers", FadeIn(ex[0], shift=RIGHT * 0.3), FadeIn(ex[1], shift=RIGHT * 0.3))
        self.cue("their sum comes out", flash_along(c.adder[0], run_time=0.8), FadeIn(ex[2], shift=RIGHT * 0.3))
        new = VGroup(num(6, 48).move_to(ex[0]), num(1, 48).move_to(ex[1]), num(7, 48, C_SUM).move_to(ex[2]))
        self.cue("no memory at all", Transform(ex[0], new[0]), Transform(ex[1], new[1]), Indicate(ex[2], color=C_SUM))
        self.hold()

        queue = VGroup(*[num(v, 48) for v in XS]).arrange(RIGHT, buff=0.55)
        queue.next_to(c.x_wire, UP, buff=0.25).set_x(-3.0)
        total = VGroup(txt("total", color=C_SUM), num("= 10", 48, C_SUM)).arrange(RIGHT, buff=0.2)
        total.next_to(c.out_wire, UP, buff=0.3).set_x(2.6)
        self.say("Let's give it a job that sounds easy. A list of numbers arrives one at a time, three, then one, "
                 "then four, then two, and we want their total.\n"
                 "The total is ten, but the adder only ever sees two numbers at once.",
                 FadeOut(ex))
        self.cue("three, then one", LaggedStart(*[FadeIn(q, shift=DOWN * 0.3) for q in queue], lag_ratio=0.6,
                                                run_time=2.4))
        self.cue("The total is ten", FadeIn(total, shift=UP * 0.2))
        self.cue("only ever sees two", Indicate(c.x_wire, color=YELLOW), Indicate(a_in, color=YELLOW))
        self.hold()

        self.say("So one input has to be the next number from the list, and the other has to be the total so far.\n"
                 "And the total so far is exactly what the adder produces. The natural thing to do is to run a "
                 "wire from the output straight back to the second input.",
                 FadeIn(c.x_lab), queue.animate.set_opacity(0.45))
        s_in = txt("total so far", color=C_SUM).next_to(a_in, DOWN, buff=0.15).set_x(-2.9)
        self.cue("the other has to be", FadeIn(s_in, shift=RIGHT * 0.2))
        self.cue("exactly what the adder produces", FadeOut(total), FadeIn(c.s_lab), Indicate(c.out_wire, color=C_SUM))
        self.cue("run a wire", FadeOut(a_in), FadeOut(a_tip), FadeOut(s_in), FadeIn(c.tap),
                 Create(c.fb, run_time=2.2))
        self.hold()

        axis = Arrow([-4.2, -2.45, 0], [3.6, -2.45, 0], color=GREY_B, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.03)
        axis_lab = txt("time", color=GREY_B).next_to(axis, RIGHT, buff=0.15)
        self.say("On paper this looks finished. To find out whether it works, we have to watch what the wires do "
                 "over time, and for that we need a way to draw time.",
                 FadeOut(queue), Circumscribe(c.all, color=GREY_B, run_time=2))
        self.cue("a way to draw time", GrowArrow(axis), FadeIn(axis_lab))
        self.hold()
        self.clear_stage()
        self.camera.frame.set(width=FRAME_W).move_to(ORIGIN)

    # ------------------------------------------------------------------ 02 waveform
    def waveform(self):
        tl = Timeline(0, 14, x_left=-4.2, width=9.0)
        y0, h = -1.6, 2.2
        w = Line([-4.6, 2.5, 0], [5.0, 2.5, 0], color=GREY_A, stroke_width=5)
        w_lab = txt("a wire", color=GREY_B).next_to(w, UP, buff=0.15).set_x(-3.6)
        probe = VGroup(Dot([0, 2.5, 0], radius=0.09, color=YELLOW),
                       Line([0, 2.5, 0], [0, 1.5, 0], color=YELLOW, stroke_width=3))
        v_ax = Arrow([tl.x(0), y0 - 0.3, 0], [tl.x(0), y0 + h + 0.7, 0], color=GREY_B, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.05)
        t_ax = Arrow([tl.x(0), y0 - 0.3, 0], [tl.x(14) + 0.5, y0 - 0.3, 0], color=GREY_B, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.025)
        v_lab = txt("voltage", color=GREY_B).next_to(v_ax, LEFT, buff=0.15).set_y(y0 + h + 0.4)
        t_lab = txt("time", color=GREY_B).next_to(t_ax, RIGHT, buff=0.15)
        changes = [(0, 0), (4.5, 1), (9.5, 0)]
        trace = bit_trace(tl, changes, y0, h, rise=0.25)
        self.say("Take a single wire and touch a probe to it. All the probe can measure is a voltage, so we plot "
                 "that voltage against time.\nA picture like this is called a waveform.",
                 Create(w), FadeIn(w_lab))
        self.cue("touch a probe", FadeIn(probe, shift=UP * 0.4))
        self.cue("we plot", GrowArrow(v_ax), GrowArrow(t_ax), FadeIn(v_lab), FadeIn(t_lab))
        self.play(Create(trace, run_time=3.2, rate_func=linear))
        name = txt("waveform", color=YELLOW).next_to(trace, UP, buff=0.25).set_x(tl.x(11.5))
        self.cue("called a waveform", FadeIn(name, shift=UP * 0.2))
        self.hold()

        lo = DashedLine([tl.x(0), y0, 0], [tl.x(14), y0, 0], color=GREY_C, stroke_width=2)
        hi = DashedLine([tl.x(0), y0 + h, 0], [tl.x(14), y0 + h, 0], color=GREY_C, stroke_width=2)
        lo_lab = txt("low = 0", color=GREY_A).next_to(lo, RIGHT, buff=0.2)
        hi_lab = txt("high = 1", color=GREY_A).next_to(hi, RIGHT, buff=0.2)
        bits = VGroup(num(0, 56).move_to([tl.x(2.2), y0 + 0.45, 0]),
                      num(1, 56).move_to([tl.x(7), y0 + h - 0.45, 0]),
                      num(0, 56).move_to([tl.x(11.8), y0 + 0.45, 0]))
        self.say("Most of the time the voltage sits at one of two levels. By convention the low level means a zero "
                 "and the high level means a one.\nSo this wire said zero, then one, then zero again.",
                 FadeOut(name), FadeOut(t_lab), Create(lo), Create(hi))
        self.cue("the low level means", FadeIn(lo_lab))
        self.cue("the high level means", FadeIn(hi_lab))
        self.cue("zero, then one", LaggedStart(*[FadeIn(b, scale=1.4) for b in bits], lag_ratio=0.7, run_time=2.2))
        self.hold()

        # the same wire, drawn honestly: levels a little off the extremes
        lv = lambda f: y0 + f * h
        rough_pts = [(0, 0.07), (1.5, 0.04), (3, 0.1), (4.3, 0.08), (4.7, 0.86), (6, 0.93), (7.5, 0.88), (9.3, 0.91),
                     (9.7, 0.12), (11, 0.06), (12.5, 0.11), (14, 0.07)]
        rough = VMobject(color=C_DATA, stroke_width=4).set_points_smoothly(
            [[tl.x(t), lv(f), 0] for t, f in rough_pts])
        clean = trace.copy()
        self.say("Look closely and the levels are not perfect. A high is sometimes a little short of the top, and a "
                 "low floats a little above the bottom.\n"
                 "That is fine, because every gate reads anything near the top as a one and then drives its own "
                 "output all the way to the top. The small errors are wiped out at each gate instead of piling up, "
                 "and that is what makes a circuit digital.",
                 FadeOut(bits), Transform(trace, rough))
        self.zoom_to([tl.x(7), y0 + h - 0.1, 0], width=7.5)
        self.cue("a low floats", self.camera.frame.animate.move_to([tl.x(11.5), y0 + 0.1, 0]), run_time=1.6)
        self.zoom_back()
        gate = block("gate", w=1.9, h=0.9, size=40).move_to([tl.x(7), 2.5, 0])
        gate[0].set_fill(BG, opacity=1)
        self.cue("every gate reads", FadeOut(probe), FadeOut(w_lab), FadeIn(gate, scale=0.9))
        self.cue("drives its own output", Transform(trace, clean, run_time=1.6), flash_along(w, run_time=1.4))
        restored = txt("restored at every gate", color=YELLOW).next_to(hi, UP, buff=0.3).set_x(tl.x(7))
        self.cue("wiped out at each gate", FadeIn(restored, shift=UP * 0.2))
        self.hold()
        self.clear_stage()

        # four wires carrying 3 (0011), then 6 (0110); then one bus band
        tl = Timeline(0, 12, x_left=-3.6, width=8.4)
        a, b, t_ch = 3, 6, 6
        assert f"{a:04b}" == "0011" and f"{b:04b}" == "0110"
        ys = [1.9, 0.9, -0.1, -1.1]
        traces, labs = VGroup(), VGroup()
        for i, y in enumerate(ys):
            bit = 3 - i
            va, vb = (a >> bit) & 1, (b >> bit) & 1
            traces.add(bit_trace(tl, [(0, va), (t_ch, vb)], y, 0.6, rise=0.2))
            labs.add(MathTex(f"x_{bit}", font_size=44, color=GREY_A).move_to([tl.x(0) - 0.6, y + 0.3, 0]))
        vals = VGroup(MathTex("0011 = 3", font_size=46).move_to([tl.x(3), 3.0, 0]),
                      MathTex("0110 = 6", font_size=46).move_to([tl.x(9), 3.0, 0]))
        self.say("A number needs several wires, one for each bit. Here are four of them carrying the number three, "
                 "and then the number six.\n"
                 "Drawing every wire gets crowded, so we draw the whole group, called a bus, as one band with its "
                 "value written inside. Where the band pinches, the value is changing.",
                 LaggedStart(*[Create(t) for t in traces], lag_ratio=0.2, run_time=2.4), FadeIn(labs))
        self.cue("the number three", FadeIn(vals[0], shift=DOWN * 0.2))
        self.cue("the number six", FadeIn(vals[1], shift=DOWN * 0.2))
        band = bus_band(tl, [(0, t_ch, a), (t_ch, 12, b)], 0.1, h=0.9, color=C_DATA, size=56)
        band_lab = txt("X", color=C_DATA).move_to([tl.x(0) - 0.6, 0.55, 0])
        bus_word = txt("a bus", color=YELLOW).next_to(band, DOWN, buff=0.4)
        self.cue("we draw the whole group", FadeOut(vals), FadeOut(labs),
                 ReplacementTransform(traces, VGroup(band[0][0], band[1][0]), run_time=1.8),
                 FadeIn(band_lab))
        self.play(FadeIn(band[0][1]), FadeIn(band[1][1]), FadeIn(bus_word, shift=UP * 0.2), run_time=0.8)
        self.cue("Where the band pinches", Flash([tl.x(t_ch), 0.55, 0], color=YELLOW, flash_radius=0.5))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 03 delay
    def delay(self):
        tl = Timeline(0, 10, x_left=-3.0, width=8.6)
        ya, yb, yo, h = 1.7, 0.6, -0.9, 0.75
        t_in, t_out = 3, 3 + DELAY
        add = block("+", w=1.1, h=1.2).move_to([-5.9, 0.6, 0])
        rows = [("in 1", ya, C_DATA), ("in 2", yb, C_DATA), ("out", yo, C_SUM)]
        labs = VGroup(*[txt(n, color=c).move_to([tl.x(0) - 0.9, y + h / 2, 0]) for n, y, c in rows])
        a_band = bus_band(tl, [(0, t_in, 0), (t_in, 10, 3)], ya, h, C_DATA, 44)
        b_band = bus_band(tl, [(0, 10, 0)], yb, h, C_DATA, 44)
        o_band = bus_band(tl, [(0, t_out, 0), (t_out, 10, 3)], yo, h, C_SUM, 44)
        ruler = tl.ruler(-1.9, 1, "ns")
        # until its change is said, each band shows its first value running to the end
        a_full = bus_cell(tl, 0, 10, 0, ya, h, C_DATA, 44)
        o_full = bus_cell(tl, 0, 10, 0, yo, h, C_SUM, 44)
        self.say("Now watch the adder in this picture. Both inputs are zero, so the output is zero.\n"
                 "Change the top input to three. The output does become three, but not at the same moment.",
                 FadeIn(add), FadeIn(labs), FadeIn(ruler), FadeIn(a_full), FadeIn(b_band))
        self.cue("so the output is zero", FadeIn(o_full))
        l_in = tl.vline(t_in, ya + h + 0.3, -1.9, color=GREY_B)
        self.cue("Change the top input", FadeOut(a_full), FadeIn(a_band), Create(l_in))
        l_out = tl.vline(t_out, yo + h + 0.3, -1.9, color=C_SUM)
        self.cue("but not at the same moment", FadeOut(o_full), FadeIn(o_band), Create(l_out))
        self.hold()

        gap = DoubleArrow([tl.x(t_in), yo + h + 0.37, 0], [tl.x(t_out), yo + h + 0.37, 0], color=YELLOW, buff=0,
                          stroke_width=4, tip_length=0.18)
        gap_lab = txt("2 ns", color=YELLOW).next_to(gap, RIGHT, buff=0.25)
        name = txt("propagation delay", color=YELLOW).next_to(gap_lab, RIGHT, buff=0.3)
        self.say("The change has to work its way through the transistors inside. The time from an input changing "
                 "to the output settling is called the propagation delay.\n"
                 "Let's say that for this adder it is two nanoseconds.",
                 flash_along(add[0], run_time=1.5))
        self.zoom_to([tl.x(4.6), 0.35, 0], width=12.2)
        self.cue("from an input changing", GrowFromCenter(gap))
        self.cue("called the propagation delay", FadeIn(name, shift=LEFT * 0.2))
        self.cue("two nanoseconds", FadeIn(gap_lab, scale=1.3))
        self.hold(0.6)
        self.zoom_back()
        self.clear_stage()

    # ------------------------------------------------------------------ 04 runaway
    def runaway(self):
        c = circuit([0, 2.75, 0], 0.9)
        tl = Timeline(0, 16, x_left=-5.2, width=11.2)
        yx, ys, h = -0.35, -1.45, 0.75
        ruler = tl.ruler(-2.0, 2, "ns")
        x_lab = txt("X", color=C_DATA).move_to([tl.x(0) - 0.6, yx + h / 2, 0])
        s_lab = txt("S", color=C_SUM).move_to([tl.x(0) - 0.6, ys + h / 2, 0])
        x_band = bus_band(tl, [(0, 8, XS[0]), (8, 16, XS[1])], yx, h, C_DATA, 44)
        s_band = bus_band(tl, RUN, ys, h, C_SUM, 44)
        loop = VGroup(c.out_wire[0], c.fb[0])
        self.c_run = c
        self.say("With that we can test our circuit. The total starts at zero, and at time zero the first number, "
                 "three, arrives.\nThe numbers come one every eight nanoseconds, so the three stays on the input "
                 "until then.",
                 FadeIn(c.all), FadeIn(ruler), FadeIn(x_lab), FadeIn(s_lab))
        self.cue("The total starts at zero", FadeIn(s_band[0]))
        self.cue("the first number", FadeIn(x_band[0]), flash_along(c.x_wire[0]))
        l8 = tl.vline(8, yx + h + 0.25, -2.0, color=GREY_B)
        self.cue("eight nanoseconds", Create(l8))
        self.hold()

        self.say("Two nanoseconds later the adder has worked out zero plus three, and the output says three. "
                 "That is the correct total so far.",
                 flash_along(c.adder[0], run_time=1.4))
        self.cue("the output says three", FadeIn(s_band[1], shift=RIGHT * 0.2))
        self.cue("the correct total", Indicate(s_band[1], color=C_SUM))
        self.hold()

        self.say("But the output is wired back to the input, so now the adder sees three plus three, and two "
                 "nanoseconds later it says six.\nThen six plus three makes nine, and nine plus three makes twelve.",
                 flash_along(loop, run_time=2.0))
        self.cue("it says six", FadeIn(s_band[2], shift=RIGHT * 0.2))
        self.cue("makes nine", flash_along(loop, run_time=1.2), FadeIn(s_band[3], shift=RIGHT * 0.2))
        self.cue("makes twelve", flash_along(loop, run_time=1.2), FadeIn(s_band[4], shift=RIGHT * 0.2))
        self.hold()

        want = VGroup(txt("should be", color=C_SUM), num(TOTALS[1], 44, C_SUM)).arrange(RIGHT, buff=0.2)
        want.move_to([5.2, 1.7, 0])
        self.say("Only now, at eight nanoseconds, does the second number show up. The total should still be three, "
                 "ready to become four.\nInstead the wire says twelve, and it carries on to thirteen, fourteen, "
                 "fifteen.",
                 FadeIn(x_band[1]), Indicate(l8, color=YELLOW, scale_factor=1.0))
        self.cue("should still be three", FadeIn(want, shift=LEFT * 0.2))
        self.cue("the wire says twelve", s_band[4].animate.set_color(C_BAD))
        self.cue("thirteen", LaggedStart(*[FadeIn(s_band[k].set_color(C_BAD), shift=RIGHT * 0.2) for k in (5, 6, 7)],
                                         lag_ratio=0.8, run_time=2.4))
        self.hold()

        self.say("Nothing is broken here, because the adder did exactly what an adder does.\n"
                 "The trouble is that each new sum went back into the input the moment it was ready, and nothing "
                 "in the circuit ever said wait.",
                 Indicate(c.adder, color=C_LOGIC, scale_factor=1.1))
        self.cue("went back into the input", flash_along(loop, color=C_BAD, run_time=1.6))
        self.cue("ever said wait", c.fb.animate.set_color(C_BAD))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 05 hold_it
    def hold_it(self):
        self.camera.frame.set(width=11.6).move_to(ORIGIN)
        fb = circuit([0, 1.3, 0], 1.0).fb          # the bare feedback wire, about to be cut
        c = circuit([0, 1.3, 0], 1.0, reg=True)
        base = VGroup(c.adder, c.x_wire, c.out_wire, c.x_lab, c.s_lab, c.tap)
        self.c = c
        door = Dot(c.fb_d[1].get_center() + RIGHT * 0.35, radius=0.11, color=C_SUM)
        self.say("So let's say what we need. Somewhere on that feedback wire there should be a box that holds on "
                 "to the old total and keeps showing it to the adder.\n"
                 "The new sum can wait at the door, but it does not get in until we say so.",
                 FadeIn(base), FadeIn(fb))
        self.cue("Somewhere on that feedback wire", Indicate(fb, color=YELLOW, scale_factor=1.03))
        self.cue("a box that holds", FadeOut(fb), FadeIn(c.fb_d), FadeIn(c.fb_q), FadeIn(c.box, scale=0.8))
        self.cue("keeps showing it", flash_along(c.fb_q[0], color=C_SUM, run_time=1.4))
        self.cue("wait at the door", FadeIn(door, shift=LEFT * 1.2, run_time=1.2))
        self.hold()

        load = txt("load", color=YELLOW).next_to(c.load_wire, DOWN, buff=0.12)
        self.say("Give the box one extra input for that, and call it load. When load gives the signal, the box "
                 "takes in whatever is at its input, and from then on shows that at its output.\n"
                 "At all other times its input can do anything, and its output stays put.",
                 Create(c.load_wire))
        self.cue("call it load", FadeIn(load, shift=UP * 0.2))
        self.cue("When load gives the signal", flash_along(c.load_wire, run_time=0.8))
        q_dot = Dot(c.fb_q[0].get_start() + LEFT * 0.3, radius=0.11, color=C_SUM)
        self.cue("takes in whatever", door.animate.move_to(c.box), run_time=0.9)
        self.cue("shows that at its output", FadeIn(q_dot, shift=LEFT * 0.3))
        self.cue("its input can do anything", Wiggle(c.fb_d[0], scale_value=1.04, run_time=1.6))
        self.cue("its output stays put", Indicate(q_dot, color=C_SUM))
        self.hold()

        name = txt("register", color=C_REG).next_to(c.box, UP, buff=0.12)
        d_lab = txt("D", color=C_REG).next_to(c.box, RIGHT, buff=0.15).shift(DOWN * 0.36)
        q_lab = txt("Q", color=C_REG).next_to(c.box, LEFT, buff=0.15).shift(DOWN * 0.36)
        self.say("A circuit like this, one that remembers, is called a register. Its input is labelled D and its "
                 "output Q.",
                 FadeOut(door), FadeOut(q_dot))
        self.cue("called a register", FadeIn(name, shift=UP * 0.15))
        self.cue("labelled D", FadeIn(d_lab))
        self.cue("its output Q", FadeIn(q_lab))
        self.hold()

        queue = VGroup(*[num(v, 48) for v in XS]).arrange(RIGHT, buff=0.5)
        queue.next_to(c.x_wire, UP, buff=0.25).set_x(-3.2)
        every = txt("one every 8 ns", color=YELLOW).next_to(queue, UP, buff=0.25)
        self.say("Who gives the load signal, and when? We want exactly one load for each number, so it should come "
                 "at the same rhythm as the numbers themselves.\nIn our example that is once every eight "
                 "nanoseconds.",
                 Indicate(load, color=YELLOW))
        self.cue("one load for each number", LaggedStart(*[FadeIn(q, shift=DOWN * 0.2) for q in queue],
                                                         lag_ratio=0.5, run_time=2.0))
        self.cue("once every eight", FadeIn(every, shift=UP * 0.2))
        self.hold()
        self.stage5 = VGroup(queue, every, name, d_lab, q_lab)
        self.load_lab = load

    # ------------------------------------------------------------------ 06 clock
    def clock(self):
        c, load = self.c, self.load_lab
        name, d_lab, q_lab = self.stage5[2:]
        top = VGroup(c.all, load, name, d_lab, q_lab)
        tl = Timeline(0, 32, x_left=-4.6, width=10.4)
        yc, h = -2.5, 0.9
        clk = clock_wave(tl, PERIOD, yc, h, first_rise=4, rise=0.5)
        clk_lab = txt("clock", color=C_CLK).move_to([tl.x(0) - 1.0, yc + h / 2, 0])
        self.say("A computer has a signal with precisely that job. It is called the clock, and it does nothing but "
                 "go high and low, high and low, at a steady rate.\n"
                 "It is made on the motherboard and wired to every part of the chip.",
                 FadeOut(self.stage5[0]), FadeOut(self.stage5[1]),
                 top.animate.scale(0.66, about_point=[0, 1.3, 0]).shift(UP * 1.5),
                 self.camera.frame.animate.set(width=FRAME_W).move_to(ORIGIN))
        self.cue("called the clock", FadeIn(clk_lab))
        self.play(Create(clk, run_time=5.0, rate_func=linear))
        self.hold()

        edges = rising_edges(tl, PERIOD, 4)
        assert edges == [4, 12, 20, 28]
        up = Arrow([tl.x(4) - 0.5, yc + h + 0.6, 0], [tl.x(4), yc + h / 2, 0], color=YELLOW, buff=0.05,
                   stroke_width=3, tip_length=0.16)
        up_lab = txt("rising edge", color=YELLOW).next_to(up.get_start(), UP, buff=0.05).shift(LEFT * 0.4)
        dn = Arrow([tl.x(8) + 0.5, yc + h + 0.6, 0], [tl.x(8), yc + h / 2, 0], color=GREY_A, buff=0.05,
                   stroke_width=3, tip_length=0.16)
        dn_lab = txt("falling edge", color=GREY_A).next_to(dn.get_start(), UP, buff=0.05).shift(RIGHT * 1.2)
        per = DoubleArrow([tl.x(12), yc + h + 0.3, 0], [tl.x(20), yc + h + 0.3, 0], color=C_CLK, buff=0,
                          stroke_width=3, tip_length=0.16)
        per_lab = txt("one period = 8 ns", color=C_CLK).next_to(per, UP, buff=0.08)
        real = txt("a real processor: about 1 ns, a billion per second", color=GREY_A)
        real.move_to([0.4, yc + h + 1.3, 0])
        self.say("The moment it goes from low to high is called a rising edge, and the moment it comes back down "
                 "is a falling edge.\n"
                 "The time from one rising edge to the next is one clock period. Ours is eight nanoseconds. In a "
                 "real processor it is closer to one nanosecond, which is a billion ticks every second.")
        self.cue("called a rising edge", GrowArrow(up), FadeIn(up_lab))
        self.cue("a falling edge", GrowArrow(dn), FadeIn(dn_lab))
        self.cue("from one rising edge to the next", FadeOut(up), FadeOut(up_lab), FadeOut(dn), FadeOut(dn_lab),
                 GrowFromCenter(per))
        self.cue("Ours is eight", FadeIn(per_lab, shift=UP * 0.1))
        self.cue("In a real processor", FadeIn(real, shift=UP * 0.15))
        self.hold()

        tri_at = c.box.get_bottom()
        tri = VMobject(color=C_CLK, stroke_width=3).set_points_as_corners(
            [tri_at + LEFT * 0.1, tri_at + UP * 0.15, tri_at + RIGHT * 0.1])
        clk_name = txt("clock", color=C_CLK).scale(0.66).move_to(load)
        marks = VGroup(*[tl.vline(t, yc + h + 0.15, yc - 0.15) for t in edges])
        self.say("Now connect the clock to the load input. This register takes in a new value at every rising "
                 "edge, and only then.",
                 FadeOut(real), FadeOut(per), FadeOut(per_lab))
        self.cue("connect the clock", ReplacementTransform(load, clk_name), c.load_wire.animate.set_color(C_CLK),
                 Create(tri))
        self.cue("at every rising edge", LaggedStart(*[Create(m) for m in marks], lag_ratio=0.5, run_time=2.0))
        self.cue("and only then", flash_along(c.load_wire, run_time=0.8), Indicate(c.box, color=C_CLK))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 07 works
    def works(self):
        c = circuit([0, 3.0, 0], 0.7, reg=True, value="?")
        c.load_wire.set_color(C_CLK)
        c.val.set_color(C_UNKNOWN)
        out_val = num("?", 40, C_UNKNOWN).next_to(c.out_wire, UP, buff=0.12)
        x_val = blank(40).next_to(c.x_wire, UP, buff=0.12)
        tl = Timeline(0, 40, x_left=-4.6, width=11.0)
        E = rising_edges(tl, PERIOD, 4)
        assert E == [4, 12, 20, 28, 36]
        h = 0.5
        y = {"reset": 0.0, "clock": -0.7, "X": -1.4, "Q": -2.1, "S": -2.8}
        col = {"reset": GREY_A, "clock": C_CLK, "X": C_DATA, "Q": C_REG, "S": C_SUM}
        labs = VGroup(*[txt(k, color=col[k]).scale(0.85).move_to([tl.x(0) - 0.9, y[k] + h / 2, 0]) for k in y])
        reset = bit_trace(tl, [(0, 0), (1, 1), (7, 0)], y["reset"], h, GREY_A, rise=0.4)
        clk = clock_wave(tl, PERIOD, y["clock"], h, first_rise=4, rise=0.4)
        # register output: unknown, then the totals, each from its edge on
        q_segs = [(0, E[0], None)] + [(E[k], E[k + 1] if k + 1 < len(E) else 40, TOTALS[k]) for k in range(5)]
        x_segs = [(E[k], E[k + 1], XS[k]) for k in range(4)]
        s_segs = [(E[k] + DELAY, E[k + 1] + DELAY, TOTALS[k + 1]) for k in range(4)]
        assert [v for *_, v in s_segs] == [3, 4, 8, 10] and [v for *_, v in q_segs[1:]] == [0, 3, 4, 8, 10]
        q = bus_band(tl, q_segs, y["Q"], h, C_REG, 36)
        x = bus_band(tl, x_segs, y["X"], h, C_DATA, 36)
        s = bus_band(tl, s_segs, y["S"], h, C_SUM, 36)
        lines = [tl.vline(t, y["reset"] + h + 0.1, y["S"] - 0.05) for t in E]

        self.say("Let's run the list again. First the register has to start at zero, and registers have an input "
                 "for that, called reset.\n"
                 "If reset is one at a rising edge, the register clears to zero, whatever is waiting at D.",
                 FadeIn(c.all), FadeIn(out_val), FadeIn(labs[1]), Create(clk, run_time=2.0), FadeIn(labs[3]),
                 FadeIn(q[0]))
        self.cue("called reset", FadeIn(labs[0]), Create(reset, run_time=1.2))
        self.cue("at a rising edge", Create(lines[0]))
        self.cue("clears to zero", FadeIn(q[1]), set_num(c.val, 0, 44 * 0.7, C_REG), Indicate(c.box, color=C_REG))
        self.hold()

        def edge(k):
            """Edge k: the register takes the adder's value and the list moves on."""
            anims = [Create(lines[k]), FadeIn(q[k + 1]), set_num(c.val, TOTALS[k], 44 * 0.7, C_REG),
                     Indicate(c.box, color=C_CLK)]
            if k < 4:
                anims += [FadeIn(x[k]), set_num(x_val, XS[k], 40, C_DATA)]
            return anims

        def settle(k):
            return [FadeIn(s[k], shift=RIGHT * 0.15), set_num(out_val, TOTALS[k + 1], 40, C_SUM),
                    flash_along(c.adder[0], run_time=0.8)]

        self.say("The register shows zero and the first number is three, so the adder settles on three.\n"
                 "And this time the three just waits at the register's input, because no edge has come yet.",
                 FadeIn(labs[2]), FadeIn(x[0]), set_num(x_val, XS[0], 40, C_DATA), FadeIn(labs[4]))
        self.cue("the adder settles on three", *settle(0))
        self.cue("just waits", Indicate(c.fb_d, color=C_SUM, scale_factor=1.05))
        self.hold()

        self.say("Here is the edge. The register takes the three, the list moves on to one, and the adder settles "
                 "on four.\n"
                 "At the next edge the register takes the four, the list gives four, and the adder says eight. "
                 "One more edge, and eight plus two is ten.",
                 *edge(1))
        self.cue("the adder settles on four", *settle(1))
        self.cue("At the next edge", *edge(2))
        self.cue("the adder says eight", *settle(2))
        self.cue("One more edge", *edge(3))
        self.cue("eight plus two is ten", *settle(3))
        self.hold()

        self.say("At the following edge the ten is stored. Four numbers, four ticks, and the total is ten.\n"
                 "The circuit now takes one step per clock period, and the register is what holds each step back "
                 "until the next tick.",
                 *edge(4))
        self.cue("the total is ten", Circumscribe(q[5], color=YELLOW))
        self.cue("one step per clock period", LaggedStart(*[Indicate(l, color=YELLOW, scale_factor=1.0)
                                                            for l in lines], lag_ratio=0.4, run_time=2.4))
        self.cue("holds each step back", Indicate(c.box, color=C_REG, scale_factor=1.25))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 08 close
    def close(self):
        self.camera.frame.set(width=11.6).move_to(ORIGIN)
        c = circuit([0, 1.0, 0], 1.0, reg=True, value="")
        c.load_wire.set_color(C_CLK)
        clk_name = txt("clock", color=C_CLK).next_to(c.load_wire, DOWN, buff=0.12)
        reg_name = txt("register", color=C_REG).next_to(c.box, UP, buff=0.12)
        sds = txt("a synchronous digital system", color=YELLOW).move_to([0, 2.55, 0])
        self.say("So a circuit that feeds its own output back needs something that holds a value still, and "
                 "something that says when to let go. Those are the register and the clock.\n"
                 "A circuit built this way, where every change follows a clock edge, is called a synchronous "
                 "digital system.",
                 FadeIn(c.all))
        self.cue("holds a value still", Indicate(c.box, color=C_REG, scale_factor=1.2))
        self.cue("says when to let go", flash_along(c.load_wire, run_time=0.9))
        self.cue("the register and the clock", FadeIn(reg_name), FadeIn(clk_name))
        self.cue("is called a synchronous", FadeIn(sds, shift=DOWN * 0.2))
        self.hold()

        q_mark = txt("?", size=56, color=YELLOW).move_to(c.box)
        self.say("We were generous to the register, though. In our picture it took its new value in no time at "
                 "all, exactly at the edge.\n"
                 "But a register is made of transistors, just like the adder. So what is inside it, and what does "
                 "at the edge really mean?",
                 FadeOut(sds))
        self.zoom_to(VGroup(c.box, clk_name), width=7.0)
        self.cue("made of transistors", Indicate(c.adder, color=C_LOGIC), Indicate(c.box, color=C_REG))
        self.cue("what is inside it", FadeIn(q_mark, scale=1.5))
        self.cue("at the edge really mean", flash_along(c.load_wire, run_time=0.9))
        self.hold(0.8)
        self.zoom_back()
