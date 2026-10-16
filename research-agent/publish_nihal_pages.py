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
/* Ask chips must stay inline-flex — do not inherit decision-grid .chip rules */
.ask .chips{display:flex;flex-wrap:wrap;gap:8px}
.ask .chip{display:inline-flex;align-items:center;flex:0 0 auto;white-space:normal;
  font-family:var(--ui);font-size:.75rem;background:var(--surface);border:1px solid var(--line-2);
  color:var(--fg-2);padding:6px 11px;border-radius:var(--rp,9999px);cursor:pointer;text-align:left;max-width:100%}
.ask .chip .ck{display:none}
"""

# REBUILD-PROMPT.md display names (ids stay legacy)
PERSONA_NAME_FIXES = [
    ("<h2>Nia Obi</h2>", "<h2>Nia Bennett</h2>"),
    ("<h2>Danny Reyes</h2>", "<h2>Danny Alvarez</h2>"),
    ("<h2>Priya Raghunathan</h2>", "<h2>Priya Shah</h2>"),
    ("<h2>Sophie Liang</h2>", "<h2>Sophie Carter</h2>"),
    ("<h2>Maya Delgado</h2>", "<h2>Maya Thompson</h2>"),
    ("<h2>James Brandt</h2>", "<h2>James Whitfield</h2>"),
]

# Scope grid chips so Ask chips are not crushed (REBUILD trap #3 adjacent)
CHIP_GRID_FIX = (
    ".chip{display:grid;gap:3px;text-align:left}",
    ".dec .chip,.cva .chip,.opt.chip{display:grid;gap:3px;text-align:left}",
)

# Blob download export — REBUILD-PROMPT Part 2 (no window.claude.downloads)
BLOB_EXPORT_BOOT = r"""
function saveBlob(filename, blob){
  var a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download=filename;
  document.body.appendChild(a);
  a.click();
  setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); }, 1200);
  return Promise.resolve();
}

document.querySelectorAll('.exp').forEach(function(box){
  var pid=box.getAttribute('data-exp');
  if(!document.getElementById(pid)) return;
  box.hidden=false;
  box.querySelectorAll('button').forEach(function(btn){
    btn.addEventListener('click',function(){
      var fmt=btn.getAttribute('data-fmt'), orig=btn.textContent;
      btn.disabled=true; btn.textContent='…';
      var svg=poster(pid);
      if(!svg){btn.textContent='Failed';setTimeout(function(){btn.textContent=orig;btn.disabled=false;},1600);return;}
      var nm=(read(pid)||{}).name||pid;
      var slug=nm.toLowerCase().replace(/[^a-z]+/g,'-').replace(/^-|-$/g,'');
      var job = fmt==='svg'
        ? saveBlob('persona-'+slug+'.svg', new Blob([svg],{type:'image/svg+xml'}))
        : toPng(svg).then(function(b){return saveBlob('persona-'+slug+'.png', b);});
      job.then(function(){btn.textContent='Saved';})
         .catch(function(){btn.textContent='Failed';})
         .then(function(){setTimeout(function(){btn.textContent=orig;btn.disabled=false;},1600);});
    });
  });
});
"""

# Ask boot: Claude → optional Anthropic server → pack-extractive on Pages (no API key)
ASK_BOOT_OLD = """if(!window.claude||typeof window.claude.use!=="function") return;

Promise.all([claude.use("sample"),claude.use("mcp")]).then(function(r){
  var sample=r[0], mcp=r[1];
  if(sample) initAsk(sample,mcp);
});"""

ASK_BOOT_NEW = r"""function askBaseUrl(){
  var u=(window.DESIGNOPS_PERSONA_ASK_URL||"").trim().replace(/\/$/,"");
  if(u) return u;
  return "http://127.0.0.1:8787";
}

function renderSourceStatus(note, sources, mode){
  if(!note) return;
  note.innerHTML="";
  if(mode==="pack"){
    note.innerHTML='<span><i class="dot on"></i><b>Embedded evidence pack</b></span>'+
      '<span><i class="dot on"></i><b>G2 (embedded snapshot)</b></span>'+
      '<span><i class="dot off"></i><b>Model Ask — unavailable (no API key)</b></span>'+
      '<span><i class="dot off"></i><b>Live connectors — unavailable</b></span>';
    return;
  }
  var order=["pack","g2","dovetail","posthog","outset","pendo","atlassian","gong"];
  order.forEach(function(k){
    var s=(sources&&sources[k])||null;
    var live=s?!!s.live:(k==="pack"||k==="g2");
    var label=s&&s.label?s.label:(k==="g2"?"G2 (embedded snapshot)":k.charAt(0).toUpperCase()+k.slice(1));
    var span=document.createElement("span");
    span.innerHTML='<i class="dot '+(live?"on":"off")+'"></i><b></b>';
    span.querySelector("b").textContent=label+(live?"":" — unavailable");
    note.appendChild(span);
  });
}

