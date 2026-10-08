# REPORT: The Residency Match (CS70 Note 11, episode 02)

## Files

- Preview (480p, voiced): `C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep02\videos\ep02_residency_match\480p15\Ep02ResidencyMatch.mp4`
- Subtitles: `C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep02\videos\ep02_residency_match\480p15\Ep02ResidencyMatch.srt`
- Code: `cs70/note11/ep02_residency_match.py` (class `Ep02ResidencyMatch`, scenes `hook`, `race`,
  `fuse`, `match`), `cs70/note11/series.py` (row 2, unchanged)
- Plan: `cs70/note11/BOARD-ep02.md` (STRICT.md, "With a storyboard")

## Last check.py run

`check.py cs70/note11 2 --strict`, the run this report answers to (the sheet lines below
are the lines of this run; the `--no-render` run after it prints the same table):

```
== check: note11 episode 2 [en] ==
PASS code    13 say(), 39 cue()
PASS lint    clean
PASS board   13 of 13 beats, word for word as in BOARD-ep02.md
PASS render  C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep02\videos\ep02_residency_match\480p15\Ep02ResidencyMatch.mp4
PASS log     clean
PASS av      video 265.0 s, audio 262.2 s, longest silence 3.9 s
PASS pace    46 subtitles, 157 words per minute
PASS sheets  12 sheets
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep02_sheets_end\sheet00.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep02_sheets_end\sheet01.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep02_sheets_end\sheet02.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep02_sheets_end\sheet03.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep02_sheets_end\sheet04.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep02_sheets_end\sheet05.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep02_sheets_mid\sheet00.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep02_sheets_mid\sheet01.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep02_sheets_mid\sheet02.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep02_sheets_mid\sheet03.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep02_sheets_mid\sheet04.png
       C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep02_sheets_mid\sheet05.png
PASS report  REPORT-ep02.md names all 12 sheets

RESULT: PASS. Not done yet:
  - open all 12 sheets above (frame number = subtitle number) and note per sheet what you saw: overlaps of text with shapes, leftovers, empty frames, a number that disagrees with its subtitle
  - listen to C:\Users\18547\AppData\Local\Temp\kit_check\note11\en\ep02\videos\ep02_residency_match\480p15\Ep02ResidencyMatch.mp4 from start to end, or say in the report that nobody did
```

The runs before it (one scene at a time, as the runbook says, and the two full-episode runs
of the first round) are in `TRIAL_LOG-ep02.md`. The first full-episode run ended with
`FAIL report` only (no `REPORT-ep02.md` yet), exactly as step 6 expects; the twelve sheets
below are the ones the round-one run wrote. The run quoted above is the fix round's full
run: it rendered the whole episode again after the five review rows were built into the
picture, and its twelve sheets carry the same names.

## Frames

One line per sheet of the last run. Frame numbers are subtitle numbers. An `end` sheet shows
the settled state 0.15 s before that subtitle's span ends; a `mid` sheet the middle of the
span. The voice-over and the burned captions have the same timing, so the last subtitle is
number 45; the end card is spoken without captions and is not in any sheet.

