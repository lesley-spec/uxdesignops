#!/usr/bin/env python3
"""Publish .agents/skills to GitHub Pages under docs/research/skills/."""

from __future__ import annotations

import json
import re
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(AGENT_DIR))
from affinity_board import designops_auth_gate_html, designops_auth_head_scripts, top_nav_brand_html

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_SRC = REPO_ROOT / ".agents" / "skills"
SKILLS_SITE = REPO_ROOT / "research-agent" / "docs" / "research" / "skills"
PACK_DIR = SKILLS_SITE / "pack"
ZIP_PATH = SKILLS_SITE / "designops-skills.zip"
INSTALL_SH = SKILLS_SITE / "install.sh"
MANIFEST_PATH = SKILLS_SITE / "manifest.json"

PAGES_BASE = "https://lesley-spec.github.io/uxdesignops/skills"
GITHUB_TREE = "https://github.com/lesley-spec/uxdesignops/tree/main/.agents/skills"

STAGE_ORDER = ("pipeline", "empathize", "define", "ideate", "prototype", "test")

STAGE_LABELS = {
    "pipeline": ("Start here", "master"),
    "empathize": ("Empathize", "stage 1"),
    "define": ("Define", "stage 2"),
    "ideate": ("Ideate", "stage 3"),
    "prototype": ("Prototype", "stage 4"),
    "test": ("Test", "stage 5"),
}

# Skills listed under each pipeline phase (includes cross-phase reuse).
STAGE_SKILLS: dict[str, list[str]] = {
    "pipeline": [
        "design-thinking-ux",
    ],
    "empathize": [
        "user-research",
        "research-synthesis",
        "synthesize-research",
        "data-analyze",
    ],
    "define": [
        "write-spec",
        "anti-sycophancy",
        "brand-operator-ux-persona",
        "creator-affiliate-ux-persona",
        "design-system",
    ],
    "ideate": [
        "ideate",
        "ux-critique",
        "prototype-handoff",
        "brand-operator-ux-persona",
        "creator-affiliate-ux-persona",
        "design-system",
    ],
    "prototype": [
        "brand-prototype",
        "partner-prototype",
        "design-system",
    ],
    "test": [
        "test-plan",
        "accessibility-review",
        "ux-critique",
        "test-loopback",
        "user-research",
        "synthesize-research",
        "brand-operator-ux-persona",
        "creator-affiliate-ux-persona",
    ],
}

USE_WHEN: dict[str, str] = {
    "design-thinking-ux": "Master skill — guided Empathize → Test; invokes phase skills",
    "user-research": "Deep-dive a finding, design a study, or post-session gate brief",
    "research-synthesis": "Triangulate PostHog + Pendo + Dovetail (+ Outset/Freshdesk)",
    "synthesize-research": "Affinity-map one corpus (Dovetail project, interview set, test export)",
    "data-analyze": "Ad-hoc PostHog / Pendo quantitative questions",
    "write-spec": "Confirmed research → one-pager + linked UX Epic / Confluence",
    "anti-sycophancy": "Pressure-test framing before Designer + PM review",
    "brand-operator-ux-persona": "Brand-side JTBD / operator lens",
    "creator-affiliate-ux-persona": "Partner / creator-affiliate lens",
    "design-system": "Styleguide + component library constraints",
    "ideate": "Framing → ideation brief + tool routing + starter directions",
    "ux-critique": "Coverage matrix: mocks/prototype vs spec (Ideate or Test pre-flight)",
    "prototype-handoff": "Exit pack after critique — ready for Prototype",
    "brand-prototype": "One prompt → Brand UI shell (<code>localhost:5174/one-program-1/</code>)",
    "partner-prototype": "One prompt → Partner UI shell (<code>localhost:5173/</code>)",
    "test-plan": "Synthetic pre-flight + Outset/Maze study draft",
    "accessibility-review": "Synthetic a11y check before recruiting",
    "test-loopback": "Publish Verified session findings → Empathize input",
}

STAGE_NOTES: dict[str, str] = {
    "pipeline": "Invoke <code>design-thinking-ux</code> first for a full run. It asks intake questions and loads the phase skill — you do not type each child skill unless you want a single step.",
    "prototype": "Prototype skills run <code>scripts/bootstrap.sh</code> — clone, <code>npm ci</code>, start Vite. Cursor preferred.",
    "test": "Human gate: review AI drafts before stakeholders. Findings loop back to Empathize.",
}


