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

**Lead with the insight, not the evidence.** What the person gets back is
short: the finding, what it changes, and the next thing to do. A few lines, not
a report — they came for a decision, not a download.

**Offer the depth, don't deliver it.** Close with one specific follow-up they
can run — "want the evidence trail behind finding 2?" — not a menu of five. The
detail stays available; it does not arrive unasked.

**A number earns its place by changing a decision.** Everything else goes in the
artifact (the claim, the card, the one-pager) where someone can find it when
they need it.

1. Require **completed sessions** (Outset/Maze export, Dovetail notes, or designer paste).
2. Run `synthesize-research` or brief `user-research` on the corpus **before** publish.
3. Label every finding **Verified** (quote/metric from session) vs **AI interpretation**.
4. Do **not** promote AI synthesis to the research pack without designer confirm.
5. **Only publish after designer confirms** the loopback summary.
6. **Atlassian Rovo MCP** — fetch the framing epic with `getJiraIssue` / `search` yourself. Do not ask the designer to paste the ticket or run `/mcp` until a tool call fails.
7. **Every finding points at a moment.** Participant id, timestamp, clip link.
   A stakeholder who cannot watch the thing happen is being asked to take it on
   trust, and in six months nobody will remember which session it came from.
8. **Frequency and cost are separate columns.** How many hit it, and what it
   cost them. A readout ranked by mentions buries the blocker one person could
   not get past.
9. **Publish what worked too.** Findings with nothing disconfirming read as
   advocacy, and the designer cannot tell which parts of the design to keep.
10. **State observations, not recommendations.** "Four of six re-entered details
    after the error" is a finding the reader can act on. "We should redesign the
    error state" is your opinion wearing the research's authority.

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

## What we asked
- Research question · why this mode · thresholds agreed before sessions
- Decision owner: …

## Verified findings (from sessions)
| Theme | n / N | Cost to participant | Evidence (Verified) | vs threshold |
|---|---|---|---|---|
| … | 4 / 6 | abandoned \| worked around \| recovered | P3 14:22 + clip link | met \| missed \| inconclusive |

Ranked by cost first, then frequency.

## What worked
- Tasks completed unaided, and by whom
- Participants who did **not** hit the main finding, and what was different
  about them

## AI interpretation (review before publish)
- …

## Task outcomes
| Task | Completion | Notes |
|---|---|---|
| … | … | … |

## What this means for the decision
- Against the thresholds agreed before sessions: …
- What it changes · what it does not address

## What this cannot tell you
- Sample size and who was excluded · tasks not covered · segments absent ·
  questions these sessions never asked

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
