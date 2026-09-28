"""Collect the narration of every rendered episode (.srt) into one Markdown
script — for proofreading, study notes, or recording a voice-over.

Usage:
    python srt_to_script.py VIDEOS_DIR OUT.md [--title "Series name"]
"""

import argparse
import re
from pathlib import Path


def ts(s):
    h, m, rest = s.split(":")
    sec = rest.split(",")[0]
    return f"{int(h) * 60 + int(m):02d}:{int(sec):02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos")
    ap.add_argument("out")
    ap.add_argument("--title", default="Narration script")
    a = ap.parse_args()

    parts = [f"# {a.title}\n", "Generated from the episode subtitles (.srt).\n"]
    for srt in sorted(Path(a.videos).glob("*.srt")):
        parts.append(f"\n## {srt.stem}\n")
        for block in re.split(r"\n\s*\n", srt.read_text(encoding="utf-8").strip()):
            lines = block.strip().splitlines()
            if len(lines) < 3:
                continue
            start = lines[1].split(" --> ")[0]
            parts.append(f"- `{ts(start)}` {' '.join(lines[2:])}")
    Path(a.out).write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
