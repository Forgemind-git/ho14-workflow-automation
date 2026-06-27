# Sample 04 -- Scheduled Report Emailer

## What this automation does

Reads a metrics CSV, builds a plain-text or HTML email report, and sends it via SMTP (Gmail app password). Designed to run weekly. Logs each send to `sends.log`.

## Problem it solves

Weekly reports that require manually opening a CSV, calculating totals, writing an email, formatting a table, and sending it to the team waste significant time. This automation does it in one command -- run it via cron on Monday morning and the report arrives in everyone's inbox automatically.

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
