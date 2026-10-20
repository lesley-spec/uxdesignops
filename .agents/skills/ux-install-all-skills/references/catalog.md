# Pipeline skill catalog (30)

The installer **must** land every name below. Personas and `design-system`
are listed once; they are reused in later phases.

## Pipeline (master)

| Skill | Use when |
|---|---|
| `ux-research-master` | **Front door.** Installs everything, routes any message, owns the `/ux-*` prompts |
| `design-thinking-ux` | Guided Empathize → Test; invokes the phase skills |
| `ux-research` | Guided research run; invokes research + Frame skills |

## Empathize / Research

| Skill | Use when |
|---|---|
| `research-intake` | Triage a research request (MICRO / SPRINT / DEEP) |
| `user-context` | Ask / critique / record against the Frame |
| `user-personas` | Partner + Brand persona set |
| `research-planner` | Design a routed study |
| `research-builder` | Pendo / interview / PostHog / audience instruments |
| `frame-maintenance` | Quarterly Frame staleness check |
| `user-research` | Study plan, deep-dive, or “problem worth solving” gate |
| `research-synthesis` | Triangulate PostHog + Pendo + Dovetail (+ Outset/Freshdesk) |
| `synthesize-research` | Affinity-map one corpus |
| `data-analyze` | Ad-hoc PostHog / Pendo quantitative questions |

## Define

| Skill | Use when |
|---|---|
| `write-spec` | One-pager + linked UX epic (after confirm) |
| `anti-sycophancy` | Pressure-test framing |
| `brand-operator-ux-persona` | Brand-side JTBD / operator lens |
| `creator-affiliate-ux-persona` | Partner / creator-affiliate lens |
| `design-system` | Styleguide + component library |

## Ideate

| Skill | Use when |
|---|---|
| `ideate` | Ideation brief + starter directions |
| `ux-critique` | Coverage matrix vs one-pager / PRD / epic |
| `heuristic-review` | Expert usability pass: ten classic heuristics + the marketplace five |
| `prototype-handoff` | Chosen direction → Prototype pack |

## Prototype

| Skill | Use when |
|---|---|
| `ux-prototyping` | Any harness → Brand or Partner live preview |
| `brand-prototype` | Brand UI shell on localhost |
| `partner-prototype` | Partner UI shell on localhost |
| `persona-check` | Synthetic persona walk-through before recruiting |

## Test

| Skill | Use when |
|---|---|
| `test-plan` | Synthetic pre-flight + Outset/Maze draft |
| `accessibility-review` | Synthetic a11y before recruiting |
| `test-loopback` | Verified session findings → Empathize |
| `adoption-check` | Post-ship: did the research hold? |

After install, start with `design-thinking-ux` for the full pipeline, or
`ux-research` for research-only.
