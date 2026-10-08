"""CS70 Note 11, episode 08: the best partner you can keep.

Built from BOARD-ep08.md: every `> ` line of the board is one say() below, copied
unchanged, and the picture is built as the board's stage lines describe.
"""
import os
import sys
from itertools import permutations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---------------------------------------------------------------- FACTS
# The board's "Facts" table. Every list, name and number the episode shows or says is
# computed here and asserted; the picture reads these names, never a typed value.
JOBS = {1: ["Ada", "Bea", "Cleo", "Dora"], 2: ["Ada", "Dora", "Cleo", "Bea"],
        3: ["Ada", "Cleo", "Bea", "Dora"], 4: ["Ada", "Bea", "Cleo", "Dora"]}          # F1
CANDS = {"Ada": [1, 3, 2, 4], "Bea": [4, 3, 2, 1], "Cleo": [2, 3, 1, 4], "Dora": [3, 4, 2, 1]}  # F2
JOB_IDS = list(JOBS)                     # 1 to 4, left to right on the stage
CAND_NAMES = list(CANDS)                 # Ada, Bea, Cleo, Dora
M1 = {1: "Ada", 2: "Dora", 3: "Cleo", 4: "Bea"}     # F3: the first, M, green
M2 = {1: "Ada", 2: "Cleo", 3: "Dora", 4: "Bea"}     # F3: the second, M', purple
PAIRS = [(j, c) for j, c in M1.items()]  # a matching as pairs, for the asserts below


def rogue(m):
    """A pair the matching leaves out and both would prefer to what they have."""
    has = {c: j for j, c in m.items()}
    return [(j, c) for j in JOBS for c in JOBS[j][:JOBS[j].index(m[j])]
            if CANDS[c].index(j) < CANDS[c].index(has[c])]


STABLE = [m for m in (dict(zip(JOBS, p)) for p in permutations(CANDS)) if not rogue(m)]
assert STABLE == [M2, M1] and len(list(permutations(CANDS))) == 24              # F3
assert len(STABLE) == 2                                                          # "two stable matchings"
assert {j for j, _ in PAIRS} == set(JOBS) and {c for _, c in PAIRS} == set(CANDS)

OPT_C = {j: min((m[j] for m in STABLE), key=JOBS[j].index) for j in JOBS}        # F5, F6
OPT_J = {c: min((j for m in STABLE for j in m if m[j] == c), key=CANDS[c].index)
         for c in CANDS}                                                         # F7
PESS_J = {c: max((j for m in STABLE for j in m if m[j] == c), key=CANDS[c].index)
          for c in CANDS}                                                        # F8
PESS_C = {j: max((m[j] for m in STABLE), key=JOBS[j].index) for j in JOBS}       # F8, mirrored
assert OPT_C == M1 and OPT_C[2] == "Dora"                                        # F6, F4
assert OPT_J == {c: j for j, c in M2.items()}                                    # F7
assert PESS_J == {c: j for j, c in M1.items()}                                   # F8
assert PESS_C == M2                                                              # F8, the purple one
# the steps the board added to the notes
assert all(m[1] == "Ada" for m in STABLE)                                        # 2.1, first on both lists
assert all(m[4] == "Bea" for m in STABLE)                                        # 2.3, together in every one
assert all(m[2] != "Ada" for m in STABLE)                                        # 2.2, F4
assert [m[2] for m in STABLE] == ["Cleo", "Dora"]                                # 2.4, two jobs, two ways
assert [m[3] for m in STABLE] == ["Dora", "Cleo"]
assert all(JOBS[j][:JOBS[j].index(M1[j])] == ["Ada"] for j in (2, 3, 4))         # 2.5, only Ada above
assert all(CANDS[c].index(j) == 0 for c, j in {c: j for j, c in M2.items()}.items())   # 2.6, favourite
assert JOBS[1][0] == JOBS[2][0] == JOBS[3][0] == JOBS[4][0] == "Ada"             # 1.2, "every job puts Ada"

