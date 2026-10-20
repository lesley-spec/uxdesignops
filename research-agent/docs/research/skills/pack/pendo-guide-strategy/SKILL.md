---
name: pendo-guide-strategy
description: >-
  The strategic layer before anyone opens Pendo. Sets audience temperature,
  writes benefit-first copy, collapses the flow to a single step, and defines the
  three conversion goals that say whether a guide actually recruited anyone.
  Built for research recruitment and panel building; the levers work for any
  in-product guide. Use when someone says build a Pendo guide, our guide
  engagement is low, recruit partners into a research panel, should this be Pendo
  or email, or why did this guide underperform.
license: Proprietary
metadata:
  stage: empathize
  pipeline: impact-ux-designops
  author: impact.com-ux
  builds: pendo-guide|research-panel
---

# Pendo guide strategy

Guides fail because they get built first and thought about second. The common
result is **1–5% engagement**: shown to everyone, three steps long, no stated
benefit, no conversion goal, and no way to tell afterwards whether anyone joined
anything.

This is the layer **before** the Pendo UI.

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

1. **A guide is customer-facing.** It never goes to live traffic without a named
   human signing off. The skill drafts; a person ships.
2. **Guide engagement is not recruitment.** A 20% click rate with nobody in the
   panel is a failure. Measure through to participation or do not claim success.
3. **No decision, no guide.** If you cannot name the product decision the
   research informs, you are fishing. Stop here.
4. **One ask per person.** Frequency-cap and exclude prior viewers, or you train
   people to dismiss the next guide unread.
5. **Benchmarks are not promises.** The numbers below are planning targets from
   guide-type norms, not measured impact.com results. Record your own.

## The three levers

```
engagement  =  audience temperature  ×  message clarity  ×  friction
```

Cold audience + vague message + multi-step → **~2%**
Warm audience + clear benefit + single step → **15–25%**

Most teams only ever pull the third one. The first is the biggest.

## 1 — Audience temperature

| Temperature | Who | Expected | Use for |
|---|---|---|---|
| **Cold** — everyone | No prior in-app engagement | 1–5% | Urgent, universal only: security, critical bugs |
| **Warm** — engaged | Has interacted with other guides or releases | 15–35% | Research recruitment, feature adoption |
| **Super-warm** — behavioural segment | Matches specific recent behaviour | 25–50% | High-value recruitment, strategic pushes |

**Target on behaviour, not self-description** — "viewed a release guide twice in
90 days" beats "says they are an active user". Three segment recipes, written as
Pendo rules: [references/targeting.md](references/targeting.md).

> If you are about to launch to everyone and it is not an emergency, that single
> decision is costing you roughly a 10× difference in response.

## 2 — Copy architecture

Lead with the benefit, not the ask.

| Component | Job | Weak | Strong |
|---|---|---|---|
| Subtitle | Benefit first | "Help us out" | "Shape what we prioritise next" |
| Title | What I will do | "Participate in research" | "Join our user research panel" |
| Description | Why me, why now, what is involved | "Understand how you use the platform" | "First look at what we're building · 2–10 min studies · informs the roadmap" |
| Button | Assumptive and specific | "Learn more" | "Join the panel" |
| Decline | Keeps them warm | "Not interested" | "Remind me later" |

Full component guidance and the three-variant test framework (exclusivity /
community / problem-solving): [references/copy.md](references/copy.md).

## 3 — Friction: single-step or multi

**Single-step** — header, title, description, one CTA to an external form.
Use when you are asking for a **decision or a one-time action**. Join, sign up,
book. Expect 15–25% on a warm audience.

**Multi-step** — use only when you are **teaching a process**: onboarding,
feature walkthroughs. For recruitment it is a graveyard; typical drop is 70–80%
by step three.

Move the form and the scheduling *outside* the guide. The guide's only job is
the yes.

## 4 — The decision this informs

Answer all three before building. If any is blank, do not build.

1. **What product decision depends on this research?** Roadmap prioritisation,
   feature validation, adoption strategy, retention intervention.
2. **What would change if we got the feedback?** No answer means no study.
3. **Who has to see it to make that decision?** If no named person says yes, the
   audience is wrong.

Routing — whether this is MICRO, SPRINT or DEEP, and whether it should run at
all — belongs to `research-intake`, not here.

## 5 — Conversion goals

Set three in Pendo. Not one.

| Goal | Transition | Tells you |
|---|---|---|
| 1 Clicked the button | awareness → intent | Is the messaging working |
| 2 Completed the signup form | intent → commitment | Is the friction acceptable |
| 3 Attended the first study | commitment → follow-through | Does the panel actually exist |

**Goal 3 is the real one.** High 1 and low 3 means you built an audience of
clickers, and the fix is downstream of the guide — form, scheduling, follow-up.

## Benchmarks

| Guide type | Typical | Target | Note |
|---|---|---|---|
| Research recruitment | 1–5% cold · 15–25% warm | 15%+ | Warm targeting is the whole game |
| Feature release | 5–15% | 10%+ | Context-triggered |
| Urgent alert | 20–50% | 30%+ | The one case for cold |
| Survey / feedback | 5–10% | 8%+ | See `research-builder` for question shape |
| Onboarding, multi-step | 40–60% | 50%+ | Mandatory flow |

## Before launch

- [ ] Audience is warm — segmented on behaviour, prior viewers excluded
- [ ] Subtitle leads with the benefit
- [ ] The description names the decision the feedback informs
- [ ] Single step, one screen
- [ ] Button is assumptive; decline is "remind me later"
- [ ] Three conversion goals set, through to participation
- [ ] Success metric written down before launch, not after
- [ ] Run length set — 2–4 weeks saturates a warm segment
- [ ] **A human has signed off.** This is customer-facing

A ready-to-fill guide spec, the four failure patterns with their fixes, and the
FAQ: [references/template.md](references/template.md).

## Where this sits

| Skill | Does |
|---|---|
| `research-intake` | Decides whether the study runs at all, and how big |
| **this skill** | How to recruit for it in product |
| `research-builder` | Builds the guide — and the in-guide **survey** protocol, which is a different instrument: [its pendo.md](../research-builder/references/pendo.md) is two or three questions asked in place; this skill is recruitment out to a panel |
| `research-planner` | Designs the study the panel then takes part in |
| `adoption-check` | Whether the decision the research informed actually worked |
