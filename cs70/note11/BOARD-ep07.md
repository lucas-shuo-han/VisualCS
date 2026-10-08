# BOARD: episode 07, Always a Stable Matching

Source: `notes.txt` lines 305 to 328. Language: en. Aim: 5 to 6 minutes (about 730 words).
File `ep07_always_stable.py`, class `Ep07AlwaysStable`. Scenes, in order: `worry`, `hands`, `stable`, `general`.

The builder copies every narration line (the lines that start with a greater-than sign)
into a `say()` unchanged, one beat per `say()`, and builds exactly the stage described.
It decides nothing; an unclear line is a question in its report.

Format, read by `check.py`: a line that starts with three hash signs opens a beat, and
every line after it that starts with a greater-than sign is that beat's narration.
Neither is used anywhere else in this file.

## Facts

| id | Fact, with all its conditions | Notes line | Computed how |
|---|---|---|---|
| F1 | The rules of propose and reject (morning, afternoon, evening, stop), as in episode 1. In particular each job makes one offer a morning, each candidate keeps one offer, and a job crosses off only a candidate who refused it. | 63 to 72 | stated |
| F2 | The run of episode 1: Control was refused by Anita on day one and by Bridget on day two, and ended with Christine; the output is Approximation with Anita, Basis with Bridget, Control with Christine. | 75 to 100 | `CROSSED` and `RESULT` below |
| F3 | Improvement Lemma (Lemma 11.2): if a job makes an offer to a candidate on some day, then at the end of that day and of every later day she holds that job or one she likes more. | 255 to 256 | episode 5 |
| F4 | Lemma 11.3: the propose-and-reject algorithm always terminates with a matching. Proof of the notes: suppose a job J is unpaired at the end; it was rejected by all n candidates; by the Improvement Lemma each of them had a better offer in hand; so n candidates have n jobs in hand, not including J; that is n + 1 jobs; contradiction. | 310 to 316 | checked on all 46656 instances with three jobs and three candidates: `never_exhausted and always_matching` |
| F5 | Theorem 11.1: the matching produced by the algorithm is always stable. Proof of the notes: take a couple (J, C) of the final matching and a candidate C* that J prefers to C. C* is before C on J's list, so J made an offer to C* before C. By the Improvement Lemma C* likes her final job at least as much as J, and therefore prefers it to J. So no job is in a rogue couple. | 319 to 328 | checked on all 46656 instances: `always_stable` |
| F6 | Lists of the example. Control: Anita, Bridget, Christine. Approximation: Anita, Bridget, Christine. Basis: Bridget, Anita, Christine. Anita: Basis, Approximation, Control. Bridget: Approximation, Basis, Control. Christine: Approximation, Basis, Control. | 17 to 44 | `JOBS`, `CANDS` below |
| F7 | In the output Anita holds Approximation and Bridget holds Basis; each of them ranks that job above Control. | from F2, F6 | `CANDS["Anita"].index("Approximation") < CANDS["Anita"].index("Control")` and the same for Bridget with Basis |
| F8 | A stable matching always exists (for jobs and candidates), because the algorithm always outputs one. | 240 to 242 | from F4, F5 |
| F9 | Three jobs without Control are two jobs. | | `3 - 1 == 2` |

