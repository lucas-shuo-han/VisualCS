# Strict runbook

Follow the steps in order. Read no other file of this skill unless a step names it. Each step ends in a gate; don't start the next before it is met.

`K` = this folder. `U` = the unit folder `<course>/<unit>`. `PY` = venv Python (`.venv/Scripts/python.exe` on Windows, `.venv/bin/python` elsewhere). Windows: set `PYTHONIOENCODING=utf-8`.

## Rules
1. One episode, one scene at a time. No sub-agents.
2. Never edit `manim_kit.py`, `tts.py` or `K/scripts`. If one looks wrong, stop and report.
3. Every number comes from the FACTS block, never hand-typed.
4. Only `check.py` says a scene works. "It rendered" is not a result.
5. Never pass a check by weakening the work (gluing sentences, deleting an `assert`, moving text off-stage, `KIT_CHECKS=0`).
6. Three failures at one gate: stop, report the last output.
7. Deliver a voiced 480p preview and a report. 1080p only on the user's go.
8. Report only what you did. "Not checked" is fine; an unverified claim is not.

Fixed: one language; 2–5 scenes, 3–6 beats each, 2–6 min; default edge-tts voice (no network → `--no-voice`, say so); `PACE` from `assets/strict_series.py`; `txt()` for words, `mono()` for code and numbers, `MathTex` only if `latex --version` works; fixed camera.

Out of scope (say so): more than three episodes, review-note rework, `narration.md`, publishing.

## With a board
If your brief names `U/BOARD-epNN.md`:
- Step 0 only if `U/manim_kit.py` is missing; leave `series.py`.
- Step 1: assert each board fact that has a formula.
- Skip step 2.
- Step 3: each `### id` = one `say()`; its `> ` lines copied unchanged as one text. "with the first word" = anims in `say()`; each `on "phrase"` = `self.cue("phrase", ...)`. Place things as the Stage line says. Narration rules are the author's; picture rules are yours.
- Lint FAIL on board words, or a beat you think wrong: build as written, list it under "questions for the author". If it blocks the gate, stop and report.

## Step 0. Set up
```bash
bash K/scripts/setup_env.sh .venv     # Windows: powershell -ExecutionPolicy Bypass -File K/scripts/setup_env.ps1
mkdir -p U
cp K/scripts/manim_kit.py K/scripts/tts.py U/
cp K/assets/strict_series.py U/series.py
cp K/assets/strict_episode.py U/ep01_pairing_sum.py
PY K/scripts/check.py U 1
```
**Gate:** `RESULT: PASS` (network error on `render` → rerun with `--no-voice`, keep it). Then read `U/ep01_pairing_sum.py` once; it is your pattern.

## Step 1. Facts
Copy the template to `U/ep01_<topic>.py` (delete the example); edit the REPLACE lines of `series.py`. Replace FACTS: compute and assert every number shown or said. Recompute the notes' examples; if yours differ, keep yours and note it.
**Gate:** `PY U/ep01_<topic>.py` runs without error.

## Step 2. Plan
Copy `K/assets/strict_plan.md` to `U/PLAN.md`; fill every cell as you go. Chain table: one row per sentence idea; "uses" names only an earlier row or "on screen". Every stated date, name, definition, theorem goes in "Stated facts" with its notes line and all its conditions; no line → mark "own memory", prefer leaving out.
**Gate:** yes to each, written in PLAN.md:
- First row shows one concrete case with real numbers?
- Every "uses" points to an earlier row or the screen?
- Every name or formula introduced after the viewer sees it happen?
- Every notes item in the coverage table, with a scene or a reason?
- Every stated fact has a line number or "own memory"?
- Every scene, the first too, has a drawn object, not sentences?

## Step 3. Write one scene
One beat per 2–4 chain rows.

Narration:
- One `say()` = 2–4 sentences, each 10–25 words. Never one short sentence per `say()`.
- Each sentence starts from the last ("so", "which means", "now"). Never continue a sentence in the next `say()`.
- Numbers as words, no symbols, no colons, no "Step two". Notation on screen.
- `\n` where the thought turns, in any beat over 60 words.
- Lone variable letter: "the scalar a", or rename.

