# Long derivation episodes: from a rough video to a lesson

Lessons from the Newton–Schulz episode (CS182): one 35-minute derivation in 14 scenes,
taken from a rough 14-minute "announce the result" video to a step-by-step lesson over
several rounds of user review. Read this when an episode is one long argument (a proof,
a design derivation, an analysis by cases) rather than a tour of facts, or when the user
says an existing video is too rough, too fast, or "just states things". §8 is what a
second review of the finished video found, and how those notes were handled.

## Contents
1. The story: derive, never announce
2. Explaining a hard step
3. Words first, then animation on the words
4. The script as an editable document
5. Fast review loop
6. Checks before you hand anything over
7. What it costs
8. Review notes on a finished video

## 1. The story: derive, never announce

The user's standard, confirmed over several rounds: **each sentence may only use what
the previous sentence just produced.**

- **Try, fail, try again, succeed, then name the pattern.** W·W does not even have
  matching shapes; WᵀW loses U; WWᵀW keeps U and Vᵀ; only now say "odd powers". The
  failures are content, not detours.
- **No spoilers.** Do not open a scene with "the rules of the game" or a list of tools.
  Introduce each operation at the moment it becomes the obvious next move. A name that
  an early scene mentions before a later scene derives it (the formula in the opening
  motivation) has to go: check the earlier scenes whenever a later one is rewritten as
  a derivation.
- **Derive conditions from the goal.** p(1) = 1 because the iteration has to settle at
  one; the second condition by plugging in 1 + e and reading off what must vanish. Not
  "we require".
- **No forward teasers** ("this will matter later") and no terms the viewer has not
  earned. Name a thing after the viewer has seen it ("call this the mirror rule").
- **Cases: easy first, by trying numbers.** Try a start, watch where it goes, try a
  bigger one, see the first failure, and only then ask why. The boundary values (√3,
  √5) come out of an explanation of what was just seen, not from a theorem.
- **The hard region: reduce the unknown to the known.** Start from the picture the
  viewer already has (the cobweb diagram). State the natural idea in plain words
  (every step shrinks the value, so it must fall into the region we already solved).
  Follow a few concrete starts and let the viewer see that their fates differ. Find
  what decides the fate (the number of sign flips), track it with one step of the map
  plus symmetry, and reduce each new interval to the previous one.
- **Close the argument.** After the method, check that it covers the whole region
  (do the stripes reach all the way to √5?) and say what happens exactly on the edges.
- **Overview last.** A summary picture (the colour strip of basins, the table of cases)
  comes after the cases have been earned, as the full view, and returns in the recap.
- **End where the episode began.** The last scene answers the opening question with the
  result (so what do we do with the matrix?).

## 2. Explaining a hard step

- **Compare the quantities themselves.** "Does the value shrink?" was first drawn as
  the curve against the auxiliary line y = −x. The user's correction: compare |p(x)|
  with |x| directly. Factor the map so the comparison is one visible number,
  |p(x)| = |x| · (x² − 3)/2, give that number a name on screen ("size factor"), check
  it on the starts already tried (0.5 at 2.0, 1.14 at 2.3), and get the boundary by
  setting it to one. Prefer the direct comparison to an auxiliary construction the
  viewer has to decode.
- **Separate what the viewer has to track.** Size and sign were tangled; splitting them
  (sizes follow the folded curve y = |p(x)|, the sign is just a flip count) made every
  later step a picture.
- **Arithmetic on screen, in steps.** 1.5 · 1.8 = 2.7, then 0.5 · 1.8³ = 2.92, then the
  difference. Three lines appearing one at a time, each when it is said.
- **Zoom when the picture is cramped**, and make the zoom a movement. A cut to a
  second, closer set of axes was read as a change of subject: the viewer could not tell
  which part of the old picture the new one was. Either move the camera
  (`zoom_to`), or frame the region with a box and let the box grow into the new axes
  (`visual-patterns.md` §8).
- **The step the user marks "explain closely" gets its own lines.** For p(b₁) = −√3 that
  meant saying why the size is rising on the whole interval (both factors grow), why it
  therefore crosses the level once, and why the sign is minus. Each is one line on
  screen and one sentence.
- **Write the argument down as it is spoken.** A proof told only through pictures
  ("the staircase has no gap") left the user saying the derivation was missing. The
  picture stays on the left; on the right the lines appear one by one: the claim, the
  recurrence, increasing, bounded, so it converges, the limit equation, the limit.
