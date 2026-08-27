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

Ad-hoc quantitative analysis. Skill id is `data-analyze`.

## Integrity

- Query live tools; do not invent series.
- State window, filters (especially filter-test-accounts), and math definition.
- Metrics are **Verified**; “why” text is **AI interpretation** until qual agrees.
- Severity heuristic (Research Insight Monitor): HIGH drop-off >30%, MEDIUM 15–30% — say so explicitly.
- **Quality gate:** If step-from count is tiny (e.g. <30 persons) or drop is 100% with ~0 completing, label **low sample / monitor only** — do not treat as a confirmed problem.

See [references/integrity.md](references/integrity.md) and [references/query-playbook.md](references/query-playbook.md).

## When to use

- “What’s the drop-off between X and Y?”
- Validate or challenge a Research Insight Monitor funnel claim with live PostHog
- Compare MLW / UPS / Login / PublisherPro volumes before a human gate

## Workflow

1. **Clarify the question** — Metric, segment, window, comparison.
2. **Schema first (PostHog)** — `read-data-schema` for events; do not assume names.
3. **Choose tool** — `query-funnel` / `query-trends` / Pendo usage or polls.
4. **Execute minimal query** — Only needed series.
5. **Report** using the template; flag low-N and instrumentation risks.
6. **Bridge** — Qual next → `research-synthesis` or `user-research`.

## Output template

```markdown
# Analysis — [question]

## Answer (Verified)
- Result: …
- Definition: …
- Window / filters: …
- Link / tool: …

## Caveats
- Sample size / instrumentation: …
- Compared to monitor report: agree | disagree | report may be stale

## AI interpretation
- …

## Action for designer
- [ ] Ready for human gate discussion (volume + clear drop)
- [ ] Monitor only (low N or instrumentation suspect)
- [ ] Next: `research-synthesis` | `user-research`
```

## Prompt examples (tested)

1. `Use data-analyze: what's the drop-off from MLW slideout open → link create API → copy button in the last 90 days?`
2. `Use data-analyze: validate PublisherPro manage-links open_linkgen_slideout → affiliate_link_generated. Is the monitor's 100% drop real?`
3. `Use data-analyze: how many partners open UPS details vs open send-proposal modal?`

## Anti-patterns

- Treating 100% drop with <30 starters as a product crisis
- Comparing PostHog persons to Pendo accounts without a conversion note
- Answering “why” from quant alone as fact
