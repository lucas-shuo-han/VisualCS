# Brief: builder

Build episode <N> of the unit in `<unit folder>` (`U`). The kit folder is `<K>`, the
Python is `<PY>`. On Windows set `PYTHONIOENCODING=utf-8` first.

Read `K/STRICT.md` and follow it, with the section "With a storyboard" in force:
`U/BOARD-ep<NN>.md` is your plan. Its `> ` lines are the narration, to be copied
unchanged; its stage and change lines are the picture, to be built as written.

You may write only inside `U`, and only `ep<NN>_*.py`, `REPORT-ep<NN>.md` and
`TRIAL_LOG-ep<NN>.md`. Do not edit the BOARD, `series.py`, `manim_kit.py`, `tts.py`.
No git commands that change anything, no downloads, no installs. Other builders may be
rendering on this machine: give `check.py` a timeout of twenty minutes and do not
start it a second time while it runs.

You are done when `PY K/scripts/check.py U <N> --strict --no-render` prints
`RESULT: PASS` and `REPORT-ep<NN>.md` has a line for every sheet you opened. If your
tools refuse to create the report file, put its full text at the end of your final
message instead.

Final message, nothing else:
1. the path of the preview video and its `.srt`;
2. the result table of the last `check.py` run, copied;
3. questions for the author: any beat whose words, number or picture you think is
   wrong, with the beat id (you built it as written anyway);
4. what you did not do or did not look at.
