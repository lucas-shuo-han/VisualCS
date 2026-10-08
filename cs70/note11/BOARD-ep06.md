# BOARD: episode 06, The First Counterexample

Source: `notes.txt` lines 267 to 304. Language: en. Aim: 5 minutes (about 680 words).
File `ep06_well_ordering.py`, class `Ep06WellOrdering`. Scenes, in order: `hook`, `same`, `least`, `fails`.

The builder copies every narration line (the lines that start with a greater-than sign)
into a `say()` unchanged, one beat per `say()`, and builds exactly the stage described.
It decides nothing; an unclear line is a question in its report.

Format, read by `check.py`: a line that starts with three hash signs opens a beat, and
every line after it that starts with a greater-than sign is that beat's narration.
Neither is used anywhere else in this file.

## Facts

| id | Fact, with all its conditions | Notes line | Computed how |
|---|---|---|---|
| F1 | Lemma 11.2 (Improvement Lemma): if job J makes an offer to candidate C on day k, then on every subsequent day C has an offer in hand that she likes at least as much as J. "The claim for a day" in this episode: at the end of that day, C holds J or a job she likes more. | 255 to 256 | stated (episode 5) |
| F2 | The claim holds on day k. | 270 | stated (episode 5, base case) |
| F3 | Alternate proof: suppose day i, with i greater than k, is the first counterexample. On day i-1 she had an offer from a job J' she likes at least as much as J. J' still has its offer out on day i. So on day i her best choice is at least as good as J'. This contradicts day i being a counterexample. | 270 to 276 | stated |
| F4 | This is also a proof by induction: it has the base case i = k, and instead of proving "for all i, P(i) implies P(i+1)" it shows that "there is an i with P(i) and not P(i+1)" is false. | 284 to 288 | stated |
| F5 | Well-Ordering Principle (Definition 11.1): if S is a set of natural numbers and S is not empty, then S has a smallest element. | 290 to 293 | stated, not proved |
| F6 | The smallest element of {5, 2, 11, 7, 8} is 2; of the odd natural numbers, 1; of the primes, 2. | 294 to 295 | `min([5, 2, 11, 7, 8]) == 2`, `min(n for n in range(100) if n % 2 == 1) == 1`, `min(PRIMES) == 2` |
| F7 | The principle is used in the words "the first counterexample"; without it that notion would not be valid. Induction relies on the same order of the natural numbers; the notes call the principle equivalent to induction. | 268 to 269, 296 to 300 | stated |
| F8 | Many familiar sets of numbers do not have this property. The notes ask about the integers, the reals and the non-negative reals. Answers worked out here: none of the three has it. | 301 to 304 | integers: for every negative integer n, n - 1 is a smaller negative integer; non-negative reals: for every positive x, x / 2 is positive and smaller (`all(0 < x / 2 < x for x in XS)`) |

```python
PRIMES = [n for n in range(2, 100) if all(n % d for d in range(2, n))]
assert min([5, 2, 11, 7, 8]) == 2
assert min(n for n in range(100) if n % 2 == 1) == 1
assert min(PRIMES) == 2 and PRIMES[:5] == [2, 3, 5, 7, 11]
XS = [1, 0.5, 0.25, 0.125, 1e-9]
assert all(0 < x / 2 < x for x in XS)
assert all(n - 1 < n < 0 for n in range(-9, 0))
```

## Added to the notes