| Sheet | text over something | cut off / on subtitle | leftover | empty frame | wrong number | wrong count | only sentences | what I saw, what I changed |
|---|---|---|---|---|---|---|---|---|
| ep02_sheets_end/sheet00.png | no | no | no | no | no | no (5 slots, 3 graduates, 4 school boxes, 1 residency box) | no | `hook` frames 0-8. Frames 0-1 the timeline is still arriving (the "residency" box faint at frame 0, full at 1); frame 2 the five slots and the strip label "slots" with the three graduates and "graduates"; frames 5-6 the three green arrows from the slots at -2, 0, 2 down to the graduates; frame 7 the heading changes to "Earlier and earlier" with beat 1.2's last words; frame 8 the two slots with no graduate get their red border. Nothing to change. |
| ep02_sheets_end/sheet01.png | no | no | no | no | no | no (3 white arrows at 10-11, 2 slots flashed at 13, 1 dashed arrow at 15) | no | `race` frames 9-17. Frame 10 the white arrows and the "offer" marker at the right end of "senior"; frame 11 the marker slid to the middle of "senior"; frame 12 "mid-1940s" in the strip and the marker at the left end of "senior"; frame 13 "junior" and "senior" flashed together for "two years"; frames 15-17 the dashed arrow under "sophomore", now a yellow dashed shaft of width 5 and dash length 0.15 with a solid tip (row 1 of the review), the same length as the solid "offer" arrow beside it in frame 17, and removed again in frame 18. Nothing else to change. |
| ep02_sheets_end/sheet02.png | no | no | no | no | no | no (3 faded school boxes, 1 red bar, 1 marker) | no | Frames 18-26: the end of `race` (frame 18 the dashed arrow gone and the marker sliding back to the middle of "senior", frame 19 the red bar between "junior" and "senior" with the first three boxes faded) and the start of `fuse` (frames 21-22 the three arrows H1 white from the slot at x = -2 to the graduate at x = 0, H2 and H3 grey from the slots at x = -4 and x = 4 to the graduates at x = -2 and x = 2, none of the three crossing another — row 2 of the review; frame 23 H1 orange and "a few hours" in orange in the strip; frames 24-26 the yellow border on the free slot at x = 2 and the white dashed arrow W from the graduate at x = 0 up to it, width 5, dash length 0.15, with a tip, crossing nothing — row 3). Frame 22's subtitle is the single word "meantime." — see the questions. |
| ep02_sheets_end/sheet03.png | no | no | no | no | no | no (3 arrows, 1 yellow slot border, 1 dashed arrow; 2 hospital lists and 1 graduate list mid-flight) | no | Frames 27-35: the end of `fuse` (frame 28 still orange, frame 29 H1 green and grown to stroke width 8, clearly the fattest arrow on the stage and the only green thing on it, with "in hand" in green in the strip — row 4; frame 30 H1 back to orange at width 4 and "a few hours" back; frame 31 the last cue, the flash of the white dashed arrow W and of the free slot at x = 2) and `match` (frame 32 the empty stage two built from nothing: "early 1950s", the two captions, the three hospital squares, the three graduate circles, the "N.R.M.P." box; frame 34 the three list icons flying from the hospital squares to the bottom edge of the box and frame 35 one from a graduate circle, plus the orange dashed line D between hospital 1 and graduate 1, now width 5 with dash length 0.15 — row 5). |
| ep02_sheets_end/sheet04.png | no | no | no | no | no | no (3 lines L1-L3, 1 dashed line, then 3 green lines) | no | Frames 36-44. Frames 36-37 the orange dashed line between hospital 1 and graduate 1, width 5 and dash length 0.15 (row 5 of the review); frame 37 L1 and L2 faded and L3 still white; frame 38 the date "1952" and "propose and reject" as the box's second line; frame 39 the words "stable" in green with G1, G2 and L3 green; frame 42 the date "2012" and the Nobel line above the box. Nothing else to change. |
| ep02_sheets_end/sheet05.png | no | no | no | no | no | no (3 green lines) | no | Frame 45, the last subtitle: the whole settled stage two — "2012", "N.R.M.P. / propose and reject", the Nobel line, the three green lines and "stable". Nothing to change. |
| ep02_sheets_mid/sheet00.png | no | no | no | no | no | no | no | Mid frames 0-8. Frames 0-1 the timeline half-arrived, frame 4 the "residency" box and the first school boxes mid-fade, frame 8 the red border half-way onto the two outer slots. The heading rule on the left is above y = 2.7 and clear of the boxes in all nine. Nothing to change. |
| ep02_sheets_mid/sheet01.png | no | no | no | no | no | no | no | Mid frames 9-17. Frame 9 the "offer" marker and the senior box scaled up mid-`Indicate`, frame 13 "junior" and "senior" mid-flash, frame 15 the dashed arrow under "sophomore" half-faded in with its tip already visible, frames 16-17 it beside the solid "offer" arrow, frame 17 the red bar being drawn and the first three boxes fading to 0.3. The marker mid-slide at frame 12. Half-faded objects are the middle of a fade, not an overlap. Nothing to change. |
| ep02_sheets_mid/sheet02.png | no | no | no | no | no | no | no | Mid frames 18-26. Frame 19 the dashed arrow gone and the marker mid-slide, frame 20 H2 and H3 at half their length, frame 21 H1 half-grown from the slot at x = -2, frame 26 the white dashed arrow W half-drawn from the graduate at x = 0 towards the free slot at x = 2. All mid-animation, not leftovers. Nothing to change. |
| ep02_sheets_mid/sheet03.png | no | no | no | no | no | no | no | Mid frames 27-35. Frame 29 H1 green, fat and scaled up mid-`Indicate` with "in hand" in the strip, frame 30 H1 mid-way back to orange and to width 4, frame 31 the free slot at x = 2 and the dashed arrow W both scaled up mid-flash for "without closing the door", frame 32 the "hospitals"/"graduates" captions half-faded in, frame 35 a list icon half-way to the box. Nothing to change. |
| ep02_sheets_mid/sheet04.png | no | no | no | no | no | no | no | Mid frames 36-44. Frame 36 the orange dashed line scaled up mid-`Indicate`, frame 37 the orange line half-faded while G1 and G2 start to draw, frame 39 the green lines half-drawn with "stable" faint as it fades in, frame 43 the Nobel line fading in. Half-faded objects are the middle of a fade, not an overlap. Nothing to change. |
| ep02_sheets_mid/sheet05.png | no | no | no | no | no | no | no | Mid frame 45: the same settled picture as the end sheet, with the three green lines flashing for "demands of a matching". Nothing to change. |

