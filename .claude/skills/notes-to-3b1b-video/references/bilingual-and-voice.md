# Bilingual series and voice-over

Both features are built into `manim_kit.py` and driven by environment variables that
`render.py` sets, so an episode file is written once and rendered in every language,
with or without a voice.

## Contents
1. Choosing the source language
2. Translation tables
3. Layout differences between languages
4. Voice-over (edge-tts)
5. Pronunciation (spoken forms, say_as.py, speak=)
6. Timing

---

## 1. Choosing the source language

Write the episodes in one language (`SOURCE_LANG` in series.py) and translate from it.
If one of the languages is Chinese/Japanese/Korean, make **it** the source: the kit can
then prove a translation complete (any string containing CJK characters must have an
entry, and rendering fails on a miss), so no untranslated line slips into the other
video. With a Latin source, missing entries pass through silently and `i18n_check.py`
can only guess which strings are prose.

Write the source for the audience of that language, not as a gloss of English: first
use of a term gets the English in parentheses (立即数（immediate）), code stays code.

## 2. Translation tables

`i18n/epNN.py` next to the episodes, one dict per target language, keyed by the exact
source string:

```python
"""English for episode 5 (keys are the Chinese strings in ep05_*.py)."""
EN = {
    "每条指令都是 32 位。": "Every instruction is 32 bits.",
    "    bne s3, s4, Else  # i != j 就跳": "    bne s3, s4, Else  # jump if i != j",
}
```

- The kit patches `Text` (so every `txt()`, `mono()`, caption, heading and `box_label`)
  to look strings up; `say()` and `end_card()` translate before wrapping. `MarkupText`
  can't be looked up (its markup is generated) and must be built from translated parts.
- Code lines with comments are translated as whole lines: keep the code identical and the
  comment column aligned with the rest of the listing.
- f-strings need one entry per value they produce (the checker lists them).
- Changing a source string means re-keying its entry. Workflow:
  `i18n_check.py SRC N --skeleton` prints the missing entries ready to paste;
  `--widths` lists translations much wider than their source (layout risk).
- Draft renders: `render.py ... --lax` shows missing entries in the source language.
- Titles, subtitles and slugs are per language in series.py; the kit's own UI strings
  ("Episode n", "Recap", "Next: ...") are in `STRINGS` in manim_kit.py (add a row for a
  new language).
- Curly quotes are straightened in Latin-script renders: CJK fonts draw “” full-width.

## 3. Layout differences

English runs ~1.3–2× wider than Chinese for the same content. In order of preference:
a shorter translation; `scale_to_fit_width` on the one label; a small `if EN:` branch in
the episode. Subtitles: CJK 30 pt at 30 units per line, Latin 28 pt at 35 units, one sentence at a
time and at most two lines (keep content above y ≈ −2.9).
Always look at the contact sheets of *every* language: most translation bugs are layout.

## 4. Voice-over

`tts.py` (copy next to the kit) synthesizes each beat (one `say()`) as one clip, by default with Microsoft's
neural voices through the `edge-tts` package: good quality, many languages, no API key, but it needs
network access. Clips are cached (`KIT_TTS_CACHE`, render.py puts it in the media dir),
trimmed of leading/trailing silence, and reused across renders, so only new or changed
lines need the network.

- Defaults: en-US-AndrewNeural, zh-CN-YunxiNeural (others in `VOICES`); override with
  `KIT_VOICE_EN=...`, speed with `KIT_TTS_RATE=+5%`.
- Enabled per render: `render.py` turns it on for full renders and off for previews
  (`--voice` / `--no-voice` override).
- `title_card()` speaks "Episode n: title", `end_card()` speaks "To sum up", each bullet,
  and "Next time: ..." or the series-end line.
- Engines, in order of preference (`KIT_TTS_ENGINE`):
  1. `edge` (default): the neural voices above. Needs `speech.platform.bing.com`.
  2. `kokoro`: Kokoro-82M, a local neural model, close to edge quality and fully
     offline. `pip install kokoro-onnx`, then put `kokoro-v1.0.onnx` and
     `voices-v1.0.bin` from github.com/thewh1teagle/kokoro-onnx/releases in
     `KIT_KOKORO_DIR` (default `~/.cache/kokoro`). Default voice `af_heart` (en);
     override with `KIT_VOICE_EN=am_michael` etc. About 4x faster than real time on CPU.
  3. `pico`: SVOX Pico (`apt install libttspico-utils`). Works anywhere but sounds
     robotic; users notice. Use only when neither of the above is reachable, and say so.
