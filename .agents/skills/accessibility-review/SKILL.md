---
name: accessibility-review
description: >-
  Synthetic accessibility pre-test on a prototype URL or Figma flow before Maze
  or Outset sessions — flags WCAG blockers, focus, labels, contrast, and keyboard
  paths. Use in Test stage pre-flight or when the designer asks for a11y review
  before usability testing.
license: Proprietary
metadata:
  stage: test
  pipeline: impact-ux-designops
  author: impact.com-ux
---

# Accessibility review (Test pre-flight)

Synthetic a11y check **before** user sessions. Complements — does not replace —
manual audit or automated CI. Output is **AI interpretation** until verified
with axe/DevTools or a11y specialist sign-off.

## Integrity

**Lead with the insight, not the evidence.** What the person gets back is
short: the finding, what it changes, and the next thing to do. A few lines, not
a report — they came for a decision, not a download.

**Offer the depth, don't deliver it.** Close with one specific follow-up they
can run — "want the evidence trail behind finding 2?" — not a menu of five. The
detail stays available; it does not arrive unasked.

**A number earns its place by changing a decision.** Everything else goes in the
artifact (the claim, the card, the one-pager) where someone can find it when
they need it.

1. Review the **actual prototype** (URL or Figma frames), not a generic checklist.
2. Label findings **Blocker** (likely WCAG A fail — fix before Maze) vs **Major** vs **Minor**.
3. Call `design-system` when components should come from Styleguide V2.
4. Do not claim WCAG conformance — report likely issues for designer follow-up.
5. **Everything here is a hypothesis to verify, not a finding.** This is a
   synthetic pass over a static artifact. It generates things to check with a
   real assistive-technology user; it does not establish that any of them are
   true for one.
6. **A clean pass is not evidence of accessibility.** No detected issues means
   none were detectable this way. Never report "no a11y issues" — report "no
   issues detectable in a static review", and say what was out of reach.
7. **Name the blockers that must clear before recruiting.** An unmoderated test
   run over a keyboard trap wastes the session and the participant's time.

## What a static review cannot tell you

State these in every output, so nobody reads silence as a pass:

| Out of reach here | Needs |
|---|---|
| Screen-reader announcement order and verbosity | A real screen reader on the built page |
| Keyboard traps in live JS, focus restoration after modals | The running prototype, tabbed by hand |
| Contrast over images, video or dynamic states | Rendered states, not the design file |
| Cognitive load, timeout pressure, error recovery | A participant with the relevant need |
| Whether any of this actually blocks anyone | A session with an AT user |

## When to use

- Test pre-flight inside `test-plan`
- Before publishing an unmoderated Maze test
- Designer asks: "a11y blockers on this prototype?"

## Workflow

1. **Inventory UI** — Screens, forms, modals, tables, nav from prototype link or Figma context.
2. **Keyboard & focus** — Tab order logical? Focus visible? Trap in modals? Skip link?
3. **Labels & names** — Inputs, buttons, icons-only controls, error associations.
4. **Contrast & text** — Body vs Styleguide tokens when visible; flag likely <4.5:1.
5. **Motion & media** — Autoplay, flashing, reduced-motion respect (if applicable).
6. **Marketplace patterns** — Data tables, filters, multi-step wizards common in Brand/Partner UI.
7. **Gate** — Blocker list for `test-plan`; recommend fix or documented accept before Maze.

## Output template

```markdown
# Accessibility review — [prototype]
Artifact: [URL / Figma link]
Scope: synthetic pre-test (not a conformance audit)

## Blockers (fix before unmoderated test)
| Issue | Where | WCAG hint | Suggested fix |
|---|---|---|---|
| … | … | … | … |

## Major / Minor
- …

## Design system
- Components that should map to Styleguide V2: …

## Gate
- [ ] Clear for Maze / Outset recruiting
- [ ] Blockers open — defer test or accept risk: [designer initials/date]
```

## Prompt examples

1. `Use accessibility-review on [prototype URL] — flag blockers before Maze.`
2. `Use accessibility-review on this Figma flow before test-plan.`

## Anti-patterns

- Approving Maze launch with open Blockers unmarked
- Generic WCAG lecture without citing prototype screens
- Claiming "WCAG AA certified" from synthetic review
