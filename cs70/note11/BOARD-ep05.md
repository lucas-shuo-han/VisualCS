# BOARD: episode 05, Offers Only Get Better

Source: `notes.txt` lines 133 to 142 and 243 to 266. Language: en. Aim: 5 minutes (about 690 words).
File `ep05_improvement_lemma.py`, class `Ep05ImprovementLemma`. Scenes, in order: `hook`, `anita`, `proof`.

The builder copies every narration line (the lines that start with a greater-than sign)
into a `say()` unchanged, one beat per `say()`, and builds exactly the stage described.
It decides nothing; an unclear line is a question in its report.

Format, read by `check.py`: a line that starts with three hash signs opens a beat, and
every line after it that starts with a greater-than sign is that beat's narration.
Neither is used anywhere else in this file.

## Facts

| id | Fact, with all its conditions | Notes line | Computed how |
|---|---|---|---|
| F1 | Two properties are to be shown about propose and reject: it halts, and it outputs a stable matching. | 135 to 136 | stated |
| F2 | The rules. Morning: each job makes an offer to the most preferred candidate on its list who has not yet rejected it. Afternoon: each candidate keeps the offer she likes best among those she got that morning ("in hand") and rejects the others. Evening: each rejected job crosses the candidate who rejected it off its list. Stop: on the first day on which no offer is rejected. | 63 to 72 | stated |
| F3 | In the run of episode 1 the algorithm stopped on day three; Control crossed off Anita in the evening of day one and Bridget in the evening of day two; nothing else was crossed off. | 75 to 98 | `CROSSED == [("Control", "Anita"), ("Control", "Bridget")]` and `len(DAYS) == 3` |
| F4 | Three jobs with three names each have nine names in all; n jobs with n names each have n times n. | 141 | `3 * 3 == 9` |
| F5 | Lemma 11.1: the propose-and-reject algorithm always halts. Proof of the notes: on each day that the algorithm does not halt, at least one job eliminates a candidate from its list; there are n lists of n elements; so it terminates in at most n squared days. | 138 to 142 | checked for every one of the 46656 instances with three jobs and three candidates: `max_refusal_days <= 9` |
| F6 | Observation 11.1: each job's best available option can only get worse over time; each candidate's offers can only get better. Intuitively the two "meet in the middle", and such a matching "should be stable". | 247 to 252 | stated |
| F7 | Lemma 11.2 (Improvement Lemma): if job J makes an offer to candidate C on the kth day, then on every subsequent day C has a job offer in hand that she likes at least as much as J. | 255 to 256 | checked for every instance with three jobs and three candidates: `lemma_holds` |
| F8 | Proof, base case (day k): C receives at least the offer from J, and she keeps the best among her offers, so at the end of day k she has in hand J or a job she likes more. | 258 to 260 | stated |
| F9 | Proof, inductive step: suppose that on day i (i at least k) C has in hand a job J' she likes at least as much as J (J' may be J). J' proposes to C again on day i+1, since she has not rejected it. So at the end of day i+1 she has J' or a job she likes more than J'; in both cases at least as much as J. | 261 to 266 | stated |
| F10 | The proof is an induction on the day. | 257 | stated |
| F11 | Anita's three days in the run of episode 1. Offers to her: day one Approximation and Control; day two Approximation; day three Approximation. In hand at the end of each day: Approximation. Her list: Basis, Approximation, Control. | 78 to 98, 33 to 36 | `ANITA` below |

