# Sample 04 -- Scheduled Report Emailer

## What this automation does

Reads a metrics CSV, builds a plain-text or HTML email report, and sends it via SMTP (Gmail app password). Designed to run weekly. Logs each send to `sends.log`.

## Use it with your Claude.ai subscription
This is the primary path — **no API key, no terminal, no Python needed.** Just your
Claude.ai login (Pro or Team, which includes Cowork).

1. Open **Claude.ai** and click **Cowork** in the left sidebar, then start a new task.
2. Paste **the example prompt** below into the chat, and upload your data (a CSV) or ask
   Claude to make a sample one.
3. Press send — Claude builds the report and shows you a **preview** of the email. Ask for
   any changes you want.
4. To send: either have Claude **post the final email back into the chat** for you to
   forward (zero setup), or enable the **Gmail connector** in Claude's settings and have
   Claude prepare a draft. Then click **Schedule** → **Weekly**, e.g. Monday 8:00 AM.

### The example prompt
Copy this into Cowork as-is, then tweak it:

```
You are building a weekly report for me.

Each time you run:
1. Read my metrics from a file called metrics.csv (columns like: metric, value).
2. Work out the total of every numeric column.
3. Write a friendly, professional report email with:
   - a subject line like "Weekly Report — <today's date>"
   - a short summary sentence
   - a clean table of the metrics
   - a totals row at the bottom
4. Show me the finished email as a preview first so I can approve it.
5. Once I approve, prepare it as a Gmail draft addressed to team@yourcompany.com
   (I'll press send), OR just post the final email text back here in the chat.

Keep the tone warm and clear — this goes to my whole team.
```

## Problem it solves

Weekly reports that require manually opening a CSV, calculating totals, writing an email, formatting a table, and sending it to the team waste significant time. This automation does it in one command -- run it via cron on Monday morning and the report arrives in everyone's inbox automatically.

---

## Optional — automate it with code + cron (advanced)

You do **not** need any of the below for the course — the Cowork steps above are the whole
hands-on. This is a reference Python implementation that sends through Gmail SMTP from your
own server on a cron schedule. It needs a Gmail app password (set in `.env`) but **no
Anthropic API key**; a key only matters if you later wire Claude into the code, and that
key is separate from your Claude.ai subscription.

## How it works

1. Reads `metrics.csv` (configurable via `.env`)
2. Computes column totals for all numeric columns
3. Builds a styled HTML email with a data table, summary, and totals row
4. Builds a plain-text fallback for email clients that don't render HTML
5. Sends via Gmail SMTP (app password) using TLS
6. Appends a record to `sends.log` (timestamp, recipient, status)
7. Logs full details to `run.log`
8. Prints a console summary

## Email output

The email contains:
- A header with the report date
- A summary section (row count, column totals)
- A styled HTML data table with alternating row colors and a totals footer
- Plain-text fallback automatically included

## Quick start

```bash
python3 -m venv .venv
cp .env.example .env
# Edit .env with your Gmail credentials and recipient
bash run.sh
```

No pip install needed -- all libraries (`smtplib`, `email`, `csv`) are in Python's standard library.

## Setting up Gmail App Password

1. Enable 2-Step Verification on your Google account
2. Go to: https://myaccount.google.com/apppasswords
3. Generate a password for "Mail / Other"
4. Paste the 16-character password into `.env` as `SMTP_PASS`

## Scheduling

See [cron_setup.md](cron_setup.md) for full instructions.

Crontab line (every Monday at 08:00):
```
0 8 * * 1 /path/to/sample-04/run.sh >> /path/to/sample-04/cron.log 2>&1
```

## Files

| File | Purpose |
|------|---------|
| `main.py` | Email build and send automation |
| `run.sh` | Cron wrapper |
| `cron_setup.md` | Step-by-step scheduling guide |
| `.env.example` | Environment variable template |
| `metrics.csv` | Sample metrics data to report on |
| `requirements.txt` | No extra packages needed (stdlib only) |
| `time_log.csv` | Time saved before/after automation |
| `run.log` | Generated: per-run log |
| `sends.log` | Generated: history of email sends |
