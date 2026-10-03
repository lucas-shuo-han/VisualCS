<!-- 副本：cs182/newton-schulz/narration.md 中 "## 09 · the_gap" 的独立编辑文件。主源仍为 narration.md。 -->

## 09 · the_gap — Follow three starts into the gap

> **Purpose.** See, on the cobweb picture, that starts between √3 and √5 do not all end the same way, and why: the number of flips before the value gets inside √3.
> **Logic chain.** In the gap every step flips and the size factor is below one → *so the size keeps shrinking; it must get inside √3, and inside we know everything (positive → +1, negative → −1)* → so just follow a start until it is inside and see on which side it arrives → cobweb for 2.0 (one flip, −1), 2.2 (two flips, +1), 2.23 (three flips, −1) → odd number of flips ends at −1, even at +1 → three starts are not the whole story: colour every start (the strip is the overview) → stripes → two open questions: where does the flip count change, and do the stripes fill the whole gap?
> **Tone.** Exploring. Nothing is claimed before it has been seen on the cobweb.
> **Polish pass (novice check).** Each start is followed step by step with its numbers; "inside" always means inside √3. The colour strip comes only after the three starts, as the whole picture, and its colours are named before it is read.
> **Numbers used.** 2.0 → −1. 2.2 → −2.02 → +1.11 → … → +1. 2.23 → −2.20 → +2.02 → −1.10 → … → −1.
> **Animation.** The p graph with the gap marked; the plan (inside √3: teal half, gold half); three cobwebs, each segment drawn when its number is said, with one row per start in the panel; the odd/even rule; then the colour strip and the zoom next to √5.

### the_gap 01 <!-- #b6b760 -->
So below square root of three, everything goes to one, and beyond square root of five, everything explodes. That leaves the gap between them. In the gap, every step flips the sign. And the size factor is below one, so every step also makes the size smaller.

### the_gap 02 <!-- #7b3eda -->
That suggests a plan. If the size keeps getting smaller, then sooner or later it drops below square root of three. And inside square root of three we already know everything. A positive value goes to plus one. By the mirror rule, a negative value goes to minus one. So we only have to follow a start until it gets inside, and see on which side it arrives.

### the_gap 03 <!-- #cfa696 -->
Try it on the cobweb picture. Start at two point zero. Go down to the curve, which gives minus one. Then across to the diagonal. Minus one is inside, on the negative side, and it is already a fixed point. So two point zero ends at minus one, after one flip.

### the_gap 04 <!-- #e5a13d -->
Now two point two. Down to the curve, at minus two point zero two. That is smaller in size than two point two, but it is still outside. So go across to the diagonal and step again. This time the curve sends it up, to plus one point one one. Now it is inside, on the positive side, and from there it settles at plus one. Two flips, and a different ending.

### the_gap 05 <!-- #1a1355 -->
And two point two three, just a little further out. Minus two point two zero. Then plus two point zero two. Then minus one point one zero. It takes three flips to get inside, it arrives on the negative side, and it ends at minus one.

### the_gap 06 <!-- #940710 -->
So the starts in the gap do not all end the same way. What matters is how many flips it takes to get inside. Every start here is positive, and each flip changes the sign. After an odd number of flips the value arrives negative, and ends at minus one. After an even number it arrives positive, and ends at plus one.

### the_gap 07 <!-- #e42be0 -->
Three starts are not the whole story, so here is every start at once. Take each start from zero to two point four, run the iteration, and color it by where it ends. Teal means plus one, gold means minus one, and red means it explodes.

### the_gap 08 <!-- #b4b6e4 -->
Below square root of three it is all teal, as we showed. The gap begins gold. That is where two point zero sits, with its one flip. Then comes a thin teal stripe, which holds two point two. And then more stripes, each thinner than the last, squeezed up against square root of five.

### the_gap 09 <!-- #610196 -->
So each stripe is a flip count. One flip, two flips, three flips, and so on. Two things are still open. Where exactly does one flip turn into two, and two into three? And do these stripes really fill the whole gap, all the way up to square root of five?
