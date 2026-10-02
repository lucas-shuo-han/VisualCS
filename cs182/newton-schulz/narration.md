# Newton–Schulz: where does a singular value go? — narration script

> **How to use this file.** Everything here is plain text.
> - **Body** = the plain lines under each `###` heading. That text is the on-screen caption and what the voice says.
> - **`speak:`** (optional) = a different wording for the voice only, for math the voice would misread.
> - **Notes** = any line starting with `>` or `//`, and `<!-- ... -->`. Never rendered. Use them freely.
> - Do not edit the `### name NN <!-- #hash -->` heading lines: they tie each line to the code.
> - Keep each caption under ~105 characters (two lines). Check with `narration.py check`.
> - Preview: `render.py cs182/newton-schulz 1 --preview --voice` (only changed lines are re-voiced).
> - **Wording, tone and sentence order inside a scene** are edited here. **Which scene comes first, or
>   adding/removing a beat**, changes the animation code: write it in the scene's notes and ask Claude.

## The story in one paragraph

> A matrix W turns a circle into an ellipse; its singular values are the half-axes. Muon wants the
> update to be orthogonal (a circle, all stretches equal to 1), and the SVD is too slow. So we repeat one
> matrix-product-only step, and the SVD tells us each singular value just follows a number map p.
> The rest of the video is one question about p: where does a starting value σ end up? The answer is
> "+1" below √3, a flip past √3, a blow-up past √5, and in the thin gap between, a pattern of stripes.
> The video ends by turning that into a recipe: scale W first so every σ is below √3.

## The viewer, scene by scene (what they know, what they now want to ask)

> | # | Scene | Viewer already knows | Viewer now wants to know |
> |---|---|---|---|
> | 1 | ellipse | what a matrix does to a circle | why would anyone want W to be a circle? |
> | 2 | why_p | σ's are the half-axes; SVD is slow | where does the cubic come from? |
> | 3 | try_numbers | p(σ) = 1.5σ − 0.5σ³ and how to evaluate it | does it really go to 1? what stays put? |
> | 4 | cobweb | numbers 0.5, 1.3, 0.1 all go to 1 | can I see the whole iteration at once? |
> | 5 | slopes | the staircase picture; fixed points −1, 0, 1 | why do ±1 attract and 0 repel? |
> | 6 | how_big | small starts work; ±1 attract | how big can σ be before it breaks? |
> | 7 | too_big | 1.8 flipped to −1; the hump crosses at √3 | does everything past √3 go to −1? (3 explodes) |
> | 8 | the_gap | flips shrink up to √5, grow beyond | what happens between √3 and √5? |
> | 9 | first_boundary | a mysterious stripe pattern | where do the stripe edges come from? |
> | 10 | basins | the first edge b1 | all the edges, and the mirror argument |
> | 11 | boundary_points | the edges b_n climb to √5 | what are the edges exactly? ratio 6 |
> | 12 | summary | the complete picture | what is the one-line answer? |
> | 13 | back_to_matrix | the table of fates | so what do I do with my matrix? |

## 01 · ellipse — Why would anyone iterate this? (motivation)

> **Purpose.** Give a reason to care before any formula. Muon wants an orthogonal update; the picture of 'orthogonal' is a circle.
> **Beats.** (1) W maps the unit circle to an ellipse. (2) SVD demo: rotate, stretch, rotate. (3) the stretches are σ1, σ2 = half-axes. (4) all stretches 1 means only rotations: orthogonal. (5) SVD is slow, so iterate with matrix products only; watch (1.3, 0.5) become a circle in 5 steps.
> **Tone.** Calm, concrete. No jargon before the picture.
> **Open choices.** Is the SVD demo too long before the viewer sees why? Would you start with the finished 5-step animation (the payoff) and then explain it?

### ellipse 01 <!-- #5ce9c7 -->
Take a matrix W. It turns the unit circle into an ellipse.
> screen: Create, FadeIn

