"""CS70 Note 11, episode 10: a job optimal matching is candidate pessimal.

Built from BOARD-ep10.md: every `> ` line of the board is one say() below, copied
unchanged, and the picture is built as the board's stage lines describe.
"""
import os
import sys
from itertools import permutations, product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---------------------------------------------------------------- FACTS
# The board's "Facts" table, F1 to F10. Every list, name and number the episode shows
# or says is computed here and asserted; the picture reads these names, never a typed value.
JOBS = {1: ["Ada", "Bea", "Cleo", "Dora"], 2: ["Ada", "Dora", "Cleo", "Bea"],
        3: ["Ada", "Cleo", "Bea", "Dora"], 4: ["Ada", "Bea", "Cleo", "Dora"]}
CANDS = {"Ada": [1, 3, 2, 4], "Bea": [4, 3, 2, 1], "Cleo": [2, 3, 1, 4], "Dora": [3, 4, 2, 1]}
JOB_IDS = list(JOBS)                     # 1 to 4, left to right on the stage
CAND_NAMES = list(CANDS)                 # Ada, Bea, Cleo, Dora
M1 = {1: "Ada", 2: "Dora", 3: "Cleo", 4: "Bea"}     # F2, green: the job optimal matching
M2 = {1: "Ada", 2: "Cleo", 3: "Dora", 4: "Bea"}     # F2, purple: the other stable matching


def run(proposers, answerers):
    """F8: propose and reject. Per day: offers proposer -> answerer; the last day is the result."""
    left = {p: list(l) for p, l in proposers.items()}
    days = []
    while True:
        offers = {p: left[p][0] for p in proposers}
        refused = []
        for a in answerers:
            got = [p for p in offers if offers[p] == a]
            if got:
                best = min(got, key=answerers[a].index)
                refused += [(p, a) for p in got if p != best]
        days.append(offers)
        if not refused:
            return days
        for p, a in refused:
            left[p].remove(a)


def stable_matchings(jobs, cands):
    """F2: every matching in which no pair would rather have each other."""
    out = []
    for p in permutations(cands):
        m = dict(zip(jobs, p))
        has = {c: j for j, c in m.items()}
        if not any(cands[c].index(j) < cands[c].index(has[c])
                   for j in jobs for c in jobs[j][:jobs[j].index(m[j])]):
            out.append(m)
    return out


STABLE = stable_matchings(JOBS, CANDS)
assert STABLE == [M2, M1] and run(JOBS, CANDS)[-1] == M1        # F2
assert len(STABLE) == 2                                          # "the only other stable matching"
PESS = {c: max((j for m in STABLE for j in m if m[j] == c), key=CANDS[c].index) for c in CANDS}
assert PESS == {c: j for j, c in M1.items()}                     # F4: the green matching is candidate pessimal
assert CANDS["Cleo"] == [2, 3, 1, 4] and M1[3] == "Cleo"         # F7
assert JOBS[3] == ["Ada", "Cleo", "Bea", "Dora"]                 # F7: Cleo is Job 3's optimal candidate
SWAP = run(CANDS, JOBS)
assert len(SWAP) == 1                                            # F8: "it stops on the first day"
assert SWAP[0] == {"Ada": 1, "Bea": 4, "Cleo": 2, "Dora": 3}     # F8: what each candidate asks
assert SWAP[0] == {c: j for j, c in M2.items()}                  # F8: the result is the purple matching
MATCH_YEAR, PAPER_YEAR = 1952, 1962                              # F9, F10
NINETIES = "1990s"                                               # F9: "in the nineteen nineties"
assert (MATCH_YEAR, PAPER_YEAR) == (1952, 1962)                  # "nineteen fifty-two", "nineteen sixty-two"
assert PAPER_YEAR - MATCH_YEAR == 10                             # F10: "in use for ten years"
assert MATCH_YEAR < PAPER_YEAR < int(NINETIES[:4])               # the paper comes before the reversal

