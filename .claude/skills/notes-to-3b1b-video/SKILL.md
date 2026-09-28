---
name: notes-to-3b1b-video
description: Turn course notes, lecture slides, textbook chapters or a study topic into a series of 3Blue1Brown-style animated explainer videos with Manim — dark background, animated diagrams, timed burned-in captions, .srt subtitles and a narration script. Use this whenever someone wants to visualize or animate a course (CS61C, CS182, CS189, linear algebra, algorithms, deep learning ...), make "3b1b-style" / Manim videos, turn notes or a PDF into explainer videos, or build a visual study series — even if they only say "make videos for this class", "animate these lecture notes" or "explain this topic visually".
---

# Notes → 3Blue1Brown-style video series

You will plan a short series, write one Manim scene per episode on top of the
bundled `manim_kit`, render it, *look at the frames*, fix what's wrong, and
ship MP4 + SRT + a narration script. The kit was extracted from a finished
7-episode CS61C RISC-V series; its components and the pitfalls list save most
of the trial and error.

## Bundled files

| Path | What it is |
|---|---|
| `scripts/manim_kit.py` | Component library: `NarratedScene` (timed captions + .srt), code listings with highlighting (asm/C/Python), registers, memory, bit fields, network diagram, heatmap, title/end cards. Read its module docstring first; skim sections as needed. |
| `scripts/setup_env.sh` | Installs ffmpeg/cairo/pango/fonts and Manim into a venv (`--latex` adds LaTeX for `MathTex`). |
| `scripts/render.py` | Renders every `class EpNN…` scene in a folder in parallel (separate media dirs), collects `mp4` + `srt`. `--preview` for 480p. |
| `scripts/contact_sheet.py` | One frame per caption tiled into PNG sheets, numbered by caption index. This is how you *see* your video. |
| `scripts/srt_to_script.py` | Collects all subtitles into a Markdown narration script. |
| `assets/example_episode.py` | A complete small episode (binary search) showing every core pattern. Read it before writing your first episode. |
| `references/visual-patterns.md` | Design principles, layout budget, and tested snippets for code, bits, math (equations, plots, matrices) and deep learning (networks, backprop, attention). |
| `references/pitfalls.md` | Every bug hit in production and how to avoid it. Read before rendering. |

## Workflow

### 1. Gather the material and decide the language
Find the notes: files the user gave you, a repo folder, a PDF, a course URL.
If the source is unreachable (blocked sites are common in sandboxes), don't
stall: work from what you know of the topic, and say clearly in the final
summary which parts came from the user's material and which from your own
knowledge.

Captions default to **English**. Use another language only if the user asks
(e.g. Chinese with English technical terms kept: "立即数 immediate"). Set
`lang = "zh"` on the scene class for Chinese title/end-card labels; the kit's
fonts cover CJK.

### 2. Plan the series (write it down before coding)
Split the material into 4–8 episodes of 3–4 minutes each, one coherent idea
per episode, ordered so each builds on the last. For each episode note:
the question it answers, one worked example with concrete numbers, the "aha"
beat (a surprise that the visuals resolve), and 4–5 recap bullets. Save this
as `PLAN.md` next to the code — it keeps a long series consistent and lets the
user redirect early.

### 3. Set up
```bash
bash <skill>/scripts/setup_env.sh .venv            # add --latex if you'll use MathTex/Matrix
mkdir -p <course>/<unit> && cp <skill>/scripts/manim_kit.py <course>/<unit>/
```
Copy (don't import from the skill dir) so the project is self-contained and
the user can tweak the kit per course. Commit the code; add `media/` to
`.gitignore`.

### 4. Write an episode
One file per episode, `epNN_short_name.py`, one `class EpNN...(NarratedScene)`:

```python
class Ep03Backprop(NarratedScene):
    series = "CS182 · Deep Learning"
    def construct(self):
        self.title_card(3, "Backpropagation", "the chain rule, run backwards")
        self.section_one()
        self.section_two()
        self.end_card(["...", "..."], next_title="...")   # also flushes the last caption
```

The core loop inside a section is `self.say(caption, *animations)`: it waits
until the previous caption has been readable, swaps the caption, and plays the
animations with it. Follow with more `self.play(...)` calls as needed, and
`self.hold()` for a beat. Use `self.heading()` for section titles and
`self.clear_stage()` between sections. See `assets/example_episode.py`.

Guidelines that made the difference in quality (details and snippets in
`references/visual-patterns.md`):
- One idea per caption; the animation should make that sentence true.
- Build and manipulate objects instead of showing bullet text.
- Compute every number with Python (trace functions, `assert`s) — never type
  results by hand.
- Keep one color per concept across the series.
- Keep content above y = −2.9 (the caption band) and anchor labels with `next_to`.

### 5. Preview → look → fix (the step that matters most)
```bash
.venv/bin/python <skill>/scripts/render.py <course>/<unit> --preview --only 3 --manim .venv/bin/manim --media <scratch>/media
.venv/bin/python <skill>/scripts/contact_sheet.py <mp4> <srt> <scratch>/sheets --at end   # settled states
.venv/bin/python <skill>/scripts/contact_sheet.py <mp4> <srt> <scratch>/sheets_mid --at mid  # mid-animation
```
Open every `sheet*.png` and check: text overlapping text or boxes, anything
off-frame or under the caption band, labels left behind after a move, captions
wrapping to 3+ lines, empty frames, numbers that don't match the narration.
The frame number is the caption index, so it maps straight back to a
`say()` call. Fix, re-render the preview, look again. Budget two or three
rounds per episode; most first drafts have 2–5 layout collisions.

Render episodes in parallel (`--jobs`), but never edit a file whose render is
still running (see `references/pitfalls.md`).

### 6. Final render and delivery
```bash
.venv/bin/python <skill>/scripts/render.py <course>/<unit> --out videos/<course>-<unit> --manim .venv/bin/manim
.venv/bin/python <skill>/scripts/srt_to_script.py videos/<course>-<unit> <course>/<unit>/SCRIPT.md --title "..."
```
Spot-check the 1080p output with one more contact sheet, then commit videos
(~8–12 MB per 4-minute episode), subtitles, script and code. Write or update
a README with an episode table (title + what it covers) and how to re-render.

In the final message, tell the user where the videos are, list the episodes,
and state limitations plainly (no voice-over; which content came from your own
knowledge; anything you couldn't verify).
