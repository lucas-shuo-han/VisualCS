# Trial log, episode 08

One line per check.py run.

1. `PY cs70/note11/ep08_optimal_partners.py` (FACTS gate: F1 to F8, the twenty-four matchings, the two stable ones, and the position and row asserts the picture reads): exits 0.
2. `PY K/scripts/check.py cs70/note11 8 --strict --scenes hook` -> PASS (code, lint, board 2 of 13, render, log, av 29.9 s, pace 151, sheets 2). 2 sheets opened, nothing to fix.
3. `PY K/scripts/check.py cs70/note11 8 --strict --scenes find` -> PASS (code, lint, board 8 of 13, render, log, av 99.1 s, pace 166, sheets 6). 6 sheets opened, nothing to fix. K1 checked in the pixels of the last frames (yellow at the Job 1 column, the sheet's own scale hides it).
4. `PY K/scripts/check.py cs70/note11 8 --strict --scenes best` -> PASS (code, lint, board 13 of 13, render, log, av 84.5 s, pace 168, sheets 4). 4 sheets opened, nothing to fix.
5. `PY K/scripts/check.py cs70/note11 8 --strict` (whole episode) -> PASS code, lint, board 13 of 13, render, log, av 254.5 s, pace 159, sheets 10; FAIL report only (no report file yet). 10 sheets opened, all clean.
6. `PY K/scripts/check.py cs70/note11 8 --strict --no-render` (after writing REPORT-ep08.md) -> PASS all nine stages. RESULT: PASS.
7. `PY K/scripts/check.py cs70/note11 8 --strict --no-render` again (after the quoted table in the report was set to the last run) -> PASS all nine stages. RESULT: PASS.

Round 2: the review of the frames (`REVIEW-ep08.md`), eight rows, `ep08_optimal_partners.py` only.

8. `PY K/scripts/check.py cs70/note11 8 --strict --scenes hook` -> PASS (code 13 say/45 cue, lint, board 2 of 13, render, log, av 29.9 s video / 28.0 s audio, pace 151, sheets 2). Sheets opened; row 7 of the review is in them (the eight headers faint at frame 0, full by frame 2).
9. `PY K/scripts/check.py cs70/note11 8 --strict --scenes find` -> PASS (board 8 of 13, log, av 99.1 s / 96.3 s, pace 166, sheets 6). Six sheets opened; rows 3, 4 and 5 are in them ("stable" at 28, the six lines at width 6 with K4 under the coloured ones, the legend at 0.4 and 22 with the entries 0.75 apart).
10. `PY K/scripts/check.py cs70/note11 8 --strict --scenes best` -> FAIL log, one finding: `[layout] beat 5 "So here the matching that is optimal for the": a Rectangle runs through the text 'which one?'`. The word at size 24 centred at (5.7, -1.4) (review row 6) reaches x = 4.866 and the Dora column's cells reach 5.4, so the cell strokes run through it; the free band right of the column up to 6.6 is 1.2 and the word is 1.668 wide. Kept size 24 and the right edge under 6.6, moved the word to (5.7, -0.24), the empty band between the two halves.
11. `PY K/scripts/check.py cs70/note11 8 --strict --scenes best` (after the move) -> PASS (board 13 of 13, log clean, av 84.5 s / 82.6 s, pace 168, sheets 4). Four sheets opened; rows 1, 2, 6 and 8 are in them (the width-7 green border on the Job 2 Dora cell, "candidate"/"optimal"/"pessimal" one line each at 22, the green arrow beside Job 3, "which one?" at 24). The transient flashes of rows 1, 2 and 6 and the coming and going of the arrow were read from the pixels of the video, frame by frame.
12. `PY K/scripts/check.py cs70/note11 8 --strict` (whole episode) -> PASS code 13 say/45 cue, lint, board 13 of 13, render, log, av 254.5 s / 251.9 s, pace 159, sheets 10 (the same ten names as before), report. The sheets holding the changed beats were opened: `ep08_sheets_end/sheet00.png` (1.1), `sheet02.png` (2.3-2.6) and `sheet03.png`/`sheet04.png` (3.1-3.5).
13. `PY K/scripts/check.py cs70/note11 8 --strict --no-render` (after the report and this log were written) -> PASS all nine stages, the same table as 12. RESULT: PASS.
