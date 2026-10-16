# The Frame

What impact.com currently believes about its users, how confident we are in each
belief, and where we are blind. Claims, not reports.

**Live:** https://claude.ai/artifact/FHc7oAPoyohgxo87VdxCGw — ask for access.

## What's here

| Path | What it is |
|---|---|
| `index.html` | The page source. Published as the artifact above. |
| `REBUILD-PROMPT.md` | Hand this to Cursor to rebuild the page off-platform |
| `data/claims/` | 51 claims, one JSON file each — a snapshot of the store |
| `data/needs/` | 34 unmet needs, placed on the partner and brand journeys |
| `data/prompts/` | 10 starter prompts, five per side, each linked to the claims it draws on |

The page holds **no data**. Claims and needs live in the artifact's database, so
`user-context` writes to it in `record` mode without republishing the page.
`data/` is a versioned snapshot, not the source of truth — re-export after
changes.

## Getting around

Nav pills under the header jump to **Ask · Coverage · Claims · Unmet needs**,
with live counts.

## The four parts

**Ask** — put a question in plain words and get an answer built only from the
claims, with confidence, n and citations. Five starter prompts sit under the box
for each side — Partner and Brand — drawn from what the Frame actually says, not
from examples. Each is a real question the claims can engage with: why only 497
of 72,239 marketplace browsers applied, why small brands approve almost nobody,
what a creator with no clicks needs. Select a coverage cell and a starter for
that cell joins them.

They live in the `prompts` collection, so they are edited as data rather than by
republishing the page — and they should be revisited whenever the claims behind
them move. When the claims don't cover it, it
says **the Frame does not cover this** and names what research would answer it.
A refusal is a research gap, not a failure, and it is the most useful thing the
Ask box produces.

**Coverage** — best available confidence per segment × domain, computed from the
claims rather than hand-drawn. An empty cell is not a gap someone chose; it is
an area nobody has looked at.

**Claims** — the ledger. Every row carries its denominator, a link to the
Dovetail study or PostHog funnel behind it, and where a confidence level has
moved, a line saying why. Hover any confidence badge for what that level means.
**Dig into this** copies a ready-made `user-context` instruction for that claim —
paste it into Claude Code to take it apart properly.

**Unmet needs** — what people need and don't have, placed where it bites on
their journey. Severity and evidence are separate axes on purpose: high severity
on thin evidence is a research job, not a design job, and collapsing the two is
how teams build the best-documented problem instead of the worst one. Each need
links to the claims it rests on, and **Take this further** copies a
`research-intake` instruction carrying the need, who it hits, its severity and
evidence, and the claims behind it — so the front door receives a fully framed
request rather than a sentence.

The page cannot run a skill or raise a ticket itself. It hands you the exact
instruction and the handoff happens in Claude Code, where `research-intake`
decides whether it becomes a ticket, a study, or a link to an answer we already
have.

## Styling

Built on the impact.com **iui3 / vnext** design system, the same tokens as the
persona set: Sarabun, `@impactinc/frontend-theme-tokens` names so the package can
be dropped in, 8px input radius and pill radius, and the three-block light/dark
pattern. Partner blue and impact red carry audience; green, amber and red carry
confidence and severity, which are different scales and never share a hue with
the accent.

## Confidence

| | Bar |
|---|---|
| **HIGH** | Two or more **genuinely independent** sources agree · n stated · under 6 months |
| **MEDIUM** | One primary source · n stated |
| **LOW** | Anecdotal, conflicting, tiny n, or over 12 months |
| **UNVALIDATED** | Asserted, not evidenced |
| **GAP** | Nothing found. Recorded so it stops being rediscovered |

**Claims lead with what people told us; the number backs it up.** Roughly four
parts Dovetail to one part PostHog, never the other way round. Behaviour says
*what* happens and never *why*, and a Frame built the other way accumulates
numbers nobody can act on.

**Single source is MEDIUM however large the n.** A million rows from one
instrument is one instrument. Two reports drawing on the same study are one
source wearing two hats.

Only **five claims are HIGH**. That is the point, not a shortfall: nothing above
MEDIUM should carry an irreversible decision, and a Frame of confident
single-source claims is worse than no Frame because it lends authority to
guesses.

Where a claim has moved up or down, the row carries a `recalibrated` line saying
why and what would move it again.

## Contested claims

Six are flagged, and they matter more than the clean ones because each is a
figure still circulating in briefs that the research has already corrected:

| Circulating | Actually |
|---|---|
| ~90% application rejection | 42.5% of 1.86M applications |
| "55% can't discover campaigns" | 6 people |
| "40% struggle with links" | 4 people |
| "73% want personalised recommendations" | Prompted multi-select, that option listed first |
| 782,577 partners | The cohort is 849,267; DAU is ~150,300 |
| "33% cite broken UI" | No denominator given |

A contested claim never closes a research request on its own.

## Sources

Dovetail · PostHog · G2 · Gong. Counted on the page so the balance is visible —
and it is uneven: most claims rest on Dovetail, and PostHog carries the only
high-N behavioural evidence.

**Not extracted:** the NPS response project (51 raw CSV exports) and the Gen AI
and impact MCP projects. Their synthesised findings are included where another
document carries them; the raw corpora are not.

## Maintaining it

Claims are written at the close of the work that produced them, as the step that
closes the ticket. A request closed as "already answered" refreshes `verified`
on the claim it closed against.

Contradictions never overwrite. Both claims stay, the domain is marked
contested, and contested domains don't auto-close a request.

Quarterly, run [`frame-maintenance`](../skills/frame-maintenance/): it re-runs
every PostHog insight, re-reads Dovetail, and returns four verdicts — keep,
refresh, retire, contest — plus promotion, which is the one people forget.
Retirement is a field, not a delete, so a finding that stops being true isn't
rediscovered and re-believed next year.

**All-keep is the failure mode.** A review that retires nothing is a review that
didn't happen.
