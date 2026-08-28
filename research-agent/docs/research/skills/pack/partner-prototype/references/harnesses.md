# Harness behavior — Brand / Partner prototype skills

These skills **bootstrap a local Vite shell**. That needs a real machine shell
(git + Node + npm). Not every design tool has that.

## Preferred: Cursor

1. Designer (or agent chat): `use brand-prototype` or `use partner-prototype`.
2. Agent runs `scripts/bootstrap.sh` (full network / all permissions if prompted).
3. Agent reads `IMPACT_PROTOTYPE_READY … path=… url=…`.
4. Agent calls Cursor `move_agent_to_root` with `path`.
5. Designer opens `url` in the browser — shell is live.
6. Designer pastes Figma mock links; agent implements into the shell (+ `design-system`).

**This is the path to optimize.** One prompt, automatic setup.

## Claude Code (desktop / CLI with shell)

Same as Cursor through step 3. Then tell the designer to **File → Open** the
`path` folder (Claude may not expose `move_agent_to_root`). Confirm `url`.

## Claude.ai chat (no local shell)

Do **not** pretend to clone. Reply:

> Brand/Partner prototype setup needs a local shell. Open the **ux-designops-ai**
> repo in **Cursor**, then say `use brand-prototype` or `use partner-prototype`.
> The agent will clone the template, install, and start the site for you.

## Figma Make (honest fallback)

Make **cannot** run `git clone` / `npm install` / the bootstrap script. Do not
claim the skill “set up the repo” inside Make.

### Option A — Recommended

Tell the designer:

1. Keep mocks in Figma (selection is fine).
2. Switch to **Cursor** → `use brand-prototype` or `use partner-prototype`.
3. After READY, paste the Make/mock frame links; build into the real shell.

### Option B — Stay in Make for a lightweight click-through

Only if they insist on Make:

1. Confirm Brand vs Partner audience.
2. Use **selected frames** as the screens to implement **inside Make**.
3. Match chrome/tokens from the source Brand/Partner UI Figma files (links in
   each skill’s Template facts) and Styleguide V2 — this is a **visual**
   prototype, not the GitHub shell.
4. Label clearly: **Make prototype (not Brand/Partner shell)**.

Never say Option B “ran partner-prototype successfully.”

## Failure cheatsheet

| Symptom | Fix |
|---|---|
| `Missing required command: git/node/npm` | Install Xcode CLT / Node 18+; re-run skill |
| Clone hangs / huge Brand repo | Wait; Brand template is large. Or `--reclone` later |
| Port in use | Script reuses existing server; open printed URL |
| Permission / sandbox deny | Re-run script with full permissions / network |
| Private-repo auth errors | Templates are public HTTPS — check VPN/firewall, not SSH keys |
| Skill not found | Install from `.agents/skills/` (see Pack README) |