```python
from itertools import permutations, product
JOBS = {"Approximation": ["Anita", "Bridget", "Christine"],
        "Basis":         ["Bridget", "Anita", "Christine"],
        "Control":       ["Anita", "Bridget", "Christine"]}
CANDS = {"Anita":     ["Basis", "Approximation", "Control"],
         "Bridget":   ["Approximation", "Basis", "Control"],
         "Christine": ["Approximation", "Basis", "Control"]}

def run(jobs, cands):
    """Per day: (offers job -> candidate, in hand candidate -> job, crossed off (job, candidate))."""
    left = {j: list(l) for j, l in jobs.items()}
    days = []
    while True:
        offers = {j: left[j][0] for j in jobs if left[j]}
        hand, crossed = {}, []
        for c in cands:
            got = [j for j in offers if offers[j] == c]
            if got:
                best = min(got, key=cands[c].index)
                hand[c] = best
                crossed += [(j, c) for j in got if j != best]
        days.append((offers, hand, crossed))
        if not crossed:
            return days
        for j, c in crossed:
            left[j].remove(c)

DAYS = run(JOBS, CANDS)
CROSSED = [x for _, _, cr in DAYS for x in cr]
assert len(DAYS) == 3 and CROSSED == [("Control", "Anita"), ("Control", "Bridget")]
ANITA = [(sorted(j for j, c in o.items() if c == "Anita"), h.get("Anita")) for o, h, _ in DAYS]
assert ANITA == [(["Approximation", "Control"], "Approximation"),
                 (["Approximation"], "Approximation"), (["Approximation"], "Approximation")]
assert 3 * 3 == 9

def lemma_ok(jobs, cands):          # the Improvement Lemma on one run
    days = run(jobs, cands)
    for k, (offers, _, _) in enumerate(days):
        for j, c in offers.items():
            for _, hand, _ in days[k:]:
                if c not in hand or cands[c].index(hand[c]) > cands[c].index(j):
                    return False
    return True

names_j, names_c = list(JOBS), list(CANDS)
max_refusal_days, lemma_holds = 0, True
for jl in product(permutations(names_c), repeat=3):
    for cl in product(permutations(names_j), repeat=3):
        jobs, cands = dict(zip(names_j, map(list, jl))), dict(zip(names_c, map(list, cl)))
        max_refusal_days = max(max_refusal_days, len(run(jobs, cands)) - 1)
        lemma_holds = lemma_holds and lemma_ok(jobs, cands)
assert max_refusal_days <= 9 and lemma_holds
```

(The enumeration takes a few seconds. The builder may keep it in a separate check and
only assert the first three `assert` lines in the episode file.)

## Added to the notes

| Beat | The step that was missing | Why it holds |
|---|---|---|
| 1.2 | The proof of Lemma 11.1 says a job "must eliminate some candidate" on a day that does not halt, without saying why, and does not say that the elimination is permanent. | A day that does not stop has a refusal (stop rule F2); a refused job crosses the name off that evening (evening rule F2); no rule ever puts a name back. Shown on the run of episode 1 (F3). |
| 1.3 | The count for the case on screen, before the general one. | Three lists of three names are nine names (F4); each refusal day uses at least one; so at most nine refusal days. |
| 1.3, 1.4 | The notes conclude "at most n squared iterations". The count only bounds the days on which somebody is refused; the day on which nobody is refused comes after them. The episode says "at most that many days can have a refusal", which is what the argument shows. Reported as a small correction of the notes' wording. | Each refusal day crosses off at least one of the n times n names. |
| 2.1 to 2.3 | A concrete case of the lemma before its statement: Anita's three days, with Control (she holds something better) and Approximation (she holds exactly that). | F11; her list on screen. |
| 2.4 | "At the end of that day, and of every later day". The notes say "on every subsequent day"; their own base case is day k itself, and "has in hand" only makes sense after her afternoon answer. | F8 starts the induction at day k and speaks of "the end of day k". |
| 3.2 | Why the job in hand crosses nothing off that evening. | It made one offer that day (the morning rule gives each job one offer), that offer was not refused, and a job only crosses off the candidate who refused it. |
| 3.3 | Why that job asks the same candidate again the next morning. The notes say only "since this job offer hasn't yet been rejected by her". | It asked her today, so today she was the first name on its list not crossed off. Its list did not change in the evening (3.2). So tomorrow she is still the first name not crossed off, and the morning rule sends the offer to her. |
| 3.4 | The last link: "at least as good as the job in hand" and "the job in hand is at least as good as the original job" give "at least as good as the original job". | Both comparisons are positions on the same list, the candidate's own; higher than or equal twice is higher than or equal. |
| 3.5 | That base case and step together give every later day. | Induction on the day (F10): true on day k, and true on a day implies true on the next. |
| 3.6 | The jobs' half of Observation 11.1, which the notes state without a reason. | A job asks the first name not crossed off; names are only crossed off, never restored; so the name it asks can only move down its list. |

## Left out, and why

