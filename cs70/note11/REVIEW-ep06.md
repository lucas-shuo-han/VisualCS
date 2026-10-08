# REVIEW: episode 06, The First Counterexample

Round 1. Reviewer (Sonnet) on the end sheets. Rows the reviewer marked "author" were
decided by the coordinator as written here; no narration word changes. Where a row
differs from BOARD-ep06.md, this file wins.

| # | Beat | What is wrong | Change wanted |
|---|---|---|---|
| 1 | 3.5 | Red dots at 4 and 6 stand under "the primes: 2, 3, 5, 7, 11, ..." and "smallest element: 2" while the voice talks about the red days. | On "Our red days", replace the set text by `txt("the red days: 4, 6, ...", 26, RED_C)` and remove the result text. On "a first red day", add `txt("first red day", 20, RED_C)` under the dot at 4, clear of the tick label, and keep it. |
| 2 | 3.4 | "Only finitely many numbers lie below eleven" shows only a dot at 11. | Add a `YELLOW_D` line (width 5) above the number line over the numbers 0 to 10 with `txt("only these lie below 11", 20, YELLOW_D)` above it, on the phrase about the numbers below eleven; remove both at the start of 3.5. |
| 3 | 1.5 | J' appears in the reasoning line with no explanation. | R1 becomes `txt("day before: she holds a job J' she likes as much as J, or more", 22)` and R3 `txt("first red day: J' or better, so J or better", 22)`; each at most 10 wide (break R1 into two texts on two rows if it is wider). |
| 4 | 1.3-1.6, 2.1-2.2 | The under-labels "offer", "day before", "first red day" are size 18 and nearly touch; "never" is the smallest text and the point of 2.1. | Under-labels size 20, "day before" (`GREEN_C`) and "first red day" (`RED_C`) on two different heights 0.35 apart so they cannot touch. "never" size 22, with the two squares of the backward pair 1.7 apart centre to centre. |
| 5 | 4.3 | The open circle at zero has the tick running through it and no explanation. | Circle with `fill_color` of the background, `fill_opacity=1`, added above the tick. Add `txt("0 is not positive: not in the set", 20)` near the circle, clear of the line and labels, on "not in the set". |
| 6 | 4.2 | "The real numbers contain that same set, so they fail too" shows nothing about the reals. | Add `txt("the real numbers contain these dots too", 22, RED_C)` above the line on "contain that same set"; fade it out at the next beat. |
| 7 | 4.2, 4.3 | The labels 0, 1, 1/2, 1/4, 1/8 are small and "half" is not on screen. | Those labels size 22. On "half of it", a yellow `CurvedArrow` from the dot at 1/2 to the dot at 1/4 with `txt("half", 20, YELLOW_D)` above it. |
| 8 | 3.3 | Old and new set texts are visible on top of each other at the end of "Infinite sets work just as well". | Fade the old set text and the result text out first (0.4 s), then bring the new set text in. |

Scene changes were clean. Result of round 1: not ready.
