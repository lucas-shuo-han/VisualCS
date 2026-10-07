"""Fast previews: render single scenes of one episode, in parallel, with the voice.

    python preview.py the_gap                 one scene  -> <unit>/preview/09_the_gap.mp4 (+ .srt)
    python preview.py 9 10 11                 scenes by number
    python preview.py all                     every scene, in parallel
    python preview.py all --join              ... and glue them into preview/all.mp4 (needs ffmpeg)
    python preview.py the_gap --silent        no voice (fastest; timing is then only estimated)
    python preview.py the_gap --no-captions   subtitles only in the .srt, not on the frame
    python preview.py the_gap --hq            1080p30 instead of 480p15
    python preview.py 3 --unit cs182/optim --ep 2 --lang en

Run it from a copy next to the episode, or from the skill with --unit. The
episode needs a `SCENES = [...]` list and the KIT_ONLY branch in construct()
(references/derivation-episodes.md §3).

Each scene renders in its own process and media folder, so a change to one scene
costs one short render. Previews have the voice-over and the subtitles on the
frame, one sentence at a time; the .srt with the same name sits next to the
.mp4. Voice clips are cached per beat, so only changed beats are synthesised.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent


def find_python(unit: Path) -> str:
    """The interpreter that has manim: a .venv in the unit folder or above it,
    else the one running this script."""
    for d in (unit, *unit.parents):
        for rel in (".venv/Scripts/python.exe", ".venv/bin/python"):
            if (d / rel).exists():
                return str(d / rel)
    return sys.executable


sys.path.insert(0, str(HERE))
try:
    from project import latex_path   # run from the skill
except ImportError:                  # a copy next to the episode, without project.py
    def latex_path() -> str | None:
        if shutil.which("latex"):
            return None
        cand = os.environ.get("KIT_LATEX_BIN") or Path.home() / "AppData/Local/Programs/MiKTeX/miktex/bin/x64"
        return str(cand) if Path(cand).exists() else None


def scene_names(ep: Path) -> tuple[str, list[str]]:
    src = ep.read_text(encoding="utf-8")
    cls = re.search(r"^class (Ep\d+\w*)\(", src, re.M)
    scenes = re.search(r"SCENES = \[(.*?)\]", src, re.S)
    if not cls or not scenes:
        sys.exit(f"{ep.name}: needs `class EpNN...` and a `SCENES = [...]` list of scene methods")
    return cls[1], re.findall(r'"(\w+)"', scenes[1])


def render(ep, cls, names, name, a, work, out):
    n = names.index(name) + 1
    stem = f"{n:02d}_{name}"
    media = work / stem
    media.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "KIT_ONLY": name,
           "KIT_TTS": "0" if a.silent else "1",
           "KIT_CAPTIONS": "0" if a.no_captions else "1"}
    if a.lang:
        env["KIT_LANG"] = a.lang
    env.setdefault("KIT_TTS_CACHE", str(work / "tts"))
    if latex_path():
        env["PATH"] = f"{latex_path()}{os.pathsep}{env['PATH']}"
    quality = ["-r", "1920,1080", "--fps", "30"] if a.hq else ["-ql"]
    # no animation cache: on a cache hit Manim's clock does not advance, so the
    # voice-over of later beats lands too early or is lost
    cmd = [find_python(ep.parent), "-m", "manim", *quality, "--disable_caching",
           "--media_dir", str(media), "-o", stem, str(ep), cls]
    t0 = time.time()
    log = work / f"{stem}.log"
    # cwd on the system drive: dvisvgm fails when the project is on another drive (Windows)
    with open(log, "w", encoding="utf-8") as fh:
        rc = subprocess.run(cmd, cwd=work, env=env, stdout=fh, stderr=subprocess.STDOUT).returncode
    text = log.read_text(encoding="utf-8", errors="replace")
    warn = [l.strip() for l in text.splitlines() if l.startswith(("[cue]", "[narration]"))]
    if rc != 0:
        return name, None, f"FAILED, see {log}: " + " | ".join(text.strip().splitlines()[-3:]), warn
    mp4 = max((media / "videos").rglob(f"{stem}.mp4"), key=lambda p: p.stat().st_mtime)
    out.mkdir(exist_ok=True)
    shutil.copy(mp4, out / f"{stem}.mp4")
    if mp4.with_suffix(".srt").exists():
        shutil.copy(mp4.with_suffix(".srt"), out / f"{stem}.srt")
    return name, out / f"{stem}.mp4", f"{time.time() - t0:.0f}s", warn


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("scenes", nargs="+", help="scene names or numbers, or 'all'")
    ap.add_argument("--unit", default=str(HERE), help="unit folder (default: where this script is)")
    ap.add_argument("--ep", type=int, help="episode number when the unit has several")
    ap.add_argument("--lang", help="language to render (default: the source language)")
    ap.add_argument("--silent", action="store_true", help="no voice-over")
    ap.add_argument("--no-captions", action="store_true", help="do not draw captions on the frame")
    ap.add_argument("--hq", action="store_true", help="1080p30")
    ap.add_argument("--join", action="store_true", help="also concatenate the scenes into preview/all.mp4")
    ap.add_argument("--jobs", type=int, default=max(2, (os.cpu_count() or 4) // 2))
    a = ap.parse_args()
    unit = Path(a.unit).resolve()
    eps = sorted(unit.glob(f"ep{a.ep:02d}_*.py" if a.ep else "ep[0-9][0-9]_*.py"))
    if not eps:
        sys.exit(f"no episode file (epNN_*.py) in {unit}")
    ep = eps[0]
    cls, names = scene_names(ep)
    want = names if a.scenes == ["all"] else [names[int(s) - 1] if s.isdigit() else s for s in a.scenes]
    bad = [s for s in want if s not in names]
    if bad:
        sys.exit(f"unknown scene(s) {bad}; scenes are: {', '.join(names)}")
    work = Path(tempfile.gettempdir()) / "kit_preview" / unit.name / ep.stem
    work.mkdir(parents=True, exist_ok=True)
    out = unit / "preview"
    done, failed = [], False
    with ThreadPoolExecutor(a.jobs) as ex:
        for name, mp4, info, warn in ex.map(lambda s: render(ep, cls, names, s, a, work, out), want):
            print(f"{name}: {mp4 or ''} ({info})", flush=True)
            for w in warn:
                print(f"    {w}")
            failed |= mp4 is None
            if mp4:
                done.append(mp4)
    if a.join and done and not failed:
        if not shutil.which("ffmpeg"):
            print("--join needs ffmpeg on PATH; the scene files above are complete on their own")
        else:
            lst = work / "join.txt"
            lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in done), encoding="utf-8")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                            "-c", "copy", str(out / "all.mp4")], check=True)
            print(f"joined: {out / 'all.mp4'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
