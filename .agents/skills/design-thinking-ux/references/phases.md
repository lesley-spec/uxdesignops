# Phase routing — Design Thinking UX

Use from the orchestrator. Pick **one primary** child skill per step; invoke
lenses (`brand-operator-ux-persona`, `creator-affiliate-ux-persona`,
`design-system`) only when the child skill or audience requires them.

## Locate the landing phase

| Designer has… | Land in |
|---|---|
| Topic / hunch / monitor finding only | **Empathize** |
| Confirmed problem + research (or override) | **Define** |
| One-pager / PRD / epic, ready to explore solutions | **Ideate** |
| Chosen mocks + `ux-critique` (or they accept risk) | **Prototype** (run `prototype-handoff` first if pack is missing) |
| Runnable prototype URL | **Test** |
| Completed Outset/Maze / session notes | **Test** loopback (`synthesize-research` → `test-loopback`) |

If mixed artifacts, choose the **earliest incomplete gate**. Example: one-pager
exists but they never confirmed “worth solving” → Empathize gate first.

Thin framing at Ideate is allowed (`ideate` labels gaps). Thin evidence at
Define is not — send back to Empathize unless they override in writing.

## Empathize — which skill

| Situation | Invoke |
|---|---|
| Quant question, funnel, drop-off, volume | `data-analyze` |
| 2+ sources or monitor `triangulated: true` | `research-synthesis` |
| One Dovetail project, interview set, or study export | `synthesize-research` |
| Need a study plan, gate recommendation, or evidence-gap map | `user-research` |
| Nothing yet | Ask: pull live data, paste a corpus, or plan fieldwork — then the row above |

Typical sequence when starting from a hunch: `data-analyze` (if a metric
exists) → `research-synthesis` or `synthesize-research` → `user-research`
gate brief. Skip steps that are already done.

**Exit:** Designer confirms problem worth solving, **or** monitor-only /
fieldwork-first (do not entice Define).

## Define — which skill

Primary: **`write-spec`**. That skill already gathers FigJam, research pack,
and personas.

Also invoke (same turn as the draft, before publish):

| When | Invoke |
|---|---|
| Always on the one-pager draft | `anti-sycophancy` |
| Audience Brand or Shared | `brand-operator-ux-persona` |
| Audience Partner or Shared | `creator-affiliate-ux-persona` |
| Spec mentions UI / components | `design-system` |

**Exit:** Designer confirms draft → `write-spec` publish (Confluence + UX
Epic). Then PM chat. Do not start `ideate` until they say so.

## Ideate — which skill

| Step | Invoke |
|---|---|
| Start diverge | `ideate` |
| Mid-explore or before handoff | `ux-critique` |
| Designer named a direction + critique OK | `prototype-handoff` |
| On-brand mocks | `design-system` + matching persona |

**Exit:** Handoff pack confirmed. Next is Prototype shells — not more mocks
inside this phase unless they want another round of `ideate`.

## Prototype — which skill

| Audience | Invoke |
|---|---|
| Brand | `brand-prototype` |
| Partner / creator-affiliate | `partner-prototype` |
| Shared | Ask which shell first; can run the other later |
| After shell READY, mapping mocks | `design-system` |

Harness: Cursor or Claude Code (shell). Figma Make cannot clone — follow the
child skill’s harness fallback.

**Exit:** Designer has localhost / deployed prototype URL.

## Test — which skill

| Situation | Invoke |
|---|---|
| Prototype ready, no sessions yet | `test-plan` (runs `ux-critique`, `accessibility-review`, personas) |
| Designer wants a11y only | `accessibility-review` |
| Sessions complete | `synthesize-research` then `test-loopback` |
| Tiny N / unclear if findings are enough | `user-research` gate brief before loopback publish |

**Exit:** Reviewed study draft (if stopping before recruit) **or** published
loopback. That is the end of the pipeline. New Empathize only if findings
reframe the problem.

## Skill paths

Read, in order:

1. `.agents/skills/<name>/SKILL.md`
2. `.cursor/skills/<name>/SKILL.md`
3. `.claude/skills/<name>/SKILL.md`

Then any `references/` files that skill’s current step names.
