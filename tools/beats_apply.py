"""Regroup an episode's one-sentence `say()` calls into spoken beats.

The animation statements are never touched. For each beat you say which `say()` calls
(numbered in file order, see --list) form it and give the English text; the later
members' animations become `cue()` calls placed on a phrase of that English text.

    python tools/beats_apply.py 5 --list            # numbered say() calls and what follows each
    python tools/beats_apply.py 5 spec.py           # apply (writes the episode and i18n table)
    python tools/beats_apply.py 5 spec.py --dry     # show the result, change nothing

spec.py defines BEATS, a list of (members, english[, cues[, plays]]):

    BEATS = [
        ([1, 2], "English for the merged beat. Both sentences.",
                 {2: "Both sentences"}),                    # say #2's animation starts here
        ([3],    "A single say() with new English."),
        ([4, 5, 6], "...", {5: "phrase five", 6: ("中文短语", "phrase six")},
                           {5: [("中文短语", "phrase for the 1st play after say #5"), None]}),
    ]

- cues[member]: the member's animations run when the voice reaches that English phrase.
  For the first member this moves its animations out of say() onto a cue.
- plays[member]: the `self.play(...)` statements that follow the member (before the next
  say) become cues, in order; None leaves one as a plain play. Give (Chinese, English).
  A play with other keywords than run_time (rate_func ...) stays a play, with a
  `self.cue(phrase)` that only waits put in front of it.

- The Chinese of a beat is its members' Chinese joined (a trailing "……" / leading "……"
  pair becomes "，"; the Chinese is otherwise not edited).
- A cue maps to (Chinese phrase, English phrase). Give just the English phrase and the
  Chinese phrase is taken from the start of that member's own text; or give both.
- Members must be consecutive say() calls in one block; the statements between them
  stay where they are, except hold(), which is dropped (it would wait for the whole beat).
- say() calls not mentioned are left alone.
"""

import argparse
import ast
import difflib
import json
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import os
UNIT = Path(os.environ.get("BEATS_UNIT") or ROOT / "cs61c" / "riscv")
STOP = "，。；：！？、"


def load_series():
    ns = {}
    exec(compile((UNIT / "series.py").read_text(encoding="utf-8"), "series.py", "exec"), ns)
    return ns["EPISODES"]


def offsets(text):
    """(lineno, utf8 col) -> char index."""
    lines = text.split("\n")
    starts, pos = [], 0
    for l in lines:
        starts.append(pos)
        pos += len(l) + 1

    def f(lineno, col):
        return starts[lineno - 1] + len(lines[lineno - 1].encode("utf-8")[:col].decode("utf-8"))
    return f


class Say:
    def __init__(self, stmt, text, body, idx, method):
        self.stmt, self.text, self.body, self.idx, self.method = stmt, text, body, idx, method
        self.call = stmt.value


def find_says(tree):
    out = []

    def visit_body(body, method):
        for i, st in enumerate(body):
            if (isinstance(st, ast.Expr) and isinstance(st.value, ast.Call)
                    and isinstance(st.value.func, ast.Attribute) and st.value.func.attr == "say"
                    and isinstance(st.value.func.value, ast.Name) and st.value.func.value.id == "self"):
                a0 = st.value.args[0] if st.value.args else None
                text = a0.value if isinstance(a0, ast.Constant) and isinstance(a0.value, str) else None
                out.append(Say(st, text, body, i, method))
            for field in ("body", "orelse", "finalbody"):
                sub = getattr(st, field, None)
                if isinstance(sub, list) and sub and isinstance(sub[0], ast.stmt):
                    visit_body(sub, method)
    for cls in [n for n in tree.body if isinstance(n, ast.ClassDef)]:
        for fn in [n for n in cls.body if isinstance(n, ast.FunctionDef)]:
            visit_body(fn.body, fn.name)
    return sorted(out, key=lambda s: (s.stmt.lineno, s.stmt.col_offset))


