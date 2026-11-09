# Site preview

A separate DesignOps site: Get started, Foundations, Styles, Agents, and the skills those agents run. A skill can still be called on its own.

Color, type, and the logo come from Styleguide V2, mode VNext Light. The theme control uses VNext Dark. The face is Sarabun. Marketing brand guidelines are not part of this site.

This folder is the new site. GitHub Pages publishes it at the root. The previous site, from `research-agent/docs/research`, is kept unchanged at `/v1/`. The installer files (`install-all.sh`, `install.sh`, `designops-skills.zip`) stay at `/skills/` so the install commands still work.

```bash
python3 -m http.server 4173 --directory site-next
```

Then open http://127.0.0.1:4173/