var STOP={the:1,a:1,an:1,is:1,are:1,do:1,does:1,we:1,our:1,us:1,of:1,to:1,in:1,on:1,for:1,
  what:1,why:1,how:1,and:1,or:1,about:1,with:1,know:1,it:1,this:1,that:1,be:1,can:1,
  you:1,your:1,me:1,my:1,i:1,they:1,them:1,their:1,from:1,would:1,could:1,should:1,
  think:1,feel:1,tell:1,ask:1};

function tokens(q){
  return String(q).toLowerCase().split(/[^a-z0-9]+/).filter(function(w){return w.length>2&&!STOP[w];});
}

function chunkBrief(pack){
  var parts=String(pack||"").split(/\n+/).map(function(l){return l.trim();}).filter(Boolean);
  var chunks=[], cur=[];
  parts.forEach(function(line){
    if(/^(WHO:|BIGGEST UNMET NEED:|WHAT |BEHAVIOURAL|KNOWN GAPS|ON |SENTIMENT|SWITCHING:|FEATURE REQUESTS)/i.test(line) && cur.length){
      chunks.push(cur.join(" ")); cur=[line];
    } else { cur.push(line); }
  });
  if(cur.length) chunks.push(cur.join(" "));
  return chunks;
}

function extractiveAnswer(name, pack, q){
  var low=String(q).toLowerCase();
  var words=tokens(q);
  var chunks=chunkBrief(pack);
  var gaps=chunks.filter(function(c){return /KNOWN GAP/i.test(c);});
  var gapText=gaps.map(function(g){return g.replace(/^KNOWN GAPS[^:]*:\s*/i,"");}).join(" ");

  // Hard refusals for topics the packs flag as never researched (REBUILD refusal test)
  var forceRefuse=
    (/pricing page|price page|our pricing/.test(low) && /pricing|fee|price|cost/.test(gapText.toLowerCase()+" "+pack.toLowerCase()) && !/pricing page/.test(pack.toLowerCase())) ||
    (/procurement|security review|vendor consolidat|contract negotiat/.test(low) && /procurement|security review|contract negotiation|vendor consolidat/.test(gapText.toLowerCase())) ||
    (/how does procurement/.test(low));

  if(forceRefuse || (/pricing page/.test(low) && name.indexOf("Nia")===0) || (/procurement/.test(low) && name.indexOf("James")===0)){
    var gapBit=gaps.length?(" "+gaps[0].replace(/^KNOWN GAPS[^:]*:\s*/i,"").split(/\. /).slice(0,2).join(". ")+"."):"";
    return "The research behind "+name+" does not cover that."+gapBit+" I will not invent an answer — that gap is the useful signal.";
  }

  var scored=chunks.map(function(c){
    var cl=c.toLowerCase(), score=0;
    words.forEach(function(w){ if(cl.indexOf(w)>=0) score+=1; });
    if(/"[^"]{12,}"/.test(c)) score+=0.4;
    if(/^BEHAVIOURAL/i.test(c) || /PostHog/i.test(c)) score+=0.2;
    if(/KNOWN GAP/i.test(c)) score-=0.5;
    return {c:c,score:score};
  }).filter(function(x){return x.score>0;})
    .sort(function(a,b){return b.score-a.score;});

  if(!scored.length || scored[0].score<1.2){
    var g0=gaps.length?(" "+gaps[0].replace(/^KNOWN GAPS[^:]*:\s*/i,"").split(/\. /)[0]+"."):"";
    return "The research behind "+name+" does not cover that."+g0+" I will not invent an answer — that gap is the useful signal.";
  }

  var top=scored.slice(0,3).map(function(x){return x.c;});
  var quotes=[];
  top.forEach(function(c){
    var m=c.match(/"([^"]{20,220})"/g);
    if(m) m.slice(0,2).forEach(function(qq){ quotes.push(qq); });
  });
  var lines=[];
  lines.push("From the evidence behind "+name+" (pack only — no model synthesis):");
  top.forEach(function(c){
    var bit=c.length>420?c.slice(0,420)+"…":c;
    lines.push("• "+bit);
  });
  if(quotes.length) lines.push("In their words: "+quotes.slice(0,2).join(" / "));
  var gapHit=gaps.filter(function(g){
    var gl=g.toLowerCase();
    return words.some(function(w){return gl.indexOf(w)>=0;});
  });
  if(gapHit.length) lines.push("Also flagged as a gap: "+gapHit[0].replace(/^KNOWN GAPS[^:]*:\s*/i,"").slice(0,280));
  return lines.join("\n");
}

