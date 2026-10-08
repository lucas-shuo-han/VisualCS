# BOARD: episode 10, And the Candidates Lose

Source: `notes.txt` lines 438 to 474. Language: en. Aim: 4 to 5 minutes (about 620 words).
File `ep10_candidate_pessimal.py`, class `Ep10CandidatePessimal`. Scenes, in order: `hook`, `cleo`, `law`, `swap`.

The builder copies every narration line (the lines that start with a greater-than sign)
into a `say()` unchanged, one beat per `say()`, and builds exactly the stage described.
It decides nothing; an unclear line is a question in its report.

Format, read by `check.py`: a line that starts with three hash signs opens a beat, and
every line after it that starts with a greater-than sign is that beat's narration.
Neither is used anywhere else in this file.

## Facts

Candidates A, B, C, D of the notes are Ada, Bea, Cleo, Dora, as in episodes 8 and 9.
The job optimal matching (M of the notes) is shown in green, the other stable matching
(M') in purple; the voice says "the green matching", "the purple matching", and "her
green job" for the job a candidate has in the job optimal matching.

| id | Fact, with all its conditions | Notes line | Computed how |
|---|---|---|---|
| F1 | The lists. Job 1: Ada, Bea, Cleo, Dora. Job 2: Ada, Dora, Cleo, Bea. Job 3: Ada, Cleo, Bea, Dora. Job 4: Ada, Bea, Cleo, Dora. Ada: 1, 3, 2, 4. Bea: 4, 3, 2, 1. Cleo: 2, 3, 1, 4. Dora: 3, 4, 2, 1. | 337 to 380 | `JOBS`, `CANDS` below |
| F2 | The two stable matchings. Green (job optimal, the output of propose and reject): Job 1 with Ada, Job 2 with Dora, Job 3 with Cleo, Job 4 with Bea. Purple: Job 1 with Ada, Job 2 with Cleo, Job 3 with Dora, Job 4 with Bea. | 381 to 382, 418 | `STABLE == [M2, M1]` (episodes 8 and 9) |
| F3 | The pessimal job for a candidate is the lowest-ranked job on her list that she is paired with in any stable matching; a matching in which every candidate has her pessimal job is candidate pessimal. (The notes define the pessimal candidate for a job and leave this mirror definition to the reader.) | 413 to 415 | stated |
| F4 | Theorem 11.3: if a matching is job (employer) optimal, then it is also candidate pessimal. | 440 | here `PESS == {c: j for j, c in M1.items()}`; checked on all 46656 instances with three jobs and three candidates: `optimal_is_pessimal` |
| F5 | Proof of the notes. Let M be the job optimal matching, with (J, C) in it, and suppose J is not the pessimal job of C. Then there is a stable matching M' with (J*, C) and (J, C'), where J* is lower than J on C's list. C prefers J to J*. J prefers C to C', because C is its partner in the job optimal matching. So (J, C) is a rogue couple in M'. Contradiction. | 441 to 450 | stated |
| F6 | The optimal candidate of a job is the best partner it has in any stable matching, so no partner it has in a stable matching is above her. | 391 to 394 | episode 8 |
| F7 | Cleo's list is Job 2, Job 3, Job 1, Job 4; her green job is Job 3. Job 3's list is Ada, Cleo, Bea, Dora; its optimal candidate is Cleo. | from F1, F2 | `CANDS["Cleo"] == [2, 3, 1, 4] and M1[3] == "Cleo" and JOBS[3] == ["Ada", "Cleo", "Bea", "Dora"]` |
| F8 | Exercise of the notes: what change makes the algorithm output the candidate optimal matching? Answer worked out here: let the candidates propose and the jobs answer. On these lists: Ada asks Job 1, Bea asks Job 4, Cleo asks Job 2, Dora asks Job 3; no job gets two offers; it stops on day one with the purple matching. | 453 to 454 | `run(CANDS, JOBS)` has one day and gives `M2` |
| F9 | The National Residency Matching Program at first ran the algorithm with the hospitals proposing, so the matchings were hospital optimal. In the 1990s the roles were reversed, so that the students propose. Later enhancements include taking into account the preferences of married students for positions at the same or nearby hospitals. | 455 to 460 | stated |
| F10 | The algorithm was in use ten years before Gale and Shapley first analysed it properly in a 1962 paper: D. Gale and L. S. Shapley, "College Admissions and the Stability of Marriage", American Mathematical Monthly 69 (1962), pages 9 to 14. | 463 to 467 | `1962 - 1952 == 10` |

