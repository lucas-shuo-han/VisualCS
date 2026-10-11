"""Episode 5: A Register to Go Faster.

Add, then shift, between two registers; a third register in the middle shortens
the clock period; throughput goes up and latency gets worse; and the general
model of a synchronous digital system, as the shape all three circuits share.
Notes: Pipelining for Performance (all); Signals, Waveforms, and the Clock §5.
"""
import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403
from sds_common import *  # noqa: E402,F403
from ep01_runaway_sum import flash_along, tip  # noqa: E402

CQ, ADD, SHIFT, SETUP = 1, 5, 3, 1                 # ns
T_ONE = CQ + ADD + SHIFT + SETUP                   # one stage
STAGE_A, STAGE_B = CQ + ADD + SETUP, CQ + SHIFT + SETUP
T_TWO = max(STAGE_A, STAGE_B)                      # two stages, one clock
LAT_TWO = 2 * T_TWO
assert (T_ONE, STAGE_A, STAGE_B, T_TWO, LAT_TWO) == (10, 7, 5, 7, 14)
assert STAGE_A + STAGE_B == 12                     # the notes' latency formula; it equals 2 T only for equal halves
assert 1.40 < T_ONE / T_TWO < 1.45                 # "more than forty percent" more results per second
assert LAT_TWO - T_ONE == (CQ + SETUP) + (T_TWO - STAGE_B) == 4     # extra register 2 ns + idle 2 ns

PAIRS = [(3, 1), (2, 5), (6, 2), (4, 4)]
SUMS = [a + b for a, b in PAIRS]
RESULTS = [s << 1 for s in SUMS]
assert SUMS[:3] == [4, 7, 8] and RESULTS[:3] == [8, 14, 16]
ITEM = [YELLOW, BLUE_B, GREEN_B, GREY_A]           # one colour per item, to follow it across the registers

XR = [-4.6, 0.3, 5.2]                              # the three register positions
XB = [-2.15, 2.75]                                 # adder, shifter
PY = 1.9                                           # the pipeline's height on the frame


def pipeline():
    g = SimpleNamespace()
    g.regs = VGroup(*[register_box("", w=0.9, h=1.6).move_to([x, PY, 0]) for x in XR])
    g.add = block("+", w=1.6, h=1.3).move_to([XB[0], PY, 0])
    g.shift = block(r"<<", w=1.6, h=1.3).move_to([XB[1], PY, 0])
    W = lambda a, b: VGroup(wire([a, PY, 0], [b, PY, 0]), tip([b, PY, 0], RIGHT))
    g.w_in = W(XR[0] + 0.45, XB[0] - 0.8)
    g.w_direct = W(XB[0] + 0.8, XB[1] - 0.8)                       # adder straight into the shifter
    g.w_mid = VGroup(W(XB[0] + 0.8, XR[1] - 0.45), W(XR[1] + 0.45, XB[1] - 0.8))
    g.w_out = W(XB[1] + 0.8, XR[2] - 0.45)
    cy = PY - 1.35
    g.clk = VGroup(wire([XR[0] - 1.6, cy, 0], [XR[2], cy, 0], [XR[2], PY - 0.8, 0], color=C_CLK),
                   wire([XR[0], cy, 0], [XR[0], PY - 0.8, 0], color=C_CLK))
    g.clk_mid = wire([XR[1], cy, 0], [XR[1], PY - 0.8, 0], color=C_CLK)
    g.clk_l = txt("clock", color=C_CLK).scale(0.8).next_to(g.clk, DOWN, buff=0.1).set_x(XR[0] - 1.1)
    g.d_add = VGroup(num(ADD, 40, C_LOGIC), txt("ns", color=C_LOGIC).scale(0.8)).arrange(RIGHT, buff=0.12)
    g.d_add.next_to(g.add, UP, buff=0.15)
    g.d_shift = VGroup(num(SHIFT, 40, C_LOGIC), txt("ns", color=C_LOGIC).scale(0.8)).arrange(RIGHT, buff=0.12)
    g.d_shift.next_to(g.shift, UP, buff=0.15)
    g.one = VGroup(g.regs[0], g.regs[2], g.add, g.shift, g.w_in, g.w_direct, g.w_out, g.clk)
    return g


def bar(parts, x0, y, unit=0.82):
    """Delays laid end to end: [(ns, colour)], starting at x0."""
    g, x = VGroup(), x0
    for ns, col in parts:
        line = Line([x + 0.04, y, 0], [x + ns * unit - 0.04, y, 0], color=col, stroke_width=12)
        g.add(VGroup(line, num(ns, 40, col).next_to(line, UP, buff=0.12)))
        x += ns * unit
    return g


