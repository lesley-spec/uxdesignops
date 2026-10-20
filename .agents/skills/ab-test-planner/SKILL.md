---
name: ab-test-planner
description: >-
  Plans an online experiment properly. Works out the sample size from a real
  baseline, how long it has to run, what the guardrails are, and what each
  outcome means before anyone looks at the numbers. Use when someone says run an
  experiment, A/B test this, how many users do we need, is this result
  significant, or should we ship it.
license: Proprietary
metadata:
  stage: test
  pipeline: impact-ux-designops
  author: impact.com-ux
  answers: did-this-change-cause-that
---

# A/B test planner

The one method that tells you what **caused** what. Everything else in this
pipeline reads a before and an after and has to be honest about the difference.

Expensive in traffic and time. Worth it when a decision is big enough that
being wrong matters more than being quick.

**Answer short.** Lead with what changes, not with everything you found. A few
lines, then one specific follow-up they can ask for — the detail stays
available, it just doesn't arrive unasked. A number earns its place by changing
a decision; the rest belongs in the artifact, where someone can go and find it.

## First, the name collision

We have two things called A/B and they are not the same instrument.

| | What it is | n |
|---|---|---|
| **This** | A live experiment. Half the traffic sees each version, and the numbers tell you which worked | Thousands |
| [Outset A/B](../research-planner/references/outset.md) | A preference test. The same task on both versions, then you ask which they would use and why | 20 to 30 |

The Outset one tells you *why* someone prefers something. This one tells you
*whether* it moved anything. If you want both, and you usually do, run the small
one first to shape the change and this one to confirm it.

Picking this when you wanted the other is the expensive mistake. Thousands of
users and three weeks to learn something eight people could have told you in an
afternoon.

## Before you plan anything

**Can we even measure it?** Run [`measurable-check`](../measurable-check/) first.
An experiment against an event nobody instrumented returns zero on both arms,
and that looks exactly like no difference.

**Do we have the traffic?** Work out the sample size before you design anything
else. Most of the time this is where it ends, and finding that out now costs
nothing.

**Do we know what we are changing and why?** If the answer is "let's see what
happens", you are not ready. That produces a number nobody can interpret.

## The rules that keep this honest

1. **Say which way it should go, and by how much, before you start.** A
   prediction you can be wrong about is the whole point.
2. **One primary metric.** Plus one or two guardrails. Three primary metrics
   means you will find something that moved and call it the result.
3. **Do not look early.** Checking as you go and stopping when it looks good
   makes a real result out of noise. Checking for *harm* is different and
   allowed. Set that threshold up front so the two never get confused.
4. **One change per variant.** Change three things and a win tells you nothing
   about which one did it.
5. **Say what inconclusive costs.** It is the most likely outcome and the one
   nobody plans for.
6. **Write the result back whatever it says**, via
   [`user-context`](../user-context/) `record`. A test that only gets recorded
   when it wins is worse than no test.

## 1. The prediction

> We think **[change]** will move **[metric]** **[up or down]** by about
> **[how much]** for **[who]**, because **[what makes us think so]**.

That last clause is where the Frame earns its keep. "Because partners told us
they click save repeatedly when nothing confirms it [p07, MEDIUM, n=11]" is a
reason. "Because it feels cleaner" is a hunch, and a hunch is fine as long as
you say that is what it is.

An experiment with no reason behind it is a lottery ticket you waited three
weeks for.

## 2. The metrics

**Primary.** One. The thing the change is meant to move. Say exactly how it is
counted and over what window, so nobody argues about the definition afterwards.

**Guardrails.** One or two things that must not get worse while the primary
improves. Usually revenue, retention, or support volume. A conversion lift that
doubles the support queue is not a win, it is a cost moved somewhere nobody is
measuring.

**Not the primary:** clicks and time on page, when what you care about is
revenue or people staying. A proxy metric will move and tell you nothing.

## 3. How many people

Work this out from our actual baseline, not from a table someone wrote down.

Two numbers go in. The **baseline**, which is what the metric does today, pulled
live from PostHog rather than remembered. And the **smallest change worth
knowing about**, which is a judgement: a 1% lift might be worth millions or
worth nothing, and only the team can say.

At 80% power and 95% significance, two-sided:

```
n per variant = 7.849 × ( p₁(1-p₁) + p₂(1-p₂) ) ÷ (p₂ - p₁)²
```