| Item of the notes | Line | Reason |
|---|---|---|
| "The former is easy to show" | 136 | Not a step. |
| "Next, we'd like to show that the algorithm finds a good matching" and section 4.1 on stability | 143 to 242 | Episodes 3 and 4. |
| "We now prove that the propose-and-reject algorithm always outputs a stable matching" | 245 | Episode 7; this episode only proves the lemma that proof needs, and ends on the question. |
| The letters k and i in the voice | 255 to 266 | They are on screen ("day k", "day i", "day i+1"); the voice says "the day of the offer", "some day", "the next day". |
| The alternate proof of the lemma and the well-ordering principle | 267 to 304 | Episode 6. |

## Layout used by every scene

Three stages, one per scene; each scene starts by removing the stage before it.
Nothing but the scene heading is above y = 2.7; nothing is below y = -2.7. A text
inside a box is scaled down, if needed, to at most the box width minus 0.4.

Colours: job blue `BLUE_C`; candidate gold `GOLD_C`; plain border `GREY_B` width 2;
"in hand" and "holds" `GREEN_C`; an offer she refused `RED_C` (the name of the refused job is
written in red); the place on her list of the job whose offer we follow: an `ORANGE` border
(Control in scene `anita`, J in scene `proof`); looked at `YELLOW_D`.

Stage one (scene `hook`).
- Three job columns at x = -3.9, 0.5, 4.9, every box 2.4 wide (the top half of the stage
  of episodes 1 and 3). Headers `box_label(name, BLUE_C, w=2.4, h=0.55, font_size=22)`
  at y = 2.42. Cells `Rectangle(width=2.4, height=0.48)`, border `GREY_B` width 2, at
  y = 1.86 (row 1), 1.35 (row 2), 0.84 (row 3), with `txt(name, 22)` at the centre.

| column | header | row 1 | row 2 | row 3 |
|---|---|---|---|---|
| x = -3.9 | Approximation | Anita | Bridget | Christine |
| x = 0.5 | Basis | Bridget | Anita | Christine |
| x = 4.9 | Control | Anita | Bridget | Christine |

- Day row at y = -0.3: three boxes `Rectangle(width=1.5, height=0.6)`, border `GREY_B`
  width 2, at x = -3.9, -2.2, -0.5, with `txt("Day 1", 22)`, `txt("Day 2", 22)`,
  `txt("Day 3", 22)` inside. Question slot: one text at (1.6, -0.3), size 24.
- Count lines, centred at x = 0: line A at y = -1.3, size 26; line B at y = -1.9, size 22; line C at y = -2.45, size 20.

Stage two (scene `anita`).
- Anita's list, left: header `box_label("Anita", GOLD_C, w=2.4, h=0.55, font_size=22)`
  at (-4.8, 1.95); three cells 2.4 wide, 0.48 high at x = -4.8 and y = 1.39 (Basis),
  0.88 (Approximation), 0.37 (Control).
- Day grid, right: three columns at x = 0.0, 2.6, 5.2, every box 2.4 wide.
  Day headers: `Rectangle(width=2.4, height=0.5)`, border `GREY_B`, at y = 2.0, with
  "Day 1", "Day 2", "Day 3" (`txt`, 22).
  Offers cells: `Rectangle(width=2.4, height=1.0)` at y = 1.15, empty at first.
  In-hand cells: `Rectangle(width=2.4, height=0.6)` at y = 0.25, empty at first.
- Row labels `txt("offers", 20, GREY_B)` at (-2.4, 1.15) and `txt("in hand", 20, GREY_B)` at (-2.4, 0.25).
- Texts that go into the grid (`txt`, 20): day 1 offers "Approximation" at (0.0, 1.38)
  and "Control" at (0.0, 0.92); day 2 offers "Approximation" at (2.6, 1.15); day 3
  offers "Approximation" at (5.2, 1.15); in hand "Approximation" at (0.0, 0.25),
  (2.6, 0.25), (5.2, 0.25).
- Statement lines, centred at x = 0: line 1 at y = -1.0, size 24; line 2 at y = -1.6, size 24; line 3 at y = -2.3, size 22.

