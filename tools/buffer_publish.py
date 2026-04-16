#!/usr/bin/env python3
"""
Buffer Publish Tool — WAT Framework
Posts to Buffer's GraphQL API using a bearer token.

Usage:
    python tools/buffer_publish.py channels
    python tools/buffer_publish.py schedule <channel> "<text>" [--date "2026-04-20T10:00:00-07:00"]
    python tools/buffer_publish.py queue <channel> "<text>"
    python tools/buffer_publish.py draft <channel> "<text>"
    python tools/buffer_publish.py posts [--channel <channel>] [--status <status>]
    python tools/buffer_publish.py account

Environment:
    BUFFER_TOKEN — Bearer token for api.buffer.com (required)
                   Falls back to .env file in project root.

Channel shortcuts:
    fb, facebook    → Anderson Lock and Safe (Facebook page)
    li, linkedin    → anderson-lock-and-safe (LinkedIn page)
    ig, instagram   → andersonlockphx (Instagram business)
    yt, youtube     → Anderson Lock and Safe (YouTube channel)
    gbp-phoenix     → Anderson Lock & Safe - Phoenix Locksmith
    gbp-chandler    → Anderson Lock and Safe - Chandler Locksmith
    gbp-arcadia     → Anderson Lock and Safe - Arcadia Locksmith
"""

import json
import os
import sys
import urllib.request
import urllib.error

# ── Config ──────────────────────────────────────────────────────────────────

API_URL = "https://api.buffer.com/graphql"
ORG_ID = "69dd19b9c941c3b168a916c6"

CHANNEL_MAP = {
    "fb": "69dd1a1d031bfa423cfca01e",
    "facebook": "69dd1a1d031bfa423cfca01e",
    "li": "69dd1ba5031bfa423cfca620",
    "linkedin": "69dd1ba5031bfa423cfca620",
    "ig": "69dd1a05031bfa423cfc9fbd",
    "instagram": "69dd1a05031bfa423cfc9fbd",
    "yt": "69dd39dc031bfa423cfd48d2",
    "youtube": "69dd39dc031bfa423cfd48d2",
    "gbp-phoenix": "69dd39fe031bfa423cfd4943",
    "gbp-chandler": "69dd39fe031bfa423cfd4944",
    "gbp-arcadia": "69dd39fe031bfa423cfd4945",
}

CHANNEL_NAMES = {
    "69dd1a1d031bfa423cfca01e": "Facebook — Anderson Lock and Safe",
    "69dd1ba5031bfa423cfca620": "LinkedIn — anderson-lock-and-safe",
    "69dd1a05031bfa423cfc9fbd": "Instagram — andersonlockphx",
    "69dd39dc031bfa423cfd48d2": "YouTube — Anderson Lock and Safe",
    "69dd39fe031bfa423cfd4943": "GBP — Phoenix Locksmith",
    "69dd39fe031bfa423cfd4944": "GBP — Chandler Locksmith",
    "69dd39fe031bfa423cfd4945": "GBP — Arcadia Locksmith",
}


# ── Token ───────────────────────────────────────────────────────────────────

def get_token():
    token = os.environ.get("BUFFER_TOKEN")
    if token:
        return token

    # Try .env file
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("BUFFER_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")

    print("Error: BUFFER_TOKEN not set. Set it as an env var or in .env", file=sys.stderr)
    sys.exit(1)


# ── GraphQL Client ──────────────────────────────────────────────────────────

def graphql(query, variables=None):
    token = get_token()
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "BufferPublishTool/1.0 (Anderson Lock WAT Framework)",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)

    if "errors" in result:
        for err in result["errors"]:
            print(f"GraphQL Error: {err['message']}", file=sys.stderr)
        if not result.get("data"):
            sys.exit(1)

    return result.get("data", {})


# ── Commands ────────────────────────────────────────────────────────────────

def cmd_account():
    data = graphql("""
        { account { id email organizations { id name } } }
    """)
    acct = data["account"]
    print(f"Email: {acct['email']}")
    for org in acct["organizations"]:
        print(f"Org: {org['name']} (ID: {org['id']})")
        print(f"Timezone: {org.get('timezone', 'not set')}")


def cmd_channels():
    data = graphql("""
        query($input: ChannelsInput!) {
            channels(input: $input) {
                id name service type isDisconnected
            }
        }
    """, {"input": {"organizationId": ORG_ID}})

    channels = data.get("channels", [])
    if not channels:
        print("No channels found.")
        return

    print(f"{'Shortcut':<14} {'Service':<12} {'Name':<40} {'Status'}")
    print("-" * 80)
    for ch in channels:
        shortcut = next((k for k, v in CHANNEL_MAP.items() if v == ch["id"] and len(k) <= 2), "")
        if not shortcut:
            shortcut = next((k for k, v in CHANNEL_MAP.items() if v == ch["id"]), ch["id"][:8])
        status = "DISCONNECTED" if ch.get("isDisconnected") else "OK"
        print(f"{shortcut:<14} {ch['service']:<12} {ch['name']:<40} {status}")


