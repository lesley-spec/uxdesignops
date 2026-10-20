---
name: findings-publish
description: >-
  Takes a finished study and turns it into the things people actually read. It
  pulls together what Outset, Pendo and PostHog hold, writes a Dovetail report
  with a TL;DR, key insights and deep dives, drafts a short Slack post, puts a
  page wherever you point it in Confluence, and suggests Jira tickets worth
  raising. Use when someone says write this up, publish the findings, share what
  we learned, or loop this back to the squad.
license: Proprietary
metadata:
  stage: test
  pipeline: impact-ux-designops
  author: impact.com-ux
  supersedes: test-loopback, dovetail-report
---

# Findings publish

A study has finished. This turns it into four things: a report in Dovetail, a
short post for Slack, a Confluence page where you want it, and a list of tickets
worth raising.

It drafts all four and creates nothing until you say so.

> Replaces `test-loopback` in the DesignOps pack and the old `dovetail-report`
> skill. Retire both rather than running them alongside this.

**Answer short.** Lead with what changes, not with everything you found. A few
lines, then one specific follow-up they can ask for — the detail stays
available, it just doesn't arrive unasked. A number earns its place by changing
a decision; the rest belongs in the artifact, where someone can go and find it.

## How to write

Lead with what people said and how they felt about it. The numbers come after,
to show how common something was, not to open with.

Plain words. Short sentences. If a sentence needs a second read, cut it in half.

Say what you do not know. A report that admits its gaps gets trusted. One that
papers over them gets quoted once and then quietly doubted.

Never invent a quote, a number or a participant. If you cannot find something,
say you could not find it.

## What to gather

| Where | What you are after |
|---|---|
| **Outset** | The interviews. Transcripts, topline, the things people actually said |
| **Dovetail** | Earlier work on this. Highlights someone already marked |
| **Pendo** | In-product responses. Bigger samples, thinner answers |
| **PostHog** | Whether the behaviour matches what people told you |
| **The Frame** | What we already believed, so you can say whether it held |

Start with the interviews. The quant tells you how often, never why, and a
report built from numbers first reads like a dashboard with sentences.

**Say what you could not get to.** If Pendo was empty or PostHog had no event
for this, that belongs in the report, not left out quietly.

## 1. The Dovetail report

Three layers, in this order.

### TL;DR

Five or six lines. What we asked, what we found, what it means for the decision.
Someone should be able to read only this and not be misled.

### Key insights

Three to five. Any more and nothing stands out.

Each one opens with the finding in plain words, then a quote that shows it, then
how common it was and what contradicts it.

```
**Partners give up on the assets page rather than ask for help.**

> "I just gave up and emailed my contact. Took two days but at least
>  I knew it'd get done." P7

Six of eleven did something similar. Two found it first time and were
surprised anyone struggled, both of them daily users.
```

The disconfirming line is not optional. If you looked and found nothing against
it, say that instead.

### Deep dives

One section per insight for people who want the detail. Transcript quotes with
timestamps, the behavioural read if there is one, what you are still unsure
about.

This is where numbers belong. Keep them out of the top two layers unless the
number is the finding.

Write it with `create_doc` into the project the evidence sits in, after you have
shown the draft.

## 2. The Slack post

Short, business casual, no jargon. Under 150 words.

```
We spent two weeks with partners on the assets page.

Short version: most people can't find it, and they don't ask. They work
around it or email their contact instead.

A few things stood out:
• Six of eleven gave up before finding what they came for
• The two who managed it were daily users who'd learned where things live
• Nobody we spoke to had used search

Worth saying: small group, eleven people, all partners. We didn't talk to
anyone on the brand side.

Full write-up: [link]
```

Say the sample size and who you did not speak to. That one line is the
difference between a post people trust and one that gets over-read.

Nothing at low confidence goes in here. In a channel it gets screenshotted
without the caveat.

## 3. The Confluence page

**Ask where it goes.** Do not guess at a space. If the person has not said,
ask, and offer what `getConfluenceSpaces` returns.

The page carries the report plus the bits Dovetail does not hold well: who
decided what, what happens next, and which beliefs this changed.

## 4. Jira tickets

Suggest them. Do not raise them without a yes.

Most findings are not tickets. A finding becomes one when someone has decided to
do something about it.

| Finding | Ticket? |
|---|---|
| Blocks people, and the owner agreed to fix it | Yes |
| We cannot measure something we need to measure | Yes, to whoever owns that surface |
| Real, but nobody has decided anything | No. Leave it in the report |
| Thin evidence | No. Suggest more research instead |
| Two readings disagree | No. Settle it first |

A backlog full of tickets nobody asked for teaches a squad to ignore research.

Each suggestion says what would change, who agreed, and what the evidence was.

## Before you create anything

Show all four drafts together. Say which findings you deliberately left out of
the Slack post and which you chose not to ticket. That second list is usually
the one worth arguing about.

## After

Close the original request, link everything together, and record what you
learned in the Frame through [`user-context`](../user-context/).

If the study was testing something we already believed, say plainly whether it
held up, got narrower, or turned out wrong. If anything shipped, hand it to
[`adoption-check`](../adoption-check/) so someone looks again in a month.
