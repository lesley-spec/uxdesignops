---
name: heuristic-evaluation
description: >-
  Expert review of a screen or flow against Nielsen's ten heuristics, with a
  severity rating on every issue and a recommendation attached. Share a Figma
  screenshot, a frame link, a staging URL or a written description. Use when you
  need problems found now and cannot wait to recruit anyone.
license: Proprietary
metadata:
  stage: prototype
  pipeline: impact-ux-designops
  author: impact.com-ux
  accepts: figma-screenshot, figma-link, url, written-flow
  output: markdown-file
---

# Heuristic evaluation

Walk an interface against ten well worn usability rules, write down what breaks,
rate how badly, and say what to do about it.

It is the fastest way to find the obvious problems. It needs nobody's calendar.

**It is an expert opinion, not a finding.** Nobody used this. Never write "users
struggled with" about anything this produced. The honest phrasing is "this looks
like it would trip people up, and here is why".

The label goes in the file, under the title, because the file outlives the
conversation.

**Answer short.** Lead with what changes, not with everything you found. A few
lines, then one specific follow-up they can ask for — the detail stays
available, it just doesn't arrive unasked. A number earns its place by changing
a decision; the rest belongs in the artifact, where someone can go and find it.

## Where it sits

| | |
|---|---|
| **This** | Does the interface break known usability rules? |
| [`persona-check`](../persona-check/) | Where does one specific person get stuck doing a task? |
| `ux-critique` | Does the design do what the one-pager asked for? |
| `accessibility-review` | Contrast, focus order, keyboard, screen readers |

This one and `persona-check` pair well. Run this first for the rule breaking,
then `persona-check` for the task breaking. They catch different things: this
finds the inconsistent button, the persona finds the moment someone gives up.

## How to write it

Plain words. "There's no way back from this screen" rather than "the flow lacks
a reversible exit affordance".

Say what someone would feel, not just what is wrong. An unlabelled error that
loses the form is not a consistency issue, it is the moment someone stops
trusting the product.

Keep it short. Eight real problems beat thirty padded ones, and a long list
means a designer fixes the three easiest.

## Back it with a quote wherever you can

This is the part that makes the difference here.

Before you write the list, pull what we already know about this area from
[`user-context`](../user-context/) and the Frame.

An issue that lines up with something a real person said is worth ten issues
that only an expert noticed. Put the quote right under the issue:

> **Nothing confirms the link saved.** (Visibility of system status, severity 3)
> A partner already told us this: "I clicked save like four times because
> nothing happened. Then I had four of them." [p07, Dovetail]

Mark the ones with nothing behind them as what they are. They may still be real.
They are just softer, and the reader deserves to know which is which.

## What you can give it

**A Figma screenshot.** Fine for one screen or state.

**A Figma frame link.** Better, because the real labels come through and labels
are where half of these problems live. If the connector is not authorised, say
so and ask for a screenshot rather than guessing at the copy.

**A staging or production URL.** Best, because you can try the error states,
which is where most severity 3 and 4 issues hide. Do not sign in with anyone's
real credentials, and do not submit anything live.

**A written description.** Works. You will miss anything that is only visible in
the layout.

If you were handed one screen and the issues are really about the flow, say so.
A single screen cannot tell you whether someone gets through.

## Running it

### 1. Say what you are reviewing and what you are not

Name the screens and the flows. Name what you could not reach: states behind a
paywall, error paths you could not trigger, anything you only saw as a static
image.

That list goes in the file. It is how a reader knows the difference between
"clean" and "not looked at".

### 2. Walk it three times

**As someone new.** First time here. No idea what the words mean. This pass
finds the jargon, the missing starting point and the unexplained default.

**As someone who does this every day.** Fourth time this week. This pass finds
the missing shortcut, the confirmation that got boring, the five clicks that
should be one.

**Through the actual tasks.** The real jobs people come here for. This pass
finds the broken handoffs between screens.

Three passes because each one makes different things visible. A new person never
notices the missing bulk action, and an expert stopped reading the empty state
months ago.

### 3. The ten heuristics

