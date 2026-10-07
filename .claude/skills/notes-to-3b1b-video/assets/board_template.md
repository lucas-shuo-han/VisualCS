# BOARD: episode NN, <title>

Source: `notes.txt` lines <a> to <b>. Language: <en>. Aim: <4 to 6> minutes.
File `epNN_<topic>.py`, class `EpNN<Topic>`. Scenes, in order: `hook`, `<name>`, `<name>`.

The builder copies every `> ` line into a `say()` unchanged, one beat per `say()`, and
builds exactly the stage described. It decides nothing; an unclear line is a question
in its report.

## Facts

Every number, date, name, definition and theorem the episode says or shows.

| id | Fact, with all its conditions | Notes line | Computed how |
|---|---|---|---|
| F1 | the sum of one to ten is fifty-five | 12 | `sum(range(1, 11)) == 55` |
| F2 | <a theorem keeps every condition: "connected and every degree even"> | 40 | stated, not computed |

## Left out, and why

| Item of the notes | Line | Reason |
|---|---|---|
| | | |

## Scene `hook`: <heading shown on screen>

Stage: <what is where. "Left block, centre (-3.4, 0.4), at most 6 wide: the ten numbers
in a row as boxes. Right block, centre (3.4, 0.4): empty until beat 1.2. Result line at
y = -2.2." Keep everything inside x ±6.8, y from -2.9 to 3.3.>
Kept from the scene before: <nothing | names>. Removed at the end: <names | nothing>.

### 1.1
> So here are the numbers from one to ten, and we want their sum without adding them
> one by one. Watch what happens when the first number is paired with the last one.

- with the first word: the ten boxes appear, left to right.
- on "paired with the last one": an arc joins box 1 and box 10; both turn yellow.
- uses: F1 is not said yet. Nothing here that the viewer has not seen.

### 1.2
> <two to four linked sentences; numbers as words; no symbols, colons or "step two">

- with the first word: <...>
- on "<exact words from this beat>": <...>
- uses: beat 1.1 (the arc), F1.

## Scene `<name>`: <heading>

Stage: <...>

### 2.1
> <...>

- with the first word: <...>

## End card

- <a result as a full sentence>
- <a result as a full sentence>
- <a result as a full sentence>

## Author's check, each answered yes

- The first beat shows one concrete case with real numbers, before any definition.
- Every "uses" line names an earlier beat, a fact row, or what is on the screen.
- A name or formula is introduced after the beat where the viewer sees it happen.
- Every beat has a drawn object that changes; no beat is words on an empty stage.
- Every phrase after "on" is copied from its own beat, and appears there once.
- A beat over fourteen seconds (about thirty-five words) has at least two changes.
- If the voice counts things, the stage shows exactly that many, separately visible.
- Every item of the notes in the source range is in a beat or in "Left out".
