# Brief: reviewer

You judge the preview of episode <N> against its storyboard. Read
`<unit>/BOARD-ep<NN>.md`, then open every contact sheet in
`<media>/en/ep<NN>_sheets_end/` (each frame is the last moment of the subtitle whose
number is printed on it) and the `.srt` next to the preview video. Open the `_mid`
sheets only for a beat you doubt. You change no file except your review.

For every beat of the storyboard, find its frames and answer:

1. Is everything the beat's stage line asks for on the frame, where it says?
2. Did each change happen by the frame of the phrase it belongs to?
3. Can a viewer who sees only this frame tell what the subtitle is talking about?
   Is the thing being named the thing the eye lands on (colour, size, position)?
4. Is anything on the frame that should be gone, or covering something else, or cut
   off, or under the subtitle?
5. If the subtitle counts or names a number, does the frame show exactly that?
6. Does the frame look crowded, lopsided, or mostly empty?

Write `<unit>/REVIEW-ep<NN>.md`: one row per finding with the frame number, the beat
id, what is wrong, and the change you want, concrete enough to do without judgement
("move the label 'V2' above the box, it touches the edge 3-4", not "tidy the labels").
Mark each row `builder` (the code departs from the board, or a layout fix) or `author`
(the board itself asks for something that does not work on screen). End with one line:
`ready` or `not ready`. If your tools refuse to create the file, return its full text.

What the sheets cannot show, so do not report it: a change that seems one subtitle
early or late inside one sentence (a sentence cut into several subtitles shares its
time by length, while the picture follows the spoken word), and a flash, which lasts
under a second. A change that is a whole sentence early, or a scene that changes
before its last sentence has ended, is a finding.

Do not list what is fine. Do not ask for changes of taste the board did not ask for.
You cannot hear the voice; say so.
