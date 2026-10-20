---
description: "Pressure-test a hypothesis against the evidence"
argument-hint: "<hypothesis>"
---

Hypothesis: **$ARGUMENTS**

What evidence supports it, what argues against it, and what has never been
tested? Give me a confidence call and the cheapest thing that would change
your mind.

## How to run this

Read `.agents/skills/user-context/SKILL.md` and run its workflow in this chat
(fallbacks: `.claude/skills/user-context/`, `.cursor/skills/user-context/`,
`~/.claude/skills/user-context/`). Do not paraphrase the skill from memory.
If the framing itself is the weak part rather than the evidence, continue
into `anti-sycophancy`.

Standing rules: label Verified vs AI interpretation · never invent a metric,
quote or participant · Jira, Confluence, Outset and Pendo stay draft-only
until a human confirms · never launch recruitment or publish a guide to live
traffic · if a connector this needs is not authorised, say which, say what
the answer loses, and run the rest.
