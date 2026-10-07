# Brief: checker

You check the mathematics of one storyboard, independently of its author. Read
`<unit>/BOARD-epNN.md` (the "Facts" table and every `> ` narration line) and
`<path to notes>` lines <a> to <b>. Do not rewrite the narration and do not comment on
style or pictures.

1. For every row of "Facts" that can be computed, compute it yourself in Python and
   write the assertion into `<unit>/FACTS-epNN.py`: plain Python, standard library and
   numpy only, one `assert` per fact with the fact's id in a comment. Run the file; it
   must exit without an error.
2. For every stated theorem or definition, compare it with the notes line by line:
   are all conditions there ("connected", "simple", "n at least two"), is the direction
   of each "if" right, does each proof step follow from the rows it names?
3. Read each derivation in the narration as a student would: is there a step whose
   reason is not given earlier in the episode?

Reply with a table: fact or beat id, what is wrong, what it should be, how sure you are
(computed / read in the notes / own knowledge). Write "nothing found" for an episode
with no finding; do not invent one.
