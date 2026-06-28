# CLAUDE.md — Coded Workflow Automation (HO14)

Guidance for **Claude Code / Claude Cowork** when working in this repo. The student is on the
**Claude.ai Pro plan**, which is usage-limited — work economically so their limit stretches,
*even when they make mistakes*.

## About this project
A workflow automation you can run and schedule.
**Primary way to do it:** Claude Cowork — **no API key needed.**
The work lives under `samples/sample-01 … sample-05`; each sample has its own `README.md` with a
ready-to-use example prompt. Start from those — they already work.

## Spend tokens wisely (read this first)
- **Plan before you build.** State a 1–3 line plan, then make the whole change in one pass.
- **Use the example prompt in the sample README** instead of writing a new one — it's tested.
- **Don't re-read or re-paste** files already shown in the conversation.
- **Keep replies short** — show only what changed, skip the preamble.
- **Make all related edits at once** — no trial-and-error loops.
- **Ask one clear question when unsure** rather than guessing and redoing the work.
- **Reuse the starter files** — tweak them, don't rebuild from scratch.

## This repo, specifically
- It's the **Coded Workflow Automation** hands-on. Automation in Cowork; code + cron is optional/advanced.
- **No API key is required for the course.** Any `main.py` / backend code is OPTIONAL, costs
  money, and should be ignored unless the student explicitly asks for the advanced path.
- When helping on the `starter` branch, don't restructure the repo or touch `main`.

See `SKILL.md` for the reusable **token-wise** skill that carries these same rules into Claude.ai.
