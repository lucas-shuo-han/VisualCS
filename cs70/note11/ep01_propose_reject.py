"""CS70 Note 11, episode 01: the propose-and-reject algorithm on three jobs and three candidates.

Built from BOARD-ep01.md: every `> ` line of the board is one say() below, copied
unchanged, and the picture is built as the board's stage lines describe.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---------------------------------------------------------------- FACTS
# The board's "Facts" table. Every name, list and number the episode shows or says is
# computed here and asserted; the picture reads these names and never a typed-in value.
JOBS = {"Approximation": ["Anita", "Bridget", "Christine"],
        "Basis": ["Bridget", "Anita", "Christine"],
        "Control": ["Anita", "Bridget", "Christine"]}
CANDS = {"Anita": ["Basis", "Approximation", "Control"],
         "Bridget": ["Approximation", "Basis", "Control"],
         "Christine": ["Approximation", "Basis", "Control"]}
EXAMPLE = {"Approximation": "Bridget", "Basis": "Christine", "Control": "Anita"}
JOB_NAMES = list(JOBS)                   # left to right on the stage
CAND_NAMES = list(CANDS)


def prefers(lists, who, a, b):           # who ranks a above b
    return lists[who].index(a) < lists[who].index(b)


# per day: (offers job -> candidate, in hand candidate -> job, rejected jobs)
DAYS = [
    ({"Approximation": "Anita", "Basis": "Bridget", "Control": "Anita"},
     {"Anita": "Approximation", "Bridget": "Basis"}, ["Control"]),
    ({"Approximation": "Anita", "Basis": "Bridget", "Control": "Bridget"},
     {"Anita": "Approximation", "Bridget": "Basis"}, ["Control"]),
    ({"Approximation": "Anita", "Basis": "Bridget", "Control": "Christine"},
     {"Anita": "Approximation", "Bridget": "Basis", "Christine": "Control"}, []),
]
RESULT = {"Approximation": "Anita", "Basis": "Bridget", "Control": "Christine"}


def run():
    """The board's procedure on the lists above: used once, to check DAYS (F12 to F15)."""
    left = {j: list(l) for j, l in JOBS.items()}
    days = []
    while True:
        offers = {j: left[j][0] for j in JOBS}
        hand, rejected = {}, []
        for c in CANDS:
            got = [j for j in JOBS if offers[j] == c]
            if got:
                best = min(got, key=CANDS[c].index)
                hand[c] = best
                rejected += [j for j in got if j != best]
        days.append((offers, hand, rejected))
        if not rejected:
            return days
        for j in rejected:
            left[j].remove(offers[j])


assert run() == DAYS and len(DAYS) == 3                          # "three days" (F15)
assert len(JOBS) == 3 and len(CANDS) == 3                        # "three companies", "three candidates"
assert {j: c for c, j in DAYS[-1][1].items()} == RESULT          # F15
assert sum(JOBS[j][0] == "Anita" for j in JOBS) == 2             # "two of the three jobs" (F5)
assert sum(1 for j in JOBS if DAYS[0][0][j] == "Anita") == 2     # day one: "Anita holds two offers"
assert sum(1 for j in JOBS if DAYS[1][0][j] == "Bridget") == 2   # day two: Bridget holds two offers
assert sum(1 for c in CANDS if c in DAYS[0][1]) == 2             # day one: two candidates hold one
assert all(sum(1 for j in JOBS if DAYS[2][0][j] == c) == 1 for c in CANDS)   # "exactly one offer"
assert DAYS[0][2] == ["Control"] and DAYS[1][2] == ["Control"]   # Control refused on day one and two
assert DAYS[2][2] == []                                          # day three: "nobody is refused"
assert prefers(JOBS, "Approximation", "Anita", "Bridget")        # F7
assert prefers(CANDS, "Anita", "Approximation", "Control") and CANDS["Anita"][-1] == "Control"   # F7
assert JOBS["Control"][-1] == "Christine" and CANDS["Christine"][-1] == "Control"                # F17
assert EXAMPLE == {"Approximation": "Bridget", "Basis": "Christine", "Control": "Anita"}         # F6

