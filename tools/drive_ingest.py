#!/usr/bin/env python3
"""
Drive-to-catalog ingest wrapper.

Takes a JSON list of Drive file descriptors (produced by Claude via the Google
Workspace MCP listing a folder), runs the proven video_analyzer.py summary
on each video and a lightweight vision caption on each photo, then writes a
manifest that catalog_content.py ingest-drive consumes.

WAT split:
- Claude (orchestrator) lists Drive folders via the Workspace MCP and writes
  an input JSON file with {drive_file_id, filename, folder_month, mime_type,
  duration_sec, orientation, webContentLink}.
- This tool loops that list, calls the existing video_analyzer.py summary
  subprocess per video (re-using that tool's Gemini File API + download
  logic), or captions photos directly via google-genai, and assembles the
  manifest.
- catalog_content.py ingest-drive upserts the manifest into ChromaDB.

This keeps video analysis deterministic, uses the tool the production
routine already uses, and avoids re-implementing download/upload logic.

Input JSON shape:
[
  {
    "type": "video"|"photo",
    "drive_file_id": "...",
    "filename": "Content 1.mp4",
    "folder_month": "2026-03",
    "mime_type": "video/mp4",          # optional
    "duration_sec": 55.93,              # video only
    "orientation": "vertical"|"horizontal"|"square",
    "web_content_link": "https://drive..."
  }, ...
]

Usage:
    python tools/drive_ingest.py build-manifest \\
        --input .tmp/drive_input.json \\
        --output .tmp/drive_manifest.json [--limit N] [--skip-videos] [--skip-photos]

Then:
    python tools/catalog_content.py ingest-drive --manifest .tmp/drive_manifest.json
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VIDEO_ANALYZER = ROOT / "tools" / "video_analyzer.py"
TMP_DIR = ROOT / ".tmp"
TMP_DIR.mkdir(parents=True, exist_ok=True)


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


_PHOTO_PROMPT = (
    "Caption this photo for a commercial locksmith's (Anderson Lock & Safe, Phoenix AZ) "
    "social media content catalog. Write 2-3 sentences covering: what's in the frame, "
    "the type of work or product visible (lock, safe, door, hardware, technician on the "
    "job), the environment (office, retail, multi-tenant, warehouse, home), and any "
    "notable details (brand of hardware, before/after cue). Then on a new line starting "
    "with 'TAGS:' list 3-6 short lowercase comma-separated tags a marketer could filter "
    "on (e.g. TAGS: rekey, commercial, mul-t-lock, retail)."
)


def _orientation_from_dims(w: int, h: int) -> str:
    if not w or not h:
        return "unknown"
    if abs(w - h) / max(w, h) < 0.05:
        return "square"
    return "vertical" if h > w else "horizontal"


def _run_video_summary(drive_file_id: str) -> str:
    """Call the proven video_analyzer.py summary as a subprocess. Captures stdout."""
    proc = subprocess.run(
        [sys.executable, str(VIDEO_ANALYZER), "summary", drive_file_id],
        capture_output=True,
        text=True,
        timeout=900,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"video_analyzer failed: {proc.stderr.strip()[-400:]}")
    return proc.stdout.strip()


def _thumbnail_for_photo(drive_file_id: str, dest: Path) -> Path | None:
    """Fetch the high-res thumbnail via the public drive endpoint.

    Photos are small; we use the thumbnail at =s1600 which is plenty for
    vision captioning and avoids the full-file download.
    """
    url = f"https://drive.google.com/thumbnail?id={drive_file_id}&sz=s1600"
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "DriveIngest/1.0"}
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            dest.write_bytes(resp.read())
        if dest.stat().st_size < 1024:  # too small = error page
            return None
        return dest
    except Exception as e:
        print(f"  thumbnail fetch failed for {drive_file_id}: {e}", file=sys.stderr)
        return None


def _caption_photo(image_path: Path) -> tuple[str, list[str]]:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    mime = "image/jpeg"
    ext = image_path.suffix.lower()
    if ext == ".png":
        mime = "image/png"
    elif ext == ".webp":
        mime = "image/webp"

    image_bytes = image_path.read_bytes()
    backoff = 2.0
    for attempt in range(4):
        try:
            resp = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type=mime),
                    _PHOTO_PROMPT,
                ],
            )
            text = (resp.text or "").strip()
            break
        except Exception as e:
            if attempt == 3:
                raise
            msg = str(e).lower()
            if any(k in msg for k in ("rate", "quota", "429", "unavailable", "503")):
                time.sleep(backoff)
                backoff *= 2
            else:
                raise

    tags: list[str] = []
    body = text
    if "TAGS:" in text:
        idx = text.rfind("TAGS:")
        body = text[:idx].strip()
        tags = [t.strip().lower() for t in text[idx + 5:].split(",") if t.strip()]
    return body, tags


def build_manifest_cmd(args) -> int:
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"input not found: {input_path}", file=sys.stderr)
        return 1

    items = json.loads(input_path.read_text())
    if args.limit:
        items = items[: args.limit]

    manifest: list[dict] = []
    # Reuse prior run if resuming
    out_path = Path(args.output)
    done_ids: set[str] = set()
    if args.resume and out_path.exists():
        try:
            prior = json.loads(out_path.read_text())
            manifest = prior
            done_ids = {f"{m.get('type')}:{m.get('drive_file_id')}" for m in prior}
            print(f"resuming: {len(done_ids)} items already done", file=sys.stderr)
        except Exception:
            pass

    for i, it in enumerate(items):
        kind = it.get("type", "video")
        fid = it["drive_file_id"]
        key = f"{kind}:{fid}"
        if key in done_ids:
            print(f"[{i+1}/{len(items)}] skip (resume) {it.get('filename')}")
            continue

        if kind == "video" and args.skip_videos:
            print(f"[{i+1}/{len(items)}] skip-videos {it.get('filename')}")
            continue
        if kind == "photo" and args.skip_photos:
            print(f"[{i+1}/{len(items)}] skip-photos {it.get('filename')}")
            continue

        print(f"[{i+1}/{len(items)}] {kind}: {it.get('filename')}")
        photo_tags: list[str] = []
        try:
            if kind == "video":
                summary = _run_video_summary(fid)
            else:
                tmp_img = TMP_DIR / f"drive_thumb_{fid}.jpg"
                if not _thumbnail_for_photo(fid, tmp_img):
                    print(f"  ! no thumbnail available")
                    continue
                body, photo_tags = _caption_photo(tmp_img)
                summary = body
        except Exception as e:
            print(f"  ! failed: {e}", file=sys.stderr)
            # Flush partial progress
            _write_manifest(out_path, manifest)
            continue

        entry = {
            "type": kind,
            "drive_file_id": fid,
            "filename": it.get("filename", ""),
            "folder_month": it.get("folder_month", ""),
            "summary": summary.split("TAGS:")[0].strip() if "TAGS:" in summary else summary,
            "web_content_link": it.get("web_content_link", ""),
        }
        if kind == "photo":
            entry["tags"] = photo_tags
        elif "TAGS:" in summary:
            tag_line = summary.rsplit("TAGS:", 1)[-1]
            entry["tags"] = [t.strip().lower() for t in tag_line.split(",") if t.strip()]
        else:
            entry["tags"] = []
        if kind == "video":
            entry["duration_sec"] = float(it.get("duration_sec", 0) or 0)
            entry["orientation"] = it.get("orientation") or _orientation_from_dims(
                it.get("width", 0), it.get("height", 0)
            )
        manifest.append(entry)
        done_ids.add(key)
        # Flush after each item so long runs can resume after a crash
        _write_manifest(out_path, manifest)
        print(f"  ✓ {len(entry['summary'])} chars, tags={entry.get('tags')}")

    _write_manifest(out_path, manifest)
    print(f"\nmanifest written: {out_path} ({len(manifest)} items)")
    return 0


def _write_manifest(path: Path, manifest: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2))


def main() -> int:
    p = argparse.ArgumentParser(description="Drive-to-catalog ingest wrapper")
    sub = p.add_subparsers(dest="cmd", required=True)

    pb = sub.add_parser("build-manifest", help="run video_analyzer/photo caption over Drive files")
    pb.add_argument("--input", required=True)
    pb.add_argument("--output", required=True)
    pb.add_argument("--limit", type=int, default=0)
    pb.add_argument("--skip-videos", action="store_true")
    pb.add_argument("--skip-photos", action="store_true")
    pb.add_argument("--resume", action="store_true", default=True, help="resume from existing output file")
    pb.set_defaults(func=build_manifest_cmd)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
