# BOARD: episode 02, The Residency Match

Source: `notes.txt` lines 101 to 132 (with one sentence each from lines 109, 168 to 171 and 472). Language: en. Aim: 4 to 5 minutes (about 620 words).
File `ep02_residency_match.py`, class `Ep02ResidencyMatch`. Scenes, in order: `hook`, `race`, `fuse`, `match`.

The builder copies every narration line (the lines that start with a greater-than sign)
into a `say()` unchanged, one beat per `say()`, and builds exactly the stage described.
It decides nothing; an unclear line is a question in its report.

Format, read by `check.py`: a line that starts with three hash signs opens a beat, and
every line after it that starts with a greater-than sign is that beat's narration.
Neither is used anywhere else in this file.

## Facts

| id | Fact, with all its conditions | Notes line | Computed how |
|---|---|---|---|
| F1 | The residency match pairs medical school graduates with residency slots (internships) at teaching hospitals. Graduates and hospitals submit ordered preference lists, and a computer produces the stable matching. | 107 to 110 | stated |
| F2 | Residency programs were first introduced about a century ago. | 111 to 112 | stated |
| F3 | Interns were a source of cheap labour for hospitals, and soon the number of residency slots exceeded the number of medical graduates, which led to fierce competition. | 112 to 113 | stated |
| F4 | Hospitals tried to outdo each other by making their offers earlier and earlier. By the mid-1940s offers were made by the beginning of the junior year of medical school, and some hospitals were contemplating offers to sophomores. | 113 to 116 | stated |
| F5 | The American Medical Association prohibited medical schools from releasing student transcripts and reference letters until the senior year. | 116 to 117 | stated |
| F6 | After that, hospitals made "short fuse" offers, so that a hospital whose offer was rejected could still find other interns; students were given only a few hours to decide. | 121 to 124 | stated |
| F7 | In the early 1950s this led to a centralized system, the National Residency Matching Program (N.R.M.P.), in which hospitals ranked the residents and residents ranked the hospitals. Its pairing was at first not stable. | 125 to 128 | stated |
| F8 | In 1952 the N.R.M.P. switched to the Propose-and-Reject algorithm, resulting in a stable matching. | 128 to 129 | stated |
| F9 | In 2012 Lloyd Shapley and Alvin Roth won the Nobel Prize in Economic Sciences by extending the Propose-and-Reject algorithm. | 130 to 132 | stated |
| F10 | From 1952 to 2012 is sixty years. | from F8, F9 | `2012 - 1952 == 60` |
| F11 | A pair who both prefer each other to their partners can leave the official matching: the candidate reneges, the employer fires its hire. | 168 to 171 (footnote 3) | stated |
| F12 | Everything happens inside a computer; none of the intermediate offers are made to humans, only the final one. | 472 (footnote 5) | stated |
| F13 | In propose and reject a candidate answers "maybe" and keeps her best offer in hand. | 65 to 67 (episode 1) | stated |

```python
assert 2012 - 1952 == 60
```

## Added to the notes

