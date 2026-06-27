"""
Sample 01 -- Daily Web Scraper -> Sheet
Scrapes a target URL for a configured CSS selector, cleans the value,
and appends a timestamped row to a CSV. Runs daily via cron.
"""

import os
import csv
import logging
import datetime
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# -- Configuration (override via .env) ----------------------------------------
TARGET_URL = os.getenv("TARGET_URL", "https://quotes.toscrape.com/")
CSS_SELECTOR = os.getenv("CSS_SELECTOR", "span.text")
OUTPUT_CSV = os.getenv("OUTPUT_CSV", "scraped_data.csv")
LOG_FILE = os.getenv("LOG_FILE", "run.log")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))

# -- Logging setup ------------------------------------------------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def clean_value(raw):
    """Strip whitespace and remove common quote characters."""
    return raw.strip().strip("""''\"'")


def scrape_page(url, selector):
    """Fetch page and extract all elements matching the CSS selector."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; CourseBot/1.0; "
            "+https://github.com/Forgemind-git/ho14-workflow-automation)"
        )
    }
    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    elements = soup.select(selector)
    return [clean_value(el.get_text()) for el in elements if el.get_text().strip()]


def ensure_csv_header(path):
    """Create CSV with header row if it does not exist."""
    if not path.exists():
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "url", "selector", "value"])
        log.info("Created new CSV: %s", path)


def append_rows(path, rows):
    """Append scraped rows to the CSV file."""
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "url", "selector", "value"])
        writer.writerows(rows)


def main():
    run_start = datetime.datetime.now()
    log.info("-" * 60)
    log.info("Run started | url=%s | selector=%s", TARGET_URL, CSS_SELECTOR)

    csv_path = Path(OUTPUT_CSV)
    ensure_csv_header(csv_path)

    try:
        values = scrape_page(TARGET_URL, CSS_SELECTOR)
    except requests.exceptions.Timeout:
        log.error("Request timed out after %ds", REQUEST_TIMEOUT)
        print("[ERROR] Request timed out after {}s".format(REQUEST_TIMEOUT))
        return 1
    except requests.exceptions.HTTPError as exc:
        log.error("HTTP error: %s", exc)
        print("[ERROR] HTTP error: {}".format(exc))
        return 1
    except requests.exceptions.RequestException as exc:
        log.error("Network error: %s", exc)
        print("[ERROR] Network error: {}".format(exc))
        return 1

    if not values:
        log.warning("No elements matched selector '%s' on %s", CSS_SELECTOR, TARGET_URL)
        print("[WARN]  No elements matched selector '{}'".format(CSS_SELECTOR))
        return 0

    timestamp = run_start.strftime("%Y-%m-%d %H:%M:%S")
    rows = [
        {"timestamp": timestamp, "url": TARGET_URL, "selector": CSS_SELECTOR, "value": v}
        for v in values
    ]
    append_rows(csv_path, rows)

    elapsed = (datetime.datetime.now() - run_start).total_seconds()
    log.info(
        "Run complete | scraped=%d rows | elapsed=%.2fs | output=%s",
        len(rows),
        elapsed,
        csv_path,
    )

    # -- Console summary -------------------------------------------------------
    print("\n" + "=" * 55)
    print("  Daily Web Scraper -- Run Complete")
    print("=" * 55)
    print("  URL      : {}".format(TARGET_URL))
    print("  Selector : {}".format(CSS_SELECTOR))
    print("  Rows     : {} appended to {}".format(len(rows), csv_path))
    print("  Elapsed  : {:.2f}s".format(elapsed))
    print("  First 3  :")
    for v in values[:3]:
        print("    * {}".format(v[:80]))
    print("=" * 55 + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
