# The four verdicts

Every claim gets exactly one per review. Write the reasoning, not just the verb.

---

## Keep

Re-verified against its source. Update `verified` to today and change nothing
else.

**Bar:** you opened the link and the evidence still says what the claim says.
Reading the claim and nodding is not keeping it — that is how a Frame rots while
every row looks reviewed.

---

## Refresh

Still directionally true; the evidence behind it is ageing or thinning.

**Do:** drop one confidence level, and write into `caveat` *what would restore
it* — a re-run, a second source, a narrower re-ask.

**Typical:** a claim at 8 months whose source is one study; a number nobody has
re-run since the surface changed; a qual finding whose sample no longer matches
who uses the feature.

Refresh is the honest middle. Reach for it when the claim is probably right and
you cannot currently prove it.

---

## Retire

No longer true, or it describes something that no longer exists.

**Do not delete.** Set:

```json
{ "retired": "YYYY-MM-DD",
  "retired_why": "<what changed, and when>",
  "confidence": "GAP" }
```

**Retire when:** the surface shipped or was rebuilt · the metric moved past the
claim's meaning · a better-evidenced claim supersedes it · the population it
describes no longer exists.

**Keep the row** so the finding is not rediscovered and re-believed in a year.
"This used to be true" is knowledge.

---

## Contest

New evidence disagrees with it.

**Do:** keep both claims, set `contested: true` on each, and record in `caveat`
what differs — scope, date, method, or genuine disagreement.

**Never resolve a contest by deleting the inconvenient side.** A contested
domain stops auto-closing intake requests, which is the behaviour you want: it
routes to a human until someone settles it.

---

## Promotion — the verdict people forget

A claim can get **stronger**. Look for it deliberately; nobody finds it by
accident.

**Promote to HIGH when** a second, genuinely independent source now agrees —
qual plus behavioural, two unrelated studies, a survey plus a funnel.

**Not independent:** two reports drawing on the same study · a larger n from the
same instrument · the same corpus counted twice.

Record it the same way as a demotion, in `demoted`, so the record shows movement
in both directions:

```
"Promoted from MEDIUM. Now two independent sources: <a> and <b>."
```

A Frame that only ever downgrades teaches people that evidence decays and never
accumulates. It does both.

---

## Confidence, for reference

| | Bar |
|---|---|
| **HIGH** | Two or more genuinely independent sources agree · n stated · under 6 months |
| **MEDIUM** | One primary source · n stated |
| **LOW** | Anecdotal, conflicting, tiny n, or over 12 months |
| **UNVALIDATED** | Asserted, not evidenced |
| **GAP** | Nothing found, or retired |

**Single source is MEDIUM, however large the n.** A million rows from one
instrument is one instrument.
