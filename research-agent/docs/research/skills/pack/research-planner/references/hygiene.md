# Question hygiene

Five things true before a question reaches a participant. Vague questions
produce vague research, and no amount of sample size rescues them.

---

## 1 — The question

**Specific enough to be wrong.**

| | |
|---|---|
| ❌ | "Do users like this?" |
| ✅ | "Would admins use bulk import to onboard a new team of 20?" |

If you cannot imagine an answer that disappoints you, it is not a question yet.

## 2 — The decision

**Named, and still open.**

"Should we build X?" · "Should we prioritise A over B?" If nobody can name the
decision, there is nothing for the answer to change, and the study will be read
by nobody.

## 3 — The decision owner

A **person**, not "the team" — and someone who has explicitly agreed to **wait
for the answer** before deciding. An owner who will decide on Thursday regardless
is not waiting; they are being polite.

## 4 — The outcomes

**What finding triggers what decision — written before fieldwork starts.**

For qual, write thresholds as **patterns and behaviour**, not percentages:

> If most participants hit the same blocker and have built a workaround for it
>   → we build it this quarter
> If the blocker appears but nobody has worked around it → we defer to Q3
> If participants split on whether it is a problem at all → we run a follow-up
>   on what separates the two groups

**Percentages belong to quant.** "70% mention X" at n=8 is a number the sample
cannot carry — the same error as claiming "90% of users" from eight interviews.
Reserve percentage thresholds for PostHog, Pendo, or an Outset sample large
enough to bear one, and name the instrument that will produce the number.

This is the check most teams skip, and skipping it is what lets a study confirm
whatever was already wanted. Once you have seen the data, "what counts as
enough?" stops being an honest question — every threshold you pick afterwards is
chosen knowing which side it lands on.

Agree thresholds with the decision owner, in writing, on the ticket.

## 5 — The boundaries

**What is in scope, and explicitly what is not.**

> In: admin workflows for team setup.
> Out: end-user onboarding, billing, SSO configuration.

Without boundaries, scope creeps mid-study, the sample stops matching the
question, and the readout answers something nobody asked.

---

## The test

| | |
|---|---|
| ❌ | "We're doing research to understand admin onboarding." |
| ✅ | "We're doing research because we need to decide whether to build bulk import before 1 September." |

The first has no end. The second tells you when you are finished, who is waiting,
and what would change their mind.

---

## When hygiene fails

Do not quietly fix it yourself — that produces a study answering *your*
interpretation of someone else's question.

| Missing | Do |
|---|---|
| Specific question | Draft two or three readings, ask which they meant |
| Decision | Back to intake. This should not have routed |
| Owner who'll wait | Ask directly: *"will you hold the decision until this lands?"* A no means stop |
| Thresholds | Propose numbers and get agreement. Proposing is fine; assuming is not |
| Boundaries | Draft them explicitly and have them confirmed |

A study held for two days over thresholds is cheaper than one delivered into a
decision already made.
