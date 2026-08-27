---
name: data-analyze
description: >-
  Runs ad-hoc PostHog and Pendo analysis for impact.com UX Empathize questions
  (funnels, drop-offs, trends, polls). Use when designers ask quantitative
  product questions in Cursor, Claude, or any MCP-enabled harness. Alias: data:analyze.
license: Proprietary
metadata:
  stage: empathize
  pipeline: impact-ux-designops
  author: impact.com-ux
  figjam-alias: data:analyze
---

# Data analyze (Empathize)

Ad-hoc quantitative analysis. FigJam sticky may still say `data:analyze`; skill id is `data-analyze`.

## Integrity

- Query live tools; do not invent series.
- State window, filters (especially filter-test-accounts), and math definition.
- Metrics are **Verified**; “why” text is **AI interpretation** until qual agrees.
- Severity heuristic (align with Research Insight Monitor): HIGH drop-off >30%, MEDIUM 15–30% between funnel steps when using that convention — say so explicitly.

See [references/integrity.md](references/integrity.md) and [references/query-playbook.md](references/query-playbook.md).

## Workflow

1. **Clarify the question** — Metric, segment, window, comparison.
2. **Schema first (PostHog)** — Discover events/properties before querying; do not assume `$pageview` names.
3. **Choose tool**
   - Trends / funnels / retention / paths → PostHog `query-*` tools
   - Named KPI in catalog → data catalog metric run when available
   - Guides / polls / feature usage → Pendo tools
4. **Execute minimal query** — Only needed series and breakdowns.
5. **Report** — Number + definition + link + caveats; optional AI interpretation clearly labeled.
6. **Bridge** — If qual context needed, hand off to `research-synthesis` or `user-research`.

## Output template

```markdown
# Analysis — [question]

## Answer (Verified)
- Result: …
- Definition: …
- Window / filters: …
- Link: …

## Caveats
- …

## AI interpretation
- …

## Suggested next step
- [ ] Triangulate with Dovetail/Pendo (`research-synthesis`)
- [ ] Study design (`user-research`)
- [ ] Enough for human gate discussion
```

## Anti-patterns

- Comparing PostHog unique users to Pendo account counts without conversion note
- Ignoring internal/test filter defaults
- Answering “why” from quant alone as fact
