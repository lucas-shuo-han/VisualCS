# Pipeline: one strong author, cheap builders

For a unit of many episodes where cost matters. The decisions that make a video good
(what to say, what to draw, in which order) are made once by a strong model and written
down; the long render-look-fix loop, where most tokens go, runs on a cheap model that
is not allowed to decide anything. Each role has its own context and reads only what
its row names.

| # | Role | Model | Reads | Writes | Brief |
|---|---|---|---|---|---|
| 1 | Author | strongest (Opus) | the notes, `SKILL.md`, `references/narration-writing.md`, `derivation-episodes.md`, `visual-patterns.md` | `series.py`, `BOARD-epNN.md` per episode | `assets/roles/author.md` |
| 2 | Builder | cheap (DeepSeek, Haiku) | `STRICT.md`, the BOARD | `epNN_*.py`, `REPORT-epNN.md`, voiced 480p preview | `assets/roles/builder.md` |
| 3 | Reviewer | mid (Sonnet) | the BOARD, the contact sheets, the `.srt` | `REVIEW-epNN.md` | `assets/roles/reviewer.md` |
| 4 | Verifier | small (Haiku) | the review, the BOARD, the new sheets | a verdict per review row | `assets/roles/verifier.md` |
| 5 | Coordinator | whoever runs the job | the reports, not the notes | the 1080p render, the final message | below |

The author does words and pictures together: which word a picture changes on is one
decision, and a second model would have to load the first one's whole context to make
it. The reviewer sits at the end because judging a frame is what cheap models do worst,
and its context is small (a dozen images and the board).

There is no separate mathematics checker. The author carries that duty as a rule of
the storyboard: no step of a proof or a derivation is skipped, and a step the notes
leave out ("it is easy to see", "left as an exercise", a jump of two lines of algebra)
is worked out and added, marked as added.

## The contract between the roles

`BOARD-epNN.md` (`assets/board_template.md`) is the only thing the author hands over,
so it has to be complete enough that the builder decides nothing:

- the narration, word for word, one `### id` beat with its `> ` lines per `say()`;
- per beat, what is on the stage, what appears with the first word, and each later
  change with the exact phrase it happens on;
- the layout of each scene in words and coordinates (left block, right block, where
  the result line goes), and what stays from the scene before;
- every number, date, name and theorem with the line of the notes it comes from.

`check.py` enforces the words: with a BOARD file in the unit, the `board` stage FAILs
when a `say()` is not a beat of it, word for word and in order. The builder may not
edit the BOARD. A wording, a number or a picture it believes is wrong goes into its
report as a question, and the coordinator takes it back to the author.

## Order of work

1. **Author**, once per unit: the episode split and `series.py`, then one BOARD per
   episode. The narration lint needs code, so at this point the author holds the BOARD
   against `narration-writing.md` itself (the builder's lint will repeat it).
   **Pilot before the batch.** The author writes two boards first: the easiest episode
   and the hardest one (a proof or a long derivation). Both are built and reviewed,
   the user listens to one preview (voice and pace forced the rewrites of every
   earlier series), and what the review finds goes into the briefs as rules. Only
   then does the author write the remaining boards. Writing all the boards after one
   build repeats the first build's faults in every episode and buys a fix round each.
2. **Builder**, one per episode. At most two at once on one machine: renders that
   compete take three times as long, and a full drive corrupts the caches.
3. **Reviewer**, per episode, on the builder's last sheets. Rows it marks "author" go
   to the author, who changes the BOARD's picture lines (one message for several
   episodes); or the coordinator decides them in the review file when speed matters.
   The coordinator drops rows the sheets cannot support (a change one subtitle early
   inside a sentence). The list, as `REVIEW-epNN.md`, goes to a builder for a fix
   round. Two rounds at most; what is still open after that goes to the coordinator.
4. **Verifier**, after a fix round: a small model answers FIXED / NOT FIXED / CANNOT
   TELL per row from the new sheets. The coordinator looks at every NOT FIXED itself.
5. **Coordinator**: for each episode, `check.py U N --strict --no-render` says PASS and
   `REVIEW-epNN.md` has no open item; then the 1080p render, after the user has heard
   a preview.

## Keeping the coordinator cheap

The coordinator is usually the strongest model, and every report, review and
notification of every worker lands in its context. That cost is easy to miss, because
only the workers' tokens are printed. Three habits keep it down:

