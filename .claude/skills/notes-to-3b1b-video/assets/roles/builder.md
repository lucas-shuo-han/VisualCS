# Brief: builder

Build episode <N> in `<unit>` (`U`). Kit `<K>`, Python `<PY>`. Windows: `PYTHONIOENCODING=utf-8`.

Follow `K/STRICT.md` with "With a board" in force; `U/BOARD-ep<NN>.md` is your plan.

Write only `U/ep<NN>_*.py`, `REPORT-ep<NN>.md`, `TRIAL_LOG-ep<NN>.md`. Never edit the board, `series.py`, `manim_kit.py`, `tts.py`. No git changes, downloads or installs. Other builders may be rendering: give `check.py` a 20-minute timeout, never start it twice.

Done when `PY K/scripts/check.py U <N> --strict --no-render` prints `RESULT: PASS` and the report has a line per sheet opened. If you can't write the report, put it in your final message.

Final message only:
1. preview video and `.srt` paths;
2. last check table, copied;
3. questions for the author (beat id; built as written anyway);
4. what you did not do or look at.
