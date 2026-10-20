# Query playbook (impact.com)

## PostHog

- Default project context: Impact Membersite when already configured in the harness.
- Prefer `query-trends` / `query-funnel` / `query-retention` / `query-paths` after `read-data-schema`.
- Keep `filterTestAccounts` on unless the user asks otherwise.
- Provide app URLs from tool `_posthogUrl` or `generate-app-url` — do not invent paths.
- **Dedupe on person + timestamp, never on session** — Membersite loads two SDKs
  and every event lands twice under different session ids.
- **PostHog has no native app data.** `mobile` here is mobile web; iOS and
  Android live in Pendo and Looker. Say that rather than answering with web.

## Pendo

- Pages/features/track events vs **objects** — use object analytics tools only for designated business objects.
- Prefer list/search entities before guessing app or feature ids.

## Research agent alignment

Scheduled funnel drop-off logic lives in `research-agent/agent_cloud.py`. For weekly packs see `research-agent/docs/research/latest.json` before re-querying the same funnels.
