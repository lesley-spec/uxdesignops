---
name: research-synthesis
description: >-
  Triangulates impact.com UX signals across PostHog, Pendo, Dovetail, Outset and
  Freshdesk into confidence-scored themes — including what the sources disagree
  about, and the gaps between what people say and what they do. Use for
  Empathize cross-source synthesis, Research Insight Monitor follow-ups, or when
  2+ sources may agree. Use when someone says triangulate this, do the sources
  agree, is this real or keyword noise, or what does the evidence actually say.
license: Proprietary
metadata:
  stage: empathize
  pipeline: impact-ux-designops
  author: impact.com-ux
---

# Research synthesis — cross-source (Empathize)

Use for **multi-source** triangulation. For one Dovetail project / interview set
only, use `synthesize-research`.

Triangulation is not "collect more agreement". Its value is in two places most
synthesis throws away: **where sources disagree**, and **where what people say
differs from what they do**.

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

1. **Cite every Verified claim** with source, link or file path, and date.
2. **HIGH confidence requires ≥2 independent sources** with usable evidence
   (not empty titles). One source is MEDIUM however large its N.
3. **Reject weak matches:** empty Dovetail `body`/`preview`, NPS comments that
   only share a keyword ("link") but are about payments, Outset studies that are
   only a welcome script.
4. **A contradiction is a finding, not a mess to tidy.** When sources disagree,
   publish both and say what would settle it. Never average them.
5. **Frequency is not importance.** Volume in Freshdesk and blocking severity
   are different axes. Record both.
6. **Independence is not agreement.** Two sources drawing on the same
   self-selected population are one source wearing two hats.
7. Separate Brand vs Partner themes. Designer owns "problem worth solving."

See [references/integrity.md](references/integrity.md),
[references/sources.md](references/sources.md) and
[references/disagreement.md](references/disagreement.md).

## When to use

- Monitor flagged an issue as `triangulated: true` — verify that claim
- Need one themed brief before the human gate
- After `data-analyze` finds a real drop and you need qual corroboration

## Workflow

1. **Scope** — Topic, audience, window.
2. **Collect** — Live MCP and/or `research-agent/docs/research/latest.json`.
3. **Normalize** — One row per signal; drop empty/irrelevant matches.
4. **Cluster** — impact taxonomy themes when they fit.
5. **Cross-check say vs do** — qual sources against behavioural ones. See below.
6. **Resolve disagreement** — where sources conflict, classify it, don't smooth it.
7. **Triangulate** — `high` / `medium` / `low` with honest source counts.
8. **Publish draft** — Gate-ready synthesis (not stakeholder-final).

### Step 5 — the say/do grid

This is what you have more than one source *for*.

| | Behaviour confirms | Behaviour contradicts |
|---|---|---|
| **People say it** | Solid. The strongest claim you can make | **Say/do gap** — the interesting one. Usually a stated preference nobody acts on, or a workaround they forgot they built |
| **People don't say it** | **Silent friction** — shows in PostHog, nobody complains. Often the biggest unserved need | Nothing here yet |

Stated sources: Dovetail, Outset, NPS, Freshdesk.
Behavioural sources: PostHog (including session replay), Pendo.

A say/do gap is never resolved by picking the louder source. It is a question:
*what makes the stated thing hard to act on?*

### Step 6 — when sources disagree

| Pattern | Likely cause | Move |
|---|---|---|
| Qual says blocked, quant shows normal completion | Workaround absorbing the cost | Look for the workaround in replay before dismissing the qual |
| Quant shows drop-off, qual never mentions it | People don't notice or don't blame it | Silent friction — worth a MICRO study |
| Two qual sources conflict | Different segments, not different truths | Split the theme by segment before calling it a conflict |
| Support volume high, everything else quiet | Self-selection; the frustrated write in | Treat as a strong positive signal, weak negative one |

Full protocol: [references/disagreement.md](references/disagreement.md).

## Output template

```markdown
# Cross-source synthesis — [topic]
Window: [dates] · Audience: [Brand|Partner|Shared|All]

## Executive take (AI interpretation)
[3–5 sentences]

## Themes

### [Theme] — confidence: high|medium|low
- **Problem statement (draft):** …
- **Verified evidence:**
  - PostHog: … (N=, date, link)
  - Pendo: "…" (only if on-topic)
  - Dovetail: "…" (non-empty quote + link + timestamp)
  - Outset: … (study name + what it actually tested)
- **Frequency:** how many signals, in which sources
- **Importance:** what it cost them — workarounds, abandonment, support contact
- **Contradicting evidence:** which source disagrees, and what would settle it
- **Say/do gap:** stated vs behavioural, if they diverge
- **Independence check:** are these really separate populations?
- **Discarded matches (not evidence):** … (empty DT / off-topic NPS)
- **What this cannot tell you:** segments absent, window limits, instruments missing
- **Open questions:** …

## Claims for the Frame
| Claim | Confidence | Sources | Sample | Owner | Refresh by |
|---|---|---|---|---|---|

## Ready for human gate?
- High-confidence themes:
- Need fieldwork (`user-research`):
- Suggested next: `user-research` | `data-analyze` | Define handoff
```

## Prompt examples (tested)

1. `Use research-synthesis on UPS Step 2 (details view → send proposal). Is triangulation real or keyword noise?`
2. `Use research-synthesis for Partner Link & Content Tools using the latest research pack + live PostHog if needed.`
3. `Use research-synthesis: Login email→password drop — what evidence survives quality filters?`

## Anti-patterns

- **Smoothing a disagreement into a middle position** nobody's data supports
- **Treating agreement as truth** when both sources drew on the same
  self-selected population
- Counting empty Dovetail notes toward high confidence
- Ranking themes by signal volume alone
- Mixing Brand and Partner pain into one "users say" blob
- Promoting monitor `triangulated: true` without re-checking evidence quality
