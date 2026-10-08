"""CS70 Note 11, episode 07: propose and reject always ends with a stable matching.

Built from BOARD-ep07.md: every `> ` line of the board is one say() below, copied
unchanged, and the picture is built as the board's stage lines describe.
"""
import os
import sys
from itertools import permutations, product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---------------------------------------------------------------- FACTS
# The board's "Facts" table. Every list, name and number the episode shows or says
# is computed here and asserted; the picture reads these names, never a typed value.
JOBS = {"Approximation": ["Anita", "Bridget", "Christine"],
        "Basis":         ["Bridget", "Anita", "Christine"],
        "Control":       ["Anita", "Bridget", "Christine"]}
CANDS = {"Anita":     ["Basis", "Approximation", "Control"],
         "Bridget":   ["Approximation", "Basis", "Control"],
         "Christine": ["Approximation", "Basis", "Control"]}
JOB_NAMES = list(JOBS)                   # left to right on the stage
CAND_NAMES = list(CANDS)


def run(jobs, cands):
    """F2/F4: propose and reject. Returns (job -> candidate, the pairs crossed off in
    order, True when some list ran empty before the last day)."""
    left = {j: list(l) for j, l in jobs.items()}
    crossed_all, exhausted = [], False
    while True:
        exhausted = exhausted or any(not left[j] for j in jobs)
        offers = {j: left[j][0] for j in jobs if left[j]}
        hand, crossed = {}, []
        for c in cands:
            got = [j for j in offers if offers[j] == c]
            if got:
                best = min(got, key=cands[c].index)
                hand[c] = best
                crossed += [(j, c) for j in got if j != best]
        crossed_all += crossed
        if not crossed:
            return {j: c for c, j in hand.items()}, crossed_all, exhausted
        for j, c in crossed:
            left[j].remove(c)


def rogue(jobs, cands, m):
    """Every rogue couple of the matching m: a job and a candidate it ranks above its
    partner who ranks it above the job she has."""
    has = {c: j for j, c in m.items()}
    return [(j, c) for j in jobs for c in jobs[j][:jobs[j].index(m[j])]
            if cands[c].index(j) < cands[c].index(has[c])]


RESULT, CROSSED, EXHAUSTED = run(JOBS, CANDS)                     # F2
assert RESULT == {"Approximation": "Anita", "Basis": "Bridget", "Control": "Christine"}
assert CROSSED == [("Control", "Anita"), ("Control", "Bridget")]  # Anita, then Bridget refused
assert not EXHAUSTED
assert JOBS["Control"] == ["Anita", "Bridget", "Christine"]       # F6
assert CANDS["Anita"] == ["Basis", "Approximation", "Control"]    # F6
assert CANDS["Anita"].index("Approximation") < CANDS["Anita"].index("Control")       # F7
assert CANDS["Bridget"].index("Basis") < CANDS["Bridget"].index("Control")           # F7
assert len(JOBS) == 3 and len(CANDS) == 3                         # "three hands"
assert len(JOBS) - 1 == 2                                         # F9: "two other jobs"
HAND_JOB = {c: j for j, c in RESULT.items()}                      # the job in each hand
assert HAND_JOB["Anita"] == "Approximation" and HAND_JOB["Bridget"] == "Basis"       # F7
assert HAND_JOB["Christine"] == "Control"

if __name__ == "__main__":     # F4/F5, the board's full check: all 46656 instances, a few seconds
    names_j, names_c = list(JOBS), list(CANDS)
    never_exhausted = always_matching = always_stable = True
    for jl in product(permutations(names_c), repeat=3):
        for cl in product(permutations(names_j), repeat=3):
            jobs, cands = dict(zip(names_j, map(list, jl))), dict(zip(names_c, map(list, cl)))
            m, _, ex = run(jobs, cands)
            never_exhausted = never_exhausted and not ex
            always_matching = always_matching and sorted(m) == sorted(names_j) \
                and sorted(m.values()) == sorted(names_c)
            always_stable = always_stable and always_matching and rogue(jobs, cands, m) == []
    assert never_exhausted and always_matching and always_stable
    print("46656 instances: never exhausted, always a matching, always stable")

