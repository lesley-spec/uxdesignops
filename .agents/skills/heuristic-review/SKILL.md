---
name: heuristic-review
description: >-
  Expert usability pass over a screen, flow, prototype or Figma frame — the ten
  classic heuristics plus the marketplace ones impact.com keeps breaking:
  two-sided consequence, money legibility, role truth, scale asymmetry. Each
  finding names the heuristic, the likely user cost, a severity, and the
  cheapest fix. Expert judgement, never evidence. Use when someone says run a
  heuristic review, expert review, usability review, what's wrong with this
  screen, give this a once-over before I show it, or review this flow.
license: Proprietary
metadata:
  stage: ideate
  pipeline: impact-ux-designops
  author: impact.com-ux
  output: expert-judgement
---

# Heuristic review

One pass over a design against a fixed list, so the obvious problems are found
by a checklist rather than by a participant in session three.

Minutes, not days. It needs no recruiting, no connectors and no prototype — a
screenshot, a Figma frame, a URL or a description is enough.

## The rule everything else depends on

**Everything this skill produces is Expert judgement.** Never evidence.

> Never write "users struggle with" about something a heuristic review found.

A violation predicts a problem. It does not measure one, and the size of the
problem is unknown until someone watches a real person hit it. Label the
output, keep the label on it when it travels into a doc, and when a review and
a study disagree, the study is right.

## What it is not

| | |
|---|---|
| **`heuristic-review`** | Does this design break known usability principles? |
| **`ux-critique`** | Does it cover the one-pager, the epic and the tickets? |
| **`persona-check`** | Where does *this named person* get stuck walking through it? |
| **`accessibility-review`** | WCAG blockers, focus order, contrast, keyboard paths |
| **`user-context` critique** | What the evidence predicts about this design |

The four pre-test skills answer different questions and none substitutes for
another. A design can pass every heuristic and still solve the wrong problem —
that is `ux-critique`'s job, not this one's.

## Integrity

**Lead with the insight, not the evidence.** What they get back is short: the
findings that change something, ranked. Not a numbered sweep of all fifteen
heuristics — nobody reads the clean ones.

**Offer the depth, don't deliver it.** Close with one follow-up they can run —
*"want the full pass including what's already fine?"* — not a menu.

1. **Name the heuristic.** A finding without one is an opinion. Use the list in
   [references/heuristics.md](references/heuristics.md) and quote its name.
2. **Say what the user does.** Not "this is confusing" — *"they will hit Save
   expecting a draft and publish to live partners."* No predicted behaviour, no
   finding.
3. **Rank by consequence, not by count.** Three findings that cost money beat
   twelve that cost a second. Severity rules below.
4. **Cheapest fix that clears the violation**, not the redesign you would
   prefer. If the fix is a redesign, say that plainly and say why.
5. **Check both sides.** Every impact.com screen sits in a two-sided
   marketplace. A brand-side change that quietly costs partners is a finding
   even when the brand screen is immaculate.
6. **Separate what you can see from what you are assuming.** A static frame
   hides states. Say which findings depend on behaviour you could not observe.
7. **Do not invent the product.** If you cannot tell what a control does, that
   is itself a finding under *Recognition over recall* — do not guess and
   review the guess.

## Workflow

```
Task Progress:
- [ ] Get the artifact and the context
- [ ] Pass against the list
- [ ] Severity and fixes
- [ ] Offer the evidence cross-check
```

1. **Take the artifact.** URL, Figma frame, screenshot, or a description.
   Ask for only what is missing, once: who the screen is for (brand or
   partner), and the one task it exists to support. Without the task there is
   no *Match with the real world* and no severity — say so and ask.

2. **Pass against [references/heuristics.md](references/heuristics.md).** Ten
   classic, five marketplace. Work the list, not your first impression.

3. **Write the findings** in the format in
   [references/report.md](references/report.md). Ranked, severity-rated, each
   with the heuristic, the predicted user cost, and the fix.

4. **Offer the cross-check.** Some findings will already be answered —
   confirmed or contradicted — by what we know. Offer one line:
   *"three of these touch claims in the Frame — want me to check them against
   `user-context`?"* Do not run it unasked.

5. **Hand on.** If the design is heading for sessions, the next skills are
   `accessibility-review` then `persona-check`, and `test-plan` turns the
   unresolved findings into tasks worth watching someone attempt.

## Severity

| | Means | Example |
|---|---|---|
| **Blocker** | The task cannot be completed, or completing it causes loss — money, data, a live change they did not intend | Publish with no confirmation on a live partner list |
| **Major** | The task completes but most people take a wrong turn first, or a sizeable group gives up | Primary action below the fold on the densest screen |
| **Minor** | Friction. People get there, slower or more annoyed | Filter state lost on back navigation |
| **Cosmetic** | Inconsistency with no behavioural cost | Two button styles for the same action class |

Severity is **frequency × cost × recoverability**, judged for the role the
screen is for. A rare action that moves money outranks a daily one that costs
a click. If you cannot judge frequency, say so and rate on cost alone.

## Output

Short. Blockers and Majors in the reply, Minors and Cosmetics listed as
one-liners, Cosmetics collapsed into a single line if there are more than
three. Full template:
[references/report.md](references/report.md).

Every finding carries the **Expert judgement (AI)** label when it travels into
Confluence, a ticket or a readout.

## Anti-patterns

- Walking all fifteen heuristics out loud, including the ones with no findings
- "This is confusing" with no predicted behaviour behind it
- Severity by how strongly you feel about it
- Reviewing one side of the marketplace and calling the design reviewed
- Redesigning instead of reviewing — the fix clears the violation, nothing more
- Writing "users will" instead of "a partner at this step likely"
- Letting a finding reach a doc without the Expert judgement label
