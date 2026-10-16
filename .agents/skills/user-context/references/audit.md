# The `ask` protocol

Six steps. Proportionate to the question — a 48-hour decision gets a short
version, not a skipped one.

---

## Step 1 — Make it falsifiable

Restate the question as a claim: **subject + behaviour + direction.** Subject can
be a persona, a cohort, a surface or a workflow — it does not have to be a
person.

Then, **before searching**, write:

- **Would confirm:** …
- **Would kill:** …

**No killer means it is not a hypothesis yet.** Fix it with the asker rather than
sweeping around a question that cannot come back negative. A question that
nothing could disprove will "find" support no matter what the data says.

## Step 2 — Scope it

Which slice of the Frame: segment, surface, workflow, cohort, time window? Name
what is explicitly **out** of scope.

Persona is optional. If a persona slice genuinely applies, take it from
[`user-personas`](../../user-personas/) — don't invent one, and don't force one
onto a question that isn't about people.

## Step 3 — Check the claims pool

Free and first. A HIGH-confidence claim, in date, matching scope, ends the audit.
A near-match narrows it. See [frame.md](frame.md).

## Step 4 — Sweep

In the order in [sources.md](sources.md), stopping when the question is answered
rather than when the list is exhausted. Record which sources ran.

## Step 5 — Hunt counter-evidence

Deliberately search for the case that would kill the claim — the segment that
behaves differently, the ticket volume that didn't materialise, the study that
disagreed.

**"Searched [scopes], none found" is a reportable result.** But you must have
looked, and you must say where.

## Step 6 — Grade and gap

Every claim gets a confidence level ([evidence.md](evidence.md)). Every gap gets
a type and the cheapest way to close it.

| Gap | Means | Cheapest close |
|---|---|---|
| `segment` | No data for *this* slice | Recruit it |
| `behavioural` | Qual claim, no quant backing | A funnel or trend |
| `attitudinal` | Quant pattern, no "why" | A handful of interviews |
| `staleness` | Evidence predates a change | Re-ask the narrow question |
| `instrumentation` | The event isn't tracked | **Instrument first.** No study fixes missing data |
| `contested` | Sources disagree | A human decides; don't auto-close |
| `domain` | The Frame has nothing here | **Foundational research** — this builds the Frame |

`instrumentation` and `domain` are the two that don't route to a normal study.
The first needs tracking before anything can be measured; the second needs
foundational work, not a quick answer.

---

## Short version

When the decision lands inside 48 hours: claims pool, Dovetail, one Outset
search. No replay, no support aggregation, no counter-evidence hunt.

**Cap confidence at LOW**, label it `short sweep — not decision-grade`, and say
in one line what a full sweep would add.

Preflight is **not** skippable in the short version.

---

## Save the brief

Write it to a file so later sessions can cite it and the next person can find it:
`docs/user-context/<yyyy-mm-dd>-<topic-slug>.md`, or the project's own research
directory.

Then **extract the claims into the pool** — the brief is narrative and will not
be read again; the claims are what compound.