Use them as a checklist on each pass, not a structure for the report.

| | Ask |
|---|---|
| **Visibility of system status** | Do you know what just happened, and what is happening now? |
| **Speaks your language** | Are these our words or the database's words? |
| **A way out** | Can you undo, go back, or leave without losing work? |
| **Consistent** | Does the same thing look and behave the same everywhere? |
| **Stops mistakes** | Is it easy to do the wrong thing? |
| **Shows, not remembers** | Do you have to carry something in your head from the last screen? |
| **Fast for regulars** | Is there a quicker path once you know the way? |
| **Nothing spare** | Is anything on screen competing with what matters? |
| **Good errors** | Does it say what went wrong, in plain words, and how to fix it? |
| **Help when stuck** | Is there help where you get stuck, rather than in a manual? |

Several heuristics usually fit one issue. Pick the one that explains it best and
move on. Arguing about which heuristic something belongs to is wasted time.

### 4. Write each issue the same way

**What breaks.** In plain words, from the person's side.

**Where.** The screen, and the exact element or label.

**Which rule.** One heuristic.

**How bad.** The severity, with a reason.

**What we already know.** The quote or claim, if there is one, or "nothing
behind this yet".

**What to do.** A concrete suggestion, not "improve clarity". If you genuinely
do not know the fix, say so. A named problem with an honest "not sure what the
right answer is" is more useful than an invented recommendation.

### 5. Severity

| | Means | Reality |
|---|---|---|
| **4** | Catastrophe. Fix before this ships | Data loss, money wrong, a dead end with no way out |
| **3** | Major. Important to fix | People will fail the task or route around it |
| **2** | Minor. Fix when you are nearby | Slows people down, they still get there |
| **1** | Cosmetic | Fix if there is time |
| **0** | Not actually a problem | You talked yourself out of it. Drop it from the list |

Rate it on three things together: how often people hit it, how much it hurts
when they do, and whether it keeps hurting or they learn their way past it once.
Something annoying that never goes away can outrank something painful that
people solve on their first try.

**Be strict with 4s.** If everything is a catastrophe, nothing is. A review with
nine 4s gets ignored, and deserves to be.

## The file

Write it to `docs/heuristic-reviews/<date>-<surface>.md`.

```markdown
# Heuristic review: [surface]
**Expert review, not research. Nobody used this.**
[date] · [what you were given] · [who ran it]

## What we looked at
[screens and flows]
**Not covered:** [states you could not reach, and why]

## The short version
[Three or four lines. The pattern, not a list. What is the one thing that would
make the most difference.]

## Issues
### [n]. [What breaks, in plain words] · severity [0-4]
**Where:** …
**Rule:** …
**What we already know:** [quote + claim id, or "nothing behind this yet"]
**Suggestion:** …

## What this can't tell you
[One evaluator, not three to five. Screens not reached. Which issues have real
evidence behind them and which are judgement. What would need a real session.]
```

Sort by severity, worst first.

## Handing it over

The markdown opens anywhere and pastes into a Figma comment or a doc as is. To
send it to a Figma agent, point the agent at the file and the frame together so
each issue lands on the screen it came from.

If someone asks for just the issues without the caveats, give them the issues
and the one label line. It is a sentence, and it is the difference between an
opinion and a claim about users.

## Being straight about the limits

Say these in the file, every time. They are not boilerplate, they change what
the reader should do with it.

**One evaluator finds a fraction of what is there.** The research on this is
clear: three to five people reviewing separately, then comparing, find
substantially more than one person does. One pass is a start, not a sweep.

**None of this is validated.** Every issue is a hypothesis. Some will turn out
not to bother anyone. A couple of real sessions will reorder this list.

**It cannot tell you what people want.** It only tells you where the interface
breaks its own rules. Plenty of usable products fail because nobody needed them.

If you have a real usability session coming up, hand them this list first. The
best use of a heuristic review is deciding what to watch for.

## Two things never to put in

**A number about users.** No percentages, no "most people". There is no sample
here.

**A ship or no-ship verdict.** It says what is broken and how badly. The call is
the team's.
