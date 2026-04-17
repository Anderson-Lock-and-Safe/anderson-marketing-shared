#!/usr/bin/env python3
"""
Master content vector DB for Anderson Lock & Safe marketing agents.

Indexes three content types into three ChromaDB collections:
- assets_video  : DropKick Drive videos (Gemini summaries)
- assets_photo  : Drive photos + ServiceTitan job attachments (Gemini vision captions)
- copy          : past Buffer posts, pillar briefs, brand guidelines, engagement calendars

Search is filtered by type so the social media agent can ask:
    python tools/catalog_content.py search "property manager rekey" --type video --limit 5

Why separate collections? Metadata schemas diverge per type; keeping them apart
means filters are fast and the embedding space stays clean.

Ingestion is incremental: each source's content_hash is tracked in
.tmp/catalog_state.json. Re-running ingest is cheap — unchanged items are skipped.

The script itself is deterministic: it takes JSON manifests (produced by Claude
via MCP tools) and converts them into embeddings + ChromaDB upserts. The MCP
work (listing Drive folders, pulling Buffer posts, enumerating ServiceTitan jobs)
stays in Claude's orchestration layer — this matches the WAT architecture.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIR = ROOT / ".chroma"
STATE_FILE = ROOT / ".tmp" / "catalog_state.json"
TMP_DIR = ROOT / ".tmp"

TMP_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)


def _load_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ.setdefault(key.strip(), val.strip())


_load_env()


# ---------- state (incremental updates) ----------


def _load_state() -> dict[str, dict[str, Any]]:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text())
    except json.JSONDecodeError:
        return {}


def _save_state(state: dict[str, dict[str, Any]]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True))


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


# ---------- embeddings (Gemini text-embedding-004) ----------


_EMBED_MODEL = "gemini-embedding-001"
_EMBED_BATCH = 100


def _genai_client():
    from google import genai

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in .env")
    return genai.Client(api_key=api_key)


def _embed_texts(texts: list[str]) -> list[list[float]]:
    """Batch-embed with exponential backoff on rate limits."""
    from google.genai import types

    client = _genai_client()
    out: list[list[float]] = []
    for i in range(0, len(texts), _EMBED_BATCH):
        batch = texts[i : i + _EMBED_BATCH]
        backoff = 2.0
        for attempt in range(5):
            try:
                resp = client.models.embed_content(
                    model=_EMBED_MODEL,
                    contents=batch,
                    config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
                )
                out.extend([e.values for e in resp.embeddings])
                break
            except Exception as e:
                msg = str(e).lower()
                if attempt == 4 or ("rate" not in msg and "quota" not in msg and "429" not in msg):
                    raise
                time.sleep(backoff)
                backoff *= 2
    return out


def _embed_query(text: str) -> list[float]:
    from google.genai import types

    client = _genai_client()
    resp = client.models.embed_content(
        model=_EMBED_MODEL,
        contents=[text],
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    )
    return resp.embeddings[0].values


# ---------- ChromaDB client ----------


def _client():
    import chromadb

    return chromadb.PersistentClient(path=str(CHROMA_DIR))


COLLECTIONS = ("assets_video", "assets_photo", "copy")


def _collection(name: str):
    client = _client()
    return client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})


# ---------- chunking (for copy only) ----------


def _chunk_text(text: str, target_tokens: int = 500, overlap_tokens: int = 50) -> list[str]:
    """Rough token-based chunking using whitespace-split as a proxy (~1 token ≈ 0.75 words)."""
    words = text.split()
    if not words:
        return []
    # approximate: target_words = target_tokens * 0.75
    step = max(1, int(target_tokens * 0.75))
    ov = max(0, int(overlap_tokens * 0.75))
    chunks = []
    i = 0
    while i < len(words):
        end = min(len(words), i + step)
        chunk = " ".join(words[i:end])
        chunks.append(chunk)
        if end == len(words):
            break
        i = end - ov
    return chunks


# ---------- ingestion: drive videos ----------


@dataclass
class VideoItem:
    drive_file_id: str
    filename: str
    folder_month: str
    summary: str
    duration_sec: float = 0.0
    orientation: str = "unknown"
    web_content_link: str = ""


def _read_manifest(path: Path) -> list[dict]:
    data = json.loads(path.read_text())
    return data if isinstance(data, list) else data.get("items", [])


def ingest_drive(args) -> int:
    """Index Drive video summaries + photo captions from a JSON manifest.

    Expected manifest shape (produced by Claude via Google Workspace MCP + video_analyzer.py):
    [
      {
        "type": "video"|"photo",
        "drive_file_id": "...",
        "filename": "Content 1.mp4",
        "folder_month": "2026-04",
        "summary": "Gemini summary or photo caption",
        "duration_sec": 30.0,            # video only
        "orientation": "horizontal"|"vertical",
        "web_content_link": "https://drive..."
      }, ...
    ]
    """
    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"manifest not found: {manifest_path}", file=sys.stderr)
        return 1

    items = _read_manifest(manifest_path)
    state = _load_state()
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    new_ids, updated_ids, skipped = 0, 0, 0
    video_batch: list[tuple[str, str, dict]] = []
    photo_batch: list[tuple[str, str, dict]] = []

    for it in items:
        kind = it.get("type", "video")
        src_id = f"drive:{kind}:{it['drive_file_id']}"
        doc = it.get("summary", "").strip()
        if not doc:
            continue
        h = _content_hash(doc)
        prev = state.get(src_id)
        if prev and prev.get("hash") == h:
            skipped += 1
            continue
        meta = {
            "source": "drive",
            "drive_file_id": it["drive_file_id"],
            "filename": it.get("filename", ""),
            "folder_month": it.get("folder_month", ""),
            "content_hash": h,
            "indexed_at": now,
        }
        if kind == "video":
            meta.update(
                {
                    "duration_sec": float(it.get("duration_sec", 0) or 0),
                    "orientation": it.get("orientation", "unknown"),
                    "webContentLink": it.get("web_content_link", ""),
                }
            )
            video_batch.append((src_id, doc, meta))
        else:
            meta["tags"] = ",".join(it.get("tags", []))
            photo_batch.append((src_id, doc, meta))
        if prev:
            updated_ids += 1
        else:
            new_ids += 1
        state[src_id] = {"hash": h, "last_indexed": now}

    _upsert(_collection("assets_video"), video_batch)
    _upsert(_collection("assets_photo"), photo_batch)
    _save_state(state)

    print(
        f"drive ingest: {new_ids} new, {updated_ids} updated, {skipped} skipped "
        f"(videos={len(video_batch)}, photos={len(photo_batch)})"
    )
    return 0


# ---------- ingestion: servicetitan photos ----------


def ingest_servicetitan(args) -> int:
    """Index ServiceTitan job attachment captions from a manifest.

    Manifest produced by tools/servicetitan_photos.py. Shape:
    [
      {
        "attachment_id": "...",
        "job_id": "...",
        "filename": "...",
        "caption": "Gemini vision caption",
        "local_path": ".tmp/servicetitan_photos/xxx.jpg",
        "tags": ["rekey","commercial"]
      }, ...
    ]
    """
    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"manifest not found: {manifest_path}", file=sys.stderr)
        return 1

    items = _read_manifest(manifest_path)
    state = _load_state()
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    new_ids, updated_ids, skipped = 0, 0, 0
    batch: list[tuple[str, str, dict]] = []

    for it in items:
        src_id = f"st:{it['attachment_id']}"
        doc = it.get("caption", "").strip()
        if not doc:
            continue
        h = _content_hash(doc)
        prev = state.get(src_id)
        if prev and prev.get("hash") == h:
            skipped += 1
            continue
        meta = {
            "source": "servicetitan",
            "source_id": it["attachment_id"],
            "job_id": str(it.get("job_id", "")),
            "filename": it.get("filename", ""),
            "tags": ",".join(it.get("tags", [])),
            "local_path": it.get("local_path", ""),
            "content_hash": h,
            "indexed_at": now,
        }
        batch.append((src_id, doc, meta))
        if prev:
            updated_ids += 1
        else:
            new_ids += 1
        state[src_id] = {"hash": h, "last_indexed": now}

    _upsert(_collection("assets_photo"), batch)
    _save_state(state)
    print(f"servicetitan ingest: {new_ids} new, {updated_ids} updated, {skipped} skipped")
    return 0


# ---------- ingestion: copy (markdown + buffer posts) ----------


_COPY_INCLUDE_GLOBS = [
    "anderson-lock-and-safe-ai-guidelines.md",
    "engagement-posts-calendar-*.md",
    "workflows/social-media.md",
    "Pillar Content Pipeline - Architecture Plan.md",
    "brand/style_guide.md",
    "brand/style_references.md",
    "workflows/tasks/generate-engagement-post.md",
]


def _discover_copy_files() -> list[Path]:
    out: list[Path] = []
    for pat in _COPY_INCLUDE_GLOBS:
        for p in ROOT.glob(pat):
            if p.is_file():
                out.append(p)
    return sorted(set(out))


def ingest_copy(args) -> int:
    """Index repo markdown copy + past Buffer posts.

    Buffer posts can optionally be supplied via --buffer-manifest (produced by
    Claude running `buffer_publish.py posts --channel <ch>` and collecting output).
    Shape:
    [
      {"post_id": "...", "platform": "facebook",
       "text": "caption text", "published_at": "2026-04-01T...",
       "updated_at": "...", "status": "sent"}, ...
    ]
    """
    state = _load_state()
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    coll = _collection("copy")

    new_ids, updated_ids, skipped = 0, 0, 0
    batch: list[tuple[str, str, dict]] = []

    # markdown files
    for path in _discover_copy_files():
        text = path.read_text()
        source_type = _classify_copy_source(path)
        chunks = _chunk_text(text)
        for idx, chunk in enumerate(chunks):
            src_id = f"file:{path.relative_to(ROOT)}:{idx}"
            h = _content_hash(chunk)
            prev = state.get(src_id)
            if prev and prev.get("hash") == h:
                skipped += 1
                continue
            meta = {
                "source_type": source_type,
                "path": str(path.relative_to(ROOT)),
                "chunk_idx": idx,
                "content_hash": h,
                "indexed_at": now,
            }
            batch.append((src_id, chunk, meta))
            if prev:
                updated_ids += 1
            else:
                new_ids += 1
            state[src_id] = {"hash": h, "last_indexed": now}

    # buffer posts from manifest
    if args.buffer_manifest:
        bm = Path(args.buffer_manifest)
        if bm.exists():
            posts = _read_manifest(bm)
            for p in posts:
                src_id = f"buffer:{p['post_id']}"
                doc = p.get("text", "").strip()
                if not doc:
                    continue
                h = _content_hash(doc + p.get("updated_at", ""))
                prev = state.get(src_id)
                if prev and prev.get("hash") == h:
                    skipped += 1
                    continue
                meta = {
                    "source_type": "buffer_post",
                    "platform": p.get("platform", ""),
                    "post_id": p["post_id"],
                    "published_at": p.get("published_at", ""),
                    "status": p.get("status", ""),
                    "chunk_idx": 0,
                    "content_hash": h,
                    "indexed_at": now,
                }
                batch.append((src_id, doc, meta))
                if prev:
                    updated_ids += 1
                else:
                    new_ids += 1
                state[src_id] = {"hash": h, "last_indexed": now}
        else:
            print(f"buffer-manifest not found, skipping: {bm}", file=sys.stderr)

    _upsert(coll, batch)
    _save_state(state)
    print(f"copy ingest: {new_ids} new, {updated_ids} updated, {skipped} skipped")
    return 0


def _classify_copy_source(path: Path) -> str:
    name = path.name.lower()
    if "engagement-posts-calendar" in name:
        return "engagement_calendar"
    if "ai-guidelines" in name:
        return "brand_guidelines"
    if "style_guide" in name or "style_references" in name:
        return "brand_style"
    if "pillar" in name:
        return "pillar_brief"
    if "social-media" in name:
        return "social_workflow"
    return "other"


# ---------- upsert helper ----------


def _upsert(collection, batch: list[tuple[str, str, dict]]) -> None:
    if not batch:
        return
    ids = [b[0] for b in batch]
    docs = [b[1] for b in batch]
    metas = [b[2] for b in batch]
    embeds = _embed_texts(docs)
    collection.upsert(ids=ids, documents=docs, metadatas=metas, embeddings=embeds)


# ---------- search ----------


def search(args) -> int:
    query_emb = _embed_query(args.query)
    type_map = {
        "video": "assets_video",
        "photo": "assets_photo",
        "copy": "copy",
    }
    collections = [type_map[args.type]] if args.type else list(COLLECTIONS)

    all_hits = []
    for cname in collections:
        try:
            coll = _collection(cname)
        except Exception:
            continue
        if coll.count() == 0:
            continue
        res = coll.query(query_embeddings=[query_emb], n_results=args.limit)
        ids = res.get("ids", [[]])[0]
        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        dists = res.get("distances", [[]])[0]
        for i, doc, meta, dist in zip(ids, docs, metas, dists):
            all_hits.append(
                {
                    "collection": cname,
                    "id": i,
                    "score": round(1.0 - float(dist), 4),
                    "text": doc,
                    "metadata": meta,
                }
            )

    all_hits.sort(key=lambda h: -h["score"])
    all_hits = all_hits[: args.limit]

    if args.json:
        print(json.dumps(all_hits, indent=2))
    else:
        if not all_hits:
            print("(no results)")
            return 0
        for h in all_hits:
            print(f"[{h['collection']}] score={h['score']} id={h['id']}")
            m = h["metadata"]
            if h["collection"] == "assets_video":
                print(
                    f"  {m.get('filename')} ({m.get('folder_month')}) — "
                    f"{m.get('duration_sec', 0):.0f}s {m.get('orientation', '')}"
                )
                if m.get("webContentLink"):
                    print(f"  link: {m['webContentLink']}")
            elif h["collection"] == "assets_photo":
                print(
                    f"  {m.get('filename')} — source={m.get('source')} "
                    f"job={m.get('job_id', '')}"
                )
            else:
                print(f"  {m.get('source_type')} — {m.get('path', m.get('post_id', ''))}")
            text_preview = h["text"][:220].replace("\n", " ")
            print(f"  {text_preview}{'...' if len(h['text']) > 220 else ''}")
            print()
    return 0


# ---------- Canva asset cache ----------


def _photo_collection():
    return _collection("assets_photo")


def get_canva_asset_id(catalog_id: str) -> str | None:
    """Return cached Canva asset_id for a photo catalog entry, or None if not uploaded yet."""
    coll = _photo_collection()
    res = coll.get(ids=[catalog_id], include=["metadatas"])
    metas = res.get("metadatas") or []
    if not metas:
        return None
    aid = metas[0].get("canva_asset_id") if metas[0] else None
    return aid or None


def set_canva_asset_id(catalog_id: str, asset_id: str) -> None:
    """Cache the Canva asset_id on an existing photo catalog entry."""
    coll = _photo_collection()
    res = coll.get(ids=[catalog_id], include=["metadatas"])
    metas = res.get("metadatas") or []
    if not metas:
        raise KeyError(f"catalog entry not found: {catalog_id}")
    meta = dict(metas[0] or {})
    meta["canva_asset_id"] = asset_id
    meta["canva_uploaded_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    coll.update(ids=[catalog_id], metadatas=[meta])


def canva_cache_cmd(args) -> int:
    """CLI: get or set Canva asset_id cache on a photo. Used by Claude orchestrator."""
    if args.action == "get":
        aid = get_canva_asset_id(args.id)
        print(json.dumps({"catalog_id": args.id, "canva_asset_id": aid}))
        return 0
    if args.action == "set":
        if not args.asset_id:
            print("--asset-id required for set", file=sys.stderr)
            return 1
        set_canva_asset_id(args.id, args.asset_id)
        print(json.dumps({"catalog_id": args.id, "canva_asset_id": args.asset_id, "cached": True}))
        return 0
    print(f"unknown action: {args.action}", file=sys.stderr)
    return 1


# ---------- stats + reset ----------


def stats(args) -> int:
    total = 0
    for cname in COLLECTIONS:
        coll = _collection(cname)
        n = coll.count()
        total += n
        print(f"{cname:15s} {n:>6d}")
    print(f"{'total':15s} {total:>6d}")
    state = _load_state()
    print(f"state entries:  {len(state)}")
    print(f"chroma dir:     {CHROMA_DIR}")
    return 0


def reset(args) -> int:
    if not args.yes:
        print("refusing to reset without --yes", file=sys.stderr)
        return 1
    import chromadb

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    for cname in COLLECTIONS:
        try:
            client.delete_collection(name=cname)
            print(f"deleted {cname}")
        except Exception as e:
            print(f"skip {cname}: {e}")
    if STATE_FILE.exists():
        STATE_FILE.unlink()
        print(f"deleted {STATE_FILE}")
    return 0


# ---------- main ----------


def main() -> int:
    p = argparse.ArgumentParser(description="Anderson marketing content vector DB")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_drive = sub.add_parser("ingest-drive", help="index Drive videos/photos from a manifest")
    p_drive.add_argument("--manifest", required=True, help="path to drive manifest JSON")
    p_drive.set_defaults(func=ingest_drive)

    p_st = sub.add_parser("ingest-servicetitan", help="index ServiceTitan photos from a manifest")
    p_st.add_argument("--manifest", required=True, help="path to servicetitan manifest JSON")
    p_st.set_defaults(func=ingest_servicetitan)

    p_copy = sub.add_parser("ingest-copy", help="index repo markdown + Buffer posts")
    p_copy.add_argument("--buffer-manifest", help="optional buffer posts JSON manifest", default=None)
    p_copy.set_defaults(func=ingest_copy)

    p_search = sub.add_parser("search", help="semantic search across collections")
    p_search.add_argument("query")
    p_search.add_argument("--type", choices=["video", "photo", "copy"], default=None)
    p_search.add_argument("--limit", type=int, default=5)
    p_search.add_argument("--json", action="store_true")
    p_search.set_defaults(func=search)

    p_canva = sub.add_parser("canva-cache", help="get/set Canva asset_id cache on a photo catalog entry")
    p_canva.add_argument("action", choices=["get", "set"])
    p_canva.add_argument("--id", required=True, help="catalog id, e.g. drive:photo:<drive_file_id>")
    p_canva.add_argument("--asset-id", help="Canva asset_id (required for 'set')")
    p_canva.set_defaults(func=canva_cache_cmd)

    p_stats = sub.add_parser("stats", help="show collection counts")
    p_stats.set_defaults(func=stats)

    p_reset = sub.add_parser("reset", help="drop all collections and state")
    p_reset.add_argument("--yes", action="store_true")
    p_reset.set_defaults(func=reset)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
