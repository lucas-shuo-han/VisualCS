# BOARD: episode 04, The Roommates Problem

Source: `notes.txt` lines 199 to 242. Language: en. Aim: 4 to 5 minutes (about 580 words).
File `ep04_roommates.py`, class `Ep04Roommates`. Scenes, in order: `hook`, `repair`, `none`, `lesson`.

The builder copies every narration line (the lines that start with a greater-than sign)
into a `say()` unchanged, one beat per `say()`, and builds exactly the stage described.
It decides nothing; an unclear line is a question in its report.

Format, read by `check.py`: a line that starts with three hash signs opens a beat, and
every line after it that starts with a greater-than sign is that beat's narration.
Neither is used anywhere else in this file.

## Facts

The notes call the four roommates A, B, C, D. A single capital letter is read badly by
the voice ("A and C"), so this episode calls them Amy, Ben, Cora, Dan, in that order.
This is a departure from the notes, reported.

| id | Fact, with all its conditions | Notes line | Computed how |
|---|---|---|---|
| F1 | Roommates problem: 2n people must be paired up; anyone can be paired with any of the other 2n - 1; there are no two types. Here 2n is four. | 205 to 208 | `len(PREF) + 1 == 4` |
| F2 | The lists (rebuilt from the garbled table). Amy (A): Ben, Cora, Dan. Ben (B): Cora, Amy, Dan. Cora (C): Amy, Ben, Dan. Dan (D): not specified, because it does not affect the argument. | 214 to 231 | the dict `PREF` below |
| F3 | The matching Amy with Ben, Cora with Dan contains the rogue couple Ben and Cora. | 232 to 233 | `rogue(M1) == [("Ben", "Cora")]` |
| F4 | The matching Ben with Cora, Amy with Dan contains the rogue couple Amy and Cora. | 233 to 234 | `rogue(M2) == [("Amy", "Cora")]` |
| F5 | The third matching, Amy with Cora, Ben with Dan, contains the rogue couple Amy and Ben. (The notes leave this as a concept check.) | 235 | `rogue(M3) == [("Amy", "Ben")]` |
| F6 | Four people can be paired up in exactly three ways, so there is no stable matching in this instance, whatever Dan's list is. | 231 to 235 | `len(MATCHINGS) == 3`, and the loop over Dan's six possible lists below |
| F7 | Matching up the rogue couple of M1 gives M2, of M2 gives M3, of M3 gives M1. | from F3 to F5 | `repair(M1) == M2 and repair(M2) == M3 and repair(M3) == M1` |
| F8 | The tempting argument: start with any matching; while there is a rogue couple, match that couple up; repeat. It is not sound: pairing up a rogue couple removes that one but may create new ones, so the procedure need not terminate. | 199 to 204 | stated; shown by F7 |
| F9 | The argument does not use that there are two types, so if it were sound it would also prove that roommates always have a stable matching, which F6 shows to be false. Any proof for jobs and candidates must therefore use the two types in an essential way. | 209 to 213, 236 to 240 | stated |
| F10 | The next section of the notes proves that a stable matching always exists by showing that propose and reject always outputs one. | 240 to 242 | stated (proved in episode 7) |

