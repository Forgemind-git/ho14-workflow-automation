#!/usr/bin/env bash
# run.sh -- cron wrapper for the API Pipeline
# Cron example: 0 * * * * /path/to/sample-02/run.sh >> /path/to/sample-02/cron.log 2>&1

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
    echo "[run.sh] Run: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
fi
source "$VENV_DIR/bin/activate"

echo "[run.sh] $(date '+%Y-%m-%d %H:%M:%S') -- starting api-pipeline"
python main.py
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "[run.sh] $(date '+%Y-%m-%d %H:%M:%S') -- completed OK"
else
    echo "[run.sh] $(date '+%Y-%m-%d %H:%M:%S') -- FAILED with exit code $EXIT_CODE"
fi

exit $EXIT_CODE
