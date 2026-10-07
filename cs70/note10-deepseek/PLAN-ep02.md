# PLAN: The Language of Graphs

Source: cs70/note10-deepseek/notes.txt, lines 48 to 181  ·  Language: en

- **The question** the viewer cannot answer before and can after: what exactly is a graph, and what do the words vertex, edge, degree, path, walk, cycle, tour and connected mean?
- **The worked example**, with its numbers (names in the FACTS block): the Königsberg multiset (BRIDGES, 7 bridges, 5 distinct pairs), the directed graph G1 (E1, 3 arrows), the undirected graph G2 (E2, 5 edges, DEG2), the neighbourhood G3 (E3, 5 roads, paths of length 2 and 3), the network G4 (two triangles and one isolated vertex, 3 components).
- **The surprise**: E of Königsberg is not a set, it is a multiset, and one extra, one-way arrow already changes what "degree" means; a graph with all degrees even can still have no Eulerian tour.

Figures did not survive the text extraction, so G2, G3 and G4 are rebuilt from the text (G1 is given by its E in line 62). See "Own reconstruction" below.

## Scenes

| # | Method name | The picture: what is built, what changes | Ends when the viewer has seen |
|---|---|---|---|
| 1 | `vertices_edges` | the four lands and seven bridges as a graph with circles and bent parallel edges; V and E written beside it; the two doubled bridges disappear | five edges, E a plain set |
| 2 | `directed_and_undirected` | G1 with three arrows, G2 with five plain edges, each with its V and E | G = (V, E) for both kinds |
| 3 | `neighbours_and_degree` | marks of degree beside every vertex of G2; an isolated vertex; a red loop; in and out labels on G1 | degree, isolated, self-loop, in-degree, out-degree |
| 4 | `walks_and_paths` | house graph G3, a dot that drives a path, a longer path, a cycle, a walk, a tour; a matrix of dots | the four words side by side |
| 5 | `connectivity` | G3 again, then G4 with three framed components, degrees on every vertex | connected, components, Theorem 10.1 with both conditions |

## Chain table, one per scene

### Scene 1: `vertices_edges`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 1.1 | the picture of four lands joined by seven bridges gets proper names | screen | four circles with letters, seven edges appear |
| 1.2 | the four lands are the vertices, a set V | 1.1 | circles flash, V = {A,B,C,D} appears |
| 1.3 | the seven bridges are the edges, a set E | 1.1 | edges flash, E written as seven pairs |
| 1.4 | two pairs appear twice, two bridges join the same lands | 1.3 | four arcs flash |
| 1.5 | so E is a multiset | 1.4 | E text flashes |
| 1.6 | we forbid this, E is a plain set, the copies vanish | 1.5 | two arcs fade, E text becomes five pairs |
| 1.7 | between two vertices no edge or exactly one | 1.6 | the five edges flash |

### Scene 2: `directed_and_undirected`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 2.1 | some relationships go one way, like a one-way street | screen | graph G1 on four vertices appears with arrows |
| 2.2 | a directed graph has edges that are ordered pairs; E holds three | 2.1 | V and E (three pairs) are written below G1 |
| 2.3 | E is a subset of V times V | 2.2 | E text flashes |
| 2.4 | order matters: (1,2) is an edge, (2,1) is not | 2.2 | first arrow flashes, red label "(2,1) is not in E" |
| 2.5 | when every edge works both ways the graph is undirected | 2.4 | G2 appears with five plain edges |
| 2.6 | drop arrowheads, write each edge as a two-member set | 2.5 | plain edges flash, V and E of G2 written |
| 2.7 | in both cases G = (V, E); G2 has five vertices and five edges | 2.6 | G = (V, E) top right, vertices then edges flash |

