---
name: user-research
description: >-
  Plans and deep-dives impact.com UX research before confirming a problem worth
  solving. Use when designing studies, interviewing, probing a Research Insight
  Monitor finding, Outset/Maze prep, or Empathize-stage user research.
license: Proprietary
metadata:
  stage: empathize
  pipeline: impact-ux-designops
  author: impact.com-ux
---

# User research (Empathize)

On-demand Empathize skill. Complements the scheduled **Research Insight Monitor**; does not replace the human gate.

## Integrity (non-negotiable)

1. Prefer **verified** sources (PostHog, Pendo, Dovetail, Outset, Freshdesk) over model recall.
2. Label every claim: `Verified` (linked source) or `AI interpretation` (narration only).
3. Never invent quotes, metrics, or participant counts.
4. Stop at the gate: recommend whether evidence supports a “problem worth solving” — the designer decides.

See [references/integrity.md](references/integrity.md).

## When to use

- Deep-dive one monitor finding before Define
- Draft interview / unmoderated study plans (Outset, Maze)
- Map evidence gaps (what we know vs what we must still ask)
- Reuse for Test-stage study design with the same rigor

## Workflow

1. **Frame the question** — One sentence: who, job-to-be-done, decision this research unlocks.
2. **Inventory evidence** — Pull existing signals (MCP or latest report under `research-agent/docs/research/`). Note audience: Brand / Partner / Shared.
3. **Gap analysis** — List unknowns that block the human gate. Prefer triangulation (`research-synthesis`) before new fieldwork if two sources may already agree.
4. **Method choice**
   - Behavioral / funnel: PostHog (`data-analyze`)
   - In-product voice: Pendo polls / guides
   - Themes & quotes: Dovetail (`synthesize-research` for one project)
   - Live / remote study: Outset or Maze
5. **Plan** — Goals, audience, tasks/script, success metrics, sample size heuristic, ethics/PII note.
6. **Output for the gate** — Short brief the designer can accept/reject (template below).

## Output template

```markdown
# Research brief — [topic]

## Decision this unlocks
[One sentence]

## What we already know (Verified)
- [Claim] — source + link
- …

## AI interpretation (not verified)
- …

## Gaps blocking “problem worth solving”
- …

## Proposed method
- Method:
- Audience (Brand / Partner / Shared):
- Tasks / questions:
- Success criteria:

## Recommendation for human gate
- [ ] Enough evidence to confirm problem
- [ ] Need fieldwork first
- [ ] Deprioritize / monitor only
Rationale (2–4 sentences, cite Verified claims only for go/no-go):
```

## Tool routing

| Need | Prefer |
|---|---|
| Funnels, drop-offs, trends | PostHog MCP → or `data-analyze` |
| In-app polls / NPS-style | Pendo MCP |
| Insights / highlights | Dovetail MCP or API |
| Interactive studies | Outset MCP (no public REST yet) |
| Support volume | Freshdesk via BigQuery agent path |
| Latest weekly pack | `research-agent/docs/research/latest.json` |

## Anti-patterns

- Jumping to solutions or wireframes (that is Ideate / Prototype)
- Treating one quote as prevalence
- Shipping AI summaries to stakeholders without the human gate
