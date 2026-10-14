# Kit (builder)

API reference: the docstring of `manim_kit.py`; a whole episode: `assets/example_episode.py`.

## Beats and timing
- `say(text, *anims)`: one beat; `anims` play as it starts, after the previous beat and its pause. `speak=` voices other words (same sentence count).
- `cue("phrase", *anims)`: plays when the voice reaches the phrase.
- Total `run_time` after a `say()` longer than the beat → next beat late; much shorter → frozen frame. Animation shorter than the words → `hold()`; longer → cut `run_time`. A silent demonstration goes between two beats.
- End each scene method with `self.hold()`.
- Shared objects on `self`. `SCENES = [...]` + `if self.preview_only([...]): return` lets later scenes render alone by fast-forwarding.

## Layout
- Labels `next_to` their object, after it is placed. After `scale()`, rebuild labels.
- Monospace at 26 ≈ 0.19 units per character.

## Snippets
```python
code = CodeListing(["while lo <= hi:", "    mid = (lo + hi) // 2"], lang="python", font_size=26).to_edge(LEFT)
box = code.line_box(0); self.play(box.animate.become(code.line_box(1)))
self.play(Circumscribe(code.glyphs(1, "mid")))
regs = reg_column([("lo", 0), ("hi", 9)]); self.play(regs[0].set(5))
row = bit_row("10110110", BLUE_B); self.play(set_bit_row(row, "00001111"))
bf = BitField([("sign", 1, RED_C), ("exponent", 8, GREEN_C), ("fraction", 23, BLUE_C)])
mem = MemoryView(0x100, rows=6, cols=4); self.play(mem.set_word(0x104, 42))
g, layers, edges = nn_diagram((3, 4, 2)); hm = heatmap([[0.9, .05], [.2, .7]])
```
- Compute a trace once, animate after; `assert` worked examples at the top of the file.
- LaTeX: split `MathTex` into parts to colour or `TransformMatchingTex`; plots with `Axes` + `ValueTracker` + `always_redraw`. Without LaTeX: no `MathTex`, `Matrix`, `DecimalNumber`. No `Polyline`: `VMobject().set_points_as_corners`.

## Camera
```python
self.cue("crosses the level", Flash(cross)); self.zoom_to(cross, width=4.5); self.hold(1); self.zoom_back()
```
`pin(mob)` keeps a mobject fixed on screen during camera moves (the subtitle is pinned already). Beyond ~3x: `ReplacementTransform(box, new_axes)` while the rest fades.

## Typeface
`TEXT_FONT = "latex"` in series.py: `txt()` prose and `num()` numbers share LaTeX; `mono()` only for code.

When something breaks: `pitfalls.md`.