# ---------------------------------------------------------------- the board's stage
X = [-3.9, 0.5, 4.9]                     # the three columns
JOB_Y = [2.13, 1.61, 1.09]               # job cells, the first choice on top
CAND_Y = [-1.32, -1.84, -2.36]           # candidate cells
CELL_W, CELL_H = 2.2, 0.5
JOB_HY, CAND_HY = 2.70, -0.75            # the two header rows
HEAD_W_MAX = 2.0                         # a header's word, inside its 2.2 wide box
HEAD_RULE_X = -5.1                       # a heading's underline stops left of the job boxes
STRIP_X = -6.0                           # the left strip
SLOT_A_Y, SLOT_B_Y = 0.42, -0.02


def cell_row(ys, x):
    return VGroup(*[Rectangle(width=CELL_W, height=CELL_H, stroke_color=GREY_B, stroke_width=2)
                    .move_to([x, y, 0]) for y in ys])


def flash(mob):
    return Indicate(mob, color=YELLOW_D, scale_factor=1.1)


def reset(mob):
    return mob.animate.set_stroke(GREY_B, 2)


def strip_text(s, size=22, color=GREY_B):
    t = txt(s, size, color)
    if t.width > 1.4:
        t.scale_to_fit_width(1.4)
    return t


def arrow(a, b):
    return Arrow(a, b, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.12, color=WHITE)


