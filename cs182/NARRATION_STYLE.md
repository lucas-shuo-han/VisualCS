# Narration style (CS182 series)

The narration should sound like someone explaining at a whiteboard, not like lecture notes read aloud.

- The full rules are in `.claude/skills/notes-to-3b1b-video/references/narration-writing.md` (skill v3). Read that first.
- The reference episode is `optimization/ep01_gd_least_squares.py`.

## The model: beats and cues

- One `say()` is a **beat**: two to four connected sentences about one picture, spoken as one clip.
- `cue("phrase from the beat", anims...)` plays the next animation when the voice reaches that phrase.
- Never write one short line per `say()`. Never split a sentence across two `say()` calls.
- Subtitles show one sentence at a time, so a beat may be long but a sentence may not (10–25 words).

## Converting an old episode (one line per `say()`)

1. Merge consecutive `say()` calls about the same picture into one beat.
2. Keep the first call's animations on `say()`. Turn each later call's animations into a `cue()` on a phrase copied from the beat.
3. A bare `self.play(...)` between lines usually becomes a `cue()` too.
4. Keep all layout code, asserts and computed numbers unchanged.
5. Add `SCENES = [...]` (the scene method names) to the class.

## Voice

1. **Open with a question or a puzzle**, and answer it in the same beat.
2. **Point at the screen; don't recite the formula.** Say the idea, show the notation.
3. **Connect the steps.** Use "so", "but", "which means", "now", "and that's why".
4. **Talk like a person.** Use contractions, "we" and "you", and everyday verbs (creep, blow up, settle down).
5. **Show the thing before naming it.** Describe the ravine, then call it the condition number.
6. **Land the aha out loud**: "So the learning rate isn't the real problem here, the ravine is."
7. **Give each number a meaning**: "each step keeps eighty-eight percent".
8. **Spell out numbers and symbols** in the beat ("zero point two", "eta", "X transpose"). The exact value stays on screen.
   - A spoken number must match a value the code computes or asserts.
9. **No colons** in narration. Use questions sparingly: about one per section.
10. **No filler**: avoid "crucially", "essentially", "note that", "let's dive in".
11. **End cards** are short takeaways a student would write in their own notes.

## Checks per episode

- `narration_lint.py <unit> N` must be clean.
- `captions.py <unit> N --spoken`: read what the voice will say and fix misreadings.
  - Example: a lone "a" after a variable was read as "ay". Reword it or add an entry to `say_as.py`.
- Voiced preview: no `[cue] phrase not in the current line` in the log.
- Contact sheets (end and mid): nothing overlaps and the picture matches the sentence.
- Audio and video durations match.
