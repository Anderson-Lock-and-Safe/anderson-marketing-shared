# Task Reporting Protocol

Every agent MUST follow this protocol when working on and completing ClickUp tasks. The task itself is the record of work — if it's not in the task, it didn't happen.

## During Work

When you start a task:
1. Set status to **"In Progress"**
2. Post a comment: `🔄 Starting work on this task. [1-sentence summary of approach]`

If work spans multiple steps, post progress comments as you go. Don't go silent for long stretches.

## On Completion

When you finish a task, post a **Task Report** comment using this exact format:

```
✅ TASK COMPLETE

## What Was Done
[Bullet list of specific actions taken. Be precise — not "analyzed ads" but "pulled Google Ads performance for Apr 8-14, compared CPL across 4 campaigns"]

## How It Was Done
[Which workflows and tools were used. Reference specific files.]
- Workflow: `workflows/tasks/analyze-ppc-performance.md`
- Tools: `gads_get_performance`, `msads_get_performance`

## Results
[The actual output — data, recommendations, content created, etc. This is the meat.]

## Key Learnings
[Anything discovered that should inform future work. Rate limits hit, unexpected data, patterns noticed, workflow gaps.]

## Blockers / Follow-ups
[Anything that couldn't be completed and why. Next steps needed. Tasks to create.]

## Time & Resources
[API calls made, credits used (Apollo), posts scheduled, emails drafted — anything with a cost or count.]
```

Then update the task:
- **Status:** "Review" if Garrett needs to approve something, "Complete" if fully done
- **Description:** Update if the original instructions turned out to be incomplete or wrong

## When Blocked

If you hit a blocker you can't resolve:
1. Post a comment explaining what's blocking you and what you've tried
2. Set status to **"Blocked"** (or "Review" if that status doesn't exist)
3. Send a Google Chat message to the Claude Code Remote space:
   `🚧 Blocked on [task name]: [1-sentence summary]. Need Garrett's input.`

## When Needs Approval

If the task requires Garrett's sign-off before final action:
1. Post your recommendation with supporting data
2. Clearly state what you're asking for: "Approve these 12 negative keywords" or "Approve activating the win-back flow"
3. Set status to **"Review"**
4. Do NOT take the action until status is changed back to "In Progress" or "Approved"

## Examples

### Good Task Report
```
✅ TASK COMPLETE

## What Was Done
- Pulled Google Ads performance for Apr 8-14 (7 days)
- Pulled Bing Ads performance for same period
- Pulled Meta Ads performance (last 30 days — no spend in last 7)
- Generated cross-platform comparison table

## How It Was Done
- Workflow: `workflows/tasks/analyze-ppc-performance.md`
- Tools: `gads_get_performance` (customer 9492021070), `msads_get_performance` (daily), `meta_get_account_insights` (act_467834931528348)

## Results
| Platform | Clicks | Spend | Conversions | CPL |
|----------|--------|-------|-------------|-----|
| Google   | 688    | $3,199 | 158        | $20.25 |
| Bing     | 1,556  | $2,062 | 986        | $2.09 |
| Meta     | 0      | $0    | 0           | N/A |

Bing CPL is 10x lower than Google. However, Bing "conversions" may be tracking different actions — needs investigation.

## Key Learnings
- Meta has had no spend since Apr 14. Campaigns may be paused.
- Bing conversion rate (62%) seems unrealistically high — likely tracking page views or clicks, not leads.
- Google Ads cost spikes on weekends (Apr 12-13) but conversions drop.

## Blockers / Follow-ups
- Need to verify Bing conversion tracking setup before drawing ROI conclusions
- Meta: investigate why no spend — create follow-up task

## Time & Resources
- 3 API calls (one per platform)
- No credits consumed
```

### Bad Task Report (DON'T do this)
```
Done. Looked at the ads. Google is doing okay, Bing looks good. Meta isn't spending.
```

## Protocol for All Agents

This protocol applies to every agent equally. Reference this document in your agent prompt. The quality of task reporting directly affects Garrett's ability to make decisions and trust the system.
