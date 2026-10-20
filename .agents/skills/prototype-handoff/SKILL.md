---
name: prototype-handoff
description: >-
  Packages a chosen Ideate direction into a Prototype handoff pack after
  ux-critique: decision, mock links, coverage report, open questions, DS notes,
  and epic/one-pager links. Use when the designer is happy with mocks and ready
  to leave Ideate for Prototype.
license: Proprietary
metadata:
  stage: ideate
  pipeline: impact-ux-designops
  author: impact.com-ux
  figjam-agent: Solution Ideator
---

# Prototype handoff (Ideate → Prototype)

Formal exit from Ideate. Runs **after** the designer is happy with mocks and
**after** `ux-critique` (or re-runs critique if missing / stale).

## Integrity

1. Require a recent **`ux-critique`** with no open Critical gaps, or documented designer acceptance of residual risk.
2. Do not invent a “chosen” direction — designer must name it.
3. Label Verified links vs AI summary of the pack.
4. Do **not** auto-start Prototype scaffolder; stop after the pack for designer confirm.
5. **Carry the beliefs forward.** The pack names the claim ids and confidence
   the direction rests on, copied from the one-pager. A prototype that outlives
   the evidence behind it is how a retired claim keeps shipping.
6. **Name what is still unvalidated.** Anything the mocks assume but the
   research has not shown goes in the open questions, not in the confidence of
   the presentation.

See [references/pack.md](references/pack.md).

## When to use

- Designer: “happy with these mocks — hand off to Prototype”
- Need a durable pack for Prototype Scaffolder / eng / PM

## Context gathering (always)

| Source | How |
|---|---|
| Chosen mocks | Figma / FigJam / Make links from designer |
| Last `ux-critique` | Chat output or re-run if missing |
| Framing | One-pager/PRD, epic, tickets |
| DS notes | `design-system` if UI-bound |

## Workflow

1. **Gate** — Confirm designer-named direction + `ux-critique` status.
2. **Assemble pack** — Decision, rejected alternatives (1 line each), annotated mock links, coverage summary, open questions / deferred scope, DS reuse/gaps, framing links.
3. **Designer review** — Show pack; adjust on feedback.
4. **Stop** — On confirm, Ideate is done. Next: the pipeline invokes
   `ux-prototyping` **in this harness** (Cursor, Claude, or Figma Make). Do
   not auto-start that here unless asked. Do not point them at a from-scratch
   Vite app.

## Output template

```markdown
# Prototype handoff — [title]
Status: READY FOR PROTOTYPE (pending designer confirm) | DRAFT
Audience: Brand | Partner | Shared

## Decision
- Chosen direction:
- Why (1–2 lines, tied to JTBD / success criteria):
- Rejected alternatives:
  - D#: … — rejected because …

## Artifacts
- Primary mocks / Figma:
- Supporting FigJam / wires:
- Annotations / flow notes:

## Coverage (from ux-critique)
- Critique date / link:
- Critical open: none | [list + residual risk accepted: yes/no]
- Major deferred:

## Design system
- Reuse:
- Gaps (needs DS review):

## Framing links
- One-pager / PRD:
- Epic / tickets:
- Research (if any):

## Open questions / out of scope for Prototype
- …

## Suggested Prototype next step
- [ ] `ux-prototyping` in this harness (Brand or Partner live preview)
- [ ] Designer confirmed — Ideate complete
```

## Prompt examples

1. `Use prototype-handoff — we picked D3. Last ux-critique is in this chat; mocks: [Figma link].`
2. `Use prototype-handoff after ux-critique; I accept the one Major gap on empty-state copy.`

## Anti-patterns

- Handing off without `ux-critique`
- Multiple “chosen” directions with no primary
- Auto-building a prototype inside this skill
- Dropping epic / one-pager links from the pack
