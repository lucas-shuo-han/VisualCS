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
the episode. Captions: CJK 30 pt at 30 units per line, Latin 28 pt at 35 units, up to
three lines (the top of a 3-line caption reaches y ≈ −2.6, so keep content above −2.5).
Always look at the contact sheets of *every* language: most translation bugs are layout.

## 4. Voice-over

`tts.py` (copy next to the kit) synthesizes each caption with Microsoft's neural voices
through the `edge-tts` package: good quality, many languages, no API key, but it needs
network access. Clips are cached (`KIT_TTS_CACHE`, render.py puts it in the media dir),
trimmed of leading/trailing silence, and reused across renders, so only new or changed
lines need the network.

- Defaults: en-US-AndrewNeural, zh-CN-YunxiNeural (others in `VOICES`); override with
  `KIT_VOICE_EN=...`, speed with `KIT_TTS_RATE=+5%`.
- Enabled per render: `render.py` turns it on for full renders and off for previews
  (`--voice` / `--no-voice` override).
- `title_card()` speaks "Episode n: title", `end_card()` speaks "To sum up", each bullet,
  and "Next time: ..." or the series-end line.
- No network? Render without voice (`--no-voice`) and ship captions + .srt; the voice can
  be added by re-rendering later since the clips are generated from the same captions.

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

## 6. Timing

With a voice, a caption stays up for max(reading time, audio + 0.35 s) plus `extra`, and
the audio starts 0.15 s after the caption appears. Animations passed to `say()` play
while it is spoken; `hold()` waits for the voice to finish. So a voiced episode runs
longer than the silent one (roughly +10–25%), and the voice sets the pace: if the
visuals need longer than the sentence, use `self.hold(extra)` rather than padding text.
