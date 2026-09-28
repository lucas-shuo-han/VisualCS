"""Render the CS61C RISC-V episodes and collect the videos + subtitles.

Usage:
    python tools/render.py                        # all episodes, zh and en, 1080p30
    python tools/render.py 3 5 --lang en          # only episodes 3 and 5, English
    python tools/render.py --preview 2            # quick 480p15 render of episode 2
    python tools/render.py --preview --lax 2 --lang en   # draft: allow missing translations
    python tools/render.py --preview --voice 2    # preview with the TTS voice-over

Full renders get the voice-over (VCS_TTS=1, see cs61c/riscv/tts.py) unless
--no-voice; previews are silent unless --voice.

Videos land in videos/cs61c-riscv/{zh,en}/. Each (episode, language) renders
in its own media directory, so several can run in parallel without clobbering
Manim's shared text cache.
"""

import argparse
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "cs61c" / "riscv"
OUT = ROOT / "videos" / "cs61c-riscv"
sys.path.insert(0, str(SRC))
import series  # noqa: E402


def render(ep, lang, preview, media_root, manim, lax, voice):
    e = series.SERIES[ep - 1]
    media = media_root / lang / f"ep{ep:02d}"
    quality = ["-ql"] if preview else ["-r", "1920,1080", "--fps", "30"]
    cmd = [manim, *quality, "--media_dir", str(media), e.file, e.scene]
    log = media_root / lang / f"ep{ep:02d}.log"
    media.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "VCS_LANG": lang, "PYTHONIOENCODING": "utf-8"}
    if lax:
        env["VCS_I18N_LAX"] = "1"
    env["VCS_TTS"] = "1" if voice else "0"
    with open(log, "w", encoding="utf-8") as fh:
        rc = subprocess.run(cmd, cwd=SRC, stdout=fh, stderr=subprocess.STDOUT, env=env).returncode
    if rc != 0:
        return ep, lang, f"FAILED (see {log})"
    quality_dir = "480p15" if preview else "1080p30"
    mp4 = next((media / "videos").rglob(f"{quality_dir}/{e.scene}.mp4"))
    srt = mp4.with_suffix(".srt")
    if preview:
        return ep, lang, str(mp4)
    dst = OUT / lang
    dst.mkdir(parents=True, exist_ok=True)
    name = series.slug(ep, lang)
    shutil.copy(mp4, dst / f"{name}.mp4")
    shutil.copy(srt, dst / f"{name}.srt")
    return ep, lang, str(dst / f"{name}.mp4")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episodes", nargs="*", type=int)
    ap.add_argument("--lang", choices=["zh", "en", "all"], default="all")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--lax", action="store_true", help="warn instead of failing on missing translations")
    ap.add_argument("--voice", action=argparse.BooleanOptionalAction, default=None,
                    help="TTS voice-over (default: on for full renders, off for previews)")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--media", default=str(ROOT / "media"))
    ap.add_argument("--manim", default=shutil.which("manim") or "manim")
    a = ap.parse_args()
    eps = a.episodes or range(1, len(series.SERIES) + 1)
    langs = ["zh", "en"] if a.lang == "all" else [a.lang]
    voice = not a.preview if a.voice is None else a.voice
    jobs = [(e, l) for e in eps for l in langs]
    with ThreadPoolExecutor(a.jobs) as ex:
        results = ex.map(lambda j: render(j[0], j[1], a.preview, Path(a.media), a.manim, a.lax, voice), jobs)
        failed = False
        for ep, lang, result in results:
            failed |= result.startswith("FAILED")
            print(f"episode {ep} [{lang}]: {result}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
