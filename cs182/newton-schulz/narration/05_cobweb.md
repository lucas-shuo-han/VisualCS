<!-- 副本：cs182/newton-schulz/narration.md 中 "## 05 · cobweb" 的独立编辑文件。主源仍为 narration.md。 -->

## 05 · cobweb — The picture of the iteration

> **Purpose.** Turn the arithmetic into a graph: up to the curve, across to the diagonal, repeat.
> **Logic chain.** We need a picture of the iteration → the graph of p turns an input into a height → *but the next step needs that height as an input* → the diagonal turns a height into a position → one step = up to the curve, across to the diagonal → staircases from 0.3 and 1.2 → fixed points are the crossings → *the picture shows paths leaving zero and entering one, but not yet why* → slopes.
> **Order matters.** The diagonal is not drawn in beat 01. It appears in beat 04, as the answer to the problem raised in beat 03 (a height has to become a position). Code change needed: move the creation of y = x from beat 01 to beat 04.
> **Beats.** Axes with y=p(x); one step with labelled points; why the diagonal; the staircase from 0.3; the same from 1.2.
> **Tone.** Explain the diagonal as 'height equals position', the one idea students trip on.
> **Polish pass (novice check).** Beat 01 now describes the shape of the curve using values the viewer already computed (p(0)=0, p(1)=1). The second step is walked through in full in beat 05 before the word "repeat" is used. The crossings in beat 07 are tied to the definition of a fixed point from scene 04.
> **Numbers used.** 0.3 → 0.44 → 0.61 → 0.80 → 0.95 → 0.997. 1.2 → 0.936 → 0.994.

### cobweb 01 <!-- #b2675a -->
Start with the graph of p. Along the bottom is the input x, and the height of the curve above it is the output, p of x. We know a few points already. At zero the height is zero, and at one the height is one. The curve rises from zero, reaches a hump at one, and comes back down after it.
> screen: Create, FadeIn, Create, Create, FadeIn, FadeIn

### cobweb 02 <!-- #192798 -->
On this picture, one step of the iteration looks like this. Start at x equals zero point three on the bottom axis, and go straight up to the curve. The height you reach is p of zero point three, about zero point four four.
> screen: FadeIn, FadeIn, Create

### cobweb 03 <!-- #5f6d39 -->
For the next step, zero point four four has to become the new input. But right now it is a height, and inputs are measured along the bottom. We need a way to turn a height into a position.
> screen: FadeIn, Create

### cobweb 04 <!-- #cf6c96 -->
Here is a line that does exactly that, the diagonal y equals x. Every point on it is as far to the right as it is high. So go sideways from the curve until you hit the diagonal. You are still at height zero point four four, and now you are also above x equals zero point four four.
> screen: GrowFromCenter, FadeIn, Create

### cobweb 05 <!-- #373a2a -->
From there, the second step is the same move. Go straight up to the curve, which gives zero point six one, and sideways to the diagonal again. Keep repeating, and the path climbs like a staircase, zero point eight, zero point nine five, and into one.
> screen: FadeIn, self.draw

### cobweb 06 <!-- #df1d8d -->
Now a start above one. From one point two, the curve is below the diagonal, so the first move goes down, to zero point nine four. After that the path climbs the last little bit and settles on one as well.
> screen: FadeOut, FadeIn, self.draw

### cobweb 07 <!-- #23bcae -->
Now look at where the curve meets the diagonal. On the diagonal the height equals x, and on the curve the height is p of x. So at a crossing, p of x equals x. The three crossings are our three fixed points, minus one, zero, and one.
And the staircases show which way things move around them. Near zero the path walks away, and near one it walks in.
> screen: FadeOut, LaggedStart
