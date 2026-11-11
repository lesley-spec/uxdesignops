# Templates

Three replies and a ticket. Keep the requester's own words for their question —
do not hand their problem back to them in research vocabulary.

Every reply gives them something: an answer, a reframe, or the one thing needed
to move forward. **A reply with no path forward is how people learn to route
around intake.**

---

## Already answered

> Good news — we've already got this.
>
> **[finding]** — [source, N] · [link]
> Last looked at [date].
>
> That covers [segment]. It doesn't cover [gap] — if your decision turns on that,
> tell me and it's a much smaller piece of work than the original ask.

## No decision behind it

> Before I scope this — if the answer comes back the opposite of what you expect,
> what changes?
>
> I ask because research with no decision waiting on it tends to become a document
> nobody reads, and I'd rather spend the time on something you'll use.
>
> If the call is already made, I can pressure-test it instead — that's often more
> useful anyway.

## It's a design decision

> As written this is a design call rather than a question about users — the answer
> wouldn't change what we build, it *is* what we build.
>
> There's a research question underneath it though: **[reframe]**. That one I can
> route.
>
> Want me to pick that up, or would you rather take this to design review? Happy
> to come either way.

## Timeline doesn't fit

> Straight answer: this needs [mode, duration] and you need it by [date].
>
> Three options —
> 1. Move the date to [date] and we do it properly
> 2. Narrow to [narrower question], which [faster mode] answers honestly
> 3. A quick directional read now, labelled as not decision-grade
>
> Any of those works. Option 3 is a real choice, it just has to be a choice we
> both made on purpose.

## We can't measure it yet

> Your question is a good one, and we can't answer it honestly right now —
> [what's missing] isn't measured, so any study would be me asking people to
> recall something we could just observe.
>
> What I'd do: [instrumentation ask] first, then a short study once there's a
> fortnight of data. That's [timeframe] rather than [original], and the answer
> would actually hold.
>
> If the decision can't wait, I can give you a directional read from [what we do
> have] — labelled as directional, because that's what it'd be.

---

## Ticket

**Destination:** project `UX`, [board 679](https://impact.atlassian.net/jira/software/projects/UX/boards/679).
Default assignee **Nihal Somers** — resolve the account with
`lookupJiraAccountId` rather than hardcoding an ID, so a change of owner doesn't
silently break ticket creation.

**Type** — the method decides, not the mode. A MICRO can be either:

| The question is answered by… | Type |
|---|---|
| Product behaviour — funnels, usage, Pendo, PostHog | **Analytics** |
| People — interviews, usability testing, surveys | **Research** |
| Both | **Research**, with the analytics piece named in the scope |

**Instrument-first tickets are the exception.** They are instrumentation work for
the squad that owns the surface, not UX research — raise those on the squad's
board and link them from the UX ticket, which stays open until the data lands.

No custom fields — prose is fine until there are enough tickets to want
otherwise.

**Title:** `Research: [topic]`. A ticket from a meeting also gets a source line under the title: meeting, date, and who was there.

```markdown
h2. Question
[what they want to know]
*Asked by:* [name] · *Decides:* [name]

h2. Decision
[what changes based on the answer]
*Needed by:* [date] · *Must hold until:* [date or "stable"]

h2. What we already know
*Verdict:* Solid | Thin | Nothing
[finding — source, N, link]
*Not covered:* [gap]

h2. Route
*[MICRO | SPRINT | DEEP | INSTRUMENT FIRST]* — [why, one line]
*Run by:* [research | name, with support on method / guide / analysis]
*Timing:* [fits | they chose option N]

h2. Scope
*Question:* …
*Sub-questions:* … (SPRINT/DEEP)
*Who:* [segment, who is in and out, sample size if discussed]
*Method:* …
```

Two labels are worth setting, because they make "what did we route this quarter"
answerable without opening tickets: `research-micro|sprint|deep` and
`team-led|research-led`.
