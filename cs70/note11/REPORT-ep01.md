# REPORT: Propose and Reject (CS70 Note 11, episode 01)

## Files

- Preview (480p, voiced): `C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep01\videos\ep01_propose_reject\480p15\Ep01ProposeReject.mp4`
- Subtitles: `C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep01\videos\ep01_propose_reject\480p15\Ep01ProposeReject.srt`
- Code: `cs70/note11/ep01_propose_reject.py` (class `Ep01ProposeReject`), `cs70/note11/series.py`
- Plan: `cs70/note11/BOARD-ep01.md` (STRICT.md, "With a storyboard")

## Last check.py run

`check.py cs70/note11 1 --strict --no-render`, the run this report answers to:

```
== check: note11 episode 1 [en] ==
PASS code    19 say(), 61 cue()
PASS lint    clean
PASS board   19 of 19 beats, word for word as in BOARD-ep01.md
PASS render  C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep01\videos\ep01_propose_reject\480p15\Ep01ProposeReject.mp4
PASS log     clean
PASS av      video 319.0 s, audio 316.6 s, longest silence 4.1 s
PASS pace    51 subtitles, 152 words per minute
PASS sheets  12 sheets
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep01_sheets_end\sheet00.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep01_sheets_end\sheet01.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep01_sheets_end\sheet02.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep01_sheets_end\sheet03.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep01_sheets_end\sheet04.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep01_sheets_end\sheet05.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep01_sheets_mid\sheet00.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep01_sheets_mid\sheet01.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep01_sheets_mid\sheet02.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep01_sheets_mid\sheet03.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep01_sheets_mid\sheet04.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep01_sheets_mid\sheet05.png
PASS report  REPORT-ep01.md names all 12 sheets

RESULT: PASS
```

The runs before it (one scene at a time, as the runbook says) are in `TRIAL_LOG-ep01.md`.

## Round 2: the four rows of REVIEW-ep01.md

All four are in `ep01_propose_reject.py`; no narration, no BOARD, no kit file changed.

| # | Change | Frame now |
|---|---|---|
| 1 | `hook` ends with `self.hold()`, so 1.6's last sentence is spoken before `first_try`'s scene change (heading swap, M1-M3, D1, "matching", the four resets). | 13 end and mid: D1, "matching", M1-M3 and the four borders all up under "So these two would both rather have each other..."; the change is at 14. |
| 2 | `days` ends with `self.hold()`, so `result`'s fade of the heading and "stop" waits for 3.5. | 41 end and mid: "Day after day" and the green "stop" up under "This is where we stop..."; both go at 42. |
| 3 | The episode overrides `heading()`: its rule is cut at x = -5.1, left of the "Approximation" box (x = -5.0 to -2.8), instead of running over its top edge (the rule sat at y = 3.01, the box top at 2.98). Every heading in the episode uses it. | 0-12 and 14-44: a short rule under the heading's first words, clear of all three header boxes. |
| 4 | `build_stage` scales any header word wider than 2.0 to 2.0 (inside the 2.2 wide box); "Approximation" was 2.11 wide, touching both borders. | 0-12 and later: the word sits 0.1 inside the box on each side. |

The scene runs of round 2 (`--scenes hook`, `--scenes days`) are rows 7 and 8 of `TRIAL_LOG-ep01.md`.

## Frames

