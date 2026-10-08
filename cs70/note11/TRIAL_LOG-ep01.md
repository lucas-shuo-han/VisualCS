# TRIAL LOG: ep01 propose and reject

One line per `check.py` run.

| # | command | result |
|---|---|---|
| 1 | `check.py cs70/note11 1 --strict --scenes hook` | PASS (code, lint, board, render, log, av, pace; 4 sheets opened) |
| 2 | `check.py cs70/note11 1 --strict --scenes first_try` | PASS (19 say, 61 cue, lint clean, board 19/19, log clean, av 81.5 s / 79.9 s, pace 164 wpm, 4 sheets opened) |
| 3 | `check.py cs70/note11 1 --strict --scenes days` | PASS (lint clean, board 19/19, log clean, av 73.2 s / 71.7 s, longest silence 1.5 s, pace 155 wpm, 4 sheets opened, no defect) |
| 4 | `check.py cs70/note11 1 --strict --scenes result` | PASS (lint clean, board 19/19, log clean, av 40.9 s / 39.3 s, pace 157 wpm, 2 sheets opened, no defect) |
| 5 | `check.py cs70/note11 1 --strict` | FAIL report only: 12 sheets, 8 had no line in REPORT-ep01.md. All 12 opened, no defect |
| 6 | `check.py cs70/note11 1 --strict --no-render` | PASS (all twelve lines: code, lint, board 19/19, render, log, av 316.0 s / 313.6 s, pace 153 wpm, sheets, report) |

Round 2, the four rows of `REVIEW-ep01.md` (rows 1 and 2 are `self.hold()` at the end of
`hook` and of `days`; row 3 is the heading rule cut at x = -5.1; row 4 caps a header word
at 2.0 wide).

| # | command | result |
|---|---|---|
| 7 | `check.py cs70/note11 1 --strict --scenes hook` | PASS (code 19 say / 61 cue, lint clean, board 19/19, log clean, av 87.0 s / 85.4 s, longest silence 1.5 s, pace 145 wpm, 4 sheets opened, no defect; frame 13 holds D1 and the four borders, the rule clears the header box, "Approximation" fits its box) |
| 8 | `check.py cs70/note11 1 --strict --scenes days` | PASS (code, lint clean, board 19/19, log clean, av 73.2 s / 71.7 s, longest silence 1.5 s, pace 155 wpm, 4 sheets opened, no defect; the last frame holds "Day after day" and "stop") |
| 9 | `check.py cs70/note11 1 --strict` | PASS (12 sheets, 319.0 s / 316.6 s, 152 wpm; frames 13 and 41 opened on the end and mid sheets, no defect; REPORT-ep01.md updated, its twelve sheet lines all pass) |
| 10 | `check.py cs70/note11 1 --strict --no-render` | PASS (the run quoted in REPORT-ep01.md: code, lint, board 19/19, render, log, av 319.0 s / 316.6 s, pace 152 wpm, sheets 12, report) |
