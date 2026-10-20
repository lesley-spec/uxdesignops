---
name: brand-operator-ux-persona
description: >-
  Applies impact.com Brand-side UX persona and JTBD lenses (operators, ACMs,
  marketing directors) when framing problems or reviewing specs. Use in Define
  write-spec, Ideate critique, or Brand UI questions.
license: Proprietary
metadata:
  stage: define
  pipeline: impact-ux-designops
  author: impact.com-ux
  audience: brand
---

# Brand operator UX persona (Define)

Lens for **Brand** advertisers and operators — not Partners.

## Sources (prefer live)

1. [Brand UI Personas (JTBD)](https://impact.atlassian.net/wiki/spaces/ux/pages/6439338009/Brand+UI+Personas+Jobs-to-be-Done)
2. [UX Design & Research](https://impact.atlassian.net/wiki/spaces/ux/overview) hub
3. Research Insight Monitor / Dovetail Brand themes
4. Fetch Confluence with Atlassian Rovo MCP (`getConfluencePage` / `search`) yourself — do not invent persona names, and do not ask the designer to paste the page

## Known gaps on the Brand side

| Gap | Consequence for this lens |
|---|---|
| **No brand in its first 90 days has been interviewed** | The founder-operator persona is built from reviews and telemetry only. Treat early-life claims as MEDIUM at best |
| **English-only recruitment** | Just under half of activity is outside North America and is unrepresented |
| **Application submission is uninstrumented** | Time-to-decision cannot be measured on either side — do not quote it |

See [`user-personas`](../user-personas/) → Known gaps for the full set.

## How to apply

1. Name the Brand role(s) in scope (e.g. Affiliate Creator Manager, Marketing Director/Analyst, Agency Lead).
2. State primary JTBD and daily cadence frictions (briefing, partners, campaigns, analysis, finance).
3. Ask: does this problem block a Brand job, or only a Partner job?
4. Return 3–5 implications for the one-pager (audience, success criteria, risks).

## Output

```markdown
# Brand lens — [topic]
Personas in scope: …
JTBD affected: …
Evidence this rests on: claim ids + confidence + n
Verified pain (links + dates): …
Implications for framing: …
Who this does NOT cover: …
Gaps / do not assume: …
```

## Anti-patterns

- Speaking for Partners without the creator-affiliate skill
- Speaking confidently about a brand's first 90 days — nobody has been interviewed
- Quoting a persona claim without its denominator
- Using outdated Estalea-only persona docs without noting age
