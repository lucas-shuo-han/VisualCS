"""CS70 Note 11, episode 06: the first counterexample, and the well-ordering principle.

Built from BOARD-ep06.md: every `> ` line of the board is one say() below, copied
unchanged, and the picture is built as the board's stage lines describe.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---------------------------------------------------------------- FACTS
# F1, F2: the claim for one day, on the days of the picture (stage A of the board).
DAYS = 8                                   # boxes k to k+7: the offer day and seven days after it
DAY_LABELS = ["k"] + [f"k+{i}" for i in range(1, DAYS)]
OFFER_DAY = DAY_LABELS.index("k")          # F2: the claim holds at the end of this day
FIRST_RED = DAY_LABELS.index("k+4")        # beat 1.3: "the first one" among the red days
DAY_BEFORE = DAY_LABELS.index("k+3")       # beat 1.4: the day just before the first red day
LATER_RED = DAY_LABELS.index("k+6")        # the second red day the picture draws
RED_PICTURE = [FIRST_RED, LATER_RED]       # a picture of "some days fail", not a claim of its own
UNDECIDED_AFTER = [i for i in range(DAYS) if i not in (OFFER_DAY, DAY_BEFORE) + tuple(RED_PICTURE)]
assert (OFFER_DAY, DAY_BEFORE, FIRST_RED, LATER_RED) == (0, 3, 4, 6)
assert RED_PICTURE == [4, 6]               # the two red days of beats 1.3 and 1.6
assert FIRST_RED < LATER_RED               # "the first one" comes first in the row
assert UNDECIDED_AFTER == [1, 2, 5, 7]     # what beat 1.6 still has to paint green

# F6: three sets of natural numbers and their smallest elements (notes 294 to 295).
PRIMES = [n for n in range(2, 100) if all(n % d for d in range(2, n))]
SET5 = [5, 2, 11, 7, 8]
ODDS = [n for n in range(100) if n % 2 == 1]
assert min(SET5) == 2                      # "its smallest element is two"
assert min(ODDS) == 1                      # "the odd numbers ... start at one"
assert min(PRIMES) == 2 and PRIMES[:5] == [2, 3, 5, 7, 11]   # "the primes ... start at two"
SHOWN_SET = SET5                           # beat 3.2: five numbers, five dots
SHOWN_ODDS = ODDS[:6]                      # beat 3.3: 1, 3, 5, 7, 9, 11
SHOWN_PRIMES = PRIMES[:5]
assert SHOWN_ODDS == [1, 3, 5, 7, 9, 11] and SHOWN_PRIMES == [2, 3, 5, 7, 11]
assert (len(SHOWN_SET), len(SHOWN_ODDS), len(SHOWN_PRIMES)) == (5, 6, 5)
ELEVEN = 11                                # beat 3.4: "pick any element of the set, say eleven"
BELOW_ELEVEN = list(range(ELEVEN))         # below eleven lie the eleven numbers zero to ten
assert len(BELOW_ELEVEN) == ELEVEN and BELOW_ELEVEN[0] == 0 and BELOW_ELEVEN[-1] == 10

# F8: what fails. The integers, the reals and the non-negative reals have no smallest element.
NEG_INTS = list(range(-1, -10, -1))        # the set of all negative integers, as beat 4.1 shows it
assert NEG_INTS == [-1, -2, -3, -4, -5, -6, -7, -8, -9]
assert all(n - 1 < n < 0 for n in range(-9, 0))       # below every negative integer there is another
XS = [1, 0.5, 0.25, 0.125, 1e-9]
assert all(0 < x / 2 < x for x in XS)      # half of a positive number is positive and smaller
HALVES = [1.0]                             # beat 4.2: the dots 1, 1/2, 1/4, 1/8, 1/16
while len(HALVES) < 5:
    HALVES.append(HALVES[-1] / 2)
LABELLED = HALVES[:-1]                     # the last dot has no label
assert HALVES == [1.0, 0.5, 0.25, 0.125, 0.0625] and len(LABELLED) == 4
assert all(0 < x / 2 < x for x in LABELLED)
assert HALVES[-1] / 2 < HALVES[-1]         # whatever is called the smallest, half is smaller

# ---------------------------------------------------------------- the board's stages
# stage A (`hook`, `same`): the row of eight days
BOX_W, BOX_H, ROW_Y = 1.3, 0.7, 1.3
DAY_X = [-5.25 + 1.5 * i for i in range(DAYS)]
DAY_LABEL_SIZE = 22
TOP_SIZE, TOP_Y, TOP_MAXW = 22, 2.35, 12.0
# review row 4: the under-labels are size 20, and "day before" (green) and
# "first red day" (red) sit at two heights 0.35 apart so they cannot touch.
UNDER_SIZE, UNDER_MAXW = 20, 1.4
UNDER_Y, UNDER_STEP = 0.65, 0.35
UNDER_COLOR = {"day before": GREEN_C, "first red day": RED_C}
LEG_Y, LEG_S, LEG_GX, LEG_RX, LEG_BUFF = -0.1, 0.35, -4.2, 0.3, 0.34   # buff: the board's x of the labels
STEP_Y = 1.72
# review row 3: J' is explained in R1 and R3, and each line is at most 10 wide.
R_LINES = ["day before: she holds a job J' she likes as much as J, or more",
           "J' was not refused, so it asks her again",
           "first red day: J' or better, so J or better"]
R_Y = [-0.9, -1.5, -2.1]
R_MAXW = 10.0
PAIR_Y, PAIR_CAP_Y, PAIR_S = -1.1, -1.9, 0.6           # scene `same`: the pairs, and the captions under them
PAIR_CAP_SIZE, NEVER_SIZE = 20, 22         # "never": row 4 of the review says size 22
FWD_X = (-4.3, -2.9)                       # the two green squares of the forward pair
BACK_X = (2.75, 4.45)                      # the green and the red square, 1.7 apart centre to centre (row 4)
PAIR_MID = {k: (a + b) / 2 for k, (a, b) in (("fwd", FWD_X), ("back", BACK_X))}
FWD_CAP_W, BACK_CAP_W = 5.0, 5.4           # the widest the board allows each caption
FWD_ARROW = (-3.95, -3.25)                 # the board's Arrow((-3.95, y), (-3.25, y), buff=0)
assert DAY_X == [-5.25, -3.75, -2.25, -0.75, 0.75, 2.25, 3.75, 5.25]
assert DAY_X[DAY_BEFORE] == -0.75 and DAY_X[FIRST_RED] == 0.75       # the step arrow's two ends
assert DAY_X[0] - BOX_W / 2 > -7.0 and DAY_X[-1] + BOX_W / 2 < 7.0
assert abs((LEG_GX + LEG_S / 2 + LEG_BUFF) - (-3.685)) < 0.01        # "claim true" starts here
assert [round(v, 3) for v in PAIR_MID.values()] == [-3.6, 3.6]       # where the board puts the captions
assert FWD_X[0] + PAIR_S / 2 < FWD_ARROW[0] < FWD_ARROW[1] < FWD_X[1] - PAIR_S / 2
assert abs((BACK_X[1] - BACK_X[0]) - 1.7) < 1e-9             # row 4: 1.7 apart centre to centre
assert abs((BACK_X[1] - BACK_X[0] - PAIR_S) - 1.1) < 1e-9    # the gap "never" (0.76 wide at 22) sits in

# stage B (`least`): the number line 0 to 12, the numbers 0 to 12 on it
NL_Y, NL_LEFT, NL_RIGHT = 0.8, -6.0, 6.0
TICK_LO, TICK_HI = 0.7, 0.9
NL_LAB_Y, NL_LAB_SIZE = 0.4, 20
NL_MAX = 12
NL_X = {n: n - 6 for n in range(NL_MAX + 1)}          # the number n sits at x = n - 6
SET_Y, SET_MAXW = 2.2, 12.5
SET_Q_SIZE, SET_LIST_SIZE = 24, 26         # beat 3.1's question, and the three sets of beats 3.2 and 3.3
RES_Y, RES_SIZE = -0.5, 24
W1_Y, W1_SIZE, W2_Y, W2_SIZE = -1.4, 26, -2.1, 22
DOT_R = 0.13
# review row 2: over the numbers 0 to 10 a span line, with its words above it, and
# review row 1: the words under the red dot at 4, clear of the tick label of the line.
BELOW_Y, BELOW_TEXT_Y, BELOW_SIZE = 1.45, 1.75, 20
BELOW_MID = (NL_X[BELOW_ELEVEN[0]] + NL_X[BELOW_ELEVEN[-1]]) / 2      # over 0 to 10: x = -1
RDAY_LAB_Y, RDAY_LAB_SIZE = 0.05, 20
assert (NL_X[BELOW_ELEVEN[0]], NL_X[BELOW_ELEVEN[-1]]) == (-6, 4)     # the span covers 0 to 10
assert abs(BELOW_MID - (-1)) < 1e-9
assert [NL_X[n] for n in (0, 5, 11, 12)] == [-6, -1, 5, 6]
assert [NL_X[n] for n in SHOWN_SET] == [-1, -4, 5, 1, 2]
assert [NL_X[n] for n in SHOWN_ODDS] == [-5, -3, -1, 1, 3, 5]
assert [NL_X[n] for n in SHOWN_PRIMES] == [-4, -3, -1, 1, 5]
assert [NL_X[n] for n in RED_PICTURE] == [-2, 0]      # the red days 4 and 6 on the number line
assert sorted(SHOWN_SET, reverse=True) == [11, 8, 7, 5, 2]   # beat 3.2: the dots flash right to left
assert len(range(10, -1, -1)) == ELEVEN                # beat 3.4: eleven tick labels, 10 down to 0
assert sum(1 for n in range(NL_MAX + 1) if n in SHOWN_ODDS) == len(SHOWN_ODDS)
assert min(SHOWN_ODDS) == 1 and min(SHOWN_PRIMES) == 2       # the one green dot of each set

# stage C (`fails`): the integer line -9 to 3, the real line 0 to 1
IL_Y, IL_LEFT, IL_RIGHT = 1.2, -6.3, 6.3
IL_TICK_LO, IL_TICK_HI = IL_Y - 0.1, IL_Y + 0.1       # the board gives the ticks no height
IL_LAB_Y, IL_LAB_SIZE = 0.8, 18
INT_MIN, INT_MAX = -9, 3
IL_X = {n: n + 3 for n in range(INT_MIN, INT_MAX + 1)}   # the integer n sits at x = n + 3
SO_ON = ((-5.6, 1.75), (-6.6, 1.75))                  # the "and so on" arrow, pointing left
CTOP_Y, CTOP_SIZE, CTOP_MAXW = 2.3, 22, 12.5
RL_Y, RL_LEFT, RL_RIGHT = -1.0, -5.0, 5.0
RL_TICK_LO, RL_TICK_HI = RL_Y - 0.1, RL_Y + 0.1
RL_LAB_Y, RL_LAB_SIZE = -1.4, 22                      # row 7: the labels 0 and 1 at size 22
HALF_LAB_Y, HALF_LAB_SIZE = -0.6, 22                  # row 7: 1, 1/2, 1/4, 1/8 at size 22
HALF_DOT_R, ZERO_R = 0.11, 0.13
HALF_LABELS = ["1", "1/2", "1/4", "1/8"]              # beat 4.2: the four dots that keep a label
ZERO_NOTE_Y = -1.78                                   # row 5: the words under the open circle at zero
REAL_NOTE_Y = 1.75                                    # row 6: the words above the integer line
CBOT_Y, CBOT_SIZE, CBOT_MAXW = -2.2, 22, 12.5
RL_EDGE = 5.0
RL_X = {t: 10 * t - RL_EDGE for t in HALVES}          # the number t sits at x = 10 t - 5
# row 7: a yellow arrow from the dot at 1/2 to the dot at 1/4, its words above it.
# It stops short of each dot, and bulges up only as far as y = -0.74, clear of the
# labels at y = -0.6 (checked below).
HALF_EDGE = HALF_DOT_R + 0.04
HALF_ARROW = (RL_X[0.5] - HALF_EDGE, RL_X[0.25] + HALF_EDGE)
HALF_ARROW_ANGLE, HALF_WORD_Y = 0.5, -0.45
assert HALF_ARROW == (-0.15, -2.35)                   # the 1/2 dot is at x = 0, the 1/4 dot at -2.5
assert HALF_WORD_Y > HALF_LAB_Y and HALF_WORD_Y < HALF_LAB_Y + 0.35   # above the labels, under the set text
assert [IL_X[n] for n in NEG_INTS] == [2, 1, 0, -1, -2, -3, -4, -5, -6]
assert [IL_X[n] for n in (INT_MIN, -1, 0, INT_MAX)] == [-6, 2, 3, 6]
assert [IL_X[n] for n in (-1, -2, -3)] == [2, 1, 0]   # beat 4.1: the first three dots, leftwards
assert [IL_X[n] for n in range(-4, -10, -1)] == [-1, -2, -3, -4, -5, -6]  # then six more, leftwards
assert [IL_X[n] for n in range(4)] == [3, 4, 5, 6]    # beat 4.3: the tick labels 0 to 3
assert len(HALF_LABELS) == len(LABELLED)              # one label per dot but the last, 1/16
assert [round(RL_X[t], 3) for t in HALVES] == [5.0, 0.0, -2.5, -3.75, -4.375]
assert [round(RL_X[t], 3) for t in LABELLED] == [5.0, 0.0, -2.5, -3.75]   # each one left of the last


def fit(t, w):
    """A text is never wider than `w`: the board's width for it, or the frame's."""
    if t.width > w:
        t.scale_to_fit_width(w)
    return t


def flash(mob):
    """The board's "Flash": the object returns to the look it had."""
    return Indicate(mob, color=YELLOW_D, scale_factor=1.1)


