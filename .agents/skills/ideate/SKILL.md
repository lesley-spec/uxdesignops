---
name: ideate
description: >-
  Starts Ideate from framing (one-pager/PRD preferred; epic, tickets, Granola,
  or notes OK): prompts for fidelity/tool, emits an ideation brief, and seeds
  wireframe or mock directions. Use for Ideate-stage divergence, solution
  brainstorming, wireframes, mock variations, or Solution Ideator handoffs.
license: Proprietary
metadata:
  stage: ideate
  pipeline: impact-ux-designops
  author: impact.com-ux
  figjam-agent: Solution Ideator
---

# Ideate (diverge)

On-demand Ideate skill. Implements the FigJam **Solution Ideator**:
framing in → ideation brief + tool routing → starter concepts / wires / mock prompts.
Does **not** pick a final direction — designer iterates, then runs `ux-critique` before
`prototype-handoff`.

## Integrity

1. Prefer a **one-pager or detailed PRD**; accept epic, tickets, Granola/meeting notes, Slack, or chat paste. If framing is thin, build a **Framing snapshot**, label gaps, warn — do not block.
2. Label **Verified** vs **AI interpretation**. Never invent metrics/quotes from framing sources.
3. Prompt the designer for **fidelity**, **surface**, and **# of directions** before generating visuals.
4. Dual marketplace: Brand and/or Partner lenses via personas when audience is known.
5. Stop short of Prototype pack — that is `prototype-handoff` after `ux-critique`.
6. **Directions are options, not answers.** Generating five concepts does not
   make any of them right, and the one that renders best is not thereby the
   strongest. The designer chooses; `ux-critique` checks it against the framing.
7. **Never let a concept invent a user need.** If a direction depends on a need
   the framing does not evidence, say so on the concept rather than in a
   footnote — that is a research question, and `research-intake` owns it.

See [references/brief.md](references/brief.md), [references/routing.md](references/routing.md).

## When to use

- Designer (+ PM chat) ready to explore solutions
- “Ideate / brainstorm / wireframe / mock variations” from a spec or notes
- Need a brief before FigJam, Figma Make, Cursor, Claude, or Google Stitch

## Context gathering (always)

Pull before diverging — do not rely on chat memory alone:

| Source | How | Preference |
|---|---|---|
| One-pager / PRD | Confluence (space `ux`) or pasted markdown | Preferred |
| UX Epic + tickets | Atlassian / Jira project `UX` | Preferred with one-pager |
| Meeting / Granola notes | Pasted notes or linked doc | Acceptable |
| Prior chats | `SearchConversations` for topic / epic | Fallback |
| UX DesignOps FigJam | Figma `get_figjam` on board `slhZ9uzMTmaekjmbEosyzb` (Ideate column) | Pipeline context |
| Personas / DS | `brand-operator-ux-persona`, `creator-affiliate-ux-persona`, `design-system` | When UI-bound |

## Workflow

1. **Intake** — Collect whatever framing exists. Prefer one-pager/PRD; if only notes, snapshot problem / audience / JTBD / constraints / open questions and list gaps.
2. **Prompt designer** — Ask (batch): fidelity (sketches / wires / hi-fi); surface (FigJam / Claude / Cursor / Figma Make / Figma agent / Stitch); how many directions (default 3–5); DS-bound vs exploratory.
3. **Ideation brief** — Jobs, constraints, non-goals, success criteria snippets, evidence anchors. See [references/brief.md](references/brief.md).
4. **Route** — Recommend surface per [references/routing.md](references/routing.md). Styleguide-aware → Figma Make or Cursor + `design-system`; wires/thinking → Claude or FigJam; visual variations → Figma agent / Stitch after brief exists.
5. **Diverge** — Emit 3–5 concept directions (text + optional lo-fi wires or tool-ready prompts). Label AI mocks as exploration.
6. **Stop** — Point designer to iterate in chosen tool, then `ux-critique` on shortlist. Do not declare a chosen solution or run Prototype handoff.

## Output template (chat)

```markdown
# Ideation brief — [title]
Status: DIVERGING · Audience: Brand | Partner | Shared
Sources: [one-pager / PRD / epic / tickets / notes / chat ids]
Framing quality: Strong (one-pager/PRD) | Partial | Thin (notes only — gaps listed)

## Framing snapshot
- Problem / opportunity:
- JTBD:
- Constraints / non-goals:
- Gaps in framing:

## Designer choices
- Fidelity:
- Surface:
- # directions:
- DS-bound: yes | no | mixed

## Directions (AI exploration)
### D1 — [name]
- Concept:
- Addresses (from framing):
- Risk:

### D2 — …
…

## Next
- Iterate in [surface]
- When shortlisted: run `ux-critique`
- When happy with mocks: run `prototype-handoff`
```

## Prompt examples

1. `Use ideate on UX-1234 — pull Confluence one-pager + epic. I want 4 wireframe directions in Claude first.`
2. `Use ideate from these Granola notes (no one-pager yet). Snapshot framing, warn on gaps, then 3 FigJam concepts.`
3. `Use ideate: we have a PRD — recommend tool for on-brand mock variations, then seed Figma Make prompts.`

## Anti-patterns

- Generating hi-fi mocks before asking fidelity/surface
- Treating notes-only intake as a signed PRD without labeling gaps
- Declaring a winning direction or skipping `ux-critique`
- Jumping to Prototype scaffolder inside Ideate
