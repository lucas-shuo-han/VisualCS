"""Lint a storyboard (BOARD-epNN.md) before any builder sees it.

Checks what a script can, so the author's own check is only about judgement:
  hole      a <...> placeholder left in
  design    the Design line missing or unfilled
  facts     no row in the Facts table
  beat      a beat without narration, over 60 words, or without "with the first word"
  cue       an `on "phrase"` that is not in its beat, or is there more than once
  still     a beat over 35 words with fewer than 2 changes, over 65 with fewer than 3
  uses      a beat without a "uses:" line
  + the narration lint (choppy, long, colon, numeral, voice) on the board's words

Usage:  python board_lint.py UNIT/BOARD-ep03.md [...]      exit 1 on any finding
"""

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from narration_lint import lint_episode  # noqa: E402


def parse(text: str):
    beats, cur = [], None
    for line in text.splitlines():
        if line.startswith("### "):
            cur = {"id": line[4:].strip(), "say": "", "first": False, "on": [], "changes": 0, "uses": False}
            beats.append(cur)
        elif line.startswith("## "):
            cur = None
        elif cur is not None:
            s = line.strip()
            if s.startswith(">"):
                cur["say"] += " " + s[1:].strip()
            elif s.startswith("- with the first word"):
                cur["first"] = True
                if not re.search(r"nothing new", s, re.I):
                    cur["changes"] += 1
            elif s.startswith("- on "):
                m = re.match(r'- on [“"](.+?)[”"]', s)
                if m:
                    cur["on"].append(m[1])
                cur["changes"] += 1
            elif s.startswith("- uses"):
                cur["uses"] = True
    for b in beats:
        b["say"] = " ".join(b["say"].split())
    return beats


def lint(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    out = []
    body = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    for m in re.finditer(r"<[^<>\n]{1,60}>", body):
        out.append(f"  hole    \"{m[0]}\" (line {body[:m.start()].count(chr(10)) + 1})")
    if not re.search(r"^Design.*question\s+\S", text, re.M | re.I):
        out.append("  design  no filled Design line (question, why care, obvious attempt, aha)")
    facts = re.search(r"^## Facts\n(.*?)(?=^## )", text, re.M | re.S)
    if not facts or len([l for l in facts[1].splitlines() if l.startswith("| F")]) == 0:
        out.append("  facts   the Facts table has no row")
    beats = parse(text)
    if not beats:
        return out + ["  beat    no `### id` beat"]
    for b in beats:
        n = len(b["say"].split())
        if not n:
            out.append(f"  beat    {b['id']}: no `> ` narration")
            continue
        if n > 60:
            out.append(f"  beat    {b['id']}: {n} words, over 60: split it")
        if not b["first"]:
            out.append(f"  beat    {b['id']}: no \"with the first word\" line")
        for p in b["on"]:
            k = b["say"].count(p)
            if k != 1:
                out.append(f"  cue     {b['id']}: \"{p}\" is {'not in' if k == 0 else f'{k} times in'} the beat")
        need = 3 if n > 65 else 2 if n > 35 else 1
        if b["changes"] < need:
            out.append(f"  still   {b['id']}: {n} words, {b['changes']} change(s), needs {need}")
        if not b["uses"]:
            out.append(f"  uses    {b['id']}: no \"uses:\" line")
    lines = [("say", b["say"], b["say"]) for b in beats if b["say"]]
    out += lint_episode(lines, "en", {}, Counter())
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    bad = 0
    for p in map(Path, sys.argv[1:]):
        found = lint(p)
        print(f"{'FAIL' if found else 'PASS'} {p.name}" + "".join("\n" + f for f in found))
        bad += bool(found)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