```python
from itertools import permutations, product
JOBS = {"Approximation": ["Anita", "Bridget", "Christine"],
        "Basis":         ["Bridget", "Anita", "Christine"],
        "Control":       ["Anita", "Bridget", "Christine"]}
CANDS = {"Anita":     ["Basis", "Approximation", "Control"],
         "Bridget":   ["Approximation", "Basis", "Control"],
         "Christine": ["Approximation", "Basis", "Control"]}

def run(jobs, cands):
    """Returns (result job -> candidate, crossed off pairs in order, True if some list ran empty)."""
    left = {j: list(l) for j, l in jobs.items()}
    crossed_all, exhausted = [], False
    while True:
        exhausted = exhausted or any(not left[j] for j in jobs)
        offers = {j: left[j][0] for j in jobs if left[j]}
        hand, crossed = {}, []
        for c in cands:
            got = [j for j in offers if offers[j] == c]
            if got:
                best = min(got, key=cands[c].index)
                hand[c] = best
                crossed += [(j, c) for j in got if j != best]
        crossed_all += crossed
        if not crossed:
            return {j: c for c, j in hand.items()}, crossed_all, exhausted
        for j, c in crossed:
            left[j].remove(c)

def rogue(jobs, cands, m):
    has = {c: j for j, c in m.items()}
    return [(j, c) for j in jobs for c in jobs[j][:jobs[j].index(m[j])]
            if cands[c].index(j) < cands[c].index(has[c])]

RESULT, CROSSED, _ = run(JOBS, CANDS)
assert RESULT == {"Approximation": "Anita", "Basis": "Bridget", "Control": "Christine"}
assert CROSSED == [("Control", "Anita"), ("Control", "Bridget")]
assert CANDS["Anita"].index("Approximation") < CANDS["Anita"].index("Control")
assert CANDS["Bridget"].index("Basis") < CANDS["Bridget"].index("Control")
assert 3 - 1 == 2

nj, nc = list(JOBS), list(CANDS)
never_exhausted = always_matching = always_stable = True
for jl in product(permutations(nc), repeat=3):
    for cl in product(permutations(nj), repeat=3):
        jobs, cands = dict(zip(nj, map(list, jl))), dict(zip(nc, map(list, cl)))
        m, _, ex = run(jobs, cands)
        never_exhausted = never_exhausted and not ex
        always_matching = always_matching and sorted(m) == sorted(nj) and sorted(m.values()) == sorted(nc)
        always_stable = always_stable and always_matching and rogue(jobs, cands, m) == []
assert never_exhausted and always_matching and always_stable
```

(The enumeration takes a few seconds. The builder may keep it in a separate check and
assert only the five lines before it in the episode file.)

## Added to the notes

| Beat | The step that was missing | Why it holds |
|---|---|---|
| 1.2, 1.3 | What "a job left unpaired" means in terms of the rules, and that the rules do not say what a job with an empty list does. The notes jump to "J must have made an offer to all n of the candidates and been rejected by all of them". | A job that still has a name asks it; a job is without an offer only when every name is crossed off, and a name is crossed off only after a refusal. The episode supposes this on some day and looks at the end of that day (the notes look at the end of the algorithm). The count is the same, and this version also shows that no list ever runs empty in the middle of a run. Reported as a tightening. |
| 1.4 | Why a candidate who refused the job holds an offer on every later day, and why that offer is from another job. The notes cite the lemma in one clause. | She refused because she kept a better offer (afternoon rule). The job asked her, so by the lemma she holds that job or better at the end of every later day. The job never asks her again after crossing her off, so what she holds is not that job. |
| 1.5 | Why n hands need n different jobs. | Each job makes one offer per morning, so it can be in at most one hand. |
| 1.6 | The count on the case with three: three hands, two other jobs. | F9. |
| 1.8 | From "no job is ever refused by everyone" to "ends with a matching". The notes stop at the contradiction. | Every job makes an offer every morning; on the last day no offer is refused, so each job is in a hand; a candidate holds one offer, so the n jobs are in n different hands; there are n candidates, so every candidate holds one. |
| 2.1 | Which pairs have to be checked at all. | A rogue couple needs a job that prefers the candidate to its partner (episode 3, beat 3.1). Approximation and Basis have their first choice. |
| 2.2 | Why "C* is before C on J's list" means that J was refused by C*. The notes say "J must have made an offer to C* before it made an offer to C". | A job asks the first name not crossed off, and a name is crossed off only by a refusal; so every name above its final partner was asked and refused. |
| 2.4 | From "at least as much as J" to "prefers it to J". The notes say "and therefore". | Her final job is not J, because J's final offer went to its partner C, a different candidate; a list has no ties, so a different job that is at least as good is strictly better. |
| 2.5 | The second pair (Control and Bridget), so that every pair of the example is checked. | F7. |
| 3.3 | That one side is enough: the notes show that no job is in a rogue couple and conclude "the matching is stable". | A rogue couple contains a job; if no job is in one, there is none. |
| 3.3 | "So a stable matching always exists." The notes say this before the proof (lines 240 to 242). | F4 and F5 together: the algorithm always ends with a matching, and it is stable. |

## Left out, and why

