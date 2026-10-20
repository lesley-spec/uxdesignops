# When the sources disagree

Most synthesis treats disagreement as a problem with the data. It is usually the
most informative thing in the corpus — and the place where smoothing does the
most damage, because the resulting middle position is supported by nothing.

---

## First: is it really a disagreement?

Before classifying a conflict, rule out the three false ones.

| False conflict | Test | If true |
|---|---|---|
| **Different segments** | Split both sources by segment, tenure, volume, role | Not a conflict — two findings. Report both, scoped |
| **Different windows** | Line up the date ranges | Not a conflict — a change over time. That is a finding in itself |
| **Different definitions** | Does "completed setup" mean the same event in both? | Not a conflict — an instrumentation mismatch. Fix the measure |

Only what survives all three is a real disagreement.

## The four real patterns

### 1 — Qual says blocked, behaviour looks fine

Completion rates are normal; interviews describe it as painful.

**Usually:** a workaround is absorbing the cost. The task completes, off-platform
or the long way round. The metric cannot see the spreadsheet.

**Move:** search session replay for the long path before you dismiss the qual.
If you find the workaround, importance is high and frequency is understated —
the people who built it have stopped complaining.

### 2 — Behaviour shows a drop, nobody mentions it

PostHog shows people leaving; no ticket, no interview quote, no NPS comment.

**Usually:** silent friction. People don't notice it, don't blame the product
for it, or have no vocabulary for it. Absence of complaint is not evidence it
works.

**Move:** this is a MICRO study — show the screen, give the task, watch. Do not
ask "did you find this difficult?", which invites a no.

### 3 — Two qual sources conflict

One study says one thing, another says the opposite.

**Usually:** segment, not truth. Enterprise admins and self-serve admins are
different users with the same job title.

**Move:** split by segment first. If the split explains it, you have two scoped
findings and a better coverage matrix. If it does not, check recruitment: who
answered, and who did not.

### 4 — Support volume high, everything else quiet

Freshdesk is full of it; nothing else shows it.

**Usually:** self-selection. People write in when angry or blocked, not when
things are fine. The sample is the frustrated tail.

**Move:** read it as a **strong positive signal and a weak negative one**. High
volume means the problem is real for someone. Low volume means nothing at all.

---

## Writing it up

Never resolve a disagreement in the summary line. Write both, then the
question:

> **Contradicting evidence.** Interviews (n=6) describe proposal setup as a
> blocker; PostHog shows 88% completion on the same flow in the same window.
> Replay shows four of six completing it by re-entering details a second time.
> **What would settle it:** instrument the retry, or run a MICRO task-based
> study on the first attempt.

The reader now knows what is known, what is not, and what it would take. That is
the whole job.

## Independence

Two sources agreeing is only worth something if they are independent.

**Not independent:** an Outset study recruited from a Pendo guide, and the Pendo
guide's own poll. Same population, same self-selection, one source.

**Independent:** behavioural PostHog data on all users, and interviews with a
recruited sample. Different populations, different failure modes.

Before promoting a theme to HIGH, say in one line why the sources are
independent. If you cannot, it is MEDIUM.
