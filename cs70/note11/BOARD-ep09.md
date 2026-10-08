# BOARD: episode 09, The Proposers Win

Source: `notes.txt` lines 416 to 437. Language: en. Aim: 5 to 6 minutes (about 730 words).
File `ep09_job_optimal.py`, class `Ep09JobOptimal`. Scenes, in order: `run`, `suppose`, `rogue`.

The builder copies every narration line (the lines that start with a greater-than sign)
into a `say()` unchanged, one beat per `say()`, and builds exactly the stage described.
It decides nothing; an unclear line is a question in its report.

Format, read by `check.py`: a line that starts with three hash signs opens a beat, and
every line after it that starts with a greater-than sign is that beat's narration.
Neither is used anywhere else in this file.

## Facts

Candidates A, B, C, D of the notes are Ada, Bea, Cleo, Dora, as in episode 8. In the
proof the notes use the letters J, C*, J*, C' and M; they are on screen, and the voice
says "the refused job", "its optimal candidate" (or "she"), "the rival", "the partner
the rival has in the stable matching".

| id | Fact, with all its conditions | Notes line | Computed how |
|---|---|---|---|
| F1 | The lists of the example. Job 1: Ada, Bea, Cleo, Dora. Job 2: Ada, Dora, Cleo, Bea. Job 3: Ada, Cleo, Bea, Dora. Job 4: Ada, Bea, Cleo, Dora. Ada: 1, 3, 2, 4. Bea: 4, 3, 2, 1. Cleo: 2, 3, 1, 4. Dora: 3, 4, 2, 1. | 337 to 380 | `JOBS`, `CANDS` below |
| F2 | The two stable matchings; the job optimal one is Job 1 with Ada, Job 2 with Dora, Job 3 with Cleo, Job 4 with Bea. Optimal candidates: Ada, Dora, Cleo, Bea for Jobs 1 to 4. | 381 to 401 | `OPT == M1` (episode 8) |
| F3 | The run of propose and reject on these lists (worked out by the author; the notes do not show it). Day one: all four jobs ask Ada; Ada keeps Job 1 and refuses Jobs 2, 3, 4. Day two: Job 1 asks Ada, Job 2 asks Dora, Job 3 asks Cleo, Job 4 asks Bea; nobody is refused. Output: the job optimal matching. | from F1 and the rules, lines 63 to 72 | `DAYS` below equals `run(JOBS, CANDS)` |
| F4 | Definition 11.2: the optimal candidate for a job is the highest-ranked candidate it is paired with in any stable matching. So (a) there is a stable matching in which the job and its optimal candidate are paired, and (b) no partner the job has in any stable matching is above its optimal candidate. | 391 to 394 | stated |
| F5 | Theorem 11.2: the matching output by the propose-and-reject algorithm is job (employer) optimal. | 418 | checked on all 46656 instances with three jobs and three candidates: `always_job_optimal` |
| F6 | Proof of the notes. Suppose not. Then on some day some job is rejected by its optimal candidate; let day k be the first such day. On it J is rejected by C* (its optimal candidate) in favour of J*. There is a stable matching M with J and C* paired; in M, J* is paired with some C'. Then (J*, C*) is a rogue couple in M: C* prefers J* to J; and since no job was rejected by its optimal candidate before day k and J* offers to C* on day k, J* likes C* at least as much as its optimal candidate, hence at least as much as C'. Contradiction. | 419 to 431 | checked on all 46656 instances: `never_refused_by_optimal` |
| F7 | The proof is an induction in the form of the well-ordering principle ("the first such day"). As a regular induction the statement is: for every k, no job is rejected by its optimal candidate on day k. | 432 to 437 | stated |
| F8 | The result of propose and reject is a stable matching (Theorem 11.1), and a job moves past a name on its list only after that name has refused it. | 319; 63 to 69 | episode 7 |

