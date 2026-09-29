"""Print an episode's narration -- every say() caption and end-card bullet, in
the order the scene runs them -- with its translations and, optionally, what
the voice-over will say. For proofreading without rendering anything.

Usage:
    python captions.py SRC 5                 # episode 5, all languages side by side
    python captions.py SRC                   # every episode
    python captions.py SRC 5 --spoken        # + the TTS spoken form of each line
    python captions.py SRC 5 --spoken --synth   # + synthesize (fills the cache, totals speech time)
    python captions.py SRC --out captions.md
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project import Unit, narration  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("episodes", nargs="*", type=int)
    ap.add_argument("--lang", default="all", help="a language code, or 'all'")
    ap.add_argument("--spoken", action="store_true", help="also print the TTS spoken form")
    ap.add_argument("--synth", action="store_true", help="synthesize every line (implies --spoken)")
    ap.add_argument("--out")
    a = ap.parse_args()
    unit = Unit(a.src)
    langs = unit.langs if a.lang == "all" else [a.lang]
    tts = None
    if a.spoken or a.synth:
        sys.path.insert(0, str(unit.src))
        import tts  # the unit's copy, with its say_as.py

    lines, speech = [], {lang: 0.0 for lang in langs}
    for ep in unit.select(a.episodes):
        path = unit.path(ep)
        title = ep.get("title", {}).get(unit.source_lang, ep["scene"]) if unit.has_series else ep["scene"]
        lines.append(f"## {ep['num']:02d} {title}\n")
        if not path.exists():
            lines.append("(not written yet)\n")
            continue
        tables = {lang: unit.table(ep["num"], lang) for lang in langs}
        k = 0
        for kind, text, speak in narration(path, ep["scene"]):
            if kind == "say":
                k += 1
            tag = "end" if kind == "end" else str(k)
            for i, lang in enumerate(langs):
                shown = text if lang == unit.source_lang else tables[lang].get(text)
                prefix = f"{tag}." if i == 0 else " " * (len(tag) + 1)
                lines.append(f"{prefix} [{lang}] {shown if shown is not None else '<<MISSING>>'}")
                if tts and shown is not None and not shown.startswith(("f'", 'f"')):
                    say = speak if lang == unit.source_lang else tables[lang].get(speak) if speak else None
                    lines.append(f"{' ' * (len(tag) + 1)}   ~ {say or tts.spoken(shown, lang)}")
                    if a.synth:
                        speech[lang] += tts.synth(shown, lang, speak=say)[1]
        lines.append("")
    if a.synth:
        lines.append("speech: " + ", ".join(f"{lang} {s / 60:.1f} min" for lang, s in speech.items()))
    text = "\n".join(lines)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"wrote {a.out}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text)


if __name__ == "__main__":
    main()
