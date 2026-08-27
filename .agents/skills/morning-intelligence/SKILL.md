---
name: morning-intelligence
description: >-
  Produces a pre-standup Empathize briefing from the latest Research Insight
  Monitor report (and optional live MCP deltas). Use for morning intelligence,
  daily UX standup prep, or “what changed in research overnight.”
license: Proprietary
metadata:
  stage: empathize
  pipeline: impact-ux-designops
  author: impact.com-ux
---

# Morning intelligence (Empathize)

Fast briefing before standup. Reads the scheduled agent’s latest pack first; only hits live MCPs for gaps or “since yesterday” deltas.

## Integrity

- Lead with **Verified** fields from the report JSON/HTML.
- Keep AI narrative short and labeled.
- Flag high-confidence candidates only when the report already shows multi-source `research_context` or you verify a second source.
- Do not declare problems “confirmed” — list candidates for the human gate.

See [references/integrity.md](references/integrity.md) and [references/report-map.md](references/report-map.md).

## Workflow

1. **Load latest pack**
   - Prefer `research-agent/docs/research/latest.json`
   - Fallback: newest file under `research-agent/docs/research/reports/`
2. **Extract**
   - `generated_at`, `period`, `source_counts`, `summary`
   - Top HIGH severity issues (cap 5–7 for standup)
   - `by_audience` theme rollup
   - Which sources were on/off (`sources` block)
3. **Prioritize** — Severity → users affected → presence of research_context.
4. **Optional delta** — If user asks “since yesterday,” compare to previous report date or run a narrow PostHog/Pendo check via `data-analyze`.
5. **Brief** — Standup card (template). Offer deep-dives via other Empathize skills.

## Standup card template

```markdown
# Morning intelligence — [date]
Report: [generated_at] · Window: [period.label]

## Source health (Verified)
| Source | On? | Volume |
|---|---|---|
| PostHog | | |
| Pendo | | |
| Dovetail | | |
| Outset | | |
| Freshdesk | | |

## Top watchlist
1. **[title]** — [Brand|Partner|Shared] · [severity] · drop [x%] / users [n]
   - Evidence: …
   - Link: …
   - Gate hint: confirm / need deep-dive / monitor

## Audience snapshot
- Brand: …
- Partner: …
- Shared: …

## AI interpretation (60 seconds)
[What to discuss in standup — 3 bullets max]

## Suggested invokes
- `data-analyze` — …
- `research-synthesis` — …
- `user-research` — …
```

## Anti-patterns

- Re-running the full weekly agent during standup
- Dumping all 20+ issues into chat
- Treating missing Pendo (`sources.pendo: false`) as “no user pain”
