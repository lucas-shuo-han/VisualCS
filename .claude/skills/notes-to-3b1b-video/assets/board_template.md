# BOARD: episode NN, <title>

Source: notes lines <a>–<b>. Aim: <n> min. File `epNN_<topic>.py`, class `EpNN<Topic>`. Scenes: `hook`, `<name>`, ...
Design (from PLAN.md): question <...>; why care <...>; obvious attempt and its failure <...>; aha <...>.

<!-- Format read by check.py: `### ` opens a beat; following `>` lines are its narration, joined into one say() (≤ 60 words). Use neither anywhere else. The builder copies narration unchanged and builds the stage exactly; an unclear line becomes a question in its report. -->

## Facts
| id | Fact, with all conditions | Notes line | Computed how |
|---|---|---|---|
| F1 | the sum of one to ten is fifty-five | 12 | `sum(range(1, 11)) == 55` |

## Added to the notes
| Beat | Missing step | Why it holds |
|---|---|---|

## Left out
| Item | Line | Reason |
|---|---|---|

## Layout
<Optional: blocks that keep their place (centre, width). Heading top left y ≈ 3.5; nothing else above 3.3; nothing below −2.9; x within ±6.8.>

## Scene `hook`: <on-screen heading>
Stage: <what is where, with centres and widths>. Kept from before: <...>. Removed at end: <...>.

### 1.1
> So here are the numbers from one to ten, and we want their sum without adding them
> one by one. Watch what happens when the first number is paired with the last one.

- with the first word: the ten boxes appear, left to right.
- on "paired with the last one": an arc joins box 1 and box 10; both turn yellow.
- uses: nothing yet.

### 1.2
> <...>

- with the first word: <...>
- on "<exact phrase>": <...>
- uses: 1.1, F1.

## End card
- <result as a full sentence> ×3

## Author's check (all yes)
- First beat: one concrete case with real numbers, before any definition.
- Every "uses" names an earlier beat, a fact, or the screen.
- Names and formulas come after the viewer sees the thing.
- Every beat has a drawn object that changes; >35 words → ≥ 2 changes.
- Every "on" phrase is copied from its beat and unique there.
- Counted things are shown exactly, separately.
- No skipped step; added steps listed.
- Every notes item in range is in a beat or "Left out".