```python
from itertools import permutations
PREF = {"Amy": ["Ben", "Cora", "Dan"], "Ben": ["Cora", "Amy", "Dan"], "Cora": ["Amy", "Ben", "Dan"]}
M1 = {"Amy": "Ben", "Ben": "Amy", "Cora": "Dan", "Dan": "Cora"}
M2 = {"Ben": "Cora", "Cora": "Ben", "Amy": "Dan", "Dan": "Amy"}
M3 = {"Amy": "Cora", "Cora": "Amy", "Ben": "Dan", "Dan": "Ben"}
MATCHINGS = [M1, M2, M3]
PEOPLE = ["Amy", "Ben", "Cora", "Dan"]

def rogue(m, dan=("Amy", "Ben", "Cora")):
    pref = dict(PREF, Dan=list(dan))
    out = []
    for i, x in enumerate(PEOPLE):
        for y in PEOPLE[i + 1:]:
            if m[x] != y and pref[x].index(y) < pref[x].index(m[x]) and pref[y].index(x) < pref[y].index(m[y]):
                out.append((x, y))
    return out

def repair(m):
    x, y = rogue(m)[0]
    a, b = m[x], m[y]
    return {x: y, y: x, a: b, b: a}

assert len(MATCHINGS) == 3 and all(m[m[p]] == p for m in MATCHINGS for p in PEOPLE)
for dan in permutations(["Amy", "Ben", "Cora"]):      # whatever Dan's list is
    assert rogue(M1, dan) == [("Ben", "Cora")]
    assert rogue(M2, dan) == [("Amy", "Cora")]
    assert rogue(M3, dan) == [("Amy", "Ben")]
assert repair(M1) == M2 and repair(M2) == M3 and repair(M3) == M1
```

## Added to the notes

| Beat | The step that was missing | Why it holds |
|---|---|---|
| 2.1 | Why Ben and Cora are a rogue couple in the first matching (the notes state it). | Ben has Amy, his second choice, and Cora is his first. Cora has Dan, her last choice, and Ben is her second. |
| 2.2 to 2.5 | The notes say the repair procedure "may create new rogue couples" and that it is "not at all clear" that it terminates. The episode runs it on the roommates and shows that here it never terminates: three repairs lead back to the start. | F7, each repair checked in the lists on screen. |
| 2.3 | Why Amy and Cora are a rogue couple in the second matching (the notes state it). | Cora has Ben, her second choice, and Amy is her first. Amy has Dan, her last choice, and Cora is her second. |
| 2.4 | The third matching and its rogue couple, which the notes leave as a concept check. | Ben has Dan, his last choice, and Amy is his second. Amy has Cora, her second choice, and Ben is her first. F5. |
| 3.1 | That there are only three matchings. | Amy's roommate is Ben, Cora or Dan, and each choice forces the other two together. |
| 3.2, 3.3 | One reason that covers all three matchings, and why Dan's list does not matter (the notes say only that it does not affect the argument). | Whoever is with Dan prefers anyone else. Each of Amy, Ben, Cora is the first choice of one of the other two (Cora, Amy, Ben in that order), and that person is not with their first choice, since Dan has it. So the two prefer each other. Dan's list is never used. |

The order of the notes is turned round: the notes give the tempting argument first and
the roommates as its refutation; the episode starts with the roommates, lets the repair
idea come up by itself and fail, and names the general lesson at the end. Reported as a
departure.

## Left out, and why

| Item of the notes | Line | Reason |
|---|---|---|
| The general 2n people | 206 | The episode has four on screen; no claim about general n is made. |
| "Surely the answer is yes" as the notes' rhetorical setup | 200 | Replaced by trying the repair on a real case. |
| "reduces the number of rogue couples by one" | 203 | Said as "each repair gets rid of one rogue couple" in beat 2.2; no count of rogue couples is shown, because here there is exactly one before and one after. |
| Footnote 4 (the name Stable Marriage problem; packets and ports, jobs and servers, and so on) | 277 to 280 | An aside on naming; it lies outside this line range and is used in no episode. |

## Layout used by every scene

One stage, built in `hook` and kept to the end. Nothing but the scene heading is above
y = 2.7; nothing is below y = -2.7.

Colours: roommate `TEAL_C`; plain border `GREY_B` width 2; "roommate in the matching on
screen" `GREEN_C`; "would rather have" `ORANGE`; `RED_C`; flash `YELLOW_D`.

Left block, the four students: circles of radius 0.5, border `TEAL_C` width 3, fill
`TEAL_C` opacity 0.15, with the name `txt(name, 22)` at the centre (at most 0.8 wide).

