"""Episode 2 of the CS70 Note 10 series: the language of graphs.

FACTS come from cs70/note10-deepseek/notes.txt (lines 51-82 graphs, 90-108 neighbours,
degree, self-loops, 111-131 paths, walks, cycles, tours, 155-170 connectivity, 175-183 the
Eulerian words and Theorem 10.1). The figures of the notes did not survive the text
extraction: G2, G3 and G4 below are rebuilt from the text (see PLAN-ep02.md). The picture
reads the names below; the narration says numbers as words, and every spoken number has
an assert here.
"""
import itertools
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---- FACTS ---------------------------------------------------------------------------
# Scene 1: the Königsberg multiset of the notes (line 53-55) and the set it becomes.
LANDS = ["A", "B", "C", "D"]
BRIDGES = (("A", "B"), ("A", "B"), ("A", "C"), ("B", "C"),
           ("B", "D"), ("B", "D"), ("C", "D"))
K_DRAW = (("A", "B", 0.5), ("A", "B", -0.5), ("A", "C", None), ("B", "C", None),
          ("B", "D", 0.5), ("B", "D", -0.5), ("C", "D", None))
assert sorted((a, b) for a, b, _ in K_DRAW) == sorted(BRIDGES)
N_BRIDGES = len(BRIDGES)                                     # "seven"
K_SET = sorted(set(BRIDGES))                                 # the plain set E
N_DISTINCT = len(K_SET)                                      # five distinct pairs
DUPES = [i for i, (a, b, bend) in enumerate(K_DRAW) if bend == -0.5]   # the second copies
assert N_BRIDGES == 7 and len(LANDS) == 4 and N_DISTINCT == 5
assert DUPES == [1, 5] and len(BRIDGES) - len(DUPES) == N_DISTINCT
assert [p for p in K_SET if BRIDGES.count(p) > 1] == [("A", "B"), ("B", "D")]  # "two pairs appear twice"

# Scene 2: G1, directed (line 62), and G2, undirected (my reconstruction of the figure).
V1 = (1, 2, 3, 4)
E1 = ((1, 2), (1, 3), (1, 4))                                # "three ordered pairs"
assert (1, 2) in E1 and (2, 1) not in E1 and len(E1) == 3
assert set(E1) <= set(itertools.product(V1, V1))             # E is a subset of V x V
V2 = (1, 2, 3, 4, 5)                                         # "five vertices"
E2 = ((1, 2), (1, 3), (2, 3), (3, 4), (4, 5))                # "five edges"
assert len(V2) == 5 and len(E2) == 5 and len(set(map(frozenset, E2))) == 5
assert all(a != b for a, b in E2)                            # no self-loops

# Scene 3: degrees of G2, in and out degrees of G1.
DEG2 = {v: sum(1 for e in E2 if v in e) for v in V2}
NEIGH3 = sorted(u for e in E2 if 3 in e for u in e if u != 3)
IN1 = {v: sum(1 for e in E1 if e[1] == v) for v in V1}
OUT1 = {v: sum(1 for e in E1 if e[0] == v) for v in V1}
assert DEG2 == {1: 2, 2: 2, 3: 3, 4: 2, 5: 1}                # "degree three", "two", "one"
assert NEIGH3 == [1, 2, 4]                                   # "one, two and four"
assert OUT1 == {1: 3, 2: 0, 3: 0, 4: 0} and IN1 == {1: 0, 2: 1, 3: 1, 4: 1}
assert sum(1 for v in V1 if v != 1 and IN1[v] == 1 and OUT1[v] == 0) == 3   # "the other three"
EDGES_AT3 = [i for i, e in enumerate(E2) if 3 in e]          # the three edges at vertex three
assert len(EDGES_AT3) == 3

# Scene 4: G3, the neighbourhood. Edges chosen so that every walk of the notes (lines
# 128-131) is legal.
V3 = (1, 2, 3, 4)
E3 = ((1, 2), (1, 3), (1, 4), (2, 3), (3, 4))


def _adj(a, b):
    return any({a, b} == set(e) for e in E3)


def _eidx(a, b):
    return next(i for i, e in enumerate(E3) if {a, b} == set(e))


