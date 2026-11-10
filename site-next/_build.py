#!/usr/bin/env python3
"""Write the preview pages. Not part of the live site."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

NAV = [
    ("Get started", [
        ("expect", "What to expect", "index.html", False),
        ("home", "Overview", "overview/index.html", False),
        ("start", "Install", "get-started/index.html", False),
    ]),
    ("Agents", [
        ("agents", "All agents", "agents/index.html", False),
        ("designer", "UX designer", "agents/designer/index.html", True),
        ("researcher", "UX researcher", "agents/researcher/index.html", True),
        ("pipeline", "Design thinking", "agents/pipeline/index.html", True),
    ]),
    ("Skills", [
        ("skills", "All skills", "skills/index.html", False),
    ]),
    ("Foundations", [
        ("foundations", "The pipeline", "foundations/index.html", False),
    ]),
    ("Styles", [
        ("styles", "Design tokens", "styles/index.html", False),
        ("color", "Color", "styles/color/index.html", True),
        ("type", "Type", "styles/type/index.html", True),
        ("space", "Space", "styles/space/index.html", True),
        ("primitives", "Primitives", "styles/primitives/index.html", True),
        ("layout", "Layout", "styles/layout/index.html", True),
    ]),
]

DEPTH = {
    "home": 1,
    "expect": 0,
    "start": 1,
    "foundations": 1,
    "styles": 1,
    "color": 2,
    "type": 2,
    "space": 2,
    "primitives": 2,
    "layout": 2,
    "agents": 1,
    "designer": 2,
    "researcher": 2,
    "pipeline": 2,
    "skills": 1,
}

CURSOR = """Install the impact.com UX skills for me. Clone https://github.com/lesley-spec/uxdesignops and copy every folder in .agents/skills that contains a SKILL.md into ~/.cursor/skills/, replacing any existing copy of those skills. Do not add a team marketplace."""

CLAUDE = """Install the impact.com UX skills for me. Clone https://github.com/lesley-spec/uxdesignops and copy every folder in .agents/skills that contains a SKILL.md into ~/.claude/skills/, replacing any existing copy of those skills."""

DESIGNER = """You are the UX designer. Brand. Christine’s welcome header doesn’t say what to do with 35 new applications. Put three variations on the Styleguide V2 sandbox page. Clone the closest example. Use only Styleguide V2 components and tokens."""

RESEARCH = """use ux-research. What do we already know about how brand operators review new partner applications, and what would we still need to learn?"""

PIPELINE = "use design-thinking-ux"


def rel(depth, href):
    return "../" * depth + href


def spec(label, text):
    escaped = text.replace("&", "&amp;").replace("<", "&lt;")
    return f"""<figure class="spec"><div class="spec-top"><span>{label}</span><button type="button" class="copy">Copy</button></div><pre>{escaped}</pre></figure>"""


def logo_markup():
    svg = (ROOT / "assets" / "impact-logo.svg").read_text().strip()
    return svg


# Skills the agents run. Each one can still be called by name.
# Designer is the screen package. Researcher is the research package.
# Design thinking calls the researcher for Empathize, then the phase skills.
SKILLS = {
    "assumption-mapper": ("Assumption mapper", "Pull the untested guesses out of a brief and rank them."),
    "research-intake": ("Research intake", "Sort a research request. Some of them close here."),
    "user-context": ("User context", "What the Frame already says, and how sure we are."),
    "user-personas": ("User personas", "The partner and brand persona set."),
    "research-planner": ("Research planner", "Turn a routed request into a study worth running."),
    "panel-planner": ("Panel planner", "Who to talk to, from a Rally export."),
    "research-builder": ("Research builder", "The guide, the in-product prompt, the interview, the audience."),
    "user-research": ("User research", "A study plan, a deep dive, or the problem-worth-solving gate."),
    "study-summary": ("Study summary", "What a pile of raw research actually supports."),
    "competitive-analysis": ("Competitive analysis", "How other platforms handle the same job."),
    "frame-maintenance": ("Frame maintenance", "Is the Frame still true?"),
    "research-synthesis": ("Research synthesis", "Read several live sources together."),
    "synthesize-research": ("Synthesize research", "Themes from one study or one corpus."),
    "data-analyze": ("Data analyze", "A PostHog or Pendo question."),
    "findings-publish": ("Findings publish", "A finished study, written up for the people who read it."),
    "adoption-check": ("Adoption check", "After something ships, did the research hold?"),
    "measurable-check": ("Measurable check", "Can we measure this at all?"),
    "talk-to-users": ("Talk to users", "Where a question should go: personas, evidence, or fieldwork."),
    "heuristic-evaluation": ("Heuristic evaluation", "An expert review of a screen, before anyone is recruited."),
    "persona-check": ("Persona check", "Walk a design through a persona as a task."),
    "ab-test-planner": ("A/B test planner", "Size and plan a live experiment."),
    "brand-operator-ux-persona": ("Brand operator", "The job on the brand side."),
    "creator-affiliate-ux-persona": ("Creator and affiliate", "The job on the partner side."),
    "design-system": ("Design system", "Styleguide V2, the components, and the tokens."),
    "ux-critique": ("UX critique", "Check a direction against the one-pager, PRD, or epic."),
    "ux-prototyping": ("UX prototyping", "Orchestrator. A Brand or Partner screen you can click, in this chat."),
    "brand-prototype": ("Brand prototype", "The Brand UI shell."),
    "partner-prototype": ("Partner prototype", "The Partner UI shell."),
    "write-spec": ("Write a spec", "A one-pager and a linked UX epic."),
    "anti-sycophancy": ("Anti-sycophancy", "Pressure-test the framing before it hardens."),
    "ideate": ("Ideate", "A few directions from a one-pager, a ticket, or notes."),
    "prototype-handoff": ("Prototype handoff", "The pack for the direction you chose."),
    "test-plan": ("Test plan", "A usability study from a prototype and its success criteria."),
    "accessibility-review": ("Accessibility review", "A synthetic accessibility pass before sessions."),
    "test-loopback": ("Test loopback", "The older publish path. Findings publish replaces it."),
    "ux-designer": ("UX designer", "Orchestrator. The front door. Asks what you are doing, then runs a screen or a new project."),
    "ux-research": ("UX research", "Orchestrator. Routes a research request through intake, the Frame, and the planning skills."),
    "design-thinking-ux": ("Design thinking", "Orchestrator. Walks a project from Empathize to Test and waits at each gate."),
}

# Orchestrators run other skills in order. Each one is also callable by name.
ORCHESTRATORS = ["ux-designer", "ux-research", "design-thinking-ux", "ux-prototyping"]

# The agent page that runs each orchestrator, and the skills it runs.
ORCHESTRATOR_AGENT = {
    "ux-designer": "designer",
    "ux-research": "researcher",
    "design-thinking-ux": "pipeline",
}

DESIGNER_RUNS = [
    "user-personas",
    "brand-operator-ux-persona",
    "creator-affiliate-ux-persona",
    "design-system",
    "ux-critique",
    "ux-prototyping",
    "brand-prototype",
    "partner-prototype",
]

RESEARCHER_RUNS = [
    "assumption-mapper",
    "research-intake",
    "user-context",
    "user-personas",
    "measurable-check",
    "research-planner",
    "panel-planner",
    "research-builder",
    "data-analyze",
    "research-synthesis",
    "synthesize-research",
    "study-summary",
    "user-research",
    "findings-publish",
    "adoption-check",
    "frame-maintenance",
]

RESEARCHER_LENSES = [
    "competitive-analysis",
    "talk-to-users",
    "heuristic-evaluation",
    "persona-check",
    "ab-test-planner",
]

PIPELINE_PHASES = [
    ("Define", ["write-spec", "anti-sycophancy", "brand-operator-ux-persona", "creator-affiliate-ux-persona", "design-system"]),
    ("Ideate", ["ideate", "talk-to-users", "ux-critique", "prototype-handoff"]),
    ("Prototype", ["ux-prototyping", "brand-prototype", "partner-prototype", "design-system", "heuristic-evaluation", "persona-check"]),
    ("Test", ["test-plan", "accessibility-review", "synthesize-research", "findings-publish", "test-loopback"]),
]

