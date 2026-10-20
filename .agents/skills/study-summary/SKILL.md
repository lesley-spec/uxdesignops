---
name: study-summary
description: >-
  Takes a pile of raw material, transcripts, PDFs, CSV exports, survey dumps,
  PostHog numbers, and works out what we currently know about a topic. Leads
  with what people said. Honest about what the material cannot tell you. Use
  when someone says here are the files, what do we know, make sense of this, or
  summarise where we are on this.
license: Proprietary
metadata:
  stage: empathize
  pipeline: impact-ux-designops
  author: impact.com-ux
  input: raw-material
---

# Study summary

Someone hands you a folder. Transcripts, a CSV, a PDF deck from last year, a
PostHog export. The question is always the same: what do we actually know here?

This reads all of it and says so, in plain words, with the gaps left visible.

**Answer short.** Lead with what changes, not with everything you found. A few
lines, then one specific follow-up they can ask for — the detail stays
available, it just doesn't arrive unasked. A number earns its place by changing
a decision; the rest belongs in the artifact, where someone can go and find it.

## How to write

Open with what people said and how they felt. Quote them. The counts come after,
to show how widespread something was.

Keep it short. A summary that runs longer than the attention someone has for it
has failed, however thorough it is.

Say what the material cannot tell you. That is not a disclaimer at the end, it
is part of the answer.

Never fill a gap with a plausible sentence. If three files disagree, say they
disagree.

## What you can take in

| Type | Read it for |
|---|---|
| Interview transcripts | What people said, in their words. The best material you will get |
| Survey or CSV exports | How common something is. Check the open text, not just the counts |
| PDF decks and docs | What someone already concluded, and when |
| PostHog | Whether behaviour matches what people told you |
| Support tickets | What breaks often enough that people complain |

Ask for what is missing before you start. If there are no transcripts, say the
summary will be thin on why, because nothing in the rest of the pile answers it.

## Working through it

### 1. Sort by age and type

List what you have, with dates. Anything over a year old gets read as history,
not as current state, and you should say so when you quote it.

A deck from last year that disagrees with interviews from last month is not a
contradiction. It is a change, and that is worth more than either file alone.

### 2. Read the words first

Transcripts and open text before numbers. Note what people say, where their tone
shifts, what they do instead when something does not work, and anything that
surprised you.

Pull quotes as you go, with who said it and roughly when. A summary without
verbatim reads like someone else's opinion.

### 3. Then the numbers

Use quant to say how common, never to say why. Check that an event or question
means what you think before you lean on it.

If a number cannot be checked, leave it out or mark it clearly as unverified.

### 4. Find what disagrees

Deliberately look for the file that cuts against the emerging story. If you did
not find one, say where you looked.

Two sources agreeing is worth more than one source with a big sample. Say which
you have.

### 5. Write it

```markdown
# What we know about [topic]
Based on [what you read] · [dates] · written [date]

## The short version
[Four or five lines. What people experience and how they feel about it.]

## What people told us
**[Finding in plain words]**
> "[quote]" [who, when]
[How common. What cuts against it.]

## What the behaviour shows
[Only where it adds something. Skip this if there is nothing solid.]

## What we don't know
[The honest list. Who we didn't hear from, what the material can't answer,
where two sources disagree and nobody has settled it.]

## How much to trust this
[One or two lines. Thin, mixed, or solid, and why.]
```

The "what we don't know" section is the one that makes the rest usable. Without
it a reader assumes you covered everything.

## Being honest about thin material

Say it plainly at the top when it applies.

- "This is six interviews from one segment. It tells you about them and nothing
  about brands."
- "The only recent material here is a survey. We have numbers and almost no
  explanation."
- "Two of these files disagree and nobody has reconciled them. I have kept both."

That is more useful than a confident summary that falls apart when someone
checks a source.

## When you are done

Offer to record what you found through [`user-context`](../user-context/) so the
next person asking finds it, and point anything genuinely unanswered at
[`research-intake`](../research-intake/).

If the pile turned out to answer the question already, say so clearly. That is a
good outcome and it saves a study.
