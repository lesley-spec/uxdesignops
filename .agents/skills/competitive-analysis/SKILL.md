---
name: competitive-analysis
description: >-
  Looks at how the other platforms actually handle a job our users have to do,
  using Klue and the weekly competitor feed, and says what it means for us
  without pretending a competitor's feature is evidence our users want it. Use
  when someone says what does Partnerize do here, how do competitors handle
  this, are we behind on this, or check the competitor feed.
license: Proprietary
metadata:
  stage: empathize
  pipeline: impact-ux-designops
  author: impact.com-ux
  sources: klue, competitor-weekly-feed, g2, the-frame
---

# Competitive analysis

What do the other platforms do about the job our users are stuck on, and does
any of it matter to us?

Both halves are the work. The first half is research anyone can do. The second
half is the one that gets skipped, and skipping it is how a roadmap fills up
with other people's features.

**Answer short.** Lead with what changes, not with everything you found. A few
lines, then one specific follow-up they can ask for — the detail stays
available, it just doesn't arrive unasked. A number earns its place by changing
a decision; the rest belongs in the artifact, where someone can go and find it.

## The rule this exists for

**A competitor shipping something is not evidence our users want it.**

It is evidence that a team somewhere decided it was worth building. They may
have been right. They may have been copying someone else who was guessing.

So everything this produces starts as **UNVALIDATED**, whatever else it has
going for it. It becomes a claim when one of our users says the underlying
problem is real, and not before.

That is not caution for its own sake. Half of what a competitor ships gets
quietly removed within two years, and you cannot tell which half from the
outside.

## Where to look

### Klue, first

Klue is where the competitive intelligence lives: battlecards, win and loss
notes, pricing, positioning, and what sales is hearing in deals right now.

Start there rather than with a competitor's website, because Klue carries the
part a website never will, which is what happened when someone tried to sell
against them.

**Ask it for:** the battlecard on the competitor, anything recent on the area
you are looking at, and the win and loss notes that mention it. Win and loss
notes are the most useful thing in the building for this and the least read.

> If the Klue connector is not authorised in your session, say so and ask for it
> rather than working around it with web searches. A competitor's marketing site
> and Klue tell you different things, and the marketing site is the one that is
> trying to persuade you.

### The weekly competitor feed

> **https://lesley-spec.github.io/uxdesignops/v1/feed/**

Our own DesignOps site runs a competitor feed that refreshes every Monday, built
from the competitors' own changelogs and blogs plus a filtered news sweep. It
currently covers **Awin, CJ Affiliate, Rakuten Advertising, Partnerize,
ShareASale, Pepperjam and Refersion**.

Use it for *what shipped lately*, which is the question Klue answers least well.
You can filter it by features, news, or both, and by week.

**It is signed in, restricted to @impact.com Google accounts**, so an agent
cannot fetch it on your behalf. Open it yourself and paste in what matters, or
drive it in a browser you are signed into. Do not substitute a web search and
present it as the feed. If you could not get in, say so in the write-up.

If a competitor you care about is not on that list, that is a decision for
whoever runs the feed, not something to quietly work around.

### G2, and our own Frame

G2 carries what customers say about the others, which is closer to use than any
feature list. We already hold 158 brand reviews there.

And check [`user-context`](../user-context/) before you start. Sometimes we
already know what our users do about this, which turns a feature comparison
into a much sharper question.

## How to do it

### 1. Start from a job, not a feature list

> Not "compare reporting across platforms."
> Instead: "a brand manager needs to work out which partners are worth keeping.
> How does each platform let them do that, and where does ours make it harder?"

A feature-by-feature grid tells you who has more boxes ticked. A job tells you
who makes the work easier, which is the only question with an answer worth
acting on.

Take the job from the Frame if we have one. Our unmet needs are already written
this way.

### 2. Follow it the whole way through

