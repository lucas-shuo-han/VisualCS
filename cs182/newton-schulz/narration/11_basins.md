<!-- 副本：cs182/newton-schulz/narration.md 中 "## 11 · basins" 的独立编辑文件。主源仍为 narration.md。 -->

## 11 · basins — Each stripe lands on the one before

> **Purpose.** Reduce every unknown stripe to the one already solved: one step (in size) carries stripe n onto stripe n − 1, so it needs exactly one more flip.
> **Logic chain.** Starts above b₁ do not get inside in one step → *but we need not follow them all the way*: if the first step lands in the first stripe, we already know the rest: one more flip → which starts land there? the folded curve passes through the band √3..b₁ on the vertical axis; it leaves it at height b₁: call that start b₂ → b₁..b₂ is the second stripe: two flips, ends at +1 → check with 2.2 (size 2.02 is in the first stripe) → the same step again gives b₃ and the third stripe → values of b₁, b₂, b₃ creep up to √5 → all stripes on one bar: stripe n flips n times, odd → −1, even → +1 → zoom: the pattern repeats → why so thin: near √5 one step stretches distances by six, so each stripe is a sixth of the one before.
> **Tone.** The "land on what we already know" step is the heart of the section; give it time, then let the repeats go faster.
> **Polish pass (novice check).** Each new stripe is defined by where it lands, read off the picture, before any formula. The factor six comes from two starts already seen (2.20 and 2.23), not from a derivative.
> **Numbers used.** b₁ ≈ 2.148, b₂ ≈ 2.221, b₃ ≈ 2.234, √5 ≈ 2.236. |p(2.20)| = 2.02, |p(2.23)| = 2.20; 0.03 in, 0.18 out.
> **Animation.** The stretched gap picture; the first stripe is copied onto the vertical axis as a band; the curve leaves the band at b₂; the path of 2.2; the second band and b₃; the values; then the bar with all stripes and the zoom towards √5; the two starts for the factor six.

### basins 01 <!-- #9eed20 -->
Now the starts above b one. Their first step does not get inside. But we do not have to follow them all the way. Suppose the first step lands, in size, somewhere in the first stripe. We already know the first stripe. From there it takes one more flip to get inside. So such a start flips exactly twice.

### basins 02 <!-- #5fbd24 -->
Which starts are those? Read it off the picture. On the vertical axis, the first stripe is the band of sizes from square root of three up to b one. The folded curve passes through that band. It enters at b one, and it leaves at a new point, where its height is exactly b one. Call that point b two. So every start between b one and b two lands in the first stripe. Two flips, an even number, so it ends at plus one. This is the second stripe.

### basins 03 <!-- #d758fb -->
Check it with two point two. It sits between b one and b two. Its first step has size two point zero two. And two point zero two lies between square root of three and b one, in the first stripe. So one more flip, and it is inside. That is the two flips we counted, and it ended at plus one.

### basins 04 <!-- #4bc08a -->
And the same step works again. Starts that land in the second stripe need one flip more than the second stripe does, so three flips. The curve leaves that band where its height is b two. Call that point b three. The starts between b two and b three are the third stripe, and they end at minus one. Each new stripe is carried onto the stripe before it, so it needs exactly one more flip.

### basins 05 <!-- #19bd55 -->
Each edge is found like b one, by trying values. b one is about two point one four eight. b two is about two point two two one. b three is about two point two three four. They creep up toward square root of five, which is two point two three six.

### basins 06 <!-- #6b2a00 -->
So here are all the stripes on one line. Stripe number n flips n times. An odd n ends at minus one, and an even n ends at plus one. That is the striped picture we saw.

### basins 07 <!-- #477d72 -->
The stripes pile up against square root of five. Zoom in, and the same pattern shows up again and again.

### basins 08 <!-- #95db52 -->
Why do the stripes get thin so quickly? Near square root of five the folded curve is steep. From two point two to two point two three, the start moves by zero point zero three. But the size after the step moves from two point zero two to two point two zero, which is zero point one eight. That is six times as far. So one step stretches a stripe to six times its width. And the stretched stripe has to fit exactly onto the stripe before it. So each stripe is only about a sixth as wide as the one before.
