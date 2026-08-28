---
name: ux-critique
description: >-
  Checks Ideate mocks and concepts against one-pager, PRD, epic, tickets, and
  notes — coverage matrix plus solution-quality critique. Use mid-Ideate or
  before prototype-handoff or Test pre-flight when the designer asks to critique,
  pressure-test concepts, or confirm framing issues are covered (UX Critique agent).
license: Proprietary
metadata:
  stage: ideate
  pipeline: impact-ux-designops
  author: impact.com-ux
  figjam-agent: UX Critique
---

# UX critique (Ideate)

Coverage + concept critique for solution exploration. Distinct from
`anti-sycophancy` (which pressure-tests **problem framing** in Define).

## Integrity

1. Critique against **stated framing sources** (one-pager / PRD / epic / tickets / notes). Do not invent requirements.
2. Label **Verified** source items vs **AI interpretation** of gaps.
3. Dual marketplace: call `brand-operator-ux-persona` / `creator-affiliate-ux-persona` when audience is Brand, Partner, or Shared.
4. Call `design-system` when mocks claim on-brand / component reuse.
5. **Required before** `prototype-handoff`: no open Critical gaps, or designer explicitly accepts residual risk.

See [references/coverage.md](references/coverage.md).

## When to use

- Mid-Ideate: kill weak directions early
- Before Prototype: designer thinks mocks are ready
- Test pre-flight: prototype vs framing before Outset/Maze (`test-plan` step 2)
- “Did we cover the PRD / epic / tickets / notes?”

## Context gathering (always)

| Source | How |
|---|---|
| Framing pack | One-pager/PRD, epic, tickets, notes used in `ideate` |
| Current concepts / mocks | Pasted links (Figma/FigJam), screenshots, or chat wires |
| Personas / DS | Persona skills + `design-system` as needed |

## Workflow

1. **Inventory framing items** — Extract material claims: problems, requirements, success criteria, ticket ACs, noted constraints. Prefer one-pager/PRD; include tickets and notes.
2. **Map to mocks** — For each item: addressed / partial / missing; cite where (frame, flow, annotation).
3. **Quality pass** — Off-problem polish? One-sided marketplace? Feature-as-goal sneaking back? DS invent vs reuse?
4. **Severity** — Critical (blocks handoff) / Major / Minor.
5. **Gate** — Ready for `prototype-handoff`, revise mocks, or back to `ideate` for more divergence.

## Output template

```markdown
# UX critique — [title]
Sources: [one-pager / PRD / epic / tickets / notes]
Artifacts reviewed: [Figma / FigJam / chat wires]

## Coverage matrix
| Framing item | Status | Where in mocks | Gap / risk | Severity |
|---|---|---|---|---|
| … | addressed \| partial \| missing | … | … | Critical \| Major \| Minor |

## Keep
- …

## Challenge
- …

## Marketplace / DS
- Brand lens:
- Partner lens:
- Design system: reuse … / gaps …

## Gate recommendation
- [ ] Ready for `prototype-handoff` (no open Critical, or residual risk accepted)
- [ ] Revise mocks — then re-run `ux-critique`
- [ ] Back to `ideate` (need more directions)
```

## Prompt examples

1. `Use ux-critique on these three Figma directions vs the UX-1234 one-pager + epic tickets.`
2. `Use ux-critique before handoff — here's the PRD and mock links. Flag anything Critical.`
3. `Use ux-critique mid-Ideate on D2 vs Granola notes — is this off-problem?`

## Anti-patterns

- Softening Critical gaps to be “helpful”
- Approving handoff with uncovered ticket ACs unmarked
- Confusing with `anti-sycophancy` (re-litigating whether the problem exists)
- Inventing PRD requirements not in sources