```python
from itertools import permutations, product
JOBS = {1: ["Ada", "Bea", "Cleo", "Dora"], 2: ["Ada", "Dora", "Cleo", "Bea"],
        3: ["Ada", "Cleo", "Bea", "Dora"], 4: ["Ada", "Bea", "Cleo", "Dora"]}
CANDS = {"Ada": [1, 3, 2, 4], "Bea": [4, 3, 2, 1], "Cleo": [2, 3, 1, 4], "Dora": [3, 4, 2, 1]}
M1 = {1: "Ada", 2: "Dora", 3: "Cleo", 4: "Bea"}

def run(jobs, cands):
    """Per day: (offers job -> candidate, refused (job, candidate) pairs)."""
    left = {j: list(l) for j, l in jobs.items()}
    days = []
    while True:
        offers = {j: left[j][0] for j in jobs}
        refused = []
        for c in cands:
            got = [j for j in offers if offers[j] == c]
            if got:
                best = min(got, key=cands[c].index)
                refused += [(j, c) for j in got if j != best]
        days.append((offers, refused))
        if not refused:
            return days
        for j, c in refused:
            left[j].remove(c)

def stable_matchings(jobs, cands):
    out = []
    for p in permutations(cands):
        m = dict(zip(jobs, p)); has = {c: j for j, c in m.items()}
        if not any(cands[c].index(j) < cands[c].index(has[c])
                   for j in jobs for c in jobs[j][:jobs[j].index(m[j])]):
            out.append(m)
    return out

def optimal(jobs, cands):
    st = stable_matchings(jobs, cands)
    return {j: min((m[j] for m in st), key=jobs[j].index) for j in jobs}

DAYS = [({1: "Ada", 2: "Ada", 3: "Ada", 4: "Ada"}, [(2, "Ada"), (3, "Ada"), (4, "Ada")]),
        ({1: "Ada", 2: "Dora", 3: "Cleo", 4: "Bea"}, [])]
assert run(JOBS, CANDS) == DAYS and DAYS[-1][0] == M1
OPT = optimal(JOBS, CANDS)
assert OPT == M1 and all(OPT[j] != c for _, ref in DAYS for j, c in ref)

nj, nc = [1, 2, 3], ["x", "y", "z"]
always_job_optimal = never_refused_by_optimal = True
for jl in product(permutations(nc), repeat=3):
    for cl in product(permutations(nj), repeat=3):
        jobs, cands = dict(zip(nj, map(list, jl))), dict(zip(nc, map(list, cl)))
        days, opt = run(jobs, cands), optimal(jobs, cands)
        always_job_optimal = always_job_optimal and days[-1][0] == opt
        never_refused_by_optimal = never_refused_by_optimal and all(opt[j] != c for _, r in days for j, c in r)
assert always_job_optimal and never_refused_by_optimal
```

(The enumeration takes some seconds. The builder may keep it in a separate check and
assert only the lines before it in the episode file.)

## Added to the notes

