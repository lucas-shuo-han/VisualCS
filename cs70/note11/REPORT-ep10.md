# REPORT: episode 10, And the Candidates Lose

## Files

- Preview (480p, voiced): `C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep10\videos\ep10_candidate_pessimal\480p15\Ep10CandidatePessimal.mp4`
- Subtitles: `C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep10\videos\ep10_candidate_pessimal\480p15\Ep10CandidatePessimal.srt`
- Code: `cs70/note11/ep10_candidate_pessimal.py`, `cs70/note11/series.py` (already held the episode 10 row), `cs70/note11/BOARD-ep10.md`

## Last check.py run

```
== check: note11 episode 10 [en] ==
PASS code    13 say(), 40 cue()
PASS lint    clean
PASS board   13 of 13 beats, word for word as in BOARD-ep10.md
PASS render  C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep10\videos\ep10_candidate_pessimal\480p15\Ep10CandidatePessimal.mp4
PASS log     clean
PASS av      video 256.3 s, audio 254.1 s, longest silence 2.9 s
PASS pace    43 subtitles, 157 words per minute
PASS sheets  10 sheets
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep10_sheets_end\sheet00.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep10_sheets_end\sheet01.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep10_sheets_end\sheet02.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep10_sheets_end\sheet03.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep10_sheets_end\sheet04.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep10_sheets_mid\sheet00.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep10_sheets_mid\sheet01.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep10_sheets_mid\sheet02.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep10_sheets_mid\sheet03.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep10_sheets_mid\sheet04.png
PASS report  REPORT-ep10.md names all 10 sheets

RESULT: PASS. Not done yet:
  - open all 10 sheets above (frame number = subtitle number) and note per sheet what you saw: overlaps of text with shapes, leftovers, empty frames, a number that disagrees with its subtitle
  - listen to C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep10\videos\ep10_candidate_pessimal\480p15\Ep10CandidatePessimal.mp4 from start to end, or say in the report that nobody did
report: C:\Users\18547\AppData\Local\Temp\kit_check\note11\CHECK-ep10-en.md
```

## Frames

One line per sheet of the full-episode run, in the order of step 5: text over something,
cut off or on the subtitle, leftover, empty frame, wrong number, wrong count, only
sentences. The sheet's frames are subtitles 1 to 9, 10 to 18 and so on; the video opens
with the title card, which has no subtitle, so frame *n* of sheet00 is subtitle *n*.

