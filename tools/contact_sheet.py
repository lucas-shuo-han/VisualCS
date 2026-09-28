"""Grab one frame near the end of every caption in an .srt and tile them into
contact sheets, for quick visual review of a rendered episode.

Usage:
    python tools/contact_sheet.py VIDEO.mp4 VIDEO.srt OUT_DIR [end|mid]

ffmpeg is taken from $FFMPEG, then PATH, then a winget install."""
import glob
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def ffmpeg_bin():
    found = os.environ.get("FFMPEG") or shutil.which("ffmpeg")
    if found:
        return found
    pat = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\*FFmpeg*\*\bin\ffmpeg.exe")
    hits = glob.glob(pat)
    if hits:
        return hits[0]
    sys.exit("ffmpeg not found: install it or set $FFMPEG")


FFMPEG = ffmpeg_bin()
# drawtext needs an explicit font on Windows (no fontconfig config there)
FONT = "fontfile='C\\:/Windows/Fonts/arial.ttf':" if sys.platform == "win32" else ""


def ts(s):
    h, m, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def main(video, srt, out_dir, at="end", per_sheet=9, cols=3):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.png"):
        f.unlink()
    entries = re.findall(r"(\d\d:\d\d:\d\d,\d+) --> (\d\d:\d\d:\d\d,\d+)", Path(srt).read_text(encoding="utf-8"))
    if at == "mid":
        times = [(ts(a) + ts(b)) / 2 for a, b in entries]
    else:
        times = [max(0, ts(b) - 0.15) for a, b in entries]
    frames = []
    for i, t in enumerate(times):
        f = out / f"f{i:03d}.png"
        subprocess.run([FFMPEG, "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", video,
                        "-frames:v", "1", "-vf",
                        f"scale=854:-2,drawtext={FONT}text='{i}':x=10:y=10:fontsize=28:fontcolor=red", str(f)],
                       check=True)
        frames.append(f)
    for s in range(0, len(frames), per_sheet):
        chunk = frames[s:s + per_sheet]
        rows = (len(chunk) + cols - 1) // cols
        args = [FFMPEG, "-loglevel", "error", "-y"]
        for f in chunk:
            args += ["-i", str(f)]
        n = len(chunk)
        inputs = "".join(f"[{k}:v]" for k in range(n))
        w, h = "w0", "h0"
        lay = []
        for k in range(n):
            cx, cy = k % cols, k // cols
            xs = "+".join([w] * cx) if cx else "0"
            ys = "+".join([h] * cy) if cy else "0"
            lay.append(f"{xs}_{ys}")
        if n == 1:
            args += ["-filter_complex", "[0:v]copy", str(out / f"sheet{s // per_sheet:02d}.png")]
        else:
            args += ["-filter_complex", f"{inputs}xstack=inputs={n}:layout={'|'.join(lay)}:fill=gray",
                     str(out / f"sheet{s // per_sheet:02d}.png")]
        subprocess.run(args, check=True)
    print(f"{len(frames)} frames -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:5])
