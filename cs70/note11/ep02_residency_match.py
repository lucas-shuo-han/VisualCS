"""CS70 Note 11, episode 02: the residency match, and the road that led to it.

Built from BOARD-ep02.md: every `> ` line of the board is one say() below, copied
unchanged, and the picture is built as the board's stage lines describe.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---------------------------------------------------------------- FACTS
# The board's "Facts" table. Every number the episode shows or says is computed here
# and asserted; the picture reads these names and never a typed-in value.
N_SLOTS, N_GRADS, N_HOSP = 5, 3, 3
DECADE_40S, EARLY_50S, NRMP_START, NOBEL = 1940, 1950, 1952, 2012
MID_40S = DECADE_40S + 5                       # "the middle of the nineteen forties"
YEARS_LATER = NOBEL - NRMP_START               # F10
D_MID_40S = f"mid-{DECADE_40S}s"               # the date in strip slot D of scene 2
D_EARLY_50S = f"early {EARLY_50S}s"            # the date in scene 4
D_1952, D_2012 = str(NRMP_START), str(NOBEL)
NOBEL_LINE = f"Shapley and Roth, Nobel Prize {NOBEL}"

assert (N_SLOTS, N_GRADS, N_HOSP) == (5, 3, 3)              # five slots, three graduates, three hospitals
assert N_SLOTS - N_GRADS == 2                              # the slots at x = -4 and x = 4 have no graduate
assert N_GRADS == N_HOSP == 3                              # a matching of three pairs in scene 4
assert MID_40S == 1945 and EARLY_50S + 2 == NRMP_START     # "nineteen fifty-two" is early in the fifties
assert YEARS_LATER == 60                                   # "Sixty years later" (F10)
assert (D_MID_40S, D_EARLY_50S, D_1952, D_2012) == ("mid-1940s", "early 1950s", "1952", "2012")

# ---------------------------------------------------------------- the board's stage one
TL_X = [-4.8, -2.4, 0.0, 2.4, 5.0]             # the five timeline boxes, left to right
TL_LABEL = ["first year", "sophomore", "junior", "senior", "residency"]
TL_Y, TL_W, TL_H = 1.9, 2.2, 0.7
CAP_XY = (-1.2, 2.5)                           # the "medical school" caption
OFFER_Y0, OFFER_Y1, OFFER_LY = 0.75, 1.5, 0.5  # the offer marker's arrow and its word
SLOT_X = [-4, -2, 0, 2, 4]
SLOT_Y, SLOT_S = -0.7, 0.7
GRAD_X = [-2, 0, 2]
GRAD_Y, GRAD_R = -2.2, 0.35
STRIP_X = -6.0
SLOT_T_Y, SLOT_D_Y = -1.45, 1.0
STRIP_W = 1.4                                  # every text of the left strip
V1 = [-2, -1.1, 0], [-2, -1.8, 0]              # the three white arrows of beat 2.2
V2 = [0, -1.1, 0], [0, -1.8, 0]
V3 = [2, -1.1, 0], [2, -1.8, 0]
H1 = [-1.8, -1.1, 0], [-0.2, -1.8, 0]          # the arrows of scene 3
H2 = [-3.8, -1.1, 0], [-2.2, -1.8, 0]          # slot at -4 to the graduate at -2
H3 = [3.8, -1.1, 0], [2.2, -1.8, 0]            # slot at 4 to the graduate at 2
W_LINE = [0.25, -1.95, 0], [1.75, -1.1, 0]     # the dashed arrow of beats 3.2 and 3.3
W_SLOT_IX = SLOT_X.index(2)                    # "a hospital she likes more": the free slot at x = 2
BAR = [1.2, 1.45, 0], [1.2, 2.35, 0]           # the red bar between "junior" and "senior"
SOPH = [-2.4, 0.75, 0], [-2.4, 1.5, 0]         # the dashed arrow under "sophomore"
DASH_W, DASH_LEN, TIP_LEN = 5, 0.15, 0.25      # every dashed line of this episode

# ---------------------------------------------------------------- the board's stage two
HX, GX2 = -3.5, 3.5                            # the two columns of scene 4
ROW_Y = [0.2, -1.0, -2.2]                      # hospital 1 to 3 and graduate 1 to 3, from the top
CAP2_Y = 0.95                                  # the two column captions
BOX_XY = (0.0, 1.6)                            # the centre box, 3.6 wide and 1.2 high
NRMP_Y, PROP_Y = 1.82, 1.32                    # its two lines
DATE_XY, WORD_XY = (-5.8, 1.6), (-5.8, -1.0)
TOP_XY = (0.0, 2.48)
L1 = [-3.1, 0.2, 0], [3.1, -1.0, 0]            # hospital 1 - graduate 2
L2 = [-3.1, -1.0, 0], [3.1, 0.2, 0]            # hospital 2 - graduate 1
L3 = [-3.1, -2.2, 0], [3.1, -2.2, 0]           # hospital 3 - graduate 3
D_LINE = [-3.1, 0.2, 0], [3.1, 0.2, 0]         # hospital 1 - graduate 1: the pair at first
G2_LINE = [-3.1, -1.0, 0], [3.1, -1.0, 0]      # the second green line
ICON_W, ICON_H = 0.35, 0.45                    # the list icons flying into the centre box
ICON_XY = [0.0, 1.0, 0]


def fit(t, w):
    """A text no wider than `w`: the board's rule for a word inside a box."""
    if t.width > w:
        t.scale_to_fit_width(w)
    return t


