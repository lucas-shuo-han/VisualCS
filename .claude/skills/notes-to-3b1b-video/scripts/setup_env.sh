#!/usr/bin/env bash
# Install Manim and its system dependencies, then create a virtualenv.
#
#   bash setup_env.sh [VENV_DIR] [--latex]
#
# --latex also installs a LaTeX toolchain, needed only for MathTex / Tex
# (equations, Matrix with tex entries). Skip it if you only use Text.
#
# A virtualenv is used on purpose: Debian/Ubuntu's system pip ships a patched
# setuptools that fails to build some Manim dependencies (e.g. `srt`) with
# "AttributeError: install_layout".
set -euo pipefail

VENV=".venv"
LATEX=0
for arg in "$@"; do
  case "$arg" in
    --latex) LATEX=1 ;;
    *) VENV="$arg" ;;
  esac
done

if command -v apt-get >/dev/null 2>&1; then
  SUDO=""; [ "$(id -u)" = 0 ] || SUDO="sudo"
  $SUDO apt-get update -qq || true   # unreachable PPAs are harmless here
  $SUDO apt-get install -y -qq ffmpeg libcairo2-dev libpango1.0-dev pkg-config \
    python3-dev python3-venv fonts-noto-cjk fonts-dejavu-core
  if [ "$LATEX" = 1 ]; then
    $SUDO apt-get install -y -qq texlive-latex-base texlive-latex-extra \
      texlive-fonts-recommended dvisvgm
  fi
elif command -v brew >/dev/null 2>&1; then
  brew install ffmpeg cairo pango pkg-config
  brew install --cask font-noto-sans-cjk-sc font-dejavu || true
  if [ "$LATEX" = 1 ]; then brew install --cask basictex; fi
else
  echo "Install ffmpeg, cairo, pango and pkg-config with your package manager, then re-run." >&2
fi

python3 -m venv "$VENV"
"$VENV/bin/pip" install -q --upgrade pip setuptools wheel
"$VENV/bin/pip" install -q manim
"$VENV/bin/python" -c "import manim, manimpango; print('manim', manim.__version__, '| fonts:', len(manimpango.list_fonts()))"
echo "manim binary: $VENV/bin/manim"
