#!/usr/bin/env bash
# wiki-check.sh — detect raw/ files that have not yet been ingested into the wiki.
#
# Usage: ./scripts/wiki-check.sh
#
# Compares modification timestamps in raw/ against entries in wiki/log.md
# and writes the names of any unprocessed files into
# progress.json.wiki.pending_raw_files (a JSON array of strings).
#
# Run this from the repository root after dropping a new file into raw/.
#
# Dependencies: bash, find, stat, awk, python3 (for safe JSON write).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RAW_DIR="$REPO_ROOT/raw"
LOG_FILE="$REPO_ROOT/wiki/log.md"
PROGRESS_FILE="$REPO_ROOT/progress.json"

if [ ! -d "$RAW_DIR" ]; then
  echo "raw/ not found at $RAW_DIR" >&2
  exit 1
fi
if [ ! -f "$LOG_FILE" ]; then
  echo "wiki/log.md not found at $LOG_FILE" >&2
  exit 1
fi
if [ ! -f "$PROGRESS_FILE" ]; then
  echo "progress.json not found at $PROGRESS_FILE" >&2
  exit 1
fi

# Collect every file in raw/ (excluding the README and any hidden files).
mapfile -t raw_files < <(
  find "$RAW_DIR" -maxdepth 1 -type f ! -name "README.md" ! -name ".*" -printf "%f\n" | sort
)

# Build the set of filenames already mentioned in wiki/log.md.
# A file is considered "ingested" if its basename appears in any log line.
pending=()
for f in "${raw_files[@]}"; do
  if ! grep -F -q "$f" "$LOG_FILE"; then
    pending+=("$f")
  fi
done

# Pick a working Python interpreter for safe JSON rewriting.
# Order: python3, py -3 (Windows launcher), python. Skip the WindowsApps
# python3 stub that prompts to install from the Microsoft Store.
PYTHON_BIN=""
PYTHON_ARGS=()
detect_python() {
  local cand
  for cand in python3 python; do
    if command -v "$cand" >/dev/null 2>&1; then
      local resolved
      resolved="$(command -v "$cand")"
      case "$resolved" in
        */WindowsApps/*) continue ;;  # MS Store stub — install prompt
      esac
      if "$cand" -c "import json,sys" >/dev/null 2>&1; then
        PYTHON_BIN="$cand"
        return 0
      fi
    fi
  done
  if command -v py >/dev/null 2>&1 && py -3 -c "import json,sys" >/dev/null 2>&1; then
    PYTHON_BIN="py"
    PYTHON_ARGS=("-3")
    return 0
  fi
  return 1
}

if detect_python; then
  if [ ${#pending[@]} -eq 0 ]; then
    set -- "$PROGRESS_FILE"
  else
    set -- "$PROGRESS_FILE" "${pending[@]}"
  fi
  "$PYTHON_BIN" "${PYTHON_ARGS[@]}" - "$@" <<'PY'
import json, sys
path = sys.argv[1]
pending = sys.argv[2:]
with open(path, "r", encoding="utf-8") as fh:
    data = json.load(fh)
data.setdefault("wiki", {})["pending_raw_files"] = pending
with open(path, "w", encoding="utf-8") as fh:
    json.dump(data, fh, indent=2)
    fh.write("\n")
PY
else
  echo "No working Python interpreter found; cannot safely rewrite progress.json" >&2
  echo "Pending files:" >&2
  printf '  %s\n' "${pending[@]:-(none)}" >&2
  exit 2
fi

count=${#pending[@]}
if [ "$count" -eq 0 ]; then
  echo "wiki-check: 0 pending files. raw/ is fully ingested."
else
  echo "wiki-check: $count pending file(s) recorded in progress.json:"
  printf '  - %s\n' "${pending[@]}"
fi
