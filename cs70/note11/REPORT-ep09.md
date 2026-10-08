# REPORT: episode 09, The Proposers Win

## Files

- Preview (480p, voiced): `C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep09\videos\ep09_job_optimal\480p15\Ep09JobOptimal.mp4`
- Subtitles: `C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep09\videos\ep09_job_optimal\480p15\Ep09JobOptimal.srt`
- Code: `cs70/note11/ep09_job_optimal.py`, `cs70/note11/series.py`, `cs70/note11/BOARD-ep09.md`

## Last check.py run

```
== check: note11 episode 9 [en] ==
PASS code    16 say(), 46 cue()
PASS lint    clean
PASS board   16 of 16 beats, word for word as in BOARD-ep09.md
PASS render  C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep09\videos\ep09_job_optimal\480p15\Ep09JobOptimal.mp4
PASS log     clean
PASS av      video 284.6 s, audio 282.4 s, longest silence 3.6 s
PASS pace    50 subtitles, 157 words per minute
PASS sheets  12 sheets
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep09_sheets_end\sheet00.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep09_sheets_end\sheet01.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep09_sheets_end\sheet02.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep09_sheets_end\sheet03.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep09_sheets_end\sheet04.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep09_sheets_end\sheet05.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep09_sheets_mid\sheet00.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep09_sheets_mid\sheet01.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep09_sheets_mid\sheet02.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep09_sheets_mid\sheet03.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep09_sheets_mid\sheet04.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep09_sheets_mid\sheet05.png
PASS report  REPORT-ep09.md names all 12 sheets

RESULT: PASS. Not done yet:
  - open all 12 sheets above (frame number = subtitle number) and note per sheet what you saw: overlaps of text with shapes, leftovers, empty frames, a number that disagrees with its subtitle
  - listen to C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep09\videos\ep09_job_optimal\480p15\Ep09JobOptimal.mp4 from start to end, or say in the report that nobody did
report: C:\Users\18547\AppData\Local\Temp\kit_check\note11\CHECK-ep09-en.md
```

## Frames

One line per sheet of the last full-episode run. Answers to the questions of step 5, in
order: text over something, cut off or on the subtitle, leftover, empty frame, wrong
number, wrong count, only sentences.

| Sheet | text over something | cut off / on subtitle | leftover | empty frame | wrong number | wrong count | only sentences | what I saw, what I changed |
|---|---|---|---|---|---|---|---|---|
| ep09_sheets_end/sheet00.png | no | no | no | no | no | no | no | Frames 0 to 8: the four job lists and the four candidate lists, day 1 with four arrows into Ada, Ada keeping Job 1 and crossing off the other three, day 2 with one offer each. Nothing overlaps; the arrows land on the cells they name. |
| ep09_sheets_end/sheet01.png | no | no | no | no | no | no | no | Frames 9 to 17: the three green arrows of day 2, the "job optimal" slot, the guess line, the flashes on Ada and on the green rows. Frame 17 opens scene 2 with the eight day boxes. Clean. |
| ep09_sheets_end/sheet02.png | no | no | no | no | no | no | no | Frames 18 to 26: day 5 and day 7 red, the legend, "first red day" under day 5, the pair J and C* with the red refused arrow, the rival J* with the green kept arrow, the matching line at the foot. Clean. |
| ep09_sheets_end/sheet03.png | no | no | no | no | no | no | no | Frames 27 to 35: the candidate's list and the matching M, the rival's list with its faded top cell, proof lines G1 to G3 all on one line each. This is the sheet where G3 used to wrap: at size twenty it was 11.0 units wide and pango broke it into "…J*'s" + "optimal", and that tail sat on top of G4. The five proof lines are set at size seventeen now (the widest is 9.6), and nothing overlaps. |
| ep09_sheets_end/sheet04.png | no | no | no | no | no | no | no | Frames 36 to 44: the yellow border on C* in the rival's list, the flashes on the cells, proof lines G4 and G5, the rogue line being drawn. All five proof lines single, no collision. |
| ep09_sheets_end/sheet05.png | no | no | no | no | no | no | no | Frames 45 to 49: the dashed rogue line complete, "stable matching M" red and flashed, the three result lines T1 to T3. The last cell is the sheet's padding, not a frame. Clean. |
| ep09_sheets_mid/sheet00.png | no | no | no | no | no | no | no | Mid-frames 0 to 8, seen for questions 3 and 4 only. Frame 4 catches the refusing arrows in mid-fade and frame 5 the second arrow in mid-draw: no leftover object and no empty frame at any mid-point. |
| ep09_sheets_mid/sheet01.png | no | no | no | no | no | no | no | Mid-frames 9 to 17. Frame 17 catches the eight day boxes appearing left to right: the partly drawn boxes are the animation, not a leftover, and no frame is empty under its subtitle. |
| ep09_sheets_mid/sheet02.png | no | no | no | no | no | no | no | Mid-frames 18 to 26, the second scene: nothing left over from the first scene, no empty frame, the numbers on the day boxes agree with the subtitles that name day 5 and day 7. |
| ep09_sheets_mid/sheet03.png | no | no | no | no | no | no | no | Mid-frames 27 to 35 of the rogue scene: the lists and matching M are built once and stay, no leftovers, no empty frame. |
| ep09_sheets_mid/sheet04.png | no | no | no | no | no | no | no | Mid-frames 36 to 44: proof lines and cells mid-flash; nothing overlaps in these mid-points either. |
| ep09_sheets_mid/sheet05.png | no | no | no | no | no | no | no | Mid-frames 45 to 49. Frame 47 catches the title "stable matching M" between white and red, which is the colour change in progress, not a leftover. |