- Queue with a shell loop, not by hand: one background command runs the builders of
  a lane one after another and prints only each one's result table, so the
  coordinator is woken once per lane instead of once per step.
- Read summaries, not transcripts: the last check table and the "questions for the
  author" of a builder, the table of a reviewer. Open a contact sheet yourself only
  for a row someone marked NOT FIXED or to spot-check a verifier.
- Hand triage down: dropping review rows the sheets cannot support and writing the
  `REVIEW-epNN.md` file is work for the reviewer's own model; the author's model is
  needed only for rows that change a board.

Report the coordinator's own usage with the workers' when you report the cost of a unit.

## Before you start: is the pipeline the right tool

- Grain. Ten episodes came out of a nine-page note under "four to six minutes, skip
  no step". Ask the user how many minutes the unit deserves before the author splits
  it; an episode count is a decision, not a consequence.
- Reach. The one full run was one language, a fixed camera, tables and arrows, no
  LaTeX, the default voice. Two languages, zooms, formula-heavy derivations and an
  auditioned voice are untested in this arrangement: for those, pilot first or use
  `SKILL.md` with one strong model.
- Shortcuts leave a mark. When the coordinator decides an author's row itself or
  edits an episode's code directly to save a round, it says so in the review file
  and in the final message; otherwise the next reader takes the board for the truth.

## Running a builder on another provider

Use an existing agent harness, not a hand-written loop: the harness brings the tools,
the permission rules and the context handling. For a model behind an
Anthropic-compatible endpoint that harness is Claude Code itself, started headless
with the endpoint swapped:

```bash
MODEL=deepseek-flash bash scripts/run_with_model.sh <key file outside the repo> \
    <builder brief with the paths filled in>.txt <repo>
```

The coordinator runs this in the background from its own Claude Code session and is
told when it ends, like a sub-agent. The worker gets its own empty config folder (no
plugins, memory or hooks of the user), may not change git state, install or download,
and its final message is printed with turns, minutes and tokens. Tested with DeepSeek:
tool calls work, and it sees images through the Read tool. The key is read from the
file into the process environment; it never goes into a prompt, a repository file or a
log. A model with its own desktop harness can be given the same brief there by hand.

Claude models (Haiku, Sonnet) run as sub-agents of the coordinator with the same
brief. `scripts/agent_loop.py` is a fallback for a machine without Claude Code.

## What this has and has not been tested on

Measured on CS70 note 10 (five episodes): a cheap model working alone from `STRICT.md`
passes every mechanical gate and still makes a mediocre video, because the gates see
overlaps and empty frames, not a weak explanation. One episode cost the cheap builder
about 18 M input tokens over 165 tool calls; a mid model about 0.2 M. The split above
follows from that.

Run once end to end, on CS70 note 11 (ten episodes, about 45 minutes of video):

| Role | Model | Per episode | Whole unit |
|---|---|---|---|
| Author | Opus | 5 to 8 minutes for a board | about 1.2 M tokens, boards and two revision passes |
| Builder, first build | DeepSeek in the Claude Code harness | 14 to 70 minutes, 6 to 14 M input tokens (proof episodes are the slow ones) | about 90 M input tokens, 5.7 hours of agent time |
| Reviewer | Sonnet | 1 to 2 minutes, about 0.1 M tokens | 1 M |
| Builder, fix round | DeepSeek | 10 to 21 minutes, 1.5 to 9 M input tokens | about 59 M input tokens, 3 hours |
| Verifier | Haiku | under a minute, about 0.1 M tokens | 1 M |

Every first build passed the gate and matched its board word for word; every episode
still needed one fix round. What the reviewer found was mostly one family, now rules in
the author's and builder's briefs: the thing a beat is about drawn as the smallest text
on the frame, dashed lines too faint to see, a highlight fading with its cell, a scene
change before the last sentence had ended. The builder's questions to the author were
worth reading (a picture contradicting its caption, a count on screen that did not
prove what the voice claimed). The verifier's verdicts matched the coordinator's own
look on the frames checked; it cannot judge sizes, so write review rows in terms of
what is visible ("larger than the cell names"), not in points.

What that run does not show. Nobody listened to the voice, and the 1080p files were
not inspected, so it has not met the test that reshaped every earlier series: the
user watching and listening. Fix rounds took about 40% of the builder's tokens, most
of them avoidable with the pilot above. The coordinator's own tokens were not
measured, and they were what ran into the usage limit. The first builds needed no
narration rewrite, which no earlier series managed; whether the narration is good is
still the user's call.
