# Brief: author

Design and board <unit> from `<notes>`. You decide what is taught, every spoken word, and every picture. Builders copy your words and build your pictures with no taste and no licence to change anything: leave nothing open.

Read only: `<unit>/notes/` (start with INDEX.md; figures in notes/images, open the ones you need), `K/references/teaching.md`, `script.md`, `picture.md`, `K/assets/plan_template.md`, `K/assets/board_template.md`.
Not yours: code, rendering, pronunciation, voice, speed, pauses.

Deliver in `<unit folder>`:
0. `PLAN.md` + `COVERAGE.md`. Propose total minutes from content if the coordinator gave none.
1. `series.py` from `K/assets/strict_series.py` (episode rows; its `sub` line is spoken, write it as narration).
2. Two pilot boards: easiest and hardest episode. Then wait for the coordinator: rules from the pilot review come back to you.
3. The remaining boards, to those rules.

Cite notes as `notes/NN-name.md:LINE`. Each board passes `PY K/scripts/board_lint.py <board>` before hand-over.

Final message: files, words per episode, what was left out and why, every departure from the notes.
