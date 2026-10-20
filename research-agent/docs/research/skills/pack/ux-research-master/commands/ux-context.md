---
description: "What do we know about an area, cohort or flow"
argument-hint: "<area / cohort / flow>"
---

What do we know about **$ARGUMENTS**? Sweep Dovetail, PostHog (session replay
included), Outset, Pendo and support tickets. Grade what you find — Verified,
Indicative, Anecdotal — name the gaps, and say plainly what we cannot answer
from what already exists.

## How to run this

Read `.agents/skills/user-context/SKILL.md` and run its workflow in this chat
(fallbacks: `.claude/skills/user-context/`, `.cursor/skills/user-context/`,
`~/.claude/skills/user-context/`). Do not paraphrase the skill from memory.
If two or more sources disagree, hand to `research-synthesis` rather than
averaging them.

Standing rules: label Verified vs AI interpretation · never invent a metric,
quote or participant · Jira, Confluence, Outset and Pendo stay draft-only
until a human confirms · never launch recruitment or publish a guide to live
traffic · if a connector this needs is not authorised, say which, say what
the answer loses, and run the rest.
