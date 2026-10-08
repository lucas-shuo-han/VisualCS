"""CS70 Note 11, episode 04: the roommates problem.

Built from BOARD-ep04.md: every `> ` line of the board is one say() below, copied
unchanged, and the picture is built as the board's stage lines describe.
"""
import os
import sys
from itertools import combinations, permutations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---------------------------------------------------------------- FACTS
# The board's "Facts" table. The four students, their lists, the three matchings and the
# rogue couple of each are computed here and asserted; the stage reads these names and
# never a typed-in value.
PEOPLE = ["Amy", "Ben", "Cora", "Dan"]          # F1: the notes' A, B, C, D, spelled out for the voice
PREF = {                                        # F2: Dan's list is left open on purpose
    "Amy": ["Ben", "Cora", "Dan"],
    "Ben": ["Cora", "Amy", "Dan"],
    "Cora": ["Amy", "Ben", "Dan"],
}
LISTED = list(PREF)                             # the rows with a list; the row of Dan is the "?" row
OPEN = "?"
M1 = {"Amy": "Ben", "Ben": "Amy", "Cora": "Dan", "Dan": "Cora"}
M2 = {"Ben": "Cora", "Cora": "Ben", "Amy": "Dan", "Dan": "Amy"}
M3 = {"Amy": "Cora", "Cora": "Amy", "Ben": "Dan", "Dan": "Ben"}
MATCHINGS = [M1, M2, M3]


def rogue(m, dan=("Amy", "Ben", "Cora")):
    """Every rogue couple of the matching m: two people who are not together who both
    rank each other above the partner m gives them (F3 to F5)."""
    pref = dict(PREF, Dan=list(dan))
    out = []
    for i, x in enumerate(PEOPLE):
        for y in PEOPLE[i + 1:]:
            if m[x] != y and pref[x].index(y) < pref[x].index(m[x]) and pref[y].index(x) < pref[y].index(m[y]):
                out.append((x, y))
    return out


def repair(m):
    """The matching the obvious repair gives: the first rogue couple of m is paired up
    and so are the two partners it leaves behind (F7)."""
    x, y = rogue(m)[0]
    a, b = m[x], m[y]
    return {x: y, y: x, a: b, b: a}


def row_of(p):
    return PEOPLE.index(p)


def name_cell(p, q):
    """Where the picture puts the name q: p's row, the column of q in p's list."""
    return row_of(p), PREF[p].index(q)


def cell_of(m, p):
    """p's roommate cell in the matching m."""
    return name_cell(p, m[p])


def couple_cells(x, y):
    """The two cells of a couple that prefers each other: x's name for y and y's for x."""
    return [name_cell(x, y), name_cell(y, x)]


def pairs_of(m):
    return [(p, m[p]) for p in PEOPLE if row_of(p) < row_of(m[p])]


def first_chooser(p):
    """The one of the other two who ranks p first (F6, the reason of beats 3.2 and 3.3)."""
    return next(q for q in LISTED if PREF[q][0] == p)


assert (len(PEOPLE), len(PREF) + 1, len(MATCHINGS)) == (4, 4, 3)   # F1, F6: "four", "three matchings"
assert all(len(PREF[p]) == 3 for p in LISTED)                      # beat 1.2: "the other three"
assert all(set(PREF[p]) == set(PEOPLE) - {p} for p in LISTED)
assert all(sorted(m) == sorted(PEOPLE) and m[m[p]] == p for m in MATCHINGS for p in PEOPLE)
assert [rogue(m) for m in MATCHINGS] == [[("Ben", "Cora")], [("Amy", "Cora")], [("Amy", "Ben")]]
for dan in permutations([p for p in PEOPLE if p != "Dan"]):        # F6: whatever the list of Dan is
    assert [rogue(m, dan) for m in MATCHINGS] == [[("Ben", "Cora")], [("Amy", "Cora")], [("Amy", "Ben")]]
assert repair(M1) == M2 and repair(M2) == M3 and repair(M3) == M1  # F7: the repairs run in a circle

