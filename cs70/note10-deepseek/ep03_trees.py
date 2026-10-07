"""Episode 3 of the CS70 Note 10 series: complete graphs and trees, Theorem 10.2.

FACTS come from cs70/note10-deepseek/notes.txt, lines 189-306. The figures of the notes did
not survive the text extraction, so every graph below is rebuilt from the text. The picture
reads the names below; the narration says numbers as words, and every spoken number has an
assert here.
"""
import os
import sys
from itertools import combinations

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---- FACTS: complete graphs (notes lines 197-216) ----------------------------------------
SIZES = (2, 3, 4, 5)                                          # K two .. K five
KN_EDGES = {n: tuple(combinations(range(n), 2)) for n in SIZES}   # every pair, once
EDGE_COUNT = {n: len(KN_EDGES[n]) for n in SIZES}
assert EDGE_COUNT == {2: 1, 3: 3, 4: 6, 5: 10}               # "one", "three", "six", "ten"
assert all(EDGE_COUNT[n] == n * (n - 1) // 2 for n in SIZES)  # the formula of the notes
KN_DEG = {n: [sum(1 for e in KN_EDGES[n] if v in e) for v in range(n)] for n in SIZES}
assert all(set(KN_DEG[n]) == {n - 1} for n in SIZES)         # every degree is n minus one
assert KN_DEG[5][0] == 4                                     # "four"
assert 5 * (5 - 1) // 2 == 10 and sum(KN_DEG[5]) == 2 * EDGE_COUNT[5] == 20   # "twice"

# ---- FACTS: a tree on six vertices (lines 220-236) ----------------------------------------
# Relative drawing positions; the scenes shift them. Vertex numbers are the labels.
TREE_REL = {1: (0.0, 1.35), 2: (-1.3, 0.0), 3: (1.3, 0.0),
            4: (-2.1, -1.35), 5: (-0.5, -1.35), 6: (1.3, -1.35)}
TREE_EDGES = ((1, 2), (1, 3), (2, 4), (2, 5), (3, 6))
N_TREE = len(TREE_REL)                                       # "six"
M_TREE = len(TREE_EDGES)                                     # "five"
assert (N_TREE, M_TREE) == (6, 5) and M_TREE == N_TREE - 1


def _components(vertices, edges):
    comp = {v: v for v in vertices}

    def find(v):
        while comp[v] != v:
            v = comp[v]
        return v
    for a, b in edges:
        comp[find(a)] = find(b)
    groups = {}
    for v in vertices:
        groups.setdefault(find(v), set()).add(v)
    return list(groups.values())


assert len(_components(TREE_REL, TREE_EDGES)) == 1           # connected
CUT = (1, 2)                                                 # the edge we cut
_cut_parts = _components(TREE_REL, [e for e in TREE_EDGES if e != CUT])
assert sorted(map(sorted, _cut_parts)) == [[1, 3, 6], [2, 4, 5]]      # "two pieces"
for _e in TREE_EDGES:                                        # every single edge disconnects
    assert len(_components(TREE_REL, [x for x in TREE_EDGES if x != _e])) == 2
ADD = (4, 5)                                                 # the edge we add: "four and five"
assert ADD not in TREE_EDGES and len(_components(TREE_REL, TREE_EDGES + (ADD,))) == 1
ADD_CYCLE = ((2, 4), (2, 5), ADD)                            # the triangle through vertex two
assert set(ADD_CYCLE[:2]) <= set(TREE_EDGES)
# adding any pair that is not an edge closes a cycle: the two ends are already connected
for _a, _b in combinations(TREE_REL, 2):
    if (_a, _b) not in TREE_EDGES:
        assert len(_components(TREE_REL, TREE_EDGES)) == 1
N_TREES_SIX = N_TREE ** (N_TREE - 2)                         # n to the power n minus two
assert (N_TREE - 2, N_TREES_SIX) == (4, 1296)                # "fourth power", "one thousand two hundred ninety six"

# a graph that is connected but has a cycle: a square with two hanging vertices
CYC_REL = {"a": (-0.9, 0.9), "b": (0.9, 0.9), "c": (0.9, -0.9), "d": (-0.9, -0.9),
           "e": (1.9, 1.7), "f": (1.9, -1.7)}
CYC_EDGES = (("a", "b"), ("b", "c"), ("c", "d"), ("d", "a"), ("b", "e"), ("c", "f"))
assert len(_components(CYC_REL, CYC_EDGES)) == 1 and len(CYC_EDGES) == 6 > len(CYC_REL) - 1
SQUARE = 4                                                   # "four of its vertices form a cycle"
assert SQUARE == 4

# ---- FACTS: a rooted tree of fifteen nodes (lines 240-268) --------------------------------
# The figure is lost; this is the complete binary tree on 15 nodes, numbered 1 to 15 from the
# top, which has the depth three that the notes' concept check answers.
N_ROOTED = 15
PARENT = {i: i // 2 for i in range(2, N_ROOTED + 1)}
LEVEL = {i: i.bit_length() - 1 for i in range(1, N_ROOTED + 1)}
DEPTH = max(LEVEL.values())
LEVEL_SIZES = [sum(1 for v in LEVEL.values() if v == k) for k in range(DEPTH + 1)]
CHILDREN = {i: [c for c, p in PARENT.items() if p == i] for i in range(1, N_ROOTED + 1)}
LEAVES = [i for i in range(1, N_ROOTED + 1) if not CHILDREN[i]]
INTERNAL = [i for i in range(2, N_ROOTED + 1) if CHILDREN[i]]
ROOT_DEG = len(CHILDREN[1])
LEAF_DEG = {len(CHILDREN[i]) + (1 if i != 1 else 0) for i in LEAVES}   # one parent, no children
assert DEPTH == 3 and LEVEL_SIZES == [1, 2, 4, 8]            # "three", "one, two, four and eight"
assert LEAVES == list(range(8, 16)) and INTERNAL == list(range(2, 8))
assert ROOT_DEG == 2 and LEAF_DEG == {1}                     # "degree two", "degree one"
assert 1 not in LEAVES                                       # the root is never a leaf
assert all(LEVEL[i] == DEPTH for i in LEAVES)                # every longest path has three edges
PATH = (1, 2, 4, 8)                                          # the path that is lit up
assert all(PARENT[PATH[k + 1]] == PATH[k] for k in range(3)) and len(PATH) - 1 == DEPTH

# ---- FACTS: the proof of Theorem 10.2 (lines 282-306) -----------------------------------
K_STEP = N_TREE - 1                                          # G has k plus one vertices; k = 5
GP_EDGES = [e for e in TREE_EDGES if 6 not in e]             # remove vertex v = 6
V_REM = 6
assert K_STEP == 5 and len(GP_EDGES) == K_STEP - 1 == 4      # "k minus one edges" for k = 5
assert len(_components([v for v in TREE_REL if v != V_REM], GP_EDGES)) == 1   # G prime connected
V_BACK = (3, 6)                                              # the one edge of v
V_SECOND = (5, 6)                                            # a second edge would close a cycle
V_CYCLE = ((3, 6), (1, 3), (1, 2), (2, 5), (5, 6))           # 6-3-1-2-5-6
assert len(GP_EDGES) + 1 == M_TREE == 5
assert all(tuple(sorted(e)) in [tuple(sorted(x)) for x in TREE_EDGES + (V_SECOND,)] for e in V_CYCLE)

# the graph of the converse: a triangle with a tail, to show that a cycle edge can go
CV_REL = {"p": (-1.2, 0.5), "q": (0.0, 1.0), "r": (0.0, -0.1), "s": (1.4, -0.1), "t": (2.7, -0.1)}
CV_EDGES = (("p", "q"), ("q", "r"), ("r", "p"), ("r", "s"), ("s", "t"))
CV_CUT = ("q", "r")
assert len(_components(CV_REL, CV_EDGES)) == 1
assert len(_components(CV_REL, [e for e in CV_EDGES if e != CV_CUT])) == 1   # still connected

EDGE_C, CUT_C, OK_C, BAD_C = BLUE_B, RED_C, GREEN_C, RED_C
NODE_R = 0.33


class Ep03Trees(NarratedScene):
    SCENES = ["complete_graphs", "what_is_a_tree", "rooted_trees", "forward_proof", "converse_proof"]

    def construct(self):
        if self.preview_only(self.SCENES):
            return
        self.title_card()
        for name in self.SCENES:
            getattr(self, name)()
        self.end_card(["A complete graph on n vertices joins every pair, and so it has n times n minus one over two edges",
                       "A tree is a connected graph with no cycles, and it has exactly n minus one edges",
                       "Cutting any edge of a tree disconnects it, and adding any edge to a tree makes a cycle",
                       "Theorem ten point two shows that connected with no cycles and connected with n minus one edges "
                       "are the same thing"])

    # ---- helpers ---------------------------------------------------------------------
    def _swap_head(self, text):
        new = self.heading(text)
        old = getattr(self, "_head", None)
        anims = [Write(new)] if old is None else [FadeOut(old, run_time=0.5), Write(new)]
        self._head = new
        return anims

    def _node(self, pos, label, r=NODE_R, size=24, color=BLUE_C, fill=BLUE_E):
        c = Circle(radius=r, stroke_color=color, stroke_width=3, fill_color=fill,
                   fill_opacity=0.35).move_to(pos)
        if label is None:
            return VGroup(c)
        return VGroup(c, txt(str(label), size, WHITE).next_to(c, ORIGIN))

    def _edge(self, a, b, r=NODE_R, color=EDGE_C):
        pa, pb = a[0].get_center(), b[0].get_center()
        return Line(pa, pb, buff=r, stroke_color=color, stroke_width=3)

    def _graph(self, rel, edges, offset, r=NODE_R, labels=True, size=24):
        """nodes dict, edges dict (keyed by the pair) and one VGroup, edges below nodes."""
        off = np.array([offset[0], offset[1], 0.0])
        nodes = {v: self._node(np.array([p[0], p[1], 0.0]) + off, v if labels else None, r, size)
                 for v, p in rel.items()}
        lines = {e: self._edge(nodes[e[0]], nodes[e[1]], r) for e in edges}
        group = VGroup(*lines.values(), *nodes.values())
        return nodes, lines, group

    def _paint(self, node, color, fill):
        return node[0].animate.set_stroke(color).set_fill(fill, 0.35)

    # ---- scene 1: complete graphs ----------------------------------------------------
    def complete_graphs(self):
        centers = {2: -4.8, 3: -1.6, 4: 1.6, 5: 4.8}
        start = {2: 0.0, 3: PI / 2, 4: PI / 4, 5: PI / 2}
        rad = {2: 0.8, 3: 0.9, 4: 0.9, 5: 0.95}
        dr = 0.13
        graphs, nodes_of, edges_of = {}, {}, {}
        for n in SIZES:
            pts = [np.array([centers[n] + rad[n] * np.cos(start[n] + 2 * PI * i / n),
                             0.9 + rad[n] * np.sin(start[n] + 2 * PI * i / n), 0.0]) for i in range(n)]
            nds = [Circle(radius=dr, stroke_color=BLUE_C, stroke_width=3, fill_color=BLUE_C,
                          fill_opacity=0.8).move_to(p) for p in pts]
            eds = {e: Line(pts[e[0]], pts[e[1]], buff=dr, stroke_color=EDGE_C, stroke_width=3)
                   for e in KN_EDGES[n]}
            graphs[n] = VGroup(*eds.values(), *nds)
            nodes_of[n], edges_of[n] = nds, eds
        assert [len(edges_of[n]) for n in SIZES] == [1, 3, 6, 10]
        names = {n: txt(f"K{n}", 28, YELLOW_D).next_to(graphs[5], DOWN, buff=0.3).set_x(centers[n])
                 for n in SIZES}
        counts = {n: mono(f"{EDGE_COUNT[n]} edge" + ("" if EDGE_COUNT[n] == 1 else "s"), 26, GREEN_B)
                  .next_to(names[n], DOWN, buff=0.2) for n in SIZES}
        all_counts = VGroup(*counts.values())
        v0 = nodes_of[5][0]
        spokes = VGroup(*[edges_of[5][e] for e in KN_EDGES[5] if 0 in e])
        deg_label = mono("degree 4", 26, YELLOW_D).next_to(v0, UP, buff=0.25)
        formula = mono("n (n - 1) / 2", 34, YELLOW_D).next_to(all_counts, DOWN, buff=0.45)
        check = mono("K5:  5 x 4 / 2 = 10", 30, GREEN_B).next_to(formula, DOWN, buff=0.3)

        # beat 1: the three small complete graphs
        self.say("Let us start with the graphs that have as many edges as they possibly can. "
                 "In a complete graph every pair of distinct vertices is joined by an edge, so nothing can be added. "
                 "So here are the complete graphs on two, three and four vertices.",
                 *self._swap_head("Complete graphs"), FadeIn(graphs[2]), FadeIn(names[2]))
        self.cue("complete graphs on two", FadeIn(graphs[3]), FadeIn(names[3]))
        self.cue("three and four vertices", FadeIn(graphs[4]), FadeIn(names[4]))

        # beat 2: K5, the counts, the degree
        self.say("Counting the edges gives one, three and six, and the complete graph on five vertices has ten. "
                 "It is the only complete graph on five vertices, so we call it K five. "
                 "Each of its vertices touches the four others, so its degree is four. "
                 "With n vertices that becomes n minus one.",
                 LaggedStart(*[FadeIn(counts[n]) for n in (2, 3, 4)], lag_ratio=0.3))
        self.cue("has ten", FadeIn(graphs[5]), FadeIn(names[5]), FadeIn(counts[5]))
        self.cue("Each of its vertices touches",
                 spokes.animate.set_color(YELLOW_D), Indicate(v0, color=YELLOW_D))
        self.cue("so its degree is four", FadeIn(deg_label, shift=UP * 0.2))

        # beat 3: the formula
        self.say("Adding up all the degrees gives n times n minus one, and this counts every edge twice "
                 "because an edge has two ends. "
                 "So the number of edges is n times n minus one over two. "
                 "For K five that is five times four over two, which is ten.",
                 FadeIn(formula, shift=UP * 0.2))
        self.cue("So the number of edges", Indicate(formula, color=YELLOW_D))
        self.cue("For K five that is", FadeIn(check, shift=UP * 0.2), Indicate(counts[5], color=YELLOW_D))
        self.hold(0.5)

    # ---- scene 2: what a tree is -----------------------------------------------------
    def what_is_a_tree(self):
        self.clear_stage()
        nodes, edges, tree = self._graph(TREE_REL, TREE_EDGES, (-3.6, 0.5))
        cn, ce, cyc = self._graph(CYC_REL, CYC_EDGES, (3.6, 0.4), r=0.2, labels=False)
        cyc_label = txt("has a cycle", 26, BAD_C).next_to(cyc, DOWN, buff=0.3)
        counts = VGroup(mono(f"{N_TREE} vertices", 26, GREEN_B), mono(f"{M_TREE} edges", 26, GREEN_B))
        counts.arrange(RIGHT, buff=0.6).next_to(tree, DOWN, buff=0.35)
        defs = VGroup(*[box_label(t, BLUE_C, w=4.6, h=0.7, font_size=26) for t in
                        ("connected, no cycles", "connected, n-1 edges", "any cut disconnects",
                         "new edge makes cycle")])
        defs.arrange(DOWN, buff=0.25).next_to(tree, RIGHT, buff=1.0)
        d1, d2, d3, d4 = defs
        many = VGroup(mono(f"6^4 = {N_TREES_SIX}", 30, YELLOW_D), txt("trees on 6 vertices", 26, GREY_A))
        many.arrange(DOWN, buff=0.2).next_to(tree, DOWN, buff=0.35)
        cut_line = edges[CUT]
        add_line = self._edge(nodes[ADD[0]], nodes[ADD[1]], color=BAD_C)

        # beat 1: a tree and a graph that is not
        self.say("A tree is a connected graph that contains no cycles, and here is one with six vertices. "
                 "Next to it stands a graph that is connected too, but four of its vertices form a cycle. "
                 "So the first graph is a tree and the second one is not.",
                 *self._swap_head("Trees"),
                 LaggedStart(*[Create(e) for e in edges.values()], lag_ratio=0.15),
                 LaggedStart(*[FadeIn(n, scale=0.7) for n in nodes.values()], lag_ratio=0.1))
        self.cue("Next to it", FadeIn(cyc))
        self.cue("form a cycle", *[ce[e].animate.set_color(BAD_C) for e in CYC_EDGES[:SQUARE]],
                 FadeIn(cyc_label))
        self.cue("the second one is not", Indicate(tree, color=OK_C))

        # beat 2: n vertices, n - 1 edges
        self.say("Now count the tree. It has six vertices and five edges, always one edge fewer than vertices. "
                 "So a tree is also a connected graph with n minus one edges, and that is the second way to say it.",
                 FadeOut(cyc), FadeOut(cyc_label), FadeIn(counts[0]))
        self.cue("five edges", FadeIn(counts[1]), Indicate(VGroup(*edges.values()), color=YELLOW_D))
        self.cue("a tree is also", FadeIn(d1), FadeIn(d2))

        # beat 3: cut an edge, add an edge
        parts = {v: (OK_C if v in _cut_parts[0] else YELLOW_D) for v in TREE_REL}
        self.say("Now cut any single edge of the tree, and it falls into two separate pieces. "
                 "So nothing can be removed without losing the connection. "
                 "In the same way, adding one new edge between vertices four and five closes a triangle, which is a cycle.",
                 cut_line.animate.set_stroke(CUT_C, opacity=0.35))
        self.cue("two separate pieces",
                 *[self._paint(nodes[v], parts[v], parts[v]) for v in TREE_REL])
        self.cue("nothing can be removed", FadeIn(d3))
        self.cue("adding one new edge",
                 cut_line.animate.set_stroke(EDGE_C, opacity=1),
                 *[self._paint(nodes[v], BLUE_C, BLUE_E) for v in TREE_REL],
                 Create(add_line))
        self.cue("closes a triangle", *[edges[e].animate.set_color(BAD_C) for e in ADD_CYCLE[:2]],
                 FadeIn(d4))

        # beat 4: many trees, one complete graph
        self.say("A complete graph is unique for each number of vertices, but trees are not. "
                 "A formula counts them, and there are n to the power n minus two trees on n vertices. "
                 "For six vertices that is six to the fourth power, which is one thousand two hundred ninety six different trees.",
                 FadeOut(add_line), FadeOut(counts),
                 *[edges[e].animate.set_color(EDGE_C) for e in ADD_CYCLE[:2]])
        self.cue("six to the fourth power", FadeIn(many, shift=UP * 0.2))
        self.hold(0.5)

    # ---- scene 3: rooted trees -------------------------------------------------------
    def rooted_trees(self):
        self.clear_stage()
        step = 1.3
        pos = {}
        for i in range(1, N_ROOTED + 1):
            k = LEVEL[i]
            idx = i - 2 ** k
            width = step * 2 ** (DEPTH - k)
            pos[i] = np.array([(idx + 0.5) * width - 4 * step, 2.1 - 1.15 * k, 0.0])
        nodes = {i: self._node(pos[i], i, size=22) for i in pos}
        edges = {(PARENT[i], i): self._edge(nodes[PARENT[i]], nodes[i]) for i in range(2, N_ROOTED + 1)}
        lvl = lambda ks: [i for i in range(1, N_ROOTED + 1) if LEVEL[i] in ks]
        root_l = txt("root", 26, GOLD_C).next_to(nodes[1], LEFT, buff=0.3)
        leaf_l = txt("leaves", 26, GREEN_B).next_to(nodes[8], DOWN, buff=0.3)
        int_l = txt("internal nodes", 26, BLUE_B).next_to(nodes[2], LEFT, buff=0.3)
        deg_l = mono("degree 2", 24, GOLD_C).next_to(nodes[1], RIGHT, buff=0.3)
        level_l = {k: txt(f"level {k}", 24, YELLOW_D).next_to(nodes[2 ** (k + 1) - 1], RIGHT, buff=0.3)
                   for k in range(DEPTH + 1)}
        size_l = {k: mono(f"{LEVEL_SIZES[k]} node" + ("" if LEVEL_SIZES[k] == 1 else "s"), 24, GREEN_B)
                  .next_to(nodes[2 ** k], LEFT, buff=0.3) for k in range(DEPTH + 1)}
        path_edges = [edges[(PATH[k], PATH[k + 1])] for k in range(DEPTH)]

        # beat 1: root, leaves, internal nodes
        self.say("A rooted tree has one special vertex called the root, which we draw at the top. "
                 "Below it the tree spreads out, and the vertices at the very bottom are the leaves. "
                 "The ones in between are the internal nodes.",
                 *self._swap_head("Rooted trees"), FadeIn(nodes[1]), FadeIn(root_l),
                 self._paint(nodes[1], GOLD_C, GOLD_C))
        self.cue("Below it the tree spreads out",
                 LaggedStart(*[AnimationGroup(Create(edges[(PARENT[i], i)]), FadeIn(nodes[i]))
                               for i in lvl({1, 2})], lag_ratio=0.2))
        self.cue("at the very bottom are the leaves",
                 LaggedStart(*[AnimationGroup(Create(edges[(PARENT[i], i)]), FadeIn(nodes[i]),
                                              self._paint(nodes[i], GREEN_C, GREEN_C)) for i in LEAVES],
                             lag_ratio=0.1), FadeIn(leaf_l))
        self.cue("internal nodes",
                 *[self._paint(nodes[i], BLUE_B, BLUE_C) for i in INTERNAL], FadeIn(int_l))

        # beat 2: the root is not a leaf, depth and levels
        self.say("In a rooted tree the root is never a leaf, whereas in an unrooted tree a leaf is any vertex of degree one. "
                 "The depth is the length of the longest path from the root to a leaf, which here is three edges. "
                 "Level k holds the vertices that are exactly k edges from the root.",
                 FadeOut(int_l), FadeOut(leaf_l), Indicate(nodes[1], color=GOLD_C), FadeIn(deg_l))
        self.cue("of degree one", Indicate(VGroup(*[nodes[i] for i in LEAVES]), color=GREEN_B))
        self.cue("longest path from the root",
                 LaggedStart(*[e.animate.set_color(YELLOW_D) for e in path_edges], lag_ratio=0.5),
                 FadeOut(deg_l))
        self.cue("Level k holds", LaggedStart(*[FadeIn(level_l[k]) for k in range(DEPTH + 1)], lag_ratio=0.3))

        # beat 3: the sizes and where trees are used
        self.say("The levels hold one, two, four and eight vertices, because every vertex has two below it. "
                 "That is exactly how a bacterium divides into two new bacteria, layer after layer. "
                 "Binary search trees use the same shape for fast searching, and hard problems like Maximum Cut become easy on trees.",
                 *[e.animate.set_color(EDGE_C) for e in path_edges], FadeOut(root_l),
                 *[FadeIn(size_l[k]) for k in range(1)])
        self.cue("two, four and eight", LaggedStart(*[FadeIn(size_l[k]) for k in range(1, DEPTH + 1)], lag_ratio=0.3))
        self.cue("a bacterium divides", Indicate(VGroup(nodes[1], nodes[2], nodes[3]), color=GREEN_B))
        self.cue("Binary search trees", Indicate(VGroup(*nodes.values()), color=YELLOW_D))
        self.hold(0.5)

    # ---- scene 4: Theorem 10.2, the forward direction ----------------------------------
    def forward_proof(self):
        self.clear_stage()
        box_a = box_label("connected, no cycles", BLUE_C, w=4.6, h=0.7, font_size=26)
        box_b = box_label("connected, n-1 edges", GREEN_C, w=4.6, h=0.7, font_size=26)
        pair = VGroup(box_a, box_b).arrange(RIGHT, buff=1.6).set_y(1.9)
        arrow = DoubleArrow(box_a.get_right(), box_b.get_left(), buff=0.1, color=YELLOW_D, stroke_width=4)
        fwd = Arrow(box_a.get_right(), box_b.get_left(), buff=0.1, color=YELLOW_D, stroke_width=6)
        base = self._node(np.array([-3.0, -0.4, 0.0]), 1)
        base_l = mono("1 vertex, 0 edges", 26, GREEN_B).next_to(base, RIGHT, buff=0.5)
        nodes, edges, tree = self._graph(TREE_REL, TREE_EDGES, (-3.0, -0.45))
        g_l = txt("G", 32, YELLOW_D).next_to(tree, RIGHT, buff=0.5)
        gp_l = txt("G'", 32, YELLOW_D).next_to(tree, RIGHT, buff=0.5)
        v_edge = edges[V_BACK]
        second = Line(nodes[V_SECOND[0]][0].get_center(), nodes[V_SECOND[1]][0].get_center(),
                      buff=NODE_R, stroke_color=BAD_C, stroke_width=3)
        k_edges = mono("4 edges = k - 1", 28, GREEN_B).next_to(gp_l, RIGHT, buff=0.9)
        g_edges = mono("4 + 1 = 5 edges", 28, YELLOW_D).next_to(k_edges, DOWN, buff=0.35)
        cycle_edges = [edges.get(tuple(e)) or second for e in V_CYCLE]

        # beat 1: the theorem
        self.say("Now we can prove that the first two definitions of a tree really are equivalent, which is Theorem ten point two. "
                 "It says that a graph is connected with no cycles exactly when it is connected with n minus one edges. "
                 "So there are two directions to check, and we take the forward one first.",
                 *self._swap_head("Theorem 10.2"), FadeIn(box_a), FadeIn(box_b))
        self.cue("exactly when", Create(arrow))
        self.cue("the forward one", ReplacementTransform(arrow, fwd))

        # beat 2: strong induction, base case
        self.say("For the forward direction we use strong induction on the number of vertices n. "
                 "The base case is a single vertex, which has no edges at all, and zero is exactly one minus one. "
                 "So the claim holds for n equal to one.",
                 FadeIn(base))
        self.cue("no edges at all", FadeIn(base_l, shift=LEFT * 0.2))
        self.cue("the claim holds", Indicate(base, color=GREEN_B))

        # beat 3: remove a vertex
        self.say("For the inductive step, suppose the claim holds up to k vertices. "
                 "Now take a connected graph G with no cycles on k plus one vertices, and remove one vertex v with its edges. "
                 "Call what is left G prime, and notice that removing a vertex can never create a cycle.",
                 FadeOut(base), FadeOut(base_l),
                 LaggedStart(*[Create(e) for e in edges.values()], lag_ratio=0.1),
                 LaggedStart(*[FadeIn(n, scale=0.7) for n in nodes.values()], lag_ratio=0.1), FadeIn(g_l))
        self.cue("remove one vertex v",
                 self._paint(nodes[V_REM], CUT_C, CUT_C), v_edge.animate.set_stroke(CUT_C, opacity=0.3))
        self.cue("Call what is left G prime", ReplacementTransform(g_l, gp_l),
                 nodes[V_REM].animate.set_opacity(0.25))

        # beat 4: the hypothesis, then put v back
        self.say("Assume that G prime is still connected, which is the case the notes treat, and the other case is left as an exercise. "
                 "Then G prime is connected with no cycles on k vertices, so the induction hypothesis gives it k minus one edges.",
                 Indicate(VGroup(*[edges[e] for e in GP_EDGES]), color=GREEN_B))
        self.cue("k minus one edges", FadeIn(k_edges, shift=LEFT * 0.2))

        self.say("Now put v back. "
                 "If v had two edges or more, then the connected graph G prime would give a cycle through v. "
                 "But G has no cycles, so v has exactly one edge. "
                 "That makes k minus one plus one, which is k edges, exactly as the claim needs.",
                 nodes[V_REM].animate.set_opacity(1), self._paint(nodes[V_REM], BLUE_C, BLUE_E),
                 v_edge.animate.set_stroke(EDGE_C, opacity=1), ReplacementTransform(gp_l, txt("G", 32, YELLOW_D).move_to(gp_l)))
        self.cue("two edges or more", Create(second))
        self.cue("a cycle through v", *[e.animate.set_color(BAD_C) for e in cycle_edges])
        self.cue("v has exactly one edge", FadeOut(second),
                 *[e.animate.set_color(EDGE_C) for e in cycle_edges if e is not second])
        self.cue("which is k edges", FadeIn(g_edges, shift=UP * 0.2), Indicate(tree, color=YELLOW_D))
        self.hold(0.5)

    # ---- scene 5: Theorem 10.2, the converse ------------------------------------------
    def converse_proof(self):
        self.clear_stage(self._head)
        nodes, edges, graph = self._graph(CV_REL, CV_EDGES, (-3.0, -0.5), r=0.22, labels=False)
        a, b = mono("n - 1 edges", 30, GREEN_B), mono("n - 2 edges", 30, YELLOW_D)
        need = mono("needs at least n - 1", 30, BAD_C)
        stack = VGroup(a, b, need).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(graph, RIGHT, buff=1.2)
        a, b, need = stack
        box_a = box_label("connected, no cycles", BLUE_C, w=4.6, h=0.7, font_size=26)
        box_b = box_label("connected, n-1 edges", GREEN_C, w=4.6, h=0.7, font_size=26)
        pair = VGroup(box_a, box_b).arrange(RIGHT, buff=1.6).set_y(1.9)
        back = Arrow(box_b.get_left(), box_a.get_right(), buff=0.1, color=YELLOW_D, stroke_width=6)
        cut = edges[CV_CUT]
        cycle = [edges[e] for e in CV_EDGES[:3]]

        # beat 1: assume a cycle, remove one of its edges
        self.say("For the converse we argue by contradiction. "
                 "Suppose a graph G is connected, has n minus one edges, and still contains a cycle. "
                 "Then removing one edge of that cycle leaves G connected, with n minus two edges.",
                 *self._swap_head("Theorem 10.2, converse"), FadeIn(box_a), FadeIn(box_b), Create(back),
                 LaggedStart(*[Create(e) for e in edges.values()], lag_ratio=0.1),
                 LaggedStart(*[FadeIn(n, scale=0.7) for n in nodes.values()], lag_ratio=0.1))
        self.cue("Suppose a graph G", FadeIn(a, shift=LEFT * 0.2))
        self.cue("a cycle", *[e.animate.set_color(BAD_C) for e in cycle])
        self.cue("removing one edge of that cycle", cut.animate.set_stroke(CUT_C, opacity=0.25))
        self.cue("with n minus two edges", FadeIn(b, shift=LEFT * 0.2))

        # beat 2: the contradiction
        self.say("But a connected graph needs at least n minus one edges, which is a fact the notes leave as an exercise. "
                 "So n minus two edges are too few, we have a contradiction, and the converse is proved.",
                 FadeIn(need, shift=LEFT * 0.2), Indicate(a, color=GREEN_B))
        self.cue("too few", Indicate(b, color=BAD_C), Indicate(need, color=BAD_C))
        self.cue("the converse is proved", Indicate(VGroup(box_a, box_b), color=GREEN_B))
        self.hold(0.5)
