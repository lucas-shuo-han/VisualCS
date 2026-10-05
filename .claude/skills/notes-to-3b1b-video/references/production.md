# Production: planning, coverage, review, parallel work, delivery

What turned a pile of scenes into a finished series (a 14-episode, two-language,
voiced CS61C RISC-V series was made this way). For one long derivation, or polishing a
video with the user over several rounds, read `derivation-episodes.md` as well.

## Contents
1. Coverage map (do this before planning)
2. Planning the series
3. Working with parallel agents
4. The review pass (writing + coverage + voice)
5. Keeping the user in the loop
6. Delivery checklist
7. Publishing (YouTube and the like)

---

## 1. Coverage map

When the user gives notes and says "cover the notes" (they usually mean it), build the
checklist first, then plan around it:

1. Convert every chapter to clean Markdown in a scratch folder (one file per chapter).
2. List every substantive item: concept, definition, rule, table, worked example, quick
   check / exercise, footnote. Keep the notes' own examples (with their numbers): viewers
   will meet them again in homework.
3. After planning, map item → episode. After writing, map item → beat. Anything
   substantive that no episode covers is a bug; trivia and tangents may be omitted but
   the omission is written down with its reason ("anecdote", "image not reproducible",
   "beyond scope", "covered in episode N").
4. Keep the table (`COVERAGE.md`, or in each agent's final report). It answers the user's
   inevitable "did you miss anything?".

Notes contain errors. Recompute every example; when the notes are wrong (an encoding
that doesn't match its listing, a register clobbered by the example code, "Hello, %s"
vs "Hello, %s!" changing an offset), show the correct version and list the discrepancy
in the final report.

## 2. Planning the series

- **Episode length follows content.** One idea with one worked example: 3–4 minutes.
  Covering a notes chapter fully: 6–8 minutes. Above ~8 minutes, split into two episodes.
  A short episode next to 7-minute ones reads as "thin"; if the notes have more, add it.
- Per episode, fill the block in `assets/plan_template.md`: the question it answers, the
  worked example (real numbers), the aha moment, a scene list (picture, what the
  narration must get across, notes items covered), 4–5 recap bullets.
- Order within an episode: a concrete case, then the rule; the reason, then the
  definition; the question, then its answer. If a scene's plan reads "state X", ask what
  the viewer would have to see to say X themselves.
- Put the order and titles in `series.py` (assets/series_template.py): numbers, "next
  episode" lines, the series-end card and file names then stay consistent through any
  reordering. Episode 1 introduces the whole series; the last one ends with a recap of it.
- Write a `GLOSSARY.md` of terms (and, bilingual, their translation): one form per concept
  across all episodes and agents ("pseudo-instruction", not also "pseudoinstruction").
- Save the plan as `PLAN.md`, commit it, and continue without waiting unless the user
  asked to approve it.

## 3. Working with parallel agents

One agent per episode (or per pair of related episodes) works well once the kit, the
series list, one or two finished example episodes and the brief exist. Before that, write
episodes yourself: the first episodes define the house style the agents copy.

- **Brief** (assets/agent_brief_template.md): project layout, hard rules, commands, API,
  layout and writing rules, "done means". Each agent prompt then only names the episode,
  its files, its notes chapter(s) and the episodes before/after it (to avoid overlap).
- **Ownership.** Each agent edits only its episode file and its table. Shared files (kit,
  series.py, scripts, README) belong to the coordinator; agents report kit bugs instead
  of fixing them. No agent runs state-changing git; the coordinator commits after
  checking `i18n_check.py` and skimming the contact sheets.
- **Concurrency.** Three agents at a time is a good ceiling: each renders previews, and
  a laptop has ~8 cores. Each agent renders one video at a time; the coordinator's own
  batch renders use `--jobs` ≈ cores / 2. Too many at once and everything slows down
  and rate limits hit more often.
- **Interruptions.** Usage limits stop agents mid-task. Agents keep `STATE.md` in their
  scratch folder; resume the same agent ("continue where you left off") rather than
  starting a new one.
- **Reviewers.** A fresh agent reviewing two episodes against their notes chapter finds
  what the author missed (translated-sounding phrasing, a term used two ways, an item
  skipped). Give it the same brief plus the review checklist below.

## 4. The review pass

Run it per episode (or per pair) after the episode renders cleanly:

1. **Coverage audit** against the checklist from §1. Add what's missing (a beat, with
   its picture), keeping the episode ≤ ~8 minutes.
