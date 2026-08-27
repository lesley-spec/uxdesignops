# Impact.com Empathize sources

| Source | Role | Typical access |
|---|---|---|
| PostHog | Funnels, drop-offs, trends, replay links | PostHog MCP; project Impact Membersite |
| Pendo | Guides, polls, open-text feedback | Pendo MCP |
| Dovetail | Insights, highlights, notes | Dovetail MCP / API (`research-agent/dovetail_api.py`) |
| Outset | Qualitative studies | Outset MCP (interactive; limited REST) |
| Freshdesk | Support tickets | BigQuery path in research-agent |
| Research Insight Monitor | Scheduled weekly pack | `research-agent/docs/research/latest.json` + HTML reports |

## Report fields to prefer

From `latest.json`: `summary`, `posthog_dropoffs`, `source_counts`, `by_audience`, per-issue `research_context`, severity, links.

## Audience & themes

Align with `research-agent/issue_taxonomy.py`: Brand / Partner / Shared and the theme keyword rules there.
