# Routing — the three modes

The mode is a statement about **ambiguity and consequence**, not about how soon
someone wants an answer or how busy the team is.

Source: Constantine Papas, *AI-Powered UX Research*, ch. 4. The ownership question in
SKILL.md comes from Lozé's bronze/silver/gold model.

---

## MICRO — 48 hours

Low ambiguity, small or reversible consequence. **One question**, no
sub-questions. Persona chat, a data query, or a single Outset study.

**What it can't do:** discover anything. MICRO checks a question against what we
already know. Where we know nothing about the area, a MICRO answer is an opinion
delivered quickly.

## SPRINT — 1–2 weeks

Moderate ambiguity, material consequence. **One central question plus two to
four sub-questions.**

The sequence is the point: run the Outset study → read the results → pick the
people whose answers were surprising, contradictory, or thin → 15-minute
follow-up calls. **The follow-ups are what make it a SPRINT.** An Outset study
with nobody followed up is a MICRO that took two weeks.

## DEEP — 4+ weeks

High ambiguity, or a consequence that is big or hard to undo. Open-ended.
Contextual inquiry with 15–20 participants, diary studies, extended engagements.

This is the mode that **builds the Frame** — new personas, unmet needs,
foundational coverage of an area we have never looked at. It is research-led for
that reason.

---

## Choosing

Score **ambiguity** and **consequence** separately. The higher one wins.

| | MICRO | SPRINT | DEEP |
|---|---|---|---|
| Ambiguity | We understand the problem | Mostly | We don't |
| Consequence | Small or reversible | Material | Big or hard to undo |

**Ambiguity wins outright** — if we cannot state the problem, it is DEEP whatever
the consequence, because an unstateable problem is a hole in the Frame and only
DEEP fills those.

| Request | Routes |
|---|---|
| "Does this empty state read as an error?" | MICRO |
| "Why did onboarding completion drop 8%?" | SPRINT |
| "Clear problem, but it changes how everyone gets paid" | DEEP — consequence |
| "What does an AI Developer partner actually need?" | DEEP — ambiguity |

**Between MICRO and SPRINT?** Can one Outset study answer it alone — yes, MICRO;
needs human follow-up to interpret, SPRINT. This breaks ties only. It never
overrides the two axes above.

---

## Two bugs this version fixes

Kept short, so nobody reintroduces them.

**1. The original validity gate rejected every MICRO request.** It asked whether
an answer stays valid longer than two weeks — but MICRO is *defined* by an
answer that expires fast. Fixed by asking two things in one question: when do you
need it (a deadline) and how long must it hold (shelf life). The test is whether
the answer **outlives the decision it informs**, not whether it lasts two weeks.

**2. The original decision tree mixed AND and OR.** MICRO and SPRINT needed all
three conditions; DEEP fired on any one. So a clear problem affecting 30% of
users matched nothing, and a clear low-reach question with a four-week timeline
matched two modes at once. Fixed by scoring axes independently and taking the
highest — and by moving turnaround out of the axes entirely, since a deadline
should never be able to make a question simpler than it is.
