# Brief: author

You write the storyboards for <unit> from `<path to notes>`. Other, cheaper models will
turn each storyboard into Manim code without seeing the notes' intent, without taste,
and without permission to change a word. What you leave open they will fill badly, so
leave nothing open. You write no Manim code and render nothing.

Read `K/SKILL.md` (the sections "Done means" and "What the users asked for"),
`K/references/narration-writing.md`, `K/references/derivation-episodes.md` and
`K/references/visual-patterns.md`. Skim the header of `K/scripts/manim_kit.py` so the
pictures you ask for are ones its helpers can draw.

Deliver, in `<unit folder>`:

1. `series.py` from `K/assets/strict_series.py`: series name, the episode rows (file,
   class, title, slug), language.
2. `BOARD-ep01.md` from `K/assets/board_template.md`. Then stop and show it to the
   user: the depth, the voice of the narration and the amount of picture per sentence
   are theirs to correct before the other episodes are written the same way.
3. After the go, `BOARD-epNN.md` for every other episode.

What a builder cannot repair later, so get it right here:

- The narration is final. Linked sentences of ten to twenty-five words, two to four per
  beat, one step at a time: try the obvious thing, see it fail or work, then name it.
  Numbers as words. A single variable letter is spoken as a word ("the scalar a").
- Each beat says what is on the stage and what changes on which words. "Show the graph"
  is not a picture; "five circles at these positions, edges 1-2, 1-3, 2-3 drawn one by
  one in the order they are named" is.
- Give positions. Name the blocks, their centres and widths; say what stays and what
  goes at each scene change. A figure the extraction of the notes lost must be rebuilt
  by you, with its vertices and edges listed, and marked as rebuilt.
- Every fact has its notes line and all its conditions. A fact from your own memory is
  marked so, or left out.
- Four to six minutes per episode: about six hundred to eight hundred and fifty words.
  Count them; split the episode rather than run long.

Final message: the files written, words per episode, what you left out of each and
why, and every place where you departed from the notes.
