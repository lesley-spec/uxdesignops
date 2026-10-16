# Evidence governance

The quality bar for what gets into the Frame, and what decisions it can carry.

This is partnership, not policing. When someone says *"admins need SAML"*, the
response is not "prove it" — it is **"where did that come from?"**, "how many
said it?", "did it come up unprompted?", "any admins who don't need it?", and
then, together, "what confidence are we assigning?"

---

## Confidence levels

Defined, not felt. The same words must mean the same thing to everyone.

| | Bar |
|---|---|
| **HIGH** | Multiple independent sources agree — qual + quant + support or behaviour · n≥8 consistent · under 6 months old · owned and reviewed |
| **MEDIUM** | Single primary source, qual **or** quant · n=4–7, mostly consistent · 6–12 months · owner assigned, refresh planned |
| **LOW** | Single anecdotal mention, or sources conflict · n<4, or one narrow segment · 12+ months, or a fast-moving topic |
| **UNVALIDATED** | Hypothesis, leadership belief, or one person's assertion. **Not in the Frame** until backed |

UNVALIDATED is a real and useful state. "Leadership believes X" is worth writing
down — as a hypothesis to test, never as a claim to build on.

## What confidence justifies what decision

| Decision | Needs |
|---|---|
| **Build a feature** | HIGH **plus** corroboration (quant + qual + support trend). Never LOW alone. If the Frame is unclear, research first — don't guess |
| **Deprioritise** | MEDIUM is enough. The bar for saying "not now" is lower than for saying "build" |
| **Strategic pivot** | HIGH **and** a sustained pattern. Never on MEDIUM |
| **Quick tactical change** | MEDIUM plus fast feedback. Try it and measure |

When someone cites the Frame to justify a big call, the question is:
**what confidence is this resting on, and is that enough?**

---

## Qual leads, behaviour backs it

**A claim says what we learned about people. A number says how much.** Write the
first and support it with the second — roughly four parts Dovetail to one part
PostHog, never the other way round.

| | |
|---|---|
| ❌ | "72,239 browsed the marketplace and 497 applied." |
| ✅ | "Partners browse the marketplace without applying — 72,239 browsed over 30 days and 497 started an application." |

Both carry the same figure. The second is a finding; the first is a measurement
waiting for someone to decide what it means — and whoever decides will not be
the person who read the research.

**Why this way round.** Behaviour tells you *what* happens and never *why*.
Dovetail holds the why. A Frame built the other way accumulates numbers nobody
can act on, and the interpretation gets invented later by whoever is in the room.

**A PostHog claim with nothing qual behind it is provisional.** Say what it is
consistent with, or say plainly that nothing explains it yet — that second one is
a research gap worth recording, not a reason to leave a number standing alone.

## How evidence is produced

Every claim entering the Frame must be:

| | |
|---|---|
| **Sourced** | Link to specific evidence — quote, timestamp, clip. Not "the research said" |
| **Disconfirmed** | Carries the contradicting evidence too, or states that you looked and found none |
| **Separated** | Frequency listed apart from importance |
| **Contexted** | When and where it was produced |
| **Bounded** | Explicit about sample — n, diversity, how recruited |

### Frequency is not importance

The most common synthesis error, and it inverts priorities.

| | Frequency | Importance |
|---|---|---|
| "8/8 mentioned bulk import" | HIGH | — |
| "…but 1 said it blocked their work" | — | LOW |
| "3/15 actively tried to do what the copilot does" | LOW | HIGH |

Ten people saying they'd *like* an AI copilot is weaker evidence than three
people building a workaround for its absence. Weight both, and show both.

### Disconfirming evidence

This is where research quietly lies — by omitting what didn't fit.

> **Finding:** admins need bulk import.
> **Against it:** 2 admins manage <10 users and say it's unnecessary; 1 prefers
> one-by-one to verify each person.
> **Honest claim:** most admins (6/8) want bulk import, though 2 managing small
> teams are content one-by-one.

Readers who can see you reporting against yourself believe the rest.

### Evidence trail

Every claim traces back far enough that a decision-maker can check it:

```
Claim: admins prefer bulk import                    [HIGH, n=8]
├─ P1 transcript 23:45 — "I'd batch import everyone at once"
├─ P3 transcript 18:12 — "copy/paste each person is painful"
├─ Support: 10+ tickets requesting it
├─ Observed: admin running an external script to generate imports
└─ Frequency 8/8 · Importance: blocking for 6
```

---

## AI safeguards

Most of this work runs through AI. These four exist because AI failure looks
exactly like AI success.

**1. Unavailable information is explicit.** Say **"data not available"** rather
than producing something plausible. QA by searching the output for phrases that
appear nowhere in the source.

**2. Generated text is labelled.** `[AI-GENERATED]` and `[HUMAN-EDITED]`, so a
decision-maker can see which is which.

**3. Confidence travels with every claim.** `[claim] + [confidence] + [n] +
[evidence link]`. A bare statement is not a finding.

**4. Probability is bounded by sample.** At n=8 you cannot say "90% of users."
You can say "most" or "roughly half". Precision you did not measure is a lie with
a decimal point — and it is the most persuasive kind.

---

## The three labels

Every line in any output carries one:

| Label | Means |
|---|---|
| **Verified** | Source + link + n. It happened, here's where |
| **Inferred** | Reasoning from verified evidence. Defensible, not observed |
| **Persona voice** | What a persona simulation said. **Never evidence** — generates hypotheses |

Never write "users said" about something a persona card said. This applies to
anything that speaks as a user, including the `user-personas` Ask panel — the
label travels with the output, not with the tool that produced it.

---

## Sample and population are different numbers

Keep these apart in every sentence:

- the **sample** that was researched
- the **cohort** being described
- the **daily actives** on the platform

Mixing them is the fastest way to lose a room, and the easiest mistake to make
when a claim is summarised a second time.
