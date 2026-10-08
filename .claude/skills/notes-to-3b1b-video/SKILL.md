---
name: notes-to-3b1b-video
description: Turn course notes, lecture slides, textbook chapters, a derivation or a study topic into 3Blue1Brown-style animated explainer videos with Manim — dark background, animated diagrams, a neural voice-over whose words drive the animation, sentence-by-sentence subtitles (.srt and on the frame), and optionally the same series in a second language. Use this whenever someone wants to visualize or animate a course (CS61C, CS182, CS189, linear algebra, algorithms, deep learning ...), make "3b1b-style" / Manim videos, turn notes or a PDF into explainer videos, walk through one long proof or derivation as a video, add narration or a translated version to such videos, fix a video that is "too rough", "too fast" or "sounds robotic", or build a visual study series — even if they only say "make videos for this class", "animate these lecture notes" or "explain this topic visually".
---

# Notes → 3Blue1Brown-style videos

**Two editions.** This file is the lean one: requirements and lessons, for a model that
plans and judges well on its own. A small or cheap model, or anyone told to work in
strict mode, follows `STRICT.md` instead and reads nothing else here. For a large unit
on a budget, `PIPELINE.md` splits the work: a strong model writes a storyboard per
episode, cheap models build from it, a mid model reviews the frames. Pilot two
episodes before the batch, and have the user listen before anything is scaled up.

You write the narration, write one Manim scene class per episode on the bundled kit,
render, look at the frames and listen, fix, and ship MP4 + SRT + scripts. Everything
below was learned on a 14-episode Chinese/English CS61C series and a CS182 derivation
that went through several rounds of user review.

## Done means

1. `python scripts/check.py <unit> N` is PASS for every episode and language, and you
   opened every contact sheet it produced. It runs the lint, a voiced 480p preview, the
   kit's own findings (`[layout]` text overlapping, off the frame or in the subtitle
   band; `[still]` a long beat with one animation; `[cue]`), audio against video, pace.
   It cannot see a text over a shape, a leftover label, a wrong number or bad prosody.
2. Every item of the notes is mapped to a beat or omitted with a written reason.
3. Every number on screen or spoken is computed in Python, the key ones asserted,
   including the notes' own examples. Notes errors are corrected and reported.
4. Delivered: 1080p MP4 + `.srt` per language, `SCRIPT.<lang>.md`, README episode table.
5. The final message gives paths, the episode list, the coverage table, and plainly
   what was not done: content from your own knowledge, scenes not re-inspected, whether
   anyone listened to the voice.

## The model: beats

```python
self.say("Here is a sorted list of ten numbers, and we want to know whether twenty-three "
         "is in it. Checking them one by one could take ten comparisons.\n"   # \n: paragraph pause
         "But the list is sorted, and that lets us do much better.",
         Write(head), FadeIn(row))                       # plays as the beat starts
self.cue("Checking them one by one", Indicate(row))      # plays when the voice gets there
```

A beat is one `say()`: two to four connected sentences (8 to 25 s) about one picture,
voiced sentence by sentence with the pauses of `PACE`; the subtitle shows one sentence at
a time. The words are the baseline and always spoken in full; the animation adapts
(`run_time`, `hold()`, or a silent demonstration between two beats). Also `speak=` (other
words aloud, same sentence count), `clear_stage()`, `zoom_to()` / `zoom_back()` / `pin()`,
`title_card()`, `end_card([...])`. The docstring of `scripts/manim_kit.py` is the API
reference; `assets/example_episode.py` is a whole small episode.

## What the users asked for, as rules

