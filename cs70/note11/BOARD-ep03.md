# BOARD: episode 03, Rogue Couples

Source: `notes.txt` lines 143 to 198. Language: en. Aim: 4 to 5 minutes (about 580 words).
File `ep03_rogue_couples.py`, class `Ep03RogueCouples`. Scenes, in order: `hook`, `unstable`, `stable`.

The builder copies every narration line (the lines that start with a greater-than sign)
into a `say()` unchanged, one beat per `say()`, and builds exactly the stage described.
It decides nothing; an unclear line is a question in its report.

Format, read by `check.py`: a line that starts with three hash signs opens a beat, and
every line after it that starts with a greater-than sign is that beat's narration.
Neither is used anywhere else in this file.

## Facts

| id | Fact, with all its conditions | Notes line | Computed how |
|---|---|---|---|
| F1 | Each job's list, most wanted first. Approximation: Anita, Bridget, Christine. Basis: Bridget, Anita, Christine. Control: Anita, Bridget, Christine. | 154 to 167 | the dict `JOBS` below |
| F2 | Each candidate's list, most wanted first. Anita: Basis, Approximation, Control. Bridget: Approximation, Basis, Control. Christine: Approximation, Basis, Control. | 175 to 188 | the dict `CANDS` below |
| F3 | Three other ways to judge a matching: maximize the number of first choices; minimize the number of last choices; minimize the sum of the ranks of the choices. | 147 to 149 | stated |
| F4 | Definition. A job and a candidate who both prefer each other over their current partners are a rogue couple. A matching with a rogue couple is unstable; a matching of n jobs and n candidates with no rogue couple is stable. | 151 to 153 | stated |
| F5 | Why "unstable": the rogue candidate can renege and the rogue employer can fire its hire; then one job is suddenly empty and one person has just been fired. | 168 to 171 | stated |
| F6 | The matching U: Approximation with Christine, Basis with Bridget, Control with Anita. It is unstable; Approximation and Bridget are a rogue couple. | 189 to 191 | `("Approximation", "Bridget") in rogue(U)` |
| F7 | In U, Approximation and Anita are a rogue couple too, and there is no third one. | from F1, F2 | `rogue(U) == [("Approximation", "Anita"), ("Approximation", "Bridget")]` |
| F8 | The matching S: Approximation with Bridget, Basis with Anita, Control with Christine. It is stable. Approximation and Anita are no rogue couple in it, because Anita prefers Basis, which she has. | 192 to 195 | `rogue(S) == []` |
| F9 | In S, Control and Christine are both paired with their least favourite choice, and this does not violate stability. | 196 to 198 | `JOBS["Control"][-1] == S["Control"] == "Christine" and CANDS["Christine"][-1] == "Control"` |
| F10 | The matching E that propose and reject produced in episode 1 (Approximation with Anita, Basis with Bridget, Control with Christine) is stable as well, and it differs from S. | 99 for E; stability from F1, F2 | `rogue(E) == [] and E != S` |

```python
JOBS = {"Approximation": ["Anita", "Bridget", "Christine"],
        "Basis":         ["Bridget", "Anita", "Christine"],
        "Control":       ["Anita", "Bridget", "Christine"]}
CANDS = {"Anita":     ["Basis", "Approximation", "Control"],
         "Bridget":   ["Approximation", "Basis", "Control"],
         "Christine": ["Approximation", "Basis", "Control"]}
U = {"Approximation": "Christine", "Basis": "Bridget", "Control": "Anita"}
S = {"Approximation": "Bridget", "Basis": "Anita", "Control": "Christine"}
E = {"Approximation": "Anita", "Basis": "Bridget", "Control": "Christine"}

def rogue(m):                       # all rogue couples (job, candidate) of the matching m
    has = {c: j for j, c in m.items()}
    out = []
    for j in JOBS:
        for c in JOBS[j]:
            if c == m[j]:
                break               # only the names above the job's partner
            if CANDS[c].index(j) < CANDS[c].index(has[c]):
                out.append((j, c))
    return out

assert rogue(U) == [("Approximation", "Anita"), ("Approximation", "Bridget")]
assert rogue(S) == [] and rogue(E) == [] and E != S
assert JOBS["Control"][-1] == S["Control"] == "Christine" and CANDS["Christine"][-1] == "Control"
```