Picture:
- What a beat names appears when named: first thing inside `say()`, the rest with `self.cue("words from the beat", ...)`. Beat over 14 s → at least two animation steps.
- Build objects and change them. Screen text = labels ≤ 4 words. Draw the situation in the opening scene too.
- Never an empty stage while talking. A result goes next to its picture.
- Two lines between the same points: `ArcBetweenPoints(p, q, angle=±0.5)`. Lines stop at circle edges (`buff=radius`); no line crosses text.
- End every scene method with `self.hold()`.
- Word in a box ≤ box width − 0.2. Only the heading above y = 2.7.
- Voice counts N things → exactly N separately visible.
- Inside y −2.9…3.3, x ±6.8. Labels via `.next_to(obj)` after the object is placed. Side-by-side blocks ≤ 6.3 wide.
- Objects kept across scenes on `self`; remove the rest with `FadeOut` or `self.clear_stage()`.

```python
# bad
self.say("Step 2: the pairs.")
self.say("Each pair = 11.")
# good
self.say("So the ten numbers split into five pairs, and each pair is worth eleven. "
         "Five times eleven is fifty-five, the same total as before.", FadeIn(count))
self.cue("Five times eleven", FadeIn(product))
```

## Step 4. Check the scene
`PY K/scripts/check.py U 1 --strict --scenes <scene>`
**Gate:** `RESULT: PASS`. Fix the first FAIL line, rerun.

| Line | Do |
|---|---|
| `code` | keep the template's shape: `SCENES`, `preview_only`, `end_card` |
| `lint choppy / split` | merge into one beat of linked sentences |
| `lint long` | make two sentences |
| `lint colon / numeral` | reword as speech; number as word |
| `lint cue`, `[cue]` | recopy the cue phrase from the beat |
| `render` | Python error: fix the line shown |
| `[layout] overlapping` | `next_to`, or shorten |
| `[layout] off frame / subtitle band` | move inside the limits |
| `[layout] runs through the text` | move label away, or end line at shape edge |
| `[layout] shapes on top of each other` | bend one or remove the copy |
| `[textonly]` | draw the thing the beat talks about |
| `[empty]` | bring the picture in with the `say()` |
| `[still]` | add `cue()` steps |
| `av` | rerun; still failing → `--no-voice`, report it |
| `pace` WARN | ignore for one scene; see step 6 |

## Step 5. Look at the frames
Open every sheet step 4 listed (image viewer or file-read tool on the `.png`; try before deciding you can't). One line per sheet in `U/REPORT.md` (from `K/assets/strict_report.md`; later episodes `PLAN-epNN.md`, `REPORT-epNN.md`). Judge layout on `_end` sheets; `_mid` only for questions 3–4 (half-faded is not an overlap).
1. Text on a shape, curve or text?
2. Anything cut off or touching the subtitle?
3. Leftovers from an earlier beat?
4. Empty or nearly empty frame while the subtitle talks?
5. A number disagreeing with its subtitle?
6. A count different from what the subtitle counts?
7. A frame of only sentences?

All no → scene done. Any yes → fix, step 4, look again. Image tool truly fails → "frames not inspected" + error in report.
**Repeat steps 3–5 for each scene.**

## Step 6. Whole episode
Fill `end_card([...])`: 3–4 full sentences, results only. `PY K/scripts/check.py U 1 --strict` (first run ends `FAIL report`: expected). Look at every sheet as in step 5, then rerun with `--no-render`.
Then `PY K/scripts/asr_check.py U 1 --out U/ASR-ep01.md`: add a `say_as.py` entry for each misheard term; list misheard ordinary words, pauses and rate flags in the report (don't reword a board).
**Gate:** `RESULT: PASS` and every sheet answered. `pace` WARN: >165 → each `PACE` value +0.2; <120 → −0.2; rerun without `--no-render` and look again. Never change words for pace.

## Step 7. Report and stop
Give the user: preview and `.srt` paths; the last check table, copied; the coverage table; every difference from the notes' numbers; what you didn't do (frames not inspected, voice not heard — you can't hear, say so, out-of-scope items).
Ask: is the voice and speed right, should 1080p run. On yes:
```bash
PY K/scripts/render.py U --out videos/<course>-<unit> --media <temp folder>
PY K/scripts/srt_to_script.py videos/<course>-<unit> U/SCRIPT.md --title "<series>"
```
Next episode: add a row to `EPISODES`, repeat steps 1–7 with N.

## Stuck
- Helpers (code listing, registers, bit fields, memory, network, heatmap): first 50 lines of `U/manim_kit.py`.
- Slow: `--scenes`, never the whole episode mid-work. Keep unwritten scenes out of `SCENES` and the file.
- Don't edit during a render; one render at a time; long timeout, don't restart.
- Disk full or `.svg` `ParseError`: free space, delete zero-size `.svg` under media `Tex` and `texts`.
- Method and mobject names: ASCII only.
- Windows LaTeX `.dvi to SVG` error in `render.py`: `MANIM_CWD` and `--media` on drive C.
