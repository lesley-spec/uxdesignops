---
name: design-thinking-ux
description: >-
  Master orchestrator for the impact.com UX Design Thinking pipeline. Walks a
  designer Empathize → Define → Ideate → Prototype → Test: asks intake
  questions, invokes the phase skills (research, write-spec, tickets, ideate,
  prototype shells, test-plan), and stops at each human gate. Use when the user
  says Design Thinking UX, design-thinking-ux, start the pipeline, take me
  through design thinking, walk me through Empathize to Test, or wants a guided
  run from research through usability testing.
license: Proprietary
metadata:
  stage: pipeline
  pipeline: impact-ux-designops
  author: impact.com-ux
  figjam-agent: Design Thinking Pipeline
---

# Design Thinking UX (master)

On-demand **pipeline orchestrator**. First skill to load when a designer wants
the full run. This skill does **not** replace phase skills — it asks questions,
**reads and runs** the skill for the current step, then invites the next phase.

Does **not** skip human gates. Designer confirms “problem worth solving,”
publishing, chosen direction, and recruiting.

Routing tables: [references/phases.md](references/phases.md).

## Integrity

1. **Orchestrate, don’t rewrite.** When this skill says invoke `skill-name`,
   Read `.agents/skills/<name>/SKILL.md` (fallback `.cursor/skills/<name>/`)
   plus any references that step needs, then execute that skill’s workflow in
   **this chat**. Do not ask the designer to type `use skill-name`.
2. **One child skill at a time** unless that skill itself calls another
   (e.g. `test-plan` → `ux-critique` + `accessibility-review`).
3. **Honor the child’s stop.** Publish / Jira / Confluence / Outset / Maze only
   when that skill allows it — after designer confirm.
4. **Label Verified vs AI interpretation.** Never invent metrics or quotes.
5. **Join anywhere.** If artifacts already exist (research, one-pager, epic,
   mocks, prototype), start at that phase. Do not force Empathize from scratch.
6. **Do not auto-advance.** After a phase gate, update the board, **entice**
   the next phase, and wait. “Keep going” still stops at the next gate.
7. **Prototype shells only.** In Prototype, the only allowed setup skills are
   `brand-prototype` (Brand) and `partner-prototype` (Partner). After READY,
   `design-system` may map mocks. Never scaffold Vite/Next/HTML from scratch,
   never treat Figma Make or a chat artifact as the pipeline prototype.

## When to use

- “Use Design Thinking UX” / `design-thinking-ux` / “start the pipeline”
- Designer wants a guided Empathize → Test run
- Unclear which phase skill to start with

If they name a **single** phase skill (`write-spec`, `ideate`, `test-plan`),
run that skill — do not wrap it in this orchestrator unless they also asked
for the full pipeline.

## Session start (always)

1. Show the **pipeline board** (template below). Fill what you already know.
2. **Intake** — batch these (do not drip one-by-one):

   - What are you working on? (flow, product area, hunch, epic, ticket)
   - Audience: **Brand** / **Partner** / **Shared**?
   - Where are you in the pipeline? (start at Empathize, or jump)
   - What do you already have? Research, one-pager/PRD, epic, mocks, prototype, test results — paste or link
   - If Empathize: do you have research, or should I pull / synthesize / plan a study?

3. Locate the phase using [references/phases.md](references/phases.md).
4. Confirm the landing phase in one sentence, then run that phase.

Resume mid-chat from the last open gate + artifacts — don’t re-ask intake.

## Phase loop

For the current phase:

1. Ask only the **phase questions** still unanswered (see below).
2. **Invoke** the child skill(s) from [references/phases.md](references/phases.md).
3. Return the child’s output.
4. Update the pipeline board.
5. **Gate** — if the child says send back a phase, do that; don’t entice forward.
6. **Entice** — when the gate is passed, offer the next phase in one short
   prompt (what you’ll invoke, what they must confirm). Wait for yes.

### Empathize

Ask:

- Existing research? (PostHog, Pendo, Dovetail, Outset, Freshdesk, pack, paste)
- If yes: links / paste — synthesize; don’t redo fieldwork unless gaps remain
- If no: pull live quant (`data-analyze`)? triangulate (`research-synthesis`)?
  affinity-map one corpus (`synthesize-research`)? plan a study (`user-research`)?
- What decision must this unlock?

**Gate:** Designer confirms **problem worth solving** (or explicit override /
monitor-only). Then entice Define: one-pager + UX epic on their confirm.

### Define

Ask (if missing): one-pager vs PM-facing PRD depth; Confluence parent; Jira
project (`UX` default).

Invoke `write-spec` (personas + `anti-sycophancy` + `design-system` per that
skill). Draft first; create Confluence/Jira only after confirm.

