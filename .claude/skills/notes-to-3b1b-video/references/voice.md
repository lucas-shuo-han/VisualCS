# Voice and pronunciation

Three layers, cheapest first:
1. Built in (`tts.spoken()`): operators, Greek, hex and bits, `A[i]`, snake_case, superscripts (² ᵀ ⁻¹), ‖x‖, f′, O(n), e.g. / i.e., units after numbers, lone math letters.
2. Per course (`say_as.py`): `SAY_AS` (word → spoken), `SPELL` (letter by letter), `REWRITES` (regex, applied first). Only what the course repeats.
3. Heard (`asr_check.py U N`): Whisper transcribes every clip and lists words heard wrong, pauses in the wrong place, long breathless runs, odd rate, clipped endings. CPU only. A human then listens to the flagged clips only.

The recognizer forgives a name with the wrong stress or a homograph read the other way: the user's ear on the short list covers those.

## Prosody
A beat is synthesized as one passage and cut at the engine's sentence boundaries (`tts.synth_beat`), so sentences connect instead of each starting and ending like a sentence read alone. Pauses between sentences stay `PACE`'s. `KIT_TTS_BEAT=0` reverts to sentence by sentence; Kokoro and Pico always are.
Fix a flagged pause or breath in the text: a comma where the breath belongs, a period-free form of "np.dot", a long sentence split.

## Engines (`KIT_TTS_ENGINE`)
- `edge` (default): neural, no key. A 403 from `speech.platform.bing.com` means edge-tts is outdated: `pip install -U edge-tts`.
- `kokoro`: local; `pip install kokoro-onnx`, model files in `KIT_KOKORO_DIR`. Reads "A" as the article: `A_NAME`, `LETTER_A`.
- `pico`: robotic; last resort, say so. No engine: `--no-voice`.

Choice in series.py: `TTS = {"engine": "edge", "rate": "-4%", "voice": {"en": "en-US-AndrewNeural"}}`; env overrides `KIT_VOICE_EN`, `KIT_TTS_RATE`, `KIT_TTS_ENGINE`.
The user picks voice and speed by ear before the first full render: `audition.py --unit U`.
