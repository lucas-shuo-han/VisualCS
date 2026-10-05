"""Pace of finished videos, measured from their subtitles.

    python pace.py videos/cs182-newton-schulz            every .srt in the folder
    python pace.py preview/09_the_gap.srt

Per file: length, words (CJK: characters) and words per minute including pauses.
Compare with what the user asked for before sending a render: an explainer in the
3Blue1Brown manner runs at about 130 to 150 words per minute including pauses; a video
that "feels too fast" usually has the speed of ordinary speech and no pauses (the first
Newton-Schulz cut measured 179).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

TIME = re.compile(r"(\d+):(\d+):(\d+)[,.](\d+) --> (\d+):(\d+):(\d+)[,.](\d+)")


def cues(path: Path):
    out = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
        lines = block.strip().splitlines()
        m = next((TIME.search(x) for x in lines if TIME.search(x)), None)
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        out.append((a, b, " ".join(x for x in lines if not TIME.search(x) and not x.strip().isdigit())))
    return out


def words(text: str) -> int:
    cjk = sum(1 for c in text if ord(c) > 0x2E7F)
    return cjk + len(re.findall(r"[A-Za-z0-9']+", text))


def report(path: Path):
    cs = cues(path)
    if not cs:
        return
    total = cs[-1][1]
    n = sum(words(t) for _, _, t in cs)
    m, sec = divmod(int(total), 60)
    print(f"{path.name[:58]:58s} {m:3d}:{sec:02d}  {n:5d} words  {n / total * 60:4.0f} wpm")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for arg in sys.argv[1:]:
        p = Path(arg)
        for f in (sorted(p.rglob("*.srt")) if p.is_dir() else [p]):
            report(f)


if __name__ == "__main__":
    main()
