"""Episode 5 — Hold Out What Will Be New (Note 1, sections 1.4-1.5: data splits, leakage, problem formulation)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import *  # noqa: E402,F403

# ------------------------------------------------------------------ numbers

# (a) 40 patients x 5 scans; every scan is its patient's fingerprint plus noise; labels are coin flips per patient
rng = np.random.RandomState(5)
NP, NS = 40, 5
GX, GY = np.meshgrid(np.arange(8), np.arange(5))
CEN = np.stack([GX.ravel(), GY.ravel()], 1) + rng.uniform(-0.2, 0.2, (NP, 2))
PAT = np.repeat(np.arange(NP), NS)
XS = CEN[PAT] + rng.normal(0, 0.1, (NP * NS, 2))
LAB_P = rng.randint(0, 2, NP)
LAB = LAB_P[PAT]

ROW_TEST = np.zeros(NP * NS, bool)
ROW_TEST[rng.permutation(NP * NS)[: NP * NS // 2]] = True
TEST_PATS = rng.permutation(NP)[: NP // 2]
PAT_TEST = np.isin(PAT, TEST_PATS)


def one_nn(test_mask):
    tr, te = np.where(~test_mask)[0], np.where(test_mask)[0]
    d = np.linalg.norm(XS[te][:, None, :] - XS[tr][None, :, :], axis=2)
    nn = tr[d.argmin(1)]
    return te, nn, float(np.mean(LAB[nn] == LAB[te]))


TE_ROW, NN_ROW, ACC_ROW = one_nn(ROW_TEST)
TE_PAT, NN_PAT, ACC_PAT = one_nn(PAT_TEST)
assert ACC_ROW > 0.97, ACC_ROW                       # memorizing patients looks like skill
assert 0.35 < ACC_PAT < 0.65, ACC_PAT                # labels are random: chance on a new patient
assert np.mean(PAT[NN_ROW] == PAT[TE_ROW]) > 0.97    # the neighbour is the same patient's other scan
assert np.all(PAT[NN_PAT] != PAT[TE_PAT])            # by construction no patient is on both sides

# (b) two-hospital toy: prevalence 34 % vs 1 %, 100 patients each; score = hospital only
SICK = [34, 1]
POS = [1] * SICK[0] + [0] * (100 - SICK[0]) + [1] * SICK[1] + [0] * (100 - SICK[1])
HOSP = [0] * 100 + [1] * 100
SCORE = [SICK[h] / 100 for h in HOSP]
pos_s = [s for s, y in zip(SCORE, POS) if y == 1]
neg_s = [s for s, y in zip(SCORE, POS) if y == 0]
AUC_TOY = (sum(1.0 for a in pos_s for b in neg_s if a > b) + 0.5 * sum(1.0 for a in pos_s for b in neg_s if a == b)) / (len(pos_s) * len(neg_s))
assert len(pos_s) == 35 and len(neg_s) == 165
assert abs(AUC_TOY - (34 / 35 * 0.6 + 0.5 * (34 / 35 * 0.4 + 1 / 35 * 0.6))) < 1e-12 and abs(AUC_TOY - 0.786) < 0.001

# (c) numbers quoted from Note 1 (Zech et al.); not recomputed here
AUC_INTERNAL, AUC_EXTERNAL, AUC_HOSP_ONLY = 0.93, 0.82, 0.86
assert AUC_INTERNAL > AUC_HOSP_ONLY > AUC_EXTERNAL > AUC_TOY > 0.5


def to_panel(p, cx, cy=0.15, s=0.7):
    return np.array([cx + (p[0] - 3.5) * s, cy + (p[1] - 2.0) * s, 0.0])


class Ep05Holdout(NarratedScene):
    series = SERIES
    SCENES = ["splits", "shortcut", "choose_unit", "formulation", "recap"]

    def construct(self):
        self.title_card()
        self.splits()
        self.shortcut()
        self.choose_unit()
        self.formulation()
        self.recap()
        self.end_card(
            ["Split at the unit that will be new in deployment",
             "Random row splits let a memorizer look like a genius",
             "A model can ace the test by reading the hospital, not the disease",
             "First ask: is there a pattern, does it matter, can we see it, can we learn it?"],
        )

    # ---------------------------------------------------------------- 1. splits
    def splits(self):
        head = self.heading("Which rows are held out?")
        panels = []
        for cx, tag in [(-3.6, "random rows"), (3.6, "whole patients")]:
            cap = txt(tag, 28, WHITE).move_to([cx, 2.4, 0])
            frame = Rectangle(width=5.9, height=3.75, stroke_color=GREY_D, stroke_width=2).move_to([cx, 0.15, 0])
            panels.append((cx, cap, frame))

        def draw(cx, mask):
            return VGroup(*[Dot(to_panel(XS[i], cx), radius=0.055, color=C_TEST if mask[i] else C_TRAIN) for i in range(NP * NS)])

        dl, dr = draw(-3.6, ROW_TEST), draw(3.6, PAT_TEST)
        for g in (dl, dr):
            assert abs(g.get_center()[1] - 0.15) < 0.3 and g.get_bottom()[1] > -1.85 and g.get_top()[1] < 2.05
        assert (NP, NS) == (40, 5)                            # spoken below
        self.say("Can a model get top marks on labels that are pure noise? Watch this. We have forty patients with five scans "
                 "each, and every patient's label comes from a coin flip. On the left we shuffle all the scans "
                 "and hold out half of them, and on the right we hold out half of the patients instead.",
                 Write(head), *[FadeIn(g) for _, c, fr in panels for g in (c, fr)])
        self.cue("On the left we shuffle", FadeIn(dl))
        self.cue("on the right we hold out", FadeIn(dr))

        def links(cx, te, nn):
            return VGroup(*[Line(to_panel(XS[t], cx), to_panel(XS[n], cx), color=YELLOW_D, stroke_width=3) for t, n in zip(te[:12], nn[:12])])

        ll, lr = links(-3.6, TE_ROW, NN_ROW), links(3.6, TE_PAT, NN_PAT)
        ra = txt(f"accuracy {ACC_ROW:.0%}", 32, C_TRAIN).move_to([-3.6, -2.2, 0])
        rb = txt(f"accuracy {ACC_PAT:.0%}", 32, C_LOSS).move_to([3.6, -2.2, 0])
        assert f"{ACC_ROW * 100:.0f}" == "100" and f"{ACC_PAT * 100:.0f}" == "58"      # spoken below
        self.say("Now take the laziest model there is, where each test scan just copies the label of the closest "
                 "training scan. On the left, the closest scan belongs to the same patient, so it scores one "
                 "hundred percent on coin flips. Split by patient and the trick falls apart. We get fifty-eight "
                 "percent, which is about chance, and that's the honest number.",
                 Create(ll), Create(lr))
        self.cue("On the left, the closest scan", FadeIn(ra))
        self.cue("Split by patient", FadeIn(rb))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 2. shortcut
    def shortcut(self):
        head = self.heading("A shortcut that is not medicine")
        cxs = [-4.6, -0.9]
        grids, labels = [], []
        for h, cx in enumerate(cxs):
            g = VGroup(*[Dot(radius=0.1, color=C_LOSS if POS[h * 100 + i] and (h * 100 + i) < 200 else GREY_D) for i in range(100)])
            g.arrange_in_grid(10, 10, buff=0.16).move_to([cx, 0.3, 0])
            # sick patients first in the list -> recolour by the actual label
            for i, d in enumerate(g):
                d.set_color(C_LOSS if POS[h * 100 + i] else GREY_D)
            grids.append(g)
            labels.append(txt(f"{'AB'[h]}: {SICK[h]} of 100 sick", 26, WHITE).next_to(g, UP, buff=0.3))
        assert grids[1].get_right()[0] < 1.2 and grids[0].get_left()[0] > -6.6
        box = VGroup(txt("model input: hospital ID", 26, GREY_B), txt("(the pixels are ignored)", 24, GREY_B),
                     txt(f"AUC = {AUC_TOY:.2f}", 44, C_LOSS)).arrange(DOWN, buff=0.25).move_to([4.6, 0.4, 0])
        assert box.get_right()[0] < 6.9
        assert SICK == [34, 1] and f"{AUC_TOY:.2f}" == "0.79"      # spoken below
        self.say("Here's a sneakier version of the same problem, with two hospitals and a hundred chest scans each. At the first "
                 "one thirty-four patients are sick, and at the second only one is. Now ignore the pixels and "
                 "guess from the hospital name alone. The area under the ROC curve, where one half is chance, "
                 "comes out at zero point seven nine.",
                 Write(head), *[FadeIn(g) for g in grids], *[FadeIn(t) for t in labels],
                 speak="Here's a sneakier version of the same problem, with two hospitals and a hundred chest scans each. At the first "
                       "one thirty-four patients are sick, and at the second only one is. Now ignore the pixels and "
                       "guess from the hospital name alone. The area under the R O C curve, where one half is "
                       "chance, comes out at zero point seven nine.")
        self.cue("Now ignore the pixels", FadeIn(box[:2]))
        self.cue("comes out at", FadeIn(box[2]))
        self.hold(0.5)
        self.clear_stage()

        head = self.heading("Zech et al.: chest X-rays")
        base_y, hgt = -1.7, 3.6
        vals = [(AUC_INTERNAL, "same hospitals", C_TRAIN), (AUC_EXTERNAL, "new hospital", C_TEST), (AUC_HOSP_ONLY, "hospital ID only", GREY_A)]
        bars, cap_txt = VGroup(), VGroup()
        for k, (v, name, col) in enumerate(vals):
            x = -3.6 + 3.4 * k
            h = (v - 0.5) / 0.5 * hgt
            r = Rectangle(width=1.7, height=h, stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.25)
            r.move_to([x, base_y + h / 2, 0])
            bars.add(r)
            cap_txt.add(VGroup(txt(f"{v:.2f}", 36, col).next_to(r, UP, buff=0.12), txt(name, 24, GREY_B).next_to(r, DOWN, buff=0.15)))
        axis = Line([-5.6, base_y, 0], [4.6, base_y, 0], color=GREY_B, stroke_width=2)
        chance = txt("0.5 = chance", 22, GREY_B).move_to([5.6, base_y, 0])
        assert bars.get_top()[1] < 2.3 and chance.get_right()[0] < 7.0
        assert (AUC_INTERNAL, AUC_EXTERNAL, AUC_HOSP_ONLY) == (0.93, 0.82, 0.86)      # spoken below
        self.say("And this really happened, to a published pneumonia detector built on a convolutional network. "
                 "It scored zero point nine three on scans from its own hospitals. At a new hospital it fell to "
                 "zero point eight two. It was the same model and the same disease, just in a different "
                 "building.",
                 Write(head), Create(axis), FadeIn(chance), GrowFromEdge(bars[0], DOWN), FadeIn(cap_txt[0]))
        self.cue("At a new hospital", GrowFromEdge(bars[1], DOWN), FadeIn(cap_txt[1]))
        note = txt("hospital identity was readable from the image with > 99.9% accuracy", 24, YELLOW_D).move_to([0, 2.65, 0])
        assert note.width < 13
        self.say("And what about the hospital name alone? That scores zero point eight six on the pooled test "
                 "set, because the sick rates differed from site to site. So the network was reading "
                 "scanner quirks, patient positioning, and stamped text, instead of the lungs. A "
                 "random split can't catch this, because the shortcut sits on both sides. You have to hold "
                 "out the hospital.",
                 GrowFromEdge(bars[2], DOWN), FadeIn(cap_txt[2]))
        self.cue("So the network was reading", FadeIn(note))
        self.cue("A random split", Indicate(bars[1], color=C_TEST))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 2b. choose the unit
    def choose_unit(self):
        head = self.heading("Split at the unit that will be new")
        units = [("patient", "medical images"), ("document", "text corpora"), ("time period", "forecasting"),
                 ("molecule scaffold", "drug discovery"), ("near-duplicate cluster", "web-scale data")]
        rows = VGroup(*[VGroup(txt(u, 30, C_TEST), txt("→", 28, GREY_B), txt(d, 26, GREY_A)).arrange(RIGHT, buff=0.4) for u, d in units])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-2.9, 0.5, 0])
        assert rows.width < 7.6 and rows.get_left()[0] > -6.7 and rows.get_bottom()[1] > -2.2
        rule = VGroup(txt("mimic deployment, no more:", 26, YELLOW_D),
                      txt("a much harder test set", 24, GREY_B),
                      txt("misleads just as much", 24, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.3, 0.5, 0])
        assert rule.get_right()[0] < 6.6 and rule.get_left()[0] > rows.get_right()[0]
        credit = txt("Leakage surveys: Kapoor and Narayanan, 2023", 22, GREY_B).move_to([0, -2.2, 0])
        self.say("So the rule is to hold out whatever will be new in deployment. That might be a patient, a "
                 "document, a time period, or a molecule scaffold. But match deployment and no more, because "
                 "a test set that differs in unrelated ways misleads you just as much.",
                 Write(head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.3))
        self.cue("But match deployment", FadeIn(rule))
        self.say("And none of this is rare, because surveys across many fields keep finding leakage like this, and it "
                 "keeps inflating published results.",
                 FadeIn(credit))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 3. formulation
    def formulation(self):
        head = self.heading("Is the problem coherent?")
        names = ["pattern exists", "pattern matters", "pattern is observable", "pattern is extractable"]
        qs = ["is the outcome\npredictable at all?", "would a decision\nchange?", "do the recorded\nfeatures carry it?", "can data + model\nfind it?"]
        cols = [C_TARGET, YELLOW_D, C_TRAIN, C_MODEL]
        boxes = VGroup(*[box_label(n, c, w=2.95, h=0.9, font_size=22) for n, c in zip(names, cols)]).arrange(RIGHT, buff=0.35).move_to([0, 1.5, 0])
        assert boxes.width < 13.4
        qtx = VGroup(*[txt(q, 22, GREY_B, line_spacing=0.9).next_to(boxes[i], DOWN, buff=0.25) for i, q in enumerate(qs)])
        fail = txt("the hospital shortcut passes the last three and fails the point of the task", 24, C_LOSS).move_to([0, -1.5, 0])
        assert fail.width < 13
        self.say("Before building any model, there are four things to check. A pattern has to exist, and it "
                 "has to matter for some decision. It also has to show up in the features we record, and a "
                 "model has to be able to pull it out. The hospital shortcut passed the last three checks "
                 "and still missed the point, because it wasn't medicine.",
                 Write(head), FadeIn(boxes[0], shift=UP * 0.2), FadeIn(qtx[0]))
        self.cue("it has to matter", FadeIn(boxes[1], shift=UP * 0.2), FadeIn(qtx[1]))
        self.cue("It also has to show up", FadeIn(boxes[2], shift=UP * 0.2), FadeIn(qtx[2]))
        self.cue("a model has to be able", FadeIn(boxes[3], shift=UP * 0.2), FadeIn(qtx[3]))
        self.cue("The hospital shortcut", FadeIn(fail))
        self.hold(0.4)
        self.clear_stage()

        head = self.heading("Vocabulary map")
        groups = [("supervised", C_LOSS, ["regression", "classification", "localized annotation"]),
                  ("unsupervised", C_TRAIN, ["embeddings, e.g. PCA", "density estimation"]),
                  ("foundation models", C_MODEL, ["pretrain on broad data", "prompt or adapt"])]
        cols_x = [-4.4, 0.0, 4.4]
        allg = VGroup()
        for (name, col, kids), x in zip(groups, cols_x):
            top = box_label(name, col, w=3.6, h=0.9, font_size=26).move_to([x, 1.6, 0])
            ch = VGroup(*[txt(k, 22, WHITE) for k in kids]).arrange(DOWN, buff=0.3).next_to(top, DOWN, buff=0.5)
            assert ch.width < 4.2
            allg.add(VGroup(top, ch))
        self.say("Now let's zoom out for a moment and name the kinds of learning. Everything so far was supervised learning, where labels drive "
                 "regression or classification. Take the labels away and you're finding structure instead, "
                 "with embeddings or density estimation. And foundation models learn from broad data first "
                 "and then get prompted or adapted, which is the same ideas at a bigger scale.",
                 Write(head), FadeIn(allg[0]))
        self.cue("Take the labels away", FadeIn(allg[1]))
        self.cue("And foundation models", FadeIn(allg[2]))
        self.hold(0.5)
        self.clear_stage()

    # ---------------------------------------------------------------- 4. recap
    def recap(self):
        head = self.heading("The series in five moves")
        items = [("1  samples", C_DATA, "learn from points"), ("2  ramps", C_RAMP, "basis of ReLU"),
                 ("3  layer", C_MODEL, "affine · ReLU · affine"), ("4  risk", C_LOSS, "proxy vs. goal"),
                 ("5  hold-out", C_TEST, "split at the new unit")]
        cols = VGroup(*[VGroup(box_label(a, c, w=2.4, h=0.9, font_size=24), txt(b, 20, GREY_B)).arrange(DOWN, buff=0.25) for a, c, b in items]).arrange(RIGHT, buff=0.22).move_to([0, 0.6, 0])
        assert cols.width < 13.4
        self.say("So here's the whole unit one more time, in five moves. Samples alone don't pin down a function. Ramps are "
                 "flexible pieces, and a layer runs many of them at once. What we train on isn't what we "
                 "actually want, and an honest test holds out exactly what will be new.",
                 Write(head), FadeIn(cols[0], shift=UP * 0.2))
        self.cue("Ramps are flexible pieces", FadeIn(cols[1], shift=UP * 0.2))
        self.cue("a layer runs many", FadeIn(cols[2], shift=UP * 0.2))
        self.cue("What we train on", FadeIn(cols[3], shift=UP * 0.2))
        self.cue("an honest test", FadeIn(cols[4], shift=UP * 0.2))
        self.hold(0.5)
