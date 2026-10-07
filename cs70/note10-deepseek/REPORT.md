# REPORT: The Seven Bridges of Königsberg — Eulerian tours

## Files

- Preview (480p, voiced): `C:\Users\18547\AppData\Local\Temp\kit_check\note10-deepseek\en\ep01\videos\ep01_konigsberg\480p15\Ep01Konigsberg.mp4`
- Subtitles: `C:\Users\18547\AppData\Local\Temp\kit_check\note10-deepseek\en\ep01\videos\ep01_konigsberg\480p15\Ep01Konigsberg.srt`
- Code: `cs70/note10-deepseek/ep01_konigsberg.py`, `cs70/note10-deepseek/series.py`,
  `cs70/note10-deepseek/PLAN.md`
- Sheets of the last full run: `...\kit_check\note10-deepseek\en\ep01_sheets_end\sheet00..03.png` and
  `...\ep01_sheets_mid\sheet00..03.png`

## Last check.py run

`PY K/scripts/check.py cs70/note10-deepseek 1 --strict --no-render`

```
== check: note10-deepseek episode 1 [en] ==
PASS code    13 say(), 24 cue()
PASS lint    clean
PASS render  C:\Users\18547\AppData\Local\Temp\kit_check\note10-deepseek\en\ep01\videos\ep01_konigsberg\480p15\Ep01Konigsberg.mp4
PASS log     clean
PASS av      video 253.5 s, audio 251.3 s, longest silence 3.3 s
PASS pace    35 subtitles, 164 words per minute
PASS sheets  8 sheets
PASS report  REPORT.md names all 8 sheets

RESULT: PASS. Not done yet:
  - open all 8 sheets above (frame number = subtitle number) and note per sheet what you saw: overlaps of text with shapes, leftovers, empty frames, a number that disagrees with its subtitle
  - listen to C:\Users\18547\AppData\Local\Temp\kit_check\note10-deepseek\en\ep01\videos\ep01_konigsberg\480p15\Ep01Konigsberg.mp4 from start to end, or say in the report that nobody did
report: C:\Users\18547\AppData\Local\Temp\kit_check\note10-deepseek\CHECK-ep01-en.md
```

The same command without `--no-render` (the full-episode render before it) had the table above with one
difference: `FAIL report  REPORT.md has no line for 6 of 8 sheets`, which is the expected first-run
failure of step 6.

## Frames

One line per sheet of the last full-episode run. Answers to the questions of step 5, in order:
1 text over a shape/curve/text · 2 cut off / on the subtitle · 3 leftover · 4 empty while it talks ·
5 number vs subtitle · 6 wrong count · 7 only sentences.

All lines below are from the last full run (8 sheets, 35 captions). Everything I saw was also checked
against single 480p frames and a few 3x zooms, because at contact-sheet size the two arcs of a doubled
bridge look like one line.

