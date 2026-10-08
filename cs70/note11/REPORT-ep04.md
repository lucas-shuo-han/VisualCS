# REPORT: The Roommates Problem (CS70 Note 11, episode 04)

## Files

- Preview (480p, voiced): `C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep04\videos\ep04_roommates\480p15\Ep04Roommates.mp4`
- Subtitles: `C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep04\videos\ep04_roommates\480p15\Ep04Roommates.srt`
- Code: `cs70/note11/ep04_roommates.py` (class `Ep04Roommates`, scenes `hook`, `repair`, `none`,
  `lesson`), `cs70/note11/series.py` (row 4, unchanged)
- Plan: `cs70/note11/BOARD-ep04.md` (STRICT.md, "With a storyboard")

## Last check.py run

`check.py cs70/note11 4 --strict --no-render`, the run this report answers to:

```
== check: note11 episode 4 [en] ==
PASS code    12 say(), 46 cue()
PASS lint    clean
PASS board   12 of 12 beats, word for word as in BOARD-ep04.md
PASS render  C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep04\videos\ep04_roommates\480p15\Ep04Roommates.mp4
PASS log     clean
PASS av      video 240.0 s, audio 237.7 s, longest silence 4.2 s
PASS pace    42 subtitles, 163 words per minute
PASS sheets  10 sheets
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep04_sheets_end\sheet00.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep04_sheets_end\sheet01.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep04_sheets_end\sheet02.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep04_sheets_end\sheet03.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep04_sheets_end\sheet04.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep04_sheets_mid\sheet00.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep04_sheets_mid\sheet01.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep04_sheets_mid\sheet02.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep04_sheets_mid\sheet03.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep04_sheets_mid\sheet04.png
PASS report  REPORT-ep04.md names all 10 sheets

RESULT: PASS. Not done yet:
  - open all 10 sheets above (frame number = subtitle number) and note per sheet what you saw: overlaps of text with shapes, leftovers, empty frames, a number that disagrees with its subtitle
  - listen to C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep04\videos\ep04_roommates\480p15\Ep04Roommates.mp4 from start to end, or say in the report that nobody did
```

The runs before it (one scene at a time, as the runbook says) are in `TRIAL_LOG-ep04.md`. The
first full-episode run ended with `FAIL report` only (no `REPORT-ep04.md` then), exactly as
step 6 expects; the ten sheets below are the ones that run wrote, and the run quoted above
renders nothing new.

## Frames

One line per sheet of the last run. Frame numbers are subtitle numbers. An `end` sheet shows
the settled state 0.15 s before that subtitle's span ends; a `mid` sheet the middle of the
span. The voice-over and the burned captions have the same timing, so the last subtitle is
number 42; the end card is spoken without captions and is not in any sheet. Subtitle spans
run out of scene order in one place only: 25 starts at 2:03.6, one beat after 24 ends.

