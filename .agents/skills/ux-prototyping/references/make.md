# Figma Make — live Brand / Partner prototype

Make **is** a valid Prototype harness. The live **preview** is the proof
it works (same role as localhost in Cursor).

Do not run `bootstrap.sh` inside Make. Do not send the designer to Cursor.

## Which Make mode

| Mode | When | What “running” means |
|---|---|---|
| **Clone template** | Make can **Clone a repository** (Figma desktop / codebase session) | Vite shell preview in Make |
| **Make file** | Clone not available (web Make, no beta) | Make preview of Brand/Partner chrome |

Prefer clone when the UI offers it. Make file is still READY.

## Clone the public shell (preferred)

Templates are public HTTPS:

- Brand: `https://github.com/lesley-spec/one-program-1.git`
- Partner: `https://github.com/lesley-spec/PartnerUI-shell.git`

In Make:

1. New Make file (or codebase session).
2. **Clone a repository** → paste the URL → pick a local folder → Clone.
3. When Make asks to **Run** setup/install, click Run (may be more than once).
4. If preview fails, add `.figma/make/` (below) and Run again.
5. Confirm the designer can click the preview.

Say up front: Brand clone is **large** and can take several minutes.

## Make file (always available)

If there is no Clone control:

1. New Make file.
2. Prompt: implement the **Brand or Partner UI shell** (not a generic app).
   Source Figma + Styleguide V2 (`design-system`) + selected mock frames.
3. Iterate until chrome matches (top nav, tokens, layout).
4. Confirm clickable preview.

Label internally: `harness=figma-make` (still Brand or Partner shell — not
an Ideate-only doodle).

## `.figma/make` (so Make can start Vite)

Copy from this skill’s `scripts/figma-make/brand/` or `…/partner/` into
the project root as `.figma/make/{setup,install,dev,verify,env}`.

Or run (shell harness / after clone on disk):

```bash
bash "/absolute/path/to/ux-prototyping/scripts/write-figma-make-config.sh" \
  --shell brand|partner --project "/path/to/cloned/repo"
```

If Make shows “Couldn’t load preview”, use **Fix for me** / Run.

Brand `env`: port **5174**, URL `http://localhost:5174/one-program-1/`.  
Partner `env`: port **5173**, URL `http://localhost:5173/`.

## GitHub from Make

After preview works:

1. Ask if they have a GitHub account.
2. Make settings → **GitHub** → Connect GitHub (their user or org).
3. First push: **Create Repository** (name they confirm). Make creates it
   under the **connected** GitHub account — not `lesley-spec`.
4. Give them the new repo URL. Pages: enable on that repo (Actions or
   Settings → Pages) if Make did not already.

Make will **not** push into the template repos. That is correct.

## Not success

- Preview never loaded
- Claiming `bootstrap.sh` ran
- Creating the GitHub repo under someone else’s personal account
