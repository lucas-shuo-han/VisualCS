# Strict runbook: notes → narrated Manim video

For a small or cheap model, or anyone told to work in strict mode. Follow the steps in
order. Do not read the other documents of this skill unless a step names one. Every
step ends in a gate; do not start the next step before the gate is met.

Names used below: `K` = the folder this file is in. `U` = the unit folder you create,
`<course>/<unit>`. `PY` = the Python of the virtualenv (`.venv/Scripts/python.exe` on
Windows, `.venv/bin/python` elsewhere).

## Rules of this mode

1. One language, one episode at a time, one scene at a time. No sub-agents.
2. Never edit `manim_kit.py`, `tts.py` or anything in `K/scripts`. If one of them looks
   wrong, stop and report it.
3. Never hand-type a number into a picture. Numbers come from the FACTS block.
4. The only way to know a scene works is `check.py`. "It rendered" is not a result.
5. Never make a check pass by weakening the work: do not glue two sentences into one
   to silence the lint, delete an `assert`, move a text off-stage, or set `KIT_CHECKS=0`.
6. Three failed attempts at the same gate: stop, and report the output of the last one.
7. You deliver a voiced 480p preview and a report. The 1080p render waits for the
   user's go, because a change of voice or speed afterwards costs the whole render.
8. Say only what you did. "Not checked" is an acceptable line in the report; a claim
   you did not verify is not.

Fixed choices, so there is nothing to decide:

| | |
|---|---|
| Language | the language of the request (`SOURCE_LANG`); a second one only in step 8 |
| Length | 2 to 5 scenes per episode, 3 to 6 beats per scene, 2 to 6 minutes |
| Voice | the default edge-tts voice; no network → add `--no-voice` and say so |
| Pauses | `PACE` as in `assets/strict_series.py` |
| Text | `txt()` for words, `mono()` for code and numbers; `MathTex` only if `latex --version` works |
| Camera | fixed; no zooms |

Out of scope here; say so in the report and leave it: more than three episodes,
reworking an existing video from review notes, the editable `narration.md` workflow,
publishing.

## With a storyboard

If your brief names a `U/BOARD-epNN.md`, an author has already made the decisions
(`PIPELINE.md` describes the whole arrangement; you do not need to read it):

- Step 0: do it only if `U/manim_kit.py` is missing. `U/series.py` exists; leave it.
- Step 1: the numbers are the BOARD's "Facts" table: assert each one that
  its "Computed how" cell gives a formula for in your FACTS block.
- Step 2: skip it. The BOARD is the plan.
- Step 3: each `### id` beat is one `say()`. Copy its `> ` lines into the `say()` as
  one text, unchanged: `check.py` FAILs on a different word. "with the first word" is
  the animation inside the `say()` call; each `on "phrase"` line is a `self.cue("phrase", ...)`.
  Put things where the "Stage" line says. The narration rules of step 3 are the
  author's business; the picture rules are still yours.
- A lint FAIL on the BOARD's own words, or a beat you think is wrong: build it as
  written, and list it under "questions for the author" in your report. If the lint
  FAIL blocks the gate, stop there and report it.

## Step 0. Set up and prove it

```bash
bash K/scripts/setup_env.sh .venv          # Windows: powershell -ExecutionPolicy Bypass -File K/scripts/setup_env.ps1
mkdir -p U
cp K/scripts/manim_kit.py K/scripts/tts.py U/
cp K/assets/strict_series.py U/series.py
cp K/assets/strict_episode.py U/ep01_pairing_sum.py
PY K/scripts/check.py U 1
```

Skip the first line if `.venv` exists. On Windows set `PYTHONIOENCODING=utf-8` first.

**Gate:** the last line group starts with `RESULT: PASS`. This proves the environment
with a known-good episode, before any of your own code exists. If it says FAIL on
`render` with a network error, run it again with `--no-voice` and keep that flag for
the whole job.

Then read `U/ep01_pairing_sum.py` once, top to bottom. It is your pattern for everything.

## Step 1. Facts

Create your episode file by copying the template: `U/ep01_<topic>.py` (delete
`ep01_pairing_sum.py`), and edit `U/series.py` (the lines marked REPLACE; `file` and
`scene` must match your file and class name).

Replace the FACTS block: compute every number the episode will show or say, and assert
it. If the notes give a worked example, compute it again here; when your result differs
from the notes, keep yours and write the difference down for the report.

**Gate:** `PY U/ep01_<topic>.py` exits without an error.

## Step 2. Plan

Copy `K/assets/strict_plan.md` to `U/PLAN.md` and fill in every cell. Write the plan
into the file as you go; do not work it all out in your head first. The chain table is
the important part: one row per sentence idea, and the column "uses" may only name an
earlier row or "the viewer sees it on screen".

