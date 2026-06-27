"""
Sample 02 -- API Fetch -> Transform -> Store Pipeline
Fetches JSON from a public API, extracts configured fields,
transforms (renames + formats), and appends to a local SQLite database.
Sends a console summary on each run.

Target: Open-Meteo weather API (free, no API key required)
"""

import os
import sqlite3
import logging
import datetime
import requests
from pathlib import Path

# -- Configuration (override via .env) ----------------------------------------
LATITUDE = os.getenv("LATITUDE", "40.7128")
LONGITUDE = os.getenv("LONGITUDE", "-74.0060")
CITY_NAME = os.getenv("CITY_NAME", "New York")
DB_FILE = os.getenv("DB_FILE", "weather_data.db")
LOG_FILE = os.getenv("LOG_FILE", "run.log")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))

OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude={lat}&longitude={lon}"
    "&current_weather=true"
    "&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
    "&forecast_days=1"
)

# -- Logging setup ------------------------------------------------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# -- Database helpers ---------------------------------------------------------

def get_connection(db_path):
    """Return a SQLite connection with row_factory set."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_table(conn):
    """Create the weather_readings table if it does not exist."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS weather_readings (
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
        )
    """)
    conn.commit()


def insert_reading(conn, record):
    """Insert one weather record into the database."""
    conn.execute(
        """
        INSERT INTO weather_readings
            (fetched_at, city, latitude, longitude,
             temperature_c, windspeed_kmh, wind_direction, weather_code, is_day)
        VALUES
            (:fetched_at, :city, :latitude, :longitude,
             :temperature_c, :windspeed_kmh, :wind_direction, :weather_code, :is_day)
        """,
        record,
    )
    conn.commit()


def row_count(conn):
    """Return total number of rows in the table."""
    return conn.execute("SELECT COUNT(*) FROM weather_readings").fetchone()[0]


# -- API helpers --------------------------------------------------------------

def fetch_weather(lat, lon):
    """Fetch current weather from Open-Meteo."""
    url = OPEN_METEO_URL.format(lat=lat, lon=lon)
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()


def transform(raw_json, city, lat, lon, fetched_at):
    """
    Extract and rename fields from the Open-Meteo response.
    
    Raw field names -> our column names:
        temperature      -> temperature_c
        windspeed        -> windspeed_kmh
        winddirection    -> wind_direction
        weathercode      -> weather_code
        is_day           -> is_day
    """
    cw = raw_json.get("current_weather", {})
    return {
        "fetched_at":     fetched_at,
        "city":           city,
        "latitude":       float(lat),
        "longitude":      float(lon),
        "temperature_c":  cw.get("temperature"),
        "windspeed_kmh":  cw.get("windspeed"),
        "wind_direction": cw.get("winddirection"),
        "weather_code":   cw.get("weathercode"),
        "is_day":         cw.get("is_day"),
    }


def weather_description(code):
    """Map WMO weather interpretation code to a human-readable string."""
    codes = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Icy fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Heavy drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
        80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
        95: "Thunderstorm", 99: "Thunderstorm with hail",
    }
    return codes.get(code, "Unknown ({})".format(code))


# -- Main ---------------------------------------------------------------------

def main():
    run_start = datetime.datetime.now()
    fetched_at = run_start.strftime("%Y-%m-%d %H:%M:%S")

    log.info("-" * 60)
    log.info("Run started | city=%s | lat=%s | lon=%s", CITY_NAME, LATITUDE, LONGITUDE)

    # -- Fetch ----------------------------------------------------------------
    try:
        raw = fetch_weather(LATITUDE, LONGITUDE)
    except requests.exceptions.Timeout:
        log.error("API request timed out after %ds", REQUEST_TIMEOUT)
        print("[ERROR] API request timed out after {}s".format(REQUEST_TIMEOUT))
        return 1
    except requests.exceptions.HTTPError as exc:
        log.error("HTTP error: %s", exc)
        print("[ERROR] HTTP error: {}".format(exc))
        return 1
    except requests.exceptions.RequestException as exc:
        log.error("Network error: %s", exc)
        print("[ERROR] Network error: {}".format(exc))
        return 1

    # -- Transform ------------------------------------------------------------
    record = transform(raw, CITY_NAME, LATITUDE, LONGITUDE, fetched_at)
    log.info(
        "Transformed | temp=%.1fC | wind=%.1f km/h | code=%s",
        record["temperature_c"] or 0,
        record["windspeed_kmh"] or 0,
        record["weather_code"],
    )

    # -- Store ----------------------------------------------------------------
    db_path = Path(DB_FILE)
    conn = get_connection(str(db_path))
    try:
        ensure_table(conn)
        insert_reading(conn, record)
        total_rows = row_count(conn)
    finally:
        conn.close()

    elapsed = (datetime.datetime.now() - run_start).total_seconds()
    log.info(
        "Run complete | rows_in_db=%d | elapsed=%.2fs | db=%s",
        total_rows,
        elapsed,
        db_path,
    )

    # -- Console summary ------------------------------------------------------
    desc = weather_description(record["weather_code"] or -1)
    day_night = "Day" if record["is_day"] else "Night"

    print("\n" + "=" * 55)
    print("  API Pipeline -- Run Complete")
    print("=" * 55)
    print("  City        : {} ({}, {})".format(CITY_NAME, LATITUDE, LONGITUDE))
    print("  Fetched at  : {}".format(fetched_at))
    print("  Temperature : {:.1f} C".format(record["temperature_c"] or 0))
    print("  Wind        : {:.1f} km/h @ {}deg".format(
        record["windspeed_kmh"] or 0, record["wind_direction"] or 0))
    print("  Condition   : {}".format(desc))
    print("  Time        : {}".format(day_night))
    print("  DB total    : {} rows in {}".format(total_rows, db_path))
    print("  Elapsed     : {:.2f}s".format(elapsed))
    print("=" * 55 + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