def parse_skill_frontmatter(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    meta: dict[str, str] = {}
    current_key: str | None = None
    in_metadata = False
    desc_lines: list[str] = []

    for line in block.splitlines():
        if line.strip() == "metadata:":
            in_metadata = True
            current_key = None
            continue
        if in_metadata:
            m = re.match(r"^\s{2}([\w-]+):\s*(.*)$", line)
            if m:
                current_key = m.group(1).replace("-", "_")
                val = m.group(2).strip()
                if val and val != ">-" and val != "|":
                    meta[current_key] = val
                continue
            if line.startswith("  ") and current_key:
                continue
            in_metadata = False
            current_key = None

        m = re.match(r"^([\w-]+):\s*(.*)$", line)
        if m:
            key = m.group(1).replace("-", "_")
            val = m.group(2).strip()
            current_key = key
            if key == "description":
                if val in {">-", "|"}:
                    desc_lines = []
                elif val:
                    meta["description"] = val
                    desc_lines = []
            elif val and val not in {">-", "|"}:
                meta[key] = val
            continue

        if current_key == "description" and line.startswith("  "):
            desc_lines.append(line.strip())

    if desc_lines and "description" not in meta:
        meta["description"] = " ".join(desc_lines)
    return meta


def skill_dirs() -> list[Path]:
    return sorted(
        p for p in SKILLS_SRC.iterdir()
        if p.is_dir() and (p / "SKILL.md").is_file()
    )


def copy_pack() -> None:
    if PACK_DIR.exists():
        shutil.rmtree(PACK_DIR)
    PACK_DIR.mkdir(parents=True)
    readme = SKILLS_SRC / "README.md"
    if readme.is_file():
        shutil.copy2(readme, PACK_DIR / "README.md")
    for skill in skill_dirs():
        shutil.copytree(skill, PACK_DIR / skill.name)


def build_manifest() -> dict:
    skills = []
    for skill in skill_dirs():
        meta = parse_skill_frontmatter(skill / "SKILL.md")
        skills.append(
            {
                "name": skill.name,
                "stage": meta.get("stage", "unknown"),
                "description": meta.get("description", ""),
                "figjam_agent": meta.get("figjam_agent", ""),
                "pack_url": f"{PAGES_BASE}/pack/{skill.name}/",
                "skill_md_url": f"{PAGES_BASE}/pack/{skill.name}/SKILL.md",
                "github_url": f"{GITHUB_TREE}/{skill.name}",
            }
        )
    skills.sort(key=lambda s: (STAGE_ORDER.index(s["stage"]) if s["stage"] in STAGE_ORDER else 99, s["name"]))
    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(skills),
        "download_zip": f"{PAGES_BASE}/designops-skills.zip",
        "install_script": f"{PAGES_BASE}/install.sh",
        "skills": skills,
    }


def build_zip() -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        readme = SKILLS_SRC / "README.md"
        if readme.is_file():
            zf.write(readme, "README.md")
        for skill in skill_dirs():
            for path in skill.rglob("*"):
                if path.is_file():
                    zf.write(path, f"{skill.name}/{path.relative_to(skill).as_posix()}")


def write_install_script() -> None:
    INSTALL_SH.write_text(
        """#!/usr/bin/env bash
# Install UX DesignOps agent skills into a project directory.
# Usage:
#   curl -fsSL https://lesley-spec.github.io/uxdesignops/skills/install.sh | bash -s -- cursor .
#   curl -fsSL https://lesley-spec.github.io/uxdesignops/skills/install.sh | bash -s -- claude ~/my-project
#   bash install.sh agents .

set -euo pipefail

HARNESS="${1:-agents}"
TARGET="${2:-.}"
ZIP_URL="${DESIGNOPS_SKILLS_ZIP:-https://lesley-spec.github.io/uxdesignops/skills/designops-skills.zip}"

case "$HARNESS" in
  cursor|Cursor) DEST_REL=".cursor/skills" ;;
  claude|Claude) DEST_REL=".claude/skills" ;;
  agents|copilot|codex|Agents) DEST_REL=".agents/skills" ;;
  *)
    echo "Unknown harness: $HARNESS" >&2
    echo "Use: cursor | claude | agents" >&2
    exit 1
    ;;
esac

TARGET="$(cd "$TARGET" && pwd)"
DEST="$TARGET/$DEST_REL"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "→ Downloading skills pack…"
if command -v curl >/dev/null 2>&1; then
  curl -fsSL "$ZIP_URL" -o "$TMP/skills.zip"
elif command -v wget >/dev/null 2>&1; then
  wget -qO "$TMP/skills.zip" "$ZIP_URL"
else
  echo "Need curl or wget to download the skills pack." >&2
  exit 1
fi

echo "→ Extracting to $DEST …"
mkdir -p "$DEST"
unzip -q "$TMP/skills.zip" -d "$TMP/extract"

count=0
for skill_dir in "$TMP/extract"/*/; do
  name="$(basename "$skill_dir")"
  [[ "$name" == "README.md" ]] && continue
  rm -rf "$DEST/$name"
  cp -R "$skill_dir" "$DEST/$name"
  count=$((count + 1))
done

echo "✓ Installed $count skills into $DEST ($HARNESS harness)"
echo "  Invoke in chat, e.g. use design-thinking-ux · use write-spec · use ideate · use test-plan"
""",
        encoding="utf-8",
    )
    INSTALL_SH.chmod(0o755)