def steps(seq):
    """(edge index, walked backwards?) for a sequence of houses."""
    out = []
    for a, b in zip(seq, seq[1:]):
        i = _eidx(a, b)
        out.append((i, E3[i] != (a, b)))
    return tuple(out)


def simple_paths(a, b, seen=()):
    seen = seen + (a,)
    if a == b:
        yield seen
        return
    for v in V3:
        if v not in seen and _adj(a, v):
            yield from simple_paths(v, b, seen)


ALL_24 = list(simple_paths(2, 4))
SHORT = (2, 1, 4)
LONG = (2, 3, 1, 4)
assert min(len(p) - 1 for p in ALL_24) == 2 and SHORT in ALL_24   # "shortest path ... two edges"
assert max(len(p) - 1 for p in ALL_24) == 3 and LONG in ALL_24    # "three edges", nothing longer
assert not _adj(2, 4)                                        # "no single road joins two and four"
CYCLE_A = (1, 2, 3, 1)
CYCLE_B = (1, 3, 4, 1)
for cyc in (CYCLE_A, CYCLE_B):
    assert cyc[0] == cyc[-1] and len(set(cyc[:-1])) == len(cyc) - 1
    assert all(_adj(a, b) for a, b in zip(cyc, cyc[1:]))
STROLL = (2, 1, 2, 3, 4)                                     # the notes: {2,1},{1,2},{2,3},{3,4}
TOUR = (2, 1, 3, 4, 1, 2)                                    # the notes: {2,1},{1,3},{3,4},{4,1},{1,2}
for w in (STROLL, TOUR):
    assert all(_adj(a, b) for a, b in zip(w, w[1:]))
assert len(set(STROLL)) < len(STROLL) and STROLL[0] != STROLL[-1]   # a walk, not a closed one
assert TOUR[0] == TOUR[-1] == 2 and TOUR.count(1) == 2       # "visits house one twice"
assert len(E3) == 5

# Scene 5: G4, three components (my reconstruction; the notes give only the components).
V4 = (1, 2, 3, 4, 5, 6, 7)
E4 = ((1, 2), (2, 3), (1, 3), (5, 6), (6, 7), (5, 7))
COMPS = ((1, 2, 3), (4,), (5, 6, 7))


def _components(vs, es):
    comp = {v: v for v in vs}

    def find(x):
        while comp[x] != x:
            x = comp[x]
        return x
    for a, b in es:
        comp[find(a)] = find(b)
    groups = {}
    for v in vs:
        groups.setdefault(find(v), []).append(v)
    return sorted(tuple(g) for g in groups.values())


assert _components(V4, E4) == sorted(COMPS)                  # "three connected components"
assert _components(V3, E3) == [V3]                           # the neighbourhood is connected
DEG4 = {v: sum(1 for e in E4 if v in e) for v in V4}
assert DEG4 == {1: 2, 2: 2, 3: 2, 4: 0, 5: 2, 6: 2, 7: 2}    # every degree is even
assert all(d % 2 == 0 for d in DEG4.values())
# Theorem 10.1: tour iff even degrees and connected apart from isolated vertices
_nonempty = [c for c in _components(V4, E4) if any(DEG4[v] for v in c)]
assert len(_nonempty) == 2                                   # two triangles: not connected
HAS_TOUR = all(d % 2 == 0 for d in DEG4.values()) and len(_nonempty) == 1
assert HAS_TOUR is False                                     # "no Eulerian tour exists"

# ---- Geometry (inside x = +-6.8 and y = -2.9 .. 3.3) -----------------------------------
def P(x, y):
    return np.array([x, y, 0.0])


POS_K = {"A": P(-5.7, 0.5), "B": P(-3.7, 1.6), "C": P(-3.7, -0.8), "D": P(-1.7, 0.5)}
POS_1 = {1: P(-5.0, 0.9), 2: P(-2.4, 1.9), 3: P(-2.4, 0.9), 4: P(-2.4, -0.1)}
POS_2 = {1: P(1.5, 1.9), 2: P(1.5, 0.0), 3: P(3.4, 0.95), 4: P(5.1, 1.9), 5: P(6.0, 0.2)}
POS_6 = P(3.4, -1.3)
POS_3 = {2: P(-5.2, 0.2), 1: P(-2.9, 1.5), 3: P(-2.9, -1.1), 4: P(-0.6, 0.2)}
POS_4 = {1: P(-5.4, 0.3), 2: P(-3.8, 1.5), 3: P(-3.8, -0.9), 4: P(-0.2, 0.3),
         5: P(3.0, 0.3), 6: P(4.6, 1.5), 7: P(4.6, -0.9)}
