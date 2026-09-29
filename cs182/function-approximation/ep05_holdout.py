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

    def construct(self):
        self.title_card()
        self.splits()
        self.shortcut()
        self.choose_unit()
        self.formulation()
        self.recap()
        self.end_card(
            ["Split at the unit that will be new in deployment",
             "Random rows let a memorizer look like a learner",
             "A hospital-only model can beat a real one on a new hospital",
             "Ask first: does a pattern exist, matter, show up in data, and can it be extracted?"],
        )

    # ---------------------------------------------------------------- 1. splits
    def splits(self):
        head = self.heading("Which rows are held out?")
        panels = []
        for cx, tag in [(-3.6, "random rows"), (3.6, "whole patients")]:
            cap = txt(tag, 28, WHITE).move_to([cx, 2.4, 0])
            frame = Rectangle(width=5.9, height=3.75, stroke_color=GREY_D, stroke_width=2).move_to([cx, 0.15, 0])
            panels.append((cx, cap, frame))
        self.say("Forty patients, five scans each. Every scan is its patient's fingerprint plus noise; the labels are coin flips.",
                 Write(head), *[FadeIn(g) for _, c, fr in panels for g in (c, fr)])

        def draw(cx, mask):
            return VGroup(*[Dot(to_panel(XS[i], cx), radius=0.055, color=C_TEST if mask[i] else C_TRAIN) for i in range(NP * NS)])

        dl, dr = draw(-3.6, ROW_TEST), draw(3.6, PAT_TEST)
        for g in (dl, dr):
            assert abs(g.get_center()[1] - 0.15) < 0.3 and g.get_bottom()[1] > -1.85 and g.get_top()[1] < 2.05
        self.say("Left: shuffle rows, half become test. Right: shuffle patients, half of the patients become test.",
                 FadeIn(dl), FadeIn(dr))

        def links(cx, te, nn):
            return VGroup(*[Line(to_panel(XS[t], cx), to_panel(XS[n], cx), color=YELLOW_D, stroke_width=3) for t, n in zip(te[:12], nn[:12])])

        ll, lr = links(-3.6, TE_ROW, NN_ROW), links(3.6, TE_PAT, NN_PAT)
        self.say("A 1-nearest-neighbor model just memorizes. Each test scan copies the label of its closest training scan.",
                 Create(ll), Create(lr))
        ra = txt(f"accuracy {ACC_ROW:.0%}", 32, C_TRAIN).move_to([-3.6, -2.2, 0])
        rb = txt(f"accuracy {ACC_PAT:.0%}", 32, C_LOSS).move_to([3.6, -2.2, 0])
        self.say("With random rows the closest scan is the same patient: about 100 percent, on labels that are pure noise.",
                 FadeIn(ra))
        self.say("Split by patient and the trick collapses to chance. The honest number is the one on the right.", FadeIn(rb))
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
        self.say("Two hospitals, a hundred chest scans each. In one hospital 34 percent are sick, in the other 1 percent.",
                 Write(head), *[FadeIn(g) for g in grids], *[FadeIn(t) for t in labels])
        box = VGroup(txt("model input: hospital ID", 26, GREY_B), txt("(the pixels are ignored)", 24, GREY_B),
                     txt(f"AUC = {AUC_TOY:.2f}", 44, C_LOSS)).arrange(DOWN, buff=0.25).move_to([4.6, 0.4, 0])
        assert box.get_right()[0] < 6.9
        self.say(f"Predict from the hospital name alone and the AUC, the area under the ROC curve, is {AUC_TOY:.2f}.",
                 FadeIn(box))
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
        self.say("A published pneumonia CNN scored AUC 0.93 on test scans from the hospitals it trained on.",
                 Write(head), Create(axis), FadeIn(chance), GrowFromEdge(bars[0], DOWN), FadeIn(cap_txt[0]))
        self.say("On scans from a new hospital it fell to 0.82. The same model, the same disease, a different building.",
                 GrowFromEdge(bars[1], DOWN), FadeIn(cap_txt[1]))
        note = txt("hospital identity was readable from the image with > 99.9% accuracy", 24, YELLOW_D).move_to([0, 2.65, 0])
        assert note.width < 13
        self.say("Prevalence differed by site, so the hospital name alone scores 0.86 on the pooled test set.",
                 GrowFromEdge(bars[2], DOWN), FadeIn(cap_txt[2]), FadeIn(note))
        self.say("The CNN read scanner signatures, patient positioning and text overlays, without needing the lungs at all.",
                 Indicate(note, color=YELLOW_D))
        self.say("Random splits could never catch this: the shortcut lives on both sides. Hold out the hospital.", Indicate(bars[1], color=C_TEST))
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
        self.say("Hold out whole units: a patient, a document, a time period, a molecule scaffold or a cluster of near-duplicates.",
                 Write(head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.3))
        rule = VGroup(txt("mimic deployment, no more:", 26, YELLOW_D),
                      txt("a much harder test set", 24, GREY_B),
                      txt("misleads just as much", 24, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.3, 0.5, 0])
        assert rule.get_right()[0] < 6.6 and rule.get_left()[0] > rows.get_right()[0]
        self.say("Mimic deployment and nothing more. A test set that differs in unrelated ways teaches you nothing either.", FadeIn(rule))
        credit = txt("Leakage surveys: Kapoor and Narayanan, 2023", 22, GREY_B).move_to([0, -2.2, 0])
        self.say("Leakage is common: surveys across many fields keep finding the same mistake, and it inflates reported results.", FadeIn(credit))
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
        self.say("Before any model, ask four questions. Does a pattern exist? Does it matter? Can we observe it? Can we extract it?",
                 Write(head), LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in boxes], lag_ratio=0.3), FadeIn(qtx))
        fail = txt("the hospital shortcut passes the last three and fails the point of the task", 24, C_LOSS).move_to([0, -1.5, 0])
        assert fail.width < 13
        self.say("A model can pass the last three and still miss the point, as the hospital shortcut did.", FadeIn(fail))
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
        self.say("Function approximation covers a family: supervised learning with labels, such as regression and classification.",
                 Write(head), FadeIn(allg[0]))
        self.say("Unsupervised learning finds structure without labels: embeddings like PCA, or density estimation, one route to generation.",
                 FadeIn(allg[1]))
        self.say("Foundation models pretrain on broad data first, then are prompted or adapted. Same ideas, bigger scale.", FadeIn(allg[2]))
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
        self.say("Samples do not determine a function. Ramps make a flexible basis, and layers stack them.",
                 Write(head), LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cols[:3]], lag_ratio=0.3))
        self.say("The training surrogate is not the goal, and honest evaluation holds out exactly what will be new.",
                 LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cols[3:]], lag_ratio=0.3))
        self.hold(0.5)
