"""Episode 4 of the CS70 Note 10 series: planar graphs, Euler's formula, and K5 / K3,3.

FACTS come from cs70/note10-deepseek/notes.txt, section 4 (lines 308-410). The figures of
the notes did not survive the text extraction, so the graphs are rebuilt here from the
text. The picture reads the names below; the narration says numbers as words, and every
spoken number has an assert here.
"""
import os
import sys
from collections import Counter
from itertools import combinations
from math import comb

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403


def ek(a, b):
    """An undirected edge as a sorted pair."""
    return tuple(sorted((a, b)))


def cycle_edges(cycle):
    """The edges along a closed list of vertices (the sides of a face)."""
    return [ek(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))]


def check_faces(edges, faces, v):
    """Every edge is a side of exactly two faces (one on each side, a bridge twice for the
    same face), and Euler's formula holds. Returns (v, e, f)."""
    sides = Counter(s for face in faces for s in face)
    assert set(sides) == set(edges) and all(n == 2 for n in sides.values())
    e, f = len(edges), len(faces)
    assert sum(len(face) for face in faces) == 2 * e
    assert v + f == e + 2
    return v, e, f


# ---- FACTS ---------------------------------------------------------------------------
# K4: four vertices, every pair joined (the example the episode starts with).
K4_V = (1, 2, 3, 4)
E_K4 = [(1, 2), (2, 3), (3, 1), (1, 4), (2, 4), (3, 4)]          # drawing order
assert sorted(ek(*e) for e in E_K4) == sorted(ek(a, b) for a, b in combinations(K4_V, 2))
K4_FACES = [cycle_edges(c) for c in ((1, 2, 4), (2, 3, 4), (3, 1, 4), (1, 2, 3))]  # last = outer
K4_N = check_faces([ek(*e) for e in E_K4], K4_FACES, 4)
assert K4_N == (4, 6, 4)                                          # "four", "six", "four"
assert all(len(f) == 3 for f in K4_FACES) and sum(len(f) for f in K4_FACES) == 12  # "three", "twelve"
assert 4 + 4 == 8 == 6 + 2                                        # "eight"

# The cube drawn flat: a square inside a square. 0-3 outer corners, 4-7 inner corners.
CUBE_V = tuple(range(8))
E_CUBE = ([(i, (i + 1) % 4) for i in range(4)] + [(4 + i, 4 + (i + 1) % 4) for i in range(4)]
          + [(i, i + 4) for i in range(4)])
CUBE_CYCLES = ([(0, 1, 2, 3), (4, 5, 6, 7)]
               + [(i, (i + 1) % 4, 4 + (i + 1) % 4, 4 + i) for i in range(4)])
CUBE_N = check_faces([ek(*e) for e in E_CUBE], [cycle_edges(c) for c in CUBE_CYCLES], 8)
assert CUBE_N == (8, 12, 6)                                       # "eight", "twelve", "six"
assert 8 + 6 == 14 == 12 + 2                                      # "fourteen"

# The induction on K4 (scene 2): delete a cycle edge, two faces merge. Faces are lists of sides.
# (an edge that has the same face on both sides, a bridge, is listed twice in that face.)
STAGES = [
    (E_K4, [[(1, 2), (2, 4), (1, 4)], [(2, 3), (3, 4), (2, 4)], [(1, 3), (1, 4), (3, 4)],
            [(1, 2), (2, 3), (1, 3)]]),
    (E_K4[:5], [[(1, 2), (2, 4), (1, 4)], [(2, 3), (2, 4), (1, 3), (1, 4)], [(1, 2), (2, 3), (1, 3)]]),
    ([E_K4[i] for i in (0, 1, 2, 4)],
     [[(1, 2), (2, 4), (2, 4), (2, 3), (1, 3)], [(1, 2), (2, 3), (1, 3)]]),
    ([E_K4[i] for i in (0, 1, 4)], [[(1, 2), (2, 4), (2, 4), (2, 3), (1, 2), (2, 3)]]),
]
STAGE_N = [check_faces([ek(*e) for e in es], [[ek(*s) for s in f] for f in fs], 4) for es, fs in STAGES]
assert STAGE_N == [(4, 6, 4), (4, 5, 3), (4, 4, 2), (4, 3, 1)]
assert STAGE_N[-1][1] == STAGE_N[-1][0] - 1 and STAGE_N[-1][2] == 1   # the tree: e = v - 1, f = 1
assert all(a[1] - b[1] == 1 and a[2] - b[2] == 1 for a, b in zip(STAGE_N, STAGE_N[1:]))
assert (1 + 1, 0 + 2) == (2, 2)                                   # the single vertex: one plus one is zero plus two