| Sheet | text over something | cut off / on subtitle | leftover | empty frame | wrong number | wrong count | only sentences | what I saw, what I changed |
|---|---|---|---|---|---|---|---|---|
| ep04_sheets_end/sheet00.png | no | no | no | no | no | no (1 circle, then 4 circles, 6 grey lines, 3 captions, 12 cells) | no | `hook` frames 0-8. Frame 0 the circle Amy alone with the heading "Four students, two rooms"; frame 2 the four circles; frame 3 all six grey lines (K4) held, then gone by frame 4; frame 4 the four row headers, twelve empty cells and the three captions; frames 5-7 the words written into the rows; frame 7 Dan's row of three "?"; frame 8 the heading now "Repair the rogue couple", the pair lines Amy-Ben and Cora-Dan, and the three green roommate cells of the first matching. Nothing to change. |
| ep04_sheets_end/sheet01.png | no | no | no | no | no | no (1 rogue line, 2 pair lines, 3 green + 2 orange cells, 1 status) | no | `repair` frames 9-17. Frame 9 the orange border on Cora in Ben's row ("his first choice is Cora"); frame 10 the orange border on Ben in Cora's row ("gladly take Ben"); frame 11 the orange dashed line Ben-Cora and the status "rogue couple"; frame 13 the two new pair lines Amy-Dan and Ben-Cora; frame 14 the green cells of the second matching; frame 15 Ben's green cell flashed; frame 16 both orange cells of the second rogue couple; frame 17 the dashed line Amy-Cora. Nothing to change. |
| ep04_sheets_end/sheet02.png | no | no | no | no | no | no (2 diagonals, then 2 sides, 1 loop arrow) | no | Frames 18-26: the end of `repair` (frame 18 the two diagonals of the third matching, frame 19 its green cells and the two orange ones, frame 20 the dashed line Amy-Ben, frame 21 back to the pair lines Amy-Ben and Cora-Dan, frame 22 "back at the start" in yellow, frame 23 the loop arrow) and the start of `none` (frame 24 the heading "No stable matching at all" with the table reset, frames 25-26 the pair lines Amy-Dan and Ben-Cora). Nothing to change. |
| ep04_sheets_end/sheet03.png | no | no | no | no | no | no (3 matchings one after another, 3 red, 3 yellow, 1 orange, 1 dashed line) | no | `none` frames 27-35. Frame 27 the status "three matchings, each with a rogue couple"; frame 29 the three "Dan" cells of the last column in red; frame 30 the first column going yellow one cell at a time from the top; frame 31 the same plus Cora's first cell (Amy) orange; frame 33 the dashed line Amy-Cora over the pair lines Amy-Dan and Ben-Cora; frame 34 the three "?" of Dan's row flashed; frame 35 the heading "Why two sides matter" with the table reset and "no stable matching" in red. Nothing to change. |
| ep04_sheets_end/sheet04.png | no | no | no | no | no | no (1 loop arrow, 2 arrows, 4 recoloured circles) | no | `lesson` frames 36-41. Frame 36 the loop arrow back in the middle of the square; frame 37 the four circles flashed; frame 39 Amy and Ben blue and Cora and Dan gold, with the loop arrow and the pair lines gone; frame 40 the two white arrows Amy-Dan and Ben-Cora; frame 41 the status "always stable?" in yellow. Nothing to change. |
| ep04_sheets_mid/sheet00.png | no | no | no | no | no | no | no | Mid frames 0-8. Frame 3 the six grey lines half-drawn (three of them), frame 4 the table fading in, frame 5 the cells being written, frame 8 the green cells half-set. Half-faded and half-drawn objects are the middle of a fade, not overlaps. Nothing to change. |
| ep04_sheets_mid/sheet01.png | no | no | no | no | no | no | no | Mid frames 9-17. Frame 13 the pair line Ben-Cora half-drawn, frame 16 the green cells of the second matching half-set, frame 17 the dashed line Amy-Cora half-drawn. Nothing to change. |
| ep04_sheets_mid/sheet02.png | no | no | no | no | no | no | no | Mid frames 18-26. Frame 18 the diagonal Amy-Cora being drawn while the orange cells of the second rogue couple are still there (they are reset with the table a moment later, in the same cue); frame 19 the green cells of the third matching being set; frame 20 the dashed line half-drawn. Nothing to change. |
| ep04_sheets_mid/sheet03.png | no | no | no | no | no | no | no | Mid frames 27-35. Frame 29 the red cells fully applied (the cue is early in its caption); frame 30 the first column only one and a half cells yellow, which is the "one after another from the top" of beat 3.2 caught in flight; frame 34 the dashed line half-drawn. Nothing to change. |
| ep04_sheets_mid/sheet04.png | no | no | no | no | no | no | no | Mid frames 36-41. Frame 37 the four circles mid-flash, frame 39 the circles half-way from teal to blue and gold, frame 40 the two arrows half-grown, frame 41 still "no stable matching" (the cue "next episodes" is at the end of its caption). Nothing to change. |

## Numbers

| Shown or spoken | Computed by (name in FACTS) | The board says | Same? |
|---|---|---|---|
| four students | `len(PREF) + 1 == 4` | F1, `2n` is four here | yes |
| three matchings | `len(MATCHINGS) == 3`, asserted | F6 | yes; status text "three matchings, each with a rogue couple" in beat 3.1 |
| the rogue couple of each matching | `[rogue(m) for m in MATCHINGS] == [[("Ben","Cora")],[("Amy","Cora")],[("Amy","Ben")]]` | F3, F4, F5 | yes; drawn one per matching, dashed, orange |
| Dan's list is open | `PREF` has no entry for Dan, the row prints `OPEN` | F2 | yes; three "?" |
| Amy, Ben, Cora all put Dan last | `[PREF[p].index("Dan") for p in LISTED] == [2, 2, 2]` | beat 1.2, beat 3.2 | yes; the last column, red in beat 3.2 |
| the first choices are Ben, Cora, Amy | `[PREF[p][0] for p in LISTED] == ["Ben","Cora","Amy"]` | beat 3.2 ("Amy wants Ben, Ben wants Cora, and Cora wants Amy") | yes; the first column, yellow in beat 3.2 |
| the two people with Dan are somebody's first choice | for every matching `set(rogue(m)[0]) == {with_dan, first_chooser(with_dan)}` | beat 3.2, beat 3.3 | yes |
| Dan's list cannot change any of it | the same three rogue couples for all six lists of Dan | F6, "Added to the notes" 3.2 and 3.3 | yes; the "?" row flashed while it is said |
| the repairs run in a circle | `repair(M1) == M2 and repair(M2) == M3 and repair(M3) == M1` | F7 | yes; three repairs lead back to the start, and the loop arrow is drawn |

No number differs from the notes.

## Not done