| name | centre |
|---|---|
| Amy | (-5.2, 1.5) |
| Ben | (-2.0, 1.5) |
| Cora | (-2.0, -1.7) |
| Dan | (-5.2, -1.7) |

Lines between two students always run from circle edge to circle edge:
`Line(centre1, centre2, buff=0.5)`. A "pair line" is white, width 5. A "rogue line" is
`DashedLine(centre1, centre2, buff=0.5, color=ORANGE, stroke_width=5)`. The six
possible lines are called by their two names: Amy-Ben (top side), Cora-Dan (bottom
side), Ben-Cora (right side), Amy-Dan (left side), Amy-Cora and Ben-Dan (the two
diagonals). Never have a pair line and a rogue line between the same two students on
the stage at once: remove the one before creating the other.

The loop arrow: `Arc(radius=0.55, start_angle=0.6, angle=5.0, color=YELLOW_D, stroke_width=5).add_tip()`
centred at (-3.6, -0.1), the middle of the square. It is only on the stage while no
diagonal line is.

Right block, the lists, as a table of boxes. Row headers: `box_label(name, TEAL_C, w=1.4, h=0.6, font_size=22)`
at x = 0.6. Cells: `Rectangle(width=1.4, height=0.6)`, border `GREY_B` width 2, with
`txt(name, 22)` at the centre, at x = 2.2 (first choice), 3.7 (second), 5.2 (last).
Column captions `txt("first", 20, GREY_B)`, `txt("second", 20, GREY_B)`, `txt("last", 20, GREY_B)`
at y = 2.0 above the three cell columns.

| row | y | header | first | second | last |
|---|---|---|---|---|---|
| 1 | 1.3 | Amy | Ben | Cora | Dan |
| 2 | 0.4 | Ben | Cora | Amy | Dan |
| 3 | -0.5 | Cora | Amy | Ben | Dan |
| 4 | -1.4 | Dan | ? | ? | ? |

Status slot: one text at (2.9, -2.3), size 22, at most 6 wide.

Rules for the builder that come from the check script:
- To highlight a cell, change the stroke of the cell's own rectangle (`set_stroke(colour, 4)`). Never put a second rectangle on top.
- Never draw a line through a name; the lines stop at the circle edges.
- "Flash" means `Indicate(obj, color=YELLOW_D, scale_factor=1.1)`; the object returns to the look it had.
- "Reset the table" means every cell border back to `GREY_B` width 2.
- When the status text changes, fade the old one out and the new one in at the same place in one animation.
- Where a beat ends a scene, hold until the voice has finished the beat, and only then remove things and change the heading.

## Scene `hook`: heading "Four students, two rooms"

Stage: empty at the start; the four circles in beat 1.1, the table in beat 1.2.
Kept from the scene before: nothing. Removed at the end: hold until the voice has
finished beat 1.2, then change the heading; nothing is removed.

### 1.1
> Last time we asked whether every set of lists has a stable matching. Before we answer
> that, look at a close cousin of the problem. Four students, Amy, Ben, Cora and Dan,
> have to pair up as roommates. This time there are no two sides, so anybody can end up
> with anybody.

- with the first word: nothing is on the stage yet, so the circle "Amy" appears with the first word.
- on "Four students": the circles "Ben", "Cora", "Dan" appear, in that order.
- on "pair up as roommates": flash the four circles together.
- on "anybody can end up with anybody": all six lines (four sides, two diagonals) are drawn as thin grey lines (`GREY_B`, width 2), held for one second, then faded out and removed, all inside this cue.
- uses: F1; episode 3 (the question).

### 1.2
> Each of them ranks the other three. Amy would like Ben best and then Cora, Ben would
> like Cora best and then Amy, and Cora would like Amy best and then Ben. All three put
> Dan last, and we leave the list of Dan open for now.

