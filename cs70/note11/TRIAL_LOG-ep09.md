# Trial log, episode 09

One line per check.py run.

1. `PY cs70/note11/ep09_job_optimal.py` (FACTS gate, all three facts incl. the 46656-instance run): exits 0, "46656 instances: always job optimal, never refused by the optimal candidate".
2. `PY K/scripts/check.py cs70/note11 9 --strict --scenes run` -> PASS (code, lint, board 6 of 16, render, log, av, pace 158, sheets 4). 4 sheets opened, nothing to fix.
3. `PY K/scripts/check.py cs70/note11 9 --strict --scenes suppose` -> PASS (code, lint, board 9 of 16, render, log, av, pace 162, sheets 4). 4 sheets opened, nothing to fix.
4. `PY K/scripts/check.py cs70/note11 9 --strict --scenes rogue` -> PASS (code, lint, board 16 of 16, render, log, av, pace 167 as `--scenes`, sheets 6). Sheets opened: proof lines G3 and G4 wrapped onto a second line that sat on the next proof line; fixed by setting the five proof lines at size 17 (pango breaks a line wider than about 10.5 units, and these were 11.0 and 10.7 at size 20).
5. `PY K/scripts/check.py cs70/note11 9 --strict --scenes rogue` (after the fix) -> PASS, same lines, sheets 6. 6 sheets opened, proof lines now one line each, nothing else to fix.
6. `PY K/scripts/check.py cs70/note11 9 --strict` (whole episode) -> PASS code, lint, board 16 of 16, render, log, av 284.6 s, pace 157, sheets 12; FAIL report only (no report file yet). 12 sheets opened, all clean.
7. `PY K/scripts/check.py cs70/note11 9 --strict --no-render` (after writing REPORT-ep09.md) -> PASS all nine stages. RESULT: PASS.

## Fix round: round 1 review, eleven changes to `ep09_job_optimal.py`

8. `PY K/scripts/check.py cs70/note11 9 --strict --scenes run` (after the review changes) -> PASS all stages, sheets 4, av 93.5 s; log clean. 4 end sheets opened: the four offer arrows with their four heads 0.6 apart on Ada's header, the strip without a label, "this is the job optimal matching" at 24 in the middle of the gap, the guess line at 24.
9. `PY K/scripts/check.py cs70/note11 9 --strict --scenes suppose` -> PASS all stages, sheets 4, av 47.2 s; log clean. 4 end sheets opened: the caption over the day boxes, labels 20, actor captions 20, "refused"/"kept"/"first red day" 22, the matching statement as two texts on two cues.
10. `PY K/scripts/check.py cs70/note11 9 --strict --scenes rogue` -> PASS all stages, sheets 6, av 106.5 s; log clean. 6 end sheets opened: seven proof lines at size 20, each one line, left edge x = -6.2; the faded top cell with its border at full strength; one dashed orange line, width 5, dash 0.15, from the top edge of J* to the bottom edge of C*; T2 at 22. A threefold enlargement of the last still was read to check the dashes.
11. `PY K/scripts/check.py cs70/note11 9 --strict` (whole episode, after the fixes) -> PASS code, lint, board 16 of 16, render, log, av 284.6 s, pace 157, sheets 12, report. 12 sheets opened, 6 end and 6 mid, nothing to fix.
12. `PY K/scripts/check.py cs70/note11 9 --strict --no-render` -> RESULT: PASS.