| Sheet | text over something | cut off / on subtitle | leftover | empty frame | wrong number | wrong count | only sentences | what I saw, what I changed |
|---|---|---|---|---|---|---|---|---|
| ep10_sheets_end/sheet00.png | no | no | no | no | no | no | no | Subtitles 1 to 9 (scene `hook`). Frame 1 is the bare four-by-four lists, frames 2 and 3 the yellow, green and purple borders of the two stable matchings with the legend "both / first / second" appearing at the right; frames 4 to 6 flash Cleo's and Dora's green cells above their purple ones and set the slot "pessimal" at size 22, at the same moment the Cleo row 2 and Dora row 3 cell borders go to width 6 (they keep that width to the last frame); frames 7 to 9 flash Ada's and Bea's row 1 and put "a law?" in the right slot at size 24, wholly inside x = 6.6. No text touches a box edge, nothing in the subtitle band. |
| ep10_sheets_end/sheet01.png | no | no | no | no | no | no | no | Subtitles 10 to 18 (scene `cleo`). Frame 11 sets the red borders on Cleo's rows three and four (Job 1, Job 4); frames 13 and 14 dim the Ada cell at the top of the Job 3 column; frame 18 draws the dashed orange line between the Job 3 column and the Cleo header and puts "not" over "stable" in the right slot. The line is `ORANGE`, `dash_length=0.15`, width 6 — three dashes, read as a line, not a stub — and it spans the gap only, from the bottom of Job 3's row 4 to the top of Cleo's header, touching neither box. While it is on screen both headers carry an `ORANGE` border of width 4. |
| ep10_sheets_end/sheet02.png | no | no | no | no | no | no | no | Subtitles 19 to 27 (end of `cleo`, scene `law`). Frame 20 has Cleo's rows three and four grey and dimmed, frame 22 the theorem line in the gap, frame 26 the rogue line drawn again with the Job 3 and Cleo headers again orange at width 4, frame 27 the line gone with the theorem line in its place and both header borders back to blue and gold. The gap holds either the line or the text, never both. |
| ep10_sheets_end/sheet03.png | no | no | no | no | no | no | no | Subtitles 28 to 36 (scene `swap`). Frame 28 has the four white arrows pointing down from the jobs and "job optimal" in the left slot; frame 29 has them pointing up; frame 30 adds "candidate / optimal" in the two left slots; frame 31, the end of "Try it on our lists.", is the bare frame — the P arrows are fully gone and no ask has started, so nothing hangs over the "Ada" header; frame 32 grows the four asks, each from its own cue, tips stopping at the bottom edge of the job row-4 cells so no tip touches a name, each flash on the header of the job it points at (Job 1, Job 4, Job 2, Job 3); frame 35 has the down arrows again with "1952 hospitals propose" in the gap; frame 36 the candidate-proposing arrows in purple. |
| ep10_sheets_end/sheet04.png | no | no | no | no | no | no | no | Subtitles 37 to 43. Frame 37 has the purple arrows with "1990s students propose" in the gap, frame 39 the paper line in the gap with "1952" over "1962" in the right slot, frames 40 to 43 that line flashed and the job headers and the legend flashed. The gap holds the one-line year text or the paper line, never both; the right strip holds the two years, never a single year. The last cell of the sheet is padding, not a frame. |
| ep10_sheets_mid/sheet00.png | no | no | no | no | no | no | no | Mid-frames 1 to 9, read for questions 3 and 4 only. Frame 1 already has the full lists (the fade-in ends well before the first sentence does), frames 4 and 5 catch the Cleo and Dora cells mid-flash. No leftover object, no empty frame. |
| ep10_sheets_mid/sheet01.png | no | no | no | no | no | no | no | Mid-frames 10 to 18. Frame 12 catches the Cleo rows between grey and red, which is the colour change in progress, not a leftover; frame 18 catches the dashed line half drawn. No frame is empty under its subtitle. |
| ep10_sheets_mid/sheet02.png | no | no | no | no | no | no | no | Mid-frames 19 to 27. Frame 19 catches Cleo's rows three and four mid-fade back to grey, frame 24 a cell mid-flash. Nothing of scene `cleo` is left over in scene `law`. |
| ep10_sheets_mid/sheet03.png | no | no | no | no | no | no | no | Mid-frames 28 to 36. Frames 29 and 30 catch the arrow swap between the jobs proposing and the candidates proposing: only one set of arrows is on the stage at any mid-point, since the outgoing set is faded out before the incoming set grows. Frame 31 is mid-"Try it on our lists." with the gap bare — no half-faded P arrow and no ask yet. Frame 32 catches the third ask half grown with Job 2's header already flashed. The four crossing asks agree with the four names in the subtitle. |
| ep10_sheets_mid/sheet04.png | no | no | no | no | no | no | no | Mid-frames 37 to 43. Frame 37 is mid-way between "1990s students propose" and the paper line, and frame 39 catches the right slot between its fade-in and the paper line. The gap text and the paper line are never on the stage together, and the two ask sets are never on the stage together. |

## Numbers

