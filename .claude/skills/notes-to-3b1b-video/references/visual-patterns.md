# Visual patterns

Tested snippets for turning common course concepts into motion. Everything here
runs against `manim_kit` (Manim Community 0.21). Snippets marked **LaTeX** need
the LaTeX toolchain (`setup_env.sh --latex`); everything else only needs `Text`.

## Contents
1. Design principles (what makes it read as 3b1b)
2. Layout budget and pacing
3. Code and step-through execution
4. Bits, words and memory
5. Math: equations, plots, matrices (LaTeX)
6. Deep learning: networks, gradients, attention
7. Transitions and emphasis
8. Camera moves and one typeface

---

## 1. Design principles

- **One picture per beat, one step per thing said.** A beat is a few sentences of
  narration (`say`) about one picture; every thing those sentences mention happens on
  screen as it is said (`cue`). A sentence the picture does not act out is a frozen frame.
- **Show the mechanism, not a slide.** Don't put a bullet list on screen and
  read it. Build the object (array, register, network) and change it while the
  narration explains why. Text on screen should label things, not narrate.
- **Concrete first, then general.** Walk one example with real numbers (compute
  them in Python, see §3) before stating the rule. The rule lands because the
  viewer just watched it happen.
- **Color is meaning.** Pick a color per concept and keep it across the whole
  series (e.g. every "gradient" is BLUE_B, every "learning rate" YELLOW_D, every
  "loss" RED_C). Say so once, then rely on it.
- **Continuity over cuts.** Transform the old picture into the new one
  (`ReplacementTransform`, `TransformFromCopy`, `.animate`) instead of fading
  everything out and drawing from scratch — the viewer's eye keeps its place.
- **Teaching order.** Intuition before formalism, why before what, the question
  before its answer. Name a thing after the viewer has seen it.
- **Reveal a surprise, then resolve it.** The best moments in the RISC-V series
  were "wait, why is this immediate split in two?" → aligned-fields picture.
  Plan one such beat per episode.
- **Dark background, few colors, generous space.** `BG` + the Manim palette
  (BLUE_*, TEAL_*, GREEN_*, YELLOW_D, GOLD_*, RED_*, GREY_*). Leave margins.

## 2. Layout budget and pacing

Frame is 14.2 × 8 units, x ∈ [−7.1, 7.1], y ∈ [−4, 4].

| Zone | y range | Use |
|---|---|---|
| heading | ≈ 3.5 | `self.heading("...")` top-left |
| content | −2.9 … 3.3 | everything else |
| subtitle | −3.9 … −2.9 | reserved: one sentence at a time, at most two lines |

Rules that prevented most layout bugs:
- Place big objects with `to_edge` / `to_corner` / `set_x` / `set_y`, and
  position labels with `next_to` relative to the object they label.
- A left block + right block side by side: give each ≤ 6.3 units of width.
  Monospace code at font 26 is ≈ 0.19 units per character, so a 40-char line
  is ≈ 7.6 units — shorten comments or drop the font size before it collides.
- After `scale()`-ing a group, rebuild labels relative to the new size (or
  scale them with it); never mix pre- and post-scale coordinates.
- Keep content above y ≈ −2.9 so the subtitle band never covers it. A sentence too
  long for two lines is shown in parts, so the band never grows.
- Bilingual: the translation is usually wider. Design for the wider language, or
  keep labels short enough for both.

Pacing: the voice sets it. `say()` first waits until the previous beat has been
spoken, plus the pause after a beat (silent renders estimate ~5 CJK chars/s or ~2.8
words/s), then
starts the new one; animations passed to `say()`, `cue()`s and plain `self.play()`
calls after it run while it is spoken. `cue()` waits until the voice reaches its
phrase. Use `self.hold()` when the viewer needs a moment to look at the result and
`extra=` on `say()` for a longer pause. Add up the `run_time` of what follows a
`say()`: if it is longer than the beat, the next beat starts late (shorten the
animations); if much shorter, the picture stands still (add cues).

## 3. Code and step-through execution

```python
code = CodeListing([
    "while lo <= hi:",
    "    mid = (lo + hi) // 2",
], lang="python", font_size=26, line_gap=0.46)      # lang: "asm", "c", "python"
code.to_edge(LEFT, buff=0.6)
box = code.line_box(0)                                # highlight bar for line 0
self.play(FadeIn(box))
self.play(box.animate.become(code.line_box(1)))       # move the highlight
self.play(Circumscribe(code.glyphs(1, "mid"), color=RED_B))   # a token inside line 1
arrow = pc_arrow().move_to(code.left_of(1, 0.5))      # program-counter style pointer
```

Drive every value you show from real computation, not hand-typed numbers:

```python
def trace(arr, target):          # compute the steps once, animate them after
    ...
for lo, hi, mid in trace(ARR, TARGET):
    self.say(f"The middle of {lo}..{hi} is {mid}", regs[2].set(mid), ...)
```

Registers / named variables: `reg_column([("lo", 0), ("hi", 9)], color=TEAL_C)`
then `regs[0].set(new_value)` (in-place transform + a small flash).

For encodings, add `assert` lines at the top of the episode that check every
worked example (see the RISC-V `assert bits_to_hex(ADD) == "0x00A98933"`). A
wrong number in an explainer video is worse than no video.

## 4. Bits, words and memory

```python
row = bit_row("10110110", BLUE_B)                  # squares with digits
self.play(set_bit_row(row, "00001111"))            # change digits in place
bf = BitField([("sign", 1, RED_C), ("exponent", 8, GREEN_C), ("fraction", 23, BLUE_C)])
self.play(bf.fill_field(1, "10000001"))            # fields fill with a lagged reveal
mem = MemoryView(0x100, rows=6, cols=4)            # byte-addressed, little-endian helpers
self.play(mem.set_word(0x104, 42))
stack = WordColumn(0x1000, 5)                      # high addresses on top
```

