"""bind_scene — put rewritten scene code into the episode with the script text taken from narration.md.

    python bind_scene.py NEWCODE START_MARKER END_MARKER scene[,scene...] [--unit DIR]

Use it when the words in narration.md are final and the animation of a scene is being
rewritten. NEWCODE is a file with the new `def <scene>(self):` methods, in which every
say() takes a token instead of a string:

        self.say(__T03__, FadeIn(calc))
        self.cue("Subtract, and the result is negative", FadeIn(result))

The code between the two markers in the episode file (comment lines that start the old
section and the next one) is replaced by NEWCODE, where

  * `__Tnn__` becomes beat nn of that scene from narration.md, as a string literal,
    so the words are never retyped (and never drift from the script);
  * every `self.cue("...")` phrase must occur in the beat it follows; if one does not,
    nothing is written and the phrases are listed (a cue whose phrase is missing would
    fire at once during the render);
  * the `### scene nn <!-- #hash -->` headings in narration.md and in
    narration/NN_scene.md are rebound to the new literals, so `narration.py check`
    stays clean without running `narration.py sync`.

Run from the unit folder (next to narration.py), or pass --unit.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import textwrap
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("newcode")
    ap.add_argument("start", help="text that begins the section to replace")
    ap.add_argument("end", help="text that begins the next section (kept)")
    ap.add_argument("scenes", help="comma-separated scene names whose tokens are filled in")
    ap.add_argument("--unit", default=".", help="unit folder (default: current directory)")
    a = ap.parse_args()
    here = Path(a.unit).resolve()
    scenes = a.scenes.split(",")
    sys.path.insert(0, str(here))
    import narration

    master = here / "narration.md"
    _, ents = narration.parse(master)
    ep = sorted(here.glob("ep[0-9][0-9]_*.py"))[0]
    raw = ep.read_bytes().decode("utf-8")
    crlf = "\r\n" in raw
    t = raw.replace("\r\n", "\n")

    code = Path(a.newcode).read_text(encoding="utf-8")
    hashes, out, bad = {}, [], 0
    for part in re.split(r"(?m)^(?=    def )", code):
        m = re.match(r"    def (\w+)\(", part)
        if m and m[1] in scenes:
            sc, cur = m[1], None
            for line in part.splitlines():
                tk = re.search(r"__T(\d\d)__", line)
                if tk:
                    cur = " ".join(ents[(sc, int(tk[1]))]["body"])
                for ph in re.findall(r'self\.cue\("([^"]+)"', line):
                    if cur is None or ph not in cur:
                        print(f"CUE NOT FOUND  {sc}: {ph!r}")
                        bad += 1

            def lit(mm, sc=sc):
                n = int(mm[1])
                body = " ".join(ents[(sc, n)]["body"])
                assert '"' not in body and "\\" not in body and "{" not in body, (sc, n)
                hashes[(sc, n)] = hashlib.sha1(body.encode()).hexdigest()[:6]
                chunks = textwrap.wrap(body, 92, break_long_words=False, drop_whitespace=False)
                assert "".join(chunks) == body
                return ("\n" + " " * 17).join(f'"{c}"' for c in chunks)

            part = re.sub(r"__T(\d\d)__", lit, part)
            want = {n for (s, n) in ents if s == sc}
            got = {n for (s, n) in hashes if s == sc}
            if want != got:
                sys.exit(f"{sc}: beats in narration.md and tokens in the code differ: {sorted(want ^ got)}")
        out.append(part)
    if bad:
        sys.exit(f"{bad} cue phrase(s) not in the script; nothing written")
    i = t.index(a.start)
    j = t.index(a.end, i + 1)
    t = t[:i] + "".join(out) + t[j:]
    ep.write_bytes((t.replace("\n", "\r\n") if crlf else t).encode("utf-8"))

    names = re.findall(r'"(\w+)"', re.search(r"SCENES = \[(.*?)\]", t, re.S)[1])
    for sc in scenes:
        for f in (master, here / "narration" / f"{names.index(sc) + 1:02d}_{sc}.md"):
            if not f.exists():
                continue
            r = f.read_bytes().decode("utf-8")
            for (s, n), h in hashes.items():
                if s == sc:
                    r, k = re.subn(rf"^(### {sc} {n:02d} <!-- #)\w+( -->)", rf"\g<1>{h}\g<2>", r, flags=re.M)
                    assert k == 1, (f.name, sc, n)
            f.write_bytes(r.encode("utf-8"))
    print("built", scenes)


if __name__ == "__main__":
    main()