### Scene 3: `neighbours_and_degree`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 3.1 | look at vertex three of G2 | screen | vertex 3 flashes |
| 3.2 | its three edges are incident on it; the other ends are its neighbours | 3.1 | three edges flash, then vertices 1, 2, 4 |
| 3.3 | degree is the number of incident edges; vertex three has three | 3.2 | mark 3 appears next to vertex 3 |
| 3.4 | vertices one, two, four have degree two, vertex five degree one | 3.3 | marks appear |
| 3.5 | add a lonely sixth vertex, degree zero | 3.4 | grey vertex with mark 0 appears |
| 3.6 | isolated: no edge connects it to the rest | 3.5 | vertex flashes |
| 3.7 | no self-loops | 3.6 | red loop at vertex 2 appears |
| 3.8 | a directed graph has in and out, arrows come in or leave | screen | arrows of G1 flash |
| 3.9 | in-degree counts arriving, out-degree counts leaving | 3.8 | arrows flash |
| 3.10 | vertex one: out three, in zero; the other three: in one, out zero | 3.9 | labels appear at vertex 1, then at the other three |

### Scene 4: `walks_and_paths`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 4.1 | a neighbourhood: vertices are houses, edges are roads | screen | four houses appear |
| 4.2 | the five roads | 4.1 | five edges appear |
| 4.3 | to drive from two to four is a job for a path | 4.2 | dot appears at house two |
| 4.4 | a path never visits a house twice | 4.3 | (the dot rests) |
| 4.5 | two, one, four is a shortest path with two edges | 4.4 | dot drives, edges turn yellow |
| 4.6 | longest path: two, three, one, four, three edges | 4.5 | second dot drives, edges turn green |
| 4.7 | cycle: path plus an edge back | 4.6 | (colors reset) |
| 4.8 | examples: one, two, three, one and one, three, four, one | 4.7 | dot drives each triangle |
| 4.9 | a stroll two, one, two, three, four is a walk; may repeat | 4.8 | dot walks, edges turn purple |
| 4.10 | a tour is a walk that ends where it started, one visited twice | 4.9 | dot drives the tour, edges orange |
| 4.11 | path: no repeated vertices; tour: closed; cycle: both; walk: none | 4.10 | matrix with dots appears |

### Scene 5: `connectivity`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 5.1 | connected: a path between any two distinct vertices | screen | houses two and four flash |
| 5.2 | the neighbourhood is connected | 5.1 | whole graph flashes |
| 5.3 | seven houses, no road between triangles and the lonely house | screen | G4 appears |
| 5.4 | so it falls apart into three connected components | 5.3 | three frames appear |
| 5.5 | the sets V1, V2, V3 | 5.4 | labels appear |
| 5.6 | Eulerian walk and tour defined | 5.1 | edges flash |
| 5.7 | the theorem: every degree even and connected, ignoring isolated | 5.6 | degree marks appear, vertex four flashes |
| 5.8 | here all degrees are even and still no tour | 5.7 | marks flash |
| 5.9 | a tour in the left triangle never reaches the right one | 5.8 | dot circles the left triangle, right flashes red |
| 5.10 | the theorem needs both conditions | 5.9 | whole graph flashes |

## Stated facts

| The fact, as it will be said | Notes line number, or "own memory" | All conditions kept? |
|---|---|---|
| A graph is a set of vertices V and a set of edges E | 51-53 | yes |
| Königsberg: V = {A,B,C,D} and E has seven pairs, two of them twice (multiset) | 53-55 | yes |
| We generally require E to be a set; between two vertices 0 or 1 edge | 55-57 | yes ("generally", "unless stated otherwise") |
| Directed graph: E is a subset of V x V; ordered pairs | 59-60 | yes |
| V = {1,2,3,4}, E = {(1,2),(1,3),(1,4)}; (1,2) in E but (2,1) not | 62, 75-76 | yes |
| Undirected: edge is the set {u,v}; arrowheads omitted | 78-81 | yes |
| G = (V, E) | 82 | yes |
| An edge is incident on its two vertices, which are neighbours or adjacent | 90-91 | yes |
| Degree of a vertex = number of edges incident on it; degree 0 is isolated | 91-93 | yes (undirected) |
| In-degree and out-degree for directed graphs | 101-103 | yes |
| No self-loops in these notes | 106-108 | yes ("unless stated otherwise") |
| A path is a sequence of edges between v1 and vn; simple (distinct vertices) | 111-112, 122 | yes |
| A cycle is a path plus the edge back to v1 | 124-126 | yes |
| A walk is a sequence of edges with possibly repeated vertices | 128-130 | yes |
| A tour is a walk that starts and ends at the same vertex | 130-131 | yes |
| Connected: a path between any two distinct vertices | 155-156 | yes |
| Connected components V1..Vk; three for the seven-vertex example | 168-170 | yes |
| Eulerian walk uses each edge exactly once; Eulerian tour is a closed one | 175-178 | yes |
| Theorem 10.1: Eulerian tour iff even degree and connected (except possibly isolated vertices) | 182-183 | yes |
| "Even degree and still no tour for two separate triangles" | own reasoning (follows from Theorem 10.1) | derived, not in the notes |

