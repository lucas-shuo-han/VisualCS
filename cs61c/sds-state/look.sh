#!/usr/bin/env bash
# Render voiced scene previews of one episode and tile their frames for review.
#   bash cs61c/sds-state/look.sh EP OUT_DIR [scene ...]      (run from the repo root; default: all scenes)
# Writes preview/NN_scene.mp4 (+ .srt) in the unit and OUT_DIR/epE/NN_scene/sheet*.png, then prints the
# kit's [layout] / [cue] / [still] warnings from the render logs.
set -u
EP=$1; OUT=$2; shift 2
UNIT=cs61c/sds-state
SK=.claude/skills/notes-to-3b1b-video/scripts
PY=$(ls ../../../.venv/Scripts/python.exe .venv/Scripts/python.exe 2>/dev/null | head -1)
export PYTHONIOENCODING=utf-8
[ $# -eq 0 ] && set -- all
"$PY" $SK/preview.py "$@" --unit $UNIT --ep "$EP" --jobs 4 2>&1 | grep -E "FAILED|\[cue\]|\[narration\]"
stem=$(basename "$(ls $UNIT/ep0${EP}_*.py)" .py)
for f in $UNIT/preview/[0-9]*.mp4; do
  [ "$f" -nt "$UNIT/$stem.py" ] || continue
  b=$(basename "$f" .mp4)
  rm -rf "$OUT/ep$EP/$b"
  "$PY" $SK/contact_sheet.py "$f" "${f%.mp4}.srt" "$OUT/ep$EP/$b" --at end --per-sheet 12 >/dev/null 2>&1
done
grep -h '^\[[a-z]' "$TEMP"/kit_preview/sds-state/"$stem"/*.log 2>/dev/null | sort | uniq -c
find "$OUT/ep$EP" -name 'sheet*.png' | sort
