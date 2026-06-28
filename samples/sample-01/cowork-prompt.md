# Cowork Automation Prompt: Daily Web Scraper

No API key needed — this runs in **Claude Cowork** using your Claude.ai subscription.

## Setup prompt (paste this into Cowork)

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

## Then schedule it
In Cowork, click **Schedule** on the task → choose **Daily** at your preferred time.

## To adapt it
Change the URL and the CSS selector to your own page. Not sure of the selector? Ask Claude:
*"What CSS selector targets the price on this page?"* and paste your page's URL.
