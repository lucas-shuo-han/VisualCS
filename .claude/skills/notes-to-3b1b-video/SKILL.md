---
name: notes-to-3b1b-video
description: Turn course notes, lecture slides, textbook chapters or a study topic into a series of 3Blue1Brown-style animated explainer videos with Manim — dark background, animated diagrams, timed burned-in captions, .srt subtitles, an optional neural voice-over, and optionally the same series in a second language. Use this whenever someone wants to visualize or animate a course (CS61C, CS182, CS189, linear algebra, algorithms, deep learning ...), make "3b1b-style" / Manim videos, turn notes or a PDF into explainer videos, add narration or a translated version to such videos, or build a visual study series — even if they only say "make videos for this class", "animate these lecture notes" or "explain this topic visually".
---

# Notes → 3Blue1Brown-style video series

You will map the notes, plan a series, write one Manim scene per episode on top of the
bundled `manim_kit`, render, *look at the frames*, fix, review the writing, and ship
MP4 + SRT + narration scripts — in one or two languages, silent or voiced. The kit and
the references come from a finished 14-episode Chinese/English voiced CS61C RISC-V
series; they save most of the trial and error.

## Bundled files

| Path | What it is |
|---|---|
| `scripts/manim_kit.py` | Component library: `NarratedScene` (timed captions + .srt, voice-over, title/end cards), translation layer, code listings (asm/C/Python), registers, memory, bit fields, network diagram, heatmap. Read its docstring first. |
| `scripts/tts.py` | Voice-over: caption → spoken form → edge-tts neural voice, cached. Copied next to the kit. |
| `scripts/render.py` | Renders a unit's episodes × languages in parallel, collects `mp4` + `srt`. `--preview` 480p, `--voice`, `--lang`. |
| `scripts/contact_sheet.py` | One frame per caption tiled into numbered PNG sheets. This is how you *see* the video. |
| `scripts/captions.py` | Dumps an episode's narration in order, all languages side by side, `--spoken` shows what the voice will say. For proofreading without rendering. |
| `scripts/i18n_check.py` | Checks the translation tables are complete (`--skeleton`, `--widths`). |
| `scripts/srt_to_script.py` | Collects subtitles into a Markdown narration script. |
| `scripts/setup_env.sh` / `setup_env.ps1` / `win_fonts.py` | Environment for Linux/macOS / Windows (fonts included). |
| `scripts/project.py` | Helpers the scripts share (unit folder, series.py, tables). |
| `assets/example_episode.py` | A complete small episode (binary search) showing the core patterns. Read it before your first episode. |
| `assets/series_template.py` | `series.py`: episode order, titles per language, source language. |
| `assets/say_as_asm.py` | Example `say_as.py` pronunciations (assembly course). |
| `assets/agent_brief_template.md` | Brief for per-episode agents when working in parallel. |
| `references/visual-patterns.md` | Design principles, layout budget, snippets for code, bits, math, deep learning. |
| `references/production.md` | Coverage map, planning, parallel agents, the review pass, keeping the user in the loop, delivery. |
| `references/bilingual-and-voice.md` | Translation tables, layout across languages, voice-over, pronunciation, timing. |
| `references/pitfalls.md` | Every bug hit in production (incl. Windows) and how to avoid it. Read before rendering. |

## Workflow

### 1. Gather the material, decide languages and voice
Find the notes (files, a repo folder, a PDF, a course URL) and convert each chapter to
clean Markdown in a scratch folder. If the source is unreachable, don't stall: work from
what you know and say in the final summary which parts came from where.

Decide from the request (ask only if it is truly ambiguous):
- **Languages.** Default: English captions. For two languages, write the episodes in one
  (prefer the CJK one: the kit can then prove the translation complete) and translate
  through tables — see `references/bilingual-and-voice.md`.
- **Voice-over.** On by default for final renders when the network allows edge-tts;
  captions stay burned in either way.
- **Coverage.** "Make videos for these notes" means cover them: build the coverage
  checklist now (`references/production.md` §1).

### 2. Plan the series (written down before coding)
Episodes of one coherent idea each, ordered so each builds on the last: 3–4 min for a
single idea, 6–8 min when covering a chapter fully; split anything longer. For each
episode: the question it answers, a worked example with concrete numbers, the "aha"
beat, the notes items it covers, 4–5 recap bullets. Save `PLAN.md`, `series.py` (from
`assets/series_template.py`) and a `GLOSSARY.md` of terms. Commit and continue without
waiting unless the user asked to approve the plan.