## Numbers

| Shown or spoken | Computed by (name in FACTS) | The notes say | Same? |
|---|---|---|---|
| Four jobs and four candidates, the lists of the four-by-four example | `JOBS`, `CANDS` (F1) | lines 337 to 380 | yes |
| Exactly two stable matchings | `stable_matchings()` (F2) | lines 381 to 401 | yes |
| The job optimal matching: Job 1 Ada, Job 2 Dora, Job 3 Cleo, Job 4 Bea | `OPT == M1` (F2) | lines 381 to 401 | yes |
| Day 1: four offers to Ada, three of them refused (Jobs 2, 3, 4) | `run()` == `DAYS` (F3) | the notes do not run the algorithm | added, computed |
| Day 2: Job 1 Ada, Job 2 Dora, Job 3 Cleo, Job 4 Bea, nobody refused | `run()` == `DAYS` (F3) | the notes do not run the algorithm | added, computed |
| Jobs 2, 3 and 4 were refused only by Ada, who is not the optimal candidate of any of them | `REFUSED_1`, `CAND_GREEN` (F3, F2) | line 419 onward, in words | yes |
| Eight day boxes, day 5 and day 7 red, day 5 the first | `DAYS_SHOWN`, `RED_DAYS`, `FIRST_RED` | the notes give no days | added, a picture |
| On all 46656 three-by-three instances the output is job optimal | `always_job_optimal` (F5) | line 418 | yes |
| On all 46656 three-by-three instances no job is refused by its optimal candidate | `never_refused_by_optimal` (F6) | lines 419 to 431 | yes |

## Not done

- Voice: not listened to by anyone. Nobody can listen in this run.
- Frames: all 12 sheets of the three-scene run were inspected, and all 6 sheets of the
  rogue scene before it. The proof-line wrap above was found this way and fixed.
- The 1080p render has not been run; it waits for the answer to question 2.
- `PACE` in `series.py` was left alone (the whole episode is 157 words per minute, in
  the accepted range); the rogue scene alone reads 167, which `--scenes` accepts.

## Questions for the user

1. Is the voice and its speed right?
2. Shall the 1080p render run?

---

## Fix round: round 1 review (2026-10-08)

`REVIEW-ep09.md` row by row, with `BOARD-ep09.md` as the specification and the
review rows only as the pointer to what the author changed. One file changed:
`ep09_job_optimal.py`. No narration word changed (`PASS board 16 of 16 beats`), and
the list of sheets did not change: the same 12 names, six end and six mid, so the
table above still names every sheet of the last run.

Two lines of that table are stale and this note replaces them: the proof lines in
`ep09_sheets_end/sheet03.png` and `sheet04.png` are no longer at size seventeen.
After this round they are size 20, seven rows, each on one line (row 4 below).

