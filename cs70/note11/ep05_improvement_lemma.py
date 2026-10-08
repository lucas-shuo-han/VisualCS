"""CS70 Note 11, episode 05: the algorithm always halts, and the improvement lemma.

Built from BOARD-ep05.md: every `> ` line of the board is one say() below, copied
unchanged, and the picture is built as the board's stage lines describe.
"""
import os
import sys
from itertools import permutations, product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---------------------------------------------------------------- FACTS
# The board's "Facts" table. Every list, name and number the episode shows or says is
# computed here and asserted; the picture reads these names and never a typed-in value.
JOBS = {"Approximation": ["Anita", "Bridget", "Christine"],
        "Basis":         ["Bridget", "Anita", "Christine"],
        "Control":       ["Anita", "Bridget", "Christine"]}
CANDS = {"Anita":     ["Basis", "Approximation", "Control"],
         "Bridget":   ["Approximation", "Basis", "Control"],
         "Christine": ["Approximation", "Basis", "Control"]}
JOB_NAMES = list(JOBS)                   # left to right on the stage


def run(jobs, cands):
    """Per day: (offers job -> candidate, in hand candidate -> job, crossed off (job, candidate))."""
    left = {j: list(l) for j, l in jobs.items()}
    days = []
    while True:
        offers = {j: left[j][0] for j in jobs if left[j]}
        hand, crossed = {}, []
        for c in cands:
            got = [j for j in offers if offers[j] == c]
            if got:
                best = min(got, key=cands[c].index)
                hand[c] = best
                crossed += [(j, c) for j in got if j != best]
        days.append((offers, hand, crossed))
        if not crossed:
            return days
        for j, c in crossed:
            left[j].remove(c)


DAYS = run(JOBS, CANDS)                                     # F3: the run of episode 1
CROSSED = [x for _, _, cr in DAYS for x in cr]
assert len(DAYS) == 3                                       # "three days"
assert CROSSED == [("Control", "Anita"), ("Control", "Bridget")]
REFUSALS = [(d, j, c) for d, (_, _, cr) in enumerate(DAYS) for j, c in cr]   # one day, one name
assert [d for d, _, _ in REFUSALS] == [0, 1] and len(REFUSALS) == len(CROSSED)
ANITA = [(sorted(j for j, c in o.items() if c == "Anita"), h.get("Anita"))   # F11
         for o, h, _ in DAYS]
assert ANITA == [(["Approximation", "Control"], "Approximation"),
                 (["Approximation"], "Approximation"), (["Approximation"], "Approximation")]
ANITA_REF = ANITA[0][0].index(REFUSALS[0][1])   # her day-1 offer that she refused, in the cell
assert len(JOBS) == 3 and len(CANDS) == 3                   # F4: three jobs, three names each
assert len(JOBS) * len(CANDS) == 9                          # "nine names in all"
assert all(len(v) == len(CANDS) for v in JOBS.values())     # "as many candidates"


def lemma_ok(jobs, cands):               # F7: the improvement lemma on one run
    days = run(jobs, cands)
    for k, (offers, _, _) in enumerate(days):
        for j, c in offers.items():
            for _, hand, _ in days[k:]:
                if c not in hand or cands[c].index(hand[c]) > cands[c].index(j):
                    return False
    return True


names_j, names_c = list(JOBS), list(CANDS)
max_refusal_days, lemma_holds = 0, True
for jl in product(permutations(names_c), repeat=3):
    for cl in product(permutations(names_j), repeat=3):
        jobs, cands = dict(zip(names_j, map(list, jl))), dict(zip(names_c, map(list, cl)))
        max_refusal_days = max(max_refusal_days, len(run(jobs, cands)) - 1)
        lemma_holds = lemma_holds and lemma_ok(jobs, cands)
assert max_refusal_days <= 9 and lemma_holds                 # F5: "at most nine days"; F7
assert max_refusal_days == 4                                 # what the check really found

