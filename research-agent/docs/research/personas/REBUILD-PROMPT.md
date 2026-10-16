# Rebuild prompt — persona page with the Ask feature

The definitive spec. Open this repo in Cursor, then paste everything below the
line into the chat. Cursor must be able to read the repo — the prompt instructs
it to pull content from real files, and pasting the prompt alone will produce an
invented persona set.

Supersedes `site/REBUILD-PROMPT.md`.

---

Build a persona reference for impact.com: **one self-contained `index.html`**,
no build step, no framework, no dependencies except a Google Fonts stylesheet.
It must work opened from the filesystem or served from any static host. The Ask
feature additionally needs a small back end — see that section.

## Rule zero

**Never invent a statistic, a quote, a participant or a persona detail.** This is
a research artefact. A plausible-sounding number is worse than a missing one.
Every percentage carries the denominator its source states — "55% of 11", never
"55%". If something is missing from the source files, leave it out and say so in
your summary. If you cannot read a file you were told to read, stop and ask
rather than filling the gap.

## Content — read these first

- `personas/personas.md` — all six personas in full: goals ladder, job statement,
  job dimensions, frustrations, biggest unmet need, confidence score and basis,
  day-in-the-life, workflow stages with friction levels, creator-vs-affiliate
  divergence, sources and gaps.
- `personas/index.html` — the reference implementation, and **the only source for
  the Ask feature's evidence packs**. They are not in the markdown.

## The six personas

| id | Name | Pill label | Side | Confidence |
|---|---|---|---|---|
| `marlo` | Nia Bennett | Partner · Getting started | partner | 64/100 |
| `quinn` | Danny Alvarez | Partner · Scaling up | partner | 81/100 |
| `nour` | Priya Shah | Partner · Strategic growth | partner | 58/100 |
| `pax` | Sophie Carter | Brand · Founder-operator | brand | 62/100 |
| `rowan` | Maya Thompson | Brand · Programme manager | brand | 76/100 |
| `kit` | James Whitfield | Brand · Partnerships lead | brand | 58/100 |

The ids are legacy slugs. Keep them — the evidence packs are keyed on them.

---

# Part 1 — The Ask feature

The hardest part and the one most likely to be built wrong. **Getting the same
answers as the reference depends entirely on reaching the same evidence.** A
beautifully built panel wired to nothing is the failure mode.

## Layer 1 — the embedded packs. Copy, never regenerate.

The floor under every answer. **Not in `personas.md`** — only in
`personas/index.html`, as JavaScript template literals:

- `var RULES = `...`;` — 2,577 characters of standing instruction
- `PACKS.marlo` · `PACKS.quinn` · `PACKS.nour` · `PACKS.pax` · `PACKS.rowan` ·
  `PACKS.kit` — about 20,000 characters in total

**Lift all seven byte for byte.** Do not summarise, reword, shorten or
regenerate. They hold verbatim participant quotes with their IDs, figures with
their exact denominators, and a `KNOWN GAPS` block per persona listing what was
never researched. A regenerated pack produces a persona that answers confidently
from invented evidence — worse than having no persona at all.

Verify with a diff, not by eye.

## Layer 2 — the data connectors. Wire all of them.

| Source | Tools | What it answers | Status |
|---|---|---|---|
| **Dovetail** | `search_workspace`, `get_insight_content`, `get_project_highlights`, `list_project_insights`, `get_doc_content` | Qualitative truth. Holds the Brand Value Stream research and the Digital Twin training profiles | verified |
| **PostHog** | `exec` → `call execute-sql` | Behavioural truth: event volumes, funnels, cohorts, regions, device splits | verified |
| **Outset** | `search`, `list_projects`, `list_reports`, `get_topline_insights` | Study design, screeners, and toplines that state their own denominators | verified |
| **Pendo** | usage, guides, polls, surveys | In-product behaviour. Never wired in the reference build — add it | available |
| **Atlassian** | Confluence search and page read | Specs, research write-ups, the UX hub | available |
| **G2** | — | No connector. 158 brand reviews are embedded in the packs as a dated snapshot | snapshot |
| **Gong** | — | Needs authorisation. Treat as unavailable and say so | unavailable |

