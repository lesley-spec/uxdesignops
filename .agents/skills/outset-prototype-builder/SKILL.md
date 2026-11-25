---
name: outset-prototype-builder
description: >-
  Builds a behavioural Outset study around a clickable prototype. Takes the study
  goals, drafts a first guide and screener, writes the outreach invitation, then
  refines the guide from real transcripts and screen recordings. Use when someone
  says build an Outset study for this prototype, write the guide for the
  prototype, draft the outreach to participants, refine the guide from the
  transcripts, or review a prototype session recording.
license: Proprietary
metadata:
  stage: test
  pipeline: impact-ux-designops
  author: impact.com-ux
  picks-up-from: prototype-handoff
---

# Outset prototype builder

Turns a prototype and a set of study goals into an Outset study that watches what
people do, then tightens it on what the first sessions show. Five stages, and the
researcher signs off between each one.

**Draft only.** Build and edit the Outset study, the invitation and the guide as
drafts. Do not launch recruitment, publish the study to live traffic or send
invitations. Those need an explicit go from the researcher. Outset, Rally and
Pendo are drafts-only until a human confirms.

**Label every finding.** Use *Verified* for something a transcript quote or a
visible screen action shows, and *AI interpretation* for anything inferred. Never
invent participants, quotes or metrics.

## Choose the branch first

Outset has two disciplines. Pick the right one before writing a question.

| The question is | Use |
|---|---|
| How much, is it ready, which of two (closed, gated, under 5 minutes) | [research-planner outset.md](../research-planner/references/outset.md) |
| What do they do, where do they get stuck, what is the workaround (tasks, think-aloud, 10 minutes) | **This skill** |

A prototype study with tasks is the behavioural branch. Read
[prompts.md](../research-planner/references/prompts.md) for the wording rules,
which ban yes/no comprehension and terminology questions.

## Stage 1: Intake the study goals

Ask for these in one message, numbered. Proceed with stated defaults for anything
the researcher skips, and flag each default.

1. **Decision.** What will change after the study, in one sentence.
2. **Goals.** Three to six, each one sentence, in the form "Understand how / Assess
   how / Identify / Gauge".
3. **Prototype.** Link, device, and which parts are built versus stubbed.
4. **Audience.** Who qualifies and what the screener must catch.
5. **Tasks.** Any tasks the researcher already has in mind.
6. **Logistics.** Incentive, payment timing, target number, language and length.
7. **Out of scope.** What the study must not try to answer.

Then map every goal to a task or question. Name any goal with no task, for
example discovery outside the participant's existing relationships, or interest in
a concept that is never shown. Ask whether to add a task, or drop the goal.

## Stage 2: Build the first version

Write the guide in this order. It is the format the Outset builder reads.

```
Header        Organization, Project, Interview type, Device, Study language,
              Guide (sections, questions), Screener (count), Participant target,
              Incentive and payment timing, Moderator
Goals         The intake goals, unchanged
Context       Two or three neutral sentences
Priorities    Live moderation rules for the task questions (below)
Screener      S1 email for payment, S2 current use, S3 frequency, language check
Guide         Welcome, then Section 1 (tasks), then Section 2 (concept and close)
```

Each question carries its type, its flags and its probe:

```
Q2. [Conversational] For your first task, imagine ... Talk through your thinking.
Required · Probing: 1-3 follow-ups · Ask verbatim
Probing instructions: ... (what to ask, and the trigger for each probe)
```

**Rules that the first sessions taught us**

- **Tasks name a goal, not a control.** "Find the link you would share with your
  audience ... then click Copy link". Do not use a term the prototype never
  defines. "Promotional link" made one participant unsure what to copy.
- **Mark the success object precisely.** Write what counts as done, and tell the
  moderator to mark the outcome *unverified* when the click cannot be seen.
- **Discovery tasks use a relationship the participant does not already have.**
  Two participants rated a task "10/10" because they loved the brand they already
  worked with. The rating measured the brand, not the prototype.
- **Ratings ask about the product, then probe the brand.** Add "Would you have
  chosen this without the brand?" Ratings pile up at the top of the scale, so
  pair every rating with a probe for the hardest moment.
- **Do not ask a yes/no about terminology.** "Is this an early access link?" gets a
  "Yes" with no evidence behind it. Ask a scenario instead: "If you shared this
  link today, when would you expect to start earning from it?", with options.
- **"What's missing" needs an anchor.** "Nothing" is the default answer to an open
  question. Ask "What was the hardest moment today?" and then "What did you expect
  to find that wasn't there?"
