# REPORT: Rogue Couples (CS70 Note 11, episode 03)

## Files

- Preview (480p, voiced): `C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep03\videos\ep03_rogue_couples\480p15\Ep03RogueCouples.mp4`
- Subtitles: `C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep03\videos\ep03_rogue_couples\480p15\Ep03RogueCouples.srt`
- Code: `cs70/note11/ep03_rogue_couples.py` (class `Ep03RogueCouples`), `cs70/note11/series.py` unchanged
- Plan: `cs70/note11/BOARD-ep03.md` (STRICT.md, "With a storyboard")
- Scene-by-scene runs: `cs70/note11/TRIAL_LOG-ep03.md`

## Last check.py run

`check.py cs70/note11 3 --strict --no-render`, the run this report answers to:

```
== check: note11 episode 3 [en] ==
PASS code    13 say(), 45 cue()
PASS lint    clean
PASS board   13 of 13 beats, word for word as in BOARD-ep03.md
PASS render  C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep03\videos\ep03_rogue_couples\480p15\Ep03RogueCouples.mp4
PASS log     clean
PASS av      video 238.5 s, audio 235.9 s, longest silence 4.2 s
PASS pace    43 subtitles, 161 words per minute
PASS sheets  10 sheets
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep03_sheets_end\sheet00.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep03_sheets_end\sheet01.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep03_sheets_end\sheet02.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep03_sheets_end\sheet03.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep03_sheets_end\sheet04.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep03_sheets_mid\sheet00.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep03_sheets_mid\sheet01.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep03_sheets_mid\sheet02.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep03_sheets_mid\sheet03.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep03_sheets_mid\sheet04.png
PASS report  REPORT-ep03.md names all 10 sheets

RESULT: PASS. Not done yet:
  - open all 10 sheets above (frame number = subtitle number) and note per sheet what you saw: overlaps of text with shapes, leftovers, empty frames, a number that disagrees with its subtitle
  - listen to C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep03\videos\ep03_rogue_couples\480p15\Ep03RogueCouples.mp4 from start to end, or say in the report that nobody did
report: C:\Users\18547\AppData\Local\Temp\kit_check\note11\CHECK-ep03-en.md
```

Both "not done yet" lines are answered above: the ten sheets are named and described in the
Frames table, and "not done" says that nobody has listened to the file.

## Frames

One line per sheet of the last run. Frame numbers are subtitle numbers. An `end` sheet shows
the settled state 0.15 s before that subtitle's span ends; a `mid` sheet the middle of the span.

