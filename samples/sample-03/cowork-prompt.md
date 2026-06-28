# Cowork Automation Prompt: File Drop Watcher & Processor

No API key needed — this runs in **Claude Cowork** using your Claude.ai subscription.

## Setup prompt (paste this into Cowork)

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

## Then schedule it
In Cowork, click **Schedule** on the task → choose **Every 15 minutes** (or whatever fits
how often new files arrive).

## To adapt it
Tell Claude your real columns and what "processing" should do — e.g. flag rows over a
threshold, reformat dates, or save the output as Excel instead of CSV.
