#!/usr/bin/env python3
"""Validate ux-research-master: routing covers the pack, prompts match commands.

Usage (from repo root or this directory):
  python3 .agents/skills/ux-research-master/scripts/validate.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
AGENTS_SKILLS = SKILL_DIR.parent
COMMANDS = SKILL_DIR / "commands"
ROUTING = SKILL_DIR / "references" / "routing.md"
PROMPTS = SKILL_DIR / "references" / "prompts.md"
RULES = SKILL_DIR / "references" / "rules-block.md"
SCRIPT = SKILL_DIR / "scripts" / "install-master.sh"

# Routed by a master or by the installer path, not by a row of their own.
ROUTING_EXEMPT = {"ux-research-master"}


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def check_skill(errors: list[str]) -> None:
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    if "name: ux-research-master" not in text:
        fail(errors, "frontmatter name is not ux-research-master")
    if "stage: pipeline" not in text:
        fail(errors, "frontmatter stage should be pipeline")
    desc = re.search(r"description: >-\n((?:  .+\n)+)", text)
    if not desc:
        fail(errors, "description block missing")
    else:
        joined = " ".join(line.strip() for line in desc.group(1).splitlines())
        if len(joined) > 1024:
            fail(errors, f"description is {len(joined)} chars (max 1024)")
        for term in ("ux-research-master", "/ux", "install"):
            if term.lower() not in joined.lower():
                fail(errors, f"description missing trigger term: {term}")
    lines = len(text.splitlines())
    if lines > 500:
        fail(errors, f"SKILL.md is {lines} lines (keep under 500)")
    for needle in ("UX_MASTER_READY", "references/routing.md", "references/prompts.md"):
        if needle not in text:
            fail(errors, f"SKILL.md must reference {needle}")


def pack_skills() -> list[str]:
    return sorted(
        d.name for d in AGENTS_SKILLS.iterdir()
        if d.is_dir() and (d / "SKILL.md").is_file()
    )


def check_routing(errors: list[str]) -> None:
    if not ROUTING.is_file():
        fail(errors, "references/routing.md missing")
        return
    routing = ROUTING.read_text(encoding="utf-8")
    for name in pack_skills():
        if name in ROUTING_EXEMPT:
            continue
        if f"`{name}`" not in routing:
            fail(errors, f"routing.md never routes to `{name}`")
    if "{#connectors}" not in routing:
        fail(errors, "routing.md missing the #connectors anchor the SKILL.md links to")


def check_commands(errors: list[str]) -> None:
    if not COMMANDS.is_dir():
        fail(errors, "commands/ missing")
        return
    files = sorted(COMMANDS.glob("*.md"))
    if not files:
        fail(errors, "commands/ has no .md files")
        return
    prompts = PROMPTS.read_text(encoding="utf-8") if PROMPTS.is_file() else ""
    known = set(pack_skills())
    for f in files:
        body = f.read_text(encoding="utf-8")
        if not body.startswith("---\n"):
            fail(errors, f"{f.name} missing frontmatter")
            continue
        fm = body.split("---", 2)[1]
        if "description:" not in fm:
            fail(errors, f"{f.name} frontmatter missing description")
        for line in fm.splitlines():
            if ":" in line and not line.strip().startswith("#"):
                key, _, value = line.partition(":")
                value = value.strip()
                if value and value[0] in "[{&*!|>%@`" and not value.startswith('"'):
                    fail(errors, f"{f.name} frontmatter {key.strip()} needs quoting")
        if "<!-- managed by ux-research-master -->" not in body:
            fail(errors, f"{f.name} missing the managed marker (install cleanup relies on it)")
        if not f.name.startswith("ux"):
            fail(errors, f"{f.name} is not namespaced ux-*")
        slug = f.stem
        if prompts and f"/{slug}" not in prompts:
            fail(errors, f"prompts.md never mentions /{slug}")
        if slug != "ux":
            targets = re.findall(r"Read `\.agents/skills/([a-z0-9-]+)/SKILL\.md`", body)
            if not targets:
                fail(errors, f"{slug} does not say which skill to read")
            for t in targets:
                if t not in known:
                    fail(errors, f"{slug} points at unknown skill {t}")


def check_rules_and_script(errors: list[str]) -> None:
    if not RULES.is_file():
        fail(errors, "references/rules-block.md missing")
    else:
        block = RULES.read_text(encoding="utf-8")
        if "<!-- BEGIN ux-research-master" not in block or "<!-- END ux-research-master" not in block:
            fail(errors, "rules-block.md must carry both managed markers")
    if not SCRIPT.is_file():
        fail(errors, "scripts/install-master.sh missing")
        return
    body = SCRIPT.read_text(encoding="utf-8")
    if "UX_MASTER_READY" not in body:
        fail(errors, "install-master.sh must print UX_MASTER_READY")
    if "managed by ux-research-master" not in body:
        fail(errors, "install-master.sh must clean up stale marked commands")
    for needle in ("--target", "--project-only", "--global-only", "--no-rules",
                   "--skip-skills", "UX_SKIP_POST"):
        if needle not in body:
            fail(errors, f"install-master.sh missing {needle}")


def main() -> int:
    errors: list[str] = []
    check_skill(errors)
    check_routing(errors)
    check_commands(errors)
    check_rules_and_script(errors)

    print("UX research master — validator")
    print(f"  skill:    {SKILL_DIR / 'SKILL.md'}")
    print(f"  pack:     {len(pack_skills())} skills")
    print(f"  commands: {len(list(COMMANDS.glob('*.md'))) if COMMANDS.is_dir() else 0}")
    if errors:
        print(f"FAIL ({len(errors)})")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