AGENT_LINKS = {
    "designer": ("UX designer", "agents/designer/index.html"),
    "researcher": ("UX researcher", "agents/researcher/index.html"),
    "pipeline": ("Design thinking", "agents/pipeline/index.html"),
}


def skill_href(depth, slug):
    return rel(depth, f"skills/{slug}/index.html")


def chip(slug, depth):
    return f'<a class="skill" href="{skill_href(depth, slug)}">{slug}</a>'


def skill_rows(slugs, depth):
    rows = []
    for slug in slugs:
        title, blurb = SKILLS[slug]
        rows.append(
            f'<a class="skill-row" href="{skill_href(depth, slug)}">'
            f'<span class="skill">{slug}</span>'
            f'<span class="skill-blurb"><b>{title}</b>{blurb}</span></a>'
        )
    return f'<div class="skill-rows">{"".join(rows)}</div>'


def agents_for(slug):
    found = []
    if slug in DESIGNER_RUNS:
        found.append("designer")
    if slug in RESEARCHER_RUNS or slug in RESEARCHER_LENSES:
        found.append("researcher")
    if any(slug in group for _, group in PIPELINE_PHASES):
        found.append("pipeline")
    return found


def agent_pills(slug, depth):
    links = []
    for key in agents_for(slug):
        name, href = AGENT_LINKS[key]
        links.append(f'<a href="{rel(depth, href)}">{name}</a>')
    return f'<div class="related">{"".join(links)}</div>'


def neighbor_rows(slug, depth):
    pools = []
    if slug in DESIGNER_RUNS:
        pools.append(DESIGNER_RUNS)
    if slug in RESEARCHER_RUNS or slug in RESEARCHER_LENSES:
        pools.append(RESEARCHER_RUNS + RESEARCHER_LENSES)
    for _, group in PIPELINE_PHASES:
        if slug in group:
            pools.append(group)
    ordered = []
    for pool in pools:
        for item in pool:
            if item != slug and item not in ordered:
                ordered.append(item)
    return skill_rows(ordered[:4], depth)


def used_by_sentence(slug):
    names = [AGENT_LINKS[key][0] for key in agents_for(slug)]
    if not names:
        return "Call it by name when you want only this job."
    if len(names) == 1:
        return f"{names[0]} runs this when the work needs it. Call it by name when you want only this job."
    if len(names) == 2:
        return f"{names[0]} and {names[1]} run this when the work needs it. Call it by name when you want only this job."
    return f"{names[0]}, {names[1]}, and {names[2]} run this when the work needs it. Call it by name when you want only this job."


def orchestrator_runs(slug):
    if slug == "ux-designer":
        return DESIGNER_RUNS
    if slug == "ux-research":
        return RESEARCHER_RUNS + RESEARCHER_LENSES
    if slug == "design-thinking-ux":
        found = []
        for _, group in PIPELINE_PHASES:
            found.extend(s for s in group if s not in found)
        return found
    return []


def orchestrator_page_body(slug):
    title, blurb = SKILLS[slug]
    agent_name, agent_href = AGENT_LINKS[ORCHESTRATOR_AGENT[slug]]
    return f"""
<section class="section" id="call">
  <h2>Call it yourself</h2>
  <p>Name the skill when you want the whole job in one chat. Open the agent when you want the steps laid out.</p>
  {spec("Prompt", "use " + slug)}
</section>
<section class="section" id="overview">
  <h2>Overview</h2>
  <p>This is the skill behind the <a href="{rel(2, agent_href)}">{agent_name}</a> agent. It runs the skills below, one at a time, and stops at the points where it needs you.</p>
</section>
<section class="section" id="runs">
  <h2>Skills it runs</h2>
  {skill_rows(orchestrator_runs(slug), 2)}
</section>
"""


def skill_page_body(slug):
    title, blurb = SKILLS[slug]
    if slug in ORCHESTRATOR_AGENT:
        return orchestrator_page_body(slug)
    extra = ""
    if slug == "test-loopback":
        extra = "<p>New studies use findings-publish.</p>"
    return f"""
<section class="section" id="call">
  <h2>Call it yourself</h2>
  <p>Name the skill. The agent is the package around it, not a requirement.</p>
  {spec("Prompt", "use " + slug)}
</section>
<section class="section" id="overview">
  <h2>Overview</h2>
  <p>{blurb}</p>
  <p>{used_by_sentence(slug)}</p>
  {extra}
</section>
<section class="section" id="used">
  <h2>Used by</h2>
  {agent_pills(slug, 2)}
</section>
<section class="section" id="related">
  <h2>Nearby skills</h2>
  {neighbor_rows(slug, 2)}
</section>
"""


def pipeline_skill_blocks(depth):
    empathize = (
        '<section class="section" id="empathize"><h2>Empathize</h2>'
        f'<p>This phase calls the <a href="{rel(depth, "agents/researcher/index.html")}">UX researcher</a>. '
        "The skills for it are on that agent. Design thinking runs one at a time, then waits at the gate.</p></section>"
    )
    blocks = [empathize]
    for label, slugs in PIPELINE_PHASES:
        anchor = label.lower()
        blocks.append(
            f'<section class="section" id="{anchor}"><h2>{label}</h2>{skill_rows(slugs, depth)}</section>'
        )
    return "".join(blocks)


def shell(key, title, kicker, lede, toc, body, nav_key=None):
    depth = DEPTH[key]
    current_key = nav_key or key
    asset = rel(depth, "assets/")
    nav = []
    for label, items in NAV:
        nav.append(f'<p class="nav-label">{label}</p>')
        for item_key, name, href, child in items:
            current = ' aria-current="page"' if item_key == current_key else ""
            cls = ' class="is-child"' if child else ""
            nav.append(f'<a href="{rel(depth, href)}"{cls}{current}>{name}</a>')
    toc_html = ""
    if toc:
        links = "".join(f'<a href="#{i}">{n}</a>' for i, n in toc)
        toc_html = f'<aside class="toc"><p>On this page</p>{links}</aside>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title} — UX DesignOps</title>
  <script>(function(){{try{{var k="theme",s=localStorage.getItem(k),d;if(s==="dark")d=true;else if(s==="light")d=false;else d=window.matchMedia("(prefers-color-scheme: dark)").matches;var e=document.documentElement;if(d)e.classList.add("dark");else e.classList.remove("dark");e.style.colorScheme=d?"dark":"light";}}catch(x){{}}}})();</script>
  <link rel="stylesheet" href="{asset}site.css?v=7" />
</head>
<body>
  <a class="skip" href="#content">Skip to content</a>
  <header class="topbar">
    <a class="brand" href="{rel(depth, "index.html")}">
      {logo_markup()}
      <span class="brand-divider" aria-hidden="true"></span>
      <span class="brand-name">UX DesignOps</span>
    </a>
    <div class="topbar-actions">
      <a class="preview-link" href="{rel(depth, "v1/")}">Previous site</a>
      <button type="button" class="menu-btn" id="menu-btn" aria-expanded="false" aria-controls="sidebar" aria-label="Open menu">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
      <button type="button" class="icon-btn" id="theme-toggle" aria-pressed="false" aria-label="Toggle color theme">
        <svg class="theme-icon-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
        <svg class="theme-icon-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>
      </button>
    </div>
  </header>
  <div class="scrim" id="scrim"></div>
  <div class="layout">
    <nav class="sidebar" id="sidebar" aria-label="Documentation">
      <div class="side-nav">{"".join(nav)}</div>
      <p class="side-foot">The previous site is kept at <a href="{rel(depth, "v1/")}">/v1</a>.</p>
    </nav>
    <main class="page" id="content">
      <article>
        <p class="kicker">{kicker}</p>
        <h1>{title}</h1>
        <p class="lede">{lede}</p>
        {body}
      </article>
      {toc_html}
    </main>
  </div>
  <script src="{asset}site.js"></script>
