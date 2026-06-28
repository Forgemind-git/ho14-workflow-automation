---
name: token-wise
description: Work economically on a Claude course hands-on so a Pro-plan student's usage limit stretches further. Use whenever helping build, debug, or extend this project.
---

# Token-Wise — make every message count

You are helping a student on the **Claude.ai Pro plan**, which has a usage limit that resets
every few hours. The goal: finish the hands-on in as few messages as possible, so the student
does not hit the limit mid-task — *even when they make mistakes*.

## Operating rules
1. **Plan, then act.** Before writing code or long output, give a 1–3 line plan, then make the
   whole change in one go — don't dribble it across many replies.
2. **One good prompt beats five vague ones.** Use the example prompt already in the sample
   README — it is tested. Don't regenerate things that already work.
3. **Don't repeat context.** If a file or output was already shown, refer to it — never re-paste
   or re-read it.
4. **Keep replies short.** No preamble, no restating the question, no giant code dumps unless
   asked. Show only what changed.
5. **Batch related edits.** Think it through once and make all the changes together; avoid
   trial-and-error loops.
6. **Ask one question when blocked.** A single clarifying question is far cheaper than guessing
   wrong and redoing the work.
7. **Reuse, don't rebuild.** Start from the starter files and tweak them — don't rewrite from
   scratch.

## Cheap vs expensive
- **Cheap:** short focused prompts, one task per message, using the provided examples, new chat
  per new task.
- **Expensive:** pasting whole large files repeatedly, "redo everything from scratch", long
  open-ended chats, asking Claude to re-explain what's already in the README.