# ---------------------------------------------------------------- the board's stages
# stage one (`hook`): the three job lists of episode 1, and the three days it took
X1 = [-3.9, 0.5, 4.9]                    # the three job columns
LIST_Y1 = [1.86, 1.35, 0.84]             # a job's cells, its favourite on top
HEAD_Y1 = 2.42
W_CELL, H_CELL = 2.4, 0.48
HEAD_W, HEAD_H = 2.4, 0.55
WORD_MAX = 0.4                           # a word stays this far inside its box
DAY_Y1, DAY_W, DAY_H = -0.3, 1.5, 0.6
DAY_X1 = [-3.9 + 1.7 * d for d in range(len(DAYS))]         # one box for each day of the run
SLOT_X1, SLOT_Y1 = 1.6, -0.3
A_Y1, B_Y1, C_Y1 = -1.3, -1.9, -2.45     # the three count lines

# stage two (`anita`): Anita's own list on the left, her three days on the right
AL_X, AL_HEAD_Y = -4.8, 1.95
AL_Y = [1.39, 0.88, 0.37]
GX = [2.6 * d for d in range(len(DAYS))]                    # one grid column for each day
G_HEAD_Y, OFF_Y, HAND_Y = 2.0, 1.15, 0.25
G_LAB_X = -2.4
OFF_GAP = 0.46                           # two offers in one cell sit this far apart
ST_Y = [-1.0, -1.6, -2.3]                # statement line 1, line 2, the lemma line

# stage three (`proof`): the candidate's list as a ladder, her days on the right
LAD_X, LAD_HEAD_Y = -4.4, 2.3
RUNG_Y = [1.74, 1.23, 0.72, 0.21, -0.30] # rung 1, her favourite, on top
RUNG_J = 3                               # J on rung 4; J' is never written on a rung
JP_X, JP_TICK = -2.95, -3.12             # the J' bracket, beside rungs 1 to 4 (J included)
JP_BOT, JP_TOP = -0.03, 1.98             # the bottom of rung 4, the top of rung 1
JP_LAB_XY = (-2.65, 0.95)
BETTER_X = -6.2                          # the up arrow beside the ladder
JL_HEAD_Y, JL_Y = -1.2, [-1.7, -2.17]    # the job's own short list, under the ladder
PX = [-0.6, 2.6, 5.3]                    # the day strip
P_DAY_Y, P_HAND_Y, P_LAB_X = 2.3, 1.65, -2.4
STEP_X = (3.65, 4.25)                    # the yellow step arrow between two days
CHAIN_X = [-0.8 + 1.4 * k for k in range(5)]        # the five boxes "k" to "k+4"
CHAIN_Y, CHAIN_W, CHAIN_H = 2.2, 1.0, 0.5
CHAIN_LAB = ["k", "k+1", "k+2", "k+3", "k+4"]
CHAIN_TIP, CHAIN_SIDE = 0.15, 0.52       # a link arrow starts and ends this far out
CHAIN_DOT_X, CHAIN_BIG = 5.9, 32         # the large "..."; the small one is `dots`
CHAIN_DAY_X, CHAIN_CAP_XY, CHAIN_CAP_W = -1.9, (2.6, 1.5), 8.0
PROOF_X, PROOF_Y = -1.6, [0.8, 0.25, -0.3, -0.85, -1.4, -2.0]
PROOF_W, LINE_W = 8.2, 11.6              # the widest a proof line, a statement line may be


def fit(t, w):
    if t.width > w:
        t.scale_to_fit_width(w)
    return t


def cells(ys, x, w=W_CELL, h=H_CELL, color=GREY_B, width=2):
    return VGroup(*[Rectangle(width=w, height=h, stroke_color=color, stroke_width=width)
                    .move_to([x, y, 0]) for y in ys])


