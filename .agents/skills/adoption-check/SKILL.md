---
name: adoption-check
description: >-
  Checks what actually happened after something shipped. Reads the baseline from
  the Frame, re-runs the measure in PostHog, says whether the research held, and
  writes the outcome back as a claim. Closes the loop from research to decision
  to result. Use when someone says did it work, check adoption, what happened
  after we shipped, did the research hold up, or post-launch check.
license: Proprietary
metadata:
  stage: test
  pipeline: impact-ux-designops
  author: impact.com-ux
  closes: research-decision-outcome
---

# Adoption check

Something shipped. Did it do what the research said it would?

This is the step almost every research process is missing, and the one that
turns a Frame from a library into evidence that research changes outcomes. It is
also the only honest way to find out whether we were right.

## Why it matters more than it looks

**It makes research defensible.** "We found X, we built it, usage moved" is an
argument. "We found X" is a document.

**It corrects the Frame with reality.** A claim that predicted something which
did not happen is the most valuable claim to find, and the only way to find it
is to look.

**It is how the Frame learns from shipping**, not only from studies. Most of
what an organisation learns about its users, it learns by changing something and
watching. Almost none of that reaches the research record.

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

1. **The baseline is not optional.** No before, no check. Reconstructing one
   afterwards is storytelling.
2. **Report what happened, including when it is nothing.** A flat line is a
   finding. A drop is a more important one.
3. **Adoption is not success.** People using a thing is not people being helped
   by it. Say which you measured.
4. **Never claim the ship caused the change** without saying what else moved.
   A launch, a season, a pricing change and a migration all look identical in a
   line chart.
5. **Write the outcome back whatever it says.** A check that only gets recorded
   when it flatters the research is worse than no check.
6. **A move inside normal variation is not a move.** Before calling anything a
   result, look at how much the measure swings on its own.
7. **This instrument cannot tell you whether it helped.** It reads behaviour.
   Whether the change made anyone's job better is a different question, with a
   different instrument.

## Workflow

```
Task Progress:
- [ ] Find the claim and its baseline
- [ ] Re-run the measure
- [ ] Compare honestly
- [ ] Check the move against normal variation
- [ ] Name what else could explain it
- [ ] Write the outcome back
- [ ] Say what it means for the belief
```

### 1 — Find the claim and its baseline

The one-pager's **predicted outcome** is the threshold you are checking against
([`write-spec`](../write-spec/) records it: measure, from, to, by when, and what
would mean it failed). Read it before you look at today's number — knowing the
figure first is how a prediction quietly becomes whatever happened.

From the Frame: the claim the decision rested on, and the baseline figure
recorded before the change
([`research-builder`](../research-builder/references/dashboard.md) writes it).

**No baseline?** Say so and stop. You can still read today's number — but it is
a new baseline for next time, not a verdict on this change. Record it that way.

### 2 — Re-run the measure

Same insight, same definition, same filters. Full protocol:
[references/measure.md](references/measure.md).

```
exec  learn -s "<topic>"                   once, first, alone
exec  call insight-query {"insightId": "<short_id>"}
exec  call dashboard-insights-run {"id": <id>}
```

**Re-run the original, do not rebuild it.** A rebuilt query means something
slightly different, and the difference will be invisible and the size of your
finding.

Give the change a fair window: at least a fortnight of post-ship data, longer if
usage is weekly or monthly.

### 3 — Compare honestly

| Reading | Means |
|---|---|
| **Moved as predicted** | The research held. Say so, and promote the claim |
| **Moved less than predicted** | Partly held. Which part did not? |
| **Did not move** | The change did not reach people, or did not matter. These are different — check exposure before concluding |
| **Moved the wrong way** | The most valuable result. Find out why before anyone reverts |
| **Cannot tell** | Instrumentation or window. Say so plainly rather than picking a story |

**Check exposure before concluding.** A feature nobody saw cannot have failed.
Separate *did they encounter it* from *did it help*, every time — conflating
them is how a discovery problem gets rebuilt as a value problem.

**Then check the move against the noise.** Pull the same measure for the four
periods *before* the baseline and look at how far it swings with nothing
happening. A change smaller than that ordinary swing is not a finding, however
much you want it to be.

| Move vs ordinary swing | Say |
|---|---|
| Clearly larger, sustained across the window | A result |
| Similar size, or only in one week | "Within normal variation — not readable yet" |
| Larger but only at the start | Novelty. Re-read in a month |

**And when the question is whether it *helped*, stop here.** This skill reads
usage. Routes for the other half:

| Question | Instrument |
|---|---|
| Did more people do it? | This skill |
| Did it make the job easier? | MICRO study — `research-planner` |
| What do the people who hit it say, in the moment? | In-product ask — `pendo-guide-strategy` |
| Did support load change? | Freshdesk via `research-synthesis` |

### 4 — Name what else could explain it

Before attributing anything, list what else moved in the window: other releases,
seasonality, a pricing or packaging change, a migration, a marketing push, an
instrumentation change.

**If you cannot rule them out, say the change is consistent with the research
rather than caused by it.** That sentence costs nothing and protects every
future claim you make.

### 5 — Write the outcome back

A new claim in the Frame, via [`user-context`](../user-context/) `record`:

```
statement   After <change>, <measure> went <figure> to <figure>
confidence  MEDIUM     one instrument, however large the n
n           <people, window>
source      PostHog: <insight>, read live <date>
caveat      Baseline <date>. Also in this window: <what else moved>.
            Predicted by <claim id>; outcome <held | partly | did not>.
```

Then update the original claim: a prediction that held is a **promotion**
candidate — behaviour now corroborates it, which is a second independent source
([`frame-maintenance`](../frame-maintenance/references/verdicts.md)). One that
failed gets `contested` or retired, with the reason.

### 6 — Say what it means for the belief

One paragraph, in the ticket and to the decision owner:

> We believed **[claim]**. We shipped **[change]**. **[What happened]**. So the
> belief is **[stronger / narrower / wrong]**, and the next thing worth knowing
> is **[question]**.

That is the whole product. Everything above exists to let you write it honestly.

## What this is not

Not an experiment. Without a control you are reading a before and an after, and
you should say so. When the decision is big enough to need causality, that is an
A/B test — and the honest version of this check says when it is out of its depth.

## References

- [references/measure.md](references/measure.md) — re-running the measure, windows, exposure
