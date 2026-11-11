# Meeting transcript to research ticket

Use this when the request arrives as a transcript or notes from a research briefing, kickoff or scoping call (Granola, Zoom, Google Meet, or pasted notes). The meeting usually answers most of the four intake questions. Pull those answers out, check them the same way as any request, and draft the ticket. Ask only for what the meeting did not cover.

## 1. Read the whole transcript

- Note who was there, who owns the decision, and what was actually decided.
- Transcripts are messy: speaker labels, filler, crosstalk. Work from what was decided or discussed, not from every sentence.
- Do not invent details. Quote only short phrases, and only where the exact wording matters.

## 2. Map the meeting onto intake

| The meeting covers | Intake question | Ticket section |
|---|---|---|
| What are we trying to answer? | 1. What do you want to know? | Question |
| Who decides, and what changes with the answer | 2. What decision, and who makes it? | Decision |
| Key dates, deadlines, review points | 3. When do you need it, and how long must it hold? | Decision (Needed by, Must hold until) |
| What happens if it goes wrong | 4. What happens if we get this wrong? | Route |
| Who we want to talk to | (part of scope) | Scope, Who |
| What we already know | Check 2 | What we already know |

If the meeting names a decision-maker or a deadline, use it. If it does not, say so in the ticket and ask for it in the draft reply.

## 3. Run the checks

Run Check 1 on what the meeting says. If the meeting says the call is already made, that is the Check 1 answer: offer to pressure-test it instead.

Run Check 2 as normal: the Frame first, then Dovetail, Outset and PostHog where they apply, then the Jira search in step 4 below. Route as usual: MICRO, SPRINT, DEEP, or instrument first.

## 4. Check Jira for related work

This is the Jira row of Check 2. It is read-only, and it runs before you draft, because a live ticket on the same question changes the route.

- Two searches at most. Use the main keywords from the topic and the research question. If the first search finds nothing, broaden the keywords once.
- Search the UX project only.
- Show the relevant hits in chat, with the draft: key, title, status, one line on how each relates to the new request, and any overlap in question, audience or prior findings. If nothing relevant turns up, say so.
- If a live ticket already covers the question, say so and route to wait, not to a second ticket.
- Do not add this summary to the ticket or post it as a comment unless the user asks.

## 5. Draft the ticket

Use the ticket template in [templates.md](templates.md), with these rules for meeting input:

- Title: `Research: [topic]`.
- Add a source line under the title: the meeting name, its date, and who was there.
- Keep every heading, even when the meeting did not cover it. Under an uncovered heading, write: `Not discussed in the meeting. [Suggested question to resolve it]`
- Show the full draft in chat. Keep any framing to one or two sentences. Ask for changes or approval.

## 6. Wait for approval

Do not call any Jira tool until the user clearly approves the draft as shown, such as "approve", "create it", or "looks good, publish". If they ask for edits, apply them, show the updated draft, and ask again. If the draft changes after approval, ask again.

## 7. Create the ticket

1. Confirm the UX project is reachable and check its available issue types.
2. Set the type by method, per [templates.md](templates.md): Research or Analytics. If neither exists, use Task and say so.
3. Assign it: look up Nihal Somers with `lookupJiraAccountId`, unless the person taking the request is someone else.
4. Create it in project `UX` (key UX) on board 679, [https://impact.atlassian.net/jira/software/projects/UX/boards/679](https://impact.atlassian.net/jira/software/projects/UX/boards/679), column To Do. Move it to To Do if it was not created there.
5. Report the ticket key and link in chat.

If any step fails, report the exact error and stop. Do not create a duplicate ticket.
