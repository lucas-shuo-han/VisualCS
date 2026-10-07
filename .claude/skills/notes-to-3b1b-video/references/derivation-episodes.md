# One long argument, and polishing a video with its viewer

From the Newton–Schulz derivation (CS182): a rough 14-minute "announce the result" video
became a 35-minute lesson over several review rounds, then three episodes after the user
watched it. Read this for a proof or derivation, or when a video is "too rough", "too
fast" or "just states things".

## 1. The story

The standard, confirmed over several rounds: **each sentence may only use what the
previous sentence just produced.**

- Try, fail, try again, succeed, then name the pattern. W·W has mismatched shapes; WᵀW
  loses U; WWᵀW keeps U and Vᵀ; only now say "odd powers". The failures are content.
- No spoilers: no "rules of the game" up front, no formula in the motivation that a
  later scene derives. When a scene is rewritten as a derivation, re-check the earlier ones.
- Conditions come from the goal (p(1) = 1 because the iteration has to settle at one),
  never from "we require". No forward teasers; a thing is named after it has been seen.
- Cases: the easy one first, by trying numbers. Watch a start, try a bigger one, meet
  the first failure, then ask why. Boundary values come out of that explanation.
- The hard region: start from the picture the viewer has, state the natural idea in
  plain words, follow a few concrete starts until their fates differ, find what decides
  the fate, and reduce each new case to the previous one.
- Close the argument: does the method cover the whole region, and what happens on the edges?
- The overview picture comes last, after the cases are earned. The last scene answers
  the opening question.

## 2. A hard step

- Compare the quantities themselves. "Does the value shrink?" drawn as the curve
  against y = −x had to be decoded; |p(x)| = |x| · (x² − 3)/2 with the factor named on
  screen and checked on the starts already tried did not.
- Separate what the viewer tracks (sizes follow the folded curve, the sign is a flip count).
- Arithmetic on screen in steps, one line as each is said.
- Zoom as a movement: `zoom_to`, or a box on the old picture that grows into the new
  axes. A cut to a closer view reads as a change of subject.
- Write the argument down as it is spoken. A proof told only in pictures drew "the
  derivation is missing". Picture on the left; on the right the claim, the recurrence,
  increasing, bounded, so it converges, the limit equation, the limit.
- Name what is used without proof and keep that list short. Each of continuity, the
  norm identity and the non-square case got one sentence instead of silence.
- A step the user marks "explain closely" gets its own lines: one per reason.

## 3. Words and animation

- Animation shorter than the words: it waits (`hold()`). Longer: cut its `run_time`. A
  pure demonstration: between two beats, silent.
- After a script rewrite, list every beat whose word count at least doubled; each needs
  its picture split into cues (the kit reports the worst as `[still]`).
- Scenes that build on one stage keep shared objects on `self`. `preview_only` lets a
  later scene render alone by fast-forwarding the earlier ones (end states, no time):

```python
SCENES = ["motivation", "design", "graph", "slopes", "summary"]

def construct(self):
    if self.preview_only(["graph", "slopes"]):   # chains of scenes that share a stage
        return
    self.title_card()
    for s in self.SCENES:
        getattr(self, s)()
    self.end_card([...])
```

  Restore shared objects only for scenes that follow the one creating them, or a
  single-scene preview shows things the full episode does not.

## 4. The script as a document

`narration.py` keeps every beat in `narration.md` under `### scene NN <!-- #hash -->`,
with notes the renderer ignores (purpose, logic chain, what the viewer knows and asks
next). The user edits wording there; `say()` takes it when the hash matches the code.

- Script rounds happen in the document only. Record under each scene what the new words
  need from the picture.
- When the words are final, write the scene's code with `__Tnn__` tokens and run
  `bind_scene.py`: it pastes the beats in, refuses a `cue()` phrase missing from its
  beat, and rebinds the hashes. `narration.py check` must report 0 before a render.
- Never run `narration.py sync` once the document has hand-written sections: it
  rebuilds the file from the code.
- Keep a revision log at the top (length before and after per scene, beats that grew,
  the animation each needs, done or not). It is the task list.

## 5. Cost

Turning "announce" into "derive" roughly triples the script (14 min became 40 of
narration). Tell the user early; let them cut after watching. First voiced render of new
text: minutes per scene; later one to two. A final 1080p render of 50 min in three jobs
took 40 min, and a change of voice or speed costs all of it again.

## 6. Review notes on a finished video

Five lines came back. **Write the plan before touching anything**: per note the cause
with file and line, the fix, the check. Terse notes hide concrete causes:

| The note | What it was | The fix |
|---|---|---|
| "fonts are inconsistent" | LaTeX formulas, Pango labels, monospace ticks; √3 written two ways | `TEXT_FONT = "latex"`, `txt()` / `num()`, three font sizes |
| "no zoom at the key places, unsuitable points" | a scene class that could not move its camera; starts 2.2 and 2.23 drawn 0.03 apart | `zoom_to` at each crossing; box grows into picture; an inset for the close pair |
| "why so fast" | 168 to 180 wpm, 0.35 s between beats, 200-word beats in one breath | `PACE`, paragraphs, a slower rate |
| "a pleasant male voice" | the offline engine's default was female | `audition.py`, the user picks |
| "derivation missing" | present, but only as pictures and two formulas | fourteen lines on screen, each with its sentence |

**Order**, set when the user rejected a code-first plan: commit a baseline and put the
plan at the top of `narration.md`; script only; voice and speed by ear while the script
is read; structure (files, series.py, shared helpers); pace, typeface, new scenes,
camera, one scene at a time with frames inspected; one final render. Work on the next
step while the user listens to the previous one.

**A handwritten derivation is read critically.** The photo had a sign error, the wrong
limit twice, "uniform" for "monotone", an inequality reversed. List the corrections, ask
the user to confirm, keep their notation where it does not clash, and `assert` each
corrected claim numerically.

**Splitting** past about 25 min: where the viewer has a new question, not by length.
Each episode ends by asking the next one's question, unanswered. Each later one opens
with two or three sentences of results and redraws what it needs. Method names stay
unique across the files.

**A last pass for rigour**, asked for by name. It found: an approximation where the
exact expression is as short; "no tidy answer" where a closed form exists; a number
without its source; a general claim with an unmentioned exception; a word used loosely
(orthogonal, for a non-square matrix); a limit through a function not said to be
continuous; a "because" that was an assertion. Report each with a proposed sentence and
add them once approved.

**Say what was not done.** The plan aimed at 120 to 125 wpm and the result was 135 to
150 after the user asked for a faster voice; changed scenes were inspected frame by
frame but the episodes were not watched end to end. Both went into the report.
