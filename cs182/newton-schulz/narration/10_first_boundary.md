<!-- 副本：cs182/newton-schulz/narration.md 中 "## 10 · first_boundary" 的独立编辑文件。主源仍为 narration.md。 -->

## 10 · first_boundary — Fold the curve, find b₁

> **Purpose.** Turn the problem into one about sizes only, and find where the first stripe ends: |p(b₁)| = √3, b₁ ≈ 2.148.
> **Logic chain.** Sign and size together are messy → the mirror rule lets us separate them: the size follows |x| → |p(x)|, and every step from outside √3 is one flip → fold the curve up (the graph of the size after one step) → compare with the diagonal: below it between √3 and √5 (|p(x)| < |x|, shrinks), above it beyond √5 (grows), they meet at √5 → the cobweb works on the folded picture (2.2 → 2.02 → 1.11) → zoom into the gap → one flip exactly when the first step lands below the level √3 → the folded curve reaches that level at one start: b₁ → everything from √3 to b₁ is the first stripe (one flip, ends at −1) → *where is b₁?* b(b² − 3)/2 = √3, try 2.1 and 2.2, close in on 2.148 → check 1.8, 2.0, 2.2.
> **Tone.** Slow; the folded picture is the tool for the rest of the section.
> **Polish pass (novice check).** "Fold" is shown, not only said. The comparison is always "size after" against "size before" (the diagonal), never the line y = −x. The name b is explained (b for boundary). Trying values is shown with two actual tries.
> **Numbers used.** 2√3 ≈ 3.46. 2.1³ − 3·2.1 = 2.96. 2.2³ − 3·2.2 = 4.05. b₁ ≈ 2.148.
> **Animation.** Mirror rule and the two bookkeeping lines; the part of the curve below the axis flips up; shrink/grow parts coloured, dot at √5; cobweb on the folded curve; then the stretched picture of the gap (x from 1.65 to 2.3) with the level line √3, the point b₁, the first stripe on the x-axis and where it lands on the y-axis; the equation and the two tries.

### first_boundary 01 <!-- #8c9a27 -->
Following the sign and the size together on this picture gets messy. But the mirror rule lets us take them apart. A negative value moves exactly like its positive twin, with the sign flipped. So the size follows a rule of its own. The next size is the size of p of x. And the sign we can simply count. Every step that starts outside square root of three is one flip.

### first_boundary 02 <!-- #81ad2b -->
So fold the picture. We only need positive sizes, so look at the right half. Wherever the curve dips below the axis, flip that part up. This folded curve answers one question. If the size is x now, what is the size after one step?

### first_boundary 03 <!-- #0b2bd6 -->
Now compare it with the diagonal, where the size would stay the same. Between square root of three and square root of five, the folded curve is below the diagonal. The size after the step is smaller than the size before. Beyond square root of five it is above the diagonal, and the size grows. They meet exactly at square root of five.

### first_boundary 04 <!-- #5dfaf7 -->
And the cobweb works on the folded picture too. Start at two point two. Up to the folded curve, at two point zero two. Across to the diagonal, and then to the curve again, at one point one one. Now we are inside, and the size climbs to one. Two of these steps started outside square root of three. So two flips, and the sign ends up positive.

### first_boundary 05 <!-- #3c6e67 -->
Now zoom in on the gap, and stretch it sideways so we can see. When does a start need exactly one flip? When its first step already lands inside, at a size below square root of three. So draw that level as a horizontal line. The folded curve climbs through it at one point. Call that start b one, b for boundary. A start to the left of b one lands below the line. One flip, and it is inside, on the negative side, so it ends at minus one. This is the first stripe.

### first_boundary 06 <!-- #cb1a5b -->
Where is b one exactly? Its size after one step must be square root of three. With the size factor, that is b, times b squared minus three, over two, equals square root of three. Multiply by two, and we get b cubed, minus three b, equals two times square root of three, which is about three point four six. This has no tidy answer, so try values. Two point one gives two point nine six, which is too small. Two point two gives four point zero five, which is too big. Closing in between them gives about two point one four eight.

### first_boundary 07 <!-- #6b9f0a -->
That fits what we saw. One point eight and two point zero are both below b one, in the first stripe, and both ended at minus one. Two point two is above b one. Its first step did not get inside, and it needed a second flip.