```python
from itertools import permutations, product
JOBS = {1: ["Ada", "Bea", "Cleo", "Dora"], 2: ["Ada", "Dora", "Cleo", "Bea"],
        3: ["Ada", "Cleo", "Bea", "Dora"], 4: ["Ada", "Bea", "Cleo", "Dora"]}
CANDS = {"Ada": [1, 3, 2, 4], "Bea": [4, 3, 2, 1], "Cleo": [2, 3, 1, 4], "Dora": [3, 4, 2, 1]}
M1 = {1: "Ada", 2: "Dora", 3: "Cleo", 4: "Bea"}     # green, job optimal
M2 = {1: "Ada", 2: "Cleo", 3: "Dora", 4: "Bea"}     # purple

def run(proposers, answerers):
    """Per day: offers proposer -> answerer. The last day is the result."""
    left = {p: list(l) for p, l in proposers.items()}
    days = []
    while True:
        offers = {p: left[p][0] for p in proposers}
        refused = []
        for a in answerers:
            got = [p for p in offers if offers[p] == a]
            if got:
                best = min(got, key=answerers[a].index)
                refused += [(p, a) for p in got if p != best]
        days.append(offers)
        if not refused:
            return days
        for p, a in refused:
            left[p].remove(a)

def stable_matchings(jobs, cands):
    out = []
    for p in permutations(cands):
        m = dict(zip(jobs, p)); has = {c: j for j, c in m.items()}
        if not any(cands[c].index(j) < cands[c].index(has[c])
                   for j in jobs for c in jobs[j][:jobs[j].index(m[j])]):
            out.append(m)
    return out

STABLE = stable_matchings(JOBS, CANDS)
assert STABLE == [M2, M1] and run(JOBS, CANDS)[-1] == M1
PESS = {c: max((j for m in STABLE for j in m if m[j] == c), key=CANDS[c].index) for c in CANDS}
assert PESS == {c: j for j, c in M1.items()}
assert CANDS["Cleo"] == [2, 3, 1, 4] and M1[3] == "Cleo" and JOBS[3] == ["Ada", "Cleo", "Bea", "Dora"]
swap = run(CANDS, JOBS)
assert len(swap) == 1 and swap[0] == {"Ada": 1, "Bea": 4, "Cleo": 2, "Dora": 3} == {c: j for j, c in M2.items()}
assert 1962 - 1952 == 10

nj, nc = [1, 2, 3], ["x", "y", "z"]
optimal_is_pessimal = True
for jl in product(permutations(nc), repeat=3):
    for cl in product(permutations(nj), repeat=3):
        jobs, cands = dict(zip(nj, map(list, jl))), dict(zip(nc, map(list, cl)))
        st, out = stable_matchings(jobs, cands), run(jobs, cands)[-1]
        pess = {c: max((j for m in st for j in m if m[j] == c), key=cands[c].index) for c in cands}
        optimal_is_pessimal = optimal_is_pessimal and pess == {c: j for j, c in out.items()}
assert optimal_is_pessimal
```

(The enumeration takes some seconds. The builder may keep it in a separate check and
assert only the lines before it in the episode file.)

## Added to the notes

| Beat | The step that was missing | Why it holds |
|---|---|---|
| 1.2 | The theorem seen on the example before it is stated: in the candidates' columns the green job is never above the purple one. | F2, the cells on screen. |
| 2.1 to 2.4 | The proof run with names (Cleo and Job 3) and list positions before the general version. | F7. |
| 2.1 | The definition of the pessimal job for a candidate, which the notes leave to the reader, and what "J is not the pessimal job of C" gives: a stable matching in which she has a job lower on her list. | F3. |
| 2.2 | Why the job has another partner in that matching, and why that partner is not above the candidate on the job's list. The notes say only "because C is its partner in the employer optimal matching". | She is with another job there, so her green job is with another candidate. That candidate is a partner of the job in a stable matching, and no such partner is above its optimal candidate (F6). |
| 2.3 | From "not above" to "below", which a rogue couple needs. | The other partner is not the candidate herself, and a list has no ties. |
| 3.1, 3.2 | The general version, with "her green job" for the notes' J and nothing else changed. | F5. |
| 4.1 | The answer to the exercise: let the candidates propose. Why the theorems carry over. | Episodes 5, 7 and 9 used only "one side proposes, the other answers"; exchanging the two names exchanges "job optimal" and "candidate optimal". |
| 4.2 | The run with the candidates proposing on the four-by-four lists. | F8, computed. |
| 4.4 | "In use for ten years before." | F10: 1962 minus 1952, the year from episode 2. |