## Added to the notes

| Beat | The step that was missing | Why it holds |
|---|---|---|
| 2.1, 2.2 | The notes' concept check asks "Approximation Inc. and Bridget are a rogue couple, why?" and does not answer. | Approximation has Christine, row 3 of its list, and Bridget is row 2. Bridget has Basis, row 2 of her list, and Approximation is row 1. Both read off the lists on screen. |
| 2.4 | A second rogue couple in the same matching, Approximation and Anita, which the notes do not mention. | Approximation: Anita is row 1, above Christine. Anita has Control, row 3 of her list, and Approximation is row 2. F7. |
| 3.1 | A method for checking that a matching is stable. The notes check one pair (Approximation, Anita) and say a word about Control and Christine, but never check all pairs. | A rogue couple needs a job that prefers the candidate to its partner, so for each job only the names above its partner have to be asked. Here that is one name for Approximation, one for Basis, two for Control. |
| 3.3 | The check for Basis (would rather have Bridget; Bridget has her first choice) and the full check for Control (would rather have Anita or Bridget; both have their first choice). | Lists on screen; F8. |
| 3.5 | That the output of episode 1 is stable too, so this example has more than one stable matching. | In E only Control has names above its partner (Anita, Bridget); Anita has Approximation and Bridget has Basis, and each ranks Control last. F10. |

## Left out, and why

| Item of the notes | Line | Reason |
|---|---|---|
| "Next, we'd like to show that the algorithm finds a good matching" | 143 to 144 | That is episode 7; this episode only says what "good" means. |
| "rooted in the idea of autonomy" | 150 | Said in plain words in beat 1.3 ("free to act on their own"). |
| "of n jobs and n candidates" in the definition | 152 | The episode has three of each on screen; the general n is used from episode 5 on. |
| "none of their more preferred choices would rather work with them" as a sentence | 197 to 198 | Shown instead, pair by pair, in beat 3.3. |

## Layout used by every scene

One stage, built in `hook` and kept to the end. Nothing but the scene heading is above
y = 2.7; nothing is below y = -2.7. All coordinates are centres unless stated. This is
the stage of episode 1, moved down a little and with wider boxes.

Colours: job blue `BLUE_C`; candidate gold `GOLD_C`; plain cell border `GREY_B`, stroke
width 2; "partner in the matching on screen" `GREEN_C`; "would rather have" `ORANGE`;
"left behind" `RED_C`; flash `YELLOW_D`.

Three columns at x = -3.9, 0.5, 4.9. Every box is 2.4 wide. A text inside a box is
scaled down, if needed, to at most 2.0 wide.

Top half, the jobs:
- Job headers: `box_label(name, BLUE_C, w=2.4, h=0.55, font_size=22)` at y = 2.42.
- Under each header three cells: `Rectangle(width=2.4, height=0.48)`, border `GREY_B`
  width 2, no fill, at y = 1.86 (row 1), 1.35 (row 2), 0.84 (row 3), each with a name
  `txt(name, 22)` at its centre. Row 1 is the first choice.

| column | header | row 1 | row 2 | row 3 |
|---|---|---|---|---|
| x = -3.9 | Approximation | Anita | Bridget | Christine |
| x = 0.5 | Basis | Bridget | Anita | Christine |
| x = 4.9 | Control | Anita | Bridget | Christine |

Bottom half, the candidates:
- Candidate headers: `box_label(name, GOLD_C, w=2.4, h=0.55, font_size=22)` at y = -0.85.
- Under each header three cells, same size and style, at y = -1.41 (row 1), -1.92 (row 2), -2.43 (row 3).

