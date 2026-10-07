"""One command that says whether an episode is ready to be looked at.

    python check.py UNIT N                      lint, voiced 480p preview, every check, contact sheets
    python check.py UNIT N --scenes hook rule   only these scene methods (needs SCENES + preview_only)
    python check.py UNIT N --lang en            one language of a bilingual unit (default: the source)
    python check.py UNIT N --no-render          check the preview that is already there again
    python check.py UNIT N --no-voice           silent preview (no network; timing is estimated)
    python check.py UNIT N --strict             the strict edition's gate (STRICT.md): fewer warnings, more FAILs

Stages, in order. A FAIL in a cheap stage stops before the expensive one (--keep-going: run all).

  code      the episode parses; SCENES + preview_only; it ends with end_card(); numbers are asserted
  lint      narration_lint.py: choppy, split, long, colon, numeral, cue   (voice terms: WARN)
  board     when the unit has BOARD-epNN.md (PIPELINE.md): every say() is a beat of it, word for word
  i18n      i18n_check.py, when the unit has more than one language
  render    render.py --preview --voice, from a folder on the system drive
  log       [cue] [narration] [layout] [still] lines the kit wrote while rendering
  av        an audio stream; audio as long as the video; no silence over 9 s
  pace      words per minute from the .srt (120 to 165 is the range users accepted)
  sheets    contact sheets (end and mid of every subtitle) for you to open

Exit code 0 only when nothing FAILs. The same report is written to <media>/CHECK-epNN-<lang>.md;
quote it in the final message. What no script can decide stays with you and is listed at
the end: open the sheets, and say whether anyone listened to the voice.
"""
from __future__ import annotations

import argparse
import ast
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from pace import cues, words  # noqa: E402
from project import Unit, narration  # noqa: E402

LINT_FAIL = ("choppy", "split", "long", "colon", "numeral", "cue")
LOG_TAGS = ("[cue]", "[narration]", "[layout]", "[still]", "i18n: missing")
SOFT_TAGS = ("[empty]", "[textonly]")     # warnings, FAIL with --strict
FIX = {
    "code": "see each line; the episode template in assets/ shows the expected shape",
    "lint": "rewrite the beats named (references/narration-writing.md); never silence the linter by gluing sentences",
    "board": "copy each beat's `> ` text from the BOARD file into its say() unchanged; a wording you think is "
             "wrong goes into REPORT as a question for the author, not into the code",
    "i18n": "python i18n_check.py UNIT N --skeleton prints the missing entries",
    "render": "read the last lines of the log; fix the Python error; run again",
    "log": "[layout]: move the text named (next_to / shorter text); bend or offset one of two identical shapes. "
           "[still]: add cue() steps to that beat. [cue]: copy the phrase from the beat's text again. "
           "[narration]: give speak= one sentence per sentence. [textonly] / [empty]: draw the thing the beat "
           "talks about and keep it on stage",
    "report": "write the line for each sheet in REPORT.md (REPORT-epNN.md from the second episode on), "
              "then run again with --no-render",
    "av": "render again once; if the voice is still missing, check the network (edge-tts) or use KIT_TTS_ENGINE=kokoro",
    "pace": "change PACE / TTS['rate'] in series.py, not the words",
}


class Report:
    def __init__(self):
        self.rows = []

    def add(self, stage, status, summary, details=()):
        self.rows.append((stage, status, summary, list(details)))
        print(f"{status:4s} {stage:7s} {summary}", flush=True)
        for d in details[:40]:
            print(f"       {d}")
        if len(details) > 40:
            print(f"       ... and {len(details) - 40} more")

    @property
    def failed(self):
        return [r[0] for r in self.rows if r[1] == "FAIL"]

    def markdown(self, title, todo):
        out = [f"# {title}", "", "| stage | result | |", "|---|---|---|"]
        out += [f"| {s} | {st} | {sm} |" for s, st, sm, _ in self.rows]
        for s, st, _, det in self.rows:
            if det:
                out += ["", f"## {s} ({st})", "", "```", *det, "```"]
        out += ["", "## Left to a person or a model with eyes", "", *[f"- [ ] {t}" for t in todo]]
        return "\n".join(out) + "\n"


