# PLAN: Complete Graphs and Trees

Source: cs70/note10-deepseek/notes.txt, lines 189-306 (section 3)  ·  Language: en

- **The question**: a graph can have the most edges, or just enough edges to stay connected; how many edges is each, and why do "connected with no cycles" and "connected with n minus one edges" mean the same thing?
- **The worked example**, with its numbers (names in FACTS): K2, K3, K4, K5 with one, three, six, ten edges; a tree on six vertices with five edges (and 6^4 = 1296 trees on six vertices); a rooted tree of fifteen nodes, depth three, levels of one, two, four, eight nodes.
- **The surprise**: counting edges of K5 by hand is slow, but each vertex has degree n minus one and every edge is counted from both ends; and the tree on six vertices has exactly five edges, never six, because a sixth would close a cycle.

## Scenes

| # | Method name | The picture: what is built, what changes | Ends when the viewer has seen |
|---|---|---|---|
| 1 | `complete_graphs` | K2, K3, K4, K5 drawn as vertices on a polygon with every pair joined; edge counts under each; one K5 vertex highlighted with its four edges | the formula n(n-1)/2 checked on K5 |
| 2 | `what_is_a_tree` | a six-vertex tree and a graph with a cycle; the tree is cut at one edge (two pieces), and gets one edge added (a cycle); four definition boxes build up | all four definitions and the count 6^4 |
| 3 | `rooted_trees` | the fifteen-node binary rooted tree built level by level; root, internal nodes, leaves coloured; the longest path highlighted; level numbers | depth three, levels, why trees are useful |
| 4 | `theorem_proof` | two boxes joined by a double arrow (the theorem); a tree with a vertex removed and added back; a graph with a cycle that loses a cycle edge | both directions of the proof idea |

## Chain table, one per scene

### Scene 1: `complete_graphs`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 1.1 | complete graph: every pair of distinct vertices joined by an edge; K2, K3, K4 | screen | K2, K3, K4 drawn |
| 1.2 | maximum number of edges possible; K_n unique; K5 has ten edges | 1.1 | K5 drawn, counts 1, 3, 6, 10 appear |
| 1.3 | each vertex of K5 has degree four, n minus one in general | 1.2 | one vertex and its four edges highlighted |
| 1.4 | n vertices times n minus one, every edge counted twice, so n(n-1)/2; K5 gives ten | 1.3 | formula appears, check line |

### Scene 2: `what_is_a_tree`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 2.1 | a tree is connected with no cycles; the second graph has a cycle so is not a tree | screen | tree and cycle graph drawn, cycle red |
| 2.2 | the tree has six vertices and five edges; connected with n minus one edges | 2.1 | counters 6 and 5, definition box 2 |
| 2.3 | remove any edge, the tree falls into two pieces | 2.1 | one edge removed, two colours |
| 2.4 | add any edge, a cycle appears | 2.1 | dashed edge, triangle red |
| 2.5 | many trees (n^(n-2), 1296 for six), only one complete graph | 2.2 | counts |

### Scene 3: `rooted_trees`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 3.1 | rooted tree: a root on top, leaves at the bottom, internal nodes between | screen | tree built, coloured |
| 3.2 | a root is never a leaf; unrooted tree leaf is degree one | 3.1 | root degree label |
| 3.3 | depth is the longest path root to leaf, three; level k is k edges away | 3.1 | path highlight, level labels |
| 3.4 | uses: bacteria divide in two; binary search trees; hard problems like Maximum Cut easy on trees | 3.3 | level sizes 1, 2, 4, 8 |

