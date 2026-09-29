# Windows setup: a virtualenv with Manim + edge-tts, and the fonts the kit uses.
#
#   powershell -ExecutionPolicy Bypass -File setup_env.ps1 [-Venv .venv]
#
# Manim's Windows wheels bundle cairo/pango and decode media with PyAV, so no
# system packages and no ffmpeg are needed (contact_sheet.py uses PyAV too).
# LaTeX (MathTex) is not installed here: use MiKTeX if you really need it, or
# stick to Text / MarkupText.
param([string]$Venv = ".venv")
$ErrorActionPreference = "Stop"

# `python` may be the Microsoft Store stub, which hangs or opens the Store: prefer the py launcher.
$py = Get-Command py -ErrorAction SilentlyContinue
if ($py) { & py -3 -m venv $Venv } else { & python -m venv $Venv }
$pyexe = Join-Path $Venv "Scripts\python.exe"
& $pyexe -m pip install -q --upgrade pip
& $pyexe -m pip install -q manim edge-tts "audioop-lts; python_version>='3.13'"
& $pyexe (Join-Path $PSScriptRoot "win_fonts.py")
& $pyexe -c "import manim, manimpango; print('manim', manim.__version__, '| Noto CJK:', 'Noto Sans CJK SC' in manimpango.list_fonts())"
Write-Host "manim binary: $(Join-Path $Venv 'Scripts\manim.exe')"
Write-Host "Always set `$env:PYTHONIOENCODING='utf-8' before running the scripts (the console codepage can't print CJK)."
