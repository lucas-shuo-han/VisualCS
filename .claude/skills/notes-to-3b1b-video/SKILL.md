---
name: notes-to-3b1b-video
description: Turn written material (notes, slides, a derivation) into 3Blue1Brown-style Manim videos that build intuition and deep understanding, with a voice-over that drives the animation and subtitles. Use for any request to animate or visually explain course material.
---

# Notes → 3b1b videos

Small or cheap model, or "strict mode": follow `STRICT.md` instead.

## Pipeline

| Stage | Output | Decides | Parallel |
|---|---|---|---|
| 1 Design | `PLAN.md` | what each episode teaches, in what order | no |
| 2 Board | `BOARD-epNN.md` | every spoken word + what changes on which word | per episode, after pilot |
| 3 Build | `epNN_*.py` | nothing, executes the board | per episode, ≤2 renders/machine |
| 4 Check | `REVIEW-epNN.md` | frames match board? sounds right? | per episode |
| 5 Deliver | `videos/` | nothing | — |

Subtitles, voice, timing come from the board text automatically. Quality is decided in 1–2.
Multi-agent split: `PIPELINE.md`.

User gates: after 1; after a pilot (easiest + hardest episode, voiced preview) before boarding the rest.

## 1. Design (per episode)

Supply what the notes skip:
- the question, and why a viewer would care
- the obvious attempt, failing visibly on real numbers; the real idea is the repair
- one concrete example carrying the episode
- the aha and the picture that makes it
- order: case before rule, reason before definition, name after seeing
- what is left out, and why; length agreed with the user

## 2. Board

- Spoken: linked sentences, plain words, symbols as words, ~140 wpm with pauses.
- Each sentence made true by the picture as it is said; no bullet text.
- No skipped step; added steps marked. Every number computed and asserted.
- Camera on the small thing that matters. One typeface, one colour per concept.

## 3–5. Build, check, deliver

- Kit API: `scripts/manim_kit.py` docstring; example `assets/example_episode.py`.
- Voice/speed chosen by the user's ear (`audition.py`) before the first full render.
- `scripts/check.py <unit> N` must PASS; then open every contact sheet and get it heard.
- User review notes → written plan (cause, fix, check) before code.
- Final: `render.py`, `srt_to_script.py`, README. Report what was not checked.

## References

- `references/narration-writing.md` — writing the script
- `references/derivation-episodes.md` — long arguments; acting on review notes
- `references/visual-patterns.md` — layout, camera, typeface
- `references/production.md` — coverage, delivery
- `references/pitfalls.md` — when something breaks
