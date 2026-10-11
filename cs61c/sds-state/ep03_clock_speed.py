"""Episode 3: How Fast Can the Clock Tick?

One clock period of the accumulator in numbers; inputs that arrive late; the
period squeezed until the register stores a wrong sum (the critical path); and
the opposite failure, a route that is too fast (a hold violation).
Notes: Timing a Synchronous System §1, §2.3-2.4, §3, §4; Summary (two relationships).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403
from sds_common import *  # noqa: E402,F403
from ep01_runaway_sum import circuit, flash_along  # noqa: E402

CQ, ADD, SETUP = 1, 5, 1          # ns: clock-to-q, adder delay, setup time
READY = CQ + ADD                  # the new sum is ready this long after the edge
T_MIN = CQ + ADD + SETUP
assert READY == 6 and T_MIN == 7
assert all((T - SETUP >= READY) == ok for T, ok in [(10, True), (8, True), (7, True), (6, False)])
assert 10 - SETUP - READY == 3    # three nanoseconds to spare at a period of ten
X_LATE = 3                        # scene `late`: the next number shows up at 3 ns
SETTLE_LATE = X_LATE + ADD
assert SETTLE_LATE == 8 and SETTLE_LATE <= 10 - SETUP
OLD, STORED, NEXT = 0, 3, 1       # the register held 0, now holds 3; the list moves from 3 to 1
WRONG = STORED + 3                # what the adder starts on while the old number is still there
assert WRONG == 6 and STORED + NEXT == 4
MHZ = 1000 / T_MIN
assert round(MHZ) == 143

# the notes' quick check: gate delays 1 ns, clock-to-q 1 ns, setup 1 ns
GATES_ON = {"a": 2, "b": 3, "c": 2, "d": 2, "q": 3}      # AND gates between each source and the register
CRIT = 1 + max(GATES_ON.values()) + 1
assert CRIT == 5 and 1000 / CRIT == 200

H_HOLD, H_CQ = 2, 1               # scene `hold`
assert H_CQ + 0 < H_HOLD and H_CQ + 1 >= H_HOLD


def lab(text, y, tl, h, color=C_DATA):
    return txt(text, color=color).scale(0.85).move_to([tl.x(tl.t0) - 0.8, y + h / 2, 0])


def seg(tl, t_a, t_b, y, text, color):
    """A labelled stretch of time: a thick bar with a number above it."""
    bar = Line([tl.x(t_a) + 0.03, y, 0], [tl.x(t_b) - 0.03, y, 0], color=color, stroke_width=10)
    return VGroup(bar, num(text, 36, color).next_to(bar, DOWN, buff=0.1))


def route(p, q, bend=0.5):
    """A wire from p to q with one vertical run, `bend` of the way across."""
    p, q = np.array(p, dtype=float), np.array(q, dtype=float)
    xm = p[0] + (q[0] - p[0]) * bend
    return wire(p, [xm, p[1], 0], [xm, q[1], 0], q)


class Ep03ClockSpeed(NarratedScene):
    SCENES = ["recap", "cycle", "late", "squeeze", "critical", "hold_scene", "close"]

    def construct(self):
        if self.preview_only(["cycle", "late", "squeeze"]):
            return
        self.title_card()
        for s in self.SCENES:
            getattr(self, s)()
        self.end_card([
            "Signals may wobble in the middle of a period. They must be steady around the edge.",
            "The shortest period is clock to q, plus the slowest logic, plus setup.",
            "That slowest route between two registers is the critical path.",
            "A route can also be too fast for the hold time, and a slower clock does not fix that.",
        ])

    # ------------------------------------------------------------------ 01 recap
    def recap(self):
        self.camera.frame.set(width=11.6).move_to(ORIGIN)
        c = circuit([0, 1.0, 0], 1.0, reg=True, value=3)
        c.load_wire.set_color(C_CLK)
        c.val.set_color(C_REG)
        clk = txt("clock", color=C_CLK).next_to(c.load_wire, DOWN, buff=0.12)
        win = Rectangle(width=0.5, height=0.8, stroke_width=0, fill_color=C_WINDOW, fill_opacity=0.45)
        win.move_to(c.fb_d[1].get_center() + RIGHT * 0.3)
        self.say("We have an adder with a register on its feedback wire, and we know that a register needs its "
                 "input steady in a window around each rising edge.\n"
                 "Today we put the two together and ask how fast this circuit can be clocked.",
                 FadeIn(c.all), FadeIn(clk))
        self.cue("a register on its feedback wire", Indicate(c.box, color=C_REG, scale_factor=1.15))
        self.cue("steady in a window", FadeIn(win, scale=1.4))
        self.cue("how fast this circuit", flash_along(c.load_wire, run_time=0.7))
        self.play(flash_along(c.load_wire, run_time=0.5))
        self.hold()
        self.clear_stage()
        self.camera.frame.set(width=FRAME_W).move_to(ORIGIN)

    # ------------------------------------------------------------------ 02 cycle
    def stage(self):
        """The picture the three timing scenes share: circuit, the three delays, a ruler in ns."""
        self.c = c = circuit([-3.9, 2.75, 0], 0.55, reg=True, value=STORED)
        c.load_wire.set_color(C_CLK)
        c.val.set_color(C_REG)
        rows = [("clock-to-q", CQ, C_CQ), ("adder", ADD, C_LOGIC), ("setup", SETUP, C_WINDOW)]
        self.legend = VGroup(*[VGroup(txt(n, color=col), num(v, 44, col), txt("ns", color=col)).arrange(RIGHT, buff=0.18)
                               for n, v, col in rows]).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        self.legend.move_to([1.2, 2.3, 0])
        self.tl = tl = Timeline(0, 11, x_left=-4.4, width=10.6)
        self.h = h = 0.5
        self.y = y = {"clock": 0.25, "Q": -0.5, "X": -1.2, "S": -1.9}
        self.ruler = tl.ruler(-2.75, 1, "ns", size=26)
        self.labs = {k: lab(k, v, tl, h, {"clock": C_CLK, "Q": C_REG, "X": C_DATA, "S": C_SUM}[k]) for k, v in y.items()}
        self.e0 = tl.vline(0, y["clock"] + h + 0.15, -2.75)

    def clock_for(self, T):
        """Clock trace, next edge and the setup window for a period of T."""
        tl, y, h = self.tl, self.y, self.h
        trace = bit_trace(tl, [(0, 1), (T / 2, 0), (T, 1)], y["clock"], h, C_CLK, rise=0.25)
        edge = tl.vline(T, y["clock"] + h + 0.15, -2.75)
        win = tl.window(T - SETUP, T, y["Q"] + h + 0.1, y["S"] - 0.1)
        return VGroup(trace, edge, win)

    def cycle(self):
        self.stage()
        c, tl, y, h = self.c, self.tl, self.y, self.h
        self.clk = self.clock_for(10)
        self.q = bus_band(tl, [(0, CQ, OLD), (CQ, 11, STORED)], y["Q"], h, C_REG, 36)
        self.x = bus_band(tl, [(0, CQ, 3), (CQ, 11, NEXT)], y["X"], h, C_DATA, 36)
        self.s = bus_band(tl, [(0, READY, STORED), (READY, 11, STORED + NEXT)], y["S"], h, C_SUM, 36)
        self.say("Give everything a number. The register has a clock to q delay of one nanosecond and a setup time "
                 "of one nanosecond.\nThe adder takes five nanoseconds, and the clock period is ten.",
                 FadeIn(c.all), FadeIn(self.ruler))
        self.cue("a clock to q delay", FadeIn(self.legend[0], shift=LEFT * 0.2), Indicate(c.box, color=C_CQ))
        self.cue("a setup time", FadeIn(self.legend[2], shift=LEFT * 0.2))
        self.cue("The adder takes five", FadeIn(self.legend[1], shift=LEFT * 0.2), Indicate(c.adder, color=C_LOGIC))
        self.cue("the clock period is ten", FadeIn(self.labs["clock"]), Create(self.clk[0], run_time=1.6),
                 Create(self.e0), Create(self.clk[1]))
        self.hold()

        m1 = tl.vline(CQ, y["Q"] + h + 0.1, -2.75, color=C_CQ)
        m6 = tl.vline(READY, y["S"] + h + 0.1, -2.75, color=C_SUM)
        self.say("Follow one period, starting at a rising edge. One nanosecond later the register's output shows "
                 "the stored total.\nSuppose the next number from the list shows up at that moment too. The adder "
                 "now has both inputs, and five nanoseconds later, at six, the new sum is ready.",
                 Indicate(self.e0, color=YELLOW, scale_factor=1.0), FadeIn(self.labs["Q"]), FadeIn(self.q[0]))
        self.cue("One nanosecond later", Create(m1), FadeIn(self.q[1], shift=RIGHT * 0.15))
        self.cue("the next number from the list", FadeIn(self.labs["X"]), FadeIn(self.x[0]),
                 FadeIn(self.x[1], shift=RIGHT * 0.15))
        self.cue("The adder now has both", FadeIn(self.labs["S"]), FadeIn(self.s[0]),
                 flash_along(c.adder[0], run_time=1.2))
        self.cue("at six, the new sum", Create(m6), FadeIn(self.s[1], shift=RIGHT * 0.15))
        self.hold()

        m9 = tl.vline(10 - SETUP, y["Q"] + h + 0.1, -2.75, color=C_WINDOW)
        spare = VGroup(DoubleArrow([tl.x(READY), y["S"] - 0.3, 0], [tl.x(9), y["S"] - 0.3, 0], color=YELLOW, buff=0,
                                   stroke_width=4, tip_length=0.16),
                       txt("3 ns to spare", color=YELLOW).scale(0.85))
        spare[1].next_to(spare[0], LEFT, buff=0.2)
        self.say("The next edge comes at ten, and the register needs its input steady one nanosecond before that, "
                 "so from nine on.\nThe sum has been waiting since six, which leaves three nanoseconds to spare.",
                 Indicate(self.clk[1], color=YELLOW, scale_factor=1.0))
        self.cue("steady one nanosecond before", FadeIn(self.clk[2]))
        self.cue("from nine on", Create(m9))
        self.cue("waiting since six", Indicate(self.s[1], color=C_SUM, scale_factor=1.05))
        self.cue("three nanoseconds to spare", GrowFromCenter(spare[0]), FadeIn(spare[1]))
        self.hold()
        self.marks = VGroup(m1, m6, m9)
        self.spare = spare

    # ------------------------------------------------------------------ 03 late
    def late(self):
        tl, y, h = self.tl, self.y, self.h
        x_late = bus_band(tl, [(0, X_LATE, 3), (X_LATE, 11, NEXT)], y["X"], h, C_DATA, 36)
        s_late = bus_band(tl, [(0, READY, STORED), (READY, SETTLE_LATE, None), (SETTLE_LATE, 11, STORED + NEXT)],
                          y["S"], h, C_SUM, 36)
        m3 = tl.vline(X_LATE, y["X"] + h + 0.1, -2.75, color=C_DATA)
        m8 = tl.vline(SETTLE_LATE, y["S"] + h + 0.1, -2.75, color=C_SUM)
        self.say("In a real machine the two inputs rarely arrive together. Say the stored total shows up at one "
                 "nanosecond as before, but the next number from the list only at three.",
                 FadeOut(self.spare), FadeOut(self.marks[1]))
        self.cue("the stored total shows up", Indicate(self.q[1], color=C_REG, scale_factor=1.03))
        self.cue("only at three", FadeOut(self.x), FadeIn(x_late), Create(m3))
        self.hold()

        clash = tl.window(CQ, X_LATE, y["Q"] + h + 0.08, y["X"] - 0.08, color=C_BAD, opacity=0.35)
        wrong = MathTex("3 + 3", font_size=44, color=C_BAD).next_to(clash, UP, buff=0.12)
        self.say("For those two nanoseconds the adder sees the new total next to the old number. Right after the "
                 "first number was stored, that means it starts adding three plus three, which nobody asked for.",
                 FadeIn(clash))
        self.cue("three plus three", FadeIn(wrong, shift=UP * 0.15))
        self.hold()

        self.say("That wrong sum does travel through the adder, so for a while the output is garbage.\n"
                 "Then at three the right number arrives, and five nanoseconds later, at eight, the output settles "
                 "on the right sum.",
                 flash_along(self.c.adder[0], color=C_BAD, run_time=1.4))
        self.cue("the output is garbage", FadeOut(self.s), FadeIn(s_late[0]), FadeIn(s_late[1]))
        self.cue("the right number arrives", FadeOut(clash), FadeOut(wrong), Indicate(x_late[1], color=YELLOW,
                                                                                    scale_factor=1.03))
        self.cue("at eight, the output settles", Create(m8), FadeIn(s_late[2], shift=RIGHT * 0.15))
        self.hold()

        self.say("Eight is still before nine. The register only looks during its small window around the edge, so "
                 "it never sees the garbage.\nThis happens in every circuit. Signals wobble in the middle of a "
                 "period, and all that matters is that they are quiet when the edge comes.",
                 Indicate(m8, color=YELLOW, scale_factor=1.0), Indicate(self.marks[2], color=YELLOW, scale_factor=1.0))
        self.cue("its small window", Indicate(self.clk[2], color=C_WINDOW, scale_factor=1.1))
        self.cue("never sees the garbage", Indicate(s_late[1], color=C_UNKNOWN, scale_factor=1.1))
        self.cue("quiet when the edge comes", Indicate(self.clk[1], color=YELLOW, scale_factor=1.0))
        self.hold()
        self.late_bits = VGroup(x_late, s_late, m3, m8)

    # ------------------------------------------------------------------ 04 squeeze
    def squeeze(self):
        tl, y, h = self.tl, self.y, self.h
        m6 = tl.vline(READY, y["S"] + h + 0.1, -2.75, color=C_SUM)
        per = VGroup(txt("period", color=C_CLK), num(10, 48, C_CLK), txt("ns", color=C_CLK)).arrange(RIGHT, buff=0.2)
        per.move_to([5.1, 2.9, 0])

        def set_T(T):
            return [Transform(self.clk, self.clock_for(T)),
                    Transform(per[1], num(T, 48, C_CLK).move_to(per[1]))]

        self.say("So how short can the period be? Go back to both inputs arriving at one nanosecond, with the sum "
                 "ready at six.\nTry a period of eight. The window now opens at seven, and the sum is there in "
                 "time.",
                 FadeOut(self.late_bits), FadeOut(self.marks[2]), FadeIn(self.x), FadeIn(self.s), Create(m6),
                 FadeIn(per))
        self.cue("Try a period of eight", *set_T(8), run_time=1.6)
        self.cue("the sum is there in time", Indicate(self.s[1], color=C_SUM, scale_factor=1.04))
        self.hold()

        bad = txt("stores the wrong value", color=C_BAD).scale(0.8).move_to([5.05, 2.0, 0])
        self.say("Try seven. The window opens at six, exactly when the sum settles, and that just works.\n"
                 "Now try six. The window opens at five, the adder is still working, and the register stores "
                 "whatever happens to be on the wire. The total is wrong, and so is every total after it.",
                 *set_T(7), run_time=1.6)
        self.cue("exactly when the sum settles", Indicate(m6, color=YELLOW, scale_factor=1.0))
        self.cue("Now try six", *set_T(6), run_time=1.6)
        self.cue("the adder is still working", self.clk[2].animate.set_fill(C_BAD, opacity=0.4),
                 Indicate(self.s[0], color=C_BAD, scale_factor=1.04))
        self.cue("stores whatever happens", FadeIn(bad, shift=UP * 0.15),
                 self.c.val.animate.set_color(C_BAD))
        self.hold()

        bars = VGroup(seg(tl, 0, CQ, -2.25, CQ, C_CQ), seg(tl, CQ, READY, -2.25, ADD, C_LOGIC),
                      seg(tl, READY, T_MIN, -2.25, SETUP, C_WINDOW))
        self.say("So seven nanoseconds is the shortest period, and we can read off where it comes from.\n"
                 "One nanosecond for the register to show its value, five for the adder, and one for the setup "
                 "time of the register that catches the result.",
                 FadeOut(bad), FadeOut(self.ruler), *set_T(7), self.c.val.animate.set_color(C_REG))
        self.cue("One nanosecond for the register", FadeIn(bars[0]), Indicate(self.legend[0], color=C_CQ))
        self.cue("five for the adder", FadeIn(bars[1]), Indicate(self.legend[1], color=C_LOGIC))
        self.cue("one for the setup time", FadeIn(bars[2]), Indicate(self.legend[2], color=C_WINDOW))
        self.hold()

        rule = MathTex(r"T", r"\;\ge\;", r"t_{\text{clock-to-q}}", "+", r"t_{\text{logic}}", "+",
                       r"t_{\text{setup}}", font_size=50)
        rule[0].set_color(C_CLK), rule[2].set_color(C_CQ), rule[4].set_color(C_LOGIC), rule[6].set_color(C_WINDOW)
        rule.move_to([2.3, 3.0, 0])
        self.say("In general the period has to be at least the clock to q delay, plus the delay of the logic, plus "
                 "the setup time.\nThe hold time is not in this sum, because it concerns what happens just after "
                 "an edge, not how long the logic takes.",
                 FadeOut(self.legend), FadeOut(per))
        self.cue("at least the clock to q delay", FadeIn(rule[:3]))
        self.cue("plus the delay of the logic", FadeIn(rule[3:5]))
        self.cue("plus the setup time", FadeIn(rule[5:]))
        self.cue("The hold time is not in this sum", Indicate(rule, color=YELLOW, scale_factor=1.05))
        self.hold()

        freq = MathTex(r"f = \frac{1}{T} = \frac{1}{7\ \text{ns}} \approx 143\ \text{MHz}", font_size=50, color=C_CLK)
        freq.move_to([2.3, 1.85, 0])
        self.say("A clock is usually described by its frequency, which is one divided by the period.\n"
                 "A period of seven nanoseconds is one seventh of a gigahertz, or about a hundred and forty three "
                 "megahertz.")
        self.cue("one divided by the period", FadeIn(freq, shift=UP * 0.15))
        self.cue("a hundred and forty three", Circumscribe(freq, color=YELLOW))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 05 critical
    def critical(self):
        def gate_at(x, y):
            g = and_gate(h=1.0).move_to([x, y, 0])
            g.add(num(1, 36, C_LOGIC).move_to(g.get_center() + LEFT * 0.08))
            return g

        y_all = -0.2
        g1, g2 = gate_at(-2.7, 0.3 + y_all), gate_at(-0.3, 1.6 + y_all)
        g3, g4 = gate_at(-0.9, -1.5 + y_all), gate_at(2.1, -0.3 + y_all)
        reg = register_box("", w=1.0, h=1.5).move_to([4.5, -0.3 + y_all, 0])
        pin = lambda g, i: g.ins()[i]
        src = {"a": [-6.0, pin(g2, 0)[1], 0], "b": [-6.0, pin(g1, 0)[1], 0],
               "c": [-6.0, pin(g3, 0)[1], 0], "d": [-6.0, pin(g3, 1)[1], 0]}
        w = {"a": wire(src["a"], pin(g2, 0)), "b": wire(src["b"], pin(g1, 0)),
             "c": wire(src["c"], pin(g3, 0)), "d": wire(src["d"], pin(g3, 1)),
             "g1": route(g1.out(), pin(g2, 1)), "g2": route(g2.out(), pin(g4, 0)),
             "g3": route(g3.out(), pin(g4, 1)), "g4": wire(g4.out(), reg.get_left())}
        fb_y = -2.7
        w["q"] = wire(reg.get_right(), [5.9, reg.get_y(), 0], [5.9, fb_y, 0], [-4.6, fb_y, 0],
                      [-4.6, pin(g1, 1)[1], 0], pin(g1, 1))
        stubs = VGroup(*[Dot(src[k], radius=0.07, color=C_REG) for k in "abcd"])
        circ = VGroup(*w.values(), g1, g2, g3, g4, reg, stubs)
        facts = VGroup(txt("each gate 1 ns", color=C_LOGIC), txt("clock-to-q 1 ns", color=C_CQ),
                       txt("setup 1 ns", color=C_WINDOW)).arrange(RIGHT, buff=0.7).move_to([0, 3.35, 0])

        def lit(keys, color=YELLOW):
            return VGroup(*[w[k].copy().set_color(color).set_stroke(width=7) for k in keys])

        self.say("Real circuits have many routes from one register to the next. Here is one from the course notes, "
                 "with four AND gates that each take one nanosecond.\n"
                 "The register has a clock to q delay and a setup time of one nanosecond each, and the four inputs "
                 "on the left come from other registers of the same kind.",
                 FadeIn(circ))
        self.cue("four AND gates", LaggedStart(*[Indicate(g, color=C_LOGIC) for g in (g1, g2, g3, g4)],
                                               lag_ratio=0.3, run_time=1.8), FadeIn(facts[0]))
        self.cue("a clock to q delay and a setup", FadeIn(facts[1]), FadeIn(facts[2]), Indicate(reg, color=C_REG))
        self.cue("the four inputs on the left", LaggedStart(*[Flash(d, color=C_REG, flash_radius=0.3) for d in stubs],
                                                           lag_ratio=0.2, run_time=1.4))
        self.hold()

        pa, pc = lit(["a", "g2", "g4"]), lit(["c", "d", "g3", "g4"])
        two_a = num("2", 48, YELLOW).next_to(g2, UP, buff=0.2)
        two_c = num("2", 48, YELLOW).next_to(g3, DOWN, buff=0.15)
        self.say("Every route has to finish within one period, so the slowest route sets the pace. Let's time "
                 "them.\nFrom this input the signal passes two gates before it reaches the register, and from "
                 "these two it also passes two.")
        self.cue("From this input", Create(pa, run_time=1.6))
        self.cue("passes two gates", FadeIn(two_a, scale=1.4))
        self.cue("from these two", FadeOut(pa), Create(pc, run_time=1.6))
        self.cue("it also passes two", FadeIn(two_c, scale=1.4))
        self.hold()

        pq = lit(["q", "g1", "g2", "g4"], C_BAD)
        pb = lit(["b"], C_BAD)
        three = num("3", 56, C_BAD).next_to(g1, UP, buff=0.25)
        self.say("But start from this input, or from the register's own output coming back around, and the signal "
                 "passes this gate, then this one, then this one. That makes three.\n"
                 "No route goes through all four, because the lower gate sits beside that chain and not in it.",
                 FadeOut(pc), FadeOut(two_a), FadeOut(two_c))
        self.cue("start from this input", Create(pb))
        self.cue("the register's own output", Create(pq[0], run_time=1.6))
        self.cue("passes this gate", Create(pq[1]), Indicate(g1, color=C_BAD))
        self.cue("then this one,", Create(pq[2]), Indicate(g2, color=C_BAD))
        self.cue("then this one.", Create(pq[3]), Indicate(g4, color=C_BAD))
        self.cue("That makes three", FadeIn(three, scale=1.4))
        self.cue("the lower gate sits beside", Indicate(g3, color=GREY_A, scale_factor=1.15))
        self.hold()

        total = MathTex("1", "+", "3", "+", "1", "=", r"5\ \text{ns}", font_size=54)
        total[0].set_color(C_CQ), total[2].set_color(C_BAD), total[4].set_color(C_WINDOW)
        fmax = MathTex(r"f = \frac{1}{5\ \text{ns}} = 200\ \text{MHz}", font_size=54, color=C_CLK)
        res = VGroup(total, fmax).arrange(RIGHT, buff=1.2).move_to([0, 3.3, 0])
        name = txt("critical path", color=C_BAD).move_to([1.2, fb_y + 0.42, 0])
        self.say("The slowest route is called the critical path. Here it costs one nanosecond for clock to q, "
                 "three for the gates and one for setup, which is five in all.\n"
                 "So the clock can run at one fifth of a gigahertz, and that is two hundred megahertz.",
                 FadeOut(facts), FadeOut(three))
        self.cue("called the critical path", FadeIn(name, shift=UP * 0.15))
        self.cue("one nanosecond for clock to q", FadeIn(total[0]))
        self.cue("three for the gates", FadeIn(total[1:3]))
        self.cue("one for setup", FadeIn(total[3:5]))
        self.cue("five in all", FadeIn(total[5:]))
        self.cue("one fifth of a gigahertz", FadeIn(fmax, shift=LEFT * 0.2))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 06 hold
    # (named hold_scene because NarratedScene.hold() is the kit's "wait for the voice")
    def hold_scene(self):
        r1 = register_box("", w=1.1, h=1.4).move_to([-3.4, 2.1, 0])
        r2 = register_box("", w=1.1, h=1.4).move_to([2.2, 2.1, 0])
        n1 = txt("first", color=C_REG).scale(0.8).next_to(r1, UP, buff=0.1)
        n2 = txt("second", color=C_REG).scale(0.8).next_to(r2, UP, buff=0.1)
        mid = wire(r1.get_right(), r2.get_left())
        d_in = wire([-5.6, 2.1, 0], r1.get_left())
        q_out = wire(r2.get_right(), [3.5, 2.1, 0])
        clk_w = VGroup(wire([-5.6, 0.95, 0], [2.2, 0.95, 0], [2.2, 1.4, 0], color=C_CLK),
                       wire([-3.4, 0.95, 0], [-3.4, 1.4, 0], color=C_CLK))
        clk_n = txt("clock", color=C_CLK).scale(0.8).next_to(clk_w, LEFT, buff=0.15).set_y(0.95)
        circ = VGroup(r1, r2, mid, d_in, q_out, clk_w, clk_n)

        tl = Timeline(-1, 6, x_left=-3.6, width=9.4)
        h = 0.55
        y = {"clock": -0.15, "Q1": -1.05, "D2": -2.15}
        labs = VGroup(lab("clock", y["clock"], tl, h, C_CLK),
                      MathTex(r"Q_{1}", font_size=44, color=C_REG).move_to([tl.x(-1) - 0.8, y["Q1"] + h / 2, 0]),
                      MathTex(r"D_{2}", font_size=44, color=C_REG).move_to([tl.x(-1) - 0.8, y["D2"] + h / 2, 0]))
        clk = bit_trace(tl, [(-1, 0), (0, 1), (3.5, 0)], y["clock"], h, C_CLK, rise=0.2)
        edge = tl.vline(0, y["clock"] + h + 0.15, y["D2"] - 0.15)
        ruler = tl.ruler(-2.6, 1, "ns", size=26)
        win = tl.window(0, H_HOLD, y["D2"] + h + 0.1, y["D2"] - 0.1)
        win_lab = txt("hold", color=C_WINDOW).scale(0.8).next_to(win, UP, buff=0.05)
        q1 = bit_trace(tl, [(-1, 0), (H_CQ, 1)], y["Q1"], h, C_REG, rise=0.25)
        d2_fast = bit_trace(tl, [(-1, 0), (H_CQ, 1)], y["D2"], h, C_BAD, rise=0.25)
        d2_ok = bit_trace(tl, [(-1, 0), (H_CQ + 1, 1)], y["D2"], h, C_SUM, rise=0.25)

        self.say("The setup time gave us a rule that the logic must not be too slow. The hold time gives a second "
                 "rule, and it points the other way.\n"
                 "Take two registers on the same clock with almost nothing between them.",
                 FadeIn(VGroup(r1, r2, n1, n2, d_in, q_out)))
        self.cue("on the same clock", Create(clk_w), FadeIn(clk_n))
        self.cue("almost nothing between them", Create(mid), flash_along(mid, run_time=1.0))
        self.hold()

        self.say("At a rising edge the second register samples its input, and it needs that input to stay put "
                 "until its hold time is over.\n"
                 "But the same edge makes the first register change its output, one clock to q delay later. That "
                 "change sets off down the wire toward the second register.",
                 FadeIn(labs[0]), Create(clk, run_time=1.6), Create(edge), FadeIn(ruler))
        self.cue("the second register samples", Indicate(r2, color=YELLOW), FadeIn(labs[2]))
        self.cue("until its hold time is over", FadeIn(win), FadeIn(win_lab))
        self.cue("the first register change its output", Indicate(r1, color=YELLOW), FadeIn(labs[1]),
                 Create(q1, run_time=1.6, rate_func=linear))
        self.cue("sets off down the wire", flash_along(mid, color=C_BAD, run_time=1.2))
        self.hold()

        nums = VGroup(txt("hold 2 ns", color=C_WINDOW), txt("clock-to-q 1 ns", color=C_CQ),
                      txt("wire 0 ns", color=GREY_A)).scale(0.8).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        nums.move_to([5.4, 2.1, 0])
        self.say("If it gets there before the hold time is over, the second register's input moves inside the "
                 "window.\nSay the hold time is two nanoseconds, clock to q is one, and the wire takes no time. "
                 "The new value arrives at one, which is too early.")
        self.cue("Say the hold time is two", FadeIn(nums[0]))
        self.cue("clock to q is one", FadeIn(nums[1]))
        self.cue("the wire takes no time", FadeIn(nums[2]))
        self.cue("arrives at one", Create(d2_fast, run_time=1.4, rate_func=linear))
        self.cue("too early", Flash([tl.x(H_CQ), y["D2"] + h / 2, 0], color=C_BAD, flash_radius=0.5),
                 win.animate.set_fill(C_BAD, opacity=0.35))
        self.hold()

        rule = MathTex(r"t_{\text{clock-to-q}}", "+", r"t_{\text{fastest logic}}", r"\;\ge\;", r"t_{\text{hold}}",
                       font_size=46)
        rule[0].set_color(C_CQ), rule[2].set_color(C_LOGIC), rule[4].set_color(C_WINDOW)
        rule.move_to([-0.6, 3.45, 0])
        self.say("So the second rule is that clock to q plus the fastest route through the logic must be at least "
                 "the hold time.\nNotice that the clock period is not in it. Both events follow the same edge, so "
                 "slowing the clock down does not help at all.",
                 FadeOut(n1), FadeOut(n2))
        self.cue("clock to q plus the fastest", FadeIn(rule, shift=DOWN * 0.15))
        self.cue("the clock period is not in it", Indicate(rule, color=YELLOW, scale_factor=1.05))
        self.cue("Both events follow the same edge", Indicate(edge, color=YELLOW, scale_factor=1.0),
                 Indicate(q1, color=C_REG, scale_factor=1.0), Indicate(win, color=C_WINDOW, scale_factor=1.05))
        self.hold()

        dly = block("delay", w=1.7, h=0.8, size=40).move_to(mid)
        dly[0].set_fill(BG, opacity=1)
        new_wire = txt("delay 1 ns", color=C_LOGIC).scale(0.8).move_to(nums[2], aligned_edge=LEFT)
        self.say("What helps is to put some delay on the route. With one nanosecond of delay here, the new value "
                 "arrives at two, just as the window closes.\n"
                 "In practice this problem is rare, because flip-flops are usually built with a hold time no "
                 "longer than their clock to q delay. Then even a bare wire is slow enough.")
        self.cue("put some delay on the route", FadeIn(dly, scale=0.8), Transform(nums[2], new_wire))
        self.cue("arrives at two", Transform(d2_fast, d2_ok, run_time=1.4), win.animate.set_fill(C_WINDOW, opacity=0.25))
        self.cue("this problem is rare", Indicate(nums[0], color=C_WINDOW), Indicate(nums[1], color=C_CQ))
        self.cue("even a bare wire", FadeOut(dly))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 07 close
    def close(self):
        r1 = MathTex(r"T", r"\;\ge\;", r"t_{\text{clock-to-q}}", "+", r"t_{\text{slowest logic}}", "+",
                     r"t_{\text{setup}}", font_size=48)
        r1[0].set_color(C_CLK), r1[2].set_color(C_CQ), r1[4].set_color(C_LOGIC), r1[6].set_color(C_WINDOW)
        r2 = MathTex(r"t_{\text{clock-to-q}}", "+", r"t_{\text{fastest logic}}", r"\;\ge\;", r"t_{\text{hold}}",
                     font_size=48)
        r2[0].set_color(C_CQ), r2[2].set_color(C_LOGIC), r2[4].set_color(C_WINDOW)
        rules = VGroup(r1, r2).arrange(DOWN, buff=0.45).move_to([0, 2.55, 0])
        c = circuit([0, 0.35, 0], 0.72, reg=True, value="?")
        c.load_wire.set_color(C_CLK)
        c.val.set_color(YELLOW)
        self.say("So the clock period has a floor, set by the slowest route between two registers. And every route "
                 "has a floor of its own, set by the hold time.\n"
                 "With timing under control we can ask what a register in a loop is good for besides adding. Our "
                 "circuit remembered a running total. What else could a circuit choose to remember?",
                 FadeIn(r1, shift=DOWN * 0.15))
        self.cue("every route has a floor", FadeIn(r2, shift=DOWN * 0.15))
        self.cue("a register in a loop", FadeIn(VGroup(*[m for m in c.all if m is not c.val])))
        self.cue("remembered a running total", Indicate(c.box, color=C_REG, scale_factor=1.2))
        self.cue("What else", FadeIn(c.val, scale=1.5))
        self.hold(0.8)