### ellipse 02 <!-- #a892b3 -->
How? Every matrix does it in three moves. Follow two perpendicular arms on the circle.
> screen: FadeIn, Write

### ellipse 03 <!-- #e14429 -->
First, a rotation turns the arms onto the axes. That is V transpose.
> screen: Rotate, FadeIn, Indicate

### ellipse 04 <!-- #8ee4e9 -->
Next, Σ stretches each axis by its own amount, here 1.3 and 0.5. The circle becomes an ellipse.
> screen: demo.animate.apply_matrix, FadeIn, Indicate

### ellipse 05 <!-- #7f031e -->
Finally U rotates the ellipse into place. Rotations never change lengths, so all the stretching lives in Σ.
> screen: Rotate, FadeIn, Indicate

### ellipse 06 <!-- #ef972a -->
The two stretch factors, σ1 and σ2, are the half-axes of the ellipse: W's singular values.
> screen: Indicate, Indicate

### ellipse 07 <!-- #8559d4 -->
If every stretch were exactly 1, only the rotations would remain: W would be orthogonal.
> screen: FadeIn

### ellipse 08 <!-- #e5460e -->
Optimizers like Muon want this for every weight update: same directions, every stretch 1.
> screen: FadeIn

### ellipse 09 <!-- #18ff36 -->
An SVD could do it, but it is slow on a GPU. The Newton–Schulz iteration uses only matrix products.
> screen: FadeOut, Write, FadeIn

### ellipse 10 <!-- #d6caa9 -->
Let's apply it a few times and watch the ellipse.
> screen: FadeIn

### ellipse 11 <!-- #ec2f8b -->
After a handful of steps, the ellipse is a circle. Why does this work? And can it fail?
> screen: Flash

## 02 · why_p — You could have invented p (design)

> **Purpose.** Answer 'how could we possibly know this cubic?'. Matrix products give only odd powers of σ (σ, σ³, σ⁵), so the cheapest recipe is aσ + bσ³.
> **Beats.** SVD gives W_{k+1} = U p(Σ) Vᵀ, so each σ moves on its own. Powers: W→σ, WWᵀW→σ³. Two wishes, p(1)=1 and p′(1)=0, force a = 3/2, b = −1/2. Then the question that drives the rest: σ → p(σ) → p(p(σ)) → … → ?
> **Tone.** 'You could have done this yourself.' Slow on the two wishes; each is one sentence.
> **Open choices.** Is 'p′(1) = 0' motivated enough here, or should it wait until the slopes scene?

### why_p 01 <!-- #aeca84 -->
To see why, write W with its SVD. U and V only rotate; all the stretching sits in Σ.
> screen: FadeIn, Write, FadeIn

### why_p 02 <!-- #3e6e23 -->
Plug it into the iteration. U and V pass through untouched; only the middle Σ changes.
> screen: VGroup, Write

### why_p 03 <!-- #a05e4d -->
Σ is diagonal, so each singular value is updated on its own: σ becomes p(σ).

### why_p 04 <!-- #73f821 -->
But why this cubic? Imagine inventing it yourself, with only matrix products to work with.

### why_p 05 <!-- #99981e -->
Multiplying W by W transpose and W again turns each σ into σ cubed; one more round gives σ to the fifth.
> screen: LaggedStart

### why_p 06 <!-- #81e917 -->
So the cheapest recipe is a mix of the first two: a times σ plus b times σ cubed.
> screen: odd.animate.scale, FadeIn

### why_p 07 <!-- #4c1bb5 -->
Wish one: a σ that is already 1 should stay 1. That means a + b = 1.
> screen: FadeIn

### why_p 08 <!-- #348df8 -->
Wish two: a σ near 1 should snap to 1 fast, so the curve should be flat there. That means a + 3b = 0.
> screen: FadeIn

### why_p 09 <!-- #98425b -->
Solve: a = 3/2 and b = −1/2. That is exactly the Newton–Schulz polynomial.
speak: Solve, and a is three halves, b is minus one half. That is exactly the Newton Schulz polynomial.
> screen: FadeOut, ReplacementTransform, Create

