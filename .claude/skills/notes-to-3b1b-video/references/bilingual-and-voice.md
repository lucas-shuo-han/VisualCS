# Two languages and the voice

Both are built into the kit and switched by environment variables that `render.py` and
`check.py` set: an episode is written once and rendered in every language, voiced or not.

## Translation

- **Source language.** If one language is Chinese, Japanese or Korean, write the
  episodes in it (`SOURCE_LANG`). Any string with CJK characters must then have a table
  entry or the render fails, so nothing untranslated slips through. With a Latin source
  a miss passes silently and `i18n_check.py` can only guess what is prose.
- **Tables.** `i18n/epNN.py`, one dict per target language (`EN = {...}`), keyed by the
  exact source string. The kit patches `Text`, so `txt()`, `mono()`, headings, captions
  and `box_label` are looked up; `say()`, `speak=` and `end_card()` too. `MarkupText`
  cannot be looked up and must be built from translated parts. Code lines with comments
  are translated whole, comment column aligned. An f-string needs one entry per value.
- **Tools.** `i18n_check.py UNIT N --skeleton` prints the missing entries ready to
  paste; `--widths` lists translations much wider than their source. A changed source
  string means re-keying its entry. `render.py --lax` drafts with holes.
- **Writing.** For the audience of that language, not a gloss: idiomatic, the meaning
  not the words, about the same reading time, course terms from GLOSSARY.md, the
  English term in parentheses on first use (立即数（immediate）).
- **Layout.** In order of preference: a shorter translation, `scale_to_fit_width` on
  that label, a small `if EN:` branch. Most translation bugs are layout: look at the
  sheets of every language. The caption wrapper can split a CJK word (洛/杉矶); reword.
- Titles and slugs per language are in series.py; the kit's own strings ("Episode n",
  "Recap") in `STRINGS` in manim_kit.py.

## Voice

`tts.py` synthesizes each sentence as its own clip, trimmed and cached
(`KIT_TTS_CACHE`); only new or changed sentences are synthesized again.

| Engine (`KIT_TTS_ENGINE`) | | |
|---|---|---|
| `edge` (default) | Microsoft neural voices through `edge-tts`, no key | needs `speech.platform.bing.com`; retries 5 times; no SSML |
| `kokoro` | Kokoro-82M, local, close to edge | `pip install kokoro-onnx`; `kokoro-v1.0.onnx` and `voices-v1.0.bin` from github.com/thewh1teagle/kokoro-onnx/releases in `KIT_KOKORO_DIR` (default `~/.cache/kokoro`) |
| `pico` | SVOX Pico | robotic, users notice: last resort, and say so |

- Test reachability first (`python tts.py --say "..." --synth`); a proxy may block
  edge and allow GitHub. Behind a TLS-inspecting proxy tts.py adds `SSL_CERT_FILE`.
- The series' choice lives in series.py:
  `TTS = {"engine": "edge", "rate": "-4%", "voice": {"en": "en-US-AndrewNeural"}, "kokoro_voice": {"en": "am_michael"}}`.
  For one render the environment wins: `KIT_VOICE_EN`, `KIT_TTS_RATE`, `KIT_TTS_ENGINE`.
- **The user chooses by ear, before the first full render.** `audition.py --unit UNIT`
  speaks one beat in six voices at three speeds into `UNIT/preview/voices/`. A request
  for "a pleasant male voice" arose because Kokoro's default `af_heart` is female; it
  got en-US-AndrewNeural.
- No engine at all: `--no-voice`, ship captions and `.srt`, add the voice later.

**Timing.** A beat lasts as long as its sentences, the pauses between them and
`PACE["beat"]`; a voiced episode runs 10 to 25% longer than the silent estimate. A cue
fires at its sentence's start plus the phrase's share of that sentence.

## Pronunciation

`tts.spoken()` rewrites a caption before synthesis: hex and bit strings digit by digit,
operators as words, `A[i]` as "A of i", snake_case split, a chain of arrows as a
sequence. Course vocabulary goes in `say_as.py` (start from `assets/say_as_asm.py`):
`SAY_AS` (word → spoken, optionally per language), `SPELL` (letter by letter), `REWRITES`
(regex → replacement per language, applied first).

A neural voice reads words and cannot know a letter is a variable:

| Written | Heard | Fix |
|---|---|---|
| scalar a times vector v | "scalar uh times" | `tts.math_letters` says "ay" after a math noun, next to an operator, after a digit, in a letter list; add course nouns to `MATH_NOUNS` |
| 标量 a 乘以向量 v | 啊 | write A in the caption, or `speak=` |
| xor, andi, ori | "X or", "and I", "or I" | `SAY_AS`: "ex-or", "and immediate" |
| jal ra | "jalr a" | say "jump and link" |
| η∇L | skipped | `tts.GREEK`; better, `speak=` with the idea |
| I, e, O(n) | the pronoun, "eh", "oh of n" | `SAY_AS` / `REWRITES`, e.g. `(r"\bO\((\w+)\)", "big O of \\1")` |
| CUDA, SIMD, GPU, RISC | a word spelled or letters read as a word | `SAY_AS` or `SPELL`, per term, the way the lecturer says it |

- Kokoro reads a bare "A" as the article and "ay" as "eye"; tts.py spells the letter
  "eigh" for it (`A_NAME`, `LETTER_A` in say_as.py). Its phonemes stand in for
  listening: `Kokoro(model, voices).tokenizer.phonemize("risk five", "en-us")`.
- Every regex that runs on Chinese text needs `re.ASCII`: `\b` and `\w` count CJK
  characters as word characters.

**Per course:** `narration_lint.py UNIT --audition DIR` lists every risky term and
synthesizes each in a carrier sentence; listen, fix `say_as.py`, repeat until clean;
read `captions.py UNIT N --spoken`; then listen to one whole episode per language. The
linter finds candidates, an ear decides.

Exact phonemes need another backend in `tts.synth` (Azure Speech with SSML, Kokoro's
inline IPA `[Kokoro](/kˈOkəɹO/)`, ElevenLabs or OpenAI dictionaries). Keep `spoken()`
in front of any engine.
