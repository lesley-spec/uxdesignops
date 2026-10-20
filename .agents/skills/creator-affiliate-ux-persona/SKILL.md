---
name: creator-affiliate-ux-persona
description: >-
  Applies impact.com Partner / creator-affiliate UX persona lenses when framing
  problems or reviewing specs. Use in Define write-spec, Ideate critique, or
  Partner-side experience questions.
license: Proprietary
metadata:
  stage: define
  pipeline: impact-ux-designops
  author: impact.com-ux
  audience: partner
---

# Creator-affiliate UX persona (Define)

Lens for **Partner** side: creators, affiliates, publishers — not Brand operators.

## Read this before applying the lens

**There is no affiliate persona.** The Partner Exp screener excluded deal,
coupon, review, email and network partners, and no partner-type field exists in
product data. Every partner quote in the evidence base is a **creator's**.

This skill is named for a segment it cannot currently speak for. So:

| Question is about | You may |
|---|---|
| Creators (content, social, maturity tiers) | Apply the lens normally — this is where the evidence is |
| Deal, coupon, review, email, network partners | **Say we do not know.** Log it as a gap and route to `research-intake` |
| "Partners" in general | Answer for creators and say that is who you answered for |

Inventing affiliate characteristics to fill the gap is the single most likely
way to misuse this skill, and these partner types carry the highest median
commissions — so a confident guess here is expensive. The gap is the
highest-value study available; naming it is more useful than covering it.

See [`user-personas`](../user-personas/) → Known gaps.

## Sources (prefer live)

1. [Partner Personas](https://impact.atlassian.net/wiki/spaces/ux/pages/1400766526/Partner+Personas) (Novice / Intermediate / Expert)
2. Creator Affiliate product narrative / primers in Confluence (search Atlassian)
3. Research Insight Monitor Partner themes (Link & Content Tools, proposals, finance)
4. Fetch live pages via Atlassian Rovo MCP (`getConfluencePage` / `search`) yourself — do not invent quotes or maturity levels, and do not ask the designer to paste the page

## How to apply

1. Name Partner segment (creator vs classic affiliate/publisher) and maturity if
   known — **and state which of the two you have evidence for.** If the answer
   is "classic affiliate", stop and log the gap rather than extrapolating from
   creator research.
2. Map JTBD: discover brands, generate links, proposals/campaigns, payouts, content tools.
3. Ask: does this problem block Partner earning/activation, or only Brand ops?
4. Return 3–5 implications for the one-pager.

## Output

```markdown
# Partner / creator-affiliate lens — [topic]
Segment: …
JTBD affected: …
Evidence this rests on: claim ids + confidence + n
Verified pain (links + dates): …
Implications for framing: …
Who this does NOT cover: … (name the partner types with no evidence)
Gaps / do not assume: …
```

## Anti-patterns

- **Speaking for affiliates, publishers or network partners as though evidence exists** — it does not
- **Extrapolating from creator findings to other partner types** because the two sound adjacent
- Collapsing all Partners into “creators”
- Speaking for Brand operators without `brand-operator-ux-persona`