### why_p 10 <!-- #7f610a -->
Start at some positive σ, apply p over and over. Where does it end up? That is part (e).
> screen: FadeIn

## 03 · try_numbers — Just try numbers (easy cases first)

> **Purpose.** Build trust with starts that behave: 0.5, 1.3, 0.1 all go to 1, by hand arithmetic. Then ask what could stay put and solve p(x) = x step by step.
> **Beats.** p(0.5) arithmetic; the staircase of values; the algebra x(1−x)(1+x)=0 gives 0, 1, −1.
> **Tone.** Unhurried. Say each arithmetic step aloud; let the numbers appear one at a time.

### try_numbers 01 <!-- #3a1984 -->
No theory yet. Let's just try numbers, starting at 0.5.
> screen: FadeIn

### try_numbers 02 <!-- #ba643a -->
One step: three halves of 0.5 is 0.75. Half of 0.5 cubed is 0.0625. Subtract: 0.6875.
speak: One step: three halves of 0.5 is 0.75. Half of 0.5 cubed is 0.0625. Subtract, and we get 0.6875.
> screen: Write

### try_numbers 03 <!-- #353593 -->
Keep going: 0.69 becomes 0.87, then 0.98, then 1.
> screen: FadeOut, Write

### try_numbers 04 <!-- #6fe2bd -->
1.3 drops to 0.85, then climbs back up to 1.
> screen: Write

### try_numbers 05 <!-- #5782f1 -->
Even a tiny 0.1 creeps up, slowly at first, and also reaches 1.
> screen: Write

### try_numbers 06 <!-- #9fea9d -->
Everything lands on 1, just as designed: p(1) = 1, so once a value reaches 1, it stays.
> screen: FadeIn

### try_numbers 07 <!-- #673f82 -->
A point with p(x) = x is called a fixed point: once there, you never move. Is 1 the only one?
> screen: FadeIn

### try_numbers 08 <!-- #d6003a -->
Write it out, and subtract x from both sides.
> screen: FadeIn

### try_numbers 09 <!-- #f7385d -->
Now factor: one half, times x, times 1 minus x, times 1 plus x.
> screen: FadeIn

### try_numbers 10 <!-- #22b296 -->
A product is zero only if one factor is zero. So there are three fixed points: 0, 1 and −1.
> screen: FadeIn

### try_numbers 11 <!-- #4efe2b -->
So why does 0.1 walk away from 0 and toward 1? A picture makes it clear.

## 04 · cobweb — The picture of the iteration

> **Purpose.** Turn the arithmetic into a graph: up to the curve, across to the diagonal, repeat.
> **Beats.** Axes with y=p(x) and y=x; one step with labelled points; why the diagonal; the staircase from 0.3; the same from 1.2.
> **Tone.** Explain the diagonal as 'height equals position', the one idea students trip on.

### cobweb 01 <!-- #223837 -->
Draw the curve y = p(x), and the diagonal y = x.
> screen: Create, FadeIn, Create, Create, FadeIn, FadeIn

### cobweb 02 <!-- #37e85e -->
To iterate on the picture, go from x up to the curve: that height is p(x).
> screen: FadeIn, FadeIn, Create

### cobweb 03 <!-- #8a9a9e -->
Then go across to the diagonal. That moves p(x) back onto the x axis as the new x.
> screen: FadeIn, Create

### cobweb 04 <!-- #543949 -->
Why the diagonal? On it, height equals position. So we arrive above x = 0.44, ready for the next step.
> screen: GrowFromCenter, FadeIn, Create

### cobweb 05 <!-- #79948d -->
Repeat. Starting at 0.3, the path climbs a staircase up to 1.
> screen: FadeIn, self.draw

### cobweb 06 <!-- #2924b4 -->
From 1.2, it drops just below 1, then settles on 1 as well.
> screen: FadeOut, FadeIn, self.draw