- **Mark wording verbatim where the wording matters.** Unmarked questions drift
  between moderator sessions.
- **Describe a concept before asking about it, in plain words.** Do not use internal
  names. "An AI assistant connected to your account" worked where "impact MCP" did
  not.
- **Pair a preference question with an interest scale.** "Where would you look?"
  measures preference. "How interested would you be?" measures interest.
- **Cap probes at three follow-ups.** Give each probe a trigger, so the moderator
  does not run every probe every time.
- **Estimate length from the words, then pilot.** Count the spoken words and budget
  for on-screen time. A full session is far longer than the spoken words suggest.
  Do not promise a length to participants until one pilot has run.
- **Add a language check when the study is in one language.** A participant who
  could not follow the English audio produced almost nothing usable.

**Building in Outset.** Use the Outset connector to create the draft study, the
screener questions and the audience (create_study, create_question,
add_screener_question, set_invite_audience). Stop before publish_study and
launch_recruitment. Run the three-participant pass in
[rigor.md](../research-planner/references/rigor.md) before the rest of the sample
is recruited.

## Stage 3: Outreach messaging

Use this structure. It is the one agreed for the marketplace study.

- **Subject.** Names the topic and the incentive, for example "Help shape the new
  impact.com marketplace: $30 for your feedback".
- **Opening.** What we are building, in one or two sentences, and "we want to know
  what you think".
- **What it involves.** Bullets: the interview format, "at a time that suits you",
  the device, and screen sharing. Give the length only as an estimate until a pilot
  has run.
- **What's in it for you.** Bullets: the exclusive look, that this is the first of
  several studies and feedback shapes the next version, and the reward with its
  timing.
- **Deadline and one link.** One call to action.
- **Sign-off placeholders.** [First name], [Your name], [Team], [link].

**Rules**

- Do not say "thanks for your earlier research" unless the people invited took
  part in it. Partners may not have.
- Keep the reward timing identical in the invitation, the screener and the guide.
  A mismatch ("within 72 hours" in one place, "within a week of our review" in
  another) causes support questions.
- Keep the tone collaborative and inviting. Do not promise product features.
- Check the incentive against the real session length. For a 10-minute B2B session,
  $30 is at the generous end of the usual range, provided the session really does
  take about 10 minutes.

## Stage 4: Refine from the real transcripts

Run this after each batch of sessions, and before changing the guide.

1. **Pull the transcripts** from the Outset transcript link or the connector.
2. **Check for screen evidence.** A transcript cannot show a click. Mark every task
   outcome *Verified* only when the recording shows it, otherwise *unverified*.
3. **Log each task**: starting point, outcome, rating, and the quote that backs it.
4. **Look for these patterns**, which the first two sessions showed:
   - a participant asking what to do, which means the task is ambiguous;
   - a rating driven by the brand rather than the product;
   - "nothing missing", said right after a blocker the participant described;
   - a moderator changing a question's wording between sessions;
   - a language or audio failure;
   - a prototype limitation read as a participant error.
5. **Propose edits per question**, each with its evidence and sample size. Label
   each edit *Verified* or *AI interpretation*.
6. **Do not rewrite on fewer than about five sessions** unless one failure is
   severe. Treat early edits as hypotheses for the next batch.
7. **Log the version** with a change log that links each change to its evidence.

## Stage 5: Screen recording review

Only when the recording includes the participant's screen. Check first. If the
frames show an audio waveform or subtitles and no screen, stop and say that no
clicks can be read from it.

1. **Extract frames** every two to four seconds, using a bundled ffmpeg (for
   example the imageio-ffmpeg package in a scratch virtualenv). Do not run tools
   from inside the downloaded folder.
2. **Build contact sheets** of four frames, each labelled with its timestamp, and
   read them in order.
3. **Log each screen** the participant visits: timestamp, screen name, visible
   cursor position, and any click.
4. **Build the heat map** per screen: click positions normalised to the screen, the
   route between screens, and time on each screen. Label clicks *Verified* when a
   cursor click is visible, and *inferred* when the click is only implied.
5. **Report the limits.** A click needs a visible cursor, so note any screen where
   the cursor is hidden.

## Output checklist

- [ ] Goals mapped to tasks, with gaps named
- [ ] Probes capped at three, each with a trigger
- [ ] Verbatim marked on wording-critical questions
- [ ] Reward timing matches across invitation, screener and guide
- [ ] Length estimated from words, pilot planned before the invitation promises it
- [ ] Nothing published, launched or sent without the researcher's go
- [ ] Every finding labelled Verified or AI interpretation, with sample size