| Sheet | text over something | cut off / on subtitle | leftover | empty frame | wrong number | wrong count | only sentences | what I saw, what I changed |
|---|---|---|---|---|---|---|---|---|
| ep03_sheets_end/sheet00.png | no | no | no | no | no | no (3 job columns, 3 candidate columns, 9 + 9 cells) | no | Frames 0-8: `hook` 1.1-1.3 then the first subtitle of `unstable`. The two lists appear column by column, the six row-1 and row-3 cells flash white/red, the six rank numbers come in at x = 6.45, then the legend (green "partner", orange "would rather") appears in the strip. Nothing changed. |
| ep03_sheets_end/sheet01.png | no | no | no | no | no | no (3 lines U1-U3, 2 dashed D1-D2, 6 green cells) | no | Frames 9-17: matching U drawn line by line with the six green partner cells, orange "would rather" on Approximation/Bridget, D1, then D1 flashing, U1 and U2 red-dimmed with the Basis and Christine headers red. At 17 the lines and two headers are back to normal for beat 2.4. Nothing changed. |
| ep03_sheets_end/sheet02.png | no | no | no | no | no | no (2 dashed lines = the counted "second rogue couple") | no | Frames 18-26: "rogue couple" and "unstable" in slots A and B, the second couple (orange on Approximation/Anita and Anita/Approximation, D2), then frame 23 onwards the cleaned stage of `stable` - no lines, no slot texts, all eighteen cells reset - with S1-S3 and their green cells. Nothing changed. |
| ep03_sheets_end/sheet03.png | no | no | no | no | no | no (4 cells flashed above a green partner, 2 cells for Control) | no | Frames 27-35: the four names above a partner flashed, the orange "would rather" on Approximation/Anita (27), Basis/Bridget (29), Control/Anita and Control/Bridget (31), each reset afterwards; "stable" appears in slot A at 33, then the Control/Christine and last-name flashes. Nothing changed. |
| ep03_sheets_end/sheet04.png | no | no | no | no | no (3 lines E1, E2, S3 at 41) | no | Frames 36-42: S1 and S2 flashed, then replaced by E1 and E2 with the six green cells moving to the other rows; orange on Control rows 1-2 and its reset; "stable" flashed at 40-41 together with the three lines; "always?" in slot B at 42. Nothing changed. |
| ep03_sheets_mid/sheet00.png | no | no | no | no | no | no | no | Mid frames 0-8: the same pictures, plus the candidate column of frame 0 half-faded and frame 8 with U1 mid-draw. Half-drawn shapes are the middle of a fade, not overlaps. Nothing changed. |
| ep03_sheets_mid/sheet01.png | no | no | no | no | no | no | no | Mid frames 9-17: settled states of `unstable`; frame 16 catches U1 as it turns red while the Basis header is already red. Nothing changed. |
| ep03_sheets_mid/sheet02.png | no | no | no | no | no | no | no | Mid frames 18-26: frame 18 has the two slot texts half-faded in, frame 22 has D2 half-drawn, frame 23 is the settled clean stage. Nothing changed. |
| ep03_sheets_mid/sheet03.png | no | no | no | no | no | no | no | Mid frames 27-35: frame 32 catches "stable" half-faded into slot A and the Control rows mid-reset. Nothing changed. |
| ep03_sheets_mid/sheet04.png | no | no | no | no | no | no | no | Mid frames 36-42: frame 36 has E1 and E2 half-drawn, frame 40 the three lines of E1, E2, S3 mid-flash. Nothing changed. |

## Numbers

