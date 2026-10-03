"""Newton–Schulz, episode 1: why an orthogonal update, and how the cubic p is forced on us."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ns_common import *  # noqa: E402,F403
from ns_common import _root  # noqa: E402,F401


class Ep01InventingP(NSScene):
    SCENES = ["ellipse", "why_orthogonal", "why_p"]
    ASK = "You could have invented it."
    ASK_SAY = "You could have invented it."

    # ------------------------------------------------------------ 1. why anyone iterates this
    def ellipse(self):
        R, th = 1.45, 30 * DEGREES
        C0 = np.array([-3.3, 0.15, 0])
        u1 = np.array([np.cos(th), np.sin(th), 0])
        u2 = np.array([-np.sin(th), np.cos(th), 0])
        circ = Circle(radius=R, color=GREY_B, stroke_width=3).move_to(C0)
        wlab = mt(r"W", 40).next_to(circ, UP, buff=0.25)
        self.say("Take a matrix W. It turns the unit circle into an ellipse.", Create(circ), FadeIn(wlab))

        # the SVD as three moves: rotate, stretch along the axes, rotate
        def arm(v, c):
            return Line(C0, C0 + R * v, color=c, stroke_width=5)

        phi = 75 * DEGREES
        v1 = np.array([np.cos(phi), np.sin(phi), 0])
        v2 = np.array([-np.sin(phi), np.cos(phi), 0])
        demo = VGroup(Circle(radius=R, color=C_SIG, stroke_width=4).move_to(C0),
                      arm(v1, C_PLUS), arm(v2, C_MINUS))
        svd = MathTex(r"W", r"=", r"U", r"\,\Sigma\,", r"V^{\top}", font_size=48).move_to([PANEL_X, 1.4, 0])
        steps = VGroup(txt("1. rotate", 26, GREY_A), txt("2. stretch the axes", 26, C_SIG),
                       txt("3. rotate again", 26, GREY_A)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        steps.next_to(svd, DOWN, buff=0.5)
        self.say("How? Every matrix does it in three moves. Follow two perpendicular arms on the circle.",
                 FadeIn(demo), Write(svd))
        self.say("First, a rotation turns the arms onto the axes. That is V transpose.",
                 Rotate(demo, -phi, about_point=C0), FadeIn(steps[0]), Indicate(svd[4]), run_time=2.0)
        self.say("Next, Σ stretches each axis by its own amount, here 1.3 and 0.5. The circle becomes an ellipse.",
                 demo.animate.apply_matrix(np.diag([1.3, 0.5, 1]), about_point=C0), FadeIn(steps[1]),
                 Indicate(svd[3], color=C_SIG), run_time=2.0)
        self.say("Finally U rotates the ellipse into place. Rotations never change lengths, "
                 "so all the stretching lives in Σ.",
                 Rotate(demo, th, about_point=C0), FadeIn(steps[2]), Indicate(svd[2]), run_time=2.0)
        self.hold()

        s1, s2 = ValueTracker(1.3), ValueTracker(0.5)

        def shape():
            a, b = s1.get_value(), s2.get_value()
            e = Ellipse(width=2 * R * a, height=2 * R * b, color=C_SIG, stroke_width=4)
            e.rotate(th).move_to(C0)
            l1 = Line(C0, C0 + R * a * u1, color=C_SIG, stroke_width=4)
            l2 = Line(C0, C0 + R * b * u2, color=C_SIG, stroke_width=4)
            t1 = mt(r"\sigma_1", 30, C_SIG).move_to(C0 + R * a * u1 * 0.55 - 0.3 * u2)
            t2 = mt(r"\sigma_2", 30, C_SIG).move_to(C0 + R * b * u2 * 0.55 + 0.3 * u1)
            return VGroup(e, l1, l2, t1, t2)

        ell = always_redraw(shape)
        self.play(circ.animate.set_stroke(opacity=0.35), FadeOut(demo), FadeIn(ell), FadeOut(steps),
                  FadeOut(svd), run_time=0.8)
        self.say("The two stretch factors, σ1 and σ2, are the half-axes of the ellipse: W's singular values.",
                 Indicate(ell[3], color=C_SIG), Indicate(ell[4], color=C_SIG))

        def readout(tr, name):
            d = DecimalNumber(tr.get_value(), num_decimal_places=3, font_size=36, color=C_SIG)
            d.add_updater(lambda m: m.set_value(tr.get_value()))
            return VGroup(mt(name + "=", 36, C_SIG), d).arrange(RIGHT, buff=0.15)

        r1, r2 = readout(s1, r"\sigma_1"), readout(s2, r"\sigma_2")
        rd = VGroup(r1, r2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([PANEL_X, 0.1, 0])
        self.play(FadeIn(rd))
        ortho = txt("all σ = 1  ⇔  W is orthogonal", 28, C_PLUS).move_to([PANEL_X, -1.3, 0])
        tall = txt("not square: orthonormal columns", 28, GREY_B).next_to(ortho, DOWN, buff=0.3)
        self.say("If every singular value were exactly one, only the rotations would remain. Nothing gets "
                 "stretched, and W would be orthogonal. If W is not square, the exact name for this is "
                 "orthonormal columns. The picture is the same, so we will keep saying orthogonal.",
                 FadeIn(ortho))
        self.cue("If W is not square", FadeIn(tall))
        self.hold()
        self.hold(1.0)
        ell.clear_updaters()
        for d in (r1[1], r2[1]):
            d.clear_updaters()
        self.clear_stage()

    # ------------------------------------------------------------ 2. why each direction should not blow up
    def why_orthogonal(self):
        R, th = 1.45, 30 * DEGREES
        C0 = np.array([-3.35, 0.15, 0])
        u1 = np.array([np.cos(th), np.sin(th), 0])
        u2 = np.array([-np.sin(th), np.cos(th), 0])

        circ = Circle(radius=R, color=GREY_B, stroke_width=3).move_to(C0)
        axes = VGroup(Line(C0 - 1.1 * R * u1, C0 + 1.1 * R * u1, color=C_SIG, stroke_width=3),
                      Line(C0 - 1.1 * R * u2, C0 + 1.1 * R * u2, color=C_SIG, stroke_width=3))
        self.say("The singular value decomposition lets us watch the stretching along each "
                 "natural direction of the matrix, one direction at a time.",
                 FadeIn(circ), FadeIn(axes))

        arm1 = Line(C0, C0 + R * u1, color=C_PLUS, stroke_width=5)
        arm2 = Line(C0, C0 + R * u2, color=C_MINUS, stroke_width=5)
        avg = txt("one average number", 26, GREY_A).move_to([PANEL_X, 0.9, 0])
        self.say("In class we worried about one thing, that the overall scale of the "
                 "gradients does not explode. That is the idea behind Xavier initialization.",
                 FadeIn(arm1), FadeIn(arm2), FadeIn(avg))

        self.say("But that is a single number, a rough average over the whole matrix. "
                 "It says little about any one direction.",
                 Indicate(avg, color=C_MINUS, scale_factor=1.15))

        big = Line(C0, C0 + 1.65 * R * u1, color=C_PLUS, stroke_width=6)
        small = Line(C0, C0 + 0.35 * R * u2, color=C_MINUS, stroke_width=6)
        lab_big = txt("too far", 26, C_PLUS).move_to(C0 + 1.9 * R * u1)
        lab_small = txt("to nothing", 26, C_MINUS).move_to(C0 + 0.15 * R * u2)
        self.say("Xavier does not solve every problem. The average can be fine while one "
                 "direction still stretches too far and another gets squeezed to nothing.",
                 Transform(arm1, big), Transform(arm2, small), FadeIn(lab_big), FadeIn(lab_small))

        back1 = Line(C0, C0 + R * u1, color=C_PLUS, stroke_width=5)
        back2 = Line(C0, C0 + R * u2, color=C_MINUS, stroke_width=5)
        self.say("We want every direction to keep its size, so none gets stretched too far "
                 "and none gets squeezed away.",
                 Transform(big, back1), Transform(small, back2), FadeOut(lab_big), FadeOut(lab_small))

        ortho = txt("every stretch one", 28, C_PLUS).move_to([PANEL_X, 0.9, 0])
        self.say("That is why Muon asks for an orthogonal update, one where every singular "
                 "value is exactly one. Nothing grows, nothing vanishes.",
                 ReplacementTransform(avg, ortho), FadeIn(Circle(radius=R, color=C_PLUS,
                                                                 stroke_width=3).move_to(C0)))

        self.say("Every direction moves together, and the matrix stays healthy step after step.",
                 Indicate(ortho, color=C_PLUS, scale_factor=1.15))
        self.hold(0.5)
        self.clear_stage()

    # ------------------------------------------------------------ 3. one matrix step = p on each σ
    def why_p(self):
        # 01-02: the target U Vᵀ, and the one cheap tool
        svd = MathTex(r"W", r"=", r"U", r"\,\Sigma\,", r"V^{\top}", font_size=56).move_to([0, 1.7, 0])
        svd[3].set_color(C_SIG)
        tgt = MathTex(r"U", r"\,I\,", r"V^{\top}", r"=", r"U", r"V^{\top}", font_size=56).move_to([0, 0.3, 0])
        tgt[1].set_color(C_SIG)
        tgt[4:].set_color(C_PLUS)
        slow = txt("but computing the SVD is slow on a GPU", 28, C_S5).move_to([0, -1.2, 0])
        self.say("We want every singular value to be one. The SVD hands us exactly that. Write W as U, sigma, "
                 "V transpose, keep the two rotations, and replace every stretch in sigma with one. What "
                 "remains is just U times V transpose. But computing an SVD is a long procedure, and it runs "
                 "slowly on a GPU.", Write(svd))
        self.cue("replace every stretch in sigma with one", TransformFromCopy(svd[2:], tgt[:3]))
        self.cue("What remains is", FadeIn(tgt[3:]))
        self.cue("But computing an SVD", FadeIn(slow))
        self.hold()
        goal = VGroup(txt("goal:", 26, GREY_A), MathTex(r"UV^{\top}", font_size=40, color=C_PLUS))
        goal.arrange(RIGHT, buff=0.2).to_corner(UL, buff=0.45)
        cheap = txt("cheap: matrix products", 30, C_PLUS).move_to([0, 0.3, 0])
        self.say("So we want that same result, U times V transpose, without ever computing the SVD. What can a"
                 " GPU do cheaply? It can multiply matrices. That is the one thing it is built for.", FadeOut(svd), FadeOut(tgt), FadeOut(slow), FadeIn(goal))
        self.cue("It can multiply matrices", FadeIn(cheap))
        self.hold()

        # 03: W·W does not fit, Wᵀ W does
        a1 = MathTex(r"W", r"\,W", font_size=56).move_to([-2.6, 1.2, 0])
        sh1 = mt(r"(3\times2)\ (3\times2)", 32, GREY_A).next_to(a1, DOWN, buff=0.35)
        x1 = Cross(VGroup(a1, sh1), stroke_color=C_S5, stroke_width=5)
        a2 = MathTex(r"W^{\top}", r"W", font_size=56).move_to([2.6, 1.2, 0])
        sh2 = mt(r"(2\times3)\ (3\times2)", 32, C_PLUS).next_to(a2, DOWN, buff=0.35)
        self.say("So let's start multiplying. The only matrix we have is W, so the first thing to try is W "
                 "times W. But two matrices can only be multiplied when the number of columns of the first "
                 "matches the number of rows of the second. If W has three rows and two columns, W times W "
                 "does not fit. The transpose swaps rows and columns. So W transpose times W always fits. "
                 "Let's see what that product gives.", cheap.animate.scale(0.8).next_to(goal, DOWN, buff=0.2, aligned_edge=LEFT))
        self.cue("the first thing to try", FadeIn(a1))
        self.cue("If W has three rows", FadeIn(sh1))
        self.cue("W times W does not fit", Create(x1))
        self.cue("The transpose swaps", FadeIn(a2), FadeIn(sh2))
        self.hold()

        # 04: Wᵀ W = V Σ² Vᵀ: U is lost
        def cancel(piece):
            br = Brace(piece, DOWN, color=GREY_B, buff=0.08)
            return VGroup(br, mt("I", 32, GREY_B).next_to(br, DOWN, buff=0.08))

        e1 = mt(r"W=U\,\Sigma\,V^{\top}", 44).move_to([-3.0, 2.0, 0])
        e2 = mt(r"W^{\top}=V\,\Sigma\,U^{\top}", 44).move_to([3.0, 2.0, 0])
        prod = MathTex(r"W^{\top}W", r"=", r"V\,\Sigma\,", r"U^{\top}U", r"\,\Sigma\,V^{\top}", font_size=52)
        prod.move_to([0, 0.6, 0])
        c4 = cancel(prod[3])
        res = MathTex(r"=", r"V\,\Sigma^2\,V^{\top}", font_size=52)
        res.shift(prod[1].get_center() + DOWN * 1.9 - res[0].get_center())
        bad = txt("U has disappeared", 28, C_S5).next_to(res, RIGHT, buff=0.6)
        self.say("To see it, write W with its SVD, as U, sigma, V transpose. Transposing a product reverses "
                 "the order, so W transpose is V, sigma, U transpose. Now put them side by side. In the "
                 "middle, U transpose meets U. The transpose of a rotation is the same rotation done "
                 "backwards, and a rotation followed by its reverse does nothing. So the pair cancels. What is"
                 " left is V, sigma times sigma, V transpose. That is not what we want. Our target has U on "
                 "the left, and here U has disappeared.", FadeOut(VGroup(a1, sh1, x1, a2, sh2)), FadeIn(e1))
        self.cue("Transposing a product", FadeIn(e2))
        self.cue("Now put them side by side", Write(prod))
        self.cue("U transpose meets U", Indicate(prod[3], color=WHITE))
        self.cue("So the pair cancels", FadeIn(c4), prod[3].animate.set_opacity(0.4))
        self.cue("What is left is", FadeIn(res))
        self.cue("That is not what we want", FadeIn(bad), Indicate(goal[1], color=C_PLUS))
        self.hold()

        # 05: one more W on the left: U Σ³ Vᵀ
        prod2 = MathTex(r"W\,W^{\top}W", r"=", r"U\,\Sigma\,", r"V^{\top}V", r"\,\Sigma^2\,V^{\top}", font_size=52)
        prod2.move_to([0, 0.6, 0])
        c5 = cancel(prod2[3])
        res2 = MathTex(r"=", r"U\,\Sigma^3\,V^{\top}", font_size=52)
        res2.shift(prod2[1].get_center() + DOWN * 1.9 - res2[0].get_center())
        res2[1].set_color(C_PLUS)
        ok = txt("both rotations are back", 28, C_PLUS).next_to(res2, RIGHT, buff=0.6)
        self.say("So bring U back. Multiply by W one more time, on the left. Now the V transpose at the end of"
                 " W meets the V at the start of our product, and that pair cancels too. What survives is U on"
                 " the left, V transpose on the right, and sigma three times in between. This time both "
                 "rotations are back where they belong.", FadeOut(VGroup(e2, prod, c4, res, bad)))
        self.cue("Multiply by W one more time", Write(prod2))
        self.cue("Now the V transpose", Indicate(prod2[3], color=WHITE))
        self.cue("and that pair cancels too", FadeIn(c5), prod2[3].animate.set_opacity(0.4))
        self.cue("What survives", FadeIn(res2))
        self.cue("This time both rotations", FadeIn(ok))
        self.hold()

        # 06: Σ is diagonal, so Σ³ cubes each σ on its own
        assert abs(1.3 ** 3 - 2.2) < 0.005 and 0.5 ** 3 == 0.125
        top3 = mt(r"W\,W^{\top}W=U\,\Sigma^3\,V^{\top}", 46).move_to([0, 2.3, 0])
        dg = mt(r"\Sigma=\begin{pmatrix}1.3&0\\0&0.5\end{pmatrix}", 42, C_SIG).move_to([0, 0.7, 0])
        dg3 = MathTex(r"\Sigma^3=\begin{pmatrix}1.3^3&0\\0&0.5^3\end{pmatrix}",
                      r"\approx\begin{pmatrix}2.2&0\\0&0.125\end{pmatrix}", font_size=42, color=C_SIG)
        dg3.move_to([0, -1.1, 0])
        self.say("And the middle is easy to read. Sigma is diagonal, which means it only holds the singular "
                 "values, one for each direction. Multiplying diagonal matrices just multiplies the matching "
                 "entries. So sigma three times in a row cubes each singular value on its own. In our example,"
                 " one point three becomes about two point two, and zero point five becomes zero point one two"
                 " five. No direction disturbs another.", FadeOut(VGroup(e1, prod2, c5, res2, ok)), FadeIn(top3))
        self.cue("Sigma is diagonal", FadeIn(dg))
        self.cue("So sigma three times", FadeIn(dg3[0]))
        self.cue("In our example", FadeIn(dg3[1]))
        self.hold()

        # 07: the two attempts, and one more Wᵀ W
        rows = VGroup(MathTex(r"W^{\top}W", r"=", r"V\,\Sigma^2\,V^{\top}", font_size=46),
                      MathTex(r"W\,W^{\top}W", r"=", r"U\,\Sigma^3\,V^{\top}", font_size=46),
                      MathTex(r"W\,W^{\top}W\,W^{\top}W", r"=", r"U\,\Sigma^5\,V^{\top}", font_size=46))
        for r_, y in zip(rows, (1.6, 0.4, -0.8)):
            r_.shift(np.array([0.6, y, 0]) - r_[1].get_center())
        notes = VGroup(txt("lost a rotation", 26, C_S5).next_to(rows[0], RIGHT, buff=0.5),
                       txt("kept both", 26, C_PLUS).next_to(rows[1], RIGHT, buff=0.5),
                       txt("kept both", 26, C_PLUS).next_to(rows[2], RIGHT, buff=0.5))
        self.say("Look back at the two attempts. Two copies of W lost a rotation. Three copies kept both, and "
                 "only the singular values changed. And we can keep going. Attach another W transpose times W,"
                 " and the same cancelling happens again. U and V transpose stay where they are, and the "
                 "middle gains two more sigmas.", FadeOut(VGroup(top3, dg, dg3)))
        self.cue("Two copies of W", FadeIn(rows[0]), FadeIn(notes[0]))
        self.cue("Three copies kept both", FadeIn(rows[1]), FadeIn(notes[1]))
        self.cue("Attach another", FadeIn(rows[2]))
        self.cue("U and V transpose stay", FadeIn(notes[2]))
        self.hold()

        # 08: the odd products
        odd = VGroup(*[MathTex(a, r"\;\leadsto\;", b, font_size=44) for a, b in
                       ((r"W", r"\sigma"), (r"W\,W^{\top}W", r"\sigma^3"),
                        (r"W\,W^{\top}W\,W^{\top}W", r"\sigma^5"))])
        for m, y in zip(odd, (1.5, 0.5, -0.5)):
            m[2].set_color(C_SIG)
            m.shift(np.array([1.2, y, 0]) - m[1].get_center())
        self.say("So the products with an odd number of copies are the ones we can use. W itself carries "
                 "sigma. Three copies carry sigma cubed. Five copies carry sigma to the fifth, and so on.", FadeOut(rows), FadeOut(notes))
        self.cue("W itself carries", FadeIn(odd[0], shift=RIGHT * 0.2))
        self.cue("Three copies carry", FadeIn(odd[1], shift=RIGHT * 0.2))
        self.cue("Five copies carry", FadeIn(odd[2], shift=RIGHT * 0.2))
        self.hold()

        # 09: a mix is a polynomial p; one step cannot do it; two terms
        mix = MathTex(r"a\,W+b\,W\,W^{\top}W+\cdots", r"=", r"U\,(a\,\Sigma+b\,\Sigma^3+\cdots)\,V^{\top}", font_size=40)
        mix.move_to([0, 2.1, 0])
        pdef = MathTex(r"\sigma\ \longmapsto\ ", r"a\,\sigma+b\,\sigma^3+\cdots", r"\ =\ p(\sigma)", font_size=40)
        pdef.move_to([0, 1.3, 0])
        pdef[1:].set_color(C_SIG)
        want = mt(r"\text{want: }\ p(\sigma)=1\ \text{ for every }\sigma", 36).move_to([0, 0.6, 0])
        wx = Line(want.get_left(), want.get_right(), color=C_S5, stroke_width=4)
        tiny = mt(r"\text{a tiny }\sigma\text{ gives a tiny }p(\sigma)", 34, C_S5).move_to([0, 0.0, 0])
        rep = mt(r"\sigma\ \to\ p(\sigma)\ \to\ p(p(\sigma))\ \to\ \cdots\ \to\ 1", 40, C_PLUS).move_to([0, -0.9, 0])
        one = mt(r"p(\sigma)=a\,\sigma\qquad\text{only rescales}", 36, GREY_B).move_to([0, -1.9, 0])
        guess = mt(r"p(\sigma)=a\,\sigma+b\,\sigma^3", 46).move_to([0, -1.9, 0])
        self.say("Every one of these products has the same U on the left and the same V transpose on the "
                 "right. So if we multiply each product by a number and add them up, U and V transpose factor "
                 "out, and only the middle is a sum. In that middle, each singular value becomes a number "
                 "times sigma, plus a number times sigma cubed, and so on. A sum of powers like this is a "
                 "polynomial. Call it p. So turning W into U times V transpose now means one thing. We need a "
                 "p that sends every sigma to one. Can p do that in a single step? Then it would have to give "
                 "one for every input. But p is made of powers of sigma, so a tiny sigma always gives a tiny "
                 "output. One step is not enough. So we ask for less. One step only has to bring sigma closer "
                 "to one, and then we apply p again and again. Which p? Every extra term costs more matrix "
                 "products, so we want as few as possible. One term alone, a times sigma, only rescales every "
                 "singular value by the same number, so the ellipse stays an ellipse. So take two terms, a "
                 "times sigma plus b times sigma cubed.", *[Indicate(m[0], color=WHITE, scale_factor=1.05) for m in odd])
        self.cue("So if we multiply each product", FadeOut(odd), FadeIn(mix))
        self.cue("each singular value becomes", FadeIn(pdef[:2]))
        self.cue("Call it p", FadeIn(pdef[2]))
        self.cue("We need a p that sends", FadeIn(want))
        self.cue("But p is made of powers", FadeIn(tiny))
        self.cue("One step is not enough", Create(wx))
        self.cue("So we ask for less", FadeIn(rep))
        self.cue("One term alone", FadeIn(one))
        self.cue("So take two terms", FadeOut(one), FadeIn(guess))
        self.hold()

        # 10: wish one, p(1) = 1
        p1 = MathTex(r"p(1)", r"=a\cdot1+b\cdot1^3", r"=a+b", font_size=42).move_to([0, 1.3, 0])
        w1 = mt(r"\text{wish 1:}\quad a+b=1", 42, C_PLUS).move_to([0, 0.2, 0])
        self.say("What should a and b be? We want the repeated steps to settle at one. So a sigma that has "
                 "reached one must stay there, or the steps would never settle. Put sigma equals one into p. "
                 "One cubed is still one, so p gives a plus b. For one to stay at one, a plus b must equal "
                 "one. Call this our first wish.", FadeOut(VGroup(mix, pdef, want, wx, tiny)), guess.animate.move_to([0, 2.6, 0]),
                 rep.animate.move_to([0, -2.4, 0]).set_opacity(0.6))
        self.cue("Put sigma equals one", FadeIn(p1[:2]))
        self.cue("so p gives", FadeIn(p1[2]))
        self.cue("must equal one", FadeIn(w1))
        self.hold()

        # 11: wish two, the error near 1 is multiplied by a + 3b
        l1 = MathTex(r"p(1+e)", r"=a\,(1+e)+b\,(1+e)^3", font_size=42).move_to([-0.6, 1.5, 0])
        cube = mt(r"(1+e)^3=1+3e+3e^2+e^3\approx1+3e", 36, GREY_A).move_to([0, 0.7, 0])
        exm = mt(r"1.1^3=1.331\approx1.3", 32, GREY_B).next_to(cube, DOWN, buff=0.22)
        assert abs(1.1 ** 3 - 1.331) < 1e-12
        ls = VGroup(mt(r"\approx a\,(1+e)+b\,(1+3e)", 42), mt(r"=(a+b)+(a+3b)\,e", 42), mt(r"=1+(a+3b)\,e", 42))
        for m, y in zip(ls, (-0.6, -1.3, -2.0)):
            m.move_to([0, y, 0]).align_to(l1[1], LEFT)
        err = mt(r"\text{error: }\quad e\ \ \longrightarrow\ \ (a+3b)\,e", 38, C_SIG).move_to([0, 0.5, 0])
        w2 = mt(r"\text{wish 2:}\quad a+3b=0", 42, C_PLUS).scale(0.8).move_to([4.7, 2.0, 0])
        self.say("Staying at one is not enough. A sigma that is only close to one has to move closer. So take "
                 "a sigma that misses one by a small error e, and put one plus e into p. We need the cube of "
                 "one plus e. Multiplied out, it is one, plus three e, plus terms with e squared and e cubed. "
                 "When e is small, those last terms are far smaller still, so we drop them. For example, one "
                 "point one cubed is one point three three, very close to one point three. So p gives a times "
                 "one plus e, plus b times one plus three e. Collect the pieces, and that is a plus b, plus a "
                 "plus three b times e. The first piece, a plus b, is one, by our first wish. So p gives one, "
                 "plus a plus three b times e. We went in with an error of e, and we came out with an error of"
                 " a plus three b times e. One step multiplies the error by a plus three b. We want the error "
                 "to shrink, and the most it can shrink is all the way to nothing. So our second wish is that "
                 "a plus three b equals zero.", FadeOut(p1), FadeOut(rep), w1.animate.scale(0.8).move_to([4.7, 2.6, 0]))
        self.cue("put one plus e into p", FadeIn(l1))
        self.cue("Multiplied out", FadeIn(cube))
        self.cue("For example", FadeIn(exm))
        self.cue("So p gives", FadeIn(ls[0]))
        self.cue("Collect the pieces", FadeIn(ls[1]))
        self.cue("The first piece", Indicate(w1, color=C_PLUS), FadeIn(ls[2]))
        self.cue("We went in with", FadeOut(VGroup(cube, exm)), FadeIn(err))
        self.cue("So our second wish", FadeIn(w2), Indicate(ls[2][0][3:8], color=C_PLUS))
        self.hold()

        # 12: solve; the polynomial and the matrix step
        both = VGroup(mt(r"a+b=1", 44, C_PLUS), mt(r"a+3b=0", 44, C_PLUS)).arrange(RIGHT, buff=1.2)
        both.move_to([0, 1.5, 0])
        sol = VGroup(mt(r"a=-3b", 42), mt(r"-3b+b=1\ \ \Longrightarrow\ \ b=-\tfrac12", 42), mt(r"a=\tfrac32", 42))
        sol.arrange(DOWN, buff=0.35).move_to([0, -0.4, 0])
        px = MathTex(r"p(\sigma)", r"=", r"\tfrac32\,\sigma-\tfrac12\,\sigma^3", font_size=60)
        px[2].set_color(C_P)
        px.move_to([0, 0.8, 0])
        box = SurroundingRectangle(px, color=C_P, buff=0.25, corner_radius=0.1)
        step = mt(r"W\ \leftarrow\ \tfrac32\,W-\tfrac12\,W\,W^{\top}W", 46).move_to([0, -1.2, 0])
        self.say("Two wishes and two unknowns, which is exactly enough. The second wish says a equals minus "
                 "three b. Put that into the first, and minus three b plus b equals one, so b is minus one "
                 "half. Then a is three halves. So p of sigma is three halves sigma, minus one half sigma "
                 "cubed. For the matrix, one step is three halves W, minus one half W times W transpose times "
                 "W. That is the Newton–Schulz step, and you could have invented it yourself.", FadeOut(VGroup(l1, ls, err)), ReplacementTransform(w1, both[0]),
                 ReplacementTransform(w2, both[1]))
        self.cue("The second wish says", FadeIn(sol[0]))
        self.cue("Put that into the first", FadeIn(sol[1]))
        self.cue("is three halves", FadeIn(sol[2]))
        self.cue("So p of sigma is", FadeOut(VGroup(both, sol)), ReplacementTransform(guess, px), Create(box))
        self.cue("For the matrix", FadeIn(step))
        self.hold(1.0)

        # 13: the question this episode leaves open
        q = mt(r"\sigma\;\to\;p(\sigma)\;\to\;p(p(\sigma))\;\to\;\cdots\;\to\;?", 42, GREY_A).move_to([0, -1.2, 0])
        self.say("We built p from what happens close to one. But a real sigma can start anywhere. So take any "
                 "positive sigma and apply p over and over. Where does it end up? That is the question in part"
                 " (e) of the worksheet.", FadeOut(step), FadeIn(q, shift=UP * 0.2))
        self.hold(0.6)
        self.clear_stage()

    # ------------------------------------------------------------ the closing card
    def closing(self):
        self.ep1_closing()

    def ep1_closing(self):
        """Where we stand, and the question for next time. No answer is given here."""
        goal = VGroup(txt("goal:", 28, GREY_A), MathTex(r"UV^{\top}", font_size=44, color=C_PLUS))
        goal.arrange(RIGHT, buff=0.25).move_to([0, 2.5, 0])
        step = mt(r"W\ \leftarrow\ \tfrac32\,W-\tfrac12\,W\,W^{\top}W", 44).move_to([0, 1.3, 0])
        px = MathTex(r"p(\sigma)", r"=", r"\tfrac32\,\sigma-\tfrac12\,\sigma^3", font_size=52)
        px[2].set_color(C_P)
        px.move_to([0, 0.0, 0])
        q = mt(r"\sigma\;\to\;p(\sigma)\;\to\;p(p(\sigma))\;\to\;\cdots\;\to\;?", 44, C_SIG).move_to([0, -1.6, 0])
        self.say("So this is where we stand. We wanted U times V transpose without computing an SVD. Matrix "
                 "products alone gave us a polynomial, and two wishes fixed its two numbers. What we have not "
                 "seen is the iteration itself. We only know what p does close to one. Where a sigma ends up "
                 "when it starts far from one, we find out next time.")
        self.cue("We wanted U times V transpose", FadeIn(goal))
        self.cue("Matrix products alone", FadeIn(step))
        self.cue("and two wishes fixed", FadeIn(px))
        self.cue("Where a sigma ends up", FadeIn(q, shift=UP * 0.2))
        self.sign_off()
