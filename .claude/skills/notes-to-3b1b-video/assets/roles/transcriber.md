# Brief: transcriber

Transcribe PDF pages <A>–<B> of `<unit>/notes` into `<unit>/notes/<output file>`. These notes are the source of everything downstream: be exact, not brief.

Read only: the page images `<unit>/notes/pages/<stem>-pNNN.png` for your pages, and their text layers `<unit>/notes/.text/<stem>-pNNN.txt` as a spelling aid (they lose math, tables and reading order; the image wins).

Per page, in order:
- First line `<!-- page N -->`, then `![page N](pages/<stem>-pNNN.png)`.
- All text, word for word, in reading order; headings as `#`, lists as lists. Drop running headers, footers and page numbers.
- Math in LaTeX (`$...$`, `$$...$$`), exactly as printed.
- Tables as Markdown tables.
- Each figure: `**Figure:** <what it shows: every labelled part, every number, arrows and what they connect>` (the author redraws figures from this and the page image).
- Code as fenced code blocks.
- Anything you cannot read: `[unclear: best guess]`. Never fill a gap from your own knowledge.

Write only your output file. Final message: one line, the file and its page count, and how many `[unclear]` marks it has.