### cobweb 07 <!-- #4ce293 -->
The fixed points −1, 0 and 1 are exactly where the curve meets the diagonal.
> screen: FadeOut, LaggedStart

## 05 · slopes — Why ±1 attract and 0 repels

> **Purpose.** Stability from the derivative. Linearize: p(x*+e) ≈ x* + p′(x*)·e.
> **Beats.** p′(0)=1.5 pushes away; p′(±1)=0 (the wish from scene 2) squares the error, so convergence is very fast.
> **Tone.** Connect back: 'this is exactly what we wished for'.

### slopes 01 <!-- #cca490 -->
Why is 1 a magnet while 0 pushes things away? Look at the slope of p at each one.
> screen: Write

### slopes 02 <!-- #3a2d20 -->
Zoom in on a fixed point and the curve looks like a straight line with slope p'.
> screen: FadeIn

### slopes 03 <!-- #ab34a8 -->
So a small offset e gets multiplied by the slope each step. Slope above 1: it grows. Below 1: it shrinks.
> screen: Indicate

### slopes 04 <!-- #bc6997 -->
At 0 the slope is 1.5, so a small offset grows by half each step. From 0.05 it drifts away.
> screen: Create, FadeIn

### slopes 05 <!-- #f8c7c5 -->
At ±1 the slope is 0, as we wished, so the error roughly squares: from 1.2 it is 0.2, 0.064, 0.006.
> screen: FadeOut, Create, FadeIn

### slopes 06 <!-- #1d7ef8 -->
So 0 is unstable, like a hilltop, and ±1 are stable, like the bottoms of two valleys.
> screen: FadeIn

## 06 · how_big — How big can σ be? (first failure)

> **Purpose.** Find the first threshold by trying a start that 'should' work.
> **Beats.** 1.5 works. Predict 1.8 (pause, let the viewer guess). It flips to −1. Factor p(x) = (x/2)(3−x²): the hump crosses the axis at √3. Shaded region shows (0, √3) → +1.
> **Tone.** A real pause before revealing 1.8. Ask the question and wait.

### how_big 01 <!-- #c798ae -->
So far every start went to 1. But we don't get to choose σ. How large can it be?

### how_big 02 <!-- #19597c -->
Try 1.5. It drops to 0.56, then climbs back to 1. Still fine.
> screen: FadeIn, FadeIn, self.draw

### how_big 03 <!-- #408480 -->
Now 1.8, a little bigger. Before we look: where do you think it ends up?
> screen: FadeOut, FadeIn

### how_big 04 <!-- #9e58b1 -->
It lands below the axis, at −0.216, and then slides all the way down to −1!
> screen: FadeIn, self.draw

### how_big 05 <!-- #be8b58 -->
After its hump, the curve comes back down and crosses the axis. Past that point, p(x) is negative.
> screen: FadeOut, FadeOut, Create, Create, GrowFromCenter

### how_big 06 <!-- #eba037 -->
Where exactly? Pull out a factor: p(x) is x over 2, times 3 minus x squared.
> screen: Write

### how_big 07 <!-- #4bca22 -->
For positive x, the first factor x over 2 is positive. So the sign comes from the second one.
> screen: FadeIn, Indicate

### how_big 08 <!-- #0cb323 -->
3 minus x squared turns negative once x squared passes 3: at x = √3, about 1.73.
> screen: FadeIn, Indicate, FadeIn, Flash

### how_big 09 <!-- #686bc1 -->
And 1.8 is just past √3. That is why it flipped.
> screen: Indicate

### how_big 10 <!-- #b26f28 -->
Below √3, the hump stays above the axis but never above 1. So one step lands between 0 and 1.
> screen: FadeOut, Create, Indicate, FadeOut

### how_big 11 <!-- #b64164 -->
And between 0 and 1 the curve sits above the diagonal, so every step climbs, never past 1.
> screen: FadeIn, self.draw

### how_big 12 <!-- #4421be -->
So every σ between 0 and √3 ends at +1.
> screen: FadeOut

