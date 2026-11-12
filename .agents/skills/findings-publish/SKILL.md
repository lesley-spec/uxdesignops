---
name: findings-publish
description: >-
  Takes a finished study and turns it into the things people actually read. It
  pulls together what Outset, Pendo and PostHog hold, writes a Dovetail data
  entry with a TL;DR, persona, jobs to be done, current workflow, friction and key
  quotes, drafts a short Slack post, puts a page wherever you point it in
  Confluence, and suggests Jira tickets worth raising. Use when someone says write this up, publish the findings, share what
  we learned, or loop this back to the squad.
license: Proprietary
metadata:
  stage: test
  pipeline: impact-ux-designops
  author: impact.com-ux
  supersedes: test-loopback, dovetail-report
---

# Findings publish

A study has finished. This turns it into four things: a data entry in Dovetail, a
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

## 1. The Dovetail data entry

One data entry per participant or account, or one per study when the evidence is
pooled. Dovetail holds research material as data entries, not documents, so this
is not a doc.

The shape follows the Backcountry entry in Dovetail
(https://impact.dovetail.com/data/6Abp2MM39JJuG0PvrSdV8E). Keep the section order
and the formatting. The topics change with the study: rename the topic-specific
sections (the example's "Stance on AI" becomes whatever the study is testing).
Drop a section only when the session has nothing on it, and then write "Not
discussed in this session" rather than leaving it out quietly.

### Header

Title: `<Account or participant> - <Segment or study topic>`, for example
`Backcountry - Strategic Growth Brand`.

Under the title, one metadata line: account ID, brand size, partner count and the
participant's role. Then the link to the Dovetail entry, and the recording link if
there is one.

Then one line: `AI-written summary. Quotes are verbatim from the transcript;
everything else is interpretation.`

### TL;DR

Heading `TL;DR: <Name> (<segment>)`, then four or five bullets, each with a bold
label. Two sentences at most per bullet:

- **The User:** who they are, what they are responsible for, the scale they manage.
- **Current Workflow:** how they do the job today.
- **Current Friction:** the two or three biggest pain points, worst first.
- **Stance on <topic>:** their position, and the condition they attach to it.

Someone should be able to read only this and not be misled.

### User persona

- **Persona type:** their role, in one line.
- **<Topic> appetite:** one line.
- **Core goals:** three or four bullets, in the participant's own terms.
- **Primary jobs to be done:** three or four bullets, each as "verb + outcome".

### Current workflow

One subsection per stage, in the order they do the job (two to four stages). Each
opens with a bold lead-in on the key point, then the detail. Keep quotes light
here; they sit in Key quotes.

### Current friction

One bullet per friction point, worst first. Each names the moment it happens and
the cost: time, trust, money or the brand. If something in the session contradicts
a friction point, say so in the same bullet.

### Stance on <topic>

One or two bullets: the position, the condition attached to it, and the main
concern.

### Key quotes

Three blockquotes at most, each tied to a point above. Verbatim only. Then the
link: `[Click to see in Dovetail](<entry link>)`.

#### Transcript

The full transcript with speaker labels and timestamps, copied from the source, not
condensed or cleaned up. Check the participant's consent to share the transcript
before including it, and leave it out if they have not agreed.

### Rules for the entry

- Quotes are verbatim. Never paraphrase inside quotation marks, and never invent a
  quote, a participant or a number.
- Every claim traces to something said in this session. If the session does not
  cover it, say so.
- Write the body as HTML, not Markdown. `create_data` takes plain text or HTML:
  `h2`/`h3` for headings, `ul`/`li` for bullets, `blockquote` for quotes, `strong`
  for bold labels. Never write it as a Dovetail doc.
- Show the full draft in chat and wait for a yes. Then `create_data` into the
  project the evidence sits in, with the title above.

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

The page carries the findings plus the bits Dovetail does not hold well: who
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