def summarize(st):
    if isinstance(st, ast.Expr) and isinstance(st.value, ast.Call):
        f = st.value.func
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id == "self":
            return f.attr
    if isinstance(st, ast.Assign):
        return "assign"
    return type(st).__name__.lower()


def do_list(path):
    text = path.read_text(encoding="utf-8")
    says = find_says(ast.parse(text))
    for n, s in enumerate(says, 1):
        shown = s.text if s.text is not None else "[dynamic text]"
        anims = max(len(s.call.args) - 1, 0)
        nxt = []
        for st in s.body[s.idx + 1:]:
            k = summarize(st)
            if k == "say":
                break
            nxt.append(k)
        tail = (" -> " + ",".join(nxt)) if nxt else ""
        print(f"{n:3d} L{s.stmt.lineno:<4d} {s.method}: {shown}\n      anims={anims}{tail}")


def smooth(pieces):
    """Join Chinese pieces without editing them, except the '……' seams between members."""
    out = [pieces[0]]
    for p in pieces[1:]:
        prev = out[-1]
        if prev.endswith("……") and p.startswith("……"):
            out[-1], p = prev[:-2] + "，", p[2:]
        elif prev.endswith("……"):
            out[-1] = prev[:-2] + "，"
        elif p.startswith("……"):
            p = p[2:]
            if not prev.endswith(tuple("。！？；;，")):
                out[-1] = prev + "，"
        elif prev and prev[-1].isascii() and not prev[-1].isspace() and p and not p[0].isascii():
            out[-1] = prev + " "
        out.append(p)
    return out


def literal(s):
    return json.dumps(s, ensure_ascii=False)


def first_clause(piece, n=22):
    piece = piece.lstrip("…")
    cut = min([piece.find(c) for c in STOP if piece.find(c) > 0] + [len(piece)])
    return piece[:min(cut, n)]


def call_text(name, args, col):
    """name(args...) on one line when it fits, else one argument per line."""
    one = f"{name}(" + ", ".join(args) + ")"
    if "\n" not in one and col + len(one) <= 110:
        return one
    pad = " " * (col + len(name) + 1)
    return f"{name}(" + (",\n" + pad).join(args) + ")"


def seg(text, node):
    return ast.get_source_segment(text, node)


