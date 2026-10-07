"""Episode 5 of the CS70 Note 10 series: hypercubes, Lemma 10.1 and Theorem 10.5.

FACTS come from cs70/note10-deepseek/notes.txt (lines 441-549). The picture reads the
names below; the narration says numbers as words, and every spoken number has an assert here.
"""
import itertools
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---- FACTS ---------------------------------------------------------------------------
# Definition 1 (notes 451-456): the corners are the n-bit strings, two are joined when they
# differ in exactly one bit position.
def differ(x, y):
    return sum(a != b for a, b in zip(x, y))


def cube_vertices(n):
    return ["".join(p) for p in itertools.product("01", repeat=n)]


def cube_edges(n):
    vs = cube_vertices(n)
    return [(x, y) for x, y in itertools.combinations(vs, 2) if differ(x, y) == 1]


def ekey(a, b):
    return tuple(sorted((a, b)))


V3 = cube_vertices(3)
E3 = cube_edges(3)
assert len(V3) == 8 and len(E3) == 12                         # "eight corners", "twelve edges"
DEG3 = {v: sum(1 for e in E3 if v in e) for v in V3}
assert set(DEG3.values()) == {3}                               # "three neighbours"
assert differ("000", "001") == 1 and differ("000", "011") == 2  # neighbours / not neighbours

# Definition 2 (notes 473-478): two (n-1)-cubes plus the edges 0x - 1x.
SUB0 = [e for e in E3 if e[0][0] == "0" and e[1][0] == "0"]
SUB1 = [e for e in E3 if e[0][0] == "1" and e[1][0] == "1"]
JOIN = [e for e in E3 if e[0][0] != e[1][0]]
assert len(SUB0) == len(SUB1) == len(JOIN) == 4               # "four", "four", "four"
assert len(SUB0) + len(SUB1) + len(JOIN) == len(E3) == 12
assert all(e[0][1:] == e[1][1:] for e in JOIN)                 # same last two bits
assert ekey("010", "110") in [ekey(*e) for e in JOIN]
assert sorted(SUB0) == sorted(("0" + a, "0" + b) for a, b in cube_edges(2))
assert len(cube_vertices(2)) == 4 and len(cube_edges(2)) == 4  # a square

# Connection Machine (notes 441-449): 20 bits, about a million processors.
N_CM = 20
assert 2 ** N_CM == 1048576 and 10 ** 6 <= 2 ** N_CM < 1.1 * 10 ** 6   # "about a million"
WIRES = 10 ** 6 * (10 ** 6 - 1) // 2
assert 4 * 10 ** 11 < WIRES < 10 ** 12                         # "about half a trillion" (notes: 10^12)

# Lemma 10.1 (notes 491-497)
def E_formula(n):
    return n * 2 ** (n - 1)


for n in range(1, 7):
    assert len(cube_edges(n)) == E_formula(n)                  # the lemma, checked by counting
REC = {1: 1}
for n in range(2, 7):
    REC[n] = 2 * REC[n - 1] + 2 ** (n - 1)                     # proof 2
assert all(REC[n] == E_formula(n) for n in REC)
assert (REC[1], REC[2], REC[3], REC[4]) == (1, 4, 12, 32)
assert 2 * REC[1] + 2 == 4 and 2 * REC[2] + 4 == 12 and 2 * REC[3] + 8 == 32
assert 4 * 2 ** 3 == 32                                        # "four times two cubed"
assert 8 * 3 == 24 and 24 // 2 == 12                           # proof 1

# Theorem 10.5 (notes 503-545): examples on the 3-cube; S has at most 2^(n-1) = 4 corners.
def cut_edges(S):
    return [e for e in E3 if (e[0] in S) != (e[1] in S)]


S_ONE = {"000"}
S_FACE = {v for v in V3 if v[0] == "0"}
assert len(cut_edges(S_ONE)) == 3 and len(cut_edges(S_FACE)) == 4
assert sorted(cut_edges(S_FACE)) == sorted(JOIN)               # the joining edges
assert len(S_FACE) == 4 == 2 ** (3 - 1)
# Induction step with k = 2 (so n = k + 1 = 3, 2^k = 4, 2^(k-1) = 2)
K = 2
# case 1: two corners in each subcube
S_C1 = {"000", "001", "100", "101"}
S0_C1 = {v for v in S_C1 if v[0] == "0"}
S1_C1 = {v for v in S_C1 if v[0] == "1"}
assert len(S0_C1) == 2 == 2 ** (K - 1) and len(S1_C1) == 2 and len(S_C1) <= 2 ** K
C1_FRONT = (("000", "010"), ("001", "011"))                    # leave S0 inside the front square
C1_BACK = (("100", "110"), ("101", "111"))                     # leave S1 inside the back square
for a, b in C1_FRONT + C1_BACK:
    assert ekey(a, b) in [ekey(*e) for e in cut_edges(S_C1)]