| Beat | The step that was missing | Why it holds |
|---|---|---|
| 1.2, 1.3 | The run of the algorithm on the four-by-four example; the notes never run it. | F3, computed. |
| 1.4 | The observation that starts the proof: in this run every refusal came from a candidate who is not the refused job's optimal candidate. | Jobs 2, 3, 4 were refused by Ada; their optimal candidates are Dora, Cleo, Bea. |
| 1.5, 1.6 | The notes begin "suppose the matching is not employer optimal; then there exists a day on which some job had its offer rejected by its optimal candidate". Why does the second follow from the first? The episode proves the equivalent statement: if no job is ever refused by its optimal candidate, every job ends with her. | A job moves past a name only after a refusal, so a job never refused by its optimal candidate does not end below her. It does not end above her, because the result is a stable matching (F8) and no stable partner is above the optimal candidate (F4 b). |
| 2.1 | Why there is a first such day. | The days with such a refusal are a set of natural numbers that is not empty; well-ordering principle (episode 6). |
| 2.2 | Why the candidate ranks the rival above the refused job. The notes: "it is clear". | Afternoon rule: she keeps the offer she likes best and refuses the others, so the one she keeps is above the one she refuses. Also the rival is a different job. |
| 2.3 | Why a stable matching with J and C* paired exists. | F4 (a): optimal candidate means the best among partners in stable matchings, so she is a partner in at least one. |
| 3.2 | Why J* asking C* on that day means that every name above C* on J*'s list has refused J* earlier. The notes skip this. | Morning rule: a job asks the first name not crossed off; names are crossed off only by a refusal, in an evening before. |
| 3.3 | Why C* is at or above J*'s optimal candidate on J*'s list. The notes: "this implies". | Before the first red day no job was refused by its optimal candidate; the names above C* all refused J* before that day; so J*'s optimal candidate is not one of them. |
| 3.4 | Why J*'s optimal candidate is at or above C'. The notes: "and therefore at least as much as C'". | C' is J*'s partner in the stable matching M, and no stable partner is above the optimal candidate (F4 b). |
| 3.5 | From "at least as much as C'" to "prefers C* to C'", which a rogue couple needs. The notes do not say it. | C' is not C*: in M, C* is with J, and J is not J*. A list has no ties. |
| 3.6 | From "no first red day" to "no job is ever refused by its optimal candidate", and with beat 1.6 to the theorem. | Well-ordering again: no first means none. |
| 3.7 | The answer to the notes' concept check (where the well-ordering principle is used) and the statement for the exercise (regular induction). | F7; shown on screen as result line T2. |

## Left out, and why

| Item of the notes | Line | Reason |
|---|---|---|
| "Now, we get to the heart of the matter" | 416 | Not a step. |
| The exercise itself (rewrite the proof as a regular induction) | 435 to 437 | The statement to induct on is shown (T2); the rewriting is left to the viewer, as in the notes. |
| The names "employer optimal", "employer/job optimal" | 418 to 431 | One name per thing: "job optimal". |

## Layout used by every scene

Three stages, one per scene; each scene starts by removing the stage before it.
Nothing but the scene heading is above y = 2.7; nothing is below y = -2.7.

Colours: job blue `BLUE_C`; candidate gold `GOLD_C`; plain border `GREY_B` width 2; in
hand, partner `GREEN_C`; refused, red day `RED_C`; "would rather have" `ORANGE`; looked at `YELLOW_D`.

Stage one (scene `run`): the lists of episode 8.
- Four columns at x = -4.2, -1.4, 1.4, 4.2; every box 2.4 wide.
- Job headers `box_label(name, BLUE_C, w=2.4, h=0.5, font_size=22)` at y = 2.42; cells
  `Rectangle(width=2.4, height=0.42)`, border `GREY_B` width 2, at y = 1.93 (row 1),
  1.49 (row 2), 1.05 (row 3), 0.61 (row 4), names `txt(name, 20)`.

| column | header | row 1 | row 2 | row 3 | row 4 |
|---|---|---|---|---|---|
| x = -4.2 | Job 1 | Ada | Bea | Cleo | Dora |
| x = -1.4 | Job 2 | Ada | Dora | Cleo | Bea |
| x = 1.4 | Job 3 | Ada | Cleo | Bea | Dora |
| x = 4.2 | Job 4 | Ada | Bea | Cleo | Dora |

- Candidate headers `box_label(name, GOLD_C, w=2.4, h=0.5, font_size=22)` at y = -0.65; cells at y = -1.14 (row 1), -1.58 (row 2), -2.02 (row 3), -2.46 (row 4).

| column | header | row 1 | row 2 | row 3 | row 4 |
|---|---|---|---|---|---|
| x = -4.2 | Ada | Job 1 | Job 3 | Job 2 | Job 4 |
| x = -1.4 | Bea | Job 4 | Job 3 | Job 2 | Job 1 |
| x = 1.4 | Cleo | Job 2 | Job 3 | Job 1 | Job 4 |
| x = 4.2 | Dora | Job 3 | Job 4 | Job 2 | Job 1 |

