"""CS70 Note 11, episode 09: the output of propose and reject is job optimal.

Built from BOARD-ep09.md: every `> ` line of the board is one say() below, copied
unchanged, and the picture is built as the board's stage lines describe.
"""
import os
import sys
from itertools import permutations, product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---------------------------------------------------------------- FACTS
# The board's "Facts" table. Every list, name and number the episode shows or says is
# computed here and asserted; the picture reads these names, never a typed value.
JOBS = {1: ["Ada", "Bea", "Cleo", "Dora"], 2: ["Ada", "Dora", "Cleo", "Bea"],
        3: ["Ada", "Cleo", "Bea", "Dora"], 4: ["Ada", "Bea", "Cleo", "Dora"]}
CANDS = {"Ada": [1, 3, 2, 4], "Bea": [4, 3, 2, 1], "Cleo": [2, 3, 1, 4], "Dora": [3, 4, 2, 1]}
JOB_IDS = list(JOBS)                     # 1 to 4, left to right on the stage
CAND_NAMES = list(CANDS)                 # Ada, Bea, Cleo, Dora
M1 = {1: "Ada", 2: "Dora", 3: "Cleo", 4: "Bea"}     # F2, the job optimal matching


def run(jobs, cands):
    """F3: propose and reject. Per day: (offers job -> candidate, refused (job, candidate))."""
    left = {j: list(l) for j, l in jobs.items()}
    days = []
    while True:
        offers = {j: left[j][0] for j in jobs}
        refused = []
        for c in cands:
            got = [j for j in offers if offers[j] == c]
            if got:
                best = min(got, key=cands[c].index)
                refused += [(j, c) for j in got if j != best]
        days.append((offers, refused))
        if not refused:
            return days
        for j, c in refused:
            left[j].remove(c)


def stable_matchings(jobs, cands):
    out = []
    for p in permutations(cands):
        m = dict(zip(jobs, p))
        has = {c: j for j, c in m.items()}
        if not any(cands[c].index(j) < cands[c].index(has[c])
                   for j in jobs for c in jobs[j][:jobs[j].index(m[j])]):
            out.append(m)
    return out


def optimal(jobs, cands):
    """F4: the highest-ranked partner of each job over all stable matchings."""
    st = stable_matchings(jobs, cands)
    return {j: min((m[j] for m in st), key=jobs[j].index) for j in jobs}


DAYS = [({1: "Ada", 2: "Ada", 3: "Ada", 4: "Ada"}, [(2, "Ada"), (3, "Ada"), (4, "Ada")]),
        ({1: "Ada", 2: "Dora", 3: "Cleo", 4: "Bea"}, [])]
assert run(JOBS, CANDS) == DAYS                     # F3: the run the episode shows
assert DAYS[-1][0] == M1                            # F3: day two is the matching M1
assert len(DAYS) == 2                               # "Day 1", "Day 2"
OPT = optimal(JOBS, CANDS)
assert OPT == M1                                    # F2: M1 is job optimal
assert len(stable_matchings(JOBS, CANDS)) == 2      # F2: "two stable matchings"
assert (len(JOBS), len(CANDS)) == (4, 4)            # "four jobs", "four candidates"

# the picture: which cell of a list carries the pair of the matching
JOB_GREEN = {j: JOBS[j].index(M1[j]) for j in JOB_IDS}          # {1:0, 2:1, 3:1, 4:1}
HAND_JOB = {c: j for j, c in M1.items()}
CAND_GREEN = {c: CANDS[c].index(HAND_JOB[c]) for c in CAND_NAMES}   # {Ada:0, Bea:0, Cleo:1, Dora:2}
assert JOB_GREEN == {1: 0, 2: 1, 3: 1, 4: 1}                    # the board 1.3: rows 1, 2, 2, 2
assert CAND_GREEN == {"Ada": 0, "Bea": 0, "Cleo": 1, "Dora": 2}  # the board 1.3: rows 1, 1, 2, 3
REFUSED_1 = tuple(DAYS[0][1])
assert REFUSED_1 == ((2, "Ada"), (3, "Ada"), (4, "Ada"))        # beat 1.2: three refusals
assert all(JOBS[j].index(c) == 0 for j, c in REFUSED_1)          # their row 1, faded
assert [M1[j] for j in (2, 3, 4)] == ["Dora", "Cleo", "Bea"]     # the optimal candidates of the
assert all(M1[j] != "Ada" for j in (2, 3, 4))                    #  refused jobs: not Ada
assert all(JOBS[j].index(M1[j]) == 1 for j in (2, 3, 4))         # their green row is row 2
assert [JOBS[j][0] for j in JOB_IDS] == ["Ada"] * len(JOBS)      # "all four jobs ask Ada"
assert CANDS["Ada"][0] == 1                                      # "Ada keeps job one"

