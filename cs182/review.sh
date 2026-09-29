# usage: bash cs182/review.sh N   -> preview render of episode N + contact sheets (end & mid) in $TEMP/shN, $TEMP/shNm
source cs182/env.sh
N=$1
$PY $RENDER cs182/function-approximation --preview --only $N --media $TEMP/media182 --manim $MANIM | cut -c1-120
V=$(find $TEMP/media182/ep0$N/videos -name "Ep0$N*.mp4" | head -1); V=${V%.mp4}
[ -f "$V.mp4" ] || { tail -15 $TEMP/media182/ep0$N.log | cut -c1-200; exit 1; }
$PY .claude/skills/notes-to-3b1b-video/scripts/contact_sheet.py $V.mp4 $V.srt $TEMP/sh$N --at end 2>&1 | tail -1
$PY .claude/skills/notes-to-3b1b-video/scripts/contact_sheet.py $V.mp4 $V.srt $TEMP/sh${N}m --at mid 2>&1 | tail -1