### how_big 13 <!-- #646e44 -->
And exactly at √3? p(√3) = 0. It lands on the unstable fixed point 0, and stays there forever.
> screen: Create, FadeIn, Flash

## 07 · too_big — Try 3, and the line y = −x

> **Purpose.** Discover √5 as the boundary between shrinking and growing.
> **Beats.** 3 → −9 → 351. Compare 2.0 (lands at size 1) with 2.3 (lands at 2.63, bigger). Draw y=−x: flipped values shrink while the curve is above it; they meet at √5; √5 is a period-2 square. Beyond √5 diverges.
> **Tone.** The y = −x picture is the proof; keep the narration short while it draws.

### too_big 01 <!-- #fe86f6 -->
Past √3 the sign flips every step. That alone might be fine. But try a big start, like 3.
> screen: FadeIn

### too_big 02 <!-- #23daf6 -->
p(3) = −9, and then 351. Flipping and growing: it explodes.
> screen: FadeIn

### too_big 03 <!-- #d4e5fb -->
Both 1.8 and 3 flip. The difference is size. Compare two starts: 2.0 lands at size 1, smaller.
> screen: FadeOut, FadeIn

### too_big 04 <!-- #e08384 -->
But 2.3 lands at size 2.63, bigger than its start. Somewhere between, shrinking turns into growing.
> screen: FadeIn

### too_big 05 <!-- #340999 -->
To find where, draw y = −x. A flipped value has shrunk exactly when the curve lies above that line.
> screen: Create, FadeIn

### too_big 06 <!-- #aee967 -->
Just past √3, the curve is above that line: flip and shrink. Further out it dives below: flip and grow.
> screen: Create, Create

### too_big 07 <!-- #614b2a -->
They meet where p(x) = −x, that is x squared = 5. The second key number is √5, about 2.24.
> screen: GrowFromCenter, FadeIn, Create, FadeIn

### too_big 08 <!-- #5730fa -->
Start exactly at √5: it lands on −√5, then back on √5. The cobweb becomes a square.
> screen: FadeOut, self.draw

### too_big 09 <!-- #c5c258 -->
So √5 neither settles nor explodes. It bounces between ±√5 forever: a period-2 orbit.
> screen: FadeIn

### too_big 10 <!-- #6442ed -->
Just past it, at 2.3, every step flips and grows: −2.63, 5.18, −61.8. It diverges.
> screen: FadeIn

## 08 · the_gap — The gap (√3, √5): show the mystery

> **Purpose.** Show the stripe pattern before explaining it. Starts in [0, 2.4] coloured by fate; zoom toward √5 shows stripes squeezed together. Then follow 2.0, 2.2, 2.23 and count flips.
> **Tone.** Curiosity, not authority. 'Why would that be?'
> **Open choices.** This is the hardest scene for a first-time viewer (your earlier feedback). Consider an easier warm-up start before the colour strip.

### the_gap 01 <!-- #1f610a -->
That leaves the gap between √3 and √5: flip and shrink. Shrinking, it must fall below √3 at some point.
> screen: Create, FadeIn, FadeIn

### the_gap 02 <!-- #ec1df4 -->
Could it shrink forever and stall inside the gap? No: sizes could only stop shrinking at √5 itself.

### the_gap 03 <!-- #29d6cd -->
So it drops below √3, the flips stop, and it settles at +1 or −1. 1.8 went to −1. Does the whole gap?

### the_gap 04 <!-- #f94856 -->
Let's not guess. Color every start from 0 to 2.4 by where it ends up.
> screen: FadeOut, FadeIn

### the_gap 05 <!-- #6af913 -->
Below √3, all teal, as we proved. But the gap is not all gold. Near √5 there are stripes.
> screen: Create

### the_gap 06 <!-- #f4f39c -->
Zoom in: gold, teal, gold, teal, each stripe thinner than the last, squeezed against √5.
> screen: Create, FadeIn, FadeIn

