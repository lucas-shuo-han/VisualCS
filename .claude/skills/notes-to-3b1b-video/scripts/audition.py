"""Voice audition: one beat in several voices and speeds, for the user to pick by ear.

    python audition.py --unit cs182/newton-schulz                       default candidates, three speeds
    python audition.py --unit <unit> --rates -5 -10 -15                 speeds in percent
    python audition.py --unit <unit> --text "What should ay and bee be? ..."
    python audition.py --unit <unit> --voices edge:en-US-BrianNeural kokoro:am_michael

Writes <unit>/preview/voices/<engine>_<voice>_<rate>.wav. The user listens and names
one; put it in series.py:

    TTS = {"engine": "edge", "rate": "-4%", "voice": {"en": "en-US-AndrewNeural"}}

Pick the beat with care: a few sentences that have both plain talk and a formula read
aloud, written in spoken form (what `speak=` would hold). Do this before the first full
render: a different voice or speed means every clip is synthesized again and every
duration changes.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

TEXT = ("What should ay and bee be? We want the repeated steps to settle at one. So a value that has "
        "reached one must stay there, or the steps would never settle. Put x equals one into p. "
        "One cubed is still one, so p gives ay plus bee. For one to stay at one, ay plus bee must "
        "equal one. Call this our first wish.")
CANDIDATES = {"en": ["edge:en-US-AndrewNeural", "edge:en-US-BrianNeural", "edge:en-GB-RyanNeural",
                     "kokoro:am_michael", "kokoro:am_fenrir", "kokoro:bm_george"],
              "zh": ["edge:zh-CN-YunxiNeural", "edge:zh-CN-YunjianNeural", "edge:zh-CN-XiaoxiaoNeural",
                     "kokoro:zm_yunxi", "kokoro:zf_xiaoxiao"]}
ONE = ("import sys, shutil, tts; p, d = tts.synth('x', sys.argv[3], speak=sys.argv[1]); "
       "shutil.copy(p, sys.argv[2]); print(f'{d:.1f}s', sys.argv[2])")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--unit", required=True, help="the folder with tts.py (and say_as.py)")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--text", default=None, help="the beat to speak, in spoken form")
    ap.add_argument("--voices", nargs="+", default=None, help="engine:voice ...")
    ap.add_argument("--rates", nargs="+", default=["-5", "-10", "-15"], help="percent, e.g. -10 0 +5")
    a = ap.parse_args()
    unit = Path(a.unit).resolve()
    out_dir = unit / "preview" / "voices"
    out_dir.mkdir(parents=True, exist_ok=True)
    text = a.text or TEXT
    if a.text is None and a.lang != "en":
        sys.exit("give --text in the language of --lang")
    for cand in a.voices or CANDIDATES.get(a.lang, CANDIDATES["en"]):
        engine, voice = cand.split(":", 1)
        for r in a.rates:
            r = r if r[0] in "+-" else "+" + r
            out = out_dir / f"{engine}_{voice}_{r}.wav"
            env = {**os.environ, "KIT_TTS_ENGINE": engine, f"KIT_VOICE_{a.lang.upper()}": voice,
                   "KIT_TTS_RATE": f"{r}%", "KIT_TTS_CACHE": str(out_dir / ".cache"),
                   "PYTHONIOENCODING": "utf-8"}
            rc = subprocess.run([sys.executable, "-c", ONE, text, str(out), a.lang], cwd=unit, env=env).returncode
            if rc:
                print(f"FAILED {engine} {voice} {r}")
    shutil.rmtree(out_dir / ".cache", ignore_errors=True)
    print(f"listen in {out_dir}")


if __name__ == "__main__":
    main()
