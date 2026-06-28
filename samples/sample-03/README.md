# Sample 03 -- File Drop Watcher & Processor

## What this automation does

Watches an `input/` folder for new CSV files. When one appears, reads it, computes a summary (row count, column totals), writes a `processed_` prefixed copy to `output/`, and moves the original to `processed/`.

## Use it with your Claude.ai subscription
This is the primary path — **no API key, no terminal, no Python needed.** Just your
Claude.ai login (Pro or Team, which includes Cowork).

1. Open **Claude.ai** and click **Cowork** in the left sidebar, then start a new task.
2. Paste **the example prompt** below into the chat.
3. Upload a sample CSV (or ask Claude to make a test one), then press send — Claude
   processes the file and shows you the summary and the processed copy.
4. Click **Schedule** on the task → **Every 15 minutes** (or whatever suits) so Cowork
   keeps checking for new files automatically.

### The example prompt
Copy this into Cowork as-is, then tweak it for your own files:

```
You are setting up a file-processing helper for me.

I will drop CSV files into a folder called input/. Each time you run:
1. Look in the input/ folder for any CSV files that haven't been processed yet.
2. For each new CSV file:
   - Read all the rows.
   - Count how many rows there are.
   - For every column that contains numbers, add up the total.
   - Save a cleaned copy into an output/ folder, named "processed_<original name>",
     adding a column called processed_at with the current date and time.
   - Move the original file into a processed/ folder so it isn't handled twice.
3. Show me a short summary for each file: its name, the row count, and the column totals.

If there are no new files, just tell me "nothing new to process".
```

## Problem it solves

Teams that receive export files (from ERPs, CRMs, reports) spend time manually opening each file, checking row counts, calculating totals, renaming/moving files, and organising archives. This watcher does it automatically the moment a file lands.

---

## Optional — automate it with code + cron (advanced)

You do **not** need any of the below for the course — the Cowork steps above are the whole
hands-on. This is a reference Python watcher (using watchdog) for developers who want it
running constantly on their own machine, reacting the instant a file appears. It needs
**no Anthropic API key**; a key only matters if you later wire Claude into the code, and
that key is separate from your Claude.ai subscription.

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
