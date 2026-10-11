"""Episode 4: Three Ones in a Row.

A circuit that must remember: why gates alone fail, what has to be remembered
(three states), the state diagram, its truth table, and the circuit: a state
register in a loop with combinational logic, down to the gates.
Notes: Finite State Machines (all); Summary (the two-state machine).
"""
import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403
from sds_common import *  # noqa: E402,F403
from ep01_runaway_sum import flash_along, tip  # noqa: E402

STREAM = [int(ch) for ch in "0101101110111101111110"]      # the notes' input (FSM page, figure 2)
# (state, input) -> (next state, output)
NEXT = {(0, 0): (0, 0), (0, 1): (1, 0), (1, 0): (0, 0), (1, 1): (2, 0), (2, 0): (0, 0), (2, 1): (0, 1)}


def run_machine(bits):
    state, states, outs = 0, [], []
    for b in bits:
        state, out = NEXT[(state, b)]
        states.append(state)
        outs.append(out)
    return states, outs


STATES, OUTS = run_machine(STREAM)
assert "".join(map(str, OUTS)) == "0000000010001000010010"
assert [i for i, o in enumerate(OUTS) if o] == [8, 12, 17, 20]      # the third 1 of each run of three
assert STATES[:9] == [0, 1, 0, 1, 2, 0, 1, 2, 0]

# the gates, checked against the table for every row
for (ps, x), (ns, out) in NEXT.items():
    ps1, ps0 = ps >> 1, ps & 1
    assert out == (ps1 & (1 - ps0) & x)                  # OUTPUT = PS1 . not PS0 . INPUT   (notes, figure 7)
    assert (ns >> 1) == ((1 - ps1) & ps0 & x)            # NS1    = not PS1 . PS0 . INPUT   (added)
    assert (ns & 1) == ((1 - ps1) & (1 - ps0) & x)       # NS0    = not PS1 . not PS0 . INPUT (added)
assert all(ns != 3 for ns, _ in NEXT.values())           # the pattern 11 is never reached

ROWS = [(f"{ps:02b}", str(x), f"{ns:02b}", str(out)) for (ps, x), (ns, out) in NEXT.items()]
assert ROWS == [("00", "0", "00", "0"), ("00", "1", "01", "0"), ("01", "0", "00", "0"),
                ("01", "1", "10", "0"), ("10", "0", "00", "0"), ("10", "1", "00", "1")]   # the notes' table 1

# the notes' summary machine: two states, a 1 switches state and outputs 1
TOGGLE = {(0, 0): (0, 0), (0, 1): (1, 1), (1, 0): (1, 0), (1, 1): (0, 1)}
assert all(out == x and ns == (s ^ x) for (s, x), (ns, out) in TOGGLE.items())


def cells(bits, y, x_left=-5.5, w=0.5, color=C_DATA, size=36):
    """A row of boxes, one per clock period, each with its bit."""
    row = VGroup()
    for i, b in enumerate(bits):
        sq = Square(w, color=GREY_C, stroke_width=2).move_to([x_left + (i + 0.5) * w, y, 0])
        t = num(b, size, color if b else GREY_B).move_to(sq)
        row.add(VGroup(sq, t))
    return row


def arc_arrow(p, q, angle, color=GREY_A):
    a = ArcBetweenPoints(np.array(p, dtype=float), np.array(q, dtype=float), angle=angle, color=color, stroke_width=4)
    a.add_tip(tip_length=0.22, tip_width=0.2)
    return a


