---
name: synthesize-research
description: >-
  Affinity-maps a single research corpus (one Dovetail project, interview set,
  or study export) into themes and insight cards. Use for Empathize single-source
  synthesis — not cross-tool triangulation (use research-synthesis for that).
license: Proprietary
metadata:
  stage: empathize
  pipeline: impact-ux-designops
  author: impact.com-ux
---

# Synthesize research — single corpus (Empathize)

Affinity / thematic synthesis for **one** dataset. For PostHog + Pendo + Dovetail together, use `research-synthesis`.

## Integrity

- Quotes must be Verified from the corpus with IDs/links when available.
- Skip empty notes; do not invent quote text from titles alone.
- Note N and selection bias; max confidence = **medium** for a single corpus.
- Mark narrative as **AI interpretation**.
- Human gate still applies.

See [references/integrity.md](references/integrity.md) and [references/themes.md](references/themes.md).

## When to use

- One Dovetail project / highlight set
- One Outset study transcript or notes dump
- Designer pastes interview notes and wants affinity themes

## Workflow

1. **Ingest** — Load one corpus; record N.
2. **Open code** — Atomic observations (blocker, workaround, desire…).
3. **Affinity** — 4–8 themes; prefer impact taxonomy labels when they fit.
4. **Insight cards** — observation + quotes + frequency + audience + implication.
5. **Handoff** — If quant needed → `data-analyze`; if multi-source → `research-synthesis`.

## Insight card template

```markdown
### Insight: [short name]
- **Audience:** Brand | Partner | Shared
- **Observation:** …
- **Evidence (Verified):**
  - “…” — id/link
- **Frequency in corpus:** n / N
- **Implication for product:** … (AI interpretation)
- **Confidence:** low | medium
- **Action for designer:** …
```

## Prompt examples (tested)

1. `Use synthesize-research on this Dovetail highlight about commission details findability (paste quote + URL). Affinity for Partner proposals.`
2. `Use synthesize-research on the Brand Marketplace Discovery Outset study summary — themes only, no PostHog.`
3. `Use synthesize-research on these Partner contextual-inquiry notes I pasted — blockers vs desires.`

## Anti-patterns

- Inflating one quote into a roadmap item
- Cross-walking to PostHog inside this skill
- Treating study welcome scripts as findings