# the picture: which row of a list carries a pair of a matching
HAND_GREEN = {c: j for j, c in M1.items()}
HAND_PURPLE = {c: j for j, c in M2.items()}
JOB_GREEN = {j: JOBS[j].index(M1[j]) for j in JOB_IDS}          # 0, 1, 1, 1
JOB_PURPLE = {j: JOBS[j].index(M2[j]) for j in JOB_IDS}         # 0, 2, 3, 1
CAND_GREEN = {c: CANDS[c].index(HAND_GREEN[c]) for c in CAND_NAMES}     # 0, 0, 1, 2
CAND_PURPLE = {c: CANDS[c].index(HAND_PURPLE[c]) for c in CAND_NAMES}   # 0, 0, 0, 0
BOTH_JOB = [j for j in JOB_IDS if JOB_GREEN[j] == JOB_PURPLE[j]]        # the yellow job cells
BOTH_CAND = [c for c in CAND_NAMES if CAND_GREEN[c] == CAND_PURPLE[c]]  # the yellow candidate cells
assert JOB_GREEN == {1: 0, 2: 1, 3: 1, 4: 1}                    # the board: Job 2 and 3, row 2
assert JOB_PURPLE == {1: 0, 2: 2, 3: 3, 4: 1}                   # the board: Job 2 row 3, Job 3 row 4
assert CAND_GREEN == {"Ada": 0, "Bea": 0, "Cleo": 1, "Dora": 2}  # the board: Cleo row 2, Dora row 3
assert all(CAND_PURPLE[c] == 0 for c in CAND_NAMES)             # the board: Cleo and Dora row 1
assert BOTH_JOB == [1, 4] and BOTH_CAND == ["Ada", "Bea"]       # the four yellow cells of beat 1.1
assert all(CAND_GREEN[c] > CAND_PURPLE[c] for c in ("Cleo", "Dora"))   # beat 1.2: green below purple
assert all(CAND_GREEN[c] == CAND_PURPLE[c] for c in ("Ada", "Bea"))    # beat 1.3: the same job in both
assert HAND_GREEN["Cleo"] == 3                                  # F7: "her green job is job three"
BELOW_CLEO = [r for r in range(len(CANDS["Cleo"])) if r > CAND_GREEN["Cleo"]]
assert BELOW_CLEO == [2, 3]                                     # beat 2.1: her rows three and four
assert [CANDS["Cleo"][r] for r in BELOW_CLEO] == [1, 4]         # beat 2.1: "job one or job four"
assert JOBS[3][0] == "Ada" and JOBS[3][JOB_GREEN[3]] == "Cleo"  # beats 2.2 and 2.3
assert JOBS[3][2:] == ["Bea", "Dora"]                           # beat 2.3: "below Cleo"
BELOW_CAND = {c: [r for r in range(len(CANDS[c])) if r > CAND_GREEN[c]] for c in CAND_NAMES}
assert BELOW_CAND == {"Ada": [1, 2, 3], "Bea": [1, 2, 3], "Cleo": [2, 3], "Dora": [3]}   # beat 3.1
BELOW_JOB = {j: [r for r in range(len(JOBS[j])) if r > JOB_GREEN[j]] for j in JOB_IDS}   # beat 2.3, 3.1
assert BELOW_JOB[3] == [2, 3] and [JOBS[3][r] for r in BELOW_JOB[3]] == ["Bea", "Dora"]
GREEN_CANDS, GREEN_JOBS = ("Cleo", "Dora"), (2, 3)              # the four green cells of beat 1.1
assert [CAND_GREEN[c] for c in GREEN_CANDS] == [1, 2] and [JOB_GREEN[j] for j in GREEN_JOBS] == [1, 1]

