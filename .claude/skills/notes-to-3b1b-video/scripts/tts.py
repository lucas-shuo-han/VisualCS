"""Voice-over for the captions: Microsoft's neural voices via the `edge-tts`
package (needs network access, no API key), cached as trimmed .wav files.

Copy this file next to manim_kit.py; the kit calls `synth()` for every caption
when KIT_TTS=1. Check what the voice will say with the skill's captions.py
(`--spoken`), or `python tts.py --say "lw t0, 8(sp)" --lang en`.

Captions are written to be read, so `spoken()` first rewrites what a voice
would stumble over: hex constants and bit strings are spelled digit by digit,
operators become words, A[i] becomes "A of i", a chain of arrows becomes a
sequence, and so on. Course vocabulary comes from an optional say_as.py next
to this file:

    SAY_AS = {"RISC-V": "risk five", "jal": "jump and link",
              "SGD": {"en": "S G D", "zh": "随机梯度下降"}}   # word -> spoken
    SPELL = ["lw", "sw", "rs1"]           # read letter by letter ("R S 1")
    REWRITES = [(regex, {"en": repl, "zh": repl})]   # applied first; repl is a
                                          # re.sub replacement or f(match)

Environment: KIT_TTS_CACHE (cache dir), KIT_VOICE_<LANG> (e.g.
KIT_VOICE_EN=en-US-AvaNeural), KIT_TTS_RATE (e.g. "+5%").
"""

from __future__ import annotations

import asyncio
import hashlib
import os
import re
import sys
import time
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = Path(os.environ.get("KIT_TTS_CACHE") or HERE / ".tts_cache")
RATE = os.environ.get("KIT_TTS_RATE", "+0%")

VOICES = {
    "en": "en-US-AndrewNeural", "zh": "zh-CN-YunxiNeural", "ja": "ja-JP-KeitaNeural",
    "ko": "ko-KR-InJoonNeural", "es": "es-ES-AlvaroNeural", "fr": "fr-FR-HenriNeural",
    "de": "de-DE-ConradNeural",
}


def voice_for(lang: str) -> str:
    return os.environ.get(f"KIT_VOICE_{lang.upper()}") or VOICES.get(lang, VOICES["en"])


# ---------------------------------------------------------------- course vocabulary

def _load_say_as():
    ns: dict = {}
    p = HERE / "say_as.py"
    if p.exists():
        exec(compile(p.read_text(encoding="utf-8"), str(p), "exec"), ns)
    say = dict(ns.get("SAY_AS", {}))
    for w in ns.get("SPELL", []):
        head, digits = re.match(r"(.*?)(\d*)$", w).groups()
        say.setdefault(w, " ".join(head.upper()) + (f" {digits}" if digits else ""))
    return say, list(ns.get("REWRITES", []))


SAY_AS, REWRITES = _load_say_as()
_SAY_RE = None
if SAY_AS:
    keys = sorted(SAY_AS, key=len, reverse=True)
    _SAY_RE = re.compile("|".join(
        (r"\b" if k[0].isalnum() or k[0] == "_" else "") + re.escape(k)
        + (r"\b" if k[-1].isalnum() or k[-1] == "_" else "") for k in keys), re.A)


def _say_as(word: str, lang: str) -> str:
    v = SAY_AS[word]
    return v.get(lang, v.get("en", word)) if isinstance(v, dict) else v


# ---------------------------------------------------------------- spoken form

_WORDS = {
    "zh": {"==": " 等于 ", "!=": " 不等于 ", ">=": " 大于等于 ", "<=": " 小于等于 ",
           "≥": " 大于等于 ", "≤": " 小于等于 ", "<<": " 左移 ", ">>": " 右移 ",
           "<": " 小于 ", ">": " 大于 ", "=": " 等于 ", "+": " 加 ", "×": " 乘 ", "·": " 乘 ",
           "±": "正负 ", "≈": " 约等于 ", "→": " 到 ", "–": " 到 ", "minus": " 减 ", "neg": "负 ",
           "star": " 星号 ", "fact": " 的阶乘", "hex": "零x ", "of": "{a} 的第 {i} 项",
           "pow": "{a} 的 {b} 次方", "#": " 井号 ", "/": "，", " / ": "、", "&": " 和 ", "|": "，",
           "then": "，", "pause": "，", "0s": "0", "1s": "1"},
    "en": {"==": " equals ", "!=": " is not equal to ", ">=": " is greater than or equal to ",
           "<=": " is less than or equal to ", "≥": " is at least ", "≤": " is at most ",
           "<<": " shifted left by ", ">>": " shifted right by ", "<": " is less than ",
           ">": " is greater than ", "=": " equals ", "+": " plus ", "×": " times ", "·": " times ",
           "±": "plus or minus ", "≈": " is about ", "→": " to ", "–": " through ", "minus": " minus ",
           "neg": "negative ", "star": " star ", "fact": " factorial", "hex": "hex ",
           "of": "{a} of {i}", "pow": "{a} to the {b}", "#": " hash ", "/": " or ", " / ": " and ",
           "&": " and ", "|": ", ", "then": ", then ", "pause": ", ", "0s": "zeros", "1s": "ones"},
}