# ---------------------------------------------------------------- the board's stages
# stage one (`worry` and `hands`): Control's list, and the three hands it could not fill
X_LIST, HEAD_Y1 = -5.0, 2.3              # Control's own list, on the left
LIST_Y = [1.72, 1.20, 0.68]              # its three names, its favourite on top
X_CAND = [-1.2, 1.9, 5.0]                # the three candidates, and the chips below them
HAND_Y1, HAND_H = 1.6, 0.7               # the hand cells under the candidate headers
CHIP_Y1 = -0.2                           # the job chips
LAB_X1, SLOT_W = -3.1, 1.3               # the row labels "in hand" and "jobs"
LINE_Y1 = [-1.2, -1.8, -2.4]             # L1, L2, L3
CELL_W, CELL_H = 2.4, 0.48
HEAD_W, HEAD_H = 2.4, 0.55
WORD_MAX = 0.4                           # a word stays this far inside its box
HAND_W = 2.2                             # a word in a hand cell
LINE_W = 10.0                            # the widest a centred line may be
ARROW_Y0, ARROW_Y1 = 0.1, 1.2            # a chip arrow: from the chip to the hand above

# stage two (`stable`): the episode-1 result, three job columns over three candidate ones
X2 = [-3.9, 0.5, 4.9]                    # a job column and the candidate column under it
JOB_Y2 = [1.86, 1.35, 0.84]              # a job's cells, its favourite on top
CAND_Y2 = [-1.41, -1.92, -2.43]          # a candidate's cells, her favourite on top
JOB_HY2, CAND_HY2 = 2.42, -0.85          # the two header rows
STRIP_X, STRIP_W = -6.0, 1.2             # the left strip: "jobs" over "candidates"
E2_PTS = [(-4.3, 0.55, -4.3, -0.52),     # the three green lines of the gap, one per pair
          (0.9, 0.55, 0.9, -0.52), (4.9, 0.55, 4.9, -0.52)]
A1_PTS = ((4.5, 0.55), (-3.5, -0.52))    # Control's refused ask to Anita
A2_PTS = ((4.5, 0.55), (0.1, -0.52))     # ... and to Bridget; never on stage together
ASK_X, ASK_Y, ASK_W = -1.7, 0.33, 3.0    # the ask label in the gap
JOB_PARTNER = {j: JOBS[j].index(RESULT[j]) for j in JOB_NAMES}        # the row of its partner
CAND_PARTNER = {c: CANDS[c].index(HAND_JOB[c]) for c in CAND_NAMES}   # the row of her job
assert JOB_PARTNER == {"Approximation": 0, "Basis": 0, "Control": 2}       # F2: the green cells
assert CAND_PARTNER == {"Anita": 1, "Bridget": 1, "Christine": 2}          # F2: the green cells
assert len(E2_PTS) == len(JOBS) == 3

# stage three (`general`): the same step with names left out
X_JOB3, X_CAND3, HEAD_Y3 = -4.8, -1.9, 2.3
LIST3_Y = [1.72, 1.20]                   # "C*" over "C"; "her final job" over "J"
PROOF_X3, PROOF_W = 0.0, 6.6             # the proof lines: left edge at 0, at most this wide
PROOF_Y3 = [2.3, 1.8, 1.3, 0.8, 0.3]     # Q1 to Q5
T_Y3 = [-0.8, -1.5, -2.3]                # T1, T2, T3


def fit(t, w):
    if t.width > w:
        t.scale_to_fit_width(w)
    return t


def cells(ys, x, w=CELL_W, h=CELL_H, color=GREY_B, width=2):
    return VGroup(*[Rectangle(width=w, height=h, stroke_color=color, stroke_width=width)
                    .move_to([x, y, 0]) for y in ys])