Every date, name, definition and theorem you will state goes into the "Stated facts"
table with the line number of the notes it comes from, copied with all its conditions
(a theorem that says "connected and even degree" keeps both). A fact with no line in
the notes is from your own memory: mark it so, and prefer leaving it out.

**Gate:** answer in PLAN.md, each with yes:
- Does the first row of the first scene show one concrete case with real numbers?
- Does every "uses" cell point to an earlier row or to the screen?
- Is every name or formula introduced in a row *after* the row where the viewer sees it happen?
- Does every item of the notes appear in the coverage table, with a scene or a reason?
- Does every row of "Stated facts" have a notes line number, or the mark "own memory"?
- Does every scene, the first one too, have a drawn object in its "picture" cell
  (shapes, lines, boxes, a graph), not sentences on the screen?

A "no" means reorder or add rows until it is a yes.

## Step 3. Write one scene

Write the method for the next scene in SCENES, from its chain table. One beat per two
to four rows. Rules, all of them checked later:

**Narration**
- A beat is one `say()` with 2 to 4 sentences. Each sentence 10 to 25 words (Chinese:
  15 to 40 characters). Never one short sentence per `say()`.
- Each sentence starts from the one before: "so", "which means", "now", "and that is why".
- A sentence never continues in the next `say()`.
- Numbers as words ("fifty-five"), no symbols, no colons, no "Step two". The notation
  is on the screen; the voice says the idea.
- A line break `\n` inside the text where the thought turns, in any beat over 60 words.
- One variable letter in a sentence is risky ("a" is read as the article). Say "the
  scalar a" or rename it.

**Picture**
- Everything a beat names appears or changes when it is named: the first thing in the
  `say()` call, each further thing with `self.cue("words copied from the beat", ...)`.
  A beat longer than 14 seconds needs at least two animation steps.
- Build objects (boxes, arrows, a graph) and change them. No bullet lists and no
  sentences on screen: a text on the picture is a label of at most four words. This
  holds for the opening scene too: draw the situation the story is about.
- Never leave the stage empty while the voice talks, and do not clear the picture to
  show a sentence. A result is written next to the picture it is about.
- Two lines between the same two points must be bent apart, or they look like one:
  `ArcBetweenPoints(p, q, angle=0.5)` and `ArcBetweenPoints(p, q, angle=-0.5)`.
- A line to a labelled circle stops at the circle's edge, not at its centre:
  `Line(a.get_center(), b.get_center(), buff=radius)`. No line may cross a text.
- End every scene method with `self.hold()`: it waits until the voice has finished the
  last beat. Without it the next scene removes the picture while it is still being
  talked about.
- A word inside a box is at most the box's width minus 0.2: scale it down if it is wider.
  Nothing but the heading above y = 2.7; the heading's underline is near y = 3.0.
- If the voice counts things ("seven edges"), exactly that many are separately visible.
- Keep everything between y = −2.9 and y = 3.3 and x = ±6.8. Below −2.9 is the subtitle.
- Place a label with `.next_to(its_object, ...)`, after the object is in its final
  place. No two texts at hand-typed coordinates.
- Two blocks side by side: 6.3 units wide each, at most.
- The previous scene's objects that you still need are on `self` (see the template).
  Remove what you no longer need with `FadeOut` or `self.clear_stage()`.

Bad, then good:

```python
self.say("Step 2: the pairs.")                  # a label, a colon, a numeral, five words
self.say("Each pair = 11.")
```
```python
self.say("So the ten numbers split into five pairs, and each pair is worth eleven. "
         "Five times eleven is fifty-five, the same total as before.", FadeIn(count))
self.cue("Five times eleven", FadeIn(product))
```

## Step 4. Check the scene

```bash
PY K/scripts/check.py U 1 --strict --scenes <scene_name>
```

**Gate:** `RESULT: PASS`. On FAIL, fix the first FAIL line and run the same command
again. What each line means:

| Line | Do |
|---|---|
| `code` | the file must keep the template's shape: `SCENES`, `preview_only`, `end_card` |
| `lint choppy / split` | merge short beats into one beat of linked sentences |
| `lint long` | make two sentences of it |
| `lint colon / numeral` | reword as a spoken sentence; write the number as a word |
| `lint cue`, `log [cue]` | copy the cue phrase again from the beat's current text |
| `render` | a Python error: read the lines shown, fix that line |
| `log [layout] overlapping text` | place one with `next_to` the other, or shorten it |
| `log [layout] off the frame / subtitle band` | move it inside the limits of step 3 |
| `log [layout] ... runs through the text` | move the label off the line (`next_to` with a direction away from it), or end the line at the shape's edge |
| `log [layout] two ... shapes exactly on top of each other` | bend one of them, or remove the copy |
| `log [textonly]` | that beat shows only words: draw the thing it talks about and keep it on stage |
| `log [empty]` | that beat talks over an empty stage: bring the picture in with the `say()`, not after it |
| `log [still]` | add `cue()` steps to that beat so the picture changes while it is spoken |
| `av` | run once more; still failing → use `--no-voice` and say so in the report |
| `pace` (WARN) | leave it for a single scene; for the whole episode see step 6 |

