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

Use this for **multi-source** triangulation. For one Dovetail project or one interview set only, use `synthesize-research` instead.

## Integrity

- Cite every Verified claim with source + link or file path.
- High confidence requires **≥2 independent sources**.
- Separate Brand vs Partner themes; call out Shared carefully.
- Designer owns “problem worth solving.”

See [references/integrity.md](references/integrity.md) and [references/sources.md](references/sources.md).

## Workflow

1. **Scope** — Topic, product area, lookback window, audience filter.
2. **Collect** (in parallel when tools allow)
   - Quant: PostHog funnels / trends (`data-analyze` if deep)
   - In-product voice: Pendo
   - Qual themes/quotes: Dovetail
   - Studies: Outset
   - Support: Freshdesk / BigQuery path
   - Baseline pack: `research-agent/docs/research/latest.json`
3. **Normalize** — One row per signal: claim, source, audience, date, severity/impact, link.
4. **Cluster** — Themes using impact taxonomy when possible (Signup & Onboarding, Login & Access, Marketplace & Discovery, Proposals & Campaigns, Finance & Payments, Link & Content Tools, Settings & Profile, Storefronts & Brand Setup).
5. **Triangulate** — For each theme, count independent sources. Mark confidence:
   - `high` — ≥2 sources agree
   - `medium` — 1 strong source + weak supporting signal
   - `low` — single source or anecdote
6. **Publish draft** — Synthesis doc for the human gate (not stakeholder-final).

## Output template

```markdown
# Cross-source synthesis — [topic]
Window: [dates] · Audience filter: [Brand|Partner|Shared|All]

## Executive take (AI interpretation)
[3–5 sentences; no uncited metrics]

## Themes

### [Theme name] — confidence: high|medium|low
- **Problem statement (draft):** …
- **Verified evidence:**
  - PostHog: … (link)
  - Pendo: …
  - Dovetail: “quote” (link)
  - Other: …
- **Disconfirming evidence:** …
- **Users / impact:** …
- **Open questions:** …

## Ready for human gate?
- Themes at high confidence:
- Themes needing fieldwork (`user-research`):
- Suggested next skill: `user-research` | `data-analyze` | Define handoff
```

## Anti-patterns

- Averaging incompatible metrics across tools without noting definitions
- Treating support tickets as prevalence without rate context
- Mixing Brand and Partner pain into one “users say” blob