- with the first word: the four row headers, the twelve empty cells and the three column captions appear.
- on "Amy would like Ben": "Ben" and "Cora" are written in the first and second cell of Amy's row.
- on "Ben would like Cora": "Cora" and "Amy" are written in the first and second cell of Ben's row.
- on "Cora would like Amy": "Amy" and "Ben" are written in the first and second cell of Cora's row.
- on "put Dan last": "Dan" is written in the last cell of the rows of Amy, Ben and Cora.
- on "open for now": a "?" is written in each of the three cells of Dan's row.
- uses: F2.
- end of scene: hold until the voice has finished this beat, then change the heading.

## Scene `repair`: heading "Repair the rogue couple"

Stage: circles and table as built. This scene adds pair lines, rogue lines, green and
orange cell borders, the status text and, in beat 2.5, the loop arrow.
Kept from the scene before: everything.
Removed at the end: hold until the voice has finished beat 2.5, then remove the loop
arrow and the status text and reset the table. The pair lines Amy-Ben and Cora-Dan stay.

### 2.1
> Let us start with any matching, say Amy with Ben and Cora with Dan. Ben has Amy, but
> his first choice is Cora, and Cora is stuck with her last choice, so she would gladly
> take Ben. So Ben and Cora are a rogue couple, and this matching is unstable.

- with the first word: the pair lines Amy-Ben and Cora-Dan are drawn. In the table the roommate cells get a `GREEN_C` border, width 4: Amy's first cell (Ben), Ben's second cell (Amy), Cora's last cell (Dan).
- on "his first choice is Cora": Ben's first cell (Cora) gets an `ORANGE` border, width 4.
- on "stuck with her last choice": flash Cora's last cell (Dan, green).
- on "gladly take Ben": Cora's second cell (Ben) gets an `ORANGE` border, width 4.
- on "are a rogue couple": the rogue line Ben-Cora is drawn (right side), and the status text "rogue couple" appears in `ORANGE`.
- uses: the lists on screen, F3, episode 3 (rogue couple, unstable).

### 2.2
> The obvious repair is to give the rogue couple what they want. So Ben moves in with
> Cora, and the two who are left behind, Amy and Dan, share the other room. Each repair
> gets rid of one rogue couple, so surely we run out of them in the end.

- with the first word: flash the rogue line Ben-Cora.
- on "Ben moves in with Cora": the pair lines Amy-Ben and Cora-Dan fade out and are removed; the rogue line Ben-Cora is removed and the pair line Ben-Cora is drawn in its place; the status text fades out.
- on "Amy and Dan": the pair line Amy-Dan is drawn (left side). The table is reset, then the roommate cells turn green: Amy's last cell (Dan), Ben's first cell (Cora), Cora's second cell (Ben).
- on "run out of them": flash the two pair lines together.
- uses: beat 2.1, F8 (the tempting argument).

### 2.3
> Ben is content now, but look at Cora, who has Ben and still ranks Amy above him. And
> Amy has been pushed down to her last choice, so she would gladly take Cora. The repair
> removed one rogue couple and created a new one, Amy and Cora.

- with the first word: flash Ben's first cell (Cora, green).
- on "ranks Amy above him": Cora's first cell (Amy) gets an `ORANGE` border, width 4.
- on "her last choice": flash Amy's last cell (Dan, green).
- on "gladly take Cora": Amy's second cell (Cora) gets an `ORANGE` border, width 4.
- on "created a new one": the rogue line Amy-Cora is drawn (diagonal), and the status text "rogue couple" appears in `ORANGE`.
- uses: beat 2.2 (the new matching), the lists on screen, F4.

### 2.4
> So we repair again, which puts Amy with Cora and leaves Ben with Dan. Now it is Ben
> who sits on his last choice, and Amy still ranks Ben above Cora. That makes Amy and
> Ben the next rogue couple.