EDGE_C, HI_C, OK_C, BAD_C = BLUE_B, YELLOW_D, GREEN_C, RED_C
WALK_C, TOUR_C = PURPLE_B, ORANGE


class Graph:
    """Nodes (circle + label), edges and the group of all of them."""

    def __init__(self, nodes, edges):
        self.nodes, self.edges = nodes, edges
        self.all = VGroup(*edges, *nodes.values())

    def circle(self, v):
        return self.nodes[v][0]

    def edge_group(self, idxs):
        return VGroup(*[self.edges[i] for i in idxs])

    def node_group(self, vs):
        return VGroup(*[self.nodes[v] for v in vs])


class Ep02GraphLanguage(NarratedScene):
    SCENES = ["vertices_edges", "directed_and_undirected", "neighbours_and_degree",
              "walks_and_paths", "connectivity"]

    def construct(self):
        if self.preview_only(self.SCENES):
            return
        self.title_card()
        for name in self.SCENES:
            getattr(self, name)()
        self.end_card(["A graph is a pair of a vertex set and an edge set, with ordered pairs as edges "
                       "when it is directed and two-member sets when it is undirected",
                       "The degree of a vertex counts its edges, and a directed graph splits that count "
                       "into an in-degree and an out-degree",
                       "A path repeats no vertex, a walk may repeat anything, and a cycle and a tour are "
                       "a path and a walk that return to the start",
                       "A graph is connected when any two vertices have a path between them, and "
                       "Euler's theorem needs both even degrees and connectivity"])

    # ---- drawing helpers -------------------------------------------------------------
    def _graph(self, pos, edges, r, size, directed=False, bends=None, color=BLUE_C):
        bends = bends or {}
        nodes = {}
        for v, p in pos.items():
            c = Circle(radius=r, stroke_color=color, stroke_width=3,
                       fill_color=BLUE_E, fill_opacity=0.35).move_to(p)
            nodes[v] = VGroup(c, txt(str(v), size, WHITE).next_to(c, ORIGIN))
        lines = []
        for i, e in enumerate(edges):
            a, b = e[0], e[1]
            p, q = pos[a], pos[b]
            d = (q - p) / np.linalg.norm(q - p)
            s, t = p + d * r, q - d * r
            if directed:
                lines.append(Arrow(s, t, buff=0, stroke_width=3, tip_length=0.22, color=EDGE_C,
                                   max_tip_length_to_length_ratio=0.4))
            elif i in bends:
                lines.append(ArcBetweenPoints(s, t, angle=bends[i], stroke_color=EDGE_C, stroke_width=3))
            else:
                lines.append(Line(s, t, stroke_color=EDGE_C, stroke_width=3))
        return Graph(nodes, lines)

    def _lands(self):
        """The four lands as a graph with letters, the bridges bent apart where doubled."""
        pos = POS_K
        nodes = {}
        for v, p in pos.items():
            c = Circle(radius=0.4, stroke_color=BLUE_C, stroke_width=3,
                       fill_color=BLUE_E, fill_opacity=0.35).move_to(p)
            nodes[v] = VGroup(c, txt(v, 26, WHITE).next_to(c, ORIGIN))
        lines = []
        for a, b, bend in K_DRAW:
            p, q = pos[a], pos[b]
            d = (q - p) / np.linalg.norm(q - p)
            s, t = p + d * 0.4, q - d * 0.4
            if bend is None:
                lines.append(Line(s, t, stroke_color=EDGE_C, stroke_width=3))
            else:
                lines.append(ArcBetweenPoints(s, t, angle=bend, stroke_color=EDGE_C, stroke_width=3))
        return Graph(nodes, lines)

    def _path(self, g, stps):
        """An invisible path along the edges `stps`, edge by edge."""
        pts = []
        for i, rev in stps:
            alphas = np.linspace(1, 0, 10) if rev else np.linspace(0, 1, 10)
            pts += [g.edges[i].point_from_proportion(float(t)) for t in alphas]
        p = VMobject(stroke_opacity=0, stroke_width=0)
        p.set_points_as_corners(pts)
        return p

    def _swap_head(self, text):
        new = self.heading(text)
        old = getattr(self, "_head", None)
        anims = [Write(new)] if old is None else [FadeOut(old, run_time=0.5), Write(new)]
        self._head = new
        return anims

    def _mark(self, g, v, value, direction, color=OK_C, size=28):
        return num(str(value), size, color).next_to(g.circle(v), direction, buff=0.14)

    def _fresh(self):
        """Clear the stage between scenes."""
        self.clear_stage()
        self._head = None

    # ---- scene 1: a graph is a pair of sets -------------------------------------------
    def vertices_edges(self):
        g = self._lands()
        v_txt = mono("V = {A,B,C,D}", 26, YELLOW_D)
        e1 = mono("E = {{A,B},{A,B},{A,C},{B,C},", 26, GREEN_B)
        e2 = mono("{B,D},{B,D},{C,D}}", 26, GREEN_B)
        e_multi = VGroup(e1, e2).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        e2.shift(RIGHT * 0.8)
        block = VGroup(v_txt, e_multi).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        block.next_to(g.all, RIGHT, buff=0.8)
        # the same E, as a plain set
        s1 = mono("E = {{A,B},{A,C},{B,C},", 26, GREEN_B)
        s2 = mono("{B,D},{C,D}}", 26, GREEN_B)
        e_set = VGroup(s1, s2).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        s2.shift(RIGHT * 0.8)
        e_set.move_to(e_multi, aligned_edge=UL)
        doubled = g.edge_group([0, 1, 4, 5])
        copies = g.edge_group(DUPES)

        # beat 1: the names
        self.say("Episode one ended with a picture of four lands joined by seven bridges, and now we give its "
                 "parts their proper names. So the four lands are the vertices, and together they form one "
                 "set, which we call V. And the seven bridges are the edges, and together they form a "
                 "second set, which we call E.",
                 *self._swap_head("A graph is a pair of sets"),
                 LaggedStart(*[FadeIn(g.nodes[v], scale=0.6) for v in LANDS], lag_ratio=0.15),
                 LaggedStart(*[Create(e) for e in g.edges], lag_ratio=0.12))
        self.cue("the four lands are the vertices", Indicate(g.node_group(LANDS), color=HI_C),
                 FadeIn(v_txt, shift=LEFT * 0.2))
        self.cue("the seven bridges are the edges", Indicate(VGroup(*g.edges), color=HI_C),
                 FadeIn(e_multi, shift=LEFT * 0.2))

        # beat 2: the multiset
        self.say("Look closely at E, because two of its pairs appear twice, since the city has two bridges "
                 "between the same two lands. So E here is a multiset, which means a set in which an element "
                 "may appear several times.",
                 Indicate(doubled, color=BAD_C))
        self.cue("a multiset", Indicate(e_multi, color=BAD_C))

        # beat 3: a plain set
        self.say("In this course we usually forbid that, so from now on E is a plain set, and the second copy "
                 "of each doubled pair disappears. Then between any two vertices there is either no edge or "
                 "exactly one edge.",
                 FadeOut(copies), Transform(e_multi, e_set))
        self.cue("exactly one edge", Indicate(VGroup(*[g.edges[i] for i in (0, 2, 3, 4, 6)]), color=HI_C))
        self.hold(0.5)

    # ---- scene 2: directed and undirected --------------------------------------------
    def directed_and_undirected(self):
        self._fresh()
        g1 = self._graph(POS_1, E1, 0.35, 24, directed=True)
        g2 = self._graph(POS_2, E2, 0.35, 24)
        t1 = VGroup(mono("V = {1,2,3,4}", 22, YELLOW_D), mono("E = {(1,2),(1,3),(1,4)}", 22, GREEN_B))
        t1.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(g1.all, DOWN, buff=0.45)
        not_in = mono("(2,1) is not in E", 24, BAD_C).next_to(t1, DOWN, buff=0.3)
        t2 = VGroup(mono("V = {1,2,3,4,5}", 22, YELLOW_D), mono("E = {{1,2},{1,3},{2,3},", 22, GREEN_B),
                    mono("{3,4},{4,5}}", 22, GREEN_B))
        t2.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(g2.all, DOWN, buff=0.45)
        t2[2].shift(RIGHT * 0.75)
        g_label = mono("G = (V, E)", 34, YELLOW_D).to_corner(UR, buff=0.5)

        # beat 1: a directed graph
        self.say("So far every bridge could be crossed in both directions, but some relationships go only "
                 "one way, like a one way street. So a directed graph models this with arrows, and its edges "
                 "are ordered pairs.\n"
                 "Here the vertex called one has an edge to two, to three and to four, so E holds exactly "
                 "three ordered pairs. That makes E a subset of V times V, the set of all ordered pairs of "
                 "vertices.",
                 *self._swap_head("Directed or undirected"),
                 LaggedStart(*[FadeIn(g1.nodes[v], scale=0.6) for v in V1], lag_ratio=0.12),
                 LaggedStart(*[GrowArrow(e) for e in g1.edges], lag_ratio=0.2))
        self.cue("three ordered pairs", FadeIn(t1, shift=UP * 0.2))
        self.cue("a subset of V times V", Indicate(t1[1], color=HI_C))

        # beat 2: order matters
        self.say("Order matters in a directed graph, so the ordered pair one, two is an edge, while the "
                 "ordered pair two, one is not. And you can follow the arrow from one to two, but nothing "
                 "lets you come back along it.",
                 Indicate(g1.edges[0], color=HI_C))
        self.cue("while the ordered pair two, one is not", FadeIn(not_in, shift=UP * 0.2))

        # beat 3: an undirected graph
        self.say("On the other hand, when every edge works in both directions, we call the graph undirected, "
                 "like a network of two way streets. And then we drop the arrowheads and write each edge as "
                 "a set with two members, instead of an ordered pair.",
                 LaggedStart(*[FadeIn(g2.nodes[v], scale=0.6) for v in V2], lag_ratio=0.12),
                 LaggedStart(*[Create(e) for e in g2.edges], lag_ratio=0.15))
        self.cue("drop the arrowheads", Indicate(VGroup(*g2.edges), color=HI_C))
        self.cue("a set with two members", FadeIn(t2, shift=UP * 0.2))

        # beat 4: G = (V, E)
        self.say("In both cases a graph is a pair, G is the ordered pair V, E, where V is the vertex set and "
                 "E is the edge set. So the undirected graph on the right has five vertices and five edges, "
                 "and it is the one we use next.",
                 FadeIn(g_label, shift=DOWN * 0.2))
        self.cue("five vertices", Indicate(g2.node_group(V2), color=HI_C))
        self.cue("five edges", Indicate(VGroup(*g2.edges), color=HI_C))
        self.hold(0.5)
        self.g1, self.g2, self.s2_old = g1, g2, VGroup(t1, not_in, t2, g_label)

    # ---- scene 3: neighbours and degree ----------------------------------------------
    def neighbours_and_degree(self):
        g1, g2 = self.g1, self.g2
        marks2 = {1: self._mark(g2, 1, DEG2[1], UP), 2: self._mark(g2, 2, DEG2[2], DOWN),
                  3: self._mark(g2, 3, DEG2[3], DR), 4: self._mark(g2, 4, DEG2[4], UP),
                  5: self._mark(g2, 5, DEG2[5], DOWN)}
        iso_c = Circle(radius=0.35, stroke_color=GREY_B, stroke_width=3,
                       fill_color=BLUE_E, fill_opacity=0.35).move_to(POS_6)
        iso = VGroup(iso_c, txt("6", 24, GREY_A).next_to(iso_c, ORIGIN))
        iso_mark = num("0", 28, OK_C).next_to(iso_c, RIGHT, buff=0.14)
        loop = Circle(radius=0.22, stroke_color=BAD_C, stroke_width=3).move_to(
            g2.circle(2).get_center() + LEFT * 0.49)
        inout = {1: mono(f"in {IN1[1]}, out {OUT1[1]}", 22, OK_C).next_to(g1.circle(1), DOWN, buff=0.2)}
        for v in (2, 3, 4):
            inout[v] = mono(f"in {IN1[v]}, out {OUT1[v]}", 22, OK_C).next_to(g1.circle(v), RIGHT, buff=0.2)

        # beat 1: incident and neighbours
        self.say("Take the undirected graph on the right and look at the vertex numbered three. So its three "
                 "edges are incident on it, and the vertices at their other ends are its neighbours, which "
                 "we also call adjacent.",
                 FadeOut(self.s2_old), *self._swap_head("Neighbours and degree"),
                 Indicate(g2.nodes[3], color=HI_C))
        self.cue("its three edges", Indicate(g2.edge_group(EDGES_AT3), color=HI_C))
        self.cue("its neighbours", Indicate(g2.node_group(NEIGH3), color=HI_C))

        # beat 2: the degrees
        self.say("The degree of a vertex is the number of edges incident on it, so the vertex three has "
                 "degree three. And counting the same way, the vertices one, two and four all have degree "
                 "two, while the vertex five has degree one.",
                 FadeIn(marks2[3], scale=1.4))
        self.cue("one, two and four all have degree two",
                 LaggedStart(*[FadeIn(marks2[v], scale=1.4) for v in (1, 2, 4)], lag_ratio=0.2))
        self.cue("the vertex five", FadeIn(marks2[5], scale=1.4))

        # beat 3: isolated vertex, self loops
        self.say("Now add a lonely sixth vertex with no edges at all, and its degree is zero. Such a vertex "
                 "is called isolated, because no edge connects it to the rest of the graph. And we agree "
                 "that no edge may start and end at the same vertex, so our graphs have no self loops.",
                 FadeIn(iso, scale=0.6), FadeIn(iso_mark))
        self.cue("called isolated", Indicate(iso, color=HI_C))
        self.cue("no self loops", FadeIn(loop))

        # beat 4: in-degree and out-degree
        self.say("A directed graph has two kinds of degree, because an arrow can come into a vertex or "
                 "leave it. And the in-degree of a vertex counts the edges arriving at it, while the "
                 "out-degree counts the edges leaving it.\n"
                 "So in the graph on the left, vertex one has out-degree three and in-degree zero. And each "
                 "of the other three vertices has in-degree one and out-degree zero, since every arrow ends "
                 "at one of them.",
                 FadeOut(loop), Indicate(VGroup(*g1.edges), color=HI_C))
        self.cue("So in the graph on the left", FadeIn(inout[1], shift=UP * 0.2),
                 Indicate(g1.nodes[1], color=HI_C))
        self.cue("each of the other three",
                 LaggedStart(*[FadeIn(inout[v], shift=LEFT * 0.2) for v in (2, 3, 4)], lag_ratio=0.25))
        self.hold(0.5)

    # ---- scene 4: paths, walks, cycles, tours ----------------------------------------
    def walks_and_paths(self):
        self._fresh()
        g = self._graph(POS_3, E3, 0.38, 26)
        dot_a = Dot(g.circle(2).get_center(), radius=0.13, color=YELLOW_D)
        dot_b = Dot(g.circle(2).get_center(), radius=0.13, color=GREEN_C)
        dot_c = Dot(g.circle(1).get_center(), radius=0.13, color=YELLOW_D)
        dot_d = Dot(g.circle(2).get_center(), radius=0.13, color=WALK_C)
        dot_e = Dot(g.circle(2).get_center(), radius=0.13, color=TOUR_C)

        def paint(idxs, color):
            return [g.edges[i].animate.set_color(color) for i in idxs]

        def idx_of(seq):
            return [i for i, _ in steps(seq)]

        reset = [e.animate.set_color(EDGE_C) for e in g.edges]

        # beat 1: the neighbourhood
        self.say("Let us explore a small neighbourhood, where each vertex is a house and each edge is a "
                 "direct road. So the roads join houses one and two, one and three, one and four, two and "
                 "three, and three and four.",
                 *self._swap_head("Walks, paths and cycles"),
                 LaggedStart(*[FadeIn(g.nodes[v], scale=0.6) for v in V3], lag_ratio=0.12))
        self.cue("the roads join houses", LaggedStart(*[Create(e) for e in g.edges], lag_ratio=0.2))

        # beat 2: paths
        self.say("Suppose we want to drive from house two to house four, which is a job for a path. A path "
                 "is a sequence of edges from the first house to the last, and here it never visits a house "
                 "twice.\n"
                 "So two, one, four is a shortest path, with two edges, because no single road joins houses "
                 "two and four. And the longest path that repeats no house is two, three, one, four, which "
                 "has three edges.",
                 FadeIn(dot_a))
        self.cue("So two, one, four",
                 MoveAlongPath(dot_a, self._path(g, steps(SHORT)), run_time=2.4),
                 *paint(idx_of(SHORT), HI_C))
        self.cue("the longest path", FadeOut(dot_a), FadeIn(dot_b), *reset)
        self.cue("two, three, one, four, which",
                 MoveAlongPath(dot_b, self._path(g, steps(LONG)), run_time=3.0),
                 *paint(idx_of(LONG), OK_C))

        # beat 3: cycles
        self.say("A cycle is a path that returns to where it began, so we add one edge from the last house "
                 "back to the first. For example, one, two, three and back to one is a cycle, and so is one, "
                 "three, four and back to one.",
                 FadeOut(dot_b), FadeIn(dot_c), *reset)
        self.cue("one, two, three and back to one",
                 MoveAlongPath(dot_c, self._path(g, steps(CYCLE_A)), run_time=3.0),
                 *paint(idx_of(CYCLE_A), HI_C))
        self.cue("so is one, three, four",
                 *[g.edges[i].animate.set_color(EDGE_C) for i in idx_of(CYCLE_A)],
                 MoveAlongPath(dot_c, self._path(g, steps(CYCLE_B)), run_time=3.0),
                 *paint(idx_of(CYCLE_B), HI_C))

        # beat 4: walks and tours
        self.say("Now suppose we only want a leisurely stroll, going from two to one, back to two, then to "
                 "three and on to four. That sequence of edges is a walk, and it may repeat houses and even "
                 "edges, which a path never does.\n"
                 "And a tour is a walk that ends where it started, so two, one, three, four, one, two is a "
                 "tour.",
                 FadeOut(dot_c), FadeIn(dot_d), *reset)
        self.cue("going from two to one",
                 MoveAlongPath(dot_d, self._path(g, steps((2, 1))), run_time=1.4),
                 *paint(idx_of((2, 1)), WALK_C))
        self.cue("back to two", MoveAlongPath(dot_d, self._path(g, steps((1, 2))), run_time=1.4))
        self.cue("then to three and on to four",
                 MoveAlongPath(dot_d, self._path(g, steps((2, 3, 4))), run_time=2.4),
                 *paint(idx_of((2, 3, 4)), WALK_C))
        self.cue("a tour is a walk that ends where it started",
                 FadeOut(dot_d), FadeIn(dot_e), *reset)
        self.cue("two, one, three, four, one, two",
                 MoveAlongPath(dot_e, self._path(g, steps(TOUR)), run_time=4.0),
                 *paint(idx_of(TOUR), TOUR_C))

        # beat 5: the four words side by side
        labels = VGroup(*[txt(w, 26, WHITE) for w in ("Walk", "Path", "Tour", "Cycle")])
        labels.arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        labels.move_to(P(1.7, 0.4))
        cx1 = labels.get_right()[0] + 1.5
        cx2 = cx1 + 2.3
        top_y = labels.get_top()[1] + 0.75
        head1 = txt("no repeats", 22, GREY_A).move_to(P(cx1, top_y))
        head2 = txt("closed", 22, GREY_A).move_to(P(cx2, top_y))

        def dot_at(col_x, row):
            return Dot(P(col_x, labels[row].get_center()[1]), radius=0.13, color=OK_C)

        d_path, d_tour = dot_at(cx1, 1), dot_at(cx2, 2)
        d_cyc = VGroup(dot_at(cx1, 3), dot_at(cx2, 3))
        dash = Line(P(cx1 - 0.2, labels[0].get_center()[1]), P(cx2 + 0.2, labels[0].get_center()[1]),
                    stroke_color=GREY_B, stroke_width=3)
        self.say("To keep the four words apart, remember that a path has no repeated vertices and a tour is "
                 "closed. A cycle is both, apart from the start and end that coincide, and a walk has no "
                 "rule at all.",
                 *reset, FadeOut(dot_e), FadeIn(labels), FadeIn(head1), FadeIn(head2))
        self.cue("a path has no repeated vertices", FadeIn(d_path, scale=1.5))
        self.cue("a tour is closed", FadeIn(d_tour, scale=1.5))
        self.cue("A cycle is both", FadeIn(d_cyc, scale=1.5))
        self.cue("a walk has no rule at all", Create(dash))
        self.hold(0.5)
        self.g3 = g
        self.table = VGroup(labels, head1, head2, d_path, d_tour, d_cyc, dash)

    # ---- scene 5: connectivity and the theorem ---------------------------------------
    def connectivity(self):
        g3 = self.g3
        g4 = self._graph(POS_4, E4, 0.38, 26)
        rects = [SurroundingRectangle(g4.node_group(c), color=col, buff=0.3, stroke_width=3)
                 for c, col in zip(COMPS, (BLUE_C, GREY_B, TEAL_C))]
        vlabels = [mono(f"V{i + 1}", 26, rects[i].get_color()).next_to(rects[i], DOWN, buff=0.15)
                   for i in range(3)]
        marks4 = {v: self._mark(g4, v, DEG4[v], d, size=26) for v, d in
                  {1: LEFT, 2: UP, 3: DOWN, 4: UP, 5: LEFT, 6: UP, 7: DOWN}.items()}
        dot = Dot(g4.circle(1).get_center(), radius=0.13, color=YELLOW_D)

        # beat 1: connected
        self.say("Now we can define connectivity, and a graph is connected if there is a path between any "
                 "two distinct vertices. So our neighbourhood is connected, since from any house we can "
                 "drive to any other house along some sequence of roads.",
                 *self._swap_head("Connectivity"), FadeOut(self.table))
        self.cue("any two distinct vertices", Indicate(g3.node_group((2, 4)), color=HI_C))
        self.cue("our neighbourhood is connected", Indicate(g3.all, color=OK_C))

        # beat 2: components
        self.say("Now look at a network of seven houses, where no road joins the left triangle to the "
                 "lonely house or to the right triangle. So the network is not connected, and it falls "
                 "apart into exactly three connected components. Those components are the sets V one, V "
                 "two and V three, holding houses one, two, three, then four alone, then five, six, seven.",
                 FadeOut(g3.all),
                 LaggedStart(*[FadeIn(g4.nodes[v], scale=0.6) for v in V4], lag_ratio=0.1),
                 LaggedStart(*[Create(e) for e in g4.edges], lag_ratio=0.1))
        self.cue("the lonely house", Indicate(g4.nodes[4], color=HI_C))
        self.cue("three connected components", LaggedStart(*[Create(r) for r in rects], lag_ratio=0.3))
        self.cue("the sets V one", LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in vlabels], lag_ratio=0.5))

        # beat 3: Eulerian words and the theorem
        self.say("With these words we can state Euler's theorem exactly, since an Eulerian walk is a walk "
                 "that uses every edge once. And an Eulerian tour is one of these walks that ends where it "
                 "started. The theorem says that an undirected graph has an Eulerian tour exactly when "
                 "every degree is even and the graph is connected, ignoring isolated vertices.",
                 FadeOut(*rects), FadeOut(*vlabels), Indicate(VGroup(*g4.edges), color=HI_C))
        self.cue("every degree is even",
                 LaggedStart(*[FadeIn(marks4[v], scale=1.4) for v in V4], lag_ratio=0.1))
        self.cue("ignoring isolated vertices", Indicate(g4.nodes[4], color=HI_C))

        # beat 4: even degrees and still no tour
        self.say("In this network every degree is even, and yet no Eulerian tour exists. So a tour that "
                 "starts in the left triangle can never reach the right triangle, since no road joins "
                 "them. That is why Euler's theorem needs both conditions, the even degrees and the "
                 "connectedness.",
                 Indicate(VGroup(*marks4.values()), color=OK_C), FadeIn(dot))
        self.cue("starts in the left triangle",
                 MoveAlongPath(dot, self._path(g4, ((0, 0), (1, 0), (2, 1))), run_time=3.0),
                 *[g4.edges[i].animate.set_color(HI_C) for i in (0, 1, 2)])
        self.cue("the right triangle", Indicate(g4.edge_group((3, 4, 5)), color=BAD_C))
        self.cue("needs both conditions", Indicate(g4.all, color=HI_C))
        self.hold(0.5)
