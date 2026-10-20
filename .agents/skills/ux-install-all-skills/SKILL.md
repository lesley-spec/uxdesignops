---
name: ux-install-all-skills
description: >-
  Installs all 37 impact.com UX Design Thinking + UX Research pipeline skills
  (Empathize through Test, plus Frame research skills) into the current project
  and globally for Cursor and Claude Code. Use when the user says
  ux-install-all-skills, install all skills, install the design thinking
  skills, set up the UX pipeline, get started with Design Thinking UX, or a
  designer needs the full skill pack before using the framework.
license: Proprietary
metadata:
  stage: pipeline
  pipeline: impact-ux-designops
  author: impact.com-ux
---

# UX install all skills (bootstrap)

**One invocation → all 37 pipeline skills installed.** Do not ask the
designer to curl, pick a harness, or copy folders. The script does that.

This skill does **not** start Empathize → Test. After READY, offer
`design-thinking-ux` or `ux-research` and wait.

Catalog: [references/catalog.md](references/catalog.md).

## Integrity

1. **Run the install script** — do not improvise `mkdir` / `cp` / `curl`
   of individual skills unless the script is missing.
2. **Install the full pack.** Never install a subset “to keep it simple.”
   The orchestrator needs every child skill.
3. **Do not start the pipeline** unless they asked for a guided run in the
   same message. Install, confirm READY, entice `design-thinking-ux`.
4. **Overwrite is OK.** Re-running updates skills. Do not ask “replace?”
5. **No-shell harnesses** (Figma Make, Claude chat): give the zip / skills
   page. Do not pretend a local install ran.

## When to use

- “Use `ux-install-all-skills`” / `/ux-install-all-skills`
- “Install the Design Thinking skills” / “set up the UX pipeline”
- First time a designer opens a project without the pack
- `design-thinking-ux` (or a phase skill) is missing its siblings

## What gets installed

**37 pipeline skills** (masters + Empathize/Research → Test, including
Nihal’s Frame pack). This installer is copied too so they can re-run later.
Names: [references/catalog.md](references/catalog.md).

**Where (defaults — do not ask):**

| Location | Path |
|---|---|
| Canonical | `<project>/.agents/skills/<name>/` |
| Cursor | `<project>/.cursor/skills/<name>/` (symlink) |
| Claude Code | `<project>/.claude/skills/<name>/` (symlink) |
| Cursor global | `~/.cursor/skills/<name>/` |
| Claude global | `~/.claude/skills/<name>/` |

Global copies mean the pack works in **any** later project, not only this
folder.

`--project-only` if they said “just this repo.” `--target ~/path` if they
named another folder. Otherwise cwd.

## Workflow (Cursor / Claude Code / Copilot)

```
Task Progress:
- [ ] Locate or bootstrap the script
- [ ] Run install-all.sh (sandbox off)
- [ ] Parse READY
- [ ] Tell them they’re set + offer design-thinking-ux
```

1. **If the skill is not in the catalog** (Claude.ai, or a blank Cursor/Claude Code
   project) — do **not** wait for `use ux-install-all-skills`. Run the published
   installer:

   ```bash
   curl -fsSL https://lesley-spec.github.io/uxdesignops/skills/install-all.sh | bash
   ```

   Claude.ai in the browser cannot run this. Tell the designer to paste the
   same curl in **Cursor or Claude Code**.
2. **If the script is already on disk** —
   `.agents/skills/ux-install-all-skills/scripts/install-all.sh`  
   (or `.cursor/skills/…` / `.claude/skills/…`).
3. **If the script is missing** (blank project), bootstrap with the curl above.
   If that URL 404s, use the harness installer:

   ```bash
   curl -fsSL https://lesley-spec.github.io/uxdesignops/skills/install.sh | bash -s -- cursor .
   ```

   Replace `cursor` with `claude` or `agents` when you know the harness.
4. **Run with the sandbox off.** In Cursor Shell, pass
   `required_permissions: ["all"]` (network + write to `~/.cursor` /
   `~/.claude`).

   ```bash
   bash "/absolute/path/to/ux-install-all-skills/scripts/install-all.sh"
   ```

   Optional: `--target /path/to/project` · `--project-only` ·
   `--global-only`.
5. **Parse READY** — look for
   `IMPACT_SKILLS_READY pipeline=37 …`.
6. **Confirm** — show how many skills landed, where, and this next line:

   > All 37 UX Design Thinking and Research skills are installed. Start a guided run with
   > **use design-thinking-ux** — I’ll walk Empathize → Test and stop at
   > each human gate.

7. **Stop.** Wait for yes (or a named phase skill).

## Path — Figma Make / Claude chat (no shell)

1. Point them at the [skills page](https://lesley-spec.github.io/uxdesignops/skills/)
   and [designops-skills.zip](https://lesley-spec.github.io/uxdesignops/skills/designops-skills.zip).
2. If they later open Cursor or Claude Code, they can re-run this skill
   there for a local + global install.
3. Do not block the current chat on a local install.

## Check the installer

From repo root:
`python3 .agents/skills/ux-install-all-skills/scripts/validate.py`

## Anti-patterns

- Asking the designer to copy skill folders by hand
- Installing only `design-thinking-ux` and hoping the rest appear
- Starting Empathize intake in the same turn as install (unless they asked)
- Skipping global install without `--project-only` / an explicit “this repo only”
- Treating a zip download in Make as a substitute for running this in Cursor
  when they actually have a shell
