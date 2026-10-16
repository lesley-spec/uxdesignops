#!/usr/bin/env python3
"""Rebuild DesignOps Frame + Personas pages from a local clone of Nihal's ux-research.

Usage:
  gh repo clone nihal-somers-impact/ux-research /tmp/ux-research-nihal -- --depth 1
  python3 research-agent/publish_nihal_pages.py [/tmp/ux-research-nihal]
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOCS = REPO / "research-agent" / "docs" / "research"
FRAME_DIR = DOCS / "frame"
PERSONAS_DIR = DOCS / "personas"
PERSONAS_V1_DIR = DOCS / "personas-v1"
THEME_JS = DOCS / "shared" / "designops-theme.js"

sys.path.insert(0, str(REPO / "research-agent"))
from affinity_board import (  # noqa: E402
    designops_auth_gate_html,
    designops_auth_head_scripts,
    designops_theme_boot_script,
    report_nav_html,
)

FRAME_EXTRA_CSS = """
.research-subnav{display:none!important}
.frame-page .top-nav{position:sticky;top:0;z-index:50}
.frame-page .wrap{padding-top:8px}
"""

PERSONAS_EXTRA_CSS = """
.personas-page .top-nav{position:sticky;top:0;z-index:50}
"""

FRAME_SNAPSHOT_PATCH = r"""
    // Static snapshot fallback for GitHub Pages / local DesignOps
    window.__frameSnapshot=true;
    try{
      var base=new URL("./data/", window.location.href);
      var [cj,nj,pj]=await Promise.all([
        fetch(new URL("claims.json", base)).then(function(r){ if(!r.ok) throw new Error(r.status); return r.json(); }),
        fetch(new URL("needs.json", base)).then(function(r){ if(!r.ok) throw new Error(r.status); return r.json(); }),
        fetch(new URL("prompts.json", base)).then(function(r){ if(!r.ok) throw new Error(r.status); return r.json(); })
      ]);
      prompts=(pj||[]).filter(function(x){return x&&x.question});
      needs=(nj||[]).filter(function(n){return n&&n.need});
      renderStarters(); renderTabs(); renderJourney();
      apply({docs:(cj||[]).map(function(c){return {data:function(){return c}}})});
      $("asksec").hidden=false;
      $("askstamp").textContent="snapshot match — keyword Ask from claims";
    }catch(e){
      $("stamp").textContent="Snapshot missing";
      renderEmpty({t:"Cannot load Frame snapshot",b:"Expected ./data/claims.json, needs.json, and prompts.json next to this page."});
    }
"""


def load_collection(folder: Path) -> list:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(folder.glob("*.json"))]


def extract_nihal_parts(src_html: str) -> tuple[str, str, str]:
    title_m = re.search(r"<title>(.*?)</title>", src_html, re.S)
    title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip() if title_m else "Page"
    style_m = re.search(r"<style>(.*?)</style>", src_html, re.S)
    style = style_m.group(1) if style_m else ""
    body = src_html[style_m.end() :].strip() if style_m else src_html.strip()
    return title, style, body


def wrap_page(*, title: str, style: str, body: str, body_class: str, extra_css: str) -> str:
    nav = report_nav_html(
        "2026-08-24",
        "listing",
        listing_href="../research/",
        affinity_href="../reports/2026-08-24-affinity.html",
        skills_href="../skills/",
        pipeline_href="../",
        brand_href="../",
        usage_href="../usage/",
        personas_href="../personas/",
        walkthrough_href="../walkthroughs/",
        feed_href="../feed/",
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  {designops_theme_boot_script()}
  <title>{title} — UX DesignOps</title>
  <link rel="stylesheet" href="../shared/designops.css" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sarabun:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap">
  <style>
{style}
{extra_css}
  </style>
  {designops_auth_head_scripts()}
</head>
<body class="{body_class}">
  {designops_auth_gate_html()}
  {nav}
{body}
<script src="../shared/designops-theme.js"></script>
</body>
</html>
"""