Stage three (scene `proof`).
- The candidate's list as a ladder, left: header `box_label("candidate C", GOLD_C, w=2.4, h=0.55, font_size=22)`
  at (-4.4, 2.3); five cells ("rungs") 2.4 wide, 0.48 high at x = -4.4 and y = 1.74
  (rung 1, her favourite), 1.23 (rung 2), 0.72 (rung 3), 0.21 (rung 4), -0.30 (rung 5).
  All rungs are empty except rung 4, which holds `txt("J", 22)` from the start. J' is not written on a rung, because it may be J itself or any job above it.
- The J' bracket (appears in beat 3.2), to the right of the ladder, spanning rungs 1 to 4: `Line((-2.95, -0.03), (-2.95, 1.98), color=GREEN_C, stroke_width=5)` with two end ticks `Line((-3.12, 1.98), (-2.95, 1.98))` and `Line((-3.12, -0.03), (-2.95, -0.03))` in the same colour and width, and `txt("J'", 22, GREEN_C)` at (-2.65, 0.95). It says: J' is one of these four rungs, J included.
- Up arrow `Arrow((-6.2, -0.3), (-6.2, 1.74), buff=0, color=GREY_B, stroke_width=4)` with `txt("better", 18, GREY_B)` at (-6.2, 2.05).
- The job's list, below the ladder (appears in beat 3.2): header `box_label("job J'", BLUE_C, w=2.4, h=0.5, font_size=22)`
  at (-4.4, -1.2); two cells 2.4 wide, 0.45 high at y = -1.7 (text "crossed off", cell and text at opacity 0.25) and y = -2.17 (text "C").
  Down arrow (beat 3.6): `Arrow((-6.2, -1.5), (-6.2, -2.35), buff=0, color=RED_C, stroke_width=4)`.
- Day strip, right: boxes `Rectangle(width=2.0, height=0.5)`, border `GREY_B`, at
  y = 2.3 and x = -0.6 ("day k"), 2.6 ("day i"), 5.3 ("day i+1"), texts `txt`, 22;
  `txt("...", 22)` at (1.0, 2.3). Under each of the three boxes an in-hand cell
  `Rectangle(width=2.0, height=0.55)` at y = 1.65, empty at first. Row label
  `txt("in hand", 20, GREY_B)` at (-2.4, 1.65). Step arrow:
  `Arrow((3.65, 1.65), (4.25, 1.65), buff=0, color=YELLOW_D, stroke_width=4)`.
- Chain row (beat 3.5 only; it takes the place of the day strip, which is removed first): five boxes `Rectangle(width=1.0, height=0.5)`, border `GREY_B` width 2, at y = 2.2 and x = -0.8, 0.6, 2.0, 3.4, 4.8, with the labels "k", "k+1", "k+2", "k+3", "k+4" (`txt`, 20); `txt("day", 20, GREY_B)` at (-1.9, 2.2); `txt("...", 32)` at (5.9, 2.2); four link arrows `Arrow((x + 0.52, 2.2), (x + 0.88, 2.2), buff=0, stroke_width=4, tip_length=0.15)` for x = -0.8, 0.6, 2.0, 3.4. A green box has stroke `GREEN_C` width 4 and fill `GREEN_C` opacity 0.25. Chain caption: `txt("the step works from any day i on which the claim holds, first with i = k", 20)` at (2.6, 1.5), at most 8 wide.
- Proof lines, `txt`, size 20, left edge at x = -1.6, at most 8.2 wide (scale down if wider):

| line | y | text |
|---|---|---|
| P1 | 0.8 | day k: J is among her offers, and she keeps the best one |
| P2 | 0.25 | day i: she holds J', which is J or better (J' may be J itself) |
| P3 | -0.3 | J' was not refused, so its list does not change |
| P4 | -0.85 | day i+1: J' asks C again |
| P5 | -1.4 | day i+1: she holds J' or better, which is J or better |
| P6 | -2.0 | do the two sides meet in a stable matching? |

Rules for the builder that come from the check script:
- To highlight a box or cell, change its own stroke (`set_stroke(colour, 4)`). Never put a second rectangle on top.
- "Crossing off" a name is done by fading the cell and its name to opacity 0.25. Never draw a line through a text.
- "Flash" means `Indicate(obj, color=YELLOW_D, scale_factor=1.1)`; the object returns to the look it had.
- When a text in a slot or cell changes, fade the old one out and the new one in at the same place in one animation.
- Where a beat ends a scene, hold until the voice has finished the beat, and only then remove things and change the heading.

