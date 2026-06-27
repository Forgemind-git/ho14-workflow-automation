# Sample 03 -- File Drop Watcher & Processor

## What this automation does

Watches an `input/` folder for new CSV files. When one appears, reads it, computes a summary (row count, column totals), writes a `processed_` prefixed copy to `output/`, and moves the original to `processed/`.

## Problem it solves

Teams that receive export files (from ERPs, CRMs, reports) spend time manually opening each file, checking row counts, calculating totals, renaming/moving files, and organising archives. This watcher does it automatically the moment a file lands.

## How it works

1. On startup, processes any CSV files already in `input/`
2. Starts a watchdog file system observer on `input/`
3. When a new `.csv` file is detected:
   - Waits `FILE_SETTLE_DELAY` seconds (lets slow copies finish)
   - Reads all rows with `csv.DictReader`
   - Computes row count and per-column totals for numeric columns
   - Writes a `processed_` copy to `output/` (adds `__processed_at` column)
   - Moves the original to `processed/` (with timestamp suffix if name collides)
   - Logs everything to `run.log`
4. Prints a live console summary for each file processed
5. Runs until Ctrl+C

## Output example

```
[08:00:01] Processing: sales_june.csv
  Rows     : 3
  Columns  : 4 (date, product, quantity, price)
  Totals   :
    quantity = 23.00
    price    = 100.99
  Output   : output/processed_sales_june.csv
  Archived : processed/sales_june.csv

=======================================================
  File Drop Watcher -- Active
=======================================================
  Watching  : input/
  Output    : output/
  Archived  : processed/
  Log       : run.log
  Drop a .csv into input/ to process it.
  Press Ctrl+C to stop.
=======================================================
```

## Quick start

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
mkdir -p input output processed
cp .env.example .env
bash run.sh
```

Drop a CSV into `input/` and watch it process automatically.

## Scheduling

See [cron_setup.md](cron_setup.md) for full instructions.

Two modes:
- **Continuous:** `@reboot` crontab entry (recommended)
- **Batch:** `*/5 * * * *` crontab entry (runs every 5 minutes)

## Files

| File | Purpose |
|------|---------|
| `main.py` | Watcher and processor logic |
| `run.sh` | Startup wrapper |
| `cron_setup.md` | Step-by-step scheduling guide |
| `.env.example` | Environment variable template |
| `requirements.txt` | Python dependencies |
| `time_log.csv` | Time saved before/after automation |
| `run.log` | Generated: per-run log |
| `input/` | Drop CSV files here |
| `output/` | Processed copies appear here |
| `processed/` | Original files archived here |
