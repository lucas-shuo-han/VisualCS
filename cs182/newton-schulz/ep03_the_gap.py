"""Newton–Schulz, episode 3: between √3 and √5. The stripes, why they fill the gap, and back to the matrix."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ns_common import *  # noqa: E402,F403
from ns_common import _root  # noqa: E402,F401


class Ep03TheGap(NSScene):
    SCENES = ["ep3_recap", "the_gap", "first_boundary", "basins", "boundary_points", "summary",
              "back_to_matrix"]
    CORNER_FROM = "ep3_recap"
    ASK = "Between √3 and √5"
    ASK_SAY = "Between square root of three and square root of five."
    GAP_SCENES = ("the_gap", "first_boundary", "basins", "boundary_points")

    def restore(self, first):
        self.add(self.make_corner())
        if first in self.GAP_SCENES:
            self.add(self.make_sizeline())

    def make_sizeline(self):
        """|p(x)| = |x| · (x² − 3)/2 in the top left corner: every argument about the gap uses it,
        so it stays on screen until the gap is settled."""
        line = MathTex(r"|p(x)|", r"=", r"|x|", r"\cdot", r"\frac{x^2-3}{2}", font_size=30)
        line.to_corner(UL, buff=0.3)
        self.sizeline = self.pin(line)
        return line

    def stay(self):
        """What clear_stage() leaves on the stage during the gap scenes."""
        return [self.corner, self.sizeline]

    # ------------------------------------------------------------ 0. what episode 2 gave us
    def ep3_recap(self):
        g = self.make_graph()
        ax = self.ax
        marks = self.gap_marks(ax)
        corner = self.make_corner()
        past = ax.plot(p, x_range=[S3, _root(-2.5, 1.0, 2.5)], color=C_MINUS, stroke_width=7)
        mirror = VGroup(mt(r"p(-x)=-p(x)", 36), txt("the mirror rule", 28, YELLOW_D)).arrange(DOWN, buff=0.15)
        negp = mt(r"x>\sqrt3:\quad p(x)<0", 36, C_MINUS)
        size = MathTex(r"|p(x)|", r"=", r"|x|", r"\cdot", r"\frac{x^2-3}{2}", font_size=40)
        facts = VGroup(mirror, negp, size).arrange(DOWN, buff=0.6).move_to([PANEL_X, 0.4, 0])
        box = SurroundingRectangle(size[4], color=YELLOW_D, buff=0.1, stroke_width=2.5)
        box_l = txt("size factor", 28, YELLOW_D).next_to(box, DOWN, buff=0.15)
        self.say("We are following one number as we apply p again and again. p of x is three halves x, minus "
                 "one half x cubed. Here is what we know so far. A negative value moves exactly like its "
                 "positive twin, with the sign flipped. We called that the mirror rule. Past square root of "
                 "three, p of x is negative, so a step flips the sign. And one step multiplies the size of the "
                 "value by the size factor, x squared minus three, over two.", FadeIn(g), run_time=1.5)
        self.cue("p of x is three halves x", FadeIn(corner))
        self.cue("A negative value moves", FadeIn(mirror[0]))
        self.cue("We called that the mirror rule", FadeIn(mirror[1]))
        self.cue("Past square root of three", FadeIn(marks[0]), FadeIn(marks[2]), Create(past), FadeIn(negp))
        self.cue("And one step multiplies", FadeIn(size))
        self.cue("by the size factor", Create(box), FadeIn(box_l))
        self.hold(0.8)
        line = self.make_sizeline()
        self.play(FadeOut(VGroup(g, marks[0], marks[2], past, mirror, negp, box, box_l)),
                  ReplacementTransform(size, line))

    def the_gap(self):
        g = self.make_graph()
        ax = self.ax
        marks = self.gap_marks(ax)
        gapseg = Line(ax.c2p(S3, 0), ax.c2p(S5, 0), color=C_ZERO, stroke_width=9)
        self.play(FadeIn(g), FadeIn(marks))
        # D2: the size factor runs from 0 to 1 across the gap, so every step shrinks the size
        assert (S3 ** 2 - 3) / 2 < 1e-12 and abs((S5 ** 2 - 3) / 2 - 1) < 1e-12
        ends = VGroup(mt(r"x^2=3:\quad\frac{3-3}{2}=0", 34, C_ZERO), mt(r"x^2=5:\quad\frac{5-3}{2}=1", 34, C_S5))
        ends.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([PANEL_X, 2.0, 0])
        small = mt(r"\sqrt3<x<\sqrt5:\quad 0<\frac{x^2-3}{2}<1", 34).next_to(ends, DOWN, buff=0.45)
        less = mt(r"|p(x)|<|x|", 44, C_ZERO).next_to(small, DOWN, buff=0.5)
        less_box = SurroundingRectangle(less, color=C_ZERO, buff=0.18, stroke_width=2.5)
        self.say("So below square root of three, everything goes to one, and beyond square root of five, "
                 "everything explodes. That leaves the gap between them. In the gap, every step flips the sign. "
                 "What about the size? One step multiplies it by the size factor, x squared minus three, over "
                 "two. At the left end of the gap, x squared is three, so the factor is zero. At the right end, "
                 "x squared is five, so the factor is one. In between, x squared is between three and five, so "
                 "the factor is between zero and one. Multiplying by a number between zero and one makes a "
                 "size smaller. So in the gap, the size of p of x is less than the size of x. Every step "
                 "brings the value closer to zero.", Create(gapseg))
        self.cue("One step multiplies it", Indicate(self.sizeline[4], color=YELLOW_D, scale_factor=1.25))
        self.cue("At the left end of the gap", FadeIn(ends[0]), Flash(marks[0], color=C_ZERO))
        self.cue("At the right end", FadeIn(ends[1]), Flash(marks[1], color=C_S5))
        self.cue("In between", FadeIn(small))
        self.cue("So in the gap, the size of p of x", FadeIn(less), Create(less_box))
        self.hold(1.0)

        # the hope: shrink until it is inside √3, where everything is known
        pos_in = Line(ax.c2p(0, 0), ax.c2p(S3, 0), color=C_PLUS, stroke_width=9)
        neg_in = Line(ax.c2p(-S3, 0), ax.c2p(0, 0), color=C_MINUS, stroke_width=9)
        known = VGroup(mt(r"\text{inside: }|x|<\sqrt3", 32), mt(r"x>0\ \ \to\ \ +1", 32, C_PLUS),
                       mt(r"x<0\ \ \to\ \ -1", 32, C_MINUS)).arrange(DOWN, buff=0.22)
        known.move_to([PANEL_X, 0.9, 0])
        # D3: inside √3 everything is known ("Suppose": that the size gets there is shown in scene 12)
        self.say("That suggests a plan. Suppose the size shrinks far enough to drop below square root of "
                 "three. Inside square root of three we already know everything. A positive value goes to plus "
                 "one. By the mirror rule, a negative value goes to minus one. So we only have to follow a "
                 "start until it gets inside, and see on which side it arrives.",
                 FadeOut(VGroup(ends, small)), VGroup(less, less_box).animate.move_to([PANEL_X, 2.3, 0]))
        self.cue("Inside square root of three we already know", FadeIn(known[0]))
        self.cue("A positive value", Create(pos_in), FadeIn(known[1]))
        self.cue("By the mirror rule", Create(neg_in), FadeIn(known[2]))
        self.hold()
        self.play(FadeOut(VGroup(less, less_box, known)))

        # three starts on the cobweb picture
        def trial(x0, d, y, terms, verdict, color):
            parts = VGroup(*[mt(t, 32) for t in terms]).arrange(RIGHT, buff=0.18)
            parts.move_to([PANEL_X, y, 0])
            v = txt(verdict, 24, color).next_to(parts, DOWN, buff=0.16)
            return Dot(self.ax.c2p(x0, 0), radius=0.07, color=WHITE), parts, v

        o = orbit(2.0, 1)
        assert o[1] == -1.0
        w1 = self.web(2.0, 3, C_MINUS)
        m1, c1, v1 = trial(2.0, 1, 2.5, ["2.0", r"\to\ -1"], "1 flip, ends at −1", C_MINUS)
        self.say("Try it on the cobweb picture. Start at two point zero. Go down to the curve, which gives "
                 "minus one. Then across to the diagonal. Minus one is inside, on the negative side, and it "
                 "is already a fixed point. So two point zero ends at minus one, after one flip.",
                 FadeIn(m1), FadeIn(c1[0]))
        self.cue("Go down to the curve", Create(w1[0]), FadeIn(c1[1]))
        self.cue("Then across to the diagonal", Create(w1[1]))
        self.cue("So two point zero ends", FadeIn(v1))
        self.hold()

        o = orbit(2.2, 3)
        assert o[1] < -S3 and 0 < o[2] < S3
        w2 = self.web(2.2, 8, WHITE)
        m2, c2, v2 = trial(2.2, 1, 1.35, ["2.2", r"\to\ " + num(o[1]), r"\to\ +" + num(o[2]),
                                          r"\to\cdots\to\ +1"], "2 flips, ends at +1", C_PLUS)
        self.say("Now two point two. Down to the curve, at minus two point zero two. That is smaller in size "
                 "than two point two, but it is still outside. So go across to the diagonal and step again. "
                 "This time the curve sends it up, to plus one point one one. Now it is inside, on the positive "
                 "side, and from there it settles at plus one. Two flips, and a different ending.",
                 FadeOut(w1), FadeOut(m1), FadeIn(m2), FadeIn(c2[0]))
        self.cue("Down to the curve", Create(w2[0]), FadeIn(c2[1]))
        self.cue("So go across to the diagonal", Create(w2[1]))
        self.cue("This time the curve sends it up", Create(w2[2]), FadeIn(c2[2]))
        self.cue("Now it is inside", self.draw(w2[3:], 0.3), FadeIn(c2[3]))
        self.cue("Two flips", FadeIn(v2))
        self.hold()

        o = orbit(2.23, 3)
        assert o[1] < -S3 and o[2] > S3 and -S3 < o[3] < 0
        w3 = self.web(2.23, 10, C_MINUS)
        m3, c3, v3 = trial(2.23, 2, 0.2, ["2.23", r"\to\ " + num(o[1]), r"\to\ +" + num(o[2]),
                                          r"\to\ " + num(o[3]), r"\to\cdots\to\ -1"],
                           "3 flips, ends at −1", C_MINUS)
        if c3.width > 6.0:
            c3.scale_to_fit_width(6.0)
        # 2.2 and 2.23 are 0.03 apart, one dot's width on this graph: show them on a magnified
        # piece of the axis first, so the new start is seen to be a different one
        lo_m, hi_m = 2.15, 2.27
        a_, b_ = ax.c2p(lo_m, 0), ax.c2p(hi_m, 0)
        look = Rectangle(width=b_[0] - a_[0], height=0.36, color=YELLOW_D, stroke_width=2.5).move_to((a_ + b_) / 2)
        mag = NumberLine(x_range=[lo_m, hi_m, 0.01], length=5.4, color=GREY_B, stroke_width=2,
                         include_tip=False, tick_size=0.04).move_to([PANEL_X, -1.75, 0])
        mag_box = SurroundingRectangle(mag, color=YELLOW_D, buff=0.62, stroke_width=2.5)
        links = VGroup(Line(look.get_corner(UR), mag_box.get_corner(UL), color=YELLOW_D, stroke_width=1.5),
                       Line(look.get_corner(DR), mag_box.get_corner(DL), color=YELLOW_D, stroke_width=1.5))
        mag_pts = VGroup(Dot(mag.n2p(2.2), radius=0.08, color=GREY_B), Dot(mag.n2p(2.23), radius=0.08, color=WHITE),
                         Line(mag.n2p(S5) + DOWN * 0.18, mag.n2p(S5) + UP * 0.18, color=C_S5, stroke_width=4))
        mag_l = VGroup(mt("2.2", 28, GREY_B).next_to(mag_pts[0], UP, buff=0.12),
                       mt("2.23", 28, WHITE).next_to(mag_pts[1], DOWN, buff=0.12),
                       mt(r"\sqrt5", 28, C_S5).next_to(mag_pts[2], UP, buff=0.08))
        inset = VGroup(look, mag, mag_box, links, mag_pts, mag_l)
        self.say("And two point two three, just a little further out. Minus two point two zero. Then plus two "
                 "point zero two. Then minus one point one zero. It takes three flips to get inside, it arrives "
                 "on the negative side, and it ends at minus one.",
                 FadeOut(w2), FadeIn(m3), FadeIn(c3[0]), Create(look))
        self.play(Create(links), FadeIn(mag), Create(mag_box), FadeIn(mag_pts[0]), FadeIn(mag_l[0]),
                  FadeIn(mag_pts[2]), FadeIn(mag_l[2]), run_time=0.8)
        self.play(GrowFromCenter(mag_pts[1]), FadeIn(mag_l[1]), FadeOut(m2), run_time=0.6)
        self.cue("Minus two point two zero", self.draw(w3[:2], 0.4), FadeIn(c3[1]))
        self.cue("Then plus two", self.draw(w3[2:4], 0.4), FadeIn(c3[2]))
        self.cue("Then minus one point one zero", self.draw(w3[4:6], 0.4), FadeIn(c3[3]))
        self.cue("It takes three flips", self.draw(w3[6:], 0.3), FadeIn(c3[4]), FadeIn(v3))
        self.hold()

        rule = VGroup(txt("odd number of flips: arrives negative, ends at −1", 24, C_MINUS),
                      txt("even number of flips: arrives positive, ends at +1", 24, C_PLUS))
        rule.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([PANEL_X, -1.6, 0])
        if rule.width > 6.2:
            rule.scale_to_fit_width(6.2)
        self.say("So the starts in the gap do not all end the same way. What matters is how many flips it "
                 "takes to get inside. Every start here is positive, and each flip changes the sign. After an "
                 "odd number of flips the value arrives negative, and ends at minus one. After an even number "
                 "it arrives positive, and ends at plus one.", FadeOut(w3), FadeOut(m3), FadeOut(inset))
        self.cue("After an odd number", FadeIn(rule[0]))
        self.cue("After an even number", FadeIn(rule[1]))
        self.hold()
        self.clear_stage(*self.stay())

        # the whole picture: color every start by its fate
        ov = NumberLine(x_range=[0, 2.4, 0.5], length=9.0, color=GREY_B, stroke_width=2,
                        include_tip=False, tick_size=0.04).move_to([-0.2, 0.4, 0])
        ovl = VGroup(mt(r"\sqrt3", 28, C_ZERO).next_to(ov.n2p(S3), DOWN, buff=0.35),
                     mt(r"\sqrt5", 28, C_S5).next_to(ov.n2p(S5), DOWN, buff=0.35),
                     mt(r"1", 28, C_PLUS).next_to(ov.n2p(1), DOWN, buff=0.35),
                     mt(r"0", 28, GREY_B).next_to(ov.n2p(0), DOWN, buff=0.35))

        def fcol(v):
            f = fate(v)[0]
            return C_S5 if f == "diverges" else (C_PLUS if f > 0 else (C_MINUS if f < 0 else C_ZERO))

        def colored(line, lo, hi, n, y):
            out, cols, i = VGroup(), [fcol(lo + (k + 0.5) * (hi - lo) / n) for k in range(n)], 0
            while i < n:
                j = i
                while j + 1 < n and cols[j + 1] == cols[i]:
                    j += 1
                a_ = line.n2p(lo + i * (hi - lo) / n)[0]
                b_ = line.n2p(lo + (j + 1) * (hi - lo) / n)[0]
                out.add(Rectangle(width=b_ - a_, height=0.5, stroke_width=0, fill_color=cols[i],
                                  fill_opacity=0.9).move_to([(a_ + b_) / 2, y, 0]))
                i = j + 1
            return out

        strip = colored(ov, 0, 2.4, 2400, 0.4)
        assert len(strip) >= 5, len(strip)
        legend = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.9),
                                 txt(t, 22, c)).arrange(RIGHT, buff=0.12)
                          for c, t in ((C_PLUS, "ends at +1"), (C_MINUS, "ends at −1"),
                                       (C_S5, "explodes"))]).arrange(RIGHT, buff=0.6).move_to([-0.2, 1.6, 0])
        self.say("Three starts are not the whole story, so here is every start at once. Take each start "
                 "from zero to two point four, run the iteration, and color it by where it ends. Teal means "
                 "plus one, gold means minus one, and red means it explodes.",
                 FadeIn(ov), FadeIn(ovl))
        self.cue("Teal means", FadeIn(legend))
        self.play(LaggedStart(*[FadeIn(r) for r in strip], lag_ratio=0.02), run_time=2.5)
        self.hold(1.0)
        lo_z, hi_z = 2.1, S5
        a0, b0 = ov.n2p(lo_z)[0], ov.n2p(hi_z)[0]
        focus = Rectangle(width=b0 - a0, height=0.8, color=YELLOW_D, stroke_width=3).move_to([(a0 + b0) / 2, 0.4, 0])
        Lz = NumberLine(x_range=[lo_z, hi_z, 0.05], length=9.0, include_tip=False).move_to([-0.2, -1.6, 0])
        mag = colored(Lz, lo_z, hi_z, 1500, -1.6)
        zl = VGroup(mt(num(lo_z, 1), 24, GREY_B).next_to(mag, DOWN, buff=0.15).align_to(mag, LEFT),
                    mt(r"\sqrt5", 24, C_S5).next_to(mag, DOWN, buff=0.15).align_to(mag, RIGHT))
        links = VGroup(Line(focus.get_corner(DL), mag.get_corner(UL), color=YELLOW_D, stroke_width=1.5),
                       Line(focus.get_corner(DR), mag.get_corner(UR), color=YELLOW_D, stroke_width=1.5))
        self.say("Below square root of three it is all teal, as we showed. The gap begins gold. That is where "
                 "two point zero sits, with its one flip. Then comes a thin teal stripe, which holds two point "
                 "two. And then more stripes, each thinner than the last, squeezed up against square root "
                 "of five.")
        self.cue("Then comes a thin teal stripe", Create(focus))
        self.cue("And then more stripes", Create(links), FadeIn(mag), FadeIn(zl))
        self.hold(1.5)
        self.say("So each stripe is a flip count. One flip, two flips, three flips, and so on. Two things are "
                 "still open. Where exactly does one flip turn into two, and two into three? And do these "
                 "stripes really fill the whole gap, all the way up to square root of five?")
        self.hold(0.5)
        self.clear_stage(*self.stay())

    # ------------------------------------------------------------ 9. sizes only: the folded curve, and b1
    def gap_picture(self, close=False):
        """Sizes in the gap: y = |p(x)| and y = x (not to scale: x is stretched).
        close=True is the corner next to √5, where the edges pile up."""
        lo, hi, ylo, top = (2.05, 2.26, 1.6, 2.3) if close else (1.65, 2.3, 0.0, 2.5)
        ax = Axes(x_range=[lo, hi, 0.05], y_range=[ylo, top, 0.1 if close else 0.5], x_length=5.8, y_length=5.0,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2, "tick_size": 0.04})
        ax.move_to([-3.3, 0.25, 0])
        xs, ys = ((2.1, 2.2), (1.8, 2.0, 2.2)) if close else ((1.8, 2.0), (1, 2))
        nums = VGroup(*[mono(str(v), 18, GREY_B).next_to(ax.c2p(v, ylo), DOWN, buff=0.14) for v in xs],
                      *[mono(str(v), 18, GREY_B).next_to(ax.c2p(lo, v), LEFT, buff=0.12) for v in ys])
        x0 = max(S3, _root(-(ylo + 0.001), S3, 2.5))
        x1 = min(_root(-(top - 0.02), S3, 2.5), hi)
        curve = ax.plot(lambda x: abs(p(x)), x_range=[x0, x1], color=C_P, stroke_width=4)
        d0, d1 = max(lo, ylo), min(hi, top)
        diag = Line(ax.c2p(d0, d0), ax.c2p(d1, d1), color=C_DIAG, stroke_width=2.5)
        lab_c = mt(r"\text{size after one step}", 26, C_P).move_to(ax.c2p(*((2.2, 1.68) if close else (1.82, 1.0))))
        lab_d = mt(r"\text{same size}", 26, C_DIAG).move_to(ax.c2p(*((2.09, 2.2) if close else (1.9, 2.42))))
        s3 = VGroup() if close else VGroup(
            Line(ax.c2p(S3, -0.05), ax.c2p(S3, 0.05), color=C_ZERO, stroke_width=4),
            mt(r"\sqrt3", 26, C_ZERO).next_to(ax.c2p(S3, 0), DOWN, buff=0.14))
        xlab = txt("size of the start", 20, GREY_B).next_to(ax.c2p((lo + hi) / 2 - 0.02 * (hi - lo), ylo), DOWN,
                                                              buff=0.55)
        self.gx, self.gbox = ax, (lo, hi, ylo)
        return VGroup(ax, nums, curve, diag, lab_c, lab_d, s3, xlab)

    def level(self, v, color, label):
        ax, (lo, hi, _) = self.gx, self.gbox
        line = DashedLine(ax.c2p(lo, v), ax.c2p(hi, v), color=color, dash_length=0.08, stroke_width=2.5)
        return VGroup(line, mt(label, 26, color).next_to(line, RIGHT, buff=0.1))

    def edge(self, k, shift=ORIGIN):
        """b_k: where the folded curve reaches the height b_{k-1}."""
        ax, (_, _, ylo) = self.gx, self.gbox
        d = Dot(ax.c2p(B[k], B[k - 1]), radius=0.07, color=C_ZERO)
        drop = DashedLine(ax.c2p(B[k], B[k - 1]), ax.c2p(B[k], ylo), color=C_ZERO, dash_length=0.06)
        lab = mt(f"b_{{{k}}}", 26, C_ZERO).next_to(ax.c2p(B[k], ylo), DOWN, buff=0.14).shift(shift)
        return VGroup(d, drop, lab)

    def stripe(self, k):
        ax, (lo, _, ylo) = self.gx, self.gbox
        return Line(ax.c2p(max(B[k - 1], lo), ylo), ax.c2p(max(B[k], lo), ylo),
                    color=C_MINUS if k % 2 else C_PLUS, stroke_width=10)

    def first_boundary(self):
        g = self.make_graph()
        ax = self.ax
        marks = self.gap_marks(ax)
        self.play(FadeIn(g), FadeIn(marks))
        twin = VGroup(mt(r"p(-x)=-p(x)", 36), mt(r"\text{size: }\ |x|\ \to\ |p(x)|", 34, C_P),
                      txt("sign: one flip for each step from outside √3", 22, C_ZERO))
        twin.arrange(DOWN, buff=0.35).move_to([PANEL_X, 1.8, 0])
        self.say("Following the sign and the size together on this picture gets messy. But the mirror rule "
                 "lets us take them apart. A negative value moves exactly like its positive twin, with the sign "
                 "flipped. So the size follows a rule of its own. The next size is the size of p of x. And the "
                 "sign we can simply count. Every step that starts outside square root of three is one flip.",
                 FadeIn(twin[0]))
        self.cue("So the size follows", FadeIn(twin[1]))
        self.cue("And the sign we can simply count", FadeIn(twin[2]))
        self.hold()

        # fold the part below the axis up: y = |p(x)|
        xq = _root(-2.45, S5, 2.5)
        fold = ax.plot(p, x_range=[S3, xq], color=C_P, stroke_width=4)
        up = ax.plot(lambda x: abs(p(x)), x_range=[S3, xq], color=C_P, stroke_width=4)
        keep = ax.plot(p, x_range=[0, S3], color=C_P, stroke_width=4)
        self.say("So fold the picture. We only need positive sizes, so look at the right half. Wherever the "
                 "curve dips below the axis, flip that part up. This folded curve answers one question. "
                 "If the size is x now, what is the size after one step?",
                 FadeOut(twin), self.curve.animate.set_stroke(opacity=0.2), FadeIn(keep), FadeIn(fold))
        self.cue("flip that part up", Transform(fold, up), run_time=2.0)
        self.hold()

        shrink = ax.plot(lambda x: abs(p(x)), x_range=[S3, S5], color=C_ZERO, stroke_width=7)
        grow = ax.plot(lambda x: abs(p(x)), x_range=[S5, xq], color=C_S5, stroke_width=7)
        meet = Dot(ax.c2p(S5, S5), radius=0.08, color=C_S5)
        cmp_ = VGroup(mt(r"\text{below the diagonal: }|p(x)|<|x|", 30, C_ZERO),
                      mt(r"\text{above the diagonal: }|p(x)|>|x|", 30, C_S5))
        cmp_.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([PANEL_X, 2.2, 0])
        self.say("Now compare it with the diagonal, where the size would stay the same. Between square root "
                 "of three and square root of five, the folded curve is below the diagonal. The size after "
                 "the step is smaller than the size before. Beyond square root of five it is above the "
                 "diagonal, and the size grows. They meet exactly at square root of five.")
        self.cue("Between square root of three", Create(shrink), FadeIn(cmp_[0]))
        self.cue("Beyond square root of five", Create(grow), FadeIn(cmp_[1]))
        self.cue("They meet exactly", GrowFromCenter(meet), Flash(meet, color=C_S5))
        self.hold()

        o = orbit(2.2, 3)
        wf = self.web(2.2, 6, WHITE, f=lambda x: abs(p(x)))
        mf = Dot(ax.c2p(2.2, 0), radius=0.07, color=WHITE)
        sizes = mt(r"2.2\ \to\ " + num(-o[1]) + r"\ \to\ " + num(o[2]) + r"\ \to\ \cdots\ \to\ 1", 34)
        sizes.next_to(cmp_, DOWN, buff=0.6)
        count = txt("two steps start outside √3: two flips", 24, C_PLUS).next_to(sizes, DOWN, buff=0.25)
        self.say("And the cobweb works on the folded picture too. Start at two point two. Up to the folded "
                 "curve, at two point zero two. Across to the diagonal, and then to the curve again, at one "
                 "point one one. Now we are inside, and the size climbs to one. Two of these steps started "
                 "outside square root of three. So two flips, and the sign ends up positive.",
                 FadeOut(grow), FadeIn(mf), FadeIn(sizes[0][:3]))
        self.cue("Up to the folded curve", Create(wf[0]), FadeIn(sizes[0][3:8]))
        self.cue("Across to the diagonal", self.draw(wf[1:3], 0.5), FadeIn(sizes[0][8:13]))
        self.cue("Now we are inside", self.draw(wf[3:], 0.3), FadeIn(sizes[0][13:]))
        self.cue("Two of these steps", FadeIn(count))
        self.hold()

        # zoom in on the gap: a box on the full graph grows into the stretched picture
        box = Rectangle(width=ax.c2p(2.3, 0)[0] - ax.c2p(1.65, 0)[0], height=ax.c2p(0, 2.5)[1] - ax.c2p(0, 0)[1],
                        color=YELLOW_D, stroke_width=3)
        box.move_to((ax.c2p(1.65, 0) + ax.c2p(2.3, 2.5)) / 2)
        pic = self.gap_picture()
        gx = self.gx
        lvl = self.level(S3, C_ZERO, r"\sqrt3")
        lvl_l = lvl[1]
        e1 = self.edge(1)
        st1 = self.stripe(1)
        land = Line(gx.c2p(1.65, 0), gx.c2p(1.65, S3), color=C_MINUS, stroke_width=10)
        # D4: the question; D5: the folded curve only goes up, so it meets the level once
        assert all(abs(p(a_)) < abs(p(b_)) for a_, b_ in zip(np.linspace(S3, S5, 60), np.linspace(S3, S5, 60)[1:]))
        ask = mt(r"|p(x)|<\sqrt3\ \ ?", 36).move_to([PANEL_X, 2.3, 0])
        form = mt(r"|p(x)|=x\cdot\frac{x^2-3}{2}", 36).next_to(ask, DOWN, buff=0.5)
        up = mt(r"x\ \uparrow\qquad\frac{x^2-3}{2}\ \uparrow\qquad\Longrightarrow\qquad|p(x)|\ \uparrow", 36)
        fit(up).next_to(form, DOWN, buff=0.45)
        lo_d = Dot(gx.c2p(S3, 0), radius=0.07, color=WHITE)
        hi_d = Dot(gx.c2p(S5, S5), radius=0.07, color=WHITE)
        lo_l = mt(r"\text{height }0", 28).next_to(lo_d, UR, buff=0.1)
        hi_l = mt(r"\text{height }\sqrt5", 28).next_to(hi_d, UL, buff=0.08)
        once = txt("one crossing", 28, C_ZERO).next_to(up, DOWN, buff=0.45)
        defn = mt(r"|p(b_1)|=\sqrt3", 36, C_ZERO).move_to([PANEL_X, 2.3, 0])
        signed = mt(r"p(b_1)=-\sqrt3", 36, C_ZERO).move_to(defn)
        maps = mt(r"(\sqrt3,\ b_1)\ \longrightarrow\ (-\sqrt3,\ 0)\ \longrightarrow\ -1", 36, C_MINUS)
        fit(maps).next_to(defn, DOWN, buff=0.45)
        first = txt("first stripe: one flip, ends at −1", 24, C_MINUS).next_to(maps, DOWN, buff=0.3)
        self.say("Now zoom in on the gap, and stretch it sideways so we can see. Start with the simplest case. "
                 "Which starts get inside in a single step? Those whose size after one step is below square "
                 "root of three. So draw that level as a horizontal line. How often does the folded curve cross "
                 "this line? Look at its formula, x times the size factor. As x moves to the right through the "
                 "gap, x gets bigger, and the size factor gets bigger too. So their product only goes up. It "
                 "starts at height zero, at square root of three, and it ends at height square root of five. "
                 "Our line lies between those two heights. And a curve that only goes up passes each height "
                 "once. So it crosses the line at exactly one point. Call that start b one, b for boundary. "
                 "Its size after one step is exactly square root of three. And in the gap, p is negative. So p "
                 "of b one is minus square root of three. Now take any start between square root of three and "
                 "b one. It is to the left of the crossing, so its step lands below the line, on the negative "
                 "side. That is somewhere between minus square root of three and zero. It is inside, and it is "
                 "negative, so it ends at minus one. One flip. This is the first stripe.", Create(box))
        self.expand(box, pic, keep=self.stay())
        self.cue("Those whose size after one step", FadeIn(ask))
        self.cue("So draw that level", Create(lvl[0]), FadeIn(lvl_l))
        self.cue("Look at its formula", FadeIn(form))
        self.cue("x gets bigger, and the size factor", FadeIn(up))
        self.cue("starts at height zero", GrowFromCenter(lo_d), FadeIn(lo_l))
        self.cue("and it ends at height", GrowFromCenter(hi_d), FadeIn(hi_l))
        self.cue("So it crosses the line at exactly one point")
        self.zoom_to(e1[0], GrowFromCenter(e1[0]), FadeIn(once), width=6.5, run_time=1.5)
        self.play(Flash(e1[0], color=C_ZERO))
        self.cue("Call that start b one")
        self.zoom_back(Create(e1[1]), FadeIn(e1[2]), FadeOut(VGroup(ask, form, up, once, lo_d, lo_l, hi_d, hi_l)),
                       run_time=1.4)
        self.cue("Its size after one step is exactly", FadeIn(defn))
        self.cue("So p of b one is minus", Transform(defn, signed))
        self.cue("Now take any start between", Create(st1))
        self.cue("so its step lands below the line", TransformFromCopy(st1, land), run_time=1.2)
        self.cue("That is somewhere between minus", FadeIn(maps))
        self.cue("This is the first stripe", FadeIn(first))
        self.hold()

        target = 2 * S3
        tries = [(v, v ** 3 - 3 * v) for v in (2.1, 2.2)]
        assert tries[0][1] < target < tries[1][1]
        eq0 = mt(r"b\cdot\frac{b^2-3}{2}=\sqrt3", 34, C_ZERO).next_to(defn, DOWN, buff=0.4)
        eq = mt(r"b^3-3b=2\sqrt3\approx" + num(target), 34, C_ZERO).next_to(eq0, DOWN, buff=0.3)
        # the cubic does have a closed form (substitute b = t + 1/t); it is shown, not used
        S2 = math.sqrt(2)
        assert abs((S3 + S2) ** (1 / 3) + (S3 - S2) ** (1 / 3) - B[1]) < 1e-9
        exact = fit(mt(r"b_1=\sqrt[3]{\sqrt3+\sqrt2}+\sqrt[3]{\sqrt3-\sqrt2}", 28, GREY_B)).next_to(eq, DOWN, buff=0.3)
        t1 = mt(r"b=2.1:\quad " + num(tries[0][1]) + r"\ \ \text{too small}", 30).next_to(exact, DOWN, buff=0.3)
        t2 = mt(r"b=2.2:\quad " + num(tries[1][1]) + r"\ \ \text{too big}", 30).next_to(t1, DOWN, buff=0.22)
        val = mt(r"b_1\approx" + num(B[1], 3), 38, C_ZERO).next_to(t2, DOWN, buff=0.35)
        self.say("Where is b one exactly? Its size after one step must be square root of three. With the size "
                 "factor, that is b, times b squared minus three, over two, equals square root of three. "
                 "Multiply by two, and we get b cubed, minus three b, equals two times square root of three, "
                 "which is about three point four six. There is an exact formula for this b, built from cube "
                 "roots, but it does not tell us much. So just try values. Two point one gives two point nine "
                 "six, which is too small. Two point two gives four point zero five, which is too big. Closing "
                 "in between them gives about two point one four eight.",
                 FadeOut(first), FadeOut(maps))
        self.cue("With the size factor", FadeIn(eq0))
        self.cue("Multiply by two", FadeIn(eq))
        self.cue("There is an exact formula", FadeIn(exact))
        self.cue("Two point one gives", FadeIn(t1))
        self.cue("Two point two gives", FadeIn(t2))
        self.cue("Closing in", FadeIn(val), Flash(e1[0], color=C_ZERO))
        self.hold()

        chk = VGroup(*[Dot(gx.c2p(v, 0), radius=0.07, color=c)
                       for v, c in ((1.8, C_MINUS), (2.0, C_MINUS), (2.2, C_PLUS))])
        chk_l = mt("2.2", 24, C_PLUS).next_to(chk[2], UP, buff=0.12)
        order = mt(r"1.8,\ \ 2.0\ <\ b_1\ <\ 2.2", 36).move_to(eq)
        self.say("That fits what we saw. One point eight and two point zero are both below b one, in the first "
                 "stripe, and both ended at minus one. Two point two is above b one. Its first step did not "
                 "get inside, and it needed a second flip.",
                 FadeOut(VGroup(eq0, eq, exact, t1, t2)), GrowFromCenter(chk[0]), GrowFromCenter(chk[1]),
                 FadeIn(order[0][:10]))
        self.cue("Two point two is above", GrowFromCenter(chk[2]), FadeIn(chk_l), FadeIn(order[0][10:]))
        self.hold(0.5)
        self.clear_stage(*self.stay())

    # ------------------------------------------------------------ 10. the alternating basins
    def basin_bar(self, lo, colored=True, n=12):
        X0, W, Y = -4.7, 11.3, 0.45
        span = S5 - lo

        def X(v):
            return X0 + (v - lo) / span * W

        bar = VGroup()
        rects, ticks, labels, fates = VGroup(), VGroup(), VGroup(), VGroup()
        for k in range(1, n + 1):
            a, b = max(B[k - 1], lo), max(B[k], lo)
            w = max(X(b) - X(a), 1e-4)
            c = (C_MINUS if k % 2 else C_PLUS) if colored else GREY_D
            r = Rectangle(width=w, height=0.62, stroke_width=0, fill_color=c, fill_opacity=0.75)
            r.move_to([(X(a) + X(b)) / 2, Y, 0])
            rects.add(r)
            f = mt("-1" if k % 2 else "+1", 30, BLACK).move_to(r)
            f.set_opacity(1 if (colored and w > 0.75) else 0)
            fates.add(f)
        for k in range(1, n + 1):
            x = X(B[k])
            gap = X(B[k + 1]) - x if k + 1 < len(B) else 0
            t = Line([x, Y - 0.36, 0], [x, Y + 0.36, 0], color=WHITE, stroke_width=2)
            t.set_opacity(1 if B[k] >= lo else 0)
            ticks.add(t)
            lab = mt(f"b_{{{k}}}", 28).next_to(t, DOWN, buff=0.12)
            lab.set_opacity(1 if (B[k] >= lo - 1e-12 and gap > 0.42) else 0)
            labels.add(lab)
        edge = Line([X(S5), Y - 0.5, 0], [X(S5), Y + 0.5, 0], color=C_S5, stroke_width=4)
        edge_l = mt(r"\sqrt5", 30, C_S5).next_to(edge, DOWN, buff=0.12)
        bar.add(rects, fates, ticks, labels, edge, edge_l)
        bar.rects, bar.fates, bar.X = rects, fates, X
        return bar

    def basins(self):
        pic = self.gap_picture()
        gx = self.gx
        lvl = self.level(S3, C_ZERO, r"\sqrt3")
        e1, st1 = self.edge(1), self.stripe(1)
        self.play(FadeIn(pic), FadeIn(lvl), FadeIn(e1), FadeIn(st1))

        def band(k):
            c = C_MINUS if k % 2 else C_PLUS
            r = Rectangle(width=gx.c2p(2.3, 0)[0] - gx.c2p(1.65, 0)[0],
                          height=gx.c2p(0, B[k])[1] - gx.c2p(0, B[k - 1])[1],
                          stroke_width=0, fill_color=c, fill_opacity=0.22)
            r.move_to([(gx.c2p(1.65, 0)[0] + gx.c2p(2.3, 0)[0]) / 2,
                       (gx.c2p(0, B[k])[1] + gx.c2p(0, B[k - 1])[1]) / 2, 0])
            side = Line(gx.c2p(1.65, B[k - 1]), gx.c2p(1.65, B[k]), color=c, stroke_width=10)
            return VGroup(r, side)

        band1 = band(1)
        idea = VGroup(txt("lands in stripe 1", 24, C_MINUS), txt("= one more flip to go", 24, C_MINUS))
        idea.arrange(DOWN, buff=0.15).move_to([PANEL_X, 2.5, 0])
        self.say("Now the starts above b one. Their first step does not get inside. But we do not have to "
                 "follow them all the way. Suppose the first step lands, in size, somewhere in the first stripe. "
                 "We already know the first stripe. From there it takes one more flip to get inside. So such a "
                 "start flips exactly twice.")
        self.cue("Suppose the first step lands", TransformFromCopy(st1, band1[1]), FadeIn(band1[0]),
                 FadeIn(idea[0]), run_time=1.5)
        self.cue("From there it takes one more flip", FadeIn(idea[1]))
        self.hold()

        e2, st2 = self.edge(2), self.stripe(2)
        lvl2 = self.level(B[1], C_ZERO, "b_1")
        # D7: p(b2) = −b1, and the whole second stripe lands on the first one, mirrored
        d2 = mt(r"|p(b_2)|=b_1", 36, C_ZERO).next_to(idea, DOWN, buff=0.4)
        d2s = mt(r"p(b_2)=-b_1", 36, C_ZERO).move_to(d2)
        map2 = mt(r"(b_1,\ b_2)\ \longrightarrow\ (-b_1,\ -\sqrt3)", 36, C_PLUS).next_to(d2, DOWN, buff=0.35)
        second = txt("second stripe: two flips, ends at +1", 24, C_PLUS).next_to(map2, DOWN, buff=0.3)
        self.say("Which starts are those? Read it off the picture. On the vertical axis, the first stripe is "
                 "the band of sizes from square root of three up to b one. The folded curve only goes up, so "
                 "it passes through that band once. It enters at b one, where its height is square root of "
                 "three. And it leaves where its height is exactly b one. Call that point b two. So the size of "
                 "p of b two is b one. The start is positive and the step flips it, so p of b two is minus b "
                 "one. Now take any start between b one and b two. Its step lands between minus b one and "
                 "minus square root of three. That is the first stripe, mirrored. From there it takes one more "
                 "flip, so two flips in all, an even number. It ends at plus one. This is the second stripe.")
        self.cue("It enters at b one", Indicate(e1[0], color=WHITE, scale_factor=1.6))
        self.cue("And it leaves where its height", FadeIn(lvl2), GrowFromCenter(e2[0]))
        self.cue("Call that point b two", Create(e2[1]), FadeIn(e2[2]))
        self.cue("So the size of p of b two", FadeIn(d2))
        self.cue("so p of b two is minus b one", Transform(d2, d2s))
        self.cue("Now take any start between b one and b two", Create(st2))
        self.cue("Its step lands between", FadeIn(map2))
        self.cue("This is the second stripe", FadeIn(second))
        self.hold()

        y22 = abs(p(2.2))
        assert S3 < y22 < B[1] and B[1] < 2.2 < B[2]
        dot22 = Dot(gx.c2p(2.2, y22), radius=0.07, color=WHITE)
        path22 = VGroup(DashedLine(gx.c2p(2.2, 0), gx.c2p(2.2, y22), color=WHITE, dash_length=0.06),
                        DashedLine(gx.c2p(2.2, y22), gx.c2p(1.65, y22), color=WHITE, dash_length=0.06))
        ex = mt(r"2.2\ \to\ \text{size }" + num(y22) + r"\qquad\sqrt3<" + num(y22) + r"<b_1", 30)
        fit(ex).next_to(second, DOWN, buff=0.4)
        self.say("Check it with two point two. It sits between b one and b two. Its first step has size two "
                 "point zero two. And two point zero two lies between square root of three and b one, in the "
                 "first stripe. So one more flip, and it is inside. That is the two flips we counted, and it "
                 "ended at plus one.")
        self.cue("Its first step has size", Create(path22[0]), GrowFromCenter(dot22))
        self.cue("And two point zero two lies", Create(path22[1]), FadeIn(ex))
        self.hold()

        band2 = band(2)
        e3, st3 = self.edge(3, shift=DOWN * 0.38 + RIGHT * 0.1), self.stripe(3)
        d3 = mt(r"p(b_3)=-b_2", 36, C_ZERO).move_to(d2)
        third = txt("third stripe: three flips, ends at −1", 24, C_MINUS).move_to(second)
        # D8: the three edges side by side, the rule behind them, and the list they start
        assert all(abs(p(B[k + 1]) + B[k]) < 1e-12 for k in range(6))
        trio = VGroup(mt(r"p(b_1)=-\sqrt3", 36, C_ZERO), mt(r"p(b_2)=-b_1", 36, C_ZERO),
                      mt(r"p(b_3)=-b_2", 36, C_ZERO)).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        trio.move_to([PANEL_X, 1.7, 0])
        rule = mt(r"p(b_{n+1})=-b_n", 44, YELLOW_D).next_to(trio, DOWN, buff=0.5)
        rule_box = SurroundingRectangle(rule, color=YELLOW_D, buff=0.16, stroke_width=2.5)
        lst = mt(r"\sqrt3,\ \ b_1,\ \ b_2,\ \ b_3,\ \ \dots", 36).next_to(rule_box, DOWN, buff=0.5)
        self.say("And the same step works again. Starts that land in the second stripe need one flip more "
                 "than the second stripe does, so three flips. The curve leaves that band where its height is "
                 "b two. Call that point b three. So p of b three is minus b two. The starts between b two and "
                 "b three are the third stripe, and they end at minus one. Put the three edges next to each "
                 "other. p of b one is minus square root of three. p of b two is minus b one. p of b three is "
                 "minus b two. One step sends each edge to the edge before it, with the sign flipped. And "
                 "nothing stops us from going on. So we get a whole list of edges. Square root of three, then "
                 "b one, b two, b three, and so on. Each new stripe is carried onto the stripe before it, so "
                 "it needs exactly one more flip.",
                 FadeOut(VGroup(dot22, path22, ex, idea, map2)), FadeOut(band1[0]))
        self.cue("Starts that land in the second stripe", TransformFromCopy(st2, band2[1]), FadeIn(band2[0]),
                 run_time=1.5)
        # b3 is 0.013 right of b2 and 0.002 left of √5: move the camera in to see it apart
        self.cue("Call that point b three")
        self.zoom_to(gx.c2p(2.215, 2.17), GrowFromCenter(e3[0]), width=4.6, run_time=1.6)
        self.play(Flash(e3[0], color=C_ZERO, flash_radius=0.12, line_length=0.08))
        self.cue("So p of b three is minus b two")
        self.zoom_back(Create(e3[1]), FadeIn(e3[2]), Transform(d2, d3), run_time=1.4)
        self.cue("The starts between b two and b three", Create(st3), Transform(second, third))
        self.cue("Put the three edges next to each other", FadeOut(VGroup(d2, second)))
        self.cue("p of b one is minus square root of three", FadeIn(trio[0]))
        self.cue("p of b two is minus b one", FadeIn(trio[1]))
        self.cue("p of b three is minus b two", FadeIn(trio[2]))
        self.cue("One step sends each edge", FadeIn(rule), Create(rule_box))
        self.cue("So we get a whole list of edges", FadeIn(lst))
        self.hold()

        vals = VGroup(*[mt(f"b_{{{k}}}\\approx{B[k]:.3f}", 34, C_ZERO) for k in (1, 2, 3)],
                      mt(r"\sqrt5\approx" + num(S5, 3), 34, C_S5)).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        vals.move_to([PANEL_X, 0.2, 0])
        self.say("Each edge is found like b one, by trying values. b one is about two point one four eight. "
                 "b two is about two point two two one. b three is about two point two three four. They creep "
                 "up toward square root of five, which is two point two three six.",
                 FadeOut(VGroup(trio, rule, rule_box, lst)), FadeIn(vals[0]))
        self.cue("b two is about", FadeIn(vals[1]))
        self.cue("b three is about", FadeIn(vals[2]))
        self.cue("They creep up", FadeIn(vals[3]))
        self.hold()
        self.clear_stage(*self.stay())

        # all the stripes on one bar, then zoom towards √5
        live = self.basin_bar(S3)
        s3l = mt(r"\sqrt3", 30, C_ZERO).next_to([live.X(S3), 0.45 - 0.31, 0], DOWN, buff=0.18)
        rule = VGroup(txt("stripe n:  n flips", 28), txt("odd n: ends at −1", 28, C_MINUS),
                      txt("even n: ends at +1", 28, C_PLUS)).arrange(RIGHT, buff=0.7).move_to([0, -1.2, 0])
        if rule.width > 11.5:
            rule.scale_to_fit_width(11.5)
        self.say("So here are all the stripes on one line. Stripe number n flips n times. An odd n ends at "
                 "minus one, and an even n ends at plus one. That is the striped picture we saw.",
                 FadeIn(live), FadeIn(s3l))
        self.cue("Stripe number n", FadeIn(rule[0]))
        self.cue("An odd n", FadeIn(rule[1]), FadeIn(rule[2]))
        self.hold()
        t = ValueTracker(0.0)
        zoomed = always_redraw(lambda: self.basin_bar(S5 - (S5 - S3) * 6 ** (-t.get_value())))
        self.remove(live)
        self.add(zoomed)
        self.say("The stripes pile up against square root of five. Zoom in, and the same pattern shows up "
                 "again and again.", FadeOut(s3l), FadeOut(rule))
        self.play(t.animate.set_value(2.0), run_time=6.0, rate_func=smooth)
        zoomed.clear_updaters()
        self.hold()
        ya, yb = p(2.2), p(2.23)
        assert 5.5 < (ya - yb) / 0.03 < 6.5
        pair = mt(r"2.20\ \to\ \text{size }" + num(-ya) + r",\qquad 2.23\ \to\ \text{size }" + num(-yb), 34)
        moved = mt(r"\text{in: }0.03\qquad\text{out: }" + num(ya - yb) + r"\ \approx\ 6\times0.03", 34, C_S5)
        # the six is exact at √5: p(√5 + e) = −√5 − 6e − (3√5/2)e² − e³/2
        assert abs(dp(S5) + 6) < 1e-12 and abs(p(S5 + 1e-4) + S5 + 6e-4) < 1e-7
        six = mt(r"p(\sqrt5+e)\ \approx\ -\sqrt5-6\,e", 36, YELLOW_D)
        sixth = mt(r"\text{each stripe}\ \approx\ \tfrac16\ \text{of the one before}", 34)
        sr = VGroup(pair, moved, six, sixth).arrange(DOWN, buff=0.24).move_to([0, -1.95, 0])
        assert abs((S5 - B[5]) / (S5 - B[6]) - 6) < 0.05
        self.say("Why do the stripes get thin so quickly? Near square root of five the folded curve is steep. "
                 "From two point two to two point two three, the start moves by zero point zero three. But "
                 "the size after the step moves from two point zero two to two point two zero, which is zero "
                 "point one eight. That is six times as far. So one step stretches a stripe to about six times "
                 "its width. Where does the six come from? Do what we did at zero and at one. Put square root "
                 "of five plus a small e into p, and drop the terms with e squared and e cubed. Out comes "
                 "minus square root of five, minus six e. So next to square root of five, one step multiplies "
                 "a small distance by six, exactly. And the stretched stripe has to fit onto the stripe before "
                 "it. So each stripe is about a sixth as wide as the one before, and the closer to square root "
                 "of five, the closer to exactly a sixth.")
        self.cue("From two point two to", FadeIn(pair))
        self.cue("That is six times as far", FadeIn(moved))
        self.cue("Out comes minus square root of five", FadeIn(six))
        self.cue("So each stripe is about a sixth", FadeIn(sixth))
        self.hold(0.5)
        self.clear_stage(*self.stay())

    # ------------------------------------------------------------ 11. do the stripes cover the gap? and the edges
    def boundary_points(self):
        # start from the picture of the last scene; a box on its corner grows into the close-up
        wide = self.gap_picture()
        wx = self.gx
        wide_sts = VGroup(*[self.stripe(k) for k in range(1, 8)])
        box = Rectangle(width=wx.c2p(2.26, 0)[0] - wx.c2p(2.05, 0)[0], height=wx.c2p(0, 2.3)[1] - wx.c2p(0, 1.6)[1],
                        color=YELLOW_D, stroke_width=3).move_to((wx.c2p(2.05, 1.6) + wx.c2p(2.26, 2.3)) / 2)
        self.play(FadeIn(wide), FadeIn(wide_sts))
        pic = self.gap_picture(close=True)
        gx = self.gx
        sts = VGroup(*[self.stripe(k) for k in range(1, 8)])
        # the edges as a staircase between the folded curve and the diagonal
        pts = [gx.c2p(self.gbox[0], S3)]
        for k in range(1, 9):
            pts += [gx.c2p(B[k], B[k - 1]), gx.c2p(B[k], B[k])]
        stair = VGroup(*[Line(a, b, color=C_ZERO, stroke_width=3) for a, b in zip(pts, pts[1:])])
        labs = VGroup(mt(r"b_1", 26, C_ZERO).next_to(gx.c2p(B[1], S3), DOWN, buff=0.1),
                      mt(r"b_2", 26, C_ZERO).next_to(gx.c2p(B[2], B[1]), RIGHT, buff=0.1))
        q = fit(txt("is there a piece next to √5 that no stripe reaches?", 24)).move_to([PANEL_X, 2.6, 0])
        # D9: the question, as a statement about the list of edges
        qf = mt(r"\sqrt3,\ b_1,\ b_2,\ \dots\ \ \longrightarrow\ \ \sqrt5\ \ ?", 36, YELLOW_D).move_to([PANEL_X, 2.6, 0])
        self.say("One question is still open. Do the stripes really fill the whole gap? Or is there a last "
                 "piece, right next to square root of five, that no stripe ever reaches? The stripes end at "
                 "the edges. So this is a question about our list of edges, square root of three, b one, b "
                 "two, and so on. Do the edges get all the way up to square root of five? Look at how we found "
                 "them. Here is the corner of the picture next to square root of five. Start at the height "
                 "square root of three, and go across to the folded curve. That is b one. Go up to the "
                 "diagonal, and across to the curve again. That is b two. The edges are a staircase, squeezed "
                 "between the curve and the diagonal.", FadeIn(q))
        self.cue("right next to square root of five", Create(box))
        self.cue("So this is a question about our list", FadeOut(q), FadeIn(qf))
        self.cue("Here is the corner of the picture")
        self.expand(box, VGroup(*pic, sts), keep=[*self.stay(), qf], run_time=1.5)
        self.cue("and go across to the folded curve", Create(stair[0]), FadeIn(labs[0]))
        self.cue("Go up to the diagonal", Create(stair[1]), Create(stair[2]), FadeIn(labs[1]))
        self.cue("The edges are a staircase", self.draw(stair[3:], 0.3))
        self.hold(1.2)

        # D10-D14: bounded, increasing, so the edges settle at some L; and L can only be √5
        assert all(B[k] < B[k + 1] < S5 for k in range(12)) and abs((S5 ** 2 - 3) / 2 - 1) < 1e-12
        top = Dot(gx.c2p(S5, S5), radius=0.08, color=C_S5)
        top_l = mt(r"\sqrt5", 28, C_S5).next_to(top, RIGHT, buff=0.12)
        f1 = mt(r"b_n<\sqrt5\ \ \Longrightarrow\ \ b_{n+1}<\sqrt5", 36)
        f2 = mt(r"b_n=|p(b_{n+1})|<b_{n+1}", 36)
        f3 = mt(r"\sqrt3<b_1<b_2<\cdots<\sqrt5", 36)
        f4 = mt(r"b_n\ \longrightarrow\ L", 36, YELLOW_D)
        steps = VGroup(f1, f2, f3, f4).arrange(DOWN, buff=0.42).next_to(qf, DOWN, buff=0.55)
        g1 = mt(r"|p(L)|=L", 36)
        g2 = mt(r"\frac{L^2-3}{2}=1\ \ \Longrightarrow\ \ L^2=5", 36)
        g3 = mt(r"L=\sqrt5", 44, C_S5)
        g0 = mt(r"|p(b_{n+1})|=b_n", 36)
        ga = fit(mt(r"b_{n+1}\to L\ \ \Longrightarrow\ \ |p(b_{n+1})|\to|p(L)|", 36))
        lim = VGroup(g0, ga, g1, g2, g3).arrange(DOWN, buff=0.3).next_to(qf, DOWN, buff=0.5)
        done = fit(mt(r"(\sqrt3,\ \sqrt5)\ =\ \text{all the stripes together}", 36, C_PLUS)).next_to(lim, DOWN, buff=0.4)
        self.say("First, can an edge ever reach square root of five? The folded curve only goes up, and it gets "
                 "to the height square root of five only at the very end of the gap. Each new edge is where "
                 "the curve reaches the height of the edge before. If that height is below square root of "
                 "five, the curve reaches it before the end of the gap. So the new edge is below square root "
                 "of five as well. The list starts at square root of three, which is below. So every edge "
                 "stays below square root of five. Next, does the list always go up? One step takes each edge "
                 "to the size of the edge before it. Every edge is in the gap, and in the gap a step makes the "
                 "size smaller. So the edge before is the smaller one. Each edge is bigger than the last. So "
                 "the edges keep rising, and they can never pass square root of five. A list of numbers that "
                 "only rises, under a ceiling it cannot pass, has to settle toward some value. Call that value "
                 "L. Where is L? Far down the list, an edge and the one after it are both as close to L as we "
                 "like. One step takes the later one to the size of the earlier one. Now p is a polynomial, so "
                 "a tiny change in the input makes only a tiny change in the output. So one step from L itself "
                 "lands as close as we like to a value of size L. And a fixed number that is as close as we "
                 "like to L can only be L. So one step takes L to a value of the same size, L. That means the size factor at L is exactly one. We have met "
                 "that before. L squared minus three, over two, equals one, so L squared is five. L is square "
                 "root of five. On the picture, that is where the folded curve meets the diagonal. So the "
                 "edges come as close to square root of five as we like. Every start below square root of five "
                 "is passed by some edge, so it lies in some stripe. The stripes fill the whole gap. We now "
                 "know where every start in the gap ends up.")
        self.cue("only at the very end of the gap", GrowFromCenter(top), FadeIn(top_l))
        self.cue("So the new edge is below", FadeIn(f1))
        self.cue("So the edge before is the smaller one", FadeIn(f2))
        self.cue("So the edges keep rising", FadeIn(f3))
        self.cue("Call that value L", FadeIn(f4))
        self.cue("Where is L?", FadeOut(VGroup(f1, f2, f3)), f4.animate.move_to(qf), FadeOut(qf))
        self.cue("One step takes the later one", FadeIn(g0))
        self.cue("Now p is a polynomial", FadeIn(ga))
        self.cue("So one step takes L", FadeIn(g1))
        self.cue("That means the size factor at L", Indicate(self.sizeline[4], color=YELLOW_D, scale_factor=1.25))
        self.cue("L squared minus three, over two", FadeIn(g2))
        self.cue("L is square root of five", FadeIn(g3), Flash(top, color=C_S5))
        self.cue("that is where the folded curve meets", Indicate(top, color=C_S5, scale_factor=1.8))
        self.cue("The stripes fill the whole gap", Indicate(sts, color=WHITE, scale_factor=1.0), FadeIn(done))
        self.hold(1.2)
        self.clear_stage(*self.stay())

        # the edges themselves: ±√3 after a few steps, then 0
        rows, dots, names, chains = VGroup(), VGroup(), VGroup(), VGroup()
        paths = []
        for i, n in enumerate((1, 2, 3)):
            row = self.number_row(1.7 - 1.55 * i, lo=-2.4, hi=2.4, length=7.4, x=-1.3, marks=(0,))
            nl = row[0]
            for v in (S3, -S3):
                row.add(Line(nl.n2p(v) + DOWN * 0.1, nl.n2p(v) + UP * 0.1, color=C_ZERO, stroke_width=4))
                row.add(mt(r"\sqrt3" if v > 0 else r"-\sqrt3", 22, C_ZERO).next_to(nl.n2p(v), DOWN, buff=0.14))
            rows.add(row)
            names.add(mt(f"b_{{{n}}}", 34, C_ZERO).next_to(nl, LEFT, buff=0.35))
            path = [(+1, n)]
            s = 1
            for k in range(n - 1, -1, -1):
                s = -s
                path.append((s, k))
            vals = [sg * B[k] for sg, k in path] + [0.0]
            assert all(abs(p(a) - b) < 1e-9 for a, b in zip(vals, vals[1:]))
            paths.append(vals)
            terms = [("-" if sg < 0 else "") + (r"\sqrt3" if k == 0 else f"b_{{{k}}}") for sg, k in path] + ["0"]
            chains.add(mt(r"\to ".join(terms), 24, C_ZERO).next_to(nl, RIGHT, buff=0.3))
            dots.add(Dot(nl.n2p(vals[0]), radius=0.09, color=C_ZERO))
        self.say("And what about the edges themselves? Take b one. Its first step lands exactly on minus "
                 "square root of three. And we know what happens at square root of three. The next step gives "
                 "exactly zero, and by the mirror rule the same holds for minus square root of three. So b one "
                 "ends on zero, and stays there.",
                 FadeIn(rows[0]), FadeIn(names[0]), GrowFromCenter(dots[0]))
        nl = rows[0][0]
        self.cue("Its first step lands", self.hop(dots[0], nl, paths[0][0], paths[0][1], C_ZERO), run_time=1.2)
        self.cue("The next step gives", self.hop(dots[0], nl, paths[0][1], paths[0][2], C_ZERO), run_time=1.2)
        self.cue("So b one ends on zero", FadeIn(chains[0]))
        self.hold()
        self.say("b two lands on minus b one, and from there it follows the path of b one with the sign "
                 "flipped. So it takes one step more. And b three takes one step more again. Every edge reaches "
                 "plus or minus square root of three after a few steps, and then it sits on zero forever. "
                 "An edge never reaches one or minus one.",
                 FadeIn(rows[1:]), FadeIn(names[1:]), *[GrowFromCenter(d) for d in dots[1:]])
        for j in range(max(len(q_) for q_ in paths[1:]) - 1):
            anims = []
            for i in (1, 2):
                if j + 1 < len(paths[i]):
                    anims.append(self.hop(dots[i], rows[i][0], paths[i][j], paths[i][j + 1], C_ZERO))
            self.play(*anims, run_time=1.2)
            self.wait(0.6)
        self.play(FadeIn(chains[1:]))
        self.hold()
        ends = [fate(B[1] - 0.01)[0], fate(B[1] + 0.01)[0]]
        assert sorted(ends) == [-1.0, 1.0]
        nudged = VGroup(*[Dot(nl.n2p(B[1] + dx), radius=0.07, color=sign_color(e))
                          for dx, e in zip((-0.01, 0.01), ends)])
        self.say("Should that worry us? Not much. Each edge is a single point, and zero is the top of the "
                 "hill. Move the start by the tiniest amount, and it is inside a stripe on one side or the "
                 "other, and it rolls down to plus one or minus one.")
        self.cue("Move the start by", FadeOut(dots[0]), *[GrowFromCenter(d) for d in nudged])
        self.play(*[d.animate(path_arc=0.5 * PI).move_to(nl.n2p(e)) for d, e in zip(nudged, ends)],
                  run_time=2.0)
        self.hold(0.5)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 12. the answer to (e)
    def summary(self):
        head = [txt("start σ", 26, GREY_B), txt("what happens", 26, GREY_B), txt("ends at", 26, GREY_B)]
        rows = [
            (mt(r"0<\sigma<\sqrt3", 34), txt("first step lands in (0, 1], then climbs", 26), mt(r"+1", 34, C_PLUS)),
            (mt(r"\sigma=\sqrt3", 34), txt("lands on 0 in one step", 26), mt(r"0", 34, C_ZERO)),
            (mt(r"b_{n-1}<\sigma<b_n\ \ {\scriptstyle(b_0=\sqrt3)}", 34), txt("n flips while shrinking", 26), mt(r"(-1)^n", 34, YELLOW_D)),
            (mt(r"\sigma=b_n", 34), txt("hits ±√3, then 0", 26), mt(r"0", 34, C_ZERO)),
            (mt(r"\sigma=\sqrt5", 34), txt("jumps between ±√5", 26), txt("period 2", 26, C_S5)),
            (mt(r"\sigma>\sqrt5", 34), txt("flips while growing", 26), txt("explodes", 26, C_S5)),
        ]
        xs = (-3.9, 0.7, 4.6)
        table = VGroup()
        for r, cells in enumerate([head] + rows):
            y = 2.75 - 0.66 * r
            table.add(VGroup(*[c.move_to([x, y, 0]) for c, x in zip(cells, xs)]))
        rule = Line([-6.2, 2.42, 0], [6.2, 2.42, 0], color=GREY_C, stroke_width=1.5)
        bar = self.basin_bar(2.0, n=8).shift(DOWN * 2.75)
        self.say("Now we can answer the question we started with. Where does a positive sigma end up when we "
                 "apply p again and again? Here is the full answer to part (e), from left to right along the "
                 "number line.")
        self.cue("Here is the full answer", FadeIn(table[0]), Create(rule))
        self.hold()
        self.say("Below square root of three, the first step lands between zero and one, and from there sigma "
                 "climbs to plus one. Exactly at square root of three, it lands on zero and stays there.", FadeIn(table[1], shift=UP * 0.1))
        self.cue("Exactly at square root of three", FadeIn(table[2], shift=UP * 0.1))
        self.hold()
        self.say("Between square root of three and square root of five, each step flips the sign and shrinks "
                 "the size, until the value is inside square root of three. An odd number of flips ends at "
                 "minus one, and an even number ends at plus one. That gives the stripes. Their edges are "
                 "single points that end on zero.", FadeIn(table[3][:2], shift=UP * 0.1))
        self.cue("An odd number of flips", FadeIn(table[3][2]))
        self.cue("That gives the stripes", FadeIn(bar))
        self.cue("Their edges are single points", FadeIn(table[4], shift=UP * 0.1))
        self.hold()
        want = SurroundingRectangle(table[1], color=C_PLUS, buff=0.14, stroke_width=3)
        self.say("Exactly at square root of five, sigma jumps between plus and minus square root of five "
                 "forever. And beyond square root of five, each step flips and grows, so it explodes. Out of "
                 "all these cases, only the first one is what we wanted.", FadeIn(table[5], shift=UP * 0.1))
        self.cue("And beyond square root of five", FadeIn(table[6], shift=UP * 0.1))
        self.cue("only the first one is what we wanted", Create(want))
        self.hold(0.8)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 13. back to the matrix
    def back_to_matrix(self):
        sig0 = [2.9, 1.6, 0.9, 0.35]
        nl = NumberLine(x_range=[0, 3.2, 0.5], length=11.0, color=GREY_B, stroke_width=2,
                        include_tip=False, tick_size=0.04).move_to([0.3, -0.6, 0])
        marks = VGroup()
        for v, c, s in ((0, GREY_B, "0"), (1, C_PLUS, "1"), (S3, C_ZERO, r"\sqrt3"), (S5, C_S5, r"\sqrt5")):
            marks.add(Line(nl.n2p(v) + DOWN * 0.12, nl.n2p(v) + UP * 0.12, color=c, stroke_width=4))
            marks.add(mt(s, 28, c).next_to(nl.n2p(v), DOWN, buff=0.2))
        lab = mt(r"\sigma_i", 32, C_SIG).next_to(nl, LEFT, buff=0.3)
        dots = VGroup(*[Dot(nl.n2p(s), radius=0.1, color=C_SIG) for s in sig0])
        safe = Line(nl.n2p(0), nl.n2p(S3), color=C_PLUS, stroke_width=8).set_opacity(0.45)
        self.say("We wanted every singular value to end at one, and that only happens for starts below square "
                 "root of three. But a real W can have singular values anywhere, some of them far above square"
                 " root of five.", Create(nl), FadeIn(marks), FadeIn(lab))
        self.cue("that only happens for starts below", Create(safe))
        self.cue("But a real W can have", LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.3))
        self.hold()
        bad = SurroundingRectangle(dots[0], color=C_S5, buff=0.12)
        blow = mt(r"2.9\to" + num(p(2.9)) + r"\to\cdots", 32, C_S5).next_to(dots[0], UP, buff=0.35)
        sc = mt(r"\frac{W}{c}=U\,\frac{\Sigma}{c}\,V^{\top}", 44).move_to([0, 2.4, 0])
        same = txt("U and Vᵀ unchanged, every σ divided by c", 26, C_PLUS).next_to(sc, DOWN, buff=0.35)
        self.say("This one, at two point nine, would explode. And one that sits in a gold stripe would end at "
                 "minus one, with its direction reversed. So before we iterate, we have to bring every "
                 "singular value down. That is easy to do. Divide W by a number, and every singular value is "
                 "divided by that number, while U and V transpose stay exactly the same. Our target, U times V"
                 " transpose, does not change at all.", Create(bad), FadeIn(blow))
        self.cue("we have to bring every singular value down", FadeOut(VGroup(bad, blow)))
        self.cue("Divide W by a number", FadeIn(sc))
        self.cue("while U and V transpose stay", FadeIn(same))
        self.hold()

        fro = math.sqrt(sum(s * s for s in sig0))
        sig1 = [s / fro for s in sig0]
        assert max(sig1) < 1 < S3 and num(fro) == "3.45" and num(sig1[0]) == "0.84"
        ideal = mt(r"c=\sigma_{\max}\ ?\qquad\text{needs the SVD}", 36, C_S5).move_to([1.5, 2.5, 0])
        fdef = mt(r"\|W\|_F=\sqrt{\textstyle\sum_{i,j}w_{ij}^2}", 38).move_to([1.5, 2.65, 0])
        # rotations keep the length of every column (U) and of every row (Vᵀ), so they keep the sum of squares
        frot = MathTex(r"\|U\,\Sigma\,V^{\top}\|_F^2", r"=\|\Sigma\,V^{\top}\|_F^2", r"=\|\Sigma\|_F^2", font_size=36)
        frot.move_to([1.5, 1.85, 0])
        assert abs(sum(x * x for x in sig0) - fro ** 2) < 1e-12
        fsum = mt(r"\textstyle\sum_{i,j}w_{ij}^2=\sum_i\sigma_i^2\ \ge\ \sigma_{\max}^2", 36).move_to([1.5, 1.1, 0])
        fge = mt(r"\|W\|_F\ \ge\ \sigma_{\max}", 40, C_PLUS).move_to([1.5, 0.35, 0])
        self.say("Which number? Dividing by the largest singular value would be ideal, because then everything"
                 " is at one or below. But finding the largest singular value takes the very SVD we are trying"
                 " to avoid. There is a cheap stand-in, called the Frobenius norm. Square every entry of W, "
                 "add them all up, and take the square root. That only needs the entries, so it costs almost "
                 "nothing. And it is big enough. Here is why. The sum of the squared entries of a matrix is the "
                 "sum of the squared lengths of its columns. A rotation on the left turns every column without "
                 "changing its length, so that sum stays the same. A rotation on the right does the same to "
                 "the rows. So W, which is U, sigma, V transpose, has the same sum as sigma alone. And sigma "
                 "holds only the singular values, so the sum of the squared entries equals the sum of the "
                 "squared singular values. That sum already contains the largest one squared, plus more. So "
                 "its square root, the Frobenius norm, is never smaller than the largest singular value.", FadeOut(same), sc.animate.scale(0.8).move_to([-4.3, 2.6, 0]))
        self.cue("Dividing by the largest singular value", FadeIn(ideal[0][:7]))
        self.cue("But finding the largest singular value", FadeIn(ideal[0][7:]))
        self.cue("There is a cheap stand-in", FadeOut(ideal), FadeIn(fdef))
        self.cue("A rotation on the left", FadeIn(frot[0]), FadeIn(frot[1]))
        self.cue("A rotation on the right", FadeIn(frot[2]))
        self.cue("so the sum of the squared entries equals", FadeIn(fsum[0][:15]))
        self.cue("That sum already contains", FadeIn(fsum[0][15:]))
        self.cue("So its square root", FadeIn(fge))
        self.hold()
        fro_eq = mt(r"\|W\|_F=\sqrt{2.9^2+1.6^2+0.9^2+0.35^2}\approx" + num(fro), 36).move_to([1.5, 2.5, 0])
        self.say("Here the Frobenius norm comes out to about three point four five, a bit more than our "
                 "largest singular value, two point nine. Divide every sigma by it.", FadeOut(VGroup(fdef, frot, fsum)), fge.animate.move_to([1.5, 1.6, 0]), FadeIn(fro_eq))
        self.hold()
        div = mt(r"2.9\,/\,3.45=0.84", 36, C_SIG).move_to([1.5, 0.8, 0])
        self.say("Two point nine becomes zero point eight four, and the others are smaller still. Now every "
                 "singular value sits between zero and one, safely below square root of three.", *[d.animate.move_to(nl.n2p(s)) for d, s in zip(dots, sig1)], FadeIn(div), run_time=2.0)
        self.hold()
        steps = 8
        orbs = [orbit(s, steps) for s in sig1]
        assert all(abs(o[-1] - 1) < 0.01 for o in orbs)
        step = mt(r"W\ \leftarrow\ \tfrac32\,W-\tfrac12\,W\,W^{\top}W", 44).move_to([0, 2.6, 0])
        each = mt(r"\sigma_i\ \leftarrow\ p(\sigma_i)", 38, C_SIG).next_to(step, DOWN, buff=0.35)
        k_lab = mt(r"k=0", 34).move_to([-4.6, 0.6, 0])
        res = mt(r"\Sigma\to I,\qquad W\to UV^{\top}", 42, C_PLUS).move_to([0, 0.9, 0])
        self.say("Now apply our matrix step, three halves W, minus one half W, W transpose, W, again and "
                 "again. It needs nothing but matrix products. And each time, every singular value goes "
                 "through p once. So each singular value climbs to plus one. The small ones start slowly, "
                 "growing by about one and a half times per step as zero point one did, but they all arrive. "
                 "The one exception is a singular value of exactly zero. Zero is a fixed point, so it stays "
                 "at zero. And all along, U and V transpose never changed. So when no singular value is zero, "
                 "the middle is now all ones, and W has become U times V transpose.",
                 FadeOut(VGroup(sc, fro_eq, fge, div)), FadeIn(step))
        self.cue("And each time, every singular value", FadeIn(each), FadeIn(k_lab))
        self.cue("So each singular value climbs")
        for k in range(1, steps + 1):
            new_k = mt(f"k={k}", 34).move_to(k_lab, aligned_edge=LEFT)
            self.play(*[d.animate.move_to(nl.n2p(o[k])).set_color(C_PLUS if abs(o[k] - 1) < 0.02 else C_SIG)
                        for d, o in zip(dots, orbs)], Transform(k_lab, new_k), run_time=1.0)
        self.cue("the middle is now all ones", FadeIn(res))
        self.hold()
        ell = Ellipse(width=3.4, height=1.3, color=C_SIG, stroke_width=4).rotate(30 * DEGREES).move_to([0, 1.6, 0])
        circ = Circle(radius=1.0, color=C_PLUS, stroke_width=4).move_to([0, 1.6, 0])
        self.say("The ellipse has become a circle. All it took was matrix products, and a cubic built from two"
                 " simple wishes.", FadeOut(VGroup(step, each, res, k_lab)), FadeIn(ell))
        self.play(Transform(ell, circ), run_time=2.0)
        self.hold(0.8)
        # leave only the circle (and the corner formula): closing() picks it up from here
        self.clear_stage(self.corner, ell)
        self.final_circle = ell

    def closing(self):
        """Under the finished circle: the method in two lines, then the title's question, answered."""
        circ = getattr(self, "final_circle", None)
        if circ is None:    # rendered on its own: put up what back_to_matrix leaves behind
            circ = Circle(radius=1.0, color=C_PLUS, stroke_width=4).move_to([0, 1.6, 0])
            self.add(circ)
        r1 = mt(r"W\ \leftarrow\ W\,/\,\|W\|_F", 40)
        r2 = mt(r"W\ \leftarrow\ \tfrac32\,W-\tfrac12\,W\,W^{\top}W", 40)
        rows = VGroup(r1, r2).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([-0.9, -0.75, 0])
        n1 = txt("once", 24, GREY_B).next_to(r1, RIGHT, buff=0.6)
        n2 = txt("again and again", 24, GREY_B).next_to(r2, RIGHT, buff=0.6)
        self.say("So the whole method is two lines. Divide W by its Frobenius norm, once. "
                 "Then apply the step, again and again.")
        self.cue("Divide W by its Frobenius norm", FadeIn(r1, shift=UP * 0.1), FadeIn(n1))
        self.cue("Then apply the step", FadeIn(r2, shift=UP * 0.1), FadeIn(n2))
        self.hold()
        ans = txt("every singular value goes to 1", 34, C_PLUS).move_to([0, -2.45, 0])
        tag = txt(series_name(), 24, GREY_B).to_edge(DOWN, buff=0.4)
        self.say("And where does a singular value go? After that first division, every one of them "
                 "goes to one.")
        self.cue("every one of them", FadeIn(ans, shift=UP * 0.15), Indicate(circ, color=C_PLUS, scale_factor=1.06))
        self.hold(1.2)
        self.uncaption()
        self.play(FadeIn(tag), run_time=0.6)
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.5)
