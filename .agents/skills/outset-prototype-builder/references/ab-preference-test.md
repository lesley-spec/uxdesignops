# Branch C: A/B preference test with image stimuli

Use when the question is which of two designs people prefer, and why, and the
designs can be shown as images or screens. Read it with [SKILL.md](../SKILL.md).
Stages 1, 3 and 4 apply as written. The stimulus and question rules below replace
Stage 2's for this branch.

Guidance here comes from vendor and independent sources (listed at the end).
Where a rule is standard experimental practice rather than something a source
says, it is marked *standard practice*.

## Fit check first

A preference test answers "which would you choose, and why". It does not answer
"which will perform better". User Interviews separates the two: preference tests
measure perception and opinion, and A/B tests measure behaviour. The Ontario
government makes the same point: what people say they prefer may not match what
they do. So:

- **If the decision is about a conversion, click or completion rate**, stop. Use
  the ab-test-planner skill for a live experiment. If the question is only "which
  of two" with no why, use the closed-ended route in
  [research-planner outset.md](../../research-planner/references/outset.md).
- **If the decision is about look, wording or how a task is framed**, this branch
  is the right tool. Label its results *stated preference*, never performance.

## Stimulus rules

- **Compare like with like.** Image against image, same size, crop and device
  frame, same content, one thing changed. Do not pit a video against a still image.
  (UserTesting's guidance.)
- **Change one variable per comparison.** If two things differ, the preference
  cannot be traced to either. *Standard practice.*
- **Neutral labels.** "Option A" and "Option B", or neutral names. Never the team's
  favourite name, and never the favourite in the first slot. *Standard practice.*
- **Randomise and counterbalance.** Randomise the order, and vary which option sits
  on the left across participants. Record the order each participant saw.
  *Standard practice.*
- **Two options per round, three at most.** With more, the forced choice becomes
  unreliable.
- **Show each option alone first (monadic), then side by side.** Ask the first
  impression on each option, then the comparison. The first impression is then not
  shaped by the other option. *Standard practice.*
- **Brand visible?** The brand effect from Stage 2 applies: a brand the participant
  already likes lifts its rating. If the study is about the design, neutralise the
  brand, or run a second version with it, and say which in the readout.
- **Check the image at the participant's screen size.** A stimulus cropped on their
  screen is a different stimulus from the one the team reviewed.

**In the Outset connector**, check the stimulus and concept tools before building
by hand. The connector exposes `upload_stimulus_bytes`, `update_question_stimulus`,
and concept-testing and monadic tools (`create_concept_testing_section`,
`set_monadic_config`). Confirm which fits, and record the choice in the change log.

## Question set

Use this order. Mark each question verbatim.

1. **First impression, per option (monadic).** "Looking at this image for a few
   seconds, in your own words, what is it showing you?" Open, not yes/no. It shows
   whether the option reads the way the team intends.
2. **Interest, per option.** "How interested would you be in using something like
   this to [task], from 1 (not at all) to 5 (very interested)?" Probe once: "What is
   the main reason for that number?" This pairs preference with interest, as Stage 2
   requires.
3. **Comparative choice.** "Which of these two would you rather use to [task]:
   Option A, Option B, neither, or both equally?" The escape options stop the
   participant inventing a preference.
4. **Why (required).** "What made you choose that one?" Probe once, on the contrast:
   "What would stop you from using the one you did not choose?"
5. **Trade-off.** "If you could keep one thing from the option you did not choose,
   what would it be?" This shows what to merge if the two designs each win on
   something. No probe.

**Do not use:**

- "Do you like A?" (yes/no, invites a polite yes)
- "Which is better?" (asks for a judgement nobody can ground)
- "Which would get more clicks?" (participants cannot predict their own behaviour;
  test that live)
- Stems that name a side ("the new design"), because the word carries the answer.

Cap probes at two per question, each with a trigger, as in Branch B.

## Analysis

- **Report counts with n.** "Seven of twelve chose Option A." Do not turn that into
  a population share. At this size a split is a reason to read the reasons, not a
  preference to build on.
- **Read the why beside every vote.** Dropbox's design team warns that raw counts
  pull attention from the reasons. Report reasons by option: "Reasons for A (n=7): …".
- **Check order effects.** If presentation order predicts the choice, the result is
  unreliable. Re-run with counterbalanced order before deciding.
- **Check every quote against the transcript** before using it. A count that matches
  the transcript is *Verified*. Grouping quotes into a theme is *AI interpretation*.
- **Decide only what the test can decide.** A preference result settles look,
  wording or framing. It does not settle which design performs better.

## Outreach

Use the Stage 3 structure. In "What it involves", say "you will see two designs and
tell us which you prefer and why". Avoid the phrase "A/B test" in the invitation.
It reads as testing the participant, and it sets an expectation of being measured.
*Recommendation.*

## Pilot

Run the first three sessions as the rigor pass. Check:

- Did every option get a first impression?
- Did the counterbalancing work in practice?
- Is "neither" or "both equally" used heavily? That means the options are not
  comparable, or the task does not fit the choice.
- Minutes per session.

## Sources

- User Interviews: [preference testing](https://userinterviews.com/ux-research-field-guide-chapter/preference-testing). Preference versus behaviour.
- Ontario government: [preference testing](https://www.ontario.ca/page/preference-testing). Stated preference may not match behaviour.
- UserTesting: [preference testing](https://help.usertesting.com/hc/articles/11880273593629). Like with like; no video against a still.
- GitLab handbook: [preference testing](https://handbook.gitlab.com/handbook/product/ux/ux-research/preference-testing/). Pair the choice with a "why" follow-up.
- Dropbox Design: [do you like it? how we evaluate preference](https://dropbox.design/article/do-you-like-it-how-we-evaluate-preference). Raw numbers against reasons.
- Digital.gov: [visual preference](https://digital.gov/guides/research-collaboration/testing/visual-preference). Ask as objectively as possible.
- NN/g: [preference testing for assessing visual design](https://www.nngroup.com/videos/preference-testing/). Preference testing sits alongside five-second and first-click testing.
