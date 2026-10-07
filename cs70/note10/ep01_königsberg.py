"""Episode 1: Königsberg Bridges and Eulerian Tours

Topics: Königsberg problem, graph abstraction, degrees, Euler's theorem.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manim_kit import *  # noqa: E402,F403

# ---- FACTS: The Königsberg bridges problem
NUM_BRIDGES = 7
NUM_LANDMASSES = 4
VERTICES = ["A", "B", "C", "D"]
# Edges in the multigraph: A-B (×2), A-C (×1), B-C (×1), B-D (×2), C-D (×1)
EDGES = [("A", "B"), ("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("B", "D"), ("C", "D")]
assert len(EDGES) == NUM_BRIDGES == 7

# Compute degrees
DEGREES = {}
for v in VERTICES:
    count = 0
    for u, w in EDGES:
        if u == v or w == v:
            count += 1
    DEGREES[v] = count

# All vertices should have odd degree in Königsberg
assert DEGREES["A"] == 3 and DEGREES["B"] == 5 and DEGREES["C"] == 3 and DEGREES["D"] == 3
assert all(d % 2 == 1 for d in DEGREES.values()), "All vertices must have odd degree"

# Count the odd degree vertices
ODD_VERTICES = [v for v in VERTICES if DEGREES[v] % 2 == 1]
assert len(ODD_VERTICES) == 4


class Ep01Königsberg(NarratedScene):
    SCENES = ["bridge_problem", "graph_abstraction", "degree_observation"]

    def construct(self):
        if self.preview_only(self.SCENES):
            return
        self.title_card()
        for name in self.SCENES:
            getattr(self, name)()
        self.end_card([
            "Königsberg residents wanted to cross each of the seven bridges exactly once.",
            "As a graph, each land mass becomes a vertex and each bridge becomes an edge.",
            "Euler showed that such a tour is possible if and only if all vertices have even degree."
        ])

    # ---- scene 1: The Königsberg bridge problem
    def bridge_problem(self):
        head = self.heading("The Königsberg Bridges")

        # Create a simple text description of the problem
        problem_text = txt("Cross each bridge exactly once,\nstarting and ending at the same place.", 28)
        problem_text.set_y(0.5)

        city_text = txt("City of Königsberg", 24, GREY_A).set_y(-0.3)
        bridges_text = mono(f"{NUM_BRIDGES} bridges", 32, YELLOW_D).set_y(-1.2)
        landmasses_text = txt(f"{NUM_LANDMASSES} land masses", 26).set_y(-1.8)

        self.say("In the eighteen hundreds, the city of Königsberg, Prussia, had a famous puzzle.\n"
                 "Seven bridges connected four land masses across the Pregel river.",
                 Write(head), FadeIn(city_text, shift=UP * 0.2))
        self.cue("Seven bridges", FadeIn(bridges_text))
        self.cue("four land masses", FadeIn(landmasses_text))

        self.say("The question was simple: could you take a walk that crosses each bridge exactly once "
                 "and returns to your starting point?",
                 FadeOut(city_text), FadeIn(problem_text, shift=UP * 0.2))

        self.say("For two centuries, nobody could do it. "
                 "Then in seventeen thirty-six, Leonhard Euler proved it was impossible.",
                 Indicate(problem_text, color=RED_C))
        self.hold()
        self.play(FadeOut(head), FadeOut(problem_text), FadeOut(bridges_text), FadeOut(landmasses_text))

    # ---- scene 2: Graph abstraction
    def graph_abstraction(self):
        head = self.heading("Abstraction: A Graph")

        # Create vertices (circles) for the land masses
        positions = {
            "A": np.array([-4, 0.8, 0]),
            "B": np.array([-1.5, 1.2, 0]),
            "C": np.array([-1.5, -1.2, 0]),
            "D": np.array([2, 0, 0])
        }

        vertices = {}
        labels = {}
        for v in VERTICES:
            circle = Circle(0.35, stroke_color=BLUE_C, stroke_width=2, fill_color=BLUE_C, fill_opacity=0.2)
            circle.move_to(positions[v])
            vertices[v] = circle
            label = mono(v, 32, YELLOW_D)
            label.move_to(positions[v])
            labels[v] = label

        # Create edges (lines) for the bridges - simple lines for now
        edge_objs = []
        edge_colors = [TEAL_C, TEAL_C, GREEN_C, RED_C, GOLD_C, GOLD_C, PURPLE_C]
        for idx, (u, w) in enumerate(EDGES):
            line = Line(positions[u], positions[w], color=edge_colors[idx], stroke_width=2)
            edge_objs.append(line)

        self.say("To solve this, Euler used abstraction. "
                 "Each land mass becomes a point, called a vertex, and each bridge becomes a line, called an edge.",
                 Write(head))

        self.say("Here we have four vertices representing the four land masses.",
                 *[FadeIn(v) for v in vertices.values()])

        self.cue("four vertices", *[FadeIn(labels[v]) for v in VERTICES])

        self.say("And the seven bridges become seven edges connecting these vertices.",
                 *[Create(e) for e in edge_objs])

        self.hold()
        self.play(FadeOut(head))

        # Store for next scene
        self.vertices_group = VGroup(*vertices.values())
        self.labels_group = VGroup(*labels.values())
        self.edges_group = VGroup(*edge_objs)

    # ---- scene 3: Degree observation
    def degree_observation(self):
        head = self.heading("The Degree of Each Vertex")

        vertices_group = self.vertices_group
        labels_group = self.labels_group
        edges_group = self.edges_group

        self.say("Now, here is the key insight. For a closed walk that uses each edge exactly once, "
                 "every time you enter a vertex you must also leave it.\n"
                 "This means each vertex must have an even number of edges.",
                 Write(head))

        self.cue("even number of edges", Indicate(vertices_group, color=YELLOW_D))

        # Show degree of each vertex
        degree_labels = []
        positions_deg = {
            "A": np.array([-4, 0.8, 0]),
            "B": np.array([-1.5, 1.2, 0]),
            "C": np.array([-1.5, -1.2, 0]),
            "D": np.array([2, 0, 0])
        }
        for v in VERTICES:
            deg_text = mono(f"degree {DEGREES[v]}", 20, RED_C if DEGREES[v] % 2 == 1 else GREEN_C)
            deg_text.next_to(positions_deg[v], DOWN, buff=0.3)
            degree_labels.append(deg_text)

        self.say("Let us count the edges at each vertex. "
                 "Vertex A has three, vertex B has five, and vertices C and D each have three.",
                 *[FadeIn(d) for d in degree_labels])

        self.say("Three and five are odd numbers. Since all four vertices have odd degree, "
                 "no such walk is possible.",
                 *[Indicate(d, color=RED_C) for d in degree_labels if d in degree_labels[:4]])

        # Show Euler's theorem
        theorem_text = txt("Euler's Theorem: A graph has an Eulerian tour\nif and only if all vertices have even degree.", 24, GREEN_B)
        theorem_text.set_y(-2.2)

        self.say("This is Euler's theorem. A closed walk using each edge exactly once exists "
                 "if and only if every vertex has an even number of edges.",
                 FadeOut(head), FadeOut(vertices_group), FadeOut(labels_group), FadeOut(edges_group),
                 *[FadeOut(d) for d in degree_labels], FadeIn(theorem_text, shift=UP * 0.2))

        self.hold(0.5)
