# Pipeline: strong author, cheap builders

Judgement once by a strong model; the long render-look-fix loop on cheap models that decide nothing. Each role has its own context and reads only its row.

Defaults, unless the user says otherwise: Claude sub-agents with the models below; no stops besides the two user gates in `SKILL.md`; findings of the pilot go into the briefs.

| Role | Model | Reads | Writes | Brief |
|---|---|---|---|---|
| Author | Opus | notes, `teaching.md`, `script.md`, `picture.md`, templates | `PLAN.md`, `series.py`, `BOARD-epNN.md` | `assets/roles/author.md` |
| Builder | Haiku | `STRICT.md`, the board | `epNN_*.py`, `REPORT-epNN.md`, 480p preview | `assets/roles/builder.md` |
| Pronouncer | Haiku | `voice.md`, `ASR-epNN.md` from `asr_check.py` | `say_as.py`, rewordings for the author | `assets/roles/pronouncer.md` |
| Reviewer | Sonnet | board, contact sheets, `.srt` | `REVIEW-epNN.md` | `assets/roles/reviewer.md` |
| Verifier | Haiku | review, board, new sheets | FIXED / NOT FIXED / CANNOT TELL per row | `assets/roles/verifier.md` |
| Coordinator | you | `SKILL.md`, this file, `production.md`, `voice.md` (pace), reports — not notes | 1080p render, final message | below |

## Contract
The board is the only hand-over; the builder decides nothing. It holds: exact narration (`### id` + `> ` lines per `say()`), per beat what is on stage and what changes on which phrase, layout with coordinates, every fact with its notes line. `board_lint.py` checks the board's form before hand-over; `check.py` FAILs if a `say()` differs from the board. Builder never edits the board; doubts go to its report as questions for the author.

## Order
1. Author: PLAN → user go → two pilot boards (easiest, hardest).
2. Builders on the pilots; reviewer; user hears one preview; findings become rules in the briefs.
3. Pronouncer on each pilot; its `say_as.py` serves the whole unit, so later episodes rarely flag.
4. Author boards the rest. Builders, ≤ 2 per machine.
5. Reviewer per episode. `author` rows → author edits the board; `builder` rows → fix round. ≤ 2 rounds.
6. Verifier after each fix round; coordinator looks at every NOT FIXED.
7. Coordinator: `check.py U N --strict --no-render` PASS and no open review row → 1080p render.

## Keeping the coordinator cheap
- Queue builders with a background shell loop that prints only result tables.
- Read summaries (check table, questions, review table), not transcripts.
- Reviewer's model does the triage; author only for board changes.
- Any shortcut (coordinator edits code or decides an author row) is written in the review file and final message.

## Builders on other providers
Claude models run as sub-agents. Others via Claude Code headless with a swapped endpoint:
`MODEL=deepseek-flash bash scripts/run_with_model.sh <key file outside repo> <brief>.txt <repo>`
Empty config, no git changes, no installs; key only in the process environment. Fallback without Claude Code: `scripts/agent_loop.py`.

Measured runs: `HISTORY.md`.