if __name__ == "__main__":   # F4, the board's full check: 46656 instances, some seconds
    nj, nc = [1, 2, 3], ["x", "y", "z"]
    optimal_is_pessimal = True
    for jl in product(permutations(nc), repeat=3):
        for cl in product(permutations(nj), repeat=3):
            jobs, cands = dict(zip(nj, map(list, jl))), dict(zip(nc, map(list, cl)))
            st, out = stable_matchings(jobs, cands), run(jobs, cands)[-1]
            pess = {c: max((j for m in st for j in m if m[j] == c), key=cands[c].index) for c in cands}
            optimal_is_pessimal = optimal_is_pessimal and pess == {c: j for j, c in out.items()}
    assert optimal_is_pessimal
    print("46656 instances with three jobs and three candidates: optimal is always pessimal")

# ---------------------------------------------------------------- the board's stage
# one stage, built in `hook` and kept to the end: the lists of episode 8, the two stable
# matchings marked by colour, a legend on the right, two slots in each strip, the gap.
X = [-4.2, -1.4, 1.4, 4.2]               # the four columns
JOB_HEAD_Y, CAND_HEAD_Y = 2.42, -0.65    # jobs above the gap, candidates below it
JOB_Y = [1.93, 1.49, 1.05, 0.61]         # a job's four names, its favourite on top
CAND_Y = [-1.14, -1.58, -2.02, -2.46]    # a candidate's four jobs, her favourite on top
CELL_W, CELL_H = 2.4, 0.42
HEAD_W, HEAD_H = 2.4, 0.5
PAD = 0.2                                # a word stays this far inside its box
STRIP_X, STRIP_W = -6.15, 1.2            # the strips: jobs / candidates left, legend right
RS_X = 6.15
SLOT_LJ_Y, SLOT_LC1_Y, SLOT_LC2_Y, SLOT_LP_Y, SLOT_RS_Y = 1.3, -1.4, -1.7, -2.3, -1.4
SQ, LEG_Y = 0.28, [1.95, 1.30, 0.65]     # the three legend squares, and their words below them
GAP_W, GAP_Y = 10.0, 0.0                 # the one text the gap holds, at most this wide
EDGE_Y = 0.36                            # where the gap meets the pictures, up and down
GAP_TOP = 0.40                           # the top of the gap: an ask ends here, short of the names
BORDER, THIN = 4, 2                      # a coloured border, and a plain one
CELL_MARK = 6                            # the width the two cells the word "pessimal" names keep
HEAD_BORDER = 3                          # box_label's own border, put back when the rogue line goes
RS_W = 0.9                               # a right-strip text this wide stays inside x = 6.6
DASH_LEN, DASH_W = 0.15, 6               # the rogue line's dashes, and a width that shows at 480p
ARROW_W = 4
D_PTS = [((x, EDGE_Y), (x, -EDGE_Y)) for x in X]         # the four offers, jobs proposing
P_PTS = [((x, -EDGE_Y), (x, EDGE_Y)) for x in X]         # the four offers, candidates proposing
U_PTS = [((-4.2, -EDGE_Y), (-4.2, GAP_TOP - 0.15)),             # Ada asks job one
         ((-1.4, -EDGE_Y), (4.2, GAP_TOP - 0.15)),              # Bea asks job four
         ((1.4, -EDGE_Y), (-1.4, GAP_TOP - 0.15)),              # Cleo asks job two
         ((4.2, -EDGE_Y), (1.4, GAP_TOP - 0.15))]               # Dora asks job three
U_NAMES = ["Ada", "Bea", "Cleo", "Dora"]
U_JOBS = [JOB_IDS[X.index(p[1][0])] for p in U_PTS]      # the job each ask points at: 1, 4, 2, 3
R_PTS = ((1.4, EDGE_Y), (1.4, -EDGE_Y))                  # the rogue line, Job 3 to Cleo
assert [U_PTS[i][1][0] for i in range(4)] == [X[0], X[3], X[1], X[2]]
assert [SWAP[0][c] for c in U_NAMES] == [1, 4, 2, 3]     # the arrow under a name is her first job
assert U_JOBS == [SWAP[0][c] for c in U_NAMES] == [1, 4, 2, 3]   # and it ends at that job's column
assert abs(GAP_TOP - (JOB_Y[3] - CELL_H / 2)) < 1e-9     # an ask ends at the bottom edge of row four,
assert GAP_TOP < JOB_Y[3] - 0.1                          # so its tip stops short of the name there


