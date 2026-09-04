---
name: test-loopback
description: >-
  Publishes Verified usability-test findings to Confluence and Jira as Empathize
  input after sessions complete. Use after Outset/Maze when the designer wants
  findings looped back to research context — not for synthetic pre-test output.
license: Proprietary
metadata:
  stage: test
  pipeline: impact-ux-designops
  author: impact.com-ux
  figjam-agent: Test Plan Generator
---

# Test loopback (Test → Empathize)

Closes the design-thinking loop: **real session findings** → durable
research artifacts for the next Empathize cycle. Runs **after** sessions —
never on AI-drafted study plans or synthetic pre-tests alone.

## Integrity

1. Require **completed sessions** (Outset/Maze export, Dovetail notes, or designer paste).
2. Run `synthesize-research` or brief `user-research` on the corpus **before** publish.
3. Label every finding **Verified** (quote/metric from session) vs **AI interpretation**.
4. Do **not** promote AI synthesis to the research pack without designer confirm.
5. **Only publish after designer confirms** the loopback summary.
6. **Atlassian Rovo MCP** — fetch the framing epic with `getJiraIssue` / `search` yourself. Do not ask the designer to paste the ticket or run `/mcp` until a tool call fails.

See [references/publish.md](references/publish.md), [references/integrity.md](references/integrity.md), and [references/atlassian-rovo.md](references/atlassian-rovo.md).

## When to use

- Outset/Maze study finished; need findings in Confluence/Jira
- “Loop test results back to Empathize” / “publish usability findings”
- PM/stakeholder readout prep from **Verified** session data

## Context gathering (always)

| Source | How |
|---|---|
| Session corpus | Outset/Maze export, Dovetail project, pasted notes/transcripts |
| Framing | Original one-pager, epic (`getJiraIssue` if they named a key), `test-plan` draft link |
| Prototype | URL tested + decision under review |
| Prior synthesis | `synthesize-research` output if already run |

## Workflow

1. **Gate** — Confirm sessions are complete (not just a study draft). If only synthetic pre-tests exist, stop → not loopback-ready.
2. **Synthesize** — Run `synthesize-research` on the session corpus (single study set). Or `user-research` for a gate brief if N is tiny.
3. **Draft loopback pack** — Themes, Verified quotes (anonymized), task outcomes, recommendation vs kill/iterate/pivot.
4. **Link framing** — Tie findings to original success criteria from one-pager/epic; note confirm / contradict / inconclusive.
5. **Designer review** — Show pack; strip or relabel anything not Verified.
6. **Publish** (on confirm only) — Confluence findings page + Jira comment or linked issue update. See [references/publish.md](references/publish.md).
7. **Stop** — Point designer to Empathize skills (`research-synthesis`, `data-analyze`) if quant follow-up needed.

## Output template

```markdown
# Test loopback — [title]
Status: DRAFT (pending designer confirm) | PUBLISHED
Study: Outset | Maze | mixed
Audience: Brand | Partner | Shared

## Decision this informs
[Ship | iterate prototype | reframe problem | monitor]

## Verified findings (from sessions)
| Theme | Evidence (Verified) | vs success criteria |
|---|---|---|
| … | quote / metric | confirm \| contradict \| inconclusive |

## AI interpretation (review before publish)
- …

## Task outcomes
| Task | Completion | Notes |
|---|---|---|
| … | … | … |

## Recommendation
- …

## Links
- Test plan / prototype:
- One-pager / epic:
- Confluence (after publish):
- Jira (after publish):

## Human gate
- [ ] Designer confirmed Verified labels
- [ ] Ready to publish to Confluence/Jira
- [ ] Stakeholder summary approved (if sharing externally)
```

## Prompt examples (tested)

1. `Use test-loopback on this Outset export — link to UX-1234 epic and publish draft to Confluence ux space.`
2. `Use test-loopback after synthesize-research on Maze results — do not publish until I confirm.`
3. `Use test-loopback: sessions done, here's Dovetail link — loop to Empathize, no stakeholder email yet.`

## Anti-patterns

- Publishing synthetic `accessibility-review` or pre-test critique as session findings
- Looping back without tying to original success criteria
- Auto-updating UX Roadmap or creating duplicate epics
- Asking the designer to paste a Jira issue or enable Atlassian Rovo before calling the MCP tools
- Pasting participant PII into Confluence/Jira
