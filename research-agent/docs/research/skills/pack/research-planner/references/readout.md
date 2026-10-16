# Readout structure

Four questions, in order. The same shape for MICRO, SPRINT and DEEP — only the
depth changes.

---

## 1 — What did you ask?

- The research question, from hygiene
- The decision it informs, and its owner
- Why it mattered now — timeline and impact
- **Why this mode** — what about the request made it MICRO, SPRINT or DEEP

That last line is doing more than it looks. It teaches the room to triage their
own requests: *"next time we need an answer by Friday, we do MICRO like this."*

## 2 — What did you find?

**Observations, not recommendations.** Each finding carries:

- Its evidence trail — quote, timestamp, link
- Disconfirming evidence, or a statement that you looked and found none
- **Frequency and importance, separately**
- A confidence level and an n

## 3 — What does it mean for the decision?

- The go/no-go against the thresholds **agreed before fieldwork**
- What this changes
- What it leaves untouched
- Next steps, if any

Thresholds set in advance make this section short and unarguable. Without them it
becomes a negotiation about what the data "really" shows.

## 4 — What can't it tell you?

The section most readouts omit, and the one that earns trust.

- Sample limits — n, diversity, how recruited
- Method limits — what you couldn't test, and why
- Coverage gaps — segments you didn't reach
- What still needs investigating

Stating your limits plainly is what makes the rest of the document credible. A
readout with no limitations section reads as a sales pitch, because that is the
only kind of document that has no limitations.

---

## Also include

**Method and cost** — mode, sample, how recruited, how long it took, effort
spent. This is how the organisation learns what research trade-offs actually
look like.

**Behavioural data**, where it exists. Do people use the feature the way they
said they would? Does PostHog agree with the interviews? Does Pendo show them
finding the thing they said was obvious? This is where stated and actual
behaviour get compared, and the disagreements are usually the finding.

---

## Tone

State findings as observations. Let the reader form the recommendation.

| | |
|---|---|
| ❌ | "We should build bulk import because users want it." |
| ✅ | "6/8 admins mentioned bulk import as a priority. Current workaround is creating users one-by-one; frustration peaked at multi-hour manual processes. If built, observed expectation is under 5 minutes." |

The first is an opinion wearing research's clothes. The second is what you
actually saw, and it survives someone disagreeing with you.

---

## Then write it back

Extract the claims into `user-context` (`record` mode) and close the ticket.

**The readout is narrative and will not be read again.** The claims are what
compound — and the next person asking this question will find them in the Frame
rather than running the study a second time.
