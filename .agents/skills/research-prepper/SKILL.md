---
name: research-prepper
description: >-
  Prepares a researcher for a call with a user, an account, or a named person.
  Use when someone says "prep me for a call", "discussion guide", "day in the
  life", "analyze this interview", or gives an account, email, or name with a call
  coming up. Scopes the call first, pulls what we know from Dovetail, Outset,
  Slack, PostHog and the Frame, then drafts a short brief, a moderator guide, and
  after the call, a Slack note.
license: Proprietary
metadata:
  stage: empathize
  pipeline: impact-ux-designops
  author: impact.com-ux
  requires-connectors: dovetail, posthog, outset, slack
  optional-connectors: google-calendar, atlassian, pendo, salesforce
---

# Research prepper

## Rules

- **Draft only.** The researcher owns what is said on the call and what is
  published. Nothing goes to Dovetail, Slack or a calendar until they confirm.
- **Label every claim** Verified (with its source), Inferred (with the reasoning),
  or Unknown. Never invent a metric, quote, or participant.
- **Stop if the identifiers disagree.** If email, account ID, and name do not
  match, ask before going on.
- **Narrow to the people named.** A shared login is a finding about the login, not
  about one person. Say so.
- **Plain language** in the guide and the Slack note. No method jargon.
- **Do not read data aloud.** Counts, dead clicks, and ticket IDs go in brackets
  for the researcher.

## 0. Scope the call first

Ask before any research. Use AskUserQuestion if it is available, otherwise ask in
chat. Do not start research until both answers are set.

1. **General or specific?**
   - *General:* full prep across who they are, jobs, friction, and unmet needs.
     Default guide is 20 minutes.
   - *Specific topic:* the researcher names it (for example marketplace, a named
     report, contracts, payouts, rage clicks, or a feature area). If they have not
     named it, ask. The guide and the evidence pulls then focus on that topic. The
     other sections stay as one-line context.
2. **First call or follow-up?** A follow-up starts from what has changed since the
   last call, and pulls the previous call's summary first.

Also get the identifier (email, account ID, or meeting name) and the call date if
they are missing.

## 1. Brief

1. **Resolve the account and the people.** From an email: `persons-list`. From an
   account ID: find the account group index first (read a `$groupidentify` event;
   do not assume an index). From a meeting: `get_calendar_events` on `primary`,
   then `get_event`. The subjects are attendees **not** on impact.com.
2. **Read prior research:**
   - *Dovetail:* `list_contacts` by name, then `search_workspace` with
     `speaker_ids` set to the contact ID. Read each hit with `get_data_content`.
   - *Outset:* `list_projects`, then `search` for the company name. Outset does not
     key participants by email. Match by reading transcripts.
   - *The Frame and the persona:* ask `user-context` for what we know, and
     `user-personas` for the matching persona.
   - *Follow-up:* summarise the last call in a few lines first: who they are, how
     the work runs, and what was still open.
3. **Product use, last 90 days** (PostHog, after `learn`):
   - Pages, reports, exceptions (group by `$exception_values`, because
     `$exception_type` is empty), rage clicks, and dead clicks.
   - For a specific topic, focus these reads on that topic.
   - Add open Jira or support threads that name the account, if Atlassian is
     connected.
4. **Recordings.** Sample the busiest recent sessions: default 10 in the last 30
   days, weighted toward the topic if there is one. The researcher can raise the
   count. This environment cannot play video, so say that you read metadata and
   event trails, not recordings. Describe actions, not intent.
5. **Slack.** Search the company or person name, `response_format` `concise`,
   `limit` 5. Note internal discussion of the account, and quote the date and the
   channel. Skip automated alert channels unless they name this account.
6. **Chat brief, five lines at most:** who and when, the one thing that should
   change how the call opens, the top friction, the open question, and links. Put
   the detail in the document.

## 2. The guide

- Bullets, one question per section.
- *General interview:* 20 minutes, human-led.
- *Day in the life:* a 30-minute timed version with screen share. Same sections.
- Open with: **"We are here to understand you as a partner or brand, and how you
  use the platform."**

Sections, in order:

1. **Who they are.** Role, who else uses the account, what a good week looks like.
   On a follow-up, start with what has changed.
2. **Jobs.** The last time they came in: what they opened and what they were there
   to finish.
3. **Friction.** In that same sitting, where they stopped, repeated something, or
   left the platform.
4. **Unmet needs.** After they closed it, what was still undone, and where they
   finished it.
5. **Evidence-led topics.** For a general interview, two topics drawn from what this
   account actually does. For a specific topic, replace these with three to five
   questions on the last real time they did it, what they used, and where it broke.

Moderator notes go in brackets: which session to listen for, which figure is the
researcher's to raise, and when to drop a topic that is not the participant's job.

Keep feature requests, ratings, and pitches out of scope until the participant
raises them. Listen for one real sitting, its outcome, and any workaround. Stop
early if they can only talk about the product in general.

## 3. After the call

Analyse against the planned questions, in this order:

- **General:** who they are, what they do on the platform, moments of friction,
  unmet needs.
- **Specific topic:** the topic first, then the other sections in one line each.

Merge the researcher's notes. Where they conflict, keep the researcher's facts and
mark what the transcript adds.

Then draft, for the researcher to approve:

- **A short Slack note:** a one-paragraph finding, the answers, wishes by person,
  and next steps with an owner.
- **Clip timestamps,** with at least one moment that is working, so the reel is not
  only complaints.
- **Dovetail:** `create_data` into the project, and highlights, only after the
  researcher confirms. Use plain text or HTML, never Markdown or a doc.

## Known pitfalls (this PostHog project)

- `$exception_type` is empty. Use `$exception_values`.
- The account group key is in `$group_N` columns on `events`. Check the index.
- `loginBrandAccountId` marks a brand login surface, not one customer.
- Recordings are kept 90 days. Set `date_from` to `-90d` for account pulls.
- `session-recording-get` returns metadata only, not the events in a session.
- Salesforce is not connected. Until it is, write "Salesforce: not checked".
- Outset does not hold participant emails. Match by transcript, not by ID.

## Open conflict to confirm

Sampling default: this brief says **10 recordings in the last 30 days**. Your
earlier instruction was **at least 20**. The skill uses 10 unless the researcher
sets a higher count.