# The bound: 3f <= 2e with f = e + 2 - v gives e <= 3v - 6 (all f, e, v nonnegative integers).
for _v in range(3, 40):
    for _e in range(0, 3 * _v):
        _f = _e + 2 - _v
        assert (3 * _f <= 2 * _e) == (_e <= 3 * _v - 6)
assert 3 * 4 - 6 == 6 == K4_N[1]                                  # K4 meets the bound exactly
N_BIG = 1000
MIN_EDGES, MAX_EDGES, MAX_PLANAR = N_BIG - 1, comb(N_BIG, 2), 3 * N_BIG - 6
assert (MIN_EDGES, MAX_EDGES, MAX_PLANAR) == (999, 499500, 2994)  # "nine hundred ninety nine", "half a million", ...

# K5
K5_V, K5_E = 5, comb(5, 2)
assert K5_E == 5 * 4 // 2 == 10 and 3 * K5_V - 6 == 9 and K5_E > 3 * K5_V - 6
# K3,3: three houses, three wells. 4f <= 2e with f = e + 2 - v gives e <= 2v - 4.
K33_H, K33_W = (1, 2, 3), (4, 5, 6)
K33_EDGES = [(h, w) for h in K33_H for w in K33_W]
K33_V, K33_E = 6, len(K33_EDGES)
assert (K33_V, K33_E) == (6, 9) and 3 * K33_V - 6 == 12 and K33_E <= 12
assert not any(ek(a, b) in {ek(*e) for e in K33_EDGES} for a, b in combinations(K33_H, 2))  # no house-house edge
assert not any(ek(a, b) in {ek(*e) for e in K33_EDGES} for a, b in combinations(K33_W, 2))  # no well-well edge
for _v in range(3, 40):
    for _e in range(0, 3 * _v):
        _f = _e + 2 - _v
        assert (4 * _f <= 2 * _e) == (_e <= 2 * _v - 4)
assert 2 * K33_V - 4 == 8 and K33_E > 8

# Geometry. Everything between y = -2.9 and 3.3 and x = +-6.8.
POS_A = {1: (-4.8, 1.7), 2: (-2.0, 1.7), 3: (-2.0, -1.1), 4: (-4.8, -1.1)}       # square, diagonals cross
POS_B = {1: (-3.4, 2.2), 2: (-1.4, -1.2), 3: (-5.4, -1.2), 4: (-3.4, -0.1)}     # triangle, centre vertex
for _p in (POS_A, POS_B):
    _p.update({k: np.array([*v, 0.0]) for k, v in _p.items()})
CUBE_POS = {0: (1.1, 2.0), 1: (4.1, 2.0), 2: (4.1, -1.0), 3: (1.1, -1.0),
            4: (1.75, 1.35), 5: (3.45, 1.35), 6: (3.45, -0.35), 7: (1.75, -0.35)}
CUBE_POS = {k: np.array([*v, 0.0]) for k, v in CUBE_POS.items()}
R_V = 0.17
EDGE_C, FACE_C, BAD_C, OK_C = BLUE_B, YELLOW_D, RED_C, GREEN_C
HOUSE_C, WELL_C = ORANGE, BLUE_C
LE, MINUS = "≤", "−"


def vdot(p, color=BLUE_C, r=R_V):
    return Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=color,
                  fill_opacity=0.35).move_to(p)


def seg(p, q, color=EDGE_C, r=R_V, width=3):
    """A line between two vertex circles, ending at their edges."""
    d = (q - p) / np.linalg.norm(q - p)
    return Line(p + d * r, q - d * r, stroke_color=color, stroke_width=width)


def graph(pos, edges, colors=None):
    """(nodes, lines): one circle per key of pos (in key order), one line per edge (in order)."""
    keys = sorted(pos)
    nodes = VGroup(*[vdot(pos[k], (colors or {}).get(k, BLUE_C)) for k in keys])
    lines = VGroup(*[seg(pos[a], pos[b]) for a, b in edges])
    return nodes, lines


