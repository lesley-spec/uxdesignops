#!/usr/bin/env python3
"""Validate Design Thinking UX can orchestrate Empathize → Test.

Checks child-skill files, markdown links, landing-phase routing, and the
UPS Step 2 invoke sequence (the repo's documented full-pipeline fixture).
Does not publish Jira/Confluence or clone prototype shells.

Usage (from repo root or this directory):
  python3 .agents/skills/design-thinking-ux/scripts/validate.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
AGENTS_SKILLS = SKILL_DIR.parent
REPO_ROOT = AGENTS_SKILLS.parent

CHILD_SKILLS = [
    "data-analyze",
    "research-synthesis",
    "synthesize-research",
    "user-research",
    "write-spec",
    "anti-sycophancy",
    "brand-operator-ux-persona",
    "creator-affiliate-ux-persona",
    "design-system",
    "ideate",
    "ux-critique",
    "prototype-handoff",
    "brand-prototype",
    "partner-prototype",
    "test-plan",
    "accessibility-review",
    "test-loopback",
]

# Landing-phase table from references/phases.md
LANDING = [
    ("hunch_only", "Empathize"),
    ("confirmed_research", "Define"),
    ("one_pager", "Ideate"),
    ("chosen_mocks", "Prototype"),
    ("prototype_url", "Test"),
    ("session_notes", "Test"),
]

# UPS Step 2 (Partner, start from scratch) — expected primary invokes per phase.
# Lenses listed where the orchestrator must also load them.
UPS_SEQUENCE = [
    (
        "Empathize",
        ["data-analyze", "research-synthesis", "user-research"],
        "problem worth solving",
        "Define",
    ),
    (
        "Define",
        [
            "write-spec",
            "anti-sycophancy",
            "creator-affiliate-ux-persona",
            "design-system",
        ],
        "Designer + PM",
        "Ideate",
    ),
    (
        "Ideate",
        ["ideate", "ux-critique", "prototype-handoff"],
        "critique + chosen direction",
        "Prototype",
    ),
    (
        "Prototype",
        ["partner-prototype", "design-system"],
        "runnable URL",
        "Test",
    ),
    (
        "Test",
        ["test-plan", "ux-critique", "accessibility-review"],
        "study reviewed",
        None,
    ),
]


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def check_master_frontmatter(errors: list[str]) -> None:
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---"):
        fail(errors, "SKILL.md missing YAML frontmatter")
        return
    if "name: design-thinking-ux" not in text:
        fail(errors, "frontmatter name is not design-thinking-ux")
    if "stage: pipeline" not in text:
        fail(errors, "frontmatter stage should be pipeline")
    if "Design Thinking UX" not in text:
        fail(errors, "body should use display name Design Thinking UX")
    desc = re.search(r"description: >-\n((?:  .+\n)+)", text)
    if not desc:
        fail(errors, "description block missing")
    else:
        joined = " ".join(line.strip() for line in desc.group(1).splitlines())
        if len(joined) > 1024:
            fail(errors, f"description is {len(joined)} chars (max 1024)")
        for term in ("Design Thinking UX", "Empathize", "Test", "design-thinking-ux"):
            if term not in joined:
                fail(errors, f"description missing trigger term: {term}")
    lines = len(text.splitlines())
    if lines > 500:
        fail(errors, f"SKILL.md is {lines} lines (keep under 500)")


def check_child_skills(errors: list[str]) -> None:
    for name in CHILD_SKILLS:
        path = AGENTS_SKILLS / name / "SKILL.md"
        if not path.is_file():
            fail(errors, f"missing child skill {name}: {path}")
            continue
        body = path.read_text(encoding="utf-8")
        if f"name: {name}" not in body:
            fail(errors, f"{name}/SKILL.md name frontmatter mismatch")
        for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", body):
            href = m.group(2)
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = (path.parent / href).resolve()
            if not target.exists():
                fail(errors, f"{name}: broken link {href}")


def check_master_links(errors: list[str]) -> None:
    skill_md = SKILL_DIR / "SKILL.md"
    phases = SKILL_DIR / "references" / "phases.md"
    if not phases.is_file():
        fail(errors, "references/phases.md missing")
        return
    for path in (skill_md, phases):
        text = path.read_text(encoding="utf-8")
        for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
            href = m.group(2)
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = (path.parent / href).resolve()
            if not target.exists():
                fail(errors, f"{path.name}: broken link {href}")
    phases_text = phases.read_text(encoding="utf-8")
    for name in CHILD_SKILLS:
        if f"`{name}`" not in phases_text:
            fail(errors, f"phases.md does not mention `{name}`")


def check_landing_table(errors: list[str]) -> None:
    text = (SKILL_DIR / "references" / "phases.md").read_text(encoding="utf-8")
    expected = {
        "Topic / hunch / monitor finding only": "Empathize",
        "Confirmed problem + research": "Define",
        "One-pager / PRD / epic": "Ideate",
        "Chosen mocks": "Prototype",
        "Runnable prototype URL": "Test",
        "Completed Outset/Maze": "Test",
    }
    for needle, phase in expected.items():
        if needle not in text:
            fail(errors, f"landing table missing row for {needle!r}")
        elif phase not in text:
            fail(errors, f"landing table missing phase {phase} near {needle!r}")


def check_ups_sequence(errors: list[str]) -> None:
    """Dry-run: every UPS invoke is a real skill the orchestrator can Read."""
    invoked: list[str] = []
    for phase, skills, gate, nxt in UPS_SEQUENCE:
        for name in skills:
            path = AGENTS_SKILLS / name / "SKILL.md"
            if not path.is_file():
                fail(errors, f"UPS {phase}: cannot invoke {name}")
                continue
            invoked.append(f"{phase}:{name}")
            # Orchestrator must not skip the child's stop language.
            body = path.read_text(encoding="utf-8").lower()
            if name == "write-spec" and "confirm" not in body:
                fail(errors, "write-spec lost confirm-before-publish gate")
            if name == "test-plan" and "do not publish" not in body and "designer review" not in body:
                fail(errors, "test-plan lost human review gate")
            if name == "test-loopback" and "confirm" not in body:
                fail(errors, "test-loopback lost confirm-before-publish gate")
        if not gate:
            fail(errors, f"UPS {phase}: missing gate")
        if phase != "Test" and not nxt:
            fail(errors, f"UPS {phase}: missing next-phase entice")
    if len(invoked) < 14:
        fail(errors, f"UPS sequence too short ({len(invoked)} invokes)")


def check_anti_auto_advance(errors: list[str]) -> None:
    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    for phrase in (
        "Do not auto-advance",
        "Honor the child’s stop",
        "Do not ask the designer to type",
        "Join anywhere",
    ):
        if phrase not in text:
            fail(errors, f"orchestrator missing integrity phrase: {phrase}")


def main() -> int:
    errors: list[str] = []
    check_master_frontmatter(errors)
    check_child_skills(errors)
    check_master_links(errors)
    check_landing_table(errors)
    check_ups_sequence(errors)
    check_anti_auto_advance(errors)

    print("Design Thinking UX — pipeline validator")
    print(f"  master: {SKILL_DIR / 'SKILL.md'}")
    print(f"  children: {len(CHILD_SKILLS)}")
    print(f"  landing fixtures: {len(LANDING)}")
    print(f"  UPS phases: {len(UPS_SEQUENCE)}")
    if errors:
        print(f"FAIL ({len(errors)})")
        for e in errors:
            print(f"  - {e}")
        return 1

    print()
    print("# Design Thinking UX — UPS Step 2 (dry run)")
    print("Audience: Partner")
    print("Phase: Test")
    print("Status: READY FOR NEXT (loopback skipped — no real sessions)")
    print()
    print("| Phase | Status | Invoked | Gate |")
    print("|---|---|---|---|")
    for phase, skills, gate, nxt in UPS_SEQUENCE:
        nxt_note = f" → offer {nxt}" if nxt else " → end (no test-loopback without sessions)"
        print(f"| {phase} | done | {', '.join('`' + s + '`' for s in skills)} | {gate}{nxt_note} |")
    print()
    print("PASS — all child skills load; UPS Empathize→Test sequence is invocable; gates intact.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
