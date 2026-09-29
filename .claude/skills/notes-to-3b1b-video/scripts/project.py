"""Helpers shared by the scripts: read a unit folder (series.py, episodes,
translation tables) without importing Manim.

A unit folder holds manim_kit.py, tts.py, the episode files epNN_*.py, an
optional series.py (order, titles, languages) and optional i18n/epNN.py tables.
Without series.py, episodes are discovered from `class EpNN...` and the
series is single-language (KIT_SOURCE_LANG, default "en").
"""

from __future__ import annotations

import ast
import os
import re
from pathlib import Path

SCENE_RE = re.compile(r"^class (Ep(\d+)\w*)\(", re.M)
CJK_RE = re.compile(r"[　-〿㐀-鿿＀-￯぀-ヿ가-힯]")
CJK_LANGS = {"zh", "ja", "ko"}


def _exec(path: Path) -> dict:
    ns: dict = {}
    if path.exists():
        exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), ns)
    return ns


class Unit:
    """Everything the scripts need to know about one unit folder."""

    def __init__(self, src):
        self.src = Path(src).resolve()
        ns = _exec(self.src / "series.py")
        self.has_series = "EPISODES" in ns
        self.source_lang = ns.get("SOURCE_LANG") or os.environ.get("KIT_SOURCE_LANG", "en")
        self.langs = list(ns.get("LANGS") or [self.source_lang])
        self.name = ns.get("SERIES_NAME", {})
        if self.has_series:
            self.episodes = [dict(e, num=i + 1) for i, e in enumerate(ns["EPISODES"])]
        else:
            self.episodes = []
            for f in sorted(self.src.glob("*.py")):
                if f.name in ("manim_kit.py", "tts.py", "say_as.py", "series.py"):
                    continue
                for m in SCENE_RE.finditer(f.read_text(encoding="utf-8")):
                    self.episodes.append({"file": f.name, "scene": m[1], "num": int(m[2])})
            self.episodes.sort(key=lambda e: e["num"])

    def episode(self, n: int) -> dict:
        for e in self.episodes:
            if e["num"] == n:
                return e
        raise SystemExit(f"no episode {n} in {self.src}")

    def select(self, nums) -> list[dict]:
        return [self.episode(n) for n in nums] if nums else list(self.episodes)

    def path(self, ep: dict) -> Path:
        return self.src / ep["file"]

    def slug(self, ep: dict, lang: str) -> str:
        s = ep.get("slug", {}).get(lang) if self.has_series else None
        return f"{ep['num']:02d}-{s}" if s else Path(ep["file"]).stem

    def table(self, n: int, lang: str) -> dict:
        """The translation table source-string -> `lang` for episode n."""
        if lang == self.source_lang:
            return {}
        return _exec(self.src / "i18n" / f"ep{n:02d}.py").get(lang.upper(), {})

    def needs_tr(self, s: str) -> bool:
        """Does `s` have to be translated? Reliable only for a CJK source
        language; for a Latin one any string with a word in it counts."""
        if self.source_lang in CJK_LANGS:
            return bool(CJK_RE.search(s))
        return bool(re.search(r"[A-Za-z]{2,}", s))


def narration(path: Path, scene: str | None = None):
    """(kind, text, speak) for each say()/end_card bullet, in the order the
    scene runs them: construct() is walked and self.<method>() calls are
    followed in source order. `text` is the literal, or the source code of a
    non-literal argument (f-strings)."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    classes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
    cls = next((c for c in classes if c.name == scene), None) or next(
        c for c in classes
        if any(isinstance(f, ast.FunctionDef) and f.name == "construct" for f in c.body))
    methods = {f.name: f for f in cls.body if isinstance(f, ast.FunctionDef)}
    out, active = [], set()

    def lit(a):
        return a.value if isinstance(a, ast.Constant) else ast.unparse(a)

    def visit(name):
        if name in active or name not in methods:
            return
        active.add(name)
        calls = sorted((n for n in ast.walk(methods[name]) if isinstance(n, ast.Call)
                        and isinstance(n.func, ast.Attribute)),
                       key=lambda c: (c.lineno, c.col_offset))
        for c in calls:
            attr = c.func.attr
            if attr in methods and isinstance(c.func.value, ast.Name) and c.func.value.id == "self":
                visit(attr)
            elif attr == "say" and c.args:
                speak = next((lit(k.value) for k in c.keywords if k.arg == "speak"), None)
                out.append(("say", lit(c.args[0]), speak))
            elif attr == "end_card" and c.args and isinstance(c.args[0], ast.List):
                out.extend(("end", lit(e), None) for e in c.args[0].elts)
        active.discard(name)

    visit("construct")
    return out


def literals(path: Path, needs_tr):
    """String literals needing translation (line, text), and f-strings that
    contain such text (line, source) -- those need one entry per value."""
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
            if any(needs_tr(p) for p in parts):
                dynamic.append((node.lineno, ast.unparse(node)))
    for node in ast.walk(tree):
        if (isinstance(node, ast.Constant) and isinstance(node.value, str)
                and id(node) not in docs and id(node) not in in_fstr and needs_tr(node.value)):
            found.append((node.lineno, node.value))
    seen, out = set(), []
    for ln, s in sorted(found):
        if s not in seen:
            seen.add(s)
            out.append((ln, s))
    return out, dynamic


def find_manim() -> str:
    """The manim executable: a local virtualenv first, then PATH."""
    import shutil
    for cand in (".venv/Scripts/manim.exe", ".venv/bin/manim"):
        if Path(cand).exists():
            return str(Path(cand).resolve())
    return shutil.which("manim") or "manim"
