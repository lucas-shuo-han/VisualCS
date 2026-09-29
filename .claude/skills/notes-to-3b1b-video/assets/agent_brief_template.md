# Brief for agents working on <SERIES>

<!-- Fill in the <...> parts, save next to the notes (outside the repo), and give each
     episode agent a short prompt: "Read BRIEF.md and GLOSSARY.md, then write episode N
     (files: <unit>/epNN_*.py and <unit>/i18n/epNN.py) covering <notes chapter / sections>." -->

Read this whole file before starting. Your task-specific instructions are in your prompt.

## Project
- Repo: `<path>` (git, branch `<branch>`). Unit folder: `<unit>/` (kit: `manim_kit.py`; episode
  list: `series.py`; tables: `i18n/epNN.py`; voice: `tts.py` + `say_as.py`).
- Source of truth for content: the notes in `<notes dir>` (one file per chapter). Cover every
  substantive item of your chapter(s); omit only trivia, and say what you omitted and why.
- Episodes are written in **<source language>**; <other language> comes from the table.
- House style examples: `<unit>/<good episode 1>.py`, `<unit>/<good episode 2>.py`.
- Terminology: `GLOSSARY.md` (same folder as this brief). Use exactly those forms.

## Hard rules (several agents share this checkout)
1. Only create/edit your own files (named in your prompt). Do NOT edit `manim_kit.py`,
   `series.py`, `tts.py`, `say_as.py`, scripts, README, other episodes or tables. Need a helper?
   Define it in your episode file. Found a kit bug? Work around it locally and report it.
2. No state-changing git commands (commit, add, stash, checkout, reset, push). The coordinator commits.
3. Scratch files go in `<scratch>/agents/<NN>/`, never in the repo.
4. One render at a time (render the languages one after the other).
5. <"No LaTeX: never use Tex/MathTex/Matrix/DecimalNumber/Integer." or "LaTeX is available.">
6. Keep a short `<scratch>/agents/<NN>/STATE.md` (done / next) so you can resume after an
   interruption (rate limits happen) without redoing work.

## Commands (<OS / shell>)
- Preview: `<python> <skill>/scripts/render.py <unit> N --preview --lang <xx> --manim <manim> --media <scratch>/agents/<NN>/media`
  (add `--lax` while the table is incomplete, `--voice` to hear it). Log on failure: `<media>/<xx>/epNN.log`.
- Frames: `<python> <skill>/scripts/contact_sheet.py <mp4> <srt> <out> --at end` and `--at mid`.
  **Open every sheet** and fix overlaps, off-frame text, content under the caption band, leftovers.
- Narration: `<python> <skill>/scripts/captions.py <unit> N --spoken` (all languages + what the voice says).
- Tables: `<python> <skill>/scripts/i18n_check.py <unit> N` (`--skeleton`, `--widths`).

## Scene API
`self.title_card()` / `self.end_card([bullets])` (titles, next episode from series.py),
`self.say(text, *anims, speak=None)`, `self.hold()`, `self.clear_stage()`, `self.heading()`,
`txt()`, `mono()`, `CodeListing`, ... -- read the docstring at the top of `manim_kit.py`.

## Layout
- Frame 14.2 × 8 (x ∈ [−7.1, 7.1], y ∈ [−4, 4]); keep content in x ∈ [−6.8, 6.8].
- Keep content above y ≈ −2.5 while a caption shows (a 3-line caption reaches y ≈ −2.6).
- Translations are often wider: prefer a shorter translation over a smaller font; branch with
  `if EN:` only when the layout genuinely has to differ.

## Writing
- Captions are the narration (and the voice-over script): each one sentence, one idea, explaining
  what is on screen at that moment. <source language> ≤ ~<45 characters / 30 words>.
- <Language-specific style: full-width punctuation and “” in Chinese, a space between CJK and
  Latin, English terms in parentheses on first use ...>
- Translations: idiomatic, the meaning not the words, course terminology from GLOSSARY.md.
- Read aloud-ability: avoid symbol soup in captions (the voice reads them). Check with
  `captions.py --spoken`; reword, or pass `speak="..."` to `say()` (and give it a table entry).
- Every number on screen is computed in Python; assert the key ones at the top of the file.
- If the notes contain an error (it happens), do the right thing and report it.

## Done means
1. `i18n_check.py <unit> N` says ok.
2. Previews render in every language without `--lax`.
3. You looked at the end + mid contact sheets of the final previews and fixed what they showed.
4. Final message (concise): files, duration per language (last .srt timestamp), a coverage table
   (notes item → caption / omitted: why), notable wording decisions, notes errors found,
   anything unresolved, kit bugs.
