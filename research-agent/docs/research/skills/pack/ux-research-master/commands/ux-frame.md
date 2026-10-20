---
description: "Frame health: what we hold, how confident, what's stale"
argument-hint: "[product area]"
---

Show me the Frame for **$ARGUMENTS**: the claims we hold, the confidence on
each, what they rest on, and what has gone stale. Rank by what a current
decision depends on. End with the three things most worth re-checking.

## How to run this

Read `.agents/skills/user-context/SKILL.md` and run its workflow in this chat
(fallbacks: `.claude/skills/user-context/`, `.cursor/skills/user-context/`,
`~/.claude/skills/user-context/`). Do not paraphrase the skill from memory.
If anything looks stale or they asked what to retire, continue into
`frame-maintenance`.

Standing rules: label Verified vs AI interpretation · never invent a metric,
quote or participant · Jira, Confluence, Outset and Pendo stay draft-only
until a human confirms · never launch recruitment or publish a guide to live
traffic · if a connector this needs is not authorised, say which, say what
the answer loses, and run the rest.
