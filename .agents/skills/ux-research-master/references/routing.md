# Routing — what a message means, and which skill answers it

Read top to bottom. The first row that matches wins. Ties are broken by the
rules at the bottom, not by asking the designer.

## Masters (hand off, don't duplicate)

| They said | Load |
|---|---|
| "take me through design thinking", "Empathize to Test", "the whole pipeline" | `design-thinking-ux` |
| "do the research properly", "full research run", "start research" | `ux-research` |
| "which skill", "what can this do", "set me up", "install" | stay here |

## Evidence and the Frame

| They said | Load | Runner-up |
|---|---|---|
| "what do we know about X", "has this been researched", "any research on…" | `user-context` | `research-synthesis` |
| "is this hypothesis supported", "is there evidence for", "prove it" | `user-context` | `anti-sycophancy` |
| "where are our blindspots", "what don't we know" | `user-context` | `frame-maintenance` |
| "which of these should we build first", "rank these on evidence" | `user-context` | `anti-sycophancy` |
| "log this finding", "record this", "add to the Frame" | `user-context` | — |
| "is the Frame stale", "what should we retire", "what should we research next" | `frame-maintenance` | `user-context` |
| "do the sources agree", "triangulate", "is this real or keyword noise" | `research-synthesis` | `synthesize-research` |
| "affinity map these notes", "theme this study", "what came out of these interviews" | `synthesize-research` | `research-synthesis` |

## Personas

| They said | Load | Runner-up |
|---|---|---|
| "who are our users", "the personas", "which persona owns this" | `user-personas` | `user-context` |
| Brand side — operator, ACM, marketing director, advertiser | `brand-operator-ux-persona` | `user-personas` |
| Partner side — creator, affiliate, publisher | `creator-affiliate-ux-persona` | `user-personas` |
| "run this past a persona", "synthetic user check", "pre-test this" | `persona-check` | `accessibility-review` |

`user-personas` is the **set** — who exists, their JTBD, confidence per claim.
The two `*-ux-persona` skills are **lenses** applied to a spec or a concept.
`persona-check` walks a persona through a **task** on a real artifact.

## Research requests and studies

| They said | Load | Runner-up |
|---|---|---|
| "research request", "can UXR look into…", "triage this", "MICRO or DEEP?" | `research-intake` | `user-context` |
| "plan the study", "write the discussion guide", "draft a screener", "set up Outset" | `research-planner` | `research-intake` |
| "build the dashboard", "who should we test with", "find partners who use X", "Pendo survey" | `research-builder` | `data-analyze` |
| "before we build any Pendo guide", "guide engagement is low", "Pendo or email" | `pendo-guide-strategy` | `research-builder` |
| "is this a problem worth solving", "deep-dive this finding", "make the case" | `user-research` | `user-context` |

**Order matters.** Intake routes, planner designs, builder instruments. A
request that skips intake usually skips the "do we already know" check.

## Quantitative

| They said | Load | Runner-up |
|---|---|---|
| "funnel", "drop-off", "conversion", "how many users", "trend since" | `data-analyze` | `research-builder` |
| "build the measure", "what should we instrument", "baseline this" | `research-builder` | `data-analyze` |
| "did it work", "post-launch check", "did adoption move", "did the research hold" | `adoption-check` | `data-analyze` |

## Define

| They said | Load | Runner-up |
|---|---|---|
| "write the one-pager", "draft the PRD", "frame this problem", "create the epic" | `write-spec` | `user-research` |
| "pressure-test this", "poke holes", "is this framing weak", "am I kidding myself" | `anti-sycophancy` | `user-context` |
| "what components exist", "tokens", "is this on-brand", "styleguide" | `design-system` | — |

## Ideate

| They said | Load | Runner-up |
|---|---|---|
| "ideas for", "how might we", "wireframe directions", "concepts" | `ideate` | `design-system` |
| "critique these mocks", "does this cover the spec", "coverage matrix" | `ux-critique` | `anti-sycophancy` |
| "heuristic review", "expert review", "usability review", "what's wrong with this screen", "give this a once-over" | `heuristic-review` | `ux-critique` |
| "we picked a direction", "ready for prototype", "hand this off" | `prototype-handoff` | `ux-critique` |

**The four pre-test skills, kept apart.** `ux-critique` asks whether it solves
the right problem. `heuristic-review` asks whether it breaks known usability
principles. `persona-check` asks where one named person gets stuck.
`accessibility-review` asks about WCAG. A request that names a screen and no
spec is usually `heuristic-review`; one that names a spec is `ux-critique`.

## Prototype

| They said | Load | Runner-up |
|---|---|---|
| "start a prototype", "localhost", "Figma Make", "publish to Pages" | `ux-prototyping` | — |
| "Brand UI shell" (Cursor / Claude Code with a shell) | `brand-prototype` | `ux-prototyping` |
| "Partner UI shell" (Cursor / Claude Code with a shell) | `partner-prototype` | `ux-prototyping` |

## Test

| They said | Load | Runner-up |
|---|---|---|
| "usability test", "test plan", "session script", "Maze study" | `test-plan` | `research-planner` |
| "accessibility", "WCAG", "keyboard path", "contrast", "screen reader" | `accessibility-review` | `ux-critique` |
| "publish the findings", "loop this back", "write it up for the team" | `test-loopback` | `synthesize-research` |

## Installing and the pack itself

| They said | Load |
|---|---|
| "install", "set up the pipeline", "new machine", "the skills are missing" | `ux-install-all-skills` (via this skill's script) |

## Tie-breaks

1. **Decision soonest.** Two skills fit → the one that unblocks the pending
   decision wins. The other gets named as the runner-up.
2. **Cheap before expensive.** `user-context` (minutes) before
   `research-planner` (weeks). Always.
3. **Single corpus vs many sources.** One Dovetail project → `synthesize-research`.
   Two or more tools → `research-synthesis`.
4. **Artifact in hand?** A mock, prototype or URL in the message pushes toward
   `ux-critique`, `heuristic-review`, `persona-check` or `accessibility-review`
   over anything that starts from scratch. No spec attached → `heuristic-review`.
5. **Shipped already?** Past tense ("we launched", "since the release") →
   `adoption-check`, not a new study.
6. **Still nothing.** Ask exactly one question: *what decision does this
   unlock?* Route on the answer.

## Connectors {#connectors}

Preflight before the first run. Say what is live, what is not, and what
degrades — then continue.

| Connector | Skills that need it | Without it |
|---|---|---|
| PostHog | `data-analyze`, `adoption-check`, `research-builder`, `user-context` (replay) | No behavioural numbers. Qual-only, and say so. |
| Dovetail | `user-context`, `synthesize-research`, `research-synthesis` | The Frame cannot be read or written. Hand-paste a corpus instead. |
| Outset | `research-planner`, `test-plan` | Study designed but not created. Output is a document to paste in. |
| Pendo | `pendo-guide-strategy`, `research-builder`, `data-analyze` (polls) | Guide copy drafted, not built. No poll data. |
| Rally | `research-builder` (audience) | No participant pool. Audience stays a description. |
| Atlassian (Jira / Confluence) | `write-spec`, `test-loopback`, `research-planner` (ticket) | Drafts in chat, nothing published. |
| Figma | `design-system`, `ideate`, `prototype-handoff` | No component or token lookup. Work from the styleguide doc. |
| BigQuery / Freshdesk | `research-synthesis`, `user-context` (tickets) | Support signal missing from triangulation. Confidence drops. |

A connector that needs authorising is the designer's to fix — connector
settings on claude.ai, or `/mcp` elsewhere. Never ask for a token.
