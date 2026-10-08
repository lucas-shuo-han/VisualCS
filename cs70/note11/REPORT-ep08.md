# REPORT: episode 08, The Best Partner You Can Keep

## Files

- Preview (480p, voiced): `C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08\videos\ep08_optimal_partners\480p15\Ep08OptimalPartners.mp4`
- Subtitles: `C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08\videos\ep08_optimal_partners\480p15\Ep08OptimalPartners.srt`
- Code: `cs70/note11/ep08_optimal_partners.py`, `cs70/note11/series.py`, `cs70/note11/BOARD-ep08.md`

## Last check.py run

```
== check: note11 episode 8 [en] ==
PASS code    13 say(), 41 cue()
PASS lint    clean
PASS board   13 of 13 beats, word for word as in BOARD-ep08.md
PASS render  C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08\videos\ep08_optimal_partners\480p15\Ep08OptimalPartners.mp4
PASS log     clean
PASS av      video 254.5 s, audio 251.9 s, longest silence 2.9 s
PASS pace    42 subtitles, 159 words per minute
PASS sheets  10 sheets
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_end\sheet00.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_end\sheet01.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_end\sheet02.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_end\sheet03.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_end\sheet04.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_mid\sheet00.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_mid\sheet01.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_mid\sheet02.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_mid\sheet03.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_mid\sheet04.png
PASS report  REPORT-ep08.md names all 10 sheets

RESULT: PASS. Not done yet:
  - open all 10 sheets above (frame number = subtitle number) and note per sheet what you saw: overlaps of text with shapes, leftovers, empty frames, a number that disagrees with its subtitle
  - listen to C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08\videos\ep08_optimal_partners\480p15\Ep08OptimalPartners.mp4 from start to end, or say in the report that nobody did
report: C:\Users\18547\AppData\Local\Temp\kit_check\CHECK-ep08-en.md
```

The whole-episode run before it had the same lines except the last: `FAIL report
REPORT.md (or REPORT-ep08.md) has no line for 10 of 10 sheets`, which is the expected
first result of step 6. That run's ten sheets are the ones listed above and looked at
above; the `--no-render` run made the same sheets from the same video.

## Frames

One line per sheet of the last full-episode run. Answers to the questions of step 5, in
order: text over something, cut off or on the subtitle, leftover, empty frame, wrong
number, wrong count, only sentences.

| Sheet | text over something | cut off / on subtitle | leftover | empty frame | wrong number | wrong count | only sentences | what I saw, what I changed |
|---|---|---|---|---|---|---|---|---|
| ep08_sheets_end/sheet00.png | no | no | no | no | no | no | no | Frames 0 to 8: the hook builds the stage. Frame 0 is the heading with the two strip words only; frame 2 has the four job headers and the candidate headers arriving; frames 3 and 4 the sixteen job cells and the sixteen candidate cells. Frame 5 opens `find` with the yellow border on Job 1 row 1 and Ada row 1, frame 7 the line K1, frame 8 a flash on the Job 2 header. The row 1 of every job column reads Ada, as the subtitle says. Frame 0 is sparse (see the note below), nothing of it is wrong. |
| ep08_sheets_end/sheet01.png | no | no | no | no | no | no | no | Frames 9 to 17: the Ada cells of the Job 2, Job 3 and Job 4 columns fade to a quarter (frame 9 and 10), the yellow borders on Job 4 row 2 and Bea row 1 (frame 12), the line K4 drawing out of the Job 4 column into Bea (frame 15), the green lines A2 and A3 with their four green borders (frames 16 and 17). Every line stays inside the gap between the two halves; no line touches a name. |
| ep08_sheets_end/sheet02.png | no | no | no | no | no | no | no | Frames 18 to 26: the second name of the jobs two, three and four flashed, "stable" in the right slot (frame 19), the green lines going and the purple lines B2 and B3 arriving with four purple borders (frame 20), the legend of three squares and three words (frame 23), then `best` opens at frame 24 with the lines and the right slot empty and the legend, the borders and the faded cells kept. Two matchings, one colour each, as counted. |
| ep08_sheets_end/sheet03.png | no | no | no | no | no | no | no | Frames 27 to 35: "optimal" in the left slot at frame 27, the two flashes on Dora and on Cleo in the Job 2 column, the flashes on Job 1 and Job 4 at frame 28 and on row 2 then row 4 of the Job 3 column, the slot changing to "job optimal" at frame 31, the four candidate headers flashing at frame 32, then the pairs Job 3 green over Job 2 purple in Cleo's column and Job 2 green over Job 3 purple in Dora's. |
| ep08_sheets_end/sheet04.png | no | no | no | no | no | no | no | Frames 36 to 41: row 1 of the four candidate columns flashed, the words "candidate" and "optimal" in two left slots at frame 37, "pessimal" under them at frame 38, the two green cells of the worst jobs flashed, "which one?" in the right slot at frame 40, and the last frame still shows the whole stage under the closing question. |
| ep08_sheets_mid/sheet00.png | no | no | no | no | no | no | no | Mid-frames 0 to 8, for questions 3 and 4 only. Frame 2 catches the Ada and Bea headers half faded in, frame 4 the Dora column mid-build, frame 5 the two headings crossing (the old one on its way out, per the stage plan), frames 7 and 8 the line K1 and a flash in progress. No leftover object, no empty frame under a subtitle. |
| ep08_sheets_mid/sheet01.png | no | no | no | no | no | no | no | Mid-frames 9 to 17. Frame 10 catches the Job 2 header flashing while the three Ada cells are half faded: both are the animation of that subtitle, not leftovers. Frames 14 and 16 catch K4 and the green lines mid-draw. The stage is never empty. |
| ep08_sheets_mid/sheet02.png | no | no | no | no | no | no | no | Mid-frames 18 to 26. Frames 20 and 21 catch the purple lines mid-draw, frame 23 the legend and the right slot half faded in. Frame 24 shows the stage with the gap empty and the right slot empty: the lines and "stable" went at the end of `find`, exactly as the board says. |
| ep08_sheets_mid/sheet03.png | no | no | no | no | no | no | no | Mid-frames 27 to 35. Frame 30 catches "optimal" becoming "job optimal" half way, frame 35 the two words "candidate" and "optimal" fading into their slots. Nothing is left over and no frame is empty. |
| ep08_sheets_mid/sheet04.png | no | no | no | no | no | no | no | Mid-frames 36 to 41, the end of `best`. Frame 39 catches "which one?" half faded in. The last mid-frame is the full stage under the last subtitle. |

