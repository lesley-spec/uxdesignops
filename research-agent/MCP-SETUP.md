# MCP Setup — Research Agent

Project MCP servers are in [`.cursor/mcp.json`](../.cursor/mcp.json). **Claude and Cursor use separate OAuth** — connecting in Claude does not connect Cursor.

## Claude vs Cursor

| | Claude | Cursor |
|---|--------|--------|
| How MCPs connect | First-party connectors (Settings → Connectors) | `.cursor/mcp.json` + Customize → Connect |
| OAuth | One-time per connector in Claude | One-time per server in Cursor |
| Tokens shared? | No | No |

If MCPs work in Claude, you still need to **Connect each one again in Cursor**.

## Current status in Cursor

| Server | Status | Notes |
|--------|--------|-------|
| **posthog** | Connected | Ready to use |
| **pendo** | Connected | Ready to use |
| **atlassian** | Connected | Via Cursor Atlassian plugin (Confluence/Jira) |
| **dovetail** | Needs API token | Generate at Account Settings → add to `research-agent/.env` |
| **outset** | OAuth MCP + API key in `.env` | MCP at `https://api.outset.ai/mcp/` creates draft studies (`studies:write`). v1 `OUTSET_API_KEY` lists studies only. Do not launch recruitment unless asked. |

## Dovetail in Cursor (not OAuth)

Claude uses a first-party Dovetail connector. **Cursor needs an API token** — being logged into dovetail.com is not enough.

1. While logged in, open [Dovetail Account Settings → Personal API keys](https://dovetail.com/settings/user/account)
2. Create a key (starts with `api.`) — copy it immediately (shown once)
3. Add to `research-agent/.env`:
   ```
   DOVETAIL_API_TOKEN=api.your_token_here
   DOVETAIL_API_KEY=api.your_token_here
   ```
4. **Developer: Reload Window** in Cursor
5. Check **Customize → MCP** — dovetail should show tools

The MCP uses a local stdio server that reads your token from `.env` (not committed to git).

## Verify in chat

Once connected, try:

- "Query PostHog for signup funnel drop-offs this week"
- "Find Dovetail insights about onboarding friction"
- "Summarize our latest Outset study findings"
- "Create a Confluence page in the Research space"

## Atlassian (Confluence)

Use the **Atlassian plugin** already installed in Cursor — no need to duplicate it in `mcp.json`. It covers Confluence pages for the weekly research agent output.

## MCP vs scheduled agent

| Use case | Tool |
|----------|------|
| Interactive research in Cursor or Claude | MCP (OAuth) |
| Weekly automated GitHub Actions run | REST APIs in `agent_cloud.py` |

The scheduled agent uses API keys in GitHub Secrets. MCPs are for you and the AI assistant during development and ad-hoc analysis.
