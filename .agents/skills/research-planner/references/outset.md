# Building the Outset study

Outset is asynchronous and AI-moderated. Its discipline is **tight and
quantitative**: under five minutes, mostly closed-ended, gated hard. That buys
30–50 responses in two to three weeks at 60–75% completion.

> Absorbed from the Outset Builder methodology.

---

## When this discipline applies — and when it doesn't

This is the important call, and it is not "always".

| The question is… | Build it |
|---|---|
| **How much?** Does this land, is it ready, which of two | **Quant-first**, as below. Closed-ended, gated, 4–8 questions |
| **What do they do?** Where do people get stuck, what is the workaround | **Behavioural**, per [prompts.md](prompts.md). Tasks, artefacts, think-aloud |

A quant Outset study cannot show you a workaround. A behavioural one cannot give
you a percentage worth reporting. Choosing wrong is the most common way an
Outset study produces a number nobody can act on.

**Where the two sets of rules meet:** [prompts.md](prompts.md) bans yes/no
*comprehension, preference and terminology* questions, because those invite
people to avoid admitting failure. It does not ban closed-ended questions. A
multiple-choice gate ("have you used this?") and a 1–5 value rating are fine. A
yes/no "did you understand it?" is not, in either mode.

---

## Shape

```
SECTION 1  SCREENING & GATE          ~30s
  Q1  Establish the audience                     MC
  Q2  Filter to the cohort that matters          MC  → gate the rest

SECTION 2  PRIMARY METRIC 1          ~1.5m
  Q3  The core outcome                           RATING or MC
  Q3a Probe, only if Q3 triggers it              MULTI-SELECT
  Q4  Did they act on it                         MC, conditional

SECTION 3  PRIMARY METRIC 2 + VALUE  ~1.5m
  Q5  Adoption / workflow                        MC
  Q6  Overall value                              RATING 1–5
  Q6a Blocker, only if Q6 < 4                    MULTI-SELECT

SECTION 4  CLOSE                     ~30s
  Q7  Follow-up consent                          MC
  Q8  Contact, only if Q7 = yes                  EMAIL
```

**4–8 questions. Under five minutes.** Every question feeds a metric; if you
cannot name the metric, cut it.

## Question types

| Type | For |
|---|---|
| **MULTIPLE_CHOICE** | Classify or segment — "which one" |
| **RATING 1–5** | Value or satisfaction — "how much" |
| **MULTIPLE_SELECT** | Reasons, capped at "pick up to 3" |
| **TEXT** | Last resort. One "anything else" at the end, if at all |

Four to five options per question, short option text, no jargon.

## Conditional logic

Three patterns, two to four branches in total. More than that and respondents
get lost.

**Gate** — Q1 decides whether the study runs at all for this person.
**Probe** — a follow-up fires only on the answers that need explaining (low
rating, surprising choice).
**Route** — the same question, different probes by segment.

A healthy probe is seen by **under 30%** of respondents. If more than 60% see
it, the gate is too loose and you have lost the time it was meant to save.

## Thresholds

Written before launch, in [hygiene.md](hygiene.md), and restated here as the
study's own success bar:

```
GO            metric 1 ≥ x% · metric 2 ≥ y% · value ≥ 4.0 avg
                and no single blocker over 40%
ITERATE       any primary metric under its bar
              one blocker over 50%
```

**Do not decide what "good" looks like after the data lands.** Half an hour
before launch costs less than an argument afterwards.

## What does not belong in the study

**Demographics.** Company size, role, budget and tier come from the screener and
from Rally, not from questions that eat the respondent's five minutes. Outset is
for learning about the thing; profiling is a separate concern and a faster one.

---

## Before you launch

- [ ] Hypothesis is falsifiable — a "no" is possible
- [ ] Every question feeds a named metric
- [ ] 80%+ closed-ended
- [ ] Gating removes 0–30%, not more
- [ ] Fewer than three conditional probes
- [ ] Runtime under five minutes
- [ ] Success bars agreed with the decision owner, in writing
- [ ] Someone outside the team read it for jargon

Then the 3-participant pass ([rigor.md](rigor.md)) before the rest runs — a
tight study can be tightly wrong, and three responses is where you find out.
