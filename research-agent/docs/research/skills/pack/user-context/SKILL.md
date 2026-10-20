---
name: user-context
description: >-
  What impact.com knows about its users, and how confident it is. Ask a question
  about any user, surface, workflow, cohort or hypothesis and it sweeps Dovetail,
  PostHog (including session replay), Outset, Pendo and support tickets, grades
  what it finds, and names the gaps — then pressure-tests a design or a roadmap
  call against that evidence. Also records new findings back into the Frame. Use
  for "what do we know about X", "has this been researched", "is this hypothesis
  supported", "where are our blindspots", "what does the evidence say about this
  mock", "which of these should we build first", or to log a finding.
license: Proprietary
metadata:
  stage: empathize
  pipeline: impact-ux-designops
  author: impact.com-ux
  modes: ask|critique|decide|record|review
  requires-connectors: dovetail, posthog
---

# User context — the Frame

The Frame is **what we currently believe about our users, how confident we are in
each belief, and where the gaps are.** Not what we have studied — what we know.

That distinction is the whole design. A research repository stores past projects.
The Frame stores *claims*: deduplicated, dated, graded, and queryable. Narrative
is thrown away; the facts are kept.

This skill reads the Frame, and writes to it.

> Constantine Papas, *AI-Powered UX Research* — the Frame. Claims-pool structure
> after Kelly's model (Outliers Insights keynote).

## Not fenced by personas

Ask about **anything**: a persona, a surface, a workflow, a cohort, a support
pattern, a hypothesis. Persona is one way to slice the Frame, not the door into
it. "What do we know about payout failures" is a valid question with no persona
attached, and the answer should not begin by making you pick one.

**Personas live in [`user-personas`](../user-personas/).** This skill references
that set and never restates it. If you need who-they-are, go there; if you need
what-we-know, you are in the right place.

## Modes

| | Mode | For |
|---|---|---|
| **1** | `ask` | What do we know about X? Sweep, grade, name the gaps |
| **2** | `critique` | What does the evidence predict about this mock, flow or copy? |
| **3** | `decide` | Which of these should we build, and what does the evidence support? |
| **4** | `record` | Write a new finding into the Frame |
| **5** | `review` | Quarterly maintenance — what changed, what's stale, what's next |

Modes 1–3 **read** the Frame. Modes 4–5 **maintain** it. Always name the mode you
are in.

**Talking to a persona is not here.** That lives in
[`user-personas`](../user-personas/), whose cards answer from the evidence behind
them and decline when a question falls outside it. One persona voice, one owner,
one update path — a second one would become the place people go when they want a
friendlier answer.

## Where to start

People rarely arrive with a well-formed question. **Route what they said to a
mode, sharpen it, and say the sharper version back** before running anything.

| They say | Mode | Ask back |
|---|---|---|
| "What do we know about X?" | `ask` | Which slice — a segment, a surface, a workflow? And what decision does this unlock? |
| "Has anyone researched this?" | `ask` | What would count as an answer? A near-match narrows the study rather than ending it |
| "Is it true that…?" | `ask` | Restate as a falsifiable claim, then write what would kill it before searching |
| "Here's a mock / flow / bit of copy" | `critique` | What is it meant to do, for whom? Critique needs the job, not just the pixels |
| "Should we build A or B?" | `decide` | What decision, by when, and what happens if we get it wrong? |
| "Which of these matters most?" | `decide` | Ranked for whom — which segment is this for? |
| "We just learned X" | `record` | One falsifiable sentence, its n, its source, and what it does *not* cover |
| "Can the Frame still be trusted?" | `review` | That is [`frame-maintenance`](../frame-maintenance/) — hand it over |

**Three questions that are not for this skill**, and should be handed on rather
than answered:

- *"What would persona X say?"* → [`user-personas`](../user-personas/)
- *"Should we research this at all?"* → [`research-intake`](../research-intake/)
- *"Did it work after we shipped?"* → [`adoption-check`](../adoption-check/)

