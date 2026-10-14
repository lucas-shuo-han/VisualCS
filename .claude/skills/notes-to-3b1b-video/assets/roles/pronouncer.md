# Brief: pronouncer

Make the voice of episode <N> in `<unit>` (`U`) say what the board means. Kit `<K>`, Python `<PY>`.
Read only: `K/references/voice.md`, the ASR report, `U/say_as.py`. Edit only `U/say_as.py`. Wording is the author's: propose, never change it.

Loop, at most three rounds:
1. `PY K/scripts/asr_check.py U <N> --out U/ASR-ep<NN>.md`
2. Per flagged sentence:
   - `word`, a term or symbol: a `SAY_AS`, `SPELL` or `REWRITES` entry (`PY U/tts.py --say "<text>"` shows the spoken form).
   - `word`, ordinary words heard as others ("with n" → "within"): a rewording for the author.
   - `pause` / `breath` / `rate`: a rewording (comma, split) for the author.
   - `cut`: report it; a kit problem.
   - recognizer plainly wrong (spoken form right and unambiguous): mark "recognizer".
3. Rerun.

Final message: entries added; rewordings proposed with sentence ids; sentences still flagged; clip paths the user should hear (names, terms, anything marked "recognizer").
