"""Voice audition: the same beat in several voices and speeds.

    python audition.py                      every candidate at -10%, -15%, -20%
    python audition.py --rates -15          one speed only

Writes preview/voices/<engine>_<voice>_<rate>.wav. Listen, pick one, then set it
as VOICE / RATE in series.py.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "preview" / "voices"
# why_p 10 (speak: wording), a beat with both plain talk and a formula read aloud
TEXT = ("What should ay and bee be? We want the repeated steps to settle at one. So a sigma that has "
        "reached one must stay there, or the steps would never settle. Put sigma equals one into p. "
        "One cubed is still one, so p gives ay plus bee. For one to stay at one, ay plus bee must "
        "equal one. Call this our first wish.")
CANDIDATES = [("edge", "en-US-AndrewNeural"), ("edge", "en-US-BrianNeural"), ("edge", "en-GB-RyanNeural"),
              ("kokoro", "am_michael"), ("kokoro", "am_fenrir"), ("kokoro", "bm_george")]
ONE = ("import sys, shutil, tts; p, d = tts.synth('x', 'en', speak=sys.argv[1]); "
       "shutil.copy(p, sys.argv[2]); print(f'{d:.1f}s', sys.argv[2])")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--rates", nargs="+", default=["-10", "-15", "-20"])
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for engine, voice in CANDIDATES:
        for r in a.rates:
            out = OUT / f"{engine}_{voice}_{r.lstrip('-')}slower.wav"
            env = {**os.environ, "KIT_TTS_ENGINE": engine, "KIT_VOICE_EN": voice, "KIT_TTS_RATE": f"{r}%",
                   "KIT_TTS_CACHE": str(OUT / ".cache"), "PYTHONIOENCODING": "utf-8"}
            rc = subprocess.run([sys.executable, "-c", ONE, TEXT, str(out)], cwd=HERE, env=env).returncode
            if rc:
                print(f"FAILED {engine} {voice} {r}")
    shutil.rmtree(OUT / ".cache", ignore_errors=True)


if __name__ == "__main__":
    main()
