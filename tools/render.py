"""Render the CS61C RISC-V episodes and collect the videos + subtitles.

Usage:
    python tools/render.py                 # all episodes, 1080p30
    python tools/render.py 3 5             # only episodes 3 and 5
    python tools/render.py --preview 2     # quick 480p15 render of episode 2

Each episode renders in its own media directory, so several can run in
parallel without clobbering Manim's shared text cache.
"""

import argparse
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "cs61c" / "riscv"
OUT = ROOT / "videos" / "cs61c-riscv"

EPISODES = {
    1: ("ep01_isa_registers.py", "Ep01ISARegisters", "01-从C到汇编-ISA与寄存器"),
    2: ("ep02_memory.py", "Ep02Memory", "02-内存-字节寻址与lw-sw"),
    3: ("ep03_branches_loops.py", "Ep03BranchesLoops", "03-决策与循环"),
    4: ("ep04_procedures.py", "Ep04Procedures", "04-函数调用与栈"),
    5: ("ep05_formats_ris.py", "Ep05FormatsRIS", "05-指令格式上-R-I-S"),
    6: ("ep06_formats_buj.py", "Ep06FormatsBUJ", "06-指令格式下-B-U-J"),
    7: ("ep07_call.py", "Ep07CALL", "07-CALL-编译汇编链接加载"),
}


def render(ep, preview, media_root, manim):
    file, scene, name = EPISODES[ep]
    media = media_root / f"ep{ep:02d}"
    quality = ["-ql"] if preview else ["-r", "1920,1080", "--fps", "30"]
    cmd = [manim, *quality, "--media_dir", str(media), file, scene]
    log = media_root / f"ep{ep:02d}.log"
    media.mkdir(parents=True, exist_ok=True)
    with open(log, "w") as fh:
        rc = subprocess.run(cmd, cwd=SRC, stdout=fh, stderr=subprocess.STDOUT).returncode
    if rc != 0:
        return ep, f"FAILED (see {log})"
    mp4 = next((media / "videos").rglob(f"{scene}.mp4"))
    srt = mp4.with_suffix(".srt")
    if preview:
        return ep, str(mp4)
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copy(mp4, OUT / f"{name}.mp4")
    shutil.copy(srt, OUT / f"{name}.srt")
    return ep, str(OUT / f"{name}.mp4")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episodes", nargs="*", type=int)
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--media", default=str(ROOT / "media"))
    ap.add_argument("--manim", default=shutil.which("manim") or "manim")
    a = ap.parse_args()
    eps = a.episodes or sorted(EPISODES)
    with ThreadPoolExecutor(a.jobs) as ex:
        for ep, result in ex.map(lambda e: render(e, a.preview, Path(a.media), a.manim), eps):
            print(f"episode {ep}: {result}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
