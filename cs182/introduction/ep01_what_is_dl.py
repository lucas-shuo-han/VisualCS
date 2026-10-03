"""Episode 1 — What Is Deep Learning? (Lecture 0: the definition, the circuit, learning the knobs, new data)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers

# (a) one circuit element (Rosenblatt-style neuron): z = w1 x1 + w2 x2 + b, output = sign(z)
X_IN = (2.0, 1.0)
KNOBS_A, BIAS_A = (0.8, -0.5), 0.2
KNOBS_B, BIAS_B = (-0.8, 0.5), 0.2
ZA = KNOBS_A[0] * X_IN[0] + KNOBS_A[1] * X_IN[1] + BIAS_A
ZB = KNOBS_B[0] * X_IN[0] + KNOBS_B[1] * X_IN[1] + BIAS_B
assert abs(ZA - 1.3) < 1e-9 and abs(ZB + 0.9) < 1e-9        # +1 then -1

# (b) twenty labeled points from a hidden rule, and the perceptron update w <- w + y x, b <- b + y
W_TRUE, B_TRUE = np.array([1.0, 0.7]), -0.3
_rng = np.random.RandomState(6)
_pts = []
while len(_pts) < 20:
    _x = _rng.uniform(-2.6, 2.6, 2)
    if abs(W_TRUE @ _x + B_TRUE) > 0.4:
        _pts.append(_x)
XS = np.round(np.array(_pts), 1)
YS = np.sign(XS @ W_TRUE + B_TRUE)
assert 8 <= int((YS > 0).sum()) <= 12 and not np.any(XS @ W_TRUE + B_TRUE == 0)


def n_wrong(w, b, X=XS, Y=YS):
    return int(np.sum(np.sign(X @ w + b) != Y))


w0, b0 = np.array([-0.3, 0.6]), 0.0
HIST = [dict(w=w0.copy(), b=b0, wrong=n_wrong(w0, b0), idx=None)]
_w, _b = w0.copy(), b0
for _ in range(100):
    changed = False
    for i in range(len(XS)):
        if np.sign(XS[i] @ _w + _b) * YS[i] <= 0:
            _w, _b = _w + YS[i] * XS[i], _b + YS[i]
            HIST.append(dict(w=_w.copy(), b=_b, wrong=n_wrong(_w, _b), idx=i))
            changed = True
    if not changed:
        break
WF, BF = _w, _b
assert [h["wrong"] for h in HIST] == [10, 4, 2, 6, 0], [h["wrong"] for h in HIST]    # 4 updates, not monotone
assert n_wrong(WF, BF) == 0

# (c) fresh points: same rule, then a different rule (labels follow another direction)
_r2 = np.random.RandomState(9)
XF = np.round(_r2.uniform(-2.6, 2.6, (100, 2)), 1)
YF1 = np.sign(XF @ W_TRUE + B_TRUE + 1e-9)
W_OTHER = np.array([-0.7, 1.0])
YF2 = np.sign(XF @ W_OTHER + 1e-9)
ACC1 = float(np.mean(np.sign(XF @ WF + BF + 1e-9) == YF1))
ACC2 = float(np.mean(np.sign(XF @ WF + BF + 1e-9) == YF2))
assert 0.85 <= ACC1 <= 0.99 and 0.35 <= ACC2 <= 0.65, (ACC1, ACC2)
WRONG1 = np.sign(XF @ WF + BF + 1e-9) != YF1
WRONG2 = np.sign(XF @ WF + BF + 1e-9) != YF2

LIM = 3.0


def line_ends(w, b):
    """Endpoints (data coords) of w.x + b = 0 clipped to the square [-LIM, LIM]^2."""
    c = []
    for xv in (-LIM, LIM):
        if abs(w[1]) > 1e-9:
            yv = -(w[0] * xv + b) / w[1]
            if abs(yv) <= LIM + 1e-9:
                c.append((xv, yv))
    for yv in (-LIM, LIM):
        if abs(w[0]) > 1e-9:
            xv = -(w[1] * yv + b) / w[0]
            if abs(xv) <= LIM + 1e-9 and all(abs(xv - p[0]) + abs(yv - p[1]) > 1e-6 for p in c):
                c.append((xv, yv))
    assert len(c) >= 2
    return c[0], c[1]


def marker(ax, p, y, color=C_DATA, s=0.13):
    c = ax.c2p(p[0], p[1])
    if y > 0:
        return Circle(radius=s, stroke_color=color, stroke_width=3, fill_opacity=0).move_to(c)
    return VGroup(Line(c + np.array([-s, -s, 0]), c + np.array([s, s, 0]), color=color, stroke_width=3),
                  Line(c + np.array([-s, s, 0]), c + np.array([s, -s, 0]), color=color, stroke_width=3))


def fmt(v):
    return f"{v:.1f}".replace("-", "−")


class Ep01WhatIsDL(NarratedScene):
    series = SERIES
    SCENES = ["definition", "one_element", "deep", "learning", "new_data"]

    def construct(self):
        self.title_card()
        self.definition()
        self.one_element()
        self.deep()
        self.learning()
        self.new_data()
        self.end_card(
            ["Deep learning: circuits with knobs, and data turns the knobs",
             "Same circuit, new knob settings, a different answer. The knobs are the program",
             "Deep just means many elements in a row",
             "Fitting the training data is easy. The real test is new data"],
        )

    # ---------------------------------------------------------------- 1. definition
    def definition(self):
        head = self.heading("The definition")
        data = box_label("training data", C_DATA, w=2.5, h=0.9, font_size=26).move_to([-5.0, 1.5, 0])
        opt = box_label("optimization algorithm", C_OPT, w=3.9, h=0.9, font_size=25).move_to([-0.35, 1.5, 0])
        circ = box_label("circuit, parameters θ", C_MODEL, w=3.4, h=0.9, font_size=25).move_to([4.7, 1.5, 0])
        sub = txt("simulated analog: multiply, add, max", 22, GREY_B).next_to(circ, UP, buff=0.2).align_to(circ, RIGHT).shift(RIGHT * 0.3)
        a1 = Arrow(data.get_right(), opt.get_left(), buff=0.08, color=GREY_B, stroke_width=3)
        a2 = Arrow(opt.get_right(), circ.get_left(), buff=0.08, color=GREY_B, stroke_width=3)
        l1 = txt("drives", 22, GREY_B).next_to(a1, UP, buff=0.08)
        l2 = txt("sets", 22, GREY_B).next_to(a2, UP, buff=0.08)
        for m in (data, opt, circ, sub):
            assert m.get_right()[0] < 6.9 and m.get_left()[0] > -6.9
        self.say("So what is deep learning, really, underneath all the excitement? The definition this course "
                 "runs on is simulated analog circuits, which just means circuits with knobs on them. And nobody "
                 "turns those knobs by hand. An optimization algorithm sets them, and it's driven by training "
                 "data.",
                 Write(head), FadeIn(circ, shift=UP * 0.2), FadeIn(sub))
        self.cue("An optimization algorithm", FadeIn(opt, shift=RIGHT * 0.2), Create(a2), FadeIn(l2))
        self.cue("it's driven by", FadeIn(data, shift=RIGHT * 0.2), Create(a1), FadeIn(l1))
        newd = box_label("new data", C_NEW, w=2.5, h=0.9, font_size=26).move_to([-5.0, -0.9, 0])
        circ2 = circ.copy().set_y(-0.9).set_x(-0.35)
        ans = box_label("answer", GREY_A, w=2.2, h=0.9, font_size=26).move_to([4.2, -0.9, 0])
        b1 = Arrow(newd.get_right(), circ2.get_left(), buff=0.08, color=GREY_B, stroke_width=3)
        b2 = Arrow(circ2.get_right(), ans.get_left(), buff=0.08, color=GREY_B, stroke_width=3)
        note = txt("the pattern it captured still applies", 24, C_NEW).next_to(VGroup(newd, ans), DOWN, buff=0.45).set_x(0)
        assert circ2.get_right()[0] < b2.get_start()[0] + 0.2
        self.say("The whole point is that the circuit captures a pattern in its training data. So when new data "
                 "arrives, the same circuit still gives a useful answer.",
                 TransformFromCopy(circ, circ2))
        self.cue("So when new data arrives", FadeIn(newd, shift=RIGHT * 0.2), Create(b1), Create(b2), FadeIn(ans), FadeIn(note))
        self.hold(0.6)
        self.clear_stage()

    # ---------------------------------------------------------------- 2. one element
    def one_element(self):
        head = self.heading("The smallest circuit")
        ins = VGroup(*[Circle(0.3, color=C_DATA, stroke_width=3).move_to([-5.2, y, 0]) for y in (1.2, -0.5)])
        xv = VGroup(*[txt(str(int(v)), 28, C_DATA).move_to(c) for v, c in zip(X_IN, ins)])
        xl = VGroup(mt("x_1", 0.75, GREY_B).next_to(ins[0], UP, buff=0.12), mt("x_2", 0.75, GREY_B).next_to(ins[1], DOWN, buff=0.12))

        def knobs(k):
            return VGroup(*[box_label("×" + fmt(v), C_MODEL, w=1.5, h=0.62, font_size=24).move_to([-3.2, y, 0])
                            for v, y in zip(k, (1.2, -0.5))])

        def prods(k):
            return VGroup(*[txt(fmt(v * x), 24, GREY_A).move_to([-1.75, y + dy, 0])
                            for v, x, y, dy in zip(k, X_IN, (1.2, -0.5), (0.42, -0.42))])

        sig = Circle(0.5, color=WHITE, stroke_width=3).move_to([-0.6, 0.35, 0])
        sigt = txt("Σ", 34, WHITE).move_to(sig)
        bias = box_label("+" + fmt(BIAS_A), C_MODEL, w=1.3, h=0.62, font_size=24).move_to([-0.6, 2.05, 0])
        bwire = Arrow(bias.get_bottom(), sig.get_top(), buff=0.05, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        thr = box_label("sign", GREY_A, w=1.4, h=0.7, font_size=26).move_to([1.9, 0.35, 0])
        w_thr = Arrow(sig.get_right(), thr.get_left(), buff=0.05, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        out = Circle(0.42, color=GREEN_C, stroke_width=3).move_to([4.2, 0.35, 0])
        w_out = Arrow(thr.get_right(), out.get_left(), buff=0.05, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.3)
        outt = txt("+1", 30, GREEN_C).move_to(out)
        kb = knobs(KNOBS_A)
        # fix wire ends after the knob boxes exist
        w2 = VGroup(*[Line(k.get_right(), sig.get_left() + np.array([0, dy, 0]), color=GREY_B)
                      for k, dy in zip(kb, (0.22, -0.22))])
        w1 = VGroup(*[Line(c.get_right(), k.get_left(), color=GREY_B) for c, k in zip(ins, kb)])
        pr = prods(KNOBS_A)

        def zt(k, b, z):
            return VGroup(txt("z =", 30, GREY_B), txt(f"{fmt(k[0])}·2 + ({fmt(k[1])})·1 + {fmt(b)} = {fmt(z)}", 30, WHITE)
                          ).arrange(RIGHT, buff=0.25).move_to([0.2, -1.7, 0])

        eq = zt(KNOBS_A, BIAS_A, ZA)
        for m in (ins, kb, sig, thr, out, eq):
            assert m.get_right()[0] < 6.9 and m.get_left()[0] > -6.9 and m.get_bottom()[1] > -2.4
        # spoken below: inputs two and one; 1.6 - 0.5 + 0.2 = 1.3
        assert X_IN == (2.0, 1.0) and abs(KNOBS_A[0] * X_IN[0] - 1.6) < 1e-9 and KNOBS_A[1] * X_IN[1] == -0.5 and BIAS_A == 0.2
        self.say("Let's start small, with Rosenblatt's adaptive neuron. Each input passes through a knob, called "
                 "a weight, that scales it. Then we add everything up, along with a bias. Feed in two and one, "
                 "and we get one point six, minus zero point five, plus zero point two, which comes to one "
                 "point three.",
                 Write(head), FadeIn(ins), FadeIn(xv), FadeIn(xl), Create(w1), FadeIn(kb, lag_ratio=0.3))
        self.cue("Then we add everything up", Create(w2), FadeIn(sig), FadeIn(sigt), FadeIn(bias), Create(bwire))
        self.cue("Feed in two and one", FadeIn(pr), Write(eq))
        kb2 = knobs(KNOBS_B)
        pr2 = prods(KNOBS_B)
        eq2 = zt(KNOBS_B, BIAS_B, ZB)
        outt2 = txt("−1", 30, RED_C).move_to(out)
        assert KNOBS_B == (-KNOBS_A[0], -KNOBS_A[1]) and BIAS_B == BIAS_A      # "flip the sign of both weights"
        self.say("Then a threshold turns that number into an answer. It's positive, so the circuit says plus "
                 "one. Now flip the sign of both weights. With the same wires and the same input, the circuit "
                 "says minus one instead, so the knobs really are the program.",
                 Create(w_thr), FadeIn(thr), Create(w_out), FadeIn(out), FadeIn(outt))
        self.cue("Now flip the sign", Transform(kb, kb2), Transform(pr, pr2), Transform(eq, eq2))
        self.cue("the circuit says minus one", Transform(outt, outt2), out.animate.set_color(RED_C))
        self.hold(0.6)
        self.clear_stage()

    # ---------------------------------------------------------------- 3. deep
    def deep(self):
        head = self.heading("Why deep?")
        g, layers, edges = nn_diagram((2, 4, 4, 1), layer_gap=2.6, node_gap=0.85, r=0.24)
        g.move_to([0, 1.0, 0])
        pat = VGroup(mt(r"\text{affine}\to\text{ReLU}\to\text{affine}", 0.85, C_MODEL)).move_to([0, -1.2, 0])
        why = txt("the pattern from the function-approximation unit", 24, GREY_B).next_to(pat, DOWN, buff=0.2)
        assert why.get_bottom()[1] > -2.45
        self.say("So where does the word deep come in? It comes from chaining elements together, so that the "
                 "signal passes through several of them in a row before it reaches the output. Each element "
                 "is still just multiply, add, and take a max, which is the same pattern as before, repeated "
                 "in sequence.",
                 Write(head), Create(edges), FadeIn(layers, lag_ratio=0.2))
        self.cue("so that the signal passes",
                 ShowPassingFlash(edges.copy().set_color(YELLOW_D).set_stroke(width=3), time_width=0.6, run_time=2.4))
        self.cue("Each element is still", FadeIn(pat), FadeIn(why))
        self.hold(0.6)
        self.clear_stage()

    # ---------------------------------------------------------------- 4. learning
    def learning(self):
        head = self.heading("Data sets the knobs")
        self.ax = ax = Axes(x_range=[-LIM, LIM, 1], y_range=[-LIM, LIM, 1], x_length=5.2, y_length=4.4,
                            axis_config={"color": GREY_B, "include_tip": False, "stroke_width": 2}).move_to([-3.6, 0.4, 0])
        pts = VGroup(*[marker(ax, p, y) for p, y in zip(XS, YS)])
        assert ax.get_bottom()[1] > -2.0

        def panel(h):
            w, b = h["w"], h["b"]
            return VGroup(txt("knob settings", 24, GREY_B),
                          txt(f"w = ({fmt(w[0])}, {fmt(w[1])})", 30, C_MODEL),
                          txt(f"b = {fmt(b)}", 30, C_MODEL),
                          txt(f"mistakes: {h['wrong']} of 20", 28, C_LOSS)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.7, 0.9, 0])

        def line(h):
            p, q = line_ends(h["w"], h["b"])
            return Line(ax.c2p(*p), ax.c2p(*q), color=C_MODEL, stroke_width=5)

        def rings(h):
            wr = np.sign(XS @ h["w"] + h["b"]) != YS
            return VGroup(*[Circle(0.26, color=C_LOSS, stroke_width=4).move_to(ax.c2p(*XS[i])) for i in np.where(wr)[0]])

        def update(h):
            return Transform(ln, line(h)), Transform(pan, panel(h)), Transform(rg, rings(h))

        pan, ln, rg = panel(HIST[0]), line(HIST[0]), rings(HIST[0])
        legend = txt("circle: +1     cross: −1", 22, GREY_B).move_to([3.7, -0.8, 0])
        assert pan.get_right()[0] < 6.9 and legend.get_bottom()[1] > -2.6
        assert len(XS) == 20 and [h["wrong"] for h in HIST] == [10, 4, 2, 6, 0]      # all spoken below
        self.say("If nobody sets the knobs by hand, then the data has to do it. Here are twenty labeled points, "
                 "and a line drawn from a random starting guess. The line is where the weighted sum hits zero, "
                 "and every point on the wrong side gets a red ring. Right now that's ten mistakes.",
                 Write(head), Create(ax), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.05), FadeIn(legend))
        self.cue("a line drawn from", Create(ln), FadeIn(pan))
        self.cue("every point on the wrong side", Create(rg))
        rule = VGroup(mt(r"w\leftarrow w+y\,x", 0.8, C_MODEL), mt(r"b\leftarrow b+y", 0.8, C_MODEL)
                      ).arrange(RIGHT, buff=0.6).move_to([3.7, -1.6, 0])
        assert rule.get_right()[0] < 6.9
        h1 = HIST[1]
        i1 = h1["idx"]
        self.say("The fix is almost too simple. We grab one mistake, add its label times its input to the "
                 "weights, and add its label to the bias. The line swings toward that point, and the mistakes "
                 "drop from ten to four.",
                 Indicate(pts[i1], color=YELLOW_D, scale_factor=2.0), Write(rule))
        self.cue("The line swings", *update(h1))
        self.hold(0.3)
        h2, h3 = HIST[2], HIST[3]
        h4 = HIST[4]
        self.say("Do it again and we're down to two. But the next update jumps back up to six, so a single step "
                 "can make things worse. Keep going anyway, and after four updates there are zero mistakes. "
                 "Nobody chose those knob settings, the data did.",
                 Indicate(pts[h2["idx"]], color=YELLOW_D, scale_factor=2.0), *update(h2))
        self.cue("But the next update", Indicate(pts[h3["idx"]], color=YELLOW_D, scale_factor=2.0), *update(h3), run_time=1.6)
        self.cue("Keep going anyway", *update(h4))
        self.hold(0.6)
        self.pts, self.ln, self.rule = pts, ln, rule
        self.clear_stage(ax, ln)
        self.head_ref = head

    # ---------------------------------------------------------------- 5. new data
    def new_data(self):
        ax = self.ax
        head = self.heading("New data")
        fresh = VGroup(*[marker(ax, p, y, C_NEW, 0.1) for p, y in zip(XF, YF1)])
        ring1 = VGroup(*[Circle(0.2, color=C_LOSS, stroke_width=3).move_to(ax.c2p(*XF[i])) for i in np.where(WRONG1)[0]])
        k1 = int(WRONG1.sum())
        assert k1 == round((1 - ACC1) * 100)
        stat = VGroup(txt("fresh points, same source", 24, C_NEW),
                      txt(f"correct: {round(ACC1 * 100)} of 100", 34, GREEN_C),
                      txt(f"wrong: {k1}", 28, C_LOSS)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.7, 0.9, 0])
        assert stat.get_right()[0] < 6.9
        assert round(ACC1 * 100) == 92 and round(ACC2 * 100) == 53      # spoken below
        self.say("But we never really cared about those twenty points. So let's draw a hundred fresh points "
                 "from the same source, and the circuit gets ninety-two of them right. The misses all hug the "
                 "boundary, because the learned line is close to the real rule, just not exactly on it.",
                 Write(head), LaggedStart(*[FadeIn(p) for p in fresh], lag_ratio=0.01, run_time=1.8), FadeIn(stat[0]))
        self.cue("the circuit gets ninety-two", FadeIn(stat[1:]))
        self.cue("The misses all hug", Create(ring1))
        fresh2 = VGroup(*[marker(ax, p, y, C_NEW, 0.1) for p, y in zip(XF, YF2)])
        ring2 = VGroup(*[Circle(0.2, color=C_LOSS, stroke_width=3).move_to(ax.c2p(*XF[i])) for i in np.where(WRONG2)[0]])
        k2 = int(WRONG2.sum())
        stat2 = VGroup(txt("same points, a different pattern", 24, C_NEW),
                       txt(f"correct: {round(ACC2 * 100)} of 100", 34, GREEN_C),
                       txt(f"wrong: {k2}", 28, C_LOSS)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.7, 0.9, 0])
        assert stat2.get_right()[0] < 6.9
        self.say("Now change the rule behind the labels. The same circuit gets only fifty-three right, which is "
                 "a coin flip, because it learned one pattern and not this one. That's why the definition says "
                 "relevant pattern. Learning only pays off if the new data follows the same rule.",
                 FadeOut(ring1), Transform(fresh, fresh2), Transform(stat, stat2), FadeIn(ring2))
        self.cue("That's why the definition", Indicate(stat[0], color=C_NEW))
        self.hold(0.6)