# the cells of the picture, exactly as the board's beats name them
assert [cell_of(M1, p) for p in LISTED] == [(0, 0), (1, 1), (2, 2)]        # beat 2.1
assert [cell_of(M2, p) for p in LISTED] == [(0, 2), (1, 0), (2, 1)]        # beat 2.2
assert [cell_of(M3, p) for p in LISTED] == [(0, 1), (1, 2), (2, 0)]        # beat 2.4
assert [couple_cells(*rogue(m)[0]) for m in MATCHINGS] == \
    [[(1, 0), (2, 1)], [(0, 1), (2, 0)], [(0, 0), (1, 1)]]                 # beats 2.1, 2.3, 2.4
assert [PREF[p].index("Dan") for p in LISTED] == [2, 2, 2]                 # beat 3.2: the three "Dan"
assert [PREF[p][0] for p in LISTED] == ["Ben", "Cora", "Amy"]              # beat 3.2: the first column
assert PREF["Ben"][0] == "Cora" and PREF["Cora"][0] == "Amy" and PREF["Amy"][0] == "Ben"   # the cycle
for m in MATCHINGS:                                                # the reason of beats 3.2, 3.3
    with_dan = next(p for p in LISTED if m[p] == "Dan")
    assert set(rogue(m)[0]) == {with_dan, first_chooser(with_dan)}
assert all(len([q for q in PEOPLE if q not in (p, "Amy")]) == 2 for p in PEOPLE[1:])   # "the other two"

# ---------------------------------------------------------------- the board's stage
R = 0.5                                          # every student: a circle of this radius
CIRC = {"Amy": (-5.2, 1.5, 0), "Ben": (-2.0, 1.5, 0),      # the square, the notes' A B C D
        "Cora": (-2.0, -1.7, 0), "Dan": (-5.2, -1.7, 0)}
CX = [2.2, 3.7, 5.2]                             # the three columns of the table
HX, CARD_W = 0.6, 1.4                            # the row headers
ROW_Y = [1.3, 0.4, -0.5, -1.4]                   # the four rows, top to bottom
CW, CH = 1.4, 0.6                                # one cell
CAP_Y = 2.0                                      # the column captions
SLOT_XY, SLOT_W, SLOT_SIZE = (-3.6, -2.4), 6.0, 30   # the status text: middle of the left block,
                                                 # under the circles, and its widest allowed
NAME_W_MAX = 2 * R - 0.2                         # a name inside its circle
LOOP_XY, LOOP_R = (-3.6, -0.1, 0), 0.55          # the repair arrow, the middle of the square


def flash(mob):
    """The board's "flash": the object returns to the look it had."""
    return Indicate(mob, color=YELLOW_D, scale_factor=1.1)


def reset_cell(cell):
    return cell.animate.set_stroke(GREY_B, 2)


def status(s, color=C_TEXT):
    t = txt(s, SLOT_SIZE, color).move_to([SLOT_XY[0], SLOT_XY[1], 0])
    if t.width > SLOT_W:
        t.scale_to_fit_width(SLOT_W)
    return t


