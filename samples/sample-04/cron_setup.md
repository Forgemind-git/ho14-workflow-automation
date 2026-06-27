# Cron Setup: Scheduled Report Emailer

## 1. Create a virtual environment

All libraries used (`smtplib`, `email`, `csv`) are part of Python's standard library.
No pip install is required, but we create the venv for consistency.

```bash
cd /path/to/sample-04
python3 -m venv .venv
```

## 2. Configure Gmail App Password

1. Log in to your Google account
2. Go to: https://myaccount.google.com/apppasswords
3. Select **App: Mail** and **Device: Other (Custom name)**, name it "Report Emailer"
4. Copy the 16-character app password shown

> Note: You need 2-Step Verification enabled on your Google account first.

## 3. Configure your environment

```bash
cp .env.example .env
nano .env
```

Fill in:
```
SMTP_USER=you@gmail.com
SMTP_PASS=abcd efgh ijkl mnop   # the 16-char app password
REPORT_TO=team@yourcompany.com
```

## 4. Prepare your metrics CSV

Edit `metrics.csv` with your actual data (or point `METRICS_CSV` to your file):

```csv
week,leads,demos,deals_closed,revenue
2026-06-22,47,13,3,9300
```

## 5. Test a manual run

```bash
bash run.sh
```

You should see:
```
=======================================================
  Report Emailer -- Run Complete
=======================================================
  To       : team@yourcompany.com
  Subject  : Weekly Metrics Report -- Jun 27, 2026
  Rows     : 4
  Columns  : week, leads, demos, deals_closed, revenue
  Totals   :
    leads = 178.00
    demos = 50.00
    deals_closed = 15.00
    revenue = 43750.00
  Status   : OK
  Elapsed  : 1.45s
  Sends log: sends.log
=======================================================
```

## 6. Add to crontab (runs every Monday at 08:00)

```bash
crontab -e
```

Add this line:
```
0 8 * * 1 /path/to/sample-04/run.sh >> /path/to/sample-04/cron.log 2>&1
```

Other schedule examples:
```
# Daily at 07:30
30 7 * * * /path/to/sample-04/run.sh >> /path/to/sample-04/cron.log 2>&1

# First of every month at 09:00
0 9 1 * * /path/to/sample-04/run.sh >> /path/to/sample-04/cron.log 2>&1
```

## 7. Verify it ran

```bash
# Check sends log
cat sends.log
# sent_at,to,subject,row_count,status
# 2026-06-27 08:00:01,team@...,Weekly Metrics Report -- Jun 27 2026,4,OK

# Check run log
tail -10 run.log

# Check cron log
tail -10 cron.log
```

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `SMTP auth failed` | Wrong app password | Regenerate at myaccount.google.com/apppasswords |
| `FileNotFoundError` | metrics.csv missing | Create or set `METRICS_CSV` in .env |
| `Empty CSV` | CSV has no data rows | Add data rows below the header |
| `Connection refused` | Wrong SMTP host/port | Check `SMTP_HOST=smtp.gmail.com` and `SMTP_PORT=587` |