### 3. Set up
```bash
bash <skill>/scripts/setup_env.sh .venv       # add --latex for MathTex/Matrix; Windows: setup_env.ps1
mkdir -p <course>/<unit>
cp <skill>/scripts/manim_kit.py <skill>/scripts/tts.py <course>/<unit>/
cp <skill>/assets/series_template.py <course>/<unit>/series.py     # then edit
cp <skill>/assets/say_as_asm.py <course>/<unit>/say_as.py          # optional; adapt to the course
```
Copy (don't import from the skill dir) so the project is self-contained and the kit can
be tweaked per course. Add `media/` and `.tts_cache/` to `.gitignore`.

### 4. Write an episode
One file per episode, `epNN_short_name.py`, one `class EpNN...(NarratedScene)` whose
name matches series.py:

```python
class Ep02Backprop(NarratedScene):
    def construct(self):
        self.title_card()                 # number, title, subtitle from series.py (spoken)
        self.chain_rule()
        self.worked_example()
        self.end_card(["...", "..."])     # recap; "next episode" / "the end" automatic
```

The core loop is `self.say(caption, *animations)`: it waits until the previous caption
has been read (and spoken), swaps the caption, starts its voice-over and plays the
animations with it. Then more `self.play(...)`, `self.hold()` for a beat,
`self.heading()` for section titles, `self.clear_stage()` between sections. Without
series.py, pass `title_card(n, "Title", "subtitle")` and `end_card(bullets, next_title=...)`.

What made the difference in quality (details in `references/visual-patterns.md`):
- One idea per caption; the animation makes that sentence true. The caption *is* the
  narration: it must explain what is on screen at that moment.
- Build and manipulate objects instead of showing bullet text.
- Compute every number with Python and `assert` the key ones — never type results by
  hand. Recompute the notes' examples too: notes contain errors.
- One color per concept across the series; one term per concept (GLOSSARY.md).
- Keep content above y ≈ −2.5 (the caption band) and anchor labels with `next_to`.
- Captions are read aloud: avoid symbol soup; check with `captions.py --spoken`.

With many episodes, write the first one or two yourself (they set the house style),
then hand episodes to parallel agents with the brief — `references/production.md` §3.

### 5. Preview → look → fix (the step that matters most)
```bash
python <skill>/scripts/render.py <unit> 3 --preview [--lang en] [--voice] --media <scratch>/media
python <skill>/scripts/contact_sheet.py <mp4> <srt> <scratch>/sheets --at end   # settled states
python <skill>/scripts/contact_sheet.py <mp4> <srt> <scratch>/sheets_mid --at mid  # mid-animation
```
Open every `sheet*.png` and check: text overlapping text or boxes, anything off-frame or
under the caption band, labels left behind after a move, captions wrapping badly,
empty frames, numbers that don't match the narration. The frame number is the caption
index. Fix, re-render, look again: budget two or three rounds per episode, and look at
**every language** (translations break layouts). Never edit a file whose render is
still running.

### 6. Review the writing and the coverage
Per episode, after it renders cleanly: coverage against the checklist, the source
captions read in order as a viewer, the translation, the spoken form
(`captions.py <unit> N --spoken`). Checklist in `references/production.md` §4. A fresh
reviewer agent per two episodes catches what authors miss.

### 7. Final render and delivery
```bash
python <skill>/scripts/i18n_check.py <unit>                    # bilingual: must be ok
python <skill>/scripts/render.py <unit> --out videos/<course>-<unit> --jobs 4   # all languages, voiced
python <skill>/scripts/srt_to_script.py videos/<course>-<unit>/<lang> <unit>/SCRIPT.<lang>.md --title "..."
```
Spot-check the 1080p output (a contact sheet; play one with sound), then commit code,
tables, videos, subtitles and scripts, and write or update a README with an episode
table and how to re-render. Delivery checklist: `references/production.md` §6.

Show progress early: send the first finished episode's preview as soon as it exists,
and when the user wants "something to watch now", render voiced 480p previews in one
language and send each as it finishes (§5 of production.md).

In the final message, tell the user where the videos are, list the episodes, point to
the coverage table, and state limitations plainly (content from your own knowledge,
notes errors found, anything unverified).
