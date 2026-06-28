# HO14 Sample 4 — Scheduled Report Emailer

## What you'll build
A weekly report that writes and sends itself. Every Monday morning the automation reads
your numbers, turns them into a clean little summary with totals, and emails it to your
team — so you never again spend an hour assembling the same report by hand.

## Use it with your Claude.ai subscription
No API key needed. Just your normal Claude.ai login (Pro or Team, which includes Cowork).

1. Open **Claude.ai** and click **Cowork** in the left sidebar.
2. Start a new Cowork task.
3. Copy **the example prompt** below and paste it into the Cowork chat box.
4. Upload your data (a CSV), or ask Claude to make a sample one to test with.
5. Press send. Claude will build the report and show you a **preview** of the email. Read
   it and tell Claude any changes you want ("add a line about last week's total", etc.).
6. To send real emails, connect your email in Cowork: the easiest beginner route is to
   ask Claude to **prepare the email as a draft in Gmail** (using the Gmail connector you
   enable in Claude's settings) so you just hit send. Then click **Schedule** → **Weekly**,
   Monday at 8:00 AM.

> Tip: if you'd rather keep it dead simple, skip email entirely — schedule the task to run
> weekly and just have Claude **post the finished report back into the chat** each Monday
> for you to forward. No email setup at all.

## The example prompt
Copy this into Cowork exactly as-is, then tweak it:

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

## Make it your own
- Replace `metrics.csv` with your real numbers, and tell Claude what each column means.
- Change the recipient, the subject line, and the tone (formal vs. casual).
- Move the schedule to fortnightly or monthly, or change the send time.

## Optional — automate it with the API (advanced)
You do **not** need this for the course. If you want a fully hands-off version that sends
through Gmail SMTP from your own server, the `main` branch has a Python emailer
(`main.py` + `.env.example` for a Gmail app password + `cron_setup.md`). The Claude-powered
version of that path would need an Anthropic API key (separate from your Claude.ai
subscription and costs money), so it's optional only.
