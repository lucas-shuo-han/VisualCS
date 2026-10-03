<!-- 副本：cs182/newton-schulz/narration.md 中 "## 06 · slopes" 的独立编辑文件。主源仍为 narration.md。 -->

## 06 · slopes — Why ±1 attract and 0 repels

> **Purpose.** Stability from the derivative. Linearize: p(x*+e) ≈ x* + p′(x*)·e.
> **Logic chain.** Paths leave zero and enter one → *why?* → we already know the answer at one: in scene 03 we put in 1+e and made the error multiplier zero → do the same at zero: p(e) ≈ 1.5e, so the error is multiplied by 1.5 and grows → this is the slow climb we watched from 0.1 → *what is this multiplier in the picture?* → the slope of the curve at the fixed point → back at one the slope is zero, so only the e² term is left and the error collapses → hilltop and valleys.
> **Beats.** p′(0)=1.5 pushes away; p′(±1)=0 (the wish from scene 3) squares the error, so convergence is very fast.
> **Tone.** Nothing new is introduced. This scene repeats the 1+e calculation of scene 03 at a second point and then gives it a picture.
> **Polish pass (novice check).** No "p prime" and no word "derivative". The slope is explained as rise over run on the zoomed-in curve. The 1.5 multiplier is checked against the 0.1 chain from scene 04 (0.1, 0.15, 0.22, 0.33). The "error gets squared" claim is now derived: the e² terms we dropped in scene 03 are all that is left, and they add up to about 1.5 e².
> **Code changes needed (later).** 02 is the calculation p(e) = 1.5e − 0.5e³ ≈ 1.5e near zero. 03 is the zoom-in with a rise-over-run triangle. 05 shows p(1+e) = 1 − 1.5e² − 0.5e³.
> **Numbers used.** 0.05 → 0.075 → 0.112. Errors from 1.2: 0.2 → 0.064 → 0.006.

### slopes 01 <!-- #bcc631 -->
Why does one pull values in, while zero pushes them away? For one, we already know. When we built p, we put in one plus a small error e, and we chose p so that one step multiplies that error by zero.
> screen: Write

### slopes 02 <!-- #527e99 -->
So do the same thing at zero. A value near zero is just a small error e. Put it into p, and we get one point five e, minus one half e cubed. For a small e, the cube is tiny. If e is zero point one, e cubed is only zero point zero zero one. So p gives about one point five e.
This time, one step multiplies the error by one point five, and the error grows.
> screen: FadeIn

### slopes 03 <!-- #c8d4c9 -->
We have seen this growth already. Zero point one went to zero point one five, then zero point two two, then zero point three three. Each value is about one and a half times the one before. That is why zero pushes values away.
On the graph, this multiplier is the slope of the curve. Zoom in at zero, and the curve looks like a straight line. Move e to the right, and it rises by one point five e. Rise over run is one point five.
> screen: Indicate

### slopes 04 <!-- #47c1ea -->
So here is the rule. Near a fixed point, each step multiplies the error by the slope of the curve there. If the slope is bigger than one in size, the error grows and values are pushed away. If it is smaller than one, the error shrinks and values are pulled in.
At zero the slope is one point five, and zero point zero five drifts to zero point zero seven five, then zero point one one, and on.
> screen: Create, FadeIn

### slopes 05 <!-- #640341 -->
At one, the multiplier is zero, so the slope is zero. The curve is flat at the top of its hump. That is our second wish, seen as a picture.
But an error cannot vanish completely in one step. When we built p, we dropped the terms with e squared, because they were small. Now they are all that is left. Worked out, the new error is about one and a half times e squared.
Start at one point two. The error goes from zero point two, to zero point zero six, to zero point zero zero six. Each step roughly squares it, which is far faster than shrinking by a fixed factor. The same calculation at minus one gives the same result.
> screen: FadeOut, Create, FadeIn

### slopes 06 <!-- #384fc8 -->
So zero is unstable, like the top of a hill, where the smallest push sends you rolling away. One and minus one are stable, like the bottoms of two valleys, where everything nearby rolls in.
> screen: FadeIn