Steps the notes skip and this episode works out. The notes tell the history as a list
of events; the episode gives each event its reason. Every reason below is the author's
reading, not a historical claim of the notes, and is worded as reasoning ("think like a
hospital"), not as a fact about what people said at the time.

| Beat | The step that was missing | Why it holds |
|---|---|---|
| 2.2 | Why "more slots than graduates" makes hospitals move their offers earlier. | A slot whose hospital waits may find its preferred graduates already taken, so asking before the others is the safe move for each single hospital. |
| 2.3 | "Two years before graduation." | Read off the timeline on screen: the junior year and the senior year lie between the offer and graduation. That medical school has four years, with the second called sophomore, the third junior and the fourth senior, is the author's own knowledge (the notes use the three words without numbering them). |
| 2.4 | Why an early offer is bad, and why holding back transcripts ends the race. | So early, the hospital knows little about the student; without transcript and letters it has nothing to base an early offer on. |
| 3.1 | Why the deadline appears. | The notes give the reason in half a sentence (line 121): a hospital whose offer is rejected late has lost its other choices meanwhile. The picture shows two other graduates being taken. |
| 3.2 | Why a few hours is bad for the student. | She must answer before a hospital she prefers has answered her. |
| 3.3 | The link to episode 1: the short deadline removes exactly the answer "maybe" (F13). | The afternoon rule of propose and reject lets a candidate keep an offer in hand while better ones can still arrive; a deadline of hours does not. |
| 4.2 | Why a pairing with a pair who both prefer each other is a problem for a central system. | F11: such a pair can ignore the result and deal directly, which is the private market again. |
| 4.4 | "Sixty years later." | F10. |

## Left out, and why

| Item of the notes | Line | Reason |
|---|---|---|
| "Why study stable matchings in the first place?" as a question to the reader | 101 to 104 | The episode answers it without asking it. |
| The words "residents", "applicants", "interns", "students" for the same people | 108 to 127 | One name per thing: "graduates" for the people, "slots" and "hospitals" for the other side. |
| The words "short fuse" | 121 | Said as "a deadline" and "a few hours"; the idiom adds nothing the picture needs. |
| "(The moral of the story? Careful modeling with appropriate abstractions pays off.)" | 132 | An opinion, not a step of the story. |
| Later changes to the program (students proposing since the 1990s, married couples) | 455 to 460 | They need the idea of an optimal matching; episode 10. |

## Layout used by every scene

Two different stages. Stage one is used by `hook`, `race` and `fuse`. Stage two is used
by `match`. Nothing but the scene heading is above y = 2.7, nothing is below y = -2.7.
A text inside a box is scaled down, if needed, to at most the box width minus 0.4.

Colours: hospital side blue `BLUE_C`; graduate side gold `GOLD_C`; plain border
`GREY_B` width 2; looked at `YELLOW_D`; in hand or stable `GREEN_C`; trouble `RED_C`;
"would rather" and "deadline" `ORANGE`.

Stage one.

- Timeline, five boxes 2.2 wide and 0.7 high at y = 1.9, each with its label
  `txt(label, 22)` at its centre:

| x | label | border |
|---|---|---|
| -4.8 | first year | `GREY_B` |
| -2.4 | sophomore | `GREY_B` |
| 0.0 | junior | `GREY_B` |
| 2.4 | senior | `GREY_B` |
| 5.0 | residency | `BLUE_C`, fill `BLUE_C` opacity 0.15 |

- Caption `txt("medical school", 20, GREY_B)` at (-1.2, 2.5).
- Offer marker: `Arrow((x, 0.75), (x, 1.5), buff=0, color=YELLOW_D, stroke_width=5)` with
  `txt("offer", 20, YELLOW_D)` at (x, 0.5), grouped, moved together along x only.
- Slots: five squares, side 0.7, border `BLUE_C` width 3, fill `BLUE_C` opacity 0.15,
  at y = -0.7 and x = -4, -2, 0, 2, 4. No text inside.
- Graduates: three circles, radius 0.35, border `GOLD_C` width 3, fill `GOLD_C` opacity
  0.15, at y = -2.2 and x = -2, 0, 2. No text inside.
  (Five and three are the author's picture of "more slots than graduates"; the notes give no numbers and the voice says none.)
- Left strip, x = -6.0, every text at most 1.4 wide: `txt("slots", 22, GREY_B)` at
  (-6.0, -0.7); `txt("graduates", 22, GREY_B)` at (-6.0, -2.2); slot T at (-6.0, -1.45),
  size 20, for "a few hours" and "in hand"; slot D at (-6.0, 1.0), size 24, for a date.
- Arrows between a slot and a graduate, all `Arrow(start, end, buff=0, stroke_width=4)`:

| name | from | to |
|---|---|---|
| V1 | (-2, -1.1) | (-2, -1.8) |
| V2 | (0, -1.1) | (0, -1.8) |
| V3 | (2, -1.1) | (2, -1.8) |
| H1 | (-1.8, -1.1) | (-0.2, -1.8) |
| H2 | (-3.8, -1.1) | (-2.2, -1.8) |
| H3 | (3.8, -1.1) | (2.2, -1.8) |
| W | dashed arrow, white, from (0.25, -1.95) | (1.75, -1.1) |

  H1 is the offer the story follows (slot at x = -2 to the graduate at x = 0). H2 (slot at x = -4 to the graduate at x = -2) and H3 (slot at x = 4 to the graduate at x = 2) are other hospitals taking the other two graduates. W points from the graduate at x = 0 up to the free slot at x = 2. None of H1, H2, H3, W crosses another.
  Every dashed line of this episode is drawn so that it can be seen: `DashedLine(start, end, stroke_width=5, dash_length=0.15)` in the colour given (white, `YELLOW_D` or `ORANGE`, never grey). A dashed arrow is that line with `.add_tip(tip_length=0.25)`; if `add_tip` fails on a dashed line, put a solid `Triangle` of side 0.25 in the same colour at the end point, pointing along the line.

Stage two (scene `match` only; stage one is removed first).

- Centre box: `RoundedRectangle(width=3.6, height=1.2)` at (0, 1.6), border `GREY_B`
  width 3, with `txt("N.R.M.P.", 26)` at (0, 1.82). A second text line goes at (0, 1.32), size 20.
- Hospitals: three squares, side 0.7, blue as above, at x = -3.5 and y = 0.2, -1.0, -2.2,
  called hospital 1, 2, 3 from the top. Caption `txt("hospitals", 20, GREY_B)` at (-3.5, 0.95).
- Graduates: three circles, radius 0.35, gold as above, at x = 3.5 and y = 0.2, -1.0, -2.2,
  called graduate 1, 2, 3 from the top. Caption `txt("graduates", 20, GREY_B)` at (3.5, 0.95).
- Date slot at (-5.8, 1.6), size 24. Word slot at (-5.8, -1.0), size 22.
- Top line: a text at (0, 2.48), size 20.
- Lines between the two columns, width 4:

| name | kind | from | to |
|---|---|---|---|
| L1 | white line | (-3.1, 0.2) | (3.1, -1.0) |
| L2 | white line | (-3.1, -1.0) | (3.1, 0.2) |
| L3 | white line | (-3.1, -2.2) | (3.1, -2.2) |
| D | dashed line, `ORANGE`, width 5, dash length 0.15 | (-3.1, 0.2) | (3.1, 0.2) |
| G1 | line, `GREEN_C` | (-3.1, 0.2) | (3.1, 0.2) |
| G2 | line, `GREEN_C` | (-3.1, -1.0) | (3.1, -1.0) |

  D and G1 have the same end points: D is removed before G1 is created.

Rules for the builder that come from the check script:
- To highlight a box, change the stroke of the box itself (`set_stroke`). Never put a second shape of the same size on top.
- Never draw a line through a text.
- "Flash" means `Indicate(obj, color=YELLOW_D, scale_factor=1.1)`; the object returns to the look it had.
- When the text in a slot changes, fade the old one out and the new one in at the same place in one animation.
- Where a beat ends a scene, hold until the voice has finished the beat, and only then remove things and change the heading.

## Scene `hook`: heading "Who gets which hospital?"

Stage: stage one, empty at the start. Built in beat 1.1.
Kept from the scene before: nothing. Removed at the end: hold until the voice has
finished beat 1.2, then remove V1, V2, V3.

### 1.1
> Every year, medical students who finish school need a place at a teaching hospital,
> which is called a residency. So on one side there are residency slots, and on the
> other side there are graduates.

- with the first word: the caption "medical school" and the four school boxes appear, left to right (first year, sophomore, junior, senior).
- on "is called a residency": the blue box "residency" appears at the right end of the timeline.
- on "residency slots": the five slot squares and the strip label "slots" appear.
- on "there are graduates": the three graduate circles and the strip label "graduates" appear.
- uses: F1. Nothing here that the viewer has not seen.

### 1.2
> This is the matching problem of the last episode, with hospitals in the place of jobs
> and graduates in the place of candidates. Today a computer takes ranked lists from
> both sides and runs propose and reject on them. But the road there was long, and
> each failed attempt shows why the algorithm is built as it is.

- with the first word: nothing new.
- on "hospitals in the place of jobs": flash the five slot squares together.
- on "graduates in the place": flash the three graduate circles together.
- on "runs propose and reject": the arrows V1, V2, V3 grow, in `GREEN_C`, from the slots at x = -2, 0, 2 down to the graduates.
- on "each failed attempt": flash the four school boxes of the timeline, left to right.
- uses: episode 1 (jobs, candidates, propose and reject), F1.

## Scene `race`: heading "Earlier and earlier"

Stage: stage one. This scene adds the offer marker, the date in slot D and the red bar.
Kept from the scene before: timeline, caption, slots, graduates, strip labels.
Removed at the end: hold until the voice has finished beat 2.4, then remove V1, V2, V3
and the text in slot D, and set the border of the slots at x = -4 and x = 4 back to `BLUE_C`.

### 2.1
> Residencies began about a century ago, and hospitals liked them, because an intern is
> cheap labour. Soon there were more slots than graduates to fill them.

- with the first word: flash the box "residency".
- on "cheap labour": flash the five slot squares together.
- on "more slots than graduates": the slots at x = -4 and x = 4, which have no graduate below them, get a `RED_C` border, width 4.
- uses: F2, F3, the five slots and three graduates on screen.

### 2.2
> Now think like one of these hospitals, which does not want to be left with an empty
> slot. If it waits, the graduates it wants may already have said yes to another
> hospital. So the safe move is to make its offer a little earlier than everybody else.

- with the first word: flash the slot at x = -4.
- on "If it waits": the arrows V1, V2, V3 grow, white, from the slots at x = -2, 0, 2 to the three graduates; no graduate is left for the slot at x = -4.
- on "a little earlier": the offer marker appears at x = 3.3 (under the right end of the "senior" box) and slides left to x = 2.4.
- uses: beat 2.1 (two slots without a graduate). The step is in "Added to the notes".

### 2.3
> But every hospital thinks the same way, so the offers crept earlier year after year.
> By the middle of the nineteen forties they arrived at the beginning of the junior
> year, two years before graduation. Some hospitals were even thinking about asking
> sophomores.

- with the first word: the offer marker slides from x = 2.4 to x = 1.4 (left end of the "senior" box).
- on "nineteen forties": the text "mid-1940s" appears in slot D.
- on "beginning of the junior year": the offer marker slides to x = -1.0 (left end of the "junior" box).
- on "two years before graduation": flash the boxes "junior" and "senior" together.
- on "asking sophomores": a dashed arrow pointing up appears under the "sophomore" box, `DashedLine((-2.4, 0.75), (-2.4, 1.5), color=YELLOW_D, stroke_width=5, dash_length=0.15).add_tip(tip_length=0.25)`, in the same place and of the same length as the solid offer marker would be, and that box is flashed.
- uses: beat 2.2 (why offers move), F4, the timeline on screen.

### 2.4
> An offer that early is a bet on a student the hospital hardly knows yet. So the
> American Medical Association stepped in, and told the schools to keep transcripts and
> reference letters locked up until the senior year. Without those papers an early
> offer had nothing to stand on, and the race to be first was over.

- with the first word: flash the offer marker.
- on "American Medical Association": a red bar `Line((1.2, 1.45), (1.2, 2.35), color=RED_C, stroke_width=6)` is drawn in the gap between the boxes "junior" and "senior".
- on "locked up until the senior year": the boxes "first year", "sophomore" and "junior", with their labels, fade to opacity 0.3.
- on "the race to be first was over": the dashed arrow under "sophomore" is removed and the offer marker slides back to x = 2.4.
- uses: beat 2.3 (where the marker stands), F5.

## Scene `fuse`: heading "A few hours to decide"

Stage: stage one. This scene adds H1, H2, H3, W and the text in slot T.
Kept from the scene before: the timeline with its three faded boxes and the red bar,
the offer marker at x = 2.4, slots, graduates, strip labels.
Removed at the end: hold until the voice has finished beat 3.3, then remove everything
on the stage (stage two is built from nothing).

### 3.1
> But now every hospital was making its offers in the same short season. A hospital
> whose offer sat unanswered could lose its second and third choices to other hospitals
> in the meantime. So hospitals attached a deadline to every offer, and in the end a
> student had only a few hours to say yes or no.

- with the first word: flash the box "senior" and the offer marker.
- on "sat unanswered": the arrow H1 grows, white, from the slot at x = -2 to the graduate at x = 0.
- on "second and third choices": the arrows H2 (slot at x = -4 to graduate at x = -2) and H3 (slot at x = 4 to graduate at x = 2) grow in `GREY_B`, width 4: the other two graduates are taken by other hospitals. Grey, not green: green is kept for "in hand" in beat 3.3.
- on "only a few hours": H1 turns `ORANGE`, and the text "a few hours" appears in slot T in `ORANGE`.
- uses: beat 2.4 (all offers now fall in the senior year), F6.

### 3.2
> Now look at it from the side of the graduate. She has an offer in front of her, and a
> hospital she likes more has not answered yet. With a few hours on the clock she must
> take it or risk ending up with nothing.

- with the first word: flash the graduate circle at x = 0.
- on "an offer in front of her": flash H1 (it stays orange).
- on "a hospital she likes more": the slot at x = 2 gets a `YELLOW_D` border, width 4, and the dashed white arrow W is drawn from the graduate at x = 0 up to that slot (width 5, dash length 0.15, with a tip).
- on "take it or risk": flash H1 again.
- uses: beat 3.1 (the orange offer and its deadline).

### 3.3
> Compare that with the candidates in the last episode, who could answer maybe and keep
> an offer in hand while better ones arrived. The short deadline took exactly that
> answer away. So the missing piece was a way to hold an offer without closing the door.

- with the first word: nothing new.
- on "keep an offer in hand": H1 turns `GREEN_C` and grows to stroke width 8, and is flashed once at that moment (`Indicate(H1, color=GREEN_C)`); slot T changes to "in hand" in `GREEN_C`. H1 is now the only green thing on the stage.
- on "took exactly that answer away": H1 turns back to `ORANGE` and to stroke width 4, and slot T changes back to "a few hours" in `ORANGE`.
- on "without closing the door": flash the dashed arrow W and the slot at x = 2.
- uses: beat 3.2, F13 (episode 1, the answer "maybe").
- end of scene: hold until the voice has finished this beat, then remove everything on the stage.

## Scene `match`: heading "One central system"

Stage: stage two, built in beat 4.1 from an empty stage.
Kept from the scene before: nothing. Removed at the end: nothing (the end card follows).

### 4.1
> In the early nineteen fifties this led to one central system, called the National
> Residency Matching Program. Every hospital handed in a ranked list of graduates, and
> every graduate handed in a ranked list of hospitals.

- with the first word: the text "early 1950s" appears in the date slot; the three hospital squares with their caption and the three graduate circles with their caption appear.
- on "National Residency Matching Program": the centre box with "N.R.M.P." appears.
- on "Every hospital handed in": three small list icons (`Rectangle(width=0.35, height=0.45)`, `BLUE_C` fill opacity 0.6), one starting on each hospital square, move to the point (0, 1.0) at the bottom edge of the centre box and fade out there.
- on "every graduate handed in": three small list icons of the same size (`GOLD_C` fill opacity 0.6), one starting on each graduate circle, move to (0, 1.0) and fade out there.
- uses: beat 3.3 (what was missing), F7.

### 4.2
> The program then paired everyone up from those lists. But at first its pairing could
> contain a hospital and a graduate who would both rather have each other. That is
> exactly the trouble we met in the last episode, and such a pair has every reason to
> make a private deal again.

- with the first word: the lines L1, L2, L3 are drawn, white, from the hospital end to the graduate end.
- on "would both rather have each other": the dashed orange line D is drawn between hospital 1 and graduate 1.
- on "the trouble we met": flash D.
- on "a private deal again": L1 and L2 fade to opacity 0.3.
- uses: F7 ("at first not stable"), episode 1 beat 1.6 (such a pair), F11. Which pair it is here is a picture, not a fact; no lists are shown.

### 4.3
> In nineteen fifty-two the program switched to propose and reject. A matching with no
> such pair is called stable, and that is what the algorithm produced, so nobody had a
> reason to deal privately. The offers and the answers of maybe all happen inside the
> computer, and people only see the final result.

- with the first word: the date slot changes to "1952".
- on "switched to propose and reject": the text `txt("propose and reject", 20, YELLOW_D)` appears as the second line in the centre box, at (0, 1.32).
- on "is called stable": D, L1 and L2 are removed; then G1 and G2 are drawn in `GREEN_C` and L3 turns `GREEN_C`; the text "stable" appears in the word slot in `GREEN_C`.
- on "inside the computer": flash the centre box.
- uses: beat 4.2 (the pair), F8, F12. That the algorithm always produces a stable matching is not proved here; episode 7 proves it.

### 4.4
> Sixty years later, in twenty twelve, Lloyd Shapley and Alvin Roth received the Nobel
> Prize in economics for work that extends this algorithm. So the word that carried the
> whole story is stable. What exactly it demands of a matching is the question of the
> next episode.

- with the first word: the date slot changes to "2012".
- on "Lloyd Shapley and Alvin Roth": the text `txt("Shapley and Roth, Nobel Prize 2012", 20, YELLOW_D)` appears on the top line at (0, 2.48).
- on "is stable": flash the text "stable" in the word slot.
- on "demands of a matching": flash the three green lines G1, G2, L3 together.
- uses: F9, F10, beat 4.3 (the word "stable").

## End card

- More residency slots than graduates pushed hospitals to make offers earlier and earlier, then with deadlines of a few hours.
- In the early 1950s one central program took ranked lists from both sides, but its first pairings were not stable.
- In 1952 it switched to propose and reject, which gives a stable matching.
- In 2012 Shapley and Roth received the Nobel Prize in economics for work that extends the algorithm.

## Author's check, each answered yes

- The first beat shows one concrete case before any definition. Yes: the timeline, the slots and the graduates.
- Every "uses" line names an earlier beat, a fact row, or what is on the screen. Yes.
- A name is introduced after the beat where the viewer sees it happen. Yes: "stable" in 4.3, after the pair of 4.2 and of episode 1.
- Every beat has a drawn object that changes; no beat is words on an empty stage. Yes.
- Every phrase after "on" is copied from its own beat, and appears there once. Yes, checked by script.
- A beat over fourteen seconds has at least two changes, over twenty-six at least three. Yes, checked by script.
- If the voice counts things, the stage shows exactly that many. Yes: the voice counts nothing but "two years" (two boxes flashed in 2.3).
- No step is skipped, and every step the notes left out is in "Added to the notes". Yes.
- Every item of the notes in the source range is in a beat or in "Left out". Yes.
- Narration: 13 beats, two to four sentences each, no sentence over 25 words, no beat over 60 words, no digit, colon or symbol. Yes, checked by script.
