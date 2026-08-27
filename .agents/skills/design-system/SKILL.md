---
name: design-system
description: >-
  Points Define/Prototype work at impact.com UX styleguide and component library
  constraints. Use when writing specs that mention UI, checking tokens/components,
  or before Ideate/Prototype handoff.
license: Proprietary
metadata:
  stage: define
  pipeline: impact-ux-designops
  author: impact.com-ux
---

# Design system (Define)

Lightweight routing skill — does not invent a parallel system.

## Canonical sources

| Resource | Link |
|---|---|
| Styleguide (Figma) | https://www.figma.com/file/n3L9jQqoKCgM7Jiems9bQH/Styleguide |
| Component library | https://impact.atlassian.net/l/c/yEv0GqPN |
| UX hub | https://impact.atlassian.net/wiki/spaces/ux/overview |

## When to use

- One-pager mentions UI patterns, density, navigation, or components
- Spec should call out reuse vs new pattern
- Before Prototype scaffolder handoff

## Workflow

1. Open/search styleguide + component library (Figma MCP / Confluence) for existing patterns.
2. In the one-pager **Scope** or **Design deliverables**, note: reuse X / gap Y.
3. Do not invent tokens or components; flag gaps for design system owners.

## Output snippet for write-spec

```markdown
## Design system notes
- Reuse: …
- Gaps / new patterns (needs DS review): …
- Figma / library links: …
```
