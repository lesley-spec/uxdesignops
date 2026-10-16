# Sources

Six, in sweep order. Each answers a different question — the order matters
because cheap and broad comes before expensive and narrow.

| | Source | Answers | If missing |
|---|---|---|---|
| 0 | **Claims pool** | Do we already know this? | Nothing to degrade — it's a file read |
| 1 | **Dovetail** | What have people told us? | **Hard stop.** No sweep without it |
| 2 | **PostHog** | What do people actually do? | Cap at MEDIUM; no behavioural claims |
| 3 | **Outset** | What studies have run, or are running? | Say so — this is where duplicates hide |
| 4 | **Session replay** | What does it look like when they do it? | Note it as unchecked |
| 5 | **Pendo** | Guides, polls, in-product surveys | Note it as unchecked |
| 6 | **Support tickets** | What is actually breaking, at volume? | Note it as unchecked |

**Dovetail first, and it carries the claim.** PostHog, Pendo and support say how
much and how often; Dovetail says what it means. Sweep in the order above, but
write the finding from the qual and let the behaviour corroborate it — see
[evidence.md](evidence.md#qual-leads-behaviour-backs-it).

**A partial sweep is provisional.** Say which sources ran. A sweep on one source
produces a confident answer, and the source you skipped is disproportionately the
one that disagrees — because a second source only changes a verdict when it says
something different.

---

## Preflight

Read-only, one call each, run in parallel. **Probe before sweeping.** Silently
degrading to model memory is the failure that produces confident fiction, and its
output is indistinguishable from a real sweep.

Dovetail unhealthy → **stop** and give the authorisation instruction. Anything
else unhealthy → continue, cap confidence, and name the missing source in the
output header.

---

## 0 — Claims pool

Always first. Free, instant, already graded, and it records what was
unanswerable last time — the single most useful thing to know before planning
anything. See [frame.md](frame.md).

A HIGH-confidence claim, in date, matching scope, **is the answer**. Stop there.

## 1 — Dovetail (qual)

```
search_workspace          → find IDs
get_folder_contents       → scope to the right folder
list_project_data / list_project_insights / get_project_highlights
get_doc_content / get_data_content
```

Scope to the relevant folder rather than the whole workspace. **Drop empty bodies
and keyword-only hits** — a document that merely contains the word is not
evidence. Record what you dropped so the next person doesn't re-find it.

## 2 — PostHog (behavioural)

**Confirm the event exists in the schema before querying it.** An uninstrumented
event returns zero, which looks exactly like "nobody does this." That is not a
finding of zero; it is an absence of data, and the difference has started whole
projects.

State the window and whether test accounts are filtered on every number.

## 3 — Outset (studies)

The half that catches duplicates. Look for three things:

1. **A study that already answers this** → the request closes
2. **One that nearly does** — right question, wrong segment, or stale → the scope
   narrows rather than closing
3. **One in flight** → route to *wait*, not to a second study

Note: getting from a search hit to its findings takes several calls, and study
names do not match report names. Budget for it.

## 4 — Session replay

**The gap between what people say and what they do.**

Not "users said they struggle with onboarding" but *here is a recording of them
struggling*. Replay catches workarounds nobody reports, hesitation nobody
remembers, and the step people skip entirely while telling you it's essential.

Use it to check a qual claim against behaviour before grading it HIGH — and when
a claim and a funnel disagree, replay usually shows why.

## 5 — Pendo

In-product guides, polls and surveys. Often the **largest n available** by a wide
margin, which makes it the fastest way to check whether a small qual finding
generalises — and the fastest way to discover it doesn't.

## 6 — Support tickets

**What is actually breaking, in volume.** Aggregate by feature or workflow rather
than reading individually; the signal is the cluster, not the ticket.

> "These 50+ tickets cluster around feature Y" is a research question that found
> itself.

Support skews to what people will bother reporting, so it under-represents quiet
abandonment — strong positive signal, weak negative signal. Absence of tickets is
not evidence that something works.

---

## Triangulation

Aim for all three on anything load-bearing:

1. **Qual** — interviews, observation, the user's own words
2. **Quant** — behaviour at scale, statistical weight
3. **A concrete example** — a quote or clip that makes it memorable

HIGH confidence requires independent sources agreeing. Two reports drawing on the
same study are one source wearing two hats.
