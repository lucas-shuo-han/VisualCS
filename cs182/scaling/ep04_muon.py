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


class Ep04Muon(NarratedScene):
    series = SERIES

    def construct(self):
        self.title_card()
        self.recap()
        self.commute()
        self.iterate()
        self.demo()
        self.tuned()
        self.muon()
        self.end_card(
            ["Muon steps along U Vᵀ, scaled by root d_out over d_in",
             "Odd matrix polynomials change singular values but keep the singular vectors",
             "Iterating 1.5x minus 0.5x cubed pushes singular values in (0, 1] toward one",
             "Newton-Schulz replaces the SVD, and a few tuned iterations are good enough"],
        )

    # ---------------------------------------------------------------- 1
    def recap(self):
        head = self.heading("Recap: the RMS step")
        eq = mts([r"\Delta W^{*}=-\eta", r"\sqrt{\dfrac{d_{\rm out}}{d_{\rm in}}}", r"\,U_rV_r^{\top}"], 1.0, {1: C_WIDTH}).move_to([0, 1.8, 0])
        tag = txt("Muon, key idea 1", 30, C_LOSS).next_to(eq, DOWN, buff=0.3)
        self.say("Last time the RMS ball gave the step minus eta, root d_out over d_in, times U V transpose. Muon's first key idea.",
                 Write(head), Write(eq), FadeIn(tag))
        prob = txt("But computing U Vᵀ needs an SVD every step: expensive", 30, C_TEXT).move_to([0, -0.4, 0])
        self.say("The catch: computing U V transpose needs an SVD of the gradient at every step, and that is expensive.", FadeIn(prob))
        obs = VGroup(txt("1.  a direction that is approximately right is good enough", 28, C_TEXT),
                     txt("2.  Newton-Schulz iterations  (Muon, key idea 2)", 28, C_LOSS)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.55, 0])
        assert obs.width < 12.5 and obs.get_bottom()[1] > -2.5
        self.say("Two observations: an approximate direction is good enough, and Newton-Schulz can produce it cheaply.",
                 FadeIn(obs[0]), FadeIn(obs[1]))
        self.hold(0.4)
        self.clear_stage()
        head = self.heading("The goal")
        a = mts([r"A=U\Sigma V^{\top}", r"\ \longrightarrow\ ", r"UV^{\top}"], 1.1, {0: C_SV, 2: C_STEP}).move_to([0, 1.5, 0])
        b = txt("replace every singular value by 1", 30, GREY_A).move_to([0, 0.3, 0])
        c = mts([r"f(U\Sigma V^{\top})\approx UV^{\top}"], 1.0).move_to([0, -0.9, 0])
        self.say("We want a cheap function f that turns U sigma V transpose into U V transpose: every singular value replaced by one.",
                 Write(head), Write(a), FadeIn(b), Write(c))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 2
    def commute(self):
        head = self.heading("Step 1: odd polynomials commute with the SVD")
        pdef = mts([r"p(X)=a_0X+a_1XX^{\top}X+a_2(XX^{\top})^2X+\cdots"], 0.85).move_to([0, 2.5, 0])
        ex = mts([r"\text{e.g. }p(X)=\tfrac32X-\tfrac12XX^{\top}X"], 0.85).move_to([0, 1.6, 0])
        self.say("Take odd matrix polynomials: X, X X transpose X, and so on. Example: three halves X minus a half X X transpose X.",
                 Write(head), Write(pdef), Write(ex))
        d1 = mts([r"p(U\Sigma V^{\top})=\tfrac32U\Sigma V^{\top}-\tfrac12(U\Sigma V^{\top})(V\Sigma^{\top}U^{\top})U\Sigma V^{\top}"], 0.7).move_to([0, 0.6, 0])
        d2 = mts([r"=\tfrac32U\Sigma V^{\top}-\tfrac12U\Sigma\Sigma^{\top}\Sigma V^{\top}"], 0.7).move_to([0, -0.4, 0])
        d3 = mts([r"=U\Big[\tfrac32\Sigma-\tfrac12\Sigma\Sigma^{\top}\Sigma\Big]V^{\top}=U\,", r"p(\Sigma)", r"\,V^{\top}"], 0.7, {1: C_SV}).move_to([0, -1.4, 0])
        assert max(x.width for x in (d1, d2, d3)) < 13.4, [x.width for x in (d1, d2, d3)]
        self.say("Plug in the SVD. The V transposes and U's in the middle cancel, because U and V have orthonormal columns.",
                 Write(d1), Write(d2))
        self.say("What is left is U times p applied to the singular values, times V transpose. The singular vectors are untouched.", Write(d3))
        chk = txt(f"numerical check on a 5 × 3 matrix: difference {np.abs(PX - U @ np.diag(p(S0)) @ Vt).max():.0e}", 26, GREY_A).move_to([0, -2.25, 0])
        self.say("So p can be applied to a whole matrix while changing only its singular values, with no SVD needed.", FadeIn(chk))
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
        self.say("Can we find p so that repeatedly applying it sends every positive singular value to one? Try this cubic.",
                 Write(head), Write(peq), Create(ax), Create(curve), Create(diag), FadeIn(tl))
        pts = [ax.c2p(ORB[0], 0)]
        for a, b in zip(ORB[:-1], ORB[1:]):
            pts += [ax.c2p(a, b), ax.c2p(b, b)]
        web = VMobject(stroke_color=C_STEP, stroke_width=3).set_points_as_corners(pts)
        fx = Dot(ax.c2p(1, 1), color=C_STEP, radius=0.1)
        vals = VGroup(*[txt(f"{v:.3f}", 24, C_STEP) for v in ORB[:6]]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, 0.3, 0])
        assert vals.get_bottom()[1] > -2.5
        self.say(f"Start at 0.3 and bounce between the curve and the diagonal: {ORB[1]:.2f}, {ORB[2]:.2f}, {ORB[3]:.2f}, and on toward one.",
                 Create(web, run_time=3.0), FadeIn(fx), LaggedStart(*[FadeIn(v) for v in vals], lag_ratio=0.4, run_time=3.0))
        self.say("The point one is a fixed point that attracts everything nearby. Iterating p, singular values in the interval zero to one climb to one.",
                 Flash(ax.c2p(1, 1), color=C_STEP, flash_radius=0.4))
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
        self.say("Zoom out. Start at 2.5 and the iteration jumps to minus four, then twenty-seven, and diverges.",
                 Write(head), Create(ax), Create(curve), Create(diag), Create(web), FadeIn(txs))
        fro = mts([r"X\leftarrow\dfrac{G}{\|G\|_F}"], 1.0).move_to([3.9, -0.8, 0])
        self.say("So singular values must start inside zero to one. Dividing by the Frobenius norm guarantees it.",
                 Write(fro))
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
        self.say(f"Take a random 5 by 3 gradient, normalized. Its singular values are {S0[0]:.2f}, {S0[1]:.2f} and {S0[2]:.2f}.",
                 Write(head), Create(base), Create(one), FadeIn(onel), FadeIn(cur), FadeIn(curl), FadeIn(kt))
        for k in range(1, 4):
            nb, nl = bars(ITS[k]), labels(ITS[k])
            self.say({1: "One iteration of p lifts the small ones the most.",
                      2: "Another one, and the spread between them is shrinking.",
                      3: "After three iterations, all three are within about one tenth of one."}[k],
                     Transform(cur, nb), Transform(curl, nl), Transform(kt, txt(f"iteration {k}", 30, C_TEXT).move_to([3.7, 1.9, 0])))
        nb, nl = bars(ITS[6]), labels(ITS[6])
        self.say(f"By iteration six the smallest is {ITS[6].min():.3f}. Almost the same as replacing the singular values by exactly one.",
                 Transform(cur, nb), Transform(curl, nl), Transform(kt, txt("iteration 6", 30, C_TEXT).move_to([3.7, 1.9, 0])))
        small = VGroup(txt("the slow case: a tiny value", 26, GREY_A),
                       txt(f"from 0.01: {K_SMALL} iterations to 0.99", 26, C_LOSS)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, 0.3, 0])
        assert small.get_right()[0] < 7.0 and small.get_left()[0] > 0.7, (small.get_left(), small.get_right())
        self.say(f"A tiny singular value grows only about one and a half times per step, so from 0.01 it takes {K_SMALL} iterations.",
                 FadeIn(small))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 5
    def tuned(self):
        head = self.heading("Tune the coefficients")
        gen = mts([r"p(x)=a\,x+b\,x^3+c\,x^5+\cdots"], 0.9).move_to([-2.6, 2.6, 0])
        self.say("We may choose the coefficients. Higher orders may converge faster, but each step costs more.",
                 Write(head), Write(gen))
        nano = mts([r"f(x)=3.444\,x-4.7750\,x^3+2.0315\,x^5"], 0.85).move_to([-2.6, 1.7, 0])
        note = txt(f"NanoGPT speedrun  ·  f(1) = {Q1:.2f}, not 1", 26, C_LOSS).move_to([-2.6, 0.95, 0])
        self.say(f"The NanoGPT speedrun uses these three coefficients. Notice f of one is {Q1:.2f}, not one. So it does not converge to one.",
                 Write(nano), FadeIn(note))
        ax = make_axes([0, 1.2, 0.2], [0, 1.4, 0.5], 6.4, 2.6).move_to([-2.9, -0.95, 0])
        assert ax.get_bottom()[1] > -2.45, ax.get_bottom()
        band = Rectangle(width=ax.x_length, height=(1.2 - 0.7) / 1.4 * ax.y_length, stroke_width=0, fill_color=C_MUP, fill_opacity=0.18)
        band.move_to(ax.c2p(0.6, 0.95))
        c5 = polyline(ax, xs, Y5, C_STEP, 3)
        pl = txt("five iterations of f", 24, C_STEP).move_to([3.9, -0.3, 0])
        rng_t = txt(f"inputs 0.01 to 1  →  outputs {Y5.min():.2f} to {Y5.max():.2f}", 24, C_MUP).move_to([3.5, -1.1, 0])
        pl2 = txt(f"plain p, five iterations: 0.01 → {PLAIN5:.2f}", 24, C_LOSS).move_to([3.5, -1.8, 0])
        assert rng_t.get_right()[0] < 7.05 and pl2.get_right()[0] < 7.05, (rng_t.get_right(), pl2.get_right())
        self.say(f"Five iterations send every input from 0.01 up to between {Y5.min():.2f} and {Y5.max():.2f}. Noisy, but far from tiny.",
                 Create(ax), FadeIn(band), Create(c5), FadeIn(pl), FadeIn(rng_t))
        self.say("Must it converge? No. Singular values roughly one are good enough, and much faster than the plain cubic.",
                 FadeIn(pl2))
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
        self.say("Put it together: Muon stands for momentum orthogonalized by Newton-Schulz.", Write(head), FadeIn(name))
        self.say("Keep a momentum buffer, orthogonalize it with a few Newton-Schulz steps, and step the weights against it.",
                 FadeIn(code, shift=UP * 0.2))
        self.play(Create(code.line_box(1)))
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
        self.say("On the NanoGPT speedrun, Muon costs about the same time per step as Adam, and far less than Shampoo or SOAP.",
                 Write(head), FadeIn(sub), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.2))
        self.say("Per step it also gets the validation loss down faster, so it reaches a given loss in less wall-clock time.",
                 Indicate(bars[4][0], color=C_STEP))
        self.hold(0.3)
        self.clear_stage()
        head = self.heading("The speedrun record")
        pts = [("baseline", 45, C_STD), ("modernized + tuned LR", 31, C_MODEL), ("Muon introduced", 25, C_STEP), ("later record", 4, C_MUP)]
        rows = VGroup()
        for i, (nm, mnt, col) in enumerate(pts):
            r = Rectangle(width=max(mnt, 0.3) * 0.16, height=0.5, stroke_color=col, fill_color=col, fill_opacity=0.35, stroke_width=3)
            r.move_to([-4.6 + r.width / 2, 1.6 - 0.85 * i, 0])
            lab = txt(nm, 24, GREY_A).next_to(r, RIGHT, buff=0.2)
            v = txt(f"≈ {mnt} min", 26, col).next_to(lab, RIGHT, buff=0.3)
            rows.add(VGroup(r, lab, v))
        assert rows.get_bottom()[1] > -2.5 and rows.get_right()[0] < 7.0, rows.get_center()
        self.say("The task took about 45 minutes at the May 2024 baseline. Muon was a big step down, and by December the record was a few minutes.",
                 Write(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.6))
        kimi = txt("Feb 2025: “Muon is Scalable for LLM Training”", 26, C_TEXT).move_to([0, -1.9, 0])
        assert kimi.width < 13
        self.say("In February 2025, Moonshot AI and UCLA showed that Muon scales to large language model training.", FadeIn(kimi))
        self.hold(0.5)