## Own reconstruction (figures lost in extraction)

- G2 (undirected, five vertices): edges {1,2},{1,3},{2,3},{3,4},{4,5}. The notes' G2 edges are not in the text.
- G3 (houses): edges {1,2},{1,3},{1,4},{2,3},{3,4}; chosen so that every walk and tour of the text (lines 128-131) is legal.
- G4 (seven vertices, three components): triangle on 1,2,3, vertex 4 alone, triangle on 5,6,7. The notes give only the components (line 170).
- The isolated sixth vertex of scene 3 and the sample graphs are mine.

## Gate

- [x] The first row of scene 1 shows one concrete case with real numbers (four lands, seven bridges).
- [x] Every "uses" cell names an earlier row or the screen.
- [x] Every name and formula comes after the row where the viewer sees it happen.
- [x] The last scene answers the question at the top.
- [x] Every row of "Stated facts" has a notes line number or the mark "own memory" ("own reasoning" for one derived row).
- [x] Every scene's picture cell names a drawn object, not sentences on the screen.

## Coverage

| Notes item | Scene · row | or left out, because |
|---|---|---|
| Formal graph: V and E, edges as line segments (51-53) | 1.1-1.3 | |
| Königsberg V and E, multiset (53-55) | 1.3-1.5 | |
| E a set, 0 or 1 edge (55-57) | 1.6-1.7 | |
| Directed graph, one-way street, E subset of V x V (58-62) | 2.1-2.3 | |
| Example G1 and (1,2) in E, (2,1) not (62, 75-76) | 2.2, 2.4 | |
| Undirected graph, {u,v}, two-way street, G2 (77-81) | 2.5-2.6 | |
| G = (V,E) (81-82) | 2.7 | |
| Concept check: V and E for G2 | 2.6 | answered on screen, without a pause |
| Social network: recognizes vs know each other (84-89) | | out of scope for this episode: an application, not a definition; the distinction directed/undirected is shown by one-way and two-way streets |
| Incident, neighbours, adjacent (90-91) | 3.2 | |
| Degree, isolated vertex (91-93) | 3.3-3.6 | |
| Concept checks on degree/isolated in the social network (99-100, 104-105) | | left out: same reason as the social network |
| In-degree and out-degree (101-103) | 3.8-3.10 | |
| Self-loops (106-108) | 3.7 | |
| Path, simple path (110-112, 122-124) | 4.3-4.6 | |
| Concept check: shortest and longest path from 2 to 4 | 4.5-4.6 | answered in the narration |
| Cycle (124-126) and its concept check | 4.7-4.8 | answered in the narration |
| Walk and tour (127-131) | 4.9-4.10 | |
| Summary table of terms (133-148) | 4.11 | as a matrix of dots from the text of the definitions |
| Remark on subtleties (149-151) | | left out: remark, no content |
| Connected (155-157) | 5.1-5.2 | |
| Disconnected network and components V1,V2,V3 (158-170) | 5.3-5.5 | |
| Concept check on a disconnected vertex (166-167) | | left out: an application question |
| Eulerian walk and tour (175-179) | 5.6 | |
| Theorem 10.1 (180-183) | 5.7-5.10 | proof is in the homework (line 184) and is not part of this episode |
