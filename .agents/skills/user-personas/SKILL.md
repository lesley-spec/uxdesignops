---
name: user-personas
description: >-
  Points work at the impact.com user persona set — three partner and
  three brand personas with jobs-to-be-done, workflow maps and per-claim
  confidence. Use in Empathize to check what is already known, in Define to
  frame a problem against a named persona, and in Ideate or Test to decide who
  a concept must satisfy first.
license: Proprietary
metadata:
  stage: define
  pipeline: impact-ux-designops
  author: impact.com-ux
  audience: both
---

# User personas (Empathize / Define)

Routing skill for the reference persona set. Does not invent personas — it points at
the maintained set and says how to use and refresh it.

## Where the set lives

| Resource | Link |
|---|---|
| DesignOps personas page | https://lesley-spec.github.io/uxdesignops/personas/ |
| Frame (claims) | https://lesley-spec.github.io/uxdesignops/frame/ |
| Markdown copy (in this skill) | [references/personas.md](references/personas.md) |
| Claude artifact (Ask + live connectors) | https://claude.ai/artifact/FaBjbFu7hiM5LYBfALemAQ |

The DesignOps pages are the day-to-day view. The Claude artifact is private (Ask / live PostHog) — ask UX Research for access.

## The set

Maturity is the spine. Role sits inside each tier as a variant.

| | Persona | Who | Confidence |
|---|---|---|---|
| P1 | **Nia Bennett** | New creator, 1–3 programmes, under $500/mo | 64 / 100 |
| P2 | **Danny Alvarez** | Working creator, 5–10 brands, $500–$5k/mo | 81 / 100 |
| P3 | **Priya Shah** | Network operator, 15+ programmes, $5k+/mo | 58 / 100 |
| B1 | **Sophie Carter** | Founder-operator, wearing a million hats | 62 / 100 |
| B2 | **Maya Thompson** | Programme manager, 30–200 partners | 76 / 100 |
| B3 | **James Whitfield** | Partnerships lead, 200+ partners | 58 / 100 |

Brand personas are **roles, not company sizes** — the ladder is how much of the job is
yours: done alongside other work, done as the work, or owned but delegated.

## The organising idea

**For a partner, impact.com is a waypoint. For a brand, it is a workspace.**
Partners need speed — every second here is overhead on work happening elsewhere.
Brands need depth and control — this is where the programme is built, run and paid.
Most partner friction is speed being taxed; most brand friction is depth or control
being withheld.

## When to use

- Empathize: before commissioning research, check whether the question is already answered
- Define: name the persona a one-pager is for, and the one it is explicitly not for
- Ideate: decide which persona a concept must satisfy first
- Test: pick who to recruit, and pressure-test a concept against the Ask panel

## Tie-breaks

- **Partners** → favour Danny, unless the change removes a capability Priya depends on.
  A simplification is an inconvenience to one and a permanent loss to the other.
- **Brands** → favour Maya. Mid-market is both the heaviest user and the group most
  likely to leave.
- **Nia** wins only on signup, profile and first-link surfaces.
- **Creator vs affiliate** → unresolved. Escalate rather than guess (see Gaps).

## Confidence model

Each persona is scored 0–100 on four things, stated openly so it can be argued with:
how many people were spoken to at that tier, how many independent sources agree,
whether behavioural data corroborates the qualitative finding, and how severe the
known gaps are. It is a judgement, not a statistical measure.

**Never cite a persona claim without its denominator.** Several figures that circulated
as segment-wide rates were six or four people.

## Evidence base

| Source | Coverage |
|---|---|
| Outset — Partner Exp | 105 interviews, 13 studies |
| Outset — Mobile App Exp | 119 interviews |
| Outset — Brand Exp | 43 interviews, 7 studies |
| Outset — Contextual Inquiry 2026/27 | 12 sessions |
| Dovetail — Brand Value Stream | 37 Gong calls, founding research Sept 2026 |
| G2 | 158 brand reviews, Jan 2025 – Jul 2026 |
| PostHog | partner and brand cohorts, 90- and 180-day pulls |

Quantitative charts in the artifact are wired live to PostHog. Qualitative claims are
dated snapshots — re-check them against Outset before quoting in a decision document.

## Known gaps — do not paper over these

1. **No affiliate persona exists.** The Partner Exp screener excluded deal, coupon,
   review, email and network partners, and no partner-type field exists in product data.
   Every partner quote is a creator's. These types carry the highest median commissions.
   Highest-value study available.
2. **Nobody who signed up and never activated has been interviewed.** Every screener
   requires active use. That group is the largest by an order of magnitude.
3. **No brand in its first 90 days has been interviewed.** Sophie is built from reviews
   and telemetry only.
4. **English-only recruitment**, though just under half of partner activity is outside
   North America.
5. **Application submission is uninstrumented**, so time-to-decision cannot be measured
   on either side.

## Workflow

1. Open the artifact. Scan the comparison matrix; click through to the persona in question.
2. Check the confidence score and the named gaps before leaning on a claim.
3. Use the Ask panel to pressure-test a concept. It answers only from the evidence behind
   that card and will decline when a question falls outside it — treat a refusal as a
   research gap, not a failure.
4. Export the persona card (PNG or SVG) into the spec, deck or Figma file.
5. Name the persona and the tie-break in the one-pager.

## Output snippet for write-spec

```markdown
## Persona
- Primary: … (confidence …/100)
- Explicitly not for: …
- Tie-break if it conflicts with …: …
- Unmet need this addresses: …
- Evidence gap to flag: …
```

## Refreshing the set

- Behavioural charts refresh themselves from PostHog on load.
- Qualitative findings are snapshots. Re-read the Outset toplines when a new report runs.
- Re-score confidence when a gap closes, and say in the artifact what moved and why.
- Related lenses: `creator-affiliate-ux-persona` (partner), `brand-operator-ux-persona`
  (brand), `research-synthesis` (cross-source triangulation).

## Feedback

Slack the UX Research team.
