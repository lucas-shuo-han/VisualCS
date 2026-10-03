"""Episode 3 — Ridge: Distrusting Weak Directions (Note 2, section 2.2; Lecture 2 and 3; HW1 problem 3)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers

# (a) the two closed forms agree (n = 5 < d = 8)
_rng = np.random.RandomState(3)
XR = _rng.randn(5, 8)
YR = _rng.randn(5)
LAM_T = 0.7
W_PRIMAL = np.linalg.solve(XR.T @ XR + LAM_T * np.eye(8), XR.T @ YR)
W_KERNEL = XR.T @ np.linalg.solve(XR @ XR.T + LAM_T * np.eye(5), YR)
assert np.allclose(W_PRIMAL, W_KERNEL)
# ... and match the SVD sum  sum_i  sigma_i/(sigma_i^2+lam) v_i u_i^T y
U, S, VT = np.linalg.svd(XR, full_matrices=False)
W_SVD = sum(S[i] / (S[i] ** 2 + LAM_T) * VT[i] * (U[:, i] @ YR) for i in range(5))
assert np.allclose(W_PRIMAL, W_SVD)

# (b) filters
LAMS = [0.035, 0.35, 3.5]
LAM_COL = ["#FFC078", ORANGE, "#C25E00"]
SIGS = np.linspace(0.0, 1.5, 151)
r_filter = lambda s, lam: s ** 2 / (s ** 2 + lam)
coef = lambda s, lam: s / (s ** 2 + lam)
for lam in LAMS:
    sp = np.sqrt(lam)
    assert abs(coef(sp, lam) - 1 / (2 * sp)) < 1e-12                                    # peak of the multiplier
    grid = np.linspace(1e-3, 5, 5000)
    assert abs(coef(grid, lam).max() - 1 / (2 * sp)) < 1e-3                             # ... is its maximum
assert abs(r_filter(0.5, 0.25) - 0.5) < 1e-12                                            # sigma = sqrt(lam): half kept

# (c) conditioning of X^T X + lambda I for sigma = (2, 0.5): eigenvalues (4, 0.25)
EIG = (4.0, 0.25)
LAM_R = [0.0, 0.25, 1.0]
KAP = [(EIG[0] + l) / (EIG[1] + l) for l in LAM_R]
assert np.allclose(KAP, [16, 8.5, 4])
RHO = [(k - 1) / (k + 1) for k in KAP]
ITS = [int(np.ceil(np.log(0.01) / np.log(r))) for r in RHO]
assert ITS == [37, 20, 10], ITS

# (d) noise per singular direction:  y~_i = sigma_i c_i + eps_i,  eps ~ N(0, s^2)
SIGD = np.array([3.0, 1.0, 0.3, 0.1])
CTRUE = np.array([1.0, -1.0, 0.2, -0.2])
NS = 0.1
LAM_D = 0.1
rr = SIGD ** 2 / (SIGD ** 2 + LAM_D)
MSE_OLS = (NS / SIGD) ** 2
MSE_RIDGE = ((1 - rr) * CTRUE) ** 2 + rr ** 2 * (NS / SIGD) ** 2
assert np.allclose(NS / SIGD, [0.0333333, 0.1, 0.3333333, 1.0], atol=1e-6)
_rs = np.random.RandomState(5)
TRIALS = 30
EPS = _rs.randn(TRIALS, 4) * NS
YT = SIGD * CTRUE + EPS
C_OLS = YT / SIGD
C_RIDGE = SIGD * YT / (SIGD ** 2 + LAM_D)
assert np.allclose(C_RIDGE, rr * C_OLS)
_big = _rs.randn(200000, 4) * NS
_yo = SIGD * CTRUE + _big
assert np.allclose(((_yo / SIGD - CTRUE) ** 2).mean(0), MSE_OLS, rtol=0.05)
assert np.allclose(((SIGD * _yo / (SIGD ** 2 + LAM_D) - CTRUE) ** 2).mean(0), MSE_RIDGE, rtol=0.05)
TOT_OLS, TOT_RIDGE = float(MSE_OLS.sum()), float(MSE_RIDGE.sum())
assert TOT_OLS > 10 * TOT_RIDGE and abs(TOT_OLS - 1.1222) < 1e-3
# if the weak direction carried a large true coefficient, ridge would pay in bias
BIAS_LARGE = float((1 - rr[3]) ** 2 * 1.0 ** 2 + rr[3] ** 2 * (NS / SIGD[3]) ** 2)
assert BIAS_LARGE < MSE_OLS[3] + 1e-9 and (1 - rr[3]) > 0.9                              # here it still wins on MSE, but almost all the signal is lost

# (e) weight decay and MAP
ETA_W, LAM_W = 0.1, 0.5
DECAY = 1 - 2 * ETA_W * LAM_W
assert abs(DECAY - 0.9) < 1e-12
WD = [DECAY ** t for t in range(16)]
SIGY2, TAU2 = 0.25, 2.5
assert abs(SIGY2 / TAU2 - 0.1) < 1e-12
# ridge gradient step == weight decay + data step
_w = np.array([1.0, -2.0, 0.5])
_X = np.array([[1.0, 0.0, 2.0], [0.0, 1.0, 1.0]])
_y = np.array([1.0, 0.5])
_g = 2 * _X.T @ (_X @ _w - _y) + 2 * LAM_W * _w
assert np.allclose(_w - ETA_W * _g, DECAY * _w - ETA_W * 2 * _X.T @ (_X @ _w - _y))

# (f) lambda cannot be learned by minimizing the objective
WFIX = np.array([1.0, 2.0])                 # some weight vector
RES = 3.0                                   # its squared residual
OBJ = lambda lam: RES + lam * float(WFIX @ WFIX)
assert OBJ(0.0) < OBJ(1.0) < OBJ(2.0)


class Ep03Ridge(NarratedScene):
    series = SERIES
    SCENES = ["objective", "filters", "conditioning", "noise", "weight_decay"]

    def construct(self):
        self.title_card()
        self.objective()
        self.filters()
        self.conditioning()
        self.noise()
        self.weight_decay()
        self.end_card(
            ["Ridge: squared error, plus lambda times the squared weight norm",
             "It keeps strong directions and squashes weak ones toward zero",
             "That stops noise in weak directions from blowing up, and shrinks kappa",
             "In gradient descent it's weight decay. Pick lambda on held-out data, not the objective"],
        )

    # ---------------------------------------------------------------- 1. objective
    def objective(self):
        head = self.heading("Ridge regression")
        obj = mts([r"\vec w_{\rm ridge}=\arg\min_{\vec w}\ \|X\vec w-\vec y\|_2^2+", r"\lambda", r"\|\vec w\|_2^2"], 0.85, {1: C_LAM})
        obj.move_to([0, 2.0, 0])
        prim = mts([r"\vec w_{\rm ridge}=(X^\top X+", r"\lambda", r"I_d)^{-1}X^\top\vec y"], 0.85, {1: C_LAM}).move_to([0, 0.6, 0])
        kern = mts([r"=X^\top(XX^\top+", r"\lambda", r"I_n)^{-1}\vec y"], 0.85, {1: C_LAM}).next_to(prim, DOWN, buff=0.35)
        kern.align_to(prim[0], LEFT).shift(RIGHT * 0.0)
        assert_on_screen(obj, prim, kern)
        self.say("What if we simply charge a price for big weights? That's ridge regression, and the price is called "
                 "lambda. With that penalty in place there's always exactly one answer, even when the data alone "
                 "can't decide.",
                 Write(head), Write(obj))
        note1 = txt("d × d inverse", 24, GREY_B).next_to(prim, RIGHT, buff=0.4)
        note2 = txt("n × n inverse: cheaper when features outnumber samples", 22, GREY_B).next_to(kern, DOWN, buff=0.3)
        assert_on_screen(note1, note2)
        self.say("Set the gradient to zero and a closed form pops out, which inverts X transpose X with lambda added "
                 "on the diagonal. There's also a second form, which inverts a matrix with one row per sample "
                 "instead. Both give the same answer, so we use whichever matrix is smaller.",
                 Write(prim))
        self.cue("There's also a second form", Write(kern), FadeIn(note1), FadeIn(note2))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 2. filters
    def filters(self):
        head = self.heading("What ridge does to each singular direction")
        svd = mts([r"\vec w_{\rm ridge}=\sum_i", r"\frac{\sigma_i}{\sigma_i^2+\lambda}", r"\,\vec v_i\,\vec u_i^\top\vec y"], 0.8, {1: C_LAM})
        svd.move_to([0, 2.5, 0])
        pinv = mts([r"\text{pseudoinverse: }\frac{1}{\sigma_i}", r"\ \ \ \text{ridge keeps }\ r_\lambda(\sigma)=\frac{\sigma^2}{\sigma^2+\lambda}"], 0.7, {1: C_LAM}).move_to([0, 1.5, 0])
        assert_on_screen(svd, pinv)
        self.say("So what does ridge actually do to the solution? Take the SVD, and each singular direction gets its "
                 "own multiplier. The pseudoinverse would use one over sigma there, so ridge keeps only a fraction "
                 "of that, and this fraction is the ridge filter.",
                 Write(head), Write(svd))
        self.cue("The pseudoinverse", Write(pinv))
        self.hold(0.3)
        self.play(FadeOut(svd), FadeOut(pinv))
        ax = make_axes([0, 1.5, 0.5], [0, 1.0, 0.5], 8.0, 3.0).move_to([-1.6, 0.3, 0])
        xt = VGroup(*[txt(f"{v:g}", 20, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.15) for v in (0, 0.5, 1.0, 1.5)])
        yt = VGroup(*[txt(f"{v:g}", 20, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.15) for v in (0, 0.5, 1)])
        xl = txt("singular value σ", 22, GREY_B).next_to(ax.x_axis, DOWN, buff=0.5)
        yl = txt("fraction of pseudoinverse kept", 22, GREY_B).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        one = DashedLine(ax.c2p(0, 1), ax.c2p(1.5, 1), color=GREY_A, stroke_width=2)
        curves = VGroup(*[plot(ax, lambda s, l=lam: r_filter(s, l), col, [0.0, 1.5], 4) for lam, col in zip(LAMS, LAM_COL)])
        labs = VGroup(*[txt(f"λ = {lam:g}", 22, col) for lam, col in zip(LAMS, LAM_COL)])
        for lab, lam in zip(labs, LAMS):
            lab.next_to(ax.c2p(1.5, r_filter(1.5, lam)), RIGHT, buff=0.15)
        labs[0].shift(UP * 0.05)
        assert_on_screen(VGroup(ax, xt, yt, xl, yl, labs))
        half = Dot(ax.c2p(np.sqrt(LAMS[1]), 0.5), radius=0.1, color=YELLOW_D)
        hl = txt("σ = √λ keeps half", 21, YELLOW_D).next_to(half, DOWN, buff=0.25).shift(RIGHT * 0.9)
        assert_on_screen(hl)
        self.say("Let's plot that fraction against the singular value, for three values of lambda. Strong directions "
                 "are left almost alone, while weak ones get squashed toward zero. The cutoff sits where sigma "
                 "equals the square root of lambda, and there exactly half is kept. So a bigger lambda slides the "
                 "cutoff to the right.",
                 Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), Create(one))
        self.cue("Strong directions", LaggedStart(*[Create(c) for c in curves], lag_ratio=0.4, run_time=2.5),
                 LaggedStart(*[FadeIn(l) for l in labs], lag_ratio=0.4, run_time=2.5))
        self.cue("The cutoff sits", Create(curves[1].copy().set_stroke(YELLOW_D, 7)), FadeIn(half), FadeIn(hl))
        self.hold(0.3)
        self.clear_stage()
        # coefficient multiplier
        head = self.heading("Ridge caps the amplification")
        ax = make_axes([0, 1.5, 0.5], [0, 5, 1], 8.0, 3.2).move_to([-1.6, 0.4, 0])
        xt = VGroup(*[txt(f"{v:g}", 20, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.15) for v in (0, 0.5, 1.0, 1.5)])
        yt = VGroup(*[txt(f"{v:g}", 20, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.15) for v in (0, 1, 2, 3, 4, 5)])
        xl = txt("singular value σ", 22, GREY_B).next_to(ax.x_axis, DOWN, buff=0.5)
        yl = txt("multiplier on uᵢᵀy", 22, GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        xs = np.linspace(0.2, 1.5, 200)
        inv = DashedVMobject(polyline(ax, xs, 1 / xs, GREY_A, 3), num_dashes=40)
        invl = txt("1/σ, no ridge", 22, GREY_A).next_to(ax.c2p(0.32, 3.4), RIGHT, buff=0.2)
        xs2 = np.linspace(0.0, 1.5, 300)
        rc = VGroup(*[polyline(ax, xs2, coef(xs2, lam), col, 4) for lam, col in zip(LAMS, LAM_COL)])
        assert_on_screen(VGroup(ax, xt, yt, xl, yl))
        peaks = VGroup(*[Dot(ax.c2p(np.sqrt(l), 1 / (2 * np.sqrt(l))), radius=0.09, color=YELLOW_D) for l in LAMS if np.sqrt(l) <= 1.5])
        pk = txt("peak 1/(2√λ) at σ = √λ", 21, YELLOW_D).move_to([3.4, 1.8, 0])
        assert_on_screen(pk)
        self.say("Now here's the multiplier itself. With no ridge it's one over sigma, which explodes as sigma "
                 "shrinks toward zero. Ridge tames that, so the curve rises, peaks where sigma equals the square "
                 "root of lambda, and then falls again.",
                 Write(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
        self.cue("With no ridge", Create(inv), FadeIn(invl))
        self.cue("Ridge tames that", LaggedStart(*[Create(c) for c in rc], lag_ratio=0.4, run_time=2.5), FadeIn(peaks), FadeIn(pk))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 3. conditioning
    def conditioning(self):
        head = self.heading("Ridge also improves conditioning")
        mat = mts([r"X^\top X+\lambda I", r"\ \text{has eigenvalues}\ \ \sigma_i^2+\lambda"], 0.85, {}).move_to([0, 2.5, 0])
        assert_on_screen(mat)
        colx = [-4.2, -1.4, 1.4, 4.4]
        hdr = ["ridge λ", "condition number κ", "rate (κ−1)/(κ+1)", "steps for 100×"]
        hdrs = VGroup(*[txt(h, 24, GREY_B).move_to([colx[j], 1.2, 0]) for j, h in enumerate(hdr)])
        rows = VGroup()
        for i in range(3):
            y = 0.5 - 0.6 * i
            col = C_LAM if i else WHITE
            rows.add(VGroup(txt(f"{LAM_R[i]:g}", 30, col).move_to([colx[0], y, 0]),
                            txt(f"{KAP[i]:g}", 30, col).move_to([colx[1], y, 0]),
                            txt(f"{RHO[i]:.3f}", 30, col).move_to([colx[2], y, 0]),
                            txt(f"{ITS[i]}", 30, col).move_to([colx[3], y, 0])))
        ex = txt("eigenvalues 4 and 1/4, as in episode 1", 22, GREY_B).move_to([0, -1.5, 0])
        assert_on_screen(hdrs, rows, ex)
        self.say("There's a bonus as well. Adding lambda lifts every eigenvalue by the same amount, so the tiny ones "
                 "gain the most in proportion. Take the ravine from episode one, where kappa was sixteen. A ridge "
                 "lambda of one quarter cuts that to eight and a half, and a ridge lambda of one brings it down "
                 "to four.",
                 Write(head), Write(mat), run_time=1.0)
        self.cue("Take the ravine", FadeIn(hdrs), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.4), FadeIn(ex))
        self.say("So the steps we need drop from thirty-seven to ten. The catch is that we're now solving a "
                 "different problem, and it has a different answer.",
                 Indicate(rows[1], color=C_LAM), Indicate(rows[2], color=C_LAM))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 4. noise
    def noise(self):
        head = self.heading("Why distrust weak directions?")
        setup = mts([r"\tilde y_i=\sigma_i c_i+\varepsilon_i", r",\ \ \varepsilon_i\sim N(0,0.1^2)"], 0.75, {}).move_to([0, 2.55, 0])
        assert_on_screen(setup)
        ys = 0.6
        y0 = 0.35
        xs = [-4.8, -1.6, 1.6, 4.8]
        pos = lambda v: y0 + v * ys
        base = VGroup(*[Line([x - 1.1, pos(c), 0], [x + 1.1, pos(c), 0], color=WHITE, stroke_width=3) for x, c in zip(xs, CTRUE)])
        axis = Line([-6.4, y0, 0], [6.4, y0, 0], color=GREY_D, stroke_width=1)
        cols = VGroup(*[txt(f"σ = {s:g}", 24, C_TEXT).move_to([x, -1.38, 0]) for x, s in zip(xs, SIGD)])
        stds = VGroup(*[txt(f"noise ×{1 / s:.0f}" if 1 / s == round(1 / s) else f"noise ×{1 / s:.1f}", 21, C_LOSS).move_to([x, -1.72, 0]) for x, s in zip(xs, SIGD)])
        ols = VGroup(); rid = VGroup()
        for j, x in enumerate(xs):
            for k in range(TRIALS):
                jit = (k % 6 - 2.5) * 0.06
                ols.add(Dot([x - 0.45 + jit, pos(C_OLS[k, j]), 0], radius=0.045, color=C_MODEL))
                rid.add(Dot([x + 0.45 + jit, pos(C_RIDGE[k, j]), 0], radius=0.045, color=C_LAM))
        for d in list(ols) + list(rid):
            assert -1.4 < d.get_center()[1] < 2.4, d.get_center()
        lg1 = txt("no ridge: estimate of c", 22, C_MODEL).move_to([-4.6, 2.05, 0])
        lg2 = txt("ridge, λ = 0.1", 22, C_LAM).move_to([-1.7, 2.05, 0])
        lg3 = txt("true c", 22, WHITE).move_to([0.8, 2.05, 0])
        assert_on_screen(cols, stds, lg1, lg2, lg3)
        assert abs(1 / SIGD[-1] - 10) < 1e-9 and round(TOT_OLS / TOT_RIDGE) == 12
        self.say("But why should we distrust weak directions at all? Let's put a small true signal in each direction "
                 "and add a little noise. Without ridge we divide by sigma, so the weakest direction blows its "
                 "noise up ten times, and you can see those estimates scatter.",
                 Write(head), Write(setup), Create(axis), FadeIn(cols), Create(base), FadeIn(lg3))
        self.cue("Without ridge", FadeIn(stds), LaggedStart(*[FadeIn(d) for d in ols], lag_ratio=0.01, run_time=2.0), FadeIn(lg1))
        tot = txt(f"total squared error: {TOT_OLS:.2f} without ridge, {TOT_RIDGE:.2f} with", 24, YELLOW_D).move_to([0, -2.32, 0])
        assert_on_screen(tot)
        self.say("Now turn ridge on. The weak directions collapse toward zero, while the strong ones barely move. "
                 "Averaged over the noise, the total error drops about twelve-fold. So overfitting is really "
                 "trusting noisy directions too much, and ridge is a judgment call to trust them less.",
                 FadeIn(lg2))
        self.cue("The weak directions", LaggedStart(*[FadeIn(d) for d in rid], lag_ratio=0.01, run_time=2.0), lead=0.6)
        self.cue("Averaged over", FadeIn(tot))
        self.cue("So overfitting", Indicate(cols[3], color=YELLOW_D))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 5. weight decay, MAP, lambda
    def weight_decay(self):
        head = self.heading("Ridge in gradient descent: weight decay")
        gd = mts([r"\vec w_{t+1}=", r"(1-2\eta\lambda)\,\vec w_t", r"-2\eta X^\top(X\vec w_t-\vec y)"], 0.85, {1: C_LAM}).move_to([0, 2.4, 0])
        assert_on_screen(gd)
        ax = make_axes([0, 15, 5], [0, 1, 0.5], 6.0, 2.4).move_to([-3.0, -0.3, 0])
        pts = [(t, WD[t]) for t in range(16)]
        cur = polyline(ax, [p[0] for p in pts], [p[1] for p in pts], C_LAM, 4)
        dd = VGroup(*[Dot(ax.c2p(*p), radius=0.06, color=C_LAM) for p in pts])
        xt = VGroup(*[txt(f"{v}", 20, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.15) for v in (0, 5, 10, 15)])
        yt = VGroup(*[txt(f"{v:g}", 20, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.15) for v in (0, 0.5, 1)])
        lab = txt(f"no data gradient: 0.9^t (η = {ETA_W}, λ = {LAM_W})", 22, C_LAM).next_to(ax, DOWN, buff=0.5)
        assert_on_screen(VGroup(ax, lab, xt, yt))
        self.say("Inside gradient descent, ridge turns out to be simple. We shrink the weights a little, and then we "
                 "take the usual data step. On its own, that shrink keeps ninety percent of a weight each step. "
                 "It's called weight decay, and here it's the same thing as ridge.",
                 Write(head), Write(gd))
        self.cue("On its own", Create(ax), FadeIn(xt), FadeIn(yt), Create(cur), FadeIn(dd), FadeIn(lab))
        bay = mts([r"\vec y\mid\vec w\sim N(X\vec w,\sigma_y^2I),\ \ \vec w\sim N(0,\tau^2I)", r"\ \Rightarrow\ \lambda=\sigma_y^2/\tau^2"], 0.6, {}).move_to([3.1, 0.9, 0])
        bay.scale_to_fit_width(5.8) if bay.width > 5.8 else None
        bay.move_to([3.5, 0.9, 0])
        num = txt(f"σy² = {SIGY2}, τ² = {TAU2}  gives  λ = {SIGY2 / TAU2:g}", 22, C_LAM).next_to(bay, DOWN, buff=0.3)
        assert_on_screen(bay, num)
        self.say("There's a Bayesian view of this too. Assume Gaussian noise on the labels and a Gaussian prior on "
                 "the weights, and the MAP estimate is exactly ridge. The ridge lambda is then the noise variance "
                 "divided by the prior variance.",
                 FadeIn(bay))
        self.cue("The ridge lambda is then", FadeIn(num))
        self.hold(0.3)
        self.play(FadeOut(bay), FadeOut(num))
        self.clear_stage(head)
        # cannot learn lambda
        ax2 = make_axes([0, 2, 0.5], [0, 14, 2], 6.0, 3.0).move_to([-2.3, -0.1, 0])
        line = ax2.plot(lambda l: OBJ(l), x_range=[0, 2], color=C_LOSS, stroke_width=4)
        xt = VGroup(*[txt(f"{v:g}", 20, GREY_B).next_to(ax2.c2p(v, 0), DOWN, buff=0.15) for v in (0, 1, 2)])
        xl = txt("λ", 24, C_LAM).next_to(ax2.x_axis.get_end(), RIGHT, buff=0.15)
        yl = txt("objective at a fixed w", 22, GREY_B).next_to(ax2, UP, buff=0.15).align_to(ax2, LEFT)
        z = Dot(ax2.c2p(0, OBJ(0)), radius=0.12, color=YELLOW_D)
        zt = txt("minimized at λ = 0", 24, YELLOW_D).next_to(z, RIGHT, buff=0.3).shift(DOWN * 0.35)
        assert_on_screen(VGroup(ax2, xt, xl, yl, zt))
        self.say("So why not let the optimizer choose lambda as well? Because the objective only grows with lambda, "
                 "so it would just slide down to zero. That makes lambda a hyperparameter, which we pick on "
                 "held-out data, and that's next, along with two more hyperparameters.",
                 Create(ax2), FadeIn(xt), FadeIn(xl), FadeIn(yl), Create(line))
        self.cue("so it would just slide", FadeIn(z), FadeIn(zt))
        self.cue("That makes lambda", Indicate(zt, color=YELLOW_D))
        self.hold(0.6)
        self.clear_stage()
