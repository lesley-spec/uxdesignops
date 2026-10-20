---
name: research-intake
description: >-
  Research request front door for impact.com UX. Four questions, two checks,
  one route: is there a decision, do we already know the answer, and if not —
  MICRO (48 hours), SPRINT (1–2 weeks), or DEEP (4+ weeks), run by research or
  by the team that asked. Use when someone files or asks for research, or says
  research request, research intake, triage this, route this study, scope this
  research, is this micro sprint or deep, or asks UX Research to look into
  something.
license: Proprietary
metadata:
  stage: empathize
  position: entry
  pipeline: impact-ux-designops
  author: impact.com-ux
  modes: micro|sprint|deep
---

# Research intake

The front door for research requests. **Four questions, two checks, one route.**

This is deliberately light. It is a v1 meant to be used and then corrected — if
a step here feels like paperwork, cut it and say what you cut. Weight gets added
later, from evidence that something was missed, not up front in case it is.

Modes come from Constantine Papas, *AI-Powered UX Research*, ch. 4 — as does
the Frame, which is his term for what the organisation believes, how confident
it is, and where the gaps are. The question of who *runs* the work comes from
Lozé's bronze/silver/gold model, kept as a separate question here because effort
and ownership come apart more often than one label allows.

## Integrity

1. **Check before you plan.** A request that is already answered does not need
   a method.
2. **No decision, no study.** Research with nothing waiting on it becomes a
   document nobody reads.
3. **Speed never lowers the mode.** Say the conflict out loud; let the requester
   choose. Shrinking method to fit a deadline produces confident fiction.
4. **Draft the ticket, don't create it.** Show it first.
5. **"Already answered" is a win.** Log it. It is the cheapest research we do.
6. **A route is not just a size, it carries a rigor gate.** Every mode gets the
   3-participant pass and thresholds agreed with the decision owner before
   fieldwork — `research-planner` sets both. Routing something as MICRO shortens
   the study, never the gates.

## Who runs intake

**One named person at a time, checking once a day.** Default: Nihal Somers. If
they cannot, they hand it to someone **by name** — never back to the queue.

Daily is not ceremony, it is what makes the 48-hour MICRO promise true. Triage
twice a week and a request filed on Tuesday gets routed Friday, so the clock is
blown before anyone starts. Most days the check takes a minute.

This section exists because a process nobody owns is exactly the thing Check 1
rejects: work with no one waiting on it, which becomes a document nobody reads.
A triage step that runs when someone remembers is not a triage step.

## The four questions

Ask these, batched, in whatever words fit the conversation.

| | Ask | Gives you |
|---|---|---|
| 1 | **What do you want to know?** | The question |
| 2 | **What decision does it inform, and who makes it?** | Check 1 |
| 3 | **When do you need it, and how long does the answer need to hold?** | The constraint |
| 4 | **What happens if we get this wrong?** | The routing axis |

That is the whole form. Do not add fields — ambiguity and domain are yours to
judge, not theirs to fill in, and every extra question costs you a request that
never gets filed.

Question 3 is two halves on purpose. *When you need it* is a deadline. *How long
it must hold* is shelf life. A copy test decided Friday and stale next quarter is
fine; a two-week study whose answer expires in one is not.

Question 4 asks about **consequence, not cost**. Ask "how much rides on it" and
you get an answer about budget or headcount — what it costs to find out, which
tells you nothing about how bad a wrong answer would be. A cheap decision can be
expensive to get wrong. Listen for whether it is reversible.

If they named a Jira key, fetch it (`getJiraIssue`) before asking them to paste
anything.

## Check 1 — Is there a decision?

One question, asked of the requester:

> **If the answer comes back the opposite of what you expect, what changes?**

A real answer means there is a decision and someone owns it. No answer means one
of two things, and both are conversations rather than rejections:

| What you're hearing | Say |
|---|---|
| The call is already made | Offer to pressure-test it instead, or to look at it after they ship |
| It's a design choice, not a question about users | Reframe it once — "should we add a confirmation screen?" becomes "do partners believe their submission worked without one?" |

Reply template: [references/templates.md](references/templates.md).

## Check 2 — Do we already know?

Look before you plan. Proportionate to the ask — a 48-hour question gets a
15-minute look, not a full audit.

