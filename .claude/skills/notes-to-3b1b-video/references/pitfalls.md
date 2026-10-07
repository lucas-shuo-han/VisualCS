# Pitfalls

Each one cost a render or a review round. The kit and scripts already guard against
those marked (handled); they are listed so you recognise the symptom.

## Environment

- Debian/Ubuntu system pip fails to build `srt`: use the virtualenv (`setup_env.sh`).
- **Windows.** `setup_env.ps1`; no ffmpeg or system packages needed. `python` may be
  the Store stub, which hangs: use `py -3` or the venv's `python.exe`. Set
  `$env:PYTHONIOENCODING="utf-8"` or printing CJK crashes. Fonts installed per user are
  invisible to Pango until the next login: run `win_fonts.py` once per login (the
  per-process fallback makes text about 100 times slower).
- **LaTeX on Windows: "does not support converting .dvi files to SVG"** when the
  working directory or the media directory is on another drive than MiKTeX. `check.py`
  and `preview.py` work from the temp folder (handled). For `render.py` set `MANIM_CWD`
  and `--media` to a folder on the system drive and `KIT_TTS_CACHE` to the project's
  cache, so no clip is synthesized twice.
- A blocked course website or TTS host: do not stall. Work from the user's files and
  your knowledge and say which is which; fall back to Kokoro or `--no-voice`.
- **The shell collapses `\\` to `\`** in heredocs and `sed`: `"\\t"` became a tab
  inside a Python string, `\b` a backspace. Write anything with LaTeX or regexes with
  the file-writing tool.

## Rendering

- Never edit a file whose render is running: the video shows the old code.
- Renders sharing one `--media_dir` crash on a temp SVG (handled: one per job).
- A render can die with exit code 255 and no traceback: run it once more before debugging.
- Several agents rendering plus a batch render slow each other down: about cores / 2
  renders in total.
- 1080p30 of a voiced 7-minute episode takes 10 to 20 min on 4 cores. Iterate at 480p,
  render 1080p once, and not before voice and speed are chosen: two long renders were
  thrown away for that.
- **A lost voice track is invisible in frames.** On a cache hit Manim's clock does not
  advance and later voice lines land early or vanish (handled: `--disable_caching`).
  `check.py` compares audio with video and looks for long silences.
- ffmpeg's `subtitles=` filter cannot take a path with a drive colon: run it from the
  folder of the `.srt` with the bare file name.

## Subtitles

- The last subtitle reaches the `.srt` only when closed: end with `end_card(...)` or
  `self.uncaption()`.
- `[cue] phrase not in the current line`: the beat was reworded and the cue was not.
  The animation then plays at once.
- `say(text, *anims, run_time=x)` sets the run time of `anims`.
- Keep narration as literals inside `say()`: a list of strings iterated later shows up
  in `captions.py` and the lint as source code.
- `clear_stage()` right before the next `say()` makes that subtitle's "end" frame
  empty: expected, look at the "mid" sheet.

## Text

- Use `txt()`, `mono()`, `num()`, `box_label()`. Raw small `Text` loses its spaces
  ("priorityqueue"); the helpers render at 4x and scale down. `MarkupText` must not be
  oversampled (it wraps).
- Glyphs a font lacks render as boxes or split: superscript digits in Noto CJK,
  combining accents ("Asanović"). Spell around them. An odd "≥": reword or use `MathTex`.
- CJK fonts draw curly quotes full-width (handled in Latin renders).

## Layout

- Text over text is the most common bug: two blocks at absolute coordinates, one wider
  than guessed (long code comments, the English translation). Measure or use `next_to`.
- A label placed before its target moved stays behind. Group it with the target.
- A growing object can cover the heading or the subtitle band mid-animation: only the
  "mid" sheet shows it.
- Inside a group prefer `Transform(old, new)` in place to a `FadeOut` / `FadeIn` swap,
  which detaches the member.

## Content

- Hand-typed values drift from the narration: compute and `assert`.
- Explain why a design is the way it is, not only what it is. That is the difference
  between this and an animated slide deck.

## If you change the kit

These bit while building the subtitle reel and the scene previews: `Scene.time` does
not advance inside an animation and a mobject's updaters are suspended while it
animates, so anything that follows the clock counts `dt` in a scene-level updater.
Manim flattens a group's family when an animation starts, so swap children by opacity,
not by membership. A `FadeIn` keeps re-applying its end state until its `play` is over.
A fast-forwarded animation must still register its mobjects
(`add_mobjects_from_animations`). Parts of a sentence cut at commas share the
sentence's span computed once, not from a moving start.
