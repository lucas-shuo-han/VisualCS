# Writing narration that sounds like a person

The narration is heard before it is read. Listeners complained of three things: a choppy
voice, a sentence broken in half, a symbol or term read wrongly. This file is about the
first two; pronunciation is in `bilingual-and-voice.md`. `narration_lint.py` (run by
`check.py`) finds the mechanical cases. Passing it is necessary, not sufficient: read the
beats of a scene in order, aloud in your head. If it sounds like bullet points, it is.

## Cutting a scene into beats

- A new beat when the picture changes subject or the stage is cleared, not per sentence.
  Every beat ends with falling intonation and the longest pause.
- Two to four sentences, 8 to 25 s. Past 25 s or four cues, cut at a sentence boundary.
- A line break in the text is a paragraph: a longer pause, time to look at what just
  appeared. A beat over about 60 words needs one (`narration.py paragraphs` proposes
  them; move a break that lands inside one step of an argument).
- A cue phrase is copied from the beat's text, a few words, unique in it. In a
  translated render the kit maps it by position, so keep the order of ideas the same.
- A demonstration with nothing to say (a six-second zoom) plays between two beats.

## Why a script sounds generated

| Cause | What is heard | Instead |
|---|---|---|
| one beat per short line | a list read aloud | merge into a beat |
| a sentence continued in the next `say()` | the first half ends as if finished, the second starts cold | one beat, the second step on a `cue()` |
| slide style: "Done!", "Why 12 bits?", "That's RISC thinking." | a quiz | full sentences; one rhetorical question per section, answered in the same beat |
| notation in the sentence: "t0 = 10 + 20 = 30" | correct and robotic | notation on screen, "add them and t zero holds thirty" aloud |
| no connectives: "Case 1: ... Case 2: ..." | each line restarts | "so", "which means", "and that's why", "now" |

## Rules

1. Sentences of 10 to 25 words (15 to 40 Chinese characters), varied. Over about 30
   words (60 characters) a sentence is also too long for the subtitle.
2. At most one subordinate clause; the simplest words that still say the idea whole.
   "use" not "utilize", "so" not "therefore", contractions.
3. Start each sentence from the previous one.
4. Numerals and symbols become words: "one point seven", "times", "sigma". Round where
   natural ("about a hundred times slower"); the exact value stays on screen.
5. No colons, in `speak=` text either. "Watch what happens to s zero next", not "s0: next".
6. One name per thing, every time (GLOSSARY.md).
7. Chinese: 口语 connectives (所以、也就是说、接下来、你看), not the 书面语 chain "X：Y。Z：W。".
   Keep Latin variable letters out of the sentence: a Chinese voice reads a lone "a" as 啊.
   Write 变量 A, or use `speak=`.

## `speak=`: notation on screen, words aloud

Prefer notation in the picture and the beat in words. When the subtitle itself must
carry notation:

```python
self.say("x ← x − η∇L",
         speak="Each step moves x a little against the gradient, scaled by the learning rate eta.")
```

`speak` needs exactly as many sentences as the text (each sentence is one clip; on a
mismatch the kit says so and speaks the text). If more than a third of the beats need
it, the text is too symbolic.

## Before and after

> Why only 32? | Because smaller is faster. | Sounds wasteful? | It isn't. | Most values
> are small. | That's RISC thinking.

> Why only 32 registers? Because a smaller register file is faster, and speed is the
> whole point of registers. It may look wasteful, but most values in real programs are
> small, and that is exactly the kind of trade-off RISC is built on.

## Pace

"Why is it so fast?" was said of a voice at normal speed: the speech was a little fast
and there were no pauses, so a formula appeared while the next sentence was running.

- Measure with `pace.py`: words per minute including pauses. 180 was "too fast", 120
  "a bit slow", 135 to 150 accepted (where 3Blue1Brown's own narration sits).
- `PACE` in series.py, seconds after a sentence / paragraph / beat: default
  0.4 / 1.0 / 0.8, the derivation 0.75 / 1.6 / 1.8. Then `TTS["rate"]`: "-4%" was the
  final choice, "-10%" slow. A slower voice without pauses sounds drugged.
- A new formula gets a second of quiet: cue it at the start of the sentence that reads
  it and end the paragraph after that sentence.
- Slower speech and pauses add about half to the running time (35 min became 52). Say
  so before rendering and offer to split. Never cut words to make a video feel slower.
