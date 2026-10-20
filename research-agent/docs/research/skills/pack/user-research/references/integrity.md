# Integrity rules — Empathize

Shared rules for impact.com UX Empathize skills.

## Verified vs AI

| Label | Meaning |
|---|---|
| **Verified** | Metric, quote, or count taken from a linked source system or file |
| **AI interpretation** | Model narration, clustering, or hypothesis — always secondary |

In FigJam / Confluence / Slack, distinguish AI content (magenta / dashed treatment in the DesignOps board legend).

## Triangulation

Promote an insight to **high confidence** only when **≥2 independent sources** agree (e.g. PostHog drop-off + Dovetail theme + Pendo open text). One source = provisional.

## Disconfirming evidence

Every finding ships with what argues against it: who does not have this problem,
who did the opposite, and what separates them from the rest. A finding with a
blank counter-evidence section has not been checked — say "counter-evidence not
found, searched X and Y" rather than leaving it empty.

## Bounded language

Counts, not percentages, below n≈30. "Six of eight partners" not "75% of
partners". Percentages belong to PostHog and Pendo, not to interviews.

## Human gate

Skills and the Research Insight Monitor **prepare** evidence. The designer confirms “problem worth solving.” Do not auto-transition to Define.

## Marketplace audiences

Classify findings as **Brand**, **Partner** (creator/affiliate/publisher), or **Shared**. Do not collapse both sides into one persona without saying so.

## PII

Do not paste emails, names, or raw session IDs into Confluence/Slack/Jira unless the destination is approved for that data. Prefer aggregate counts and anonymized quotes.
