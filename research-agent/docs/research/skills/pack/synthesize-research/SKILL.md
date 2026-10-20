---
name: synthesize-research
description: >-
  Affinity-maps a single research corpus (one Dovetail project, interview set,
  or study export) into themes and insight cards — separating how often
  something came up from how much it matters, and carrying the evidence that
  argues against each theme as well as for it. Use for Empathize single-source
  synthesis — not cross-tool triangulation (use research-synthesis for that).
  Use when someone says affinity map these notes, theme this study, what came
  out of these interviews, or turn this corpus into insight cards.
license: Proprietary
metadata:
  stage: empathize
  pipeline: impact-ux-designops
  author: impact.com-ux
---

# Synthesize research — single corpus (Empathize)

Affinity / thematic synthesis for **one** dataset. For PostHog + Pendo +
Dovetail together, use `research-synthesis`.

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

1. **Read the raw data, not the summary.** A summary is already an
   interpretation, and it is the interpretation that drops the thing you needed.
   If you only have a summary, say so and cap confidence at **low**.
2. **Frequency is not importance.** Eight people mentioning something and one
   person blocked by it are different findings. Record both, separately.
3. **Every theme carries its disconfirming evidence.** Who did not hit this?
   Who did the opposite? A theme with no counter-evidence listed has not been
   looked for, and the reader should treat it as weaker, not stronger.
4. **Bound language to N.** At n=8 you cannot say "most users" of anything
   beyond the eight. Say "six of eight participants", not a percentage.
5. **Ceiling confidence is MEDIUM.** One corpus is one source, however large.
   HIGH needs a second independent source — that is `research-synthesis`.
6. **Label what is interpretation.** Observations are what people said and did.
   Implications are yours. Mark them.

Full protocol: [references/rigor.md](references/rigor.md). Also
[references/integrity.md](references/integrity.md) and
[references/themes.md](references/themes.md).

## When to use

- One Dovetail project / highlight set
- One Outset study transcript or notes dump
- Designer pastes interview notes and wants affinity themes

## Workflow

| # | Step | The move that matters |
|---|---|---|
| 1 | **Ingest** | Load one corpus, record N and how people were recruited |
| 2 | **Read raw** | Transcripts, not summaries. Mark tone shifts, workarounds, say/do contradictions |
| 3 | **Open code** | Atomic observations — blocker, workaround, desire, confusion |
| 4 | **Affinity** | 4–8 themes; prefer the impact taxonomy labels when they fit |
| 5 | **Weigh** | Frequency *and* importance, scored separately — see below |
| 6 | **Disconfirm** | For each theme, sweep the corpus for what argues against it |
| 7 | **Insight cards** | One per theme, with the evidence trail |
| 8 | **Handoff** | Quant needed → `data-analyze`; multi-source → `research-synthesis` |

### Step 5 — frequency and importance are two columns

| Theme | Frequency | Importance | Reading |
|---|---|---|---|
| Bulk import | 8/8 mentioned | 1/8 blocked today | Widely wanted, not urgent |
| Commission findability | 3/8 mentioned | 3/3 of those built a workaround | Narrow but blocking |

Importance is evidenced by **what people did**: a workaround built, a task
abandoned, support contacted, money or time lost. "They said it was important"
is frequency wearing importance's clothes.

## Insight card template

```markdown
### Insight: [short name]
- **Audience:** Brand | Partner | Shared
- **Observation:** what people said and did — no interpretation
- **Evidence (Verified):**
  - "…" — participant id, timestamp, link
  - "…" — participant id, timestamp, link
- **Frequency in corpus:** n / N (mentioned)
- **Importance:** n / N (blocked, worked around, or abandoned) + what they did
- **Disconfirming evidence:** who did not hit this, who did the opposite, and
  what separates them from the rest
- **Implication for product:** … (AI interpretation)
- **Confidence:** low | medium — and why
- **What this cannot tell you:** sample limits, segments absent, questions the
  corpus never asked
- **Action for designer:** …
```

## Prompt examples (tested)

1. `Use synthesize-research on this Dovetail highlight about commission details findability (paste quote + URL). Affinity for Partner proposals.`
2. `Use synthesize-research on the Brand Marketplace Discovery Outset study summary — themes only, no PostHog.`
3. `Use synthesize-research on these Partner contextual-inquiry notes I pasted — blockers vs desires.`

## Anti-patterns

- **Ranking themes by frequency alone** — the loudest theme is rarely the most
  costly one
- **Presenting a theme with no disconfirming evidence** — it means nobody looked
- Inflating one quote into a roadmap item
- Percentages at small n ("70% of users…" from eight interviews)
- Reading the AI summary instead of the transcripts, then calling it synthesis
- Cross-walking to PostHog inside this skill
- Treating study welcome scripts as findings