Two Dovetail documents worth pulling by id — twin-training material written for
exactly this purpose:

- `6qF7tESYHrVRUz6786Bnx1` — Partner Digital Twin, Full Training Profile
- `3ou91MsxLsBENNxp0c9puP` — Brand Value Stream, Founding Research Sept 2026

## The grounding hierarchy — this is what makes answers match

1. **Answer from the embedded pack** when it covers the question. It is curated
   and every figure carries its denominator.
2. **Look it up** when the pack does not, and name which source answered. A
   lookup returning nothing useful is reported as nothing useful.
3. **Decline and name the gap** when neither answers.

**Never let a live lookup silently override a pack figure.** If they disagree,
show both and say they disagree. That is a finding, not a bug.

## Architecture

`window.claude` is an artifact-runtime API and does not exist outside claude.ai,
so this build needs its own back end:

- A server route that calls the Anthropic API with
  `RULES.replace('NAME_HERE', name) + PACKS[id]` as a leading user turn, then the
  last eight conversation turns.
- Tool definitions bridged to your MCP clients or the sources' REST APIs.
- **Keys stay server-side.** Never ship an API key to the browser.
- Stream the response. Support cancellation with an abort signal. Keep turn
  history on the client.
- Guard the SQL path: reject anything matching
  insert/update/delete/drop/alter/create/truncate.
- Degrade cleanly. If the back end is unreachable, hide the panel. The rest of
  the page must not depend on it.

Show a status line naming which sources are live for this view, and state plainly
that G2 is an embedded snapshot and which connectors are missing. Silence about a
dead connector is a bug.

## The predefined prompts — use these exactly

Three per persona, rendered as unlabelled chips. One empathy, one for designers,
one for product managers, in that order.

**Nia Bennett** (`marlo`)
- Walk me through the moment you nearly gave up.
- I'm redesigning the profile step — what would make you finish it?
- If we fixed one thing for you this quarter, what should it be?

**Danny Alvarez** (`quinn`)
- What does a bad week actually feel like?
- Would a predicted EPC on the offer card change what you click?
- Rank mobile sharing, offer signal and payout speed for me.

**Priya Shah** (`nour`)
- What made you stop counting applications as pipeline?
- If the cost-model filter came back, where should it live?
- Is API depth a retention issue for you, or a nice-to-have?

**Sophie Carter** (`pax`)
- What went through your mind the first time you logged in?
- I'm designing an applicant quality score — what would you need to see?
- Is the price or the learning curve the bigger risk to you renewing?

**Maya Thompson** (`rowan`)
- What was the worst moment with a partner this quarter?
- I'm adding partner recommendations — what would make you trust them?
- What would actually make you leave for another platform?

**James Whitfield** (`kit`)
- How did it feel to find the dashboard had changed?
- We're redesigning the partner-side link flow — why should you care?
- What would justify consolidating onto one platform to your CMO?

## The point of the feature

The RULES make **declining the default**. Asked something the evidence does not
cover, the persona says so, names the gap, and stops. **That refusal is the
feature. If your build answers everything, you have broken it.**

---

# Part 2 — The page

## Design system — impact.com iui3, vnext theme

Declare tokens under their real names so `@impactinc/frontend-theme-tokens` can
replace them later, then alias page variables to them.

```
                   vnext-light    vnext-dark
text-default       #25282f        #e4e5e8
text-subdued       #606672        #a7a7a7
text-disabled      #a7a7a7        #606672
background         #ffffff        #18191d
dimmed             #f0f1f3        #2f3138
border             #e0e9f0        #323742
primary button     #1d66de        #276fe5
brand red          #f5333f        #f5333f
```

Font **Sarabun** (Google Fonts), fallback `"Helvetica Neue", helvetica,
sans-serif`. Scale: 40/52 display · 24/33 header · 18/23 subheader · 16/20 body ·
14/18 UI · 12/15 caption · 26/33 metric. Radius 8px for cards and inputs, fully
rounded for pills and chips.

Both themes: tokens on bare `:root`, redefined under
`@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) }` and
again under `:root[data-theme="dark"]`. `body` sets an explicit background.

## Structure