</body>
</html>
"""


PAGES = {}

PAGES["home"] = dict(
    title="Pick an agent",
    kicker="UX DesignOps",
    lede="Three doors. The skills stay inside them. You do not have to choose from a list of 38 names.",
    toc=[("start", "Get started"), ("doors", "The doors"), ("system", "How this is organized"), ("which", "Which door")],
    body=f"""
<section class="section" id="start">
  <h2>Get started</h2>
  <p><a href="../get-started/index.html">Install the pack once</a>, then paste this. It asks whether you have a screen or a new project.</p>
  {spec("Prompt", "You are the UX designer.")}
  <p class="quiet">More prompts are on <a href="../agents/designer/">UX designer</a>, including a Figma link, a screenshot, and a new project.</p>
</section>
<section class="section" id="doors">
  <div class="door-grid">
    <a class="card" href="../agents/designer/">
      <span class="status status-ready">Available</span>
      <h2>Start here</h2>
      <p>A screen that is not working, or a new project. It asks a few questions, then draws variations or starts research and a one-pager.</p>
      <span class="go">UX designer</span>
    </a>
    <a class="card" href="../agents/researcher/">
      <span class="status status-ready">Available</span>
      <h2>Research a question</h2>
      <p>Answer a question about users from what we already know. Plan a new study only for the part we still cannot answer.</p>
      <span class="go">UX researcher</span>
    </a>
    <a class="card" href="../agents/pipeline/">
      <span class="status status-ready">Available</span>
      <h2>Walk the whole project</h2>
      <p>Go from first research through usability testing, one step at a time. It pauses at each decision and waits for you.</p>
      <span class="go">Design thinking</span>
    </a>
  </div>
</section>
<section class="section" id="system">
  <h2>How this is organized</h2>
  <p>Same shape as a design system. Foundations are the rules. Styles are what every screen and study has to apply. Agents are the packages you call. Skills are the jobs inside them, and you can still call a skill by itself.</p>
  <div class="layer-grid">
    <a class="card" href="../foundations/"><h3>Foundations</h3><p>Five phases, with a review point at the end of each one.</p><span class="go">The pipeline</span></a>
    <a class="card" href="../styles/"><h3>Styles</h3><p>Design tokens (the named colors, type and spacing) with the same names as in Figma.</p><span class="go">Design tokens</span></a>
    <a class="card" href="../agents/"><h3>Agents</h3><p>Pick the one that matches your job: designer, researcher, or the full project walk.</p><span class="go">All agents</span></a>
    <a class="card" href="../skills/"><h3>Skills</h3><p>The jobs an agent runs for you. Open one when you want only that job.</p><span class="go">All skills</span></a>
    <a class="card" href="../get-started/"><h3>Get started</h3><p>Install the pack once. Then call an agent, or a single skill.</p><span class="go">Install</span></a>
  </div>
</section>
<section class="section" id="which">
  <h2>Which door</h2>
  <div class="split">
    <article class="card"><h3>A screen to change</h3><p>UX designer. Paste a Figma link to the screen, or a screenshot if you do not have one.</p></article>
    <article class="card"><h3>A question about users</h3><p>UX researcher. It checks what we already know about users (the Frame) before it proposes a new study.</p></article>
    <article class="card"><h3>A project, start unclear</h3><p>UX designer. Say it is a new project. It starts research, then a one-pager, and waits.</p></article>
    <article class="card"><h3>First time on this machine</h3><p>Install, then come back to a door. The skills are the parts inside the agent.</p></article>
  </div>
  <p class="quiet">This folder is a preview. It does not replace the current DesignOps site.</p>
</section>
""",
)

PAGES["expect"] = dict(
    title="What to expect",
    kicker="UX DesignOps",
    lede="The pack has 41 skills. Most of them sit in two places: UX research, which finds out what we know, and UX design, which shapes and checks the work. A small design ops group runs the pipeline between them.",
    toc=[("overview", "What to expect"), ("start", "Get started"), ("role", "Pick a role"), ("do", "What do you want to do?"), ("how", "How this is organized")],
    body=(ROOT / "_partials" / "expect-body.html").read_text().replace("../assets/", "assets/"),
)

PAGES["start"] = dict(
    title="Install",
    kicker="Get started",
    lede="One install. After that, call an agent. You do not type the names of the skills inside it.",
    toc=[("cursor", "Cursor"), ("claude", "Claude Code")],
    body=f"""
<section class="section" id="then">
  <div class="door-grid">
    <a class="card" href="../agents/designer/"><span class="status status-ready">Ready</span><h3>UX designer</h3><p>Start here. A screen, or a new project. More prompts are on that page.</p></a>
    <a class="card" href="../agents/researcher/"><span class="status status-ready">Ready</span><h3>UX researcher</h3><p>Questions about users, evidence, and studies.</p></a>
    <a class="card" href="../agents/pipeline/"><span class="status status-ready">Ready</span><h3>Design thinking</h3><p>The full walk, with a stop at each gate.</p></a>
  </div>
</section>
<section class="section" id="cursor">
  <h2>Cursor</h2>
  <p>Paste this in a Cursor agent chat. Approve the file access when Cursor asks. The skills, including the UX designer, then work in every project on that computer.</p>
  {spec("Cursor", CURSOR)}
  <p>Run the same prompt again after a new skill is pushed. A new chat uses the updated copy.</p>
  <p>A Cursor admin can install the pack for the whole team. In the dashboard, open Plugins and MCPs, choose Add Marketplace, then Import from Repo, and paste <code>https://github.com/lesley-spec/uxdesignops</code>. Turn on Auto Refresh and set the impact-ux plugin to Required. That import is limited to admins.</p>
</section>
<section class="section" id="claude">
  <h2>Claude Code</h2>
  <p>Paste this in Claude Code. Approve the file access when it asks. The skills, including the UX designer, then work in every project on that computer. The browser chat cannot run this.</p>
  {spec("Claude Code", CLAUDE)}
  <p>Run the same prompt again after a new skill is pushed. A new chat uses the updated copy.</p>
  <p>Or run the published installer yourself:</p>
  {spec("Terminal", "curl -fsSL https://lesley-spec.github.io/uxdesignops/skills/install-all.sh | bash")}
</section>
""",
)

PAGES["foundations"] = dict(
    title="The pipeline",
    kicker="Foundations",
    lede="Five phases. Each one ends when a person confirms the decision. The agents stop there.",
    toc=[("phases", "Phases"), ("join", "Join in the middle"), ("audience", "Brand and Partner"), ("rules", "What every agent keeps")],
    body="""
<section class="section" id="phases">
  <h2>Phases</h2>
  <div class="phases">
    <div class="phase"><div class="phase-rail"><span class="phase-num">1</span><span class="phase-line"></span></div><div class="phase-body"><h3>Empathize</h3><p>What we know from the Frame, product data, and studies.</p><p class="meta">Gate: this is a problem worth solving.</p></div></div>
    <div class="phase"><div class="phase-rail"><span class="phase-num">2</span><span class="phase-line"></span></div><div class="phase-body"><h3>Define</h3><p>A one-pager and a linked UX epic.</p><p class="meta">Gate: publish.</p></div></div>
    <div class="phase"><div class="phase-rail"><span class="phase-num">3</span><span class="phase-line"></span></div><div class="phase-body"><h3>Ideate</h3><p>A few directions, then a critique against the spec.</p><p class="meta">Gate: a chosen direction.</p></div></div>
    <div class="phase"><div class="phase-rail"><span class="phase-num">4</span><span class="phase-line"></span></div><div class="phase-body"><h3>Prototype</h3><p>A Brand or Partner screen you can click.</p><p class="meta">Gate: ready to test.</p></div></div>
    <div class="phase"><div class="phase-rail"><span class="phase-num">5</span><span class="phase-line"></span></div><div class="phase-body"><h3>Test</h3><p>A study plan. Findings go back to Empathize.</p><p class="meta">Gate: recruit.</p></div></div>
  </div>
