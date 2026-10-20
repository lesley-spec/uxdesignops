---
description: "I need research on this - what's the fastest way to a real answer?"
argument-hint: "<question>"
---

I need research on **$ARGUMENTS**. What's the fastest way to a real answer?

What decision does this unlock, do we already know, and if not — 48 hours,
two weeks, or four-plus, and who should run it?

## How to run this

Read `.agents/skills/research-intake/SKILL.md` and run its workflow in this chat
(fallbacks: `.claude/skills/research-intake/`, `.cursor/skills/research-intake/`,
`~/.claude/skills/research-intake/`). Do not paraphrase the skill from memory.
Run the "do we already know" check through `user-context` before routing
anything. If it is already answered, say so and stop.

Standing rules: label Verified vs AI interpretation · never invent a metric,
quote or participant · Jira, Confluence, Outset and Pendo stay draft-only
until a human confirms · never launch recruitment or publish a guide to live
traffic · if a connector this needs is not authorised, say which, say what
the answer loses, and run the rest.

<!-- managed by ux-research-master -->
