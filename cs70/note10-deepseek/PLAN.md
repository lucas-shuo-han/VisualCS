# PLAN: The Seven Bridges of Königsberg — Eulerian tours

Source: `cs70/note10-deepseek/notes.txt` (line numbers below are lines of that file) · Language: en

- **The question** the viewer cannot answer before and can after: *can a walk cross each of the seven
  Königsberg bridges exactly once and come back to where it started — and in general, which pictures
  allow such a walk?*
- **The worked example**, with its numbers (the names in the FACTS block): the notes' multiset
  `BRIDGES = {{A,B},{A,B},{A,C},{B,C},{B,D},{B,D},{C,D}}`, so `N_BRIDGES = 7` and
  `DEG = {A: 3, B: 5, C: 3, D: 3}` (all odd); the walk `WALK = A B D C A B D` crosses
  `CROSSED = 6` bridges with `LEFT = 1` left; the yes-example `TRI*` has `DEG2 = {1:2, 2:2, 3:4, 4:2, 5:2}`
  plus one isolated vertex of degree 0 and the tour `TOUR = 1 2 3 4 5 3 1` (6 edges).
- **The surprise**: the natural first try walks and gets stuck; the fix is not a better route but
  *parity* — a walk enters and leaves each land mass, so every degree must be even.

## Scenes

| # | Method name | The picture: what is built, what changes | Ends when the viewer has seen |
|---|---|---|---|
| 1 | `seven_bridges` | four land-mass circles labelled A B C D (r = 0.85) with seven bridges drawn between their edges (two pairs bent apart with ±0.5 arcs); a dot walks 6 of the 7 bridges and they turn yellow, the seventh stays blue; a label "6 of 7 crossed" | the concrete case, the 7 bridges, and a route that fails |
| 2 | `as_a_graph` | the same four blobs shrink into four small circles (r = 0.40) and the bridges stay as lines (one Transform); the degree of each point appears next to it (3, 5, 3, 3), then a legend "degree = the lines at a point" | the abstract graph and the four numbers a walk must obey |
| 3 | `pen_argument` | a pen dot travels out of A along one bridge and back along the other; two of A's three lines turn green (one arrival + one departure), the third turns red; the four degree labels flash red; a label "no tour" appears beside the graph | why an odd degree kills the tour, and that Königsberg has four odd degrees |
| 4 | `eulers_theorem` | the Königsberg graph is replaced by two triangles sharing a point, plus one isolated point; degrees 2 2 4 2 2 and 0 appear; two condition labels appear at the right; a dot walks the whole tour 1-2-3-4-5-3-1 and the six lines turn yellow | the two conditions of Euler's theorem and a tour that exists |

## Chain table, one per scene

### Scene 1: `seven_bridges`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 1.1 | This is Königsberg, a city on the Pregel river, with four pieces of land and seven bridges. | screen | four land-mass circles fade in, left to right, each with its letter A B C D |
| 1.2 | The people there liked to walk, and they wanted a route that crossed every bridge exactly once and came home again. | 1.1 | the seven bridges are drawn one after the other (drawing a pair bent apart) |
| 1.3 | Start on the left bank and cross to the island above, and from there go across to the right bank. | 1.2 | a dot appears at A and walks A→B→D, those bridges turn yellow |
| 1.4 | Then walk down to the island below, back to the left bank, and out over the last bridge you can still reach. | 1.3 | the dot walks D→C→A→B→D; five more bridges turn yellow |
| 1.5 | Six of the seven bridges are behind us, and we are standing on the right bank with one bridge still waiting. | 1.4 | the untouched bridge B–C is indicated; the label "6 of 7 crossed" appears under the graph |
| 1.6 | Six bridges crossed and one still standing, so this route has failed, but maybe a cleverer route exists. | 1.5 | the dot and the label stay; the crossed bridges keep their colour |
| 1.7 | In seventeen thirty six a mathematician named Leonhard Euler asked a sharper question about all routes at once. | 1.2 | the year 1736 is written as a small heading line, the graph is dimmed by an Indicate |
| 1.8 | To answer it he threw away the river and the houses and kept only what a walk can feel. | 1.7 | the graph is Indicated again, preparing the Transform of scene 2 |

