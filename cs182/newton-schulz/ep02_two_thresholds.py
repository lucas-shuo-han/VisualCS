"""Newton–Schulz, episode 2: iterate p on one number. Fixed points, the cobweb, and the thresholds √3 and √5."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ns_common import *  # noqa: E402,F403
from ns_common import _root  # noqa: E402,F401


class Ep02TwoThresholds(NSScene):
    SCENES = ["ep2_recap", "try_numbers", "cobweb", "slopes", "how_big", "too_big"]
    CHAIN = ["cobweb", "slopes", "how_big", "too_big"]     # these four draw on one graph
    CORNER_FROM = "ep2_recap"
    ASK = "Where does a singular value go?"
    ASK_SAY = "Where does a singular value go?"

    # ------------------------------------------------------------ 0. what episode 1 gave us
    def ep2_recap(self):
        step = mt(r"W\ \leftarrow\ \tfrac32\,W-\tfrac12\,W\,W^{\top}W", 44).move_to([0, 1.9, 0])
        px = MathTex(r"p(\sigma)", r"=", r"\tfrac32\,\sigma-\tfrac12\,\sigma^3", font_size=52)
        px[2].set_color(C_P)
        px.move_to([0, 0.5, 0])
        wishes = mt(r"p(1)=1\qquad\qquad p(1+e)\approx1", 36, C_PLUS).move_to([0, -0.8, 0])
        q = mt(r"\sigma\;\to\;p(\sigma)\;\to\;p(p(\sigma))\;\to\;\cdots\;\to\;?", 44, C_SIG).move_to([0, -2.1, 0])
        self.say("Last time we built one step out of nothing but matrix products. Three halves W, minus one "
                 "half W, W transpose, W. On each singular value, that step is a polynomial. p of sigma is "
                 "three halves sigma, minus one half sigma cubed. We chose it so that one stays at one, and a "
                 "value close to one moves closer. But a real sigma can start anywhere.")
        self.cue("Three halves W", FadeIn(step))
        self.cue("p of sigma is three halves sigma", FadeIn(px))
        self.cue("We chose it so that", FadeIn(wishes))
        self.cue("But a real sigma", FadeIn(q, shift=UP * 0.2))
        self.hold(0.6)
        corner = self.make_corner()
        self.play(FadeOut(VGroup(step, wishes, q)), ReplacementTransform(px, corner))

    # ------------------------------------------------------------ 3. just try some numbers
    def try_numbers(self):
        def chain(x0, n):
            """x0 → p(x0) → …, one mobject per term, so each can appear when it is said."""
            o = orbit(x0, n)
            assert abs(o[-1] - 1) < 0.003
            terms = [num(x0, 1)] + [r"\to " + num(v, 3 if 0.995 <= v < 0.9995 else 2) for v in o[1:]]
            return VGroup(*[mt(s, 34) for s in terms], mt(r"\to\cdots\to 1", 34, C_PLUS)).arrange(RIGHT, buff=0.14)

        lines = VGroup(chain(0.5, 4), chain(1.3, 3), chain(0.1, 8))
        lines.arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(UP * 1.2).to_edge(LEFT, buff=0.8)
        if lines.width > 12.4:
            lines.scale_to_fit_width(12.4).to_edge(LEFT, buff=0.8)
        assert abs(1.5 * 0.5 - 0.75) < 1e-12 and 0.5 ** 3 == 0.125 and p(0.5) == 0.6875
        calc = VGroup(mt(r"\tfrac32\cdot0.5=0.75", 38), mt(r"0.5^3=0.125", 38),
                      mt(r"\tfrac12\cdot0.125=0.0625", 38)).arrange(RIGHT, buff=0.9).move_to(DOWN * 0.6)
        res = mt(r"p(0.5)=0.75-0.0625=0.6875", 40, C_P).move_to(DOWN * 1.7)
        self.say("Where does a sigma end up? No theory yet. Let's just pick a number and try it, say zero "
                 "point five.")
        self.cue("say zero point five", FadeIn(lines[0][0]))
        self.say("One step of p takes three halves of the number, and subtracts one half of its cube. Three "
                 "halves of zero point five is zero point seven five. Zero point five cubed is zero point one "
                 "two five, and half of that is zero point zero six two five. Subtract, and we get zero point "
                 "six eight seven five.")
        self.cue("Three halves of zero point five", FadeIn(calc[0]))
        self.cue("Zero point five cubed", FadeIn(calc[1]))
        self.cue("and half of that", FadeIn(calc[2]))
        self.cue("Subtract", FadeIn(res))
        self.hold()
        self.say("Now feed that result back in, and keep going. Zero point six nine becomes zero point eight "
                 "seven, then zero point nine eight, then zero point nine nine nine. It is closing in on one.", FadeOut(calc), FadeOut(res), FadeIn(lines[0][1]))
        self.cue("becomes zero point eight seven", FadeIn(lines[0][2]))
        self.cue("then zero point nine eight", FadeIn(lines[0][3]))
        self.cue("then zero point nine nine nine", FadeIn(lines[0][4]))
        self.cue("It is closing in on one", FadeIn(lines[0][5]))
        self.say("That start was below one. Now try one above it. One point three drops to zero point eight "
                 "five, which is below one, and then it climbs, to zero point nine seven, and then zero point "
                 "nine nine eight. It also closes in on one.")
        self.cue("One point three drops", FadeIn(lines[1][0]), FadeIn(lines[1][1]))
        self.cue("to zero point nine seven", FadeIn(lines[1][2]))
        self.cue("and then zero point nine nine eight", FadeIn(lines[1][3]))
        self.cue("It also closes in", FadeIn(lines[1][4]))
        self.say("Both of those were fairly close to one. So try a start that is far away, down near zero. "
                 "Zero point one becomes zero point one five, then zero point two two, then zero point three "
                 "three. It is slow at first, but it keeps climbing, and after eight steps it also reaches "
                 "one.")
        self.cue("Zero point one becomes", FadeIn(lines[2][0]), FadeIn(lines[2][1]))
        self.cue("then zero point two two", FadeIn(lines[2][2]))
        self.cue("then zero point three three", FadeIn(lines[2][3]))
        self.cue("but it keeps climbing", LaggedStart(*[FadeIn(m) for m in lines[2][4:9]], lag_ratio=0.5),
                 run_time=2.5)
        self.cue("it also reaches one", FadeIn(lines[2][9]))
        self.hold()
        p1 = mt(r"p(1)=\tfrac32-\tfrac12=1", 40, C_PLUS).move_to([-2.6, -1.6, 0])
        self.say("All three starts end at one. And once a value is at one, it stays there. Three halves minus "
                 "one half is one, so p of one equals one. That is our first wish at work.", *[Indicate(l[-1], color=C_PLUS) for l in lines])
        self.cue("Three halves minus one half", FadeIn(p1))
        self.hold()
        p0 = mt(r"p(0)=\tfrac32\cdot0-\tfrac12\cdot0^3=0", 40, C_ZERO).move_to([2.8, -1.6, 0])
        fp = VGroup(txt("fixed point:", 30), mt(r"p(x)=x", 42)).arrange(RIGHT, buff=0.3).move_to(UP * 1.6)
        self.say("But if some other number also stayed put, a sigma could get stuck there and never reach one."
                 " Is there such a number? Try zero. Three halves of zero is zero, and zero cubed is zero, so "
                 "p of zero is zero. Zero stays put as well. From here on, call the input x. A value where p "
                 "of x equals x is called a fixed point. We have found two of them. Are there any more?")
        self.cue("Try zero", FadeIn(p0))
        self.cue("From here on, call the input x", FadeOut(lines), FadeIn(fp))
        self.cue("We have found two of them", Indicate(p1, color=C_PLUS), Indicate(p0, color=C_ZERO))
        self.hold()

        der = VGroup(mt(r"p(x)=x", 40),
                     mt(r"\tfrac32x-\tfrac12x^3=x", 40),
                     mt(r"\tfrac12x-\tfrac12x^3=0", 40),
                     mt(r"\tfrac12\,x\,(1-x^2)=0", 40),
                     mt(r"\tfrac12\,x\,(1-x)(1+x)=0", 40),
                     mt(r"x=0,\ \ x=1,\ \ x=-1", 42, C_PLUS)).arrange(DOWN, buff=0.33).move_to(UP * 0.5)
        self.say("To find them all at once, write down p of x equals x. That is three halves x, minus one half"
                 " x cubed, equals x. Subtract x from both sides, and we get one half x, minus one half x "
                 "cubed, equals zero.", FadeOut(VGroup(p1, p0, fp)))
        self.cue("write down p of x equals x", FadeIn(der[0]))
        self.cue("That is three halves x", FadeIn(der[1]))
        self.cue("Subtract x from both sides", FadeIn(der[2]))
        self.say("Both terms contain one half x, so pull it out. What is left inside is one minus x squared. "
                 "And one minus x squared splits into one minus x, times one plus x. So the equation says one "
                 "half x, times one minus x, times one plus x, equals zero.")
        self.cue("so pull it out", FadeIn(der[3]))
        self.cue("splits into", FadeIn(der[4]))
        self.hold()
        chk = mt(r"p(-1)=-\tfrac32+\tfrac12=-1", 36, C_MINUS).next_to(der, DOWN, buff=0.4)
        self.say("A product is zero only if one of its factors is zero. So x is zero, or x is one, or x is "
                 "minus one. Those are all the fixed points there are, the two we found and a new one. And "
                 "minus one does check out. Minus three halves, plus one half, is minus one. A singular value "
                 "is never negative, so for now minus one is just a point on the list.")
        self.cue("So x is zero", FadeIn(der[5]))
        self.cue("And minus one does check out", FadeIn(chk))
        self.hold()
        again = chain(0.1, 8)
        again.move_to(DOWN * 0.2)
        if again.width > 12.4:
            again.scale_to_fit_width(12.4)
        stuck = mt(r"0\to 0\to 0\to\cdots", 36, C_ZERO).next_to(again, UP, buff=0.6)
        self.say("But zero matters right away. A sigma at exactly zero is stuck. And yet zero point one, right"
                 " next to zero, walked away from it, all the way to one. Why would one fixed point pull "
                 "values in and another push them away? To see what happens around each of them, we need a "
                 "picture of the iteration.", FadeOut(VGroup(der, chk)))
        self.cue("A sigma at exactly zero", FadeIn(stuck))
        self.cue("And yet zero point one", FadeIn(again))
        self.hold()
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ 4. the graph and the cobweb
    def cobweb(self):
        g = self.make_graph()
        ax, curve, diag = self.ax, self.curve, self.diag
        known = VGroup(Dot(ax.c2p(0, 0), radius=0.07, color=WHITE), Dot(ax.c2p(1, 1), radius=0.07, color=WHITE))
        guide = VGroup(DashedLine(ax.c2p(1, 0), ax.c2p(1, 1), color=GREY_B, dash_length=0.05),
                       DashedLine(ax.c2p(0, 1), ax.c2p(1, 1), color=GREY_B, dash_length=0.05))
        io = VGroup(txt("along the bottom: the input x", 24), txt("height of the curve: the output p(x)", 24, C_P))
        io.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([PANEL_X, 1.8, 0])
        self.say("Start with the graph of p. Along the bottom is the input x, and the height of the curve "
                 "above it is the output, p of x. We know a few points already. At zero the height is zero, "
                 "and at one the height is one. The curve rises from zero, reaches a hump at one, and comes "
                 "back down after it.", Create(ax), FadeIn(g[1]), Create(curve), FadeIn(g[4]), run_time=2.0)
        self.cue("Along the bottom", FadeIn(io[0]))
        self.cue("and the height of the curve", FadeIn(io[1]))
        self.cue("At zero the height is zero", GrowFromCenter(known[0]))
        self.cue("and at one the height is one", Create(guide), GrowFromCenter(known[1]))
        self.hold()

        w = self.web(0.3, 8, WHITE)
        m = self.start_mark(0.3, WHITE)
        y1 = p(0.3)
        assert abs(y1 - 0.44) < 0.005 and abs(p(y1) - 0.61) < 0.005
        pt1 = Dot(ax.c2p(0.3, y1), radius=0.06, color=WHITE)
        pl1 = mt(r"p(0.3)\approx" + num(y1), 36).move_to([PANEL_X, 1.9, 0])
        self.say("On this picture, one step of the iteration looks like this. Start at x equals zero point "
                 "three on the bottom axis, and go straight up to the curve. The height you reach is p of zero"
                 " point three, about zero point four four.", FadeOut(VGroup(known, guide, io)))
        self.cue("Start at x equals zero point three", FadeIn(m))
        self.cue("and go straight up to the curve", Create(w[0]))
        self.cue("The height you reach", GrowFromCenter(pt1), FadeIn(pl1))
        self.hold()
        hgt = DashedLine(ax.c2p(0.3, y1), ax.c2p(0, y1), color=YELLOW_D, dash_length=0.05)
        hl = mt(num(y1), 24, YELLOW_D).next_to(ax.c2p(0, y1), LEFT, buff=0.1)
        ask = VGroup(txt("a height", 26, YELLOW_D), mt(r"\longrightarrow", 34), txt("a position ?", 26))
        ask.arrange(RIGHT, buff=0.3).next_to(pl1, DOWN, buff=0.6)
        self.say("For the next step, zero point four four has to become the new input. But right now it is a "
                 "height, and inputs are measured along the bottom. We need a way to turn a height into a "
                 "position.")
        self.cue("But right now it is a height", Create(hgt), FadeIn(hl))
        self.cue("We need a way", FadeIn(ask))
        self.hold()
        pt2 = Dot(ax.c2p(y1, y1), radius=0.06, color=WHITE)
        drop = DashedLine(ax.c2p(y1, y1), ax.c2p(y1, 0), color=YELLOW_D, dash_length=0.05)
        dl = mt(num(y1), 24, YELLOW_D).next_to(ax.c2p(y1, 0), DOWN, buff=0.1)
        on_d = mt(r"\text{on the diagonal: }(" + num(y1) + r",\ " + num(y1) + ")", 32).move_to(ask)
        self.say("Here is a line that does exactly that, the diagonal y equals x. Every point on it is as far "
                 "to the right as it is high. So go sideways from the curve until you hit the diagonal. You "
                 "are still at height zero point four four, and now you are also above x equals zero point "
                 "four four.", FadeOut(ask))
        self.cue("the diagonal y equals x", Create(diag), FadeIn(g[5]))
        self.cue("So go sideways from the curve", Create(w[1]), GrowFromCenter(pt2))
        self.cue("You are still at height", FadeIn(on_d))
        self.cue("and now you are also above", Create(drop), FadeIn(dl))
        self.hold()
        seq = mt(r"0.3\to " + r"\to ".join(num(v) for v in orbit(0.3, 4)[1:]) + r"\to\cdots\to 1", 32)
        seq.move_to([PANEL_X, 1.9, 0])
        if seq.width > 6.2:
            seq.scale_to_fit_width(6.2)
        self.say("From there, the second step is the same move. Go straight up to the curve, which gives zero "
                 "point six one, and sideways to the diagonal again. Keep repeating, and the path climbs like "
                 "a staircase, zero point eight, zero point nine five, and into one.", FadeOut(VGroup(pt1, pl1, pt2, on_d, drop, dl, hgt, hl)), FadeIn(seq))
        self.cue("Go straight up to the curve", Create(w[2]))
        self.cue("and sideways to the diagonal again", Create(w[3]))
        self.cue("Keep repeating", self.draw(w[4:], 0.3))
        self.hold()
        w2 = self.web(1.2, 5, WHITE)
        m2 = self.start_mark(1.2, WHITE)
        assert abs(p(1.2) - 0.94) < 0.005
        seq2 = mt(r"1.2\to " + num(p(1.2)) + r"\to\cdots\to 1", 32).move_to(seq)
        self.say("Now a start above one. From one point two, the curve is below the diagonal, so the first "
                 "move goes down, to zero point nine four. After that the path climbs the last little bit and "
                 "settles on one as well.", FadeOut(VGroup(w, m, seq)), FadeIn(m2))
        self.cue("so the first move goes down", Create(w2[0]), FadeIn(seq2))
        self.cue("After that the path climbs", self.draw(w2[1:], 0.4))
        self.hold()
        fps = VGroup(*[Dot(ax.c2p(v, v), radius=0.09, color=c)
                       for v, c in ((-1, C_MINUS), (0, C_ZERO), (1, C_PLUS))])
        cross = VGroup(mt(r"\text{diagonal: height}=x", 32, C_DIAG), mt(r"\text{curve: height}=p(x)", 32, C_P),
                       mt(r"\text{crossing: }p(x)=x", 34)).arrange(DOWN, buff=0.3).move_to([PANEL_X, 1.5, 0])
        away = self.web(0.05, 6, C_ZERO, width=2.5)
        self.say("Now look at where the curve meets the diagonal. On the diagonal the height equals x, and on "
                 "the curve the height is p of x. So at a crossing, p of x equals x. The three crossings are "
                 "our three fixed points, minus one, zero, and one. And the staircases show which way things "
                 "move around them. Near zero the path walks away, and near one it walks in.", FadeOut(VGroup(w2, m2, seq2)))
        self.cue("On the diagonal the height equals x", FadeIn(cross[0]))
        self.cue("and on the curve", FadeIn(cross[1]))
        self.cue("So at a crossing", FadeIn(cross[2]))
        self.cue("The three crossings", LaggedStart(*[GrowFromCenter(d) for d in fps], lag_ratio=0.25))
        self.cue("Near zero the path walks away", self.draw(away, 0.2))
        self.hold()
        self.play(FadeOut(VGroup(cross, away)))
        self.fps = fps

    # ------------------------------------------------------------ 5. why 1 attracts and 0 repels
    def slopes(self):
        ax, fps = self.ax, self.fps
        TOP = [PANEL_X, 2.2, 0]
        at1 = VGroup(mt(r"p(1+e)\approx1+(a+3b)\,e", 36), mt(r"a+3b=0", 36, C_PLUS),
                     mt(r"\text{at }1:\ \text{error}\times0", 36, C_PLUS)).arrange(DOWN, buff=0.3).move_to(TOP, UP)
        self.say("Why does one pull values in, while zero pushes them away? For one, we already know. When we "
                 "built p, we put in one plus a small error e, and we chose p so that one step multiplies that"
                 " error by zero.", Indicate(fps[2], color=C_PLUS), Indicate(fps[1], color=C_ZERO))
        self.cue("we put in one plus a small error e", FadeIn(at1[0]))
        self.cue("and we chose p", FadeIn(at1[1]))
        self.cue("multiplies that error by zero", FadeIn(at1[2]))
        self.hold()
        at0 = VGroup(mt(r"p(e)=1.5\,e-0.5\,e^3", 36), mt(r"e=0.1:\quad e^3=0.001", 32, GREY_A),
                     mt(r"p(e)\approx1.5\,e", 36), mt(r"\text{at }0:\ \text{error}\times1.5", 36, C_ZERO))
        at0.arrange(DOWN, buff=0.3).move_to(TOP, UP)
        self.say("So do the same thing at zero. A value near zero is just a small error e. Put it into p, and "
                 "we get one point five e, minus one half e cubed. For a small e, the cube is tiny. If e is "
                 "zero point one, e cubed is only zero point zero zero one. So p gives about one point five e."
                 " This time, one step multiplies the error by one point five, and the error grows.", FadeOut(at1[:2]), at1[2].animate.move_to([PANEL_X, -2.3, 0]))
        self.cue("Put it into p", FadeIn(at0[0]))
        self.cue("If e is zero point one", FadeIn(at0[1]))
        self.cue("So p gives about", FadeIn(at0[2]))
        self.cue("This time, one step multiplies", FadeIn(at0[3]))
        self.hold()
        o = orbit(0.1, 3)
        assert all(abs(b_ / a_ - 1.5) < 0.03 for a_, b_ in zip(o, o[1:]))
        grow = mt(r"0.1\to " + r"\to ".join(num(v) for v in o[1:]), 34)
        times = mt(r"\times1.5\quad\times1.5\quad\times1.5", 26, C_ZERO)
        gg = VGroup(grow, times).arrange(DOWN, buff=0.15).move_to(TOP, UP)
        tan0 = ax.plot(lambda x: 1.5 * x, x_range=[-0.9, 0.9], color=C_ZERO, stroke_width=3)
        E = 0.6
        tri = VGroup(Line(ax.c2p(0, 0), ax.c2p(E, 0), color=YELLOW_D, stroke_width=4),
                     Line(ax.c2p(E, 0), ax.c2p(E, 1.5 * E), color=YELLOW_D, stroke_width=4))
        tri_l = VGroup(mt("e", 26, YELLOW_D).next_to(tri[0], DOWN, buff=0.08),
                       mt("1.5e", 26, YELLOW_D).next_to(tri[1], RIGHT, buff=0.08))
        slope0 = mt(r"\text{slope at }0:\ \frac{1.5\,e}{e}=1.5", 36, C_ZERO).next_to(gg, DOWN, buff=0.5)
        self.say("We have seen this growth already. Zero point one went to zero point one five, then zero "
                 "point two two, then zero point three three. Each value is about one and a half times the one"
                 " before. That is why zero pushes values away. On the graph, this multiplier is the slope of "
                 "the curve. Zoom in at zero, and the curve looks like a straight line. Move e to the right, "
                 "and it rises by one point five e. Rise over run is one point five.", FadeOut(at0[:3]), at0[3].animate.move_to([PANEL_X, -1.7, 0]), FadeIn(grow))
        self.cue("Each value is about", FadeIn(times))
        self.cue("Zoom in at zero")
        self.zoom_to(ax.c2p(0.35, 0.45), Create(tan0), width=5.5, run_time=1.6)
        self.cue("Move e to the right", Create(tri[0]), FadeIn(tri_l[0]))
        self.cue("and it rises by", Create(tri[1]), FadeIn(tri_l[1]))
        self.cue("Rise over run")
        self.zoom_back(FadeIn(slope0), run_time=1.4)
        self.hold()
        rule = VGroup(txt("each step: error × slope", 26),
                      mt(r"|\text{slope}|>1:\ \text{pushed away}", 34, C_ZERO),
                      mt(r"|\text{slope}|<1:\ \text{pulled in}", 34, C_PLUS)).arrange(DOWN, buff=0.3).move_to(TOP, UP)
        near0 = orbit(0.05, 3)
        assert abs(near0[1] - 0.075) < 0.0005 and abs(near0[2] - 0.11) < 0.005
        seq0 = mt(r"0.05\to0.075\to0.11\to\cdots", 32, C_ZERO).next_to(rule, DOWN, buff=0.45)
        w0 = self.web(0.05, 10, C_ZERO, width=2.5)
        self.say("So here is the rule. Near a fixed point, each step multiplies the error by the slope of the "
                 "curve there. If the slope is bigger than one in size, the error grows and values are pushed "
                 "away. If it is smaller than one, the error shrinks and values are pulled in. At zero the "
                 "slope is one point five, and zero point zero five drifts to zero point zero seven five, then"
                 " zero point one one, and on.", FadeOut(VGroup(gg, slope0, tri, tri_l)), FadeIn(rule[0]))
        self.cue("If the slope is bigger than one", FadeIn(rule[1]))
        self.cue("If it is smaller than one", FadeIn(rule[2]))
        self.cue("and zero point zero five drifts", FadeIn(seq0), self.draw(w0, 0.22))
        self.hold()
        near1 = orbit(1.2, 2)
        errs = [abs(v - 1) for v in near1]
        assert abs(errs[1] - 0.06) < 0.005 and abs(errs[2] - 0.006) < 0.0005
        tan1 = VGroup(ax.plot(lambda x: 1, x_range=[0.5, 1.5], color=C_PLUS, stroke_width=3),
                      ax.plot(lambda x: -1, x_range=[-1.5, -0.5], color=C_MINUS, stroke_width=3))
        # the terms dropped in episode 1, put back: p(1+e) = 1 − 1.5e² − 0.5e³ exactly
        assert abs(p(1.2) - (1 - 1.5 * 0.2 ** 2 - 0.5 * 0.2 ** 3)) < 1e-12
        flat = VGroup(mt(r"\text{slope at }\pm1:\ 0", 36, C_PLUS),
                      fit(mt(r"p(1+e)=\tfrac32(1+e)-\tfrac12(1+3e+3e^2+e^3)", 36)),
                      mt(r"=1-\tfrac32\,e^2-\tfrac12\,e^3", 36),
                      mt(r"\text{new error}\approx-1.5\,e^2", 36, C_PLUS),
                      mt(r"\text{error size: }\ 0.2\to0.06\to0.006", 34, C_PLUS)).arrange(DOWN, buff=0.3).move_to(TOP, UP)
        w1 = self.web(1.2, 5, C_PLUS, width=2.5)
        self.say("At one, the multiplier is zero, so the slope is zero. The curve is flat at the top of its "
                 "hump. That is our second wish, seen as a picture. But an error cannot vanish completely in "
                 "one step. When we built p, we dropped the terms with e squared and e cubed, because they "
                 "were small. Now put them back. p of one plus e is three halves times one plus e, minus one "
                 "half times the full cube, one plus three e plus three e squared plus e cubed. The ones add "
                 "up to one. The terms with e cancel, as we arranged. What is left is minus one and a half e "
                 "squared, minus one half e cubed. So the new error is about minus one and a half times e "
                 "squared. The minus sign says that we land just below one, whichever side we started on. "
                 "Start at one point two. The error goes from zero point two, to zero point zero six, to zero "
                 "point zero zero six. Each step roughly squares it, which is far faster than shrinking by a "
                 "fixed factor. The same calculation at minus one gives the same result.",
                 FadeOut(VGroup(rule, seq0, w0, tan0)))
        self.cue("The curve is flat", Create(tan1[0]), FadeIn(flat[0]))
        self.cue("p of one plus e is three halves", FadeIn(flat[1]))
        self.cue("What is left is", FadeIn(flat[2]))
        self.cue("So the new error is about", FadeIn(flat[3]))
        self.cue("Start at one point two", self.draw(w1, 0.3), FadeIn(flat[4]))
        self.cue("The same calculation at minus one", Create(tan1[1]))
        self.hold()
        lab0 = txt("unstable", 22, C_ZERO).next_to(fps[1], RIGHT, buff=0.3).shift(DOWN * 0.45)
        lab1 = txt("stable", 22, C_PLUS).next_to(fps[2], UP, buff=0.3).shift(LEFT * 0.35)
        lab_1 = txt("stable", 22, C_MINUS).next_to(fps[0], DOWN, buff=0.3).shift(RIGHT * 0.45)
        self.say("So zero is unstable, like the top of a hill, where the smallest push sends you rolling away."
                 " One and minus one are stable, like the bottoms of two valleys, where everything nearby "
                 "rolls in.", FadeOut(w1), FadeIn(lab0))
        self.cue("One and minus one are stable", FadeIn(lab1), FadeIn(lab_1))
        self.hold()
        self.play(FadeOut(VGroup(flat, tan1, lab0, lab1, lab_1, at1[2], at0[3])))

    # ------------------------------------------------------------ 6. how big can σ be? (√3)
    def how_big(self):
        ax = self.ax
        TOP = [PANEL_X, 2.3, 0]
        m13 = Dot(ax.c2p(1.3, 0), radius=0.06, color=C_PLUS)
        l13 = mt("1.3", 24, C_PLUS).next_to(m13, DOWN, buff=0.35)
        self.say("So far every start rolled into the valley at one. But the largest start we tried was one "
                 "point three, and we don't get to choose sigma. How large can it be before something goes "
                 "wrong?", Indicate(self.fps[2], color=C_PLUS))
        self.cue("the largest start we tried", GrowFromCenter(m13), FadeIn(l13))
        self.hold()
        o = orbit(1.5, 3)
        assert [num(v) for v in o[1:]] == ["0.56", "0.75", "0.92"]
        w = self.web(1.5, 8, C_PLUS)
        m = Dot(ax.c2p(1.5, 0), radius=0.07, color=C_PLUS)
        t15 = mt(r"1.5\to " + r"\to ".join(num(v) for v in o[1:]) + r"\to\cdots\to 1", 34, C_PLUS).move_to(TOP)
        self.say("Go a little bigger, to one point five. That is past the hump, where the curve is already "
                 "coming down, so the first step drops all the way to zero point five six. But from there it "
                 "climbs as before, zero point seven five, zero point nine two, and into one. Still fine.", FadeOut(VGroup(m13, l13)), FadeIn(m), FadeIn(t15[0][:3]))
        self.cue("so the first step drops", Create(w[0]), FadeIn(t15[0][3:8]))
        self.cue("But from there it climbs", self.draw(w[1:], 0.3), FadeIn(t15[0][8:]))
        self.hold()
        m2 = Dot(ax.c2p(1.8, 0), radius=0.07, color=WHITE)
        q18 = mt(r"1.8\to\ ?", 38).move_to(TOP)
        self.say("A little bigger again, one point eight. Before we look, where do you think it ends up?", FadeOut(VGroup(w, m, t15)), FadeIn(m2), FadeIn(q18))
        self.hold(1.5)

        assert abs(1.5 * 1.8 - 2.7) < 1e-9 and abs(0.5 * 1.8 ** 3 - 2.916) < 1e-9 and abs(p(1.8) + 0.216) < 1e-9
        assert abs(p(0.216) - 0.32) < 0.005
        calc = VGroup(mt(r"\tfrac32\cdot1.8=2.7", 34), mt(r"\tfrac12\cdot1.8^3=2.92", 34),
                      mt(r"p(1.8)=2.7-2.92=-0.216", 34, C_MINUS)).arrange(DOWN, buff=0.22).move_to(TOP, UP)
        mirror = VGroup(mt(r"p(-x)=-p(x)", 36), txt("the mirror rule", 24, YELLOW_D)).arrange(RIGHT, buff=0.35)
        mirror.next_to(calc, DOWN, buff=0.45)
        pair = VGroup(mt(r"+0.216\to+0.32", 34, C_PLUS), mt(r"-0.216\to-0.32", 34, C_MINUS))
        pair.arrange(DOWN, buff=0.2).next_to(mirror, DOWN, buff=0.4)
        end = mt(r"1.8\to-0.216\to-0.32\to\cdots\to-1", 32, C_MINUS).next_to(pair, DOWN, buff=0.4)
        w2 = self.web(1.8, 9, C_MINUS)
        self.say("Do the step. Three halves of one point eight is two point seven. But half of its cube is two"
                 " point nine two, which is bigger. Subtract, and the result is negative, minus zero point two"
                 " one six. What does p do with a negative number? p has only odd powers, so flipping the sign"
                 " of the input just flips the sign of the output. Plus zero point two one six goes to plus "
                 "zero point three two, so minus zero point two one six goes to minus zero point three two. "
                 "The negative side is a mirror image of the positive side. Call this the mirror rule. So this"
                 " value does what its mirror image would do, with the sign flipped. It moves away from zero "
                 "and settles at minus one. For a singular value, that has the right size but the wrong sign. "
                 "This direction ends up reversed.", FadeOut(q18))
        self.cue("Three halves of one point eight", FadeIn(calc[0]))
        self.cue("But half of its cube", FadeIn(calc[1]))
        self.cue("Subtract, and the result is negative", FadeIn(calc[2]), Create(w2[0]))
        self.cue("p has only odd powers", FadeIn(mirror[0]))
        self.cue("Plus zero point two one six goes to", FadeIn(pair[0]))
        self.cue("so minus zero point two one six", FadeIn(pair[1]))
        self.cue("Call this the mirror rule", FadeIn(mirror[1]))
        self.cue("It moves away from zero", self.draw(w2[1:], 0.3), FadeIn(end))
        self.cue("that has the right size but the wrong sign", Flash(self.fps[0], color=C_MINUS))
        self.hold(1.0)

        # √3 is where the hump comes back down to the axis
        hump = ax.plot(p, x_range=[0, S3], color=C_PLUS, stroke_width=7)
        past = ax.plot(p, x_range=[S3, 2.05], color=C_MINUS, stroke_width=7)
        cross = Dot(ax.c2p(S3, 0), radius=0.09, color=C_ZERO)
        self.say("So what went wrong was the very first step, which landed below the axis. On the graph, that "
                 "is where the curve, after its hump, comes down and crosses the axis. Past that crossing, p "
                 "of x is negative.", FadeOut(VGroup(calc, mirror, pair, end)), FadeOut(w2[1:]), Indicate(w2[0], color=C_MINUS))
        self.cue("comes down and crosses the axis")
        self.zoom_to(ax.c2p(S3, 0), Create(hump), GrowFromCenter(cross), width=6.0, run_time=1.8)
        self.cue("Past that crossing", Create(past))
        self.hold(1.0)
        self.zoom_back()
        fac = MathTex(r"p(x)", r"=", r"\frac{x}{2}", r"\,(3-x^2)", font_size=42)
        fac.move_to([PANEL_X, 2.2, 0])
        split = VGroup(mt(r"\tfrac32\,x=\tfrac{x}{2}\cdot3", 36), mt(r"\tfrac12\,x^3=\tfrac{x}{2}\cdot x^2", 36))
        split.arrange(DOWN, buff=0.3).next_to(fac, DOWN, buff=0.6)
        tick = Line(ax.c2p(S3, -0.08), ax.c2p(S3, 0.08), color=C_ZERO, stroke_width=4)
        lab = mt(r"\sqrt3", 30, C_ZERO).move_to(ax.c2p(S3 - 0.3, 0.25))
        sgn = VGroup(mt(r"x>0:\quad\frac{x}{2}>0", 36), mt(r"3-x^2<0\iff x>\sqrt3\approx1.73", 36, C_ZERO))
        sgn.arrange(DOWN, buff=0.3).next_to(fac, DOWN, buff=0.45)
        self.say("Where is the crossing? Both terms of p contain x over two. Three halves x is x over two "
                 "times three, and one half x cubed is x over two times x squared. So p of x is x over two, "
                 "times three minus x squared.", FadeOut(w2[0]))
        self.cue("Three halves x is x over two times three", FadeIn(split[0]))
        self.cue("and one half x cubed", FadeIn(split[1]))
        self.cue("So p of x is x over two", Write(fac))
        self.hold()
        self.say("For a positive x, the first factor, x over two, is positive. So the sign of p comes from the"
                 " second factor, three minus x squared.", FadeOut(split), FadeIn(sgn[0]), Indicate(fac[2]))
        self.cue("So the sign of p comes from", Indicate(fac[3]))
        self.say("Three minus x squared is positive while x squared is below three, and negative once x "
                 "squared passes three. The change happens at x equals square root of three, about one point "
                 "seven three.")
        self.cue("and negative once x squared passes three", FadeIn(sgn[1]), Indicate(fac[3], color=C_ZERO))
        self.cue("The change happens at")
        self.zoom_to(ax.c2p(S3, 0), FadeIn(lab), width=7.0, run_time=1.2)
        self.play(Flash(cross, color=C_ZERO))
        self.hold(1.0)
        self.zoom_back()
        m15 = Dot(ax.c2p(1.5, 0), radius=0.07, color=C_PLUS)
        cmp_ = mt(r"1.5<\sqrt3<1.8", 38).next_to(sgn, DOWN, buff=0.5)
        self.say("One point five is below square root of three, and it was fine. One point eight is just above"
                 " it, and it flipped. That matches.", GrowFromCenter(m15), FadeIn(cmp_[0][:3]))
        self.cue("One point eight is just above", Indicate(m2, scale_factor=1.6), FadeIn(cmp_[0][3:]))
        self.hold()
        top = DashedLine(ax.c2p(0, 1), ax.c2p(S3, 1), color=GREY_B, dash_length=0.08)
        land = Line(ax.c2p(0, 0), ax.c2p(0, 1), color=C_PLUS, stroke_width=8)
        first = mt(r"0<x<\sqrt3:\quad 0<p(x)\le1", 36, C_PLUS).next_to(fac, DOWN, buff=0.5)
        self.say("Then is every start below square root of three safe? Look at the curve between zero and "
                 "square root of three. It stays above the axis, and its highest point, the top of the hump, "
                 "is at height one. So wherever we start in this range, the first step lands somewhere between"
                 " zero and one.", FadeOut(VGroup(sgn, cmp_, m15, m2)), FadeOut(past))
        self.cue("It stays above the axis", Indicate(hump, color=C_PLUS, scale_factor=1.0))
        self.cue("the top of the hump", Create(top), Indicate(self.fps[2], color=C_PLUS))
        self.cue("the first step lands somewhere between zero and one", Create(land), FadeIn(first))
        self.hold()
        seg01 = ax.plot(p, x_range=[0, 1], color=C_PLUS)
        area = ax.get_area(seg01, x_range=[0, 1], bounded_graph=self.diag, color=C_PLUS, opacity=0.35)
        w3 = self.web(0.3, 8, WHITE, width=2.5)
        climb = mt(r"0<x<1:\quad p(x)>x", 36, C_PLUS).next_to(first, DOWN, buff=0.35)
        self.say("And between zero and one, the curve sits above the diagonal. That means the output is bigger"
                 " than the input, so every step climbs. It cannot climb past one, because the curve never "
                 "goes higher than one. A value that keeps climbing and can never pass one has to settle "
                 "somewhere. And the only place where it can settle is a fixed point, so it ends at one.")
        self.cue("the curve sits above the diagonal", FadeIn(area), FadeIn(climb))
        self.cue("so every step climbs", self.draw(w3, 0.3))
        self.cue("so it ends at one", Flash(self.fps[2], color=C_PLUS))
        self.hold()
        safe = Line(ax.c2p(0, 0), ax.c2p(S3, 0), color=C_PLUS, stroke_width=8)
        verdict = mt(r"0<\sigma<\sqrt3\ \ \Longrightarrow\ \ \sigma\to+1", 38, C_PLUS).next_to(climb, DOWN, buff=0.5)
        self.say("So yes. Every sigma between zero and square root of three ends at one.", FadeOut(w3), Create(safe), FadeIn(verdict))
        self.hold()
        arrow = CurvedArrow(ax.c2p(S3, 0) + UP * 0.12, ax.c2p(0, 0) + UP * 0.12, angle=PI / 3,
                            color=C_ZERO, stroke_width=4)
        s3 = mt(r"p(\sqrt3)=\tfrac{\sqrt3}{2}\,(3-3)=0", 36, C_ZERO).next_to(verdict, DOWN, buff=0.4)
        self.say("And exactly at square root of three, the second factor is zero, so p gives zero. The value "
                 "lands on the fixed point at zero, and it stays there forever.", Indicate(fac[3], color=C_ZERO))
        self.cue("so p gives zero", Create(arrow), FadeIn(s3))
        self.cue("and it stays there forever", Flash(self.fps[1], color=C_ZERO))
        self.hold()
        self.play(FadeOut(VGroup(s3, arrow, top, hump, area, cross, land, first, climb, safe, verdict)), FadeIn(tick))
        self.s3_mark = VGroup(tick, lab)
        self.fac = fac

    # ------------------------------------------------------------ 7. much bigger σ (√5)
    def too_big(self):
        ax = self.ax
        o3 = orbit(3.0, 2)
        assert o3 == [3.0, -9.0, 351.0] and 1.5 * 9 == 13.5 and 0.5 * 9 ** 3 == 364.5
        under = self.fac.get_bottom() + DOWN * 0.4
        start3 = mt(r"\text{start: }3", 38, C_S5).move_to(under, UP)
        self.say("So past square root of three, the first step flips the sign. One point eight flipped and "
                 "still settled, at minus one. Maybe a flip is all that ever happens. Test that with a much "
                 "bigger start, three.")
        self.cue("Test that with a much bigger start", FadeIn(start3))
        self.hold()
        steps = VGroup(mt(r"p(3)=4.5-13.5=-9", 34), mt(r"p(-9)=-p(9)", 34),
                       mt(r"p(9)=13.5-364.5=-351", 34)).arrange(DOWN, buff=0.25).move_to(under, UP)
        blow = mt(r"3\to -9\to +351\to\cdots", 38, C_S5).next_to(steps, DOWN, buff=0.4)
        self.say("Three halves of three is four point five, and half of three cubed is thirteen point five. "
                 "Subtract, and we get minus nine. It flipped, as expected. Now the next step. By the mirror "
                 "rule, minus nine does what nine does, with the sign flipped. Nine goes to thirteen point "
                 "five minus three hundred sixty four point five, which is minus three hundred fifty one. So "
                 "minus nine goes to plus three hundred fifty one. It flips every time, and it gets bigger "
                 "every time. This one explodes.", FadeOut(start3))
        self.cue("Three halves of three is four point five", FadeIn(steps[0]))
        self.cue("By the mirror rule", FadeIn(steps[1]))
        self.cue("Nine goes to", FadeIn(steps[2]))
        self.cue("So minus nine goes to plus", FadeIn(blow))
        self.hold()
        sizes = VGroup(mt(r"1.8:\ \ \text{size }0.216<1.8", 34, C_ZERO), mt(r"3:\ \ \text{size }9>3", 34, C_S5),
                       mt(r"2.0:\ \ \text{size }" + num(abs(p(2.0))) + r"<2.0", 34, C_ZERO),
                       mt(r"2.3:\ \ \text{size }" + num(abs(p(2.3))) + r">2.3", 34, C_S5))
        sizes.arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(under, UP)
        self.say("Both one point eight and three flip, so the difference must be in the size, meaning the "
                 "number without its sign. One point eight came out at size zero point two, smaller than it "
                 "went in. Three came out at size nine, bigger than it went in. So somewhere between them, "
                 "shrinking turns into growing. Narrow it down. Two point zero goes to minus one, so its size "
                 "is one. That is still smaller.", FadeOut(VGroup(steps, blow)))
        self.cue("One point eight came out at size", FadeIn(sizes[0]))
        self.cue("Three came out at size nine", FadeIn(sizes[1]))
        self.cue("Two point zero goes to minus one", FadeIn(sizes[2]))
        self.say("But two point three goes to minus two point six three. Its size is bigger than where it "
                 "started. So the turning point is somewhere between two point zero and two point three.", FadeIn(sizes[3]))
        self.hold()
        self.play(FadeOut(sizes))
        xc = _root(-2.5, 1.0, 2.5)
        shrink = ax.plot(p, x_range=[S3, S5], color=C_ZERO, stroke_width=7)
        grow = ax.plot(p, x_range=[S5, xc], color=C_S5, stroke_width=7)
        size = MathTex(r"|p(x)|", r"=", r"|x|", r"\cdot", r"\frac{x^2-3}{2}", font_size=40)
        size.next_to(self.fac, DOWN, buff=0.4)
        box = SurroundingRectangle(size[4], color=YELLOW_D, buff=0.1, stroke_width=2.5)
        box_l = txt("size factor", 22, YELLOW_D).next_to(box, RIGHT, buff=0.15)
        self.say("Where exactly is the turning point? Compare the size after a step with the size before. Use "
                 "the factored form. p of x is x over two, times three minus x squared. So the size of p of x "
                 "is the size of x, times the size of three minus x squared, over two. Past square root of "
                 "three, that second part is x squared minus three, over two. Call it the size factor. Each "
                 "step multiplies the size by this factor.")
        self.cue("p of x is x over two", Indicate(self.fac))
        self.cue("So the size of p of x", FadeIn(size[:4]))
        self.cue("Past square root of three", FadeIn(size[4]))
        self.cue("Call it the size factor", Create(box), FadeIn(box_l))
        self.hold()
        f20, f23 = (2.0 ** 2 - 3) / 2, (2.3 ** 2 - 3) / 2
        assert f20 == 0.5 and abs(2.0 * f20 - abs(p(2.0))) < 1e-12 and abs(2.3 * f23 - abs(p(2.3))) < 1e-12
        assert num(f23) == "1.14"
        rows = VGroup(mt(r"x=2.0:\quad\frac{4-3}{2}=0.5<1\quad\text{shrinks}", 32, C_ZERO),
                      mt(r"x=2.3:\quad\frac{5.29-3}{2}\approx" + num(f23) + r">1\quad\text{grows}", 32, C_S5))
        rows.arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(size, DOWN, buff=0.5)
        self.say("Check it with the starts we tried. At two point zero, the factor is four minus three, over "
                 "two, which is one half. And two did go to size one. At two point three, the factor is about "
                 "one point one four, and two point three did come out bigger. So a factor below one means "
                 "flip and shrink. A factor above one means flip and grow.", FadeIn(rows[0][0][:15]))
        self.cue("And two did go", FadeIn(rows[0][0][15:]))
        self.cue("At two point three", FadeIn(rows[1][0][:19]))
        self.cue("and two point three did come out", FadeIn(rows[1][0][19:]))
        self.hold()
        eqm = mt(r"\frac{x^2-3}{2}=1\iff x^2=5", 36, C_S5).next_to(size, DOWN, buff=0.5)
        s5 = Line(ax.c2p(S5, -0.08), ax.c2p(S5, 0.08), color=C_S5, stroke_width=4)
        s5l = mt(r"\sqrt5", 30, C_S5).next_to(s5, UP, buff=0.1)
        self.say("The turning point is where the factor is exactly one. That means x squared minus three "
                 "equals two, so x squared equals five. The turning point is square root of five, about two "
                 "point two four, and it does sit between two point zero and two point three. On the curve, "
                 "between square root of three and square root of five a step shrinks the size, and beyond "
                 "square root of five it grows.", FadeOut(rows), FadeIn(eqm))
        self.cue("The turning point is square root of five", Create(s5), FadeIn(s5l))
        self.cue("On the curve")
        self.zoom_to(ax.c2p(2.0, -1.1), Create(shrink), width=6.5, run_time=1.6)
        self.cue("and beyond square root of five", Create(grow))
        self.hold(1.2)
        self.zoom_back()

        pts = [ax.c2p(S5, 0)]
        x = S5
        for _ in range(4):
            y = p(x)
            pts += [ax.c2p(x, y), ax.c2p(y, y)]
            x = y
        sq = VGroup(*[Line(a, b, color=C_S5, stroke_width=3.5) for a, b in zip(pts, pts[1:])])
        at5 = mt(r"p(\sqrt5)=\tfrac{\sqrt5}{2}\,(3-5)=-\sqrt5", 34, C_S5).next_to(eqm, DOWN, buff=0.4)
        self.say("What happens exactly at square root of five? Use the factored form. x over two, times three "
                 "minus five, is minus x. So square root of five goes to minus square root of five. By the "
                 "mirror rule, that goes straight back to plus square root of five. On the picture, the path "
                 "becomes a square.", FadeOut(VGroup(shrink, grow)))
        self.cue("x over two, times three minus five", FadeIn(at5))
        self.cue("So square root of five goes to", self.draw(sq[:2], 0.5))
        self.cue("that goes straight back", self.draw(sq[2:5], 0.5))
        self.hold()
        per = txt("period-2 orbit", 26, C_S5).next_to(at5, DOWN, buff=0.35)
        self.say("So square root of five neither settles nor explodes. It jumps back and forth between plus "
                 "and minus square root of five forever. This is called a period two orbit, because it repeats"
                 " every two steps.", self.draw(sq[5:], 0.4))
        self.cue("This is called a period two orbit", FadeIn(per))
        self.hold(1.0)
        o = orbit(2.3, 3)
        assert [num(o[1]), num(o[2]), num(o[3], 1)] == ["-2.63", "5.18", "-61.8"]
        seq = mt(r"\to ".join(num(v, 2 if abs(v) < 10 else 1) for v in o) + r"\to\cdots", 34, C_S5)
        seq.next_to(per, DOWN, buff=0.45)
        if seq.width > 6.2:
            seq.scale_to_fit_width(6.2)
        self.say("And past square root of five, every step flips and grows. Two point three goes to minus two "
                 "point six three, then five point one eight, then minus sixty one point eight. Like three, it"
                 " explodes.", FadeOut(sq))
        self.cue("Two point three goes to", FadeIn(seq))
        self.hold(0.5)
        self.clear_stage(self.corner)

    # ------------------------------------------------------------ the closing card
    def closing(self):
        self.ep2_closing()

    def ep2_closing(self):
        """Two thresholds and the gap between them. The gap is left open for the next episode."""
        nl = NumberLine(x_range=[0, 2.6, 0.5], length=10.4, color=GREY_B, stroke_width=2,
                        include_tip=False, tick_size=0.04).move_to([0, 0.2, 0])

        def seg(a, b, c):
            return Line(nl.n2p(a), nl.n2p(b), color=c, stroke_width=14)

        safe, gap, boom = seg(0, S3, C_PLUS), seg(S3, S5, GREY_D), seg(S5, 2.6, C_S5)
        marks = VGroup(*[mt(s, 28, c).next_to(nl.n2p(v), DOWN, buff=0.3)
                         for v, s, c in ((0, "0", GREY_B), (1, "1", C_PLUS), (S3, r"\sqrt3", C_ZERO),
                                         (S5, r"\sqrt5", C_S5))])
        l_safe = txt("ends at 1", 28, C_PLUS).next_to(safe, UP, buff=0.35)
        l_boom = txt("explodes", 28, C_S5).next_to(boom, UP, buff=0.35)
        qm = mt("?", 44, WHITE).next_to(gap, UP, buff=0.3)
        tried = VGroup(*[Dot(nl.n2p(v), radius=0.09, color=C_MINUS) for v in (1.8, 2.0)])
        tried_l = VGroup(*[mt(s, 28, C_MINUS).next_to(d, DOWN, buff=0.75) for s, d in zip(("1.8", "2.0"), tried)])
        self.say("So now we have two thresholds. Below square root of three, every start ends at one. Beyond "
                 "square root of five, every start explodes. Between them there is a gap, and we have only "
                 "tried two starts in it, one point eight and two point zero. Both ended at minus one. Does "
                 "every start in the gap do that? That is next time.", Create(nl), FadeIn(marks))
        self.cue("Below square root of three", Create(safe), FadeIn(l_safe))
        self.cue("Beyond square root of five", Create(boom), FadeIn(l_boom))
        self.cue("Between them there is a gap", Create(gap))
        self.cue("one point eight and two point zero", *[GrowFromCenter(d) for d in tried], FadeIn(tried_l))
        self.cue("Does every start in the gap", FadeIn(qm, shift=UP * 0.2))
        self.sign_off()
