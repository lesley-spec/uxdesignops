---
description: "Plan the usability test"
argument-hint: "<prototype URL> + <success criteria>"
---

**$ARGUMENTS**

Draft the usability study — tasks, what each one is actually measuring, the
script, and who we need in the room.

## How to run this

Read `.agents/skills/test-plan/SKILL.md` and run its workflow in this chat
(fallbacks: `.claude/skills/test-plan/`, `.cursor/skills/test-plan/`,
`~/.claude/skills/test-plan/`). Do not paraphrase the skill from memory.
`test-plan` pulls in `persona-check` and `accessibility-review` as the
pre-flight. Run those before recruiting anyone.

Standing rules: label Verified vs AI interpretation · never invent a metric,
quote or participant · Jira, Confluence, Outset and Pendo stay draft-only
until a human confirms · never launch recruitment or publish a guide to live
traffic · if a connector this needs is not authorised, say which, say what
the answer loses, and run the rest.