`FormatScene` adds `encode()`, `hex_of()` and `fly_bits()` for "watch the
number get packed into fields" moments.

## 5. Math (LaTeX)

**LaTeX.** Split a formula into parts so each part can be colored or
transformed on its own:

```python
eq = MathTex(r"w", r"\leftarrow", r"w", r"-", r"\eta", r"\nabla_w L(w)")
eq[4].set_color(YELLOW_D); eq[5].set_color(BLUE_B)
self.say("Step against the gradient, scaled by the learning rate.", Write(eq))
```

Transform one equation into the next with
`TransformMatchingTex(eq1, eq2)` when they share parts.

Plots driven by a `ValueTracker` (the dot follows the tracker every frame):

```python
axes = Axes(x_range=[-3, 3, 1], y_range=[0, 9, 3], x_length=6, y_length=3.4,
            axis_config={"color": GREY_B, "include_tip": False})
f = lambda x: x ** 2
curve = axes.plot(f, color=BLUE_C)
x = ValueTracker(-2.6)
dot = always_redraw(lambda: Dot(axes.c2p(x.get_value(), f(x.get_value())), color=YELLOW_D))
for _ in range(4):                                  # gradient descent, lr = 0.3
    self.play(x.animate.set_value(x.get_value() - 0.3 * 2 * x.get_value()), run_time=0.6)
```

Matrices (**LaTeX**):

```python
W = Matrix([[1, 2], [3, 4]]).scale(0.7)
v = Matrix([[5], [6]]).scale(0.7)
prod = VGroup(W, v, MathTex("="), Matrix([[17], [39]]).scale(0.7)).arrange(RIGHT, buff=0.2)
self.play(Indicate(W.get_rows()[0]), Indicate(prod[3].get_entries()[0]))
```

## 6. Deep learning

```python
g, layers, edges = nn_diagram((3, 4, 2))           # fully connected net
self.play(Create(g))
self.play(LaggedStart(*[Indicate(n, color=YELLOW_D) for L in layers for n in L], lag_ratio=0.05))
self.play(ShowPassingFlash(edges.copy().set_color(YELLOW_D).set_stroke(width=3), time_width=0.5))  # forward pass

hm = heatmap([[0.9, .05, .05], [.2, .7, .1], [.1, .3, .6]])   # values in [0, 1]; cell=0.8 leaves room for labels
labels = VGroup(*[txt(t, 22, GREY_A).next_to(hm[j], UP, buff=0.12) for j, t in enumerate(["the", "cat", "sat"])])
```

Ideas that work well for a deep-learning course:
- **Backprop**: run `ShowPassingFlash` right-to-left over `edges` in a different
  color, and put the local gradient next to each node as it arrives.
- **Loss landscapes**: 1-D curve + tracker dot (above); for 2-D, draw contour
  rings with `axes.plot_implicit_curve` at several levels and move a dot.
- **Softmax / attention**: bars (`Rectangle`s whose heights come from the
  numbers) morphing from logits to probabilities; then the heatmap.
- **Convolution**: a small kernel `Square` grid sliding over an input grid with
  `.animate.shift`, writing each output cell as it goes.
- **Training dynamics**: a `ValueTracker` for "step", with `always_redraw`
  plots of loss that grow as it advances.

## 7. Transitions and emphasis

- `Indicate`, `Circumscribe`, `Flash`, `Wiggle` for "look here".
- `LaggedStart(*anims, lag_ratio=0.1)` for building rows/grids.
- `TransformFromCopy(a, b)` for "this value came from there".
- `self.clear_stage(keep1, keep2)` between sections (keeps the caption).
- `CurvedArrow(p, q, angle=±TAU/5)` for jumps/links; put it in a margin, not
  across text.

## 8. Camera moves and one typeface

`NarratedScene` is a `MovingCameraScene`. Use the camera where the argument rests on
something small:

```python
self.say("The curve crosses the level root three exactly once.\nCall that point b one.", ...)
self.cue("crosses the level", Flash(cross))
self.zoom_to(cross, width=4.5)            # or zoom_to(group): frames it with a margin
self.cue("Call that point", FadeIn(b1_label))
self.hold(1.0)
self.zoom_back()
```

- `self.pin(mob)` keeps a mobject where it is on the screen, at its size, while the
  camera moves: the formula kept in a corner all episode, a side panel. The subtitle is
  pinned for you.
- Zooming makes strokes and text thicker. Up to about 3x this reads as emphasis. Past
  that, draw a second set of axes for the region, and connect the two: a box around the
  region on the old picture, then `ReplacementTransform(box, new_axes_frame)` while the
  rest fades, so the viewer sees where the new picture came from. Never `clear_stage()`
  and cut to the closer view.
- Two values that differ by less than the width of a dot (2.2 and 2.23 on an axis from
  −2.5 to 2.5) cannot both be followed on one picture. Follow one on the full picture
  and the other in a magnified inset, or choose values the picture can tell apart.
- Where a result is a crossing of two curves, go there and stop for a second before
  moving on (`hold(1.0)`).

One typeface: with `TEXT_FONT = "latex"` in series.py, `txt()` typesets prose with LaTeX
(Unicode signs such as √3, −, σ, ≈ inside it become math) and `num()` typesets tick
labels and values in math mode. Then a "2.2" on an axis, in a label and in a formula
look the same. `mono()` stays monospace: use it for code only. Without the setting a
frame can easily carry three typefaces (formula, label, tick), which the user saw at
once. Keep font sizes to a few tiers as well (formula, label, tick), not a dozen.