| Shown or spoken | Computed by (name in FACTS) | The notes say | Same? |
|---|---|---|---|
| Four jobs, four candidates, the lists of the four-by-four example | `JOBS`, `CANDS` (F1) | lines 337 to 380 | yes |
| Exactly two stable matchings, green (job optimal) and purple | `STABLE == [M2, M1]` (F2) | lines 381 to 382, 418 | yes |
| The green matching is the output of propose and reject | `run(JOBS, CANDS)[-1] == M1` (F2) | line 418 | yes |
| Every candidate's pessimal job is her green job | `PESS == {c: j for j, c in M1.items()}` (F4) | lines 413 to 415 (definition), 440 (theorem) | yes |
| On all 46656 three-by-three instances the job optimal matching is candidate pessimal | `optimal_is_pessimal` (F4) | line 440 | yes |
| Cleo's list is Job 2, Job 3, Job 1, Job 4; her green job is Job 3; Job 3's list is Ada, Cleo, Bea, Dora | `CANDS["Cleo"]`, `M1[3]`, `JOBS[3]` (F7) | from lines 337 to 380 | yes |
| With the candidates proposing it stops after one day and gives the purple matching | `SWAP` (F8) | lines 453 to 454 | yes, computed |
| The paper is from 1962, ten years after the 1952 match | `PAPER_YEAR - MATCH_YEAR == 10` (F10) | lines 455 to 467 | yes |

## Not done

- Voice: not listened to by anyone. Nobody can listen in this run.
- Frames: all 10 sheets of the full-episode run were opened, and the 2 sheets of each
  scene-only run (hook, cleo, law, swap) before them. No frame needed a fix.
- Round 2 (the review): the seven rows of REVIEW-ep10.md were done, and each scene was
  rendered again on its own before the full run. In the full run the end sheets that hold
  the changed beats were opened again — sheet00 (frames 4 to 9), sheet01 (frame 18),
  sheet02 (frames 24 to 27), sheet03 (frames 31 to 36), sheet04 (frames 36 to 43) — and
  the mid sheets 03 and 04 for the asks and the year text. Everything reads at 480p.
- The 1080p render has not been run; it waits for the answer to question 2.
- `PACE` in `series.py` was left alone: the full episode reads 157 words per minute, in
  the accepted range of 120 to 165.

## Questions for the user

1. Is the voice and its speed right?
2. Shall the 1080p render run?

Beats whose words or numbers I am not sure of. All of them were built exactly as the
board writes them.

3. Beat 2.2, "Could she be above Cleo on its list?" The "she" is the other candidate,
   but the word just before is "Cleo". A listener may attach "she" to Cleo, and then the
   sentence asks whether Cleo is above Cleo. The picture flashes the other candidate's
   cell, so the eye has it, but "Could that other candidate be above Cleo on its list?"
   would say it without the picture. Same spot, beat 2.3, "So that other candidate is
   below Cleo" — this one already carries the noun.
