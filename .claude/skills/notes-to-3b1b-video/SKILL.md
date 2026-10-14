---
name: notes-to-3b1b-video
description: Turn course notes, lecture slides, textbook chapters, a derivation or a study topic into 3Blue1Brown-style animated explainer videos with Manim — dark background, animated diagrams, a neural voice-over whose words drive the animation, sentence-by-sentence subtitles (.srt and on the frame), and optionally the same series in a second language. Use this whenever someone wants to visualize or animate a course (CS61C, CS182, CS189, linear algebra, algorithms, deep learning ...), make "3b1b-style" / Manim videos, turn notes or a PDF into explainer videos, walk through one long proof or derivation as a video, add narration or a translated version to such videos, fix a video that is "too rough", "too fast" or "sounds robotic", or build a visual study series — even if they only say "make videos for this class", "animate these lecture notes" or "explain this topic visually".
---

# Notes → 3Blue1Brown-style videos

This file is for a model that plans and judges on its own: it states what the video must
achieve and leaves the how to you. A small or cheap model, or anyone told to work in
strict mode, follows `STRICT.md` instead and reads nothing else here.

## The pipeline

Five stages, each leaving one file the next stage works from. Subtitles, voice and
timing are not stages: the kit derives all three from the narration text, so the only
things anyone writes are the lesson design, the script with its pictures, and the code.

```
notes ─► 1 DESIGN ─► 2 BOARD ─► 3 BUILD ─► 4 CHECK ─► 5 DELIVER
         teaching     script +    Manim       machine,     1080p, srt,
         decisions    pictures    code        frames, ear  script, README
         PLAN.md      BOARD-epNN  epNN_*.py   REVIEW-epNN  videos/
         (judgement)  (judgement) (execution) (judgement + execution)
```

| Stage | Decides | Parallel? | Who, in a pipeline run |
|---|---|---|---|
| 1 Design | what each episode teaches, in what order, and why the viewer cares | no: one mind per unit | strongest model, then the user |
| 2 Board | every spoken word and what changes on which word | per episode, after a pilot | strongest model |
| 3 Build | nothing; it executes the board | per episode (two renders per machine) | cheap model on `STRICT.md` |
| 4 Check | whether the frames match the board; whether it sounds right | per episode | mid model for frames, the user for the ear |
| 5 Deliver | nothing | — | coordinator |

Working alone on a few episodes, you play every role, but keep the files: the board is
what the user reviews, and it is what `check.py` holds the code to. For a large unit on
a budget, `PIPELINE.md` runs the roles as separate agents with their own briefs.

Quality is decided in stages 1 and 2. A cheap builder passing every gate on a weak
board makes a weak video; a strong builder cannot rescue it either. Spend effort there.

**Two user gates.** After stage 1 (the design, short enough to read in two minutes)
unless the user said to go ahead; and after a pilot (the easiest and the hardest
episode built through stage 4 and heard as a voiced preview) before the other episodes
are boarded. Voice, speed and pace were what forced every earlier series to be redone.

## 1. Design: what makes it teaching, not a reading of the notes

Notes are written for someone sitting the course; they state results in their final
order and skip the reasons a learner would want them. The video's job is to supply
what the notes leave out. For each episode decide, in `PLAN.md`:

- **The question** the viewer cannot answer before and can after, and why they would
  want to: a concrete situation where it matters, not "today we learn X".
- **The obvious attempt and where it fails.** The natural first idea, tried on real
  numbers, breaking in a way the viewer sees. The idea that works is the repair. The
  failures are content; a video that only shows the correct path announces instead of
  derives.
- **The concrete case** carrying the episode, with real numbers computed in Python, the
  notes' own example where there is one.
- **The moment it clicks**, and the picture that makes it click.
- **The order**: each step uses only what the one before produced. A case before the
  rule, the reason before the definition, a name after the thing has been seen, the
  overview last.
