# Empathize skills (Design Thinking stage 1)

Portable [Agent Skills](https://agentskills.io/specification) for the **Empathize** column on the [UX DesignOps FigJam](https://www.figma.com/board/slhZ9uzMTmaekjmbEosyzb/UX-DesignOps).

Canonical source: `.agents/skills/` (open standard). Cursor also discovers them via symlinks in `.cursor/skills/`.

| Skill | Use when |
|---|---|
| `user-research` | Deep-dive a finding, design a study, or decide if a problem is worth solving |
| `research-synthesis` | Triangulate across PostHog + Pendo + Dovetail (+ Outset/Freshdesk) |
| `synthesize-research` | Affinity / theme a **single** corpus (one Dovetail project, one interview set) |
| `data-analyze` | Ad-hoc PostHog or Pendo quantitative questions (FigJam label was `data:analyze`) |
| `morning-intelligence` | Pre-standup briefing from the latest Research Insight Monitor report |

**Agent (scheduled):** Research Insight Monitor in `research-agent/` — these skills are the **on-demand** layer designers invoke in any harness.

**Human gate:** Designer confirms the problem is worth solving. Skills gather and narrate; they do not make that call.

## Install in any harness

Skills are plain folders with `SKILL.md`. Copy or symlink the folders you need:

| Harness | Typical path |
|---|---|
| Cursor | `.cursor/skills/<name>/` (already symlinked in this repo) |
| Claude Code / Claude | `.claude/skills/<name>/` or `.agents/skills/<name>/` |
| Codex / VS Code Copilot | `.agents/skills/<name>/` |
| Figma Agent | Project or org skills that point at the same `SKILL.md` folders |
| Other Agent Skills clients | Any path the client documents for skill discovery |

```bash
# Example: Claude Code in this repo
mkdir -p .claude/skills
ln -sfn ../../.agents/skills/user-research .claude/skills/user-research
# …repeat for the other four
```

Invoke by name, e.g. “use `morning-intelligence`” or “run `research-synthesis` on this finding.”
