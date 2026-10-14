# Brief: pronouncer

Make the voice of episode <N> in `<unit>` (`U`) say what the board means. Kit `<K>`, Python `<PY>`. Edit only `U/say_as.py`; propose rewordings, never make them.

Loop, at most three rounds:
1. `PY K/scripts/asr_check.py U <N> --out U/ASR-ep<NN>.md`
2. Per flagged sentence:
   - `word`, a term or symbol: add a `SAY_AS`, `SPELL` or `REWRITES` entry that makes it sound right (`PY U/tts.py --say "<text>"` shows the spoken form).
   - `word`, ordinary words heard as others ("with n" → "within"): a rewording for the author.
   - `pause` / `breath` / `rate`: a rewording (comma, split) for the author.
   - `cut`: report it; it is a kit problem.
   - Whisper plainly wrong (the spoken form is right and unambiguous): mark "recognizer".
3. Rerun.

Final message: the entries added; rewordings proposed, with sentence ids; sentences still flagged; the clip paths the user should hear (names, terms, anything marked "recognizer").
