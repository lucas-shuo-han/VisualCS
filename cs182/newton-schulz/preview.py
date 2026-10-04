"""Fast previews: render single scenes of the episodes, in parallel, with the voice.

    python preview.py the_gap                 one scene  -> preview/09_the_gap.mp4 (+ .srt)
    python preview.py 9 10 11                 story scenes by number (1-14, across the episodes)
    python preview.py ep2                     every scene of episode 2, cards included
    python preview.py ep3_recap ep1_opening ep2_closing     recaps and cards by name
    python preview.py all                     everything, in parallel
    python preview.py ep3 --join              ... and glue the clips into preview/joined.mp4
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
OUT = HERE / "preview"
# dvisvgm exits with 127 when the working directory is on the D: drive of this
# machine, so Manim runs from a scratch folder on the system drive instead
WORK = Path(tempfile.gettempdir()) / "kit_preview" / HERE.name
MIKTEX = Path.home() / "AppData/Local/Programs/MiKTeX/miktex/bin/x64"


def targets() -> list[dict]:
    """Every previewable piece, in story order: ep (1..), file, cls, scene (the method to run),
    key (what to type) and stem (the output name). Story scenes are numbered 01.. across the
    episodes; recaps and cards carry their episode instead."""
    out, story = [], 0
    for k, f in enumerate(sorted(HERE.glob("ep[0-9][0-9]_*.py")), 1):
        src = f.read_text(encoding="utf-8")
        cls = re.search(r"^class (Ep\d+\w*)\(", src, re.M)[1]
        names = re.findall(r'"(\w+)"', re.search(r"SCENES = \[(.*?)\]", src, re.S)[1])
        for name in ["opening"] + names + ["closing"]:
            if name in ("opening", "closing"):
                key = stem = f"ep{k}_{name}"
            elif name.startswith(f"ep{k}_"):
                key = stem = name
            else:
                story += 1
                key, stem = name, f"{story:02d}_{name}"
            out.append(dict(ep=k, file=f, cls=cls, scene=name, key=key, stem=stem,
                            num=story if key == name and not name.startswith("ep") else None))
    return out


def render(t, a):
    name, stem, cls, EP = t["scene"], t["stem"], t["cls"], t["file"]
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
        return stem, None, f"FAILED, see {log}: " + " | ".join(text.strip().splitlines()[-3:]), warn
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
    return stem, OUT / f"{stem}.mp4", f"{time.time() - t0:.0f}s", warn


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("scenes", nargs="+", help="scene names or numbers, ep1/ep2/ep3, or 'all'")
    ap.add_argument("--silent", action="store_true", help="no voice-over")
    ap.add_argument("--no-captions", action="store_true", help="do not draw captions on the frame")
    ap.add_argument("--hq", action="store_true", help="1080p30")
    ap.add_argument("--join", action="store_true", help="also concatenate the clips into preview/joined.mp4")
    ap.add_argument("--jobs", type=int, default=max(2, (os.cpu_count() or 4) // 2))
    a = ap.parse_args()
    every = targets()
    want, bad = [], []
    for x in a.scenes:
        if x == "all":
            want += every
        elif re.fullmatch(r"ep\d+", x):
            want += [t for t in every if t["ep"] == int(x[2:])]
        else:
            hit = [t for t in every if t["key"] == x or (x.isdigit() and t["num"] == int(x))]
            want += hit
            bad += [] if hit else [x]
    if bad:
        sys.exit(f"unknown scene(s) {bad}; scenes are: {', '.join(t['key'] for t in every)}")
    WORK.mkdir(parents=True, exist_ok=True)
    done, failed = [], False
    with ThreadPoolExecutor(a.jobs) as ex:
        for name, mp4, info, warn in ex.map(lambda t: render(t, a), want):
            print(f"{name}: {mp4 or ''} ({info})", flush=True)
            for w in warn:
                print(f"    {w}")
            failed |= mp4 is None
            if mp4:
                done.append(mp4)
    if a.join and done and not failed:
        lst = WORK / "join.txt"
        lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in done), encoding="utf-8")
        out = OUT / "joined.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                        "-c", "copy", str(out)], check=True)
        print(f"joined: {out}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
