# Who to test with

Built from what people do, not from what they say they do.

---

## Five axes

| Axis | Values | From |
|---|---|---|
| **Side** | Partner · Brand | Account type |
| **Persona** | The six in [`user-personas`](../../user-personas/) | Never invented here |
| **Size** | Partner: programmes, monthly earnings. Brand: partner-count band, DAU tier | Account properties |
| **Feature usage** | Has done X · n times · in the last N days | **PostHog** |
| **Recency** | Active · lapsed · never | Last sign-in |

**Usage is the axis teams skip**, and it decides whether the sessions are worth
watching. A study about a feature recruited from people who have never opened it
measures first impressions. That is sometimes the question — say so when it is,
and never by accident.

## Recency changes the study

| Who | What you learn |
|---|---|
| **Active** | Why it works, where it still bites |
| **Lapsed** | Why they stopped — usually the most valuable, hardest to recruit |
| **Never** | First impressions, discoverability, whether people know it exists |

Mixing all three and reporting one number averages three different studies into
a figure describing nobody.

## Building the cohort

```
exec  call read-data-schema {"query":{"kind":"events"}}        confirm the event
exec  call cohorts-retrieve {"id": <id>}                       reuse an existing one
exec  call execute-sql { … }                                   people who did X, n times, in N days
```

Reuse an existing cohort where one fits — they are maintained, and a fresh query
quietly means something slightly different.

Hand the result to **Rally** for recruitment, scoped to the population, with
recruitment history checked so the same cooperative handful is not interviewed
for the fourth time this quarter.

## Check it before you recruit

Against **minimum viable diversity**
([`research-planner`](../../research-planner/references/rigor.md)):

- [ ] Varies on the two or three dimensions most likely to change the answer
- [ ] Not eight copies of one profile — that reads as consensus and is one story
- [ ] Recency is deliberate, not whoever answered
- [ ] Size band spans more than one tier, unless the question is tier-specific
- [ ] **Who is excluded is written down**

That last one is the honest part. A sample is defined as much by who is missing
as by who is in it, and the missing group is what the readout cannot speak for.
