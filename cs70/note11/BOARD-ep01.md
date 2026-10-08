# BOARD: episode 01, Propose and Reject

Source: `notes.txt` lines 9 to 100. Language: en. Aim: 5 to 6 minutes (about 750 words).
File `ep01_propose_reject.py`, class `Ep01ProposeReject`. Scenes, in order: `hook`, `first_try`, `days`, `result`.

The builder copies every narration line (the lines that start with a greater-than sign)
into a `say()` unchanged, one beat per `say()`, and builds exactly the stage described.
It decides nothing; an unclear line is a question in its report.

## Facts

Every number, name, list and rule the episode says or shows.

| id | Fact, with all its conditions | Notes line | Computed how |
|---|---|---|---|
| F1 | There are three jobs. The notes call them Approximation Inc., Basis Co. and Control Corp.; this episode says and shows "Approximation", "Basis", "Control". | 14 | `len(JOBS) == 3` |
| F2 | There are three candidates: Anita, Bridget, Christine. | 15 | `len(CANDS) == 3` |
| F3 | Each job's list, most wanted first. Approximation: Anita, Bridget, Christine. Basis: Bridget, Anita, Christine. Control: Anita, Bridget, Christine. | 17 to 30 | the dict `JOBS` below |
| F4 | Each candidate's list, most wanted first. Anita: Basis, Approximation, Control. Bridget: Approximation, Basis, Control. Christine: Approximation, Basis, Control. | 31 to 44 | the dict `CANDS` below |
| F5 | Anita is at the top of the list of two of the three jobs (Approximation and Control). | 17 to 30 | `sum(JOBS[j][0] == "Anita" for j in JOBS) == 2` |
| F6 | One possible matching: Approximation with Bridget, Basis with Christine, Control with Anita. | 47 | `EXAMPLE` below, stated |
| F7 | In the matching F6, Approximation ranks Anita above the candidate it has (Bridget), and Anita ranks Approximation above the job she has (Control, the last on her list). | from F3, F4, F6 (the idea: 49, 151 to 152) | `prefers(JOBS, "Approximation", "Anita", "Bridget") and prefers(CANDS, "Anita", "Approximation", "Control") and CANDS["Anita"][-1] == "Control"` |
| F8 | Morning rule: each job makes an offer to the most preferred candidate on its list who has not yet rejected it. | 63 to 64 | stated |
| F9 | Afternoon rule: each candidate says "maybe" to the offer she likes best among those she got that morning (she has it "in hand") and "no" to the others. | 65 to 67 | stated |
| F10 | Evening rule: each rejected job crosses the candidate who rejected it off its list. | 68 to 69 | stated |
| F11 | Stop rule: the days repeat until a day on which no offer is rejected; on that day each candidate accepts the offer she has in hand. | 70 to 72 | stated |
| F12 | Day one. Offers: Approximation to Anita, Basis to Bridget, Control to Anita. In hand: Anita has Approximation, Bridget has Basis, Christine has nothing. Rejected: Control (by Anita). | 78 to 84 | `DAYS[0]` below equals `run()[0]` |
| F13 | Day two. Offers: Approximation to Anita, Basis to Bridget, Control to Bridget. In hand: Anita has Approximation, Bridget has Basis, Christine has nothing. Rejected: Control (by Bridget). | 85 to 91 | `DAYS[1]` equals `run()[1]` |
| F14 | Day three. Offers: Approximation to Anita, Basis to Bridget, Control to Christine. Every candidate has exactly one offer. Nobody is rejected. | 92 to 98 | `DAYS[2]` equals `run()[2]` |
| F15 | The run stops on day three, and the output is Approximation with Anita, Basis with Bridget, Control with Christine. | 99 to 100 | `len(run()) == 3` and `RESULT` below |
| F16 | The procedure is called the Propose-and-Reject algorithm, also known as the Gale-Shapley algorithm. | 52 | stated |
| F17 | In the output, Control has the last candidate on its list (Christine) and Christine has the last job on her list (Control). | from F3, F4, F15 | `JOBS["Control"][-1] == "Christine" and CANDS["Christine"][-1] == "Control"` |