### Openers worth offering

When someone has no question yet, offer these rather than a blank prompt. Each
one lands somewhere real, and the answer teaches what the Frame can do:

- **What is contested?** The claims two readings disagree on — usually figures
  still circulating in decks
- **Where are we blind?** The empty coverage cells, and which has a live decision
  behind it
- **Which blocking needs rest on the weakest evidence?** High severity, low
  evidence: a research job, not a design job
- **What can we actually decide on today?** What HIGH confidence supports, and
  what is still blocked
- **What do we know about [domain]?** The densest domain is the easiest place to
  see the Frame working

The Frame page carries the same openers as buttons, generated from its current
state, so the two stay in step.

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

1. **Never fabricate.** If the sweep found nothing, say **"data not available."**
   A plausible answer with no source behind it is the one failure that looks
   identical to success.
2. **Label every line** — **Verified** (source + link + N), **Inferred**
   (reasoning from verified evidence), or **Persona voice** (what a persona
   simulation said). Persona voice is never evidence; it generates hypotheses.
3. **Confidence travels with the claim.** Never a bare statement — always
   `[claim] + [confidence] + [n] + [evidence link]`.
4. **Bound your language to your sample.** At n=8 you cannot say "90% of users."
   You can say "most" or "roughly half." Precision you did not measure is a lie
   with a decimal point.
5. **Answer from evidence, not from a voice.** Persona questions go to
   `user-personas`. This skill says what the claims support.
6. **Carry the disconfirming evidence.** Every finding states what contradicts
   it, or states that you looked and found nothing.
7. **Separate frequency from importance.** Eight of eight mentioning something is
   not the same as it blocking anyone's work.

Full rules, confidence definitions and AI safeguards:
[references/evidence.md](references/evidence.md).

## Sources

| Source | Answers |
|---|---|
| **Dovetail** | What have people told us? Interviews, highlights, past projects |
| **PostHog** | What do people actually do? Events, funnels, retention |
| **PostHog session replay** | What does it *look like* when they do it? |
| **Outset** | What studies have run — or are running right now? |
| **Pendo** | Guides, polls, in-product surveys |
| **Support tickets** | What is actually breaking, in volume |

Session replay and support tickets are the two that catch what interviews miss:
replay shows the gap between what people say they do and what they do, and
ticket clusters show friction nobody thought to report in a study.

Preflight, sweep order and query recipes: [references/sources.md](references/sources.md).

## Mode 1 — ask

The core loop. Full protocol: [references/audit.md](references/audit.md).

1. **Make it falsifiable.** Restate as a claim with a subject, a behaviour and a
   direction. Write what would confirm it and what would kill it *before*
   searching. No killer means it is not a hypothesis yet.
2. **Scope it.** Which slice of the Frame — segment, surface, workflow, cohort?
   Name what is explicitly *out* of scope.
3. **Check the claims pool first.** Existing claims are free. See
   [references/frame.md](references/frame.md).
4. **Sweep** what the pool does not cover, in the order in
   [references/sources.md](references/sources.md).
5. **Hunt counter-evidence.** Deliberately look for the disconfirming case.
   "None found" is reportable — but you must have looked.
6. **Grade and gap.** Every claim HIGH / MEDIUM / LOW / UNVALIDATED. Every gap
   gets a type and the cheapest way to close it.

### Output

```markdown
# Context — [topic]
Mode: ask · Date: [YYYY-MM-DD] · Scope: [segment / surface / cohort]
Sources: Dovetail [✅] · PostHog [✅] · Replay [✅] · Outset [✅] · Pendo [—] · Support [✅]

## Question (falsifiable)
**Claim:** [subject] + [behaviour] + [direction]
**Would confirm:** … · **Would kill:** …

## Verdict
[Supported | Partly | Not supported | Unknown — cannot answer yet]
Best confidence: [HIGH|MEDIUM|LOW|UNVALIDATED]

## What we know
| Claim | Confidence | n | Source | Link |
|---|---|---|---|---|

## Frequency vs importance
| Finding | Mentioned by | Actually blocking |
|---|---|---|

## What contradicts it
- … (or: "searched [scopes], none found")

## Gaps
| Gap | Type | Why it matters | Cheapest close |
|---|---|---|---|

## Settled — do not re-research
- … (with links)

## Who this affects
[from user-personas, when a persona slice applies — otherwise say "not
persona-scoped"]
```