One line per sheet of the last run. Frame numbers are subtitle numbers. An `end` sheet
shows the settled state 0.15 s before that subtitle's span ends; a `mid` sheet the middle
of the span. (A span carries the pause after its sentence, so an `end` frame could already
show the next scene's opening move: frames 13 and 41 did, and round 2 gives both the
kit's `self.hold()` at the end of their scene so the picture waits for the voice.)

| Sheet | text over something | cut off / on subtitle | leftover | empty frame | wrong number | wrong count | only sentences | what I saw, what I changed |
|---|---|---|---|---|---|---|---|---|
| ep01_sheets_end/sheet00.png | no | no | no | no | no | no (3 job headers, 3 candidate headers, 9 + 9 cells) | no | `hook` frames 0-8. Stage built label by label; the three job lists written column by column, then the candidate lists. Frame 4 catches the Control names as their Write starts (faint strokes, gone by frame 5). Round 2: the heading rule stops at x = -5.1, clear of the "Approximation" header box, and that header's word now sits 0.1 inside its box on both sides. |
| ep01_sheets_end/sheet01.png | no | no | no | no | no | no (3 lines M1-M3, 3 arrows P1-P3) | no | `hook` 9-13 and `first_try` 14-17. "matching" in slot A, M1-M3, the yellow/orange borders and the orange dashed line of 1.6, then (frame 14) the heading "Let every job ask", the three row-1 yellow borders and P1-P3. Round 2: frame 13 still shows all of 1.6 - D1, "matching", M1-M3, the four borders - under its own subtitle; the scene change to "Let every job ask" waits for beat 1.6 to be spoken. |
| ep01_sheets_end/sheet02.png | no | no | no | no | no | no (2 arrows into Anita at 19, 1 into Bridget at 19) | no | Frames 18-26. P1/P2 green with the Anita and Bridget "in hand" cells, P3 red then gone with the red legend, "Day 1" plus morning/afternoon/evening, Control row 1 faded at 24, Control row 2 yellow at 25-26. Nothing changed. |
| ep01_sheets_end/sheet03.png | no | no | no | no | no | no (one arrow into each of Anita and Bridget, then one into Bridget) | no | Frames 27-35. Day 2 morning (repeated offers flashed, P4 to Bridget), afternoon (P4 red then removed, Bridget row 3 yellow, then reset), evening (Control row 2 faded), Day 3 morning with P5. Nothing changed. |
| ep01_sheets_end/sheet04.png | no | no | no | no | no | no (one arrow into each candidate at 39-44) | no | Frames 36-44. P5 green with the Christine "in hand" cell, the "refused" legend dimmed, "stop" in slot A at 40, the chapter 4 flashes, the heading "Propose and reject" at 44. Round 2: frame 41 is 0.15 s before its span ends and now shows "Day after day" and the green "stop" still up (beat 3.5 holds to its end); the heading and "stop" go at frame 42, after the beat is spoken. |
| ep01_sheets_end/sheet05.png | no | no | no | no | no | no (3 orange cells at 46, one arrow into each candidate) | no | Frames 45-50, the result scene: "also called Gale-Shapley" at the top right, "Day 3" and "always?" in the strip, the Control/Christine flashes, the last three questions. Nothing changed. |
| ep01_sheets_mid/sheet00.png | no | no | no | no | no | no | no | Mid frames 0-8, the same beats: names half-written (frame 3 "Christine", frame 8 the candidate lists) and the two row-1 cells scaled up during `Indicate`. Half-drawn text is the middle of a Write, not an overlap. The heading rule is clear of the header box in all nine. |
| ep01_sheets_mid/sheet01.png | no | no | no | no | no | no | no | Mid frames 9-17: the same pictures as the end sheet, plus frame 11 with a yellow border mid-way onto Control row 2 and frame 14 catching a name mid-write. Round 2: mid 13 has D1, "matching", M1-M3 and the four borders up, under the 1.6 subtitle. |
| ep01_sheets_mid/sheet02.png | no | no | no | no | no | no | no | Mid frames 18-26: frame 18 has P3 half-faded in red, frame 24 has Control row 1 half-faded; both are mid-animation, not leftovers. Nothing changed. |
| ep01_sheets_mid/sheet03.png | no | no | no | no | no | no | no | Mid frames 27-35: P4 half-grown at 31 and half-faded red at 33, Bridget row 3 mid-yellow. Nothing changed. |
| ep01_sheets_mid/sheet04.png | no | no | no | no | no | no | no | Mid frames 36-44: "stop" on screen at 41 (see the note on the end sheet), the three green arrows thicker at 40, and the Basis/Bridget headers scaled up mid-`Indicate` at 42. Round 2: mid 41 has both "Day after day" and "stop"; the removal is no longer inside beat 3.5. |
| ep01_sheets_mid/sheet05.png | no | no | no | no | no | no | no | Mid frames 45-50: same pictures as the end sheet; frame 50 has the arrows flashing. Nothing changed. |

## Numbers

| Shown or spoken | Computed by (name in FACTS) | The notes say | Same? |
|---|---|---|---|
| three jobs, three candidates | `len(JOBS)`, `len(CANDS)` | n = 3 (line 14) | yes |
| three days | `len(DAYS) == 3` | three days in the table (lines 78-98) | yes |
| one possible matching (F6) | `EXAMPLE` | line 47 | yes |
| Anita is first on two of the three job lists | `sum(JOBS[j][0] == "Anita") == 2` | lines 17-30 | yes |
| the day-by-day offers, in hand, rejected | `DAYS` | lines 78-98 | yes |
| the output matching | `RESULT` | lines 99-100 | yes |
| Control and Christine each end with the last name on their list | `JOBS["Control"][-1]`, `CANDS["Christine"][-1]` | line 196 (about another matching; here checked for the output) | yes |
| "Day 1", "Day 2", "Day 3", "stop" | `len(DAYS)` and the stop rule (F11) | lines 78-98, 70-72 | yes |

## Not done

- Voice: nobody listened to the preview from start to end; the pacing line (153 words per
  minute, 120 to 165) is the only check on the speaking rate.
- The 1080p render has not been run.
- The `--scenes` runs of steps 4 and 5 rendered one scene each into the same sheet files,
  which the full run then overwrote; only the full run's twelve sheets are described above.

## Questions for the user

1. Is the voice right, and is its speed right? Nobody has heard it.
2. Shall the 1080p render run?
