# Production (coordinator)

## Conventions

## Sources (stage 0)
The notes are the root of everything: exact beats cheap. They reach `<unit>/notes/` as Markdown + images, never through the coordinator's context; it reads only the script's summary table.

| Source | Run | Then |
|---|---|---|
| web page with its source on GitHub (MyST, Jupyter Book) | `fetch_notes.py <url> --out U/notes` | — (exact source, toc order, figures) |
| other web page | `fetch_notes.py <url> ...` per page | residue reported → Haiku cleans markup only |
| PDF, slides, scans, handwriting | `fetch_notes.py <file.pdf> ...` (page images + text layer, batches in `TRANSCRIBE.md`) | one transcriber (Haiku) per batch, in parallel; `fetch_notes.py --out U/notes --verify`; flagged pages re-transcribed by Sonnet |
| Markdown / HTML files | `fetch_notes.py <file> ...` | — |

The author gets text and images together: `images/` for web figures, `pages/` for PDF pages. A whole textbook (hundreds of pages): consider MinerU (local, no tokens) for the first pass and transcribers only on the pages it gets wrong; not set up yet. `[unclear]` marks in a transcript go to the author as open questions, never silently filled.
Unit folder `<course>/<topic>/`, videos in `videos/<course>-<topic>/`. House style: the latest unit of the same course. Machine and voice defaults: the repo's `CLAUDE.md`.

## Decisions with the user, before the first full render
Defaults stand unless the user objects; the voice is usually fixed in `CLAUDE.md`.
- Voice, speed and pauses (`voice.md`): `audition.py`, the user picks by ear. A change later redoes every clip.
- Subtitles burned in or `.srt` only.

## The user
- Send the first voiced 480p preview early, with its exact path. Review clips are voiced, subtitled, one scene each.
- They hear the clips `asr_check.py` flagged and the pilot preview; the rest they may skip.
- Big rework: task list first, report against it. Ask before deleting old videos.

## Review notes on a finished video
Plan first: per note, the cause (file:line), the fix, the check. Terse notes hide concrete causes:

| Note | Cause | Fix, and who |
|---|---|---|
| fonts inconsistent | LaTeX, Pango, monospace mixed | `TEXT_FONT = "latex"`; builder |
| no zoom at key places | fixed camera; values too close | camera and values in the board; author |
| too fast | 170+ wpm, no pauses | `PACE`, rate; coordinator + user |
| voice | engine default | `audition.py`; user |
| derivation missing | only pictures | steps as lines in the board; author |
| just states things | no motive, no failed attempt | design; author |

Order: baseline commit → board wording → voice by ear → code, scene by scene → one final render. Announce → derive roughly triples the script; say so early.

## Optional: the script as a document
`narration.py` keeps beats in `narration.md` for the user to edit; `bind_scene.py` binds final wording into code; `narration.py check` must report 0. Never `sync` once it has hand-written parts.

## Delivery
- [ ] `check.py` PASS and `asr_check.py` flags settled per episode
- [ ] `render.py U --out videos/<course>-<unit>` (1080p, once, in the background); `pace.py`. It refuses an episode with kit findings or a narration-lint FAIL and forces the checks on.
- [ ] 1080p spot check: sheets of 2–3 episodes, one heard
- [ ] `srt_to_script.py`; README with episode table and how to re-render
- [ ] commit; final message: paths, episodes, coverage, notes errors, clips the user should hear, tokens per role (coordinator included), what was not checked

## Publishing (only when asked)
The user uploads, as Private, in their own browser. The description discloses: unofficial, not affiliated with the course, AI-assisted, synthetic voice, Manim, 3b1b-inspired. Raise course policy and voice licence first.
