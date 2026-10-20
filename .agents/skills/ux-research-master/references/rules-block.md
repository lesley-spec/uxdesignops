<!-- BEGIN ux-research-master (managed — edit the skill, not this block) -->
## UX pack routing

This project has the impact.com UX DesignOps skill pack installed
(`.agents/skills/`, mirrored to `.claude/skills/` and `.cursor/skills/`).

When a message is about users, research, evidence, personas, a spec, mocks, a
prototype or product analytics, **load the matching skill before answering**.
Read `.agents/skills/ux-research-master/references/routing.md` and follow it.
Say which skill you loaded and why, in one line. Do not answer a research
question from general knowledge while a skill for it exists.

Quick map — full table in `routing.md`:

| Message is about | Skill |
|---|---|
| What do we know / is this supported / blindspots / rank on evidence | `user-context` |
| Frame staleness, what to retire, what to research next | `frame-maintenance` |
| Personas, who owns this problem | `user-personas` |
| A research request to triage or route | `research-intake` |
| Designing a study, guide, screener | `research-planner` |
| Dashboards, audience, instruments, Pendo guides | `research-builder` |
| Funnels, drop-off, trends | `data-analyze` |
| Triangulating sources / theming one corpus | `research-synthesis` / `synthesize-research` |
| One-pager, PRD, epic | `write-spec` |
| Pressure-testing framing | `anti-sycophancy` |
| Mocks vs spec | `ux-critique` |
| Pre-testing a prototype with a persona | `persona-check` |
| Usability test plan / accessibility pass | `test-plan` / `accessibility-review` |
| Post-launch, did it work | `adoption-check` |
| Unclear, or the full guided run | `ux-research-master` |

Always: label Verified vs AI interpretation · never invent metrics, quotes or
participants · drafts only for Jira, Confluence, Outset and Pendo until a
human confirms · never launch recruitment or publish a guide to live traffic.

**Answer short.** Lead with the finding and what it changes — a few lines, not
a report. Offer one specific follow-up rather than delivering the detail
unasked. A number earns its place by changing a decision; everything else
belongs in the artifact, where it can be found when it is needed. This
constrains the output, not the rigour.

Starter prompts: `/ux` for the menu, or `/ux-frame`, `/ux-context`,
`/ux-intake`, `/ux-personas`, and the rest in
`.agents/skills/ux-research-master/references/prompts.md`.
<!-- END ux-research-master -->
