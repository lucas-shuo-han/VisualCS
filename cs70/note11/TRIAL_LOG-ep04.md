# TRIAL LOG: ep04 roommates

One line per `check.py` run.

| # | command | result |
|---|---|---|
| 1 | `check.py cs70/note11 4 --strict --scenes hook` | PASS (code 2 say / 8 cue, lint clean, board 2/12, log clean, av 36.1 s / 34.6 s, longest silence 2.1 s, pace 166 wpm, 2 sheets opened, no defect) |
| 2 | `check.py cs70/note11 4 --strict --scenes repair` | FAIL render: `ValueError: operands could not be broadcast together with shapes (32,3) (2,)` in `Arc.generate_points`; `LOOP_XY` was a 2-tuple, made 3-D |
| 3 | `check.py cs70/note11 4 --strict --scenes repair` | PASS (all eight lines; 4 sheets opened, no defect) |
| 4 | `check.py cs70/note11 4 --strict --scenes none` | PASS (code 10 say / 38 cue, lint clean, board 10/12, log clean, av 52.2 s / 49.7 s, longest silence 1.5 s, pace 170 wpm, 4 sheets opened, no defect) |
| 5 | `check.py cs70/note11 4 --strict --scenes lesson` | PASS (code 12 say / 46 cue, lint clean, board 12/12, log clean, av 35.6 s / 34.1 s, longest silence 1.5 s, pace 164 wpm, 2 sheets opened, no defect) |
| 6 | `check.py cs70/note11 4 --strict` (whole episode) | FAIL report only, as step 6 expects (code, lint, board 12/12, render, log, av 240.0 s / 237.7 s, longest silence 4.2 s, pace 163 wpm, 10 sheets; 10 sheets opened, no defect) |
| 7 | `check.py cs70/note11 4 --strict --no-render` | PASS (all eight lines, `RESULT: PASS`; report names all 10 sheets) |

## Round 2: the three picture changes of REVIEW-ep04.md (rows 1 to 3)

Beat 2.4's reset and green borders moved into the cue on "leaves Ben with Dan" (`run_time=0.9`, one
play, the green cells left out of the reset); the rogue lines take `dash_length=0.25`; the status
text is size 30 at (-3.6, -2.4). Rows 1 to 3 of the review. Nothing else changed.

| # | command | result |
|---|---|---|
| 8 | `check.py cs70/note11 4 --strict --scenes repair` | PASS (code 12 say / 46 cue, lint clean, board 12/12, log clean, av 84.3 s / 81.5 s, longest silence 1.9 s, pace 166 wpm, 4 sheets opened: frame 10 end shows the three green cells of the third matching already before the sentence "leaves Ben with Dan" ends; the dashed rogue lines and the status as asked) |
| 9 | `check.py cs70/note11 4 --strict --scenes none` | PASS (code, lint, board 12/12, log clean, av 54.5 s / 51.7 s, longest silence 1.8 s, pace 163 wpm, 4 sheets opened: frames 9 and 10 end, the dashed Amy-Cora diagonal as visible as the white pair lines, the status clear of the circles) |
| 10 | `check.py cs70/note11 4 --strict --scenes lesson` | PASS (code, lint, board 12/12, log clean, av 37.0 s / 35.2 s, longest silence 1.8 s, pace 157 wpm, 2 sheets opened: both statuses at the new slot, clear of the circles and of the two arrows) |
| 11 | `check.py cs70/note11 4 --strict` (whole episode) | PASS (code, lint, board 12/12, render, log clean, av 248.5 s / 246.3 s, longest silence 4.2 s, pace 156 wpm, 10 sheets; end sheets 01 to 04 and mid sheets 01 to 04 opened, no defect) |
