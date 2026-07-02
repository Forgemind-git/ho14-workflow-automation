# HO14 — Coded Workflow Automation

> Hands-on portfolio project · **Week 6** · **Solo** · module M18. Part of the **ForgeMind AI — AI Productivity Essentials** course.

## Goal

**Done when:** A scheduled, coded automation (Claude Code) · measured time saved

## What to ship

The automation script + how it's scheduled + a 5-step Loom + a measured before/after time log.

## Pick a problem statement

Choose **one** of these real use-cases — or bring your own (get it approved first):

1. You copy the same numbers off a website into a tracking sheet every morning and it is soul-crushing. Build a coded automation with Claude Code that scrapes that page daily, cleans the data, and appends it to a sheet or database, scheduled on a cron. Success: it runs unattended each day and your time log shows the daily minutes saved.

2. You manually pull from an API, reshape it, and drop it somewhere every day. Build a coded pipeline with Claude Code that fetches from the API, transforms the data, and stores it or sends a notification, triggered on a schedule. Success: a cron-driven run that completes the fetch-transform-store loop unattended, with a before/after time log.

3. Files land in a folder and someone has to process each one by hand. Build a file-watcher automation with Claude Code that detects a new file, processes it (convert or extract), and writes the output. Success: dropping a file triggers the job automatically and produces the result, with a time log showing the manual minutes removed.

4. Your boss expects the same report emailed every week and assembling it eats an hour. Build a scheduled job with Claude Code that queries the data, builds the report, and emails it weekly. Success: the email arrives on schedule with no manual steps, and a before/after time log proves the recurring hour saved.

5. Two of your systems drift out of sync and you reconcile them by hand. Build a coded sync job with Claude Code that keeps a sheet, database or tool aligned automatically on a schedule. Success: the systems stay in sync after each scheduled run with no manual reconciliation, documented with a before/after time log.

## How to use this repo

1. Click **Use this template** to create your own copy.
2. Build your chosen project in your copy.
3. Replace this section of the README with: what you built, the problem it solves, and how to run it.

---

*HO14 · Solo · ForgeMind AI Course · module M18 (Week 6)*


## 💡 Use your Claude.ai Pro plan wisely

The Pro plan has a usage limit that resets every few hours. A few habits make it stretch — and
keep a mistake from burning your whole session:

- **Use the example prompt** in each sample's README — it's already written and tested. Don't
  reinvent it.
- **One clear prompt** beats lots of vague back-and-forth. Say what you want, with an example, in
  a single message.
- **Start a new chat when you switch tasks.** Long chats re-read every earlier message and use up
  your limit faster.
- **Don't paste big files over and over.** Paste once, then refer back to it.
- **If something works, keep it.** Tweak it rather than regenerate from scratch.
- **Using Claude Code or Cowork?** This repo's `CLAUDE.md` makes Claude follow these same rules
  automatically, and `SKILL.md` is a reusable "token-wise" skill.

If you do hit the limit, it resets after a few hours — nothing you've saved is lost.

## Run it locally

This is a **scheduled, coded automation** — it runs on your own machine, not on the GitHub Pages
page (Pages is static and can't run a cron job). To run and schedule it:

```bash
# clone your copy of this repo, then from your project folder:
pip install -r requirements.txt

# run it once to make sure it works:
python main.py

# then schedule it with cron so it runs unattended.
# edit your crontab:
crontab -e

# example — run every day at 8am:
0 8 * * * cd /path/to/your/project && /usr/bin/python3 main.py >> run.log 2>&1
```

On Windows, use **Task Scheduler** instead of cron to run the same command on a schedule. Each
`samples/sample-0X/` folder has its own README with the exact run command and a suggested
schedule. Keep a before/after time log so you can measure the minutes saved.

## Deploying to a server

You don't have to host this anywhere to pass — it runs locally on your own schedule. If you later
want it running unattended on a public server (so it fires even when your laptop is off), the
course covers that once: **See the Week-6 deploy walkthrough**.
