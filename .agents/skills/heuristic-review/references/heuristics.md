# The list

Fifteen. Ten are Nielsen's, restated for the product rather than quoted. Five
are impact.com's own — the ones a two-sided marketplace keeps breaking and a
generic checklist never asks about.

Work the list in order. Name the heuristic in every finding.

## The ten

**1 · Visibility of system status**
Does the screen say what is happening, and when it will be done? Saving,
syncing, queued, pending approval, scheduled. Anything that takes longer than
an instant, or that happens later, needs to say so where the person is looking
— not in an email an hour on.

**2 · Match with the real world**
Does the wording match what the person calls this, or what the database calls
it? Watch for internal names leaking: object types, statuses that only make
sense to the service that owns them, and acronyms that mean one thing to a
brand and another to a partner.

**3 · User control and freedom**
Can they get out? Back, cancel, undo, edit after save. Any action that cannot
be undone must be hard to do by accident, and must say it is permanent before
it happens, not after.

**4 · Consistency and standards**
Same thing, same name, same place, same control. Across the screen, across the
product, and against the styleguide. Two patterns for one job is a finding even
when both work.

**5 · Error prevention**
Is the mistake possible at all? Prefer a constrained control over validation, a
confirmation over an apology, and a default that is safe over one that is
convenient. The best version of an error message is the design where the error
cannot occur.

**6 · Recognition over recall**
Can they see what they need, or must they remember it from a screen they have
left? IDs typed from elsewhere, settings whose effect is invisible from where
you set them, and controls whose purpose you only learn by clicking.

**7 · Flexibility and efficiency**
Does the tenth time cost what the first did? Bulk actions, saved views,
keyboard paths, sensible defaults for the repeat case — without making the
first time harder.

**8 · Aesthetic and minimalist design**
Is everything on the screen doing work? Dense is fine when the job is dense;
decorative is not. Rank by what the screen exists to do and ask what competes
with it.

**9 · Recognise, diagnose, recover**
When it goes wrong, does the message say what happened, why, and what to do?
No codes without language, no "something went wrong", no dead end without a
route out.

**10 · Help and documentation**
Is help where the confusion is? In-context over a help centre, example over
explanation, and nothing that requires leaving the task to understand the task.

## The five

**11 · Two-sided consequence**
Does this screen show the effect on the other side of the marketplace? A brand
changing terms, pausing a programme or editing a payout changes a partner's
income. A partner's change alters a brand's reporting. The side taking the
action should see who it lands on and when they will find out — before they
confirm, not in the changelog.

**12 · Money legibility**
Where a number is money — commission, payout, fee, adjustment, hold — can they
tell where it came from, what period it covers, when it arrives and whether it
is final? Unprovenanced money is the single most expensive confusion in this
product. "Pending" with no date is a finding.

**13 · Role truth**
Does the interface match what this role can actually do? Actions that will
fail on permission, settings visible to someone who cannot change them, and
states the account type can never reach. Showing the door and locking it is
worse than not showing it — unless the screen says who can open it.

**14 · Scale asymmetry**
Does it work at both ends? A partner with three brands and an operator with
three thousand partners meet the same table. Check the empty state, the one-row
state and the ten-thousand-row state: filters, sort, pagination, bulk,
search-before-scroll, and what the default view shows when it is full.

**15 · Shared vocabulary, split meaning**
The same word means different things to each side — "programme", "partner",
"account", "campaign", "approved". Does this screen use the reader's meaning,
and does it stay consistent with what the other side will read in their own
copy of this event? Inconsistency here produces support tickets, not confusion.

## Using the list

- A finding may break more than one. Name the one that explains the user cost
  best, and mention the others in a clause.
- The five marketplace heuristics are not a bonus round. On any screen that
  touches money, programmes, permissions or another party's work, check them
  first — they produce the Blockers.
- Nothing on this list is about whether the design solves the right problem.
  That is `ux-critique`.
