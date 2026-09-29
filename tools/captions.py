"""Print an episode's narration (every `self.say(...)` caption plus the end-card
bullets) in source order, Chinese next to English, for proofreading without
rendering anything.

Usage:
    python tools/captions.py 5          # episode 5
    python tools/captions.py            # all episodes
    python tools/captions.py 5 --out captions.md
"""

import argparse
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "cs61c" / "riscv"
sys.path.insert(0, str(SRC))
import series  # noqa: E402


def table(n):
    p = SRC / "i18n" / f"ep{n:02d}.py"
    if not p.exists():
        return {}
    ns = {}
    exec(compile(p.read_text(encoding="utf-8"), str(p), "exec"), ns)
    return ns.get("EN", {})


def narration(path, scene=None):
    """(kind, text) in source order; methods are visited in the order
    construct() calls them."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    cls = next((c for c in classes if c.name == scene), None) or next(
        c for c in classes if any(isinstance(f, ast.FunctionDef) and f.name == "construct" for f in c.body))
    methods = {f.name: f for f in cls.body if isinstance(f, ast.FunctionDef)}
    out, active = [], set()

    def visit(name):
        """say/end_card calls of a method, descending into the self.<method>()
        calls it makes, all in source order."""
        if name in active:
            return
        active.add(name)
        calls = sorted((n for n in ast.walk(methods[name]) if isinstance(n, ast.Call)
                        and isinstance(n.func, ast.Attribute)),
                       key=lambda c: (c.lineno, c.col_offset))
        for c in calls:
            attr = c.func.attr
            if (attr in methods and isinstance(c.func.value, ast.Name)
                    and c.func.value.id == "self"):
                visit(attr)
            elif attr == "say" and c.args:
                a = c.args[0]
                out.append(("say", a.value if isinstance(a, ast.Constant) else ast.unparse(a)))
            elif attr == "end_card" and c.args and isinstance(c.args[0], ast.List):
                out.extend(("end", e.value) for e in c.args[0].elts if isinstance(e, ast.Constant))
        active.discard(name)

    visit("construct")
    return out


def render(n):
    ep = series.SERIES[n - 1]
    path = SRC / ep.file
    lines = [f"## {n:02d} {ep.zh_title} / {ep.en_title}\n"]
    if not path.exists():
        return lines + ["(not written yet)\n"]
    en = table(n)
    k = 0
    for kind, zh in narration(path, ep.scene):
        if kind == "say":
            k += 1
        tag = "小结" if kind == "end" else f"{k}"
        lines.append(f"{tag}. {zh}")
        lines.append(f"    {en.get(zh, '<<MISSING>>')}")
    return lines + [""]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episodes", nargs="*", type=int)
    ap.add_argument("--out")
    a = ap.parse_args()
    eps = a.episodes or range(1, len(series.SERIES) + 1)
    text = "\n".join(line for n in eps for line in render(n))
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"wrote {a.out}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text)


if __name__ == "__main__":
    main()
