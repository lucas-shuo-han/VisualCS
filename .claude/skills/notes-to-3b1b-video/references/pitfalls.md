# Pitfalls (all hit for real while making the CS61C RISC-V series)

## Environment
- **System pip fails to build `srt`** ("AttributeError: install_layout") on
  Debian/Ubuntu. Use a virtualenv (`scripts/setup_env.sh` does).
- **Windows**: use `setup_env.ps1`. Manim's wheels bundle cairo/pango and decode media
  with PyAV, so no system packages or ffmpeg are needed; the scripts avoid ffmpeg too.
  - `python` can be the Microsoft Store stub, which hangs: use `py -3` or the venv's
    `python.exe` by full path.
  - Set `$env:PYTHONIOENCODING="utf-8"`, or printing CJK to the console (gbk) crashes.
  - Fonts installed per user are invisible to Pango until the next login; run
    `win_fonts.py` once per login (the kit's per-process fallback works but makes text
    ~100× slower).
  - `.venv\Scripts\manim.exe`, not `.venv/bin/manim`; `find_manim()` picks either.
- **Network-restricted sandboxes**: the course website may be blocked. Don't stall;
  work from the user's files and your knowledge, and say which is which.
- **edge-tts needs network** (Microsoft's service; no key). It is occasionally flaky:
  `tts.synth` retries 5 times. Offline: render with `--no-voice`.
- `Polyline` is not in every Manim version; build polylines with
  `VMobject().set_points_as_corners([...])`.
- No LaTeX installed means no `Tex`, `MathTex`, `Matrix`, `DecimalNumber`, `Integer`
  (they all compile TeX). Say so in agent briefs, or agents will reach for them.

## Rendering
- **Parallel renders sharing one `--media_dir` crash** with `FileNotFoundError` on a
  temp SVG. `render.py` gives each (episode, language) its own media dir.
- **Editing a scene while its render is running** leaves you with a video of the old
  code. Re-render after fixes; check file timestamps.
- **CPU contention**: several agents each rendering, plus a batch render, all slow
  down together. Budget ~cores / 2 concurrent renders in total.
- A render can die without a traceback (exit code 255 and a truncated log). Re-run it
  once before debugging.
- 1080p30 of a 7-minute voiced episode takes 10–20 min on 4 cores and ends up
  ~15–20 MB. Always iterate at `--preview` (480p15) and render 1080p once.

- **dvisvgm fails when the working directory is on another drive** (Windows, project on D:, MiKTeX on C:): "does not support converting .dvi files to SVG", exit 127. Run Manim with `cwd` in a folder on the system drive and pass the episode by absolute path (preview.py does).
- **ffmpeg's `subtitles=` filter cannot take a path with a drive colon.** Run ffmpeg with `cwd` in the folder of the .srt and give the bare file name.
- **A fast-forwarded animation must still register its mobjects.** Jumping an animation to its end without `scene.add_mobjects_from_animations` leaves faded-out objects on stage (`fast_forward` in the kit does this).

## Captions / subtitles
- **The last caption only reaches the .srt when it is closed**: end every episode with
  `end_card(...)` or `self.uncaption()`.
- `say(text, *anims, run_time=x)` sets the run time of `anims`.
- A beat can be several sentences; the subtitle shows one at a time (two lines at
  most). A sentence over ~30 English words / ~60 CJK characters is shown in parts cut
  at commas: rewrite it as two sentences instead.
- **`cue()` phrase not found** prints `[cue] phrase not in the current line` and plays
  the animation at once. It means the beat was reworded and the cue was not.
- **`Scene.time` does not advance inside an animation, and a mobject's updaters are
  suspended while it animates.** Anything that must follow the clock during a `play`
  (the subtitle reel) has to count `dt` in a scene-level updater.
- **Manim flattens a group's family when an animation starts.** Swapping a group's
  children during a `play` leaves the old children drawn. Keep all children and toggle
  their opacity instead (the subtitle reel does).
- **A `FadeIn(caption)` keeps re-applying its end state until the play it belongs to is
  over.** A sentence switch that happens inside that first play (the first sentence of a
  beat is shorter than the animation that starts it) was undone on the next frame: the
  reel showed sentence 1 for seconds, skipped sentences 2 and 3, and left a ghost of 1
  under later ones. The reel's updater now says the current state again each frame
  after the first 0.45 s; check the `mid` contact sheet of a beat whose first sentence
  is short and whose first `play` is long.
- The wrapper never breaks inside an English word or an arrow route, but it can split a
  CJK word (洛/杉矶). Read the contact sheets; reword or shorten when it happens.
- `captions.py` finds captions by walking `construct()` and the `self.<method>()` calls
  it makes. A caption built far away from `say()` (a list of strings iterated later)
  shows up as source code, not text; keep caption literals inside `say()` calls.

## Text rendering
- **Pango drops or squeezes spaces in small `Text`** ("priority queue" →
  "priorityqueue"), worse below ~26 pt. The kit's `txt()`, `mono()`, captions, titles
  and `box_label()` go through `crisp_text()`, which renders at 4× and scales down. Use
  those helpers; if you call `Text(...)` directly, do the same.
- **Don't oversample `MarkupText`**: Manim lays it out with a fixed Pango width, so a
  4× font size wraps long lines. `CodeListing` keeps normal size.
- **CJK fonts draw curly quotes full-width**, which gapes in English; the kit
  straightens them in Latin-script renders.
- Glyphs the font lacks render as boxes or split: superscript digits (²) in Noto CJK;
  combining accents ("Asanović" → the accent lands after the letter). Spell around
  them ("2^32" as a separate small `mono`, "Asanovic").
- Some glyphs ("≥" in certain fonts) render oddly; reword ("at least") or use `MathTex`.

## Layout
- **Text overlapping text** is the #1 bug. It happens when two blocks are placed with
  absolute coordinates and one is wider than you guessed (long code comments, CJK
  labels, the English translation). Measure (`mob.width`) or anchor with `next_to`.
- A label placed with `next_to` *before* its target moved stays behind. Place labels
  after the final position, or group them with their target.
- A growing object (zoom-out, stacked bars) can cover the caption band or heading
  mid-animation: the `mid` contact sheet catches it; clip or scale it.
- `clear_stage()` right before the next `say()` means the "end" contact-sheet frame of
  that caption is empty — expected; check the `mid` sheet.
- Transforming a mobject inside a group: prefer in-place `Transform(old, new)` (keeps
  group membership) over `FadeOut`/`FadeIn` swaps that detach it.

- **A panel next to a graph collides with what stays all episode** (a corner formula, the previous scene's tag). Place panel lines from one anchor going down, and check the frame where the panel is fullest.
- **Labels at the start point of a path hide axis labels** (a start marked "2.2" on top of √5). Use a plain dot and put the number in the side panel; put a level line's label at its far end, away from the diagonal.

## Content
- Compute every number shown (bits, hex, addresses, loss values) in Python and
  `assert` the key ones. Hand-typed values drift from the narration.
- The notes can be wrong: recompute their examples; show the correct version and
  report the discrepancy.
- Explain *why* a design is the way it is, not just *what* it is — that's the
  difference between a 3b1b-style video and an animated slide deck.

## Voice-over and Manim's cache
- Render voiced videos with `--disable_caching` (render.py and preview.py do). On a cache hit Manim plays the cached clip without advancing its clock, so `add_sound` places later lines too early or drops them: a re-render comes out with missing or shifted voice while the picture looks right.
- After every voiced render compare audio and video duration (`ffprobe`) and look for long silences (`ffmpeg -af silencedetect`). Frames alone do not show a lost voice track.

## Regexes on mixed text
- Python's `\b` and `\w` count CJK characters as word characters, so `\bx5\b` never
  matches in "寄存器x5里". Use `flags=re.ASCII` for anything that runs on CJK text.
- Shell heredocs mangle backslashes (`\b` became a backspace character): edit Python
  source with a file-editing tool, not `sed`/heredocs, when it contains regexes.
