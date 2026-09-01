#!/usr/bin/env python3
"""Pull competitor product-feature posts into docs/research/feed/feed.json.

Sources: first-party RSS/Atom, Awin product-release HTML, Google News RSS.
Run locally or from .github/workflows/competitor-feed.yml (Mondays).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

USER_AGENT = (
    "UXDesignOpsCompetitorFeed/1.0 (+https://github.com/lesley-spec/uxdesignops; "
    "internal product+UX competitive intel)"
)
TIMEOUT_SEC = 25
LOOKBACK_DAYS = 120
MAX_ITEMS_PER_SOURCE = 18

ROOT = Path(__file__).resolve().parent
DEFAULT_OUT = ROOT / "docs" / "research" / "feed" / "feed.json"

FEATURE_RE = re.compile(
    r"\b("
    r"feature|launch(?:ed|es|ing)?|releas(?:e|ed|es|ing)|"
    r"product update|changelog|what'?s new|roll(?:ed)? out|"
    r"introduc(?:e|ed|es|ing)|announc(?:e|ed|es|ing)|"
    r"upgrade|dashboard|reporting|attribution|tracking|"
    r"campaign builder|ai |new platform|overhaul"
    r")\b",
    re.I,
)

SKIP_TITLES = {
    "solutions",
    "resources",
    "company",
    "platform",
    "for advertisers",
    "for publishers",
    "see it in action",
    "what's new?",
    "whats new?",
    "welcome to the new awin",
    "advertisers",
    "publishers",
    "partners",
    "about us",
    "newsroom",
    "contact",
    "privacy",
    "cookie",
    "documentation index",
    "fetch the complete documentation index",
}

NEWS_EXCLUDE_RE = {
    "awin": re.compile(
        r"aviation week|spaceplane|starship|launcher startup|esa awards|"
        r"reusable|louisiana for starship",
        re.I,
    ),
    "cj": re.compile(
        r"\bcj one\b|groundseesaw|ground seesaw|digitaltoday|herald",
        re.I,
    ),
}

NEWS_QUERIES = {
    "awin": (
        '"Awin" (affiliate OR advertiser OR publisher OR "product release" '
        'OR "Campaign Builder" OR "product update") '
        "-aviation -spaceplane -Starship"
    ),
    "cj": (
        '("CJ Affiliate" OR "cj.com") (launch OR "product update" OR feature '
        'OR platform OR "CJ One") -"CJ ONE points" -Groundseesaw'
    ),
    "rakuten": '"Rakuten Advertising" (launch OR "product update" OR Mirai OR feature OR platform)',
    "partnerize": 'Partnerize (launch OR "product update" OR Lighthouse OR feature OR platform)',
    "shareasale": "ShareASale (Awin OR migrate OR launch OR feature OR platform)",
    "pepperjam": '(Pepperjam OR "Pepperjam Ascend") (launch OR "product update" OR feature OR platform)',
    "refersion": 'Refersion (launch OR "product update" OR feature OR platform)',
}

COMPETITORS = [
    {
        "id": "awin",
        "name": "Awin",
        "note": "ShareASale programs now run on Awin",
    },
    {
        "id": "cj",
        "name": "CJ Affiliate",
        "note": "formerly Commission Junction",
    },
    {
        "id": "rakuten",
        "name": "Rakuten Advertising",
        "note": "",
    },
    {
        "id": "partnerize",
        "name": "Partnerize",
        "note": "",
    },
    {
        "id": "shareasale",
        "name": "ShareASale",
        "note": "migrated onto Awin (Oct 2025)",
    },
    {
        "id": "pepperjam",
        "name": "Pepperjam",
        "note": "Ascend / Gutsy family",
    },
    {
        "id": "refersion",
        "name": "Refersion",
        "note": "Partnerize family",
    },
]

FIRST_PARTY: list[dict[str, str]] = [
    {
        "competitor": "awin",
        "kind": "html_features",
        "url": "https://www.awin.com/gb/product-releases",
        "label": "Awin Product Releases",
    },
    {
        "competitor": "awin",
        "kind": "html_features",
        "url": "https://help.awin.com/docs/winter-2026",
        "label": "Awin Help — Winter 2026",
    },
    {
        "competitor": "rakuten",
        "kind": "rss",
        "url": "https://blog.rakutenadvertising.com/feed/",
        "label": "Rakuten Advertising Blog",
    },
    {
        "competitor": "partnerize",
        "kind": "rss",
        "url": "https://partnerize.com/feed/",
        "label": "Partnerize Feed",
    },
    {
        "competitor": "partnerize",
        "kind": "rss",
        "url": "https://partnerize.com/resources/blog/feed/",
        "label": "Partnerize Resources Blog",
    },
    {
        "competitor": "refersion",
        "kind": "rss",
        "url": "https://www.refersion.com/blog/feed/",
        "label": "Refersion Blog",
    },
]


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _strip_html(raw: str) -> str:
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", raw or "")
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _clip(text: str, limit: int = 280) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0]
    return (cut or text[: limit - 1]).rstrip(".,;:") + "…"


def _item_id(*parts: str) -> str:
    blob = "|".join(p.strip().lower() for p in parts if p)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:16]


def _iso_week(d: date) -> str:
    iso = d.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def _week_label(d: date) -> str:
    start = d - timedelta(days=d.weekday())
    end = start + timedelta(days=6)
    if start.month == end.month:
        return f"{start.strftime('%b')} {start.day}–{end.day}, {end.year}"
    if start.year == end.year:
        return f"{start.strftime('%b')} {start.day} – {end.strftime('%b')} {end.day}, {end.year}"
    return f"{start.strftime('%b')} {start.day}, {start.year} – {end.strftime('%b')} {end.day}, {end.year}"


def _parse_date(raw: str) -> datetime | None:
    if not raw:
        return None
    text = raw.strip()
    try:
        dt = parsedate_to_datetime(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except (TypeError, ValueError, OverflowError):
        pass
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        pass
    for fmt in ("%Y-%m-%d", "%B %d, %Y", "%b %d, %Y"):
        try:
            dt = datetime.strptime(text[:32], fmt)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def _guess_release_date(url: str, html: str) -> datetime:
    blob = f"{url} {html[:4000]}".lower()
    year = _now().year
    m = re.search(r"(winter|spring|summer|autumn|fall)\s+(20\d{2})", blob)
    if m:
        season, year_s = m.group(1), int(m.group(2))
        month = {"winter": 1, "spring": 3, "summer": 6, "autumn": 9, "fall": 9}[season]
        return datetime(year_s, month, 15, tzinfo=timezone.utc)
    if "winter" in blob:
        return datetime(year, 1, 15, tzinfo=timezone.utc)
    if "summer" in blob:
        return datetime(year, 6, 15, tzinfo=timezone.utc)
    if "spring" in blob:
        return datetime(year, 3, 15, tzinfo=timezone.utc)
    return _now()


def _classify(title: str, excerpt: str, source_kind: str) -> str:
    if source_kind == "html_features":
        return "feature"
    hay = f"{title} {excerpt}"
    if FEATURE_RE.search(hay):
        return "feature"
    return "news"


def _local_tag(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def fetch(url: str) -> tuple[int, str, str]:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with urlopen(req, timeout=TIMEOUT_SEC) as resp:
        status = getattr(resp, "status", 200)
        ctype = resp.headers.get("Content-Type", "")
        body = resp.read()
    charset = "utf-8"
    if "charset=" in ctype:
        charset = ctype.split("charset=", 1)[1].split(";", 1)[0].strip() or "utf-8"
    text = body.decode(charset, errors="replace")
    return status, ctype, text


class _HeadingCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.features: list[tuple[str, str]] = []
        self._h: list[str] | None = None
        self._p: list[str] | None = None
        self._pending_title: str | None = None
        self._skip = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "nav", "footer"}:
            self._skip += 1
            return
        if self._skip:
            return
        if tag in {"h2", "h3"} and self._h is None:
            self._h = []
        elif tag == "p" and self._pending_title and self._p is None:
            self._p = []

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "nav", "footer"} and self._skip:
            self._skip -= 1
            return
        if self._skip:
            return
        if tag in {"h2", "h3"} and self._h is not None:
            title = re.sub(r"\s+", " ", "".join(self._h)).strip()
            self._h = None
            if (
                title
                and title.lower() not in SKIP_TITLES
                and 3 < len(title) < 90
                and "llms.txt" not in title.lower()
                and "documentation index" not in title.lower()
            ):
                self._pending_title = title
        elif tag == "p" and self._p is not None and self._pending_title:
            excerpt = re.sub(r"\s+", " ", "".join(self._p)).strip()
            self.features.append((self._pending_title, excerpt))
            self._pending_title = None
            self._p = None

    def handle_data(self, data: str) -> None:
        if self._skip:
            return
        if self._h is not None:
            self._h.append(data)
        elif self._p is not None:
            self._p.append(data)


def parse_html_features(html: str, page_url: str, competitor: str, label: str) -> list[dict[str, Any]]:
    parser = _HeadingCollector()
    try:
        parser.feed(html)
    except Exception:
        return []
    published = _guess_release_date(page_url, html)
    items: list[dict[str, Any]] = []
    seen: set[str] = set()
    for title, excerpt in parser.features:
        key = title.lower()
        if key in seen:
            continue
        seen.add(key)
        items.append(
            _make_item(
                competitor=competitor,
                title=title,
                url=page_url,
                published=published,
                excerpt=excerpt or f"Listed on {label}.",
                source_label=label,
                source_kind="html_features",
            )
        )
        if len(items) >= MAX_ITEMS_PER_SOURCE:
            break
    return items


def parse_rss(xml_text: str, competitor: str, label: str, source_kind: str) -> list[dict[str, Any]]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []

    items: list[dict[str, Any]] = []
    nodes = [el for el in root.iter() if _local_tag(el.tag) in {"item", "entry"}]
    for node in nodes:
        fields: dict[str, str] = {}
        for child in list(node):
            fields[_local_tag(child.tag)] = (child.text or "").strip()
            if _local_tag(child.tag) == "link":
                href = child.get("href") or child.text or ""
                if href:
                    fields["link"] = href.strip()

        title = _strip_html(fields.get("title", ""))
        link = fields.get("link") or fields.get("id") or fields.get("guid") or ""
        if not title or not link:
            continue
        raw_date = (
            fields.get("pubDate")
            or fields.get("published")
            or fields.get("updated")
            or fields.get("date")
            or ""
        )
        published = _parse_date(raw_date) or _now()
        excerpt = _strip_html(fields.get("description") or fields.get("summary") or fields.get("content") or "")
        items.append(
            _make_item(
                competitor=competitor,
                title=title,
                url=link,
                published=published,
                excerpt=excerpt,
                source_label=label,
                source_kind=source_kind,
            )
        )
        if len(items) >= MAX_ITEMS_PER_SOURCE:
            break
    return items


def _make_item(
    *,
    competitor: str,
    title: str,
    url: str,
    published: datetime,
    excerpt: str,
    source_label: str,
    source_kind: str,
) -> dict[str, Any]:
    d = published.date()
    return {
        "id": _item_id(competitor, url, title),
        "competitor": competitor,
        "title": title,
        "url": url,
        "published": published.date().isoformat(),
        "published_at": published.isoformat(),
        "week": _iso_week(d),
        "week_label": _week_label(d),
        "excerpt": _clip(excerpt),
        "kind": _classify(title, excerpt, source_kind),
        "source_label": source_label,
        "source_kind": source_kind,
    }


def google_news_url(query: str) -> str:
    return (
        "https://news.google.com/rss/search?q="
        + quote_plus(query)
        + "&hl=en-US&gl=US&ceid=US:en"
    )


def collect(lookback_days: int = LOOKBACK_DAYS) -> dict[str, Any]:
    cutoff = _now() - timedelta(days=lookback_days)
    sources_out: list[dict[str, Any]] = []
    items: list[dict[str, Any]] = []

    jobs: list[dict[str, str]] = list(FIRST_PARTY)
    for cid, query in NEWS_QUERIES.items():
        jobs.append(
            {
                "competitor": cid,
                "kind": "news",
                "url": google_news_url(query),
                "label": f"{next(c['name'] for c in COMPETITORS if c['id'] == cid)} in the news",
            }
        )

    for job in jobs:
        status = "ok"
        error = ""
        found = 0
        try:
            http_status, ctype, body = fetch(job["url"])
            if http_status >= 400:
                raise RuntimeError(f"HTTP {http_status}")
            looks_xml = "xml" in ctype or body.lstrip().startswith(("<?xml", "<rss", "<feed"))
            if job["kind"] == "html_features" or (job["kind"] == "rss" and not looks_xml and "<html" in body[:400].lower()):
                if job["kind"] == "rss" and not looks_xml:
                    raise RuntimeError("expected RSS, got HTML")
                batch = parse_html_features(body, job["url"], job["competitor"], job["label"])
            else:
                batch = parse_rss(body, job["competitor"], job["label"], job["kind"])
            kept = []
            exclude = NEWS_EXCLUDE_RE.get(job["competitor"])
            for item in batch:
                pub = _parse_date(item["published_at"]) or _now()
                if pub < cutoff and job["kind"] != "html_features":
                    continue
                hay = f"{item['title']} {item['excerpt']}"
                if exclude and exclude.search(hay):
                    continue
                kept.append(item)
            items.extend(kept)
            found = len(kept)
        except Exception as exc:
            status = "error"
            error = str(exc)[:180]

        sources_out.append(
            {
                "competitor": job["competitor"],
                "label": job["label"],
                "url": job["url"],
                "kind": job["kind"],
                "status": status,
                "error": error,
                "items": found,
            }
        )

    deduped: dict[str, dict[str, Any]] = {}
    for item in items:
        key = item["url"].split("?")[0].rstrip("/").lower() + "|" + item["title"].lower()
        prev = deduped.get(key)
        if not prev or item["published"] > prev["published"]:
            deduped[key] = item

    ranked = sorted(
        deduped.values(),
        key=lambda it: (it["published"], 0 if it["kind"] == "feature" else 1, it["title"]),
        reverse=True,
    )

    generated = _now()
    return {
        "generated_at": generated.isoformat(),
        "lookback_days": lookback_days,
        "competitors": COMPETITORS,
        "sources": sources_out,
        "items": ranked,
        "counts": {
            "items": len(ranked),
            "features": sum(1 for it in ranked if it["kind"] == "feature"),
            "news": sum(1 for it in ranked if it["kind"] == "news"),
            "ok_sources": sum(1 for s in sources_out if s["status"] == "ok"),
            "error_sources": sum(1 for s in sources_out if s["status"] == "error"),
        },
    }


def write_feed(payload: dict[str, Any], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--lookback-days", type=int, default=LOOKBACK_DAYS)
    args = parser.parse_args(argv)
    payload = collect(args.lookback_days)
    write_feed(payload, args.out)
    counts = payload["counts"]
    print(
        f"Wrote {args.out} — {counts['items']} items "
        f"({counts['features']} features, {counts['news']} news); "
        f"{counts['ok_sources']} sources ok, {counts['error_sources']} failed",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