The author ran this by hand and by this code; the builder puts it in its FACTS block
and asserts it, and uses the constants `DAYS` and `RESULT` (it does not need `run()`
to draw anything).

```python
JOBS = {"Approximation": ["Anita", "Bridget", "Christine"],
        "Basis":         ["Bridget", "Anita", "Christine"],
        "Control":       ["Anita", "Bridget", "Christine"]}
CANDS = {"Anita":     ["Basis", "Approximation", "Control"],
         "Bridget":   ["Approximation", "Basis", "Control"],
         "Christine": ["Approximation", "Basis", "Control"]}
EXAMPLE = {"Approximation": "Bridget", "Basis": "Christine", "Control": "Anita"}

def prefers(lists, who, a, b):          # who ranks a above b
    return lists[who].index(a) < lists[who].index(b)

# per day: (offers job -> candidate, in hand candidate -> job, rejected jobs)
DAYS = [
    ({"Approximation": "Anita", "Basis": "Bridget", "Control": "Anita"},
     {"Anita": "Approximation", "Bridget": "Basis"}, ["Control"]),
    ({"Approximation": "Anita", "Basis": "Bridget", "Control": "Bridget"},
     {"Anita": "Approximation", "Bridget": "Basis"}, ["Control"]),
    ({"Approximation": "Anita", "Basis": "Bridget", "Control": "Christine"},
     {"Anita": "Approximation", "Bridget": "Basis", "Christine": "Control"}, []),
]
RESULT = {"Approximation": "Anita", "Basis": "Bridget", "Control": "Christine"}

def run():
    left = {j: list(l) for j, l in JOBS.items()}
    days = []
    while True:
        offers = {j: left[j][0] for j in JOBS}
        hand, rejected = {}, []
        for c in CANDS:
            got = [j for j in JOBS if offers[j] == c]
            if got:
                best = min(got, key=CANDS[c].index)
                hand[c] = best
                rejected += [j for j in got if j != best]
        days.append((offers, hand, rejected))
        if not rejected:
            return days
        for j in rejected:
            left[j].remove(offers[j])

assert run() == DAYS and len(DAYS) == 3
assert {j: c for c, j in DAYS[-1][1].items()} == RESULT
assert sum(JOBS[j][0] == "Anita" for j in JOBS) == 2
assert prefers(JOBS, "Approximation", "Anita", "Bridget")
assert prefers(CANDS, "Anita", "Approximation", "Control") and CANDS["Anita"][-1] == "Control"
assert JOBS["Control"][-1] == "Christine" and CANDS["Christine"][-1] == "Control"
```

## Added to the notes

Steps the notes skip and this episode works out, so no claim rests on "clearly".

