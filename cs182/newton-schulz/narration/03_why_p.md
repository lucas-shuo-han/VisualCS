<!-- 副本：cs182/newton-schulz/narration.md 中 "## 03 · why_p" 的独立编辑文件。主源仍为 narration.md。 -->

## 03 · why_p — You could have invented p (design)

> **Purpose.** Let the viewer invent p. The polynomial is never announced. It falls out of one constraint (only matrix products are cheap) and one calculation (W Wᵀ W = U Σ³ Vᵀ).
> **Logic chain.** Each beat answers the question the previous beat leaves open:
> 1. We want U Vᵀ, but the SVD is slow. → *What is cheap, then?*
> 2. Matrix multiplication is cheap. → *What can we build from W with products alone?*
> 3. So just start multiplying. The only matrix we have is W. W·W fails on shape, so try Wᵀ W. → *What does that product give?* (Do not list "the rules of the game" here. Scaling and adding only appear in beat 09, where they are obvious.)
> 4. Through the SVD: Wᵀ W = V Σ² Vᵀ. U is lost, so this is a failure. One more W gives W Wᵀ W = U Σ³ Vᵀ, and both rotations are back. → *Why did three work when two did not?*
> 5. An odd number of copies keeps U and Vᵀ and only changes each σ. So we get σ, σ³, σ⁵, … → *How do we combine them to reach U Vᵀ?*
> 6. A mix is an odd polynomial p(σ). The matrix problem is now a number problem. → *Which p?*
> 7. No p works in one step, so ask for a step that gets closer, and repeat. One term only rescales, so take two. → *What should a and b be?*
> 8. Both wishes are derived from "repeat until it settles at one", not announced. (a) To settle at one, one must stay: p(1)=1, so a+b=1. (b) Near one it must get closer: p(1+e) ≈ 1 + (a+3b)e, so the error is multiplied by a+3b; the best is zero. Then "two wishes, two unknowns" → a = 3/2, b = −1/2.
> 9. The question for the rest of the video: σ → p(σ) → p(p(σ)) → … → ?
> **Tone.** 'You could have done this yourself.' The viewer should feel the polynomial was forced on us, not picked. Slow on the two wishes.
> **Polish pass (novice check).** Every step a first-time viewer cannot do alone is now spoken: why W·W does not fit, what Wᵀ is in SVD form, why Uᵀ U cancels, what "diagonal" buys us (with the numbers 1.3 and 0.5 from scene 01), why odd products keep working, how U and Vᵀ factor out of a sum, why one step cannot be enough, why one term is not enough, where (1+e)³ ≈ 1+3e comes from, and how the two equations are solved. The sentence "the curve is flat at one" was removed from beat 11, because no graph exists yet; scene 06 makes that link.
> **Your original notes for 02–03 (kept for reference).** "what operation for matrix is cheap? maybe just operate on x itself because it is natural and you don't need to compute anything for each specific matrix / polynomials are a great class of funcs that is easy to compute and can represent a lot / what kind of polynomials? / A constant would treat every direction the same, but Muon must handle each direction on its own." The last idea is now in beat 09, as the reason one term is not enough.
> **Code changes needed (later).** 03 shows two attempts (W·W fails on shape with a 3×2 example, then Wᵀ W). 04 expands Wᵀ W = V Σ Uᵀ U Σ Vᵀ = V Σ² Vᵀ and marks it as a failure (U gone). 05 multiplies by W on the left to get U Σ³ Vᵀ. 06 shows diag(1.3, 0.5)³ = diag(2.2, 0.125). 07 compares the two attempts and attaches one more Wᵀ W. 09 shows U(aΣ + bΣ³ + …)Vᵀ, then the two-term candidate. 11 shows p(1+e) = a(1+e) + b(1+e)³ ≈ (a+b) + (a+3b)e. 12 shows the solved p and the matrix step 3/2 W − 1/2 W Wᵀ W.
> **Voice.** The coefficients a and b are written as letters in the caption and respelled in `speak:` as "ay" and "bee", so the voice does not read "a" as the article. Only the coefficient is respelled; the article in "a sigma", "a number" stays "a". If a caption changes, change its `speak:` line too.
> **Open choices.** Beats 09 and 11 are long. Each could be split into two or three `say()` calls in code without changing a word.

