---
name: ux-prototyping
description: >-
  Prototype-phase orchestrator for any harness (Cursor, Claude Code, Claude
  chat, Figma Make, Copilot/Codex): installs missing Brand/Partner tools when
  a shell exists, launches a live Brand or Partner preview (localhost, Make
  preview, or Claude preview), then offers to publish a new GitHub repo on
  the designer’s account. Use when the user says ux-prototyping, start a
  prototype, Brand or Partner prototype, localhost, Figma Make prototype, or
  GitHub Pages.
license: Proprietary
metadata:
  stage: prototype
  pipeline: impact-ux-designops
  author: impact.com-ux
  figjam-agent: Prototype Scaffolder
---

# UX prototyping (any harness → live preview → GitHub)

**Stay in this harness.** Do not send the designer to Cursor (or any other
tool) to finish Prototype. Detect the harness, get a **live Brand or Partner
preview** running here, then ask about GitHub.

This skill does **not** scaffold a random Vite/Next app. The prototype is
always the Brand UI shell or the Partner UI shell — via bootstrap, Make
preview, or Claude preview.

| How | See |
|---|---|
| Per-harness steps | [references/harnesses.md](references/harnesses.md) |
| Figma Make clone + `.figma/make` | [references/make.md](references/make.md) |
| GitHub ownership / Pages / fork | [references/github.md](references/github.md) |

## Integrity

**Lead with the insight, not the evidence.** What the person gets back is
short: the finding, what it changes, and the next thing to do. A few lines, not
a report — they came for a decision, not a download.

**Offer the depth, don't deliver it.** Close with one specific follow-up they
can run — "want the evidence trail behind finding 2?" — not a menu of five. The
detail stays available; it does not arrive unasked.

**A number earns its place by changing a decision.** Everything else goes in the
artifact (the claim, the card, the one-pager) where someone can find it when
they need it.

1. **Finish in the current harness.** Cursor, Claude Code, Claude chat,
   Figma Make, Copilot/Codex — all valid. Do not bounce them.
2. **Exclusive shells** — Brand → Brand shell. Partner → Partner shell.
   Never `npm create vite` / Next as a substitute.
3. **Shell harnesses:** run `ensure-harness.sh` then that shell’s
   `bootstrap.sh`. Do not hand a git/npm checklist.
4. **No-shell harnesses (Make, Claude chat):** do not pretend `bootstrap.sh`
   ran. Use that harness’s live preview (Make canvas or Claude artifact).
5. **Do not create repos under someone else’s GitHub user** (including
   `lesley-spec`) unless `gh api user` / the connected GitHub login **is**
   that user. Designers publish to **their** account (or an org they can
   create in).
6. **Do not push to the template remotes** (`one-program-1`,
   `PartnerUI-shell`).
7. GitHub is **opt-in** after the live preview works.
8. **Publishing is the designer's call, every time.** A GitHub repo and a Pages
   site are public artifacts under their name. Confirm before creating either,
   and never treat an earlier yes as standing permission for the next one.
**A prototype is not evidence.** It shows what something could be, not that
anyone needs it or can use it. Everything it appears to demonstrate stays a
hypothesis until `test-plan` puts it in front of participants — a clickable
thing persuades out of proportion to what it proves, and hardest on the people
furthest from the research. Link the one-pager or epic it is built from, so
anyone looking at it can check the framing.


## When to use

- “Use `ux-prototyping`” / `/ux-prototyping`
- After mocks / `prototype-handoff`, in **any** designer harness
- `design-thinking-ux` Prototype phase

## 0. Detect harness (do this first)

| You have… | Harness | Path |
|---|---|---|
| Shell + Cursor `move_agent_to_root` | **Cursor** | A |
| Shell, no Cursor root-move | **Claude Code / Copilot / Codex** | A |
| Figma Make canvas / `figma.com/make` | **Figma Make** | B |
| Claude.ai / Claude chat, no shell | **Claude chat** | C |

If mixed (e.g. Claude with a terminal), prefer **A**.

Ask Brand vs Partner only if unknown.

