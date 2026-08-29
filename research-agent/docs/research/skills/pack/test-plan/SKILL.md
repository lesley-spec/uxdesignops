---
name: test-plan
description: >-
  Drafts Outset or Maze usability studies from a prototype plus one-pager success
  criteria; orchestrates synthetic pre-tests before recruiting. Use in Test stage
  after Prototype is ready, or when the designer asks for a test plan, study script,
  or session guide (Test Plan Generator).
license: Proprietary
metadata:
  stage: test
  pipeline: impact-ux-designops
  author: impact.com-ux
  figjam-agent: Test Plan Generator
---

# Test plan (Test)

On-demand Test skill. Implements the FigJam **Test Plan Generator**:
problem + prototype → drafted study in **Outset** or **Maze**, after synthetic
pre-tests. Does **not** auto-publish or recruit — designer reviews first.

## Integrity

1. Require a **prototype link** (Figma, localhost shell, or Maze-ready URL).
2. Anchor tasks and success criteria to **Verified** framing (one-pager / PRD / epic).
3. Run synthetic pre-flight before drafting the study (see Workflow step 2).
4. Label **Verified** vs **AI interpretation** in every output.
5. **Stop at the human gate** — do not publish to Outset/Maze or share with stakeholders without designer confirm.
6. After real sessions, loop findings to Empathize via `synthesize-research` — never treat this skill's draft as verified research.

See [references/integrity.md](references/integrity.md).

## When to use

- Prototype is ready; need an Outset or Maze study draft
- “Test this prototype” / “draft usability study” / “session guide”
- Pre-flight before scheduling participants

## Context gathering (always)

| Source | How |
|---|---|
| Prototype | Figma / localhost / handoff pack URL from designer |
| Framing | One-pager / PRD, epic, tickets, prototype-handoff pack |
| Pre-tests | Recent `ux-critique`, `accessibility-review` (re-run if missing) |
| Audience | Brand / Partner / Shared — drives persona skills + recruitment |

## Workflow

1. **Gate** — Confirm prototype URL + framing sources. If no prototype, stop → back to Prototype.
2. **Synthetic pre-flight** — Before drafting the study:
   - `ux-critique` on prototype vs framing (pre-test mode — flag Critical blockers)
   - `accessibility-review` on prototype URL (flag blockers before Maze)
   - `brand-operator-ux-persona` / `creator-affiliate-ux-persona` when audience is Brand, Partner, or Shared
   - Summarize blockers; if Critical a11y/coverage gaps, recommend fix before recruiting unless designer accepts risk.
3. **Method pick** — Recommend Outset vs Maze (see [references/study-template.md](references/study-template.md)).
4. **Draft study** — Goals, screener, tasks, success metrics, facilitator script, recruitment notes, PII handling.
5. **Designer review** — Show full pack; adjust on feedback.
6. **Stop** — On confirm, create an Outset **draft** study (do not publish, do not launch recruitment). Next after real sessions: `test-loopback` (or `synthesize-research` then `test-loopback`).

## Outset connection

| Path | What it can do |
|---|---|
| `OUTSET_API_KEY` (v1 REST) | List/read studies. **Cannot** create guides. |
| Outset MCP `https://api.outset.ai/mcp/` (OAuth `studies:write`) | Create/edit draft studies, sections, questions. |

When the designer asks to publish the test to Outset:

1. Use MCP `create_project` / `create_study` / `create_section` / `create_question`.
2. Label the study **PIPELINE TEST** if this is a pipeline demonstration.
3. Leave the study **draft** (`validate_study` is OK). Do **not** call `publish_study`, `configure_recruitment`, or anything under the `studies:launch` scope unless the designer explicitly asks to recruit.
4. Link the Outset URL on the Confluence plan and UX Research ticket.

## Output template

```markdown
# Test plan — [title]
Status: DRAFT (pending designer review) | READY TO PUBLISH
Audience: Brand | Partner | Shared
Method: Outset | Maze | hybrid

## Prototype under test
- URL:
- Framing links (one-pager / epic):

## Pre-flight summary (synthetic)
| Check | Status | Blockers |
|---|---|---|
| ux-critique | pass \| defer \| fail | … |
| accessibility-review | pass \| defer \| fail | … |
| Persona task realism | pass \| notes | … |

## Study goals (from Verified success criteria)
1. …

## Research questions
- …

## Participants
- Profile / screener:
- Target N: (heuristic — state if provisional)
- Recruitment notes:

## Tasks (think-aloud)
1. **Task:** …
   - Success: …
   - Probe if stuck: …

## Success metrics
- Task completion / time-on-task / SUS or custom:
- What would confirm or kill the direction:

## Facilitator script (Outset) / Maze setup notes
- Intro:
- Consent / recording:
- Wrap-up questions:

## Out of scope for this round
- …

## Human gate
- [ ] Designer reviewed AI draft
- [ ] Blockers accepted or resolved
- [ ] Ready to publish to Outset/Maze

## After sessions (loop-back)
- `test-loopback` — publish Verified findings to Confluence/Jira (after designer confirm)
- Or run `synthesize-research` first, then `test-loopback`
```

## Prompt examples (tested)

1. `Use test-plan for [prototype link] from the one-pager success criteria — Outset, Partner audience.`
2. `Use test-plan after prototype-handoff; run pre-flight then draft Maze study.`
3. `Use test-plan on localhost:5173 shell — epic UX-1234; flag anything that blocks recruiting.`

## Anti-patterns

- Publishing to Outset/Maze without designer review
- Tasks not tied to Verified success criteria
- Skipping pre-flight when prototype changed since last critique
- Treating AI-drafted study results as Empathize evidence
- Recruiting when Critical a11y blockers are open (unless risk accepted in writing)