### why_p 01 <!-- #f2373c -->
We want every singular value to be one. The SVD hands us exactly that. Write W as U, sigma, V transpose, keep the two rotations, and replace every stretch in sigma with one. What remains is just U times V transpose.
But computing an SVD is a long procedure, and it runs slowly on a GPU.

### why_p 02 <!-- #cb23f8 -->
So we want that same result, U times V transpose, without ever computing the SVD.
What can a GPU do cheaply? It can multiply matrices. That is the one thing it is built for.

### why_p 03 <!-- #dd0e65 -->
So let's start multiplying. The only matrix we have is W, so the first thing to try is W times W.
But two matrices can only be multiplied when the number of columns of the first matches the number of rows of the second. If W has three rows and two columns, W times W does not fit.
The transpose swaps rows and columns. So W transpose times W always fits. Let's see what that product gives.
> screen: Write

### why_p 04 <!-- #64d094 -->
To see it, write W with its SVD, as U, sigma, V transpose. Transposing a product reverses the order, so W transpose is V, sigma, U transpose.
Now put them side by side. In the middle, U transpose meets U. The transpose of a rotation is the same rotation done backwards, and a rotation followed by its reverse does nothing. So the pair cancels.
What is left is V, sigma times sigma, V transpose. That is not what we want. Our target has U on the left, and here U has disappeared.
> screen: FadeIn, Write, FadeIn

### why_p 05 <!-- #32efd2 -->
So bring U back. Multiply by W one more time, on the left. Now the V transpose at the end of W meets the V at the start of our product, and that pair cancels too.
What survives is U on the left, V transpose on the right, and sigma three times in between. This time both rotations are back where they belong.
> screen: VGroup, Write

### why_p 06 <!-- #936ed4 -->
And the middle is easy to read. Sigma is diagonal, which means it only holds the singular values, one for each direction. Multiplying diagonal matrices just multiplies the matching entries.
So sigma three times in a row cubes each singular value on its own. In our example, one point three becomes about two point two, and zero point five becomes zero point one two five. No direction disturbs another.

### why_p 07 <!-- #bd8c5d -->
Look back at the two attempts. Two copies of W lost a rotation. Three copies kept both, and only the singular values changed.
And we can keep going. Attach another W transpose times W, and the same cancelling happens again. U and V transpose stay where they are, and the middle gains two more sigmas.

### why_p 08 <!-- #a4b47f -->
So the products with an odd number of copies are the ones we can use. W itself carries sigma. Three copies carry sigma cubed. Five copies carry sigma to the fifth, and so on.
> screen: LaggedStart

### why_p 09 <!-- #6a3be5 -->
Every one of these products has the same U on the left and the same V transpose on the right. So if we multiply each product by a number and add them up, U and V transpose factor out, and only the middle is a sum.
In that middle, each singular value becomes a number times sigma, plus a number times sigma cubed, and so on. A sum of powers like this is a polynomial. Call it p.
So turning W into U times V transpose now means one thing. We need a p that sends every sigma to one.
Can p do that in a single step? Then it would have to give one for every input. But p is made of powers of sigma, so a tiny sigma always gives a tiny output. One step is not enough.
So we ask for less. One step only has to bring sigma closer to one, and then we apply p again and again.
Which p? Every extra term costs more matrix products, so we want as few as possible. One term alone, a times sigma, only rescales every singular value by the same number, so the ellipse stays an ellipse.
So take two terms, a times sigma plus b times sigma cubed.
speak: Every one of these products has the same U on the left and the same V transpose on the right. So if we multiply each product by a number and add them up, U and V transpose factor out, and only the middle is a sum. In that middle, each singular value becomes a number times sigma, plus a number times sigma cubed, and so on. A sum of powers like this is a polynomial. Call it p. So turning W into U times V transpose now means one thing. We need a p that sends every sigma to one. Can p do that in a single step? Then it would have to give one for every input. But p is made of powers of sigma, so a tiny sigma always gives a tiny output. One step is not enough. So we ask for less. One step only has to bring sigma closer to one, and then we apply p again and again. Which p? Every extra term costs more matrix products, so we want as few as possible. One term alone, ay times sigma, only rescales every singular value by the same number, so the ellipse stays an ellipse. So take two terms, ay times sigma plus bee times sigma cubed.
> screen: odd.animate.scale, FadeIn

