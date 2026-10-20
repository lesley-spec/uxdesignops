---
name: user-research
description: >-
  The gate brief: deep-dives one finding and says whether the evidence is enough
  to confirm a problem worth solving, or what is still missing. States the
  hypothesis, the evidence against it, and what the current evidence cannot tell
  you. Hands routing to research-intake and study design to research-planner.
  Use when designing the case for a problem, probing a Research Insight Monitor
  finding, mapping evidence gaps before Define, or looping Test findings back.
license: Proprietary
metadata:
  stage: empathize
  pipeline: impact-ux-designops
  author: impact.com-ux
---

# User research (Empathize)

On-demand Empathize skill. Complements the scheduled **Research Insight
Monitor**; does not replace the human gate.

**Scope, since three skills sit near this one:**

| Want | Use |
|---|---|
| Should this be researched at all, and how big? | `research-intake` |
| **Is what we have enough to confirm a problem?** | **this skill** |
| Design the study, screener, probes, Outset build | `research-planner` |
| What do we already know about X, across all sources? | `user-context` |

## Integrity

1. Prefer verified sources over model recall.
2. Label **Verified** vs **AI interpretation**.
3. Never invent quotes, metrics, or participant counts.
4. **State the hypothesis and what would falsify it.** A brief that cannot come
   back negative is not a brief, it is a case for something already decided.
5. **Carry the evidence against.** Every brief lists what argues the other way,
   or says plainly that nobody looked.
6. **Bound language to the sample.** Counts below n≈30, never percentages on
   qual.
7. Stop at the gate — recommend; designer decides.
8. If quant N is tiny or qual matches are empty/off-topic, recommend **fieldwork
   or monitor**, not "confirm problem."

See [references/integrity.md](references/integrity.md).

## When to use

- Deep-dive one monitor finding before Define
- Decide whether a problem is evidenced well enough to frame
- Map evidence gaps blocking the human gate
- Loop Test findings back as Empathize input

## Workflow

| # | Step | The move that matters |
|---|---|---|
| 1 | **Frame** | Who, JTBD, and the decision this unlocks — plus **who owns that decision** |
| 2 | **Hypothesis** | State it so it can fail. Write what finding would falsify it |
| 3 | **Inventory** | Report + MCP; mark Brand / Partner / Shared; cite every claim |
| 4 | **Counter-sweep** | What argues against the hypothesis? Who doesn't have this problem? |
| 5 | **Gaps** | Prefer `research-synthesis` / `data-analyze` before new fieldwork |
| 6 | **Set the bar, then recommend** | Say what would be *enough* before you weigh what you have — see below |
| 7 | **Hand off** | Fieldwork needed → `research-planner`. Not yet routed → `research-intake` |

### Step 6 — say what "enough" means, before you judge what you have

"Is there enough evidence?" has no answer until someone says what enough is.
Write the bar first, then test the evidence against it:

| Decision this unlocks | Bar |
|---|---|
| **Build it** | HIGH — two independent sources, one behavioural, current |
| **Deprioritise it** | MEDIUM is enough; the cost of a wrong no is lower |
| **Reframe the problem** | MEDIUM, plus agreement on what the problem actually is |
| **Change something small and watch** | MEDIUM with a measure already instrumented |

Then the recommendation is a comparison, not a judgement call — and the reader
can disagree with the bar rather than with you.

### Step 2 — make the hypothesis falsifiable

| Level | Example | Problem |
|---|---|---|
| Confirmatory | "Why do partners love the marketplace?" | Collects only positives |
| Exploratory | "What works and what frustrates in the marketplace?" | Balanced, but cannot be wrong |
| **Hypothesis-driven** | "Proposal drop-off is caused by unclear commission terms, not by form length. Falsified if participants complete it with terms hidden, or abandon it with terms shown." | Can change the plan |

Write at level three. The brief is stronger when it names the result that would
stop the work.

## Output template

```markdown
# Research brief — [topic]

## Decision this unlocks
[One sentence] · **Owner:** [named person] · **Needed by:** [date]

## Hypothesis
[Statement] · **Falsified if:** […]

## What we already know (Verified)
- … (source, date, n, link)

## What argues against it
- … (or: "counter-evidence not found — searched Dovetail, PostHog, Freshdesk")

## Frequency vs importance
| Signal | How often | What it cost them |
|---|---|---|

## AI interpretation
- …

## Gaps blocking "problem worth solving"
- …

## What this evidence cannot tell you
- Segments absent · window limits · instruments missing · questions never asked

## Recommendation for human gate
- [ ] Enough evidence to confirm problem
- [ ] Need fieldwork first → `research-planner`
- [ ] Deprioritize / monitor only
Rationale (cite Verified only):

## Action for designer (next 24h)
1. …
```

## Prompt examples (tested)

1. `Use user-research on MLW: 32% drop slideout→create and 46% overall to copy. Do we have enough to confirm a problem, or do we need fieldwork?`
2. `Use user-research on PublisherPro link gen (14 open → 0 generated). Gate recommendation plus what the evidence can't tell us.`
3. `Use user-research for UPS details→send proposal (large Partner volume). What must we still ask before Define?`

## Anti-patterns

- **A brief with no disconfirming section** — it means nobody looked
- **An unfalsifiable hypothesis** — "users find this confusing" cannot come back no
- Designing the study here instead of handing to `research-planner`
- Jumping to Ideate solutions
- Confirming a problem on low-N or empty triangulation
- Percentages on qual samples
- Shipping AI summaries past the human gate
