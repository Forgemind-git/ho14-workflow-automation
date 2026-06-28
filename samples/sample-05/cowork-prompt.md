# Cowork Automation Prompt: Two-Source Sync Job

No API key needed — this runs in **Claude Cowork** using your Claude.ai subscription.

## Setup prompt (paste this into Cowork)

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

## Then schedule it
In Cowork, click **Schedule** on the task → choose **Daily**.

## To adapt it
Change the ID column to whatever uniquely identifies your rows (email, order_number, sku),
or sync a Google Sheet by enabling the Google connector in Claude.
