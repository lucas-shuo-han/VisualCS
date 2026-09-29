# Source this: `source cs182/env.sh` (Git Bash on Windows). Uses the manim venv from ../VisualCS/.venv.
export PATH="$PATH:/c/Users/18547/AppData/Local/Programs/MiKTeX/miktex/bin/x64"
export MANIM_KIT_SANS="Segoe UI"
export MANIM_KIT_MONO="Consolas"
export PYTHONIOENCODING=utf-8
VENV=/d/HuaweiMoveData/Users/18547/Desktop/VisualCS/.venv/Scripts
PY=$VENV/python.exe; MANIM=$VENV/manim.exe
export MANIM_CWD="C:/Users/18547/AppData/Local/Temp"   # dvisvgm breaks with cwd on D:
RENDER=.claude/skills/notes-to-3b1b-video/scripts/render.py
