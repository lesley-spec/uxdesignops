---
name: partner-prototype
description: >-
  Auto-sets up the impact.com Partner UI prototype shell on the designer's
  machine: clones PartnerUI-shell, installs Node if missing plus npm/Vite
  deps, starts Vite. Use when the user says partner-prototype, Partner UI
  shell, Partner prototype, or wants a running Partner / creator-affiliate
  prototype after Ideate mocks / prototype-handoff. Primary harness: Cursor
  (also Claude Code with shell). Figma Make cannot clone repos — skill
  routes Make to a fallback.
license: Proprietary
metadata:
  stage: prototype
  pipeline: impact-ux-designops
  author: impact.com-ux
  figjam-agent: Prototype Scaffolder
---

# Partner prototype (shell bootstrap)

**One invocation → running Partner UI shell.** Do not ask the designer to clone,
install Node, or run `npm install`. The bootstrap script does that.

This skill **only** bootstraps the shell. Building mocks into screens is a
follow-on step in the same Cursor chat after READY.

## Integrity

1. **Run the bootstrap script** — do not improvise `mkdir` / `git clone` / `npm`
   steps by hand unless the script is missing.
2. Template is **Vite + React** (Figma Make–origin bundle).
3. Do **not** claim Figma Make can `git clone` or run this script. Be honest.
4. After READY, move the Cursor workspace to the project path when possible.

## When to use

- “Use `partner-prototype`” / `/partner-prototype`
- Designer ready to prototype Partner-side after mocks / `prototype-handoff`
- Need the real Partner chrome locally

## Hard requirements (agent must check)

| Need | Why |
|---|---|
| Shell / terminal | Script runs locally (Cursor or Claude Code) |
| `git` | Clone the public template |
| Network | GitHub + npm registry (+ Node download if missing) |

**Node 18+ and npm are auto-provisioned** when missing (local copy under
`~/Documents/impact-prototypes/.toolchain`, no sudo). Only `git` is a
hard machine prerequisite (Xcode CLT on macOS).

If git is missing, or the harness has no shell (Figma Make / Claude chat) →
stop with the harness fallback. Do not hand the designer a git/npm checklist.

## Workflow (Cursor / Claude Code)

1. **Locate script** —  
   `.agents/skills/partner-prototype/scripts/bootstrap.sh`  
   (or `.cursor/skills/partner-prototype/scripts/bootstrap.sh` via symlink).
2. **Run it with the sandbox off.** In Cursor Shell, pass
   `required_permissions: ["all"]` (network + unsandboxed npm). Default
   sandbox **cannot** `npm install` or start Vite — that is why other
   designers see “packages missing.”

   ```bash
   bash "/absolute/path/to/partner-prototype/scripts/bootstrap.sh"
   ```

   Optional flags: `--no-dev`, `--reclone`, `--parent ~/other/folder`.
3. **Parse READY** — look for `IMPACT_PROTOTYPE_READY shell=partner path=… url=…`.
4. **Cursor only** — call `move_agent_to_root` with that `path`.
5. **Confirm** — folder path + open the printed URL (Partner default `http://localhost:5173/`).
6. **Stop** — shell is ready. Wait for mock links before editing UI.
   Use `design-system` for Styleguide V2 constraints.

Default install location:

`~/Documents/impact-prototypes/partner-ui`

Override with `IMPACT_PROTOTYPE_HOME` or `--parent`.

## Harness matrix

See [references/harnesses.md](references/harnesses.md).

| Harness | What to do |
|---|---|
| **Cursor** | Run script → `move_agent_to_root` → confirm URL. Preferred. |
| **Claude Code** | Run script → tell user to open the path → confirm URL. |
| **Figma Make** | **Cannot** run bootstrap. Follow Make fallback in harnesses.md. |
| **Claude chat (no shell)** | Open this repo in **Cursor** and say `use partner-prototype`. |

## Template facts (do not invent)

| | |
|---|---|
| Repo | https://github.com/lesley-spec/PartnerUI-shell.git (public) |
| Stack | Vite · React · `npm run dev` |
| Source design | https://www.figma.com/design/jsQedgqU0QkgXQEsMFEyOE/Partner-UI-%E2%80%94-impact.com--Copy- |
| Layout | `src/app/` (routes, layout, TopNav), `src/styles/`, `index.html` |

## Prompt examples

1. `Use partner-prototype — set up the Partner shell for me.`
2. `Use partner-prototype; then build these Partner mocks into the shell: [Figma link].`
3. `Partner prototype broken — partner-prototype --reclone.`

## Anti-patterns

- Manual git/npm recipes for the designer when the script exists
- Asking the designer to install Node, Homebrew, or `npm install` themselves
- Faking success in Figma Make
- Editing UI before READY
- Asking where to put the folder when the default is fine
- Scaffolding a new Vite app instead of this Partner shell

## Success criteria

- [ ] Script exited 0
- [ ] `IMPACT_PROTOTYPE_READY` printed with path + url
- [ ] Designer sees Partner UI at the URL
- [ ] (Cursor) Workspace root is the prototype folder
