# Production: planning, coverage, review, parallel work, delivery

What turned a pile of scenes into a finished series (a 14-episode, two-language,
voiced CS61C RISC-V series was made this way).

## Contents
1. Coverage map (do this before planning)
2. Planning the series
3. Working with parallel agents
4. The review pass (writing + coverage + voice)
5. Keeping the user in the loop
6. Delivery checklist

---

## 1. Coverage map

When the user gives notes and says "cover the notes" (they usually mean it), build the
checklist first, then plan around it:

1. Convert every chapter to clean Markdown in a scratch folder (one file per chapter).
2. List every substantive item: concept, definition, rule, table, worked example, quick
   check / exercise, footnote. Keep the notes' own examples (with their numbers): viewers
   will meet them again in homework.
3. After planning, map item → episode. After writing, map item → caption. Anything
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
- Per episode, write down: the question it answers, the worked example (real numbers),
  the aha beat, the notes items it covers, 4–5 recap bullets.
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

1. **Coverage audit** against the checklist from §1. Add what's missing (a caption or a
   few, with a visual), keeping the episode ≤ ~8 minutes.
2. **Writing, source language.** Read every caption in order (`captions.py SRC N`), as a
   viewer. Fix: translated-sounding phrasing, vague or wrong statements, inconsistent
   terms, captions that don't match the screen at that moment, missing transitions between
   sections, repetition, captions over ~50 CJK characters / ~30 words, punctuation style.
3. **Writing, translation.** Idiomatic, concise, course terminology, the meaning not the
   words, about the same reading time as the source line.
4. **Voice.** `narration_lint.py SRC N` first. It flags split sentences, runs of short
   captions, tiny sentences and risky terms. Fix them following
   `references/narration-writing.md`. Then `captions.py SRC N --spoken` for anything a
   listener would stumble on (symbols, code fragments, long hex runs, list punctuation
   read as nothing). Reword the caption, add a pronunciation to `say_as.py`, or pass
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
      with sound.
- [ ] Narration scripts: `srt_to_script.py videos/<...>/<lang> <unit>/SCRIPT.<lang>.md`.
- [ ] README: episode table (title + what it covers, per language), how to re-render,
      how to add a translation or change a pronunciation.
- [ ] Remove superseded videos from git (old renders) rather than leaving two sets.
- [ ] Commit code, tables, videos (~8–20 MB per episode at 1080p), subtitles, scripts.
- [ ] Final message: where the videos are, the episode list, the coverage table or a
      pointer to it, notes errors found, limitations (e.g. which content came from your
      own knowledge, anything unverified).
