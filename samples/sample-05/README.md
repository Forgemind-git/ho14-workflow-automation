# Sample 05 -- Two-Source Sync Job

## What this automation does

Reads records from a primary source (CSV A) and a secondary source (CSV B), identifies rows in A missing from B (keyed on an ID column), appends them to B, and logs the sync delta.

## Use it with your Claude.ai subscription
This is the primary path — **no API key, no terminal, no Python needed.** Just your
Claude.ai login (Pro or Team, which includes Cowork).

1. Open **Claude.ai** and click **Cowork** in the left sidebar, then start a new task.
2. Paste **the example prompt** below into the chat, and upload your two CSV files (or let
   Claude create two sample files to test the idea).
3. Press send — Claude compares them, copies the missing rows across, and shows you exactly
   which ones it added.
4. Click **Schedule** on the task → **Daily** so the two stay in sync automatically.

### The example prompt
Copy this into Cowork as-is, then tweak it:

```
You are keeping two spreadsheets in sync for me.

I have two CSV files:
- source_a.csv  → the authoritative master list
- source_b.csv  → a second copy that should match it

Both share a unique ID column called "id".

Each time you run:
1. Read both files.
2. Find every row whose "id" is in source_a.csv but NOT in source_b.csv.
3. Append those missing rows to source_b.csv, adding a column called synced_at with the
   current date and time.
4. Keep a running log file called delta_log.jsonl — add one line per run recording the
   date, how many rows you added, and which ids they were.
5. Show me a summary: which ids were synced, or "already in sync" if nothing changed.

Important: running twice in a row should add nothing the second time (don't duplicate rows).
```

## Problem it solves

When data lives in two places (a CRM export and a local database, two team spreadsheets, a master list and a filtered list), keeping them in sync manually means comparing hundreds of rows by eye and copy-pasting rows. This job does it automatically and tracks exactly what changed.

---

## Optional — automate it with code + cron (advanced)

You do **not** need any of the below for the course — the Cowork steps above are the whole
hands-on. This is a reference Python sync job (with a JSON-Lines audit trail) for
developers who want it running unattended on their own server via cron. It needs **no
Anthropic API key**; a key only matters if you later wire Claude into the code, and that
key is separate from your Claude.ai subscription.

## How it works

1. Reads Source A (primary/authoritative CSV) -- `source_a.csv`
2. Reads Source B (secondary CSV) -- `source_b.csv` (creates it if missing)
3. Builds a set of IDs present in each source
4. Computes the delta: IDs in A but not in B
5. Appends the missing rows to Source B (with a `__synced_at` timestamp column)
6. Writes a JSON Lines delta record to `delta_log.jsonl`
7. Logs all activity to `run.log`
8. Prints a console summary showing exactly which IDs were synced
9. **Idempotent**: running twice in a row does nothing on the second run

## Output example

First run (2 records missing from B):
```
=======================================================
  Sync Job -- Run Complete
=======================================================
  Source A     : source_a.csv (4 rows)
  Source B     : source_b.csv (2 rows -> 4 rows)
  Appended     : 2 new row(s)
  IDs synced   :
    + 1003
    + 1004
  Delta log    : delta_log.jsonl
  Elapsed      : 0.01s
=======================================================
```

Second run (already in sync):
```
  Delta    : 0 rows to sync -- sources are IN SYNC
```

## Delta log format (`delta_log.jsonl`)

One JSON record per run:
```json
{"synced_at": "2026-06-27 08:00:01", "source_a_rows": 4, "source_b_rows_before": 2, "source_b_rows_after": 4, "appended": 2, "missing_ids": ["1003", "1004"], "status": "SYNCED"}
{"synced_at": "2026-06-27 14:00:01", "source_a_rows": 4, "source_b_rows": 4, "appended": 0, "missing_ids": [], "status": "IN_SYNC"}
```

## Quick start

```bash
python3 -m venv .venv
cp .env.example .env
# Edit .env to point at your CSVs and set ID_COLUMN
bash run.sh
```

No pip install needed -- all libraries (`csv`, `json`) are in Python's standard library.

## Scheduling

See [cron_setup.md](cron_setup.md) for full instructions.

Crontab line (every 6 hours):
```
0 */6 * * * /path/to/sample-05/run.sh >> /path/to/sample-05/cron.log 2>&1
```

## Files

| File | Purpose |
|------|---------|
| `main.py` | Sync logic -- compare, delta, append |
| `run.sh` | Cron wrapper |
| `cron_setup.md` | Step-by-step scheduling guide |
| `.env.example` | Environment variable template |
| `source_a.csv` | Sample primary source (4 records) |
| `source_b.csv` | Sample secondary source (2 records -- starts incomplete) |
| `requirements.txt` | No extra packages needed (stdlib only) |
| `time_log.csv` | Time saved before/after automation |
| `run.log` | Generated: per-run log |
| `delta_log.jsonl` | Generated: JSON Lines audit trail of every sync |
