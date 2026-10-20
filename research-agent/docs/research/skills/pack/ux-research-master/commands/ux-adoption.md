---
description: "Post-launch: did the research hold?"
argument-hint: "<what shipped, and when>"
---

We shipped **$ARGUMENTS**

Read the baseline from the Frame, re-run the measure in PostHog, and tell me
whether the research held. Write the outcome back as a claim.

## How to run this

Read `.agents/skills/adoption-check/SKILL.md` and run its workflow in this chat
(fallbacks: `.claude/skills/adoption-check/`, `.cursor/skills/adoption-check/`,
`~/.claude/skills/adoption-check/`). Do not paraphrase the skill from memory.
Write the claim back either way. A miss is evidence.

Standing rules: label Verified vs AI interpretation · never invent a metric,
quote or participant · Jira, Confluence, Outset and Pendo stay draft-only
until a human confirms · never launch recruitment or publish a guide to live
traffic · if a connector this needs is not authorised, say which, say what
the answer loses, and run the rest.