# a green day: stroke GREEN_C width 3, fill GREEN_C 0.25; a red day the same in RED_C;
# an undecided day: stroke GREY_B width 2 and no fill.
DAY_STYLE = {"grey": (GREY_B, 2, 0.0), "green": (GREEN_C, 3, 0.25), "red": (RED_C, 3, 0.25)}


def day_rect(x, y, kind="grey", w=BOX_W, h=BOX_H):
    c, sw, fo = DAY_STYLE[kind]
    r = Rectangle(width=w, height=h, stroke_color=c, stroke_width=sw).move_to([x, y, 0])
    if fo:
        r.set_fill(c, fo)
    return r


def to_day(rect, kind):
    """Recolour a day in place, its own stroke and fill: never a second rectangle."""
    c, sw, fo = DAY_STYLE[kind]
    a = rect.animate.set_stroke(c, sw)
    return a.set_fill(c, fo) if fo else a


class Ep06WellOrdering(NarratedScene):
    """Episode 06: the improvement lemma proved backwards, and the well-ordering principle."""

    SCENES = ["hook", "same", "least", "fails"]   # the scene methods, in order

    def construct(self):
        if self.preview_only(self.SCENES):
            return
        self.title_card()
        for name in self.SCENES:
            getattr(self, name)()
        self.end_card([
            "The improvement lemma can be proved a second way: suppose it fails, take the first day "
            "on which it fails, and show that day cannot fail.",
            "That is induction told backwards: a red day never comes right after a green one.",
            "Well-Ordering Principle: every set of natural numbers that is not empty has a smallest "
            "element.",
            "The integers, the real numbers and the non-negative real numbers do not have this "
            "property.",
        ])

    # ---- pieces the scenes share
    def swap_head(self, text):
        """This scene's heading: the old one out and the new one in, in one animation."""
        new = self.heading(text)
        old = getattr(self, "head", None)
        if old is not None and old in self.mobjects:
            self.play(FadeOut(old), FadeIn(new))
        else:
            self.play(FadeIn(new))
        self.head = new

    def under_label(self, text, box, y):
        """A label centred under a day box, at the height the review gives it."""
        return fit(txt(text, UNDER_SIZE, UNDER_COLOR.get(text)), UNDER_MAXW) \
            .move_to([box.get_center()[0], y, 0])

    # ---- scene 1: suppose the lemma fails, and take the first day it fails
    def hook(self):
        self.swap_head("A second proof")
        self.top = fit(txt("the claim for one day: at its end, candidate C holds job J or a better one",
                           TOP_SIZE), TOP_MAXW).move_to([0, TOP_Y, 0])
        # one group per day: a box and its label are one thing, so an animation never
        # leaves a throwaway wrapper on the stage holding a box this scene has to keep
        self.cells = [VGroup(day_rect(x, ROW_Y),
                             fit(txt(DAY_LABELS[i], DAY_LABEL_SIZE), BOX_W - 0.2).move_to([x, ROW_Y, 0]))
                      for i, x in enumerate(DAY_X)]
        self.boxes = [c[0] for c in self.cells]
        self.blabels = [c[1] for c in self.cells]
        self.under = {"offer": self.under_label("offer", self.boxes[OFFER_DAY], UNDER_Y),
                      "day before": self.under_label("day before", self.boxes[DAY_BEFORE], UNDER_Y),
                      "first red day": self.under_label("first red day", self.boxes[FIRST_RED],
                                                        UNDER_Y - UNDER_STEP)}
        sq_g, sq_r = day_rect(LEG_GX, LEG_Y, "green", LEG_S, LEG_S), day_rect(LEG_RX, LEG_Y, "red", LEG_S, LEG_S)
        self.legend = VGroup(sq_g, fit(txt("claim true", 20), 3.0).next_to(sq_g, RIGHT, buff=LEG_BUFF),
                             sq_r, fit(txt("claim false", 20), 3.0).next_to(sq_r, RIGHT, buff=LEG_BUFF))
        self.step = CurvedArrow([DAY_X[DAY_BEFORE], STEP_Y, 0], [DAY_X[FIRST_RED], STEP_Y, 0],
                                angle=-1.2, color=YELLOW_D)
        self.rows = [fit(txt(s, 22), R_MAXW).move_to([0, y, 0]) for s, y in zip(R_LINES, R_Y)]

        self.say("Last time we proved the improvement lemma by walking forward from day to day. "
                 "Once a job has made a candidate an offer, she holds that job or a better one. "
                 "That is true at the end of that day and of every later day.",
                 FadeIn(self.top, shift=DOWN * 0.2))
        self.cue("made a candidate an offer",
                 LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in self.cells], lag_ratio=0.12),
                 FadeIn(self.under["offer"]))
        self.cue("every later day",
                 LaggedStart(*[flash(b) for b in self.boxes[1:]], lag_ratio=0.12))

        self.say("Here is a different way to prove the same thing. On the day of the offer itself "
                 "the claim is true, because she keeps the best of her offers and this job is among "
                 "them. So let us paint that day green.",
                 FadeIn(self.legend))
        self.cue("the claim is true", flash(self.boxes[OFFER_DAY]))
        self.cue("paint that day green", to_day(self.boxes[OFFER_DAY], "green"))

        self.say("Now suppose the lemma were false. Then on some later days the claim fails, so let "
                 "us paint those days red, wherever they may be. Among the red days, look at the "
                 "first one.",
                 flash(self.top))
        self.cue("paint those days red", *[to_day(self.boxes[i], "red") for i in RED_PICTURE])
        self.cue("the first one", flash(self.boxes[FIRST_RED]), FadeIn(self.under["first red day"]))

        self.say("The first red day is not the day of the offer, because that day is green. So there "
                 "is a day just before it, and that day is not red, because then ours would not be "
                 "the first. The claim is true on the day before.",
                 flash(self.boxes[OFFER_DAY]), flash(self.boxes[FIRST_RED]))
        self.cue("a day just before it", flash(self.boxes[DAY_BEFORE]), FadeIn(self.under["day before"]))
        self.cue("is not red", flash(self.boxes[LATER_RED]))
        self.play(flash(self.boxes[DAY_BEFORE]))
        self.cue("true on the day before", to_day(self.boxes[DAY_BEFORE], "green"))

        self.say("So on the day before, she holds a job at least as good as the original one. She did "
                 "not refuse that job, so by the step from last time it asks her again on the red "
                 "day. Then she keeps it or something better, which makes the claim true on the red "
                 "day.")
        self.cue("at least as good", FadeIn(self.rows[0]))
        self.cue("asks her again", Create(self.step), FadeIn(self.rows[1]))
        self.cue("keeps it or something better", FadeIn(self.rows[2]))
        self.cue("true on the red day", self.boxes[FIRST_RED].animate.set_stroke(GREEN_C, 6))

        self.say("But a day cannot be red and green at once, so the first red day does not exist. "
                 "And if there is no first red day, there are no red days at all. So the lemma "
                 "holds, and we have proved it a second time.",
                 flash(self.boxes[FIRST_RED]))
        self.cue("does not exist", to_day(self.boxes[FIRST_RED], "green"),
                 FadeOut(self.under["first red day"]))
        self.cue("no red days at all", to_day(self.boxes[LATER_RED], "green"),
                 LaggedStart(*[to_day(self.boxes[i], "green") for i in UNDECIDED_AFTER], lag_ratio=0.3))
        self.cue("a second time", flash(self.top))

        self.hold()
        # the board's end of scene: remove the reasoning lines, the step arrow and the
        # under-labels. Named one by one, not clear_stage(): the top text, the day row,
        # the legend and the heading have to stay for scene `same`.
        self.play(*[FadeOut(m) for m in [*self.rows, self.step,
                                         self.under["offer"], self.under["day before"]]], run_time=0.8)

    # ---- scene 2: the two proofs are one argument, told in two directions
    def same(self):
        self.swap_head("One proof, two directions")
        f_sq = VGroup(*[day_rect(x, PAIR_Y, "green", PAIR_S, PAIR_S) for x in FWD_X])
        f_ar = Arrow([FWD_ARROW[0], PAIR_Y, 0], [FWD_ARROW[1], PAIR_Y, 0], buff=0)
        f_cap = fit(txt("forwards: green today, so green tomorrow", PAIR_CAP_SIZE),
                    FWD_CAP_W).move_to([PAIR_MID["fwd"], PAIR_CAP_Y, 0])
        self.fwd = VGroup(f_sq, f_ar, f_cap)
        b_sq = VGroup(day_rect(BACK_X[0], PAIR_Y, "green", PAIR_S, PAIR_S),
                      day_rect(BACK_X[1], PAIR_Y, "red", PAIR_S, PAIR_S))
        b_word = txt("never", NEVER_SIZE, YELLOW_D).move_to([PAIR_MID["back"], PAIR_Y, 0])
        b_cap = fit(txt("backwards: no red day right after a green day", PAIR_CAP_SIZE),
                    BACK_CAP_W).move_to([PAIR_MID["back"], PAIR_CAP_Y, 0])
        self.back = VGroup(b_sq, b_word, b_cap)
        self.caps = VGroup(f_cap, b_cap)

        self.say("Is this a new kind of proof? Both proofs begin by checking the day of the offer. "
                 "And both do the same work in the middle, which is to show that a green day is "
                 "never followed by a red one.")
        self.cue("the day of the offer", flash(self.boxes[OFFER_DAY]))
        self.cue("never", FadeIn(self.back, shift=UP * 0.2))

        self.say("Induction tells it forwards, where green today forces green tomorrow, so the green "
                 "runs on forever. The second proof tells it backwards, where a first red day would "
                 "need a green day right before it. It is one argument told in two directions.")
        self.cue("green today forces green tomorrow", FadeIn(self.fwd, shift=UP * 0.2))
        self.cue("runs on forever",
                 LaggedStart(*[flash(b) for b in self.boxes], lag_ratio=0.12))
        self.cue("a first red day would need", flash(self.back))
        self.cue("two directions", flash(self.caps))

        self.hold()
        self.clear_stage()

    # ---- scene 3: the well-ordering principle, and why the notion of a first red day is valid
    def least(self):
        self.swap_head("The smallest element")
        nl = Line([NL_LEFT, NL_Y, 0], [NL_RIGHT, NL_Y, 0])
        ticks = VGroup(*[Line([NL_X[n], TICK_LO, 0], [NL_X[n], TICK_HI, 0])
                         for n in range(NL_MAX + 1)])
        self.tlabel = {n: txt(str(n), NL_LAB_SIZE).move_to([NL_X[n], NL_LAB_Y, 0])
                       for n in range(NL_MAX + 1)}
        self.axis = VGroup(nl, ticks, *self.tlabel.values())
        qtext = fit(txt("does every set of natural numbers have a smallest element?", SET_Q_SIZE),
                    SET_MAXW).move_to([0, SET_Y, 0])
        s_set = fit(txt("{5, 2, 11, 7, 8}", SET_LIST_SIZE), SET_MAXW).move_to([0, SET_Y, 0])
        s_odd = fit(txt("the odd numbers: 1, 3, 5, 7, ...", SET_LIST_SIZE), SET_MAXW).move_to([0, SET_Y, 0])
        s_prime = fit(txt("the primes: 2, 3, 5, 7, 11, ...", SET_LIST_SIZE), SET_MAXW).move_to([0, SET_Y, 0])
        # review row 1: on "Our red days" the set text names the red days, in red
        s_red = fit(txt("the red days: 4, 6, ...", SET_LIST_SIZE, RED_C), SET_MAXW).move_to([0, SET_Y, 0])
        r_set = txt("smallest element: 2", RES_SIZE, GREEN_C).move_to([0, RES_Y, 0])
        r_odd = txt("smallest element: 1", RES_SIZE, GREEN_C).move_to([0, RES_Y, 0])
        r_prime = txt("smallest element: 2", RES_SIZE, GREEN_C).move_to([0, RES_Y, 0])
        # review rows 1 and 2: the words under the red dot at 4, and the span over 0 to 10
        rday = txt("first red day", RDAY_LAB_SIZE, RED_C).move_to([NL_X[FIRST_RED], RDAY_LAB_Y, 0])
        below = Line([NL_X[BELOW_ELEVEN[0]], BELOW_Y, 0], [NL_X[BELOW_ELEVEN[-1]], BELOW_Y, 0],
                     color=YELLOW_D, stroke_width=5)
        below_txt = txt("only these lie below 11", BELOW_SIZE, YELLOW_D).move_to([BELOW_MID, BELOW_TEXT_Y, 0])
        w1 = txt("Well-Ordering Principle", W1_SIZE, YELLOW_D).move_to([0, W1_Y, 0])
        w2 = fit(txt("a set of natural numbers that is not empty has a smallest element", W2_SIZE),
                 SET_MAXW).move_to([0, W2_Y, 0])
        # one dot per number, the smallest of the set in green
        def dot(n, color=BLUE_C):
            return Dot([NL_X[n], NL_Y, 0], radius=DOT_R, color=color)
        d_red = {n: dot(n, RED_C) for n in RED_PICTURE}
        d_set = {n: dot(n) for n in SHOWN_SET}
        d_odd = {n: dot(n, GREEN_C if n == min(SHOWN_ODDS) else BLUE_C) for n in SHOWN_ODDS}
        d_prime = {n: dot(n, GREEN_C if n == min(SHOWN_PRIMES) else BLUE_C) for n in SHOWN_PRIMES}

        self.say("But the backward telling leaned on something we never proved. We said, look at "
                 "the first red day. Why should a set of days have a first one at all?",
                 FadeIn(self.axis))
        self.cue("the first red day", *[FadeIn(d) for d in d_red.values()])
        self.play(flash(d_red[FIRST_RED]))
        self.cue("a first one at all", FadeIn(qtext))

        self.say("Days are counted with natural numbers, so let us try it with numbers. Take the "
                 "set five, two, eleven, seven and eight. Its smallest element is two, and in a "
                 "finite set we can always find it by comparing.",
                 *[FadeOut(d) for d in d_red.values()])
        self.cue("five, two, eleven, seven and eight",
                 FadeOut(qtext), FadeIn(s_set),
                 LaggedStart(*[FadeIn(d_set[n]) for n in SHOWN_SET], lag_ratio=0.15))
        self.cue("smallest element is two", d_set[min(SET5)].animate.set_color(GREEN_C), FadeIn(r_set))
        self.cue("by comparing", *[flash(d_set[n]) for n in sorted(SHOWN_SET, reverse=True)])

        self.say("Infinite sets work just as well. The odd numbers never end, but they start at "
                 "one. The primes never end, but they start at two.",
                 *[FadeOut(d_set[n]) for n in SHOWN_SET])
        # review row 8: the old set text and the result text go out first (0.4 s), then
        # the new set text comes in: never two set texts on top of each other.
        self.cue("The odd numbers", FadeOut(s_set, run_time=0.4), FadeOut(r_set, run_time=0.4))
        self.cue("The odd numbers",
                 FadeIn(s_odd), FadeIn(r_odd),
                 LaggedStart(*[FadeIn(d_odd[n]) for n in SHOWN_ODDS], lag_ratio=0.15))
        self.cue("The primes", *[FadeOut(d_odd[n]) for n in SHOWN_ODDS],
                 FadeOut(s_odd, run_time=0.4), FadeOut(r_odd, run_time=0.4))
        self.cue("The primes",
                 FadeIn(s_prime), FadeIn(r_prime),
                 LaggedStart(*[FadeIn(d_prime[n]) for n in SHOWN_PRIMES], lag_ratio=0.15))

        self.say("Here is why it cannot fail. Pick any element of the set, say eleven, and only "
                 "finitely many natural numbers lie below it. So we can check them one by one, and "
                 "the lowest one that belongs to the set is the smallest.")
        self.cue("say eleven", d_prime[ELEVEN].animate.set_color(YELLOW_D))
        self.cue("finitely many", Create(below), FadeIn(below_txt),
                 *[flash(self.tlabel[n]) for n in range(10, -1, -1)])
        self.cue("the lowest one", flash(d_prime[min(SHOWN_PRIMES)]))

        self.say("This fact is called the well ordering principle. Every set of natural numbers "
                 "that is not empty has a smallest element. Our red days were such a set, not "
                 "empty because we supposed the lemma false, and so a first red day had to exist.",
                 FadeOut(below), FadeOut(below_txt))
        self.cue("well ordering principle", FadeIn(w1))
        self.cue("has a smallest element", FadeIn(w2))
        self.cue("Our red days", *[FadeOut(d_prime[n]) for n in SHOWN_PRIMES],
                 FadeOut(s_prime), FadeOut(r_prime), FadeIn(s_red),
                 *[FadeIn(d_red[n]) for n in RED_PICTURE])
        self.cue("a first red day", flash(d_red[FIRST_RED]), FadeIn(rday))

        self.hold()
        self.clear_stage()

    # ---- scene 4: not every kind of number has a smallest element
    def fails(self):
        self.swap_head("Not every kind of number")
        il_ticks = VGroup(*[Line([IL_X[n], IL_TICK_LO, 0], [IL_X[n], IL_TICK_HI, 0])
                            for n in range(INT_MIN, INT_MAX + 1)])
        self.ilabel = {n: txt(str(n), IL_LAB_SIZE).move_to([IL_X[n], IL_LAB_Y, 0])
                       for n in range(INT_MIN, INT_MAX + 1)}
        self.iline = VGroup(Line([IL_LEFT, IL_Y, 0], [IL_RIGHT, IL_Y, 0]), il_ticks,
                            *self.ilabel.values())
        self.so_on = Arrow([SO_ON[0][0], SO_ON[0][1], 0], [SO_ON[1][0], SO_ON[1][1], 0],
                           buff=0, color=RED_C)
        d_neg = {n: Dot([IL_X[n], IL_Y, 0], radius=DOT_R, color=RED_C) for n in NEG_INTS}
        t_plain = fit(txt("the set of all negative integers", CTOP_SIZE), CTOP_MAXW).move_to([0, CTOP_Y, 0])
        t_red = fit(txt("the set of all negative integers: no smallest element", CTOP_SIZE, RED_C),
                    CTOP_MAXW).move_to([0, CTOP_Y, 0])
        rl_ticks = VGroup(*[Line([x, RL_TICK_LO, 0], [x, RL_TICK_HI, 0])
                            for x in (RL_LEFT, RL_RIGHT)])
        rl_labels = VGroup(*[txt(s, RL_LAB_SIZE).move_to([x, RL_LAB_Y, 0])
                             for s, x in (("0", RL_LEFT), ("1", RL_RIGHT))])
        self.rline = VGroup(Line([RL_LEFT, RL_Y, 0], [RL_RIGHT, RL_Y, 0]), rl_ticks, rl_labels)
        # zero, and not in the set. `color` is not decoration here: Circle's own
        # default colour is RED in this Manim, and a red circle at zero would read
        # as "zero is in the set", the opposite of the board's white open circle.
        # review row 5: the circle is filled with the background, at opacity 1, and
        # added after the real line (in beat 4.3), so the ring covers the tick at zero.
        self.ring = Circle(radius=ZERO_R, color=WHITE, fill_color=BG,
                           fill_opacity=1).move_to([RL_LEFT, RL_Y, 0])
        self.ring_note = txt("0 is not positive: not in the set", 20).move_to([RL_LEFT, ZERO_NOTE_Y, 0])
        # review row 6: the reals hold the same dots
        self.real_note = fit(txt("the real numbers contain these dots too", 22, RED_C),
                             CTOP_MAXW).move_to([0, REAL_NOTE_Y, 0])
        h_dots = {t: Dot([RL_X[t], RL_Y, 0], radius=HALF_DOT_R, color=BLUE_C) for t in HALVES}
        h_lab = {t: txt(s, HALF_LAB_SIZE).move_to([RL_X[t], HALF_LAB_Y, 0])
                 for t, s in zip(LABELLED, HALF_LABELS)}
        # review row 7: from the dot at 1/2 to the dot at 1/4, its word above the arrow
        self.half_arrow = CurvedArrow([HALF_ARROW[0], RL_Y, 0], [HALF_ARROW[1], RL_Y, 0],
                                      angle=HALF_ARROW_ANGLE, color=YELLOW_D)
        self.half_word = txt("half", 20, YELLOW_D).move_to([(HALF_ARROW[0] + HALF_ARROW[1]) / 2,
                                                            HALF_WORD_Y, 0])
        cbot = fit(txt("the set of all positive real numbers: no smallest element", CBOT_SIZE, RED_C),
                   CBOT_MAXW).move_to([0, CBOT_Y, 0])

        self.say("Other number systems are not so kind. Take the integers, which include the negative "
                 "numbers, and look at the set of all negative ones. Below minus one comes minus two, "
                 "then minus three, and it never ends, so this set has no smallest element.",
                 FadeIn(self.iline))
        self.cue("all negative ones", FadeIn(t_plain),
                 LaggedStart(*[FadeIn(d_neg[n]) for n in (-1, -2, -3)], lag_ratio=0.3))
        self.cue("it never ends",
                 LaggedStart(*[FadeIn(d_neg[n]) for n in range(-4, -10, -1)], lag_ratio=0.2),
                 FadeIn(self.so_on))
        self.cue("no smallest element", FadeOut(t_plain), FadeIn(t_red))

        self.say("The real numbers contain that same set, so they fail too. What if we only allow zero "
                 "and everything above it? Then look at the set of all positive numbers. Whatever "
                 "positive number you call the smallest, half of it is smaller and still positive.",
                 LaggedStart(*[flash(d_neg[n]) for n in NEG_INTS], lag_ratio=0.1))
        self.cue("contain that same set", FadeIn(self.real_note))
        self.cue("zero and everything above it", FadeIn(self.rline))
        self.cue("all positive numbers", FadeIn(h_dots[1.0]), FadeIn(h_lab[1.0]))
        self.cue("half of it",
                 LaggedStart(*[FadeIn(m) for t in LABELLED[1:] for m in (h_dots[t], h_lab[t])]
                             + [FadeIn(h_dots[HALVES[-1]])], lag_ratio=0.3),
                 Create(self.half_arrow), FadeIn(self.half_word))

        self.say("Zero would be below them all, but zero is not positive, so it is not in the set. So "
                 "first counterexamples belong to the natural numbers, and to things counted by them, "
                 "like our days. Next we use the improvement lemma to show that the result of propose "
                 "and reject is stable.",
                 FadeIn(self.ring), FadeOut(self.real_note))
        self.cue("not in the set", FadeIn(cbot), FadeIn(self.ring_note))
        self.cue("first counterexamples", *[flash(self.ilabel[n]) for n in range(4)])
        self.cue("is stable", flash(cbot), flash(t_red))

        self.hold()
        # nothing is removed here: the board hands the stage to the end card as it is