def fit(t, w):
    """A text no wider than w: a word in a box, a label in a strip, a line in the gap."""
    if t.width > w:
        t.scale_to_fit_width(w)
    return t


def cells(ys, x, w=CELL_W, h=CELL_H, color=GREY_B, width=THIN):
    return VGroup(*[Rectangle(width=w, height=h, stroke_color=color, stroke_width=width)
                    .move_to([x, y, 0]) for y in ys])


def header(text, x, y, color=BLUE_C, w=HEAD_W, h=HEAD_H, size=22):
    """A header box, its word kept PAD inside the box."""
    b = box_label(text, color, w=w, h=h, font_size=size).move_to([x, y, 0])
    fit(b[1], w - PAD)
    return b


def word(s, x, y, size=20, color=C_TEXT):
    """A word in a cell: at most the cell's width minus PAD."""
    return fit(txt(s, size, color), CELL_W - PAD).move_to([x, y, 0])


def arrow(p, q, color=WHITE, width=ARROW_W):
    return Arrow([p[0], p[1], 0], [q[0], q[1], 0], buff=0, color=color, stroke_width=width,
                 max_tip_length_to_length_ratio=0.5, tip_length=0.18)


def flash(mob):
    return Indicate(mob, color=YELLOW_D, scale_factor=1.1)


def mark(mob, color, width=BORDER):
    return mob.animate.set_stroke(color, width)


def rogue_line():
    """R of the board's arrow table: the dashed orange line in the gap, Job 3 and Cleo.
    Drawn at a width and a dash length that read as a line at 480p, not as a stub."""
    return DashedLine([R_PTS[0][0], R_PTS[0][1], 0], [R_PTS[1][0], R_PTS[1][1], 0],
                      color=ORANGE, stroke_width=DASH_W, dash_length=DASH_LEN)


