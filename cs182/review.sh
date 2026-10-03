# usage: UNIT=optimization MEDIA_ROOT=$TEMP/media_x bash cs182/review.sh N [--voice]
#   preview of episode N of cs182/$UNIT + contact sheets (end & mid) in $TEMP/${UNIT}_shN and ${UNIT}_shNm
source cs182/env.sh
UNIT=${UNIT:-function-approximation}
N=$1; shift
NN=$(printf "%02d" $N)
M=${MEDIA_ROOT:-$TEMP/media_$UNIT}
$PY $RENDER cs182/$UNIT $N --preview --media $M --manim $MANIM "$@" | cut -c1-140
V=$(find $M/en/ep$NN/videos -path "*480p15*" -name "*.mp4" | head -1); V=${V%.mp4}
[ -f "$V.mp4" ] || { tail -15 $M/en/ep$NN.log | cut -c1-200; exit 1; }
$PY .claude/skills/notes-to-3b1b-video/scripts/contact_sheet.py $V.mp4 $V.srt $TEMP/${UNIT}_sh$N --at end 2>&1 | tail -1
$PY .claude/skills/notes-to-3b1b-video/scripts/contact_sheet.py $V.mp4 $V.srt $TEMP/${UNIT}_sh${N}m --at mid 2>&1 | tail -1
