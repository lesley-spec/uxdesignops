---
name: brand-prototype
description: >-
  Auto-sets up the impact.com Brand UI prototype shell: clones the public
  Brand template, installs Node if missing plus npm/Vite deps, starts Vite.
  Use when the user says brand-prototype, Brand UI shell, or Brand prototype
  in Cursor / Claude Code / Copilot. In Figma Make or Claude chat, use
  ux-prototyping (those harnesses run a live preview without this script).
license: Proprietary
metadata:
  stage: prototype
  pipeline: impact-ux-designops
  author: impact.com-ux
  figjam-agent: Prototype Scaffolder
---

# Brand prototype (shell bootstrap)

**One invocation → running Brand UI shell.** Do not ask the designer to clone,
install Node, or run `npm install`. The bootstrap script does that.

This skill **only** bootstraps the shell. Building mocks into screens is a
follow-on step in the same Cursor chat after READY.

## Integrity

1. **Run the bootstrap script** — do not improvise `mkdir` / `git clone` / `npm`
   steps by hand unless the script is missing.
2. Templates are **Vite + React** (Figma Make–origin bundles), **not** Next.js.
3. In Figma Make or Claude chat (no shell), do **not** run this script —
   invoke `ux-prototyping` instead (live preview in that harness).
4. After READY, move the Cursor workspace to the project path when possible.

## When to use

- “Use `brand-prototype`” / `/brand-prototype`
- Designer ready to prototype Brand-side after mocks / `prototype-handoff`
- Need the real Brand chrome + Styleguide-aligned shell locally

## Hard requirements (agent must check)

| Need | Why |
|---|---|
| Shell / terminal | Script runs locally (Cursor or Claude Code) |
| `git` | Clone the public template |
| Network | GitHub + npm registry (+ Node download if missing) |

**Node 18+ and npm are auto-provisioned** when missing (local copy under
`~/Documents/impact-prototypes/.toolchain`, no sudo). Only `git` is a
hard machine prerequisite (Xcode CLT on macOS).

If git is missing on a **shell** harness → stop with a short git/Xcode note.
If this is Figma Make or Claude chat → invoke `ux-prototyping` (Path B / C).
Do not hand the designer a git/npm checklist.

## Workflow (Cursor / Claude Code)

1. **Locate script** —  
   `.agents/skills/brand-prototype/scripts/bootstrap.sh`  
   (or `.cursor/skills/brand-prototype/scripts/bootstrap.sh` via symlink).
2. **Run it with the sandbox off.** In Cursor Shell, pass
   `required_permissions: ["all"]` (network + unsandboxed npm). Default
   sandbox **cannot** `npm install` or start Vite — that is why other
   designers see “packages missing.”

   ```bash
   bash "/absolute/path/to/brand-prototype/scripts/bootstrap.sh"
   ```

   Optional flags: `--no-dev` (skip Vite), `--reclone` (wipe + fresh clone),  
   `--parent ~/other/folder`.
3. **Parse READY** — look for `IMPACT_PROTOTYPE_READY shell=brand path=… url=…`.
4. **Cursor only** — call `move_agent_to_root` with that `path` so the designer
   is inside the prototype project.
5. **Confirm** — tell the designer the folder path + open the printed URL
   (Brand default `http://localhost:5174/one-program-1/` — template uses a Vite base path).
6. **Stop** — shell is ready. Wait for mock links / “build this flow” before
   editing UI. Point Styleguide work at `design-system`.

Default install location:

`~/Documents/impact-prototypes/brand-ui`

Override with `IMPACT_PROTOTYPE_HOME` or `--parent`.

## Harness matrix

See [references/harnesses.md](references/harnesses.md).

| Harness | What to do |
|---|---|
| **Cursor** | Run script → `move_agent_to_root` → confirm URL. |
| **Claude Code / Copilot** | Run script → open the path → confirm URL. |
| **Figma Make / Claude chat** | Do not run this script. Use `ux-prototyping` (preview in that harness). |

## Template facts (do not invent)

| | |
|---|---|
| Repo | https://github.com/lesley-spec/one-program-1.git (public) |
| Stack | Vite · React · `npm run dev` |
| Source design | https://www.figma.com/design/rwAqBrLfwQy8cLyfi2tm3Y/Brand-UI---Impact.com |
| Entry | `index.html` + `src/` |
| Note | Repo is **large**; first clone can take several minutes. Say so up front. |

## Prompt examples

1. `Use brand-prototype — set up the Brand shell for me.`
2. `Use brand-prototype after prototype-handoff; then we'll drop in these Figma mocks: [link].`
3. `Brand prototype isn't running — re-run brand-prototype with a clean setup.`  
   → run bootstrap with `--reclone`.

## Anti-patterns

- Pasting multi-step git/npm instructions for the designer to run manually when the script exists
- Asking the designer to install Node, Homebrew, or `npm install` themselves
- Describing a Next.js / `src/pages` layout that this template does not have
- Claiming this bootstrap ran inside Figma Make or Claude chat (use `ux-prototyping`)
- Editing product UI before bootstrap prints READY
- Blocking on “where should I put the folder?” — use the default parent unless they specify
- Scaffolding a new Vite app instead of this Brand shell

## Success criteria

- [ ] Script exited 0
- [ ] `IMPACT_PROTOTYPE_READY` printed with path + url
- [ ] Designer can open the URL and see Brand UI chrome
- [ ] (Cursor) Workspace root is the prototype folder
