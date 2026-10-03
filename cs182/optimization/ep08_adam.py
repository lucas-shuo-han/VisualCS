"""Episode 8 — Adam and AdamW (Note 4, sections 4.2-4.3)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers

# (a) SignSGD: m = g, v = g*g  =>  m / sqrt(v) = sign(g), whatever the gradient's size
G_BIG = np.array([100.0, 0.01, -3.0])
assert (G_BIG / np.sqrt(G_BIG * G_BIG) == np.sign(G_BIG)).all()

LAM = np.array([1.0, 20.0])
GRAD = lambda w: LAM * w
W0 = np.array([-4.0, 1.0])
ETA = 0.3


def signsgd(T):
    w, P = W0.copy(), [W0.copy()]
    for _ in range(T):
        w = w - ETA * np.sign(GRAD(w))
        P.append(w.copy())
    return np.array(P)


P_SIGN = signsgd(40)
assert np.allclose(P_SIGN[13], P_SIGN[15]) and np.allclose(P_SIGN[14], P_SIGN[16])     # two-point cycle
assert np.linalg.norm(P_SIGN[13] - P_SIGN[14]) > 0.3                                   # it never settles
assert np.allclose(P_SIGN[13], [-0.1, 0.1]) and np.allclose(P_SIGN[14], [0.2, -0.2])


def adam(T, eta=ETA, b1=0.8, b2=0.999, eps=1e-8, correct=True):
    w, m, v, P = W0.copy(), np.zeros(2), np.zeros(2), [W0.copy()]
    for t in range(1, T + 1):
        g = GRAD(w)
        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * g * g
        mh = m / (1 - b1 ** t) if correct else m
        vh = v / (1 - b2 ** t) if correct else v
        w = w - eta * mh / (np.sqrt(vh) + eps)
        P.append(w.copy())
    return np.array(P)


T_ADAM = 60
P_ADAM = adam(T_ADAM)
assert np.linalg.norm(P_ADAM[-1]) < 0.03 and np.linalg.norm(P_SIGN[-1]) > 0.2
assert P_ADAM[:, 0].min() > -4.5 and P_ADAM[:, 0].max() < 1.0 and abs(P_ADAM[:, 1]).max() < 1.3, (P_ADAM.min(0), P_ADAM.max(0))
_n = np.linalg.norm(P_ADAM, axis=1)
assert _n[50:].max() < 0.05                                                            # it does settle

# (b) bias correction
B1, B2 = 0.9, 0.999
G_C = 2.0
M1 = (1 - B1) * G_C
assert abs(M1 - 0.2) < 1e-12                                                         # 0.1 g, not g
assert abs(M1 / (1 - B1) - G_C) < 1e-12                                              # corrected
V1 = (1 - B2) * G_C ** 2
FIRST_UNC = M1 / np.sqrt(V1)                                                         # both uncorrected
FIRST_M_ONLY = (M1 / (1 - B1)) / np.sqrt(V1)                                         # only m corrected
FIRST_FULL = (M1 / (1 - B1)) / np.sqrt(V1 / (1 - B2))
assert abs(FIRST_UNC - 0.1 / np.sqrt(0.001)) < 1e-9 and abs(FIRST_UNC - 3.1623) < 1e-3     # 0.1/sqrt(.001): too big
assert abs(FIRST_FULL - 1.0) < 1e-12 and abs(FIRST_M_ONLY - 31.62) < 0.01
# with a constant gradient, the corrected moments are exact at every step
_m = _v = 0.0
for _t in range(1, 30):
    _m = B1 * _m + (1 - B1) * G_C
    _v = B2 * _v + (1 - B2) * G_C ** 2
    assert abs(_m / (1 - B1 ** _t) - G_C) < 1e-9 and abs(_v / (1 - B2 ** _t) - G_C ** 2) < 1e-9

# (c) L2 penalty inside Adam vs decoupled weight decay
LAMWD, ETAW = 0.1, 0.01
W = np.array([1.0, 1.0])
GSC = np.array([10.0, 0.05])                                  # typical size of the data gradient per coordinate
DECAY_L2 = ETAW * 2 * LAMWD * W / GSC                         # eta * (2 lambda w) / sqrt(v_hat)
DECAY_W = ETAW * LAMWD * W                                     # eta * lambda_wd * w
assert np.allclose(DECAY_L2, [0.0002, 0.04]) and np.allclose(DECAY_W, [0.001, 0.001])
assert abs(DECAY_L2[1] / DECAY_L2[0] - 200) < 1e-9
# plain GD: L2 gradient and shrinkage agree
_w, _g = 0.7, 0.3
assert abs((_w - ETAW * (_g + 2 * LAMWD * _w)) - ((1 - 2 * ETAW * LAMWD) * _w - ETAW * _g)) < 1e-12


class Ep08Adam(NarratedScene):
    series = SERIES
    SCENES = ["why", "sign", "adam_update", "race", "adamw", "ledger"]

    def construct(self):
        self.title_card()
        self.why()
        self.sign()
        self.adam_update()
        self.race()
        self.adamw()
        self.ledger()
        self.end_card(
            ["Adam divides each coordinate by the running size of its gradient, so all steps are comparable",
             "SignSGD is the raw version and can cycle. Adam smooths both averages",
             "Both moments start at zero, so bias correction scales the early steps back up",
             "AdamW shrinks weights as a separate step, so decay isn't warped by the second moment",
             "No optimizer wins on speed, final solution and memory all at once"],
        )

    # ---------------------------------------------------------------- 1. why
    def why(self):
        head = self.heading("Why normalize every coordinate?")
        b1 = box_label("gradient descent is slow along small singular values", C_SOFT, w=9.6, h=0.9, font_size=22).move_to([0, 2.2, 0])
        b2 = box_label("ideal fix: divide each SVD direction by its singular value", C_STIFF, w=9.6, h=0.9, font_size=22).move_to([0, 0.9, 0])
        b3 = box_label("but computing an SVD of a huge model is far too expensive", C_LOSS, w=9.6, h=0.9, font_size=22).move_to([0, -0.4, 0])
        b4 = box_label("cheap compromise: make steps comparable in every coordinate", C_TRAIN, w=9.6, h=0.9, font_size=22).move_to([0, -1.7, 0])
        assert_on_screen(b1, b2, b3, b4)
        self.say("Why would we normalize every coordinate? Well, gradient descent is slow along weak directions, "
                 "which helps it resist noise, but it's also just slow. The ideal fix would divide each direction "
                 "by its singular value, but an SVD of a huge model is far too expensive. So we do the next best "
                 "thing, and make the steps about the same size in every ordinary coordinate.",
                 Write(head), FadeIn(b1, shift=UP * 0.2))
        self.cue("The ideal fix", FadeIn(b2, shift=UP * 0.2))
        self.cue("but an SVD", FadeIn(b3, shift=UP * 0.2))
        self.cue("So we do", FadeIn(b4, shift=UP * 0.2))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 2. SignSGD
    def sign(self):
        head = self.heading("The crudest version: SignSGD")
        eq = mts([r"m=g,\ \ v=g\odot g", r"\ \Rightarrow\ ", r"\frac{m}{\sqrt v}=\mathrm{sgn}(g)"], 0.9, {2: C_GRAD}).move_to([0, 2.3, 0])
        rows = VGroup(*[VGroup(mt(rf"g_{{{j + 1}}}={g:g}", 0.75, C_NOISE), mt(r"\longrightarrow", 0.75), mt(rf"\text{{step }}{'+' if g > 0 else '-'}\eta", 0.75, C_GRAD)).arrange(RIGHT, buff=0.4)
                        for j, g in enumerate(G_BIG)]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.4, 0.2, 0])
        note = txt("every coordinate moves the same distance,\nwhatever the size of its gradient", 24, C_TRAIN).move_to([3.6, 0.3, 0])
        assert_on_screen(eq, rows, note)
        self.say("What's the crudest way to do that? Divide each gradient coordinate by its own size, and all "
                 "that's left is the sign. Gradients of one hundred, one hundredth and minus three all become "
                 "steps of plus or minus eta, so the scale just stops mattering.",
                 Write(head), Write(eq))
        self.cue("Gradients of", FadeIn(rows, shift=UP * 0.2), FadeIn(note))
        self.hold(0.3)
        ax = Axes(x_range=[-4.5, 4.5, 1], y_range=[-1.2, 1.2, 1], x_length=8.4, y_length=3.4,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([-1.6, -0.15, 0])
        cont = contour_family(ax, (1.0, 20.0), [16.0, 9.0, 4.0, 1.0, 0.16])
        ps = path_pts(ax, [tuple(p) for p in P_SIGN], C_LOSS, 3)
        pd_ = path_dots(ax, [tuple(p) for p in P_SIGN], C_LOSS, 0.05)
        lab = VGroup(txt(f"SignSGD, η = {ETA}", 20, C_LOSS), txt("reaches the valley floor in 13 steps,", 18, C_LOSS),
                     txt("then cycles between two points", 18, C_LOSS)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.5, 1.2, 0])
        assert_on_screen(VGroup(ax, cont), lab)
        self.play(FadeOut(eq), FadeOut(rows), FadeOut(note))
        self.say("Let's try it in the ravine. It races to the valley floor, because every coordinate moves at full "
                 "speed. But then it's stuck, because a step of fixed size keeps overshooting, so it bounces "
                 "between two points near the minimum forever.",
                 Create(ax), Create(cont))
        self.cue("It races", Create(ps, run_time=2.5), FadeIn(pd_), FadeIn(lab))
        self.cue("But then it's stuck", Indicate(pd_[13:17], color=YELLOW_D))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 3. Adam formula
    def adam_update(self):
        head = self.heading("Adam: smooth both moments")
        m = mts([r"m_{t+1}=\beta_1 m_t+(1-\beta_1)\,g_t"], 0.8, {}).move_to([0, 2.4, 0])
        v = mts([r"v_{t+1}=\beta_2 v_t+(1-\beta_2)\,g_t\odot g_t"], 0.8, {}).move_to([0, 1.5, 0])
        m[0].set_color(C_MOM)
        v[0].set_color(C_V2)
        assert_on_screen(m, v)
        st =txt("m and v start at zero, so early on they are biased toward zero", 24, YELLOW_D).move_to([0, 0.5, 0])
        ex = mts([r"\beta_1=0.9:\ \ m_1=0.1\,g_0\ \ \text{(too small)}"], 0.8, {}).move_to([0, -0.4, 0])
        cor = mts([r"\hat m=\frac{m_{t+1}}{1-\beta_1^{t+1}},\qquad \hat v=\frac{v_{t+1}}{1-\beta_2^{t+1}}"], 0.8, {}).move_to([0, -1.5, 0])
        assert_on_screen(st, ex, cor)
        self.say("Adam smooths both of those pieces. It keeps a running average of the gradient, called the first "
                 "moment, and a running average of its square, the second moment. The catch is that both start "
                 "at zero, so with beta at zero point nine the first average is only a tenth of the gradient.",
                 Write(head), Write(m))
        self.cue("and a running average of its square", Write(v))
        self.cue("The catch is", FadeIn(st), Write(ex))
        self.say("Bias correction fixes that. We divide each average by one minus its beta raised to the step "
                 "count, and that scales the early averages back up.",
                 Write(cor), run_time=1.2)
        self.hold(0.3)
        self.play(FadeOut(m), FadeOut(v), FadeOut(st), FadeOut(ex), FadeOut(cor))
        upd = mts([r"w_{t+1}=w_t-\eta\,\frac{\hat m_{t+1}}{\sqrt{\hat v_{t+1}}+\varepsilon}"], 1.0, {}).move_to([0, 2.2, 0])
        cnt = txt("all operations are coordinatewise; ε is a tiny stabilizer", 24, GREY_B).move_to([0, 1.2, 0])
        tab = VGroup(txt(f"first step, gradient g = {G_C:g}:", 24, GREY_B),
                     mt(rf"\text{{no correction: }}\frac{{0.1\,g}}{{\sqrt{{0.001\,g^2}}}}\approx{FIRST_UNC:.2f}\ \ (\text{{about }}3\times\text{{ too big}})", 0.7, C_LOSS),
                     mt(r"\text{corrected: }\frac{g}{\sqrt{g^2}}=1", 0.7, C_TRAIN)).arrange(DOWN, buff=0.3).move_to([0, -0.5, 0])
        assert_on_screen(upd, cnt, tab)
        self.say("The update then divides the corrected first moment by the square root of the second, one "
                 "coordinate at a time. If we skip the corrections, the very first step comes out over three "
                 "times too big, and with them the ratio is exactly one.",
                 Write(upd), FadeIn(cnt))
        self.cue("If we skip", FadeIn(tab))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 4. race
    def race(self):
        head = self.heading("Adam in the same ravine")
        ax = Axes(x_range=[-4.5, 4.5, 1], y_range=[-1.2, 1.2, 1], x_length=8.4, y_length=3.4,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([-1.6, -0.15, 0])
        cont = contour_family(ax, (1.0, 20.0), [16.0, 9.0, 4.0, 1.0, 0.16])
        ps = path_pts(ax, [tuple(p) for p in P_SIGN], C_LOSS, 2)
        pa = path_pts(ax, [tuple(p) for p in P_ADAM], C_MOM, 4)
        pad = path_dots(ax, [tuple(p) for p in P_ADAM], C_MOM, 0.045)
        l1 = txt("SignSGD: cycles", 22, C_LOSS).move_to([4.6, 1.5, 0])
        l2 = VGroup(txt("Adam, β₁ = 0.8, β₂ = 0.999", 22, C_MOM), txt(f"distance {np.linalg.norm(P_ADAM[-1]):.2f} after {T_ADAM} steps", 20, C_MOM)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.6, 0.6, 0])
        assert_on_screen(VGroup(ax, cont), l1, l2)
        self.say("Now back to the same ravine, with the same step size. The thin line is SignSGD, stuck in its "
                 "cycle. Adam's averages smooth the path, so it settles down instead of cycling.",
                 Write(head), Create(ax), Create(cont))
        self.cue("The thin line", Create(ps), FadeIn(l1))
        self.cue("Adam's averages", Create(pa, run_time=3), FadeIn(pad), FadeIn(l2))
        cav = txt("Why dropping magnitude helps is not fully understood.", 22, YELLOW_D).move_to([0, -2.25, 0])
        assert_on_screen(cav)
        self.say("Why throwing away the size of the gradient helps isn't fully understood, and the original proof "
                 "had gaps. Adam works well in practice anyway.",
                 FadeIn(cav))
        self.hold(0.4)
        self.clear_stage()

    # ---------------------------------------------------------------- 5. AdamW
    def adamw(self):
        head = self.heading("AdamW: decoupled weight decay")
        gd = mts([r"L_\lambda=L+\lambda\|w\|^2", r"\ \Rightarrow\ ", r"w_{t+1}=(1-2\eta\lambda)\,w_t-\eta\nabla L"], 0.8, {1: C_LAM}).move_to([0, 2.4, 0])
        gd[0].set_color(C_LAM)
        assert_on_screen(gd)
        why = txt("Inside Adam the penalty gradient is averaged, then divided by √v", 24, C_LOSS).move_to([0, 1.4, 0])
        assert_on_screen(why)
        self.say("Now for weight decay. In plain gradient descent, a ridge penalty is the same as shrinking the "
                 "weights by the same fixed factor at each step. Put that penalty inside Adam, though, and it gets "
                 "divided by the second moment like everything else.",
                 Write(head), Write(gd), run_time=0.9)
        self.cue("Put that penalty", FadeIn(why))
        ax = Axes(x_range=[0, 3, 1], y_range=[0, 0.05, 0.01], x_length=5.0, y_length=2.4,
                  axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([-2.9, -0.2, 0])
        ymax = ax.c2p(0, 0.05)[1] - ax.c2p(0, 0)[1]
        h = lambda val: max(ymax * val / 0.05, 0.02)
        bars = VGroup()
        cols = [C_LOSS, C_LOSS, C_TRAIN, C_TRAIN]
        vals = [DECAY_L2[0], DECAY_L2[1], DECAY_W[0], DECAY_W[1]]
        for x, val, c in zip([0.35, 0.95, 2.05, 2.65], vals, cols):
            bars.add(Rectangle(width=0.4, height=h(val), color=c, fill_opacity=0.85, stroke_width=1).move_to(ax.c2p(x, 0), aligned_edge=DOWN))
        names = VGroup(txt("L2 inside Adam", 20, C_LOSS).next_to(ax.c2p(0.65, 0), DOWN, buff=0.35),
                       txt("AdamW", 20, C_TRAIN).next_to(ax.c2p(2.35, 0), DOWN, buff=0.35))
        yl = txt("shrinkage per step", 20, GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        yt = VGroup(*[txt(f"{v:g}", 18, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (0, 0.02, 0.04)])
        big = txt("coordinate with big gradient: 0.0002", 20, C_LOSS).move_to([3.7, 0.7, 0])
        small = txt("coordinate with small gradient: 0.04", 20, C_LOSS).move_to([3.7, 0.1, 0])
        aw = txt("AdamW: 0.001 in both", 20, C_TRAIN).move_to([3.7, -0.7, 0])
        assert_on_screen(VGroup(ax, names, yl, yt), big, small, aw)
        assert (GSC[0], GSC[1]) == (10.0, 0.05)
        self.say("Take two weights that both equal one, with typical gradient sizes of ten and zero point zero "
                 "five. The penalty ends up shrinking the second weight two hundred times harder than the first.",
                 FadeOut(why), Create(ax), FadeIn(yl), FadeIn(yt), FadeIn(names[0]))
        self.cue("The penalty ends up", FadeIn(bars[:2]), FadeIn(big), FadeIn(small))
        wd = mts([r"w_{t+1}=(1-\eta\lambda_{\mathrm{wd}})\,w_t-\eta\frac{\hat m_{t+1}}{\sqrt{\hat v_{t+1}}+\varepsilon}"], 0.8, {}).move_to([0, 1.9, 0])
        self.hold(0.2)
        self.play(FadeOut(gd))
        assert_on_screen(wd)
        cn = txt("Careful: λ_wd is the rate inside the factor (1 − ηλ_wd), not the ridge λ.", 22, YELLOW_D).move_to([0, -2.25, 0])
        assert_on_screen(cn)
        self.say("AdamW takes the shrink out and does it as a separate step, so the moments only ever see the "
                 "data. Now both weights decay alike. Watch the convention, though, because lambda wd sits "
                 "inside the factor one minus eta lambda wd, and it's not the ridge lambda.",
                 Write(wd))
        self.cue("Now both weights", FadeIn(bars[2:]), FadeIn(aw), FadeIn(names[1]))
        self.cue("Watch the convention", FadeIn(cn))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 6. ledger
    def ledger(self):
        head = self.heading("Comparing optimizers: a ledger, not a ranking")
        cols = ["", "training speed", "where it ends up", "extra state"]
        rows = [("SGD", "depends on geometry", "stochastic path", "none"),
                ("momentum", "filtered gradient", "different stopping behavior", "1 vector"),
                ("Adam", "coordinate scaling", "differs from SGD", "2 vectors")]
        colors = [WHITE, C_NOISE, C_MOM, C_V2]
        xs = [-4.6, -1.5, 1.9, 5.0]
        grp = VGroup()
        for cx, c in zip(xs, cols):
            grp.add(txt(c, 22, YELLOW_D).move_to([cx, 2.4, 0]))
        for i, r in enumerate(rows):
            for cx, c in zip(xs, r):
                t = txt(c, 22, colors[i + 1] if cx == xs[0] else WHITE).move_to([cx, 1.5 - 0.9 * i, 0])
                grp.add(t)
        assert_on_screen(grp)
        nt = VGroup(txt("These are optimizer-state counts, not a full training-memory budget.", 22, GREY_B),
                    txt("None of the three axes gives a universal ordering: measure on your own task.", 22, YELLOW_D)).arrange(DOWN, buff=0.25).move_to([0, -1.6, 0])
        assert_on_screen(nt)
        self.say("So which optimizer is best? We can compare them on three axes, namely training speed, "
                 "where you end up, and how much memory they need. On memory, momentum stores one extra vector "
                 "and Adam stores two, and the gradients and activations cost more on top of that.",
                 Write(head), FadeIn(grp), run_time=1.2)
        self.cue("On memory", FadeIn(nt[0]))
        self.say("And no optimizer wins on every axis. They all chase a low training loss, but what we really want "
                 "is generalization, so measure on your own task.",
                 FadeIn(nt[1]))
        self.hold(0.6)
        self.clear_stage()
