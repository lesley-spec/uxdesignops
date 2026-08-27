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

## Integrity

1. Prefer verified sources over model recall.
2. Label **Verified** vs **AI interpretation**.
3. Never invent quotes, metrics, or participant counts.
4. Stop at the gate — recommend; designer decides.
5. If quant N is tiny or qual matches are empty/off-topic, recommend **fieldwork or monitor**, not “confirm problem.”

See [references/integrity.md](references/integrity.md).

## When to use

- Deep-dive one monitor finding before Define
- Turn a synthesis into a study plan (Outset / Maze)
- Map evidence gaps blocking the human gate

## Workflow

1. **Frame** — Who, JTBD, decision unlocked.
2. **Inventory** — Report + MCP; note Brand / Partner / Shared.
3. **Gaps** — Prefer `research-synthesis` / `data-analyze` before new fieldwork if sources may already agree.
4. **Method** — PostHog / Pendo / Dovetail / Outset / Maze as appropriate.
5. **Plan** — Goals, tasks, success criteria, N heuristic, PII note.
6. **Gate brief** — Template below with a clear recommendation.

## Output template

```markdown
# Research brief — [topic]

## Decision this unlocks
[One sentence]

## What we already know (Verified)
- …

## AI interpretation
- …

## Gaps blocking “problem worth solving”
- …

## Proposed method
- Method / audience / tasks / success criteria:

## Recommendation for human gate
- [ ] Enough evidence to confirm problem
- [ ] Need fieldwork first
- [ ] Deprioritize / monitor only
Rationale (cite Verified only):

## Action for designer (next 24h)
1. …
2. …
```

## Prompt examples (tested)

1. `Use user-research on MLW: 32% drop slideout→create and 46% overall to copy. Do we have enough to confirm a problem, or design an Outset study?`
2. `Use user-research on PublisherPro link gen (14 open → 0 generated). Gate recommendation + study plan if needed.`
3. `Use user-research for UPS details→send proposal (large Partner volume). What must we still ask before Define?`

## Anti-patterns

- Jumping to Ideate solutions
- Confirming a problem on low-N or empty triangulation
- Shipping AI summaries past the human gate