# the arrows of the two days, and the offer each one stands for (F3). The four heads on
# Ada's header land 0.6 apart, and the three arrows of day two cross each other at three
# different points, not in one knot (the board's layout).
OFFER_PTS = {"O1": ((-5.1, 0.36), (-5.1, -0.36)), "O2": ((-1.4, 0.36), (-4.5, -0.36)),
             "O3": ((1.4, 0.36), (-3.9, -0.36)), "O4": ((4.2, 0.36), (-3.3, -0.36)),
             "N2": ((-0.6, 0.36), (4.6, -0.36)), "N3": ((0.7, 0.36), (0.7, -0.36)),
             "N4": ((3.6, 0.36), (-2.2, -0.36))}
ARROW_JOB = {"O1": 1, "O2": 2, "O3": 3, "O4": 4, "N2": 2, "N3": 3, "N4": 4}
DAY1_ARROWS, DAY2_ARROWS = ("O1", "O2", "O3", "O4"), ("O1", "N2", "N3", "N4")
assert all(DAYS[0][0][ARROW_JOB[a]] == "Ada" for a in DAY1_ARROWS)     # all four ask Ada
assert [DAYS[1][0][ARROW_JOB[a]] for a in DAY2_ARROWS] == ["Ada", "Dora", "Cleo", "Bea"]
assert len(DAYS[0][1]) == 3 and len(DAYS[1][1]) == 0    # three refused, then nobody


def _crossing(p, q, r, s):
    """Where the segments pq and rs cross, or None when they do not."""
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p, q, r, s
    d = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)
    if abs(d) < 1e-9:
        return None
    t = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / d
    u = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / d
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1)) if 0 <= t <= 1 and 0 <= u <= 1 else None


HEAD_X1 = [OFFER_PTS[a][1][0] for a in DAY1_ARROWS]                    # the four heads on Ada
assert all(round(b - a, 6) == 0.6 for a, b in zip(HEAD_X1, HEAD_X1[1:]))
CROSS2 = [_crossing(OFFER_PTS[a][0], OFFER_PTS[a][1], OFFER_PTS[b][0], OFFER_PTS[b][1])
          for a, b in (("N2", "N3"), ("N2", "N4"), ("N3", "N4"))]
assert all(CROSS2)                                                     # each pair does cross
assert len({(round(x, 3), round(y, 3)) for x, y in CROSS2}) == 3       # at three points, not one

# the picture of scene two: the days, and which of them are red (a picture, not a fact)
DAYS_SHOWN, RED_DAYS = 8, [5, 7]
assert len(RED_DAYS) == 2 and min(RED_DAYS) == 5 and max(RED_DAYS) <= DAYS_SHOWN
FIRST_RED = min(RED_DAYS)
assert FIRST_RED == 5                                   # "first red day", under "day 5"

if __name__ == "__main__":    # F5/F6, the board's full check: 46656 instances, some seconds
    nj, nc = [1, 2, 3], ["x", "y", "z"]
    always_job_optimal = never_refused_by_optimal = True
    for jl in product(permutations(nc), repeat=3):
        for cl in product(permutations(nj), repeat=3):
            jobs = dict(zip(nj, map(list, jl)))
            cands = dict(zip(nc, map(list, cl)))
            days, opt = run(jobs, cands), optimal(jobs, cands)
            always_job_optimal = always_job_optimal and days[-1][0] == opt
            never_refused_by_optimal = never_refused_by_optimal and all(
                opt[j] != c for _, r in days for j, c in r)
    assert always_job_optimal and never_refused_by_optimal
    print("46656 instances: always job optimal, never refused by the optimal candidate")