- **A script that sounds spoken.** Sentences of 10 to 25 words, linked ("so", "which
  means", "now"), contractions, plain words. No colons, no numerals or symbols left to
  the voice, no slide fragments ("Why 12 bits?"), a sentence never split over two
  `say()` calls, no run of short beats. Notation goes on screen, the idea is said.
- **Derive, never announce.** Each sentence uses only what the previous one produced.
  Try, fail, try again, succeed, then name the pattern. No spoilers, no "this will
  matter later", no "we require". A concrete case before the rule; the overview last.
- **The picture makes the sentence true as it is said.** One `cue()` per thing named.
  Build and change objects, never bullet text. Transform the old picture into the new
  one. Every step of an argument is a line on screen; say which facts go unproven.
- **Show the small thing.** Move the camera to the crossing the argument rests on (a
  move, not a cut), or draw an inset. Pick example values the picture can tell apart.
- **Pace.** 130 to 150 words per minute including pauses. Pauses do the work, the rate
  a little. Never cut words to slow a video down.
- **Voice and speed are the user's taste.** `audition.py`, they choose, it goes into
  `TTS` in series.py, all before the first full render (a change redoes every clip).
- **One look.** One typeface (`TEXT_FONT = "latex"` when math-heavy), three font sizes,
  one colour and one spoken form per concept (GLOSSARY.md, `say_as.py`).
- **Review material is watchable.** Voiced, subtitles on the frame, one scene per clip,
  the exact path. Send the first one as soon as it exists.
- **Decide details yourself and list them**; ask only what the user alone can decide.
  Review notes become a written plan first (cause with file and line, fix, check), and
  new content goes into the script before any code.

## Workflow

1. **Material and choices.** Notes to Markdown. Languages (default English; for two,
   write the CJK one and translate through tables, which the kit can then prove
   complete). Shape: a series from notes (episodes of 4 to 8 min, one idea each) or one
   derivation (scenes of 1 to 3 min in `narration.md`; past 25 min, split into episodes
   that each end on the next one's question). For a derivation set
   `PACE = {"sentence": 0.75, "paragraph": 1.6, "beat": 1.8}`.
2. **Plan in writing**: `assets/plan_template.md` as PLAN.md with the coverage map,
   `series.py`, GLOSSARY.md. Commit and go on unless the user asked to approve it.
3. **Set up.** `scripts/setup_env.sh .venv` (`--latex`; Windows `setup_env.ps1`). Copy
   `manim_kit.py`, `tts.py`, `assets/series_template.py` → `series.py`,
   `assets/say_as_asm.py` → `say_as.py` into `<course>/<unit>/`: the project is
   self-contained. Ignore `media/`, `.tts_cache/`, `preview/`.
4. **Words, then pictures.** Write a scene's beats as prose, read them in order, then
   animate. Give each episode `SCENES = [...]` and `if self.preview_only(...): return`.
5. **Loop** per scene, then per episode, in every language:
   `check.py <unit> N [--scenes a b] [--lang xx]` → fix → open the sheets → fix.
   `captions.py <unit> N --spoken` shows what the voice will say; `preview.py` renders
   scenes in parallel into `<unit>/preview/` for the user.
6. **Review** coverage, the script read as a viewer, the translation. With many
   episodes: write the first two yourself, then one agent per episode from
   `assets/agent_brief_template.md`, three at a time, and a fresh reviewer per pair.
7. **Final render once**: `i18n_check.py <unit>`, then
   `render.py <unit> --out videos/<course>-<unit> --jobs 4`, `pace.py`,
   `srt_to_script.py`. Spot-check the 1080p output with a sheet and by ear.

## Read when

| File | Read it when |
|---|---|
| `references/narration-writing.md` | before the first script; when the lint or a listener objects |
| `references/derivation-episodes.md` | one long argument; "too rough / too fast / just states things"; acting on review notes |
| `references/visual-patterns.md` | layout budget, kit snippets (code, bits, plots, networks), camera, typeface |
| `references/bilingual-and-voice.md` | a second language; choosing an engine or voice; a mispronounced term |
| `references/production.md` | coverage map, parallel agents, delivery, publishing to YouTube |
| `references/pitfalls.md` | before the first render on a machine, and when something breaks |

Other scripts: `narration.py` + `bind_scene.py` (the script as an editable
`narration.md`), `narration_lint.py --audition` (clips of risky terms), `contact_sheet.py`.