2. **Writing, source language.** Read every beat in order (`captions.py SRC N`), as a
   viewer. Fix: translated-sounding phrasing, vague or wrong statements, inconsistent
   terms, sentences that don't match the screen at that moment, missing transitions between
   sections, repetition, sentences over ~60 CJK characters / ~30 words, colons.
3. **Writing, translation.** Idiomatic, concise, course terminology, the meaning not the
   words, about the same reading time as the source line.
4. **Voice.** `narration_lint.py SRC N` first. It flags split sentences, runs of short
   beats, tiny and over-long sentences, colons, numerals and risky terms. Fix them following
   `references/narration-writing.md`. Then `captions.py SRC N --spoken` for anything a
   listener would stumble on (symbols, code fragments, long hex runs, list punctuation
   read as nothing). Reword the sentence, add a pronunciation to `say_as.py`, or pass
   `speak=` for that one line. Finally, **listen** to one voiced preview per language
   end to end. Reading the spoken text doesn't catch prosody.
5. **Frames.** Re-render changed episodes and look at the end + mid sheets again.

## 5. Keeping the user in the loop

- Show a watchable result early: after the first finished episode, send the 480p preview.
  Users want to *see* the series long before it is done.
- When the user asks for "something to watch quickly", render 480p previews with
  `--voice` in one language only, `--jobs` ≈ cores / 2, and send each video as it
  finishes rather than waiting for the batch.
- Review clips always have the voice and the subtitles on the frame, and are short: one scene per clip. Give the exact path of every file. A silent clip with a separate subtitle file is not reviewable.
- For a large rework, write the task list first and report against it; decide details yourself and list them, ask only what the user alone can decide. See `derivation-episodes.md` §5.
- Final renders (1080p30, every language, voice) take a long time; run them in the
  background once, after the review pass, and tell the user where the files will land.

## 6. Delivery checklist

- [ ] `i18n_check.py SRC` ok for every episode (bilingual).
- [ ] Final render: `render.py SRC --out videos/<course>-<unit>` (voice on by default).
- [ ] A 1080p contact sheet spot check of two or three episodes; play one start to end
      with sound. `pace.py` on the output folder; put the numbers in the report.
- [ ] Narration scripts: `srt_to_script.py videos/<...>/<lang> <unit>/SCRIPT.<lang>.md`.
- [ ] README: episode table (title + what it covers, per language), how to re-render,
      how to add a translation or change a pronunciation.
- [ ] Superseded videos (old renders): ask before removing them. One user wanted the old
      single episode kept beside the new three.
- [ ] Commit code, tables, videos (~8–20 MB per episode at 1080p), subtitles, scripts.
- [ ] Final message: where the videos are, the episode list, the coverage table or a
      pointer to it, notes errors found, limitations (e.g. which content came from your
      own knowledge, anything unverified).

## 7. Publishing (YouTube and the like)

Only when the user asks, and with their account open in their own browser. Never ask
for a password.

- **Private first.** Upload as Private (or Unlisted) and let the user decide about
  Public after watching it on the site.
- **The user puts the files in.** Browser automation cannot hand a 20 to 50 MB video to
  an upload dialog, and it must not be cut into pieces to get it through. Open the
  upload dialog, ask the user to drag the files in, then fill in every field for them.
- **Title**: the episode title with a part number. No other creator's name or logo in
  the title or thumbnail.
- **Description**, the same block on every episode after a one-line summary:
  - an unofficial, student-made study video; not affiliated with, endorsed by or
    reviewed by the university, the course or its staff; not official course material
    and not a solution key; mistakes are the author's;
  - how it was made: script and animation code with an AI coding assistant (name it),
    directed and reviewed by the author; the narration is a synthetic voice; animated
    with Manim Community Edition; style inspired by 3Blue1Brown, with no affiliation;
  - thanks: the course staff, the Manim developers, whoever else helped;
  - not monetized, and an offer to change or remove on request;
  - a link to the code if the repository is public (check; do not assume).
- **Settings**: not made for kids; no paid promotion; leave monetization untouched.
  Answer the platform's AI-use question as it is worded. YouTube's asks about realistic
  altered or synthetic content (a real person, real footage, a realistic scene); an
  abstract animation with a synthetic narrator is "No" there, and the description
  carries the plain disclosure. Tell the user which answer you chose and why.
- **Risks to raise before uploading**, so the user decides: whether the course allows
  solutions or walkthroughs of its problems to be posted (and whether official solutions
  are already out); the licence terms of the voice engine, which matter more once a
  video earns money; any figure or text copied from the notes.
- Keep the browser tab in the foreground while filling the form: a background tab stops
  rendering and typed text is lost. Read each field back after filling it, and confirm
  the saved visibility on the content list.