class Ep01ProposeReject(NarratedScene):
    """Episode 01: three jobs, three candidates, three days of propose and reject."""

    SCENES = ["hook", "first_try", "days", "result"]

    def construct(self):
        if self.preview_only(self.SCENES):
            return
        self.title_card()
        for name in self.SCENES:
            getattr(self, name)()
        self.end_card([
            "Each morning every job makes an offer to the best candidate who has not refused it.",
            "Each afternoon every candidate keeps her best offer in hand and refuses the rest.",
            "Each evening a refused job crosses that candidate off, and the days stop when nobody "
            "is refused.",
            "In our example it stopped on day three with Approximation and Anita, Basis and Bridget, "
            "Control and Christine.",
        ])

    # -- the one stage every scene stands on
    def build_stage(self):
        self.lab_jobs = strip_text("jobs").move_to([STRIP_X, JOB_HY, 0])
        self.lab_cands = strip_text("candidates").move_to([STRIP_X, CAND_HY, 0])
        self.job_head = VGroup(*[box_label(n, BLUE_C, w=2.2, h=0.55, font_size=24)
                                 .move_to([x, JOB_HY, 0]) for n, x in zip(JOB_NAMES, X)])
        self.cand_head = VGroup(*[box_label(n, GOLD_C, w=2.2, h=0.55, font_size=24)
                                  .move_to([x, CAND_HY, 0]) for n, x in zip(CAND_NAMES, X)])
        for head in (*self.job_head, *self.cand_head):
            label = head[1]                 # the header's word; "Approximation" is as wide as its box
            if label.width > HEAD_W_MAX:
                label.scale_to_fit_width(HEAD_W_MAX)
        self.job_cell = [cell_row(JOB_Y, x) for x in X]
        self.cand_cell = [cell_row(CAND_Y, x) for x in X]
        self.job_names, self.cand_names = {}, {}
        self.slot_a, self.slot_b = None, None

    def heading(self, text, color=YELLOW_D):
        """The kit's heading, with its rule stopped before the job columns: the
        underline ran into the top edge of the "Approximation" header (x = -5.0)."""
        head = super().heading(text, color)
        text_mob, rule = head[0], head[1]
        x0, x1 = text_mob.get_left()[0], min(text_mob.get_right()[0], HEAD_RULE_X)
        y = rule.get_center()[1]
        rule.put_start_and_end_on([x0, y, 0], [x1, y, 0])
        return head

    def job_name_at(self, i, r):                    # the name in job column i, row r
        t = txt(JOBS[JOB_NAMES[i]][r], 22).move_to([X[i], JOB_Y[r], 0])
        self.job_names[(i, r)] = t
        return t

    def cand_name_at(self, i, r):
        t = txt(CANDS[CAND_NAMES[i]][r], 22).move_to([X[i], CAND_Y[r], 0])
        self.cand_names[(i, r)] = t
        return t

    def swap(self, attr, new):
        """Slot A or B changes: the old text out and the new one in, in one animation."""
        old = getattr(self, attr)
        setattr(self, attr, new)
        if old is None:
            return () if new is None else (FadeIn(new),)
        return (FadeOut(old),) if new is None else (FadeOut(old), FadeIn(new))

    # ---- scene 1: the two lists, and a matching that will not hold
    def hook(self):
        self.head1 = self.heading("Three jobs, three candidates")
        self.play(FadeIn(self.head1))
        self.build_stage()

        self.say("Three companies each have one job to fill, and we will call the jobs "
                 "Approximation, Basis and Control. Three candidates, Anita, Bridget and "
                 "Christine, are each looking for exactly one job.",
                 FadeIn(self.lab_jobs, shift=UP * 0.2),
                 LaggedStart(*[FadeIn(h, shift=UP * 0.2) for h in self.job_head], lag_ratio=0.2))
        self.cue("Three candidates", FadeIn(self.lab_cands, shift=DOWN * 0.2),
                 LaggedStart(*[FadeIn(h, shift=DOWN * 0.2) for h in self.cand_head], lag_ratio=0.2))

        self.say("Every job has ranked the candidates from the one it wants most to the one it wants "
                 "least. Approximation would hire Anita first, then Bridget, and Christine comes last "
                 "on its list.",
                 LaggedStart(*[FadeIn(c) for col in self.job_cell for c in col], lag_ratio=0.06))
        self.cue("hire Anita first", FadeIn(self.job_name_at(0, 0)))
        self.cue("then Bridget", FadeIn(self.job_name_at(0, 1)))
        self.cue("Christine comes last", FadeIn(self.job_name_at(0, 2)))

        self.say("Basis sees it differently, because it puts Bridget first, then Anita, then Christine. "
                 "Control has the same list as Approximation, so Anita is at the top for two of the "
                 "three jobs.",
                 LaggedStart(*[FadeIn(self.job_name_at(1, r)) for r in range(3)], lag_ratio=0.3))
        self.cue("Control has the same list",
                 LaggedStart(*[FadeIn(self.job_name_at(2, r)) for r in range(3)], lag_ratio=0.3))
        self.cue("at the top for two", flash(self.job_cell[0][0]), flash(self.job_cell[2][0]))

        self.say("The candidates have opinions too, and each of them has ranked the three jobs in the "
                 "same way. Anita likes Basis best, then Approximation, then Control, while Bridget and "
                 "Christine both put Approximation first, then Basis, then Control.",
                 LaggedStart(*[FadeIn(c) for col in self.cand_cell for c in col], lag_ratio=0.06))
        self.cue("Anita likes Basis best",
                 LaggedStart(*[FadeIn(self.cand_name_at(0, r)) for r in range(3)], lag_ratio=0.3))
        self.cue("Christine both put Approximation first",
                 LaggedStart(*[FadeIn(self.cand_name_at(i, r)) for i in (1, 2) for r in range(3)],
                             lag_ratio=0.2))

        self.m1 = Line([-3.5, 0.80, 0], [0.5, -0.45, 0], stroke_color=WHITE, stroke_width=4)
        self.m2 = Line([0.5, 0.80, 0], [4.9, -0.45, 0], stroke_color=WHITE, stroke_width=4)
        self.m3 = Line([4.9, 0.80, 0], [-3.4, -0.45, 0], stroke_color=WHITE, stroke_width=4)
        matching = txt("matching", 24).move_to([STRIP_X, SLOT_A_Y, 0])
        self.say("Our task is a matching, which means every job gets one candidate and nobody is used "
                 "twice. Here is one, where Approximation takes Bridget, Basis takes Christine, and "
                 "Control takes Anita.",
                 FadeIn(matching))
        self.slot_a = matching
        self.cue("Approximation takes Bridget", Create(self.m1))
        self.cue("Basis takes Christine", Create(self.m2))
        self.cue("Control takes Anita", Create(self.m3))

        self.d1 = DashedLine([-4.3, 0.80, 0], [-4.3, -0.45, 0], color=ORANGE, stroke_width=4)
        self.say("But look at Approximation, which got Bridget although Anita is higher on its list. "
                 "And Anita got Control, the last job on her list, although she ranks Approximation "
                 "higher. So these two would both rather have each other, and a matching like that "
                 "will not hold.",
                 flash(self.job_head[0]))
        self.cue("which got Bridget", self.job_cell[0][1].animate.set_stroke(YELLOW_D, 4))
        self.cue("Anita is higher", self.job_cell[0][0].animate.set_stroke(ORANGE, 4))
        self.cue("Anita got Control", self.cand_cell[0][2].animate.set_stroke(YELLOW_D, 4))
        self.cue("she ranks Approximation", self.cand_cell[0][1].animate.set_stroke(ORANGE, 4))
        self.cue("would both rather have each other", Create(self.d1))
        self.marked = [self.job_cell[0][1], self.job_cell[0][0],
                       self.cand_cell[0][2], self.cand_cell[0][1]]
        self.hold()   # 1.6: D1 and the four borders stay until the voice has finished the beat

    # ---- scene 2: the obvious plan, and the first day named part by part
    def first_try(self):
        head2 = self.heading("Let every job ask")
        self.play(FadeOut(self.head1), FadeOut(self.slot_a), FadeOut(self.m1), FadeOut(self.m2),
                  FadeOut(self.m3), FadeOut(self.d1), *[reset(c) for c in self.marked], run_time=1.0)
        self.slot_a = None
        self.play(FadeIn(head2))
        self.head1, self.head2 = None, head2

        self.p1 = arrow([-4.3, 0.80, 0], [-4.3, -0.45, 0])
        self.p2 = arrow([0.1, 0.80, 0], [0.1, -0.45, 0])
        self.p3 = arrow([4.9, 0.80, 0], [-3.4, -0.45, 0])
        self.say("So let us try the obvious thing and let every job ask for the candidate at the top "
                 "of its list. Approximation asks Anita, Basis asks Bridget, and Control asks Anita "
                 "as well.",
                 *[self.job_cell[i][0].animate.set_stroke(YELLOW_D, 4) for i in range(3)])
        self.cue("Approximation asks Anita", GrowArrow(self.p1))
        self.cue("Basis asks Bridget", GrowArrow(self.p2))
        self.cue("Control asks Anita as well", GrowArrow(self.p3))

        self.say("Now Anita holds two offers and Christine holds none, so the obvious thing has failed. "
                 "Anita can only take one job, so let her choose, and her own list puts Approximation "
                 "above Control.",
                 flash(self.cand_head[0]))
        self.cue("two offers", flash(self.p1), flash(self.p3))
        self.cue("Christine holds none", flash(self.cand_head[2]))
        self.cue("her own list", self.cand_cell[0][1].animate.set_stroke(YELLOW_D, 4),
                 self.cand_cell[0][2].animate.set_stroke(YELLOW_D, 4))

        red_seg = Line([-6.5, -2.05, 0], [-5.5, -2.05, 0], color=RED_C, stroke_width=4)
        red_lab = txt("refused", 20, RED_C).move_to([STRIP_X, -2.35, 0])
        self.say("So Anita keeps the offer from Approximation and says no to Control. "
                 "Bridget has a single offer, from Basis, so she simply keeps that one.")
        self.cue("keeps the offer", self.p1.animate.set_color(GREEN_C),
                 self.cand_cell[0][1].animate.set_stroke(GREEN_C, 4))
        self.cue("says no to Control", self.p3.animate.set_color(RED_C), reset(self.cand_cell[0][2]))
        self.play(FadeOut(self.p3), FadeIn(red_seg), FadeIn(red_lab))
        self.p3 = None
        self.red_seg, self.red_lab = red_seg, red_lab
        self.cue("she simply keeps", self.p2.animate.set_color(GREEN_C),
                 self.cand_cell[1][1].animate.set_stroke(GREEN_C, 4))

        green_seg = Line([-6.5, -1.35, 0], [-5.5, -1.35, 0], color=GREEN_C, stroke_width=4)
        green_lab = txt("in hand", 20, GREEN_C).move_to([STRIP_X, -1.65, 0])
        self.say("Notice that Anita has not said yes. Basis is at the top of her list and might still "
                 "ask her on a later day, so her answer is only a maybe. We say that she has the offer "
                 "from Approximation in hand.",
                 flash(self.cand_head[0]))
        self.cue("Basis is at the top", flash(self.cand_cell[0][0]))
        self.cue("only a maybe", flash(self.p1))
        self.cue("in hand", FadeIn(green_seg), FadeIn(green_lab))

        self.say("Control has been refused, so there is no point in asking Anita again. "
                 "It crosses her off its list, and the best candidate it has left is Bridget.",
                 flash(self.job_head[2]))
        self.cue("crosses her", self.job_cell[2][0].animate.set_stroke(GREY_B, 2, opacity=0.25),
                 self.job_names[(2, 0)].animate.set_opacity(0.25))
        self.cue("is Bridget", self.job_cell[2][1].animate.set_stroke(YELLOW_D, 4))

        morning = txt("morning", 20, GREY_B).move_to([STRIP_X, SLOT_B_Y, 0])
        afternoon = txt("afternoon", 20, GREY_B).move_to([STRIP_X, SLOT_B_Y, 0])
        evening = txt("evening", 20, GREY_B).move_to([STRIP_X, SLOT_B_Y, 0])
        self.say("What we just watched was one full day, so let us give its parts their names.\n"
                 "In the morning every job made an offer to the best candidate still on its list. "
                 "In the afternoon every candidate kept her best offer in hand and refused the rest. "
                 "In the evening every refused job crossed off the candidate who said no.",
                 *self.swap("slot_a", txt("Day 1", 26).move_to([STRIP_X, SLOT_A_Y, 0])))
        self.cue("In the morning", *self.swap("slot_b", morning),
                 flash(self.job_cell[0][0]), flash(self.job_cell[1][0]))
        self.cue("In the afternoon", *self.swap("slot_b", afternoon), flash(self.p1), flash(self.p2))
        self.cue("In the evening", *self.swap("slot_b", evening), flash(self.job_cell[2][0]))

    # ---- scene 3: days two and three, and why it stops
    def days(self):
        head3 = self.heading("Day after day")
        self.play(FadeOut(self.head2), FadeIn(head3))
        self.head2, self.head3 = None, head3

        self.p4 = arrow([4.9, 0.80, 0], [1.0, -0.45, 0])
        self.say("On the second morning the rule is the same, so every job asks the best candidate who "
                 "has not refused it. Approximation and Basis were never refused, so they simply repeat "
                 "their offers to Anita and Bridget. Control asks Bridget for the first time.",
                 *self.swap("slot_a", txt("Day 2", 26).move_to([STRIP_X, SLOT_A_Y, 0])),
                 *self.swap("slot_b", txt("morning", 20, GREY_B).move_to([STRIP_X, SLOT_B_Y, 0])))
        self.cue("the best candidate", flash(self.job_cell[0][0]), flash(self.job_cell[1][0]),
                 flash(self.job_cell[2][1]))
        self.cue("repeat their offers", flash(self.p1), flash(self.p2))
        self.cue("Control asks Bridget", GrowArrow(self.p4))

        self.say("So this afternoon it is Bridget who holds two offers, one from Basis and one from "
                 "Control. Her list puts Basis above Control, so she keeps Basis in hand and refuses "
                 "Control.",
                 *self.swap("slot_b", txt("afternoon", 20, GREY_B).move_to([STRIP_X, SLOT_B_Y, 0])))
        self.cue("holds two offers", flash(self.p2), flash(self.p4))
        self.cue("Her list puts", self.cand_cell[1][2].animate.set_stroke(YELLOW_D, 4),
                 flash(self.cand_cell[1][1]))
        self.cue("keeps Basis in hand", flash(self.p2))
        self.cue("refuses", self.p4.animate.set_color(RED_C), reset(self.cand_cell[1][2]))
        self.play(FadeOut(self.p4))
        self.p4 = None

        self.say("In the evening Control crosses Bridget off as well. "
                 "Only one name is left on its list now, and that name is Christine.",
                 *self.swap("slot_b", txt("evening", 20, GREY_B).move_to([STRIP_X, SLOT_B_Y, 0])))
        self.cue("crosses Bridget off", self.job_cell[2][1].animate.set_stroke(GREY_B, 2, opacity=0.25),
                 self.job_names[(2, 1)].animate.set_opacity(0.25))
        self.cue("that name is Christine", self.job_cell[2][2].animate.set_stroke(YELLOW_D, 4))

        self.p5 = arrow([4.9, 0.80, 0], [4.9, -0.45, 0])
        self.say("On the third morning Approximation asks Anita again, Basis asks Bridget again, and "
                 "Control asks Christine. In the afternoon every candidate holds exactly one offer, so "
                 "for the first time nobody is refused.",
                 *self.swap("slot_a", txt("Day 3", 26).move_to([STRIP_X, SLOT_A_Y, 0])),
                 *self.swap("slot_b", txt("morning", 20, GREY_B).move_to([STRIP_X, SLOT_B_Y, 0])),
                 flash(self.p1), flash(self.p2))
        self.cue("Control asks Christine", GrowArrow(self.p5))
        self.cue("In the afternoon", *self.swap("slot_b", txt("afternoon", 20, GREY_B)
                                                .move_to([STRIP_X, SLOT_B_Y, 0])))
        self.cue("exactly one offer", self.p5.animate.set_color(GREEN_C),
                 self.cand_cell[2][2].animate.set_stroke(GREEN_C, 4))
        self.cue("nobody is refused", flash(self.red_seg), flash(self.red_lab))
        self.play(self.red_seg.animate.set_opacity(0.3), self.red_lab.animate.set_opacity(0.3))

        self.say("Think about what a fourth day would look like. Nobody was refused, so no list changed "
                 "in the evening, and every job would ask the same candidate again. Each candidate "
                 "would get the same single offer, so nothing could ever change. This is where we stop, "
                 "and each candidate accepts the offer she has in hand.",
                 *self.swap("slot_b", txt("evening", 20, GREY_B).move_to([STRIP_X, SLOT_B_Y, 0])))
        self.cue("no list changed", *[flash(h) for h in self.job_head])
        self.cue("ask the same candidate again", flash(self.job_cell[0][0]), flash(self.job_cell[1][0]),
                 flash(self.job_cell[2][2]))
        self.cue("the same single offer", flash(self.p1), flash(self.p2), flash(self.p5))
        self.cue("This is where we stop", *self.swap("slot_a", txt("stop", 26, GREEN_C)
                                                     .move_to([STRIP_X, SLOT_A_Y, 0])),
                 *self.swap("slot_b", None))
        self.cue("accepts the offer",
                 *[p.animate.set_stroke(width=7) for p in (self.p1, self.p2, self.p5)])
        self.hold()   # 3.5: "stop" and the heading stay until the voice has finished the beat

    # ---- scene 4: the result, its name, and the open questions
    def result(self):
        self.play(FadeOut(self.head3), FadeOut(self.slot_a))
        self.slot_a = None

        also = txt("also called Gale-Shapley", 24, YELLOW_D)
        also.move_to([6.6 - also.width / 2, 3.5, 0])
        self.say("So the result is that Approximation hires Anita, Basis hires Bridget, and Control "
                 "hires Christine. The pair that spoiled our first matching, Approximation and Anita, "
                 "has ended up together. This procedure is called the propose and reject algorithm, "
                 "and it is also known as the Gale Shapley algorithm.",
                 flash(self.p1), flash(self.p2), flash(self.p5))
        self.cue("Approximation hires Anita", flash(self.p1), flash(self.job_head[0]),
                 flash(self.cand_head[0]))
        self.cue("Basis hires Bridget", flash(self.p2), flash(self.job_head[1]), flash(self.cand_head[1]))
        self.cue("hires Christine", flash(self.p5), flash(self.job_head[2]), flash(self.cand_head[2]))
        self.cue("spoiled our first matching", Indicate(self.p1, color=ORANGE, scale_factor=1.1))
        self.cue("propose and reject algorithm", FadeIn(self.heading("Propose and reject")))
        self.cue("Gale Shapley algorithm", FadeIn(also))

        self.say("Look at Control and Christine, who each ended up with the last name on their own list. "
                 "And we watched only one example, which happened to stop after three days. Does this "
                 "procedure always stop, and is its result always free of pairs who would both rather "
                 "have each other? Those are the questions for the next episodes.",
                 flash(self.job_head[2]), flash(self.cand_head[2]))
        self.cue("the last name", flash(self.job_cell[2][2]), flash(self.cand_cell[2][2]))
        self.cue("after three days", FadeIn(txt("Day 3", 26).move_to([STRIP_X, SLOT_A_Y, 0])))
        self.cue("always stop", FadeIn(txt("always?", 20, YELLOW_D).move_to([STRIP_X, SLOT_B_Y, 0])))
        self.cue("free of pairs", flash(self.p1), flash(self.p2), flash(self.p5))
