# Voice and pronunciation

## Engines (`KIT_TTS_ENGINE`)
- `edge` (default): neural, no key, needs `speech.platform.bing.com`.
- `kokoro`: local; `pip install kokoro-onnx`, model files in `KIT_KOKORO_DIR`.
- `pico`: robotic; last resort, say so. No engine at all: `--no-voice`.

Test: `python tts.py --say "..." --synth`. Clips are per sentence and cached.

The choice lives in series.py: `TTS = {"engine": "edge", "rate": "-4%", "voice": {"en": "en-US-AndrewNeural"}}`. Env overrides: `KIT_VOICE_EN`, `KIT_TTS_RATE`, `KIT_TTS_ENGINE`.
The user picks by ear before the first full render: `audition.py --unit U` (six voices × three speeds into `U/preview/voices/`).

## Pronunciation
`tts.spoken()` handles hex and bits, operators, `A[i]`, snake_case, arrows. Course terms go in `say_as.py`: `SAY_AS` (word → spoken), `SPELL` (letter by letter), `REWRITES` (regex, applied first).

| Written | Heard | Fix |
|---|---|---|
| scalar a | "uh" | `math_letters` / `MATH_NOUNS` |
| xor, andi | "X or", "and I" | `SAY_AS` |
| η∇L | skipped | `speak=` with the idea |
| O(n), I, e | "oh of n", the pronoun | `REWRITES` |
| GPU, RISC | spelled the wrong way | `SAY_AS` / `SPELL`, as the lecturer says it |

- Kokoro reads "A" as the article: `A_NAME`, `LETTER_A`. Check phonemes with `tokenizer.phonemize`.
- `narration_lint.py U --audition DIR` synthesizes each risky term; listen, fix, repeat. Then `captions.py U N --spoken`, then one whole episode by ear.
