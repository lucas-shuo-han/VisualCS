"""Voice-over for the captions: text-to-speech with Microsoft's neural voices
(the `edge-tts` package), cached as .wav files under media/tts/<lang>/.

Captions are written to be read, so before synthesis `spoken()` rewrites the
bits a voice would stumble over: hex constants are spelled digit by digit,
registers and mnemonics letter by letter (`beq` -> "B E Q"), `8(sp)` becomes
"S P plus 8", operators become words, and so on.

    python cs61c/riscv/tts.py 5                # spoken form of episode 5's captions
    python cs61c/riscv/tts.py 5 --lang en --synth   # also synthesize (fills the cache)
    python cs61c/riscv/tts.py --say "lw t0, 8(sp)" --lang en
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

ROOT = Path(__file__).resolve().parents[2]
CACHE = Path(os.environ.get("VCS_TTS_CACHE", ROOT / "media" / "tts"))

VOICES = {
    "zh": ("zh-CN-YunxiNeural", "+0%"),
    "en": ("en-US-AndrewNeural", "+0%"),
}

# ---------------------------------------------------------------- spoken form


def _spell(s: str) -> str:
    return " ".join(s.upper())


# instruction names and assembler jargon that a voice would otherwise mangle
_SAY_AS = {
    "addi": "add I", "subi": "sub I", "andi": "and I", "ori": "or I",
    "xori": "X or I", "xor": "X or", "mv": "move", "ret": "return", "nop": "no-op",
    "ecall": "E call", "ebreak": "E break", "printf": "print F",
    "funct3": "funct 3", "funct7": "funct 7", "opcode": "op code",
    "RISC-V": "risk five", "RISC": "risk", "CS61C": "CS 61 C", "61C": "61 C",
    "RV32I": "R V 32 I", "RV32": "R V 32", "x0": "X 0",
    # spelled out, "jal ra" would sound like "jalr a"
    "jal": "jump and link", "jalr": "jump and link register",
}
_SPELLED = """lw sw lb lbu lh lhu lwu sb sh sbu beq bne blt bge bltu bgeu bgt ble
    sll srl sra slli srli srai slt slti sltu sltiu jr lui auipc li la
    ISA ABI PC pc sp ra fp gp tp rd rs rs1 rs2 lt""".split()
for _m in _SPELLED:
    _SAY_AS.setdefault(_m, _spell(_m) if not _m[-1].isdigit() else _spell(_m[:-1]) + " " + _m[-1])

_WORDS = {
    "zh": {"==": " 等于 ", "!=": " 不等于 ", ">=": " 大于等于 ", "<=": " 小于等于 ",
           "≥": " 大于等于 ", "≤": " 小于等于 ", "<<": " 左移 ", ">>": " 右移 ",
           "<": " 小于 ", ">": " 大于 ", "=": " 等于 ", "+": " 加 ", "×": " 乘 ",
           "±": "正负 ", "→": " 到 ", "–": " 到 ", "minus": " 减 ", "neg": "负 ",
           "star": " 星号 ", "fact": " 的阶乘", "hex": "零x ", "KiB": " KB", "MiB": " MB",
           "of": "{a} 的第 {i} 项", "imm": "立即数第 {bits} 位", "inst": "指令第 {bits} 位", "to": "到", "bar": "、",
           "off": "{r} 加 {n}", "offneg": "{r} 减 {n}", "pow": "{a} 的 {b} 次方",
           "bs0": " 反斜杠零", "#": " 井号 ", "/": "，", " / ": "、", "&": " 和 ", "|": "，"},
    "en": {"==": " equals ", "!=": " is not equal to ", ">=": " is greater than or equal to ",
           "<=": " is less than or equal to ", "≥": " is at least ", "≤": " is at most ",
           "<<": " shifted left by ", ">>": " shifted right by ", "<": " is less than ",
           ">": " is greater than ", "=": " equals ", "+": " plus ", "×": " times ",
           "±": "plus or minus ", "→": " to ", "–": " through ", "minus": " minus ",
           "neg": "negative ", "star": " star ", "fact": " factorial", "hex": "hex ",
           "KiB": " kibibytes", "MiB": " mebibytes",
           "of": "{a} of {i}", "imm": "immediate bits {bits}", "inst": "instruction bits {bits}", "to": " to ", "bar": ", ",
           "off": "{r} plus {n}", "offneg": "{r} minus {n}", "pow": "{a} to the {b}",
           "bs0": " backslash zero", "#": " hash ", "/": " or ", " / ": " and ", "&": " and ", "|": ", "},
}


def spoken(text: str, lang: str) -> str:
    """What the voice should say for caption `text`."""
    w = _WORDS[lang]

    def sub(pat, rep, s):   # ASCII-only \w and \b: CJK must not count as a word character
        return re.sub(pat, rep, s, flags=re.A)

    s = text.replace("\n", " ")
    # pauses and decorations
    s = sub(r"^[…\s]+", "", s)
    s = sub(r"[…]+|——|—", "，" if lang == "zh" else ", ", s)
    s = s.replace("“", "").replace("”", "").replace('"', "")
    s = s.replace("\\0", w["bs0"])
    # imm[20|10:1|11|19:12], imm[11:0], inst[30:25]
    s = sub(r"\b(imm|inst)\[([0-9:|]+)\]",
            lambda m: w[m[1]].format(bits=m[2].replace(":", w["to"]).replace("|", w["bar"])), s)
    # 8(sp), -4(sp), 0(x5)
    def _off(m):
        n, r = m[1].replace("−", "-"), _SAY_AS.get(m[2], m[2])
        r = sub(r"^([xatsXATS])(\d{1,2})$", lambda k: f"{k[1].upper()} {k[2]}", r)
        return (w["offneg"] if n.startswith("-") else w["off"]).format(r=r, n=n.lstrip("-"))
    s = sub(r"([−-]?\d+)\((\w+)\)", _off, s)
    # hex constants, digit by digit; long 0/1 strings (bit fields) likewise
    s = sub(r"\b0x([0-9A-Fa-f]+)\b", lambda m: w["hex"] + " ".join(m[1].upper()), s)
    s = sub(r"\b(0[01]{3,}|[01]{5,})\b", lambda m: " ".join(m[1]), s)
    # A[i] -> "A of i"
    s = sub(r"\b([A-Za-z]\w*)\[(\w+)\]", lambda m: w["of"].format(a=m[1], i=m[2]), s)
    # 2^k, (n − 1)!, *y, I*
    s = sub(r"(\w+)\^(\w+)", lambda m: w["pow"].format(a=m[1], b=m[2]), s)
    s = sub(r"\)!", ")" + w["fact"], s)
    s = sub(r"(?<![\w)])\*(?=\w)|(?<=\s)\*(?=\s)", w["star"], s)
    s = sub(r"(?<=\w)\*", w["star"], s)
    # identifiers: func_b, sumSquare
    s = sub(r"\b(\w+)_(\w+)\b", r"\1 \2", s)
    s = sub(r"\b([a-z]+)([A-Z][a-z]+)\b", r"\1 \2", s)
    # mnemonics, register names, jargon
    s = sub(r"RISC-V|\b[\w]+\b", lambda m: _SAY_AS.get(m[0], m[0]), s)
    s = sub(r"\b([xatsXATS])(\d{1,2})\b", lambda m: f"{m[1].upper()} {m[2]}", s)
    if lang == "en":
        s = sub(r"\b([01])s\b", lambda m: ("zeros", "ones")[int(m[1])], s)
    s = sub(r"\b(\d)([a-rt-z])\b", r"\1 \2", s)          # 4i
    # a chain of arrows is a sequence of steps, a single one is "to"
    if s.count("→") >= 2:
        s = sub(r"\s*→\s*", "，" if lang == "zh" else ", then ", s)
    s = sub(r"\b(KiB|MiB)\b", lambda m: w[m[1]], s)
    # operators (longest first); a minus sign is binary between spaces, else unary
    s = sub(r"\s[−-]\s", w["minus"], s)
    s = sub(r"[−](?=\d)", w["neg"], s)
    s = sub(r"(?<=\s)-(?=\d)", w["neg"], s)
    for op in ("==", "!=", ">=", "<=", "<<", ">>", "≥", "≤", "<", ">", "=", "+", "×", "±", "→", "–", "#"):
        s = s.replace(op, w[op])
    s = sub(r"(?<=\w)/(?=\w)", w["/"], s)
    s = s.replace(" / ", w[" / "]).replace("&", w["&"]).replace("|", w["|"])
    s = sub(r"\s+", " ", s).strip(" ,，")
    return s


# ---------------------------------------------------------------- synthesis


def _key(text: str, lang: str) -> str:
    voice, rate = VOICES[lang]
    return hashlib.sha1(f"{voice}|{rate}|{text}".encode()).hexdigest()[:16]


def _duration(path: Path) -> float:
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


async def _edge(text: str, voice: str, rate: str, out: Path):
    import edge_tts
    await edge_tts.Communicate(text, voice, rate=rate).save(str(out))


def synth(caption: str, lang: str, speak: str | None = None) -> tuple[Path, float]:
    """(wav path, seconds) of the voice-over for `caption` (or `speak` verbatim)."""
    text = speak if speak is not None else spoken(caption, lang)
    d = CACHE / lang
    wav = d / f"{_key(text, lang)}.wav"
    if wav.exists():
        return wav, _duration(wav)
    d.mkdir(parents=True, exist_ok=True)
    voice, rate = VOICES[lang]
    mp3 = wav.with_suffix(f".{os.getpid()}.mp3")
    for attempt in range(5):
        try:
            asyncio.run(_edge(text, voice, rate, mp3))
            break
        except Exception as e:  # network hiccups, throttling
            if attempt == 4:
                raise RuntimeError(f"TTS failed for {text!r}: {e}") from e
            time.sleep(2 + 3 * attempt)
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
    os.replace(tmp, wav)
    for f in (mp3, raw):
        f.unlink(missing_ok=True)
    return wav, _duration(wav)


# ---------------------------------------------------------------- CLI


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("episodes", nargs="*", type=int)
    ap.add_argument("--lang", default="zh", choices=["zh", "en", "all"])
    ap.add_argument("--synth", action="store_true", help="synthesize (fill the cache)")
    ap.add_argument("--say", help="just this text")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    langs = ["zh", "en"] if a.lang == "all" else [a.lang]
    if a.say:
        for lang in langs:
            print(spoken(a.say, lang))
            if a.synth:
                print(*synth(a.say, lang))
        return
    sys.path.insert(0, str(ROOT / "tools"))
    import captions
    import series
    for n in a.episodes or range(1, len(series.SERIES) + 1):
        ep = series.SERIES[n - 1]
        path = Path(__file__).parent / ep.file
        if not path.exists():
            continue
        table = captions.table(n)
        for lang in langs:
            total, count = 0.0, 0
            print(f"## {n:02d} [{lang}]")
            for kind, zh in captions.narration(path, ep.scene):
                if not isinstance(zh, str):
                    continue
                text = zh if lang == "zh" else table.get(zh)
                if text is None:
                    continue
                print(f"- {spoken(text, lang)}")
                if a.synth:
                    total += synth(text, lang)[1]
                    count += 1
            if a.synth:
                print(f"   {count} clips, {total / 60:.1f} min of speech")


if __name__ == "__main__":
    main()
