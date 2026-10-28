---
name: design-system
description: >-
  Points Define/Ideate/Prototype work at impact.com UX styleguide and component
  library constraints. Use when writing specs that mention UI, checking
  tokens/components, before on-brand Ideate mocks, or Prototype handoff.
license: Proprietary
metadata:
  stage: define
  pipeline: impact-ux-designops
  author: impact.com-ux
---

# Design system (Define / Ideate)

Lightweight routing skill — does not invent a parallel system.

## Canonical sources

| Resource | Link |
|---|---|
| Styleguide V2 (Figma) | https://www.figma.com/design/Uwg1IvlTgvVA2IvX6WLxOd/Styleguide--V2- |
| Screen DB (existing Brand and Partner screens, each with a Zenix Figma link) | https://docs.superhuman.com/d/Screen-DB_d4K5aqNTMna/All-Screens_suJvIBge#_lucIMxeq |
| Tokens, text styles, component states | [references/styleguide-v2.md](references/styleguide-v2.md) |
| Component library | https://impact.atlassian.net/l/c/yEv0GqPN |
| UX hub | https://impact.atlassian.net/wiki/spaces/ux/overview |

## When to use

- One-pager mentions UI patterns, density, navigation, or components
- Spec should call out reuse vs new pattern
- Before on-brand Ideate mocks (Figma Make / Cursor) or Prototype scaffolder handoff

## Workflow

1. Read [references/styleguide-v2.md](references/styleguide-v2.md). Existing product screens come from the Screen DB, not from the Styleguide file. Open the Zenix Figma link for the area you are changing and duplicate those frames into a new file in the Impact org. Do not edit the Styleguide file or the Zenix source file. Attach the Styleguide (V2) library, theme the file to VNext Light or VNext Dark, and build new UI from those components, variables, and text styles.
2. In the one-pager **Scope** or **Design deliverables**, note: reuse X / gap Y.
3. Do not invent tokens or components. If the library has no match, flag it for the design system owners.

## Output snippet for write-spec

```markdown
## Design system notes
- Reuse: …
- Gaps / new patterns (needs DS review): …
- Figma / library links: …
```
