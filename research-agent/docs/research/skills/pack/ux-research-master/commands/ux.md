---
description: "Show the UX pack menu and route what you're working on"
argument-hint: "[what you're working on]"
---

Load the `ux-research-master` skill.

If the pack is not installed yet (no `.claude/commands/ux-frame.md`, or no
routing block in `CLAUDE.md`), run its first-run install, then print the menu.

Otherwise: if `$ARGUMENTS` is empty, print the starter-prompt menu from
`references/prompts.md` and stop. If `$ARGUMENTS` says something, skip the
menu — route it with `references/routing.md`, name the pick in one line, and
run that skill.
