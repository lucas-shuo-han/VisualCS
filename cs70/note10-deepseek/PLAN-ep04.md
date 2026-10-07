# PLAN: Planar Graphs and Euler's Formula

Source: cs70/note10-deepseek/notes.txt, section 4 (lines 307-410)  ·  Language: en

- **The question** the viewer cannot answer before and can after: why can K5 and K3,3 not be drawn on the plane without crossings, and what does that have to do with the count of vertices, edges and faces?
- **The worked example**, with its numbers (FACTS names K4, CUBE, K5, K33): K4 has 4 vertices, 6 edges, 4 faces (4+4 = 6+2); the cube has 8, 12, 6; K5 has 5 vertices and 10 edges against the bound 9; K3,3 has 6 vertices and 9 edges against bounds 12 and 8.
- **The surprise**: a drawing with a crossing does not make a graph non-planar (K4 redrawn), and K3,3 passes the first test (9 <= 12) but still fails the sharper one (9 > 8).

## Scenes

| # | Method name | The picture: what is built, what changes | Ends when the viewer has seen |
|---|---|---|---|
| 1 | `planar_and_faces` | K4 drawn as a square with two crossing diagonals, then redrawn as a triangle with a centre vertex; face numbers; the cube as square in square | that v + f = e + 2 holds for K4 and the cube |
| 2 | `euler_induction` | the planar K4 loses cycle edges one at a time, merged faces tinted, a counter row v + f = e + 2 updated; a single dot as base case | the formula survives each deletion and ends on a tree |
| 3 | `edge_bound` | planar K4 with the side count 3 in every face; chain of inequalities; a bar from 999 to 499500 with a short highlighted piece | e <= 3v - 6 and what it means for a 1000-vertex graph |
| 4 | `two_graphs` | K5 (pentagon plus star) and K3,3 (houses and wells) with their counts, a red dashed "no edge" between two houses | K5 and K3,3 are not planar |
| 5 | `kuratowski` | mini K5 and K3,3, then six blobs joined by nine edges that contract to K3,3 | Theorem 10.4 and what contains means |

## Chain table, one per scene

### Scene 1: `planar_and_faces`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 1.1 | a graph on 4 vertices, every vertex joined to every other, 6 edges; drawn as a square with both diagonals two edges cross | screen | square with two crossing diagonals appears |
| 1.2 | move one vertex into the middle: same 6 edges, no crossing | 1.1 | the drawing morphs to the triangle with centre |
| 1.3 | planar = can be drawn without crossings; the first drawing crossed but the graph is still planar | 1.2 | label "planar" |
| 1.4 | the edges cut the plane into faces: three inside triangles plus the infinite outer one, 4 faces | 1.2 | numbers 1 to 4 in the faces |
| 1.5 | v + f = 4 + 4 = 8 and e + 2 = 6 + 2 = 8 | 1.4 | the formula and the numbers under the graph |
| 1.6 | the cube drawn flat: 8, 12, 6 faces, 8 + 6 = 12 + 2 | 1.5 | cube appears, its numbers |
| 1.7 | the Greeks knew it for polyhedra but could not prove it: induction on a solid has no smaller solid; Euler generalised to planar graphs | 1.6 | cube highlighted |

### Scene 2: `euler_induction`

| Row | What the sentence says | Uses | What happens on screen |
|---|---|---|---|
| 2.1 | Theorem 10.3: connected planar graph satisfies the formula, proof by induction on edges | screen | formula label, K4 drawn with counter 4 + 4 = 6 + 2 |
| 2.2 | smallest case: one vertex, no edges, one face, 1 + 1 = 0 + 2 | 2.1 | a single dot with its counter at the side |
| 2.3 | graph with a cycle: delete one edge of the cycle; the two faces beside it merge, so edges and faces both drop by one | 2.1 | two inner triangles tinted, edge removed, counter 4 + 3 = 5 + 2 |
| 2.4 | the smaller graph obeys the formula by induction, so the larger does | 2.3 | counter indicated |
| 2.5 | repeat until no cycle is left | 2.3 | two more edges removed, counters 4 + 2 = 4 + 2, then 4 + 1 = 3 + 2 |
| 2.6 | a tree has one face and one edge fewer than vertices, so the formula holds | 2.5 | final tree, counter |

### Scene 3: `edge_bound`

| Row | What the sentence says | Uses | What happens on screen |
|---|---|---|---|
| 3.1 | count the sides of every face: 3 in each of the 4 faces, 12 in all | screen | K4 planar drawing, a 3 in each face, sum row |
| 3.2 | each edge has two sides, so the sum is twice the edges; 12 = 2 times 6 | 3.1 | sum row extended with 2e |
| 3.3 | no parallel edges and at least 3 vertices, so every face has at least 3 sides, so 3f <= 2e | 3.2 | inequality appears |
| 3.4 | put f from Euler's formula in: e <= 3v - 6 | 3.3 | algebra lines; K4: 3*4 - 6 = 6 |
| 3.5 | planar graphs are sparse: 1000 vertices connected, 999 to 499500 edges in general, at most 2994 if planar | 3.4 | bar with a small highlighted piece |

### Scene 4: `two_graphs`

