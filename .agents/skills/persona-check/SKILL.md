---
name: persona-check
description: >-
  Walks a design, flow or piece of copy through a persona as a task — where they
  hesitate, what they look for and cannot find, what they do instead — before it
  reaches real participants. A synthetic pre-test, not a verdict. Everything it
  produces is a hypothesis to test, never a finding. Use when someone says run
  this past a persona, synthetic user check, pre-test this prototype, how would
  a Scaling Up creator handle this, or check this before we recruit.
license: Proprietary
metadata:
  stage: prototype
  pipeline: impact-ux-designops
  author: impact.com-ux
  output: persona-voice
---

# Persona check

Take a design and walk one persona through it as a **task**: where they stop,
what they look for, what they do when they cannot find it.

This is a **pre-test**. It finds the obvious breakages before a real participant
spends a session on them, and it costs minutes. It does not tell you what users
think, and nothing it produces is evidence.

## The rule everything else depends on

**Everything this skill produces is Persona voice.** Never evidence.

> Never write "users said" about something a persona simulation said.

A persona check generates **hypotheses worth testing**. It cannot confirm one.
If a check and a study disagree, the study is right. Label the output, keep the
label on it when it travels into a doc, and if someone quotes a persona check in
a readout as a finding, that is the failure this rule exists to prevent.

## What it is not

| | |
|---|---|
| **`user-context` `critique`** | What the evidence *predicts* about this design. Claims, confidence, gaps |
| **`persona-check`** | Where this *person* gets stuck walking through it |
| **`ux-critique`** | Does the design cover the one-pager and the epic |
| **`accessibility-review`** | WCAG blockers, focus, contrast, keyboard |

Run the evidence one when you need to defend a decision. Run this one when you
need to find the breakages before a session. They answer different questions and
the second cannot do the first's job.

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

1. **Ground it or do not run it.** Pull the persona from
   [`user-personas`](../user-personas/) and the relevant claims from
   [`user-context`](../user-context/). An ungrounded persona is a confident
   stranger inventing a user.
2. **Refuse outside the research.** When a question falls outside what the
   persona set covers, say so and log it as a gap. A refusal is a finding about
   our coverage, not a failure of the check.
3. **One persona at a time**, named. "Users would struggle" means nobody did.
4. **Tasks, not opinions.** Never "would they like this?" — always "what do they
   do on this screen, and what happens when it is not there?"
5. **Rank by consequence**, not by how many things you found. Ten observations
   with no ordering is a list, not a review.
6. **Report where it works, not only where it breaks.** A walkthrough that only
   finds problems gives the designer nothing to protect in the next revision,
   and reads as advocacy rather than a check.
7. **Every output is a hypothesis with a test attached.** Each observation says
   what would confirm or kill it with a real participant — otherwise it is an
   opinion formatted like a finding.
8. **Mark which observations the persona card could not support.** Those are
   coverage gaps, and they belong in the output where someone will act on them.

## Workflow

```
Task Progress:
- [ ] Pick the persona, and say why that one
- [ ] Pull what we know about them here
- [ ] Set the task and the entry state
- [ ] Walk it, step by step
- [ ] Rank what broke
- [ ] Hand the top few to the real study
```

### 1 — Pick the persona

One, named, from the reference six. Say why: *who does this design have to
satisfy first, and who would it fail most expensively?*

Those are often different people. If they are, run the second one too — the
design usually survives its intended audience.

### 2 — Pull what we know

From `user-context`: the claims for this persona and this domain, with their
confidence. From `user-personas`: their JTBD, workflow and the stated gaps.

**What is thin here matters more than what is solid.** A check grounded in LOW
claims produces LOW hypotheses, and should say so up front.

### 3 — Set the task

A real one, in their words, with the state they arrive in:

> *"You have just published a video. You want the affiliate link for the product
> you mentioned. You are on your phone."*

Entry state carries most of the weight — logged out, mid-task, interrupted, on a
phone, first time, fourth time this week. The same screen is a different design
depending on how someone reaches it.

### 4 — Walk it

Step by step, in their voice, per
[references/walkthrough.md](references/walkthrough.md). At each step:

| | |
|---|---|
| **Looking for** | What they expect to see |
| **See** | What is actually there |
| **Do** | Where they click, or stall |
| **Carry** | What question they take to the next step unanswered |

That last one is where real abandonment comes from — not one bad screen, but
three screens that each left something unresolved.

### 5 — Rank what broke

Four levels, in [references/walkthrough.md](references/walkthrough.md#ranking):
**stops them · costs them · annoys them · noticed**.

Stops-them items go to the study. Noticed items go in a list and no further.

### 6 — Hand it on

The top two or three become **things to watch for** in the real sessions, not
findings in a report. Give them to
[`research-planner`](../research-planner/) as probes, so the study tests the
hypotheses instead of rediscovering them.

## Output

```markdown
# Persona check — [design]
Persona: [name, tier] · Task: [one line] · Entry: [state]
**Persona voice — hypotheses to test, not findings**

## Grounding
| Claim | Confidence | n |
|---|---|---|
_Thin where: [what we do not know about this persona here]_

## Walkthrough
| Step | Looking for | See | Do | Carry |
|---|---|---|---|---|

## What broke
| | What | Why it matters to them |
|---|---|---|
| **Stops** | | |
| **Costs** | | |
| **Annoys** | | |

## Watch for in the real sessions
1. …

## Outside what we know
[questions the persona set cannot answer — log as gaps]
```

## References

- [references/walkthrough.md](references/walkthrough.md) — running the walk, and the ranking