| column | header | row 1 | row 2 | row 3 |
|---|---|---|---|---|
| x = -3.9 | Anita | Basis | Approximation | Control |
| x = 0.5 | Bridget | Approximation | Basis | Control |
| x = 4.9 | Christine | Approximation | Basis | Control |

Rank numbers (appear in beat 1.2 and stay): `txt("1", 18, GREY_B)`, `txt("2", 18, GREY_B)`,
`txt("3", 18, GREY_B)` at x = 6.45 beside the three job rows (y = 1.86, 1.35, 0.84) and
again beside the three candidate rows (y = -1.41, -1.92, -2.43). Six numbers.

The band between the halves (y from 0.60 down to -0.575) has three parts. Under the columns, from x = -5.1 to x = 6.1, it holds the lines of the table below. At its left end, in the left strip (x from -6.6 to -5.4), it holds the two text slots A and B. And in beat 3.6 one large text, the closing question, is placed between the lines E1 and E2 at (-1.7, 0.02). No line ever runs through a text.
Solid lines have width 4. The dashed lines D1 and D2 are `DashedLine(start, end, color=ORANGE, stroke_width=5, dash_length=0.15)`, so that they read as lines and not as dots.

| name | kind | from (x, y) | to (x, y) |
|---|---|---|---|
| U1 | white line, Approximation to Christine | (-3.9, 0.55) | (4.5, -0.52) |
| U2 | white line, Basis to Bridget | (0.9, 0.55) | (0.9, -0.52) |
| U3 | white line, Control to Anita | (4.9, 0.55) | (-3.5, -0.52) |
| D1 | dashed line, `ORANGE`, Approximation to Bridget | (-3.5, 0.55) | (0.1, -0.52) |
| D2 | dashed line, `ORANGE`, Approximation to Anita | (-4.3, 0.55) | (-4.3, -0.52) |
| S1 | white line, Approximation to Bridget | (-3.5, 0.55) | (0.1, -0.52) |
| S2 | white line, Basis to Anita | (0.5, 0.55) | (-3.9, -0.52) |
| S3 | white line, Control to Christine | (4.9, 0.55) | (4.9, -0.52) |
| E1 | white line, Approximation to Anita | (-4.3, 0.55) | (-4.3, -0.52) |
| E2 | white line, Basis to Bridget | (0.9, 0.55) | (0.9, -0.52) |

Pairs with the same end points (D1 and S1, D2 and E1, U2 and E2) are never on the stage
together: the first of each pair is removed at the end of scene `unstable`.

Left strip (x = -6.0, every text there, the two legend texts included, at most 1.2 wide; scale it down if it is wider, so that nothing comes closer than 0.3 to the Approximation column, whose left edge is at x = -5.1):
- `txt("jobs", 22, GREY_B)` at (-6.0, 2.42); `txt("candidates", 22, GREY_B)` at (-6.0, -0.85).
- Legend (appears in beat 2.1 and stays): a square of side 0.3 with `GREEN_C` border
  width 4 at (-6.0, 1.85) and `txt("partner", 20, GREEN_C)` at (-6.0, 1.55); a square of
  side 0.3 with `ORANGE` border width 4 at (-6.0, 1.15) and `txt("would rather", 20, ORANGE)` at (-6.0, 0.85).
- Slot A at (-6.0, 0.22), size 20. Slot B at (-6.0, -0.2), size 20.

Rules for the builder that come from the check script:
- To highlight a cell, change the stroke of the cell's own rectangle (`set_stroke(colour, 4)`). Never put a second rectangle on top of a cell.
- Never draw a line through a name.
- "Flash" means `Indicate(obj, color=YELLOW_D, scale_factor=1.1)`; the object returns to the look it had.
- "Reset a cell" means border `GREY_B` width 2.
- When the text in a slot changes, fade the old one out and the new one in at the same place in one animation.
- Where a beat ends a scene, hold until the voice has finished the beat, and only then remove things and change the heading.

## Scene `hook`: heading "What is a good matching?"