## Numbers

Every number in the picture and in the voice is computed in the FACTS block: the two lists
(F1, F2), the twenty-four permutations of which exactly two are stable (F3), the optimal
candidate of each job and of each candidate (F6, F7), the pessimal pair (F8), the row of
every name in every column that the borders read, and the positions the narration speaks
("the second name on its list", "the third", "higher on her list"). The board's numbers
agree with mine everywhere; there is nothing to report as a difference. The names Ada,
Bea, Cleo and Dora are the board's departure from the notes' A, B, C, D, for the voice.

## Questions for the author

None: no beat's words, numbers or picture looked wrong while building, and the board's
six pair-line coordinates fit the gap exactly.

## Left to a person

- [ ] Looking at the frames: done, all ten sheets, one line each above.
- [ ] Listening to the voice: nobody did. The builder cannot hear the audio; the `av`
      stage only measured that the audio is there, 251.9 s against a 254.5 s video, with
      2.9 s as the longest silence.
- [ ] The 1080p render: not run. It waits for the user's go, per STRICT.md step 7.

## What was not done

- No second language (STRICT.md step 8): not asked for.
- No `render.py` and no `srt_to_script.py`: the preview is the deliverable until the
  voice and its speed are settled.
- The board's stage in the `hook` scene starts with only the two strip words on screen
  for the first narration sentence, because that is where the board puts them ("with the
  first word: the strip labels appear", the headers on "four jobs"). It is the board's
  choice, not a defect, and it is written down here only so that the author sees it.

## Second round: the review of the frames (`REVIEW-ep08.md`)

Round 1's reviewer looked at the end sheets of the build above. The eight rows of
`REVIEW-ep08.md` were done in `ep08_optimal_partners.py` alone; the narration, the BOARD,
`series.py`, `manim_kit.py` and the kit are untouched. The list of sheets did not change
(same ten names, same frames), so the sheet lines above still stand. Sheets are named by
the paths of the whole-episode run below; frame number = subtitle number, 0-based.

| Review row | What I changed | What the sheet shows now (sheet opened) |
|---|---|---|
| 1 (3.1) | The Job 2 column's row 2 (Dora) cell gets `GREEN_C` stroke width 7 (`OPT_W`) on "optimal" and an `Indicate(scale_factor=1.15)` right after, as two cues on the same phrase so the fade of the slot is not overwritten; slot LJ is at `SLOT_SIZE` 22. | `ep08_sheets_end/sheet03.png`, frame 27: "optimal" in the left strip at 22, one line, and the Dora cell of the Job 2 column in a bright green border that is visibly heavier than every other border on the stage. The flash was measured in the video: the cell turns yellow (peak at t = 151.13 s), inside the word "optimal" of that sentence. |
| 2 (3.4, 3.5) | Slots LC1, LC2, LP at size 22, each one word on one line; the strip widened to 1.5 and moved 0.1 left (`STRIP_X = -6.25`) so "job optimal" (1.485) and "candidate" (1.32) keep 0.1 clear of the leftmost column and the frame edge; on "pessimal" the Cleo column's row 2 and the Dora column's row 3 flash again. | `ep08_sheets_end/sheet04.png`, frames 36, 37 and 41: "candidate" over "optimal" in the two slots and "pessimal" in the third, each a single line at 22 with clear space on both sides, nothing clipped at the left edge. The two flashes were measured in the video: both cells go yellow together (peak at t = 200.0 s) and return to green, inside "The word for that is pessimal." |
| 3 (2.5, 2.6) | "stable" at `STAT_SIZE` 28 in slot RS, its right edge placed at 6.15 or less (never past `RS_EDGE` 6.6); flashed when it appears, once per matching (cue "no rogue couple" for the green one, "the only ones" for the purple one). | `ep08_sheets_end/sheet02.png`, frames 18 and 22: "stable" large in the right strip with a wide margin to the frame edge and to the Dora column. The flash was measured in the video (the green word turns yellow at t = 110.8 s). |
| 4 (2.3–2.5) | All six lines at `LINE_W` 6, `GREEN_C` and `PURPLE_B` at `stroke_opacity=1.0`. K4 was already created and drawn before the green and the purple lines (2.3 before 2.4 and 2.6), so it lies under them where the three cross; a comment at the call site says so. | `ep08_sheets_end/sheet02.png`, frames 18–22: the six lines are thick and bright, and every crossing is readable. In the pixels the green is on top at the K4 x A2 crossing (1.6, 0.0): the sheet's own scale hides which line wins, so this was read from the frames of the video. |
| 5 (2.6 on) | Legend squares 0.4 with stroke width 4, words 22 each scaled to at most 1.2, the three entries 0.75 apart with the word 0.39 under its square (`LEG_TOP`, `LEG_STEP`, `LEG_DY`). | `ep08_sheets_end/sheet02.png`, frames 23–26: three squares with their three words, bigger and further apart than before, all inside the frame. |
| 6 (3.5) | "which one?" at 24 with its right edge under 6.6, and the "first" and "second" legend entries flashed together when it appears (cue "propose and reject"). One deviation, see the note below: the word sits at (5.7, -0.24), not (5.7, -1.4). | `ep08_sheets_end/sheet04.png`, frame 41: a large yellow "which one?" at the right, clear of the legend above it, of the Dora column to its left and of the frame edge. The two legend entries flash together (measured: both squares go yellow at t = 216.0 s). |
| 7 (1.1) | The four job headers and the four candidate headers are added to the stage at opacity 0.35 on the first word of 1.1, and the board's cues ("four jobs", "four candidates") raise them to full opacity instead of fading them in. | `ep08_sheets_end/sheet00.png`, frames 0–2: frame 0 shows the four blue job headers and the four orange candidate headers faintly beside the two strip words, so the stage is no longer two words alone; by frame 2, the "four jobs" beat, they are at full strength. |
| 8 (3.2) | A `GREEN_C` arrow, stroke width 4, tip length 0.18, at x = 2.75 (0.15 right of the Job 3 column), from the height of the row 4 (Dora) cell up to the row 2 (Cleo) cell; drawn on "better off with Cleo" after the two flashes, removed at the start of 3.3. | `ep08_sheets_end/sheet03.png`, frames 27–35: the arrow points up beside the Job 3 column. Read from the pixels of the video, frame by frame: absent at 27 and 28, present at 29, 30 and 31 (the rest of 3.2), gone from 32 on, which is the first frame of 3.3. |

### The one deviation: where "which one?" sits (review row 6)

The row asks for size 24 centred at (5.7, -1.4) and wholly inside x = 6.6. At size 24 the
word is 1.668 wide, and the clear band between the Dora column (which ends at x = 5.4) and
6.6 is 1.2, so the three together are not satisfiable: at (5.7, -1.4) the word runs over
the Dora column's cells and `check.py --strict` fails with

```
[layout] beat 5 "So here the matching that is optimal for the": a Rectangle runs through the text 'which one?'
```

Size 24 and the right edge inside 6.6 are kept, and the y is the only thing changed: the
word sits at (5.7, -0.24), in the band between the two halves, which holds nothing else by
3.5 (the pair lines went at the end of `find`). The alternative, keeping y = -1.4, would
have meant scaling the word down to about 16 to fit 1.2, smaller than the size 18 the
review called too small.

### Last check.py run (this round)

```
== check: note11 episode 8 [en] ==
PASS code    13 say(), 45 cue()
PASS lint    clean
PASS board   13 of 13 beats, word for word as in BOARD-ep08.md
PASS render  C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08\videos\ep08_optimal_partners\480p15\Ep08OptimalPartners.mp4
PASS log     clean
PASS av      video 254.5 s, audio 251.9 s, longest silence 2.9 s
PASS pace    42 subtitles, 159 words per minute
PASS sheets  10 sheets
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_end\sheet00.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_end\sheet01.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_end\sheet02.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_end\sheet03.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_end\sheet04.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_mid\sheet00.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_mid\sheet01.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_mid\sheet02.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_mid\sheet03.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep08_sheets_mid\sheet04.png
PASS report  REPORT-ep08.md names all 10 sheets

RESULT: PASS.
```

The ten sheets of this run are the ten named above, unchanged. The `--no-render` run after
it gave the same table and `RESULT: PASS`.
