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
| Styleguide (Figma) | https://www.figma.com/file/n3L9jQqoKCgM7Jiems9bQH/Styleguide |
| Component library | https://impact.atlassian.net/l/c/yEv0GqPN |
| UX hub | https://impact.atlassian.net/wiki/spaces/ux/overview |

## Integrity

1. **Check the live library before claiming reuse.** "This uses existing
   components" is a statement about the current library, not about what you
   remember of it.
2. **Do not invent tokens or components.** A gap is a gap — flag it for the
   design system owners rather than inventing a parallel system in a spec.
3. **On-brand is not the same as usable.** Matching the styleguide says nothing
   about whether the pattern works for the job; that question belongs to
   `test-plan` or `persona-check`.
4. **Date what you checked.** A styleguide reference with no date ages silently
   and will be quoted long after the component changed.

## When to use

- One-pager mentions UI patterns, density, navigation, or components
- Spec should call out reuse vs new pattern
- Before on-brand Ideate mocks (Figma Make / Cursor) or Prototype scaffolder handoff

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
