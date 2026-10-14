# Brief: reviewer

Judge the preview of episode <N> against its board. Read `<unit>/BOARD-ep<NN>.md`, every sheet in `<media>/en/ep<NN>_sheets_end/` (frame = last moment of the numbered subtitle) and the `.srt`. `_mid` sheets only for a doubtful beat. Change no file but your review.

Per beat:
1. Is everything the stage line asks for there, where it says?
2. Did each change happen by its phrase's frame?
3. Can a viewer tell from the frame what the subtitle is about? Is the named thing where the eye lands?
4. Anything that should be gone, covering, cut off, or under the subtitle?
5. Counts and numbers match the subtitle?
6. Crowded, lopsided, or mostly empty?

Write `<unit>/REVIEW-ep<NN>.md`: one row per finding — frame, beat, what's wrong, the concrete change ("move 'V2' above the box, it touches edge 3-4"). Mark `builder` (code departs from board, or layout) or `author` (the board asks for something that fails on screen). Last line: `ready` or `not ready`. Can't write the file → return its text.

Don't report: a change one subtitle early/late inside one sentence, flashes, things that are fine, taste the board didn't ask for. A change a whole sentence early, or a scene change before its last sentence ends, is a finding. Say you cannot hear the voice.
