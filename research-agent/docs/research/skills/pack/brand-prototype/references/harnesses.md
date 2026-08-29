# Harness behavior — Brand / Partner prototype skills

These skills **bootstrap a local Vite shell**. The agent runs
`scripts/bootstrap.sh`. That script clones the template, **installs Node if
missing**, runs `npm ci` / `npm install` (Vite + deps), and starts the
dev server. Designers should not install packages by hand.

## Preferred: Cursor

1. Designer (or pipeline): `use brand-prototype` or `use partner-prototype`.
2. Agent runs `scripts/bootstrap.sh` with **sandbox off**
   (`required_permissions: ["all"]`). Network is required for clone, npm,
   and the Node download.
3. Agent reads `IMPACT_PROTOTYPE_READY … path=… url=…`.
4. Agent calls Cursor `move_agent_to_root` with `path`.
5. Designer opens `url` in the browser — shell is live.
6. Designer pastes Figma mock links; agent implements into the shell (+ `design-system`).

**This is the path to optimize.** One prompt, automatic setup — including
Node and Vite packages on a machine that has never run npm.

## Claude Code (desktop / CLI with shell)

Same as Cursor through step 3. Then tell the designer to **File → Open** the
`path` folder (Claude may not expose `move_agent_to_root`). Confirm `url`.

## Claude.ai chat (no local shell)

Do **not** pretend to clone. Reply:

> Brand/Partner prototype setup needs a local shell. Open the **ux-designops-ai**
> repo in **Cursor**, then say `use brand-prototype` or `use partner-prototype`.
> The agent will clone the template, install Node + npm packages, and start the site.

## Figma Make (honest fallback)

Make **cannot** run `git clone` / `npm install` / the bootstrap script. Do not
claim the skill “set up the repo” inside Make. Make is **not** a valid
Prototype-phase deliverable in the Design Thinking pipeline — route to Cursor.

### Option A — Required for the pipeline

Tell the designer:

1. Keep mocks in Figma (selection is fine).
2. Switch to **Cursor** → `use brand-prototype` or `use partner-prototype`.
3. After READY, paste the Make/mock frame links; build into the real shell.

### Option B — Stay in Make for a lightweight click-through

Only if they insist on Make **and** they are **not** in the pipeline Prototype
phase (Ideate-only click-through):

1. Confirm Brand vs Partner audience.
2. Use **selected frames** as the screens to implement **inside Make**.
3. Match chrome/tokens from the source Brand/Partner UI Figma files (links in
   each skill’s Template facts) and Styleguide V2 — this is a **visual**
   prototype, not the GitHub shell.
4. Label clearly: **Make prototype (not Brand/Partner shell)**.

Never say Option B “ran brand-prototype / partner-prototype successfully.”

## Failure cheatsheet

| Symptom | Fix |
|---|---|
| `Missing required command: git` | Install Xcode Command Line Tools, then re-run |
| Node/npm missing | Script downloads a local Node into `impact-prototypes/.toolchain` — re-run with `all` permissions |
| `Vite did not install` / empty `node_modules` | Re-run bootstrap with sandbox off (`required_permissions: ["all"]`) |
| Clone hangs / huge Brand repo | Wait; Brand template is large. Or `--reclone` later |
| Port in use | Script reuses existing server; open printed URL |
| Permission / sandbox deny | Re-run script with `all` permissions (not just network) |
| Private-repo auth errors | Templates are public HTTPS — check VPN/firewall, not SSH keys |
| Skill not found | Install from `.agents/skills/` (see Pack README) |
