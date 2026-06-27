# Cron Setup: API Fetch -> Transform -> Store Pipeline

## 1. Create a virtual environment

```bash
cd /path/to/sample-02
python3 -m venv .venv
```

## 2. Install dependencies

```bash
.venv/bin/pip install -r requirements.txt
```

Note: `sqlite3` and `requests` are the only libraries used. `sqlite3` is part of Python's
standard library. Only `requests` needs to be installed.

## 3. Configure your environment

```bash
cp .env.example .env
# Edit coordinates and city name for your location
nano .env
```

## 4. Test a manual run

```bash
bash run.sh
```

Expected output:
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
  DB total    : 1 rows in weather_data.db
  Elapsed     : 0.84s
=======================================================
```

## 5. Add to crontab (runs every hour)

```bash
crontab -e
```

Add this line:
```
0 * * * * /path/to/sample-02/run.sh >> /path/to/sample-02/cron.log 2>&1
```

For daily runs at 07:00:
```
0 7 * * * /path/to/sample-02/run.sh >> /path/to/sample-02/cron.log 2>&1
```

## 6. Query the stored data

```bash
sqlite3 weather_data.db "SELECT * FROM weather_readings ORDER BY fetched_at DESC LIMIT 10;"
```

Or with formatted output:
```bash
sqlite3 -column -header weather_data.db \
  "SELECT fetched_at, temperature_c, windspeed_kmh, weather_code FROM weather_readings ORDER BY fetched_at DESC LIMIT 5;"
```

## 7. Verify it ran

```bash
# Check cron log
tail -20 /path/to/sample-02/cron.log

# Check run log
tail -20 /path/to/sample-02/run.log

# Check DB row count
sqlite3 weather_data.db "SELECT COUNT(*) FROM weather_readings;"
```

## Other cities (Open-Meteo coordinates)

| City | LATITUDE | LONGITUDE |
|------|----------|-----------|
| London | 51.5074 | -0.1278 |
| Tokyo | 35.6762 | 139.6503 |
| Sydney | -33.8688 | 151.2093 |
| Mumbai | 19.0760 | 72.8777 |

Find any city at: https://open-meteo.com/