### Scene 2: `as_a_graph`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 2.1 | Now Euler threw away the river and the houses, and kept only what a walk can feel. | 1.1–1.8 | the four blobs shrink into four small circles (Transform of the whole picture) |
| 2.2 | Every piece of land becomes a single point, and every bridge becomes a line joining the two points that it touches. | 2.1 | the bridges are Indicated as they settle as lines between the small circles |
| 2.3 | That leaves four points and seven lines, and the whole problem is now about these lines. | 2.1 | the four circles and the seven lines are Indicated together |
| 2.4 | Look at the island above and count the lines that touch it, and you find five. | 2.2 | the label "5" fades in next to point B, its five lines are Indicated |
| 2.5 | The other three points each have three lines, so the four numbers are five, three, three and three. | 2.4 | the labels 3, 3, 3 fade in next to A, C, D |
| 2.6 | The number of lines at a point is called its degree, and a point with no lines at all is isolated. | 2.4 | the legend "degree = the lines at a point" fades in under the graph |
| 2.7 | Here no point is isolated, and every one of the four degrees is odd, which is the difficulty. | 2.5, 2.6 | the four degree labels are Indicated together |

### Scene 3: `pen_argument`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 3.1 | Euler turned the walk into a pen that traces every line once and comes back to where it started. | 2.1 | a pen dot appears at point A on the graph of scene 2 |
| 3.2 | The pen never lifts, and no line is traced twice. | 3.1 | the pen dot slides from A to B along one bridge and back along the other |
| 3.3 | So think about one point of the picture and the visits the pen makes to it. | 3.2 | the pen dot is left at A and A is Indicated |
| 3.4 | Every visit to a point uses one line to arrive and another line to leave. | 3.3 | one arriving and one leaving line of A turn green |
| 3.5 | That means the lines at the point can be paired up, one arrival with one departure, which forces their number to be even. | 3.4 | the leftover third line of A turns red and is Indicated; the text "one line left over" is not drawn, the red line says it |
| 3.6 | Here the points have degrees three, five, three and three, and not one of those numbers is even. | 3.5 | the four degree labels flash red |
| 3.7 | So at every point of Königsberg a walk would be left with one line that it cannot use, and the tour is impossible. | 3.4, 3.6 | the label "no tour" fades in beside the graph, the legend of scene 2 fades out |
| 3.8 | In seventeen thirty six Euler proved it, and he also found exactly when a tour is possible. | 3.7 | the graph is Indicated once more (the last thing before scene 4) |

### Scene 4: `eulers_theorem`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 4.1 | A walk that uses every line exactly once is called an Eulerian walk, and if it ends where it started we call it an Eulerian tour. | screen | the Königsberg graph fades out and the two-triangle graph with its isolated point fades in |
| 4.2 | Königsberg asked for such a tour, and now we want to know which graphs have one. | 4.1 | the six lines and six points of the new graph are Indicated |
| 4.3 | Euler's theorem answers the question with two conditions that we can check by looking. | 4.2 | the point labels 2 2 4 2 2 and 0 appear next to the points |
| 4.4 | A graph has an Eulerian tour exactly when every degree is even and the graph is connected. | 4.3 | the label "every degree even" fades in at the right of the graph |
| 4.5 | The only exception is a point with no lines at all, which a walk simply never visits. | 4.4 | the label "connected, ignoring isolated points" fades in under it, the isolated point and its 0 are Indicated |
| 4.6 | In this little graph every degree is even, and the whole graph is connected, so a tour must exist. | 4.3 | the ten degree labels of the example are Indicated |
| 4.7 | The lonely point at the bottom left has no lines, so its degree is zero, and the walk ignores it. | 4.5 | the isolated point and its label 0 are Indicated |
| 4.8 | Here is one tour, and it walks around the left triangle, then the right one, and returns. | 4.6 | the dot appears at point 1, walks 1-2-3 (two lines turn yellow), then 3-4-5-3, then 3-1; all six lines are yellow |
| 4.9 | So the same test decides both puzzles, the seven bridges and this little graph of two triangles. | 1.8, 4.8 | the six yellow lines are Indicated as one group |
| 4.10 | You count what touches each point, and you look at whether the picture holds together. | 4.4, 4.5 | the two condition labels are Indicated |

