---
name: research-builder
description: >-
  Builds the instruments a study needs that are not the Outset study itself: a
  Pendo in-product guide, a human interview guide, the PostHog dashboard that
  will measure the outcome, and the audience — who to test with, drawn from real
  feature usage rather than a guess. Use when someone says build the dashboard,
  write the interview guide, set up a Pendo survey, who should we test with, find
  me partners who use this feature, or build the measurement before we run.
license: Proprietary
metadata:
  stage: define
  pipeline: impact-ux-designops
  author: impact.com-ux
  builds: pendo-guide|interview-guide|posthog-dashboard|audience
---

# Research builder

Four instruments. **`research-planner` designs the study and builds the Outset
one** — this builds the rest, and the one that matters most is the dashboard,
because it gets built *before* the study runs.

| Build | When |
|---|---|
| **PostHog dashboard** | Always, if the question touches behaviour. First |
| **Audience** | Always. Who, from real usage |
| **Pendo guide** | In-product reach, large n, people you cannot recruit. Decide targeting and copy with [`pendo-guide-strategy`](../pendo-guide-strategy/) **before** building — a guide shipped to everyone returns 1–5% and burns the audience |
| **Interview guide** | Human sessions — SPRINT follow-ups, DEEP fieldwork |

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

1. **Measurement first.** Build the dashboard before recruiting. If the event
   does not exist you have found that out for free, instead of after fifteen
   sessions.
2. **An uninstrumented event returns zero**, which reads identically to nobody
   doing the thing. Never report a zero you have not confirmed is real.
3. **Target on behaviour, not on self-description.** "People who used this
   feature twice last month" beats "people who say they use it".
4. **Draft, don't ship.** Guides and dashboards are drafts until a human has
   read them. Never publish a Pendo guide to live traffic without explicit
   sign-off — it is customer-facing.
5. **Name who you excluded.** A sample is defined as much by who is missing.

## 1 — The PostHog dashboard

**Do this first, before any recruiting.** Full protocol:
[references/dashboard.md](references/dashboard.md).

1. **Name the measure** the study is meant to move, in events: what fires, on
   what surface, by whom.
2. **Check the schema** — `read-data-schema` — before building anything. This is
   the step that pays for the whole skill.
3. **Build it** — the funnel or trend, plus the breakdown that will matter, plus
   a baseline window *before* the change.
4. **Record the baseline figure** as a claim in the Frame, dated, so the
   after-reading has something honest to compare against.

> If the decisive event is not instrumented, **stop and raise an instrumentation
> ticket.** No study design recovers data that was never recorded, and a study
> run anyway will produce a confident answer to a question it cannot see.

## 2 — The audience

Who to test with, drawn from what people actually do. Full recipes:
[references/audience.md](references/audience.md).

Five axes, used together:

| Axis | From |
|---|---|
| **Side** | Partner or brand |
| **Persona** | [`user-personas`](../user-personas/) — never invented here |
| **Size** | Partner tier, brand partner-count band, DAU tier |
| **Feature usage** | PostHog: has done X, n times, in the last N days |
| **Recency** | Active, lapsed, never — three different studies |

**Build the cohort in PostHog, hand it to Rally for recruitment.** Usage is the
axis teams skip and it is the one that decides whether the sessions are worth
watching: a study about a feature, recruited from people who have never opened
it, measures first impressions and nothing else. Sometimes that is the question
— say so if it is.

Then check it against **minimum viable diversity**
([`research-planner`](../research-planner/references/rigor.md)): eight people who
all look the same give you one story told eight times, and it will feel like
consensus.

## 3 — The Pendo guide

In-product, large n, reaches people you could never recruit — and interrupts
someone mid-task, which is the cost. Full guidance:
[references/pendo.md](references/pendo.md).

- **Two or three questions.** This is an interruption, not a study
- Target by segment and page, never site-wide
- Ask about **the thing they are doing right now** — that is the whole advantage
- Set a response cap and an end date before it goes live
- Expect single-digit response rates and a satisfaction skew: the annoyed answer
  and the delighted answer, with the middle missing

**Draft only.** A Pendo guide is customer-facing; it ships when a human says so.

## 4 — The interview guide

For SPRINT follow-ups and DEEP fieldwork. Full structure:
[references/interview.md](references/interview.md).

Opens with warm-up, moves to **artefacts and tasks before opinions**, and ends
with the one question worth asking everyone. Probes are written down so two
interviewers get comparable data.

The rules in [`research-planner`](../research-planner/references/prompts.md)
apply here hardest: test the thing not the idea, no hypotheticals without a
stimulus, no yes/no comprehension questions. A human moderator can follow a
thread an AI cannot — that is the point of the format, and it is wasted on a
script that only collects agreement.

## Handoff

| Built | Goes to |
|---|---|
| Dashboard + baseline claim | The Frame, via `user-context` `record` |
| Audience cohort | Rally, for recruitment |
| Pendo guide | A human, for sign-off, then Pendo |
| Interview guide | `research-planner`, for the 3-participant pass |

Nothing here launches anything. Building is not running.

## References

- [references/dashboard.md](references/dashboard.md) — measurement before the study
- [references/audience.md](references/audience.md) — targeting on real usage
- [references/pendo.md](references/pendo.md) — in-product guides
- [references/interview.md](references/interview.md) — human session guides
