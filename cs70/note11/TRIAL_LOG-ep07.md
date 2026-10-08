# TRIAL LOG: ep07 always a stable matching

One line per `check.py` run.

| # | command | result |
|---|---|---|
| 1 | `check.py cs70/note11 7 --strict --scenes worry` | PASS (code 8 say / 21 cue, lint clean, board 8 of 17, log clean, av 121.3 s / 118.7 s, pace 158 wpm, 6 sheets opened, no defect) |
| 2 | `check.py cs70/note11 7 --strict --scenes stable` | FAIL render (`AttributeError: no attribute 'head1'`: scene `worry` kept its heading in a local; stored it on `self` instead) |
| 3 | `check.py cs70/note11 7 --strict --scenes stable` | PASS (code 13 say / 35 cue, lint clean, board 13 of 17, log clean, av 82.3 s / 79.7 s, pace 163 wpm, 4 sheets opened, no defect) |
| 4 | `check.py cs70/note11 7 --strict --scenes general` | PASS (code 17 say / 45 cue, lint clean, board 17 of 17, log clean, av 60.5 s / 58.7 s, pace 164 wpm, 4 sheets opened, no defect) |
| 5 | `check.py cs70/note11 7 --strict` | PASS code (17 say / 45 cue), lint clean, board 17 of 17, render OK, log clean, av 303.8 s / 301.6 s (longest silence 3.7 s), pace 156 wpm, sheets 12 — FAIL report (no line for 12 of 12 sheets, expected on the first full run); all 12 sheets opened, no defect |
| 6 | `check.py cs70/note11 7 --strict --no-render` | PASS (code 17 say / 45 cue, lint clean, board 17 of 17, log clean, av 303.8 s / 301.6 s, pace 156 wpm, sheets 12, report names all 12 sheets) — **RESULT: PASS** |
| 7 | `check.py cs70/note11 7 --strict --no-render` (after the report edit) | PASS, all nine lines, sheet list of 12 — **RESULT: PASS** |

## Fix round (REVIEW-ep07.md round 1 read back; the BOARD had been revised)

The scene list became `worry` (1.1-1.3), `hands` (1.4-1.8), `stable`, `general`; scenes
`worry` and `hands` were rebuilt, and beats 2.2, 2.4, 2.5, 3.1 to 3.4 changed.

| # | command | result |
|---|---|---|
| 8 | `check.py cs70/note11 7 --strict --scenes worry` | PASS (code 17 say / 47 cue, lint clean, board 17 of 17, log clean, av 39.9 s / 38.0 s, pace 163 wpm, 2 sheets opened, no defect) |
| 9 | `check.py cs70/note11 7 --strict --scenes hands` | PASS (code 17 say / 47 cue, lint clean, board 17 of 17, log clean, av 82.8 s / 80.1 s, pace 154 wpm, 4 sheets opened, no defect) |
| 10 | `check.py cs70/note11 7 --strict --scenes stable` | PASS (code 17 say / 47 cue, lint clean, board 17 of 17, log clean, av 82.3 s / 79.7 s, pace 163 wpm, 4 sheets opened, no defect) |
| 11 | `check.py cs70/note11 7 --strict --scenes general` | PASS (code 17 say / 47 cue, lint clean, board 17 of 17, log clean, av 60.5 s / 58.7 s, pace 164 wpm, 4 sheets opened, no defect) |
| 12 | `check.py cs70/note11 7 --strict` | PASS code (17 say / 47 cue), lint clean, board 17 of 17, render OK, log clean, av 304.8 s / 302.6 s (longest silence 3.7 s), pace 156 wpm, sheets 12, report names all 12 sheets; all 6 end sheets of the full run opened, no defect — no `FAIL report` this time: the twelve sheet names did not change |
| 13 | `check.py cs70/note11 7 --strict --no-render` (after the report edit) | PASS, all ten lines, sheet list of 12 — **RESULT: PASS** |
