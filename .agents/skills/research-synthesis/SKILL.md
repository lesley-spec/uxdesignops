---
name: research-synthesis
description: >-
  Triangulates impact.com UX signals across PostHog, Pendo, Dovetail, Outset,
  and Freshdesk into confidence-scored themes. Use for Empathize cross-source
  synthesis, Research Insight Monitor follow-ups, or when 2+ sources may agree.
license: Proprietary
metadata:
  stage: empathize
  pipeline: impact-ux-designops
  author: impact.com-ux
---

# Research synthesis — cross-source (Empathize)

Use for **multi-source** triangulation. For one Dovetail project / interview set only, use `synthesize-research`.

## Integrity

- Cite every Verified claim with source + link or file path.
- High confidence requires **≥2 independent sources** with **usable evidence** (not empty titles).
- **Reject weak matches:** empty Dovetail `body`/`preview`, NPS comments that only share a keyword (e.g. “link”) but are about payments/signup, or Outset studies that are only a welcome script.
- Separate Brand vs Partner themes.
- Designer owns “problem worth solving.”

See [references/integrity.md](references/integrity.md) and [references/sources.md](references/sources.md).

## When to use

- Monitor flagged an issue as `triangulated: true` — verify that claim
- Need one themed brief before the human gate
- After `data-analyze` finds a real drop and you need qual corroboration

## Workflow

1. **Scope** — Topic, audience, window.
2. **Collect** — Live MCP and/or `research-agent/docs/research/latest.json`.
3. **Normalize** — One row per signal; drop empty/irrelevant matches.
4. **Cluster** — impact taxonomy themes when they fit.
5. **Triangulate** — `high` / `medium` / `low` with honest source counts.
6. **Publish draft** — Gate-ready synthesis (not stakeholder-final).

## Output template

```markdown
# Cross-source synthesis — [topic]
Window: [dates] · Audience: [Brand|Partner|Shared|All]

## Executive take (AI interpretation)
[3–5 sentences]

## Themes

### [Theme] — confidence: high|medium|low
- **Problem statement (draft):** …
- **Verified evidence:**
  - PostHog: … (N=, link)
  - Pendo: “…” (only if on-topic)
  - Dovetail: “…” (non-empty quote + link)
  - Outset: … (study name + what it actually tested)
- **Discarded matches (not evidence):** … (empty DT / off-topic NPS)
- **Open questions:** …

## Ready for human gate?
- High-confidence themes:
- Need fieldwork (`user-research`):
- Suggested next: `user-research` | `data-analyze` | Define handoff
```

## Prompt examples (tested)

1. `Use research-synthesis on UPS Step 2 (details view → send proposal). Is triangulation real or keyword noise?`
2. `Use research-synthesis for Partner Link & Content Tools using the latest research pack + live PostHog if needed.`
3. `Use research-synthesis: Login email→password drop — what evidence survives quality filters?`

## Anti-patterns

- Counting empty Dovetail notes toward high confidence
- Mixing Brand and Partner pain into one “users say” blob
- Promoting monitor `triangulated: true` without re-checking evidence quality
