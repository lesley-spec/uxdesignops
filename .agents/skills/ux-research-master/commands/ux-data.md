---
description: "A quantitative question: funnel, drop-off, trend"
argument-hint: "<question>"
---

Question: **$ARGUMENTS**

Run it in PostHog or Pendo, show me the numbers, and say what they can and
cannot support. Flag instrumentation that would make the answer trustworthy
if it is not already.

## How to run this

Read `.agents/skills/data-analyze/SKILL.md` and run its workflow in this chat
(fallbacks: `.claude/skills/data-analyze/`, `.cursor/skills/data-analyze/`,
`~/.claude/skills/data-analyze/`). Do not paraphrase the skill from memory.
If the event does not exist yet, hand to `research-builder` to instrument it.

Standing rules: label Verified vs AI interpretation · never invent a metric,
quote or participant · Jira, Confluence, Outset and Pendo stay draft-only
until a human confirms · never launch recruitment or publish a guide to live
traffic · if a connector this needs is not authorised, say which, say what
the answer loses, and run the rest.
