# Brief: verifier

Check that requested fixes are visible in the frames of episode <N> of `<unit>`. Change no file; reply in text.

1. `<unit>/REVIEW-ep<NN>.md`: each row is a requested fix (it wins over the board).
2. `<unit>/BOARD-ep<NN>.md` for the beats named.
3. The `.srt` next to the preview: subtitle K is frame K−1.
4. Every `sheetNN.png` in `<media>/<lang>/ep<NN>_sheets_end/`: nine frames each, red top-left number is a label; a frame is its subtitle's last moment.

Per row: FIXED / NOT FIXED / CANNOT TELL, the frame, and one sentence of what is there (text, colour, larger or smaller than nearby text, touching anything, where an arrow ends). No exact sizes. Flashes and anything not on the frames: CANNOT TELL; never guess.

Then anything clearly broken on any frame (text on text, cut off, covered, empty while talking), or "none". No style comments.

Final message: the table, the other breakages, sheets opened.