| Item of the notes | Line | Reason |
|---|---|---|
| "Before reading the proof, see if you can convince yourself that this is true"; "remarkably short and elegant" | 307 to 309 | Not steps. |
| The letters J, C, C* in the voice | 311 to 328 | On screen in scene `general`; the voice says "the job", "its partner", "the candidate it would rather have". |
| "all n candidates have job offers" in general n, as a formula with n + 1 | 314 to 316 | Shown with three (beat 1.6) and then said for any number (beat 1.7); the screen shows "n hands, n - 1 other jobs". |

## Layout used by every scene

Three stages. Stage one serves the scenes `worry` and `hands`; `stable` and `general` each start by removing the stage before them.
Nothing but the scene heading is above y = 2.7; nothing is below y = -2.7.

Colours, one meaning each: job blue `BLUE_C`; candidate gold `GOLD_C`; plain border
`GREY_B` width 2; in hand, partner `GREEN_C`; `ORANGE` for the pair that is being tested (the
candidate a job would rather have, that job's place on her list, and its refused ask to
her); `RED_C` only for the impossible count of beats 1.6 and 1.7; flash `YELLOW_D`.
"Crossed off" or "faded" always means: the name (and any fill) goes to the stated opacity,
and the border of the cell keeps full opacity. So a coloured border on a faded cell stays
fully visible.
Sizes: a label or a conclusion that a beat is about is size 24 or more (22 where a slot is
narrow) and sits next to its objects; no text is below size 20; no single text is wider
than 10 units (break it into two texts instead).

Stage one (scenes `worry` and `hands`).
- Control's list, left: header `box_label("Control", BLUE_C, w=2.4, h=0.55, font_size=22)` at (-5.0, 2.3); three cells `Rectangle(width=2.4, height=0.48)` at x = -5.0 and y = 1.72 (Anita), 1.20 (Bridget), 0.68 (Christine), names `txt`, 22.
- The candidates, right: headers `box_label(name, GOLD_C, w=2.4, h=0.55, font_size=22)` at y = 2.3 and x = -1.2 (Anita), 1.9 (Bridget), 5.0 (Christine). Under each a hand cell `Rectangle(width=2.4, height=0.7)` at y = 1.6, empty at first. A text in a hand cell is `txt`, size 20, at most 2.2 wide.
- Hand label, slot HL at (-3.1, 1.6), at most 1.3 wide: `txt("in hand", 20, GREY_B)` at first.
- The jobs as chips: `box_label(name, BLUE_C, w=2.4, h=0.55, font_size=22)` at y = -0.2 and x = -1.2 ("Approximation", text at most 2.0 wide), 1.9 ("Basis"), 5.0 ("Control").
- Job label, slot JL at (-3.1, -0.2), at most 1.3 wide: `txt("jobs", 20, GREY_B)` at first.
- Chip arrows, from a chip up to the hand above it, used only in beat 1.8: `Arrow((x, 0.1), (x, 1.2), buff=0, stroke_width=4, tip_length=0.18)` at x = -1.2, 1.9, 5.0, called arrow 1, 2, 3.
- Count lines, centred at x = 0, size 24, each at most 10 wide: L1 at y = -1.2, L2 at y = -1.8, L3 at y = -2.4.

Stage two (scene `stable`). The stage of episode 3, in the final state of episode 1.
- Three columns at x = -3.9, 0.5, 4.9, every box 2.4 wide, texts at most 2.0 wide.
- Job headers `box_label(name, BLUE_C, w=2.4, h=0.55, font_size=22)` at y = 2.42; cells `Rectangle(width=2.4, height=0.48)` at y = 1.86 (row 1), 1.35 (row 2), 0.84 (row 3).

| column | header | row 1 | row 2 | row 3 |
|---|---|---|---|---|
| x = -3.9 | Approximation | Anita | Bridget | Christine |
| x = 0.5 | Basis | Bridget | Anita | Christine |
| x = 4.9 | Control | Anita | Bridget | Christine |

- Candidate headers `box_label(name, GOLD_C, w=2.4, h=0.55, font_size=22)` at y = -0.85; cells at y = -1.41 (row 1), -1.92 (row 2), -2.43 (row 3).

| column | header | row 1 | row 2 | row 3 |
|---|---|---|---|---|
| x = -3.9 | Anita | Basis | Approximation | Control |
| x = 0.5 | Bridget | Approximation | Basis | Control |
| x = 4.9 | Christine | Approximation | Basis | Control |

