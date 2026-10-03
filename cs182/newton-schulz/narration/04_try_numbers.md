<!-- 副本：cs182/newton-schulz/narration.md 中 "## 04 · try_numbers" 的独立编辑文件。主源仍为 narration.md。 -->

## 04 · try_numbers — Just try numbers (easy cases first)

> **Purpose.** Build trust with starts that behave: 0.5, 1.3, 0.1 all go to 1, by hand arithmetic. Then ask what could stay put and solve p(x) = x step by step.
> **Logic chain.** Scene 03 ended on "where does a sigma end up?" → just try one: 0.5 → one above one: 1.3 → one far away: 0.1 → all reach one, and one stays put (first wish) → *if another number also stayed put, sigma could get stuck there. Is there one?* → try zero: it stays too → algebra finds them all: 0, 1, −1 → *but 0.1 left zero and went to one. Why does one fixed point pull and another push?* → cobweb.
> **Beats.** p(0.5) arithmetic; the staircase of values; the algebra x(1−x)(1+x)=0 gives 0, 1, −1.
> **Tone.** Unhurried. Say each arithmetic step aloud; let the numbers appear one at a time.
> **Polish pass (novice check).** The first step is now computed in full (cube first, then half). Each chain of values is spoken with its real numbers, so the viewer can pause and check. The switch from the letter sigma to the letter x is announced in beat 07. Each line of the algebra in 08–10 says what was done and what it gives, and minus one is checked by plugging it in.
> **Numbers used.** 0.5 → 0.6875 → 0.869 → 0.975 → 0.999. 1.3 → 0.8515 → 0.969 → 0.9985. 0.1 → 0.1495 → 0.223 → 0.328 → 0.475 → 0.659 → 0.845 → 0.966 → 0.998.

### try_numbers 01 <!-- #e12179 -->
Where does a sigma end up? No theory yet. Let's just pick a number and try it, say zero point five.
> screen: FadeIn

### try_numbers 02 <!-- #b2ca63 -->
One step of p takes three halves of the number, and subtracts one half of its cube. Three halves of zero point five is zero point seven five. Zero point five cubed is zero point one two five, and half of that is zero point zero six two five. Subtract, and we get zero point six eight seven five.
> screen: Write

### try_numbers 03 <!-- #ea3911 -->
Now feed that result back in, and keep going. Zero point six nine becomes zero point eight seven, then zero point nine eight, then zero point nine nine nine. It is closing in on one.
> screen: FadeOut, Write

### try_numbers 04 <!-- #f7274e -->
That start was below one. Now try one above it. One point three drops to zero point eight five, which is below one, and then it climbs, to zero point nine seven, and then zero point nine nine eight. It also closes in on one.
> screen: Write

### try_numbers 05 <!-- #56cc9c -->
Both of those were fairly close to one. So try a start that is far away, down near zero. Zero point one becomes zero point one five, then zero point two two, then zero point three three. It is slow at first, but it keeps climbing, and after eight steps it also reaches one.
> screen: Write

### try_numbers 06 <!-- #e96769 -->
All three starts end at one. And once a value is at one, it stays there. Three halves minus one half is one, so p of one equals one. That is our first wish at work.
> screen: FadeIn

### try_numbers 07 <!-- #769257 -->
But if some other number also stayed put, a sigma could get stuck there and never reach one. Is there such a number? Try zero. Three halves of zero is zero, and zero cubed is zero, so p of zero is zero. Zero stays put as well.
From here on, call the input x. A value where p of x equals x is called a fixed point. We have found two of them. Are there any more?
> screen: FadeIn

### try_numbers 08 <!-- #4eb4c7 -->
To find them all at once, write down p of x equals x. That is three halves x, minus one half x cubed, equals x. Subtract x from both sides, and we get one half x, minus one half x cubed, equals zero.
> screen: FadeIn

### try_numbers 09 <!-- #cb4264 -->
Both terms contain one half x, so pull it out. What is left inside is one minus x squared. And one minus x squared splits into one minus x, times one plus x. So the equation says one half x, times one minus x, times one plus x, equals zero.
> screen: FadeIn

### try_numbers 10 <!-- #81f7b9 -->
A product is zero only if one of its factors is zero. So x is zero, or x is one, or x is minus one. Those are all the fixed points there are, the two we found and a new one. And minus one does check out. Minus three halves, plus one half, is minus one.
A singular value is never negative, so for now minus one is just a point on the list.
> screen: FadeIn

### try_numbers 11 <!-- #e4b1cb -->
But zero matters right away. A sigma at exactly zero is stuck. And yet zero point one, right next to zero, walked away from it, all the way to one. Why would one fixed point pull values in and another push them away? To see what happens around each of them, we need a picture of the iteration.