# ---------------------------------------------------------------- the board's stages
# stage one (scene `run`): the lists of episode 8, and the offers of two days
X1 = [-4.2, -1.4, 1.4, 4.2]              # the four columns
JOB_HEAD_Y1, CAND_HEAD_Y1 = 2.42, -0.65
JOB_Y1 = [1.93, 1.49, 1.05, 0.61]       # a job's four names, its favourite on top
CAND_Y1 = [-1.14, -1.58, -2.02, -2.46]  # a candidate's four jobs, her favourite on top
CELL_W1, CELL_H1 = 2.4, 0.42
HEAD_W1, HEAD_H1 = 2.4, 0.5
PAD = 0.2                                # a word stays this far inside its box
STRIP_X1, STRIP_W1 = -6.15, 1.2          # the strips: jobs / candidates on the left, day right
RS_X1 = 6.15                             # the slot of the day, on the right
SLOT_RS_Y1 = 1.3
GAP_MAX_W = 10.0                         # the widest the guess in the gap may be
ARROW_TIP1, ARROW_W1 = 0.18, 4           # the offer arrows: an absolute tip length, a width

# stage two (scene `suppose`): the days, the red ones, and the two actors of the proof
DAY_N, DAY_Y2, DAY_W2, DAY_H2 = 8, 1.9, 1.3, 0.7
DAY_X2 = [-5.25 + 1.5 * i for i in range(DAY_N)]
RED_EDGE, RED_FILL = 3, 0.25
SQ_SIDE, LEG_SQ_X, LEG_Y2 = 0.35, -5.0, 0.5
LEG_X2, LEG_W2 = -4.6, 11.6              # the legend text, its left edge and its width
CAPTION_Y2, CAPTION_W2 = 2.5, 9.0        # the caption over the day row: what these days are
UNDER_Y2 = 1.25                          # the under-label "first red day", under "day 5"
ACT_X2 = [-4.0, 0.0, 4.0]                # J (the refused job), C* (her), J* (the rival)
ACT_Y2, ACT_W2, ACT_H2 = -0.9, 1.6, 0.6
CAP_Y2 = -1.5                            # the three captions under the actors
REFUSE_PTS = ((-3.2, -0.9), (-0.8, -0.9))
KEEP_PTS = ((3.2, -0.9), (0.8, -0.9))
WORD_X2, WORD_Y2 = -2.0, -0.5            # the labels "refused" and "kept", over the arrows
M1_Y2, M2_Y2 = -2.05, -2.50              # the two lines of the matching M, on two cues
assert ACT_X2[2] > ACT_X2[1] > ACT_X2[0] and len(ACT_X2) == 3

# stage three (scene `rogue`): the two lists, the matching M, the proof lines
X_LIST3, LIST_HEAD_Y3 = -5.2, 2.3
LIST_H3, LIST_CELL_H3 = 0.55, 0.48
CLIST_Y3 = [1.72, 1.20]                  # C* then J in the candidate's list
X_RIVAL3 = -2.4
RLIST_Y3 = [1.72, 1.20, 0.68, 0.16]      # refused J* earlier / C* / optimal for J* / C'
FADED_NAME3 = 0.5                        # names J* crossed off earlier: dim, but still readable
BOXW3, BOXH3 = 1.4, 0.55
BOX_X3, MATCH_X3 = 2.0, 5.2
MTITLE_X3, MTITLE_Y3 = 3.6, 2.4
MROW_Y3 = [1.7, 0.8]
PAIR_X3 = (2.7, 4.5)
ROGUE_PTS3 = ((2.3, 1.1), (4.9, 1.4))    # top edge of the box J* to bottom edge of the box C*
ROGUE_W3, ROGUE_DASH3 = 5, 0.15          # the rogue link: width and dash of the board
PROOF_X3, PROOF_W3 = -6.2, 10.0
# The proof lines are seven rows of the lower half, at size twenty: the longest measures
# 8.83, inside the ten units the board allows. (At a hand-picked size below twenty they
# would not be the board's size; above about ten and a half units pango breaks a line no
# one asked it to break, and the tail lands on the line below.)
PROOF_SIZE3 = 20
PROOF_Y3 = [-0.42, -0.78, -1.14, -1.50, -1.86, -2.22, -2.58]
CAND_LIST_NAMES = ("J*", "J")            # C*'s list: the rival above the job she refused
RIVAL_LIST_NAMES = ("refused J* earlier", "C*", "optimal for J*", "C'")
assert CAND_LIST_NAMES[0] != CAND_LIST_NAMES[1]          # "and C' is not C*"
assert RIVAL_LIST_NAMES[1] == "C*" and RIVAL_LIST_NAMES[3] == "C'"
PROOF_3 = ("C* prefers J* to J: she refused J and kept J*",
           "J* asks C* on the first red day, so every name above C* refused J* earlier",
           "before that day no job was refused by its optimal candidate,",
           "so C* is at or above the optimal candidate of J*",
           "C' is the partner of J* in the stable matching M,",
           "so C' is at or below the optimal candidate of J*, and C' is not C*",
           "so J* prefers C* to C': J* and C* are a rogue couple in M")