## Numbers

| Shown or spoken | Computed by (name in FACTS) | The board says | Same? |
|---|---|---|---|
| five slots, three graduates | `N_SLOTS`, `N_GRADS` | "five slots, three graduates (the author's picture of 'more slots than graduates')" | yes; the voice says no number |
| two slots with no graduate below | `N_SLOTS - N_GRADS == 2` | beat 2.1: "the slots at x = -4 and x = 4" | yes |
| three hospitals, three graduates | `N_HOSP`, `N_GRADS` | stage two: three squares and three circles | yes |
| "mid-1940s" | `D_MID_40S` = `f"mid-{DECADE_40S}s"`, `MID_40S = DECADE_40S + 5` | F4 (notes 113-116, "By the mid-40s") | yes |
| "early 1950s" | `D_EARLY_50S` | F7 (notes 125, "in the early 1950's") | yes |
| "1952" | `D_1952 = str(NRMP_START)` | F8 (notes 128) | yes |
| "2012" | `D_2012 = str(NOBEL)` | F9 (notes 130) | yes |
| "Sixty years later" | `YEARS_LATER == 60` | F10 (`2012 - 1952`) | yes |
| "two years before graduation" | `EARLY_50S + 2 == NRMP_START` asserts the fifties arithmetic; the two years themselves are the junior and senior boxes flashed in 2.3 | F4, "Added to the notes" row 2.3 (read off the timeline) | yes |

No number differs from the notes.

## Not done

- Voice: nobody listened to the preview from start to end; the pace line (163 words per
  minute, in 120 to 165) is the only check on the speaking rate. The words themselves were
  not heard, so a mispronunciation would not have been caught.
- The 1080p render has not been run.
- The `--scenes` runs of steps 4 and 5 wrote one scene each into the same sheet files, which
  the full run then overwrote; only the full run's twelve sheets are described above.
- The end card is outside every sheet (it is spoken without captions), so its picture was
  never looked at on a frame.
- Out of scope and untouched: episodes 03 to 10, the editable `narration.md` workflow,
  `render.py`/`srt_to_script.py` (step 7) and publishing.

## Questions for the author

