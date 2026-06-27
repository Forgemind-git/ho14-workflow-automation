# Sample 02 -- API Fetch -> Transform -> Store Pipeline

## What this automation does

Fetches JSON from a public API, extracts the configured fields, transforms (renames + formats), and appends to a local SQLite database. Sends a console summary on each run.

**Target:** Open-Meteo weather API (free, no API key required)

## Problem it solves

Manually checking an API, copying values into a spreadsheet, and renaming columns to match your schema is repetitive. This pipeline automates the full ETL cycle: fetch -> transform -> store. Run it hourly or daily to build a historical dataset automatically.

## How it works

1. Reads city coordinates from `.env`
2. Calls the Open-Meteo `/v1/forecast` endpoint
3. Extracts `current_weather` fields from the JSON
4. Renames API field names to readable column names (e.g. `weathercode` -> `weather_code`)
5. Inserts a timestamped record into `weather_data.db` (SQLite)
6. Creates the table on first run -- idempotent, safe to run multiple times
7. Prints a console summary with the weather condition decoded

## Output example

```
=======================================================
  API Pipeline -- Run Complete
=======================================================
  City        : New York (40.7128, -74.0060)
  Fetched at  : 2026-06-27 08:00:01
  Temperature : 22.4 C
  Wind        : 14.2 km/h @ 230deg
  Condition   : Partly cloudy
  Time        : Day
  DB total    : 47 rows in weather_data.db
  Elapsed     : 0.84s
=======================================================
```

## Database schema

```sql
CREATE TABLE weather_readings (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    fetched_at       TEXT NOT NULL,
    city             TEXT NOT NULL,
    latitude         REAL NOT NULL,
    longitude        REAL NOT NULL,
    temperature_c    REAL,
    windspeed_kmh    REAL,
    wind_direction   INTEGER,
    weather_code     INTEGER,
    is_day           INTEGER
);
```

## Quick start

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
bash run.sh
```

## Scheduling

See [cron_setup.md](cron_setup.md) for full instructions.

Crontab line (every hour):
```
0 * * * * /path/to/sample-02/run.sh >> /path/to/sample-02/cron.log 2>&1
```

## Files

| File | Purpose |
|------|---------|
| `main.py` | Fetch, transform, store automation |
| `run.sh` | Cron wrapper |
| `cron_setup.md` | Step-by-step scheduling guide |
| `.env.example` | Environment variable template |
| `requirements.txt` | Python dependencies |
| `time_log.csv` | Time saved before/after automation |
| `run.log` | Generated: per-run log |
| `weather_data.db` | Generated: SQLite database |