- with the first word: the status text fades out.
- on "puts Amy with Cora": the pair lines Ben-Cora and Amy-Dan fade out and are removed; the rogue line Amy-Cora is removed and the pair line Amy-Cora is drawn in its place.
- on "leaves Ben with Dan": the pair line Ben-Dan is drawn (the other diagonal). The table is reset, then the roommate cells turn green: Amy's second cell (Cora), Ben's last cell (Dan), Cora's first cell (Amy).
- on "sits on his last choice": flash Ben's last cell (Dan, green); then Ben's second cell (Amy) gets an `ORANGE` border, width 4.
- on "ranks Ben above Cora": Amy's first cell (Ben) gets an `ORANGE` border, width 4.
- on "the next rogue couple": the rogue line Amy-Ben is drawn (top side), and the status text "rogue couple" appears in `ORANGE`.
- uses: beat 2.3, the lists on screen, F5.

### 2.5
> Repair once more, and Amy is with Ben and Cora is with Dan. But that is exactly the
> matching we started from. The repairs run in a circle and never finish, so this
> recipe does not always lead to a stable matching.

- with the first word: the status text fades out.
- on "Amy is with Ben": the pair lines Amy-Cora and Ben-Dan fade out and are removed; the rogue line Amy-Ben is removed and the pair line Amy-Ben is drawn in its place; the pair line Cora-Dan is drawn. The table is reset, then the roommate cells turn green as in beat 2.1: Amy's first cell, Ben's second cell, Cora's last cell.
- on "the matching we started from": the status text "back at the start" appears in `YELLOW_D`.
- on "run in a circle": the loop arrow is drawn in the middle of the square.
- on "does not always lead": flash the loop arrow.
- uses: beats 2.1 to 2.4, F7, F8.
- end of scene: hold until the voice has finished this beat, then remove the loop arrow and the status text and reset the table.

## Scene `none`: heading "No stable matching at all"

Stage: circles, table (all cells reset), and the pair lines Amy-Ben and Cora-Dan.
Kept from the scene before: those. Removed at the end: hold until the voice has
finished beat 3.3, then remove the rogue line Amy-Cora and reset the table. The pair
lines Amy-Dan and Ben-Cora and the status text stay.

### 3.1
> Maybe the recipe was just unlucky and a stable matching hides somewhere else. Let us
> count the possibilities. Amy shares with Ben, with Cora, or with Dan, and each choice
> leaves the other two no option but each other. So there are only three matchings, and
> we have just seen a rogue couple in every one of them.

- with the first word: flash the four circles together.
- on "Amy shares with Ben": flash the pair lines Amy-Ben and Cora-Dan.
- on "with Cora": the pair lines Amy-Ben and Cora-Dan are removed, and the pair lines Amy-Cora and Ben-Dan are drawn.
- on "or with Dan": the pair lines Amy-Cora and Ben-Dan are removed, and the pair lines Amy-Dan and Ben-Cora are drawn.
- on "only three matchings": the status text `txt("three matchings, each with a rogue couple", 22)` appears.
- uses: beats 2.1, 2.3, 2.4 (one rogue couple in each), F6.

### 3.2
> There is a pattern behind this. Whoever shares with Dan has landed on their last
> choice and would rather be with anyone else. Now look at the first choices, where Amy
> wants Ben, Ben wants Cora, and Cora wants Amy. So whoever is with Dan is always
> somebody's first choice.

- with the first word: nothing new.
- on "Whoever shares with Dan": flash the circle "Dan" and the pair line Amy-Dan; the three cells that say "Dan" (the last column of the rows of Amy, Ben, Cora) get a `RED_C` border, width 4.
- on "Amy wants Ben": the three cells of the first column (Ben, Cora, Amy) get a `YELLOW_D` border, width 4, one after another from the top.
- on "somebody's first choice": Cora's first cell (Amy) turns from yellow to an `ORANGE` border, width 4: on screen it is Amy who is with Dan, and Amy is Cora's first choice.
- uses: the lists on screen; the matching on screen (Amy with Dan). The step is in "Added to the notes".

