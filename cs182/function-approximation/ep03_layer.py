"""Episode 3 — From Ramps to a Layer (Note 1, section 1.3)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers

# one unit
W_U, B_U = 2.0, -1.0
UNIT_TRACE = {}
for xv in (1.5, 0.2):
    wx_, z_ = W_U * xv, W_U * xv + B_U
    UNIT_TRACE[xv] = (wx_, z_, float(relu(z_)))
assert UNIT_TRACE[1.5] == (3.0, 2.0, 2.0)
assert UNIT_TRACE[0.2][2] == 0.0 and abs(UNIT_TRACE[0.2][1] + 0.6) < 1e-12

# a layer with d = 4 hidden units
W1 = np.array([[1.0], [-1.0], [2.0], [0.5]])
B1 = np.array([0.0, 1.0, -1.0, -0.5])
W2 = np.array([[1.0, -1.0, 0.5, 2.0]])
B2 = 0.5
D = 4


def forward(x):
    z = W1[:, 0] * x + B1
    h = relu(z)
    return z, h, float(W2[0] @ h + B2)


X0 = 1.5
Z0, H0, N0 = forward(X0)
assert np.allclose(Z0, [1.5, -0.5, 2.0, 0.25]) and np.allclose(H0, [1.5, 0.0, 2.0, 0.25]) and N0 == 3.5
assert N0 == sum(W2[0, i] * H0[i] for i in range(D)) + B2
MACS = D + D          # multiply-accumulates: d in the first layer (1 input each), d in the readout
ELBOWS = -B1 / W1[:, 0]
assert np.allclose(ELBOWS, [0.0, 1.0, 0.5, 1.0])

# collapse without ReLU
A_LIN = float((W2 @ W1)[0, 0])            # slope
C_LIN = float(W2[0] @ B1 + B2)     # intercept
assert (A_LIN, C_LIN) == (4.0, -2.0)
XS = np.linspace(-1, 3, 401)
lin = lambda x: A_LIN * np.asarray(x) + C_LIN
nonlin = lambda x: np.array([forward(v)[2] for v in np.atleast_1d(x)])
assert np.allclose(lin(X0), 4.0)
assert not np.allclose(nonlin(XS), lin(XS))
assert abs(nonlin(np.array([X0]))[0] - N0) < 1e-12


def f1(v):
    return f"{v:.1f}"


class Ep03Layer(NarratedScene):
    series = SERIES
    SCENES = ["one_unit", "parallel_units", "matrix_form", "collapse"]

    def construct(self):
        self.title_card()
        self.one_unit()
        self.parallel_units()
        self.matrix_form()
        self.collapse()
        self.end_card(
            ["One unit is three cheap steps: multiply, add a bias, clip at zero",
             "A layer runs many units at once: h = ReLU(W₁x + b₁)",
             "The readout just adds them up: N(x) = W₂h + b₂",
             "Take out the ReLUs and any stack of layers collapses into one line"],
        )

    # ---------------------------------------------------------------- 1. one unit
    def one_unit(self):
        head = self.heading("One unit as a computation graph")
        names = [("× w", BLUE_C), ("+ b", BLUE_C), ("max(0, ·)", C_RAMP)]
        boxes = VGroup(*[box_label(n, c, w=2.1, h=0.9, font_size=28) for n, c in names]).arrange(RIGHT, buff=1.3).move_to([0.6, 0.6, 0])
        xin = txt("x", 34, WHITE).next_to(boxes[0], LEFT, buff=1.2)
        hout = txt("h", 34, C_RAMP).next_to(boxes[2], RIGHT, buff=1.2)
        arrows = VGroup(Arrow(xin.get_right(), boxes[0].get_left(), buff=0.1, color=GREY_B),
                        Arrow(boxes[0].get_right(), boxes[1].get_left(), buff=0.1, color=GREY_B),
                        Arrow(boxes[1].get_right(), boxes[2].get_left(), buff=0.1, color=GREY_B),
                        Arrow(boxes[2].get_right(), hout.get_left(), buff=0.1, color=GREY_B))
        params = VGroup(mt(rf"w={fmt_num(W_U)}", 0.8, C_MODEL).next_to(boxes[0], UP, buff=0.3),
                        mt(rf"b={fmt_num(B_U)}", 0.8, C_MODEL).next_to(boxes[1], UP, buff=0.3))
        self.say("To see what one ramp actually computes, let's draw it as a little pipeline. The input is "
                 "scaled by its weight, then a bias is added, and then we take the max with zero.",
                 Write(head), FadeIn(xin), *[FadeIn(b) for b in boxes], *[Create(a) for a in arrows], FadeIn(hout), FadeIn(params))
        self.cue("scaled by its weight", Indicate(boxes[0], color=BLUE_C))
        self.cue("then a bias is added", Indicate(boxes[1], color=BLUE_C))
        self.cue("we take the max", Indicate(boxes[2], color=C_RAMP))
        self.hold(0.3)

        def tokens(xv, col):
            wx_, z_, h_ = UNIT_TRACE[xv]
            vals = [xv, wx_, z_, h_]
            pos = [xin.get_center() + DOWN * 0.9, arrows[1].get_center() + DOWN * 0.75,
                   arrows[2].get_center() + DOWN * 0.75, hout.get_center() + DOWN * 0.9]
            return [txt(f"{v:g}", 32, col).move_to(p) for v, p in zip(vals, pos)]

        assert (W_U, B_U) == (2.0, -1.0) and abs(UNIT_TRACE[0.2][0] - 0.4) < 1e-12      # spoken below
        toks = tokens(1.5, YELLOW_D)
        self.say("Feed in one point five. Doubling it gives three, and subtracting one leaves two. That's "
                 "positive, so it passes straight through, and the output is two.",
                 FadeIn(toks[0], shift=RIGHT * 0.2))
        self.cue("Doubling it gives three", FadeIn(toks[1], shift=RIGHT * 0.2))
        self.cue("subtracting one leaves two", FadeIn(toks[2], shift=RIGHT * 0.2))
        self.cue("the output is two", FadeIn(toks[3], shift=RIGHT * 0.2))
        self.hold(0.4)
        self.play(*[FadeOut(t) for t in toks], run_time=0.4)
        toks = tokens(0.2, ORANGE)
        self.say("Now try a smaller input, zero point two. Doubling it gives zero point four, and subtracting "
                 "one leaves minus zero point six. That's negative, so the max with zero wipes it out, and the "
                 "output is zero.",
                 FadeIn(toks[0], shift=RIGHT * 0.2))
        self.cue("Doubling it gives zero point four", FadeIn(toks[1], shift=RIGHT * 0.2))
        self.cue("leaves minus zero point six", FadeIn(toks[2], shift=RIGHT * 0.2))
        self.cue("the output is zero", FadeIn(toks[3], shift=RIGHT * 0.2))
        self.hold(0.4)
        self.play(*[FadeOut(t) for t in toks], run_time=0.4)
        self.say("So one unit is three cheap operations, and only the last one bends anything. That matters in "
                 "practice, because hardware built for multiplying and adding can run huge numbers of these "
                 "at once.",
                 Indicate(boxes[2], color=C_RAMP))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 2. parallel units
    def parallel_units(self):
        head = self.heading("d units in parallel")
        ys = [1.95, 0.8, -0.35, -1.5]
        inp = Circle(0.38, color=WHITE, stroke_width=3).move_to([-5.0, 0.225, 0])
        inp_t = txt("x", 28, WHITE).move_to(inp)
        hid = VGroup(*[Circle(0.36, color=C_RAMP, fill_opacity=0.15, stroke_width=3).move_to([-1.4, y, 0]) for y in ys])
        hid_t = VGroup(*[txt(f"h{i + 1}", 24, C_RAMP).move_to(hid[i]) for i in range(D)])
        out = Circle(0.42, color=C_MODEL, fill_opacity=0.15, stroke_width=3).move_to([2.6, 0.225, 0])
        out_t = txt("N", 28, C_MODEL).move_to(out)
        e1 = VGroup(*[Line(inp.get_right(), hid[i].get_left(), color=GREY_B, stroke_width=2) for i in range(D)])
        e2 = VGroup(*[Line(hid[i].get_right(), out.get_left(), color=GREY_B, stroke_width=2) for i in range(D)])
        w1l = VGroup(*[txt(f1(W1[i, 0]), 20, C_MODEL).move_to(e1[i].point_from_proportion(0.58)).shift(UP * 0.17 if i < 2 else DOWN * 0.17) for i in range(D)])
        w2l = VGroup(*[txt(f1(W2[0, i]), 20, C_MODEL).move_to(e2[i].point_from_proportion(0.42)).shift(UP * 0.17 if i < 2 else DOWN * 0.17) for i in range(D)])
        bl = VGroup(*[txt(f"b = {f1(B1[i])}", 18, GREY_A).next_to(hid[i], UP, buff=0.04) for i in range(D)])
        b2l = txt(f"b = {f1(B2)}", 18, GREY_A).next_to(out, UP, buff=0.08)
        cols = VGroup(txt("input", 22, GREY_B).next_to(inp, DOWN, buff=1.2),
                      txt("hidden units", 22, C_RAMP).move_to([-1.4, -2.15, 0]),
                      txt("output", 22, C_MODEL).next_to(out, DOWN, buff=1.2))
        assert D == 4                                         # spoken: "four of them"
        self.say("There's no reason to stop at one ramp, so let's put four of them side by side. Each ramp is now a hidden unit "
                 "with its own weight and bias, and all of them read the same input x. Then a readout adds "
                 "them up, each with its own output weight, plus one more bias. The notes call this equation "
                 "one point seven.",
                 Write(head), FadeIn(inp), FadeIn(inp_t), *[FadeIn(h) for h in hid], *[FadeIn(t) for t in hid_t],
                 *[Create(e) for e in e1], FadeIn(w1l), FadeIn(bl), FadeIn(cols[:2]))
        self.cue("Then a readout adds", FadeIn(out), FadeIn(out_t), *[Create(e) for e in e2], FadeIn(w2l), FadeIn(b2l), FadeIn(cols[2]))
        self.hold(0.3)
        # forward pass with real numbers
        xv = X0
        new_inp = txt(f"{xv:g}", 26, YELLOW_D).move_to(inp)
        new_b = VGroup(*[txt(f"z = {f1(Z0[i])}", 18, YELLOW_D).next_to(hid[i], UP, buff=0.04) for i in range(D)])
        new_h = VGroup(*[txt(f"{H0[i]:g}", 24, C_RAMP if H0[i] > 0 else GREY).move_to(hid[i]) for i in range(D)])
        terms = "".join((" − " if W2[0, i] < 0 else (" + " if i else "")) + f"{abs(W2[0, i]):g}·{H0[i]:g}" for i in range(D))
        new_out = txt(f"{N0:g}", 26, YELLOW_D).move_to(out)
        sumline = txt(f"N({xv:g}) = {terms} + {B2:g} = {N0:g}", 26, YELLOW_D).move_to([0, 2.95, 0]).shift(RIGHT * 2.3)
        assert sumline.get_right()[0] < 7.0, sumline.get_right()
        assert X0 == 1.5 and sum(H0 > 0) == 3 and H0[1] == 0 and N0 == 3.5      # spoken below
        self.say("Let's push one point five through it. Each unit first computes its weight times x, plus its "
                 "bias, and we'll call that number z. ReLU then lets three of them through and sets the second "
                 "one to zero. Finally the readout weighs each output, adds them up with its bias, and out "
                 "comes three point five.",
                 Transform(inp_t, new_inp), *[Transform(bl[i], new_b[i]) for i in range(D)])
        self.cue("ReLU then lets three", *[Transform(hid_t[i], new_h[i]) for i in range(D)],
                 *[hid[i].animate.set_stroke(color=GREY, opacity=0.6) for i in range(D) if H0[i] == 0])
        self.cue("Finally the readout", Transform(out_t, new_out), FadeIn(sumline))
        self.hold(0.6)
        self.clear_stage()

    # ---------------------------------------------------------------- 3. matrix form
    def matrix_form(self):
        head = self.heading("The vectorized layer")

        def col(v):
            return Matrix([[f"{x:g}"] for x in v], element_alignment_corner=ORIGIN, v_buff=0.6).scale(0.62)

        eq1 = VGroup(mt(r"\vec z=", 0.85), col(W1[:, 0]), mt(r"x", 0.85), mt(r"+", 0.85), col(B1), mt(r"=", 0.85), col(Z0)).arrange(RIGHT, buff=0.25)
        eq1.move_to([0, 1.5, 0])
        assert eq1.width < 13.5, eq1.width
        shapes = mt(r"W^{(1)}\in\mathbb{R}^{d\times 1},\quad \vec b^{(1)}\in\mathbb{R}^{d}", 0.7, GREY_A).next_to(eq1, DOWN, buff=0.45)
        self.say("Going unit by unit gets tedious, so we stack the weights into a matrix and the biases into a "
                 "vector, and then one multiply does all the units at once. This first matrix is tall and "
                 "skinny. It has d rows and a single column, because our input is just one number.",
                 Write(head), FadeIn(eq1))
        self.cue("This first matrix", FadeIn(shapes))
        eq2 = VGroup(mt(r"\vec h=\mathrm{ReLU}(\vec z)=", 0.85, C_RAMP), col(H0)).arrange(RIGHT, buff=0.3)
        eq3 = VGroup(mt(r"N_\theta(x)=W^{(2)}\vec h+b^{(2)}=", 0.85, C_MODEL),
                     Matrix([[f"{v:g}" for v in W2[0]]], h_buff=0.9).scale(0.62), col(H0), mt(rf"+{B2:g}={N0:g}", 0.85)
                     ).arrange(RIGHT, buff=0.25)
        assert eq3.width < 13.5, eq3.width
        eq2.move_to([0, 1.5, 0])
        eq3.move_to([0, -0.9, 0])
        assert MACS == 8                                      # spoken: "eight multiply-adds"
        self.say("ReLU then acts on each entry separately. After that the second matrix, which is a single "
                 "row, squashes the four activations back down to one number. So the whole layer costs just "
                 "eight multiply-adds, and with vector inputs or outputs only the shapes change.",
                 FadeOut(eq1), FadeOut(shapes), FadeIn(eq2))
        self.cue("After that the second matrix", FadeIn(eq3))
        self.cue("So the whole layer", Indicate(eq2[1], color=YELLOW_D), Indicate(eq3[1], color=YELLOW_D))
        self.hold(0.6)
        self.clear_stage()

    # ---------------------------------------------------------------- 4. collapse
    def collapse(self):
        head = self.heading("Why the nonlinearity is essential")
        ax = make_axes([-1, 3, 1], [-3, 6, 3], 6.4, 3.4).move_to([-3.0, 0.15, 0])
        xl = txt("x", 24, GREY_B).next_to(ax.x_axis.get_end(), RIGHT, buff=0.15)
        curve = polyline(ax, XS, nonlin(XS), C_MODEL, 4)
        el = VGroup(*[Dot(ax.c2p(t, float(nonlin(np.array([t]))[0])), radius=0.07, color=YELLOW_D) for t in sorted(set(float(e) + 0.0 for e in ELBOWS))])
        lab = txt(f"N(x) with ReLU", 24, C_MODEL).next_to(ax, UP, buff=0.25)
        assert sorted(set(float(e) + 0.0 for e in ELBOWS)) == [0.0, 0.5, 1.0]      # spoken below
        eq_a = mt(r"W^{(2)}\big(W^{(1)}x+\vec b^{(1)}\big)+b^{(2)}", 0.75)
        eq_b1 = mt(r"=\big(W^{(2)}W^{(1)}\big)\,x", 0.75)
        eq_b2 = mt(r"\quad+\big(W^{(2)}\vec b^{(1)}+b^{(2)}\big)", 0.75)
        eq_c = mt(rf"={A_LIN:g}\,x{C_LIN:+g}", 0.9, RED_C)
        eqs = VGroup(eq_a, eq_b1, eq_b2, eq_c).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.9, 1.2, 0])
        assert eqs.get_right()[0] < 7.0 and eqs.get_left()[0] > 0.4, (eqs.get_left(), eqs.get_right())
        eq_b = VGroup(eq_b1, eq_b2)
        self.say("Here's the whole layer from before, drawn as a function of its input x. You can see it bend at the knots, which sit "
                 "at zero, one half, and one. But what if we deleted the ReLUs? Then two affine maps in a row "
                 "just multiply out into a single one, with one matrix and one bias.",
                 Write(head), Create(ax), FadeIn(xl), Create(curve, run_time=2.0), FadeIn(lab))
        self.cue("You can see it bend", FadeIn(el))
        self.cue("But what if we deleted", Write(eq_a))
        self.cue("Then two affine maps", Write(eq_b))
        _k = (lin(XS) >= -3) & (lin(XS) <= 6)
        line = polyline(ax, XS[_k], lin(XS)[_k], RED_C, 4)
        assert (A_LIN, C_LIN) == (4.0, -2.0)                  # spoken below
        self.say("With our numbers, the weights multiply out to four and the biases add up to minus two, so "
                 "what's left is just a line. We used four units and two layers, and all we got was a straight "
                 "line. Without the bend, depth buys us nothing.",
                 Write(eq_c), Create(line, run_time=1.6))
        self.cue("We used four units", Indicate(line, color=RED_C), Indicate(eq_c, color=RED_C))
        self.hold(0.4)
        chain = VGroup(*[box_label(n, c, w=1.5, h=0.6, font_size=22) for n, c in
                         [("affine", BLUE_C), ("ReLU", C_RAMP), ("affine", BLUE_C), ("ReLU", C_RAMP), ("affine", BLUE_C)]]).arrange(RIGHT, buff=0.35)
        chain.move_to([0, -2.1, 0])
        assert chain.get_bottom()[1] > -2.5
        assert chain.width < 13.5
        self.say("And that's why deep networks alternate, going affine, ReLU, affine, ReLU. The ReLUs in between "
                 "are what stop the layers from merging into one.",
                 FadeIn(chain, shift=UP * 0.2))
        self.hold(0.6)
        self.clear_stage()


def fmt_num(v):
    return f"{v:g}"
