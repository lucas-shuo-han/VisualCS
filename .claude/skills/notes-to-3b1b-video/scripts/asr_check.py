"""Listen to an episode's voice-over with a speech recognizer and list what sounds wrong.

Each sentence clip (the same cached clips the render uses) is transcribed by Whisper
with word times and compared with what the voice was meant to say:

  word     words heard differently: a symbol skipped, a letter read as a word, a
           term the engine mangled. Fix in say_as.py, or reword.
  pause    a silence inside a sentence where the text has no comma (a dot in "e.g."
           or "np.dot" read as a full stop, a breath in the wrong place).
  breath   a long sentence spoken without any pause: add a comma or split it.
  rate     a sentence much faster or slower than the episode's median.
  cut      the clip ends while a word is still sounding (trimmed or cut too hard).

CPU only, no tokens. The recognizer corrects towards real words, so a name with the
wrong stress or a homograph read the other way passes: those still need an ear,
on the short list this prints, not the whole episode.

Usage:
    python asr_check.py UNIT 3                 # episode 3, report on stdout
    python asr_check.py UNIT 3 --out U/ASR-ep03.md
    python asr_check.py UNIT 3 --model base.en # faster, rougher (default small.en)
Needs `pip install faster-whisper`; the model downloads on first use.
"""

import argparse
import difflib
import re
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project import Unit, narration  # noqa: E402

PAUSE = 0.45      # s of silence inside a sentence, not at a comma
BREATH = 22       # words without a pause
RATE_DEV = 0.3    # off the median words per second by this fraction ...
RATE_MIN = 12     # ... judged only on sentences this long (short ones run fast)
CUT = 0.04        # s between the last word's end and the clip's end

_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen " \
        "fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def _int_words(n: int) -> str:
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else " " + _ONES[n % 10])
    for div, name in ((10**9, "billion"), (10**6, "million"), (1000, "thousand"), (100, "hundred")):
        if n >= div:
            rest = n % div
            return _int_words(n // div) + " " + name + ("" if rest == 0 else " " + _int_words(rest))
    return str(n)


def _num_words(m) -> str:
    s = m[0].replace(",", "")
    if "." in s:
        a, b = s.split(".", 1)
        return _int_words(int(a or 0)) + " point " + " ".join(_ONES[int(c)] for c in b)
    return _int_words(int(s))


def words(text: str) -> list[str]:
    """Comparable words: lower case, numbers spelled, punctuation and hyphens gone."""
    s = text.lower().replace("%", " percent").replace("&", " and ")
    s = re.sub(r"\d[\d,]*(?:\.\d+)?", _num_words, s)
    s = re.sub(r"[-–—/]", " ", s)
    s = re.sub(r"[^a-z' ]", " ", s)
    return [w.strip("'") for w in s.split() if w.strip("'")]


def sentences(text: str) -> list[str]:   # as manim_kit.sentences
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Z\"“(]|[^\x00-\x7f])|(?<=[。？！])\s*", text.strip())
    return [x for x in parts if x]


def beats(path: Path, scene: str):
    """(sentences, speak sentences or Nones) per say() of the episode."""
    for kind, text, speak in narration(path, scene):
        if kind != "say":
            continue
        sents = [x for p in text.split("\n") if p.strip() for x in sentences(p.strip())]
        said = [x for p in (speak or "").split("\n") if p.strip() for x in sentences(p.strip())]
        yield sents, (said if len(said) == len(sents) else [None] * len(sents))


def diff(expected: list[str], heard: list[str]) -> list[str]:
    out = []
    for op, a1, a2, b1, b2 in difflib.SequenceMatcher(a=expected, b=heard, autojunk=False).get_opcodes():
        if op != "equal":
            out.append(f"meant \"{' '.join(expected[a1:a2]) or '—'}\", heard \"{' '.join(heard[b1:b2]) or '—'}\"")
    return out


def check_clip(model, wav: Path, meant: str, dur: float):
    segs, _ = model.transcribe(str(wav), language="en", word_timestamps=True, beam_size=5,
                               condition_on_previous_text=False, vad_filter=False)
    ws = [w for s in segs for w in (s.words or [])]
    heard = " ".join(w.word.strip() for w in ws)
    found = [("word", d) for d in diff(words(meant), words(heard))]
    meant_tokens = meant.split()
    run = 0
    for i in range(1, len(ws)):
        gap = ws[i].start - ws[i - 1].end
        prev = ws[i - 1].word.strip()
        if gap >= PAUSE and not re.search(r"[,;:—–)]$", prev):
            # trust the meant text's punctuation where the recognizer dropped it
            k = min(i - 1, len(meant_tokens) - 1)
            if not re.search(r"[,;:—–)]$", meant_tokens[k] if k >= 0 else ""):
                found.append(("pause", f"{gap:.2f} s after \"{prev}\" (… {' '.join(x.word.strip() for x in ws[max(0, i-3):i+2])} …)"))
        run = 0 if gap >= 0.15 else run + 1
        if run == BREATH:
            found.append(("breath", f"{BREATH} words without a pause, up to \"{ws[i].word.strip()}\""))
    if ws and dur - ws[-1].end < CUT:
        found.append(("cut", f"last word ends {max(0, dur - ws[-1].end) * 1000:.0f} ms before the clip does"))
    n = len(words(meant))
    speech = (ws[-1].end - ws[0].start) if ws else 0
    return heard, found, (n / speech if speech > 0.5 and n >= RATE_MIN else None)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("unit")
    ap.add_argument("episode", type=int)
    ap.add_argument("--model", default="small.en")
    ap.add_argument("--out")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    unit = Unit(a.unit)
    ep = next(e for e in unit.select([a.episode]))
    sys.path.insert(0, str(unit.src))
    import tts   # the unit's copy, with its say_as.py and cache
    from faster_whisper import WhisperModel
    model = WhisperModel(a.model, device="cpu", compute_type="int8")

    rows, rates, k = [], [], 0
    for sents, said in beats(unit.path(ep), ep["scene"]):
        k += 1
        clips = tts.synth_beat(sents, "en", said)
        for j, ((wav, dur), x, sp) in enumerate(zip(clips, sents, said)):
            meant = sp if sp is not None else tts.spoken(x, "en")
            heard, found, rate = check_clip(model, wav, meant, dur)
            rows.append((f"{k}.{j + 1}", x, meant, heard, found, rate, wav))
            if rate:
                rates.append(rate)
    med = statistics.median(rates) if rates else 0
    for r in rows:
        if r[5] and med and abs(r[5] / med - 1) > RATE_DEV:
            r[4].append(("rate", f"{r[5]:.1f} words/s against a median of {med:.1f}"))

    flagged = [r for r in rows if r[4]]
    out = [f"# ASR check: episode {a.episode:02d}", "",
           f"{len(rows)} sentences, {len(flagged)} flagged, median {med:.1f} words/s, model {a.model}.", ""]
    for sid, x, meant, heard, found, _, wav in flagged:
        out += [f"## {sid}", f"- text: {x}", f"- meant: {meant}", f"- heard: {heard}"]
        out += [f"- **{kind}**: {msg}" for kind, msg in found]
        out += [f"- clip: `{wav}`", ""]
    text = "\n".join(out)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"wrote {a.out}: {len(flagged)} of {len(rows)} sentences flagged")
    else:
        print(text)


if __name__ == "__main__":
    main()
