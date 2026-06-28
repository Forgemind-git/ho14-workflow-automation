# HO14 Sample 2 — API Fetch → Transform → Store Pipeline

## What you'll build
An automatic data collector. Once a day (or every hour) it calls a free online data
service, picks out the values you care about, tidies them up, and saves them into a
growing table — so over time you build your own little history without copying anything by
hand. The example uses a free weather service, but the same pattern works for any API.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login (Pro or Team, which includes Cowork).

1. Open **Claude.ai** and click **Cowork** in the left sidebar.
2. Start a new Cowork task.
3. Copy **the example prompt** below and paste it into the Cowork chat box.
4. Press send. Claude will call the service, save the first reading into a table, and show
   you what it stored so you can confirm it looks right.
5. Click **Schedule** on the task and choose how often to run it (e.g. **Hourly** or
   **Daily**). Cowork will keep collecting for you.
6. Any time, ask Claude *"show me everything collected so far as a table"* to review it.

## The example prompt
Copy this into Cowork exactly as-is (it uses a free, no-key weather API), then tweak it:

```
You are setting up a small recurring data pipeline for me.

Each time you run, please:
1. Call this free weather API (no key needed):
   https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&current_weather=true
2. From the JSON response, read the "current_weather" section.
3. Transform it into clean, readable columns:
   - fetched_at (current date and time)
   - city (use "New York")
   - temperature_c (from "temperature")
   - windspeed_kmh (from "windspeed")
   - wind_direction (from "winddirection")
   - weather_code (from "weathercode")
4. Append that as one new row to a file called weather_data.csv (create it with a header
   row the first time, then just add rows after that).
5. Show me the row you just added and the total number of rows in the file.

Keep using the same weather_data.csv every run so a history builds up.
```

## Make it your own
- Change the `latitude` and `longitude` in the URL to your own city — ask Claude
  *"what are the coordinates for Tokyo?"* if you're not sure.
- Point it at a completely different API (currency rates, your own product's stats, etc.) —
  just tell Claude the URL and which fields to keep.
- Set the schedule to hourly for fine detail, or daily for a lighter history.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. If you later want to run this from your own
server as code, the `main` branch has a Python version that stores readings in a SQLite
database (`main.py` + `cron_setup.md`). That path needs an Anthropic API key (separate
from your Claude.ai subscription, and it costs money), so it's optional only.
