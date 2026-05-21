#!/usr/bin/env bash
# NumberCals — one-command runner for Mac / Linux.
# Usage:  ./run.sh
#
# What it does:
#   1. Checks Python 3.9+ is available
#   2. Creates a local virtual environment (./.venv) on first run
#   3. Installs dependencies into the venv
#   4. Starts the server on http://localhost:8000
#
# Re-running just starts the server (skips install if already done).

set -e

cd "$(dirname "$0")/backend"

# 1. Find a usable Python
PY=""
for candidate in python3.12 python3.11 python3.10 python3.9 python3 python; do
  if command -v "$candidate" >/dev/null 2>&1; then
    VERSION=$("$candidate" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")
    MAJOR=$(echo "$VERSION" | cut -d. -f1)
    MINOR=$(echo "$VERSION" | cut -d. -f2)
    if [ "$MAJOR" = "3" ] && [ "$MINOR" -ge 9 ]; then
      PY="$candidate"
      break
    fi
  fi
done

if [ -z "$PY" ]; then
  echo "ERROR: Python 3.9 or newer is required."
  echo "Install from https://www.python.org/downloads/ and try again."
  exit 1
fi

echo "Using $PY ($("$PY" --version 2>&1))"

# 2. Create venv if missing
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment in backend/.venv ..."
  "$PY" -m venv .venv
fi

# 3. Activate + install if requirements changed (or first run)
# shellcheck disable=SC1091
source .venv/bin/activate

INSTALL_STAMP=".venv/.installed"
if [ ! -f "$INSTALL_STAMP" ] || [ "requirements.txt" -nt "$INSTALL_STAMP" ]; then
  echo "Installing dependencies (this may take a minute) ..."
  pip install --quiet --upgrade pip
  pip install --quiet -r requirements.txt
  touch "$INSTALL_STAMP"
fi

# 4. Start the server
echo ""
echo "=========================================="
echo "  NumberCals is starting at:"
echo "    http://localhost:8000"
echo ""
echo "  Press Ctrl+C to stop."
echo "=========================================="
echo ""

exec uvicorn main:app --host 127.0.0.1 --port 8000 --reload
