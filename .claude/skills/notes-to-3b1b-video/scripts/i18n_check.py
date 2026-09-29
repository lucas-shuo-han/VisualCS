"""Check the translation tables of a unit: every source-language string literal
in an episode must have an entry in i18n/epNN.py for every other language.

    # i18n/ep05.py
    EN = {"源字符串": "English", ...}      # one dict per target language

Usage:
    python i18n_check.py SRC                 # all episodes, all target languages
    python i18n_check.py SRC 5 --skeleton    # print the missing entries, ready to paste
    python i18n_check.py SRC 5 --widths      # entries much wider than their source (layout risk)

Exits non-zero if anything is missing. f-strings containing source text are
listed as warnings: give the table one entry per value they produce (with a
CJK source language, the render fails loudly on any miss).
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from project import Unit, literals  # noqa: E402


def units(s):
    return max((sum(1.0 if ord(c) > 0x2E7F else 0.55 for c in line) for line in s.split("\n")),
               default=0)


def check(unit, ep, lang, skeleton, widths):
    path = unit.path(ep)
    if not path.exists():
        print(f"ep{ep['num']:02d}: {ep['file']} does not exist yet")
        return True
    strings, dynamic = literals(path, unit.needs_tr)
    table = unit.table(ep["num"], lang)
    missing = [(ln, s) for ln, s in strings if s not in table]
    used = {s for _, s in strings}
    unused = [k for k in table if k not in used]
    ok = not missing
    print(f"ep{ep['num']:02d} [{lang}] {ep['file']}: {len(strings)} strings, {len(missing)} missing, "
          f"{len(unused)} unused/dynamic -> {'ok' if ok else 'INCOMPLETE'}")
    for ln, s in missing:
        print(f"   missing  line {ln}: {s!r}")
    for ln, s in dynamic:
        print(f"   f-string line {ln}: {s}  (add an entry per runtime value)")
    if not skeleton:
        for k in unused:
            print(f"   unused?  {k!r}")
    if widths:
        rows = sorted(((units(v) / max(units(k), 1), k, v) for k, v in table.items()
                       if isinstance(v, str) and k in used), reverse=True)
        for r, k, v in rows[:25]:
            if r > 1.3:
                print(f"   x{r:.2f}  {k!r}\n          -> {v!r}")
    if skeleton and missing:
        print(f"\n# ---- paste into i18n/ep{ep['num']:02d}.py, {lang.upper()} = {{...}} ----")
        for _, s in missing:
            print(f"    {s!r}: \"\",")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("episodes", nargs="*", type=int)
    ap.add_argument("--lang", default="all")
    ap.add_argument("--skeleton", action="store_true")
    ap.add_argument("--widths", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")   # a Windows console (gbk) can't print everything
    unit = Unit(a.src)
    targets = [lang for lang in (unit.langs if a.lang == "all" else [a.lang]) if lang != unit.source_lang]
    if not targets:
        print("single-language unit: nothing to check")
        return 0
    if unit.source_lang not in ("zh", "ja", "ko"):
        print(f"note: source language {unit.source_lang!r} is not CJK, so 'needs translation' is a "
              "guess (any string with a word in it); code and labels may show up as missing.")
    ok = all([check(unit, ep, lang, a.skeleton, a.widths)
              for ep in unit.select(a.episodes) for lang in targets])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
