# Pitfalls

(handled) = the kit already guards; listed so you recognise the symptom.

## Environment
- Use the venv (`setup_env.sh` / `.ps1`). Windows: `python` may be the Store stub, use the venv's; set `PYTHONIOENCODING=utf-8`; run `win_fonts.py` once per login.
- Windows LaTeX "does not support converting .dvi files to SVG": cwd or media on another drive. `check.py` handles it; for `render.py` set `MANIM_CWD` and `--media` on C: and `KIT_TTS_CACHE`.
- Blocked TTS host: Kokoro or `--no-voice`; don't stall.
- Shell heredocs and sed collapse `\\`: write LaTeX and regexes with the file tool.

## Rendering
- Never edit a file while it renders.
- Exit 255 with no traceback: rerun once.
- At most cores/2 renders in total. Iterate at 480p; 1080p once, after voice and speed are chosen.
- A lost voice track is invisible in frames (handled: `--disable_caching`; `check.py` compares audio and video).
- ffmpeg `subtitles=` can't take a drive colon: run from the `.srt` folder.
- Disk full → zero-size `.svg` and `ParseError`: free space, delete them.

## Subtitles
- The last subtitle lands only when closed: `end_card()` or `uncaption()`.
- `[cue] phrase not in the current line`: the beat was reworded, the cue was not.
- Narration as literals in `say()`, not lists iterated later.
- `clear_stage()` right before a `say()` makes its end frame empty: look at the mid sheet.

## Text and layout
- Use `txt()` / `mono()` / `num()` / `box_label()`; raw small `Text` loses its spaces.
- Missing glyphs (superscripts, combining accents) render as boxes: spell around them.
- Text over text: absolute coordinates plus wider-than-guessed text. Use `next_to`.
- A label placed before its target moves stays behind: group them.
- Growing objects cover heading or subtitles mid-animation: only mid sheets show it.
- In a group, `Transform` in place, not a FadeOut / FadeIn swap.

## Changing the kit
`Scene.time` doesn't advance inside an animation and updaters pause while their mobject animates: use a scene-level `dt` updater. Groups flatten when an animation starts: swap children by opacity. `FadeIn` re-applies its end state until its `play` ends. Fast-forwarded animations must still register their mobjects.
