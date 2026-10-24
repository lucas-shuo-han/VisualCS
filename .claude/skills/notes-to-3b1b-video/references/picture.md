# Picture (author)

## Principles
- The picture makes each sentence true as it is said: one change per thing named.
- Build objects and change them; screen text only labels (≤ 4 words). Never bullet text, never words on an empty stage.
- Transform the old picture into the new one rather than clearing and starting over.
- Few objects, one focus, large. The thing a beat is about is the biggest, brightest thing on the frame.
- One colour per concept across the series; one typeface (LaTeX for math-heavy series); three sizes.

## Layout budget
Frame x −7.1…7.1, y −4…4. Heading top left (y ≈ 3.5); content y −2.9…3.3, x ±6.8; below −2.9 is the subtitle band. Two side-by-side blocks ≤ 6.3 wide each. Give blocks as centre + width, and say what stays and what goes at each scene change.

## Camera
- Move to where the argument lives: zoom on a crossing, a small region, a close pair. Up to ~3x reads as emphasis; beyond that, a box on the old picture grows into new axes. A move, never a cut.
- Values closer than a dot's width can't both be followed: an inset, or other values.
- Stop at the key point for a second.

## What the kit draws
Code listings with a moving line highlight and token circling; register columns; bit rows and bit fields; memory grids and stacks; neural-network diagrams with a passing flash; heatmaps; axes and plots with a moving tracker; LaTeX formulas split into parts that recolour or transform. Anything else is built from shapes, arrows and labels.

## Rejected by the builder's check, so don't ask for it
A highlight as a second rectangle (recolour the border); a line through text; two lines between the same two points (bend them apart); a words-only beat; a beat over 35 words with fewer than two changes, over 65 with fewer than three; anything below y = −2.9; boxes that only hold words (a slide); a text of seven or more words; over fifteen words on stage at once; a heading over six words. `render.py` refuses such an episode.