- **Name what is used without proof**, and keep that list as short as you can. After
  three passes one fact was left (an increasing sequence with an upper bound
  converges); continuity of the map, the norm identity and the non-square case each got
  one sentence instead of silence.
- All numbers computed and asserted in code, including the rounded forms the voice says.

## 3. Words first, then animation on the words

The sync rule, set by the user: **the text is the baseline and is always spoken in
full; the animation adapts.**

- `self.say(text, first_anims...)` starts the line; `self.cue("phrase from the line",
  anims...)` plays each further step when the voice reaches that phrase (its position in
  the text gives the time). One `cue` per thing the sentence mentions.
- Decide case by case when animation and words differ in length:
  - animation shorter → it waits for the words (`hold()`);
  - animation longer → shorten its `run_time`;
  - a pure demonstration (a 6-second zoom along the strip) → play it between two
    lines with no narration at all.
- A beat whose narration grew from 5 to 40 seconds with its old single animation is a
  frozen frame. After a script rewrite, list every beat whose word count at least
  doubled; each one needs its picture split into cues.
- Scenes that build on one stage (one graph through four scenes): keep the shared
  objects on `self`, and let a later scene be rendered alone by running the earlier
  ones through `self.fast_forward(...)`, which jumps every animation to its end state
  with no frames, voice or time.
- Subtitles appear one sentence at a time, on the frame and in the `.srt`. That
  project shipped a clean frame (`BURN_CAPTIONS = False` in series.py) with the `.srt`
  beside it; review previews always draw them on the frame.

## 4. The script as an editable document

- `narration.md` (via `scripts/narration.py`) holds every beat under a
  `### scene NN <!-- #hash -->` heading, with notes the renderer ignores: purpose of the
  scene, its logic chain, what the viewer knows and wants to ask next. The user edits
  wording there; `say()` swaps the text in when the hash matches the code.
- Script rounds are done in the document only: no code, and binding warnings do not
  block the writing. Record what the new words need from the picture under the scene's
  notes.
- When the words are final, rewrite the scene's code with `__Tnn__` tokens and run
  `scripts/bind_scene.py`: it pastes the beats in as literals, refuses to write if a
  `cue()` phrase is not in its beat, and rebinds the hashes. `narration.py check` should
  report 0 problems before any render.
- Do not run `narration.py sync` once the document has hand-written sections (story
  paragraph, viewer tables, revision log): it rebuilds the file from the code.
- Keep a revision log at the top of the document: length before and after per scene,
  which beats grew, what animation each needs, what is done. It is the task list.

## 5. Fast review loop

The user reviews by watching and listening. What they asked for, in order of weight:

1. **Voice and visible subtitles in every preview.** A silent clip with a separate
   subtitle file was unusable. Say exactly where the files are.
2. **Short waits.** One scene per process, in parallel (`scripts/preview.py 9 10 11
   --unit <unit>`, or `all --join`), 480p. A change to one scene costs one short render.
3. **A task list first, then step by step** when the job is large; report progress
   against the list.
4. Decide open details yourself (label positions, timing) and list them in the report;
   keep questions for things only the user can decide (total length, what to cut).

Each scene must render alone. preview.py sets `KIT_ONLY=<scene>`; the episode needs a
`SCENES` list and one line in `construct` naming the scenes that draw on a shared stage
(the earlier ones are fast-forwarded: end states only, no frames, voice or time):

```python
SCENES = ["motivation", "design", "graph", "slopes", "summary"]

def construct(self):
    if self.preview_only(["graph", "slopes"]):  # preview: no title or end card
        return
    self.title_card()
    for s in self.SCENES:
        getattr(self, s)()
    self.end_card([...])
```

## 6. Checks before you hand anything over

- `narration.py check`: 0 problems.
- Per scene, a contact sheet of about 12 frames: overlaps, labels on curves, anything in
  the caption band, formulas colliding with a corner formula that stays all episode.
- **Audio duration equals video duration for every scene** (`ffprobe`), and no long
  silence (`ffmpeg -af silencedetect=n=-45dB:d=9`). A lost voice track is invisible in
  frames; it happened here through Manim's cache (pitfalls.md).
- Re-check a scene's frames after every layout edit to it, and say in the report which
  scenes were not re-inspected and that the voice was not listened to, if so.

## 7. What it costs

