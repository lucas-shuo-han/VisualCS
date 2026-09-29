"""Tile frames from a rendered episode into contact sheets for visual review.

One frame per caption (from the .srt), sampled either just before the caption
ends (`end`: the settled state after that caption's animations) or at its
middle (`mid`: catches overlaps that only exist mid-animation). Each frame is
numbered with its caption index so a problem maps straight back to the code.

Uses PyAV and Pillow (both come with Manim): no ffmpeg binary needed.

Usage:
    python contact_sheet.py VIDEO.mp4 VIDEO.srt OUT_DIR [--at end|mid] [--per-sheet 9]
    python contact_sheet.py VIDEO.mp4 VIDEO.srt OUT_DIR --only 12 13 14   # just these captions
Then look at OUT_DIR/sheet00.png, sheet01.png, ...
"""

import argparse
import re
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont


def ts(s):
    h, m, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def grab(video, times, width=854):
    """One PIL image per time (seconds), decoding forward from a seek."""
    out = []
    with av.open(str(video)) as c:
        st = c.streams.video[0]
        for t in times:
            c.seek(int(max(0.0, t - 1.0) / st.time_base), stream=st, backward=True)
            img = None
            for fr in c.decode(st):
                img = fr
                if fr.time is not None and fr.time >= t:
                    break
            im = img.to_image()
            out.append(im.resize((width, round(im.height * width / im.width))))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("srt")
    ap.add_argument("out")
    ap.add_argument("--at", choices=["end", "mid"], default="end")
    ap.add_argument("--per-sheet", type=int, default=9)
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--only", nargs="*", type=int, help="caption indices to include")
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("sheet*.png"):
        f.unlink()
    entries = re.findall(r"(\d\d:\d\d:\d\d,\d+) --> (\d\d:\d\d:\d\d,\d+)",
                         Path(a.srt).read_text(encoding="utf-8"))
    idx = [i for i in range(len(entries)) if not a.only or i in a.only]
    times = [(ts(entries[i][0]) + ts(entries[i][1])) / 2 if a.at == "mid"
             else max(0.0, ts(entries[i][1]) - 0.15) for i in idx]
    frames = grab(a.video, times)
    try:
        font = ImageFont.load_default(size=28)
    except TypeError:   # Pillow < 10.1
        font = ImageFont.load_default()
    for im, i in zip(frames, idx):
        ImageDraw.Draw(im).text((10, 6), str(i), fill=(255, 40, 40), font=font)

    w, h = frames[0].size if frames else (854, 480)
    for s in range(0, len(frames), a.per_sheet):
        chunk = frames[s:s + a.per_sheet]
        cols = min(a.cols, len(chunk))
        rows = (len(chunk) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * w, rows * h), (128, 128, 128))
        for k, im in enumerate(chunk):
            sheet.paste(im, ((k % cols) * w, (k // cols) * h))
        sheet.save(out / f"sheet{s // a.per_sheet:02d}.png")
    print(f"{len(frames)} frames -> {out}/sheet*.png")


if __name__ == "__main__":
    main()