### Scene 4: `theorem_proof`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 4.1 | Theorem 10.2: the two statements are equivalent; two directions | screen | two boxes with double arrow |
| 4.2 | forward: strong induction on n; base case one vertex, no edges | 4.1 | single vertex |
| 4.3 | inductive step: remove a vertex v; G prime has no cycles; case G prime connected | 4.2 | tree of six, v removed |
| 4.4 | hypothesis: G prime has k minus one edges; adding v with two edges would make a cycle, so exactly one: k edges | 4.3 | v returns, a second dashed edge makes a cycle |
| 4.5 | converse: by contradiction, a cycle; removing a cycle edge keeps G connected with n minus two edges | 4.1 | graph with a cycle, edge removed |
| 4.6 | but connected needs at least n minus one edges, a fact left as an exercise; contradiction | 4.5 | counters clash |

## Stated facts

| The fact, as it will be said | Notes line number, or "own memory" | All conditions kept? |
|---|---|---|
| In a complete graph every pair of distinct vertices is joined by an edge | 197-201 | yes |
| K_n is the unique complete graph on n vertices | 204 | yes |
| K_n has n(n-1)/2 edges | 214 | yes |
| Every vertex of K_n has degree n-1 | 211-212 (concept check, answer not given); derived from definition | yes, derived |
| A tree is a connected graph with no cycles | 220 | yes |
| Equivalent: connected with n-1 edges; removing any edge disconnects; no cycles and adding any edge creates a cycle | 222-228 | yes |
| n^(n-2) trees on n vertices | 235 | yes |
| Hard problems such as Maximum Cut are easy on trees | 237-239 | yes |
| Rooted tree: root on top, leaves bottom-most, internal nodes between; a root is never a leaf; in an unrooted tree a leaf is a vertex of degree 1 | 258-262 | yes |
| Depth is the length of the longest path from root to a leaf; level k is the vertices at exactly k edges from the root | 262-265 | yes |
| Bacterial cell division, binary search trees | 269-272 | yes |
| Theorem 10.2 and the two directions | 282-285 | yes |
| Forward: strong induction on n; base n=1; remove a vertex; two cases, we show G' connected, the other is an exercise | 285-296 | yes |
| Converse: contradiction; removing a cycle edge leaves G connected with n-2 edges; a connected graph needs at least n-1 edges (exercise) | 300-306 | yes |
| Complete directed graphs | 216-217 | left out, see coverage |
| Notes figure of the rooted tree is rebuilt as a complete binary tree of 15 nodes | figure lost; consistent with "depth 3" at line 267 | own rebuild |

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
| Complete graphs, K2 K3 K4 (197-203) | 1.1 | |
| K_n formal definition (205-206) | 1.1 | only said in words, the set notation is not shown |
| Concept check: draw K5 | 1.2 | |
| Concept check: degree of every vertex in K_n | 1.3 | |
| Exercise: edges in K_n, check K5 | 1.4 | |
| Complete directed graphs (216-217) | | left out: one sentence in the notes, not used by the rest of the series |
| Complete graphs are maximal among connected graphs (190-191) | 1.2 | |
| Tree definition, four equivalent definitions (220-228) | 2.1-2.4 | |
| Three tree examples (229-230) | 2.1 | one example drawn, figure lost |
| Concept check: examples satisfy all four; give a non-tree (232-234) | 2.1-2.4 | |
| n^(n-2) trees, in contrast to unique K_n (235-236) | 2.5 | |
| Why trees matter: Maximum Cut (237-239) | 3.4 | |
| Rooted tree, root, leaves, internal nodes (240-262) | 3.1, 3.2 | |
| Depth and levels (262-265) | 3.3 | |
| Concept check: depth 3, level 0 and 3 (266-268) | 3.3 | |
| Bacterial division, binary search trees (269-272) | 3.4 | |
| Theorem 10.2 statement (282) | 4.1 | |
| Forward direction: base, hypothesis, step (285-296) | 4.2-4.4 | |
| G' disconnected case (292-293) | | left out: the notes leave it as an exercise |
| Converse direction (300-306) | 4.5, 4.6 | |
| Fact: connected needs n-1 edges (305-306) | 4.6 | stated, proof left as exercise as in the notes |