def boxed(text, x, y, color=BLUE_C, w=W_CELL, h=HEAD_H, size=22):
    """A header box, its word kept WORD_MAX inside the box."""
    b = box_label(text, color, w=w, h=h, font_size=size).move_to([x, y, 0])
    fit(b[1], w - WORD_MAX)
    return b


def in_box(s, x, y, w=W_CELL - WORD_MAX, size=22, color=C_TEXT):
    """A word in a cell: at most the cell width minus WORD_MAX."""
    return fit(txt(s, size, color), w).move_to([x, y, 0])


def line_text(s, size, y, color=C_TEXT, left=None):
    """A line of the picture: centred, or with its left edge at `left`."""
    t = fit(txt(s, size, color), PROOF_W if left is not None else LINE_W)
    if left is None:
        return t.move_to([0, y, 0])
    return t.move_to([left + t.width / 2, y, 0])


def flash(mob):
    return Indicate(mob, color=YELLOW_D, scale_factor=1.1)


def mark(mob, color, width=4):
    return mob.animate.set_stroke(color, width)


def green_box(mob):
    """The chain's green box: stroke GREEN_C width 4 and fill GREEN_C opacity 0.25."""
    return mob.animate.set_stroke(GREEN_C, 4).set_fill(GREEN_C, 0.25)


def reset(mob):
    return mob.animate.set_stroke(GREY_B, 2)


def crossed_off(cell, name):
    """The board's way of crossing a name off: the cell and its name fade to 0.25."""
    return (cell.animate.set_stroke(GREY_B, 2, opacity=0.25), name.animate.set_opacity(0.25))