## Scene `hook`: heading "Does it always stop?"

Stage: stage one, built in beat 1.1.
Kept from the scene before: nothing. Removed at the end: hold until the voice has
finished beat 1.4, then remove everything.

### 1.1
> In the first episode, propose and reject stopped after three days, but that was one
> example. The stopping rule waits for a day on which nobody is refused, so could there
> be lists for which such a day never comes?

- with the first word: the three job columns (headers and cells with names) appear, column by column from the left.
- on "after three days": the three day boxes "Day 1", "Day 2", "Day 3" appear, left to right.
- on "nobody is refused": the border of the box "Day 3" turns `GREEN_C`, width 4.
- on "never comes": the text `txt("always?", 24, YELLOW_D)` appears in the question slot.
- uses: episode 1 (the run and the stop rule), F1, F2, F3.

### 1.2
> Look at what a day with a refusal does. In the evening the refused job crosses a name
> off its list, and a name that is crossed off never comes back. On day one Control
> crossed off Anita, and on day two it crossed off Bridget.

- with the first word: the borders of the boxes "Day 1" and "Day 2" turn `RED_C`, width 4.
- on "crosses a name": flash the header "Control".
- on "day one Control": row 1 of the Control column (Anita) and its name fade to opacity 0.25; flash the box "Day 1".
- on "day two it crossed off Bridget": row 2 of the Control column (Bridget) and its name fade to opacity 0.25; flash the box "Day 2".
- uses: F2 (evening rule), F3. The step is in "Added to the notes".

### 1.3
> So every day that does not stop the algorithm uses up at least one name. And the
> supply is limited, since three jobs with three names each make nine names in all.
> That means at most nine days can have a refusal, and after that a day with no refusal
> has to come.

- with the first word: nothing new.
- on "uses up at least one name": flash the two faded cells of the Control column together.
- on "nine names in all": flash all nine cells together; line A appears: `txt("3 × 3 = 9 names", 26)`.
- on "at most nine days": line B appears: `txt("at most 9 days with a refusal", 22)`.
- on "has to come": line B changes to `txt("at most 9 days with a refusal, then a day with none: stop", 22)`; flash the green box "Day 3".
- uses: beat 1.2, the nine cells on screen, F4.

### 1.4
> Nothing in this count was special about three. With any number of jobs, and as many
> candidates, the number of names is that number times itself. So only that many days
> can have a refusal, and propose and reject always halts, whatever the lists are.

- with the first word: flash line A.
- on "any number of jobs": line A changes to `txt("n × n names", 26)`.
- on "only that many days": line B changes to `txt("at most n × n days with a refusal, then a day with none: stop", 22)`, so that the line above "Lemma 11.1" shows the day on which the algorithm halts.
- on "always halts": the text in the question slot changes to `txt("always", 24, GREEN_C)`, and line C appears: `txt("Lemma 11.1: propose and reject always halts", 20, YELLOW_D)`.
- uses: beat 1.3 (the same count), F5.
- end of scene: hold until the voice has finished this beat, then remove everything.

## Scene `anita`: heading "What a candidate holds"

Stage: stage two, built in beat 2.1 from an empty stage.
Kept from the scene before: nothing. Removed at the end: hold until the voice has
finished beat 2.4, then remove everything.

### 2.1
> Halting is half of what we want, and the other half is that the result is stable. For
> that we need to know what a candidate holds from day to day, so let us replay the
> three days of Anita.

- with the first word: Anita's header and her three cells (Basis, Approximation, Control) appear.
- on "what a candidate holds": the row labels "offers" and "in hand" appear.
- on "the three days of Anita": the three day headers, the three empty offers cells and the three empty in-hand cells appear, column by column from the left.
- uses: F1, F11.

### 2.2
> On day one Approximation and Control both made her an offer, and she kept
> Approximation in hand. On days two and three Approximation simply asked again, and she
> kept it again.