def boxed(text, x, y, color=BLUE_C, w=HEAD_W, h=HEAD_H, size=22):
    """A header box or a chip, its word kept WORD_MAX inside the box."""
    b = box_label(text, color, w=w, h=h, font_size=size).move_to([x, y, 0])
    fit(b[1], w - WORD_MAX)
    return b


def in_box(s, x, y, w=CELL_W - WORD_MAX, size=22, color=C_TEXT):
    """A word in a list cell: at most the cell width minus WORD_MAX."""
    return fit(txt(s, size, color), w).move_to([x, y, 0])


def cell_word(s, x, y, size=20, color=C_TEXT, w=HAND_W):
    """A word in a hand cell: at most HAND_W wide, first choice size 20."""
    return fit(txt(s, size, color), w).move_to([x, y, 0])


def slot_text(s, x, y, size=20, color=GREY_B, w=SLOT_W):
    """A label in the narrow slot beside the list or the chips."""
    return fit(txt(s, size, color), w).move_to([x, y, 0])


def line_text(s, size, y, color=C_TEXT, w=LINE_W):
    """A line of the picture, centred at x = 0, never wider than w."""
    return fit(txt(s, size, color), w).move_to([0, y, 0])


def left_text(s, size, y, color=C_TEXT, x0=PROOF_X3, w=PROOF_W):
    """A line of the picture with its left edge at x0, never wider than w."""
    t = fit(txt(s, size, color), w)
    return t.move_to([x0 + t.width / 2, y, 0])


def strip_text(s, size=22, color=GREY_B):
    """A text of the left strip: never wider than the strip's slot."""
    return fit(txt(s, size, color), STRIP_W)


def ask_label(s):
    """The ask label in the gap, above the arrows and between E1 and E2."""
    return fit(txt(s, 22, ORANGE), ASK_W).move_to([ASK_X, ASK_Y, 0])


def gap_arrow(pts):
    """The orange arrow of a refused ask, grown across the gap."""
    return Arrow([pts[0][0], pts[0][1], 0], [pts[1][0], pts[1][1], 0], buff=0,
                 color=ORANGE, stroke_width=5, tip_length=0.18)


def flash(mob):
    return Indicate(mob, color=YELLOW_D, scale_factor=1.1)


def mark(mob, color, width=4):
    """Highlight a cell: its own stroke, at full opacity, however faded its name is."""
    return mob.animate.set_stroke(color, width, opacity=1)


def reset(mob):
    """A cell back to its plain border; the opacity of its name stays as it is."""
    return mob.animate.set_stroke(GREY_B, 2, opacity=1)


def chip_faded(chip):
    """A crossed-off chip: its box and its word fade; the box keeps its outline."""
    chip[0].set_stroke(opacity=0.25)
    chip[0].set_fill(opacity=0.04)
    chip[1].set_opacity(0.25)
    return chip


def chip_full(chip, color=BLUE_C):
    return (chip[0].animate.set_stroke(color, 3, opacity=1).set_fill(color, opacity=0.15),
            chip[1].animate.set_opacity(1))