Which gives, for a few common cases:

| Baseline | Smallest lift worth knowing | Per variant | Total |
|---|---|---|---|
| 5% | 20% relative (5.0 → 6.0) | ~8,200 | ~16,400 |
| 10% | 15% relative (10.0 → 11.5) | ~6,700 | ~13,400 |
| 20% | 10% relative (20.0 → 22.0) | ~6,500 | ~13,000 |
| 40% | 10% relative (40.0 → 44.0) | ~2,400 | ~4,800 |
| 60% | 5% relative (60.0 → 63.0) | ~4,200 | ~8,400 |

These were computed from the formula above, not copied. Check them yourself
against Evan Miller's calculator or whatever PostHog gives you, and if a number
here disagrees with a tool, trust the tool and fix this table.

**The pattern worth internalising:** the smaller the change you want to detect,
the more people you need, and it gets worse fast. Halving the lift you care
about roughly quadruples the sample. Most experiments that never reach
significance were asking to detect something too small from the start.

## 4. How long

```
weeks = (n per variant × 2) ÷ (daily eligible users × share exposed) ÷ 7
```

**At least two full weeks**, whatever the arithmetic says, so you capture a
whole weekly cycle. Partner behaviour on a Tuesday is not partner behaviour on
a Sunday.

**At most four.** Past that, the novelty of a new thing has worn off and
something else has usually shipped on top of your test.

**If it needs more than eight weeks, stop.** The honest answer is that we do not
have the traffic for this question. Options, in order of how much we like them:

1. Ask a bigger question. A change you expect to move things more needs fewer
   people to detect.
2. Go qualitative. Eight people watched closely will tell you more than an
   underpowered experiment, and will tell you *why*.
3. Ship it on judgement and use [`adoption-check`](../adoption-check/)
   afterwards, saying plainly that it is a before and after rather than an
   experiment.

Option 3 is legitimate. Option 3 described as an experiment is not.

## 5. What each result means, agreed now

Write this down before launch. After the numbers land, everyone has an opinion
about what counts.

| | Means | Then |
|---|---|---|
| **Ship** | Primary moved by at least the lift you named, at 95%, and guardrails held | Ship it. Record it as a claim |
| **Iterate** | Right direction, not significant | Usually means the change was too small, not that the idea was wrong. Make it bigger, do not just run longer |
| **Reject** | No movement, or it went the wrong way | The most useful outcome. Find out why before anyone reverts |
| **Inconclusive** | Not enough signal either way | **Not a quiet win.** Say it plainly. Nothing was learned and that is worth knowing |

**Rollback:** if [guardrail] drops by [number], stop the test immediately. That
is a safety check, not peeking, and it is the one reason to look early.

## 6. Afterwards

Record it via [`user-context`](../user-context/) `record`:

```
statement   <change> moved <metric> from <figure> to <figure>
confidence  MEDIUM    one source, however big the numbers
n           <users per variant, window>
source      PostHog experiment: <name>, read <date>
caveat      Ran <dates>. Primary <metric>, guardrails held / did not.
            Predicted by <claim id>; outcome <as predicted | smaller | no | wrong way>.
```

**MEDIUM, not HIGH**, even with a hundred thousand users in it. One instrument
is one instrument, and the size of the n does not change that. It becomes HIGH
when something independent agrees, which is usually a handful of people telling
you the same story the numbers are telling you.

## What an experiment can't tell you

Say these in the write-up, every time.

**It tells you what moved, never why.** A conversion lift with no explanation is
a fact you cannot build on. Pair it with a few sessions and you have something
that lasts.

**It only measures what you chose to measure.** Everything the change did to
people that you did not instrument is invisible, including the annoying parts.

**It describes the people in it.** An experiment on active partners says nothing
about the ones who never came back, and they are usually the larger group.

**It is true of the moment it ran.** Seasonality, a pricing change or a
migration in the same window all look like your change in the numbers.

## Where it sits

```
measurable-check      can we see it at all
      ↓
ab-test-planner       plan it, size it, agree what counts
      ↓
   (it runs)
      ↓
adoption-check        read it, record it, say what it means
```

For the behaviour the experiment cannot explain, go to
[`talk-to-users`](../talk-to-users/) or run a small Outset study alongside it.