- Final state, on the stage from the first moment of the scene: rows 1 and 2 of the Control column crossed off (names at opacity 0.25, borders at full opacity); `GREEN_C` border, width 4, on the partner cells: Approximation row 1, Basis row 1, Control row 3, Anita row 2, Bridget row 2, Christine row 3; three green lines of width 4 in the gap: E1 from (-4.3, 0.55) to (-4.3, -0.52), E2 from (0.9, 0.55) to (0.9, -0.52), E3 from (4.9, 0.55) to (4.9, -0.52).
- Left strip: `txt("jobs", 22, GREY_B)` at (-6.0, 2.42); `txt("candidates", 22, GREY_B)` at (-6.0, -0.85), each at most 1.2 wide. No other text in the strip.
- The refused ask, drawn in the gap in `ORANGE`: arrow A1 (Control to Anita) `Arrow((4.5, 0.55), (-3.5, -0.52), buff=0, color=ORANGE, stroke_width=5, tip_length=0.18)`; arrow A2 (Control to Bridget) `Arrow((4.5, 0.55), (0.1, -0.52), buff=0, color=ORANGE, stroke_width=5, tip_length=0.18)`. A1 and A2 are never on the stage together.
- Ask label: one text `txt(..., 22, ORANGE)` at (-1.7, 0.33), at most 3.0 wide. It lies in the gap above both arrows and between the lines E1 and E2, and touches neither.

Stage three (scene `general`).
- The job's list: header `box_label("job J", BLUE_C, w=2.4, h=0.55, font_size=22)` at (-4.8, 2.3); two cells 2.4 wide, 0.48 high at y = 1.72 (text "C*") and y = 1.20 (text "C", `GREEN_C` border width 4: its partner).
- The candidate's list: header `box_label("candidate C*", GOLD_C, w=2.4, h=0.55, font_size=22)` at (-1.9, 2.3); two cells at y = 1.72 (text "her final job") and y = 1.20 (text "J").
- Proof lines, `txt`, size 22, left edge at x = 0.0, at most 6.6 wide:

| line | y | text |
|---|---|---|
| Q1 | 2.3 | J would rather have C* than its partner C |
| Q2 | 1.8 | so J asked C* earlier, and she refused |
| Q3 | 1.3 | Improvement Lemma: she ends with J or better |
| Q4 | 0.8 | not J itself: J's last offer went to C |
| Q5 | 0.3 | so she likes her final job more: no rogue couple |

- Result lines, centred at x = 0, each at most 10 wide: T1 at y = -0.8, size 24; T2 at y = -1.5, size 24; T3 at y = -2.3, size 24.

Rules for the builder that come from the check script:
- To highlight a cell, change the stroke of the cell's own rectangle (`set_stroke(colour, 4)`). Never put a second rectangle on top.
- Never draw a line through a text.
- "Flash" means `Indicate(obj, color=YELLOW_D, scale_factor=1.1)`; the object returns to the look it had.
- "Reset a cell" means border `GREY_B` width 2 (the opacity of its name stays as it is).

## Scene `worry`: heading "Can a job run out of names?"

Stage: stage one. Beat 1.1 builds Control's list and the candidate headers, beat 1.3 the hand cells.
Kept from the scene before: nothing. Removed at the end: hold until the voice has
finished beat 1.3, then change the heading; nothing is removed.

### 1.1
> We know that propose and reject always stops. But stopping is not the same as
> succeeding. When it stops, is every job really paired with a candidate, and every
> candidate with a job?

- with the first word: Control's list appears (header and three cells), with rows 1 and 2 (Anita, Bridget) already crossed off (names at opacity 0.25), as in episode 1.
- on "every job really paired": row 3 (Christine) gets a `GREEN_C` border, width 4.
- on "every candidate with a job": the three candidate headers "Anita", "Bridget", "Christine" appear at the right, left to right (headers only, no hand cells yet).
- uses: episode 5 (halting), F2.

### 1.2
> Here is what could go wrong. In the first episode Control was refused by Anita and
> then by Bridget, and it ended with the last name on its list, Christine. What if
> Christine had refused it too?

