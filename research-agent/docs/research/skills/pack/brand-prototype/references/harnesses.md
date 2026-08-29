# Harness behavior — Brand / Partner prototype skills

These skills **bootstrap a local Vite shell** when the harness has a
terminal. The agent runs `scripts/bootstrap.sh`. Designers should not
install packages by hand.

**Figma Make and Claude chat:** do not run this script. Invoke
`ux-prototyping` — that skill completes Prototype in those harnesses
(live Make/Claude preview + GitHub on the designer’s account).

## Cursor

1. `use brand-prototype` or `use partner-prototype` (or `ux-prototyping`).
2. Run `scripts/bootstrap.sh` with sandbox off (`required_permissions: ["all"]`).
3. Read `IMPACT_PROTOTYPE_READY … path=… url=…`.
4. `move_agent_to_root` with `path`.
5. Designer opens `url`.
6. Paste Figma mocks; implement + `design-system`.

## Claude Code / Copilot / Codex (shell)

Same through READY. Then File → Open `path`. Confirm `url`.

## Claude.ai / Figma Make

Use **`ux-prototyping`** (Paths C and B). Do not claim this bootstrap ran.

## Failure cheatsheet

| Symptom | Fix |
|---|---|
| `Missing required command: git` | Xcode Command Line Tools, then re-run |
| Node/npm missing | Script downloads Node — re-run with `all` permissions |
| `Vite did not install` | Sandbox off (`required_permissions: ["all"]`) |
| Clone hangs / huge Brand repo | Wait, or `--reclone` later |
| Port in use | Script reuses existing server; open printed URL |
| Designer is in Make or Claude chat | `ux-prototyping` — do not run bootstrap here |