### 3.3
> That somebody cannot be with their first choice, because Dan has taken it. So the two
> of them would both rather have each other, and they form a rogue couple whatever the
> list of Dan says.

- with the first word: flash the pair line Ben-Cora (Cora is with Ben, not with Amy).
- on "Dan has taken it": flash the pair line Amy-Dan.
- on "would both rather have each other": Amy's second cell (Cora) gets an `ORANGE` border, width 4, and the rogue line Amy-Cora is drawn (diagonal).
- on "whatever the list of Dan says": flash the three "?" cells of Dan's row.
- uses: beat 3.2, F6.
- end of scene: hold until the voice has finished this beat, then remove the rogue line Amy-Cora and reset the table.

## Scene `lesson`: heading "Why two sides matter"

Stage: circles, table (reset), pair lines Amy-Dan and Ben-Cora, the status text of beat 3.1.
Kept from the scene before: those. Removed at the end: nothing (the end card follows).

### 4.1
> So for roommates a stable matching does not have to exist. Now remember the repair
> recipe, which never asked who was a job and who was a candidate. If it proved that
> jobs and candidates always have a stable matching, the same words would prove it for
> roommates, and that is false.

- with the first word: nothing new.
- on "does not have to exist": the status text changes to "no stable matching" in `RED_C`.
- on "the repair recipe": the loop arrow is drawn again in the middle of the square.
- on "the same words would prove it": flash the four circles together.
- on "that is false": flash the status text.
- uses: beats 3.1 to 3.3, beat 2.5 (the recipe fails here), F9.

### 4.2
> So any proof for jobs and candidates has to use the two sides somewhere. Propose and
> reject does exactly that, because only jobs make offers and only candidates answer.
> Whether it always ends in a stable matching is what the next episodes work out.

- with the first word: the loop arrow and the pair lines Amy-Dan and Ben-Cora fade out and are removed.
- on "use the two sides": the circles "Amy" and "Ben" (top row) turn `BLUE_C` (border and fill), and the circles "Cora" and "Dan" (bottom row) turn `GOLD_C`. This is only a picture of "two sides"; the four keep their names.
- on "only jobs make offers": two white arrows grow from the top row down to the bottom row, `Arrow(centre1, centre2, buff=0.5, stroke_width=5)`: from Amy to Dan and from Ben to Cora.
- on "only candidates answer": flash the circles "Cora" and "Dan".
- on "next episodes": the status text changes to "always stable?" in `YELLOW_D`.
- uses: beat 4.1, F9, F10, episode 1 (who offers and who answers).

## End card

- Repairing a rogue couple can create a new one, so repairing again and again need not end.
- For four roommates with these lists the repairs run in a circle, and none of the three matchings is stable.
- A stable matching does not have to exist when there is only one kind of participant.
- So a proof that jobs and candidates always have a stable matching must use the two sides.

## Author's check, each answered yes

- The first beat shows one concrete case before any definition. Yes: four named students.
- Every "uses" line names an earlier beat, a fact row, or what is on the screen. Yes.
- A name is introduced after the beat where the viewer sees it happen. Yes: the general lesson (4.1, 4.2) comes after the case.
- Every beat has a drawn object that changes; no beat is words on an empty stage. Yes.
- Every phrase after "on" is copied from its own beat, and appears there once. Yes, checked by script.
- A beat over fourteen seconds has at least two changes, over twenty-six at least three. Yes, checked by script.
- If the voice counts things, the stage shows exactly that many. Yes: four circles; three matchings shown one after another in 3.1.
- No step is skipped, and every step the notes left out is in "Added to the notes". Yes.
- Every item of the notes in the source range is in a beat or in "Left out". Yes.
- Narration: 12 beats, two to four sentences each, no sentence over 25 words, no beat over 60 words, no digit, colon or symbol. Yes, checked by script.