def _esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_skills_index(manifest: dict) -> str:
    count = manifest["count"]
    by_name = {s["name"]: s for s in manifest["skills"]}
    seen_ids: set[str] = set()

    def skill_row(name: str) -> str:
        skill = by_name[name]
        row_id = ""
        if name not in seen_ids:
            row_id = f' id="{name}"'
            seen_ids.add(name)
        use_when = USE_WHEN.get(name, skill.get("description", ""))
        return (
            f"        <tr{row_id}>"
            f"<td><code>{_esc(name)}</code></td>"
            f"<td>{use_when}</td>"
            f'<td class="dl"><a href="./pack/{_esc(name)}/">Browse</a> · '
            f'<a href="./pack/{_esc(name)}/SKILL.md">SKILL.md</a></td>'
            f"</tr>\n"
        )

    stage_blocks = []
    auth_head_scripts = designops_auth_head_scripts(skills_page=True)
    auth_gate_html = designops_auth_gate_html()
    for stage in STAGE_ORDER:
        label, sub = STAGE_LABELS[stage]
        rows = "".join(skill_row(n) for n in STAGE_SKILLS[stage] if n in by_name)
        note = STAGE_NOTES.get(stage, "")
        note_html = f'    <p class="muted">{note}</p>\n' if note else ""
        stage_blocks.append(
            f"""    <h2 id="{stage}">{label} ({sub})</h2>
    <table class="skills-table">
      <thead><tr><th>Skill</th><th>Use when</th><th>Download</th></tr></thead>
      <tbody>
{rows}      </tbody>
    </table>
{note_html}"""
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <script>(function(){{var k="ux-designops-theme",s=localStorage.getItem(k),d=s==="dark"||(s!=="light"&&window.matchMedia("(prefers-color-scheme: dark)").matches);document.documentElement.setAttribute("data-theme",d?"dark":"light");}})();</script>
  <script>(function(){{try{{var k="theme",s=localStorage.getItem(k),d;if(s==="dark")d=true;else if(s==="light")d=false;else d=window.matchMedia("(prefers-color-scheme: dark)").matches;var e=document.documentElement;if(d)e.classList.add("dark");else e.classList.remove("dark");e.style.colorScheme=d?"dark":"light";}}catch(x){{}}}})();</script>
  <title>UX DesignOps — Agent Skills</title>
  <link rel="stylesheet" href="../shared/designops.css" />
  {auth_head_scripts}
</head>
<body class="skills-page">
  {auth_gate_html}
  <header class="top-nav" role="banner">
    <div class="top-nav-inner">
      {top_nav_brand_html("../")}
      <div class="top-nav-actions">
        <nav class="report-nav" aria-label="Site sections">
          <a class="nav-link" href="../" data-nav="pipeline">Design Thinking Pipeline</a>
          <a class="nav-link" href="../research/" data-nav="listing">Research</a>
          <a class="nav-link" href="../reports/2026-08-24-affinity.html" data-nav="affinity">Affinity</a>
          <a class="nav-link is-active" href="./" data-nav="skills">Skills</a>
        </nav>
        <button type="button" class="theme-toggle" id="theme-toggle" aria-label="Toggle theme">
          <svg class="theme-icon theme-icon-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
          <svg class="theme-icon theme-icon-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>
        </button>
      </div>
    </div>
  </header>

  <main class="wrap">
    <header class="page-header">
      <h1>Agent Skills</h1>
      <p class="sub muted"><strong>{count} portable skills</strong> — start with the master skill
        <code>design-thinking-ux</code>, which invokes Empathize through Test.
        Download the full pack below — no repo clone required.</p>
    </header>

    <aside class="walkthrough-banner is-master">
      <p><strong>Master skill.</strong> Start every full run with <code>use design-thinking-ux</code> (Design Thinking UX). It asks intake questions and invokes Empathize → Define → Ideate → Prototype → Test. Phase skills below still work on their own.</p>
      <a href="#design-thinking-ux">See design-thinking-ux</a>
    </aside>

    <section class="skills-download" id="install" aria-labelledby="install-heading">
      <h2 id="install-heading">Download all skills</h2>
      <div class="skills-download-grid">
        <div class="skills-download-card">
          <h3>Zip pack</h3>
          <p class="muted">All {count} skills — Empathize through Test.</p>
          <a class="skills-btn skills-btn-primary" href="./designops-skills.zip" download>Download designops-skills.zip</a>
        </div>
        <div class="skills-download-card">
          <h3>One-command install</h3>
          <p class="muted">Pick your harness; installs every skill into your project.</p>
          <div class="skills-install-tabs" role="tablist" aria-label="Harness">
            <button type="button" class="skills-tab is-active" data-harness="cursor" role="tab" aria-selected="true">Cursor</button>
            <button type="button" class="skills-tab" data-harness="claude" role="tab" aria-selected="false">Claude</button>
            <button type="button" class="skills-tab" data-harness="agents" role="tab" aria-selected="false">Copilot / Codex</button>
          </div>
          <pre class="skills-cmd" id="install-cmd">curl -fsSL https://lesley-spec.github.io/uxdesignops/skills/install.sh | bash -s -- cursor .</pre>
          <button type="button" class="skills-btn skills-btn-secondary" id="copy-install-cmd">Copy command</button>
        </div>
      </div>
      <table class="skills-table skills-harness-table">
        <thead><tr><th>Harness</th><th>Install path</th><th>Skills installed</th></tr></thead>
        <tbody>
          <tr><td>Cursor</td><td><code>.cursor/skills/&lt;name&gt;/</code></td><td>{count} (all phases)</td></tr>
          <tr><td>Claude Code</td><td><code>.claude/skills/&lt;name&gt;/</code></td><td>{count} (all phases)</td></tr>
          <tr><td>Copilot / Codex</td><td><code>.agents/skills/&lt;name&gt;/</code></td><td>{count} (all phases)</td></tr>
        </tbody>
      </table>
      <p class="muted">Start a full run with <code>use design-thinking-ux</code>, or invoke a phase skill
        (<code>use write-spec</code>, <code>use ideate</code>, <code>use test-plan</code>).
        Persona and design-system skills appear in multiple phases — install once, reuse everywhere.
        <a href="./pack/README.md">Pack README</a> · <a href="./manifest.json">manifest.json</a></p>
    </section>

    <div class="skills-jump">
      <strong>Jump:</strong>
      <a href="#install">Install</a> ·
      <a href="#pipeline">Start here</a> ·
      <a href="#empathize">Empathize</a> ·
      <a href="#define">Define</a> ·
      <a href="#ideate">Ideate</a> ·
      <a href="#prototype">Prototype</a> ·
      <a href="#test">Test</a>
    </div>

{chr(10).join(stage_blocks)}
  </main>
  <script src="../shared/designops-theme.js"></script>
  <script>
    (function () {{
      var tabs = document.querySelectorAll(".skills-tab");
      var cmd = document.getElementById("install-cmd");
      var copyBtn = document.getElementById("copy-install-cmd");
      var commands = {{
        cursor: "curl -fsSL https://lesley-spec.github.io/uxdesignops/skills/install.sh | bash -s -- cursor .",
        claude: "curl -fsSL https://lesley-spec.github.io/uxdesignops/skills/install.sh | bash -s -- claude .",
        agents: "curl -fsSL https://lesley-spec.github.io/uxdesignops/skills/install.sh | bash -s -- agents ."
      }};
      tabs.forEach(function (tab) {{
        tab.addEventListener("click", function () {{
          tabs.forEach(function (t) {{
            t.classList.remove("is-active");
            t.setAttribute("aria-selected", "false");
          }});
          tab.classList.add("is-active");
          tab.setAttribute("aria-selected", "true");
          cmd.textContent = commands[tab.dataset.harness];
        }});
      }});
      if (copyBtn && cmd) {{
        copyBtn.addEventListener("click", function () {{
          navigator.clipboard.writeText(cmd.textContent).then(function () {{
            copyBtn.textContent = "Copied!";
            setTimeout(function () {{ copyBtn.textContent = "Copy command"; }}, 1500);
          }});
        }});
      }}
    }})();
  </script>
</body>
</html>
"""


def main() -> None:
    SKILLS_SITE.mkdir(parents=True, exist_ok=True)
    copy_pack()
    build_zip()
    write_install_script()
    manifest = build_manifest()
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    index_path = SKILLS_SITE / "index.html"
    index_path.write_text(render_skills_index(manifest), encoding="utf-8")
    print(f"  ✅ Skills pack: {PACK_DIR} ({manifest['count']} skills)")
    print(f"  ✅ Zip: {ZIP_PATH}")
    print(f"  ✅ Install script: {INSTALL_SH}")
    print(f"  ✅ Manifest: {MANIFEST_PATH}")
    print(f"  ✅ Skills page: {index_path}")


if __name__ == "__main__":
    main()
