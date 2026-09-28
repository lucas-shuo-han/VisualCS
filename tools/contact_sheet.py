"""Grab one frame near the end of every caption in an .srt and tile them into
contact sheets, for quick visual review of a rendered episode."""
import re
import subprocess
import sys
from pathlib import Path


def ts(s):
    h, m, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def main(video, srt, out_dir, per_sheet=9, cols=3):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.png"):
        f.unlink()
    entries = re.findall(r"(\d\d:\d\d:\d\d,\d+) --> (\d\d:\d\d:\d\d,\d+)", Path(srt).read_text())
    times = [max(0, ts(b) - 0.15) for a, b in entries]
    frames = []
    for i, t in enumerate(times):
        f = out / f"f{i:03d}.png"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", video,
                        "-frames:v", "1", "-vf", f"drawtext=text='{i}':x=10:y=10:fontsize=28:fontcolor=red", str(f)],
                       check=True)
        frames.append(f)
    for s in range(0, len(frames), per_sheet):
        chunk = frames[s:s + per_sheet]
        rows = (len(chunk) + cols - 1) // cols
        args = ["ffmpeg", "-loglevel", "error", "-y"]
        for f in chunk:
            args += ["-i", str(f)]
        n = len(chunk)
        inputs = "".join(f"[{k}:v]" for k in range(n))
        layout = "|".join(f"{(k % cols)}*w0_{(k // cols)}*h0".replace("*w0_", "_").replace("*h0", "") for k in range(n))
        # build explicit xstack layout
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
    main(*sys.argv[1:4])
