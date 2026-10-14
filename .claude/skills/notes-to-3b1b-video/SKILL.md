---
name: notes-to-3b1b-video
description: Turn written material (notes, slides, a derivation) into 3Blue1Brown-style Manim videos that build intuition and deep understanding, with a voice-over that drives the animation and subtitles. Use for any request to animate or visually explain course material.
---

# Notes → 3b1b videos

Small or cheap model, or "strict mode": follow `STRICT.md` instead.

## Pipeline

| Stage | Role | Output | Reads only |
|---|---|---|---|
| 0 Source | script; transcriber for PDFs | `notes/*.md` + `images/` or `pages/`, `INDEX.md` | page images (transcriber) |
| 1 Design | author | `PLAN.md`, `COVERAGE.md` | `notes/`, `references/teaching.md` |
| 2 Board | author | `BOARD-epNN.md` | PLAN, `teaching.md`, `script.md`, `picture.md` |
| 3 Build | builder | `epNN_*.py`, 480p preview | its board, `STRICT.md` (or `references/kit.md`) |
| 4a Voice | pronouncer | `say_as.py`, rewordings | `ASR-epNN.md`, `references/voice.md` |
| 4b Frames | reviewer, verifier | `REVIEW-epNN.md` | board, contact sheets |
| 5 Deliver | coordinator | `videos/` | reports, `references/production.md` |

The coordinator never reads or fetches the notes itself; stage 0 is in `references/production.md` ("Sources"). The coordinator runs the stages, owns the decisions taken with the user (minutes, voice, speed, pauses) and reads reports, not notes. Each role reads only its row; the board is the only thing passed from author to builder.

Alone on a few episodes, you play each role in turn and read that row's files when you enter its stage. For many episodes on a budget, run the roles as separate agents: `PIPELINE.md`.

Subtitles, voice and timing come from the board text automatically. Quality is decided in stages 1–2.

## Checkpoints (non-blocking)
Send the user the file and keep going; they interrupt if something is wrong, and may not look at all.
1. PLAN.md, when design is done.
2. The pilot: easiest + hardest episode through stage 4 before the rest are boarded, so review findings become rules first. Send its voiced preview.

## Checks (scripts, no tokens)
`fetch_notes.py` (stage 0), `board_lint.py` (stage 2), `check.py` (stage 3: lint, render, layout, audio/video, pace, code = board), `asr_check.py` (stage 4a: misheard words, pauses, rate, clipped endings), contact sheets (4b). A human hears the flagged clips. The final message states what was not checked.

Setup: `scripts/setup_env.sh` (or `.ps1`); copy `manim_kit.py`, `tts.py`, `assets/series_template.py` → `series.py`, `assets/say_as_asm.py` → `say_as.py` into `<course>/<unit>/`. When something breaks: `references/pitfalls.md`.
