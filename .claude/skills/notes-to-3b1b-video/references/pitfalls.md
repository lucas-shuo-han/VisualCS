# Pitfalls (all hit for real while making the CS61C RISC-V series)

## Environment
- **System pip fails to build `srt`** ("AttributeError: install_layout") on
  Debian/Ubuntu. Use a virtualenv (`scripts/setup_env.sh` does).
- **Network-restricted sandboxes**: the course website may be blocked. Don't
  stall on it — work from files the user provides, from what you know about the
  topic, and say which parts were written from your own knowledge.
- **No neural TTS offline** (model hosts are often blocked). Ship burned-in
  captions + .srt; the user can add a voice-over later from the .srt/script.
- `Polyline` is not in every Manim version; build polylines with
  `VMobject().set_points_as_corners([...])`.

## Rendering
- **Parallel renders sharing one `--media_dir` crash** with
  `FileNotFoundError` on a temp SVG. `render.py` gives each episode its own
  media dir — keep it that way.
- **Editing a scene while its render is running** leaves you with a video of
  the old code. Stop and re-render after fixes; check file timestamps.
- 1080p30 of a 4-minute episode takes ~5–10 min on 4 cores and ends up
  ~8–12 MB. Always iterate at `--preview` (480p15) and render 1080p once.

## Captions / subtitles
- **The last caption only reaches the .srt when it is closed**: end every
  episode with `end_card(...)` or `self.uncaption()`.
- `say(text, *anims, run_time=x)` sets the run time of `anims`; don't pass
  `run_time` to anything else expecting it to apply to the caption.
- Captions are wrapped automatically, but keep each one ≤ ~2 lines (≈ 60
  English words is too many; ≈ 25–30 is comfortable).

## Text rendering
- **Pango drops or squeezes spaces in small `Text`** ("priority queue" →
  "priorityqueue", "x = 3" → "x=3"), worse below ~30 pt. The kit's `txt()`,
  `mono()`, captions, titles and `box_label()` all go through `crisp_text()`,
  which renders at 4× and scales down. Use those helpers; if you call
  `Text(...)` directly, do the same.
- **Don't oversample `MarkupText`**: Manim lays it out with a fixed Pango
  width, so a 4× font size wraps long lines. `CodeListing` keeps normal size
  (monospace spacing is fine).
- Some glyphs (e.g. "≥" in certain fonts) render oddly; if one looks wrong in
  the contact sheet, reword ("at least") or use `MathTex`.

## Layout
- **Text overlapping text** is the #1 bug. It happens when two blocks are
  placed with absolute coordinates and one of them is wider than you guessed
  (long code comments, CJK labels). Measure (`mob.width`) or anchor with
  `next_to`.
- A label placed with `next_to` *before* its target moved stays behind. Place
  labels after the final position, or group them with their target.
- `clear_stage()` right before the next `say()` means the "end" contact-sheet
  frame of that caption is empty — that is expected, check the `mid` sheet.
- Transforming a mobject that is inside a group: prefer in-place
  `Transform(old, new)` (keeps group membership) over `FadeOut`/`FadeIn` swaps
  that detach it.

## Content
- Compute every number shown (bits, hex, addresses, loss values) in Python and
  `assert` the key ones. Hand-typed values drift from the narration.
- Explain *why* a design is the way it is, not just *what* it is — that's the
  difference between a 3b1b-style video and an animated slide deck.
