# PLAN: Hypercubes (episode 5)

Source: cs70/note10-deepseek/notes.txt lines 411-546 (section 5)  ·  Language: en

- **The question** the viewer cannot answer before and can after: how can a network of a million processors give each one only twenty neighbours, and why is it still hard to cut apart?
- **The worked example**, with its numbers (the names in the FACTS block): the 3-cube, 8 corners named by 3 bits, 12 edges (EDGES3), degree 3, 12 = 4 + 4 + 4; S = one corner (3 cut edges), S = front face (4 cut edges), case-2 set S = {000,001,010,100} (bounds 1 + 1 + 2 = 4).
- **The surprise**: a million processors would need about half a trillion wires if every pair were joined (the notes say 10^12), yet twenty neighbours each is enough.

## Scenes

| # | Method name | The picture: what is built, what changes | Ends when the viewer has seen |
|---|---|---|---|
| 1 | `the_cube` | 8 circles named by bits, then 12 edges drawn, one edge highlighted, panel of short labels | the direct definition, 2^n corners, 20 neighbours |
| 2 | `subcubes` | the same cube tinted: front square blue, back square orange, 4 green joining edges, 12 = 4+4+4 | the recursive definition |
| 3 | `counting_edges` | the cube with one corner's 3 edges highlighted, panel of sums; then the recurrence table 1, 4, 12, 32 | Lemma 10.1 by both proofs and the idea of the induction |
| 4 | `cutting_apart` | the cube with a chosen set filled yellow and its leaving edges red (1 corner, then the front square) | Theorem 10.5 statement |
| 5 | `induction` | tiny 1-cube, then the 3-cube with S0, S1 and the counted edges coloured, panel of bounds | both cases of the induction step |

## Chain table, one per scene

### Scene 1: `the_cube`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 1.1 | a cube with eight corners, each named by three bits; 000 front left, 010 above it | screen | eight circles with bit names appear |
| 1.2 | two corners are joined exactly when names differ in one bit; 000 and 001 are neighbours; twelve edges | 1.1 | twelve edges drawn, one highlighted |
| 1.3 | 000 and 011 differ in two bits, no edge; every corner has three neighbours | 1.2 | circles indicated |
| 1.4 | n bits give 2^n corners and n neighbours; the Connection Machine, twenty bits, about a million processors | 1.3 | panel lines |

### Scene 2: `subcubes`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 2.1 | corners starting with zero form the front square, the zero-subcube | screen | front square tinted blue |
| 2.2 | corners starting with one form the back square | 2.1 | back square tinted orange |
| 2.3 | four edges join each front corner to the corner behind | 2.2 | four joining edges green |
| 2.4 | second definition; twelve = twice four plus four | 2.3 | panel line |

### Scene 3: `counting_edges`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 3.1 | Lemma 10.1, n times 2^(n-1); two proofs | screen | formula under the cube |
| 3.2 | proof 1: every corner has n neighbours, three in the cube | 3.1 | corner 000 and its edges indicated |
| 3.3 | each edge counted twice, 8 times 3 is 24, half is 12 | 3.2 | panel sums |
| 3.4 | proof 2: recurrence E(n) = 2E(n-1) + 2^(n-1) | 3.3 | panel replaced by recurrence |
| 3.5 | 1, 4, 12, 32 matches 4 times 2^3 | 3.4 | table lines |
| 3.6 | induction idea: (n-1)2^(n-1) + 2^(n-1) = n 2^(n-1) | 3.5 | line of algebra |

### Scene 4: `cutting_apart`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 4.1 | cut one corner away: three edges | screen | corner 000 filled, 3 edges red |
| 4.2 | cut the front square away: four edges, equal to its corners | 4.1 | square filled, 4 joining edges red |
| 4.3 | Theorem 10.5 with its condition on |S| | 4.1, 4.2 | two panel lines |

### Scene 5: `induction`

| Row | What the sentence says | Uses | What happens on screen as it is said |
|---|---|---|---|
| 5.1 | base case: one bit, two corners, one edge | screen | tiny 1-cube |
| 5.2 | step: split S into S0, S1; two cases | 5.1 | S filled on the cube |
| 5.3 | case 1: hypothesis in each subcube, 2 + 2 = 4 | 5.2 | four edges red, panel |
| 5.4 | case 2 set-up: S0 has three corners, S1 one, S1 gives 1 | 5.2 | new S, one edge |
| 5.5 | complement of S0 inside the front: one corner, gives 1 | 5.4 | corner 011 indicated, edge red |
| 5.6 | joining edges: at least 3 - 1 = 2; total 4 = 2^k >= |S| | 5.5 | two joining edges red, panel total |

## Stated facts

| The fact, as it will be said | Notes line number, or "own memory" | All conditions kept? |
|---|---|---|
| vertices are the n-bit strings; edge when the strings differ in exactly one bit position | 451-456 | yes |
| 000 and 100 neighbours, 000 and 011 not | 455-456 (notes use 0000 / 1000 / 0011; I use 3 bits) | yes |
| recursive definition: 0-subcube, 1-subcube, edge between 0x and 1x | 473-478 | yes |
| Connection Machine, Thinking Machines, 1980s, a million processors, 20-dimensional hypercube, 20 neighbours | 441-449 | yes |
| complete graph on a million processors needs a huge number of wires (notes: 10^12; I compute about half a trillion) | 446 | differs, see report |
| Lemma 10.1: n 2^(n-1) edges | 491 | yes |
| Proof 1: degree n, each edge counted twice, n 2^n / 2 | 492-493 | yes |
| Proof 2: E(n) = 2E(n-1) + 2^(n-1), E(1) = 1, induction | 494-497 | yes |
| Theorem 10.5: |S| <= |V-S| (i.e. <= 2^(n-1)), E_S = edges between S and V-S, |E_S| >= |S| | 503-507 | yes |
| induction on n; base n = 1; step n = k+1, |S| <= 2^k, S0 and S1, S0 at least as large as S1 | 508-522 | yes |
| case 1: both <= 2^(k-1), hypothesis in each subcube, at least |S0| + |S1| | 523-528 | yes |
| case 2: |S0| > 2^(k-1); |S1| <= 2^(k-1); complement V0 - S0 small; at least 2^k - |S0|; joining edges at least |S0| - |S1|; total 2^k >= |S| | 529-545 | yes |

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
| connectivity motivation, trees, redundancy (lines 413-423) | not shown | belongs to episode 3 (trees) |
| complete graph, exercise on edges to remove from Kn | 1.4 (only the wire count) | the exercise is not worked: it is an exercise |
| diameter | not shown | only mentioned in notes; episode keeps to edges and cuts |
| Connection Machine | 1.4 | |
| definition 1, with 1-, 2-, 3-cubes | 1.1-1.3 | the 1- and 2-cubes appear as the tiny cube (5.1) and the front square (2.1) |
| definition 2, 0- and 1-subcubes | 2.1-2.4 | |
| Concept check (where are the subcubes, draw the 4-cube) | 2.1-2.3 | the 4-cube is not drawn |
| Exercise 2^n vertices and diameter n | 1.4 says 2^n corners | diameter exercise left out |
| Lemma 10.1, proof 1 | 3.2-3.3 | |
| Lemma 10.1, proof 2 and its induction exercise | 3.4-3.6 | idea only, as asked |
| Theorem 10.5 statement | 4.1-4.3 | |
| Theorem 10.5 base case | 5.1 | |
| Theorem 10.5 step, case 1 | 5.2-5.3 | |
| Theorem 10.5 step, case 2 | 5.4-5.6 | |