## Left out, and why

| Item of the notes | Line | Reason |
|---|---|---|
| "We conclude that employers would fare very well... The following theorem confirms a sad truth" | 438 to 439 | Said by the opening question of beat 1.1 and by the title. |
| "the asymmetry in the Propose-and-Reject algorithm leads to dramatically different outcomes" | 451 to 452 | It is beat 4.1 in plainer words. |
| Footnote 5 (everything happens inside a computer) | 472 | Already used in episode 2, beat 4.3. |
| "still stands as one of the great achievements in the analysis of algorithms"; research in EECS and economics | 464 to 468 | Praise and outlook, not steps. |
| D. Gusfield and R. W. Irving, The Stable Marriage Problem: Structure and Algorithms, MIT Press, 1989 | 469 to 471 | A further-reading entry; the Gale and Shapley paper is shown on screen in beat 4.4, the book is left to the notes. |

## Layout used by every scene

One stage, built in `hook` and kept to the end: the lists of episode 8 with the two
stable matchings marked by colour. Nothing but the scene heading is above y = 2.7;
nothing is below y = -2.7.

Colours: job blue `BLUE_C`; candidate gold `GOLD_C`; plain cell border `GREY_B` width
2; "partner in both stable matchings" `YELLOW_D`; "partner in the job optimal matching"
`GREEN_C`; "partner in the other stable matching" `PURPLE_B`; supposed, impossible `RED_C`;
rogue `ORANGE`.

Four columns at x = -4.2, -1.4, 1.4, 4.2. Every box is 2.4 wide.

Job headers `box_label(name, BLUE_C, w=2.4, h=0.5, font_size=22)` at y = 2.42; cells
`Rectangle(width=2.4, height=0.42)`, border `GREY_B` width 2, at y = 1.93 (row 1), 1.49
(row 2), 1.05 (row 3), 0.61 (row 4), names `txt(name, 20)`.

| column | header | row 1 | row 2 | row 3 | row 4 |
|---|---|---|---|---|---|
| x = -4.2 | Job 1 | Ada | Bea | Cleo | Dora |
| x = -1.4 | Job 2 | Ada | Dora | Cleo | Bea |
| x = 1.4 | Job 3 | Ada | Cleo | Bea | Dora |
| x = 4.2 | Job 4 | Ada | Bea | Cleo | Dora |

Candidate headers `box_label(name, GOLD_C, w=2.4, h=0.5, font_size=22)` at y = -0.65;
cells at y = -1.14 (row 1), -1.58 (row 2), -2.02 (row 3), -2.46 (row 4).

| column | header | row 1 | row 2 | row 3 | row 4 |
|---|---|---|---|---|---|
| x = -4.2 | Ada | Job 1 | Job 3 | Job 2 | Job 4 |
| x = -1.4 | Bea | Job 4 | Job 3 | Job 2 | Job 1 |
| x = 1.4 | Cleo | Job 2 | Job 3 | Job 1 | Job 4 |
| x = 4.2 | Dora | Job 3 | Job 4 | Job 2 | Job 1 |

Coloured borders (width 4), set in beat 1.1 and kept:
- yellow: Job 1 row 1, Job 4 row 2, Ada row 1, Bea row 1;
- green: Job 2 row 2, Job 3 row 2, Cleo row 2, Dora row 3;
- purple: Job 2 row 3, Job 3 row 4, Cleo row 1, Dora row 1.
"A candidate's green job" on the stage is her green cell, or her yellow cell if she has none: Ada row 1, Bea row 1, Cleo row 2, Dora row 3.
"A job's optimal candidate" on the stage is its green or yellow cell: Job 1 row 1, Job 2 row 2, Job 3 row 2, Job 4 row 2.

The gap between the halves (y from 0.40 down to -0.40, x from -5.4 to 5.4) holds either
one text at (0, 0) (size 20, at most 10 wide) or lines and arrows, never both at once.