- Voice: nobody listened to the preview from start to end; the pace line (163 words per
  minute, in 120 to 165) is the only check on the speaking rate. The words themselves were
  not heard, so a mispronunciation would not have been caught.
- The 1080p render has not been run.
- The `--scenes` runs wrote one scene each into the same sheet files, which the full run
  then overwrote; only the full run's ten sheets are described above.
- The end card is outside every sheet (it is spoken without captions), so its picture was
  never looked at on a frame.
- Out of scope and untouched: episodes 01 to 03 and 05 to 10, the editable `narration.md`
  workflow, `render.py`/`srt_to_script.py` (step 7) and publishing.

## Questions for the author

No beat's words, number or picture looked wrong to me; everything was built as written.
Three things about the picture are worth your eye, but none of them is a departure I made:

1. Beat 3.2: the words are about all three matchings ("whoever", "always"), while the stage
   shows one of them. The three red "Dan" cells and the three yellow first-column cells are
   properties of the lists, and the one orange cell is a property of the matching on screen
   (Amy with Dan). If you wanted the "always" to be visible, the three matchings would have
   to be on screen at once, which the layout has no room for. Built as written.
2. Beat 3.2: `YELLOW_D` is also the flash colour, so the yellow border on the first column
   and the yellow flash of a green cell are the same yellow a beat apart. Legible here, but
   a different colour for one of the two would separate "this cell is a first choice" from
   "look at this cell now".
3. Beat 4.2: the arrows Amy-Dan and Ben-Cora stand for "jobs offer, candidates answer", but
   the four circles keep the names of the students, so the picture reads as the roommates
   offering, not as jobs and candidates. The board asks for exactly this ("This is only a
   picture of 'two sides'; the four keep their names"), so it is a note, not a fault.

## Questions for the user

1. Is the voice right, and is its speed right? Nobody has heard it.
2. Shall the 1080p render run?

## Round 2: the picture changes of REVIEW-ep04.md

The three rows of `REVIEW-ep04.md` (round 1) are done; no narration word, no heading, no box text
changed, and the sheet list is the same ten sheets, so the times and the sheet names above still
hold. This run: `check.py cs70/note11 4 --strict`, `RESULT: PASS`, log clean, video 248.5 s, audio
246.3 s, longest silence 4.2 s, 42 subtitles, 156 words per minute.

What changed, and what the frame now shows:

| Row of the review | Change | Frame now |
|---|---|---|
| 1, beat 2.4 | the table reset and the three green borders are in the cue on "leaves Ben with Dan", one play, `run_time=0.9`, the three cells left out of the reset (`reset_except`) so no cell is drawn to two states at once | `end/sheet02.png` frame 18, the end sheet of the sentence itself: the cells of Amy's second (Cora), Ben's last (Dan) and Cora's first (Amy) are green and every other cell grey. A frame taken 0.2 s before the voice ends that sentence shows the same, so the change lands inside the sentence, not a sentence later |
| 2, beats 2.1, 2.3, 2.4, 3.3 | every rogue line is `DashedLine(..., dash_length=0.25, stroke_width=5, color=ORANGE)` | `end/sheet01.png` frames 11, 12, 13 and 17 (Ben-Cora, then the Amy-Cora diagonal) and `end/sheet03.png` frames 33, 34 (Amy-Cora): the orange dashes are as heavy as the white pair lines and stop at the circle edges |
| 3, beats 2.1, 2.3, 2.4, 2.5, 3.1 to 3.3, 4.1, 4.2 | the status text is size 30 at (-3.6, -2.4), still scaled to 6 wide, in the middle of the left block under the circles | `end/sheet01.png` frame 11 and `end/sheet02.png` frames 20, 22, 23 ("rogue couple", "back at the start"), `end/sheet03.png` frames 27 to 34 ("three matchings, each with a rogue couple") and `end/sheet04.png` frames 36 to 41 ("no stable matching", "always stable?"): the status sits below Dan and Cora with a clear gap, well above the subtitle band, and its left edge stays clear of the table |

The lines of the Frames table above that describe those sheets were written before this round; the
row above replaces them for beats 2.1 to 4.2. Sheet `end/sheet00.png` and both `mid/sheet00.png`
hold beats 1.1 and 1.2 only and are untouched.

Checked sheet by sheet in this round (no text over a shape, nothing cut off, no leftover, no empty
frame, no wrong number or count, nothing but sentences): `end/sheet01.png`, `end/sheet02.png`,
`end/sheet03.png`, `end/sheet04.png`, `mid/sheet01.png`, `mid/sheet02.png`, `mid/sheet03.png`,
`mid/sheet04.png`. The `mid` sheets of 2.4 and 3.3 catch the dashed line and the green borders half
way; that is the animation in flight, not a leftover.

Still not done, and unchanged by this round: nobody has listened to the preview from start to end,
and the 1080p render has not been run.
