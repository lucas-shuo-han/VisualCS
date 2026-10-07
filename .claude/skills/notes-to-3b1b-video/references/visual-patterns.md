# Visual patterns

Layout budget and snippets for `manim_kit` (Manim Community 0.21). Snippets marked
**LaTeX** need the toolchain; the rest only need `Text`. General Manim practice is not
repeated here.

## Principles

- One picture per beat, one step per thing said. A sentence the picture does not act
  out is a frozen frame.
- Build the object (array, register, network) and change it while the narration says
  why. Text on screen labels things; it does not narrate.
- A worked example with real numbers before the rule, so the rule summarises what was
  just watched. One "wait, why?" per episode, then the picture that resolves it.
- Colour is meaning: one colour per concept across the series, said once.
- Transform the old picture into the new one (`ReplacementTransform`,
  `TransformFromCopy`, `.animate`) instead of fading everything and starting over.

## Layout budget

The frame is 14.2 × 8 units: x ∈ [−7.1, 7.1], y ∈ [−4, 4].

| Zone | y | Use |
|---|---|---|
| heading | ≈ 3.5 | `self.heading("...")`, top left |
| content | −2.9 to 3.3 | everything else, x within ±6.8 |
| subtitle | −3.9 to −2.9 | reserved: one sentence, two lines at most |

- Place big objects with `to_edge` / `to_corner` / `set_x` / `set_y`; place every label
  with `next_to` its object, after the object has its final position.
- Two blocks side by side: 6.3 units each at most. Monospace at font 26 is about 0.19
  units per character, so a 40-character line is 7.6 units.
- After `scale()`, rebuild labels or scale them too.
- A panel beside a graph: lines from one anchor going down; check the frame where it is
  fullest against whatever stays all episode (a corner formula).
- A label at the start of a path hides the axis label there: use a dot, put the number
  in the side panel, and a level line's label at its far end.
- Two languages: design for the wider one (English runs 1.3 to 2 times wider than Chinese).

The kit reports text over text, off the frame and in the subtitle band as `[layout]`.
Text over a shape or a curve, and anything mid-animation, only the sheets show.

## Timing

`say()` waits for the previous beat and its pause, then starts; its animations, `cue()`s
and plain `self.play()` calls run while it is spoken. Add up the `run_time` after a
`say()`: longer than the beat and the next beat starts late; much shorter and the
picture stands still. `hold(extra)` gives the viewer a moment; `extra=` on `say()` a
longer pause.

## Kit snippets

```python
code = CodeListing(["while lo <= hi:", "    mid = (lo + hi) // 2"],
                   lang="python", font_size=26, line_gap=0.46).to_edge(LEFT, buff=0.6)   # "asm" | "c" | "python"
box = code.line_box(0); self.play(FadeIn(box))
self.play(box.animate.become(code.line_box(1)))                 # move the highlight
self.play(Circumscribe(code.glyphs(1, "mid"), color=RED_B))     # a token in line 1
arrow = pc_arrow().move_to(code.left_of(1, 0.5))

regs = reg_column([("lo", 0), ("hi", 9)], color=TEAL_C); self.play(regs[0].set(5))

row = bit_row("10110110", BLUE_B); self.play(set_bit_row(row, "00001111"))
bf = BitField([("sign", 1, RED_C), ("exponent", 8, GREEN_C), ("fraction", 23, BLUE_C)])
self.play(bf.fill_field(1, "10000001"))
mem = MemoryView(0x100, rows=6, cols=4); self.play(mem.set_word(0x104, 42))
stack = WordColumn(0x1000, 5)                                   # high addresses on top
# FormatScene adds encode(), hex_of(), fly_bits() for packing a number into fields

g, layers, edges = nn_diagram((3, 4, 2)); self.play(Create(g))
self.play(ShowPassingFlash(edges.copy().set_color(YELLOW_D).set_stroke(width=3), time_width=0.5))
hm = heatmap([[0.9, .05, .05], [.2, .7, .1], [.1, .3, .6]])     # values in [0, 1]
```

Compute the steps once and animate them after, so the picture cannot disagree with the
algorithm (`for lo, hi, mid in trace(ARR, TARGET): ...`), and `assert` every worked
example at the top of the file.

**LaTeX**: split a formula into parts to colour or transform them
(`MathTex(r"w", r"\leftarrow", r"w", r"-", r"\eta", r"\nabla_w L(w)")`,
`TransformMatchingTex`). Plots: `Axes` + `ValueTracker` + `always_redraw`. Without
LaTeX there is no `Tex`, `MathTex`, `Matrix`, `DecimalNumber` or `Integer`.
`Polyline` does not exist in every version: `VMobject().set_points_as_corners([...])`.

Deep-learning pictures that worked: backprop as a flash running right to left with the
local gradient appearing at each node; a loss curve with a tracker dot, contour rings
for 2-D; bars morphing from logits to probabilities, then the heatmap; a kernel grid
sliding over an input, writing each output cell.

## Camera

`NarratedScene` is a `MovingCameraScene`.

```python
self.say("The curve crosses the level root three exactly once.\nCall that point b one.", ...)
self.cue("crosses the level", Flash(cross))
self.zoom_to(cross, width=4.5)            # or zoom_to(group): frames it with a margin
self.cue("Call that point", FadeIn(b1_label))
self.hold(1.0)
self.zoom_back()
```

- `pin(mob)` keeps a mobject at its place and size on the screen while the camera
  moves (a corner formula, a side panel). The subtitle is pinned for you.
- Up to about 3x a zoom reads as emphasis. Past that, draw second axes for the region
  and connect them: a box on the old picture, `ReplacementTransform(box, new_frame)`
  while the rest fades. Never `clear_stage()` and cut to the closer view.
- Two values closer than a dot's width (2.2 and 2.23 on an axis from −2.5 to 2.5)
  cannot both be followed on one picture: an inset for one, or other values.
- At a crossing of two curves, go there and stop for a second before moving on.

## One typeface

With `TEXT_FONT = "latex"` in series.py, `txt()` typesets prose with LaTeX (Unicode
signs such as √3, −, σ, ≈ become math) and `num()` typesets ticks and values in math
mode, so "2.2" looks the same on an axis, in a label and in a formula. `mono()` stays
monospace, for code only. Without it a frame easily carries three typefaces, which the
user saw at once. Three font sizes (formula, label, tick), not a dozen.
