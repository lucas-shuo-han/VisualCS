# Trial log: episode 10, strict edition

One line per `check.py` run.

| # | Command | Result |
|---|---|---|
| 1 | `check.py cs70/note11 10 --strict --scenes hook` | PASS — code, lint, board, render, log, av, pace, sheets |
| 2 | `check.py cs70/note11 10 --strict --scenes cleo` | FAIL render — `NameError: name 'BELOW_JOB' is not defined` (line 272) |
| 3 | `check.py cs70/note11 10 --strict --scenes cleo` | PASS after `BELOW_JOB` was added to FACTS |
| 4 | `check.py cs70/note11 10 --strict --scenes law` | PASS |
| 5 | `check.py cs70/note11 10 --strict --scenes swap` | PASS |
| 6 | `check.py cs70/note11 10 --strict` (full episode) | FAIL report only — every other stage PASS; expected, the report did not exist yet |
| 7 | `check.py cs70/note11 10 --strict --no-render` | PASS — see REPORT-ep10.md |

Scene-only runs report `pace OK` by rule; the full run reads 157 words per minute.

## Round 2: REVIEW-ep10.md

The review's seven rows were done in `ep10_candidate_pessimal.py` (the review wins over the
board where they differ). One line per run:

| # | Command | Result |
|---|---|---|
| 8 | `check.py cs70/note11 10 --strict --scenes hook` | PASS — rows 2 and 3 (the right-strip text and the two green cell borders) |
| 9 | `check.py cs70/note11 10 --strict --scenes cleo` | PASS — rows 1, 2 and 4 in scene `cleo` |
| 10 | `check.py cs70/note11 10 --strict --scenes law` | PASS — row 1 in scene `law` |
| 11 | `check.py cs70/note11 10 --strict --scenes swap` | PASS — rows 4, 5, 6 and 7 |
| 12 | `check.py cs70/note11 10 --strict` (full episode) | PASS — 40 `cue()`, 10 sheets, 157 words per minute |
| 13 | `check.py cs70/note11 10 --strict --no-render` | PASS — the table above |

Row 5 was the one row that could not be done as written: "hospitals propose" at size 20 in
a strip 1.2 wide would come out under size 16, so the review's own fallback was used — the
one-line year text goes in the gap while the arrows are gone. That leaves the gap and not
the right strip holding it, which is a deliberate difference from BOARD-ep10.md's beat 4.3.
Every other row is as the review writes it.