assert len(PROOF_3) == len(PROOF_Y3) == 7
assert ROGUE_PTS3[0][1] > MROW_Y3[1] + BOXH3 / 2        # from the top of the box J* ...
assert ROGUE_PTS3[1][1] < MROW_Y3[0] - BOXH3 / 2        # ... to the bottom of the box C*
T_Y3 = [-0.9, -1.65, -2.35]
T_W3 = 10.0                              # the widest a centred result line may be


def fit(t, w):
    """A text no wider than w: a word in a box, a label in a strip, a line of the proof."""
    if t.width > w:
        t.scale_to_fit_width(w)
    return t


def cells(ys, x, w=CELL_W1, h=CELL_H1, color=GREY_B, width=2):
    return VGroup(*[Rectangle(width=w, height=h, stroke_color=color, stroke_width=width)
                    .move_to([x, y, 0]) for y in ys])


def header(text, x, y, color=BLUE_C, w=HEAD_W1, h=HEAD_H1, size=22):
    """A header box, its word kept PAD inside the box."""
    b = box_label(text, color, w=w, h=h, font_size=size).move_to([x, y, 0])
    fit(b[1], w - PAD)
    return b


def word(s, x, y, size=20, color=C_TEXT, w=None):
    """A word in a cell: at most the cell's width minus PAD."""
    return fit(txt(s, size, color), w or (CELL_W1 - PAD)).move_to([x, y, 0])


def arrow(p, q, color=WHITE, width=ARROW_W1):
    """The board's arrow: buff=0 and an absolute tip length. Arrow's own tip is a fraction
    of the length, and on the 0.72-long vertical arrows that fraction leaves a head a third
    of the board's size; the ratios below keep the tip at 0.18 and the stroke at 4."""
    return Arrow([p[0], p[1], 0], [q[0], q[1], 0], buff=0, color=color, stroke_width=width,
                 tip_length=ARROW_TIP1, max_tip_length_to_length_ratio=1.0,
                 max_stroke_width_to_length_ratio=100.0)


# the head of a vertical arrow: its height is the tip length the board asks for, where
# Arrow's own rule would have given a third of it
assert round(arrow((0, 0.36), (0, -0.36)).tip.height, 6) == ARROW_TIP1


def flash(mob):
    return Indicate(mob, color=YELLOW_D, scale_factor=1.1)


def mark(mob, color, width=4):
    return mob.animate.set_stroke(color, width)


def crossed(cell, name):
    """The board's "crossed off": the cell and its name go to opacity 0.25."""
    return cell.animate.set_stroke(opacity=0.25), name.animate.set_opacity(0.25)


def red_day(sq):
    return sq.animate.set_stroke(RED_C, RED_EDGE).set_fill(RED_C, opacity=RED_FILL)