def code_stage(path: Path, scenes, strict=False):
    src = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return "FAIL", f"syntax error line {e.lineno}", [str(e)]
    fail, warn = [], []
    calls = {n.func.attr for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
    # construct() may live in a module the episodes of a unit share
    shared = "\n".join(f.read_text(encoding="utf-8") for f in path.parent.glob("*.py")
                       if f != path and f.name not in ("manim_kit.py", "tts.py") and not f.name.startswith("ep"))
    calls |= {x for x in ("end_card", "uncaption", "preview_only") if f".{x}(" in shared}
    src += shared
    if not {"end_card", "uncaption"} & calls:
        fail.append("no end_card(): the last subtitle never reaches the .srt")
    if "say" not in calls:
        fail.append("no say() call: the episode has no narration")
    has_scenes = bool(re.search(r"^\s*SCENES\s*=\s*\[", src, re.M)) and "preview_only" in calls
    if not has_scenes:
        (fail if scenes else warn).append("no `SCENES = [...]` + `if self.preview_only(...)`: scenes cannot render alone")
    if not any(isinstance(n, ast.Assert) for n in ast.walk(tree)):
        warn.append("no assert: compute every number shown in Python and assert the key ones")
    raw = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
           and n.func.id == "Text"]
    if raw:
        warn.append(f"Text(...) used directly on line(s) {raw[:8]}: use txt() / mono() (spacing, translation)")
    say_calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                 and n.func.attr == "say" and n.args]
    says = len(say_calls)
    loose = [n.lineno for n in say_calls
             if not (isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str))]
    if loose:
        warn.append(f"say() text on line(s) {loose[:8]} is not a plain string literal: the lint cannot read it")
    if strict:   # the strict edition has no warnings in this stage
        fail, warn = fail + warn, []
    cue_n = sum(1 for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == "cue")
    status = "FAIL" if fail else "WARN" if warn else "PASS"
    return status, f"{says} say(), {cue_n} cue()", [f"FAIL {x}" for x in fail] + [f"WARN {x}" for x in warn]


