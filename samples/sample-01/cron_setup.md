# Cron Setup: Daily Web Scraper

## 1. Create a virtual environment

```bash
cd /path/to/sample-01
python3 -m venv .venv
```

## 2. Install dependencies

```bash
.venv/bin/pip install -r requirements.txt
```

## 3. Configure your environment

```bash
cp .env.example .env
# Edit .env and set TARGET_URL and CSS_SELECTOR to match your target page
nano .env
```

## 4. Test a manual run

```bash
bash run.sh
```

You should see output like:
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

## 5. Add to crontab (runs every day at 08:00)

```bash
crontab -e
```

Add this line (replace the path with your actual path):
```
0 8 * * * /path/to/sample-01/run.sh >> /path/to/sample-01/cron.log 2>&1
```

## 6. Verify it ran

After the next scheduled run:

```bash
# Check cron output
tail -20 /path/to/sample-01/cron.log

# Check run log
tail -20 /path/to/sample-01/run.log

# Check the CSV data
tail -5 /path/to/sample-01/scraped_data.csv
```

## Output files

| File | Description |
|------|-------------|
| `scraped_data.csv` | Timestamped scraped values (timestamp, url, selector, value) |
| `run.log` | Detailed run log with timestamps |
| `cron.log` | Cron execution log (stdout + stderr) |

## Customising the target

Edit `.env` to point at any public page:

```bash
# Example: scrape book titles from books.toscrape.com
TARGET_URL=https://books.toscrape.com/
CSS_SELECTOR=article.product_pod h3 a

# Example: scrape headlines from a news site
TARGET_URL=https://example-news.com/
CSS_SELECTOR=h2.article-title
```
