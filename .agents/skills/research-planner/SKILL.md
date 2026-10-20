---
name: research-planner
description: >-
  Turns a routed research request into a study that is actually worth running.
  Applies question hygiene, sets go/no-go thresholds, designs prompts that test
  the thing rather than the idea, picks a sample and its diversity, builds the
  study, runs the 3-participant rigor pass before the rest launches, and updates
  the UX ticket as it goes. Use after research-intake routes a request, or when
  someone says plan a study, design the research, write the discussion guide,
  set up the Outset study, or draft a screener.
license: Proprietary
metadata:
  stage: empathize
  pipeline: impact-ux-designops
  author: impact.com-ux
  picks-up-from: research-intake
---

# Research planner

Takes a **routed** request and makes it a study worth running.

Intake decided *whether* and *what shape*. This decides *how* — and the gap
between those is where most research quietly fails, by testing the idea of a
thing instead of the thing, or by discovering at participant 12 that the question
was wrong at participant 1.

> Question hygiene, prompt design, the 3-participant pass and sample guidance
> follow Constantine Papas, *AI-Powered UX Research*, chs. 7–8 and the Outliers
> Booking keynote.

## Where it sits

```
research-intake ──routed──→ research-planner ──findings──→ user-context (record)
     creates ticket             updates ticket              writes the claim
```

**Intake owns the ticket's triage fields; this skill owns the plan fields and the
transitions.** Never rewrite intake's sections — the record of *why this was
routed* has to survive the study.

| Writes | |
|---|---|
| Intake | Question · Decision · What we already know · Route · Who runs it |
| **Planner** | Method · sub-questions · sample · probes · thresholds · pass result |

Only **routed** requests arrive here. Closed, reframed, instrument-first and
provisional outcomes end at intake.

## Integrity

1. **Draft, don't decide.** This skill writes the first version of everything —
   design, screener, guide, probes. A human finalises, sets the boundaries, and
   owns what goes to participants.
2. **Thresholds before fieldwork.** "If most participants work around it, we
   build" is written *before* anyone is recruited. Deciding what counts after
   you've seen the data is how research confirms whatever was already wanted.
   Write qual thresholds as patterns, not percentages — a percentage at n=8 is
   a number the sample cannot carry.
3. **The 3-participant pass is not optional.** No mode skips it. It is the
   difference between fixing a broken study at participant 3 and discovering it
   at participant 15.
4. **Test the thing, not the idea of the thing.**
5. **Never launch recruitment without the research lead saying so.**

## Workflow

```
Task Progress:
- [ ] Pick up the ticket
- [ ] Question hygiene — sharpen until it is answerable
- [ ] Thresholds — what finding triggers what decision
- [ ] Sample — size and diversity
- [ ] Design — prompts, probes, screener, guide
- [ ] Human review — boundaries set, leading questions removed
- [ ] Build it
- [ ] 3-participant pass
- [ ] Launch the rest
- [ ] Readout → hand to user-context
```

### 1 — Pick up the ticket

Read the intake ticket (`getJiraIssue`). You need the scoped question, the mode,
the decision and its owner, the date, and **what the Frame already covered** —
that last one narrows scope and stops you re-asking a settled question.

### 2 — Question hygiene

Five things must be true before a question reaches a participant. Full checklist
and the anti-patterns: [references/hygiene.md](references/hygiene.md).

| | |
|---|---|
| **The question** | Specific, not "do users like this?" |
| **The decision** | Named. No decision, no research |
| **The decision owner** | A person who has agreed to wait for the answer |
| **The outcomes** | What finding triggers what decision — **before** fieldwork |
| **The boundaries** | What's in scope, and explicitly what isn't |

Intake checked that a decision exists. This checks the question can actually
answer it.

> **Anti-pattern:** "we're doing research to understand X."
> **Pattern:** "we're doing research because we need to decide whether to build X
> by 1 September."

### 3 — Sample

Concrete numbers, not "enough interviews":

| Mode | Target | Notes |
|---|---|---|
| **MICRO** | 8–15 | Min 5 if patterns are obvious by 3; diminishing returns past 15 |
| **SPRINT** | 15–20 Outset, **5** human follow-ups | Follow-ups on days 7–10 |
| **DEEP** | 12–15 | Min 8 if homogeneous; 5–7 per segment if multi-segment |

**Minimum viable diversity**, not representativeness. You need *variation* to
catch edge cases and common paths — eight identical admins give you one story
told eight times. See [references/rigor.md](references/rigor.md).

### 4 — Design

Where most studies are won or lost. Principles with worked
anti-pattern/pattern pairs: [references/prompts.md](references/prompts.md).

- **Test the thing, not the idea.** Not "would you use bulk import?" but "here's
  the screen and a CSV — what would you do?"
- **No hypothetical futures** without a prototype in front of them. People are
  bad at predicting their own behaviour and generous about yours.
- **Probes specific enough for consistent AI follow-up.** "Ask about their
  workflow" produces a different conversation per participant and uncomparable
  data. Tighter in MICRO, where there is no second chance; looser in SPRINT,
  where human follow-ups adjust on the fly.
- **No yes/no questions.** "Do you understand this?" invites people to avoid
  admitting failure. Ask them to *do* or *recall* something instead.

Draft the screener, the guide and the probes. Then stop — a human reviews for
leading questions, scope creep and domain nuance before anything is built.

### 5 — Build it

Create the study, sections, screener and quotas. Configure recruitment. **Do not
launch.** Validate, show the research lead what will go out, and wait.

**For an Outset study**, follow [references/outset.md](references/outset.md):
under five minutes, 4–8 questions, mostly closed-ended, gated hard. That file
also carries the call it is easy to get wrong — whether this study is measuring
**how much** (quant, closed-ended) or **what people do** (behavioural, tasks).
A quant study cannot show you a workaround; a behavioural one cannot give you a
percentage. Picking wrong is how a study produces a number nobody can act on.

Demographics come from the screener and Rally, never from questions that eat the
respondent's five minutes.

### 6 — The 3-participant pass

**Review the first three end-to-end before the rest runs.** Per mode:
[references/rigor.md](references/rigor.md).

Read the raw transcripts, not the AI summary. Then decide: **proceed, fix, or
pivot.** Record which, and why, on the ticket.

This is the single cheapest piece of rigor available. It is not gatekeeping — it
is staying curious long enough to notice the study is asking the wrong thing.

### 7 — Launch the rest

Only after the pass, and only on the research lead's go.

### 8 — Readout

Four questions, in order — including the one most readouts omit. Structure:
[references/readout.md](references/readout.md).

1. What did you ask?
2. What did you find?
3. What does it mean for the decision?
4. **What can't it tell you?**

State findings as **observations, not recommendations.** "6/8 admins mentioned
bulk import; current workaround is one-by-one creation" lets the reader decide.
"We should build bulk import" is your opinion wearing research's clothes.

Then hand the claims to `user-context` in `record` mode. **A study that doesn't
write back doesn't compound** — and transition the ticket closed.

## References

- [references/hygiene.md](references/hygiene.md) — the five checks, thresholds
- [references/prompts.md](references/prompts.md) — prompt design, with pairs
- [references/outset.md](references/outset.md) — building the Outset study: shape, question types, gating, thresholds
- [references/rigor.md](references/rigor.md) — sample sizes, diversity, the pass
- [references/readout.md](references/readout.md) — readout structure and tone
