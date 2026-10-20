# Starter prompts

Eight ways in, in the words a designer or PM would use. Print the **menu**
once, after install or when someone asks what this can do. Expand a prompt
only when they pick it.

Each one is also a slash command in Cursor and Claude Code, project and
global.

## The menu (print this)

```
How can UX research help you today?

 1  "What do we already know about this?"
 2  "Who am I designing for, and what are they trying to get done?"
 3  "Give me a few directions to explore for this problem."
 4  "Do these mocks actually solve the problem we wrote down?"
 5  "Run a heuristic review on this."
 6  "Walk a user through this before I put it in front of real people."
 7  "I need research on this — what's the fastest way to a real answer?"
 8  "We shipped it. Did it make any difference?"

Pick a number, type the matching /ux- command, or just tell me what
you're working on.
```

Nothing else goes on the menu. The other 22 skills route from plain chat —
see [routing.md](routing.md).

## 1 · `/ux-context` — What do we already know

> What do we already know about **<area / flow / cohort / question>**? Sweep
> Dovetail, PostHog (session replay included), Outset, Pendo and support
> tickets. Grade what you find — Verified, Indicative, Anecdotal — name the
> gaps, and say plainly what we cannot answer from what exists.

Loads `user-context`. Also the right prompt for *"is this hypothesis
supported"* and *"which of these should we build first"* — same skill, say the
hypothesis or list the options and it handles both. Sources disagree →
`research-synthesis`.

## 2 · `/ux-personas` — Who am I designing for

> Who am I designing for in **<problem / flow>**, and what are they trying to
> get done? Walk me through the personas in play, their jobs to be done, their
> workflow around this, and how confident each claim is. If it spans two, say
> which one it must satisfy first and why.

Loads `user-personas`. Then `brand-operator-ux-persona` or
`creator-affiliate-ux-persona` for the deeper lens on one side.

## 3 · `/ux-ideate` — Directions to explore

> Give me a few directions to explore for **<problem>**. Start from the
> framing we have — one-pager, PRD, epic, tickets or notes — and seed
> genuinely different approaches, not three versions of one idea. Say what
> each one assumes and what it would cost to be wrong.

Loads `ideate`. `design-system` first when the output is heading for on-brand
mocks.

## 4 · `/ux-critique` — Do these mocks solve it

> Mocks: **<links>**. Spec: **<one-pager / epic / tickets>**. Build the
> coverage matrix — what the framing asked for versus what the mocks do — then
> critique the solution itself. Flag anything the spec needed and the design
> silently dropped.

Loads `ux-critique`. This is the *right problem* question. For usability
principles use 5; for a named person's journey use 6.

## 5 · `/ux-heuristics` — Heuristic review

> Run a heuristic review on **<screen / flow / prototype / frame>**. It's for
> **<brand / partner>**, and the job it exists to do is **<task>**. Ten classic
> heuristics plus the marketplace ones — two-sided consequence, money
> legibility, role truth, scale asymmetry. Rank by consequence, give me the
> cheapest fix for each, and tell me what a static frame can't show you.

Loads `heuristic-review`. Expert judgement, never evidence. Minutes, no
recruiting, no connectors.

## 6 · `/ux-persona-check` — Walk a user through it

> Walk **<persona>** through **<prototype URL / flow / copy>** as a task.
> Where do they hesitate, what do they look for and not find, what do they do
> instead? Everything here is a hypothesis to test with real people — never a
> finding.

Loads `persona-check`. A pre-test, never a substitute for recruiting. Pair
with `accessibility-review` before sessions.

## 7 · `/ux-intake` — Fastest way to a real answer

> I need research on **<question>**. What's the fastest way to a real answer?
> What decision does this unlock, do we already know, and if not — 48 hours,
> two weeks, or four-plus, and who should run it?

Loads `research-intake`. The "do we already know" check runs through
`user-context` first; if it is already answered, it says so and stops rather
than routing a study. Routed requests continue into `research-planner` and
`research-builder`.

## 8 · `/ux-adoption` — Did it make any difference

> We shipped **<thing>** on **<date>**. Read the baseline, re-run the measure
> in PostHog, and tell me whether the research held. Write the outcome back as
> a claim.

Loads `adoption-check`. The claim gets written either way — a miss is
evidence.

## House rules for every prompt

- Fill the `<placeholders>` from what they already said. Ask once for what is
  genuinely missing, and only for what the skill cannot start without.
- Verified vs AI interpretation, labelled, every time.
- Drafts stop at the human gate. Nothing publishes, launches or recruits.
- If a connector the prompt needs is not authorised, say which, say what the
  answer loses, and run the rest.
