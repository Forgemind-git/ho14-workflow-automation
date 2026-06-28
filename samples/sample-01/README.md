# HO14 Sample 1 — Daily Web Scraper

## What you'll build
A little robot that does a boring morning job for you. Every day it visits a web page,
grabs the numbers or text you care about (a price, a headline, a stock count), and adds
them as a new row in a spreadsheet — with the date stamped on it. You set it up once in
**Claude Cowork** and it keeps a tidy history for you without you lifting a finger.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login (Pro or Team, which includes Cowork).

1. Open **Claude.ai** in your browser and click **Cowork** in the left sidebar.
2. Start a new Cowork task.
3. Copy **the example prompt** below and paste it into the Cowork chat box. (Change the
   website address and what to grab to match your own page first — see "Make it your own".)
4. Press send. Claude will write a small script, run it, and show you the first rows it
   collected. Check they look right.
5. Click the **Schedule** button on the task and choose **Daily** at the time you want
   (e.g. 8:00 AM). That's it — Cowork now runs it for you every morning.
6. Come back any day and ask Claude *"show me the spreadsheet so far"* to see your history.

## The example prompt
Copy this into Cowork exactly as-is (it works against a free practice page), then tweak it:

```
You are setting up a small daily automation for me.

Every day, please do the following:
1. Open this web page: https://quotes.toscrape.com/
2. Find every quote on the page (each one is in an element matching the CSS selector "span.text").
3. Clean each quote — strip extra spaces and surrounding quote marks.
4. Append the results to a spreadsheet file called scraped_data.csv, one row per quote,
   with these columns: timestamp, source_url, value.
5. Use the current date and time for the timestamp column.
6. After it runs, show me how many new rows you added and the first 3 values, so I can
   confirm it worked.

Keep the same CSV file each day so the history builds up over time. If the page can't be
reached, log the error and don't add empty rows.
```

## Make it your own
- Swap `https://quotes.toscrape.com/` for the page you actually check each morning.
- Change the CSS selector to point at the thing you want — ask Claude in Cowork
  *"what's the CSS selector for the price on this page?"* and paste the page URL.
- Change the schedule from Daily to Weekly, or move the time to suit you.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. If you're a developer and later want to run the
same job from your own server with code instead of Cowork, the `main` branch of this repo
has a ready-made Python version (`main.py` + `cron_setup.md`). That route needs an
Anthropic API key, which is separate from your Claude.ai subscription and costs money — so
it's optional and not part of the hands-on.