class Ep05ImprovementLemma(NarratedScene):
    """Episode 05: the count behind Lemma 11.1, and Lemma 11.2, the improvement lemma."""

    SCENES = ["hook", "anita", "proof"]

    def construct(self):
        if self.preview_only(self.SCENES):
            return
        self.title_card()
        for name in self.SCENES:
            getattr(self, name)()
        self.end_card([
            "Every day with a refusal crosses a name off a list for good, and there are only n times n "
            "names, so propose and reject always halts.",
            "Improvement Lemma: once a job has made a candidate an offer, she holds that job or a better "
            "one at the end of that day and of every later day.",
            "The reason is that an offer which was not refused is made again the next morning.",
            "So a candidate's hand only climbs her list, and a job only moves down its own.",
        ])

    def swap(self, attr, new):
        """A text in a slot changes: the old one out and the new one in, in one animation."""
        old = getattr(self, attr)
        setattr(self, attr, new)
        if old is None:
            return () if new is None else (FadeIn(new),)
        return (FadeOut(old),) if new is None else (FadeOut(old), FadeIn(new))

    def swap_at(self, slots, i, new):
        """The same, for the i-th slot of a list of texts (the three in-hand cells)."""
        old = slots[i]
        slots[i] = new
        if old is None:
            return () if new is None else (FadeIn(new),)
        return (FadeOut(old),) if new is None else (FadeOut(old), FadeIn(new))

    def refusal_at(self, k):
        """The cell and the name of the one name crossed off on refusal day k."""
        _, job, cand = REFUSALS[k]
        i, r = JOB_NAMES.index(job), JOBS[job].index(cand)
        return i, r

    # ---- scene 1: the count that says the algorithm stops
    def hook(self):
        self.head1 = self.heading("Does it always stop?")
        self.play(FadeIn(self.head1))
        self.list_head = [boxed(name, X1[i], HEAD_Y1) for i, name in enumerate(JOB_NAMES)]
        self.list_cell = [cells(LIST_Y1, x) for x in X1]
        self.list_name = [[in_box(JOBS[name][r], X1[i], LIST_Y1[r]) for r in range(len(CANDS))]
                          for i, name in enumerate(JOB_NAMES)]
        col = [VGroup(self.list_head[i], self.list_cell[i], *self.list_name[i])
               for i in range(len(JOB_NAMES))]
        self.days = [VGroup(Rectangle(width=DAY_W, height=DAY_H, stroke_color=GREY_B, stroke_width=2)
                            .move_to([x, DAY_Y1, 0]),
                            txt(f"Day {d + 1}", 22).move_to([x, DAY_Y1, 0]))
                     for d, x in enumerate(DAY_X1)]
        self.day_box = [g[0] for g in self.days]
        self.slot = txt("always?", 24, YELLOW_D).move_to([SLOT_X1, SLOT_Y1, 0])
        self.line_a = line_text(f"{len(JOB_NAMES)} × {len(CANDS)} = {len(JOBS) * len(CANDS)} names",
                                26, A_Y1)
        self.line_b = line_text(f"at most {len(JOBS) * len(CANDS)} days with a refusal", 22, B_Y1)
        self.line_c = line_text("Lemma 11.1: propose and reject always halts", 20, C_Y1, YELLOW_D)

        self.say("In the first episode, propose and reject stopped after three days, but that was one "
                 "example. The stopping rule waits for a day on which nobody is refused, so could there "
                 "be lists for which such a day never comes?",
                 LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in col], lag_ratio=0.35))
        self.cue("after three days",
                 LaggedStart(*[FadeIn(g, shift=UP * 0.2) for g in self.days], lag_ratio=0.3))
        self.cue("nobody is refused", mark(self.day_box[-1], GREEN_C))
        self.cue("never comes", FadeIn(self.slot))

        self.say("Look at what a day with a refusal does. In the evening the refused job crosses a name "
                 "off its list, and a name that is crossed off never comes back. On day one Control "
                 "crossed off Anita, and on day two it crossed off Bridget.",
                 *[mark(self.day_box[d], RED_C) for d, _, _ in REFUSALS])
        control = JOB_NAMES.index("Control")
        self.cue("crosses a name", flash(self.list_head[control]))
        i, r = self.refusal_at(0)
        self.cue("day one Control", *crossed_off(self.list_cell[i][r], self.list_name[i][r]),
                 flash(self.day_box[0]))
        i, r = self.refusal_at(1)
        self.cue("day two it crossed off Bridget", *crossed_off(self.list_cell[i][r], self.list_name[i][r]),
                 flash(self.day_box[1]))

        self.say("So every day that does not stop the algorithm uses up at least one name. And the supply "
                 "is limited, since three jobs with three names each make nine names in all. That means at "
                 "most nine days can have a refusal, and after that a day with no refusal has to come.")
        i0, r0 = self.refusal_at(0)
        i1, r1 = self.refusal_at(1)
        self.cue("uses up at least one name",
                 flash(VGroup(self.list_cell[i0][r0], self.list_cell[i1][r1])))
        self.cue("nine names in all", flash(VGroup(*[c for cells_i in self.list_cell for c in cells_i])),
                 FadeIn(self.line_a))
        self.cue("at most nine days", FadeIn(self.line_b))
        self.cue("has to come",
                 *self.swap("line_b", line_text(f"at most {len(JOBS) * len(CANDS)} days with a refusal, "
                                                "then a day with none: stop", 22, B_Y1)),
                 flash(self.day_box[-1]))

        self.say("Nothing in this count was special about three. With any number of jobs, and as many "
                 "candidates, the number of names is that number times itself. So only that many days can "
                 "have a refusal, and propose and reject always halts, whatever the lists are.",
                 flash(self.line_a))
        self.cue("any number of jobs", *self.swap("line_a", line_text("n × n names", 26, A_Y1)))
        self.cue("only that many days",
                 *self.swap("line_b", line_text("at most n × n days with a refusal, then a day with none: stop",
                                                22, B_Y1)))
        self.cue("always halts",
                 *self.swap("slot", txt("always", 24, GREEN_C).move_to([SLOT_X1, SLOT_Y1, 0])),
                 FadeIn(self.line_c))
        self.hold()
        self.clear_stage(self.head1)

    # ---- scene 2: what a candidate holds, day by day
    def anita(self):
        self.head2 = self.heading("What a candidate holds")
        self.play(FadeOut(self.head1), FadeIn(self.head2))
        self.head1 = None
        self.list = CANDS["Anita"]                       # her own ranked list, on the left
        head = boxed("Anita", AL_X, AL_HEAD_Y, GOLD_C)
        al_cell = cells(AL_Y, AL_X)
        al_name = [in_box(self.list[r], AL_X, AL_Y[r]) for r in range(len(self.list))]
        self.ghead = [VGroup(Rectangle(width=W_CELL, height=0.5, stroke_color=GREY_B, stroke_width=2)
                             .move_to([x, G_HEAD_Y, 0]),
                             txt(f"Day {d + 1}", 22).move_to([x, G_HEAD_Y, 0]))
                       for d, x in enumerate(GX)]
        self.off_cell = [Rectangle(width=W_CELL, height=1.0, stroke_color=GREY_B, stroke_width=2)
                         .move_to([x, OFF_Y, 0]) for x in GX]
        self.hand_cell = [Rectangle(width=W_CELL, height=0.6, stroke_color=GREY_B, stroke_width=2)
                          .move_to([x, HAND_Y, 0]) for x in GX]
        self.glab = [txt("offers", 20, GREY_B).move_to([G_LAB_X, OFF_Y, 0]),
                     txt("in hand", 20, GREY_B).move_to([G_LAB_X, HAND_Y, 0])]
        self.off_txt = {}                                # (day, which offer) -> its job
        for d, (offers, _) in enumerate(ANITA):
            for k, job in enumerate(offers):
                y = OFF_Y + (len(offers) - 1) * OFF_GAP / 2 - k * OFF_GAP
                self.off_txt[(d, k)] = in_box(job, GX[d], y, size=20)
        self.hand_txt = [in_box(hand, GX[d], HAND_Y, size=20) for d, (_, hand) in enumerate(ANITA)]
        self.st1 = line_text("job J makes an offer to candidate C on day k", 24, ST_Y[0])
        self.st2 = line_text("from day k on, C holds an offer she likes at least as much as J",
                             24, ST_Y[1])
        self.st3 = line_text("Lemma 11.2, the Improvement Lemma", 22, ST_Y[2], YELLOW_D)

        self.say("Halting is half of what we want, and the other half is that the result is stable. For that "
                 "we need to know what a candidate holds from day to day, so let us replay the three days "
                 "of Anita.",
                 FadeIn(VGroup(head, al_cell, VGroup(*al_name))))
        self.cue("what a candidate holds", FadeIn(VGroup(*self.glab)))
        self.cue("the three days of Anita",
                 LaggedStart(*[FadeIn(VGroup(self.ghead[d], self.off_cell[d], self.hand_cell[d]),
                                      shift=UP * 0.2) for d in range(len(DAYS))], lag_ratio=0.3))

        self.say("On day one Approximation and Control both made her an offer, and she kept Approximation "
                 "in hand. On days two and three Approximation simply asked again, and she kept it again.",
                 FadeIn(VGroup(*[self.off_txt[(0, k)] for k in range(len(ANITA[0][0]))])))
        self.cue("kept Approximation in hand", FadeIn(self.hand_txt[0]),
                 mark(self.hand_cell[0], GREEN_C),
                 self.off_txt[(0, ANITA_REF)].animate.set_color(RED_C))   # the offer she refused
        self.cue("simply asked again", *[FadeIn(self.off_txt[(d, 0)]) for d in range(1, len(DAYS))])
        self.cue("kept it again", *[FadeIn(self.hand_txt[d]) for d in range(1, len(DAYS))],
                 *[mark(self.hand_cell[d], GREEN_C) for d in range(1, len(DAYS))])

        self.say("Now pick any job that ever made Anita an offer, for example Control on day one. From that "
                 "day on, what Anita holds is never below Control on her own list. The same is true for "
                 "Approximation, where what she holds is exactly as good, because it is Approximation "
                 "itself.")
        control_cell = al_cell[self.list.index("Control")]
        best_cell = al_cell[self.list.index(ANITA[-1][1])]       # the cell of what she holds
        self.cue("Control on day one", flash(self.off_txt[(0, ANITA_REF)]),
                 mark(control_cell, ORANGE))
        self.cue("never below Control", mark(best_cell, GREEN_C),
                 flash(VGroup(*self.hand_cell)))
        self.cue("exactly as good", flash(VGroup(self.off_txt[(0, 0)], best_cell)))

        self.say("Here is the claim in general. Suppose a job makes an offer to a candidate on some day. "
                 "Then at the end of that day, and of every later day, she holds an offer she likes at "
                 "least as much. This is called the improvement lemma, and one example is not a proof of "
                 "it.",
                 flash(VGroup(head, al_cell)))
        self.cue("makes an offer", FadeIn(self.st1))
        self.cue("every later day", FadeIn(self.st2))
        self.cue("improvement lemma", FadeIn(self.st3))
        self.hold()
        self.clear_stage(self.head2)

    # ---- scene 3: why an offer that was not refused comes back
    def proof(self):
        self.head3 = self.heading("Why offers only get better")
        self.play(FadeOut(self.head2), FadeIn(self.head3))
        self.head2 = None
        head_c = boxed("candidate C", LAD_X, LAD_HEAD_Y, GOLD_C)
        rung = cells(RUNG_Y, LAD_X)                      # her list, rung 1 her favourite
        j_rung = in_box("J", LAD_X, RUNG_Y[RUNG_J])      # J' is not on a rung: it may be J
        # The J' bracket: it says J' is one of these four rungs, J included (beat 3.2).
        jp_bracket = VGroup(
            Line([JP_X, JP_BOT, 0], [JP_X, JP_TOP, 0], color=GREEN_C, stroke_width=5),
            Line([JP_TICK, JP_TOP, 0], [JP_X, JP_TOP, 0], color=GREEN_C, stroke_width=5),
            Line([JP_TICK, JP_BOT, 0], [JP_X, JP_BOT, 0], color=GREEN_C, stroke_width=5),
            txt("J'", 22, GREEN_C).move_to([JP_LAB_XY[0], JP_LAB_XY[1], 0]))
        arrow = lambda a, b, color: Arrow(a, b, buff=0, stroke_width=4, color=color,
                                          max_tip_length_to_length_ratio=0.12)
        up = arrow([BETTER_X, RUNG_Y[-1], 0], [BETTER_X, RUNG_Y[0], 0], GREY_B)
        better = txt("better", 18, GREY_B).move_to([BETTER_X, RUNG_Y[0] + 0.31, 0])
        down = arrow([BETTER_X, JL_Y[0] + 0.2, 0], [BETTER_X, JL_Y[1] - 0.18, 0], RED_C)
        day = [VGroup(Rectangle(width=2.0, height=0.5, stroke_color=GREY_B, stroke_width=2)
                      .move_to([x, P_DAY_Y, 0]),
                      txt(s, 22).move_to([x, P_DAY_Y, 0]))
               for s, x in zip(["day k", "day i", "day i+1"], PX)]
        self.day_box3 = [g[0] for g in day]
        dots = txt("...", 22).move_to([(PX[0] + PX[1]) / 2, P_DAY_Y, 0])
        hand = [Rectangle(width=2.0, height=0.55, stroke_color=GREY_B, stroke_width=2)
                .move_to([x, P_HAND_Y, 0]) for x in PX]
        hand_grp = VGroup(*hand)                 # the one object of the three in-hand cells
        plab = txt("in hand", 20, GREY_B).move_to([P_LAB_X, P_HAND_Y, 0])
        self.step = arrow([STEP_X[0], P_HAND_Y, 0], [STEP_X[1], P_HAND_Y, 0], YELLOW_D)
        self.hand_txt3 = [None] * len(PX)                # the three in-hand texts, as they change
        # The chain row of beat 3.5: it takes the place of the day strip, whose pieces
        # (the day boxes, the three in-hand cells with their texts, the step arrow, the
        # row label) hold no text of their own from here on.
        chain_box = [Rectangle(width=CHAIN_W, height=CHAIN_H, stroke_color=GREY_B, stroke_width=2)
                     .move_to([x, CHAIN_Y, 0]) for x in CHAIN_X]
        chain_num = [in_box(s, x, CHAIN_Y, w=CHAIN_W - WORD_MAX, size=20)
                     for s, x in zip(CHAIN_LAB, CHAIN_X)]
        chain_day = txt("day", 20, GREY_B).move_to([CHAIN_DAY_X, CHAIN_Y, 0])
        chain_dot = txt("...", CHAIN_BIG).move_to([CHAIN_DOT_X, CHAIN_Y, 0])
        chain_link = [Arrow([x + CHAIN_SIDE, CHAIN_Y, 0], [x + CHAIN_SIDE + 0.36, CHAIN_Y, 0],
                            buff=0, stroke_width=4, tip_length=CHAIN_TIP) for x in CHAIN_X[:-1]]
        chain_cap = fit(txt("the step works from any day i on which the claim holds, first with i = k",
                            20), CHAIN_CAP_W).move_to([CHAIN_CAP_XY[0], CHAIN_CAP_XY[1], 0])
        jl_head = boxed("job J'", LAD_X, JL_HEAD_Y, BLUE_C, h=0.5)
        jl_cell = cells(JL_Y, LAD_X, h=0.45)
        jl_lost = in_box("crossed off", LAD_X, JL_Y[0])
        jl_name = in_box("C", LAD_X, JL_Y[1])
        for m in (jl_cell[0], jl_lost):
            m.set_opacity(0.25)
        self.p1 = line_text("day k: J is among her offers, and she keeps the best one", 20, PROOF_Y[0], left=PROOF_X)
        self.p2 = line_text("day i: she holds J', which is J or better (J' may be J itself)", 20, PROOF_Y[1], left=PROOF_X)
        self.p3 = line_text("J' was not refused, so its list does not change", 20, PROOF_Y[2], left=PROOF_X)
        self.p4 = line_text("day i+1: J' asks C again", 20, PROOF_Y[3], left=PROOF_X)
        self.p5 = line_text("day i+1: she holds J' or better, which is J or better", 20, PROOF_Y[4], left=PROOF_X)
        self.p6 = line_text("do the two sides meet in a stable matching?", 20, PROOF_Y[5], YELLOW_D, left=PROOF_X)

        self.say("Take a candidate and a job that makes her an offer, and look at the afternoon of that same "
                 "day. She has at least this one offer to choose from, and the rule says she keeps the best "
                 "of what she has. So at the end of that day she holds this job or one she likes more.",
                 FadeIn(VGroup(head_c, rung, j_rung)), FadeIn(up), FadeIn(better),
                 LaggedStart(*[FadeIn(g, shift=DOWN * 0.2) for g in day], lag_ratio=0.25),
                 FadeIn(dots), FadeIn(hand_grp), FadeIn(plab))
        self.cue("makes her an offer", mark(rung[RUNG_J], ORANGE), flash(self.day_box3[0]))
        self.cue("keeps the best", FadeIn(self.p1))
        self.cue("this job or one she likes more", *[mark(rung[k], GREEN_C) for k in range(RUNG_J)],
                 *self.swap_at(self.hand_txt3, 0,
                               in_box("J or better", PX[0], P_HAND_Y, w=1.6, size=20, color=GREEN_C)))

        self.say("Now suppose that at the end of some day she holds a job that is at least this good. The "
                 "question is whether that job will ask her again tomorrow. She did not refuse it, and a job "
                 "makes only one offer a day, so in the evening it crossed nothing off its list.",
                 flash(self.day_box3[1]))
        self.cue("at least this good", FadeIn(jp_bracket),
                 *self.swap_at(self.hand_txt3, 1,
                               in_box("J'", PX[1], P_HAND_Y, w=1.6, size=20, color=GREEN_C)),
                 FadeIn(self.p2))
        self.cue("ask her again tomorrow", FadeIn(self.step))
        self.cue("crossed nothing off", FadeIn(VGroup(jl_head, jl_cell, jl_lost, jl_name)),
                 mark(jl_cell[1], YELLOW_D), FadeIn(self.p3))

        self.say("So the next morning her name is still the first one on its list that is not crossed off, "
                 "exactly as it was this morning. The morning rule then makes that job ask her again. That "
                 "is the step the whole proof turns on, because an offer that was not refused always comes "
                 "back the next day.")
        self.cue("not crossed", flash(jl_cell[1]))
        self.cue("ask her again",
                 *self.swap_at(self.hand_txt3, 2,
                               in_box("J' asks again", PX[2], P_HAND_Y, w=1.6, size=20)),
                 FadeIn(self.p4))
        self.cue("always comes back", flash(self.step), flash(self.p4))

        self.say("So tomorrow afternoon she again has that job among her offers, and again she keeps the "
                 "best of what she has. What she holds tomorrow is that job or one she likes more. And "
                 "since that job was at least as good as the original one, what she holds tomorrow is at "
                 "least as good too.",
                 flash(hand[2]))
        self.cue("keeps the best",
                 *self.swap_at(self.hand_txt3, 2,
                               in_box("J' or better", PX[2], P_HAND_Y, w=1.6, size=20, color=GREEN_C)))
        self.cue("that job or one she likes more", flash(jp_bracket))
        self.cue("the original one", flash(VGroup(*[rung[k] for k in range(RUNG_J + 1)])), FadeIn(self.p5))

        # Every piece of the day strip goes out as the object the scene holds: a VGroup
        # made here is not in the scene, and fading that out would leave its pieces (and
        # the texts of the day boxes, which are inside those groups) behind.
        strip = [*day, dots, hand_grp, *self.hand_txt3, self.step, plab]
        self.say("So the claim is true on the day of the offer, and whenever it is true on one day it is "
                 "true on the next. That carries it from day to day forever, which is a proof by induction "
                 "on the days. The hand of a candidate can only climb her list.",
                 *[FadeOut(m) for m in strip],
                 FadeIn(VGroup(chain_day, *chain_box, *chain_num, chain_dot)))
        self.cue("the day of the offer", green_box(chain_box[0]), flash(self.p1))   # the base case
        self.cue("true on the next", FadeIn(chain_cap), GrowArrow(chain_link[0]))
        self.play(green_box(chain_box[1]), run_time=0.5)     # and then k+1: the step with i = k
        self.cue("from day to day", GrowArrow(chain_link[1]), run_time=0.5)
        self.play(green_box(chain_box[2]), run_time=0.5)
        self.play(GrowArrow(chain_link[2]), run_time=0.5)
        self.play(green_box(chain_box[3]), run_time=0.5)
        self.play(GrowArrow(chain_link[3]), run_time=0.5)
        self.play(green_box(chain_box[4]), run_time=0.5)
        self.play(chain_dot.animate.set_color(GREEN_C), run_time=0.5)
        self.cue("only climb", mark(up, GREEN_C))
        self.play(flash(up))

        self.say("A job, meanwhile, starts at the top of its list and can only move down, because names are "
                 "crossed off and never come back. So candidates climb while jobs sink, and somewhere the "
                 "two have to meet. Whether the place where they meet is always stable is the question we "
                 "are heading for.",
                 flash(jl_head))
        self.cue("can only move down", FadeIn(down), flash(jl_cell[0]))
        self.cue("candidates climb while jobs sink", flash(VGroup(up, down)))
        self.cue("always stable", FadeIn(self.p6))
        self.hold()
