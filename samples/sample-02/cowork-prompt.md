# Cowork Automation Prompt: API Fetch → Transform → Store Pipeline

No API key needed — this runs in **Claude Cowork** using your Claude.ai subscription.
(The weather API below is also free and needs no key.)

## Setup prompt (paste this into Cowork)

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

## Then schedule it
In Cowork, click **Schedule** on the task → choose **Hourly** or **Daily**.

## To adapt it
Swap the latitude/longitude for your city, or point the URL at a different API entirely
and tell Claude which fields to keep.