</section>
<section class="section" id="join">
  <h2>Join in the middle</h2>
  <p>If you already have research, a one-pager, mocks, or a prototype, start at that phase. The pipeline asks what you have before it starts over.</p>
</section>
<section class="section" id="audience">
  <h2>Brand and Partner</h2>
  <p>These are different products. Say which one. Shared work names both. Screens and this documentation use Styleguide V2.</p>
</section>
<section class="section" id="rules">
  <h2>What every agent keeps</h2>
  <ul class="plain">
    <li>Label what is verified and what is an interpretation. Do not invent quotes or numbers.</li>
    <li>Brand and Partner stay on their own shells.</li>
    <li>Critique a direction against the spec before prototyping it.</li>
    <li>Stop at the human gate. Publishing, recruiting, and a chosen direction wait for a person.</li>
  </ul>
</section>
""",
)

HEX = re.compile(r"^#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?$")
TOKENS = json.loads((ROOT / "_tokens.json").read_text())


def esc(value):
    return html.escape(str(value), quote=True)


def pretty(name):
    if name == "space/size-touch-target-min":
        return "Minimum touch target"
    tail = name.split("/")[-1]
    tail = re.sub(r"^vnext[ -]", "", tail)
    tail = tail.replace("-", " ").replace("_", " ")
    return tail[:1].upper() + tail[1:] if tail else name


def hay(*parts):
    return esc(" ".join(str(part) for part in parts if part is not None))


def finder():
    return (
        '<label class="finder"><span>Find a token</span>'
        '<input id="token-finder" type="search" placeholder="text-default, gap, #1d66de" autocomplete="off">'
        "</label>"
        '<p class="finder-empty is-hidden" id="finder-empty">No tokens match.</p>'
    )


def token_section(sid, title, inner, intro="", count=None):
    bits = [f'<section class="section token-section" id="{esc(sid)}"><h2>{esc(title)}</h2>']
    if count:
        bits.append(f'<p class="token-count">{count} tokens</p>')
    if intro:
        bits.append(f"<p>{intro}</p>")
    bits.append(inner)
    bits.append("</section>")
    return "".join(bits)


def swatch(value):
    if not isinstance(value, str) or not HEX.match(value):
        return f'<b class="num">{esc(value)}</b>'
    alpha = len(value) == 9 and value[7:].lower() != "ff"
    well = " chip-well" if alpha else ""
    return f'<span class="chip-hold{well}"><i class="chip" style="background:{esc(value)}"></i></span>'


def color_row(row):
    name, label = row["n"], pretty(row["n"])
    return (
        f'<article class="token-row" data-token="{hay(name, label, row["l"], row["d"])}">'
        f'<div class="token-id"><b>{esc(label)}</b><span class="token-name">{esc(name)}</span></div>'
        f'<div class="token-mode">{swatch(row["l"])}<span>Light</span><span class="token-note">{esc(row["l"])}</span></div>'
        f'<div class="token-mode">{swatch(row["d"])}<span>Dark</span><span class="token-note">{esc(row["d"])}</span></div>'
        "</article>"
    )


def number_row(name, value, second=None, labels=("Light", "Dark"), note="", paired=False):
    label = pretty(name)
    show_pair = paired or (second is not None and second != value)
    note_html = f'<span class="token-note">{esc(note)}</span>' if note else ""
    if not show_pair:
        return (
            f'<article class="token-row single" data-token="{hay(name, label, value, note)}">'
            f'<div class="token-id"><b>{esc(label)}</b><span class="token-name">{esc(name)}</span>{note_html}</div>'
            f'<div class="token-mode"><b class="num">{esc(value)}</b></div>'
            "</article>"
        )
    return (
        f'<article class="token-row" data-token="{hay(name, label, value, second, note)}">'
        f'<div class="token-id"><b>{esc(label)}</b><span class="token-name">{esc(name)}</span>{note_html}</div>'
        f'<div class="token-mode"><b class="num">{esc(value)}</b><span>{esc(labels[0])}</span></div>'
        f'<div class="token-mode"><b class="num">{esc(second)}</b><span>{esc(labels[1])}</span></div>'
        "</article>"
    )


PAGES["styles"] = dict(
    title="Design tokens",
    kicker="Styles",
    lede="Design tokens are the building blocks of the UI. These pages list the living set: every design token, every VNext primitive, and every screen-size token. The same names are used in Figma and on this site.",
    toc=[("what", "What a token is"), ("name", "Parts of a name"), ("cover", "What they cover"), ("context", "Light and dark"), ("use", "How to use one")],
    body="""
<ul class="points">
  <li>A token is a name that points at a color, a type style, or a measurement.</li>
  <li>Bind the token. Do not type the value by hand.</li>
  <li>The name says where it is used. <span class="token-name">color/text/text-default</span> is the default text color.</li>
  <li>VNext Light and VNext Dark share the name. The value changes with the mode.</li>
</ul>
<section class="section" id="what">
  <h2>What a token is</h2>
  <p>Two things. A name, and the value that name points at. The name stays when the value changes, so a screen and this page can share one decision.</p>
  <div class="token-example">
    <div>
      <span class="token-kicker">Name</span>
      <span class="token-name token-name-lg">color/text/text-default</span>
    </div>
    <div>
      <span class="token-kicker">Value, VNext Light</span>
      <i class="chip l-text example-chip"></i>
    </div>
  </div>
  <p>Figma binds the variable. This site uses the same name. A hex typed into a frame will not follow the next change.</p>
</section>
<section class="section" id="name">
  <h2>Parts of a name</h2>
  <p>Names go from the general to the specific. The pieces are separated by slashes.</p>
  <ol class="name-parts">
    <li><b>color</b><span>What it is</span></li>
    <li><b>text</b><span>The role</span></li>
    <li><b>text-default</b><span>The decision</span></li>
  </ol>
  <p>Read it as a sentence: the default color for text.</p>
</section>
<section class="section" id="cover">
  <h2>What they cover</h2>
  <div class="door-grid">
    <a class="card" href="color/"><h3>Color</h3><p>Every color role. Text, buttons, navigation, status, AI, and social. Each name has a light value and a dark value.</p><span class="go">Open</span></a>
    <a class="card" href="type/"><h3>Type</h3><p>Sarabun and Roboto Mono, three weights, and every size on desktop and mobile.</p><span class="go">Open</span></a>
    <a class="card" href="space/"><h3>Space</h3><p>The spacing scale, then every gap, padding, height, width, and radius.</p><span class="go">Open</span></a>
    <a class="card" href="primitives/"><h3>Primitives</h3><p>The VNext color ramps, spacing steps, and size steps the tokens point at.</p><span class="go">Open</span></a>
    <a class="card" href="layout/"><h3>Layout</h3><p>Screen widths, page padding, and grid columns for desktop and mobile.</p><span class="go">Open</span></a>
  </div>
  <p>The V2 mode and the Primitives (V2) collection are retired. These pages list VNext Light, VNext Dark, Primitives (VNext), and Screen Size.</p>
  <div class="resources">
    <a href="https://www.figma.com/design/Uwg1IvlTgvVA2IvX6WLxOd/Styleguide--V2-"><b>Styleguide V2</b><span>The file. Set Design Tokens to VNext Light or VNext Dark.</span></a>
    <a href="https://impact.atlassian.net/l/c/yEv0GqPN"><b>Component library</b><span>The components those tokens sit on.</span></a>
  </div>
</section>
<section class="section" id="context">
  <h2>Light and dark</h2>
  <p>A context is a mode. The token name does not change. VNext Light is the default. VNext Dark is the other value. This site’s theme control is that switch. The old V2 column in the file is retired.</p>
  <div class="context-pair">
    <div class="context light">
      <p class="context-kicker">VNext Light</p>
      <p class="context-title">Pick an agent</p>
      <p class="context-body">Same names. The light values.</p>
      <span class="context-btn">Primary button</span>
    </div>
    <div class="context dark">
      <p class="context-kicker">VNext Dark</p>
      <p class="context-title">Pick an agent</p>
      <p class="context-body">Same names. The dark values.</p>
      <span class="context-btn">Primary button</span>
    </div>
  </div>
