<!-- 副本：cs182/newton-schulz/narration.md 中 "## 07 · how_big" 的独立编辑文件。主源仍为 narration.md。 -->

## 07 · how_big — How big can σ be? (first failure)

> **Purpose.** Find the first threshold by trying a start that 'should' work.
> **Logic chain.** One is a valley, and every start so far fell into it → *but the largest start we tried was 1.3. How big can sigma be?* → 1.5 fine → 1.8 lands below zero and ends at −1 → *why negative?* half the cube has overtaken three halves of the number → *where does that begin?* → factor p to find √3 → *is everything below √3 safe?* → yes: one step lands in (0, 1], then it climbs → *and exactly at √3?* → lands on zero.
> **Beats.** 1.5 works. Predict 1.8 (pause, let the viewer guess). It flips to −1. Factor p(x) = (x/2)(3−x²): the hump crosses the axis at √3. Shaded region shows (0, √3) → +1.
> **Tone.** A real pause before revealing 1.8. Ask the question and wait.
> **Polish pass (novice check).** The step from 1.8 is computed aloud (2.7 minus 2.92), so the negative result is seen, not announced. The mirror rule is shown on one pair of numbers (p(0.216) = 0.32, p(−0.216) = −0.32) before it is used. One sentence says what "ending at minus one" means for a singular value. The factoring is done term by term. "Safe below √3" is argued in two short steps that each point at something on the graph.
> **Numbers used.** 1.5 → 0.5625 → 0.755 → 0.917 → 0.990. 1.8 → −0.216 → −0.319 → −0.462 → −0.644 → −0.832 → −0.960 → −0.998.

### how_big 01 <!-- #b9119e -->
So far every start rolled into the valley at one. But the largest start we tried was one point three, and we don't get to choose sigma. How large can it be before something goes wrong?

### how_big 02 <!-- #0aa92a -->
Go a little bigger, to one point five. That is past the hump, where the curve is already coming down, so the first step drops all the way to zero point five six. But from there it climbs as before, zero point seven five, zero point nine two, and into one. Still fine.
> screen: FadeIn, FadeIn, self.draw

### how_big 03 <!-- #ac882f -->
A little bigger again, one point eight. Before we look, where do you think it ends up?
> screen: FadeOut, FadeIn

### how_big 04 <!-- #8a41e6 -->
Do the step. Three halves of one point eight is two point seven. But half of its cube is two point nine two, which is bigger. Subtract, and the result is negative, minus zero point two one six.
What does p do with a negative number? p has only odd powers, so flipping the sign of the input just flips the sign of the output. Plus zero point two one six goes to plus zero point three two, so minus zero point two one six goes to minus zero point three two.
The negative side is a mirror image of the positive side. Call this the mirror rule. So this value does what its mirror image would do, with the sign flipped. It moves away from zero and settles at minus one.
For a singular value, that has the right size but the wrong sign. This direction ends up reversed.
> screen: FadeIn, self.draw

### how_big 05 <!-- #a51ad9 -->
So what went wrong was the very first step, which landed below the axis. On the graph, that is where the curve, after its hump, comes down and crosses the axis. Past that crossing, p of x is negative.
> screen: FadeOut, FadeOut, Create, Create, GrowFromCenter

### how_big 06 <!-- #de5caa -->
Where is the crossing? Both terms of p contain x over two. Three halves x is x over two times three, and one half x cubed is x over two times x squared. So p of x is x over two, times three minus x squared.
> screen: Write

### how_big 07 <!-- #6c74e8 -->
For a positive x, the first factor, x over two, is positive. So the sign of p comes from the second factor, three minus x squared.
> screen: FadeIn, Indicate

### how_big 08 <!-- #afdac5 -->
Three minus x squared is positive while x squared is below three, and negative once x squared passes three. The change happens at x equals square root of three, about one point seven three.
> screen: FadeIn, Indicate, FadeIn, Flash

### how_big 09 <!-- #d9920c -->
One point five is below square root of three, and it was fine. One point eight is just above it, and it flipped. That matches.
> screen: Indicate

### how_big 10 <!-- #ff045e -->
Then is every start below square root of three safe? Look at the curve between zero and square root of three. It stays above the axis, and its highest point, the top of the hump, is at height one. So wherever we start in this range, the first step lands somewhere between zero and one.
> screen: FadeOut, Create, Indicate, FadeOut

### how_big 11 <!-- #82fe74 -->
And between zero and one, the curve sits above the diagonal. That means the output is bigger than the input, so every step climbs. It cannot climb past one, because the curve never goes higher than one. And the only place where it stops moving is a fixed point, so it ends at one.
> screen: FadeIn, self.draw

### how_big 12 <!-- #7d7317 -->
So yes. Every sigma between zero and square root of three ends at one.
> screen: FadeOut

### how_big 13 <!-- #d097e3 -->
And exactly at square root of three, the second factor is zero, so p gives zero. The value lands on the fixed point at zero, and it stays there forever.
> screen: Create, FadeIn, Flash
