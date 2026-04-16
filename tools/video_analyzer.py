#!/usr/bin/env python3
"""
Video Analyzer Tool — WAT Framework
Sends a video to Google Gemini for scene-by-scene analysis.

Usage:
    python tools/video_analyzer.py analyze <google_drive_file_id> [--prompt "custom prompt"]
    python tools/video_analyzer.py analyze-url <video_url> [--prompt "custom prompt"]
    python tools/video_analyzer.py summary <google_drive_file_id>

Environment:
    GEMINI_API_KEY — Google AI Studio API key (required)
    BUFFER_TOKEN   — Not needed, but .env is shared

The tool downloads the video from Google Drive (via webContentLink),
uploads it to Gemini's File API, then asks Gemini to analyze it.

Output is a structured analysis that agents can use to:
- Write captions and post copy
- Decide which platform to post on (reel vs feed vs story)
- Plan content sequencing
- Create edit instructions for repurposing
"""

import json
import os
import sys
import tempfile
import time
import urllib.request
import urllib.error

# ── Config ──────────────────────────────────────────────────────────────────

GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_UPLOAD_URL = "https://generativelanguage.googleapis.com/upload/v1beta/files"
GEMINI_GENERATE_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
GEMINI_FILE_URL = "https://generativelanguage.googleapis.com/v1beta/files/{name}"

DEFAULT_ANALYSIS_PROMPT = """Analyze this video for social media marketing purposes. Provide:

## Video Overview
- Duration and format (vertical/horizontal/square)
- Overall quality assessment
- Setting/location description

## Scene Breakdown
For each distinct scene or segment:
- Timestamp range (e.g., 0:00-0:15)
- What's happening visually
- Any text on screen
- Any spoken words or narration (transcribe key quotes)
- Mood/energy level

## People & Branding
- Who appears (describe roles — technician, customer, office staff, etc.)
- Anderson Lock and Safe branding visible (uniforms, vehicles, signage, tools)
- Any customer interactions

## Social Media Recommendations
- Best platform(s): Facebook, LinkedIn, Instagram Reel, Instagram Story, YouTube
- Suggested caption angle (what story does this tell?)
- 3 caption options (casual FB tone, professional LI tone, short IG tone)
- Best thumbnail moment (timestamp)
- Should this be posted as-is, or trimmed? If trimmed, suggest cut points.
- Any content warnings or things to avoid highlighting

## Repurposing Potential
- Can this be cut into multiple shorter clips? If so, suggest segments.
- Still frames worth extracting as photos?
- Audio worth using separately (quotes, soundbites)?

Keep responses specific to what you actually see in the video. Do not make up details."""

SUMMARY_PROMPT = """Give me a brief 3-4 sentence summary of this video:
- What's happening
- Who's in it
- What it would be useful for in marketing
- Suggested platform (Facebook, LinkedIn, Instagram Reel, YouTube)"""


# ── API Key ─────────────────────────────────────────────────────────────────

def get_api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key

    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")

    print("Error: GEMINI_API_KEY not set. Set it as an env var or in .env", file=sys.stderr)
    print("Get a key at: https://aistudio.google.com/apikey", file=sys.stderr)
    sys.exit(1)


# ── HTTP Helper ─────────────────────────────────────────────────────────────

def api_request(url, data=None, headers=None, method="GET"):
    if headers is None:
        headers = {}
    headers.setdefault("User-Agent", "VideoAnalyzer/1.0 (Anderson Lock WAT)")

    if data and isinstance(data, dict):
        data = json.dumps(data).encode("utf-8")
        headers.setdefault("Content-Type", "application/json")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


# ── Download from Google Drive ──────────────────────────────────────────────

def download_drive_file(file_id, dest_path):
    """Download a file from Google Drive using the export URL."""
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    print(f"Downloading from Google Drive: {file_id}...", file=sys.stderr)

    req = urllib.request.Request(url, headers={
        "User-Agent": "VideoAnalyzer/1.0"
    })

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            with open(dest_path, "wb") as f:
                total = 0
                while True:
                    chunk = resp.read(1024 * 1024)  # 1MB chunks
                    if not chunk:
                        break
                    f.write(chunk)
                    total += len(chunk)
                    print(f"  Downloaded {total / 1024 / 1024:.1f} MB...", file=sys.stderr)
    except urllib.error.HTTPError as e:
        print(f"Download failed (HTTP {e.code}). File may not be shared publicly.", file=sys.stderr)
        print("Ensure the file has 'Anyone with the link' sharing enabled.", file=sys.stderr)
        sys.exit(1)

    print(f"  Done. {total / 1024 / 1024:.1f} MB downloaded.", file=sys.stderr)
    return dest_path


# ── Gemini File Upload ──────────────────────────────────────────────────────

