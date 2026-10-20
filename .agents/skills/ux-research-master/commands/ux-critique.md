---
description: "Do these mocks cover the spec?"
argument-hint: "<mock links> + <spec>"
---

**$ARGUMENTS**

Build the coverage matrix — what the framing asked for versus what the mocks
do — then critique the solution itself. Flag anything the spec needed and the
design silently dropped.

## How to run this

Read `.agents/skills/ux-critique/SKILL.md` and run its workflow in this chat
(fallbacks: `.claude/skills/ux-critique/`, `.cursor/skills/ux-critique/`,
`~/.claude/skills/ux-critique/`). Do not paraphrase the skill from memory.
If a prototype URL exists, offer `accessibility-review` next.

Standing rules: label Verified vs AI interpretation · never invent a metric,
quote or participant · Jira, Confluence, Outset and Pendo stay draft-only
until a human confirms · never launch recruitment or publish a guide to live
traffic · if a connector this needs is not authorised, say which, say what
the answer loses, and run the rest.
