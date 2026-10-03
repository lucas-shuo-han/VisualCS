"""Render the episodes of a unit folder and collect videos + subtitles.

Episodes come from SRC/series.py (order, languages, file names) or, without
it, from every `class EpNN...` in SRC/*.py.

Usage:
    python render.py SRC                          # every episode, every language, 1080p30
    python render.py SRC 2 5 --lang en            # episodes 2 and 5, English only
    python render.py SRC 3 --preview              # 480p15 quick check (stays in the media dir)
    python render.py SRC 3 --preview --voice      # ... with the voice-over
    python render.py SRC 3 --preview --lang en --lax   # draft: tolerate missing translations
    python render.py SRC --out videos/cs182-optim --jobs 4 --manim .venv/bin/manim

Full renders get the voice-over unless --no-voice (it needs network for
edge-tts; clips are cached, so re-renders are offline); previews are silent
unless --voice. Finished videos go to OUT/<lang>/NN-slug.mp4 (+ .srt), or
OUT/<file stem>.mp4 for a single-language unit.

Every (episode, language) renders in its own media dir, so parallel jobs never
race on Manim's text/SVG cache. Logs: MEDIA/<lang>/epNN.log.
"""

import argparse
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project import Unit, find_manim  # noqa: E402


def render(unit, ep, lang, a, voice):
    n, scene = ep["num"], ep["scene"]
    media_root = Path(a.media).resolve()
    media = media_root / lang / f"ep{n:02d}"
    media.mkdir(parents=True, exist_ok=True)
    quality = ["-ql"] if a.preview else ["-r", "1920,1080", "--fps", "30"]
    env = {**os.environ, "KIT_LANG": lang, "PYTHONIOENCODING": "utf-8",
           "KIT_TTS": "1" if voice else "0",
           "KIT_TTS_CACHE": os.environ.get("KIT_TTS_CACHE", str(media_root / "tts"))}
    if a.lax:
        env["KIT_I18N_LAX"] = "1"
    log = media_root / lang / f"ep{n:02d}.log"
    with open(log, "w", encoding="utf-8") as fh:
        # no animation cache: on a cache hit Manim's clock does not advance and the voice-over drifts
        rc = subprocess.run([a.manim, *quality, "--disable_caching", "--media_dir", str(media), ep["file"], scene],
                            cwd=unit.src, stdout=fh, stderr=subprocess.STDOUT, env=env).returncode
    if rc != 0:
        tail = log.read_text(encoding="utf-8", errors="replace").strip().splitlines()[-3:]
        return f"FAILED ({log}): " + " | ".join(tail)
    qdir = "480p15" if a.preview else "1080p30"
    mp4 = next((media / "videos").rglob(f"{qdir}/{scene}.mp4"))
    srt = mp4.with_suffix(".srt")
    if a.preview:
        return str(mp4)
    out = Path(a.out).resolve()
    dst = out / lang if len(unit.langs) > 1 else out
    dst.mkdir(parents=True, exist_ok=True)
    name = unit.slug(ep, lang)
    shutil.copy(mp4, dst / f"{name}.mp4")
    if srt.exists():
        shutil.copy(srt, dst / f"{name}.srt")
    return str(dst / f"{name}.mp4")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", help="unit folder: manim_kit.py, series.py, epNN_*.py")
    ap.add_argument("episodes", nargs="*", type=int)
    ap.add_argument("--lang", default="all", help="a language code, or 'all' (series.py LANGS)")
    ap.add_argument("--preview", action="store_true", help="480p15, output stays in the media dir")
    ap.add_argument("--voice", action=argparse.BooleanOptionalAction, default=None,
                    help="voice-over (default: on for full renders, off for previews)")
    ap.add_argument("--lax", action="store_true", help="warn instead of failing on missing translations")
    ap.add_argument("--out", default="videos", help="where finished mp4/srt are collected")
    ap.add_argument("--media", default="media", help="scratch media root")
    ap.add_argument("--jobs", type=int, default=3, help="parallel renders (~ CPU cores / 2)")
    ap.add_argument("--manim", default=None, help="manim executable (default: .venv, then PATH)")
    a = ap.parse_args()
    a.manim = a.manim or find_manim()

    unit = Unit(a.src)
    eps = unit.select(a.episodes)
    if not eps:
        sys.exit(f"no episodes found in {unit.src}")
    langs = unit.langs if a.lang == "all" else [a.lang]
    voice = not a.preview if a.voice is None else a.voice
    jobs = [(e, lang) for e in eps for lang in langs]
    failed = False
    with ThreadPoolExecutor(a.jobs) as ex:
        results = ex.map(lambda j: (j, render(unit, j[0], j[1], a, voice)), jobs)
        for (ep, lang), result in results:
            failed |= result.startswith("FAILED")
            print(f"episode {ep['num']} [{lang}]: {result}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
