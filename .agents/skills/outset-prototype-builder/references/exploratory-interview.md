# Branch B: Exploratory interview on Outset

Use when the researcher wants to understand how people think, decide or work in
an area that is not yet defined, and there is no prototype to test. Read it with
[SKILL.md](../SKILL.md). Stages 1, 3 and 4 apply as written. The question rules
below replace Stage 2's for this branch.

Guidance here comes from vendor and independent sources (listed at the end).
Where a rule is standard practice rather than something a source says, it is
marked *standard practice*.

## Fit check first

AI moderation works best once the research question is defined. Maze recommends
human moderators for exploratory work. NN/g tested two AI interviewers on the same
script and found one ran long summaries and over-enthusiastic replies, while the
other felt cold, brief and barely probed. So before drafting anything:

- **Name the decision** the study informs, in one sentence. If nobody can, say so
  and recommend a human-moderated discovery session first.
- **Write three to five goals**, each as "Understand how / Identify / Gauge", each
  specific enough to have a *good enough* answer.
- **If the brief is fully open** ("tell me about your work"), do not draft the
  guide. Ask the researcher to narrow it, or recommend a human moderator.

## The budget, set before any question

| Budget | Rule | Why |
|---|---|---|
| Length | 15 to 20 minutes of conversation. *Recommendation*, based on Forrester's guidance that AI-moderated interviews suit sessions under 30 minutes | Fatigue shows as one-word answers late in the session |
| Main questions | Five to seven. Each maps to one goal | Past seven, the last goals go unanswered |
| Probes | At most two per main question, each with a trigger and a stop condition | Outset's depth varies by answer, and its deepest mode can run up to ten layered follow-ups. Unbounded probing spends the whole budget on one goal |
| Good enough | Per goal, what a complete answer contains | Tells the moderator when to stop probing |

State the probe cap inside the probing instruction itself ("ask at most two
follow-ups"), not only in the depth setting, so the limit survives a change of
setting.

## Guide structure

1. **Opening (verbatim).** Welcome, the purpose ("we want to understand how you
   handle X"), no right answers, and "we're learning about the topic, not testing
   you".
2. **Section 1: The last time.** Past behaviour, one specific event.
3. **Section 2: Workarounds and tools.** What they use instead, and why.
4. **Section 3: The hardest moment.** Where it went wrong or took longest.
5. **Section 4: Expectation and interest.** One interest scale, then why.
6. **Close.** "Is there anything about this we have not asked that matters?"

Put the most important goal in Section 1 or 2, so a session that ends early still
answers it.

## Writing the questions

- **Ask about one past event.** "Tell me about the last time you did that" returns
  specifics. "How do you usually do that?" returns the version people think they
  should give. *Standard practice.*
- **Behaviour before opinion.** Ask what they did, then what they thought.
- **One concept per question.** No double-barrelled questions.
- **No yes/no questions.** [prompts.md](../../research-planner/references/prompts.md)
  bans them where they invite people to avoid admitting failure.
- **Do not name a feature** before the participant has described their own
  approach. Naming it first hands them the answer.
- **Mark wording verbatim** wherever the wording matters.

## Probing rules

Each probe is an explicit direction to the AI, in this shape:

```
Probe:    [what to surface]
Trigger:  [the answer is vague, gives no example, or contradicts an earlier answer]
Stop:     [once they give one concrete example, or after two probes]
```

Four probe types cover most needs:

- **Example:** "Tell me about the last time that happened."
- **Sequence:** "What did you do next?"
- **Contrast:** "What did you expect to happen instead?"
- **Priority:** "Of those, which mattered most, and why?"

Use "what" and "when" for behaviour. Use "why" once per answer, not in chains.

Keep out of probes: pricing and purchase frequency (give them their own
instruction, per Outset's guidance), and any question asking the participant to
predict future behaviour without an example.

**Moderator voice.** Put this in the Priorities block: "Do not summarise, praise or
agree with the answer. Acknowledge in a few words, then ask the next question or
probe." It targets the NN/g failure of long summaries and enthusiastic replies.

## Efficiency

- **Sequence.** One warm-up question in their own work, then the past event, the
  workaround, the hardest moment, expectation and interest, then close.
- **Time budget per question** in the guide, for example "about two minutes". Mark
  the lowest-priority question with "Skip if running over" so the moderator knows
  what to drop.
- **Stop rule.** Once a goal has its good-enough answer, move on, even if a probe
  is still available.
- **Merge check.** If two questions would produce the same answer, cut one.

## Pilot and refine

Run the first three sessions as the rigor pass in
[rigor.md](../../research-planner/references/rigor.md). Check:

- Did the probes fire where intended?
- Were triggers too broad (every answer probed) or too narrow (never fired)?
- Minutes per session, against the budget.
- Did the moderator summarise or praise? That is the NN/g failure. Fix the
  moderator-voice line before changing any question.

Log per session: minutes, main questions completed, probes fired per question, and
which goals reached a good-enough answer. Do not rewrite on fewer than about five
sessions unless one failure is severe (Stage 4 rule).

## Readout

Goal coverage, with n on every row:

| Goal | Sessions with a good-enough answer | Representative quote |
|---|---|---|

Label each finding *Verified* (backed by a transcript quote) or *AI
interpretation*. A goal met in two of six sessions is a partial answer, and the
readout should say so.

## Sources

- Outset help: [best practices for writing probing instructions](https://help.outset.ai/en/articles/10697756-best-practices-for-writing-probing-instructions). Probing as explicit directions; keep pricing out of probes; avoid redundancy.
- Outset: [AI Moderated Interviews: A Practical Research Guide](https://outset.ai/almanac/ai-moderated-interviews-a-practical-research-guide).
- Outset: [how participants experience AI-moderated interviews](https://outset.ai/blog/how-participants-experience-ai-moderated-interviews). Source for the deeper follow-up mode. Check the current limit in the connector before relying on it.
- Forrester: [AI-Moderated Interviews Expand How Teams Conduct Customer Research](https://www.forrester.com/blogs/ai-moderated-interviews-expand-how-teams-conduct-customer-research/). Under 30 minutes.
- NN/g: [AI interviewers](https://nngroup.com/articles/ai-interviewers/). Tool variation; pilot the probing.
- Maze: [AI moderated research](https://maze.co/guides/ai-moderated-research/). Defined questions suit AI moderation; human moderators for exploration; set a probe limit.
