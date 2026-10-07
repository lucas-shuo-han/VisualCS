# Pipeline: one strong author, cheap builders

For a unit of many episodes where cost matters. The decisions that make a video good
(what to say, what to draw, in which order) are made once by a strong model and written
down; the long render-look-fix loop, where most tokens go, runs on a cheap model that
is not allowed to decide anything. Each role has its own context and reads only what
its row names.

| # | Role | Model | Reads | Writes | Brief |
|---|---|---|---|---|---|
| 1 | Author | strongest (Opus) | the notes, `SKILL.md`, `references/narration-writing.md`, `derivation-episodes.md`, `visual-patterns.md` | `series.py`, `BOARD-epNN.md` per episode | `assets/roles/author.md` |
| 2 | Checker (optional) | a different model that is good at mathematics | the notes, the BOARD's facts and derivation rows | `FACTS-epNN.py`, corrections | `assets/roles/checker.md` |
| 3 | Builder | cheap (DeepSeek, Haiku) | `STRICT.md`, the BOARD, the FACTS file | `epNN_*.py`, `REPORT-epNN.md`, voiced 480p preview | `assets/roles/builder.md` |
| 4 | Reviewer | mid (Sonnet) | the BOARD, the contact sheets, the `.srt` | `REVIEW-epNN.md` | `assets/roles/reviewer.md` |
| 5 | Coordinator | whoever runs the job | the reports, not the notes | the 1080p render, the final message | below |

The author does words and pictures together: which word a picture changes on is one
decision, and a second model would have to load the first one's whole context to make
it. The reviewer sits at the end because judging a frame is what cheap models do worst,
and its context is small (a dozen images and the board).

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
   against `narration-writing.md` itself (the builder's lint will repeat it). Stop and show
   the user the first BOARD before writing the rest; a change of voice or depth is
   cheap now and expensive after the builders ran.
2. **Checker**, in parallel per episode, when the unit has derivations or computed
   examples: recompute, write the asserts, list disagreements. The author resolves
   every disagreement in the BOARD before a builder starts.
3. **Builder**, one per episode. At most two at once on one machine: renders that
   compete take three times as long, and a full drive corrupts the caches.
4. **Reviewer**, per episode, on the builder's last sheets. Its fix list goes back to
   the same builder (same context if it is still alive, otherwise a new one with the
   BOARD, the code and the list). Two rounds at most; what is still open after that
   goes to the coordinator.
5. **Coordinator**: for each episode, `check.py U N --strict --no-render` says PASS and
   `REVIEW-epNN.md` has no open item; then the 1080p render, after the user has heard
   a preview.

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
follows from that. The full pipeline, with an author's BOARD, has not been run yet:
the first unit made with it is the test, so keep its numbers (tokens and minutes per
role, review rounds, what the reviewer caught) in the unit's `TRIAL_LOG.md`.