Stage: empty at the start, built in beat 1.1 as in the layout section.
Kept from the scene before: nothing. Removed at the end: hold until the voice has
finished beat 1.3, then change the heading; nothing else is removed.

### 1.1
> Here are the three jobs and the three candidates from the first episode, each with
> the same ranked list as before. The first name under a header is the favourite, and
> the last name is the least wanted.

- with the first word: the strip label "jobs", the three job headers and their nine cells with names appear, column by column from the left.
- on "the three candidates": the strip label "candidates", the three candidate headers and their nine cells with names appear, column by column from the left.
- on "is the favourite": flash the six row 1 cells together.
- on "least wanted": flash the six row 3 cells together.
- uses: F1, F2; episode 1.

### 1.2
> What should a good matching do for them? We could give as many of them as possible
> their first choice, or as few as possible their last choice. Or we could add up how
> far down its list everybody lands, and make that total small.

- with the first word: flash the six headers together.
- on "their first choice": the six row 1 cells get a `YELLOW_D` border, width 4 (not green: green gets its meaning in beat 2.1).
- on "their last choice": the six row 1 cells are reset, and the six row 3 cells get a `RED_C` border, width 4.
- on "add up how far down": the six row 3 cells are reset, and the six rank numbers appear at the right of the rows.
- uses: F3; the lists on screen.

### 1.3
> But all of these are scores handed down from above, and jobs and candidates are free
> to act on their own. So let us look at one matching through their eyes.

- with the first word: flash the six rank numbers together.
- on "free to act": flash the three job headers and the three candidate headers together.
- on "through their eyes": flash the header "Approximation".
- uses: beat 1.2 (the three scores).
- end of scene: hold until the voice has finished this beat, then change the heading.

## Scene `unstable`: heading "A pair that walks away"

Stage: the layout as built. This scene adds U1, U2, U3, D1, D2, the legend, and texts in slots A and B.
Kept from the scene before: everything.
Removed at the end: hold until the voice has finished beat 2.4, then remove U1, U2, U3,
D1, D2 and the texts in slots A and B, and reset all eighteen cells.

### 2.1
> Take this matching, where Approximation has Christine, Basis has Bridget, and Control
> has Anita. Start with Approximation, which sits at the bottom of its own list with
> Christine, so it would rather have Bridget.

