# The routing rule block

A skill cannot listen passively — it loads when its description matches or
when it is named. To get *"just chat and the right skill shows up"*, the
install writes a short routing block into the project's agent rule files,
which every turn sees.

## Where it goes

| File | Read by |
|---|---|
| `CLAUDE.md` (project root) | Claude Code, Claude desktop |
| `AGENTS.md` (project root) | Cursor, Codex, Copilot, any AGENTS.md-aware agent |

Both get the **same** block, verbatim from
[rules-block.md](rules-block.md). Nothing else in either file is touched.

## How it stays idempotent

The block is fenced by HTML comments:

```
<!-- BEGIN ux-research-master (managed — edit the skill, not this block) -->
…
<!-- END ux-research-master -->
```

`install-master.sh` replaces whatever sits between the markers and appends the
block when the markers are absent. Re-running the installer never duplicates
it. Hand-edits inside the markers are overwritten on the next install — change
`rules-block.md` in the skill instead.

## Opting out

- `--no-rules` on the installer writes skills and commands but leaves the rule
  files alone.
- Deleting the block (markers included) is enough; nothing re-adds it until
  the installer runs again.
- On a shared repo where `CLAUDE.md` is reviewed, run with `--no-rules` and
  raise the block as its own PR.

## Why a block and not a long preamble

Rule files are read on every turn in every session. The block is kept to one
screen: a routing table, four standing constraints, and a pointer to
`routing.md` for the detail. Anything longer competes with the project's own
instructions for attention and gets skimmed.