| # | Beat | What changed in `ep09_job_optimal.py` | Where I saw it |
|---|---|---|---|
| 1 | 1.2, 1.3 | The seven arrow end points are now the board's own numbers (`OFFER_PTS`), and `Arrow` is called with `tip_length=0.18`, `stroke_width=4`, `max_tip_length_to_length_ratio=1.0`, `max_stroke_width_to_length_ratio=100.0`: manim's default caps shrink the tip of an arrow this short (0.72) to 0.058 and the stroke to 3.6, so the caps had to be lifted for an absolute tip. Three asserts hold the board's layout claims: a probe arrow's `tip.height` is exactly 0.18; the four head x-values (`HEAD_X1`) are 0.6 apart; N2, N3 and N4 cross pairwise at three different points (0.7, 0.18), (0.7, 0.0) and (1.386, 0.085). | `ep09_sheets_end/sheet00.png` frames 3 to 6 |
| 2 | 1.4, 1.5 | The strip label is gone, so the strips carry no word of their own. The gap text is `fit(txt("this is the job optimal matching", 24, GREEN_C), 10)` centred in the gap, and it is what the four offer arrows fade out into; the guess line is size 24 and replaces it on its own cue. | `ep09_sheets_end/sheet00.png` frames 7 and 8; `sheet01.png` frames 11 to 15 |
| 3 | 2.1 to 2.3 | The caption is `a supposed run on other lists, not the run we just watched`, size 22, fitted to 9 units, at (0, 2.5). Strip labels are size 20; actor captions are `txt(..., 20, GREY_A)`; `refused`, `kept` and `first red day` are size 22. The matching statement is two texts on two cues: `a stable matching M pairs J with C*` at (0, -2.05) on the cue "there is a stable matching", `in M, the rival J* has some partner C'` at (0, -2.50) on the cue "the rival has some partner". | `ep09_sheets_end/sheet01.png` frame 17; `sheet02.png` frames 18 to 26 |
| 4 | 3.1 to 3.6 | The proof lines are rebuilt from the board's seven rows (`PROOF_3`): size 20, `PROOF_W3 = 10`, left edge at x = -6.2, at the board's y = -0.42 to -2.58, and the wording "the optimal candidate of J*" everywhere instead of the possessive. No scaling is needed — the widest is 8.83 units, under pango's wrap width, and each line is one line. G3 and G4 appear as their two texts together, one cue each. The rival's top cell keeps the name at opacity 0.5 with its border at full strength. The rogue link is one `DashedLine` from `ROGUE_PTS3` = (2.3, 1.1) to (4.9, 1.4), `stroke_width=5`, `dash_length=0.15`, ORANGE, with two asserts against the M row and box height that its first end is on the top edge of the box J* and its last end on the bottom edge of the box C*. | `ep09_sheets_end/sheet03.png` frames 27 to 35; `sheet04.png` frames 36 to 44 |
| 5 | 3.7 | T2 (`as an induction on k: no job is refused by its optimal candidate on day k`) is size 22, was 20. T1 stays 24 and T3 (`and the candidates?`) 22; all three fitted to 10 units, one line each. | `ep09_sheets_end/sheet05.png` frames 47 to 49 |
| 6 | headings | Nothing changed, as the review asks: the underline still touches the descenders and the kit will fix it. | — |

What the changed frames show, read with the Read tool. Sheet00 frames 3 to 6: the
four day-one offers leave the four job cells and land on Ada's header with their
heads 0.6 apart, one of them straight down at x = -5.1, and the three day-two offers
in green; no two arrows meet at one point, and no arrow head touches Ada's name.
Sheet00 frames 7 and 8 and sheet01 frames 11 to 15: the green "this is the job
optimal matching" sits in the middle of the gap, one line, and later the yellow guess
line of the same size takes its place; nothing but the heading is above the strips.
Sheet01 frame 17 and sheet02 frames 18 to 26: the caption stands over the day boxes,
one line, well inside the frame; labels 20, actor captions 20 and grey, "refused",
"kept" and "first red day" 22; the two matching texts arrive one on each of their two
cues and sit at the foot, above the subtitle band, with no overlap with the actor
captions. Sheet03 frames 27 to 35 and sheet04 frames 36 to 44: the seven proof lines
are in the lower half, each one line, left edges flush, no line running into the
lists above; the rival's top cell reads "refused J* earlier" dimmer than its own
border. Sheet04 frame 44 and sheet05 frames 47 to 49: one orange dashed line, thick
and long-dashed, leaves the top edge of the box J* and ends on the bottom edge of the
box C*, clear of the two white pair lines and of the box corners (a threefold
enlargement of that still was cut to read the dashes: a single line, no second one).
T1, T2 and T3 are all on screen in the last stills, one line each, T2 larger than
before.

Nothing else was touched: `series.py`, `K`, the BOARD, the narration and the strip of
the first scene are as they were, and `PACE` was left alone (the whole episode reads
157, the rogue scene alone 167, which `--scenes` accepts).

The two entries of "Not done" above still stand: nobody listened to the voice, and
the 1080p render has not been run.