def sync_frame_data(nihal: Path) -> None:
    src = nihal / "frame" / "data"
    dst = FRAME_DIR / "data"
    for name in ("claims", "needs", "prompts"):
        sdir, ddir = src / name, dst / name
        if ddir.exists():
            shutil.rmtree(ddir)
        shutil.copytree(sdir, ddir)
        aggregate = load_collection(ddir)
        (dst / f"{name}.json").write_text(
            json.dumps(aggregate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"  frame data/{name}.json → {len(aggregate)} rows")


def patch_frame_body(body: str) -> str:
    old = """    if(!db){
      $("stamp").textContent="Store unavailable";
      renderEmpty({t:"Cannot reach the claims store",b:"Sign in to view the Frame. The page itself holds no data."});
      return;
    }"""
    if "Static snapshot fallback" not in body:
        if old not in body:
            raise SystemExit("Frame snapshot patch anchor not found")
        body = body.replace(old, "    if(!db){\n" + FRAME_SNAPSHOT_PATCH + "\n      return;\n    }", 1)
    return body


def rebuild_frame(nihal: Path) -> None:
    src = (nihal / "frame" / "index.html").read_text(encoding="utf-8")
    (FRAME_DIR / "frame-src.html").write_text(src, encoding="utf-8")
    shutil.copy2(nihal / "frame" / "README.md", FRAME_DIR / "README.md")
    sync_frame_data(nihal)
    _title, style, body = extract_nihal_parts(src)
    body = patch_frame_body(body)
    out = wrap_page(
        title="The Frame",
        style=style,
        body=body,
        body_class="frame-page",
        extra_css=FRAME_EXTRA_CSS,
    )
    (FRAME_DIR / "index.html").write_text(out, encoding="utf-8")
    print(f"  wrote {FRAME_DIR / 'index.html'}")


def rebuild_personas(nihal: Path) -> None:
    if PERSONAS_DIR.exists() and not PERSONAS_V1_DIR.exists():
        cur = (PERSONAS_DIR / "index.html").read_text(encoding="utf-8")
        if "Aisha" in cur or "Affiliate & Creator" in cur:
            shutil.copytree(PERSONAS_DIR, PERSONAS_V1_DIR)
            print(f"  archived V1 → {PERSONAS_V1_DIR}")

    src = (nihal / "personas" / "index.html").read_text(encoding="utf-8")
    PERSONAS_DIR.mkdir(parents=True, exist_ok=True)
    (PERSONAS_DIR / "personas-src.html").write_text(src, encoding="utf-8")
    shutil.copy2(nihal / "personas" / "personas.md", PERSONAS_DIR / "personas.md")
    shutil.copy2(nihal / "personas" / "README.md", PERSONAS_DIR / "README.md")
    skill_ref = REPO / ".agents" / "skills" / "user-personas" / "references" / "personas.md"
    if skill_ref.parent.exists():
        shutil.copy2(nihal / "personas" / "personas.md", skill_ref)

    _title, style, body = extract_nihal_parts(src)
    out = wrap_page(
        title="User Personas",
        style=style,
        body=body,
        body_class="personas-page",
        extra_css=PERSONAS_EXTRA_CSS,
    )
    (PERSONAS_DIR / "index.html").write_text(out, encoding="utf-8")
    print(f"  wrote {PERSONAS_DIR / 'index.html'}")


def update_theme_nav() -> None:
    text = THEME_JS.read_text(encoding="utf-8")
    text = re.sub(
        r"var SUBNAV_ITEMS = \[[\s\S]*?\];",
        """var SUBNAV_ITEMS = [
    { key: "frame", label: "The Frame", path: "frame/" },
    { key: "personas", label: "Personas", path: "personas/" },
    { key: "listing", label: "Insight Monitor", path: "research/" },
    { key: "personas-v1", label: "Personas (archive)", path: "personas-v1/" },
    { key: "affinity", label: "Affinity", path: "reports/2026-08-24-affinity.html" },
    { key: "feed", label: "Competitor News", path: "feed/" },
  ];""",
        text,
        count=1,
    )
    if "personas-v1" not in text or "path.slice(-11)" not in text:
        text = text.replace(
            'if (/\\/personas(\\/|$)/.test(path) || path.slice(-8) === "personas") return "personas";',
            'if (/\\/personas-v1(\\/|$)/.test(path) || path.slice(-11) === "personas-v1") return "personas-v1";\n'
            '    if (/\\/personas(\\/|$)/.test(path) || path.slice(-8) === "personas") return "personas";',
            1,
        )
    THEME_JS.write_text(text, encoding="utf-8")
    print("  updated designops-theme.js")


def main() -> None:
    nihal = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/ux-research-nihal")
    if not (nihal / "frame" / "index.html").exists():
        raise SystemExit(f"Nihal frame not found at {nihal}/frame/index.html")
    print("→ Frame")
    rebuild_frame(nihal)
    print("→ Personas")
    rebuild_personas(nihal)
    print("→ Nav")
    update_theme_nav()
    print("Done. Re-apply extractive Ask patch in frame/index.html if regenerating from scratch.")


if __name__ == "__main__":
    main()