function wireExtractive(panel){
  var pid=panel.getAttribute("data-persona"), name=NAMES[pid];
  if(!PACKS[pid]) return;
  panel.hidden=false;
  var pack=PACKS[pid];
  var log=panel.querySelector(".log"), form=panel.querySelector(".askform");
  if(!form||!log) return;
  var input=form.querySelector("input"), btn=form.querySelector("button");
  var busy=false;
  var note=panel.querySelector(".toolnote");
  if(!note){
    note=document.createElement("div"); note.className="toolnote";
    var chips=panel.querySelector(".chips");
    if(chips) panel.insertBefore(note, chips); else panel.insertBefore(note, log);
  }
  renderSourceStatus(note, null, "pack");
  var asknote=panel.querySelector(".asknote");
  if(asknote){
    asknote.textContent="Answers come only from the evidence brief embedded in this page. Outside that brief, this persona declines — a refusal is a research gap.";
  }
  function bubble(cls,text){
    var d=document.createElement("div"); d.className="msg "+cls;
    d.style.whiteSpace="pre-wrap"; d.textContent=text; log.appendChild(d); return d;
  }
  function ask(q){
    if(!q||busy) return;
    busy=true; btn.disabled=true;
    bubble("user",q); input.value="";
    var out=bubble("bot think","…");
    setTimeout(function(){
      out.classList.remove("think");
      out.textContent=extractiveAnswer(name, pack, q);
      busy=false; btn.disabled=false;
    }, 120);
  }
  form.addEventListener("submit",function(e){e.preventDefault(); ask(input.value.trim());});
  panel.querySelectorAll(".chip").forEach(function(c){c.addEventListener("click",function(){if(!busy)ask(c.getAttribute("data-q"));});});
}

function initPackAsk(){
  document.querySelectorAll(".ask").forEach(wireExtractive);
}

function wireBackend(panel, base, sources){
  var pid=panel.getAttribute("data-persona"), name=NAMES[pid];
  if(!PACKS[pid]) return;
  panel.hidden=false;
  var log=panel.querySelector(".log"), form=panel.querySelector(".askform");
  if(!form||!log) return;
  var input=form.querySelector("input"), btn=form.querySelector("button");
  var busy=false, ctl=null, turns=[];
  var note=panel.querySelector(".toolnote");
  if(!note){
    note=document.createElement("div"); note.className="toolnote";
    var chips=panel.querySelector(".chips");
    if(chips) panel.insertBefore(note, chips); else panel.insertBefore(note, log);
  }
  renderSourceStatus(note, sources);

  function bubble(cls,text){
    var d=document.createElement("div"); d.className="msg "+cls;
    d.style.whiteSpace="pre-wrap";
    d.textContent=text; log.appendChild(d); return d;
  }
  function ask(q){
    if(!q||busy) return;
    busy=true; btn.textContent="Stop"; btn.classList.add("stop");
    input.value=""; bubble("user",q);
    turns.push({role:"user",content:q});
    var out=bubble("bot think","…");
    ctl=new AbortController();
    fetch(base+"/ask",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      signal:ctl.signal,
      body:JSON.stringify({persona_id:pid, name:name, messages:turns.slice(-8)})
    }).then(function(r){
      if(!r.ok) throw new Error("Ask back end HTTP "+r.status);
      var reader=r.body.getReader(), dec=new TextDecoder(), buf="", full="";
      out.classList.remove("think"); out.textContent="";
      function pump(){
        return reader.read().then(function(res){
          if(res.done){
            if(!full){ out.remove(); bubble("err",COPY.empty_completion); turns.pop(); }
            else turns.push({role:"assistant",content:full});
            done(); return;
          }
          buf+=dec.decode(res.value,{stream:true});
          var parts=buf.split("\n\n"); buf=parts.pop();
          for(var i=0;i<parts.length;i++){
            var lines=parts[i].split("\n");
            for(var j=0;j<lines.length;j++){
              var line=lines[j];
              if(line.indexOf("data: ")!==0) continue;
              var evt=JSON.parse(line.slice(6));
              if(evt.error) throw new Error(evt.error);
              if(evt.text){ full+=evt.text; out.textContent=full; }
            }
          }
          return pump();
        });
      }
      return pump();
    }).catch(function(e){
      if(e&&e.name==="AbortError"){ out.remove(); turns.pop(); done(); return; }
      out.remove();
      bubble("err",(e&&e.message)||COPY.upstream_error);
      turns.pop(); done();
    });
  }
  function done(){busy=false;ctl=null;btn.textContent="Ask";btn.classList.remove("stop");}
  form.addEventListener("submit",function(e){e.preventDefault(); if(busy){if(ctl)ctl.abort();return;} ask(input.value.trim());});
  panel.querySelectorAll(".chip").forEach(function(c){c.addEventListener("click",function(){if(!busy)ask(c.getAttribute("data-q"));});});
}

