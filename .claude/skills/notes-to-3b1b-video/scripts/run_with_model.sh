#!/usr/bin/env bash
# Run one role of PIPELINE.md on another provider's model, inside the Claude Code harness
# (its tools, permissions, context handling), headless. The endpoint must speak the
# Anthropic API. The key is read from a file and only ever lives in this process's
# environment.
#
#   run_with_model.sh KEY_FILE PROMPT_FILE [WORK_DIR]
#
#   MODEL=deepseek-flash BASE_URL=https://api.deepseek.com/anthropic   (the defaults)
#   CLAUDE_BIN=<path to claude>       default: `claude` on PATH, else the desktop app's copy
#   AGENT_HOME=<folder>               the worker's own config folder: none of your plugins,
#                                     memory or hooks are loaded, which keeps its context small
#
# Prints the worker's final message; the full JSON result is written next to the prompt
# as <prompt>.result.json. Run it in the background from a coordinator session, at most
# two at a time on one machine.
set -euo pipefail
key_file="$1"; prompt_file="$2"; work_dir="${3:-$PWD}"
model="${MODEL:-deepseek-flash}"
bin="${CLAUDE_BIN:-$(command -v claude || true)}"
if [ -z "$bin" ] && [ -n "${APPDATA:-}" ]; then
  bin="$(ls -t "$APPDATA"/Claude/claude-code/*/*/claude.exe 2>/dev/null | head -1)"
fi
[ -n "$bin" ] || { echo "no claude executable found: set CLAUDE_BIN" >&2; exit 2; }
home="${AGENT_HOME:-${TMPDIR:-${TEMP:-/tmp}}/kit_agent_home}"
mkdir -p "$home"
command -v cygpath >/dev/null && home="$(cygpath -w "$home")"

export CLAUDE_CONFIG_DIR="$home"
export ANTHROPIC_BASE_URL="${BASE_URL:-https://api.deepseek.com/anthropic}"
export ANTHROPIC_MODEL="$model" ANTHROPIC_DEFAULT_HAIKU_MODEL="$model" ANTHROPIC_SMALL_FAST_MODEL="$model"
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 PYTHONIOENCODING=utf-8
ANTHROPIC_AUTH_TOKEN="$(tr -d '\r\n ' < "$key_file")"; export ANTHROPIC_AUTH_TOKEN
unset ANTHROPIC_API_KEY CLAUDE_CODE_OAUTH_TOKEN

out="${prompt_file%.*}.result.json"
cd "$work_dir"
"$bin" -p "$(cat "$prompt_file")" --output-format json \
  --allowedTools "Bash Read Write Edit Glob Grep" \
  --disallowedTools "Bash(git add:*) Bash(git commit:*) Bash(git push:*) Bash(git reset:*) Bash(git checkout:*) Bash(git clean:*) Bash(git stash:*) Bash(pip install:*) Bash(curl:*) Bash(wget:*) WebFetch WebSearch Agent" \
  < /dev/null > "$out" 2> "${out%.json}.err.txt" || true
python - "$out" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception as e:
    sys.exit(f"no result ({e}); see the .err.txt next to {sys.argv[1]}")
u = d.get("usage") or {}
print(d.get("result") or "")
print(f"\n[turns {d.get('num_turns')}, {(d.get('duration_ms') or 0) / 60000:.1f} min, error {d.get('is_error')}, "
      f"input tokens {u.get('input_tokens', 0) + u.get('cache_read_input_tokens', 0)}, output {u.get('output_tokens')}]")
PY