| name | kind | from | to |
|---|---|---|---|
| R | dashed line, `ORANGE`, width 4, Job 3 and Cleo | (1.4, 0.36) | (1.4, -0.36) |
| D1 to D4 | four arrows pointing down, white | (x, 0.36) | (x, -0.36), for x = -4.2, -1.4, 1.4, 4.2 |
| P1 to P4 | four arrows pointing up, white | (x, -0.36) | (x, 0.36), for x = -4.2, -1.4, 1.4, 4.2 |
| U1 | arrow, Ada to Job 1 | (-4.2, -0.36) | (-4.2, 0.36) |
| U2 | arrow, Bea to Job 4 | (-1.4, -0.36) | (4.2, 0.36) |
| U3 | arrow, Cleo to Job 2 | (1.4, -0.36) | (-1.4, 0.36) |
| U4 | arrow, Dora to Job 3 | (4.2, -0.36) | (1.4, 0.36) |

All arrows are `Arrow(start, end, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.1)`.
Never have two of these on the stage with the same end points: the D arrows are removed
before the P arrows are drawn, the P arrows before U1 to U4, and U1 to U4 before the D
arrows return.

Left strip (x = -6.15, texts at most 1.2 wide): `txt("jobs", 18, GREY_B)` at (-6.15, 2.42);
`txt("candidates", 18, GREY_B)` at (-6.15, -0.65); slot LJ at (-6.15, 1.3), size 18; slot LC1 at
(-6.15, -1.4) and slot LC2 at (-6.15, -1.7), size 18; slot LP at (-6.15, -2.3), size 18.

Right strip (x = 6.15, texts at most 1.2 wide). Legend: a square of side 0.28 with
`YELLOW_D` border width 4 at (6.15, 1.95) and `txt("both", 18, YELLOW_D)` at (6.15, 1.65);
a `GREEN_C` square at (6.15, 1.30) and `txt("first", 18, GREEN_C)` at (6.15, 1.00); a
`PURPLE_B` square at (6.15, 0.65) and `txt("second", 18, PURPLE_B)` at (6.15, 0.35).
Slot RS at (6.15, -1.4), size 18.

Rules for the builder that come from the check script:
- To highlight a cell, change the stroke of the cell's own rectangle (`set_stroke(colour, 4)`). Never put a second rectangle on top.
- Never draw a line through a name.
- "Flash" means `Indicate(obj, color=YELLOW_D, scale_factor=1.1)`; the object returns to the look it had.
- When a text in a slot or in the gap changes, fade the old one out and the new one in at the same place in one animation.

## Scene `hook`: heading "What do the candidates get?"

Stage: empty at the start, built in beat 1.1.
Kept from the scene before: nothing. Removed at the end: hold until the voice has
finished beat 1.3, then remove the text in slot RS.

### 1.1
> Propose and reject gives every job its optimal candidate, the best partner it has in
> any stable matching. In our example that is the green matching, and the purple one is
> the only other stable matching.

- with the first word: the strip labels, the four job columns and the four candidate columns appear (headers and cells with names), jobs first.
- on "the green matching": the four yellow and the four green borders are set, and the legend entries "both" and "first" appear.
- on "the purple one": the four purple borders are set, and the legend entry "second" appears.
- uses: episodes 8 and 9, F1, F2.

### 1.2
> Now look at the columns of the candidates. For Cleo and for Dora the green job sits
> below the purple one. So the matching that is best for every job gives these two the
> lowest job they have in any stable matching, which we called pessimal.

- with the first word: flash the four candidate headers together.
- on "For Cleo": flash row 2 of the Cleo column (Job 3, green), then row 1 (Job 2, purple).
- on "for Dora": flash row 3 of the Dora column (Job 2, green), then row 1 (Job 3, purple).
- on "pessimal": the text `txt("pessimal", 18, GREEN_C)` appears in slot LP.
- uses: the cells on screen, F3, episode 8 beat 3.4.

### 1.3
> Ada and Bea have the same job in both, so for them best and worst are one and the
> same. Is this an accident of the example, or a law? Let us test it on Cleo, whose
> green job is job three.

- with the first word: flash row 1 of the Ada column and row 1 of the Bea column (both yellow).
- on "or a law": the text `txt("a law?", 18, YELLOW_D)` appears in slot RS.
- on "test it on Cleo": flash the header "Cleo", then row 2 of the Cleo column (Job 3, green).
- uses: beat 1.2, F7.
- end of scene: hold until the voice has finished this beat, then remove the text in slot RS.

## Scene `cleo`: heading "Could Cleo do worse?"

Stage: as built. This scene adds red borders, the line R and a text in slot RS, and takes them away again in beat 2.4.
Kept from the scene before: everything except the text in slot RS.
Removed at the end: nothing more (beat 2.4 cleans up).

### 2.1
> Suppose there were some other stable matching in which Cleo has a job she likes less
> than job three. On her list that could only be job one or job four.