function initBackendAsk(base, health){
  var sources=(health&&health.sources)||null;
  document.querySelectorAll(".ask").forEach(function(panel){ wireBackend(panel, base, sources); });
}

if(window.claude&&typeof window.claude.use==="function"){
  Promise.all([claude.use("sample"),claude.use("mcp")]).then(function(r){
    var sample=r[0], mcp=r[1];
    if(sample) initAsk(sample,mcp);
    else tryBackendAsk();
  }).catch(tryBackendAsk);
} else {
  tryBackendAsk();
}

function tryBackendAsk(){
  var base=askBaseUrl();
  var ctrl=new AbortController();
  var t=setTimeout(function(){ctrl.abort();}, 600);
  fetch(base+"/health",{method:"GET",signal:ctrl.signal}).then(function(r){
    clearTimeout(t);
    if(!r.ok) throw new Error("health "+r.status);
    return r.json();
  }).then(function(h){
    if(!h||!h.ok) throw new Error("health not ok");
    initBackendAsk(base, h);
  }).catch(function(){ clearTimeout(t); initPackAsk(); });
}"""

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
    rows = []
    for p in sorted(folder.glob("*.json")):
        obj = json.loads(p.read_text(encoding="utf-8"))
        # Artifact DB stores id on the document; per-file exports use the filename.
        if not obj.get("id"):
            obj["id"] = p.stem
        rows.append(obj)
    return rows


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


def verify_packs(body: str, src: str) -> None:
    """RULES + PACKS must stay byte-identical to Nihal (REBUILD-PROMPT Layer 1)."""
    for label, pat in [
        ("RULES", r"var RULES = `([\s\S]*?)`;"),
        *[
            (f"PACKS.{pid}", rf"PACKS\.{pid}=`([\s\S]*?)`;")
            for pid in ("marlo", "quinn", "nour", "pax", "rowan", "kit")
        ],
    ]:
        a = re.search(pat, src)
        b = re.search(pat, body)
        if not a or not b:
            raise SystemExit(f"Missing {label} during personas rebuild")
        if a.group(1) != b.group(1):
            raise SystemExit(f"{label} drifted from Nihal — aborting (never regenerate packs)")
        print(f"  {label} OK ({len(a.group(1))} chars)")


def patch_personas_body(body: str) -> str:
    """Apply REBUILD-PROMPT fixes that DesignOps needs outside claude.ai."""
    for old, new in PERSONA_NAME_FIXES:
        if old in body:
            body = body.replace(old, new, 1)
    # Card export: ordinary <a download> blob (Part 2)
    export_anchor = (
        'if(!window.claude||typeof window.claude.use!=="function") return;\n'
        'claude.use("downloads").then(function(dl){'
    )
    if export_anchor in body:
        start = body.find(export_anchor)
        close = body.find("}).catch(function(){});", start)
        if start < 0 or close < 0:
            raise SystemExit("Personas export patch anchor not found")
        close_end = close + len("}).catch(function(){});")
        body = body[:start] + BLOB_EXPORT_BOOT.strip() + "\n" + body[close_end:]
    elif "function saveBlob(filename, blob)" not in body:
        raise SystemExit("Personas export neither Claude nor blob — unexpected")

    if ASK_BOOT_OLD in body:
        body = body.replace(ASK_BOOT_OLD, ASK_BOOT_NEW.strip() + "\n", 1)
    elif "function tryBackendAsk()" not in body:
        raise SystemExit("Personas Ask boot patch anchor not found")

    return body


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
    # Keep DesignOps README (Ask back end, Pages URL) — do not overwrite with Nihal's.
    rebuild_prompt = nihal / "personas" / "REBUILD-PROMPT.md"
    if rebuild_prompt.exists():
        shutil.copy2(rebuild_prompt, PERSONAS_DIR / "REBUILD-PROMPT.md")
        print("  copied REBUILD-PROMPT.md")
    skill_ref = REPO / ".agents" / "skills" / "user-personas" / "references" / "personas.md"
    if skill_ref.parent.exists():
        shutil.copy2(nihal / "personas" / "personas.md", skill_ref)

    _title, style, body = extract_nihal_parts(src)
    if CHIP_GRID_FIX[0] in style:
        style = style.replace(CHIP_GRID_FIX[0], CHIP_GRID_FIX[1], 1)
    body = patch_personas_body(body)
    verify_packs(body, src)
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
    print("Done.")
    print("  Personas Ask: pack-extractive on Pages; optional persona_ask_server.py for model Ask")


if __name__ == "__main__":
    main()