| Beat | The step that was missing | Why it holds |
|---|---|---|
| 1.3 | The picture of the proof: the days after the offer in a row, a day green when the claim holds and red when it fails. The two red days drawn (k+4 and k+6) are only a picture of "some days fail". | Every day is one or the other, because the claim for a day is either true or false. |
| 1.4 | Why the first counterexample is later than day k, and why the claim holds on the day before it. The notes say "by assumption". | Day k is not a counterexample (F2), so the first one is later and has a day before it; that day is not a counterexample, or the one we took would not be the first. |
| 1.5 | The step from the day before to the red day, in three moves. | Episode 5, beats 3.2 to 3.4: the job in hand was not refused, so it asks her again; she keeps it or a better one; at least as good as J' and J' at least as good as J. |
| 1.6 | From "no first red day" to "no red days". The notes stop at "this contradicts our initial assumption". | If there were any red day there would be a first one (this is the well-ordering principle, named in 3.5). |
| 2.1, 2.2 | In what sense the two proofs are the same (the notes' concept check). | Both check day k. Induction shows "green, so the next is green". The second proof shows "a red day right after a green day is impossible". These are the same statement. |
| 3.2 | The answer to the first concept check, with the set on a number line. | F6. |
| 3.4 | A reason to believe the principle: below any element there are only finitely many natural numbers, so the smallest can be found by checking them. This is a reason, not a proof from nothing; the notes take the principle as given, and so does the episode (beat 3.5 says "this fact is called"). | Below eleven lie the eleven numbers zero to ten. |
| 3.5 | Why the set of red days is not empty. | We supposed the lemma false, and that means the claim fails on at least one day. |
| 4.1 | The integers fail: the set of all negative integers has no smallest element. | Below every negative integer there is another. |
| 4.2 | The reals fail (they contain the negative integers), and the non-negative reals fail: the set of all positive reals has no smallest element. | Half of a positive number is positive and smaller. |
| 4.3 | Why zero does not rescue the positive numbers. | Zero is not positive, so it is not an element of that set; the set itself has no smallest element even though the non-negative reals as a whole do. |

## Left out, and why

| Item of the notes | Line | Reason |
|---|---|---|
| The letters J*, i and k in the voice; "no offer or an offer from some J* inferior to J" | 271 to 272 | On screen as "day k", "k+4" and so on; the voice says "the red day" and "the day before". The two ways the claim can fail are both "red". |
| "by the law of the excluded middle" | 287 to 288 | Used silently when a day that is not red is called green; the name adds nothing here. |
| The symbols P(i) and the arrow for "implies" | 286 to 288 | Replaced by green and red days. |
| "the natural numbers are indeed quite special" | 302 | Said by the two failures of scene `fails`. |
| "Back to our analysis of the Propose-and-Reject Algorithm" | 305 | It is the last sentence of beat 4.3 in other words. |

## Layout used by every scene

Three stages. Stage A for `hook` and `same`, stage B for `least`, stage C for `fails`.
Nothing but the scene heading is above y = 2.7; nothing is below y = -2.7.

Colours: a green day has stroke `GREEN_C` width 3 and fill `GREEN_C` opacity 0.25; a red
day has stroke `RED_C` width 3 and fill `RED_C` opacity 0.25; an undecided day has
stroke `GREY_B` width 2 and no fill; looked at `YELLOW_D`.

Stage A.
- Top text: `txt("the claim for one day: at its end, candidate C holds job J or a better one", 22)` at (0, 2.35), at most 12 wide.
- Day row: eight boxes `Rectangle(width=1.3, height=0.7)` at y = 1.3 and
  x = -5.25, -3.75, -2.25, -0.75, 0.75, 2.25, 3.75, 5.25, with the labels "k", "k+1",
  "k+2", "k+3", "k+4", "k+5", "k+6", "k+7" (`txt`, 22). All undecided at first.
  They are called box k, box k+1 and so on.
- Under-labels at y = 0.65, size 18, centred under a box: "offer" under box k, "day before" under box k+3, "first red day" under box k+4 (at most 1.4 wide each).
- Step arrow over the row: `CurvedArrow((-0.75, 1.72), (0.75, 1.72), angle=-1.2, color=YELLOW_D)` from box k+3 to box k+4; its highest point stays below y = 2.1.
- Legend at y = -0.1: a green-day square of side 0.35 at (-4.2, -0.1) with `txt("claim true", 20)` at (-3.1, -0.1); a red-day square of side 0.35 at (0.3, -0.1) with `txt("claim false", 20)` at (1.45, -0.1).
- Reasoning lines, centred at x = 0, size 22: R1 at y = -0.9, R2 at y = -1.5, R3 at y = -2.1.
- For scene `same`, in place of the reasoning lines:
  forward pair: two green-day squares of side 0.6 at (-4.3, -1.1) and (-2.9, -1.1), an
  arrow `Arrow((-3.95, -1.1), (-3.25, -1.1), buff=0)` between them, and the caption
  `txt("forwards: green today, so green tomorrow", 20)` at (-3.6, -1.9), at most 5 wide;
  backward pair: a green-day square at (2.9, -1.1) and a red-day square at (4.3, -1.1),
  `txt("never", 18, YELLOW_D)` at (3.6, -1.1) between them, and the caption
  `txt("backwards: no red day right after a green day", 20)` at (3.6, -1.9), at most 5.4 wide.

Stage B.
- Number line: `Line((-6, 0.8), (6, 0.8))`, with thirteen ticks `Line((x, 0.7), (x, 0.9))` at x = -6, -5, ..., 6 and the labels "0" to "12" (`txt`, 20) at y = 0.4 under them. The number n sits at x = n - 6.
- A dot for the number n: `Dot((n - 6, 0.8), radius=0.13, color=BLUE_C)`.
- Set text at (0, 2.2), size 26. Result text at (0, -0.5), size 24.
- Principle lines: W1 at (0, -1.4), size 26; W2 at (0, -2.1), size 22.

Stage C.
- Integer line: `Line((-6.3, 1.2), (6.3, 1.2))`, with thirteen ticks at x = -6, -5, ..., 6 and the labels "-9" to "3" (`txt`, 18) at y = 0.8 under them. The integer n sits at x = n + 3.
- "and so on" arrow: `Arrow((-5.6, 1.75), (-6.6, 1.75), buff=0, color=RED_C)`.
- Top text at (0, 2.3), size 22.
- Real line: `Line((-5, -1.0), (5, -1.0))`, ticks at x = -5 and x = 5 with labels "0" at (-5, -1.4) and "1" at (5, -1.4). The number t sits at x = 10 t - 5.
- Halving dots (`Dot`, radius 0.11, `BLUE_C`) at x = 5, 0, -2.5, -3.75, -4.375 on the real line, for 1, 1/2, 1/4, 1/8, 1/16; labels "1", "1/2", "1/4", "1/8" (`txt`, 18) at y = -0.6 above the first four.
- Open circle for zero: `Circle(radius=0.13, color=WHITE)` at (-5, -1.0), no fill.
- Bottom text at (0, -2.2), size 22.

Rules for the builder that come from the check script:
- To recolour a box, change its own stroke and fill. Never put a second rectangle on top.
- Never draw a line through a text.
- "Flash" means `Indicate(obj, color=YELLOW_D, scale_factor=1.1)`; the object returns to the look it had.
- When a text in a slot changes, fade the old one out and the new one in at the same place in one animation.

## Scene `hook`: heading "A second proof"

Stage: stage A, built in beat 1.1.
Kept from the scene before: nothing. Removed at the end: hold until the voice has
finished beat 1.6, then remove the reasoning lines, the step arrow and the three under-labels.

### 1.1
> Last time we proved the improvement lemma by walking forward from day to day. Once a
> job has made a candidate an offer, she holds that job or a better one. That is true
> at the end of that day and of every later day.

- with the first word: the top text appears.
- on "made a candidate an offer": the eight day boxes appear, left to right, all undecided; the under-label "offer" appears under box k.
- on "every later day": flash the boxes k+1 to k+7, left to right.
- uses: F1, episode 5.

### 1.2
> Here is a different way to prove the same thing. On the day of the offer itself the
> claim is true, because she keeps the best of her offers and this job is among them.
> So let us paint that day green.

- with the first word: the legend (both squares and both texts) appears.
- on "the claim is true": flash box k.
- on "paint that day green": box k becomes a green day.
- uses: F2 (episode 5, beat 3.1).

### 1.3
> Now suppose the lemma were false. Then on some later days the claim fails, so let us
> paint those days red, wherever they may be. Among the red days, look at the first one.

- with the first word: flash the top text.
- on "paint those days red": the boxes k+4 and k+6 become red days.
- on "the first one": flash box k+4; the under-label "first red day" appears under it.
- uses: F1 (what "false" means), F3. Which days are red is a picture.

### 1.4
> The first red day is not the day of the offer, because that day is green. So there is
> a day just before it, and that day is not red, because then ours would not be the
> first. The claim is true on the day before.

- with the first word: flash box k and box k+4 together.
- on "a day just before it": flash box k+3; the under-label "day before" appears under it.
- on "is not red": flash the red box k+6, then box k+3.
- on "true on the day before": box k+3 becomes a green day.
- uses: beat 1.2 (day k is green), beat 1.3 (first red day).

### 1.5
> So on the day before, she holds a job at least as good as the original one. She did
> not refuse that job, so by the step from last time it asks her again on the red day.
> Then she keeps it or something better, which makes the claim true on the red day.

- with the first word: nothing new.
- on "at least as good": reasoning line R1 appears: `txt("day before: she holds J', which is J or better", 22)`.
- on "asks her again": the step arrow is drawn from box k+3 to box k+4; reasoning line R2 appears: `txt("J' was not refused, so it asks her again", 22)`.
- on "keeps it or something better": reasoning line R3 appears: `txt("first red day: she holds J' or better, so J or better", 22)`.
- on "true on the red day": box k+4 keeps its red fill and gets a `GREEN_C` stroke, width 6.
- uses: beat 1.4, episode 5 beats 3.2 to 3.4, F3.

### 1.6
> But a day cannot be red and green at once, so the first red day does not exist. And if
> there is no first red day, there are no red days at all. So the lemma holds, and we
> have proved it a second time.

- with the first word: flash box k+4.
- on "does not exist": box k+4 becomes a green day; the under-label "first red day" fades out.
- on "no red days at all": box k+6 becomes a green day, and all remaining undecided boxes become green days, left to right.
- on "a second time": flash the top text.
- uses: beat 1.5 (the contradiction), F3. The move from "no first" to "none" is taken up in scene `least`.
- end of scene: hold until the voice has finished this beat, then remove the reasoning lines, the step arrow and the under-labels.

## Scene `same`: heading "One proof, two directions"

Stage: stage A with all eight boxes green, the top text and the legend. This scene adds the forward pair and the backward pair.
Kept from the scene before: top text, day row, legend.
Removed at the end: hold until the voice has finished beat 2.2, then remove everything.

### 2.1
> Is this a new kind of proof? Both proofs begin by checking the day of the offer. And
> both do the same work in the middle, which is to show that a green day is never
> followed by a red one.

- with the first word: nothing new.
- on "the day of the offer": flash box k.
- on "never": the backward pair appears (green square, red square, the word "never" between them) with its caption.
- uses: beat 1.2, beats 1.4 and 1.5, episode 5 beat 3.5.

### 2.2
> Induction tells it forwards, where green today forces green tomorrow, so the green
> runs on forever. The second proof tells it backwards, where a first red day would need
> a green day right before it. It is one argument told in two directions.

- with the first word: nothing new.
- on "green today forces green tomorrow": the forward pair appears (two green squares and the arrow) with its caption.
- on "runs on forever": flash the eight boxes of the day row, left to right.
- on "a first red day would need": flash the backward pair.
- on "two directions": flash both captions together.
- uses: beat 2.1, F4.
- end of scene: hold until the voice has finished this beat, then remove everything.

## Scene `least`: heading "The smallest element"

Stage: stage B, built in beat 3.1 from an empty stage.
Kept from the scene before: nothing. Removed at the end: hold until the voice has
finished beat 3.5, then remove everything.

### 3.1
> But the backward telling leaned on something we never proved. We said, look at the
> first red day. Why should a set of days have a first one at all?

- with the first word: the number line with its ticks and labels appears.
- on "the first red day": red dots (`Dot`, radius 0.13, `RED_C`) appear at the numbers 4 and 6 (as in the picture of scene `hook`), and the dot at 4 is flashed.
- on "a first one at all": the set text appears: `txt("does every set of natural numbers have a smallest element?", 24, YELLOW_D)`.
- uses: beat 1.3 (the first red day), beat 1.6.

### 3.2
> Days are counted with natural numbers, so let us try it with numbers. Take the set
> five, two, eleven, seven and eight. Its smallest element is two, and in a finite set
> we can always find it by comparing.

- with the first word: the two red dots are removed.
- on "five, two, eleven, seven and eight": the set text changes to `txt("{5, 2, 11, 7, 8}", 26)`, and blue dots appear at 5, 2, 11, 7, 8, in that order.
- on "smallest element is two": the dot at 2 turns `GREEN_C`; the result text appears: `txt("smallest element: 2", 24, GREEN_C)`.
- on "by comparing": flash the five dots from right to left (11, 8, 7, 5, 2).
- uses: F6, the dots on screen.

### 3.3
> Infinite sets work just as well. The odd numbers never end, but they start at one. The
> primes never end, but they start at two.

- with the first word: the five dots and the result text are removed.
- on "The odd numbers": the set text changes to `txt("the odd numbers: 1, 3, 5, 7, ...", 26)`; blue dots appear at 1, 3, 5, 7, 9, 11, the dot at 1 in `GREEN_C`; the result text is `txt("smallest element: 1", 24, GREEN_C)`.
- on "The primes": the dots are removed; the set text changes to `txt("the primes: 2, 3, 5, 7, 11, ...", 26)`; blue dots appear at 2, 3, 5, 7, 11, the dot at 2 in `GREEN_C`; the result text changes to `txt("smallest element: 2", 24, GREEN_C)`.
- uses: F6.

### 3.4
> Here is why it cannot fail. Pick any element of the set, say eleven, and only finitely
> many natural numbers lie below it. So we can check them one by one, and the lowest one
> that belongs to the set is the smallest.

- with the first word: nothing new.
- on "say eleven": the dot at 11 turns `YELLOW_D`.
- on "finitely many": flash the eleven tick labels "10" down to "0", one after another from right to left.
- on "the lowest one": flash the green dot at 2.
- uses: the primes on screen (beat 3.3). A reason, not a proof; see "Added to the notes".

### 3.5
> This fact is called the well ordering principle. Every set of natural numbers that is
> not empty has a smallest element. Our red days were such a set, not empty because we
> supposed the lemma false, and so a first red day had to exist.

- with the first word: nothing new.
- on "well ordering principle": principle line W1 appears: `txt("Well-Ordering Principle", 26, YELLOW_D)`.
- on "has a smallest element": principle line W2 appears: `txt("a set of natural numbers that is not empty has a smallest element", 22)`.
- on "Our red days": the dots of the primes are removed and red dots appear at 4 and 6 again.
- on "a first red day": flash the red dot at 4.
- uses: beats 3.2 to 3.4, F5, F7, beat 1.3.
- end of scene: hold until the voice has finished this beat, then remove everything.

## Scene `fails`: heading "Not every kind of number"

Stage: stage C, built in beats 4.1 and 4.2 from an empty stage.
Kept from the scene before: nothing. Removed at the end: nothing (the end card follows).

### 4.1
> Other number systems are not so kind. Take the integers, which include the negative
> numbers, and look at the set of all negative ones. Below minus one comes minus two,
> then minus three, and it never ends, so this set has no smallest element.

- with the first word: the integer line with its ticks and labels appears.
- on "all negative ones": the top text appears: `txt("the set of all negative integers", 22)`; red dots (`Dot`, radius 0.13, `RED_C`) appear at -1, -2, -3, in that order.
- on "it never ends": red dots appear at -4, -5, -6, -7, -8, -9, one after another to the left, and the "and so on" arrow appears at the left end.
- on "no smallest element": the top text changes to `txt("the set of all negative integers: no smallest element", 22, RED_C)`.
- uses: F8.

### 4.2
> The real numbers contain that same set, so they fail too. What if we only allow zero
> and everything above it? Then look at the set of all positive numbers. Whatever
> positive number you call the smallest, half of it is smaller and still positive.

- with the first word: flash the nine red dots together.
- on "zero and everything above it": the real line with its two ticks and the labels "0" and "1" appears.
- on "all positive numbers": the dot for 1 with its label appears at the right end of the real line.
- on "half of it": the dots for 1/2, 1/4, 1/8 appear with their labels, one after another to the left, then the dot for 1/16 without a label.
- uses: beat 4.1, F8.

### 4.3
> Zero would be below them all, but zero is not positive, so it is not in the set. So
> first counterexamples belong to the natural numbers, and to things counted by them,
> like our days. Next we use the improvement lemma to show that the result of propose
> and reject is stable.

- with the first word: the open circle appears at zero on the real line.
- on "not in the set": the bottom text appears: `txt("the set of all positive real numbers: no smallest element", 22, RED_C)`.
- on "first counterexamples": flash the tick labels "0" to "3" at the right end of the integer line.
- on "is stable": flash the bottom text and the top text together.
- uses: beat 4.2, F7, F8. The last sentence announces episode 7.

## End card

- The improvement lemma can be proved a second way: suppose it fails, take the first day on which it fails, and show that day cannot fail.
- That is induction told backwards: a red day never comes right after a green one.
- Well-Ordering Principle: every set of natural numbers that is not empty has a smallest element.
- The integers, the real numbers and the non-negative real numbers do not have this property.

## Author's check, each answered yes

- The first beat shows one concrete case before any definition. Yes: the row of days after the offer.
- Every "uses" line names an earlier beat, a fact row, or what is on the screen. Yes.
- A name is introduced after the beat where the viewer sees it happen. Yes: the principle is named in 3.5, after it was used in 1.3 and tried in 3.2 to 3.4.
- Every beat has a drawn object that changes; no beat is words on an empty stage. Yes.
- Every phrase after "on" is copied from its own beat, and appears there once. Yes, checked by script.
- A beat over fourteen seconds has at least two changes, over twenty-six at least three. Yes, checked by script.
- If the voice counts things, the stage shows exactly that many. Yes: five dots for the five numbers in 3.2.
- No step is skipped, and every step the notes left out is in "Added to the notes". Yes.
- Every item of the notes in the source range is in a beat or in "Left out". Yes.
- Narration: 16 beats, two to four sentences each, no sentence over 25 words, no beat over 60 words, no digit, colon or symbol. Yes, checked by script.
