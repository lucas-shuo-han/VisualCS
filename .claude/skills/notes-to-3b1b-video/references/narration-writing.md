# Writing narration that sounds like a person

The captions are the script, and with a voice-over they are *heard* before they are
read. Scripts written as on-screen text sound wrong aloud. In the CS61C series, the
listener's complaints were almost all of three kinds: the voice sounded choppy, a
sentence broke in half, or a symbol or term was read wrongly. This file covers the first
two. Pronunciation is covered in `bilingual-and-voice.md` §5.

Run `python <skill>/scripts/narration_lint.py <unit> [N]` after writing each episode. It
flags split sentences, runs of short captions, tiny sentences, and terms the voice may
misread.

## Contents
1. Why AI scripts sound choppy
2. Rules for a spoken script
3. Captions vs. narration: when to use `speak=`
4. Before / after
5. What other 3b1b / Manim skills do (and don't)

## 1. Why AI scripts sound choppy

- **Every caption is a separate TTS clip.** Each clip ends with falling intonation, and
  then there is a gap: the audio length plus 0.35 s, or the reading time if longer. A
  script made of 5-word captions sounds like a list read aloud.
- **Split sentences.** When "First the compiler turns C into assembly..." is followed by
  "...then the assembler...", each half is synthesized alone. The voice ends the first
  half as if it were a full sentence, and the second half starts cold.
- **Punchy slide style.** Lines like "Done!", "Why 12 bits?", "Sounds wasteful?" and
  "That's RISC thinking." work as text on a slide. Spoken back to back by a neural voice,
  they sound like a quiz. One rhetorical question per section is plenty.
- **Notation in the sentence.** "t0 = 10 + 20 = 30" is fine on screen, but aloud it is
  "t zero equals ten plus twenty equals thirty": correct, but robotic.
- **No connectives.** Each caption restarts the thought ("Case 1: ...", "Case 2: ...").
  Spoken explanation links its steps: "so", "which means", "and that's why", "now".

## 2. Rules for a spoken script

1. **One caption is one or two complete sentences.** Aim for 10–25 words in English and
   15–40 characters in Chinese. Vary the length; don't let three short ones run in a row.
2. **Never split a sentence across captions** when voiced. If a sentence needs two
   visual beats, keep one caption and play both animations inside `say()`, or run
   `self.play()` after it while the voice is still talking. Another option is to rewrite
   it as two full sentences ("The compiler turns C into assembly. Then the assembler...").
3. **Connect the steps.** Start each caption from the previous one: "So...", "That
   means...", "Now watch what happens to...". Read the episode's captions in order out
   loud. If it sounds like bullet points, it is.
4. **Say the idea, show the notation.** The screen shows `sum = 3 + 1 + 4 + 1 = 9`, while
   the voice says "Add them up and the sum is nine." Put the notation in the caption only
   when the viewer needs to read it. Otherwise pass a natural `speak=` (§3).
5. **Contractions and plain words.** Write "it's", "don't", "we'll". Write "use" rather
   than "utilize", and "so" rather than "therefore".
6. **Questions sparingly.** A question should make the viewer wait for the answer on
   screen. Follow it with the answer in the same or the next caption, and use a full
   sentence rather than "Why?".
7. **Name things the same way every time** (GLOSSARY.md). Once the viewer knows what `rd`
   is, say "the destination register" or spell it out, but always the same way.
8. **Chinese:** avoid the 书面语 chain "X：Y。Z：W。". Use 口语 connectives (所以、也就是说、
   接下来、你看). Keep Latin letters out of the sentence when they are variables: a Chinese
   voice reads a lone "a" as 啊. Write 变量 A, or use `speak=`.
9. **Numbers and symbols, spelled out:** every numeral and symbol a voice would read
   strangely becomes an English word or phrase. "1.7" is "one point seven", "1.3" is "one
   point three", "×" is "times", "Σ" is "sigma" (pronunciation in
   `bilingual-and-voice.md` §5). Round where natural: "about a hundred times slower", not
   "100×". The exact value stays on screen; the voice never reads it. Use `speak=` when the
   caption must carry notation (§3).