assert len(C1_FRONT) + len(C1_BACK) == 4 == len(S_C1)
# case 2: three corners in the front subcube, one in the back
S_C2 = {"000", "001", "010", "100"}
S0_C2 = {v for v in S_C2 if v[0] == "0"}
S1_C2 = {v for v in S_C2 if v[0] == "1"}
assert len(S0_C2) == 3 > 2 ** (K - 1) and len(S1_C2) == 1 and len(S_C2) == 2 ** K
OUT0 = {v for v in V3 if v[0] == "0"} - S0_C2
assert OUT0 == {"011"} and len(OUT0) == 2 ** K - len(S0_C2) == 1
C2_BACK = ("100", "101")                                       # at least |S1| = 1
C2_FRONT = ("001", "011")                                      # at least 2^k - |S0| = 1
C2_JOIN = (("001", "101"), ("010", "110"))                     # at least |S0| - |S1| = 2
for a, b in (C2_BACK, C2_FRONT) + C2_JOIN:
    assert ekey(a, b) in [ekey(*e) for e in cut_edges(S_C2)]
assert len(S1_C2) == 1 and 2 ** K - len(S0_C2) == 1 and len(S0_C2) - len(S1_C2) == 2
assert 1 + 1 + 2 == 2 ** K == 4 and len(cut_edges(S_C2)) >= len(S_C2)
assert len(S0_C2) + len(S1_C2) == len(S_C2) == 4

# Geometry: the front square (first bit 0) and the back square (first bit 1), shifted up and right.
FRONT0 = np.array([-5.0, -1.4, 0.0])
STEP_X, STEP_Y, BACK = 2.2, 2.2, np.array([1.5, 1.2, 0.0])
R_V = 0.40


def pos(bits):
    b1, b2, b3 = (int(c) for c in bits)
    return FRONT0 + np.array([STEP_X * b3, STEP_Y * b2, 0.0]) + BACK * b1


LINE_C, SUB0_C, SUB1_C, JOIN_C = GREY_B, BLUE_C, ORANGE, GREEN_C
IN_C, CUT_C = YELLOW_D, RED_C