- with the first word: flash the header "Control".
- on "refused by Anita": flash row 1 of Control's list and the candidate header "Anita" together.
- on "then by Bridget": flash row 2 of Control's list and the candidate header "Bridget" together.
- on "Christine had refused it too": row 3 is reset and its name fades to opacity 0.25, like the other two; flash the candidate header "Christine".
- uses: F2. The third refusal is a supposition, not a fact of the run.

### 1.3
> Then Control would have no name left, and it could never make an offer again. So let
> us suppose that this happens to some job on some day, and look closely at the end of
> that day.

- with the first word: nothing new.
- on "no name left": the header "Control" fades to opacity 0.4 (no red here: red is kept for the impossible count).
- on "the end of that day": the three empty hand cells appear under the candidate headers, with the label "in hand" in slot HL.
- uses: beat 1.2, F1 (a job asks a name that is not crossed off).
- end of scene: hold until the voice has finished this beat, then change the heading.

## Scene `hands`: heading "Three hands, two jobs"

Stage: stage one as left by `worry`. Beat 1.5 adds the chips, beats 1.6 to 1.8 the count labels and lines.
Kept from the scene before: everything. Removed at the end: hold until the voice has
finished beat 1.8, then remove everything.

### 1.4
> Each candidate who refused Control did so because she kept an offer she liked more.
> And by the improvement lemma she still holds Control or something better at the end of
> every later day. It cannot be Control itself, which she has refused, so she holds
> another job.

- with the first word: flash the three candidate headers together.
- on "kept an offer she liked more": the three hand cells get a `GREEN_C` border, width 4.
- on "improvement lemma": `txt("Control or better", 20, GREEN_C)` is written in each of the three hand cells.
- on "another job": the text in each hand cell changes to `txt("above Control", 20, GREEN_C)`.
- uses: F1 (afternoon rule), F3, beat 1.3.

### 1.5
> So at the end of that day all three candidates hold an offer, and none of the three
> offers is from Control. A job makes only one offer each morning, so three hands need
> three different jobs.

- with the first word: flash the three hand cells together.
- on "none of the three": the three job chips appear with the label "jobs" in slot JL; the chip "Control" is at opacity 0.25 from the start.
- on "three different jobs": the label in slot HL changes to `txt("3 hands", 24)`; flash the three hand cells one after another, left to right.
- uses: beat 1.4, F1 (one offer per job and morning).

### 1.6
> But without Control only two jobs are left, Approximation and Basis. Two jobs cannot
> fill three hands. So the day we supposed can never come, and Control cannot be refused
> by everyone.

- with the first word: flash the faded chip "Control".
- on "Approximation and Basis": flash the chips "Approximation" and "Basis" together; the label in slot JL changes to `txt("2 jobs", 24)`.
- on "cannot fill three hands": the labels "3 hands" and "2 jobs" both turn `RED_C`.
- on "can never come": line L1 appears: `txt("3 hands need 3 jobs, but only 2 are left", 24, RED_C)`.
- uses: beat 1.5, F9. No arrows are drawn from chips to hands here: the argument is the count, not who holds whom.

### 1.7
> The same count works for any number of jobs. A job refused by everyone would leave one
> job fewer than there are candidates, while every candidate holds an offer of her own.
> So no job ever runs out of names.

- with the first word: nothing new.
- on "any number of jobs": the label in slot HL changes to `txt("n hands", 22, RED_C)`, the label in slot JL to `txt("n - 1 jobs", 22, RED_C)`, and line L1 to `txt("n hands need n jobs, but only n - 1 are left", 24, RED_C)`.
- on "one job fewer": flash the faded chip "Control".
- on "runs out of names": line L2 appears: `txt("so no job is ever refused by every candidate", 24)`.
- uses: beats 1.4 to 1.6 (nothing in them used the number three except the count), F4.

### 1.8
> So every morning every job has someone to ask. On the last day nobody is refused, so
> every job's offer is in the hand of some candidate. No candidate holds two offers, and
> there are as many candidates as jobs, so everyone is paired. Propose and reject always
> ends with a matching.