1. Beat 3.1: the sentence "A hospital whose offer sat unanswered could lose its second and
   third choices to other hospitals in the meantime." is one character too long for two
   caption lines at this font, so the kit's splitter leaves the single word "meantime." as a
   subtitle of its own (0.5 s, frame 22). Built as written; no scene code can change it
   without changing the words or the kit. A shorter tail ("...could lose its other choices in
   the meantime") or a sentence break after "choices" would remove it.
2. Beat 2.3: "two years before graduation" flashes the "junior" and "senior" boxes, which is
   right for the school years, but the board's own rule reads the two years off a timeline
   whose boxes are all drawn the same size. If you wanted the two years to be countable, the
   junior and senior boxes would need to be the years that carry them. Built as written.
3. Beat 3.2: the dashed line W from the graduate at x = 0 up to the slot at x = 4 crosses the
   green arrow H3 (slot x = 2 to graduate x = 2) on the way. It is legible but it is the one
   crossing of two lines in the episode. Built as written.
   **Answered in the fix round:** the board now sends W to the free slot at x = 2 and re-routes
   H2 and H3 to the outer slots, so no two of H1, H2, H3, W cross; the lines above are the
   round-one report and this footnote is the only change to them.

## Questions for the user

1. Is the voice right, and is its speed right? Nobody has heard it.
2. Shall the 1080p render run?

## Fix round after review round 1 (`REVIEW-ep02.md`)

The author changed picture lines of `BOARD-ep02.md` only (no narration word changed), and this
round rebuilt the picture from them. The only code file touched is `ep02_residency_match.py`.

| Row | Beat | What the board now says | What the code now does |
|---|---|---|---|
| 1 | 2.3 | the dashed arrow under "sophomore" is `DashedLine((-2.4, 0.75), (-2.4, 1.5), color=YELLOW_D, stroke_width=5, dash_length=0.15).add_tip(tip_length=0.25)` | `self.soph = dashed(*SOPH, color=YELLOW_D, tip=True)` |
| 2 | 3.1 | H2 is the slot at x = -4 to the graduate at x = -2, H3 the slot at x = 4 to the graduate at x = 2, both `GREY_B` width 4 | the `H2`/`H3` constants take the board's new coordinates; `arrow(*H2, color=GREY_B)`, `arrow(*H3, color=GREY_B)` |
| 3 | 3.2 | the hospital she likes more is the free slot at x = 2; W is the white dashed arrow from (0.25, -1.95) to (1.75, -1.1) with a tip | `W_LINE` takes the new coordinates, `W_SLOT_IX = SLOT_X.index(2)`, `self.w_line = dashed(*W_LINE, color=WHITE, tip=True)`, and both the border cue and the flash of beat 3.3 use `self.slots[W_SLOT_IX]` |
| 4 | 3.3 | H1 turns `GREEN_C` and grows to stroke width 8 and is flashed once (`Indicate(H1, color=GREEN_C)`); back to `ORANGE` at width 4 on the next cue; the last cue flashes W and the slot at x = 2 | `self.h1.animate.set_color(GREEN_C).set_stroke(width=8)`, then `self.play(Indicate(self.h1, color=GREEN_C))`; `set_color(ORANGE).set_stroke(width=4)` on the next cue; `flash(self.w_line), flash(self.slots[W_SLOT_IX])` |
| 5 | 4.2 | `D` is a dashed line, `ORANGE`, width 5, dash length 0.15 | `self.d_line = dashed(*D_LINE, color=ORANGE)` |

Every dashed line of the episode now goes through one helper, `dashed(a, b, color, tip=False)`,
so the board's single style (width 5, dash length 0.15, a light colour) holds in all three
places. `add_tip` worked on a dashed line in this manim (0.21.0) for the vertical and the
slanted one alike, so the `Triangle` fallback of the board's rule was not needed. The one
flash of beat 3.3 is a `play()` of its own, next to the cue that turns H1 green; it is the
only timing this round adds.

Every scene method still ends with `self.hold()`; nothing but the heading is above y = 2.7 and
nothing is below y = -2.9 (the lowest points are the graduate circles at y = -2.55).

Checks of this round, one scene at a time, never two at once (all `--strict`, full lines in
`TRIAL_LOG-ep02.md`):

| command | result |
|---|---|
| `check.py cs70/note11 2 --strict --scenes race` | PASS (av 65.4 s / 62.5 s, longest silence 1.8 s, pace 163 wpm, 4 sheets; the end sheet shows the tipped dashed arrow under "sophomore" at frames 15-17) |
| `check.py cs70/note11 2 --strict --scenes fuse` | PASS (av 50.8 s / 48.2 s, longest silence 1.8 s, 4 sheets; the end sheets show H2/H3 grey without crossings, the white tipped dashed arrow W to the slot at x = 2, and H1 green at width 8) |
| `check.py cs70/note11 2 --strict --scenes match` | PASS (av 73.5 s / 71.7 s, longest silence 2.3 s, pace 155 wpm, 4 sheets; the end sheet shows the orange dashed line at width 5 and dash length 0.15) |
| `check.py cs70/note11 2 --strict` (whole episode) | PASS, 12 sheets, the table quoted above |
| `check.py cs70/note11 2 --strict --no-render` | PASS, the same table |

Sheets opened in this round: the `--scenes` end sheet01 of `race` (frames 9-12), the end
sheets 00 and 01 of `fuse` (frames 0-11), the end sheet00 of `match` (frames 0-8); then, from
the full run, `ep02_sheets_end/sheet01.png`, `sheet02.png`, `sheet03.png`, `sheet04.png` and
`ep02_sheets_mid/sheet01.png`, `sheet02.png`, `sheet03.png` (frames 9-17, 18-26, 27-35, 36-44).
Each of the five changes is in them and readable at that size; the frame lines of the two
tables above are the lines of the round-one run, corrected where this round changed what a
frame shows.

Not done in this round: nobody listened to the preview; the 1080p render did not run; the
narration, the BOARD, `series.py`, `manim_kit.py`, `tts.py` and everything in `K` are
untouched.
