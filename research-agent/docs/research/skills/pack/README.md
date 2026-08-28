# Design Thinking skills (impact.com UX DesignOps)

Portable [Agent Skills](https://agentskills.io/specification) for the [UX DesignOps FigJam](https://www.figma.com/board/slhZ9uzMTmaekjmbEosyzb/UX-DesignOps).

Canonical source: `.agents/skills/` (open standard). Cursor discovers them via symlinks in `.cursor/skills/`.

## Empathize (stage 1)

| Skill | Use when |
|---|---|
| `user-research` | Deep-dive a finding, design a study, or decide if a problem is worth solving |
| `research-synthesis` | Triangulate across PostHog + Pendo + Dovetail (+ Outset/Freshdesk) |
| `synthesize-research` | Affinity / theme a **single** corpus (one Dovetail project, one interview set) |
| `data-analyze` | Ad-hoc PostHog or Pendo quantitative questions (FigJam label was `data:analyze`) |

**Agent (scheduled):** Research Insight Monitor in `research-agent/` — on-demand layer is the skills above.

**Human gate:** Designer confirms the problem is worth solving. Skills recommend; they do not decide.

## Define (stage 2)

| Skill | Use when |
|---|---|
| `write-spec` | Confirmed research → one-pager + linked UX Epic / Confluence (Problem Definition Generator) |
| `anti-sycophancy` | Pressure-test framing before Designer + PM review |
| `brand-operator-ux-persona` | Brand-side JTBD / operator lens |
| `creator-affiliate-ux-persona` | Partner / creator-affiliate lens |
| `design-system` | Point specs at styleguide + component library |

**Human gate:** Designer signs off when happy, then chats with a PM before Ideate. `write-spec` drafts and publishes only after designer confirm; it does not auto-advance.

## Ideate (stage 3)

| Skill | Use when |
|---|---|
| `ideate` | Framing → ideation brief + tool routing + starter directions (Solution Ideator) |
| `ux-critique` | Coverage matrix: mocks vs one-pager / PRD / epic / tickets / notes (UX Critique) |
| `prototype-handoff` | Designer happy with mocks → Prototype pack (after `ux-critique`) |
| `brand-operator-ux-persona` | Brand lens on concepts |
| `creator-affiliate-ux-persona` | Partner / creator-affiliate lens on concepts |
| `design-system` | Before on-brand mocks (Figma Make / Cursor) |

**Agents (on-demand):** Solution Ideator (`ideate`) · UX Critique (`ux-critique`).

**Intake:** One-pager or detailed PRD preferred; epic, tickets, Granola/meeting notes, or chat paste OK (label framing gaps).

**Human gate:** Do not auto-advance to Prototype. Run `ux-critique` before `prototype-handoff`. Designer confirms the handoff pack.

## Prototype (stage 4)

| Skill | Use when |
|---|---|
| `brand-prototype` | One prompt → clone Brand UI shell, `npm install`, start Vite (Cursor preferred) |
| `partner-prototype` | One prompt → clone Partner UI shell, `npm install`, start Vite (Cursor preferred) |
| `design-system` | After shell is up, when mapping mocks to Styleguide V2 |

**Agent (on-demand):** Prototype Scaffolder — today these two shell skills; orchestrator `prototype` skill can come later.

**How it works:** Each skill ships `scripts/bootstrap.sh`. The agent **runs the script** (does not hand the designer a git/npm checklist). Default folders: `~/Documents/impact-prototypes/brand-ui` and `…/partner-ui`.

**Harness reality:** Full auto-setup needs a local shell → **Cursor** (best) or Claude Code. Figma Make cannot clone repos; skills route Make to Cursor or a labeled Make-only click-through (see each skill’s `references/harnesses.md`).

**Human gate:** Designer owns fidelity and interaction after the shell is running.

## Test (stage 5)

| Skill | Use when |
|---|---|
| `test-plan` | Prototype ready → synthetic pre-flight + Outset/Maze study draft (Test Plan Generator) |
| `accessibility-review` | Synthetic a11y pre-test before unmoderated Maze or recruiting |
| `ux-critique` | Re-check prototype coverage vs one-pager/PRD/epic before sessions (pre-test mode) |
| `test-loopback` | After sessions → publish Verified findings to Confluence/Jira → Empathize input |
| `user-research` | Study-plan depth, recruitment gaps, or post-session gate brief |
| `synthesize-research` | Affinity / theme a completed test corpus (feeds `test-loopback`) |
| `brand-operator-ux-persona` | Brand-side task realism in test scripts |
| `creator-affiliate-ux-persona` | Partner-side task realism in test scripts |

**Agent (on-demand):** Test Plan Generator (`test-plan`).

**Tools:** Outset, Maze, Pendo, Confluence, Jira, Figma (prototype links).

**Human gate:** Review AI study summaries before stakeholders. Findings loop back to Empathize — do not treat AI synthesis as verified research.

## Install in any harness

**Download all 17 skills (all phases):** [designops-skills.zip](https://lesley-spec.github.io/uxdesignops/skills/designops-skills.zip) · [Skills page](https://lesley-spec.github.io/uxdesignops/skills/)

One-command install (Cursor example — installs every skill):

```bash
curl -fsSL https://lesley-spec.github.io/uxdesignops/skills/install.sh | bash -s -- cursor .
```

Replace `cursor` with `claude` or `agents` for Claude Code or Copilot/Codex.

| Harness | Typical path |
|---|---|
| Cursor | `.cursor/skills/<name>/` (symlinked in this repo) |
| Claude Code / Claude | `.claude/skills/<name>/` or `.agents/skills/<name>/` |
| Codex / VS Code Copilot | `.agents/skills/<name>/` |
| Figma Agent | Project or org skills that point at the same `SKILL.md` folders |

```bash
# Example: Claude Code (single skill)
mkdir -p .claude/skills
ln -sfn ../../.agents/skills/write-spec .claude/skills/write-spec
```

Invoke by name, e.g. “use `write-spec` on this confirmed finding” or “use `ideate` on UX-1234” or “run `ux-critique` before handoff” or “use `brand-prototype`” / “use `partner-prototype`” or “use `test-plan` on [prototype link]”.

```bash
# Prototype shells (also symlink for Cursor)
ln -sfn ../../.agents/skills/brand-prototype .cursor/skills/brand-prototype
ln -sfn ../../.agents/skills/partner-prototype .cursor/skills/partner-prototype
```
