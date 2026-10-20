---
description: "The persona set, and which persona owns this problem"
argument-hint: "[problem]"
---

Walk me through the persona set, then tell me which persona owns
**$ARGUMENTS** — their jobs to be done, their workflow around this, and how
confident each claim is. If it spans two personas, say which one it must
satisfy first and why.

## How to run this

Read `.agents/skills/user-personas/SKILL.md` and run its workflow in this chat
(fallbacks: `.claude/skills/user-personas/`, `.cursor/skills/user-personas/`,
`~/.claude/skills/user-personas/`). Do not paraphrase the skill from memory.
Then apply the deeper lens — `brand-operator-ux-persona` for brand side,
`creator-affiliate-ux-persona` for partner side.

Standing rules: label Verified vs AI interpretation · never invent a metric,
quote or participant · Jira, Confluence, Outset and Pendo stay draft-only
until a human confirms · never launch recruitment or publish a guide to live
traffic · if a connector this needs is not authorised, say which, say what
the answer loses, and run the rest.
