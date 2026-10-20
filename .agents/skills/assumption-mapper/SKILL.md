---
name: assumption-mapper
description: >-
  Pulls the untested assumptions out of a brief, PRD or pitch, checks each one
  against what we already know, and ranks what is left by how much rests on it
  versus how sure we are. Hands the scariest one to research-intake. Use when
  someone says review this brief, what are we assuming here, what could sink
  this, or before we build this what should we check.
license: Proprietary
metadata:
  stage: empathize
  position: pre-entry
  pipeline: impact-ux-designops
  author: impact.com-ux
  hands-off-to: research-intake
---

# Assumption mapper

Every brief rests on things nobody has checked. Most are fine. One or two will
sink it.

This finds them, sorts the ones we already know the answer to from the ones we
do not, and ranks what is left by how much damage a wrong answer does.

**Answer short.** Lead with what changes, not with everything you found. A few
lines, then one specific follow-up they can ask for — the detail stays
available, it just doesn't arrive unasked. A number earns its place by changing
a decision; the rest belongs in the artifact, where someone can go and find it.

## Why it sits in front of intake

[`research-intake`](../research-intake/) starts when someone asks for research.
This starts earlier, with a brief nobody has questioned yet, and works out
whether there is a question worth asking at all.

```
a brief, a PRD, a pitch
        ↓
assumption-mapper        what are we taking on faith?
        ↓
   check the Frame       do we already know any of this?
        ↓
research-intake          route the ones we don't
```

Most of what comes out of this is not a research request. That is the point. A
map where everything needs a study is a map nobody will use.

## The rules that keep this honest

1. **Check the Frame before you rank anything.** Half of what looks like an
   assumption is a claim somebody already wrote down. Finding that is the
   cheapest win here.
2. **Nobody arguing with it is not the same as it being true.** An assumption
   nobody has challenged usually got high confidence by going unnoticed.
3. **Every assumption gets a way to check it**, or gets called what it is: a
   risk we are carrying on purpose. Do not invent a plausible test for
   something untestable.
4. **Don't write "do some research" five times.** Some of these are a data
   query, some are a conversation with one engineer, some are reading a
   competitor's pricing page.
5. **Name the scariest one.** Not the easiest to check. A map with no clear
   top item has not done its job.

## 1. Surface them, across four kinds

People only ever write down the first kind, so go looking for the other three.

| | Ask |
|---|---|
| **Do they want it?** | Does anybody actually have this problem, badly enough to change what they do? |
| **Can we build it?** | Does the data exist, does the integration hold, can it work at the sizes we have? |
| **Does it work for us?** | Does it make money or save it, does it fit how we sell, can we support it? |
| **Can they use it?** | Can the person who has this problem actually get through it unaided? |

**The dangerous ones are the ones too obvious to write down.** "Partners want to
be found by brands" sounds like a fact. It is an assumption, and the marketplace
numbers argue with it.

Keep going until you have at least one of each kind, then read the brief again
for whichever kind is emptiest. It is empty because nobody thought about it,
not because there is nothing there.

## 2. Check each one against what we know

This step is ours and it is the one generic versions skip.

For each assumption, ask [`user-context`](../user-context/) `ask`, or query the
Frame directly. Four things can come back:

| | Means | Do |
|---|---|---|
| **We know this** | A claim covers it, right segment, still current | Mark it settled, link the claim. It is not an assumption any more |
| **We half know it** | Right area, wrong segment, or getting old | Note what is covered and what is not. The question just got smaller |
| **We know we don't** | It is already a recorded gap | Say so, and say what was going to be done about it |
| **Nothing** | Nobody has looked | Carry it to the ranking |

A brief where six of ten assumptions come back settled is a good outcome for
everyone, and it takes twenty minutes.

## 3. Rank what is left

Two numbers each, both 1 to 5.

**How much rests on it.** If this turns out false, does the plan need a tweak,
or does it collapse?

**How sure are we.** Be strict. 5 means we have evidence, with a source. 3 means
it sounds right and nobody has checked. Tag where each one came from:
**[evidence]** with a link, or **[hunch]**, honestly.

**What it adds up to = rests on it − how sure.**

Anything scoring 3 or more, or sitting at rests-on-it 4+ with confidence 2 or
less, is a **load-bearing guess**. Say so in those words. It is the sentence
people remember.

| Assumption | Kind | Rests on it | Sure | Score | Where it came from | How to check |
|---|---|---|---|---|---|---|

Leave the negative scores visible. An assumption we are very sure about that
nothing much rests on is worth seeing, because it shows the map was not written
to make a case.

## 4. The cheapest way to check the top one

For the scariest assumption, name the cheapest thing that could prove it wrong
this week. Not the most thorough thing. The cheapest.

| | Good for | Rough cost |
|---|---|---|
| **Query what we already have** | Anything about what people currently do | An hour |
| **Read the Frame properly** | Anything we might have studied before | Twenty minutes |
| **Ask one person who would know** | Can we build it, does it work for us | A conversation |
| **A MICRO study** | Do they want it, can they use it | 48 hours |
| **Look at what a competitor did** | Whether the approach is even viable | An afternoon |
| **A fake door or a mock** | Would anyone click this at all | A few days |
| **Check the schema** | Can we measure the thing we would need to measure | Minutes, via [`measurable-check`](../measurable-check/) |

Then say what a fail looks like, concretely, before anyone runs it. "If fewer
than two of eight have ever tried to do this, the assumption is dead."

## 5. Hand it on

Say explicitly which assumption the next step has to treat as open.

- A load-bearing guess that needs people → [`research-intake`](../research-intake/),
  with the assumption as the question and "the plan collapses without it" as the
  decision
- One that needs numbers → [`measurable-check`](../measurable-check/) first,
  since it might not be measurable at all
- One we cannot check → write it into the brief as a risk somebody owns, with
  a name on it

An unresolved load-bearing guess goes into the brief as an open question. It
does not quietly become a decision.

## The output

```markdown
# What this brief is assuming: [name]
[date] · [what you were given] · stage: [idea / discovery / pre-build / shipped]

## The short version
[Two or three lines. The one assumption that could sink this, and whether
anything we already know speaks to it.]

## Already answered
[Assumption] → [claim id, confidence, n, link]. Not an assumption any more.

## Already a known gap
[Assumption] → recorded as [need/gap], [what was planned]

## Still untested
| Assumption | Kind | Rests on it | Sure | Score | From | How to check |

## The load-bearing guesses
**[the assumption, in plain words]**
Rests on it [n], sure [n]. [Where it came from.]
Cheapest check: [what, and roughly how long]
A fail looks like: [concretely]

## Risks we are carrying on purpose
[Things that cannot be checked. Named, with an owner.]

## What this map can't tell you
[What you had to assume about the brief itself, anything you could not reach,
and whether the Frame check was quick or thorough]
```

## Two ways this goes wrong

**Everything becomes a research request.** Then nobody runs it twice. Most
assumptions are fine, some are answered already, and only one or two are worth
anyone's week.

**It only finds the comfortable ones.** If the top of the map is something the
team was already planning to check, go back and read the brief again. The
assumption that scares people tends not to make it onto the page.