**Gate:** Designer happy with framing, then **PM chat** before Ideate. Entice
Ideate after they say the PM chat happened (or they explicitly skip).

### Ideate

Ask: fidelity (sketches / wires / hi-fi); surface; how many directions
(default 3–5); DS-bound vs exploratory.

Invoke `ideate` → designer iterates → `ux-critique` → on chosen direction
`prototype-handoff`.

**Gate:** Designer names the direction; critique has no open Critical (or
accepted residual risk). Entice Prototype: Brand vs Partner shell.

### Prototype

**Exclusive shells.** Invoke `brand-prototype` or `partner-prototype` only —
see [references/phases.md](references/phases.md). Route from intake Audience
(do not re-ask if already Brand or Partner):

- Brand → `brand-prototype`
- Partner / creator-affiliate → `partner-prototype`
- Shared → ask which shell first; the other can run later

If the harness has no local shell (Figma Make, Claude chat): stop and send
them to Cursor. Do not fake a prototype.

The bootstrap script installs Node (if missing) and npm/Vite packages.
Run it with sandbox off (`required_permissions: ["all"]`). Do not ask the
designer to install Node or run `npm install`.

After READY, `design-system` if mapping mocks to UI.

**Gate:** Designer has a runnable URL from the Brand or Partner shell. Entice
Test: pre-flight + Outset/Maze draft.

### Test

Ask: prototype URL; Outset vs Maze vs recommend; sessions already done?

- No sessions → invoke `test-plan` (it runs pre-flight).
- Sessions done → `synthesize-research` then `test-loopback`.

**Gate:** Designer reviews the study before recruiting; reviews loopback
before Confluence/Jira. Pipeline **ends** at published loopback (or a
ready-to-publish test plan if they stop before sessions). Offer a new
Empathize cycle only if findings reframe the problem.

## Pipeline board (keep updated)

```markdown
# Design Thinking UX — [title]
Audience: Brand | Partner | Shared
Phase: Empathize | Define | Ideate | Prototype | Test
Status: INTAKE | IN PHASE | GATE | READY FOR NEXT

## Board
| Phase | Status | Artifacts | Gate |
|---|---|---|---|
| Empathize | todo \| doing \| done \| skipped | … | problem worth solving? |
| Define | todo \| doing \| done \| skipped | … | Designer + PM? |
| Ideate | todo \| doing \| done \| skipped | … | critique + chosen direction? |
| Prototype | todo \| doing \| done \| skipped | … | runnable URL? |
| Test | todo \| doing \| done | … | study reviewed / loopback? |

## Invoked this session
- `skill-name` — why

## Next
- Offer: [next phase / child skill]
- Waiting on designer: [confirm / links / PM chat / sessions]
```

Show the board at start, after each child skill, and at each gate.

## Entice lines (adapt, don’t copy blindly)

- Empathize → Define: “You confirmed this is worth solving. Define next — I’ll draft the one-pager and, if you confirm, create the Confluence page and UX epic. Ready?”
- Define → Ideate: “Framing is signed off. After your PM chat, I can start Ideate (brief + directions). Say the word.”
- Ideate → Prototype: “Direction is chosen and critique is clear. I can bootstrap the Brand or Partner prototype shell. Which surface?”
- Prototype → Test: “Prototype is up. I can run a11y + coverage pre-flight and draft an Outset or Maze study. Go?”
- Test complete: “Loopback is the end of this run. Findings can start a new Empathize cycle if the problem shifted.”

## Prompt examples

1. `Use Design Thinking UX — I'm starting from scratch on Partner UPS Step 2. I don't have research yet.`  
   → Intake → Empathize skills → gate → offer Define (`write-spec` + epic).
2. `Use design-thinking-ux. We already have a one-pager and UX-1234. Jump to Ideate.`  
   → Skip Empathize/Define; invoke `ideate`.
3. `Use Design Thinking UX. Prototype is at localhost:5173 — take me through Test.`  
   → Invoke `test-plan` (pre-flight + study draft). Stop before recruit.

## Check the orchestrator

From repo root: `python3 .agents/skills/design-thinking-ux/scripts/validate.py`

Confirms every child `SKILL.md` loads, markdown links resolve, and the UPS Step 2 Empathize → Test invoke sequence still matches this skill.

## Anti-patterns

- Reimplementing a child skill instead of reading its `SKILL.md`
- Asking the designer to manually invoke the next skill
- Auto-creating Jira/Confluence or publishing to Outset/Maze
- Jumping to mocks before Empathize gate + Define sign-off (unless they joined mid-pipeline)
- Running Empathize → Test in one turn with no gates
- Treating synthetic pre-tests as session findings
- Scaffolding a from-scratch Vite/Next app, or using Figma Make, as the
  Prototype-phase deliverable instead of `brand-prototype` / `partner-prototype`