| Shown or spoken | Computed by (name in FACTS) | The notes say | Same? |
|---|---|---|---|
| the three job lists and three candidate lists | `JOBS`, `CANDS` | lines 154-167, 175-188 | yes |
| U is unstable; Approximation and Bridget are a rogue couple | `("Approximation", "Bridget") in rogue(U)` | lines 189-191 | yes |
| U has two rogue couples, the second being Approximation and Anita | `len(rogue(U)) == 2`, `rogue(U) == [...]` | not in the notes (added by the board, F7) | added |
| S is stable | `rogue(S) == []` | lines 192-195 | yes |
| in S, Control and Christine are both last on their own list | `JOBS["Control"][-1] == S["Control"] == "Christine"`, `CANDS["Christine"][-1] == "Control"` | lines 196-198 | yes |
| the four names above a partner in S (1 + 1 + 2) | `sum(len(above_partner(j, S)) for j in JOBS) == 4` | not in the notes (the method of beat 3.1, added by the board) | added |
| E (episode 1's output) is stable as well and is not S | `rogue(E) == [] and E != S` | line 99 for E; stability from F1, F2 | yes |

Every number in my FACTS block is the board's, computed again from `JOBS`, `CANDS`, U, S and E
and asserted; none of them disagreed with the notes. The two rows marked "added" are the steps
the board itself lists under "Added to the notes", not numbers of mine.

## Not done

- Voice: nobody listened to the preview from start to end; the pacing line (161 words per
  minute, accepted range 120 to 165) is the only check on the speaking rate.
- The 1080p render has not been run.
- The `--scenes` runs of steps 4 and 5 wrote their sheets into the same folder as the full run;
  only the full run's ten sheets are described above.
- Nothing outside `cs70/note11` was touched; `series.py`, `manim_kit.py`, `tts.py` and the
  skill folder are unchanged.

## Questions for the author

1. End-card bullet 4 reads "Stable does not mean that everyone has a first choice". Everyone
   always has a first choice (a first name on their list); the point of beat 3.4 is that stable
   need not give anyone that first choice. Built as written; probably "gets their first choice".
2. The layout section says the gap between the halves "holds only lines, never text", but the
   same section puts slots A and B at y = 0.22 and y = -0.2, inside that band. Built as written:
   the slots sit in the left strip at x = -6.0 and no line reaches there, so no picture problem -
   only the wording is ambiguous.

## For the user

1. Is the voice right, and is its speed right? Nobody has heard it.
2. Shall the 1080p render run?

## Fix round 1 (review of episode 03)

Four rows of `REVIEW-ep03.md`, each done against the BOARD as it now reads. No narration
line, no cue phrase and no `say()` was touched: the four changes are picture only.

| Row | Beat | What I changed | What the frame shows now |
|---|---|---|---|
| 1 | 2.2, 2.4 | `stage_line()` now builds D1 and D2 as `DashedLine(color=ORANGE, stroke_width=5, dash_length=0.15)` instead of a width-4 stroke at the default dash length. | `ep03_sheets_end/sheet01.png` frame 13 and `sheet02.png` frames 19-22: D1 and D2 read as two thick dashed orange lines, dash by dash, against the four white width-4 lines; at the old width they were a string of dots. |
| 2 | legend (from 2.1) | The strip cap `STRIP_W_MAX` went from 1.4 to 1.2 (`STRIP_X_LEFT` and `STRIP_GAP` now name the arithmetic: 1.2 wide at x = -6.0 clears the Approximation column at x = -5.1 by 0.3). Every strip text goes through it: "jobs", "candidates", "partner", "would rather", and the slot texts. | `ep03_sheets_end/sheet01.png` frames 9-17 and `sheet02.png` frames 18-22: "would rather" is 1.2 wide (size about 16) and stops about 0.3 short of the Approximation box; "candidates" shrank by the same rule. |
| 3 | 3.6 | The cue "Does every set of lists" no longer writes "always?" into slot B. It fades in `band_text("does one always exist?")`: `txt(..., 30, YELLOW_D)` at (-1.7, 0.02), scaled to at most 4.2 wide, in the band between E1 and E2. Slot B stays empty. | `ep03_sheets_end/sheet04.png` frame 42 (and frame 19 of the `--scenes stable` run's `ep03_sheets_end/sheet02.png`): the question sits in yellow between the two vertical lines under Approximation and Basis, clear of both, with nothing under "stable" in the left strip. |
| 4 | end card | Bullet 4 is now "... everyone gets their first choice ...", copied with the other three from the BOARD. | No sheet shows it: the end card is spoken without captions, so it is outside every sheet (as in episodes 02 and 04). Checked instead by reading the four strings out of `construct()` and comparing them with the BOARD's "End card" list: identical, all four. |

The reviewer's five rows that were dropped, and the "scene changes were clean" line, asked
for nothing.

### The runs of this round

`check.py cs70/note11 3 --strict --scenes unstable`: PASS, 4 sheets, av 72.7 s / 69.9 s,
longest silence 1.8 s, pace 148 wpm (with `--scenes` the pace line is a PASS).
`check.py cs70/note11 3 --strict --scenes stable`: PASS, 6 sheets, av 99.7 s / 97.9 s,
longest silence 1.8 s, pace 163 wpm.
`check.py cs70/note11 3 --strict`: PASS on all eight lines, 10 sheets, av 246.8 s / 244.3 s,
longest silence 4.2 s, 43 subtitles, 155 wpm.

The list of sheets did not change: the same ten names as in the table above, in the same two
folders, so no sheet line in the Frames table needed editing. Two of those lines describe
frames this round changed, and the Frames table is left as it was written; the rows above
supersede them:

- sheet01 and sheet02: the two dashed lines are thicker and dashed now, and every strip text
  is 1.2 wide, so the legend no longer comes close to the Approximation column.
- sheet04: the last frame (42) no longer shows "always?" in slot B. It shows the closing
  question "does one always exist?" in the band between E1 and E2; slot B is empty.

The log line for the whole episode is 155 words per minute, between the 120 and 165 of the
strict edition (161 before this round; `series.py`'s slower pauses lengthened the video).
Nothing else in the report changed: the FACTS block, the numbers table and the "Questions for
the author" stand. Question 1 there ("probably gets their first choice") is the change of row 4.