- with the first word: the supposition is taken back, all in one animation: line L1 turns `GREY_B`, and L1 and L2 fade to opacity 0.3; the label in slot HL changes back to `txt("in hand", 20, GREY_B)` and the label in slot JL back to `txt("jobs", 20, GREY_B)`; row 3 of Control's list returns to full opacity with a `GREEN_C` border; the header "Control" and the chip "Control" return to full opacity; the texts in the three hand cells fade out (the cells keep their green borders).
- on "nobody is refused": the arrows 1, 2 and 3 grow in `GREEN_C`, each from a chip to the hand above it; the hand cells get the texts "Approximation" (Anita), "Basis" (Bridget), "Control" (Christine), `txt`, 20. This is the real result of episode 1.
- on "holds two offers": flash the three hand cells together.
- on "ends with a matching": line L3 appears: `txt("Lemma 11.3: it always ends with a matching", 24, YELLOW_D)`.
- uses: beat 1.7, F1 (stop rule, one offer in hand), F2 (the real result), F4.
- end of scene: hold until the voice has finished this beat, then remove everything.

## Scene `stable`: heading "Is the result stable?"

Stage: stage two, on the stage in its final state with the first word of beat 2.1.
Kept from the scene before: nothing. Removed at the end: hold until the voice has
finished beat 2.5, then remove everything.

### 2.1
> Now the main question, whether that matching is stable. Here is the result of the
> first episode, with the two names that Control crossed off shown faded. Approximation
> and Basis have their first choices, so the only job that would rather have someone
> else is Control.

- with the first word: the whole of stage two appears in its final state.
- on "shown faded": flash rows 1 and 2 of the Control column (they stay faded).
- on "have their first choices": flash row 1 of the Approximation column and row 1 of the Basis column (both green).
- on "is Control": flash the header "Control".
- uses: F2, F6, episode 3 beat 3.1 (only names above the partner matter).

### 2.2
> Control would rather have Anita, who is above its partner Christine. Now, why is Anita
> above Christine and yet not its partner? A job works down its list, and it only moves
> past a name when that name has refused it. So Control asked Anita on an earlier day,
> and she said no.

- with the first word: nothing new.
- on "would rather have Anita": row 1 of the Control column (Anita) gets an `ORANGE` border, width 4, at full opacity; only its name stays at opacity 0.25.
- on "works down its list": flash rows 1, 2 and 3 of the Control column one after another, from the top.
- on "she said no": the orange arrow A1 grows in the gap from the Control column to the candidate header "Anita", and the ask label `txt("day one: asked, refused", 22, ORANGE)` appears at (-1.7, 0.33), above the arrow.
- uses: F1 (morning and evening rule), F2. The step is in "Added to the notes".

### 2.3
> Now the improvement lemma speaks. From the day Control asked her, Anita holds Control
> or something better at the end of every day, and that includes the last day.

- with the first word: flash the header "Anita".
- on "the day Control asked her": row 3 of the Anita column (Control) gets an `ORANGE` border, width 4.
- on "or something better": flash rows 3, 2 and 1 of the Anita column one after another, from the bottom.
- on "the last day": flash row 2 of the Anita column (Approximation, green).
- uses: beat 2.2 (Control asked her), F3.

### 2.4
> And on the last day she does not hold Control, because Control's last offer went to
> Christine. So what Anita holds at the end is a job she likes more than Control, and
> she has no wish to leave it. Control and Anita are not a rogue couple.

- with the first word: nothing new.
- on "went to": flash the line E3 (Control to Christine).
- on "likes more than Control": flash row 2 of the Anita column (Approximation, green), which is above row 3 (Control, orange).
- on "not a rogue couple": row 1 of the Control column and row 3 of the Anita column are reset, and the arrow A1 and the ask label fade out and are removed.
- uses: beat 2.3, the lists on screen, F7.

### 2.5
> Bridget is the other name above Christine, and the same steps apply to her. Control
> asked her on day two and she refused, so she ends with Control or better. It is not
> Control, so it is Basis, which is higher on her list.

- with the first word: row 2 of the Control column (Bridget) gets an `ORANGE` border, width 4, at full opacity; only its name stays at opacity 0.25.
- on "asked her on day two": the orange arrow A2 grows in the gap from the Control column to the candidate header "Bridget", and the ask label `txt("day two: asked, refused", 22, ORANGE)` appears at (-1.7, 0.33).
- on "ends with Control or better": row 3 of the Bridget column (Control) gets an `ORANGE` border, width 4; flash rows 3, 2 and 1 of the Bridget column from the bottom.
- on "higher on her list": flash row 2 of the Bridget column (Basis, green); then row 2 of the Control column and row 3 of the Bridget column are reset, and the arrow A2 and the ask label fade out and are removed.
- uses: beats 2.2 to 2.4, F2, F7.
- end of scene: hold until the voice has finished this beat, then remove everything.