def build(text, says, spec, table):
    off = offsets(text)
    edits, new_entries, drop_keys = [], {}, set()
    problems = []

    def cue_phrase(zh, en, pieces_k, member, en_beat, zh_beat, c):
        zh_phrase, en_phrase = (c if isinstance(c, tuple) else (None, c))
        if zh_phrase is None:
            n = 22
            zh_phrase = first_clause(pieces_k, n)
            while zh_beat.count(zh_phrase) != 1 and n < 44:
                n += 4
                zh_phrase = first_clause(pieces_k, n)
        if zh_beat.count(zh_phrase) < 1:
            problems.append(f"cue Chinese phrase {zh_phrase!r} (say #{member}) is not in its beat")
        if en_beat.count(en_phrase) < 1:
            problems.append(f"cue English phrase {en_phrase!r} (say #{member}) is not in the English of its beat")
        if zh_phrase in table and table[zh_phrase] != en_phrase:
            problems.append(f"{zh_phrase!r} is already a table key ({table[zh_phrase]!r}); choose a longer Chinese phrase")
        if zh_phrase in new_entries and new_entries[zh_phrase] != en_phrase:
            problems.append(f"{zh_phrase!r} is used for two different English phrases")
        new_entries[zh_phrase] = en_phrase
        return zh_phrase

    def cue_call(g, zh_phrase, indent_col):
        canims = [seg(text, x) for x in g.call.args[1:]]
        ckw = [f"{x.arg}={seg(text, x.value)}" for x in g.call.keywords if x.arg == "run_time"]
        extra = [x.arg for x in g.call.keywords if x.arg != "run_time"]
        if extra:
            print(f"  note: a say() had {extra}, dropped (a cue takes only run_time)", file=sys.stderr)
        return call_text("self.cue", [f"tr({literal(zh_phrase)})"] + canims + ckw, indent_col)

    for item in spec:
        members, en = item[0], item[1]
        cues = item[2] if len(item) > 2 else {}
        plays = item[3] if len(item) > 3 else {}
        grp = [says[m - 1] for m in members]
        if len(set(id(g.body) for g in grp)) != 1 or any(
                grp[i + 1].idx < grp[i].idx for i in range(len(grp) - 1)):
            problems.append(f"beat {members}: members are not in one block, in order")
            continue
        if any(g.text is None for g in grp):
            problems.append(f"beat {members}: a member has non-literal text")
            continue
        pieces = smooth([g.text for g in grp])
        zh = "".join(pieces)
        for g in grp:
            if g.text != zh:
                drop_keys.add(g.text)
        new_entries[zh] = en
        first = grp[0]
        col = first.stmt.col_offset
        move_first = members[0] in cues and len(first.call.args) > 1
        a0 = first.call.args[0]
        t0, t1 = off(a0.lineno, a0.col_offset), off(a0.end_lineno, a0.end_col_offset)
        pad = " " * (t0 - (text.rfind("\n", 0, t0) + 1))
        lit = ("\n" + pad).join(literal(p) for p in pieces)
        if len(grp) == 1 and not move_first:
            pass   # a single say(): its Chinese stays as it is, only the English changes
        elif move_first:
            # the first member's animations wait for their phrase: keep only the text
            end = off(first.stmt.end_lineno, first.stmt.end_col_offset)
            zp = cue_phrase(zh, en, pieces[0], members[0], en, zh, cues[members[0]])
            edits.append((t0, end, lit + ")\n" + " " * col + cue_call(first, zp, col)))
        else:
            edits.append((t0, t1, lit))
        # a hold() between members would wait for the whole beat's voice: drop it
        for st in first.body[first.idx + 1:grp[-1].idx]:
            kind = summarize(st)
            if kind == "hold":
                la = text.rfind("\n", 0, off(st.lineno, st.col_offset)) + 1
                edits.append((la, text.find("\n", off(st.end_lineno, st.end_col_offset)) + 1, ""))
            elif kind == "clear_stage":
                problems.append(f"beat {members}: clear_stage() between the members (line {st.lineno}); "
                                f"split the beat there")
        for k, g in enumerate(grp[1:], 1):
            member = members[k]
            c = cues.get(member)
            a, b = off(g.stmt.lineno, g.stmt.col_offset), off(g.stmt.end_lineno, g.stmt.end_col_offset)
            if len(g.call.args) <= 1:
                if c:
                    problems.append(f"say #{member} has no animation, so its cue {c!r} does nothing")
                la = text.rfind("\n", 0, a) + 1
                lb = text.find("\n", b) + 1
                edits.append((la, lb, ""))
                continue
            if c is None:
                problems.append(f"say #{member} has animations: give it a cue phrase in the spec")
                continue
            zp = cue_phrase(zh, en, pieces[k], member, en, zh, c)
            edits.append((a, b, cue_call(g, zp, g.stmt.col_offset)))
        # self.play(...) statements after a member that should wait for a phrase
        for member, phrases in plays.items():
            g = says[member - 1]
            if g not in grp:
                continue
            after = []
            for st in g.body[g.idx + 1:]:
                if summarize(st) == "say":
                    break
                if summarize(st) == "play":
                    after.append(st)
            for st, ph in zip(after, phrases):
                if ph is None:
                    continue
                call_ = st.value
                bad = [x.arg for x in call_.keywords if x.arg != "run_time"]
                zp = cue_phrase(zh, en, "", member, en, zh, ph)
                a, b = off(st.lineno, st.col_offset), off(st.end_lineno, st.end_col_offset)
                if bad:   # rate_func etc.: keep the play, wait for the phrase in front of it
                    edits.append((a, a, f"self.cue(tr({literal(zp)}))\n" + " " * st.col_offset))
                    continue
                args = [f"tr({literal(zp)})"] + [seg(text, x) for x in call_.args] + \
                       [f"{x.arg}={seg(text, x.value)}" for x in call_.keywords]
                edits.append((a, b, call_text("self.cue", args, st.col_offset)))
            if len(phrases) > len(after):
                problems.append(f"say #{member}: {len(phrases)} play phrases but only {len(after)} plays follow it")
    return edits, new_entries, drop_keys, problems