Compare the journey, not the screen. Most of the difference between platforms
is in the handoffs: what you have to remember between steps, how many places
you go, what happens when something fails.

For each platform, for that job:

| | |
|---|---|
| **Can you do it at all?** | Fully, partly, with a workaround, or not |
| **How much work is it** | Steps, screens, places you have to go |
| **What they assume** | Who they think is doing this, and how often |
| **Anything genuinely different** | An approach nobody else took |

Note where you could not look. Most of these platforms do not let you in
without an account, so a lot of this is documentation, screenshots and what
Klue holds. **Say which it was.** "From their help docs" and "I used it" are
very different claims, and a reader deserves to know which one they are getting.

### 3. Sort what you find into four piles

| | Means | What to do |
|---|---|---|
| **Everyone has it** | Table stakes. Missing it is a reason we lose deals | Check against win and loss notes in Klue. If it shows up there, it is real |
| **Someone solved it better** | A genuinely nicer answer to a job our users have | Worth understanding. Not worth copying until a user says the problem is real |
| **Nobody does it** | Either an opening, or something everyone tried and dropped | Treat as an opening only if our evidence says the need exists |
| **We do it better** | Worth knowing, and worth telling sales | Hand to Klue rather than burying it in a research doc |

The third pile is where people get excited and where most bad roadmap items
come from. An empty space in a market usually got that way for a reason.

### 4. Say what it means for us, honestly

The only section anyone needs to read, and the one that takes the judgement.

For each finding, answer: **do our users have this problem?**

- **Yes, and we have evidence** → link the claim. Now it is a real gap, and
  the competitor is just confirmation
- **Yes, probably, but nothing written down** → this is a research question.
  Route it through [`research-intake`](../research-intake/), with the
  competitive finding as context rather than as the reason
- **No idea** → say that. It is the honest answer most of the time
- **No, our evidence says otherwise** → the most valuable line in the document.
  Write it down, because somebody will raise this feature again in six months

## The write-up

Keep it short. Nobody reads a long competitor document twice.

```markdown
# [The job], across the platforms
[date] · Klue [✅ / not reachable] · Feed [✅ / signed out] · G2 [✅] · Frame [✅]

## The short version
[Three or four lines. What the others do, and the one thing that actually
matters for us. Not a list.]

## The job
[Whose job, what they are trying to get done, and which of our claims or
unmet needs it maps to]

## How each one handles it
| Platform | Can you do it | How much work | Their angle | How I know |

## What it means for us
**Table stakes we're missing:** … [with the Klue win/loss note, if there is one]
**Someone's solved this better:** … [and whether our users have the problem]
**Nobody does this:** … [and whether that is an opening or a warning]
**We're ahead here:** … [send to Klue]

## What our own evidence says
[For each finding: do our users actually have this problem? Claim ids and
confidence, or "nothing written down", honestly]

## What this can't tell you
[Which platforms you could not get into. What came from docs rather than use.
How old the feed entries were. Everything here is UNVALIDATED until a user
says the problem is real.]
```

## Keeping it from going stale

A competitive analysis is true of the week it was written. It does not get
re-verified like a claim does, because the thing it describes keeps moving.

**Put a date on it and let it expire.** Six months old is a historical
document, not a current one. The Monday feed is the thing that stays current;
this is a snapshot taken for a decision.

If a finding here turns into something we act on, it gets recorded as a claim
through [`user-context`](../user-context/) `record` with the user evidence
attached, not the competitor evidence. "Partnerize does this" is not a claim
about our users and never becomes one.

## What this is not

**Not a reason to build something.** It is context for a decision somebody else
makes on evidence about our own users.

**Not a feature parity checklist.** Chasing parity means your roadmap is set by
whoever ships fastest, and it is how products end up with everything and no
point of view.

**Not a review of their design quality.** If you want to know whether an
interface works, [`heuristic-evaluation`](../heuristic-evaluation/) does that,
and it works just as well on somebody else's product as on ours.