- with the first word: "Approximation" and "Control" are written in the day 1 offers cell.
- on "kept Approximation in hand": "Approximation" is written in the day 1 in-hand cell, and that cell gets a `GREEN_C` border, width 4; the text "Control" in the day 1 offers cell turns `RED_C` (the offer she refused).
- on "simply asked again": "Approximation" is written in the day 2 and day 3 offers cells.
- on "kept it again": "Approximation" is written in the day 2 and day 3 in-hand cells, and both cells get a `GREEN_C` border, width 4.
- uses: F11, episode 1.

### 2.3
> Now pick any job that ever made Anita an offer, for example Control on day one. From
> that day on, what Anita holds is never below Control on her own list. The same is true
> for Approximation, where what she holds is exactly as good, because it is
> Approximation itself.

- with the first word: nothing new.
- on "Control on day one": flash the red text "Control" in the day 1 offers cell (it stays red: she refused it), and the cell "Control" in Anita's list gets an `ORANGE` border, width 4 (the place of that job on her list).
- on "never below Control": the cell "Approximation" in Anita's list gets a `GREEN_C` border, width 4; flash the three in-hand cells together.
- on "exactly as good": flash the text "Approximation" in the day 1 offers cell and the cell "Approximation" in Anita's list together.
- uses: beat 2.2, Anita's list on screen (Approximation is above Control).

### 2.4
> Here is the claim in general. Suppose a job makes an offer to a candidate on some day.
> Then at the end of that day, and of every later day, she holds an offer she likes at
> least as much. This is called the improvement lemma, and one example is not a proof
> of it.

- with the first word: flash Anita's list (header and three cells).
- on "makes an offer": statement line 1 appears: `txt("job J makes an offer to candidate C on day k", 24)`.
- on "every later day": statement line 2 appears: `txt("from day k on, C holds an offer she likes at least as much as J", 24)`.
- on "improvement lemma": statement line 3 appears: `txt("Lemma 11.2, the Improvement Lemma", 22, YELLOW_D)`.
- uses: beat 2.3 (the case), F7.
- end of scene: hold until the voice has finished this beat, then remove everything.

## Scene `proof`: heading "Why offers only get better"

Stage: stage three, built in beat 3.1 from an empty stage; the job's list appears in beat 3.2.
Kept from the scene before: nothing. Removed at the end: nothing (the end card follows).

### 3.1
> Take a candidate and a job that makes her an offer, and look at the afternoon of that
> same day. She has at least this one offer to choose from, and the rule says she keeps
> the best of what she has. So at the end of that day she holds this job or one she
> likes more.

- with the first word: the ladder (header "candidate C", five rungs, "J" on rung 4), the up arrow with "better", the day strip (three day boxes, "...", three empty in-hand cells) and the row label "in hand" appear.
- on "makes her an offer": rung 4 (J) gets an `ORANGE` border, width 4; flash the box "day k".
- on "keeps the best": proof line P1 appears.
- on "this job or one she likes more": rungs 1, 2 and 3 get a `GREEN_C` border, width 4 (rung 4 stays orange); `txt("J or better", 20, GREEN_C)` is written in the in-hand cell under "day k".
- uses: F2 (afternoon rule), F8.

### 3.2
> Now suppose that at the end of some day she holds a job that is at least this good.
> The question is whether that job will ask her again tomorrow. She did not refuse it,
> and a job makes only one offer a day, so in the evening it crossed nothing off its
> list.

- with the first word: flash the box "day i".
- on "at least this good": the J' bracket appears beside rungs 1 to 4 of the ladder (the line, its two ticks and the green "J'"), and `txt("J'", 20, GREEN_C)` is written in the in-hand cell under "day i"; proof line P2 appears.
- on "ask her again tomorrow": the yellow step arrow appears between the in-hand cells of "day i" and "day i+1".
- on "crossed nothing off": the job's list appears below the ladder (header "job J'", the faded cell "crossed off", the cell "C" with a `YELLOW_D` border, width 4); proof line P3 appears.
- uses: beat 3.1 (what "this good" means), F2 (morning and evening rule), F9. The bracket covers rung 4 (J) and the three rungs above it, which is exactly what P2 says: J or better, and J' may be J itself.

### 3.3
> So the next morning her name is still the first one on its list that is not crossed
> off, exactly as it was this morning. The morning rule then makes that job ask her
> again. That is the step the whole proof turns on, because an offer that was not
> refused always comes back the next day.

