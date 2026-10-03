<!-- 副本：cs182/newton-schulz/narration.md 中 "## 08 · too_big" 的独立编辑文件。主源仍为 narration.md。 -->

## 08 · too_big — Try 3, and the size factor

> **Purpose.** Discover √5 as the boundary between shrinking and growing, by comparing |p(x)| with |x|.
> **Logic chain.** 1.8 flipped but still settled → *is a flip all that ever happens?* → 3 explodes → *both flip, so what differs?* size: 1.8 came out smaller, 3 came out bigger → narrow it down: 2.0 still smaller, 2.3 bigger → *where exactly is the turning point?* → compare the size after with the size before: |p(x)| = |x| · (x² − 3)/2, so one step multiplies the size by the "size factor" → check the factor at 2.0 (0.5) and 2.3 (1.14) → factor = 1 gives x² = 5 → at √5 it bounces forever, past it it diverges.
> **Tone.** The size factor is the one new idea; it is reused all through scenes 09–12, so say it slowly.
> **Polish pass (novice check).** The two steps from 3 are computed aloud. The word "size" is defined once (the number without its sign). The size factor is read off the factored form from scene 07, then checked on the two starts already tried, before it is used to find √5. The bounce at √5 is checked with the factored form. "Period two orbit" is kept as a name only, after the plain description.
> **Numbers used.** p(3) = −9; p(−9) = 351. p(2) = −1. p(2.3) = −2.63. Factor at 2.0: (4 − 3)/2 = 0.5. Factor at 2.3: (5.29 − 3)/2 = 1.145. 2.3 → −2.63 → 5.18 → −61.8.
> **Animation.** No y = −x line any more. Beat 05: |p(x)| = |x| · (x²−3)/2 builds up under the factored form, the factor gets a box and the name. Beat 06: one row per start. Beat 07: factor = 1 ⟺ x² = 5, the √5 tick, then the curve is coloured (shrink part, grow part).

### too_big 01 <!-- #1df1e8 -->
So past square root of three, the first step flips the sign. One point eight flipped and still settled, at minus one. Maybe a flip is all that ever happens. Test that with a much bigger start, three.

### too_big 02 <!-- #9b0755 -->
Three halves of three is four point five, and half of three cubed is thirteen point five. Subtract, and we get minus nine. It flipped, as expected. Now the next step. By the mirror rule, minus nine does what nine does, with the sign flipped. Nine goes to thirteen point five minus three hundred sixty four point five, which is minus three hundred fifty one. So minus nine goes to plus three hundred fifty one.
It flips every time, and it gets bigger every time. This one explodes.

### too_big 03 <!-- #5ff1d3 -->
Both one point eight and three flip, so the difference must be in the size, meaning the number without its sign. One point eight came out at size zero point two, smaller than it went in. Three came out at size nine, bigger than it went in.
So somewhere between them, shrinking turns into growing. Narrow it down. Two point zero goes to minus one, so its size is one. That is still smaller.

### too_big 04 <!-- #292d3e -->
But two point three goes to minus two point six three. Its size is bigger than where it started. So the turning point is somewhere between two point zero and two point three.

### too_big 05 <!-- #26b539 -->
Where exactly is the turning point? Compare the size after a step with the size before. Use the factored form. p of x is x over two, times three minus x squared. So the size of p of x is the size of x, times the size of three minus x squared, over two. Past square root of three, that second part is x squared minus three, over two. Call it the size factor. Each step multiplies the size by this factor.

### too_big 06 <!-- #82b56f -->
Check it with the starts we tried. At two point zero, the factor is four minus three, over two, which is one half. And two did go to size one. At two point three, the factor is about one point one four, and two point three did come out bigger. So a factor below one means flip and shrink. A factor above one means flip and grow.

### too_big 07 <!-- #25d1c3 -->
The turning point is where the factor is exactly one. That means x squared minus three equals two, so x squared equals five. The turning point is square root of five, about two point two four, and it does sit between two point zero and two point three. On the curve, between square root of three and square root of five a step shrinks the size, and beyond square root of five it grows.

### too_big 08 <!-- #e6b98a -->
What happens exactly at square root of five? Use the factored form. x over two, times three minus five, is minus x. So square root of five goes to minus square root of five. By the mirror rule, that goes straight back to plus square root of five. On the picture, the path becomes a square.

### too_big 09 <!-- #3840ae -->
So square root of five neither settles nor explodes. It jumps back and forth between plus and minus square root of five forever. This is called a period two orbit, because it repeats every two steps.

### too_big 10 <!-- #d9c1b8 -->
And past square root of five, every step flips and grows. Two point three goes to minus two point six three, then five point one eight, then minus sixty one point eight. Like three, it explodes.
