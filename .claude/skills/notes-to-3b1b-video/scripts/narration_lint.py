"""Lint the narration of a unit before rendering: where the voice will stumble,
and where the script sounds like a list of fragments read aloud.

Per episode and language, over every say() caption and end-card bullet:
  choppy  runs of 3+ consecutive short captions (en < 9 words, zh < 14 chars),
          and episodes where more than 15% of sentences are tiny
          (en < 5 words, zh < 7 chars): "Done!", "Step two.", "Why?"
  split   a sentence continued in the next caption ("...then" / "...and"):
          each caption is voiced as its own clip, so the sentence breaks in two
  voice   tokens in the *spoken* form a neural voice is likely to misread:
          spelled letters that fuse with a word (xor -> "X or", andi -> "and I"),
          ALL-CAPS words not in say_as.py (read as a word, or not),
          letter+digit codes, leftover symbols, and in Chinese a lone
          lowercase a / e / o (read as 啊 / 呃 / 哦).
          Single letters used as variables ("scalar a") are handled by
          tts.math_letters; check the rest with `captions.py --spoken`.

Usage:
    python narration_lint.py SRC [N ...] [--lang en] [--audition DIR]

--audition synthesizes each flagged term once, in a carrier sentence, and writes
DIR/audition.md listing the clips: listen, then fix say_as.py. The linter only
finds candidates; an ear decides.
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project import Unit, narration  # noqa: E402

SHORT = {"en": 9, "zh": 14}
TINY = {"en": 5, "zh": 7}
ALLOWED_SYM = set(".,;:!?'’()%-，。；：！？、（）")
SENT_END = re.compile(r"(?<=[.!?。！？])\s*")


def size(s: str, lang: str) -> int:
    """Words for Latin scripts, characters (no spaces) for Chinese."""
    return len(re.sub(r"\s", "", s)) if lang.startswith("zh") else len(s.split())


def voice_risks(spoken: str, lang: str, say_as: dict) -> list[str]:
    out = []
    if lang.startswith("zh"):
        out += [f"letter '{m[1]}'"
                for m in re.finditer(r"(?<![A-Za-z])([aeo])(?![A-Za-z])", spoken)]
    for m in re.finditer(r"\b[A-Z] (?:or|and)\b(?= [A-Z0-9]|[,.:;]|$)|\b(?:and|or) I\b", spoken):
        out.append(f"phrase '{m[0]}'")
    for m in re.finditer(r"\b[A-Z]{2,}s?\b", spoken, re.A):
        if m[0] not in say_as and m[0].rstrip("s") not in say_as:
            out.append(f"caps '{m[0]}'")
    for m in re.finditer(r"\b(?=\w*\d)(?=\w*[A-Za-z])\w+\b", spoken, re.A):
        out.append(f"code '{m[0]}'")
    for ch in spoken:
        if not (ch.isalnum() or ch.isspace() or ch in ALLOWED_SYM):
            out.append(f"symbol '{ch}'")
    return out


def lint_episode(lines, lang, say_as, risks: Counter) -> list[str]:
    report = []
    short = SHORT.get(lang[:2], 9)
    run = []
    for i, (kind, shown, _) in enumerate(lines + [("end", "", "")]):
        if kind == "say" and size(shown, lang) < short:
            run.append(i)
            continue
        if len(run) >= 3:
            report.append(f"  choppy  #{run[0] + 1}-{run[-1] + 1}: "
                          + " | ".join(lines[j][1] for j in run))
        run = []
    sents = [x for kind, shown, _ in lines if kind == "say"
             for x in SENT_END.split(shown) if re.search(r"\w", x)]
    tiny = [x for x in sents if size(x, lang) < TINY.get(lang[:2], 5)]
    if sents and len(tiny) / len(sents) > 0.15:
        mean = sum(size(x, lang) for x in sents) / len(sents)
        report.append(f"  choppy  {len(tiny)}/{len(sents)} sentences are tiny "
                      f"(mean {mean:.1f}): " + " | ".join(tiny[:12]))
    # a sentence split over two captions is synthesized as two clips: each half
    # gets its own falling intonation and a gap, which sounds broken
    for i, (kind, shown, _) in enumerate(lines):
        if kind == "say" and re.search(r"(……|\.\.\.|…)\s*$", shown):
            report.append(f"  split   #{i + 1}-{i + 2}: {shown}  //  "
                          f"{lines[i + 1][1] if i + 1 < len(lines) else ''}")
    for i, (kind, shown, sp) in enumerate(lines):
        r = voice_risks(sp, lang, say_as)
        risks.update(r)
        if r:
            report.append(f"  voice   #{i + 1}: {', '.join(dict.fromkeys(r))}\n          ~ {sp}")
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("episodes", nargs="*", type=int)
    ap.add_argument("--lang", default="all")
    ap.add_argument("--audition", help="synthesize each flagged term into this folder")
    a = ap.parse_args()
    unit = Unit(a.src)
    langs = unit.langs if a.lang == "all" else [a.lang]
    sys.path.insert(0, str(unit.src))
    import tts  # the unit's copy, with its say_as.py
    say_as = getattr(tts, "SAY_AS", None) or getattr(tts, "_SAY_AS", {})
    sys.stdout.reconfigure(encoding="utf-8")

    risks = {lang: Counter() for lang in langs}
    for ep in unit.select(a.episodes):
        path = unit.path(ep)
        if not path.exists():
            continue
        for lang in langs:
            table = unit.table(ep["num"], lang)
            lines = []
            for kind, text, speak in narration(path, ep["scene"]):
                shown = text if lang == unit.source_lang else table.get(text)
                if not shown or shown.startswith(("f'", 'f"')):
                    continue
                say = (speak if lang == unit.source_lang else table.get(speak)) if speak else None
                lines.append((kind, shown, say or tts.spoken(shown, lang)))
            report = lint_episode(lines, lang, say_as, risks[lang])
            if report:
                print(f"## {ep['num']:02d} [{lang}]")
                print("\n".join(report) + "\n")

    for lang, c in risks.items():
        if c:
            print(f"[{lang}] most frequent voice risks: "
                  + ", ".join(f"{k} x{n}" for k, n in c.most_common(25)))
    if a.audition:
        out = Path(a.audition)
        out.mkdir(parents=True, exist_ok=True)
        md = ["# Pronunciation audition", "",
              "Listen to each clip; fix what sounds wrong in say_as.py (SAY_AS / SPELL / REWRITES).", ""]
        for lang, c in risks.items():
            carrier = "这里是 {}。" if lang.startswith("zh") else "Here is {}."
            for key in c:
                term = key.split("'")[1]
                clip, _ = tts.synth(carrier.format(term), lang)
                md.append(f"- [{lang}] `{term}` -> {clip}")
        (out / "audition.md").write_text("\n".join(md), encoding="utf-8")
        print(f"wrote {out / 'audition.md'}")


if __name__ == "__main__":
    main()
