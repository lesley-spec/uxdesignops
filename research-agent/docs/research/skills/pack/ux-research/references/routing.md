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
| Pull assumptions out of a brief / rank risky guesses | `assumption-mapper` |
| Summarise a mixed folder of raw research material | `study-summary` |
| Compare how competitors handle a user job | `competitive-analysis` |
| Check whether a question is instrumented and measurable | `measurable-check` |
| Check a Rally export / plan who to recruit | `panel-planner` |
| Route an Ideate question to personas, evidence, or fieldwork | `talk-to-users` |
| Expert usability review against Nielsen’s heuristics | `heuristic-evaluation` |
| Plan and size a live online experiment | `ab-test-planner` |
| Publish finished findings to Dovetail, Slack, Confluence, and Jira | `findings-publish` |

## Existing Empathize pack

| Situation | Invoke |
|---|---|
| Quant question, funnel, drop-off | `data-analyze` |
| 2+ sources or monitor triangulated | `research-synthesis` |
| One Dovetail / interview / study export | `synthesize-research` |
| Study plan, gate brief, evidence-gap map | `user-research` |

## Typical sequences

**New ask from PM / designer**

1. If a brief or PRD exists, `assumption-mapper`; otherwise `research-intake`
2. If not closed → `user-context` (and `user-personas` if who-matters is unclear)
3. If fieldwork needed → `research-planner` → `panel-planner` / `research-builder` as needed
4. Empathize pack skills for evidence gaps (`data-analyze` / synthesis / `user-research`)

**Existing research material**

1. Mixed raw files → `study-summary`
2. One corpus needing themes → `synthesize-research`
3. Multiple live sources needing triangulation → `research-synthesis`

**Monitor finding deep-dive**

1. `user-context` or `research-synthesis` / `data-analyze`
2. `user-research` gate brief
3. If fieldwork → `research-planner`

**Before usability sessions**

1. `heuristic-evaluation` (expert hypotheses only)
2. `persona-check` (persona task hypotheses only)
3. Existing `test-plan` / `accessibility-review` when in the Design Thinking Test phase

**Experiment**

1. `measurable-check`
2. `ab-test-planner`
3. After it runs, `adoption-check`

**Finished study**

1. `findings-publish`
2. Record durable claims through `user-context`

**After ship**

1. `adoption-check` (writes back to the Frame)

## Design Thinking handoff

When the research gate is “problem worth solving,” entice
`design-thinking-ux` at **Define** (`write-spec`) — do not auto-start Ideate.
