---
name: ux-research
description: >-
  Master UX research orchestrator for impact.com. Routes research requests
  through intake, the Frame (user-context), personas, planning/builder skills,
  and the Empathize pack (user-research, research-synthesis, synthesize-research,
  data-analyze). Use when the user says ux-research, /ux-research, start
  research, research request, what do we know, triage this study, or wants the
  full research skill set rather than a single phase skill.
license: Proprietary
metadata:
  stage: pipeline
  pipeline: impact-ux-designops
  author: impact.com-ux
  figjam-agent: UX Research
---

# UX Research (master)

On-demand **research orchestrator**. Loads when someone wants research done
well — not when they only named a single child skill.

Does **not** replace child skills. Reads and runs one child at a time, then
entices the next step. Stops at human gates (route confirm, study launch,
problem-worth-solving).

Child routing: [references/routing.md](references/routing.md).

## Integrity

1. **Orchestrate, don’t rewrite.** When this skill says invoke `skill-name`,
   Read `.agents/skills/<name>/SKILL.md` (fallback `.cursor/skills/<name>/`)
   plus any references that step needs, then execute that skill’s workflow in
   **this chat**.
2. **One child skill at a time** unless that skill itself calls another.
3. **Check the Frame before planning fieldwork.** Prefer
   `research-intake` → `user-context` over jumping to a new study.
4. **Label Verified vs AI interpretation.** Never invent metrics or quotes.
5. **Honor child stop conditions.** Do not launch Outset recruitment or create
   Jira tickets unless the child skill allows it after designer confirm.
6. **Join anywhere.** If they already have a routed request, Frame answer, or
   study plan, start at that step.

## When to use

- “Use `ux-research`” / `/ux-research` / “start research”
- Research request, triage, “what do we already know”
- Unclear which research skill to start with

If they named a **single** child (`research-intake`, `user-context`,
`user-research`, …), run that skill directly — do not wrap it unless they also
asked for the full research run.

## Session start (always)

0. If sibling research skills are missing, invoke `ux-install-all-skills` first.
1. Show the **research board** (template below). Fill what you already know.
2. **Intake** — batch these:

   - What decision does this unlock?
   - Audience: Brand / Partner / Shared?
   - Do you already have a Frame answer, Dovetail link, PostHog insight, or study?
   - Is this a new request, a deep-dive on a monitor finding, or post-ship check?

3. Route with [references/routing.md](references/routing.md). Confirm the
   landing skill in one sentence, then run it.

## Default path

```
research-intake  →  (already answered? stop with Frame link)
                 →  user-context / user-personas as needed
                 →  research-planner (+ research-builder)
                 →  user-research / research-synthesis / data-analyze / synthesize-research
                 →  (after ship) adoption-check
                 →  (quarterly) frame-maintenance
```

Prototype / Test lenses from Nihal’s pack when relevant:
`persona-check` (synthetic pre-test), `adoption-check` (post-launch).

## Research board

```markdown
# UX Research — [title]
Audience: Brand | Partner | Shared
Step: Intake | Frame | Plan | Empathize pack | Pre-test | Adoption
Status: INTAKE | IN STEP | GATE | DONE

## Board
| Step | Status | Artifacts | Gate |
|---|---|---|---|
| Intake (`research-intake`) | | | Route MICRO/SPRINT/DEEP or closed |
| Frame (`user-context`) | | | Gaps named |
| Personas (`user-personas`) | | | Persona named if needed |
| Plan (`research-planner` / `research-builder`) | | | Study + instruments ready |
| Empathize pack | | | Problem-worth-solving / fieldwork |
| Pre-test (`persona-check`) | | | Hypotheses only |
| Adoption (`adoption-check`) | | | Outcome written to Frame |

## Next
[one sentence]
```

## Site

- Frame (DesignOps): `https://lesley-spec.github.io/uxdesignops/frame/`
- Claude live Ask: https://claude.ai/artifact/FHc7oAPoyohgxo87VdxCGw
- Insight Monitor: `https://lesley-spec.github.io/uxdesignops/research/`
