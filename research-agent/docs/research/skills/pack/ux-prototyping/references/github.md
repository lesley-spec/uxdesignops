# GitHub publish — designer-owned repos

Designers **cannot** create repositories under another person’s GitHub
user (including `lesley-spec`). Collaborator access on an existing repo
does **not** grant create-repo on that account.

After the live preview works (localhost, Make, or Claude), ask if they
have a GitHub account. If yes, publish under **their** login (or an org
they can create in).

Pages URL:

`https://<github-user-or-org>.github.io/<repo-name>/`

## Path A — `gh` (Cursor / Claude Code / Copilot)

`publish-repo.sh` creates a new repo as the logged-in `gh` user, rewrites
Vite `base`, adds a Pages workflow. It **renames** template `origin` to
`template` and will refuse to create under `lesley-spec` unless that is
the login.

## Path B — Figma Make

Make settings → GitHub → Connect → **Create Repository**.

The repo is created on the GitHub account **connected to Make** (their
user or org). Make only pushes to repos **it** created — it will not
push to `lesley-spec/one-program-1` or `PartnerUI-shell`. That is what
we want.

Then enable GitHub Pages on that new repo if needed.

## Path C — Claude chat (no `gh`)

Do not paste a git recipe and stop. Walk the browser flow:

1. They must be logged into GitHub as **themselves**.
2. **Fork** the public template (creates a repo under *their* user):
   - Brand: https://github.com/lesley-spec/one-program-1/fork
   - Partner: https://github.com/lesley-spec/PartnerUI-shell/fork
3. Settings → Pages: deploy from GitHub Actions or `gh-pages` / `docs`.
   If the fork has no Pages workflow yet, they can add one from the
   skill’s `scripts/pages.yml` in a later Cursor/Claude Code session.
4. Share `https://<their-user>.github.io/<fork-name>/`.

Forking is the no-CLI way to get a repo on **their** account without
creating anything under `lesley-spec`.

## Do not

- Create repos under `lesley-spec` unless that **is** the connected login.
- Push to the public templates.
- Share a personal access token so everyone publishes as one person.

## Shared org (optional)

If the team uses a GitHub org with **Create repository** permission:

```bash
export IMPACT_PROTOTYPE_GITHUB_OWNER=the-org-login
```

Or Make: connect that **org** (not a teammate’s personal user).

## Auth (Path A)

1. `gh auth status` — else `gh auth login`.
2. Show `gh api user --jq .login`.
3. Default **public** (Pages on private needs GitHub Pro).
4. No secrets, `.env`, or customer data in prototype repos.

## Vite `base`

Project Pages serve `/<repo-name>/`. `publish-repo.sh` rewrites
`vite.config.*`. After a fork, they may need the same `base` change.
