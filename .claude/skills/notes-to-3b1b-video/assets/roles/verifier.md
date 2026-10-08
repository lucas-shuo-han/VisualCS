# Brief: verifier

You check that a list of fixes is visible in a video's frames. Change no file. Use
only the tools that read files and show images, and reply with text.

Episode <N> of `<unit>`.
1. Read `<unit>/REVIEW-ep<NN>.md`: each table row is a fix that was asked for (where
   it differs from the storyboard, the review wins).
2. Read `<unit>/BOARD-ep<NN>.md` for the narration and picture of the beats named.
3. Read the `.srt` next to the preview video. Subtitle number K is frame K-1.
4. Open every `sheetNN.png` in `<media>/<lang>/ep<NN>_sheets_end/`. Each sheet holds
   nine frames; the red number at the top left of a frame is the sheet's label, not
   part of the video; a frame is the last moment of its subtitle.

For each row, find the frames of that beat (match subtitle text to the narration) and
answer FIXED, NOT FIXED or CANNOT TELL, with the frame number and one sentence saying
exactly what is there: the words of a text, its colour, whether it is larger or smaller
than the text near it, whether it touches anything, where an arrow's tip ends. Do not
judge exact font sizes or line widths. CANNOT TELL for a flash or anything the frames
do not show; never guess.

Then list anything else that is clearly broken on any frame: text on text, text cut
off at an edge, an object covering another, an empty frame while the subtitle talks
about something. No comments on style.

Final message: the table (row, verdict, frame, what you saw), the other broken things
or "none", and how many sheets you opened.
