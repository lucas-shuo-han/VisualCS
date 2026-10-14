# Narration

Heard, not read. `narration_lint.py` catches the mechanical cases; then read each scene's beats in order in your head. If it sounds like bullet points, it is.

## Beats
- New beat when the picture changes subject, not per sentence. 2–4 sentences, 8–25 s.
- `\n` in a beat = paragraph pause; needed past ~60 words, at a turn of thought.
- Cue phrase: copied from the beat, a few words, unique in it.
- A silent demonstration goes between two beats.

## Rules
- Sentences 10–25 words, varied, each starting from the last ("so", "which means", "now").
- Plain words, contractions, at most one subordinate clause.
- Numbers and symbols as words; round aloud, exact value on screen. No colons.
- One name per thing (GLOSSARY.md).
- Never split a sentence across two `say()`; never a run of short beats; no slide fragments ("Why 12 bits?", "Done!").
- Notation on screen, idea aloud. If the subtitle must carry notation: `say("x ← x − η∇L", speak="Each step moves x a little against the gradient.")`, same sentence count. Needed in over a third of beats → too symbolic.

## Pace
- `pace.py`: 135–150 wpm including pauses was accepted; 180 too fast, 120 slow.
- `PACE` (sentence / paragraph / beat, seconds): default 0.4 / 1.0 / 0.8, derivation 0.75 / 1.6 / 1.8. Then `TTS["rate"]` ("-4%" chosen). A slower voice without pauses sounds drugged.
- A new formula gets a second of quiet: cue it at its sentence start, end the paragraph after.
- Pauses add ~50% to running time; tell the user, offer to split. Never cut words to slow down.
