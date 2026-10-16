# User personas at impact.com

Reference persona set for the UX DesignOps pipeline: three partner personas and three
brand personas, each with goals, a job-to-be-done, a workflow map and a stated
confidence score.

**Live on DesignOps:** https://lesley-spec.github.io/uxdesignops/personas/

Claude artifact (optional, live connectors on claude.ai):
https://claude.ai/artifact/FaBjbFu7hiM5LYBfALemAQ — ask UX Research for access.

**Definitive how-it-should-work spec:** [`REBUILD-PROMPT.md`](./REBUILD-PROMPT.md)

## Contents

| File | What it is |
|---|---|
| `index.html` | The page — packs, cards, Ask client, card export |
| `personas.md` | Full markdown copy of every persona |
| `REBUILD-PROMPT.md` | Architecture for Ask, packs, export, design system |
| `personas-src.html` | Unwrapped Nihal source snapshot used for rebuilds |

## Ask feature

Ask is grounded in byte-identical `RULES` + `PACKS` from the reference HTML.

**On DesignOps Pages (default):** answers are built in the browser from the embedded
evidence packs only — no API key, no back end. Outside the brief, the persona declines.
Status line names pack/G2 as live and model/connectors as unavailable.

**Optional model Ask:** run `persona_ask_server.py` with an Anthropic key; the page
probes `http://127.0.0.1:8787` and upgrades automatically when that server is up.

**Refusal test:** ask Nia *"what do you think of our pricing page?"* and James *"how does
procurement work at your company?"* — both must decline and name the gap.

## Card export

Each card exports PNG and SVG via an ordinary `<a download>` blob (no Claude downloads
API). Always light theme; measures against Helvetica Neue for SVG→canvas.

## Rebuild from Nihal

```bash
gh repo clone nihal-somers-impact/ux-research /tmp/ux-research-nihal -- --depth 1
python3 research-agent/publish_nihal_pages.py /tmp/ux-research-nihal
```

That copies `REBUILD-PROMPT.md`, verifies packs with a diff, unifies display names,
scopes chip CSS, swaps export to blob download, and wires the Ask client to
`DESIGNOPS_PERSONA_ASK_URL`.

## What makes this set different

**Every claim carries its denominator.** Several figures that had circulated as
segment-wide rates turned out to be six or four people. Those are marked, not quietly
dropped.

**Confidence is scored and visible**, so a reader knows which cards carry weight.

**Gaps are stated as prominently as findings.** There is no affiliate persona because the
research screener excluded them; that absence is on the page.

**You can question a persona** when Ask is live. Declining outside the evidence is the
feature — if the build answers everything, the packs were regenerated and the page is
not trustworthy.

## Feedback

For any feedback on how we can improve this, Slack the UX Research team.
