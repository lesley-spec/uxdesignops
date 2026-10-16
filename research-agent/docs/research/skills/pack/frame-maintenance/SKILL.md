---
name: frame-maintenance
description: >-
  Staleness check and rebuild plan for the Frame. Re-reads every claim against
  Dovetail and PostHog, says what to retire, what to refresh, and what to
  research next, ranked by what a decision currently rests on. Run it quarterly,
  or when someone asks whether the Frame can still be trusted. Use when the user
  says frame maintenance, staleness check, what should we retire, is the Frame
  stale, what should we research next, or rebuild the Frame.
license: Proprietary
metadata:
  stage: empathize
  pipeline: impact-ux-designops
  author: impact.com-ux
  cadence: quarterly
  frame: https://lesley-spec.github.io/uxdesignops/frame/
  frame_claude: https://claude.ai/artifact/FHc7oAPoyohgxo87VdxCGw
---

# Frame maintenance

A Frame nobody maintains **degrades silently while still looking
authoritative** — which is worse than having none, because decisions keep being
made against it. This is the ritual that stops that.

Run it quarterly. It takes an hour or two, most of it reading.

> **The Frame:** https://claude.ai/artifact/FHc7oAPoyohgxo87VdxCGw
> Collections `claims` and `needs`, read and written with `ArtifactData`.

## Integrity

1. **Re-read the source, don't re-read the claim.** A claim that still sounds
   right is not evidence that it is. Open what it links to.
2. **Retirement is a feature.** A Frame that only grows is one nobody trusts.
   "This used to be true" is itself worth recording.
3. **Never retire quietly.** Every retirement says what changed and when.
4. **Rank by exposure, not by age.** A stale claim nobody cites is housekeeping.
   A stale claim a roadmap rests on is urgent.
5. **Pull, don't ask.** Dovetail and PostHog are connected. Read them rather
   than asking the researcher what they remember.

## The four questions

From Constantine Papas, *AI-Powered UX Research* — asked in this order:

1. What did we learn this cycle that **updates** what we believed?
2. What did we find that we still **cannot explain**?
3. What would we **do differently**?
4. What used to be true and **isn't any more**?

Everything below is a way of answering them with evidence.

## Workflow

```
Task Progress:
- [ ] Pull the Frame
- [ ] Age every claim
- [ ] Re-read what PostHog measures
- [ ] Re-read what Dovetail holds
- [ ] Decide: keep / refresh / retire / contest
- [ ] Write the verdicts back
- [ ] Rank what to research next
- [ ] Publish the maintenance note
```

### 1 — Pull the Frame

```
ArtifactData list  claims   (limit 100)
ArtifactData list  needs    (limit 100)
```

Use `out_dir` and read the files rather than paging through output.

### 2 — Age every claim

Mechanical, no sources needed. Sort by `verified` and bucket:

| Age | Default verdict |
|---|---|
| Under 3 months | Keep |
| 3–6 months | Keep; flag if it describes a surface that shipped since |
| 6–12 months | **Refresh** — drop one confidence level unless re-verified |
| Over 12 months | **Retire or re-verify.** No middle option |

Then override by **exposure**: any claim cited by a `needs` row, a one-pager or
an epic jumps the queue regardless of age. Check `needs[].claims` for which
claims are load-bearing.

### 3 — Re-read what PostHog measures

Every claim with a `posthog` link is re-runnable. Re-run it.

```
exec  learn -s "<topic>"              (once per session, first)
exec  call insight-query {"insightId": "<short_id>"}
exec  call dashboard-insights-run {"id": <id>}
exec  call cohorts-retrieve {"id": <id>}
```

Compare to the claim's stated number. Three outcomes:

| Then | Do |
|---|---|
| Within noise | Update `verified` to today. Cheapest maintenance there is |
| Materially moved | Rewrite the claim with the new figure; record the old one in `caveat` |
| Query broken or event gone | **Instrumentation gap.** The claim is unmeasurable now — say so rather than keeping a number nobody can reproduce |

**A number that cannot be re-run is not a claim, it is a memory.**

### 4 — Re-read what Dovetail holds

Qual decays differently: findings do not move, their *relevance* does.

```
search_workspace          → what is new in this domain since last review
list_docs {project_id}    → new synthesis in the projects behind the claims
get_doc_content           → read the ones that touch a live claim
```

Ask of each domain:

- Has anything **new** been published that agrees, disagrees, or supersedes?
- Has the **surface changed** since the research? A claim about a screen dies
  the day that screen ships
- Did a new study **corroborate** a single-source claim? That is a promotion —
  see [references/verdicts.md](references/verdicts.md)

### 5 — Decide

Four verdicts, full criteria in
[references/verdicts.md](references/verdicts.md):

| | Means |
|---|---|
| **Keep** | Re-verified. Update `verified`, nothing else changes |
| **Refresh** | Still directionally true, evidence is ageing. Drop a confidence level and name what would restore it |
| **Retire** | No longer true, or describes something that no longer exists |
| **Contest** | New evidence disagrees. Keep both, mark the domain contested, and it stops auto-closing requests |

### 6 — Write the verdicts back

Use one `ArtifactData` `batch`. Pin every write with the `version` you read.

Retirement is a field, not a delete:

```json
{ "retired": "2026-10-13",
  "retired_why": "The assets page was rebuilt in August; this described the old IA.",
  "confidence": "GAP" }
```

**Keep the row.** A retired claim is the record that something used to be true,
and it stops the same finding being rediscovered and re-believed next year.

### 6b — Check the prompts still hold

The Frame's starter prompts describe what the claims say. When a claim is
rewritten, recalibrated or retired, **a prompt built on it goes quietly stale** —
and it arrives with the page's authority behind it, which makes it worse than no
prompt at all.

```
ArtifactData list prompts
```

For each: does it still describe something the claims support? Rewrite what has
drifted, and keep it **human-first** — the question a designer would ask, with
the figure as backing rather than as the opening.

### 7 — Rank what to research next

The output that makes this worth doing. Rank by **exposure × weakness**, not by
curiosity:

| Rank | Pattern |
|---|---|
| 1 | A `blocking` need whose only evidence is LOW or retired |
| 2 | A domain the coverage matrix shows blind where a decision is live |
| 3 | A contested claim that keeps blocking requests |
| 4 | A single-source claim a roadmap rests on — one corroborating source makes it HIGH |
| 5 | Everything else |

Rank 4 is usually the cheapest win: promotion needs one new source, not a study.

### 8 — Publish the note

Short, and it goes to the team, not in a drawer. Template:
[references/note.md](references/note.md).

## What to watch

Three numbers, quarter on quarter:

| | Healthy |
|---|---|
| Claims re-verified vs retired | Both non-zero. All-keep means nobody looked |
| Share of claims over 6 months | Falling, or at least flat |
| Requests closed as already-answered | Rising |

**All-keep is the failure mode**, not all-retire. A review that retires nothing
is a review that did not happen.

## References

- [references/verdicts.md](references/verdicts.md) — the four verdicts, promotion and retirement criteria
- [references/note.md](references/note.md) — the maintenance note template
