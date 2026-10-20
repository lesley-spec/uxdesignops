# Starter prompts

Fifteen ways in. Print the **menu** once per session; expand a prompt only
when they pick it. Each prompt is also a slash command in Cursor and Claude
Code, project and global.

## The menu (print this)

```
UX pack ready. Pick a number, type a /ux- command, or just say what you're working on.

  EVIDENCE
   1  /ux-frame          What's in the Frame, how confident, what's gone stale
   2  /ux-context        What do we know about <area / cohort / flow>?
   3  /ux-evidence       Is this hypothesis supported? Where are the blindspots?
   4  /ux-personas       Who are our users, and which one owns this problem?

  RESEARCH
   5  /ux-intake         I have a research request — triage and route it
   6  /ux-study          Design the study: questions, sample, probes, thresholds
   7  /ux-measure        Build the measure and the audience before we run

  PRODUCT
   8  /ux-prioritise     Rank these options on evidence, not opinion
   9  /ux-pressure-test  Poke holes in this framing before anyone agrees with it
  10  /ux-spec           Turn confirmed research into a one-pager + epic
  11  /ux-adoption       We shipped it — did it work?

  DESIGN
  12  /ux-critique       Do these mocks cover the spec?
  13  /ux-persona-check  Walk a persona through this before we recruit
  14  /ux-test-plan      Plan the usability test

  DATA
  15  /ux-data           Funnel, drop-off, trend — a quantitative question
```

## 1 · `/ux-frame` — Frame health

> Show me the Frame for **<area>**: the claims we hold, the confidence on
> each, what they rest on, and what has gone stale. Rank by what a current
> decision depends on. End with the three things most worth re-checking.

Loads `user-context` for the inventory, `frame-maintenance` when anything
looks stale or they asked what to retire.

## 2 · `/ux-context` — What do we know

> What do we know about **<area / cohort / flow / surface>**? Sweep Dovetail,
> PostHog (replay included), Outset, Pendo and support tickets. Grade what you
> find — Verified, Indicative, Anecdotal — name the gaps, and say plainly
> what we cannot answer from what exists.

Loads `user-context`. If two or more sources disagree, hands to
`research-synthesis` rather than averaging them.

## 3 · `/ux-evidence` — Pressure-test a hypothesis

> Hypothesis: **<statement>**. What evidence supports it, what argues against
> it, and what has never been tested? Give me a confidence call and the
> cheapest thing that would change your mind.

Loads `user-context` in critique mode. `anti-sycophancy` if the framing itself
is the weak part.

## 4 · `/ux-personas` — Persona set and owner

> Walk me through the persona set, then tell me which persona owns
> **<problem>** — their jobs to be done, their workflow around this, and how
> confident each claim is. If the problem spans two personas, say which one it
> must satisfy first and why.

Loads `user-personas`. Then `brand-operator-ux-persona` or
`creator-affiliate-ux-persona` for the deeper lens.

## 5 · `/ux-intake` — Triage a request

> Research request: **<paste the ask>**. Run intake — what decision does this
> unlock, do we already know the answer, and if not, is this MICRO, SPRINT or
> DEEP, and who runs it? If we already know, say so and stop.

Loads `research-intake`. The "we already know" check goes through
`user-context` before any route is given.

## 6 · `/ux-study` — Design the study

> Routed request: **<paste or summarise>**. Design the study worth running:
> sub-questions, what would disconfirm it, sample and its diversity, the
> probes, go/no-go thresholds, and the 3-participant rigor pass before the
> rest launches.

Loads `research-planner`. Drafts only — nothing launches without a human yes.

## 7 · `/ux-measure` — Build the measure first

> Before we run anything on **<feature / flow>**: build the PostHog dashboard
> that will tell us whether this moved, draw the audience from real usage
> rather than a guess, and draft the instruments — interview guide, Pendo
> guide, screener — we'll actually need.

Loads `research-builder`. `pendo-guide-strategy` first if a Pendo guide is in
scope — strategy before anyone opens the builder.

## 8 · `/ux-prioritise` — Rank on evidence

> Options: **<list them>**. Rank these on what the evidence actually supports.
> For each: the claim it rests on, the confidence, the users it serves, and
> what we'd be guessing about. Say which one has the weakest evidence under
> the loudest advocacy.

Loads `user-context`. Not a roadmap tool — it ranks evidence, not effort.

## 9 · `/ux-pressure-test` — Poke holes

> Here is the framing: **<paste the one-pager / PRD / problem statement>**.
> Pressure-test it. Where is the evidence thin, where is a feature standing in
> for a goal, where is the marketplace only being read from one side, and what
> would a sceptical PM ask that this does not answer?

Loads `anti-sycophancy`. Pair with `user-context` to check specific claims.

## 10 · `/ux-spec` — One-pager and epic

> Research is confirmed: **<link or summary>**. Draft the one-pager — problem,
> who it hurts, the evidence, success measures — and the linked UX epic. Draft
> only; I'll confirm before anything is published to Confluence or Jira.

Loads `write-spec`. Publishes nothing without an explicit yes.

## 11 · `/ux-adoption` — Did it work

> We shipped **<thing>** on **<date>**. Read the baseline from the Frame,
> re-run the measure in PostHog, and tell me whether the research held. Write
> the outcome back as a claim — including if it didn't hold.

Loads `adoption-check`. The claim gets written either way; a miss is evidence.

## 12 · `/ux-critique` — Mocks vs spec

> Mocks: **<links>**. Spec: **<one-pager / epic / tickets>**. Build the
> coverage matrix — what the framing asked for versus what the mocks do — then
> critique the solution itself. Flag anything the spec needed and the design
> silently dropped.

Loads `ux-critique`. `accessibility-review` next if a prototype URL exists.

## 13 · `/ux-persona-check` — Synthetic pre-test

> Walk **<persona>** through **<prototype URL / flow / copy>** as a task.
> Where do they hesitate, what do they look for and not find, what do they do
> instead? Treat everything as a hypothesis to test with real people, never a
> finding.

Loads `persona-check`. Pre-test only — it never substitutes for recruiting.

## 14 · `/ux-test-plan` — Plan the test

> Prototype: **<URL>**. Success criteria: **<from the one-pager>**. Draft the
> usability study — tasks, what each one is actually measuring, the script,
> and who we need in the room. Run the synthetic pre-test and the
> accessibility pass before we recruit anyone.

Loads `test-plan`, which pulls in `persona-check` and `accessibility-review`.

## 15 · `/ux-data` — Quantitative question

> Question: **<funnel / drop-off / trend / cohort>**. Run it in PostHog or
> Pendo, show me the numbers, and say what they can and cannot support. Flag
> instrumentation that would make the answer trustworthy if it is not already.

Loads `data-analyze`. `research-builder` if the event does not exist yet.

## House rules for every prompt

- Fill the `<placeholders>` from what the designer already said. Ask only for
  what is genuinely missing, and ask once.
- Verified vs AI interpretation, labelled, every time.
- Drafts stop at the human gate. Nothing publishes, launches or recruits.
- If a connector the prompt needs is not authorised, say which, say what the
  answer loses, and run the rest.