def edit_table(path, new_entries, drop_keys):
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    d = next(n.value for n in tree.body if isinstance(n, ast.Assign)
             and any(getattr(t, "id", "") == "EN" for t in n.targets))
    lines = text.split("\n")
    kill = []
    for k, v in zip(d.keys, d.values):
        if isinstance(k, ast.Constant) and (k.value in drop_keys or k.value in new_entries):
            kill.append((k.lineno, v.end_lineno))
    for a, b in sorted(kill, reverse=True):
        del lines[a - 1:b]
    body = "\n".join(lines).rstrip()
    assert body.endswith("}")
    out = ["", "    # ---- spoken beats and cue phrases (see references/narration-writing.md)"]
    for zh, en in new_entries.items():
        wrapped = textwrap.wrap(en, 84, break_on_hyphens=False)
        if len(zh) + len(en) < 80 and len(wrapped) == 1:
            out.append(f"    {literal(zh)}: {literal(en)},")
        else:
            out.append(f"    {literal(zh)}:")
            for i, w in enumerate(wrapped):
                tail = " " if i < len(wrapped) - 1 else ""
                out.append(f"        {literal(w + tail)}" + ("," if i == len(wrapped) - 1 else ""))
    return body[:-1].rstrip() + "\n" + "\n".join(out) + "\n}\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode", type=int)
    ap.add_argument("spec", nargs="?")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    e = load_series()[a.episode - 1]
    src, tbl = UNIT / e["file"], UNIT / "i18n" / f"ep{a.episode:02d}.py"
    if a.list or not a.spec:
        return do_list(src)
    ns = {}
    exec(compile(Path(a.spec).read_text(encoding="utf-8"), a.spec, "exec"), ns)
    spec = ns["BEATS"]
    text = src.read_text(encoding="utf-8")
    tns = {}
    exec(compile(tbl.read_text(encoding="utf-8"), str(tbl), "exec"), tns)
    table = tns["EN"]
    says = find_says(ast.parse(text))
    edits, new_entries, drop_keys, problems = build(text, says, spec, table)
    if problems:
        print(f"episode {a.episode}: {len(problems)} problem(s), nothing written")
        for p in problems:
            print("  -", p)
        return 1
    new = text
    for s, t, r in sorted(edits, key=lambda x: -x[0]):
        new = new[:s] + r + new[t:]
    if "tr(" in new and not re.search(r"^from manim_kit import \*", new, re.M):
        print("  warning: manim_kit's tr() is needed", file=sys.stderr)
    ast.parse(new)
    new_tbl = edit_table(tbl, new_entries, drop_keys)
    ast.parse(new_tbl)
    if a.dry:
        sys.stdout.writelines(difflib.unified_diff(text.splitlines(True), new.splitlines(True), "old", "new", n=1))
        return 0
    src.write_text(new, encoding="utf-8")
    tbl.write_text(new_tbl, encoding="utf-8")
    cues = len(new_entries) - len([1 for it in spec if True])
    print(f"episode {a.episode}: {len(spec)} beats written; table: {len(new_entries)} entries "
          f"added, {len(drop_keys)} old sentence keys dropped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
