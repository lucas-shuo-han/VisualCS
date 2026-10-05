# Writing narration that sounds like a person

The narration is heard before it is read. Scripts written as on-screen text sound wrong
aloud. Across two projects the listener's complaints were of three kinds: the voice
sounded choppy, a sentence broke in half, or a symbol or term was read wrongly. This
file covers the first two. Pronunciation is covered in `bilingual-and-voice.md` §5.

Run `python <skill>/scripts/narration_lint.py <unit> [N]` after writing each episode. It
flags split sentences, runs of short beats, tiny and over-long sentences, colons,
numerals left to the voice, and terms the voice may misread.

## Contents
1. Beats: the unit of narration
2. Why AI scripts sound choppy
3. Rules for a spoken script
4. Notation on screen, words aloud: `speak=`
5. Before / after
6. What other 3b1b / Manim skills do (and don't)
7. Pace: speed and pauses

## 1. Beats: the unit of narration

A **beat** is one `say()` call: two to four connected sentences (roughly 8–25 seconds)
about one picture. The kit synthesizes the whole beat as **one** voice clip, so the
intonation carries across its sentences, and shows the subtitle one sentence at a time.
`cue("phrase", anims...)` plays a step of the picture when the voice reaches the phrase.

```python
self.say("Look at the middle of the window, which is index four. "
         "That is too small, so the left half can go.",
         cur.animate.move_to(cells[4]))
self.cue("That is too small", Indicate(cells[4]), *[c.animate.set_opacity(0.2) for c in left])
```

How to cut a scene into beats:
- A new beat when the picture changes subject or the stage is cleared; not for every
  sentence. One sentence per beat brings back the choppiness (every beat ends with the
  longest pause).
- Inside a long beat, put a line break in the text where the thought turns. The voice
  takes a longer pause there (`PACE["paragraph"]`), and the viewer gets time to look at
  what just appeared. A beat of more than about 60 words needs at least one.
- Everything a beat mentions should happen on screen while it is said: one `cue()` per
  thing. If a beat has more than about four cues, or runs past 25 seconds, cut it at a
  sentence boundary.
- A cue phrase is copied from the beat's text, a few words long, and unique in it. With
  a translation table the source-language phrase is enough: the kit maps it by position.
  A `[cue] phrase not in the current line` warning at render time means the text was
  edited and the cue was not.
- A demonstration with nothing to say (a six-second zoom) is played between two beats,
  silently.

## 2. Why AI scripts sound choppy

- **One beat per short line.** Each beat ends with falling intonation, then the long
  pause. A script of 5-word lines sounds like a list read aloud.
- **Split sentences.** When "First the compiler turns C into assembly..." is followed by
  "...then the assembler...", each half is synthesized alone. The voice ends the first
  half as if it were a full sentence, and the second half starts cold. Inside one beat
  this cannot happen.
- **Punchy slide style.** Lines like "Done!", "Why 12 bits?", "Sounds wasteful?" and
  "That's RISC thinking." work as text on a slide. Spoken back to back by a neural voice,
  they sound like a quiz. One rhetorical question per section is plenty.
- **Notation in the sentence.** "t0 = 10 + 20 = 30" is fine on screen, but aloud it is
  "t zero equals ten plus twenty equals thirty": correct, but robotic.
- **No connectives.** Each line restarts the thought ("Case 1: ...", "Case 2: ...").
  Spoken explanation links its steps: "so", "which means", "and that's why", "now".

## 3. Rules for a spoken script

1. **Write sentences of 10–25 words** (15–40 Chinese characters), two to four to a beat.
   Vary the length. The subtitle shows one sentence at a time, so a sentence over about
   30 words (60 characters) is also too long to read; the lint flags it.
2. **A sentence lives in one beat.** If it needs two visual steps, give the second step
   a `cue()`.
3. **Connect the steps.** Start each sentence from the previous one: "So...", "That
   means...", "Now watch what happens to...". Read the scene's beats in order out
   loud. If it sounds like bullet points, it is.
4. **Say the idea, show the notation.** The screen shows `sum = 3 + 1 + 4 + 1 = 9`, while
   the voice says "Add them up and the sum is nine." (§4).
5. **Contractions and plain words.** Write "it's", "don't", "we'll". Write "use" rather
   than "utilize", and "so" rather than "therefore".
6. **Questions sparingly.** A question should make the viewer wait for the answer on
   screen. Answer it in the same beat, and use a full sentence rather than "Why?".
7. **Name things the same way every time** (GLOSSARY.md). Once the viewer knows what `rd`
   is, say "the destination register" or spell it out, but always the same way.
8. **Chinese:** avoid the 书面语 chain "X：Y。Z：W。". Use 口语 connectives (所以、也就是说、
   接下来、你看). Keep Latin letters out of the sentence when they are variables: a Chinese
   voice reads a lone "a" as 啊. Write 变量 A, or use `speak=`.
9. **Numbers and symbols, spelled out:** every numeral and symbol a voice would read
   strangely becomes a word or phrase. "1.7" is "one point seven", "×" is "times", "Σ" is
   "sigma" (pronunciation in `bilingual-and-voice.md` §5). Round where natural: "about a
   hundred times slower", not "100×". The exact value stays on screen.
10. **No colons in narration.** A colon turns the sentence into a labelled bullet ("Step
    two: ..."). Rephrase so the two halves are a spoken sentence: "watch what happens to
    s0 next" instead of "s0: what happens next". This applies to `speak=` text alike.
11. **Moderate length, low complexity.** Prefer medium-length sentences with at most one
    subordinate clause each. Say the idea completely, but keep the grammar simple enough
    to follow by ear.
12. **Plain, easy words.** Say the idea in the simplest words that still say it
    completely, so a listener who is new to the topic can follow on a first pass.

## 4. Notation on screen, words aloud: `speak=`

Prefer putting the notation in the picture (a `mono()` line, a formula) and keeping the
beat in words. When the subtitle itself must carry notation, `self.say(text, ...,
speak="...")` shows `text` and voices `speak` (also translated through the table):

```python
self.say("x ← x − η∇L",
         speak="Each step moves x a little against the gradient, scaled by the learning rate eta.")
```

The voice is synthesized sentence by sentence, so `speak` must have exactly as many
sentences as the text (the kit warns and speaks the text if not; `narration.py check`
reports it as `SPEAK`). If more than a third of an episode's beats need `speak=`, the text
is too symbolic. Rewrite it.

## 5. Before / after

Before (6 lines, each voiced separately):
> Why only 32? | Because smaller is faster. | Sounds wasteful? | It isn't. | Most values
> are small. | That's RISC thinking.

After (one beat):
> Why only 32 registers? Because a smaller register file is faster, and speed is the
> whole point of registers. It may look wasteful, but most values in real programs are
> small, and that is exactly the kind of trade-off RISC is built on.

Before (a split sentence):
> First the compiler turns C into assembly language... | ...then the assembler turns
> each instruction into a 32-bit machine word.

After (one beat, the second step on a cue):
```python
self.say("The compiler turns C into assembly, and then the assembler turns each "
         "assembly instruction into a thirty-two bit machine word.", FadeIn(asm))
self.cue("then the assembler", TransformFromCopy(asm, words))
```

## 6. What other 3b1b / Manim skills do (and don't)

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
pronunciation. Those came from this skill's production runs and are covered here and in
`bilingual-and-voice.md` §5. Borrow from them: manim-composer's written scene plan
(`assets/plan_template.md`), the pedagogy ordering above, and manim-voiceover's bookmark
idea, which is `cue()` here. `cue()` places the phrase by its position in the text, which
is accurate to about half a second and needs no speech recognizer; that is enough for
"highlight this when it is named".

## 7. Pace: speed and pauses

"Why is it so fast?" was said of a video whose voice ran at its normal speed. Two things
were wrong, and the user named both: the speech itself was a little fast, and there
were no pauses, so a formula appeared and the next sentence was already running.

- **Measure.** `python <skill>/scripts/pace.py <videos folder>` gives words per minute
  including pauses. The cut the user called too fast measured about 180. The accepted one
  measured 135 to 150, which is also where 3Blue1Brown's own narration sits. A first
  attempt at 120 was "a bit slow".
- **Pauses do most of the work.** `PACE` in series.py, in seconds: after a sentence,
  after a paragraph (a line break in the beat), after a beat. Defaults 0.4 / 1.0 / 0.8;
  the derivation used 0.75 / 1.6 / 1.8. Then the speed: `TTS["rate"]`, where "-4%" was
  the final choice after "-10%" was judged slow. Slowing the voice alone, without
  pauses, makes it sound drugged.
- **Long beats get paragraphs**, not more `say()` calls. `narration.py paragraphs`
  breaks every one-line beat of more than 60 words at a sentence that starts a new
  thought. Read the result; move a break when it lands inside one step of an argument.
- **A new formula gets a second of quiet.** Put the cue for it at the start of the
  sentence that reads it, and end the paragraph after that sentence.
- **Length follows.** Slower speech and pauses added about half again to the running
  time (35 minutes became 52). Tell the user before rendering, and offer to split the
  video into episodes (`derivation-episodes.md` §8).
- Do not cut words to make a video feel slower. The complaint is about breathing room,
  not about content.
