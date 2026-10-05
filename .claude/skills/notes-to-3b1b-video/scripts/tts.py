"""Voice-over for the captions, cached as trimmed .wav files. Engines
(KIT_TTS_ENGINE): "edge" = Microsoft's neural voices via the `edge-tts` package
(default; needs network access to speech.platform.bing.com, no API key);
"kokoro" = Kokoro-82M, a local neural model (near edge quality, fully offline);
"pico" = SVOX Pico, robotic, only when nothing else is available.

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


def _series() -> dict:
    ns: dict = {}
    f = HERE / "series.py"
    if f.exists():
        exec(compile(f.read_text(encoding="utf-8"), str(f), "exec"), ns)
    return ns.get("TTS", {})


# The series' voice, chosen once by ear (audition.py) and kept in series.py:
#   TTS = {"engine": "edge", "rate": "-4%", "voice": {"en": "en-US-AndrewNeural"},
#          "kokoro_voice": {"en": "am_michael"}}
# The environment variables below still win, so one render can try something else.
_SERIES_TTS = _series()
RATE = os.environ.get("KIT_TTS_RATE") or _SERIES_TTS.get("rate", "+0%")
# "edge": Microsoft neural voices, online (speech.platform.bing.com).
# "kokoro": Kokoro-82M neural voices, offline once the model files are downloaded
#   (pip install kokoro-onnx; kokoro-v1.0.onnx + voices-v1.0.bin from
#   github.com/thewh1teagle/kokoro-onnx/releases, in KIT_KOKORO_DIR).
# "pico": SVOX Pico (apt install libttspico-utils): offline, robotic, last resort.
ENGINE = os.environ.get("KIT_TTS_ENGINE") or _SERIES_TTS.get("engine", "edge")
KOKORO_DIR = Path(os.environ.get("KIT_KOKORO_DIR") or Path.home() / ".cache" / "kokoro")
# How to write the letter A so the voice says its name. Kokoro (espeak) reads "ay" as "eye"
# and a bare capital A as the article ("uh"); "eigh" gives /eI/ in any context. edge is fine with "ay".
A_NAME = "eigh" if ENGINE == "kokoro" else "ay"
KOKORO_VOICES = {"en": ("af_heart", "en-us"), "zh": ("zf_xiaoxiao", "cmn"), "ja": ("jf_alpha", "ja"),
                 "es": ("ef_dora", "es"), "fr": ("ff_siwis", "fr-fr")}
PICO_LANG = {"en": "en-US", "de": "de-DE", "fr": "fr-FR", "es": "es-ES", "it": "it-IT"}

VOICES = {
    "en": "en-US-AndrewNeural", "zh": "zh-CN-YunxiNeural", "ja": "ja-JP-KeitaNeural",
    "ko": "ko-KR-InJoonNeural", "es": "es-ES-AlvaroNeural", "fr": "fr-FR-HenriNeural",
    "de": "de-DE-ConradNeural",
}


def voice_for(lang: str) -> str:
    return (os.environ.get(f"KIT_VOICE_{lang.upper()}") or _SERIES_TTS.get("voice", {}).get(lang)
            or VOICES.get(lang, VOICES["en"]))


# ---------------------------------------------------------------- course vocabulary

def _load_say_as():
    ns: dict = {"LETTER_A": A_NAME}   # say_as.py: use LETTER_A where it spells a register like a0
    p = HERE / "say_as.py"
    if p.exists():
        exec(compile(p.read_text(encoding="utf-8"), str(p), "exec"), ns)
    say = dict(ns.get("SAY_AS", {}))
    for w in ns.get("SPELL", []):
        head, digits = re.match(r"(.*?)(\d*)$", w).groups()
        letters = " ".join(A_NAME if c in "aA" else c.upper() for c in head)
        say.setdefault(w, letters + (f" {digits}" if digits else ""))
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


# Greek letters by name (a voice may skip them or read "alpha" in another language).
GREEK = {"α": "alpha", "β": "beta", "γ": "gamma", "δ": "delta", "ε": "epsilon", "ζ": "zeta",
         "η": "eta", "θ": "theta", "λ": "lambda", "μ": "mu", "π": "pi", "ρ": "rho",
         "σ": "sigma", "τ": "tau", "φ": "phi", "χ": "chi", "ψ": "psi", "ω": "omega",
         "Δ": "delta", "Σ": "sigma", "Π": "pi", "Ω": "omega", "∇": "the gradient of ",
         "∂": "partial ", "∑": "the sum of ", "∈": " in ", "∞": "infinity", "√": "root "}

# A lone letter used as a math variable is read as a *word* by neural voices:
# "scalar a times vector v" comes out as the article "uh", "I" as the pronoun,
# Chinese voices read a lone "a" as the interjection 啊. Spell such letters out.
LETTER_NAMES = {"en": {"a": A_NAME, "A": A_NAME, "e": "ee", "o": "oh", "u": "you", "y": "why"},
                "zh": {c: c.upper() for c in "abcdefghijklmnopqrstuvwxyz"}}
MATH_NOUNS = {"en": r"scalar|vector|matrix|variable|constant|element|entry|point|set|node|"
                    r"vertex|function|parameter|coefficient|register|array|value|number|"
                    r"integer|input|output|weight|bias|term|letter|index|basis|version|option",
              "zh": r"标量|向量|矩阵|变量|常数|元素|点|集合|节点|函数|参数|系数|寄存器|数组|值|数|下标"}
# words (and punctuation) that never follow the article "a": "sets a to five", "load a into t1"
_NOT_AFTER_ARTICLE = {",", ".", ";", "?", "!", ":", "is", "are", "was", "were", "to", "into", "of",
                      "and", "or", "but", "with", "from", "has", "have", "goes", "starts", "becomes",
                      "holds", "gets"}
_OPS = set("=+×·*/^<>≤≥≈∈−-") | {"times", "plus", "minus", "over", "equals", "by",
                                  "乘", "加", "减", "除以", "等于"}
_TOK = re.compile(r"[A-Za-z]+|\d+|[一-鿿]+|[^\sA-Za-z\d一-鿿]")


def math_letters(s: str, lang: str) -> str:
    """Spell out single-letter variables in a math context: after a math noun
    ("vector a", "向量 a"), next to an operator ("a · v", "a = 3", "v times a"),
    after a digit ("2a") or in a list of letters ("a, b and c"). Ordinary
    words ("a dog") are left alone."""
    names = LETTER_NAMES.get(lang[:2])
    if not names:
        return s
    nouns = re.compile(rf"(?:{MATH_NOUNS.get(lang[:2], MATH_NOUNS['en'])})$", re.I)
    toks = [(m.start(), m.end(), m[0]) for m in _TOK.finditer(s)]
    single = lambda t: len(t) == 1 and t.isalpha() and t.isascii()
    out, last = [], 0
    for i, (a, b, t) in enumerate(toks):
        if t not in names:
            continue
        prev = toks[i - 1][2] if i else ""
        nxt = toks[i + 1][2] if i + 1 < len(toks) else ""
        glued_digit = i and toks[i - 1][1] == a and prev.isdigit()
        if nxt in ("'", "’"):
            continue
        listy = (prev == "," and i > 1 and single(toks[i - 2][2])) or                 (nxt == "," and i + 2 < len(toks) and single(toks[i + 2][2]))
        after = lang[:2] == "en" and t in ("a", "A") and nxt in _NOT_AFTER_ARTICLE and not (
            nxt == "to" and i + 2 < len(toks) and toks[i + 2][2] == "-")
        # "by a register", "plus a constant": a word follows, so this is the article
        article = (lang[:2] == "en" and t in ("a", "A") and re.fullmatch(r"[A-Za-z]{2,}", nxt or "") is not None
                   and nxt not in _OPS and nxt not in _NOT_AFTER_ARTICLE and not nouns.search(prev))
        if article:
            continue
        if nouns.search(prev) or prev in _OPS or nxt in _OPS or glued_digit or listy or after:
            out += [s[last:a], names[t]]
            last = b
    return "".join(out) + s[last:]


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
    if lang[:2] == "en":
        for g, name in GREEK.items():
            s = s.replace(g, f" {name} ")
    # hex constants, digit by digit; long 0/1 strings (bit patterns) likewise
    s = sub(r"\b0x([0-9A-Fa-f]+)\b", lambda m: w["hex"] + " ".join(m[1].upper()), s)
    s = sub(r"\b(0[01]{3,}|[01]{5,})\b", lambda m: " ".join(m[1]), s)
    # A[i] -> "A of i";  2^k;  (n - 1)!;  *p
    s = sub(r"\b([A-Za-z]\w*)\[(\w+)\]",
            lambda m: w["of"].format(a=A_NAME if m[1] in ("a", "A") and lang[:2] == "en" else m[1], i=m[2]), s)
    s = sub(r"(\w+)\^(\w+)", lambda m: w["pow"].format(a=m[1], b=m[2]), s)
    s = sub(r"\)!", ")" + w["fact"], s)
    s = sub(r"(?<![\w)])\*(?=\w)|(?<=\s)\*(?=\s)|(?<=\w)\*", w["star"], s)
    # identifiers: learning_rate, sumSquare
    s = sub(r"\b(\w+)_(\w+)\b", r"\1 \2", s)
    s = sub(r"\b([a-z]+)([A-Z][a-z]+)\b", r"\1 \2", s)
    # course vocabulary
    if _SAY_RE is not None:
        s = _SAY_RE.sub(lambda m: _say_as(m[0], lang), s)
    # "a · v", "2 · x": a spaced dot between single letters/numbers is a product
    s = sub(r"(?<![\w.])([A-Za-z]|\d+) · (?=(?:[A-Za-z]|\d+)(?![\w.]))", r"\1 × ", s)
    s = math_letters(s, lang)
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
    voice = {"pico": "pico", "kokoro": f"kokoro:{_kokoro_voice(lang)[0]}"}.get(ENGINE) or voice_for(lang)
    return hashlib.sha1(f"{voice}|{RATE}|{text}".encode()).hexdigest()[:16]


def _kokoro_voice(lang: str):
    v, code = KOKORO_VOICES.get(lang, KOKORO_VOICES["en"])
    return (os.environ.get(f"KIT_VOICE_{lang.upper()}") or _SERIES_TTS.get("kokoro_voice", {}).get(lang)
            or v), code


_KOKORO = None


def _kokoro(text: str, lang: str, out: Path):
    global _KOKORO
    import numpy as np
    from kokoro_onnx import Kokoro
    if _KOKORO is None:
        _KOKORO = Kokoro(str(KOKORO_DIR / "kokoro-v1.0.onnx"), str(KOKORO_DIR / "voices-v1.0.bin"))
    voice, code = _kokoro_voice(lang)
    m = re.match(r"([+-]\d+)%", RATE)
    samples, sr = _KOKORO.create(text, voice=voice, lang=code, speed=1 + int(m[1]) / 100 if m else 1.0)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((np.clip(samples, -1, 1) * 32767).astype("<i2").tobytes())


def _duration(path: Path) -> float:
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


async def _edge(text: str, voice: str, out: Path):
    import edge_tts
    import edge_tts.communicate as _comm
    # edge-tts pins certifi's CA list; behind a TLS-inspecting proxy, also trust
    # the CA named by SSL_CERT_FILE (a no-op everywhere else)
    ca = os.environ.get("SSL_CERT_FILE")
    if ca and os.path.exists(ca) and not getattr(_comm, "_kit_ca", False):
        _comm._SSL_CTX.load_verify_locations(ca)
        _comm._kit_ca = True
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
    if ENGINE == "kokoro":
        mp3 = mp3.with_suffix(".kokoro.wav")
        _kokoro(text, lang, mp3)
    elif ENGINE == "pico":
        import subprocess
        mp3 = mp3.with_suffix(".pico.wav")
        subprocess.run(["pico2wave", "-l", PICO_LANG.get(lang, "en-US"), "-w", str(mp3), text], check=True)
    for attempt in range(5 if ENGINE == "edge" else 0):
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
