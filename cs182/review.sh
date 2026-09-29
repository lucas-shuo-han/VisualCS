# usage: bash cs182/review.sh N [--voice]  -> preview of episode N + contact sheets (end & mid) in $TEMP/shN, $TEMP/shNm
source cs182/env.sh
N=$1; shift
M=${MEDIA_ROOT:-$TEMP/media182}
$PY $RENDER cs182/function-approximation $N --preview --media $M --manim $MANIM "$@" | cut -c1-140
V=$(find $M/en/ep0$N/videos -name "Ep0$N*.mp4" | head -1); V=${V%.mp4}
[ -f "$V.mp4" ] || { tail -15 $M/en/ep0$N.log | cut -c1-200; exit 1; }
$PY .claude/skills/notes-to-3b1b-video/scripts/contact_sheet.py $V.mp4 $V.srt $TEMP/sh$N --at end 2>&1 | tail -1
$PY .claude/skills/notes-to-3b1b-video/scripts/contact_sheet.py $V.mp4 $V.srt $TEMP/sh${N}m --at mid 2>&1 | tail -1
