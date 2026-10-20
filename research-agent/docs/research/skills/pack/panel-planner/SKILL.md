---
name: panel-planner
description: >-
  Works out who to talk to for a study, using a Rally CSV export. Checks whether
  the right people are in the panel at all, suggests who to approach based on
  what the export tells you about them, and flags anyone we have been leaning on
  too often. Use when someone says who should we talk to, can we recruit this,
  check the panel, or have we spoken to these people before.
license: Proprietary
metadata:
  stage: define
  pipeline: impact-ux-designops
  author: impact.com-ux
  input: rally-csv
---

# Panel planner

Three questions, in order:

1. Do we have the right people at all?
2. Who specifically should we approach?
3. Who have we been asking too often?

Run it before anyone writes a screener. A screener built for people who are not
in the panel wastes the design and the slot.

**Answer short.** Lead with what changes, not with everything you found. A few
lines, then one specific follow-up they can ask for — the detail stays
available, it just doesn't arrive unasked. A number earns its place by changing
a decision; the rest belongs in the artifact, where someone can go and find it.

## How to write it up

Plain words. The person reading this is deciding whether a study can happen, not
reading a report.

Say what the export does not tell you. CSV columns vary, and a column that is
missing is not a column you can guess at.

Never widen the audience quietly to make the numbers work. The study then
answers a question nobody asked, and nobody notices until the readout.

## The export

Read the header rather than assuming. What this needs, and what it is usually
called:

| Needs | Often called |
|---|---|
| Someone's id | `id`, `person_id`, `email` |
| Partner or brand | `type`, `account_type`, `role` |
| Size or tier | `partner_tier`, `programs`, `monthly_earnings` |
| Region | `country`, `region` |
| When we last spoke to them | `last_study`, `last_contacted` |
| How often they have taken part | `studies`, `participation_count` |

**If the last contacted column is missing, say so and stop after question two.**
Fatigue cannot be guessed at, and a confident "these people are fine to ask"
that nobody checked is worse than not answering.

Count people, not rows. Exports have duplicates, and a panel that looks like 400
is often nearer 260.

## 1. Do we have the right people?

Filter down one thing at a time and write the count after each step.

```
Everyone in the panel          1,240
  partners only                1,240
  Scaling Up tier                418
  EMEA                            96
  active in the last 30 days      31   <- this is what's limiting you
```

That ladder is the useful output, not the number at the bottom. It shows which
filter is doing the damage, which is the one worth negotiating.

Compare the pool against the target in
[`research-planner`](../research-planner/references/rigor.md):

| Pool against target | What to say |
|---|---|
| Five times or more | Comfortable. Recruit normally |
| Three to five times | Workable. Expect to chase, allow a longer window |
| Under three times | Tight. Flag it before the screener gets written |
| Under the target | We cannot recruit this group. Options below |

You need the multiple because most people do not reply. A panel the same size as
the target recruits nobody.

When it is short, lay out the choices and let the requester pick. Widen one
filter, and say what that costs. Use a different method, since a Pendo guide
reaches people the panel does not. Or wait and recruit into the panel first.

## 2. Who should we approach?

This is the part people usually do by hand, and the export already knows most of
it.

Sort the eligible pool by what makes someone worth talking to for this study:

**Match the behaviour, not the label.** If the study is about link generation,
someone who generates links weekly tells you more than someone whose tier says
they should.

**Spread across the thing most likely to change the answer.** Usually tenure,
size, or how heavily they use the feature. Pick two or three and spread across
them deliberately.

**Include people it went badly for.** Lapsed accounts and low earners are harder
to reach and usually say the most useful things. A panel of happy regulars
produces a comfortable study.

**Flag anyone unusual.** The partner with 200 programmes, the brand with none.
Worth one session each, never worth treating as typical.

Hand back a shortlist with a reason beside each name, not just a filtered list.
The reason is what lets someone swap one out sensibly.

## 3. Who are we over-asking?

| Last spoke to them | Treat as |
|---|---|
| Under 30 days | Leave them out. Too soon |
| 30 to 90 days | Fine, unless they are more than a third of the pool |
| Over 90 days | Fine |
| Three or more studies in a year | Flag as a regular |

The regulars are the real problem and you cannot see them without checking. The
same handful says yes to everything, gets good at being interviewed, learns the
product and the team, and gives you articulate, forgiving research that reads
like strong signal.

If regulars are more than a third of who is left, say so. It belongs in the
readout's limitations whether or not anyone changes the recruitment.

## What to hand back

```markdown
# Panel plan: [study]
[file], [n] rows, [n] actual people · [date]

## Can we run it?
[The filter ladder]
Target [n], pool [n]. [Comfortable / Workable / Tight / Not with this group]
What's limiting it: [which filter]

## Who to approach
| Person | Why them |
Spread across: [what you varied]
Worth one session: [the unusual ones]

## Who to leave out this time
Spoke to them recently: [n]
Regulars: [n], which is [n]% of the pool

## Who this won't reach
[The group the panel does not contain. This goes in the readout.]

## What the export didn't tell me
[Missing columns, and what that means you cannot answer.]
```

Send the shortlist to Rally for recruitment, and send the "who this won't reach"
line to [`research-planner`](../research-planner/). It belongs in the write-up
from the start, not added defensively at the end.
