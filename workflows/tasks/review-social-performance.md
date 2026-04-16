# Review Social Performance — Task Workflow

## Objective

Pull and analyze social media engagement metrics across Facebook, LinkedIn, and Instagram to identify what's working, what's not, and recommend adjustments.

## Required Inputs

| Input | Source | Example |
|-------|--------|---------|
| **Time period** | User request or default to last 7 days | `last 7 days`, `April 2026` |
| **Channels** | All active or specific platform | `all`, `linkedin only` |

## Steps

### 1. Pull Post Performance from Buffer

Call `list_posts` for each channel to get recent posts with engagement data.

For each post, capture:
- Post text (first 100 chars for identification)
- Published date
- Likes / reactions
- Comments
- Shares / reposts
- Clicks (if available)
- Reach / impressions (if available)

### 2. Organize by Platform

Group posts by platform and sort by engagement rate (interactions / reach, or total interactions if reach unavailable).

### 3. Analyze Patterns

Look for:
- **Top performers:** Which topics, formats, or tones drove the most engagement?
- **Bottom performers:** What fell flat? Was it timing, topic, or tone?
- **Platform differences:** Does the same topic perform differently on FB vs LI?
- **Question quality:** Did posts with direct questions get more comments?
- **Posting time correlation:** Any time-of-day patterns?

### 4. Generate Report

Format as:

```
## Social Performance Report — [Time Period]

### Summary
- Total posts: X
- Total engagement: X (likes + comments + shares)
- Avg engagement per post: X
- Best performer: [post summary] — [X interactions]
- Worst performer: [post summary] — [X interactions]

### Facebook
| Date | Post (truncated) | Likes | Comments | Shares | Total |
|------|-----------------|-------|----------|--------|-------|
| ...  | ...             | ...   | ...      | ...    | ...   |

**FB Insight:** [1-2 sentence observation]

### LinkedIn
| Date | Post (truncated) | Likes | Comments | Shares | Total |
|------|-----------------|-------|----------|--------|-------|
| ...  | ...             | ...   | ...      | ...    | ...   |

**LI Insight:** [1-2 sentence observation]

### Recommendations
1. [Specific, actionable recommendation]
2. [Specific, actionable recommendation]
3. [Specific, actionable recommendation]
```

### 5. Deliver Report

- Output directly to the user if on-demand
- If part of the monthly rhythm: create as a ClickUp task in the PERFORMANCE folder

## Available Tools

| Priority | Tool | Usage |
|----------|------|-------|
| 1 (MCP) | **Buffer** — `list_posts` | Pull post data and engagement metrics |
| 2 (MCP) | **Windsor.ai** — `get_data` | Cross-platform analytics if deeper metrics needed |
| 3 (MCP) | **ClickUp** — `clickup_create_task` | Store report in PERFORMANCE folder |

## Edge Cases

- **Buffer doesn't return engagement data for some posts:** Some platforms limit API metric access. Note which metrics are unavailable and suggest checking natively.
- **No posts in the period:** Report that no posts were found. Recommend checking if Buffer queue is empty or if there were scheduling issues.
- **Instagram metrics limited:** Instagram API often restricts reach/impression data. Work with what's available.