# positions used in the narration (1 = first name on the list)
pos = lambda lists, who, x: lists[who].index(x) + 1
assert [pos(JOBS, 2, "Dora"), pos(JOBS, 2, "Cleo")] == [2, 3]                    # 3.1 "the second", "the third"
assert [pos(JOBS, 3, "Cleo"), pos(JOBS, 3, "Dora")] == [2, 4]                    # 3.2, 3.4
assert [pos(CANDS, "Cleo", 3), pos(CANDS, "Cleo", 2)] == [2, 1]                  # 3.3, higher on her list
assert [pos(CANDS, "Dora", 2), pos(CANDS, "Dora", 3)] == [3, 1]                  # 3.3
assert pos(CANDS, "Ada", 1) == 1 and pos(CANDS, "Bea", 4) == 1                   # 1.2, 3.4
assert pos(JOBS, 1, "Ada") == 1 and pos(JOBS, 4, "Bea") == 2                     # 2.1, 2.3
assert (len(JOBS), len(CANDS)) == (4, 4)                                         # "four jobs", "four candidates"

# the picture: which row of a column a name sits on (0 = the top row of that column)
JOB_ROW = {(j, c): JOBS[j].index(c) for j in JOB_IDS for c in JOBS[j]}
CAND_ROW = {(c, j): CANDS[c].index(j) for c in CAND_NAMES for j in CANDS[c]}
assert JOB_ROW[(1, "Ada")] == 0 and JOB_ROW[(4, "Bea")] == 1                     # 2.1, 2.3 yellow
assert JOB_ROW[(2, "Ada")] == 0 and JOB_ROW[(3, "Ada")] == 0 and JOB_ROW[(4, "Ada")] == 0
assert JOB_ROW[(2, "Dora")] == 1 and JOB_ROW[(3, "Cleo")] == 1                   # 2.4 green
assert JOB_ROW[(2, "Cleo")] == 2 and JOB_ROW[(3, "Dora")] == 3                   # 2.6 purple
assert JOB_ROW[(3, "Bea")] == 2 and JOB_ROW[(2, "Bea")] == 3                     # 2.6 "rather have"
assert CAND_ROW[("Ada", 1)] == 0 and CAND_ROW[("Bea", 4)] == 0                   # 2.1, 2.3 yellow
assert CAND_ROW[("Cleo", 3)] == 1 and CAND_ROW[("Dora", 2)] == 2                 # 2.4 green
assert CAND_ROW[("Cleo", 2)] == 0 and CAND_ROW[("Dora", 3)] == 0                 # 2.6 purple
assert JOB_ROW[(3, "Dora")] == 3 and JOB_ROW[(3, "Cleo")] == 1                   # 3.2 the "better off" arrow
assert JOB_ROW[(2, "Dora")] == 1 and OPT_C[2] == "Dora"                          # 3.1 the optimal candidate's cell

# ---------------------------------------------------------------- the board's stage
X = [-4.2, -1.4, 1.4, 4.2]                # the four columns, jobs above, candidates below
JOB_HEAD_Y, CAND_HEAD_Y = 2.42, -0.65
JOB_Y = [1.93, 1.49, 1.05, 0.61]          # a job's four names, its favourite on top
CAND_Y = [-1.14, -1.58, -2.02, -2.46]     # a candidate's four jobs, her favourite on top
CELL_W, CELL_H = 2.4, 0.42
HEAD_W, HEAD_H = 2.4, 0.5
PAD = 0.2                                  # a word stays this far inside its box
STRIP_X, STRIP_W = -6.25, 1.5              # the left strip: 1.5 wide for the longer words, and 0.1
                                           # left of the board's -6.15 so they clear the columns
RS_X, RS_EDGE = 6.15, 6.6                  # the right strip, and the edge its words stay inside
LJ_Y, LC1_Y, LC2_Y, LP_Y, RS_Y = 1.3, -1.4, -1.7, -2.3, -1.4
ASK_X = 5.7                                # "which one?" sits between the two halves: at size 24 it is
ASK_Y = -0.24                              # 1.67 wide, and the clear band right of the Dora column
                                           # (x 5.4 to 6.6, 1.2) cannot hold it
