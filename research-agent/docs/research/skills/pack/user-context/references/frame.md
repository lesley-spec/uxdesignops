# The Frame

**What we currently believe about our users, how confident we are, and where the
gaps are.** Not an archive of what we studied.

The shift that matters: a research repo is **narrative** — reports, stored whole,
read start to finish by nobody. The Frame is **claims** — facts with IDs,
deduplicated, dated, graded, queryable. When a study lands, the narrative is
thrown away and the facts are kept.

> Structure after Constantine Papas, *AI-Powered UX Research*; claims-pool model
> after Kelly's framework (Outliers Insights keynote).

```
THE FRAME
├─ WHO ARE OUR USERS ──────→ user-personas (not duplicated here)
├─ JOBS TO BE DONE            what they are trying to accomplish
├─ UNMET NEEDS & GAPS         what we know they need and don't have
├─ COVERAGE MATRIX            segment × domain — where we're deep, where we're blind
├─ BELIEF MAP                 claims with confidence + evidence
├─ CLAIMS POOL                the deduplicated, queryable facts
└─ MAINTENANCE LOG            what changed, what's stale, what's next
```

---

## The claims pool

One row per claim. This is the whole data model.

| Field | |
|---|---|
| `statement` | One falsifiable sentence: subject + behaviour + direction |
| `audience` | `Partner` · `Brand` · `Both` |
| `segments` | Array of `partner:getting-started` · `…:scaling-up` · `…:strategic-growth`, and the `brand:` equivalents |
| `domain` | One of: Onboarding · Discovery · Approval & vetting · Links & tracking · Reporting · Payouts · Mobile · Platform |
| `confidence` | HIGH · MEDIUM · LOW · UNVALIDATED · GAP ([evidence.md](evidence.md)) |
| `n` | Sample size. Never omitted — a claim without an n cannot be bounded |
| `source` | Where it came from, named well enough to find again |
| `scope` | What it covers, and what it does not |
| `verified` | `YYYY-MM-DD` — when someone last confirmed it |
| `contested` | `true` when another claim disagrees. Contested claims never close a request |
| `caveat` | The qualification a reader needs: the denominator problem, the sampling issue, the thing it does not cover |

The document id is the claim id — stable and citable, because a claim gets
referenced from one-pagers and epics. `GAP` is a real confidence level: a
recorded known-unknown stops being rediscovered next quarter.

**Lead with the finding, not the figure.** "Most creators never get a click —
69% have never driven one" is a claim. "69% of creators have never driven a
click" is a statistic, and the reader has to do the interpreting themselves.

**The statement must be falsifiable.** "Partners find payouts confusing" matches
every payout question and settles none of them. "Scaling Up creators abandon
payout setup more often than established affiliates" settles one.

**Scope is doing real work.** A claim about Scaling Up creators is not a claim
about partners. Most wrong answers from a Frame come from reading a scoped claim
as a general one.

### Where it lives

**The Frame is built.** It is an Artifact with a database:

> **https://claude.ai/artifact/FHc7oAPoyohgxo87VdxCGw**

Two collections: `claims` and `needs`. Read and write them with the
`ArtifactData` tool, passing that URL. The page holds no data of its own, so
writing a claim does **not** mean republishing the page — the view updates on its
own.

A snapshot lives in `frame/data/` in the `ux-research` repo for versioning and
grep. It is a snapshot, not the source of truth: re-export after changes rather
than editing it.

### The needs collection

The other half, and the one designers actually open. One row per unmet need.

| Field | |
|---|---|
| `need` | What they need and do not have, in their terms |
| `audience` | `Partner` · `Brand` |
| `stage` | Where it bites. Partner: Join & set up · Discover brands · Apply & get approved · Generate links · Promote · Track performance · Get paid. Brand: Commit · Integrate & configure · Recruit · Activate · Measure · Pay · Protect |
| `severity` | `blocking` (people stop or leave) · `major` (costs real time weekly) · `watch` (named, not yet sized) |
| `evidence` | HIGH · MEDIUM · LOW — how well we know it |
| `segments` | Who it hits |
| `claims` | Array of claim ids that evidence it |

**Severity and evidence are separate on purpose.** A need can be blocking on thin
evidence, or well-evidenced and minor. The gap between them is the useful part:
high severity on low evidence is a research job, not a design job. Collapsing the
two is how a team builds the best-documented problem instead of the worst one.

Every need links to the claims behind it. A need with no `claims` is an opinion.

---

## Coverage matrix