10. **No colons in narration.** A colon turns the caption into a labelled bullet ("Step
    two: ..."). Rephrase so the two halves are a spoken sentence: "watch what happens to
    s0 next" instead of "s0: what happens next". This applies to captions and `speak=`
    text alike.
11. **Moderate length, low complexity.** A long run of very short captions reads like a
    list and sounds unclear; a long sentence stacked with subordinate clauses loses the
    viewer. Prefer a few medium-length sentences with at most one clause each. Say the
    idea completely, but keep the grammar simple enough to follow by ear.
12. **Plain, easy words.** Say the idea in the simplest words that still say it
    completely. Reach for everyday verbs and nouns, not technical or fancy ones, so a
    listener who is new to the topic can follow on a first pass.

## 3. Captions vs. narration: `speak=`

`self.say(caption, ..., speak="...")` shows `caption` and voices `speak`. `speak` is also
translated through the table. Use it when the caption carries notation:

```python
self.say("Step two: s0 = t0 − d = 30 − 5 = 25.",
         speak="Then subtract d: thirty minus five leaves twenty-five in s zero.")
self.say("x ← x − η∇L",
         speak="Each step moves x a little against the gradient, scaled by the learning rate eta.")
```

Budget: if more than about a third of an episode's captions need `speak=`, the captions
themselves are too symbolic. Rewrite them.

## 4. Before / after

Before (6 captions, each voiced separately):
> Why only 32? | Because smaller is faster. | Sounds wasteful? | It isn't. | Most values
> are small. | That's RISC thinking.

After (2 captions):
> Why only 32 registers? Because a smaller register file is faster, and speed is the
> whole point of registers.
> You might think 12 bits is wasteful, but most constants in real programs are small,
> which is exactly the kind of trade-off RISC is built on.

Before (a split sentence):
> First the compiler turns C into assembly language... | ...then the assembler turns
> each instruction into a 32-bit machine word.

After:
> The compiler turns C into assembly, and then the assembler turns each assembly
> instruction into a 32-bit machine word.

## 5. What other 3b1b / Manim skills do (and don't)

Surveyed October 2026 so you don't have to repeat it:

- **adithya-s-k/manim_skill.** `manimce-best-practices`, `manimgl-best-practices`, and
  `manim-composer`, which plans a `scenes.md` with narration notes before any code. It is
  good on API patterns and planning. It covers no TTS and no pronunciation.
- **Yusuke710/manim-skill.** A plan → code → render → user-feedback loop that shows
  videos in the browser. It has no narration pipeline.
- **subinium/3b1b-style-animation-skill.** Pedagogy: intuition before formalism, why
  before what, concrete before abstract, show don't tell. It also has a palette. Nothing
  on scripts or voice.
- **NousResearch hermes-agent `manim-video`.** Plan → code → render → stitch (ffmpeg) →
  audio → review. It adds breathing room between animations (about 2 s). It has no
  pronunciation handling.
- **manim-voiceover** (the Manim community plugin). `with self.voiceover(text=...) as
  tracker:` sizes animations to `tracker.duration`. Its bookmarks (`<bookmark mark="A"/>`,
  aligned with Whisper) trigger an animation at a given word. It supports Azure, OpenAI,
  ElevenLabs, gTTS, Coqui and a recorder. It is the reference design for word-level sync,
  but it does nothing about how the text is pronounced.

Conclusion: none of them deal with spoken-script quality or with term and symbol
pronunciation. Those came from this skill's production run and are covered here and in
`bilingual-and-voice.md` §5. Borrow from them: manim-composer's written scene plan
(this skill's PLAN.md), the pedagogy ordering above, and manim-voiceover's bookmark idea
if you ever need an animation to land on an exact word.
