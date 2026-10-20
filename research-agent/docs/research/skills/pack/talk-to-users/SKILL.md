---
name: talk-to-users
description: >-
  The Ideate-stage way in to the people you are designing for. Frames what you
  actually want to know, then points you at the right place. The persona set to
  talk to, the Frame for what the evidence says, or a real study when neither
  will do. It generates no personas of its own. Use when someone says I want to
  talk to users, what would a partner think, run this past someone, or who am I
  designing this for.
license: Proprietary
metadata:
  stage: ideate
  pipeline: impact-ux-designops
  author: impact.com-ux
  generates: nothing
---

# Talk to users

In Ideate you want a user in the room. This gets you to one, or tells you
straight that we do not have one for this question.

**It generates nothing.** There is one persona voice at impact.com, in
[`user-personas`](../user-personas/), and one body of evidence, in
[`user-context`](../user-context/). A second place to produce a user-shaped
answer would become the place people go when they want a friendlier one.

**Answer short.** Lead with what changes, not with everything you found. A few
lines, then one specific follow-up they can ask for — the detail stays
available, it just doesn't arrive unasked. A number earns its place by changing
a decision; the rest belongs in the artifact, where someone can go and find it.

## Four ways in, and they answer different questions

| You want | Go to | You get |
|---|---|---|
| To hear how someone talks about this | [`user-personas`](../user-personas/), the Ask panel | Persona voice, grounded in the research behind that card |
| To know what the evidence says | [`user-context`](../user-context/) `ask` | Claims with confidence, n, and the gaps named |
| To walk a design through someone | [`persona-check`](../persona-check/) | Where a persona gets stuck, as a task walkthrough |
| To actually ask real people | [`research-intake`](../research-intake/) | A route, and often the answer is that we already know |

Most Ideate questions want the second. People ask for the first because it feels
closer to a user, and the evidence is usually both closer and stronger.

## The question to ask first

> **What would you do differently depending on the answer?**

In Ideate the honest answer is often "nothing yet, I am just exploring". That is
fine. It only changes where you go. Exploring wants the persona voice and the
claims, not a study. Save `research-intake` for when the answer would change
something.

## Routing

**"What would a Scaling Up creator think of this?"**
→ `user-personas`. Their cards answer from the evidence behind them and decline
when a question falls outside it.

**"Do partners actually struggle with X?"**
→ `user-context` `ask`. This is an evidence question wearing a persona's
clothes, and the Frame answers it better.

**"Here's a flow. Where does it break?"**
→ `persona-check` for where someone gets stuck, `user-context` `critique` for
what the evidence predicts. Both, if it matters.

**"We've never researched this group."**
→ `research-intake`. Say plainly that the persona set does not cover them, and
that anything a simulation says about them would be invention.

## When a persona card refuses

`user-personas` declines questions outside its research. **That is the system
working.** It means you have found an area where we have a persona and no
evidence.

Do not route around it by asking a different persona, or by rephrasing until
something answers. Record it as a gap in [`user-context`](../user-context/).
A refusal nobody writes down gets rediscovered next quarter.

## What you may not do with what comes back

Persona voice is **never evidence**. It generates hypotheses worth testing.

- Never write *"users said"* about something a persona card said
- Never put persona voice in a one-pager as a finding
- Never let it settle an argument. If two people disagree about users, that is a
  research question, and a made up voice will take a side with total confidence

What it is genuinely good for: finding the question you should be asking, before
you spend a session finding it the expensive way.

## If you want a persona we do not have

Say so, and treat it as a gap rather than a gap to fill with a generated card.

There is no affiliate persona, for instance, because the screener left them out.
That gap is written down rather than hidden. A generated stand-in would be quoted
within a week and would not survive contact with a real affiliate.

The route is [`research-intake`](../research-intake/): a new persona is DEEP
research, because a persona built from nothing is the most expensive kind of
wrong.
