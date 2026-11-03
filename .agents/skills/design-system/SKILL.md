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
| Page Templates (read, then duplicate into the working file) | https://www.figma.com/design/Uwg1IvlTgvVA2IvX6WLxOd/Styleguide--V2-?node-id=5314-16 |
| Tokens, text styles, component states | [references/styleguide-v2.md](references/styleguide-v2.md) |
| Component library | https://impact.atlassian.net/l/c/yEv0GqPN |
| UX hub | https://impact.atlassian.net/wiki/spaces/ux/overview |

## When to use

- One-pager mentions UI patterns, density, navigation, or components
- Spec should call out reuse vs new pattern
- Before on-brand Ideate mocks (Figma Make / Cursor) or Prototype scaffolder handoff

## Workflow

1. Read [references/styleguide-v2.md](references/styleguide-v2.md). Do not fetch the Screen DB. The current screen is the Figma link the person shares, or a screenshot if they have no link. Do not edit the Styleguide file, Page Templates, or that source file. Ask whether they already have a working Figma file and will share the link, or whether to create a new one. Create a file only after they say yes. Read Page Templates (`5314:16` in `Uwg1IvlTgvVA2IvX6WLxOd`), duplicate the closest template into the working file, and duplicate their source frame there too when they shared a link. Attach the Styleguide (V2) library, theme the file to VNext Light or VNext Dark, and build from those components, variables, and text styles. Rebind any raw hex. Do not sample a hex from a screenshot.
2. In the one-pager **Scope** or **Design deliverables**, note: reuse X / gap Y.
3. Do not invent tokens or components. If the library has no match, flag it for the design system owners.

## Output snippet for write-spec

```markdown
## Design system notes
- Reuse: …
- Gaps / new patterns (needs DS review): …
- Figma / library links: …
```