- Turning "announce" into "derive" roughly triples the script: 14 minutes became about
  40 of narration (35 rendered). Tell the user the new length early and let them decide
  what to cut after watching, not before.
- First voiced render of new text takes minutes per scene (synthesis); later renders
  about one to two minutes per scene without the animation cache.
- A final 1080p render of 50 minutes in three parallel jobs took about 40 minutes.
  Changing the voice or its speed afterwards costs all of it again.

## 8. Review notes on a finished video

The user watched the 35-minute episode and wrote five lines: the fonts differ, the
animation does not zoom in at the key places or pick suitable points, why so fast, I
want a pleasant male voice, a derivation is missing (with a photo of their own
handwritten version). This is how such notes turn into work.

**Write the revision plan before touching anything.** For each note: the cause in the
code with file and line, the fix, the check. Terse notes hide concrete causes:

| The note | What it turned out to be | The fix |
|---|---|---|
| "fonts are inconsistent" | Three typefaces on one frame: LaTeX in formulas, Pango sans in labels, monospace on axis ticks; √3 written two ways | `TEXT_FONT = "latex"`; labels through `txt()`, numbers through `num()`; font sizes cut to three tiers |
| "no zoom at the key places, unsuitable points" | A scene class that cannot move its camera, so every "zoom" was a cut; example starts 2.2 and 2.23 drawn 0.03 apart | `zoom_to` at each crossing the argument rests on; box-grows-into-picture transitions; a magnified inset for the two close starts |
| "why so fast" | 168 to 180 words per minute, 0.35 s between beats, 200-word beats spoken in one breath, cues timed by estimate | `PACE`, paragraphs, a slower rate, exact cue times (`narration-writing.md` §7) |
| "a pleasant male voice" | The offline engine's default voice was female | `audition.py`, the user picks, `TTS` in series.py |
| "derivation missing" | The argument was there, but only as pictures and two formulas | Fourteen lines on screen, each with its sentence (§2) |

**Read a handwritten derivation critically.** The photo had a sign error in the first
line, the wrong limit in two places, "uniform" for "monotone", and an inequality the
wrong way round. List the corrections in the plan and ask the user to confirm them;
keep their notation only where it does not clash with the video's (their b* was the
video's b₁). Check every corrected claim numerically in the code with `assert`.

**Order of work**, set by the user when they rejected the first plan: new content goes
into the script first, code second.
1. Commit the current state as a baseline. Put the plan at the top of `narration.md` as
   a dated revision record.
2. Script only: the new beats, the recaps and cards of new episodes, and under each
   scene a note of what the picture must now show.
3. Voice and speed by ear (`audition.py`), while the script is being read.
4. Structure: split files, `series.py`, shared helpers in one module.
5. Pace, typeface, then the new derivation scenes, then the camera. One scene at a
   time with `preview.py`, frames inspected after each.
6. One final render; `pace.py`; update videos, `.srt`, README.
Work on the next step while the user is listening to the previous one. Ask before
deleting the superseded video; here the answer was to keep it.

**Splitting into episodes.** Once slower speech pushes a derivation past about 25
minutes, split it where the viewer has a new question, not by length: you could have
invented p (11 min) / where does one value go (19 min) / what happens in the gap
(23 min). Each episode ends by asking the next one's question and gives no answer. Each
later episode opens with a recap of two or three sentences that states only results,
and redraws what it needs (the graph, the one formula), because nothing is left on the
stage from before. Method names stay unique across the episode files so `narration.md`
and `preview.py` can address a scene by name.

**A last pass for rigour and clarity**, which the user asked for by name ("anything not
mathy enough, or not told clearly"). What it found:
- an approximation where the exact expression is just as short: p(1 + e) = 1 − 1.5e² − 0.5e³;
- "there is no tidy answer" where a closed form exists (b₁ as a sum of two cube roots);
- a number stated without its source (the factor 6 near √5 comes from p(√5 + e));
- a general claim with an exception that was never mentioned (a singular value of 0);
- a word used loosely (orthogonal, for a matrix that is not square);
- a limit taken through a function without saying the function is continuous;
- a "because" that was only an assertion ("so it has to settle somewhere").
Report these to the user as a short list with a proposed sentence for each, and add
them once approved.

**Say plainly what was not done.** The plan aimed at 120 to 125 words per minute; the
result was 135 to 150 after the user asked for a faster voice. The finished episodes
were inspected frame by frame per changed scene but not watched end to end. Both went
into the report.