## Scene `general`: heading "Any job, any candidate"

Stage: stage three, built in beat 3.1 from an empty stage.
Kept from the scene before: nothing. Removed at the end: nothing (the end card follows).

### 3.1
> Nothing in those steps used the names. Take any job with its final partner, and any
> candidate the job would rather have. She stands above the partner on its list, so the
> job asked her on an earlier day and she refused.

- with the first word: the job's list (header "job J", cells "C*" and "C", the cell "C" green) and the candidate's list (header "candidate C*", cells "her final job" and "J") appear.
- on "would rather have": the cell "C*" in the job's list gets an `ORANGE` border, width 4; proof line Q1 appears.
- on "she refused": the text "C*" in the job's list goes to opacity 0.4 (still readable); its `ORANGE` border stays at full opacity; proof line Q2 appears.
- uses: beats 2.2 and 2.5 (the same step with names), F5.

### 3.2
> By the improvement lemma she ends with that job or a better one. It is not that job,
> because its last offer went to its partner. So she ends with a job she likes more, and
> she will not leave it.

- with the first word: nothing new.
- on "improvement lemma": the cell "J" in the candidate's list gets an `ORANGE` border, width 4; proof line Q3 appears.
- on "went to its partner": flash the green cell "C" in the job's list; proof line Q4 appears.
- on "she will not leave": the cell "her final job" in the candidate's list gets a `GREEN_C` border, width 4; proof line Q5 appears.
- uses: beats 2.3 and 2.4, F3, F5.

### 3.3
> A rogue couple needs a job and a candidate who both want to switch, and here the
> candidate never does. So the result of propose and reject has no rogue couple, which
> means it is always stable. And so a stable matching always exists, which the roommates
> could not promise.

- with the first word: nothing new.
- on "never does": flash proof line Q5.
- on "always stable": result line T1 appears: `txt("Theorem 11.1: the result of propose and reject is always stable", 24, YELLOW_D)`.
- on "always exists": result line T2 appears: `txt("so a stable matching always exists", 24)`.
- uses: beats 3.1 and 3.2, beat 1.8 (it is a matching), F5, F8, episode 4.

### 3.4
> But in episode three one set of lists had two stable matchings. So which one does
> propose and reject choose, and who is it good for? That is where we go next.

- with the first word: nothing new.
- on "two stable matchings": flash result line T2.
- on "which one": result line T3 appears: `txt("which stable matching, and good for whom?", 24, YELLOW_D)`.
- uses: episode 3 beat 3.5. Nothing is answered here; episodes 8 and 9 answer it.

## End card

- No job is ever refused by every candidate, because the candidates' hands would need more jobs than there are.
- So propose and reject always ends with a matching (Lemma 11.3).
- Every candidate a job would rather have has refused it, and by the Improvement Lemma she ends with a job she likes more.
- So the result is always stable (Theorem 11.1), and a stable matching always exists.

## Author's check, each answered yes

- The first beat shows one concrete case before any definition. Yes: Control's list from episode 1.
- Every "uses" line names an earlier beat, a fact row, or what is on the screen. Yes.
- A name is introduced after the beat where the viewer sees it happen. Yes: the lemma and the theorem are named after their arguments (1.8, 3.3).
- Every beat has a drawn object that changes; no beat is words on an empty stage. Yes.
- Every phrase after "on" is copied from its own beat, and appears there once. Yes, checked by script.
- A beat over fourteen seconds has at least two changes, over twenty-six at least three. Yes, checked by script.
- If the voice counts things, the stage shows exactly that many. Yes: three hands, two unfaded chips in 1.6.
- No step is skipped, and every step the notes left out is in "Added to the notes". Yes.
- Every item of the notes in the source range is in a beat or in "Left out". Yes.
- Narration: 17 beats in four scenes, two to four sentences each, no sentence over 25 words, no beat over 60 words, no digit, colon or symbol. Yes, checked by script.
