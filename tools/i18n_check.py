"""Check English translation coverage of the episodes.

Every string literal in an episode that contains Chinese must have an entry in
cs61c/riscv/i18n/epNN.py:

    EN = {
        "中文原文": "English text",
        ...
    }

Usage:
    python tools/i18n_check.py                # report on all episodes
    python tools/i18n_check.py 5 9            # only these episodes
    python tools/i18n_check.py 5 --skeleton   # print missing entries, ready to paste
    python tools/i18n_check.py 5 --widths     # entries whose English is much wider

Exits non-zero if anything is missing. f-strings containing Chinese are listed
as warnings: their runtime value can't be checked statically, so give the
table an entry for each value they produce (the render fails loudly if not).
"""

import argparse
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "cs61c" / "riscv"
sys.path.insert(0, str(SRC))
import series  # noqa: E402

NEEDS_TR = re.compile(r"[　-〿㐀-鿿＀-￯]")


def units(s):
    return max(len(line) and sum(1.0 if ord(c) > 0x2E7F else 0.55 for c in line)
               for line in s.split("\n"))


def literals(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    docs = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
                docs.add(id(first.value))
    found, dynamic, in_fstr = [], [], set()
    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            parts = [v.value for v in node.values if isinstance(v, ast.Constant)]
            in_fstr.update(id(v) for v in node.values)
            if any(NEEDS_TR.search(p) for p in parts):
                dynamic.append((node.lineno, ast.unparse(node)))
    for node in ast.walk(tree):
        if (isinstance(node, ast.Constant) and isinstance(node.value, str)
                and id(node) not in docs and id(node) not in in_fstr
                and NEEDS_TR.search(node.value)):
            found.append((node.lineno, node.value))
    seen, out = set(), []
    for ln, s in sorted(found):
        if s not in seen:
            seen.add(s)
            out.append((ln, s))
    return out, dynamic


def load(n):
    p = SRC / "i18n" / f"ep{n:02d}.py"
    if not p.exists():
        return None, p
    ns = {}
    exec(compile(p.read_text(encoding="utf-8"), str(p), "exec"), ns)
    return ns.get("EN", {}), p


def check(n, skeleton=False, widths=False):
    ep = series.SERIES[n - 1]
    path = SRC / ep.file
    if not path.exists():
        print(f"ep{n:02d}: {ep.file} does not exist yet")
        return True
    strings, dynamic = literals(path)
    table, tpath = load(n)
    table = table or {}
    missing = [(ln, s) for ln, s in strings if s not in table]
    bad = [(k, v) for k, v in table.items() if not isinstance(v, str) or NEEDS_TR.search(v)]
    used = {s for _, s in strings}
    unused = [k for k in table if k not in used]
    ok = not missing and not bad
    status = "ok" if ok else "INCOMPLETE"
    print(f"ep{n:02d} {ep.file}: {len(strings)} strings, {len(missing)} missing, "
          f"{len(bad)} bad values, {len(unused)} unused/dynamic entries -> {status}")
    for ln, s in missing:
        print(f"   missing  line {ln}: {s!r}")
    for k, v in bad:
        print(f"   bad      {k!r}: {v!r}")
    for ln, s in dynamic:
        print(f"   f-string line {ln}: {s}  (add an entry per runtime value)")
    if unused and not skeleton:
        for k in unused:
            print(f"   unused?  {k!r}")
    if widths:
        rows = []
        for k, v in table.items():
            if isinstance(v, str) and k in used:
                rows.append((units(v) / max(units(k), 1), k, v))
        for r, k, v in sorted(rows, reverse=True)[:25]:
            if r > 1.3:
                print(f"   x{r:.2f}  {k!r}\n          -> {v!r}")
    if skeleton and missing:
        print(f"\n# ---- paste into {tpath.relative_to(ROOT)} ----")
        for _, s in missing:
            print(f"    {s!r}: \"\",")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episodes", nargs="*", type=int)
    ap.add_argument("--skeleton", action="store_true")
    ap.add_argument("--widths", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")   # the Windows console default (gbk) can't print everything
    eps = a.episodes or range(1, len(series.SERIES) + 1)
    ok = all([check(n, a.skeleton, a.widths) for n in eps])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