NAME_SIZE, HEAD_SIZE, SLOT_SIZE = 20, 22, 22
STAT_SIZE, ASK_SIZE, LABEL_SIZE = 28, 24, 18   # "stable", "which one?", the strip labels
MARK_W, LINE_W, OPT_W = 4, 6, 7            # a coloured border, a pair line, the optimal cell
GAP_TOP, GAP_BOT = 0.40, -0.40             # between the two halves: lines only, never text
FAINT = 0.35                               # the headers, before the cue that brings them in
LEG_SQ, LEG_SQ_W, LEG_SIZE, LEG_W = 0.4, 4, 22, 1.2   # the legend: a square and a word, three times
LEG_TOP, LEG_STEP, LEG_DY = 1.95, 0.75, 0.39          # 0.75 apart, the word under its square
LEG_ORDER = (("both", YELLOW_D), ("first", GREEN_C), ("second", PURPLE_B))
BETTER_X, BETTER_W, BETTER_TIP = 2.75, 4, 0.18        # the "better off" arrow beside Job 3

# the six pair lines of the board's table: name, colour, from, to, the pair it stands for
PAIR_LINE = {
    "K1": (YELLOW_D, (-4.2, 0.36), (-4.2, -0.36), (1, "Ada")),
    "K4": (YELLOW_D, (4.2, 0.36), (-1.0, -0.36), (4, "Bea")),
    "A2": (GREEN_C, (-1.4, 0.36), (4.6, -0.36), (2, "Dora")),
    "A3": (GREEN_C, (1.0, 0.36), (1.0, -0.36), (3, "Cleo")),
    "B2": (PURPLE_B, (-1.4, 0.36), (1.8, -0.36), (2, "Cleo")),
    "B3": (PURPLE_B, (1.8, 0.36), (4.6, -0.36), (3, "Dora")),
}
assert all(GAP_BOT < y < GAP_TOP for _, p, q, _ in PAIR_LINE.values()
           for y in (p[1], q[1]))          # every line stays in the gap
assert all(M1[j] == c for n, (_, _, _, (j, c)) in PAIR_LINE.items() if n in ("K1", "K4", "A2", "A3"))
assert all(M2[j] == c for n, (_, _, _, (j, c)) in PAIR_LINE.items() if n in ("B2", "B3"))
assert {n for n, (_, _, _, (j, c)) in PAIR_LINE.items() if M1[j] == M2[j]} == {"K1", "K4"}
assert {j for _, _, _, (j, _) in PAIR_LINE.values()} == set(JOB_IDS)


def fit(t, w):
    """A text no wider than w: a word in a box, a label in a strip."""
    if t.width > w:
        t.scale_to_fit_width(w)
    return t


def cells(ys, x, w=CELL_W, h=CELL_H, color=GREY_B, width=2):
    return VGroup(*[Rectangle(width=w, height=h, stroke_color=color, stroke_width=width)
                    .move_to([x, y, 0]) for y in ys])


def header(text, x, y, color=BLUE_C):
    """A header box, its word kept PAD inside the box."""
    b = box_label(text, color, w=HEAD_W, h=HEAD_H, font_size=HEAD_SIZE).move_to([x, y, 0])
    fit(b[1], HEAD_W - PAD)
    return b


def word(s, x, y):
    """A name in a cell: at most the cell's width minus PAD."""
    return fit(txt(s, NAME_SIZE), CELL_W - PAD).move_to([x, y, 0])


def slot(text, x, y, color, size=SLOT_SIZE):
    """A text in a strip slot: at most the strip's width."""
    return fit(txt(text, size, color), STRIP_W).move_to([x, y, 0])


def rs_slot(text, size, color, x=RS_X, y=RS_Y):
    """A word in slot RS at the size asked for: its right edge inside RS_EDGE."""
    t = txt(text, size, color)
    return t.move_to([min(x, RS_EDGE - t.width / 2), y, 0])