- with the first word: the legend (both squares and both texts) appears in the left strip.
- on "Approximation has Christine": the line U1 is drawn; row 3 of the Approximation column (Christine) and row 1 of the Christine column (Approximation) get a `GREEN_C` border, width 4.
- on "Basis has Bridget": the line U2 is drawn; row 1 of the Basis column (Bridget) and row 2 of the Bridget column (Basis) get a `GREEN_C` border, width 4.
- on "has Anita": the line U3 is drawn; row 1 of the Control column (Anita) and row 3 of the Anita column (Control) get a `GREEN_C` border, width 4.
- on "would rather have Bridget": row 2 of the Approximation column (Bridget) gets an `ORANGE` border, width 4.
- uses: F6; the lists on screen (Bridget is above Christine in Approximation's column).

### 2.2
> But wanting is not enough, because Bridget has to want it too. Bridget has Basis, the
> second name on her list, and the first name on her list is Approximation. So
> Approximation and Bridget would both rather have each other, and they can simply walk
> away from this matching together.

- with the first word: flash the header "Bridget".
- on "Bridget has Basis": flash row 2 of the Bridget column (Basis, green).
- on "the first name on her list": row 1 of the Bridget column (Approximation) gets an `ORANGE` border, width 4.
- on "would both rather have each other": the dashed orange line D1 is drawn from the Approximation column to the Bridget header.
- uses: beat 2.1 (Approximation's side), Bridget's list on screen, F6.

### 2.3
> And look what that does to the others. Approximation drops Christine, who is suddenly
> without a job, and Bridget leaves Basis, which suddenly has an empty position. A pair
> like this is called a rogue couple, and a matching that contains one is called
> unstable.

- with the first word: flash the dashed line D1.
- on "drops Christine": the line U1 turns `RED_C` and fades to opacity 0.3; the border of the header "Christine" turns `RED_C`.
- on "leaves Basis": the line U2 turns `RED_C` and fades to opacity 0.3; the border of the header "Basis" turns `RED_C`.
- on "rogue couple": the text "rogue couple" appears in slot A in `ORANGE`.
- on "called unstable": the text "unstable" appears in slot B in `RED_C`.
- uses: beat 2.2 (the pair), F4, F5.

### 2.4
> Is that the only rogue couple here? Approximation also ranks Anita above Christine,
> and Anita, who has Control at the bottom of her list, ranks Approximation above it. So
> Approximation and Anita are a second rogue couple, and one is already enough to make
> a matching unstable.

- with the first word: the lines U1 and U2 return to white at full opacity, and the borders of the headers "Christine" and "Basis" return to `GOLD_C` and `BLUE_C`.
- on "ranks Anita above Christine": row 1 of the Approximation column (Anita) gets an `ORANGE` border, width 4.
- on "ranks Approximation above it": row 2 of the Anita column (Approximation) gets an `ORANGE` border, width 4.
- on "second rogue couple": the dashed orange line D2 is drawn from the Approximation column to the Anita header.
- on "already enough": flash the text "unstable" in slot B.
- uses: the lists on screen, the green cells of beat 2.1, F7, F4.
- end of scene: hold until the voice has finished this beat, then remove U1, U2, U3, D1, D2 and the texts in slots A and B, and reset all eighteen cells.

## Scene `stable`: heading "No pair walks away"

Stage: the layout, with all cells reset and the gap empty. The legend and the rank numbers stay.
Kept from the scene before: headers, cells, strip labels, legend, rank numbers.
Removed at the end: nothing (the end card follows).

### 3.1
> Now try a different matching, where Approximation has Bridget, Basis has Anita, and
> Control has Christine. To hunt for a rogue couple we can go through the jobs one at a
> time. A job only prefers the names above its partner, so those are the only
> candidates we need to ask.

- with the first word: nothing new.
- on "Approximation has Bridget": the line S1 is drawn; row 2 of the Approximation column (Bridget) and row 1 of the Bridget column (Approximation) get a `GREEN_C` border, width 4.
- on "Basis has Anita": the line S2 is drawn; row 2 of the Basis column (Anita) and row 1 of the Anita column (Basis) get a `GREEN_C` border, width 4.
- on "Control has Christine": the line S3 is drawn; row 3 of the Control column (Christine) and row 3 of the Christine column (Control) get a `GREEN_C` border, width 4.
- on "the names above its partner": flash the four cells that lie above a green cell in the job columns: Approximation row 1, Basis row 1, Control row 1 and Control row 2.
- uses: F8, F4 (what a rogue couple is).

### 3.2
> Approximation has Bridget and would rather have Anita. But Anita has Basis, the very
> first name on her list, so she will not move. That is why Approximation and Anita are
> no rogue couple here.

- with the first word: flash the header "Approximation".
- on "would rather have Anita": row 1 of the Approximation column (Anita) gets an `ORANGE` border, width 4.
- on "Anita has Basis": flash row 1 of the Anita column (Basis, green).
- on "no rogue couple here": row 1 of the Approximation column is reset.
- uses: beat 3.1 (the method), Anita's list on screen, F8.

### 3.3
> Basis has Anita and would rather have Bridget, but Bridget has Approximation, which is
> first on her list, so she stays too. Control would rather have Anita or Bridget, and
> we have just seen that each of them holds her first choice.

- with the first word: flash the header "Basis".
- on "would rather have Bridget": row 1 of the Basis column (Bridget) gets an `ORANGE` border, width 4.
- on "she stays too": flash row 1 of the Bridget column (Approximation, green); then row 1 of the Basis column is reset.
- on "Control would rather": rows 1 and 2 of the Control column (Anita, Bridget) get an `ORANGE` border, width 4.
- on "holds her first choice": flash row 1 of the Anita column and row 1 of the Bridget column together; then rows 1 and 2 of the Control column are reset.
- uses: beat 3.2, the lists on screen, F8.

### 3.4
> So every job has been checked and no rogue couple turned up, and a matching with no
> rogue couple is called stable. Notice that Control and Christine are both stuck with
> the last name on their lists. So stable does not mean everyone is happy, only that
> nobody can find a partner who wants to leave with them.

- with the first word: flash the three job headers together.
- on "is called stable": the text "stable" appears in slot A in `GREEN_C`.
- on "Control and Christine": flash the headers "Control" and "Christine".
- on "the last name on their lists": flash row 3 of the Control column and row 3 of the Christine column together (both green).
- on "wants to leave with them": flash the lines S1, S2, S3 together.
- uses: beats 3.2 and 3.3 (all four names asked), F4, F9.

### 3.5
> This is not the matching that propose and reject gave us in the first episode. That
> one paired Approximation with Anita, Basis with Bridget, and Control with Christine.
> There, only Control has names above its partner, and Anita and Bridget each rank
> Control last, so it is stable as well.

- with the first word: flash the lines S1 and S2.
- on "paired Approximation with Anita": S1 and S2 are removed and E1 and E2 are drawn (S3 stays). The green borders move: Approximation row 2 is reset and row 1 turns green; Basis row 2 is reset and row 1 turns green; Anita row 1 is reset and row 2 (Approximation) turns green; Bridget row 1 is reset and row 2 (Basis) turns green.
- on "only Control has names above": rows 1 and 2 of the Control column (Anita, Bridget) get an `ORANGE` border, width 4.
- on "rank Control last": flash row 3 of the Anita column and row 3 of the Bridget column together (both say Control).
- on "stable as well": rows 1 and 2 of the Control column are reset; flash the text "stable" in slot A.
- uses: episode 1 (the output), the method of beat 3.1, F10.

### 3.6
> So one set of lists can have more than one stable matching. But we found both of them
> by luck and by checking. Does every set of lists have a stable matching at all?

- with the first word: nothing new.
- on "more than one": flash the text "stable" in slot A.
- on "by luck and by checking": flash the lines E1, E2, S3 together.
- on "Does every set of lists": the closing question appears large in the band between the halves, between the lines E1 and E2: `txt("does one always exist?", 30, YELLOW_D)` at (-1.7, 0.02), at most 4.2 wide. Slot B stays empty.
- uses: beats 3.4 and 3.5 (two stable matchings). Nothing is answered here; episode 4 takes up the question.

## End card

- A job and a candidate who would both rather have each other than their partners are a rogue couple.
- A matching with a rogue couple is unstable, and a matching with none is stable.
- To check a matching, ask for every job only the candidates above its partner.
- Stable does not mean that everyone gets their first choice, and one set of lists can have several stable matchings.

## Author's check, each answered yes

- The first beat shows one concrete case before any definition. Yes: the lists of episode 1.
- Every "uses" line names an earlier beat, a fact row, or what is on the screen. Yes.
- A name is introduced after the beat where the viewer sees it happen. Yes: "rogue couple" and "unstable" in 2.3 after 2.2; "stable" in 3.4 after the check of 3.2 and 3.3.
- Every beat has a drawn object that changes; no beat is words on an empty stage. Yes.
- Every phrase after "on" is copied from its own beat, and appears there once. Yes, checked by script.
- A beat over fourteen seconds has at least two changes, over twenty-six at least three. Yes, checked by script.
- If the voice counts things, the stage shows exactly that many. Yes: three jobs, three candidates, a second rogue couple (two dashed lines in 2.4).
- No step is skipped, and every step the notes left out is in "Added to the notes". Yes.
- Every item of the notes in the source range is in a beat or in "Left out". Yes.
- Narration: 13 beats, two to four sentences each, no sentence over 25 words, no beat over 60 words, no digit, colon or symbol. Yes, checked by script.