def spoken(text: str, lang: str) -> str:
    """What the voice should say for caption `text`."""
    w = _WORDS.get(lang, _WORDS["en"])

    def sub(pat, rep, s):   # ASCII \w and \b: CJK must not count as word characters
        return re.sub(pat, rep, s, flags=re.A)

    s = text.replace("\n", " ")
    for pat, reps in REWRITES:
        rep = reps.get(lang, reps.get("en")) if isinstance(reps, dict) else reps
        if rep is not None:
            s = sub(pat, (lambda m, r=rep: r(m)) if callable(rep) else rep, s)
    # pauses and decorations
    s = sub(r"^[…\s]+", "", s)
    s = sub(r"[…]+|——|—", w["pause"], s)
    s = s.replace("“", "").replace("”", "").replace('"', "")
    # hex constants, digit by digit; long 0/1 strings (bit patterns) likewise
    s = sub(r"\b0x([0-9A-Fa-f]+)\b", lambda m: w["hex"] + " ".join(m[1].upper()), s)
    s = sub(r"\b(0[01]{3,}|[01]{5,})\b", lambda m: " ".join(m[1]), s)
    # A[i] -> "A of i";  2^k;  (n - 1)!;  *p
    s = sub(r"\b([A-Za-z]\w*)\[(\w+)\]", lambda m: w["of"].format(a=m[1], i=m[2]), s)
    s = sub(r"(\w+)\^(\w+)", lambda m: w["pow"].format(a=m[1], b=m[2]), s)
    s = sub(r"\)!", ")" + w["fact"], s)
    s = sub(r"(?<![\w)])\*(?=\w)|(?<=\s)\*(?=\s)|(?<=\w)\*", w["star"], s)
    # identifiers: learning_rate, sumSquare
    s = sub(r"\b(\w+)_(\w+)\b", r"\1 \2", s)
    s = sub(r"\b([a-z]+)([A-Z][a-z]+)\b", r"\1 \2", s)
    # course vocabulary
    if _SAY_RE is not None:
        s = _SAY_RE.sub(lambda m: _say_as(m[0], lang), s)
    s = sub(r"\b([01])s\b", lambda m: w[m[0]], s)          # "0s" -> zeros
    s = sub(r"\b(\d)([a-rt-z])\b", r"\1 \2", s)            # 4i
    # a chain of arrows is a sequence of steps; a single one is "to"
    if s.count("→") >= 2:
        s = sub(r"\s*→\s*", w["then"], s)
    # operators (longest first); a minus is binary between spaces, else unary
    s = sub(r"\s[−-]\s", w["minus"], s)
    s = sub(r"−(?=\d)", w["neg"], s)
    s = sub(r"(?<=\s)-(?=\d)", w["neg"], s)
    for op in ("==", "!=", ">=", "<=", "<<", ">>", "≥", "≤", "<", ">", "=", "+", "×", "±", "≈",
               "→", "–", "#"):
        s = s.replace(op, w[op])
    s = sub(r"(?<=\w)·(?=\w)", w["·"], s)                # w·x is a product ...
    s = s.replace(" · ", w["pause"])                       # ... "a · b" a list separator
    s = sub(r"(?<=\w)/(?=\w)", w["/"], s)
    s = s.replace(" / ", w[" / "]).replace("&", w["&"]).replace("|", w["|"])
    s = sub(r"\s+", " ", s).strip(" ,，")
    return s


# ---------------------------------------------------------------- synthesis


def _key(text: str, lang: str) -> str:
    return hashlib.sha1(f"{voice_for(lang)}|{RATE}|{text}".encode()).hexdigest()[:16]


def _duration(path: Path) -> float:
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


async def _edge(text: str, voice: str, out: Path):
    import edge_tts
    await edge_tts.Communicate(text, voice, rate=RATE).save(str(out))


def synth(caption: str, lang: str, speak: str | None = None) -> tuple[Path, float]:
    """(wav path, seconds) of the voice-over for `caption` (or `speak` verbatim)."""
    text = speak if speak is not None else spoken(caption, lang)
    d = CACHE / lang
    wav = d / f"{_key(text, lang)}.wav"
    if wav.exists():
        return wav, _duration(wav)
    d.mkdir(parents=True, exist_ok=True)
    mp3 = wav.with_suffix(f".{os.getpid()}.mp3")
    for attempt in range(5):
        try:
            asyncio.run(_edge(text, voice_for(lang), mp3))
            break
        except Exception as e:  # network hiccups, throttling
            if attempt == 4:
                raise RuntimeError(f"TTS failed for {text!r}: {e}") from e
            time.sleep(2 + 3 * attempt)
    # decode with PyAV (a Manim dependency), so no ffmpeg binary is needed
    from manim.scene.scene_file_writer import convert_audio
    from pydub import AudioSegment
    from pydub.silence import detect_leading_silence

    raw = wav.with_suffix(f".{os.getpid()}.raw.wav")
    convert_audio(mp3, raw, "pcm_s16le")
    seg = AudioSegment.from_file(raw)
    lead = detect_leading_silence(seg, silence_threshold=-45.0)
    tail = detect_leading_silence(seg.reverse(), silence_threshold=-45.0)
    seg = seg[max(0, lead - 40):max(lead + 1, len(seg) - max(0, tail - 80))]
    tmp = wav.with_suffix(f".{os.getpid()}.tmp.wav")
    seg.export(tmp, format="wav")
    os.replace(tmp, wav)   # atomic: parallel renders may synthesize the same line
    for f in (mp3, raw):
        f.unlink(missing_ok=True)
    return wav, _duration(wav)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="print (and optionally synthesize) the spoken form")
    ap.add_argument("--say", required=True)
    ap.add_argument("--lang", default="en")
    ap.add_argument("--synth", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    print(spoken(a.say, a.lang))
    if a.synth:
        print(*synth(a.say, a.lang))
