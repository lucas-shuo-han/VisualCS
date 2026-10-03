<!-- 副本：cs182/newton-schulz/narration.md 中 "## 14 · back_to_matrix" 的独立编辑文件。主源仍为 narration.md。 -->

## 14 · back_to_matrix — So what do we do with W?

> **Purpose.** Close the loop: divide W by its Frobenius norm so every singular value is below √3, then iterate; all σ go to 1 and the ellipse becomes a circle.
> **Logic chain.** Only "below √3" is safe → *but a real W has singular values anywhere* → so shrink W first → *does shrinking change the answer?* no: dividing W by a number only divides the σ's, U and Vᵀ stay → *divide by what?* the largest σ would be ideal, but finding it needs the SVD → the Frobenius norm is cheap and never smaller than the largest σ → every σ now sits in (0, 1] → all walk to one → W becomes U Vᵀ, the circle from scene 1.
> **Tone.** Practical and short. End on the picture of the circle.
> **Polish pass (novice check).** Says why dividing W is harmless (the target U Vᵀ does not depend on the sizes). Says how the Frobenius norm is computed, why it is cheap, and why it is at least as large as the biggest σ (its square already contains that σ squared, plus more). The 2.9 example is carried through the division (2.9 / 3.45 = 0.84). The slow start of small σ's is tied to the factor 1.5 from scene 06. Second read as a novice: "the step" in beat 06 was ambiguous (number step or matrix step), so the matrix step from scene 03 is now said in full, with the reminder that it sends every σ through p once; "the middle is now all ones" links back to U Σ Vᵀ. "Gold stripe" relies on the colour strip of scene 09 (gold = ends at −1).
> **One fact taken on trust.** "The sum of the squared entries of W equals the sum of the squared singular values" is stated, not shown. It is standard, and proving it would start a new topic.
> **Code changes needed (later).** If the on-screen singular values differ from the ones implied here (largest 2.9, norm 3.45), change the two numbers in beats 02, 04, 05.

### back_to_matrix 01 <!-- #8a4aa3 -->
We wanted every singular value to end at one, and that only happens for starts below square root of three. But a real W can have singular values anywhere, some of them far above square root of five.
> screen: Create, FadeIn, FadeIn, LaggedStart

### back_to_matrix 02 <!-- #989d50 -->
This one, at two point nine, would explode. And one that sits in a gold stripe would end at minus one, with its direction reversed. So before we iterate, we have to bring every singular value down.
That is easy to do. Divide W by a number, and every singular value is divided by that number, while U and V transpose stay exactly the same. Our target, U times V transpose, does not change at all.
> screen: Create, FadeIn

### back_to_matrix 03 <!-- #22d274 -->
Which number? Dividing by the largest singular value would be ideal, because then everything is at one or below. But finding the largest singular value takes the very SVD we are trying to avoid.
There is a cheap stand-in, called the Frobenius norm. Square every entry of W, add them all up, and take the square root. That only needs the entries, so it costs almost nothing.
And it is big enough. The sum of the squared entries always equals the sum of the squared singular values. That sum already contains the largest one squared, plus more. So its square root, the Frobenius norm, is never smaller than the largest singular value.
> screen: FadeOut, Write

### back_to_matrix 04 <!-- #39d19b -->
Here the Frobenius norm comes out to about three point four five, a bit more than our largest singular value, two point nine. Divide every sigma by it.
> screen: FadeIn

### back_to_matrix 05 <!-- #2f01eb -->
Two point nine becomes zero point eight four, and the others are smaller still. Now every singular value sits between zero and one, safely below square root of three.
> screen: *[d.animate.move_to

### back_to_matrix 06 <!-- #777d57 -->
Now apply our matrix step, three halves W, minus one half W, W transpose, W, again and again. It needs nothing but matrix products. And each time, every singular value goes through p once.
So each singular value climbs to plus one. The small ones start slowly, growing by about one and a half times per step as zero point one did, but they all arrive.
And all along, U and V transpose never changed. So the middle is now all ones, and W has become U times V transpose.
> screen: FadeIn

### back_to_matrix 07 <!-- #40417c -->
The ellipse has become a circle. All it took was matrix products, and a cubic built from two simple wishes.