- with the first word: nothing new.
- on "not crossed": flash the cell "C" in the job's list.
- on "ask her again": `txt("J' asks again", 20)` is written in the in-hand cell under "day i+1"; proof line P4 appears.
- on "always comes back": flash the step arrow and proof line P4.
- uses: beat 3.2 (its list did not change), F2 (morning rule), F9.

### 3.4
> So tomorrow afternoon she again has that job among her offers, and again she keeps the
> best of what she has. What she holds tomorrow is that job or one she likes more. And
> since that job was at least as good as the original one, what she holds tomorrow is
> at least as good too.

- with the first word: flash the in-hand cell under "day i+1".
- on "keeps the best": the text in the in-hand cell under "day i+1" changes to `txt("J' or better", 20, GREEN_C)`.
- on "that job or one she likes more": flash the J' bracket.
- on "the original one": flash rungs 1, 2, 3 and 4 together; proof line P5 appears.
- uses: beat 3.3 (the offer comes back), beat 3.1 (the same afternoon argument), the ladder on screen, F9.

### 3.5
> So the claim is true on the day of the offer, and whenever it is true on one day it is
> true on the next. That carries it from day to day forever, which is a proof by
> induction on the days. The hand of a candidate can only climb her list.

- with the first word: the day strip is removed (the three day boxes, its "...", the three in-hand cells with their texts, the step arrow and the row label "in hand"), and the chain row appears in its place: the caption "day", the five boxes "k" to "k+4", all grey, and the large "...". The link arrows are not there yet.
- on "the day of the offer": the box "k" becomes a green box; flash proof line P1 (the base case).
- on "true on the next": the chain caption appears; the first link arrow grows from box "k" to box "k+1", and then box "k+1" becomes a green box: the step used with i = k.
- on "from day to day": the second, third and fourth link arrows grow one after another, and after each one the box it points to becomes a green box ("k+2", then "k+3", then "k+4"), about half a second apart; then the large "..." turns `GREEN_C`.
- on "only climb": the up arrow beside the ladder turns `GREEN_C` and is flashed.
- uses: beat 3.1 (base case), beats 3.2 to 3.4 (step), F10, F7.

### 3.6
> A job, meanwhile, starts at the top of its list and can only move down, because names
> are crossed off and never come back. So candidates climb while jobs sink, and
> somewhere the two have to meet. Whether the place where they meet is always stable is
> the question we are heading for.

- with the first word: flash the header "job J'".
- on "can only move down": the red down arrow appears beside the job's list; flash the faded cell "crossed off".
- on "candidates climb while jobs sink": flash the green up arrow and the red down arrow together.
- on "always stable": proof line P6 appears in `YELLOW_D`.
- uses: scene `hook` beat 1.2 (names never come back), beat 3.5, F6. Nothing is answered here; episode 7 answers it.

## End card

- Every day with a refusal crosses a name off a list for good, and there are only n times n names, so propose and reject always halts.
- Improvement Lemma: once a job has made a candidate an offer, she holds that job or a better one at the end of that day and of every later day.
- The reason is that an offer which was not refused is made again the next morning.
- So a candidate's hand only climbs her list, and a job only moves down its own.

## Author's check, each answered yes

- The first beat shows one concrete case before any definition. Yes: the lists and the three days of episode 1.
- Every "uses" line names an earlier beat, a fact row, or what is on the screen. Yes.
- A name is introduced after the beat where the viewer sees it happen. Yes: the lemma is named in 2.4 after Anita's case; "induction" in 3.5 after base case and step.
- Every beat has a drawn object that changes; no beat is words on an empty stage. Yes.
- Every phrase after "on" is copied from its own beat, and appears there once. Yes, checked by script.
- A beat over fourteen seconds has at least two changes, over twenty-six at least three. Yes, checked by script.
- If the voice counts things, the stage shows exactly that many. Yes: three days, three jobs with three names, nine cells.
- No step is skipped, and every step the notes left out is in "Added to the notes". Yes.
- Every item of the notes in the source range is in a beat or in "Left out". Yes.
- Narration: 14 beats, two to four sentences each, no sentence over 25 words, no beat over 60 words, no digit, colon or symbol. Yes, checked by script.
