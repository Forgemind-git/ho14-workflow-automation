# Sample 02 -- API Fetch -> Transform -> Store Pipeline

## What this automation does

Fetches JSON from a public API, extracts the configured fields, transforms (renames + formats), and appends to a local SQLite database. Sends a console summary on each run.

**Target:** Open-Meteo weather API (free, no API key required)

## Use it with your Claude.ai subscription
This is the primary path — **no API key, no terminal, no Python needed.** Just your
Claude.ai login (Pro or Team, which includes Cowork). The weather API below is also free
and needs no key.

1. Open **Claude.ai** and click **Cowork** in the left sidebar, then start a new task.
2. Paste **the example prompt** below into the chat.
3. Press send — Claude calls the service, saves the first reading, and shows you what it stored.
4. Click **Schedule** on the task → **Hourly** or **Daily**. Cowork keeps collecting for you.

### The example prompt
Copy this into Cowork as-is (it uses a free, no-key weather API), then tweak it:

```
You are setting up a small recurring data pipeline for me.

Each time you run, please:
1. Call this free weather API (no key needed):
   https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&current_weather=true
2. From the JSON response, read the "current_weather" section.
3. Transform it into clean, readable columns:
   - fetched_at (current date and time)
   - city (use "New York")
   - temperature_c (from "temperature")
   - windspeed_kmh (from "windspeed")
   - wind_direction (from "winddirection")
   - weather_code (from "weathercode")
4. Append that as one new row to a file called weather_data.csv (create it with a header
   row the first time, then just add rows after that).
5. Show me the row you just added and the total number of rows in the file.

Keep using the same weather_data.csv every run so a history builds up.
```

## Problem it solves

Manually checking an API, copying values into a spreadsheet, and renaming columns to match your schema is repetitive. This pipeline automates the full ETL cycle: fetch -> transform -> store. Run it hourly or daily to build a historical dataset automatically.

---

## Optional — automate it with code + cron (advanced)

You do **not** need any of the below for the course — the Cowork steps above are the whole
hands-on. This is a reference Python implementation (storing readings in a local SQLite
database) for developers who want to run it unattended with a script and cron. It needs
**no Anthropic API key**; a key only matters if you later wire Claude into the code, and
that key is separate from your Claude.ai subscription.

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
