"""STRICT TEMPLATE: a whole small episode that passes check.py as it is.

Copy it to <unit>/ep01_<topic>.py, run check.py once to prove the setup, then replace
the parts marked REPLACE, one scene at a time. Keep the shape:
FACTS with asserts -> class EpNN... -> SCENES -> construct -> one method per scene.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---- FACTS (REPLACE). Every number that is shown or spoken is computed here and asserted.
# The picture reads these names. The narration says numbers as words, so each spoken
# number gets an assert here that pins it to the computed value.
N = 10
NUMS = list(range(1, N + 1))
TOTAL = sum(NUMS)
PAIRS = [(NUMS[i], NUMS[-1 - i]) for i in range(N // 2)]
PAIR_SUM = N + 1
assert all(a + b == PAIR_SUM for a, b in PAIRS)
assert (N, len(PAIRS), PAIR_SUM, TOTAL) == (10, 5, 11, 55)     # "ten", "five", "eleven", "fifty-five"
assert TOTAL == len(PAIRS) * PAIR_SUM == N * (N + 1) // 2
assert NUMS[0] + NUMS[1] == 3 and sum(NUMS[:3]) == 6           # "three", "six"


class Ep01PairingSum(NarratedScene):       # REPLACE the name; the same name goes in series.py
    SCENES = ["by_hand", "pairing"]        # REPLACE: your scene methods, in order

    def construct(self):                   # keep this method exactly; edit only the recap
        if self.preview_only(self.SCENES):
            return
        self.title_card()
        for name in self.SCENES:
            getattr(self, name)()
        self.end_card(["Adding one at a time takes one step for every number",
                       "Pairing the two ends gives the same sum for every pair",
                       "So the total is the number of pairs times the sum of one pair"])

    # ---- scene 1: the natural first try, on a concrete case
    def by_hand(self):
        head = self.heading("Adding one by one")
        row = VGroup(*[VGroup(Square(0.9, stroke_color=BLUE_C, stroke_width=2, fill_color=BLUE_C,
                                     fill_opacity=0.1), mono(str(v), 28)) for v in NUMS])
        row.arrange(RIGHT, buff=0.15).set_y(0.3)
        total = mono("0", 40, YELLOW_D).set_y(-1.4)
        label = txt("running total", 26, GREY_A).next_to(total, LEFT, buff=0.5)   # labels: always next_to

        # A beat: 2 to 4 linked sentences about ONE picture. The animations after the text start with it.
        self.say("Here are the whole numbers from one to ten, and we want their sum. "
                 "The obvious way is to add them one at a time and keep a running total.",
                 Write(head), LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in row], lag_ratio=0.08))
        # A cue: the phrase is copied from the beat above; its animation plays when the voice gets there.
        self.cue("keep a running total", FadeIn(label), FadeIn(total))

        self.say("One plus two is three, plus three is six, and so it goes on for nine additions. "
                 "At the end the total is fifty-five, but imagine doing this for a thousand numbers.")
        run = 0
        for cell, v in zip(row, NUMS):     # plain play() calls run while the beat is spoken
            run += v
            self.play(Indicate(cell, color=YELLOW_D), Transform(total, mono(str(run), 40, YELLOW_D).set_y(-1.4)),
                      run_time=0.45)
        assert run == TOTAL
        self.hold()                        # wait until the voice has finished
        self.play(FadeOut(head))
        self.row, self.total = row, VGroup(total, label)   # the next scene continues on this stage

    # ---- scene 2: the better idea, shown before it is named
    def pairing(self):
        row = self.row
        arcs = VGroup(*[ArcBetweenPoints(row[i].get_top(), row[-1 - i].get_top(), angle=-PI / 3, color=c)
                        for i, c in enumerate([YELLOW_D, GREEN_C, TEAL_C, GOLD_C, RED_C])])

        self.say("Now look at the two ends of the row instead. One and ten make eleven.\n"   # \n = longer pause
                 "Two and nine make eleven as well, and so does every pair as we walk inward.",
                 FadeOut(self.total), Create(arcs[0]))
        self.cue("Two and nine", Create(arcs[1]))
        self.cue("every pair", LaggedStart(*[Create(a) for a in arcs[2:]], lag_ratio=0.3))

        count = txt(f"{len(PAIRS)} pairs, each worth {PAIR_SUM}", 30).set_y(-1.3)
        product = mono(f"{len(PAIRS)} × {PAIR_SUM} = {TOTAL}", 34, YELLOW_D).next_to(count, DOWN, buff=0.35)
        self.say("So the ten numbers split into five pairs, and each pair is worth eleven. "
                 "Five times eleven is fifty-five, the same total as before, with a single multiplication.",
                 FadeIn(count, shift=UP * 0.2))
        self.cue("Five times eleven", FadeIn(product, shift=UP * 0.2))

        rule = txt("n numbers:  n / 2 pairs,  each worth n + 1", 30, GREEN_B).set_y(-1.6)
        self.say("Nothing in this picture depended on the number ten. "
                 "With n numbers there are n over two pairs, and each pair is worth n plus one.",
                 FadeOut(count), FadeOut(product), FadeIn(rule))
        self.cue("each pair is worth", Indicate(rule))
        self.hold(0.5)
