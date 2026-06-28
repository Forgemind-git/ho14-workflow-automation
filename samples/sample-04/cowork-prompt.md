# Cowork Automation Prompt: Scheduled Report Emailer

No API key needed — this runs in **Claude Cowork** using your Claude.ai subscription.

## Setup prompt (paste this into Cowork)

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

## Then schedule it
In Cowork, click **Schedule** on the task → choose **Weekly**, e.g. Monday at 8:00 AM.

## Sending email (two easy options)
- **Simplest:** have Claude post the finished email back into the chat each week and you
  forward it. No setup at all.
- **Hands-off:** enable the **Gmail connector** in Claude's settings, then have Claude
  prepare a draft (or send) each week.

## To adapt it
Replace metrics.csv with your real numbers, change the recipient and subject, and adjust
the schedule (weekly, fortnightly, monthly).
