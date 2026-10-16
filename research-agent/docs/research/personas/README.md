# User personas at impact.com

Reference persona set for the UX DesignOps pipeline: three partner personas and three
brand personas, each with goals, a job-to-be-done, a workflow map and a stated
confidence score.

**Live on DesignOps:** https://lesley-spec.github.io/uxdesignops/personas/

Claude artifact (Ask + live PostHog connectors): https://claude.ai/artifact/FaBjbFu7hiM5LYBfALemAQ — ask for access.
UX Research team for access)

## Contents

| File | What it is |
|---|---|
| `SKILL.md` | The agent skill. Routes work to the persona set and says how to use it. |
| `personas.md` | Full markdown copy — every persona, workflow table and source note. |
| `index.html` | Source of the live artifact. Publish to update the page. |

## What makes this set different

**Every claim carries its denominator.** Several figures that had circulated as
segment-wide rates turned out to be six or four people. Those are marked, not quietly
dropped.

**Confidence is scored and visible**, 41–81 out of 100, so a reader knows which cards
carry weight. Brand personas scored lower until the Dovetail Brand Value Stream research
was folded in.

**Gaps are stated as prominently as findings.** There is no affiliate persona because the
research screener excluded them; that absence is on the page rather than hidden behind a
plausible-sounding card.

**The charts are live.** Partner funnel, device split, approval decisions, region spread
and the new-brand cohort all pull from PostHog on load, with a snapshot fallback and a
status badge when a connector is unavailable.

**You can question a persona.** Each card has an Ask panel grounded in the evidence
behind it. It declines when a question falls outside what the research covers — a
refusal is a research gap, not a failure.

## Corrections this work produced

- The "~90% application rejection" figure was one participant's own experience. The real
  number is **42.5% of 1.86M applications**.
- "55% can't discover campaigns" and "40% struggle with links" are **6 and 4 people**.
- Marketplace-originated partnerships convert at **3.6–4.9%** against **17.6–23.1%** for a
  branded signup — so discovery and vetting are one problem, not two.

## Design system

Styled with the iui3 **vnext** theme — tokens read from the public component-library
Storybook, declared under their real `--iui3-*` names so
`@impactinc/frontend-theme-tokens` can be dropped in. Chart palettes validated for
colour-vision deficiency and contrast in both themes.

Known DS gap: vNext publishes no semantic success or warning **text** colour, only
`reporting-success`, which is unreadable as text on white. The friction chips use a
derived pair in light mode and the real tokens in dark.

## Maintaining it

1. Edit `index.html`.
2. Publish it to the artifact URL above (keeps the link stable).
3. Keep `personas.md` in step.
4. Re-score confidence when a gap closes and note what moved.

## Feedback

For any feedback on how we can improve this, Slack the UX Research team.
