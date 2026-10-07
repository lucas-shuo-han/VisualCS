# PLAN: Königsberg Bridges and Eulerian Tours

Source: CS70 Note 10, Graph Theory  ·  Language: en

- **The question**: Can you walk across each of the seven bridges of Königsberg exactly once and return to your starting point?
- **The worked example**: The seven bridges of Königsberg, Prussia, connecting four land masses A, B, C, D. The degrees are: A=3, B=5, C=3, D=3 (all odd).
- **The surprise**: Euler proved this is impossible, not by trying all paths, but by showing that every vertex must have even degree for such a walk to exist.

## Scenes

| # | Method name | The picture: what is built, what changes | Ends when the viewer has seen |
|---|---|---|---|
| 1 | `bridge_problem` | Text describing the problem, city name, bridge count, and land mass count | The impossible challenge: cross each bridge exactly once |
| 2 | `graph_abstraction` | Vertices (circles) for land masses and edges (lines) for bridges; labeled clearly | How the problem maps to a simple graph with 4 vertices and 7 edges |
| 3 | `degree_observation` | Degree of each vertex displayed, color-coded (red for odd, green for even); Euler's theorem statement | Why Königsberg's walk is impossible: all vertices have odd degree |

## Chain table, one per scene

### Scene 1: `bridge_problem`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 1.1 | In the eighteen hundreds, the city of Königsberg, Prussia, had a famous puzzle. Seven bridges connected four land masses across the Pregel river. | screen | Title appears; city name displayed |
| 1.2 | The question was simple: could you take a walk that crosses each bridge exactly once and returns to your starting point? | 1.1 | Problem text appears; bridge count (7) and land mass count (4) displayed |
| 1.3 | For two centuries, nobody could do it. Then in seventeen thirty-six, Leonhard Euler proved it was impossible. | 1.2 | Problem text highlighted in red to show impossibility |

### Scene 2: `graph_abstraction`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 2.1 | To solve this, Euler used abstraction. Each land mass becomes a point, called a vertex, and each bridge becomes a line, called an edge. | screen | Title "Abstraction: A Graph" appears |
| 2.2 | Here we have four vertices representing the four land masses. | 2.1 | Four circles (vertices) appear at positions for A, B, C, D |
| 2.3 | And the seven bridges become seven edges connecting these vertices. | 2.2 | Seven lines (edges) appear connecting the vertices, representing the bridges |

### Scene 3: `degree_observation`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 3.1 | Now, here is the key insight. For a closed walk that uses each edge exactly once, every time you enter a vertex you must also leave it. This means each vertex must have an even number of edges. | screen | Title appears; graph from scene 2 remains visible |
| 3.2 | Let us count the edges at each vertex. Vertex A has three, vertex B has five, and vertices C and D each have three. | 3.1 | Degree labels appear at each vertex: A=3, B=5, C=3, D=3 (in red for odd) |
| 3.3 | Three and five are odd numbers. Since all four vertices have odd degree, no such walk is possible. | 3.2 | Degree labels flash in red to emphasize that all are odd |
| 3.4 | This is Euler's theorem. A closed walk using each edge exactly once exists if and only if every vertex has an even number of edges. | 3.3 | Euler's theorem statement displayed prominently on screen |

## Gate

- [x] The first row of scene 1 shows one concrete case (Königsberg) with real numbers (7 bridges, 4 land masses).
- [x] Every "uses" cell names an earlier row or the screen.
- [x] Every name and formula comes after the row where the viewer sees it happen (degrees shown before theorem).
- [x] The last scene answers the question (no walk is possible because all vertices have odd degree).

## Coverage

Every item of the notes: concept, rule, table, worked example, exercise.

| Notes item | Scene · row | or left out, because |
|---|---|---|---|
| Königsberg problem (Section 1 intro) | 1.1, 1.2, 1.3 | |
| Graph formal definition (Section 1.1) | 2.1 (informal version) | Formal notation deferred to later episode |
| Vertices and edges terminology | 2.1, 2.2, 2.3 | |
| Paths, walks, cycles, tours (Section 1.2) | Implicit in 3.1 | Full definitions left out: later episode |
| Connectivity (Section 1.3) | Not shown explicitly | Implicit in graph structure; left out: later episode |
| Eulerian tours definition | 3.1 (informal) | Formal definition brief; full terminology left out: later episode |
| Euler's Theorem 10.1 | 3.4 | Full proof and conditions left out: later episode |
| Trees and Complete Graphs (Section 3) | | Left out: later episode |
| Planar Graphs and Euler's Formula (Section 4-5) | | Left out: later episode |
| Hypercubes and other advanced topics | | Left out: later episode |
