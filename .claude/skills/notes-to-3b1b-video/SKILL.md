---
name: notes-to-3b1b-video
description: Turn course notes, lecture slides, textbook chapters, a derivation or a study topic into 3Blue1Brown-style animated explainer videos with Manim — dark background, animated diagrams, a neural voice-over whose words drive the animation, sentence-by-sentence subtitles (.srt and on the frame), and optionally the same series in a second language. Use this whenever someone wants to visualize or animate a course (CS61C, CS182, CS189, linear algebra, algorithms, deep learning ...), make "3b1b-style" / Manim videos, turn notes or a PDF into explainer videos, walk through one long proof or derivation as a video, add narration or a translated version to such videos, fix a video that is "too rough", "too fast" or "sounds robotic", or build a visual study series — even if they only say "make videos for this class", "animate these lecture notes" or "explain this topic visually".
---

# Notes → 3Blue1Brown-style videos

You will map the material, plan, write the narration, write one Manim scene per episode
on the bundled `manim_kit`, render, *look at the frames and listen*, fix, and ship
MP4 + SRT + scripts. The kit and references come from two finished projects: a
14-episode Chinese/English CS61C RISC-V series (covering a course's notes) and a
35-minute CS182 Newton–Schulz derivation polished over several rounds of user review.

## What this skill adds, and what it borrows

Other Manim skills cover the animation API and the planning habit well; none covers
what viewers actually complained about here. The work that is this skill's own:

1. **A script that sounds spoken**, and animation timed to its words.
2. **Pronunciation** of variables, symbols, mnemonics and acronyms.
3. **Coverage**: every item of the notes mapped to an episode, or omitted on purpose.
4. **Two languages** from one source, with proof that nothing is left untranslated.
5. **Looking and listening** as the acceptance test, not "it rendered".

Borrowed, and worth using when installed: general Manim CE practice (e.g.
adithya-s-k's `manimce-best-practices`), the 3b1b teaching order (intuition before
formalism, why before what, concrete before abstract, show don't tell), and
manim-voiceover's idea of landing an animation on a word (here: `cue()`).

## The model: beats

A **beat** is a few connected sentences of narration with the picture they explain.

```python
self.say("Here is a sorted list of ten numbers, and we want to know whether twenty-three "
         "is in it. Checking them one by one could take ten comparisons. "
         "But the list is sorted, and that lets us do much better.",
         Write(head), FadeIn(row))                       # starts with the beat
self.cue("Checking them one by one", Indicate(row))      # when the voice reaches these words
```

- `say(text, *anims)` speaks the whole beat as **one** voice clip (natural intonation
  across sentences) and plays `anims` as it starts. It first waits for the previous
  beat to finish.
- `cue("phrase from the beat", *anims)` plays the next step when the voice reaches that
  phrase. One cue per thing the sentences mention. The words are the baseline and are
  always spoken in full; the animation adapts (shorten `run_time`, or play a pure
  demonstration silently between two beats).
- Subtitles show **one sentence at a time**, on the frame and in the `.srt`, switching as
  the voice reaches each. So a beat may be long; a subtitle never is.
- `speak="..."` voices different words from the subtitle (notation on screen, plain
  words aloud). `hold()` waits for the voice; `clear_stage()` changes section.

Never split one sentence across two `say()` calls, and never write a run of 5-word
beats: each `say()` is a separate clip, so both sound broken.

## Bundled files

| Path | What it is |
|---|---|
| `scripts/manim_kit.py` | Component library: `NarratedScene` (`say`, `cue`, `hold`, sentence subtitles, voice, title/end cards, `fast_forward`), translation layer, code listings, registers, memory, bit fields, network diagram, heatmap. Read its docstring first. |
| `scripts/tts.py` | Beat → spoken form → neural voice (edge-tts, or offline Kokoro), cached. `math_letters`, Greek, operators, hex. |
| `scripts/render.py` | Episodes × languages in parallel → `mp4` + `srt`. `--preview` 480p, `--voice`, `--lang`. |
| `scripts/preview.py` | Single scenes of one episode in parallel, voiced, subtitles on the frame: the fast loop for a long episode. |
| `scripts/contact_sheet.py` | One frame per subtitle, tiled into numbered sheets. This is how you *see* the video. |
| `scripts/narration_lint.py` | Lints the script: split sentences, choppy runs, over-long sentences, colons, numerals, terms the voice will misread; `--audition` synthesizes those terms. |
| `scripts/captions.py` | Dumps the narration in order, languages side by side; `--spoken` shows what the voice will say. |
| `scripts/narration.py`, `bind_scene.py` | Optional: keep the script in an editable `narration.md` the user can revise; bind final wording back into the code and check every `cue()` phrase. |
| `scripts/i18n_check.py` | Translation tables complete? (`--skeleton`, `--widths`) |
| `scripts/srt_to_script.py` | Subtitles → Markdown narration script. |
| `scripts/setup_env.sh` / `setup_env.ps1` / `win_fonts.py` | Environment for Linux/macOS / Windows. |
| `assets/example_episode.py` | A complete small episode using beats and cues. Read it before your first episode. |
| `assets/plan_template.md` | PLAN.md: series table, per-episode scene plan, coverage map. |
| `assets/series_template.py`, `say_as_asm.py`, `agent_brief_template.md` | `series.py`; example pronunciations; brief for per-episode agents. |
| `references/narration-writing.md` | How to write the script. **Read before writing any narration.** |
| `references/visual-patterns.md` | Design principles, layout budget, snippets for code, bits, math, deep learning. |
| `references/production.md` | Coverage map, planning, parallel agents, review pass, user loop, delivery. |
| `references/derivation-episodes.md` | One long argument as an episode; polishing a rough video with the user; the editable script; scene-by-scene preview. |
| `references/bilingual-and-voice.md` | Translation tables, layout across languages, engines, pronunciation, timing. |
| `references/pitfalls.md` | Every bug hit in production. **Read before rendering.** |

## Which shape is the job?

| | **Series from notes** | **One long derivation** / **polish a rough video** |
|---|---|---|
| Typical ask | "make videos for these notes / this class" | "derive X step by step", "this video is too rough" |
| Unit of work | episode, 4–8 min, one idea each | scene, 1–3 min, inside one long episode |
| Script lives in | the episode code (`say()` literals) | `narration.md`, bound into the code when final |
| Fast loop | `render.py N --preview --voice` | `preview.py <scene>` |
| Extra reading | `production.md` | `derivation-episodes.md` |

Everything else (beats, voice, lint, frames, delivery) is the same.

## Workflow

### 1. Gather the material; decide languages and voice
Convert the notes (files, PDF, course URL) to clean Markdown in a scratch folder. If a
source is unreachable, work from what you know and say so in the final report.
Decide from the request, asking only if truly ambiguous:
- **Languages.** Default English. For two, write in one (prefer the CJK one: the kit can
  then prove the translation complete) and translate through tables.
- **Voice.** On for everything the user will review and for final renders: edge-tts when
  its host is reachable, else offline Kokoro (`KIT_TTS_ENGINE=kokoro`).
- **Subtitles on the frame.** On by default; `BURN_CAPTIONS = False` in series.py for a
  clean frame with the `.srt` beside it.
- **Coverage.** "Make videos for these notes" means cover them: build the checklist now
  (`production.md` §1).

### 2. Plan, in writing
Fill `assets/plan_template.md` as `PLAN.md`: per episode the question it answers, the
worked example with real numbers, the "aha", and a scene list (picture, what the
narration must get across, notes items covered). Order ideas the 3b1b way: a concrete
case before the rule, the reason before the definition. Also `series.py` and a
`GLOSSARY.md` (one term and one colour per concept). Commit and continue without
waiting unless the user asked to approve the plan.

### 3. Set up
```bash
bash <skill>/scripts/setup_env.sh .venv       # --latex for MathTex; Windows: setup_env.ps1
mkdir -p <course>/<unit>
cp <skill>/scripts/manim_kit.py <skill>/scripts/tts.py <course>/<unit>/
cp <skill>/assets/series_template.py <course>/<unit>/series.py     # then edit
cp <skill>/assets/say_as_asm.py <course>/<unit>/say_as.py          # adapt to the course
```
Copy, don't import from the skill, so the project is self-contained. Add `media/`,
`.tts_cache/` and `preview/` to `.gitignore`.

### 4. Write the narration, then the scene
Read `references/narration-writing.md` first. Write each scene's beats as prose, read
them aloud in order, and only then animate them:

```python
class Ep02Backprop(NarratedScene):
    SCENES = ["chain_rule", "worked_example"]       # lets preview.py render one alone
    def construct(self):
        self.title_card()                           # from series.py, spoken
        self.chain_rule()
        self.worked_example()
        self.end_card(["...", "..."])               # recap; "next episode" automatic
```

What made the difference in quality:
- The picture makes the sentence true at the moment it is said: one `cue()` per thing
  mentioned. A 20-second beat with one animation is a frozen frame.
- Build and change objects; don't show bullet text.
- Compute every number in Python and `assert` the key ones, including the notes' own
  examples (notes contain errors).
- Derive, don't announce: each sentence uses only what the previous one produced.
- Keep content above y ≈ −2.9 (the subtitle band) and anchor labels with `next_to`.

With many episodes, write the first one or two yourself, then hand the rest to parallel
agents with the brief (`production.md` §3; three at a time).

### 5. Lint → preview → look and listen → fix
```bash
python <skill>/scripts/narration_lint.py <unit> 3 [--audition <scratch>/audition]
python <skill>/scripts/render.py <unit> 3 --preview --voice --media <scratch>/media
python <skill>/scripts/preview.py 4 5 --unit <unit> --ep 3        # or: single scenes
python <skill>/scripts/contact_sheet.py <mp4> <srt> <scratch>/sheets --at end
python <skill>/scripts/contact_sheet.py <mp4> <srt> <scratch>/sheets_mid --at mid
```
- **Lint first**: fix every `split`, `choppy`, `long` and `colon`; settle each flagged
  term in `say_as.py` by listening to its audition clip.
- **Open every sheet**: overlapping text, anything off-frame or under the subtitles,
  labels left behind, empty frames, numbers that disagree with the narration. Two or
  three rounds per episode, in **every language**.
- **Listen** to one voiced preview per language start to end. Reading the spoken text
  does not catch prosody or a mispronounced term.
- After each voiced render check that audio and video durations match (a lost voice
  track is invisible in frames; `pitfalls.md`).
- Never edit a file whose render is still running.

Send the user the first voiced preview as soon as it exists, with its exact path.

### 6. Review the writing and the coverage
Per episode: coverage against the checklist, the narration read in order as a viewer,
the translation, the lint, the spoken form (`captions.py <unit> N --spoken`). Checklist
in `production.md` §4. A fresh reviewer agent per two episodes catches what authors miss.

### 7. Final render and delivery
```bash
python <skill>/scripts/i18n_check.py <unit>                    # bilingual: must be ok
python <skill>/scripts/render.py <unit> --out videos/<course>-<unit> --jobs 4
python <skill>/scripts/srt_to_script.py videos/<course>-<unit>/<lang> <unit>/SCRIPT.<lang>.md --title "..."
```
Spot-check the 1080p output (a contact sheet; play one with sound), commit code, tables,
videos, subtitles and scripts, and update the README with an episode table and how to
re-render (`production.md` §6).

In the final message say where the videos are, list the episodes, point to the coverage
table, and state limitations plainly: content from your own knowledge, notes errors
found, which scenes you did not re-inspect, whether you listened to the voice.
