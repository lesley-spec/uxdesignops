---
name: ux-research-master
description: >-
  One front door for the whole impact.com UX pack. First run installs all 31
  skills plus the /ux-* starter prompts and writes the routing rules, so after
  that a plain-English message gets matched to the right skill on its own.
  Research-led: it asks what decision this unlocks and what the Frame already
  says before it asks anyone to run a study. Use when the user says
  ux-research-master, /ux, install the UX skills, set me up, get started,
  which skill should I use, or opens a UX or product question without naming a
  skill.
license: Proprietary
metadata:
  stage: pipeline
  pipeline: impact-ux-designops
  author: impact.com-ux
  figjam-agent: UX Research Master
---

# UX Research Master (front door)

**One skill to remember.** It installs the pack, prints the starter prompts,
and routes everything after that. It does not do research itself — it names
the skill that should, loads it, and gets out of the way.

Three masters sit under this one. Know the difference:

| Master | Owns |
|---|---|
| `ux-research-master` (this) | Install, routing, starter prompts. Entry point. |
| `ux-research` | A guided **research** run: intake → Frame → plan → build |
| `design-thinking-ux` | A guided **design** run: Empathize → Define → Ideate → Prototype → Test |

Routing table: [references/routing.md](references/routing.md) ·
Starter prompts: [references/prompts.md](references/prompts.md) ·
Rule block: [references/rules.md](references/rules.md).

## Integrity

1. **Route, don't rewrite.** When routing says invoke `skill-name`, Read
   `.agents/skills/<name>/SKILL.md` (fallback `.claude/skills/` or
   `.cursor/skills/`) and run that skill's workflow in **this** chat. Never
   paraphrase a child skill from memory, and never ask the designer to type
   `use skill-name` themselves.
2. **Name the pick, then proceed.** One line — the skill, why it fits, and the
   runner-up — then start. Only stop and ask when the top two lead to
   genuinely different outcomes.
3. **Evidence before fieldwork.** A question that may already be answered goes
   to `user-context` or `research-intake` before `research-planner`. Never
   route straight to a new study because someone asked for one.
4. **Label Verified vs AI interpretation.** Never invent a metric, a quote or
   a participant. A synthetic persona pass is a hypothesis, never a finding.
5. **Honour child stop conditions.** Jira, Confluence, Outset and Pendo stay
   draft-only until a human confirms. Never launch recruitment or publish a
   guide to live traffic.
6. **Install once, silently after that.** Only re-run the installer when the
   pack is missing or the designer asks.
7. **Say what is degraded.** If a connector the chosen skill needs is not
   authorised, say so before running, name what the skill will fall back to,
   and continue — do not pretend the data is there.

## When to use

- "use ux-research-master" · `/ux` · "install the UX skills" · "set me up"
- "which skill should I use for…" · "what can this pack do"
- Any UX, research or product question where no skill was named

If they named a **single** skill, run that one. If they asked for the full
research run, hand to `ux-research`. If they asked for the full design run,
hand to `design-thinking-ux`. Do not wrap a named skill in this one.

## First run in a project

Detect first run: `.agents/skills/ux-research-master/` is absent, or
`.claude/commands/ux-frame.md` is absent, or the rule block is not in
`CLAUDE.md`.

```
Task Progress:
- [ ] Run install-master.sh (sandbox off)
- [ ] Parse UX_MASTER_READY
- [ ] Connector preflight
- [ ] Print the menu, then stop
```

1. **Install.** Run with the sandbox off (Cursor Shell:
   `required_permissions: ["all"]` — it writes to `~/.claude` and `~/.cursor`).

   ```bash
   bash ".agents/skills/ux-research-master/scripts/install-master.sh"
   ```

   Not on disk yet? Bootstrap the whole pack, master included:

   ```bash
   curl -fsSL https://lesley-spec.github.io/uxdesignops/skills/install-all.sh | bash
   ```

   This installs 31 skill folders, 16 `/ux-*` commands (project + global,
   Cursor + Claude Code), and writes the routing block into `CLAUDE.md` and
   `AGENTS.md`. Flags: `--project-only` · `--global-only` · `--no-rules` ·
   `--target PATH`.

2. **Parse** `UX_MASTER_READY skills=31 commands=16 rules=…`. Do not claim a
   count the script did not print.

3. **Connector preflight.** Check which MCP servers are authorised in this
   harness and report in one short block — what is live, what is not, and
   which prompts degrade. Mapping: [references/routing.md](references/routing.md#connectors).
   Never ask for tokens; tell them to authorise in connector settings or
   `/mcp`.

4. **Print the menu** from [references/prompts.md](references/prompts.md) —
   the 15 starter prompts in their four groups, plus "or just describe what
   you're working on."

5. **Stop.** Wait for a number, a `/ux-*` command, or a sentence.

No shell (Claude.ai chat, Figma Make): do not pretend an install ran. Point at
the [skills page](https://lesley-spec.github.io/uxdesignops/skills/) and the
zip, say the `/ux-*` commands need Cursor or Claude Code, and keep routing by
hand in this chat — routing works without an install.

## Every run after that

1. Read the message. Match it in [references/routing.md](references/routing.md).
2. Say the pick in one line: *"That's a Frame question — loading `user-context`
   (runner-up: `research-synthesis` if you want the sources triangulated)."*
3. Load that skill and run it.
4. At its stop, name the next step and wait. Never auto-advance past a human
   gate.

If nothing matches, ask one question — what decision this unlocks — and route
on the answer. If five things match, pick the one that answers the decision
soonest and name the rest.

## The four questions behind the routing

Research-led means these come first, in this order, whatever was asked:

1. **What decision does this unlock?** No decision → no study. Say so.
2. **Do we already know?** → `user-context`. A question already answered does
   not need a method.
3. **If not, how big?** → `research-intake` routes MICRO (48h) / SPRINT (1–2w)
   / DEEP (4w+), and who runs it.
4. **How will we know it worked?** → the measure gets built **before** the
   study, not after. `research-builder`, then `adoption-check` post-ship.

## Anti-patterns

- Printing the menu again on every turn — once per session is enough
- Routing to `research-planner` before anyone checked the Frame
- Re-running the installer because the designer said hello
- Answering a research question from this skill instead of loading the child
- Reporting a connector as missing without saying which prompts it degrades
- Listing five candidate skills and asking the designer to choose
