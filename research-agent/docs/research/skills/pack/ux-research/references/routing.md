# UX Research routing

Pick **one primary** child skill. Invoke lenses only when needed.

## Nihal pack (ux-research repo)

| Situation | Invoke |
|---|---|
| New research request / triage / MICRO·SPRINT·DEEP | `research-intake` |
| “What do we know about X?” / critique / record a finding | `user-context` |
| Who are we talking about / persona set | `user-personas` |
| Routed request → study design / Outset draft | `research-planner` |
| Instruments: Pendo guide, interview guide, PostHog dash, audience | `research-builder` |
| Synthetic walk-through before recruiting | `persona-check` |
| Post-ship: did the research hold? | `adoption-check` |
| Quarterly / “is the Frame stale?” | `frame-maintenance` |

## Existing Empathize pack

| Situation | Invoke |
|---|---|
| Quant question, funnel, drop-off | `data-analyze` |
| 2+ sources or monitor triangulated | `research-synthesis` |
| One Dovetail / interview / study export | `synthesize-research` |
| Study plan, gate brief, evidence-gap map | `user-research` |

## Typical sequences

**New ask from PM / designer**

1. `research-intake`
2. If not closed → `user-context` (and `user-personas` if who-matters is unclear)
3. If fieldwork needed → `research-planner` → `research-builder` as needed
4. Empathize pack skills for evidence gaps (`data-analyze` / synthesis / `user-research`)

**Monitor finding deep-dive**

1. `user-context` or `research-synthesis` / `data-analyze`
2. `user-research` gate brief
3. If fieldwork → `research-planner`

**Before usability sessions**

1. `persona-check` (hypotheses only)
2. Existing `test-plan` / `accessibility-review` when in the Design Thinking Test phase

**After ship**

1. `adoption-check` (writes back to the Frame)

## Design Thinking handoff

When the research gate is “problem worth solving,” entice
`design-thinking-ux` at **Define** (`write-spec`) — do not auto-start Ideate.
