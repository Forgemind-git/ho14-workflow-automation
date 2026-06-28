# HO14 Sample 5 — Two-Source Sync Job

## What you'll build
A reconciler that keeps two lists in step. You have the same data in two places — say a
master spreadsheet and a second copy — and they drift apart. This automation compares
them, finds the rows that are missing from the second one, copies them over, and keeps a
record of exactly what it changed. No more eyeballing hundreds of rows.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login (Pro or Team, which includes Cowork).

1. Open **Claude.ai** and click **Cowork** in the left sidebar.
2. Start a new Cowork task.
3. Copy **the example prompt** below and paste it into the Cowork chat box.
4. Upload your two files (or let Claude create the two sample files to test the idea).
5. Press send. Claude will compare them, copy the missing rows across, and show you
   exactly which ones it added. Check that's correct.
6. Click **Schedule** → **Daily** so the two stay in sync automatically from now on.

## The example prompt
Copy this into Cowork exactly as-is, then tweak it:

```
You are keeping two spreadsheets in sync for me.

I have two CSV files:
- source_a.csv  → the authoritative master list
- source_b.csv  → a second copy that should match it

Both share a unique ID column called "id".

Each time you run:
1. Read both files.
2. Find every row whose "id" is in source_a.csv but NOT in source_b.csv.
3. Append those missing rows to source_b.csv, adding a column called synced_at with the
   current date and time.
4. Keep a running log file called delta_log.jsonl — add one line per run recording the
   date, how many rows you added, and which ids they were.
5. Show me a summary: which ids were synced, or "already in sync" if nothing changed.

Important: running twice in a row should add nothing the second time (don't duplicate rows).
```

## Make it your own
- Change the ID column name to whatever uniquely identifies a row in your data
  (e.g. `email`, `order_number`, `sku`).
- Sync in both directions if you need to (tell Claude "also copy B's new rows back to A").
- Point it at a Google Sheet instead of a CSV by enabling the Google connector in Claude.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. If you later want this running unattended on your
own server, the `main` branch has a Python sync job with a JSON-Lines audit trail
(`main.py` + `cron_setup.md`). A Claude-powered version of that would need an Anthropic API
key (separate from your Claude.ai subscription and costs money), so it's optional only.
