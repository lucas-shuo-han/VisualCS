"""Episode 1 of the CS70 Note 10 series: the seven bridges of Königsberg and Eulerian tours.

FACTS come from cs70/note10-deepseek/notes.txt (lines 16-21, 34-43, 51-57, 90-93,
174-184). The picture reads the names below; the narration says numbers as words, and every
spoken number has an assert here.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---- FACTS ---------------------------------------------------------------------------
# The land masses and the multiset of bridges of the notes:
#   V = {A,B,C,D}, E = {{A,B},{A,B},{A,C},{B,C},{B,D},{B,D},{C,D}}
TOWNS = ["A", "B", "C", "D"]
BRIDGES = (("A", "B"), ("A", "B"), ("A", "C"), ("B", "C"),
           ("B", "D"), ("B", "D"), ("C", "D"))
N_BRIDGES = len(BRIDGES)                                     # "seven"
DEG = {t: sum(1 for e in BRIDGES if t in e) for t in TOWNS}
assert DEG == {"A": 3, "B": 5, "C": 3, "D": 3}               # "three", "five", "three", "three"
assert N_BRIDGES == 7 and sum(DEG.values()) == 2 * N_BRIDGES == 14
assert all(d % 2 == 1 for d in DEG.values())                 # every degree is odd
N_LAND = len(TOWNS)                                          # "four"
assert N_LAND == 4
YEAR = 1736                                                  # "seventeen thirty six"
assert YEAR == 1736

# Where each bridge is drawn; two bridges between the same pair are bent apart, or they
# would look like one. This is the same multiset as BRIDGES.
PLAN_ORDER = (("A", "B", 0.5), ("A", "B", -0.5), ("A", "C", None), ("B", "C", None),
              ("B", "D", 0.5), ("B", "D", -0.5), ("C", "D", None))
assert sorted((a, b) for a, b, _ in PLAN_ORDER) == sorted(BRIDGES)
assert len(PLAN_ORDER) == 7 and len({frozenset((a, b)) for a, b, _ in PLAN_ORDER}) == 5
EDGES_AT = {t: tuple(i for i, (a, b, _) in enumerate(PLAN_ORDER) if t in (a, b)) for t in TOWNS}
assert tuple(len(EDGES_AT[t]) for t in TOWNS) == (3, 5, 3, 3)

# The walk of scene 1, one row per bridge crossed: (from, to, bridge index). It gets stuck.
WALK = (("A", "B", 0), ("B", "D", 4), ("D", "C", 6), ("C", "A", 2), ("A", "B", 1), ("B", "D", 5))
# (bridge index, 1 if the bridge is walked against its drawn direction)
LEG1 = ((0, 0), (4, 0))            # left bank -> island above -> right bank
LEG2 = ((6, 1), (2, 1))            # right bank -> island below -> left bank
LEG3 = ((1, 0), (5, 0))            # out again over both free bridges
LEGS = LEG1 + LEG2 + LEG3
CROSSED = len(WALK)                                          # "six"
BRIDGES_LEFT = N_BRIDGES - CROSSED                           # "one"
assert tuple(i for i, _ in LEGS) == tuple(i for _, _, i in WALK)
assert tuple((PLAN_ORDER[i][1], PLAN_ORDER[i][0]) if rev else PLAN_ORDER[i][:2]
             for i, rev in LEGS) == tuple((a, b) for a, b, _ in WALK)
assert WALK[0][0] == "A" and WALK[-1][1] == "D"
for k, (a, b, i) in enumerate(WALK):
    assert frozenset(PLAN_ORDER[i][:2]) == frozenset((a, b))
    if k:
        assert WALK[k - 1][1] == a                           # the walk goes on from where it is
assert len({i for _, _, i in WALK}) == CROSSED == 6 and BRIDGES_LEFT == 1
assert BRIDGES_LEFT + CROSSED == N_BRIDGES
assert {i for _, _, i in WALK} == set(range(N_BRIDGES)) - {3}   # the bridge B-C never crossed

# The example that does have a tour: two triangles that share the point 3, plus one point
# that no line touches. (Not in the notes: the notes give no worked Eulerian tour.)
TWIN = {1: np.array([-5.0, 1.9, 0.0]), 2: np.array([-5.0, -1.1, 0.0]),
        3: np.array([-3.0, 0.4, 0.0]), 4: np.array([-1.0, 1.9, 0.0]),
        5: np.array([-1.0, -1.1, 0.0]), 6: np.array([-6.0, -2.2, 0.0])}
TWIN_EDGES = ((1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 3))
TOUR = (1, 2, 3, 4, 5, 3, 1)
N_TRI = 2                                                     # "two triangles"
DEG2 = {v: sum(1 for e in TWIN_EDGES if v in e) for v in TWIN}
TOUR_IDX = tuple(TWIN_EDGES.index((TOUR[k], TOUR[k + 1])) for k in range(len(TOUR) - 1))
# The tour, cut into the three pieces the narration names: (edge index, walked backwards?)
TOUR_LEGS = (((0, 0), (1, 0)), ((3, 0), (4, 0), (5, 0)), ((2, 0),))
assert DEG2 == {1: 2, 2: 2, 3: 4, 4: 2, 5: 2, 6: 0}
assert all(d % 2 == 0 for d in DEG2.values())                # every degree is even
assert len(TWIN_EDGES) == 6 and len(TOUR) - 1 == 6 and TOUR[0] == TOUR[-1] == 1
assert TOUR_IDX == (0, 1, 3, 4, 5, 2)
assert tuple(i for leg in TOUR_LEGS for i, _ in leg) == TOUR_IDX and all(
    rev == 0 for leg in TOUR_LEGS for _, rev in leg)   # every tour edge matches its drawn direction
assert TWIN_EDGES[0] == (TOUR[0], TOUR[1]) and TWIN_EDGES[2] == (TOUR[-2], TOUR[-1])
_used = sorted(tuple(sorted(TOUR[k:k + 2])) for k in range(len(TOUR) - 1))
assert _used == sorted(tuple(sorted(e)) for e in TWIN_EDGES)  # every line exactly once
assert DEG2[6] == 0 and 6 not in [v for e in TWIN_EDGES for v in e]
assert DEG2[3] == 4 and N_TRI * 3 == 6

# Geometry (kept inside x = +-6.8 and y = -2.9 .. 3.3; the labels sit outward from the graph)
POS = {"A": np.array([-4.4, 1.0, 0.0]), "B": np.array([-0.9, 1.95, 0.0]),
       "C": np.array([-0.9, -1.35, 0.0]), "D": np.array([2.9, 1.0, 0.0])}
R_CITY, R_GRAPH = 0.85, 0.40
EDGE_C, CROSS_C, ODD_C = BLUE_B, YELLOW_D, RED_C


class Ep01Konigsberg(NarratedScene):
    SCENES = ["seven_bridges", "as_a_graph", "pen_argument", "eulers_theorem"]

    def construct(self):
        if self.preview_only(self.SCENES):
            return
        self.title_card()
        for name in self.SCENES:
            getattr(self, name)()
        self.end_card(["Königsberg has four pieces of land, seven bridges, and all four degrees are odd",
                       "So no walk crosses every bridge exactly once and returns to its starting point",
                       "Euler's theorem says a tour exists exactly when every degree is even and the graph "
                       "is connected",
                       "A point with no lines at all is the one exception, since no walk ever visits it"])

    # ---- drawing helpers -------------------------------------------------------------
    def _picture(self, r, label_size):
        """Four land masses (a circle with its letter) and the seven bridges between them."""
        parts = []
        for t in TOWNS:
            c = Circle(radius=r, stroke_color=BLUE_C, stroke_width=3,
                       fill_color=BLUE_E, fill_opacity=0.35).move_to(POS[t])
            parts.append(VGroup(c, txt(t, label_size, WHITE).next_to(c, ORIGIN)))
        for a, b, bend in PLAN_ORDER:
            parts.append(self._line(POS[a], POS[b], r, bend))
        return VGroup(*parts)

    def _line(self, p, q, r, bend=None, color=EDGE_C):
        """A line from the edge of the circle at p to the edge of the circle at q."""
        d = (q - p) / np.linalg.norm(q - p)
        s, e = p + d * r, q - d * r
        if bend is None:
            return Line(s, e, stroke_color=color, stroke_width=3)
        return ArcBetweenPoints(s, e, angle=bend, stroke_color=color, stroke_width=3)

    def _edge_path(self, edges, steps):
        """An invisible path through the bridges `steps` (index, walked backwards?), from
        circle edge to circle edge, crossing the land mass in between like a walker."""
        pts = []
        for i, rev in steps:
            e = edges[i]
            alphas = np.linspace(1, 0, 10) if rev else np.linspace(0, 1, 10)
            pts += [e.point_from_proportion(float(t)) for t in alphas]
        p = VMobject(stroke_opacity=0, stroke_width=0)
        p.set_points_as_corners(pts)
        return p

    def _swap_head(self, text):
        new = self.heading(text)
        old = getattr(self, "_head", None)
        anims = [Write(new)] if old is None else [FadeOut(old, run_time=0.5), Write(new)]
        self._head = new
        return anims

    def _mark(self, point, value, direction, color, size=30):
        """A number next to a point: the number of lines at it."""
        return num(value, size, color).next_to(point, direction, buff=0.16)

    # ---- scene 1: the concrete case --------------------------------------------------
    def seven_bridges(self):
        city = self._picture(R_CITY, 40)
        circles = VGroup(*city[:N_LAND])
        bridges = VGroup(*city[N_LAND:])
        w_dot = Dot(bridges[0].point_from_proportion(0.0), radius=0.14, color=GREEN_C)
        crossed = mono(f"{CROSSED} of {N_BRIDGES} crossed", 28, CROSS_C).next_to(city, DOWN, buff=0.18)

        # beat 1: the city, its four lands and its seven bridges
        self.say("This is Königsberg, a city on the Pregel river, with four pieces of land and "
                 "seven bridges. The people there liked to walk, and they wanted a route that "
                 "crossed every bridge exactly once and came home again.",
                 *self._swap_head("Königsberg, 1736"),
                 LaggedStart(*[FadeIn(c, scale=0.6) for c in circles], lag_ratio=0.15))
        self.cue("seven bridges", LaggedStart(*[Create(b) for b in bridges], lag_ratio=0.16))

        # beat 2: a first try that walks and gets stuck
        self.say("Start on the left bank and cross to the island above, and from there go across to "
                 "the right bank. Then walk down to the island below and back to the left bank, and "
                 "two more bridges are behind us. Six of the seven bridges are behind us, and we are "
                 "standing on the right bank with one bridge still waiting.",
                 FadeIn(w_dot))
        self.cue("cross to the island above",
                 MoveAlongPath(w_dot, self._edge_path(bridges, LEG1), run_time=2.6),
                 *[bridges[i].animate.set_color(CROSS_C) for i, _ in LEG1])
        self.cue("Then walk down to the island below",
                 MoveAlongPath(w_dot, self._edge_path(bridges, LEG2), run_time=2.6),
                 *[bridges[i].animate.set_color(CROSS_C) for i, _ in LEG2])
        self.cue("Six of the seven bridges",
                 MoveAlongPath(w_dot, self._edge_path(bridges, LEG3), run_time=2.4),
                 *[bridges[i].animate.set_color(CROSS_C) for i, _ in LEG3])
        self.cue("one bridge still waiting", FadeIn(crossed))

        # beat 3: the question Euler asked instead
        self.say("Six bridges crossed and one still standing, so this route has failed, but maybe a "
                 "cleverer route exists. In seventeen thirty six a mathematician named Leonhard "
                 "Euler asked a sharper question about all routes at once.",
                 Indicate(VGroup(*[bridges[i] for i, _ in LEGS]), color=CROSS_C))
        self.cue("one still standing", Indicate(bridges[3], color=BLUE_B))
        self.cue("a sharper question", Indicate(circles, color=CROSS_C), FadeOut(w_dot))
        self.hold(0.5)
        self.city, self.bridges, self.crossed = city, bridges, crossed

    # ---- scene 2: the abstraction ----------------------------------------------------
    def as_a_graph(self):
        city, bridges = self.city, self.bridges
        graph = self._picture(R_GRAPH, 26)
        where = {"A": LEFT, "B": UP, "C": LEFT, "D": RIGHT}
        # the numbers belong to the small circles, so place them against the graph, not the city
        marks = {t: self._mark(graph[TOWNS.index(t)][0], DEG[t], where[t], YELLOW_D) for t in TOWNS}
        legend = txt("degree = the lines at a point", 26, GREEN_B).next_to(graph, DOWN, buff=0.25)

        # beat 1: the Transform of the whole picture
        self.say("Now Euler threw away the river and the houses, and kept only what a walk can feel. "
                 "Every piece of land becomes a single point, and every bridge becomes a line "
                 "joining the two points that it touches.",
                 *self._swap_head("Euler's abstraction"), Transform(city, graph), FadeOut(self.crossed),
                 run_time=1.6)
        self.cue("every bridge becomes a line", Indicate(bridges, color=YELLOW_D))

        # beat 2: count the lines at each point
        self.say("That leaves four points and seven lines, and the whole problem is now about these "
                 "lines. Look at the island above and count the lines that touch it, and you will "
                 "find five. The other three points each have three lines, so the four numbers are "
                 "five, three, three and three.",
                 Indicate(city, color=YELLOW_D))
        self.cue("count the lines that touch it",
                 Indicate(VGroup(*[city[i] for i in EDGES_AT["B"]]), color=YELLOW_D),
                 FadeIn(marks["B"]))
        self.cue("The other three points",
                 LaggedStart(*[FadeIn(marks[t]) for t in ("A", "C", "D")], lag_ratio=0.3))

        # beat 3: the name of that count
        self.say("The number of lines at a point is called its degree, and a point with no lines at "
                 "all is isolated. Here no point is isolated, and every one of the four degrees is "
                 "odd, which is the difficulty.",
                 FadeIn(legend, shift=UP * 0.2))
        self.cue("every one of the four degrees", Indicate(VGroup(*marks.values()), color=YELLOW_D))
        self.hold(0.5)
        self.marks, self.legend = marks, legend

    # ---- scene 3: the parity argument ------------------------------------------------
    def pen_argument(self):
        city, bridges, marks = self.city, self.bridges, self.marks
        pen = Dot(bridges[0].point_from_proportion(0.0), radius=0.13, color=GREEN_C)
        a_lines = VGroup(*[bridges[i] for i in EDGES_AT["A"]])
        no_tour = txt("no tour", 32, RED_C).next_to(marks["D"], RIGHT, buff=0.4)

        # beat 1: the pen
        self.say("Euler turned the walk into a pen that traces every line once and comes back to "
                 "where it started. The pen never lifts, and no line is traced twice. So think "
                 "about one point of the picture and the visits the pen makes to it.",
                 *self._swap_head("One point at a time"), FadeIn(pen),
                 *[b.animate.set_color(EDGE_C) for b in bridges])   # a clean picture for this argument
        self.cue("The pen never lifts",
                 MoveAlongPath(pen, self._edge_path(bridges, ((0, 0), (1, 1))), run_time=2.6))
        self.cue("one point of the picture", Indicate(a_lines, color=YELLOW_D), Indicate(marks["A"]))

        # beat 2: arriving and leaving pair up
        self.say("Every visit to a point uses one line to arrive and another line to leave. That "
                 "means the lines at the point can be paired up, one arrival with one departure, "
                 "which forces their number to be even. Here the points have degrees three, five, "
                 "three and three, and not one of those numbers is even.",
                 *[bridges[i].animate.set_color(GREEN_C) for i in (0, 1)])
        self.cue("forces their number to be even",
                 bridges[2].animate.set_color(RED_C), Indicate(marks["A"]))
        self.cue("not one of those numbers is even", Indicate(VGroup(*marks.values()), color=RED_C))

        # beat 3: the answer to Königsberg
        self.say("So at every point of Königsberg a walk would be left with one line that it cannot "
                 "use, and the tour is impossible. In seventeen thirty six Euler proved it, and he "
                 "also found exactly when a tour is possible.",
                 FadeOut(pen), FadeIn(no_tour, shift=LEFT * 0.2))
        self.cue("Euler proved it", Indicate(city, color=YELLOW_D))
        self.hold(0.5)
        self.no_tour = no_tour

    # ---- scene 4: Euler's theorem and an example that works ---------------------------
    def eulers_theorem(self):
        twin_r = 0.40
        nodes = VGroup()
        for v in (1, 2, 3, 4, 5):
            c = Circle(radius=twin_r, stroke_color=BLUE_C, stroke_width=3,
                       fill_color=BLUE_E, fill_opacity=0.35).move_to(TWIN[v])
            nodes.add(VGroup(c, txt(str(v), 26, WHITE).next_to(c, ORIGIN)))
        iso_c = Circle(radius=twin_r, stroke_color=GREY_B, stroke_width=3,
                       fill_color=BLUE_E, fill_opacity=0.35).move_to(TWIN[6])
        iso = VGroup(iso_c, txt("6", 26, GREY_A).next_to(iso_c, ORIGIN))
        edges = VGroup(*[self._line(TWIN[a], TWIN[b], twin_r) for a, b in TWIN_EDGES])
        dirs = {1: UP, 2: DOWN, 3: LEFT, 4: UP, 5: DOWN}
        degs = {v: self._mark(nodes[v - 1][0], DEG2[v], dirs[v], GREEN_C) for v in dirs}
        zero = self._mark(iso_c, DEG2[6], UP, GREEN_C)
        conds = VGroup(txt("every degree even", 26, GREEN_C),
                       txt("connected, except isolated points", 26, GREEN_C))
        conds.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        conds.next_to(edges, RIGHT, buff=0.7)
        cond1, cond2 = conds
        t_dot = Dot(edges[0].point_from_proportion(0.0), radius=0.13, color=CROSS_C)
        old = [self.city] + list(self.marks.values()) + [self.legend, self.no_tour]

        # beat 1: the two words
        self.say("A walk that uses every line exactly once is called an Eulerian walk, and if it ends "
                 "where it started we call it an Eulerian tour. Königsberg asked for such a tour, "
                 "and now we want to know which graphs have one.",
                 *self._swap_head("Euler's theorem"), FadeOut(*old),
                 LaggedStart(*[FadeIn(n, scale=0.7) for n in list(nodes) + [iso]], lag_ratio=0.12),
                 LaggedStart(*[Create(e) for e in edges], lag_ratio=0.12),
                 run_time=1.4)
        self.cue("which graphs have one", Indicate(edges, color=YELLOW_D))

        # beat 2: the theorem
        self.say("Euler's theorem answers the question with two conditions that we can check by "
                 "looking. A graph has an Eulerian tour exactly when every degree is even and the "
                 "graph is connected. The only exception is a point with no lines at all, which a "
                 "walk simply never visits.",
                 LaggedStart(*[FadeIn(degs[v]) for v in sorted(degs)], lag_ratio=0.2),
                 FadeIn(zero))
        self.cue("every degree is even", FadeIn(cond1, shift=LEFT * 0.2))
        self.cue("The only exception", FadeIn(cond2, shift=LEFT * 0.2), Indicate(iso))

        # beat 3: one tour, and the lonely point
        self.say("In this little graph every degree is even, and the whole graph is connected, so a "
                 "tour must exist. The lonely point at the bottom left has no lines, so its degree "
                 "is zero, and the walk ignores it. Here is one tour, and it walks around the left "
                 "triangle, then the right one, and returns.",
                 Indicate(VGroup(*degs.values(), zero), color=GREEN_B), FadeIn(t_dot))
        self.cue("lonely point at the bottom left", Indicate(iso, color=YELLOW_D))
        self.cue("walks around the left triangle",
                 MoveAlongPath(t_dot, self._edge_path(edges, TOUR_LEGS[0]), run_time=2.2),
                 *[edges[i].animate.set_color(CROSS_C) for i in TOUR_IDX[:2]])
        self.cue("then the right one",
                 MoveAlongPath(t_dot, self._edge_path(edges, TOUR_LEGS[1]), run_time=3.0),
                 *[edges[i].animate.set_color(CROSS_C) for i in TOUR_IDX[2:5]])
        self.cue("and returns",
                 MoveAlongPath(t_dot, self._edge_path(edges, TOUR_LEGS[2]), run_time=1.2),
                 edges[TOUR_IDX[5]].animate.set_color(CROSS_C))

        # beat 4: the same test for both puzzles
        self.say("So the same test decides both puzzles, the seven bridges and this little graph of "
                 "two triangles. You count what touches each point, and you look at whether the "
                 "picture holds together.",
                 Indicate(edges, color=CROSS_C))
        self.cue("whether the picture holds together", Indicate(VGroup(cond1, cond2), color=YELLOW_D))
        self.hold(0.5)
