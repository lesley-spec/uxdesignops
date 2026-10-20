# Output template

Short in the reply. The full pass goes in the artifact if they ask for it.

## In the reply

```
Heuristic review — <screen / flow>  ·  <brand | partner>  ·  Expert judgement (AI)
Task reviewed against: <the one job this screen exists to do>

BLOCKER  Money legibility
  Payout shows "Pending" with no date and no period.
  → A partner checking whether last month cleared cannot tell, and raises a ticket.
  Fix: show the period and the expected date beside the amount.

MAJOR  Two-sided consequence
  Pausing a programme confirms "Pause?" with no mention of live partners.
  → The operator pauses without knowing 40 partners lose attribution tonight.
  Fix: name the count and when partners are notified, in the confirm.

MAJOR  Error prevention
  ...

Minor (3): filter state lost on back · sort resets on refresh · "Save" and
"Apply" both present with different meanings
Cosmetic (5): mixed button styles, inconsistent date formats, …

Not assessable from a static frame: loading states, error states, bulk
behaviour over ~50 rows.

Three of these touch claims we already hold — want me to check them against
`user-context`?
```

## Rules for the write-up

- **Blockers and Majors get the three lines**: what breaks, what the person
  does, the fix. Minors and Cosmetics get one line each, Cosmetics collapsed
  when there are more than three.
- **Predicted behaviour, always.** "A partner at this step likely…", never
  "users struggle".
- **Name what you could not see.** A static frame hides states; say which
  findings are unverifiable and which states you never saw.
- **Expert judgement (AI)** rides along with every finding that leaves the
  chat — into Confluence, a ticket, a readout or a deck.
- **No scores.** No "7/10 usability", no heuristic pass rates. A count of
  violations is not a measurement and invites comparison between screens that
  were never comparable.

## When it travels

| Going to | Carry |
|---|---|
| A ticket | The finding, the heuristic, the fix, the label. Not the whole pass |
| `test-plan` | The unresolved Blockers and Majors as tasks to watch someone attempt |
| `user-context` | Only after the cross-check, and only as a hypothesis unless a study confirmed it |
| A readout | The label, prominently. A heuristic review in a findings deck without it is the failure this skill guards against |