Narration rows are grouped into beats of 2–4 sentences as STRICT.md step 3 requires:
1.1+1.2 (beat 1), 1.3+1.4+1.5 (beat 2), 1.6+1.7+1.8 (beat 3);
2.1+2.2 (beat 1), 2.3+2.4+2.5 (beat 2), 2.6+2.7 (beat 3);
3.1+3.2+3.3 (beat 1), 3.4+3.5+3.6 (beat 2), 3.7+3.8 (beat 3);
4.1+4.2 (beat 1), 4.3+4.4+4.5 (beat 2), 4.6+4.7+4.8 (beat 3), 4.9+4.10 (beat 4).

## Stated facts

| The fact, as it will be said | Notes line number (of notes.txt) | All conditions kept? |
|---|---|---|
| Königsberg lies on the Pregel river and had four pieces of land and seven bridges | 16–21 | yes (four land masses A B C D, seven bridges) |
| The residents wanted a route crossing each bridge exactly once and returning to the start | 19–21 | yes ("precisely once" and "return to the starting point") |
| Leonhard Euler proved this impossible in seventeen thirty six | 34 | yes (1736, impossible) |
| Each land mass becomes a point and each bridge a line segment | 35–37 | yes |
| The number of lines at a point is its degree; a point with no lines is isolated | 90–93 | yes ("edge incident on u and v" -> lines at a point; degree 0 = isolated) |
| A walk that uses every edge exactly once is an Eulerian walk; if it is closed it is an Eulerian tour | 175–179 | yes (each edge exactly once; closed = ends at its starting point) |
| Theorem 10.1: an undirected graph has an Eulerian tour iff it is even degree and connected (except possibly for isolated vertices) | 180–183 | yes: both conditions, including the isolated-vertex exception |
| The pen must enter each point as many times as it exits it, so the number of lines at it must be even | 39–41 | yes (the notes' impossibility argument) |
| The two-triangle example, its six lines, its degrees and its tour | own memory | not in the notes: invented here as the "yes" example, because the notes give no worked Eulerian-tour example. Every number in it is asserted in FACTS. |
| "the same test decides both puzzles" | own memory | a summary sentence, no new fact |
| Königsberg's four degrees are 3, 5, 3, 3 | 41–42 (notes: "each point has an odd number of line segments"), 53 (the edge multiset) | yes, recomputed from E |

## Gate

- [x] The first row of scene 1 shows one concrete case with real numbers (Königsberg, four lands, seven bridges).
- [x] Every "uses" cell names an earlier row or the screen (checked row by row above).
- [x] Every name and formula comes after the row where the viewer sees it happen: "degree" is named in 2.6, after the counts appear in 2.4/2.5; "Eulerian walk/tour" in 4.1, after the walk of scene 1; the theorem in 4.4, after the even degrees of 4.3.
- [x] The last scene answers the question at the top: the tour exists here (4.6–4.8) and the two conditions are stated (4.4–4.5).
- [x] Every row of "Stated facts" has a notes line number or the mark "own memory".
- [x] Every scene's picture cell names drawn objects (circles, lines, arcs, a moving dot, short labels), not sentences on the screen.

## Coverage

Every item of the notes.

| Notes item | Scene · row | or left out, because |
|---|---|---|
| §1 abstraction: internet, brain, maps, social networks as graphs (9–15) | — | left out: later episode (the notes' introduction; the episode opens on the concrete city) |
| §1 The seven bridges, the evening walk, return to the start (16–21) | 1.1, 1.2 | |
| Euler 1736, proved impossible (34) | 1.7 | |
| The city replaced by points and line segments (35–37) | 2.1, 2.2 | |
| Restatement as tracing without lifting the pen, no segment twice (37–39) | 3.1, 3.2 | |
| The interleaving proof: enter as often as you exit, so the count is even (39–41) | 3.4, 3.5 | |
| "each point has an odd number of segments, so impossible" (41–43) | 3.6, 3.7 | |
| Euler gave a precise condition (42–43) | 3.8, 4.4 | |
| §1.1 Formal definition of a graph G = (V, E), V and E (51–53) | 2.1–2.3 | |
| E is a multiset here (two bridges between a pair) (53–54) | 1.2 | |
| "we require E to be a set, not a multi-set" unless stated (55–57) | — | left out: later episode (a convention of the later formal sections) |
| Directed graphs, E ⊆ V × V, one-way streets (58–62) | — | left out: later episode |
| Directed vs undirected, dropping the arrows (75–82) | — | left out: later episode |
| G = (V, E) as an ordered pair (81–82) | — | left out: later episode |
| Concept check: V and E of G2 (83) | — | left out: later episode (exercise, not part of this episode's story) |
| Social-network example: recognizes / know each other (84–89) | — | left out: later episode |
| Incident, neighbours/adjacent (90–91) | 2.6 (as "lines at a point is its degree") | partially: the words "incident" and "neighbours" are not said; left out: later episode |
| Degree of a vertex, degree(u) = \|{v : {u,v} ∈ E}\| (91–92) | 2.4–2.6 | |
| Isolated vertex (93) | 2.6, 4.5, 4.7 | |
| In-degree and out-degree (101–103) | — | left out: later episode |
| Self-loops excluded in these notes (106–109) | — | left out: later episode |
| Paths (111–112) | — | left out: later episode |
| G3 housing example, shortest/longest path (113–121) | — | left out: later episode |
| Path is simple in this class (122–124) | — | left out: later episode |
| Cycles (124–126) | — | left out: later episode |
| Walk = sequence of edges, vertices may repeat (128–130) | 4.1 (the word "walk" is used from 1.3 on and named in 4.1) | |
| Tour = walk that starts and ends at the same vertex (130–131) | 1.2, 4.1 | |
| Summary table walk/path/tour/cycle (137–151) | — | left out: later episode (needs path and cycle first) |
| Remark on the subtleties of the definitions (152–153) | — | left out: later episode |
| Connectivity: path between any two distinct vertices (154–158) | 4.4, 4.5 | |
| Disconnected example (158–165) | — | left out: later episode |
| Connected components V1, V2, V3 (168–171) | — | left out: later episode |
| §2 Is there a walk using each edge exactly once? (174–176) | 1.2, 3.1, 4.1 | |
| Eulerian walk (176–178) | 4.1 | |
| Eulerian tour = closed Eulerian walk (178–179) | 4.1 | |
| Even degree graph (180–181) | 4.3, 4.4 | |
| Theorem 10.1 (182–183) | 4.4, 4.5 | |
| "Proof in the homework" (184) | — | left out: it is not in the notes |
| Concept check: why does Theorem 10.1 answer no for Königsberg (190) | end card, 3.6, 3.7 | |
| §3 Complete graphs, K_n, degree n−1, n(n−1)/2 edges, K5 (196–217) | — | left out: later episode |
| §3.2 Trees, four equivalent definitions, n−1 edges (219–226) | — | left out: later episode |
| Rooted trees, root, leaves, internal nodes, depth, levels (259–265) | — | left out: later episode |
| Bacterial division, binary search trees (269–273) | — | left out: later episode |
| Theorem 10.2 and its induction proof (282–306) | — | left out: later episode |
| §4 Planar graphs, faces, Euler's formula v + f = e + 2 (308–340) | — | left out: later episode |
| Exercise: planar graphs generalize polyhedra (341–342) | — | left out: later episode |
| Theorem 10.3, Euler's formula and its proof (348–355) | — | left out: later episode |
| Exercise: non-connected graphs and components in the formula (356–357) | — | left out: later episode |
| Face sides s_i, sum s_i = 2e, bridges (358–363) | — | left out: later episode |
| K3,3 bipartite, e ≤ 2v − 4 (364–384) | — | left out: later episode |
| Theorem 10.4 Kuratowski, contains K5 or K3,3 (385–404) | — | left out: later episode |
| §5 Connectivity and hypercubes, router networks, robustness (411–440) | — | left out: later episode |
| Exercise: minimum edges to disconnect K_n (429) | — | left out: later episode |
| Hypercubes, 2^n vertices, diameter n, E(n) = n 2^(n−1) (440–500) | — | left out: later episode |
| Theorem 10.5, crossing edges in the hypercube and its induction (503–546) | — | left out: later episode |
| §6 Practice problems, de Bruijn sequence (547–610) | — | left out: later episode |