</section>
<section class="section" id="use">
  <h2>How to use one</h2>
  <p>In Figma, bind the variable or apply the text style. On a product screen, clone an example and place a real component. A primary action is the Primary Button, State Default. A field label is the Field Label text style.</p>
  <p>To check a color, open <a href="color/">Color</a> and search the name. The swatch is the current value. Bind the name.</p>
</section>
""",
)

def by_name(rows):
    return {row["n"]: row for row in rows}


def rows_for(rows, prefix):
    return [row for row in rows if row["n"].startswith(prefix)]


def color_group_key(name):
    parts = name.split("/")
    if len(parts) >= 3 and parts[1] == "background" and parts[2] == "social":
        return "social"
    return parts[1]


COLOR_ORDER = [
    ("text", "Text"),
    ("icon", "Icon"),
    ("background", "Background"),
    ("social", "Social"),
    ("border", "Border"),
    ("primary", "Primary"),
    ("secondary", "Secondary"),
    ("tertiary", "Tertiary"),
    ("danger", "Danger"),
    ("filter", "Filter"),
    ("tab", "Tab"),
    ("navigation", "Navigation"),
    ("critical", "Critical"),
    ("success", "Success"),
    ("warning", "Warning"),
    ("decorative", "Decorative"),
    ("ai", "AI"),
    ("brand", "Brand"),
    ("reporting", "Reporting"),
    ("calendar", "Calendar"),
    ("dropshadow-default", "Shadow"),
    ("loading-skeleton", "Loading"),
]

SPACE_ORDER = [
    ("gap", "Gap"),
    ("padding", "Padding"),
    ("height", "Height"),
    ("width", "Width"),
    ("radius", "Radius"),
    ("size-touch-target-min", "Touch target"),
]

TYPE_ORDER = [
    "display-title",
    "display-text",
    "wizard-header",
    "metric",
    "header",
    "wizard-subheader",
    "subheader",
    "field-label",
    "secondary-field-label",
    "regular-text",
    "description-text",
    "text-link",
    "ghost-text",
    "html-code",
    "help-text",
    "table-first-column",
    "table-subtext",
]

RAMP_ORDER = [
    ("gray", "Gray"),
    ("blue", "Blue"),
    ("red", "Red"),
    ("orange", "Orange"),
    ("yellow", "Yellow"),
    ("pink", "Pink"),
    ("green", "Green"),
    ("ai", "AI"),
    ("brand", "Brand"),
    ("social", "Social"),
    ("gradients", "Gradients"),
]

WEIGHTS = {"bold": 700, "semibold": 600, "regular": 400}


def luminance(value):
    if not isinstance(value, str) or not HEX.match(value):
        return -1
    channel = value[1:7]
    red = int(channel[0:2], 16)
    green = int(channel[2:4], 16)
    blue = int(channel[4:6], 16)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def build_color():
    colors = [row for row in TOKENS["design"] if row["t"] == "COLOR"]
    grouped = {}
    for row in colors:
        grouped.setdefault(color_group_key(row["n"]), []).append(row)
    toc = []
    parts = [finder()]
    for key, title in COLOR_ORDER:
        rows = grouped.pop(key, [])
        if not rows:
            continue
        rows.sort(key=lambda row: row["n"])
        toc.append((key, title))
        body = '<div class="token-list">' + "".join(color_row(row) for row in rows) + "</div>"
        parts.append(token_section(key, title, body, count=len(rows)))
    if grouped:
        raise SystemExit(f"color tokens without a group: {sorted(grouped)}")
    return toc, "".join(parts), len(colors)


def build_type():
    screen = by_name(TOKENS["screen"])
    families = [row for row in TOKENS["design"] if row["n"].startswith("typography/font family/")]
    primitive_family = {
        "typography/font family/font-family": "font family/body",
        "typography/font family/font-family-html-code": "font family/html",
    }
    family_cards = []
    for row in families:
        css = "var(--font-family-code)" if "html" in row["n"] else "var(--font-family)"
        sample = "use design-system" if "html" in row["n"] else row["l"]
        primitive = primitive_family[row["n"]]
        family_cards.append(
            f'<article class="type-row" data-token="{hay(row["n"], primitive, row["l"], sample)}">'
            f'<p class="family-sample" style="font-family:{css}">{esc(sample)}</p>'
            f'<span class="token-name">{esc(row["n"])}</span>'
            f'<span class="token-name">{esc(primitive)}</span>'
            f'<span class="token-note">{esc(row["l"])}</span></article>'
        )
    weight_cards = []
    for slug, css_weight in WEIGHTS.items():
        row = screen[f"typography/font weight/{slug}"]
        weight_cards.append(
            f'<article class="type-row" data-token="{hay(row["n"], row["desktop"])}">'
            f'<p class="weight-sample" style="font-weight:{css_weight}">{esc(row["desktop"])}</p>'
            f'<span class="token-name">{esc(row["n"])}</span></article>'
        )
    scale = []
    for slug in TYPE_ORDER:
        size = screen[f"typography/font size/{slug}"]
        line = screen[f"typography/line height/{slug}"]
        scale.append(
            f'<article class="token-row" data-token="{hay(size["n"], line["n"], pretty(slug), size["desktop"], size["mobile"], line["desktop"], line["mobile"])}">'
            f'<div class="token-id"><b>{esc(pretty(slug))}</b>'
            f'<span class="token-name">{esc(size["n"])}</span>'
            f'<span class="token-name">{esc(line["n"])}</span></div>'
            f'<div class="token-mode"><b class="num">{size["desktop"]} / {line["desktop"]}</b><span>Desktop</span></div>'
            f'<div class="token-mode"><b class="num">{size["mobile"]} / {line["mobile"]}</b><span>Mobile</span></div>'
            "</article>"
        )
    styles = "".join(
        f'<li data-token="{esc(name)}">{esc(name)}</li>' for name in TOKENS["textStyles"]
    )
    toc = [("families", "Families"), ("weights", "Weights"), ("scale", "Size scale"), ("styles", "Text styles")]
    body = finder() + token_section(
        "families",
        "Families",
        f'<div class="type-list">{"".join(family_cards)}</div>',
        "Apply the family token. Sarabun is the UI face. Roboto Mono is the code face.",
    ) + token_section(
        "weights",
        "Weights",
        f'<div class="type-list weights">{"".join(weight_cards)}</div>',
        "Three weights. The same names on desktop and mobile. A text style chooses one of them.",
    ) + token_section(
        "scale",
        "Size scale",
        '<div class="token-list">' + "".join(scale) + "</div>",
        "Size and line height. The first number is the size. The second is the line height. Desktop and mobile are both in the Screen Size collection.",
        count=len(scale),
    ) + token_section(
        "styles",
        "Text styles",
        f'<ul class="style-names">{styles}</ul>',
        "Apply the style by this name in Figma. Reporting styles share the scale above. They do not have their own size tokens.",
        count=len(TOKENS["textStyles"]),
    )
    return toc, body


def build_space():
    steps = [row for row in TOKENS["primitives"] if row["n"].startswith("spacing/")]
    steps.sort(key=lambda row: (row["v"] == 9999, row["v"]))
    bars = []
    for row in steps:
        value = row["v"]
        if value == 9999:
            bar = '<i class="is-pill"></i>'
            note = "Pill"
        elif value == 0:
            bar = '<i class="is-zero"></i>'
            note = ""
        else:
            width = max(2, round(value / 64 * 100))
            bar = f'<i style="width:{width}%"></i>'
            note = ""
        bars.append(
            f'<div class="space-row" data-token="{hay(row["n"], value, note)}">'
            f"<b>{value}</b>{bar}<span class=\"token-name\">{esc(row['n'])}</span>"
            + (f'<span class="token-note">{note}</span>' if note else "")
            + "</div>"
        )
    grouped = {}
    for row in TOKENS["design"]:
        if row["n"].startswith("space/"):
            grouped.setdefault(row["n"].split("/")[1], []).append(row)
    toc = [("scale", "The scale")]
    parts = [finder(), token_section(
        "scale",
        "The scale",
        f'<div class="space-scale">{"".join(bars)}</div>',
        "Primitives (VNext) spacing. A gap or a padding token points at one of these.",
        count=len(steps),
    )]
    for key, title in SPACE_ORDER:
        rows = grouped.pop(key, [])
        if not rows:
            continue
        rows.sort(key=lambda row: row["n"])
        toc.append((key, title))
        cards = []
        for row in rows:
            note = "Pill" if row["l"] == 9999 else ""
            cards.append(number_row(row["n"], row["l"], row["d"], note=note))
        parts.append(token_section(
            key,
            title,
            '<div class="token-list">' + "".join(cards) + "</div>",
            count=len(rows),
        ))
    if grouped:
        raise SystemExit(f"space tokens without a group: {sorted(grouped)}")
    return toc, "".join(parts)


def ramp_key(name):
    parts = name.split("/")
    if parts[1].startswith("vnext"):
        return "gradients"
    return parts[1]


def ramp_card(row):
    value = row["v"]
    alpha = isinstance(value, str) and len(value) == 9 and value[7:].lower() != "ff"
    well = " chip-well" if alpha else ""
    return (
        f'<article class="ramp-swatch" data-token="{hay(row["n"], pretty(row["n"]), value)}">'
        f'<div class="swatch-face{well}"><i style="background:{esc(value)}"></i></div>'
        f'<b>{esc(pretty(row["n"]))}</b>'
        f'<span class="token-name">{esc(row["n"])}</span>'
        f'<span class="token-note">{esc(value)}</span>'
        "</article>"
    )


def build_primitives():
    colors = [row for row in TOKENS["primitives"] if row["n"].startswith("color/")]
    grouped = {}
    for row in colors:
        grouped.setdefault(ramp_key(row["n"]), []).append(row)
    steps = [row for row in TOKENS["primitives"] if row["n"].startswith("spacing/")]
    sizes = [row for row in TOKENS["primitives"] if row["n"].startswith("size/")]
    sizes.sort(key=lambda row: row["v"])
    toc = []
    parts = [finder()]
    for key, title in RAMP_ORDER:
        rows = grouped.pop(key, [])
        if not rows:
            continue
        rows.sort(key=lambda row: (-luminance(row["v"]), row["n"]))
        toc.append((key, title))
        intro = ""
        if key == "brand":
            intro = "Brand primitives. On a product screen, the logo uses color/brand/brand-red."
        elif key == "social":
            intro = "Platform colors. Social backgrounds in the design tokens point here."
        elif key == "gradients":
            intro = "The two stops of each gradient."
        parts.append(token_section(
            key,
            title,
            f'<div class="ramp">{"".join(ramp_card(row) for row in rows)}</div>',
            intro,
            count=len(rows),
        ))
    if grouped:
        raise SystemExit(f"primitive colors without a ramp: {sorted(grouped)}")
    toc.append(("size", "Size"))
    size_cards = "".join(
        number_row(row["n"], row["v"]) for row in sizes
    )
    parts.append(token_section(
        "size",
        "Size",
        f'<div class="token-list">{size_cards}</div>',
        "Raw size steps. Spacing steps are on Space. Grid columns are on Layout.",
        count=len(sizes),
    ))
    parts.append(
        f'<p class="quiet">{len(colors)} color primitives, {len(steps)} spacing steps, {len(sizes)} size steps.</p>'
    )
    return toc, "".join(parts)


def column_sort(name):
    match = re.search(r"(\d+)-column", name)
    if match:
        return (0, int(match.group(1)), name)
    if "total" in name:
        return (1, 0, name)
    return (2, 0, name)


def build_layout():
    screen = TOKENS["screen"]
    widths = [row for row in screen if row["n"].startswith(("width/", "padding/"))]
    grids = [row for row in TOKENS["design"] if row["n"].startswith("grid/")]
    columns = [row for row in TOKENS["primitives"] if row["n"].startswith("grid columns/")]
    grouped = {}
    for row in columns:
        parts = row["n"].split("/")
        key = "desktop" if len(parts) == 2 else parts[1]
        grouped.setdefault(key, []).append(row)
    switches = []
    for row in TOKENS["design"]:
        if row["t"] in ("BOOLEAN",):
            switches.append(("design", row["n"], row["l"], row["d"]))
    for row in screen:
        if row["t"] in ("BOOLEAN", "STRING") and not row["n"].startswith("typography/"):
            switches.append(("screen", row["n"], row["desktop"], row["mobile"]))
    toc = [("screen", "Screen"), ("columns", "Grid columns")]
    screen_cards = "".join(
        number_row(row["n"], row["desktop"], row["mobile"], labels=("Desktop", "Mobile"), paired=True)
        for row in widths
    )
    parts = [finder(), token_section(
        "screen",
        "Screen",
        f'<div class="token-list">{screen_cards}</div>',
        "Screen Size collection. Desktop is 1440. Mobile is 375.",
        count=len(widths),
    )]
    column_html = []
    order = [
        "brand expanded grid",
        "brand collapsed grid",
        "partner grid",
        "checklist grid",
        "tablet grid",
        "mobile grid",
        "desktop",
    ]
    for key in order:
        rows = grouped.pop(key, [])
        if not rows:
            continue
        rows.sort(key=lambda row: column_sort(row["n"]))
        title = "Desktop" if key == "desktop" else pretty(key)
        sid = "col-" + re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-")
        toc.append((sid, title))
        cards = "".join(number_row(row["n"], row["v"]) for row in rows)
        column_html.append(f'<div class="token-group"><h3 id="{sid}">{esc(title)}</h3><div class="token-list">{cards}</div></div>')
    if grouped:
        raise SystemExit(f"grid columns without a group: {sorted(grouped)}")
    parts.append(token_section(
        "columns",
        "Grid columns",
        "".join(column_html),
        "Primitives (VNext) column widths, in pixels.",
        count=len(columns),
    ))
    toc.append(("one", "One column"))
    one = "".join(number_row(row["n"], row["l"], row["d"]) for row in sorted(grids, key=lambda row: row["n"]))
    parts.append(token_section(
        "one",
        "One column",
        f'<div class="token-list">{one}</div>',
        "Design-token names for a single column. The values match the 1-column primitives.",
        count=len(grids),
    ))
    toc.append(("switches", "File switches"))
    switch_cards = []
    for source, name, light, dark in switches:
        labels = ("Light", "Dark") if source == "design" else ("Desktop", "Mobile")
        left = "On" if light is True else "Off" if light is False else light
        right = "On" if dark is True else "Off" if dark is False else dark
        switch_cards.append(number_row(name, left, right, labels=labels, paired=True))
    parts.append(token_section(
        "switches",
        "File switches",
        f'<div class="token-list">{"".join(switch_cards)}</div>',
        "These control which components the Styleguide file shows. They are not colors or measurements.",
        count=len(switches),
    ))
    return toc, "".join(parts)


_color_toc, _color_body, _color_count = build_color()
PAGES["color"] = dict(
    title="Color",
    kicker="Design tokens",
    lede=f"{_color_count} color tokens. Light is VNext Light. Dark is VNext Dark. Bind the name.",
    toc=_color_toc,
    href="styles/color/index.html",
    body=_color_body,
)

_type_toc, _type_body = build_type()
PAGES["type"] = dict(
    title="Type",
    kicker="Design tokens",
    lede="Apply the text style by name. Size and line height change between desktop and mobile. Weight is Bold, SemiBold, or Regular.",
    toc=_type_toc,
    href="styles/type/index.html",
    body=_type_body,
)

_space_toc, _space_body = build_space()
PAGES["space"] = dict(
    title="Space",
    kicker="Design tokens",
    lede="The spacing scale, then every space token. Bind the name. The number is the current value.",
    toc=_space_toc,
    href="styles/space/index.html",
    body=_space_body,
)

_prim_toc, _prim_body = build_primitives()
PAGES["primitives"] = dict(
    title="Primitives",
    kicker="Design tokens",
    lede="Primitives (VNext) are the raw scale. Design tokens point at them. On a screen, bind the design token.",
    toc=_prim_toc,
    href="styles/primitives/index.html",
    body=_prim_body,
)

_layout_toc, _layout_body = build_layout()
PAGES["layout"] = dict(
    title="Layout",
    kicker="Design tokens",
    lede="Screen widths, page padding, and the grid. Desktop and mobile are modes of the Screen Size collection.",
    toc=_layout_toc,
    href="styles/layout/index.html",
    body=_layout_body,
)

PAGES["agents"] = dict(
    title="Agents",
    kicker="Agents",
    lede="Call the agent. It runs the skills inside it. Name a skill yourself when you only want that job.",
    toc=[("make", "Make"), ("learn", "Learn"), ("run", "Run the whole job"), ("later", "Later")],
    body="""
