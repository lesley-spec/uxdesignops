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
| `anti-sycophancy` | Pressure-test framing before Principal review |
| `brand-operator-ux-persona` | Brand-side JTBD / operator lens |
| `creator-affiliate-ux-persona` | Partner / creator-affiliate lens |
| `design-system` | Point specs at styleguide + component library |

**Human gate:** Principal approves framing before Ideate. `write-spec` drafts and publishes only after designer confirm; it does not auto-advance.

## Install in any harness

| Harness | Typical path |
|---|---|
| Cursor | `.cursor/skills/<name>/` (symlinked in this repo) |
| Claude Code / Claude | `.claude/skills/<name>/` or `.agents/skills/<name>/` |
| Codex / VS Code Copilot | `.agents/skills/<name>/` |
| Figma Agent | Project or org skills that point at the same `SKILL.md` folders |

```bash
# Example: Claude Code
mkdir -p .claude/skills
ln -sfn ../../.agents/skills/write-spec .claude/skills/write-spec
```

Invoke by name, e.g. “use `write-spec` on this confirmed finding” or “run `anti-sycophancy` on this one-pager draft.”
