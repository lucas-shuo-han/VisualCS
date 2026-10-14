# Visuals

## Principles
- One picture per beat, one change per thing said.
- Build objects and change them; on-screen text only labels (≤ 4 words).
- Transform old into new (`ReplacementTransform`, `TransformFromCopy`, `.animate`); don't fade out and restart.
- One colour per concept across the series.

## Layout
Frame x ∈ [−7.1, 7.1], y ∈ [−4, 4]. Heading y ≈ 3.5; content y −2.9…3.3, x ±6.8; subtitle band below −2.9.
- Labels `next_to` their object, after it is placed. Two side-by-side blocks ≤ 6.3 wide each. Monospace 26 ≈ 0.19 per character.
- After `scale()`, rebuild labels. Check the fullest frame against whatever stays all episode.
- The kit reports text overlap and off-frame as `[layout]`; text over shapes only the sheets show.

## Timing
`say()` starts after the previous beat; its anims, `cue()`s and `play()`s run while it is spoken. Total `run_time` longer than the beat → next beat late; much shorter → frozen frame.

## Kit snippets
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
- Compute the trace once, animate after; `assert` worked examples at the top of the file.
- LaTeX: split `MathTex` into parts to colour or transform; plots with `Axes` + `ValueTracker` + `always_redraw`. Without LaTeX: no `MathTex`, `Matrix`, `DecimalNumber`. No `Polyline`: use `VMobject().set_points_as_corners`.

## Camera
```python
self.cue("crosses the level", Flash(cross)); self.zoom_to(cross, width=4.5); self.hold(1); self.zoom_back()
```
- `pin(mob)` keeps it fixed on screen during camera moves.
- Up to ~3x is emphasis; beyond, a box on the old picture transforms into new axes.
- Values closer than a dot's width can't both be followed: inset, or other values.
- Stop at a crossing for a second.

## Typeface
`TEXT_FONT = "latex"`: `txt()` prose and `num()` numbers share LaTeX; `mono()` only for code. Three sizes.
