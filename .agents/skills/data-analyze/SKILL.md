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
- **A number with no baseline is not a finding.** Always pull the prior period
  and the step's own history. A 35% drop at a step that has always dropped 35%
  is the design, not a problem.
- Severity heuristic (Research Insight Monitor): HIGH drop-off >30%, MEDIUM
  15–30% — say so explicitly, **and say whether it moved**. The absolute figure
  flags where to look; the change against baseline is what makes it news.
- **Quality gate:** If step-from count is tiny (e.g. <30 persons) or drop is 100%
  with ~0 completing, label **low sample / monitor only** — do not treat as a
  confirmed problem.
- **Quant answers what and how many, never why.** The "why" line is a hypothesis
  for `research-synthesis` or a MICRO study to test, and is labelled as one.
- **Name who is not in the number.** A funnel filtered to one surface, one
  region or one account tier is a claim about those people only.

See [references/integrity.md](references/integrity.md) and [references/query-playbook.md](references/query-playbook.md).

## Known traps in this instance

Two things about the impact.com PostHog that will silently produce a wrong
answer. Both were found the hard way; re-confirm either if the instrumentation
has been changed since.

| Trap | What happens | What to do |
|---|---|---|
| **Membersite runs two SDKs** | Every event is captured **twice**, under different session ids. Counts inflate and session-level dedupe does not work | Dedupe on person + timestamp, not on session. Say in the output which you used, and treat raw session counts as unusable |
| **No native app telemetry** | PostHog "mobile" means **mobile web only**. The iOS and Android apps do not report here | A question about the apps cannot be answered in PostHog. Route to Pendo or Looker and say so rather than returning a web number labelled "mobile" |

*Recorded from Membersite analysis, October 2026.*

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

## Baseline
- Prior period: … · Ordinary swing across the last four periods: …
- Is this move larger than that swing? yes | no | not readable yet

## Caveats
- Sample size / instrumentation: …
- Dedupe basis (person, not session — see known traps): …
- Who is not in this number: …
- Compared to monitor report: agree | disagree | report may be stale

## What this cannot tell you
- Why. Which people. Whether it helped anyone.

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

- **Reporting a figure with no prior period to compare it to**
- **Counting sessions on Membersite** — two SDKs, every session doubled
- **Answering an app question with PostHog "mobile"** — that is mobile web
- Treating 100% drop with <30 starters as a product crisis
- Comparing PostHog persons to Pendo accounts without a conversion note
- Answering “why” from quant alone as fact
