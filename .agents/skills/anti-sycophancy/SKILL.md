---
name: anti-sycophancy
description: >-
  Challenges weak UX framing and agreeable drafts — flags thin evidence, feature-
  as-goal, and one-sided marketplace claims. Use in Define (write-spec review),
  critique of one-pagers, or when the user asks to pressure-test a problem statement.
license: Proprietary
metadata:
  stage: define
  pipeline: impact-ux-designops
  author: impact.com-ux
---

# Anti-sycophancy (Define)

Adversarial review for problem framing. Prefer hard questions over polished agreement.

## When to use

- Before publishing a `write-spec` one-pager
- User asks “challenge this” / “what’s weak here?”
- Soft language (“users struggle”) without Verified evidence

## Checklist

1. **Evidence** — Which claims are Verified? Which are AI interpretation? Any low-N or empty Dovetail matches?
1b. **Beliefs table** — Does the one-pager name the claim ids it rests on, with
   confidence, n and last-verified date? Missing table is itself a finding: the
   spec cannot be found when one of its claims is retired.
1c. **Confidence vs commitment** — Is a build decision resting on MEDIUM or LOW?
   Building needs HIGH with corroboration; deprioritising can rest on MEDIUM.
   A mismatch here is the most expensive thing on this list, and the easiest to
   wave through because the doc reads confidently.
2. **Goal ≠ feature** — Rewrite feature names into customer/business outcomes.
3. **Marketplace** — Brand and Partner both addressed, or explicit single-side caveat?
4. **Disconfirming** — What would falsify this problem? Is that mentioned?
5. **Scope honesty** — In/Out clear? Hidden solution baked into the problem statement?
6. **Gate** — Ready for Designer sign-off + PM chat, or send back to Empathize?

## Output

```markdown
# Pressure test — [title]

## Keep
- …

## Challenge
- …

## Rewrite suggestions
- Goal: …
- Problem statement: …

## Gate recommendation
- [ ] Ready for Designer + PM chat
- [ ] Revise framing
- [ ] Back to Empathize (`user-research` / `research-synthesis`)
```

## Prompt examples (tested)

1. `Use anti-sycophancy on this UPS Step 2 one-pager draft — what is too weak for Designer + PM review?`  
   → Keeps volume; rejects empty Dovetail / off-topic Outset as triangulation; fieldwork before Ideate.

## Anti-patterns

- Softening criticism to be “helpful”
- Inventing counter-evidence
- Passing a one-pager whose central belief is UNVALIDATED because the writing is good
- Challenging the prose while leaving the evidence base unexamined
- Approving framing on single weak source
