---
description: "Build the measure and the audience before we run"
argument-hint: "<feature / flow>"
---

Before we run anything on **$ARGUMENTS**: build the PostHog dashboard that
will tell us whether this moved, draw the audience from real feature usage
rather than a guess, and draft the instruments we will actually need —
interview guide, Pendo guide, screener.

## How to run this

Read `.agents/skills/research-builder/SKILL.md` and run its workflow in this chat
(fallbacks: `.claude/skills/research-builder/`, `.cursor/skills/research-builder/`,
`~/.claude/skills/research-builder/`). Do not paraphrase the skill from memory.
If a Pendo guide is in scope, run `pendo-guide-strategy` first — strategy
before anyone opens the builder.

Standing rules: label Verified vs AI interpretation · never invent a metric,
quote or participant · Jira, Confluence, Outset and Pendo stay draft-only
until a human confirms · never launch recruitment or publish a guide to live
traffic · if a connector this needs is not authorised, say which, say what
the answer loses, and run the rest.
