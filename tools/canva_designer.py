#!/usr/bin/env python3
"""
Canva Connect API wrapper — template-driven branded graphic generation.

PRIMARY FLOW (via the claude.ai Canva MCP): once the MCP is authenticated
(user runs /mcp, selects claude.ai Canva, completes OAuth), the real tools
surface and Claude uses them directly from the orchestrator layer. Typical
calls look like:
    mcp__claude_ai_Canva__* (list_designs, create_design_from_template,
    autofill_design, export_design)

This Python wrapper exists for deterministic CLI use — scheduled tasks and
other non-Claude callers. It uses a Canva Connect user access token
(CANVA_ACCESS_TOKEN in .env) to call the REST API directly. Get an access
token via the MCP OAuth flow (or via Canva Connect app → personal token for
dev).

API docs: https://www.canva.dev/docs/connect/

Usage:
    python tools/canva_designer.py list-templates [--search <query>]
    python tools/canva_designer.py render --template <id> \\
        --vars '{"headline":"...","body":"...","image_asset_id":"..."}' \\
        --out .tmp/graphics/out.png
    python tools/canva_designer.py render-from-brief --brief brief.json --out .tmp/graphics/

Note: if CANVA_ACCESS_TOKEN is not set, this tool prints a clear error and
exits. Garrett's preferred flow is to use the claude.ai Canva MCP from the
agent itself; CLI calls are for automation and offline jobs.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import requests

ROOT = Path(__file__).resolve().parent.parent
CANVA_API = "https://api.canva.com/rest/v1"


def _load_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


_load_env()


def _token() -> str:
    tok = os.environ.get("CANVA_ACCESS_TOKEN", "").strip()
    if not tok:
        print(
            "CANVA_ACCESS_TOKEN not set in .env.\n"
            "For agent use, prefer the claude.ai Canva MCP — run /mcp in Claude "
            "Code and select 'claude.ai Canva' to authenticate; the MCP's tools "
            "will appear automatically.\n"
            "For CLI use, generate a user access token via Canva Connect OAuth "
            "and put it in .env.",
            file=sys.stderr,
        )
        sys.exit(2)
    return tok


def _headers() -> dict:
    return {"Authorization": f"Bearer {_token()}", "Content-Type": "application/json"}


# ---------- templates ----------


def cmd_list_templates(args) -> int:
    params: dict[str, Any] = {}
    if args.search:
        params["query"] = args.search
    r = requests.get(f"{CANVA_API}/brand-templates", headers=_headers(), params=params, timeout=30)
    if not r.ok:
        print(f"{r.status_code}: {r.text[:400]}", file=sys.stderr)
        return 1
    items = r.json().get("items", [])
    if args.json:
        print(json.dumps(items, indent=2))
    else:
        for t in items:
            print(f"{t.get('id')}  {t.get('title', '')}")
            if t.get("thumbnail"):
                print(f"  thumbnail: {t['thumbnail'].get('url', '')}")
    return 0


# ---------- render ----------


def _autofill_template(template_id: str, data_fields: dict) -> str:
    """Kick off an autofill job; returns a design_id."""
    payload = {"brand_template_id": template_id, "data": data_fields}
    r = requests.post(
        f"{CANVA_API}/autofills",
        headers=_headers(),
        data=json.dumps(payload),
        timeout=60,
    )
    if not r.ok:
        raise RuntimeError(f"autofill start failed: {r.status_code} {r.text[:400]}")
    job = r.json().get("job", {})
    job_id = job.get("id")
    if not job_id:
        raise RuntimeError(f"no job id in autofill response: {r.json()}")

    # Poll
    for _ in range(60):
        r = requests.get(f"{CANVA_API}/autofills/{job_id}", headers=_headers(), timeout=30)
        if not r.ok:
            raise RuntimeError(f"autofill poll failed: {r.status_code} {r.text[:400]}")
        j = r.json().get("job", {})
        status = j.get("status")
        if status == "success":
            return j["result"]["design"]["id"]
        if status == "failed":
            raise RuntimeError(f"autofill failed: {j.get('error')}")
        time.sleep(2)
    raise RuntimeError("autofill timed out")


def _export_design(design_id: str, fmt: str = "png") -> str:
    """Kick off an export job; returns the download URL."""
    payload = {"design_id": design_id, "format": {"type": fmt}}
    r = requests.post(
        f"{CANVA_API}/exports",
        headers=_headers(),
        data=json.dumps(payload),
        timeout=60,
    )
    if not r.ok:
        raise RuntimeError(f"export start failed: {r.status_code} {r.text[:400]}")
    job = r.json().get("job", {})
    job_id = job.get("id")
    if not job_id:
        raise RuntimeError(f"no job id in export response: {r.json()}")

    for _ in range(60):
        r = requests.get(f"{CANVA_API}/exports/{job_id}", headers=_headers(), timeout=30)
        if not r.ok:
            raise RuntimeError(f"export poll failed: {r.status_code} {r.text[:400]}")
        j = r.json().get("job", {})
        status = j.get("status")
        if status == "success":
            urls = j.get("urls") or [u["url"] for u in j.get("result", {}).get("urls", [])]
            if not urls:
                raise RuntimeError(f"export success but no url: {j}")
            return urls[0]
        if status == "failed":
            raise RuntimeError(f"export failed: {j.get('error')}")
        time.sleep(2)
    raise RuntimeError("export timed out")


def cmd_render(args) -> int:
    vars_raw = args.vars
    try:
        data_fields = json.loads(vars_raw)
    except json.JSONDecodeError as e:
        print(f"--vars must be valid JSON: {e}", file=sys.stderr)
        return 2

    # Canva autofill expects data fields in a specific shape — either {"name": "value"}
    # or {"name": {"type": "text", "text": "value"}}. Normalize simple strings.
    normalized: dict[str, Any] = {}
    for k, v in data_fields.items():
        if isinstance(v, dict):
            normalized[k] = v
        else:
            normalized[k] = {"type": "text", "text": str(v)}

    design_id = _autofill_template(args.template, normalized)
    print(f"design_id: {design_id}", file=sys.stderr)
    url = _export_design(design_id, args.format)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, timeout=120, stream=True)
    r.raise_for_status()
    with out.open("wb") as f:
        for chunk in r.iter_content(65536):
            f.write(chunk)
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    print(f"design_url: https://www.canva.com/design/{design_id}/view")
    return 0


def cmd_render_from_brief(args) -> int:
    """Brief JSON shape: {template_id, vars, out}."""
    brief = json.loads(Path(args.brief).read_text())
    if isinstance(brief, dict):
        briefs = [brief]
    else:
        briefs = brief
    for i, b in enumerate(briefs):
        class A:
            pass
        a = A()
        a.template = b["template_id"]
        a.vars = json.dumps(b.get("vars", {}))
        a.format = b.get("format", "png")
        a.out = b.get("out") or f"{args.out_dir}/canva_render_{i}.png"
        rc = cmd_render(a)
        if rc != 0:
            return rc
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Canva Connect API wrapper")
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("list-templates")
    pl.add_argument("--search", default=None)
    pl.add_argument("--json", action="store_true")
    pl.set_defaults(func=cmd_list_templates)

    pr = sub.add_parser("render")
    pr.add_argument("--template", required=True, help="brand_template_id")
    pr.add_argument("--vars", required=True, help="JSON map of placeholder -> value")
    pr.add_argument("--format", default="png", choices=["png", "jpg", "pdf"])
    pr.add_argument("--out", required=True)
    pr.set_defaults(func=cmd_render)

    prb = sub.add_parser("render-from-brief")
    prb.add_argument("--brief", required=True)
    prb.add_argument("--out-dir", default=".tmp/graphics")
    prb.set_defaults(func=cmd_render_from_brief)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
