---
description: "Rank options on evidence rather than opinion"
argument-hint: "<options>"
---

Options: **$ARGUMENTS**

Rank these on what the evidence actually supports. For each: the claim it
rests on, the confidence, the users it serves, and what we would be guessing
about. Say which one has the weakest evidence under the loudest advocacy.

## How to run this

Read `.agents/skills/user-context/SKILL.md` and run its workflow in this chat
(fallbacks: `.claude/skills/user-context/`, `.cursor/skills/user-context/`,
`~/.claude/skills/user-context/`). Do not paraphrase the skill from memory.
This ranks evidence, not effort. Do not invent effort estimates.

Standing rules: label Verified vs AI interpretation · never invent a metric,
quote or participant · Jira, Confluence, Outset and Pendo stay draft-only
until a human confirms · never launch recruitment or publish a guide to live
traffic · if a connector this needs is not authorised, say which, say what
the answer loses, and run the rest.
