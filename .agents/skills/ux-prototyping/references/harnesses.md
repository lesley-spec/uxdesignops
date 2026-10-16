# Harness behavior — ux-prototyping

**Stay where the designer is.** Every harness below can produce a live
Brand or Partner prototype. Do not route them to another tool.

Templates (public):

| Shell | GitHub | Source Figma |
|---|---|---|
| Brand | https://github.com/lesley-spec/one-program-1.git | https://www.figma.com/design/rwAqBrLfwQy8cLyfi2tm3Y/Brand-UI---Impact.com |
| Partner | https://github.com/lesley-spec/PartnerUI-shell.git | https://www.figma.com/design/jsQedgqU0QkgXQEsMFEyOE/Partner-UI-%E2%80%94-impact.com--Copy- |

## Cursor

1. `ensure-harness.sh` then Brand/Partner `bootstrap.sh` (sandbox off).
2. `move_agent_to_root` with `path`.
3. Designer opens `url` (Brand `http://localhost:5174/one-program-1/`,
   Partner `http://localhost:5173/`).
4. GitHub: `publish-repo.sh` after they confirm.

## Claude Code / Copilot / Codex (shell)

Same scripts as Cursor. Then **File → Open** `path` (no
`move_agent_to_root`). Then GitHub prompt.

If skills are missing, `ensure-harness.sh` copies `brand-prototype` and
`partner-prototype` into this harness’s skills folder from the pack zip.

Claude Code install: `.claude/skills/` (this repo already symlinks them).
Copilot/Codex: `.agents/skills/`.

## Claude.ai / Claude chat (no shell)

**This is a complete Prototype path.** Do not tell them to open Cursor.

1. Confirm Brand vs Partner.
2. Produce a **clickable preview in this conversation** (artifact / inline
   preview) using Brand or Partner chrome. Load `design-system` and the
   source Figma link above. Fold in selected mock frames if they shared
   them.
3. Ask them to click it. When they can, that is READY.
4. GitHub: they **fork** the public template to *their* user, then enable
   Pages — see [github.md](github.md). You cannot run `gh` here.

Optional upgrade (never a blocker): if they later open Claude Code, Path A
gives them the real Vite shell on localhost.

## Figma Make

**This is a complete Prototype path.** Do not tell them to open Cursor.

Full clone + `.figma/make` steps: [make.md](make.md).

Short version:

1. Confirm Brand vs Partner.
2. Clone the public template into Make **or** (if clone isn’t available)
   start a Make file and implement that shell from the source Figma + mocks.
3. Wait until Make’s **preview is running**. That is localhost-equivalent.
4. GitHub: Make settings → GitHub → **Create Repository** on the GitHub
   account they connected (their user or org — not a teammate’s personal
   account).

Make’s GitHub integration only creates repos it owns; it will not push
into `lesley-spec` templates.

## Skills install (any harness)

Prefer `ux-install-all-skills` (all 28 pipeline skills, project + global).
If that skill is missing:

```bash
curl -fsSL https://lesley-spec.github.io/uxdesignops/skills/install-all.sh | bash
```

Harness-only fallback:

```bash
curl -fsSL https://lesley-spec.github.io/uxdesignops/skills/install.sh | bash -s -- cursor .
# or: claude | agents
```

In Make / Claude chat with no terminal: point them at
[the skills page](https://lesley-spec.github.io/uxdesignops/skills/) and
this skill’s SKILL.md — then continue the Make/Claude preview path
immediately. Do not wait on a local install to show a live prototype.

## Failure cheatsheet

| Symptom | Fix |
|---|---|
| `Missing required command: git` (Path A) | Xcode CLT, then re-run |
| Node/npm missing (Path A) | Script downloads Node — sandbox off |
| Make preview blank | Add `.figma/make` from [make.md](make.md); click Fix / Run |
| Make cannot clone | Use standard Make file path (still valid READY) |
| Claude has no artifact | Keep iterating the preview in chat until they can click it |
| `gh` not logged in | Path A: `gh auth login`. Path B: Connect GitHub in Make. Path C: fork in the browser |
| Sandbox deny (Path A) | `required_permissions: ["all"]` |