def resolve_channel(channel_arg):
    """Resolve a channel shortcut or ID to a channel ID."""
    if channel_arg.lower() in CHANNEL_MAP:
        return CHANNEL_MAP[channel_arg.lower()]
    # Check if it's a raw ID
    if len(channel_arg) == 24:
        return channel_arg
    print(f"Unknown channel: {channel_arg}", file=sys.stderr)
    print(f"Valid shortcuts: {', '.join(sorted(set(CHANNEL_MAP.keys())))}", file=sys.stderr)
    sys.exit(1)


def cmd_create_post(channel_arg, text, mode="addToQueue", due_at=None, save_to_draft=False, video_url=None, image_url=None):
    channel_id = resolve_channel(channel_arg)
    channel_name = CHANNEL_NAMES.get(channel_id, channel_id)

    # Determine the service for platform-specific metadata
    service = None
    for ch_id, name in CHANNEL_NAMES.items():
        if ch_id == channel_id:
            if "Facebook" in name:
                service = "facebook"
            elif "LinkedIn" in name:
                service = "linkedin"
            elif "Instagram" in name:
                service = "instagram"
            elif "YouTube" in name:
                service = "youtube"
            elif "GBP" in name:
                service = "googlebusiness"
            break

    variables = {
        "input": {
            "channelId": channel_id,
            "text": text,
            "mode": mode,
            "schedulingType": "automatic",
            "aiAssisted": True,
            "source": "claude-code-wat",
        }
    }

    # Platform-specific metadata
    metadata = {}
    if service == "facebook":
        metadata["facebook"] = {"type": "post"}
    elif service == "instagram":
        metadata["instagram"] = {"type": "post", "shouldShareToFeed": True}
    elif service == "googlebusiness":
        metadata["google"] = {"type": "whats_new", "detailsWhatsNew": {"button": "none"}}
    if metadata:
        variables["input"]["metadata"] = metadata

    # Media assets
    assets = {}
    if video_url:
        assets["videos"] = [{"url": video_url}]
    if image_url:
        assets["images"] = [{"url": image_url}]
    if assets:
        variables["input"]["assets"] = assets

    if due_at:
        variables["input"]["dueAt"] = due_at

    if save_to_draft:
        variables["input"]["saveToDraft"] = True

    data = graphql("""
        mutation($input: CreatePostInput!) {
            createPost(input: $input) {
                ... on PostActionSuccess {
                    post { id status dueAt channel { name service } }
                }
                ... on NotFoundError { message }
                ... on UnauthorizedError { message }
                ... on UnexpectedError { message }
                ... on RestProxyError { message code }
                ... on LimitReachedError { message }
                ... on InvalidInputError { message }
            }
        }
    """, variables)

    result = data.get("createPost", {})

    # Check for error types
    if "message" in result and "post" not in result:
        print(f"Buffer error: {result['message']}", file=sys.stderr)
        sys.exit(1)

    post = result.get("post")
    if not post:
        print("Failed to create post — no post returned.", file=sys.stderr)
        print(f"Response: {json.dumps(result)}", file=sys.stderr)
        sys.exit(1)

    print(f"Post created successfully!")
    print(f"  ID: {post['id']}")
    print(f"  Channel: {channel_name}")
    print(f"  Status: {post.get('status', 'unknown')}")
    if post.get("dueAt"):
        print(f"  Scheduled: {post['dueAt']}")
    if save_to_draft:
        print(f"  Saved as: DRAFT")
    else:
        print(f"  Mode: {mode}")

    return post


def cmd_posts(channel_arg=None, status_filter=None):
    input_obj = {"organizationId": ORG_ID}
    filter_obj = {}
    if channel_arg:
        filter_obj["channelIds"] = [resolve_channel(channel_arg)]
    if status_filter:
        filter_obj["status"] = status_filter
    if filter_obj:
        input_obj["filter"] = filter_obj

    data = graphql("""
        query($input: PostsInput!, $first: Int) {
            posts(input: $input, first: $first) {
                edges {
                    node {
                        id text status dueAt
                        channel { name service }
                    }
                }
            }
        }
    """, {"input": input_obj, "first": 20})

    posts = data.get("posts", {})
    edges = posts.get("edges", [])

    if not edges:
        print("No posts found.")
        return

    print(f"{'Status':<12} {'Channel':<20} {'Scheduled':<22} {'Text (preview)'}")
    print("-" * 90)
    for edge in edges:
        node = edge["node"]
        ch = node.get("channel", {})
        text_preview = (node.get("text") or "")[:50].replace("\n", " ")
        print(f"{node.get('status', '?'):<12} {ch.get('service', '?'):<20} {(node.get('dueAt') or 'queue'):<22} {text_preview}")