def fsm_diagram():
    """The three-ones machine: circles, six arrows with input/output labels. Built at full size
    around the origin; arrows and labels are keyed by (state, input)."""
    g = SimpleNamespace()
    xs, y, r = [-4.0, 0.0, 4.0], 0.6, 0.7
    g.circles = VGroup(*[state_circle(f"S{k}", r=r) for k in range(3)])
    for c, x in zip(g.circles, xs):
        c.move_to([x, y, 0])
    P = lambda k, ang: np.array([xs[k] + r * np.cos(ang), y + r * np.sin(ang), 0])
    lab = lambda s, color=GREY_A: MathTex(s, font_size=44, color=color)
    g.arrows, g.labels = {}, {}
    # the two steps forward
    for k in (0, 1):
        a = Arrow(P(k, 0), P(k + 1, PI), buff=0.05, color=GREY_A, stroke_width=4, tip_length=0.22)
        g.arrows[(k, 1)] = a
        g.labels[(k, 1)] = lab("1/0").next_to(a, UP, buff=0.1)
    # S0 stays on a 0: a self loop on its left
    loop = Arc(radius=0.42, start_angle=50 * DEGREES, angle=260 * DEGREES, color=GREY_A, stroke_width=4)
    loop.move_arc_center_to([xs[0] - r - 0.3, y, 0])
    loop.add_tip(tip_length=0.2, tip_width=0.18)
    g.arrows[(0, 0)] = loop
    g.labels[(0, 0)] = lab("0/0").next_to(loop, LEFT, buff=0.12)
    # S1 back to S0 on a 0, under the forward arrow
    g.arrows[(1, 0)] = arc_arrow(P(1, -140 * DEGREES), P(0, -40 * DEGREES), -TAU / 5)
    g.labels[(1, 0)] = lab("0/0").next_to(g.arrows[(1, 0)], DOWN, buff=0.08)
    # S2 back to S0: on a 1 over the top (the only output 1), on a 0 underneath
    g.arrows[(2, 1)] = arc_arrow(P(2, 110 * DEGREES), P(0, 70 * DEGREES), TAU / 4, color=YELLOW)
    g.labels[(2, 1)] = lab("1/1", YELLOW).next_to(g.arrows[(2, 1)], UP, buff=0.08)
    g.arrows[(2, 0)] = arc_arrow(P(2, -110 * DEGREES), P(0, -70 * DEGREES), -TAU / 4)
    g.labels[(2, 0)] = lab("0/0").next_to(g.arrows[(2, 0)], DOWN, buff=0.08)
    g.all = VGroup(g.circles, *g.arrows.values(), *g.labels.values())
    return g


def truth_table(x0, y_top, dx=1.45, dy=0.6, size=40):
    """Header and six rows; `rows[i]` is a VGroup of that row's four entries."""
    heads = ["PS", "IN", "NS", "OUT"]
    head = VGroup(*[txt(s, color=GREY_A).scale(0.8).move_to([x0 + j * dx, y_top, 0]) for j, s in enumerate(heads)])
    rule = Line([x0 - 0.6, y_top - 0.33, 0], [x0 + 3 * dx + 0.6, y_top - 0.33, 0], color=GREY_C, stroke_width=2)
    split = Line([x0 + 1.5 * dx, y_top + 0.3, 0], [x0 + 1.5 * dx, y_top - 0.5 - 6 * dy + 0.2, 0], color=GREY_C,
                 stroke_width=2)
    rows = VGroup()
    for i, r in enumerate(ROWS):
        rows.add(VGroup(*[num(v, size, C_REG if j in (0, 2) else (YELLOW if (j == 3 and v == "1") else C_DATA))
                          .move_to([x0 + j * dx, y_top - 0.72 - i * dy, 0]) for j, v in enumerate(r)]))
    return VGroup(head, rule, split), rows


def loop_circuit():
    """A state register in a loop with a block of logic (the shape of episode 1's accumulator)."""
    g = SimpleNamespace()
    g.cl = block("logic", w=2.8, h=1.9)
    g.cl.move_to([0, 1.0, 0])
    g.reg = register_box("", w=1.3, h=1.2).move_to([0, -1.5, 0])
    g.inp = VGroup(wire([-4.6, 1.45, 0], [-1.4, 1.45, 0]), tip([-1.4, 1.45, 0], RIGHT))
    g.out = VGroup(wire([1.4, 1.45, 0], [4.6, 1.45, 0]), tip([4.6, 1.45, 0], RIGHT))
    g.ns = VGroup(wire([1.4, 0.55, 0], [3.0, 0.55, 0], [3.0, -1.5, 0], [0.65, -1.5, 0]), tip([0.65, -1.5, 0], LEFT))
    g.ps = VGroup(wire([-0.65, -1.5, 0], [-3.0, -1.5, 0], [-3.0, 0.55, 0], [-1.4, 0.55, 0]),
                  tip([-1.4, 0.55, 0], RIGHT))
    g.clk = wire([0, -2.1, 0], [0, -2.7, 0], color=C_CLK)
    g.inp_l = txt("input", color=C_DATA).next_to(g.inp, UP, buff=0.12).set_x(-3.6)
    g.out_l = txt("output", color=YELLOW).next_to(g.out, UP, buff=0.12).set_x(3.7)
    g.ns_l = txt("next state", color=C_REG).next_to([3.0, -0.5, 0], RIGHT, buff=0.2)
    g.ps_l = txt("present state", color=C_REG).next_to([-3.0, -0.5, 0], LEFT, buff=0.2)
    g.clk_l = txt("clock", color=C_CLK).scale(0.8).next_to(g.clk, RIGHT, buff=0.15)
    g.all = VGroup(g.cl, g.reg, g.inp, g.out, g.ns, g.ps, g.clk, g.inp_l, g.out_l, g.ns_l, g.ps_l, g.clk_l)
    return g


