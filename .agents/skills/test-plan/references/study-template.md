# Study method — Outset vs Maze

## When to use Outset

- Need **moderated** depth, follow-up probes, or concept reactions
- Complex marketplace workflows (Brand operator decisions, Partner campaign flows)
- Study length > ~10 minutes or multi-step narrative

**Setup notes:** Draft intro, consent, task list, and wrap-up in the test-plan output. Designer creates the study in Outset; use Outset MCP in Cursor when available for study context.

## When to use Maze

- **Unmoderated** click-through on Figma or live URL
- Fast validation of a single flow (3–5 tasks)
- Need completion rate / misclick heatmaps

**Setup notes:** Keep tasks short (one primary goal per task). Prototype must be link-stable. Run `accessibility-review` first — Maze participants won't have a facilitator.

## Hybrid

- Maze for breadth (task success rates) → Outset for depth on failures
- State sequence explicitly in the test plan

## Task-writing rules

1. Anchor each task to a **Verified** success criterion from framing
2. Use realistic JTBD wording — check with persona skills
3. Avoid leading ("Click the blue button to…") unless testing discoverability is the goal
4. Include **success** and **failure** signals per task
5. Cap unmoderated studies at ~5 tasks; Outset can go longer with breaks

## Recruitment heuristics (provisional — label AI)

| Study type | Typical N |
|---|---|
| Qual / Outset concept | 5–8 per audience slice |
| Maze unmoderated | 20–40 for directional signal |
| Shared marketplace | Split or dual sessions — do not collapse Brand + Partner without stating tradeoff |

Always label N as provisional until designer confirms with PM.
