# Sample 01 -- Daily Web Scraper -> Sheet

## What this automation does

Scrapes a target URL for a configured CSS selector (e.g. price, headline), cleans the value, and appends a timestamped row to a CSV. Runs daily via cron.

**Target:** quotes.toscrape.com (freely scrapable public page -- swap via .env)

## Use it with your Claude.ai subscription
This is the primary path — **no API key, no terminal, no Python needed.** Just your
Claude.ai login (Pro or Team, which includes Cowork).

1. Open **Claude.ai** and click **Cowork** in the left sidebar, then start a new task.
2. Paste **the example prompt** below into the chat (swap the URL/selector for your own page first).
3. Press send — Claude writes and runs the script and shows you the first rows it collected.
4. Click **Schedule** on the task → **Daily** at your chosen time. Cowork now runs it for you.

### The example prompt
Copy this into Cowork as-is (it works against a free practice page), then tweak it:

```
You are setting up a small daily automation for me.

Every day, please do the following:
1. Open this web page: https://quotes.toscrape.com/
2. Find every quote on the page (each one is in an element matching the CSS selector "span.text").
3. Clean each quote — strip extra spaces and surrounding quote marks.
4. Append the results to a spreadsheet file called scraped_data.csv, one row per quote,
   with these columns: timestamp, source_url, value.
5. Use the current date and time for the timestamp column.
6. After it runs, show me how many new rows you added and the first 3 values.

Keep the same CSV file each day so the history builds up. If the page can't be reached,
log the error and don't add empty rows.
```

## Problem it solves

Instead of manually visiting a website each day, copying data into a spreadsheet, and formatting it -- this script does it in seconds on a schedule. You wake up to fresh data already in your CSV.

---

## Optional — automate it with code + cron (advanced)

You do **not** need any of the below for the course — the Cowork steps above are the whole
hands-on. This is a reference Python implementation for developers who want to run the job
unattended on their own server with a local script and cron. These scripts need **no
Anthropic API key**; an API key only comes into play if you later wire Claude into the
code yourself, and that key is separate from your Claude.ai subscription.

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