def better_arrow():
    """Job 3's row 4 up to its row 2: on a job's list, better off is higher up."""
    return Arrow([BETTER_X, JOB_Y[3], 0], [BETTER_X, JOB_Y[1], 0], color=GREEN_C,
                 stroke_width=BETTER_W, tip_length=BETTER_TIP, buff=0)


def pair_line(name):
    color, p, q, _ = PAIR_LINE[name]
    return Line([p[0], p[1], 0], [q[0], q[1], 0], color=color, stroke_width=LINE_W,
                stroke_opacity=1.0)


def flash(mob, scale=1.1):
    return Indicate(mob, color=YELLOW_D, scale_factor=scale)


def mark(mob, color, width=MARK_W):
    return mob.animate.set_stroke(color, width)


def crossed(cell, name):
    """A cell a job can no longer hope for: the cell and its name fade back."""
    return cell.animate.set_stroke(opacity=0.25), name.animate.set_opacity(0.25)


class Ep08OptimalPartners(NarratedScene):
    """Episode 08: two stable matchings, and the best and worst partner in each."""

    SCENES = ["hook", "find", "best"]

    def construct(self):
        if self.preview_only(self.SCENES):
            return
        self.title_card()
        for name in self.SCENES:
            getattr(self, name)()
        self.end_card([
            "The optimal candidate of a job is the best partner it has in any stable matching, "
            "which need not be the top of its list.",
            "A stable matching that gives every job its optimal candidate is job optimal, and one "
            "that gives every candidate her optimal job is candidate optimal.",
            "Pessimal means the worst partner in any stable matching.",
            "Here there are exactly two stable matchings: one is job optimal and candidate "
            "pessimal, the other is candidate optimal.",
        ])

    # ---- scene 1: the four-by-four lists of the board, on one stage
    def hook(self):
        head = self.heading("Four jobs, four candidates")
        job_head = VGroup(*[header(f"Job {j}", x, JOB_HEAD_Y) for j, x in zip(JOB_IDS, X)])
        cand_head = VGroup(*[header(c, x, CAND_HEAD_Y, GOLD_C) for c, x in zip(CAND_NAMES, X)])
        job_cell = [cells(JOB_Y, x) for x in X]
        job_name = [[word(JOBS[j][r], X[i], JOB_Y[r]) for r in range(len(JOBS[j]))]
                    for i, j in enumerate(JOB_IDS)]
        cand_cell = [cells(CAND_Y, x) for x in X]
        cand_name = [[word(f"Job {j}", X[i], CAND_Y[r]) for r, j in enumerate(CANDS[c])]
                     for i, c in enumerate(CAND_NAMES)]
        strip = VGroup(slot("jobs", STRIP_X, JOB_HEAD_Y, GREY_B, LABEL_SIZE),
                       slot("candidates", STRIP_X, CAND_HEAD_Y, GREY_B, LABEL_SIZE))
        cols = [VGroup(job_cell[i], *job_name[i]) for i in range(len(X))]
        cols += [VGroup(cand_cell[i], *cand_name[i]) for i in range(len(X))]
        for h in (*job_head, *cand_head):   # on stage from the first word, faint, until their cue
            h.set_opacity(0)
        self.add(job_head, cand_head)

        self.say("In episode three one set of lists had two stable matchings, so stable alone does "
                 "not pick a winner. To see what separates them, here is a slightly bigger example. "
                 "There are four jobs, numbered one to four, and four candidates, Ada, Bea, Cleo "
                 "and Dora.",
                 FadeIn(head), LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in strip], lag_ratio=0.6),
                 LaggedStart(*[h.animate.set_opacity(FAINT) for h in job_head], lag_ratio=0.35),
                 LaggedStart(*[h.animate.set_opacity(FAINT) for h in cand_head], lag_ratio=0.35))
        self.cue("four jobs", LaggedStart(*[h.animate.set_opacity(1) for h in job_head], lag_ratio=0.35))
        self.cue("four candidates",
                 LaggedStart(*[h.animate.set_opacity(1) for h in cand_head], lag_ratio=0.35))

        self.say("Each column shows a list, most wanted first as always. Notice that every job puts "
                 "Ada at the top, and that the favourite of Ada is job one.",
                 LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cols], lag_ratio=0.25))
        self.cue("every job puts Ada",
                 AnimationGroup(*[flash(job_cell[i][JOB_ROW[(j, "Ada")]]) for i, j in enumerate(JOB_IDS)]))
        self.cue("is job one", flash(cand_cell[0][CAND_ROW[("Ada", 1)]]))

        self.head_hook = head
        self.job_head, self.cand_head = job_head, cand_head
        self.job_cell, self.job_name = job_cell, job_name
        self.cand_cell, self.cand_name = cand_cell, cand_name
        self.hold()

    # ---- scene 2: which of the twenty-four matchings are stable
    def find(self):
        head = self.heading("Which matchings are stable?")
        job_head, cand_head = self.job_head, self.cand_head
        job_cell, job_name = self.job_cell, self.job_name
        cand_cell, cand_name = self.cand_cell, self.cand_name
        # K4 is created and drawn before the green and the purple lines, so it lies under them where
        # the three of them cross (2.3 before 2.4 and 2.6)
        k1, k4 = pair_line("K1"), pair_line("K4")
        a2, a3 = pair_line("A2"), pair_line("A3")
        b2, b3 = pair_line("B2"), pair_line("B3")
        rs1 = rs_slot("stable", STAT_SIZE, GREEN_C)
        rs2 = rs_slot("stable", STAT_SIZE, PURPLE_B)
        legend = VGroup(*[
            VGroup(Rectangle(width=LEG_SQ, height=LEG_SQ, stroke_color=col, stroke_width=LEG_SQ_W)
                   .move_to([RS_X, LEG_TOP - i * LEG_STEP, 0]),
                   fit(txt(w, LEG_SIZE, col), LEG_W)
                   .move_to([RS_X, LEG_TOP - i * LEG_STEP - LEG_DY, 0]))
            for i, (w, col) in enumerate(LEG_ORDER)])
        self.legend = legend

        self.say("Let us hunt for the stable matchings, starting with job one and Ada, who are first "
                 "on each other's lists. If they were not together, each would prefer the other to "
                 "its partner, and they would be a rogue couple. So every stable matching pairs job "
                 "one with Ada.",
                 FadeOut(self.head_hook), FadeIn(head), flash(job_head[0]), flash(cand_head[0]))
        self.cue("first on", mark(job_cell[0][JOB_ROW[(1, "Ada")]], YELLOW_D),
                 mark(cand_cell[0][CAND_ROW[("Ada", 1)]], YELLOW_D))
        self.cue("a rogue couple", flash(job_cell[0][JOB_ROW[(1, "Ada")]]),
                 flash(cand_cell[0][CAND_ROW[("Ada", 1)]]))
        self.cue("every stable matching", Create(k1))

        self.say("That already tells us something about job two. Its first choice is Ada as well, "
                 "but in a stable matching Ada is always taken by job one. So the top of a list is "
                 "not always a realistic hope.",
                 flash(job_head[1]))
        self.cue("Its first choice is Ada", flash(job_cell[1][JOB_ROW[(2, "Ada")]]))
        self.cue("always taken",
                 *[a for i in (1, 2, 3) for a in crossed(job_cell[i][JOB_ROW[(i + 1, "Ada")]],
                                                         job_name[i][JOB_ROW[(i + 1, "Ada")]])])
        self.cue("realistic hope", flash(job_head[1]))

        self.say("With Ada out of reach, look at job four. Its next name is Bea, and the favourite "
                 "of Bea is job four. Apart, job four would have someone below Bea, and Bea would "
                 "have a job below her favourite. So job four and Bea are together in every stable "
                 "matching as well.",
                 flash(job_head[3]))
        self.cue("Its next name is Bea", mark(job_cell[3][JOB_ROW[(4, "Bea")]], YELLOW_D),
                 mark(cand_cell[1][CAND_ROW[("Bea", 4)]], YELLOW_D))
        self.cue("someone below Bea", flash(job_cell[3][JOB_ROW[(4, "Cleo")]]),
                 flash(job_cell[3][JOB_ROW[(4, "Dora")]]))
        self.cue("below her favourite",
                 AnimationGroup(*[flash(cand_cell[1][CAND_ROW[("Bea", j)]]) for j in (3, 2, 1)]))
        self.cue("are together", Create(k4))

        self.say("That leaves jobs two and three with Cleo and Dora, and they can be paired in only "
                 "two ways. Either job two takes Dora and job three takes Cleo, or the other way "
                 "round.",
                 AnimationGroup(flash(job_head[1]), flash(job_head[2]),
                                flash(cand_head[2]), flash(cand_head[3])))
        self.cue("job two takes Dora", Create(a2), Create(a3),
                 mark(job_cell[1][JOB_ROW[(2, "Dora")]], GREEN_C),
                 mark(job_cell[2][JOB_ROW[(3, "Cleo")]], GREEN_C),
                 mark(cand_cell[2][CAND_ROW[("Cleo", 3)]], GREEN_C),
                 mark(cand_cell[3][CAND_ROW[("Dora", 2)]], GREEN_C))
        self.cue("the other way round", flash(cand_head[2]), flash(cand_head[3]))

        self.say("Is the first way stable? Jobs two, three and four each have the second name on "
                 "their lists, and the only name above it is Ada. Ada has her favourite and will "
                 "not move, so there is no rogue couple.",
                 flash(a2), flash(a3))
        self.cue("the second name on their lists",
                 AnimationGroup(*[flash(job_cell[i][JOB_ROW[(j, M1[j])]])
                                  for i, j in zip((1, 2, 3), (2, 3, 4))]))
        self.cue("the only name above it",
                 AnimationGroup(*[flash(job_cell[i][JOB_ROW[(j, "Ada")]])
                                  for i, j in zip((1, 2, 3), (2, 3, 4))]))
        self.cue("no rogue couple", FadeIn(rs1))
        self.cue("no rogue couple", flash(rs1))

        self.say("Now the other way round, where job two has Cleo and job three has Dora. Job two "
                 "would rather have Dora, and job three would rather have Cleo or Bea. But Dora, "
                 "Cleo and Bea each have their favourite job here, so none of them would move. "
                 "Both matchings are stable, and they are the only ones.",
                 FadeOut(a2), FadeOut(a3), FadeOut(rs1))
        self.cue("job two has Cleo", Create(b2), Create(b3),
                 mark(job_cell[1][JOB_ROW[(2, "Cleo")]], PURPLE_B),
                 mark(job_cell[2][JOB_ROW[(3, "Dora")]], PURPLE_B),
                 mark(cand_cell[2][CAND_ROW[("Cleo", 2)]], PURPLE_B),
                 mark(cand_cell[3][CAND_ROW[("Dora", 3)]], PURPLE_B))
        self.cue("would rather have Dora", flash(job_cell[1][JOB_ROW[(2, "Dora")]]))
        self.cue("would rather have Dora", flash(job_cell[2][JOB_ROW[(3, "Cleo")]]),
                 flash(job_cell[2][JOB_ROW[(3, "Bea")]]))
        self.cue("their favourite job",
                 AnimationGroup(*[flash(cand_cell[CAND_NAMES.index(c)][0])
                                  for c in ("Dora", "Cleo", "Bea")]))
        self.cue("the only ones", FadeIn(rs2),
                 LaggedStart(*[FadeIn(m, shift=LEFT * 0.2) for m in legend], lag_ratio=0.25))
        self.cue("the only ones", flash(rs2))

        self.hold()
        self.head_find = head
        self.play(*[FadeOut(m) for m in (k1, k4, b2, b3, rs2)])

    # ---- scene 3: best for the jobs, best for the candidates, and the worst
    def best(self):
        head = self.heading("Best for whom?")
        job_head, cand_head = self.job_head, self.cand_head
        job_cell, cand_cell = self.job_cell, self.cand_cell
        legend = self.legend
        lj, lj2 = (slot("optimal", STRIP_X, LJ_Y, GREEN_C), slot("job optimal", STRIP_X, LJ_Y, GREEN_C))
        lc1 = slot("candidate", STRIP_X, LC1_Y, PURPLE_B)
        lc2 = slot("optimal", STRIP_X, LC2_Y, PURPLE_B)
        lp = slot("pessimal", STRIP_X, LP_Y, GREEN_C)
        rs = rs_slot("which one?", ASK_SIZE, YELLOW_D, x=ASK_X, y=ASK_Y)
        arrow = better_arrow()

        self.say("Now compare the two through the eyes of job two. In the first matching it has "
                 "Dora, the second name on its list, and in the second matching it has Cleo, the "
                 "third. Dora is the best partner job two has in any stable matching, and we call "
                 "her its optimal candidate.",
                 FadeOut(self.head_find), FadeIn(head), flash(job_head[1]))
        self.cue("it has Dora", flash(job_cell[1][JOB_ROW[(2, "Dora")]]))
        self.cue("it has Cleo", flash(job_cell[1][JOB_ROW[(2, "Cleo")]]))
        self.cue("optimal", mark(job_cell[1][JOB_ROW[(2, "Dora")]], GREEN_C, OPT_W), FadeIn(lj))
        self.cue("optimal", flash(job_cell[1][JOB_ROW[(2, "Dora")]], 1.15))

        self.say("Do the same for the other jobs. Job one has Ada and job four has Bea in both, and "
                 "job three is better off with Cleo than with Dora. So the first matching gives "
                 "every job its optimal candidate at once, and such a matching is called job "
                 "optimal.")
        self.cue("Job one has Ada", flash(job_cell[0][JOB_ROW[(1, "Ada")]]),
                 flash(job_cell[3][JOB_ROW[(4, "Bea")]]))
        self.cue("better off with Cleo", flash(job_cell[2][JOB_ROW[(3, "Cleo")]]))
        self.cue("better off with Cleo", flash(job_cell[2][JOB_ROW[(3, "Dora")]]))
        self.cue("better off with Cleo", Create(arrow))
        self.cue("called job optimal", Transform(lj, lj2))

        self.say("Now take the side of the candidates. Cleo has job three in the first matching and "
                 "job two in the second, and job two is higher on her list. Dora has job two in the "
                 "first and job three in the second, and job three is higher on hers.",
                 FadeOut(arrow), AnimationGroup(*[flash(h) for h in cand_head]))
        self.cue("Cleo has job three", flash(cand_cell[2][CAND_ROW[("Cleo", 3)]]))
        self.cue("Cleo has job three", flash(cand_cell[2][CAND_ROW[("Cleo", 2)]]))
        self.cue("Dora has job two", flash(cand_cell[3][CAND_ROW[("Dora", 2)]]))
        self.cue("Dora has job two", flash(cand_cell[3][CAND_ROW[("Dora", 3)]]))

        self.say("So the second matching gives every candidate her best stable job, and it is called "
                 "candidate optimal. And the first matching gives Cleo and Dora the lowest job they "
                 "have in any stable matching. The word for that is pessimal.",
                 AnimationGroup(*[flash(cand_cell[i][0]) for i in range(len(CAND_NAMES))]))
        self.cue("candidate optimal", FadeIn(lc1), FadeIn(lc2))
        self.cue("the lowest job", flash(cand_cell[2][CAND_ROW[("Cleo", 3)]]),
                 flash(cand_cell[3][CAND_ROW[("Dora", 2)]]))
        self.cue("pessimal", FadeIn(lp), flash(cand_cell[2][CAND_ROW[("Cleo", 3)]]),
                 flash(cand_cell[3][CAND_ROW[("Dora", 2)]]))

        self.say("So here the matching that is optimal for the jobs is pessimal for the candidates. "
                 "Is that an accident of these lists, or a law? Can every job always get its optimal "
                 "candidate at once? And which of the two does propose and reject produce?")
        self.cue("optimal for the jobs", flash(lj))
        self.cue("pessimal for the candidates", flash(lp))
        self.cue("propose and reject", FadeIn(rs), flash(legend[1]), flash(legend[2]))
        self.hold()
