"""Tile frames from a rendered episode into contact sheets for visual review.

One frame per caption (from the .srt), sampled either just before the caption
ends (`end`: the settled state after that caption's animations) or at its
middle (`mid`: catches overlaps that only exist mid-animation). Each frame is
numbered with its caption index so a problem maps straight back to the code.

Usage:
    python contact_sheet.py VIDEO.mp4 VIDEO.srt OUT_DIR [--at end|mid] [--per-sheet 9]
Then look at OUT_DIR/sheet00.png, sheet01.png, ...
"""

import argparse
import re
import subprocess
from pathlib import Path


def ts(s):
    h, m, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("srt")
    ap.add_argument("out")
    ap.add_argument("--at", choices=["end", "mid"], default="end")
    ap.add_argument("--per-sheet", type=int, default=9)
    ap.add_argument("--cols", type=int, default=3)
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.png"):
        f.unlink()
    entries = re.findall(r"(\d\d:\d\d:\d\d,\d+) --> (\d\d:\d\d:\d\d,\d+)",
                         Path(a.srt).read_text(encoding="utf-8"))
    if a.at == "mid":
        times = [(ts(s) + ts(e)) / 2 for s, e in entries]
    else:
        times = [max(0, ts(e) - 0.15) for s, e in entries]

    frames = []
    for i, t in enumerate(times):
        f = out / f"f{i:03d}.png"
        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", a.video, "-frames:v", "1", "-vf"]
        rc = subprocess.run(cmd + [f"scale=854:-2,drawtext=text='{i}':x=10:y=10:fontsize=28:fontcolor=red", str(f)]).returncode
        if rc != 0:  # e.g. Windows ffmpeg without fontconfig: extract, then number the frame with Pillow
            subprocess.run(cmd + ["scale=854:-2", str(f)], check=True)
            from PIL import Image, ImageDraw, ImageFont
            im = Image.open(f).convert("RGB")
            dr = ImageDraw.Draw(im)
            try:
                font = ImageFont.truetype("arial.ttf", 28)
            except OSError:
                font = ImageFont.load_default()
            dr.text((10, 8), str(i), fill=(255, 60, 60), font=font)
            im.save(f)
        frames.append(f)

    for s in range(0, len(frames), a.per_sheet):
        chunk = frames[s:s + a.per_sheet]
        n = len(chunk)
        sheet = out / f"sheet{s // a.per_sheet:02d}.png"
        args = ["ffmpeg", "-loglevel", "error", "-y"]
        for f in chunk:
            args += ["-i", str(f)]
        if n == 1:
            args += ["-filter_complex", "[0:v]copy", str(sheet)]
        else:
            layout = []
            for k in range(n):
                cx, cy = k % a.cols, k // a.cols
                xs = "+".join(["w0"] * cx) if cx else "0"
                ys = "+".join(["h0"] * cy) if cy else "0"
                layout.append(f"{xs}_{ys}")
            inputs = "".join(f"[{k}:v]" for k in range(n))
            args += ["-filter_complex",
                     f"{inputs}xstack=inputs={n}:layout={'|'.join(layout)}:fill=gray", str(sheet)]
        subprocess.run(args, check=True)
    print(f"{len(frames)} frames -> {out}/sheet*.png")


if __name__ == "__main__":
    main()
