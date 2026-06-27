# Sample 01 -- Daily Web Scraper -> Sheet

## What this automation does

Scrapes a target URL for a configured CSS selector (e.g. price, headline), cleans the value, and appends a timestamped row to a CSV. Runs daily via cron.

**Target:** quotes.toscrape.com (freely scrapable public page -- swap via .env)

## Problem it solves

Instead of manually visiting a website each day, copying data into a spreadsheet, and formatting it -- this script does it in seconds on a schedule. You wake up to fresh data already in your CSV.

## How it works

1. Reads `TARGET_URL` and `CSS_SELECTOR` from `.env`
2. Fetches the page with a proper User-Agent header
3. Parses the HTML with BeautifulSoup
4. Extracts all elements matching the CSS selector
5. Cleans each value (strips whitespace and quote characters)
6. Appends timestamped rows to `scraped_data.csv`
7. Writes a detailed entry to `run.log`
8. Prints a console summary

## Output example

```
=======================================================
  Daily Web Scraper -- Run Complete
=======================================================
  URL      : https://quotes.toscrape.com/
  Selector : span.text
  Rows     : 10 appended to scraped_data.csv
  Elapsed  : 1.23s
  First 3  :
    * The world as we have created it is a process of our thinking.
    * It is our choices, Harry, that show what we truly are.
    * There are only two ways to live your life.
=======================================================
```

`scraped_data.csv` format:
```
timestamp,url,selector,value
2026-06-27 08:00:01,https://quotes.toscrape.com/,span.text,The world as we have created it...
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

Crontab line (daily at 08:00):
```
0 8 * * * /path/to/sample-01/run.sh >> /path/to/sample-01/cron.log 2>&1
```

## Files

| File | Purpose |
|------|---------|
| `main.py` | Core automation logic |
| `run.sh` | Cron wrapper (loads .env, activates venv) |
| `cron_setup.md` | Step-by-step scheduling guide |
| `.env.example` | Environment variable template |
| `requirements.txt` | Python dependencies |
| `time_log.csv` | Time saved before/after automation |
| `run.log` | Generated: per-run log |
| `scraped_data.csv` | Generated: output data |