class Ep04Roommates(NarratedScene):
    """Episode 04: four students, and a repair that runs in a circle."""

    SCENES = ["hook", "repair", "none", "lesson"]

    def construct(self):
        if self.preview_only(self.SCENES):
            return
        self.title_card()
        for name in self.SCENES:
            getattr(self, name)()
        self.end_card([
            "Repairing a rogue couple can create a new one, so repairing again and again need not end.",
            "For four roommates with these lists the repairs run in a circle, and none of the three "
            "matchings is stable.",
            "A stable matching does not have to exist when there is only one kind of participant.",
            "So a proof that jobs and candidates always have a stable matching must use the two sides.",
        ])

    # -- the one stage every scene stands on
    def build_students(self):
        self.circ, self.word, self.seat = {}, {}, {}
        for p in PEOPLE:
            c = Circle(radius=R, stroke_color=TEAL_C, stroke_width=3,
                       fill_color=TEAL_C, fill_opacity=0.15).move_to(CIRC[p])
            t = txt(p, 22).move_to(CIRC[p])
            if t.width > NAME_W_MAX:
                t.scale_to_fit_width(NAME_W_MAX)
            self.circ[p], self.word[p] = c, t
            self.seat[p] = VGroup(c, t)
        self.every_line = [Line(CIRC[a], CIRC[b], buff=R, color=GREY_B, stroke_width=2)
                           for a, b in combinations(PEOPLE, 2)]        # the six possible pairs
        self.loop = None
        self.slot = None

    def build_table(self):
        self.card = [box_label(p, TEAL_C, w=CARD_W, h=CH, font_size=22).move_to([HX, ROW_Y[i], 0])
                     for i, p in enumerate(PEOPLE)]
        self.cells = [[Rectangle(width=CW, height=CH, stroke_color=GREY_B, stroke_width=2)
                       .move_to([CX[c], ROW_Y[r], 0]) for c in range(len(CX))]
                      for r in range(len(PEOPLE))]
        self.cellword = [[txt(PREF[PEOPLE[r]][c] if PEOPLE[r] in PREF else OPEN, 22)
                          .move_to([CX[c], ROW_Y[r], 0]) for c in range(len(CX))]
                         for r in range(len(PEOPLE))]
        for r in range(len(PEOPLE)):
            for t in self.cellword[r]:
                if t.width > CW - 0.2:
                    t.scale_to_fit_width(CW - 0.2)
        self.heads = VGroup(*self.card)
        self.cellgrid = VGroup(*[c for row in self.cells for c in row])
        self.captions = VGroup(*[txt(cap, 20, GREY_B).move_to([CX[c], CAP_Y, 0])
                                 for c, cap in enumerate(["first", "second", "last"])])

    def cell(self, rc):
        return self.cells[rc[0]][rc[1]]

    def word_at(self, rc):
        return self.cellword[rc[0]][rc[1]]

    def pair_line(self, a, b):
        return Line(CIRC[a], CIRC[b], buff=R, color=WHITE, stroke_width=5)

    def rogue_line(self, a, b):
        return DashedLine(CIRC[a], CIRC[b], buff=R, color=ORANGE, stroke_width=5, dash_length=0.25)

    def green(self, m):
        """The matching on screen: every roommate cell gets a green border."""
        return [self.cell(cell_of(m, p)).animate.set_stroke(GREEN_C, 4) for p in LISTED]

    def reset(self):
        return [reset_cell(c) for c in self.cellgrid]

    def reset_except(self, keep):
        """The table reset, except for the cells in `keep` (each one a (row, column)
        pair). Used where one play both resets the table and turns the roommate cells
        green: a cell named twice in one play is drawn to two states at once."""
        keep = set(keep)
        return [reset_cell(self.cells[r][c]) for r in range(len(PEOPLE)) for c in range(len(CX))
                if (r, c) not in keep]

    def slot_change(self, new):
        """The status text changes: the old one out, the new one in, in one animation."""
        old = self.slot
        self.slot = new
        if old is None:
            return () if new is None else (FadeIn(new),)
        return (FadeOut(old),) if new is None else (FadeOut(old), FadeIn(new))

    def loop_arrow(self):
        return Arc(radius=LOOP_R, start_angle=0.6, angle=5.0, arc_center=list(LOOP_XY),
                   color=YELLOW_D, stroke_width=5).add_tip()

    # ---- scene 1: the four students and their lists
    def hook(self):
        self.head1 = self.heading("Four students, two rooms")
        self.play(FadeIn(self.head1))
        self.build_students()
        self.build_table()

        self.say("Last time we asked whether every set of lists has a stable matching. "
                 "Before we answer that, look at a close cousin of the problem. "
                 "Four students, Amy, Ben, Cora and Dan, have to pair up as roommates. "
                 "This time there are no two sides, so anybody can end up with anybody.",
                 FadeIn(self.seat["Amy"], shift=UP * 0.2))
        self.cue("Four students",
                 LaggedStart(*[FadeIn(self.seat[p], shift=UP * 0.2) for p in PEOPLE[1:]], lag_ratio=0.3))
        self.cue("pair up as roommates", *[flash(self.circ[p]) for p in PEOPLE])
        self.cue("anybody can end up with anybody",
                 LaggedStart(*[Create(l) for l in self.every_line], lag_ratio=0.15))
        self.wait(1.0)
        self.play(*[FadeOut(l) for l in self.every_line])

        self.say("Each of them ranks the other three. Amy would like Ben best and then Cora, "
                 "Ben would like Cora best and then Amy, and Cora would like Amy best and then Ben. "
                 "All three put Dan last, and we leave the list of Dan open for now.",
                 FadeIn(self.heads), FadeIn(self.cellgrid), FadeIn(self.captions))
        self.cue("Amy would like Ben", *[FadeIn(self.cellword[0][c]) for c in range(2)])
        self.cue("Ben would like Cora", *[FadeIn(self.cellword[1][c]) for c in range(2)])
        self.cue("Cora would like Amy", *[FadeIn(self.cellword[2][c]) for c in range(2)])
        self.cue("put Dan last", *[FadeIn(self.cellword[r][2]) for r in range(3)])
        self.cue("open for now", *[FadeIn(self.cellword[3][c]) for c in range(3)])
        self.hold()

    # ---- scene 2: the obvious repair, and the circle it runs in
    def repair(self):
        self.head2 = self.heading("Repair the rogue couple")
        self.play(FadeOut(self.head1), FadeIn(self.head2))
        self.head1 = None
        self.cur = [self.pair_line(*p) for p in pairs_of(M1)]          # Amy-Ben and Cora-Dan
        x, y = rogue(M1)[0]                                            # Ben and Cora

        self.say("Let us start with any matching, say Amy with Ben and Cora with Dan. "
                 "Ben has Amy, but his first choice is Cora, and Cora is stuck with her last "
                 "choice, so she would gladly take Ben. So Ben and Cora are a rogue couple, "
                 "and this matching is unstable.",
                 *[Create(p) for p in self.cur], *self.green(M1))
        self.cue("his first choice is Cora",
                 self.cell(name_cell(x, y)).animate.set_stroke(ORANGE, 4))
        self.cue("stuck with her last choice", flash(self.cell(cell_of(M1, y))))
        self.cue("gladly take Ben",
                 self.cell(name_cell(y, x)).animate.set_stroke(ORANGE, 4))
        self.dash = self.rogue_line(x, y)
        self.cue("are a rogue couple", Create(self.dash),
                 *self.slot_change(status("rogue couple", ORANGE)))

        # the repair: Ben and Cora move in together, Amy and Dan are left with each other
        l_amydan, l_bencora = self.pair_line("Amy", "Dan"), self.pair_line("Ben", "Cora")
        self.say("The obvious repair is to give the rogue couple what they want. "
                 "So Ben moves in with Cora, and the two who are left behind, Amy and Dan, "
                 "share the other room. Each repair gets rid of one rogue couple, so surely "
                 "we run out of them in the end.",
                 flash(self.dash))
        self.cue("Ben moves in with Cora",
                 *[FadeOut(p) for p in self.cur], FadeOut(self.dash), Create(l_bencora),
                 *self.slot_change(None))
        self.cur = [l_amydan, l_bencora]
        self.dash = None
        self.cue("Amy and Dan", Create(l_amydan))
        self.play(*self.reset())
        self.play(*self.green(M2))
        self.cue("run out of them", flash(l_bencora), flash(l_amydan))

        x, y = rogue(M2)[0]                                            # Amy and Cora
        self.say("Ben is content now, but look at Cora, who has Ben and still ranks Amy above him. "
                 "And Amy has been pushed down to her last choice, so she would gladly take Cora. "
                 "The repair removed one rogue couple and created a new one, Amy and Cora.",
                 flash(self.cell(cell_of(M2, "Ben"))))
        self.cue("ranks Amy above him",
                 self.cell(name_cell(y, x)).animate.set_stroke(ORANGE, 4))
        self.cue("her last choice", flash(self.cell(cell_of(M2, x))))
        self.cue("gladly take Cora",
                 self.cell(name_cell(x, y)).animate.set_stroke(ORANGE, 4))
        self.dash = self.rogue_line(x, y)
        self.cue("created a new one", Create(self.dash),
                 *self.slot_change(status("rogue couple", ORANGE)))

        x, y = rogue(M3)[0]                                            # Amy and Ben
        l_amycora, l_bendan = self.pair_line("Amy", "Cora"), self.pair_line("Ben", "Dan")
        self.say("So we repair again, which puts Amy with Cora and leaves Ben with Dan. "
                 "Now it is Ben who sits on his last choice, and Amy still ranks Ben above Cora. "
                 "That makes Amy and Ben the next rogue couple.",
                 *self.slot_change(None))
        self.cue("puts Amy with Cora",
                 *[FadeOut(p) for p in self.cur], FadeOut(self.dash), Create(l_amycora))
        self.cur = [l_amycora, l_bendan]
        self.dash = None
        # the reset and the three green borders, in this cue and done before the
        # sentence ends (the phrase sits at the end of it)
        self.cue("leaves Ben with Dan", Create(l_bendan),
                 *self.reset_except([cell_of(M3, p) for p in LISTED]), *self.green(M3),
                 run_time=0.9)
        self.cue("sits on his last choice", flash(self.cell(cell_of(M3, y))))
        self.play(self.cell(name_cell(y, x)).animate.set_stroke(ORANGE, 4))
        self.cue("ranks Ben above Cora",
                 self.cell(name_cell(x, y)).animate.set_stroke(ORANGE, 4))
        self.dash = self.rogue_line(x, y)
        self.cue("the next rogue couple", Create(self.dash),
                 *self.slot_change(status("rogue couple", ORANGE)))

        # and back where we started: the repair never gets anywhere
        l_amyben, l_coradan = self.pair_line("Amy", "Ben"), self.pair_line("Cora", "Dan")
        self.say("Repair once more, and Amy is with Ben and Cora is with Dan. "
                 "But that is exactly the matching we started from. "
                 "The repairs run in a circle and never finish, so this recipe does not always "
                 "lead to a stable matching.",
                 *self.slot_change(None))
        self.cue("Amy is with Ben",
                 *[FadeOut(p) for p in self.cur], FadeOut(self.dash),
                 Create(l_amyben), Create(l_coradan))
        self.cur = [l_amyben, l_coradan]
        self.dash = None
        self.play(*self.reset())
        self.play(*self.green(M1))
        self.cue("the matching we started from",
                 *self.slot_change(status("back at the start", YELLOW_D)))
        self.loop = self.loop_arrow()
        self.cue("run in a circle", Create(self.loop))
        self.cue("does not always lead", flash(self.loop))
        self.hold()
        self.play(FadeOut(self.loop), *self.slot_change(None), *self.reset())
        self.loop = None

    # ---- scene 3: the three matchings, and the rogue couple each of them has
    def none(self):
        self.head3 = self.heading("No stable matching at all")
        self.play(FadeOut(self.head2), FadeIn(self.head3))
        self.head2 = None

        self.say("Maybe the recipe was just unlucky and a stable matching hides somewhere else. "
                 "Let us count the possibilities. Amy shares with Ben, with Cora, or with Dan, and "
                 "each choice leaves the other two no option but each other. So there are only "
                 "three matchings, and we have just seen a rogue couple in every one of them.",
                 *[flash(self.circ[p]) for p in PEOPLE])
        self.cue("Amy shares with Ben", flash(self.cur[0]), flash(self.cur[1]))
        l_amycora, l_bendan = self.pair_line("Amy", "Cora"), self.pair_line("Ben", "Dan")
        self.cue("with Cora", *[FadeOut(p) for p in self.cur], Create(l_amycora), Create(l_bendan))
        self.cur = [l_amycora, l_bendan]
        l_amydan, l_bencora = self.pair_line("Amy", "Dan"), self.pair_line("Ben", "Cora")
        self.cue("or with Dan", *[FadeOut(p) for p in self.cur], Create(l_amydan), Create(l_bencora))
        self.cur = [l_amydan, l_bencora]
        self.cue("only three matchings",
                 *self.slot_change(status("three matchings, each with a rogue couple")))

        self.say("There is a pattern behind this. Whoever shares with Dan has landed on their last "
                 "choice and would rather be with anyone else. Now look at the first choices, where "
                 "Amy wants Ben, Ben wants Cora, and Cora wants Amy. So whoever is with Dan is always "
                 "somebody's first choice.")
        self.cue("Whoever shares with Dan", flash(self.circ["Dan"]), flash(self.cur[0]),
                 *[self.cell(name_cell(p, "Dan")).animate.set_stroke(RED_C, 4) for p in LISTED])
        self.cue("Amy wants Ben",
                 LaggedStart(*[self.cell((r, 0)).animate.set_stroke(YELLOW_D, 4)
                               for r in range(len(LISTED))], lag_ratio=0.5))
        self.cue("somebody's first choice",
                 self.cell(name_cell("Cora", "Amy")).animate.set_stroke(ORANGE, 4))

        self.say("That somebody cannot be with their first choice, because Dan has taken it. So the "
                 "two of them would both rather have each other, and they form a rogue couple "
                 "whatever the list of Dan says.",
                 flash(self.cur[1]))
        self.cue("Dan has taken it", flash(self.cur[0]))
        self.dash = self.rogue_line("Amy", "Cora")
        self.cue("would both rather have each other",
                 self.cell(name_cell("Amy", "Cora")).animate.set_stroke(ORANGE, 4),
                 Create(self.dash))
        self.cue("whatever the list of Dan says",
                 *[flash(VGroup(self.cells[3][c], self.cellword[3][c])) for c in range(len(CX))])
        self.hold()
        self.play(FadeOut(self.dash), *self.reset())
        self.dash = None

    # ---- scene 4: the recipe never used the two sides, and that is why it was unsound
    def lesson(self):
        self.head4 = self.heading("Why two sides matter")
        self.play(FadeOut(self.head3), FadeIn(self.head4))
        self.head3 = None
        self.jobs, self.answers = ("Amy", "Ben"), ("Dan", "Cora")   # the arrows go Amy to Dan, Ben to Cora

        self.say("So for roommates a stable matching does not have to exist. Now remember the repair "
                 "recipe, which never asked who was a job and who was a candidate. If it proved that "
                 "jobs and candidates always have a stable matching, the same words would prove it "
                 "for roommates, and that is false.")
        self.cue("does not have to exist", *self.slot_change(status("no stable matching", RED_C)))
        self.loop = self.loop_arrow()
        self.cue("the repair recipe", Create(self.loop))
        self.cue("the same words would prove it", *[flash(self.circ[p]) for p in PEOPLE])
        self.cue("that is false", flash(self.slot))

        self.say("So any proof for jobs and candidates has to use the two sides somewhere. Propose and "
                 "reject does exactly that, because only jobs make offers and only candidates answer. "
                 "Whether it always ends in a stable matching is what the next episodes work out.",
                 FadeOut(self.loop), *[FadeOut(l) for l in self.cur])
        self.loop = None
        self.cur = []
        self.cue("use the two sides",
                 *[self.circ[p].animate.set_stroke(BLUE_C, 3).set_fill(BLUE_C, 0.15) for p in self.jobs],
                 *[self.circ[p].animate.set_stroke(GOLD_C, 3).set_fill(GOLD_C, 0.15)
                   for p in self.answers])
        self.arrows = [Arrow(CIRC[a], CIRC[b], buff=R, stroke_width=5)
                       for a, b in zip(self.jobs, self.answers)]
        self.cue("only jobs make offers", *[Create(a) for a in self.arrows])
        self.cue("only candidates answer", *[flash(self.circ[p]) for p in self.answers])
        self.cue("next episodes", *self.slot_change(status("always stable?", YELLOW_D)))