<section class="section" id="make">
  <h2>Make</h2>
  <div class="layer-grid">
    <a class="card" href="designer/">
      <span class="status status-ready">Ready</span>
      <h3>UX designer</h3>
      <p>Start here. Variations of a screen, or a new project from research and a one-pager.</p>
      <span class="go">Open</span>
    </a>
  </div>
</section>
<section class="section" id="learn">
  <h2>Learn</h2>
  <div class="layer-grid">
    <a class="card" href="researcher/">
      <span class="status status-ready">Ready</span>
      <h3>UX researcher</h3>
      <p>Intake, the Frame, a study only if we still need one, then findings.</p>
      <span class="go">Open</span>
    </a>
  </div>
</section>
<section class="section" id="run">
  <h2>Run the whole job</h2>
  <div class="layer-grid">
    <a class="card" href="pipeline/">
      <span class="status status-ready">Ready</span>
      <h3>Design thinking</h3>
      <p>Empathize through Test. Use this when the work is a project, not a single screen or a single question.</p>
      <span class="go">Open</span>
    </a>
  </div>
</section>
<section class="section" id="later">
  <h2>Later</h2>
  <article class="card">
    <span class="status status-later">Not a door yet</span>
    <h3>Product manager</h3>
    <p>Specs, epics, and the handoff after Define. We will add this door after designer and researcher are clear.</p>
  </article>
