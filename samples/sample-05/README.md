# Sample 05 -- Two-Source Sync Job

## What this automation does

Reads records from a primary source (CSV A) and a secondary source (CSV B), identifies rows in A missing from B (keyed on an ID column), appends them to B, and logs the sync delta.

## Problem it solves

When data lives in two places (a CRM export and a local database, two team spreadsheets, a master list and a filtered list), keeping them in sync manually means comparing hundreds of rows by eye and copy-pasting rows. This job does it automatically and tracks exactly what changed.

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