class Ep09JobOptimal(NarratedScene):
    """Episode 09: no job is ever refused by its optimal candidate, so the jobs win."""

    SCENES = ["run", "suppose", "rogue"]

    def construct(self):
        if self.preview_only(self.SCENES):
            return
        self.title_card()
        for name in self.SCENES:
            getattr(self, name)()
        self.end_card([
            "In propose and reject no job is ever refused by its optimal candidate.",
            "If one were, the first such day would produce a rogue couple inside a stable "
            "matching, which is impossible.",
            "So every job ends with its optimal candidate, and the result is the job optimal "
            "matching, which is Theorem 11.2.",
            "The proof is an induction on the days, told through the first counterexample.",
        ])

    # ---- scene 1: run the algorithm on the four-by-four lists
    def run(self):
        self.head1 = head = self.heading("Which one does the algorithm pick?")

        job_head = VGroup(*[header(f"Job {j}", x, JOB_HEAD_Y1) for j, x in zip(JOB_IDS, X1)])
        job_cell = [cells(JOB_Y1, x) for x in X1]
        job_name = [[word(JOBS[j][r], X1[i], JOB_Y1[r]) for r in range(len(JOBS[j]))]
                    for i, j in enumerate(JOB_IDS)]
        cand_head = VGroup(*[header(c, x, CAND_HEAD_Y1, GOLD_C) for c, x in zip(CAND_NAMES, X1)])
        cand_cell = [cells(CAND_Y1, x) for x in X1]
        cand_name = [[word(f"Job {j}", X1[i], CAND_Y1[r]) for r, j in enumerate(CANDS[c])]
                     for i, c in enumerate(CAND_NAMES)]
        strip = VGroup(fit(txt("jobs", 20, GREY_B), STRIP_W1).move_to([STRIP_X1, JOB_HEAD_Y1, 0]),
                       fit(txt("candidates", 20, GREY_B), STRIP_W1).move_to([STRIP_X1, CAND_HEAD_Y1, 0]))
        jobs_block = VGroup(job_head, *job_cell, *[n for ns in job_name for n in ns])
        cands_block = VGroup(cand_head, *cand_cell, *[n for ns in cand_name for n in ns])
        day1 = fit(txt("Day 1", 20, GREY_B), STRIP_W1).move_to([RS_X1, SLOT_RS_Y1, 0])
        day2 = fit(txt("Day 2", 20, GREY_B), STRIP_W1).move_to([RS_X1, SLOT_RS_Y1, 0])
        a = {k: arrow(*OFFER_PTS[k]) for k in OFFER_PTS}

        self.say("Last time four jobs and four candidates had exactly two stable matchings, one "
                 "optimal for the jobs and one optimal for the candidates. So let us run propose "
                 "and reject on these lists and see which one comes out.",
                 LaggedStart(FadeIn(strip), FadeIn(jobs_block, shift=UP * 0.2),
                             FadeIn(cands_block, shift=UP * 0.2), lag_ratio=0.6))
        self.cue("run propose and reject", FadeIn(day1))

        self.say("On the first morning all four jobs ask Ada, because she is at the top of every "
                 "list. Ada keeps job one, her favourite, and refuses the other three, and each of "
                 "them crosses her off.",
                 AnimationGroup(*[flash(job_cell[i][0]) for i in range(len(JOB_IDS))]))
        self.cue("all four jobs ask Ada",
                 LaggedStart(*[Create(a[k]) for k in DAY1_ARROWS], lag_ratio=0.35))
        self.cue("Ada keeps job one", a["O1"].animate.set_color(GREEN_C),
                 mark(job_cell[0][JOB_GREEN[1]], GREEN_C), mark(cand_cell[0][CAND_GREEN["Ada"]], GREEN_C))
        self.cue("refuses the other three",
                 *[a[k].animate.set_color(RED_C) for k in DAY1_ARROWS[1:]])
        self.cue("refuses the other three", *[FadeOut(a[k]) for k in DAY1_ARROWS[1:]])
        self.cue("crosses her off", *[c for j in (2, 3, 4) for c in
                                      crossed(job_cell[j - 1][0], job_name[j - 1][0])])

        green2 = (a["N2"], a["N3"], a["N4"])
        self.say("On the second morning job one asks Ada again, job two asks Dora, job three asks "
                 "Cleo, and job four asks Bea. Every candidate has exactly one offer, so nobody is "
                 "refused and the algorithm stops.",
                 FadeOut(day1), FadeIn(day2), flash(a["O1"]))
        self.cue("job two asks Dora", Create(a["N2"]))
        self.cue("job three asks Cleo", Create(a["N3"]))
        self.cue("job four asks Bea", Create(a["N4"]))
        self.cue("nobody is refused",
                 *[g.animate.set_color(GREEN_C) for g in green2],
                 *[mark(job_cell[j - 1][JOB_GREEN[j]], GREEN_C) for j in (2, 3, 4)],
                 *[mark(cand_cell[CAND_NAMES.index(c)][CAND_GREEN[c]], GREEN_C)
                   for c in ("Dora", "Cleo", "Bea")])

        job_opt = fit(txt("this is the job optimal matching", 24, GREEN_C),
                      GAP_MAX_W).move_to([0, 0, 0])
        self.say("This is the first of our two matchings, the one in which every job has its "
                 "optimal candidate. And look who did the refusing along the way. Jobs two, three "
                 "and four were refused only by Ada, and Ada is not the optimal candidate of any "
                 "of them.",
                 AnimationGroup(*[flash(a[k]) for k in DAY2_ARROWS]))
        self.cue("every job has its optimal candidate",
                 *[FadeOut(a[k]) for k in DAY2_ARROWS], FadeIn(job_opt))
        self.cue("refused only by Ada",
                 AnimationGroup(*[flash(job_cell[j - 1][0]) for j in (2, 3, 4)]))
        self.cue("not the optimal candidate",
                 AnimationGroup(*[flash(job_cell[j - 1][JOB_GREEN[j]]) for j in (2, 3, 4)]))

        guess = fit(txt("guess: no job is ever refused by its optimal candidate", 24, YELLOW_D),
                    GAP_MAX_W).move_to([0, 0, 0])
        self.say("So here is a bold guess for all lists. In propose and reject no job is ever "
                 "refused by its optimal candidate. If that is true, every job ends with its "
                 "optimal candidate, and the result is job optimal.",
                 flash(job_opt))
        self.cue("no job is ever refused", FadeOut(job_opt), FadeIn(guess))
        self.cue("ends with its optimal candidate",
                 AnimationGroup(*[flash(job_cell[i][JOB_GREEN[j]]) for i, j in enumerate(JOB_IDS)]))

        self.say("Why would that be enough? A job only moves past a name that has refused it, so "
                 "it never ends below its optimal candidate. And it cannot end above her, because "
                 "the result is stable, and she is the best partner in any stable matching.",
                 flash(job_head[1]))
        self.cue("moves past a name",
                 LaggedStart(flash(job_cell[1][0]), flash(job_cell[1][1]), lag_ratio=1.0))
        self.cue("never ends below",
                 AnimationGroup(flash(job_cell[1][2]), flash(job_cell[1][3])))
        self.cue("cannot end above her", flash(job_cell[1][0]))
        self.hold()
        self.clear_stage()

    # ---- scene 2: suppose some job is refused by its optimal candidate
    def suppose(self):
        self.head2 = head = self.heading("Suppose it happens")
        self.play(FadeIn(head))

        day_box = VGroup(*[Rectangle(width=DAY_W2, height=DAY_H2, stroke_color=GREY_B, stroke_width=2)
                           .move_to([x, DAY_Y2, 0]) for x in DAY_X2])
        day_lab = [fit(txt(f"day {i + 1}", 20), DAY_W2 - PAD).move_to([DAY_X2[i], DAY_Y2, 0])
                   for i in range(DAY_N)]
        days = [VGroup(day_box[i], day_lab[i]) for i in range(DAY_N)]
        red_i, i_first = [d - 1 for d in RED_DAYS], FIRST_RED - 1
        sq = Rectangle(width=SQ_SIDE, height=SQ_SIDE, stroke_color=RED_C, stroke_width=RED_EDGE,
                       fill_color=RED_C, fill_opacity=RED_FILL).move_to([LEG_SQ_X, LEG_Y2, 0])
        leg_t = fit(txt("a day on which some job is refused by its optimal candidate", 20), LEG_W2)
        leg_t.move_to([LEG_X2 + leg_t.width / 2, LEG_Y2, 0])   # its left edge at x = -4.6
        legend = VGroup(sq, leg_t)
        caption = fit(txt("a supposed run on other lists, not the run we just watched", 22, GREY_A),
                      CAPTION_W2).move_to([0, CAPTION_Y2, 0])
        under = txt("first red day", 22, RED_C).move_to([DAY_X2[i_first], UNDER_Y2, 0])

        self.say("Suppose the guess is wrong for some lists. Then there are days on which some job "
                 "is refused by its optimal candidate, so mark those days red. By the well ordering "
                 "principle there is a first red day, and we look at that day.",
                 Succession(FadeIn(caption, shift=UP * 0.15),
                            LaggedStart(*[FadeIn(d, shift=UP * 0.15) for d in days], lag_ratio=0.25)))
        self.cue("mark those days red", *[red_day(day_box[i]) for i in red_i], FadeIn(legend))
        self.cue("a first red day", flash(day_box[i_first]), FadeIn(under))

        jb = header("J", ACT_X2[0], ACT_Y2, BLUE_C, w=ACT_W2, h=ACT_H2, size=24)
        cb = header("C*", ACT_X2[1], ACT_Y2, GOLD_C, w=ACT_W2, h=ACT_H2, size=24)
        jcb = header("J*", ACT_X2[2], ACT_Y2, BLUE_C, w=ACT_W2, h=ACT_H2, size=24)
        cap = [txt(s, 20, GREY_A).move_to([x, CAP_Y2, 0]) for s, x in
               zip(("the refused job", "its optimal candidate", "the rival"), ACT_X2)]
        refuse, keep = arrow(*REFUSE_PTS, color=RED_C), arrow(*KEEP_PTS, color=GREEN_C)
        r_word = txt("refused", 22, RED_C).move_to([WORD_X2, WORD_Y2, 0])
        k_word = txt("kept", 22, GREEN_C).move_to([-WORD_X2, WORD_Y2, 0])

        self.say("On that day some job is refused by its optimal candidate. She refuses it because "
                 "she keeps an offer she likes more, from another job, which we will call the rival. "
                 "So she ranks the rival above the job she refused.",
                 flash(day_box[i_first]))
        self.cue("refused by its optimal candidate", FadeIn(VGroup(jb, cb), shift=UP * 0.15),
                 FadeIn(cap[0]), FadeIn(cap[1]), Create(refuse), FadeIn(r_word))
        self.cue("call the rival", FadeIn(jcb, shift=UP * 0.15), FadeIn(cap[2]),
                 Create(keep), FadeIn(k_word))
        self.cue("ranks the rival above", LaggedStart(flash(keep), flash(refuse), lag_ratio=1.0))

        m1 = txt("a stable matching M pairs J with C*", 22).move_to([0, M1_Y2, 0])
        m2 = txt("in M, the rival J* has some partner C'", 22).move_to([0, M2_Y2, 0])
        self.say("Now remember what optimal means. She is the best partner the refused job has in "
                 "any stable matching, so there is a stable matching in which these two are together. "
                 "In that matching the rival has some partner too.",
                 flash(cap[1]))
        self.cue("there is a stable matching", FadeIn(m1))
        self.cue("these two are together", AnimationGroup(flash(jb), flash(cb)))
        self.cue("the rival has some partner", FadeIn(m2), flash(jcb))
        self.hold()
        self.clear_stage()

    # ---- scene 3: the rogue couple of the first red day
    def rogue(self):
        self.head3 = head = self.heading("A rogue couple where none can be")
        self.play(FadeIn(head))

        c_head = header("candidate C*", X_LIST3, LIST_HEAD_Y3, GOLD_C, w=CELL_W1, h=LIST_H3)
        c_cell = cells(CLIST_Y3, X_LIST3, h=LIST_CELL_H3)
        c_name = [word(s, X_LIST3, y) for s, y in zip(CAND_LIST_NAMES, CLIST_Y3)]
        r_head = header("job J*", X_RIVAL3, LIST_HEAD_Y3, BLUE_C, w=CELL_W1, h=LIST_H3)
        r_cell = cells(RLIST_Y3, X_RIVAL3, h=LIST_CELL_H3)
        r_name = [word(s, X_RIVAL3, y) for s, y in zip(RIVAL_LIST_NAMES, RLIST_Y3)]
        r_name[0].set_opacity(FADED_NAME3)      # the names J* crossed off earlier: still readable,
                                                # and the border of that cell stays at full strength

        mt = fit(txt("stable matching M", 20), 3.2).move_to([MTITLE_X3, MTITLE_Y3, 0])
        box = [header(s, x, y, col, w=BOXW3, h=BOXH3) for s, x, y, col in
               (("J", BOX_X3, MROW_Y3[0], BLUE_C), ("J*", BOX_X3, MROW_Y3[1], BLUE_C),
                ("C*", MATCH_X3, MROW_Y3[0], GOLD_C), ("C'", MATCH_X3, MROW_Y3[1], GOLD_C))]
        pair = [Line([PAIR_X3[0], y, 0], [PAIR_X3[1], y, 0], color=WHITE, stroke_width=4)
                for y in MROW_Y3]
        rogue = DashedLine([ROGUE_PTS3[0][0], ROGUE_PTS3[0][1], 0],
                           [ROGUE_PTS3[1][0], ROGUE_PTS3[1][1], 0],
                           color=ORANGE, stroke_width=ROGUE_W3, dash_length=ROGUE_DASH3)
        g = [fit(txt(s, PROOF_SIZE3), PROOF_W3) for s in PROOF_3]
        for t, y in zip(g, PROOF_Y3):            # every proof line starts at x = -6.2
            t.move_to([PROOF_X3 + t.width / 2, y, 0])

        self.say("We will show that in this stable matching the candidate and the rival would both "
                 "rather have each other. Her side of this is quick. There she is with the refused "
                 "job, and we just saw that she ranks the rival above it.",
                 FadeIn(VGroup(mt, *box, *pair, c_head, *c_cell, *c_name), shift=UP * 0.2))
        self.cue("Her side of this", flash(c_head))
        self.cue("with the refused job", flash(pair[0]), mark(c_cell[1], GREEN_C))
        self.cue("ranks the rival above", mark(c_cell[0], ORANGE), FadeIn(g[0]))

        self.say("Now the side of the rival. On the first red day the rival is asking her, and a job "
                 "asks the first name it has not crossed off. So every name above her on its list has "
                 "already refused it, on an earlier day.",
                 FadeIn(VGroup(r_head, *r_cell, *r_name), shift=UP * 0.2))
        self.cue("is asking her", mark(r_cell[1], YELLOW_D))
        self.cue("already refused it", flash(r_cell[0]), FadeIn(g[1]))

        self.say("But before the first red day no job was refused by its optimal candidate. So the "
                 "optimal candidate of the rival is not among the names above her. That puts her "
                 "level with the rival's optimal candidate or higher.")
        self.cue("before the first red day",
                 AnimationGroup(FadeIn(g[2]), FadeIn(g[3])))     # G3: its two texts, together
        self.cue("not among the names above her", flash(r_cell[0]))
        self.cue("level with", AnimationGroup(flash(r_cell[1]), flash(r_cell[2])))

        self.say("Now look at the partner the rival has in the stable matching. That partner cannot "
                 "be above its optimal candidate, because optimal means the best partner in any "
                 "stable matching. So our candidate is level with that partner or higher.")
        self.cue("the partner the rival has", flash(pair[1]), flash(box[3]))
        self.cue("cannot be above", AnimationGroup(flash(r_cell[2]), flash(r_cell[3])),
                 FadeIn(g[4]), FadeIn(g[5]))                    # G4: its two texts, together
        self.cue("our candidate is level", AnimationGroup(flash(r_cell[1]), flash(r_cell[3])))

        self.say("And she is not that partner, because in this matching she is with the refused "
                 "job. So the rival ranks her strictly above its partner, and wants to switch.",
                 AnimationGroup(flash(g[4]), flash(g[5])))       # G4
        self.cue("she is with the refused job", flash(pair[0]))
        self.cue("strictly above", mark(r_cell[1], ORANGE), FadeIn(g[6]))

        self.say("So she prefers the rival and the rival prefers her, and they are a rogue couple "
                 "inside a matching we called stable. That is a plain contradiction. So there is no "
                 "first red day, no red day at all, and no job is ever refused by its optimal "
                 "candidate.",
                 AnimationGroup(flash(c_cell[0]), flash(r_cell[1])))
        self.cue("a rogue couple", Create(rogue))
        self.cue("plain contradiction", mt.animate.set_color(RED_C))
        self.cue("plain contradiction", flash(mt))
        self.cue("ever refused", flash(g[6]))                   # G5

        t = [fit(txt(s, size, col), T_W3).move_to([0, y, 0]) for s, size, col, y in
             (("Theorem 11.2: propose and reject produces the job optimal matching", 24, YELLOW_D,
               T_Y3[0]),
              ("as an induction on k: no job is refused by its optimal candidate on day k", 22,
               C_TEXT, T_Y3[1]),
              ("and the candidates?", 22, YELLOW_D, T_Y3[2]))]
        self.say("So every job ends with its optimal candidate, and propose and reject always "
                 "produces the job optimal matching. The proof took the first red day and showed it "
                 "cannot happen, which is induction in its well ordering form. And if the jobs get "
                 "their best, what is left for the candidates?",
                 *[FadeOut(x) for x in g])
        self.cue("job optimal matching", FadeIn(t[0]))
        self.cue("well ordering form", FadeIn(t[1]))
        self.cue("left for the candidates", FadeIn(t[2]))
        self.hold()