- with the first word: flash row 2 of the Cleo column (Job 3, green).
- on "likes less": flash rows 3 and 4 of the Cleo column together.
- on "job one or job four": rows 3 and 4 of the Cleo column (Job 1, Job 4) get a `RED_C` border, width 4.
- uses: F3 (what "not pessimal" would mean), F7, Cleo's list on screen.

### 2.2
> In that matching job three is not with Cleo, so it has some other candidate. Could she
> be above Cleo on its list? No, because Cleo is the optimal candidate of job three, the
> best it gets in any stable matching, and this matching is stable.

- with the first word: flash the header "Job 3".
- on "some other candidate": flash rows 1, 3 and 4 of the Job 3 column (Ada, Bea, Dora) together.
- on "above Cleo on its list": flash row 1 of the Job 3 column (Ada).
- on "optimal candidate of job three": flash row 2 of the Job 3 column (Cleo, green); then row 1 (Ada) fades to opacity 0.25, cell and name.
- uses: beat 2.1, F6, F7.

### 2.3
> So that other candidate is below Cleo, and job three would rather have Cleo. And Cleo
> would rather have job three than her job there, because that is what we supposed. They
> are a rogue couple, so that matching is not stable after all.

- with the first word: nothing new.
- on "below Cleo": rows 3 and 4 of the Job 3 column (Bea, Dora) get a `RED_C` border, width 4.
- on "would rather have job three": flash row 2 of the Cleo column (Job 3, green), which is above her two red cells.
- on "a rogue couple": the dashed orange line R is drawn in the gap between the Job 3 column and the Cleo header.
- on "not stable after all": the text `txt("not stable", 18, RED_C)` appears in slot RS.
- uses: beats 2.1 and 2.2, the lists on screen, F5.

### 2.4
> So no stable matching gives Cleo less than job three. Job three is the worst she can
> get, her pessimal job, and the job optimal matching hands her exactly that.

- with the first word: the line R and the text in slot RS are removed.
- on "less than job three": rows 3 and 4 of the Cleo column are set back to `GREY_B` width 2 and fade to opacity 0.25; rows 3 and 4 of the Job 3 column are set back to `GREY_B` width 2; row 1 of the Job 3 column returns to full opacity.
- on "her pessimal job": flash row 2 of the Cleo column (Job 3, green) and the text "pessimal" in slot LP.
- on "hands her exactly that": rows 3 and 4 of the Cleo column return to full opacity.
- uses: beat 2.3, F3.

## Scene `law`: heading "Best for one side, worst for the other"

Stage: as at the end of beat 2.4 (lists, coloured borders, legend, "pessimal" in slot LP, empty gap).
Kept from the scene before: everything.
Removed at the end: hold until the voice has finished beat 3.2, then remove the gap text.

### 3.1
> The argument never used the name of Cleo. Take any candidate, and call the job she
> gets in the job optimal matching her green job. Suppose some stable matching gave her
> a job she likes less. Then her green job has another partner there, and it likes her
> more, because she is its optimal candidate.

- with the first word: flash the header "Cleo".
- on "Take any candidate": flash the four candidate headers together.
- on "matching her green job": flash the green job of each candidate together: Ada row 1, Bea row 1, Cleo row 2, Dora row 3.
- on "a job she likes less": flash every candidate cell that lies below her green job together: Ada rows 2, 3, 4; Bea rows 2, 3, 4; Cleo rows 3, 4; Dora row 4.
- on "its optimal candidate": flash the optimal candidate of each job together: Job 1 row 1, Job 2 row 2, Job 3 row 2, Job 4 row 2.
- uses: beats 2.1 to 2.3 (the same steps with names), F5, F6.

### 3.2
> So she and her green job would both rather have each other, and that matching has a
> rogue couple. So it does not exist, and her green job is her pessimal job. A job
> optimal matching is always candidate pessimal.

- with the first word: nothing new.
- on "a rogue couple": the dashed orange line R is drawn again, as the picture of such a pair.
- on "does not exist": the line R is removed.
- on "always candidate pessimal": the gap text appears: `txt("Theorem 11.3: a job optimal matching is candidate pessimal", 20, YELLOW_D)`.
- uses: beat 3.1, F4, F5.
- end of scene: hold until the voice has finished this beat, then remove the gap text.

## Scene `swap`: heading "Who should propose?"

Stage: lists, coloured borders, legend, "pessimal" in slot LP, empty gap.
Kept from the scene before: those. Removed at the end: nothing (the end card follows).

