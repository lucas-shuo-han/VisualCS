"""A minimal tool-using agent loop against an Anthropic-compatible endpoint: runs a builder
(PIPELINE.md) on another provider's model. The key comes from --key-file (a file outside
the repository) or the environment (AGENT_KEY); it is never logged or passed to a tool.

    python agent_loop.py --base https://api.deepseek.com/anthropic --model <model> \
        --key-file ~/.deepseek_key --cwd <repo> --allow-write <unit folder> \
        --prompt prompt.txt --log run.jsonl

AGENT_BASH names the shell on Windows (Git Bash's bash.exe)."""
import argparse
import base64
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

TOOLS = [
    {"name": "bash", "description": "Run a command in Git Bash (POSIX shell) from the working directory. "
     "Returns stdout+stderr and the exit code. Use timeout_s up to 900 for renders.",
     "input_schema": {"type": "object", "properties": {"command": {"type": "string"},
                      "timeout_s": {"type": "integer"}}, "required": ["command"]}},
    {"name": "read_file", "description": "Read a text file (optionally a line range).",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "offset": {"type": "integer"},
                      "limit": {"type": "integer"}}, "required": ["path"]}},
    {"name": "write_file", "description": "Create or overwrite a text file with exactly this content.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                      "required": ["path", "content"]}},
    {"name": "edit_file", "description": "Replace one exact occurrence of old with new in a text file.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "old": {"type": "string"},
                      "new": {"type": "string"}}, "required": ["path", "old", "new"]}},
    {"name": "view_image", "description": "Look at an image file (png/jpg). The image is shown to you.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
]
DENY = re.compile(r"\bgit\s+(add|commit|push|reset|checkout|switch|stash|clean|rebase|merge|rm|mv|restore)\b"
                  r"|\brm\s+-[a-z]*r[a-z]*\s+(/|~|\.\.|[A-Za-z]:)|\bshutdown\b|\bcurl\b|\bwget\b|\bpip\s+install\b")