def upload_to_gemini(file_path, mime_type="video/mp4"):
    """Upload a file to Gemini's File API for processing."""
    api_key = get_api_key()
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)

    print(f"Uploading to Gemini ({file_size / 1024 / 1024:.1f} MB)...", file=sys.stderr)

    # Start resumable upload
    url = f"{GEMINI_UPLOAD_URL}?key={api_key}"
    headers = {
        "X-Goog-Upload-Protocol": "resumable",
        "X-Goog-Upload-Command": "start",
        "X-Goog-Upload-Header-Content-Length": str(file_size),
        "X-Goog-Upload-Header-Content-Type": mime_type,
        "Content-Type": "application/json",
        "User-Agent": "VideoAnalyzer/1.0",
    }
    metadata = json.dumps({"file": {"display_name": file_name}}).encode("utf-8")

    req = urllib.request.Request(url, data=metadata, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        upload_url = resp.headers.get("X-Goog-Upload-URL")

    if not upload_url:
        print("Failed to get upload URL from Gemini.", file=sys.stderr)
        sys.exit(1)

    # Upload the file
    with open(file_path, "rb") as f:
        file_data = f.read()

    upload_headers = {
        "Content-Length": str(file_size),
        "X-Goog-Upload-Offset": "0",
        "X-Goog-Upload-Command": "upload, finalize",
        "User-Agent": "VideoAnalyzer/1.0",
    }

    req = urllib.request.Request(upload_url, data=file_data, headers=upload_headers, method="PUT")
    with urllib.request.urlopen(req, timeout=600) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    file_uri = result["file"]["uri"]
    file_name = result["file"]["name"]
    state = result["file"].get("state", "PROCESSING")

    print(f"  Upload complete. File: {file_name}", file=sys.stderr)

    # Wait for processing
    while state == "PROCESSING":
        print("  Waiting for Gemini to process video...", file=sys.stderr)
        time.sleep(5)
        check_url = f"https://generativelanguage.googleapis.com/v1beta/{file_name}?key={api_key}"
        status = api_request(check_url)
        state = status.get("state", "ACTIVE")

    if state == "FAILED":
        print("Gemini failed to process the video.", file=sys.stderr)
        sys.exit(1)

    print("  Video ready for analysis.", file=sys.stderr)
    return file_uri


# ── Gemini Analysis ────────────────────────────────────────────────────────

def analyze_video(file_uri, prompt, retries=3):
    """Send a video to Gemini for analysis."""
    api_key = get_api_key()
    url = GEMINI_GENERATE_URL.format(model=GEMINI_MODEL) + f"?key={api_key}"

    payload = {
        "contents": [{
            "parts": [
                {"file_data": {"mime_type": "video/mp4", "file_uri": file_uri}},
                {"text": prompt}
            ]
        }]
    }

    print("Analyzing video with Gemini...", file=sys.stderr)

    for attempt in range(retries):
        try:
            result = api_request(url, data=payload)
            break
        except SystemExit:
            if attempt < retries - 1:
                wait = 30 * (attempt + 1)
                print(f"  Gemini unavailable, retrying in {wait}s (attempt {attempt + 2}/{retries})...", file=sys.stderr)
                time.sleep(wait)
            else:
                raise

    # Extract the text response
    candidates = result.get("candidates", [])
    if not candidates:
        print("Gemini returned no response.", file=sys.stderr)
        sys.exit(1)

    parts = candidates[0].get("content", {}).get("parts", [])
    text = "\n".join(p.get("text", "") for p in parts if "text" in p)

    # Print token usage
    usage = result.get("usageMetadata", {})
    if usage:
        print(f"\nTokens — Input: {usage.get('promptTokenCount', '?')}, "
              f"Output: {usage.get('candidatesTokenCount', '?')}, "
              f"Total: {usage.get('totalTokenCount', '?')}", file=sys.stderr)

    return text


# ── Commands ────────────────────────────────────────────────────────────────

def cmd_analyze(file_id, prompt=None):
    """Download a video from Google Drive and analyze it."""
    if prompt is None:
        prompt = DEFAULT_ANALYSIS_PROMPT

    with tempfile.TemporaryDirectory() as tmp:
        video_path = os.path.join(tmp, "video.mp4")
        download_drive_file(file_id, video_path)
        file_uri = upload_to_gemini(video_path)
        analysis = analyze_video(file_uri, prompt)
        print(analysis)


def cmd_summary(file_id):
    """Quick summary of a video."""
    cmd_analyze(file_id, prompt=SUMMARY_PROMPT)


def cmd_analyze_url(video_url, prompt=None):
    """Download a video from a URL and analyze it."""
    if prompt is None:
        prompt = DEFAULT_ANALYSIS_PROMPT

    with tempfile.TemporaryDirectory() as tmp:
        video_path = os.path.join(tmp, "video.mp4")
        print(f"Downloading from URL...", file=sys.stderr)

        req = urllib.request.Request(video_url, headers={"User-Agent": "VideoAnalyzer/1.0"})
        with urllib.request.urlopen(req, timeout=300) as resp:
            with open(video_path, "wb") as f:
                f.write(resp.read())

        print(f"  Done. {os.path.getsize(video_path) / 1024 / 1024:.1f} MB", file=sys.stderr)
        file_uri = upload_to_gemini(video_path)
        analysis = analyze_video(file_uri, prompt)
        print(analysis)


# ── CLI ─────────────────────────────────────────────────────────────────────

def print_usage():
    print(__doc__)


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        print_usage()
        sys.exit(0)

    command = args[0].lower()

    custom_prompt = None
    if "--prompt" in args:
        idx = args.index("--prompt")
        if idx + 1 < len(args):
            custom_prompt = args[idx + 1]

    if command == "analyze" and len(args) >= 2:
        cmd_analyze(args[1], prompt=custom_prompt)

    elif command == "analyze-url" and len(args) >= 2:
        cmd_analyze_url(args[1], prompt=custom_prompt)

    elif command == "summary" and len(args) >= 2:
        cmd_summary(args[1])

    else:
        print(f"Unknown command or missing args: {command}", file=sys.stderr)
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
