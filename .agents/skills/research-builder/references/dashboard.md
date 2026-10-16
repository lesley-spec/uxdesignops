# The dashboard, built first

The study measures what people say. The dashboard measures what they do. Build
the second one before you run the first.

---

## Why first

Three things only a dashboard built in advance can give you:

**A baseline.** After a change ships, "it went up" needs a before. Nobody can
reconstruct one afterwards from memory.

**An instrumentation check.** If the decisive event does not exist, you learn it
now and for free rather than after recruiting fifteen people around a question
the data cannot answer.

**A sampling frame.** The cohort you will recruit from comes out of the same
query — see [audience.md](audience.md).

---

## Protocol

```
exec  learn -s "<topic>"                          once, first, alone
exec  call read-data-schema {"query":{"kind":"events"}}
exec  call read-data-schema {"query":{"kind":"event_properties","event_name":"<event>"}}
exec  call query-funnel / query-trends { … }
```

**Confirm the event exists before querying it.** Event names vary per team and
look canonical when they are not. An uninstrumented event returns zero, and a
zero reads exactly like nobody doing the thing.

State the window and whether test accounts are filtered on every number you
report.

## What to build

| Tile | Answers |
|---|---|
| **The funnel** | Where do people fall out, and how many |
| **The trend** | Is this moving, over a window wide enough to see seasonality |
| **One breakdown** | By persona, tier or region — whichever the study segments on |
| **The baseline** | The pre-change figure, boxed and dated |

Four tiles. A dashboard nobody reads is the same as no dashboard, and the fifth
tile is usually where that starts.

## Building first is not leading with it

The dashboard goes up before the study so a missing event is cheap to find. That
is a sequence, not a hierarchy. **The claim that comes out still leads with what
people told us**, with the number behind it —
[`evidence.md`](../../user-context/references/evidence.md#qual-leads-behaviour-backs-it).

## Record the baseline as a claim

The step people skip. Write it into the Frame before the change ships:

```
statement   <measure> is <figure> as of <date>
confidence  MEDIUM        single source, however large the n
n           <people, window>
source      PostHog: <insight name>, read live <date>
link        <insight url>
caveat      Baseline taken before <change>. The after-reading is <adoption-check>.
```

Without it, the adoption check has nothing to compare to and you are back to
arguing from memory about whether things were better before.

## When the event does not exist

**Stop.** Do not design around it.

Raise an instrumentation ticket on the squad that owns the surface, name the
event and the property you need, and say plainly that the question cannot be
answered until it lands. Then a small study once there is a fortnight of data.

This is the `instrument first` route in
[`research-intake`](../../research-intake/SKILL.md). It is a real outcome, not a
failure to plan — and it is cheaper than every alternative.