class Ep05Hypercubes(NarratedScene):
    SCENES = ["the_cube", "subcubes", "counting_edges", "cutting_apart", "induction"]

    def construct(self):
        if self.preview_only(self.SCENES):
            return
        self.title_card()
        for name in self.SCENES:
            getattr(self, name)()
        self.end_card(["A hypercube joins two bit strings exactly when they differ in one bit, or it is two smaller "
                       "hypercubes with every corner joined to its twin",
                       "So an n-dimensional hypercube has n times two to the n minus one edges, which we proved "
                       "by counting degrees and by a recurrence",
                       "To cut a set of at most half the corners away from the rest, at least as many edges must "
                       "be removed as the set has corners",
                       "The proof is an induction on the number of bits, with one case for each way the set "
                       "falls into the two subcubes"])

    # ---- helpers ---------------------------------------------------------------------
    def _swap_head(self, text):
        new = self.heading(text)
        old = getattr(self, "_head", None)
        anims = [Write(new)] if old is None else [FadeOut(old, run_time=0.5), Write(new)]
        self._head = new
        return anims

    def _build_cube(self):
        self.vert = {}
        for b in V3:
            c = Circle(radius=R_V, stroke_color=BLUE_C, stroke_width=3,
                       fill_color=BLUE_E, fill_opacity=0.35).move_to(pos(b))
            self.vert[b] = VGroup(c, mono(b, 20, WHITE).next_to(c, ORIGIN))
        self.edg = {ekey(a, b): Line(pos(a), pos(b), buff=R_V, stroke_color=LINE_C, stroke_width=3)
                    for a, b in E3}
        self.edge_group = VGroup(*self.edg.values())
        self.vert_group = VGroup(*self.vert.values())
        self.cube = VGroup(self.edge_group, self.vert_group)

    def _paint(self, tint=None, chosen=(), edge_colors=None):
        """Animations that put every corner and edge into one stated colour state."""
        tint, edge_colors = tint or {}, edge_colors or {}
        anims = []
        for b, v in self.vert.items():
            on = b in chosen
            anims.append(v[0].animate.set_stroke(tint.get(b, BLUE_C))
                         .set_fill(IN_C if on else BLUE_E, 0.75 if on else 0.35))
        for e, line in self.edg.items():
            anims.append(line.animate.set_color(edge_colors.get(e, LINE_C)))
        return anims

    def _stack(self, items):
        """Short mono labels, one under the other, to the right of the cube. items = (text, color)."""
        g = VGroup(*[mono(t, 26, c) for t, c in items])
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(self.cube, RIGHT, buff=0.7)
        return g

    # ---- scene 1: the direct definition ----------------------------------------------
    def the_cube(self):
        self._build_cube()
        panel = self._stack([("differ in one bit", IN_C), ("3 neighbours each", GREEN_B),
                             ("20 bits: 2^20 corners", ORANGE), ("20 neighbours each", GREEN_B)])
        one, nbrs, big, twenty = panel
        e0 = self.edg[ekey("000", "001")]

        # beat 1: the corners and their names
        self.say("Here is a cube whose eight corners each carry a name made of three bits. "
                 "So the corner at the front left is zero zero zero, and the corner above it is "
                 "zero one zero.",
                 *self._swap_head("The hypercube"),
                 LaggedStart(*[FadeIn(v, scale=0.7) for v in self.vert.values()], lag_ratio=0.1))
        self.cue("front left", Indicate(self.vert["000"], color=IN_C))
        self.cue("above it", Indicate(self.vert["010"], color=IN_C))

        # beat 2: the rule for an edge
        self.say("Now we join two corners by an edge exactly when their names differ in one single bit. "
                 "So zero zero zero and zero zero one are neighbours, since only the last bit changes. "
                 "In all, the cube has twelve such edges.",
                 FadeIn(one, shift=LEFT * 0.2))
        self.cue("join two corners", LaggedStart(*[Create(e) for e in self.edg.values()], lag_ratio=0.1))
        self.cue("zero zero zero and zero zero one",
                 e0.animate.set_color(IN_C), Indicate(self.vert["000"], color=IN_C),
                 Indicate(self.vert["001"], color=IN_C))
        self.cue("twelve such edges", Indicate(self.edge_group, color=IN_C))

        # beat 3: a pair that is not joined, and the degree
        self.say("But zero zero zero and zero one one differ in two bits, so no edge joins them. "
                 "That means a corner has one neighbour for every bit that can be flipped, which is three "
                 "neighbours for each corner here.",
                 e0.animate.set_color(LINE_C), Indicate(self.vert["011"], color=CUT_C),
                 Indicate(self.vert["000"], color=CUT_C))
        self.cue("three neighbours", FadeIn(nbrs, shift=LEFT * 0.2),
                 Indicate(VGroup(*[self.edg[ekey("000", b)] for b in ("001", "010", "100")]), color=GREEN_B))

        # beat 4: n bits, the Connection Machine
        self.say("With n bits the same rule gives two to the n corners, and each one has n neighbours. "
                 "The Connection Machine of the nineteen eighties used twenty bits, so it joined about a "
                 "million processors that each had only twenty neighbours. "
                 "Wiring every pair directly would have needed about half a trillion wires.",
                 FadeIn(big, shift=LEFT * 0.2))
        self.cue("only twenty neighbours", FadeIn(twenty, shift=LEFT * 0.2))
        self.hold(0.5)
        self.panel1 = panel

    # ---- scene 2: the recursive definition -------------------------------------------
    def subcubes(self):
        v0 = {b: SUB0_C for b in V3 if b[0] == "0"}
        v1 = {b: SUB1_C for b in V3 if b[0] == "1"}
        e0 = {ekey(*e): SUB0_C for e in SUB0}
        e1 = {ekey(*e): SUB1_C for e in SUB1}
        ej = {ekey(*e): JOIN_C for e in JOIN}
        lines = self._stack([("0-subcube: front", SUB0_C), ("1-subcube: back", SUB1_C),
                             ("4 joining edges", JOIN_C), ("12 = 4 + 4 + 4", WHITE)])
        l0, l1, lj, total = lines

        # beat 1: the front square
        self.say("Now look at the same cube a second way. "
                 "The four corners whose names start with zero form a square at the front, "
                 "and we call it the zero subcube.",
                 *self._swap_head("Two copies of a smaller cube"), FadeOut(self.panel1),
                 *self._paint(tint=v0, edge_colors=e0))
        self.cue("the zero subcube", FadeIn(l0, shift=LEFT * 0.2))

        # beat 2: the back square
        self.say("The four corners whose names start with one form a second square at the back, "
                 "which is the one subcube. "
                 "Each square is a two dimensional hypercube, and the first bit is simply copied onto "
                 "every name.",
                 *self._paint(tint={**v0, **v1}, edge_colors={**e0, **e1}))
        self.cue("the one subcube", FadeIn(l1, shift=LEFT * 0.2))

        # beat 3: the joining edges
        self.say("The four edges left over join each corner of the front square to the corner behind it, "
                 "which has the same last two bits. "
                 "So zero one zero is joined to one one zero, and the first bit is the only one that "
                 "changes.",
                 *self._paint(tint={**v0, **v1}, edge_colors={**e0, **e1, **ej}))
        self.cue("four edges left over", FadeIn(lj, shift=LEFT * 0.2))
        self.cue("zero one zero is joined",
                 Indicate(self.vert["010"], color=JOIN_C), Indicate(self.vert["110"], color=JOIN_C),
                 Indicate(self.edg[ekey("010", "110")], color=WHITE))

        # beat 4: the second definition and its count
        self.say("That is the second definition, which takes two copies of the smaller hypercube and "
                 "joins every corner to its twin. "
                 "So the cube has twelve edges, which is twice the four edges of a square plus four "
                 "joining edges.",
                 Indicate(self.cube, color=WHITE))
        self.cue("twelve edges", FadeIn(total, shift=LEFT * 0.2))
        self.hold(0.5)
        self.panel2 = lines

    # ---- scene 3: Lemma 10.1 ---------------------------------------------------------
    def counting_edges(self):
        lemma = mono("E = n * 2^(n-1)", 32, IN_C).next_to(self.cube, DOWN, buff=0.25)
        p1 = self._stack([("8 corners * 3", GREEN_B), ("= 24 edge ends", GREEN_B),
                          ("24 / 2 = 12 edges", IN_C)])
        a, b, c = p1
        rec = self._stack([("E(n) = 2E(n-1) + 2^(n-1)", IN_C), ("E(1) = 1", WHITE),
                           ("E(2) = 2*1 + 2 = 4", WHITE), ("E(3) = 2*4 + 4 = 12", WHITE),
                           ("E(4) = 2*12 + 8 = 32", WHITE)])
        step = mono("(n-1)*2^(n-1) + 2^(n-1) = n*2^(n-1)", 24, GREEN_B).next_to(rec, DOWN, buff=0.4)
        step.align_to(rec, LEFT)
        around = VGroup(*[self.edg[ekey("000", t)] for t in ("001", "010", "100")])

        # beat 1: the lemma
        self.say("Lemma ten point one counts the edges of the hypercube, and it says the answer is "
                 "n times two to the n minus one. "
                 "We will prove it twice, once from each definition, and the cube with its twelve edges "
                 "is our test case.",
                 *self._swap_head("Lemma 10.1"), FadeOut(self.panel2),
                 *self._paint(), FadeIn(lemma, shift=UP * 0.2))
        self.cue("twelve edges", Indicate(self.edge_group, color=IN_C))

        # beat 2: proof 1, degrees
        self.say("The first proof uses the direct definition, in which every corner has exactly n neighbours, "
                 "one for each bit that can be flipped. "
                 "So in our cube each of the eight corners has degree three.",
                 Indicate(self.vert["000"], color=IN_C), around.animate.set_color(GREEN_B))
        self.cue("each of the eight corners", Indicate(self.vert_group, color=GREEN_B), FadeIn(a))

        # beat 3: counting each edge twice
        self.say("Adding up the degrees counts every edge twice, once from each of its two ends. "
                 "So eight times three is twenty four ends, and half of that is twelve edges. "
                 "In general that is n times two to the n, divided by two, which is n times two to the "
                 "n minus one.",
                 *self._paint(), FadeIn(b))
        self.cue("half of that", FadeIn(c))

        # beat 4: proof 2, the recurrence
        self.say("The second proof uses the recursive definition instead. "
                 "A hypercube is two smaller hypercubes plus the edges joining twins, so the edge count "
                 "E of n equals twice E of n minus one, plus two to the n minus one.",
                 FadeOut(p1), FadeIn(rec[0]), *[e.animate.set_color(JOIN_C) for e in
                                                  [self.edg[ekey(*x)] for x in JOIN]])
        self.cue("two smaller hypercubes", *self._paint(
            tint={**{x: SUB0_C for x in V3 if x[0] == "0"}, **{x: SUB1_C for x in V3 if x[0] == "1"}},
            edge_colors={**{ekey(*e): SUB0_C for e in SUB0}, **{ekey(*e): SUB1_C for e in SUB1},
                         **{ekey(*e): JOIN_C for e in JOIN}}))

        # beat 5: the table
        self.say("Start from one edge for the one dimensional cube, and the rule gives four for the square. "
                 "Then it gives twelve for the cube, and one more step gives thirty two, "
                 "which matches four times two cubed.",
                 FadeIn(rec[1]), FadeIn(rec[2]))
        self.cue("Then it gives twelve", FadeIn(rec[3]))
        self.cue("thirty two", FadeIn(rec[4]))

        # beat 6: the induction idea
        self.say("To prove it for every n, assume the formula holds for one fewer bit, "
                 "so doubling it gives n minus one times two to the n minus one. "
                 "Then adding the joining edges, two to the n minus one more, makes it n times two to the "
                 "n minus one.",
                 FadeIn(step))
        self.cue("adding the joining edges", Indicate(step, color=IN_C))
        self.hold(0.5)
        self.old = [lemma, rec, step]

    # ---- scene 4: Theorem 10.5, the statement ----------------------------------------
    def cutting_apart(self):
        lemma, rec, step = self.old
        panel = self._stack([("S = chosen corners", IN_C), ("|S| <= 2^(n-1)", WHITE),
                             ("cut edges >= |S|", CUT_C)])
        s_lab, s_size, s_cut = panel
        cut1 = {ekey(*e): CUT_C for e in cut_edges(S_ONE)}
        cut4 = {ekey(*e): CUT_C for e in cut_edges(S_FACE)}

        # beat 1: one corner
        self.say("Now ask how hard it is to cut a group of corners away from the rest of the cube. "
                 "Take just the corner zero zero zero, and the three edges leaving it must all be cut.",
                 *self._swap_head("Theorem 10.5"), FadeOut(lemma), FadeOut(rec), FadeOut(step),
                 *self._paint(chosen=S_ONE, edge_colors=cut1))
        self.cue("three edges leaving it", Indicate(VGroup(*[self.edg[k] for k in cut1]), color=WHITE),
                 FadeIn(s_lab, shift=LEFT * 0.2))

        # beat 2: the front square
        self.say("Take instead all four corners of the front square, which is the zero subcube. "
                 "Now exactly four edges leave it, and those are the four joining edges, "
                 "so four edges are cut for four corners.",
                 *self._paint(chosen=S_FACE, edge_colors=cut4))
        self.cue("exactly four edges", Indicate(VGroup(*[self.edg[k] for k in cut4]), color=WHITE))

        # beat 3: the theorem
        self.say("Theorem ten point five says that this always happens. "
                 "Whenever S holds at most half of all the corners, at least as many edges leave S "
                 "as S has corners.",
                 FadeIn(s_size, shift=LEFT * 0.2))
        self.cue("at least as many edges", FadeIn(s_cut, shift=LEFT * 0.2))
        self.hold(0.5)
        self.panel4 = panel

    # ---- scene 5: Theorem 10.5, the induction ----------------------------------------
    def induction(self):
        f1 = {ekey(*e): CUT_C for e in C1_FRONT + C1_BACK}
        tiny_c = [Circle(radius=0.3, stroke_color=BLUE_C, stroke_width=3, fill_color=BLUE_E,
                         fill_opacity=0.35) for _ in range(2)]
        tiny = VGroup(tiny_c[0], tiny_c[1]).arrange(RIGHT, buff=1.2)
        tiny_l = VGroup(mono("0", 22, WHITE).move_to(tiny_c[0]), mono("1", 22, WHITE).move_to(tiny_c[1]))
        tiny_e = Line(tiny_c[0].get_center(), tiny_c[1].get_center(), buff=0.3, stroke_color=CUT_C,
                      stroke_width=3)
        mini = VGroup(tiny, tiny_l, tiny_e).next_to(self.cube, RIGHT, buff=1.0)
        case1 = self._stack([("case 1: both parts", GREEN_B), ("front >= 2", WHITE),
                             ("back >= 2", WHITE), ("total >= 4 = |S|", IN_C)])
        case2 = self._stack([("case 2: S0 is big", GREEN_B), ("back >= 1", WHITE),
                             ("front >= 4 - 3 = 1", WHITE), ("joining >= 3 - 1 = 2", WHITE),
                             ("total >= 4 = |S|", IN_C)])
        zero_e = {ekey(*C2_BACK): CUT_C}
        c2_back = {ekey(*C2_BACK): CUT_C}
        c2_front = {**c2_back, ekey(*C2_FRONT): CUT_C}
        c2_all = {**c2_front, **{ekey(*e): CUT_C for e in C2_JOIN}}
        tint = {**{b: SUB0_C for b in V3 if b[0] == "0"}, **{b: SUB1_C for b in V3 if b[0] == "1"}}

        # beat 1: the base case
        self.say("We prove it by induction on the number of bits. "
                 "With one bit there are two corners and one edge, so a set of one corner is cut off "
                 "by exactly that one edge.",
                 *self._swap_head("The induction"), FadeOut(self.panel4), FadeIn(mini),
                 *self._paint())
        self.cue("exactly that one edge", Indicate(tiny_e, color=WHITE))

        # beat 2: the step
        self.say("For the step, split S into S zero in the front subcube and S one in the back one, "
                 "where S zero is the larger part. "
                 "Then either both parts are at most half of their subcube, or S zero is more than half.",
                 FadeOut(mini), *self._paint(tint=tint, chosen=S_C1,
                                             edge_colors={ekey(*e): LINE_C for e in E3}))
        self.cue("S zero in the front subcube", Indicate(VGroup(*[self.vert[b] for b in S0_C1]), color=IN_C))
        self.cue("S one in the back one", Indicate(VGroup(*[self.vert[b] for b in S1_C1]), color=IN_C))

        # beat 3: case 1
        self.say("In the first case the hypothesis applies inside each subcube separately. "
                 "So at least two edges leave S zero inside the front, and at least two leave S one "
                 "inside the back, which gives at least four, as many as S has corners.",
                 FadeIn(case1[0], shift=LEFT * 0.2),
                 *self._paint(tint=tint, chosen=S_C1, edge_colors={ekey(a, b): CUT_C for a, b in C1_FRONT}))
        self.cue("at least two leave S one",
                 *self._paint(tint=tint, chosen=S_C1, edge_colors=f1), FadeIn(case1[1]))
        self.cue("at least four", FadeIn(case1[2]), FadeIn(case1[3]))

        # beat 4: case 2, the small part
        self.say("In the second case S zero is more than half of the front subcube, so the hypothesis "
                 "cannot be used on it directly. "
                 "In our cube S zero has three corners and S one has one, which is small enough to give "
                 "at least one edge in the back.",
                 FadeOut(case1), *self._paint(tint=tint, chosen=S_C2))
        self.cue("small enough", FadeIn(case2[0], shift=LEFT * 0.2),
                 *self._paint(tint=tint, chosen=S_C2, edge_colors=zero_e), FadeIn(case2[1]))

        # beat 5: the complement
        self.say("The trick is to look at the front corners outside S zero, which here is the single corner "
                 "zero one one. "
                 "That set is small, so the hypothesis gives at least one edge between it and S zero.",
                 Indicate(self.vert["011"], color=CUT_C))
        self.cue("at least one edge between", *self._paint(tint=tint, chosen=S_C2, edge_colors=c2_front),
                 FadeIn(case2[2]))

        # beat 6: the joining edges
        self.say("Finally every corner of S zero has a twin behind it, and at most one of those twins is in S one. "
                 "So at least three minus one, which is two, joining edges cross, "
                 "and one plus one plus two is four, the number of corners of S. "
                 "In general the three parts add up to two to the k, and that is at least the size of S.",
                 Indicate(VGroup(*[self.vert[b] for b in S0_C2]), color=IN_C))
        self.cue("two, joining edges cross", *self._paint(tint=tint, chosen=S_C2, edge_colors=c2_all),
                 FadeIn(case2[3]))
        self.cue("one plus one plus two", FadeIn(case2[4]))
        self.hold(0.5)