def centroid(pos, cycle):
    return sum(pos[k] for k in cycle) / len(cycle)


def poly(pos, cycle, color=FACE_C, opacity=0.28):
    return Polygon(*[pos[k] for k in cycle], stroke_width=0, fill_color=color, fill_opacity=opacity)


def counts(v, f, e, color=FACE_C, size=34):
    return mono(f"{v} + {f} = {e} + 2", size, color)


class Ep04Planar(NarratedScene):
    SCENES = ["planar_and_faces", "euler_induction", "edge_bound", "two_graphs", "kuratowski"]

    def construct(self):
        if self.preview_only(self.SCENES):
            return
        self.title_card()
        for name in self.SCENES:
            getattr(self, name)()
        self.end_card(["A graph is planar when it can be drawn on the plane with no crossings, and a planar "
                       "drawing cuts the plane into faces",
                       "Euler's formula says that vertices plus faces equals edges plus two for every connected "
                       "planar graph",
                       "So a planar graph has at most three times its vertices minus six edges, which rules out "
                       "the complete graph on five vertices",
                       "The houses and wells graph needs the sharper bound, and a graph is non-planar exactly "
                       "when it contains one of these two graphs"])

    # ---- helpers ---------------------------------------------------------------------
    def _swap_head(self, text):
        new = self.heading(text)
        old = getattr(self, "_head", None)
        anims = [Write(new)] if old is None else [FadeOut(old, run_time=0.5), Write(new)]
        self._head = new
        return anims

    def _fresh(self):
        """Clear the stage between scenes; the heading is swapped by the first beat."""
        self.clear_stage()
        self._head = None

    def _face_marks(self, values, color=FACE_C):
        """The number of each face of K4 in the planar drawing (three inner faces, then the
        outer one at the left of the drawing, with the word outer under it)."""
        inner = [num(str(values[i]), 26, color).move_to(centroid(POS_B, c))
                 for i, c in enumerate(((1, 2, 4), (2, 3, 4), (3, 1, 4)))]
        outer = num(str(values[3]), 26, color).move_to(POS_B[3] + LEFT * 0.95)
        word = txt("outer", 22, GREY_A).next_to(outer, DOWN, buff=0.1)
        return VGroup(*inner), VGroup(outer, word)

    # ---- scene 1: planar, faces, the formula -------------------------------------------
    def planar_and_faces(self):
        nodes, edges = graph(POS_A, E_K4)
        nodes_b, edges_b = graph(POS_B, E_K4)
        planar = txt("planar", 34, OK_C).next_to(edges_b, RIGHT, buff=0.7)
        inner, outer = self._face_marks((1, 2, 3, 4))
        rule = mono("v + f = e + 2", 30, GREEN_B)
        k4_sum = counts(*[K4_N[0], K4_N[2], K4_N[1]])
        k4_formula = VGroup(rule, k4_sum).arrange(DOWN, buff=0.15).next_to(edges_b, DOWN, buff=0.35)
        c_nodes, c_edges = graph(CUBE_POS, E_CUBE)
        c_marks = VGroup(num("1", 22, FACE_C).move_to(centroid(CUBE_POS, CUBE_CYCLES[1])),
                         *[num(str(i + 2), 22, FACE_C).move_to(centroid(CUBE_POS, CUBE_CYCLES[2 + i]))
                           for i in range(4)],
                         num("6", 22, FACE_C).move_to(CUBE_POS[0] + UL * 0.5))
        c_sum = counts(CUBE_N[0], CUBE_N[2], CUBE_N[1]).next_to(c_edges, DOWN, buff=0.35)

        # beat 1: K4 drawn with a crossing, then without one
        self.say("Here is a graph with four vertices in which every vertex is joined to every other one, "
                 "so it has six edges. Drawn as a square with both diagonals, two of its edges cross in the "
                 "middle. Now we move one vertex into the middle, and the same six edges are drawn with no "
                 "crossing at all.",
                 *self._swap_head("Planar graphs"),
                 LaggedStart(*[FadeIn(n, scale=0.6) for n in nodes], lag_ratio=0.12),
                 LaggedStart(*[Create(e) for e in edges], lag_ratio=0.12))
        self.cue("two of its edges cross", Indicate(VGroup(edges[2], edges[4]), color=BAD_C))
        self.cue("we move one vertex",
                 Transform(nodes, nodes_b), Transform(edges, edges_b), run_time=1.6)

        # beat 2: the word planar
        self.say("A graph is called planar when it can be drawn on the plane with no crossings. "
                 "The first drawing had a crossing, but the second drawing has none, so this graph is planar.",
                 FadeIn(planar, shift=LEFT * 0.2))
        self.cue("second drawing has none", Indicate(edges, color=OK_C))

        # beat 3: faces and the formula
        self.say("The edges cut the plane into regions that we call faces. Our drawing has three small "
                 "triangles inside and one infinite face outside, so there are four faces in all. "
                 "Counting vertices plus faces gives four plus four, which is eight, and edges plus two gives "
                 "six plus two, which is eight as well.",
                 LaggedStart(*[FadeIn(m, scale=0.6) for m in inner], lag_ratio=0.3))
        self.cue("one infinite face outside", FadeIn(outer))
        self.cue("Counting vertices plus faces", FadeIn(rule), FadeIn(k4_sum))
        self.cue("six plus two", Indicate(k4_sum, color=FACE_C))

        # beat 4: the cube, and the history
        self.say("The cube drawn flat has eight vertices, twelve edges and six faces, and eight plus six "
                 "is twelve plus two. The ancient Greeks knew the formula for polyhedra like this cube, "
                 "but they could not prove it. Euler saw that planar graphs are the right setting for a "
                 "proof, and that is the version we prove next.",
                 LaggedStart(*[FadeIn(n, scale=0.6) for n in c_nodes], lag_ratio=0.08),
                 LaggedStart(*[Create(e) for e in c_edges], lag_ratio=0.08))
        self.cue("six faces", LaggedStart(*[FadeIn(m, scale=0.6) for m in c_marks], lag_ratio=0.15))
        self.cue("eight plus six", FadeIn(c_sum))
        self.cue("The ancient Greeks", Indicate(c_edges, color=FACE_C))
        self.cue("planar graphs are the right setting", Indicate(edges, color=OK_C))
        self.hold(0.5)

    # ---- scene 2: Theorem 10.3, the induction ------------------------------------------
    def euler_induction(self):
        self._fresh()
        nodes, edges = graph(POS_B, E_K4)
        rule = mono("v + f = e + 2", 30, GREEN_B)
        cnt = counts(*[STAGE_N[0][0], STAGE_N[0][2], STAGE_N[0][1]])
        panel = VGroup(rule, cnt).arrange(DOWN, buff=0.15).next_to(edges, DOWN, buff=0.35)
        dot = vdot(np.array([3.0, 0.9, 0.0]), r=0.28)
        dot_cnt = counts(1, 1, 0).next_to(dot, DOWN, buff=0.45)
        ghost = DashedLine(POS_B[3] + (POS_B[4] - POS_B[3]) / np.linalg.norm(POS_B[4] - POS_B[3]) * R_V,
                           POS_B[4] - (POS_B[4] - POS_B[3]) / np.linalg.norm(POS_B[4] - POS_B[3]) * R_V,
                           stroke_color=GREY_B, stroke_width=3)
        tint_bottom = poly(POS_B, (2, 3, 4))
        tint_left = poly(POS_B, (3, 1, 4))
        tint_merged = poly(POS_B, (1, 3, 2, 4))
        tint_right = poly(POS_B, (1, 2, 4))
        tint_inner = poly(POS_B, (1, 3, 2))

        # beat 1: the theorem on our example
        self.say("Theorem ten point three says that every connected planar graph satisfies vertices plus faces "
                 "equals edges plus two. We prove it by induction on the number of edges, using our four "
                 "vertex graph as the example. Right now it has six edges and four faces, and four plus four "
                 "is six plus two.",
                 *self._swap_head("Theorem 10.3"),
                 LaggedStart(*[FadeIn(n, scale=0.6) for n in nodes], lag_ratio=0.1),
                 LaggedStart(*[Create(e) for e in edges], lag_ratio=0.1))
        self.cue("equals edges plus two", FadeIn(rule))
        self.cue("six edges and four faces", FadeIn(cnt))

        # beat 2: the base case
        self.say("The smallest case has no edges at all, just one vertex and one face, and one plus one is "
                 "zero plus two. So the formula holds for the base case, and every bigger graph will be "
                 "reduced to a smaller one.",
                 FadeIn(dot, scale=0.5))
        self.cue("one plus one", FadeIn(dot_cnt))

        # beat 3: delete a cycle edge
        self.say("Now take a graph with a cycle and delete one edge of it, so the two faces beside that "
                 "edge merge into one. Edges and faces each drop by one, so four plus three equals five plus "
                 "two for the smaller graph. By induction the smaller graph obeys the formula, and putting "
                 "the edge back adds one to both sides.",
                 FadeOut(dot), FadeOut(dot_cnt), FadeIn(tint_bottom), FadeIn(tint_left))
        self.cue("merge into one", FadeOut(edges[5]), FadeOut(tint_bottom), FadeOut(tint_left),
                 FadeIn(tint_merged))
        self.cue("Edges and faces each drop by one",
                 Transform(cnt, counts(STAGE_N[1][0], STAGE_N[1][2], STAGE_N[1][1]).move_to(cnt)))
        self.cue("putting the edge back", FadeIn(ghost), Indicate(cnt, color=FACE_C))

        # beat 4: repeat until a tree is left
        self.say("We keep deleting cycle edges until no cycle is left, and what remains is a tree. "
                 "A tree does not cut the plane, so it has one face and one edge fewer than vertices. "
                 "Four vertices, three edges and one face fit the formula, which completes the induction.",
                 FadeOut(ghost), FadeIn(tint_right))
        self.cue("until no cycle is left",
                 FadeOut(edges[3]), FadeOut(tint_merged), FadeOut(tint_right), FadeIn(tint_inner),
                 Transform(cnt, counts(STAGE_N[2][0], STAGE_N[2][2], STAGE_N[2][1]).move_to(cnt)))
        self.cue("what remains is a tree",
                 FadeOut(edges[2]), FadeOut(tint_inner),
                 Transform(cnt, counts(STAGE_N[3][0], STAGE_N[3][2], STAGE_N[3][1]).move_to(cnt)))
        self.cue("one face and one edge fewer",
                 Indicate(VGroup(edges[0], edges[1], edges[4]), color=OK_C))
        self.cue("three edges and one face", Indicate(cnt, color=FACE_C))
        self.hold(0.5)

    # ---- scene 3: the bound on edges ------------------------------------------------
    def edge_bound(self):
        self._fresh()
        nodes, edges = graph(POS_B, E_K4)
        marks_in, marks_out = self._face_marks((3, 3, 3, 3), GREEN_B)
        lines = [mono("3 + 3 + 3 + 3 = 12", 28, GREEN_B),
                 mono("sides in all = 2e", 28, GREEN_B),
                 mono(f"3f {LE} 2e", 30, FACE_C),
                 mono(f"3(e + 2 {MINUS} v) {LE} 2e", 30, FACE_C),
                 mono(f"e {LE} 3v {MINUS} 6", 34, OK_C),
                 mono(f"3·4 {MINUS} 6 = 6", 28, GREEN_B)]
        panel = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        panel.next_to(edges, RIGHT, buff=0.9).align_to(edges, UP)
        bar = Rectangle(width=12.0, height=0.45, stroke_color=GREY_B, stroke_width=2,
                        fill_color=BLUE_E, fill_opacity=0.35).move_to([0, -1.9, 0])
        share = (MAX_PLANAR - MIN_EDGES) / (MAX_EDGES - MIN_EDGES)
        sliver = Rectangle(width=12.0 * share, height=0.45, stroke_width=0,
                           fill_color=FACE_C, fill_opacity=0.95).align_to(bar, LEFT).align_to(bar, UP)
        l_low = mono(str(MIN_EDGES), 24, GREY_A).next_to(bar.get_corner(DL), DOWN, buff=0.15, aligned_edge=LEFT)
        l_high = mono(str(MAX_EDGES), 24, GREY_A).next_to(bar.get_corner(DR), DOWN, buff=0.15, aligned_edge=RIGHT)
        l_plan = mono(f"planar {LE} {MAX_PLANAR}", 26, FACE_C).next_to(sliver, UP, buff=0.35, aligned_edge=LEFT)
        l_all = txt("1000 vertices", 26, GREY_A).next_to(bar, DOWN, buff=0.3)

        # beat 1: count the sides of every face
        self.say("Count the sides of every face, where a side is an edge on the boundary of that face. "
                 "In our drawing each of the four faces has three sides, so together they have twelve. "
                 "Every edge has a face on each of its two sides, so the total is twice the edges, and twice "
                 "six is twelve.",
                 *self._swap_head("How many edges?"),
                 LaggedStart(*[FadeIn(n, scale=0.6) for n in nodes], lag_ratio=0.1),
                 LaggedStart(*[Create(e) for e in edges], lag_ratio=0.1))
        self.cue("each of the four faces has three sides",
                 LaggedStart(*[FadeIn(m, scale=0.6) for m in marks_in], lag_ratio=0.2), FadeIn(marks_out))
        self.cue("together they have twelve", FadeIn(lines[0]))
        self.cue("twice the edges", FadeIn(lines[1]))

        # beat 2: the inequality
        self.say("There are no parallel edges and at least three vertices, so every face has at least three "
                 "sides. That makes three times the faces at most twice the edges. Euler's formula gives the "
                 "faces as edges plus two minus vertices. Putting that in, the edges are at most three times "
                 "the vertices minus six.",
                 Indicate(marks_in, color=FACE_C))
        self.cue("That makes three times the faces", FadeIn(lines[2]))
        self.cue("Euler's formula gives", FadeIn(lines[3]))
        self.cue("Putting that in", FadeIn(lines[4]))

        # beat 3: planar graphs are sparse
        self.say("So planar graphs are sparse, and our four vertex graph meets the bound exactly, since three "
                 "times four minus six is six. A connected graph on a thousand vertices can have anywhere from "
                 "nine hundred ninety nine edges up to nearly half a million. If it is planar, the bound allows "
                 "at most two thousand nine hundred ninety four.",
                 Indicate(edges, color=OK_C))
        self.cue("meets the bound exactly", FadeIn(lines[5]))
        self.cue("A connected graph on a thousand vertices",
                 FadeOut(nodes), FadeOut(edges), FadeOut(marks_in), FadeOut(marks_out),
                 *[FadeOut(lines[i]) for i in (0, 1, 2, 3, 5)],
                 FadeIn(bar), FadeIn(l_low), FadeIn(l_high), FadeIn(l_all))
        self.cue("If it is planar", FadeIn(sliver), FadeIn(l_plan))
        self.hold(0.5)

    # ---- scene 4: K5 and K3,3 ------------------------------------------------------
    def two_graphs(self):
        self._fresh()
        k5_pos = {i: np.array([-3.2 + 1.7 * np.cos(np.pi / 2 + 2 * np.pi * i / 5),
                               0.2 + 1.7 * np.sin(np.pi / 2 + 2 * np.pi * i / 5), 0.0]) for i in range(5)}
        k5_edges = [(a, b) for a, b in combinations(range(5), 2)]
        assert len(k5_edges) == K5_E
        n5, e5 = graph(k5_pos, k5_edges)
        p5 = VGroup(mono("v = 5, e = 10", 30, GREEN_B),
                    mono(f"3v {MINUS} 6 = 9", 30, GREEN_B),
                    mono("10 > 9", 38, BAD_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        p5.next_to(e5, RIGHT, buff=1.0)

        k33_pos = {1: (-5.0, 1.4), 2: (-3.2, 1.4), 3: (-1.4, 1.4), 4: (-5.0, -1.0), 5: (-3.2, -1.0), 6: (-1.4, -1.0)}
        k33_pos = {k: np.array([*v, 0.0]) for k, v in k33_pos.items()}
        cols = {**{h: HOUSE_C for h in K33_H}, **{w: WELL_C for w in K33_W}}
        n33, e33 = graph(k33_pos, K33_EDGES, cols)
        houses = txt("houses", 24, HOUSE_C).next_to(n33[0], LEFT, buff=0.3)
        wells = txt("wells", 24, WELL_C).next_to(n33[3], LEFT, buff=0.3)
        no_edge = DashedLine(k33_pos[1] + RIGHT * R_V, k33_pos[2] + LEFT * R_V, stroke_color=BAD_C, stroke_width=4)
        no_lbl = txt("no edge", 24, BAD_C).next_to(no_edge, UP, buff=0.5)
        p33 = VGroup(mono("v = 6, e = 9", 26, GREEN_B),
                     mono(f"3v {MINUS} 6 = 12", 26, GREEN_B),
                     mono(f"9 {LE} 12", 26, OK_C),
                     mono(f"4f {LE} 2e", 26, FACE_C),
                     mono(f"e {LE} 2v {MINUS} 4", 26, FACE_C),
                     mono(f"2v {MINUS} 4 = 8", 26, GREEN_B),
                     mono("9 > 8", 32, BAD_C)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        p33.next_to(e33, RIGHT, buff=0.9).to_edge(UP, buff=0.7)
        k33_all = VGroup(n33, e33, houses, wells)

        # beat 1: K5
        self.say("Take the complete graph on five vertices, which is called K five. Each vertex joins the other "
                 "four, so there are five times four divided by two, which is ten edges. The bound allows at "
                 "most three times five minus six, which is nine edges, so ten is too many and K five is not "
                 "planar.",
                 *self._swap_head("K5 is not planar"),
                 LaggedStart(*[FadeIn(n, scale=0.6) for n in n5], lag_ratio=0.1),
                 LaggedStart(*[Create(e) for e in e5], lag_ratio=0.08))
        self.cue("five times four divided by two", FadeIn(p5[0]))
        self.cue("three times five minus six", FadeIn(p5[1]))
        self.cue("ten is too many", FadeIn(p5[2]), Indicate(e5, color=BAD_C))

        # beat 2: K3,3 passes the first test
        self.say("Next is the graph of three houses and three wells, where every house is joined to every well. "
                 "That gives six vertices and nine edges, while the bound allows three times six minus six, "
                 "which is twelve. So this graph passes the first test, and we have to think harder to show "
                 "it is not planar.",
                 *self._swap_head("K3,3 is trickier"),
                 FadeOut(n5), FadeOut(e5), FadeOut(p5),
                 LaggedStart(*[FadeIn(n, scale=0.6) for n in n33], lag_ratio=0.1),
                 FadeIn(houses), FadeIn(wells))
        self.cue("every house is joined to every well", LaggedStart(*[Create(e) for e in e33], lag_ratio=0.08))
        self.cue("six vertices and nine edges", FadeIn(p33[0]))
        self.cue("three times six minus six", FadeIn(p33[1]))
        self.cue("passes the first test", FadeIn(p33[2]))

        # beat 3: no triangles
        self.say("A triangle would need two houses or two wells to be joined, but houses only meet wells. "
                 "So a flat drawing would have no triangles, and every face would have at least four sides.",
                 FadeIn(no_edge), FadeIn(no_lbl))
        self.cue("no triangles", Indicate(e33, color=FACE_C))

        # beat 4: the sharper bound
        self.say("That gives four times the faces at most twice the edges, and then the edges are at most two "
                 "times the vertices minus four. For six vertices that limit is eight, but we have nine edges, "
                 "so K three three is not planar.",
                 FadeOut(no_edge), FadeOut(no_lbl), FadeIn(p33[3]))
        self.cue("the edges are at most two times", FadeIn(p33[4]))
        self.cue("that limit is eight", FadeIn(p33[5]))
        self.cue("we have nine edges", FadeIn(p33[6]), Indicate(e33, color=BAD_C))
        self.hold(0.5)

    # ---- scene 5: Kuratowski -------------------------------------------------------
    def kuratowski(self):
        self._fresh()
        s5_pos = {i: np.array([-3.4 + 1.1 * np.cos(np.pi / 2 + 2 * np.pi * i / 5),
                               0.6 + 1.1 * np.sin(np.pi / 2 + 2 * np.pi * i / 5), 0.0]) for i in range(5)}
        s5_n, s5_e = graph(s5_pos, list(combinations(range(5), 2)))
        s5_label = mono("K5", 34, GREEN_B).next_to(s5_e, DOWN, buff=0.4)
        s33_pos = {1: (1.6, 1.3), 2: (2.9, 1.3), 3: (4.2, 1.3), 4: (1.6, -0.3), 5: (2.9, -0.3), 6: (4.2, -0.3)}
        s33_pos = {k: np.array([*v, 0.0]) for k, v in s33_pos.items()}
        s33_n, s33_e = graph(s33_pos, K33_EDGES, {**{h: HOUSE_C for h in K33_H}, **{w: WELL_C for w in K33_W}})
        s33_label = mono("K3,3", 34, GREEN_B).next_to(s33_e, DOWN, buff=0.4)
        s33_label.align_to(s5_label, DOWN)

        # six blobs of two connected vertices each; red = pieces for the first side, green = the other side
        rows = (1.6, 0.1, -1.4)
        blob_pos, blob_edges, blob_shapes, inner_edges = {}, [], [], []
        for side, (cx, color) in enumerate(((-2.6, RED_C), (2.6, GREEN_C))):
            for j, y in enumerate(rows):
                a, b = np.array([cx - 0.3, y, 0.0]), np.array([cx + 0.3, y, 0.0])
                blob_pos[(side, j)] = (a, b)
                blob_shapes.append(VGroup(Ellipse(width=1.6, height=0.95, stroke_color=color, stroke_width=3,
                                                  fill_color=color, fill_opacity=0.14).move_to([cx, y, 0]),
                                          vdot(a, color), vdot(b, color)))
                inner_edges.append(seg(a, b, color))
        pieces = [(0, i) for i in range(3)] + [(1, j) for j in range(3)]
        assert len(pieces) == K33_V
        links = VGroup(*[seg(blob_pos[(0, i)][1], blob_pos[(1, j)][0], EDGE_C) for i in range(3) for j in range(3)])
        assert len(links) == K33_E
        red, green = VGroup(*blob_shapes[:3]), VGroup(*blob_shapes[3:])
        inner = VGroup(*inner_edges)
        # the same six pieces squeezed to one vertex each
        c_nodes = VGroup(*[vdot((blob_pos[p][0] + blob_pos[p][1]) / 2, RED_C if p[0] == 0 else GREEN_C)
                           for p in pieces])
        c_links = VGroup(*[seg((blob_pos[(0, i)][0] + blob_pos[(0, i)][1]) / 2,
                               (blob_pos[(1, j)][0] + blob_pos[(1, j)][1]) / 2, EDGE_C)
                           for i in range(3) for j in range(3)])

        # beat 1: the theorem
        self.say("So K five and K three three are both non-planar, and in some sense they are the only ones. "
                 "This is made exact by Kuratowski, a Polish mathematician, and the K in K five stands for his "
                 "name. Theorem ten point four says that a graph is non-planar exactly when it contains K five "
                 "or K three three.",
                 *self._swap_head("Theorem 10.4"),
                 LaggedStart(*[FadeIn(n, scale=0.6) for n in s5_n], lag_ratio=0.08),
                 LaggedStart(*[Create(e) for e in s5_e], lag_ratio=0.05),
                 FadeIn(s5_label))
        self.cue("the only ones", FadeIn(s33_n), LaggedStart(*[Create(e) for e in s33_e], lag_ratio=0.05),
                 FadeIn(s33_label))
        self.cue("exactly when it contains K five", Indicate(VGroup(s5_e, s5_label), color=FACE_C))
        self.cue("or K three three", Indicate(VGroup(s33_e, s33_label), color=FACE_C))

        # beat 2: what contains means
        self.say("Contains does not mean that a copy of K three three sits there unchanged. For each vertex of "
                 "K three three we need one connected piece of the graph, and no two pieces share a vertex. "
                 "Wherever K three three has an edge, some edge of the graph must join the two matching pieces.",
                 FadeOut(s5_n), FadeOut(s5_e), FadeOut(s5_label), FadeOut(s33_n), FadeOut(s33_e),
                 FadeOut(s33_label),
                 LaggedStart(*[FadeIn(b) for b in blob_shapes], lag_ratio=0.1),
                 *[Create(e) for e in inner_edges])
        self.cue("one connected piece", Indicate(red, color=RED_C), Indicate(green, color=GREEN_C))
        self.cue("some edge of the graph", LaggedStart(*[Create(e) for e in links], lag_ratio=0.08))

        # beat 3: contraction, the cube, the two directions
        self.say("If we squeeze every piece into a single vertex, a copy of K three three appears. "
                 "The notes use exactly this idea to show that the four-dimensional cube is not planar. "
                 "One direction is obvious, since a graph that contains a non-planar graph is itself "
                 "non-planar. The other direction is difficult, and the notes leave its proof out.",
                 *[FadeOut(b) for b in blob_shapes], FadeOut(inner), FadeIn(c_nodes),
                 Transform(links, c_links), run_time=1.6)
        self.cue("four-dimensional cube", Indicate(links, color=FACE_C))
        self.cue("One direction is obvious", Indicate(c_nodes, color=OK_C))
        self.hold(0.5)