| Beat | The step that was missing | Why it holds |
|---|---|---|
| 1.6 | The notes ask for a matching where "nobody can realistically hope to benefit by switching jobs" (line 49) but show no case of somebody who can. The episode shows one in the notes' own second matching: Approximation and Anita. | F7: Approximation's list has Anita above Bridget, Anita's list has Approximation above Control. Both read off the lists on screen. |
| 2.1, 2.2 | The notes present the algorithm ready-made. The episode first tries the obvious plan (every job takes its first choice) and sees it fail. | F3: Approximation and Control both have Anita first, so Anita gets two offers and Christine none. |
| 2.3 | Why Bridget also has an offer in hand after day one (the notes' table shows it in bold, the text does not say it). | She got exactly one offer, so the best among her offers is that one (afternoon rule F9). |
| 2.4 | Why the candidate answers "maybe" and not "yes" (the notes only say she "responds maybe"). | F4: Basis is first on Anita's list and has not made her an offer yet; a job she likes more can still come. |
| 2.5 | Why a rejected job crosses the candidate off. | The morning rule F8 only lets a job ask a candidate who has not rejected it; crossing off is how the list remembers that. |
| 3.1 | Why Approximation and Basis make the same offer again on day two (the notes' table repeats them without comment). | Nobody rejected them, so the candidate they asked is still the first name not crossed off (F8). |
| 3.5 | Why "no offer rejected" is the right moment to stop (the notes state it as the rule, line 70). | No rejection means no list changes in the evening; the morning offers depend only on the lists, so the next day would repeat this one exactly. |
| 4.1 | That the pair that broke the example matching in 1.6 is together in the output. | F15: Approximation is matched with Anita. |
| 4.2 | That Control and Christine each end with the last name on their list. The notes say this at line 196 about another matching; here it is checked for the output. | F17. |

## Left out, and why

| Item of the notes | Line | Reason |
|---|---|---|
| Introduction: proof techniques of the earlier notes; "one of the highlights of the field of algorithms" | 9 to 11 | Not a step of the argument; the series is its own introduction. |
| "Suppose you run an employment system", n jobs and n candidates in general | 12 to 13 | The episode stays with the case of three; the general n comes with the first proof (episode 5). |
| The suffixes Inc., Co., Corp. | 14 | A full stop inside a sentence breaks the voice's sentence split; the three names stay recognisable. Departure from the notes, reported. |
| The first example matching (Approximation with Anita, Basis with Bridget, Control with Christine) | 46 | It is the output of the algorithm; showing it early would give the ending away. The second example matching (line 47) is shown. |
| "Can you do this efficiently?", "remarkably simple, fast, and widely-used" | 50 to 51 | Claims this episode cannot show; halting and the bound on the days are episode 5, the use in practice is episode 2. |
| "Days" give a clear sense of discrete time | 56 | Said by doing: the day is named in beat 2.6 after the viewer has watched one. |
| Footnote 1 (EECS internships), footnote 2 (pronouns) | 57 to 59 | Asides. The episode follows footnote 2's convention ("she" for a candidate, "it" for a job). |
| "At that point, each candidate has a job offer in hand" as a general claim | 70 to 71 | Shown only for this example (beat 3.4). In general it needs Lemma 11.3, episode 7. |
| The words "on a string" | 66 | One name per thing: "in hand" only. |
| "Why study stable matchings in the first place?" | 101 to 104 | It is the opening of episode 2. |

## Layout used by every scene

One stage, built in `hook` and kept to the end. Nothing is ever cleared except what a
"Removed" line names. All coordinates are centres unless stated.

Colours: job blue `BLUE_C`; candidate gold `GOLD_C`; plain cell border `GREY_B`,
stroke width 2; "being looked at / the candidate a job asks now" `YELLOW_D`; "in hand"
`GREEN_C`; "refused" `RED_C`; "would rather" `ORANGE`.

Three columns at x = -3.9, 0.5, 4.9. Every box is 2.2 wide.

Top half, the jobs:
- Job headers: `box_label(name, BLUE_C, w=2.2, h=0.55, font_size=24)` at y = 2.70.
  Left to right: "Approximation", "Basis", "Control".
- Under each header three cells: `Rectangle(width=2.2, height=0.5)`, border `GREY_B`
  width 2, no fill, at y = 2.13 (row 1), 1.61 (row 2), 1.09 (row 3), each with a name
  `txt(name, 22)` at its centre. Row 1 is the job's first choice.

| column | header | row 1 | row 2 | row 3 |
|---|---|---|---|---|
| x = -3.9 | Approximation | Anita | Bridget | Christine |
| x = 0.5 | Basis | Bridget | Anita | Christine |
| x = 4.9 | Control | Anita | Bridget | Christine |

Bottom half, the candidates:
- Candidate headers: `box_label(name, GOLD_C, w=2.2, h=0.55, font_size=24)` at y = -0.75.
  Left to right: "Anita", "Bridget", "Christine".
- Under each header three cells, same size and style, at y = -1.32 (row 1), -1.84
  (row 2), -2.36 (row 3). Row 1 is the candidate's first choice.

| column | header | row 1 | row 2 | row 3 |
|---|---|---|---|---|
| x = -3.9 | Anita | Basis | Approximation | Control |
| x = 0.5 | Bridget | Approximation | Basis | Control |
| x = 4.9 | Christine | Approximation | Basis | Control |

The gap between the halves (y from 0.84 down to -0.475, x from -5.0 to 6.0) holds only
lines and arrows, never text. The fixed lines and arrows, each named once:

| name | kind | from (x, y) | to (x, y) |
|---|---|---|---|
| M1 | plain line, white, width 4 | (-3.5, 0.80) | (0.5, -0.45) |
| M2 | plain line, white, width 4 | (0.5, 0.80) | (4.9, -0.45) |
| M3 | plain line, white, width 4 | (4.9, 0.80) | (-3.4, -0.45) |
| D1 | dashed line, `ORANGE`, width 4 | (-4.3, 0.80) | (-4.3, -0.45) |
| P1 | arrow, Approximation to Anita | (-4.3, 0.80) | (-4.3, -0.45) |
| P2 | arrow, Basis to Bridget | (0.1, 0.80) | (0.1, -0.45) |
| P3 | arrow, Control to Anita | (4.9, 0.80) | (-3.4, -0.45) |
| P4 | arrow, Control to Bridget | (4.9, 0.80) | (1.0, -0.45) |
| P5 | arrow, Control to Christine | (4.9, 0.80) | (4.9, -0.45) |

Arrows: `Arrow(start, end, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.12)`,
white when drawn. D1 and P1 share coordinates but are never on the stage together
(D1 is removed at the end of `hook`, P1 is created in `first_try`). P3, P4 and P5 are
never on the stage together either: each is faded out before the next is created.

Left strip (x = -6.0, every text there at most 1.4 wide; scale it down if it is wider):
- "jobs" `txt("jobs", 22, GREY_B)` at (-6.0, 2.70); "candidates" `txt("candidates", 22, GREY_B)` at (-6.0, -0.75).
- Slot A at (-6.0, 0.42), size 26: the day label ("Day 1", "Day 2", "Day 3", "stop"), and "matching" in `hook`.
- Slot B at (-6.0, -0.02), size 20, `GREY_B`: the part of the day ("morning", "afternoon", "evening").
- Legend, beside the candidates' cells: a green segment `Line((-6.5, -1.35), (-5.5, -1.35))`
  `GREEN_C` width 4 with `txt("in hand", 20, GREEN_C)` at (-6.0, -1.65); a red segment
  `Line((-6.5, -2.05), (-5.5, -2.05))` `RED_C` width 4 with `txt("refused", 20, RED_C)` at (-6.0, -2.35).

Rules for the builder that come from the check script:
- To highlight a cell, change the stroke of the cell's own rectangle
  (`cell.animate.set_stroke(YELLOW_D, 4)`). Never put a second rectangle on top of a
  cell: two identical shapes are a layout FAIL.
- "Crossing off" a name is done by fading the cell and its name to opacity 0.25 and
  setting its border back to `GREY_B` width 2. Never draw a line through a name: a
  line through a text is a layout FAIL.
- "Flash" means `Indicate(obj, color=YELLOW_D, scale_factor=1.1)`; the object returns
  to the look it had.
- A repeated offer is the arrow that is already there. Flash it; do not create a
  second arrow on top.
- When a text in slot A or B changes, fade the old one out and the new one in at the
  same place in one animation (`FadeOut(old), FadeIn(new)`), so two texts never overlap.
- "Reset a cell" means border `GREY_B` width 2.

## Scene `hook`: heading "Three jobs, three candidates"

Stage: empty at the start, then built as in "Layout used by every scene". At the end of
the scene all six headers, all eighteen cells with their names and the two strip labels
"jobs" and "candidates" are on the stage.
Kept from the scene before: nothing. Removed at the end: M1, M2, M3, D1, the text
"matching" in slot A; and the four cells highlighted in beat 1.6 are reset.

### 1.1
> Three companies each have one job to fill, and we will call the jobs Approximation,
> Basis and Control. Three candidates, Anita, Bridget and Christine, are each looking
> for exactly one job.

- with the first word: the strip label "jobs" and the three job headers appear, left to right (Approximation, Basis, Control).
- on "Three candidates": the strip label "candidates" and the three candidate headers appear, left to right (Anita, Bridget, Christine).
- uses: F1, F2. Nothing here that the viewer has not seen.

### 1.2
> Every job has ranked the candidates from the one it wants most to the one it wants
> least. Approximation would hire Anita first, then Bridget, and Christine comes last
> on its list.

- with the first word: the nine empty cells under the three job headers appear (rectangles only, no names yet).
- on "hire Anita first": the name "Anita" is written in row 1 of the Approximation column.
- on "then Bridget": the name "Bridget" is written in row 2 of the Approximation column.
- on "Christine comes last": the name "Christine" is written in row 3 of the Approximation column.
- uses: beat 1.1 (the headers), F3.

### 1.3
> Basis sees it differently, because it puts Bridget first, then Anita, then Christine.
> Control has the same list as Approximation, so Anita is at the top for two of the
> three jobs.

- with the first word: the names "Bridget", "Anita", "Christine" are written in rows 1, 2, 3 of the Basis column, top to bottom.
- on "Control has the same list": the names "Anita", "Bridget", "Christine" are written in rows 1, 2, 3 of the Control column, top to bottom.
- on "at the top for two": flash the row 1 cell of the Approximation column and the row 1 cell of the Control column (both say "Anita") together.
- uses: beat 1.2, F3, F5.

### 1.4
> The candidates have opinions too, and each of them has ranked the three jobs in the
> same way. Anita likes Basis best, then Approximation, then Control, while Bridget and
> Christine both put Approximation first, then Basis, then Control.

- with the first word: the nine empty cells under the three candidate headers appear (rectangles only).
- on "Anita likes Basis best": the names "Basis", "Approximation", "Control" are written in rows 1, 2, 3 of the Anita column, top to bottom.
- on "Christine both put Approximation first": the names "Approximation", "Basis", "Control" are written in rows 1, 2, 3 of the Bridget column and of the Christine column, both columns at once, top to bottom.
- uses: beat 1.1, F4. "In the same way" means most wanted first, as in beat 1.2.

### 1.5
> Our task is a matching, which means every job gets one candidate and nobody is used
> twice. Here is one, where Approximation takes Bridget, Basis takes Christine, and
> Control takes Anita.

- with the first word: the text "matching" `txt("matching", 24)` appears in slot A.
- on "Approximation takes Bridget": the line M1 is drawn, from the job end to the candidate end.
- on "Basis takes Christine": the line M2 is drawn.
- on "Control takes Anita": the line M3 is drawn.
- uses: F6; the lists on screen.

### 1.6
> But look at Approximation, which got Bridget although Anita is higher on its list.
> And Anita got Control, the last job on her list, although she ranks Approximation
> higher. So these two would both rather have each other, and a matching like that
> will not hold.

- with the first word: flash the header "Approximation".
- on "which got Bridget": the row 2 cell of the Approximation column (Bridget) gets a `YELLOW_D` border, width 4.
- on "Anita is higher": the row 1 cell of the Approximation column (Anita) gets an `ORANGE` border, width 4.
- on "Anita got Control": the row 3 cell of the Anita column (Control) gets a `YELLOW_D` border, width 4.
- on "she ranks Approximation": the row 2 cell of the Anita column (Approximation) gets an `ORANGE` border, width 4.
- on "would both rather have each other": the dashed orange line D1 is drawn from the Approximation column down to the Anita header.
- uses: beat 1.5 (M1 and M3 show who has whom), the lists on screen, F7. The words "rogue couple" and "stable" are not used; they belong to episode 3.

## Scene `first_try`: heading "Let every job ask"

Stage: the layout as built. This scene adds the arrows P1, P2, P3, the legend and the
labels in slots A and B.
Kept from the scene before: the six headers, the eighteen cells with names, the strip
labels "jobs" and "candidates". Removed before beat 2.1 (at the scene change, together
with the change of heading): M1, M2, M3, D1, "matching"; the four highlighted cells are
reset. Removed at the end: nothing.

### 2.1
> So let us try the obvious thing and let every job ask for the candidate at the top
> of its list. Approximation asks Anita, Basis asks Bridget, and Control asks Anita as
> well.

- with the first word: the row 1 cell of each of the three job columns gets a `YELLOW_D` border, width 4 (Anita, Bridget, Anita).
- on "Approximation asks Anita": the arrow P1 grows from the Approximation column to the Anita header.
- on "Basis asks Bridget": the arrow P2 grows from the Basis column to the Bridget header.
- on "Control asks Anita as well": the arrow P3 grows from the Control column to the Anita header.
- uses: beats 1.2 and 1.3 (the lists), F12 (offers).

### 2.2
> Now Anita holds two offers and Christine holds none, so the obvious thing has failed.
> Anita can only take one job, so let her choose, and her own list puts Approximation
> above Control.

- with the first word: flash the header "Anita".
- on "two offers": flash the arrows P1 and P3 together.
- on "Christine holds none": flash the header "Christine".
- on "her own list": the row 2 cell (Approximation) and the row 3 cell (Control) of the Anita column get a `YELLOW_D` border, width 4.
- uses: beat 2.1 (the three arrows), beat 1.4 (Anita's list).

### 2.3
> So Anita keeps the offer from Approximation and says no to Control. Bridget has a
> single offer, from Basis, so she simply keeps that one.

- with the first word: nothing new.
- on "keeps the offer": the arrow P1 turns `GREEN_C`; the row 2 cell of the Anita column (Approximation) turns from yellow to a `GREEN_C` border, width 4.
- on "says no to Control": the arrow P3 turns `RED_C`, then fades out and is removed; the row 3 cell of the Anita column (Control) is reset; the red legend (segment and "refused") appears.
- on "she simply keeps": the arrow P2 turns `GREEN_C`; the row 2 cell of the Bridget column (Basis) gets a `GREEN_C` border, width 4.
- uses: beat 2.2 (Anita's choice), F9, F12 (in hand, rejected).

### 2.4
> Notice that Anita has not said yes. Basis is at the top of her list and might still
> ask her on a later day, so her answer is only a maybe. We say that she has the offer
> from Approximation in hand.

- with the first word: flash the header "Anita".
- on "Basis is at the top": flash the row 1 cell of the Anita column (Basis).
- on "only a maybe": flash the arrow P1 (it stays green).
- on "in hand": the green legend (segment and "in hand") appears.
- uses: beat 2.3 (the green arrow), Anita's list on screen, F9.

### 2.5
> Control has been refused, so there is no point in asking Anita again. It crosses her
> off its list, and the best candidate it has left is Bridget.

- with the first word: flash the header "Control".
- on "crosses her": the row 1 cell of the Control column (Anita) and its name fade to opacity 0.25, and its border is reset.
- on "is Bridget": the row 2 cell of the Control column (Bridget) gets a `YELLOW_D` border, width 4.
- uses: beat 2.3 (Anita said no to Control), F10.

### 2.6
> What we just watched was one full day, so let us give its parts their names. In the
> morning every job made an offer to the best candidate still on its list. In the
> afternoon every candidate kept her best offer in hand and refused the rest. In the
> evening every refused job crossed off the candidate who said no.

- with the first word: the text "Day 1" appears in slot A.
- on "In the morning": the text "morning" appears in slot B; flash the row 1 cells of the Approximation column and of the Basis column.
- on "In the afternoon": slot B changes to "afternoon"; flash the green arrows P1 and P2.
- on "In the evening": slot B changes to "evening"; flash the faded row 1 cell of the Control column (it stays faded).
- uses: beats 2.1 to 2.5, which were this day; F8, F9, F10.

State of the stage at the end of `first_try`, for the builder to compare with a frame:
yellow borders on Approximation row 1, Basis row 1, Control row 2; Control row 1 faded;
green borders on Anita row 2 and Bridget row 2; arrows P1 and P2 green; no P3; both
legend entries; slot A "Day 1", slot B "evening".

## Scene `days`: heading "Day after day"

Stage: unchanged. This scene adds P4, then P5.
Kept from the scene before: everything. Removed at the end: nothing.

### 3.1
> On the second morning the rule is the same, so every job asks the best candidate who
> has not refused it. Approximation and Basis were never refused, so they simply repeat
> their offers to Anita and Bridget. Control asks Bridget for the first time.

- with the first word: slot A changes to "Day 2" and slot B changes to "morning".
- on "the best candidate": flash the three yellow cells (Approximation row 1, Basis row 1, Control row 2) together.
- on "repeat their offers": flash the green arrows P1 and P2 (no new arrows).
- on "Control asks Bridget": the arrow P4 grows, white, from the Control column to the Bridget header.
- uses: beat 2.6 (the morning rule), beat 2.5 (Control's list), F13 (offers).

### 3.2
> So this afternoon it is Bridget who holds two offers, one from Basis and one from
> Control. Her list puts Basis above Control, so she keeps Basis in hand and refuses
> Control.

- with the first word: slot B changes to "afternoon".
- on "holds two offers": flash the arrows P2 and P4 together.
- on "Her list puts": the row 3 cell of the Bridget column (Control) gets a `YELLOW_D` border, width 4; flash the row 2 cell of the Bridget column (Basis, green since beat 2.3).
- on "keeps Basis in hand": flash the arrow P2 (it stays green).
- on "refuses": the arrow P4 turns `RED_C`, then fades out and is removed; the row 3 cell of the Bridget column is reset.
- uses: beat 3.1 (the arrows), beat 1.4 (Bridget's list), F13.

### 3.3
> In the evening Control crosses Bridget off as well. Only one name is left on its list
> now, and that name is Christine.

- with the first word: slot B changes to "evening".
- on "crosses Bridget off": the row 2 cell of the Control column (Bridget) and its name fade to opacity 0.25, and its border is reset.
- on "that name is Christine": the row 3 cell of the Control column (Christine) gets a `YELLOW_D` border, width 4.
- uses: beat 3.2 (Bridget refused Control), F10.

### 3.4
> On the third morning Approximation asks Anita again, Basis asks Bridget again, and
> Control asks Christine. In the afternoon every candidate holds exactly one offer, so
> for the first time nobody is refused.

- with the first word: slot A changes to "Day 3" and slot B changes to "morning"; flash the green arrows P1 and P2.
- on "Control asks Christine": the arrow P5 grows, white, from the Control column to the Christine header.
- on "In the afternoon": slot B changes to "afternoon".
- on "exactly one offer": the arrow P5 turns `GREEN_C`; the row 3 cell of the Christine column (Control) gets a `GREEN_C` border, width 4.
- on "nobody is refused": flash the red legend entry (segment and "refused"), then fade it to opacity 0.3.
- uses: beat 3.3 (Control's list), the three arrows on screen (one into each candidate header), F14.

### 3.5
> Think about what a fourth day would look like. Nobody was refused, so no list changed
> in the evening, and every job would ask the same candidate again. Each candidate
> would get the same single offer, so nothing could ever change. This is where we stop,
> and each candidate accepts the offer she has in hand.

- with the first word: slot B changes to "evening".
- on "no list changed": flash the three job headers together.
- on "ask the same candidate again": flash the three yellow cells (Approximation row 1, Basis row 1, Control row 3) together.
- on "the same single offer": flash the arrows P1, P2 and P5 together.
- on "This is where we stop": slot A changes to "stop" in `GREEN_C`; the text in slot B fades out.
- on "accepts the offer": the arrows P1, P2 and P5 get stroke width 7 (they stay green).
- uses: beat 3.4 (nobody refused), beat 2.6 (the three rules), F11.

State of the stage at the end of `days`: yellow borders on Approximation row 1, Basis
row 1, Control row 3; Control rows 1 and 2 faded; green borders on Anita row 2, Bridget
row 2, Christine row 3; arrows P1, P2, P5 green and thick; slot A "stop", slot B empty;
legend "in hand" full, "refused" at opacity 0.3.

## Scene `result`: no heading until beat 4.1 names the algorithm

Stage: unchanged. At the scene change the heading "Day after day" fades out and no new
heading is shown yet; the text "stop" in slot A fades out.
Kept from the scene before: everything else. Removed at the end: nothing (the end card follows).

### 4.1
> So the result is that Approximation hires Anita, Basis hires Bridget, and Control
> hires Christine. The pair that spoiled our first matching, Approximation and Anita,
> has ended up together. This procedure is called the propose and reject algorithm,
> and it is also known as the Gale Shapley algorithm.

- with the first word: flash the three green arrows together.
- on "Approximation hires Anita": flash P1 with the headers "Approximation" and "Anita".
- on "Basis hires Bridget": flash P2 with the headers "Basis" and "Bridget".
- on "hires Christine": flash P5 with the headers "Control" and "Christine".
- on "spoiled our first matching": flash P1 again, in `ORANGE` this time (`Indicate(P1, color=ORANGE)`).
- on "propose and reject algorithm": the heading `self.heading("Propose and reject")` appears in its usual place, top left.
- on "Gale Shapley algorithm": the text `txt("also called Gale-Shapley", 24, YELLOW_D)` appears on the heading line at the top right, its right edge at x = 6.6, its centre at y = 3.5.
- uses: beat 3.5 (the accepted offers), beat 1.6 (the pair), F15, F16.

### 4.2
> Look at Control and Christine, who each ended up with the last name on their own
> list. And we watched only one example, which happened to stop after three days. Does
> this procedure always stop, and is its result always free of pairs who would both
> rather have each other? Those are the questions for the next episodes.

- with the first word: flash the headers "Control" and "Christine".
- on "the last name": flash the row 3 cell of the Control column (Christine) and the row 3 cell of the Christine column (Control) together.
- on "after three days": the text "Day 3" appears in slot A (`txt("Day 3", 26)`).
- on "always stop": the text `txt("always?", 20, YELLOW_D)` appears in slot B.
- on "free of pairs": flash the three green arrows together.
- uses: the lists on screen, F17, F15, beat 1.6 (what such a pair is). Nothing is answered here; episodes 5 and 7 answer it.

## End card

- Each morning every job makes an offer to the best candidate who has not refused it.
- Each afternoon every candidate keeps her best offer in hand and refuses the rest.
- Each evening a refused job crosses that candidate off, and the days stop when nobody is refused.
- In our example it stopped on day three with Approximation and Anita, Basis and Bridget, Control and Christine.

## Author's check, each answered yes

- The first beat shows one concrete case with real names, before any definition. Yes.
- Every "uses" line names an earlier beat, a fact row, or what is on the screen. Yes.
- A name or formula is introduced after the beat where the viewer sees it happen. Yes: "in hand" in 2.4 after 2.3, the parts of the day in 2.6 after 2.1 to 2.5, the algorithm's name in 4.1.
- Every beat has a drawn object that changes; no beat is words on an empty stage. Yes.
- Every phrase after "on" is copied from its own beat, and appears there once. Yes, checked by script.
- A beat over fourteen seconds (about thirty-five words) has at least two changes. Yes; the beats over fifty words have four or more.
- If the voice counts things, the stage shows exactly that many, separately visible. Yes: three job headers, three candidate headers, two arrows into Anita (2.2), two into Bridget (3.2), one into each candidate (3.4).
- No step is skipped: every claim follows from an earlier beat or the screen by one move, and every step the notes left out is in "Added to the notes". Yes.
- Every item of the notes in the source range is in a beat or in "Left out". Yes.
- Narration: 19 beats, every beat two to four sentences, no sentence over 25 words, no digit, no colon, no symbol. Yes, checked by script.