- Kokoro reads a bare capital "A" or a variable "a" as the article ("uh"), and "ay" as
  "eye". tts.py therefore spells the letter A as "eigh" for Kokoro (`A_NAME`, and
  `LETTER_A` inside say_as.py): "a0" is "eigh 0", "ISA" is "I S eigh". `math_letters`
  also treats a lone `a` followed by a verb or preposition ("sets a to five", "a is a
  variable") as the letter, and leaves "by a register" or "a load" alone. Check
  `captions.py --spoken` for stray "uh"s, and look at the phonemes of risky words, which stands in for listening:
  `Kokoro(model, voices).tokenizer.phonemize("risk five", "en-us")` (kokoro_onnx) prints
  what the model will say.
- Check which hosts are reachable before choosing (a proxy may block the edge host but
  allow GitHub); try a sample line with `python tts.py --say "..." --synth`.
- Behind a TLS-inspecting proxy, tts.py adds `SSL_CERT_FILE` to edge-tts's CA list.
- No engine at all? Render without voice (`--no-voice`) and ship captions + .srt; the voice
  can be added by re-rendering later since the clips are generated from the same captions.

## 5. Pronunciation

Captions are written to be read, so `tts.spoken()` rewrites them before synthesis:
hex and bit strings digit by digit, operators as words, `A[i]` as "A of i", `2^k`,
`(n-1)!`, snake_case and camelCase split, "0s/1s", a chain of arrows as a sequence
("a, then b, then c"), a lone arrow as "to", ellipses and dashes as pauses.

Course vocabulary lives in `say_as.py` next to tts.py (see assets/say_as_asm.py for an
assembly course): `SAY_AS` (word → spoken, optionally per language), `SPELL` (read
letter by letter: "lw" → "L W", "rs1" → "R S 1"), and `REWRITES` (regex → replacement per
language, applied first: e.g. `8(sp)` → "S P plus 8"). Things learned the hard way:

- Mnemonics that are also sounds get mangled: "jal ra" was heard as "jalr a"; say "jump
  and link". Acronyms that are words ("RISC") need an explicit spoken form.
- Python's `\b` and `\w` treat CJK characters as word characters: every regex that runs
  on Chinese text needs `re.ASCII` (tts.py does this).
- One-off wording: `self.say("x ← x − η∇L", speak="x becomes x minus eta times the gradient")`.
  `speak` is translated through the table too.
- Review spoken forms in bulk: `captions.py SRC N --spoken`, before rendering.

### Math and technical terms: the "scalar a" problem

A neural voice reads *words*. It has no way to know that a letter in a sentence is a
variable. The CS61C run and later lessons turned up these failures:

| Written | Heard | Fix |
|---|---|---|
| scalar a times vector v | "scalar uh times..." (the article) | `tts.math_letters` spells out `a` → "ay" in a math context |
| 标量 a 乘以向量 v | 啊 (interjection) | math_letters uppercases lone letters in Chinese; better to write A in the caption |
| xor, xori | "X or", "X or I" | `SAY_AS`: "ex-or", "ex-or immediate" |
| andi, ori, addi | "and I", "or I" | `SAY_AS`: "and immediate", ... |
| η∇L | skipped or read as a random character | `tts.GREEK`: "eta the gradient of L" |
| I (identity matrix), e (Euler), O(n) | the pronoun "I", "eh", "oh of n" | `SAY_AS` / `REWRITES` per course, e.g. `(r"\bO\((\w+)\)", "big O of \\1")` |
| CUDA, SIMD, GPU, SQL, RISC | read as a word when it should be spelled, or the reverse | `SAY_AS` or `SPELL`, decided per term by ear (GPU spelled, CUDA a word) |

`math_letters` uses a heuristic. It spells out a lone letter when it follows a math noun
(scalar, vector, matrix, variable, register...), sits next to an operator (`a · v`,
`a = 3`, `v times a`), follows a digit (`2a`), or appears in a letter list (`a, b and c`).
Ordinary words ("a dog") are left alone. For anything it misses, use `speak=` or a
`REWRITES` rule. Add course nouns to `MATH_NOUNS` in the copied tts.py.

**Workflow per course:**
1. Run `python narration_lint.py <unit> --audition <scratch>/audition`. It lists every
   risky term (spelled letters that fuse with a word, unknown ALL-CAPS, letter+digit
   codes, leftover symbols, lone a/e/o in Chinese) and synthesizes each one in a carrier
   sentence.
2. Listen to the clips. Put what sounds wrong in `say_as.py`. Decide ALL-CAPS terms one
   by one, the way the lecturer says them.
3. Re-run until clean. Then listen to one full episode per language before the final
   render: the linter finds candidates, but your ear decides.

**Engines and control.** edge-tts is free and good, but Microsoft blocks custom SSML
there, so `<phoneme>`, `<say-as>` and `<break>` are unavailable: text rewriting is the
only lever. If a course needs exact phonemes, switch the backend in `tts.synth`:
- **Azure Speech** (same voices, needs a key): full SSML, `<phoneme alphabet="ipa">`
  and custom lexicons.
- **Kokoro** (local, open weights): inline IPA with Markdown syntax,
  `[Kokoro](/kˈOkəɹO/)`.
- **ElevenLabs / OpenAI**: pronunciation dictionaries or aliases.

Keep `spoken()` in front of any engine. Operators, hex and identifiers still need
rewriting.

## 6. Timing

With a voice, a beat lasts as long as its clip plus 0.35 s (plus `extra`), and the audio
starts 0.15 s after the first subtitle appears. The subtitle switches sentence, and a
`cue("phrase")` fires, at the moment given by the phrase's position in the text (by
character count, weighted for CJK), which is within about half a second of the voice.
Animations passed to `say()` play while it is spoken; `hold()` waits for the voice to
finish. In a translation the same cue lands at the same fraction of the translated beat,
so keep the order of ideas inside a beat the same in both languages. So a voiced episode runs
longer than the silent one (roughly +10–25%), and the voice sets the pace: if the
visuals need longer than the sentence, use `self.hold(extra)` rather than padding text.