class Ep07AlwaysStable(NarratedScene):
    """Episode 07: the algorithm never runs out of names, and its matching is stable."""

    SCENES = ["worry", "hands", "stable", "general"]

    def construct(self):
        if self.preview_only(self.SCENES):
            return
        self.title_card()
        for name in self.SCENES:
            getattr(self, name)()
        self.end_card([
            "No job is ever refused by every candidate, because the candidates' hands would need "
            "more jobs than there are.",
            "So propose and reject always ends with a matching, which is Lemma 11.3.",
            "Every candidate a job would rather have has refused it, and by the Improvement Lemma "
            "she ends with a job she likes more.",
            "So the result is always stable, which is Theorem 11.1, and a stable matching always "
            "exists.",
        ])

    # ---- scene 1: could a job be left with nobody to ask?
    def worry(self):
        self.head1 = head = self.heading("Can a job run out of names?")
        self.play(FadeIn(head))

        self.ctrl_head = boxed("Control", X_LIST, HEAD_Y1)
        self.ctrl_cell = cells(LIST_Y, X_LIST)
        self.ctrl_name = [in_box(n, X_LIST, y) for n, y in zip(JOBS["Control"], LIST_Y)]
        for r in range(2):      # episode 1 crossed Anita off, and then Bridget: the names
            self.ctrl_name[r].set_opacity(0.25)   # fade, the borders of the cells stay
        self.cand_head = VGroup(*[boxed(n, x, HEAD_Y1, GOLD_C) for n, x in zip(CAND_NAMES, X_CAND)])
        self.hand = VGroup(*[Rectangle(width=CELL_W, height=HAND_H, stroke_color=GREY_B, stroke_width=2)
                             .move_to([x, HAND_Y1, 0]) for x in X_CAND])
        self.lab_hand = slot_text("in hand", LAB_X1, HAND_Y1)

        self.say("We know that propose and reject always stops. But stopping is not the same as "
                 "succeeding. When it stops, is every job really paired with a candidate, and every "
                 "candidate with a job?",
                 FadeIn(VGroup(self.ctrl_head, self.ctrl_cell, *self.ctrl_name), shift=UP * 0.2))
        self.cue("every job really paired", mark(self.ctrl_cell[2], GREEN_C))
        self.cue("every candidate with a job",
                 LaggedStart(*[FadeIn(h, shift=UP * 0.2) for h in self.cand_head], lag_ratio=0.3))

        self.say("Here is what could go wrong. In the first episode Control was refused by Anita and "
                 "then by Bridget, and it ended with the last name on its list, Christine. What if "
                 "Christine had refused it too?",
                 flash(self.ctrl_head))
        self.cue("refused by Anita", flash(VGroup(self.ctrl_cell[0], self.cand_head[0])))
        self.cue("then by Bridget", flash(VGroup(self.ctrl_cell[1], self.cand_head[1])))
        self.cue("Christine had refused it too",
                 reset(self.ctrl_cell[2]), self.ctrl_name[2].animate.set_opacity(0.25),
                 flash(self.cand_head[2]))

        self.say("Then Control would have no name left, and it could never make an offer again. So "
                 "let us suppose that this happens to some job on some day, and look closely at the "
                 "end of that day.")
        self.cue("no name left", self.ctrl_head.animate.set_opacity(0.4))
        self.cue("the end of that day", FadeIn(self.hand), FadeIn(self.lab_hand))
        self.hold()

    # ---- scene 2: the three hands the two other jobs cannot fill
    def hands(self):
        head = self.heading("Three hands, two jobs")
        self.play(FadeOut(self.head1), FadeIn(head))
        self.head1 = None

        ctrl_cell, ctrl_name, hand = self.ctrl_cell, self.ctrl_name, self.hand
        holds_better = VGroup(*[cell_word("Control or better", x, HAND_Y1, color=GREEN_C)
                                for x in X_CAND])
        holds_other = VGroup(*[cell_word("above Control", x, HAND_Y1, color=GREEN_C)
                               for x in X_CAND])

        self.say("Each candidate who refused Control did so because she kept an offer she liked more. "
                 "And by the improvement lemma she still holds Control or something better at the end "
                 "of every later day. It cannot be Control itself, which she has refused, so she holds "
                 "another job.",
                 flash(self.cand_head))
        self.cue("kept an offer she liked more", *[mark(c, GREEN_C) for c in hand])
        self.cue("improvement lemma", FadeIn(holds_better))
        self.cue("another job", FadeOut(holds_better), FadeIn(holds_other))

        chip = VGroup(*[boxed(n, x, CHIP_Y1) for n, x in zip(JOB_NAMES, X_CAND)])
        lab_jobs = slot_text("jobs", LAB_X1, CHIP_Y1)

        self.say("So at the end of that day all three candidates hold an offer, and none of the three "
                 "offers is from Control. A job makes only one offer each morning, so three hands need "
                 "three different jobs.",
                 flash(hand))
        self.cue("none of the three", FadeIn(VGroup(chip[0], chip[1]), shift=UP * 0.2),
                 FadeIn(chip_faded(chip[2])), FadeIn(lab_jobs))
        self.cue("three different jobs",
                 Transform(self.lab_hand, slot_text("3 hands", LAB_X1, HAND_Y1, 24)),
                 LaggedStart(*[flash(c) for c in hand], lag_ratio=0.5))

        line1 = line_text(f"{len(CANDS)} hands need {len(JOBS)} jobs, but only {len(JOBS) - 1} are left",
                          24, LINE_Y1[0], RED_C)
        line1n = line_text("n hands need n jobs, but only n - 1 are left", 24, LINE_Y1[0], RED_C)
        line2 = line_text("so no job is ever refused by every candidate", 24, LINE_Y1[1])

        self.say("But without Control only two jobs are left, Approximation and Basis. Two jobs cannot "
                 "fill three hands. So the day we supposed can never come, and Control cannot be "
                 "refused by everyone.",
                 flash(chip[2]))
        self.cue("Approximation and Basis", flash(VGroup(chip[0], chip[1])),
                 Transform(lab_jobs, slot_text("2 jobs", LAB_X1, CHIP_Y1, 24)))
        self.cue("cannot fill three hands", self.lab_hand.animate.set_color(RED_C),
                 lab_jobs.animate.set_color(RED_C))
        self.cue("can never come", FadeIn(line1))

        self.say("The same count works for any number of jobs. A job refused by everyone would leave "
                 "one job fewer than there are candidates, while every candidate holds an offer of "
                 "her own. So no job ever runs out of names.")
        self.cue("any number of jobs",
                 Transform(self.lab_hand, slot_text("n hands", LAB_X1, HAND_Y1, 22, RED_C)),
                 Transform(lab_jobs, slot_text("n - 1 jobs", LAB_X1, CHIP_Y1, 22, RED_C)),
                 Transform(line1, line1n))
        self.cue("one job fewer", flash(chip[2]))
        self.cue("runs out of names", FadeIn(line2))

        hand_text = VGroup(*[cell_word(HAND_JOB[c], x, HAND_Y1)
                             for c, x in zip(CAND_NAMES, X_CAND)])
        arrows = [Arrow([x, ARROW_Y0, 0], [x, ARROW_Y1, 0], buff=0, color=GREEN_C,
                        stroke_width=4, tip_length=0.18) for x in X_CAND]
        line3 = line_text("Lemma 11.3: it always ends with a matching", 24, LINE_Y1[2], YELLOW_D)

        self.say("So every morning every job has someone to ask. On the last day nobody is refused, so "
                 "every job's offer is in the hand of some candidate. No candidate holds two offers, "
                 "and there are as many candidates as jobs, so everyone is paired. Propose and reject "
                 "always ends with a matching.",
                 ctrl_cell[2].animate.set_stroke(GREEN_C, 4, opacity=1),
                 ctrl_name[2].animate.set_opacity(1),
                 self.ctrl_head.animate.set_opacity(1),
                 *chip_full(chip[2]),
                 line1.animate.set_color(GREY_B).set_opacity(0.3),
                 line2.animate.set_opacity(0.3),
                 Transform(self.lab_hand, slot_text("in hand", LAB_X1, HAND_Y1)),
                 Transform(lab_jobs, slot_text("jobs", LAB_X1, CHIP_Y1)),
                 FadeOut(holds_other))
        self.cue("nobody is refused", *[Create(a) for a in arrows], FadeIn(hand_text))
        self.cue("holds two offers", flash(hand))
        self.cue("ends with a matching", FadeIn(line3))
        self.hold()
        self.clear_stage()

    # ---- scene 3: the episode-1 matching, and the couple it might fail on
    def stable(self):
        head = self.heading("Is the result stable?")
        self.play(FadeIn(head))

        job_head = VGroup(*[boxed(n, x, JOB_HY2) for n, x in zip(JOB_NAMES, X2)])
        job_cell = [cells(JOB_Y2, x) for x in X2]
        job_name = [[in_box(JOBS[JOB_NAMES[i]][r], X2[i], JOB_Y2[r]) for r in range(3)]
                    for i in range(3)]
        cand_head = VGroup(*[boxed(n, x, CAND_HY2, GOLD_C) for n, x in zip(CAND_NAMES, X2)])
        cand_cell = [cells(CAND_Y2, x) for x in X2]
        cand_name = [[in_box(CANDS[CAND_NAMES[i]][r], X2[i], CAND_Y2[r]) for r in range(3)]
                     for i in range(3)]
        edges = VGroup(*[Line([x0, y0, 0], [x1, y1, 0], color=GREEN_C, stroke_width=4)
                         for x0, y0, x1, y1 in E2_PTS])
        strip = VGroup(txt("jobs", 22, GREY_B).move_to([STRIP_X, JOB_HY2, 0]),
                       strip_text("candidates").move_to([STRIP_X, CAND_HY2, 0]))
        ci = JOB_NAMES.index("Control")
        for r in range(2):                  # episode 1 crossed Anita off, and then Bridget:
            job_name[ci][r].set_opacity(0.25)    # the names fade, the borders stay
        for i, j in enumerate(JOB_NAMES):   # the partner cell of every job, and of every name
            job_cell[i][JOB_PARTNER[j]].set_stroke(GREEN_C, 4)
        for i, c in enumerate(CAND_NAMES):
            cand_cell[i][CAND_PARTNER[c]].set_stroke(GREEN_C, 4)
        stage = VGroup(job_head, *job_cell, *[n for ns in job_name for n in ns],
                       cand_head, *cand_cell, *[n for ns in cand_name for n in ns], edges, strip)

        self.say("Now the main question, whether that matching is stable. Here is the result of the "
                 "first episode, with the two names that Control crossed off shown faded. "
                 "Approximation and Basis have their first choices, so the only job that would rather "
                 "have someone else is Control.",
                 FadeIn(stage, shift=UP * 0.2))
        self.cue("shown faded", flash(VGroup(job_cell[ci][0], job_cell[ci][1])))
        self.cue("have their first choices", flash(VGroup(job_cell[0][0], job_cell[1][0])))
        self.cue("is Control", flash(job_head[ci]))

        a1 = gap_arrow(A1_PTS)
        lab1 = ask_label("day one: asked, refused")
        self.say("Control would rather have Anita, who is above its partner Christine. Now, why is "
                 "Anita above Christine and yet not its partner? A job works down its list, and it "
                 "only moves past a name when that name has refused it. So Control asked Anita on an "
                 "earlier day, and she said no.")
        self.cue("would rather have Anita", mark(job_cell[ci][0], ORANGE))
        self.cue("works down its list",
                 LaggedStart(*[flash(job_cell[ci][r]) for r in range(3)], lag_ratio=0.6))
        self.cue("she said no", Create(a1), FadeIn(lab1))

        ai = CAND_NAMES.index("Anita")
        self.say("Now the improvement lemma speaks. From the day Control asked her, Anita holds Control "
                 "or something better at the end of every day, and that includes the last day.",
                 flash(cand_head[ai]))
        self.cue("the day Control asked her", mark(cand_cell[ai][2], ORANGE))
        self.cue("or something better",
                 LaggedStart(*[flash(cand_cell[ai][r]) for r in (2, 1, 0)], lag_ratio=0.6))
        self.cue("the last day", flash(cand_cell[ai][1]))

        self.say("And on the last day she does not hold Control, because Control's last offer went to "
                 "Christine. So what Anita holds at the end is a job she likes more than Control, and "
                 "she has no wish to leave it. Control and Anita are not a rogue couple.")
        self.cue("went to", flash(edges[2]))
        self.cue("likes more than Control", flash(cand_cell[ai][1]))
        self.cue("not a rogue couple", reset(job_cell[ci][0]), reset(cand_cell[ai][2]),
                 FadeOut(a1), FadeOut(lab1))

        bi = CAND_NAMES.index("Bridget")
        a2 = gap_arrow(A2_PTS)
        lab2 = ask_label("day two: asked, refused")
        self.say("Bridget is the other name above Christine, and the same steps apply to her. Control "
                 "asked her on day two and she refused, so she ends with Control or better. It is not "
                 "Control, so it is Basis, which is higher on her list.",
                 mark(job_cell[ci][1], ORANGE))
        self.cue("asked her on day two", Create(a2), FadeIn(lab2))
        self.cue("ends with Control or better", mark(cand_cell[bi][2], ORANGE))
        self.cue("or better",
                 LaggedStart(*[flash(cand_cell[bi][r]) for r in (2, 1, 0)], lag_ratio=0.6))
        self.cue("higher on her list", flash(cand_cell[bi][1]), reset(job_cell[ci][1]),
                 reset(cand_cell[bi][2]), FadeOut(a2), FadeOut(lab2))
        self.hold()
        self.clear_stage()

    # ---- scene 4: the same argument with the names left out
    def general(self):
        head = self.heading("Any job, any candidate")
        self.play(FadeIn(head))

        job_head = boxed("job J", X_JOB3, HEAD_Y3)
        job_cell = cells(LIST3_Y, X_JOB3)
        job_name = [in_box("C*", X_JOB3, LIST3_Y[0]), in_box("C", X_JOB3, LIST3_Y[1])]
        job_cell[1].set_stroke(GREEN_C, 4)                       # its partner
        cand_head = boxed("candidate C*", X_CAND3, HEAD_Y3, GOLD_C)
        cand_cell = cells(LIST3_Y, X_CAND3)
        cand_name = [in_box("her final job", X_CAND3, LIST3_Y[0]), in_box("J", X_CAND3, LIST3_Y[1])]
        q = [left_text(s, 22, y) for s, y in zip(
            ["J would rather have C* than its partner C",
             "so J asked C* earlier, and she refused",
             "Improvement Lemma: she ends with J or better",
             "not J itself: J's last offer went to C",
             "so she likes her final job more: no rogue couple"], PROOF_Y3)]
        t1 = line_text("Theorem 11.1: the result of propose and reject is always stable",
                       24, T_Y3[0], YELLOW_D)
        t2 = line_text("so a stable matching always exists", 24, T_Y3[1])
        t3 = line_text("which stable matching, and good for whom?", 24, T_Y3[2], YELLOW_D)

        self.say("Nothing in those steps used the names. Take any job with its final partner, and "
                 "any candidate the job would rather have. She stands above the partner on its list, "
                 "so the job asked her on an earlier day and she refused.",
                 FadeIn(VGroup(job_head, job_cell, *job_name, cand_head, cand_cell, *cand_name),
                        shift=UP * 0.2))
        self.cue("would rather have", mark(job_cell[0], ORANGE), FadeIn(q[0]))
        self.cue("she refused", job_name[0].animate.set_opacity(0.4), FadeIn(q[1]))

        self.say("By the improvement lemma she ends with that job or a better one. It is not that "
                 "job, because its last offer went to its partner. So she ends with a job she likes "
                 "more, and she will not leave it.")
        self.cue("improvement lemma", mark(cand_cell[1], ORANGE), FadeIn(q[2]))
        self.cue("went to its partner", flash(job_cell[1]), FadeIn(q[3]))
        self.cue("she will not leave", mark(cand_cell[0], GREEN_C), FadeIn(q[4]))

        self.say("A rogue couple needs a job and a candidate who both want to switch, and here the "
                 "candidate never does. So the result of propose and reject has no rogue couple, "
                 "which means it is always stable. And so a stable matching always exists, which the "
                 "roommates could not promise.")
        self.cue("never does", flash(q[4]))
        self.cue("always stable", FadeIn(t1))
        self.cue("always exists", FadeIn(t2))

        self.say("But in episode three one set of lists had two stable matchings. So which one does "
                 "propose and reject choose, and who is it good for? That is where we go next.")
        self.cue("two stable matchings", flash(t2))
        self.cue("which one", FadeIn(t3))
        self.hold()