def lint_stage(unit_dir, n, lang):
    r = subprocess.run([sys.executable, str(HERE / "narration_lint.py"), str(unit_dir), str(n), "--lang", lang],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    if r.returncode != 0:
        return "FAIL", "narration_lint.py crashed", (r.stderr or r.stdout).strip().splitlines()[-6:]
    bad, voice, keep = [], [], False
    for line in r.stdout.splitlines():
        m = re.match(r"  (\w+) ", line)
        if m:
            keep = m[1] in LINT_FAIL
            (bad if keep else voice).append(line.strip())
        elif line.startswith("          ~") and not keep and voice:
            voice[-1] += "  " + line.strip()
    if bad:
        return "FAIL", f"{len(bad)} finding(s)", bad
    if voice:
        return "WARN", f"{len(voice)} term(s) the voice may misread: settle each in say_as.py or with speak=", voice
    return "PASS", "clean", []


def media_info(mp4: Path):
    """(video seconds, audio seconds or None, longest silence seconds, where it starts)."""
    import av
    import numpy as np
    with av.open(str(mp4)) as c:
        v = c.streams.video[0]
        vdur = float(v.duration * v.time_base) if v.duration else float(c.duration) / av.time_base
        if not c.streams.audio:
            return vdur, None, 0.0, 0.0
        rate = 8000
        rs = av.AudioResampler(format="s16", layout="mono", rate=rate)
        chunks = []
        for frame in c.decode(c.streams.audio[0]):
            for f in rs.resample(frame):
                chunks.append(f.to_ndarray().reshape(-1))
    x = np.concatenate(chunks).astype(np.float64) if chunks else np.zeros(1)
    win = rate // 10
    k = len(x) // win
    if k == 0:
        return vdur, len(x) / rate, 0.0, 0.0
    rms = np.sqrt((x[:k * win].reshape(k, win) ** 2).mean(axis=1)) / 32768
    quiet = rms < 10 ** (-45 / 20)
    best = start = run = 0
    for i, q in enumerate(quiet):
        run = run + 1 if q else 0
        if run > best:
            best, start = run, i - run + 1
    return vdur, len(x) / rate, best / 10, start / 10


def board_beats(path: Path):
    """(beat id, narration) of a storyboard: a `### id` heading, then its `> ` lines."""
    beats, bid = [], "?"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("### "):
            bid = line[4:].split()[0] if line[4:].split() else "?"
            beats.append([bid, ""])
        elif line.startswith(">") and beats:
            beats[-1][1] += " " + line[1:].strip()
    return [(b, " ".join(t.split())) for b, t in beats if t.strip()]


def board_stage(path: Path, said, whole: bool):
    """The say() texts are the storyboard's narration, word for word and in its order.
    While scenes are still missing (--scenes) the code may hold fewer beats, never others."""
    beats = board_beats(path)
    if not beats:
        return "FAIL", f"{path.name} has no `### id` beat with `> ` narration lines", []
    texts = [t for _, t in beats]
    bad, at = [], 0
    for s in said:
        s = " ".join(s.split())
        if s in texts[at:]:
            at = texts.index(s, at) + 1
        elif s in texts:
            bad.append(f"out of order (beat {beats[texts.index(s)][0]}): {s[:70]}")
        else:
            near = max(beats, key=lambda b: len(set(b[1].split()) & set(s.split())))
            bad.append(f"not the words of beat {near[0]}: {s[:70]}")
    if whole:
        have = {" ".join(s.split()) for s in said}
        bad += [f"beat {b} is not in the code: {t[:60]}" for b, t in beats if t not in have]
    if bad:
        return "FAIL", f"the narration differs from {path.name}", bad
    return "PASS", f"{len(said)} of {len(beats)} beats, word for word as in {path.name}", []


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("unit")
    ap.add_argument("episode", type=int)
    ap.add_argument("--lang", help="language to check (default: the source language)")
    ap.add_argument("--scenes", nargs="+", help="render only these scene methods")
    ap.add_argument("--no-render", action="store_true", help="reuse the preview in the media folder")
    ap.add_argument("--no-voice", action="store_true")
    ap.add_argument("--keep-going", action="store_true", help="run every stage even after a FAIL")
    ap.add_argument("--strict", action="store_true", help="the strict edition: warnings of the code stage and "
                    "[textonly] / [empty] findings FAIL; a full-episode run also wants REPORT.md")
    ap.add_argument("--media", help="scratch folder (default: a temp folder on the system drive)")
    ap.add_argument("--manim", help="manim executable (default: next to this python, then .venv, then PATH)")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    unit = Unit(a.unit)
    ep = unit.episode(a.episode)
    n, lang = ep["num"], a.lang or unit.source_lang
    media = Path(a.media).resolve() if a.media else Path(tempfile.gettempdir()) / "kit_check" / unit.src.name
    media.mkdir(parents=True, exist_ok=True)
    rep = Report()
    title = f"check: {unit.src.name} episode {n} [{lang}]" + (f" scenes {' '.join(a.scenes)}" if a.scenes else "")
    print(f"== {title} ==")
    todo = []

    def finish():
        failed = rep.failed
        out = media / f"CHECK-ep{n:02d}-{lang}.md"
        out.write_text(rep.markdown(title, todo), encoding="utf-8")
        print()
        if failed:
            print(f"RESULT: FAIL ({', '.join(failed)}). Fix the FAIL lines from the top, then run the same command.")
            for s in dict.fromkeys(failed):
                print(f"  how, {s}: {FIX[s]}")
        else:
            print("RESULT: PASS. Not done yet:")
            for t in todo:
                print(f"  - {t}")
        print(f"report: {out}")
        return 1 if failed else 0

    def stop():
        return rep.failed and not a.keep_going

    path = unit.path(ep)
    if not path.exists():
        rep.add("code", "FAIL", f"{path} does not exist")
        return finish()
    rep.add("code", *code_stage(path, a.scenes, a.strict))
    if stop():
        return finish()
    seen = [x for x in narration(path, ep["scene"]) if x[0] == "say"]
    if not seen:   # a clean lint of nothing is not a pass
        rep.add("lint", "FAIL", "the lint finds no say() beat: call the scene methods from construct() as "
                                "self.name() or through `for s in self.SCENES: getattr(self, s)()`")
    else:
        rep.add("lint", *lint_stage(unit.src, n, lang))
    board = next((p for p in (unit.src / f"BOARD-ep{n:02d}.md", unit.src / "BOARD.md") if p.exists()), None)
    if board and seen:   # the pipeline (PIPELINE.md): the words belong to the storyboard's author
        rep.add("board", *board_stage(board, [x[1] for x in seen], whole=not a.scenes))
    if len(unit.langs) > 1:
        r = subprocess.run([sys.executable, str(HERE / "i18n_check.py"), str(unit.src), str(n)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        lines = [x for x in r.stdout.splitlines() if x.startswith("   missing") or "INCOMPLETE" in x]
        rep.add("i18n", "PASS" if r.returncode == 0 else "FAIL", "tables complete" if r.returncode == 0
                else "missing translations", lines)
    if stop():
        return finish()

    voice = not a.no_voice
    log = media / lang / f"ep{n:02d}.log"
    if not a.no_render:
        py_dir = Path(sys.executable).parent
        manim = a.manim or next((str(p) for p in (py_dir / "manim.exe", py_dir / "manim") if p.exists()), None)
        env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
        env.setdefault("MANIM_CWD", str(media))                      # dvisvgm needs the system drive (Windows)
        env.setdefault("KIT_TTS_CACHE", str(unit.src / ".tts_cache"))  # one cache for previews and the final render
        if a.scenes:
            env["KIT_ONLY"] = ",".join(a.scenes)
        else:
            env.pop("KIT_ONLY", None)
        cmd = [sys.executable, str(HERE / "render.py"), str(unit.src), str(n), "--preview", "--lang", lang,
               "--voice" if voice else "--no-voice", "--media", str(media)] + (["--manim", manim] if manim else [])
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
        if r.returncode != 0 or "FAILED" in r.stdout:
            tail = log.read_text(encoding="utf-8", errors="replace").strip().splitlines()[-12:] if log.exists() else []
            rep.add("render", "FAIL", f"see {log}", tail or (r.stdout + r.stderr).strip().splitlines()[-8:])
            return finish()
    vids = sorted((media / lang / f"ep{n:02d}" / "videos").rglob(f"480p15/{ep['scene']}.mp4")) \
        if (media / lang / f"ep{n:02d}").exists() else []
    if not vids:
        rep.add("render", "FAIL", f"no preview under {media / lang}: run without --no-render")
        return finish()
    mp4 = vids[-1]
    srt = mp4.with_suffix(".srt")
    rep.add("render", "PASS", str(mp4))

    text = log.read_text(encoding="utf-8", errors="replace") if log.exists() else ""
    found = [x.strip() for x in text.splitlines() if x.strip().startswith(LOG_TAGS)]
    soft = [x.strip() for x in text.splitlines() if x.strip().startswith(SOFT_TAGS)]
    if a.strict:
        found, soft = found + soft, []
    found, soft = list(dict.fromkeys(found)), list(dict.fromkeys(soft))
    rep.add("log", "FAIL" if found else "WARN" if soft else "PASS",
            f"{len(found)} finding(s) from the kit" if found else f"{len(soft)} warning(s)" if soft else "clean",
            found + soft)

    vdur, adur, quiet, at = media_info(mp4)
    if not voice:
        rep.add("av", "WARN", f"video {vdur:.0f} s, rendered without voice: timing is only estimated")
    elif adur is None:
        rep.add("av", "FAIL", f"video {vdur:.0f} s has no audio stream")
    else:
        bad = []
        if adur < vdur - 6:
            bad.append(f"audio ends {vdur - adur:.0f} s before the video: voice lines were lost")
        if quiet > 9:
            bad.append(f"{quiet:.0f} s of silence from {int(at // 60)}:{at % 60:04.1f}")
        rep.add("av", "FAIL" if bad else "PASS", f"video {vdur:.1f} s, audio {adur:.1f} s, longest silence {quiet:.1f} s", bad)

    cs = cues(srt) if srt.exists() else []
    if not cs:
        rep.add("pace", "FAIL", "no subtitles in the .srt")
    else:
        wpm = sum(words(t) for _, _, t in cs) / cs[-1][1] * 60
        ok = 120 <= wpm <= 165 or bool(a.scenes)
        rep.add("pace", "PASS" if ok else "WARN", f"{len(cs)} subtitles, {wpm:.0f} words per minute"
                + ("" if ok else " (accepted range 120 to 165: adjust PACE / TTS rate in series.py)"))
        sheets = []
        for at_ in ("end", "mid"):
            out = media / lang / f"ep{n:02d}_sheets_{at_}"
            r = subprocess.run([sys.executable, str(HERE / "contact_sheet.py"), str(mp4), str(srt), str(out),
                                "--at", at_], capture_output=True, text=True, encoding="utf-8", errors="replace")
            if r.returncode != 0:
                rep.add("sheets", "FAIL", f"contact_sheet.py --at {at_} failed", r.stderr.strip().splitlines()[-4:])
                break
            sheets += sorted(out.glob("sheet*.png"))
        else:
            rep.add("sheets", "PASS", f"{len(sheets)} sheets", [str(s) for s in sheets])
            todo.append(f"open all {len(sheets)} sheets above (frame number = subtitle number) and note per sheet "
                        "what you saw: overlaps of text with shapes, leftovers, empty frames, a number that "
                        "disagrees with its subtitle")
    todo.append(f"listen to {mp4} from start to end, or say in the report that nobody did")
    if a.strict and not a.scenes and not rep.failed and cs:   # the frames were looked at: one line per sheet
        per_ep = unit.src / f"REPORT-ep{n:02d}.md"      # several episodes in one unit: one report each
        report = per_ep if per_ep.exists() else unit.src / "REPORT.md"
        body = report.read_text(encoding="utf-8", errors="replace") if report.exists() else ""
        want = [f"{s.parent.name}/{s.name}" for s in sheets]
        miss = [w for w in want if w not in body.replace(chr(92), "/")]
        if miss:
            name = report.name if report.exists() else f"REPORT.md (or {per_ep.name})"
            rep.add("report", "FAIL", f"{name} has no line for {len(miss)} of {len(want)} sheets", miss)
        else:
            rep.add("report", "PASS", f"{report.name} names all {len(want)} sheets")
    return finish()


if __name__ == "__main__":
    sys.exit(main())