def and3(y, inverted, out_name, x=2.6):
    """A three-input AND gate fed by PS1, PS0 and IN, with a bubble on each inverted input."""
    g = and_gate(h=1.7).move_to([x, y, 0])
    names = [r"PS_1", r"PS_0", r"IN"]
    parts = VGroup(g)
    for i, (pin, name) in enumerate(zip(g.ins(3), names)):
        start = pin + LEFT * 1.3
        if i in inverted:
            bub = Circle(radius=0.09, color=C_LOGIC, stroke_width=3).move_to(pin + LEFT * 0.09)
            parts.add(wire(start, pin + LEFT * 0.18), bub)
        else:
            parts.add(wire(start, pin))
        parts.add(MathTex(name, font_size=34, color=C_REG if i < 2 else C_DATA).next_to(start, LEFT, buff=0.12))
    o = g.out()
    parts.add(wire(o, o + RIGHT * 0.9))
    parts.add(MathTex(out_name, font_size=40, color=YELLOW if out_name == "OUT" else C_REG)
              .next_to(o + RIGHT * 0.9, RIGHT, buff=0.12))
    return parts


class Ep04ThreeOnes(NarratedScene):
    SCENES = ["hook", "memory", "states", "run", "table", "circuit", "gates", "other", "close"]

    def construct(self):
        if self.preview_only(["states", "run"]):
            return
        self.title_card()
        for s in self.SCENES:
            getattr(self, s)()
        self.end_card([
            "Logic without memory gives the same output whenever the input is the same.",
            "A finite state machine has states, and arrows labelled with an input and an output.",
            "Number the states, and every arrow becomes a row of a truth table.",
            "Any state machine is a register for the state, in a loop with logic for the table.",
        ])

    # ------------------------------------------------------------------ 01 hook
    def rows(self, filled=False):
        inp = cells(STREAM, 1.0)
        out = cells(OUTS, -0.4, color=YELLOW)
        for c in out:
            if not filled:
                c[1].set_opacity(0)
        labs = VGroup(txt("input", color=C_DATA).scale(0.85).next_to(inp, UP, buff=0.2, aligned_edge=LEFT),
                      txt("output", color=YELLOW).scale(0.85).next_to(out, DOWN, buff=0.2, aligned_edge=LEFT))
        return inp, out, labs

    def hook(self):
        inp, out, labs = self.rows()
        show = lambda ks: [out[k][1].animate.set_opacity(1) for k in ks]
        mark = lambda a, b: SurroundingRectangle(VGroup(*inp[a:b + 1]), color=YELLOW, buff=0.06)
        self.say("Here is a wire that brings one bit in each clock period. We want a circuit that watches it and "
                 "raises its output for one period whenever it has just seen three ones in a row.\n"
                 "After that it starts counting again from nothing.",
                 FadeIn(labs[0]), LaggedStart(*[FadeIn(c, shift=LEFT * 0.2) for c in inp], lag_ratio=0.08,
                                              run_time=3.0))
        self.cue("raises its output", FadeIn(labs[1]), FadeIn(VGroup(*[c[0] for c in out])))
        self.hold()

        m1, m2 = mark(1, 1), mark(3, 4)
        m3 = mark(6, 8)
        self.say("Let's see what that means on a stream. A single one, and then two ones, give us nothing.\n"
                 "Then come three ones, and on the third the output goes high.")
        self.cue("A single one", Create(m1), *show([0, 1, 2]))
        self.cue("then two ones", ReplacementTransform(m1, m2), *show([3, 4, 5]))
        self.cue("Then come three ones", ReplacementTransform(m2, m3), *show([6, 7]))
        self.cue("on the third", *show([8]), Flash(out[8], color=YELLOW, flash_radius=0.45))
        self.hold()

        m4, m5 = mark(10, 13), mark(15, 20)
        self.say("With four ones in a row we still get a single pulse, on the third, and the fourth is a fresh "
                 "start.\nSix in a row give two pulses.",
                 ReplacementTransform(m3, m4), *show([9, 10, 11]))
        self.cue("a single pulse", *show([12]), Flash(out[12], color=YELLOW, flash_radius=0.45))
        self.cue("the fourth is a fresh start", *show([13, 14]), Indicate(inp[13], color=YELLOW))
        self.cue("Six in a row", ReplacementTransform(m4, m5), *show([15, 16, 18, 19, 21]))
        self.cue("two pulses", *show([17, 20]), Flash(out[17], color=YELLOW, flash_radius=0.45),
                 Flash(out[20], color=YELLOW, flash_radius=0.45))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 02 memory
    def memory(self):
        inp, out, labs = self.rows(filled=True)
        col = lambda k, color: SurroundingRectangle(VGroup(inp[k], out[k]), color=color, buff=0.07, stroke_width=5)
        a, b = col(6, C_BAD), col(8, YELLOW)
        assert STREAM[6] == STREAM[8] == 1 and OUTS[6] == 0 and OUTS[8] == 1
        self.say("Can logic gates alone do this? Look at these two moments. In both the input is a one, but at the "
                 "first the output must be zero and at the second it must be one.\n"
                 "Gates without memory give the same output for the same input, so the answer is no.",
                 FadeIn(inp), FadeIn(out), FadeIn(labs))
        self.cue("these two moments", Create(a), Create(b))
        self.zoom_to(VGroup(a, b), width=6.0)
        self.cue("at the first the output must be zero", Indicate(out[6], color=C_BAD, scale_factor=1.4))
        self.cue("at the second it must be one", Indicate(out[8], color=YELLOW, scale_factor=1.4))
        self.hold(0.3)
        self.zoom_back()

        tally = VGroup(*[txt(s, color=C_REG) for s in ("none", "one", "two")]).arrange(RIGHT, buff=1.6)
        tally.move_to([0, -2.3, 0])
        ask = txt("how many 1s in a row so far?", color=GREY_A).next_to(tally, UP, buff=0.3)
        back = arc_arrow(tally[2].get_bottom() + DOWN * 0.08, tally[0].get_bottom() + DOWN * 0.08, -TAU / 6, YELLOW)
        self.say("The circuit has to remember something about the past, but not the whole history. Ask what it "
                 "must know in order to deal with the next bit.\n"
                 "All it needs is how many ones in a row it has just seen, and that is none, one or two. On the "
                 "third it fires and goes back to none.",
                 FadeOut(a), FadeOut(b))
        self.cue("how many ones in a row", FadeIn(ask, shift=UP * 0.15))
        self.cue("none, one or two", LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in tally], lag_ratio=0.5,
                                                  run_time=1.6))
        self.cue("goes back to none", Create(back))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 03 states
    def states(self):
        g = self.g = fsm_diagram()
        means = VGroup(*[txt(s, color=GREY_A).scale(0.8).next_to(c, DOWN, buff=0.18)
                         for s, c in zip(("no ones yet", "one so far", "two so far"), g.circles)])
        A, L = g.arrows, g.labels
        self.say("Give those three situations names. S zero means no ones yet, S one means one so far, and S two "
                 "means two so far.\n"
                 "We draw each as a circle and call it a state. At any moment the machine is in exactly one of "
                 "them.")
        for k, phrase in enumerate(("S zero means", "S one means", "S two means")):
            self.cue(phrase, FadeIn(g.circles[k], scale=0.8), FadeIn(means[k], shift=UP * 0.15))
        self.cue("call it a state", LaggedStart(*[Indicate(c, color=C_REG) for c in g.circles], lag_ratio=0.3,
                                                run_time=1.6))
        self.hold()

        what = txt("input / output", color=YELLOW).scale(0.8).next_to(L[(0, 1)], UP, buff=0.25)
        self.say("Now go through them and ask what each bit does. In S zero a one arrives, which makes one in a "
                 "row, so we move to S one and the output stays zero.\n"
                 "We draw that as an arrow, labelled with the input, a slash, and the output. If a zero arrives "
                 "instead we stay where we are, and that is an arrow from the state back to itself, called a self "
                 "loop.",
                 Indicate(g.circles[0], color=YELLOW))
        self.cue("we move to S one", GrowArrow(A[(0, 1)]))
        self.cue("labelled with the input", FadeIn(L[(0, 1)]), FadeIn(what, shift=DOWN * 0.1))
        self.cue("If a zero arrives instead", FadeOut(what), Create(A[(0, 0)]), FadeIn(L[(0, 0)]))
        self.cue("called a self loop", Indicate(A[(0, 0)], color=YELLOW))
        self.hold()

        self.say("In S one, another one takes us to S two, still with output zero. A zero breaks the run, so we go "
                 "back to S zero.",
                 Indicate(g.circles[1], color=YELLOW))
        self.cue("takes us to S two", GrowArrow(A[(1, 1)]), FadeIn(L[(1, 1)]))
        self.cue("A zero breaks the run", Create(A[(1, 0)]), FadeIn(L[(1, 0)]))
        self.hold()

        self.say("In S two, a one is the third in a row. This is the arrow that carries an output of one, and it "
                 "leads back to S zero to start over.\n"
                 "A zero from S two also leads back to S zero, with output zero.",
                 Indicate(g.circles[2], color=YELLOW), FadeOut(means))
        self.cue("This is the arrow", Create(A[(2, 1)], run_time=1.6))
        self.cue("an output of one", FadeIn(L[(2, 1)], scale=1.4))
        self.cue("A zero from S two", Create(A[(2, 0)], run_time=1.6), FadeIn(L[(2, 0)]))
        self.hold()

        name = txt("a finite state machine", color=YELLOW).move_to([4.6, -2.5, 0])
        self.say("That makes six arrows, two out of every state, so the machine always knows what to do.\n"
                 "A picture like this is called a finite state machine. It has inputs, outputs, a fixed set of "
                 "states, and arrows that say where each input leads and what to output on the way.",
                 LaggedStart(*[Indicate(a, scale_factor=1.05) for a in A.values()], lag_ratio=0.15, run_time=2.4))
        self.cue("called a finite state machine", FadeIn(name, shift=UP * 0.15))
        self.cue("a fixed set of states", LaggedStart(*[Indicate(c, color=C_REG) for c in g.circles], lag_ratio=0.2,
                                                      run_time=1.4))
        self.cue("arrows that say where", LaggedStart(*[Indicate(l, color=YELLOW) for l in L.values()],
                                                      lag_ratio=0.15, run_time=1.8))
        self.hold()
        self.fsm_name = name

    # ------------------------------------------------------------------ 04 run
    def run(self):
        g = self.g
        inp = cells(STREAM, -2.1, w=0.48, size=32)
        out = cells(OUTS, -2.62, w=0.48, color=YELLOW, size=32)
        for c in out:
            c[1].set_opacity(0)
        ring = Circle(radius=0.82, color=YELLOW, stroke_width=6).move_to(g.circles[0])
        self.ring_k = 0

        def step(i, rt=0.7):
            """Feed bit i: light its cell, follow its arrow, write its output."""
            s_from = 0 if i == 0 else STATES[i - 1]
            arrow = g.arrows[(s_from, STREAM[i])]
            anims = [inp[i][0].animate.set_stroke(YELLOW, width=5), out[i][1].animate.set_opacity(1),
                     flash_along(arrow, run_time=rt)]
            if i > 0:
                anims.append(inp[i - 1][0].animate.set_stroke(GREY_C, width=2))
            anims.append(ring.animate.move_to(g.circles[STATES[i]]))
            return anims

        self.say("Let's run the stream through it. A zero, and we stay. A one takes us to S one, and the next zero "
                 "sends us back.\nThen one and one bring us to S two, but a zero sends us home again.",
                 FadeOut(self.fsm_name), g.all.animate.shift(UP * 0.5), FadeIn(inp), FadeIn(VGroup(*[c[0] for c in out])))
        ring.shift(UP * 0.5)
        self.play(Create(ring), run_time=0.6)
        self.cue("A zero, and we stay", *step(0))
        self.cue("A one takes us", *step(1))
        self.cue("the next zero sends us back", *step(2))
        self.cue("Then one and one", *step(3), run_time=0.6)
        self.play(*step(4), run_time=0.6)
        self.cue("a zero sends us home", *step(5))
        self.hold()

        self.say("Now one, one, and one more. On that last arrow the output is one, and we are back in S zero, "
                 "ready for the next run.",
                 *step(6))
        self.cue("one, and one more", *step(7))
        self.cue("On that last arrow", *step(8), Flash(out[8], color=YELLOW, flash_radius=0.4))
        self.hold()
        for i in range(9, len(STREAM)):                 # the rest of the stream, without words
            self.play(*step(i, rt=0.4), run_time=0.4)
            if OUTS[i]:
                self.play(Flash(out[i], color=YELLOW, flash_radius=0.4), run_time=0.4)
        self.wait(0.8)
        self.clear_stage()

    # ------------------------------------------------------------------ 05 table
    def table(self):
        g = fsm_diagram()
        g.all.scale(0.6, about_point=ORIGIN).shift([-3.0, 0.6, 0])
        codes = VGroup(*[num(f"{k:02b}", 44, C_REG).next_to(c, DOWN, buff=0.15) for k, c in enumerate(g.circles)])
        frame, rows = truth_table(2.3, 2.7, dx=1.3)
        order = list(NEXT.keys())
        self.say("To build this, the states have to become bits. Three states fit in two bits, so let S zero be "
                 "zero zero, S one be zero one, and S two be one zero.\n"
                 "Then every arrow becomes a row of a table. On the left go the present state and the input, and "
                 "on the right the next state and the output.",
                 FadeIn(g.all))
        for k, phrase in enumerate(("S zero be zero zero", "S one be zero one", "S two be one zero")):
            self.cue(phrase, FadeIn(codes[k], shift=UP * 0.15))
        self.cue("every arrow becomes a row", FadeIn(frame[1]), FadeIn(frame[2]))
        self.cue("On the left go", FadeIn(frame[0][0]), FadeIn(frame[0][1]))
        self.cue("on the right the next state", FadeIn(frame[0][2]), FadeIn(frame[0][3]))
        self.hold()

        i = order.index((1, 1))
        lit = g.arrows[(1, 1)].copy().set_color(YELLOW).set_stroke(width=8)
        self.say("Take the arrow from S one on a one. Its row reads present state zero one, input one, next state "
                 "one zero, output zero.\nSix arrows give six rows. The pattern one one never appears, because no "
                 "arrow leads to it.",
                 FadeIn(lit))
        self.cue("present state zero one", FadeIn(rows[i][0]))
        self.cue("input one", FadeIn(rows[i][1]))
        self.cue("next state one zero", FadeIn(rows[i][2]))
        self.cue("output zero", FadeIn(rows[i][3]))
        rest = [k for k in range(6) if k != i]
        self.cue("Six arrows give six rows", FadeOut(lit),
                 LaggedStart(*[AnimationGroup(FadeIn(rows[k]), Indicate(g.arrows[order[k]], color=YELLOW,
                                                                        scale_factor=1.05))
                               for k in rest], lag_ratio=0.35, run_time=3.0))
        unused = VGroup(num("11", 40, GREY_B), txt("never used", color=GREY_B).scale(0.8)).arrange(RIGHT, buff=0.3)
        unused.next_to(rows, DOWN, buff=0.35)
        self.cue("The pattern one one", FadeIn(unused, shift=UP * 0.15))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 06 circuit
    def circuit(self):
        self.camera.frame.set(width=11.8).move_to([0, -0.4, 0])
        g = loop_circuit()
        mini_frame, mini_rows = truth_table(0, 0, dx=1.45, dy=0.6)
        mini = VGroup(mini_frame, mini_rows).scale(0.3).move_to(g.cl).shift(DOWN * 0.15)
        g.cl[1].scale(0.8).shift(UP * 0.62)
        bits = txt("2 bits", color=C_REG).scale(0.8).next_to(g.reg, DOWN, buff=0.12).shift(LEFT * 1.3)
        self.say("Look at what this table is. Its left side decides its right side with no memory involved, so it "
                 "is a job for plain logic gates.\n"
                 "The only thing that has to be remembered is the present state, which is two bits, and we know "
                 "what remembers bits.",
                 FadeIn(mini))
        self.cue("a job for plain logic gates", FadeIn(g.cl, scale=1.1))
        self.cue("the present state, which is two bits", FadeIn(bits, shift=UP * 0.15))
        self.cue("what remembers bits", FadeIn(g.reg, scale=0.8))
        self.hold()

        self.say("So the circuit is a register for two bits and a block of logic. The register's output is the "
                 "present state.\n"
                 "The logic takes that and the input bit and produces the output and the next state. And the next "
                 "state goes around to the register's input, where it waits for the clock.",
                 Indicate(g.reg, color=C_REG), Indicate(g.cl, color=C_LOGIC))
        self.cue("The register's output is", Create(g.ps, run_time=1.4), FadeIn(g.ps_l))
        self.cue("and the input bit", Create(g.inp), FadeIn(g.inp_l))
        self.cue("produces the output", Create(g.out), FadeIn(g.out_l))
        self.cue("the next state goes around", Create(g.ns, run_time=1.4), FadeIn(g.ns_l))
        self.cue("waits for the clock", Create(g.clk), FadeIn(g.clk_l), FadeOut(bits))
        self.hold()

        plus = txt("+", size=64, color=C_LOGIC).move_to(g.cl)
        self.say("At each rising edge the next state becomes the present state, and the logic starts on the "
                 "following bit.\nThis is the same loop as our running sum, with the adder swapped for a table.",
                 flash_along(g.clk, run_time=0.8), flash_along(g.ns[0], color=C_REG, run_time=1.2))
        self.cue("the logic starts on", flash_along(g.ps[0], color=C_REG, run_time=1.2),
                 flash_along(g.cl[0], run_time=1.2))
        self.cue("the same loop as our running sum", FadeOut(mini), FadeOut(g.cl[1]), FadeIn(plus, scale=1.3))
        self.cue("swapped for a table", FadeOut(plus), FadeIn(mini), FadeIn(g.cl[1]))
        self.hold()
        self.clear_stage()
        self.camera.frame.set(width=FRAME_W).move_to(ORIGIN)

    # ------------------------------------------------------------------ 07 gates
    def gates(self):
        frame, rows = truth_table(-5.9, 2.4, dx=1.25)
        g_out, g_ns1, g_ns0 = and3(2.3, {1}, "OUT"), and3(0.2, {0}, r"NS_1"), and3(-1.9, {0, 1}, r"NS_0")
        box = lambda i, color: SurroundingRectangle(rows[i], color=color, buff=0.1, stroke_width=4)
        b_out = box(5, YELLOW)
        self.say("What is inside the logic block? We can read it off the table. The output is one in a single "
                 "row, where the present state is one zero and the input is one.\n"
                 "So the output is the high state bit, and not the low state bit, and the input.",
                 FadeIn(frame), FadeIn(rows))
        self.cue("one in a single row", Create(b_out))
        self.cue("the high state bit", FadeIn(g_out[0]), FadeIn(g_out[1:3]))
        self.cue("not the low state bit", FadeIn(g_out[3:6]))
        self.cue("and the input.", FadeIn(g_out[6:]))
        self.hold()

        b1, b0 = box(3, C_REG), box(1, C_REG)
        self.say("The next state works the same way. Its high bit is one only in the row with state zero one and "
                 "input one, and its low bit only in the row with state zero zero and input one.\n"
                 "That is three AND gates and a few inverters, and the machine is complete.",
                 b_out.animate.set_stroke(opacity=0.4))
        self.cue("Its high bit is one only", Create(b1), FadeIn(g_ns1, shift=LEFT * 0.2))
        self.cue("its low bit only", Create(b0), FadeIn(g_ns0, shift=LEFT * 0.2))
        self.cue("three AND gates", LaggedStart(*[Indicate(x[0], color=C_LOGIC) for x in (g_out, g_ns1, g_ns0)],
                                                lag_ratio=0.3, run_time=1.6))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 08 other
    def other(self):
        r = 0.7
        a = state_circle("0", r=r).move_to([-2.4, 0.8, 0])
        b = state_circle("1", r=r).move_to([2.4, 0.8, 0])
        P = lambda c, ang: c.get_center() + r * np.array([np.cos(ang), np.sin(ang), 0])
        lab = lambda s, color=GREY_A: MathTex(s, font_size=44, color=color)
        ab = arc_arrow(P(a, 40 * DEGREES), P(b, 140 * DEGREES), -TAU / 6, YELLOW)
        ba = arc_arrow(P(b, -140 * DEGREES), P(a, -40 * DEGREES), -TAU / 6, YELLOW)
        loops = VGroup()
        for c, side in ((a, -1), (b, 1)):
            lp = Arc(radius=0.42, start_angle=(50 if side < 0 else 230) * DEGREES, angle=260 * DEGREES, color=GREY_A,
                     stroke_width=4)
            lp.move_arc_center_to(c.get_center() + side * RIGHT * (r + 0.3))
            lp.add_tip(tip_length=0.2, tip_width=0.18)
            loops.add(VGroup(lp, lab("0/0").next_to(lp, LEFT if side < 0 else RIGHT, buff=0.12)))
        l_ab, l_ba = lab("1/1", YELLOW).next_to(ab, UP, buff=0.08), lab("1/1", YELLOW).next_to(ba, DOWN, buff=0.08)
        recipe = txt("1 flip-flop + a little logic", color=C_REG).move_to([0, -2.2, 0])
        self.say("The same recipe works for any diagram. Here is a smaller one with two states. On a zero it stays "
                 "where it is and outputs zero, and on a one it switches to the other state and outputs one.\n"
                 "One flip-flop holds the state, and a little logic does the rest.",
                 FadeIn(a, scale=0.8), FadeIn(b, scale=0.8))
        self.cue("On a zero it stays", FadeIn(loops))
        self.cue("on a one it switches", Create(ab), Create(ba), FadeIn(l_ab), FadeIn(l_ba))
        self.cue("One flip-flop holds the state", FadeIn(recipe, shift=UP * 0.15))
        self.hold()

        names = ["check", "fetch", "store"]
        cs = VGroup(*[state_circle(n, r=0.95, size=36) for n in names])
        for c, x in zip(cs, (-4.0, 0.0, 4.0)):
            c.move_to([x, 0.8, 0])
        arrows = VGroup(Arrow(cs[0].get_right(), cs[1].get_left(), buff=0.08, color=GREY_A, stroke_width=4),
                        Arrow(cs[1].get_right(), cs[2].get_left(), buff=0.08, color=GREY_A, stroke_width=4),
                        arc_arrow(cs[2].get_bottom() + DOWN * 0.05, cs[0].get_bottom() + DOWN * 0.05, -TAU / 5))
        title = txt("a cache controller", color=YELLOW).move_to([0, 2.9, 0])
        self.say("Real processors are full of machines like this. The controller of a cache, for instance, steps "
                 "through states as it serves a request, first checking, then fetching from memory, then "
                 "storing.\nAny step by step procedure with a fixed number of situations can be built from a "
                 "register and logic.",
                 *[FadeOut(m) for m in (a, b, ab, ba, loops, l_ab, l_ba)], recipe.animate.set_opacity(0))
        self.cue("The controller of a cache", FadeIn(title, shift=DOWN * 0.15))
        self.cue("first checking", FadeIn(cs[0], scale=0.8))
        self.cue("then fetching", GrowArrow(arrows[0]), FadeIn(cs[1], scale=0.8))
        self.cue("then storing", GrowArrow(arrows[1]), FadeIn(cs[2], scale=0.8), Create(arrows[2]))
        reg_l = txt("a register + logic", color=C_REG).move_to([0, -2.3, 0])
        self.cue("built from a register and logic", FadeIn(reg_l, shift=UP * 0.15))
        self.hold()
        self.clear_stage()

    # ------------------------------------------------------------------ 09 close
    def close(self):
        self.camera.frame.set(width=12.6).move_to([0.6, -0.4, 0])
        g = loop_circuit()
        q = txt("?", size=64, color=YELLOW).move_to([4.9, -1.5, 0])
        extra = register_box("", w=1.0, h=1.2).move_to([4.9, -1.5, 0]).set_opacity(0.5)
        self.say("So a register in a loop can remember anything we can number, and the logic decides how that "
                 "memory changes.\n"
                 "There is one more use for a register, and it has nothing to do with remembering. Sometimes we "
                 "add one just to make the clock faster.",
                 FadeIn(g.all))
        self.cue("remember anything we can number", Indicate(g.reg, color=C_REG, scale_factor=1.2))
        self.cue("the logic decides", Indicate(g.cl, color=C_LOGIC, scale_factor=1.1))
        self.cue("one more use for a register", g.all.animate.set_opacity(0.3), FadeIn(extra))
        self.cue("make the clock faster", FadeIn(q, scale=1.4))
        self.hold(0.8)
