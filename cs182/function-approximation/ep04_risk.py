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
    SCENES = ["four_objects", "empirical_risk", "overfit", "ridge", "validation"]

    def construct(self):
        self.title_card()
        self.four_objects()
        self.empirical_risk()
        self.overfit()
        self.ridge()
        self.validation()
        self.end_card(
            ["What we want, what we measure and what we train on are different things",
             "We can only minimize training loss. We actually care about fresh data",
             "More flexibility always helps training error, not test error",
             "Pick knobs on validation data. Open the test set once, at the end"],
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
        self.say("We train a model to do well, but well at what? There are really four different things hiding "
                 "in that one word. For a classifier, what we want is good decisions, and what we measure is "
                 "accuracy. But what we train on is cross-entropy, and each update is estimated from one "
                 "mini-batch.",
                 Write(head), LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in boxes], lag_ratio=0.25), Create(arrows), FadeIn(qtx))
        self.cue("For a classifier", FadeIn(etx[0]))
        self.cue("what we measure", FadeIn(etx[1]))
        self.cue("But what we train on", FadeIn(etx[2]))
        self.cue("each update is estimated", FadeIn(etx[3]))
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
        assert (P[0], P[1], P[-1]) == (0.45, 0.49, 0.90)      # spoken below
        self.say("You might ask why we don't just train on accuracy itself. Here are four predictions, where the probability given "
                 "to the true class goes from zero point four five up to zero point nine. Accuracy only asks "
                 "whether that number is past one half.",
                 Write(head2), FadeIn(cells), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3))
        box = SurroundingRectangle(VGroup(rows[0], rows[1]), color=YELLOW_D, buff=0.12)
        assert f"{CE[0]:.2f}" == "0.80" and f"{CE[1]:.2f}" == "0.71"      # spoken below
        self.say("From zero point four five to zero point four nine, accuracy doesn't move at all. Cross-entropy "
                 "does, dropping from zero point eight to zero point seven one, and that gives training something "
                 "to follow. That's the job of a training surrogate. It points where we care, gives a signal "
                 "nearby, stays stable, and is cheap to compute.",
                 Create(box))
        self.cue("That's the job", FadeOut(box))
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
        self.say("So we pick a loss, and training averages it over the training set and pushes that average "
                 "down. That average is called the empirical risk. Let's take four points and squared error, "
                 "and start with a line through the origin with slope one. It misses each point by one of "
                 "these red gaps.",
                 Write(head), Write(eq), Create(ax), FadeIn(d))
        self.cue("and start with a line", Create(lineA))
        self.cue("It misses each point", LaggedStart(*[Create(s) for s in segs], lag_ratio=0.2))
        sq = " + ".join(f"{abs(r):.1f}²" for r in RES_A)
        calc = VGroup(txt("mean of squared gaps", 24, GREY_B),
                      txt(f"({sq}) / 4", 28, C_LOSS),
                      txt(f"= {RISK_A:.3f}", 32, C_LOSS)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.4, -0.2, 0])
        assert calc.get_right()[0] < 7.0
        lineB = ax.plot(lambda x: LINE_B[0] * x + LINE_B[1], x_range=[0, 5], color=C_MODEL, stroke_width=4)
        segsB = VGroup(*[Line(ax.c2p(x, y), ax.c2p(x, LINE_B[0] * x + LINE_B[1]), color=C_LOSS, stroke_width=4) for x, y in PTS])
        sqB = " + ".join(f"{abs(r):.1f}²" for r in RES_B)
        calcB = VGroup(txt("mean of squared gaps", 24, GREY_B),
                       txt(f"({sqB}) / 4", 28, C_LOSS),
                       txt(f"= {RISK_B:.3f}", 32, C_LOSS)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(calc)
        # spoken below
        assert f"{RISK_A:.3f}" == "0.045" and f"{RISK_B:.3f}" == "0.270" and f"{RISK_B / RISK_A:.0f}" == "6"
        assert LINE_B[0] < LINE_A[0]
        self.say("Square the gaps and average them, and this line scores zero point zero four five. Now try a "
                 "flatter line instead. That one scores zero point two seven, which is six times worse, so "
                 "training picks the first line.",
                 FadeIn(calc))
        self.cue("Now try a flatter line", Transform(lineA, lineB), Transform(segs, segsB), Transform(calc, calcB))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 3. overfit
    def overfit(self):
        head = self.heading("Fitting the data is not the goal")
        ax = make_axes([0, 6, 1], [-1, 4, 1], 7.6, 3.3).move_to([-2.0, -0.15, 0])
        tgt = DashedVMobject(plot(ax, f, C_TARGET, [0, 6], width=3), num_dashes=60)
        d = dots(ax, XT, YT, C_TRAIN)
        curve = poly_curve(ax, W0)
        info = VGroup(txt("degree 9, ten points", 24, C_TEXT),
                      txt(f"train RMSE {TR[-1]:.2f}", 26, C_TRAIN),
                      txt(f"test RMSE {TE[-1]:.1f}", 26, C_TEST)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.6, 1.0, 0])
        assert info.get_right()[0] < 7.0
        assert f"{TE[-1]:.1f}" == "3.2" and f"{TR[-1]:.2f}" == "0.00"      # spoken below
        self.say("But what we really want is low loss on fresh data, and that's called the population risk. "
                 "Here are ten samples, along with the hidden target function. A degree-nine polynomial "
                 "threads through all ten of them, so its training error is zero. On fresh data, though, its "
                 "error is three point two.",
                 Write(head), Create(ax), Create(tgt), FadeIn(d))
        self.cue("A degree-nine polynomial", Create(curve, run_time=2.0), FadeIn(info[:2]))
        self.cue("On fresh data, though", FadeIn(info[2]))
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
        assert D_STAR == 3                                    # spoken: "degree three"
        self.say("Make the model more flexible and the training error can only go down, because a bigger family "
                 "always fits at least as well. But the error on fresh data bottoms out at degree three and "
                 "then climbs, and that turnaround is overfitting. We can only optimize what we can see, which "
                 "is the training set, so we're looking where the light is.",
                 Write(head), Create(ax), FadeIn(ticks), FadeIn(xl), Create(floor), FadeIn(fl), Create(ctr), FadeIn(ltr))
        self.cue("But the error on fresh data", Create(cte), FadeIn(lte), Flash(ax.c2p(D_STAR, TE[D_STAR - 1]), color=YELLOW_D, flash_radius=0.35))
        self.cue("We can only optimize", Indicate(ltr, color=C_TRAIN), Indicate(lte, color=C_TEST))
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

        def stage(lam):
            return Transform(cur, poly_curve(ax, W_S[lam])), Transform(pan, panel(lam))

        pan = panel(0.0)
        assert STAGES == [0.0, 1e-3, LAM_STAR, 10.0]
        self.say("To rein in a model that flexible, we add a second pressure, called regularization. Ridge regression charges a price for big "
                 "weights, and lambda sets how high that price is. Even a tiny lambda calms down those wild "
                 "swings between the points.",
                 Write(head), Write(eq), Create(ax), Create(tgt), FadeIn(d), Create(cur), FadeIn(pan))
        self.cue("Even a tiny lambda", *stage(1e-3))
        self.hold(0.3)
        assert f"{LAM_STAR:g}" == "0.1" and f"{TEST_L[K_STAR]:.2f}" == "0.40"      # spoken below
        self.say("At lambda equals zero point one, the curve follows the trend and misses some points on "
                 "purpose, and the test error drops to zero point four. Turn it up too far, though, and the "
                 "weights get squeezed flat, so now the model underfits. So regularization is a dial, not a "
                 "cure. We fit the data, but not too tightly, and even then nothing guarantees it will "
                 "generalize.",
                 *stage(LAM_STAR))
        self.cue("Turn it up too far", *stage(10.0))
        self.cue("So regularization is a dial", Indicate(eq[1], color=C_LAM))
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
        self.say("That leaves one question, which is who gets to pick lambda. The training set decides the parameters, meaning the weights and "
                 "biases. A hyperparameter like lambda gets chosen on a separate validation set. So we sweep "
                 "lambda over powers of ten, and each dot here is a whole training run, scored on the "
                 "validation set.",
                 Write(head), Create(ax), FadeIn(ticks), FadeIn(xl))
        self.cue("So we sweep lambda", LaggedStart(*[GrowFromCenter(p) for p in vd], lag_ratio=0.15), Create(vc, run_time=2.0), FadeIn(lv))
        best = Dot(ax.c2p(ks[K_STAR] + 7, VAL[K_STAR]), radius=0.13, color=YELLOW_D)
        pick = txt(f"best: λ = {LAM_STAR:g}", 24, YELLOW_D).next_to(best, UP, buff=0.9)
        tst = VGroup(txt("test error, checked once", 24, C_TEST), txt(f"{TEST_L[K_STAR]:.2f}", 44, C_TEST),
                     txt(f"vs {TE[-1]:.1f} with no regularization", 24, GREY_A)).arrange(DOWN, buff=0.2).move_to([0.6, 1.8, 0])
        assert tst.get_right()[0] < 7.0
        self.say("The lowest dot tells us to set lambda to zero point one. But be careful, because every peek "
                 "at the validation set spends a little of its honesty. Only now, with every choice made, do "
                 "we open the test set, and we do it exactly once.",
                 FadeIn(best), FadeIn(pick))
        self.cue("Only now", FadeIn(tst))
        self.say("Even that number assumes the test set looks like the real world. Show a model trained on "
                 "cats and dogs a dinosaur, and its test score tells you nothing. That's called distribution "
                 "shift, and spotting it is hard.",
                 Indicate(tst[1], color=C_TEST))
        self.hold(0.6)
        self.clear_stage()
