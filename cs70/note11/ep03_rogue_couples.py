"""CS70 Note 11, episode 03: rogue couples, and what makes a matching stable.

Built from BOARD-ep03.md: every `> ` line of the board is one say() below, copied
unchanged, and the picture is built as the board's stage lines describe.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---------------------------------------------------------------- FACTS
# The board's "Facts" table. Every list, name and number the episode shows or says is
# computed here and asserted; the picture reads these names and never a typed-in value.
JOBS = {"Approximation": ["Anita", "Bridget", "Christine"],
        "Basis": ["Bridget", "Anita", "Christine"],
        "Control": ["Anita", "Bridget", "Christine"]}
CANDS = {"Anita": ["Basis", "Approximation", "Control"],
         "Bridget": ["Approximation", "Basis", "Control"],
         "Christine": ["Approximation", "Basis", "Control"]}
JOB_NAMES = list(JOBS)                   # left to right on the stage
CAND_NAMES = list(CANDS)
U = {"Approximation": "Christine", "Basis": "Bridget", "Control": "Anita"}
S = {"Approximation": "Bridget", "Basis": "Anita", "Control": "Christine"}
E = {"Approximation": "Anita", "Basis": "Bridget", "Control": "Christine"}


def rogue(m):                            # every rogue couple (job, candidate) of the matching m
    has = {c: j for j, c in m.items()}
    out = []
    for j in JOBS:
        for c in JOBS[j]:
            if c == m[j]:
                break                    # only the names above the job's partner
            if CANDS[c].index(j) < CANDS[c].index(has[c]):
                out.append((j, c))
    return out


def above_partner(j, m):                 # the names a job ranks above its partner
    return JOBS[j][:JOBS[j].index(m[j])]


assert len(JOBS) == 3 and len(CANDS) == 3                       # "the three jobs and the three candidates"
assert all(len(v) == 3 for v in JOBS.values()) and all(len(v) == 3 for v in CANDS.values())
assert all(set(m) == set(JOBS) and set(m.values()) == set(CANDS) for m in (U, S, E))
assert rogue(U) == [("Approximation", "Anita"), ("Approximation", "Bridget")]     # F7
assert len(rogue(U)) == 2                                       # "a second rogue couple"
assert ("Approximation", "Bridget") in rogue(U)                 # F6
assert rogue(S) == [] and rogue(E) == [] and E != S             # F8, F10
assert JOBS["Control"][-1] == S["Control"] == "Christine" and CANDS["Christine"][-1] == "Control"  # F9
assert all(above_partner(j, m) == [] for j in JOBS for m in (S, E) if JOBS[j].index(m[j]) == 0)
assert [len(above_partner(j, S)) for j in JOB_NAMES] == [1, 1, 2]                # beat 3.1: four cells
assert sum(len(above_partner(j, S)) for j in JOBS) == 4                          # "the names above its partner"
assert above_partner("Control", E) == ["Anita", "Bridget"]                       # beat 3.5
assert JOBS["Approximation"].index("Bridget") < JOBS["Approximation"].index("Christine")   # beats 2.1, 3.2
assert CANDS["Bridget"].index("Approximation") < CANDS["Bridget"].index("Basis")           # beat 2.2
assert CANDS["Anita"].index("Approximation") < CANDS["Anita"].index("Control")             # beat 2.4

# ---------------------------------------------------------------- the board's stage
X = [-3.9, 0.5, 4.9]                     # the three columns
JOB_Y = [1.86, 1.35, 0.84]               # job cells, the first choice on top
CAND_Y = [-1.41, -1.92, -2.43]           # candidate cells
CELL_W, CELL_H = 2.4, 0.48
JOB_HY, CAND_HY = 2.42, -0.85            # the two header rows
HEAD_W_MAX = 2.0                         # a header's word, inside its 2.4 wide box
RANK_X = 6.45                            # the six rank numbers
STRIP_X = -6.0                           # the left strip
SLOT_A_Y, SLOT_B_Y = 0.22, -0.2
STRIP_X_LEFT = -6.6                     # the strip's left edge: 1.2 wide at x = -6.0 ...
STRIP_GAP = 0.3                         # ... leaves 0.3 to the Approximation column at -5.1
STRIP_W_MAX = 1.2                       # every text in the left strip, the legend included
BAND_X, BAND_Y = -1.7, 0.02             # the closing question of beat 3.6, between E1 and E2
BAND_W_MAX = 4.2                        # at most 4.2 wide, so it touches neither line
LINE_PTS = {                             # the gap between the halves; all lines stroke width 4
    "U1": ((-3.9, 0.55), (4.5, -0.52)),
    "U2": ((0.9, 0.55), (0.9, -0.52)),
    "U3": ((4.9, 0.55), (-3.5, -0.52)),
    "D1": ((-3.5, 0.55), (0.1, -0.52)),
    "D2": ((-4.3, 0.55), (-4.3, -0.52)),
    "S1": ((-3.5, 0.55), (0.1, -0.52)),
    "S2": ((0.5, 0.55), (-3.9, -0.52)),
    "S3": ((4.9, 0.55), (4.9, -0.52)),
    "E1": ((-4.3, 0.55), (-4.3, -0.52)),
    "E2": ((0.9, 0.55), (0.9, -0.52)),
}
DASHED = {"D1", "D2"}                    # the two "would rather" lines
# the pairs that share end points, so they are never on the stage together (D* go at the end
# of scene `unstable`): the check would call two identical shapes one
assert LINE_PTS["D1"] == LINE_PTS["S1"] and LINE_PTS["D2"] == LINE_PTS["E1"]
assert LINE_PTS["U2"] == LINE_PTS["E2"]


def cell_row(ys, x):
    return VGroup(*[Rectangle(width=CELL_W, height=CELL_H, stroke_color=GREY_B, stroke_width=2)
                    .move_to([x, y, 0]) for y in ys])


def flash(mob):
    return Indicate(mob, color=YELLOW_D, scale_factor=1.1)


def reset(mob):
    return mob.animate.set_stroke(GREY_B, 2)


def strip_fit(t):
    if t.width > STRIP_W_MAX:
        t.scale_to_fit_width(STRIP_W_MAX)
    return t


def strip_text(s, size=22, color=GREY_B):
    return strip_fit(txt(s, size, color))


def slot_text(s, y, color=C_TEXT):
    return strip_fit(txt(s, 20, color)).move_to([STRIP_X, y, 0])


def band_text(s):                        # the one large text in the band between the halves
    t = txt(s, 30, YELLOW_D)
    if t.width > BAND_W_MAX:
        t.scale_to_fit_width(BAND_W_MAX)
    return t.move_to([BAND_X, BAND_Y, 0])


def stage_line(key):
    (x0, y0), (x1, y1) = LINE_PTS[key]
    if key in DASHED:                    # a line, not a string of dots, and not thin
        return DashedLine([x0, y0, 0], [x1, y1, 0],
                          color=ORANGE, stroke_width=5, dash_length=0.15)
    return Line([x0, y0, 0], [x1, y1, 0], color=WHITE, stroke_width=4)


class Ep03RogueCouples(NarratedScene):
    """Episode 03: what makes a matching stable, told through rogue couples."""

    SCENES = ["hook", "unstable", "stable"]

    def construct(self):
        if self.preview_only(self.SCENES):
            return
        self.title_card()
        for name in self.SCENES:
            getattr(self, name)()
        self.end_card([
            "A job and a candidate who would both rather have each other than their partners "
            "are a rogue couple.",
            "A matching with a rogue couple is unstable, and a matching with none is stable.",
            "To check a matching, ask for every job only the candidates above its partner.",
            "Stable does not mean that everyone gets their first choice, and one set of lists can have "
            "several stable matchings.",
        ])

    # -- the one stage every scene stands on
    def build_stage(self):
        self.lab_jobs = strip_text("jobs").move_to([STRIP_X, JOB_HY, 0])
        self.lab_cands = strip_text("candidates").move_to([STRIP_X, CAND_HY, 0])
        self.job_head = VGroup(*[box_label(n, BLUE_C, w=2.4, h=0.55, font_size=22)
                                 .move_to([x, JOB_HY, 0]) for n, x in zip(JOB_NAMES, X)])
        self.cand_head = VGroup(*[box_label(n, GOLD_C, w=2.4, h=0.55, font_size=22)
                                  .move_to([x, CAND_HY, 0]) for n, x in zip(CAND_NAMES, X)])
        for head in (*self.job_head, *self.cand_head):
            if head[1].width > HEAD_W_MAX:     # "Approximation" fills the box edge to edge
                head[1].scale_to_fit_width(HEAD_W_MAX)
        self.job_cell = [cell_row(JOB_Y, x) for x in X]
        self.cand_cell = [cell_row(CAND_Y, x) for x in X]
        self.job_names = {(i, r): txt(JOBS[JOB_NAMES[i]][r], 22).move_to([X[i], JOB_Y[r], 0])
                          for i in range(3) for r in range(3)}
        self.cand_names = {(i, r): txt(CANDS[CAND_NAMES[i]][r], 22).move_to([X[i], CAND_Y[r], 0])
                           for i in range(3) for r in range(3)}
        self.rank = VGroup(*[txt(str(k + 1), 18, GREY_B).move_to([RANK_X, y, 0])
                             for ys in (JOB_Y, CAND_Y) for k, y in enumerate(ys)])
        self.all_heads = VGroup(*self.job_head, *self.cand_head)
        self.row1 = VGroup(*[self.job_cell[i][0] for i in range(3)],
                           *[self.cand_cell[i][0] for i in range(3)])
        self.row3 = VGroup(*[self.job_cell[i][2] for i in range(3)],
                           *[self.cand_cell[i][2] for i in range(3)])
        self.slot_a, self.slot_b = None, None

    def job_col(self, i):                    # a whole column: header, its three cells and their names
        return VGroup(self.job_head[i], self.job_cell[i],
                      *[self.job_names[(i, r)] for r in range(3)])

    def cand_col(self, i):
        return VGroup(self.cand_head[i], self.cand_cell[i],
                      *[self.cand_names[(i, r)] for r in range(3)])

    def swap(self, attr, new):
        """Slot A or B changes: the old text out and the new one in, in one animation."""
        old = getattr(self, attr)
        setattr(self, attr, new)
        if old is None:
            return () if new is None else (FadeIn(new),)
        return (FadeOut(old),) if new is None else (FadeOut(old), FadeIn(new))

    # ---- scene 1: the two lists, and what a good matching could mean
    def hook(self):
        self.head1 = self.heading("What is a good matching?")
        self.play(FadeIn(self.head1))
        self.build_stage()

        self.say("Here are the three jobs and the three candidates from the first episode, each with "
                 "the same ranked list as before. The first name under a header is the favourite, and "
                 "the last name is the least wanted.",
                 FadeIn(self.lab_jobs, shift=UP * 0.2),
                 LaggedStart(*[FadeIn(self.job_col(i), shift=UP * 0.2) for i in range(3)], lag_ratio=0.35))
        self.cue("the three candidates", FadeIn(self.lab_cands, shift=DOWN * 0.2),
                 LaggedStart(*[FadeIn(self.cand_col(i), shift=DOWN * 0.2) for i in range(3)],
                             lag_ratio=0.35))
        self.cue("is the favourite", flash(self.row1))
        self.cue("least wanted", flash(self.row3))

        self.say("What should a good matching do for them? We could give as many of them as possible "
                 "their first choice, or as few as possible their last choice. Or we could add up how "
                 "far down its list everybody lands, and make that total small.",
                 flash(self.all_heads))
        self.cue("their first choice",
                 *[self.job_cell[i][0].animate.set_stroke(YELLOW_D, 4) for i in range(3)],
                 *[self.cand_cell[i][0].animate.set_stroke(YELLOW_D, 4) for i in range(3)])
        self.cue("their last choice",
                 *[reset(self.job_cell[i][0]) for i in range(3)],
                 *[reset(self.cand_cell[i][0]) for i in range(3)],
                 *[self.job_cell[i][2].animate.set_stroke(RED_C, 4) for i in range(3)],
                 *[self.cand_cell[i][2].animate.set_stroke(RED_C, 4) for i in range(3)])
        self.cue("add up how far down",
                 *[reset(self.job_cell[i][2]) for i in range(3)],
                 *[reset(self.cand_cell[i][2]) for i in range(3)],
                 FadeIn(self.rank))

        self.say("But all of these are scores handed down from above, and jobs and candidates are free "
                 "to act on their own. So let us look at one matching through their eyes.",
                 flash(self.rank))
        self.cue("free to act", flash(self.all_heads))
        self.cue("through their eyes", flash(self.job_head[0]))
        self.hold()

    # ---- scene 2: the matching that a pair walks away from
    def unstable(self):
        self.head2 = self.heading("A pair that walks away")
        self.play(FadeOut(self.head1), FadeIn(self.head2))
        self.head1 = None
        self.legend = VGroup(
            Square(0.3, stroke_color=GREEN_C, stroke_width=4).move_to([STRIP_X, 1.85, 0]),
            strip_text("partner", 20, GREEN_C).move_to([STRIP_X, 1.55, 0]),
            Square(0.3, stroke_color=ORANGE, stroke_width=4).move_to([STRIP_X, 1.15, 0]),
            strip_text("would rather", 20, ORANGE).move_to([STRIP_X, 0.85, 0]))
        self.u1, self.u2, self.u3 = (stage_line(k) for k in ("U1", "U2", "U3"))
        self.d1, self.d2 = stage_line("D1"), stage_line("D2")

        self.say("Take this matching, where Approximation has Christine, Basis has Bridget, and "
                 "Control has Anita. Start with Approximation, which sits at the bottom of its own "
                 "list with Christine, so it would rather have Bridget.",
                 FadeIn(self.legend))
        self.cue("Approximation has Christine", Create(self.u1),
                 self.job_cell[0][2].animate.set_stroke(GREEN_C, 4),
                 self.cand_cell[2][0].animate.set_stroke(GREEN_C, 4))
        self.cue("Basis has Bridget", Create(self.u2),
                 self.job_cell[1][0].animate.set_stroke(GREEN_C, 4),
                 self.cand_cell[1][1].animate.set_stroke(GREEN_C, 4))
        self.cue("has Anita", Create(self.u3),
                 self.job_cell[2][0].animate.set_stroke(GREEN_C, 4),
                 self.cand_cell[0][2].animate.set_stroke(GREEN_C, 4))
        self.cue("would rather have Bridget", self.job_cell[0][1].animate.set_stroke(ORANGE, 4))

        self.say("But wanting is not enough, because Bridget has to want it too. Bridget has Basis, the "
                 "second name on her list, and the first name on her list is Approximation. So "
                 "Approximation and Bridget would both rather have each other, and they can simply walk "
                 "away from this matching together.",
                 flash(self.cand_head[1]))
        self.cue("Bridget has Basis", flash(self.cand_cell[1][1]))
        self.cue("the first name on her list", self.cand_cell[1][0].animate.set_stroke(ORANGE, 4))
        self.cue("would both rather have each other", Create(self.d1))

        self.say("And look what that does to the others. Approximation drops Christine, who is suddenly "
                 "without a job, and Bridget leaves Basis, which suddenly has an empty position. A pair "
                 "like this is called a rogue couple, and a matching that contains one is called "
                 "unstable.",
                 flash(self.d1))
        self.cue("drops Christine", self.u1.animate.set_stroke(color=RED_C, opacity=0.3),
                 self.cand_head[2][0].animate.set_stroke(RED_C, 3))
        self.cue("leaves Basis", self.u2.animate.set_stroke(color=RED_C, opacity=0.3),
                 self.job_head[1][0].animate.set_stroke(RED_C, 3))
        self.cue("rogue couple", *self.swap("slot_a", slot_text("rogue couple", SLOT_A_Y, ORANGE)))
        self.cue("called unstable", *self.swap("slot_b", slot_text("unstable", SLOT_B_Y, RED_C)))

        self.say("Is that the only rogue couple here? Approximation also ranks Anita above Christine, "
                 "and Anita, who has Control at the bottom of her list, ranks Approximation above it. So "
                 "Approximation and Anita are a second rogue couple, and one is already enough to make "
                 "a matching unstable.",
                 self.u1.animate.set_stroke(color=WHITE, opacity=1),
                 self.u2.animate.set_stroke(color=WHITE, opacity=1),
                 self.cand_head[2][0].animate.set_stroke(GOLD_C, 3),
                 self.job_head[1][0].animate.set_stroke(BLUE_C, 3))
        self.cue("ranks Anita above Christine", self.job_cell[0][0].animate.set_stroke(ORANGE, 4))
        self.cue("ranks Approximation above it", self.cand_cell[0][1].animate.set_stroke(ORANGE, 4))
        self.cue("second rogue couple", Create(self.d2))
        self.cue("already enough", flash(self.slot_b))
        self.hold()
        self.play(*[FadeOut(m) for m in (self.u1, self.u2, self.u3, self.d1, self.d2)],
                  *self.swap("slot_a", None), *self.swap("slot_b", None),
                  *[reset(c) for col in (*self.job_cell, *self.cand_cell) for c in col])
        self.u1 = self.u2 = self.u3 = self.d1 = self.d2 = None

    # ---- scene 3: the matching that holds, checked job by job
    def stable(self):
        self.head3 = self.heading("No pair walks away")
        self.play(FadeOut(self.head2), FadeIn(self.head3))
        self.head2 = None
        self.s1, self.s2, self.s3 = (stage_line(k) for k in ("S1", "S2", "S3"))
        self.e1, self.e2 = stage_line("E1"), stage_line("E2")

        self.say("Now try a different matching, where Approximation has Bridget, Basis has Anita, and "
                 "Control has Christine. To hunt for a rogue couple we can go through the jobs one at a "
                 "time. A job only prefers the names above its partner, so those are the only "
                 "candidates we need to ask.")
        self.cue("Approximation has Bridget", Create(self.s1),
                 self.job_cell[0][1].animate.set_stroke(GREEN_C, 4),
                 self.cand_cell[1][0].animate.set_stroke(GREEN_C, 4))
        self.cue("Basis has Anita", Create(self.s2),
                 self.job_cell[1][1].animate.set_stroke(GREEN_C, 4),
                 self.cand_cell[0][0].animate.set_stroke(GREEN_C, 4))
        self.cue("Control has Christine", Create(self.s3),
                 self.job_cell[2][2].animate.set_stroke(GREEN_C, 4),
                 self.cand_cell[2][2].animate.set_stroke(GREEN_C, 4))
        self.above = VGroup(*[self.job_cell[i][r] for i in range(3)
                              for r in range(len(above_partner(JOB_NAMES[i], S)))])
        self.cue("the names above its partner", flash(self.above))

        self.say("Approximation has Bridget and would rather have Anita. But Anita has Basis, the very "
                 "first name on her list, so she will not move. That is why Approximation and Anita are "
                 "no rogue couple here.",
                 flash(self.job_head[0]))
        self.cue("would rather have Anita", self.job_cell[0][0].animate.set_stroke(ORANGE, 4))
        self.cue("Anita has Basis", flash(self.cand_cell[0][0]))
        self.cue("no rogue couple here", reset(self.job_cell[0][0]))

        self.say("Basis has Anita and would rather have Bridget, but Bridget has Approximation, which is "
                 "first on her list, so she stays too. Control would rather have Anita or Bridget, and "
                 "we have just seen that each of them holds her first choice.",
                 flash(self.job_head[1]))
        self.cue("would rather have Bridget", self.job_cell[1][0].animate.set_stroke(ORANGE, 4))
        self.cue("she stays too", flash(self.cand_cell[1][0]), reset(self.job_cell[1][0]))
        self.cue("Control would rather",
                 self.job_cell[2][0].animate.set_stroke(ORANGE, 4),
                 self.job_cell[2][1].animate.set_stroke(ORANGE, 4))
        self.cue("holds her first choice",
                 flash(VGroup(self.cand_cell[0][0], self.cand_cell[1][0])),
                 reset(self.job_cell[2][0]), reset(self.job_cell[2][1]))

        self.say("So every job has been checked and no rogue couple turned up, and a matching with no "
                 "rogue couple is called stable. Notice that Control and Christine are both stuck with "
                 "the last name on their lists. So stable does not mean everyone is happy, only that "
                 "nobody can find a partner who wants to leave with them.",
                 flash(self.job_head))
        self.cue("is called stable", *self.swap("slot_a", slot_text("stable", SLOT_A_Y, GREEN_C)))
        self.cue("Control and Christine", flash(VGroup(self.job_head[2], self.cand_head[2])))
        self.cue("the last name on their lists",
                 flash(VGroup(self.job_cell[2][2], self.cand_cell[2][2])))
        self.cue("wants to leave with them", flash(VGroup(self.s1, self.s2, self.s3)))

        self.say("This is not the matching that propose and reject gave us in the first episode. That "
                 "one paired Approximation with Anita, Basis with Bridget, and Control with Christine. "
                 "There, only Control has names above its partner, and Anita and Bridget each rank "
                 "Control last, so it is stable as well.",
                 flash(self.s1), flash(self.s2))
        self.cue("paired Approximation with Anita",
                 FadeOut(self.s1), FadeOut(self.s2), Create(self.e1), Create(self.e2),
                 reset(self.job_cell[0][1]), reset(self.job_cell[1][1]),
                 reset(self.cand_cell[0][0]), reset(self.cand_cell[1][0]),
                 self.job_cell[0][0].animate.set_stroke(GREEN_C, 4),
                 self.job_cell[1][0].animate.set_stroke(GREEN_C, 4),
                 self.cand_cell[0][1].animate.set_stroke(GREEN_C, 4),
                 self.cand_cell[1][1].animate.set_stroke(GREEN_C, 4))
        self.s1 = self.s2 = None
        self.cue("only Control has names above",
                 self.job_cell[2][0].animate.set_stroke(ORANGE, 4),
                 self.job_cell[2][1].animate.set_stroke(ORANGE, 4))
        self.cue("rank Control last", flash(VGroup(self.cand_cell[0][2], self.cand_cell[1][2])))
        self.cue("stable as well", reset(self.job_cell[2][0]), reset(self.job_cell[2][1]),
                 flash(self.slot_a))

        self.say("So one set of lists can have more than one stable matching. But we found both of them "
                 "by luck and by checking. Does every set of lists have a stable matching at all?")
        self.cue("more than one", flash(self.slot_a))
        self.cue("by luck and by checking", flash(VGroup(self.e1, self.e2, self.s3)))
        self.question = band_text("does one always exist?")     # slot B stays empty
        self.cue("Does every set of lists", FadeIn(self.question))
        self.hold()