- Offer arrows in the gap (y from 0.36 down to -0.36), `Arrow(start, end, buff=0, stroke_width=4, tip_length=0.18)` (an absolute tip length, so that the short vertical arrows show a head too), white when drawn. The four heads on Ada's header land 0.6 apart, and N2, N3, N4 cross each other at three different points:

| name | offer | from | to |
|---|---|---|---|
| O1 | Job 1 to Ada | (-5.1, 0.36) | (-5.1, -0.36) |
| O2 | Job 2 to Ada | (-1.4, 0.36) | (-4.5, -0.36) |
| O3 | Job 3 to Ada | (1.4, 0.36) | (-3.9, -0.36) |
| O4 | Job 4 to Ada | (4.2, 0.36) | (-3.3, -0.36) |
| N2 | Job 2 to Dora | (-0.6, 0.36) | (4.6, -0.36) |
| N3 | Job 3 to Cleo | (0.7, 0.36) | (0.7, -0.36) |
| N4 | Job 4 to Bea | (3.6, 0.36) | (-2.2, -0.36) |

  O2, O3, O4 are removed before N2, N3, N4 are drawn.
- Gap text (beats 1.4 to 1.6, after all arrows are removed): one text at (0, 0), size 24, at most 10 wide. It is the thing these beats are about, so it sits in the middle of the frame between the two halves.
- Left strip (x = -6.15, texts at most 1.2 wide): `txt("jobs", 20, GREY_B)` at (-6.15, 2.42); `txt("candidates", 20, GREY_B)` at (-6.15, -0.65). No other text in the strip.
- Right strip: slot RS at (6.15, 1.3), size 20, at most 1.2 wide, for the day.

Stage two (scene `suppose`).
- Caption over the day row, so that nobody takes these days for the run of scene `run`: `txt("a supposed run on other lists, not the run we just watched", 22, GREY_A)` at (0, 2.5), at most 9 wide.
- Day row: eight boxes `Rectangle(width=1.3, height=0.7)`, border `GREY_B` width 2, at y = 1.9 and x = -5.25, -3.75, -2.25, -0.75, 0.75, 2.25, 3.75, 5.25, with the labels "day 1" to "day 8" (`txt`, 20, at most 1.1 wide). A red day has stroke `RED_C` width 3 and fill `RED_C` opacity 0.25.
- Under-label `txt("first red day", 22, RED_C)` at (0.75, 1.25), under "day 5".
- Legend: a red-day square of side 0.35 at (-5.0, 0.5) and `txt("a day on which some job is refused by its optimal candidate", 20)` with its left edge at x = -4.6, y = 0.5.
- Actors at y = -0.9: `box_label("J", BLUE_C, w=1.6, h=0.6, font_size=24)` at (-4.0, -0.9); `box_label("C*", GOLD_C, w=1.6, h=0.6, font_size=24)` at (0, -0.9); `box_label("J*", BLUE_C, w=1.6, h=0.6, font_size=24)` at (4.0, -0.9).
  Captions `txt`, 20, `GREY_A`, at y = -1.5: "the refused job" at x = -4.0; "its optimal candidate" at x = 0; "the rival" at x = 4.0.
  Refusal arrow `Arrow((-3.2, -0.9), (-0.8, -0.9), buff=0, color=RED_C)` with `txt("refused", 22, RED_C)` at (-2.0, -0.5).
  Kept arrow `Arrow((3.2, -0.9), (0.8, -0.9), buff=0, color=GREEN_C)` with `txt("kept", 22, GREEN_C)` at (2.0, -0.5).
- Matching lines, two texts, size 22, centred at x = 0: M1 `txt("a stable matching M pairs J with C*", 22)` at (0, -2.05); M2 `txt("in M, the rival J* has some partner C'", 22)` at (0, -2.5).