def total(b, value, color=C_CLK):
    t = VGroup(num("=", 44, color), num(value, 48, color), txt("ns", color=color)).arrange(RIGHT, buff=0.18)
    return t.next_to(b, RIGHT, buff=0.35).shift(UP * 0.2)


def mini_loop(cx, cy, label):
    """Logic with a register on its feedback wire, small."""
    b = block(label, w=1.5, h=0.95, size=36).move_to([cx, cy + 0.75, 0])
    r = register_box("", w=0.9, h=0.75, clocked=False).move_to([cx, cy - 0.85, 0])
    wires = VGroup(wire([cx - 1.6, cy + 0.95, 0], [cx - 0.75, cy + 0.95, 0]),
                   wire([cx + 0.75, cy + 0.75, 0], [cx + 1.6, cy + 0.75, 0]))
    fb = VGroup(wire([cx + 1.25, cy + 0.75, 0], [cx + 1.25, cy - 0.85, 0], [cx + 0.45, cy - 0.85, 0]),
                wire([cx - 0.45, cy - 0.85, 0], [cx - 1.25, cy - 0.85, 0], [cx - 1.25, cy + 0.55, 0],
                     [cx - 0.75, cy + 0.55, 0]))
    clk = wire([cx, cy - 1.75, 0], [cx, cy - 1.23, 0], color=C_CLK)
    return SimpleNamespace(logic=VGroup(b), regs=VGroup(r), wires=wires, fb=fb, clk=VGroup(clk),
                           all=VGroup(wires, fb, b, r))


def mini_pipe(cx, cy):
    xs = [cx - 2.0, cx, cx + 2.0]
    regs = VGroup(*[register_box("", w=0.5, h=1.0, clocked=False).move_to([x, cy, 0]) for x in xs])
    logic = VGroup(block("+", w=0.95, h=0.8, size=36).move_to([cx - 1.0, cy, 0]),
                   block(r"<<", w=0.95, h=0.8, size=36).move_to([cx + 1.0, cy, 0]))
    wires = VGroup(wire([cx - 2.6, cy, 0], [cx + 2.6, cy, 0]))
    clk = VGroup(wire([cx - 2.6, cy - 1.75, 0], [xs[2], cy - 1.75, 0], [xs[2], cy - 0.5, 0], color=C_CLK),
                 wire([xs[0], cy - 1.75, 0], [xs[0], cy - 0.5, 0], color=C_CLK),
                 wire([xs[1], cy - 1.75, 0], [xs[1], cy - 0.5, 0], color=C_CLK))
    for m in (*regs, *logic):
        m[0].set_fill(BG, opacity=1)
    return SimpleNamespace(logic=logic, regs=regs, wires=wires, fb=VGroup(), clk=clk, all=VGroup(wires, logic, regs))


