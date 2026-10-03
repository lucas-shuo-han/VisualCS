"""Fast previews: render single scenes of the episode, in parallel, with the voice.

    python preview.py the_gap                 one scene  -> preview/09_the_gap.mp4 (+ .srt)
    python preview.py 9 10 11                 scenes by number
    python preview.py all                     every scene, in parallel
    python preview.py all --join              ... and glue them into preview/all.mp4
    python preview.py the_gap --silent        no voice (fastest; timing is then only estimated)
    python preview.py the_gap --no-captions   as in the final video: subtitles only in the .srt
    python preview.py the_gap --hq            1080p30 instead of 480p15

Each scene renders in its own process and media folder, so a change to one scene
costs one short render. Previews have the voice-over and the subtitles drawn on
the frame (one sentence at a time, from the .srt); the .srt with the same name always sits next to the .mp4. Voice clips
are cached per sentence, so only changed lines are synthesised again.
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
ROOT = HERE.parents[1]
EP = sorted(HERE.glob("ep[0-9][0-9]_*.py"))[0]
OUT = HERE / "preview"
# dvisvgm exits with 127 when the working directory is on the D: drive of this
# machine, so Manim runs from a scratch folder on the system drive instead
WORK = Path(tempfile.gettempdir()) / "kit_preview" / HERE.name
MIKTEX = Path.home() / "AppData/Local/Programs/MiKTeX/miktex/bin/x64"


def scene_names() -> tuple[str, list[str]]:
    src = EP.read_text(encoding="utf-8")
    cls = re.search(r"^class (Ep\d+\w*)\(", src, re.M)[1]
    names = re.findall(r'"(\w+)"', re.search(r"SCENES = \[(.*?)\]", src, re.S)[1])
    return cls, names


def render(cls, names, name, a):
    n = names.index(name) + 1
    stem = f"{n:02d}_{name}"
    media = WORK / stem
    media.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "KIT_ONLY": name,
           "KIT_TTS": "0" if a.silent else "1",
           "KIT_CAPTIONS": "0",   # captions are added below from the .srt, one sentence at a time
           "KIT_TTS_CACHE": os.environ.get("KIT_TTS_CACHE", str(ROOT / "media" / "tts"))}
    if not shutil.which("latex") and MIKTEX.exists():
        env["PATH"] = f"{MIKTEX}{os.pathsep}{env['PATH']}"
    quality = ["-r", "1920,1080", "--fps", "30"] if a.hq else ["-ql"]
    py = ROOT / ".venv" / "Scripts" / "python.exe"
    # no animation cache: on a cache hit Manim's clock does not advance, so the voice-over
    # of later beats lands too early or is lost
    cmd = [str(py if py.exists() else sys.executable), "-m", "manim", *quality, "--disable_caching",
           "--media_dir", str(media), "-o", stem, str(EP), cls]
    t0 = time.time()
    log = WORK / f"{stem}.log"
    with open(log, "w", encoding="utf-8") as fh:
        rc = subprocess.run(cmd, cwd=WORK, env=env, stdout=fh, stderr=subprocess.STDOUT).returncode
    text = log.read_text(encoding="utf-8", errors="replace")
    warn = [l.strip() for l in text.splitlines() if l.startswith(("[cue]", "[narration]"))]
    if rc != 0:
        return name, None, f"FAILED, see {log}: " + " | ".join(text.strip().splitlines()[-3:]), warn
    mp4 = max((media / "videos").rglob(f"{stem}.mp4"), key=lambda p: p.stat().st_mtime)
    OUT.mkdir(exist_ok=True)
    srt = mp4.with_suffix(".srt")
    if srt.exists():
        shutil.copy(srt, OUT / f"{stem}.srt")
    if srt.exists() and not a.no_captions:
        # draw the subtitles onto the preview (relative paths: the filter cannot take "C:")
        style = "FontName=Arial,FontSize=15,Outline=1,Shadow=0,MarginV=10"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4.name, "-vf",
                        f"subtitles={srt.name}:force_style='{style}'", "-c:a", "copy", "burned.mp4"],
                       cwd=mp4.parent, check=True)
        shutil.copy(mp4.parent / "burned.mp4", OUT / f"{stem}.mp4")
    else:
        shutil.copy(mp4, OUT / f"{stem}.mp4")
    return name, OUT / f"{stem}.mp4", f"{time.time() - t0:.0f}s", warn


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("scenes", nargs="+", help="scene names or numbers, or 'all'")
    ap.add_argument("--silent", action="store_true", help="no voice-over")
    ap.add_argument("--no-captions", action="store_true", help="do not draw captions on the frame")
    ap.add_argument("--hq", action="store_true", help="1080p30")
    ap.add_argument("--join", action="store_true", help="also concatenate the scenes into preview/all.mp4")
    ap.add_argument("--jobs", type=int, default=max(2, (os.cpu_count() or 4) // 2))
    a = ap.parse_args()
    cls, names = scene_names()
    want = names if a.scenes == ["all"] else [names[int(s) - 1] if s.isdigit() else s for s in a.scenes]
    bad = [s for s in want if s not in names]
    if bad:
        sys.exit(f"unknown scene(s) {bad}; scenes are: {', '.join(names)}")
    WORK.mkdir(parents=True, exist_ok=True)
    done, failed = [], False
    with ThreadPoolExecutor(a.jobs) as ex:
        for name, mp4, info, warn in ex.map(lambda s: render(cls, names, s, a), want):
            print(f"{name}: {mp4 or ''} ({info})", flush=True)
            for w in warn:
                print(f"    {w}")
            failed |= mp4 is None
            if mp4:
                done.append(mp4)
    if a.join and done and not failed:
        lst = WORK / "join.txt"
        lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in done), encoding="utf-8")
        out = OUT / "all.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                        "-c", "copy", str(out)], check=True)
        print(f"joined: {out}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
