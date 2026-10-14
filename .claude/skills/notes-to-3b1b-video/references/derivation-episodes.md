# Long arguments; acting on review notes

## Story
- Each sentence uses only what the previous one produced.
- Try, fail, try again, succeed, then name the pattern. Failures are content.
- No spoilers, no teasers, no "we require": conditions come from the goal.
- Easy case first, by trying numbers; find what decides the outcome; reduce each new case to the last.
- Close it: does the method cover the whole region and its edges? Overview last; the last scene answers the first question.

## Hard steps
- Compare the quantities themselves, with the deciding factor named on screen.
- Arithmetic in steps, one line per sentence. The argument written on screen as spoken (picture left, claims right); a proof told only in pictures reads as "derivation missing".
- Name what is used without proof; keep that list short.
- Zoom as a movement (`zoom_to`, or a box growing into new axes), never a cut.

## Words and animation
- Animation shorter than the words → `hold()`; longer → cut `run_time`.
- After a rewrite, beats whose word count doubled need more cues (`[still]`).
- Shared objects on `self`; `preview_only([...])` renders later scenes alone by fast-forwarding.

## Script as a document (optional)
`narration.py` keeps beats in `narration.md` for the user to edit; `bind_scene.py` binds final wording into code; `narration.py check` must report 0. Never `sync` once it has hand-written parts.

## Cost
Announce → derive roughly triples the script. A 50-min 1080p render takes ~40 min; a voice or speed change redoes all of it.

## Review notes on a finished video
Plan first: per note, cause (file:line), fix, check. Terse notes hide concrete causes:

| Note | Cause | Fix |
|---|---|---|
| fonts inconsistent | LaTeX + Pango + monospace mixed | `TEXT_FONT = "latex"`, `txt()` / `num()`, three sizes |
| no zoom at key places | fixed camera; values 0.03 apart | `zoom_to`, inset, other values |
| too fast | 170+ wpm, no pauses | `PACE`, paragraphs, slower rate |
| voice | engine default | `audition.py`, user picks |
| derivation missing | only pictures | lines on screen, one per sentence |

Order: baseline commit → script → voice by ear → structure → visuals scene by scene → one final render.
- A handwritten derivation is checked, not trusted: list corrections, get them confirmed, `assert` each.
- Split past ~25 min where the viewer has a new question; each episode ends on the next one's question.
- A rigour pass finds: approximations where exact is as short, unsourced numbers, unstated exceptions, loose words, "because" that is only assertion.
- Report what was not done.