</section>
""",
)

PAGES["designer"] = dict(
    title="UX designer",
    kicker="Agents",
    lede="The easy way in. It asks what you are doing, then either draws three variations of a screen or starts a new project from research and a one-pager.",
    toc=[("start", "Get started"), ("overview", "Overview"), ("usage", "Usage"), ("anatomy", "Anatomy"), ("runs", "Skills it runs"), ("related", "Related")],
    body=f"""
<p><span class="status status-ready">Ready</span></p>
<section class="section" id="start">
  <h2>Get started</h2>
  <p>Install once from <a href="../../get-started/index.html">Install</a>, then paste a prompt. Replace the bracketed link with your frame.</p>
  {spec("Not sure yet", "You are the UX designer.")}
  {spec("Variations", "You are the UX designer. Brand. Christine’s welcome header doesn’t say what to do with 35 new applications. Here is the screen: [Figma link]. I don’t have a working file yet.")}
  {spec("Screenshot", "You are the UX designer. Brand. Christine’s welcome header doesn’t say what to do with 35 new applications. I don’t have a Figma link. The screenshot is the current screen. I don’t have a working file yet.")}
  {spec("New project", "You are the UX designer. This is a new project. Partner. I only have a hunch. No research yet.")}
  <ul class="plain">
    <li>A Figma link is the screen to design from. A screenshot is the fallback.</li>
    <li>It duplicates the closest Page Template into a working file. It does not draw in the Styleguide file.</li>
    <li>Color is a Styleguide V2 variable. Type is a named text style. It asks before it creates a file.</li>
  </ul>
</section>
<section class="section" id="overview">
  <h2>Overview</h2>
  <p>Say you are the UX designer. You do not need to name a skill or a phase. It asks whether this is a specific screen or a new project, who it is for, and what you already have. A screen becomes three variations. A new project starts the pipeline and does not draw yet.</p>
  <p>This agent is the {chip("ux-designer", 2)} skill. Call it by name to run the same flow in any chat.</p>
</section>
<section class="section" id="usage">
  <h2>Usage</h2>
  <div class="split">
    <article class="card"><h3>Use it when</h3><p>You have a screen that fails a job, or you are starting a project and are not sure where to begin. Christine’s welcome header does not say what to do with 35 new applications.</p></article>
    <article class="card"><h3>Use another door when</h3><p>The only question is about users. That is the researcher. You already know you want the full walk and want to name it. That is design thinking.</p></article>
  </div>
</section>
<section class="section" id="anatomy">
  <h2>Anatomy</h2>
  <div class="anatomy">
    <article><span class="n">1</span><div><h3>Ask</h3><p>A specific screen or a new project. Brand or Partner. A hunch, research, a one-pager, mocks, or a prototype.</p></div></article>
    <article><span class="n">2</span><div><h3>The screen</h3><p>Paste a Figma link. A screenshot works if you do not have one. It reads <a href="https://www.figma.com/design/Uwg1IvlTgvVA2IvX6WLxOd/Styleguide--V2-?node-id=5314-16">Page Templates</a> and duplicates the closest one. It does not draw on that page.</p></div></article>
    <article><span class="n">3</span><div><h3>Tokens</h3><p>{chip("design-system", 2)}. Styleguide V2 only. VNext Light or VNext Dark. Named text styles. No raw hex, including from a screenshot.</p></div></article>
    <article><span class="n">4</span><div><h3>Variations</h3><p>Three directions in a working file. It asks before it creates that file. Then it stops.</p></div></article>
    <article><span class="n">5</span><div><h3>Or the pipeline</h3><p>A new project goes to research, then a one-pager. No screens until you ask for them.</p></div></article>
  </div>
</section>
<section class="section" id="runs">
  <h2>Skills it runs</h2>
  <p>You do not call these yourself. A screen runs the set below. A new project runs <a href="../pipeline/">design thinking</a> from the phase your artifacts point to. You can still call any skill by name.</p>
  {skill_rows(DESIGNER_RUNS, 2)}
</section>
<section class="section" id="related">
  <h2>Related</h2>
  <div class="related">
    <a href="../researcher/">UX researcher</a>
    <a href="../pipeline/">Design thinking</a>
    <a href="../../styles/">Styles</a>
    <a href="../../skills/">All skills</a>
    <a href="../../foundations/">Foundations</a>
  </div>
</section>
""",
)

PAGES["researcher"] = dict(
    title="UX researcher",
    kicker="Agents",
    lede="Answers a question from what impact.com already knows, then plans only the study that is still missing.",
    toc=[("start", "Get started"), ("overview", "Overview"), ("usage", "Usage"), ("anatomy", "Anatomy"), ("runs", "Skills it runs"), ("related", "Related")],
    body=f"""
<p><span class="status status-ready">Ready</span></p>
<section class="section" id="start">
  <h2>Get started</h2>
  <p><a href="../../get-started/index.html">Install</a> once, then paste this.</p>
  {spec("Prompt", RESEARCH)}
  <p>When the gate is “problem worth solving,” the next door is design thinking at Define. It does not start ideating on its own.</p>
</section>
<section class="section" id="overview">
  <h2>Overview</h2>
  <p>Call {chip("ux-research", 2)}. It reads one skill at a time. It checks the Frame before it plans fieldwork, and it stops before it launches a study or writes tickets. Name a single skill if you only want that job.</p>
</section>
<section class="section" id="usage">
  <h2>Usage</h2>
  <div class="split">
    <article class="card"><h3>Use it when</h3><p>Someone has a research request, a “what do we know?” question, or a finding that needs a closer look.</p></article>
    <article class="card"><h3>Use another door when</h3><p>The output should be a screen. That is the designer, after the problem is confirmed. A full Empathize-to-Test project is design thinking.</p></article>
  </div>
