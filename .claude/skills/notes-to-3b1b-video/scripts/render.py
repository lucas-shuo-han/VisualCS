"""Render every episode scene in a folder and collect the videos + subtitles.

Episode scenes are discovered by name: any `class EpNN...(...)` in a *.py file
of SRC (manim_kit.py itself is skipped). The output video is named after the
file, e.g. ep01_twos_complement.py -> OUT/ep01_twos_complement.mp4 (+ .srt).

Usage:
    python render.py SRC                      # all episodes, 1080p30
    python render.py SRC --only 2 5           # episodes 2 and 5
    python render.py SRC --preview            # 480p15 quick check (no copy to OUT)
    python render.py SRC --manim .venv/bin/manim --jobs 3 --out videos

Each episode renders in its own media directory, so parallel jobs never race
on Manim's shared text/SVG cache.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SCENE_RE = re.compile(r"^class (Ep(\d+)\w*)\(", re.M)


def discover(src: Path):
    eps = []
    for f in sorted(src.glob("*.py")):
        if f.name == "manim_kit.py":
            continue
        for m in SCENE_RE.finditer(f.read_text(encoding="utf-8")):
            eps.append((int(m.group(2)), f, m.group(1)))
    return sorted(eps)


def render(job, preview, media_root: Path, out: Path, manim: str):
    num, file, scene = job
    media = media_root / f"ep{num:02d}"
    media.mkdir(parents=True, exist_ok=True)
    quality = ["-ql"] if preview else ["-r", "1920,1080", "--fps", "30"]
    log = media_root / f"ep{num:02d}.log"
    with open(log, "w") as fh:
        # MANIM_CWD: run from another directory (Windows: MiKTeX's dvisvgm fails when the
        # cwd is on some drives, e.g. a D: folder; point this at a C: folder).
        cwd = os.environ.get("MANIM_CWD")
        env = dict(os.environ, PYTHONPATH=os.pathsep.join(filter(None, [str(file.parent), os.environ.get("PYTHONPATH")])))
        rc = subprocess.run([manim, *quality, "--media_dir", str(media), str(file) if cwd else file.name, scene],
                            cwd=cwd or file.parent, env=env, stdout=fh, stderr=subprocess.STDOUT).returncode
    if rc != 0:
        tail = log.read_text(errors="replace").strip().splitlines()[-3:]
        return num, f"FAILED ({log}): " + " | ".join(tail)
    mp4 = next((media / "videos").rglob(f"{scene}.mp4"))
    srt = mp4.with_suffix(".srt")
    if preview:
        return num, f"{mp4}  (subtitles: {srt if srt.exists() else 'none'})"
    out.mkdir(parents=True, exist_ok=True)
    shutil.copy(mp4, out / f"{file.stem}.mp4")
    if srt.exists():
        shutil.copy(srt, out / f"{file.stem}.srt")
    return num, str(out / f"{file.stem}.mp4")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", help="folder with manim_kit.py and the episode files")
    ap.add_argument("--only", nargs="*", type=int, default=None, help="episode numbers")
    ap.add_argument("--preview", action="store_true", help="480p15, leave output in media dir")
    ap.add_argument("--out", default="videos", help="where finished mp4/srt are collected")
    ap.add_argument("--media", default="media", help="scratch media root")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--manim", default=shutil.which("manim") or "manim")
    a = ap.parse_args()

    jobs = discover(Path(a.src).resolve())
    if a.only:
        jobs = [j for j in jobs if j[0] in a.only]
    if not jobs:
        sys.exit(f"no `class EpNN...` scenes found in {a.src}")
    media, out = Path(a.media).resolve(), Path(a.out).resolve()
    with ThreadPoolExecutor(a.jobs) as ex:
        for num, result in ex.map(lambda j: render(j, a.preview, media, out, a.manim), jobs):
            print(f"episode {num}: {result}", flush=True)


if __name__ == "__main__":
    main()
