"""Turn `L("中文短语", "English phrase")` cue helpers into translation-table entries.

While writing an episode, a cue is written once with both phrases:

    self.cue(L("但 CPU 并不认识 C", "But a CPU can't run C"), FadeIn(machine))

This script then rewrites each `L(zh, en)` to `tr(zh)` in the episode file and adds
`"zh": "en",` to the episode's table in i18n/epNN.py, which is where English lives (so
`i18n_check.py` is happy and the episode file keeps only Chinese). It first checks that
every English phrase really occurs in the English beat whose Chinese text contains the
Chinese phrase, which is the mistake that otherwise shows up as "[cue] phrase not in
the current line" at render time.

    python tools/cue_tables.py 2 5 8        # convert these episodes
    python tools/cue_tables.py 2 --check    # only verify, change nothing
"""

import argparse
import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "cs61c" / "riscv"


def load_series():
    ns = {}
    exec(compile((UNIT / "series.py").read_text(encoding="utf-8"), "series.py", "exec"), ns)
    return ns["EPISODES"]


def char_offset(text, lineno, col):
    """ast column offsets are UTF-8 bytes: convert to an index into `text`."""
    lines = text.split("\n")
    start = sum(len(l) + 1 for l in lines[:lineno - 1])
    return start + len(lines[lineno - 1].encode("utf-8")[:col].decode("utf-8"))


def find_calls(text):
    tree = ast.parse(text)
    out = []
    for n in ast.walk(tree):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "L"
                and len(n.args) == 2 and all(isinstance(a, ast.Constant) and isinstance(a.value, str)
                                             for a in n.args)):
            a, b = char_offset(text, n.lineno, n.col_offset), char_offset(text, n.end_lineno, n.end_col_offset)
            out.append((a, b, n.args[0].value, n.args[1].value, ast.get_source_segment(text, n.args[0])))
    return sorted(out)


def load_table(path):
    ns = {}
    exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), ns)
    return ns["EN"]


def verify(pairs, table):
    problems = []
    for zh, en in pairs:
        beats = [(k, v) for k, v in table.items() if zh in k]
        if not beats:
            problems.append(f"no source string contains the Chinese phrase {zh!r}")
        elif not any(en in v for _, v in beats):
            problems.append(f"{en!r} is not in the English of the beat containing {zh!r}")
        elif sum(v.count(en) for _, v in beats) > 1 and not any(v.count(en) == 1 for _, v in beats):
            print(f"  note: {en!r} occurs more than once; the cue uses the first", file=sys.stderr)
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episodes", nargs="+", type=int)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    eps = load_series()
    bad = False
    for n in a.episodes:
        e = eps[n - 1]
        src, tbl = UNIT / e["file"], UNIT / "i18n" / f"ep{n:02d}.py"
        text = src.read_text(encoding="utf-8")
        calls = find_calls(text)
        table = load_table(tbl)
        pairs, seen = [(c[2], c[3]) for c in calls], {}
        problems = verify(pairs, table)
        for zh, en in pairs:
            if seen.setdefault(zh, en) != en:
                problems.append(f"{zh!r} is used with two different English phrases")
            if zh in table and table[zh] != en:
                problems.append(f"{zh!r} is already a table key for {table[zh]!r} "
                                f"(a label or caption): pick a different Chinese phrase for the cue")
        if problems:
            bad = True
            print(f"episode {n}: {len(problems)} problem(s)")
            for p in problems:
                print("  -", p)
            continue
        if a.check or not calls:
            print(f"episode {n}: {len(calls)} L() cues ok" if calls else f"episode {n}: nothing to convert")
            continue
        for start, end, zh, en, zh_src in reversed(calls):
            text = text[:start] + f"tr({zh_src})" + text[end:]
        if "L(" not in text:
            text = text.replace("from beats import L  # noqa: E402\n", "")
        src.write_text(text, encoding="utf-8")
        t = tbl.read_text(encoding="utf-8").rstrip()
        assert t.endswith("}")
        add = [f"    {json.dumps(zh, ensure_ascii=False)}: {json.dumps(en, ensure_ascii=False)},"
               for zh, en in seen.items() if zh not in table]
        if add:
            t = t[:-1].rstrip() + "\n\n    # ---- cue phrases (Chinese phrase -> the words in the English beat)\n" \
                + "\n".join(add) + "\n}\n"
            tbl.write_text(t, encoding="utf-8")
        print(f"episode {n}: converted {len(calls)} cues, {len(add)} table entries added")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
