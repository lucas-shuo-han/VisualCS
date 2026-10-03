<!-- 副本：cs182/newton-schulz/narration.md 中 "## 12 · boundary_points" 的独立编辑文件。主源仍为 narration.md。 -->

## 12 · boundary_points — Do the stripes fill the gap? And the edges

> **Purpose.** Check that the method covers everything between √3 and √5, and say what happens to the edges themselves.
> **Logic chain.** *Is there a last piece next to √5 that no stripe reaches?* → look at how the edges were found: across to the folded curve, up to the diagonal, across again: a staircase between the curve and the diagonal → every step goes right and never passes √5, so the edges close in on some point → there the staircase has no room, so the curve touches the diagonal → in the gap that only happens at √5 → so the edges come as close to √5 as we like, every start below √5 is in some stripe → *and the edges themselves?* b₁ lands exactly on −√3, then on 0 → b₂ lands on −b₁, one step more; every edge ends on 0 → should that worry us? no: single points, and 0 is the top of the hill; the tiniest nudge rolls to ±1.
> **Tone.** A short proof, then a calm closing remark.
> **Polish pass (novice check).** No limit notation; "close in on a point" and "no room left" carry the argument. The edge paths are shown as hops on a number line.
> **Numbers used.** b₁ → −√3 → 0. b₂ → −b₁ → √3 → 0. b₃ → −b₂ → b₁ → −√3 → 0.
> **Animation.** The corner of the gap picture next to √5 (x from 2.05 to 2.26); the staircase drawn step by step; the dot at √5; then three number lines with the hopping edges and their chains; two nudged starts rolling to −1 and +1.

### boundary_points 01 <!-- #b8d83c -->
One question is still open. Do the stripes really fill the whole gap? Or is there a last piece, right next to square root of five, that no stripe ever reaches? Look at how we found the edges. Here is the corner of the picture next to square root of five. Start at the height square root of three, and go across to the folded curve. That is b one. Go up to the diagonal, and across to the curve again. That is b two. The edges are a staircase, squeezed between the curve and the diagonal.

### boundary_points 02 <!-- #f1c72f -->
Every step of the staircase moves to the right, and it can never get past square root of five. So the edges close in on some point. At that point the staircase has no room left, which means the curve touches the diagonal there. And in the gap, the only place where the curve touches the diagonal is square root of five itself. So the edges come as close to square root of five as we like. Every start below square root of five is passed by some edge, so it lies in some stripe. The stripes fill the whole gap.

### boundary_points 03 <!-- #62fe7d -->
And what about the edges themselves? Take b one. Its first step lands exactly on minus square root of three. And we know what happens at square root of three. The next step gives exactly zero, and by the mirror rule the same holds for minus square root of three. So b one ends on zero, and stays there.

### boundary_points 04 <!-- #ba4456 -->
b two lands on minus b one, and from there it follows the path of b one with the sign flipped. So it takes one step more. And b three takes one step more again. Every edge reaches plus or minus square root of three after a few steps, and then it sits on zero forever. An edge never reaches one or minus one.

### boundary_points 05 <!-- #ea416e -->
Should that worry us? Not much. Each edge is a single point, and zero is the top of the hill. Move the start by the tiniest amount, and it is inside a stripe on one side or the other, and it rolls down to plus one or minus one.
