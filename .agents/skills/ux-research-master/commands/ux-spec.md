---
description: "Turn confirmed research into a one-pager and epic"
argument-hint: "<research link or summary>"
---

Research is confirmed: **$ARGUMENTS**

Draft the one-pager — problem, who it hurts, the evidence behind it, success
measures — and the linked UX epic. Draft only; I will confirm before anything
is published to Confluence or Jira.

## How to run this

Read `.agents/skills/write-spec/SKILL.md` and run its workflow in this chat
(fallbacks: `.claude/skills/write-spec/`, `.cursor/skills/write-spec/`,
`~/.claude/skills/write-spec/`). Do not paraphrase the skill from memory.

Standing rules: label Verified vs AI interpretation · never invent a metric,
quote or participant · Jira, Confluence, Outset and Pendo stay draft-only
until a human confirms · never launch recruitment or publish a guide to live
traffic · if a connector this needs is not authorised, say which, say what
the answer loses, and run the rest.
