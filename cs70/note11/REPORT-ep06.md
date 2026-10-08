# REPORT: The First Counterexample (CS70 Note 11, episode 06)

## Files

- Preview (480p, voiced): `C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep06\videos\ep06_well_ordering\480p15\Ep06WellOrdering.mp4`
- Subtitles: `C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep06\videos\ep06_well_ordering\480p15\Ep06WellOrdering.srt`
- Code: `cs70/note11/ep06_well_ordering.py` (class `Ep06WellOrdering`)
- Plan: `cs70/note11/BOARD-ep06.md` (STRICT.md, "With a storyboard")
- Contact sheets: `C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\`

## Sheets of the scene runs (step 4)

One row per sheet, in the order I opened them. The questions are the seven of step 5.

The hook was rebuilt once, after the sheets of run 2 showed the day row coming apart at the
hook / `same` boundary: `clear_stage` fades every mobject whose own id is not in the keep
set, and `FadeIn(VGroup(box, label))` had left a throwaway wrapper on the stage holding the
box and its label. Manim's `remove` drops only the wrapper, so the box went with it. Each
day is now one `VGroup(box, label)` built once, and the end of `hook` removes the reasoning
lines, the step arrow and the two under-labels by name. Run 4 is the render of the fixed
hook; a frame probe shows all eight boxes green and labelled from 86 s to 118 s of it.

### run 1, `--scenes hook` (before the fix) — 6 sheets, all opened

| Sheet | text over something | cut off / on subtitle | leftover | empty frame | wrong number | wrong count | only sentences | what I saw |
|---|---|---|---|---|---|---|---|---|
| `ep06_sheets_end/sheet00.png` | no | no | no | no | no | no (eight day boxes, none counted by the voice) | no | Frames 0-8. The claim line, then the eight day boxes k to k+7 appearing left to right with "offer" under box k; the legend ("claim true", "claim false") appears; box k turns green; the boxes k+4 and k+6 turn red and "first red day" appears under k+4. Nothing overlaps; the day row, the legend and the reasoning area stay clear of each other. |
| `ep06_sheets_end/sheet01.png` | no | no | no | no | no | no (one "offer", one "day before", one "first red day"; the labels sit under k, k+3 and k+4) | no | Frames 9-17. "day before" appears under box k+3, k+3 turns green, the reasoning lines R1 to R3 come in one at a time under the row, the step arrow is drawn from k+3 to k+4, k+4 turns green while "first red day" fades out and k+6 turns green. The reasoning lines are centred under the row and touch nothing. |
| `ep06_sheets_end/sheet02.png` | no | no | no | no | no | no (eight green boxes, one arrow, three reasoning lines) | no | Frame 18, the last of the scene. All eight days green, the step arrow and the three reasoning lines still up: they are removed after the voice of this beat has finished, as the board says. The frame holds the picture the voice is talking about. |
| `ep06_sheets_mid/sheet00.png` | no | no | no | no | no | no | no | Mid frames 0-8: frame 0 the claim line alone (the boxes come on the next cue), frame 1 the day row half-faded in, frame 4 box k mid-`Indicate`, frame 8 the two red days half-grown. Half-faded objects are mid-animation, not leftovers. |
| `ep06_sheets_mid/sheet01.png` | no | no | no | no | no | no | no | Mid frames 9-17: frame 9 box k+4 mid-`Indicate`, frame 15 the step arrow half-drawn, frame 16 box k+4 mid-`Indicate` over its red fill, frame 17 the four undecided boxes going green one after another. |
| `ep06_sheets_mid/sheet02.png` | no | no | no | no | no | no | no | Mid frame 18: the same picture as the end frame with the claim line mid-`Indicate` (the flash of "a second time"). Nothing left over. |

### run 2, `--scenes same` (before the fix) — 2 sheets, all opened

| Sheet | text over something | cut off / on subtitle | leftover | empty frame | wrong number | wrong count | only sentences | what I saw |
|---|---|---|---|---|---|---|---|---|
| `ep06_sheets_end/sheet00.png` | no | no | no | no | no | no | no | Frames 0-5. The scene's heading, the claim line, the legend and the pairs all in place; but in frames 0-2 the day row is only part green (boxes k+3, k+4, k+6 filled, box k missing, k+1, k+2, k+5, k+7 without fill). This became the defect below. |
| `ep06_sheets_mid/sheet00.png` | no | no | no | no | no | no | no | Mid frames 0-5: frame 0 box k mid-`Indicate` (yellow frame), frame 3 the forward pair half-faded in, frame 4 the row mid-flash ("runs on forever"). Same part-green row in frames 0-2. |

**Defect found here, and fixed.** Box k with its label, and the green of boxes k+1, k+2, k+5,
k+7, were being removed at the hook / `same` boundary, and came back only when a later
`Indicate` touched them. A frame probe of a faithful `--scenes hook same` render put the
loss at 87.75 s, the hook's `clear_stage`. See `TRIAL_LOG-ep06.md` runs 2 to 5.

### run 4, `--scenes hook same` (fixed) — 6 sheets, all opened

| Sheet | text over something | cut off / on subtitle | leftover | empty frame | wrong number | wrong count | only sentences | what I saw |
|---|---|---|---|---|---|---|---|---|
| `ep06_sheets_end/sheet00.png` | no | no | no | no | no | no (eight boxes, none counted) | no | Frames 0-8, the hook as in run 1: the claim line, the eight boxes with "offer" under box k, the legend, box k green, k+4 and k+6 red with "first red day". This time the boxes and labels are steady throughout. |
| `ep06_sheets_end/sheet01.png` | no | no | no | no | no | no (one "offer", one "day before", one "first red day") | no | Frames 9-17: k+4 flashing among the red days, k and k+4 compared, "day before" under k+3, k+3 green, R1 to R3 appearing in order, the step arrow drawn from k+3 to k+4, k+4 keeping its red fill and taking a green stroke, k+6 going green. |
| `ep06_sheets_end/sheet02.png` | no | no | no | no | no | no | no | Frames 18-24. Frame 18 ends the hook (A second proof, all eight green, the reasoning lines and the arrow still up). Frame 19 is the first frame of `same`: heading "One proof, two directions", the reasoning lines and step arrow gone, the top text, the day row (all eight green, all eight labelled) and the legend kept, exactly what the board says is kept. Frames 19-21 bring the backward pair ("never") with its caption; 22-23 the forward pair with its caption; 24 both pairs, the last frame of the scene. |
| `ep06_sheets_mid/sheet00.png` | no | no | no | no | no | no | no | Mid frames 0-8: frame 0 the claim line alone, frame 1 the boxes half in, frame 2 the boxes mid-`Indicate`, frame 4 box k mid-`Indicate`, frame 6 box k green, frame 8 the two red days. |
| `ep06_sheets_mid/sheet01.png` | no | no | no | no | no | no | no | Mid frames 9-17: frame 9 k+4 mid-`Indicate`, frame 11 "day before" fading in under k+3, frame 15 the step arrow mid-`Create`, frame 16 k+4 mid-`Indicate` over its red fill, frame 17 k+6 mid-recolour. |
| `ep06_sheets_mid/sheet02.png` | no | no | no | no | no | no | no | Mid frames 18-24: frame 20 box k mid-`Indicate` on "the day of the offer" (yellow frame, the words it answers to), frame 22 the row mid-flash on "runs on forever", frame 23 the backward pair mid-`Indicate` on "a first red day would need", frame 24 both captions mid-flash on "two directions". |

The picture of these sheets was checked against the video itself, frame by frame: box k
goes green inside the caption "So let us paint that day green."; k+4 and k+6 go red inside
"Then on some later days the claim fails, so let us paint those days red"; k+4 flashes
inside "Among the red days, look at the first one."; k and k+4 flash together on the first
words of "The first red day is not the day of the offer"; k+3 goes green inside "The claim
is true on the day before."; k+4 takes its green stroke while keeping its red fill inside
"Then she keeps it or something better"; and its fill goes green inside "But a day cannot be
red and green at once". In `same`, the backward pair appears inside "never" and the forward
pair inside "green today forces green tomorrow", and the row is green without a break from
86 s to 118 s. Every change lands in the caption whose words ask for it.

### run 5, `--scenes least` — 4 sheets, all opened

| Sheet | text over something | cut off / on subtitle | leftover | empty frame | wrong number | wrong count | only sentences | what I saw |
|---|---|---|---|---|---|---|---|---|
| `ep06_sheets_end/sheet00.png` | no | no | no | no | no | no | no | Frames 0-8. Frame 0 the number line, its thirteen ticks and the labels 0 to 12, the first frame of the scene. Frame 1 the red dots at 4 and 6 (4 flashing), frame 2 the question "does every set of natural numbers have a smallest element?" above them, frame 3 the question with the dots gone, frame 4 the set text `{5, 2, 11, 7, 8}` with five blue dots, frame 5 the dot at 2 green with "smallest element: 2", frame 6 the set with the dots going out, frames 7 and 8 the odd numbers 1, 3, 5, 7, 9, 11 with 1 green and then the primes 2, 3, 5, 7, 11 with 2 green, each with its own result line. The dots sit on the line, not the line on the dots; the labels are clear of the line. |
| `ep06_sheets_end/sheet01.png` | no | no | no | no | no | no (five primes, one of them green, one yellow; five labels of the principle area) | no | Frames 9-15. Frame 10 the dot at 11 yellow on "say eleven", frame 12 "Well-Ordering Principle" appearing, frame 13 the second principle line under it, frames 14 and 15 the prime dots replaced by the red dots at 4 and 6 (4 flashing on "a first red day"). The principle line at y = -2.1 and the subtitle at the bottom of the frame do not touch. |
| `ep06_sheets_mid/sheet00.png` | no | no | no | no | no | no | no | Mid frames 0-8: frame 0 the bare number line, frame 1 the red dots half in, frame 2 the question half in, frame 4 the five dots coming in one after another, frame 5 the green dot at 2 with the result line, frame 6 the dots half out, frames 7 and 8 the odd dots and then the primes coming in. All half-states are mid-animation, none is a leftover. |
| `ep06_sheets_mid/sheet01.png` | no | no | no | no | no | no | no | Mid frames 9-15: frame 10 the dot at 11 mid-`Indicate`, frame 11 the tick labels 2, 3, 5 and 7 brighter than the rest (the "finitely many" sweep, right to left, mid-way), frame 12 the first principle line half in, frame 13 both principle lines, frame 14 the red dots half in, frame 15 the dot at 4 mid-`Indicate`. |

The dots were checked against the video at every number and every subtitle: red 4 and 6 in
beat 3.1; the five dots of `{5, 2, 11, 7, 8}` in 3.2, the dot at 2 turning green on "smallest
element is two" and all five flashing right to left (11, 8, 7, 5, 2) on "by comparing"; the
six odd numbers in 3.3 with 1 green; the five primes with 2 green and none of the old dots
left behind; the dot at 11 yellow on "say eleven"; and the red days 4 and 6 back in 3.5.

### run 6, `--scenes fails` — 4 sheets, all opened

| Sheet | text over something | cut off / on subtitle | leftover | empty frame | wrong number | wrong count | only sentences | what I saw |
|---|---|---|---|---|---|---|---|---|
| `ep06_sheets_end/sheet00.png` | no | no | no | no | no | no (three dots at the cue that names three numbers, then nine) | no | Frames 0-8. Frame 0 the bare integer line with its thirteen ticks and the labels -9 to 3. Frame 1 the top text "the set of all negative integers" with red dots at -1, -2, -3. Frame 2 the same text in red ending "no smallest element", nine red dots to -9 and the red "and so on" arrow at the left end. Frames 3-6 the real line with the labels 0 and 1, then the dot at 1 with its label, then the halving dots and labels 1/8, 1/4, 1/2. Frames 7-8 the open circle at zero and the bottom text "the set of all positive real numbers: no smallest element" in red. Nothing overlaps; the bottom text sits above the subtitle band. |
| `ep06_sheets_end/sheet01.png` | no | no | no | no | no | no (nine dots, five dots, four labels) | no | Frame 9, the last of the scene. The whole picture at once: the integer line with nine red dots and the arrow, the real line with its two ticks, the labels 0 and 1, the five halving dots with the four labels, the white open circle at zero, and both texts. In this sheet the circle is white. |
| `ep06_sheets_mid/sheet00.png` | no | no | no | no | no | no | no | Mid frames 0-8: frame 1 the three dots half in, frame 2 the six more dots arriving leftwards and the arrow fading in, frame 4 the real line mid-`Create`, frame 5 the dot at 1 mid-fade, frame 6 the halving dots arriving one after another, frames 7-8 the circle and the bottom text mid-fade. All half-states are mid-animation, none is a leftover. |
| `ep06_sheets_mid/sheet01.png` | no | no | no | no | no | no | no | Mid frame 9: the same picture as the end frame, with both texts brighter and slightly larger on "is stable" (the `Indicate` at its midpoint). |

**Defect found here, and fixed.** The first render of this scene had the open circle at zero
in red, not white: `Circle(radius=0.13)` takes `RED` as its own default colour in this Manim,
and the board's line is `Circle(radius=0.13, color=WHITE)`. The sheets showed a ring with a
warm tint at the left end of the real line and a pixel probe found 84 red pixels in a ring of
radius 8 px around (-5, -1) from the moment the circle appeared (t = 36 s). A red circle at
zero says the opposite of the sentence: the point of the beat is that zero is *not* in the
set. `color=WHITE` is now passed. After the fix the probe finds 33 of 36 samples on the circle
white and not one red pixel in the ring's box from t = 34 s to the end. See
`TRIAL_LOG-ep06.md` runs 7 and 8.

The picture of these sheets was checked against the video at each subtitle: the three dots
appear inside "look at the set of all negative ones" and the six more inside "it never ends";
the top text turns red on "no smallest element"; the real line appears inside "zero and
everything above it"; the dot at 1 inside "all positive numbers", the rest of the halving dots
inside "half of it"; the open circle at zero inside "Zero would be below them all"; the bottom
text on "not in the set"; the tick labels 0 to 3 flash inside "first counterexamples"; and both
texts flash together on "is stable" (measured: their red pixel counts fall from about 750 and
780 to 343 and 440 and come back, the two texts scaling together).

### run 9, the whole episode, `check.py cs70/note11 6 --strict` — 12 sheets, all opened

Run 9 rendered the episode end to end (283.7 s, 51 subtitles) and PASSed every stage except
`report`, which wanted a line for each of its 12 sheets. One row per sheet, in the order the
run listed them.

| Sheet | text over something | cut off / on subtitle | leftover | empty frame | wrong number | wrong count | only sentences | what I saw |
|---|---|---|---|---|---|---|---|---|
| `ep06_sheets_end/sheet00.png` | no | no | no | no | no | no (eight boxes, none counted; one "offer") | no | Frames 0-8, the hook. The claim line; the eight day boxes with their labels arriving left to right, "offer" under box k; the legend; box k green on "paint that day green"; k+4 and k+6 red on "paint those days red"; "first red day" under k+4. |
| `ep06_sheets_end/sheet01.png` | no | no | no | no | no | no (one "day before", one "first red day", three reasoning lines) | no | Frames 9-17. k+4 flashing among the red days; k and k+4 compared; "day before" under k+3 and k+3 green; the three reasoning lines one at a time; the step arrow from k+3 to k+4; k+4 keeping its red fill while taking a green stroke; k+6 green on "no red days at all". All eight boxes stay filled and labelled. |
| `ep06_sheets_end/sheet02.png` | no | no | no | no | no | no | no | Frames 18-26. Frame 18 ends the hook (all eight green, reasoning lines and arrow still up). Frame 19 is the first frame of `same`: the new heading, the reasoning lines and arrow gone, the top text, the day row (all eight green, all eight labelled) and the legend kept, exactly what the board keeps. Frames 20-24 the backward pair, then the forward pair, then both pairs and both captions. Frames 25-26 the heading swap to "The smallest element" and the number line with the red dots at 4 and 6. |
| `ep06_sheets_end/sheet03.png` | no | no | no | no | no | no (five dots for the five numbers) | no | Frames 27-35. The question, the red dots at 4 and 6 and their removal; `{5, 2, 11, 7, 8}` with five blue dots, 2 green and "smallest element: 2"; the odd numbers 1, 3, 5, 7, 9, 11 with 1 green and "smallest element: 1"; the primes 2, 3, 5, 7, 11 with 2 green; the dot at 11 yellow on "say eleven". |
| `ep06_sheets_end/sheet04.png` | no | no | no | no | no | no | no | Frames 36-44. The primes with 11 still yellow and the lowest-one flash on 2; "Well-Ordering Principle" and its second line; the prime dots replaced by the red days 4 and 6 (4 flashing on "a first red day") while the principle lines stay; then the heading swap to "Not every kind of number" and the integer line with the red dots at -1, -2, -3. |
| `ep06_sheets_end/sheet05.png` | no | no | no | no | no | no (three, then nine dots; five dots with four labels) | no | Frames 45-50. The nine red dots with the "and so on" arrow and the red top text; the real line with 0 and 1; the dot at 1 with its label; the halving dots with 1/8, 1/4, 1/2; the white open circle at zero with the red bottom text; the last frame with both texts flashing on "is stable". |
| `ep06_sheets_mid/sheet00.png` | no | no | no | no | no | no | no | Mid frames 0-8: the boxes mid-fade, box k mid-`Indicate`, box k mid-recolour to green, k+4 and k+6 mid-recolour to red. Every half-state is mid-animation, none is a leftover. |
| `ep06_sheets_mid/sheet01.png` | no | no | no | no | no | no | no | Mid frames 9-17: k+4 mid-`Indicate`, "day before" fading in, k+3 mid-recolour, the step arrow mid-`Create`, the reasoning lines fading in one by one, k+4 mid-recolour while its stroke is already green. |
| `ep06_sheets_mid/sheet02.png` | no | no | no | no | no | no | no | Mid frames 18-26: frame 19 the first frame of `same` with the row whole; the backward pair mid-fade; box k mid-`Indicate` on "the day of the offer"; the row mid-flash on "runs on forever"; the number line mid-fade with the heading mid-swap. |
| `ep06_sheets_mid/sheet03.png` | no | no | no | no | no | no | no | Mid frames 27-35: the red dots arriving, the question fading in, the five set dots arriving one after another, the dot at 2 turning green with its result line, the dots mid-fade-out, the odd dots and then the prime dots arriving, the dot at 11 mid-`Indicate`. |
| `ep06_sheets_mid/sheet04.png` | no | no | no | no | no | no | no | Mid frames 36-44: the "finitely many" sweep fading the tick labels, the principle lines fading in, the red days fading in as the primes fade out, the dot at 4 mid-`Indicate`, the heading swap and the integer line fading in, the three red dots arriving, the six more arriving leftwards with the arrow. |
| `ep06_sheets_mid/sheet05.png` | no | no | no | no | no | no | no | Mid frames 45-50: the nine dots mid-flash, the real line mid-`Create`, the dot at 1 mid-fade, the halving dots arriving one after another, the open circle at zero and the bottom text fading in, both texts mid-`Indicate` on "is stable". |

The picture was then checked against the video at each subtitle, by probing the rendered pixels.
The elements of scene `fails` appear in this order: the integer line with its labels on "Other
number systems are not so kind." (caption 42); the three red dots on "look at the set of all
negative ones" (43); the six more dots and the "and so on" arrow on "it never ends" (44); the
top text turning red on "no smallest element"; the nine dots flashing on the first word of
"The real numbers contain that same set" (45); the real line on "zero and everything above it"
(46); the dot at 1 on "all positive numbers" (47); the halving dots one after another on "half
of it" (48); the open circle at zero and then the bottom text on "not in the set" (49); the tick
labels 0 to 3 brightening on "first counterexamples" (50); and both texts brightening together
on "is stable" (51). In `least`: the dot at 2 is green and 5, 7, 8, 11 blue (their own colours
checked against the reference RGB, not by eye); the flash on "by comparing" takes all five to
yellow and back; the odd dots have 1 green; the primes have 2 green and no dot of an earlier
set is left behind; the dot at 11 turns yellow on "say eleven" and stays yellow, as the board's
word is "turns" not "flashes"; and on "Our red days" the primes go and 4 and 6 come back red.

## Numbers

| Shown or spoken | Computed by (name in FACTS) | The notes say | Same? |
|---|---|---|---|
| smallest of {5, 2, 11, 7, 8} is 2 | `SET5`, `min(SET5) == 2` (F6) | 2 (line 294) | yes |
| the odd numbers start at 1 | `ODDS`, `min(ODDS) == 1` (F6) | 1 (line 294) | yes |
| the primes start at 2 | `PRIMES`, `min(PRIMES) == 2` (F6) | 2 (line 295) | yes |
| below 11 lie 11 numbers, 0 to 10 | `ELEVEN`, `BELOW_ELEVEN` | eleven (line 295, "finitely many") | yes |
| the negative integers have no smallest | `NEG_INTS`, `all(n - 1 < n < 0 ...)` (F8) | no answer in the notes | added, F8 |
| half of a positive number is smaller | `HALVES`, `LABELLED`, `all(0 < x / 2 < x ...)` (F8) | no answer in the notes | added, F8 |

## Not done

- Voice: not listened to by anyone (I cannot listen). The timing was checked against the
  frames instead.
- Frames: all sheets of every run were opened with the image tool (36 in the scene runs, 12
  in the whole-episode run).
- Out of scope for strict mode and left out: the 1080p render, the `narration.md`
  workflow, publishing, more episodes.

## Questions for the author

1. **End card, item 4, against beat 4.3 (F8).** The end card says "The integers, the real
   numbers and the non-negative real numbers do not have this property." But the
   non-negative reals do have it: zero is their smallest element, and beat 4.3 says so in
   other words ("zero is not positive, so it is not in the set"), as does the board's own
   line for 4.3 ("the non-negative reals as a whole do"). The scene's bottom text is right
   about the set that fails, the set of all *positive* real numbers. Either the end card
   should say "positive", or F8's "none of the three has it" is wrong. I built both as
   written.
2. **Beat 3.1, the question text.** The beat asks for `txt("does every set of natural
   numbers have a smallest element?", 24, YELLOW_D)` and stage B says "Set text at (0, 2.2),
   size 26". I built the beat's numbers: size 24 and yellow, where the other set texts of
   3.2 and 3.3 are size 26 and plain. Is the question meant to differ in both?
3. **Beat 3.5, "Our red days".** The beat removes only "the dots of the primes" and puts
   the red dots at 4 and 6 back. So the set text above them still reads "the primes: 2, 3,
   5, 7, 11, ..." and "smallest element: 2" is still on the stage while the dots show the
   red days. The picture says one thing and the dots another. I built it as written.
4. **Not a beat, a builder's rule for the board.** On the board's line "Rules for the
   builder that come from the check script", it may be worth adding that a stage line which
   names a colour is load-bearing: in this Manim, `Circle` is RED by default (the round
   circle at zero was red until I passed `color=WHITE`), and `Dot` / `Line` differ too. The
   check script cannot see a wrong colour; only the sheets can.

## Questions for the user

1. Is the voice and its speed right?
2. Shall the 1080p render run?

## Fix round 1 (REVIEW-ep06.md) — runs 12 to 18

The eight rows of `REVIEW-ep06.md` are done; only `ep06_well_ordering.py` changed (no
narration word, no BOARD line, nothing in the kit). The sheet list did not change: 12
sheets, the same names as run 9, so the sheet lines below are the only ones.

| # | Beat | What the code does now |
|---|---|---|
| 1 | 3.5 | On "Our red days" the set text changes to `txt("the red days: 4, 6, ...", 26, RED_C)` while the primes and the result text go out, and the red dots come back; on "a first red day" `txt("first red day", 20, RED_C)` appears under the dot at 4, below the tick label "4", and stays |
| 2 | 3.4 | On "finitely many" a `Line` in `YELLOW_D`, stroke width 5, is drawn above the number line from the number 0 to the number 10, with `txt("only these lie below 11", 20, YELLOW_D)` above it; both are removed at the start of 3.5 |
| 3 | 1.5 | R1 is `txt("day before: she holds a job J' she likes as much as J, or more", 22)` and R3 is `txt("first red day: J' or better, so J or better", 22)`; both are 10 wide at most (8.4 and 5.2, so neither needs two rows) |
| 4 | 1.3-1.6, 2.1-2.2 | Under-labels size 20; "day before" in `GREEN_C` at y = 0.65 and "first red day" in `RED_C` at y = 0.30, two heights 0.35 apart; "never" size 22, and the two squares of the backward pair 1.7 apart centre to centre (3.05 and 4.15 edge to edge for a word 0.76 wide) |
| 5 | 4.3 | The circle at zero has `fill_color=BG, fill_opacity=1` and is added after the real line, so the tick at zero is covered; `txt("0 is not positive: not in the set", 20)` sits under the "0" label, 0.14 below it and clear of the line and the bottom text |
| 6 | 4.2 | On "contain that same set": `txt("the real numbers contain these dots too", 22, RED_C)` above the integer line, 0.30 under the top text; faded out at the start of 4.3 |
| 7 | 4.2, 4.3 | The labels 0, 1, 1/2, 1/4, 1/8 are size 22; on "half of it" a `CurvedArrow` in `YELLOW_D` runs from the dot at 1/2 to the dot at 1/4 (0.15 short of each), bulging up to y = -0.74, with `txt("half", 20, YELLOW_D)` above it at y = -0.45, between the labels "1/2" and "1/4" |
| 8 | 3.3 | On "The odd numbers" the old set text and the result text fade out first (run_time 0.4), then a second cue with the same phrase brings the odd set text, its result line and its dots in. The same two plays are used at "The primes", where the same overlap was visible: `s_odd` and `r_odd` go out, then `s_prime` and `r_prime` come in |

**Defect found while checking, and fixed.** The first fix of row 1 dropped the
`FadeOut` of the five prime dots from the "Our red days" cue, and the sheet of `least`
showed the primes 2, 3, 5, 7 still on the line beside the red days 4 and 6. Run 16 has
the fix (the dots go out with the primes text); the sheet above is the fixed one.

### run 18, the whole episode, `check.py cs70/note11 6 --strict` — 12 sheets, all opened

One row per sheet, in the order the run listed them. Frame number = subtitle number.

| Sheet | text over something | cut off / on subtitle | leftover | empty frame | wrong number | wrong count | only sentences | what I saw |
|---|---|---|---|---|---|---|---|---|
| `ep06_sheets_end/sheet00.png` | no | no | no | no | no | no (eight boxes, none counted) | no | Frames 0-8, the hook. The claim line; the eight boxes with their labels, "offer" under box k; the legend; box k green on "paint that day green"; k+4 and k+6 red on "paint those days red". The under-labels and the legend texts stand clear of each other. |
| `ep06_sheets_end/sheet01.png` | no | no | no | no | no | no (one "day before", one "first red day", three reasoning lines) | no | Frames 9-17. "first red day" appears under k+4 at its own height, "day before" under k+3 0.35 higher, in green; the two labels clear the "claim false" legend text and each other; R1, R2, R3 at size 22 with J\*s spelled out ("she holds a job J' she likes as much as J, or more", "first red day: J' or better, so J or better"), all on one row each and clear of the legend; the step arrow from k+3 to k+4; k+4 red-filled with a green stroke; k+6 green. |
| `ep06_sheets_end/sheet02.png` | no | no | no | no | no | no (eight green boxes; two squares per pair) | no | Frames 18-26. Frame 18 ends the hook. Frames 19-24, `same`: the row all green, the backward pair as a green square, "never" (size 22) and a red square 1.7 apart centre to centre with room around the word, the forward pair with its arrow, both captions clear. Frames 25-26 the number line with the red dots at 4 and 6. |
| `ep06_sheets_end/sheet03.png` | no | no | no | no | no | no (five dots for the five numbers, then six odds, then five primes) | no | Frames 27-35. The question, the red dots, `{5, 2, 11, 7, 8}` with 2 green and "smallest element: 2", the odds with 1 green, the primes with 2 green. Frame 35 adds the yellow span line over the numbers 0 to 10 with "only these lie below 11" above it and the dot at 11 (yellow) outside its right end. No text touches it. |
| `ep06_sheets_end/sheet04.png` | no | no | no | no | no | no | no | Frames 36-44. The span line still up in 36 and gone from 37 (start of 3.5); "Well-Ordering Principle" and its second line; frames 39-40 the set text now reads "the red days: 4, 6, ..." in red with the primes and the result text gone, the red dots at 4 and 6, and "first red day" under the dot at 4, below the tick label "4"; frame 41 the heading swap and the integer line; 42-43 the negative-integer dots; 44 "the real numbers contain these dots too" in red above the line. |
| `ep06_sheets_end/sheet05.png` | no | no | no | no | no | no (nine red dots; five halving dots with four labels) | no | Frames 45-50. The reals note still up in 45-48 and gone from 49; the real line with 0 and 1 at size 22; the dot at 1; the halving dots with 1/8, 1/4, 1/2 at size 22; the yellow arrow from the dot at 1/2 to the dot at 1/4 with "half" above it, clear of both labels; the white ring at zero, filled with the background so no tick runs through it, with "0 is not positive: not in the set" under the "0" label; both red texts clear of each other. |
| `ep06_sheets_mid/sheet00.png` | no | no | no | no | no | no | no | Mid frames 0-8: the boxes mid-fade, box k mid-`Indicate`, the legend mid-fade, box k mid-recolour, k+4 and k+6 arriving red. Every half-state is mid-animation. |
| `ep06_sheets_mid/sheet01.png` | no | no | no | no | no | no | no | Mid frames 9-17: k+4 mid-`Indicate` with "first red day" under it, "day before" fading in under k+3, k+3 mid-recolour, k+4 mid-`Indicate` over its red fill, the step arrow mid-`Create`, R1 fading in. |
| `ep06_sheets_mid/sheet02.png` | no | no | no | no | no | no | no | Mid frames 18-26: frame 18 the hook end; frame 19 the first frame of `same` with the row whole and the new heading; the backward pair mid-fade with "never"; the forward pair; the row mid-flash on "runs on forever"; the number line and the red dots behind the heading swap. |
| `ep06_sheets_mid/sheet03.png` | no | no | no | no | no | no | no | Mid frames 27-35: the red dots arriving, the question, the five dots of the set, the dot at 2 turning green, the dots going out, the odd dots and then the primes, the dot at 11 mid-`Indicate`, and on frame 35 the span line half drawn with its words already up. |
| `ep06_sheets_mid/sheet04.png` | no | no | no | no | no | no | no | Mid frames 36-44: the span line fading out, the principle lines, "the red days: 4, 6, ..." fading in as the primes text goes out, the dot at 4 mid-`Indicate`, "first red day" fading in (frame 40), the heading swap, the red dots arriving, and "the real numbers contain these dots too" fading in on 44. |
| `ep06_sheets_mid/sheet05.png` | no | no | no | no | no | no | no | Mid frames 45-50: the reals note, the real line mid-`Create`, the dot at 1, the halving dots one after another, the yellow arrow and "half" mid-`Create` (frame 47), the ring and "0 is not positive: not in the set" fading in under the "0" label (frame 48), both red texts mid-`Indicate` on "is stable". |

The order of the changes inside each beat was checked against the subtitles: the span
line and its words come on "only finitely many natural numbers lie below it" and are gone
before "This fact is called the well ordering principle"; the red-days text and the
"first red day" label come on their two phrases of 3.5, the second of them after the
dot at 4 flashes; "the real numbers contain these dots too" comes on "The real numbers
contain that same set" and is gone at the first word of 4.3; the half arrow comes with
the rest of the halving dots inside "half of it is smaller and still positive"; and the
words under the circle come on "so it is not in the set".