def cmd_delete(post_id):
    """Delete a post by ID."""
    data = graphql("""
        mutation($input: DeletePostInput!) {
            deletePost(input: $input) {
                ... on PostActionSuccess { post { id } }
                ... on NotFoundError { message }
                ... on UnauthorizedError { message }
                ... on UnexpectedError { message }
            }
        }
    """, {"input": {"id": post_id}})

    result = data.get("deletePost", {})
    if "message" in result and "post" not in result:
        print(f"Error: {result['message']}", file=sys.stderr)
        sys.exit(1)

    print(f"Post {post_id} deleted.")


def cmd_promote(post_id):
    """Promote a draft to the queue. Fetches the draft, creates a queued copy, deletes the draft."""

    # Fetch the draft details
    data = graphql("""
        query($input: PostsInput!, $first: Int) {
            posts(input: $input, first: $first) {
                edges {
                    node {
                        id text status
                        channel { id name service }
                        assets { id type source thumbnail mimeType }
                    }
                }
            }
        }
    """, {"input": {"organizationId": ORG_ID}, "first": 50})

    # Find the draft
    draft = None
    for edge in data.get("posts", {}).get("edges", []):
        if edge["node"]["id"] == post_id:
            draft = edge["node"]
            break

    if not draft:
        print(f"Post {post_id} not found.", file=sys.stderr)
        sys.exit(1)

    if draft["status"] != "draft":
        print(f"Post {post_id} is not a draft (status: {draft['status']}). Only drafts can be promoted.", file=sys.stderr)
        sys.exit(1)

    channel_id = draft["channel"]["id"]
    channel_name = f"{draft['channel']['service']} — {draft['channel']['name']}"
    text = draft["text"]

    # Create the queued post from the draft
    print(f"Promoting draft to queue: {channel_name}", file=sys.stderr)
    cmd_create_post(
        channel_id,
        text,
        mode="addToQueue",
    )

    # Delete the original draft
    del_data = graphql("""
        mutation($input: DeletePostInput!) {
            deletePost(input: $input) {
                ... on PostActionSuccess { post { id } }
                ... on NotFoundError { message }
                ... on UnauthorizedError { message }
                ... on UnexpectedError { message }
            }
        }
    """, {"input": {"id": post_id}})

    print(f"  Original draft {post_id} deleted.")


# ── CLI ─────────────────────────────────────────────────────────────────────

def print_usage():
    print(__doc__)


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        print_usage()
        sys.exit(0)

    command = args[0].lower()

    if command == "account":
        cmd_account()

    elif command == "channels":
        cmd_channels()

    elif command in ("now", "queue", "schedule", "draft"):
        if len(args) < 3:
            print(f"Usage: buffer_publish.py {command} <channel> \"<text>\" [--video URL] [--image URL] [--date ISO8601]", file=sys.stderr)
            sys.exit(1)

        channel_arg = args[1]
        text = args[2]
        due_at = None
        video_url = None
        image_url = None

        i = 3
        while i < len(args):
            if args[i] == "--date" and i + 1 < len(args):
                due_at = args[i + 1]
                i += 2
            elif args[i] == "--video" and i + 1 < len(args):
                video_url = args[i + 1]
                i += 2
            elif args[i] == "--image" and i + 1 < len(args):
                image_url = args[i + 1]
                i += 2
            else:
                i += 1

        if command == "now":
            cmd_create_post(channel_arg, text, mode="shareNow", video_url=video_url, image_url=image_url)
        elif command == "queue":
            cmd_create_post(channel_arg, text, mode="addToQueue", video_url=video_url, image_url=image_url)
        elif command == "schedule":
            cmd_create_post(channel_arg, text, mode="customScheduled", due_at=due_at, video_url=video_url, image_url=image_url)
        elif command == "draft":
            cmd_create_post(channel_arg, text, save_to_draft=True, video_url=video_url, image_url=image_url)

    elif command == "delete":
        if len(args) < 2:
            print("Usage: buffer_publish.py delete <post_id>", file=sys.stderr)
            sys.exit(1)
        cmd_delete(args[1])

    elif command == "promote":
        if len(args) < 2:
            print("Usage: buffer_publish.py promote <post_id>", file=sys.stderr)
            sys.exit(1)
        cmd_promote(args[1])

    elif command == "posts":
        channel = None
        status = None
        i = 1
        while i < len(args):
            if args[i] == "--channel" and i + 1 < len(args):
                channel = args[i + 1]
                i += 2
            elif args[i] == "--status" and i + 1 < len(args):
                status = args[i + 1]
                i += 2
            else:
                i += 1
        cmd_posts(channel, status)

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
