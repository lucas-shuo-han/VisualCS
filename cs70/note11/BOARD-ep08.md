# BOARD: episode 08, The Best Partner You Can Keep

Source: `notes.txt` lines 329 to 415. Language: en. Aim: 4 to 5 minutes (about 620 words).
File `ep08_optimal_partners.py`, class `Ep08OptimalPartners`. Scenes, in order: `hook`, `find`, `best`.

The builder copies every narration line (the lines that start with a greater-than sign)
into a `say()` unchanged, one beat per `say()`, and builds exactly the stage described.
It decides nothing; an unclear line is a question in its report.

Format, read by `check.py`: a line that starts with three hash signs opens a beat, and
every line after it that starts with a greater-than sign is that beat's narration.
Neither is used anywhere else in this file.

## Facts

The notes label the jobs 1, 2, 3, 4 and the candidates A, B, C, D. A single capital
letter is read badly by the voice, so the candidates are called Ada, Bea, Cleo, Dora
(A, B, C, D in that order) in episodes 8, 9 and 10. Departure from the notes, reported.
The notes call the two stable matchings M and M'; the voice says "the first" and "the
second", the screen shows them in green and purple.

| id | Fact, with all its conditions | Notes line | Computed how |
|---|---|---|---|
| F1 | The jobs' lists (rebuilt from the garbled table). Job 1: Ada, Bea, Cleo, Dora. Job 2: Ada, Dora, Cleo, Bea. Job 3: Ada, Cleo, Bea, Dora. Job 4: Ada, Bea, Cleo, Dora. | 337 to 358 | `JOBS` below |
| F2 | The candidates' lists (rebuilt). Ada: 1, 3, 2, 4. Bea: 4, 3, 2, 1. Cleo: 2, 3, 1, 4. Dora: 3, 4, 2, 1. | 359 to 380 | `CANDS` below |
| F3 | There are exactly two stable matchings. First (M): Job 1 with Ada, Job 2 with Dora, Job 3 with Cleo, Job 4 with Bea. Second (M'): Job 1 with Ada, Job 2 with Cleo, Job 3 with Dora, Job 4 with Bea. | 381 to 382 | `STABLE == [M2, M1]` over all 24 matchings |
| F4 | Job 2's first choice is Ada, but there is no stable matching in which Job 2 is paired with Ada; its best stable outcome is Dora. | 384 to 388 | `all(m[2] != "Ada" for m in STABLE)` and `OPT_C[2] == "Dora"` |
| F5 | Definition 11.2: the optimal candidate for a job J is the highest-ranked candidate on J's list that J is paired with in any stable matching. | 391 to 394 | stated |
| F6 | Optimal candidates here: Job 1 Ada, Job 2 Dora, Job 3 Cleo, Job 4 Bea. A stable matching in which every job has its optimal candidate is called job optimal (employer optimal); here M is one. | 395 to 401 | `OPT_C == M1` |
| F7 | Definition 11.3: the optimal job for a candidate C is the highest-ranked job on C's list that C is paired with in any stable matching. The matching in which every candidate has her optimal job is candidate optimal; here it is M'. | 402 to 412 | `OPT_J == {c: j for j, c in M2.items()}` |
| F8 | The pessimal candidate for a job is the lowest-ranked candidate it is paired with in any stable matching; job pessimal and candidate pessimal matchings are defined in the same way. Here M is candidate pessimal. | 413 to 415 | `PESS_J == {c: j for j, c in M1.items()}` |
| F9 | Is there always a stable matching in which every job has its optimal candidate? (Asked, not answered, in this range.) | 397 to 399 | answered in episode 9 |

```python
from itertools import permutations
JOBS = {1: ["Ada", "Bea", "Cleo", "Dora"], 2: ["Ada", "Dora", "Cleo", "Bea"],
        3: ["Ada", "Cleo", "Bea", "Dora"], 4: ["Ada", "Bea", "Cleo", "Dora"]}
CANDS = {"Ada": [1, 3, 2, 4], "Bea": [4, 3, 2, 1], "Cleo": [2, 3, 1, 4], "Dora": [3, 4, 2, 1]}
M1 = {1: "Ada", 2: "Dora", 3: "Cleo", 4: "Bea"}     # the first, M, green
M2 = {1: "Ada", 2: "Cleo", 3: "Dora", 4: "Bea"}     # the second, M', purple

def rogue(m):
    has = {c: j for j, c in m.items()}
    return [(j, c) for j in JOBS for c in JOBS[j][:JOBS[j].index(m[j])]
            if CANDS[c].index(j) < CANDS[c].index(has[c])]

STABLE = [m for m in (dict(zip(JOBS, p)) for p in permutations(CANDS)) if not rogue(m)]
assert STABLE == [M2, M1] and len(list(permutations(CANDS))) == 24
assert all(m[1] == "Ada" and m[4] == "Bea" and m[2] != "Ada" for m in STABLE)
OPT_C = {j: min((m[j] for m in STABLE), key=JOBS[j].index) for j in JOBS}
OPT_J = {c: min((j for m in STABLE for j in m if m[j] == c), key=CANDS[c].index) for c in CANDS}
PESS_J = {c: max((j for m in STABLE for j in m if m[j] == c), key=CANDS[c].index) for c in CANDS}
assert OPT_C == M1 and OPT_C[2] == "Dora"
assert OPT_J == {c: j for j, c in M2.items()}
assert PESS_J == {c: j for j, c in M1.items()}
# positions used in the narration (1 = first name on the list)
pos = lambda lists, who, x: lists[who].index(x) + 1
assert [pos(JOBS, 2, "Dora"), pos(JOBS, 2, "Cleo")] == [2, 3]
assert [pos(JOBS, 3, "Cleo"), pos(JOBS, 3, "Dora")] == [2, 4] and pos(JOBS, 4, "Bea") == 2
assert [pos(CANDS, "Cleo", 3), pos(CANDS, "Cleo", 2)] == [2, 1]
assert [pos(CANDS, "Dora", 2), pos(CANDS, "Dora", 3)] == [3, 1]
assert pos(CANDS, "Ada", 1) == 1 and pos(CANDS, "Bea", 4) == 1
```

## Added to the notes

The notes assert "there are exactly two stable matchings" and leave three concept
checks open. The episode derives all of it.

| Beat | The step that was missing | Why it holds |
|---|---|---|
| 2.1 | Why Job 1 and Ada are together in every stable matching. | They are first on each other's lists; apart, each prefers the other to its partner, a rogue couple. |
| 2.2 | Why Job 2 can never have Ada (the notes say "so low on A's preference list, and other jobs also prefer A"). | Ada is always with Job 1 (beat 2.1). |
| 2.3 | Why Job 4 and Bea are together in every stable matching. | With Ada taken, Job 4's partner, if not Bea, is Cleo or Dora, both below Bea on its list; Bea, if not with Job 4, has a job below her first choice. So apart they are a rogue couple. |
| 2.4 | Why there are at most two stable matchings. | Two jobs (2 and 3) and two candidates (Cleo, Dora) remain, and two things can be paired with two things in two ways. |
| 2.5 | That the first is stable. | Jobs 2, 3 and 4 have row 2 of their lists; the only name above is Ada, who has her first choice. |
| 2.6 | That the second is stable. | Job 2 has Cleo and prefers Ada, Dora; Job 3 has Dora and prefers Ada, Cleo, Bea; Ada, Dora, Cleo, Bea all have their first choice in this matching. |
| 3.2 | The answer to the concept check "who are the optimal candidates for each job". | F6, read off the green and purple cells: in each job column the green cell is above the purple one or they are the same cell. |
| 3.3, 3.4 | The answer to the concept check "M' is candidate optimal". | In Cleo's and Dora's columns the purple cell is row 1; Ada and Bea have the same job in both. |
| 3.4 | That the first matching is candidate pessimal (the notes ask the reader to define it). | In each candidate column the green cell is below the purple one or the same cell, and there are only these two stable matchings. |

## Left out, and why

| Item of the notes | Line | Reason |
|---|---|---|
| "But is this so impressive? Will your employment system really be successful..." | 331 to 334 | Motivation in the notes' voice; beat 1.1 gives the motive from episode 3. |
| The names "employer optimal" and "job/employer optimal" | 399 to 400 | One name per thing: "job optimal". |
| The job pessimal matching by name | 414 to 415 | The episode shows one pessimal case (the candidates); the mirror case adds a word and no idea. It is the purple matching here. |
| "Who is better off in the Propose-and-Reject Algorithm?" | 416 to 417 | It is the closing question (beat 3.5) and the subject of episode 9. |

## Layout used by every scene

One stage, built in `hook` and kept to the end. Nothing but the scene heading is above
y = 2.7; nothing is below y = -2.7.

Colours: job blue `BLUE_C`; candidate gold `GOLD_C`; plain cell border `GREY_B` width
2; "partner in both stable matchings" `YELLOW_D`; "partner in the first" `GREEN_C`;
"partner in the second" `PURPLE_B`.

Four columns at x = -4.2, -1.4, 1.4, 4.2. Every box is 2.4 wide.

Top half, the jobs: headers `box_label(name, BLUE_C, w=2.4, h=0.5, font_size=22)` at
y = 2.42; under each four cells `Rectangle(width=2.4, height=0.42)`, border `GREY_B`
width 2, at y = 1.93 (row 1), 1.49 (row 2), 1.05 (row 3), 0.61 (row 4), names `txt(name, 20)`.

| column | header | row 1 | row 2 | row 3 | row 4 |
|---|---|---|---|---|---|
| x = -4.2 | Job 1 | Ada | Bea | Cleo | Dora |
| x = -1.4 | Job 2 | Ada | Dora | Cleo | Bea |
| x = 1.4 | Job 3 | Ada | Cleo | Bea | Dora |
| x = 4.2 | Job 4 | Ada | Bea | Cleo | Dora |

Bottom half, the candidates: headers `box_label(name, GOLD_C, w=2.4, h=0.5, font_size=22)`
at y = -0.65; under each four cells of the same size at y = -1.14 (row 1), -1.58 (row 2),
-2.02 (row 3), -2.46 (row 4).

| column | header | row 1 | row 2 | row 3 | row 4 |
|---|---|---|---|---|---|
| x = -4.2 | Ada | Job 1 | Job 3 | Job 2 | Job 4 |
| x = -1.4 | Bea | Job 4 | Job 3 | Job 2 | Job 1 |
| x = 1.4 | Cleo | Job 2 | Job 3 | Job 1 | Job 4 |
| x = 4.2 | Dora | Job 3 | Job 4 | Job 2 | Job 1 |

The gap between the halves (y from 0.40 down to -0.40) holds only lines, never text. Lines have width 4.

| name | pair | colour | from (x, y) | to (x, y) |
|---|---|---|---|---|
| K1 | Job 1 and Ada | `YELLOW_D` | (-4.2, 0.36) | (-4.2, -0.36) |
| K4 | Job 4 and Bea | `YELLOW_D` | (4.2, 0.36) | (-1.0, -0.36) |
| A2 | Job 2 and Dora | `GREEN_C` | (-1.4, 0.36) | (4.6, -0.36) |
| A3 | Job 3 and Cleo | `GREEN_C` | (1.0, 0.36) | (1.0, -0.36) |
| B2 | Job 2 and Cleo | `PURPLE_B` | (-1.4, 0.36) | (1.8, -0.36) |
| B3 | Job 3 and Dora | `PURPLE_B` | (1.8, 0.36) | (4.6, -0.36) |

A2 and A3 are removed before B2 and B3 are drawn.

Left strip (x = -6.15, every text at most 1.2 wide, scale down if wider):
`txt("jobs", 18, GREY_B)` at (-6.15, 2.42); `txt("candidates", 18, GREY_B)` at (-6.15, -0.65);
slot LJ at (-6.15, 1.3), size 18; slot LC1 at (-6.15, -1.4) and slot LC2 at (-6.15, -1.7), size 18; slot LP at (-6.15, -2.3), size 18.

Right strip (x = 6.15, every text at most 1.2 wide). Legend (appears in beat 2.6): a
square of side 0.28 with `YELLOW_D` border width 4 at (6.15, 1.95) and `txt("both", 18, YELLOW_D)`
at (6.15, 1.65); a `GREEN_C` square at (6.15, 1.30) and `txt("first", 18, GREEN_C)` at
(6.15, 1.00); a `PURPLE_B` square at (6.15, 0.65) and `txt("second", 18, PURPLE_B)` at (6.15, 0.35).
Slot RS at (6.15, -1.4), size 18.

Rules for the builder that come from the check script:
- To highlight a cell, change the stroke of the cell's own rectangle (`set_stroke(colour, 4)`). Never put a second rectangle on top.
- Never draw a line through a name.
- "Flash" means `Indicate(obj, color=YELLOW_D, scale_factor=1.1)`; the object returns to the look it had.
- "Out of reach" is shown by fading a cell and its name to opacity 0.25.

## Scene `hook`: heading "Four jobs, four candidates"

Stage: empty at the start, built in beats 1.1 and 1.2.
Kept from the scene before: nothing. Removed at the end: nothing.

### 1.1
> In episode three one set of lists had two stable matchings, so stable alone does not
> pick a winner. To see what separates them, here is a slightly bigger example. There
> are four jobs, numbered one to four, and four candidates, Ada, Bea, Cleo and Dora.

- with the first word: the strip labels "jobs" and "candidates" appear.
- on "four jobs": the four job headers appear, left to right.
- on "four candidates": the four candidate headers appear, left to right.
- uses: episode 3 beat 3.5, F1, F2.

### 1.2
> Each column shows a list, most wanted first as always. Notice that every job puts Ada
> at the top, and that the favourite of Ada is job one.

- with the first word: the sixteen job cells with their names appear, column by column, then the sixteen candidate cells with their names.
- on "every job puts Ada": flash row 1 of the four job columns together.
- on "is job one": flash row 1 of the Ada column (Job 1).
- uses: F1, F2.

## Scene `find`: heading "Which matchings are stable?"

Stage: the layout as built. This scene adds the gap lines, coloured borders and the legend.
Kept from the scene before: everything.
Removed at the end: hold until the voice has finished beat 2.6, then remove the lines
K1, K4, B2, B3 and the text in slot RS. All coloured borders, the faded cells and the legend stay.

### 2.1
> Let us hunt for the stable matchings, starting with job one and Ada, who are first on
> each other's lists. If they were not together, each would prefer the other to its
> partner, and they would be a rogue couple. So every stable matching pairs job one with
> Ada.

- with the first word: flash the headers "Job 1" and "Ada".
- on "first on": row 1 of the Job 1 column (Ada) and row 1 of the Ada column (Job 1) get a `YELLOW_D` border, width 4.
- on "a rogue couple": flash those two cells together.
- on "every stable matching": the line K1 is drawn.
- uses: the lists on screen, episode 3 (rogue couple). The step is in "Added to the notes".

### 2.2
> That already tells us something about job two. Its first choice is Ada as well, but in
> a stable matching Ada is always taken by job one. So the top of a list is not always a
> realistic hope.

- with the first word: flash the header "Job 2".
- on "Its first choice is Ada": flash row 1 of the Job 2 column (Ada).
- on "always taken": row 1 (Ada) of the Job 2, Job 3 and Job 4 columns fades to opacity 0.25, cell and name.
- on "realistic hope": flash the header "Job 2".
- uses: beat 2.1, F4.

### 2.3
> With Ada out of reach, look at job four. Its next name is Bea, and the favourite of Bea
> is job four. Apart, job four would have someone below Bea, and Bea would have a job
> below her favourite. So job four and Bea are together in every stable matching as
> well.

- with the first word: flash the header "Job 4".
- on "Its next name is Bea": row 2 of the Job 4 column (Bea) and row 1 of the Bea column (Job 4) get a `YELLOW_D` border, width 4.
- on "someone below Bea": flash rows 3 and 4 of the Job 4 column (Cleo, Dora).
- on "below her favourite": flash rows 2, 3 and 4 of the Bea column.
- on "are together": the line K4 is drawn.
- uses: beat 2.2 (Ada is out of reach), the lists on screen.

### 2.4
> That leaves jobs two and three with Cleo and Dora, and they can be paired in only two
> ways. Either job two takes Dora and job three takes Cleo, or the other way round.

- with the first word: flash the headers "Job 2", "Job 3", "Cleo", "Dora" together.
- on "job two takes Dora": the lines A2 and A3 are drawn; `GREEN_C` border, width 4, on row 2 of the Job 2 column (Dora), row 2 of the Job 3 column (Cleo), row 2 of the Cleo column (Job 3) and row 3 of the Dora column (Job 2).
- on "the other way round": flash the headers "Cleo" and "Dora".
- uses: beats 2.1 and 2.3 (two pairs are fixed).

### 2.5
> Is the first way stable? Jobs two, three and four each have the second name on their
> lists, and the only name above it is Ada. Ada has her favourite and will not move, so
> there is no rogue couple.

- with the first word: flash the lines A2 and A3.
- on "the second name on their lists": flash row 2 of the Job 2, Job 3 and Job 4 columns together.
- on "the only name above it": flash the three faded Ada cells (row 1 of the Job 2, Job 3, Job 4 columns).
- on "no rogue couple": the text `txt("stable", 18, GREEN_C)` appears in slot RS.
- uses: beat 2.4, beat 2.1 (Ada has Job 1), episode 3 beat 3.1 (the method).

### 2.6
> Now the other way round, where job two has Cleo and job three has Dora. Job two would
> rather have Dora, and job three would rather have Cleo or Bea. But Dora, Cleo and Bea
> each have their favourite job here, so none of them would move. Both matchings are
> stable, and they are the only ones.

- with the first word: the lines A2 and A3 are removed and the text in slot RS fades out (the green borders stay).
- on "job two has Cleo": the lines B2 and B3 are drawn; `PURPLE_B` border, width 4, on row 3 of the Job 2 column (Cleo), row 4 of the Job 3 column (Dora), row 1 of the Cleo column (Job 2) and row 1 of the Dora column (Job 3).
- on "would rather have Dora": flash row 2 of the Job 2 column (Dora), then rows 2 and 3 of the Job 3 column (Cleo, Bea).
- on "their favourite job": flash row 1 of the Dora, Cleo and Bea columns together.
- on "the only ones": the text `txt("stable", 18, PURPLE_B)` appears in slot RS, and the legend (three squares, three words) appears in the right strip.
- uses: beat 2.4, the lists on screen, F3.
- end of scene: hold until the voice has finished this beat, then remove K1, K4, B2, B3 and the text in slot RS.

State of the stage at the end of `find`: yellow borders on Job 1 row 1, Job 4 row 2,
Ada row 1, Bea row 1; green borders on Job 2 row 2, Job 3 row 2, Cleo row 2, Dora row 3;
purple borders on Job 2 row 3, Job 3 row 4, Cleo row 1, Dora row 1; the Ada cells of the
Job 2, Job 3, Job 4 columns faded; legend on; gap empty.

## Scene `best`: heading "Best for whom?"

Stage: as at the end of `find`. This scene adds texts in the left strip and in slot RS.
Kept from the scene before: everything listed in the state above.
Removed at the end: nothing (the end card follows).

### 3.1
> Now compare the two through the eyes of job two. In the first matching it has Dora,
> the second name on its list, and in the second matching it has Cleo, the third. Dora
> is the best partner job two has in any stable matching, and we call her its optimal
> candidate.

- with the first word: flash the header "Job 2".
- on "it has Dora": flash row 2 of the Job 2 column (Dora, green).
- on "it has Cleo": flash row 3 of the Job 2 column (Cleo, purple).
- on "optimal": the text `txt("optimal", 18, GREEN_C)` appears in slot LJ.
- uses: the green and purple cells on screen, F3, F5.

### 3.2
> Do the same for the other jobs. Job one has Ada and job four has Bea in both, and job
> three is better off with Cleo than with Dora. So the first matching gives every job
> its optimal candidate at once, and such a matching is called job optimal.

- with the first word: nothing new.
- on "Job one has Ada": flash row 1 of the Job 1 column and row 2 of the Job 4 column (both yellow).
- on "better off with Cleo": flash row 2 of the Job 3 column (Cleo, green), then row 4 (Dora, purple).
- on "called job optimal": the text in slot LJ changes to `txt("job optimal", 18, GREEN_C)`.
- uses: beat 3.1, the cells on screen, F6.

### 3.3
> Now take the side of the candidates. Cleo has job three in the first matching and job
> two in the second, and job two is higher on her list. Dora has job two in the first
> and job three in the second, and job three is higher on hers.

- with the first word: flash the four candidate headers together.
- on "Cleo has job three": flash row 2 of the Cleo column (Job 3, green), then row 1 (Job 2, purple).
- on "Dora has job two": flash row 3 of the Dora column (Job 2, green), then row 1 (Job 3, purple).
- uses: the green and purple cells on screen, F2, F3.

### 3.4
> So the second matching gives every candidate her best stable job, and it is called
> candidate optimal. And the first matching gives Cleo and Dora the lowest job they have
> in any stable matching. The word for that is pessimal.

- with the first word: flash row 1 of the four candidate columns together (two yellow, two purple).
- on "candidate optimal": `txt("candidate", 18, PURPLE_B)` appears in slot LC1 and `txt("optimal", 18, PURPLE_B)` in slot LC2.
- on "the lowest job": flash row 2 of the Cleo column and row 3 of the Dora column together (both green).
- on "pessimal": the text `txt("pessimal", 18, GREEN_C)` appears in slot LP.
- uses: beat 3.3, F7, F8. Ada and Bea have the same job in both stable matchings.

### 3.5
> So here the matching that is optimal for the jobs is pessimal for the candidates. Is
> that an accident of these lists, or a law? Can every job always get its optimal
> candidate at once? And which of the two does propose and reject produce?

- with the first word: nothing new.
- on "optimal for the jobs": flash the text in slot LJ.
- on "pessimal for the candidates": flash the text in slot LP.
- on "propose and reject": the text `txt("which one?", 18, YELLOW_D)` appears in slot RS.
- uses: beats 3.2 and 3.4, F9. Nothing is answered here; episodes 9 and 10 answer all three questions.

## End card

- The optimal candidate of a job is the best partner it has in any stable matching, which need not be the top of its list.
- A stable matching that gives every job its optimal candidate is job optimal; one that gives every candidate her optimal job is candidate optimal.
- Pessimal means the worst partner in any stable matching.
- In this example there are exactly two stable matchings: one is job optimal and candidate pessimal, the other is candidate optimal.

## Author's check, each answered yes

- The first beat shows one concrete case before any definition. Yes: four jobs and four candidates with their lists.
- Every "uses" line names an earlier beat, a fact row, or what is on the screen. Yes.
- A name is introduced after the beat where the viewer sees it happen. Yes: "optimal candidate" in 3.1 after both partners of Job 2 were seen; "pessimal" last in 3.4.
- Every beat has a drawn object that changes; no beat is words on an empty stage. Yes.
- Every phrase after "on" is copied from its own beat, and appears there once. Yes, checked by script.
- A beat over fourteen seconds has at least two changes, over twenty-six at least three. Yes, checked by script.
- If the voice counts things, the stage shows exactly that many. Yes: four job headers, four candidate headers, two matchings in two colours.
- No step is skipped, and every step the notes left out is in "Added to the notes". Yes.
- Every item of the notes in the source range is in a beat or in "Left out". Yes.
- Narration: 13 beats, two to four sentences each, no sentence over 25 words, no beat over 60 words, no digit, colon or symbol. Yes, checked by script.