### the_gap 07 <!-- #e3b669 -->
Where do these stripes come from? Let's follow one start from each: 2.0, 2.2 and 2.23.

### the_gap 08 <!-- #7e7d87 -->
We plot only the size of each value, show its sign by color, and count the flips.
> screen: FadeIn, FadeIn, FadeIn, FadeIn, FadeIn, FadeIn, LaggedStart, FadeIn

### the_gap 09 <!-- #14ccb1 -->
Step by step: the sizes move left, and the colors alternate.
> screen: *step

### the_gap 10 <!-- #a62ccb -->
2.0 flips once before dropping below √3. 2.2 flips twice, and 2.23 three times.
> screen: LaggedStart

### the_gap 11 <!-- #b50fe1 -->
So 2.0 ends at −1, 2.2 at +1, and 2.23 at −1: one for each stripe.
> screen: LaggedStart

### the_gap 12 <!-- #574ffe -->
From a positive start, an odd number of flips ends at −1, and an even number at +1.
> screen: FadeIn

### the_gap 13 <!-- #d42800 -->
So the stripes are flip counts. Where exactly does the count change from one to two?

## 09 · first_boundary — The first stripe edge b₁

> **Purpose.** Find where the first stripe starts: p(b₁) = −√3, so b₁³ − 3b₁ = 2√3, b₁ ≈ 2.148.
> **Tone.** Slow; this is where the algebra starts to feel heavy, so keep the picture on screen.

### first_boundary 01 <!-- #a00c9d -->
One flip or two? One step must land inside √3. The cutoff is where p(x) is exactly −√3. Call it b1.
> screen: Create, FadeIn, GrowFromCenter, Create, FadeIn, FadeIn, FadeIn

### first_boundary 02 <!-- #cdd1dc -->
p is decreasing here, so every x between √3 and b1 lands between −√3 and 0: one flip, then −1.
> screen: Create, Create, FadeIn

### first_boundary 03 <!-- #4b26b3 -->
To pin b1 down, solve b cubed minus 3b = 2√3. Trying values until it fits gives about 2.148.
> screen: FadeIn

### first_boundary 04 <!-- #e223f4 -->
Both 1.8 and 2 are in this piece. In fact p(2) is exactly −1.
> screen: GrowFromCenter, FadeIn, Flash

## 10 · basins — The mirror argument (the aha)

> **Purpose.** p maps each stripe onto the mirror image of the previous one, and p is odd, so the fates alternate −1, +1, −1, …  Check with 2.2.
> **Tone.** This is the payoff. Let the animation of piece 2 sliding onto piece 1 play in silence for a beat.

### basins 01 <!-- #bd1554 -->
Same idea one level up: b2 is the start that lands exactly on −b1, b3 lands exactly on −b2, and so on.
> screen: Write

### basins 02 <!-- #1ef215 -->
b1 is about 2.148, b2 about 2.221, b3 about 2.234: the stripe edges, creeping up toward √5.
> screen: FadeIn

### basins 03 <!-- #34fa0e -->
Cut the gap at these points, and watch where one step of p sends each piece.
> screen: FadeIn, FadeIn, FadeIn, FadeIn

### basins 04 <!-- #17f4f7 -->
The first piece lands inside √3, on the negative side. From there it slides to −1.
> screen: bar.rects[0].animate.set_fill, Indicate

### basins 05 <!-- #74b7de -->
The second piece lands exactly on the first piece, flipped to the negative side.
> screen: Indicate

### basins 06 <!-- #c2c9b2 -->
p is odd, so a flipped start has a flipped fate. The first piece's −1 becomes +1.
> screen: FadeOut, bar.rects[1].animate.set_fill

### basins 07 <!-- #0136cc -->
Check with 2.2, in the second piece. One step gives −2.02. Its size, 2.02, is in the first piece.
> screen: FadeIn

### basins 08 <!-- #5fc89b -->
A positive 2.02 would end at −1. This one is negative, so the mirror image: 2.2 ends at +1.
> screen: Indicate

