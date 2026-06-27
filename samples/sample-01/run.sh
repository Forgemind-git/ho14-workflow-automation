#!/usr/bin/env bash
# run.sh -- cron wrapper for the Daily Web Scraper
# Usage: bash run.sh
# Cron example: 0 8 * * * /path/to/sample-01/run.sh >> /path/to/sample-01/cron.log 2>&1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Load .env if present
if [ -f ".env" ]; then
    set -a
    # shellcheck source=/dev/null
    source ".env"
    set +a
fi

# Activate virtual environment
VENV_DIR="${VENV_DIR:-$SCRIPT_DIR/.venv}"
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "[run.sh] ERROR: venv not found at $VENV_DIR"
    echo "[run.sh] Run: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
fi
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

echo "[run.sh] $(date '+%Y-%m-%d %H:%M:%S') -- starting web-scraper"
python main.py
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "[run.sh] $(date '+%Y-%m-%d %H:%M:%S') -- completed OK"
else
    echo "[run.sh] $(date '+%Y-%m-%d %H:%M:%S') -- FAILED with exit code $EXIT_CODE"
fi

exit $EXIT_CODE
