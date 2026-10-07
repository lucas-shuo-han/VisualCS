# Production: coverage, planning, agents, the user, delivery

## Coverage

"Make videos for these notes" means cover them. Before planning:

1. Every chapter to clean Markdown in a scratch folder.
2. List every substantive item: concept, definition, rule, table, worked example,
   exercise, footnote. Keep the notes' own examples with their numbers: viewers meet
   them again in homework.
3. Map item → episode after planning and item → beat after writing. A substantive item
   nobody covers is a bug. Trivia may go, with its reason written down ("anecdote",
   "image not reproducible", "beyond scope", "covered in episode N").
4. Keep the table (`COVERAGE.md`): it answers "did you miss anything?".

Notes contain errors (an encoding that does not match its listing, a register the
example clobbers, "Hello, %s" against "Hello, %s!" shifting an offset). Recompute every
example, show the correct version, report the difference.

## Planning

- Length follows content: one idea with one example is 3 to 4 min, a notes chapter 6 to
  8, more than that is two episodes. A short episode beside 7-minute ones reads as thin.
- `assets/plan_template.md` per episode: the question, the worked example with real
  numbers, the aha, a scene list, recap bullets. Where a scene's plan says "state X",
  ask what the viewer would have to see to say X themselves.
- Order and titles live in `series.py`, so numbers, "next episode" lines, the end card
  and file names survive reordering. Episode 1 introduces the series, the last recaps it.
- `GLOSSARY.md`: one form and one colour per concept, with its translation.

## Parallel agents

Write the first one or two episodes yourself: they are the house style agents copy.
Then one agent per episode from `assets/agent_brief_template.md`; its prompt only names
the episode, its files, its notes chapters and the neighbouring episodes.

- Each agent edits only its episode file and table. Kit, series.py, scripts and README
  are the coordinator's; agents report kit bugs and run no state-changing git.
- Three agents at a time; one render each; about cores / 2 renders in total.
- Usage limits interrupt agents: each keeps a `STATE.md`; resume the same agent.
- A fresh reviewer per two episodes finds what the author missed (translated-sounding
  phrasing, a term used two ways, a skipped item).
- The coordinator commits after `check.py` passes and it has skimmed the sheets.

## Review pass, per episode

Coverage against the checklist. The source script read in order as a viewer: vague or
wrong statements, sentences that do not match the screen at that moment, missing
transitions, repetition. The translation. `captions.py UNIT N --spoken` for what a
listener would stumble on. One voiced preview per language heard end to end. Changed
episodes re-rendered and their sheets looked at again.

## The user

- A watchable result early: the first finished episode as a voiced 480p preview.
- Review clips are voiced, subtitled on the frame, one scene each, with the exact path.
  A silent clip with a separate subtitle file was called unusable.
- For a large rework write the task list first and report against it.
- Final renders run once, in the background, after the review pass. Say where the
  files will land.
- Ask before removing superseded videos; one user wanted the old cut kept.

## Delivery

- [ ] `check.py` PASS per episode and language; `i18n_check.py UNIT` ok
- [ ] `render.py UNIT --out videos/<course>-<unit>`; `pace.py` on the folder, numbers in the report
- [ ] one 1080p sheet spot check of two or three episodes; one played with sound
- [ ] `srt_to_script.py videos/<...>/<lang> UNIT/SCRIPT.<lang>.md`
- [ ] README: episode table per language, how to re-render, how to change a
      pronunciation or add a translation
- [ ] commit code, tables, videos (8 to 20 MB per episode), subtitles, scripts
- [ ] final message: paths, episodes, coverage, notes errors, limitations

## Publishing

Only when asked, in the user's own browser session, never asking for a password.

- Upload as Private; the user decides about Public after watching it there.
- The user drags the files in. Browser automation cannot hand over a 20 to 50 MB
  video, and a file is never cut into pieces to get under an upload limit.
- Title: the episode title with a part number; no other creator's name or logo.
- Description, the same block on every episode: an unofficial student-made study
  video, not affiliated with or reviewed by the university or course staff, not
  official material or a solution key, mistakes are the author's; made with an AI
  coding assistant (named), directed and reviewed by the author, synthetic voice, Manim
  Community Edition, style inspired by 3Blue1Brown without affiliation; thanks; not
  monetized, will change or remove on request; a code link only if the repo is public.
- Settings: not made for kids, no paid promotion, monetization untouched. Answer the
  platform's AI question as worded (YouTube's is about realistic synthetic content: an
  abstract animation with a synthetic narrator is "No", and the description discloses).
  Tell the user which answer you chose and why.
- Raise before uploading: whether the course allows walkthroughs of its problems, the
  voice engine's licence terms, any figure or text copied from the notes.
- Keep the tab in the foreground while filling the form, read each field back, and
  confirm the saved visibility on the content list.
