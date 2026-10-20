---
name: measurable-check
description: >-
  Answers one question before anyone designs a study: can we measure this at
  all? Checks whether the events, properties and surfaces a question depends on
  actually exist in PostHog, and says plainly when they do not. Use when someone
  says can we measure this, is this instrumented, do we track that, before we
  run a study can you check the data exists, or why does this number say zero.
license: Proprietary
metadata:
  stage: define
  pipeline: impact-ux-designops
  author: impact.com-ux
  answers: can-we-measure-it
---

# Measurable check

One question, asked early: **can we measure this at all?**

It takes five minutes and it is the cheapest step in the pipeline. The
alternative is finding out after fifteen people have been recruited around a
question the data cannot see.

**Answer short.** Lead with what changes, not with everything you found. A few
lines, then one specific follow-up they can ask for — the detail stays
available, it just doesn't arrive unasked. A number earns its place by changing
a decision; the rest belongs in the artifact, where someone can go and find it.

## Why it earns its own skill

`research-builder` checks instrumentation while building a dashboard, and
`research-intake` routes to *instrument first* when a request turns on a missing
event. Both find the problem **mid-flow**, once someone is already invested.

This is the standalone front door: ask it before designing anything, about a
question that does not yet have a study attached.

## The rule this exists for

**An uninstrumented event returns zero, and a zero reads exactly like nobody
doing the thing.**

That sentence is the entire justification. A funnel step with no event behind it
looks like total abandonment. A property that was never set looks like every
account having the same value. Both look confident, both look plausible, and both
are wrong. Neither one tells you it is wrong.

## The rules that keep this honest

1. **Check the schema, never go off the name.** Teams name events differently,
   and a name can look official when it is nothing of the sort.
2. **No data is not the same as zero.** Say which of the two you are looking at,
   every time.
3. **Check the property, not just the event.** An event that fires without the
   breakdown you need is tracked and still no use to you.
4. **Report the gap, do not design around it.** Shrinking a question until the
   data we happen to have can answer it is how a study ends up answering
   something nobody asked.

## Workflow

```
Task Progress:
- [ ] State what would have to be true
- [ ] Check the events exist
- [ ] Check the properties exist
- [ ] Check there is enough history
- [ ] Verdict
```

### 1. State what would have to be true

Turn the question into the events that would answer it. Write them down before
searching, or you will find something adjacent and accept it.

> *"Do partners who use bulk link generation stay longer?"*
> needs: a bulk-generation event · something on it that identifies the partner ·
> sign-in or activity events across a window long enough to see people stay.

Three things, any of which can be missing independently.

### 2. Check the events

```
exec  learn -s "<topic>"                                     once, first, alone
exec  call read-data-schema {"query":{"kind":"events"}}
```

Match on the real name. A near-match is not a match: `link_generated` and
`PPX:publisherpro_affiliate_link_generated` may be different surfaces, different
eras, or one may have replaced the other and stopped firing.

### 3. Check the properties

```
exec  call read-data-schema {"query":{"kind":"event_properties","event_name":"<event>"}}
exec  call read-data-schema {"query":{"kind":"event_property_values","event_name":"<e>","property_name":"<p>"}}
```

The breakdown is usually where this fails. An event fires for everyone but
carries nothing that separates partners from brands, or one tier from another.
It can tell you *how many* and never *which*.

Check the **values**, not just that the property exists. A property present on
3% of events is not a breakdown, it is a trap.

### 4. Check there is enough history

An event instrumented three weeks ago cannot answer a question about last
quarter. Find when it started firing and compare that to the window the question
needs.

Watch for a **rename**: a clean cliff where one event stops and a similar one
starts is one behaviour split across two names, and every trend through that
date is wrong.

### 5. The answer

Four, and only one of them is "yes":

| | Means | Next |
|---|---|---|
| **Measurable** | Events, properties and history all present | Hand to [`research-builder`](../research-builder/) to build the dashboard |
| **Partly** | We can honestly answer a smaller version | Say exactly which part and let them decide. Do not shrink it for them |
| **Not yet** | The event or property does not exist | Instrumentation ticket to the squad that owns the surface, then a small study once there is a fortnight of data |
| **Not countable** | The question is about how people feel: why, whether they trust it, what they expected | Not a tracking gap. Go and ask people |

**That last one matters most.** Not every question is a counting question.
Treating a how-do-they-feel question as a tracking gap sends a squad off to
build instrumentation that will never answer it.

## Output

```markdown
# Can we measure this? [question]
Checked [date] · PostHog project [id]

## What would have to be true
1. [event] · [found / missing / renamed on <date>]
2. [property on that event] · [found / missing / thin: n% of events]
3. [history] · [first seen <date>, question needs <window>]

## The answer
**[Measurable | Partly | Not yet | Not countable]**
[one line]

## If not yet
Event: [name] · Property: [name] · Surface: [where] · Owner: [squad]
Earliest a study could run: [date + a fortnight]

## What this does not tell you
[the how-do-they-feel half of the question, if there is one. No amount of
tracking will reach it]
```

## Record it

A **Not yet** is worth recording. Write it to the Frame via
[`user-context`](../user-context/) `record` with `confidence: GAP`, so the next
person asking the same question finds the answer instead of rediscovering it.

Include the event name and the owning squad. A gap that names its fix is a
ticket; one that does not is a complaint.
