# Publish — Confluence + Jira (Define)

**Only after the designer confirms the chat draft.**

Use the **Atlassian Rovo MCP** for every Jira/Confluence call. Fetch named tickets with `getJiraIssue` yourself — do not wait for “the connector is on.” See [atlassian-rovo.md](atlassian-rovo.md).

## Atlassian site

- Cloud: `https://impact.atlassian.net`
- `cloudId`: `8bd0a64b-b516-411d-b33c-b692737a5317`

## Confluence

| Field | Value |
|---|---|
| Space | `ux` (Impact UX) — spaceId `393347460` |
| Status | Prefer `draft` until Designer sign-off + PM chat |
| Parent | UX Roadmap page `6436978692` unless user names another parent |
| Label | `product-one-pager` when using full Product Shaping shape |
| Tool | `createConfluencePage` (markdown or html) |

Page title: initiative name (no “DRAFT” in title; status field/body carries draft).

Include a **Research context** section with links to `latest.json` / report HTML / Dovetail / PostHog.

## Jira (UX Squad)

| Field | Value |
|---|---|
| Project | `UX` |
| Issue type | **Epic** for initiative framing (collection of research + design speccing) |
| Description | Short problem summary + **One-pager:** \<Confluence URL\> + bullet research links |
| Labels | `ux_roadmap` when it belongs on the UX Roadmap |
| Tool | `createJiraIssue` |

Other UX types (use only when asked): Research, Analytics, Mocks, Other, Subtask.

### Description skeleton

```markdown
[1–3 sentence problem]

**One-pager:** <confluence url>

**Research context (Verified):**
- PostHog: …
- Pendo / Dovetail / Outset: …
- Empathize pack: …

**Audience:** Brand | Partner | Shared
**Status:** Framing draft — Designer sign-off, then PM chat before Ideate
```

## Link both ways

1. Create Confluence page → get URL  
2. Create UX Epic with one-pager URL in description  
3. Edit Confluence Epic field / body to include `https://impact.atlassian.net/browse/UX-…`  
4. Offer to add a row on [UX Roadmap](https://impact.atlassian.net/wiki/spaces/ux/pages/6436978692/UX+Roadmap) (do not edit roadmap unless asked)

## Dedup

Before create: Atlassian `search` / JQL for same title in `UX` and space `ux`. Reuse or update instead of duplicating.