4. Beat 2.3 and the arrow table, line R: the board says the dashed rogue line is width 4,
   the closing lesson of the earlier episodes says a dashed line is a faint stub below
   width 5. The line is drawn at width 5 (and at `ORANGE`, the board's colour), because
   at width 4 it was the stub the lesson warns about. Beat 2.3 is otherwise as written.
5. Beat 4.2, the four asks: Ada asks Job 1, Bea Job 4, Cleo Job 2, Dora Job 3, so the
   arrows of Bea, Cleo and Dora cross two or three times in the middle of the gap. The
   board prescribes these four arrows, so they are drawn; the crossing is dense in the
   two seconds before the four colours go on. Should the arrows be drawn one at a time,
   or the two middle ones moved apart?
6. Beat 4.3 and 4.4, the year 1952: the board's stage line puts `1952` on screen when
   the hospitals propose, and the board's own note says the year comes from episode 2,
   not from the notes' lines 438 to 474 (which give 1962 and "the nineteen nineties"). I
   checked `1962 - 1952 == 10` against the board's F10 and it holds, but I cannot check
   1952 itself against the notes. Is the residency match of 1952 the right start year for
   this series?
7. Beat 4.3 says "In the nineteen nineties the roles were reversed". The screen shows
   `1990s`. The notes give no year; the board writes the decade. Fine as spoken, only
   asking whether the decade is the one you want the series to claim.

## Round 2: what REVIEW-ep10.md changed

No narration text was touched. The BOARD was left alone; each row below is the review's
change, and where a row differs from the board the review wins.

| Row | Beat | Change in `ep10_candidate_pessimal.py` | What the frame shows now |
|---|---|---|---|
| 1 | 2.3, 3.2 | `rogue_line()` returns `DashedLine(..., dash_length=0.15, stroke_width=6, color=ORANGE)`; while it is on stage the Job 3 header and the Cleo header are drawn with an `ORANGE` border of width 4 (`HEAD_BORDER = 3` puts the box's own border back). Both scenes call the same helper. | sheet01 frame 18: three orange dashes spanning the gap, Job 3 and Cleo headers orange at width 4, "not" over "stable" at the right. sheet02 frames 26/27: line drawn with both borders orange, then line gone and both borders back to blue and gold. |
| 2 | 1.3, 2.3 | `RS_W = 0.9` (a text this wide centred at x = 6.15 stays inside x = 6.6). "a law?" at size 24, `fit` to `RS_W`; "not stable" at size 24 on two rows in a `VGroup`, each `fit` to `RS_W` (neither needs scaling: 0.44 and 0.86). | sheet00 frames 8 and 9: "a law?" in the right strip, inside x = 6.6. sheet01 frame 18 and sheet02 frame 20: "not" over "stable", red, same strip. |
| 3 | 1.2 on | The left-slot text is size 22 (was 18); on the "pessimal" cue the Cleo row 2 and Dora row 3 cells are marked with `CELL_MARK = 6` in green, and nothing resets them. | sheet00 frames 5 to 9 and every later sheet: the two cells keep a fat green border and "pessimal" sits at size 22 beside them in the left strip. |
| 4 | 4.2 | `GAP_TOP = 0.40` = the bottom edge of job row 4, and `U_PTS` ends there; each ask grows on its own cue (`lead=0.0`) with a flash on the header of the job it points at (`U_JOBS` = 1, 4, 2, 3, asserted against `SWAP`). | sheet03 frame 32: four asks, no tip on a name, each starting at its cue; the flashed header matches the spoken job. |
| 5 | 4.3 | Slot RS would need size 14 for "hospitals propose" in a 1.2-wide strip, under the review's size-16 floor, so the review's fallback is used: one line in the gap, at most 10 wide — `f"{MATCH_YEAR} hospitals propose"` then `f"{NINETIES} students propose"`, both size 20 fitted to `GAP_W`, and no D/P arrows during that beat. | sheet03 frame 35: "1952 hospitals propose" in the gap with the down arrows; sheet04 frames 36 and 37: "1990s students propose" with the purple arrows. |
| 6 | 4.4 | Slot RS is a two-row `VGroup` of `str(MATCH_YEAR)` over `str(PAPER_YEAR)` (1952 over 1962), size 20. | sheet04 frames 38 to 43: "1952" over "1962" in the right strip while the Gale-and-Shapley line is in the gap. |
| 7 | 4.2 | The four ask cues carry `lead=0.0`, so no part of an ask is on stage while the sentence before it is read; the P arrows are faded out at the end of 4.1 as before. | sheet03 frame 31 (end of "Try it on our lists."): a bare gap, nothing over the "Ada" header — the stray dot is gone. Verified by a pixel scan of the run: the gap strips read zero bright pixels from 18.7 s until 20.0 s, when the Ada ask starts. |

Row 5 is the only place this round differs from BOARD-ep10.md: the board's beat 4.3 puts
the year in slot RS, the review's fallback moves it to the gap. The words are the board's,
unchanged.

One thing the review does not ask for but now reads differently: "pessimal" is size 22 in
the left strip, and it is the same size on every later sheet, so the slot is set once and
never re-scaled.