## Path A — shell (Cursor, Claude Code, Copilot, Codex)

```
Task Progress:
- [ ] Harness script
- [ ] Brand vs Partner bootstrap
- [ ] Live localhost
- [ ] Workspace (Cursor)
- [ ] GitHub prompt
```

1. Sandbox off (`required_permissions: ["all"]`):

   ```bash
   bash "/absolute/path/to/ux-prototyping/scripts/ensure-harness.sh"
   ```

   Parse `IMPACT_HARNESS_READY`.

2. Read `brand-prototype` or `partner-prototype` `SKILL.md`. Run **its**
   `scripts/bootstrap.sh` (sandbox off).

3. Parse `IMPACT_PROTOTYPE_READY … path=… url=…`. Verify the URL. Tell the
   designer it is live.

4. Cursor: `move_agent_to_root` with `path`. Claude Code: File → Open `path`.

5. GitHub prompt (below). Path A uses `publish-repo.sh`.

## Path B — Figma Make

Do **not** run bash bootstrap. Make runs the preview.

Follow [references/make.md](references/make.md):

1. Confirm Brand vs Partner.
2. **Preferred:** Clone the public template into Make (desktop / codebase
   session) so the real Vite shell is the preview.
3. **Always available:** New Make file → implement Brand/Partner chrome from
   the source Figma file + selected mocks + `design-system`. Preview = live.
4. Confirm the designer can click the preview. That is READY.
5. GitHub prompt — Make **Settings → GitHub → Create Repository** on *their*
   connected account (Make cannot create under someone else’s user).

Print:

`IMPACT_PROTOTYPE_READY shell=brand|partner harness=figma-make url=<Make preview or file URL>`

## Path C — Claude chat (no shell)

Do **not** run bash bootstrap. Do **not** send them to Cursor.

1. Confirm Brand vs Partner.
2. Build a **live interactive preview in this chat** (Claude artifact /
   preview) of that shell: chrome, nav, tokens from `design-system` + the
   source Brand/Partner Figma file. Use selected mocks if they pasted links.
3. Confirm they can click through it. That is READY.
4. GitHub prompt — no `gh` CLI. Walk **fork** of the public template onto
   *their* GitHub user, then Pages. See [references/github.md](references/github.md).

Print:

`IMPACT_PROTOTYPE_READY shell=brand|partner harness=claude-chat url=<artifact or preview URL>`

If this Claude later grows a terminal, switch to Path A for the Vite shell
**in addition** — do not block Path C on that.

## GitHub prompt (every path, after READY)

> The prototype is live here. Do you have a GitHub account? If yes, I can
> publish a **new repo under your GitHub user** (not the DesignOps template
> account) so you can share a Pages URL.

| Answer | Do |
|---|---|
| No / later | Stop. Live preview is enough. |
| Yes | Path A: `publish-repo.sh`. Path B: Make GitHub Create Repository. Path C: fork + Pages on github.com. |
| Yes, org `X` | Owner = `X` if they can create repos there. |

**Never** create under `lesley-spec` unless that is the logged-in / connected
GitHub user.

## Prompt examples

1. `Use ux-prototyping — Partner, get it running here.`
2. `Use ux-prototyping in Figma Make for Brand.`
3. `Use ux-prototyping in Claude — I don’t have Cursor open.`
4. `Preview works — I have GitHub, publish it.`

## Anti-patterns

- Sending Make or Claude users to Cursor to “finish” Prototype
- Asking the designer to install Node / Homebrew / `npm install` when a
  script or Make install exists
- Scaffolding a new Vite/Next app instead of Brand/Partner
- Pushing to `lesley-spec/one-program-1` or `PartnerUI-shell`
- Creating a repo under another person’s user
- `gh repo create` / Make Create Repository before they confirm GitHub
- Claiming Path B/C ran `bootstrap.sh`

## Success criteria

- [ ] Harness detected; work finished **here**
- [ ] Live Brand or Partner preview (localhost **or** Make **or** Claude)
- [ ] GitHub asked; if yes, repo is on **their** login (or their org)
