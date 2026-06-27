#!/usr/bin/env bash
# run.sh -- cron wrapper for the Report Emailer
# Cron example (weekly Monday 08:00):
#   0 8 * * 1 /path/to/sample-04/run.sh >> /path/to/sample-04/cron.log 2>&1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f ".env" ]; then
    set -a
    source ".env"
    set +a
fi

VENV_DIR="${VENV_DIR:-$SCRIPT_DIR/.venv}"
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "[run.sh] ERROR: venv not found at $VENV_DIR"
    echo "[run.sh] Run: python3 -m venv .venv"
    exit 1
fi
source "$VENV_DIR/bin/activate"

echo "[run.sh] $(date '+%Y-%m-%d %H:%M:%S') -- starting report-emailer"
python main.py
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "[run.sh] $(date '+%Y-%m-%d %H:%M:%S') -- completed OK"
else
    echo "[run.sh] $(date '+%Y-%m-%d %H:%M:%S') -- FAILED with exit code $EXIT_CODE"
fi

exit $EXIT_CODE