Stage three (scene `rogue`).
- The candidate's list: header `box_label("candidate C*", GOLD_C, w=2.4, h=0.55, font_size=22)` at (-5.2, 2.3); cells `Rectangle(width=2.4, height=0.48)` at y = 1.72 (text "J*") and 1.20 (text "J").
- The rival's list: header `box_label("job J*", BLUE_C, w=2.4, h=0.55, font_size=22)` at (-2.4, 2.3); four cells at y = 1.72 (text "refused J* earlier", text at opacity 0.5 so that it can still be read, border at full opacity, text at most 2.2 wide), 1.20 (text "C*"), 0.68 (text "optimal for J*"), 0.16 (text "C'").
- The stable matching M, right: title `txt("stable matching M", 20)` at (3.6, 2.4); `box_label("J", BLUE_C, w=1.4, h=0.55, font_size=22)` at (2.0, 1.7) and `box_label("J*", BLUE_C, w=1.4, h=0.55, font_size=22)` at (2.0, 0.8); `box_label("C*", GOLD_C, w=1.4, h=0.55, font_size=22)` at (5.2, 1.7) and `box_label("C'", GOLD_C, w=1.4, h=0.55, font_size=22)` at (5.2, 0.8); pair lines, white, width 4, from (2.7, 1.7) to (4.5, 1.7) and from (2.7, 0.8) to (4.5, 0.8); rogue line `DashedLine((2.3, 1.1), (4.9, 1.4), color=ORANGE, stroke_width=5, dash_length=0.15)`, from the top edge of the box "J*" to the bottom edge of the box "C*", clear of the box corners and of both pair lines.
- Proof lines, `txt`, size 20, left edge at x = -6.2. They fill the lower half of the frame. No line is wider than 10 units; G3 and G4 are two texts each, and both texts of a line appear together. The possessive of J* is never written (it renders like a double quote): the lines say "the optimal candidate of J*".

