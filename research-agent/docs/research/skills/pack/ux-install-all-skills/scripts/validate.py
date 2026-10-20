#!/usr/bin/env python3
"""Validate ux-install-all-skills can install the 37 pipeline skills.

Usage (from repo root or this directory):
  python3 .agents/skills/ux-install-all-skills/scripts/validate.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
AGENTS_SKILLS = SKILL_DIR.parent
SCRIPT = SKILL_DIR / "scripts" / "install-all.sh"
CATALOG = SKILL_DIR / "references" / "catalog.md"

PIPELINE_SKILLS = [
    "design-thinking-ux",
    "ux-research",
    "assumption-mapper",
    "research-intake",
    "user-context",
    "user-personas",
    "research-planner",
    "research-builder",
    "study-summary",
    "competitive-analysis",
    "frame-maintenance",
    "user-research",
    "research-synthesis",
    "synthesize-research",
    "data-analyze",
    "write-spec",
    "anti-sycophancy",
    "brand-operator-ux-persona",
    "creator-affiliate-ux-persona",
    "design-system",
    "measurable-check",
    "panel-planner",
    "ideate",
    "talk-to-users",
    "ux-critique",
    "prototype-handoff",
    "ux-prototyping",
    "brand-prototype",
    "partner-prototype",
    "heuristic-evaluation",
    "persona-check",
    "test-plan",
    "accessibility-review",
    "test-loopback",
    "findings-publish",
    "ab-test-planner",
    "adoption-check",
]


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def check_frontmatter(errors: list[str]) -> None:
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    if "name: ux-install-all-skills" not in text:
        fail(errors, "frontmatter name is not ux-install-all-skills")
    if "stage: pipeline" not in text:
        fail(errors, "frontmatter stage should be pipeline")
    desc = re.search(r"description: >-\n((?:  .+\n)+)", text)
    if not desc:
        fail(errors, "description block missing")
    else:
        joined = " ".join(line.strip() for line in desc.group(1).splitlines())
        if len(joined) > 1024:
            fail(errors, f"description is {len(joined)} chars (max 1024)")
        for term in ("ux-install-all-skills", "37", "design thinking"):
            if term.lower() not in joined.lower():
                fail(errors, f"description missing trigger term: {term}")
    lines = len(text.splitlines())
    if lines > 500:
        fail(errors, f"SKILL.md is {lines} lines (keep under 500)")
    if "Do not start the pipeline" not in text:
        fail(errors, "SKILL.md missing do-not-auto-start integrity")
    if "IMPACT_SKILLS_READY" not in text:
        fail(errors, "SKILL.md must tell the agent to parse IMPACT_SKILLS_READY")


def check_catalog_and_siblings(errors: list[str]) -> None:
    if not CATALOG.is_file():
        fail(errors, "references/catalog.md missing")
        return
    catalog = CATALOG.read_text(encoding="utf-8")
    for name in PIPELINE_SKILLS:
        if f"`{name}`" not in catalog:
            fail(errors, f"catalog.md missing `{name}`")
        path = AGENTS_SKILLS / name / "SKILL.md"
        if not path.is_file():
            fail(errors, f"missing pipeline skill {name}: {path}")
    named = re.findall(r"`([a-z0-9-]+)`", catalog)
    unique = [n for n in dict.fromkeys(named) if n in PIPELINE_SKILLS or n == "ux-install-all-skills"]
    pipeline_in_catalog = [n for n in unique if n in PIPELINE_SKILLS]
    if len(pipeline_in_catalog) != 37:
        fail(errors, f"catalog should name 37 pipeline skills, found {len(pipeline_in_catalog)}")


def check_script(errors: list[str]) -> None:
    if not SCRIPT.is_file():
        fail(errors, "scripts/install-all.sh missing")
        return
    body = SCRIPT.read_text(encoding="utf-8")
    if "IMPACT_SKILLS_READY" not in body:
        fail(errors, "install-all.sh must print IMPACT_SKILLS_READY")
    if "pipeline=37" not in body:
        fail(errors, "install-all.sh must report pipeline=37")
    for name in PIPELINE_SKILLS:
        if name not in body:
            fail(errors, f"install-all.sh missing required skill {name}")
    for needle in ("--project-only", "--global-only", "--target", "${HOME}/.cursor/skills", "${HOME}/.claude/skills"):
        if needle not in body:
            fail(errors, f"install-all.sh missing {needle}")


def main() -> int:
    errors: list[str] = []
    check_frontmatter(errors)
    check_catalog_and_siblings(errors)
    check_script(errors)

    print("UX install all skills — validator")
    print(f"  skill: {SKILL_DIR / 'SKILL.md'}")
    print(f"  pipeline: {len(PIPELINE_SKILLS)}")
    if errors:
        print(f"FAIL ({len(errors)})")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
