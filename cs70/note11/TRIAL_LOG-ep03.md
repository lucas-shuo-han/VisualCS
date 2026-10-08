# TRIAL LOG: ep03 rogue couples

One line per `check.py` run.

| # | command | result |
|---|---|---|
| 1 | `check.py cs70/note11 3 --strict --scenes hook` | FAIL render: `NameError: name 'r' is not defined` in `build_stage` (the rank numbers used a stray index) |
| 2 | `check.py cs70/note11 3 --strict --scenes hook` | PASS (code 3 say / 8 cue, lint clean, board 3/13, log clean, av 37.5 s / 36.0 s, longest silence 1.5 s, pace 184 wpm — with `--scenes` the pace line is a PASS, 2 sheets opened, no defect) |
| 3 | `check.py cs70/note11 3 --strict --scenes unstable` | PASS (code 7 say / 23 cue, lint clean, board 7/13, log clean, av 70.1 s / 67.6 s, longest silence 1.5 s, pace 154 wpm, 4 sheets opened, no defect) |
| 4 | `check.py cs70/note11 3 --strict --scenes stable` | PASS (code 13 say / 45 cue, lint clean, board 13/13, log clean, av 95.7 s / 94.2 s, longest silence 1.6 s, pace 170 wpm, 6 sheets opened, no defect) |
| 5 | `check.py cs70/note11 3 --strict` (whole episode) | FAIL report only (everything else PASS; pace 161 wpm; 10 sheets opened, no defect) |
| 6 | `check.py cs70/note11 3 --strict --no-render` | PASS (all eight lines; `RESULT: PASS`) |

Fix round 1 (review of episode 03; picture lines only, no narration word):

| # | command | result |
|---|---|---|
| 7 | `check.py cs70/note11 3 --strict --scenes unstable` | PASS (4 sheets, av 72.7 s / 69.9 s, longest silence 1.8 s, pace 148 wpm, no defect) |
| 8 | `check.py cs70/note11 3 --strict --scenes stable` | PASS (6 sheets, av 99.7 s / 97.9 s, longest silence 1.8 s, pace 163 wpm, no defect) |
| 9 | `check.py cs70/note11 3 --strict` (whole episode) | PASS (all eight lines, 10 sheets - the same ten names as before, av 246.8 s / 244.3 s, longest silence 4.2 s, 43 subtitles, 155 wpm) |
| 10 | `check.py cs70/note11 3 --strict --no-render` | PASS (`RESULT: PASS`) |
