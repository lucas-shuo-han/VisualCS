"""narration — edit the voice-over and the story logic in plain text.

`narration.md` (next to the episode) holds every caption/voice line, grouped by
scene, with free-form notes. Edit it, then render: manim_kit.say() swaps in the
text from the file. No Python needs to change.

Body vs notes (what the renderer reads / ignores):
    plain lines under a "###" heading   -> BODY: caption + voice-over text
    "speak: ..."                        -> how the voice says it (optional)
    lines starting with ">" or "//"     -> NOTES, never rendered
    <!-- ... -->  (one line)            -> NOTES, never rendered
    "## " scene headings and the intro  -> NOTES

Commands (run from the repo root with the venv python):
    narration.py check          validate the file (lengths, stale lines, empties)
    narration.py sync           rebuild/merge narration.md from the code + last dump
    KIT_NARRATION_DUMP=/tmp/d.jsonl  render ...   records the text each say() shows
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MD = Path(os.environ.get("KIT_NARRATION", HERE / "narration.md"))
SCRIPTS = sorted(HERE.glob("ep[0-9][0-9]_*.py"))
DUMP = os.environ.get("KIT_NARRATION_DUMP")
MAX_CAPTION = 105          # characters; longer captions wrap to three lines


def _burned() -> bool:
    """Are captions drawn on the frame? (series.py BURN_CAPTIONS / KIT_CAPTIONS)"""
    if os.environ.get("KIT_CAPTIONS"):
        return os.environ["KIT_CAPTIONS"] != "0"
    m = re.search(r"^BURN_CAPTIONS\s*=\s*(\w+)", (HERE / "series.py").read_text(encoding="utf-8")
                  if (HERE / "series.py").exists() else "", re.M)
    return not (m and m[1] == "False")
HEAD = re.compile(r"^### (\S+) (\d+)\s*<!-- #(\w+) -->\s*$")

_sites_cache: dict[str, list[dict]] = {}
_entries = None


# ------------------------------------------------------------------ code side
def _template(node):
    """Source text of the first argument of a say() call (f-strings as written)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        out = []
        for v in node.values:
            if isinstance(v, ast.Constant):
                out.append(str(v.value).replace("{", "{{").replace("}", "}}"))
            else:
                spec = ""
                if v.format_spec is not None:
                    spec = ":" + "".join(str(p.value) for p in v.format_spec.values
                                         if isinstance(p, ast.Constant))
                out.append("{" + ast.unparse(v.value) + spec + "}")
        return "".join(out)
    return None


def sites(path) -> list[dict]:
    """Every self.say(...) call in the episode class, in source order."""
    path = str(path)
    if path in _sites_cache:
        return _sites_cache[path]
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    out, count = [], {}
    for cls in [n for n in tree.body if isinstance(n, ast.ClassDef)]:
        for fn in [n for n in cls.body if isinstance(n, ast.FunctionDef)]:
            calls = [n for n in ast.walk(fn)
                     if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                     and n.func.attr == "say" and isinstance(n.func.value, ast.Name)
                     and n.func.value.id == "self" and n.args]
            for n in sorted(calls, key=lambda c: (c.lineno, c.col_offset)):
                tpl = _template(n.args[0])
                if tpl is None:
                    continue
                count[fn.name] = count.get(fn.name, 0) + 1
                speak = next((_template(k.value) for k in n.keywords if k.arg == "speak"), None)
                out.append(dict(
                    method=fn.name, n=count[fn.name], start=n.lineno, end=n.end_lineno,
                    template=tpl, speak=speak, hash=hashlib.sha1(tpl.encode()).hexdigest()[:6],
                    screen=[ast.unparse(a) for a in n.args[1:]]))
    _sites_cache[path] = out
    return out


def _site_at(filename, lineno):
    for s in sites(filename):
        if s["start"] <= lineno <= s["end"]:
            return s
    return None


# ------------------------------------------------------------------ md side
def parse(md_path=MD):
    """-> (scenes, entries). scenes: ordered {method: [header+intro lines]};
    entries: {(method, n): dict(hash, body, speak, notes)}."""
    scenes, entries = {}, {}
    if not Path(md_path).exists():
        return scenes, entries
    cur_scene, cur = None, None
    preamble = []
    for raw in Path(md_path).read_text(encoding="utf-8").splitlines():
        m = HEAD.match(raw)
        if m:
            cur = dict(method=m.group(1), n=int(m.group(2)), hash=m.group(3),
                       body=[], speak=None, notes=[])
            entries[(cur["method"], cur["n"])] = cur
            continue
        if raw.startswith("## "):
            cur = None
            cur_scene = re.sub(r"^## \d+ · (\S+).*$", r"\1", raw)
            scenes[cur_scene] = [raw]
            continue
        if cur is None:
            (scenes[cur_scene] if cur_scene else preamble).append(raw)
            continue
        s = raw.strip()
        if not s or s.startswith("<!--"):
            continue
        if s.startswith(">") or s.startswith("//"):
            cur["notes"].append(raw)
        elif s.lower().startswith("speak:"):
            cur["speak"] = s[6:].strip() or None
        else:
            cur["body"].append(s)
    scenes["__preamble__"] = preamble
    return scenes, entries