| line | y | text |
|---|---|---|
| G1 | -0.42 | C* prefers J* to J: she refused J and kept J* |
| G2 | -0.78 | J* asks C* on the first red day, so every name above C* refused J* earlier |
| G3, first text | -1.14 | before that day no job was refused by its optimal candidate, |
| G3, second text | -1.50 | so C* is at or above the optimal candidate of J* |
| G4, first text | -1.86 | C' is the partner of J* in the stable matching M, |
| G4, second text | -2.22 | so C' is at or below the optimal candidate of J*, and C' is not C* |
| G5 | -2.58 | so J* prefers C* to C': J* and C* are a rogue couple in M |

  (In the rival's list the cells "C*", "optimal for J*" and "C'" are drawn on three rungs; the proof lines say "at or above" and "at or below", because two of them may be the same candidate. The cell "C'" may never be the cell "C*".)
- Result lines for beat 3.7 (after the proof lines are removed), centred at x = 0, each at most 10 wide: T1 at y = -0.9, size 24; T2 at y = -1.65, size 22; T3 at y = -2.35, size 22.

Rules for the builder that come from the check script:
- To highlight a cell or box, change its own stroke (`set_stroke(colour, 4)`). Never put a second rectangle on top.
- "Crossed off" is shown by fading the cell and its name to opacity 0.25. Never draw a line through a text.
- "Flash" means `Indicate(obj, color=YELLOW_D, scale_factor=1.1)`; the object returns to the look it had.
- When a text in a slot changes, fade the old one out and the new one in at the same place in one animation.

## Scene `run`: heading "Which one does the algorithm pick?"

Stage: stage one, built in beat 1.1.
Kept from the scene before: nothing. Removed at the end: hold until the voice has
finished beat 1.6, then remove everything.

### 1.1
> Last time four jobs and four candidates had exactly two stable matchings, one optimal
> for the jobs and one optimal for the candidates. So let us run propose and reject on
> these lists and see which one comes out.

- with the first word: the strip labels, the four job columns and the four candidate columns appear (headers and cells with names), jobs first.
- on "run propose and reject": the text "Day 1" appears in slot RS.
- uses: episode 8, F1, F2.

### 1.2
> On the first morning all four jobs ask Ada, because she is at the top of every list.
> Ada keeps job one, her favourite, and refuses the other three, and each of them
> crosses her off.

- with the first word: flash row 1 of the four job columns together.
- on "all four jobs ask Ada": the arrows O1, O2, O3, O4 grow, left to right.
- on "Ada keeps job one": O1 turns `GREEN_C`; row 1 of the Ada column (Job 1) and row 1 of the Job 1 column (Ada) get a `GREEN_C` border, width 4.
- on "refuses the other three": O2, O3, O4 turn `RED_C`, then fade out and are removed.
- on "crosses her off": row 1 (Ada) of the Job 2, Job 3 and Job 4 columns fades to opacity 0.25, cell and name.
- uses: F3 (day one), the lists on screen (Ada's list starts with Job 1).

### 1.3
> On the second morning job one asks Ada again, job two asks Dora, job three asks Cleo,
> and job four asks Bea. Every candidate has exactly one offer, so nobody is refused and
> the algorithm stops.

- with the first word: slot RS changes to "Day 2"; flash O1.
- on "job two asks Dora": the arrow N2 grows.
- on "job three asks Cleo": the arrow N3 grows.
- on "job four asks Bea": the arrow N4 grows.
- on "nobody is refused": N2, N3, N4 turn `GREEN_C`; `GREEN_C` border, width 4, on row 2 of the Job 2 column (Dora), row 2 of the Job 3 column (Cleo), row 2 of the Job 4 column (Bea), row 3 of the Dora column (Job 2), row 2 of the Cleo column (Job 3) and row 1 of the Bea column (Job 4).
- uses: F3 (day two), beat 1.2 (the crossed-off cells).

### 1.4
> This is the first of our two matchings, the one in which every job has its optimal
> candidate. And look who did the refusing along the way. Jobs two, three and four were
> refused only by Ada, and Ada is not the optimal candidate of any of them.

- with the first word: flash the four green arrows O1, N2, N3, N4 together.
- on "every job has its optimal candidate": the four arrows O1, N2, N3, N4 fade out and are removed (the green borders keep the matching on screen), and the gap text appears: `txt("this is the job optimal matching", 24, GREEN_C)`.
- on "refused only by Ada": flash the three faded Ada cells (row 1 of the Job 2, Job 3, Job 4 columns).
- on "not the optimal candidate": flash row 2 of the Job 2, Job 3 and Job 4 columns (Dora, Cleo, Bea, green).
- uses: beat 1.3, F2, episode 8.

### 1.5
> So here is a bold guess for all lists. In propose and reject no job is ever refused by
> its optimal candidate. If that is true, every job ends with its optimal candidate, and
> the result is job optimal.

- with the first word: flash the gap text.
- on "no job is ever refused": the gap text changes to `txt("guess: no job is ever refused by its optimal candidate", 24, YELLOW_D)`.
- on "ends with its optimal candidate": flash the green cells of the four job columns together.
- uses: beat 1.4 (the observation). A guess, proved in scenes `suppose` and `rogue`.

### 1.6
> Why would that be enough? A job only moves past a name that has refused it, so it
> never ends below its optimal candidate. And it cannot end above her, because the
> result is stable, and she is the best partner in any stable matching.

- with the first word: flash the header "Job 2".
- on "moves past a name": flash row 1 of the Job 2 column (Ada, faded), then row 2 (Dora, green).
- on "never ends below": flash rows 3 and 4 of the Job 2 column (Cleo, Bea).
- on "cannot end above her": flash row 1 of the Job 2 column (Ada, faded).
- uses: beat 1.5, F8, F4 (b). Job 2 is the example; the argument is general.
- end of scene: hold until the voice has finished this beat, then remove everything.

## Scene `suppose`: heading "Suppose it happens"

Stage: stage two, built in beats 2.1 to 2.3 from an empty stage.
Kept from the scene before: nothing. Removed at the end: hold until the voice has
finished beat 2.3, then remove everything.

### 2.1
> Suppose the guess is wrong for some lists. Then there are days on which some job is
> refused by its optimal candidate, so mark those days red. By the well ordering
> principle there is a first red day, and we look at that day.

- with the first word: the caption "a supposed run on other lists, not the run we just watched" appears, then the eight day boxes, left to right.
- on "mark those days red": the boxes "day 5" and "day 7" become red days, and the legend appears.
- on "a first red day": flash the box "day 5"; the under-label "first red day" appears under it.
- uses: beat 1.5 (the guess), episode 6 (well-ordering principle). Which days are red is a picture.

### 2.2
> On that day some job is refused by its optimal candidate. She refuses it because she
> keeps an offer she likes more, from another job, which we will call the rival. So she
> ranks the rival above the job she refused.

- with the first word: flash the box "day 5".
- on "refused by its optimal candidate": the boxes "J" and "C*" with their captions, the refusal arrow and the word "refused" appear.
- on "call the rival": the box "J*" with its caption, the kept arrow and the word "kept" appear.
- on "ranks the rival above": flash the kept arrow, then the refusal arrow.
- uses: beat 2.1, the afternoon rule (episode 1), F6.

### 2.3
> Now remember what optimal means. She is the best partner the refused job has in any
> stable matching, so there is a stable matching in which these two are together. In
> that matching the rival has some partner too.

- with the first word: flash the caption "its optimal candidate".
- on "there is a stable matching": matching line M1 appears.
- on "these two are together": flash the boxes "J" and "C*" together.
- on "the rival has some partner": matching line M2 appears; flash the box "J*".
- uses: beat 2.2, F4 (a), F6.
- end of scene: hold until the voice has finished this beat, then remove everything.

## Scene `rogue`: heading "A rogue couple where none can be"

Stage: stage three. Beat 3.1 builds the candidate's list and the matching M, beat 3.2 the rival's list.
Kept from the scene before: nothing. Removed at the end: nothing (the end card follows).

### 3.1
> We will show that in this stable matching the candidate and the rival would both
> rather have each other. Her side of this is quick. There she is with the refused job, and we
> just saw that she ranks the rival above it.

- with the first word: the stable matching M (title, the four boxes, the two pair lines) and the candidate's list (header "candidate C*", cells "J*" and "J") appear.
- on "Her side of this": flash the header "candidate C*".
- on "with the refused job": flash the pair line between "J" and "C*" in the matching; the cell "J" in the candidate's list gets a `GREEN_C` border, width 4.
- on "ranks the rival above": the cell "J*" in the candidate's list gets an `ORANGE` border, width 4; proof line G1 appears.
- uses: beats 2.2 and 2.3, F6.

### 3.2
> Now the side of the rival. On the first red day the rival is asking her, and a job
> asks the first name it has not crossed off. So every name above her on its list has
> already refused it, on an earlier day.

- with the first word: the rival's list appears (header "job J*" and its four cells, the top one faded).
- on "is asking her": the cell "C*" in the rival's list gets a `YELLOW_D` border, width 4.
- on "already refused it": flash the faded top cell "refused J* earlier"; proof line G2 appears.
- uses: beat 2.2 (the rival's offer is the one she keeps), the morning and evening rules (episode 1).

### 3.3
> But before the first red day no job was refused by its optimal candidate. So the
> optimal candidate of the rival is not among the names above her. That puts her level
> with the rival's optimal candidate or higher.

- with the first word: nothing new.
- on "before the first red day": proof line G3 appears.
- on "not among the names above her": flash the faded top cell of the rival's list.
- on "level with": flash the cells "C*" and "optimal for J*" in the rival's list together.
- uses: beat 2.1 (it is the first red day), beat 3.2.

### 3.4
> Now look at the partner the rival has in the stable matching. That partner cannot be
> above its optimal candidate, because optimal means the best partner in any stable
> matching. So our candidate is level with that partner or higher.

- with the first word: nothing new.
- on "the partner the rival has": flash the pair line between "J*" and "C'" in the matching and the box "C'".
- on "cannot be above": flash the cells "optimal for J*" and "C'" in the rival's list together; proof line G4 appears.
- on "our candidate is level": flash the cells "C*" and "C'" in the rival's list together.
- uses: beat 3.3, F4 (b), beat 2.3.

### 3.5
> And she is not that partner, because in this matching she is with the refused job. So
> the rival ranks her strictly above its partner, and wants to switch.

- with the first word: flash proof line G4.
- on "she is with the refused job": flash the pair line between "J" and "C*" in the matching.
- on "strictly above": the cell "C*" in the rival's list turns from yellow to an `ORANGE` border, width 4; proof line G5 appears.
- uses: beat 3.4, the matching on screen.

### 3.6
> So she prefers the rival and the rival prefers her, and they are a rogue couple inside
> a matching we called stable. That is a plain contradiction. So there is no first red day, no
> red day at all, and no job is ever refused by its optimal candidate.

- with the first word: flash the two orange cells (the cell "J*" in the candidate's list and the cell "C*" in the rival's list).
- on "a rogue couple": the dashed orange rogue line is drawn in the matching, from "J*" to "C*".
- on "plain contradiction": the title "stable matching M" turns `RED_C` and is flashed.
- on "ever refused": flash proof line G5.
- uses: beats 3.1 and 3.5, beat 2.1, episode 6 (no first means none), F6.

### 3.7
> So every job ends with its optimal candidate, and propose and reject always produces
> the job optimal matching. The proof took the first red day and showed it cannot
> happen, which is induction in its well ordering form. And if the jobs get their best,
> what is left for the candidates?

- with the first word: the proof lines G1 to G5 fade out and are removed.
- on "job optimal matching": result line T1 appears: `txt("Theorem 11.2: propose and reject produces the job optimal matching", 24, YELLOW_D)`.
- on "well ordering form": result line T2 appears: `txt("as an induction on k: no job is refused by its optimal candidate on day k", 22)`.
- on "left for the candidates": result line T3 appears: `txt("and the candidates?", 22, YELLOW_D)`.
- uses: beat 3.6, beat 1.6 (never refused means ends with her), F5, F7. The last question is episode 10.

## End card

- In propose and reject no job is ever refused by its optimal candidate.
- If one were, the first such day would produce a rogue couple inside a stable matching.
- So every job ends with its optimal candidate: the result is the job optimal matching (Theorem 11.2).
- The proof is an induction on the days, told through the first counterexample.

## Author's check, each answered yes

- The first beat shows one concrete case before any definition. Yes: the four-by-four lists and a run on them.
- Every "uses" line names an earlier beat, a fact row, or what is on the screen. Yes.
- A name is introduced after the beat where the viewer sees it happen. Yes: "the rival" in 2.2 as it appears; the theorem in 3.7.
- Every beat has a drawn object that changes; no beat is words on an empty stage. Yes.
- Every phrase after "on" is copied from its own beat, and appears there once. Yes, checked by script.
- A beat over fourteen seconds has at least two changes, over twenty-six at least three. Yes, checked by script.
- If the voice counts things, the stage shows exactly that many. Yes: four arrows into Ada in 1.2, three of them refused.
- No step is skipped, and every step the notes left out is in "Added to the notes". Yes.
- Every item of the notes in the source range is in a beat or in "Left out". Yes.
- Narration: 16 beats, two to four sentences each, no sentence over 25 words, no beat over 60 words, no digit, colon or symbol. Yes, checked by script.
