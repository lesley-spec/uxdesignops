#!/usr/bin/env python3
"""Persona Ask back end — REBUILD-PROMPT.md Layer 2 architecture.

Serves Anthropic from RULES + PACKS embedded in personas/index.html.
Keys stay server-side. Connectors beyond the packs are reported as unavailable
until wired; G2 is an embedded snapshot inside the packs.

Usage:
  export ANTHROPIC_API_KEY=sk-...
  python3 research-agent/persona_ask_server.py
  # then on the personas page (console or config):
  #   window.DESIGNOPS_PERSONA_ASK_URL = "http://127.0.0.1:8787"

Env:
  ANTHROPIC_API_KEY   required
  PERSONA_ASK_PORT    default 8787
  PERSONA_ASK_MODEL   default claude-sonnet-4-5
  PERSONA_HTML        optional path to personas index.html
"""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HTML = ROOT / "research-agent" / "docs" / "research" / "personas" / "index.html"
PORT = int(os.environ.get("PERSONA_ASK_PORT", "8787"))
MODEL = os.environ.get("PERSONA_ASK_MODEL", "claude-sonnet-4-5")
API = "https://api.anthropic.com/v1/messages"

NAMES = {
    "marlo": "Nia Bennett",
    "quinn": "Danny Alvarez",
    "nour": "Priya Shah",
    "pax": "Sophie Carter",
    "rowan": "Maya Thompson",
    "kit": "James Whitfield",
}

# Status line sources — pack is always live; others named until wired.
SOURCES = {
    "pack": {"live": True, "label": "Embedded evidence pack"},
    "g2": {"live": True, "label": "G2 (embedded snapshot in pack)"},
    "dovetail": {"live": False, "label": "Dovetail"},
    "posthog": {"live": False, "label": "PostHog"},
    "outset": {"live": False, "label": "Outset"},
    "pendo": {"live": False, "label": "Pendo"},
    "atlassian": {"live": False, "label": "Atlassian"},
    "gong": {"live": False, "label": "Gong (unavailable)"},
}


def load_packs(html_path: Path) -> tuple[str, dict[str, str]]:
    text = html_path.read_text(encoding="utf-8")
    rules_m = re.search(r"var RULES = `([\s\S]*?)`;", text)
    if not rules_m:
        raise SystemExit(f"RULES not found in {html_path}")
    rules = rules_m.group(1)
    packs: dict[str, str] = {}
    for pid in NAMES:
        m = re.search(rf"PACKS\.{pid}=`([\s\S]*?)`;", text)
        if not m:
            raise SystemExit(f"PACKS.{pid} not found in {html_path}")
        packs[pid] = m.group(1)
    return rules, packs


RULES, PACKS = load_packs(Path(os.environ.get("PERSONA_HTML", str(DEFAULT_HTML))))


def cors(handler: BaseHTTPRequestHandler) -> None:
    origin = handler.headers.get("Origin", "*")
    handler.send_header("Access-Control-Allow-Origin", origin)
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.send_header("Vary", "Origin")


def anthropic_stream(system: str, messages: list[dict], abort_check=None):
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")
    body = json.dumps(
        {
            "model": MODEL,
            "max_tokens": 1200,
            "stream": True,
            "system": system,
            "messages": messages,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        API,
        data=body,
        headers={
            "content-type": "application/json",
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        for raw in resp:
            if abort_check and abort_check():
                break
            line = raw.decode("utf-8", errors="replace").rstrip("\n")
            if not line.startswith("data: "):
                continue
            payload = line[6:]
            if payload == "[DONE]":
                break
            try:
                evt = json.loads(payload)
            except json.JSONDecodeError:
                continue
            et = evt.get("type")
            if et == "content_block_delta":
                delta = evt.get("delta") or {}
                if delta.get("type") == "text_delta":
                    yield delta.get("text") or ""
            elif et == "error":
                err = evt.get("error") or {}
                raise RuntimeError(err.get("message") or "Anthropic stream error")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        print(f"[persona-ask] {self.address_string()} {fmt % args}")

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        cors(self)
        self.end_headers()

    def do_GET(self) -> None:
        if self.path.rstrip("/") in ("/health", ""):
            payload = {
                "ok": True,
                "model": MODEL,
                "packs": sorted(PACKS.keys()),
                "rules_chars": len(RULES),
                "sources": SOURCES,
            }
            raw = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            cors(self)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
            return
        self.send_error(404)

    def do_POST(self) -> None:
        if self.path.rstrip("/") != "/ask":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length") or 0)
        try:
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.send_error(400, "invalid JSON")
            return

        pid = str(data.get("persona_id") or "")
        if pid not in PACKS:
            self.send_error(400, "unknown persona_id")
            return
        name = str(data.get("name") or NAMES[pid])
        turns = data.get("messages") or []
        if not isinstance(turns, list) or not turns:
            self.send_error(400, "messages required")
            return
        # Keep last eight conversation turns (REBUILD-PROMPT)
        turns = turns[-8:]
        messages = []
        for t in turns:
            role = t.get("role")
            content = t.get("content")
            if role not in ("user", "assistant") or not isinstance(content, str):
                continue
            messages.append({"role": role, "content": content[:8000]})
        if not messages or messages[-1]["role"] != "user":
            self.send_error(400, "last message must be user")
            return

        system = (
            RULES.replace("NAME_HERE", name.split()[0])
            + "\n\n--- EVIDENCE BRIEF ---\n\n"
            + PACKS[pid]
        )

        self.send_response(200)
        cors(self)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

        try:
            for chunk in anthropic_stream(system, messages):
                if not chunk:
                    continue
                frame = f"data: {json.dumps({'text': chunk})}\n\n".encode("utf-8")
                self.wfile.write(frame)
                self.wfile.flush()
            self.wfile.write(b"data: {\"done\": true}\n\n")
            self.wfile.flush()
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")[:500]
            err = json.dumps({"error": f"Anthropic HTTP {e.code}: {detail}"})
            self.wfile.write(f"data: {err}\n\n".encode("utf-8"))
        except Exception as e:  # noqa: BLE001 — surface to client
            err = json.dumps({"error": str(e)})
            self.wfile.write(f"data: {err}\n\n".encode("utf-8"))


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Warning: ANTHROPIC_API_KEY unset — /health works, /ask will fail.")
    print(f"Persona Ask on http://127.0.0.1:{PORT}")
    print(f"  RULES={len(RULES)} chars, packs={', '.join(PACKS)}")
    print(f"  Set window.DESIGNOPS_PERSONA_ASK_URL = 'http://127.0.0.1:{PORT}'")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
