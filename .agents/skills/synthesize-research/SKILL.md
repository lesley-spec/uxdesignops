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

- Quotes must be Verified (from the corpus) with IDs or links when available.
- Note sample size and selection bias; do not generalize to all users.
- Mark synthesis narrative as **AI interpretation**.
- Human gate still applies before Define.

See [references/integrity.md](references/integrity.md).

## Workflow

1. **Ingest** — Load project/notes/highlights (Dovetail MCP, export, or pasted transcript set). Record N participants / highlights.
2. **Open code** — Tag atomic observations (behavior, attitude, blocker, workaround, desire).
3. **Affinity** — Cluster into 4–8 themes. Prefer impact taxonomy labels when they fit ([references/themes.md](references/themes.md)).
4. **Insight cards** — Per theme: observation, evidence quotes, frequency, audience, implication.
5. **Confidence** — Single corpus = max `medium` unless the designer already triangulated elsewhere.
6. **Handoff** — If quant or second qual source exists, point to `research-synthesis` next.

## Insight card template

```markdown
### Insight: [short name]
- **Audience:** Brand | Partner | Shared
- **Observation:** …
- **Evidence (Verified):**
  - “…” — participant/highlight id or link
  - …
- **Frequency in corpus:** n / N
- **Implication for product:** … (AI interpretation)
- **Confidence:** low | medium
```

## Deliverable shape

```markdown
# Synthesis — [project / study name]
Corpus: [source] · N= · Dates:

## Themes overview
| Theme | Frequency | Audience | Confidence |
|---|---|---|---|

## Insight cards
…

## Gaps / next research
…
```

## Anti-patterns

- Inflating one vivid story into a roadmap item without frequency
- Cross-walking to PostHog inside this skill (switch to `research-synthesis`)
- Dropping contradictory notes