</section>
<section class="section" id="anatomy">
  <h2>Anatomy</h2>
  <div class="anatomy">
    <article><span class="n">1</span><div><h3>Route</h3><p>{chip("research-intake", 2)} sorts the ask. Some requests close here.</p></div></article>
    <article><span class="n">2</span><div><h3>What we know</h3><p>{chip("user-context", 2)} and {chip("user-personas", 2)} against the Frame.</p></div></article>
    <article><span class="n">3</span><div><h3>Evidence</h3><p>{chip("data-analyze", 2)}, {chip("research-synthesis", 2)}, or {chip("synthesize-research", 2)}, depending on the source.</p></div></article>
    <article><span class="n">4</span><div><h3>A study, if needed</h3><p>{chip("research-planner", 2)} and {chip("research-builder", 2)}. Recruiting waits for a person.</p></div></article>
  </div>
</section>
<section class="section" id="runs">
  <h2>Skills it runs</h2>
  <p>One at a time, in roughly this order, skipping whatever you already have. The second list is for a question that needs it. Call any row by name and the researcher will not wrap the rest of the path around it.</p>
  <h3>The path</h3>
  {skill_rows(RESEARCHER_RUNS, 2)}
  <h3>When the question needs them</h3>
  {skill_rows(RESEARCHER_LENSES, 2)}
</section>
<section class="section" id="related">
  <h2>Related</h2>
  <div class="related">
    <a href="../designer/">UX designer</a>
    <a href="../pipeline/">Design thinking</a>
    <a href="../../skills/">All skills</a>
    <a href="../../foundations/">Foundations</a>
  </div>
</section>
""",
)

PAGES["pipeline"] = dict(
    title="Design thinking",
    kicker="Agents",
    lede="Walks a project from Empathize to Test. It calls the phase skill, shows the work, and waits at each gate.",
    toc=[("start", "Get started"), ("overview", "Overview"), ("usage", "Usage"), ("anatomy", "Anatomy"), ("runs", "Skills it runs"), ("related", "Related")],
    body=f"""
<p><span class="status status-ready">Ready</span></p>
<section class="section" id="start">
  <h2>Get started</h2>
  <p>The easier start is the <a href="../designer/">UX designer</a>. <a href="../../get-started/index.html">Install</a> once, then paste a prompt.</p>
  {spec("Easier start", "You are the UX designer. This is a new project. Partner. I only have a hunch. No research yet.")}
  {spec("This agent", PIPELINE)}
  <p>You can join mid-pipeline: “We already have a one-pager and UX-1234. Jump to Ideate.”</p>
</section>
<section class="section" id="overview">
  <h2>Overview</h2>
  <p>Call {chip("design-thinking-ux", 2)} when you want the whole pipeline. If you only want research or only a screen, use those doors instead. This one is for the project.</p>
</section>
<section class="section" id="usage">
  <h2>Usage</h2>
  <div class="split">
    <article class="card"><h3>Use it when</h3><p>You have a flow, a hunch, or a ticket, and you are willing to stop at each decision.</p></article>
    <article class="card"><h3>Use another door when</h3><p>You already know it is a research question, or you already know it is a screen. Those agents are narrower on purpose.</p></article>
  </div>
</section>
<section class="section" id="anatomy">
  <h2>Anatomy</h2>
  <div class="anatomy">
    <article><span class="n">1</span><div><h3>Intake</h3><p>What you are working on, Brand or Partner, where you already are, and what you already have.</p></div></article>
    <article><span class="n">2</span><div><h3>One phase</h3><p>It reads that phase’s skill and does the work in the same chat.</p></div></article>
    <article><span class="n">3</span><div><h3>The gate</h3><p>Problem worth solving, publish, chosen direction, or recruit. It updates the board and waits.</p></div></article>
  </div>
</section>
<section class="section" id="runs">
  <h2>Skills it runs</h2>
  <p>Name <span class="skill">design-thinking-ux</span> for the whole walk. Name a skill below when you already know the phase. Empathize is the researcher.</p>
  {pipeline_skill_blocks(2)}
</section>
<section class="section" id="related">
  <h2>Related</h2>
  <div class="related">
    <a href="../designer/">UX designer</a>
    <a href="../researcher/">UX researcher</a>
    <a href="../../foundations/">Foundations</a>
    <a href="../../skills/">All skills</a>
    <a href="../../get-started/">Install</a>
  </div>
</section>
""",
)

PAGES["skills"] = dict(
    title="Skills",
    kicker="Skills",
    lede="An agent is a package of these. Call the agent and it picks the skill. Call a skill when you already know which job you want.",
    toc=[("orchestrators", "Orchestrators"), ("designer", "UX designer"), ("researcher", "UX researcher"), ("pipeline", "Design thinking")],
    href="skills/index.html",
    body=f"""
<section class="section" id="orchestrators">
  <h2>Orchestrators</h2>
  <p>These skills run other skills in order. Call one when you want the whole job. Each one is also the skill behind an agent. The lists below are the skills they call, and you can still name any of them yourself.</p>
  {skill_rows(ORCHESTRATORS, 1)}
</section>
<section class="section" id="designer">
  <h2>UX designer</h2>
  <p>A screen to change, or a new project. The designer runs this set, then waits for you to pick a direction. <a href="../agents/designer/">Open the designer</a>.</p>
  {skill_rows(DESIGNER_RUNS, 1)}
</section>
<section class="section" id="researcher">
  <h2>UX researcher</h2>
  <p><a href="../agents/researcher/">UX researcher</a> runs one of these at a time, then offers the next. Name a skill from this list when you only want that job.</p>
  <h3>The path</h3>
  {skill_rows(RESEARCHER_RUNS, 1)}
  <h3>When the question needs them</h3>
  {skill_rows(RESEARCHER_LENSES, 1)}
</section>
<section class="section" id="pipeline">
  <h2>Design thinking</h2>
  <p><a href="../agents/pipeline/">Design thinking</a> walks the whole project. Empathize uses the researcher. Later phases run the skills below. Name a phase skill if you are already there.</p>
  {pipeline_skill_blocks(1)}
</section>
""",
)

covered = set(DESIGNER_RUNS) | set(RESEARCHER_RUNS) | set(RESEARCHER_LENSES) | set(ORCHESTRATORS)
for _, group in PIPELINE_PHASES:
    covered.update(group)
missing = set(SKILLS) - covered
if missing:
    raise SystemExit(f"skills not in a package: {sorted(missing)}")

for slug in SKILLS:
    DEPTH[slug] = 2
    title, blurb = SKILLS[slug]
    PAGES[slug] = dict(
        title=title,
        kicker="Skills",
        lede=blurb,
        toc=(
            [("call", "Call it yourself"), ("overview", "Overview"), ("runs", "Skills it runs")]
            if slug in ORCHESTRATOR_AGENT
            else [("call", "Call it yourself"), ("overview", "Overview"), ("used", "Used by"), ("related", "Nearby skills")]
        ),
        href=f"skills/{slug}/index.html",
        nav="skills",
        body=skill_page_body(slug),
    )

NAV_HREF = {k: h for _, items in NAV for k, _, h, _ in items}

for key, page in PAGES.items():
    href = page.get("href") or NAV_HREF[key]
    out = ROOT / href
    out.parent.mkdir(parents=True, exist_ok=True)
    html = shell(
        key,
        page["title"],
        page["kicker"],
        page["lede"],
        page["toc"],
        page["body"],
        page.get("nav"),
    )
    out.write_text(html)
    print(out.relative_to(ROOT))

redirect = ROOT / "expect" / "index.html"
redirect.parent.mkdir(parents=True, exist_ok=True)
redirect.write_text("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta http-equiv="refresh" content="0; url=../" />
  <link rel="canonical" href="../" />
  <title>What to expect — UX DesignOps</title>
  <script>location.replace("../")</script>
</head>
<body>
  <p><a href="../">What to expect</a></p>
</body>
</html>
""")
print(redirect.relative_to(ROOT))
