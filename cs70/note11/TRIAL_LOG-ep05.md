# TRIAL LOG: ep05 offers only get better

One line per `check.py` run.

| # | command | result |
|---|---|---|
| 1 | `check.py cs70/note11 5 --strict --scenes hook` | PASS (code 4 say / 13 cue, lint clean, board 4 of 14, log clean, av 64.7 s / 62.4 s, pace 174 wpm, 4 sheets opened, no defect) |
| 2 | `check.py cs70/note11 5 --strict --scenes anita` | PASS (code 8 say / 24 cue, lint clean, board 8 of 14, log clean, av 61.2 s / 58.8 s, pace 176 wpm, 4 sheets opened, no defect) |
| 3 | `check.py cs70/note11 5 --strict --scenes proof` | PASS (code 14 say / 43 cue, lint clean, board 14 of 14, log clean, av 102.5 s / 101.0 s, pace 194 wpm, 6 sheets opened, no defect; `J` on rung 4 and `J'` on rung 2 checked on the pixels of frame 12) |
| 4 | `check.py cs70/note11 5 --strict` | PASS code, lint, board 14 of 14, render 269.5 s, log, av (267.2 s, longest silence 3.6 s), sheets 12 — WARN pace 177 wpm — FAIL report (no line for 6 of 12 sheets, expected on the first full run); all 12 sheets opened, no defect |
| 5 | `check.py cs70/note11 5 --strict --no-render` | PASS (code 14 say / 43 cue, lint clean, board 14 of 14, log clean, av 269.5 s / 267.2 s, WARN pace 177 wpm, sheets 12, report names all 12 sheets) — **RESULT: PASS** |
| 6 | `check.py cs70/note11 5 --strict --scenes hook` (fix round: line B of 1.3 and 1.4) | PASS (lint clean, log clean; end and mid sheets opened — the two new line-B texts are complete, inside the frame and clear of the day boxes, no defect) |
| 7 | `check.py cs70/note11 5 --strict --scenes anita` (fix round: Control red, orange on the list only) | PASS (lint clean, log clean; sheets opened — the "Control" in the day-1 offers cell is red from 2.2 and flashed in 2.3, the orange border only on Control's cell in Anita's list, no defect) |
| 8 | `check.py cs70/note11 5 --strict --scenes proof` (fix round, first run) | **FAIL log** — beat 5 "So the claim is true on the day of the offer": `[layout] a Arrow runs through the text 'day k'`; the day strip was handed to `FadeOut` as a `VGroup` built inline in the beat, and the Cairo branch of `Scene.remove` calls `restructure_mobjects(..., extract_families=False)` (`manim/scene/scene.py:581`), so the scene's list is searched for that new wrapper itself — which is in no scene family — and nothing is removed; the boxes of "day k" and "day i" stayed on stage under the chain row. Fixed by fading the on-stage objects themselves (`strip = [*day, dots, hand_grp, *self.hand_txt3, self.step, plab]`) |
| 9 | `check.py cs70/note11 5 --strict --scenes proof` (fix round, second run, after the strip is faded out object by object) | PASS (lint clean, board 14 of 14, log clean; end and mid sheets opened — no "J'" on any rung, the green J' bracket beside rungs 1 to 4, the chain row green one box at a time with the large "..." green at the end, no defect) |
| 10 | `check.py cs70/note11 5 --strict` (fix round, whole episode) | PASS code 14 say / 43 cue, lint clean, board 14 of 14, render, log clean, av 278.8 s / 276.5 s (longest silence 3.6 s), WARN pace 46 subtitles 170 wpm, sheets 12, report names all 12 sheets — all 12 sheets opened, no defect |
| 11 | `check.py cs70/note11 5 --strict --no-render` (fix round, final) | PASS (code 14 say / 43 cue, lint clean, board 14 of 14, log clean, av 278.8 s / 276.5 s, WARN pace 170 wpm, sheets 12, report names all 12 sheets) — **RESULT: PASS** |

Note on rows 6-9: the scene runs write the same sheet file names as the whole-episode run, so
the full run of row 10 overwrote them; the frame-by-frame record of rows 6-9 is in
`REPORT-ep05.md`, section "Sheets of the scene runs of the fix round". Scene runs do not print
an av or pace line of their own (they reuse the episode audio), so those rows carry no numbers
of their own; the "no defect" verdicts are from opening the sheets.