- **What to leave out**, with the reason. Coverage means every substantive item of the
  notes is in an episode or omitted on purpose (`COVERAGE.md`), not that every line is
  narrated.
- **Length** from content: ask the user how many minutes the unit deserves before
  splitting it into episodes.

## 2. Board: the script and its pictures together

Which word a picture changes on is one decision, so words and pictures are written in
one file, `BOARD-epNN.md` (`assets/board_template.md`). Requirements:

- **Spoken, not read.** Linked sentences, plain words, numbers and symbols as words,
  notation on screen and the idea aloud (`speak=`). Paced near 140 words per minute
  including pauses; pauses do the work, never cut words to slow down.
- **The picture makes each sentence true as it is said.** Objects that build and
  transform, never bullet text; every claim of an argument as a line on screen when
  spoken; the eye drawn to what is named.
- **Show the small thing**: move the camera to where the argument lives; choose values
  the picture can tell apart.
- **No step skipped.** Where the notes say "clearly" or jump two lines of algebra, the
  step is worked out and added, marked as added. Facts used without proof are said so.
- **Every number** computed and asserted in code; notes errors corrected and reported.
- **One look**: one typeface (LaTeX when math-heavy), few sizes, one colour and one
  spoken form per concept (`GLOSSARY.md`, `say_as.py`).

`references/narration-writing.md` has the spoken-script craft; `derivation-episodes.md`
the craft of one long argument; `visual-patterns.md` the frame and camera.

## 3. Build

The kit: `say(text, *anims)` voices a beat (two to four sentences about one picture)
sentence by sentence and shows one subtitle sentence at a time; `cue("phrase", *anims)`
lands an animation on a phrase of the beat; `zoom_to` / `pin` / `clear_stage` /
`title_card` / `end_card`. API in the docstring of `scripts/manim_kit.py`, a whole
episode in `assets/example_episode.py`. Set up with `scripts/setup_env.sh` (or `.ps1`)
and copy `manim_kit.py`, `tts.py`, `series_template.py` → `series.py`, `say_as_asm.py`
→ `say_as.py` into `<course>/<unit>/` so the project stands alone.

Choose before the first full render, because a change redoes every clip: languages
(for two, write the CJK one and translate through tables), voice and speed by the
user's ear (`audition.py`), `PACE`, `TEXT_FONT`, subtitles burned or not.

## 4. Check

`python scripts/check.py <unit> N` runs the lint, a voiced 480p preview, the kit's
layout and stillness findings, audio against video, pace, and, with a board present,
that the code says the board's words in order. PASS is necessary, not sufficient: it
cannot see a weak explanation, a label over a shape, a wrong number or bad prosody.
So open every contact sheet against the board, and get the voice heard. Send the user
the first voiced preview with its exact path as soon as it exists.

Review notes from the user become a written plan first (cause with file and line, fix,
check); new content goes into the board before any code (`derivation-episodes.md` §6).

## 5. Deliver

`i18n_check.py`, then one `render.py <unit> --out videos/<course>-<unit>`, `pace.py`,
`srt_to_script.py`; spot-check the 1080p output; README with an episode table; commit.
The final message gives paths, episodes, the coverage table, and plainly what was not
done: content from your own knowledge, scenes not re-inspected, whether anyone listened.

## Read when

| File | When |
|---|---|
| `PIPELINE.md` | the roles as separate agents; cheap builders on other providers |
| `references/narration-writing.md` | before the first board; when a listener objects |
| `references/derivation-episodes.md` | one long argument; "too rough / too fast / just states things"; acting on review notes |
| `references/visual-patterns.md` | layout budget, kit snippets, camera, typeface |
| `references/bilingual-and-voice.md` | a second language; engine or voice; a mispronounced term |
| `references/production.md` | coverage map, delivery checklist, publishing |
| `references/pitfalls.md` | before the first render on a machine; when something breaks |
