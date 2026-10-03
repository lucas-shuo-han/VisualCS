"""A complete, small episode showing the manim_kit patterns end to end.

Render a quick preview from the folder that holds manim_kit.py:
    manim -ql example_episode.py Ep01BinarySearch
or, saved as ep01_binary_search.py in a unit, one scene at a time with the voice:
    python preview.py walkthrough --unit <unit>
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

ARR = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
TARGET = 23


def trace(arr, target):
    """Compute the steps in Python so the animation can never disagree with the algorithm."""
    lo, hi, steps = 0, len(arr) - 1, []
    while lo <= hi:
        mid = (lo + hi) // 2
        steps.append((lo, hi, mid))
        if arr[mid] == target:
            break
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return steps


class Ep01BinarySearch(NarratedScene):
    series = "Algorithms, Visually"
    SCENES = ["idea", "walkthrough"]      # scene methods, in order (preview.py reads this)

    def construct(self):
        if self.preview_only(self.SCENES):    # walkthrough continues on idea's stage
            return
        self.title_card(1, "Binary Search", "halving the problem, one comparison at a time")
        self.idea()
        self.walkthrough()
        self.end_card(
            ["Keep a window from lo to hi that must contain the target",
             "Compare with the middle element, then discard half",
             "A list of n items takes about log base two of n comparisons"],
            next_title="Sorting with merges",
        )

    def cells(self):
        row = VGroup()
        for k, v in enumerate(ARR):
            sq = Square(0.9, stroke_color=BLUE_C, stroke_width=2, fill_color=BLUE_C, fill_opacity=0.1)
            sq.move_to(RIGHT * k * 0.9)
            idx = mono(str(k), 18, GREY).next_to(sq, DOWN, buff=0.12)
            row.add(VGroup(sq, mono(str(v), 28).move_to(sq), idx))
        return row.move_to(UP * 1.9)

    def idea(self):
        head = self.heading("The idea")
        row = self.cells()
        # One beat = a few sentences spoken as one clip. say() starts it with the first
        # animation; cue() plays each further step when the voice reaches those words.
        self.say("Here is a sorted list of ten numbers, and we want to know whether twenty-three "
                 "is in it. Checking them one by one could take ten comparisons. "
                 "But the list is sorted, and that lets us do much better.",
                 Write(head), LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in row], lag_ratio=0.08))
        self.cue("Checking them one by one",
                 LaggedStart(*[Indicate(c[0], color=GREY_B) for c in row], lag_ratio=0.1))
        self.hold()
        self.row = row
        self.play(FadeOut(head))

    def walkthrough(self):
        row = self.row
        code = CodeListing([
            "while lo <= hi:",
            "    mid = (lo + hi) // 2",
            "    if a[mid] == t: return mid",
            "    if a[mid] < t: lo = mid + 1",
            "    else:          hi = mid - 1",
        ], lang="python", font_size=26, line_gap=0.46).to_edge(LEFT, buff=0.6).set_y(-0.5)
        regs = reg_column([("lo", 0), ("hi", 9), ("mid", "-")], width=1.2, font_size=24, color=TEAL_C)
        regs.to_edge(RIGHT, buff=0.8).set_y(-0.5)
        self.say("Keep a window from lo to hi that must contain the target, if it is there at all.",
                 FadeIn(code, shift=UP * 0.2), FadeIn(regs))
        window = SurroundingRectangle(row, color=YELLOW_D, buff=0.08)
        self.play(Create(window))
        box = code.line_box(1)
        arrow = Arrow(UP * 0.8, ORIGIN, buff=0, color=YELLOW_D).next_to(row[0], UP, buff=0.1)

        for step, (lo, hi, mid) in enumerate(trace(ARR, TARGET)):
            span = VGroup(*row[lo:hi + 1])
            found = ARR[mid] == TARGET
            small = ARR[mid] < TARGET
            verdict = ("That is the number we are looking for." if found else
                       "That is too small, so the whole left half can go." if small else
                       "That is too big, so the whole right half can go.")
            # numbers stay on screen; the voice says the idea in plain words
            self.say(f"{'First' if step == 0 else 'Next'}, look at the middle of the window, "
                     f"which is index {mid}. {verdict}",
                     window.animate.become(SurroundingRectangle(span, color=YELLOW_D, buff=0.08)),
                     FadeIn(box) if step == 0 else box.animate.become(code.line_box(1)),
                     arrow.animate.next_to(row[mid], UP, buff=0.1),
                     regs[0].set(lo), regs[1].set(hi), regs[2].set(mid))
            if found:
                self.cue("That is", box.animate.become(code.line_box(2)),
                         row[mid][0].animate.set_fill(GREEN_C, 0.45))
            else:
                gone = VGroup(*row[lo:mid + 1]) if small else VGroup(*row[mid:hi + 1])
                self.cue("That is", box.animate.become(code.line_box(3 if small else 4)),
                         gone.animate.set_opacity(0.25))
            self.hold()

        n = len(trace(ARR, TARGET))
        assert n == 3
        self.say("That took three comparisons instead of up to ten. Every comparison halves the "
                 "window, so even a million items need only about twenty.")
        self.hold(0.5)