1. **Header** — "User Personas at impact.com", one-line lede with the evidence base.
2. **Sticky pill nav** — "All six" plus one pill per persona labelled with the
   tier, persona name in `title`, colour-coded by side. Active pill tracked with
   `IntersectionObserver`; scroll targets offset by the bar height; active pill
   scrolls itself into view when narrow.
3. **Comparison matrix** — a column per persona; rows for Goal, Core job, #1 pain,
   #1 unmet need, Key quote, Evidence & confidence. Whole column header is one
   click target. Horizontally scrollable with snap.
4. **Partner section**, then **Brand section**, each with a two-column intro
   (heading left, description right above 860px).
5. **Six persona cards** — portrait, name, tier, role, meta, pull quote; two
   columns (left: goals ladder, job statement, job dimensions, frustrations;
   right: biggest unmet need, confidence card, charts); creator-vs-affiliate block
   on partner cards only; day-in-the-life in two reading columns above 900px;
   workflow map; Ask panel; back-to-top row.
6. **Creator/affiliate section**, **feedback block**, **sources footer**.

## Charts

Hand-built HTML bars and inline SVG. No charting library. Every chart carries
visible value labels and a `<details>` table view.

Palette, already validated for colour-vision deficiency and contrast in both
themes — do not substitute:

- series `#1d66de` light / `#276fe5` dark; second series `#f5333f`
- diverging sentiment: blue / `#606672` light, `#a7a7a7` dark / `#f5333f`
- friction good `#2f7d4f`, warn `#8a6d1f`, bad `#f5333f` light;
  `#8bd738`, `#eeba00`, `#f5333f` dark

The workflow map is a friction polyline above a row of stage columns — number,
stage name, what they do, friction pill. Stages and levels come from
`personas.md`.

## Card export

Each card exports as PNG and SVG. Build the poster by **reading the live card
from the DOM**, not from a parallel data object, so it cannot drift and captures
the whole persona: goals, job, dimensions, frustrations, unmet need, the full
workflow strip, the creator/affiliate block, the confidence bar.

Two columns at 1240px wide, height computed from flowed content, always light
theme with literal hex since it lands in decks. Download via an ordinary
`<a download>` blob.

---

# Part 3 — Four traps

All four were hit building the reference. Each cost a debugging round.

1. **Web fonts do not load in a data-URI SVG.** Rendering an SVG through
   `new Image()` onto a canvas falls back to a system font. Character-count
   wrapping against a web font therefore overflows and clips. Measure with canvas
   `measureText` against **the exact stack the SVG declares**, and declare one
   that is always present: `Helvetica Neue, Helvetica, Arial`.
2. **An unbalanced tag makes an SVG silently unrenderable.** One stray `</tspan>`
   made every PNG export fail through `img.onerror` with no message. Check tag
   balance on the generated string before encoding.
3. **Watch CSS class collisions.** `.pb` as a brand-pill modifier collided with
   `.pb` the paired-bar chart row, turning the pills into grids capped at 100px.
   Namespace nav classes: `.nav-p`, `.nav-b`.
4. **Flex children shrink by default.** Pills in an `overflow-x:auto` row with
   `white-space:nowrap` compress and clip instead of overflowing. Set
   `flex: 0 0 auto`.

---

# Done when

**The page**
- Renders in light and dark, and at 400px wide with no horizontal page scroll
- Every pill shows its full label — `scrollWidth <= offsetWidth` for all of them
- Every persona exports a complete PNG and SVG with nothing clipped. Check Priya
  first, hers is the longest
- Every chart has visible labels and a table view
- Every percentage on the page states its denominator
- No console errors

**The Ask feature**
- `RULES` and all six `PACKS` are byte-identical to `personas/index.html` —
  diffed, not eyeballed
- Every connector is either wired and shown as live, or named as unavailable in
  the status line
- A question the pack covers is answered from the pack; one it does not triggers
  a visible lookup; neither answering produces a refusal
- No API key is reachable from the browser
- With the back end unreachable, the Ask panel hides and nothing else breaks
- **The refusal test:** ask Nia *"what do you think of our pricing page?"* and
  James *"how does procurement work at your company?"* — both must decline and
  name the gap. If either answers, the packs were regenerated and the build is
  not trustworthy.
