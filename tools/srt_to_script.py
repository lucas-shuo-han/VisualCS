"""Collect the narration of every rendered episode (.srt) into one Markdown
script per language, handy for proofreading or recording a voice-over:
videos/cs61c-riscv/zh/*.srt -> cs61c/riscv/SCRIPT.md,
videos/cs61c-riscv/en/*.srt -> cs61c/riscv/SCRIPT.en.md."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIDEOS = ROOT / "videos" / "cs61c-riscv"
DOCS = ROOT / "cs61c" / "riscv"

HEADERS = {
    "zh": ("SCRIPT.md", "# CS61C RISC-V 系列 · 旁白脚本\n",
           "由各集字幕（.srt）自动生成：`python tools/srt_to_script.py`。\n"),
    "en": ("SCRIPT.en.md", "# CS61C RISC-V series · narration script\n",
           "Generated from the episodes' subtitles (.srt): `python tools/srt_to_script.py`.\n"),
}


def ts(s):
    h, m, rest = s.split(":")
    sec = rest.split(",")[0]
    return f"{int(h) * 60 + int(m):02d}:{int(sec):02d}"


def build(lang):
    name, title, note = HEADERS[lang]
    srts = sorted((VIDEOS / lang).glob("*.srt"))
    if not srts:
        return
    parts = [title, note]
    for srt in srts:
        parts.append(f"\n## {srt.stem}\n")
        blocks = re.split(r"\n\s*\n", srt.read_text(encoding="utf-8").strip())
        for b in blocks:
            lines = b.strip().splitlines()
            if len(lines) < 3:
                continue
            start = lines[1].split(" --> ")[0]
            text = " ".join(lines[2:])
            parts.append(f"- `{ts(start)}` {text}")
    out = DOCS / name
    out.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"wrote {out}")


def main():
    for lang in HEADERS:
        build(lang)


if __name__ == "__main__":
    main()
