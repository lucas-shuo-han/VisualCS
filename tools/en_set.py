"""Change English values in an episode's translation table without touching the keys.

    python tools/en_set.py 2 values.py       # values.py defines VALUES = {"中文 key": "new English", ...}

Used to rewrite end-card bullets and labels so they can be read aloud (no colons,
numerals as words). Keys that are not in the table are reported and nothing is written.
"""

import ast
import os
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT = Path(os.environ.get("BEATS_UNIT") or ROOT / "cs61c" / "riscv")


def literal(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def set_values(path, values):
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    d = next(n.value for n in tree.body if isinstance(n, ast.Assign)
             and any(getattr(t, "id", "") == "EN" for t in n.targets))
    lines = text.split("\n")
    todo = dict(values)
    edits = []
    for k, v in zip(d.keys, d.values):
        if isinstance(k, ast.Constant) and k.value in todo:
            en = todo.pop(k.value)
            indent = " " * k.col_offset
            if len(k.value) + len(en) < 76 and "\n" not in en:
                new = [f"{indent}{literal(k.value)}: {literal(en)},"]
            else:
                wrapped = textwrap.wrap(en, 84, break_on_hyphens=False)
                new = [f"{indent}{literal(k.value)}:"]
                for i, w in enumerate(wrapped):
                    tail = " " if i < len(wrapped) - 1 else ""
                    new.append(f"{indent}    {literal(w + tail)}" + ("," if i == len(wrapped) - 1 else ""))
            edits.append((k.lineno, v.end_lineno, new))
    if todo:
        return [f"not in the table: {zh!r}" for zh in todo]
    for a, b, new in sorted(edits, reverse=True):
        lines[a - 1:b] = new
    out = "\n".join(lines)
    ast.parse(out)
    path.write_text(out, encoding="utf-8")
    return []


def main():
    n, spec = int(sys.argv[1]), sys.argv[2]
    ns = {}
    exec(compile(Path(spec).read_text(encoding="utf-8"), spec, "exec"), ns)
    bad = set_values(UNIT / "i18n" / f"ep{n:02d}.py", ns["VALUES"])
    for b in bad:
        print("  -", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
