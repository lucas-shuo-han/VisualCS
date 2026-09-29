"""Episode 4 — Looking Where the Light Is (Note 1, section 1.4: risk, generalization, regularization)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers

# (a) metric vs surrogate for one prediction: p = probability given to the true class
P = [0.45, 0.49, 0.51, 0.90]
ACC = [int(p > 0.5) for p in P]
CE = [-float(np.log(p)) for p in P]
assert ACC == [0, 0, 1, 1] and all(a > b for a, b in zip(CE, CE[1:]))

# (b) empirical risk of two lines on four points
PTS = [(1.0, 1.2), (2.0, 1.9), (3.0, 3.2), (4.0, 3.7)]
PX, PY = np.array([p[0] for p in PTS]), np.array([p[1] for p in PTS])
LINE_A = (1.0, 0.0)        # y = x
LINE_B = (0.5, 1.0)        # y = 0.5x + 1
RES_A, RES_B = PY - (LINE_A[0] * PX + LINE_A[1]), PY - (LINE_B[0] * PX + LINE_B[1])
RISK_A, RISK_B = float(np.mean(RES_A ** 2)), float(np.mean(RES_B ** 2))
assert np.allclose(RES_A, [0.2, -0.1, 0.2, -0.3]) and abs(RISK_A - 0.045) < 1e-12 and RISK_B > RISK_A

# (c) polynomial experiment
f = lambda x: np.sin(x) + 0.35 * x
SIGMA = 0.3
rng = np.random.RandomState(12)
XT = np.sort(rng.uniform(0.2, 5.8, 10)); YT = f(XT) + rng.normal(0, SIGMA, 10)
XV = rng.uniform(0, 6, 30); YV = f(XV) + rng.normal(0, SIGMA, 30)
XP = rng.uniform(0, 6, 5000); YP = f(XP) + rng.normal(0, SIGMA, 5000)      # large fresh sample ~ population


def feats(x, d):
    return np.vander((np.asarray(x, float) - 3) / 3, d + 1, increasing=True)


def fit(d, lam):
    A = feats(XT, d)
    if lam == 0:
        return np.linalg.lstsq(A, YT, rcond=None)[0]
    return np.linalg.solve(A.T @ A + lam * np.eye(d + 1), A.T @ YT)


def rmse(w, x, y):
    d = len(w) - 1
    return float(np.sqrt(np.mean((feats(x, d) @ w - y) ** 2)))


DEGS = list(range(1, 10))
TR = [rmse(fit(d, 0), XT, YT) for d in DEGS]
TE = [rmse(fit(d, 0), XP, YP) for d in DEGS]
assert all(b <= a + 1e-9 for a, b in zip(TR, TR[1:])) and TR[-1] < 1e-6      # more flexible: training error only falls
D_STAR = DEGS[int(np.argmin(TE))]
assert 2 <= D_STAR <= 6 and TE[-1] > 3 * TE[D_STAR - 1] and TE[-1] > 3.0

LAMS = [10.0 ** k for k in range(-6, 3)]
W_L = {lam: fit(9, lam) for lam in LAMS}
VAL = [rmse(W_L[l], XV, YV) for l in LAMS]
TEST_L = [rmse(W_L[l], XP, YP) for l in LAMS]
TRAIN_L = [rmse(W_L[l], XT, YT) for l in LAMS]
K_STAR = int(np.argmin(VAL))
LAM_STAR = LAMS[K_STAR]
W0 = fit(9, 0)
assert abs(LAM_STAR - 0.1) < 1e-12
assert TEST_L[K_STAR] < TE[-1] / 3 and TRAIN_L[K_STAR] > TR[-1]
STAGES = [0.0, 1e-3, LAM_STAR, 10.0]
W_S = {lam: (W0 if lam == 0 else fit(9, lam)) for lam in STAGES}
XG = np.linspace(0, 6, 400)


def runs(ax, xs, ys, lo, hi, color=C_MODEL, width=4):
    """Polyline pieces for the parts of a curve inside [lo, hi] (the curve leaves through the top/bottom edge)."""
    ok = (ys >= lo) & (ys <= hi)
    out, start = VGroup(), None
    for i, o in enumerate(list(ok) + [False]):
        if o and start is None:
            start = i
        elif not o and start is not None:
            if i - start >= 2:
                out.add(polyline(ax, xs[start:i], ys[start:i], color, width))
            start = None
    return out


def poly_curve(ax, w, lo=-1.0, hi=4.0, color=C_MODEL):
    return runs(ax, XG, feats(XG, len(w) - 1) @ w, lo, hi, color)


class Ep04Risk(NarratedScene):
    series = SERIES

    def construct(self):
        self.title_card()
        self.four_objects()
        self.empirical_risk()
        self.overfit()
        self.ridge()
        self.validation()
        self.end_card(
            ["Metric, surrogate and update estimator are different objects",
             "Empirical risk is what we can optimize; population risk is what we want",
             "More flexibility lowers training error, not necessarily test error",
             "Regularization and validation keep the proxy honest"],
        )

    # ---------------------------------------------------------------- 1. four objects
    def four_objects(self):
        head = self.heading("Four different objects")
        names = ["intended outcome", "evaluation metric", "training surrogate", "update estimator"]
        qs = ["what should happen\nin deployment?", "what will we\nmeasure?", "what supplies the\nlocal learning signal?", "how is an update\nestimated?"]
        ex = ["good decisions", "accuracy", "cross-entropy", "mini-batch gradient"]
        cols = [GREY_A, YELLOW_D, C_LOSS, C_MODEL]
        boxes = VGroup(*[box_label(n, c, w=2.95, h=0.9, font_size=23) for n, c in zip(names, cols)]).arrange(RIGHT, buff=0.35).move_to([0, 1.6, 0])
        assert boxes.width < 13.4
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.03, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.5) for i in range(3)])
        qtx = VGroup(*[txt(q, 21, GREY_B, line_spacing=0.9).next_to(boxes[i], DOWN, buff=0.2) for i, q in enumerate(qs)])
        etx = VGroup(*[txt(e, 26, cols[i]).next_to(qtx[i], DOWN, buff=0.3) for i, e in enumerate(ex)])
        self.say("Keep four things apart: the outcome we want, the metric, the training surrogate, and the update estimator.",
                 Write(head), LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in boxes], lag_ratio=0.25), Create(arrows), FadeIn(qtx))
        self.say("For a classifier: good decisions, measured by accuracy, trained with cross-entropy and mini-batch gradients.",
                 FadeIn(etx, lag_ratio=0.3))
        self.hold(0.4)
        self.clear_stage()
        # table: accuracy vs cross-entropy
        hdr = ["p (true class)", "accuracy", "−ln p"]
        colx = [-3.6, 0.0, 3.3]
        cells = VGroup()
        for j, h in enumerate(hdr):
            cells.add(txt(h, 26, GREY_B).move_to([colx[j], 1.9, 0]))
        rows = []
        for i, p in enumerate(P):
            y = 1.15 - 0.62 * i
            r = VGroup(txt(f"{p:.2f}", 30, WHITE).move_to([colx[0], y, 0]),
                       txt("correct" if ACC[i] else "wrong", 28, GREEN_C if ACC[i] else C_LOSS).move_to([colx[1], y, 0]),
                       txt(f"{CE[i]:.3f}", 30, C_LOSS).move_to([colx[2], y, 0]))
            rows.append(r)
        head2 = self.heading("Metric vs surrogate")
        self.say("The true class gets probability 0.45, 0.49, 0.51, then 0.90. Accuracy only sees which side of 0.5 we are on.",
                 Write(head2), FadeIn(cells), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3))
        box = SurroundingRectangle(VGroup(rows[0], rows[1]), color=YELLOW_D, buff=0.12)
        self.say(f"0.45 to 0.49: accuracy is stuck, but cross-entropy falls from {CE[0]:.2f} to {CE[1]:.2f}. That is a usable signal.",
                 Create(box))
        self.say("A useful surrogate expresses what we care about, gives local information, is stable, and is cheap to optimize.",
                 FadeOut(box))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 2. empirical risk
    def empirical_risk(self):
        head = self.heading("Empirical risk")
        eq = mt(r"\hat\theta=\arg\min_\theta\ \frac1n\sum_{i=1}^{n}\ell\big(y_i,f_\theta(x_i)\big)", 0.8)
        eq.move_to([2.4, 2.85, 0])
        assert eq.get_right()[0] < 7.0
        ax = make_axes([0, 5, 1], [0, 5, 1], 5.6, 3.2).move_to([-3.4, -0.35, 0])
        d = dots(ax, PX, PY, C_DATA)
        lineA = ax.plot(lambda x: LINE_A[0] * x + LINE_A[1], x_range=[0, 5], color=C_MODEL, stroke_width=4)
        segs = VGroup(*[Line(ax.c2p(x, y), ax.c2p(x, LINE_A[0] * x + LINE_A[1]), color=C_LOSS, stroke_width=4) for x, y in PTS])
        self.say("With a loss chosen, training minimizes the empirical risk: the average loss over the training pairs.",
                 Write(head), Write(eq), Create(ax), FadeIn(d))
        self.say("Take squared error and four points. This line, y = x, misses them by these red gaps.",
                 Create(lineA), LaggedStart(*[Create(s) for s in segs], lag_ratio=0.2))
        sq = " + ".join(f"{abs(r):.1f}²" for r in RES_A)
        calc = VGroup(txt("mean of squared gaps", 24, GREY_B),
                      txt(f"({sq}) / 4", 28, C_LOSS),
                      txt(f"= {RISK_A:.3f}", 32, C_LOSS)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.4, -0.2, 0])
        assert calc.get_right()[0] < 7.0
        self.say(f"Square each gap, average them, and this line scores an empirical risk of {RISK_A:.3f}.", FadeIn(calc))
        lineB = ax.plot(lambda x: LINE_B[0] * x + LINE_B[1], x_range=[0, 5], color=C_MODEL, stroke_width=4)
        segsB = VGroup(*[Line(ax.c2p(x, y), ax.c2p(x, LINE_B[0] * x + LINE_B[1]), color=C_LOSS, stroke_width=4) for x, y in PTS])
        sqB = " + ".join(f"{abs(r):.1f}²" for r in RES_B)
        calcB = VGroup(txt("mean of squared gaps", 24, GREY_B),
                       txt(f"({sqB}) / 4", 28, C_LOSS),
                       txt(f"= {RISK_B:.3f}", 32, C_LOSS)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(calc)
        self.say(f"Another line, y = 0.5x + 1, scores {RISK_B:.3f}. Empirical risk minimization prefers the first line.",
                 Transform(lineA, lineB), Transform(segs, segsB), Transform(calc, calcB))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 3. overfit
    def overfit(self):
        head = self.heading("Fitting the data is not the goal")
        ax = make_axes([0, 6, 1], [-1, 4, 1], 7.6, 3.3).move_to([-2.0, -0.15, 0])
        tgt = DashedVMobject(plot(ax, f, C_TARGET, [0, 6], width=3), num_dashes=60)
        d = dots(ax, XT, YT, C_TRAIN)
        self.say("The real target is population risk: expected loss on fresh data. Ten noisy samples; dashed is the unseen truth.",
                 Write(head), Create(ax), Create(tgt), FadeIn(d))
        curve = poly_curve(ax, W0)
        info = VGroup(txt("degree 9, ten points", 24, C_TEXT),
                      txt(f"train RMSE {TR[-1]:.2f}", 26, C_TRAIN),
                      txt(f"test RMSE {TE[-1]:.1f}", 26, C_TEST)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.6, 1.0, 0])
        assert info.get_right()[0] < 7.0
        self.say(f"A degree-nine polynomial can hit all ten points: training error is essentially zero, but on fresh data it is {TE[-1]:.1f}.",
                 Create(curve, run_time=2.0), FadeIn(info))
        self.hold(0.4)
        self.clear_stage()
        # error vs degree
        head = self.heading("Flexibility vs error")
        ax = make_axes([0, 10, 1], [0, 3.5, 1], 7.6, 3.3).move_to([-1.6, 0.35, 0])
        ticks = tick_labels(ax, DEGS, 20)
        xl = txt("polynomial degree", 22, GREY_B).next_to(ax.x_axis.get_end(), RIGHT, buff=0.15)
        floor = DashedLine(ax.c2p(0, SIGMA), ax.c2p(10, SIGMA), color=GREY, stroke_width=2)
        fl = txt(f"noise floor {SIGMA}", 20, GREY_B).next_to(floor, UP, buff=0.08).align_to(floor, RIGHT)
        ctr = polyline(ax, DEGS, np.minimum(TR, 3.5), C_TRAIN, 4)
        cte = polyline(ax, DEGS, np.minimum(TE, 3.5), C_TEST, 4)
        ltr = txt("training error", 24, C_TRAIN).move_to([4.4, 1.2, 0])
        lte = txt("error on new data", 24, C_TEST).move_to([4.4, 0.6, 0])
        self.say("Training error only ever falls as models get more flexible: a richer family can always fit the samples at least as well.",
                 Write(head), Create(ax), FadeIn(ticks), FadeIn(xl), Create(floor), FadeIn(fl), Create(ctr), FadeIn(ltr))
        self.say(f"Error on new data bottoms out near degree {D_STAR}, then climbs. That turnaround is overfitting.",
                 Create(cte), FadeIn(lte), Flash(ax.c2p(D_STAR, TE[D_STAR - 1]), color=YELLOW_D, flash_radius=0.35))
        self.say("Empirical risk can be optimized; population performance cannot be seen. We are looking where the light is.",
                 Indicate(ltr, color=C_TRAIN), Indicate(lte, color=C_TEST))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 4. ridge
    def ridge(self):
        head = self.heading("A second pressure: regularization")
        eq = mts([r"\arg\min_{\vec w}\Big(\|X\vec w-\vec y\|_2^2+", r"\lambda", r"\|\vec w\|_2^2\Big)"], 0.8, {1: C_LAM})
        eq.move_to([3.0, 2.5, 0])
        assert eq.get_right()[0] < 7.0
        ax = make_axes([0, 6, 1], [-1, 4, 1], 7.6, 3.0).move_to([-2.0, -0.35, 0])
        tgt = DashedVMobject(plot(ax, f, C_TARGET, [0, 6], width=3), num_dashes=60)
        d = dots(ax, XT, YT, C_TRAIN)
        cur = poly_curve(ax, W_S[0.0])

        def panel(lam):
            w = W_S[lam]
            lab = "λ = 0" if lam == 0 else f"λ = {lam:g}"
            return VGroup(txt(lab, 30, C_LAM),
                          txt(f"train RMSE {rmse(w, XT, YT):.2f}", 24, C_TRAIN),
                          txt(f"test RMSE {rmse(w, XP, YP):.2f}", 24, C_TEST),
                          txt(f"‖w‖ = {np.linalg.norm(w):.1f}", 24, GREY_A)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.6, -0.2, 0])

        pan = panel(0.0)
        self.say("One remedy is a second pressure: ridge regression balances fit against weight size, with strength lambda.",
                 Write(head), Write(eq), Create(ax), Create(tgt), FadeIn(d), Create(cur), FadeIn(pan))
        caps = {1e-3: "A small lambda already tames the wild swings between the points.",
                LAM_STAR: "At lambda = 0.1 the curve follows the trend, misses some points on purpose, and generalizes far better.",
                10.0: "Too much lambda squeezes the weights until the model underfits. Regularization is a dial, not a cure."}
        for lam in STAGES[1:]:
            self.say(caps[lam], Transform(cur, poly_curve(ax, W_S[lam])), Transform(pan, panel(lam)))
            self.hold(0.3)
        self.say("So fit the data, but not too tightly. Even then, generalization is never guaranteed.",
                 Indicate(eq[1], color=C_LAM))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 5. validation
    def validation(self):
        head = self.heading("Choosing hyperparameters")
        ks = list(range(-6, 3))
        ax = make_axes([0, 10, 1], [0, 3.5, 1], 7.8, 3.2).move_to([-1.6, 0.4, 0])
        ticks = VGroup(*[mt(rf"10^{{{k}}}", 0.5, GREY_B).next_to(ax.c2p(k + 7, 0), DOWN, buff=0.18) for k in ks[::2]])
        xl = txt("regularization strength λ", 22, C_LAM).next_to(ax.x_axis.get_end(), RIGHT, buff=0.15)
        vc = polyline(ax, [k + 7 for k in ks], np.minimum(VAL, 3.5), C_VAL, 4)
        vd = VGroup(*[Dot(ax.c2p(k + 7, min(v, 3.5)), radius=0.07, color=C_VAL) for k, v in zip(ks, VAL)])
        lv = txt("validation error", 24, C_VAL).move_to([5.0, 1.3, 0])
        self.say("Training data sets the weights; validation data sets hyperparameters like lambda, learning rate, and hidden units.",
                 Write(head), Create(ax), FadeIn(ticks), FadeIn(xl))
        self.say("Sweep the hyperparameter over orders of magnitude. Each point is a full training run scored on validation.",
                 LaggedStart(*[GrowFromCenter(p) for p in vd], lag_ratio=0.15), Create(vc, run_time=2.0), FadeIn(lv))
        best = Dot(ax.c2p(ks[K_STAR] + 7, VAL[K_STAR]), radius=0.13, color=YELLOW_D)
        pick = txt(f"best: λ = {LAM_STAR:g}", 24, YELLOW_D).next_to(best, UP, buff=0.9)
        self.say(f"Validation picks lambda = {LAM_STAR:g}. Careful: every look at the validation set spends a little of its honesty.",
                 FadeIn(best), FadeIn(pick))
        tst = VGroup(txt("test error, checked once", 24, C_TEST), txt(f"{TEST_L[K_STAR]:.2f}", 44, C_TEST),
                     txt(f"vs {TE[-1]:.1f} with no regularization", 24, GREY_A)).arrange(DOWN, buff=0.2).move_to([0.6, 1.8, 0])
        assert tst.get_right()[0] < 7.0
        self.say("Only now do we open the test set, once, after every choice is made. It assumes test data resemble deployment.",
                 FadeIn(tst))
        self.say("A cats-and-dogs model shown dinosaurs: test scores mislead when deployment differs. Detecting shift is only partial.",
                 Indicate(tst[1], color=C_TEST))
        self.hold(0.6)
        self.clear_stage()