### basins 09 <!-- #a8a40a -->
The third maps onto the mirror of the second: −1 again. And so on, alternating.
> screen: bar.rects[2].animate.set_fill, Indicate, *[bar.rects[k].animate.set_fill

### basins 10 <!-- #af3845 -->
So the n-th piece flips n times: odd n ends at −1, even n at +1. That is the striped picture.
> screen: FadeOut, FadeIn

### basins 11 <!-- #92eb2e -->
The pieces pile up against √5. Zoom in, and the same pattern repeats again and again.
> screen: FadeOut

### basins 12 <!-- #24e249 -->
Each piece is about a sixth of the one before, because the slope of p at √5 is −6.
> screen: FadeIn

### basins 13 <!-- #d57783 -->
So between √3 and √5 there are infinitely many basins, alternating −1, +1, −1, +1, and so on.
> screen: Indicate

## 11 · boundary_points — The edges converge to √5

> **Purpose.** b_n climb to √5; stripes shrink by a factor 6 each time because p′(√5) = −6; the edges reach ±√3 exactly, then 0.

### boundary_points 01 <!-- #556617 -->
And the stripe edges themselves? b1 goes to −√3 in one step, and then to 0.
> screen: FadeIn, FadeIn, GrowFromCenter

### boundary_points 02 <!-- #2f7475 -->
b2 takes two steps to reach √3, b3 takes three. Then both drop to 0.
> screen: FadeIn, FadeIn, *[GrowFromCenter

### boundary_points 03 <!-- #78d3f4 -->
Every stripe edge hits ±√3 exactly after a few steps, then sits on 0, the unstable fixed point.
> screen: LaggedStart

### boundary_points 04 <!-- #23fca7 -->
But they are single points: nudge one slightly, and it falls into a basin on either side.

## 12 · summary — The complete answer

> **Purpose.** One table of fates for every starting σ. Say it once, plainly.

### summary 01 <!-- #c9f039 -->
Here is the full answer to part (e).
> screen: FadeIn, Create

### summary 02 <!-- #4bf71a -->
Below √3, σ goes to +1. Exactly at √3, it lands on 0.
> screen: FadeIn, FadeIn

### summary 03 <!-- #eed3f2 -->
Between √3 and √5, the stripes alternate −1 and +1 by flip count; their edges go to 0.
> screen: FadeIn, FadeIn

### summary 04 <!-- #f19389 -->
At √5 it bounces forever, and beyond √5 it diverges.
> screen: FadeIn, FadeIn

## 13 · back_to_matrix — So what do we do with W?

> **Purpose.** Close the loop: divide W by its Frobenius norm so every singular value is below √3, then iterate; all σ go to 1 and the ellipse becomes a circle.
> **Tone.** Practical and short. End on the picture of the circle.

### back_to_matrix 01 <!-- #1aee9d -->
Back to the matrix. A real W can have singular values anywhere, some far above √5.
> screen: Create, FadeIn, FadeIn, LaggedStart

### back_to_matrix 02 <!-- #575d1e -->
This one at 2.9 would blow up. So before iterating, W must be scaled down.
> screen: Create, FadeIn

### back_to_matrix 03 <!-- #2379f9 -->
A common choice: divide by the Frobenius norm. It is never smaller than the largest singular value.
> screen: FadeOut, Write

### back_to_matrix 04 <!-- #e1af02 -->
Here that norm is the square root of the sum of squares, about 3.45. Divide every σ by it.
> screen: FadeIn

### back_to_matrix 05 <!-- #e0a44c -->
After scaling, every singular value sits between 0 and 1, safely below √3.
> screen: *[d.animate.move_to

### back_to_matrix 06 <!-- #2d0430 -->
Now each one walks to +1. Small ones take longer, but all arrive, and W becomes U V transpose.
> screen: FadeIn

### back_to_matrix 07 <!-- #63dad6 -->
The ellipse became a circle. All it took was a cubic built from two simple wishes.
