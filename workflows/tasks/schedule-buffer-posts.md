# Schedule Buffer Posts — Task Workflow

## Objective

Schedule one or more social media posts to Buffer for publishing via the Buffer MCP tools.

## Required Inputs

| Input | Source | Example |
|-------|--------|---------|
| **Post copy** | Output from `generate-engagement-post.md` or user-provided | Full post text |
| **Platform** | `facebook`, `linkedin`, or `instagram` | `linkedin` |
| **Scheduled date/time** | Content calendar or user request | `2026-04-27 10:00 AM MST` |

## Tool

```
python tools/buffer_publish.py <command> <channel> "<text>" [options]
```

Reads `BUFFER_TOKEN` from `.env` automatically. Requires no external dependencies.

## Channel Shortcuts

| Shortcut | Platform |
|----------|----------|
| `fb` | Facebook — Anderson Lock and Safe |
| `li` | LinkedIn — anderson-lock-and-safe |
| `ig` | Instagram — andersonlockphx |
| `yt` | YouTube — Anderson Lock and Safe |
| `gbp-phoenix` | Google Business — Phoenix |
| `gbp-chandler` | Google Business — Chandler |
| `gbp-arcadia` | Google Business — Arcadia |

## Steps

### 1. Verify Channels

```bash
python tools/buffer_publish.py channels
```

Confirm the target channel(s) are connected and showing "OK" status.

### 2. Choose Scheduling Mode

| Mode | Command | When |
|------|---------|------|
| **Add to queue** | `queue <channel> "<text>"` | Default — publishes at next available slot in Buffer's schedule |
| **Specific time** | `schedule <channel> "<text>" --date "<ISO8601>"` | When exact timing matters |
| **Save as draft** | `draft <channel> "<text>"` | Needs review before publishing |

**Timezone:** Anderson Lock is in Phoenix, AZ (MST = UTC-7, no daylight saving).
`10:00 AM MST` → `2026-04-27T10:00:00-07:00`

### 3. Create the Post

Example — queue a LinkedIn post:
```bash
python tools/buffer_publish.py queue li "Quick question for our network: How many keys does your facilities team manage across all your properties? We've seen some teams juggling over 500."
```

Example — schedule a Facebook post for a specific time:
```bash
python tools/buffer_publish.py schedule fb "Do you know who has a copy of your building keys? If the answer is 'not exactly,' you're not alone." --date "2026-04-27T10:00:00-07:00"
```

### 4. Verify

```bash
python tools/buffer_publish.py posts --channel li
```

Confirm the post appears in the queue with the correct status and scheduled time.

## Batch Scheduling

When scheduling multiple posts (e.g., a full week):

1. Verify channels once (step 1)
2. Run `queue` or `schedule` for each post
3. Track successes and failures
4. Report a summary: "5/6 posts scheduled successfully. 1 failed: [reason]"

## Expected Output

The tool prints confirmation for each post:
```
Post created successfully!
  ID: 69e104601da155c1ebd5487a
  Channel: Facebook — Anderson Lock and Safe
  Status: draft
  Mode: addToQueue
```

## Edge Cases

- **Auth error:** The BUFFER_TOKEN in `.env` may have expired. Ask Garrett to generate a new one. Document post copy in ClickUp so it's not lost.
- **Channel shows DISCONNECTED:** The platform needs to be reconnected in Buffer settings. Flag for Garrett.
- **Instagram requires images:** Instagram posts must include image assets. The tool currently supports text-only posts. For Instagram, create the post as a draft and note that an image must be added in Buffer's UI.
- **Past date requested:** Buffer won't schedule in the past. Flag the issue and suggest the next available slot.
- **Duplicate detection:** Before scheduling, run `posts --channel <channel>` to check if a similar post is already queued.