def clip(s, n=12000):
    return s if len(s) <= n else s[:n // 2] + f"\n... [{len(s) - n} characters cut] ...\n" + s[-n // 2:]


def run_tool(name, inp, cwd, allow_write):
    def inside(p):
        q = (Path(cwd) / p).resolve() if not Path(p).is_absolute() else Path(p).resolve()
        return q
    try:
        if name == "bash":
            if DENY.search(inp["command"]):
                return "refused: this command is not allowed in the trial (git changes, downloads, installs, recursive deletes)", None
            r = subprocess.run([os.environ.get("AGENT_BASH", "bash"), "-c", inp["command"]], cwd=cwd, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=min(int(inp.get("timeout_s") or 180), 900),
                               env={**os.environ, "PYTHONIOENCODING": "utf-8", "AGENT_KEY": ""})
            return clip((r.stdout + r.stderr).strip() + f"\n[exit code {r.returncode}]"), None
        if name == "read_file":
            lines = inside(inp["path"]).read_text(encoding="utf-8", errors="replace").splitlines()
            a = int(inp.get("offset") or 0)
            b = a + int(inp.get("limit") or 400)
            body = "\n".join(f"{i + 1}\t{x}" for i, x in enumerate(lines[a:b], a))
            return clip(body + (f"\n[lines {a + 1}-{min(b, len(lines))} of {len(lines)}]"), 20000), None
        if name in ("write_file", "edit_file"):
            p = inside(inp["path"])
            if not str(p).lower().startswith(str(Path(allow_write).resolve()).lower()):
                return f"refused: writing is only allowed under {allow_write}", None
            if name == "write_file":
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(inp["content"], encoding="utf-8", newline="\n")
                return f"wrote {p} ({len(inp['content'])} characters)", None
            s = p.read_text(encoding="utf-8")
            if s.count(inp["old"]) != 1:
                return f"edit failed: `old` occurs {s.count(inp['old'])} times (must be exactly 1)", None
            p.write_text(s.replace(inp["old"], inp["new"]), encoding="utf-8", newline="\n")
            return "edited", None
        if name == "view_image":
            from PIL import Image
            im = Image.open(inside(inp["path"])).convert("RGB")
            im.thumbnail((1568, 1568))
            buf = io.BytesIO()
            im.save(buf, "PNG")
            return f"image {inp['path']} ({im.width}x{im.height}) is attached below", base64.b64encode(buf.getvalue()).decode()
        return f"unknown tool {name}", None
    except subprocess.TimeoutExpired:
        return "timed out", None
    except Exception as e:
        return f"error: {type(e).__name__}: {e}", None


def call(base, model, system, messages):
    body = {"model": model, "max_tokens": 16000, "system": system, "tools": TOOLS, "messages": messages}
    for attempt in range(5):
        req = urllib.request.Request(base.rstrip("/") + "/v1/messages", json.dumps(body).encode(),
                                     {"x-api-key": os.environ["AGENT_KEY"], "anthropic-version": "2023-06-01",
                                      "content-type": "application/json"})
        try:
            return json.loads(urllib.request.urlopen(req, timeout=600).read())
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:500]
            if e.code < 500 and e.code != 429:
                raise RuntimeError(f"HTTP {e.code}: {msg}")
            err = f"HTTP {e.code}: {msg}"
        except Exception as e:
            err = f"{type(e).__name__}: {e}"
        print(f"  retry {attempt + 1}: {err}", flush=True)
        time.sleep(5 + 10 * attempt)
    raise RuntimeError(err)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--cwd", required=True)
    ap.add_argument("--allow-write", required=True, help="the only folder write_file/edit_file may touch")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--max-turns", type=int, default=260)
    ap.add_argument("--key-file", help="a file holding only the API key (keep it outside the repository)")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if a.key_file:
        os.environ["AGENT_KEY"] = Path(a.key_file).expanduser().read_text(encoding="utf-8").strip()
    if not os.environ.get("AGENT_KEY"):
        sys.exit("no key: pass --key-file or set AGENT_KEY")
    system = ("You are a careful coding agent working on a Windows machine through tools. The shell is Git Bash. "
              f"Your working directory is {a.cwd}. Work step by step with the tools; when you are completely "
              "finished, reply with your final report as plain text and no tool call.")
    messages = [{"role": "user", "content": Path(a.prompt).read_text(encoding="utf-8")}]
    log = open(a.log, "a", encoding="utf-8")
    used = {"in": 0, "out": 0, "tools": 0, "images": 0}
    t0 = time.time()
    for turn in range(a.max_turns):
        r = call(a.base, a.model, system, messages)
        u = r.get("usage", {})
        used["in"] += u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0)
        used["out"] += u.get("output_tokens", 0)
        content = r["content"]
        has_call = any(c["type"] == "tool_use" for c in content)
        has_text = any(c["type"] == "text" and c["text"].strip() for c in content)
        if not has_call and (r.get("stop_reason") == "max_tokens" or not has_text):
            # ran out of output while thinking, or said nothing: drop the turn and nudge
            print(f"[{turn:3d}] no action (stop_reason={r.get('stop_reason')}): nudging", flush=True)
            log.write(json.dumps({"turn": turn, "dropped": r.get("stop_reason"), "usage": u}) + "\n")
            nudge = {"type": "text", "text": "Your last turn ran out of output budget before any tool call, so it was "
                     "discarded. Think briefly, then act with a tool call. Put plans into files (write_file) "
                     "instead of working them out in your head."}
            if messages[-1]["role"] == "user":
                c0 = messages[-1]["content"]
                messages[-1]["content"] = ([{"type": "text", "text": c0}] if isinstance(c0, str) else c0) + [nudge]
            continue
        messages.append({"role": "assistant", "content": content})
        log.write(json.dumps({"turn": turn, "assistant": content, "usage": u}, ensure_ascii=False) + "\n")
        log.flush()
        calls = [c for c in content if c["type"] == "tool_use"]
        if not calls:
            final = "\n".join(c["text"] for c in content if c["type"] == "text")
            print(f"\n=== FINAL after {turn + 1} turns, {used['tools']} tool calls, {used['images']} images, "
                  f"{time.time() - t0:.0f} s, tokens in {used['in']} out {used['out']} ===\n{final}", flush=True)
            return 0
        results, images = [], []
        for c in calls:
            used["tools"] += 1
            text, img = run_tool(c["name"], c["input"], a.cwd, a.allow_write)
            brief = json.dumps(c["input"], ensure_ascii=False)[:150]
            print(f"[{turn:3d} {time.time() - t0:5.0f}s] {c['name']} {brief} -> {text[:110]!r}", flush=True)
            results.append({"type": "tool_result", "tool_use_id": c["id"], "content": text})
            if img:
                used["images"] += 1
                images.append({"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img}})
        log.write(json.dumps({"turn": turn, "results": [x["content"][:3000] for x in results]}, ensure_ascii=False) + "\n")
        # old images are dropped from the history to bound the context
        for m in messages:
            if m["role"] == "user" and isinstance(m["content"], list):
                m["content"] = [({"type": "text", "text": "[an image shown earlier was removed]"}
                                 if x.get("type") == "image" else x) for x in m["content"]]
        messages.append({"role": "user", "content": results + images})
    print(f"=== STOPPED at the turn limit, {used} ===")
    return 1


if __name__ == "__main__":
    sys.exit(main())