| Where | For |
|---|---|
| **The Frame** — [claims + needs](https://claude.ai/artifact/FHc7oAPoyohgxo87VdxCGw) | Do we already believe something about this? **Always first.** |
| **Dovetail** | Have we interviewed on this? |
| **Outset** | Has a study already run — or is one running right now? |
| **PostHog** | Only if the question is behavioural |

**Read the Frame before touching a connector.** It is one `ArtifactData` query,
instant, already graded, and it records what was unanswerable last time — the
single most useful thing to know before planning a study. Filter `claims` by
domain and segment; check `needs` for whether this is already a named gap.
Skipping it is how you spend five API calls rediscovering something a colleague
wrote down.

A **contested** claim does not close a request, whatever its confidence. Route it
and say which two readings disagree.

**A partial check is provisional, and provisional does not get routed on.** If a
source is unavailable, say which half you ran, give the verdict as provisional,
and stop. Do not pick a mode.

This is not caution for its own sake. One source will hand you a plausible,
confident answer — and the source you skipped is disproportionately the one that
disagrees, because a second source only changes the verdict when it says
something different. A half-run check is not a weaker version of the full one;
it is a different answer that looks identical.

**Budget about five calls and a few minutes** for the full check: briefs, a
Dovetail search, then Outset search → project → reports → topline. It is not a
glance. Saying so is what stops it being quietly skipped.

Invoke `user-context` in `ask` mode when you want the full version — it sweeps
every source properly, with counter-evidence, and records what it finds back
into the Frame.

Three verdicts, not five grades:

| Verdict | Means | Do |
|---|---|---|
| **Solid** | Clear evidence, right segment, still current | **Close.** Send the link. |
| **Thin** | Right area, wrong segment, or ageing | Route — but the scope just got smaller |
| **Nothing** | No coverage of this area at all | Route in full. If the *area* is unknown, that is a DEEP signal. |

**Solid has a bar, because Solid closes tickets.** It means you could put the
finding in front of the decision owner and defend it:

1. It covers **the segment they asked about** — not an adjacent one
2. It **states how many people** it is based on
3. **Nothing has changed since** that would undermine it — no relevant ship, no
   pricing change, and not simply old

Miss any of the three and it is **Thin**. Thin is not a failure; it still cuts
the scope, often by a lot.

**The bar scales with consequence.** If question 4 said the decision is big or
hard to undo, one source is not enough — Solid then needs two that agree and
were gathered independently. A reversible decision can rest on one good study;
an irreversible one should not.

A study already in flight routes to **wait**, not to a second study.

## Step 3 — Route

### First — can it be answered at all?

Before picking a mode, check the question does not turn on something nobody
measures. If the decisive evidence would come from an event that is not
instrumented, a funnel that does not exist, or a field nobody fills in, **no
amount of research fixes that.**

The route is **instrument first, then a MICRO** — an instrumentation ticket, and
a small study once the data exists. Say it plainly: the question is good, the
measurement is missing, and running a study now would produce opinion dressed as
evidence.

This is a real outcome, not a failure to route. It is also the one the three
modes cannot express, because all of them assume research is the thing standing
in the way.

### Then — what shape

| | MICRO | SPRINT | DEEP |
|---|---|---|---|
| **Turnaround** | 48 hours | 1–2 weeks | 4+ weeks |
| **Ambiguity** | We understand the problem | Mostly | We don't |
| **Consequence** | Small or reversible | Material | Big or hard to undo |
| **Shape** | One question | 1 central + 2–4 sub | Open-ended |
| **Method** | Persona chat, data query, one Outset study | Outset study + 2–5 human follow-ups | Contextual inquiry, 15–20 participants |
| **The Frame** | Uses what we know | Fills gaps in it | **Builds it** |

**Score ambiguity and consequence separately; the higher one wins.** Not both
together — a clear problem with a big consequence is still DEEP.

**Ambiguity wins outright.** If we cannot state the problem, it is DEEP whatever
else is true. A 48-hour study against a question nobody can phrase buys
confidence, not knowledge.

**Stuck between MICRO and SPRINT?** Ask whether one Outset study answers it
alone. Yes → MICRO. Needs human follow-up to interpret → SPRINT.

### Who runs it

> **Can the person who asked run this, with support?**

| | Who | Research does |
|---|---|---|
| **Team-led** | The designer, PM, or CX person who asked | Agrees the method, looks at the guide, reads the analysis |
| **Research-led** | Us | All of it |

Most MICRO and a good share of SPRINT can be team-led. DEEP is research-led —
foundational work is where the Frame comes from.

This question is the one that stops the queue becoming a bottleneck. Ask it
every time, even when the answer is obvious.

### Timing

The deadline is a **constraint, not an input**. It never lowers the mode. When
the mode needs longer than they have, offer three things and let them pick:

1. Move the date.
2. Narrow the question until a faster mode honestly answers it.
3. Take a quick read now, labelled as directional and not decision-grade.

Option 3 is legitimate. Running option 3 while calling it the full study is not.

## Step 4 — Ticket and handoff

Draft the ticket ([references/templates.md](references/templates.md)), show it,
create it on confirm.

**Where it goes:** Jira project `UX`, [board 679](https://impact.atlassian.net/jira/software/projects/UX/boards/679).
Type **Research** or **Analytics** — the *method* picks it, not the mode.
Assignee **Nihal Somers** unless someone else is taking it.

| Mode | Next |
|---|---|
| **Instrument first** | Instrumentation ticket to the squad; a MICRO once the data lands |
| MICRO | `user-context`, `data-analyze`, or one Outset study |
| SPRINT | `user-research` — the study plus the follow-up calls |
| DEEP | `user-research` — contextual inquiry, then recruit |

Team-led work hands to the requester with the three support points agreed.
Intake recommends; the research lead decides.

## Re-routing

Routing once at intake is a guess made at the moment of least information. Three
signals say re-route, and any of them is enough:

- The same pattern keeps turning up across studies or teams
- We can see *what* people do but not *why*
- People read the findings differently and argue about what they mean

The usual case: a usability test reveals people don't understand what the thing
is for, and a design question turns strategic. That is a success, not a scope
failure — say so, and re-route it.

## References

- [references/routing.md](references/routing.md) — the three modes in full, and
  two bugs in the original routing spec that this version fixes
- [references/templates.md](references/templates.md) — reply templates and the
  ticket template

## What to watch

One number, and it costs nothing to collect: **how often you close a request as
already answered.** If it rises, the Frame is compounding and intake is paying
for itself. If it stays at zero, either nothing is being reused or Check 2 is
being skipped — both worth knowing.

Everything else — cycle time, rejection mix, capacity — wait until there is a
reason to want it.