### 4.1
> So the side that proposes gets its best stable outcome, and the side that answers gets
> its worst. Then the remedy for the candidates is to let them do the proposing. None of
> our proofs cared which side was called jobs, so with candidates proposing the result
> is candidate optimal.

- with the first word: nothing new.
- on "the side that proposes": the four arrows D1 to D4 grow, pointing down from the job columns; the text `txt("job optimal", 18, GREEN_C)` appears in slot LJ.
- on "let them do the proposing": D1 to D4 are removed, and the four arrows P1 to P4 grow, pointing up from the candidate headers.
- on "is candidate optimal": `txt("candidate", 18, PURPLE_B)` appears in slot LC1 and `txt("optimal", 18, PURPLE_B)` in slot LC2; flash the purple and yellow cells of the four candidate columns (row 1 of each) together.
- uses: episode 9 (the proposers get their optimal partners), beat 3.2, F8.

### 4.2
> Try it on our lists. Ada asks job one, Bea asks job four, Cleo asks job two, and Dora
> asks job three. Every job has exactly one offer, so it stops on the first day, and the
> result is the purple matching.

- with the first word: P1 to P4 are removed.
- on "Ada asks job one": the arrow U1 grows.
- on "Bea asks job four": the arrow U2 grows.
- on "Cleo asks job two": the arrow U3 grows.
- on "asks job three": the arrow U4 grows.
- on "the purple matching": the four arrows turn `PURPLE_B`; flash row 1 of the four candidate columns together.
- uses: the candidates' lists on screen (row 1 of each column), F8.

### 4.3
> This choice was made for real in the residency match. At first the hospitals did the
> proposing, so the result was hospital optimal. In the nineteen nineties the roles were
> reversed, so that the students do the proposing. Later changes also let married
> couples ask for positions at the same or nearby hospitals.

- with the first word: U1 to U4 are removed.
- on "the hospitals did the proposing": the arrows D1 to D4 grow, pointing down; the text `txt("1952", 18)` appears in slot RS.
- on "the roles were reversed": D1 to D4 are removed and P1 to P4 grow, pointing up; slot RS changes to `txt("1990s", 18)`.
- on "married couples": flash the headers "Cleo" and "Dora" together (a picture of two candidates who apply together).
- uses: episode 2 (the residency match, 1952), F9.

### 4.4
> The algorithm was in use for ten years before Gale and Shapley analysed it properly,
> in a paper from nineteen sixty-two. It always stops, it always ends in a stable
> matching, and it gives the best stable outcome to whoever proposes. So the question to
> ask of any matching system is who makes the offers.

- with the first word: P1 to P4 are removed.
- on "Gale and Shapley": the gap text appears: `txt("Gale and Shapley, College Admissions and the Stability of Marriage, 1962", 20)`; slot RS changes to `txt("1962", 18)`.
- on "always stops": flash the four job headers together.
- on "a stable": flash the legend (three squares, three words).
- on "whoever proposes": flash the texts in slots LJ, LC1 and LC2 together.
- on "who makes the offers": flash the gap text.
- uses: F10, episodes 5, 7 and 9, beat 4.1.

## End card

- A job optimal matching is always candidate pessimal (Theorem 11.3): every candidate gets the worst job she has in any stable matching.
- If a stable matching gave her less, she and her job from the job optimal matching would be a rogue couple in it.
- Let the candidates propose, and the result is candidate optimal instead.
- The residency match began with the hospitals proposing and has had the students proposing since the 1990s.

## Author's check, each answered yes

- The first beat shows one concrete case before any definition. Yes: the four-by-four lists with both stable matchings.
- Every "uses" line names an earlier beat, a fact row, or what is on the screen. Yes.
- A name is introduced after the beat where the viewer sees it happen. Yes: the theorem is stated in 3.2 after Cleo's case.
- Every beat has a drawn object that changes; no beat is words on an empty stage. Yes.
- Every phrase after "on" is copied from its own beat, and appears there once. Yes, checked by script.
- A beat over fourteen seconds has at least two changes, over twenty-six at least three. Yes, checked by script.
- If the voice counts things, the stage shows exactly that many. Yes: four offers in 4.2, one arrow each.
- No step is skipped, and every step the notes left out is in "Added to the notes". Yes.
- Every item of the notes in the source range is in a beat or in "Left out". Yes.
- Narration: 13 beats, two to four sentences each, no sentence over 25 words, no beat over 60 words, no digit, colon or symbol. Yes, checked by script.