class Ep10CandidatePessimal(NarratedScene):
    """Episode 10: the side that proposes wins, so the other side loses."""

    SCENES = ["hook", "cleo", "law", "swap"]

    def construct(self):
        if self.preview_only(self.SCENES):
            return
        self.title_card()
        for name in self.SCENES:
            getattr(self, name)()
        self.end_card([
            "A job optimal matching is always candidate pessimal, which is Theorem 11.3: every "
            "candidate gets the worst job she has in any stable matching.",
            "If a stable matching gave her less, she and her job from the job optimal matching "
            "would be a rogue couple in it.",
            "Let the candidates propose, and the result is candidate optimal instead.",
            "The residency match began with the hospitals proposing and has had the students "
            "proposing since the nineteen nineties.",
        ])

    # ---- scene 1: the two stable matchings, seen from the candidates' side
    def hook(self):
        self.head = head = self.heading("What do the candidates get?")
        strip = VGroup(fit(txt("jobs", 18, GREY_B), STRIP_W).move_to([STRIP_X, JOB_HEAD_Y, 0]),
                       fit(txt("candidates", 18, GREY_B), STRIP_W).move_to([STRIP_X, CAND_HEAD_Y, 0]))
        self.job_head = job_head = VGroup(*[header(f"Job {j}", x, JOB_HEAD_Y) for j, x in zip(JOB_IDS, X)])
        self.job_cell = job_cell = [cells(JOB_Y, x) for x in X]
        self.job_name = job_name = [[word(JOBS[j][r], X[i], JOB_Y[r]) for r in range(len(JOBS[j]))]
                                    for i, j in enumerate(JOB_IDS)]
        self.cand_head = cand_head = VGroup(*[header(c, x, CAND_HEAD_Y, GOLD_C)
                                              for c, x in zip(CAND_NAMES, X)])
        self.cand_cell = cand_cell = [cells(CAND_Y, x) for x in X]
        self.cand_name = cand_name = [[word(f"Job {j}", X[i], CAND_Y[r]) for r, j in enumerate(CANDS[c])]
                                      for i, c in enumerate(CAND_NAMES)]
        jobs_block = VGroup(job_head, *job_cell, *[n for ns in job_name for n in ns])
        cands_block = VGroup(cand_head, *cand_cell, *[n for ns in cand_name for n in ns])
        self.sq = sq = [Square(SQ, stroke_color=c, stroke_width=BORDER).move_to([RS_X, y, 0])
                        for c, y in zip((YELLOW_D, GREEN_C, PURPLE_B), LEG_Y)]
        self.lg = lg = [fit(txt(s, 18, c), STRIP_W).move_to([RS_X, y, 0])
                        for s, c, y in (("both", YELLOW_D, LEG_Y[0] - 0.30),
                                        ("first", GREEN_C, LEG_Y[1] - 0.30),
                                        ("second", PURPLE_B, LEG_Y[2] - 0.30))]

        self.say("Propose and reject gives every job its optimal candidate, the best partner it has "
                 "in any stable matching. In our example that is the green matching, and the purple "
                 "one is the only other stable matching.",
                 FadeIn(head),
                 LaggedStart(FadeIn(strip), FadeIn(jobs_block, shift=UP * 0.2),
                             FadeIn(cands_block, shift=UP * 0.2), lag_ratio=0.6))
        self.cue("the green matching",
                 *[mark(job_cell[j - 1][JOB_GREEN[j]], YELLOW_D if j in BOTH_JOB else GREEN_C)
                   for j in JOB_IDS],
                 *[mark(cand_cell[CAND_NAMES.index(c)][CAND_GREEN[c]],
                        YELLOW_D if c in BOTH_CAND else GREEN_C) for c in CAND_NAMES],
                 FadeIn(sq[0]), FadeIn(lg[0]), FadeIn(sq[1]), FadeIn(lg[1]))
        self.cue("the purple one",
                 *[mark(job_cell[j - 1][JOB_PURPLE[j]], PURPLE_B) for j in JOB_IDS if j not in BOTH_JOB],
                 *[mark(cand_cell[CAND_NAMES.index(c)][CAND_PURPLE[c]], PURPLE_B)
                   for c in CAND_NAMES if c not in BOTH_CAND],
                 FadeIn(sq[2]), FadeIn(lg[2]))

        self.say("Now look at the columns of the candidates. For Cleo and for Dora the green job "
                 "sits below the purple one. So the matching that is best for every job gives these "
                 "two the lowest job they have in any stable matching, which we called pessimal.",
                 AnimationGroup(*[flash(h) for h in cand_head]))
        self.cue("For Cleo",
                 LaggedStart(flash(cand_cell[2][CAND_GREEN["Cleo"]]),
                             flash(cand_cell[2][CAND_PURPLE["Cleo"]]), lag_ratio=1.0))
        self.cue("for Dora",
                 LaggedStart(flash(cand_cell[3][CAND_GREEN["Dora"]]),
                             flash(cand_cell[3][CAND_PURPLE["Dora"]]), lag_ratio=1.0))
        self.pess = fit(txt("pessimal", 22, GREEN_C), STRIP_W).move_to([STRIP_X, SLOT_LP_Y, 0])
        self.cue("pessimal", FadeIn(self.pess),
                 *[mark(cand_cell[CAND_NAMES.index(c)][CAND_GREEN[c]], GREEN_C, CELL_MARK)
                   for c in ("Cleo", "Dora")])

        self.say("Ada and Bea have the same job in both, so for them best and worst are one and the "
                 "same. Is this an accident of the example, or a law? Let us test it on Cleo, whose "
                 "green job is job three.",
                 AnimationGroup(flash(cand_cell[0][CAND_GREEN["Ada"]]),
                                flash(cand_cell[1][CAND_GREEN["Bea"]])))
        rs_law = fit(txt("a law?", 24, YELLOW_D), RS_W).move_to([RS_X, SLOT_RS_Y, 0])
        self.cue("or a law", FadeIn(rs_law))
        self.cue("test it on Cleo",
                 LaggedStart(flash(cand_head[2]), flash(cand_cell[2][CAND_GREEN["Cleo"]]), lag_ratio=1.0))
        self.hold()
        self.play(FadeOut(rs_law))

    # ---- scene 2: the same steps run on Cleo, with names
    def cleo(self):
        old_head, self.head = self.head, self.heading("Could Cleo do worse?")
        head = self.head
        job_head, job_cell, job_name = self.job_head, self.job_cell, self.job_name
        cand_head, cand_cell = self.cand_head, self.cand_cell
        cand_name = self.cand_name
        col, j3 = CAND_NAMES.index("Cleo"), JOB_IDS.index(3)   # the two columns of the proof
        green_cleo, green_j3 = CAND_GREEN["Cleo"], JOB_GREEN[3]
        below3 = BELOW_JOB[3]                        # the rows of Job 3 below Cleo: Bea, Dora

        self.say("Suppose there were some other stable matching in which Cleo has a job she likes "
                 "less than job three. On her list that could only be job one or job four.",
                 FadeOut(old_head), FadeIn(head), flash(cand_cell[col][green_cleo]))
        self.cue("likes less", AnimationGroup(*[flash(cand_cell[col][r]) for r in BELOW_CLEO]))
        self.cue("job one or job four", *[mark(cand_cell[col][r], RED_C) for r in BELOW_CLEO])

        self.say("In that matching job three is not with Cleo, so it has some other candidate. Could "
                 "she be above Cleo on its list? No, because Cleo is the optimal candidate of job "
                 "three, the best it gets in any stable matching, and this matching is stable.",
                 flash(job_head[j3]))
        self.cue("some other candidate",
                 AnimationGroup(*[flash(job_cell[j3][r]) for r in range(4) if r != green_j3]))
        self.cue("above Cleo on its list", flash(job_cell[j3][0]))
        self.cue("optimal candidate of job three",
                 LaggedStart(flash(job_cell[j3][green_j3]),
                             job_cell[j3][0].animate.set_stroke(opacity=0.25),
                             job_name[j3][0].animate.set_opacity(0.25), lag_ratio=1.0))

        r_line = rogue_line()
        rs_bad = VGroup(fit(txt("not", 24, RED_C), RS_W),
                        fit(txt("stable", 24, RED_C), RS_W)).arrange(DOWN, buff=0.05)
        rs_bad.move_to([RS_X, SLOT_RS_Y, 0])
        rogue_heads = [job_head[j3][0], cand_head[col][0]]     # Job 3's header, and the Cleo header
        self.say("So that other candidate is below Cleo, and job three would rather have Cleo. And "
                 "Cleo would rather have job three than her job there, because that is what we "
                 "supposed. They are a rogue couple, so that matching is not stable after all.")
        self.cue("below Cleo", *[mark(job_cell[j3][r], RED_C) for r in below3])
        self.cue("would rather have job three", flash(cand_cell[col][green_cleo]))
        self.cue("a rogue couple", Create(r_line), *[mark(h, ORANGE) for h in rogue_heads])
        self.cue("not stable after all", FadeIn(rs_bad))

        self.say("So no stable matching gives Cleo less than job three. Job three is the worst she "
                 "can get, her pessimal job, and the job optimal matching hands her exactly that.",
                 FadeOut(r_line), FadeOut(rs_bad),
                 rogue_heads[0].animate.set_stroke(BLUE_C, HEAD_BORDER),
                 rogue_heads[1].animate.set_stroke(GOLD_C, HEAD_BORDER))
        self.cue("less than job three",
                 *[cand_cell[col][r].animate.set_stroke(GREY_B, THIN, opacity=0.25) for r in BELOW_CLEO],
                 *[cand_name[col][r].animate.set_opacity(0.25) for r in BELOW_CLEO],
                 *[job_cell[j3][r].animate.set_stroke(GREY_B, THIN) for r in below3],
                 job_cell[j3][0].animate.set_stroke(opacity=1.0),
                 job_name[j3][0].animate.set_opacity(1.0))
        self.cue("her pessimal job", flash(cand_cell[col][green_cleo]), flash(self.pess))
        self.cue("hands her exactly that",
                 *[cand_cell[col][r].animate.set_stroke(opacity=1.0) for r in BELOW_CLEO],
                 *[cand_name[col][r].animate.set_opacity(1.0) for r in BELOW_CLEO])
        self.hold()

    # ---- scene 3: the same argument with no name in it
    def law(self):
        old_head, self.head = self.head, self.heading("Best for one side, worst for the other")
        head = self.head
        job_head, job_cell = self.job_head, self.job_cell
        cand_head, cand_cell = self.cand_head, self.cand_cell
        cleo_col = CAND_NAMES.index("Cleo")
        j3 = JOB_IDS.index(3)

        self.say("The argument never used the name of Cleo. Take any candidate, and call the job she "
                 "gets in the job optimal matching her green job. Suppose some stable matching gave "
                 "her a job she likes less. Then her green job has another partner there, and it "
                 "likes her more, because she is its optimal candidate.",
                 FadeOut(old_head), FadeIn(head), flash(cand_head[cleo_col]))
        self.cue("Take any candidate", AnimationGroup(*[flash(h) for h in cand_head]))
        self.cue("matching her green job",
                 AnimationGroup(*[flash(cand_cell[i][CAND_GREEN[c]]) for i, c in enumerate(CAND_NAMES)]))
        self.cue("a job she likes less",
                 AnimationGroup(*[flash(cand_cell[i][r]) for i, c in enumerate(CAND_NAMES)
                                  for r in BELOW_CAND[c]]))
        self.cue("its optimal candidate",
                 AnimationGroup(*[flash(job_cell[i][JOB_GREEN[j]]) for i, j in enumerate(JOB_IDS)]))

        r_line = rogue_line()
        rogue_heads = [job_head[j3][0], cand_head[cleo_col][0]]   # Job 3's header, and the Cleo header
        gap = fit(txt("Theorem 11.3: a job optimal matching is candidate pessimal", 20, YELLOW_D),
                  GAP_W).move_to([0, GAP_Y, 0])
        self.say("So she and her green job would both rather have each other, and that matching has a "
                 "rogue couple. So it does not exist, and her green job is her pessimal job. A job "
                 "optimal matching is always candidate pessimal.")
        self.cue("a rogue couple", Create(r_line), *[mark(h, ORANGE) for h in rogue_heads])
        self.cue("does not exist", FadeOut(r_line),
                 rogue_heads[0].animate.set_stroke(BLUE_C, HEAD_BORDER),
                 rogue_heads[1].animate.set_stroke(GOLD_C, HEAD_BORDER))
        self.cue("always candidate pessimal", FadeIn(gap))
        self.hold()
        self.play(FadeOut(gap))

    # ---- scene 4: who should propose, and what the real match did
    def swap(self):
        old_head, self.head = self.head, self.heading("Who should propose?")
        head = self.head
        job_head, job_cell = self.job_head, self.job_cell
        cand_head, cand_cell = self.cand_head, self.cand_cell
        sq, lg = self.sq, self.lg
        col = {c: i for i, c in enumerate(CAND_NAMES)}
        down, up = [arrow(*p) for p in D_PTS], [arrow(*p) for p in P_PTS]
        asks = [arrow(*p) for p in U_PTS]
        slot_lj = fit(txt("job optimal", 18, GREEN_C), STRIP_W).move_to([STRIP_X, SLOT_LJ_Y, 0])
        slot_c1 = fit(txt("candidate", 18, PURPLE_B), STRIP_W).move_to([STRIP_X, SLOT_LC1_Y, 0])
        slot_c2 = fit(txt("optimal", 18, PURPLE_B), STRIP_W).move_to([STRIP_X, SLOT_LC2_Y, 0])
        gap_hosp = fit(txt(f"{MATCH_YEAR} hospitals propose", 20), GAP_W).move_to([0, GAP_Y, 0])
        gap_stud = fit(txt(f"{NINETIES} students propose", 20), GAP_W).move_to([0, GAP_Y, 0])
        rs_years = VGroup(fit(txt(str(MATCH_YEAR), 20), RS_W),
                          fit(txt(str(PAPER_YEAR), 20), RS_W)).arrange(DOWN, buff=0.05)
        rs_years.move_to([RS_X, SLOT_RS_Y, 0])

        self.say("So the side that proposes gets its best stable outcome, and the side that answers "
                 "gets its worst. Then the remedy for the candidates is to let them do the proposing. "
                 "None of our proofs cared which side was called jobs, so with candidates proposing "
                 "the result is candidate optimal.",
                 FadeOut(old_head), FadeIn(head))
        self.cue("the side that proposes", LaggedStart(*[Create(a) for a in down], lag_ratio=0.2),
                 FadeIn(slot_lj))
        self.cue("let them do the proposing", *[FadeOut(a) for a in down])
        self.cue("let them do the proposing", LaggedStart(*[Create(a) for a in up], lag_ratio=0.2))
        self.cue("is candidate optimal", FadeIn(slot_c1), FadeIn(slot_c2),
                 AnimationGroup(*[flash(cand_cell[col[c]][CAND_PURPLE[c]]) for c in CAND_NAMES]))

        self.say("Try it on our lists. Ada asks job one, Bea asks job four, Cleo asks job two, and "
                 "Dora asks job three. Every job has exactly one offer, so it stops on the first day, "
                 "and the result is the purple matching.",
                 *[FadeOut(a) for a in up])
        # the four asks: each arrow grows from the moment its name is said (lead 0), so no
        # part of it is on the stage while the sentence before it is still being read
        for i, phrase in enumerate(("Ada asks job one", "Bea asks job four",
                                    "Cleo asks job two", "asks job three")):
            self.cue(phrase, Create(asks[i]), flash(job_head[U_JOBS[i] - 1]), lead=0.0)
        self.cue("the purple matching", *[a.animate.set_color(PURPLE_B) for a in asks],
                 AnimationGroup(*[flash(cand_cell[col[c]][CAND_PURPLE[c]]) for c in CAND_NAMES]))

        self.say("This choice was made for real in the residency match. At first the hospitals did "
                 "the proposing, so the result was hospital optimal. In the nineteen nineties the "
                 "roles were reversed, so that the students do the proposing. Later changes also let "
                 "married couples ask for positions at the same or nearby hospitals.",
                 *[FadeOut(a) for a in asks])
        self.cue("the hospitals did the proposing", FadeIn(gap_hosp))
        self.cue("the roles were reversed", FadeOut(gap_hosp), FadeIn(gap_stud))
        self.cue("married couples",
                 AnimationGroup(flash(cand_head[col["Cleo"]]), flash(cand_head[col["Dora"]])))

        gap = fit(txt("Gale and Shapley, College Admissions and the Stability of Marriage, 1962", 20),
                  GAP_W).move_to([0, GAP_Y, 0])
        self.say("The algorithm was in use for ten years before Gale and Shapley analysed it properly, "
                 "in a paper from nineteen sixty-two. It always stops, it always ends in a stable "
                 "matching, and it gives the best stable outcome to whoever proposes. So the question "
                 "to ask of any matching system is who makes the offers.")
        self.cue("Gale and Shapley", FadeOut(gap_stud), FadeIn(gap), FadeIn(rs_years))
        self.cue("always stops", AnimationGroup(*[flash(h) for h in job_head]))
        self.cue("a stable", AnimationGroup(*[flash(s) for s in sq], *[flash(t) for t in lg]))
        self.cue("whoever proposes", AnimationGroup(flash(slot_lj), flash(slot_c1), flash(slot_c2)))
        self.cue("who makes the offers", flash(gap))
        self.hold()
