# TRIAL LOG: ep02 the residency match

One line per `check.py` run.

| # | command | result |
|---|---|---|
| 1 | `check.py cs70/note11 2 --strict --scenes hook` | FAIL render: `ValueError: could not broadcast input array from shape (1,2) into shape (1,3)` — the arrow end points were 2-tuples; made them 3-element. Lint also WARNed on the end-card "1950s": the board's four end-card bullets were written with digits, put into words (the beats are untouched). |
| 2 | `check.py cs70/note11 2 --strict --scenes hook` | PASS (2 say, 7 cue, lint clean, board 2/13 word for word, log clean, av 34.3 s / 31.7 s, longest silence 1.5 s, pace 170 wpm, 2 sheets opened, no defect) |
| 3 | `check.py cs70/note11 2 --strict --scenes race` | PASS (6 say, 18 cue, lint clean, board 6/13, log clean, av 62.9 s / 60.4 s, pace 170 wpm, 4 sheets opened, no defect) |
| 4 | `check.py cs70/note11 2 --strict --scenes fuse` | PASS (9 say, 27 cue, lint clean, board 9/13, log clean, av 48.7 s / 46.4 s, pace 185 wpm, 4 sheets opened, no defect; one subtitle is the single word "meantime." — the kit's caption splitter cutting the board's sentence at the width limit, not a scene defect) |
| 5 | `check.py cs70/note11 2 --strict --scenes match` | PASS (13 say, 39 cue, lint clean, board 13/13, log clean, av 71.2 s / 69.7 s, longest silence 2.3 s, pace 160 wpm, 4 sheets opened, no defect) |
| 6 | `check.py cs70/note11 2 --strict` (whole episode; the first run of step 6) | FAIL report only: `REPORT.md (or REPORT-ep02.md) has no line for 12 of 12 sheets`. Every other line PASS (code 13 say / 39 cue, lint clean, board 13/13 word for word, render 256.8 s, log clean, av video 256.8 s / audio 254.0 s / longest silence 3.9 s, pace 46 subtitles at 163 wpm, sheets 12). All 12 sheets opened and written up in REPORT-ep02.md; no defect. |
| 7 | `check.py cs70/note11 2 --strict --no-render` | PASS (see the table in REPORT-ep02.md) |

## Fix round after review round 1 (`REVIEW-ep02.md`)

The five review rows, built from the board's new picture lines (no narration word changed).
One scene at a time first, never two at once, then the whole episode.

| # | command | result |
|---|---|---|
| 8 | `check.py cs70/note11 2 --strict --scenes race` | PASS (code 13 say / 39 cue, lint clean, board 13/13, log clean, av 65.4 s / 62.5 s, longest silence 1.8 s, pace 163 wpm, 4 sheets; end sheet01 frames 9-12 opened: the dashed yellow arrow under "sophomore" now has width 5, dash length 0.15 and a solid tip, frames 15-17 of the full run) |
| 9 | `check.py cs70/note11 2 --strict --scenes fuse` | PASS (lint clean, board 13/13, log clean, av 50.8 s / 48.2 s, longest silence 1.8 s, 4 sheets; end sheets 00 and 01 opened: H2 and H3 grey from the outer slots, no two arrows crossing; W white and dashed to the free slot at x = 2 with a tip; H1 green at stroke width 8 and flashed, then orange at width 4; the last cue flashes W and the slot at x = 2) |
| 10 | `check.py cs70/note11 2 --strict --scenes match` | PASS (lint clean, board 13/13, log clean, av 73.5 s / 71.7 s, longest silence 2.3 s, pace 155 wpm, 4 sheets; end sheet00 opened: the orange dashed line D between hospital 1 and graduate 1 at width 5, dash length 0.15) |
| 11 | `check.py cs70/note11 2 --strict` (whole episode) | PASS every line: code 13 say / 39 cue, lint clean, board 13/13 word for word, render 265.0 s, log clean, av video 265.0 s / audio 262.2 s / longest silence 3.9 s, pace 46 subtitles at 157 wpm, sheets 12, report names all 12 sheets. Sheets end 01-04 and mid 01-03 opened; each change is in them and readable. No FAIL, so the run is the fix round's full run. |
| 12 | `check.py cs70/note11 2 --strict --no-render` | PASS, the same table (the preview of run 11); the run the report quotes |
