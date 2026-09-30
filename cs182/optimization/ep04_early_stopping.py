"""Episode 4 — Early Stopping and the Knobs (Note 2, sections 2.3-2.4; Lecture 2; Lecture 3)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers

# (a) GD in the SVD basis: w~_{t,i} = q_t(sigma_i) y~_i / sigma_i
ETA_F = 0.12
q_t = lambda s, eta, t: 1 - (1 - 2 * eta * s ** 2) ** t
SIGS = np.linspace(0, 1.5, 151)
TS_SHOW = [1, 3, 6, 20, 100]
assert ETA_F <= 1 / (2 * 1.5 ** 2)                          # monotone guarantee for sigma_max = 1.5
# check against an explicit GD run on a diagonal problem
_s, _y = 0.8, 1.7
_w = 0.0
for _t in range(1, 7):
    _w = _w - ETA_F * 2 * _s * (_s * _w - _y)
    assert abs(_w - q_t(_s, ETA_F, _t) * _y / _s) < 1e-12
LAM_R = 0.35
ridge_r = lambda s, lam: s ** 2 / (s ** 2 + lam)
Q6 = q_t(0.5, ETA_F, 6)
assert abs(Q6 - 0.3101) < 1e-3 and abs(ridge_r(0.5, LAM_R) - 0.4167) < 1e-3

# (b) overshoot outside the monotone range: sigma = 1.5
SG = 1.5
ET_OK, ET_BAD = 0.1, 0.3
assert ET_OK <= 1 / (2 * SG ** 2) < ET_BAD < 1 / SG ** 2
Q_OK = [q_t(SG, ET_OK, t) for t in range(9)]
Q_BAD = [q_t(SG, ET_BAD, t) for t in range(9)]
assert all(b >= a for a, b in zip(Q_OK, Q_OK[1:])) and max(Q_OK) < 1
assert max(Q_BAD) > 1.3 and Q_BAD[2] < 1 < Q_BAD[3]

# (c) expected errors along the GD path (four singular directions, as in episode 3)
SIGD = np.array([3.0, 1.0, 0.3, 0.1])
CTRUE = np.array([1.0, -1.0, 0.2, -0.2])
NS = 0.1
ETA_D = 0.05
assert ETA_D <= 1 / (2 * SIGD.max() ** 2)
T_GRID = np.unique(np.round(np.logspace(0, 4.3, 120)).astype(int))
QT = np.array([q_t(SIGD, ETA_D, t) for t in T_GRID])                # (T, 4)
PARAM_ERR = ((1 - QT) ** 2 * CTRUE ** 2 + QT ** 2 * (NS / SIGD) ** 2).sum(1)      # E |c_hat - c|^2
TRAIN = ((1 - QT) ** 2 * ((SIGD * CTRUE) ** 2 + NS ** 2)).sum(1)                  # E training residual
T0_ERR = float((CTRUE ** 2).sum())
T0_TRAIN = float(((SIGD * CTRUE) ** 2 + NS ** 2).sum())
K_STAR = int(np.argmin(PARAM_ERR))
T_STAR = int(T_GRID[K_STAR])
E_STAR = float(PARAM_ERR[K_STAR])
E_END = float(PARAM_ERR[-1])
assert 20 <= T_STAR <= 400 and E_STAR < 0.1 and E_END > 1.0 and E_END > 10 * E_STAR, (T_STAR, E_STAR, E_END)
assert all(b <= a + 1e-12 for a, b in zip(TRAIN, TRAIN[1:])) and TRAIN[-1] < 0.05 * T0_TRAIN
# Monte Carlo agreement at t_star
_r = np.random.RandomState(0)
_eps = _r.randn(100000, 4) * NS
_yt = SIGD * CTRUE + _eps
_q = q_t(SIGD, ETA_D, T_STAR)
assert abs((((_q * _yt / SIGD) - CTRUE) ** 2).sum(1).mean() - E_STAR) < 0.01

# (d) grid search cost
KVALS = 5
GRID_COST = [KVALS ** m for m in (1, 2, 3, 4, 6)]
assert GRID_COST == [5, 25, 125, 625, 15625]


def xlog(ax, t):
    return ax.c2p(np.log10(t), 0)[0]


class Ep04EarlyStopping(NarratedScene):
    series = SERIES

    def construct(self):
        self.title_card()
        self.svd_dynamics()
        self.compare()
        self.u_curve()
        self.knobs()
        self.end_card(
            ["In the SVD basis, gradient descent fits each direction on its own clock: strong directions first",
             "Stopping early keeps strong directions and attenuates weak ones, much like ridge, but it is not the same estimator",
             "In practice: checkpoint during training and keep the checkpoint that is best on validation data",
             "Regularization strength, learning rate and stopping time are hyperparameters: search them on log scales"],
        )

    # ---------------------------------------------------------------- 1. SVD dynamics
    def svd_dynamics(self):
        head = self.heading("Gradient descent in the SVD basis")
        defs = mts([r"\tilde w_t=V^\top w_t,\ \ \tilde y=U^\top y,\ \ X=U\Sigma V^\top"], 0.75, {}).move_to([0, 2.5, 0])
        rec = mts([r"\tilde w_{t+1,i}=", r"(1-2\eta\sigma_i^2)", r"\,\tilde w_{t,i}+2\eta\sigma_i\tilde y_i"], 0.85, {1: C_ETA}).move_to([0, 1.3, 0])
        sol = mts([r"\tilde w_{t,i}=", r"q_t(\sigma_i)", r"\,\frac{\tilde y_i}{\sigma_i},\ \ ", r"q_t(\sigma)=1-(1-2\eta\sigma^2)^t"], 0.85, {1: C_LAM, 3: C_LAM}).move_to([0, -0.1, 0])
        pinv = mts([r"\text{fully converged: }\tilde w_i=\tilde y_i/\sigma_i\ \ (q=1)"], 0.7, {}).move_to([0, -1.3, 0])
        assert_on_screen(defs, rec, sol, pinv)
        self.say("Rotate gradient descent into the SVD basis, with the weights and the targets rotated the same way.",
                 Write(head), Write(defs))
        self.say("Each singular direction obeys its own scalar recurrence, with factor one minus two eta sigma squared.",
                 Write(rec))
        self.say("Start at zero and solve it. Direction i reaches the fraction q t of the converged answer, y tilde over sigma.",
                 Write(sol), FadeIn(pinv))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 2. compare the filters
    def axes(self, ymax=1.0):
        ax = make_axes([0, 1.5, 0.5], [0, ymax, 0.5], 8.0, 3.2).move_to([-1.6, 0.3, 0])
        xt = VGroup(*[txt(f"{v:g}", 20, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.15) for v in (0, 0.5, 1.0, 1.5)])
        yt = VGroup(*[txt(f"{v:g}", 20, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.15) for v in (0, 0.5, 1)])
        xl = txt("singular value σ", 22, GREY_B).next_to(ax.x_axis, DOWN, buff=0.5)
        yl = txt("fraction of pseudoinverse coefficient", 22, GREY_B).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        one = DashedLine(ax.c2p(0, 1), ax.c2p(1.5, 1), color=GREY_A, stroke_width=2)
        return ax, VGroup(xt, yt, xl, yl, one)

    def compare(self):
        head = self.heading("Early stopping is a filter")
        ax, deco = self.axes()
        shades = [BLUE_E, BLUE_D, BLUE_C, TEAL_C, GREEN_C]
        cs = [plot(ax, lambda s, t=t: q_t(s, ETA_F, t), col, [0, 1.5], 4) for t, col in zip(TS_SHOW, shades)]
        labs = VGroup(*[txt(f"t = {t}", 22, col) for t, col in zip(TS_SHOW, shades)])
        for lab, t in zip(labs, TS_SHOW):
            lab.next_to(ax.c2p(1.5, q_t(1.5, ETA_F, t)), RIGHT, buff=0.15)
        order = sorted(range(len(labs)), key=lambda i: labs[i].get_center()[1])
        for a, b in zip(order, order[1:]):
            gap = labs[b].get_center()[1] - labs[a].get_center()[1]
            if gap < 0.36:
                labs[b].shift(UP * (0.36 - gap))
        assert_on_screen(VGroup(ax, deco, labs))
        self.say("Plot q t against sigma. After a few steps only large singular values are fit; small ones have barely started.",
                 Write(head), Create(ax), FadeIn(deco), Create(cs[0]), FadeIn(labs[0]), Create(cs[1]), FadeIn(labs[1]))
        self.say("Keep stepping and the curve rises from the right: large singular values converge first, small ones far later.",
                 LaggedStart(*[Create(c) for c in cs[2:]], lag_ratio=0.4, run_time=3), LaggedStart(*[FadeIn(l) for l in labs[2:]], lag_ratio=0.4, run_time=3))
        self.play(*[FadeOut(c) for c in cs if c is not cs[2]], *[FadeOut(l) for l in labs if l is not labs[2]])
        rc = plot(ax, lambda s: ridge_r(s, LAM_R), C_LAM, [0, 1.5], 4)
        rl = txt(f"ridge, λ = {LAM_R}", 22, C_LAM).next_to(ax.c2p(1.5, ridge_r(1.5, LAM_R)), RIGHT, buff=0.15).shift(DOWN * 0.1)
        assert_on_screen(rl)
        self.say("Compare with ridge. Both hold back weak directions, so stopping early regularizes without a penalty.",
                 Create(rc), FadeIn(rl))
        pit = txt("Same lesson, not the same estimator: the shapes differ, and stopping also depends on the start and the step size.", 24, YELLOW_D).move_to([0, 2.95, 0])
        pit.scale_to_fit_width(12.6) if pit.width > 12.6 else None
        pit.move_to([0, 3.0, 0])
        head2 = head
        assert_on_screen(pit, ymax=3.7)
        self.say("The curves need not coincide. What they share is the ordering: weak singular directions enter last.",
                 FadeOut(head), FadeIn(pit))
        self.hold(0.4)
        self.clear_stage()
        # overshoot footnote
        head = self.heading("A caveat on the ordering")
        ax = make_axes([0, 8, 1], [0, 1.5, 0.5], 7.0, 3.0).move_to([-2.5, -0.1, 0])
        xt = VGroup(*[txt(f"{v}", 20, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.15) for v in (0, 2, 4, 6, 8)])
        yt = VGroup(*[txt(f"{v:g}", 20, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.15) for v in (0, 0.5, 1, 1.5)])
        one = DashedLine(ax.c2p(0, 1), ax.c2p(8, 1), color=GREY_A, stroke_width=2)
        ok = polyline(ax, range(9), Q_OK, GREEN_C, 4)
        bad = polyline(ax, range(9), Q_BAD, C_LOSS, 4)
        okd = VGroup(*[Dot(ax.c2p(t, q), radius=0.06, color=GREEN_C) for t, q in enumerate(Q_OK)])
        badd = VGroup(*[Dot(ax.c2p(t, q), radius=0.06, color=C_LOSS) for t, q in enumerate(Q_BAD)])
        lab_ok = txt(f"η = {ET_OK}: rises to 1", 22, GREEN_C).move_to([4.3, 1.4, 0])
        lab_bad = txt(f"η = {ET_BAD}: overshoots", 22, C_LOSS).move_to([4.3, 0.7, 0])
        cond = mts([r"\eta\le\frac{1}{2\sigma_{\max}^2}\ \Rightarrow\ \text{monotone}"], 0.7, {}).move_to([4.2, -0.3, 0])
        cond2 = VGroup(mts([r"\frac{1}{2\sigma_{\max}^2}<\eta<\frac{1}{\sigma_{\max}^2}"], 0.7, {}), txt("stable, may overshoot", 22, C_LOSS)).arrange(DOWN, buff=0.15).move_to([4.2, -1.5, 0])
        assert_on_screen(VGroup(ax, xt, yt), lab_ok, lab_bad, cond, cond2)
        self.say("This ordering is guaranteed only for eta up to one over two sigma max squared: here sigma is 1.5, eta 0.1.",
                 Write(head), Create(ax), FadeIn(xt), FadeIn(yt), Create(one), Create(ok), FadeIn(okd), FadeIn(lab_ok), Write(cond))
        self.say("Up to one over sigma max squared, the largest directions overshoot: q t goes above one, then settles.",
                 Create(bad), FadeIn(badd), FadeIn(lab_bad), Write(cond2))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 3. U curve
    def u_curve(self):
        head = self.heading("When to stop")
        ax = Axes(x_range=[0, 4.3, 1], y_range=[0, 1.05, 0.5], x_length=8.2, y_length=3.0,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([-1.2, 0.6, 0])
        ticks = VGroup(*[txt(lab, 20, GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.15) for k, lab in enumerate(["1", "10", "100", "1000", "10⁴"])])
        xl = txt("gradient steps t", 22, GREY_B).next_to(ax.x_axis, DOWN, buff=0.5)
        yt = VGroup(*[txt(f"{v:g}", 20, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.15) for v in (0, 0.5, 1)])
        yl = txt("fraction of the starting value", 22, GREY_B).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        lt = np.log10(T_GRID)
        ctr = polyline(ax, lt, TRAIN / T0_TRAIN, C_TRAIN, 4)
        cer = polyline(ax, lt, PARAM_ERR / T0_ERR, C_TEST, 4)
        ltr = txt("training loss", 24, C_TRAIN).move_to([4.4, 1.6, 0])
        ler = txt("distance from the true weights", 22, C_TEST).move_to([4.5, 0.8, 0])
        setup = txt("four singular directions, σ = 3, 1, 0.3, 0.1", 22, GREY_B).move_to([3.9, 2.45, 0])
        assert_on_screen(VGroup(ax, ticks, xl, yt, yl), ltr, ler, setup)
        self.say("Now watch four directions, with singular values 3, 1, 0.3 and 0.1, noisy data, and a fixed step size.",
                 Write(head), Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yt), FadeIn(yl), FadeIn(setup))
        self.say("Training loss only ever falls: given enough steps, gradient descent fits every direction, noise included.",
                 Create(ctr, run_time=2.5), FadeIn(ltr))
        star = Dot(ax.c2p(np.log10(T_STAR), E_STAR / T0_ERR), radius=0.12, color=YELLOW_D)
        pick = txt(f"best: t ≈ {T_STAR}, error {E_STAR:.2f}", 24, YELLOW_D).next_to(star, UP, buff=0.9).shift(LEFT * 0.4)
        assert_on_screen(pick)
        self.say(f"The distance falls, then climbs as noisy weak directions are fit. Best stopping is near {T_STAR} steps.",
                 Create(cer, run_time=2.5), FadeIn(ler), FadeIn(star), FadeIn(pick))
        end = txt(f"run to convergence: error {E_END:.2f}, {E_END / E_STAR:.0f}× worse", 24, C_LOSS).move_to([3.3, -2.3, 0]).align_to([-6.4, 0, 0], LEFT)
        end.move_to([0.2, -2.05, 0])
        assert_on_screen(end)
        self.say("Run to convergence and the error is many times larger. Stopping early trades a little bias for much less noise.",
                 FadeIn(end))
        self.say("In practice, save checkpoints and keep the one with the best validation score, not an arbitrary step count.",
                 Indicate(star, color=YELLOW_D, scale_factor=2))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 4. knobs
    def knobs(self):
        head = self.heading("Selecting the control knobs")
        names = [("regularization λ", C_LAM), ("learning rate η", C_ETA), ("stopping time t", BLUE_C)]
        boxes = VGroup(*[box_label(n, c, w=3.6, h=0.9, font_size=26) for n, c in names]).arrange(RIGHT, buff=0.5).move_to([0, 2.2, 0])
        assert_on_screen(boxes)
        self.say("Regularization strength, learning rate and stopping time are hyperparameters spanning orders of magnitude.",
                 Write(head), LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in boxes], lag_ratio=0.3))
        ln = NumberLine(x_range=[-6, 2, 1], length=11.5, color=GREY_B, include_numbers=False, tick_size=0.1).move_to([0, 0.6, 0])
        lab = VGroup(*[mt(rf"10^{{{k}}}", 0.5, GREY_B).next_to(ln.n2p(k), DOWN, buff=0.2) for k in range(-6, 3, 2)])
        vals = np.linspace(12.5, 100, 8)
        lin = VGroup(*[Dot(ln.n2p(np.log10(v)), radius=0.07, color=C_LOSS) for v in vals])
        lg = VGroup(*[Dot(ln.n2p(x), radius=0.07, color=GREEN_C) for x in range(-6, 3)])
        cap1 = txt("8 evenly spaced values, 12.5 to 100", 22, C_LOSS).next_to(ln, UP, buff=0.25).align_to(ln, LEFT)
        cap2 = txt("one value per power of ten", 22, GREEN_C).next_to(ln, UP, buff=0.25).align_to(ln, LEFT)
        assert_on_screen(VGroup(ln, lab))
        self.say("So sweep on a log scale. Evenly spaced values bunch into one decade; one value per power of ten spans it all.",
                 FadeIn(ln), FadeIn(lab), FadeIn(cap1), LaggedStart(*[FadeIn(d) for d in lin], lag_ratio=0.1))
        self.play(FadeOut(cap1), FadeOut(lin), FadeIn(cap2), LaggedStart(*[FadeIn(d) for d in lg], lag_ratio=0.1))
        self.hold(0.3)
        self.play(FadeOut(ln), FadeOut(lab), FadeOut(cap2), FadeOut(lg))
        # roles of the sets
        roles = VGroup(box_label("training set: fits the weights", C_TRAIN, w=5.6, h=0.8, font_size=24),
                       box_label("validation set: picks among trained candidates", C_VAL, w=5.6, h=0.8, font_size=24),
                       box_label("test set: reserved for the final fixed procedure", C_TEST, w=5.6, h=0.8, font_size=24)).arrange(DOWN, buff=0.3).move_to([0, 0.3, 0])
        assert_on_screen(roles)
        self.say("Each candidate is trained, then scored on validation data. The test set is kept for the final procedure.",
                 LaggedStart(*[FadeIn(r, shift=UP * 0.2) for r in roles], lag_ratio=0.3))
        self.play(FadeOut(roles))
        # grid vs random
        pl = Square(2.8, color=GREY_B, stroke_width=2).move_to([-3.4, -0.1, 0])
        gpts = VGroup(*[Dot(pl.get_center() + np.array([(i - 1) * 0.9, (j - 1) * 0.9, 0]), radius=0.07, color=C_LOSS) for i in range(3) for j in range(3)])
        rs = np.random.RandomState(4)
        rpts = VGroup(*[Dot(pl.get_center() + np.array([(a - 0.5) * 2.5, (b - 0.5) * 2.5, 0]), radius=0.07, color=GREEN_C)
                        for a, b in zip(rs.permutation(9) / 8, rs.permutation(9) / 8)])
        pl2 = pl.copy().move_to([0.4, -0.1, 0])
        gl = txt("grid: 9 runs, 3 values per knob", 20, C_LOSS).next_to(pl, DOWN, buff=0.2)
        rl = txt("random: 9 runs, 9 values per knob", 20, GREEN_C).next_to(pl2, DOWN, buff=0.2)
        tab = VGroup(*[txt(f"{m}  →  {c:,}", 26, C_LOSS if m >= 4 else WHITE) for m, c in zip((1, 2, 3, 4, 6), GRID_COST)]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        tab.move_to([5.0, -0.2, 0])
        thead = txt("knobs → grid runs", 22, GREY_B).next_to(tab, UP, buff=0.25)
        assert_on_screen(VGroup(pl, gl, pl2, rl), tab, thead)
        self.say("A grid grows exponentially: five values per knob is 5, 25, 125 runs, and over fifteen thousand for six knobs.",
                 FadeIn(thead), LaggedStart(*[FadeIn(t) for t in tab], lag_ratio=0.3))
        self.say("Random search tries new values of every knob on every run, usually a better use of the same budget.",
                 Create(pl), FadeIn(gpts), FadeIn(gl), Create(pl2), FadeIn(rpts.move_to(pl2.get_center())), FadeIn(rl))
        self.play(FadeOut(pl), FadeOut(gpts), FadeOut(gl), FadeOut(pl2), FadeOut(rpts), FadeOut(rl), FadeOut(tab), FadeOut(thead))
        sup = VGroup(box_label("no budget for a broad search?", C_TEXT, w=6.2, h=0.8, font_size=24),
                     box_label("borrow settings from a closely related paper", C_TEXT, w=6.2, h=0.8, font_size=24),
                     txt("a starting prior, not a derivation or a proof of optimality", 24, YELLOW_D)).arrange(DOWN, buff=0.35).move_to([0, -0.2, 0])
        assert_on_screen(sup)
        self.say("With no budget for broad search, borrow settings from a closely related paper: an engineering prior, not proof.",
                 LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in sup], lag_ratio=0.3))
        self.say("Could another learner tune the knobs? Meta-learning can, but it is an outer loop with its own data and cost.",
                 Indicate(sup[0], color=YELLOW_D))
        self.hold(0.6)
        self.clear_stage()
