# HO14 Sample 3 — File Drop Watcher & Processor

## What you'll build
A tireless helper that watches a folder. The moment a new spreadsheet file lands in it,
the helper opens it, counts the rows, adds up the numbers, saves a tidy processed copy,
and files the original away in an archive folder — all on its own. Perfect for those
"someone emailed me another export, now I have to deal with it" jobs.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login (Pro or Team, which includes Cowork).

1. Open **Claude.ai** and click **Cowork** in the left sidebar.
2. Start a new Cowork task.
3. Copy **the example prompt** below and paste it into the Cowork chat box.
4. Upload a sample CSV (or ask Claude to create a test one) so it has something to work on.
5. Press send. Claude will process the file and show you the summary and the processed
   copy. Check it looks right.
6. Click **Schedule** and choose **Every 15 minutes** (or whatever suits) so Cowork keeps
   checking the folder and processes anything new automatically.

## The example prompt
Copy this into Cowork exactly as-is, then tweak it for your own files:

```
You are setting up a file-processing helper for me.

I will drop CSV files into a folder called input/. Each time you run:
1. Look in the input/ folder for any CSV files that haven't been processed yet.
2. For each new CSV file:
   - Read all the rows.
   - Count how many rows there are.
   - For every column that contains numbers, add up the total.
   - Save a cleaned copy into an output/ folder, named "processed_<original name>",
     adding a column called processed_at with the current date and time.
   - Move the original file into a processed/ folder so it isn't handled twice.
3. Show me a short summary for each file: its name, the row count, and the column totals.

If there are no new files, just tell me "nothing new to process".
```

## Make it your own
- Tell Claude the real columns in your files and what "processing" should mean (e.g.
  "flag any row where amount is over 1000", or "convert the date column to DD/MM/YYYY").
- Ask it to save the output as Excel (`.xlsx`) instead of CSV if that's what you need.
- Change how often it checks the folder in the Schedule settings.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. If you later want a version that runs constantly
on your own machine and reacts the instant a file appears, the `main` branch has a Python
watcher (`main.py` + `cron_setup.md`). That path needs an Anthropic API key (separate from
your Claude.ai subscription and costs money), so it's optional only.
