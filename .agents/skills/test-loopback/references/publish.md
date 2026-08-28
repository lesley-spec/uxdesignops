# Publish — Confluence + Jira (Test loopback)

**Only after designer confirms the loopback pack.**

## Atlassian site

- Cloud: `https://impact.atlassian.net`
- `cloudId`: `8bd0a64b-b516-411d-b33c-b692737a5317`

## Confluence

| Field | Value |
|---|---|
| Space | `ux` (Impact UX) — spaceId `393347460` |
| Status | Prefer `draft` until designer sign-off |
| Parent | Link under the initiative one-pager or UX Roadmap child — ask designer if unclear |
| Title pattern | `Test findings — [initiative name] — [YYYY-MM-DD]` |
| Tool | `createConfluencePage` (markdown) |

### Body skeleton

```markdown
## Summary
[1–2 sentences — decision: ship / iterate / reframe]

## Verified findings
- …

## vs success criteria (from one-pager)
| Criterion | Result |
|---|---|
| … | confirm \| contradict \| inconclusive |

## Artifacts
- Study: Outset | Maze link
- Prototype tested:
- Epic / one-pager:

## AI interpretation (secondary)
- …

**Audience:** Brand | Partner | Shared
**Status:** Test loopback — feeds next Empathize cycle
```

## Jira

Prefer **comment on existing UX Epic** from Define over creating a new epic.

| Action | When |
|---|---|
| `addCommentToJiraIssue` | Default — append Verified summary + Confluence URL to framing epic |
| `createJiraIssue` | Only if designer asks for a dedicated Research sub-task |

Comment skeleton:

```markdown
**Usability test loopback** ([date])

**Recommendation:** ship | iterate | reframe | monitor

**Verified highlights:**
- …

**Full findings:** <confluence url>

**Prototype:** …
```

## Dedup

Search Confluence space `ux` and JQL `project = UX AND text ~ "[initiative]"` before create. Update existing findings page if same study round.

## Link both ways

1. Create Confluence findings page → URL
2. Comment on UX Epic with link
3. Optional: add Confluence back-link to epic in findings page body

Do **not** edit UX Roadmap unless designer asks.