### why_p 10 <!-- #8b28c8 -->
What should a and b be? We want the repeated steps to settle at one. So a sigma that has reached one must stay there, or the steps would never settle.
Put sigma equals one into p. One cubed is still one, so p gives a plus b. For one to stay at one, a plus b must equal one. Call this our first wish.
speak: What should ay and bee be? We want the repeated steps to settle at one. So a sigma that has reached one must stay there, or the steps would never settle. Put sigma equals one into p. One cubed is still one, so p gives ay plus bee. For one to stay at one, ay plus bee must equal one. Call this our first wish.
> screen: FadeIn

### why_p 11 <!-- #915b49 -->
Staying at one is not enough. A sigma that is only close to one has to move closer. So take a sigma that misses one by a small error e, and put one plus e into p.
We need the cube of one plus e. Multiplied out, it is one, plus three e, plus terms with e squared and e cubed. When e is small, those last terms are far smaller still, so we drop them. For example, one point one cubed is one point three three, very close to one point three.
So p gives a times one plus e, plus b times one plus three e. Collect the pieces, and that is a plus b, plus a plus three b times e.
The first piece, a plus b, is one, by our first wish. So p gives one, plus a plus three b times e. We went in with an error of e, and we came out with an error of a plus three b times e.
One step multiplies the error by a plus three b. We want the error to shrink, and the most it can shrink is all the way to nothing. So our second wish is that a plus three b equals zero.
speak: Staying at one is not enough. A sigma that is only close to one has to move closer. So take a sigma that misses one by a small error e, and put one plus e into p. We need the cube of one plus e. Multiplied out, it is one, plus three e, plus terms with e squared and e cubed. When e is small, those last terms are far smaller still, so we drop them. For example, one point one cubed is one point three three, very close to one point three. So p gives ay times one plus e, plus bee times one plus three e. Collect the pieces, and that is ay plus bee, plus, ay plus three bee, times e. The first piece, ay plus bee, is one, by our first wish. So p gives one, plus, ay plus three bee, times e. We went in with an error of e, and we came out with an error of, ay plus three bee, times e. One step multiplies the error by ay plus three bee. We want the error to shrink, and the most it can shrink is all the way to nothing. So our second wish is that ay plus three bee equals zero.
> screen: FadeIn

### why_p 12 <!-- #25c434 -->
Two wishes and two unknowns, which is exactly enough. The second wish says a equals minus three b. Put that into the first, and minus three b plus b equals one, so b is minus one half. Then a is three halves.
So p of sigma is three halves sigma, minus one half sigma cubed. For the matrix, one step is three halves W, minus one half W times W transpose times W. That is the Newton–Schulz step, and you could have invented it yourself.
speak: Two wishes and two unknowns, which is exactly enough. The second wish says ay equals minus three bee. Put that into the first, and minus three bee plus bee equals one, so bee is minus one half. Then ay is three halves. So p of sigma is three halves sigma, minus one half sigma cubed. For the matrix, one step is three halves W, minus one half W times W transpose times W. That is the Newton Schulz step, and you could have invented it yourself.
> screen: FadeOut, ReplacementTransform, Create

### why_p 13 <!-- #0dc503 -->
We built p from what happens close to one. But a real sigma can start anywhere. So take any positive sigma and apply p over and over. Where does it end up? That is the question in part (e) of the worksheet, and the rest of this video answers it.
> screen: FadeIn