def strip_text(s, size=22, color=GREY_B):
    return fit(txt(s, size, color), STRIP_W)


def flash(mob):
    return Indicate(mob, color=YELLOW_D, scale_factor=1.1)


def arrow(a, b, color=WHITE):
    return Arrow(a, b, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.12, color=color)


def line(a, b, color=WHITE, width=4):
    return Line(a, b, stroke_color=color, stroke_width=width)


def dashed(a, b, color, tip=False):
    """The board's one dashed style: width 5 and dash length 0.15, in a light colour
    (white, YELLOW_D or ORANGE, never grey); with a tip when it stands for an arrow."""
    ln = DashedLine(a, b, color=color, stroke_width=DASH_W, dash_length=DASH_LEN)
    if tip:
        ln.add_tip(tip_length=TIP_LEN)
    return ln


class Ep02ResidencyMatch(NarratedScene):
    """Episode 02: why the residency match needed propose and reject."""

    SCENES = ["hook", "race", "fuse", "match"]

    def construct(self):
        if self.preview_only(self.SCENES):
            return
        self.title_card()
        for name in self.SCENES:
            getattr(self, name)()
        self.end_card([
            "More residency slots than graduates pushed hospitals to make offers earlier and "
            "earlier, then with deadlines of a few hours.",
            "In the early nineteen fifties one central program took ranked lists from both sides, "
            "but its first pairings were not stable.",
            "In nineteen fifty-two it switched to propose and reject, which gives a stable matching.",
            "In twenty twelve Shapley and Roth received the Nobel Prize in economics for work that "
            "extends the algorithm.",
        ])

    # -- stage one: the timeline, the slots, the graduates, the left strip
    def stage1(self):
        """The board's stage one. Nothing is added here; the beats fade the parts in."""
        self.school = VGroup(*[Rectangle(width=TL_W, height=TL_H, stroke_color=GREY_B, stroke_width=2)
                               .move_to([x, TL_Y, 0]) for x in TL_X[:4]])
        self.school_lab = VGroup(*[fit(txt(lab, 22), TL_W - 0.4).move_to([x, TL_Y, 0])
                                   for lab, x in zip(TL_LABEL[:4], TL_X[:4])])
        self.sboxes = [VGroup(b, l) for b, l in zip(self.school, self.school_lab)]
        self.res_box = Rectangle(width=TL_W, height=TL_H, stroke_color=BLUE_C, stroke_width=2,
                                 fill_color=BLUE_C, fill_opacity=0.15).move_to([TL_X[4], TL_Y, 0])
        self.res_lab = fit(txt(TL_LABEL[4], 22), TL_W - 0.4).move_to([TL_X[4], TL_Y, 0])
        self.res = VGroup(self.res_box, self.res_lab)
        self.cap = txt("medical school", 20, GREY_B).move_to([CAP_XY[0], CAP_XY[1], 0])
        self.slots = VGroup(*[Square(SLOT_S, stroke_color=BLUE_C, stroke_width=3, fill_color=BLUE_C,
                                     fill_opacity=0.15).move_to([x, SLOT_Y, 0]) for x in SLOT_X])
        self.grads = VGroup(*[Circle(GRAD_R, stroke_color=GOLD_C, stroke_width=3, fill_color=GOLD_C,
                                     fill_opacity=0.15).move_to([x, GRAD_Y, 0]) for x in GRAD_X])
        self.lab_slots = strip_text("slots").move_to([STRIP_X, SLOT_Y, 0])
        self.lab_grads = strip_text("graduates").move_to([STRIP_X, GRAD_Y, 0])

    def swap_slot(self, attr, s, size=20, color=C_TEXT, strip=False):
        """A slot's text changes: the old word out and the new one in at the same place,
        in one animation (the board's rule for a slot whose text changes)."""
        old = getattr(self, attr)
        new = (strip_text if strip else txt)(s, size, color).move_to(old.get_center())
        setattr(self, attr, new)
        return FadeOut(old), FadeIn(new)

    def marker(self, x):
        """The offer marker at x: its arrow and its word, which move together along x."""
        return VGroup(Arrow([x, OFFER_Y0, 0], [x, OFFER_Y1, 0], buff=0, color=YELLOW_D,
                            stroke_width=5),
                      txt("offer", 20, YELLOW_D).move_to([x, OFFER_LY, 0]))

    # ---- scene 1: the situation, and what the episode is about
    def hook(self):
        self.head1 = self.heading("Who gets which hospital?")
        self.play(FadeIn(self.head1))
        self.stage1()

        self.say("Every year, medical students who finish school need a place at a teaching "
                 "hospital, which is called a residency. So on one side there are residency "
                 "slots, and on the other side there are graduates.",
                 FadeIn(self.cap),
                 LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in self.sboxes], lag_ratio=0.25))
        self.cue("is called a residency", FadeIn(self.res, shift=UP * 0.2))
        self.cue("residency slots", FadeIn(self.slots), FadeIn(self.lab_slots))
        self.cue("there are graduates", FadeIn(self.grads), FadeIn(self.lab_grads))

        self.v1, self.v2, self.v3 = (arrow(*V1, color=GREEN_C), arrow(*V2, color=GREEN_C),
                                     arrow(*V3, color=GREEN_C))
        self.say("This is the matching problem of the last episode, with hospitals in the place "
                 "of jobs and graduates in the place of candidates. Today a computer takes "
                 "ranked lists from both sides and runs propose and reject on them. But the road "
                 "there was long, and each failed attempt shows why the algorithm is built as it is.")
        self.cue("hospitals in the place of jobs", flash(self.slots))
        self.cue("graduates in the place", flash(self.grads))
        self.cue("runs propose and reject",
                 LaggedStart(GrowArrow(self.v1), GrowArrow(self.v2), GrowArrow(self.v3),
                             lag_ratio=0.3))
        self.cue("each failed attempt",
                 LaggedStart(*[flash(g) for g in self.sboxes], lag_ratio=0.3))
        self.hold()
        self.play(FadeOut(self.v1), FadeOut(self.v2), FadeOut(self.v3))
        self.v1 = self.v2 = self.v3 = None

    # ---- scene 2: why the offers crept earlier, and how the race was stopped
    def race(self):
        head = self.heading("Earlier and earlier")
        self.play(FadeOut(self.head1), FadeIn(head))
        self.head1 = head

        self.say("Residencies began about a century ago, and hospitals liked them, because an "
                 "intern is cheap labour. Soon there were more slots than graduates to fill them.",
                 flash(self.res))
        self.cue("cheap labour", flash(self.slots))
        self.cue("more slots than graduates",
                 self.slots[0].animate.set_stroke(RED_C, 4),
                 self.slots[4].animate.set_stroke(RED_C, 4))

        self.v1, self.v2, self.v3 = arrow(*V1), arrow(*V2), arrow(*V3)
        self.mk = self.marker(2.4)             # it appears at x = 3.3 and slides to x = 2.4
        self.say("Now think like one of these hospitals, which does not want to be left with an "
                 "empty slot. If it waits, the graduates it wants may already have said yes to "
                 "another hospital. So the safe move is to make its offer a little earlier than "
                 "everybody else.",
                 flash(self.slots[0]))
        self.cue("If it waits",
                 LaggedStart(GrowArrow(self.v1), GrowArrow(self.v2), GrowArrow(self.v3),
                             lag_ratio=0.3))
        self.cue("a little earlier", FadeIn(self.mk, shift=RIGHT * 0.9))

        self.slot_d = strip_text(D_MID_40S, 24).move_to([STRIP_X, SLOT_D_Y, 0])
        self.soph = dashed(*SOPH, color=YELLOW_D, tip=True)
        self.say("But every hospital thinks the same way, so the offers crept earlier year after "
                 "year. By the middle of the nineteen forties they arrived at the beginning of "
                 "the junior year, two years before graduation. Some hospitals were even thinking "
                 "about asking sophomores.",
                 self.mk.animate.shift(LEFT * 1.0))                    # 2.4 -> 1.4
        self.cue("nineteen forties", FadeIn(self.slot_d))
        self.cue("beginning of the junior year", self.mk.animate.shift(LEFT * 2.4))   # 1.4 -> -1.0
        self.cue("two years before graduation", flash(self.sboxes[2]), flash(self.sboxes[3]))
        self.cue("asking sophomores", FadeIn(self.soph), flash(self.sboxes[1]))

        self.bar = line(*BAR, color=RED_C, width=6)
        self.say("An offer that early is a bet on a student the hospital hardly knows yet. So the "
                 "American Medical Association stepped in, and told the schools to keep "
                 "transcripts and reference letters locked up until the senior year. Without "
                 "those papers an early offer had nothing to stand on, and the race to be first "
                 "was over.",
                 flash(self.mk))
        self.cue("American Medical Association", FadeIn(self.bar))
        self.cue("locked up until the senior year",
                 *[g.animate.set_opacity(0.3) for g in self.sboxes[:3]])
        self.cue("the race to be first was over", FadeOut(self.soph),
                 self.mk.animate.shift(RIGHT * 3.4))                   # -1.0 -> 2.4
        self.soph = None

        self.hold()
        self.play(FadeOut(self.v1), FadeOut(self.v2), FadeOut(self.v3), FadeOut(self.slot_d),
                  self.slots[0].animate.set_stroke(BLUE_C, 3),
                  self.slots[4].animate.set_stroke(BLUE_C, 3))
        self.v1 = self.v2 = self.v3 = self.slot_d = None

    # ---- scene 3: the deadline, and what it takes away from the graduate
    def fuse(self):
        head = self.heading("A few hours to decide")
        self.play(FadeOut(self.head1), FadeIn(head))
        self.head1 = head

        self.h1 = arrow(*H1)
        self.h2, self.h3 = arrow(*H2, color=GREY_B), arrow(*H3, color=GREY_B)
        self.slot_t = strip_text("a few hours", 20, ORANGE).move_to([STRIP_X, SLOT_T_Y, 0])
        self.say("But now every hospital was making its offers in the same short season. A "
                 "hospital whose offer sat unanswered could lose its second and third choices to "
                 "other hospitals in the meantime. So hospitals attached a deadline to every "
                 "offer, and in the end a student had only a few hours to say yes or no.",
                 flash(self.sboxes[3]), flash(self.mk))
        self.cue("sat unanswered", GrowArrow(self.h1))
        self.cue("second and third choices", GrowArrow(self.h2), GrowArrow(self.h3))
        self.cue("only a few hours", self.h1.animate.set_color(ORANGE), FadeIn(self.slot_t))

        self.w_line = dashed(*W_LINE, color=WHITE, tip=True)
        self.say("Now look at it from the side of the graduate. She has an offer in front of her, "
                 "and a hospital she likes more has not answered yet. With a few hours on the "
                 "clock she must take it or risk ending up with nothing.",
                 flash(self.grads[1]))
        self.cue("an offer in front of her", flash(self.h1))
        self.cue("a hospital she likes more", self.slots[W_SLOT_IX].animate.set_stroke(YELLOW_D, 4),
                 FadeIn(self.w_line))
        self.cue("take it or risk", flash(self.h1))

        self.say("Compare that with the candidates in the last episode, who could answer maybe "
                 "and keep an offer in hand while better ones arrived. The short deadline took "
                 "exactly that answer away. So the missing piece was a way to hold an offer "
                 "without closing the door.")
        self.cue("keep an offer in hand",
                 self.h1.animate.set_color(GREEN_C).set_stroke(width=8),
                 *self.swap_slot("slot_t", "in hand", 20, GREEN_C, strip=True))
        self.play(Indicate(self.h1, color=GREEN_C))       # the one flash, as H1 turns green
        self.cue("took exactly that answer away",
                 self.h1.animate.set_color(ORANGE).set_stroke(width=4),
                 *self.swap_slot("slot_t", "a few hours", 20, ORANGE, strip=True))
        self.cue("without closing the door", flash(self.w_line), flash(self.slots[W_SLOT_IX]))
        self.hold()
        self.clear_stage(self.head1)
        self.h1 = self.h2 = self.h3 = self.w_line = self.mk = None

    # ---- scene 4: the central system, the pair it could not stop, and the Nobel Prize
    def match(self):
        head = self.heading("One central system")
        self.play(FadeOut(self.head1), FadeIn(head))
        self.head1 = head

        self.nrmp_box = RoundedRectangle(corner_radius=0.12, width=3.6, height=1.2,
                                         stroke_color=GREY_B, stroke_width=3
                                         ).move_to([BOX_XY[0], BOX_XY[1], 0])
        self.nrmp_lab = txt("N.R.M.P.", 26).move_to([BOX_XY[0], NRMP_Y, 0])
        self.hosp = VGroup(*[Square(SLOT_S, stroke_color=BLUE_C, stroke_width=3, fill_color=BLUE_C,
                                    fill_opacity=0.15).move_to([HX, y, 0]) for y in ROW_Y])
        self.grads2 = VGroup(*[Circle(GRAD_R, stroke_color=GOLD_C, stroke_width=3, fill_color=GOLD_C,
                                      fill_opacity=0.15).move_to([GX2, y, 0]) for y in ROW_Y])
        self.cap_h = txt("hospitals", 20, GREY_B).move_to([HX, CAP2_Y, 0])
        self.cap_g = txt("graduates", 20, GREY_B).move_to([GX2, CAP2_Y, 0])
        self.date = txt(D_EARLY_50S, 24).move_to([DATE_XY[0], DATE_XY[1], 0])
        self.word = txt("stable", 22, GREEN_C).move_to([WORD_XY[0], WORD_XY[1], 0])

        h_icons = [Rectangle(width=ICON_W, height=ICON_H, stroke_color=BLUE_C, stroke_width=2,
                             fill_color=BLUE_C, fill_opacity=0.6).move_to(sq) for sq in self.hosp]
        g_icons = [Rectangle(width=ICON_W, height=ICON_H, stroke_color=GOLD_C, stroke_width=2,
                             fill_color=GOLD_C, fill_opacity=0.6).move_to(c) for c in self.grads2]

        def fly(icons):
            return LaggedStart(*[Succession(FadeIn(i), i.animate.move_to(ICON_XY), FadeOut(i))
                                 for i in icons], lag_ratio=0.25)

        self.prop = txt("propose and reject", 20, YELLOW_D).move_to([BOX_XY[0], PROP_Y, 0])
        self.say("In the early nineteen fifties this led to one central system, called the "
                 "National Residency Matching Program. Every hospital handed in a ranked list of "
                 "graduates, and every graduate handed in a ranked list of hospitals.",
                 FadeIn(self.date),
                 LaggedStart(FadeIn(self.hosp, shift=RIGHT * 0.2), FadeIn(self.cap_h),
                             lag_ratio=0.4),
                 LaggedStart(FadeIn(self.grads2, shift=LEFT * 0.2), FadeIn(self.cap_g),
                             lag_ratio=0.4))
        self.cue("National Residency Matching Program",
                 FadeIn(self.nrmp_box), FadeIn(self.nrmp_lab))
        self.cue("Every hospital handed in", fly(h_icons))
        self.cue("every graduate handed in", fly(g_icons))

        self.l1 = line(*L1)
        self.l2 = line(*L2)
        self.l3 = line(*L3)
        self.d_line = dashed(*D_LINE, color=ORANGE)
        self.g1 = line(*D_LINE, color=GREEN_C)
        self.g2 = line(*G2_LINE, color=GREEN_C)
        self.say("The program then paired everyone up from those lists. But at first its pairing "
                 "could contain a hospital and a graduate who would both rather have each other. "
                 "That is exactly the trouble we met in the last episode, and such a pair has "
                 "every reason to make a private deal again.",
                 LaggedStart(Create(self.l1), Create(self.l2), Create(self.l3), lag_ratio=0.3))
        self.cue("would both rather have each other", Create(self.d_line))
        self.cue("the trouble we met", flash(self.d_line))
        self.cue("a private deal again", self.l1.animate.set_opacity(0.3),
                 self.l2.animate.set_opacity(0.3))

        self.say("In nineteen fifty-two the program switched to propose and reject. A matching "
                 "with no such pair is called stable, and that is what the algorithm produced, so "
                 "nobody had a reason to deal privately. The offers and the answers of maybe all "
                 "happen inside the computer, and people only see the final result.",
                 *self.swap_slot("date", D_1952, 24))
        self.cue("switched to propose and reject", FadeIn(self.prop))
        self.cue("is called stable", FadeOut(self.d_line), FadeOut(self.l1), FadeOut(self.l2))
        self.play(Create(self.g1), Create(self.g2), self.l3.animate.set_color(GREEN_C),
                  FadeIn(self.word))
        self.cue("inside the computer", flash(self.nrmp_box))

        self.nobel = txt(NOBEL_LINE, 20, YELLOW_D).move_to([TOP_XY[0], TOP_XY[1], 0])
        self.say("Sixty years later, in twenty twelve, Lloyd Shapley and Alvin Roth received the "
                 "Nobel Prize in economics for work that extends this algorithm. So the word that "
                 "carried the whole story is stable. What exactly it demands of a matching is the "
                 "question of the next episode.",
                 *self.swap_slot("date", D_2012, 24))
        self.cue("Lloyd Shapley and Alvin Roth", FadeIn(self.nobel))
        self.cue("is stable", flash(self.word))
        self.cue("demands of a matching", flash(self.g1), flash(self.g2), flash(self.l3))
        self.hold()