| Sheet | text over something | cut off / on subtitle | leftover | empty frame | wrong number | wrong count | only sentences | what I saw |
|---|---|---|---|---|---|---|---|---|
| ep01_sheets_end/sheet00.png | no | no | no | no | no | no | no | frames 0-8: the four lands, the seven bridges (frame 0 already has them all), the walk: the dot runs A-B-D-C-A-B-D and the six crossed bridges turn yellow while the B-C bridge stays blue; at the end "6 of 7 crossed" sits under the graph. The dot starts on A's rim, so the letter A is never covered. |
| ep01_sheets_end/sheet01.png | no | no | no | no | no | no | no | frames 9-17: the city blobs become the small graph; the degree numbers appear 5 then 3,3,3 next to their points (frame 11 shows "5" with its five lines, frame 12 the other three); the legend "degree = the lines at a point" fades in under the graph in frame 13; the pen dot appears on A's rim in frame 15. |
| ep01_sheets_end/sheet02.png | no | no | no | no | no | no | no | frames 18-26: two of A's lines turn green (arrival and departure) and the third turns red in frame 20; the four degree numbers flash red; "no tour" appears to the right of D in frame 22; frames 24-26 show the two-triangle graph with the lonely point at the bottom left. |
| ep01_sheets_end/sheet03.png | no | no | no | no | no | no | no | frames 27-35: degree numbers 2,2,4,2,2 and 0; the two condition lines on the right, clear of the graph; the dot walks 1-2-3, then 3-4-5-3, then 3-1, and in frames 33-35 all six lines are yellow and the dot is back at 1. |
| ep01_sheets_mid/sheet00.png | no | no | no | **the first mid frame shows the four lands only** | no | no | no | frames 0-8: frame 0 is caught between the land masses and the bridges, because the seven bridges are drawn on the cue "seven bridges" (about 2 s into a 6.4 s sentence); by the end of that caption all seven are there. Frames 3-5 show the walk in progress: one arc of each doubled pair is yellow, the other still blue; frame 5 has six yellow bridges and a blue B-C. Frame 8 is mid-Transform into the graph. |
| ep01_sheets_mid/sheet01.png | no | no | no | no | no | no | no | frames 9-17: mid-animation states of the same as end/sheet01: the "5" appears with the words "count the lines that touch it"; nothing hangs in the air. |
| ep01_sheets_mid/sheet02.png | no | no | no | no | no | no | no | frames 18-26: the red third line, the numbers flashing red, "no tour"; the twin graph is built node by node in frame 24 and its lines one after the other in 25-26. |
| ep01_sheets_mid/sheet03.png | no | no | no | no | no | no | no | frames 27-35: the condition lines appear on their words; the tour: frame 31 has the left triangle walked (two lines yellow, the dot at 3), frame 32 the right triangle; frames 33-35 carry the lightening of Indicate over the six lines and the two condition lines. |

## Numbers

| Shown or spoken | Computed by (name in FACTS) | The notes say | Same? |
|---|---|---|---|
| seven bridges, four pieces of land | `N_BRIDGES`, `N_LAND` | "two banks A and D and islands B and C", "seven bridges" (lines 17-21) | yes |
| the four degrees three, five, three, three | `DEG` from the multiset `BRIDGES` | "each point has an odd number of line segments incident to it" (line 41); E = {{A,B},{A,B},{A,C},{B,C},{B,D},{B,D},{C,D}} (line 53) | yes |
| six bridges crossed, one left over | `CROSSED`, `BRIDGES_LEFT` | not in the notes: this walk is mine, and it is asserted edge by edge against `WALK` | n/a (own example) |
| seventeen thirty six | `YEAR` | 1736 (line 34) | yes |
| degrees 2,2,4,2,2 and 0, six lines, the tour 1-2-3-4-5-3-1 | `DEG2`, `TWIN_EDGES`, `TOUR`, `TOUR_LEGS` | not in the notes: the notes give no worked Eulerian tour, so the "yes" example is mine (marked "own memory" in PLAN.md) | n/a (own example) |

No number in the episode disagrees with the notes.

## Not done

- Voice: not listened to by anyone (I cannot listen to audio). The voice and the pace were never judged
  by ear; only the `av` line (audio covers the video, no silence longer than 3.3 s) and the `pace` line
  (164 words per minute) were checked.
- Frames: all 8 contact sheets of the last full-episode run were inspected, plus hand-extracted 480p
  frames (PyAV, into a scratch folder under %TEMP%) and three 3x zooms to settle small details.
- Nothing was rendered without voice; `--no-voice` was never needed.
- The 1080p render (STRICT.md step 8) was **not** run: it waits for the user's go.
- A second language (strict step 8) was not asked for and not made.
- Out of scope and left for later episodes: the rest of Note 10 (complete graphs, trees, rooted trees,
  Theorem 10.2, planar graphs, Euler's formula, Theorem 10.3, Kuratowski, hypercubes, Theorem 10.5,
  practice problems, and the notes' own concept checks and exercises). See the coverage table in PLAN.md
  for the item-by-item list.

## Questions for the user

1. Is the voice and its speed right?
2. Shall the 1080p render run?
