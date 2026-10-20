---
name: write-spec
description: >-
  Turns confirmed Empathize research into an impact.com UX one-pager and linked
  UX Jira epic (Confluence draft + research context). Use for Define-stage
  problem framing, write-spec, one-pager, PRD draft, or Problem Definition
  Generator handoffs after “problem worth solving.”
license: Proprietary
metadata:
  stage: define
  pipeline: impact-ux-designops
  author: impact.com-ux
  figjam-agent: Problem Definition Generator
---

# Write spec (Define)

On-demand Define skill. Implements the FigJam **Problem Definition Generator**:
confirmed research → one-pager (+ optional PRD depth) → auto-linked Jira/Confluence.
Does **not** approve framing — Designer signs off when happy, then chats with a PM before Ideate.

## Integrity

1. Require Empathize gate: designer confirmed **problem worth solving** (or explicit override).
2. Label **Verified** vs **AI interpretation**. Never invent metrics/quotes.
3. Pressure-test with dual marketplace lenses (`brand-operator-ux-persona`, `creator-affiliate-ux-persona`) + `anti-sycophancy`.
4. Draft first; **create Confluence/Jira only after the designer confirms** the draft.
5. Minimize PII in Confluence/Jira.
6. **Atlassian Rovo MCP** — fetch existing tickets/pages with `getJiraIssue` / `search` yourself. Do not ask the designer to paste a Jira issue or run `/mcp` until a tool call fails.
7. **Name the beliefs this rests on, by claim id and confidence.** A spec is a
   bet on what we think is true about users. Writing the claim ids down is what
   lets `frame-maintenance` find this doc when one of them is retired — and
   without it, specs quietly outlive the evidence that justified them.
8. **Match confidence to the commitment.** Building something needs HIGH with
   corroboration; deprioritising something can rest on MEDIUM. A spec whose
   central belief is LOW or UNVALIDATED is a research request wearing a
   one-pager's format — say so rather than shipping it.
9. **Carry what argues against.** The evidence section names who does not have
   this problem, or states that nobody checked.

See [references/integrity.md](references/integrity.md), [references/one-pager.md](references/one-pager.md), [references/publish.md](references/publish.md), [references/atlassian-rovo.md](references/atlassian-rovo.md).

## When to use

- Empathize finding confirmed; need a one-pager + UX epic
- “Write a spec / one-pager / problem statement” for a UX initiative
- Link research pack evidence into Jira so tickets are not orphaned

## Context gathering (always)

Pull before drafting — do not rely on chat memory alone:

| Source | How |
|---|---|
| UX DesignOps FigJam | Figma `get_figjam` on board `slhZ9uzMTmaekjmbEosyzb` (Define column + pipeline) |
| Prior chats | `SearchConversations` for the topic / finding |
| Research pack | `research-agent/docs/research/latest.json` + related HTML report |
| Empathize outputs | Pasted synthesis, or re-run `research-synthesis` / `user-research` briefly if missing |
| Personas | Load `brand-operator-ux-persona` and/or `creator-affiliate-ux-persona`; Confluence Brand UI Personas / Partner Personas |
| Existing specs | Atlassian Rovo MCP `search` in space `ux` + Product Shaping template |
| Named Jira key | `getJiraIssue` immediately — do not ask them to paste the issue |

## Workflow

1. **Gate check** — Confirm problem worth solving. If not, send back to Empathize skills.
2. **Gather** — FigJam + chats + research pack + personas (table above).
3. **Frame** — Problem/opportunity (no solution), audience (Brand / Partner / Shared), JTBD, ranked pains.
4. **Pressure test** — Apply anti-sycophancy: weakest evidence, missing side of marketplace, goal ≠ feature.
5. **Draft one-pager** — Chat markdown using [references/one-pager.md](references/one-pager.md) (UX short form by default; expand to full Product Shaping sections when PM-facing).
6. **Designer review** — Show draft + open questions. Do not publish yet.
7. **Publish (on confirm)** — Confluence page in space `ux` (draft OK) + UX **Epic** with research context and one-pager link. See [references/publish.md](references/publish.md).
8. **Stop** — When the Designer is happy with framing, they chat with a PM before Ideate (`ideate` skill). Do not invent solutions boards.

## Output template (chat draft)

```markdown
# One-pager draft — [title]
Status: DRAFT · Audience: Brand | Partner | Shared
Sources: [FigJam / chat ids / latest.json / Confluence links]

## Problem / opportunity (Verified + AI interpretation labeled)
…

## Audience & JTBD
- Audience:
- Jobs-to-be-done:
- Brand lens:
- Partner / creator-affiliate lens:

## Beliefs this rests on
| Claim id | Statement | Confidence | n | Last verified |
|---|---|---|---|---|
| C… | … | HIGH \| MEDIUM \| LOW | … | … |

If the central belief is LOW or UNVALIDATED, stop and route to
`research-intake` instead of writing around it.

**Who does not have this problem:** … (or: nobody checked)

**What would change this plan:** …

## Evidence (Verified)
- PostHog / Pendo / Dovetail / Outset / Freshdesk — with links
- Discarded / weak evidence:

## Goal (customer + business — not the feature)
…

## Success criteria
- Quant:
- Qual:
- Exit / Designer + PM gate:

## Predicted outcome (what we are betting)
- **Measure:** the one number this should move · **From:** … **to:** …
- **By when:** … · **Agreed with:** … (named decision owner)
- **What would mean this failed:** …

Written before building, not after. This is the prediction
[`adoption-check`](../adoption-check/) checks once it ships — with no figure
recorded here, a post-launch read has nothing to compare against and becomes
storytelling. [`research-builder`](../research-builder/) captures the baseline
for the same measure before anyone starts.

## Scope
- In:
- Out:

## Risks & open questions
…

## Proposed publish
- Confluence: space `ux`, title “…”, parent [UX Roadmap or ask]
- Jira: project `UX`, type Epic, labels e.g. `ux_roadmap`
- [ ] Designer confirmed — ready to create
```

## Prompt examples (tested)

1. `Use write-spec on UPS Step 2 (details → send proposal). Empathize gate OK for draft. Pull FigJam + latest pack; draft only — do not create tickets.`  
   → Draft with Verified ~7110→1810 (−74.5%); weak qual flagged; stops for confirm.
2. `Use write-spec on PublisherPro link gen (14→0). Confirmed worth solving — draft one-pager.`  
   → Should refuse full Define framing (tiny N) → back to Empathize.
3. `Use write-spec: turn this Empathize synthesis into a Confluence one-pager under Impact UX and a linked UX Epic — ask me before creating.`

## Anti-patterns

- Jumping to Ideate / mocks inside the one-pager “Approach” before Designer sign-off and a PM chat
- Creating Jira/Confluence without an explicit confirm
- Asking the designer to paste a Jira issue or enable Atlassian Rovo before calling the MCP tools
- Collapsing Brand and Partner into one “users” statement
- One-pagers with no Verified research links (violates “100% tickets with research context”)