**Segment × problem domain.** The point is not what we know; it is seeing, at a
glance, what we **don't**.

| | Onboarding | Payouts | Discovery | Reporting |
|---|---|---|---|---|
| Getting Started | 🟢 | 🟡 | 🔴 | 🔴 |
| Scaling Up | 🟢 | 🟢 | 🟡 | 🟡 |
| Strategic Growth | 🟡 | 🔴 | 🔴 | 🟡 |

🟢 HIGH-confidence claims, current · 🟡 thin, stale, or single-source · 🔴 nothing

Two different reds, and they need different responses:

- **Gap** — we know we don't know. Routes to research.
- **Blindspot** — we didn't know to look. Only the matrix surfaces these, and
  only by making the empty cells visible next to the full ones.

**The matrix is computed, not maintained.** It derives from the claims — best
available confidence per segment and domain — so it cannot drift from them, and
nobody has to remember to update it. Add a claim and the cell changes.

Review it quarterly anyway. A matrix nobody looks at is a diagram, not a tool.

---

## Belief map

The claims that are currently **load-bearing** — the ones decisions rest on —
with confidence shown, not hidden.

> "Onboarding time is the #1 friction for admins" — **HIGH**, n=12, [CI video],
> [support cluster], last verified 2026-08

Broadcasting uncertainty is the point. A belief map that shows only confident
claims teaches the organisation that research is certain, and then one stale
claim quietly steers a quarter.

---

## Writing to the pool

### When

**At the close of the work that produced the finding**, as the step that closes
the ticket — never as a chore afterwards. The researcher has shipped the finding
and the requester is happy; nothing in that moment rewards going back to update
an index.

Four events write:

| Event | Writes |
|---|---|
| A MICRO answered | The answer, as one claim |
| A SPRINT brief | One claim per sub-question |
| A DEEP report | The claims, plus new JTBD or unmet needs |
| **A request closed as already-answered** | **A fresh `verified-on`** on the claim it closed against |

That last one is free and easy to forget. Closing against a claim means someone
checked it today and it held.

### Dedup

Before adding, search the pool. If a claim already says this:

- **Same scope, agrees** → refresh `verified-on`, add the new source. Do not
  create a second row.
- **Narrower scope** → add as its own claim, linked to the broader one.
- **Disagrees** → see below.

Duplicate claims are how a pool becomes a repo again.

### Contradictions

**Never overwrite.** Keep both claims, mark the domain `contested`, and record
what differs — scope, date, method, or genuine disagreement.

**Contested domains do not auto-close an intake request.** They route to a human
regardless of confidence. An unsettled question that looks settled is the most
expensive state the Frame can be in.

---

## Maintenance

Continuous updates as work lands, plus a quarterly review. **The quarterly is
load-bearing.** Skip it and the Frame degrades silently while still looking
authoritative — which is worse than having no Frame, because decisions keep being
made against it.

### Quarterly review questions

- What did we learn this cycle that **updates** what we believed?
- What did we find that we still **cannot explain**?
- What would we **do differently**?
- Coverage matrix — where are our **blindspots**?
- What used to be true and **isn't any more**? Retire it.

### Decay

Claims age at different rates. A JTBD is stable for years; a claim about a
screen dies the day the screen ships.

| Signal | Do |
|---|---|
| Past its review date | Drop one confidence level, flag `staleness` |
| The thing it describes has shipped or changed | Retire it — do not downgrade |
| 12+ months and nobody has cited it | Review for retirement |

**Retirement is a feature.** A Frame that only grows is a Frame nobody trusts.
Record what was retired and why in the maintenance log — "this used to be true"
is itself useful knowledge.

### Know when to say "talk to a researcher"

The Frame should name its own limits. When the matrix cell is 🔴, or the best
claim is LOW, the honest output is not a hedged answer — it is *this is not
something we know, and here is the cheapest way to find out*.

---

## Seeding

**Already done** — the Frame opened with 51 claims and 34 needs drawn from the
Partner and Brand Value Stream founding research, Outset, G2, the marketplace NPS
corpus, PostHog and Gong. What follows applies to seeding a new domain.

An empty Frame closes nothing, so nobody trusts it, so nobody maintains it.

| Seed from | Gives |
|---|---|
| Existing context briefs | Claims already graded, with sources |
| Outset topline reports | Study-level claims, already with n |
| Dovetail project insights | The qual backbone |
| Known gaps | 🔴 cells worth recording as known-unknowns |

Record the known-unknowns explicitly. A gap that is written down stops being
rediscovered by whoever asks next quarter.