| Row | What the sentence says | Uses | What happens on screen |
|---|---|---|---|
| 4.1 | K5: 5 vertices, 10 edges (each vertex 4 neighbours, 5 times 4 over 2) | screen | pentagon plus star |
| 4.2 | the bound allows 3*5 - 6 = 9, 10 is too many, K5 not planar | 4.1 | counts, red comparison |
| 4.3 | K3,3: three houses, three wells, each house joined to each well, 6 vertices, 9 edges | screen | K3,3 drawn |
| 4.4 | bound is 12, so it passes; sharper argument needed | 4.3 | counts, green comparison |
| 4.5 | a triangle would join two houses or two wells, but houses meet only wells | 4.3 | red dashed "no edge" between two houses |
| 4.6 | so every face has at least 4 sides, 4f <= 2e, e <= 2v - 4 = 8 < 9, so K3,3 is not planar | 4.5 | inequality lines |

### Scene 5: `kuratowski`

| Row | What the sentence says | Uses | What happens on screen |
|---|---|---|---|
| 5.1 | K5 and K3,3 are both non-planar and in some sense the only ones; Kuratowski (Polish mathematician); Theorem 10.4 | screen | mini K5 and K3,3 |
| 5.2 | contains = disjoint connected pieces, one per vertex, an edge between pieces where the small graph has an edge | 5.1 | six blobs and nine edges |
| 5.3 | squeeze each piece to one vertex and a copy appears | 5.2 | blobs contract to K3,3 |
| 5.4 | notes use it for the 4-cube; one direction obvious, the other hard, proof left out | 5.3 | blobs stay, the picture highlighted |

## Stated facts

| The fact, as it will be said | Notes line number, or "own memory" | All conditions kept? |
|---|---|---|
| a graph is planar if it can be drawn on the plane without crossings | 309-312 | yes |
| the same graph can have a drawing with crossings and still be planar | 310-312 | yes |
| K3,3 is the three houses, three wells graph; K5 complete graph on five nodes | 313-316 | yes |
| faces are the regions the plane is cut into, one infinite (outer), the rest finite | 331-332 | yes |
| cube has six faces | 333 | yes |
| Euler's formula v + f = e + 2 | 334 | yes |
| the Greeks knew it for polyhedra but could not prove it; the right generalisation is planar graphs | 335-340 | yes |
| Theorem 10.3: every connected planar graph satisfies v + f = e + 2; induction on e; base e = 0, v = f = 1 | 348-350 | yes |
| tree: f = 1, e = v - 1; with a cycle delete a cycle edge, e and f both drop by one | 351-355 | yes |
| sum of sides of faces = 2e | 358-364 | yes |
| no parallel edges and at least two edges (so at least three vertices): every face has at least three sides, so 3f <= 2e, so e <= 3v - 6 | 366-371 | yes |
| planar graphs are sparse; 1000 vertices: between 999 and 2994 edges for planar | 372-374 | yes |
| K5 has five vertices and ten edges, so not planar | 375 | yes |
| K3,3 has v = 6, e = 9, passes; no triangles; 4f <= 2e; e <= 2v - 4; non-planar | 376-382 | yes |
| Kuratowski, a Polish mathematician; Theorem 10.4: non-planar iff it contains K5 or K3,3 | 383-385 | yes |
| contains: disjoint connected subgraphs B_v, an edge between B_u and B_v for every edge uv; contract to get a copy | 386-395 | yes |
| the 4-cube is shown non-planar by containing K3,3 | 396-405 | yes |
| one direction obvious, the other difficult, proof not given | 407-410 | yes |
| "K" stands for Kuratowski | 384 | yes |

## Gate

- [x] The first row of scene 1 shows one concrete case with real numbers.
- [x] Every "uses" cell names an earlier row or the screen.
- [x] Every name and formula comes after the row where the viewer sees it happen.
- [x] The last scene answers the question at the top.
- [x] Every row of "Stated facts" has a notes line number or the mark "own memory".
- [x] Every scene's picture cell names a drawn object, not sentences on the screen.

## Coverage

| Notes item | Scene · row | or left out, because |
|---|---|---|
| definition of planar, example drawing with crossings | 1.1-1.3 | |
| K3,3, K5, 4-cube named as non-planar | 4, 5.4 | the three pictured graphs of the notes are rebuilt from the text |
| bipartite graphs, 4-cube is bipartite | | belongs to the hypercube episode (5); K3,3 is drawn as houses and wells instead |
| faces, v, e, f, outer face | 1.4 | |
| Euler's formula, cube, tetrahedron, octahedron checks | 1.5, 1.6 | tetrahedron is K4 (1.5); octahedron not drawn |
| history: Greeks, Euler, generalisation | 1.7 | |
| exercise: why planar graphs generalise polyhedra | | exercise, left to the reader |
| Theorem 10.3 and induction (base, tree, cycle) | 2.1-2.6 | |
| exercise: disconnected graphs and components | | exercise, left to the reader |
| sum of sides = 2e, bridges counted twice | 3.1-3.2 | bridge case not drawn (said only through "each edge has two sides") |
| 3f <= 2e, e <= 3v - 6 | 3.3-3.4 | |
| sparse planar graphs, 999 to 2994 | 3.5 | |
| K5 not planar | 4.1-4.2 | |
| K3,3 passes first test; no triangles; e <= 2v - 4; not planar | 4.3-4.6 | |
| Theorem 10.4 (Kuratowski) | 5.1 | |
| the definition of "contains" and contraction | 5.2-5.3 | |
| 4-cube contains K3,3 figure | 5.4 | only mentioned, the figure is not rebuilt (not in the text) |
| exercise: K5 in the 4-cube | | exercise, left to the reader |
| easy direction obvious, hard direction proof omitted | 5.4 | |