class Ep05Pipelining(NarratedScene):
    SCENES = ["recap", "one_stage", "idea", "flow", "trade", "model"]

    def construct(self):
        if self.preview_only(["one_stage", "idea"]):
            return
        self.title_card()
        for s in self.SCENES:
            getattr(self, s)()
        self.end_card([
            "A register between two blocks lets each block have a clock period of its own.",
            "The period is set by the slowest stage.",
            "Pipelining raises throughput, results per second, and makes latency, the time for one item, worse.",
            "A synchronous digital system is logic blocks between registers, with a clock that drives only the registers.",
        ])

    # ------------------------------------------------------------------ 01 recap
    def recap(self):
        rule = MathTex(r"T", r"\;\ge\;", r"t_{\text{clock-to-q}}", "+", r"t_{\text{slowest logic}}", "+",
                       r"t_{\text{setup}}", font_size=52)
        rule[0].set_color(C_CLK), rule[2].set_color(C_CQ), rule[4].set_color(C_LOGIC), rule[6].set_color(C_WINDOW)
        rule.move_to([0, 2.4, 0])
        r1 = register_box("", w=0.9, h=1.5).move_to([-3.2, -0.3, 0])
        r2 = register_box("", w=0.9, h=1.5).move_to([3.2, -0.3, 0])
        lg = block("logic", w=3.0, h=1.3).move_to([0, -0.3, 0])
        ws = VGroup(wire(r1.get_right(), lg.get_left()), wire(lg.get_right(), r2.get_left()))
        route = VGroup(ws[0], ws[1])
        self.say("The clock period has to cover the slowest route from one register to the next.\n"
                 "Today we use that rule backwards. If a route is too slow, we change the route.",
                 FadeIn(rule, shift=DOWN * 0.15), FadeIn(VGroup(r1, r2, lg, ws)))
        self.cue("the slowest route", flash_along(route, color=C_BAD, run_time=1.6))
        self.cue("we change the route", Indicate(lg, color=YELLOW, scale_factor=1.1))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 02 one_stage
    def one_stage(self):
        g = self.g = pipeline()
        (a, b), s, r = PAIRS[0], SUMS[0], RESULTS[0]
        v_in = MathTex(f"{a},\\ {b}", font_size=44, color=ITEM[0]).next_to(g.w_in, DOWN, buff=0.12)
        v_sum = num(s, 44, ITEM[0]).next_to(g.w_direct, DOWN, buff=0.12)
        v_res = num(r, 44, ITEM[0]).next_to(g.w_out, DOWN, buff=0.12)
        self.say("Here is a piece of a processor. Two numbers come out of a register, an adder adds them, a shifter "
                 "shifts the sum, and the result goes into a second register.\n"
                 "For example three plus one is four, and shifted left by one bit that becomes eight.",
                 FadeIn(g.regs[0]), FadeIn(g.clk), FadeIn(g.clk_l), FadeIn(g.regs[2]))
        self.cue("an adder adds them", Create(g.w_in), FadeIn(g.add, scale=0.9))
        self.cue("a shifter shifts the sum", Create(g.w_direct), FadeIn(g.shift, scale=0.9))
        self.cue("into a second register", Create(g.w_out), Indicate(g.regs[2], color=C_REG))
        self.cue("three plus one is four", FadeIn(v_in), FadeIn(v_sum, shift=RIGHT * 0.3))
        self.cue("that becomes eight", FadeIn(v_res, shift=RIGHT * 0.3))
        self.hold()

        facts = VGroup(txt("clock-to-q 1 ns", color=C_CQ), txt("setup 1 ns", color=C_WINDOW)).scale(0.85)
        facts.arrange(RIGHT, buff=0.8).move_to([0, 3.55, 0])
        self.b1 = b1 = bar([(CQ, C_CQ), (ADD, C_LOGIC), (SHIFT, C_LOGIC), (SETUP, C_WINDOW)], -4.6, -1.4)
        self.t1 = t1 = total(b1, T_ONE)
        self.say("For the timing, say the adder takes five nanoseconds and the shifter three, and each register "
                 "has a clock to q delay of one and a setup time of one.\n"
                 "The only route goes through everything, so the period is one plus five plus three plus one, "
                 "which is ten nanoseconds.",
                 FadeOut(v_in), FadeOut(v_sum), FadeOut(v_res))
        self.cue("the adder takes five", FadeIn(g.d_add, shift=DOWN * 0.15))
        self.cue("the shifter three", FadeIn(g.d_shift, shift=DOWN * 0.15))
        self.cue("a clock to q delay of one", FadeIn(facts[0]))
        self.cue("a setup time of one", FadeIn(facts[1]))
        self.cue("goes through everything", flash_along(VGroup(g.w_in[0], g.w_direct[0], g.w_out[0]), color=C_BAD,
                                                         run_time=1.6))
        self.cue("one plus five plus three plus one", LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in b1],
                                                                 lag_ratio=0.5, run_time=2.4))
        self.cue("ten nanoseconds", FadeIn(t1, shift=LEFT * 0.2))
        self.hold()

        facts2 = VGroup(txt("one result every 10 ns", color=GREY_A), txt("each takes 10 ns", color=GREY_A)).scale(0.85)
        facts2.arrange(RIGHT, buff=1.0).move_to([0, -2.55, 0])
        self.say("At every edge a new pair goes in on the left, and the previous result is caught on the right.\n"
                 "So we get one result every ten nanoseconds, and each result takes ten nanoseconds from going in "
                 "to being caught.",
                 flash_along(g.clk[0], run_time=1.0))
        self.cue("a new pair goes in", Indicate(g.regs[0], color=YELLOW))
        self.cue("caught on the right", Indicate(g.regs[2], color=YELLOW))
        self.cue("one result every ten", FadeIn(facts2[0], shift=UP * 0.15))
        self.cue("each result takes ten", FadeIn(facts2[1], shift=UP * 0.15))
        self.hold()
        self.facts, self.facts2 = facts, facts2

    # ------------------------------------------------------------------ 03 idea
    def idea(self):
        g = self.g
        path = VGroup(g.w_in[0], g.w_direct[0], g.w_out[0])
        self.say("Suppose that is not fast enough. We can't make the adder or the shifter any quicker.\n"
                 "But notice why the period is long. It is long only because one signal must get through both of "
                 "them between two edges.",
                 FadeOut(self.facts2))
        self.cue("the adder or the shifter", Indicate(g.add, color=C_LOGIC), Indicate(g.shift, color=C_LOGIC))
        self.cue("one signal must get through both", flash_along(path, color=C_BAD, run_time=2.0))
        self.cue("between two edges", Indicate(g.regs[0], color=C_CLK), Indicate(g.regs[2], color=C_CLK))
        self.hold()

        self.say("So let's stop asking for that. Put a third register between the adder and the shifter.\n"
                 "Now the sum is caught in the middle at one edge, and the shifter works on it during the next "
                 "period.")
        self.cue("Put a third register", FadeOut(g.w_direct), FadeIn(g.w_mid), FadeIn(g.regs[1], shift=DOWN * 0.6),
                 Create(g.clk_mid))
        self.cue("caught in the middle", flash_along(VGroup(g.w_in[0], g.w_mid[0][0]), color=YELLOW, run_time=1.2),
                 Indicate(g.regs[1], color=YELLOW))
        self.cue("the shifter works on it", flash_along(VGroup(g.w_mid[1][0], g.w_out[0]), color=YELLOW,
                                                        run_time=1.2))
        self.hold()

        ba = bar([(CQ, C_CQ), (ADD, C_LOGIC), (SETUP, C_WINDOW)], -4.6, -1.0)
        bb = bar([(CQ, C_CQ), (SHIFT, C_LOGIC), (SETUP, C_WINDOW)], -4.6, -2.3)
        ta, tb = total(ba, STAGE_A), total(bb, STAGE_B, GREY_A)
        period = VGroup(txt("period", color=C_CLK), num(T_TWO, 48, C_CLK), txt("ns", color=C_CLK)).arrange(RIGHT, buff=0.2)
        period.move_to([4.6, -1.5, 0])
        was = VGroup(txt("was", color=GREY_B), num(T_ONE, 44, GREY_B)).arrange(RIGHT, buff=0.2).scale(0.85)
        was.next_to(period, DOWN, buff=0.25)
        self.say("Each period only has to cover one of the two halves. The first half is one plus five plus one, "
                 "seven nanoseconds, and the second is one plus three plus one, five.\n"
                 "One clock drives all the registers, so the period has to suit the slower half. That gives seven "
                 "nanoseconds instead of ten.",
                 FadeOut(self.t1), FadeOut(self.b1))
        self.cue("The first half is", LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in ba], lag_ratio=0.4,
                                                   run_time=1.6))
        self.cue("seven nanoseconds, and", FadeIn(ta, shift=LEFT * 0.2))
        self.cue("the second is", LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in bb], lag_ratio=0.4, run_time=1.6))
        self.cue("plus one, five", FadeIn(tb, shift=LEFT * 0.2))
        self.cue("One clock drives all", flash_along(g.clk[0], run_time=1.2), flash_along(g.clk_mid, run_time=1.2))
        self.cue("suit the slower half", Indicate(ta, color=YELLOW))
        self.cue("instead of ten", FadeIn(period, shift=UP * 0.15), FadeIn(was))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 04 flow
    def flow(self):
        g = pipeline()
        two = VGroup(g.regs, g.add, g.shift, g.w_in, g.w_mid, g.w_out, g.clk, g.clk_mid)
        ys = [-0.45, -1.15, -1.85, -2.55]
        heads = VGroup(*[txt(f"edge {e + 1}", color=C_CLK).scale(0.8).move_to([XR[0] - 1.75, y, 0])
                         for e, y in enumerate(ys)])

        def entry(e, col):
            """What register `col` holds after edge e (0-based), or None."""
            k = e - col
            if not 0 <= k < len(PAIRS):
                return None
            if col == 0:
                m = MathTex(f"{PAIRS[k][0]},\\ {PAIRS[k][1]}", font_size=44, color=ITEM[k])
            else:
                m = num(SUMS[k] if col == 1 else RESULTS[k], 44, ITEM[k])
            return m.move_to([XR[col], ys[e], 0])

        cell = {(e, c): entry(e, c) for e in range(4) for c in range(3)}
        assert cell[(0, 1)] is None and cell[(2, 2)] is not None
        guides = VGroup(*[DashedLine([x, PY - 0.9, 0], [x, ys[-1] - 0.3, 0], color=GREY_D, stroke_width=2) for x in XR])

        def moved(e, c):
            """The entry of register c after edge e, arriving from the register to its left."""
            return FadeIn(cell[(e, c)], shift=RIGHT * 0.6 + DOWN * 0.2) if c else FadeIn(cell[(e, c)], shift=DOWN * 0.2)

        self.say("Watch the data move. At the first edge the pair three and one goes in.\n"
                 "At the second edge its sum, four, is caught in the middle. And at that same edge a new pair goes "
                 "in on the left, because the adder is free again.",
                 FadeIn(two), FadeIn(guides))
        self.cue("At the first edge", FadeIn(heads[0]), flash_along(g.clk[0], run_time=0.8), moved(0, 0))
        self.cue("At the second edge", FadeIn(heads[1]), flash_along(g.clk[0], run_time=0.8), moved(1, 1))
        self.cue("a new pair goes in", moved(1, 0))
        self.cue("the adder is free again", Indicate(g.add, color=YELLOW))
        self.hold()

        self.say("At the third edge the first result, eight, is caught on the right. The second sum moves to the "
                 "middle, and a third pair goes in.\n"
                 "From then on a finished result comes out at every edge, and two computations are always under "
                 "way at once, one in each half.",
                 FadeIn(heads[2]), flash_along(g.clk[0], run_time=0.8), moved(2, 2))
        self.cue("The second sum moves", moved(2, 1))
        self.cue("a third pair goes in", moved(2, 0))
        self.cue("From then on", FadeIn(heads[3]), flash_along(g.clk[0], run_time=0.8), moved(3, 2), moved(3, 1),
                 moved(3, 0))
        done = SurroundingRectangle(VGroup(cell[(2, 2)], cell[(3, 2)]), color=YELLOW, buff=0.15)
        self.cue("at every edge", Create(done))
        self.cue("one in each half", Indicate(g.add, color=YELLOW), Indicate(g.shift, color=YELLOW))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 05 trade
    def trade(self):
        xc = [0.6, 4.2]
        heads = VGroup(txt("one stage", color=GREY_A).move_to([xc[0], 2.9, 0]),
                       txt("two stages", color=C_REG).move_to([xc[1], 2.9, 0]))
        row1 = txt("one result every", color=C_DATA).move_to([-3.9, 1.7, 0])
        row2 = txt("one item takes", color=C_DATA).move_to([-3.9, 0.3, 0])
        val = lambda v, x, y, col: VGroup(num(v, 56, col), txt("ns", color=col)).arrange(RIGHT, buff=0.15).move_to([x, y, 0])
        v = [val(T_ONE, xc[0], 1.7, GREY_A), val(T_TWO, xc[1], 1.7, C_SUM),
             val(T_ONE, xc[0], 0.3, GREY_A), val(LAT_TWO, xc[1], 0.3, C_BAD)]
        thr = txt("throughput", color=YELLOW).scale(0.85).next_to(row1, DOWN, buff=0.12)
        lat = txt("latency", color=YELLOW).scale(0.85).next_to(row2, DOWN, buff=0.12)
        self.say("Now compare the two designs. Before, we got one result every ten nanoseconds, and now we get one "
                 "every seven.\n"
                 "The number of results per second is called the throughput, and it has gone up by more than "
                 "forty percent.",
                 FadeIn(heads), FadeIn(row1))
        self.cue("one result every ten", FadeIn(v[0], shift=UP * 0.15))
        self.cue("one every seven", FadeIn(v[1], shift=UP * 0.15))
        self.cue("called the throughput", FadeIn(thr, shift=UP * 0.1))
        self.cue("gone up by more than", Indicate(v[1], color=C_SUM, scale_factor=1.25))
        self.hold()

        self.say("But follow one single pair. It needs two periods to get through, and two times seven is fourteen "
                 "nanoseconds, where before it needed ten.\n"
                 "The time one item takes from start to finish is called the latency, and it got worse.",
                 FadeIn(row2))
        self.cue("two times seven is fourteen", FadeIn(v[3], shift=UP * 0.15))
        self.cue("before it needed ten", FadeIn(v[2], shift=UP * 0.15))
        self.cue("called the latency", FadeIn(lat, shift=UP * 0.1))
        self.cue("it got worse", Indicate(v[3], color=C_BAD, scale_factor=1.25))
        self.hold()

        parts = VGroup(
            VGroup(num(LAT_TWO, 52, C_BAD), num("=", 52)).arrange(RIGHT, buff=0.3),
            VGroup(num(T_ONE, 52, GREY_A), txt("as before", color=GREY_A).scale(0.75)).arrange(DOWN, buff=0.15),
            num("+", 52),
            VGroup(num(CQ + SETUP, 52, C_REG), txt("extra register", color=C_REG).scale(0.75)).arrange(DOWN, buff=0.15),
            num("+", 52),
            VGroup(num(T_TWO - STAGE_B, 52, C_CLK), txt("waiting", color=C_CLK).scale(0.75)).arrange(DOWN, buff=0.15))
        parts.arrange(RIGHT, buff=0.45, aligned_edge=UP).move_to([0.6, -1.9, 0])
        self.say("It got worse for two reasons. The item now passes an extra register and pays that register's "
                 "clock to q and setup time.\n"
                 "And the faster half sits idle for two nanoseconds in every period, because the clock is set by "
                 "the slower half.",
                 FadeIn(parts[0]), FadeIn(parts[1]))
        self.cue("passes an extra register", FadeIn(parts[2]), FadeIn(parts[3], shift=UP * 0.15))
        self.cue("sits idle for two nanoseconds", FadeIn(parts[4]), FadeIn(parts[5], shift=UP * 0.15))
        self.hold()

        name = txt("pipelining", size=56, color=YELLOW).move_to([-3.9, 2.95, 0])
        self.say("This move is called pipelining. It is the right trade when you care about results per second, as "
                 "a processor running a long stream of instructions does.\n"
                 "It is the wrong one when you only care how soon a single answer comes back.",
                 FadeOut(parts))
        self.cue("called pipelining", FadeIn(name, scale=1.2))
        self.cue("results per second", Indicate(thr, color=YELLOW), Indicate(v[1], color=C_SUM))
        self.cue("how soon a single answer", Indicate(lat, color=YELLOW), Indicate(v[3], color=C_BAD))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 06 model
    def model(self):
        cy = 0.9
        m = [mini_loop(-5.05, cy, "+"), mini_loop(-1.25, cy, "logic"), mini_pipe(3.9, cy)]
        names = VGroup(*[txt(s, color=GREY_A).scale(0.8).move_to([x, cy - 2.35, 0])
                         for s, x in (("running sum", -5.05), ("three ones", -1.25), ("pipeline", 3.9))])
        logic = VGroup(*[x.logic for x in m])
        regs = VGroup(*[x.regs for x in m])
        clks = VGroup(*[x.clk for x in m])
        self.say("Step back and look at the three circuits of this series, the running sum, the machine that "
                 "counts ones, and this pipeline.\n"
                 "They are all built the same way. There are blocks of logic with no memory, separated by "
                 "registers, and a clock that connects to the registers and to nothing else.")
        for k, phrase in enumerate(("the running sum", "the machine that counts ones", "this pipeline")):
            self.cue(phrase, FadeIn(m[k].all, shift=UP * 0.2), FadeIn(names[k]))
        self.cue("blocks of logic with no memory", Indicate(logic, color=C_LOGIC, scale_factor=1.08))
        self.cue("separated by registers", Indicate(regs, color=C_REG, scale_factor=1.08))
        self.cue("a clock that connects", LaggedStart(*[Create(c) for c in clks], lag_ratio=0.2, run_time=1.8))
        self.hold()

        sds = txt("a synchronous digital system", size=48, color=YELLOW).move_to([0, 3.2, 0])
        self.say("Sometimes a register's output loops back, as in the first two, and sometimes the data only moves "
                 "forward. Registers can sit back to back, and so can logic blocks.\n"
                 "That is the whole model of a synchronous digital system, and a processor is a large one of "
                 "these.",
                 flash_along(m[0].fb, color=YELLOW, run_time=1.6), flash_along(m[1].fb, color=YELLOW, run_time=1.6))
        self.cue("only moves forward", flash_along(m[2].wires, color=YELLOW, run_time=1.6))
        self.cue("the whole model", FadeIn(sds, shift=DOWN * 0.15))
        self.cue("a processor is a large one", Indicate(VGroup(*[x.all for x in m]), color=YELLOW, scale_factor=1.03))
        self.hold(1.0)