def _load():
    global _entries
    if _entries is None:
        _entries = parse()[1]
    return _entries


# ------------------------------------------------------------------ runtime
def apply(frame, text, speak):
    """Called by NarratedScene.say(): returns the (text, speak) to use."""
    s = _site_at(frame.f_code.co_filename, frame.f_lineno)
    if s is None:
        return text, speak
    if DUMP:
        with open(DUMP, "a", encoding="utf-8") as f:
            f.write(json.dumps(dict(method=s["method"], n=s["n"], hash=s["hash"],
                                    text=text, speak=speak), ensure_ascii=False) + "\n")
    e = _load().get((s["method"], s["n"]))
    if e is None or not e["body"]:
        return text, speak
    if e["hash"] != s["hash"]:
        print(f"[narration] {s['method']} {s['n']:02d}: code changed since the file was "
              f"synced; using the code's text (run narration.py sync)", file=sys.stderr)
        return text, speak
    return " ".join(e["body"]), e["speak"]


# ------------------------------------------------------------------ commands
def _dump_texts(dump_path):
    got = {}
    if dump_path and Path(dump_path).exists():
        for line in Path(dump_path).read_text(encoding="utf-8").splitlines():
            d = json.loads(line)
            got.setdefault((d["method"], d["n"]), d)
    return got


def sync(dump_path=None, titles=None):
    """Create narration.md from code + a dump of rendered text, or merge into it."""
    from narration_notes import INTRO, SCENES   # seed text for a fresh file
    ep = SCRIPTS[0]
    st = sites(ep)
    dumped = _dump_texts(dump_path)
    old_scenes, old = parse()
    order = []
    for s in st:
        if s["method"] not in order:
            order.append(s["method"])
    lines = list(old_scenes.get("__preamble__") or INTRO.splitlines())
    while lines and not lines[-1].strip():
        lines.pop()
    lines.append("")
    kept = set()
    for idx, meth in enumerate(order, 1):
        head = old_scenes.get(meth) or SCENES.get(meth, [f"## {idx} · {meth}"])[:]
        head = [re.sub(r"^## \d+ · ", f"## {idx:02d} · ", head[0])] + list(head[1:])
        lines += head
        while lines and not lines[-1].strip():
            lines.pop()
        lines.append("")
        for s in [x for x in st if x["method"] == meth]:
            key = (s["method"], s["n"])
            e = old.get(key)
            if e and e["hash"] == s["hash"] and e["body"]:
                body, speak, notes = e["body"], e["speak"], e["notes"]
                notes = [n for n in notes if not n.startswith("> screen:")]
            else:
                d = dumped.get(key)
                body = [d["text"] if d else s["template"]]
                speak = (d or {}).get("speak") or s["speak"]
                notes = []
            kept.add(key)
            lines.append(f"### {meth} {s['n']:02d} <!-- #{s['hash']} -->")
            lines += body
            if speak:
                lines.append(f"speak: {speak}")
            lines += notes
            if s["screen"]:
                scr = ", ".join(a.split("(")[0] for a in s["screen"])[:110]
                lines.append(f"> screen: {scr}")
            lines.append("")
    lost = [(k, e) for k, e in old.items() if k not in kept]
    if lost:
        lines += ["## Orphaned lines (their code changed; copy wording into the new lines)", ""]
        for k, e in lost:
            lines += [f"> {k[0]} {k[1]:02d}: " + " ".join(e["body"]), ""]
    MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {MD} ({len(kept)} lines, {len(lost)} orphaned)")


def check():
    st = {(s["method"], s["n"]): s for s in sites(SCRIPTS[0])}
    _, ents = parse()
    bad = 0
    words = 0
    for key, s in st.items():
        e = ents.get(key)
        if e is None:
            print(f"MISSING   {key[0]} {key[1]:02d}: not in narration.md (run sync)")
            bad += 1
            continue
        text = " ".join(e["body"])
        words += len(text.split())
        if e["hash"] != s["hash"]:
            print(f"STALE     {key[0]} {key[1]:02d}: code changed; the code's text will be used")
            bad += 1
        if not text:
            print(f"EMPTY     {key[0]} {key[1]:02d}")
            bad += 1
        if len(text) > MAX_CAPTION and _burned():   # .srt-only subtitles are split per sentence
            print(f"LONG      {key[0]} {key[1]:02d}: {len(text)} chars (max {MAX_CAPTION}): {text[:50]}...")
            bad += 1
        if re.search(r"[{}]", text):
            print(f"BRACES    {key[0]} {key[1]:02d}: unresolved {{}} in text")
            bad += 1
    extra = set(ents) - set(st)
    for k in sorted(extra):
        print(f"UNKNOWN   {k[0]} {k[1]:02d}: no such line in the code")
        bad += 1
    print(f"{len(st)} lines, ~{words} words (~{words / 2.5 / 60:.1f} min of speech at 150 wpm); "
          f"{bad} problem(s)")
    return bad


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "sync":
        sync(sys.argv[2] if len(sys.argv) > 2 else DUMP)
    else:
        sys.exit(1 if check() else 0)
