# Pipeline: strong author, cheap builders

Judgement once by a strong model; the long render-look-fix loop on cheap models that decide nothing. Each role has its own context and reads only its row.

| Role | Model | Reads | Writes | Brief |
|---|---|---|---|---|
| Author | strongest | notes, `SKILL.md`, narration-writing, derivation-episodes, visual-patterns | `PLAN.md`, `series.py`, `BOARD-epNN.md` | `assets/roles/author.md` |
| Builder | cheap | `STRICT.md`, the board | `epNN_*.py`, `REPORT-epNN.md`, 480p preview | `assets/roles/builder.md` |
| Reviewer | mid | board, contact sheets, `.srt` | `REVIEW-epNN.md` | `assets/roles/reviewer.md` |
| Verifier | small | review, board, new sheets | FIXED / NOT FIXED / CANNOT TELL per row | `assets/roles/verifier.md` |
| Coordinator | you | reports, not notes | 1080p render, final message | below |

## Contract
The board is the only hand-over; the builder decides nothing. It holds: exact narration (`### id` + `> ` lines per `say()`), per beat what is on stage and what changes on which phrase, layout with coordinates, every fact with its notes line. `check.py` FAILs if a `say()` differs from the board. Builder never edits the board; doubts go to its report as questions for the author.

## Order
1. Author: PLAN → user go → two pilot boards (easiest, hardest).
2. Builders on the pilots; reviewer; user hears one preview; findings become rules in the briefs.
3. Author boards the rest. Builders, ≤ 2 per machine.
4. Reviewer per episode. `author` rows → author edits the board; `builder` rows → fix round. ≤ 2 rounds.
5. Verifier after each fix round; coordinator looks at every NOT FIXED.
6. Coordinator: `check.py U N --strict --no-render` PASS and no open review row → 1080p render.

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
