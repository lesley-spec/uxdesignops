---
description: "Triage a research request: decision, prior art, route"
argument-hint: "<the request>"
---

Research request: **$ARGUMENTS**

Run intake — what decision does this unlock, do we already know the answer,
and if not, is this MICRO (48h), SPRINT (1–2 weeks) or DEEP (4+ weeks), and
who runs it?

## How to run this

Read `.agents/skills/research-intake/SKILL.md` and run its workflow in this chat
(fallbacks: `.claude/skills/research-intake/`, `.cursor/skills/research-intake/`,
`~/.claude/skills/research-intake/`). Do not paraphrase the skill from memory.
The "do we already know" check runs through `user-context` before any route
is given. If we already know, say so and stop — do not route a study.

Standing rules: label Verified vs AI interpretation · never invent a metric,
quote or participant · Jira, Confluence, Outset and Pendo stay draft-only
until a human confirms · never launch recruitment or publish a guide to live
traffic · if a connector this needs is not authorised, say which, say what
the answer loses, and run the rest.
