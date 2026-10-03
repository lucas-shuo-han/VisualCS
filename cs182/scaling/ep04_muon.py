"""Episode 4 — Muon: Orthogonalize Cheaply (Lecture 8: Newton-Schulz iterations, the Muon optimizer)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers

rng = np.random.RandomState(0)
GG = rng.randn(5, 3)
U, S, Vt = np.linalg.svd(GG, full_matrices=False)
FRO = float(np.linalg.norm(GG))
S0 = S / FRO                                    # singular values after Frobenius normalization
assert (S0 > 0).all() and (S0 <= 1).all() and abs(S0[0] - 0.840) < 1e-3 and abs(S0[2] - 0.183) < 1e-3

# (a) odd polynomials act on the singular values only
p = lambda x: 1.5 * x - 0.5 * x ** 3
X0 = GG / FRO
PX = 1.5 * X0 - 0.5 * X0 @ X0.T @ X0
assert np.allclose(PX, U @ np.diag(p(S0)) @ Vt)

# (b) iterating p on a scalar
def orbit(x, n):
    xs = [x]
    for _ in range(n):
        xs.append(p(xs[-1]))
    return xs


ORB = orbit(0.3, 6)
assert all(a < b for a, b in zip(ORB, ORB[1:])) and ORB[-1] > 0.98
assert abs(p(1) - 1) < 1e-12 and abs(p(-1) + 1) < 1e-12
OUT = orbit(2.5, 3)
assert OUT[1] < -4 and abs(OUT[2]) > 20 and abs(OUT[3]) > abs(OUT[2])            # outside sqrt(3) it blows up

# (c) singular values through NS iterations
ITS = [np.array(S0)]
for _ in range(8):
    ITS.append(p(ITS[-1]))
assert ITS[-1].min() > 0.99 and ITS[0].min() < 0.2
NS_K = next(k for k, v in enumerate(ITS) if v.min() > 0.9)
Xk = X0.copy()
for _ in range(8):
    Xk = 1.5 * Xk - 0.5 * Xk @ Xk.T @ Xk
assert np.allclose(Xk, U @ Vt, atol=1e-2)                   # the matrix itself approaches U V^T


def iters_to(x, thr=0.99):
    k = 0
    while x < thr:
        x, k = p(x), k + 1
    return k


K_SMALL = iters_to(0.01)
assert K_SMALL == 14

# (d) the tuned quintic from the NanoGPT speedrun
QA, QB, QC = 3.444, -4.7750, 2.0315
q = lambda x: QA * x + QB * x ** 3 + QC * x ** 5
Q1 = q(1.0)
assert abs(Q1 - 0.7005) < 1e-3
def q5(x):
    for _ in range(5):
        x = q(x)
    return x


xs = np.linspace(0.01, 1.0, 2000)
Y5 = q5(xs)
assert 0.68 < Y5.min() and Y5.max() < 1.25, (Y5.min(), Y5.max())
PLAIN5 = orbit(0.01, 5)[-1]
assert PLAIN5 < 0.1 and q5(0.01) > 0.68

# numbers read off the slides (NanoGPT speedrun, Jordan et al.), ms/step
MS = [("Adam", 139), ("Shampoo (update every 32)", 154), ("Shampoo (every 10)", 179), ("SOAP", 301), ("Muon", 142)]

# the numbers the narration says out loud
assert [f"{v:.2f}" for v in ORB[:4]] == ["0.30", "0.44", "0.61", "0.80"]
assert (OUT[0], f"{OUT[1]:.1f}", f"{OUT[2]:.0f}") == (2.5, "-4.1", "27")
assert [f"{v:.2f}" for v in S0] == ["0.84", "0.51", "0.18"]
assert f"{ITS[3].min():.2f}" == "0.56" and f"{ITS[6].min():.2f}" == "0.99"
assert f"{Q1:.2f}" == "0.70" and (f"{Y5.min():.2f}", f"{Y5.max():.2f}") == ("0.68", "1.13") and f"{PLAIN5:.2f}" == "0.08"


class Ep04Muon(NarratedScene):
    series = SERIES
    SCENES = ["recap", "commute", "iterate", "demo", "tuned", "muon"]

    def construct(self):
        self.title_card()
        self.recap()
        self.commute()
        self.iterate()
        self.demo()
        self.tuned()
        self.muon()
        self.end_card(
            ["Muon steps along U V transpose, scaled by root d_out over d_in",
             "Odd matrix polynomials reshape the singular values and leave the singular vectors alone",
             "Iterate three halves x minus one half x cubed, and singular values between zero and one climb to one",
             "Newton-Schulz stands in for the SVD, and a few tuned iterations are close enough"],
        )

    # ---------------------------------------------------------------- 1
    def recap(self):
        head = self.heading("Recap: the RMS step")
        eq = mts([r"\Delta W^{*}=-\eta", r"\sqrt{\dfrac{d_{\rm out}}{d_{\rm in}}}", r"\,U_rV_r^{\top}"], 1.0, {1: C_WIDTH}).move_to([0, 1.8, 0])
        tag = txt("Muon, key idea 1", 30, C_LOSS).next_to(eq, DOWN, buff=0.3)
        prob = txt("But computing U Vᵀ needs an SVD every step: expensive", 30, C_TEXT).move_to([0, -0.4, 0])
        self.say("Last time we found the step we want. It's U V transpose, scaled by the square root of d_out over "
                 "d_in, and that's the first key idea of Muon. The catch is that getting U V transpose means an SVD of "
                 "the gradient at every step, and that's expensive.")
        self.play(Write(head), Write(eq))
        self.cue("and that's the first key idea", FadeIn(tag))
        self.cue("The catch is", FadeIn(prob))
        obs = VGroup(txt("1.  a direction that is approximately right is good enough", 28, C_TEXT),
                     txt("2.  Newton-Schulz iterations  (Muon, key idea 2)", 28, C_LOSS)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.55, 0])
        assert obs.width < 12.5 and obs.get_bottom()[1] > -2.5
        self.say("There are two ways out of this. First, we don't need the exact direction, because one that's "
                 "approximately right is good enough. And second, a trick called the Newton-Schulz iteration gets us "
                 "there cheaply, which is Muon's second key idea.")
        self.cue("First, we don't need", FadeIn(obs[0]))
        self.cue("And second", FadeIn(obs[1]))
        self.hold(0.4)
        self.clear_stage()
        head = self.heading("The goal")
        a = mts([r"A=U\Sigma V^{\top}", r"\ \longrightarrow\ ", r"UV^{\top}"], 1.1, {0: C_SV, 2: C_STEP}).move_to([0, 1.5, 0])
        b = txt("replace every singular value by 1", 30, GREY_A).move_to([0, 0.3, 0])
        c = mts([r"f(U\Sigma V^{\top})\approx UV^{\top}"], 1.0).move_to([0, -0.9, 0])
        self.say("So here's the goal. We want a cheap function that takes U sigma V transpose and hands back U V "
                 "transpose. In other words, it should replace every singular value with one.")
        self.play(Write(head), Write(a))
        self.cue("In other words", FadeIn(b), Write(c))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 2
    def commute(self):
        head = self.heading("Step 1: odd polynomials commute with the SVD")
        pdef = mts([r"p(X)=a_0X+a_1XX^{\top}X+a_2(XX^{\top})^2X+\cdots"], 0.85).move_to([0, 2.5, 0])
        ex = mts([r"\text{e.g. }p(X)=\tfrac32X-\tfrac12XX^{\top}X"], 0.85).move_to([0, 1.6, 0])
        self.say("Let's try odd polynomials of a matrix. They're built from X, then X times X transpose times X, and "
                 "so on up. Here's one example, with three halves on the first term and minus one half on the second.")
        self.play(Write(head), Write(pdef))
        self.cue("Here's one example", Write(ex))
        d1 = mts([r"p(U\Sigma V^{\top})=\tfrac32U\Sigma V^{\top}-\tfrac12(U\Sigma V^{\top})(V\Sigma^{\top}U^{\top})U\Sigma V^{\top}"], 0.7).move_to([0, 0.6, 0])
        d2 = mts([r"=\tfrac32U\Sigma V^{\top}-\tfrac12U\Sigma\Sigma^{\top}\Sigma V^{\top}"], 0.7).move_to([0, -0.4, 0])
        d3 = mts([r"=U\Big[\tfrac32\Sigma-\tfrac12\Sigma\Sigma^{\top}\Sigma\Big]V^{\top}=U\,", r"p(\Sigma)", r"\,V^{\top}"], 0.7, {1: C_SV}).move_to([0, -1.4, 0])
        assert max(x.width for x in (d1, d2, d3)) < 13.4, [x.width for x in (d1, d2, d3)]
        self.say("Now plug in the SVD. In the middle, V transpose meets V and then U transpose meets U. Both pairs "
                 "cancel, because their columns are orthonormal. What's left is U, then p of the singular values, then "
                 "V transpose.")
        self.play(Write(d1))
        self.cue("Both pairs cancel", Write(d2))
        self.cue("What's left is", Write(d3))
        chk = txt(f"numerical check on a 5 × 3 matrix: difference {np.abs(PX - U @ np.diag(p(S0)) @ Vt).max():.0e}", 26, GREY_A).move_to([0, -2.25, 0])
        self.say("So here's the trick. The polynomial acts on the whole matrix, but it only touches the singular "
                 "values. The singular vectors don't budge. That means we can reshape the singular values without ever "
                 "computing an SVD.")
        self.play(Indicate(d3[1], color=C_SV))
        self.cue("That means we can", FadeIn(chk))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 3
    def iterate(self):
        head = self.heading("Step 2: find p that pushes values to 1")
        peq = mts([r"p(x)=\tfrac32x-\tfrac12x^3"], 0.9).move_to([3.4, 2.5, 0])
        ax = make_axes([0, 1.5, 0.5], [0, 1.2, 0.5], 6.4, 3.4).move_to([-2.4, 0.1, 0])
        curve = plot(ax, p, C_MODEL, [0, 1.5], width=5)
        diag = ax.plot(lambda x: x, x_range=[0, 1.2], color=GREY_B, stroke_width=3)
        tl = VGroup(*[txt(f"{v:g}", 20, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.12) for v in (0.5, 1.0, 1.5)])
        self.say("Now we need a polynomial that, applied over and over, drives every singular value to one. Let's try "
                 "this cubic, which is three halves x minus one half x cubed.")
        self.play(Write(head), Create(ax), FadeIn(tl))
        self.cue("Let's try this cubic", Write(peq), Create(curve), Create(diag))
        pts = [ax.c2p(ORB[0], 0)]
        for a, b in zip(ORB[:-1], ORB[1:]):
            pts += [ax.c2p(a, b), ax.c2p(b, b)]
        web = VMobject(stroke_color=C_STEP, stroke_width=3).set_points_as_corners(pts)
        fx = Dot(ax.c2p(1, 1), color=C_STEP, radius=0.1)
        vals = VGroup(*[txt(f"{v:.3f}", 24, C_STEP) for v in ORB[:6]]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, 0.3, 0])
        assert vals.get_bottom()[1] > -2.5
        self.say("Start at zero point three, and bounce between the curve and the diagonal. You get zero point four "
                 "four, then zero point six one, then zero point eight, creeping up toward one. That's because one is "
                 "a fixed point that pulls its neighbors in, so anything between zero and one climbs up to it.")
        self.play(FadeIn(vals[0]))
        self.cue("and bounce between", Create(web, run_time=6.0),
                 LaggedStart(*[FadeIn(v) for v in vals[1:]], lag_ratio=0.5, run_time=6.0))
        self.cue("That's because one", FadeIn(fx), Flash(ax.c2p(1, 1), color=C_STEP, flash_radius=0.4))
        self.hold(0.3)
        self.clear_stage()
        head = self.heading("But only inside a safe range")
        ax = make_axes([-3, 3, 1], [-6, 3, 1], 6.4, 3.6).move_to([-2.4, 0.2, 0])
        curve = plot(ax, p, C_MODEL, [-2.6, 2.6], width=5)
        diag = ax.plot(lambda x: x, x_range=[-3, 3], color=GREY_B, stroke_width=3)
        pts = [ax.c2p(OUT[0], 0), ax.c2p(OUT[0], OUT[1])]
        web = VMobject(stroke_color=C_LOSS, stroke_width=3).set_points_as_corners(pts)
        txs = VGroup(txt(f"2.5  →  {OUT[1]:.1f}  →  {OUT[2]:.1f}  →  {OUT[3]:.0f}", 30, C_LOSS),
                     txt("diverges beyond √3 ≈ 1.73", 26, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.9, 1.0, 0])
        assert txs.get_right()[0] < 7.0 and txs.get_left()[0] > 0.6, (txs.get_left(), txs.get_right())
        fro = mts([r"X\leftarrow\dfrac{G}{\|G\|_F}"], 1.0).move_to([3.9, -0.8, 0])
        self.say("But zoom out, and there's a danger. Start at two point five, and it jumps to minus four point one, "
                 "then to about twenty-seven, and off it goes. So the singular values have to start between zero and "
                 "one. Dividing by the Frobenius norm makes sure of that.")
        self.play(Write(head), Create(ax), Create(curve), Create(diag))
        self.cue("Start at two point five", Create(web), FadeIn(txs))
        self.cue("So the singular values", Write(fro))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 4
    def demo(self):
        head = self.heading("Newton-Schulz on a real gradient")
        base_y, sc = -1.4, 3.6
        xs = [-3.6, -2.2, -0.8]

        def bars(vals, col=C_SV):
            g = VGroup()
            for x, v in zip(xs, vals):
                r = Rectangle(width=0.9, height=max(v, 0.01) * sc, stroke_color=col, fill_color=col, fill_opacity=0.35, stroke_width=3)
                r.move_to([x, base_y + max(v, 0.01) * sc / 2, 0])
                g.add(r)
            return g

        def labels(vals):
            return VGroup(*[txt(f"{v:.2f}", 26, C_SV).move_to([x, base_y - 0.35, 0]) for x, v in zip(xs, vals)])

        one = DashedLine([-5.2, base_y + sc, 0], [0.4, base_y + sc, 0], color=C_STEP, stroke_width=2)
        onel = txt("1", 24, C_STEP).next_to(one, LEFT, buff=0.1)
        base = Line([-5.2, base_y, 0], [0.4, base_y, 0], color=GREY_D, stroke_width=2)
        cur = bars(ITS[0]); curl = labels(ITS[0])
        kt = txt("iteration 0", 30, C_TEXT).move_to([3.7, 1.9, 0])
        assert base_y + sc < 3.0

        def to_iter(k):
            return [Transform(cur, bars(ITS[k])), Transform(curl, labels(ITS[k])),
                    Transform(kt, txt(f"iteration {k}", 30, C_TEXT).move_to([3.7, 1.9, 0]))]

        self.say("Let's run it on a real gradient, five by three and normalized. Its singular values start at zero "
                 "point eight four, zero point five one and zero point one eight.")
        self.play(Write(head), Create(base), Create(one), FadeIn(onel), FadeIn(cur), FadeIn(curl), FadeIn(kt))
        self.say("After one iteration, the small values get the biggest boost in proportion. After another, the gap "
                 "between them keeps shrinking. And after three, the top two are nearly one, while the smallest is "
                 "still catching up at zero point five six.")
        self.play(*to_iter(1))
        self.cue("After another", *to_iter(2))
        self.cue("And after three", *to_iter(3))
        small = VGroup(txt("the slow case: a tiny value", 26, GREY_A),
                       txt(f"from 0.01: {K_SMALL} iterations to 0.99", 26, C_LOSS)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, 0.3, 0])
        assert small.get_right()[0] < 7.0 and small.get_left()[0] > 0.7, (small.get_left(), small.get_right())
        self.say("By iteration six, even the smallest has reached zero point nine nine, which is practically U V "
                 "transpose. The slow case is a tiny value, since it only grows about one and a half times per "
                 "iteration. Starting from zero point zero one, it takes fourteen iterations to get close.")
        self.play(*to_iter(6))
        self.cue("The slow case", FadeIn(small))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 5
    def tuned(self):
        head = self.heading("Tune the coefficients")
        gen = mts([r"p(x)=a\,x+b\,x^3+c\,x^5+\cdots"], 0.9).move_to([-2.6, 2.6, 0])
        nano = mts([r"f(x)=3.444\,x-4.7750\,x^3+2.0315\,x^5"], 0.85).move_to([-2.6, 1.7, 0])
        note = txt(f"NanoGPT speedrun  ·  f(1) = {Q1:.2f}, not 1", 26, C_LOSS).move_to([-2.6, 0.95, 0])
        self.say("But who says it has to be this cubic? Higher powers can converge faster, though each iteration costs "
                 "more. The NanoGPT speedrun uses a fifth-degree polynomial with these tuned coefficients.")
        self.play(Write(head), Write(gen))
        self.cue("The NanoGPT speedrun", Write(nano))
        ax = make_axes([0, 1.2, 0.2], [0, 1.4, 0.5], 6.4, 2.6).move_to([-2.9, -0.95, 0])
        assert ax.get_bottom()[1] > -2.45, ax.get_bottom()
        band = Rectangle(width=ax.x_length, height=(1.2 - 0.7) / 1.4 * ax.y_length, stroke_width=0, fill_color=C_MUP, fill_opacity=0.18)
        band.move_to(ax.c2p(0.6, 0.95))
        c5 = polyline(ax, xs, Y5, C_STEP, 3)
        pl = txt("five iterations of f", 24, C_STEP).move_to([3.9, -0.3, 0])
        rng_t = txt(f"inputs 0.01 to 1  →  outputs {Y5.min():.2f} to {Y5.max():.2f}", 24, C_MUP).move_to([3.5, -1.1, 0])
        pl2 = txt(f"plain p, five iterations: 0.01 → {PLAIN5:.2f}", 24, C_LOSS).move_to([3.5, -1.8, 0])
        assert rng_t.get_right()[0] < 7.05 and pl2.get_right()[0] < 7.05, (rng_t.get_right(), pl2.get_right())
        self.say("And look at what it does at one. It gives zero point seven, not one, so this iteration never settles "
                 "down at one. Yet five rounds of it lift every input, even one as small as zero point zero one, into "
                 "a band near one. It runs from zero point six eight to one point one three.")
        self.play(FadeIn(note))
        self.cue("Yet five rounds", Create(ax), FadeIn(band), Create(c5), FadeIn(pl))
        self.cue("It runs from", FadeIn(rng_t))
        self.say("So does it need to converge? Not really, because roughly one is good enough. And it gets there far "
                 "faster than the cubic. After five iterations, the cubic has only brought zero point zero one up to "
                 "zero point zero eight.")
        self.play(Indicate(band, color=C_MUP, scale_factor=1.03))
        self.cue("After five iterations", FadeIn(pl2))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 6
    def muon(self):
        head = self.heading("Muon")
        name = VGroup(txt("Mo", 44, C_STEP), txt("mentum ", 34, GREY_A), txt("O", 44, C_STEP), txt("rthogonalized by ", 34, GREY_A),
                      txt("N", 44, C_STEP), txt("ewton-", 34, GREY_A), txt("S", 44, C_STEP), txt("chulz", 34, GREY_A))
        name.arrange(RIGHT, buff=0.04, aligned_edge=DOWN).move_to([0, 2.5, 0])
        assert name.width < 12
        code = CodeListing([
            "B = mu * B + grad          # momentum",
            "O = newton_schulz(B)       # orthogonalize",
            "W = W - eta * O           # step",
        ], lang="python", font_size=28, line_gap=0.6).move_to([0, 0.7, 0])
        assert code.width < 12.5, code.width
        self.say("Now let's put it all together. Muon stands for momentum, orthogonalized by Newton-Schulz, and that "
                 "name is the whole algorithm. We keep a momentum buffer, orthogonalize it with a few Newton-Schulz "
                 "iterations, then step the weights against it.")
        self.play(Write(head))
        self.cue("Muon stands for", FadeIn(name))
        self.cue("We keep a momentum", FadeIn(code, shift=UP * 0.2))
        self.cue("orthogonalize it with", Create(code.line_box(1)))
        self.hold(0.3)
        self.clear_stage()
        # impact
        head = self.heading("Impact")
        base_y = -1.6
        sc = 3.0 / 301
        bars = VGroup()
        for i, (nm, v) in enumerate(MS):
            col = C_STEP if nm == "Muon" else C_MODEL
            r = Rectangle(width=1.5, height=v * sc, stroke_color=col, fill_color=col, fill_opacity=0.3, stroke_width=3)
            r.move_to([-5.0 + 2.5 * i, base_y + v * sc / 2, 0])
            lab = txt(nm, 20, GREY_A, line_spacing=0.85).next_to(r, DOWN, buff=0.12)
            lab.scale_to_fit_width(min(lab.width, 2.2))
            val = txt(f"{v} ms", 24, col).next_to(r, UP, buff=0.08)
            bars.add(VGroup(r, lab, val))
        assert bars.get_bottom()[1] > -2.5 and bars.get_top()[1] < 3.0 and bars.get_right()[0] < 7.0, bars.get_center()
        sub = txt("time per step, NanoGPT speedrun (read off the lecture slide)", 24, GREY_B).move_to([0, 2.65, 0])
        self.say("So is it worth it? Per step, Muon costs about what Adam does, and far less than Shampoo or SOAP. And "
                 "each step cuts the validation loss more, so it reaches a target loss in less wall-clock time.")
        self.play(Write(head), FadeIn(sub), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.2))
        self.cue("And each step", Indicate(bars[4][0], color=C_STEP))
        self.hold(0.3)
        self.clear_stage()
        head = self.heading("The speedrun record")
        pts = [("baseline", 45, C_STD), ("modernized + tuned LR", 31, C_MODEL), ("Muon introduced", 25, C_STEP), ("later record", 4, C_MUP)]
        assert (pts[0][1], pts[3][1]) == (45, 4)
        rows = VGroup()
        for i, (nm, mnt, col) in enumerate(pts):
            r = Rectangle(width=max(mnt, 0.3) * 0.16, height=0.5, stroke_color=col, fill_color=col, fill_opacity=0.35, stroke_width=3)
            r.move_to([-4.6 + r.width / 2, 1.6 - 0.85 * i, 0])
            lab = txt(nm, 24, GREY_A).next_to(r, RIGHT, buff=0.2)
            v = txt(f"≈ {mnt} min", 26, col).next_to(lab, RIGHT, buff=0.3)
            rows.add(VGroup(r, lab, v))
        assert rows.get_bottom()[1] > -2.5 and rows.get_right()[0] < 7.0, rows.get_center()
        self.say("Here's the record on the NanoGPT speedrun. Back in May of twenty twenty-four, the record stood at "
                 "about forty-five minutes. Muon helped bring that down, and by December it was about four minutes.")
        self.play(Write(head))
        self.cue("Back in May", FadeIn(rows[0]))
        self.cue("Muon helped", LaggedStart(FadeIn(rows[1]), FadeIn(rows[2]), lag_ratio=0.5))
        self.cue("and by December", FadeIn(rows[3]))
        kimi = txt("Feb 2025: “Muon is Scalable for LLM Training”", 26, C_TEXT).move_to([0, -1.9, 0])
        assert kimi.width < 13
        self.say("Then in February of twenty twenty-five, Moonshot and UCLA showed that Muon holds up for large "
                 "language models. So the recipe we started with, a linearized loss inside a norm ball, has turned "
                 "into a real optimizer.")
        self.play(FadeIn(kimi))
        self.hold(0.5)