**Decision thresholds.** Say out loud what the confidence supports. Building a
feature needs HIGH plus corroboration; deprioritising can run on MEDIUM; a
strategic pivot needs HIGH and a sustained pattern. See
[references/evidence.md](references/evidence.md#what-confidence-justifies-what-decision).

## Modes 2–3 — critique, decide

Both answer **from the claims**, never from a simulated voice. Run `ask` first, or
re-read a dated brief — neither mode is useful ungrounded.

**`critique`** takes a mock, flow or copy and says what the evidence predicts:
where it collides with observed behaviour, which assumption it rests on and how
well that assumption is evidenced, and what it does not address at all. This is
the thing a persona simulation cannot do, because the claims pool is here and the
simulation only has a character.

**`decide`** weighs options against what the evidence actually supports, using
the thresholds in [references/evidence.md](references/evidence.md#what-confidence-justifies-what-decision)
— and names what is still blocked rather than ranking everything regardless.

### When a persona card refuses

`user-personas` declines questions that fall outside its research. **That refusal
is a finding**: an area where we have a persona but no evidence.

Capture it as a gap and, if it recurs, a 🔴 cell on the coverage matrix. The
persona set already treats a refusal as a research gap rather than a failure;
nothing currently writes it down, and a gap nobody records gets rediscovered next
quarter.

## Mode 4 — record

New finding, new claim. **Research that does not write back does not compound.**

**A claim is proposed here, confirmed by a person.** Show the claim, its
confidence and its denominator, and get a yes before writing. A Frame full of
weak claims is worse than no Frame, because it lends the authority of the record
to a guess — and the curation is the part that makes the whole thing worth
having. The sweep proposes; a researcher sets or confirms confidence.

**Every claim carries an owner** — the person who will be asked about it at the
next review. A claim with no name on it is retired at the first
`frame-maintenance` pass, so write one in now.

Write with the `ArtifactData` tool against the Frame:

> **https://claude.ai/artifact/FHc7oAPoyohgxo87VdxCGw**

- One **claim** per finding, into `claims`, with its denominator, source and owner
- A **need** into `needs` when the finding names something people lack, linked to
  the claim ids that evidence it
- Use `batch` for more than a couple of writes
- The page holds no data, so **writing a claim is not republishing the page**

Also refresh `verified` when a sweep confirms an existing claim still holds —
someone checked it today and it held, and not recording that ages a good claim
into a staleness flag for nothing. Pin every write to an existing document with
the `version` you last read.

Field shapes, dedup and contradiction handling:
[references/frame.md](references/frame.md).

## Mode 5 — review

Quarterly, and it is load-bearing — skip it and the Frame degrades silently while
still looking authoritative.

- What did we learn this cycle that **updates** what we believed?
- What did we find that we still **cannot explain**?
- What would we **do differently**?
- Coverage matrix — where are the **blindspots**?
- What used to be true and **isn't any more**? Retire it.

Ritual, coverage matrix and decay tracking:
[references/frame.md](references/frame.md#maintenance).

## References

- [references/frame.md](references/frame.md) — the Frame: claims pool, coverage
  matrix, belief map, maintenance ritual
- [references/evidence.md](references/evidence.md) — confidence standard,
  decision thresholds, AI safeguards, evidence governance
- [references/sources.md](references/sources.md) — the six sources, preflight,
  sweep order, query recipes
- [references/audit.md](references/audit.md) — the `ask` protocol in full
- [`user-personas`](../user-personas/) — who our users are. Not duplicated here.
