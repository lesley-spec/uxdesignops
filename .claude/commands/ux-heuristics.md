---
description: "Run a heuristic review on this"
argument-hint: "<screen / flow / prototype / frame>"
---

Run a heuristic review on **$ARGUMENTS**.

Ten classic heuristics plus the marketplace ones — two-sided consequence,
money legibility, role truth, scale asymmetry. Rank by consequence, give me
the cheapest fix for each, and tell me what a static frame cannot show you.

## How to run this

Read `.agents/skills/heuristic-review/SKILL.md` and run its workflow in this chat
(fallbacks: `.claude/skills/heuristic-review/`, `.cursor/skills/heuristic-review/`,
`~/.claude/skills/heuristic-review/`). Do not paraphrase the skill from memory.
Expert judgement, never evidence. If the side (brand or partner) or the
task the screen exists to do is missing, ask once — severity cannot be
judged without them.

Standing rules: label Verified vs AI interpretation · never invent a metric,
quote or participant · Jira, Confluence, Outset and Pendo stay draft-only
until a human confirms · never launch recruitment or publish a guide to live
traffic · if a connector this needs is not authorised, say which, say what
the answer loses, and run the rest.

<!-- managed by ux-research-master -->
