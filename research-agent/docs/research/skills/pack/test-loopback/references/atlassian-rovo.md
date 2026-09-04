# Atlassian Rovo MCP — Jira and Confluence

**Call this yourself. Do not wait for the designer to say the connector is on.**

Jira and Confluence in this pipeline go through the **Atlassian Rovo MCP** (Claude: Settings → Connectors → Atlassian Rovo; Cursor: Atlassian plugin). Same tools either way.

## Do this first

1. If the designer names a ticket (`TTPI-478`, `UX-1234`, any `PROJECT-123`), **immediately** call `getJiraIssue` with that key.
2. For lookup without a key, call `search` (Rovo Search) across Jira + Confluence, then `getJiraIssue` / `getConfluencePage` for the hits you need.
3. Discover tools and invoke them. Do **not** assume a “non-interactive session” cannot OAuth. Do **not** ask them to run `/mcp`, paste the issue, or enable the connector **until a tool call actually fails**.

## Site

- Cloud: `https://impact.atlassian.net`
- `cloudId`: `8bd0a64b-b516-411d-b33c-b692737a5317`

## Tools (call these — do not describe them to the designer)

| Need | Tool |
|---|---|
| Fetch one issue | `getJiraIssue` (`cloudId`, `issueIdOrKey`) |
| Search Jira + Confluence | `search` (Rovo Search) — default unless they asked for JQL/CQL |
| JQL | `searchJiraIssuesUsingJql` |
| CQL | `searchConfluenceUsingCql` |
| Full page | `getConfluencePage` |
| Create epic (after confirm) | `createJiraIssue` — project `UX` |
| Comment on epic (after confirm) | `addCommentToJiraIssue` |
| Create one-pager (after confirm) | `createConfluencePage` — space `ux` |

If the namespace is `needsAuth`, run the MCP auth flow for Atlassian, then retry the same tool. Only then tell the designer the connector needs a one-time authorize.

## Anti-patterns

- “I can’t access Jira in this session — paste the title/description”
- “Open Claude in a terminal and run `/mcp`” as the **first** response
- Waiting for “Atlassian Rovo connector is on” before calling tools
- Inventing ticket fields instead of `getJiraIssue`