## Step 5. Look at the frames

Look at every sheet file that step 4 listed (frames are numbered by subtitle). Use
your tool that shows an image file (an image viewer or the file-reading tool, given the
`.png` path). Try it on the first sheet before you decide that you cannot see images.
For each sheet write one line in `U/REPORT.md` (copy `K/assets/strict_report.md` the
first time): the sheet's name as `ep01_sheets_end/sheet00.png`, then the answers.
From the second episode of a unit on, the files are `PLAN-ep02.md` and `REPORT-ep02.md`.

The `_end` sheets show each subtitle's last moment: judge the layout on these. The
`_mid` sheets show its middle, often during a move or a fade: use them for questions 3
and 4 only, and do not report a half-faded object there as an overlap.

1. Is any text on top of a shape, a curve or other text?
2. Is anything cut off at an edge or touching the subtitle?
3. Is anything left over from an earlier beat that should be gone?
4. Is any frame empty or nearly empty while the subtitle talks about something?
5. Does any number on the frame disagree with its subtitle?
6. Count what the subtitle counts (edges, boxes, steps): is a different number visible?
7. Is there a frame that shows only sentences, with no drawn object?

All "no": the scene is done. Any "yes": fix, run step 4 again, look again. If the
image tool really fails, write "frames not inspected" and the error in the report and
go on.

**Then repeat steps 3 to 5 for the next scene.**

## Step 6. Check the whole episode

Fill in the `end_card([...])` bullets: three or four full sentences, results only.

```bash
PY K/scripts/check.py U 1 --strict
```

The first run ends with `FAIL report`: that is expected. Look at every sheet of this
run as in step 5, write its line in `U/REPORT.md`, then run the same command with
`--no-render` added.

**Gate:** `RESULT: PASS`, and the questions of step 5 answered for every sheet. If the
`pace` line says WARN: above 165, raise each `PACE` value in `series.py` by 0.2; below
120, lower each by 0.2; run again without `--no-render` (a new pace is a new video, so
look at its sheets again). Do not change the words to change the pace.

## Step 7. Report and stop

Complete `U/REPORT.md` and give the user, in the chat:
- the path of the preview video and its `.srt` (from the `render` line);
- the result table of the last `check.py` run, copied, not retold;
- the coverage table from PLAN.md;
- every difference between your numbers and the notes;
- what you did not do: frames not inspected, voice not listened to (you cannot listen,
  so say so), rendered without voice, anything out of scope.

Then ask two things and stop: is the voice and its speed right, and should the 1080p
render run. On a yes:

```bash
PY K/scripts/render.py U --out videos/<course>-<unit> --media <a temp folder>
PY K/scripts/srt_to_script.py videos/<course>-<unit> U/SCRIPT.md --title "<series name>"
```

More episodes: add a row to `EPISODES` in series.py and do steps 1 to 7 again with the
next number N, using `PLAN-epNN.md` and `REPORT-epNN.md` for that episode's plan and report.

## Step 8. A second language (only if asked)

1. Add the language to `LANGS` and to `SERIES_NAME`, `title`, `sub`, `slug` in series.py.
2. `PY K/scripts/i18n_check.py U 1 --skeleton` prints every string that needs a
   translation. Paste them into `U/i18n/ep01.py` as `EN = {...}` (or `ZH = {...}`) and
   fill them in: natural sentences in that language, the same order of ideas.
3. `PY K/scripts/check.py U 1 --lang <code>`, then step 5 on its sheets. Translations
   are wider: shorten the translation before you touch the layout.

## If you are stuck

- A helper you need (code listing, register boxes, bit fields, memory, a network
  diagram, a heatmap) is in the kit: read the first 50 lines of `U/manim_kit.py`.
- The render is slow: use `--scenes`, never the whole episode, while a scene is unfinished.
- With `--scenes` the `code` and `lint` lines still cover the whole file: keep the
  scenes you have not written yet out of `SCENES` and out of the file.
- Do not edit a file while its render is running. Do not run two renders at once; when
  other work loads the machine a whole episode can take 20 minutes, so give the command
  a long timeout instead of starting it again.
- "No space left on device", or afterwards a `ParseError` on an `.svg`: free space on the
  drive, delete the `.svg` files of size zero under the media folder's `Tex` and `texts`
  folders, and run again.
- Name a scene method and a mobject with plain letters and digits (`k5`, not `K₅`).
- Windows and LaTeX: `check.py` already renders from the system drive. If `render.py`
  fails with "does not support converting .dvi files to SVG", set `MANIM_CWD` and
  `--media` to a folder on drive C.
